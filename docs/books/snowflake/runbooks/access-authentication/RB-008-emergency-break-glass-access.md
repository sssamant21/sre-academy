# RB-008 — Emergency / Break-Glass Access

**Snowflake DBRE/SRE Production Runbook**  
**Runbook ID:** RB-008  
**Category:** Access & Authentication  
**Edition:** Revised Final / Canonical  
**Risk:** Critical

> **Core principle:** Break-glass access is a pre-provisioned, strongly authenticated, tightly controlled emergency path used only when normal administrative access is unavailable and critical recovery cannot wait. Successful emergency login alone does not constitute recovery: normal administrative access must be restored, emergency access closed, credentials handled according to policy, and all privileged activity accounted for.

## 1. Purpose

Use RB-008 when urgent production Snowflake administration is required and the normal approved administrative authentication path is unavailable or unusable, including IdP/SSO outages, authentication-policy lockout, widespread MFA/authentication failure, security containment affecting normal administrators, or critical production recovery blocked by an authentication incident.

RB-008 governs the emergency-access lifecycle. It does not replace the specialized runbook for repairing the underlying failure.

## 2. Related Runbooks

- RB-001 — Reset User Password
- RB-002 — Unlock/Restore User Access
- RB-003 — Troubleshoot Login/Authentication Failure
- RB-004 — MFA Recovery
- RB-005 — Key-Pair Authentication Failure
- RB-006 — SSO/OAuth Failure
- RB-007 — Network Policy Blocking Access
- RB-009/RB-010 — Role/Privilege Recovery
- RB-078 — Compromised User Credentials
- RB-079 — Unauthorized Privilege Change
- RB-082 — Emergency Credential Rotation
- RB-083/RB-088/RB-089 — Snowflake service/support escalation

## 3. Production Architecture

```text
Normal path:
Administrator → Enterprise IdP/SSO/MFA → Normal admin identity → Snowflake

Emergency path:
Normal path unavailable → Critical recovery → Incident authorization
→ Approved credential vault → Password + OTP/approved MFA
→ Dedicated PERSON emergency user → Approved network path
→ Recovery authentication policy → Snowflake
→ Minimum required administrative role → Defined recovery action
→ Restore normal authentication → Validate normal administrator
→ Close emergency access → Credential/OTP lifecycle → Audit review
```

## 4. Trigger / Alert

Use RB-008 only when no authorized administrator can access production, or critical administrative recovery is required while the normal path is unavailable and normal recovery cannot safely wait.

Do not use break-glass for forgotten routine passwords, ordinary MFA recovery, convenience, bypassing SSO/VPN/change approval/RBAC, routine deployments, routine maintenance, developer troubleshooting, or privilege escalation for convenience.

## 5. Impact and Severity

Improper break-glass use can result in unauthorized administrative access, excessive privilege exposure, security-control bypass, credential compromise, account takeover, untracked production changes, compliance failure, and loss of accountability. Treat RB-008 as **Critical Risk**. Unexpected or unauthorized break-glass activity is a security incident.

## 6. Pre-Incident Readiness

```text
[ ] Dedicated emergency PERSON user exists
[ ] Identity owner documented
[ ] Identity not used for normal administration, applications, or automation
[ ] Password stored in approved privileged vault
[ ] Current Snowflake MFA requirements satisfied
[ ] OTP / approved backup MFA provisioned
[ ] Multiple recovery opportunities available
[ ] Recovery authentication policy verified
[ ] Approved network path and network policy verified
[ ] Required administrative roles verified
[ ] ACCOUNTADMIN usage explicitly governed
[ ] Administrative redundancy exists
[ ] Successful and failed login monitoring configured
[ ] User-change monitoring configured
[ ] Credential rotation and OTP replenishment documented
[ ] DR/failover emergency access independently verified
[ ] Periodic break-glass test completed
```

A failed readiness check is a production-readiness gap.

## 7. Emergency Identity

Interactive emergency administration should use a dedicated human identity (`TYPE=PERSON`).

```sql
SHOW USERS LIKE '<break_glass_user>';
DESC USER "<break_glass_user>";
```

Verify `NAME`, `LOGIN_NAME`, `TYPE`, `DISABLED`, `DEFAULT_ROLE`, and `NETWORK_POLICY`. Do not repurpose a `SERVICE` or `SERVICE_AGENT` identity for interactive emergency administration.

The break-glass user must own no application, ETL, scheduled task, BI, service integration, or routine automation dependency.

## 8. Strong Authentication and Vault

Password-only break-glass is not the production baseline. Use a dedicated PERSON user with a strong protected password plus OTP or another approved MFA method that satisfies current Snowflake requirements.

Store all break-glass authentication material only in an organization-approved privileged credential/key vault with restricted access and retrieval auditing. Never store passwords, OTP values, MFA secrets, private keys, tokens, or recovery codes in Slack, Teams, email, Jira, Confluence, GitHub, runbook source, chat, shell history, screenshots, or incident evidence.

## 9. OTP Provisioning and Lifecycle

Where approved and applicable, planned OTP provisioning can use:

```sql
ALTER USER "<break_glass_user>"
ADD MFA METHOD OTP COUNT = 5;
```

The exact count follows organizational policy. Provision emergency OTPs during controlled setup/rotation, not as the routine first action during an outage.

OTPs are emergency inventory. Record only non-secret metadata such as number provisioned/remaining, provisioning date, rotation date, vault reference, and owner. A successfully used OTP is consumed; do not assume it can be reused.

Before consuming emergency authentication:

```text
[ ] Password available
[ ] Valid OTP / approved MFA available
[ ] Additional recovery opportunity remains
```

If the only remaining recovery opportunity would be consumed, raise the risk with Security/Incident Command before proceeding. Password rotation and OTP replenishment are separate lifecycle decisions.

## 10. Authentication Independence

The emergency mechanism should not depend entirely on the same authentication component it is designed to recover. A break-glass path that relies on the same failed IdP/MFA dependency is not independent recovery.

Where appropriate, use a dedicated user-level recovery authentication policy for the emergency administrator. Recovery means independence from the failed normal mechanism, not weak authentication.

## 11. Network Policy Still Applies

Valid emergency credentials do not bypass Snowflake network-policy enforcement. Network policy is evaluated before authentication policy for access control. Therefore valid password + valid MFA + blocked network still means no access.

Pre-establish the emergency source network, VPN/private path, expected NAT/egress, network policy, and relevant network rules. Use RB-007 for network-policy remediation. Never broadly allow `0.0.0.0/0` merely to enable emergency access.

## 12. Mandatory Activation STOP Gate

```text
[ ] Correct Snowflake account/environment confirmed
[ ] Production impact confirmed
[ ] Normal admin path unavailable
[ ] Existing authorized sessions evaluated
[ ] Break-glass actually necessary
[ ] Incident/ticket exists
[ ] Incident commander identified
[ ] Required authorization obtained
[ ] Emergency PERSON identity identified and verified
[ ] No security containment exists
[ ] Authentication policy understood
[ ] Network path and policy understood
[ ] Vault retrieval authorized
[ ] Password available
[ ] OTP / approved MFA available
[ ] Backup authentication opportunity remains
[ ] Operator identified
[ ] Recovery objective defined
[ ] Minimum required role identified
[ ] Exit procedure and credential lifecycle understood
```

If authorization or identity integrity cannot be established: **STOP**.

## 13. Security STOP

Immediately involve Security if emergency credentials may be compromised; the identity shows unexplained activity; it was used outside an approved incident; the source network is unexpected; unauthorized role activation occurred; privileges or authentication methods changed unexpectedly; vault integrity is uncertain; normal administrator compromise is suspected; Security intentionally disabled the identity; or audit evidence is missing/contradictory.

Do not override security containment under RB-008.

## 14. Existing Authorized Session

Before consuming emergency credentials, determine whether a valid authorized administrative session already exists. An existing session may provide a lower-risk recovery path, but its use still requires incident authorization.

## 15. Credential Retrieval and Authentication

Record incident ID, emergency identity, authorized operator, approver, retrieval timestamp, and vault reference—but never the secret.

After authentication immediately verify context:

```sql
SELECT
    CURRENT_ACCOUNT(),
    CURRENT_REGION(),
    CURRENT_USER(),
    CURRENT_ROLE();
```

Any unexpected account, region, identity, or role is a **STOP condition**.

## 16. Authentication Is Not Authorization

Break-glass authentication does not justify automatic privilege escalation. Determine the recovery objective, required privilege, and minimum required role before elevation.

```sql
SELECT CURRENT_ROLE();
USE ROLE <approved_role>;
SELECT CURRENT_ROLE();
```

Record role transitions in incident evidence.

## 17. ACCOUNTADMIN Hard Gate

Before `USE ROLE ACCOUNTADMIN;` require:

```text
[ ] Exact operation identified
[ ] ACCOUNTADMIN genuinely required
[ ] Lower role evaluated
[ ] Incident severity justifies elevation
[ ] Authorization covers ACCOUNTADMIN
[ ] Operator and start timestamp recorded
[ ] Expected operations documented
[ ] Exit requirement documented
```

Do not investigate broadly under ACCOUNTADMIN when a lower role is sufficient. Break-glass complements normal administrative redundancy; it does not replace it.

## 18. Define One Recovery Objective

Before changing production, document the exact recovery objective: for example restoring SSO administration, correcting authentication policy, restoring an approved network policy, recovering an administrator, correcting OAuth configuration, or collecting support evidence.

Do not use the emergency session for unrelated work.

## 19. Preserve Current State and Route the Repair

Before mutation capture the non-secret current state with the appropriate `SHOW`, `DESC`, Account Usage, or specialized-runbook evidence.

Examples:

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
SHOW NETWORK POLICIES;
SHOW SECURITY INTEGRATIONS;
```

Route repair to RB-001 through RB-007 or RB-009/RB-010 as appropriate. Use evidence → hypothesis → minimum change → validation. Avoid changing SSO, MFA, authentication policy, network policy, user state, and role grants simultaneously unless evidence requires coordinated changes.

## 20. Emergency Change Boundary

Emergency access may be used only to restore production administration, critical authentication/security controls, critical service, collect required evidence, or safely transition back to normal administration. Do not use it for routine cleanup, cost optimization, unrelated tuning, unrelated schema/data changes, or routine user administration.

Where staffing permits, run emergency recovery and restoration of normal authentication in parallel.

## 21. Validation

Validate the repaired control through its original path. Examples include normal administrator SSO, expected MFA flow, approved network source, original OAuth client, or the original administrative identity.

Break-glass login success does **not** mean the incident is resolved.

From the normal administrator session, where safe:

```sql
SELECT
    CURRENT_ACCOUNT(),
    CURRENT_REGION(),
    CURRENT_USER(),
    CURRENT_ROLE();
```

Confirm the expected account, region, identity, authentication path, network path, role, and security controls.

## 22. Do Not Rotate Too Early

Do not immediately rotate emergency authentication material while the emergency session remains the only proven administrative path. First complete recovery, restore and validate normal administration, and confirm a backup recovery path. Then perform password/OTP lifecycle operations.

## 23. Password and OTP Closure

After emergency use, evaluate whether password exposure, policy, or compromise requires rotation. Never place the replacement password in incident evidence.

A used OTP is consumed. Evaluate remaining inventory separately. If inventory is low or trust is uncertain, invalidate/reissue according to the approved procedure, update the vault securely, and verify readiness.

## 24. Return Emergency User to Baseline

The approved dormant state may be enabled-but-tightly-protected or disabled-until-activation. Do not change that baseline during an incident without Security approval.

If the approved baseline requires disabling:

```sql
ALTER USER "<break_glass_user>"
SET DISABLED = TRUE;
```

Only proceed after recovery is complete, normal admin access is validated, no emergency query is running, no scheduled dependency exists, the emergency session is no longer needed, and closure is approved.

Close the emergency client/session using the organization's approved process and verify emergency activity ended.

## 25. DR / Failover Requirement

Emergency administration must be validated independently for DR/failover accounts. Do not assume that because an emergency user exists in a target account, usable emergency authentication material also exists there. In particular, do not assume emergency OTP availability is replicated.

DR readiness requires:

```text
[ ] Emergency user exists
[ ] User TYPE correct
[ ] Authentication method works
[ ] MFA mechanism independently verified
[ ] Network path verified
[ ] Authentication policy verified
[ ] Network policy verified
[ ] Required role grants verified
[ ] Vault material correctly mapped
[ ] No primary-only OTP assumption exists
[ ] DR test includes emergency administration
```

## 26. Monitoring

Alert/review at minimum: successful and failed break-glass logins; emergency user enable/disable; password changes; MFA-method changes; OTP provisioning; authentication-policy changes; network-policy changes; role grants/revokes; and ACCOUNTADMIN use.

A successful break-glass login with no approved incident is a **security incident**. Contain, preserve evidence, review source network, login/query history, grants/roles, user/policy changes, and recover/rotate emergency authentication as required.

Unknown-source failed authentication against the break-glass identity also requires Security review.

## 27. Login and Query Audit

Historical login evidence:

```sql
SELECT
    EVENT_TIMESTAMP,
    USER_NAME,
    CLIENT_IP,
    REPORTED_CLIENT_TYPE,
    REPORTED_CLIENT_VERSION,
    IS_SUCCESS,
    ERROR_CODE,
    ERROR_MESSAGE
FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
WHERE USER_NAME = '<break_glass_user>'
ORDER BY EVENT_TIMESTAMP DESC
LIMIT 100;
```

Account Usage can have ingestion latency; absence of an immediate record does not prove authentication did not occur.

Query review:

```sql
SELECT
    QUERY_ID,
    USER_NAME,
    ROLE_NAME,
    QUERY_TYPE,
    START_TIME,
    END_TIME,
    EXECUTION_STATUS
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE USER_NAME = '<break_glass_user>'
  AND START_TIME >= <incident_start>
  AND START_TIME <= <incident_end>
ORDER BY START_TIME;
```

Capture query ID, timestamp, role, operation type, status, affected object, and incident relevance. Avoid copying sensitive SQL into broadly accessible tickets unless necessary.

Review the period before activation through a short post-closure observation window.

## 28. Periodic Testing

Break-glass access that has never been tested is not a reliable recovery control. At an approved cadence: authorize the exercise; retrieve emergency material; authenticate; verify account/user/role, network path, authentication policy, and monitoring; avoid unnecessary mutation; close the session; restore baseline; replenish consumed OTP if needed; and audit the exercise.

The test must verify identity, vault retrieval, MFA/OTP, backup recovery opportunity, network/authentication policy, expected role, ACCOUNTADMIN governance, alerts, audit logging, exit procedure, credential lifecycle, OTP inventory, and DR emergency path.

## 29. Mandatory Closure Gate

```text
[ ] Recovery objective completed
[ ] Normal administrative authentication restored
[ ] Normal administrator tested successfully
[ ] Original authentication path validated
[ ] Required security controls restored
[ ] Emergency elevated role exited
[ ] Emergency session closed
[ ] Emergency identity returned to approved baseline
[ ] No automation depends on emergency identity
[ ] Password rotation decision completed
[ ] Used OTP accounted for
[ ] Remaining OTP inventory evaluated/replenished as required
[ ] DR emergency mechanism remains valid
[ ] Login and query history reviewed
[ ] Role/grant and policy changes reviewed
[ ] Monitoring and vault audit reviewed where available
[ ] No unexplained privileged activity remains
[ ] Evidence captured without secrets
[ ] Follow-up actions assigned
```

RB-008 is complete only when emergency access was authorized, required recovery completed, normal administrative access restored, emergency access closed, and privileged activity fully accounted for.

## 30. Abort Conditions

Stop routine execution if identity/account/authorization cannot be verified; vault integrity is uncertain; credentials may be compromised; unexplained activity exists; source network is unexpected; Security intentionally disabled the identity; policy or role state differs unexpectedly; broad weakening of controls would be required; the only remaining authentication opportunity would be consumed without contingency; primary/DR identities are confused; the exit procedure is unknown; or the action conflicts with security containment.

**Escalate rather than improvise.**

## 31. Rollback

For a failed recovery change, restore the known-good configuration and validate unless that state is insecure or compromised.

If emergency activation/use becomes unsafe: stop emergency activity, close the session, return the identity to a secure baseline, recover/rotate authentication material, preserve evidence, and involve Security.

Never restore a compromised credential/identity, vulnerable authentication configuration, unauthorized network access, security-blocked identity, or known-bad privilege assignment merely because it was the previous state.

## 32. Escalation Matrix

| Condition | Route |
|---|---|
| Password recovery | RB-001 |
| Disabled/locked user | RB-002 |
| Authentication diagnosis | RB-003 |
| MFA issue | RB-004 |
| Key-pair/JWT | RB-005 |
| SSO/OAuth | RB-006 |
| Network policy | RB-007 |
| Role/privilege issue | RB-009/RB-010 |
| Compromised credentials | RB-078 |
| Unauthorized privilege change | RB-079 |
| Service-account compromise | RB-081 |
| Emergency credential rotation | RB-082 |
| Snowflake service degradation | RB-083 |
| Support evidence | RB-088 |
| Snowflake Support escalation | RB-089 |

## 33. Evidence to Capture

Capture environment/account, region, incident/severity, reason for emergency access, normal-path failure, incident commander/approvers, emergency identity/type/baseline, authentication/network policies, operator/source/client, vault reference and retrieval timestamp, login timestamp/result, initial `CURRENT_ACCOUNT/REGION/USER/ROLE`, recovery objective, required/elevated role, ACCOUNTADMIN justification, actions/objects/query IDs, underlying runbook, normal-path validation, emergency-role/session closure, baseline restoration, password-rotation decision, OTP inventory lifecycle, DR readiness, login/query/grant/policy/monitoring/vault-audit reviews, unexpected activity, escalation, timestamps, post-incident owner, and follow-ups.

Never capture passwords, temporary passwords, private keys/passphrases, OTP values, MFA seeds/codes, recovery codes, OAuth/PAT/session tokens, or secret-manager secret values.

## 34. Quick Production Procedure

1. Confirm production impact and correct account/environment.
2. Confirm normal admin path is unavailable and evaluate existing authorized sessions.
3. Open/confirm incident and obtain authorization.
4. Verify approved emergency PERSON user and security state.
5. Verify authentication policy and approved network path/policy.
6. Authorize vault retrieval and confirm password + OTP/approved MFA plus backup recovery opportunity.
7. Authenticate and verify `CURRENT_ACCOUNT`, `CURRENT_REGION`, `CURRENT_USER`, and `CURRENT_ROLE`.
8. Define one recovery objective and minimum required privilege.
9. Elevate only when required and authorized.
10. Capture current state and route remediation through the specialized runbook.
11. Apply the minimum recovery change and validate production recovery.
12. Validate the **original** normal administrative path.
13. Exit emergency elevation and close the emergency session.
14. Return the identity to approved baseline.
15. Complete password and OTP lifecycle decisions.
16. Verify DR emergency readiness.
17. Review login/query/role/policy/monitoring/vault evidence.
18. Confirm no unexplained privileged activity or emergency access remains.
19. Assign follow-up actions and close.

## 35. Production Guardrails

**Always:** pre-provision emergency access; use a dedicated PERSON identity; strongly authenticate; protect secrets in a vault; maintain backup recovery authentication; authorize activation; verify account/network/policies; use minimum privilege; gate ACCOUNTADMIN; define one objective; preserve state; use specialized runbooks; validate normal access; close sessions; restore baseline; manage password and OTP separately; preserve DR readiness; and audit all privileged activity.

**Never:** use break-glass for convenience; routinely create ad-hoc privileged accounts during incidents; use service identities as human emergency admins; rely on password-only break-glass as the production baseline; share secrets; broadly disable MFA/SSO/authentication controls; allow `0.0.0.0/0`; automatically activate ACCOUNTADMIN; perform unrelated administration; make the emergency identity an automation dependency; rotate the only functioning credential before normal access is restored; assume OTPs replicate to DR; leave emergency sessions active; or treat emergency login success as incident resolution.

## 36. Canonical Success Model

```text
Normal administration fails
→ Critical recovery required
→ Break-glass authorized
→ Emergency identity verified
→ Secure authentication
→ Correct account verified
→ Minimum privilege
→ Defined recovery objective
→ Specialized remediation
→ Normal administration restored
→ Original path validated
→ Emergency role exited
→ Emergency session closed
→ Identity returned to baseline
→ Password / OTP lifecycle completed
→ DR readiness preserved
→ Privileged activity reviewed
→ CLOSE
```

## 37. References

Primary technical authority:

- Snowflake — Multi-factor authentication and break-glass access: https://docs.snowflake.com/en/user-guide/security-mfa
- Snowflake — Authentication policies: https://docs.snowflake.com/en/user-guide/authentication-policies
- Snowflake — Strong authentication rollout: https://docs.snowflake.com/en/user-guide/security-mfa-rollout
- Snowflake — ALTER USER: https://docs.snowflake.com/en/sql-reference/sql/alter-user
- Snowflake — Access control considerations: https://docs.snowflake.com/en/user-guide/security-access-control-considerations
- Snowflake — LOGIN_HISTORY: https://docs.snowflake.com/en/sql-reference/account-usage/login_history
- Snowflake — QUERY_HISTORY: https://docs.snowflake.com/en/sql-reference/account-usage/query_history

---

## Canonical Decision

**RB-008 — Emergency / Break-Glass Access: REVISED FINAL / CANONICAL EDITION APPROVED**

Non-negotiable production principles:

1. Break-glass must be pre-provisioned, strongly authenticated, monitored, and periodically tested—not invented during the outage.
2. Emergency authentication and emergency authorization are separate controls; successful login never automatically justifies `ACCOUNTADMIN`.
3. The original normal administrative path must be restored and validated before emergency recovery is complete.
4. Every activation ends with emergency-session closure, baseline restoration, password/OTP lifecycle handling, DR-readiness preservation, and complete privileged-activity review.
