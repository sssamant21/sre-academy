# Facilitator Guide: Unexpected Credit Spike

Version: v1.2.0  
Status: Vendor-validated facilitator guide  
Last vendor validation: 2026-08-15

## Expected diagnosis

A deployment introduced overlapping schedules that submit duplicate batch work. The batch warehouse drives the variance; the interactive warehouse is not the containment target.

## Strong response

1. Establish baseline, variance, warehouse attribution and telemetry latency.
2. Correlate the spike with task and deployment history.
3. Pause the duplicate non-critical submission path with owner approval.
4. Preserve the required batch run.
5. Verify current activity through an appropriate near-real-time surface while Account Usage catches up.
6. Correct scheduling tests and review warehouse guardrails.

## Common mistakes

- Suspending all warehouses.
- Treating delayed Account Usage as real-time enforcement.
- Assuming resource monitors cover serverless and AI services.
- Reporting savings before metering confirms them.
- Omitting the business owner from containment.

## Example communication

“FinOps detected a fivefold hourly variance concentrated in the batch warehouse. Duplicate schedules introduced by the latest deployment are the leading cause. The workload owner approved pausing the duplicate path; interactive services remain unchanged. Current activity and delayed metering will be reconciled before closure.”

## Official references

- [Resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [WAREHOUSE_METERING_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history)
