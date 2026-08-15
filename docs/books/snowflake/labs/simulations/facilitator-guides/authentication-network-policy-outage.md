# Facilitator Guide: Authentication and Network-Policy Outage

Version: v1.2.0  
Status: Vendor-validated facilitator guide  
Last vendor validation: 2026-08-15

## Expected diagnosis

The scope and timing point to an effective network-policy rule that excludes the approved private endpoint. Other networks succeed, and Snowflake records failed login attempts for the service client.

## Strong response

1. Protect secrets and collect redacted client, timestamp and network evidence.
2. Compare the affected path with a successful path.
3. Review effective account, user and integration policies.
4. Test the correction with the narrowest approved user-level policy.
5. Preserve break-glass access and a rollback owner.
6. Validate from the affected private path before broader promotion.

## Common mistakes

- Detaching the account policy during diagnosis.
- Requesting passwords, tokens or private keys.
- Treating successful authentication as proof of SQL authorization.
- Testing only from the corporate network.
- Ignoring integration-level policy behavior for OAuth.

## Example communication

“Private-path service connections are failing while corporate interactive access remains healthy. Login and change evidence point to a network-policy rule introduced before impact. No credentials are being collected. Security is preparing a narrow user-level validation with documented rollback before any broader policy change.”

## Official references

- [Network policies](https://docs.snowflake.com/en/user-guide/network-policies)
- [LOGIN_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/login_history)
