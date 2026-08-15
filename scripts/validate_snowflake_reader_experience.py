#!/usr/bin/env python3
"""Validate reader-facing Snowflake handbook Markdown beyond chapter structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path("docs/books/snowflake")
MARKER_RE = re.compile(r"\b(?:TODO|TBD|FIXME)\b", re.IGNORECASE)
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*```", re.MULTILINE)
H1_RE = re.compile(r"^#\s+\S", re.MULTILINE)
REQUIRED_METADATA = ("Version:", "Status:")
V11_DIRS = (ROOT / "labs", ROOT / "runbooks")


def relative_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split()[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    return (source.parent / target).resolve()


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    if text.startswith("\ufeff"):
        errors.append("contains a UTF-8 byte-order mark")
    if MARKER_RE.search(text):
        errors.append("contains TODO/TBD/FIXME marker")
    if len(FENCE_RE.findall(text)) % 2:
        errors.append("has unbalanced fenced code blocks")
    if len(H1_RE.findall(text)) != 1:
        errors.append("must contain exactly one H1 heading")

    for raw_target in LINK_RE.findall(text):
        target = relative_target(path, raw_target)
        if target is not None and not target.exists():
            errors.append(f"broken relative link: {raw_target}")

    if any(directory in path.parents for directory in V11_DIRS):
        for field in REQUIRED_METADATA:
            if field not in text:
                errors.append(f"missing required metadata field: {field}")
        if path.name != "index.md" and "standard" not in path.stem:
            if "Official references" not in text and path.parent.name != "templates":
                errors.append("missing Official references section")

    return errors


def main() -> int:
    if not ROOT.is_dir():
        print(f"Missing handbook directory: {ROOT}", file=sys.stderr)
        return 1

    failures: list[str] = []
    markdown_files = sorted(ROOT.rglob("*.md"))
    for path in markdown_files:
        for error in validate_file(path):
            failures.append(f"{path}: {error}")

    if failures:
        print("Snowflake reader-experience validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(markdown_files)} Snowflake Markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
