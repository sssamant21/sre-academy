# Lab: Authentication and Network-Policy Diagnosis

Version: v1.1.0  
Status: Vendor-validated lab  
Last vendor validation: 2026-08-15

## Objective

Diagnose a hypothetical connection failure using redacted client evidence, Login History and effective network-policy metadata without modifying account access.

## Safety and prerequisites

- Duration: approximately 20–30 minutes.
- Cost risk: low, read-only metadata analysis.
- Required privileges: approved visibility into relevant login events and network-policy metadata.
- Do not collect passwords, private keys, OAuth tokens, MFA codes or full connection strings.
- Do not activate, detach or broaden a network policy in this lab.
- Snowflake recommends testing network rules with a user-level policy before account-level enforcement.

## Evidence worksheet

Record:

- UTC failure window;
- affected account identifier and region;
- client and version;
- redacted error code/message;
- affected identity;
- source network or private endpoint reference;
- whether other identities and networks succeed.

Query recent events:

```sql
SELECT
  EVENT_TIMESTAMP,
  EVENT_TYPE,
  USER_NAME,
  CLIENT_IP,
  REPORTED_CLIENT_TYPE,
  REPORTED_CLIENT_VERSION,
  IS_SUCCESS,
  ERROR_CODE,
  ERROR_MESSAGE,
  FIRST_AUTHENTICATION_FACTOR,
  SECOND_AUTHENTICATION_FACTOR
FROM TABLE(
  INFORMATION_SCHEMA.LOGIN_HISTORY(
    TIME_RANGE_START => DATEADD('hour', -4, CURRENT_TIMESTAMP()),
    RESULT_LIMIT => 1000
  )
)
ORDER BY EVENT_TIMESTAMP DESC;
```

Inspect effective policy parameters through an authorized administration role:

```sql
SHOW PARAMETERS LIKE 'NETWORK_POLICY' IN ACCOUNT;
SHOW PARAMETERS LIKE 'NETWORK_POLICY' IN USER <user_name>;
SHOW NETWORK POLICIES;
```

Use `RESULT_SCAN(LAST_QUERY_ID())` immediately after a `SHOW` command when structured filtering is needed.

## Decision exercise

Classify the failure:

- No login event: investigate DNS, proxy, firewall, endpoint and TLS path.
- Login event with network-policy rejection: evaluate the effective account, user or integration policy.
- Authentication-factor failure: follow the corresponding SSO, OAuth, key-pair or MFA procedure.
- Successful login followed by SQL denial: investigate roles and privileges, not connectivity.

Prepare a proposed user-level test plan, but do not apply it.

## Success criteria

- Evidence is bounded to a UTC window.
- Secrets are excluded.
- The failure is classified before any policy change.
- The proposed test avoids account-wide lockout risk.
- Rollback and break-glass ownership are identified.

## Cleanup

No objects or policies are changed.

## Official references

- [Common connectivity issues](https://docs.snowflake.com/en/user-guide/client-connectivity-troubleshooting/common-issues)
- [LOGIN_HISTORY functions](https://docs.snowflake.com/en/sql-reference/functions/login_history)
- [Network policies](https://docs.snowflake.com/en/user-guide/network-policies)
- [Network rules](https://docs.snowflake.com/en/user-guide/network-rules)
