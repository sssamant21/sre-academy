# Runbook: Alert-Quality Failure

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-15

## Trigger

- customer impact occurs without an alert;
- repeated alerts do not require action;
- alert execution or notification delivery fails;
- routing reaches the wrong or unavailable owner;
- an alert condition is based on stale telemetry.

## Procedure

1. Confirm whether active customer impact requires incident command.
2. Preserve alert definition, execution history, notification evidence and recent changes.
3. Classify the failure: detection, condition, schedule, execution, delivery, routing or response.
4. Verify the source data and latency independently.
5. Check alert state; newly created or cloned SQL alerts are suspended until resumed.
6. Validate privileges, warehouse/serverless execution context and notification integration.
7. Apply a temporary manual watch with a named owner and expiry.
8. Correct the alert through change control and test a controlled qualifying event.
9. Confirm delivery, acknowledgement, runbook link and escalation.
10. Review duplicates, thresholds and coverage before closing.

## Safety

Do not create automated destructive actions as a quick alert fix. Restrict notification destinations and avoid placing sensitive values in payloads.

## References

- [Setting up alerts](https://docs.snowflake.com/en/user-guide/alerts)
- [CREATE ALERT](https://docs.snowflake.com/en/sql-reference/sql/create-alert)
- [Notifications](https://docs.snowflake.com/en/user-guide/notifications/about-notifications)
- [ALERT_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/alert_history)

