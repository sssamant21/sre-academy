---
title: "Chapter 3 Glossary"
chapter: 3
section: glossary
status: Draft
review_state: Author Draft
version: 0.1
---

# Chapter 3 Glossary

This glossary defines the core terms used in Chapter 3, Workloads and Scheduling.

The definitions are intentionally production-focused. They explain how an SRE should reason about workload behavior during design reviews,
rollouts, incidents, capacity planning, and platform operations.

## Affinity

A scheduling rule that influences where Pods should run. Node affinity selects nodes based on node labels. Pod affinity places Pods near other
Pods. In production, affinity should be used carefully because hard affinity can reduce scheduler flexibility and cause Pending Pods.

## Anti-Affinity

A scheduling rule that keeps Pods away from other matching Pods. Anti-affinity is commonly used to avoid placing all replicas of a critical
workload on the same node or zone. Hard anti-affinity can improve failure isolation but can also block scheduling when capacity is limited.

## BestEffort QoS

A Pod QoS class assigned when containers have no CPU or memory requests and no CPU or memory limits. BestEffort Pods are the first candidates for
eviction under resource pressure and are usually inappropriate for critical production workloads.

## Burstable QoS

A Pod QoS class assigned when at least one container has a CPU or memory request or limit, but the Pod does not meet the requirements for
Guaranteed QoS. Many production workloads are Burstable, but requests and limits still need to be based on measured behavior.

## Container

A runnable process environment inside a Pod. Kubernetes manages containers through the kubelet and container runtime. In production, container
startup, shutdown, probes, resource usage, and logs are operationally important.

## CronJob

A Kubernetes workload controller that creates Jobs on a time-based schedule. Production CronJobs require review of schedule, concurrency policy,
starting deadline, retry behavior, history limits, idempotency, and observability.

## DaemonSet

A workload controller that runs one Pod on each selected node. DaemonSets are commonly used for node-level agents such as logging, monitoring,
networking, storage, and security components.

## Deployment

A workload controller commonly used for stateless replicated services. A Deployment manages ReplicaSets, supports rolling updates and rollbacks,
and is the default controller choice for many production applications.

## Disruption

An event that causes Pods to stop, be evicted, become unavailable, or be replaced. Disruptions can be voluntary, such as node drains, or
involuntary, such as node failure or node-pressure eviction.

## EndpointSlice

A Kubernetes resource that tracks Service backend endpoints. For workloads, EndpointSlices are important because readiness affects whether a Pod is
included as a traffic endpoint.

## Eviction

The process of terminating a Pod due to policy, node pressure, preemption, or disruption workflows. API-initiated evictions can respect
PodDisruptionBudgets, while node-pressure eviction is driven by kubelet and does not provide the same protection.

## Eviction API

The Kubernetes API mechanism used to request a policy-aware Pod eviction. It is commonly used by node drain workflows and can respect
PodDisruptionBudgets and termination grace periods.

## Guaranteed QoS

A Pod QoS class assigned when every container has CPU and memory requests and limits, and each request equals its corresponding limit. Guaranteed
Pods receive the strongest eviction preference, but limits must still be chosen carefully.

## HorizontalPodAutoscaler

A Kubernetes controller that adjusts the replica count of a scalable workload based on metrics. HPA can scale desired replicas, but it cannot make
Pods schedule, start quickly, become Ready, or create node capacity by itself.

## Init Container

A container that runs to completion before application containers start. Init containers are useful for setup tasks, but slow or failing init
containers delay Pod readiness and can block rollouts.

## Job

A Kubernetes workload controller for finite tasks that should run to completion. Jobs require operational review of completions, parallelism,
backoff limits, deadlines, retries, cleanup, and idempotency.

## kubelet

The node agent that starts containers, runs probes, reports Pod status, mounts volumes, and handles Pod termination on its node after the scheduler
assigns Pods.

## Label Selector

A query over labels used to match Kubernetes objects. Selectors connect Deployments to Pods, Services to backends, PDBs to protected Pods, and many
other relationships. Incorrect selectors can cause severe production impact.

## Liveness Probe

A kubelet probe used to decide whether a container should be restarted. Liveness should detect unrecoverable local failure. Aggressive liveness
probes can cause cascading restarts during overload.

## Namespace

A Kubernetes scope for namespaced objects. Workloads, Services, Jobs, CronJobs, and PDBs commonly live in namespaces. Namespaces help organize
ownership and policy but are not complete isolation boundaries by themselves.

## Node Affinity

A scheduling rule that constrains or prefers nodes based on node labels. Required node affinity is a hard scheduling rule; preferred node affinity
is a scoring preference.

## Node Selector

A simple scheduling constraint that requires a Pod to run only on nodes with matching labels. Node selectors are easy to understand but less
expressive than node affinity.

## Node-Pressure Eviction

A kubelet action that terminates Pods to reclaim resources when a node is under memory, disk, inode, or other resource pressure. Node-pressure
eviction is not the same as API-initiated eviction and does not respect PodDisruptionBudgets.

## Pending Pod

A Pod that has been accepted by the API server but is not yet running. Pending can mean image pull, volume, init, or scheduling work is still in
progress. For scheduling failures, inspect Pod events and node constraints.

## Pod

The smallest deployable workload unit in Kubernetes. A Pod contains one or more containers that share networking and lifecycle. Production Pods are
usually managed by controllers rather than created directly.

## Pod Anti-Affinity

A scheduling rule that discourages or prevents Pods from running near other matching Pods in a topology domain such as a node or zone. It is useful
for spreading replicas but can block scheduling if too strict.

## PodDisruptionBudget

A policy object that limits voluntary disruptions for selected Pods. PDBs are important for maintenance and node drains, but they do not protect
against all failures or create spare capacity.

## Pod Lifecycle

The sequence of states and transitions a Pod moves through from creation to termination. SREs care about scheduling, startup, readiness,
restarts, deletion, graceful termination, and final status.

## Pod Template

The Pod specification embedded inside a controller such as a Deployment, StatefulSet, DaemonSet, Job, or CronJob. Changing a controller's Pod
template usually creates new Pods and may trigger rollout behavior.

## PriorityClass

A Kubernetes object that assigns scheduling priority to Pods. Higher-priority Pods can be scheduled before lower-priority Pods and may preempt
lower-priority Pods when necessary. Use priority carefully because it affects multi-tenant reliability.

## Readiness Probe

A kubelet probe used to decide whether a Pod should receive traffic through Services. Readiness should represent real traffic-serving ability, not
only whether the process is alive.

## ReplicaSet

A controller that maintains a desired number of matching Pod replicas. Deployments create and manage ReplicaSets as part of rollout and rollback
behavior.

## Resource Limit

A maximum resource amount a container can use. Memory limits can cause container termination when exceeded. CPU limits can cause throttling.
Limits should be intentional and tested.

## Resource Request

The amount of CPU, memory, or another resource reserved for scheduling. Requests are the scheduler's placement contract and are also important for
QoS and HPA CPU utilization calculations.

## Restart Policy

A Pod-level setting that controls whether containers should be restarted. Long-running workloads commonly use `Always`; Jobs commonly use
`Never` or `OnFailure` depending on retry behavior.

## Rolling Update

A rollout strategy that gradually replaces old Pods with new Pods. Availability depends on readiness, replica count, surge capacity, disruption
settings, and cluster headroom.

## Scheduler

The control-plane component that assigns unscheduled Pods to nodes. It evaluates resource requests, node state, affinity, topology, taints,
tolerations, volume constraints, and scheduling plugins.

## Startup Probe

A kubelet probe used to determine whether an application has finished starting. Startup probes protect slow-starting containers from premature
liveness failures.

## StatefulSet

A workload controller for applications that need stable network identity, ordered lifecycle, and stable storage association. StatefulSets are common
for databases, queues, and clustered systems, but application-specific operational knowledge is still required.

## Taint

A node property that repels Pods unless those Pods have a matching toleration. Taints are commonly used for dedicated node pools, special hardware,
maintenance, and node health conditions.

## Toleration

A Pod setting that allows scheduling onto nodes with matching taints. A toleration does not force placement; it only permits placement on tainted
nodes.

## Topology Spread Constraint

A scheduling constraint that controls how Pods are distributed across topology domains such as nodes, zones, or custom domains. It is useful for
availability and skew control, but strict constraints can cause Pending Pods.

## Vertical Pod Autoscaling

A resource recommendation or adjustment mechanism for Pod requests. VPA can help tune resource requests, but it must be reviewed carefully with
HPA, rollout behavior, and workload restart tolerance.

## Voluntary Disruption

A planned or operator-initiated action that removes Pods, such as a node drain, node upgrade, or cluster scale-down. PDBs are designed primarily to
limit voluntary disruption for selected Pods.

## Workload Controller

A Kubernetes controller that manages Pods for a workload lifecycle. Examples include Deployment, ReplicaSet, StatefulSet, DaemonSet, Job, and
CronJob.
