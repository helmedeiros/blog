#!/usr/bin/env python3
"""
Strip the legacy "Series Navigation" trailing block from migrated posts.

Posts have already been migrated to the front-matter `series:` convention,
so the new card widget renders from layouts. This script removes the
hand-written markdown block that the WordPress migration left behind.

Block to remove:
  [optional leading `---` HR + blanks]
  Series Navigation heading (### **...**, **...:**, or **Custom Series Navigation:**)
  blank line
  bulleted list (lines starting with `-` or indented continuations)
  [optional trailing `**This series documents...**` paragraph]
  [optional trailing `**Complete series**: [...]` line]

Anything *after* the block (e.g. a closing "Stay tuned." line) is preserved.

Run with --check to preview without modifying.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TARGETS = list((REPO / "content").rglob("*.md"))

SERIES_META_PARA = re.compile(r"^\*\*This series\b", re.I)
COMPLETE_SERIES_LINE = re.compile(r"^\*\*Complete series\*\*:", re.I)

def find_block(lines: list[str]) -> tuple[int, int] | None:
    """Return (start, end_exclusive) of the widget block, or None."""
    # Find last "Series Navigation" line.
    nav_idx = None
    for i, line in enumerate(lines):
        if "Series Navigation" in line:
            nav_idx = i
    if nav_idx is None:
        return None

    # Walk backward to include optional leading blank lines and `---` HR.
    start = nav_idx
    # Skip blank lines immediately before heading.
    while start > 0 and lines[start - 1].strip() == "":
        start -= 1
    # If the line before that is `---`, include it (with its preceding blanks).
    if start > 0 and lines[start - 1].strip() == "---":
        start -= 1
        while start > 0 and lines[start - 1].strip() == "":
            start -= 1

    # Walk forward through heading + blank + bulleted list.
    j = nav_idx + 1
    # Skip blank line(s) right after heading.
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    # Consume bullet list.
    while j < len(lines):
        s = lines[j].lstrip()
        if s.startswith("- ") or s.startswith("* ") or lines[j].startswith("  "):
            j += 1
        else:
            break
    # Optional trailing series-meta paragraph(s).
    while j < len(lines):
        # Skip a single blank line then check.
        k = j
        while k < len(lines) and lines[k].strip() == "":
            k += 1
        if k >= len(lines):
            j = k
            break
        if SERIES_META_PARA.match(lines[k]) or COMPLETE_SERIES_LINE.match(lines[k]):
            # Consume this paragraph (until next blank line or EOF).
            j = k + 1
            while j < len(lines) and lines[j].strip() != "":
                j += 1
        else:
            break

    return (start, j)

def process(path: Path, check: bool) -> str:
    text = path.read_text()
    if "Series Navigation" not in text:
        return "skip"

    lines = text.splitlines(keepends=True)
    block = find_block(lines)
    if block is None:
        return "skip"
    start, end = block

    head = lines[:start]
    tail = lines[end:]

    # Drop trailing blank lines from head (so we don't leave dangling whitespace).
    while head and head[-1].strip() == "":
        head.pop()

    # If tail has only blank lines, drop it entirely.
    if all(l.strip() == "" for l in tail):
        tail = []
    else:
        # Trim leading blanks then ensure exactly one blank line between head and tail.
        while tail and tail[0].strip() == "":
            tail.pop(0)
        head.append("\n")

    new_text = "".join(head + tail).rstrip() + "\n"

    if check:
        removed = "".join(lines[start:end]).rstrip()
        kept_after = "".join(tail).rstrip()
        msg = f"WOULD-STRIP {path}\n--- removing ---\n{removed}\n----------------"
        if kept_after:
            msg += f"\n--- keeping after ---\n{kept_after}\n---------------------"
        return msg
    else:
        path.write_text(new_text)
        return f"stripped: {path}"

def main():
    check = "--check" in sys.argv
    stripped = 0
    skipped = 0
    for p in sorted(TARGETS):
        result = process(p, check)
        if result == "skip":
            skipped += 1
        else:
            stripped += 1
            print(result)
    print(f"\nProcessed: stripped={stripped} skipped={skipped}")

if __name__ == "__main__":
    sys.exit(main())
