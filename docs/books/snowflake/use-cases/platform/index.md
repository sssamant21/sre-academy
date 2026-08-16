# Sharing, Iceberg, Applications, and AI/ML

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

This phase covers patterns that publish data beyond a single workload, preserve open-table interoperability, package applications, and operationalize AI/ML. Confirm cloud, region, edition, model and account availability before implementation.

| Need | Pattern | Primary control |
|---|---|---|
| Governed cross-account access without copying | [Policy-protected Secure Data Sharing](secure-data-sharing.md) | Consumer contract and negative access tests |
| Open table format in object storage | [Iceberg lakehouse table](iceberg-lakehouse.md) | Catalog ownership and writer authority |
| Installable application running with consumer data | [Snowflake Native App](native-app.md) | Minimum privileges and versioned upgrades |
| Batch classification or extraction from text | [Governed AI enrichment](ai-enrichment.md) | Evaluation, token cost and sensitive-data policy |
| Retrieval over governed documents | [Cortex Search RAG](cortex-search-rag.md) | Retrieval quality and citation grounding |
| Time-series operational outliers | [ML anomaly detection](ml-anomaly-detection.md) | Baseline quality and alert response |

## Shared launch gate

Record the owner, approved regions and editions, data classification, privilege boundary, cost model, SLO, validation evidence, incident owner, recovery method, version policy and decommission procedure. Preview features require an explicit risk acceptance and must not be described as generally available.
