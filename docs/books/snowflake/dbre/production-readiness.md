# DBRE Production-Readiness Standard

Version: v1.3.0  
Status: Production Release  
Last vendor validation: 2026-08-15

Use this standard before a new Snowflake service enters production and after a material architecture, workload, security or recovery change. Record evidence and approved exceptions; a checked box without evidence is not acceptance.

## Gate 1: ownership and scope

- [ ] Business and technical owners are named.
- [ ] On-call and escalation paths are tested.
- [ ] Service boundary, consumers and dependencies are documented.
- [ ] Criticality and data classification are approved.

## Gate 2: objectives and telemetry

- [ ] SLIs and SLOs have formulas, sources, windows and exclusions.
- [ ] Telemetry latency and retention are suitable for each decision.
- [ ] Dashboards show consumer impact and contributing platform signals.
- [ ] Alerts are actionable, routed and tested.
- [ ] Error-budget policy names decision owners.

## Gate 3: performance and capacity

- [ ] Representative workload tests meet approved objectives.
- [ ] Warehouse isolation, size, scaling and suspension policies are justified.
- [ ] Query regression and queueing baselines are retained.
- [ ] Capacity and growth thresholds have owners and lead time.

## Gate 4: pipelines and data correctness

- [ ] Task, stream, pipe and dynamic-table dependencies are documented.
- [ ] Retry, replay and idempotency behavior is tested.
- [ ] Freshness, completeness and correctness checks are defined.
- [ ] Schema-change and downstream compatibility controls exist.

## Gate 5: security and governance

- [ ] Least-privilege roles and ownership are reviewed.
- [ ] Authentication, network and break-glass paths are tested.
- [ ] Sensitive-data policies and audit evidence meet requirements.
- [ ] Secrets and integrations have rotation and revocation procedures.

## Gate 6: recovery

- [ ] RPO and RTO are approved and mapped to a feasible design.
- [ ] Replicated and non-replicated dependencies are identified.
- [ ] Recovery, rerouting and failback procedures are exercised.
- [ ] Exercise results meet objectives or have accepted corrective actions.

## Gate 7: change and operations

- [ ] Deployment, verification and rollback are automated or documented.
- [ ] Runbooks use explicit scope, UTC evidence and safety gates.
- [ ] Incident command and vendor-escalation paths are documented.
- [ ] Configuration drift and unsupported manual changes are detected.

## Gate 8: cost and lifecycle

- [ ] Cost owner, tags/attribution and expected baseline are documented.
- [ ] Budgets or resource-monitor controls match the consumption model.
- [ ] Retention, archival and decommissioning are defined.
- [ ] Suspension controls have been assessed for availability impact.

## Decision

| Result | Meaning |
|---|---|
| Approved | Required controls and evidence meet policy |
| Approved with conditions | Time-bound exceptions have owners and due dates |
| Not approved | Material reliability risk remains unresolved |

The approver must record the service version, evidence links, exceptions, compensating controls, expiry date and next review.

## Related handbook assets

- [Production-readiness review template](../templates/production-readiness-review.md)
- [Production-readiness exercise](../labs/production-readiness-exercise.md)
- [Incident and RCA template](../templates/incident-and-rca.md)

## Official references

- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Access-control overview](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
- [Business continuity and disaster recovery](https://docs.snowflake.com/en/user-guide/replication-intro)
- [Cost-management overview](https://docs.snowflake.com/en/user-guide/cost-management-overview)

