# Lab Authoring Standard

Version: v1.1.0  
Status: Active standard  
Last reviewed: 2026-08-15

## Required front matter

Each lab states its objective, audience, estimated duration, cost risk, required privileges, edition or region constraints and last vendor-validation date.

## Object isolation

Use a recognizable prefix such as `HB_LAB_`. Do not reuse production roles, warehouses, databases, schemas, stages or integrations. Setup and cleanup statements must name every affected object explicitly.

## Evidence

A lab distinguishes:

- **Expected observation:** a structural or behavioral result supported by Snowflake documentation.
- **Measured result:** a timing, scan, queue or credit value produced by the reader's account.
- **Success criterion:** evidence that the reader completed the objective.

Never present measured results as universal performance guarantees.

## SQL quality

- Use bounded time predicates on history views.
- Select only the columns needed for the exercise.
- Explain required role or database-role grants.
- Identify Account Usage latency where it affects interpretation.
- Avoid destructive statements unless they operate exclusively on lab-owned objects.
- Provide cleanup with `IF EXISTS` when the relevant command supports it.

## Vendor validation

References must link to official Snowflake documentation. Revalidate a lab when its referenced command, view, privilege model, interface or feature status changes.
