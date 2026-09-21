#!/usr/bin/env python3
"""Render miamicontactimprov.com into site/.

Usage:  python3 build/build.py [--out site]

Every page is a (slug, locale) pair. The slug is locale-independent; build/locales.py
owns which route that slug has in each locale, and therefore the hreflang pairing and
the sitemap entry. A locale a slug does not have is never written, never listed and
never advertised to a crawler.
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
import content_es  # noqa: E402
import content_local  # noqa: E402
import content_blog  # noqa: E402
import content_marketing  # noqa: E402
import content_practice  # noqa: E402
import locales  # noqa: E402
import schema  # noqa: E402
import shell  # noqa: E402
import videos_data  # noqa: E402

SITE = shell.SITE
def _sitemap_lastmod():
    """The sitemap's lastmod: when this site's content last changed.

    This was `TODAY = "2026-09-14"`, a literal somebody bumped by hand. Two commits landed on
    2026-09-19 -- the Event/offer `validFrom` fix and the gate change -- the pages went live, and
    every URL still advertised 2026-09-14, so the one mechanical freshness signal Google has said
    nothing had changed. Derived from git so it cannot rot; falls back to today when the build has
    no history (an exported tarball), which is still true -- the build is happening now.
    """
    import datetime as _dt
    import os as _os
    import subprocess as _sp
    here = _os.path.dirname(_os.path.abspath(__file__))
    for cmd in (["git", "log", "-1", "--format=%cs", "--", here],
                ["git", "log", "-1", "--format=%cs"]):
        try:
            r = _sp.run(cmd, cwd=here, capture_output=True, text=True, timeout=10)
        except (OSError, _sp.SubprocessError):
            break
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    return _dt.date.today().isoformat()


TODAY = _sitemap_lastmod()

# slug, locale, builder, sitemap priority, changefreq, background video id
PAGES = [
    ("home", "en", content_marketing.home, "1.0", "weekly", None),
    ("what-is-contact-improvisation", "en", content_core.what_is, "0.9", "monthly", None),
    ("miami", "en", content_directory.miami, "0.9", "weekly", None),
    ("miami-jams", "en", content_local.miami_jams, "0.9", "weekly", None),
    ("jams", "en", content_practice.jams, "0.8", "weekly", None),
    ("friday-jam", "en", content_practice.friday_jam, "0.9", "weekly", None),
    ("classes", "en", content_practice.classes, "0.8", "monthly", None),
    ("your-first-jam", "en", content_practice.your_first_jam, "0.8", "monthly", None),
    ("keep-practising", "en", content_practice.keep_practising, "0.7", "monthly", None),
    ("videos", "en", content_practice.videos, "0.7", "monthly", None),
    ("directory", "en", content_directory.directory, "0.7", "weekly", None),
    ("glossary", "en", content_core.glossary, "0.6", "monthly", None),
    ("history", "en", content_core.history, "0.6", "yearly", None),
    ("safety-and-consent", "en", content_practice.safety, "0.6", "yearly", None),
    ("faq", "en", content_directory.faq, "0.7", "monthly", None),
    ("about", "en", content_marketing.about, "0.5", "yearly", None),
    ("events", "en", content_marketing.events, "0.9", "weekly", None),
    ("contact", "en", content_marketing.contact, "0.6", "monthly", None),
    ("blog", "en", content_blog.index, "0.7", "weekly", None),
    ("blog-first-jam", "en", content_blog.first_jam, "0.6", "monthly", None),
    ("blog-weight-sharing", "en", content_blog.weight_sharing, "0.6", "monthly", None),
    ("blog-falling", "en", content_blog.falling, "0.6", "monthly", None),
    ("blog-consent", "en", content_blog.consent, "0.6", "monthly", None),
    ("blog-no-music", "en", content_blog.no_music, "0.6", "monthly", None),
    # Spanish. Same slug, second locale: each of these is a first-class route with its
    # own canonical, its own sitemap entry and its own side of the hreflang pair.
    ("home", "es", content_es.home, "1.0", "weekly", None),
    ("what-is-contact-improvisation", "es", content_es.what_is, "0.9", "monthly", None),
    ("miami", "es", content_es.miami, "0.9", "weekly", None),
    ("miami-jams", "es", content_es.miami_jams, "0.8", "weekly", None),
    ("jams", "es", content_es.jams, "0.7", "weekly", None),
    ("friday-jam", "es", content_es.friday_jam, "0.8", "weekly", None),
    ("classes", "es", content_es.classes, "0.7", "monthly", None),
    ("your-first-jam", "es", content_es.your_first_jam, "0.7", "monthly", None),
    ("keep-practising", "es", content_es.keep_practising, "0.6", "monthly", None),
    ("videos", "es", content_es.videos, "0.6", "monthly", None),
    ("directory", "es", content_es.directory, "0.6", "weekly", None),
    ("glossary", "es", content_es.glossary, "0.5", "monthly", None),
    ("history", "es", content_es.history, "0.5", "yearly", None),
    ("safety-and-consent", "es", content_es.safety, "0.6", "yearly", None),
    ("faq", "es", content_es.faq, "0.6", "monthly", None),
    ("about", "es", content_es.about, "0.4", "yearly", None),
]

ROW_FIELDS = ("slug", "lang", "route", "filename", "builder", "priority", "changefreq", "bg")


def check_tables_agree():
    """The two tables that define this site must not drift.

    build/locales.py says which route a page has in which language; PAGES says which
    builder writes it and in what order. A row in one and not the other is either a page
    with no URL or a URL with no page, so the build stops rather than guessing.
    """
    declared = {(slug, lang) for slug, lang, *_rest in PAGES}
    known = {(slug, lang) for slug, lang in locales.ORDER}
    missing_route = declared - known
    missing_builder = known - declared
    problems = []
    for slug, lang in sorted(missing_route):
        problems.append(f"PAGES has ({slug}, {lang}) but locales.ORDER has no such row")
    for slug, lang in sorted(missing_builder):
        problems.append(f"locales.ORDER has ({slug}, {lang}) but PAGES has no builder")
    for slug, lang, *_rest in PAGES:
        if not locales.route(slug, lang):
            problems.append(f"locales.ROUTES has no route for ({slug}, {lang})")
    if problems:
        raise SystemExit("i18n table drift:\n  " + "\n  ".join(problems))
    seen = {}
    for slug, lang, *_rest in PAGES:
        filename = locales.filename_for(locales.route(slug, lang))
        if filename in seen:
            raise SystemExit(f"two pages write {filename}: {seen[filename]} and ({slug}, {lang})")
        seen[filename] = f"({slug}, {lang})"


def rows():
    """Yield one dict per page: the single place a page's URL and file are decided."""
    check_tables_agree()
    for slug, lang, builder, prio, freq, bg in PAGES:
        route = locales.route(slug, lang)
        yield {
            "slug": slug, "lang": lang, "route": route,
            "filename": locales.filename_for(route),
            "builder": builder, "priority": prio, "changefreq": freq, "bg": bg,
        }


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

/assets/*
  Cache-Control: public, max-age=604800

/assets/site.css
  Cache-Control: public, max-age=0, must-revalidate

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/llms.txt
  Content-Type: text/plain; charset=utf-8
  Cache-Control: public, max-age=3600
"""

REDIRECT_ALIASES = """# Clean-URL safety net. Cloudflare Pages serves /miami.html at /miami, but the
# .html form is still reachable, which is a second URL for the same page. These
# collapse it. Generated per page below, plus the hand-written aliases.
/what-is-ci                 /what-is-contact-improvisation    301
/contact-improvisation      /what-is-contact-improvisation    301
/contact-improvisation-miami /miami                           301
/safety                     /safety-and-consent               301
/teachers                   /directory                        301
"""


def redirects_file():
    lines = [
        "# Generated by build/build.py. Do not hand-edit: edits are lost on the next build.",
        "# One URL per page. The .html form 301s to the clean form.",
        "",
    ]
    for row in rows():
        if row["filename"] == "index.html":
            continue
        lines.append(f"/{row['filename']}  {row['route']}  301")
        if row["filename"].endswith(".html") and not row["filename"].endswith("index.html"):
            stem = row["filename"][:-5]
            lines.append(f"/{stem}/index.html  {row['route']}  301")
            lines.append(f"/{stem}/  {row['route']}  301")
    # A locale directory is reachable with and without its trailing slash. Collapse it,
    # the same way the .html form is collapsed, rather than serving two URLs per page.
    for lang in locales.LOCALES:
        if lang == locales.DEFAULT:
            continue
        home = locales.route("home", lang)
        if home and home != "/":
            lines.append(f"{home.rstrip('/')}  {home}  301")
    lines.append("")
    lines.append(REDIRECT_ALIASES.rstrip())
    lines.append("")
    return "\n".join(lines)


def build(out_dir: pathlib.Path, base_url=None):
    site = SITE if not base_url else base_url.rstrip("/")
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    page_rows = list(rows())
    for row in page_rows:
        out_path = out_dir / row["filename"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        body = row["builder"]()
        if base_url:
            body = body.replace(SITE, site)
        out_path.write_text(body, encoding="utf-8")
        written.append(row["filename"])
        # Clean-URL fallback for plain file servers (python -m http.server, S3, a USB
        # stick): /events -> 301 -> /events/ -> events/index.html. Production never
        # serves the copy, because _redirects collapses /events/ to /events first.
        if row["filename"].endswith(".html") and not row["filename"].endswith("index.html"):
            alias = out_dir / row["filename"][:-5] / "index.html"
            alias.parent.mkdir(parents=True, exist_ok=True)
            alias.write_text(body, encoding="utf-8")
            written.append(alias.relative_to(out_dir).as_posix())

    # 404. One document, served for every locale: the Spanish pages are translations of
    # pages that exist, and a missing URL is missing in both languages.
    (out_dir / "404.html").write_text(
        content_directory.not_found().replace(SITE, site) if base_url
        else content_directory.not_found(),
        encoding="utf-8",
    )
    written.append("404.html")

    # sitemap
    sitemap_rows = []
    for row in page_rows:
        loc = site + row["route"]
        sitemap_rows.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
            f"    <changefreq>{row['changefreq']}</changefreq>\n"
            f"    <priority>{row['priority']}</priority>\n  </url>"
        )
    (out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(sitemap_rows)
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    written.append("sitemap.xml")

    (out_dir / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (out_dir / "_headers").write_text(HEADERS, encoding="utf-8")
    (out_dir / "_redirects").write_text(redirects_file(), encoding="utf-8")
    written += ["robots.txt", "_headers", "_redirects"]

    (out_dir / "llms.txt").write_text(llms_txt(site), encoding="utf-8")
    (out_dir / "llms-full.txt").write_text(llms_full(site), encoding="utf-8")
    written += ["llms.txt", "llms-full.txt"]

    return written


# ------------------------------------------------------------------ llms.txt

LLMS_INTRO = (
    # Line 1 of llms.txt carries the entity disambiguation, so an answer engine
    # reading only the top of the file cannot mistake this site for a studio, a
    # paid directory, or for miamiimprov.com (a comedy theatre).
    "Miami Contact Improv is " + schema.DISAMBIGUATION + " and is not affiliated with "
    "miamiimprov.com, the comedy theatre that dominates search for the bare word 'improv'.\n"
    "It is an independent, non-commercial community resource that maps "
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
    "Miami Contact Improv hosts a weekly class followed by an open jam every Friday, 7:00 to 9:00 PM, at Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009, from 2 October 2026. $20 at the door on a $20 to $50 sliding scale; no partner, experience or booking needed.",
]

LOCALE_NOTE = (
    "The library pages are published in both English and Spanish; the Events, Contact and Blog pages are English only. The "
    "Spanish pages under /es/ are translations of their English counterparts and make no "
    "claim the English page does not make; a page is never machine-translated, and a page "
    "that is not translated is absent from /es/ rather than generated. The English page is "
    "the x-default of every pair."
)


def _page_index(site):
    lines = []
    for row in rows():
        lines.append(f"- {site}{row['route']}  ({row['lang']})")
    return "\n".join(lines)


def llms_txt(site):
    facts = "\n".join(f"- {f}" for f in KEY_FACTS)
    return f"""# Miami Contact Improv

> {LLMS_INTRO}

## Languages

{LOCALE_NOTE}

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
        "## Languages",
        "",
        LOCALE_NOTE,
        "",
        "## Key facts",
        "",
        "\n".join(f"- {f}" for f in KEY_FACTS),
        "",
    ]
    for row in rows():
        html_src = (pathlib.Path(OUT_DIR) / row["filename"]).read_text(encoding="utf-8")
        parts.append(f"\n---\n\n## {site}{row['route']}\n")
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
