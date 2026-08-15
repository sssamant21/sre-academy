# Integrated Reliability Controls

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-15

DBRE integrates existing engineering controls around a service's approved reliability objectives. This page is a control map; detailed procedures remain in the linked handbook chapters and runbooks.

## Control domains

| Domain | Preventive controls | Detective controls | Recovery controls |
|---|---|---|---|
| Capacity | Workload isolation, sizing baseline, concurrency policy | Queueing and load trend | Reversible resize, scale-out or workload shift |
| Query performance | Review, representative test, pruning and plan evidence | Regression baseline, Query Profile | Rollback SQL/configuration; isolate workload |
| Pipelines | Idempotency, dependency and retry design | Task/refresh history, freshness SLI | Controlled replay, resume or rebuild |
| Access | Least privilege, SSO/MFA and network controls | Login/access history and exception review | Break-glass process and access restoration |
| Change | Version control, test, approval and rollback | Deployment verification and drift detection | Rollback or forward correction |
| Recovery | Replication/failover design and dependency inventory | Replication lag and exercise findings | Approved failover/failback procedure |
| Cost | Warehouse policy, budgets and resource monitors | Metering and anomaly detection | Suspend/resize after impact assessment |

## Capacity and performance

Do not use warehouse resizing as the default response to every slow query. Separate queueing, compilation, scanning, data movement, spill and external dependency time. Establish a representative baseline and link every capacity change to workload SLOs and cost impact.

## Pipeline reliability

Task success is not equivalent to data correctness or freshness. Monitor schedule completion, graph dependencies, retries, duration, output validation and downstream visibility. For dynamic tables, distinguish target lag from a guaranteed refresh interval and monitor refresh outcomes and actual freshness.

## Recovery engineering

Time Travel, Fail-safe and replication serve different purposes. A documented recovery design must identify eligible objects, edition/region requirements, dependencies, refresh schedule, expected data loss, promotion steps, application rerouting and failback. Exercise the complete customer procedure rather than only checking that a secondary exists.

Failover groups support promotion; replication groups provide read-only replicated objects without failover capability. Account-object failover is a Business Critical Edition feature or higher at the time of validation.

## Cost reliability

Unexpected consumption can create operational and financial impact. Resource monitors focus on user-managed warehouses, whereas budgets can cover supported warehouses and serverless features. A suspend action can itself cause an availability incident; thresholds and responders must reflect service criticality.

## Automation progression

1. **Observe:** collect evidence without action.
2. **Recommend:** generate a bounded, reviewable remediation.
3. **Approve:** require a human decision and record the change.
4. **Automate:** execute only proven, reversible actions with scope controls.
5. **Verify:** measure recovery and stop escalation loops.

## Official references

- [Query Profile](https://docs.snowflake.com/en/user-guide/ui-query-profile)
- [Troubleshoot task graphs](https://docs.snowflake.com/en/user-guide/tasks-graphs-troubleshooting)
- [Monitor dynamic tables](https://docs.snowflake.com/en/user-guide/dynamic-tables/monitoring)
- [Business continuity and disaster recovery](https://docs.snowflake.com/en/user-guide/replication-intro)
- [Failover and failback](https://docs.snowflake.com/en/user-guide/account-replication-failover-failback)
- [Managing cost](https://docs.snowflake.com/en/user-guide/cost-management-overview)

