# Simulation: Failed Task Graph

Version: v1.2.0  
Status: Vendor-validated simulation  
Last vendor validation: 2026-08-15

## Objective

Find the first failed task, correct the cause and decide whether retrying the graph is safe.

## Scenario

A nightly transformation graph is incomplete. Downstream reporting is delayed, and one child task shows a failed state.

## Safety

Do not retry until idempotency and partial side effects are understood. Do not alter task ownership or grants without recording the original state.

## Facilitator injects

| Time | Inject |
|---|---|
| T+0 | Reporting freshness alert fires |
| T+5 | Root succeeded; one child failed; downstream tasks did not complete |
| T+10 | Error evidence shows a referenced column was renamed |
| T+15 | The failed child wrote no rows before failure |
| T+20 | The task graph has not been modified since the failed run |
| T+25 | The first attempt occurred within the supported retry window |

## Evidence participants must request

```sql
SELECT
  NAME,
  ROOT_TASK_ID,
  GRAPH_RUN_GROUP_ID,
  SCHEDULED_TIME,
  COMPLETED_TIME,
  STATE,
  QUERY_ID,
  ERROR_CODE,
  ERROR_MESSAGE,
  SCHEDULED_FROM
FROM TABLE(
  INFORMATION_SCHEMA.TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START => DATEADD('day', -1, CURRENT_TIMESTAMP()),
    RESULT_LIMIT => 500
  )
)
ORDER BY SCHEDULED_TIME DESC;
```

Request task definitions, owner roles, dependent-task graph, deployment record and downstream data checks.

## Decisions

1. Identify the first failed node rather than the final symptom.
2. Confirm whether correcting the SQL requires a task-graph modification.
3. Determine whether `EXECUTE TASK ... RETRY LAST` prerequisites remain satisfied.
4. If retry is not eligible, define a controlled alternative.
5. Validate completeness and absence of duplicates.

## Success criteria

- Replay safety is explicit.
- Permission, state, condition and SQL causes are distinguished.
- The team does not blindly restart the entire pipeline.
- Downstream freshness and data correctness are both validated.

## Official references

- [Troubleshooting tasks](https://docs.snowflake.com/en/user-guide/tasks-ts)
- [TASK_HISTORY table function](https://docs.snowflake.com/en/sql-reference/functions/task_history)
- [EXECUTE TASK](https://docs.snowflake.com/en/sql-reference/sql/execute-task)
- [Task graphs](https://docs.snowflake.com/en/user-guide/tasks-graphs)
