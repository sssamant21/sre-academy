# RB-007 — Network Policy Blocking Access

**Snowflake DBRE/SRE Production Runbook**  
**Runbook ID:** RB-007  
**Category:** Access & Authentication  
**Edition:** Revised Final / Canonical  
**Risk:** High  
**Primary Operator:** DBRE / SRE / Snowflake Administrator  
**Supporting Teams:** Security / Network / Cloud Platform / IAM / Application Owner

> **Core principle:** Prove that Snowflake network-policy enforcement is the failing control, identify the effective policy and actual source network identity, and verify the intended security boundary before modifying production access.

## 1. Purpose

Use RB-007 to diagnose and safely recover Snowflake access failures involving account-, user-, and security-integration-level network policies; network rules; legacy IP allow/block lists; IPv4/IPv6; AWS PrivateLink; Azure Private Link; Google Cloud Private Service Connect; NAT/VPN/proxy/firewall/VDI/Citrix/cloud egress; Kubernetes egress; internal-stage controls; and network-policy precedence.

This runbook does **not** assume every connection failure is caused by a Snowflake network policy.

## 2. Trigger / Alert

Use when Snowflake reports network-policy/IP rejection, access works from one network but not another, one user is blocked while peers succeed, a VPN/office/application population fails after an egress change, OAuth client traffic is selectively blocked, private connectivity fails, IPv4 and IPv6 behave differently, or internal-stage access is blocked by network controls.

If the cause has not been narrowed to network controls, begin with **RB-003 — Troubleshoot Login / Authentication Failure**.

## 3. Impact and Severity

Potential impact ranges from a single user through application, BI, ETL/ELT, VPN/office, OAuth, cloud workload, private-connectivity, internal-stage, administrator, or account-wide outage. Treat administrator or account-wide loss as Critical and unauthorized policy changes or untrusted source requests as Security incidents/reviews.

## 4. Mandatory Production STOP Gate

Before changing any network policy or network rule:

```text
[ ] Correct Snowflake account/environment confirmed
[ ] Exact affected user/application identified
[ ] Exact error captured
[ ] Snowflake reachability established
[ ] Blast radius and last known good established
[ ] Authentication/client path identified
[ ] USER / ACCOUNT / INTEGRATION scope evaluated
[ ] Effective network policy identified and inspected
[ ] Relevant network rules and database/schema identified
[ ] Rule MODE and TYPE understood
[ ] Actual source/network identifier established
[ ] IPv4 / IPv6 / private-connectivity path established
[ ] Allow/block and private-connectivity precedence evaluated
[ ] Shared network-rule consumers identified
[ ] Recent policy/network changes reviewed
[ ] Existing sessions considered
[ ] Administrative recovery access preserved
[ ] Current configuration captured
[ ] Command mutation semantics understood
[ ] Proposed change authorized
[ ] Rollback understood
```

If the effective policy, source identity, or security intent remains unknown: **STOP. Do not widen production access.**

## 5. Security STOP

Stop routine recovery if Security intentionally blocked the source, source ownership cannot be established, unauthorized policy modification is suspected, an unexpected source requests access, containment would be bypassed, broad Internet access is required, or an approved private path is unexpectedly bypassed.

A correctly blocked connection is not a failure of the security control.

## 6. Required Access and Evidence Safety

Use least privilege across Snowflake Administration, Security, Network Engineering, Cloud Platform, IAM, and Application Engineering. Do not default every incident to `ACCOUNTADMIN`.

Never capture passwords, temporary passwords, private keys, OAuth tokens, client secrets, session tokens, MFA secrets/codes, cloud credentials, VPN credentials, or proxy credentials.

## 7. Verify Administrative Context

```sql
SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_USER();
```

Confirm the intended account before changing security controls.

## 8. Capture Failure and Blast Radius

Classify the exact failure as explicit network-policy rejection, IP/network source denial, authentication rejection, DNS/TCP/TLS/proxy/private-endpoint failure, or SSO/OAuth failure.

Classify blast radius: ONE USER, APPLICATION, HOST, POD, NODE, SUBNET, OFFICE, VPN, NAT GATEWAY, CLOUD REGION, OAUTH CLIENT, ALL USERS, or ALL APPLICATIONS.

One user failing while peers from the same source work raises user-policy suspicion; many users from one network raises shared egress/policy suspicion; one OAuth client raises integration-policy suspicion; everyone failing raises account/shared-control suspicion.

## 9. Establish Last Known Good

Capture last successful connection, first failure, and recent policy, rule, user/integration assignment, NAT, VPN/proxy/firewall, cloud network, private-connectivity, and application changes. Use `LAST KNOWN GOOD → CHANGE → FIRST FAILURE` as correlation, not automatic proof of causation.

## 10. Verify User State

```sql
SHOW USERS LIKE '<username>';
DESC USER "<username>";
```

Confirm `NAME`, `LOGIN_NAME`, `TYPE`, `DISABLED`, and `NETWORK_POLICY`. Route disabled/locked users to RB-002 where appropriate.

## 11. Determine Effective Policy Scope

Evaluate `USER`, `ACCOUNT`, and `SECURITY INTEGRATION` scope. For ordinary user authentication, a user-level policy takes precedence when assigned; otherwise evaluate account scope. For applicable OAuth/client traffic, integration-level policy can govern the request.

For Snowflake OAuth distinguish browser/user authorization from OAuth client token/query traffic. Browser authorization follows the user/account path, while applicable client traffic follows integration/account policy. Verify current documented precedence for local-application OAuth rather than assuming the generic model.

## 12. Discover and Inspect Policies

```sql
SHOW NETWORK POLICIES;
DESC NETWORK POLICY <policy_name>;
```

Where privileges permit:

```sql
SELECT *
FROM TABLE(
    INFORMATION_SCHEMA.POLICY_REFERENCES(
        POLICY_NAME => '<policy_name>',
        POLICY_KIND => 'NETWORK_POLICY'
    )
);
```

Use references to establish ACCOUNT, USER, and INTEGRATION associations. Insufficient visibility is not proof that no association exists.

## 13. Preferred and Legacy Models

Preferred production model: `NETWORK RULE → NETWORK POLICY`. Legacy compatibility uses `ALLOWED_IP_LIST` and `BLOCKED_IP_LIST`. Diagnose legacy configurations when present, but do not turn an active incident into an unplanned migration.

## 14. Discover and Inspect Network Rules

```sql
SHOW NETWORK RULES;
DESC NETWORK RULE <rule_name>;
```

Confirm database, schema, name, `MODE`, `TYPE`, and `VALUE_LIST`. Network rules are schema-level objects; establish the fully qualified object before modifying it.

For ordinary inbound service access investigate `MODE = INGRESS`. Do not confuse `EGRESS` or `INTERNAL_STAGE` rules with normal login controls.

Relevant inbound identities include `IPV4`, `IPV6`, `AWSVPCEID`, `AZURELINKID`, and `GCPPSCID`, subject to current Snowflake support for the applicable mode/deployment.

## 15. IPv4, IPv6, Dual Stack, and Private Connectivity

Explicitly determine whether the path is IPv4, IPv6, dual stack, or private connectivity. Dual-stack failures can appear intermittent when one family passes and the other is blocked. Legacy IP-list controls must not be assumed to cover IPv6.

For private connectivity, evaluate the private endpoint/network identity where applicable. Do not assume public IP rules decide a private request. If an approved private workload suddenly exits via public NAT, investigate DNS/routing/private endpoint failure instead of immediately allowlisting the public address.

## 16. Determine Actual Source Identity

Never assume local host or pod IP is what Snowflake evaluates. Trace application → pod/VM → subnet → firewall → NAT/proxy/VPN → Snowflake, or the private endpoint path. Determine the actual identity presented to Snowflake.

## 17. Login History

Known user:

```sql
SELECT EVENT_TIMESTAMP, USER_NAME, CLIENT_IP,
       REPORTED_CLIENT_TYPE, REPORTED_CLIENT_VERSION,
       IS_SUCCESS, ERROR_CODE, ERROR_MESSAGE
FROM TABLE(
    INFORMATION_SCHEMA.LOGIN_HISTORY(
        TIME_RANGE_START => DATEADD('hour', -1, CURRENT_TIMESTAMP()),
        RESULT_LIMIT => 1000
    )
)
WHERE USER_NAME = '<username>'
ORDER BY EVENT_TIMESTAMP DESC;
```

Some failures can occur before Snowflake resolves the username. For deeper correlation remove the username predicate and correlate timestamp, `CLIENT_IP`, client type, and error.

Historical evidence:

```sql
SELECT EVENT_TIMESTAMP, USER_NAME, CLIENT_IP,
       REPORTED_CLIENT_TYPE, REPORTED_CLIENT_VERSION,
       IS_SUCCESS, ERROR_CODE, ERROR_MESSAGE
FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
WHERE USER_NAME = '<username>'
ORDER BY EVENT_TIMESTAMP DESC
LIMIT 100;
```

Account Usage can lag; use current-state commands/views for active decisions.

Never interpret `CLIENT_IP = 0.0.0.0` as an instruction to allowlist `0.0.0.0`; investigate Snowflake-internal/client origin behavior.

## 18. Allow/Block and Private Precedence

Always inspect both allowed and blocked configuration. A source appearing in an allowed rule/list can still be blocked by blocked configuration. For private requests, evaluate applicable private endpoint identity/rules rather than assuming public IP controls decide the request.

## 19. Shared Rule Dependency Gate

Before modifying a network rule:

```text
[ ] Rule fully identified
[ ] Policy references identified
[ ] Integration dependencies identified
[ ] Consumers identified
[ ] Blast radius understood
```

Use current metadata and `SNOWFLAKE.ACCOUNT_USAGE.NETWORK_RULE_REFERENCES` where appropriate. Never treat a reusable rule as dedicated until proven.

## 20. Historical Policy/Rule Evidence

Use `SHOW`/`DESC` for current state and Account Usage metadata for historical timeline, including recent policy/rule alteration or deletion. Do not use delayed historical metadata as the sole authority during an active outage.

## 21. Common Source Change Pattern

A common incident is application works → NAT/proxy/VPN changes → source identity changes → Snowflake still permits old source → application fails. Verify that the new source is expected, approved, stable, and owned by the correct environment before changing Snowflake.

For Kubernetes capture namespace, workload, pod, node, subnet/AZ, NAT, firewall/proxy, expected egress, and observed `CLIENT_IP`. If only some replicas fail, compare placement/path before changing account policy.

For corporate VPN/VDI/Citrix, do not allowlist employee home addresses as a substitute for repairing the approved corporate path.

For AWS/Azure/GCP, inspect VPC/VNet, subnet, route, NAT, firewall, proxy, private endpoint, DNS, and expected egress.

## 22. Prove Snowflake Is Reached

An explicit Snowflake network rejection makes RB-007 likely applicable. If TCP never reaches Snowflake, investigate DNS/routing/firewall/proxy. For TLS failure investigate TLS/proxy/certificate path. If network policy passes but authentication fails, route to the appropriate authentication runbook.

Where approved:

```bash
nslookup <account-hostname>
dig <account-hostname>
curl -I https://<account-hostname>
```

`curl` is reachability evidence only; success does not prove authentication and failure does not prove a Snowflake policy rejection. Do not hard-code resolved Snowflake IPs as an application workaround.

For approved/current Snowflake CLI installations:

```bash
snow connection test -c <connection_name>
snow connection test -c <connection_name> --enable-diag
```

Use `--print-diag` only where supported and appropriate. Review diagnostic output for sensitive environment/network metadata before sharing. Do not use SnowCD as the primary current diagnostic path.

## 23. Decision Points

**Is network policy responsible?** If Snowflake is not reached, diagnose the network path. If reached but no policy rejection is confirmed, continue authentication/connectivity diagnosis. If a policy rejection is confirmed, determine whether the source is expected and approved; unapproved sources go to Security/Network review, approved sources proceed to drift/change analysis.

**User/account/integration?** One user failing while peers work points toward USER policy. Multiple ordinary users can point toward ACCOUNT/shared controls. OAuth client-only failure raises INTEGRATION/client policy.

**Old vs new identity?** If last success was Source A and failure is Source B, establish whether B is an approved, stable production source and whether A should be retired.

## 24. Critical `ALTER ... SET` Warning

Never assume `SET <list> = ('new-value')` means append. A `SET` operation can replace the existing list.

> **Capture the complete current list before any list-replacement operation and construct the intended full post-change state—not merely the new entry.**

Do not make recovery dependent on Preview/cloud-specific additive/removal syntax. Verify current release, cloud/account support, production approval, and exact semantics before using such functionality.

## 25. High-Risk Account Policy Changes

Account-level policy activation/replacement can affect users, administrators, applications, automation, BI tools, pipelines, and existing sessions. Do not switch the active account policy merely to test a theory.

Do not assume only new logins are affected; consider existing interactive/application sessions, scheduled jobs, and administrators.

Never activate an empty restrictive policy. Verify administrator, critical workload, user, IPv4/IPv6, private-connectivity, and OAuth paths first.

## 26. Broad Access and CIDR Guardrails

Do not use `0.0.0.0/0` as routine recovery. As an allowed range it defeats meaningful IPv4 allowlisting; careless broad blocking can also cause lockout. Use the smallest operationally correct authorized source range.

Do not allow large CIDRs because the operator is uncertain. Validate the exact IP/range/private identifier with Network/Security.

Repeated emergency allowlist changes caused by dynamic egress indicate an architecture problem. Post-incident remediation should consider stable NAT, controlled proxy, private connectivity, or another stable egress design.

## 27. Internal Stage Access

Successful SQL authentication does not exclude network controls from an internal-stage incident. Investigate applicable `MODE = INTERNAL_STAGE` rules/policy design when stage access fails.

## 28. Minimum-Change Remediation

Use: inspect actual state → prove exact mismatch → verify approved desired state → identify dependencies → capture rollback → apply minimum change → controlled validation.

Do not combine unrelated cleanup or architecture migration with active incident recovery.

If an approved production source is genuinely absent, verify ownership, identity, environment, stability, effective policy, dependencies, current state, and authorization; then apply the minimum change, validate original workload and existing consumers, validate the security boundary, and separately retire obsolete entries when safe.

For an incorrect user policy, verify intended policy and authorization, correct assignment, validate the original path, and validate expected restrictions.

For a stale shared rule, identify all consumers, confirm replacement, capture state, apply the minimum correction, validate all consumers, then retire obsolete values when safe.

For private connectivity, verify DNS → private endpoint → routing → cloud endpoint identity → Snowflake private rule → policy before creating any public exception.

## 29. Controlled Validation

For shared user changes validate a controlled user, then a representative second user, then broader population. For application changes validate a controlled instance, then a representative instance, then restore normal workload. Avoid retry storms.

The original user/application + original network + expected network identity + original authentication path must succeed. Administrator connectivity from a different network is not proof of recovery.

Where safe:

```sql
SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE();
```

Do not perform production writes solely to validate connectivity.

Successful recovery requires both: expected source works **and** unauthorized/unexpected source remains blocked. Perform negative-path validation only when safe and approved.

After shared changes validate the original source, representative existing sources, administrator access, OAuth clients, VPN/office users, cloud workloads, private connectivity, IPv4/IPv6 where applicable, and internal-stage access where applicable.

## 30. Stability Gate

```text
[ ] Root cause identified
[ ] Effective policy documented
[ ] Actual network identity documented
[ ] Expected access restored
[ ] Unauthorized sources remain blocked
[ ] Original path validated
[ ] Existing consumers validated
[ ] Existing sessions considered
[ ] No broad temporary access remains
[ ] No stale emergency entry remains
[ ] Administrative access preserved
[ ] Retry failures stopped
[ ] Evidence captured
[ ] Architectural follow-up recorded
```

## 31. Rollback

For ordinary configuration failure, restore the captured known-good state and validate both expected access and the security boundary.

Never roll back to an unauthorized/compromised source, known-bad broad CIDR, Security-blocked endpoint, or obsolete insecure path merely because it previously worked. Escalate to Security.

## 32. Abort Conditions

Stop routine remediation if account/environment is uncertain; effective policy/source identity/source ownership/rule dependencies/policy ownership cannot be established; Security intentionally blocked the source; unauthorized changes are suspected; broad Internet access is required; administrative recovery could be lost; private-connectivity or dual-stack behavior is unclear; current configuration or mutation semantics cannot be safely established; rollback is unavailable; or the operator lacks authorization.

Escalate rather than experiment.

## 33. Escalation

- Network policy/rule → Snowflake Admin / Security
- Corporate NAT/VPN or proxy/SWG → Network / Security
- AWS/Azure/GCP network/private connectivity → Cloud Platform
- Kubernetes egress → Platform / Network
- Unauthorized change or suspicious source → Security
- MFA → RB-004
- Key-pair auth → RB-005
- SSO/OAuth auth → RB-006
- Emergency access → RB-008
- Authorization → RB-009/RB-010
- Snowflake service issue → RB-083
- Support evidence/escalation → RB-088/RB-089

## 34. Evidence to Capture

```text
RUNBOOK: RB-007
Environment/account:
Region:
Incident/ticket:
Affected user/application:
LOGIN_NAME:
TYPE:
Authentication/client path:
Exact error / error code:
Failure start / last success:
Production impact / blast radius:
Snowflake reached:
Observed and previous CLIENT_IP:
Network model: IPv4 / IPv6 / Dual Stack / Private
Expected IP/CIDR / AWS VPCE / Azure Link ID / GCP PSC ID:
Source owner/environment:
Host/pod/node/subnet/AZ/NAT/VPN/proxy/firewall/private endpoint/expected egress:
Policy scope: USER / ACCOUNT / INTEGRATION
Effective network policy / owner / references:
Allowed and blocked network rules:
Legacy allowed/blocked IP lists:
Network rule database/schema/MODE/TYPE/VALUE_LIST:
Rule consumers/references:
Recent policy/rule/user/integration/network/private-connectivity changes:
Existing sessions considered:
Administrative access preserved:
Root cause / approved desired state / remediation / approval / rollback:
Original path validated:
Expected source validated:
Security boundary validated:
Existing consumers validated:
Temporary access removed:
Architecture follow-up:
Operator / administrative role / Network / Security / application owners:
Start/completion timestamp:
```

## 35. Quick Production Procedure

1. Capture exact failure and verify account/environment.
2. Identify affected user/application, blast radius, and last known good.
3. Determine client/authentication path and confirm Snowflake reachability.
4. Determine actual source identity and IPv4/IPv6/private path.
5. Inspect login history, including unresolved-user failures when needed.
6. Determine USER/ACCOUNT/INTEGRATION scope and effective policy.
7. `SHOW NETWORK POLICIES`; `DESC NETWORK POLICY`.
8. Inspect `POLICY_REFERENCES` where appropriate.
9. Identify allowed/blocked rules; `SHOW`/`DESC` relevant network rules.
10. Confirm database/schema/MODE/TYPE/VALUE_LIST and shared consumers.
11. Check blocked and private-connectivity precedence.
12. Review recent policy/rule/network changes.
13. Verify source ownership and intended security design.
14. Preserve administrative access and capture complete current state.
15. Verify command replacement/additive semantics.
16. Apply minimum authorized correction.
17. Validate the ORIGINAL path and expected network identity.
18. Validate existing consumers and intended security boundary.
19. Confirm failures/retries stop and remove temporary access.
20. Capture evidence, record architectural follow-up, close or escalate.

## 36. Production Guardrails

**Always:** prove Snowflake is reached and policy is involved; establish blast radius; identify USER/ACCOUNT/INTEGRATION scope; inspect actual policy/rules; identify actual source identity; distinguish IPv4/IPv6/private connectivity; inspect allowed and blocked controls; identify shared dependencies; preserve administrative access; capture state before mutation; understand replacement semantics; apply minimum change; validate original path, consumers, and security boundary.

**Never:** whitelist an unverified source; assume every failure is network policy; assume pod/local IP is Snowflake's source; use `0.0.0.0/0` as routine recovery; weaken controls merely to test; bypass Security containment; modify account policy for a user-only problem; edit shared rules without dependency analysis; assume `SET` means append; activate an empty restrictive policy; unnecessarily migrate architecture during an incident; allow home IPs to bypass approved VPN design; create public access because private connectivity failed; allowlist `CLIENT_IP = 0.0.0.0`; validate only from an administrator workstation; or leave temporary emergency access indefinitely.

## 37. References

Primary technical authority is current Snowflake documentation:

- Network policies: https://docs.snowflake.com/en/user-guide/network-policies
- Network rules: https://docs.snowflake.com/en/user-guide/network-rules
- CREATE NETWORK POLICY: https://docs.snowflake.com/en/sql-reference/sql/create-network-policy
- ALTER NETWORK POLICY: https://docs.snowflake.com/en/sql-reference/sql/alter-network-policy
- DESCRIBE NETWORK POLICY: https://docs.snowflake.com/en/sql-reference/sql/desc-network-policy
- CREATE NETWORK RULE: https://docs.snowflake.com/en/sql-reference/sql/create-network-rule
- POLICY_REFERENCES: https://docs.snowflake.com/en/sql-reference/functions/policy_references
- NETWORK_RULE_REFERENCES: https://docs.snowflake.com/en/sql-reference/account-usage/network_rule_references
- Snowflake OAuth overview: https://docs.snowflake.com/en/user-guide/oauth-snowflake-overview
- Client connectivity troubleshooting: https://docs.snowflake.com/en/user-guide/client-connectivity-troubleshooting/snowflake-tools
- Network Policy Advisor: https://docs.snowflake.com/en/user-guide/network-policy-advisor

## 38. Canonical Operating Model

```text
Connection failure
       ↓
Prove Snowflake is reached
       ↓
Prove network policy is involved
       ↓
Determine USER / ACCOUNT / INTEGRATION scope
       ↓
Identify effective policy and rules
       ↓
Determine actual IPv4 / IPv6 / private identity
       ↓
Check allow/block/private precedence
       ↓
Verify source ownership and security intent
       ↓
Identify shared dependencies
       ↓
Preserve administrative access and capture state
       ↓
Apply minimum authorized correction
       ↓
Validate ORIGINAL path and existing consumers
       ↓
Validate security boundary
       ↓
Close or escalate
```

> A successful connection alone is not sufficient evidence of successful remediation. The expected source must work while unauthorized network paths remain blocked.
