# Runbook Authoring Standard

Version: v1.1.0  
Status: Active standard  
Last reviewed: 2026-08-15

## Required sections

A production runbook must include scope, triggers, severity guidance, required access, safety constraints, evidence collection, diagnosis, mitigation, validation, rollback, escalation, communications and references.

## Operational principles

- Preserve query IDs, timestamps, warehouse names, session context and error messages before changing the system.
- Use bounded history queries and identify telemetry latency.
- Prefer reversible changes with explicit owners and expiry times.
- Separate overload, provisioning, locking, network, authentication and SQL causes.
- Do not resize a warehouse solely because one query is slow.
- Do not suspend or abort shared workloads without incident authority.
- Never place credentials, tokens or private keys in an incident ticket.
- Record the exact before-and-after configuration.

## Closure criteria

Close the runbook only when service indicators recover, the mitigation is stable, follow-up risk is owned and temporary changes have an expiry or rollback plan.
