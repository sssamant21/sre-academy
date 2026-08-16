# Production Incidents, RCA, and Case Studies

Version: v1.5.0
Status: Production Release
Last vendor validation: 2026-08-16

These case studies are fictional composites built from documented Snowflake failure modes. They are exercises, not claims about a named customer or observed outage. Each case separates evidence from inference and ends with corrective and preventive actions.

## Phase 1 cases

| Case | Primary symptom | Core evidence |
|---|---|---|
| [Snowpipe backlog and missing files](snowpipe-backlog.md) | Landing data stopped advancing | Pipe status, copy history, notification path |
| [Kafka ingestion freshness breach](kafka-freshness.md) | Topic offsets advanced but target freshness degraded | Kafka lag, connector tasks, Snowflake channel progress |
| [Dynamic-table refresh breach](dynamic-table-refresh.md) | Dashboard exceeded freshness objective | Refresh history, dependency graph, upstream DDL |
| [Task-graph failure](task-graph-failure.md) | Downstream tasks never completed | Graph history, task history, query errors |
| [Warehouse saturation](warehouse-saturation.md) | Interactive latency and queueing increased | Warehouse load and query history |
| [Unexpected credit consumption](unexpected-credit-consumption.md) | Daily spend exceeded forecast | Metering, warehouse, serverless and query attribution |

## Phase 2 cases

| Case | Primary symptom | Core evidence |
|---|---|---|
| [Authentication and network-policy outage](authentication-outage.md) | Human and workload logins failed | Login history, IdP and network-policy change |
| [Secure-sharing policy failure](sharing-policy-failure.md) | Approved consumer role returned no rows | Share grants, policy references and access history |
| [Iceberg catalog staleness](iceberg-catalog-staleness.md) | Snowflake remained on an older snapshot | Refresh status, catalog permissions and snapshot IDs |
| [AI enrichment regression](ai-enrichment-regression.md) | Quality declined while token use increased | Prompt/model lineage, evaluations and usage history |
| [Cortex Search grounding failure](cortex-search-grounding.md) | Answer cited an obsolete procedure | Retrieval trace, corpus version and document lifecycle |
| [ML model drift](ml-model-drift.md) | Normal behavior generated excessive alerts | Training lineage, feature drift and backtesting |

## Case-study contract

Every case includes impact, timeline, evidence, triage, containment, root cause, contributing factors, recovery, validation, RCA, corrective/preventive actions and learning objectives. Times, identifiers and measurements are illustrative. Responders must query the evidence retained in their account and account for telemetry latency and retention.

## Release scope

1. Pipeline and platform incidents — Production Release.
2. Security, sharing, Iceberg and AI/ML incidents — Production Release.

End-to-end architectures and full-lifecycle case studies remain candidates for a future handbook release and are not part of v1.5.0.
