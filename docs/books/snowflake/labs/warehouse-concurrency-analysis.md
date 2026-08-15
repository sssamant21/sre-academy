# Lab: Warehouse Concurrency and Queue Analysis

Version: v1.1.0  
Status: Vendor-validated lab  
Last vendor validation: 2026-08-15

## Objective

Use bounded history queries to distinguish workload execution, overload queuing, provisioning queuing and transaction blocking.

## Safety and prerequisites

- Duration: approximately 20–30 minutes.
- Cost risk: read-only analysis; querying metadata still uses warehouse compute.
- Required access: permission to use a small analysis warehouse and access the relevant Information Schema or Account Usage history.
- Do not resize, resume, suspend or change scaling policy in this lab.

## Recent warehouse load

Replace `<warehouse-name>` with the exact warehouse name:

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
    DATE_RANGE_START => DATEADD('hour', -4, CURRENT_TIMESTAMP()),
    DATE_RANGE_END   => DATEADD('minute', -2, CURRENT_TIMESTAMP()),
    WAREHOUSE_NAME  => '<warehouse-name>'
  )
)
ORDER BY START_TIME;
```

Snowflake notes that the table function covers the most recent 14 days and that values within one minute of the current timestamp can be inaccurate. This lab deliberately ends the range two minutes before the current time.

## Longer-term pattern

```sql
SELECT
  DATE_TRUNC('hour', START_TIME) AS HOUR,
  AVG(AVG_RUNNING) AS AVG_RUNNING,
  AVG(AVG_QUEUED_LOAD) AS AVG_QUEUED_LOAD,
  AVG(AVG_QUEUED_PROVISIONING) AS AVG_QUEUED_PROVISIONING,
  AVG(AVG_BLOCKED) AS AVG_BLOCKED
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_LOAD_HISTORY
WHERE WAREHOUSE_NAME = '<warehouse-name>'
  AND START_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY 1;
```

Interpretation:

- `AVG_QUEUED_LOAD` indicates queueing because the warehouse was overloaded.
- `AVG_QUEUED_PROVISIONING` indicates queueing while compute resources were being provisioned.
- `AVG_BLOCKED` indicates time blocked by a transaction lock.
- `AVG_RUNNING` is a load ratio, not a direct query count.

## Success criteria

- The observation window and warehouse are explicit.
- Queuing is separated from provisioning and blocking.
- A recommendation is based on repeated intervals, not a single sample.
- No capacity change is made without workload, cost and rollback review.

## Cleanup

No objects are created. Suspend the analysis warehouse only if that is consistent with the environment's normal operating procedure.

## Official references

- [WAREHOUSE_LOAD_HISTORY table function](https://docs.snowflake.com/en/sql-reference/functions/warehouse_load_history)
- [WAREHOUSE_LOAD_HISTORY Account Usage view](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_load_history)
