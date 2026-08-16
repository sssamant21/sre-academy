# Snowflake DBRE Practical Labs

Version: v1.3.0  
Status: Production Release  
Last vendor validation: 2026-08-16

These labs convert the DBRE operating model into reviewable operational artifacts. They are designed for a sandbox, non-production account, or tabletop evidence pack.

| Lab | Duration | Primary output |
|---|---:|---|
| [Build a service profile](service-profile.md) | 60 minutes | Owned service catalog record |
| [Define an SLO and error budget](slo-and-error-budget.md) | 75 minutes | Versioned objective and response policy |
| [Design a reliability dashboard](reliability-dashboard.md) | 75 minutes | Dashboard and metric data contracts |
| [Validate telemetry quality](telemetry-quality.md) | 60 minutes | Freshness/completeness test report |
| [Assess recovery readiness](recovery-readiness.md) | 90 minutes | RPO/RTO evidence and risk register |
| [Run a production-readiness review](production-readiness-review.md) | 90 minutes | Approval decision with exceptions |

## Safety contract

- Do not use production credentials or alter production objects.
- Use read-only metadata where possible and bound all history queries.
- Use synthetic evidence when the required feature, edition or secondary account is unavailable.
- Do not initiate failover, suspend shared warehouses, change policies or replay workloads.
- Redact identities, query text and sensitive object names from submitted evidence.
- Record measured results as account-specific observations, not universal guarantees.

## Completion package

Each lab produces an artifact, evidence table, assumptions, risks, owner, review date and links to official Snowflake documentation.

## Official references

- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Access-control overview](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
- [Business continuity and disaster recovery](https://docs.snowflake.com/en/user-guide/replication-intro)

