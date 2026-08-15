# Simulation: Dynamic-Table Freshness Breach

Version: v1.2.0  
Status: Vendor-validated simulation  
Last vendor validation: 2026-08-15

## Objective

Trace a freshness breach to the first upstream failure and restore the pipeline without unnecessary recreation.

## Scenario

A customer-facing dataset exceeds its freshness objective. The downstream dynamic table is present but its data timestamp is stale.

## Safety

Do not recreate the dynamic table during initial triage. Reinitialization can reprocess data and can expose a large change set to streams.

## Facilitator injects

| Time | Inject |
|---|---|
| T+0 | Actual freshness exceeds the target |
| T+5 | Downstream refresh state is `UPSTREAM_FAILED` |
| T+10 | The first upstream table shows `FAILED` with a schema-related message |
| T+15 | An upstream column was renamed during a deployment |
| T+20 | The previous definition is available |
| T+25 | Reverting the schema change is safer than recreating the pipeline |

## Evidence participants must request

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

Request connected dependencies, deployment changes, target lag, refresh duration, current data timestamp and downstream consumers.

## Decisions

1. Identify the first failed upstream object.
2. Choose rollback or forward correction.
3. Avoid changing target lag or warehouse size when the cause is schema incompatibility.
4. Define validation across at least two expected refresh cycles.
5. Assess downstream streams and consumers for reinitialization effects.

## Success criteria

- The first failure is distinguished from downstream symptoms.
- Target lag is treated as best effort, not a guaranteed interval.
- The selected change directly addresses the schema cause.
- Freshness, correctness, cost and downstream health are validated.

## Official references

- [Monitor dynamic tables](https://docs.snowflake.com/en/user-guide/dynamic-tables/monitoring)
- [Troubleshoot refreshes](https://docs.snowflake.com/en/user-guide/dynamic-tables/troubleshoot-refreshes)
- [DYNAMIC_TABLE_REFRESH_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/dynamic_table_refresh_history)
- [Set target lag](https://docs.snowflake.com/en/user-guide/dynamic-tables/target-lag)
