# Case Study: Warehouse Saturation

Version: v1.5.0
Status: In development
Last vendor validation: 2026-08-16

Fictional composite; measurements are environment-specific.

## Incident

Interactive dashboard p95 latency increased from 8 seconds to 74 seconds during a batch window. Queries showed significant queued-overload time while compilation and remote spill remained near their normal ranges.

```sql
SELECT START_TIME, AVG_RUNNING, AVG_QUEUED_LOAD,
       AVG_QUEUED_PROVISIONING, AVG_BLOCKED
FROM TABLE(INFORMATION_SCHEMA.WAREHOUSE_LOAD_HISTORY(
  WAREHOUSE_NAME => 'BI_WH',
  START_TIME => DATEADD('hour', -4, CURRENT_TIMESTAMP())))
ORDER BY START_TIME;

SELECT QUERY_ID, USER_NAME, QUERY_TAG, TOTAL_ELAPSED_TIME,
       QUEUED_OVERLOAD_TIME, QUEUED_PROVISIONING_TIME,
       BYTES_SCANNED, BYTES_SPILLED_TO_REMOTE_STORAGE
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE WAREHOUSE_NAME = 'BI_WH'
  AND START_TIME >= DATEADD('hour', -4, CURRENT_TIMESTAMP())
ORDER BY QUEUED_OVERLOAD_TIME DESC;
```

Query tags identified a new hourly export sharing the BI warehouse. Its fan-out produced many concurrent broad scans. The incident was concurrency saturation, not proof that every dashboard query required a larger warehouse.

## Containment and recovery

The export was paused and moved to its designated batch warehouse. Queueing fell without resizing `BI_WH`. The team then replayed representative dashboards and confirmed latency, error rate and credits across a peak interval.

## Root cause and contributors

Root cause: workload-routing configuration assigned a batch export to the interactive warehouse. Contributors were a permissive default warehouse, missing mandatory query tags, and no queue-depth SLO alert.

## Corrective actions

- Enforce workload-specific roles, warehouses and query tags.
- Alert on queued-overload time and latency percentiles together.
- Decide between SQL remediation, workload isolation, scale-up and multi-cluster scale-out from evidence.
- Load-test concurrency and failure behavior before onboarding a workload.
- Apply auto-suspend, timeouts and resource controls to each warehouse class.

## Official references

- [Monitoring warehouse load](https://docs.snowflake.com/en/user-guide/warehouses-load-monitoring)
- [`WAREHOUSE_LOAD_HISTORY`](https://docs.snowflake.com/en/sql-reference/functions/warehouse_load_history)
- [`QUERY_HISTORY`](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)
- [Multi-cluster warehouses](https://docs.snowflake.com/en/user-guide/warehouses-multicluster)

