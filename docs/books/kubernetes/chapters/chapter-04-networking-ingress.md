# Chapter 4: Networking, Ingress, and Service Discovery

This chapter covers the Kubernetes networking model and the operational patterns SREs need for reliable service-to-service and user-facing traffic.

## Objectives

By the end of this chapter, readers should be able to:

- Explain Pod, Service, and Ingress traffic flow.
- Identify where DNS, CNI, kube-proxy, and ingress controllers fit.
- Troubleshoot common service discovery and routing failures.
- Define reliability checks for cluster networking.

## Core concepts

### Kubernetes networking model

Kubernetes assumes every Pod can communicate with every other Pod without NAT, subject to network policy and infrastructure controls. This model is implemented by the cluster CNI plugin and underlying infrastructure.

Important networking objects include:

| Object | Purpose | Operational concern |
| --- | --- | --- |
| Pod IP | Address for a Pod instance. | Ephemeral and not suitable as a stable dependency. |
| Service | Stable virtual endpoint for a set of Pods. | Selector accuracy, endpoints, and traffic policy. |
| EndpointSlice | Tracks backing endpoints for Services. | Missing or stale endpoints break routing. |
| Ingress | HTTP routing into Services. | Controller behavior, TLS, annotations, and backend readiness. |
| NetworkPolicy | Controls allowed traffic. | Default deny behavior, namespace boundaries, and debugging. |

### Service discovery

Kubernetes Services provide stable names and virtual IPs. DNS records are created for Services and Pods by cluster DNS. Most application traffic should depend on Service DNS names instead of Pod IPs.

When service discovery fails, check:

1. Does the Service exist in the expected namespace?
2. Does the Service selector match ready Pods?
3. Do EndpointSlices contain the expected endpoints?
4. Can the client resolve the Service DNS name?
5. Does network policy allow the path?

### Ingress and gateways

Ingress controllers and Gateway API implementations bridge external traffic into Kubernetes. They usually depend on cloud load balancers, DNS records, TLS certificates, and controller-specific configuration.

Use the [Networking handbook](../networking/index.md) for broader DNS, HTTP, TLS, reverse proxy, load balancing, ingress, and Gateway API fundamentals.

## Operating practices

### Standardize service naming

Service names should be stable and predictable. Namespace boundaries should be clear, and cross-namespace dependencies should be intentional.

### Monitor cluster DNS

DNS issues often appear as application failures. Monitor DNS latency, error rates, and saturation. Confirm that DNS failures have an incident runbook.

### Treat ingress as production infrastructure

Ingress controllers should be monitored like any other critical data plane. Track request rates, error rates, latency, backend health, reload failures, and certificate expiration.

### Use network policies intentionally

Network policy should protect boundaries without making diagnosis impossible. Document default namespace behavior and provide tested examples for common application patterns.

## Hands-on checks

For each production service path, confirm:

- Service selectors match intended Pods.
- EndpointSlices show ready endpoints.
- DNS resolution works from client namespaces.
- Network policies allow intended traffic and block unintended traffic.
- Ingress or gateway configuration has ownership and rollback notes.
- TLS certificates and DNS records are monitored.

## Chapter review

Readers should be able to explain:

- How Pod, Service, DNS, and Ingress traffic fit together.
- How to diagnose missing endpoints and broken service discovery.
- Which networking signals should trigger incident response.

## Next steps

Continue to [Chapter 5: Storage, State, and Backup](chapter-05-storage-state-backup.md).
