# SRE-Academy Author Style Guide

## Writing Standard

Write for engineers who operate production systems.

Use engineering-first writing. Explain why a system behaves the way it does before explaining how to operate it.

Avoid certification-style writing. The handbook should teach real operational judgment, not only exam definitions.

Prefer declarative explanations over procedural lists when describing architecture, control loops, and production behavior.

Use consistent terminology throughout the handbook.

## Major Topic Structure

Every major topic should include the following elements where appropriate:

- Architecture
- Internal workflow
- Production examples
- Failure scenarios
- SRE Insight
- Engineering Note
- Best Practices
- Common Pitfalls
- Summary

## Diagrams

Use Mermaid diagrams where they clarify architecture, request flow, ownership, reconciliation, or failure handling.

Validate Mermaid syntax before publication.

## Code Blocks

Use fenced code blocks with an explicit language identifier when appropriate.

Use `text` for plain terminal output or conceptual snippets that are not tied to a specific language.

## Terminology

Use Kubernetes terms consistently with upstream Kubernetes documentation.

Prefer precise component names such as API Server, kubelet, scheduler, controller, and etcd.
