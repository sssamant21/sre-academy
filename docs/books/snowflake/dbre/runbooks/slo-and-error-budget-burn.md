# Runbook: SLO and Error-Budget Burn

Version: v1.3.0  
Status: In development  
Last vendor validation: 2026-08-15

## Trigger

- SLO breach;
- sustained short/long-window burn above policy;
- budget exhaustion forecast before the window ends;
- conflicting service and platform health signals.

## Safety

Do not change workload eligibility, exclusions or the metric definition during an event to make the breach disappear. Do not resize, suspend, cancel or replay work without using the relevant technical runbook and authority.

## Procedure

1. Identify the service, SLI version, window, owner and criticality.
2. Verify telemetry freshness, completeness, units, timezone and eligibility filters.
3. Recalculate numerator, denominator and budget from source evidence.
4. Establish customer impact and affected consumers.
5. Correlate query, warehouse, task, freshness, access, deployment and dependency signals.
6. Classify the cause: genuine service failure, dependency failure, measurement defect or approved exclusion.
7. Invoke the authoritative technical runbook for the failure mode.
8. Apply the error-budget policy: change restriction, reliability prioritization or documented exception.
9. Verify recovery using both the SLI and customer-facing evidence.
10. Record budget consumed, incident link, corrective actions and next review.

## Escalate when

- critical-service impact is active;
- telemetry cannot confirm impact;
- mitigation could affect other services or security;
- budget is exhausted with no approved recovery plan;
- Snowflake service behavior requires vendor investigation.

## Completion

Close only when service behavior is restored, measurement is trusted, policy actions are recorded, and follow-up has owners and dates.

## References

- [DBRE reliability objectives](../reliability-objectives.md)
- [Production runbooks](../../runbooks/index.md)
- [QUERY_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)

