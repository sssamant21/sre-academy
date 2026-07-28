# Chapter 8: etcd

etcd is the strongly consistent datastore behind Kubernetes cluster state. A healthy API server still depends on etcd quorum, storage latency, disk reliability, and backup discipline.

## Objectives

By the end of this chapter, readers should be able to:

- Explain what Kubernetes stores in etcd.
- Describe quorum, leader election, compaction, and snapshots.
- Identify etcd failure modes that affect the Kubernetes API.
- Define backup and restore expectations for Kubernetes v1.34 clusters.

## Architecture

etcd stores Kubernetes objects as key-value records. The kube-apiserver is the normal client; cluster operators should avoid direct writes to etcd except during well-understood recovery procedures.

Production etcd clusters require an odd number of voting members, reliable low-latency networking, fast durable disks, monitored leader health, and tested backups.

| Concept | SRE concern |
| --- | --- |
| Quorum | The cluster must keep majority agreement to accept writes. |
| Leader | Write traffic flows through the leader; leader churn increases latency. |
| WAL | Write-ahead log durability depends on disk performance and reliability. |
| Snapshot | Point-in-time backup used for disaster recovery. |
| Compaction | Removes old revisions; required for storage health. |
| Defragmentation | Reclaims disk space after compaction. |

## Internal implementation

Kubernetes stores desired state in etcd through the API server storage layer. Controllers do not normally talk to etcd directly. Watches depend on revision history, so compaction and watch behavior are connected.

When etcd is slow, the API server can become slow. When etcd loses quorum, write operations fail. When disk fills, the cluster can enter a degraded or read-only state depending on the failure.

## SRE operating guidance

### Monitor quorum and leader health

Alert on leader changes, failed proposals, unavailable members, and loss of quorum risk. A single failed member in a three-member cluster should trigger timely repair because the next failure can stop writes.

### Protect disk latency

etcd is sensitive to fsync latency. Use dedicated durable disks where possible. Monitor disk latency, database size, backend commit duration, WAL fsync duration, and free space.

### Test snapshots and restores

A snapshot is only useful if restore is tested. Document who can take snapshots, where they are stored, how they are encrypted, and how restore is validated.

### Coordinate with managed provider boundaries

Managed Kubernetes providers often hide etcd operations. SREs still need to know the provider backup guarantees, support escalation path, control plane recovery behavior, and customer responsibilities.

## Failure scenarios

| Scenario | Symptoms | First checks |
| --- | --- | --- |
| Lost quorum | API writes fail, controllers cannot reconcile. | Member health, network partitions, provider control plane status. |
| Slow disk | High API write latency and watch lag. | WAL fsync duration, backend commit duration, disk saturation. |
| Database growth | Increased latency, disk pressure, maintenance alerts. | DB size, compaction status, defragmentation needs. |
| Bad restore plan | Recovery delays during control plane incident. | Snapshot age, restore drill evidence, runbook ownership. |
| Network partition | Leader changes, failed proposals, member instability. | Member connectivity, latency, packet loss, maintenance events. |

## Kubernetes v1.34 notes

For Kubernetes v1.34, confirm the etcd version and support matrix used by the distribution or managed provider. Review upgrade guidance for backup compatibility, storage format expectations, and disaster recovery procedures.

Before a v1.34 control plane upgrade, verify:

- A current etcd snapshot or provider-backed recovery point exists.
- Restore procedures are tested in a non-production environment.
- etcd member health is clean before starting upgrade work.
- Disk pressure and database size are within operating limits.
- Control plane maintenance windows and rollback expectations are documented.

## Engineering Review

Use these questions in design or readiness reviews:

1. What is the expected recovery time if etcd state is lost?
2. Where are snapshots stored and who can restore them?
3. Which alerts indicate quorum risk before outage?
4. How is etcd disk latency isolated from other workloads?
5. What provider responsibilities apply for managed clusters?

## Chapter review

Readers should be able to explain:

- Why etcd quorum and disk latency matter to Kubernetes reliability.
- How snapshots, compaction, and defragmentation support operations.
- Which etcd risks remain visible even in managed Kubernetes platforms.

## Next steps

Continue to [Chapter 9: kube-scheduler](chapter-09-kube-scheduler.md).
