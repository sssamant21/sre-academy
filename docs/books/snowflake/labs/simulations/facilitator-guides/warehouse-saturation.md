# Facilitator Guide: Warehouse Saturation

Version: v1.2.0  
Status: Vendor-validated facilitator guide  
Last vendor validation: 2026-08-15

## Expected diagnosis

The interactive and batch workloads share a saturated warehouse. Elevated `AVG_QUEUED_LOAD`, with low provisioning and blocked load, supports overload queueing rather than resume latency or transaction locking.

## Strong response

1. Capture the UTC window, warehouse, query IDs, tags and owners.
2. Confirm the batch burst aligns with the SLO breach.
3. Pause the approved non-critical batch path.
4. Observe queue and application latency across multiple intervals.
5. Roll back the pause if critical processing risk exceeds the incident decision.
6. Create follow-up work for workload isolation and capacity/cost testing.

A temporary resize is defensible only with explicit cost authority, expiry and rollback. A permanent resize is premature.

## Common mistakes

- Resizing before separating overload, provisioning and blocking.
- Cancelling queries without business ownership.
- Using one interval as proof of steady-state capacity.
- Ignoring the shared-warehouse design cause.
- Closing when queueing falls but the application remains degraded.

## Example communication

“Since 14:00 UTC, interactive latency has exceeded its SLO. Evidence shows overload queueing on the shared warehouse following a batch burst; provisioning and lock signals remain low. The batch owner approved a 30-minute pause. We are monitoring latency, queueing and critical batch impact and will update at 14:30 UTC.”

## Official references

- [WAREHOUSE_LOAD_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/warehouse_load_history)
- [Query History](https://docs.snowflake.com/en/user-guide/ui-snowsight-activity)
