# Facilitator Guide: Rapid Error-Budget Burn

Version: v1.3.0  
Status: In development  
Duration: 60–75 minutes  
Last reviewed: 2026-08-16

## Learning outcomes

Participants should validate the SLI and customer impact, distinguish queueing from query regression, apply the error-budget policy and reject unbounded capacity changes.

## Facilitation sequence

| Time | Inject | Expected response |
|---:|---|---|
| 0 min | 60% monthly budget consumed in two hours | Declare investigation, identify service/SLI version and verify impact |
| 10 min | Account Usage data is delayed | Check metric quality and obtain bounded lower-latency evidence |
| 20 min | Queueing affects one workload class | Narrow scope; compare concurrency, workload timing and change history |
| 30 min | Unverified warehouse policy change | Preserve state and evaluate rollback/change correction |
| 40 min | Request for global resize | Require blast-radius, isolation, cost, rollback and recovery criteria |
| 50 min | Queueing improves after bounded correction | Validate consumer latency and budget trend; communicate next review |

## Strong response characteristics

- does not edit eligibility or exclusions during the event;
- treats delayed telemetry as a limitation, not proof of health;
- invokes the correct technical runbook after evidence supports a failure mode;
- applies risk restrictions proportionate to budget state;
- records a controlled change and post-change verification.

## Coaching flags

- immediate resize without diagnosis;
- treating query success as proof of latency health;
- confusing an internal SLO with a vendor SLA;
- closing when queueing falls without validating customer outcome.

## Debrief

1. Which evidence changed the decision?
2. What made the resize request unsafe or incomplete?
3. Which policy action follows elevated or exhausted budget?
4. What monitoring or change-control improvement prevents recurrence?

Use the [common rubric](index.md#common-24-point-rubric).

