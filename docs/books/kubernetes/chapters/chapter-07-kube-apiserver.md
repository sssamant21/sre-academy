# Chapter 7: kube-apiserver

The kube-apiserver is the front door of Kubernetes. Every controller, scheduler, kubelet, operator, admission webhook, and user workflow depends on its availability, latency, authentication, authorization, and storage path.

## Objectives

By the end of this chapter, readers should be able to:

- Explain the kube-apiserver request path from client to etcd.
- Identify production signals for API availability, latency, and saturation.
- Diagnose authentication, authorization, admission, and storage failures.
- Review kube-apiserver risk for Kubernetes v1.34 environments.

## Architecture

The kube-apiserver is a stateless HTTPS API process. Production clusters usually run multiple replicas behind a load balancer or provider-managed endpoint. It validates requests, applies authentication and authorization, runs admission control, persists state through etcd, and serves watch streams to clients.

| Responsibility | Operational concern |
| --- | --- |
| API serving | Endpoint availability, TLS, client compatibility, and request latency. |
| Authentication | Broken credentials, expired certificates, identity provider outages, and token review latency. |
| Authorization | RBAC regressions, privilege drift, and denied operational access during incidents. |
| Admission | Webhook latency, webhook failure policy, policy regressions, and object mutation surprises. |
| Storage | etcd latency, object size, watch pressure, and compaction behavior. |
| API priority and fairness | Request starvation, noisy clients, and control plane protection. |

## Internal request flow

A typical write request follows this path:

1. The client connects over TLS.
2. The request is authenticated.
3. The request is authorized.
4. Mutating admission webhooks may modify the object.
5. Built-in validation and validating admission webhooks evaluate the object.
6. The object is persisted to etcd.
7. Watchers observe the updated state and controllers reconcile.

For read and watch traffic, storage and cache behavior matter. Informers and controllers should use watches efficiently; repeated list calls from poorly behaved clients can create avoidable API pressure.

## SRE operating guidance

### Protect the API server budget

The kube-apiserver has finite request capacity. Treat API QPS, request latency, and inflight request saturation as production capacity signals. Noisy automation can create incidents even when application traffic is healthy.

### Audit admission webhooks

Admission webhooks are part of the control plane request path. Slow or unavailable webhooks can block deployments, scaling, and incident mitigation. Document each webhook owner, timeout, failure policy, certificate lifecycle, and rollback path.

### Monitor API priority and fairness

API Priority and Fairness protects important traffic from starvation. Review flow schemas and priority levels when critical controllers, kubelets, or humans are delayed by bulk automation.

### Keep emergency access tested

SRE teams need a documented emergency access path for control plane incidents. Test that break-glass credentials work, are audited, and do not depend on the same failed system being debugged.

## Failure scenarios

| Scenario | Symptoms | First checks |
| --- | --- | --- |
| API endpoint unavailable | kubectl timeouts, controller errors, failed rollouts. | Endpoint health, load balancer, certificates, provider status. |
| etcd latency | Slow writes, watch delays, controller lag. | API request duration, etcd metrics, storage errors. |
| Webhook outage | Object creates or updates hang or fail. | Admission webhook status, timeout, failure policy, certificate validity. |
| Auth provider outage | Users or controllers receive authentication errors. | Identity provider health, token review errors, certificate expiry. |
| Noisy client | Elevated list/watch requests and API saturation. | Audit logs, user agents, request rate by verb/resource. |

## Kubernetes v1.34 notes

For Kubernetes v1.34, review release notes and component configuration before upgrading. Pay special attention to removed or changed APIs, admission plugin behavior, audit configuration, API Priority and Fairness settings, and compatibility with controllers that depend on watch behavior.

Before upgrading a production v1.34 control plane, verify:

- All API clients use supported API versions.
- Admission webhooks support the target Kubernetes version.
- Audit policy volume and retention are understood.
- API Priority and Fairness configuration is reviewed.
- Provider-managed control plane maintenance windows are documented.

## Engineering Review

Use these questions in design or readiness reviews:

1. Which clients generate the highest API request volume?
2. Which admission webhooks can block emergency changes?
3. What API server SLO or operational target is used?
4. How are kube-apiserver audit logs retained and queried?
5. What is the recovery path when API writes are slow but reads still work?

## Chapter review

Readers should be able to explain:

- The kube-apiserver request path and the dependencies in that path.
- Why admission and etcd latency can become deployment incidents.
- Which metrics and logs are needed during API server incidents.

## Next steps

Continue to [Chapter 8: etcd](chapter-08-etcd.md).
