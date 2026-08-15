# Runbook: Dynamic Table Freshness Degradation

Version: v1.1.0  
Status: Vendor-validated runbook  
Last vendor validation: 2026-08-15

## Trigger

Use when a dynamic table misses its target lag, refresh duration grows materially, or downstream data freshness violates an agreed objective.

## Safety

Do not recreate or change refresh mode during initial triage. Reinitialization can reprocess data and can produce a large change set for streams on the dynamic table.

## Evidence

Query recent refresh history and retain state, message, action, trigger, target lag, data timestamp and refresh timing. Map the full upstream chain before changing a downstream object.

```sql
SELECT
  NAME,
  STATE,
  STATE_CODE,
  STATE_MESSAGE,
  REFRESH_ACTION,
  REFRESH_TRIGGER,
  TARGET_LAG_SEC,
  DATA_TIMESTAMP,
  REFRESH_START_TIME,
  REFRESH_END_TIME
FROM TABLE(
  INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    NAME => '<database>.<schema>.<dynamic-table>',
    RESULT_LIMIT => 100
  )
)
ORDER BY REFRESH_START_TIME DESC;
```

## Decision points

- `UPSTREAM_FAILED`: repair the first failed upstream object.
- `SKIPPED`: inspect upstream skips, scheduler decisions and target-lag chain.
- Reinitialization: identify upstream replacement or schema change.
- Successful but slow refresh: inspect refresh query performance, changed volume and warehouse behavior.
- Replica state: account for replication and read-only secondary limitations.

## Mitigation

Correct the earliest upstream failure. Coordinate planned DDL by suspending and resuming affected dynamic tables when that procedure is appropriate. Change target lag, warehouse or definition only after freshness, cost and downstream consequences are reviewed.

## Validation

Confirm successful refreshes across at least two expected cycles, current data timestamp, downstream health and acceptable credit use.

## Official references

- [Monitor dynamic tables](https://docs.snowflake.com/en/user-guide/dynamic-tables/monitoring)
- [Troubleshoot refreshes](https://docs.snowflake.com/en/user-guide/dynamic-tables/troubleshoot-refreshes)
- [Dynamic table refresh history](https://docs.snowflake.com/en/sql-reference/functions/dynamic_table_refresh_history)
