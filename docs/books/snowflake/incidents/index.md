# Production Incidents, RCA, and Case Studies

Version: v1.5.0
Status: In development
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

## Case-study contract

Every case includes impact, timeline, evidence, triage, containment, root cause, contributing factors, recovery, validation, RCA, corrective/preventive actions and learning objectives. Times, identifiers and measurements are illustrative. Responders must query the evidence retained in their account and account for telemetry latency and retention.

## Planned phases

1. Pipeline and platform incidents — draft implementation.
2. Security, sharing, Iceberg and AI/ML incidents — planned.
3. End-to-end architectures and full lifecycle case studies — planned.

