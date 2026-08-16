# Governed AI Enrichment

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

## Use when

Use Cortex AI Functions for bounded classification, extraction, summarization or generation over governed Snowflake data. Do not use an LLM result as an authoritative decision without an approved evaluation and human-review policy.

## Implementation pattern

Persist the prompt version, model, input identity and raw output so results are reproducible and auditable.

```sql
INSERT INTO ai_work.ticket_enrichment
  (ticket_id, prompt_version, model_name, generated_at, result)
SELECT ticket_id,
       'support_category_v3',
       '<approved_model>',
       CURRENT_TIMESTAMP(),
       AI_CLASSIFY(ticket_text, ['billing', 'access', 'performance', 'other'])
FROM governed.support_tickets
WHERE ticket_id IN (SELECT ticket_id FROM ai_work.pending_tickets);
```

Use the current model catalog and regional-availability page to select the model. Model capability, latency, price and region support can change.

## Production controls

- Classify inputs before use; prohibit sensitive or regulated content unless policy and regional processing permit it.
- Grant the narrow Snowflake Cortex database role to a dedicated execution role.
- Version prompts and keep a representative golden dataset with acceptance thresholds.
- Validate structured output before downstream use; quarantine malformed or unsafe results.
- Batch intentionally, limit input size and monitor both input and output tokens.
- Track usage with the current Cortex usage-history views and enforce workload cost thresholds.

## Evaluation and rollback

Measure accuracy by category, abstention or parse failures, harmful output, latency and cost per accepted result. Compare a candidate model or prompt against the active version before promotion. Roll back by switching the controlled prompt/model configuration, stopping pending batches and reprocessing only records whose lineage identifies the failed version.

## Official references

- [Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)
- [Regional availability and models](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-regional-availability)
- [AI Function cost](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-cost)
- [AI cost management](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-func-cost-management)

