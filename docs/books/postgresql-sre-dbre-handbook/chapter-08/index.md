# Chapter 8 — PostgreSQL Vacuum, Autovacuum, Bloat, and Maintenance

Status: **IN PROGRESS — 5/25 CANONICAL**

Master Chapter 8 Structure v1.0 — **LOCKED**

## Sections

- 8.1 — Vacuum Architecture and Maintenance Fundamentals — Complete — Canonical
- 8.2 — MVCC Cleanup, Dead Tuples, and Reusable Space — Complete — Canonical
- 8.3 — Standard VACUUM Internals and Processing Phases — Complete — Canonical
- 8.4 — Autovacuum Architecture: Launcher, Workers, and Scheduling — Complete — Canonical
- 8.5 — Autovacuum Trigger Thresholds and Scale Factors — Complete — Canonical
- 8.6 — Per-Table Autovacuum Configuration and High-Churn Tables — Planned
- 8.7 — Vacuum Cost-Based Delay, Throttling, and Resource Control — Planned
- 8.8 — Vacuum Memory, Parallel Vacuum, and Maintenance Resources — Planned
- 8.9 — Visibility Map, All-Visible, and All-Frozen Pages — Planned
- 8.10 — Transaction ID Freezing and Anti-Wraparound Vacuum — Planned
- 8.11 — Multixact Aging, Freezing, and Wraparound Protection — Planned
- 8.12 — Long Transactions, Old Snapshots, and Vacuum Blockers — Planned
- 8.13 — Replication Slots, Standbys, and Cleanup Horizons — Planned
- 8.14 — Heap Bloat Architecture, Detection, and Interpretation — Planned
- 8.15 — Index Bloat, Dead Index Tuples, and Index Cleanup — Planned
- 8.16 — VACUUM FULL, Table Rewrites, and Physical Space Reclamation — Planned
- 8.17 — REINDEX and Index Maintenance Strategy — Planned
- 8.18 — ANALYZE, Planner Statistics, and Autovacuum Integration — Planned
- 8.19 — Partitioned Tables and Maintenance Strategy — Planned
- 8.20 — Vacuum Progress, Statistics, Logs, and Observability — Planned
- 8.21 — Vacuum, Autovacuum, Bloat, and Wraparound Alerting — Planned
- 8.22 — Autovacuum Tuning Methodology and Capacity Planning — Planned
- 8.23 — Vacuum and Bloat Troubleshooting and Failure Scenarios — Planned
- 8.24 — Maintenance Automation and Production Runbooks — Planned
- 8.25 — Production Vacuum, Bloat, and Wraparound Case Studies — Planned

## Canonical production principles

Routine standard VACUUM is the default maintenance mechanism; VACUUM FULL is a controlled rewrite requiring additional working space and an ACCESS EXCLUSIVE lock. Autovacuum should be tuned from workload churn and table size rather than disabled as a routine response to performance concerns. Vacuum health must be assessed through cleanup throughput, dead-tuple trends, freeze age, blocker horizons, worker saturation, I/O impact, and maintenance runway. Long-running transactions and retained horizons can prevent effective cleanup even when workers are active. Anti-wraparound maintenance is a correctness requirement. Heap and index bloat require evidence-based diagnosis rather than size alone. Automation should aggressively collect evidence and forecast risk while keeping destructive maintenance behind explicit safety gates.

Technical baseline: PostgreSQL 18 official documentation for routine vacuuming, VACUUM, autovacuum configuration, statistics/progress reporting, transaction-ID and multixact freezing, visibility maps, and routine reindexing.
