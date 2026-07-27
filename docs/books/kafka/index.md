# Apache Kafka

The Apache Kafka handbook focuses on operating event streaming systems that are durable, observable, and recoverable. Managed offerings are documented here so provider differences stay connected to Kafka fundamentals.

## Core operating areas

- Cluster architecture, brokers, topics, and partitions
- Producer and consumer reliability patterns
- Lag, throughput, retention, and capacity planning
- Replication, rebalancing, and failure recovery
- Monitoring, alerting, and operational runbooks
- Managed Kafka platform operations

## Managed Kafka platforms

| Platform | Focus |
| --- | --- |
| Amazon MSK | AWS-managed Kafka operations and AWS integration points. |
| Azure Event Hubs for Kafka | Kafka protocol workloads on Azure Event Hubs. |
| Google Managed Service for Apache Kafka | Google Cloud managed Kafka operations. |
| Confluent Cloud | SaaS Kafka operations, networking, governance, and reliability. |

## Starter reliability questions

1. What does healthy consumer lag look like for this workload?
2. Which topics are business critical?
3. How quickly can the platform recover from broker or provider failure?
