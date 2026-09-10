# Snowflake DBRE/SRE Production Runbook

Production operational playbooks for Snowflake DBRE/SRE and on-call engineers.

**Scope:** problem → diagnosis → action → validation → rollback/escalation  
**Version:** v1.0  
**Runbooks:** 90  
**Canonical progress:** 9/90

## Standard Runbook Template

Trigger / Alert → Impact → Severity → Safety Checks → Required Access → Diagnosis → SQL/Commands → Decision Points → Remediation → Validation → Rollback → Escalation → Evidence to Capture → References

## 1. Access & Authentication

- [RB-001 — Reset User Password](access-authentication/RB-001-reset-user-password.md) — **CANONICAL**
- [RB-002 — Unlock/Restore User Access](access-authentication/RB-002-unlock-restore-user-access.md) — **CANONICAL**
- [RB-003 — Troubleshoot Login/Authentication Failure](access-authentication/RB-003-troubleshoot-login-authentication-failure.md) — **CANONICAL**
- [RB-004 — MFA Recovery](access-authentication/RB-004-mfa-recovery.md) — **CANONICAL**
- [RB-005 — Key-Pair Authentication Failure](access-authentication/RB-005-key-pair-authentication-failure.md) — **CANONICAL**
- [RB-006 — SSO/OAuth Failure](access-authentication/RB-006-sso-oauth-failure.md) — **CANONICAL**
- [RB-007 — Network Policy Blocking Access](access-authentication/RB-007-network-policy-blocking-access.md) — **CANONICAL**
- [RB-008 — Emergency/Break-Glass Access](access-authentication/RB-008-emergency-break-glass-access.md) — **CANONICAL**

## 2. Roles, Grants & Permissions

- [RB-009 — Grant User/Role Access](roles-grants-permissions/RB-009-grant-user-role-access.md) — **CANONICAL**
- RB-010 — Troubleshoot Insufficient Privileges — **NEXT: DRAFT**
- RB-011 through RB-014.

## 3. Warehouse & Compute

RB-015 through RB-022.

## 4. Query Performance

RB-023 through RB-032.

## 5. Data Loading & Pipelines

RB-033 through RB-040.

## 6. Streams, Tasks & Dynamic Tables

RB-041 through RB-047.

## 7. Storage & Data Recovery

RB-048 through RB-054.

## 8. Cost & Capacity

RB-055 through RB-061.

## 9. Connectivity & Integrations

RB-062 through RB-069.

## 10. Replication & Disaster Recovery

RB-070 through RB-076.

## 11. Security Incidents

RB-077 through RB-082.

## 12. Snowflake Service & Major Incidents

RB-083 through RB-090.

## Canonical Workflow

`Draft → Technical + Source Review → Production + Copyright Review → Revised Final / Canonical Edition → Commit → Status Update → Next Runbook`

See [STATUS.md](STATUS.md) for current progress.
