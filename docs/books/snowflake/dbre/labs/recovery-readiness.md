# Lab: Assess Recovery Readiness

Version: v1.3.0  
Status: Production Release  
Audience: DBRE, architects and service owners  
Duration: 90 minutes  
Cost risk: Low for tabletop/read-only execution  
Required privileges: Read-only replication metadata, or synthetic evidence  
Edition constraint: Account-object failover/failback requires Business Critical Edition or higher  
Last vendor validation: 2026-08-16

## Objective

Determine whether a selected service has a credible path to meet its approved RPO and RTO.

## Procedure

1. Record service criticality, approved RPO/RTO and decision owners.
2. Inventory data, roles, warehouses, integrations, policies and external dependencies required after recovery.
3. Identify which dependencies are protected and which require separate restoration or reconfiguration.
4. Review latest successful refresh, schedule, duration, error and verified data time.
5. Calculate current recovery-point exposure conservatively.
6. Walk through promotion authority, application rerouting, validation and failback.
7. Estimate elapsed time for every customer-owned step.
8. Identify gaps that prevent meeting RPO/RTO and assign corrective actions.
9. Schedule a controlled exercise; do not perform production failover in this lab.

## Success criteria

- protected scope matches the service inventory;
- RPO/RTO claims are supported by end-to-end evidence;
- non-Snowflake dependencies are included;
- exercise findings have owners and due dates.

## References

- [Recovery-readiness dashboard](../dashboards/dashboard-specifications.md#5-recovery-readiness-dashboard)
- [BCDR introduction](https://docs.snowflake.com/en/user-guide/replication-intro)
- [Replication refresh history](https://docs.snowflake.com/en/sql-reference/account-usage/replication_group_refresh_history)
- [Failover and failback](https://docs.snowflake.com/en/user-guide/account-replication-failover-failback)

