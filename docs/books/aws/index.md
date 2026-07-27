# AWS

The AWS handbook documents provider-specific cloud operations. It should not duplicate Kubernetes or Kafka internals; use it for AWS services, controls, and operational boundaries that support production platforms.

## Planned chapters

- IAM, Organizations, account structure, and guardrails
- VPC, routing, private connectivity, and security boundaries
- EC2, load balancing, autoscaling, and compute operations
- S3, backup patterns, lifecycle controls, and data durability
- RDS and managed database operations
- CloudWatch, logging, metrics, alarms, and operational visibility
- Route 53, DNS operations, and traffic management
- EKS provider operations and AWS integration points
- MSK provider operations and AWS integration points

## Cross-references

- Use Enterprise Kubernetes for Kubernetes internals, workloads, controllers, and cluster reliability patterns.
- Use Apache Kafka for Kafka topics, partitions, producers, consumers, retention, and lag.
- Use Networking for DNS, load balancing, TLS, ingress, and proxy fundamentals.

## Starter reliability questions

1. Which AWS services are critical to production availability?
2. What limits or quotas can affect scale events?
3. How do we recover from account, region, or service degradation?
