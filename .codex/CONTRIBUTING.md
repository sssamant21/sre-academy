# Codex Contribution Guide

This guide defines how Codex should contribute to the SRE Academy documentation repository.

## Codex responsibilities

- Preserve the author's technical intent and voice.
- Keep changes scoped to the user's request.
- Validate documentation changes before opening a pull request.
- Explain structural changes clearly in commits and pull requests.
- Flag uncertainty instead of guessing about Kubernetes, SRE, cloud, or datastore behavior.
- Prefer small, reviewable pull requests over broad rewrites.

## Repository standards

- Keep documentation source under `docs/` unless the file is repository infrastructure.
- Keep MkDocs navigation in `mkdocs.yml` synchronized with new, moved, or removed pages.
- Preserve existing chapter content unless the task explicitly allows editing it.
- Use descriptive filenames with lowercase words separated by hyphens.
- Keep examples production-minded and operationally useful.
- Avoid introducing generated files, build artifacts, or local environment files.

## Markdown conventions

- Use one `#` heading per page.
- Increase headings one level at a time without skipping levels.
- Use fenced code blocks for commands, configuration, manifests, and logs.
- Specify a language for fenced code blocks where appropriate, such as `bash`, `yaml`, `json`, `text`, or `mermaid`.
- Use relative links for internal documentation references.
- Keep tables readable in source form.
- Add alt text for images.
- Use Mermaid only inside fenced `mermaid` blocks.

## Commit message conventions

Use concise, imperative commit messages that describe the documentation change.

Preferred examples:

- `Add documentation engineering workflow`
- `docs(kubernetes): add API server section`
- `docs(networking): update load balancing navigation`
- `ci: add MkDocs pull request checks`

Avoid vague messages such as `updates`, `fix docs`, or `changes`.

## Pull request workflow

1. Create a feature branch from `main`.
2. Make only the requested documentation or infrastructure changes.
3. Run the relevant checks locally when available.
4. Confirm MkDocs navigation includes new pages.
5. Confirm links, headings, code blocks, and image references are valid.
6. Open a pull request with a clear summary and validation notes.
7. Wait for required checks to pass before merging.

## Author-content protection rules

- Never rewrite author content unless explicitly instructed.
- Never change technical meaning to satisfy linting or style tools.
- Formatting-only changes must preserve terminology, examples, sequence, and emphasis.
- If linting requires a change that could alter meaning, leave the content unchanged and document the concern in the pull request.
- When integrating a supplied manuscript, insert it exactly as supplied unless a build or formatting issue prevents publication.
