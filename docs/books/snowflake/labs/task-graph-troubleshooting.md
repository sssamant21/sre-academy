# Lab: Task and Task-Graph Troubleshooting

Version: v1.1.0  
Status: Vendor-validated lab  
Last vendor validation: 2026-08-15

## Objective

Create an isolated root and child task, execute the graph, inspect task history and practice distinguishing task state, owner privilege and SQL failures.

## Safety and prerequisites

- Duration: approximately 30–45 minutes.
- Cost risk: low with a dedicated X-Small warehouse and auto-suspend.
- Required privileges: create database/schema/warehouse/task in the training environment, plus the account-level privileges required for owned tasks to run.
- Use only an approved training role. Tasks are created suspended and are not assigned a recurring schedule.
- Review replay safety before retrying any failed task graph.

## Setup

```sql
CREATE OR REPLACE WAREHOUSE HB_LAB_TASK_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

CREATE OR REPLACE DATABASE HB_LAB_TASK_DB;
CREATE OR REPLACE SCHEMA HB_LAB_TASK_DB.OPS;

CREATE OR REPLACE TABLE HB_LAB_TASK_DB.OPS.RUN_LOG (
  STEP_NAME VARCHAR,
  RUN_TS TIMESTAMP_LTZ
);

CREATE OR REPLACE TASK HB_LAB_TASK_DB.OPS.ROOT_TASK
  WAREHOUSE = HB_LAB_TASK_WH
AS
  INSERT INTO HB_LAB_TASK_DB.OPS.RUN_LOG
  SELECT 'ROOT', CURRENT_TIMESTAMP();

CREATE OR REPLACE TASK HB_LAB_TASK_DB.OPS.CHILD_TASK
  WAREHOUSE = HB_LAB_TASK_WH
  AFTER HB_LAB_TASK_DB.OPS.ROOT_TASK
AS
  INSERT INTO HB_LAB_TASK_DB.OPS.RUN_LOG
  SELECT 'CHILD', CURRENT_TIMESTAMP();
```

Tasks are initially suspended. Resume the child first and the root last:

```sql
ALTER TASK HB_LAB_TASK_DB.OPS.CHILD_TASK RESUME;
ALTER TASK HB_LAB_TASK_DB.OPS.ROOT_TASK RESUME;
EXECUTE TASK HB_LAB_TASK_DB.OPS.ROOT_TASK;
```

Execution is asynchronous. Wait for the graph to reach a terminal state, then inspect bounded history:

```sql
SELECT
  NAME,
  ROOT_TASK_ID,
  GRAPH_RUN_GROUP_ID,
  SCHEDULED_TIME,
  STATE,
  QUERY_ID,
  ERROR_CODE,
  ERROR_MESSAGE
FROM TABLE(
  HB_LAB_TASK_DB.INFORMATION_SCHEMA.TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START => DATEADD('hour', -1, CURRENT_TIMESTAMP()),
    RESULT_LIMIT => 100
  )
)
WHERE DATABASE_NAME = 'HB_LAB_TASK_DB'
ORDER BY SCHEDULED_TIME DESC;
```

Verify that the log contains both steps:

```sql
SELECT STEP_NAME, RUN_TS
FROM HB_LAB_TASK_DB.OPS.RUN_LOG
ORDER BY RUN_TS;
```

## Troubleshooting exercise

Without changing the task, document how you would diagnose each hypothetical condition:

1. Root remains suspended.
2. Owner role loses `USAGE` on the warehouse.
3. Child SQL references a missing object.
4. A non-idempotent child fails after partially committing external work.

For each, identify evidence, safe mitigation, retry risk and rollback.

## Success criteria

- Root and child appear in the same graph run.
- Both tasks reach `SUCCEEDED` and produce log rows.
- The reader explains task-owner privilege evaluation.
- Retry is not recommended until workload idempotency is established.

## Cleanup

```sql
ALTER TASK IF EXISTS HB_LAB_TASK_DB.OPS.ROOT_TASK SUSPEND;
DROP DATABASE IF EXISTS HB_LAB_TASK_DB;
DROP WAREHOUSE IF EXISTS HB_LAB_TASK_WH;
```

## Official references

- [Introduction to tasks](https://docs.snowflake.com/en/user-guide/tasks-intro)
- [Task graphs](https://docs.snowflake.com/en/user-guide/tasks-graphs)
- [TASK_HISTORY table function](https://docs.snowflake.com/en/sql-reference/functions/task_history)
- [EXECUTE TASK](https://docs.snowflake.com/en/sql-reference/sql/execute-task)
