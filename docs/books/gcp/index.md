# GCP

The GCP handbook documents provider-specific cloud operations. It should not duplicate Kubernetes or Kafka internals; use it for Google Cloud services, controls, and operational boundaries that support production platforms.

## Planned chapters

- Projects, folders, organization policies, and IAM
- VPC networking, private connectivity, routing, and security boundaries
- GKE provider operations and Google Cloud integration points
- Cloud SQL and managed database operations
- Cloud Storage, lifecycle controls, and data durability
- Pub/Sub provider operations and eventing patterns
- Cloud Monitoring, logging, metrics, alerts, and diagnostics
- Google Managed Service for Apache Kafka provider operations

## Cross-references

- Use Enterprise Kubernetes for Kubernetes internals, workloads, controllers, and cluster reliability patterns.
- Use Apache Kafka for Kafka topics, partitions, producers, consumers, retention, and lag.
- Use Networking for DNS, load balancing, TLS, ingress, and proxy fundamentals.

## Starter reliability questions

1. Which projects and services are production critical?
2. How do we monitor quota pressure and service health?
3. What recovery path exists for regional or service degradation?
