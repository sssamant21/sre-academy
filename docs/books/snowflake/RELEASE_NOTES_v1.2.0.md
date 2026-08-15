# Snowflake Enterprise Handbook v1.2.0 Release Notes

Release date: 2026-08-15  
Status: Production Release  
Theme: Production Simulations and Assessment

## Overview

Version 1.2.0 turns the handbook's operational guidance into a complete practice, assessment and reference experience. It builds on the production-ready v1.1.0 labs, runbooks and reader paths without changing the validated 20-chapter core.

## Added

### Incident simulations

Six facilitated production-incident simulations:

- warehouse saturation
- query performance regression
- unexpected credit spike
- failed task graph
- authentication and network-policy outage
- dynamic-table freshness breach

Each simulation defines learning objectives, safety boundaries, injects, evidence requirements, remediation and recovery checks.

### Facilitator guides

Six matching facilitator guides with a common 24-point scoring rubric, timing guidance, expected evidence, decision gates, debrief prompts and reset instructions.

### Chapter assessments

Sixty questions spanning Chapters 01–20, organized into four assessment sets. The separate answer appendix provides sixty concise answers with chapter references for review and remediation.

### Unified reference layer

- a handbook-wide Snowflake glossary
- an acronym reference with handbook context
- a task-oriented SQL and command index
- links to current official Snowflake reference material

## Release inventory

| Area | Included |
|---|---:|
| Core chapters | 20 |
| Hands-on labs | 8 |
| Production runbooks | 6 |
| Incident simulations | 6 |
| Facilitator guides | 6 |
| Assessment questions | 60 |
| Assessment answers | 60 |
| Unified reference pages | 4 |
| Snowflake Markdown files | 83 |

## Validation

The release passed:

- the Snowflake handbook structural validator
- the Snowflake reader-experience validator
- MkDocs strict build and documentation checks
- Snowflake handbook integrity checks
- GitHub Pages deployment validation

Vendor behavior, syntax, privileges, edition and regional availability remain governed by the linked official Snowflake documentation.
