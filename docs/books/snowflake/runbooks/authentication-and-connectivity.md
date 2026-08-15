# Runbook: Authentication and Connectivity Failure

Version: v1.1.0  
Status: Vendor-validated runbook  
Last vendor validation: 2026-08-15

## Trigger

Use when users, services or clients cannot authenticate or establish a supported connection to Snowflake.

## Safety

Never request passwords, private keys, OAuth tokens, MFA codes or full connection strings in tickets or chat. Preserve redacted client errors, timestamps, account identifier, region, client type and source network evidence.

## Triage boundary

Determine whether the failure affects one identity, one client, one source network or the entire account. Separate DNS, proxy, TLS, private-connectivity, network-policy, SSO, OAuth, key-pair, MFA and authorization failures.

## Evidence

When an authorized session is available, use a bounded login history query:

```sql
SELECT
  EVENT_TIMESTAMP,
  EVENT_TYPE,
  USER_NAME,
  CLIENT_IP,
  REPORTED_CLIENT_TYPE,
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

Redact IP addresses when the incident audience does not require them. Compare client and IdP timestamps in UTC.

## Decision points

- No Snowflake login event: investigate DNS, proxy, firewall, endpoint and TLS before changing identity settings.
- Network-policy rejection: verify the effective account and user policies and approved network rules.
- SSO or OAuth error: use the documented provider-specific error and integration evidence.
- Key-pair failure: verify username, active public key, rotation state and client configuration without exposing private material.
- Successful authentication but SQL denied: follow authorization and role investigation rather than connectivity remediation.

## Mitigation

Prefer a tested user-level network-policy change before account-wide policy changes. Use break-glass access only under the approved security procedure. Apply one change, record it and validate from the affected path.

## Official references

- [Common connectivity issues](https://docs.snowflake.com/en/user-guide/client-connectivity-troubleshooting/common-issues)
- [LOGIN_HISTORY functions](https://docs.snowflake.com/en/sql-reference/functions/login_history)
- [Network policies](https://docs.snowflake.com/en/user-guide/network-policies)
- [Federated authentication troubleshooting](https://docs.snowflake.com/en/user-guide/errors-saml)
