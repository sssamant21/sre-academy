# DBRE Operational Dashboards

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-15

DBRE dashboards turn Snowflake telemetry and service context into operational decisions. They supplement the observability architecture in Chapter 13; they do not redefine Snowflake system-view semantics.

## Dashboard set

| Dashboard | Decision it supports | Primary owner |
|---|---|---|
| Service reliability | Is each service meeting its SLO, and where is budget burning? | DBRE and service owner |
| Workload and capacity | Is latency caused by demand, queueing, configuration or query behavior? | DBRE and performance engineering |
| Pipeline and freshness | Are critical data products complete, current and recoverable? | Data engineering and DBRE |
| Security reliability | Are authentication, access and control failures affecting service? | Security and DBRE |
| Recovery readiness | Can approved RPO/RTO objectives still be met? | DBRE and architecture |
| Cost reliability | Is consumption within the approved service baseline and guardrails? | FinOps and DBRE |

See [dashboard specifications](dashboard-specifications.md) and [metric data contracts](metric-data-contracts.md).

## Design principles

- Design around a named decision, owner and response.
- Separate customer-impact indicators from contributing platform signals.
- Display telemetry freshness and completeness with every time-sensitive panel.
- Preserve service, account, environment, warehouse and workload dimensions.
- Use UTC internally and label any presentation-time conversion.
- Link every actionable condition to a runbook and escalation policy.
- Test calculations against source telemetry and controlled events.

## Standard page layout

1. current service state and active incidents;
2. SLO attainment and error-budget burn;
3. leading indicators and dependency health;
4. recent changes and annotations;
5. capacity/cost context;
6. telemetry freshness and known gaps;
7. runbooks, owner and escalation links.

## Official references

- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Alerts and notifications](https://docs.snowflake.com/en/guides-overview-alerts)
- [QUERY_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)
- [WAREHOUSE_LOAD_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_load_history)

