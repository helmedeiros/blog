#!/usr/bin/env python3
"""Archive original PDFs of your own Speaker Deck presentations.

Speaker Deck is a CDN, not a backup. This pulls the original PDF for every
deck on a profile so the talks survive the platform. Older decks sometimes
expose no PDF at all - those are reported explicitly at the end, because a
deck you cannot download is a deck that exists in exactly one place.

Downloads go OUTSIDE the git repo: PDFs do not delta-compress, and a few
hundred MB of them would permanently bloat .git.

Usage:
    python3 scripts/archive_speakerdeck.py                    # default user
    python3 scripts/archive_speakerdeck.py --user someone
    python3 scripts/archive_speakerdeck.py --out ~/somewhere
    python3 scripts/archive_speakerdeck.py --dry-run

Re-running skips decks already downloaded at the expected size, so it is
safe to resume an interrupted archive.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

BASE = "https://speakerdeck.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
SKIP = {"followers", "following", "stars"}


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def head_size(url):
    """Size without downloading. Some older decks answer HEAD without a
    Content-Length, so fall back to a one-byte ranged GET and read the total
    out of Content-Range. Never treat an unknown size as "missing" - these
    decks download perfectly well, HEAD just does not describe them."""
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            n = int(r.headers.get("Content-Length") or 0)
            if n:
                return n
    except Exception:
        pass
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": UA, "Range": "bytes=0-0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            cr = r.headers.get("Content-Range", "")
            m = re.search(r"/(\d+)$", cr)
            if m:
                return int(m.group(1))
    except Exception:
        pass
    return 0


def list_decks(user):
    """Walk every page of the profile. Speaker Deck paginates silently -
    reading only page 1 undercounts, which is how 34 decks looked like 19."""
    slugs, page = [], 1
    while True:
        try:
            html = get(f"{BASE}/{user}?page={page}")
        except urllib.error.HTTPError:
            break
        found = re.findall(rf'href="/{re.escape(user)}/([a-z0-9-]+)"', html)
        fresh = [s for s in dict.fromkeys(found) if s not in SKIP and s not in slugs]
        if not fresh:
            break
        slugs.extend(fresh)
        print(f"  page {page}: {len(fresh)} decks")
        page += 1
        if page > 25:
            break
    return slugs


def deck_info(user, slug):
    html = get(f"{BASE}/{user}/{slug}")
    pdf = re.search(r'https?://files\.speakerdeck\.com[^"\'\s]*\.pdf', html)
    title = re.search(r'<meta property="og:title" content="([^"]*)"', html)
    return (pdf.group(0) if pdf else None,
            title.group(1) if title else slug)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="helmedeiros")
    ap.add_argument("--out", default="~/Dropbox/DOCUMENTS/speakerdeck-archive")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    out = os.path.expanduser(args.out)
    if not args.dry_run:
        os.makedirs(out, exist_ok=True)

    print(f"\nArchiving speakerdeck.com/{args.user} -> {out}\n")
    slugs = list_decks(args.user)
    print(f"\n{len(slugs)} decks found.\n")

    got, missing, skipped, total = [], [], 0, 0
    for i, slug in enumerate(slugs, 1):
        try:
            pdf, title = deck_info(args.user, slug)
        except Exception as exc:
            print(f"  [{i:>2}/{len(slugs)}] {slug}: page error ({exc})")
            missing.append({"slug": slug, "title": slug, "reason": str(exc)})
            continue

        if not pdf:
            print(f"  [{i:>2}/{len(slugs)}] \033[33mNO PDF\033[0m   {title[:56]}")
            missing.append({"slug": slug, "title": title,
                            "reason": "no PDF exposed on the public page"})
            continue

        size = head_size(pdf)
        dest = os.path.join(out, f"{slug}.pdf")
        mb = size / 1048576

        if os.path.exists(dest) and size and abs(os.path.getsize(dest) - size) < 1024:
            print(f"  [{i:>2}/{len(slugs)}] have     {mb:6.1f} MB  {title[:46]}")
            skipped += 1
            total += size
            got.append({"slug": slug, "title": title, "pdf": pdf, "bytes": size})
            continue

        if args.dry_run:
            shown = f"{mb:6.1f} MB" if size else "  size ? "
            print(f"  [{i:>2}/{len(slugs)}] would   {shown}  {title[:46]}")
            total += size
            got.append({"slug": slug, "title": title, "pdf": pdf, "bytes": size})
            continue

        try:
            data = get(pdf, binary=True)
            with open(dest, "wb") as fh:
                fh.write(data)
            total += len(data)
            print(f"  [{i:>2}/{len(slugs)}] \033[32msaved\033[0m    "
                  f"{len(data)/1048576:6.1f} MB  {title[:46]}")
            got.append({"slug": slug, "title": title, "pdf": pdf,
                        "bytes": len(data)})
        except Exception as exc:
            print(f"  [{i:>2}/{len(slugs)}] \033[31mFAILED\033[0m   {title[:46]} ({exc})")
            missing.append({"slug": slug, "title": title, "reason": str(exc)})

    print(f"\n  {len(got)} archived ({skipped} already present), "
          f"{total/1048576:.0f} MB total")

    if missing:
        print(f"\n  \033[33m{len(missing)} deck(s) with no downloadable original:\033[0m")
        for m in missing:
            print(f"    - {m['title']}")
            print(f"      {BASE}/{args.user}/{m['slug']}")
        print("\n  Check these while signed in as the owner - Speaker Deck\n"
              "  sometimes offers a download that the public page does not.\n"
              "  If it does not, these exist in exactly one place.")

    if not args.dry_run:
        manifest = os.path.join(out, "manifest.json")
        with open(manifest, "w", encoding="utf-8") as fh:
            json.dump({"user": args.user, "archived": got, "missing": missing},
                      fh, indent=2, ensure_ascii=False)
        print(f"\n  Manifest: {manifest}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
