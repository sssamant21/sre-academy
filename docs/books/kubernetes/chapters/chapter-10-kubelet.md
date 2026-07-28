# Chapter 10: kubelet

The kubelet is the node agent that turns scheduled Pods into running containers. It is the bridge between Kubernetes desired state and real workload execution on each node.

## Objectives

By the end of this chapter, readers should be able to:

- Explain kubelet responsibilities on a worker node.
- Identify node-level failures that prevent Pods from running.
- Diagnose probe, runtime, image, volume, and resource-pressure issues.
- Review kubelet operations for Kubernetes v1.34 environments.

## Architecture

The kubelet watches the API server for Pods assigned to its node. It works with the container runtime, CNI plugin, CSI plugin, and operating system to prepare volumes, configure networking, pull images, start containers, run probes, report status, and enforce resource behavior.

| Responsibility | Operational concern |
| --- | --- |
| Pod lifecycle | Containers stuck in creating, waiting, crash loop, or unknown states. |
| Runtime integration | containerd or CRI failures, image pull failures, sandbox creation errors. |
| Probes | Incorrect readiness, liveness, or startup behavior. |
| Node status | Ready condition, pressure conditions, leases, and heartbeat freshness. |
| Resource enforcement | CPU, memory, ephemeral storage, eviction thresholds, and cgroups. |
| Volume management | Mount failures, attach delays, CSI errors, and filesystem issues. |
| Networking | CNI setup, Pod sandbox creation, DNS configuration, and node routing. |

## Internal kubelet flow

A typical Pod startup includes:

1. kubelet observes a Pod assigned to the node.
2. Volumes and secrets are prepared.
3. A Pod sandbox is created through the runtime and CNI.
4. Images are pulled or found locally.
5. Containers are started in dependency order.
6. Startup, readiness, and liveness probes begin.
7. Pod and container status are reported back to the API server.

If any dependency fails, the scheduler may have done its job while the Pod still cannot run.

## SRE operating guidance

### Treat node health as workload health

Node issues become application incidents quickly. Alert on NotReady nodes, frequent node condition changes, runtime failures, image pull failures, disk pressure, memory pressure, and network unavailable conditions.

### Design probes carefully

Probe failures trigger traffic removal or restarts. Poorly designed liveness probes can restart healthy but slow applications. Missing readiness probes can send traffic to Pods before they can serve.

### Monitor eviction pressure

kubelet protects node stability by evicting Pods under resource pressure. Track memory, disk, inode, PID, and ephemeral storage pressure. Define workload requests and limits so node pressure is predictable.

### Keep runtime and OS operations visible

Kubernetes incidents often require host-level diagnosis. SREs should know how to inspect kubelet logs, runtime status, image pull failures, CNI errors, CSI mount failures, and node-level resource pressure.

## Failure scenarios

| Scenario | Symptoms | First checks |
| --- | --- | --- |
| Node NotReady | Pods unavailable or unknown. | kubelet status, node conditions, node lease, network reachability. |
| Runtime failure | Pods stuck creating or containers fail to start. | container runtime health, kubelet logs, CRI errors. |
| Image pull failure | Pods in ImagePullBackOff or ErrImagePull. | Registry access, credentials, image tag, network path. |
| Probe misconfiguration | Restart loops or no traffic to healthy Pods. | Probe endpoint, timeout, thresholds, startup behavior. |
| Disk pressure | Evictions, failed writes, image garbage collection. | Node filesystem usage, ephemeral storage, logs, image cache. |
| Volume mount failure | Pods stuck ContainerCreating. | CSI driver, PVC events, mount permissions, provider status. |

## Kubernetes v1.34 notes

For Kubernetes v1.34, review kubelet configuration, node OS compatibility, container runtime compatibility, cgroup settings, credential provider configuration, eviction thresholds, and feature gates used by your distribution.

Before upgrading nodes to v1.34, verify:

- Runtime and CNI versions are supported.
- Node bootstrap and certificate rotation are healthy.
- Kubelet configuration is managed declaratively.
- Eviction thresholds and reserved resources match production needs.
- Rollback or node replacement procedures are documented.

## Engineering Review

Use these questions in design or readiness reviews:

1. What node conditions page an operator?
2. How do SREs inspect kubelet and runtime failures during an incident?
3. Are probes matched to real application health semantics?
4. Are eviction thresholds, reserved resources, and workload requests aligned?
5. How are node upgrades rolled out and rolled back safely?

## Chapter review

Readers should be able to explain:

- How kubelet converts scheduled Pods into running containers.
- Why runtime, CNI, CSI, and host issues appear as Kubernetes workload failures.
- Which node-level signals are required for production operations.

## Next steps

Return to the [Enterprise Kubernetes overview](../index.md) or continue with supporting sections such as [Helm](../helm.md), [Kustomize](../kustomize.md), [GitOps](../gitops.md), and [Managed Kubernetes](../managed-kubernetes/index.md).
