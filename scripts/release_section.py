#!/usr/bin/env python3
"""Release a completed manuscript section into the SRE Academy docs site."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
MKDOCS_FILE = ROOT / "mkdocs.yml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy a manuscript section into docs, update MkDocs nav, and run documentation checks."
    )
    parser.add_argument("--source", required=True, help="Source Markdown manuscript file.")
    parser.add_argument("--chapter", required=True, help="Chapter number, such as 7 or 07.")
    parser.add_argument("--section", required=True, help="Section number, such as 7.1.")
    parser.add_argument("--title", required=True, help="Section title for the destination filename and navigation label.")
    parser.add_argument("--commit", required=True, help="Commit message to pass to scripts/open_pr.sh.")
    return parser.parse_args()


def chapter_dir_name(chapter: str) -> str:
    chapter_number = int(chapter)
    return f"chapter-{chapter_number:02d}"


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-") or "section"


def destination_path(chapter: str, section: str, title: str) -> Path:
    directory = DOCS_DIR / chapter_dir_name(chapter)
    filename = f"{section}-{slugify(title)}.md"
    return directory / filename


def validate_markdown(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    h1_count = 0
    previous_level = 0
    in_fence = False
    fence_start = 0
    mermaid_has_content = False
    current_fence_language = ""

    for line_number, line in enumerate(lines, start=1):
        fence_match = re.match(r"^```(\S*)", line)
        if fence_match:
            if not in_fence:
                in_fence = True
                fence_start = line_number
                current_fence_language = fence_match.group(1)
                mermaid_has_content = False
                if not current_fence_language:
                    errors.append(f"{path}: line {line_number}: fenced code block is missing a language")
            else:
                if current_fence_language == "mermaid" and not mermaid_has_content:
                    errors.append(f"{path}: line {fence_start}: Mermaid block is empty")
                in_fence = False
                current_fence_language = ""
            continue

        if in_fence:
            if current_fence_language == "mermaid" and line.strip():
                mermaid_has_content = True
            continue

        heading_match = re.match(r"^(#{1,6})\s+", line)
        if not heading_match:
            continue

        level = len(heading_match.group(1))
        if level == 1:
            h1_count += 1
        if previous_level and level > previous_level + 1:
            errors.append(
                f"{path}: line {line_number}: heading jumps from H{previous_level} to H{level}"
            )
        previous_level = level

    if in_fence:
        errors.append(f"{path}: line {fence_start}: fenced code block is not closed")
    if h1_count != 1:
        errors.append(f"{path}: expected exactly one H1 heading, found {h1_count}")

    return errors


def run_command(command: list[str], *, required: bool = True) -> bool:
    executable = command[0]
    if shutil.which(executable) is None and executable not in {sys.executable}:
        print(f"Skipping {' '.join(command)} because {executable} is not installed.")
        return True

    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT, text=True)
    if result.returncode != 0:
        if required:
            print(f"Command failed with exit code {result.returncode}: {' '.join(command)}")
            return False
        print(f"Optional command failed with exit code {result.returncode}: {' '.join(command)}")
    return True


def mkdocs_build() -> bool:
    if shutil.which("mkdocs"):
        return run_command(["mkdocs", "build", "--strict"])
    return run_command([sys.executable, "-m", "mkdocs", "build", "--strict"])


def update_mkdocs_nav(chapter: str, section: str, title: str, doc_path: Path) -> bool:
    if not MKDOCS_FILE.exists():
        raise FileNotFoundError("mkdocs.yml was not found")

    nav_path = doc_path.relative_to(DOCS_DIR).as_posix()
    label = f"{section}. {title}"
    chapter_number = int(chapter)
    chapter_label = f"{chapter_number}."
    overview_label = f'"{chapter_number}. '

    text = MKDOCS_FILE.read_text(encoding="utf-8")
    if nav_path in text:
        print(f"MkDocs navigation already contains {nav_path}; no duplicate entry added.")
        return False

    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith(f"- {overview_label}") and not stripped.startswith(f"- '{chapter_number}. "):
            continue
        if ":" not in stripped or ".md" not in stripped:
            continue

        indent = len(line) - len(line.lstrip(" "))
        marker, existing_path = line.split(":", 1)
        chapter_title = marker.strip()[2:].strip()
        existing_path = existing_path.strip()
        replacement = [
            " " * indent + f"- {chapter_title}:",
            " " * (indent + 4) + f"- Overview: {existing_path}",
            " " * (indent + 4) + f'"{label}": {nav_path}',
        ]
        lines[index:index + 1] = replacement
        MKDOCS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Updated MkDocs navigation under Chapter {chapter_number}.")
        return True

    chapter_nav = [
        "  - Released Sections:",
        f"      - Chapter {chapter_number}:",
        f'          - "{label}": {nav_path}',
    ]
    insert_at = next(
        (i for i, line in enumerate(lines) if line.startswith("markdown_extensions:")),
        len(lines),
    )
    lines[insert_at:insert_at] = [""] + chapter_nav
    MKDOCS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Added Released Sections navigation for Chapter {chapter_number}.")
    return True


def main() -> int:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        print(f"Source Markdown file does not exist: {source}", file=sys.stderr)
        return 1
    if source.suffix.lower() != ".md":
        print(f"Source file must be Markdown: {source}", file=sys.stderr)
        return 1

    target = destination_path(args.chapter, args.section, args.title)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    print(f"Copied {source} to {target.relative_to(ROOT)}")

    nav_changed = update_mkdocs_nav(args.chapter, args.section, args.title, target)

    markdown_errors = validate_markdown(target)
    if markdown_errors:
        print("Markdown validation failed:", file=sys.stderr)
        for error in markdown_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    checks: list[tuple[str, bool]] = []
    checks.append(("markdown validation", True))
    checks.append(("markdownlint", run_command(["markdownlint", str(target.relative_to(ROOT))])))
    if (ROOT / ".vale.ini").exists():
        checks.append(("vale", run_command(["vale", str(target.relative_to(ROOT))])))
    checks.append(("mkdocs build", mkdocs_build()))

    failed = [name for name, ok in checks if not ok]
    if failed:
        print("Validation failed: " + ", ".join(failed), file=sys.stderr)
        return 1

    print("\nRelease section summary")
    print(f"- Source: {source}")
    print(f"- Destination: {target.relative_to(ROOT)}")
    print(f"- MkDocs navigation updated: {'yes' if nav_changed else 'already present'}")
    print(f"- Commit message: {args.commit}")
    print("- Validation: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
