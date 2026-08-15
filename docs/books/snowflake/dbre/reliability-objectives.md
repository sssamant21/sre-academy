# SLIs, SLOs and Error Budgets

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-15

## Reliability objective hierarchy

- **SLI:** measured service behavior, such as successful critical task runs.
- **SLO:** internal target for an SLI over a defined scope and window.
- **Error budget:** permitted unreliability derived from the SLO.
- **Alert:** a response trigger based on impact or credible risk, not a substitute for the SLO.
- **SLA:** a contractual commitment; do not infer one from an internal SLO.

## Candidate Snowflake workload SLIs

| Reliability dimension | Example SLI | Evidence source |
|---|---|---|
| Query success | Successful eligible queries / eligible queries | `QUERY_HISTORY` |
| Query latency | Percentage of eligible queries below a threshold | `QUERY_HISTORY` |
| Queueing | Percentage below approved overload wait | `QUERY_HISTORY`, `WAREHOUSE_LOAD_HISTORY` |
| Pipeline execution | Successful critical runs / scheduled runs | `TASK_HISTORY` |
| Data freshness | Percentage of observations within approved age | application watermark or refresh history |
| Dynamic-table health | Successful eligible refreshes / refreshes | `DYNAMIC_TABLE_REFRESH_HISTORY` |
| Authentication | Successful eligible login attempts / attempts | `LOGIN_HISTORY` |
| Recovery | Exercises meeting approved RPO and RTO | controlled exercise evidence |

Snowflake telemetry has different latency and retention characteristics. The SLI specification must name the exact view or function, filters, latency allowance, exclusions, timezone and aggregation.

## SLO specification template

Every SLO should include:

1. service and consumer scope;
2. SLI formula and data source;
3. objective and measurement window;
4. eligible and excluded events;
5. telemetry latency and completeness checks;
6. error-budget calculation;
7. burn-rate or threshold response;
8. owner, reviewer and review cadence;
9. version and effective date.

## Error-budget calculation

For an event-based SLO:

`allowed bad events = eligible events × (1 − SLO target)`

For a 99.9% target across 1,000,000 eligible events, the budget is 1,000 bad events. Do not convert event-based objectives into downtime unless the service measurement is genuinely time-based.

## Error-budget policy

| Budget state | Expected decision |
|---|---|
| Healthy | Normal delivery with standard controls |
| Elevated burn | Investigate causes and reduce high-risk change |
| At risk | Prioritize reliability work and require stronger approval |
| Exhausted | Pause discretionary risk, document exceptions and restore reliability |

Error budgets guide decisions; they do not authorize unsafe action or override security, compliance or contractual obligations.

## Measurement pitfalls

- Mixing interactive, batch and administrative queries into one latency objective.
- Treating delayed Account Usage data as real-time paging telemetry.
- Excluding failures after observing the result.
- Measuring task success while ignoring missed schedules or stale output.
- Aggregating services in a way that hides a critical consumer's failure.
- setting objectives without a named response when the budget burns.

## Official references

- [QUERY_HISTORY view](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)
- [WAREHOUSE_LOAD_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/warehouse_load_history)
- [TASK_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/task_history)
- [Monitor dynamic tables](https://docs.snowflake.com/en/user-guide/dynamic-tables/monitoring)
- [LOGIN_HISTORY view](https://docs.snowflake.com/en/sql-reference/account-usage/login_history)

