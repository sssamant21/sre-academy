# Lab: Validate Telemetry Quality

Version: v1.3.0  
Status: Production Release  
Audience: DBRE and observability engineers  
Duration: 60 minutes  
Cost risk: Low  
Required privileges: Read access to selected metadata sources  
Last vendor validation: 2026-08-16

## Objective

Prove that an operational metric is fresh, complete and reconcilable enough for its intended decision.

## Procedure

1. Select one dashboard metric and retrieve its data contract.
2. Record the source's documented latency, retention and privilege requirements.
3. Run a bounded source query with explicit columns.
4. Record maximum event timestamp, query completion time and row count.
5. Compare the curated metric with source data over an overlapping closed interval.
6. Explain legitimate differences in timezone, late arrival, eligibility and aggregation.
7. Simulate a stale-source state in the dashboard or evidence pack.
8. Verify that the metric becomes delayed/unknown and links to the telemetry-gap runbook.
9. Record reconciliation tolerance, owner and next validation date.

## Safety

Do not create unbounded scans of Account Usage. Do not treat differences between Information Schema and Account Usage as defects until semantics, windows and latency are aligned.

## Success criteria

- freshness and completeness are measured, not assumed;
- unexplained variance is assigned for investigation;
- dashboard behavior under stale data is safe;
- blind-window decisions are documented.

## References

- [Telemetry-gap runbook](../runbooks/telemetry-gap.md)
- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
- [QUERY_HISTORY table functions](https://docs.snowflake.com/en/sql-reference/functions/query_history)

