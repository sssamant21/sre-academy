# Facilitator Guide: Recovery-Readiness Gap

Version: v1.3.0  
Status: Production Release  
Duration: 75 minutes  
Last reviewed: 2026-08-16

## Learning outcomes

Participants should separate replication success from service recoverability, identify missing customer-owned dependencies and create a controlled corrective exercise.

## Facilitation sequence

| Time | Inject | Expected response |
|---:|---|---|
| 0 min | Refresh completed inside RPO | Verify protected scope and actual data timestamp |
| 15 min | Secondary data readable; service role cannot access it | Identify grant/role recovery gap and ownership |
| 25 min | Required integrations are absent | Map non-data dependencies and implementation constraints |
| 40 min | Application rerouting needs another team/approvals | Add external dependency, authority and elapsed time to RTO |
| 55 min | Leadership asks for production failover now | Decline absent incident authority and safe end-to-end procedure |
| 65 min | Corrective exercise window is offered | Define prechecks, success, rollback, failback and evidence package |

## Strong response characteristics

- calculates RPO from verified evidence rather than schedule alone;
- makes customer-owned RTO steps visible;
- distinguishes replication groups from failover capability;
- checks roles, integrations, policies and application routing;
- requires failback readiness and business validation.

## Coaching flags

- declaring recovery ready from `COMPLETED` refresh alone;
- production failover during a tabletop exercise;
- excluding external routing and approvals from RTO;
- validating data while ignoring service access and correctness.

## Debrief

1. Which dependency was most important to RTO?
2. What evidence supports the RPO calculation?
3. What edition or region constraints need confirmation?
4. What must the next exercise prove?

Use the [common rubric](index.md#common-24-point-rubric).

