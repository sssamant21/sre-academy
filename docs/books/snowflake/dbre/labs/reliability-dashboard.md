# Lab: Design a DBRE Reliability Dashboard

Version: v1.3.0  
Status: Production Release  
Audience: DBRE and observability engineers  
Duration: 75 minutes  
Cost risk: Low  
Required privileges: Read-only telemetry access or synthetic data  
Last vendor validation: 2026-08-16

## Objective

Design a decision-oriented dashboard with service state, SLO/error-budget context, contributing signals and telemetry-quality indicators.

## Procedure

1. Select one cataloged service and one operational decision.
2. Define the customer-impact SLI and error-budget panels.
3. Add only contributing signals required to distinguish likely failure modes.
4. Add recent change and incident annotations.
5. Display source event time, pipeline completion and current metric-quality state.
6. Create a data contract for every panel: formula, source, scope, latency, retention, owner and runbook.
7. Define drill-down dimensions without exposing sensitive data.
8. Conduct a tabletop test for healthy, active-impact and stale-telemetry states.

## Required dashboard behavior

| State | Expected presentation |
|---|---|
| Healthy and current | Objective, remaining budget and supporting evidence |
| Impact detected | Severity, affected service, runbook and owner |
| Telemetry delayed | Unknown/delayed state, last trustworthy time and manual verification path |
| Mixed services | Separate results when eligibility or objectives differ |

## Success criteria

- the dashboard answers a named decision within one minute;
- unknown data is not shown as healthy;
- each alertable panel links to a runbook;
- calculations are reproducible from the data contracts.

## References

- [DBRE dashboard specifications](../dashboards/dashboard-specifications.md)
- [Metric data contracts](../dashboards/metric-data-contracts.md)
- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)

