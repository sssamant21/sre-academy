# DBRE Reliability Simulations

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-16

These tabletop simulations test DBRE decisions and management-system controls. Participants use synthetic evidence; they do not create failures in production.

| Simulation | Primary challenge | Core decision |
|---|---|---|
| [Rapid error-budget burn](rapid-error-budget-burn.md) | A critical SLO burns while technical signals disagree | Validate impact and restrict risk without premature remediation |
| [Observability blind spot](observability-blind-spot.md) | Dashboard data is stale during reported customer impact | Operate safely when monitoring cannot establish truth |
| [Recovery-readiness gap](recovery-readiness-gap.md) | Replication is healthy but an exercise cannot restore service | Reconcile platform success with end-to-end RPO/RTO failure |

## Roles

- incident commander;
- DBRE lead;
- service/workload owner;
- observability or recovery specialist;
- security/FinOps partner as applicable;
- facilitator and scribe.

## Submission

Teams provide a UTC timeline, evidence table, impact statement, decision log, mitigation/rollback criteria, communication and corrective actions.

## Safety

- No production changes, failover, cancellation, workload generation or access-policy modifications.
- Do not expose credentials, query text or sensitive identities.
- Treat every inject as evidence requiring validation, not as facilitator-confirmed truth.

## References

- [DBRE reliability runbooks](../runbooks/index.md)
- [Existing Snowflake incident simulations](../../labs/simulations/index.md)

