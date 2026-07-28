# Chapter 9: kube-scheduler

The kube-scheduler decides where Pods should run. Scheduling is a reliability function because placement affects capacity, blast radius, latency, maintenance safety, and workload availability.

## Objectives

By the end of this chapter, readers should be able to:

- Explain how the scheduler filters and scores nodes.
- Diagnose Pending Pods and scheduling failures.
- Review workload placement rules for reliability risk.
- Define operational checks for Kubernetes v1.34 scheduling behavior.

## Architecture

The scheduler watches for Pods without an assigned node. For each unscheduled Pod, it evaluates feasible nodes, scores them, chooses a target node, and binds the Pod. The kubelet on the selected node then attempts to run the Pod.

| Scheduling input | Reliability concern |
| --- | --- |
| Resource requests | Missing or unrealistic requests cause poor placement and evictions. |
| Node affinity | Overly narrow rules can strand Pods during node loss. |
| Pod affinity and anti-affinity | Useful for locality or separation, but expensive and easy to overconstrain. |
| Taints and tolerations | Protect special nodes, but incorrect tolerations bypass isolation. |
| Topology spread constraints | Reduce blast radius when capacity exists across domains. |
| Priority and preemption | Protect critical workloads, but can disrupt lower-priority services. |
| PodDisruptionBudget | Protects availability during voluntary disruption, but can block maintenance. |

## Internal scheduling flow

A scheduling cycle generally includes:

1. Queueing the unscheduled Pod.
2. Filtering nodes that cannot run the Pod.
3. Scoring feasible nodes.
4. Reserving the selected node for the Pod.
5. Binding the Pod to the node through the API server.
6. Waiting for kubelet and runtime execution.

A Pod can remain Pending because no node is feasible, because resources are unavailable, because constraints are too strict, or because external dependencies such as volume binding cannot complete.

## SRE operating guidance

### Treat Pending Pods as capacity signals

A Pending Pod is not always an application bug. It may indicate exhausted capacity, broken autoscaling, unavailable zones, storage topology mismatch, or overly strict placement rules.

### Review constraints before incidents

Affinity, anti-affinity, topology spread constraints, taints, tolerations, and priority classes should be reviewed as part of production readiness. Rules that make sense during normal operation can fail during zone loss or maintenance.

### Align autoscaling with scheduling needs

Cluster autoscaling depends on schedulable intent. If Pods request impossible combinations of CPU, memory, labels, zones, GPUs, storage topology, or taints, autoscaling may not help.

### Use priority classes carefully

Priority should reflect business and platform criticality. Too many high-priority workloads make priority meaningless; incorrect preemption can create cascading incidents.

## Failure scenarios

| Scenario | Symptoms | First checks |
| --- | --- | --- |
| Insufficient resources | Pods remain Pending. | Pod events, node allocatable resources, requests, autoscaler status. |
| Overconstrained placement | Pods cannot schedule despite free capacity. | Node selectors, affinity, taints, topology spread constraints. |
| Zone imbalance | Replicas land in unhealthy or overloaded domains. | Topology labels, spread constraints, node pool capacity. |
| Storage binding failure | Stateful Pods remain Pending. | PVC events, StorageClass topology, available volumes. |
| Preemption surprise | Lower-priority workloads are evicted. | Priority classes, preemption events, disruption budgets. |

## Kubernetes v1.34 notes

For Kubernetes v1.34, review scheduler configuration, plugin behavior, default feature gates, and autoscaler compatibility before upgrading. Confirm custom scheduler profiles or admission policies still match workload expectations.

Before production rollout, verify:

- Scheduler metrics and Pending Pod alerts exist.
- Critical workloads have realistic requests and placement rules.
- Topology labels are consistent across nodes and zones.
- Autoscaler behavior is tested with real workload constraints.
- Priority classes are documented and reviewed.

## Engineering Review

Use these questions in design or readiness reviews:

1. What makes each critical workload schedulable during node or zone loss?
2. Which constraints are required for reliability and which are accidental?
3. Are resource requests based on observed usage and performance targets?
4. Can the autoscaler add capacity that actually satisfies Pending Pods?
5. Which workloads can preempt others and why?

## Chapter review

Readers should be able to explain:

- How filtering, scoring, and binding affect Pod placement.
- How placement rules can improve or reduce reliability.
- How to troubleshoot common Pending Pod scenarios.

## Next steps

Continue to [Chapter 10: kubelet](chapter-10-kubelet.md).
