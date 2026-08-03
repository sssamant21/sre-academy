# Chapter 3 Glossary and Review Answers Source Validation

## Scope

This validation covers the Chapter 3 glossary and Chapter 3 review-answer appendix.

Files covered:

- `author/drafts/chapter-03/glossary.md`
- `docs/books/kubernetes/chapter-03/glossary.md`
- `author/drafts/appendices/chapter-03-review-answers.md`
- `docs/books/kubernetes/appendices/chapter-03-review-answers.md`

## Validation Summary

The glossary and answers were reviewed for consistency with the completed Chapter 3 manuscript and upstream Kubernetes concepts for workloads,
scheduling, resource management, autoscaling, and disruption handling.

## Source Matrix

| Area | Validation note |
| --- | --- |
| Workload controllers | Definitions and answers align with Kubernetes controller concepts for Deployments, ReplicaSets, StatefulSets, DaemonSets, Jobs, and CronJobs. |
| Pod lifecycle | Terms distinguish Pod lifecycle, readiness, liveness, startup, termination, and controller-owned replacement behavior. |
| Scheduling | Answers describe scheduling as a decision based on requests, constraints, taints, tolerations, affinity, topology, volume constraints, and node state. |
| Resource management | Glossary and answers distinguish requests from limits and connect requests to scheduling, QoS, eviction, and HPA CPU utilization. |
| Autoscaling | HPA answers explain that HPA changes desired replicas and depends on metrics, requests, readiness, scheduling, startup behavior, and capacity. |
| Disruption handling | PDB answers correctly describe voluntary disruption protection and avoid claiming protection from all failures. |
| Graceful termination | Answers explain termination as a contract between Kubernetes, application behavior, and traffic-routing systems. |

## Markdown Review

- Heading hierarchy starts at H1 and proceeds through H2.
- Fenced code blocks are not required in these pages.
- No internal relative links were introduced.
- Published pages use the repository snippet-wrapper pattern.
- Navigation updates are required for Chapter 3 glossary and Chapter 3 review answers.

## Official References Reviewed

- Kubernetes Workload Management documentation.
- Kubernetes Deployments documentation.
- Kubernetes ReplicaSets documentation.
- Kubernetes StatefulSets documentation.
- Kubernetes DaemonSets documentation.
- Kubernetes Jobs documentation.
- Kubernetes CronJobs documentation.
- Kubernetes Assigning Pods to Nodes documentation.
- Kubernetes Resource Management for Pods and Containers documentation.
- Kubernetes Pod Quality of Service Classes documentation.
- Kubernetes Horizontal Pod Autoscaling documentation.
- Kubernetes Disruptions and PodDisruptionBudget documentation.
- Kubernetes Liveness, Readiness, and Startup Probes documentation.
