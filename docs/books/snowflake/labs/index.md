# Snowflake Hands-on Labs

Version: v1.1.0  
Status: In development  
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

See the [lab authoring standard](lab-standard.md) before adding or modifying a lab.
