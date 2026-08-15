# Answers: Chapters 6–10

Version: v1.2.0  
Status: In development  
Last reviewed: 2026-08-15

1. Overload reflects warehouse demand, provisioning reflects compute startup/scaling, and blocking reflects transactional locks.
2. Isolation is preferable when workloads have different SLOs, owners, schedules or interference patterns and the added governance/cost is justified.
3. Pause or route approved non-critical batch work, then validate queueing, interactive latency, critical completion and cost across multiple intervals.
4. Pruning eliminates storage work, caching reuses prior results/data, and Search Optimization targets supported selective access patterns.
5. Query Profile exposes operator-level execution, expensive nodes, scan and spill behavior beyond summary duration.
6. Record result-cache and scanned-cache evidence and compare executions that actually performed equivalent work.
7. Roles aggregate privileges; users/services receive roles; privileges are granted only on required objects and operations.
8. A narrow user-level test reduces lockout blast radius and provides rollback evidence before broader enforcement.
9. The session authenticated successfully; the remaining failure concerns active roles or object privileges.
10. Delayed views can misrepresent current state, so alerts must identify freshness and use appropriate immediate sources.
11. UTC window, account/region, warehouse/object, query/task/login identifier, severity, owner and source.
12. Use immediate Snowsight/Information Schema or client evidence for current state and Account Usage for retained trend, explicitly noting latency.
13. Resource monitors apply to warehouses, not all serverless features and AI services; budgets and service-specific views are also required.
14. Record current size/configuration, load/SLO, credit baseline, representative workload, test result, rollback and business approval.
15. Attribute by warehouse/workload, stop only the confirmed duplicate or runaway non-critical path, preserve critical service, and reconcile immediate activity with metering.

Review [Chapters 6–10](../chapters-06-10.md) and the linked handbook chapters for deeper reasoning.
