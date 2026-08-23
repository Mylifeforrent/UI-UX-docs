#!/usr/bin/env python3
"""Validate local Markdown links, anchors, and empty Markdown files."""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!\!)\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+)(?:\s+[^)]*)?)\)")
HEADING = re.compile(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```+|~~~+)")


def github_slug(text: str) -> str:
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = unicodedata.normalize("NFKC", text).strip().lower()
    text = re.sub(r"[^\w\u0080-\uffff -]", "", text)
    return re.sub(r"\s+", "-", text)


def document_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING.match(line)
        if not match:
            continue
        base = github_slug(match.group(1))
        index = counts.get(base, 0)
        counts[base] = index + 1
        anchors.add(base if index == 0 else f"{base}-{index}")
    return anchors


def iter_markdown() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".zcode" not in path.parts)


def main() -> int:
    errors: list[str] = []
    documents = iter_markdown()
    anchor_cache = {path: document_anchors(path) for path in documents}

    for source in documents:
        if source.stat().st_size == 0:
            errors.append(f"EMPTY {source.relative_to(ROOT)}")

        in_fence = False
        for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            for match in MARKDOWN_LINK.finditer(line):
                target = (match.group(1) or match.group(2) or "").strip()
                if not target:
                    errors.append(f"EMPTY_LINK {source.relative_to(ROOT)}:{line_number}")
                    continue
                parsed = urlparse(target)
                if parsed.scheme or target.startswith("//"):
                    continue

                raw_path = unquote(parsed.path)
                fragment = unquote(parsed.fragment)
                destination = (source.parent / raw_path).resolve() if raw_path else source
                try:
                    destination.relative_to(ROOT.resolve())
                except ValueError:
                    errors.append(f"OUTSIDE_ROOT {source.relative_to(ROOT)}:{line_number} -> {target}")
                    continue
                if not destination.is_file():
                    errors.append(f"MISSING {source.relative_to(ROOT)}:{line_number} -> {target}")
                    continue
                if destination.suffix.lower() == ".md" and destination.stat().st_size == 0:
                    errors.append(f"EMPTY_TARGET {source.relative_to(ROOT)}:{line_number} -> {target}")
                if fragment and destination in anchor_cache and fragment not in anchor_cache[destination]:
                    errors.append(f"MISSING_ANCHOR {source.relative_to(ROOT)}:{line_number} -> {target}")

    if errors:
        print("\n".join(errors))
        print(f"\nDocumentation check failed: {len(errors)} issue(s).", file=sys.stderr)
        return 1

    print(f"Documentation check passed: {len(documents)} Markdown files, local links and anchors verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
