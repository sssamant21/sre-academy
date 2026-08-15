# Lab: Query Regression Investigation

Version: v1.1.0  
Status: Vendor-validated lab  
Last vendor validation: 2026-08-15

## Objective

Identify a repeated query pattern whose latency changed, compare representative query IDs and inspect operator evidence without immediately changing warehouse capacity.

## Safety and prerequisites

- Duration: approximately 30 minutes.
- Cost risk: low, read-only history analysis.
- Required access: an analysis warehouse and approved Query History visibility.
- Account Usage can have latency. Use a bounded window and do not treat it as a real-time alert source.
- Query text can contain sensitive literals; restrict access and avoid copying it into broadly visible tickets.

## Identify repeated patterns

```sql
SELECT
  QUERY_PARAMETERIZED_HASH,
  COUNT(*) AS EXECUTIONS,
  APPROX_PERCENTILE(TOTAL_ELAPSED_TIME, 0.50) AS P50_MS,
  APPROX_PERCENTILE(TOTAL_ELAPSED_TIME, 0.95) AS P95_MS,
  SUM(BYTES_SCANNED) AS BYTES_SCANNED,
  SUM(CREDITS_USED_CLOUD_SERVICES) AS CLOUD_SERVICES_CREDITS
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
  AND EXECUTION_STATUS = 'SUCCESS'
  AND QUERY_PARAMETERIZED_HASH IS NOT NULL
GROUP BY QUERY_PARAMETERIZED_HASH
HAVING COUNT(*) >= 5
ORDER BY P95_MS DESC
LIMIT 25;
```

Choose one approved query hash. Retrieve representative recent executions:

```sql
SELECT
  QUERY_ID,
  START_TIME,
  WAREHOUSE_NAME,
  TOTAL_ELAPSED_TIME,
  EXECUTION_TIME,
  QUEUED_OVERLOAD_TIME,
  QUEUED_PROVISIONING_TIME,
  BYTES_SCANNED,
  PARTITIONS_SCANNED,
  PARTITIONS_TOTAL,
  BYTES_SPILLED_TO_LOCAL_STORAGE,
  BYTES_SPILLED_TO_REMOTE_STORAGE,
  PERCENTAGE_SCANNED_FROM_CACHE
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
  AND QUERY_PARAMETERIZED_HASH = '<approved-query-hash>'
ORDER BY START_TIME DESC
LIMIT 50;
```

For two comparable completed query IDs:

```sql
SELECT *
FROM TABLE(GET_QUERY_OPERATOR_STATS('<query-id>'));
```

Compare the same logical pattern, data context and warehouse conditions. Separate execution regression from queueing, provisioning and cache effects.

## Success criteria

- A repeated pattern is selected using a query hash rather than text matching.
- At least two comparable query IDs are documented.
- Operator, scan, spill, queue and cache evidence are compared.
- The conclusion accounts for data volume and warehouse context.
- A reversible experiment is proposed before permanent optimization.

## Cleanup

No objects are created.

## Official references

- [QUERY_HISTORY Account Usage view](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)
- [GET_QUERY_OPERATOR_STATS](https://docs.snowflake.com/en/sql-reference/functions/get_query_operator_stats)
- [Explore execution times](https://docs.snowflake.com/en/user-guide/performance-query-exploring)
