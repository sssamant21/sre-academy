#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/open_pr.sh --branch <branch-name> --commit <commit-message> --title <pr-title> [--body <pr-body>]

Creates the feature branch when needed, commits staged and unstaged changes, pushes the branch,
and opens a GitHub pull request with the GitHub CLI when gh is installed.
USAGE
}

BRANCH=""
COMMIT_MESSAGE=""
PR_TITLE=""
PR_BODY=""
BASE_BRANCH="main"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --branch)
      BRANCH="${2:-}"
      shift 2
      ;;
    --commit)
      COMMIT_MESSAGE="${2:-}"
      shift 2
      ;;
    --title)
      PR_TITLE="${2:-}"
      shift 2
      ;;
    --body)
      PR_BODY="${2:-}"
      shift 2
      ;;
    --base)
      BASE_BRANCH="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$BRANCH" || -z "$COMMIT_MESSAGE" || -z "$PR_TITLE" ]]; then
  echo "Missing required arguments." >&2
  usage >&2
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo "git is required to create a branch, commit, and push changes." >&2
  exit 1
fi

CURRENT_BRANCH="$(git branch --show-current)"
if [[ "$CURRENT_BRANCH" != "$BRANCH" ]]; then
  if git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
    git checkout "$BRANCH"
  else
    git checkout -b "$BRANCH"
  fi
fi

git add docs mkdocs.yml scripts

if git diff --cached --quiet; then
  echo "No staged changes to commit."
else
  git commit -m "$COMMIT_MESSAGE"
fi

git push --set-upstream origin "$BRANCH"

if command -v gh >/dev/null 2>&1; then
  if gh pr view "$BRANCH" >/dev/null 2>&1; then
    echo "Pull request already exists for $BRANCH."
  else
    if [[ -n "$PR_BODY" ]]; then
      gh pr create --base "$BASE_BRANCH" --head "$BRANCH" --title "$PR_TITLE" --body "$PR_BODY"
    else
      gh pr create --base "$BASE_BRANCH" --head "$BRANCH" --title "$PR_TITLE" --fill
    fi
  fi
else
  echo "gh is not installed; pushed branch $BRANCH but did not open a pull request."
  echo "Open a pull request manually from: https://github.com/sssamant21/sre-academy/pull/new/$BRANCH"
fi
