# DBRE Dashboard Specifications

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-15

## 1. Service reliability dashboard

| Panel | Required dimensions | Required response |
|---|---|---|
| SLO attainment | Service, SLI, window | Open objective definition and owner |
| Error-budget remaining | Service and window | Apply error-budget policy |
| Burn rate | Short and long window | Run SLO-burn procedure |
| Impacting events | Incident, deployment, dependency | Correlate change and impact |
| Telemetry quality | Source, freshness, completeness | Run telemetry-gap procedure |

Never combine services with different eligibility rules into a single unqualified SLO percentage.

## 2. Workload and capacity dashboard

Minimum panels:

- query volume, success, latency percentiles and queue time by service/workload;
- running, queued overload, queued provisioning and blocked load;
- warehouse size, cluster count and relevant configuration changes;
- top regressing query patterns with representative query IDs;
- spill, scan and pruning evidence where curated from operator analysis;
- credits alongside workload and SLO results.

The dashboard should distinguish queueing from slow execution. It must not recommend resizing without workload, performance and cost context.

## 3. Pipeline and freshness dashboard

Minimum panels:

- critical schedule completion and missed-run detection;
- task-graph failures, retries and duration trend;
- dynamic-table refresh status, duration and actual freshness;
- ingestion errors and delayed files/events where applicable;
- data-quality or business-watermark results;
- downstream dependency impact and replay readiness.

Task or refresh success alone is not proof that delivered data is complete or correct.

## 4. Security reliability dashboard

Minimum panels:

- login success/failure by approved dimensions;
- authentication method and client changes;
- privileged or unusual access signals;
- policy/integration health and recent changes;
- unresolved access exceptions and break-glass usage;
- telemetry freshness and edition-dependent coverage.

`ACCESS_HISTORY` requires Enterprise Edition or higher. Restrict dashboard access and avoid exposing sensitive identity or query information unnecessarily.

## 5. Recovery-readiness dashboard

Minimum panels:

- protected service and approved RPO/RTO;
- last successful replication/failover-group refresh;
- refresh duration, bytes, object count and failures;
- estimated recovery-point exposure based on the latest verified data;
- last exercise result, next due date and open corrective actions;
- non-replicated dependency and application-rerouting readiness.

A successful refresh does not prove that end-to-end recovery or failback will meet objectives.

## 6. Cost-reliability dashboard

Minimum panels:

- service and warehouse consumption versus approved baseline;
- cost per successful workload unit where attribution is defensible;
- resource-monitor and budget state;
- query/workload contributors to material variance;
- SLO impact alongside cost changes;
- forecast, anomaly owner and active optimization work.

Resource monitors focus on warehouses; budgets can monitor supported warehouses and serverless features. Document coverage gaps.

## Official references

- [TASK_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/task_history)
- [Monitor dynamic tables](https://docs.snowflake.com/en/user-guide/dynamic-tables/monitoring)
- [LOGIN_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/login_history)
- [ACCESS_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/access_history)
- [Replication refresh history](https://docs.snowflake.com/en/sql-reference/account-usage/replication_group_refresh_history)
- [Cost attribution](https://docs.snowflake.com/en/user-guide/cost-attributing)

