# Lab: Production Readiness Review Exercise

Version: v1.1.0  
Status: Vendor-aligned operational lab  
Last vendor validation: 2026-08-15

## Objective

Complete an evidence-based production-readiness review for a proposed Snowflake workload and produce explicit launch conditions, owners and rollback criteria.

## Safety and prerequisites

- Duration: approximately 45–60 minutes.
- Cost risk: read-only unless the review team separately approves a test.
- Required participants: workload owner, platform/SRE, security and FinOps; include data governance and compliance when applicable.
- Use the [production-readiness template](../templates/production-readiness-review.md).
- Do not approve launch based only on object existence or a successful functional query.

## Scenario

Review a proposed workload containing:

- one interactive application warehouse;
- one scheduled transformation workload;
- restricted data;
- a dynamic table or task dependency;
- monthly cost and freshness objectives;
- an on-call support requirement.

Use real non-secret metadata from an approved non-production environment or clearly label all scenario data as hypothetical.

## Evidence collection

Document:

1. Account, region, environment and ownership.
2. Role hierarchy and required object privileges.
3. Authentication and network path.
4. Warehouse size, auto-suspend, concurrency and isolation.
5. Task or dynamic-table monitoring.
6. Query and warehouse-load baseline.
7. Credit attribution, guardrails and notification ownership.
8. SLOs, alerts, runbooks and escalation.
9. Deployment rollback and recovery expectations.
10. Data classification, protection and audit requirements.

Useful read-only commands include:

```sql
SHOW WAREHOUSES;
SHOW TASKS;
SHOW DYNAMIC TABLES;
SHOW RESOURCE MONITORS;
SHOW NETWORK POLICIES;
```

Filter `SHOW` output immediately with `RESULT_SCAN(LAST_QUERY_ID())` when required. Use only authorized roles and avoid exposing sensitive policy details.

## Decision record

Classify every requirement:

- **Ready:** evidence satisfies the requirement.
- **Conditional:** launch depends on a named action and due date.
- **Blocked:** risk is unacceptable or ownership/evidence is missing.
- **Not applicable:** rationale is documented.

The review result is **Go**, **Conditional Go** or **No Go**. A Conditional Go must list time-bound conditions and an accountable approver.

## Success criteria

- Every critical control has evidence and an owner.
- SLO, alert and runbook links are recorded.
- Cost controls distinguish warehouses from serverless and AI services.
- Rollback and incident authority are explicit.
- No unresolved Blocked item is approved for launch.

## Cleanup

No objects are created. Store the completed review according to the organization's records policy.

## Official references

- [Access control privileges](https://docs.snowflake.com/en/user-guide/security-access-control-privileges)
- [Working with resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [Monitor query activity](https://docs.snowflake.com/en/user-guide/ui-snowsight-activity)
- [Monitor dynamic tables](https://docs.snowflake.com/en/user-guide/dynamic-tables/monitoring)
