# Runbook: Recovery-Readiness Risk

Version: v1.3.0  
Status: Production Release  
Last vendor validation: 2026-08-15

## Trigger

- replication/failover-group refresh fails or exceeds the approved interval;
- estimated data-loss exposure threatens RPO;
- a recovery exercise misses RPO/RTO;
- protected-object membership or a critical dependency changes;
- failover/failback instructions are untested or inaccessible.

## Safety

This runbook addresses readiness degradation, not authorization for production failover. Promotion, rerouting and failback require incident authority, business approval and the service-specific recovery procedure.

## Procedure

1. Identify service, criticality, approved RPO/RTO and recovery owner.
2. Record latest successful refresh, current phase/error and verified data timestamp.
3. Determine whether customer production is currently impacted.
4. Compare protected objects with the service dependency inventory.
5. Review edition/region capability, schedule, recent changes and target-account readiness.
6. Estimate current RPO exposure conservatively; label uncertainty.
7. Retry or modify refresh only through the approved recovery procedure.
8. Establish compensating controls, business communication and next decision time.
9. After recovery, verify object availability, access, pipeline behavior and application routing.
10. Schedule or repeat an end-to-end exercise and track findings.

## Escalation package

- group/account identifiers and edition;
- UTC failure interval and query IDs;
- refresh phase, bytes, object count and error;
- recent configuration changes;
- RPO/RTO impact and business criticality;
- attempted actions and results.

## References

- [BCDR introduction](https://docs.snowflake.com/en/user-guide/replication-intro)
- [Replication refresh history](https://docs.snowflake.com/en/sql-reference/account-usage/replication_group_refresh_history)
- [Failover and failback](https://docs.snowflake.com/en/user-guide/account-replication-failover-failback)

