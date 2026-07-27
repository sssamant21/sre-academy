# SRE Academy

Documentation and learning materials for SRE Academy.

## Documentation site

This repository uses [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for the documentation site.

### Preview locally

```bash
pip install -r requirements.txt
mkdocs serve
```

### Build locally

```bash
mkdocs build --strict
```

### Quality checks

Pull requests run these documentation checks before the site build:

- Markdown linting with `markdownlint-cli2`.
- Link checking with `lychee`.
- Strict MkDocs builds with `mkdocs build --strict`.

### Publish

GitHub Actions builds the site on pull requests and deploys it to GitHub Pages when changes are merged to `main`.
