# Simulation: Query Performance Regression

Version: v1.2.0  
Status: Vendor-validated simulation  
Last vendor validation: 2026-08-15

## Objective

Determine why a repeated query pattern regressed and avoid treating warehouse size as the default answer.

## Scenario

A dashboard query that normally completes within its SLO becomes three times slower after a data release. Functional results remain correct.

## Safety

Use supplied query IDs or isolated non-production evidence. Query text can contain sensitive literals; do not copy it into broad incident channels.

## Facilitator injects

| Time | Inject |
|---|---|
| T+0 | P95 latency regression is confirmed for one parameterized query hash |
| T+5 | Queued and provisioning time are near baseline |
| T+10 | Partitions and bytes scanned increased materially |
| T+15 | Query Profile shows the table-scan operator dominates |
| T+20 | The data team confirms a predicate changed in the release |
| T+25 | A known-good query version is available for rollback |

## Evidence participants must request

- Two comparable query IDs from before and after the release.
- Query hash, data window, warehouse, scan, partition, spill, queue and cache metrics.
- Query Profile or operator statistics:

```sql
SELECT *
FROM TABLE(GET_QUERY_OPERATOR_STATS('<query-id>'));
```

## Decisions

1. Separate SQL/data regression from warehouse contention.
2. Decide whether to restore the known-good SQL.
3. Define correctness and performance validation.
4. Identify whether longer-term pruning, clustering or another optimization needs controlled evaluation.
5. Reject any performance guarantee unsupported by measured evidence.

## Success criteria

- Comparable executions are used.
- Scan and operator evidence supports the diagnosis.
- Rollback includes correctness validation.
- Cost-bearing optimizations are treated as experiments, not assumptions.

## Official references

- [Explore execution times](https://docs.snowflake.com/en/user-guide/performance-query-exploring)
- [GET_QUERY_OPERATOR_STATS](https://docs.snowflake.com/en/sql-reference/functions/get_query_operator_stats)
- [QUERY_HISTORY Account Usage view](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)
