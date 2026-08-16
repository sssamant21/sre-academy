# Operational Anomaly Detection with Snowflake ML

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

## Use when

Use Snowflake ML anomaly detection for time-series values whose unusual behavior should be compared with a learned forecast. Use deterministic thresholds when the rule is known and explainability or immediate response is more important than learned seasonality.

## Model pattern

Train on a clean, representative window that excludes known incidents and includes expected seasonality.

```sql
CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION ops.credit_anomaly_model(
  INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'OPS.CREDIT_TRAINING_DATA'),
  TIMESTAMP_COLNAME => 'USAGE_HOUR',
  TARGET_COLNAME => 'CREDITS_USED',
  LABEL_COLNAME => ''
);

CALL ops.credit_anomaly_model!DETECT_ANOMALIES(
  INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'OPS.CREDIT_SCORING_DATA'),
  TIMESTAMP_COLNAME => 'USAGE_HOUR',
  TARGET_COLNAME => 'CREDITS_USED'
);
```

Confirm the current class signature, privilege and warehouse requirements; multi-series and labeled-data options require additional parameters.

## Production controls

- Validate missing, duplicate and misaligned timestamps before training.
- Keep training window, features, model parameters, model version and evaluation results.
- Measure precision, recall, false-alert rate and detection delay against labeled incidents.
- Route anomalies through an operational rule that includes severity, suppression and owner—not directly to automated remediation.
- Monitor inference failures, data freshness, distribution drift and credit consumption.
- Retrain on an approved cadence or material drift, not automatically after every incident.

## Validation and rollback

Backtest across normal seasonality and known incidents, then shadow the model without paging. Promote only when it improves the existing control. Roll back by disabling the alert binding and restoring the prior model/version or deterministic threshold; keep detected results and model lineage for RCA.

## Official references

- [Anomaly Detection](https://docs.snowflake.com/en/user-guide/ml-functions/anomaly-detection)
- [`SNOWFLAKE.ML.ANOMALY_DETECTION`](https://docs.snowflake.com/en/sql-reference/classes/anomaly_detection)
- [Real-world time-series preprocessing](https://docs.snowflake.com/en/user-guide/ml-functions/preprocessing)
- [Snowflake ML Functions](https://docs.snowflake.com/en/guides-overview-ml-functions)
