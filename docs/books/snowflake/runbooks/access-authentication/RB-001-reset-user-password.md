# RB-001 — Reset User Password

**Snowflake DBRE/SRE Production Runbook**  
**Runbook ID:** RB-001  
**Category:** Access & Authentication  
**Edition:** Revised Final / Canonical  
**Risk:** Medium  
**Primary Operator:** DBRE / SRE / Snowflake Administrator

## 1. Purpose

This runbook provides the production procedure for resetting the password of a Snowflake human user. It is designed to verify that the incident is password-related, prevent changes to the wrong user/account, distinguish human from non-human identities, preserve authorization, protect credentials, and provide controlled validation and escalation.

This runbook is not the procedure for SSO, OAuth, MFA, key-pair, network-policy, service-account authentication failures, or suspected credential compromise.

## 2. Trigger

Use RB-001 when a human user forgot their Snowflake password, has a confirmed invalid/unknown password, requires an approved administrator reset, or requires routine password rotation.

Do not automatically reset a password for a generic login or connection failure; diagnose the authentication path first.

## 3. Mandatory Pre-Change Gate

> **STOP — Do not change credentials until the target Snowflake account, username, user type, authentication method, request authorization, and expected production impact have been verified.**

Confirm:

- Correct Snowflake account/environment
- Exact username
- Requester identity and authorization
- User type
- Authentication method
- Production dependencies
- No broader authentication outage
- No indication of credential compromise

If any required check cannot be completed, stop and investigate.

## 4. Required Access

Use the lowest-privileged administrative role authorized to modify the target user. `USERADMIN` is commonly used in the standard hierarchy, but activating it does not guarantee authority over every user in environments with custom ownership/RBAC.

```sql
USE ROLE USERADMIN;
```

Avoid `ACCOUNTADMIN` for routine resets when a lower-privileged authorized role is sufficient.

## 5. Diagnosis

### 5.1 Verify Execution Context

```sql
SELECT CURRENT_ACCOUNT(),
       CURRENT_REGION(),
       CURRENT_ROLE(),
       CURRENT_USER();
```

Confirm the intended Snowflake environment before proceeding.

### 5.2 Locate the User

```sql
SHOW USERS LIKE '<username>';
```

If the expected user is not returned, stop and verify username spelling, identifier handling, account/environment, and provisioning records. Do not create a user as part of this runbook.

### 5.3 Inspect the User

```sql
DESC USER "<username>";
```

Review relevant properties such as `TYPE`, `LOGIN_NAME`, `DISABLED`, `SNOWFLAKE_LOCK`, and `MUST_CHANGE_PASSWORD`. Do not modify unrelated properties.

## 6. User-Type Decision Gate

For `TYPE = PERSON`, determine whether password authentication is actually being used. Continue RB-001 only for an approved password-authentication reset.

For `TYPE = SERVICE` or `TYPE = SERVICE_AGENT`, stop the password-reset workflow and investigate the configured non-password authentication mechanism.

If SSO/SAML, OAuth, MFA, key-pair authentication, or network policy is responsible, route to the corresponding runbook.

## 7. Login Failure Investigation

When the cause is uncertain:

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
LIMIT 20;
```

Use the evidence to distinguish password failure from account state, network-policy, SSO/OAuth, MFA/authentication-policy, or client problems.

`ACCOUNT_USAGE.LOGIN_HISTORY` can have ingestion latency of up to approximately two hours. Absence of a very recent event does not prove the login attempt did not occur.

## 8. Security Incident Gate

A routine password reset is not a credential-compromise response. If credentials were exposed, suspicious successful logins occurred, unknown client/IP activity exists, account takeover is suspected, or unauthorized activity is associated with the identity, stop RB-001 and invoke the security-incident procedure.

## 9. Password Reset Methods

### Method A — User Selects a New Password

Where organizational policy permits:

```sql
ALTER USER "<username>" RESET PASSWORD;
```

Snowflake generates a single-use, time-limited password-reset URL. Treat the URL as sensitive authentication material and deliver it only through an approved mechanism.

Generating a reset URL does not by itself immediately invalidate the existing password. Do not rely on this method alone when existing credentials may be compromised.

### Method B — Administrator Assigns a Temporary Password

Generate a strong temporary password using an approved credential-generation mechanism and ensure it satisfies the effective password policy.

```sql
ALTER USER "<username>"
SET PASSWORD = '<secure-temporary-password>'
    MUST_CHANGE_PASSWORD = TRUE;
```

Never use predictable temporary credentials.

## 10. Secret Handling

Passwords and password-reset URLs are secrets. Never store actual credentials in Git, source code, runbooks, ordinary ticket comments, screenshots, shared notes, shell history, or incident transcripts. Use only organization-approved secret-delivery mechanisms.

Repository examples must use placeholders such as `<username>`, `<temporary-password>`, `<account>`, and `<ticket-id>`.

Never ask the user to disclose their permanent password for validation.

## 11. Password Policy

The new password must satisfy the effective password policy applied to the user/account. Organizational policies can be stronger than Snowflake's platform baseline. Do not weaken a password policy merely to make a reset succeed.

## 12. Mandatory Password Change

When `MUST_CHANGE_PASSWORD = TRUE` is used, the interactive user should complete the required password-change workflow through the Snowflake web interface as applicable before troubleshooting normal JDBC, ODBC, CLI, or application connectivity.

## 13. Validation

A successful `ALTER USER` statement alone does not prove resolution.

Verify account state:

```sql
SHOW USERS LIKE '<username>';
```

Have the user authenticate using the normal approved Snowflake interface. If applicable, confirm completion of the mandatory password change and successful reconnection through the user's normal client.

If authorization verification is needed:

```sql
SHOW GRANTS TO USER "<username>";
```

This is verification only. A password reset does not normally require roles or grants to be recreated. If authentication succeeds but object access fails, move to the authorization/privilege runbook.

## 14. Abort Conditions

Abort RB-001 if the user cannot be positively identified, authorization cannot be verified, the environment is uncertain, the identity is inappropriate for password authentication, SSO/OAuth/MFA/key-pair authentication is responsible, multiple users are failing, credential compromise is suspected, or changing credentials could unexpectedly disrupt production.

## 15. Rollback / Recovery

Password resets do not have a conventional rollback. Do not restore or redistribute an old password as the normal rollback strategy.

If the new credential cannot be used, determine the failure, verify the authentication mechanism and account state, perform another controlled reset if appropriate, securely establish the credential, and validate authentication.

For a production application identity, use the dedicated service-account/secret-rotation procedure.

## 16. Escalation

Escalate when authorized administration cannot modify the user, account state is unexpected, authentication still fails after a validated reset, multiple users are affected, SSO/MFA/network policy is involved, suspicious activity is detected, production services are affected, or Snowflake service degradation is suspected.

For a suspected platform problem, capture timestamps, account/region information, error codes, login evidence, and correlation details before opening a Snowflake Support case.

## 17. Evidence Collection

Record only non-secret operational evidence:

```text
RUNBOOK: RB-001
Environment/account:
Region:
Username:
User type:
Authentication method:
Request/ticket:
Requester verified: Yes/No
Administrator:
Administrative role:
Start timestamp:
Reason:
Pre-change diagnosis:
Reset method: Reset URL / Temporary Password
Reset completed: Yes/No
MUST_CHANGE_PASSWORD: Yes/No/N/A
Authentication validated: Yes/No
Authorization validated: Yes/No/N/A
Production impact:
Escalation:
Completion timestamp:
```

Never record passwords, temporary passwords, password-reset URLs, private keys, OAuth/session tokens, or secret values.

## 18. Quick Operational Procedure

```sql
-- 1. Confirm execution context.
SELECT CURRENT_ACCOUNT(),
       CURRENT_REGION(),
       CURRENT_ROLE(),
       CURRENT_USER();

-- 2. Locate the target user.
SHOW USERS LIKE '<username>';

-- 3. Inspect the target user.
DESC USER "<username>";

-- STOP and evaluate user type, authentication method,
-- account state, authorization, and production dependencies.
```

Then choose exactly one approved remediation method:

```sql
-- Reset URL method
ALTER USER "<username>" RESET PASSWORD;
```

or:

```sql
-- Administrator-assigned temporary password
ALTER USER "<username>"
SET PASSWORD = '<secure-temporary-password>'
    MUST_CHANGE_PASSWORD = TRUE;
```

Verify afterward:

```sql
SHOW USERS LIKE '<username>';
SHOW GRANTS TO USER "<username>";
```

Complete user-side authentication validation before closing the request.

## 19. Operational Guardrails

Always verify environment and identity, use least privilege, determine user type and authentication method, protect secrets, validate actual login, preserve existing authorization, and record non-secret evidence.

Never blindly reset credentials for generic connection errors, expose passwords/reset URLs, bypass security controls, modify unrelated properties, change non-human identities without dependency analysis, or use `ACCOUNTADMIN` merely for convenience.

## 20. References

Use current Snowflake primary documentation as the technical authority:

- Snowflake SQL command reference — `ALTER USER`
- Snowflake SQL command reference — `DESCRIBE USER`
- Snowflake SQL command reference — `SHOW USERS`
- Snowflake Account Usage — `LOGIN_HISTORY`
- Snowflake password authentication documentation
- Snowflake user-management documentation
- Snowflake access-control documentation

---

**Canonical status:** `CANONICAL`  
**Workflow:** Draft → Technical + Source Review → Production + Copyright Review → Revised Final / Canonical Edition
