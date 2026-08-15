# Simulation: Unexpected Credit Spike

Version: v1.2.0  
Status: Vendor-validated simulation  
Last vendor validation: 2026-08-15

## Objective

Attribute a credit anomaly, contain avoidable consumption and preserve critical workloads.

## Scenario

Hourly warehouse credits are five times the approved baseline. No customer-facing incident has been reported yet.

## Safety

Do not create a real consumption spike. Do not suspend a critical warehouse or change resource-monitor actions without incident and business authority.

## Facilitator injects

| Time | Inject |
|---|---|
| T+0 | FinOps alert identifies a fivefold hourly variance |
| T+5 | One batch warehouse accounts for most additional credits |
| T+10 | Query History shows duplicate scheduled submissions |
| T+15 | The task owner confirms a deployment introduced overlapping schedules |
| T+20 | The workload is safe to pause; an interactive warehouse must remain available |
| T+25 | Account Usage data is delayed relative to current activity |

## Evidence participants must request

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

Request schedule changes, task history, query tags, resource-monitor coverage and the business criticality map.

## Decisions

1. Attribute the anomaly before containment.
2. Pause only the confirmed duplicate non-critical submission path.
3. Explain Account Usage latency and define a near-real-time validation source.
4. Decide whether guardrail thresholds or deployment tests need correction.
5. Separate warehouse controls from serverless and AI-service budgets.

## Success criteria

- Critical workloads are protected.
- The containment target is specific and owned.
- Expected savings are not claimed until telemetry confirms them.
- Corrective actions address schedule duplication and detection.

## Official references

- [Working with resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [WAREHOUSE_METERING_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history)
- [TASK_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/task_history)
