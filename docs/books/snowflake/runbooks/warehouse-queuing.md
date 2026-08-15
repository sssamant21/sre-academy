# Runbook: Warehouse Queuing

Version: v1.1.0  
Status: Vendor-validated runbook  
Last vendor validation: 2026-08-15

## Trigger

Use this runbook when users report increased latency and warehouse telemetry shows sustained queued load. Do not assume queuing is the cause until it is separated from provisioning delay and transaction blocking.

## Immediate safety

- Declare the affected warehouse, workloads, time window and incident owner.
- Avoid simultaneous resize, scaling-policy and SQL changes.
- Preserve query IDs and configuration before mitigation.
- Do not cancel queries or suspend a shared warehouse without incident authority.

## Evidence

```sql
SELECT
  START_TIME,
  END_TIME,
  AVG_RUNNING,
  AVG_QUEUED_LOAD,
  AVG_QUEUED_PROVISIONING,
  AVG_BLOCKED
FROM TABLE(
  INFORMATION_SCHEMA.WAREHOUSE_LOAD_HISTORY(
    DATE_RANGE_START => DATEADD('hour', -2, CURRENT_TIMESTAMP()),
    DATE_RANGE_END   => DATEADD('minute', -2, CURRENT_TIMESTAMP()),
    WAREHOUSE_NAME  => '<warehouse-name>'
  )
)
ORDER BY START_TIME;
```

Capture slow or queued queries from an appropriately privileged history surface. Record query ID, user, role, warehouse, queue time, execution time and query tag. Account Usage can have latency.

## Decision points

- **Queued load dominates:** identify concurrency bursts, workload mixing and expensive repeated queries.
- **Queued provisioning dominates:** inspect resume or cluster-provisioning timing before increasing steady-state capacity.
- **Blocked dominates:** follow transaction and lock investigation; additional compute may not resolve it.
- **One query dominates:** inspect Query Profile and SQL behavior before altering warehouse capacity.

## Mitigation options

Choose one controlled change:

1. Reduce or pause non-critical batch submissions.
2. Route an approved workload to an isolated warehouse.
3. Correct a high-impact query when rollback is immediate.
4. Temporarily resize the warehouse with an owner and expiry time.
5. Adjust multi-cluster settings only when supported by edition, workload design, budget and change control.

## Validation

Confirm that queued load and customer-visible latency recover over multiple intervals. Verify that cost, error rate and critical batch completion remain within accepted limits.

## Rollback

Restore the previous warehouse size, scaling parameters or workload route if cost, stability or performance deteriorates. Record exact before-and-after settings.

## Escalation package

Provide Snowflake Support with account locator, region, incident window in UTC, warehouse name, representative query IDs, query profiles, configuration, observed load categories and changes already attempted. Do not include secrets.

## Official references

- [WAREHOUSE_LOAD_HISTORY table function](https://docs.snowflake.com/en/sql-reference/functions/warehouse_load_history)
- [WAREHOUSE_LOAD_HISTORY Account Usage view](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_load_history)
- [Monitor query activity with Query History](https://docs.snowflake.com/en/user-guide/ui-snowsight-activity)
