# Case Study: Cortex Search Grounding Failure

Version: v1.5.0
Status: In development
Last vendor validation: 2026-08-16

Fictional composite; documents and questions are synthetic.

## Incident

A support assistant cited an obsolete procedure after a newer document had replaced it. The answer was fluent and included a citation, but retrieval selected an older chunk with similar keywords.

## Evidence

Request traces preserved the query, filters, returned chunks, scores, corpus version and generated answer. The newer document carried a `supersedes_document_id` field, but the Cortex Search source query indexed both versions and the application applied no active-document filter.

## Root cause and recovery

Root cause: document lifecycle metadata was not enforced in the search corpus. Contributors were evaluation focused on answer style rather than source currency, no stale-document test, and cached responses without corpus-version lineage.

The team disabled affected answers, filtered the corpus to active approved documents, refreshed the service, invalidated versioned caches and reran retrieval/grounding evaluations before reopening.

## Preventive actions

- Model document status, validity interval and supersession explicitly.
- Enforce access and active-document filters before generation.
- Log request, corpus version, retrieved chunks and citations.
- Evaluate retrieval recall, source currency, groundedness, refusal and unauthorized-document exclusion.
- Display evidence timestamps and handle conflicting sources.
- Canary corpus/service changes and retain a tested rollback service.

## Official references

- [Cortex Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview)
- [`CREATE CORTEX SEARCH SERVICE`](https://docs.snowflake.com/en/sql-reference/sql/create-cortex-search)
- [Cortex Search costs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-costs)
- [AI Observability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability/reference)
