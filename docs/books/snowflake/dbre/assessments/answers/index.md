# Snowflake DBRE Answer Appendix

Version: v1.3.0  
Status: In development  
Last reviewed: 2026-08-16

Equivalent answers are acceptable when they preserve documented Snowflake behavior, DBRE reasoning and operational safety.

## Operating model and ownership

1. Snowflake manages the service infrastructure; the enterprise owns workload design, configuration, access, pipelines, telemetry, customer recovery preparation, change safety, incident response and cost controls.
2. Different workloads and data products can have distinct consumers, owners, dependencies, criticality and objectives; controls need an explicit service boundary.
3. Purpose, environment, owners/on-call, criticality, consumers, classification, dependencies, SLOs, RPO/RTO, cost ownership, dashboards, alerts, runbooks and review date.
4. Accountable owns the outcome/approval; responsible performs the work. One activity may combine them, but ambiguity must be resolved.
5. No. Operational assets without an accepted owner lack decision authority, escalation and maintenance accountability.
6. Updated maturity evidence, top risks/exceptions, SLO/budget trend, incident recurrence, recovery findings, capacity/cost forecast and owned commitments.

## SLIs, SLOs and error budgets

7. SLI is measured behavior; SLO is its internal target; error budget is permitted unreliability; alert triggers response; SLA is a contractual commitment.
8. Defining them afterward permits outcome-driven exclusions and makes the metric irreproducible.
9. `500,000 × (1 − 0.999) = 500` allowed bad events.
10. It counts events, not unavailable time; conversion changes the measurement model unless the SLI is time-based.
11. Restrict discretionary risk, prioritize restoration/reliability work, require stronger approval, document exceptions and assign owners/dates.
12. Mark the result delayed/unknown, verify freshness/completeness, recalculate from trustworthy bounded evidence and separately establish customer impact.

## Dashboards and telemetry

13. Customer-impact indicators measure the service outcome; contributing signals help explain causes such as queueing, failures or changes.
14. Decision, owner, formula, source, eligibility/exclusions, dimensions, time, latency, retention, quality, threshold, runbook and version.
15. Without them, stale or incomplete data may be presented as current health and drive unsafe decisions.
16. Use its lower-latency operational table functions when their shorter history fits the decision; it still has function-specific windows, privilege requirements and semantics.
17. They create avoidable cost/latency and may make monitoring itself unreliable; bound time and select explicit columns.
18. Align source semantics, event timestamps, timezone, closed window, latency, eligibility, exclusions, aggregation and late-arrival policy.

## Reliability controls and runbooks

19. Latency can arise from queueing, compilation, scanning, spill, data movement, SQL design or dependencies; resizing may add cost without fixing cause.
20. It does not prove schedule completeness, freshness, correctness, downstream delivery, or safe replay.
21. Proven detection, narrow scope, authorization, reversibility, stop conditions, audit trail and automatic post-action verification.
22. Preserve current/baseline state, determine whether it is unauthorized drift or stale desired state, assess impact, and define rollback/verification.
23. Missing evidence means unknown, not no activity; zero can falsely show health and corrupt SLO calculations.
24. Detection/source, condition, schedule, execution, notification delivery, routing, acknowledgement and responder action.

## Recovery and production readiness

25. Replication groups provide read-only replicated objects; failover groups also support promotion of a secondary to primary for supported objects.
26. RTO includes grants, integrations, policies, application rerouting, validation, approvals and other customer-owned steps beyond refresh completion.
27. Roles/grants, warehouses, integrations, network/identity, tasks/pipelines, policies, secrets, application routing, downstream consumers and failback.
28. Evidence for each gate plus every exception's risk, owner, compensating control, due/expiry date and approving authority.
29. RTO is directly at risk. Do not declare success; diagnose missing access/routing, correct the plan, assign owners and repeat a controlled exercise.
30. Material security, compliance, recovery or ownership gaps—and any mandatory critical-service domain below policy—can block production.

## References

- [DBRE section](../../index.md)
- [Official Snowflake Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Snowflake BCDR](https://docs.snowflake.com/en/user-guide/replication-intro)

