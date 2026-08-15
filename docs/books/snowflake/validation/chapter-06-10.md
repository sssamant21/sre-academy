# Snowflake Vendor Validation Matrix — Chapters 6–10

Validation date: 2026-08-15  
Status: Technical review complete for the claims listed below  
Source policy: Official Snowflake documentation only

| Area | Chapters | Validation result | Action |
|---|---:|---|---|
| Multi-cluster warehouses | 6, 7, 9, 10 | Confirmed; Enterprise Edition or higher | Added edition, Auto-scale, configured-limit, concurrency, and cost qualifications |
| Auto-suspend and warehouse cache | 6, 9 | Confirmed | Retained workload-specific tuning guidance and cache-loss-on-suspension context |
| Resource monitors | 6, 10 | Scope required clarification | Limited claims to supported user-managed warehouse credit governance and distinguished Snowflake Budgets |
| Performance features | 7 | Confirmed with edition and workload constraints | Added Enterprise Edition qualification and retained evidence-based Query Profile testing |
| MFA and strong authentication | 8 | Current rollout materially changed guidance | Added single-factor password deprecation, mandatory MFA direction for human password users, and non-password authentication for service users |
| SSO with MFA | 8 | Conditional | Clarified that Snowflake relies on the IdP by default unless an authentication policy enforces Snowflake MFA |
| Access History | 8 | Enterprise Edition feature | Added edition qualification |
| Private connectivity and Tri-Secret Secure | 8 | Edition/cloud/region dependent | Added explicit deployment validation requirement |
| ACCOUNT_USAGE | 7, 9, 10 | Historical, commonly 365-day retention | Added per-view latency and retention qualification; not guaranteed real-time |
| Time Travel | 9, 10 | One-day standard; up to 90 days with Enterprise Edition or higher | Added edition and storage-cost qualification |
| Snowflake Budgets | 10 | Broader than resource monitors, with limitations | Recorded 100 custom-budget account limit and unsupported Hybrid Table monitoring |

## Primary sources

- [Multi-cluster warehouses](https://docs.snowflake.com/en/user-guide/warehouses-multicluster)
- [Resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [Snowflake Budgets](https://docs.snowflake.com/en/user-guide/budgets)
- [MFA](https://docs.snowflake.com/en/user-guide/security-mfa)
- [Single-factor password deprecation](https://docs.snowflake.com/en/user-guide/security-mfa-rollout)
- [Access History](https://docs.snowflake.com/en/sql-reference/account-usage/access_history)
- [Account Usage](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel)

## Review limitation

Telemetry latency, retention, edition requirements, regional availability, and preview/GA status can differ by feature and view. Revalidate these constraints before production implementation.
