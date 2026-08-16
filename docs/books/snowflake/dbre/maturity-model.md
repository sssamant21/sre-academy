# Snowflake DBRE Maturity Model

Version: v1.3.0  
Status: Production Release  
Last vendor validation: 2026-08-15

The maturity model prioritizes improvement; it is not a certification. Score each domain using current evidence, record gaps and reassess after corrective work.

## Levels

| Level | Name | Characteristics |
|---:|---|---|
| 1 | Reactive | Ownership is unclear; response depends on individuals; evidence is incomplete |
| 2 | Defined | Owners, basic monitoring and recurring procedures exist but vary by service |
| 3 | Managed | SLOs, readiness gates, tested runbooks and change controls are consistently applied |
| 4 | Measured | Error budgets, trends, risk and cost/reliability tradeoffs drive priorities |
| 5 | Adaptive | Safe automation, continuous verification and learning systematically reduce risk |

## Assessment domains

Score each domain from 1 to 5 and attach evidence.

| Domain | Evidence examples |
|---|---|
| Ownership | Service catalog, RACI, on-call test |
| Reliability objectives | Versioned SLI/SLO and error-budget policy |
| Observability | Coverage map, tested alerts, telemetry-quality checks |
| Performance and capacity | Baselines, forecasts, queueing/regression review |
| Pipeline and data reliability | Freshness/correctness measures, replay tests |
| Security reliability | Access review, break-glass test, policy exceptions |
| Change safety | Deployment evidence, rollback tests, drift findings |
| Incident/problem management | Incident metrics, RCAs, recurring-failure reduction |
| Recovery | RPO/RTO mapping and full exercise results |
| Cost reliability | Attribution, anomaly response and guardrail evidence |
| Automation | Bounded remediation, audit trail and automatic verification |

## Scoring rules

- Use the lowest level whose required practice is not consistently demonstrated; do not average away a critical missing control.
- Tier 0 and Tier 1 services should define mandatory minimums by domain.
- A level requires repeatable evidence across the assessment period, not a single successful example.
- Security, compliance and recovery gaps can block production regardless of the overall score.

## Improvement backlog

For every gap, record:

1. risk and affected service;
2. current and target level;
3. control or outcome to implement;
4. accountable owner and delivery date;
5. verification evidence;
6. residual risk and exception expiry.

Prioritize work using business impact, likelihood, time to detect, time to recover and control effectiveness. Avoid prioritizing solely by ease of implementation.

## Quarterly review output

- domain scores and evidence changes;
- top reliability risks and overdue exceptions;
- SLO/error-budget trend;
- incident recurrence and corrective-action closure;
- recovery exercise results;
- capacity and cost forecast;
- next-quarter reliability commitments.

## Official references

The maturity levels are an enterprise DBRE framework, not a Snowflake product model. Product-specific evidence should be validated against:

- [Snowflake monitoring documentation](https://docs.snowflake.com/en/user-guide/monitoring)
- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Business continuity and disaster recovery](https://docs.snowflake.com/en/user-guide/replication-intro)
- [Cost management](https://docs.snowflake.com/en/user-guide/cost-management-overview)

