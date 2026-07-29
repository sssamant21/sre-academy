# Chapter 1 Glossary

## Purpose

This glossary defines the core terms used in Chapter 1 of the Kubernetes SRE Engineering Handbook.

The definitions are intentionally production-focused. They explain how an SRE should reason about the term during design reviews,
operations, and incidents.

## A

### Admission Control

The Kubernetes API stage that evaluates a request after authentication and authorization. Admission can validate, reject, or mutate objects
before they are persisted.

### API Object

A Kubernetes resource representation stored and served through the Kubernetes API, such as a Pod, Deployment, Service, Secret, or
PersistentVolumeClaim.

### API Server

The front door of the Kubernetes control plane. Users, controllers, schedulers, kubelets, and integrations communicate with the cluster
through the API server.

### Authentication

The process of identifying who or what is making a Kubernetes API request.

### Authorization

The process of deciding whether an authenticated identity is allowed to perform a requested action.

## C

### CNI

Container Network Interface. The plugin model commonly used to configure Pod networking and implement the cluster network model.

### CSI

Container Storage Interface. The plugin model used by storage providers to integrate provisioning, attachment, mounting, expansion, and
snapshot behavior with Kubernetes.

### Cluster

A Kubernetes environment made of a control plane, worker nodes, networking, storage integrations, security policy, and workloads.

### ClusterRole

An RBAC object that defines permissions at cluster scope or reusable permission sets that can be bound inside namespaces.

### ClusterRoleBinding

An RBAC binding that grants a ClusterRole to subjects at cluster scope. In production, ClusterRoleBindings require careful review because they
can grant broad access.

### ConfigMap

A Kubernetes object used to provide non-sensitive configuration data to workloads.

### Container Runtime

The software on a node that runs containers for Pods, under kubelet control.

### Control Plane

The components that manage cluster state and decisions, including the API server, etcd, scheduler, controller manager, and cloud controller
manager where applicable.

### Controller

A control loop that watches cluster state and works to move actual state toward desired state.

## D

### Desired State

The intended state declared through Kubernetes API objects. Controllers reconcile actual state toward desired state.

### Deployment

A workload controller commonly used for stateless applications. It manages ReplicaSets and supports rolling updates and rollbacks.

### Disruption

An event that causes one or more Pods to stop or become unavailable. Disruptions can be voluntary, such as node drains, or involuntary, such
as node failures.

## E

### EndpointSlice

A Kubernetes resource that tracks network endpoints backing a Service. EndpointSlices help Services route traffic to selected, ready Pods.

### etcd

The strongly consistent key-value store used by Kubernetes to store cluster state.

### Eviction

A controlled process for terminating Pods, often used during node pressure or voluntary disruption workflows.

## F

### Failure Domain

A boundary where failures can be correlated, such as a container, Pod, node, zone, cluster, region, storage backend, or external dependency.

## G

### Gateway API

A Kubernetes API family for more expressive service networking and traffic management than traditional Ingress, depending on implementation.

## H

### HorizontalPodAutoscaler

A Kubernetes controller that adjusts replica count based on observed metrics, such as CPU or custom metrics, when metrics and capacity are
available.

## I

### Ingress

A Kubernetes API object for HTTP and HTTPS routing into Services. Ingress requires an ingress controller to implement behavior.

## K

### kubelet

The node agent that communicates with the API server and ensures containers for assigned Pods are running on the node.

### kube-proxy

A component that implements part of the Service networking dataplane in many clusters. Some network implementations replace or bypass it.

## L

### Label

A key-value pair attached to Kubernetes objects. Labels are used heavily for selection, grouping, routing, policy, and ownership.

### Liveness Probe

A kubelet health check used to decide whether a container should be restarted. A liveness probe should detect local unrecoverable failure, not
ordinary dependency slowness.

## N

### Namespace

A Kubernetes scope for grouping resources, access control, quota, and policy. Namespaces are useful boundaries but not complete security
boundaries by themselves.

### NetworkPolicy

A Kubernetes API object that defines allowed Pod ingress or egress traffic when enforced by the cluster network plugin.

### Node

A worker machine where kubelet, the container runtime, networking, and Pods run.

## P

### PersistentVolume

A cluster resource representing storage known to Kubernetes.

### PersistentVolumeClaim

A user's request for storage. Workloads normally reference PVCs rather than backend storage directly.

### Pod

The smallest deployable workload unit in Kubernetes. A Pod has one or more containers that share networking and lifecycle.

### PodDisruptionBudget

A policy object that limits voluntary disruptions for selected Pods. It does not protect against all failures or every deletion path.

### Pod Security Admission

The built-in admission controller that enforces Pod Security Standards using namespace labels.

### Pod Security Standards

The Kubernetes-defined Pod security profiles: Privileged, Baseline, and Restricted.

### Readiness Probe

A kubelet health check used to decide whether a Pod should receive traffic through matching Services.

### Reconciliation

The process where Kubernetes controllers continuously compare desired state with observed state and act to reduce the difference.

### ReplicaSet

A controller that maintains a specified number of Pod replicas. Deployments manage ReplicaSets for rollout behavior.

### Resource Limit

A maximum amount of CPU, memory, or another resource that a container can use, enforced by the node and runtime.

### Resource Request

The amount of resource a container asks Kubernetes to reserve for scheduling. Requests are scheduling contracts.

### Role

An RBAC object that defines permissions within a namespace.

### RoleBinding

An RBAC object that grants a Role or ClusterRole to users, groups, or ServiceAccounts in a namespace.

## S

### Secret

A Kubernetes object for sensitive data. Secrets still require encryption, RBAC, rotation, and careful handling.

### Selector

A query over labels used by Services, Deployments, NetworkPolicies, PDBs, and other resources to match objects.

### Service

A stable Kubernetes abstraction for reaching a changing set of backend Pods.

### ServiceAccount

An identity for processes running in Pods. Workloads should use dedicated ServiceAccounts when they need Kubernetes API access.

### Startup Probe

A kubelet health check used to determine whether an application has finished starting. It protects slow-starting applications from premature
liveness restarts.

### StatefulSet

A workload controller used for applications that need stable Pod identity and usually stable storage identity.

### StorageClass

A Kubernetes object that describes a class of storage and dynamic provisioning behavior.

## T

### Topology Spread Constraint

A scheduling control that helps distribute Pods across topology domains such as nodes or zones.

## V

### Volume

Storage made available to containers in a Pod. Volumes can be ephemeral or persistent depending on type and configuration.

## W

### Workload

An application or process running on Kubernetes, usually managed by a workload resource such as a Deployment, StatefulSet, DaemonSet, Job, or
CronJob.
