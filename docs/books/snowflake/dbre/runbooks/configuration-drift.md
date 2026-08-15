# Runbook: Snowflake Configuration Drift

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-15

## Trigger

- account, warehouse, role, policy, integration, task or dynamic-table state differs from the approved baseline;
- an untracked manual change is discovered;
- deployment reconciliation repeatedly proposes unexpected changes;
- drift creates SLO, security, recovery or cost risk.

## Procedure

1. Identify the exact object, property, environment and approved baseline version.
2. Preserve current state, ownership, grants, change history and dependent-service context.
3. Determine whether the difference is unauthorized drift, emergency change, stale baseline or tool defect.
4. Assess active impact across reliability, security, cost and recovery.
5. Select a direction: restore approved state or approve and codify the current state.
6. Define execution role, prechecks, blast radius, rollback and verification.
7. Apply the smallest approved change; avoid broad reconciliation during an incident.
8. Verify object behavior, dependent workloads and dashboards.
9. Update code/baseline and record the change so drift does not recur.
10. Correct access, process or automation gaps that permitted untracked drift.

## Safety

Do not overwrite an emergency production change before understanding why it exists. Treat ownership, grants, network policies, integrations and recovery configuration as high-impact changes.

## Escalate when

- privileged access or data protection changed;
- the desired state is disputed;
- correction affects multiple services/accounts;
- rollback is not tested;
- drift may indicate compromise.

## References

- [Access-control overview](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
- [ACCESS_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/access_history)
- [DBRE production-readiness standard](../production-readiness.md)

