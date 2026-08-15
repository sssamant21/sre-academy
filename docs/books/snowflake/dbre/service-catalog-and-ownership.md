# Service Catalog and Ownership

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-15

## Why a service catalog is required

A Snowflake account is not a single service. Warehouses, data products, ingestion paths, transformations, shares and serving workloads can have different owners and reliability requirements. DBRE controls should therefore be applied to an identified service boundary.

## Minimum service record

| Field | Required content |
|---|---|
| Service name and purpose | Stable name and business outcome |
| Account and environment | Organization/account identifiers and production tier |
| Business owner | Person or accountable team |
| Technical owner | Team able to diagnose and change the service |
| On-call and escalation | Primary, secondary and executive paths |
| Criticality | Approved tier with rationale |
| Consumers | Applications, teams, shares or external users |
| Data classification | Sensitivity, regulatory scope and handling controls |
| Dependencies | Warehouses, databases, pipelines, integrations and upstream/downstream services |
| Reliability objectives | SLIs, SLOs, measurement windows and exclusions |
| Recovery objectives | RPO, RTO, recovery method and exercise date |
| Cost ownership | Cost center, budget owner and anomaly route |
| Operational assets | Dashboards, alerts, runbooks, deployment and rollback procedures |

## Criticality tiers

| Tier | Typical impact | Expected control strength |
|---|---|---|
| Tier 0 | Enterprise-wide or regulated critical path | Continuous coverage, tested recovery, strict change gates |
| Tier 1 | Major customer or revenue impact | On-call ownership, SLOs, tested runbooks and recovery |
| Tier 2 | Important internal workload | Business-hours support plus defined escalation and recovery |
| Tier 3 | Development, experimental or low-impact | Named owner, cost controls and basic lifecycle management |

Tier names and response commitments are internal policy; Snowflake does not prescribe them.

## Dependency mapping

Record both platform and data dependencies. At minimum, map:

- identity provider, network path and client/driver;
- storage integration, stage, pipe or ingestion service;
- source tables, streams, tasks and dynamic-table graph;
- warehouse and resource/cost controls;
- downstream tables, shares, applications and BI tools;
- external functions, APIs and notification integrations;
- replicated objects and recovery account.

Dynamic-table graph functions can support discovery, but the catalog remains an owned enterprise record and must include dependencies outside Snowflake.

## Ownership acceptance criteria

A production service is not considered owned until:

- accountable and technical owners accept the record;
- escalation paths are tested;
- the service boundary and dependencies are reviewable;
- SLO and recovery decisions are approved;
- operational assets are accessible to responders;
- the next review date is assigned.

## Official references

- [DYNAMIC_TABLE_GRAPH_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/dynamic_table_graph_history)
- [OBJECT_DEPENDENCIES view](https://docs.snowflake.com/en/sql-reference/account-usage/object_dependencies)
- [TAG_REFERENCES view](https://docs.snowflake.com/en/sql-reference/account-usage/tag_references)

