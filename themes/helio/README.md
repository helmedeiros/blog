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
`layouts` and `static`. Since then the self-hosted asset mode, the
highlight.js option, the mermaid shortcode, KaTeX and the demo images
have been removed. The upstream example site, screenshots and CI
files were left out.

## Changing the theme

Templates in the site's own `layouts/` directory override the ones here,
so most of the blog's look is defined there and in the site's
`assets/css/`.

The theme's stylesheets live in `assets/css/` and are bundled into one
minified, fingerprinted `theme.min.<hash>.css`; the site bundles its own
into `site.min.<hash>.css`. Bootstrap, jQuery and PhotoSwipe load from
their CDNs with integrity hashes, and PhotoSwipe only on pages whose
content has a `<figure>`.

Site parameters the theme reads:

- `googleFonts`: the query for one Google Fonts css2 request; defaults to
  the theme's Lora and Open Sans families.
- `fontAwesome`: set to `false` to skip the Font Awesome CDN stylesheet
  when the site serves its own icons.

To adopt something from upstream Beautiful Hugo, port that change on its
own, then check the build with the link checker and smoke test
(`python3 scripts/check_links.py public` and `npm run smoke -- <url>`) and
compare screenshots of the home page, a post and the series page before
merging. Upstream moved to a different layout structure after v3.5.0, so
updating wholesale breaks the blog's navigation and post layout.
