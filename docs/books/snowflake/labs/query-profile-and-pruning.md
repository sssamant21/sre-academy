# Lab: Query Profile and Micro-partition Pruning

Version: v1.1.0  
Status: Vendor-validated lab  
Last vendor validation: 2026-08-15

## Objective

Run two semantically related queries, capture their query IDs and use Query History and Query Profile to compare scanned data and execution operators.

## Safety and prerequisites

- Duration: approximately 30–45 minutes.
- Cost risk: low when using a dedicated X-Small warehouse with auto-suspend.
- Required capabilities: permission to create objects in an isolated lab database and use a lab warehouse.
- Query History visibility depends on the active role. A user can review their own queries; broader visibility requires additional monitoring privileges.

## Setup

Replace the sample role assignment with an approved training role if required.

```sql
CREATE OR REPLACE WAREHOUSE HB_LAB_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

CREATE OR REPLACE DATABASE HB_LAB_DB;
CREATE OR REPLACE SCHEMA HB_LAB_DB.PERF;

CREATE OR REPLACE TABLE HB_LAB_DB.PERF.EVENTS AS
SELECT
  SEQ4() AS EVENT_ID,
  DATEADD('minute', -UNIFORM(0, 525600, RANDOM()), CURRENT_TIMESTAMP()) AS EVENT_TS,
  MOD(SEQ4(), 100) AS CUSTOMER_GROUP,
  UNIFORM(1, 1000, RANDOM()) AS METRIC_VALUE
FROM TABLE(GENERATOR(ROWCOUNT => 1000000));
```

## Exercise

Run and record the query ID for the broad scan:

```sql
SELECT CUSTOMER_GROUP, AVG(METRIC_VALUE)
FROM HB_LAB_DB.PERF.EVENTS
GROUP BY CUSTOMER_GROUP;

SELECT LAST_QUERY_ID() AS BROAD_QUERY_ID;
```

Run and record the query ID for a selective time predicate:

```sql
SELECT CUSTOMER_GROUP, AVG(METRIC_VALUE)
FROM HB_LAB_DB.PERF.EVENTS
WHERE EVENT_TS >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY CUSTOMER_GROUP;

SELECT LAST_QUERY_ID() AS SELECTIVE_QUERY_ID;
```

In Snowsight, open **Monitoring → Query History**, select each recorded query and inspect **Query Profile**. Compare the table-scan operator, partitions scanned, bytes scanned and most expensive nodes. Result-cache reuse can hide execution work; rerun only when necessary and record whether the result was served from cache.

For programmatic history, use a bounded query and replace the IDs:

```sql
SELECT
  QUERY_ID,
  TOTAL_ELAPSED_TIME,
  BYTES_SCANNED,
  PARTITIONS_SCANNED,
  PARTITIONS_TOTAL,
  PERCENTAGE_SCANNED_FROM_CACHE
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= DATEADD('hour', -2, CURRENT_TIMESTAMP())
  AND QUERY_ID IN ('<broad-query-id>', '<selective-query-id>');
```

Account Usage data can have latency; use Snowsight Query History for immediate inspection.

## Success criteria

- Both query IDs are captured.
- The reader can identify the scan operator and most expensive node.
- The comparison records partitions and bytes scanned.
- Any result-cache effect is explicitly identified.
- No conclusion relies solely on elapsed time.

## Cleanup

```sql
DROP DATABASE IF EXISTS HB_LAB_DB;
DROP WAREHOUSE IF EXISTS HB_LAB_WH;
```

## Official references

- [Monitor query activity with Query History](https://docs.snowflake.com/en/user-guide/ui-snowsight-activity)
- [Explore execution times in Query Profile](https://docs.snowflake.com/en/user-guide/performance-query-exploring)
- [QUERY_HISTORY Account Usage view](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)
