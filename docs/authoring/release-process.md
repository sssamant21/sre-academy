# Release Process

This guide explains how to publish a completed SRE Academy chapter section with the release automation scripts.

## Release workflow

1. Save the approved manuscript as a Markdown file outside the target documentation directory.
2. Run `scripts/release_section.py` with the source file, chapter number, section number, title, and commit message.
3. Review the generated destination path and MkDocs navigation update.
4. Confirm the script validation summary reports success.
5. Run `scripts/open_pr.sh` to create the branch, commit the changes, push the branch, and open the pull request.
6. Wait for the pull request documentation checks to pass before merging.

## Script usage

Use `release_section.py` to copy a manuscript into the documentation tree and validate the site.

```bash
python scripts/release_section.py \
  --source manuscripts/chapter-07/7.1-introduction.md \
  --chapter 7 \
  --section 7.1 \
  --title "Introduction to the Kubernetes API Server" \
  --commit "Add Chapter 7 Section 7.1: Introduction to the Kubernetes API Server"
```

The script performs these actions:

- Verifies that the source Markdown file exists.
- Creates the destination chapter directory when needed.
- Copies the manuscript to `docs/chapter-XX/`.
- Updates `mkdocs.yml` without adding duplicate navigation entries.
- Validates heading hierarchy and fenced code blocks.
- Runs `markdownlint` when it is installed.
- Runs Vale when `.vale.ini` is configured and the `vale` command is installed.
- Builds the site with `mkdocs build --strict`.
- Prints a release summary.

Use `open_pr.sh` after the release script succeeds.

```bash
scripts/open_pr.sh \
  --branch feature/chapter-07-section-7-1 \
  --commit "Add Chapter 7 Section 7.1: Introduction to the Kubernetes API Server" \
  --title "Chapter 7: Add Section 7.1 - Introduction to the Kubernetes API Server" \
  --body "Adds Chapter 7 Section 7.1, updates MkDocs navigation, and confirms the documentation build passes."
```

The script uses `git` for branch, commit, and push operations. If the GitHub CLI is installed, it opens the pull request automatically.

## Expected directory structure

Released section manuscripts are copied into chapter-specific directories under `docs/`.

```text
docs/
  chapter-07/
    7.1-introduction-to-the-kubernetes-api-server.md
  authoring/
    release-process.md
scripts/
  release_section.py
  open_pr.sh
mkdocs.yml
```

The destination filename is created from the section number and a slugified section title.

## Troubleshooting

### Source file is missing

Confirm the path passed to `--source` exists and points to a Markdown file.

### Markdown validation fails

Check the reported line number. Common causes include multiple H1 headings, skipped heading levels, unclosed fenced code blocks, or fenced code blocks without a language.

### Markdownlint is skipped

Install `markdownlint-cli` if local linting is required.

```bash
npm install --global markdownlint-cli
```

### Vale is skipped

Install Vale if local style checks are required.

```bash
vale docs
```

### MkDocs build fails

Install the documentation dependencies and rerun the release script.

```bash
pip install -r requirements.txt
python scripts/release_section.py --help
```

### Pull request is not opened automatically

Install and authenticate the GitHub CLI, then rerun `scripts/open_pr.sh` or open the pull request from the pushed branch in GitHub.

```bash
gh auth login
```
