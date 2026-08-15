# Facilitator Guide: Dynamic-Table Freshness Breach

Version: v1.2.0  
Status: Vendor-validated facilitator guide  
Last vendor validation: 2026-08-15

## Expected diagnosis

The downstream `UPSTREAM_FAILED` state is a symptom. The first upstream refresh fails after a column rename. Target lag and warehouse size are not the primary cause.

## Strong response

1. Map connected dependencies and locate the first failed refresh.
2. Correlate the schema error with the deployment.
3. Choose rollback to the compatible schema or a tested forward correction.
4. Avoid recreation and unnecessary reinitialization.
5. Validate successful refreshes across at least two expected cycles.
6. Check data timestamp, correctness, cost, downstream consumers and streams.

## Common mistakes

- Recreating the downstream table first.
- Increasing warehouse size for a schema incompatibility.
- Treating target lag as a guaranteed interval.
- Ignoring reinitialization effects on streams.
- Closing after one successful refresh.

## Example corrective actions

- Add dependency-aware schema compatibility checks.
- Coordinate upstream DDL with dynamic-table lifecycle procedures.
- Alert on actual freshness and first upstream failure.
- Include downstream stream behavior in change review.

## Official references

- [Troubleshoot dynamic table refreshes](https://docs.snowflake.com/en/user-guide/dynamic-tables/troubleshoot-refreshes)
- [Monitor dynamic tables](https://docs.snowflake.com/en/user-guide/dynamic-tables/monitoring)
