# DBRE Simulation Facilitator Guides

Version: v1.3.0  
Status: In development  
Last reviewed: 2026-08-16

These guides contain scenario injects, expected reasoning and scoring guidance. Participants should complete the simulation before opening its guide.

## Common 24-point rubric

Score each category from 0–4.

| Category | 0 | 2 | 4 |
|---|---|---|---|
| Safety and authority | Unsafe or unauthorized action | Risk identified, controls incomplete | Narrow, authorized, reversible decisions with clear stop conditions |
| Evidence quality | Assumes cause | Partial or stale evidence | Validates scope, freshness, completeness and comparable evidence |
| Reliability reasoning | Confuses indicator, objective and cause | Plausible but incomplete | Connects customer outcome, SLO/budget, dependencies and contributing signals |
| Decision control | Unowned or open-ended action | Owner or expiry missing | Owned, time-bound decision with rollback and escalation |
| Validation and learning | No recovery criteria | One technical check | Validates customer outcome, metric integrity, recurrence and corrective actions |
| Communication | No impact or timeline | Basic status | Clear UTC timeline, uncertainty, decision, owner and next update |

Interpretation:

- 21–24: production-ready DBRE response;
- 17–20: operationally competent with minor gaps;
- 12–16: coaching required;
- below 12: repeat after remediation.

## Facilitation rules

- Score observable reasoning and decisions, not preferred wording.
- Do not reveal later injects early.
- Require participants to identify uncertainty and telemetry limitations.
- Stop an unsafe production action; simulations authorize tabletop decisions only.
- Capture one strength, one material gap and one corrective exercise per participant/team.

## Guides

- [Rapid error-budget burn](rapid-error-budget-burn.md)
- [Observability blind spot](observability-blind-spot.md)
- [Recovery-readiness gap](recovery-readiness-gap.md)

