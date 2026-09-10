# RB-006 — SSO/OAuth Failure

**Snowflake DBRE/SRE Production Runbook**  
**Runbook ID:** RB-006  
**Category:** Access & Authentication  
**Edition:** Revised Final / Canonical  
**Risk:** High  
**Primary Operator:** DBRE / SRE / Snowflake Administrator  
**Supporting Teams:** IAM / Security / Identity Provider Team / Application Owner

> **Core principle:** Identify the authentication model, blast radius, security integration, and failing trust boundary before changing Snowflake, the identity provider, certificates, OAuth configuration, or authentication policy.

## 1. Purpose

Use this runbook to diagnose and safely recover Snowflake authentication failures involving SAML2 federated SSO, OIDC federated SSO, Snowflake OAuth, External OAuth, identity/claim mapping, SAML certificates, OAuth tokens, external authorization servers, JWKS/signing-key relationships, OAuth role restrictions, and authentication-policy interactions.

This is an authentication incident runbook, not a generic IdP/OAuth administration guide.

## 2. Authentication Models

Always establish the exact model:

```text
SSO
├── SAML2
└── OIDC

OAuth
├── Snowflake OAuth
└── External OAuth
```

Do not treat these mechanisms as interchangeable.

> **OIDC production note:** OIDC federated SSO was Public Preview during the September 2026 source review. Verify current Snowflake support status, account availability, organizational approval, and applicable limitations before production configuration changes.

## 3. Trigger / Alert

Use RB-006 when SSO/SAML/OIDC authentication fails, a user authenticates at the IdP but Snowflake rejects login, an SSO redirect loop occurs, an OAuth token is rejected, a production OAuth workload stops authenticating, or failures correlate with IdP certificate/signing-key/security-integration changes.

If the authentication mechanism has not been established, use **RB-003 — Troubleshoot Login / Authentication Failure** first.

## 4. Impact / Severity

Potential impact includes individual-user loss of access, department/team outage, BI/reporting outage, production application or pipeline failure, multiple OAuth consumer outage, organization-wide SSO outage, or security incident.

| Condition | Suggested Severity |
|---|---|
| Single non-production user | Low–Medium |
| Single production user | Medium |
| Small production group | Medium–High |
| Production OAuth application | High |
| Multiple production applications | High |
| All federated users | Major incident |
| Multiple authentication mechanisms | Major incident |
| Unauthorized integration change | Security incident |
| Token/secret/signing-key compromise | Security incident |

Follow organizational severity standards where they differ.

## 5. Mandatory Safety Gate

Before changing authentication configuration:

```text
[ ] Correct Snowflake account/environment confirmed
[ ] Exact user/application identified
[ ] Authentication model identified
[ ] SAML2 / OIDC / Snowflake OAuth / External OAuth established
[ ] Identity provider/authorization server identified
[ ] Snowflake security integration identified
[ ] Integration TYPE confirmed
[ ] Integration ENABLED state inspected
[ ] Exact failure captured
[ ] Blast radius established
[ ] Last known good established
[ ] Shared users/consumers identified
[ ] Recent changes reviewed
[ ] Security concern evaluated
[ ] Change authorization available
[ ] Rollback path understood
```

Do not proceed with state-changing authentication commands until this gate is satisfied, except for approved security containment.

## 6. SECURITY STOP

Stop routine recovery if signing-key compromise, OAuth secret/token exposure, unauthorized integration changes, suspicious successful authentication, intentional Security containment, or other compromise indicators exist.

Escalate to Security and the applicable security incident runbook. Never restore compromised authentication material merely to recover service.

## 7. Credential Handling — Hard Rule

Never capture passwords, temporary passwords, SAML signing private keys, OIDC/OAuth client secrets, access tokens, refresh tokens, authorization codes, bearer headers, private keys, PAT secrets, session tokens, or MFA seeds/codes.

Never paste production tokens into public online token/JWT decoders.

Safe evidence can include public certificates/fingerprints, issuer, audience/resource, token timestamps, scope names, role claims, client IDs, integration names, mapping claim names, error codes, and timestamps, subject to organizational policy.

## 8. Required Access

Use least privilege. Ownership may span Snowflake Administration, IAM, Identity Provider Administration, Security, Application Engineering, and Platform/Cloud teams.

Do not run the entire incident using ACCOUNTADMIN merely because an isolated diagnostic operation may require elevated access. Record elevated-role usage.

## 9. Verify Snowflake Environment

```sql
SELECT
    CURRENT_ACCOUNT(),
    CURRENT_REGION(),
    CURRENT_ROLE(),
    CURRENT_USER();
```

Confirm the intended account before changing authentication infrastructure.

## 10. Verify Identity

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

Confirm NAME, LOGIN_NAME, TYPE, and DISABLED state. If the identity is disabled/locked, route to **RB-002 — Unlock/Restore User Access** as appropriate.

## 11. Identify Authentication Model

```text
SAML2 SSO       → RB-006 SAML2 branch
OIDC SSO        → RB-006 OIDC branch
Snowflake OAuth → RB-006 Snowflake OAuth branch
External OAuth  → RB-006 External OAuth branch
Key pair/JWT    → RB-005
MFA             → RB-004
Password        → RB-001/RB-003
```

## 12. Determine Blast Radius

Classify the incident as one user, one application, one group, one integration, one IdP, all federated users, multiple applications, or multiple authentication mechanisms.

One-user failures point first toward identity/assignment/mapping/client state. Broad SSO failures point toward IdP/integration/certificate/shared controls. One OAuth application points toward client/token/configuration. Multiple External OAuth clients point toward IdP/issuer/JWKS/shared integration.

Do not apply account-wide remediation to an isolated failure.

## 13. Shared Consumer Inventory

Before changing shared authentication infrastructure, record the integration, owner, authentication model, affected users/applications, known consumers, environment, current state, proposed change, expected blast radius, rollback, and approval.

## 14. Establish Last Known Good

Capture the last successful authentication, first known failure, and recent IdP, certificate, signing-key, security-integration, authentication-policy, provisioning/mapping, application, and OAuth changes.

Use the timeline `LAST KNOWN GOOD → CHANGE → FIRST FAILURE` to prioritize investigation without assuming correlation proves causation.

## 15. Authentication Evidence

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

Use this to establish last success, first failure, source IP, client, repeated failures, and suspicious successes.

## 16. Historical Evidence

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

Account Usage can have ingestion latency; absence of a row is not proof that an attempt never occurred.

## 17. Discover and Inspect Security Integration

```sql
SHOW SECURITY INTEGRATIONS;
```

or:

```sql
SHOW SECURITY INTEGRATIONS LIKE '<pattern>';
```

Then:

```sql
DESC SECURITY INTEGRATION <integration_name>;
```

Determine NAME, TYPE, ENABLED, and model-specific properties.

If the expected integration is not visible, verify role/privilege visibility before concluding that it does not exist. Never create a duplicate integration because the current role cannot see the original.

If `ENABLED = FALSE`, determine who disabled it, when, why, whether Security containment was involved, and whether re-enabling is authorized.

## 18. SAML2 Branch

Trust path:

```text
User → Snowflake/IdP entry point → IdP → SAML assertion → Snowflake SAML2 integration → identity mapping → Snowflake controls → session
```

Inspect:

```sql
DESC SECURITY INTEGRATION <saml_integration>;
```

Review applicable properties including ENABLED, SAML2_ISSUER, SAML2_SSO_URL, SAML2_PROVIDER, SAML2_X509_CERT, SAML2_SNOWFLAKE_ISSUER_URL, SAML2_SNOWFLAKE_ACS_URL, SAML2_ENABLE_SP_INITIATED, SAML2_SIGN_REQUEST, and SAML2_REQUESTED_NAMEID_FORMAT.

Compare Snowflake NAME/LOGIN_NAME with the IdP subject/SAML NameID and expected enterprise identity. A correctly signed assertion can still fail because identity mapping is wrong.

For isolated failure, verify user existence, active state, Snowflake application assignment, required group membership, and applicable IdP policy through approved IAM tooling.

### SAML Certificate Gate

When broad failure correlates with IdP certificate rotation, confirm the rotation, identify the current public certificate/fingerprint, inspect Snowflake integration state, prove a mismatch, engage the IAM owner, obtain approval, select a controlled validation identity, and understand rollback before changing configuration.

Never request or capture the IdP signing private key.

### Snowflake SAML Private-Key Guardrail

Do **not** use:

```sql
ALTER SECURITY INTEGRATION <integration_name>
REFRESH SAML2_SNOWFLAKE_PRIVATE_KEY;
```

as exploratory incident troubleshooting. Use a separately planned SAML key/certificate rotation procedure.

Metadata refresh is also state-changing; use it only after the metadata source and mismatch are established and the change is authorized.

For redirect loops, inspect account URL, IdP application, SSO/ACS URLs, integration, assignment, mapping, browser/session state, authentication policy, and identifier-first routing.

Determine whether IdP-initiated or Snowflake/SP-initiated authentication fails; preserve the distinction as evidence.

## 19. OIDC Federated SSO Branch

OIDC federated SSO was Public Preview during this runbook's source review. Verify current feature status before production changes.

Trust path:

```text
User → login routing/identifier → OIDC provider → authentication → claims → Snowflake OIDC integration → identity mapping → policy/MFA → session
```

Investigate provider, integration, enabled state, user identity, expected identity claim, provider application, consent, tenant, identifier-first login, authentication policy, MFA requirement, and recent provider/integration changes.

When multiple SSO integrations exist, inspect enabled integrations, identifier-first login design, supplied user identifier, expected provider routing, and policy before disabling anything.

Because OIDC is Preview in the reviewed source state, escalate earlier when configuration, provider state, mapping, and policy all appear correct but the failure remains reproducible.

## 20. Snowflake OAuth Branch

Trust path:

```text
Application/User → Snowflake authorization endpoint → Snowflake token endpoint → Snowflake-issued access token → Snowflake → role/authorization → session
```

Inspect:

```sql
DESC SECURITY INTEGRATION <oauth_integration>;
```

Review relevant ENABLED, OAUTH_CLIENT, OAUTH_ISSUE_REFRESH_TOKENS, OAUTH_ACCESS_TOKEN_VALIDITY, OAUTH_REFRESH_TOKEN_VALIDITY, BLOCKED_ROLES_LIST, and PRE_AUTHORIZED_ROLES_LIST properties where applicable.

Where applicable, inspect delegated authorization:

```sql
SHOW DELEGATED AUTHORIZATIONS
BY USER <username>;
```

and with appropriate authorization:

```sql
SHOW DELEGATED AUTHORIZATIONS
TO SECURITY INTEGRATION <integration_name>;
```

Revocation is state-changing and can invalidate authentication state. Do not revoke authorization merely as a test.

For refresh failure, inspect whether refresh tokens are enabled, refresh-token lifecycle, delegated authorization, client configuration, client secret/configuration where applicable, and application token caching. Do not simply extend token lifetime.

If token issuance/authentication succeeds but role selection fails, inspect user grants and OAuth role restrictions rather than rotating credentials.

## 21. External OAuth Branch

Trust path:

```text
Application → external authorization server → access token → Snowflake External OAuth integration → issuer validation → signature/JWKS validation → claim/user mapping → role → session
```

Inspect:

```sql
DESC SECURITY INTEGRATION <external_oauth_integration>;
```

Review applicable ENABLED, EXTERNAL_OAUTH_TYPE, EXTERNAL_OAUTH_ISSUER, EXTERNAL_OAUTH_JWS_KEYS_URL, EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM, and EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE properties, plus provider-specific audience/resource and role configuration.

Verify token issuer against the configured issuer. Correct wrong-tenant/environment/authorization-server configuration rather than weakening validation.

For broad failures, check authorization-server health, recent signing-key rotation, JWS/JWKS relationship, issuer, and Snowflake integration. Never request the authorization server's signing private key.

Understand identity mapping as:

```text
Token identity claim → configured token mapping claim → Snowflake mapping attribute → Snowflake user
```

A cryptographically valid token can still fail because mapping is wrong. Do not rotate signing keys to fix mapping.

Compare the intended audience/resource with the provider/integration configuration. Do not weaken audience validation to accept a token intended for another environment/resource.

## 22. Token Expiration and Time

Establish issued-at time, expiration, current trusted time, and whether refresh was attempted. An expired token usually points first to application/token lifecycle rather than Snowflake security-integration failure.

Check host time where appropriate:

```bash
date -u
```

and where available:

```bash
timedatectl status
```

Investigate NTP, not-before/expiration times, application delay, and network delay. Do not extend token validity to hide clock drift.

## 23. Authentication Policy

If federation/token configuration appears correct, inspect the effective authentication policy. Determine whether the intended authentication method is permitted, whether external-authentication MFA is required, whether a different policy applies to the identity/application, and whether policy configuration recently changed.

Never weaken an account-wide authentication policy merely to test authentication.

If external authentication succeeds but Snowflake MFA fails, stop RB-006 and route to **RB-004 — MFA Recovery**.

## 24. Authentication vs Authorization

If authentication succeeds but role/warehouse/database/schema/object access fails, the authentication incident is resolved. Route authorization problems to **RB-009 — Grant User/Role Access** or **RB-010 — Troubleshoot Insufficient Privileges**.

Do not continue rotating OAuth credentials/certificates.

## 25. Shared Failure Gate

If many users fail through one SSO path, stop per-user remediation and investigate the shared IdP/integration/certificate/policy.

If multiple applications fail through one External OAuth provider, stop per-client credential rotation and investigate the shared IdP/JWKS/issuer/integration.

## 26. Recovery Patterns

### Isolated SSO User

```text
Verify identity → IdP assignment → LOGIN_NAME/federation mapping → user state → expected SSO route → minimum correction → validate original SSO path
```

### Shared SAML2 Failure

```text
Confirm shared failure → IdP health → SAML2 integration → issuer/URLs/certificate → recent changes → prove mismatch → minimum approved correction → controlled identity → representative population
```

### OIDC Failure

```text
Confirm feature/provider state → OIDC integration → routing/identifier-first login → claims/mapping → consent → policy/MFA → minimum correction → controlled validation
```

### Snowflake OAuth

```text
Integration → client → delegated authorization → token lifecycle → role restrictions → minimum correction → valid token → Snowflake session
```

### External OAuth

```text
Authorization server → issuer → audience/resource → JWKS/signing relationship → user mapping → role/scope → minimum correction → valid token → Snowflake session
```

## 27. Emergency Access Boundary

Do not use passwords as a routine SSO bypass, disable MFA to troubleshoot federation, or create replacement privileged identities. If emergency administrative access is genuinely required, use **RB-008 — Emergency/Break-Glass Access**.

## 28. Change-Control Guardrails

Do not use `CREATE OR REPLACE SECURITY INTEGRATION` as routine incident recovery. Inspect actual state, identify the exact mismatch, alter the minimum necessary property, and validate.

Change one failure domain at a time. Avoid simultaneous certificate, issuer, LOGIN_NAME, authentication-policy, and OAuth changes. Preserve causality and rollback.

## 29. Controlled Validation

For shared SSO, validate a controlled identity, then a representative second identity/group, then the broader population.

For OAuth, validate a controlled application instance through token acquisition, Snowflake authentication, and session validation before restoring broader workload traffic.

Do not immediately release a large retry storm after a configuration change.

## 30. Validate Original Authentication Path

The original mechanism must work:

```text
SAML incident     → SAML must work
OIDC incident     → OIDC must work
Snowflake OAuth   → Snowflake OAuth must work
External OAuth    → External OAuth must work
```

Success using a password, key pair, another IdP, or break-glass identity does not prove RB-006 is resolved.

Where safe:

```sql
SELECT
    CURRENT_USER(),
    CURRENT_ROLE(),
    CURRENT_WAREHOUSE();
```

Do not perform a production write merely to prove authentication.

## 31. Stability Validation

```text
[ ] Original authentication path works
[ ] Expected users/applications recovered
[ ] Representative consumers validated
[ ] Repeated failures stopped
[ ] Retry storm stopped
[ ] Expected identity mapping confirmed
[ ] No unexpected authentication successes
[ ] No unintended fallback/bypass remains
[ ] No credential/token exposed
[ ] Shared integration stable
[ ] Authentication policy remains approved
[ ] Emergency access closed where applicable
[ ] Evidence captured
```

## 32. Rollback

For ordinary non-security configuration changes:

```text
Known-good configuration → approved correction → authentication worsens → restore known-good configuration → validate original path
```

Never roll back to compromised certificates, client secrets, signing keys, unauthorized configuration, or known-insecure policy. Security containment takes precedence.

## 33. Abort Conditions

Stop routine remediation if the authentication model/account/integration ownership/blast radius cannot be established; multiple unrelated authentication mechanisms fail; credential/signing-key compromise is suspected; unauthorized integration changes exist; Security intentionally disabled the integration; remediation requires weakening controls; authorization is unavailable; safe rollback cannot be established; or OIDC Preview behavior remains unexplained after configuration verification.

Escalate rather than experiment.

## 34. Escalation

| Condition | Escalation |
|---|---|
| SAML2 integration | IAM / Snowflake Admin |
| IdP assignment/mapping | IAM |
| IdP outage | IAM / Provider |
| Certificate problem | IAM / Security |
| OIDC Preview issue | IAM / Snowflake Support |
| Snowflake OAuth | Application / Snowflake Admin |
| External OAuth | IAM / Application / Snowflake Admin |
| JWKS/signing-key issue | IAM / Security |
| Token/secret compromise | Security |
| Authentication policy | Security / Snowflake Admin |
| MFA failure | RB-004 |
| Emergency access | RB-008 |
| Authorization issue | RB-009/RB-010 |
| Snowflake service issue | RB-083 |
| Support evidence | RB-088 |
| Support escalation | RB-089 |

## 35. Evidence to Capture

```text
RUNBOOK: RB-006
Environment/account:
Region:
Request/ticket:
Affected identity/application:
Snowflake NAME:
LOGIN_NAME:
TYPE:
Authentication model:
Identity provider:
Authorization server:
Security integration:
Integration TYPE:
Integration ENABLED:
Failure start:
Last successful authentication:
Exact error:
Error code:
Source IP:
Blast radius:
Production impact:
Known users/consumers:
Integration owner:
Recent IdP change:
Recent certificate/signing-key rotation:
Recent Snowflake integration change:
Recent authentication-policy change:
Recent application deployment:
Recent provisioning/mapping change:
SAML issuer/URLs/mapping/public certificate fingerprint/expiration:
OIDC provider/current support state/routing/claim/consent/policy/MFA:
Snowflake OAuth client/refresh configuration/delegated authorization/role restrictions:
External OAuth type/issuer/JWKS/mapping claim/mapping attribute/audience/role:
Clock synchronization:
Root cause:
Remediation:
Controlled validation:
Original authentication path validated:
Representative users/consumers validated:
Repeated failures stopped:
Rollback required:
Security escalation:
Snowflake operator:
Administrative role:
IAM operator:
Application owner:
Start timestamp:
Completion timestamp:
```

Never include secret/token/private-key material in the evidence record.

## 36. Quick Production Procedure

```text
1. Capture exact error.
2. Determine blast radius.
3. Verify Snowflake account/environment.
4. Identify user/application.
5. Identify SAML2 / OIDC / Snowflake OAuth / External OAuth.
6. Identify IdP/authorization server.
7. Identify Snowflake security integration.
8. SHOW SECURITY INTEGRATIONS.
9. DESC SECURITY INTEGRATION.
10. Confirm TYPE and ENABLED state.
11. Establish last known good.
12. Review recent changes.
13. Inspect authentication evidence.
14. Evaluate security indicators.
15. SAML2: assignment, mapping, issuer, URLs, certificate, metadata/key changes.
16. OIDC: provider/support state, routing, identifier-first login, claim, consent, policy/MFA.
17. Snowflake OAuth: client, integration, delegated authorization, lifecycle, refresh config, role restrictions.
18. External OAuth: issuer, audience, JWKS, user mapping, role/scope.
19. Verify time dependencies.
20. Verify effective authentication policy.
21. Identify exact failing trust boundary.
22. Apply minimum authorized correction.
23. Validate controlled user/client.
24. Validate ORIGINAL authentication path.
25. Validate representative population/consumers.
26. Confirm failures/retries stop.
27. Confirm no security bypass remains.
28. Capture evidence.
29. Close or escalate.
```

## 37. Production Guardrails

### Always

- identify the exact authentication model;
- establish blast radius first;
- identify shared consumers;
- inspect actual integration state;
- establish last known good;
- verify identity mapping;
- correlate recent changes;
- protect credentials/tokens/private keys;
- determine shared vs isolated failure;
- change one failure domain at a time;
- apply minimum remediation;
- validate the original authentication path;
- validate representative consumers after shared changes;
- preserve approved security controls.

### Never

- disable SSO account-wide for one user;
- disable MFA to troubleshoot federation;
- reset passwords as routine SSO bypass;
- expose OAuth tokens/client secrets;
- request IdP signing private keys;
- blindly replace certificates;
- experimentally refresh Snowflake SAML private keys;
- refresh SAML metadata without evidence;
- rotate every OAuth client during a shared outage;
- weaken issuer/audience validation;
- weaken authentication policy;
- use `CREATE OR REPLACE SECURITY INTEGRATION` as routine recovery;
- create privileged replacement identities;
- treat alternate authentication as proof of recovery.

## 38. References

Primary technical authority is current Snowflake documentation covering federated authentication, SAML2/OIDC security integrations, integration discovery/description, certificate management, Snowflake OAuth, delegated OAuth authorization, External OAuth, issuer/JWS/JWKS validation, user mapping, OAuth role controls, authentication policies, login history, and Snowflake user identity attributes.

- Snowflake: Configure SAML2 federated authentication — https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-security-integration
- Snowflake: ALTER SECURITY INTEGRATION for SAML2 — https://docs.snowflake.com/en/sql-reference/sql/alter-security-integration-saml2
- Snowflake: DESCRIBE INTEGRATION — https://docs.snowflake.com/en/sql-reference/sql/desc-integration
- Snowflake: Snowflake OAuth security integration — https://docs.snowflake.com/en/sql-reference/sql/create-security-integration-oauth-snowflake
- Snowflake: External OAuth security integration — https://docs.snowflake.com/en/sql-reference/sql/create-security-integration-oauth-external
- Snowflake: OIDC federated authentication 2026 release note — https://docs.snowflake.com/en/release-notes/2026/other/2026-07-17-oidc-federated-authentication-preview

## Canonical Decision

**RB-006 — SSO/OAuth Failure: CANONICAL**

Canonical operating model:

```text
Authentication failure
→ identify exact model
→ determine blast radius
→ identify integration
→ inspect actual production state
→ locate failing trust boundary
→ apply minimum authorized correction
→ controlled validation
→ validate ORIGINAL authentication path
→ validate broader population
→ close or escalate
```
