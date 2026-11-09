"""The free beginner's guide: /guide, eight chapters, /guide/print and the PDF.

Chapter prose lives in guide_chapters*.py. This module owns the pages around it: the
index, the chapter shell with its breadcrumb and prev/next links, and the one-page print
view that tools/make_guide_pdf.py turns into the committed PDF.
"""

import hashlib

import guide_chapters
import locales
import schema
from shell import answer, band, cards, cite_block, page, subscribe_block

CHAPTERS = guide_chapters.CHAPTERS
PDF_PATH = "/guide/contact-improvisation-beginners-guide.pdf"
PDF_NAME = "contact-improvisation-beginners-guide.pdf"
GUIDE_TITLE = "Contact Improvisation: A Beginner's Guide"
MODIFIED = "2026-11-09"

# Pages that stay reachable but are not for search: not listed in the sitemap or llms files.
NOINDEX_ROUTES = ("/guide/print",)

ROBOTS_INDEX = 'content="index, follow, max-image-preview:large, max-snippet:-1"'
ROBOTS_NOINDEX = 'content="noindex, follow"'

STYLE = """<style>
.guide-crumbs { font-size: 0.82rem; letter-spacing: 0.03em; margin: 0 0 18px; color: var(--muted); }
.guide-crumbs a { color: inherit; }
.guide-crumbs span[aria-current] { color: var(--ink); }
.guide-pager { display: flex; flex-wrap: wrap; gap: 14px; justify-content: space-between; align-items: center; margin: 40px 0 0; padding-top: 22px; border-top: 1px solid var(--line-strong); max-width: var(--read); }
.guide-pager a { font-weight: 600; }
.guide-pdf { margin: 0 0 30px; }
.guide-list { list-style: none; margin: 0 0 28px; padding: 0; max-width: var(--read); }
.guide-list li { margin: 0 0 14px; padding: 0 0 14px; border-bottom: 1px solid var(--line); }
.guide-list a { font-weight: 600; }
.guide-list .num { display: block; font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--terracotta); font-weight: 700; }
</style>"""

PRINT_STYLE = """<style>
.g-cover { padding: 12vh 0 8vh; }
.g-cover h1 { font-size: clamp(36px, 6vw, 64px); line-height: 1.02; text-transform: uppercase; max-width: 18ch; margin: 0 0 20px; }
.g-cover .g-sub { font-size: 1.15rem; margin: 0 0 40px; max-width: 46ch; }
.g-cover .g-site { font-weight: 600; letter-spacing: 0.04em; }
.g-kicker { font-size: 0.78rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--terracotta); font-weight: 700; margin: 0 0 8px; }
.g-chapter { padding: 44px 0 0; }
.g-chapter h2.g-title { font-size: clamp(1.9rem, 3.6vw, 2.8rem); line-height: 1.08; text-transform: uppercase; margin: 0 0 12px; }
.g-lede { font-size: 1.1rem; margin: 0 0 20px; }
.g-toc { margin: 0 0 30px 22px; }
.g-toc li { margin: 0 0 8px; }
@media print {
  @page { margin: 20mm 17mm 22mm; @bottom-center { content: counter(page); font: 9pt Georgia, serif; color: #555; } }
  html, body { background: #fff !important; color: #171512 !important; }
  body { font: 11pt/1.55 Georgia, "Times New Roman", serif; }
  .site-header, .site-footer, .skip-link, #grain, .scroll-controls, .mci-popup-overlay, .mci-popup, .mci-ribbon, #bgwrap { display: none !important; }
  .page, main { margin: 0 !important; padding: 0 !important; }
  .wrap { max-width: none !important; width: auto !important; margin: 0 !important; padding: 0 !important; }
  .section { padding: 0 !important; }
  .prose { max-width: none !important; }
  h1, h2, h3, .g-kicker, .g-cover .g-site { font-family: "Helvetica Neue", Arial, sans-serif; }
  .g-cover { min-height: 235mm; padding: 38mm 0 0; break-after: page; }
  .g-cover h1 { font-size: 38pt; }
  .g-contents { break-after: page; }
  .g-chapter { break-before: page; padding: 0; }
  .g-chapter h2.g-title { font-size: 24pt; }
  .g-chapter h3 { font-size: 13pt; margin: 18pt 0 6pt; text-transform: none; break-after: avoid; }
  p, li { orphans: 3; widows: 3; }
  ol, ul { break-inside: avoid; }
  a { color: #171512; text-decoration: underline; }
  blockquote, .g-credit { break-inside: avoid; }
}
</style>"""


def _chapter(slug):
    for i, c in enumerate(CHAPTERS):
        if c["slug"] == slug:
            return i, c
    raise KeyError(slug)


def _route(c):
    return locales.route("guide-" + c["slug"], "en")


def _crumbs(trail):
    """Visible breadcrumb. `trail` is [(label, route or None)], the last one being this page."""
    parts = ['<a href="/">Home</a>']
    for label, route in trail:
        parts.append(f'<a href="{route}">{label}</a>' if route else f'<span aria-current="page">{label}</span>')
    return '<nav class="guide-crumbs" aria-label="Breadcrumb">' + " &rsaquo; ".join(parts) + "</nav>"


def _pdf_button(label="Download the free PDF", style="primary"):
    return f'<a class="btn {style}" href="{PDF_PATH}" download>{label}</a>'


def further_reading():
    return (
        f'<p>Much of this guide builds on ideas and exercise structures taught by Martin Keogh, a contact '
        f'improvisation teacher and author. His book <em>{guide_chapters.BOOK_TITLE}</em> '
        f'({guide_chapters.BOOK_PUBLISHER}, {guide_chapters.BOOK_YEAR}) is the place to go for the long version. '
        f'<a href="{guide_chapters.BOOK_URL}" rel="noopener">Find the book on martinkeogh.com</a>.</p>'
        "<p>All the prose here is written for this site, with short credited quotations and links to his pages. "
        "Keogh has not reviewed or endorsed this guide.</p>"
    )


def index():
    items = [
        ("Chapter %d" % (i + 1), c["short"], c["lede"], _route(c)) for i, c in enumerate(CHAPTERS)
    ]
    body = f"""
<section class="hero">
  <div class="wrap">
    {_crumbs([("Guide", None)])}
    <p class="eyebrow">Free &middot; eight short chapters &middot; no partner needed</p>
    <h1>A beginner's guide to contact improvisation.</h1>
    <p class="lede">Eight short chapters you can read in an evening and practise on the floor, from the first fall to your first jam. Free to read here and free to download.</p>
    <div class="btn-row guide-pdf">
      {_pdf_button()}
      <a class="btn secondary" href="{_route(CHAPTERS[0])}">Start with chapter 1</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("This guide takes a newcomer through contact improvisation in eight chapters: what the form is, learning to fall, sharing weight, sensation and space, saying no, your first jam, quieting the inner critic, and what progress looks like. Each chapter takes about ten minutes to read and has one or two exercises you can try alone first. The whole guide is free as web pages and as one PDF.")}
    <div class="prose">
      <h2>The chapters</h2>
    </div>
    {cards(items)}
    <div class="prose">
      <h2>Take it with you</h2>
      <p>The free PDF holds all eight chapters on one document that prints cleanly on Letter or A4. You do not need to give an email address to download it.</p>
    </div>
    <div class="btn-row guide-pdf">
      {_pdf_button()}
    </div>
    {subscribe_block("en", source="miamicontactimprov:guide", offer="Want the next Miami dates by email? One short message a month.", uid="guide")}
    <div class="prose">
      <h2>Further reading</h2>
      {further_reading()}
      <p>Before you practise with a partner, read <a href="/safety-and-consent">safety and consent</a>. Ready to try a session? See <a href="/your-first-jam">your first jam</a> and the <a href="/friday-jam">Friday jam</a>.</p>
    </div>
    {cite_block(f"Miami Contact Improv (2026). <em>{GUIDE_TITLE}</em>. miamicontactimprov.com. https://miamicontactimprov.com/guide/")}
  </div>
</section>
"""
    wp = schema.webpage(
        "/guide/", "A beginner's guide to contact improvisation",
        "A free eight-chapter beginner's guide to contact improvisation with exercises, written for this site, plus a downloadable PDF.",
        date_modified=MODIFIED,
    )
    wp["datePublished"] = MODIFIED
    jsonld = schema.render(schema.organisation(), wp, schema.breadcrumb("/guide/", "Guide"))
    return page(
        "Contact Improv Beginner's Guide [Free PDF, 2026]",
        "A free eight-chapter beginner's guide to contact improvisation: falling, sharing weight, saying no and your first jam. Read online or download the PDF.",
        "/guide/",
        body,
        jsonld=jsonld,
        extra_head=STYLE + "\n",
    )


def chapter_builder(slug):
    def build():
        return chapter_page(slug)
    build.__name__ = "guide_" + slug.replace("-", "_")
    return build


def chapter_page(slug):
    i, c = _chapter(slug)
    n = len(CHAPTERS)
    route = _route(c)
    prev_c = CHAPTERS[i - 1] if i > 0 else None
    next_c = CHAPTERS[i + 1] if i < n - 1 else None
    prev_link = (f'<a href="{_route(prev_c)}" rel="prev">&larr; Previous: {prev_c["short"]}</a>' if prev_c
                 else '<span></span>')
    next_link = (f'<a href="{_route(next_c)}" rel="next">Next: {next_c["short"]} &rarr;</a>' if next_c
                 else f'<a href="/keep-practising">Next: keep practising &rarr;</a>')
    body = f"""
<section class="hero">
  <div class="wrap">
    {_crumbs([("Guide", "/guide/"), (c["short"], None)])}
    <p class="eyebrow">Beginner's guide &middot; chapter {i + 1} of {n}</p>
    <h1>{c["h1"]}</h1>
    <p class="lede">{c["lede"]}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer(c["answer"])}
    <div class="prose">{c["html"]}</div>
    <nav class="guide-pager" aria-label="Chapters">
      {prev_link}
      <a href="/guide/">Back to the guide</a>
      {next_link}
    </nav>
    {band("Read it offline", "All eight chapters are in one free PDF. No email needed.", [("Download the free PDF", PDF_PATH, "primary"), ("Back to the guide", "/guide/", "secondary")])}
    {cite_block(f"Miami Contact Improv (2026). <em>{GUIDE_TITLE}</em>, chapter {i + 1}: {c['short']}. miamicontactimprov.com. https://miamicontactimprov.com{route}")}
  </div>
</section>
"""
    wp = schema.webpage(route, c["short"] + " | " + GUIDE_TITLE, c["desc"], date_modified=MODIFIED)
    wp["datePublished"] = MODIFIED
    jsonld = schema.render(
        schema.organisation(), wp,
        schema.breadcrumb_trail(route, [("Guide", "/guide/"), (c["short"], route)]),
    )
    return page(c["title"], c["desc"], route, body, jsonld=jsonld, extra_head=STYLE + "\n")


def _absolute(html):
    """A PDF cannot keep root-relative links: they would resolve to whatever host rendered it."""
    return html.replace('href="/', f'href="{locales.SITE}/')


def _retitle(html):
    """Chapter sections are h2 on their own page; inside the print page the chapter is the h2."""
    return html.replace("<h2>", "<h3>").replace("</h2>", "</h3>")


def print_page():
    toc = "".join(f"<li>{c['short']}</li>" for c in CHAPTERS)
    chapters = "".join(
        f"""
<section class="g-chapter">
  <p class="g-kicker">Chapter {i + 1}</p>
  <h2 class="g-title">{c["short"]}</h2>
  <p class="g-lede">{c["lede"]}</p>
  <div class="prose">{_absolute(_retitle(c["html"]))}</div>
</section>"""
        for i, c in enumerate(CHAPTERS)
    )
    body = f"""
<section class="section g-cover">
  <div class="wrap">
    <p class="g-kicker">A free guide</p>
    <h1>{GUIDE_TITLE}</h1>
    <p class="g-sub">Eight short chapters, with exercises you can try alone first.</p>
    <p class="g-site">Miami Contact Improv, miamicontactimprov.com</p>
  </div>
</section>

<section class="section g-contents">
  <div class="wrap">
    <h2>Contents</h2>
    <ol class="g-toc">{toc}</ol>
    <div class="prose">
      <p>Read the chapters in order the first time. Before you try any exercise with a partner, read the safety and consent page at {locales.SITE}/safety-and-consent. This guide is not medical advice.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">{chapters}
    <section class="g-chapter g-credit">
      <p class="g-kicker">Credits</p>
      <h2 class="g-title">Further reading</h2>
      <div class="prose">{further_reading()}
      <p>Online: {locales.SITE}/guide/. Miami Contact Improv is an independent community resource and is not affiliated with Martin Keogh or his publisher.</p></div>
    </section>
  </div>
</section>
"""
    route = "/guide/print"
    wp = schema.webpage(route, GUIDE_TITLE + " (print version)",
                        "All eight chapters of the free contact improvisation beginner's guide on one page, formatted for printing.",
                        date_modified=MODIFIED)
    wp["datePublished"] = MODIFIED
    jsonld = schema.render(
        schema.organisation(), wp,
        schema.breadcrumb_trail(route, [("Guide", "/guide/"), ("Print version", route)]),
    )
    html = page(
        "Contact Improv Beginner's Guide, Print Version",
        "All eight chapters of the free contact improvisation beginner's guide on one page, formatted to print or save as a PDF.",
        route, body, jsonld=jsonld, extra_head=PRINT_STYLE + "\n",
    )
    if html.count(ROBOTS_INDEX) != 1:
        raise SystemExit("content_guide: expected one robots meta on the print page")
    return html.replace(ROBOTS_INDEX, ROBOTS_NOINDEX)


def is_noindex(route):
    return route in NOINDEX_ROUTES


def page_rows():
    """PAGES rows for the guide: (slug, lang, builder, priority, changefreq, bg)."""
    rows = [("guide", "en", index, "0.8", "monthly", None)]
    for c in CHAPTERS:
        rows.append(("guide-" + c["slug"], "en", chapter_builder(c["slug"]), "0.6", "monthly", None))
    rows.append(("guide-print", "en", print_page, "0.1", "yearly", None))
    return rows


def print_fingerprint():
    """sha256 of everything that decides what the PDF looks like: the print page's <main> and its CSS.

    Nothing date- or build-dependent is in either (the head, with the analytics snippet, is
    excluded). tools/make_guide_pdf.py stores this next to the PDF and tests/test_guide.py
    recomputes it, so a chapter edit without a regenerated PDF fails CI without needing Chrome.
    """
    html = print_page()
    main = html.split("<main", 1)[1].split("</main>", 1)[0]
    return hashlib.sha256((main + PRINT_STYLE).encode("utf-8")).hexdigest()
