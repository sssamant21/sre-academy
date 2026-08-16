# Data Ingestion and Real-Time Pipelines

Version: v1.4.0
Status: In development
Last vendor validation: 2026-08-16

Select an ingestion pattern from the source contract and freshness objective—not from a product name.

| Source and need | Primary pattern | Key trade-off |
|---|---|---|
| Periodic files; controlled batch window | [`COPY INTO`](bulk-copy.md) | Simple and auditable; warehouse and scheduling required |
| Files arriving continuously | [Snowpipe auto-ingest](snowpipe-auto-ingest.md) | Event-driven convenience; notification path must be operated |
| Application rows without staged files | [Snowpipe Streaming](snowpipe-streaming.md) | Low-latency ingestion; client/channel lifecycle adds complexity |
| Kafka topics | [Kafka connector v4](kafka-connector.md) | Managed connector semantics; version and mapping need governance |
| Rate-limited external API | [Durable micro-batches](api-microbatch.md) | Replayable and source-friendly; freshness follows batch cadence |
| Landing-to-curated change processing | [Streams and triggered tasks](streams-triggered-tasks.md) | Incremental SQL processing; stream staleness and task failures need controls |

## Shared production rules

- Land immutable source data before destructive transformations.
- Carry a source event ID, event time, ingestion time and source position where available.
- Define duplicate, late-arrival, schema-change and poison-record policies before launch.
- Use least-privilege service roles and storage integrations; do not embed cloud credentials.
- Measure freshness, completeness, correctness, duplicate rate and rejected records.
- Test replay and recovery, not only the happy path.
