#!/usr/bin/env python3
"""Strip leftover manual series navigation from EN/PT posts.

Two patterns are handled, both conservative:

1. Top-of-post blockquote banner (one line + the blank after):
    > **Series: X** | **Part N of M** > _description_
    > **Série: X** | **Parte N de M** > _description_
    > **Series: X** | **Introduction** > _description_

2. Bottom "Navegação da Série" block:
    [optional ---]
    [blank]
    **Navegação da Série [name]:**                  # bold paragraph variant
    OR ### **Navegação da Série**                   # h3 variant
    [blank]
    - **Atual**: ...
    - **Anterior**: ...
    - **Próxim[oa]**: ...
    - **Parte N**: ...
    - **Série completa**: ...
    - **Final**: ...
    - **Introdução**: ...

   Block ends at the first non-blank line that isn't one of the recognised
   bullets — so trailing ref-link defs like `[1]: /uploads/...` are kept.

Refuses to touch anything else. Idempotent.

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

NAV_HEADER_RE = re.compile(
    r"^(?:###\s+)?\*\*Navegação da Série[^*\n]*\*\*:?\s*$"
)

NAV_BULLET_RE = re.compile(
    r"^- \*\*("
    r"Atual|Anterior|Próxim[oa]|Pr[oó]ximo|Parte \d+|"
    r"Série completa|Final|Introdução"
    r")\*\*"
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


def has_series_taxonomy(text: str) -> bool:
    """True if the post's frontmatter declares a `series:` field.

    Only inspects the YAML frontmatter (between the first two `---` lines) so
    body matches like "## Série" don't fool us.
    """
    if not text.startswith("---"):
        return False
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return False
    fm_body = parts[0]
    return any(
        line.startswith("series:") or line.startswith("series :")
        for line in fm_body.splitlines()
    )


def find_nav_block(lines: list[str]) -> tuple[int, int] | None:
    """Locate the bottom Navegação da Série block.

    Returns (start_idx, end_idx) where lines[start_idx:end_idx] is the segment
    to remove (inclusive of leading separator/blank lines and trailing blank).
    Returns None if no unique header is found or if the bullets don't look right.
    """
    headers = [
        i for i, line in enumerate(lines)
        if NAV_HEADER_RE.match(line.rstrip("\n"))
    ]
    if len(headers) != 1:
        return None
    h = headers[0]

    # Walk forward: blank lines + recognised bullets only.
    e = h + 1
    saw_bullet = False
    while e < len(lines):
        stripped = lines[e].rstrip("\n").strip()
        if stripped == "":
            e += 1
            continue
        if NAV_BULLET_RE.match(lines[e].rstrip("\n")):
            saw_bullet = True
            e += 1
            continue
        break
    if not saw_bullet:
        return None  # header alone — refuse to touch

    # Walk backward from the header: skip blanks, then optional --- separator,
    # then more blanks above it. This collapses the visual divider too.
    s = h
    while s > 0 and lines[s - 1].rstrip("\n").strip() == "":
        s -= 1
    if s > 0 and lines[s - 1].rstrip("\n").strip() == "---":
        s -= 1
        while s > 0 and lines[s - 1].rstrip("\n").strip() == "":
            s -= 1

    return s, e


def strip_nav_block(lines: list[str], span: tuple[int, int]) -> list[str]:
    s, e = span
    return lines[:s] + lines[e:]


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

    # (path, kind, descriptor)
    affected: list[tuple[Path, str, str]] = []
    skipped_multiple: list[Path] = []
    skipped_no_taxonomy: list[Path] = []

    for posts_dir in POST_DIRS:
        if not posts_dir.exists():
            continue
        for path in sorted(posts_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines(keepends=True)

            idx = find_banner(lines)
            if idx is not None:
                affected.append(
                    (path, "banner", f"line {idx + 1}: {lines[idx].rstrip()}")
                )
            else:
                all_matches = [
                    i for i, line in enumerate(lines[:60])
                    if BANNER_RE.match(line.rstrip("\n"))
                ]
                if len(all_matches) > 1:
                    skipped_multiple.append(path)

            span = find_nav_block(lines)
            if span is not None:
                # Safety guard: refuse to strip the manual nav block if the post
                # doesn't have the Hugo `series:` taxonomy — doing so would leave
                # the page with no series navigation at all.
                if not has_series_taxonomy(text):
                    skipped_no_taxonomy.append(path)
                else:
                    s, e = span
                    affected.append(
                        (path, "navblock", f"lines {s + 1}–{e} ({e - s} lines)")
                    )

    if args.show_line or not args.apply:
        for path, kind, desc in affected:
            rel = path.relative_to(REPO_ROOT)
            print(f"  [{kind:8s}] {rel}")
            if args.show_line:
                print(f"    {desc}")

    if skipped_multiple:
        print(f"\nWARNING: {len(skipped_multiple)} file(s) had multiple top-banner matches and were skipped:")
        for p in skipped_multiple:
            print(f"  {p.relative_to(REPO_ROOT)}")

    if skipped_no_taxonomy:
        print(
            f"\nWARNING: {len(skipped_no_taxonomy)} file(s) had a Navegação block but no Hugo "
            f"`series:` taxonomy — stripping would leave them with NO series navigation. Skipped:"
        )
        for p in skipped_no_taxonomy:
            print(f"  {p.relative_to(REPO_ROOT)}")

    by_kind: dict[str, int] = {}
    files_touched = {a[0] for a in affected}
    for _, kind, _ in affected:
        by_kind[kind] = by_kind.get(kind, 0) + 1
    print(f"\nMatched {len(affected)} edit(s) across {len(files_touched)} file(s): {by_kind}")

    if not args.apply:
        print("DRY-RUN — no files written. Re-run with --apply to write.")
        return 0

    written = 0
    for path in sorted(files_touched, key=lambda p: str(p)):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)

        # Apply nav block first (it's near EOF, so indices are stable
        # even if we later touch the top banner).
        span = find_nav_block(lines)
        if span is not None:
            lines = strip_nav_block(lines, span)

        idx = find_banner(lines)
        if idx is not None:
            lines = strip_banner(lines, idx)

        path.write_text("".join(lines), encoding="utf-8")
        written += 1
        print(f"  wrote {path.relative_to(REPO_ROOT)}")

    print(f"\nWrote {written} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
