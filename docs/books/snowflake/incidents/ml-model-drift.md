# Case Study: ML Model Drift and Alert Fatigue

Version: v1.5.0
Status: Production Release
Last vendor validation: 2026-08-16

Fictional composite; evaluation figures are illustrative.

## Incident

An operational anomaly model began flagging normal daily credit usage after a planned workload migration. Alert volume tripled, and responders started ignoring notifications.

## Evidence

Model lineage showed training data ended before the new workload launch. Feature distributions and residuals shifted at cutover, while platform health and billing reconciliation were normal. Backtesting confirmed the model interpreted the new stable baseline as anomalous.

## Root cause and recovery

Root cause: a material workload change invalidated the model's training distribution without triggering re-evaluation. Contributors were no drift threshold, no model-to-service dependency record, and paging directly from model output without persistence or severity logic.

The team disabled paging while preserving detections, restored deterministic high-severity cost thresholds, built a clean post-migration training window, and shadow-tested a new model version before controlled promotion.

## Preventive actions

- Register model version, training window, features, metrics and service dependencies.
- Monitor input distribution, residuals, precision, recall, false-alert rate and detection delay.
- Trigger review on platform, schedule, pricing or workload changes.
- Route predictions through an operational policy with persistence, suppression and owner.
- Shadow and canary new versions; keep the prior model callable for rollback.
- Never train automatically on unresolved incident periods.

## Official references

- [Anomaly Detection](https://docs.snowflake.com/en/user-guide/ml-functions/anomaly-detection)
- [Snowflake Model Registry](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/overview)
- [Model management](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-management)
- [Time-series preprocessing](https://docs.snowflake.com/en/user-guide/ml-functions/preprocessing)
