#!/usr/bin/env python3
"""Fix the WordPress migration `[<img.../>][N]` markup that Hugo renders broken.

The legacy WordPress markup wraps an HTML `<img>` tag inside a markdown
reference-link `[link-text][N]`. Hugo's markdown engine doesn't render this
correctly — the `[` and `]` leak through as visible characters.

Two patterns are handled:

  1. Bare:        `[<img src="X" alt="Y" .../>][N]`
                  → `![Y](X)`

  2. WP figure:   `<figure ...>[<img.../>][N] <figcaption>caption</figcaption></figure>`
                  → `![Y](X)`  + italic caption line if non-empty

Stray reference definitions (`[N]: …`) are left alone — they are harmless
dangling references in markdown.

Usage:
    scripts/fix_broken_wp_images.py            # dry-run (default)
    scripts/fix_broken_wp_images.py --apply    # write changes
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POST_DIRS = [REPO_ROOT / "content/en/posts", REPO_ROOT / "content/pt/posts"]

# Order matters: figure-wrapped first so we don't double-replace.
# Capture optional leading whitespace on the same line so we de-indent it.
FIGURE_RE = re.compile(
    r"[ \t]*<figure[^>]*>\s*\[<img\s[^>]*?/>\]\[\d+\]\s*"
    r"(?:<figcaption[^>]*>(?P<cap>.*?)</figcaption>)?\s*</figure>[ \t]*",
    re.DOTALL,
)

# Capture optional leading whitespace too — WP markup often has 1-2 spaces
# of indent that would prevent goldmark from parsing the result as markdown.
BARE_RE = re.compile(r"[ \t]*\[(<img\s[^>]*?/>)\]\[\d+\][ \t]*", re.DOTALL)

IMG_TAG_RE = re.compile(r"<img\s[^>]*?/>", re.DOTALL)
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


def get_attr(img_tag: str, name: str) -> str:
    for k, v in ATTR_RE.findall(img_tag):
        if k.lower() == name.lower():
            return v
    return ""


def replace_figure(match: re.Match[str]) -> str:
    block = match.group(0)
    img_match = IMG_TAG_RE.search(block)
    if img_match is None:
        return block  # safety: leave untouched
    img_tag = img_match.group(0)
    src = get_attr(img_tag, "src")
    alt = get_attr(img_tag, "alt").strip()
    cap = (match.group("cap") or "").strip()
    if not src:
        return block

    md = f"![{alt}]({src})"
    if cap and cap != alt:
        md += f"\n*{cap}*"
    return md


def replace_bare(match: re.Match[str]) -> str:
    img_tag = match.group(1)
    src = get_attr(img_tag, "src")
    alt = get_attr(img_tag, "alt").strip()
    if not src:
        return match.group(0)
    return f"![{alt}]({src})"


def ensure_blank_lines_around(text: str) -> str:
    """For each `![alt](src)` line, ensure a blank line before and after.

    Goldmark won't parse a markdown image as such if it abuts an HTML block
    on either side. Inserting blank lines forces it to be its own paragraph.
    """
    out_lines: list[str] = []
    lines = text.splitlines(keepends=True)
    md_image_re = re.compile(r"^!\[[^\]]*\]\([^)]+\)\s*$")
    for i, line in enumerate(lines):
        if md_image_re.match(line):
            # blank line before — unless start of file or previous line already blank
            if out_lines and out_lines[-1].rstrip("\n") != "":
                out_lines.append("\n")
            out_lines.append(line if line.endswith("\n") else line + "\n")
            # blank line after — unless next is blank or EOF
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if nxt.rstrip("\n") != "":
                out_lines.append("\n")
        else:
            out_lines.append(line)
    return "".join(out_lines)


def fix_text(text: str) -> tuple[str, int, int]:
    """Apply both patterns. Returns (new_text, n_figure, n_bare)."""
    new_text, n_fig = FIGURE_RE.subn(replace_figure, text)
    new_text, n_bare = BARE_RE.subn(replace_bare, new_text)
    if n_fig or n_bare:
        new_text = ensure_blank_lines_around(new_text)
    return new_text, n_fig, n_bare


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="Actually rewrite files. Default is dry-run.")
    parser.add_argument("--show-diff", action="store_true",
                        help="Print before/after snippets for each replacement.")
    args = parser.parse_args()

    affected: list[tuple[Path, int, int]] = []

    for posts_dir in POST_DIRS:
        if not posts_dir.exists():
            continue
        for path in sorted(posts_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            new_text, n_fig, n_bare = fix_text(text)
            if n_fig == 0 and n_bare == 0:
                continue
            affected.append((path, n_fig, n_bare))
            if args.show_diff:
                rel = path.relative_to(REPO_ROOT)
                print(f"\n=== {rel} ===")
                for m in FIGURE_RE.finditer(text):
                    print(f"  [figure] BEFORE: {m.group(0)[:120]}...")
                    print(f"           AFTER:  {replace_figure(m)[:120]}...")
                for m in BARE_RE.finditer(text):
                    print(f"  [bare]   BEFORE: {m.group(0)[:120]}...")
                    print(f"           AFTER:  {replace_bare(m)[:120]}...")
            if args.apply:
                path.write_text(new_text, encoding="utf-8")

    total_fig = sum(f for _, f, _ in affected)
    total_bare = sum(b for _, _, b in affected)
    print(f"\nFiles affected: {len(affected)}")
    print(f"Replacements: figure-wrapped={total_fig}, bare={total_bare}, total={total_fig + total_bare}")
    if not args.apply:
        for path, n_fig, n_bare in affected:
            rel = path.relative_to(REPO_ROOT)
            print(f"  {rel}: figure={n_fig}, bare={n_bare}")
        print("\nDRY-RUN — no files written. Re-run with --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
