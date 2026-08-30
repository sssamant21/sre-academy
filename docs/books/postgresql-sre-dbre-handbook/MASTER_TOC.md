# PostgreSQL SRE & DBRE Handbook

## Master Table of Contents v1.0

Status: LOCKED

This 24-chapter structure is the authoritative source of truth for the PostgreSQL SRE & DBRE Handbook. Chapter names, numbering, or ordering must not be changed without explicit project approval.

## Chapters

1. PostgreSQL Architecture and Internals
2. PostgreSQL Installation, Configuration, Patching, and Upgrades
3. PostgreSQL Database and Object Administration
4. PostgreSQL Storage Architecture and Capacity Management
5. PostgreSQL Transactions, MVCC, Locking, and Concurrency
6. PostgreSQL Query Processing, Performance Tuning, and Optimization
7. PostgreSQL Index Architecture, Design, and Optimization
8. PostgreSQL Vacuum, Autovacuum, Bloat, and Maintenance
9. PostgreSQL WAL, Checkpoints, Backup, and Recovery
10. PostgreSQL Replication and High Availability
11. PostgreSQL Security, Authentication, Authorization, and Auditing
12. PostgreSQL Monitoring, Observability, and Alerting
13. PostgreSQL Connection Management and PgBouncer
14. PostgreSQL Reliability Engineering and Production Operations
15. PostgreSQL Performance Engineering and Capacity Planning
16. PostgreSQL on AWS RDS
17. Amazon Aurora PostgreSQL
18. Azure Database for PostgreSQL
19. Google Cloud SQL for PostgreSQL
20. PostgreSQL on Kubernetes
21. PostgreSQL Production Incidents, Troubleshooting, and Root Cause Analysis
22. PostgreSQL Enterprise DBA and SRE Operations
23. PostgreSQL Automation, Infrastructure as Code, and Self-Healing Operations
24. PostgreSQL Enterprise Reference Architectures and Production Runbooks

## Chapter Structure Locks

- Chapter 1 section sequence: LOCKED
- Chapter 2 section sequence: Published
- Master Chapter 3 Structure v1.0 -- LOCKED
- Master Chapter 4 Structure v1.1 -- LOCKED
- Master Chapter 5 Structure v1.0 -- LOCKED and COMPLETE
- Master Chapter 6 Structure v1.0 -- LOCKED and COMPLETE

Chapter 3 through Chapter 6 locked section titles, numbering, and order must not be changed without explicit project approval.

## Chapter 5 Locked Section Sequence

5.1 PostgreSQL Transaction Architecture and Fundamentals
5.2 Transaction Lifecycle: BEGIN, COMMIT, ROLLBACK, and SAVEPOINT
5.3 ACID Properties and PostgreSQL Transaction Guarantees
5.4 MVCC Architecture and Tuple Versioning
5.5 Transaction IDs, XIDs, and Transaction Visibility
5.6 Snapshots and MVCC Visibility Rules
5.7 Transaction Isolation Levels
5.8 Read Committed Isolation
5.9 Repeatable Read Isolation
5.10 Serializable Isolation and SSI
5.11 Read-Only and Deferrable Transactions
5.12 Subtransactions, SAVEPOINTs, and Transaction Error Handling
5.13 PostgreSQL Lock Manager Architecture
5.14 Table-Level Locks and Lock Modes
5.15 Row-Level Locks and Row Locking Behavior
5.16 Page-Level, Advisory, and Other Lock Types
5.17 Explicit Locking and SELECT FOR UPDATE/SHARE
5.18 Lock Queues, Wait Events, and Blocking Chains
5.19 Deadlocks: Detection, Diagnosis, and Prevention
5.20 Long-Running Transactions and idle in transaction
5.21 Transaction ID Wraparound and Freeze Management
5.22 Concurrency Contention and High-Contention Workloads
5.23 Transaction and Lock Monitoring, Metrics, and Alerting
5.24 Transaction/Concurrency Troubleshooting and Production Runbooks
5.25 Production Transaction, Locking, and Deadlock Case Studies

## Chapter 6 Locked Section Sequence

6.1 PostgreSQL Query Processing Architecture and Lifecycle
6.2 Parser, Analyzer, Rewriter, Planner, and Executor
6.3 Query Planner and Optimizer Architecture
6.4 Planner Cost Model and Cost Parameters
6.5 Cardinality, Selectivity, and Row-Count Estimation
6.6 Planner Statistics and ANALYZE
6.7 Extended Statistics and Correlated Columns
6.8 EXPLAIN Fundamentals and Plan Trees
6.9 EXPLAIN ANALYZE, BUFFERS, WAL, and Production-Safe Plan Analysis
6.10 Sequential, Index, Index-Only, and Bitmap Scan Strategies
6.11 Nested Loop, Hash, and Merge Join Strategies
6.12 Sorting, Aggregation, DISTINCT, and GROUP BY Execution
6.13 CTEs, Subqueries, Views, and Query Transformation
6.14 Partition Pruning and Partition-Wise Query Planning
6.15 Query Memory: work_mem, Hash Memory, and Temporary Spill
6.16 Parallel Query Architecture and Parallel Plans
6.17 JIT Compilation and CPU-Intensive Query Execution
6.18 Prepared Statements, Generic Plans, and Custom Plans
6.19 pg_stat_statements and Query Workload Profiling
6.20 Slow Query Identification and Performance Baselines
6.21 Query Tuning Methodology and Optimization Workflow
6.22 Plan Regression, Statistics Drift, and Performance Instability
6.23 Query Performance Monitoring, Metrics, and Alerting
6.24 Query Performance Troubleshooting and Production Runbooks
6.25 Production Query Performance Incidents and Case Studies
