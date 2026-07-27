# Chapter 5: Storage, State, and Backup

This chapter covers Kubernetes storage and the operational expectations for stateful workloads, persistent volumes, backups, and recovery.

## Objectives

By the end of this chapter, readers should be able to:

- Explain PersistentVolume and PersistentVolumeClaim behavior.
- Identify storage risks for stateful workloads.
- Define backup and restore requirements for Kubernetes applications.
- Review stateful workload readiness for production.

## Core concepts

### Kubernetes storage objects

Kubernetes separates storage requests from storage implementation.

| Object | Purpose | Operational concern |
| --- | --- | --- |
| StorageClass | Defines dynamic provisioning behavior. | Reclaim policy, expansion, topology, and provider settings. |
| PersistentVolume | Represents provisioned storage. | Lifecycle, attachment, reclaim, and data retention. |
| PersistentVolumeClaim | Requests storage for a workload. | Size, access mode, binding, and expansion. |
| VolumeSnapshot | Captures point-in-time volume state. | Consistency, restore process, and provider support. |
| StatefulSet | Manages identity-aware Pods and volume claims. | Ordered rollout, stable identity, and recovery sequencing. |

### Stateful workload risks

Stateful workloads increase operational complexity. They may depend on stable network identity, ordered startup, durable storage, zone affinity, backup consistency, and careful recovery procedures.

Before running stateful workloads on Kubernetes, decide whether Kubernetes is the right operating environment. Some databases are better consumed as managed services, while others can run well with a mature operator and tested recovery model.

### Backups and restore

A backup strategy is incomplete until restore is tested. Backups should define:

- What data is protected.
- How often backups run.
- Where backups are stored.
- Who can restore them.
- How restore is validated.
- Which recovery point and recovery time objectives apply.

## Operating practices

### Review StorageClass defaults

Default StorageClasses can create durable resources with surprising behavior. Confirm volume type, reclaim policy, encryption, expansion support, zone topology, and snapshot support.

### Plan for node and zone failure

Storage topology matters. A Pod may be schedulable only where its volume can attach. Multi-zone services need a design that handles node and zone loss without trapping critical workloads.

### Separate application backup from cluster backup

Cluster object backup is not the same as application data backup. A reliable recovery plan may need Kubernetes manifests, secrets, persistent volume snapshots, database dumps, and provider-level recovery procedures.

### Test restore regularly

Restore tests should be scheduled and documented. A restore that only works with one expert present is not an operational capability.

## Hands-on checks

For each stateful workload, confirm:

- StorageClass behavior is documented.
- PVC size, access mode, and expansion expectations are clear.
- Backup and restore procedures are tested.
- Recovery point and recovery time objectives are known.
- Node, zone, and provider failure modes are understood.
- Secrets and configuration needed for restore are protected.

## Chapter review

Readers should be able to explain:

- How Kubernetes provisions and attaches persistent storage.
- Why backup and restore require more than a PVC snapshot.
- Which questions determine whether a stateful workload is production-ready.

## Next steps

Continue to [Chapter 6: Observability and Operations](chapter-06-observability-operations.md).
