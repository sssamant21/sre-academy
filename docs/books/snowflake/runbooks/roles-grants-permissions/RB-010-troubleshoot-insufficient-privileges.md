# RB-010 — Troubleshoot Insufficient Privileges

**Snowflake DBRE/SRE Production Runbook**  
**Runbook ID:** RB-010  
**Category:** Roles, Grants & Permissions  
**Edition:** Revised Final / Canonical  
**Risk:** High  
**Primary Operator:** Authorized Snowflake Administrator / DBRE  
**Supporting Teams:** Security / IAM / Data Owner / Application Owner / Platform Engineering

> **Core principle:** An insufficient-privileges error is evidence to investigate, not authorization to grant more access. Identify the actual execution identity, execution model, exact operation, exact securable object, and effective privilege path before making any change. If an exact authorization gap cannot be proven, do not grant additional privileges.

## 1. Purpose

Use RB-010 when a Snowflake workload fails because the executing identity appears to lack authorization.

Typical symptoms include insufficient privileges, object does not exist or not authorized, database/schema or warehouse authorization failures, DML/object creation failures, stored-procedure or task authorization failures, role/context mismatches, and existing objects working while newly created objects fail.

```text
FAILURE → PRESERVE EVIDENCE → EXECUTION IDENTITY → EXECUTION MODEL → ROLE/SESSION CONTEXT → EXACT OPERATION → EXACT OBJECT → EFFECTIVE PRIVILEGE PATH → ROOT CAUSE → AUTHORIZATION → RB-009 REMEDIATION → ORIGINAL-PATH VALIDATION → SECURITY-BOUNDARY VALIDATION
```

RB-010 determines **why access fails**. RB-009 governs **how an authorized access change is made**.

## 2. Trigger / Alert

- SQL access-control or insufficient-privileges error.
- Object does not exist or not authorized.
- Cannot use warehouse or access database/schema.
- SELECT/INSERT/UPDATE/DELETE/CREATE operation fails.
- Procedure or task authorization failure.
- Role appears assigned but access fails.
- Application fails while engineer succeeds.
- Old objects work while new objects fail.
- Previously working access stopped after a change.

## 3. Impact

Privilege failures can affect production applications, ETL/ELT, scheduled workloads, BI/reporting, deployments, data synchronization, administration, incident response, and customer-facing services. Incorrect troubleshooting can introduce excessive access, privilege escalation, sensitive-data exposure, role blast radius, future access drift, security-policy bypass, or outages caused by incorrect revocation.

## 4. Severity

| Condition | Suggested Classification |
|---|---|
| Single non-production user | Low/Medium |
| Production user blocked | Medium |
| Production pipeline blocked | High |
| Critical application unavailable | High/Critical |
| Multiple workloads suddenly fail | High |
| Administrative workflow blocked | High |
| Unauthorized privilege change suspected | Security Incident |
| Unexpected privilege escalation | Security Incident |

Organizational incident policy takes precedence.

## 5. Mandatory Diagnostic Safety Gate

Before changing any privilege confirm: correct account/environment; original error, code, query ID and timestamp; actual execution identity and type; execution model; exact operation/object/type; primary and secondary-role context; warehouse/database/schema; user/role/database-role hierarchy; direct-user and parent privileges; managed access/ownership; procedure or task execution semantics where applicable; future grants for new-object failures; policy/governance behavior; application/session configuration; recent changes; exact proven privilege gap; and authorization for remediation.

Until the exact gap is established:

```text
NO GRANT
NO REVOKE
NO OWNERSHIP TRANSFER
NO ROLE ESCALATION
```

## 6. Security Stop

Stop routine troubleshooting and involve Security/IAM for unexplained loss of access, unauthorized privilege or hierarchy changes, unexpected administrative roles or OWNERSHIP, unexpected direct grants, policy bypass, security containment, or suspected privilege escalation/account compromise. Preserve evidence before mutation.

## 7. Preserve the Original Failure

Capture exact error, error code, query ID, timestamp, Snowflake user, application/client, configured role, warehouse, database, schema, object, and operation before remediation whenever possible.

## 8. Never Diagnose by Escalating Access

Do not progressively grant broader roles, SYSADMIN, SECURITYADMIN, ACCOUNTADMIN, ALL PRIVILEGES, OWNERSHIP, or WITH GRANT OPTION to discover whether authorization is involved. Use evidence → privilege trace → exact gap → authorization → minimum fix.

## 9. Verify Administrative Context

```sql
SELECT
    CURRENT_ACCOUNT(),
    CURRENT_REGION(),
    CURRENT_USER(),
    CURRENT_ROLE(),
    CURRENT_SECONDARY_ROLES(),
    CURRENT_WAREHOUSE(),
    CURRENT_DATABASE(),
    CURRENT_SCHEMA();
```

This is the administrator's diagnostic context, not necessarily the failing workload context.

## 10. Identify Actual Execution Identity and Model

Determine whether execution is interactive, application/service account, procedure, task, ETL/BI identity, or other automation. The reporter may not be the Snowflake identity producing the error.

For a known user:

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

Confirm NAME, LOGIN_NAME, TYPE, DISABLED and DEFAULT_ROLE as applicable.

For applications capture account, user, authentication model, configured role, warehouse, database, schema and technical owner.

## 11. Reconstruct the Failing Session

Determine USER, PRIMARY ROLE, SECONDARY ROLES, WAREHOUSE, DATABASE, SCHEMA, OBJECT, OPERATION and CLIENT/APPLICATION.

Where safe:

```sql
SELECT CURRENT_ROLE(), CURRENT_SECONDARY_ROLES();
```

A user possessing a role does not prove the failing session effectively used it.

## 12. Inspect User, Role and Hierarchy

```sql
SHOW GRANTS TO USER "<username>";
SHOW GRANTS TO ROLE "<role_name>";
SHOW GRANTS OF ROLE "<role_name>";
```

Consider direct-user privileges, primary/secondary roles, child/parent inheritance and all relevant consumers. Do not trust role names as evidence of privilege content.

## 13. Database Roles

```sql
SHOW DATABASE ROLES IN DATABASE "<database>";
SHOW GRANTS TO DATABASE ROLE "<database>"."<database_role>";
```

Trace object privilege → database role → account role → user. Database roles are not activated directly as primary session roles; identify the account role through which they are inherited.

## 14. Identify Exact Operation and Object

Translate the failure to the exact operation: SELECT, INSERT, UPDATE, DELETE, TRUNCATE, CREATE, ALTER, DROP, EXECUTE, OPERATE, USAGE, or another precise operation.

Capture fully qualified `DATABASE.SCHEMA.OBJECT` and object type. Prefer fully qualified names during controlled diagnosis to remove database/schema-resolution ambiguity.

## 15. Object Resolution vs Authorization

For `Object does not exist or not authorized`, investigate both object resolution and authorization. Verify account, database, schema, object name/type, identifier case, existence and authorization before changing grants.

Examples:

```sql
SHOW TABLES LIKE '<table_name>' IN SCHEMA "<database>"."<schema>";
SHOW VIEWS LIKE '<view_name>' IN SCHEMA "<database>"."<schema>";
```

Quoted mixed-case identifiers can represent different objects from unquoted identifiers.

## 16. Common Query Authorization Chain

For a typical warehouse-backed query investigate compute authorization, required database parent authorization, required schema parent authorization and the operation-specific object privilege. This is a common diagnostic path, not a universal formula for every Snowflake securable object.

Do not add more data privileges when the actual gap is warehouse authorization, and do not duplicate object grants when a required parent authorization is missing.

## 17. Stored Procedures

Separate caller invocation authorization from internal execution authorization. Determine the execution model: owner's rights, caller's rights, or restricted caller's rights where applicable.

For owner's-rights execution, investigate the owner's effective authorization for internal operations rather than automatically granting referenced-object privileges to the caller. For caller's-rights execution, trace the caller's effective privileges. For restricted caller's rights, investigate caller privileges plus applicable caller grants and verify current Snowflake feature status/semantics before production changes.

If an owner's-rights procedure uses object references, investigate the reference creator, referenced object, required operation and reference authorization before broadening the procedure owner's privileges.

## 18. Tasks

For task authorization failures trace task owner → task execution privileges → compute model → database/schema authorization → SQL-object privileges.

Interactive success under an engineer role does not prove task authorization because the engineer role and task-owner role are different execution contexts.

For user-managed task compute investigate applicable task execution privilege, warehouse authorization and SQL-object privileges. For serverless tasks investigate applicable task execution and managed-task execution privileges plus object authorization; do not automatically grant warehouse access.

For previously working tasks inspect recent ownership transfers, hierarchy changes, revokes, warehouse changes, object changes and task-definition changes.

## 19. Managed Access and Ownership

```sql
SHOW SCHEMAS LIKE '<schema>' IN DATABASE "<database>";
```

In managed-access schemas, centralized grant authority can be expected behavior. Do not transfer ownership merely because an object owner cannot independently grant privileges.

If the problem is fundamentally ownership, route to **RB-011 — Troubleshoot Object Ownership**. Do not solve ordinary read/write failures by transferring OWNERSHIP.

## 20. Existing vs Future Access

When old objects work and new objects fail, investigate future grants before individually granting the new object.

```sql
SHOW FUTURE GRANTS IN DATABASE "<database>";
SHOW FUTURE GRANTS IN SCHEMA "<database>"."<schema>";
```

Compare scope, object type, privilege, recipient and database/schema rules. Do not assume database-level and schema-level future grants simply combine for the same object type; schema-level future-grant configuration can take precedence for objects created in that schema.

Inspect actual materialized grants on the affected object. For RENAME, SWAP, REPLACE or other lifecycle paths, do not assume future grants materialized as they would for ordinary object creation. Verify future-grant support for unusual securable object types.

## 21. Recent Change Correlation

For regressions ask what changed between the last successful execution and first failure. Investigate GRANT, REVOKE, role assignment/hierarchy, ownership, managed access, future grants, object lifecycle, task ownership, procedure deployment, application role configuration, warehouse configuration and masking/row-access policy changes.

## 22. Query History

Use query history where appropriate:

```sql
SELECT
    QUERY_ID,
    USER_NAME,
    ROLE_NAME,
    WAREHOUSE_NAME,
    DATABASE_NAME,
    SCHEMA_NAME,
    QUERY_TYPE,
    EXECUTION_STATUS,
    ERROR_CODE,
    ERROR_MESSAGE,
    START_TIME
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE USER_NAME = '<username>'
  AND START_TIME >= <incident_start>
ORDER BY START_TIME DESC;
```

Use a narrow incident window. Do not include QUERY_TEXT in default evidence because SQL can contain sensitive values. Account Usage can have latency; for recent incidents use query ID, client error, application logs or an appropriate recent-history source. Absence from a historical view is not proof the query never ran.

## 23. Policy-Controlled Access

A query that succeeds but returns masked values is not automatically missing SELECT. A query that succeeds but returns fewer rows can reflect row-access policy behavior. Do not grant broad roles to bypass masking or row filtering; route such requirements through governance/security authorization.

## 24. Application and Session Configuration

Verify the application's actual account, user, role, warehouse, database, schema and client/driver. DEFAULT_ROLE does not prove the application uses that role because clients can select another role after authentication.

After an authorized change, check connection pools or stale sessions before stacking additional grants. Reconnect or refresh session context when appropriate.

## 25. No Missing Privilege Found

If the expected authorization path appears complete, **STOP GRANTING**. Investigate wrong identity/account/role, secondary-role behavior, database/schema/object context, identifier case, procedure semantics/references, task owner, future-grant behavior, managed access, ownership, masking/row-access policy, application configuration, stale session or unsupported operation.

No additional grant is a valid RB-010 outcome.

## 26. Determine Exact Root Cause

Before remediation document identity, execution role, operation, object, present authorization, exact missing component and primary root-cause classification.

Example:

```text
ROOT CAUSE: SCHEMA_PRIVILEGE
Identity: APP_USER
Execution role: APP_READER
Operation: SELECT
Object: PROD_DB.L1.TABLE_A
Present: warehouse authorization, database parent authorization, SELECT ON TABLE
Missing: required schema parent authorization
```

A valid non-grant result is:

```text
ROOT CAUSE: ACTIVE_ROLE
Expected role: APP_READER
Actual role: PUBLIC
Privilege gap: NONE
Snowflake grant change required: NO
```

## 27. Root-Cause Taxonomy

Use one primary category where possible: ROLE_ASSIGNMENT, ACTIVE_ROLE, SECONDARY_ROLE, DIRECT_USER_GRANT, ROLE_HIERARCHY, DATABASE_ROLE, WAREHOUSE_PRIVILEGE, DATABASE_PRIVILEGE, SCHEMA_PRIVILEGE, OBJECT_PRIVILEGE, MANAGED_ACCESS, OWNERSHIP, FUTURE_GRANT, FUTURE_GRANT_PRECEDENCE, FUTURE_GRANT_MATERIALIZATION, OBJECT_CONTEXT, OBJECT_TYPE, IDENTIFIER_CASE, APPLICATION_CONFIGURATION, STALE_SESSION, MASKING_POLICY, ROW_ACCESS_POLICY, PROCEDURE_OWNER_RIGHTS, PROCEDURE_CALLER_RIGHTS, PROCEDURE_RESTRICTED_CALLER_RIGHTS, PROCEDURE_REFERENCE_AUTHORIZATION, TASK_EXECUTE_PRIVILEGE, TASK_SERVERLESS_PRIVILEGE, TASK_WAREHOUSE_PRIVILEGE, TASK_OBJECT_PRIVILEGE, UNAUTHORIZED_CHANGE, OTHER.

## 28. Authorization and Remediation

A technically missing privilege is not automatically authorized. Confirm business requirement, identity, role, approval, role consumers, sensitive-data boundary, scope and existing-vs-future requirement.

If an authorized privilege gap is proven, use **RB-009 — Grant User/Role Access** for the production mutation. RB-010 records root cause, exact missing privilege, target role/object/scope, evidence and authorization.

Remediate only the exact proven cause. Wrong role → correct session/application role. Missing warehouse privilege → only approved compute authorization. Missing object privilege → only approved object privilege. Broken future-grant design → approved governed future-grant repair.

## 29. Shared Role, Delegation and Administrative Safety

Before modifying a shared role, identify all consumers. If the blast radius exceeds authorization, use a narrower governed role.

Do not add WITH GRANT OPTION for ordinary privilege-use failures. Never use ALL PRIVILEGES, SYSADMIN, SECURITYADMIN or ACCOUNTADMIN as diagnostic experiments.

## 30. Validation

Retest through the original workload path wherever possible: same identity, intended role model, application/client, compute model, object and operation.

For controlled interactive validation:

```sql
SELECT
    CURRENT_ACCOUNT(),
    CURRENT_USER(),
    CURRENT_ROLE(),
    CURRENT_SECONDARY_ROLES(),
    CURRENT_WAREHOUSE(),
    CURRENT_DATABASE(),
    CURRENT_SCHEMA();
```

Validate the approved operation using safe, non-sensitive testing. Then verify the security boundary: no unapproved databases/schemas/tables, DML, CREATE, OWNERSHIP, delegation, administrative roles, sensitive-data exposure or unexpected inheritance.

Do not perform destructive negative tests such as DROP, DELETE, TRUNCATE or ALTER against production merely to prove denial. Use SHOW GRANTS, hierarchy inspection, metadata and controlled test objects where appropriate.

## 31. Rollback

If RB-009 introduced an incorrect remediation, identify the exact delta, confirm it belongs to the incident change, revoke only that delta and retest. Do not revoke unrelated pre-existing access.

If the pre-change state itself contained unauthorized access, do not automatically restore it. Preserve evidence and involve Security/IAM.

## 32. Escalation

| Finding | Route |
|---|---|
| Exact authorized privilege missing | RB-009 |
| Ownership problem | RB-011 |
| Accidentally revoked access | RB-012 |
| Broad permission audit required | RB-013 |
| Access should be removed | RB-014 |
| Authentication problem | RB-003 |
| Task operational failure beyond authorization | RB-041/RB-043 |
| Policy/governance restriction | Security/Data Governance |
| Unauthorized privilege change | RB-079 / Security |
| Platform behavior unclear after evidence collection | Snowflake Support |

## 33. Evidence to Capture

Record account/region/environment; incident/reporter/service; failing user/type/application; execution model; exact error/code/query ID/time; client; configured/primary/secondary roles; warehouse/database/schema/object/type/operation; user/role/database-role/hierarchy/direct grants; warehouse/database/schema/object privileges; managed-access and owner; procedure mode/reference; task owner/compute/execution/warehouse privileges; database/schema future grants and precedence/materialization; object lifecycle event; recent grant/revoke/role/ownership changes; masking/row policies; application/session checks; no-missing-privilege branch; root cause and exact gap; authorization/approver; RB-009 change reference; original-path and security-boundary validation; rollback/security escalation; operator/completion timestamp.

## 34. Never Capture

Never capture passwords, temporary passwords, private keys, MFA codes, OAuth/session tokens, secrets, credential-bearing connection strings, sensitive production result sets or unnecessary sensitive SQL literals. Redact logs before attaching them to incident records.

## 35. Quick Production Procedure

1. Preserve exact error/code/query ID/time.
2. Verify account/environment.
3. Identify actual execution identity and type.
4. Identify execution model/application/client.
5. Identify primary/secondary roles and warehouse.
6. Identify database/schema, exact operation, fully qualified object and object type.
7. Verify object existence and identifier/case.
8. Inspect user/direct grants, account-role grants, hierarchy and database roles.
9. Trace compute, database, schema and object authorization.
10. Check managed access and ownership.
11. Check procedure execution mode/references or task owner/execution/compute as applicable.
12. Inspect future grants, precedence and materialized grants for new-object failures.
13. Check recent changes and policy behavior.
14. Verify application configuration and stale/pooled sessions.
15. Determine exact root cause.
16. If no gap exists, STOP GRANTING.
17. If a gap exists, verify authorization and route mutation through RB-009.
18. Retest the original workload path and validate session context.
19. Validate required operation and security boundary.
20. Capture root-cause classification/evidence and close or escalate.

## 36. Production Guardrails

**Always:** preserve evidence; identify actual execution identity/model; reconstruct original context; inspect primary/secondary roles; use exact object identity; distinguish resolution from authorization; trace compute/parent/object privileges and role/database-role inheritance; consider direct grants; check managed access/ownership; distinguish procedure/task execution models; investigate future grants for new-object regressions; distinguish policies from privilege failures; verify application/session state; prove exact gap; verify authorization; route grants through RB-009; validate original path and security boundary.

**Never:** start with a GRANT; add broader roles until the query works; use ACCOUNTADMIN/ALL PRIVILEGES as diagnostic shortcuts; transfer OWNERSHIP for ordinary access; add WITH GRANT OPTION during troubleshooting; assume reporter equals execution identity; assume role membership equals active role; assume CURRENT_ROLE explains all effective access; assume object-not-found proves absence; assume task uses engineer privileges; assume procedures use caller privileges; bypass policies; perform destructive negative tests; or keep granting when the expected authorization path is complete.

## 37. Canonical Decision

**RB-010 — Troubleshoot Insufficient Privileges: REVISED FINAL / CANONICAL EDITION APPROVED**

Seven non-negotiable production principles:

1. Preserve the original failure and do not change privileges until an exact authorization gap is proven.
2. Troubleshoot the actual Snowflake execution identity and execution model, not merely the reporter or an administrator reproducing SQL.
3. Trace effective authorization across primary/secondary roles, hierarchy, database roles, compute, parent objects, object privileges and applicable direct grants.
4. Treat procedures, tasks, managed-access schemas, future grants, ownership and policy-controlled data access as distinct authorization models.
5. If the expected authorization path is complete, stop granting and investigate object resolution, execution semantics, application configuration, policies or session state.
6. A technically missing privilege is not automatically authorized; production access changes must route through RB-009.
7. Resolution requires validation through the original workload path and confirmation that the approved security boundary remains intact.

## References

Use current official Snowflake documentation for access-control privileges and inheritance, database roles, managed-access schemas, future grants, stored-procedure execution rights, restricted caller rights/references, task privileges and query history. Verify Preview-feature status before production changes where applicable.
