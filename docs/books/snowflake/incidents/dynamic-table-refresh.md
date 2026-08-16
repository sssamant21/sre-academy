# Case Study: Dynamic-Table Refresh Breach

Version: v1.5.0
Status: In development
Last vendor validation: 2026-08-16

Fictional composite; target lag is a best-effort freshness objective, not a guarantee.

## Incident

The executive sales dashboard exceeded its 15-minute freshness objective. The leaf dynamic table showed `UPSTREAM_FAILED`; its own SQL had not changed.

```sql
SELECT NAME, STATE, REFRESH_ACTION, REFRESH_TRIGGER,
       REFRESH_START_TIME, REFRESH_END_TIME, DATA_TIMESTAMP,
       TARGET_LAG_SEC, ERROR_CODE, ERROR_MESSAGE
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME_PREFIX => 'ANALYTICS', RESULT_LIMIT => 200))
ORDER BY REFRESH_START_TIME DESC;
```

The dependency graph traced the first `FAILED` state to `ORDERS_CLEAN`. Deployment history showed `CREATE OR REPLACE TABLE RAW.ORDERS` at the same time. The replacement reset change-tracking history and forced downstream reinitialization; the refresh warehouse could not complete the larger work within target lag.

## Root cause and contributors

Root cause: an upstream deployment replaced a base table without coordinating the dynamic-table pipeline's change-tracking and reinitialization behavior. Contributors were no DDL dependency gate, refresh-failure alerts not enabled, and capacity testing limited to incremental refreshes.

## Recovery

The team suspended affected publication, preserved refresh history and DDL, restored the compatible base-table definition, and resumed the pipeline in dependency order during a controlled window. It monitored the full reinitialization and validated source totals, aggregate results and downstream stream behavior before reopening the dashboard.

## Corrective actions

- Prefer compatible DML such as an approved `INSERT OVERWRITE` pattern when object identity must remain stable.
- Suspend and resume pipelines around incompatible planned DDL.
- Alert on `FAILED`, `UPSTREAM_FAILED`, suspension and actual-lag breaches.
- Capacity-test reinitialization and include it in cost/recovery planning.
- Record the dynamic-table dependency graph in change impact analysis.
- Set `REFRESH_MODE` explicitly and verify the resolved mode.

## Official references

- [Monitor dynamic tables](https://docs.snowflake.com/en/user-guide/dynamic-tables/monitoring)
- [Troubleshoot refreshes](https://docs.snowflake.com/en/user-guide/dynamic-tables/troubleshoot-refreshes)
- [`DYNAMIC_TABLE_REFRESH_HISTORY`](https://docs.snowflake.com/en/sql-reference/functions/dynamic_table_refresh_history)
- [Dynamic-table best practices](https://docs.snowflake.com/en/user-guide/dynamic-tables/best-practices)
