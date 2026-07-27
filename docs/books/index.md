# Handbook Catalog

The SRE Academy catalog is organized by operational domain. Each handbook can grow from introductory notes into labs, runbooks, troubleshooting guides, and production readiness checklists.

## Platform Engineering

| Handbook | Focus |
| --- | --- |
| Kubernetes | Cluster operations, workload reliability, networking, storage, and observability. |
| Helm | Kubernetes package management, release safety, and rollback workflows. |
| Argo CD | GitOps delivery, drift detection, sync workflows, and multi-cluster operations. |
| Terraform | Infrastructure as code, state management, plan review, and change safety. |
| Kustomize | Kubernetes overlays, environment promotion, and manifest customization. |

## Observability

| Handbook | Focus |
| --- | --- |
| Prometheus | Metrics, PromQL, alerting, service-level indicators, and operational signals. |
| Grafana | Dashboards, alert views, incident context, and observability workflows. |
| OpenTelemetry | Instrumentation, collectors, telemetry pipelines, and trace context. |
| Loki | Log aggregation, labels, retention, LogQL, and production troubleshooting. |
| Tempo | Trace storage, sampling, retention, and metrics-log-trace correlation. |
| Jaeger | Distributed tracing operations and latency investigation workflows. |

## Messaging & Streaming

| Handbook | Focus |
| --- | --- |
| Apache Kafka | Event streaming operations, topic design, consumer health, capacity, and recovery. |
| Amazon MSK | Managed Kafka on AWS, cluster operations, scaling, monitoring, and recovery. |
| RabbitMQ (Future) | Queueing operations, routing, acknowledgements, dead lettering, and broker health. |

## Datastores

| Handbook | Focus |
| --- | --- |
| PostgreSQL | Relational database operations, schema safety, backups, replication, failover, and performance. |
| MongoDB | Document database operations, schema design, indexing, replication, backups, and sharding. |
| Elasticsearch | Search operations, index lifecycle, shard health, query tuning, and resilience. |
| Redis | Cache and data structure operations, persistence, replication, high availability, and failover. |
| Snowflake | Data warehouse operations, performance, cost management, governance, and pipelines. |
| MySQL | Relational database operations, replication, backup, restore, performance, and maintenance. |
| Cassandra (Future) | Distributed database operations, data modeling, repair, compaction, and resilience. |

## Cloud

| Handbook | Focus |
| --- | --- |
| AWS | Account foundations, managed services, resilience, quotas, and cloud operations. |
| Azure | Subscription foundations, managed services, monitoring, resilience, and recovery. |
| GCP | Project foundations, managed services, monitoring, quotas, and cloud operations. |
| Multi-Cloud | Cross-provider governance, resilience tradeoffs, portability, and recovery patterns. |

## DevOps & CI/CD

| Handbook | Focus |
| --- | --- |
| Git | Source control workflows, release branches, tags, history, and recovery. |
| GitHub Actions | Workflow automation, permissions, environments, artifacts, and delivery reliability. |
| Jenkins | Pipeline operations, controller health, agents, credentials, and recovery. |
| Argo Workflows | Kubernetes-native workflows, retries, artifacts, scheduling, and troubleshooting. |
| Flux (Future) | GitOps reconciliation, source control state, drift, and automated delivery. |

## Linux & Networking

| Handbook | Focus |
| --- | --- |
| Linux | Host operations, processes, filesystems, resource pressure, and troubleshooting. |
| DNS | Name resolution, records, delegation, caching, TTLs, and DNS incident response. |
| Load Balancing | Traffic distribution, health checks, failover, retries, and routing reliability. |
| NGINX | Proxy, ingress, web serving, TLS, upstreams, and configuration validation. |
| Service Mesh (Istio) | Mesh traffic policy, mTLS, observability, gateways, and control plane operations. |

## Suggested page pattern

1. Start with the operational problem.
2. Explain the key concepts needed to reason about it.
3. Provide commands, diagrams, or checklists for practice.
4. End with validation steps and common failure modes.
