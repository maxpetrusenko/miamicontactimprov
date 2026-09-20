# miamicontactimprov.com

Independent, non-commercial community resource mapping Contact Improvisation
(CI) across Miami-Dade and Broward County, Florida.

Static site. Cloudflare Pages. Built by a Python generator, gated in CI, deployed
from `main` only.

## Layout

```
build/          generator (Python, stdlib + Pillow for raster assets)
  shell.py        head, nav, footer, page assembly, reusable content blocks
  schema.py       JSON-LD @graph builders
  content_core.py         home, what-is, history, glossary
  content_practice.py     jams, classes, safety-and-consent, videos
  content_directory.py    miami, directory, faq, about, 404
  listings.py     CONFIRMED local jams / classes / teachers. Empty is a valid state.
  videos_data.py  embed-verified video room. Raises if empty.
  build.py        driver: renders pages, sitemap, robots, llms.txt, llms-full.txt
  make_assets.py  favicons, apple-touch-icon, 1200x630 og.png
site/           build output. This is what Cloudflare Pages serves.
tools/gate.py   the gate. exit 0 clean, 1 findings, 2 gate could not run.
```

## Build and check locally

```bash
python3 build/make_assets.py
python3 build/build.py --out site
python3 tools/gate.py --site site
python3 tools/serve.py          # http://localhost:8000 — clean URLs, like production
```

Use `tools/serve.py`, not `python3 -m http.server`: the site uses clean URLs (`/events`,
not `/events.html`). Cloudflare Pages resolves those in production; a plain file server
does not, so every nav and footer link 404s under it.

`tools/gate.py` is fail-closed and will be wired into CI ahead of the deploy.
A check that measures zero items exits 2 rather than passing.

## Rules this site holds itself to

1. **Nothing local is published unverified.** `build/listings.py` starts empty on
   purpose. An empty list renders an honest paragraph telling the reader where the
   answer actually lives, never a placeholder. No fabricated jams, teachers,
   venues, dates or reviews.
2. **Nothing is copied.** All prose is written for this site. Quotations are short,
   attributed and cited on the page.
3. **Videos are embedded, never re-hosted.** Every entry in `videos_data.py` was
   verified against the YouTube oEmbed endpoint (HTTP 200) before being added.
   Nothing is downloaded or re-cut.
4. **No ranking claims.** No self-ranked "best in Miami" lists, no area x topic
   page matrix (that is what Google calls scaled content abuse), no fake address or
   fake Google Business Profile. Geography is expressed through schema `areaServed`
   and content, not through invented premises.
5. **Raster assets only.** SVG favicons and SVG og:images are ignored by crawlers;
   the gate enforces PNG at the right pixel dimensions.

## AEO / discovery surface

- `robots.txt` names the answer-engine crawlers explicitly and points at the sitemap.
- `llms.txt` and `llms-full.txt` are generated from the same source as the pages, so
  they cannot drift.
- Every page emits exactly one JSON-LD `@graph`: `Organization`, `WebSite`,
  `WebPage`, `BreadcrumbList`, plus page-specific `FAQPage`, `DefinedTermSet`,
  `ItemList`, `Place` or `VideoObject`.
- Every page has one `h1`, one canonical, a 1200x630 og:image and an
  answer-first block near the top.

## Adding a page

1. Add the builder to the right `content_*.py` module.
2. Add a row to `PAGES` in `build/build.py` (route, filename, builder, priority,
   changefreq, background video id).
3. If the page has a new nav destination, edit `NAV` in `build/shell.py`.
4. Rebuild and run the gate. A new page that is not in `PAGES` is not in the
   sitemap, and the gate fails on that.

## Adding a listing

Edit `build/listings.py`. Each entry is a tuple with a `verified` date. Open the
organiser's own page before adding it. Removing a dead entry is a normal change.

## Adding a video

Verify first, then add:

```bash
curl -s -o /dev/null -w '%{http_code}\n' \
  "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<ID>&format=json"
```

200 means embeddable. Anything else means do not add it.

## Deploying

Push to `main`. `.github/workflows/publish.yml` builds, gates, deploys to Cloudflare
Pages project `miamicontactimprov`, verifies the custom domain serves the new build,
then pings IndexNow. The gates and the deploy are in one job on purpose: a red gate
must abort the deploy, not run beside it.
