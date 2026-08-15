# Runbook: Query Performance Regression

Version: v1.1.0  
Status: Vendor-validated runbook  
Last vendor validation: 2026-08-15

## Trigger

Use when a previously stable query pattern exceeds its latency objective or consumes materially more scan, compute or spill resources.

## Safety

Capture representative query IDs before changing SQL, warehouse size, clustering or services. Do not use one elapsed-time sample as proof; result-cache reuse, queueing and data volume can change the observation.

## Evidence

Use Query History with a bounded UTC window. Compare query hash or parameterized query hash when available, warehouse, compilation and execution time, bytes and partitions scanned, spill, queueing and cache percentage.

For a completed query ID:

```sql
SELECT *
FROM TABLE(GET_QUERY_OPERATOR_STATS('<query-id>'));
```

In Snowsight, inspect Query Profile and its most expensive operators.

## Decision points

- Increased queued time: follow the warehouse-queuing runbook.
- Increased partitions or bytes scanned: inspect predicates, pruning and data distribution.
- Remote or local spill: review operator memory pressure, SQL shape and warehouse evidence.
- Compilation increase: inspect object, policy and SQL changes.
- Stable operator evidence but slower elapsed time: compare concurrency, provisioning and client timing.
- Changed data volume or distribution: do not attribute the regression solely to code.

## Mitigation

Choose one reversible change: restore a known-good SQL version, isolate the workload, remove an accidental broad scan, or temporarily adjust compute through change control. Validate before adopting clustering, Search Optimization Service, materialized views or other cost-bearing features.

## Validation and rollback

Compare multiple equivalent executions and record service latency, scan, spill, queueing and credits. Roll back if performance, correctness or cost worsens.

## Official references

- [Explore execution times](https://docs.snowflake.com/en/user-guide/performance-query-exploring)
- [GET_QUERY_OPERATOR_STATS](https://docs.snowflake.com/en/sql-reference/functions/get_query_operator_stats)
- [Query History](https://docs.snowflake.com/en/user-guide/ui-snowsight-activity)
