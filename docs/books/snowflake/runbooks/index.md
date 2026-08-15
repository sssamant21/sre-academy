# Snowflake Production Runbooks

Version: v1.1.0  
Status: In development  
Last vendor validation: 2026-08-15

Runbooks provide evidence-first response procedures. They do not replace change management, incident command or Snowflake Support.

## Available runbooks

| Runbook | Primary chapters | Primary signal |
|---|---|---|
| [Warehouse Queuing](warehouse-queuing.md) | 6, 9 and 11 | Sustained queued load or user-visible latency |
| [Unexpected Credit Consumption](unexpected-credit-consumption.md) | 9, 10 and 11 | Credit usage materially exceeds the approved baseline |
| [Query Performance Regression](query-performance-regression.md) | 4, 5, 7 and 14 | A stable query pattern regresses |
| [Task and Dynamic Table Failures](task-and-dynamic-table-failures.md) | 11, 12 and 18 | Scheduled processing fails or stops |
| [Authentication and Connectivity Failure](authentication-and-connectivity.md) | 8, 11 and 17 | Clients cannot authenticate or connect |
| [Dynamic Table Freshness Degradation](dynamic-table-freshness.md) | 9, 11 and 18 | Refreshes miss the freshness objective |

## Response contract

Every runbook contains:

1. Trigger and customer impact.
2. Safety constraints.
3. Initial evidence with bounded queries.
4. Decision points that separate similar failure modes.
5. Reversible mitigation options.
6. Validation and rollback criteria.
7. Escalation evidence for Snowflake Support.
8. Official vendor references and validation date.

See the [runbook authoring standard](runbook-standard.md).
