# Snowflake SQL and Command Index

Version: v1.2.0  
Status: Production Release  
Last vendor validation: 2026-08-15

This is a task-oriented handbook index, not a replacement for the complete Snowflake command reference. Verify current syntax and privileges before execution.

## Session context

| Command/function | Purpose | Handbook guidance |
|---|---|---|
| `USE ROLE` | Select primary role | Make execution authority explicit |
| `USE SECONDARY ROLES` | Control secondary roles | Avoid hidden privilege assumptions |
| `USE WAREHOUSE` | Select compute | Separate analysis from workload compute |
| `USE DATABASE`, `USE SCHEMA` | Select namespace | Prefer explicit context or fully qualified names |
| `CURRENT_ROLE()`, `CURRENT_WAREHOUSE()` | Inspect context | Capture with incident evidence |

## Object lifecycle

| Command | Primary use |
|---|---|
| `CREATE/ALTER/DROP DATABASE` | Database lifecycle |
| `CREATE/ALTER/DROP SCHEMA` | Schema lifecycle |
| `CREATE/ALTER/DROP TABLE` | Table lifecycle |
| `CREATE/ALTER/DROP VIEW` | View lifecycle |
| `CREATE/ALTER/DROP WAREHOUSE` | Compute lifecycle |
| `CREATE/ALTER/DROP TASK` | Scheduled workload lifecycle |
| `CREATE/ALTER/DROP DYNAMIC TABLE` | Declarative pipeline lifecycle |
| `CREATE/ALTER/DROP RESOURCE MONITOR` | Warehouse cost guardrails |

Use `IF EXISTS` or `IF NOT EXISTS` only where supported and operationally appropriate.

## Data operations

| Command | Use |
|---|---|
| `SELECT` | Query data |
| `INSERT` | Add rows |
| `UPDATE` | Modify rows |
| `DELETE` | Remove rows |
| `MERGE` | Conditional insert/update/delete |
| `COPY INTO <table>` | Load staged files |
| `COPY INTO <location>` | Unload query/table results |
| `TRUNCATE TABLE` | Remove all rows while retaining the table |

Treat destructive statements as change-controlled operations with explicit targets and validation.

## Access control

| Command | Use |
|---|---|
| `CREATE ROLE`, `CREATE DATABASE ROLE` | Define access principals |
| `GRANT <privilege>` | Grant object/account privileges |
| `GRANT ROLE`, `GRANT DATABASE ROLE` | Build role hierarchy |
| `REVOKE` | Remove privileges or roles |
| `SHOW GRANTS` | Inspect current grants |
| `EXPLAIN_GRANTABLE_PRIVILEGES` | Discover grantable privileges for supported objects |

## Monitoring and evidence

| Surface | Operational use |
|---|---|
| `QUERY_HISTORY` | Query status and performance |
| `GET_QUERY_OPERATOR_STATS` | Operator-level statistics |
| `WAREHOUSE_LOAD_HISTORY` | Running, queued, provisioning and blocked load |
| `WAREHOUSE_METERING_HISTORY` | Warehouse credit usage |
| `LOGIN_HISTORY` | Authentication evidence |
| `TASK_HISTORY` | Task and graph execution |
| `DYNAMIC_TABLE_REFRESH_HISTORY` | Refresh state and freshness evidence |
| `RESULT_SCAN(LAST_QUERY_ID())` | Process recent `SHOW` or query results |

Use bounded UTC time ranges, explicit columns and documented telemetry latency.

## Operations

| Command | Use | Safety note |
|---|---|---|
| `ALTER WAREHOUSE ... SUSPEND/RESUME` | Compute control | Confirm shared-workload impact |
| `ALTER WAREHOUSE ... SET WAREHOUSE_SIZE` | Resize compute | Record old value and rollback |
| `EXECUTE TASK` | Run an owned/operable task | Confirm replay safety |
| `ALTER TASK ... RESUME/SUSPEND` | Control scheduling | Resume child tasks before root in a graph |
| `ALTER DYNAMIC TABLE ... REFRESH` | Request manual refresh | Avoid refresh loops |
| `ALTER DYNAMIC TABLE ... SUSPEND/RESUME` | Control refresh lifecycle | Assess reinitialization and downstream effects |
| `SYSTEM$CANCEL_QUERY` | Cancel a query | Require incident authority and exact query ID |

## Inspection

`SHOW` and `DESCRIBE` commands inspect warehouses, tasks, dynamic tables, policies, integrations, users, roles and other objects. Output schemas can evolve; process results by column name and validate automation after behavior changes.

## Official references

- [SQL command reference](https://docs.snowflake.com/en/sql-reference-commands)
- [All commands](https://docs.snowflake.com/en/sql-reference/sql-all)
- [All functions](https://docs.snowflake.com/en/sql-reference/functions-all)
- [Table functions](https://docs.snowflake.com/en/sql-reference/functions-table)
- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
