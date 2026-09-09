# RB-002 — Unlock / Restore User Access

**Snowflake DBRE/SRE Production Runbook**  
**Runbook ID:** RB-002  
**Category:** Access & Authentication  
**Edition:** Revised Final / Canonical  
**Risk:** Medium–High  
**Primary Operator:** DBRE / SRE / Snowflake Administrator

## 1. Purpose

Use this runbook to diagnose and safely restore access when an existing Snowflake identity cannot authenticate because it is administratively disabled, temporarily locked after failed authentication attempts, expired, or affected by another user-level access restriction.

Restore only access that is authorized and necessary. Do not reset credentials, change authentication mechanisms, modify roles/grants, or weaken security controls unless separately diagnosed and approved.

> **Core principle: Restoring technical access is not equivalent to authorization to restore access.**

## 2. Trigger / Alert

Use RB-002 for reports such as unable to log in, user appears locked, account disabled, too many failed login attempts, previously working account cannot authenticate, or an approved disabled account needs restoration.

Do not immediately enable or unlock the identity. First establish why access was restricted.

## 3. Impact / Severity

| Condition | Suggested Severity |
|---|---|
| Single non-critical human user | Low |
| Production engineer blocked | Medium |
| Critical operational identity affected | High |
| Production workload affected | High |
| Multiple users affected | Major authentication incident |
| Security-related restriction | Security incident |

Use the organization's incident-severity standard where applicable.

## 4. STOP — Mandatory Pre-Change Gate

> **Do not restore access until the Snowflake environment, exact identity, current account state, reason for restriction, authorization, authentication mechanism, and production impact have been verified.**

Confirm:

```text
[ ] Correct Snowflake account/environment
[ ] Exact username confirmed
[ ] Requester identity verified
[ ] Request/ticket authorized
[ ] User type determined
[ ] Authentication method identified
[ ] Current user state inspected
[ ] Reason for restriction investigated
[ ] Production dependencies understood
[ ] No active security restriction exists
[ ] No broader authentication incident exists
```

If any required check cannot be completed, stop and investigate.

## 5. SECURITY STOP

If the identity was disabled or restricted by Security, IAM, incident response, automated security controls, offboarding, credential-compromise containment, access review, or leave/suspension processes, do not enable or unlock it without explicit authorization from the responsible control owner.

## 6. Required Access

Use the lowest-privileged administrative role authorized to inspect and modify the target identity.

```sql
USE ROLE USERADMIN;
```

Do not assume `USERADMIN` automatically has authority over every user in custom ownership/RBAC models. Avoid `ACCOUNTADMIN` when it is being used only for convenience.

## 7. Verify Execution Context

```sql
SELECT
    CURRENT_ACCOUNT(),
    CURRENT_REGION(),
    CURRENT_ROLE(),
    CURRENT_USER();
```

Verify the account, region, administrative role, and administrator identity. If the environment is wrong or uncertain, stop.

## 8. Locate and Inspect the User

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

If the intended identity is not returned, verify username, `LOGIN_NAME`, account/environment, identifier case/quoting, and provisioning records. Do not create a replacement user under RB-002.

Review relevant state including `TYPE`, `LOGIN_NAME`, `DISABLED`, `MINS_TO_UNLOCK`, `SNOWFLAKE_LOCK`, expiration information, `MUST_CHANGE_PASSWORD`, authentication indicators, owner, and last successful login.

The objective is to distinguish administrative disablement, temporary lock, expiration, credential failure, SSO/OAuth/MFA, key-pair authentication, network policy, and authorization failures.

## 9. Determine Identity Type

For `PERSON`, identify the interactive authentication mechanism such as password, SSO/SAML, OAuth, or MFA.

For `SERVICE` or `SERVICE_AGENT`, identify the owning application/team, authentication mechanism, workload dependencies, token/key dependencies, retry behavior, and production impact before modifying the identity.

> **Do not unlock a non-human identity until the source of repeated failed authentication has been identified or contained.**

## 10. Investigate Authentication Failures

```sql
SELECT
    EVENT_TIMESTAMP,
    USER_NAME,
    CLIENT_IP,
    REPORTED_CLIENT_TYPE,
    IS_SUCCESS,
    ERROR_CODE,
    ERROR_MESSAGE
FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
WHERE USER_NAME = '<username>'
ORDER BY EVENT_TIMESTAMP DESC
LIMIT 50;
```

Look for repeated failures, unexpected source IPs/clients, authentication-policy failures, network-policy rejection, SSO/OAuth problems, and successful authentication followed by failures.

`ACCOUNT_USAGE.LOGIN_HISTORY` can have ingestion latency. Absence of an immediately recent event does not prove that no authentication attempt occurred.

## 11. Classify the Restriction

### A. Administratively Disabled

If `DISABLED = TRUE`, determine why the identity was disabled and whether restoration is authorized before changing it.

### B. Temporary Snowflake Lock

Indicators can include `MINS_TO_UNLOCK > 0`, `SNOWFLAKE_LOCK`, and lock-until information. Before clearing the lock, identify what generated the failed authentication attempts.

### C. User Expiration

Review the configured expiry state. Do not automatically extend an expired identity. Expiration may be an intentional lifecycle/security boundary.

### D. Credential Failure

If the password is forgotten or invalid, route to **RB-001 — Reset User Password**.

### E. Other Authentication Mechanism

For SSO, OAuth, MFA, key pair, network policy, or authentication-policy problems, route to the corresponding runbook.

### F. Authorization Failure

If authentication succeeds but access to a warehouse/database/schema/object fails, route to the Roles, Grants & Permissions runbooks.

## 12. Decision Matrix

| Finding | Action |
|---|---|
| `DISABLED=TRUE`, restoration approved | Enable user |
| `DISABLED=TRUE`, reason unknown | STOP |
| Security-related disablement | SECURITY STOP |
| `MINS_TO_UNLOCK > 0` | Investigate failed-auth source |
| Temporary lock, low urgency | Correct cause and allow automatic unlock |
| Temporary lock, immediate restoration required | Approved administrative unlock |
| User expired | Validate lifecycle authorization |
| Password forgotten/invalid | RB-001 |
| `MUST_CHANGE_PASSWORD` outstanding | Complete required password workflow |
| SSO/SAML, OAuth, MFA, key pair, network policy | Corresponding authentication runbook |
| Login works but object access fails | Permissions runbook |
| Multiple users affected | Major authentication incident |

## 13. Remediation Path A — Re-Enable User

Use only when `DISABLED = TRUE` and restoration is explicitly authorized.

```sql
ALTER USER "<username>"
SET DISABLED = FALSE;
```

Verify immediately:

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

Do not bundle this with password, role, MFA, key, network-policy, or authentication-policy changes unless each is independently diagnosed and authorized.

## 14. Remediation Path B — Temporary Login Lock

First identify and correct or contain the source of repeated failed authentication.

For low-impact situations, correct the underlying issue and allow the temporary lock to clear automatically.

When immediate restoration is justified:

```sql
ALTER USER "<username>"
SET MINS_TO_UNLOCK = 0;
```

Verify:

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

Do not attempt to set `SNOWFLAKE_LOCK = FALSE`. Inspect `SNOWFLAKE_LOCK` as diagnostic state; use `MINS_TO_UNLOCK` for temporary-lock remediation.

## 15. Prevent Immediate Re-Lock

Do not repeatedly unlock an identity while a client continues retrying invalid authentication material. Identify the source, stop or correct the retries, restore access, and monitor for renewed failures.

This is particularly important for service identities and automated workloads.

## 16. Programmatic Access Token Check

If the identity uses PATs:

```sql
SHOW USER PROGRAMMATIC ACCESS TOKENS
FOR USER "<username>";
```

Do not automatically restore disabled tokens. Determine why each token is disabled, whether it should still exist, and whether restoration is authorized.

Only when independently approved:

```sql
ALTER USER "<username>"
MODIFY PROGRAMMATIC ACCESS TOKEN "<token_name>"
SET DISABLED = FALSE;
```

Treat user restoration and token restoration as separate security decisions.

## 17. Password Reset Separation

Do not automatically reset a password while unlocking or enabling an identity.

`RB-001 = Credential reset`  
`RB-002 = Account access-state restoration`

If both are genuinely necessary, diagnose and authorize each action independently.

## 18. Preserve Security Controls

Never restore access by arbitrarily disabling MFA, removing network policies, weakening authentication policies, bypassing SSO, changing RSA keys, granting broad roles, granting `ACCOUNTADMIN`, or extending expiration without authorization.

Fix the actual failure.

## 19. Validation

### Verify User State

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

Confirm that the intended state changed and unrelated properties did not.

### Validate Authentication

Have the human user authenticate through the normal approved interface, or validate an automated workload through its normal workload path. Never request passwords, MFA codes, OAuth/session tokens, private keys, or PAT secrets.

### Validate Normal Session

For an interactive user, a low-risk check can include:

```sql
SELECT
    CURRENT_USER(),
    CURRENT_ROLE(),
    CURRENT_WAREHOUSE();
```

### Watch for Re-Lock

For automated identities, monitor for renewed authentication failures. If the identity immediately locks again, stop repeatedly unlocking it and correct the authentication source.

### PAT Validation

Where applicable:

```sql
SHOW USER PROGRAMMATIC ACCESS TOKENS
FOR USER "<username>";
```

Confirm that only expected tokens are active.

## 20. Authorization Validation

If authentication works but authorization does not:

```sql
SHOW GRANTS TO USER "<username>";
```

Use this for diagnosis only. Do not add roles or privileges under RB-002; route authorization failures to the permissions runbook.

## 21. Successful Resolution Criteria

```text
[✓] Correct Snowflake account verified
[✓] Correct identity verified
[✓] Identity type understood
[✓] Authentication method understood
[✓] Reason for restriction identified
[✓] Restoration explicitly authorized
[✓] Underlying failed-auth source corrected/contained
[✓] Minimum required remediation performed
[✓] Post-change user state verified
[✓] Authentication succeeds
[✓] Normal access succeeds
[✓] No immediate re-lock occurs
[✓] PAT state checked where applicable
[✓] No security controls were weakened
[✓] No unnecessary authorization changes made
[✓] Non-secret evidence recorded
```

## 22. Abort Conditions

Stop when the identity cannot be positively verified, the environment is uncertain, authorization is missing, the reason for disablement is unknown, Security/IAM intentionally restricted the identity, suspicious authentication activity exists, production dependencies are unclear, multiple users are affected, restoration would require weakening security controls, or the repeated-authentication source cannot be identified/contained.

## 23. Rollback

If an identity was mistakenly enabled and should remain disabled:

```sql
ALTER USER "<username>"
SET DISABLED = TRUE;
```

Before disabling it again, determine whether the brief restoration resulted in successful authentication, token usage, query execution, data access, or other activity requiring security review.

## 24. Escalation

Escalate when user state cannot be explained, the authorized administrative role cannot modify the identity, authentication still fails after correct remediation, repeated failures continue, SSO/OAuth/MFA/key-pair/network policy is involved, suspicious activity exists, security-related disablement is discovered, production service identities are affected, multiple users are affected, or Snowflake service degradation is suspected.

For suspected Snowflake platform issues, capture account/region, timestamps, errors, client information, login evidence, and correlation details before opening a support case.

## 25. Evidence to Capture

```text
RUNBOOK: RB-002
Environment/account:
Region:
Username:
User type:
Authentication method:
Request/ticket:
Requester verified: Yes/No
Restoration authorized: Yes/No
Authorization source:
Administrator:
Administrative role:
Start timestamp:

PRE-CHANGE
DISABLED:
MINS_TO_UNLOCK:
SNOWFLAKE_LOCK:
Expiration state:
MUST_CHANGE_PASSWORD:
PAT applicable: Yes/No
Observed login failures:
Failure source identified: Yes/No
Reason for restriction:

REMEDIATION
Automatic unlock / Enable user / Immediate unlock / Other:
Underlying cause corrected/contained: Yes/No
PAT action performed: Yes/No/N/A

VALIDATION
Post-change state:
Authentication validated: Yes/No
Normal access validated: Yes/No
Re-lock observed: Yes/No
Security escalation: Yes/No
Production impact:
Completion timestamp:
```

Never record passwords, temporary passwords, MFA codes, password-reset URLs, private keys, OAuth/session tokens, PAT secrets, or other secret values.

## 26. Quick Operational Procedure

### Diagnose

```sql
SELECT
    CURRENT_ACCOUNT(),
    CURRENT_REGION(),
    CURRENT_ROLE(),
    CURRENT_USER();

SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

Stop and evaluate `DISABLED`, temporary-lock state, expiration, `MUST_CHANGE_PASSWORD`, identity type, authentication method, reason for restriction, authorization, failed-authentication source, and production dependencies.

### Choose Exactly One Matching Remediation

Approved administrative enablement:

```sql
ALTER USER "<username>"
SET DISABLED = FALSE;
```

**OR**, approved immediate temporary unlock:

```sql
ALTER USER "<username>"
SET MINS_TO_UNLOCK = 0;
```

Do not blindly execute both.

### Verify

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

If PATs are applicable:

```sql
SHOW USER PROGRAMMATIC ACCESS TOKENS
FOR USER "<username>";
```

Complete end-to-end authentication validation before closing.

## 27. Operational Guardrails

Always diagnose before changing state, verify environment and identity, understand why access was restricted, identify the authentication type, obtain restoration authorization, fix failed-authentication sources before unlocking, use least privilege, validate end-to-end, check programmatic credentials where relevant, and record non-secret evidence.

Never blindly unlock users, restore security-disabled identities, repeatedly unlock broken applications, reset passwords unnecessarily, remove MFA/network policies to bypass failures, extend expiration without approval, restore PATs automatically, grant broader privileges to solve authentication, or use `ACCOUNTADMIN` merely for convenience.

## 28. References

Use current Snowflake primary documentation as the technical authority:

- Snowflake user management and unlocking users
- Snowflake SQL command reference — `ALTER USER`
- Snowflake SQL command reference — `SHOW USERS`
- Snowflake SQL command reference — `DESCRIBE USER`
- Snowflake Account Usage — `LOGIN_HISTORY`
- Snowflake programmatic access token documentation
- Snowflake access-control documentation

---

**Canonical status:** `CANONICAL`  
**Workflow:** Draft → Technical + Source Review → Production + Copyright Review → Revised Final / Canonical Edition
