---
title: "Chapter 2 Glossary"
chapter: 2
section: glossary
status: Draft
review_state: Author Draft
version: 0.1
---

# Chapter 2 Glossary

This glossary defines the core terms used in Chapter 2, Cluster Architecture.

## Add-On

A component installed into the cluster to provide supporting platform functionality beyond the core Kubernetes control plane. Examples include
CoreDNS, CNI plugins, CSI drivers, ingress controllers, metrics agents, policy engines, and observability agents.

## Admission Control

The API server phase that evaluates write requests after authentication and authorization but before persistence. Admission can mutate or reject
objects and is commonly used for policy, security, defaults, and validation.

## Admission Webhook

An HTTP callback used by the API server during admission. Mutating webhooks can modify requests. Validating webhooks can allow or reject requests.
Because webhooks sit in the API write path, webhook latency or outages can affect cluster operations.

## API Server

The Kubernetes control-plane component that exposes the Kubernetes API. All clients, controllers, kubelets, schedulers, and automation interact
with cluster state through the API server.

## API Version Skew

A supported temporary difference between Kubernetes component minor versions during an upgrade. Unsupported skew can cause compatibility and
correctness problems even if individual components appear healthy.

## Authentication

The process of proving the identity of a user, service account, or automation client before the Kubernetes API server handles the request.

## Authorization

The process of deciding whether an authenticated identity is allowed to perform a requested action. RBAC is the most common Kubernetes
authorization mechanism.

## CNI

Container Network Interface. The plugin interface used by Kubernetes networking implementations to configure Pod networking. CNI behavior affects
Pod IP allocation, routing, policy enforcement, and sometimes Service dataplane behavior depending on the implementation.

## CSI

Container Storage Interface. The standard interface used by modern Kubernetes storage drivers to provision, attach, mount, expand, snapshot, or
otherwise manage storage volumes.

## Cloud Controller Manager

A Kubernetes control-plane component that integrates Kubernetes with cloud-provider APIs. It can manage cloud load balancers, node metadata,
routes, or other provider-specific behavior depending on the provider.

## Cluster Architecture

The structure and interaction model of Kubernetes control-plane components, worker nodes, networking, storage, security controls, add-ons,
upgrade processes, and operational boundaries.

## ClusterRole

An RBAC object that defines permissions at cluster scope. A ClusterRole can be bound cluster-wide with a ClusterRoleBinding or bound into a
namespace with a RoleBinding.

## ClusterRoleBinding

An RBAC binding that grants a ClusterRole to users, groups, or service accounts at cluster scope. It should be used carefully because it can grant
broad permissions across the cluster.

## Container Runtime

The node-level software used by kubelet to run containers. Kubernetes commonly uses CRI-compatible runtimes. The runtime is part of the node trust
and workload execution boundary.

## Control Plane

The set of components responsible for cluster state and coordination. Core control-plane components include the API server, etcd,
kube-scheduler, and kube-controller-manager. Some clusters also run cloud-controller-manager and additional policy or admission components.

## Controller

A reconciliation loop that watches cluster state and acts to move actual state toward desired state. Examples include Deployment, ReplicaSet,
Node, Job, and EndpointSlice controllers.

## Controller Manager

The control-plane component that runs many built-in Kubernetes controllers. These controllers reconcile objects such as nodes, endpoints,
replicas, namespaces, and service accounts.

## CoreDNS

The common DNS add-on used in Kubernetes clusters. It provides DNS resolution for Services and Pods according to Kubernetes DNS behavior.

## DaemonSet

A workload controller that runs a copy of a Pod on selected nodes. Common uses include CNI agents, log collectors, monitoring agents, storage
node plugins, and security agents.

## Deployment

A workload controller that manages rollout and availability for stateless replicated Pods through ReplicaSets.

## Desired State

The state declared through Kubernetes API objects. Controllers compare desired state with actual state and reconcile differences.

## Drain

The maintenance operation of marking a node unschedulable and evicting eligible Pods from it. Safe drains should respect PodDisruptionBudgets
through the eviction API where supported.

## EndpointSlice

A Kubernetes resource that represents network endpoints for a Service. EndpointSlices scale better than the older Endpoints object and decouple
Service identity from changing Pod IPs.

## etcd

The strongly consistent key-value store used by Kubernetes to persist cluster state. Protecting etcd is critical because it stores the source of
truth for Kubernetes API objects.

## Eviction API

The Kubernetes API mechanism used to request Pod eviction while respecting disruption controls such as PodDisruptionBudgets.

## Failure Domain

A boundary where failure can affect multiple resources together, such as a node, rack, zone, region, node pool, storage pool, or network segment.
Production architecture should spread critical replicas across appropriate failure domains.

## Ingress Controller

A controller that watches Ingress resources and configures an HTTP or HTTPS traffic entry point. It is not part of the core control plane, but it
is often critical to production traffic.

## kube-apiserver

The binary name for the Kubernetes API server. It handles API requests, authentication, authorization, admission, validation, and persistence to
etcd.

## kube-controller-manager

The binary name for the control-plane component that runs built-in Kubernetes controllers.

## kube-proxy

A node-level component that implements part of the Kubernetes Service dataplane in many clusters. Some modern CNIs replace or augment kube-proxy
with eBPF or other dataplane implementations.

## kube-scheduler

The control-plane component that assigns unscheduled Pods to nodes based on resource requests, constraints, policies, topology, taints,
tolerations, affinity, and plugin behavior.

## kubelet

The node agent that watches the API server for Pods assigned to its node and drives container runtime, volume, networking, and Pod status behavior
on that node.

## kubectl

The Kubernetes command-line client. It communicates with the API server and must remain within supported version skew relative to the API server.

## Mutating Admission

Admission logic that can modify an object before it is persisted. Common uses include injecting defaults, sidecars, labels, annotations, or policy
settings.

## Namespace

A Kubernetes scope used to organize and isolate namespaced resources. Namespaces are useful administrative and policy boundaries, but they are not
strong security boundaries by themselves.

## NetworkPolicy

A Kubernetes resource that defines allowed ingress or egress traffic for selected Pods. Enforcement depends on the cluster network plugin.

## Node

A worker machine, virtual machine, or physical host that runs kubelet and workload Pods. Nodes provide compute, memory, networking, local runtime,
and sometimes local storage resources.

## Node Condition

A status signal reported for a node, such as `Ready`, `MemoryPressure`, `DiskPressure`, `PIDPressure`, or `NetworkUnavailable`. Node conditions
help SREs understand node health and scheduling impact.

## Node Pool

A group of nodes with shared characteristics such as instance type, operating system image, zone, labels, taints, or lifecycle policy. Node pools
are often used to separate workload classes.

## PersistentVolume

A cluster-scoped Kubernetes storage resource that represents storage available to the cluster. A PersistentVolume can be statically created or
dynamically provisioned.

## PersistentVolumeClaim

A namespace-scoped request for storage. Applications usually reference PVCs rather than backend-specific storage details.

## PodDisruptionBudget

A Kubernetes policy object that limits how many Pods selected by the budget may be unavailable during voluntary disruptions. PDBs do not prevent
all failures and do not guarantee spare capacity.

## Pod Security Admission

The built-in Kubernetes admission controller that enforces Pod Security Standards at namespace level using labels such as `enforce`, `audit`, and
`warn`.

## Pod Security Standards

Kubernetes-defined policy profiles for Pod security: `privileged`, `baseline`, and `restricted`.

## Reconciliation

The control-loop process of observing actual state, comparing it with desired state, and taking actions to reduce the difference.

## ReplicaSet

A controller that maintains a specified number of matching Pod replicas. Deployments manage ReplicaSets during rollouts.

## Role

An RBAC object that defines permissions within a namespace.

## RoleBinding

An RBAC object that grants a Role or ClusterRole to users, groups, or service accounts within a namespace.

## Scheduler

The control-plane decision-maker that chooses a node for a pending Pod. The scheduler does not run containers; kubelet runs containers after a Pod
is bound to a node.

## Secret

A Kubernetes API resource intended to hold sensitive data. Secrets require careful RBAC, encryption at rest, rotation, and leak-aware operations.

## Service

A stable virtual networking abstraction for reaching a set of Pods. Services use selectors and EndpointSlices to route traffic to ready backends.

## Service Account

A Kubernetes identity for workloads and in-cluster automation. Service accounts should be scoped to the workload and granted least-privilege RBAC.

## StorageClass

A Kubernetes resource that describes a class of storage available for dynamic provisioning. In production, each StorageClass should document
performance, topology, reclaim policy, expansion, backup, and support boundaries.

## Taint

A node property that repels Pods unless the Pods have matching tolerations. Taints are commonly used to reserve nodes for specific workload
classes or system components.

## Toleration

A Pod setting that allows the Pod to schedule onto a node with a matching taint. A toleration does not force placement; it only permits it.

## Validating Admission

Admission logic that can allow or reject an object but does not mutate it.

## Version Skew

The temporary and supported difference between Kubernetes component versions during upgrade or operation. Version skew rules protect component
compatibility.

## Volume Binding Mode

A StorageClass setting that controls when a volume is bound or provisioned. `WaitForFirstConsumer` helps storage topology and Pod scheduling be
considered together.

## Worker Node

A node that runs workload Pods. Worker nodes rely on kubelet, container runtime, CNI, kube-proxy or equivalent dataplane, CSI node plugins, and
system agents.
