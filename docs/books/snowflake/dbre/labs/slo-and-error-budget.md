# Lab: Define an SLO and Error Budget

Version: v1.3.0  
Status: In development  
Audience: DBRE, SRE and service owners  
Duration: 75 minutes  
Cost risk: Low  
Required privileges: Read access to an approved telemetry source, or synthetic data  
Last vendor validation: 2026-08-16

## Objective

Create a measurable workload SLO, calculate an error budget and define actions for elevated burn and exhaustion.

## Scenario

The reporting service is called “available” when Snowflake is reachable, but consumers care whether eligible reports complete successfully within an agreed latency.

## Procedure

1. Write the consumer outcome and service boundary.
2. Select one event-based SLI: successful eligible executions within the threshold divided by eligible executions.
3. Define eligible workload, result states, latency threshold and exclusions before inspecting results.
4. Choose the measurement window and internal target with the service owner.
5. Document exact source, event timestamp, expected latency, retention and timezone.
6. Calculate permitted bad events: `eligible × (1 − objective)`.
7. Define healthy, elevated, at-risk and exhausted budget responses.
8. Test the formula using synthetic or bounded historical data.
9. Record limitations and a version/effective date.

## Worked calculation

For 200,000 eligible executions and a 99.5% objective, the budget is 1,000 bad executions. This is an event budget; it should not be represented as downtime.

## Success criteria

- a second reviewer can reproduce the result;
- exclusions are predefined and auditable;
- telemetry delay is visible;
- every budget state has a named decision owner;
- internal SLO language is not confused with Snowflake's contractual SLA.

## References

- [DBRE reliability objectives](../reliability-objectives.md)
- [QUERY_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)
- [TASK_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/task_history)

