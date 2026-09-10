# RB-005 — Key-Pair Authentication Failure

**Snowflake DBRE/SRE Production Runbook**  
**Runbook ID:** RB-005  
**Category:** Access & Authentication  
**Edition:** Revised Final / Canonical  
**Risk:** High  
**Primary Operator:** DBRE / SRE / Snowflake Administrator

> **Core principle:** Diagnose before rotating. A key-pair authentication failure does not, by itself, prove that the key must be replaced.

## Purpose

Use this runbook to diagnose and safely recover Snowflake key-pair authentication failures affecting service identities, applications, ETL/ELT pipelines, Kubernetes workloads, scheduled jobs, CI/CD systems, automation, and supported Snowflake connectors/drivers.

The runbook supports both Snowflake key-management models:

- **Named key pairs** — inspect with `SHOW USER KEY PAIRS` and use the named-key lifecycle.
- **Legacy RSA slots** — inspect with `DESC USER` and manage `RSA_PUBLIC_KEY` / `RSA_PUBLIC_KEY_2`.

Do not migrate between these models merely because an authentication incident occurred.

## Trigger / Alert

Use RB-005 when investigation identifies key-pair/JWT authentication as the likely failure domain. Typical symptoms include JWT token invalid errors, application authentication failures, service identity failures, failures after key rotation, private-key load/passphrase errors, or inconsistent authentication across replicas.

If the authentication mechanism has not been established, start with **RB-003 — Troubleshoot Login / Authentication Failure**.

## Impact

Potential impacts include application outage, ingestion or pipeline failure, scheduled-job failure, unavailable automation, authentication retry storms, downstream SLA impact, or credential exposure. Shared service identities can increase blast radius because multiple workloads may depend on the same authentication state.

## Severity

| Condition | Suggested Severity |
|---|---|
| Development/test workload | Low–Medium |
| Single non-critical production workload | Medium |
| Production application/pipeline degraded | High |
| Critical processing stopped | High |
| Multiple consumers using same identity fail | High |
| Multiple unrelated identities fail | Major incident |
| Unauthorized key change/private-key compromise | Security incident |

## Safety Checks

Before changing any key:

- [ ] Correct Snowflake account/environment confirmed.
- [ ] Exact identity confirmed.
- [ ] `NAME` and `LOGIN_NAME` verified.
- [ ] `TYPE` verified.
- [ ] Workload owner identified.
- [ ] Known consumers identified.
- [ ] Authentication mechanism confirmed.
- [ ] NAMED vs LEGACY key model identified.
- [ ] Exact failure captured.
- [ ] Blast radius established.
- [ ] Last known successful authentication established.
- [ ] Registered key state inspected.
- [ ] Client public-key fingerprint determined where possible.
- [ ] Secret/runtime key version investigated.
- [ ] Recent changes reviewed.
- [ ] Security concern evaluated.
- [ ] Rotation authorization available if rotation may be required.

If unknown consumers may share the identity, **STOP before rotation**.

### Security STOP

Immediately stop routine troubleshooting if the private key was exposed, committed to Git, pasted into collaboration/ticket systems, obtained by unauthorized users, changed without authorization, associated with unexpected successful authentication, or cannot be reconciled with approved key inventory. Route suspected service-account compromise to RB-081 and emergency credential rotation to RB-082.

Never request or copy a production private key for troubleshooting. Never place private keys, passphrases, signed JWTs, secret plaintext, passwords, PAT secrets, OAuth tokens, session tokens, or cloud credentials in Git, tickets, chat, email, screenshots, documentation, incident transcripts, or shell history.

## Required Access

Use the lowest-privileged authorized administrative role capable of the required operation. For named-key administration, prefer appropriately delegated programmatic-authentication management privileges rather than using `ACCOUNTADMIN` for the entire incident. Use elevated roles only for operations that require them.

## Diagnosis

### Verify Administrative Context

```sql
SELECT
    CURRENT_ACCOUNT(),
    CURRENT_REGION(),
    CURRENT_ROLE(),
    CURRENT_USER();
```

### Verify Identity

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

Record `NAME`, `LOGIN_NAME`, `TYPE`, disabled state, and owner. Compare the client-configured username with the expected `LOGIN_NAME`. Do not rotate a key to fix a username mismatch.

Confirm that key-pair/JWT authentication is the intended mechanism. If the workload uses OAuth, PAT, workload identity, password, SSO, or another mechanism, return to RB-003.

### Determine Blast Radius and Consumers

Classify whether one process/pod, one application, one identity, all consumers of one secret, multiple identities, or multiple unrelated workloads are affected. If one replica fails while peers succeed, investigate runtime/secret drift first. Identify the workload owner, known consumers, secret source, connector/version, last deployment, and last rotation.

Contain excessive automated retries where operationally safe before making authentication changes.

### Determine Key-Management Model

For named key pairs:

```sql
SHOW USER KEY PAIRS FOR USER "<username>";
```

Review key name, fingerprint, status, expiration, last use, role restriction, and rotation relationship. Determine whether the expected key is present, active, expired, disabled, fingerprint-matched, role-restricted, or recently rotated.

For legacy RSA users:

```sql
DESC USER "<username>";
```

Inspect:

- `RSA_PUBLIC_KEY`
- `RSA_PUBLIC_KEY_FP`
- `RSA_PUBLIC_KEY_LAST_SET_TIME`
- `RSA_PUBLIC_KEY_2`
- `RSA_PUBLIC_KEY_2_FP`
- `RSA_PUBLIC_KEY_2_LAST_SET_TIME`

Do not assume slot 1 is old or slot 2 is new.

### Authentication Evidence

For recent failures:

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

For historical evidence:

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

Account Usage can have ingestion latency; absence of a row does not prove no attempt occurred.

### JWT Failure Details

If the client returns a Snowflake JWT failure UUID, preserve the UUID as non-secret diagnostic evidence and use:

```sql
SELECT SYSTEM$GET_LOGIN_FAILURE_DETAILS('<uuid>');
```

Retrieve failure details before rotating credentials when possible.

Important diagnostic categories include account mismatch, invalid user in issuer, public-key fingerprint mismatch, invalid signature, invalid algorithm, invalid issue time, invalid expiration time, and missing issue/expiration time.

### Fingerprint Comparison

Use public fingerprints rather than private keys:

1. Keep the client private key inside the approved security boundary.
2. Derive its corresponding public key/fingerprint using approved tooling.
3. Compare that fingerprint with the Snowflake registered fingerprint.

If fingerprints match, investigate account, `LOGIN_NAME`, JWT construction, timing, role restriction, authentication policy, connector, and runtime configuration before rotation. If they do not match, determine which state is stale: Snowflake, secret manager, runtime deployment, rotation inventory, or selected identity.

### Account, JWT, Time, and Client Checks

Verify the expected organization/account, configured account identifier, Snowflake request destination, and JWT account identity. Verify client username against `LOGIN_NAME`.

For RSA JWT authentication, investigate signing algorithm, signature/key pairing, token construction, issue/expiration times, host clock, NTP synchronization, CPU/disk pressure, scheduling delay, and network latency. Do not manually alter production clocks as a troubleshooting shortcut.

Keep JWT expiration, named-key expiration, and organizational key-rotation age as separate concepts.

### Secret and Runtime Checks

Verify the correct secret path, environment, secret version, workload authorization, secret injection/mount, formatting, private-key passphrase reference, private-key format, and connector-specific requirements.

A secret manager containing KEY B does not prove the running application is using KEY B. Check process/pod start time, mounted secret, environment injection, application reload behavior, rollout state, and runtime configuration.

If only one replica fails, investigate pod age, secret version, key path, passphrase source, connector version, and clock before making global identity changes.

### Named-Key Status, Role Restriction, and Policy

For named keys, inspect whether the key is active, expired, or disabled. Do not immediately re-enable a disabled key; determine who disabled it, why, and whether enabling is authorized.

If `ROLE_RESTRICTION` is configured, verify the requested role and that the role remains granted to the user. Do not rotate the key to fix a role mismatch.

If key/JWT/runtime configuration appears correct, inspect whether the effective authentication policy permits the intended programmatic authentication method. Do not weaken an account-wide authentication policy as a troubleshooting shortcut.

## Decision Points

| Finding | Primary Action |
|---|---|
| Wrong account | Correct client/account configuration |
| Wrong `LOGIN_NAME` | Correct client identity |
| Fingerprint mismatch | Investigate secret/key/rotation state |
| Invalid signature | Verify key pairing/JWT construction |
| Invalid algorithm | Correct JWT implementation |
| Invalid issue time | Check clock/load/network delay |
| Invalid expiration | Correct JWT generation/lifetime |
| Named key expired | Approved replacement/rotation |
| Named key disabled | Determine reason before enabling/replacing |
| Role restriction mismatch | Correct approved role configuration |
| Authentication-policy restriction | Policy/change investigation |
| One replica stale | Fix runtime/secret drift; do not rotate globally |
| Private key compromised | Security incident |
| Legacy key mismatch | Staged dual-slot recovery |
| Named-key mismatch | Named-key lifecycle recovery |

## Remediation

### Named-Key Registration

For an approved named-key replacement where adding a key is appropriate:

```sql
ALTER USER "<username>"
ADD KEY PAIR <key_pair_name>
PUBLIC_KEY = '<public-key>';
```

Inspect inventory first:

```sql
SHOW USER KEY PAIRS FOR USER "<username>";
```

Use a staged lifecycle: preserve the known-good key, register/rotate the replacement, securely deploy the matching private key, validate a controlled workload, validate all required consumers, and retire the previous key only when safe.

Do not confuse temporary disablement with permanent removal. Use the operation matching the authorized objective.

After replacement validation and authorization:

```sql
ALTER USER "<username>"
REMOVE KEY PAIR <obsolete_key_pair_name>;
```

Remove only after the replacement and all required consumers are validated and no rollback dependency remains.

### Legacy RSA Rotation

For a legacy deployment with slot 1 established, register the new public key in the unused slot:

```sql
ALTER USER "<username>"
SET RSA_PUBLIC_KEY_2 = '<new-public-key>';
```

Deploy the corresponding new private key and validate the workload and all consumers. Only then retire the old slot:

```sql
ALTER USER "<username>"
UNSET RSA_PUBLIC_KEY;
```

If slot 2 is the established key, use the reverse-slot strategy. Inspect first; never mechanically assume slot 1 is old.

Do not combine incident recovery with an unplanned migration from legacy RSA slots to named key pairs.

### Stale Client/Runtime

If Snowflake has the approved current public key but the workload uses an obsolete private key, do not modify Snowflake. Correct the secret/deployment, reload or restart as required, and validate.

If the workload has the approved current private credential but Snowflake lacks the corresponding public key, verify authorization, register the replacement safely while preserving a working key where possible, validate, and then retire the obsolete key.

If neither side matches approved inventory, stop and investigate failed rotation, wrong environment/secret, configuration drift, unauthorized change, or compromise. Do not guess which key should become authoritative.

### Lost or Compromised Private Key

Snowflake cannot recover a workload private key from its public key. If the approved private key is permanently lost and compromise is not suspected, generate an approved replacement pair, store the private key securely, register the public key using staged rotation, deploy, validate, and retire the obsolete public key.

If compromise is suspected, follow the security incident path. Do not use the compromised key as normal rollback.

## Validation

Administrative inspection does not prove authentication works. Validate the actual application using the approved runtime secret, supported connector, expected Snowflake endpoint, and expected identity.

Where safe:

```sql
SELECT
    CURRENT_USER(),
    CURRENT_ROLE(),
    CURRENT_WAREHOUSE();
```

For shared identities, validate every required consumer/replica before retiring the previous key.

Before closure confirm:

- [ ] Authentication failures stopped.
- [ ] Retry storm stopped.
- [ ] Expected consumers authenticate.
- [ ] Required replicas are healthy.
- [ ] No stale secret consumers remain.
- [ ] No unexpected source IP or unexplained successful authentication exists.
- [ ] Production processing resumed.
- [ ] Previous-key disposition is known.

If authentication succeeds but role, warehouse, database, schema, or object privilege errors remain, key-pair authentication is no longer the failure domain. Route to the Roles, Grants & Permissions runbooks.

## Rollback

For ordinary non-compromise rotation, preserve KEY A while introducing KEY B. If KEY B fails, return the workload to KEY A and investigate KEY B. Do not remove KEY A until replacement validation is complete.

For a compromised KEY A, there is **no normal rollback to KEY A**. Security containment takes precedence.

## Escalation

| Condition | Escalation |
|---|---|
| Private-key exposure | Security |
| Unauthorized key change | Security / IAM |
| Service identity compromise | RB-081 |
| Emergency rotation | RB-082 |
| Secret-manager problem | Platform / Cloud / Security |
| Kubernetes secret/deployment issue | Platform / Application |
| Connector problem | Application / vendor support |
| JWT implementation | Application Engineering |
| Time synchronization | Platform / Cloud |
| Snowflake key/user configuration | Snowflake Admin |
| Authentication policy | IAM / Security / Snowflake Admin |
| Unknown Snowflake behavior | Snowflake Support |

## Evidence to Capture

```text
RUNBOOK: RB-005
Environment/account:
Region:
Snowflake NAME:
LOGIN_NAME:
TYPE:
Application/workload:
Owning team:
Known consumers:
Request/ticket:
Authentication mechanism:
Key-management model: NAMED / LEGACY
Connector/driver:
Connector version:
Account identifier:
Source IP:
Secret-management system:
Secret reference:
Secret version identifier:
Failure start:
Last successful authentication:
Exact error:
JWT failure UUID:
JWT failure detail/code:
Blast radius:
Production impact:
Recent deployment:
Recent key rotation:
Recent secret update:
Recent connector change:
Named key name/status/fingerprint/expiration/last-used/role restriction:
Legacy RSA_PUBLIC_KEY_FP:
Legacy RSA_PUBLIC_KEY_2_FP:
Expected client public fingerprint:
Fingerprint match:
Expected key version:
Observed runtime key version:
LOGIN_NAME verified:
Account identifier verified:
Private-key load successful:
Passphrase source valid:
JWT algorithm/timing verified:
Clock synchronization verified:
Host resource pressure:
Network latency concern:
Authentication policy checked:
Retry storm:
Retries contained:
Root cause:
Remediation:
Replacement key registered/deployed/validated:
Consumers validated:
Previous key retained/disabled/removed:
Rollback required:
Unexpected authentication:
Security escalation:
Administrator:
Administrative role:
Start timestamp:
Completion timestamp:
```

Never capture private keys, passphrases, signed JWTs, secret-manager plaintext, OAuth tokens, PAT secrets, passwords, session tokens, or cloud credentials.

## Quick Production Procedure

1. Capture exact error and JWT failure UUID.
2. Determine blast radius.
3. Identify workload owner and all known consumers.
4. Contain excessive retries where safe.
5. Verify Snowflake account/environment.
6. Verify `NAME`, `LOGIN_NAME`, and `TYPE`.
7. Confirm key-pair authentication is intended.
8. Determine NAMED vs LEGACY key model.
9. Inspect registered key state.
10. Retrieve JWT failure details when available.
11. Derive and compare public-key fingerprints.
12. Check key status, expiration, and role restriction.
13. Verify account identifier.
14. Verify client username against `LOGIN_NAME`.
15. Verify JWT algorithm/signature/timing.
16. Check clock, resource pressure, and network delay.
17. Verify private-key loading/passphrase/format.
18. Verify secret version and runtime deployment state.
19. Check effective authentication policy.
20. Identify root cause.
21. Correct configuration or perform approved staged rotation.
22. Validate the actual production workload.
23. Validate all required consumers/replicas.
24. Confirm authentication failures/retries stop.
25. Retire the previous key only when safe.
26. Capture evidence.
27. Close or escalate.

## Production Guardrails

**Always:** verify account and identity, verify `LOGIN_NAME`, identify workload ownership and blast radius, determine named vs legacy key model, inspect current key state, use public fingerprints, retrieve JWT failure details where available, distinguish secret-manager state from runtime state, preserve the known-good credential during ordinary rotation, validate every required consumer, contain excessive retries, and protect private-key material.

**Never:** ask someone to send a private key, paste private keys into troubleshooting channels, rotate solely because a client says `JWT invalid`, blindly overwrite `RSA_PUBLIC_KEY`, assume slot 1 is old and slot 2 is new, remove the known-good key before replacement validation, rotate globally because one pod fails, change a password to fix a key-pair problem, create a replacement service identity as a shortcut, weaken authentication policy to troubleshoot, combine incident recovery with an unplanned authentication migration, or use a compromised key as rollback.

## References

Primary technical authority for this runbook is current Snowflake documentation covering key-pair authentication and troubleshooting, named key-pair management, `SHOW USER KEY PAIRS`, `ALTER USER ... ADD KEY PAIR`, named-key lifecycle operations, `ALTER USER`, `DESCRIBE USER`, `RSA_PUBLIC_KEY` / `RSA_PUBLIC_KEY_2`, JWT authentication failure details, authentication policies, user/service identity types, and login history.

The canonical procedure intentionally supports both current named-key management and existing legacy RSA-slot deployments.

## Canonical Operating Model

`Diagnose → identify NAMED vs LEGACY → inspect key state → retrieve JWT failure details → compare public fingerprints → verify account/LOGIN_NAME/JWT/time/secret/runtime/role/policy → correct configuration or rotate safely → validate actual workload → validate every required consumer → retire previous key only when safe`
