# Azure

The Azure handbook documents provider-specific cloud operations. It should not duplicate Kubernetes or Kafka internals; use it for Azure services, controls, and operational boundaries that support production platforms.

## Planned chapters

- Subscriptions, management groups, identity, and policy
- Virtual Network, private endpoints, routing, and security boundaries
- AKS provider operations and Azure integration points
- Azure SQL and managed database operations
- Key Vault, secrets, certificates, and access patterns
- Azure Monitor, logging, metrics, alerts, and diagnostics
- Event Hubs Kafka protocol provider operations

## Cross-references

- Use Enterprise Kubernetes for Kubernetes internals, workloads, controllers, and cluster reliability patterns.
- Use Apache Kafka for Kafka protocol fundamentals, topics, partitions, producers, consumers, retention, and lag.
- Use Networking for DNS, load balancing, TLS, ingress, and proxy fundamentals.

## Starter reliability questions

1. Which subscriptions and resources support production services?
2. How do we detect quota, networking, or identity failures?
3. What recovery path exists for regional service degradation?
