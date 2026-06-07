# Series convention

How to wire a group of posts into a discoverable series on this blog. Use this whenever a new arc of posts should be readable in order, with a landing page and in-post navigation.

The convention is the same one used by:

- `pricing-platform` (13 posts, 2023–2026)
- `dotfiles` (11 posts, 2013–2025)
- `okra` (existing)

## What "being a series" gives a reader

Once a series is wired up, the reader gets three discovery surfaces for free:

| Surface | Where it appears | What it shows |
| --- | --- | --- |
| **Series landing page** | `/series/{slug}/` (and `/pt/series/{slug}/`) | Friendly title, description, total count, every post in `series_order` as a numbered reading list with date and subtitle |
| **In-post nav** | End of every post in the series, just before the footer | "Part of the series **<title>**", the full ordered list with the current post marked "you're reading this one" / "você está lendo este", and a "View all posts in this series →" link |
| **Hugo taxonomy** | `/series/`, RSS, related-posts logic | The `series` taxonomy is configured in `config.toml` and Hugo auto-populates it from post front matter |

## Convention — three pieces

### 1. Post front matter

Every post in the series gets:

```yaml
series:
  - slug-of-the-series
series_order: 7
```

Rules:

- **Slug is lowercase-hyphenated, ASCII only**, and shared across EN and PT. Examples: `pricing-platform`, `dotfiles`, `okra`.
  Do not invent a different PT slug — the series should resolve to the same URL slug under `/series/{slug}/` in both languages. The title and description differ per language; the slug doesn't.
- **`series_order` is an integer starting at 1**, contiguous, with no duplicates. Use chronological order by `date` unless a different reading order is intentional.
- **List form, not single-string form.** Older posts on the blog use `series: "Display Name"` as a single string. That works for Hugo's taxonomy URL generation but conflicts with the landing page template's lookup. New series use the list form above.

### 2. Series term file

One file per language at `content/{en,pt}/series/{slug}.md`. Front matter only, no body:

```yaml
---
title: "Building a Pricing Platform: The Series"
description: "Thirteen posts on building and evolving a revenue-critical pricing platform — from Strangler Fig migration through rule engines, experimentation, segmentation, models, simulation, and the lifecycle that holds it all together."
---
```

- The **title** drives the heading on the landing page, the eyebrow on the in-post nav, the page `<title>`, and OpenGraph.
- The **description** drives the landing page subtitle and the page meta description.
- No `_index.md`, no directory — just a flat file named after the slug.

### 3. Templates (already in place)

You don't normally need to touch these — they already exist:

| File | Purpose |
| --- | --- |
| `layouts/partials/series-nav.html` | Renders the in-post navigation block. Picks up the series title from the term file via `.Site.GetPage`. Bilingual via `.Language.Lang`. |
| `layouts/series/single.html` | Renders the `/series/{slug}/` landing page: title, description, total count, numbered reading list ordered by `series_order`. |
| `layouts/_default/single.html` | Includes `series-nav.html` between the article body and the footer. Don't move that include. |
| `config.toml` | The `series = "series"` taxonomy entry. Already configured — don't change. |

## Wiring up a new series — the checklist

1. **Pick a slug.** Lowercase-hyphenated, ASCII only, shared across EN and PT. Sanity-check it doesn't collide with an existing series in `content/{en,pt}/series/`.
2. **Decide read order.** By default, chronological by `date`. Number the posts 1..N — no duplicates, no gaps.
3. **Add `series:` + `series_order:` to each post** in both EN and PT, using the list form. Insert in the front matter right before `description:` (the convention used by pricing-platform and dotfiles).
4. **Create the term file in both languages**: `content/en/series/{slug}.md` and `content/pt/series/{slug}.md`. Front matter only — title + description, no body.
5. **Run `hugo --quiet --destination /tmp/series-check`**. The landing pages should exist at `/series/{slug}/` and `/pt/series/{slug}/`. Verify the post count is right and the order matches what you expect.
6. **Open one of the posts locally**. The in-post navigation block should appear at the end of the body with the right title and the current post highlighted.
7. **Commit and push.**

## Important: don't auto-edit old posts

The older posts (2008–2012 conference reports, 2022 Kanban-to-Scrum, etc.) use a different front matter format — `series: "Display Name"` as a single string, often without `series_order`. Hugo still generates a URL for those series, but they don't render in the landing page template the same way.

**Don't sweep them retroactively in one script.** They'll need a careful per-series pass (rewriting the `series:` line into list form, picking a slug, adding `series_order`, then creating the term file). Each is a small, reviewable PR — never bundle multiple old series into one mass edit.

## Naming hygiene

- Keep titles human and descriptive on the term file. Not just "Pricing Platform" — say what the series is *about*.
- Description should hint at the arc, the time span, or the depth. Reader sees this before they invest in 13 posts.
- Don't put the post count in the description — the landing page template renders it automatically as "N posts in total" / "N posts no total".

## When in doubt

Look at `content/en/series/pricing-platform.md` and `content/en/series/dotfiles.md`. They follow this convention exactly and serve as the working reference.
