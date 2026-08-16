# Slowly Changing Dimension Type 2

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

## Use when

Use SCD Type 2 when analytics must reproduce the attributes that were valid at an event time. Use Type 1 overwrite when history has no business or regulatory value.

## Model contract

```sql
CREATE TABLE core.customer_dim (
  customer_sk NUMBER AUTOINCREMENT,
  customer_id VARCHAR NOT NULL,
  segment VARCHAR,
  valid_from TIMESTAMP_TZ NOT NULL,
  valid_to TIMESTAMP_TZ,
  is_current BOOLEAN NOT NULL,
  source_version VARCHAR,
  attribute_hash VARCHAR,
  loaded_at TIMESTAMP_LTZ NOT NULL
);
```

For each business key, require at most one current row and non-overlapping validity ranges. Deduplicate a source batch by a deterministic source version before applying it.

## Transactional implementation outline

1. Stage one canonical row per `customer_id` and source version.
2. Calculate a stable hash of tracked attributes.
3. In one transaction, expire current rows whose hash changed.
4. Insert new keys and changed versions with `is_current = TRUE`.
5. Commit only after uniqueness and overlap assertions pass.

```sql
BEGIN;

UPDATE core.customer_dim d
SET valid_to = s.effective_at, is_current = FALSE
FROM work.customer_changes s
WHERE d.customer_id = s.customer_id
  AND d.is_current
  AND d.attribute_hash <> s.attribute_hash;

INSERT INTO core.customer_dim
  (customer_id, segment, valid_from, valid_to, is_current,
   source_version, attribute_hash, loaded_at)
SELECT s.customer_id, s.segment, s.effective_at, NULL, TRUE,
       s.source_version, s.attribute_hash, CURRENT_TIMESTAMP()
FROM work.customer_changes s
LEFT JOIN core.customer_dim d
  ON d.customer_id = s.customer_id AND d.is_current
WHERE d.customer_id IS NULL OR d.attribute_hash <> s.attribute_hash;

COMMIT;
```

## Production controls

- Define late-arriving correction behavior before launch; effective time and arrival time are different.
- Reject ambiguous duplicate source versions instead of choosing an arbitrary row.
- Assert one current row per key, no inverted ranges and no overlaps.
- Preserve deletion events as an approved tombstone or closed interval.
- Reconcile changed, expired and inserted counts to the source batch.

## Validation and rollback

Test new, unchanged, changed, deleted, duplicate and late records. Rerunning a source version must not create another dimension version. Roll back with a pre-deployment clone or Time Travel according to retention policy, then replay from durable staged changes.

## Official references

- [`MERGE`](https://docs.snowflake.com/en/sql-reference/sql/merge)
- [Transactions](https://docs.snowflake.com/en/sql-reference/transactions)
- [Window functions](https://docs.snowflake.com/en/user-guide/functions-window-using)
- [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel)

