# Runbook: Telemetry Gap

Version: v1.3.0  
Status: Production Release  
Last vendor validation: 2026-08-15

## Trigger

- dashboard freshness exceeds its contract;
- expected records are absent or incomplete;
- Account Usage, Information Schema and curated data disagree materially;
- monitoring query, task or materialization fails;
- service state is reported healthy without current evidence.

## Procedure

1. Mark affected panels and dependent SLOs as delayed, incomplete or unknown.
2. Record last trustworthy event time, load time and query ID.
3. Check documented source latency, retention, privileges and edition requirements.
4. Validate the source with a bounded query using explicit columns.
5. Inspect the monitoring pipeline, task history, warehouse and recent changes.
6. Compare an independent source where semantics and time windows overlap.
7. Restore the collection/materialization path using its rollback procedure.
8. Backfill only after verifying idempotency, range and cost impact.
9. Reconcile the repaired period and recalculate affected objectives.
10. Document blind-window operational decisions and corrective actions.

## Safety

Do not interpret missing telemetry as zero activity. Do not silently substitute a source with different semantics. Avoid unbounded backfills against large usage views.

## Escalation

Escalate to the monitoring owner for pipeline failure, security for lost privileges, the service owner for decision risk, and Snowflake Support when source behavior contradicts documented expectations with reproducible evidence.

## References

- [Metric data contracts](../dashboards/metric-data-contracts.md)
- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
- [ALERT_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/alert_history)

