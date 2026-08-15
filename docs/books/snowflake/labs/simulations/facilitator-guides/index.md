# Incident Simulation Facilitator Guides

Version: v1.2.0  
Status: Production Release  
Last vendor validation: 2026-08-15

These guides contain expected reasoning and scoring guidance for the six incident simulations. Participants should complete a simulation before opening its guide.

## Common scoring rubric

Score each category from 0–4 for a maximum of 24 points.

| Category | 0 | 2 | 4 |
|---|---|---|---|
| Safety | Creates unacceptable risk | Identifies risk but controls are incomplete | Uses narrow, reversible and authorized actions |
| Evidence | Guesses without evidence | Collects partial evidence | Uses bounded, comparable and relevant evidence |
| Diagnosis | Treats symptoms as cause | Plausible but incomplete cause | Identifies primary cause and contributing factors |
| Mitigation | Unowned or irreversible | Partially controlled | Direct, reversible, owned and time-bound |
| Validation | No measurable recovery criteria | Checks one signal | Validates service, correctness, cost and recurrence |
| Communication | No impact/timeline clarity | Basic update | Clear UTC timeline, impact, action and next update |

Suggested interpretation:

- 21–24: production-ready response
- 17–20: competent with minor gaps
- 12–16: requires coaching
- below 12: repeat the exercise

## Guides

- [Warehouse Saturation](warehouse-saturation.md)
- [Query Regression](query-regression.md)
- [Unexpected Credit Spike](unexpected-credit-spike.md)
- [Failed Task Graph](failed-task-graph.md)
- [Authentication and Network-Policy Outage](authentication-network-policy-outage.md)
- [Dynamic-Table Freshness Breach](dynamic-table-freshness-breach.md)
