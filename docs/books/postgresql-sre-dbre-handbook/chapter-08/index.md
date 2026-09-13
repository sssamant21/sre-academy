# Chapter 8 — PostgreSQL Vacuum, Autovacuum, Bloat, and Maintenance

Status: **IN PROGRESS — 21/25 CANONICAL**

Master Chapter 8 Structure v1.0 — **LOCKED**

## Sections

- 8.1 — Vacuum Architecture and Maintenance Fundamentals — Complete — Canonical
- 8.2 — MVCC Cleanup, Dead Tuples, and Reusable Space — Complete — Canonical
- 8.3 — Standard VACUUM Internals and Processing Phases — Complete — Canonical
- 8.4 — Autovacuum Architecture: Launcher, Workers, and Scheduling — Complete — Canonical
- 8.5 — Autovacuum Trigger Thresholds and Scale Factors — Complete — Canonical
- 8.6 — Per-Table Autovacuum Configuration and High-Churn Tables — Complete — Canonical
- 8.7 — Vacuum Cost-Based Delay, Throttling, and Resource Control — Complete — Canonical
- 8.8 — Vacuum Memory, Parallel Vacuum, and Maintenance Resources — Complete — Canonical
- 8.9 — Visibility Map, All-Visible, and All-Frozen Pages — Complete — Canonical
- 8.10 — Transaction ID Freezing and Anti-Wraparound Vacuum — Complete — Canonical
- 8.11 — Multixact Aging, Freezing, and Wraparound Protection — Complete — Canonical
- 8.12 — Long Transactions, Old Snapshots, and Vacuum Blockers — Complete — Canonical
- 8.13 — Replication Slots, Standbys, and Cleanup Horizons — Complete — Canonical
- 8.14 — Heap Bloat Architecture, Detection, and Interpretation — Complete — Canonical
- 8.15 — Index Bloat, Dead Index Tuples, and Index Cleanup — Complete — Canonical
- 8.16 — VACUUM FULL, Table Rewrites, and Physical Space Reclamation — Complete — Canonical
- 8.17 — REINDEX and Index Maintenance Strategy — Complete — Canonical
- 8.18 — ANALYZE, Planner Statistics, and Autovacuum Integration — Complete — Canonical
- 8.19 — Partitioned Tables and Maintenance Strategy — Complete — Canonical
- 8.20 — Vacuum Progress, Statistics, Logs, and Observability — Complete — Canonical
- 8.21 — Vacuum, Autovacuum, Bloat, and Wraparound Alerting — Complete — Canonical
- 8.22 — Autovacuum Tuning Methodology and Capacity Planning — Planned
- 8.23 — Vacuum and Bloat Troubleshooting and Failure Scenarios — Planned
- 8.24 — Maintenance Automation and Production Runbooks — Planned
- 8.25 — Production Vacuum, Bloat, and Wraparound Case Studies — Planned

## Canonical production principles

Routine standard VACUUM is the default maintenance mechanism; VACUUM FULL is a controlled rewrite requiring additional working space and an ACCESS EXCLUSIVE lock. Autovacuum should be tuned from workload churn and table size rather than disabled as a routine response to performance concerns. Vacuum health must be assessed through cleanup throughput, dead-tuple trends, freeze age, blocker horizons, worker saturation, I/O impact, and maintenance runway. Long-running transactions and retained horizons can prevent effective cleanup even when workers are active. Anti-wraparound maintenance is a correctness requirement. Heap and index bloat require evidence-based diagnosis rather than size alone. REINDEX is structural maintenance that should be driven by correctness or persistent physical inefficiency, with the smallest justified scope and explicit locking, capacity, WAL, replication, and failure-recovery controls. ANALYZE is planner-maintenance infrastructure: statistics freshness must be judged against workload churn and data-distribution change, with targeted per-table thresholds, column statistics targets, extended statistics, partition-parent maintenance, and post-ANALYZE estimate validation used where evidence requires them. Partitioned-table maintenance must distinguish the logical parent from physical partitions, use workload- and lifecycle-aware per-partition maintenance, explicitly protect parent statistics and transaction-age correctness, monitor future/default partition behavior, and strongly gate destructive retention operations. Vacuum observability must separate maintenance activity, progress, effectiveness, and efficiency, combining phase-aware PostgreSQL progress views, cumulative relation statistics, XID/MXID safety, blocker horizons, PostgreSQL-native I/O/WAL telemetry, logs, infrastructure signals, replica health, and application impact. Maintenance alerting must emphasize sustained risk, failed recovery, retained correctness horizons, shrinking runway, and workload-aware severity rather than isolated metrics; alerting should be configuration-aware, deduplicated, phase-aware, and paired with runbooks while keeping destructive remediation behind explicit human safety gates. Automation should aggressively collect evidence and forecast risk while keeping destructive maintenance behind explicit safety gates.

Technical baseline: PostgreSQL 18 official documentation for routine vacuuming, VACUUM, ANALYZE, autovacuum configuration, planner statistics, extended statistics, declarative partitioning, partition ATTACH/DETACH lifecycle, pg_class and pg_inherits, statistics/progress reporting, transaction-ID and multixact freezing, visibility maps, routine reindexing, REINDEX, index-maintenance progress reporting, VACUUM/ANALYZE progress reporting, pg_stat_io, pg_stat_wal, pg_stat_replication, replication slots, standby conflicts, autovacuum logging, anti-wraparound thresholds, vacuum failsafe settings, autovacuum worker capacity, and maintenance alerting inputs.
