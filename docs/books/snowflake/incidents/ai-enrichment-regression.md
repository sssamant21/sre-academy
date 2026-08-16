# Case Study: AI Enrichment Quality and Cost Regression

Version: v1.5.0
Status: In development
Last vendor validation: 2026-08-16

Fictional composite; model and cost figures are illustrative.

## Incident

Support-ticket classification acceptance fell from 93% to 71% while daily AI consumption doubled. The deployment had changed both prompt version and model, preventing immediate attribution from aggregate business metrics.

## Evidence

Lineage columns identified the affected prompt/model pair. Cortex AI usage history showed higher input and output token volume per ticket. A golden evaluation set revealed that a new prompt embedded entire email threads instead of the latest customer message, diluting the classification signal and increasing tokens.

## Root cause and recovery

Root cause: an unbounded prompt-construction change shipped with a model change and bypassed the evaluation gate. Contributors were two variables changed in one release, no per-record token guardrail, and acceptance monitored only daily.

The team stopped the pending batch, restored the prior prompt/model configuration, and reprocessed only records carrying the failed version. Low-confidence results remained quarantined for human review.

## Preventive actions

- Change prompt or model independently unless the combined release is explicitly evaluated.
- Version prompt, model, input selector and output schema on every result.
- Enforce maximum input, output and batch size.
- Monitor accuracy, parse failure, abstention, latency and tokens per accepted result.
- Use current Cortex usage-history views for cost attribution and thresholds.
- Require human review for high-impact or low-confidence decisions.

## Official references

- [Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)
- [Cortex AI Function cost management](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-func-cost-management)
- [AI cost and governance](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance)
- [AI Observability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability/reference)

