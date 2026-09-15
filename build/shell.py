"""Shared page shell for miamicontactimprov.com.

Every page is rendered through here so the head, nav and footer exist in exactly
one place, in every locale. Editing the nav means editing NAV below and re-running
build.py; adding a language means adding it to build/locales.py.

The locale model lives in build/locales.py. This module asks it two questions and
never invents a URL of its own: which route does this page have in that language
(`locales.route`), and which languages may this page offer (`locales.switch_targets`).
That is what stops the language switcher from pointing at a page that does not exist.
"""

import locales
import schema

SITE = locales.SITE
NAME = "Miami Contact Improv"
TAGLINE = "A working map of Contact Improvisation in Miami"

# Bump when the local listings in build/listings.py are re-checked against source.
LAST_CHECKED = "14 September 2026"
LAST_CHECKED_ES = "14 de septiembre de 2026"
LAST_CHECKED_ISO = "2026-09-14"
LAST_CHECKED_BY_LANG = {"en": LAST_CHECKED, "es": LAST_CHECKED_ES}

# The site's scope and nature, stated one way everywhere (footer, schema, llms.txt).
# schema.py owns the strings; the footer must not carry a second version of them.
SITE_SENTENCE_BY_LANG = schema.SITE_SENTENCE_BY_LANG
SITE_SENTENCE = schema.SITE_SENTENCE

# slug + the label in each locale. `locales.route(slug, lang)` decides the href, so a
# nav item can only point at a page this site actually builds.
NAV = [
    ("what-is-contact-improvisation", {"en": "What is CI", "es": "Qué es la IC"}),
    ("miami", {"en": "Miami", "es": "Miami"}),
    ("jams", {"en": "Jams", "es": "Jams"}),
    ("classes", {"en": "Classes", "es": "Clases"}),
    ("videos", {"en": "Videos", "es": "Vídeos"}),
    ("directory", {"en": "Directory", "es": "Directorio"}),
    ("about", {"en": "About", "es": "Acerca de"}),
]

NAV_CTA = {"en": ("Submit a jam", "/about#submit"), "es": ("Publica tu sesión", "/es/acerca-de#submit")}

# Properties Max owns and runs. One canonical host each, rendered on every page so
# every crawled URL carries the outbound link rather than a single about page.
# Miami Contact Improv itself is deliberately absent from its own footer.
PROJECT_HEADING = {"en": "Projects", "es": "Proyectos"}
PROJECT_LINKS = [
    ("Max Petrusenko", "https://www.maxpetrusenko.com"),
    ("GeoAnalyzer", "https://geo-analyzer.com"),
    ("Unfollow X", "https://unfollow-x.com"),
    ("SMM Agent", "https://smmagent.app"),
    ("SMMClaw", "https://smmclaw.app"),
    ("ClawPoster", "https://clawposter.app"),
    ("Max Wiki", "https://wiki.maxpetrusenko.com"),
]

FOOTER_COLS = [
    ("start", {
        "en": "Start here",
        "es": "Para empezar",
    }, [
        ("what-is-contact-improvisation", {"en": "What is Contact Improvisation?", "es": "¿Qué es la Improvisación de Contacto?"}),
        ("your-first-jam", {"en": "Your first jam, step by step", "es": "Tu primera jam, paso a paso"}),
        ("glossary", {"en": "Glossary of CI terms", "es": "Glosario de términos"}),
        ("history", {"en": "History of CI", "es": "Historia de la IC"}),
    ]),
    ("miami", {
        "en": "In Miami",
        "es": "En Miami",
    }, [
        ("miami", {"en": "The Miami scene", "es": "La escena de Miami"}),
        ("miami-jams", {"en": "Miami-Dade and Broward jam list", "es": "Lista de jams de Miami-Dade y Broward"}),
        ("jams", {"en": "Jams and open practice", "es": "Jams y práctica abierta"}),
        ("classes", {"en": "Classes and workshops", "es": "Clases y talleres"}),
        ("keep-practising", {"en": "Keep practising", "es": "Seguir practicando"}),
    ]),
    ("watch", {
        "en": "Watch",
        "es": "Vídeo",
    }, [
        ("videos", {"en": "Video room", "es": "Sala de vídeo"}),
    ]),
    ("site", {
        "en": "This site",
        "es": "Este sitio",
    }, [
        ("about", {"en": "About and contact", "es": "Acerca de y contacto"}),
        ("safety-and-consent", {"en": "Safety and consent", "es": "Seguridad y consentimiento"}),
        ("faq", {"en": "Questions people ask", "es": "Preguntas frecuentes"}),
    ]),
]

STYLESHEET = "/assets/site.css?v=3"


def _nav_href(slug, lang):
    """The route for a nav/footer link, in the reader's language when one exists.

    When it does not, the link still goes to the page that exists rather than to a
    404, and the anchor carries lang="en" so a screen reader and a browser's
    translator are told the destination is in English.
    """
    route = locales.route(slug, lang)
    if route:
        return route, True
    return locales.route(slug, locales.DEFAULT) or "/", False


def _link(slug, lang, label):
    href, translated = _nav_href(slug, lang)
    attr = "" if translated else f' lang="{locales.HTML_LANG[locales.DEFAULT]}" hreflang="{locales.HTML_LANG[locales.DEFAULT]}"'
    return f'<a href="{href}"{attr}>{label}</a>'


def head(title, description, path, *, jsonld="", og_type="website", extra_head="", lang="en", slug=None):
    """Return the <head> block. `path` is the site-relative route, e.g. /miami.

    Emits the reciprocal alternate set for this page and x-default. A locale appears
    in that set only when this page exists in it, so every hreflang target on this
    site is a file the build actually wrote.
    """
    url = SITE + path
    slug = slug or locales.slug_for(path, lang)
    alts = locales.alternates(slug) if slug else []
    alt_tags = "\n".join(
        f'<link rel="alternate" hreflang="{locales.HTML_LANG[code]}" href="{href}">'
        for code, href in alts
    )
    if alts:
        default_route = locales.route(slug, locales.DEFAULT)
        alt_tags += f'\n<link rel="alternate" hreflang="x-default" href="{locales.url_for(default_route)}">'
    og_locale = locales.OG_LOCALE.get(lang, "en_US")
    og_alternates = "\n".join(
        f'<meta property="og:locale:alternate" content="{locales.OG_LOCALE[code]}">'
        for code, _href in alts
        if code != lang
    )
    return f"""<!DOCTYPE html>
<html lang="{locales.HTML_LANG.get(lang, "en")}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
{alts and alt_tags or ""}
<meta name="theme-color" content="#0c1210">
<meta name="color-scheme" content="dark">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Two dancers in contact improvisation, one supporting the other's weight">
<meta property="og:locale" content="{og_locale}">
{og_alternates}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE}/assets/og.png">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/favicon-96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=Instrument+Serif:ital@0;1&display=swap">
<link rel="stylesheet" href="{STYLESHEET}">
<link rel="alternate" type="text/plain" href="{SITE}/llms.txt" title="llms.txt">
{extra_head}{jsonld}
</head>"""


LANG_SWITCH_CSS_CLASS = "lang-switch"


def language_switch(path, lang):
    """The language switcher. One entry per locale this site publishes.

    Three things this deliberately does:

    * A locale whose translation of THIS page does not exist is not advertised as a
      translation. Its link goes to that locale's home and carries no hreflang, because
      hreflang asserts "same page, other language" and that would be false.
    * The current locale is a <span>, not a link to itself.
    * Each option is labelled in its own language and carries lang=, so "Español" is
      announced in Spanish rather than mangled by an English synthesizer.
    """
    if not locales.LOCALES or len(locales.LOCALES) < 2:
        return ""
    slug = locales.slug_for(path, lang)
    if not slug:
        return ""
    items = []
    for code, href, is_current, is_translation in locales.switch_targets(slug, lang):
        label = locales.LOCALE_LABEL[code]
        if is_current:
            items.append(
                f'<span class="lang-item is-current" lang="{locales.HTML_LANG[code]}" '
                f'aria-current="true">{label}</span>'
            )
            continue
        note = locales.NO_TRANSLATION_TITLE.get(code, locales.NO_TRANSLATION_TITLE["en"])
        extra = "" if is_translation else f' title="{note}"'
        # hreflang is emitted only when this really is the same page in another
        # language. Declaring it on a fallback link would be a false equivalence.
        hl = f' hreflang="{locales.HTML_LANG[code]}"' if is_translation else ""
        items.append(
            f'<a class="lang-item" href="{href}" lang="{locales.HTML_LANG[code]}"'
            f'{hl}{extra}>{label}</a>'
        )
    return (
        f'<nav class="{LANG_SWITCH_CSS_CLASS}" aria-label="{locales.SWITCHER_LABEL}">'
        + "".join(items)
        + "</nav>"
    )


def header(current, lang="en"):
    links = []
    for slug, labels in NAV:
        label = labels.get(lang) or labels[locales.DEFAULT]
        href, translated = _nav_href(slug, lang)
        cur = ' aria-current="page"' if href == current else ""
        default_lang = locales.HTML_LANG[locales.DEFAULT]
        extra = "" if translated else f' lang="{default_lang}" hreflang="{default_lang}"'
        links.append(f'<a href="{href}"{cur}{extra}>{label}</a>')
    cta_label, cta_href = NAV_CTA.get(lang, NAV_CTA[locales.DEFAULT])
    links.append(f'<a class="cta" href="{cta_href}">{cta_label}</a>')
    home = locales.route("home", lang) or "/"
    return f"""<header class="site-header" id="site-header">
  <div class="header-inner">
    <a class="brand" href="{home}">
      <span class="dot" aria-hidden="true"></span>
      <span>Miami Contact Improv<small>miamicontactimprov.com</small></span>
    </a>
    {language_switch(current, lang)}
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="primary-nav">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="primary-nav" aria-label="Primary">
      {''.join(links)}
    </nav>
  </div>
</header>"""


def footer(lang="en"):
    cols = []
    for _key, titles, items in FOOTER_COLS:
        title = titles.get(lang) or titles[locales.DEFAULT]
        lis = "".join(
            f'<li>{_link(slug, lang, label.get(lang) or label[locales.DEFAULT])}</li>'
            for slug, label in items
        )
        cols.append(f'<div><h3>{title}</h3><ul>{lis}</ul></div>')
    sentence = SITE_SENTENCE_BY_LANG.get(lang, SITE_SENTENCE)
    if lang == "es":
        colophon = (
            f"Última comprobación de las sesiones locales: {LAST_CHECKED}. La Improvisación de "
            "Contacto no tiene autoridad central, ni licencia, ni membresía. Este sitio es un "
            "mapa, no el mapa."
        )
    else:
        colophon = (
            f"Local listings last checked {LAST_CHECKED}. Contact Improvisation has no central "
            "authority, no licence and no membership. This site is one map of it, not the map."
        )
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      {''.join(cols)}
    </div>
    <nav class="footer-projects" aria-label="{PROJECT_HEADING.get(lang, PROJECT_HEADING['en'])}">
      <span class="footer-projects-title">{PROJECT_HEADING.get(lang, PROJECT_HEADING['en'])}</span>
      {''.join(
          f'<a href="{href}" target="_blank" rel="noopener">{label}</a>'
          for label, href in PROJECT_LINKS
      )}
    </nav>
    <div class="colophon">
      <span>{sentence}</span>
      <span>{colophon}</span>
    </div>
  </div>
</footer>"""


SKIP_LABELS = {"en": "Skip to content", "es": "Saltar al contenido"}


def body_script():
    return """<script>
(function () {
  var header = document.getElementById('site-header');
  var toggle = header && header.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { header.classList.remove('nav-open'); if (toggle) toggle.setAttribute('aria-expanded', 'false'); }
  });
  var v = document.getElementById('video');
  if (v) {
    var kick = function () { var p = v.play(); if (p && p.catch) p.catch(function () {}); };
    kick();
    ['pointerdown', 'scroll', 'touchstart', 'keydown'].forEach(function (ev) {
      window.addEventListener(ev, kick, { once: true, passive: true });
    });
  }
})();
</script>
</body>
</html>"""


def bg_youtube_embed(video_id):
    """YouTube background-embed: official embed player in muted loop mode.

    Nothing is downloaded or re-hosted; the film plays from the owner's channel.
    """
    src = (
        f"https://www.youtube-nocookie.com/embed/{video_id}"
        "?autoplay=1&mute=1&controls=0&loop=1&playlist=" + video_id
        + "&modestbranding=1&playsinline=1&rel=0&iv_load_policy=3&disablekb=1&fs=0"
    )
    return f"""<div id="bgwrap" aria-hidden="true">
  <iframe id="video" src="{src}" title="" tabindex="-1"
    allow="autoplay; encrypted-media" frameborder="0"></iframe>
</div>"""


def page(title, description, path, body, *, jsonld="", bg_video=None, bg_youtube=None,
         og_type="website", lang="en"):
    """Assemble a full HTML document.

    bg_youtube: a verified YouTube id, played as a muted looping background embed.
    bg_video: a self-hosted filename stem in /assets/videos/ (poster + webm + mp4).
    lang: the locale this page is written in. It selects <html lang>, the reciprocal
    alternates, the switcher, the nav labels and the footer.
    """
    bg = ""
    if bg_youtube:
        bg = bg_youtube_embed(bg_youtube)
    elif bg_video:
        bg = f"""<div id="bgwrap" aria-hidden="true">
  <video id="video" autoplay loop muted playsinline preload="metadata" poster="/assets/videos/{bg_video}-poster.jpg">
    <source src="/assets/videos/{bg_video}.webm?v=1" type="video/webm">
    <source src="/assets/videos/{bg_video}.mp4?v=1" type="video/mp4">
  </video>
</div>"""
    return (
        head(title, description, path, jsonld=jsonld, og_type=og_type, lang=lang)
        + "\n<body>\n"
        + f'<a class="skip-link" href="#main">{SKIP_LABELS.get(lang, SKIP_LABELS["en"])}</a>\n'
        + bg
        + '<div id="scrim" aria-hidden="true"></div><div id="grain" aria-hidden="true"></div>\n'
        + '<div class="page">\n'
        + header(path, lang)
        + "\n<main id=\"main\">\n"
        + body
        + "\n</main>\n"
        + footer(lang)
        + "\n</div>\n"
        + body_script()
    )


# ---------- reusable content blocks ----------

def answer(text, label="Short answer"):
    return f'<div class="answer"><div class="label">{label}</div><p>{text}</p></div>'


def cite_block(text, label="Cite this page"):
    return f'<div class="cite"><div class="label">{label}</div><p>{text}</p></div>'


def band(title, text, buttons, band_id=None):
    bid = f' id="{band_id}"' if band_id else ""
    btns = "".join(
        f'<a class="btn {style}" href="{href}">{label}</a>' for label, href, style in buttons
    )
    return (
        f'<div class="band"{bid}><h2>{title}</h2><p>{text}</p>'
        f'<div class="btn-row">{btns}</div></div>'
    )


def facts(rows, caption=None):
    trs = "".join(
        f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows
    )
    return f'<table class="facts">{trs}</table>'


def cards(items):
    out = []
    for tag, title, text, href in items:
        out.append(
            f'<a class="card" href="{href}"><span class="tag">{tag}</span>'
            f"<h3>{title}</h3><p>{text}</p></a>"
        )
    return f'<div class="grid">{"".join(out)}</div>'
