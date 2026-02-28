# Helio Medeiros — Blog

Bilingual technology blog at [blog.heliomedeiros.com](https://blog.heliomedeiros.com).
Notes on software engineering, leadership, pricing systems, agile practice,
and working with AI agents — written in **English** and **Brazilian
Portuguese (PT-BR)**.

- Browse in English: [blog.heliomedeiros.com](https://blog.heliomedeiros.com)
- Ler em português: [blog.heliomedeiros.com/pt](https://blog.heliomedeiros.com/pt)

## What's in here

The repo holds the full Hugo source for the site — content, layouts,
theme, and the GitHub Actions pipeline that deploys to GitHub Pages.

- **`content/en/`** and **`content/pt/`** — bilingual post and series content.
- **`layouts/`** — custom Hugo templates and shortcodes.
- **`themes/beautifulhugo/`** — base theme (pinned submodule).
- **`static/`** — images, CSS, uploads.
- **`scripts/`** — Python helpers for occasional content maintenance.
- **`docs/`** — operational notes.

## Voice & style

Two style guides describe how the blog is written. New posts and edits
should follow them.

- **[`STYLE_GUIDE.md`](STYLE_GUIDE.md)** — English voice and writing patterns.
- **[`STYLE_GUIDE_PT_BR.md`](STYLE_GUIDE_PT_BR.md)** — Brazilian Portuguese
  voice (PT-BR only, never PT-PT). Identity and natural phrasing rather
  than translation rules.

## Series

Related posts are grouped into series — conference notes, technical
deep-dives, and longer-form reflections. A post joins a series by
declaring `series:` and `series_order:` in its front matter. The
current list lives at [`/series/`](https://blog.heliomedeiros.com/series/);
the wiring convention is documented in
[`docs/SERIES_CONVENTION.md`](docs/SERIES_CONVENTION.md).

## Stack

- **Hugo** static site generator with the Beautiful Hugo theme.
- **Bilingual** content under language directories (`en/`, `pt/`).
- **GitHub Actions** builds on every push to `master` and deploys to
  GitHub Pages.
- **Custom domain**: `blog.heliomedeiros.com`.

## Local development

```bash
brew install hugo
git clone --recurse-submodules <repository-url>
cd blog

# Live-reload dev server
hugo server -D

# Production build
hugo --minify
```

If you cloned without `--recurse-submodules`, fetch the theme:

```bash
git submodule update --init --recursive
```

## Deployment

Pushes to `master` trigger the **Deploy Hugo site to Pages** workflow,
which builds with the pinned Hugo version and publishes to GitHub
Pages. To deploy manually: **Actions → Deploy Hugo site to Pages →
Run workflow**.
