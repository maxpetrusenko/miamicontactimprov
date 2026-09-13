#!/usr/bin/env python3
"""Site gates for miamicontactimprov.com.

Exit codes (fixed contract, no workflow special-cases any of them):
  0  no error-band findings
  1  at least one error-band finding
  2  the gate itself could not run (missing surface, zero pages measured,
     malformed config, or a crash)

A check that measures nothing is a failure, never a pass. Every check asserts a
non-zero measured count and exits 2 if the count is zero.

Usage:  python3 tools/gate.py [--site site] [--report-only]
"""

import argparse
import json
import pathlib
import re
import sys
from collections import Counter

ERROR, WARN, INFO = "error", "warn", "info"
findings = []          # (band, check, page, message)
counts = {}


def add(band, check, page, message):
    findings.append((band, check, page, message))


def measured(name, n):
    counts[name] = n
    if n == 0:
        add(ERROR, "measurement", "-",
            f"check '{name}' measured 0 items; a check that verifies nothing must not be green")
        raise SystemExit(2)


# ---------------------------------------------------------------- html structure
BLOCK_IN_HEADING = re.compile(
    r"<h([1-6])\b[^>]*>(?:(?!</h\1>).)*?<(p|div|ul|ol|section|article|table|blockquote)\b",
    re.S | re.I,
)
HEADING_OPEN = re.compile(r"<h([1-6])\b", re.I)
HEADING_CLOSE = re.compile(r"</h([1-6])>", re.I)
P_IN_P = re.compile(r"<p\b[^>]*>(?:(?!</p>).)*?<p\b", re.S | re.I)


def check_html_structure(pages):
    n = 0
    for page, src in pages.items():
        n += 1
        for m in BLOCK_IN_HEADING.finditer(src):
            add(ERROR, "html-structure", page,
                f"block element <{m.group(2)}> nested inside <h{m.group(1)}> "
                f"- the whole block inherits the heading's styling")
        opens = Counter(HEADING_OPEN.findall(src))
        closes = Counter(HEADING_CLOSE.findall(src))
        for lvl in sorted(set(opens) | set(closes)):
            if opens[lvl] != closes[lvl]:
                add(ERROR, "html-structure", page,
                    f"<h{lvl}> opened {opens[lvl]} times, closed {closes[lvl]} times")
        for _ in P_IN_P.finditer(src):
            add(ERROR, "html-structure", page, "<p> nested inside <p>")
    measured("html-structure.pages", n)


# ---------------------------------------------------------------- json-ld
REQUIRED = {
    "Organization": ["name", "url", "description"],
    "WebSite": ["url", "name"],
    "WebPage": ["url", "name", "description", "isPartOf"],
    "BreadcrumbList": ["itemListElement"],
    "FAQPage": ["mainEntity"],
    "DefinedTermSet": ["name", "hasDefinedTerm"],
    "ItemList": ["name", "itemListElement", "numberOfItems"],
    "Place": ["name"],
    "VideoObject": ["name", "thumbnailUrl", "embedUrl"],
    "Event": ["name", "startDate", "location", "eventStatus"],
    "Course": ["name", "description", "provider"],
    "CourseInstance": ["courseMode", "location"],
    "Schedule": ["byDay", "startTime"],
    "ListItem": ["position"],
    "Question": ["name", "acceptedAnswer"],
    "DefinedTerm": ["name", "description"],
}
LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)

# Types that a single page must define at most once. Everything else may repeat.
SINGLETON_TYPES = {
    "Organization", "WebSite", "WebPage", "BreadcrumbList", "FAQPage",
    "DefinedTermSet", "Place", "Course",
}


def check_jsonld(pages):
    total_nodes = 0
    for page, src in pages.items():
        blocks = LD_RE.findall(src)
        if not blocks:
            add(ERROR, "json-ld", page, "no application/ld+json block")
            continue
        if len(blocks) != 1:
            add(WARN, "json-ld", page, f"{len(blocks)} ld+json blocks (one @graph is simpler to audit)")
        for raw in blocks:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                add(ERROR, "json-ld", page, f"invalid JSON: {exc}")
                continue
            if data.get("@context") != "https://schema.org":
                add(ERROR, "json-ld", page, "missing or wrong @context")
            nodes = data.get("@graph") or [data]
            seen = Counter()
            for node in nodes:
                t = node.get("@type")
                total_nodes += 1
                if not t:
                    add(ERROR, "json-ld", page, "node without @type")
                    continue
                seen[t] += 1
                for prop in REQUIRED.get(t, []):
                    if prop not in node:
                        add(ERROR, "json-ld", page, f"{t} missing required property '{prop}'")
            for t, c in seen.items():
                # Only true singletons. A page may legitimately list many Events,
                # ListItems, VideoObjects, Questions or DefinedTerms.
                if c > 1 and t in SINGLETON_TYPES:
                    add(ERROR, "json-ld", page, f"{t} defined {c} times in one graph")
        if '"@type": "Organization"' not in src:
            add(ERROR, "json-ld", page, "no Organization node")
    measured("json-ld.pages", len(pages))
    measured("json-ld.nodes", total_nodes)


# ---------------------------------------------------------------- seo
PLACEHOLDERS = [
    r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"\bXXX\b", r"lorem ipsum",
    r"Replace with", r"\bFirst name\b", r"\bLast name\b", r"YYYY-MM-DD",
    r"2026-MM-DD", r"\bplaceholder\b", r"\bLorem\b", r"\[insert",
]
PLACE_RE = re.compile("|".join(PLACEHOLDERS), re.I)
CANON_RE = re.compile(r'<link rel="canonical" href="([^"]+)">')
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)">')
H1_RE = re.compile(r"<h1\b")
SITEMAP_LOC_RE = re.compile(r"<loc>(.*?)</loc>")


def check_seo(pages, site_dir, canonicals_seen):
    for page, src in pages.items():
        if PLACE_RE.search(src):
            hits = sorted({m.group(0) for m in PLACE_RE.finditer(src)})
            add(ERROR, "seo", page, f"placeholder text in markup: {hits}")
        t = TITLE_RE.search(src)
        d = DESC_RE.search(src)
        if not t:
            add(ERROR, "seo", page, "no <title>")
        else:
            title = t.group(1).strip()
            if not 15 <= len(title) <= 75:
                add(WARN, "seo", page, f"title length {len(title)} (aim 15-75)")
        if not d:
            add(ERROR, "seo", page, "no meta description")
        else:
            desc = d.group(1).strip()
            if not 50 <= len(desc) <= 175:
                add(WARN, "seo", page, f"meta description length {len(desc)} (aim 50-175)")
        n_h1 = len(H1_RE.findall(src))
        if n_h1 != 1:
            add(ERROR, "seo", page, f"{n_h1} <h1> elements (exactly one required)")
        canons = CANON_RE.findall(src)
        if len(canons) != 1:
            add(ERROR, "seo", page, f"{len(canons)} canonical links (exactly one required)")
        for c in canons:
            canonicals_seen[(page, c)] = True
            if not c.startswith("https://miamicontactimprov.com"):
                add(ERROR, "seo", page, f"canonical points off the canonical host: {c}")
        if "www.miamicontactimprov.com" in src:
            add(ERROR, "seo", page, "references the www host, which is not canonical")
    measured("seo.pages", len(pages))


def check_sitemap(site_dir, pages):
    sm = (site_dir / "sitemap.xml").read_text(encoding="utf-8")
    locs = SITEMAP_LOC_RE.findall(sm)
    measured("sitemap.urls", len(locs))
    if len(set(locs)) != len(locs):
        add(ERROR, "sitemap", "sitemap.xml", "duplicate <loc> entries")
    page_urls = {CANON_RE.search(s).group(1) for s in pages.values() if CANON_RE.search(s)}
    page_urls.discard("https://miamicontactimprov.com/404")
    missing = page_urls - set(locs)
    extra = set(locs) - page_urls
    for u in sorted(missing):
        add(ERROR, "sitemap", "sitemap.xml", f"page not in sitemap: {u}")
    for u in sorted(extra):
        add(ERROR, "sitemap", "sitemap.xml", f"sitemap entry has no page: {u}")


# ---------------------------------------------------------------- internal links
HREF_RE = re.compile(r'href="(/[^"#?]*)"')


def check_links(pages, site_dir):
    n = 0
    for page, src in pages.items():
        for href in HREF_RE.findall(src):
            n += 1
            target = href.lstrip("/")
            if not target:
                continue
            candidates = [
                site_dir / target,
                site_dir / (target + ".html"),
                site_dir / target / "index.html",
            ]
            if not any(c.is_file() for c in candidates):
                add(ERROR, "links", page, f"internal link target missing from the build: {href}")
    measured("links.internal", n)


# ---------------------------------------------------------------- required files
REQUIRED_FILES = ["robots.txt", "sitemap.xml", "llms.txt", "llms-full.txt",
                  "_headers", "404.html", "assets/site.css", "assets/og.png"]


def check_files(site_dir):
    for rel in REQUIRED_FILES:
        p = site_dir / rel
        if not p.is_file() or p.stat().st_size == 0:
            add(ERROR, "files", rel, "required discovery file missing or empty")
    measured("files.checked", len(REQUIRED_FILES))

    robots = (site_dir / "robots.txt").read_text(encoding="utf-8")
    for agent in ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "OAI-SearchBot"]:
        if agent not in robots:
            add(WARN, "files", "robots.txt", f"{agent} not named in robots.txt")
    if "Sitemap:" not in robots:
        add(ERROR, "files", "robots.txt", "no Sitemap directive")
    if re.search(r"^Disallow: /\s*$", robots, re.M):
        add(ERROR, "files", "robots.txt", "a blanket Disallow blocks every crawler")


def check_canonical_forms(site_dir, pages):
    """Every page must exist at exactly one URL. The .html form 301s to the clean form.

    Only real rules count. The first version of this check substring-matched the whole
    file, so a comment mentioning the path satisfied it and the gate lied green.
    """
    red = (site_dir / "_redirects").read_text(encoding="utf-8")
    rules = [ln.strip() for ln in red.splitlines()
             if ln.strip() and not ln.strip().startswith("#")]
    measured("redirects.rules", len(rules))
    if len(rules) < 2:
        add(ERROR, "canonical", "_redirects",
            "too few redirect rules; a second reachable URL per page is duplicate content")
    sources = set(rules)
    for name in pages:
        if name in ("index.html", "404.html"):
            continue
        needle = f"/{name}"
        if not any(r.split()[0] == needle for r in rules if r.split()):
            add(ERROR, "canonical", "_redirects",
                f"{name} is reachable at two URLs; no rule collapses it")
    if not sources:
        add(ERROR, "canonical", "_redirects", "no redirect rules parsed")


def check_assets(site_dir):
    """favicon and og:image must be raster at the right size."""
    try:
        from PIL import Image
    except ImportError:
        add(ERROR, "assets", "-", "Pillow missing; cannot verify raster asset geometry")
        return
    og = site_dir / "assets" / "og.png"
    if og.is_file():
        w, h = Image.open(og).size
        if (w, h) != (1200, 630):
            add(ERROR, "assets", "assets/og.png", f"og:image is {w}x{h}, must be 1200x630")
    else:
        add(ERROR, "assets", "assets/og.png", "og:image missing")
    for s in (16, 32, 48, 96):
        f = site_dir / "assets" / f"favicon-{s}.png"
        if not f.is_file():
            add(ERROR, "assets", f"assets/favicon-{s}.png", "missing raster favicon")
        elif Image.open(f).size != (s, s):
            add(ERROR, "assets", f"assets/favicon-{s}.png", "wrong pixel dimensions")
    svg = list((site_dir / "assets").glob("*.svg"))
    for p in svg:
        if "favicon" in p.name or "og" in p.name:
            add(ERROR, "assets", str(p.name), "SVG favicon / og:image is ignored by crawlers")
    measured("assets.raster_checked", 6)


# ---------------------------------------------------------------- aria / a11y basics
def check_a11y(pages):
    n = 0
    for page, src in pages.items():
        n += 1
        if 'lang="en"' not in src:
            add(ERROR, "a11y", page, "no lang attribute on <html>")
        if 'name="viewport"' not in src:
            add(ERROR, "a11y", page, "no viewport meta")
        if "<main" not in src:
            add(ERROR, "a11y", page, "no <main> landmark")
        if 'aria-label="Primary"' not in src:
            add(ERROR, "a11y", page, "primary nav has no accessible name")
        for m in re.finditer(r"<img\b[^>]*>", src):
            tag = m.group(0)
            if "alt=" not in tag:
                add(ERROR, "a11y", page, f"<img> without alt: {tag[:70]}")
        for m in re.finditer(r"<iframe\b[^>]*>", src):
            tag = m.group(0)
            if 'title="' not in tag:
                add(WARN, "a11y", page, f"<iframe> without title: {tag[:70]}")
    measured("a11y.pages", n)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="site")
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    site_dir = pathlib.Path(args.site).resolve()
    if not site_dir.is_dir():
        print(f"site directory not found: {site_dir}", file=sys.stderr)
        return 2
    html_files = sorted(site_dir.glob("*.html"))
    if not html_files:
        print(f"no html files in {site_dir}", file=sys.stderr)
        return 2
    pages = {p.name: p.read_text(encoding="utf-8") for p in html_files}
    measured("pages.rendered", len(pages))

    check_html_structure(pages)
    check_jsonld(pages)
    check_seo(pages, site_dir, {})
    check_sitemap(site_dir, pages)
    check_links(pages, site_dir)
    check_files(site_dir)
    check_canonical_forms(site_dir, pages)
    check_assets(site_dir)
    check_a11y(pages)

    bands = Counter(b for b, *_ in findings)
    if not args.quiet:
        for band, check, page, msg in findings:
            print(f"[{'E' if band == ERROR else 'W' if band == WARN else 'I'}] {check:16} {page:38} {msg}")
        print()
        print("measured:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        print(f"findings: error={bands[ERROR]} warn={bands[WARN]} info={bands[INFO]}")

    if args.report_only:
        print("report-only: not failing the run")
        return 0
    return 1 if bands[ERROR] else 0


if __name__ == "__main__":
    # A crash is a broken validator, not a finding. Exit 2 so it can never be
    # mistaken for the exit-1 findings band.
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        print(f"\ngate could not run: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)
