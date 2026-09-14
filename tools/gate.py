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
    "VideoObject": ["name", "thumbnailUrl"],
    "Event": ["name", "startDate", "location", "eventStatus"],
    "Course": ["name", "description", "provider"],
    "CourseInstance": ["courseMode", "location"],
    "Schedule": ["byDay", "startTime"],
    "ListItem": ["position"],
    "Question": ["name", "acceptedAnswer"],
    "DefinedTerm": ["name", "description"],
}

# A video plays from somewhere. Someone else's film is embedded from the platform
# that hosts it (embedUrl); a film this site made and hosts is served from here
# (contentUrl). Either satisfies the requirement, and check_video_room decides which
# one carries the credit.
REQUIRED_ANY = {
    "VideoObject": [("embedUrl", "contentUrl")],
}

LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)

# Nodes that live under a container key rather than at the top of @graph. Without
# walking these, REQUIRED["VideoObject"] and REQUIRED["ListItem"] applied to nothing
# at all: the VideoObjects sit in ItemList.itemListElement[].item, so the check was
# green while measuring nothing.
NESTED_KEYS = ("itemListElement", "item", "mainEntity", "hasDefinedTerm")


def _nested_typed_nodes(obj, out):
    """Collect typed nodes reachable under a container key."""
    if isinstance(obj, list):
        for item in obj:
            _nested_typed_nodes(item, out)
        return
    if not isinstance(obj, dict):
        return
    if obj.get("@type"):
        out.append(obj)
    for key in NESTED_KEYS:
        value = obj.get(key)
        if isinstance(value, (dict, list)):
            _nested_typed_nodes(value, out)


# Types that a single page must define at most once. Everything else may repeat.
SINGLETON_TYPES = {
    "Organization", "WebSite", "WebPage", "BreadcrumbList", "FAQPage",
    "DefinedTermSet", "Place", "Course",
}


def check_jsonld(pages):
    total_nodes = 0
    nested_nodes = 0
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
                for group in REQUIRED_ANY.get(t, []):
                    if not any(prop in node for prop in group):
                        add(ERROR, "json-ld", page,
                            f"{t} has none of {' / '.join(group)}: it does not say where the video plays")
                # The same rules apply to typed nodes nested in a container
                # (ItemList.itemListElement[].item, FAQPage.mainEntity, a
                # DefinedTermSet's terms). They are what the room is actually built
                # from, so they are measured rather than assumed.
                nested = []
                _nested_typed_nodes(node, nested)
                for child in nested:
                    nt = child.get("@type")
                    nested_nodes += 1
                    for prop in REQUIRED.get(nt, []):
                        if prop not in child:
                            add(ERROR, "json-ld", page,
                                f"nested {nt} missing required property '{prop}' (in {t})")
                    for group in REQUIRED_ANY.get(nt, []):
                        if not any(prop in child for prop in group):
                            add(ERROR, "json-ld", page,
                                f"nested {nt} has none of {' / '.join(group)} (in {t})")
            for t, c in seen.items():
                # Only true singletons. A page may legitimately list many Events,
                # ListItems, VideoObjects, Questions or DefinedTerms.
                if c > 1 and t in SINGLETON_TYPES:
                    add(ERROR, "json-ld", page, f"{t} defined {c} times in one graph")
        if '"@type": "Organization"' not in src:
            add(ERROR, "json-ld", page, "no Organization node")
    measured("json-ld.pages", len(pages))
    measured("json-ld.nodes", total_nodes)
    measured("json-ld.nested_nodes", nested_nodes)


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


# Google renders title links at about 20px Arial in desktop results and cuts
# them off near 580px. Measure the real font rather than counting characters:
# character counts are off by 30-40px on these titles, which is the whole
# margin at this length.
TITLE_PIXEL_LIMIT = 580
TITLE_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _title_font():
    try:
        from PIL import ImageFont
    except Exception:  # noqa: BLE001
        return None
    for path in TITLE_FONT_CANDIDATES:
        if pathlib.Path(path).exists():
            try:
                return ImageFont.truetype(path, 20)
            except Exception:  # noqa: BLE001
                continue
    return None


def check_title_width(pages):
    font = _title_font()
    if font is None:
        # Fail closed. A measurement check that cannot measure must not be green.
        add(ERROR, "title-width", "-",
            "cannot measure title width: PIL or an Arial/Liberation font is missing")
        return
    n = 0
    for page, src in pages.items():
        m = TITLE_RE.search(src)
        if not m:
            continue
        title = m.group(1).strip()
        n += 1
        px = round(font.getlength(title), 1)
        if px > TITLE_PIXEL_LIMIT:
            add(ERROR, "title-width", page,
                f"title is {px}px, past the {TITLE_PIXEL_LIMIT}px cutoff: {title}")
    measured("title-width.titles", n)


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


# ---------------------------------------------------------------- disambiguation
def _schema_constant(name):
    """Read a constant out of build/schema.py. Empty string when it is gone.

    Asserting on the exported constant rather than on a copy of the sentence is
    what stops this regressing: a substring test over a served page passes while
    the constant is deleted and an inline literal silently replaces it.
    """
    build = pathlib.Path(__file__).resolve().parent.parent / "build"
    if not (build / "schema.py").is_file():
        return ""
    if str(build) not in sys.path:
        sys.path.insert(0, str(build))
    try:
        import schema as _schema
    except Exception:  # noqa: BLE001
        return ""
    return getattr(_schema, name, "")


def check_disambiguation(site_dir, pages):
    """The Organization node and llms.txt must both carry the entity disambiguation.

    Without it a model can read this site as a studio, a paid directory, or as
    miamiimprov.com (a comedy theatre), which is a real liability on this domain.
    """
    phrase = _schema_constant("DISAMBIGUATION")
    if not phrase:
        add(ERROR, "disambiguation", "build/schema.py",
            "the DISAMBIGUATION constant is missing or empty; the entity "
            "disambiguation has been dropped")
        return
    n = 0
    for page, src in pages.items():
        for raw in LD_RE.findall(src):
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            for node in (data.get("@graph") or [data]):
                if node.get("@type") != "Organization":
                    continue
                n += 1
                dd = node.get("disambiguatingDescription") or ""
                if not dd:
                    add(ERROR, "disambiguation", page,
                        "Organization has no disambiguatingDescription property")
                elif phrase.lower() not in dd.lower():
                    add(ERROR, "disambiguation", page,
                        f"Organization.disambiguatingDescription does not state '{phrase}'")
    measured("disambiguation.organization_nodes", n)

    llms = (site_dir / "llms.txt").read_text(encoding="utf-8")
    # The summary line an answer engine reads first, not a substring anywhere in
    # the file (which a comment would satisfy).
    summary = next((ln for ln in llms.splitlines() if ln.startswith("> ")), "")
    measured("disambiguation.llms_summary_lines", 1 if summary else 0)
    if phrase.lower() not in summary.lower():
        add(ERROR, "disambiguation", "llms.txt",
            f"llms.txt summary line does not state '{phrase}'")


# ---------------------------------------------------------------- local listings
DATE_FIELD_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _import_build_module(name):
    """Import a module out of build/, the way _schema_constant reads schema.py."""
    build = pathlib.Path(__file__).resolve().parent.parent / "build"
    if not (build / f"{name}.py").is_file():
        return None
    if str(build) not in sys.path:
        sys.path.insert(0, str(build))
    try:
        return __import__(name)
    except Exception:  # noqa: BLE001
        return None


def check_local_listings():
    """The local listing tables are this property's honesty rules; enforce them in code.

    build/listings.py used to say those rules were "enforced by review rather than by
    code". Review is what let an undated listing read as current in the first place, so
    the rules that carry a published claim are asserted here instead: a session with no
    stated modality, no source URL or no checked date, a dated occurrence with no named
    organiser, and an organiser map that has drifted away from the session names all
    fail the build rather than shipping.

    The session COUNT is deliberately not the measured value. An empty list is a valid,
    honest state on this property (see the module docstring in build/listings.py), so a
    check that failed closed on it would punish the correct behaviour. What is measured
    is the number of constraints actually compared, which is what must never be zero.
    """
    listings = _import_build_module("listings")
    if listings is None:
        add(ERROR, "local-listings", "build/listings.py",
            "cannot import build/listings.py; the local listing contract is unverified")
        return

    checks = 0
    sessions = getattr(listings, "SESSIONS", None)
    if not isinstance(sessions, list):
        add(ERROR, "local-listings", "build/listings.py", "SESSIONS is missing or not a list")
        return

    def bad(name, message):
        add(ERROR, "local-listings", name, message)

    names = []
    for row in sessions:
        checks += 1
        if len(row) != 9:
            bad(str(row[0] if row else "?"), f"session row has {len(row)} fields, expected 9")
            continue
        name, modality, _city, venue, schedule, cost, url, verified, note = row
        names.append(name)
        if not str(modality).strip():
            bad(name, "session states no modality; a contact-adjacent practice must never read as CI")
        if not str(url).startswith("http"):
            bad(name, f"session source is not a URL: {url!r}")
        if not DATE_FIELD_RE.match(str(verified)):
            bad(name, f"session checked date is not YYYY-MM-DD: {verified!r}")
        for field, value in (("venue", venue), ("schedule", schedule), ("cost", cost), ("note", note)):
            checks += 1
            if not str(value).strip():
                bad(name, f"session {field} is empty")

    orgs = getattr(listings, "SESSION_ORGANISERS", {})
    checks += 1
    if not isinstance(orgs, dict):
        bad("build/listings.py", "SESSION_ORGANISERS is missing or not a dict")
        orgs = {}
    for name in names:
        checks += 1
        if name not in orgs:
            bad(name, "session names no organiser in SESSION_ORGANISERS")
    if names:
        for name in sorted(orgs):
            checks += 1
            if name not in names:
                bad(name, "SESSION_ORGANISERS entry matches no session (orphaned organiser)")

    dates = getattr(listings, "EVENT_DATES", {})
    event_orgs = getattr(listings, "EVENT_ORGS", {})
    for name, occurrences in (dates.items() if isinstance(dates, dict) else []):
        checks += 1
        if name not in names:
            bad(name, "EVENT_DATES names a session that does not exist")
        if name not in event_orgs:
            bad(name, "a dated occurrence has no EVENT_ORGS entry, so an Event would publish "
                      "under a guessed organiser")
        for iso, location in occurrences:
            checks += 1
            if not DATE_FIELD_RE.match(str(iso)):
                bad(name, f"occurrence date is not YYYY-MM-DD: {iso!r}")
            checks += 1
            if not str(location).strip():
                bad(name, "occurrence has no location string")

    measured("local-listings.constraints", checks)


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


# ---------------------------------------------------------------- video room
SITE_ROOT = "https://miamicontactimprov.com"
VIDEO_ROOM_PATH = "/videos"
VIDEO_COUNT_RE = re.compile(r"\((\d+)\)")


def _all_typed_nodes(src):
    """Every typed node in a page's @graph, containers included."""
    out = []
    for raw in LD_RE.findall(src):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for node in (data.get("@graph") or [data]):
            out.append(node)
            _nested_typed_nodes(node, out)
    return out


def _credit_names(node):
    """Every name and @id a VideoObject credits as creator or publisher."""
    names = []
    for key in ("creator", "publisher"):
        credit = node.get(key)
        if isinstance(credit, dict):
            if credit.get("name"):
                names.append(credit["name"])
            if credit.get("@id"):
                names.append(credit["@id"])
        elif isinstance(credit, str):
            names.append(credit)
    return names


def check_video_room(pages):
    """Two claims the video room must keep true.

    1. Attribution. A film with an embedUrl belongs to the channel that published it
       and must name that channel, never this site. A film this site hosts may only
       be credited to this site. Either way the room cannot carry a film with no
       credited maker, which is what the room did before: 22 embeds and no credit.
    2. The title's bracket count. `(22)` in a title is a claim made in the search
       result, so it is recounted here against the films actually on the page. The
       count covers owned and embedded films alike, because that is what the page
       carries.
    """
    site_name = _schema_constant("ORG_NAME") or "Miami Contact Improv"
    org_id = _schema_constant("ORG_ID")
    if not org_id:
        add(ERROR, "video-attribution", "build/schema.py",
            "schema.ORG_ID is missing, so no self-hosted film can be credited to this site")
        return
    # The site's own name is read off the served Organization node rather than
    # hardcoded here, so this check cannot drift away from what the page actually says.
    site_credit = {org_id}
    for src in pages.values():
        for node in _all_typed_nodes(src):
            if node.get("@type") == "Organization" and node.get("@id") == org_id and node.get("name"):
                site_credit.add(node["name"].lower())
    if len(site_credit) < 2:
        add(ERROR, "video-attribution", "build/schema.py",
            "no Organization node names this site, so its own credit cannot be identified")
        return
    room_pages = [p for p, src in pages.items()
                  if any(c.rstrip("/") == SITE_ROOT + VIDEO_ROOM_PATH for c in CANON_RE.findall(src))]
    if not room_pages:
        add(ERROR, "video-count", "-",
            f"no page canonicalises to {VIDEO_ROOM_PATH}; the video room cannot be checked")
        return
    total = 0
    for page, src in pages.items():
        videos = [n for n in _all_typed_nodes(src) if n.get("@type") == "VideoObject"]
        if not videos:
            continue
        total += len(videos)
        for v in videos:
            credited = _credit_names(v)
            claimed_by_site = any(name.lower() in site_credit or name == org_id for name in credited)
            if v.get("embedUrl"):
                if claimed_by_site:
                    add(ERROR, "video-attribution", page,
                        f"embedded film credited to this site: {v.get('name')!r}")
                if not credited:
                    add(ERROR, "video-attribution", page,
                        f"embedded film with no credited channel: {v.get('name')!r}")
            elif org_id not in credited:
                add(ERROR, "video-attribution", page,
                    f"self-hosted film not credited to this site: {v.get('name')!r}")
        if page in room_pages:
            m = TITLE_RE.search(src)
            if not m:
                continue
            bracket = VIDEO_COUNT_RE.search(m.group(1))
            if not bracket:
                add(ERROR, "video-count", page,
                    f"video room title carries no (n) count: {m.group(1).strip()!r}")
            elif int(bracket.group(1)) != len(videos):
                add(ERROR, "video-count", page,
                    f"title says ({bracket.group(1)}) but the page carries {len(videos)} films")
    measured("video.attributed", total)
    if total == 0:
        add(ERROR, "video-count", "-", "no VideoObject found anywhere; the room lost its films")


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
    check_title_width(pages)
    check_sitemap(site_dir, pages)
    check_links(pages, site_dir)
    check_files(site_dir)
    check_canonical_forms(site_dir, pages)
    check_assets(site_dir)
    check_a11y(pages)
    check_disambiguation(site_dir, pages)
    check_video_room(pages)
    check_local_listings()

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
