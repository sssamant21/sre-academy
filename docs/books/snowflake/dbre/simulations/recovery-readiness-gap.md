# Simulation: Recovery-Readiness Gap

Version: v1.3.0  
Status: Production Release  
Duration: 75 minutes  
Last vendor validation: 2026-08-16

## Situation

Replication refreshes are successful and within the approved interval, but a quarterly exercise cannot restore the reporting service within RTO. A required integration and application connection configuration are absent from the recovery plan.

## Objectives

- distinguish successful Snowflake replication from recoverable service;
- calculate RPO exposure using verified evidence;
- identify customer-owned RTO steps and dependencies;
- create a safe corrective exercise plan.

## Injects

1. Refresh history shows `COMPLETED` within the RPO window.
2. Secondary data is readable, but the service role lacks required access.
3. Storage/notification integration dependencies were not included.
4. Application DNS/connection rerouting requires another team and two approvals.
5. Leadership asks whether production failover should be attempted immediately.

## Expected decisions

- do not authorize production failover from a tabletop result alone;
- record that platform refresh success does not prove end-to-end RTO;
- map missing objects, grants, integrations and external routing;
- assign owners and time estimates for every recovery step;
- repeat a controlled exercise and verify failback readiness.

## Completion evidence

RPO calculation, RTO timeline, dependency gap analysis, risk communication, corrected procedure and next exercise criteria.

## References

- [Recovery-readiness runbook](../runbooks/recovery-readiness-risk.md)
- [Replication refresh history](https://docs.snowflake.com/en/sql-reference/account-usage/replication_group_refresh_history)
- [Failover and failback](https://docs.snowflake.com/en/user-guide/account-replication-failover-failback)

