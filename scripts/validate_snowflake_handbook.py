#!/usr/bin/env python3
"""Validate structural integrity of the Snowflake Enterprise Handbook."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "docs" / "books" / "snowflake"
CHAPTER_RE = re.compile(r"chapter-(\d{2})$")
SECTION_RE = re.compile(r"^##\s+(\d+)\.(\d+)\s+(.+)$", re.MULTILINE)
LINK_RE = re.compile(r"https://docs\.snowflake\.com/")
CONTROL = "> **Document control**"


def validate_chapter(path: Path) -> list[str]:
    errors: list[str] = []
    chapter_match = CHAPTER_RE.match(path.parent.name)
    if not chapter_match:
        return [f"{path}: cannot infer chapter number"]

    chapter = int(chapter_match.group(1))
    text = path.read_text(encoding="utf-8")

    if CONTROL not in text:
        errors.append(f"{path}: missing document-control block")
    if not LINK_RE.search(text):
        errors.append(f"{path}: missing official Snowflake documentation link")
    if text.count(chr(96) * 3) % 2:
        errors.append(f"{path}: unbalanced fenced code block")

    sections = [
        int(minor)
        for major, minor, _ in SECTION_RE.findall(text)
        if int(major) == chapter
    ]
    duplicates = sorted({number for number in sections if sections.count(number) > 1})
    if duplicates:
        errors.append(f"{path}: duplicate top-level sections {duplicates}")

    if sections:
        expected = set(range(min(sections), max(sections) + 1))
        missing = sorted(expected.difference(sections))
        if missing:
            errors.append(f"{path}: missing top-level sections {missing}")

    return errors


def main() -> int:
    errors: list[str] = []
    chapters = sorted(BOOK.glob("chapter-*/README.md"))
    if len(chapters) != 20:
        errors.append(f"expected 20 chapters; found {len(chapters)}")

    for chapter in chapters:
        errors.extend(validate_chapter(chapter))

    required = [BOOK / "index.md", BOOK / "summary.md", BOOK / "content-ownership.md"]
    for document in required:
        if not document.exists():
            errors.append(f"missing required document: {document}")

    if errors:
        print("Snowflake handbook validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Snowflake handbook validation passed for {len(chapters)} chapters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
