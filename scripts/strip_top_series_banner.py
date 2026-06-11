#!/usr/bin/env python3
"""Strip the top-of-post Series blockquote banner from EN/PT posts.

Targets only this exact one-line pattern (and the blank line after it):

    > **Series: X** | **Part N of M** > _description_
    > **Série: X** | **Parte N de M** > _description_
    > **Series: X** | **Introduction** > _description_
    > **Series: X** | **Part N of M** | _description_   # | separator variant

Refuses to touch anything else. Conservative by design.

Usage:
    scripts/strip_top_series_banner.py            # dry-run (default)
    scripts/strip_top_series_banner.py --apply    # write changes
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Anchored regex — must start at column 0, must be exactly one blockquote line.
# - "Series" (EN) or "Série" (PT)
# - position label: "Part N of M", "Parte N de M", or "Introduction"
# - the position label is followed by " | " or " > " then the italic description
BANNER_RE = re.compile(
    r"^> \*\*(Series|Série): [^*]+\*\* \| "
    r"\*\*(Part(?: Part)? \d+ of \d+|Parte \d+ de \d+|Introduction|Introdução)\*\*"
    r" [|>] _[^_]+_$"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
POST_DIRS = [REPO_ROOT / "content/en/posts", REPO_ROOT / "content/pt/posts"]


def find_banner(lines: list[str]) -> int | None:
    """Return the line index of the banner if it matches uniquely, else None.

    Banner must appear in the first 60 lines (after frontmatter & maybe one image).
    Refuses to act if more than one match exists in the file.
    """
    matches = [i for i, line in enumerate(lines[:60]) if BANNER_RE.match(line.rstrip("\n"))]
    if len(matches) != 1:
        return None
    return matches[0]


def strip_banner(lines: list[str], idx: int) -> list[str]:
    """Remove the banner line and one trailing blank line if present."""
    new_lines = lines[:idx]
    after = lines[idx + 1 :]
    # If the next line is blank, drop it too (it was paired with the banner).
    if after and after[0].strip() == "":
        after = after[1:]
    return new_lines + after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rewrite files. Default is dry-run.",
    )
    parser.add_argument(
        "--show-line",
        action="store_true",
        help="Print the matched line for each affected file.",
    )
    args = parser.parse_args()

    affected: list[tuple[Path, int, str]] = []
    skipped_multiple: list[Path] = []

    for posts_dir in POST_DIRS:
        if not posts_dir.exists():
            continue
        for path in sorted(posts_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines(keepends=True)
            idx = find_banner(lines)
            if idx is None:
                # Check whether it skipped due to multiple matches
                all_matches = [
                    i for i, line in enumerate(lines[:60])
                    if BANNER_RE.match(line.rstrip("\n"))
                ]
                if len(all_matches) > 1:
                    skipped_multiple.append(path)
                continue
            line = lines[idx].rstrip("\n")
            affected.append((path, idx + 1, line))

    if args.show_line or not args.apply:
        for path, lineno, line in affected:
            rel = path.relative_to(REPO_ROOT)
            print(f"  {rel}:{lineno}")
            if args.show_line:
                print(f"    {line}")

    if skipped_multiple:
        print(f"\nWARNING: {len(skipped_multiple)} file(s) had multiple matches and were skipped:")
        for p in skipped_multiple:
            print(f"  {p.relative_to(REPO_ROOT)}")

    print(f"\nMatched {len(affected)} file(s).")

    if not args.apply:
        print("DRY-RUN — no files written. Re-run with --apply to write.")
        return 0

    for path, _, _ in affected:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        idx = find_banner(lines)
        if idx is None:
            # Safety: if state changed between scan and write, skip.
            continue
        new_lines = strip_banner(lines, idx)
        path.write_text("".join(new_lines), encoding="utf-8")
        print(f"  wrote {path.relative_to(REPO_ROOT)}")

    print(f"\nWrote {len(affected)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
