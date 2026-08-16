# Analytics Acceleration by Query Pattern

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

## Decision table

Do not enable every optimization. Capture a stable baseline and select the smallest mechanism that addresses the observed operator.

| Evidence | Candidate | Avoid when |
|---|---|---|
| Poor pruning on large range scans | Clustering | Table is small or change cost exceeds benefit |
| Highly selective point or substring lookup | Search Optimization Service | Queries return broad portions of the table |
| Frequently repeated eligible precomputation | Materialized view | Base data changes heavily or query shape is not reusable |
| Bursty scan with parallelizable operators | Query Acceleration Service | Bottleneck is queueing, compilation or poor SQL |
| Repeated identical result | Result cache and stable SQL | Freshness or session conditions prevent reuse |

## Controlled rollout

1. Record query ID, profile, duration distribution, bytes scanned, partitions scanned, concurrency and warehouse state.
2. Clone or isolate representative data and replay a query set, not one query.
3. Enable one candidate mechanism.
4. Compare latency percentiles, credits, serverless maintenance and storage.
5. Keep it only when the measured benefit satisfies the product SLO and cost policy.

Example materialized view candidate:

```sql
CREATE MATERIALIZED VIEW analytics.mv_daily_product_sales AS
SELECT order_date, product_id,
       SUM(net_amount) AS net_sales,
       COUNT(*) AS line_count
FROM core.order_lines
GROUP BY order_date, product_id;
```

Materialized views store results and incur storage and maintenance cost. They also have definition restrictions and edition requirements; confirm both before implementation.

## Monitoring and rollback

Track user latency and credits together with clustering, search-optimization or materialized-view maintenance. Re-test after material source-volume or query-shape changes. Remove an accelerator only after verifying queries no longer depend on its performance; retain the baseline and rollback threshold in the change record.

## Official references

- [Query performance options](https://docs.snowflake.com/en/user-guide/performance-query-options)
- [Storage optimization](https://docs.snowflake.com/en/user-guide/performance-query-storage)
- [Materialized views](https://docs.snowflake.com/en/user-guide/views-materialized)
- [Search Optimization Service](https://docs.snowflake.com/en/user-guide/search-optimization-service)
