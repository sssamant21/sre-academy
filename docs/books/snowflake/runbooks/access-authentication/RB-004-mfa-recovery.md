# RB-004 — MFA Recovery

**Snowflake DBRE/SRE Production Runbook**  
**Runbook ID:** RB-004  
**Category:** Access & Authentication  
**Edition:** Revised Final / Canonical  
**Risk:** High  
**Primary Operator:** DBRE / SRE / Snowflake Administrator

## 1. Purpose

Use this runbook to safely diagnose and recover a human Snowflake user's access when MFA is the confirmed authentication failure domain. It covers lost/replaced factors, enrollment/re-enrollment, replacement-factor enrollment, removal of obsolete factors, controlled temporary bypass when explicitly authorized, and validation that strong authentication has been restored.

> **Core principle:** MFA recovery is complete only when legitimate access and the expected MFA protection are both restored.

## 2. Trigger / Alert

Use RB-004 for confirmed MFA failures such as a lost/replaced device, unavailable factor, MFA enrollment failure, inability to complete the expected challenge, or approved MFA re-enrollment. For an unclassified authentication failure, use **RB-003** first.

## 3. Impact / Severity

| Condition | Suggested Severity |
|---|---|
| Single non-critical user | Medium |
| Production engineer blocked | Medium–High |
| Privileged administrator / critical responder blocked | High |
| Multiple unrelated users | Major authentication incident |
| Suspicious MFA recovery request | Security incident |
| Account-wide MFA behavior changed | High / Security review |

## 4. STOP — Mandatory Pre-Recovery Gate

Do not enroll, remove, bypass, reset, or otherwise modify MFA until the correct account and identity are confirmed, `NAME`/`LOGIN_NAME`/`TYPE` are verified, requester identity is independently verified, recovery is explicitly authorized, MFA is confirmed as the failure domain, MFA authority is identified, security indicators are checked, and blast radius is established.

If these conditions cannot be established, **STOP AND ESCALATE**.

## 5. SECURITY STOP

Stop routine recovery for suspected credential compromise, stolen device plus suspicious activity, unexpected successful authentication/source IP, user-denied activity, unexpected MFA/policy changes, Security-imposed restrictions, unverifiable requester identity, or suspected social engineering. Route suspected compromise to **RB-078 — Compromised User Credentials** and preserve evidence unless immediate containment is required.

## 6. Identity Verification and Authorization

A claim such as "I lost my phone" is not sufficient identity proof. Use the organization's approved independent identity-verification process. Do not invent personal security questions or rely exclusively on the factor being recovered.

Identity verification and authorization are separate gates. Record both the verification method and authorization source.

## 7. Determine Blast Radius

Determine whether the issue affects one user/authentication path or multiple unrelated users/account-wide MFA behavior. For multiple unrelated users, stop individual recovery actions and investigate shared dependencies such as authentication policy, IdP, Snowflake service, shared MFA provider, or recent security-policy changes.

## 8. Required Access and Environment Verification

Use the lowest-privileged authorized role capable of the required operation.

```sql
SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_USER();
```

Do not use `ACCOUNTADMIN` for the entire incident merely because one diagnostic operation requires it.

## 9. Locate and Inspect the User

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

Verify environment/account, `NAME`, `LOGIN_NAME`, `TYPE`, disabled/lock state, authentication configuration, and owner. If the target cannot be positively identified, stop and return to RB-003. Never create a replacement user as a shortcut.

## 10. Identity-Type Hard Gate

RB-004 is for interactive human identities. If `TYPE=SERVICE` or `TYPE=SERVICE_AGENT`, stop RB-004 and return to RB-003 to investigate the workload's supported non-interactive authentication mechanism.

## 11. Confirm MFA Is the Failure Domain

Determine whether primary authentication succeeds, the user reaches an MFA challenge, the expected factor is unavailable, or enrollment itself fails. If authentication fails before MFA is involved, return to RB-003.

## 12. Determine MFA Authority

Determine whether MFA is enforced by Snowflake, the enterprise IdP, both, or another approved provider. If the factor is entirely IdP-controlled, use the IAM/IdP recovery process. For SSO/OAuth issues route to RB-006 as appropriate.

## 13. Authentication Evidence

For recent evidence:

```sql
SELECT EVENT_TIMESTAMP, USER_NAME, CLIENT_IP, REPORTED_CLIENT_TYPE,
       REPORTED_CLIENT_VERSION, IS_SUCCESS, ERROR_CODE, ERROR_MESSAGE
FROM TABLE(
    INFORMATION_SCHEMA.LOGIN_HISTORY(
        TIME_RANGE_START => DATEADD('hour', -1, CURRENT_TIMESTAMP()),
        RESULT_LIMIT => 1000
    )
)
WHERE USER_NAME = '<username>'
ORDER BY EVENT_TIMESTAMP DESC;
```

For historical evidence:

```sql
SELECT EVENT_TIMESTAMP, USER_NAME, CLIENT_IP, REPORTED_CLIENT_TYPE,
       REPORTED_CLIENT_VERSION, IS_SUCCESS, ERROR_CODE, ERROR_MESSAGE
FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
WHERE USER_NAME = '<username>'
ORDER BY EVENT_TIMESTAMP DESC
LIMIT 50;
```

Account Usage can have ingestion latency; absence of a recent row is not proof that no authentication attempt occurred.

## 14. Inspect Current MFA Methods

When Snowflake owns the MFA factor and the operator is authorized:

```sql
SHOW MFA METHODS FOR USER "<username>";
```

Inspection of another user's MFA methods may require `ACCOUNTADMIN`. Where required and authorized:

```sql
USE ROLE ACCOUNTADMIN;
SHOW MFA METHODS FOR USER "<username>";
```

Use the elevated role only for operations that require it. Capture method metadata only; never capture MFA secrets.

Current Snowflake MFA methods can include `PASSKEY`, `TOTP`, and `DUO`, subject to effective authentication policy.

## 15. Recovery Decision Matrix

| Finding | Action |
|---|---|
| MFA not actually failing | RB-003 |
| SERVICE / SERVICE_AGENT | RB-003 |
| Temporary factor problem | Wait/retry where appropriate |
| Lost/replaced Snowflake factor | Replacement-first recovery |
| Snowflake enrollment problem | Diagnose enrollment/policy |
| IdP-owned MFA | IAM/IdP recovery |
| Disabled/locked user | RB-002 |
| Password issue | RB-001 |
| SSO/OAuth issue | RB-006 |
| Suspicious activity | RB-078 |
| Multiple users | Shared incident investigation |
| Emergency privileged access | RB-008 |
| Identity cannot be verified | STOP / Security-IAM |

## 16. Preferred Recovery Strategy

The normal production order is: inspect current MFA methods → enroll replacement → user completes enrollment → verify replacement → remove obsolete factor if required → set default factor only if required → validate original authentication path → confirm MFA protection restored.

> **Replacement-first recovery is the default.** Do not begin by removing every MFA method.

## 17. Initiate Replacement Enrollment

After all safety gates pass:

```sql
ALTER USER "<username>"
ENROLL MFA;
```

The user completes the supported enrollment workflow. Depending on configuration, Snowflake can use verified-email delivery or provide an enrollment URL.

## 18. Enrollment URL and Secret Handling

Treat an MFA enrollment URL as sensitive temporary authentication material. Never store the actual URL in Git, Slack/Teams, tickets, screenshots, incident transcripts, shared notes, or documentation unless a specifically approved secure-delivery process permits the channel.

Evidence should record only whether an enrollment URL was generated and securely delivered. Never record the URL itself.

Never request or store TOTP seeds, QR secrets, MFA response codes, passkey secret material, recovery secrets, device backup secrets, passwords, tokens, private keys, or session tokens.

## 19. Verify Replacement Method

After enrollment:

```sql
SHOW MFA METHODS FOR USER "<username>";
```

Confirm the expected replacement exists, the method type is correct, and no unexpected factor was introduced.

## 20. Remove Obsolete MFA Method

Only after identifying the exact obsolete method:

```sql
ALTER USER "<username>"
REMOVE MFA METHOD <obsolete_mfa_method>;
```

Prefer enroll replacement → validate replacement → remove obsolete factor. Preserve healthy backup factors unless there is a documented security reason to revoke them.

## 21. Optional Default MFA Method

Where multiple methods exist and an approved default change is required:

```sql
ALTER USER "<username>"
SET DEFAULT_MFA_METHOD = <approved_method>;
```

Do not change the default merely because recovery occurred.

## 22. Temporary MFA Bypass — Exception Only

Snowflake provides:

```sql
ALTER USER "<username>"
SET MINS_TO_BYPASS_MFA = <approved_minutes>;
```

**WARNING:** This temporarily reduces authentication protection and is not the standard recovery mechanism.

Use it only when identity is independently verified, recovery is explicitly authorized, compromise is ruled out, urgent business need exists, normal enrollment cannot meet that need, the minimum practical duration is selected, the user is ready to restore MFA, and the operator will validate closure.

Never standardize a fixed duration; use the shortest operationally appropriate approved interval.

A successful login during bypass does not close the incident. MFA must be restored, verified, and the normal MFA-protected authentication path must succeed before closure.

## 23. DISABLE_MFA — Not Standard Recovery

`ALTER USER ... SET DISABLE_MFA = TRUE` is not the standard RB-004 recovery action. Its effect is broader than replacing a single factor. Any exceptional use requires separate security authorization and explicit impact analysis.

## 24. Authentication Policy and Snowsight Enrollment

Investigate effective authentication policy when expected methods disappear, enrollment behavior changes, or multiple users are affected. Do not modify account-wide authentication policy to fix one user; such a change requires separate change control.

Where Snowflake requires MFA enrollment through Snowsight, complete the supported enrollment workflow before repeatedly testing JDBC, ODBC, Python, or other clients.

## 25. Break-Glass Boundary

Normal MFA recovery belongs to RB-004. Emergency privileged/break-glass access belongs to **RB-008**. Do not introduce break-glass OTPs or emergency identities into routine RB-004 recovery.

## 26. Password and User-State Separation

Password problem → RB-001. Disabled/locked identity → RB-002. MFA problem → RB-004. Do not automatically perform all three changes because one authentication attempt fails. If multiple factors may be compromised, route to RB-078.

## 27. Validate Original Authentication Path

Validate the user's intended production path (for example password + Snowflake MFA or SSO + MFA), not an unintended alternate path.

After successful authentication:

```sql
SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE();
```

Never request an MFA code as proof.

## 28. Validate MFA Protection and Stability

Confirm the expected replacement method exists and works, obsolete factor is handled appropriately, no unexpected factor exists, default is correct if changed, no unintended bypass remains, and normal MFA-protected authentication succeeds.

Briefly observe for repeated failures, re-lock, unexpected successful logins/source IPs, unexpected factor enrollment, or continued MFA failure. Re-diagnose rather than repeatedly resetting MFA.

## 29. Authentication vs Authorization

Once MFA-protected authentication succeeds, authorization errors are outside RB-004. `SHOW GRANTS TO USER "<username>";` can support diagnosis; route permission problems to the Roles, Grants & Permissions runbooks rather than modifying MFA again.

## 30. Successful Resolution Criteria

RB-004 is complete when the correct account/user and `TYPE=PERSON` are confirmed; requester identity and authorization are verified; MFA failure/authority/blast radius are established; security checks pass; current methods are understood; approved recovery is used; replacement is enrolled and validated where required; obsolete factor is handled appropriately; original authentication succeeds; expected MFA protection is restored; no unintended bypass or unauthorized factor remains; no immediate repeated failure/re-lock occurs; no secret is captured; and evidence is recorded.

## 31. Abort Conditions

Stop and escalate when requester identity or authorization cannot be verified, compromise is suspected, Security restricted the identity, account/user is uncertain, MFA authority is unknown, target is a service identity, multiple unrelated users are affected, recovery requires weakening account-wide controls, privileges are insufficient, recovery cannot be performed safely, or break-glass access is required.

## 32. Rollback / Failed Recovery

MFA recovery has no conventional rollback. If the wrong factor/user is changed or protection is accidentally reduced: stop, assess exposure, contain the identity if required, notify Security/IAM, re-establish approved MFA state, revoke unintended factors, validate authentication, and review activity during the exposure window. Do not restore a compromised/unavailable old factor merely to reproduce the prior configuration.

## 33. Escalation

| Condition | Escalation |
|---|---|
| Identity-verification problem | IAM / Security |
| Suspicious MFA recovery | Security |
| Compromised/stolen factor | Security / IAM |
| Snowflake-native MFA problem | Snowflake Admin / Support |
| Enterprise IdP MFA | IAM / IdP team |
| Authentication-policy problem | IAM / Security / Snowflake Admin |
| Multiple-user MFA incident | Major incident team |
| Emergency access | RB-008 |
| Unsupported Snowflake behavior | Snowflake Support |

## 34. Evidence to Capture

```text
RUNBOOK: RB-004
Environment/account:
Region:
User NAME:
LOGIN_NAME:
TYPE:
Authentication path:
MFA authority:
Request/ticket:
Requester identity verified:
Verification method:
Recovery authorized:
Authorization source:
Administrator:
Administrative role:
Start timestamp:
Failure start:
Last successful authentication:
Error code/message:
Blast radius:
Recent changes:
Security concern:
Pre-recovery MFA methods:
Unavailable method name/type:
Recovery method:
Replacement enrollment initiated:
Enrollment URL generated:
Enrollment URL securely delivered:
Replacement method:
Replacement validated:
Obsolete method removed:
Default MFA method changed:
Temporary bypass used:
Bypass duration:
Bypass authorization:
Normal authentication validated:
MFA protection restored:
Unexpected factor present:
Repeated failures:
Unexpected login:
Security escalation:
Production impact:
Completion timestamp:
```

Never record the enrollment URL or any authentication secret.

## 35. Quick Operational Procedure

1. Capture exact MFA/authentication failure.
2. Determine blast radius.
3. Verify account/environment and `NAME`/`LOGIN_NAME`.
4. Confirm `TYPE=PERSON`.
5. Independently verify requester identity and recovery authorization.
6. Check security/compromise indicators.
7. Determine MFA authority and confirm MFA is the failure domain.
8. Inspect authentication evidence and current MFA methods.
9. Prefer replacement enrollment.
10. User completes enrollment; verify replacement.
11. Remove only obsolete factor if required.
12. Set default factor only if required.
13. Validate original authentication path and expected MFA protection.
14. Confirm no unintended bypass remains.
15. Observe for immediate repeated/suspicious failures.
16. Capture evidence and close/escalate.

Temporary MFA bypass is an exception branch, not a normal recovery step.

## 36. Quick SQL Reference

```sql
-- Verify environment
SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_USER();

-- Inspect user
SHOW USERS LIKE '<username>';
DESC USER "<username>";

-- Inspect MFA methods
SHOW MFA METHODS FOR USER "<username>";

-- Initiate replacement enrollment
ALTER USER "<username>" ENROLL MFA;

-- Remove confirmed obsolete factor
ALTER USER "<username>" REMOVE MFA METHOD <obsolete_mfa_method>;

-- Optional default factor
ALTER USER "<username>" SET DEFAULT_MFA_METHOD = <approved_method>;

-- EXCEPTION ONLY: temporary bypass
ALTER USER "<username>" SET MINS_TO_BYPASS_MFA = <approved_minutes>;
```

## 37. Operational Guardrails

Always verify the requester independently and authorization separately; establish blast radius; confirm exact identity and `TYPE=PERSON`; determine MFA ownership; inspect factors before changing them; prefer replacement-first recovery; protect enrollment material; validate replacement before removing healthy factors; use temporary bypass only as a tightly controlled exception; validate the original authentication path; and prove MFA protection is restored.

Never reset MFA solely because someone claims device loss, use a ticket as identity proof, treat service identities as MFA users, remove every factor first, disable account-wide MFA for one user, weaken authentication policy to troubleshoot, expose secrets/enrollment URLs, use `ACCOUNTADMIN` for unrelated actions, use bypass as routine recovery, leave a bypass unresolved, create privileged replacement identities, or mix break-glass access into normal recovery.

## 38. References

Use current Snowflake primary documentation as canonical technical authority for MFA, second-factor configuration, `ALTER USER`, `SHOW MFA METHODS`, authentication policies, user types/administration, strong-authentication requirements, login history, and federated authentication/SSO.

---

**Canonical status:** `CANONICAL`  
**Workflow:** Draft → Technical + Source Review → Production + Copyright Review → Revised Final / Canonical Edition
