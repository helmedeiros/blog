#!/usr/bin/env python3
"""Rank blog posts as text-to-speech candidates.

Combines GA4 traffic (reach + engagement depth) with a locally computed
"narratability" score, so the TTS budget goes to posts that people actually
finish AND that read well aloud. A 2012 WordPress import full of inline
screenshots can be popular and still be a terrible thing to narrate.

Usage:
    gcloud auth application-default login \
        --scopes=https://www.googleapis.com/auth/analytics.readonly,\
https://www.googleapis.com/auth/cloud-platform
    export GA4_PROPERTY_ID=312345678
    python3 scripts/ga_top_posts.py --days 365 --top 20

    # Before GA credentials exist, rank on narratability + recency alone:
    python3 scripts/ga_top_posts.py --offline

Requires: pip install google-analytics-data  (not needed for --offline)
"""

import argparse
import glob
import math
import os
import re
import sys
from datetime import date

CONTENT = {"en": "content/en/posts", "pt": "content/pt/posts"}
WPM = 150  # narration pace, matching the Wired reference measurement


# --------------------------------------------------------------------------
# Local content analysis
# --------------------------------------------------------------------------

def split_frontmatter(raw):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        return {}, raw
    fm = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^(\w+):\s*(.*)$", line)
        if km:
            fm[km.group(1)] = km.group(2).strip().strip('"')
    return fm, m.group(2)


def spoken_text(body):
    """Strip everything a narrator would not read aloud."""
    t = re.sub(r"```.*?```", " ", body, flags=re.S)
    t = re.sub(r"~~~.*?~~~", " ", t, flags=re.S)
    t = re.sub(r"\{\{[<%].*?[>%]\}\}", " ", t, flags=re.S)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"!\[[^\]]*\]\[[^\]]*\]", " ", t)
    t = re.sub(r"^\s*\[[^\]]+\]:\s*\S+.*$", " ", t, flags=re.M)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"\[([^\]]*)\]\[[^\]]*\]", r"\1", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"^[ \t]*[#>*\-+]+[ \t]*", " ", t, flags=re.M)
    t = re.sub(r"[*_~|]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def narratability(body, spoken):
    """0..1 — how well this post survives being read aloud.

    Penalises code blocks, image density and raw HTML: all of it either
    vanishes from the audio (leaving dangling references like "as you can
    see below") or has to be awkwardly described.
    """
    if not spoken:
        return 0.0
    code = sum(len(m) for m in re.findall(r"```.*?```", body, re.S))
    images = len(re.findall(r"!\[[^\]]*\]", body))
    html = len(re.findall(r"<(?!/?(?:em|strong|i|b)\b)[a-zA-Z][^>]*>", body))
    words = len(spoken.split())

    code_ratio = code / max(len(body), 1)
    img_per_1k = images / max(words / 1000, 0.1)
    html_per_1k = html / max(words / 1000, 0.1)

    score = 1.0
    score -= min(code_ratio * 2.0, 0.5)      # code is dead air
    score -= min(img_per_1k * 0.08, 0.35)    # "see the screenshot" problem
    score -= min(html_per_1k * 0.02, 0.15)   # WordPress import cruft
    return max(score, 0.0)


def load_posts():
    posts = {}
    for lang, d in CONTENT.items():
        for path in sorted(glob.glob(f"{d}/*.md")):
            stem = os.path.basename(path)[:-3]
            raw = open(path, encoding="utf-8").read()
            fm, body = split_frontmatter(raw)
            spoken = spoken_text(body)
            words = len(spoken.split())
            if words < 100:
                continue
            slug = fm.get("slug") or stem
            url = f"/posts/{slug}/" if lang == "en" else f"/pt/posts/{slug}/"
            posts[url] = {
                "lang": lang,
                "path": path,
                "title": fm.get("title", stem),
                "date": fm.get("date", "")[:10],
                "words": words,
                "chars": len(spoken),
                "minutes": words / WPM,
                "narr": narratability(body, spoken),
                "views": 0,
                "engaged_sec": 0.0,
            }
    return posts


# --------------------------------------------------------------------------
# GA4
# --------------------------------------------------------------------------

# Channels where the traffic is a person. "Direct" is excluded on purpose:
# it is ~96% headless-Chrome bots on this property (11.6k sessions at 2.8s
# each, 97% of them "new"), which swamps every engagement metric.
HUMAN_CHANNELS = ["Organic Search", "Referral", "Organic Social",
                  "Organic Video", "Email", "Paid Search", "AI Assistant"]


def fetch_ga(days, traffic="human"):
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            DateRange, Dimension, Filter, FilterExpression, Metric,
            RunReportRequest,
        )
    except ImportError:
        sys.exit("Missing dependency. Run: pip install google-analytics-data")

    prop = os.environ.get("GA4_PROPERTY_ID")
    if not prop:
        sys.exit("Set GA4_PROPERTY_ID to the numeric property id (not G-XXXX).")

    # Credentials come from either a service-account key (CI) or the
    # Application Default Credentials written by:
    #   gcloud auth application-default login --scopes=...analytics.readonly
    try:
        client = BetaAnalyticsDataClient()
    except Exception as exc:
        sys.exit(
            f"Could not load credentials ({exc}).\n"
            "Either run:\n"
            "  gcloud auth application-default login \\\n"
            "    --scopes=https://www.googleapis.com/auth/analytics.readonly,"
            "https://www.googleapis.com/auth/cloud-platform\n"
            "or set GOOGLE_APPLICATION_CREDENTIALS to a service-account JSON."
        )
    dim_filter = None
    if traffic == "human":
        dim_filter = FilterExpression(filter=Filter(
            field_name="sessionDefaultChannelGroup",
            in_list_filter=Filter.InListFilter(values=HUMAN_CHANNELS)))

    rows, offset = {}, 0
    while True:
        resp = client.run_report(RunReportRequest(
            property=f"properties/{prop}",
            dimensions=[Dimension(name="pagePath")],
            metrics=[Metric(name="screenPageViews"),
                     Metric(name="userEngagementDuration")],
            date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
            dimension_filter=dim_filter,
            limit=1000,
            offset=offset,
        ))
        for r in resp.rows:
            path = r.dimension_values[0].value.split("?")[0].split("#")[0]
            if not path.endswith("/"):
                path += "/"
            v = int(r.metric_values[0].value or 0)
            s = float(r.metric_values[1].value or 0)
            prev = rows.get(path, (0, 0.0))
            rows[path] = (prev[0] + v, prev[1] + s)
        offset += len(resp.rows)
        if len(resp.rows) < 1000 or offset >= resp.row_count:
            break
    return rows


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--lang", choices=["en", "pt", "all"], default="all")
    ap.add_argument("--traffic", choices=["human", "all"], default="human",
                    help="human (default) excludes Direct, ~96%% of it bots")
    ap.add_argument("--offline", action="store_true",
                    help="skip GA; rank on narratability + recency only")
    ap.add_argument("--csv", help="write full ranking to this path")
    args = ap.parse_args()

    posts = load_posts()

    matched = 0
    if not args.offline:
        for path, (views, sec) in fetch_ga(args.days, args.traffic).items():
            if path in posts:
                posts[path]["views"] = views
                posts[path]["engaged_sec"] = sec
                matched += 1
        label = ("human channels only (Direct excluded as bot traffic)"
                 if args.traffic == "human" else "ALL traffic, bots included")
        print(f"GA4: matched {matched} of {len(posts)} posts over the last "
              f"{args.days} days -- {label}.\n")

    ranked = []
    this_year = date.today().year
    for url, p in posts.items():
        if args.lang != "all" and p["lang"] != args.lang:
            continue
        per_view = p["engaged_sec"] / p["views"] if p["views"] else 0.0

        if args.offline:
            try:
                age = this_year - int(p["date"][:4])
            except ValueError:
                age = 20
            score = p["narr"] * math.exp(-age / 4)
        else:
            # Total engaged seconds = the human attention this post actually
            # earned, reach and depth in one number. Site-wide engagement is
            # only ~2s/view (bots and bounces dominate), so any metric using
            # expected-read-time as a denominator is noise; the relative
            # spread between posts, however, is real and large.
            #
            # Narratability is a soft modifier, not a veto: it can at most
            # halve a post's score, so a genuine traffic leader with some code
            # blocks still outranks a prose-perfect post nobody reads.
            score = p["engaged_sec"] * (0.5 + 0.5 * p["narr"])

        p.update(url=url, per_view=per_view, score=score,
                 cost=p["chars"] * 15 / 1_000_000)
        ranked.append(p)

    ranked.sort(key=lambda p: -p["score"])
    top = ranked[:args.top]

    hdr = f"{'#':>3}  {'lang':4} {'date':10} {'views':>6} {'s/view':>7} " \
          f"{'attn':>8} {'narr':>5} {'min':>5} {'$':>6}  title"
    print(hdr)
    print("-" * len(hdr))
    for i, p in enumerate(top, 1):
        attn = f"{p['engaged_sec']/60:.0f}m"
        print(f"{i:>3}  {p['lang']:4} {p['date']:10} {p['views']:>6} "
              f"{p['per_view']:>6.1f}s {attn:>8} {p['narr']:>5.2f} "
              f"{p['minutes']:>5.1f} {p['cost']:>6.2f}  {p['title'][:46]}")

    tot_cost = sum(p["cost"] for p in top)
    tot_min = sum(p["minutes"] for p in top)
    tot_mb = tot_min * 60 * 48 / 8 / 1024
    print(f"\nBatch of {len(top)}: {tot_min:.0f} min audio, "
          f"${tot_cost:.2f} on OpenAI tts-1, {tot_mb:.0f} MB at 48kbps mono.")

    if args.csv:
        import csv
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=[
                "score", "lang", "date", "title", "url", "path", "views",
                "per_view", "engaged_sec", "narr", "words", "minutes", "cost"])
            w.writeheader()
            for p in ranked:
                w.writerow({k: p[k] for k in w.fieldnames})
        print(f"Full ranking ({len(ranked)} posts) written to {args.csv}")


if __name__ == "__main__":
    main()
