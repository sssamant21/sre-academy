# Assessment: Chapters 1–5

Version: v1.2.0  
Status: Production Release  
Last reviewed: 2026-08-15

## Chapter 1 — Enterprise Architecture

1. **Concept:** Why does separating storage, compute and cloud services matter for enterprise workload design?
2. **Operations:** Name three account or platform boundaries that should be explicit before production onboarding.
3. **Scenario:** Two business units require different security and cost ownership. What evidence determines whether they should share an account?

## Chapter 2 — Platform Components

4. **Concept:** What responsibilities belong to virtual warehouses versus Snowflake-managed services?
5. **Operations:** Why should operators avoid assuming undocumented internal implementation behavior?
6. **Scenario:** Query latency rises while stored data remains unchanged. Which platform layers and evidence should be investigated first?

## Chapter 3 — Storage Internals

7. **Concept:** How do immutable micro-partitions support pruning and metadata-driven optimization?
8. **Operations:** Which metrics help distinguish efficient pruning from a broad scan?
9. **Scenario:** A selective query scans most partitions after a data-pattern change. What should be verified before adding a clustering key?

## Chapter 4 — Query Processing

10. **Concept:** What is the difference between compilation time, queue time and execution time?
11. **Operations:** Why is a query ID essential during performance diagnosis?
12. **Scenario:** Total elapsed time rises but execution time is stable. What evidence separates warehouse queueing, provisioning and client-side delay?

## Chapter 5 — Performance Engineering

13. **Concept:** Why is elapsed time alone an insufficient performance baseline?
14. **Operations:** What makes two query executions comparable?
15. **Scenario:** A team proposes a larger warehouse for a scan-heavy query. Describe the safer evidence-first experiment.
