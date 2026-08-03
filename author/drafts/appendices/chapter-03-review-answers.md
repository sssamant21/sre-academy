---
title: "Chapter 3 Review Answers"
chapter: 3
section: appendix
status: Draft
review_state: Author Draft
version: 0.1
---

# Chapter 3 Review Answers

This appendix provides reference answers for the Chapter 3 review questions.

The answers are concise by design. They are intended for self-checking, engineering review preparation, and interview practice. They do not replace
reading the chapter or running the labs.

## 1. Why should long-running production services usually use a controller instead of standalone Pods?

Controllers provide reconciliation. If a Pod fails or is deleted, a controller such as a Deployment, StatefulSet, or DaemonSet can create a
replacement to restore desired state.

Standalone Pods do not provide rollout, replica management, scaling, or replacement behavior. They are useful for simple tests, but they are rarely
the right production unit for long-running services.

## 2. What is the relationship between a Deployment, ReplicaSet, and Pod?

A Deployment owns rollout intent and manages ReplicaSets. A ReplicaSet maintains a desired number of Pods for a specific Pod template revision.
Pods are the actual workload instances created from that template.

During a rollout, the Deployment creates or scales ReplicaSets so old Pods are replaced by new Pods in a controlled way.

## 3. Why should a Deployment selector be treated carefully after creation?

The selector defines which Pods belong to the Deployment. If it is wrong, the Deployment can adopt unintended Pods or fail to manage the Pods it
should manage.

Changing selector logic is risky because it affects ownership, rollout behavior, Service matching assumptions, and operational tooling that depends
on labels.

## 4. When is a StatefulSet more appropriate than a Deployment?

Use a StatefulSet when the workload needs stable network identity, ordered lifecycle, stable storage association, or predictable identity per
replica.

Examples include databases, quorum systems, brokers, and clustered systems. A StatefulSet does not automatically make these systems safe; the
application still needs correct replication, backup, recovery, and operational procedures.

## 5. Why do DaemonSets commonly run infrastructure agents?

DaemonSets run Pods on selected nodes, which makes them a good fit for node-level agents. Examples include log collectors, metrics agents,
security agents, storage node plugins, and CNI components.

Their lifecycle is tied to node membership: when a node joins, the DaemonSet can place an agent there; when a node leaves, the agent Pod leaves
with it.

## 6. What fields matter most when reviewing a CronJob for production?

Review the schedule, time zone behavior where applicable, `concurrencyPolicy`, `startingDeadlineSeconds`, `suspend`, retry settings inherited by
Jobs, successful and failed history limits, and cleanup strategy.

Also review idempotency, runtime duration, external side effects, alerting, and whether missed or overlapping runs are safe.

## 7. What does the scheduler use to decide whether a Pod can fit on a node?

The scheduler evaluates node readiness, resource requests, node selectors, node affinity, pod affinity or anti-affinity, taints and tolerations,
topology spread constraints, volume constraints, and scheduler plugin behavior.

It schedules using declared requests and constraints, not only observed CPU or memory utilization graphs.

## 8. What is the difference between a hard scheduling constraint and a preferred scheduling rule?

A hard constraint must be satisfied before the Pod can be scheduled. Examples include `nodeSelector`, required node affinity, required pod
affinity, required pod anti-affinity, and some topology spread settings.

A preferred rule influences scoring but does not block scheduling if the preference cannot be met. Preferred rules are useful when placement is
important but availability is more important than perfect placement.

## 9. Why can an overly strict topology spread constraint cause Pending Pods?

Topology spread constraints can require Pods to be distributed across topology domains such as nodes or zones. If the cluster lacks enough eligible
nodes or zones, or if other constraints reduce the candidate set, the scheduler may not find a valid placement.

This is often a deliberate tradeoff: Kubernetes is preserving the spread rule instead of placing Pods in a way that violates the declared policy.

## 10. How do taints and tolerations interact?

A taint on a node repels Pods that do not tolerate it. A toleration on a Pod permits that Pod to be scheduled onto a node with the matching taint.

A toleration does not force placement onto the tainted node. It only removes the taint as a blocking condition. Other scheduling rules still apply.

## 11. What is the difference between CPU requests and CPU limits?

A CPU request is the amount of CPU reserved for scheduling and used by Kubernetes to decide whether a Pod fits on a node. It is also important for
HPA CPU utilization calculations.

A CPU limit is an upper bound enforced by the runtime. If a container reaches its CPU limit, it can be throttled. CPU limits should be intentional
because excessive throttling can create latency and throughput problems.

## 12. Why can memory limits cause container restarts?

Memory is not throttled in the same way CPU is. If a container exceeds its memory limit, it can be terminated by the kernel or runtime and then
restarted according to the Pod restart policy.

SREs should review memory limits against real high-water marks, garbage collection behavior, caches, and traffic spikes.

## 13. How is QoS class determined?

QoS class is derived from Pod container resource requests and limits.

A Pod is BestEffort when it has no CPU or memory requests or limits. It is Guaranteed when every container has CPU and memory requests and limits,
and each request equals its corresponding limit. Other Pods with at least some requests or limits are Burstable.

## 14. Why are BestEffort Pods risky for production critical workloads?

BestEffort Pods have no declared CPU or memory reservation. They are most vulnerable during node resource pressure and are typically evicted before
Burstable and Guaranteed Pods.

For critical workloads, missing requests also harms scheduling accuracy, capacity planning, and autoscaling behavior.

## 15. Why does HPA CPU utilization depend on CPU requests?

For CPU utilization targets, HPA compares observed CPU usage to the Pod's CPU request. If requests are missing or unrealistic, HPA cannot calculate
meaningful utilization or may scale based on misleading ratios.

This makes CPU requests part of the autoscaling contract, not only scheduling metadata.

## 16. What does HPA change when it scales a Deployment?

HPA updates the scale target's desired replica count through the scale subresource. For a Deployment, that changes the desired number of replicas.
The Deployment and ReplicaSet controllers then create or remove Pods to match the new desired state.

HPA does not directly run containers, add nodes, fix readiness, or guarantee that new Pods can schedule.

## 17. Why can HPA scale up and the application still remain overloaded?

HPA can increase desired replicas, but new Pods may remain Pending, take too long to start, fail readiness, lack node capacity, hit scheduling
constraints, or overwhelm downstream dependencies.

The scaling metric can also be wrong. For example, CPU may not represent queue depth, request latency, database saturation, or external rate
limits.

## 18. What does a PodDisruptionBudget protect against?

A PodDisruptionBudget limits voluntary disruptions for selected Pods. It is commonly used during node drains, cluster upgrades, node maintenance,
and some scale-down workflows that use policy-aware eviction.

It helps prevent too many selected Pods from being unavailable at the same time during planned operations.

## 19. What does a PDB not protect against?

A PDB does not protect against all failure modes. It does not prevent node crashes, hardware failures, network partitions, node-pressure eviction,
all preemption cases, unsafe direct deletion, or application bugs.

It also does not create replicas, spare capacity, healthy readiness, or correct application behavior.

## 20. Why is readiness important during rollouts and drains?

Readiness controls whether a Pod is eligible to receive Service traffic. During a rollout, new Pods should not receive traffic until they are ready.
During a drain, PDB status relies on Pod readiness to decide how many Pods are currently healthy.

Incorrect readiness can cause traffic to go to broken Pods or can block maintenance because Kubernetes thinks too few Pods are healthy.

## 21. Why should liveness probes be conservative?

Liveness probes restart containers. If they are too aggressive, dependency slowness, high load, garbage collection pauses, or temporary saturation
can trigger restarts across many replicas.

A good liveness probe should detect local unrecoverable failure, not ordinary traffic pressure or downstream service latency.

## 22. When should a startup probe be used?

Use a startup probe when a container can take longer to initialize than the normal liveness tolerance allows. Examples include JVM warmup, cache
loading, model loading, migrations, and recovery work.

When configured, startup probes delay normal liveness and readiness probing until startup succeeds, reducing premature restarts.

## 23. What should happen during graceful Pod termination?

The Pod should stop accepting new work, be removed from normal traffic routing, drain in-flight requests or background work, handle SIGTERM, and
exit before the termination grace period expires.

External systems such as ingress controllers, load balancers, service meshes, clients, and queues may also need compatible drain behavior.

## 24. Why can a rollout with multiple replicas still cause downtime?

Multiple replicas are not enough if rollout settings, readiness, capacity, and dependencies are unsafe. Downtime can occur if new Pods fail
readiness, old Pods terminate too quickly, surge Pods cannot schedule, liveness restarts healthy-but-overloaded Pods, or downstream systems become
saturated.

Replica count is only one part of availability.

## 25. What information would you collect before approving a workload for production?

Collect workload ownership, SLOs, traffic profile, replica count rationale, resource measurements, rollout strategy, readiness and liveness design,
autoscaling plan, PDB, topology requirements, dependency map, observability, security posture, backup or recovery needs, and runbooks.

Approval should be based on measured behavior and operational readiness, not only a syntactically valid manifest.

# Interview-Style Answer Guide

## A Deployment has ten replicas, but all Pods are running on two nodes. What risks do you see and how would you fix placement?

The workload has poor failure-domain distribution. A single node failure could remove a large share of capacity, and maintenance on one node could
cause user impact.

Review scheduler constraints, node labels, topology spread constraints, pod anti-affinity, node pool capacity, and zone distribution. Add topology
spread or anti-affinity where appropriate, but avoid rules so strict that they block scheduling during incidents.

## A Pod is Pending with an event saying no nodes have enough CPU. The cluster CPU graph looks mostly idle. Explain the mismatch.

The scheduler uses CPU requests and node allocatable capacity, not only observed usage. A cluster can look idle while still lacking enough
unallocated requested CPU for a new Pod.

Check Pod requests, node allocatable resources, existing requested resources, quotas, taints, affinity, and topology constraints.

## A service has an HPA, but traffic spikes still cause errors. Walk through your investigation.

Start with service SLOs, latency, error rate, saturation, and traffic shape. Inspect HPA status, current metrics, desired replicas, min and max
replicas, and events.

Then verify whether new Pods scheduled, started, passed readiness, and received traffic. Check node capacity, image pull time, startup latency,
downstream dependency saturation, and whether the autoscaling metric matches the real bottleneck.

## A node drain is blocked by a PDB during a cluster upgrade. What is your decision process?

Treat the blocked drain as an availability signal. Identify which workload and PDB are blocking, inspect `disruptionsAllowed`, replica count,
readiness, selector correctness, and current workload health.

Prefer restoring health, scaling replicas, adding capacity, or postponing maintenance. Only override the PDB through an approved incident or
maintenance process after understanding the risk.

## A new release passes liveness but fails readiness. What does that mean operationally?

The process is alive but not ready to serve normal traffic. It should not receive Service traffic until readiness succeeds.

Investigate application startup, dependencies, configuration, migrations, ports, readiness endpoint logic, logs, events, and whether the release
should be paused or rolled back.

## A CronJob sometimes runs two copies of the same task at once. Which fields would you inspect?

Inspect `schedule`, `concurrencyPolicy`, `startingDeadlineSeconds`, Job runtime, retry behavior, deadlines, and whether previous Jobs are still
active when the next schedule arrives.

If duplicate execution is unsafe, use `concurrencyPolicy: Forbid` or application-level idempotency and locking where needed.

## A Pod restarts every few minutes only under high traffic. How would you evaluate the liveness probe and resource limits?

Check `kubectl describe pod`, restart reasons, exit codes, events, container logs, liveness probe failures, CPU throttling, memory usage, OOM kills,
and request latency during traffic spikes.

If liveness depends on a slow endpoint or external dependency, separate liveness from readiness. If memory limits are too low or CPU throttling is
severe, tune resources based on measured behavior.

## A StatefulSet Pod is stuck terminating after node failure. What additional risks exist compared with a stateless Deployment?

StatefulSet Pods often have stable identity and attached persistent storage. A stuck terminating Pod can block replacement with the same identity,
and volume attachments may prevent the Pod from starting elsewhere.

The SRE must consider storage consistency, force detach behavior, quorum, application recovery, and provider-specific node failure procedures.

## A rollout creates new Pods, but they remain Pending because of topology spread constraints. What tradeoff is Kubernetes enforcing?

Kubernetes is enforcing the declared placement policy instead of placing Pods in a way that violates spread requirements. This protects failure-domain
distribution but can reduce availability if there is not enough eligible capacity.

Decide whether to add capacity, relax constraints, adjust `maxSkew`, or accept delayed rollout based on service criticality and risk.

## A team wants `minAvailable: 100%` for every PDB. What operational problem can that create?

It can block every voluntary disruption because no selected Pod is allowed to become unavailable. Node drains, upgrades, autoscaler scale-down, and
maintenance can stall indefinitely.

A better PDB balances workload availability with operational progress. Use replica count, SLOs, capacity, readiness behavior, and maintenance needs
to choose a realistic budget.
