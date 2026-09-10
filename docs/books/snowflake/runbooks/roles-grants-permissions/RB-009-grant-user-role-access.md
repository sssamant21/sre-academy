# RB-009 — Grant User/Role Access

**Snowflake DBRE/SRE Production Runbook**  
**Runbook ID:** RB-009  
**Category:** Roles, Grants & Permissions  
**Edition:** Revised Final / Canonical  
**Risk:** High  
**Primary Operator:** Authorized Snowflake Administrator / DBRE  
**Supporting Teams:** Security / IAM / Data Owner / Application Owner / Platform Engineering

> **Core principle:** Grant the minimum approved privilege through the correct governed role, at the correct scope, to the correct identity. A production access change is successful only when the required access works, unintended consumers have not gained access, the approved security boundary remains intact, and the exact change can be audited and reversed.

## 1. Purpose

Use RB-009 to provision authorized Snowflake access for human users, service/application identities, account roles, database roles, production support teams, data consumers, and engineering teams.

Production lifecycle:

```text
REQUEST → AUTHORIZATION → IDENTITY → EXACT REQUIREMENT → EXISTING ACCESS → ROLE/HIERARCHY → BLAST RADIUS → MINIMUM PRIVILEGE → CHANGE → VALIDATION → AUDIT
```

RB-009 is for authorized provisioning. If expected access already exists but the workload receives an authorization error, use **RB-010 — Troubleshoot Insufficient Privileges**.

## 2. Trigger / Alert

Use this runbook for approved requests to grant production read/DML access, add a user to an approved role, provide warehouse `USAGE`, grant application/schema access, assign database roles, grant current-object access, explicitly approved future-object access, or temporary production access.

## 3. Impact

Incorrect grants can expose production data, PII/PHI, financial/confidential information, future datasets, compute resources, integrations, or administrative capabilities. Role-hierarchy changes can affect many identities simultaneously. Treat production grants as security-sensitive production changes.

## 4. Severity

| Condition | Suggested Classification |
|---|---|
| Routine approved access | Normal Change |
| Deployment blocked by access | Medium |
| Critical application blocked | High |
| Production outage caused by missing privilege | High/Critical |
| Unauthorized grant / suspected escalation | Security Incident |
| High-privilege administrative-role request | High-Risk Security Change |

Organizational incident/change policy takes precedence.

## 5. Mandatory Safety Gate

Before any production `GRANT`:

```text
[ ] Correct account/region/environment verified
[ ] Request/ticket, requester, target identity, and approval verified
[ ] Identity TYPE and business requirement understood
[ ] Exact privilege and object/scope identified
[ ] Existing user and role access inspected
[ ] Role consumers and hierarchy understood
[ ] Account role vs database role determined
[ ] Grant authority identified
[ ] Managed-access status checked where relevant
[ ] Direct-user grant avoided or exception approved
[ ] WITH GRANT OPTION explicitly evaluated
[ ] Existing-object and future-object requirements separately determined
[ ] Future-grant precedence checked where relevant
[ ] Sensitive-data controls considered
[ ] OWNERSHIP / ALL PRIVILEGES not used as shortcuts
[ ] Exact rollback/revoke path documented
```

If authorization cannot be established: **STOP.**

## 6. SECURITY STOP

Stop routine provisioning and involve Security/IAM/Data Governance when the requester cannot be verified; approval is absent or suspicious; requested access exceeds business need; sensitive-data approval is missing; unexpected administrative access exists; privilege escalation is suspected; broad administrative access is unexpectedly requested; governance controls would be bypassed; unexplained `OWNERSHIP` is requested; unauthorized future/direct grants exist; or the change conflicts with security containment.

Never grant broad temporary access while waiting for authorization.

## 7. Verify Administrative Context

```sql
SELECT
    CURRENT_ACCOUNT(),
    CURRENT_REGION(),
    CURRENT_USER(),
    CURRENT_ROLE(),
    CURRENT_SECONDARY_ROLES();
```

Hard STOP if account, environment, identity, or administrative role is unexpected. Use the lowest approved administrative role with legitimate grant authority; do not automatically use `ACCOUNTADMIN`.

## 8. Translate the Request

Every request must identify **WHO, WHAT, WHERE, WHY, HOW, and WHEN**. A vague request such as “give this user production database access” is not sufficiently defined.

## 9. Verify Target User

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

Confirm `NAME`, `LOGIN_NAME`, `TYPE`, `DISABLED`, and `DEFAULT_ROLE`. Do not identify the target solely by display name or ticket text.

## 10. PERSON vs Service Identity

For service/application identities record application, environment, technical/business owner, purpose, authentication model, required role, and lifecycle owner. Do not give service identities broad interactive administrative access merely to simplify troubleshooting.

## 11. Preferred Production Model

Prefer:

```text
PRIVILEGE → GOVERNED ROLE → IDENTITY
```

rather than direct privilege-to-user grants. Role-based access provides cleaner governance, audit, revocation, lifecycle management, and privilege review.

## 12. Direct User Grants

Snowflake supports direct user privileges, but production use should normally be exceptional. Before a direct-user grant confirm a role-based solution was evaluated, the exception is documented and permitted, the requested privilege supports direct grant, no FUTURE/CREATE/OWNERSHIP requirement exists, secondary-role behavior is understood, and a revocation owner is identified.

## 13. Inspect Existing User Access

```sql
SHOW GRANTS TO USER "<username>";
```

Identify existing roles, direct privileges, duplicate access, and unexpected elevated access before adding anything.

## 14. Inspect Existing Account Role

```sql
SHOW GRANTS TO ROLE "<role_name>";
SHOW GRANTS OF ROLE "<role_name>";
```

Determine what the role can do and which users, applications, parent roles, and indirect consumers inherit it.

## 15. Shared-Role Blast Radius

A privilege added to a shared role changes what every consumer can potentially inherit. Role names are not security evidence; inspect actual grants and consumers.

## 16. Object Grant vs Role Assignment

```sql
GRANT SELECT ON TABLE DB1.S1.T1 TO ROLE DATA_READER;
```

changes what `DATA_READER` can do.

```sql
GRANT ROLE DATA_READER TO USER USER1;
```

changes what `USER1` inherits. Record which layer is being changed.

## 17. Existing Role vs New Role

Use an existing governed role only when purpose, scope, consumers, privilege boundary, and ownership match. Design/request a separate governed role when existing roles are too broad, lifecycle/data boundaries differ, sensitive-data boundaries differ, temporary access needs isolation, or modifying a shared role would expose unrelated consumers. Avoid uncontrolled role proliferation.

## 18. Account Roles vs Database Roles

Use database roles for privileges contained within one database. Use account roles for warehouses, account objects, cross-database responsibilities, database-role aggregation, and user assignment. Database roles are not directly activated as the session role.

## 19. Recommended Database Role Pattern

```text
DATABASE ROLE → database/schema/object privileges → ACCOUNT ROLE → USER
```

```sql
GRANT DATABASE ROLE "<database>"."<database_role>" TO ROLE "<account_role>";
GRANT ROLE "<account_role>" TO USER "<username>";
USE ROLE "<account_role>";
```

Do not attempt `USE ROLE "<database_role>"`.

## 20. Inspect Database Roles

```sql
SHOW DATABASE ROLES IN DATABASE "<database>";
SHOW GRANTS TO DATABASE ROLE "<database>"."<database_role>";
```

Confirm the database role represents the intended authorization boundary.

## 21. Warehouse Authorization

```sql
GRANT USAGE ON WAREHOUSE "<warehouse>" TO ROLE "<account_role>";
```

Do not grant `OPERATE`, `MODIFY`, or `OWNERSHIP` when only query execution is required.

## 22. Common Read Privilege Chain

Typical query access requires warehouse `USAGE`, database `USAGE`, schema `USAGE`, and table/view `SELECT`. A table `SELECT` grant alone may be insufficient. Grant only missing approved components.

## 23. Database and Schema USAGE

```sql
GRANT USAGE ON DATABASE "<database>" TO ROLE "<role>";
GRANT USAGE ON SCHEMA "<database>"."<schema>" TO ROLE "<role>";
```

Neither grant alone provides table access.

## 24. Single Table Read Access

```sql
GRANT SELECT ON TABLE "<database>"."<schema>"."<table>" TO ROLE "<role>";
```

Use when authorization is object-specific.

## 25. Existing Tables and Views

```sql
GRANT SELECT ON ALL TABLES IN SCHEMA "<database>"."<schema>" TO ROLE "<role>";
GRANT SELECT ON ALL VIEWS IN SCHEMA "<database>"."<schema>" TO ROLE "<role>";
```

These are broader than single-object grants; review consumers first.

## 26. Existing and Future Access Are Separate

Authorization for current objects does not automatically authorize future objects. Treat them as separate security decisions.

## 27. Mandatory Future-Grant Inspection

```sql
SHOW FUTURE GRANTS IN DATABASE "<database>";
SHOW FUTURE GRANTS IN SCHEMA "<database>"."<schema>";
```

Inspect scope, object type, privilege, recipient, and existing database/schema-level rules.

## 28. Future Grant Precedence

For the same object type, schema-level future grants take precedence for objects created in that schema when both database-level and schema-level future grants exist. Do not assume both scopes simply combine.

## 29. Future Table/View Access

Where explicitly approved:

```sql
GRANT SELECT ON FUTURE TABLES IN SCHEMA "<database>"."<schema>" TO ROLE "<role>";
GRANT SELECT ON FUTURE VIEWS IN SCHEMA "<database>"."<schema>" TO ROLE "<role>";
```

Before execution verify future access approval, object-type support, DB/schema future grants, precedence, consumers, sensitive future datasets, managed-access implications, and applicable sharing/database-role restrictions.

## 30. Existing + Future Read Access

Where both are explicitly authorized:

```sql
GRANT SELECT ON ALL TABLES IN SCHEMA "<database>"."<schema>" TO ROLE "<role>";
GRANT SELECT ON FUTURE TABLES IN SCHEMA "<database>"."<schema>" TO ROLE "<role>";
```

Record these as separate changes. Prefer schema scope when the business requirement is schema-specific.

## 31. Future Grant Lifecycle

A future grant acts as an initial access template when a new object is created. After materialization, the object's privilege state can evolve independently.

## 32. Revoking Future Grants

```sql
REVOKE SELECT ON FUTURE TABLES IN SCHEMA "<database>"."<schema>" FROM ROLE "<role>";
```

This stops future materialization; it does not automatically remove `SELECT` already materialized on existing tables. If separately authorized, existing access may also require:

```sql
REVOKE SELECT ON ALL TABLES IN SCHEMA "<database>"."<schema>" FROM ROLE "<role>";
```

## 33. Future Grant Object Support / Future OWNERSHIP

Verify that the target securable object supports future grants. Do not use future `OWNERSHIP` for routine RB-009 provisioning; route ownership work to RB-011 or a dedicated ownership procedure.

## 34. Managed Access Schemas

```sql
SHOW SCHEMAS LIKE '<schema>' IN DATABASE "<database>";
```

Determine whether the schema is managed access. In a managed-access schema, privilege management is centralized; do not assume an individual object owner can independently grant access. Use the approved schema owner or role with appropriate grant-management authority.

## 35. Grant Authority

Before a privilege grant, identify the legitimate authority path: applicable `MANAGE GRANTS`, `OWNERSHIP`, or the privilege held `WITH GRANT OPTION`, subject to Snowflake object/parent rules. Record the authority path.

`MANAGE GRANTS` is powerful. Mature environments may delegate it through controlled custom roles; do not automatically escalate to `SECURITYADMIN` or `ACCOUNTADMIN`.

## 36. WITH GRANT OPTION

`WITH GRANT OPTION` allows delegation of the privilege. It requires explicit delegation approval and must not be added for ordinary access provisioning.

## 37. DML Access

Translate “write access” into exact privileges such as `INSERT`, `UPDATE`, `DELETE`, or `TRUNCATE`.

```sql
GRANT INSERT, UPDATE ON TABLE "<database>"."<schema>"."<table>" TO ROLE "<role>";
```

Do not grant operations that are not required.

## 38. CREATE Privileges

Before granting `CREATE`, determine object type, business need, schema, resulting ownership/governance, and lifecycle. Example:

```sql
GRANT CREATE TABLE ON SCHEMA "<database>"."<schema>" TO ROLE "<role>";
```

## 39. ALL PRIVILEGES / OWNERSHIP Guardrails

Do not routinely use `GRANT ALL PRIVILEGES`. Explicit privileges provide better authorization, auditability, rollback, and least privilege.

Never solve ordinary SELECT/DML/CREATE access with `OWNERSHIP`; ownership changes administrative control and belongs to RB-011.

## 40. Administrative Roles Are Not Access Shortcuts

Never grant `ACCOUNTADMIN`, `SECURITYADMIN`, `SYSADMIN`, or another broad role simply because a query fails. Use RB-010 to diagnose the actual missing privilege.

## 41. Sensitive Data Gate

Before granting access verify classification, data-owner approval, masking policy, row-access policy, privacy/regulatory requirements, role consumers, and environment. Do not bypass governance controls merely to make a query succeed.

## 42. Temporary Access

Temporary access must record user, role, reason, approver, start, expiration, removal owner, and verification owner. A temporary grant without a reliable removal mechanism is effectively persistent access.

## 43. Role and Hierarchy Assignment

```sql
GRANT ROLE "<role>" TO USER "<username>";
GRANT ROLE "<child_role>" TO ROLE "<parent_role>";
GRANT DATABASE ROLE "<database>"."<database_role>" TO ROLE "<account_role>";
```

Before execution verify role contents, target identity, hierarchy, and upward inheritance blast radius.

## 44. Secondary Roles

`CURRENT_ROLE()` alone may not explain effective access. Validate:

```sql
SELECT
    CURRENT_USER(),
    CURRENT_ROLE(),
    CURRENT_SECONDARY_ROLES(),
    CURRENT_WAREHOUSE();
```

This is especially important with multiple account roles, direct-user privileges, or enabled secondary roles.

## 45. Positive Validation

Validate using the intended approved role set, not an unrelated elevated role:

```sql
USE ROLE "<approved_account_role>";
USE WAREHOUSE "<approved_warehouse>";

SELECT
    CURRENT_USER(),
    CURRENT_ROLE(),
    CURRENT_SECONDARY_ROLES(),
    CURRENT_WAREHOUSE();

SELECT *
FROM "<database>"."<schema>"."<table>"
LIMIT 1;
```

Use a non-sensitive validation query where possible.

## 46. Security-Boundary Validation

Required access working is only half the validation. Confirm the role does not unintentionally possess unapproved DML, CREATE, OWNERSHIP, delegation, broader database access, or sensitive-data access.

Never use destructive production commands such as `DROP`, `TRUNCATE`, or `DELETE` merely to verify denial. Prefer grant metadata, hierarchy inspection, controlled test objects, and non-destructive validation.

## 47. Validate Metadata

```sql
SHOW GRANTS TO ROLE "<role>";
SHOW GRANTS TO DATABASE ROLE "<database>"."<database_role>";
SHOW GRANTS TO USER "<username>";
SHOW FUTURE GRANTS IN DATABASE "<database>";
SHOW FUTURE GRANTS IN SCHEMA "<database>"."<schema>";
```

## 48. Default Role

Granting a role does not mean it should become `DEFAULT_ROLE`. Changing a default role is a separate configuration decision requiring explicit justification.

## 49. Unexpected Existing Access

If investigation finds unexpected administrative roles, `OWNERSHIP`, unauthorized direct/future grants, sensitive-data access, or unexpected hierarchy, do not silently remove it under RB-009. Preserve evidence and route to RB-013, RB-014, RB-079, and/or the Security Incident process.

## 50. Exact-Delta Rollback

Capture pre-change state, exact change, and post-change state. Rollback removes only the delta introduced by RB-009; never revoke unrelated pre-existing access.

Examples:

```sql
REVOKE SELECT ON TABLE "<database>"."<schema>"."<table>" FROM ROLE "<role>";
REVOKE ROLE "<role>" FROM USER "<username>";
REVOKE ROLE "<child_role>" FROM ROLE "<parent_role>";
REVOKE DATABASE ROLE "<database>"."<database_role>" FROM ROLE "<account_role>";
REVOKE SELECT ON FUTURE TABLES IN SCHEMA "<database>"."<schema>" FROM ROLE "<role>";
```

Before revocation confirm the grant was introduced by the current change, pre-existing access is distinguished, consumers/dependencies are understood, and future vs existing behavior is clear. An incorrect revoke can cause a production outage.

If the previous state was itself unauthorized or insecure, do not restore it merely because it was the pre-change state; preserve evidence and involve Security/IAM.

## 51. Emergency Access Boundary

If administrators cannot authenticate and emergency administration is required, use **RB-008 — Emergency / Break-Glass Access**. Do not create ad-hoc emergency administrators through RB-009.

## 52. Escalation

| Condition | Route |
|---|---|
| Missing approval | Data Owner / IAM / Security |
| Authentication problem | RB-003 |
| Existing privilege but operation fails | RB-010 |
| Ownership issue | RB-011 |
| Accidentally revoked access | RB-012 |
| Permission audit | RB-013 |
| Access removal | RB-014 |
| Sensitive-data issue | Data Governance / Security |
| Unauthorized privilege | RB-079 / Security |
| Emergency administrator access | RB-008 |
| Complex platform behavior | Snowflake Support |

## 53. Evidence to Capture

Capture account, region, environment, ticket, requester, approver, data/application owner, target identity/type/owner, business requirement, account/database roles, consumers/parents, grant authority, warehouse/database/schema/object/object type, requested/existing/new privilege, managed-access status, sensitive-data controls, existing/future-object scope, database/schema future grants and precedence, direct-user exception, delegation approval, administrative role used, pre-change state, exact SQL/change/timestamp, validation identity/roles/warehouse/results, temporary-access expiration/removal owner, rollback, unexpected access, security escalation, operator, and completion timestamp.

## 54. Never Capture

Never capture passwords, temporary passwords, private keys, MFA codes, OAuth/session tokens, secrets, unnecessary production data, or sensitive query output.

## 55. Quick Production Procedure

```text
1. Verify account/region/environment and administrative context.
2. Verify request, requester, approval, and target identity.
3. Define exact business requirement, privilege, object, scope, and duration.
4. Inspect existing user grants, candidate role privileges, consumers, and hierarchy.
5. Determine account-role/database-role model and grant authority.
6. Check managed-access status and sensitive-data controls.
7. Prefer governed role; document any direct-user exception.
8. Evaluate WITH GRANT OPTION separately.
9. Determine parent/warehouse requirements.
10. Separate existing-object and future-object authorization.
11. Inspect database/schema future grants and precedence.
12. Capture pre-change state and exact rollback.
13. Execute minimum approved grant.
14. Verify metadata and primary/secondary role context.
15. Validate required operation and security boundary non-destructively.
16. Verify no unintended consumer gained access.
17. Record exact change and schedule temporary-access removal if applicable.
18. Capture evidence and close or escalate.
```

## 56. Production Decision Model

```text
ACCESS REQUEST
   ↓
Authorization valid? ──NO→ STOP
   ↓ YES
Identity verified? ───NO→ STOP
   ↓ YES
Requirement exact? ───NO→ CLARIFY
   ↓ YES
Sensitive/governed data? → verify governance approval
   ↓
Existing governed role?
   ├─ YES → inspect contents/consumers → grant role or minimum privilege
   └─ NO  → design governed role if needed
   ↓
Future access? → explicit approval → inspect DB/schema future grants → understand precedence
   ↓
Grant authority valid? ──NO→ STOP
   ↓ YES
Apply minimum exact change
   ↓
Verify metadata
   ↓
Validate intended role set
   ↓
Required operation works? ──NO→ RB-010
   ↓ YES
Security boundary intact? ──NO→ ROLLBACK / ESCALATE
   ↓ YES
AUDIT → CLOSE
```

## 57. Production Guardrails

**Always:** verify authorization/account/identity; define exact privilege/scope; inspect existing access, consumers, and hierarchy; prefer governed roles; use account/database roles according to their boundaries; verify grant authority and managed-access behavior; treat delegation separately; separate current/future access; inspect future-grant precedence; validate secondary-role context, positive access, and security boundary; prepare exact rollback; audit temporary access.

**Never:** grant solely from an informal request without required approval; blindly grant broader roles until an error disappears; use `ACCOUNTADMIN`, `ALL PRIVILEGES`, or `OWNERSHIP` as shortcuts; add `WITH GRANT OPTION` without approval; modify shared roles without consumer analysis; grant future access without explicit authorization; assume DB/schema future grants combine; bypass masking/row-access controls; use destructive negative tests; revoke unrelated access; or leave temporary access without an exit mechanism.

## 58. Canonical Access Model

```text
BUSINESS REQUIREMENT
        ↓
AUTHORIZATION
        ↓
IDENTITY
        ↓
GOVERNED ACCOUNT ROLE
        ↓
DATABASE ROLE where appropriate
        ↓
MINIMUM OBJECT PRIVILEGES
        ↓
VALIDATION
        ↓
AUDIT
```

Anti-pattern:

```text
ACCESS ERROR → BIGGER ROLE → BIGGER ROLE → ADMIN ROLE
```

If the expected role already exists and access still fails, stop granting and use RB-010.

## 59. References

Primary technical authority for this runbook is current Snowflake documentation covering access control, account roles, database roles, privilege grants, direct-user privileges, future grants, managed-access schemas, secondary roles, grant authority, `WITH GRANT OPTION`, and privilege inheritance. Operational safety gates, blast-radius analysis, validation, evidence, and rollback procedures in this runbook are production DBRE/SRE guidance.

## 60. Canonical Decision

**RB-009 — Grant User/Role Access: REVISED FINAL / CANONICAL EDITION APPROVED**

Non-negotiable principles:

1. Every access change requires verified authorization and an exact identity, privilege, object, scope, and duration.
2. Prefer governed roles over direct-user privileges and evaluate the entire hierarchy/consumer blast radius before modifying a shared role.
3. Use account roles and database roles according to their Snowflake security boundaries.
4. Existing-object and future-object access are separate authorization decisions; database/schema future-grant precedence must be understood.
5. `WITH GRANT OPTION`, `OWNERSHIP`, `ALL PRIVILEGES`, and broad administrative roles are not routine provisioning shortcuts.
6. Validation must prove both required access and the intended security boundary, including primary/secondary-role effects, without destructive testing.

**Workflow:** `Draft → Technical + Source Review → Production + Copyright Review → Revised Final / Canonical Edition → Commit → Status Update → Next Runbook`
