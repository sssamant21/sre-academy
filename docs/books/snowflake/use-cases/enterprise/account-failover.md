# Account Failover and Failback

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

## Use when

Use failover groups for account-level business continuity requiring promotion of replicated data and selected account objects in another account, region or cloud. Account failover/failback requires Business Critical Edition or higher. Replication does not replace application, DNS, identity, integration and operational recovery planning.

```mermaid
flowchart LR
    A[Primary account] --> B[Failover group]
    B --> C[Secondary account]
    C --> D[Application cutover]
```

## Setup skeleton

```sql
-- Source account
CREATE FAILOVER GROUP production_fg
  OBJECT_TYPES = DATABASES, USERS, ROLES, WAREHOUSES,
                 RESOURCE MONITORS, INTEGRATIONS
  ALLOWED_DATABASES = production_db
  ALLOWED_INTEGRATION_TYPES = STORAGE INTEGRATIONS,
                              NOTIFICATION INTEGRATIONS
  ALLOWED_ACCOUNTS = myorg.recovery_account
  REPLICATION_SCHEDULE = '10 MINUTE';

-- Recovery account
CREATE FAILOVER GROUP production_fg
  AS REPLICA OF myorg.primary_account.production_fg;
```

Confirm supported object types, dependencies and regional limitations for the exact topology. Secrets, external cloud policies, network connectivity and some objects require separate recovery actions.

## Exercise procedure

1. Measure current replication lag and verify the last successful refresh.
2. Declare the exercise or incident and freeze conflicting changes.
3. Refresh if the scenario permits, promote the secondary, and record the achieved recovery point.
4. activate identity, integrations, application endpoints and scheduled processing in dependency order.
5. Run write/read, security, pipeline and data-product smoke tests.
6. Operate for the approved period; plan reverse replication and failback as a separate change.

## Controls and failback

Track achieved RPO/RTO, missing dependencies, manual steps, cost and evidence. Dynamic tables may reinitialize after failover, so include refresh duration and cost in readiness tests. Before failback, stop writes, reconcile the current primary, replicate toward the original account, promote only after approval, then validate again. Avoid rapid failover/failback that creates competing write histories.

## Official references

- [Business continuity and disaster recovery](https://docs.snowflake.com/en/user-guide/replication-intro)
- [Account replication and failover](https://docs.snowflake.com/en/user-guide/account-replication-intro)
- [Failover and failback](https://docs.snowflake.com/en/user-guide/account-replication-failover-failback)
- [`CREATE FAILOVER GROUP`](https://docs.snowflake.com/en/sql-reference/sql/create-failover-group)
