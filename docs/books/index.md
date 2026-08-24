# Handbook Catalog

The SRE Academy catalog is organized around core technologies that justify full production handbooks. Cloud-managed services and supporting tools are documented inside those handbooks instead of being promoted as duplicate standalone books.

## Primary handbooks

| Handbook | Focus |
| --- | --- |
| Enterprise Kubernetes | Cluster operations, workloads, Helm, Kustomize, GitOps, EKS, AKS, and GKE. |
| Apache Kafka | Kafka fundamentals, production operations, and managed Kafka platforms. |
| PostgreSQL SRE & DBRE Handbook | Relational database operations, internals, HA/DR, managed-cloud PostgreSQL, production SRE/DBRE workflows, and performance. |
| MongoDB | Document database operations, schema design, indexing, replication, backups, and sharding. |
| Elasticsearch | Search operations, index lifecycle, shard health, query tuning, and resilience. |
| Redis | Cache and data structure operations, persistence, replication, high availability, and failover. |
| Snowflake | Data warehouse operations, performance, cost management, governance, and pipelines. |
| Prometheus | Metrics, PromQL, alerting, service-level indicators, and operational signals. |
| Grafana | Dashboards, alert views, incident context, and observability workflows. |
| Argo CD | GitOps delivery, drift detection, sync workflows, and multi-cluster operations. |
| Terraform SRE & Cloud Infrastructure Engineering Handbook | Infrastructure as code, state management, plan review, and change safety. |
| Linux | Host operations, processes, filesystems, resource pressure, and troubleshooting. |
| Networking | DNS, TCP/IP, HTTP/HTTPS, reverse proxy, load balancing, TLS, service discovery, ingress, and gateways. |
| AWS | AWS platform operations across IAM, Organizations, VPC, EC2, S3, RDS, CloudWatch, Route 53, EKS, and MSK. |
| Azure | Azure platform operations across AKS, Azure SQL, Key Vault, Azure Monitor, and Virtual Network. |
| GCP | Google Cloud operations across GKE, Cloud SQL, Cloud Storage, Pub/Sub, Cloud Monitoring, and managed Kafka. |

## Consolidated supporting topics

| Supporting topic | New home |
| --- | --- |
| Helm | Enterprise Kubernetes |
| Kustomize | Enterprise Kubernetes |
| Amazon EKS | Enterprise Kubernetes and AWS |
| Azure AKS | Enterprise Kubernetes and Azure |
| Google GKE | Enterprise Kubernetes and GCP |
| Amazon MSK | Apache Kafka and AWS |
| Azure Event Hubs for Kafka protocol | Apache Kafka and Azure |
| Google Managed Service for Apache Kafka | Apache Kafka and GCP |
| Confluent Cloud | Apache Kafka |
| DNS | Networking |
| Load Balancing | Networking |
| NGINX | Networking |
| Service Mesh (Istio) | Networking |

## Preserved reference pages

Existing standalone pages are preserved in the repository so old links and history remain available, but new content should be added to the consolidated handbook locations above.

## Suggested page pattern

1. Start with the operational problem.
2. Explain the key concepts needed to reason about it.
3. Provide commands, diagrams, or checklists for practice.
4. End with validation steps and common failure modes.
