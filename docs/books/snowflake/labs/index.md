# Snowflake Hands-on Labs

Version: v1.1.0  
Status: Production Release  
Last vendor validation: 2026-08-15

The labs turn handbook concepts into repeatable exercises. Run them in a non-production account or an isolated training environment.

## Safety rules

- Use a dedicated training role, database, schema and warehouse.
- Apply a small warehouse size, auto-suspend and a resource monitor or budget appropriate to the environment.
- Never use production data, credentials, integrations or network policies.
- Review each statement before execution; privileges and available features vary by account and edition.
- Complete the cleanup section even when a lab fails midway.
- Treat measured performance as environment-specific evidence, not a guaranteed benchmark.

## Available labs

| Lab | Primary chapters | Outcome |
|---|---|---|
| [Query Profile and Micro-partition Pruning](query-profile-and-pruning.md) | 3, 4, 5 and 7 | Compare query history and profiles before and after a selective predicate |
| [Warehouse Concurrency and Queue Analysis](warehouse-concurrency-analysis.md) | 6 and 9 | Identify running, queued and provisioning load without changing production capacity |
| [Credit Baseline and Cost Guardrails](credit-baseline-and-guardrails.md) | 9 and 10 | Build a bounded consumption baseline and evaluate warehouse guardrails |
| [Task and Task-Graph Troubleshooting](task-graph-troubleshooting.md) | 11, 12 and 18 | Execute an isolated graph and diagnose state, privilege and replay risks |
| [Dynamic Table Monitoring and Freshness](dynamic-table-monitoring.md) | 9, 11 and 18 | Observe refresh history and interpret best-effort target lag |
| [Authentication and Network-Policy Diagnosis](authentication-network-policy-diagnosis.md) | 8, 11 and 17 | Classify connection failures without changing account access |
| [Query Regression Investigation](query-regression-investigation.md) | 4, 5, 7 and 14 | Compare repeated query patterns and operator evidence |
| [Production Readiness Review Exercise](production-readiness-exercise.md) | 8–12 and 17–20 | Produce an evidence-based launch decision |

## Standard lab contract

Every lab must include:

1. Objective and measurable success criteria.
2. Required privileges, edition considerations and estimated cost exposure.
3. Isolated setup using uniquely named objects.
4. Ordered execution and evidence-capture steps.
5. Expected observations without fixed performance promises.
6. Troubleshooting notes.
7. Idempotent cleanup where Snowflake supports it.
8. Official Snowflake references and a validation date.

## Incident simulations

The [v1.2 incident simulation collection](simulations/index.md) provides six facilitated exercises for warehouse saturation, query regression, credit anomalies, failed task graphs, authentication/network-policy outages and dynamic-table freshness breaches.

See the [lab authoring standard](lab-standard.md) before adding or modifying a lab.
