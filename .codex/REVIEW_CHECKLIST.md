# Documentation Review Checklist

Use this checklist before requesting review or merging documentation changes.

## Content scope

- [ ] The change matches the requested scope.
- [ ] Existing chapter content was not rewritten unless explicitly requested.
- [ ] Technical meaning is preserved for any formatting-only edits.

## Markdown validity

- [ ] Markdown renders correctly in MkDocs.
- [ ] Lists, tables, admonitions, and blockquotes are well formed.
- [ ] Files end with a single trailing newline.

## Heading hierarchy

- [ ] Each page has one top-level `#` heading.
- [ ] Headings increase one level at a time.
- [ ] Section titles are clear and consistent with nearby pages.

## Links and references

- [ ] Internal links resolve correctly.
- [ ] Relative links point to the intended pages.
- [ ] External links are current where verification is required.
- [ ] Image references resolve and include useful alt text.

## Code and diagrams

- [ ] Fenced code blocks specify a language where appropriate.
- [ ] Shell commands use `bash` unless another shell is required.
- [ ] Configuration examples use the correct language, such as `yaml`, `json`, or `toml`.
- [ ] Mermaid diagrams use fenced `mermaid` blocks.
- [ ] Mermaid syntax is valid and readable.

## MkDocs navigation

- [ ] New pages are added to `mkdocs.yml` when they should appear in navigation.
- [ ] Moved pages have updated navigation entries.
- [ ] Navigation labels match the handbook structure.
- [ ] No orphaned pages were introduced unintentionally.

## Quality checks

- [ ] `mkdocs build --strict` passes.
- [ ] Markdown linting passes or documented exceptions are intentional.
- [ ] Vale style checks pass or documented exceptions are intentional.
- [ ] Spelling is reviewed where appropriate for prose changes.

## Pull request readiness

- [ ] The pull request summary explains what changed.
- [ ] Validation steps are listed in the pull request.
- [ ] Any known limitations or follow-up work are documented.
