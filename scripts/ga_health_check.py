#!/usr/bin/env python3
"""Check whether the GA4 instrumentation is measuring what we think it is.

Run this before and after each rollout phase. It reports the handful of
numbers that reveal whether tracking is sound, with an explicit verdict
per check, so "did that change work?" has an answer instead of a vibe.

Usage:
    export GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/ga4-blog-sa.json
    export GA4_PROPERTY_ID=494331706

    python3 scripts/ga_health_check.py                 # last 7 days
    python3 scripts/ga_health_check.py --since 2026-08-25
    python3 scripts/ga_health_check.py --since 365daysAgo   # historical

Exit code is 0 when every check passes, 1 otherwise.
"""

import argparse
import os
import sys

try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Filter, FilterExpression, Metric, OrderBy,
        RunReportRequest,
    )
except ImportError:
    sys.exit("Missing dependency. Run: pip install google-analytics-data")

HUMAN_CHANNELS = ["Organic Search", "Referral", "Organic Social",
                  "Organic Video", "Email", "Paid Search", "AI Assistant"]

PASS, FAIL, INFO, WARN = "PASS", "FAIL", "info", "WARN"


def verdict(tag, label, value, note=""):
    colour = {"PASS": "\033[32m", "FAIL": "\033[31m",
              "WARN": "\033[33m", "info": "\033[90m"}.get(tag, "")
    print(f"  {colour}{tag:>4}\033[0m  {label:<34} {value:>12}   {note}")
    return tag != FAIL


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="7daysAgo",
                    help="window start: YYYY-MM-DD or NdaysAgo (default 7daysAgo)")
    ap.add_argument("--until", default="today")
    args = ap.parse_args()

    prop = os.environ.get("GA4_PROPERTY_ID")
    if not prop:
        sys.exit("Set GA4_PROPERTY_ID to the numeric property id (not G-XXXX).")
    client = BetaAnalyticsDataClient()
    P = f"properties/{prop}"
    window = [DateRange(start_date=args.since, end_date=args.until)]

    def report(dims, mets, limit=25, order=None, dim_filter=None):
        return client.run_report(RunReportRequest(
            property=P,
            dimensions=[Dimension(name=d) for d in dims],
            metrics=[Metric(name=m) for m in mets],
            date_ranges=window, limit=limit,
            order_bys=order or [], dimension_filter=dim_filter))

    print(f"\nGA4 health check — property {prop}, {args.since} .. {args.until}\n")
    ok = True

    # ---- 1. Is page_view firing once per pageload? ----------------------
    r = report([], ["screenPageViews", "sessions", "engagedSessions",
                    "engagementRate", "bounceRate", "userEngagementDuration"])
    if not r.rows:
        sys.exit("No data in this window yet. GA4 lags ~24-48h.")
    m = {h.name: float(v.value)
         for h, v in zip(r.metric_headers, r.rows[0].metric_values)}

    vps = m["screenPageViews"] / max(m["sessions"], 1)
    if vps >= 1.8:
        ok &= verdict(FAIL, "views per session", f"{vps:.3f}",
                      "~2.00 means page_view still fires twice")
    elif vps >= 1.6:
        ok &= verdict(WARN, "views per session", f"{vps:.3f}",
                      "high; check for a second page_view")
    else:
        ok &= verdict(PASS, "views per session", f"{vps:.3f}",
                      "one page_view per pageload")

    # Site-wide engagement rate is meaningless here: it is dominated by bot
    # sessions that bounce instantly. Judge the human channels instead.
    er = m["engagementRate"]
    if er > 0.90:
        ok &= verdict(WARN, "engagement rate (all)", f"{er*100:.1f}%",
                      "implausibly high; usually a double-count artefact")
    else:
        verdict(INFO, "engagement rate (all)", f"{er*100:.1f}%",
                "low is expected — bots dominate and bounce")

    hf = FilterExpression(filter=Filter(
        field_name="sessionDefaultChannelGroup",
        in_list_filter=Filter.InListFilter(values=HUMAN_CHANNELS)))
    rh = report([], ["engagementRate", "sessions"], dim_filter=hf)
    if rh.rows and int(rh.rows[0].metric_values[1].value) >= 30:
        her = float(rh.rows[0].metric_values[0].value)
        n = int(rh.rows[0].metric_values[1].value)
        tag = PASS if her >= 0.35 else WARN
        ok &= verdict(tag, "engagement rate (human)", f"{her*100:.1f}%",
                      f"{n} sessions; content sites run 45-70%")
    else:
        n = int(rh.rows[0].metric_values[1].value) if rh.rows else 0
        verdict(INFO, "engagement rate (human)", "n/a",
                f"only {n} human sessions — need 30+ to read")

    verdict(INFO, "bounce rate", f"{m['bounceRate']*100:.1f}%")
    verdict(INFO, "sessions", f"{m['sessions']:,.0f}")
    verdict(INFO, "page views", f"{m['screenPageViews']:,.0f}")

    # ---- 2. How much of this is actually human? -------------------------
    print()
    r = report(["sessionDefaultChannelGroup"], ["sessions", "userEngagementDuration"],
               15, [OrderBy(metric=OrderBy.MetricOrderBy(
                   metric_name="sessions"), desc=True)])
    total = human = 0
    for row in r.rows:
        ch = row.dimension_values[0].value
        s = int(row.metric_values[0].value)
        total += s
        if ch in HUMAN_CHANNELS:
            human += s
    share = 100 * human / max(total, 1)
    tag = PASS if share >= 20 else INFO
    ok &= verdict(tag, "human-channel sessions", f"{share:.1f}%",
                  f"{human:,} of {total:,} (Direct is bot-dominated here)")

    for row in r.rows[:6]:
        ch = row.dimension_values[0].value
        s = int(row.metric_values[0].value)
        d = float(row.metric_values[1].value)
        verdict(INFO, f"  {ch}", f"{s:,}", f"{d/max(s,1):.1f}s/session")

    # ---- 3. Is the scroll-depth data queryable yet? ---------------------
    print()
    try:
        r = report(["eventName", "customEvent:event_label"], ["eventCount"], 50,
                   [OrderBy(metric=OrderBy.MetricOrderBy(
                       metric_name="eventCount"), desc=True)],
                   FilterExpression(filter=Filter(
                       field_name="eventName",
                       string_filter=Filter.StringFilter(value="scroll"))))
        # '(not set)' is GA4's own enhanced-measurement scroll event, which
        # fires once at 90% and carries no event_label. Only the labelled
        # rows come from our own milestone tracking.
        milestones = {rw.dimension_values[1].value: int(rw.metric_values[0].value)
                      for rw in r.rows if rw.dimension_values[1].value.endswith("%")}
        labelled = sum(milestones.values())
        auto = sum(int(rw.metric_values[0].value) for rw in r.rows
                   if rw.dimension_values[1].value in ("(not set)", ""))

        if labelled >= 50:
            ok &= verdict(PASS, "event_label custom dimension", f"{labelled:,} events",
                          "scroll depth is queryable with usable volume")
        else:
            ok &= verdict(WARN, "event_label custom dimension", f"{labelled:,} events",
                          "registered but still filling (not retroactive)")
        verdict(INFO, "  enhanced-measurement scroll", f"{auto:,}",
                "GA4's own 90% event, unlabelled")

        base = milestones.get("25%", 0)
        for lbl in ("25%", "50%", "75%", "90%", "100%"):
            n = milestones.get(lbl, 0)
            pct = f"{100*n/base:.0f}% of those who reached 25%" if base else ""
            verdict(INFO, f"  reached {lbl}", f"{n:,}", pct)
    except Exception as exc:
        msg = str(exc).split("\n")[0]
        if "not a valid dimension" in msg:
            ok &= verdict(FAIL, "event_label custom dimension", "missing",
                          "register in Admin > Custom definitions")
        else:
            ok &= verdict(FAIL, "event_label custom dimension", "error",
                          msg[:60])

    print("\n" + ("  All checks passed." if ok else
                  "  Some checks failed — see above.") + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
