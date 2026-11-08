# helio theme

The theme for [blog.heliomedeiros.com](https://blog.heliomedeiros.com). It
lives in this repository so upstream changes can never restyle the blog
unexpectedly.

## Origin

Forked from [Beautiful Hugo](https://github.com/halogenica/beautifulhugo)
v3.5.0 (commit `e69e25d4ca0d3c737f0677995d2bf9541ffb4926`), which the blog
used as a git submodule until then. Beautiful Hugo is MIT licensed; its
license and copyright notices are kept in [LICENSE](LICENSE).

Only the parts Hugo uses were copied: `archetypes`, `data`, `i18n`,
`layouts` and `static`. The upstream example site, screenshots and CI
files were left out.

## Changing the theme

Templates in the site's own `layouts/` directory override the ones here,
so most of the blog's look is defined there and in
`static/css/custom-layout.css` and `static/css/blog-style.css`.

To adopt something from upstream Beautiful Hugo, port that change on its
own, then check the build with the link checker and smoke test
(`python3 scripts/check_links.py public` and `npm run smoke -- <url>`) and
compare screenshots of the home page, a post and the series page before
merging. Upstream moved to a different layout structure after v3.5.0, so
updating wholesale breaks the blog's navigation and post layout.
