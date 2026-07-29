# SRE-Academy Documentation Bible

## Purpose

This document is the central authoring standard for the SRE-Academy Kubernetes Engineering Handbook.

Use it when creating, integrating, reviewing, or publishing handbook content. It complements the author style guide, engineering review checklist, publishing checklist, roadmap, and book outline.

## Core Principles

- Treat approved manuscript content as canonical.
- Do not rewrite author content unless explicitly instructed.
- Keep repository engineering changes separate from technical manuscript changes.
- Explain why a system behaves a certain way before explaining how to operate it.
- Write for engineers who operate production systems.
- Prefer real operational judgment over certification-style summaries.
- Preserve technical meaning when fixing Markdown, lint, or build issues.

## Repository Editing Rules

- Do not modify published chapter content during infrastructure-only changes.
- Do not delete documentation unless the deletion is explicitly requested.
- Do not move pages without updating navigation and internal links.
- Preserve existing MkDocs navigation conventions.
- Keep pull requests focused on one clear purpose.
- Use authoring files for planning, tracking, and review guidance.
- Use `docs/` files for published or publishable documentation.

## Manuscript Integration Rules

When integrating an approved manuscript:

- Insert the manuscript exactly as supplied.
- Preserve headings, paragraphs, tables, lists, callouts, code blocks, and Mermaid diagrams.
- Remove duplicate mid-page front matter only when appending to an existing canonical page.
- Fix only formatting or build issues that prevent validation.
- Do not summarize, shorten, or change technical meaning.
- Do not claim technical authorship of ChatGPT-authored manuscript content.

## Chapter Structure

Each chapter should have a clear landing page or index when appropriate.

Each major section should have a canonical manuscript file.

Supporting assets should live near the chapter when they are chapter-specific:

```text
docs/chapter-XX/
  index.md
  X.Y-section-title.md
  diagrams/
  examples/
  labs/
  references/
```

Shared authoring and planning documents should live under `author/`.

## Section Structure

Every major topic should include these elements where appropriate:

- Architecture
- Internal workflow
- Production examples
- Failure scenarios
- SRE Insight
- Engineering Note
- Best Practices
- Common Pitfalls
- Summary

Not every section needs every element, but omissions should be intentional.

## Heading Standards

- Use a single top-level heading for each standalone page unless the canonical manuscript requires otherwise.
- Maintain a consistent heading hierarchy.
- Avoid duplicate headings when possible.
- If repeated headings are required by the manuscript, use explicit anchors or local markdownlint exceptions without changing visible manuscript wording.

## Markdown Standards

- Use valid Markdown.
- Use fenced code blocks.
- Specify a language for code fences when appropriate.
- Use `text` for conceptual snippets, command output, or plain text examples.
- Keep tables simple and readable.
- Avoid broken relative links.
- Validate image references before publication.

## Mermaid Standards

Use Mermaid diagrams for architecture, request flow, reconciliation, ownership, lifecycle, and failure paths when they improve understanding.

Before publication:

- Validate Mermaid syntax.
- Confirm diagrams render in MkDocs Material.
- Keep labels clear and concise.
- Prefer diagrams that explain relationships over decorative diagrams.

## SRE Content Standards

Production handbook content should emphasize:

- Control-plane behavior
- Failure modes
- Observability signals
- Performance limits
- Security boundaries
- Operational trade-offs
- Recovery patterns
- Automation behavior
- Capacity and scaling considerations

The reader should understand how the system behaves under normal and failure conditions.

## Review Workflow

Before marking a section complete:

1. Confirm technical accuracy.
2. Confirm behavior matches upstream Kubernetes where applicable.
3. Check production relevance.
4. Review performance and scaling implications.
5. Review security and access-control implications.
6. Confirm observability and troubleshooting guidance.
7. Validate diagrams and code examples.
8. Run documentation checks.
9. Confirm navigation and links.
10. Complete editorial review.

## Validation Requirements

Every documentation pull request should pass:

- Markdown lint
- Vale/style checks
- MkDocs build
- Link validation
- Mermaid rendering checks when diagrams are added or changed

If a check fails, fix the smallest issue necessary and preserve the technical meaning of the content.

## Pull Request Standards

Each pull request should include:

- Summary of changes
- Files added or modified
- Validation status
- Notes about formatting-only fixes
- Confirmation when existing manuscript content was not modified

Use draft pull requests for incomplete scaffolding, planning, or review-in-progress work.

Mark a pull request ready for review only after checks pass and the work is ready for human review.

## Publication Standard

A section is ready for publication only when:

- The manuscript is complete.
- Engineering review is complete.
- Editorial review is complete.
- Navigation is correct.
- Links are valid.
- Diagrams render.
- MkDocs builds successfully.
- The publishing checklist is complete.

## Source of Truth

Use these files together:

- `author/documentation-bible.md` for the overall documentation standard.
- `author/style-guide.md` for writing style.
- `author/engineering-review-checklist.md` for technical review.
- `author/publishing-checklist.md` for release readiness.
- `author/book-outline.md` for chapter and section planning.
- `author/roadmap.md` for authoring direction.
