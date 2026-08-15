# Facilitator Guide: Query Regression

Version: v1.2.0  
Status: Vendor-validated facilitator guide  
Last vendor validation: 2026-08-15

## Expected diagnosis

The regression is caused by a predicate change that increases scanning. Comparable query IDs show stable queueing but materially higher partitions and bytes scanned, with the scan operator dominating Query Profile.

## Strong response

1. Compare pre-change and post-change executions with the same query pattern and similar context.
2. Confirm correctness and the release timeline.
3. Restore the known-good SQL version through normal rollback.
4. Validate results, scan, operators, latency, queueing and credits.
5. Open a controlled optimization follow-up if the new requirement cannot use the old predicate.

## Common mistakes

- Increasing warehouse size without scan evidence.
- Comparing a result-cache hit with an executed query.
- Ignoring changes in data volume or distribution.
- Claiming clustering or Search Optimization will guarantee recovery.
- Validating only elapsed time and not query correctness.

## Example corrective actions

- Add representative regression queries to release testing.
- Record query hashes and performance baselines.
- Require performance review for predicate or join changes on large tables.
- Alert on repeated query-pattern deviation rather than isolated duration.

## Official references

- [GET_QUERY_OPERATOR_STATS](https://docs.snowflake.com/en/sql-reference/functions/get_query_operator_stats)
- [Explore execution times](https://docs.snowflake.com/en/user-guide/performance-query-exploring)
