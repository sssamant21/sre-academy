# Unified Snowflake Glossary

Version: v1.2.0  
Status: Production Release  
Last vendor validation: 2026-08-15

**Account Usage:** Views in the shared `SNOWFLAKE` database providing retained metadata and usage history, generally with data latency.

**Account:** An administrative Snowflake boundary containing users, roles, warehouses, databases and configuration.

**Auto-clustering:** Snowflake-managed maintenance of clustering for a table with a clustering key.

**Auto-resume:** Warehouse behavior that starts suspended compute when eligible work arrives.

**Auto-suspend:** Warehouse behavior that suspends compute after a configured idle period.

**Budget:** A cost-management capability used to monitor supported consumption, including costs not covered by warehouse resource monitors.

**Cloud services:** Snowflake-managed services for authentication, metadata, optimization, coordination and other control-plane activity.

**Cluster key:** One or more expressions used to influence micro-partition organization for selected workloads.

**Compilation time:** Time used to parse, resolve, optimize and prepare a statement before execution.

**Credit:** Snowflake's unit for consumption of supported compute and services.

**Data sharing:** Controlled access to data between Snowflake accounts without copying the shared data into the consumer account.

**Database role:** A role scoped to privileges within a database and grantable to account roles.

**Dynamic Data Masking:** Policy-driven transformation of column values at query time.

**Dynamic table:** A declarative table refreshed by Snowflake to maintain query results within a target-lag objective.

**Fail-safe:** Snowflake-managed recovery period intended for exceptional recovery by Snowflake, not a user backup mechanism.

**Failover group:** A replication grouping used to support account-level failover capabilities for supported objects.

**Information Schema:** Per-database metadata views and table functions, often used for recent operational evidence.

**Least privilege:** Granting identities only the permissions needed for approved duties.

**Masking policy:** A policy that controls the value returned for a protected column based on execution context.

**Materialized view:** A Snowflake-maintained persisted result for an eligible query definition.

**Micro-partition:** Snowflake's immutable internal unit of table storage with metadata used for pruning and management.

**Multi-cluster warehouse:** A warehouse capable of using multiple compute clusters to address supported concurrency demand.

**Network policy:** An inbound access-control object using allowed or blocked network identifiers, commonly through network rules.

**Network rule:** A named set of network identifiers used by network policies or external access controls according to its mode.

**Organization:** A Snowflake object for administering and observing multiple accounts.

**Partition pruning:** Elimination of irrelevant micro-partitions using metadata and predicates.

**Query hash:** A value used to group repeated query text or parameterized query patterns for analysis.

**Query History:** A UI or SQL history surface containing query identifiers, status and performance metadata.

**Query ID:** A unique identifier for one query execution and its profile, history and operator evidence.

**Query Profile:** Operator-level execution visualization and statistics for a completed query.

**Queued overload time:** Time a statement waits because a warehouse is overloaded.

**Queued provisioning time:** Time a statement waits while compute resources are starting or scaling.

**Replication group:** A grouping of supported objects replicated across regions or accounts.

**Resource monitor:** A warehouse-focused credit control with notification and suspension actions; it does not cover every serverless or AI service.

**Result cache:** Reuse of an eligible persisted query result rather than repeating execution.

**Role:** An access-control principal to which privileges can be granted.

**Role-based access control (RBAC):** Access through privileges granted to roles and roles granted to users or other roles.

**Row access policy:** A policy expression that determines which table or view rows are visible.

**Secure view:** A view designed to protect sensitive definitions and reduce indirect exposure, with security/performance tradeoffs.

**Serverless feature:** A Snowflake-managed capability that uses compute without a user-managed warehouse.

**Service-level indicator (SLI):** A measured signal representing service behavior.

**Service-level objective (SLO):** A target for an SLI over a defined period and scope.

**Snowpipe:** Snowflake's continuous file-loading service.

**Spill:** Intermediate query data written to local or remote storage when operator memory is insufficient.

**Stage:** A named or implicit location used to access files for loading, unloading or related operations.

**Stream:** An object that records change-tracking offsets for supported table changes.

**Target lag:** A best-effort freshness target for a dynamic table, not a guaranteed refresh interval.

**Task:** A scheduled or triggered Snowflake object that executes SQL or supported procedure logic.

**Task graph:** A directed acyclic graph of root and dependent tasks.

**Time Travel:** Access to eligible historical object data within the configured retention period.

**User:** A human or service identity recognized by Snowflake.

**Virtual warehouse:** Independent Snowflake compute used for queries and supported data operations.

**Warehouse load:** A ratio-based measure of running, queued, provisioning or blocked query activity over an interval.

## Official references

- [Snowflake SQL reference](https://docs.snowflake.com/en/sql-reference)
- [Access-control overview](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
