# Chapter 6: Observability and Operations

This chapter defines the observability and operational practices required to run Kubernetes as a reliable production platform.

## Objectives

By the end of this chapter, readers should be able to:

- Identify the key signals for cluster, node, workload, and ingress health.
- Define useful alerts that support action instead of noise.
- Describe incident response workflows for Kubernetes failures.
- Establish operational review practices for continuous improvement.

## Core concepts

### Four layers of Kubernetes observability

Kubernetes observability should cover four layers.

| Layer | Example signals | Operational question |
| --- | --- | --- |
| Control plane | API latency, errors, admission failures, controller health. | Can Kubernetes accept and reconcile changes? |
| Nodes | Ready state, CPU, memory, disk, network, runtime errors. | Can nodes run workloads safely? |
| Workloads | Replicas, restarts, readiness, latency, errors, saturation. | Can applications serve users? |
| Traffic path | DNS, ingress, gateway, Service endpoints, TLS, backend health. | Can clients reach healthy services? |

### Events, logs, metrics, and traces

No single signal is enough. Events explain recent object-level changes. Logs show component and application details. Metrics show trends and alert conditions. Traces show request paths and dependency behavior.

Use the Prometheus and Grafana handbooks for observability platform details. Use this chapter to define what Kubernetes-specific signals should exist and how operators should use them.

### Alert quality

Good alerts are actionable, urgent, and owned. Avoid paging on symptoms that do not require human action. Prefer alerts that identify user impact, platform risk, or imminent exhaustion.

Examples of useful alert themes include:

- API server error rate or latency affecting operations.
- Nodes repeatedly becoming NotReady.
- Critical workloads unavailable or unable to roll out.
- DNS failures affecting service discovery.
- Ingress error rate or certificate expiration.
- Persistent volume exhaustion or attach failures.

## Operating practices

### Build standard dashboards

A Kubernetes platform should provide default dashboards for:

- Cluster health and capacity.
- Node pools and node conditions.
- Namespace resource usage.
- Workload rollout and availability.
- Ingress and gateway traffic.
- Persistent storage health.

Dashboards should answer incident questions quickly, not merely display every possible metric.

### Maintain runbooks

Runbooks should describe detection, impact, diagnosis, mitigation, escalation, and follow-up. Each runbook should identify required permissions and commands that are safe during an incident.

### Review incidents and changes

Kubernetes incidents often reveal gaps in defaults, ownership, deployment workflows, or capacity planning. Post-incident review should turn those gaps into platform improvements.

### Track operational readiness

Before onboarding a workload, confirm that monitoring, alerting, logs, traces, rollback, ownership, and escalation paths exist.

## Hands-on checks

For each production namespace or service, confirm:

- Dashboards exist for workload health and traffic.
- Alerts are actionable and owned.
- Logs are searchable by namespace, workload, and Pod.
- Traces exist for critical request paths where appropriate.
- Runbooks exist for common failure modes.
- On-call teams know the escalation path.

## Chapter review

Readers should be able to explain:

- Which signals matter for cluster and workload reliability.
- How to distinguish useful alerts from noise.
- How runbooks and incident reviews improve platform reliability.

## Next steps

Continue with supporting sections: [Helm](../helm.md), [Kustomize](../kustomize.md), [GitOps](../gitops.md), and [Managed Kubernetes](../managed-kubernetes/index.md).
