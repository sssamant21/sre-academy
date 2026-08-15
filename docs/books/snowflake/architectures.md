# Snowflake Operational Architecture Diagrams

Version: v1.1.0  
Status: Production Release  
Last reviewed: 2026-08-15

These diagrams are conceptual operating models. They do not describe Snowflake's undisclosed internal implementation and must be adapted to each account, cloud and network design.

## Query investigation flow

```mermaid
flowchart TD
    A["User or alert reports latency"] --> B["Capture query ID and UTC window"]
    B --> C{"Dominant signal?"}
    C -->|Scan or operator cost| D["Inspect Query Profile"]
    C -->|Queued or blocked| E["Inspect warehouse load"]
    C -->|Authentication or network| F["Inspect login and client evidence"]
    D --> G["Apply one reversible change"]
    E --> G
    F --> G
    G --> H["Validate service and cost indicators"]
```

## Workload and warehouse isolation

```mermaid
flowchart TD
    A["Workload classification"] --> B{"Service objective"}
    B -->|Interactive| C["Interactive warehouse"]
    B -->|Batch| D["Batch warehouse"]
    B -->|Administration| E["Operations warehouse"]
    C --> F["Query and load telemetry"]
    D --> F
    E --> F
    F --> G["SLO and cost review"]
```

Isolation reduces interference but increases the number of objects and cost controls that operators must govern. It is an engineering decision, not a universal requirement.

## Incident evidence pipeline

```mermaid
flowchart LR
    A["Query, task, login and load history"] --> B["Bounded evidence collection"]
    B --> C["Incident timeline"]
    C --> D["Diagnosis and mitigation"]
    D --> E["Validation and rollback decision"]
    E --> F["RCA and follow-up actions"]
```

## Release and operational control

```mermaid
flowchart TD
    A["Source-controlled change"] --> B["Automated validation"]
    B --> C{"Checks pass?"}
    C -->|No| D["Correct and revalidate"]
    D --> B
    C -->|Yes| E["Reviewed promotion"]
    E --> F["Production observation"]
    F --> G{"Indicators healthy?"}
    G -->|No| H["Rollback or incident response"]
    G -->|Yes| I["Close change record"]
```

## Usage guidance

- Use the query flow with the performance-investigation template.
- Use workload isolation with Chapters 6, 9, 10 and 19.
- Use the incident evidence pipeline with every production runbook.
- Use release control with Chapters 12 and 18.
