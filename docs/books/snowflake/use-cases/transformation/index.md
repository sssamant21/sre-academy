# Transformation, Analytics, and Data Products

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

This phase turns trusted landing data into maintained models and governed consumer products. Select the pattern from the transformation semantics, freshness objective, query profile and consumer contract.

| Need | Pattern | Main operational concern |
|---|---|---|
| Declarative, freshness-driven SQL pipeline | [Dynamic table pipeline](dynamic-table-pipeline.md) | Actual lag and refresh cost |
| Historical dimension changes | [SCD Type 2 model](scd2-dimension.md) | Deterministic version ordering |
| Repeated selective or expensive analytics | [Analytics acceleration](analytics-acceleration.md) | Evidence-based feature selection and maintenance cost |
| Governed BI serving layer | [Governed dashboard product](governed-dashboard-product.md) | Metric, access and freshness contracts |
| Reusable business definitions | [Semantic metrics layer](semantic-metrics-layer.md) | Definition ownership and query validation |
| Automated quality evidence | [Data-quality contract](data-quality-contract.md) | Edition, evaluation cost and response ownership |

## Shared product contract

Every production data product must name its owner, consumers, source dependencies, schema and metric definitions, freshness and quality SLOs, access policy, cost boundary, change process, monitoring, recovery path and deprecation date. A table or dashboard without those controls is an output, not an operated data product.

