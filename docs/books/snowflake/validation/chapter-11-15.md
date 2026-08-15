# Snowflake Vendor Validation Matrix — Chapters 11–15

Validation date: 2026-08-15  
Source policy: Official Snowflake documentation only

| Area | Chapters | Validation result and correction |
|---|---:|---|
| Alerts and tasks | 11–13 | Serverless compute is Snowflake-managed and capped at the documented XXLARGE equivalent; telemetry can have view-specific latency |
| SQL API | 12 | AUTOCOMMIT must be TRUE per statement; PUT/GET are unsupported; session-scoped operations require supported multi-statement patterns |
| Terraform provider | 12 | Only the latest provider version is officially supported; preview resources are disabled by default and can introduce breaking changes |
| ACCOUNT_USAGE | 11, 13, 15 | Historical telemetry with view-specific latency and retention, not a uniform real-time feed |
| Query Profile and optimizer internals | 11, 13, 14 | Runtime evidence is documented; complete optimizer algorithms remain proprietary |
| Materialized views and Search Optimization | 14 | Enterprise Edition-or-higher features with storage/maintenance costs and restrictions |
| Legacy Worksheets and Dashboards | 15 | Retired in 2026; new implementations must use supported visualization surfaces, Workspaces, Streamlit, or external BI |

## Primary sources

- [Alerts](https://docs.snowflake.com/en/user-guide/alerts)
- [Tasks](https://docs.snowflake.com/en/user-guide/tasks-intro)
- [SQL API](https://docs.snowflake.com/en/developer-guide/sql-api/intro)
- [Terraform provider](https://docs.snowflake.com/en/user-guide/terraform)
- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Query Profile](https://docs.snowflake.com/en/user-guide/ui-query-profile)
- [Legacy Worksheets and Dashboards retirement](https://docs.snowflake.com/en/release-notes/bcr-bundles/un-bundled/bcr-2260)
