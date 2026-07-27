# Chapter 3: Workloads and Scheduling

This chapter covers how Kubernetes runs workloads and how SREs can make scheduling, rollout, and recovery behavior predictable.

## Objectives

By the end of this chapter, readers should be able to:

- Explain the purpose of common workload controllers.
- Use scheduling primitives to influence placement safely.
- Define health probes and resource requests for reliable workloads.
- Identify common rollout and scheduling failure modes.

## Core concepts

### Workload controllers

Kubernetes workload controllers manage Pods for different operating patterns.

| Controller | Use case | Reliability concern |
| --- | --- | --- |
| Deployment | Stateless services and rolling updates. | Rollout safety, availability, and rollback. |
| StatefulSet | Ordered, identity-aware workloads. | Storage, identity, sequencing, and recovery. |
| DaemonSet | One Pod per matching node. | Node coverage and platform add-ons. |
| Job | Finite batch work. | Completion, retries, and cleanup. |
| CronJob | Scheduled batch work. | Missed runs, concurrency, and backoff. |

Choose the controller that matches the workload lifecycle. Do not force stateful or ordered workloads into a Deployment just because it is familiar.

### Scheduling primitives

The scheduler places Pods on Nodes based on requested resources, constraints, and policies. Important primitives include:

- Resource requests and limits.
- Node selectors and node affinity.
- Pod affinity and anti-affinity.
- Taints and tolerations.
- Topology spread constraints.
- Priority classes and preemption.

Scheduling policy should express reliability intent, not accidental preferences. For example, topology spread constraints can reduce blast radius, while anti-affinity can prevent replicas from landing on the same failure domain.

### Probes and lifecycle

Probes tell Kubernetes when containers are ready, alive, or still starting.

| Probe | Purpose | Common mistake |
| --- | --- | --- |
| Readiness | Controls service traffic. | Marking a Pod ready before dependencies are usable. |
| Liveness | Restarts stuck containers. | Restarting slow but healthy processes. |
| Startup | Protects slow startup from liveness probes. | Omitting it for large applications with long boot time. |

Readiness should represent whether the Pod can serve traffic. Liveness should represent unrecoverable local failure.

## Operating practices

### Set resource requests deliberately

Resource requests drive scheduling decisions. Missing or unrealistic requests create noisy neighbors, poor bin packing, and surprise evictions. Production workloads should define CPU and memory requests based on observed behavior and performance targets.

### Make rollouts observable

A safe rollout requires visibility into desired replicas, available replicas, readiness, error rates, latency, and dependency health. Rollback should be documented before rollout, not improvised during an incident.

### Design for failure domains

Spread replicas across nodes, zones, or topology domains when service availability requires it. Validate that the cluster has enough capacity to honor these constraints during node loss.

### Use disruption budgets carefully

PodDisruptionBudgets protect availability during voluntary disruption. They do not protect against every failure. A strict budget with too few replicas can block maintenance and upgrades.

## Hands-on checks

For each production workload, confirm:

- Controller type matches workload behavior.
- CPU and memory requests are defined.
- Readiness and liveness probes match real health semantics.
- Rollout and rollback expectations are documented.
- Replica spread matches the required failure domain.
- Disruption budgets exist where maintenance safety requires them.

## Chapter review

Readers should be able to explain:

- Which workload controller fits a given application pattern.
- How scheduling rules affect placement and availability.
- How probes and resources influence rollout safety.

## Next steps

Continue to [Chapter 4: Networking, Ingress, and Service Discovery](chapter-04-networking-ingress.md).
