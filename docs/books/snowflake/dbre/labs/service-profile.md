# Lab: Build a Snowflake Service Profile

Version: v1.3.0  
Status: In development  
Audience: DBRE, service owners and platform engineers  
Duration: 60 minutes  
Cost risk: Low  
Required privileges: Read-only metadata appropriate to the selected service  
Last vendor validation: 2026-08-16

## Objective

Define an owned Snowflake service boundary with consumers, dependencies, criticality and operational assets.

## Scenario

A business-critical reporting service uses a dedicated warehouse, curated tables, scheduled transformations and a BI client. No single record identifies the technical owner, downstream consumers or recovery dependencies.

## Procedure

1. Name the service by business outcome rather than account or warehouse alone.
2. Record account, environment, databases, schemas, warehouses and integrations.
3. Identify business owner, technical owner, on-call and escalation routes.
4. Classify criticality and data sensitivity with rationale.
5. Map identity/network, ingestion, transformation, storage and consumer dependencies.
6. Link dashboards, alerts, deployment, rollback, runbooks and recovery procedures.
7. Define SLO and RPO/RTO decision owners even if objectives are not yet approved.
8. Review the record with one upstream and one downstream owner.

## Evidence table

| Evidence | Source | Finding | Owner/action |
|---|---|---|---|
| Object/dependency inventory | Approved metadata or architecture record |  |  |
| Ownership acceptance | Team review |  |  |
| Operational asset links | Service record |  |  |
| Known gaps | Risk register |  |  |

## Success criteria

- service boundary is specific and reviewable;
- accountable and technical owners accept it;
- critical dependencies outside Snowflake are included;
- missing controls have owners and dates.

## Cleanup

No Snowflake objects are created. Remove any exported evidence containing sensitive identifiers according to organizational policy.

## References

- [DBRE service catalog and ownership](../service-catalog-and-ownership.md)
- [OBJECT_DEPENDENCIES](https://docs.snowflake.com/en/sql-reference/account-usage/object_dependencies)
- [DYNAMIC_TABLE_GRAPH_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/dynamic_table_graph_history)

