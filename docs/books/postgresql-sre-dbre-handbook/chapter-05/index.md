# Chapter 5 -- PostgreSQL Transactions, MVCC, Locking, and Concurrency

**Status:** Complete -- Canonical

**Workflow:** Draft -> Technical Review -> Production Review -> Revised Final / Canonical Edition

**Master Chapter 5 Structure v1.0 -- LOCKED**

Chapter 5 covers transaction semantics, MVCC, snapshots and isolation, lock architecture, blocking, deadlocks, transaction-ID safety, contention engineering, observability, troubleshooting, and production case studies.

## Sections

- [5.1 -- PostgreSQL Transaction Architecture and Fundamentals](5.1-postgresql-transaction-architecture-and-fundamentals.md) -- Complete
- [5.2 -- Transaction Lifecycle: BEGIN, COMMIT, ROLLBACK, and SAVEPOINT](5.2-transaction-lifecycle-begin-commit-rollback-and-savepoint.md) -- Complete
- [5.3 -- ACID Properties and PostgreSQL Transaction Guarantees](5.3-acid-properties-and-postgresql-transaction-guarantees.md) -- Complete
- [5.4 -- MVCC Architecture and Tuple Versioning](5.4-mvcc-architecture-and-tuple-versioning.md) -- Complete
- [5.5 -- Transaction IDs, XIDs, and Transaction Visibility](5.5-transaction-ids-xids-and-transaction-visibility.md) -- Complete
- [5.6 -- Snapshots and MVCC Visibility Rules](5.6-snapshots-and-mvcc-visibility-rules.md) -- Complete
- [5.7 -- Transaction Isolation Levels](5.7-transaction-isolation-levels.md) -- Complete
- [5.8 -- Read Committed Isolation](5.8-read-committed-isolation.md) -- Complete
- [5.9 -- Repeatable Read Isolation](5.9-repeatable-read-isolation.md) -- Complete
- [5.10 -- Serializable Isolation and SSI](5.10-serializable-isolation-and-ssi.md) -- Complete
- [5.11 -- Read-Only and Deferrable Transactions](5.11-read-only-and-deferrable-transactions.md) -- Complete
- [5.12 -- Subtransactions, SAVEPOINTs, and Transaction Error Handling](5.12-subtransactions-savepoints-and-transaction-error-handling.md) -- Complete
- [5.13 -- PostgreSQL Lock Manager Architecture](5.13-postgresql-lock-manager-architecture.md) -- Complete
- [5.14 -- Table-Level Locks and Lock Modes](5.14-table-level-locks-and-lock-modes.md) -- Complete
- [5.15 -- Row-Level Locks and Row Locking Behavior](5.15-row-level-locks-and-row-locking-behavior.md) -- Complete
- [5.16 -- Page-Level, Advisory, and Other Lock Types](5.16-page-level-advisory-and-other-lock-types.md) -- Complete
- [5.17 -- Explicit Locking and SELECT FOR UPDATE/SHARE](5.17-explicit-locking-and-select-for-update-share.md) -- Complete
- [5.18 -- Lock Queues, Wait Events, and Blocking Chains](5.18-lock-queues-wait-events-and-blocking-chains.md) -- Complete
- [5.19 -- Deadlocks: Detection, Diagnosis, and Prevention](5.19-deadlocks-detection-diagnosis-and-prevention.md) -- Complete
- [5.20 -- Long-Running Transactions and idle in transaction](5.20-long-running-transactions-and-idle-in-transaction.md) -- Complete
- [5.21 -- Transaction ID Wraparound and Freeze Management](5.21-transaction-id-wraparound-and-freeze-management.md) -- Complete
- [5.22 -- Concurrency Contention and High-Contention Workloads](5.22-concurrency-contention-and-high-contention-workloads.md) -- Complete
- [5.23 -- Transaction and Lock Monitoring, Metrics, and Alerting](5.23-transaction-and-lock-monitoring-metrics-and-alerting.md) -- Complete
- [5.24 -- Transaction/Concurrency Troubleshooting and Production Runbooks](5.24-transaction-concurrency-troubleshooting-and-production-runbooks.md) -- Complete
- [5.25 -- Production Transaction, Locking, and Deadlock Case Studies](5.25-production-transaction-locking-and-deadlock-case-studies.md) -- Complete

## Canonical Safety Principles

- Keep transactions as short as business correctness permits.
- Treat isolation level as an application correctness contract, not a tuning knob.
- Expect serialization failures and deadlocks to require transaction-level retry where applicable.
- Diagnose blockers before terminating sessions.
- Monitor transaction age, lock waits, deadlocks, and XID/MultiXact age continuously.
- Never disable wraparound protection to solve performance pressure.
- Use explicit/advisory locking only with documented ownership and ordering rules.
- Automate observation aggressively and destructive intervention conservatively.
