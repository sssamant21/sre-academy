# Lab: Dynamic Table Monitoring and Freshness

Version: v1.1.0  
Status: Vendor-validated lab  
Last vendor validation: 2026-08-15

## Objective

Create an isolated dynamic table, observe refresh history and distinguish target lag from a guaranteed refresh interval.

## Safety and prerequisites

- Duration: approximately 30–45 minutes.
- Cost risk: low with an X-Small refresh warehouse and limited source data.
- Required privileges: approved training permissions to create and operate a warehouse, database, schema, table and dynamic table.
- Feature availability, privileges and behavior must be confirmed for the training account.
- Target lag is a freshness target and is best effort; it is not a guaranteed schedule.

## Setup

```sql
CREATE OR REPLACE WAREHOUSE HB_LAB_DT_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

CREATE OR REPLACE DATABASE HB_LAB_DT_DB;
CREATE OR REPLACE SCHEMA HB_LAB_DT_DB.PIPELINE;

CREATE OR REPLACE TABLE HB_LAB_DT_DB.PIPELINE.EVENT_SOURCE (
  EVENT_ID NUMBER,
  EVENT_TS TIMESTAMP_LTZ,
  AMOUNT NUMBER(12,2)
);

INSERT INTO HB_LAB_DT_DB.PIPELINE.EVENT_SOURCE
VALUES
  (1, CURRENT_TIMESTAMP(), 10.00),
  (2, CURRENT_TIMESTAMP(), 20.00);

CREATE OR REPLACE DYNAMIC TABLE HB_LAB_DT_DB.PIPELINE.EVENT_SUMMARY
  TARGET_LAG = '5 minutes'
  WAREHOUSE = HB_LAB_DT_WH
  REFRESH_MODE = AUTO
  INITIALIZE = ON_CREATE
AS
SELECT
  DATE_TRUNC('hour', EVENT_TS) AS EVENT_HOUR,
  COUNT(*) AS EVENT_COUNT,
  SUM(AMOUNT) AS TOTAL_AMOUNT
FROM HB_LAB_DT_DB.PIPELINE.EVENT_SOURCE
GROUP BY DATE_TRUNC('hour', EVENT_TS);
```

## Observe state and refresh evidence

```sql
SELECT *
FROM TABLE(
  HB_LAB_DT_DB.INFORMATION_SCHEMA.DYNAMIC_TABLES(
    NAME => 'HB_LAB_DT_DB.PIPELINE.EVENT_SUMMARY',
    RESULT_LIMIT => 10
  )
);

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
  HB_LAB_DT_DB.INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    NAME => 'HB_LAB_DT_DB.PIPELINE.EVENT_SUMMARY',
    RESULT_LIMIT => 100
  )
)
ORDER BY REFRESH_START_TIME DESC;
```

Add a new source row, then observe that target lag does not mean an exact five-minute refresh interval:

```sql
INSERT INTO HB_LAB_DT_DB.PIPELINE.EVENT_SOURCE
VALUES (3, CURRENT_TIMESTAMP(), 30.00);
```

Do not loop manual refreshes. Wait for the scheduler or, if explicitly approved, perform one manual refresh:

```sql
ALTER DYNAMIC TABLE HB_LAB_DT_DB.PIPELINE.EVENT_SUMMARY REFRESH;
```

## Success criteria

- The dynamic table and its latest refresh state are visible.
- The reader records refresh action, trigger, data timestamp and target lag.
- The reader can explain best-effort target lag.
- No performance or freshness guarantee is inferred from one refresh.

## Cleanup

```sql
DROP DATABASE IF EXISTS HB_LAB_DT_DB;
DROP WAREHOUSE IF EXISTS HB_LAB_DT_WH;
```

## Official references

- [Dynamic tables overview](https://docs.snowflake.com/en/user-guide/dynamic-tables/overview)
- [Monitor dynamic tables](https://docs.snowflake.com/en/user-guide/dynamic-tables/monitoring)
- [Set target lag](https://docs.snowflake.com/en/user-guide/dynamic-tables/target-lag)
- [DYNAMIC_TABLE_REFRESH_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/dynamic_table_refresh_history)
