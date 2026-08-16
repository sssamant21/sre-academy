# Iceberg Lakehouse Table

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

## Choose catalog ownership first

| Requirement | Primary option |
|---|---|
| Snowflake controls lifecycle and writes | Snowflake-managed Iceberg table |
| Existing REST catalog remains authority | Externally managed table or catalog-linked database |
| Multiple engines require catalog interoperability | Validate Open Catalog or supported REST-catalog pattern |

Do not create competing writers until the catalog and commit protocol explicitly support them. Catalog ownership determines refresh behavior, write support, cleanup responsibility and recovery.

## Snowflake-managed skeleton

```sql
CREATE OR REPLACE ICEBERG TABLE lakehouse.sales.order_lines (
  order_id NUMBER,
  product_id NUMBER,
  order_date DATE,
  net_amount NUMBER(18,2)
)
CATALOG = 'SNOWFLAKE'
EXTERNAL_VOLUME = 'lakehouse_volume'
BASE_LOCATION = 'sales/order_lines/'
TARGET_FILE_SIZE = '64MB';
```

The external volume uses a storage integration-style trust boundary; never embed cloud keys. For an external catalog, create and scope a catalog integration and use the catalog-specific `CREATE ICEBERG TABLE` or catalog-linked database workflow.

## Production controls

- Restrict the external volume to a dedicated path and validate cloud IAM from both sides.
- Record catalog authority, supported writers, partition evolution, target file size and maintenance ownership.
- Monitor snapshot age, file count and size, metadata growth, catalog sync, query pruning and failed commits.
- Test engine compatibility for data types, deletes, schema and partition evolution before declaring interoperability.
- Treat `DROP` and purge semantics as catalog-specific; external catalogs may own physical cleanup.

## Validation and rollback

Write synthetic rows through the authorized engine, query from every approved engine, evolve a compatible column, and reconcile snapshots and counts. For rollback, stop all writers first, identify the last valid snapshot through the owning catalog, restore or create a safe reference according to the selected table type, then reconcile storage and catalog metadata. Never delete object-storage files manually as a first response.

## Official references

- [Iceberg tables](https://docs.snowflake.com/en/user-guide/tables-iceberg)
- [Create an Iceberg table](https://docs.snowflake.com/en/user-guide/tables-iceberg-create)
- [Catalog integrations](https://docs.snowflake.com/en/user-guide/tables-iceberg-configure-catalog-integration)
- [`CREATE ICEBERG TABLE`](https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table)

