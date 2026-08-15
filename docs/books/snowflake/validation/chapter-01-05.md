# Snowflake Vendor Validation Matrix — Chapters 1–5

Validation date: 2026-08-15  
Status: Technical review complete for the claims listed below  
Source policy: Official Snowflake documentation only

| Area | Chapters | Validation result | Action |
|---|---:|---|---|
| Organizations, accounts, editions, and architecture | 1–2 | Confirmed with availability caveats | Removed unresolved publication notes and retained edition/region qualification |
| Native-table micro-partitions | 2–3 | Confirmed | Preserved the documented 50–500 MB uncompressed range and automatic columnar organization |
| Persisted query results | 2, 4 | Correct with missing lifecycle nuance | Added 24-hour retention, reset-on-reuse, 31-day maximum, and non-guaranteed reuse wording |
| Warehouse cache | 2, 4 | Confirmed | Clarified that suspension drops the warehouse cache |
| General “metadata cache” | 2, 4 | Not documented as a separate general-purpose cache | Reframed as metadata services and metadata-based optimization |
| Optimizer internals | 2, 4, 5 | Partially proprietary | Replaced overly specific cost-based-algorithm claims with cautious Snowflake optimizer terminology |
| Multi-cluster warehouses | 2, 5 | Confirmed; Enterprise Edition or higher | Added edition and Auto-scale qualifications |
| Search optimization | 5 | Confirmed; Enterprise Edition or higher | Added edition and cost qualification |
| Materialized views | 5 | Confirmed; Enterprise Edition or higher | Added edition, storage, maintenance, and restriction context |
| Query Profile and operators | 4–5 | Confirmed | Retained evidence-based diagnostic guidance |

## Primary sources

- [Snowflake editions](https://docs.snowflake.com/en/user-guide/intro-editions)
- [Micro-partitions and data clustering](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions)
- [Using persisted query results](https://docs.snowflake.com/en/user-guide/querying-persisted-results)
- [Optimizing the warehouse cache](https://docs.snowflake.com/en/user-guide/performance-query-warehouse-cache)
- [Multi-cluster warehouses](https://docs.snowflake.com/en/user-guide/warehouses-multicluster)
- [Query Profile](https://docs.snowflake.com/en/user-guide/ui-query-profile)
- [Optimizing query performance](https://docs.snowflake.com/en/user-guide/performance-query-options)
- [Search optimization service](https://docs.snowflake.com/en/user-guide/search-optimization-service)
- [Materialized views](https://docs.snowflake.com/en/user-guide/views-materialized)

## Review limitation

This validation confirms handbook statements against currently published vendor documentation. It does not certify undocumented Snowflake internals, guarantee feature availability in every account, or replace workload-specific testing. Edition, cloud, region, account configuration, and preview/GA status must be rechecked before implementation.
