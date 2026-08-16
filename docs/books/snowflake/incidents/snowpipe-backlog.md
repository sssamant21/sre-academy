# Case Study: Snowpipe Backlog and Missing Files

Version: v1.5.0
Status: In development
Last vendor validation: 2026-08-16

Fictional composite; all names and times are illustrative.

## Incident

The `ORDERS_PIPE` freshness SLO breached at 09:20 UTC. Objects continued arriving in cloud storage, but the landing table's newest source timestamp remained at 08:52. Dashboards were held rather than publishing incomplete totals.

## Evidence sequence

```sql
SELECT SYSTEM$PIPE_STATUS('RAW.INGEST.ORDERS_PIPE');

SELECT *
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
  TABLE_NAME => 'RAW.INGEST.ORDERS_LANDING',
  START_TIME => DATEADD('hour', -4, CURRENT_TIMESTAMP())))
ORDER BY LAST_LOAD_TIME DESC;

SELECT *
FROM TABLE(INFORMATION_SCHEMA.VALIDATE_PIPE_LOAD(
  PIPE_NAME => 'RAW.INGEST.ORDERS_PIPE',
  START_TIME => DATEADD('hour', -4, CURRENT_TIMESTAMP())));
```

Responders found no recent queued files in pipe status and no copy attempts for objects visible under the expected stage prefix. That distinguished notification failure from file-format rejection. Cloud event delivery showed the subscription had been replaced during an infrastructure deployment with a prefix that excluded `orders/inbound/`.

## Timeline

| Time UTC | Event |
|---|---|
| 08:47 | Notification configuration deployment completed |
| 08:52 | Last file loaded |
| 09:20 | Freshness alert fired |
| 09:27 | Storage arrival confirmed; no COPY attempt found |
| 09:36 | Notification prefix mismatch identified |
| 09:44 | Correct subscription restored |
| 09:50 | Bounded pipe refresh/backfill initiated |
| 10:08 | File manifest and row controls reconciled |

## Root cause and contributors

Root cause: the cloud event subscription filter no longer matched the stage prefix monitored by the pipe. Contributors were missing infrastructure contract tests, no notification-delivery metric, and reliance on target-table freshness as the first alert.

## Recovery

The team restored the validated event subscription, then used the documented Snowpipe refresh/backfill procedure for the affected path and bounded time window. It reconciled object manifests, copy history, row counts and monetary controls before releasing dashboards. A broad replay or `FORCE` load was rejected because it could duplicate business rows.

## Corrective actions

- Test stage prefix, event filter and pipe definition together in CI.
- Alert independently on storage arrivals, notifications, copy attempts, load failures and table freshness.
- Retain an external delivery manifest beyond short Information Schema diagnostic windows.
- Require a bounded backfill plan and idempotent business-key reconciliation.
- Add the notification resource to production-readiness and drift reviews.

## Official references

- [Monitor Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-monitor)
- [`SYSTEM$PIPE_STATUS`](https://docs.snowflake.com/en/sql-reference/functions/system_pipe_status)
- [`COPY_HISTORY`](https://docs.snowflake.com/en/sql-reference/functions/copy_history)
- [`VALIDATE_PIPE_LOAD`](https://docs.snowflake.com/en/sql-reference/functions/validate_pipe_load)
