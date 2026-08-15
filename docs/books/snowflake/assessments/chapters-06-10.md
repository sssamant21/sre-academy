# Assessment: Chapters 6–10

Version: v1.2.0  
Status: Production Release  
Last reviewed: 2026-08-15

## Chapter 6 — Workload and Concurrency

1. **Concept:** Distinguish overload queueing, provisioning queueing and transaction blocking.
2. **Operations:** When is workload isolation preferable to permanent warehouse resizing?
3. **Scenario:** Interactive and batch traffic share a saturated warehouse. Define the first reversible mitigation and validation.

## Chapter 7 — Query Tuning

4. **Concept:** How do pruning, caching and Search Optimization address different performance problems?
5. **Operations:** What does Query Profile contribute beyond Query History summary metrics?
6. **Scenario:** A query becomes faster on its second run. Which cache evidence prevents a false tuning conclusion?

## Chapter 8 — Security and Governance

7. **Concept:** Explain least privilege using role hierarchy and object privileges.
8. **Operations:** Why should network policies be tested narrowly before account-level activation?
9. **Scenario:** Authentication succeeds but a query is denied. Why is this an authorization investigation rather than connectivity?

## Chapter 9 — Observability and Operations

10. **Concept:** Why must history-view latency be documented in alert and incident procedures?
11. **Operations:** What minimum identifiers should accompany a Snowflake operational alert?
12. **Scenario:** A dashboard shows delayed metrics during an incident. How should responders combine immediate and historical evidence?

## Chapter 10 — Cost and FinOps

13. **Concept:** Why do resource monitors not provide complete coverage for every Snowflake cost?
14. **Operations:** What evidence is required before resizing a warehouse for savings?
15. **Scenario:** Credits spike after a deployment. Describe attribution, containment and validation without suspending critical services.
