# Runbook: Task and Dynamic Table Failures

Version: v1.1.0  
Status: Vendor-validated runbook  
Last vendor validation: 2026-08-15

## Trigger

Use when a task, task graph or dynamic-table refresh is failed, skipped, cancelled, suspended or missing its service objective.

## Safety

Do not repeatedly retry a non-idempotent workload. Preserve the task graph run ID, query ID, scheduled time, owner role, error code, error message and upstream state before modifying objects.

## Task evidence

```sql
SELECT
  NAME,
  DATABASE_NAME,
  SCHEMA_NAME,
  SCHEDULED_TIME,
  STATE,
  QUERY_ID,
  ERROR_CODE,
  ERROR_MESSAGE
FROM TABLE(
  INFORMATION_SCHEMA.TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START => DATEADD('hour', -4, CURRENT_TIMESTAMP()),
    RESULT_LIMIT => 100
  )
)
ORDER BY SCHEDULED_TIME DESC;
```

Verify that the task is resumed, the owner has required privileges, its condition is true, predecessors completed, and compute or serverless settings are valid.

## Dynamic-table evidence

```sql
SELECT
  NAME,
  STATE,
  STATE_CODE,
  STATE_MESSAGE,
  REFRESH_ACTION,
  REFRESH_TRIGGER,
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

Separate `FAILED`, `UPSTREAM_FAILED`, `SKIPPED`, `CANCELLED` and long-running `EXECUTING` states. Schema changes and upstream replacement can trigger reinitialization.

## Mitigation

Correct permissions, ownership, conditions, dependencies or SQL first. Retry a failed task graph only when the workload is safe to replay and the official retry prerequisites are satisfied. Coordinate dynamic-table suspension and resume around planned upstream DDL when appropriate.

## Validation

Confirm the next scheduled or approved manual run succeeds, downstream freshness is restored, duplicate processing did not occur and credits remain within expectations.

## Official references

- [Troubleshooting tasks](https://docs.snowflake.com/en/user-guide/tasks-ts)
- [TASK_HISTORY table function](https://docs.snowflake.com/en/sql-reference/functions/task_history)
- [Dynamic table refresh history](https://docs.snowflake.com/en/sql-reference/functions/dynamic_table_refresh_history)
- [Troubleshoot dynamic table refreshes](https://docs.snowflake.com/en/user-guide/dynamic-tables/troubleshoot-refreshes)
