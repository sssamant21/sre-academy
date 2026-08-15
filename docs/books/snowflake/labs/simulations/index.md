# Snowflake Incident Simulation Labs

Version: v1.2.0  
Status: In development  
Last vendor validation: 2026-08-15

These tabletop and controlled-environment simulations train evidence-based response without intentionally disrupting production.

## Simulation catalog

| Simulation | Primary signal | Core decision |
|---|---|---|
| [Warehouse Saturation](warehouse-saturation.md) | Sustained queued load and latency | Workload control, isolation or temporary capacity |
| [Query Regression](query-regression.md) | Stable query pattern becomes slower | SQL, data, queue, spill or cache cause |
| [Unexpected Credit Spike](unexpected-credit-spike.md) | Consumption exceeds baseline | Contain waste without harming critical services |
| [Failed Task Graph](failed-task-graph.md) | Scheduled graph enters failure state | Correct cause and decide whether replay is safe |
| [Authentication and Network-Policy Outage](authentication-network-policy-outage.md) | Clients cannot connect | Network path, policy, identity or authorization |
| [Dynamic-Table Freshness Breach](dynamic-table-freshness-breach.md) | Actual freshness misses objective | Repair upstream failure or address refresh capacity |

## Safety contract

- Use synthetic evidence or an isolated non-production account.
- Never trigger an account-wide lockout, uncontrolled workload, production cancellation or unbounded credit consumption.
- Facilitators provide injects; participants do not manufacture failures in production.
- All timestamps use UTC.
- Credentials, tokens, private keys, MFA codes and full connection strings are prohibited.
- Any controlled change requires an owner, rollback, expiry and validation criteria.

## Participant roles

- Incident commander
- Snowflake platform/SRE responder
- Workload or application owner
- Security responder when access is involved
- FinOps responder when consumption is involved
- Scribe and facilitator

## Facilitator material

Use the [facilitator guides and common scoring rubric](facilitator-guides/index.md) only after participants complete the scenario.

## Completion evidence

Each team submits an incident timeline, evidence table, diagnosis, selected mitigation, rollback decision, customer communication and corrective actions. The facilitator scores reasoning and operational safety, not memorization.
