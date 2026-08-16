# Lab: Conduct a DBRE Production-Readiness Review

Version: v1.3.0  
Status: In development  
Audience: DBRE, service owners, security, platform engineering and FinOps  
Duration: 90 minutes  
Cost risk: Low  
Required privileges: None when using an evidence pack  
Last vendor validation: 2026-08-16

## Objective

Reach an evidence-based production decision for a proposed Snowflake workload.

## Scenario

A new regulated reporting pipeline is scheduled for production next week. It has passed functional testing, but ownership, recovery, telemetry and cost evidence are incomplete.

## Procedure

1. Assign chair, service owner, DBRE reviewer, security, platform and FinOps roles.
2. Review ownership, consumers, criticality and data classification.
3. Evaluate SLOs, telemetry quality, dashboards and alert tests.
4. Review representative performance, capacity and cost evidence.
5. Evaluate pipeline replay, schema change and data-correctness controls.
6. Review access, network, break-glass and audit requirements.
7. Test recovery evidence against RPO/RTO.
8. Review deployment, rollback, runbooks and drift detection.
9. Classify every gap as blocking, conditional or accepted residual risk.
10. Issue one decision: approved, approved with conditions or not approved.

## Success criteria

- every gate has evidence or an explicit gap;
- exceptions have owner, compensating control and expiry;
- unresolved security/recovery risks are not hidden by an average score;
- the final decision and authority are recorded.

## References

- [DBRE production-readiness standard](../production-readiness.md)
- [Production-readiness template](../../templates/production-readiness-review.md)
- [Access-control overview](https://docs.snowflake.com/en/user-guide/security-access-control-overview)

