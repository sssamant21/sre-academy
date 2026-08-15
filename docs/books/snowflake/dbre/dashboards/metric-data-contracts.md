# DBRE Metric Data Contracts

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-15

A dashboard metric is production-ready only when its calculation, scope and operating limitations are versioned as a data contract.

## Required contract fields

| Field | Requirement |
|---|---|
| Metric name | Stable, unique and human-readable |
| Decision | Question the metric answers |
| Owner | Team responsible for correctness and response |
| Formula | Numerator, denominator, aggregation and units |
| Source | Fully qualified view/function or curated dataset |
| Eligibility | Included services, events and states |
| Exclusions | Predefined, reviewed and auditable |
| Dimensions | Approved grouping keys and cardinality limits |
| Time | Event timestamp, timezone, window and late-arrival policy |
| Latency | Expected source and pipeline delay |
| Retention | Available and curated history |
| Quality | Freshness, completeness and reconciliation checks |
| Threshold | Objective/alert mapping and rationale |
| Runbook | Response link and escalation |
| Version | Effective date and change history |

## Source-selection rules

Use Information Schema table functions when their shorter, lower-latency operational window fits the decision. Use Account Usage for longer account history, while explicitly accommodating each view's documented latency. Use Organization Usage only for organization-level decisions and account for its view-specific latency and availability.

Do not query large history views without bounded time predicates. Select required columns explicitly and materialize curated monitoring datasets when repeated dashboard scans create avoidable cost or latency.

## Metric-quality indicators

Every dashboard should expose:

- source maximum observed event time;
- ingestion/materialization completion time;
- expected versus actual row/event count where feasible;
- last successful reconciliation;
- current quality state: healthy, delayed, incomplete or unknown.

When quality is unknown, show the service state as unknown rather than healthy.

## Change control

A metric change requires:

1. versioned definition and reason;
2. comparison of old and new results over a representative interval;
3. SLO/error-budget impact assessment;
4. owner approval;
5. dashboard, alert and runbook updates;
6. effective-date annotation.

## Official references

- [Differences between Account Usage and Information Schema](https://docs.snowflake.com/en/sql-reference/account-usage#differences-between-account-usage-and-information-schema)
- [Account Usage latency](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Organization Usage](https://docs.snowflake.com/en/sql-reference/organization-usage)
- [QUERY_HISTORY table functions](https://docs.snowflake.com/en/sql-reference/functions/query_history)

