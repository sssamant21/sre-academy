# PostgreSQL SRE & DBRE Handbook

## Master Table of Contents v1.0

Status: LOCKED

This 24-chapter structure is the authoritative source of truth for the PostgreSQL SRE & DBRE Handbook. Chapter names, numbering, or ordering must not be changed without explicit project approval.

## Recovery and Reconciliation Note

Repository history, merged PR evidence, and current handbook files verify Chapter 1 as `PostgreSQL Architecture and Internals` and verify the locked Chapter 1 section sequence from 1.1 through 1.24.

The original historical Master TOC v1.0 file was not recoverable from the current repository, reachable git history, branches, deleted files, or PR metadata. Chapters 2 through 24 are therefore preserved here from the project-approved reconciliation list supplied on 2026-08-17. If an older approved Master TOC artifact is later recovered, that historical evidence takes precedence for exact wording.

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

Chapter 3, Chapter 4, and Chapter 5 section titles, numbering, and order must not be renamed, renumbered, merged, split, reordered, deleted, or extended with new numbered sections unless explicitly approved later.

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
