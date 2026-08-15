# Simulation: Authentication and Network-Policy Outage

Version: v1.2.0  
Status: Vendor-validated simulation  
Last vendor validation: 2026-08-15

## Objective

Classify an access outage without exposing secrets or creating a broader lockout.

## Scenario

A service using private connectivity cannot authenticate after a security change. Interactive users from a different network continue to connect.

## Safety

This simulation must not activate or detach an account-wide policy. Never collect credentials, tokens, private keys, MFA codes or complete connection strings.

## Facilitator injects

| Time | Inject |
|---|---|
| T+0 | One service reports connection failures |
| T+5 | Interactive users from the corporate network succeed |
| T+10 | Login History contains failed events for the service client |
| T+15 | A network-policy change occurred 15 minutes before impact |
| T+20 | The approved private endpoint identifier is absent from the candidate rule |
| T+25 | A tested user-level policy can be used before any broader change |

## Evidence participants must request

```sql
SELECT
  EVENT_TIMESTAMP,
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

Request redacted client errors, UTC timestamps, effective user/account/integration policies, network rules, change record and private-connectivity evidence.

## Decisions

1. Distinguish network-policy rejection from DNS, TLS, SSO and authorization.
2. Identify the narrowest safe test.
3. Preserve break-glass access and rollback.
4. Define validation from the affected network path.
5. Decide when Snowflake Support or the identity/network team must join.

## Success criteria

- No secret is requested or transmitted.
- Account-wide policy changes are avoided during diagnosis.
- The policy test is narrow, time-bound and reversible.
- Successful authentication is distinguished from SQL authorization.

## Official references

- [Network policies](https://docs.snowflake.com/en/user-guide/network-policies)
- [Network rules](https://docs.snowflake.com/en/user-guide/network-rules)
- [LOGIN_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/login_history)
- [Common connectivity issues](https://docs.snowflake.com/en/user-guide/client-connectivity-troubleshooting/common-issues)
