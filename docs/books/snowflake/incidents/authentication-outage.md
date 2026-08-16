# Case Study: Authentication and Network-Policy Outage

Version: v1.5.0
Status: In development
Last vendor validation: 2026-08-16

Fictional composite; identities, addresses and times are illustrative.

## Incident

BI users and scheduled workloads began receiving authentication failures after a network-policy deployment. Snowsight access from the administrator network still worked, but traffic from the application NAT range failed.

```sql
SELECT EVENT_TIMESTAMP, USER_NAME, CLIENT_TYPE,
       IS_SUCCESS, ERROR_CODE, ERROR_MESSAGE,
       REPORTED_CLIENT_TYPE, REPORTED_CLIENT_VERSION
FROM TABLE(INFORMATION_SCHEMA.LOGIN_HISTORY(
  TIME_RANGE_START => DATEADD('hour', -2, CURRENT_TIMESTAMP())))
ORDER BY EVENT_TIMESTAMP DESC;
```

Login history showed failures began at the policy change and affected clients originating from a newly introduced NAT range. IdP logs showed successful assertions, excluding SAML generation as the primary failure. The applied network rule contained the old egress CIDR only.

## Root cause and recovery

Root cause: infrastructure changed the application egress range without updating and testing the Snowflake network rule. Contributors were separate ownership of network and identity configuration, no synthetic login from each approved path, and an untested break-glass procedure.

An emergency administrator used the separately controlled path to add the validated new range while retaining the old range during transition. Teams verified successful and deliberately blocked origins before removing the obsolete CIDR.

## Preventive actions

- Treat egress ranges, network rules and applied policies as one versioned contract.
- Run synthetic authentication from every critical client path.
- Alert on failure rate by error code, user type and client—not only total failures.
- Maintain two tested break-glass administrators outside the normal IdP/network failure domain.
- Canary account- or user-level policy changes before broad application.
- Never disable MFA as a general outage workaround.

## Official references

- [`LOGIN_HISTORY`](https://docs.snowflake.com/en/sql-reference/functions/login_history)
- [Network policies](https://docs.snowflake.com/en/user-guide/network-policies)
- [Authentication policies](https://docs.snowflake.com/en/user-guide/authentication-policies)
- [SAML troubleshooting](https://docs.snowflake.com/en/user-guide/errors-saml)
