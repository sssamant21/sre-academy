# Snowflake Vendor Validation Matrix — Chapters 16–20

Validation date: 2026-08-15  
Source policy: Official Snowflake documentation only

| Area | Chapters | Validation result and correction |
|---|---:|---|
| Replication and RPO | 16, 20 | Asynchronous; RPO follows refresh schedule and secondary lag can reach documented bounds |
| Failover/failback | 16, 17, 20 | Business Critical Edition or higher; dependencies and unsupported objects need separate procedures |
| Replicated privileges and objects | 16–17 | Support varies; REPLICATE and FAILOVER privileges are not replicated |
| Terraform automation | 17–18 | Only latest provider officially supported; preview resources disabled by default |
| Cortex AI operations | 18, 20 | Feature/model region, privileges, preview status, and token costs require validation |
| SLO/SLA operating model | 19 | Enterprise targets, not implied Snowflake contractual guarantees |
| Private connectivity | 20 | Commonly Business Critical or higher and cloud-specific |
| Reference architectures | 20 | Edition, region, feature maturity, dependencies, RPO/RTO, identity, networking, and cost made mandatory inputs |

## Primary sources

- [BCDR introduction](https://docs.snowflake.com/en/user-guide/replication-intro)
- [Account replication](https://docs.snowflake.com/en/user-guide/account-replication-intro)
- [Replication considerations](https://docs.snowflake.com/en/user-guide/account-replication-considerations)
- [Terraform provider](https://docs.snowflake.com/en/user-guide/terraform)
- [Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)
- [Supported cloud platforms](https://docs.snowflake.com/en/user-guide/intro-cloud-platforms)
- [AWS PrivateLink](https://docs.snowflake.com/en/user-guide/admin-security-privatelink)
