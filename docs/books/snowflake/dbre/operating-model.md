# Snowflake DBRE Operating Model

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-15

## Purpose

The DBRE function makes Snowflake workload reliability explicit and measurable. It does not replace Snowflake administrators, data engineers, security, platform engineering, SRE or FinOps. It connects those disciplines through common service ownership, production standards and evidence-based decisions.

## Reliability boundary

Snowflake manages the service infrastructure. The enterprise DBRE boundary normally includes:

- account, database, schema, role and warehouse configuration;
- workload isolation, capacity and query-performance risk;
- tasks, streams, dynamic tables, ingestion and dependent pipelines;
- telemetry, alerts, dashboards and evidence retention;
- customer-configured replication, failover and recovery procedures;
- deployment safety, automation and configuration drift;
- incident coordination, RCA and corrective-action tracking;
- consumption guardrails and cost anomalies.

An internal SLO is a customer workload objective. It must not be represented as a Snowflake contractual SLA.

## Core responsibilities

| Responsibility | DBRE accountability | Key partners |
|---|---|---|
| Service inventory | Require an owner, criticality and dependency record | Product, data engineering |
| Reliability objectives | Facilitate measurable SLIs, SLOs and policies | Service owner, SRE |
| Production readiness | Define and enforce entry criteria | Platform, security, FinOps |
| Operational evidence | Ensure telemetry is decision-ready | Observability, administrators |
| Capacity and performance | Detect saturation and regressions; coordinate remediation | Performance engineering, FinOps |
| Recovery readiness | Validate RPO/RTO design and exercise procedures | Architecture, security, application teams |
| Incident and problem management | Lead technical diagnosis and durable follow-up | Incident command, service owner |
| Change safety | Require testing, rollback and post-change verification | Platform engineering, change management |

## RACI baseline

| Activity | Service owner | DBRE | Platform engineering | Security | FinOps |
|---|---|---|---|---|---|
| Set business criticality | A/R | C | C | C | C |
| Define SLO and error-budget policy | A | R | C | C | C |
| Implement telemetry | C | A | R | C | C |
| Approve production readiness | A | R | C | C | C |
| Execute standard remediation | C | A/R | R | C | C |
| Approve emergency risk acceptance | A | R | C | C | C |
| Set cost guardrails | C | C | C | C | A/R |
| Approve security exceptions | C | C | C | A/R | C |

`A` = accountable, `R` = responsible, `C` = consulted. Each organization should adapt the matrix and identify named roles.

## Operating cadence

| Cadence | Minimum review |
|---|---|
| Per shift/on call | Active incidents, failed critical pipelines, freshness breaches, saturation and security signals |
| Weekly | SLO trend, recurring failures, risky changes, capacity exceptions and open corrective actions |
| Monthly | Error-budget consumption, cost/reliability tradeoffs, access and configuration exceptions |
| Quarterly | Recovery exercise, maturity score, dependency review and risk register |
| Annually | SLO suitability, architecture, criticality, RPO/RTO and operating-model review |

## Guardrails

- Use dedicated operational roles with least privilege.
- Make high-impact actions explicit, reviewed and reversible where possible.
- Preserve query IDs, UTC timestamps and pre-change state in incident evidence.
- Do not automate destructive remediation until detection quality, scope controls and rollback are proven.
- Treat telemetry latency as part of the monitoring design.

## Official references

- [Access-control overview](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
- [Account Usage latency](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Cost-management overview](https://docs.snowflake.com/en/user-guide/cost-management-overview)

