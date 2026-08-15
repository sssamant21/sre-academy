# Answers: Chapters 1–5

Version: v1.2.0  
Status: Production Release  
Last reviewed: 2026-08-15

1. Separation permits independent compute scaling, shared managed storage and service-managed coordination, enabling isolation and cost attribution without coupling data size to compute.
2. Accept account/organization, environment, region/cloud, security, ownership, data-classification and cost boundaries; any three with rationale earn full credit.
3. Evaluate regulatory isolation, identity/governance ownership, data sharing, blast radius, region, billing and operating responsibility. Separate accounts are justified by boundaries, not preference alone.
4. Warehouses supply workload compute; Snowflake-managed services handle coordination, metadata, security and platform services.
5. Undocumented assumptions can change and cannot be treated as supported contracts. Decisions should rely on documented behavior and measured evidence.
6. Separate client/network timing, cloud-service compilation, warehouse queue/provisioning and execution using query history, warehouse load and query IDs.
7. Snowflake organizes table data into immutable micro-partitions and maintains metadata that allows eligible partitions to be eliminated.
8. Compare partitions scanned/total, bytes scanned, predicates, Query Profile scan operators and comparable data windows.
9. Confirm stable predicate patterns, clustering information, data distribution, pruning evidence, workload frequency, maintenance cost and measured benefit.
10. Compilation prepares the query; queue time waits for compute or resources; execution performs operators after admission.
11. It anchors history, profile, operator statistics, support evidence and comparisons to one execution.
12. Use queued-overload, queued-provisioning, blocked and execution metrics, plus application/client timing and warehouse load.
13. Cache, queueing, data volume, concurrency and client timing can change elapsed time independently of SQL quality.
14. Match logical pattern, parameters/data window, warehouse configuration, concurrency, cache state and measurement method.
15. Establish scan/operator evidence, test an approved SQL or data-design correction, compare correctness/performance/cost, then evaluate compute only if evidence supports it.

Review [Chapters 1–5](../chapters-01-05.md) and the linked handbook chapters for deeper reasoning.
