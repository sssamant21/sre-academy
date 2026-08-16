# Snowflake DBRE Assessment Questions

Version: v1.3.0  
Status: In development  
Last reviewed: 2026-08-16

Complete all questions before opening the answer appendix.

## Operating model and ownership

1. What is the primary customer-owned DBRE boundary in a managed Snowflake service?
2. Why should a Snowflake account not automatically be treated as one service?
3. Which fields make a service catalog record operationally actionable?
4. How do accountable and responsible roles differ in a RACI model?
5. A critical workload has dashboards and runbooks but no accepted technical owner. Is it production-ready, and why?
6. What should a quarterly DBRE operating review produce?

## SLIs, SLOs and error budgets

7. Distinguish an SLI, SLO, error budget, alert and SLA.
8. Why must eligibility and exclusions be defined before inspecting performance results?
9. Calculate the allowed bad events for 500,000 eligible events at a 99.9% objective.
10. Why should an event-based error budget not automatically be expressed as downtime?
11. What actions should an exhausted error budget trigger?
12. A dashboard reports an SLO breach, but its source is stale. What is the correct initial response?

## Dashboards and telemetry

13. What is the difference between a customer-impact indicator and a contributing signal?
14. Which metric data-contract fields are essential for safe operational use?
15. Why must dashboard panels expose telemetry freshness and completeness?
16. When should Information Schema be preferred over Account Usage, and what limitation remains?
17. Why are unbounded history-view queries an operational anti-pattern?
18. A curated dashboard disagrees with a bounded source query. List the first comparison checks.

## Reliability controls and runbooks

19. Why is warehouse resizing not the default response to every latency incident?
20. Why does successful task execution not prove pipeline reliability?
21. What makes an automated remediation safe enough to progress beyond recommendation?
22. What must happen before correcting detected configuration drift?
23. During a telemetry gap, why must missing observations not be converted to zero?
24. An alert missed customer impact. Which failure classes should the responder examine?

## Recovery and production readiness

25. Distinguish a replication group from a failover group.
26. Why does a successful replication refresh not prove RTO readiness?
27. Which dependencies should an end-to-end recovery review include beyond data?
28. What evidence is required for an approved-with-conditions production decision?
29. A recovery exercise can read secondary data but the application cannot connect. Which objective is most directly at risk, and what should happen next?
30. Which conditions can block production regardless of an average DBRE maturity score?

