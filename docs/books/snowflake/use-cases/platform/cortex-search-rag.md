# Cortex Search Retrieval-Augmented Generation

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

## Use when

Use Cortex Search for governed hybrid retrieval over Snowflake text, including RAG applications. Search improves grounding but does not prove that a generated answer is correct.

```mermaid
flowchart LR
    A[Governed documents] --> B[Chunked corpus]
    B --> C[Cortex Search]
    C --> D[Prompt context]
    D --> E[Answer with citations]
```

## Service skeleton

```sql
CREATE OR REPLACE CORTEX SEARCH SERVICE ai_product.support_search
  ON chunk_text
  ATTRIBUTES document_id, product, access_group
  WAREHOUSE = search_refresh_wh
  TARGET_LAG = '1 hour'
AS
SELECT chunk_text, document_id, product, access_group, updated_at
FROM ai_product.governed_chunks;
```

Use current SQL syntax and privilege guidance for the account. Chunk source-aware documents, retain stable document and chunk IDs, and expose only metadata needed for filters and citations.

## Production controls

- Enforce document entitlements before or during retrieval; application filtering must not be the sole security boundary.
- Remove secrets and unsupported sensitive data before indexing.
- Evaluate retrieval recall, precision, citation coverage, groundedness and refusal behavior with a versioned question set.
- Limit retrieved context, prompt size and generated output; monitor search serving, refresh, embedding and AI-function costs.
- Display source citations and distinguish retrieved evidence from generated prose.
- Define behavior for no result, conflicting sources and stale documents.

## Validation and rollback

Test authorized and unauthorized users, uncommon terminology, no-answer questions, conflicting revisions and deleted documents. Canary a new corpus or service, compare it with the active evaluation baseline, and switch application configuration only after acceptance. Roll back to the previous service/corpus and invalidate cached responses; preserve request, retrieval and answer lineage for investigation.

## Official references

- [Cortex Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview)
- [`CREATE CORTEX SEARCH SERVICE`](https://docs.snowflake.com/en/sql-reference/sql/create-cortex-search)
- [Cortex Search costs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-costs)
- [Vector embeddings](https://docs.snowflake.com/en/user-guide/snowflake-cortex/vector-embeddings)

