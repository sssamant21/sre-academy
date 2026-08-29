# MongoDB Administration Handbook — Master TOC v1.0

**Status:** 🔒 LOCKED  
**Baseline:** MongoDB 8.x  
**Compatibility:** MongoDB 7.x notes where operationally relevant

## Editorial and Technical Rules

Major operational topics follow: Architecture → Configuration → Administration → Best Practices → Monitoring → Alerting → Failure Scenarios → Troubleshooting → Recovery → Automation → Production Case Studies.

Where relevant, sections identify applicability to MongoDB Community, MongoDB Enterprise Advanced, MongoDB Atlas, self-managed deployments, and version-specific behavior.

## Chapter 1 — MongoDB Architecture and Internals
1.1 What Is MongoDB?  
1.2 MongoDB Deployment Architecture  
1.3 mongod, mongos, and Supporting Components  
1.4 Database, Collection, Document, and Field Architecture  
1.5 BSON Architecture and Data Types  
1.6 MongoDB Namespace Architecture  
1.7 MongoDB Process Architecture  
1.8 Client and Server Connection Architecture  
1.9 Connection Strings: Standard and SRV  
1.10 Replica Set Discovery and Server Selection  
1.11 Connection Pools and Timeout Architecture  
1.12 DNS and Connectivity Considerations  
1.13 MongoDB Memory Architecture  
1.14 WiredTiger Storage Engine Architecture  
1.15 Journaling and Durability Architecture  
1.16 Checkpoints and Recovery Architecture  
1.17 Concurrency and Locking Fundamentals  
1.18 Read and Write Execution Architecture  
1.19 Replication Architecture Overview  
1.20 Sharding Architecture Overview  
1.21 MongoDB Deployment Topologies  
1.22 Community vs. Enterprise Advanced vs. Atlas  
1.23 MongoDB Versioning and Release Lifecycle  
1.24 Architecture Troubleshooting and Diagnostic Fundamentals

## Chapter 2 — Installation, Configuration, Patching, and Upgrades
2.1 Production Installation Planning  
2.2 Hardware and OS Requirements  
2.3 Linux Preparation  
2.4 Filesystem and Storage Preparation  
2.5 Package and Repository Installation  
2.6 mongod.conf Architecture  
2.7 Network Configuration  
2.8 Storage Configuration  
2.9 Process Management with systemd  
2.10 Resource Limits and OS Tuning  
2.11 NUMA and Memory Considerations  
2.12 Transparent Huge Pages Considerations  
2.13 Time Synchronization  
2.14 Secure Production Configuration Baseline  
2.15 Runtime Parameters and setParameter  
2.16 Cluster Parameters and setClusterParameter  
2.17 Restart-Required vs. Runtime Changes  
2.18 Configuration Drift Detection  
2.19 MongoDB Version Management and Patch Management  
2.20 Upgrade Planning and Prechecks  
2.21 Feature Compatibility Version Architecture  
2.22 Binary Version vs. FCV  
2.23 FCV Upgrade Procedure and Burn-In Period  
2.24 Rolling Upgrades  
2.25 Backward-Incompatible Features and Downgrade Constraints  
2.26 Post-Upgrade Validation  
2.27 Upgrade Failure, Recovery, and Rollback Planning  
2.28 Installation and Upgrade Runbooks

## Chapter 3 — Database, Collection, and Document Administration
3.1 Database Administration Fundamentals  
3.2 Creating and Managing Databases  
3.3 Collection Administration and Creation Options  
3.4 Capped Collections  
3.5 Clustered Collections  
3.6 Views and View Administration  
3.7 Time-Series Collections and Administration  
3.8 Collection Modification with collMod  
3.9 Document and BSON Data-Type Administration  
3.10 Collection and Index Integrity  
3.11 validate and validateDBMetadata  
3.12 Integrity Check Planning and Performance Impact  
3.13 Integrity Failure Response  
3.14 Schema Validation and JSON Schema Validation  
3.15 Collection Rename and Drop Operations  
3.16 Database Drop Operations  
3.17 Database and Collection Statistics  
3.18 Data Growth and Large Collection Administration  
3.19 Administrative Metadata Commands  
3.20 Safe Production Change Procedures  
3.21 Database/Object Troubleshooting  
3.22 Administration Automation and Production Case Studies

## Chapter 4 — Production CRUD, Transactions, and Change Streams
4.1 CRUD Architecture  
4.2 Insert, Query, Update, and Delete Operations  
4.3 Bulk Operations and Atomicity  
4.4 Transactions and Multi-Document Transactions  
4.5 Transaction Lifetime and Resource Impact  
4.6 Transactions in Replica Sets and Sharded Clusters  
4.7 Transaction Monitoring and Long-Running Transactions  
4.8 Transaction Failure and Recovery  
4.9 Read Concern  
4.10 Write Concern  
4.11 Read Preference  
4.12 Retryable Reads and Writes  
4.13 Sessions  
4.14 Change Streams Fundamentals  
4.15 Resume Tokens and Resumability  
4.16 Change Stream Operational Considerations  
4.17 Cursor Administration  
4.18 Long-Running Operations and Safe Termination  
4.19 Production Data Change Procedures  
4.20 CRUD Failure Scenarios, Troubleshooting, and Recovery

## Chapter 5 — Schema Design and Data Modeling
5.1 MongoDB Data Modeling Principles  
5.2 Embedded vs. Referenced Models  
5.3 One-to-One, One-to-Many, and Many-to-Many Relationships  
5.4 Document Growth and Large Documents  
5.5 Array Design and Polymorphic Data  
5.6 Schema Evolution  
5.7 Data Validation  
5.8 Operational Impact of Schema Design  
5.9 Data Modeling Anti-Patterns  
5.10 Production Modeling Case Studies

## Chapter 6 — MongoDB Index Administration
6.1 Index Architecture  
6.2 _id and Single-Field Indexes  
6.3 Compound and Multikey Indexes  
6.4 Unique, Sparse, and Partial Indexes  
6.5 TTL and Hidden Indexes  
6.6 Wildcard, Text, and Specialized Index Considerations  
6.7 Index Creation and Production Index Builds  
6.8 Index Removal  
6.9 Index Usage Analysis  
6.10 Redundant and Unused Indexes  
6.11 Index Storage and Memory Impact  
6.12 Index Maintenance  
6.13 Index Build Failure Scenarios  
6.14 Index Troubleshooting and Administration Runbooks

## Chapter 7 — Query Analysis and Administrative Performance
7.1 Query Processing and Query Planner Fundamentals  
7.2 explain() and Execution Statistics  
7.3 Collection Scans and Index Scans  
7.4 Sorting and Aggregation Pipelines  
7.5 Slow Queries and Database Profiler  
7.6 $currentOp and Operation Visibility  
7.7 Filtering Active and Long-Running Operations  
7.8 Operation Termination  
7.9 Query Shapes  
7.10 Query Settings Administration  
7.11 Query Plan Control Considerations  
7.12 Query Settings Monitoring and Removal  
7.13 Query Performance Baselines  
7.14 Query Troubleshooting and Production Case Studies

## Chapter 8 — Authentication, Authorization, Encryption, and Security
8.1 MongoDB Security Architecture  
8.2 Authentication Architecture and SCRAM  
8.3 Enterprise Authentication Considerations  
8.4 User, Role, Built-In Role, and Custom Role Administration  
8.5 Least-Privilege Design  
8.6 Internal and Keyfile Authentication  
8.7 X.509 Authentication  
8.8 TLS and Encryption in Transit  
8.9 Encryption at Rest  
8.10 Client-Side Field Level Encryption  
8.11 Queryable Encryption  
8.12 Key Management  
8.13 Certificate Management and Online Rotation  
8.14 Auditing and Audit Logging  
8.15 Network Security  
8.16 Secrets and Credential Management  
8.17 Security Hardening Baseline  
8.18 Credential Rotation  
8.19 Security Monitoring  
8.20 Security Failure Scenarios, Troubleshooting, and Runbooks

## Chapter 9 — Replica Set Architecture and Deployment
9.1 Replica Set Architecture  
9.2 Primary and Secondary Members  
9.3 Elections, Voting, and Member Priority  
9.4 Hidden and Delayed Members  
9.5 Arbiters and Their Risks  
9.6 Replica Set Deployment  
9.7 Adding and Removing Members  
9.8 Reconfiguring Replica Sets  
9.9 Member Maintenance  
9.10 Planned Primary Stepdown  
9.11 Production Maintenance Procedures and Runbooks

## Chapter 10 — Replication Operations and Troubleshooting
10.1 Oplog Architecture and Sizing  
10.2 Replication Flow and Lag  
10.3 Initial Sync and Resynchronization  
10.4 Rollback  
10.5 Election Troubleshooting  
10.6 Primary and Secondary Unavailability  
10.7 Stale Members and Network Partitions  
10.8 Replica Set Monitoring and Alerts  
10.9 Replication Recovery  
10.10 Production Failure Scenarios and Incident Runbooks

## Chapter 11 — Sharded Cluster Administration
11.1 Sharding Fundamentals and Components  
11.2 Config Server Replica Sets, mongos, and Shards  
11.3 Shard Keys  
11.4 Ranged, Hashed, and Zone Sharding  
11.5 Sharding Collections  
11.6 Balancer Operations and Data Distribution  
11.7 Adding and Removing Shards  
11.8 Resharding  
11.9 Hot Shards and Data Skew  
11.10 Sharded Cluster Monitoring  
11.11 Sharding Failure Scenarios  
11.12 Troubleshooting, Recovery, and Production Runbooks

## Chapter 12 — WiredTiger, Storage, and Capacity Administration
12.1 WiredTiger Administration  
12.2 Data Files, Journal, and Checkpoints  
12.3 WiredTiger Cache and Compression  
12.4 Filesystem Selection and Disk Layout  
12.5 Disk I/O and Space Monitoring  
12.6 Logical Data Size vs. Allocated Storage  
12.7 Reusable Free Space vs. Filesystem Free Space  
12.8 Fragmentation and Space Reuse  
12.9 compact and compact dryRun  
12.10 Disk Space Reclamation Strategies  
12.11 Reclamation vs. Capacity Expansion  
12.12 Capacity Forecasting and Disk Expansion  
12.13 Disk-Full Scenarios and Storage Failure Recovery  
12.14 Capacity Runbooks

## Chapter 13 — Backup Architecture and Administration
13.1 Backup Requirements, RPO, and RTO  
13.2 Backup Consistency  
13.3 mongodump and mongorestore  
13.4 Filesystem and Volume Snapshots  
13.5 Replica Set and Sharded Cluster Backup Strategies  
13.6 Enterprise Backup Capabilities  
13.7 Atlas Backup Considerations  
13.8 Backup Encryption and Retention  
13.9 Backup Monitoring and Validation  
13.10 Automated Restore Testing  
13.11 Backup Failure Scenarios and Production Runbooks

## Chapter 14 — Restore and Disaster Recovery
14.1 Restore Architecture  
14.2 Logical and Snapshot Restore  
14.3 Replica Set Recovery  
14.4 Point-in-Time Recovery Concepts  
14.5 Accidental Data Deletion and Collection/Database Recovery  
14.6 Node and Complete Cluster Loss  
14.7 Regional Failure  
14.8 Disaster Recovery Architecture  
14.9 DR Testing and Recovery Validation  
14.10 DR Runbooks

## Chapter 15 — MongoDB Monitoring and Alerting
15.1 Monitoring Architecture  
15.2 serverStatus, Database, and Collection Statistics  
15.3 Operation Visibility and Diagnostic Data  
15.4 MongoDB Logs  
15.5 CPU, Memory, WiredTiger, Disk, and Connection Metrics  
15.6 Query, Replication, Oplog, and Sharding Metrics  
15.7 Prometheus Integration and Grafana Dashboards  
15.8 Alert Design and Warning/Critical Thresholds  
15.9 Monitoring Runbooks

## Chapter 16 — Performance Administration
16.1 Performance Methodology and Baselines  
16.2 CPU and Memory Analysis  
16.3 WiredTiger Cache Pressure  
16.4 Disk I/O and Connection Analysis  
16.5 Lock and Concurrency Analysis  
16.6 Slow Query and Index Performance  
16.7 Replication Performance  
16.8 Write-Heavy, Read-Heavy, and Batch Workloads  
16.9 Capacity Planning  
16.10 Performance Troubleshooting and Production Runbooks

## Chapter 17 — Production Maintenance and Operational Procedures
17.1 Daily, Weekly, and Monthly DBA Checklists  
17.2 Health Checks and Capacity Reviews  
17.3 Security and Backup Reviews  
17.4 Index and Slow Query Reviews  
17.5 Replica Set and Sharded Cluster Maintenance  
17.6 Certificate and Credential Rotation  
17.7 Storage Expansion and Node Replacement  
17.8 Planned Maintenance Windows and Change Management  
17.9 Operational Evidence and Audit Records

## Chapter 18 — MongoDB Troubleshooting and Failure Scenarios
18.1 Troubleshooting Methodology  
18.2 MongoDB Will Not Start or Crashes  
18.3 High CPU, High Memory, and OOM Kill  
18.4 WiredTiger Cache Pressure  
18.5 High Disk Latency and Disk Full  
18.6 Slow Queries and Connection Exhaustion  
18.7 Authentication and TLS Failures  
18.8 Replication Lag and Election Problems  
18.9 Secondary Out of Sync  
18.10 Index Problems  
18.11 Backup and Restore Failures  
18.12 Sharding Problems and Data Integrity Problems  
18.13 Diagnostic Evidence Collection  
18.14 Escalation Procedures and RCA Development

## Chapter 19 — MongoDB DBA Automation
19.1 Automation Principles  
19.2 MongoDB Shell and Python Administration  
19.3 Health Check, Backup, and Restore Validation Automation  
19.4 User and Index Administration Automation  
19.5 Capacity and Monitoring Automation  
19.6 Configuration Validation and Upgrade Automation  
19.7 Safe Automation Guardrails and Idempotency  
19.8 Secrets Handling  
19.9 Production Automation Runbooks

## Chapter 20 — MongoDB Migration and Upgrade Operations
20.1 Migration Architecture and Assessment  
20.2 Source Inventory and Compatibility Analysis  
20.3 Dump/Restore Migration  
20.4 Replica-Based and Snapshot-Based Strategies  
20.5 Self-Managed to Atlas  
20.6 Server-to-Server and Cloud Migration Considerations  
20.7 Large Database Migration  
20.8 Downtime Planning and Cutover  
20.9 Validation, Rollback, and Data Reconciliation  
20.10 Migration Failure Scenarios and Production Runbooks

## Chapter 21 — MongoDB Production Standards and Governance
21.1 Production Readiness  
21.2 Naming and Configuration Standards  
21.3 Security and Backup Standards  
21.4 Monitoring and Capacity Standards  
21.5 Index and Schema Standards  
21.6 Change Management and Access Reviews  
21.7 Audit and Documentation Requirements  
21.8 Operational Ownership  
21.9 Production Readiness Checklist

## Chapter 22 — MongoDB Production Runbook Library
22.1 MongoDB Health Check  
22.2 High CPU / High Memory / WiredTiger Cache Pressure  
22.3 Disk Space Emergency  
22.4 Slow Queries and Connection Exhaustion  
22.5 Replication Lag and Primary Failure  
22.6 Secondary Recovery and Member Replacement  
22.7 Oplog Capacity Problem  
22.8 Index Build Failure  
22.9 Backup Failure and Restore  
22.10 Accidental Data Deletion  
22.11 Certificate Expiration and Credential Rotation  
22.12 Disk Expansion  
22.13 MongoDB Upgrade and Emergency Rollback  
22.14 Disaster Recovery

## Chapter 23 — Production Incident and Case Study Library
23.1 CPU Saturation During Batch Writes  
23.2 WiredTiger Cache Saturation  
23.3 Disk Exhaustion  
23.4 Deleted-but-Open Files and Disk Reclamation  
23.5 Large Collection Performance Degradation  
23.6 Missing Index / Collection Scan and Index Overhead Incidents  
23.7 Connection Storm  
23.8 Replication Lag and Oplog Window Exhaustion  
23.9 Repeated Elections and Failed Secondary Recovery  
23.10 Failed Backup, Restore, and Upgrade  
23.11 Data Loss / Accidental Deletion  
23.12 Security Incident  
23.13 Multi-Failure Scenario  
23.14 RCA Examples, Lessons Learned, and Preventive Engineering

## Chapter 24 — MongoDB DBA Command and Operations Reference
24.1 mongosh Administration Reference  
24.2 Database and Collection Commands  
24.3 Index Commands  
24.4 User and Role Commands  
24.5 Replica Set and Sharding Commands  
24.6 Monitoring and Diagnostic Commands  
24.7 Backup and Restore Commands  
24.8 Process and OS Commands  
24.9 Common JavaScript Administration Patterns  
24.10 Common Linux Troubleshooting Commands  
24.11 Configuration Parameter Reference  
24.12 Production Checklists and Emergency Command Reference

---

## Architecture Lock

This 24-chapter structure is the canonical **MongoDB Administration Handbook Master TOC v1.0**. Chapter and section structure must not be changed without an explicit architecture revision. Drafting begins with **1.1 — What Is MongoDB?**.