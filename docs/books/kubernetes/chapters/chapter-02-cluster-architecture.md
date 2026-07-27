# Chapter 2: Cluster Architecture and Control Plane

This chapter explains the Kubernetes cluster architecture that SREs need to understand for operations, troubleshooting, and reliability planning.

## Objectives

By the end of this chapter, readers should be able to:

- Describe the major control plane and node components.
- Explain how desired state moves through the Kubernetes API.
- Identify common control plane and node failure modes.
- Define baseline health checks for cluster operations.

## Core concepts

### Control plane

The control plane exposes the Kubernetes API and coordinates cluster state. The main components are:

| Component | Role | Operational concern |
| --- | --- | --- |
| API server | Front door for Kubernetes API requests. | Latency, availability, authentication, admission, and rate limits. |
| etcd | Consistent store for cluster state. | Quorum, storage latency, backups, and corruption recovery. |
| Scheduler | Assigns Pods to Nodes. | Pending Pods, constraints, taints, tolerations, and resource pressure. |
| Controller manager | Reconciles desired state. | Controller lag, failed reconciliation, and event storms. |
| Cloud controller manager | Integrates provider resources. | Load balancers, node lifecycle, routes, and provider API limits. |

Managed Kubernetes platforms often hide some control plane operations, but SREs still need to understand symptoms and provider integration points.

### Worker nodes

Worker nodes run workloads. Important node components include:

- kubelet, which manages Pods on the node.
- container runtime, which starts and stops containers.
- kube-proxy or equivalent dataplane, which handles Service traffic.
- CNI plugin, which configures Pod networking.
- CSI plugin, which integrates persistent storage.

Node health is workload health. If node resource pressure, disk pressure, networking failure, or runtime instability is ignored, application incidents follow.

### Desired state and reconciliation

Kubernetes works by reconciling desired state. Users submit objects to the API server. Controllers observe state and attempt to make reality match that desired state. This model is powerful, but it means incidents often appear as reconciliation failures rather than one obvious failed command.

When troubleshooting, ask:

1. What object declares the desired state?
2. Which controller owns reconciliation?
3. What events or conditions show reconciliation progress?
4. Which dependency prevents convergence?

## Operating practices

### Monitor API server health

Track API server request latency, error rates, saturation, and authentication or admission failures. Slow API operations can delay scheduling, rollouts, autoscaling, and incident mitigation.

### Protect etcd and cluster state

For self-managed clusters, document etcd backup, restore, compaction, defragmentation, and quorum recovery. For managed clusters, document the provider backup and support boundaries.

### Track node readiness

Node conditions such as `Ready`, `MemoryPressure`, `DiskPressure`, `PIDPressure`, and `NetworkUnavailable` are core operational signals. Treat repeated node churn as a platform reliability issue.

### Understand provider dependencies

Managed clusters depend on cloud APIs for node lifecycle, load balancers, identity, storage, and networking. Provider API throttling or regional degradation can look like Kubernetes failure.

## Hands-on checks

Use these checks during cluster review:

- List control plane health signals available from the provider or monitoring stack.
- Identify node pools and their workload purpose.
- Confirm node readiness alerts exist.
- Confirm cluster version, upgrade policy, and support window.
- Confirm backup and restore expectations for cluster state.

## Chapter review

Readers should be able to explain:

- How API server, scheduler, controllers, and nodes interact.
- Why desired state reconciliation shapes troubleshooting.
- Which node and control plane signals should page an operator.

## Next steps

Continue to [Chapter 3: Workloads and Scheduling](chapter-03-workloads-scheduling.md).
