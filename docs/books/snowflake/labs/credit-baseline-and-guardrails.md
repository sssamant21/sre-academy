# Lab: Credit Baseline and Cost Guardrails

Version: v1.1.0  
Status: Vendor-validated lab  
Last vendor validation: 2026-08-15

## Objective

Create a bounded warehouse-credit baseline, identify major consumers and evaluate an appropriate guardrail without modifying production controls.

## Safety and prerequisites

- Duration: approximately 20–30 minutes.
- Cost risk: low, read-only metadata analysis.
- Required access: an analysis warehouse and access to `SNOWFLAKE.ACCOUNT_USAGE`.
- Resource monitors apply to warehouses. They do not cover serverless features or AI services; use budgets or the appropriate usage views for those costs.

## Build the baseline

```sql
SELECT
  WAREHOUSE_NAME,
  SUM(CREDITS_USED_COMPUTE) AS COMPUTE_CREDITS,
  SUM(CREDITS_USED_CLOUD_SERVICES) AS CLOUD_SERVICES_CREDITS,
  SUM(CREDITS_USED) AS TOTAL_CREDITS
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY WAREHOUSE_NAME
ORDER BY TOTAL_CREDITS DESC;
```

Review existing monitors:

```sql
SHOW RESOURCE MONITORS;
```

If authorized, compare the baseline with the `SNOWFLAKE.ACCOUNT_USAGE.RESOURCE_MONITORS` view. Account Usage views can have latency, so do not treat them as real-time enforcement signals.

## Design exercise

For one non-production warehouse, document:

- historical daily and monthly consumption;
- business criticality and acceptable interruption;
- notification owners and escalation path;
- warning thresholds;
- whether suspension is permissible;
- rollback and emergency override ownership.

Do not create or attach a monitor until an account administrator approves the quota and actions. Only `ACCOUNTADMIN` can create a resource monitor, though privileges can be delegated for some management operations.

## Success criteria

- The baseline uses a bounded time range.
- Warehouse costs are separated from unsupported serverless and AI-service coverage.
- Proposed thresholds are tied to historical usage and business impact.
- Suspension behavior has an owner, escalation path and rollback decision.

## Official references

- [Working with resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [CREATE RESOURCE MONITOR](https://docs.snowflake.com/en/sql-reference/sql/create-resource-monitor)
- [RESOURCE_MONITORS Account Usage view](https://docs.snowflake.com/en/sql-reference/account-usage/resource_monitors)
