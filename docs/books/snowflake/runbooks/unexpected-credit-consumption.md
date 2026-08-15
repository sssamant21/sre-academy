# Runbook: Unexpected Credit Consumption

Version: v1.1.0  
Status: Vendor-validated runbook  
Last vendor validation: 2026-08-15

## Trigger

Use this runbook when warehouse credit consumption materially exceeds the approved baseline or forecast.

## Immediate safety

- Identify the financial and service owner.
- Do not immediately suspend a business-critical warehouse without incident authority.
- Preserve metering, query and warehouse configuration evidence.
- Distinguish warehouse consumption from serverless features and AI services; resource monitors cover warehouses, not those other services.

## Evidence

```sql
SELECT
  WAREHOUSE_NAME,
  DATE_TRUNC('hour', START_TIME) AS HOUR,
  SUM(CREDITS_USED_COMPUTE) AS COMPUTE_CREDITS,
  SUM(CREDITS_USED_CLOUD_SERVICES) AS CLOUD_SERVICES_CREDITS,
  SUM(CREDITS_USED) AS TOTAL_CREDITS
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY WAREHOUSE_NAME, DATE_TRUNC('hour', START_TIME)
ORDER BY HOUR DESC, TOTAL_CREDITS DESC;
```

Correlate the anomaly with query history, scheduled tasks, warehouse configuration changes, auto-suspend behavior and workload releases. Use bounded time ranges and account for telemetry latency.

## Decision points

- **Expected workload growth:** confirm ownership, forecast and budget.
- **Idle-running warehouse:** verify auto-suspend eligibility and session behavior.
- **Repeated or failed workload:** stop only the responsible submission path when safe.
- **Oversized warehouse:** compare performance and cost using a controlled test before resizing.
- **Serverless or AI consumption:** use the appropriate budget and service-specific usage history rather than relying on a warehouse resource monitor.

## Mitigation options

1. Pause a confirmed runaway non-critical workload.
2. Correct scheduling duplication or retry storms.
3. Apply an approved warehouse size or auto-suspend change.
4. Route workloads to the correct isolated warehouse.
5. Create or revise resource-monitor notifications and actions through approved account administration.

## Validation and rollback

Track consumption and service indicators over multiple intervals. Roll back configuration changes if they increase latency, queueing or failure rates. Assign an expiry time to temporary limits.

## Escalation package

Include the UTC incident window, warehouses, credit baseline, metering evidence, representative query IDs, recent configuration or release changes and the actions taken. Exclude secrets and private keys.

## Official references

- [Working with resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [QUERY_HISTORY Account Usage view](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)
- [WAREHOUSE_LOAD_HISTORY Account Usage view](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_load_history)
