# Case Study: Unexpected Credit Consumption

Version: v1.5.0
Status: In development
Last vendor validation: 2026-08-16

Fictional composite; credit figures are illustrative.

## Incident

Daily Snowflake consumption exceeded forecast by 62%. No single business team reported a planned load increase. FinOps alerted the DBRE on-call before the monthly budget threshold was reached.

## Attribution sequence

1. Separate warehouse, serverless, cloud-services, AI and data-transfer categories.
2. Compare current consumption with the same weekday baseline.
3. Attribute warehouse growth by warehouse and hour.
4. Attribute workload using query history, task history and query tags.
5. Confirm whether the increase is legitimate volume, inefficient work, retry amplification or configuration drift.

```sql
SELECT START_TIME, WAREHOUSE_NAME,
       CREDITS_USED_COMPUTE, CREDITS_USED_CLOUD_SERVICES
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD('day', -2, CURRENT_TIMESTAMP())
ORDER BY START_TIME DESC;
```

The increase mapped to `TRANSFORM_WH`, which no longer suspended between five-minute task runs. A deployment had set `AUTO_SUSPEND = 0` while testing and promoted the setting to production.

## Root cause and contributors

Root cause: warehouse configuration drift disabled automatic suspension. Contributors were no policy-as-code assertion, cost alerting at daily rather than hourly resolution, and a change review that assessed functional behavior but not FinOps impact.

## Containment and recovery

The team restored the approved auto-suspend setting after confirming no long-lived session dependency, preserved warehouse and query evidence, and monitored two full task cycles. It did not suspend unrelated warehouses or terminate critical queries solely to meet a budget number.

## Corrective actions

- Enforce warehouse configuration through IaC and drift detection.
- Require query tags and ownership for scheduled workloads.
- Alert on hourly burn rate, idle-running intervals and forecast variance.
- Use resource monitors for warehouse controls while separately monitoring serverless services.
- Include credits per successful business unit—such as batch, row or report—in service SLO reviews.
- Add FinOps review to changes affecting size, cluster count, schedule, target lag or serverless features.

## Official references

- [Explore compute cost](https://docs.snowflake.com/en/user-guide/cost-exploring-compute)
- [`WAREHOUSE_METERING_HISTORY`](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history)
- [Resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [Cost management](https://docs.snowflake.com/en/user-guide/cost-understanding-overall)
