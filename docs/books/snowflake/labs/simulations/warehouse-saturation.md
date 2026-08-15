# Simulation: Warehouse Saturation

Version: v1.2.0  
Status: Vendor-validated simulation  
Last vendor validation: 2026-08-15

## Objective

Diagnose elevated application latency, distinguish overload queueing from provisioning and blocking, and select a reversible mitigation.

## Scenario

At 14:00 UTC, an interactive workload exceeds its latency SLO. A batch release started 20 minutes earlier on the same warehouse. No Snowflake service incident is reported.

## Safety

This is a tabletop or isolated-environment exercise. Do not launch uncontrolled concurrent queries, cancel production queries or resize a production warehouse.

## Facilitator injects

| Time | Inject |
|---|---|
| T+0 | P95 application latency is four times baseline |
| T+5 | Warehouse history shows elevated `AVG_QUEUED_LOAD`; provisioning and blocked load remain low |
| T+10 | Query History shows a burst of batch statements sharing the interactive warehouse |
| T+15 | FinOps reports that an immediate permanent resize would exceed forecast |
| T+20 | The batch owner confirms the workload can pause for 30 minutes |

## Evidence participants must request

```sql
SELECT
  START_TIME,
  END_TIME,
  AVG_RUNNING,
  AVG_QUEUED_LOAD,
  AVG_QUEUED_PROVISIONING,
  AVG_BLOCKED
FROM TABLE(
  INFORMATION_SCHEMA.WAREHOUSE_LOAD_HISTORY(
    DATE_RANGE_START => DATEADD('hour', -2, CURRENT_TIMESTAMP()),
    DATE_RANGE_END => DATEADD('minute', -2, CURRENT_TIMESTAMP()),
    WAREHOUSE_NAME => '<warehouse-name>'
  )
)
ORDER BY START_TIME;
```

Also request representative query IDs, query tags, workload owners, current warehouse configuration and credit baseline.

## Decisions

1. Declare whether saturation is confirmed.
2. Choose between pausing non-critical batch work, approved workload isolation or temporary capacity.
3. State why a lock or client problem is not the primary diagnosis.
4. Define validation intervals and rollback.
5. Record the long-term corrective action.

## Success criteria

- Queueing is separated from provisioning and blocking.
- The mitigation protects the interactive SLO and is reversible.
- Cost impact and temporary-change expiry are explicit.
- A permanent resize is not selected from one interval alone.

## Official references

- [WAREHOUSE_LOAD_HISTORY table function](https://docs.snowflake.com/en/sql-reference/functions/warehouse_load_history)
- [WAREHOUSE_LOAD_HISTORY Account Usage view](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_load_history)
- [Query History](https://docs.snowflake.com/en/user-guide/ui-snowsight-activity)
