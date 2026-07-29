# Appendix: Chapter 1 Review Answers

## Purpose

This appendix provides concise answer guidance for the Chapter 1 review questions.

The answers are intentionally short. They are designed for self-checking and interview preparation, not as a replacement for reading the
chapter.

## Conceptual Questions

### 1. What is Kubernetes in production terms?

Kubernetes is an API-driven control system for running containerized workloads across a cluster of machines. It provides declarative state,
controllers, scheduling, service discovery, rollout behavior, and extensibility.

### 2. What is Kubernetes not responsible for?

Kubernetes does not automatically make applications reliable, secure, observable, cost-efficient, or well-designed. Application teams and
platform teams still own architecture, data safety, dependencies, security posture, and operations.

### 3. Why is the Kubernetes API central to the platform model?

The API is the shared contract used by users, controllers, schedulers, kubelets, admission webhooks, operators, and automation. It is where
state is submitted, validated, stored, watched, and reconciled.

### 4. What is desired state?

Desired state is the intended configuration declared through Kubernetes API objects, such as the replica count in a Deployment or the storage
request in a PVC.

### 5. What is reconciliation?

Reconciliation is the controller process of comparing desired state with observed state and taking action to reduce the difference.

### 6. Why are controllers important?

Controllers automate recovery and lifecycle management. They continuously watch state and act when actual state drifts from desired state.

### 7. Why are Pods considered replaceable?

Pods are lifecycle units. Controllers usually replace failed or deleted Pods rather than preserving the same Pod identity forever.

### 8. Why should durable application state not live only in a container filesystem?

Container filesystems are tied to container and Pod lifecycle. Data stored only there can be lost when containers restart or Pods are replaced.

### 9. What is the difference between a Service and a Pod IP?

A Pod IP belongs to a specific Pod lifecycle. A Service provides a stable abstraction that routes to selected ready backend Pods.

### 10. Why does Kubernetes use labels and selectors?

Labels and selectors let Kubernetes group and match objects for Deployments, Services, NetworkPolicies, PDBs, and operational ownership.

## Architecture Questions

### 1. What are the major control-plane components?

The major components are the API server, etcd, scheduler, controller manager, and cloud controller manager where applicable.

### 2. What is the role of the API server?

The API server receives and serves Kubernetes API requests, performs authentication and authorization integration, runs admission, and exposes
cluster state to clients and controllers.

### 3. What is stored in etcd?

etcd stores Kubernetes cluster state, including API objects and configuration state needed by the control plane.

### 4. What does the scheduler do?

The scheduler selects suitable nodes for unscheduled Pods based on resource requests, constraints, affinity, taints, topology, and other
scheduling rules.

### 5. What does the kubelet do?

The kubelet runs on each node and ensures containers for assigned Pods are started, monitored, and reported back to the control plane.

### 6. What is the role of the container runtime?

The runtime pulls images and runs containers on the node under kubelet control.

### 7. What is the role of CNI?

CNI plugins configure Pod networking and implement the cluster network model used by Pods and Services.

### 8. What is the role of CSI?

CSI drivers integrate storage systems with Kubernetes for provisioning, attachment, mounting, expansion, and snapshots where supported.

### 9. What is the difference between control-plane responsibility and node responsibility?

The control plane stores state and makes decisions. Nodes execute assigned workloads through kubelet, runtime, networking, and storage mounts.

### 10. What changes in a managed Kubernetes responsibility model?

The provider usually manages parts of the control plane, but the customer still owns workloads, configuration, node pools, networking,
identity, security policy, observability, and application reliability.

## Networking Questions

### 1. Why are Pod IPs not durable service addresses?

Pod IPs change when Pods are recreated. They identify Pod instances, not long-lived services.

### 2. What problem does a Service solve?

A Service gives clients a stable name and virtual access point for a changing set of backend Pods.

### 3. What are EndpointSlices used for?

EndpointSlices track the current backend endpoints for Services and include readiness-related endpoint state.

### 4. How does Kubernetes DNS help service discovery?

Kubernetes DNS lets workloads reach Services by stable names instead of hard-coded IP addresses.

### 5. What does NetworkPolicy require in order to enforce traffic rules?

NetworkPolicy requires a network plugin that implements NetworkPolicy enforcement.

### 6. What is the difference between north-south and east-west traffic?

North-south traffic enters or leaves the cluster. East-west traffic moves between services or Pods inside the cluster.

### 7. Why does LoadBalancer behavior depend on the environment?

LoadBalancer Services depend on cloud provider or load balancer controller integration. Behavior differs across EKS, AKS, GKE, bare metal, and
other environments.

### 8. Why is Ingress not the same thing as a Service?

A Service provides stable access to Pods. Ingress defines HTTP or HTTPS routing rules and requires an ingress controller.

### 9. Why is Gateway API important for future traffic management?

Gateway API provides a more expressive, role-oriented model for traffic management than traditional Ingress, depending on implementation.

### 10. What should an SRE check when Service traffic fails?

Check Service selectors, Pod labels, EndpointSlices, readiness, DNS, NetworkPolicy, ingress or load balancer state, and application health.

## Storage Questions

### 1. What is the difference between ephemeral and persistent storage?

Ephemeral storage follows Pod or node lifecycle. Persistent storage is intended to survive Pod replacement through PVs, PVCs, and storage
backends.

### 2. What is a PersistentVolumeClaim?

A PVC is a user's request for storage, including size, access mode, StorageClass, and optionally volume mode or data source.

### 3. What is a PersistentVolume?

A PV is a cluster resource representing storage known to Kubernetes, either statically created or dynamically provisioned.

### 4. What is a StorageClass?

A StorageClass describes a storage policy and dynamic provisioning behavior exposed to workloads.

### 5. Why does reclaim policy matter?

Reclaim policy controls what happens to a PV and often the backend storage when a PVC is deleted.

### 6. What does `ReadWriteOnce` imply?

It means the volume can be mounted read-write by a single node. It does not guarantee application-level write safety.

### 7. Why can storage topology affect scheduling?

Some storage exists only in a specific zone or node location. Pods must be scheduled where the volume can attach and mount.

### 8. What is the role of a CSI driver?

A CSI driver connects Kubernetes to a storage backend for operations such as provisioning, attach, mount, resize, snapshot, and clone.

### 9. Why is a snapshot not automatically a complete backup strategy?

Snapshots may be crash-consistent only, provider-scoped, or untested. Backup strategy requires retention, restore testing, consistency, and
recovery objectives.

### 10. What should an SRE avoid deleting during a storage incident?

Avoid deleting PVCs, PVs, backend volumes, or snapshots until reclaim policy, data impact, and recovery options are fully understood.

## Security Questions

### 1. What is the difference between authentication, authorization, and admission?

Authentication identifies the caller. Authorization checks allowed actions. Admission validates, rejects, or mutates requests after those
checks.

### 2. What does RBAC control?

RBAC controls which users, groups, or ServiceAccounts can perform specific verbs on specific Kubernetes resources.

### 3. Why is `cluster-admin` dangerous?

It grants broad cluster-wide authority. If a workload or user with that access is compromised, the blast radius can include the whole cluster.

### 4. What is a ServiceAccount?

A ServiceAccount is an identity for processes running in Pods.

### 5. When should service account token automounting be disabled?

Disable it for workloads that do not need to call the Kubernetes API.

### 6. What are the Pod Security Standards levels?

The levels are Privileged, Baseline, and Restricted.

### 7. Why are Secrets not a complete secret-management solution by default?

Secrets still require encryption at rest, RBAC, rotation, careful mounting, auditability, and protection from logs or support bundles.

### 8. Why are namespaces not complete security boundaries?

Namespaces organize resources and policy, but stronger isolation also requires RBAC, admission, NetworkPolicy, node isolation, and sometimes
separate clusters.

### 9. Why does NetworkPolicy support matter for security?

NetworkPolicy objects only enforce traffic restrictions when the network plugin supports enforcement.

### 10. What evidence is needed during a security incident?

Useful evidence includes audit logs, events, RBAC bindings, ServiceAccount usage, Pod specs, Secret access, node logs, network flow logs, and
application logs.

## Reliability Questions

### 1. Why is replica count not the same as reliability?

Replicas help only when the application can tolerate replacement, traffic distribution, dependency failures, and safe rollout behavior.

### 2. What is the difference between startup, readiness, and liveness probes?

Startup probes protect initialization. Readiness probes control traffic eligibility. Liveness probes trigger restarts for unrecoverable local
failures.

### 3. How can a bad liveness probe cause cascading failure?

If liveness checks dependencies or times out under load, Kubernetes may restart healthy-but-slow Pods, shifting traffic to remaining Pods and
amplifying the outage.

### 4. What does a PodDisruptionBudget protect against?

A PDB limits voluntary evictions for selected Pods, such as during node drains or maintenance.

### 5. What does a PDB not protect against?

It does not prevent all direct deletions, node failures, hardware failures, resource-pressure evictions, or application crashes.

### 6. Why do resource requests affect reliability?

Requests tell the scheduler how much capacity to reserve. Without realistic requests, Pods can be packed onto nodes unsafely.

### 7. Why is autoscaling not instant protection?

Autoscaling depends on metrics, control-loop timing, scheduling, image pulls, readiness, and available node capacity.

### 8. Why does graceful termination matter?

Graceful termination lets Pods stop accepting new work, finish or hand off in-flight work, and exit without unnecessary user impact.

### 9. What makes stateful reliability different from stateless reliability?

Stateful systems must preserve data, identity, ordering, quorum, replication, backups, and restore behavior, not only Pod availability.

### 10. Why should SREs monitor service-level signals, not only Kubernetes object status?

Kubernetes objects can look healthy while users see failures caused by application bugs, bad routing, dependency outages, or data issues.
