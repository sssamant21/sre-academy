# Case Study: Secure-Sharing Policy Failure

Version: v1.5.0
Status: In development
Last vendor validation: 2026-08-16

Fictional composite; no real consumer data is represented.

## Incident

A consumer's approved database role returned zero rows from a policy-protected shared view after a provider policy release. The provider's internal test role still returned data, and the share and imported database remained available.

## Evidence

The provider compared share grants, database-role grants, policy references and access history. The new row access policy used `IS_ROLE_IN_SESSION`, which evaluated provider account roles and did not recognize the shared database role expected in the consumer context. The approved design required `IS_DATABASE_ROLE_IN_SESSION` and sharing the database containing the policy and protected data.

```sql
SELECT *
FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(
  REF_ENTITY_NAME => 'SHARED_PRODUCT.SERVING.V_ORDERS',
  REF_ENTITY_DOMAIN => 'VIEW'));

SHOW GRANTS TO SHARE ORDERS_SHARE;
```

## Root cause and recovery

Root cause: the policy function was changed without a consumer-context regression test. Contributors were provider-only testing and no golden results for each shared database role.

The provider restored the prior policy definition, validated authorized and unauthorized consumer roles in a test account, then republished the corrected change. It did not grant the consumer direct base-table access as a shortcut.

## Preventive actions

- Test policy DDL in a real provider/consumer account pair.
- Maintain positive and negative golden queries for every shared role.
- Version the share, database-role and policy graph together.
- Alert on sudden zero-row or access-error changes for critical consumers.
- Preserve `ACCESS_HISTORY.policies_referenced` evidence where available.
- Include consumer communication and rollback in policy change review.

## Official references

- [Share policy-protected data](https://docs.snowflake.com/en/user-guide/data-sharing-policy-protected-data)
- [`IS_DATABASE_ROLE_IN_SESSION`](https://docs.snowflake.com/en/sql-reference/functions/is_database_role_in_session)
- [Share secure objects](https://docs.snowflake.com/en/user-guide/data-sharing-gs)
- [Access History](https://docs.snowflake.com/en/user-guide/access-history)

