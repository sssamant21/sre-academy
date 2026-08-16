# DBRE Reliability Runbooks

Version: v1.3.0  
Status: Production Release  
Last vendor validation: 2026-08-15

These runbooks protect the DBRE management system. Technical incidents should use the existing production runbooks for warehouse queueing, query regression, pipeline failure, connectivity, dynamic-table freshness and unexpected cost.

| Runbook | Trigger |
|---|---|
| [SLO and error-budget burn](slo-and-error-budget-burn.md) | A service breaches or rapidly consumes its reliability budget |
| [Telemetry gap](telemetry-gap.md) | Required evidence is delayed, incomplete or unavailable |
| [Alert-quality failure](alert-quality-failure.md) | Alerts miss impact, fire without action or repeatedly fail |
| [Recovery-readiness risk](recovery-readiness-risk.md) | Replication/exercise evidence indicates RPO/RTO risk |
| [Configuration drift](configuration-drift.md) | Production state differs from the approved baseline |

## Common response contract

1. Confirm the affected service, owner, objective and criticality.
2. Record UTC timestamps, source freshness and current change context.
3. Preserve evidence before modifying configuration.
4. Separate customer impact from monitoring/control failure.
5. Prefer bounded and reversible mitigation.
6. Define verification, rollback and escalation before action.
7. Create a time-bound corrective action for systemic gaps.

## Official references

- [Alerts and notifications](https://docs.snowflake.com/en/guides-overview-alerts)
- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Business continuity and disaster recovery](https://docs.snowflake.com/en/user-guide/replication-intro)

