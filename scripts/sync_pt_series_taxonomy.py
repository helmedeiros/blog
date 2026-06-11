#!/usr/bin/env python3
"""Copy Hugo `series:` taxonomy from EN posts to their PT counterparts.

For each PT post that:
  - lacks a `series:` field in its frontmatter, AND
  - has an EN counterpart at content/en/posts/<same-filename> with `series:` set

…copy the `series:` block and the `series_order:` line from EN to PT,
inserting them just before the closing `---` of PT's frontmatter.

Refuses to overwrite an existing `series:` field. Refuses if the PT
frontmatter is malformed. Idempotent.

Usage:
    scripts/sync_pt_series_taxonomy.py            # dry-run (default)
    scripts/sync_pt_series_taxonomy.py --apply    # write changes
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EN_DIR = REPO_ROOT / "content/en/posts"
PT_DIR = REPO_ROOT / "content/pt/posts"


def split_frontmatter(text: str) -> tuple[list[str], list[str]] | None:
    """Return (frontmatter_lines_without_fences, body_lines) or None if malformed.

    Each list element keeps its trailing newline (splitlines(keepends=True)).
    """
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\n") != "---":
        return None
    # Find the second `---` on its own line.
    for i in range(1, len(lines)):
        if lines[i].rstrip("\n") == "---":
            return lines[1:i], lines[i:]  # body starts at the closing fence
    return None


def has_series_field(fm_lines: list[str]) -> bool:
    """True if the frontmatter declares a `series:` (top-level) field."""
    for line in fm_lines:
        if line.startswith("series:") or line.startswith("series :"):
            return True
    return False


def extract_series_block(fm_lines: list[str]) -> list[str] | None:
    """Pull the `series:` block + optional `series_order:` line from EN frontmatter.

    Returns the lines to copy (each with trailing newline) or None if not found.
    Handles both the inline form (`series: [foo]`) and the block list form:

        series:
          - foo

    Plus the optional sibling `series_order: N`.
    """
    out: list[str] = []
    n = len(fm_lines)
    i = 0
    while i < n:
        line = fm_lines[i]
        bare = line.rstrip("\n")
        if bare.startswith("series:") or bare.startswith("series :"):
            out.append(line)
            i += 1
            # Consume indented children (list items)
            while i < n:
                nxt = fm_lines[i]
                if nxt.startswith(" ") or nxt.startswith("\t"):
                    out.append(nxt)
                    i += 1
                else:
                    break
            continue
        if bare.startswith("series_order:") or bare.startswith("series_order :"):
            out.append(line)
            i += 1
            continue
        i += 1
    return out or None


def insert_taxonomy(pt_text: str, taxonomy_lines: list[str]) -> str | None:
    """Insert the taxonomy lines at the end of PT frontmatter (before closing ---)."""
    split = split_frontmatter(pt_text)
    if split is None:
        return None
    fm_lines, body_lines = split
    # Ensure the taxonomy block ends with a newline.
    addition = "".join(taxonomy_lines)
    if not addition.endswith("\n"):
        addition += "\n"
    new_fm = "".join(fm_lines) + addition
    # Rebuild: opening fence + new_fm + closing fence + rest of body
    return "---\n" + new_fm + "".join(body_lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rewrite PT files. Default is dry-run.",
    )
    args = parser.parse_args()

    if not PT_DIR.exists() or not EN_DIR.exists():
        print(f"ERROR: expected {EN_DIR} and {PT_DIR}", file=sys.stderr)
        return 2

    candidates: list[tuple[Path, Path, list[str]]] = []  # (pt_path, en_path, taxonomy)
    skipped_no_en: list[Path] = []
    skipped_en_no_series: list[Path] = []
    skipped_pt_has_series: list[Path] = []
    skipped_malformed_fm: list[Path] = []

    for pt_path in sorted(PT_DIR.glob("*.md")):
        pt_text = pt_path.read_text(encoding="utf-8")
        pt_split = split_frontmatter(pt_text)
        if pt_split is None:
            skipped_malformed_fm.append(pt_path)
            continue
        pt_fm, _ = pt_split
        if has_series_field(pt_fm):
            skipped_pt_has_series.append(pt_path)
            continue

        en_path = EN_DIR / pt_path.name
        if not en_path.exists():
            skipped_no_en.append(pt_path)
            continue

        en_text = en_path.read_text(encoding="utf-8")
        en_split = split_frontmatter(en_text)
        if en_split is None:
            skipped_malformed_fm.append(en_path)
            continue
        en_fm, _ = en_split
        taxonomy = extract_series_block(en_fm)
        if taxonomy is None:
            skipped_en_no_series.append(pt_path)
            continue

        candidates.append((pt_path, en_path, taxonomy))

    print(f"Candidates: {len(candidates)} PT post(s) will receive taxonomy from EN.")
    for pt_path, en_path, taxonomy in candidates:
        rel = pt_path.relative_to(REPO_ROOT)
        print(f"\n  {rel}")
        for line in taxonomy:
            print(f"    + {line.rstrip()}")

    if args.apply:
        written = 0
        for pt_path, _, taxonomy in candidates:
            pt_text = pt_path.read_text(encoding="utf-8")
            new_text = insert_taxonomy(pt_text, taxonomy)
            if new_text is None:
                continue  # safety: skip on parse failure
            pt_path.write_text(new_text, encoding="utf-8")
            written += 1
        print(f"\nWrote {written} file(s).")
    else:
        print("\nDRY-RUN — no files written. Re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
