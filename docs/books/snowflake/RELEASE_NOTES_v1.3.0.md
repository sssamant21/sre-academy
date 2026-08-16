# Snowflake Enterprise Handbook v1.3.0 Release Notes

Release date: 2026-08-16
Status: Production Release
Theme: DBRE and Reliability Engineering

## Overview

Version 1.3.0 adds a complete Database Reliability Engineering operating and learning system for Snowflake workloads. It connects service ownership, reliability objectives, operational controls, dashboards, runbooks, practice and assessment to the existing 20-chapter handbook.

The release defines enterprise DBRE practices without presenting them as Snowflake-prescribed organizational models or contractual service commitments. Product-specific claims retain links to current official Snowflake documentation.

## Added

### DBRE foundation

- customer-owned reliability boundary and operating model;
- service catalog, criticality tiers, ownership and RACI baseline;
- SLI, SLO and error-budget framework;
- integrated performance, pipeline, security, change, recovery and cost controls;
- evidence-based production-readiness standard;
- five-level DBRE maturity model.

### Operational dashboards and runbooks

- six decision-oriented dashboard specifications;
- versioned metric data-contract standard;
- runbooks for SLO burn, telemetry gaps, alert-quality failure, recovery-readiness risk and configuration drift.

### Practice and assessment

- six hands-on DBRE labs;
- three incident-style reliability simulations;
- three facilitator guides and a common 24-point rubric;
- 30 assessment questions and a separate 30-answer appendix.

## Release inventory

| Area | Included |
|---|---:|
| Core handbook chapters | 20 |
| Total Snowflake Markdown files | 118 |
| DBRE pages | 34 |
| DBRE dashboard views specified | 6 |
| DBRE reliability runbooks | 5 |
| DBRE practical labs | 6 |
| DBRE simulations | 3 |
| DBRE facilitator guides | 3 |
| DBRE assessment questions | 30 |
| DBRE assessment answers | 30 |

## Validation

The release passed:

- Snowflake handbook structural validation for all 20 chapters;
- reader-experience validation for all 118 Snowflake Markdown files;
- strict MkDocs build and navigation validation;
- GitHub documentation and Snowflake integrity checks;
- GitHub Pages deployment validation before publication.

## Upgrade notes

- Existing v1.2.0 chapters, labs, runbooks, simulations and assessments remain valid.
- DBRE pages link to existing authoritative procedures rather than duplicating them.
- Organizations should adapt RACI, criticality, SLO and maturity policies to their own governance and contractual requirements.
- Edition, region, privilege, telemetry latency and feature-status requirements must be revalidated before implementation.

