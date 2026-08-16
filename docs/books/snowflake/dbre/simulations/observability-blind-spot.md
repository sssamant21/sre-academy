# Simulation: Observability Blind Spot

Version: v1.3.0  
Status: In development  
Duration: 60 minutes  
Last vendor validation: 2026-08-16

## Situation

Consumers report missing morning data while the DBRE dashboard shows all services healthy. The dashboard's curated dataset has not refreshed for 95 minutes, and the freshness indicator was removed during a recent redesign.

## Objectives

- recognize that missing telemetry is not healthy telemetry;
- establish customer impact through alternate evidence;
- restore monitoring without unsafe backfill;
- identify design and alert-coverage corrections.

## Injects

1. Dashboard screenshot shows green status with no source timestamp.
2. Monitoring task history shows a privilege-related failure.
3. Direct task history shows one critical pipeline failure.
4. A proposed fix grants a broad administrative role to the monitoring task.
5. The backfill query has no time bound.

## Expected decisions

- mark status unknown and communicate the blind window;
- use least-privilege correction through change control;
- invoke the pipeline-failure runbook for the customer issue;
- bound and reconcile any backfill;
- restore freshness/completeness indicators and test the alert.

## Completion evidence

Impact statement, alternate evidence, privilege-safe correction, bounded recovery plan, reconciliation and prevention backlog.

## References

- [Telemetry-gap runbook](../runbooks/telemetry-gap.md)
- [TASK_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/task_history)
- [Account Usage latency](https://docs.snowflake.com/en/sql-reference/account-usage)

