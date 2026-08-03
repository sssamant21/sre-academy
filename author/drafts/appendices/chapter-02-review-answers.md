---
title: "Chapter 2 Review Answers"
chapter: 2
section: appendix
status: Draft
review_state: Author Draft
version: 0.1
---

# Chapter 2 Review Answers

This appendix provides reference answers for the Chapter 2 review questions.

## 1. What is the difference between Kubernetes control-plane architecture and worker-node architecture?

The control plane stores and coordinates cluster state. It includes components such as the API server, etcd, scheduler, controller manager, and
sometimes cloud-controller-manager. Worker-node architecture is responsible for running workloads. It includes kubelet, the container runtime,
CNI, kube-proxy or an equivalent dataplane, CSI node components, and system agents.

A simple distinction is: the control plane decides and records desired state; worker nodes execute assigned Pods and report actual state.

## 2. Why is the API server the central coordination point for Kubernetes?

The API server is the front door to Kubernetes state. Clients, controllers, scheduler, kubelets, admission webhooks, and automation interact with
cluster state through the API server. It handles authentication, authorization, admission, validation, and persistence to etcd.

Because every major control loop observes or changes state through the API, API server availability and correctness are central to cluster
operation.

## 3. What role does etcd play, and why is it critical to protect and back up?

etcd stores Kubernetes cluster state. It contains API objects such as Deployments, Pods, Secrets, ConfigMaps, Services, RBAC, and many other
resources.

If etcd is lost or corrupted, the cluster can lose its source of truth. Protecting etcd means controlling access, enabling appropriate encryption,
monitoring health, and maintaining tested backup and restore procedures.

## 4. How does the scheduler decide where a Pod should run?

The scheduler watches for Pods that do not yet have a node assignment. It evaluates candidate nodes using resource requests, taints and
tolerations, node selectors, affinity and anti-affinity, topology constraints, volume binding, and scheduler plugins.

After selecting a node, the scheduler binds the Pod to that node. The kubelet on that node is then responsible for running the Pod.

## 5. What does kubelet do after a Pod is assigned to a node?

kubelet observes Pods assigned to its node and works to make them run. It coordinates with the container runtime, prepares volumes, invokes CNI
networking, starts containers, runs probes, and reports Pod and node status back to the API server.

kubelet does not choose where Pods should run. It executes Pods that have already been scheduled to its node.

## 6. Why can a Pod be `Running` while the application is still not serving traffic?

`Running` means the Pod has been bound to a node and at least one container is running or starting. It does not prove that the application is ready
to serve traffic.

The application may fail readiness probes, listen on the wrong port, be unable to connect to dependencies, be blocked by configuration, or be
excluded from EndpointSlices. SREs should check readiness, events, logs, probes, Service selectors, and EndpointSlices.

## 7. What is the difference between a Service and an EndpointSlice?

A Service provides a stable virtual access point for a set of Pods. It has a stable name and virtual IP behavior. An EndpointSlice stores the
actual backend endpoints selected for a Service.

Services define how clients find a workload. EndpointSlices show which Pod IPs and ports are currently eligible as backends.

## 8. Why is CNI enforcement required for NetworkPolicy to provide isolation?

NetworkPolicy is an API object that declares allowed traffic, but Kubernetes itself does not enforce those rules without network-plugin support.
The CNI implementation must translate NetworkPolicy into dataplane enforcement.

If a cluster network plugin does not enforce NetworkPolicy, policy objects may exist but traffic may still flow unrestricted.

## 9. What is the relationship between a PersistentVolumeClaim, PersistentVolume, and StorageClass?

A PersistentVolumeClaim is a namespace-scoped request for storage. A PersistentVolume is the cluster-scoped storage resource that satisfies that
claim. A StorageClass describes how dynamic storage should be provisioned.

In a dynamic provisioning flow, a PVC references a StorageClass, the storage provisioner creates backend storage, and Kubernetes binds the PVC to a
PV.

## 10. Why is `WaitForFirstConsumer` useful for topology-aware storage?

`WaitForFirstConsumer` delays volume binding or provisioning until a Pod that uses the PVC is scheduled. This allows the scheduler to consider Pod
placement and storage topology together.

This is important for zonal storage. Without it, a volume can be provisioned in one zone while the Pod needs to run in another zone, causing
scheduling or mount failures.

## 11. Why is access to Secrets a high-risk RBAC permission?

Secrets can contain credentials, tokens, keys, certificates, and other sensitive data. A user or service account that can read Secrets may be able
to impersonate applications, access databases, call cloud APIs, or escalate privileges indirectly.

Secret access should be tightly scoped, audited, and limited to workloads or operators that truly need it.

## 12. Why should Pods that do not need API access disable service account token mounting?

A mounted service account token gives a Pod an identity that can call the Kubernetes API. If the application is compromised, an attacker may use
that token to query or modify cluster resources within the service account permissions.

Disabling token mounting for Pods that do not need API access reduces the blast radius of application compromise.

## 13. What does Pod Security Admission enforce?

Pod Security Admission enforces Kubernetes Pod Security Standards at namespace level. It can enforce, audit, or warn based on namespace labels.
The standard profiles are `privileged`, `baseline`, and `restricted`.

It helps prevent unsafe Pod configurations, but it is not a complete security model. RBAC, NetworkPolicy, node hardening, image policy, secrets
handling, and runtime controls still matter.

## 14. Why are namespaces not strong security boundaries by themselves?

Namespaces organize and scope many Kubernetes resources, but they do not automatically provide strong isolation. Without RBAC, admission policy,
NetworkPolicy, resource quotas, Pod security controls, and sometimes node separation, workloads in different namespaces can still affect each
other.

For example, a user who can create Pods in a namespace may be able to use powerful service accounts in that namespace unless RBAC and admission
controls prevent it.

## 15. What does Kubernetes version skew policy protect against?

Version skew policy defines supported version differences between Kubernetes components during mixed-version operation. It helps ensure components
remain compatible while the cluster is upgraded.

It protects against unsupported combinations such as kubelets being newer than the API server, API servers in HA being too far apart, or clients
being too far outside the supported API server version window.

## 16. Why should minor Kubernetes upgrades not skip versions?

Skipping minor versions is unsupported by upstream Kubernetes upgrade policy and increases risk. API behavior, removed APIs, component
compatibility, feature gates, and add-ons may assume a one-minor-version upgrade path.

Production clusters should upgrade one minor version at a time and validate each step.

## 17. Why should admission webhooks be reviewed before a cluster upgrade?

Admission webhooks run in the API write path. If they are unavailable, incompatible with target-version API objects, too slow, or configured with a
strict failure policy, they can block deployments and controllers.

Before an upgrade, SREs should review webhook health, replicas, PDBs, `failurePolicy`, timeouts, namespace selectors, and compatibility with new
API versions and object shapes.

## 18. What does a PodDisruptionBudget protect, and what does it not protect?

A PodDisruptionBudget limits voluntary disruptions for selected Pods, such as evictions during node drains. It helps keep enough replicas
available during planned maintenance.

It does not prevent involuntary failures such as node crashes, resource pressure, network partitions, or direct workload controller rollouts that
bypass PDB enforcement. It also does not create spare capacity by itself.

## 19. Why can deleting a PDB during maintenance be dangerous?

Deleting a PDB removes a safeguard that may be correctly preventing too many Pods from being disrupted at once. If the PDB is blocking a drain, it
may indicate insufficient replicas, unhealthy Pods, tight capacity, or a real availability risk.

The safer response is to understand why the budget blocks disruption, add capacity or restore workload health, and only override controls through
an approved incident or maintenance process.

## 20. What should be included in post-upgrade validation?

Post-upgrade validation should confirm that the cluster and workloads are healthy. At minimum, check node readiness and versions, system namespace
Pods, API errors, admission webhook health, DNS, CNI, CSI, ingress, metrics, logging, autoscaling, workload SLOs, and continued deprecated API
usage.

A good closeout records final versions, warnings, incidents, manual actions, and follow-up work.

## Interview-Style Answer Guide

### Walk me through what happens when a user creates a Deployment.

The client sends a request to the API server. The request is authenticated, authorized, admitted, validated, and persisted. The Deployment
controller observes the Deployment and creates or updates a ReplicaSet. The ReplicaSet creates Pods. The scheduler assigns unscheduled Pods to
nodes. kubelet on each selected node starts the containers and reports status. Services and EndpointSlices update when Pods become ready and match
selectors.

### A Pod is stuck in `Pending`. What do you check first?

Check whether the Pod has a node assignment. If not, inspect `kubectl describe pod` events for scheduler messages about resources, taints,
affinity, topology, or volume binding. Then check node readiness, capacity, requests, quotas, and storage constraints.

### A Service has no endpoints. What are the most likely causes?

The Service selector may not match Pod labels, Pods may not be Ready, Pods may not expose the expected port, the workload may not exist, or the
EndpointSlice controller may not have updated yet. Start with Service selectors, Pod labels, Pod readiness, and EndpointSlices.

### A node is `NotReady`. What is your first five-minute investigation?

Check node conditions and events, identify affected Pods on the node, look for kubelet heartbeat loss, check whether other nodes have capacity,
review recent maintenance or infrastructure events, and confirm whether workloads are rescheduling. If needed, coordinate with node or cloud
platform owners.

### How would you explain the difference between kube-proxy and a CNI plugin?

A CNI plugin sets up Pod networking and may enforce network policy. kube-proxy implements Kubernetes Service dataplane behavior in many clusters.
Some modern CNIs replace kube-proxy functionality, but the conceptual split remains: Pod network setup and policy are CNI concerns; Service
traffic routing is kube-proxy or equivalent dataplane behavior.

### How do you design node pools for different workload classes?

Use separate node pools when workloads have different trust levels, resource shapes, operating system needs, availability requirements, hardware
requirements, or lifecycle policies. Use labels, taints, tolerations, affinity, topology spread, quotas, and autoscaling configuration to control
placement and capacity.

### How do you review a StorageClass for production readiness?

Review provisioner, reclaim policy, volume binding mode, expansion support, allowed access modes, topology behavior, performance, encryption,
backup and restore integration, cost, support ownership, and failure behavior. Confirm application requirements match the class behavior.

### Why is `cluster-admin` dangerous for application service accounts?

An application Pod compromise becomes a cluster compromise if the Pod has `cluster-admin`. Attackers can read Secrets, create privileged Pods,
modify RBAC, change workloads, and tamper with control-plane objects. Application service accounts should receive only the permissions required.

### How do you safely upgrade a Kubernetes cluster with minimal downtime?

Plan the target version, check skew policy, scan deprecated APIs, validate add-on compatibility, test in non-production, ensure backups and
recovery procedures, upgrade the control plane first, roll node pools in small batches, respect PDBs, maintain spare capacity, watch SLOs and
system health, and pause if risk thresholds are crossed.

### What metrics and signals would you watch during a node pool upgrade?

Watch node readiness, Pod restarts, pending Pods, failed scheduling events, PDB disruption allowance, API errors, DNS errors, CNI and CSI errors,
load balancer health, application latency, error rates, saturation, and critical business SLOs.
