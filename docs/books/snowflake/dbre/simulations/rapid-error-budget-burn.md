# Simulation: Rapid Error-Budget Burn

Version: v1.3.0  
Status: Production Release  
Duration: 60–75 minutes  
Last vendor validation: 2026-08-16

## Situation

A Tier 1 reporting service has consumed 60% of its monthly error budget in two hours. Query success remains high, latency breaches are concentrated in one workload, and a warehouse change occurred shortly before impact.

## Objectives

- validate SLI scope and telemetry before declaring cause;
- separate customer impact, queueing, query regression and measurement defect;
- apply the error-budget policy and choose a safe technical path;
- produce measurable recovery criteria.

## Injects

1. Dashboard shows high burn, but Account Usage data is delayed.
2. A lower-latency bounded query confirms queueing for one workload class.
3. Change record shows a warehouse policy modification without post-change evidence.
4. Service owner requests an immediate global resize.
5. FinOps reports the current warehouse is already above baseline.

## Expected decisions

- verify the objective and impact using an independent source;
- use the warehouse-queueing or query-regression runbook based on evidence;
- avoid a global resize without isolation, rollback and cost analysis;
- restrict discretionary risk according to the budget policy;
- verify recovery through customer outcome and SLI trend.

## Completion evidence

Timeline, burn calculation, cause hypothesis table, selected runbook, change decision, rollback, customer message and corrective actions.

## References

- [SLO-burn runbook](../runbooks/slo-and-error-budget-burn.md)
- [Warehouse-queueing runbook](../../runbooks/warehouse-queuing.md)
- [QUERY_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)

