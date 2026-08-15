# Facilitator Guide: Failed Task Graph

Version: v1.2.0  
Status: Vendor-validated facilitator guide  
Last vendor validation: 2026-08-15

## Expected diagnosis

A child task fails because its SQL references a renamed column. The graph is incomplete, but the failed child produced no partial rows. Replay eligibility depends on whether the graph is modified while correcting the task.

## Strong response

1. Use graph-run identifiers to locate the first failed task.
2. Validate task state, owner privileges and error evidence.
3. Confirm downstream non-execution and absence of partial side effects.
4. Decide whether rollback preserves `RETRY LAST` eligibility.
5. If the task must be modified, use a controlled alternative rather than assuming retry remains allowed.
6. Validate data completeness, duplicates, freshness and the next schedule.

## Common mistakes

- Retrying before idempotency review.
- Restarting the entire graph blindly.
- Treating downstream non-runs as separate failures.
- Changing ownership or grants without preserving state.
- Closing after task success without data validation.

## Example corrective actions

- Add schema-contract validation before deployment.
- Test task SQL against proposed upstream schema changes.
- Add failure notifications with graph and query identifiers.
- Document replay safety for every task with external or non-idempotent effects.

## Official references

- [Troubleshooting tasks](https://docs.snowflake.com/en/user-guide/tasks-ts)
- [EXECUTE TASK](https://docs.snowflake.com/en/sql-reference/sql/execute-task)
