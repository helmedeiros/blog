# Rollout Plan: Listen-to-Post Audio & Analytics Repair

Adding a "listen to this post" option to the blog, and fixing the analytics
needed to tell whether it worked.

Phases run **one at a time**. Each has an explicit check with a pass/fail
answer, and a Result box to fill in before moving on. The ordering is not
cosmetic: changes to the *measuring instrument* come first and must settle,
otherwise later changes can't be attributed.

Verify any phase with:

```sh
export GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/ga4-blog-sa.json
export GA4_PROPERTY_ID=494331706
.venv-ga/bin/python scripts/ga_health_check.py --since 2026-08-26
```

---

## The constraint that shapes everything

Over the 365 days to 2026-08-25, GA4 recorded 12,121 sessions — but only
**430 of them (3.5%) came from human channels**. The rest is Direct traffic
averaging 2.8 seconds per session, 97% "new": headless-Chrome bots.

Real human traffic is roughly **1,023 page views per year, about 20 per week**
across the whole blog.

That number governs the whole plan. **No change here can be A/B tested.** A 5%
play rate on 20 weekly views is one play a month — you would wait a year for a
signal that never arrives. So:

- Phases 0–2 (instrumentation) have fast, unambiguous technical checks. Trust those.
- Phases 3+ (product) are judged on **quality and cost**, not conversion stats.
  Instrument them anyway, but never *wait* on the data to decide.

---

## Baseline — recorded 2026-08-25, before any change

| Metric | Value | Reading |
| --- | --- | --- |
| Views per session | **1.998** | page_view fires twice; all view counts 2x inflated |
| Engagement rate | 94.3% | artefact — GA4 marks >=2 views "engaged" |
| Bounce rate | 5.7% | artefact of the same bug |
| Sessions (365d) | 12,121 | |
| Page views (365d) | 24,221 | ~12,100 real |
| Human-channel sessions | 3.5% | 430 of 12,113 |
| Human page views | ~1,023 | across 108 pages |
| Human engagement | 17.8s/view | ~35s once corrected for double-count |

Channel split: Direct 11,658 (2.8s) · Organic Search 241 (47.1s) ·
Organic Social 120 (14.2s) · Referral 54 (95.0s) · AI Assistant 15 (2.3s).

Organic Search at 47s and Referral at 95s per session are **healthy**. The
readers are fine; the measurement was not.

---

## Phase 0 — Repair the instrument  ▸ *today*

Nothing downstream is trustworthy until this lands.

- [x] Suppress the duplicate `page_view` (`0586c49`)
- [x] Serve a `robots.txt` that welcomes AI crawlers (`57d3037`)
- [x] Add GA4-backed post ranking (`0a52ead`)
- [x] Register `event_label` as an event-scoped custom dimension in GA4
- [x] Push to `master` — deployed 2026-08-26, run 32935777379
- [ ] Set **Admin → Data Settings → Data Retention → 14 months**

Retention matters more than it first appeared: queries involving a custom
dimension read *event-level* data, which the retention window **does** cap.
Aggregate reports are unaffected. So scroll-depth analysis specifically is
limited by this setting. Not retroactive — change it now.

**Check after 48h** (GA4 lags 24–48h):

| Check | Before | Pass condition |
| --- | --- | --- |
| Views per session | 1.998 | **< 1.6** |
| Engagement rate | 94.3% | **< 90%**, ideally 45–70% |
| `event_label` events | 10 | **> 50** and growing |

If views/session is still ~2.00, the deploy didn't take — check the Actions run.

> **Result — checked 2026-08-27: PASS**
>
> Views/session **1.998 → 1.167** on deploy day. Decisive: every day in the
> preceding three weeks sat at ~2.00 (range 1.57–2.22, mostly exactly 2.00),
> and 2026-08-26 is the first below 1.5 in the window. `robots.txt` returns
> 200, `send_page_view:!1` confirmed in the deployed bundle.
>
> Sample is thin (7 views / 6 sessions, and GA4 had not ingested the 27th),
> so direction is certain but magnitude is not. Ignore the 33.3% engagement
> rate — 2 of 6 sessions is noise.
>
> **Discovered:** bot traffic arrives in *campaigns*, not a steady trickle.
> Eight burst days (2026-08-12 to -20) total 12,666 views — **52% of the
> entire year's recorded traffic in eight days**. Normal days are 6–35 views.
> The 24,221 annual figure is mostly one month of scraping, so the long-run
> human baseline is thinner still. Phase 2 must be checked during or just
> after a burst to show anything; a quiet day reveals nothing.

---

## Phase 1 — Baseline on clean data  ▸ *~5 weeks, change nothing*

The discipline step. Let uncontaminated data accumulate.

**Revised 2026-08-30.** Originally scoped at 2 weeks on an assumption of ~2
human sessions/day. Five days of clean data show **0.8/day** (4 human sessions
2026-08-26 to -30), so the 30-session threshold needed for a readable
engagement rate lands in **early October**, not mid-September.

- [ ] Wait until ~2026-10-01 without shipping tracking changes
- [ ] Re-run `ga_health_check.py` — "engagement rate (human)" should stop
      reporting n/a once 30+ human sessions have accumulated
- [ ] Keep ranking on `--days 365`; a 14-day window returns noise at this volume

**Comparing across 2026-08-26 requires halving the older side.** Pre-fix view
counts were doubled, so raw before/after comparisons show a phantom 50% drop.
Real traffic has been flat across the deploy.

> **Result (fill in):**
> Human sessions accumulated:
> Engagement rate (human):
> New top 5:

---

## Phase 2 — Cloudflare in front  ▸ *one evening*

Deliberately **not** simultaneous with Phase 0, so effects stay attributable.
This is the only way to see crawler traffic at all: AI crawlers don't execute
JavaScript, so they are invisible to GA4 and always will be. GitHub Pages
gives no access logs.

Also needed later for R2 audio hosting, so this is not a detour.

- [ ] Screenshot the **complete** GoDaddy DNS record list first
- [ ] Cloudflare free account → add `heliomedeiros.com`
- [ ] **Diff imported records against the screenshot — especially MX.**
      Nameserver changes move the whole zone; a missed MX silently kills email
- [ ] **Carry over the Google Search Console TXT record.** The Domain
      property is verified by a TXT record Google wrote into the GoDaddy
      zone. If it does not survive the import, Search Console verification
      breaks and the near-miss query reports stop working
- [ ] GoDaddy → Nameservers → Custom → Cloudflare's two
- [ ] **SSL/TLS → Full (strict).** Never Flexible — GitHub Pages forces HTTPS
      and Flexible causes an infinite redirect loop
- [ ] Leave `static/CNAME` untouched

**Check after 24h:**

- [ ] Site loads over HTTPS, no redirect loop
- [ ] Email still delivers (send yourself one)
- [ ] Cloudflare analytics shows a crawler breakdown
- [ ] Cloudflare human page views roughly agree with GA4 — large divergence
      means misconfiguration
- [ ] Did the disallowed SEO scrapers actually stop? robots.txt compliance is
      voluntary, and this is the first time you can see who ignored it

Certificate note: GitHub renews via an HTTP-01 challenge that can fail while
proxied. Existing cert is fine; at renewal you may need to grey-cloud briefly.

> **Result (fill in):**
> Crawlers seen:
> Bots blocked:            Email OK?

---

## Phase 3 — Audio pilot, 2 posts  ▸ *~$0.30*

Not 8. Two, chosen to bracket the quality range:

| Post | Why | narr | Human engagement |
| --- | --- | --- | --- |
| It is time for Agent-Friendly Codebase | code-heavy — the stress test | 0.68 | 48.9s/view |
| Bullet Journal | prose-perfect — the benchmark | 0.97 | 104.7s/view |

- [ ] Build the TTS script (strip frontmatter/code/shortcodes, content-hash keyed)
- [ ] Generate both on OpenAI `tts-1`, 48kbps mono
- [ ] Listen to each **end to end**

**Check — qualitative, and that is deliberate:**

> Would you listen to your own post without wincing? Do the code sections
> produce dead air or dangling "as you can see below" references?

If the code-heavy one fails, that's the real constraint discovered for pocket
change. Options then: skip code-heavy posts, or write a spoken-form summary
for code blocks.

- [ ] Expand to the top 8 only if this passes

> **Result (fill in):**
> Agent-Friendly:          Bullet Journal:
> Constraint found:

---

## Phase 4 — Player + instrumentation  ▸ *don't wait on the data*

- [ ] `layouts/partials/listen.html`, audio as a front-matter field
- [ ] Upload MP3s to R2 (free tier, **zero egress** — the reason not to use
      S3+CloudFront, where one viral post is a surprise bandwidth bill)
- [ ] GA events: `audio_play`, `audio_25/50/75/complete`

At ~20 human views/week across the whole blog, two posts with audio might see
1–2 views a week between them. **A meaningful play rate is not obtainable.**
Instrument it because it's cheap and useful later — then decide on whether the
thing is good.

---

## Phase 5 — Podcast feed  ▸ *the actual payoff*

- [ ] Hugo layout emitting RSS with `<enclosure>` tags
- [ ] Submit to Apple Podcasts and Spotify

Different metric entirely: **subscribers, not play rate.** It reaches people
who will never visit the site — which, at 20 human views a week, is where
audio earns its keep. Everything before this is groundwork.

- [ ] Backfill more posts only once subscribers exist

---

## Phase 6 — llms.txt  ▸ *lowest confidence, last*

- [ ] Generate a curated markdown index from Hugo

Honest caveat: an emerging convention, and **no major LLM provider has
committed to reading it**. An hour's work and a lottery ticket, not a strategy.

---

## Full backfill economics (for later)

Measured across 456 posts, stripping everything a narrator wouldn't read:

- **2,300,915 spoken characters** = 374,677 words = **41.6 hours** of audio
- Spoken text is 74% of raw markdown (the rest is code and markup)
- OpenAI `tts-1` at $15/1M chars → **$34.51**, budget **$45** with re-runs
- Ongoing: **$0.15 per new post** (both languages), ~$1.20/year
- Storage: 878 MB at 48kbps — inside R2's 10 GB free tier, egress free
- ElevenLabs would be $299–598 for the same backfill

Money is not the constraint. The 1–2 days of pipeline work is.

**Do not put MP3s in the repo** — even the 32kbps encode is 585 MB of binary
that won't delta-compress, against a `.git` already at 174 MB and a GitHub
Pages 1 GB site limit with 93 MB of `uploads/` already there.
