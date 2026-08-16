# Case Study: Iceberg Catalog Staleness

Version: v1.5.0
Status: In development
Last vendor validation: 2026-08-16

Fictional composite; catalog and storage names are illustrative.

## Incident

A third-party engine committed a new Iceberg snapshot, but Snowflake queries remained on the prior snapshot beyond the catalog refresh objective. Object storage contained the new metadata and data files; Snowflake's external-catalog table had not refreshed successfully.

```sql
SHOW ICEBERG TABLES LIKE 'ORDER_LINES' IN SCHEMA LAKEHOUSE.SALES;
ALTER ICEBERG TABLE lakehouse.sales.order_lines REFRESH;
```

The manual refresh returned an authorization error. Cloud audit records showed that a catalog-role rotation had removed metadata-read permissions while leaving object-data reads intact. This explained why existing snapshots remained queryable but new metadata could not be discovered.

## Root cause and recovery

Root cause: the external catalog integration's cloud role lost catalog metadata permission during rotation. Contributors were permission testing limited to existing queries, no refresh-status alert, and unclear catalog ownership.

The team stopped other catalog changes, restored least-privilege metadata access, manually refreshed, and reconciled snapshot IDs, schema, counts and partitions across engines. It did not delete metadata files or point Snowflake directly at an unverified metadata path.

## Preventive actions

- Test metadata discovery and commit/refresh behavior after credential rotation.
- Monitor `SHOW ICEBERG TABLES` refresh status and catalog-integration health.
- Assign one accountable catalog owner and document authorized writers.
- Preserve snapshot IDs in reconciliation and incident evidence.
- Rehearse rollback through the owning catalog rather than object-storage deletion.
- For Snowflake-managed tables, evaluate current Horizon Catalog access; older Open Catalog synchronization is no longer the recommended pattern.

## Official references

- [Automatic Iceberg refresh](https://docs.snowflake.com/en/user-guide/tables-iceberg-auto-refresh)
- [`ALTER ICEBERG TABLE REFRESH`](https://docs.snowflake.com/en/sql-reference/sql/alter-iceberg-table-refresh)
- [Manage Iceberg tables](https://docs.snowflake.com/en/user-guide/tables-iceberg-manage)
- [Horizon Catalog external-engine access](https://docs.snowflake.com/en/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)

