# Facilitator Guide: Observability Blind Spot

Version: v1.3.0  
Status: Production Release  
Duration: 60 minutes  
Last reviewed: 2026-08-16

## Learning outcomes

Participants should mark service state unknown, establish impact using alternate evidence, correct monitoring access safely and reconcile the blind interval.

## Facilitation sequence

| Time | Inject | Expected response |
|---:|---|---|
| 0 min | Customer reports missing data; dashboard is green | Check source event time and customer evidence |
| 10 min | Curated dataset is 95 minutes stale | Mark dashboard unknown/delayed and communicate blind window |
| 20 min | Monitoring task failed after a privilege change | Preserve history; inspect least privilege and recent change |
| 30 min | Proposed fix grants broad admin role | Reject; use approved minimum privileges and change control |
| 40 min | Critical pipeline also failed | Separate monitoring incident from service incident; invoke pipeline runbook |
| 50 min | Proposed backfill is unbounded | Bound range, test idempotency/cost and reconcile results |

## Strong response characteristics

- never converts missing telemetry into a zero or healthy value;
- maintains two tracks: restore service and restore trustworthy observation;
- avoids privilege escalation as a shortcut;
- documents decisions made during the blind window;
- tests dashboard freshness indicators and alert delivery after repair.

## Coaching flags

- trusting dashboard color without source timestamps;
- broad role grant to make monitoring work;
- unbounded Account Usage scan or backfill;
- closing the service issue when monitoring alone recovers.

## Debrief

1. When should state become unknown instead of critical?
2. Which independent evidence was safe and relevant?
3. How should the blind interval affect SLO calculation?
4. What metric contract fields would have exposed this sooner?

Use the [common rubric](index.md#common-24-point-rubric).

