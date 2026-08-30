#!/usr/bin/env python3
"""Find the queries this blog is one edit away from ranking for.

Google organic is the largest human channel here (205 of ~430 sessions a
year), and Search Console is the only place that shows what people actually
searched before landing - or, more usefully, what they searched where the
blog appeared and was *not* clicked.

The interesting rows are not the ones already ranking. They are:

  near-miss   position 8-20 with real impressions. Already relevant enough
              to surface, not visible enough to click. Cheapest wins.
  no-click    high impressions, near-zero CTR. Usually a title/description
              problem rather than a ranking problem.
  rising      queries growing period over period.

Usage:
    export GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/ga4-blog-sa.json
    python3 scripts/gsc_near_misses.py
    python3 scripts/gsc_near_misses.py --days 90 --min-impressions 20
    python3 scripts/gsc_near_misses.py --pages      # by page instead of query
    python3 scripts/gsc_near_misses.py --csv out.csv

Requires the service account to be added as a user on the Search Console
property (Settings -> Users and permissions -> Add user -> Full/Restricted).
"""

import argparse
import datetime as dt
import os
import sys

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    sys.exit("Missing deps. Run: pip install google-api-python-client")

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
DOMAIN = "blog.heliomedeiros.com"


def resolve_site(svc, wanted=None):
    """Find the property to query.

    Search Console has two property types and the API addresses them
    differently: a URL-prefix property is 'https://host/' while a Domain
    property is 'sc-domain:host'. Guessing wrong returns a bare 404, so
    ask the API which properties this service account can actually see.
    """
    try:
        entries = svc.sites().list().execute().get("siteEntry", [])
    except HttpError as e:
        if e.resp.status == 403:
            sys.exit("\n403 listing properties. The service account has no\n"
                     "Search Console access yet - add it under\n"
                     "Settings -> Users and permissions.\n")
        raise
    if not entries:
        sys.exit("\nThe service account can see no Search Console properties.\n"
                 "Add it: Settings -> Users and permissions -> Add user ->\n"
                 "  ga4-blog-reader@helio-blog-ga.iam.gserviceaccount.com\n")

    urls = [e["siteUrl"] for e in entries]
    if wanted:
        for u in urls:
            if u == wanted or wanted in u:
                return u
        sys.exit(f"\n{wanted!r} not among accessible properties:\n  " +
                 "\n  ".join(urls) + "\n")
    # prefer a Domain property, then any URL-prefix one, for this blog
    for u in urls:
        if u == f"sc-domain:{DOMAIN}":
            return u
    for u in urls:
        if DOMAIN in u:
            return u
    return urls[0]


def client():
    key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not key:
        sys.exit("Set GOOGLE_APPLICATION_CREDENTIALS to the service-account JSON.")
    creds = service_account.Credentials.from_service_account_file(
        os.path.expanduser(key), scopes=SCOPES)
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def query(svc, site, start, end, dimensions, limit=25000):
    rows, start_row = [], 0
    while True:
        body = {"startDate": start, "endDate": end, "dimensions": dimensions,
                "rowLimit": 25000, "startRow": start_row}
        try:
            resp = svc.searchanalytics().query(siteUrl=site, body=body).execute()
        except HttpError as e:
            if e.resp.status == 403:
                sys.exit(
                    f"\n403 from Search Console for {site}.\n"
                    "Add the service account as a user on the property:\n"
                    "  Search Console -> Settings -> Users and permissions\n"
                    "  -> Add user -> the ...iam.gserviceaccount.com address\n"
                    "Also confirm the site URL matches the property exactly\n"
                    "(https + trailing slash for a URL-prefix property).\n")
            if e.resp.status == 404:
                sys.exit(f"\n404: no Search Console property matches {site!r}.\n"
                         "Pass the exact property URL with --site.\n")
            raise
        batch = resp.get("rows", [])
        rows.extend(batch)
        start_row += len(batch)
        if len(batch) < 25000 or start_row >= limit:
            break
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=None,
                    help="property to query; auto-detected if omitted")
    ap.add_argument("--list", action="store_true",
                    help="list accessible properties and exit")
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--min-impressions", type=int, default=10)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--pages", action="store_true",
                    help="group by page instead of query")
    ap.add_argument("--csv")
    args = ap.parse_args()

    svc = client()
    if args.list:
        entries = svc.sites().list().execute().get("siteEntry", [])
        if not entries:
            print("\n  No properties visible to this service account.\n"
                  "  Search Console -> Settings -> Users and permissions ->\n"
                  "  Add user -> ga4-blog-reader@helio-blog-ga"
                  ".iam.gserviceaccount.com\n")
            return 1
        for e in entries:
            print(f"  {e['permissionLevel']:22} {e['siteUrl']}")
        return 0
    site = resolve_site(svc, args.site)
    end = dt.date.today() - dt.timedelta(days=2)      # GSC lags ~2 days
    start = end - dt.timedelta(days=args.days)
    dim = ["page"] if args.pages else ["query"]

    rows = query(svc, site, start.isoformat(), end.isoformat(), dim)
    if not rows:
        print(f"\nNo data for {site} in {start}..{end}.\n"
              "If the property was just verified, Search Console needs a few\n"
              "days before search-analytics data appears.\n")
        return 0

    recs = [{"key": r["keys"][0], "clicks": r["clicks"],
             "impressions": r["impressions"], "ctr": r["ctr"],
             "position": r["position"]} for r in rows]
    tot_c = sum(r["clicks"] for r in recs)
    tot_i = sum(r["impressions"] for r in recs)
    label = "pages" if args.pages else "queries"
    print(f"\nSearch Console — {site}   {start} .. {end}")
    print(f"{len(recs):,} {label} | {tot_i:,} impressions | {tot_c:,} clicks "
          f"| {100*tot_c/max(tot_i,1):.1f}% CTR\n")

    def table(title, sel, note=""):
        sel = sel[:args.top]
        if not sel:
            print(f"  {title}: none\n"); return
        print(f"  \033[1m{title}\033[0m  {note}")
        print(f"    {'clicks':>6} {'impr':>7} {'ctr':>6} {'pos':>6}  {label[:-1]}")
        for r in sel:
            print(f"    {r['clicks']:>6} {r['impressions']:>7} "
                  f"{100*r['ctr']:>5.1f}% {r['position']:>6.1f}  {r['key'][:58]}")
        print()

    qualified = [r for r in recs if r["impressions"] >= args.min_impressions]

    near = sorted([r for r in qualified if 8 <= r["position"] <= 20],
                  key=lambda r: -r["impressions"])
    table("NEAR MISSES (position 8-20)", near,
          "— already relevant, not yet visible. Best effort/reward.")

    noclick = sorted([r for r in qualified
                      if r["position"] <= 10 and r["ctr"] < 0.02],
                     key=lambda r: -r["impressions"])
    table("RANKING BUT NOT CLICKED (top 10, CTR < 2%)", noclick,
          "— usually a title/description problem, not a ranking one.")

    winners = sorted(recs, key=lambda r: -r["clicks"])
    table("ALREADY WINNING", winners, "— protect and expand these.")

    if args.csv:
        import csv
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["key", "clicks", "impressions",
                                               "ctr", "position"])
            w.writeheader()
            w.writerows(sorted(recs, key=lambda r: -r["impressions"]))
        print(f"  Full data ({len(recs):,} rows) -> {args.csv}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
