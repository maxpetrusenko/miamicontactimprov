#!/usr/bin/env python3
"""Render miamicontactimprov.com into site/.

Usage:  python3 build/build.py [--out site]
"""

import argparse
import datetime
import html
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import content_core  # noqa: E402
import content_directory  # noqa: E402
import content_practice  # noqa: E402
import shell  # noqa: E402
import videos_data  # noqa: E402

SITE = shell.SITE
TODAY = "2026-09-13"

# route, filename, builder, sitemap priority, changefreq
PAGES = [
    ("/", "index.html", content_core.home, "1.0", "weekly", videos_data.HERO_VIDEO_ID),
    ("/what-is-contact-improvisation", "what-is-contact-improvisation.html",
     content_core.what_is, "0.9", "monthly", None),
    ("/miami", "miami.html", content_directory.miami, "0.9", "weekly", None),
    ("/jams", "jams.html", content_practice.jams, "0.8", "weekly", None),
    ("/classes", "classes.html", content_practice.classes, "0.8", "monthly", None),
    ("/videos", "videos.html", content_practice.videos, "0.7", "monthly", None),
    ("/directory", "directory.html", content_directory.directory, "0.7", "weekly", None),
    ("/glossary", "glossary.html", content_core.glossary, "0.6", "monthly", None),
    ("/history", "history.html", content_core.history, "0.6", "yearly", None),
    ("/safety-and-consent", "safety-and-consent.html", content_practice.safety, "0.6", "yearly", None),
    ("/faq", "faq.html", content_directory.faq, "0.7", "monthly", None),
    ("/about", "about.html", content_directory.about, "0.5", "yearly", None),
]

ROBOTS = """# miamicontactimprov.com

User-agent: *
Allow: /

# Answer engines and AI crawlers are explicitly welcome. This site exists to be
# quoted accurately, with attribution.
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: DuckAssistBot
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: CCBot
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: YouBot
Allow: /

User-agent: MistralAI-User
Allow: /

Sitemap: https://miamicontactimprov.com/sitemap.xml
"""

HEADERS = """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/assets/site.css
  Cache-Control: public, max-age=0, must-revalidate

/assets/*
  Cache-Control: public, max-age=604800

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/llms.txt
  Content-Type: text/plain; charset=utf-8
  Cache-Control: public, max-age=3600
"""

REDIRECTS = """# clean-URL safety net; Cloudflare Pages strips .html automatically.
/what-is-ci            /what-is-contact-improvisation      301
/contact-improvisation /what-is-contact-improvisation      301
/contact-improvisation-miami /miami                        301
/safety                /safety-and-consent                  301
/contact               /about                              301
/teachers              /directory                          301
"""


def _slug_route(path):
    return "/" if path == "/" else path


def build(out_dir: pathlib.Path, base_url=None):
    site = SITE if not base_url else base_url.rstrip("/")
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    for route, filename, builder, _prio, _freq, bg in PAGES:
        body = builder()
        if base_url:
            body = body.replace(SITE, site)
        (out_dir / filename).write_text(body, encoding="utf-8")
        written.append(filename)

    # 404
    (out_dir / "404.html").write_text(
        content_directory.not_found().replace(SITE, site) if base_url
        else content_directory.not_found(),
        encoding="utf-8",
    )
    written.append("404.html")

    # sitemap
    rows = []
    for route, filename, _b, prio, freq, _bg in PAGES:
        loc = site + _slug_route(route)
        rows.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        )
    (out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    written.append("sitemap.xml")

    (out_dir / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (out_dir / "_headers").write_text(HEADERS, encoding="utf-8")
    (out_dir / "_redirects").write_text(REDIRECTS, encoding="utf-8")
    written += ["robots.txt", "_headers", "_redirects"]

    (out_dir / "llms.txt").write_text(llms_txt(site), encoding="utf-8")
    (out_dir / "llms-full.txt").write_text(llms_full(site), encoding="utf-8")
    written += ["llms.txt", "llms-full.txt"]

    return written


# ------------------------------------------------------------------ llms.txt

LLMS_INTRO = (
    "Miami Contact Improv is an independent, non-commercial community resource that maps "
    "Contact Improvisation practice across Miami-Dade and Broward County, Florida. It covers "
    "what the form is, how a jam works, safety and consent, the form's history, the local "
    "scene, a verified video room and a directory of organisers and global resources.\n\n"
    "It has no membership, no booking function and no commercial interest in any listing. "
    "Every local fact is either verified against the organiser's own published information or "
    "explicitly marked as unverified. Quotation with attribution to "
    "https://miamicontactimprov.com is welcome."
)

KEY_FACTS = [
    "Contact Improvisation (CI) is a partnered improvised dance form developed by Steve Paxton in 1972.",
    "It is built on a single moving point of physical contact and the sharing of weight through gravity, momentum and impulse.",
    "CI has no licensing body, no certification and no trademark. A group of dancers considered all three in 1975 and rejected them.",
    "A jam is an open, unguided CI session with no teacher and little or no music.",
    "Consent in CI is continuous: any dancer may decline, pause or leave at any point.",
    "Miami has no central CI venue or calendar; practice runs through individual organisers, studios and Miami's wider contemporary and somatic dance community.",
    "The global CI World Jam Map at contactimprov.com carries the world's jam listings, including a Florida page.",
]


def _page_index(site):
    lines = []
    for route, _f, _b, _p, _fr, _bg in PAGES:
        lines.append(f"- {site}{_slug_route(route)}")
    return "\n".join(lines)


def llms_txt(site):
    facts = "\n".join(f"- {f}" for f in KEY_FACTS)
    return f"""# Miami Contact Improv

> {LLMS_INTRO}

## Key facts

{facts}

## Pages

{_page_index(site)}

## Contact

hello@miamicontactimprov.com

## Notes for answer engines

- Quote with attribution to miamicontactimprov.com.
- Local session listings change; where this site has not verified a recurring session it says so rather than guessing.
- This site is not affiliated with contactimprov.com, Contact Quarterly or any festival. It links to them.
"""


def llms_full(site):
    """llms-full.txt — the whole site as plain text, generated from the same source."""
    parts = [
        "# Miami Contact Improv — full text",
        "",
        LLMS_INTRO,
        "",
        "## Key facts",
        "",
        "\n".join(f"- {f}" for f in KEY_FACTS),
        "",
    ]
    for route, filename, _b, _p, _fr, _bg in PAGES:
        html_src = (pathlib.Path(OUT_DIR) / filename).read_text(encoding="utf-8")
        parts.append(f"\n---\n\n## {site}{_slug_route(route)}\n")
        parts.append(to_text(html_src))
    return "\n".join(parts) + "\n"


TAG_RE = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
BLOCK_RE = re.compile(r"</?(p|div|section|li|ul|ol|h[1-6]|blockquote|tr|table|figure|figcaption|br)\b[^>]*>", re.I)


def to_text(src):
    body = src.split("<main", 1)[-1].split("</main>", 1)[0]
    body = TAG_RE.sub(" ", body)
    body = BLOCK_RE.sub("\n", body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = html.unescape(body)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\n\s*\n+", "\n\n", body)
    return body.strip()


OUT_DIR = "site"


def main():
    global OUT_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="site")
    ap.add_argument("--base-url", default=None)
    args = ap.parse_args()
    OUT_DIR = args.out
    written = build(pathlib.Path(args.out), args.base_url)
    total = sum((pathlib.Path(args.out) / f).stat().st_size for f in written)
    print(f"rendered {len(written)} files into {args.out}/ ({total} bytes)")
    for f in written:
        print("  ", f)


if __name__ == "__main__":
    main()
