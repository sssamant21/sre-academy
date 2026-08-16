# Declarative Transformation with Dynamic Tables

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

## Use when

Use dynamic tables when the desired result is expressible as a supported `SELECT` and Snowflake should manage refresh scheduling. Use streams and tasks when explicit procedural branching or fine-grained event handling is required.

## Flow

```mermaid
flowchart LR
    A[Landing] --> B[Clean dynamic table]
    B --> C[Aggregate dynamic table]
    C --> D[Consumer view]
```

## Implementation

```sql
CREATE OR REPLACE DYNAMIC TABLE analytics.orders_clean
  TARGET_LAG = DOWNSTREAM
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
SELECT order_id, customer_id, order_ts, amount
FROM raw.orders
WHERE order_id IS NOT NULL;

CREATE OR REPLACE DYNAMIC TABLE analytics.daily_sales
  TARGET_LAG = '15 minutes'
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
AS
SELECT DATE_TRUNC('DAY', order_ts) AS sales_date,
       SUM(amount) AS gross_sales,
       COUNT(*) AS order_count
FROM analytics.orders_clean
GROUP BY sales_date;
```

`TARGET_LAG` is a best-effort staleness objective, not a fixed refresh interval or guarantee. Set `REFRESH_MODE` explicitly so recreation does not silently resolve `AUTO` differently.

## Production controls

- Test whether every operator supports the selected refresh mode before deployment.
- Monitor actual lag, refresh duration, status, rows changed and credits; alert on skipped, failed or increasingly slow refreshes.
- Give intermediate tables `DOWNSTREAM` lag when only leaf consumers define freshness.
- Isolate refresh compute and tune from measured change volume and query profile.
- Suspend affected tables before incompatible upstream DDL and plan reinitialization cost.

```sql
SELECT *
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME => 'ANALYTICS.DAILY_SALES', RESULT_LIMIT => 100));
```

## Validation and recovery

Compare a full source calculation with the dynamic-table result, verify late and corrected rows, then induce an upstream schema failure in non-production. If freshness breaches, inspect refresh history and upstream failures before resizing compute. For rollback, suspend the new pipeline and restore the prior consumer view; retain the old model until reconciliation succeeds.

## Official references

- [Dynamic tables overview](https://docs.snowflake.com/en/user-guide/dynamic-tables/overview)
- [Target lag](https://docs.snowflake.com/en/user-guide/dynamic-tables/target-lag)
- [Refresh modes](https://docs.snowflake.com/en/user-guide/dynamic-tables/refresh-modes)
- [Dynamic-table best practices](https://docs.snowflake.com/en/user-guide/dynamic-tables/best-practices)

