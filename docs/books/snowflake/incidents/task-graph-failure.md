# Case Study: Task-Graph Failure

Version: v1.5.0
Status: In development
Last vendor validation: 2026-08-16

Fictional composite; all identifiers are illustrative.

## Incident

A nightly task graph stopped after its transform node. The root task had succeeded, but publication and quality-control children did not run. The daily product remained on the prior validated version.

## Evidence

```sql
SELECT *
FROM TABLE(INFORMATION_SCHEMA.COMPLETE_TASK_GRAPHS(
  ROOT_TASK_NAME => 'PIPELINE.ROOT_ORDERS',
  ERROR_ONLY => TRUE));

SELECT NAME, STATE, QUERY_ID, ERROR_CODE, ERROR_MESSAGE,
       SCHEDULED_TIME, COMPLETED_TIME
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
  TASK_NAME => 'PIPELINE.TRANSFORM_ORDERS',
  RESULT_LIMIT => 100))
ORDER BY SCHEDULED_TIME DESC;
```

The failed query showed a privilege error on a new target table. Deployment created the table under an engineer's role, and the task-owner role never received the expected `INSERT` grant.

## Root cause and contributors

Root cause: object creation bypassed the managed deployment role and left the task owner without required privileges. Contributors were ownership-dependent grants, no pre-deployment execution-as-owner test, and alerting that checked only root-task state.

## Recovery

Responders suspended the root to prevent overlapping retries, granted the minimum privilege through the approved role hierarchy, executed the failed SQL against cloned objects, then retried the graph using the supported task-graph retry mechanism. Counts and control totals were reconciled before publication.

## Corrective actions

- Deploy objects and grants from versioned code under controlled owner roles.
- Test every graph node with its execution role.
- Alert on failed/cancelled graph runs and nodes, not only the root.
- Make node SQL idempotent or persist a run ID and replay boundary.
- Add privilege-diff and future-object behavior tests to CI.
- Document automatic suspension thresholds and the operator resume procedure.

## Official references

- [Task graphs](https://docs.snowflake.com/en/user-guide/tasks-graphs)
- [Introduction to tasks](https://docs.snowflake.com/en/user-guide/tasks-intro)
- [`TASK_HISTORY`](https://docs.snowflake.com/en/sql-reference/functions/task_history)
- [`COMPLETE_TASK_GRAPHS`](https://docs.snowflake.com/en/sql-reference/functions/complete_task_graphs)

