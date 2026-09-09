# RB-003 — Troubleshoot Login / Authentication Failure

**Snowflake DBRE/SRE Production Runbook**  
**Runbook ID:** RB-003  
**Category:** Access & Authentication  
**Edition:** Revised Final / Canonical  
**Risk:** Medium–High  
**Primary Operator:** DBRE / SRE / Snowflake Administrator

## 1. Purpose

Use this runbook to diagnose Snowflake login and authentication failures, identify the failing authentication domain, and route remediation to the appropriate production runbook.

RB-003 is the central authentication triage and orchestration runbook. It is intentionally diagnostic rather than a collection of password-reset, unlock, MFA, key, SSO/OAuth, PAT, or network-policy modification procedures.

> **Core principle:** Diagnose the authentication path before modifying the identity or weakening any security control.

## 2. Trigger / Alert

Use RB-003 for login/authentication failures involving password, SSO/SAML, MFA, OAuth, JWT/key pair, PAT, applications, JDBC/ODBC, Python connectors, CLI clients, previously working authentication, or multiple users suddenly unable to authenticate.

Use RB-003 before changing credentials or security configuration when the failure domain is unknown.

## 3. Impact / Severity

| Condition | Suggested Severity |
|---|---|
| Single non-critical human user | Low |
| Production engineer blocked | Medium |
| Single production application/service | Medium–High |
| Critical production workload | High |
| Multiple unrelated identities | High / Major incident |
| Account-wide authentication failure | Major incident |
| Suspicious authentication activity | Security incident |

Follow the organization's incident-severity standard where applicable.

## 4. STOP — Mandatory Safety Gate

Do not reset passwords, unlock identities, disable MFA, remove network policies, modify authentication policies, rotate keys, modify SSO/OAuth, restore PATs, or grant elevated privileges until the failure has been classified.

Establish the correct environment/account/endpoint, exact identity, `NAME` and `LOGIN_NAME`, identity type, expected authentication method, exact error, client/version, failure start, last known successful authentication, blast radius, recent changes, and security implications.

## 5. Security Incident Gate

Immediately consider security escalation for unexpected successful authentication, unknown source IPs, credential exposure, unexpected key/PAT usage, repeated failures followed by unexplained success, unauthorized authentication-method/MFA changes, or attempted use of a security-disabled identity.

Route suspected credential compromise to **RB-078 — Compromised User Credentials**. Preserve evidence before making changes unless immediate containment is required.

## 6. Capture the Exact Failure

Record timestamp/timezone, account, region, account identifier/connection URL, username supplied by the client, client/application and version, authenticator, expected authentication method, error code/message, source IP where known, last known success, and recent changes.

Never capture credential material in screenshots, logs, tickets, chat, or runbook evidence.

## 7. Determine Blast Radius

Determine whether the incident affects one user, one application/workload, one authentication method, or multiple unrelated users/workloads.

If several unrelated identities fail at approximately the same time, stop individual password resets and unlocks. Investigate shared dependencies such as Snowflake service, IdP, OAuth provider, DNS, proxy, firewall, NAT/egress, network/authentication policy, account configuration, and recent shared changes.

## 8. Verify Administrative Environment

```sql
SELECT
    CURRENT_ACCOUNT(),
    CURRENT_REGION(),
    CURRENT_ROLE(),
    CURRENT_USER();
```

Confirm the intended environment and region before changing credentials or identity state.

## 9. Verify Account / Endpoint

Compare the failing client's account identifier, organization/account where applicable, region, connection URL, authenticator, and client-supplied username against the intended Snowflake environment.

A valid credential presented to the wrong Snowflake account can appear to be an authentication failure.

## 10. Locate the Identity

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

If no matching identity is found, investigate wrong account, wrong username, `LOGIN_NAME` mismatch, identifier/case issue, provisioning failure, removed user, or incorrect application configuration. Do not create a replacement identity as a troubleshooting shortcut.

## 11. Verify NAME vs LOGIN_NAME

Do not assume `NAME = LOGIN_NAME`. Capture and compare the Snowflake user object name, configured login name, and client-supplied username before changing credentials.

## 12. Inspect Authentication-Relevant User State

Review relevant `SHOW USERS` and `DESC USER` state including identity type, `LOGIN_NAME`, disabled/lock state, mandatory password-change state, expiration/lifecycle state, authentication indicators, owner, and last successful login.

Determine whether the identity can authenticate, how it is expected to authenticate, and whether Snowflake is intentionally restricting it.

## 13. Determine Identity Type

Identify whether the identity is `PERSON`, `SERVICE`, or `SERVICE_AGENT`.

For non-human identities, identify the owning application/team, authentication mechanism, credential/key/token source, production dependencies, recent deployment, rotation history, retry behavior, and current production impact before remediation.

## 14. Service Identity Retry-Storm Gate

Before resetting, unlocking, rotating, or restoring a production service identity, identify and contain uncontrolled authentication retries. Correct the workload's credential/key/token configuration before restoring identity state, then monitor for renewed failures.

> **Do not repeatedly unlock a service identity while bad-authentication retries continue.**

## 15. Identify Expected Authentication Method

Establish whether the identity should use password, MFA, SSO/SAML, OAuth, key pair/JWT, PAT, or another approved mechanism. Troubleshoot the expected authentication path rather than substituting an easier one.

## 16. Recent Login Evidence

For active/recent incidents, use the Information Schema login-history function as appropriate:

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
FROM TABLE(
    INFORMATION_SCHEMA.LOGIN_HISTORY(
        TIME_RANGE_START => DATEADD('hour', -1, CURRENT_TIMESTAMP()),
        RESULT_LIMIT => 1000
    )
)
WHERE USER_NAME = '<username>'
ORDER BY EVENT_TIMESTAMP DESC;
```

## 17. Historical Login Evidence

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
WHERE USER_NAME = '<username>'
ORDER BY EVENT_TIMESTAMP DESC
LIMIT 50;
```

`ACCOUNT_USAGE.LOGIN_HISTORY` can have ingestion latency; do not treat it as an instantaneous source.

## 18. Login History Interpretation Guardrail

Absence of a login-history row does not prove no authentication attempt occurred. Consider ingestion latency, wrong account/login name, upstream SSO/OAuth/network failure, or a client request that never reached Snowflake. Combine login evidence with client errors, identity state, authentication method, source/network information, and timeline.

## 19. Last Known Good and Change Correlation

Determine the last successful authentication and failure start, then identify what changed between them. Review password/secret rotation, identity state, MFA, authentication/network policy, SSO/IdP, OAuth, RSA-key/PAT rotation, application deployments, connector upgrades, proxy/firewall, NAT/public IP, and DNS changes.

## 20. Branch — Disabled or Locked Identity

If the identity is administratively disabled or temporarily locked, route to **RB-002 — Unlock / Restore User Access**. RB-003 diagnoses the condition; RB-002 owns state-changing remediation and rollback.

## 21. Branch — Password Authentication

If password authentication is confirmed, investigate account/endpoint, `LOGIN_NAME`, disabled/lock state, mandatory password-change state, stale client/application secrets, and authentication policy before deciding the password itself requires replacement.

When replacement is required, route to **RB-001 — Reset User Password**.

## 22. Branch — Mandatory Password Change

If `MUST_CHANGE_PASSWORD = TRUE`, the user may need to complete the required password-change workflow before normal client authentication. Do not disable this requirement merely to make a client work.

## 23. Branch — MFA

Do not disable MFA, remove authentication policy, or bypass MFA requirements as a diagnostic test. When MFA is the confirmed failure domain, route to **RB-004 — MFA Recovery**.

## 24. Branch — SSO / SAML

For one-user failures, investigate identity mapping, application assignment, and user-specific IdP state. For multi-user failures, prioritize IdP/integration/certificate/configuration/network/service investigation. Route remediation to **RB-006 — SSO/OAuth Failure**.

## 25. Branch — OAuth

Investigate provider, issuer, audience, expiration, scopes, Snowflake security integration, client configuration, and recent provider/configuration changes. Never store bearer/access/refresh tokens in incident evidence. Route remediation to **RB-006 — SSO/OAuth Failure**.

## 26. Branch — Key Pair / JWT

Investigate the correct identity, registered public key, expected active key slot/version, recent key rotation, client private-key configuration, JWT generation, clock synchronization, and connector configuration. Safe evidence can include public-key fingerprint, key slot/version, rotation timestamp, client version, error message, and clock state. Never collect private keys, passphrases, signed JWTs, or secret-manager plaintext. Route remediation to **RB-005 — Key-Pair Authentication Failure**.

## 27. Branch — Programmatic Access Token

Only inspect PAT state when PAT authentication is expected:

```sql
SHOW USER PROGRAMMATIC ACCESS TOKENS
FOR USER "<username>";
```

Identify expected token state, lifecycle/rotation, client use, identity state, and policy interactions. RB-003 must not automatically re-enable or replace a PAT. Credential lifecycle changes require separately authorized remediation. Never record PAT secrets.

## 28. Branch — Network Policy

Investigate observed source IP, expected NAT/egress IP, user/account-level policies, allowed/blocked ranges, and recent network changes. Never remove a production network policy merely to test authentication. Route confirmed remediation to **RB-007 — Network Policy Blocking Access**.

## 29. Branch — Client / Connector Failure

A valid final diagnosis is that Snowflake identity/authentication controls are healthy and the failure is client-side. Investigate account identifier, endpoint, `LOGIN_NAME`, authenticator, stale credential/token, key path, secret injection, proxy, environment variables, connector version, workstation/Citrix, and application deployment regression.

Do not modify Snowflake merely because one client fails.

## 30. Client Isolation Test

Where policy permits, determine whether the failure follows the identity, client, network, or authentication provider using an approved alternate client and the same approved authentication method. Do not transfer production passwords, private keys, PATs, or OAuth tokens between systems to perform the test.

## 31. Multiple-User Failure Path

For multiple unrelated users/workloads, stop individual resets/unlocks and investigate shared dependencies. Escalate as a major incident when appropriate.

## 32. Snowflake Service Investigation

When evidence points toward Snowflake service degradation, capture account, region, failure start, affected identities/workloads, authentication methods, errors, last known good, client types, source locations, and recent changes. Route as appropriate to RB-083, RB-088, and RB-089.

Do not attribute the incident to Snowflake solely because one user or client cannot authenticate.

## 33. Authentication vs Authorization Gate

Successful authentication does not guarantee object access. If login succeeds but access is denied, authentication troubleshooting is complete.

```sql
SHOW GRANTS TO USER "<username>";
```

Use this for diagnosis only. Do not grant additional privileges under RB-003; route to the Roles, Grants & Permissions runbooks.

## 34. Routing Matrix

| Finding | Route / Action |
|---|---|
| Wrong account/endpoint | Correct client configuration |
| Wrong `LOGIN_NAME` | Correct client identity configuration |
| User missing | Verify account/provisioning |
| Disabled identity | RB-002 |
| Temporary lock | RB-002 |
| Password replacement required | RB-001 |
| `MUST_CHANGE_PASSWORD` | Complete required workflow |
| MFA | RB-004 |
| Key pair/JWT | RB-005 |
| SSO/SAML | RB-006 |
| OAuth | RB-006 |
| Network policy | RB-007 |
| PAT issue | Approved token-lifecycle remediation |
| Client-only failure | Client/application owner |
| Authorization issue | Roles/Permissions runbook |
| Suspicious authentication | RB-078 |
| Multiple unrelated users | Major incident investigation |
| Snowflake-side issue | RB-083/RB-088/RB-089 |

## 35. Validation

After remediation through the specialized runbook, validate the original authentication path. Do not substitute an administrator test for the original workflow.

For an interactive user, a low-risk session check can include:

```sql
SELECT
    CURRENT_USER(),
    CURRENT_ROLE(),
    CURRENT_WAREHOUSE();
```

Never ask the user to provide authentication secrets for validation.

## 36. Stability Validation

For automated workloads, one successful authentication is insufficient. Observe briefly and confirm repeated failures have stopped, no immediate re-lock occurs, and the workload remains stable. If failures continue, return to diagnosis rather than repeatedly executing the same remediation.

## 37. Successful Resolution Criteria

Confirm the environment/account/endpoint and exact identity, understand `NAME` vs `LOGIN_NAME`, establish identity/authentication type, capture the exact failure and blast radius, establish last known good, correlate changes, identify the failure domain, use the correct remediation runbook, validate the original authentication path, confirm stability/no re-lock, distinguish authentication from authorization, preserve security controls, and capture no secrets.

## 38. Abort Conditions

Stop routine troubleshooting and escalate when credential compromise is suspected, identity ownership or environment is uncertain, multiple unrelated users suddenly fail, Security intentionally restricted the identity, remediation would weaken security controls, service dependencies are unknown, uncontrolled authentication retries continue, a shared Snowflake/IdP/network failure is suspected, or required changes exceed RB-003's diagnostic scope.

## 39. Rollback

RB-003 is diagnostic and should normally perform no state-changing remediation. Rollback belongs to the specialized runbook that performs the change: RB-001 for password reset, RB-002 for enable/unlock, RB-004 for MFA, RB-005 for key pair, RB-006 for SSO/OAuth, and RB-007 for network policy.

## 40. Escalation

Route Security issues to Security/IAM; SSO/SAML to IAM/IdP owner; OAuth to IAM/application owner; network issues to Network/Cloud; client/application issues to the application owner; key management to Security/application owner; and Snowflake service issues to Snowflake Support. Capture diagnostic evidence before escalation where operationally feasible.

## 41. Evidence to Capture

```text
RUNBOOK: RB-003
Environment/account:
Region:
Account identifier/endpoint:
User object NAME:
LOGIN_NAME:
Client-supplied username:
Identity type:
Authentication method:
Authenticator:
Client/application:
Client version:
Source IP:
Request/ticket:
Failure start:
Last known successful authentication:
Error code/message:
Blast radius:
Affected identities/workloads:
Recent changes:
Account/endpoint verified: Yes/No
DISABLED:
Temporary lock:
Expiration state:
MUST_CHANGE_PASSWORD:
Password/MFA/SSO/OAuth/key pair/PAT/network policy applicable:
Recent login-history findings:
Historical login-history findings:
Suspected failure domain:
Failure source contained: Yes/No/N/A
Child runbook invoked:
Remediation performed:
Original authentication path validated: Yes/No
Normal access validated: Yes/No
Repeated failures after remediation: Yes/No
Re-lock observed: Yes/No
Security escalation: Yes/No
Production impact:
Completion timestamp:
```

Never record passwords, temporary passwords, reset URLs, MFA codes, private keys/passphrases, signed JWTs, OAuth tokens, PAT secrets, session tokens, or other credential material.

## 42. Quick Diagnostic Procedure

```sql
-- RB-003 — DIAGNOSTIC ONLY
SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_USER();
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

For recent evidence use `INFORMATION_SCHEMA.LOGIN_HISTORY`; for historical evidence use `SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY`. Classify wrong environment/endpoint/login name, disabled/lock, password, MFA, SSO, OAuth, key/JWT, PAT, network policy, client, shared incident, or security incident, then route state-changing remediation to the specialized runbook.

## 43. Operational Guardrails

Always capture the exact error, determine blast radius early, verify account/endpoint and identity, distinguish `NAME` from `LOGIN_NAME`, establish the expected authentication mechanism, inspect login evidence, determine last known good, correlate changes, contain service retry storms, route state-changing actions to specialized runbooks, validate the original authentication path, and protect credential material.

Never blindly reset passwords, repeatedly unlock users, disable MFA to test, remove network policies to test, weaken authentication policies, expose tokens/private keys, restore PATs without authorization, grant elevated roles to solve authentication, create replacement identities as a shortcut, transfer production credentials to alternate machines for testing, or treat a multi-user outage as unrelated user tickets.

## 44. References

Use current Snowflake primary documentation as technical authority for `LOGIN_HISTORY` (Information Schema and Account Usage), `SHOW USERS`, `DESCRIBE USER`, user authentication, MFA, federated authentication/SSO, OAuth, key-pair authentication, programmatic access tokens, network policies, authentication policies, and access control.

---

**Canonical status:** `CANONICAL`  
**Workflow:** Draft → Technical + Source Review → Production + Copyright Review → Revised Final / Canonical Edition
