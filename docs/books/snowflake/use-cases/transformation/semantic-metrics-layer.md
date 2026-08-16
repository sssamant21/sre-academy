# Semantic Metrics Layer

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

## Use when

Use a Snowflake semantic view when BI, SQL and Cortex consumers need shared business entities, relationships, dimensions and metrics stored as a governed schema object. Confirm current feature availability, region support and account requirements before adoption.

## Contract-first workflow

1. Choose one bounded domain and fewer source objects than the enterprise model.
2. Define grain and primary keys for every logical table.
3. Name relationship cardinality and validate orphan and fan-out behavior.
4. Define public dimensions and metrics in business language; keep helper facts private.
5. Add descriptions, synonyms and verified queries.
6. Compare generated SQL and results with an approved golden-query suite.

A semantic view requires at least one dimension or metric. Start from the current official `CREATE SEMANTIC VIEW` grammar rather than copying a stale generated YAML or preview-era example.

```sql
DESCRIBE SEMANTIC VIEW analytics_semantic.sales_model;
SHOW SEMANTIC METRICS IN analytics_semantic.sales_model;
SHOW SEMANTIC DIMENSIONS IN analytics_semantic.sales_model;
```

## Production controls

- Assign a business metric owner and technical object owner.
- Treat relationship or metric-expression changes as reviewed code.
- Apply row access and masking to the underlying tables or views and test the semantic consumer role.
- Monitor query correctness, verified-query pass rate, latency and warehouse cost.
- Do not expose ambiguous metrics with the same name but different filters or time grains.
- Maintain a compatibility and deprecation policy for downstream tools.

## Validation and rollback

Validate totals across time grains, join paths, null keys, many-to-many relationships, role restrictions and representative natural-language questions. Preserve the prior DDL/YAML and verified queries; if validation fails, replace the semantic view with the last approved definition and invalidate dependent caches as appropriate.

## Official references

- [Semantic views overview](https://docs.snowflake.com/en/user-guide/views-semantic/overview)
- [`CREATE SEMANTIC VIEW`](https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view)
- [Semantic-view SQL management](https://docs.snowflake.com/en/user-guide/views-semantic/sql)
- [Semantic-view development practices](https://docs.snowflake.com/en/user-guide/views-semantic/best-practices-dev)

