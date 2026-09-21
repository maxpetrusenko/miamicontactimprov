"""Shared page shell for miamicontactimprov.com.

Every page is rendered through here so the head, nav and footer exist in exactly
one place, in every locale. Editing the nav means editing NAV below and re-running
build.py; adding a language means adding it to build/locales.py.

The locale model lives in build/locales.py. This module asks it two questions and
never invents a URL of its own: which route does this page have in that language
(`locales.route`), and which languages may this page offer (`locales.switch_targets`).
That is what stops the language switcher from pointing at a page that does not exist.

The visual system is the Miami Contact Improv marketing design: warm cream, Anton +
Poppins, a terracotta accent, a full-page grain overlay and a four-item pill nav
(Home / Events / About / Contact) plus a Follow-on-Instagram pill. The deeper library
pages (what-is, jams, classes, history, glossary, safety, directory, videos and the
Spanish tree) are kept reachable from the footer and inherit the same shell.
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

INSTAGRAM_URL = "https://instagram.com/miamicontactimprov"

# The primary nav: the four marketing views. slug + the label in each locale.
# `locales.route(slug, lang)` decides the href, so a nav item can only point at a page
# this site actually builds; Events and Contact exist in English only, and a Spanish
# reader is sent to the English page with a lang annotation rather than to a 404.
NAV = [
    ("home", {"en": "Home", "es": "Inicio"}),
    ("events", {"en": "Events", "es": "Eventos"}),
    ("blog", {"en": "Blog", "es": "Blog"}),
    ("about", {"en": "About", "es": "Acerca de"}),
    ("contact", {"en": "Contact", "es": "Contacto"}),
]

# Instagram glyph, inline so the header carries no external request.
IG_GLYPH = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="6"/>'
    '<circle cx="12" cy="12" r="4.2"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" '
    'stroke="none"/></svg>'
)

# Properties Max owns and runs. Retained in code as the canonical list of outbound
# links; NOT rendered in the footer (see SHOW_PROJECT_LINKS). Hidden-but-present links
# would be a search-spam signal, so when they are off they are off in the HTML too.
SHOW_PROJECT_LINKS = False
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
        ("blog", {"en": "Blog", "es": "Blog"}),
    ]),
    ("miami", {
        "en": "In Miami",
        "es": "En Miami",
    }, [
        ("events", {"en": "Upcoming events", "es": "Próximos eventos"}),
        ("friday-jam", {"en": "Friday jam, Miami", "es": "Jam de los viernes, Miami"}),
        ("miami", {"en": "The Miami scene", "es": "La escena de Miami"}),
        ("miami-jams", {"en": "Miami-Dade and Broward jam list", "es": "Lista de jams de Miami-Dade y Broward"}),
        ("jams", {"en": "Jams and open practice", "es": "Jams y práctica abierta"}),
        ("classes", {"en": "Classes and workshops", "es": "Clases y talleres"}),
        ("keep-practising", {"en": "Keep practising", "es": "Seguir practicando"}),
    ]),
    ("site", {
        "en": "This site",
        "es": "Este sitio",
    }, [
        ("about", {"en": "About the practice", "es": "Acerca de la práctica"}),
        ("safety-and-consent", {"en": "Safety and consent", "es": "Seguridad y consentimiento"}),
        ("faq", {"en": "Questions people ask", "es": "Preguntas frecuentes"}),
        ("directory", {"en": "Directory", "es": "Directorio"}),
        ("contact", {"en": "Contact", "es": "Contacto"}),
    ]),
]

STYLESHEET = "/assets/site.css?v=4"


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
<meta name="theme-color" content="#F3EDE1">
<meta name="color-scheme" content="light">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Poppins:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{STYLESHEET}">
<link rel="alternate" type="text/plain" href="{SITE}/llms.txt" title="llms.txt">
{extra_head}{jsonld}
</head>"""


LANG_SWITCH_CSS_CLASS = "lang-switch"


def language_switch(path, lang):
    """The language switcher. One entry per locale this site publishes."""
    if not locales.LOCALES or len(locales.LOCALES) < 2:
        return ""
    slug = locales.slug_for(path, lang)
    if not slug:
        return ""
    items = []
    for code, href, is_current, is_translation in locales.switch_targets(slug, lang):
        label = locales.LOCALE_SHORT[code]
        if is_current:
            items.append(
                f'<span class="lang-item is-current" lang="{locales.HTML_LANG[code]}" '
                f'aria-current="true">{label}</span>'
            )
            continue
        note = locales.NO_TRANSLATION_TITLE.get(code, locales.NO_TRANSLATION_TITLE["en"])
        extra = "" if is_translation else f' title="{note}"'
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
    follow_label = "Follow" if lang != "es" else "Seguir"
    links.append(
        f'<a class="follow" href="{INSTAGRAM_URL}" target="_blank" rel="noopener">'
        f'{IG_GLYPH}<span>{follow_label}</span></a>'
    )
    home = locales.route("home", lang) or "/"
    return f"""<header class="site-header" id="site-header">
  <div class="header-inner">
    <a class="brand" href="{home}">
      <img src="/assets/logo.png" alt="Miami Contact Improv" width="42" height="42">
      <span class="wordmark">Miami<br>Contact Improv</span>
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
    projects = ""
    if SHOW_PROJECT_LINKS:
        projects = (
            f'<nav class="footer-projects" aria-label="{PROJECT_HEADING.get(lang, PROJECT_HEADING["en"])}">'
            f'<span class="footer-projects-title">{PROJECT_HEADING.get(lang, PROJECT_HEADING["en"])}</span>'
            + "".join(f'<a href="{href}" target="_blank" rel="noopener">{label}</a>' for label, href in PROJECT_LINKS)
            + "</nav>"
        )
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      {''.join(cols)}
    </div>
    {projects}
    <div class="colophon">
      <span>&copy; Miami Contact Improv &middot; {sentence}</span>
    </div>
  </div>
</footer>"""


SKIP_LABELS = {"en": "Skip to content", "es": "Saltar al contenido"}


SCROLL_CONTROLS = """<div class="scroll-controls" id="scroll-controls" aria-hidden="true">
  <button class="to-top" type="button" aria-label="Scroll to top">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>
  </button>
  <button class="to-bottom" type="button" aria-label="Scroll down">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14"/><path d="M19 12l-7 7-7-7"/></svg>
  </button>
</div>"""


def body_script():
    return """<script>
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canHover = window.matchMedia && window.matchMedia('(hover: hover)').matches;

  // ---- mobile nav ----
  var header = document.getElementById('site-header');
  var toggle = header && header.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
    });
    header.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && header) { header.classList.remove('nav-open'); if (toggle) toggle.setAttribute('aria-expanded', 'false'); }
  });

  // ---- floating scroll controls ----
  var sc = document.getElementById('scroll-controls');
  if (sc) {
    var top = sc.querySelector('.to-top');
    var down = sc.querySelector('.to-bottom');
    var onScroll = function () {
      sc.classList.toggle('is-scrolled', window.scrollY > 400);
      var atBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 80;
      sc.classList.toggle('at-bottom', atBottom);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
    if (down) down.addEventListener('click', function () { window.scrollBy({ top: window.innerHeight * 0.85, behavior: reduce ? 'auto' : 'smooth' }); });
  }

  // ---- scroll reveal ----
  var reveals = document.querySelectorAll('.mci-reveal');
  if (reveals.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      reveals.forEach(function (el) { el.classList.add('mci-in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('mci-in'); io.unobserve(en.target); } });
      }, { threshold: 0.15 });
      reveals.forEach(function (el) { io.observe(el); });
      setTimeout(function () {
        reveals.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.top < window.innerHeight && r.bottom > 0) el.classList.add('mci-in');
        });
      }, 600);
    }
  }

  // ---- hero cursor parallax ----
  var hero = document.getElementById('mci-hero');
  if (hero && canHover && !reduce) {
    var byId = function (id) { return document.getElementById(id); };
    var apply = function (hx, hy) {
      var set = function (id, t) { var el = byId(id); if (el) el.style.transform = t; };
      set('mci-disc', 'translate(' + (hx * 34).toFixed(1) + 'px,' + (hy * 34).toFixed(1) + 'px)');
      set('mci-ring', 'translate(' + (hx * -22).toFixed(1) + 'px,' + (hy * -22).toFixed(1) + 'px) rotate(' + (hx * 10).toFixed(1) + 'deg)');
      set('mci-dot1', 'translate(' + (hx * 60).toFixed(1) + 'px,' + (hy * 60).toFixed(1) + 'px)');
      set('mci-dot2', 'translate(' + (hx * -48).toFixed(1) + 'px,' + (hy * -48).toFixed(1) + 'px)');
      set('mci-logo', 'rotateY(' + (hx * 16).toFixed(1) + 'deg) rotateX(' + (-hy * 12).toFixed(1) + 'deg) translate(' + (hx * -18).toFixed(1) + 'px,' + (hy * -18).toFixed(1) + 'px)');
      set('mci-stamp', 'translate(' + (hx * 52).toFixed(1) + 'px,' + (hy * 52).toFixed(1) + 'px) rotate(' + (-10 + hx * 8).toFixed(1) + 'deg)');
      set('mci-chip1', 'translate(' + (hx * 42).toFixed(1) + 'px,' + (hy * 42).toFixed(1) + 'px) rotate(' + (hx * 6).toFixed(1) + 'deg)');
      set('mci-chip2', 'translate(' + (hx * -36).toFixed(1) + 'px,' + (hy * -36).toFixed(1) + 'px) rotate(' + (hx * -5).toFixed(1) + 'deg)');
      set('mci-w1', 'translate(' + (hx * 6).toFixed(1) + 'px,' + (hy * 6).toFixed(1) + 'px)');
      set('mci-w2', 'translate(' + (hx * 12).toFixed(1) + 'px,' + (hy * 12).toFixed(1) + 'px)');
      set('mci-w3', 'translate(' + (hx * 20).toFixed(1) + 'px,' + (hy * 20).toFixed(1) + 'px)');
    };
    hero.addEventListener('mousemove', function (e) {
      var r = hero.getBoundingClientRect();
      apply((e.clientX - r.left) / r.width - 0.5, (e.clientY - r.top) / r.height - 0.5);
    });
    hero.addEventListener('mouseleave', function () { apply(0, 0); });
    var logoWrap = document.getElementById('mci-logo-float');
    var logo = byId('mci-logo');
    if (logo && logoWrap) {
      logo.addEventListener('click', function () {
        logoWrap.classList.add('pulse');
        setTimeout(function () { logoWrap.classList.remove('pulse'); }, 600);
      });
    }
  }

  // ---- read-more (home) ----
  document.querySelectorAll('.mci-more').forEach(function (btn) {
    var target = document.getElementById(btn.getAttribute('data-target'));
    if (!target) return;
    target.hidden = true;
    btn.addEventListener('click', function () {
      var open = target.hidden;
      target.hidden = !open;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      var lbl = btn.querySelector('.lbl');
      if (lbl) lbl.textContent = open ? 'Show less' : 'Read more';
    });
  });

  // ---- accordion (about FAQ) ----
  document.querySelectorAll('.mci-accordion .q').forEach(function (q) {
    q.addEventListener('click', function () {
      var item = q.closest('.item');
      var open = item.classList.toggle('open');
      q.setAttribute('aria-expanded', open ? 'true' : 'false');
      var ic = q.querySelector('.ic');
      if (ic) ic.textContent = open ? '\\u2013' : '+';
    });
  });

  // ---- mailing-list form (contact) ----
  var form = document.getElementById('mci-signup');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (form.querySelector('[name=name]') || {}).value || '';
      var email = (form.querySelector('[name=email]') || {}).value || '';
      var btn = form.querySelector('button');
      if (name && email) {
        var body = encodeURIComponent('Please add me to the Miami Contact Improv mailing list.\\n\\nName: ' + name + '\\nEmail: ' + email);
        window.location.href = 'mailto:hello@miamicontactimprov.com?subject=' + encodeURIComponent('Mailing list sign-up') + '&body=' + body;
        if (btn) btn.textContent = 'Opening your email app…';
      }
    });
  }

  // ---- background video kick (unused on the marketing views, kept for compatibility) ----
  var v = document.getElementById('video');
  if (v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
})();
</script>
</body>
</html>"""


def bg_youtube_embed(video_id):
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

    lang: the locale this page is written in. It selects <html lang>, the reciprocal
    alternates, the switcher, the nav labels and the footer.
    """
    return (
        head(title, description, path, jsonld=jsonld, og_type=og_type, lang=lang)
        + "\n<body>\n"
        + f'<a class="skip-link" href="#main">{SKIP_LABELS.get(lang, SKIP_LABELS["en"])}</a>\n'
        + '<div id="grain" aria-hidden="true"></div>\n'
        + '<div class="page">\n'
        + header(path, lang)
        + "\n<main id=\"main\">\n"
        + body
        + "\n</main>\n"
        + SCROLL_CONTROLS
        + "\n"
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
