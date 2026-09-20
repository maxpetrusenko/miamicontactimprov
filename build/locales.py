"""The locale model for miamicontactimprov.com.

One table owns every URL on this property. `ROUTES` maps a locale-independent page
slug to the route in each locale that has that page, and that pairing IS the
hreflang graph and the language switcher: a slug with two routes is a translation
pair, a slug with one route is a page that exists in one language only.

Why the routes live here rather than in build/build.py:

* A route must be defined exactly once. build/build.py orders the pages and pairs
  each one with a builder; it does not invent URLs. If a route were written down in
  two places, a hreflang tag and a switcher link would eventually disagree with the
  sitemap, and a switcher that 404s is worse than no switcher.
* `filename_for` derives the output path from the route, so a new locale is a row in
  this file and nothing else.

Path scheme: locale PREFIX for non-default locales (`/es/...`), and the default
locale unprefixed at the root. Justification is in docs/i18n.md; the short version is
that root-stays-English keeps every existing URL, canonical, sitemap entry and inbound
link byte-identical, and a prefix groups a locale under one directory so a third
language is one row here.
"""

SITE = "https://miamicontactimprov.com"

DEFAULT = "en"
LOCALES = ("en", "es")

# The name of each language in that language. A switcher that labels Spanish "Spanish"
# is written for the reader who does not need it.
LOCALE_LABEL = {"en": "English", "es": "Español"}
LOCALE_SHORT = {"en": "EN", "es": "ES"}

# <html lang> and the schema.org inLanguage value per locale.
HTML_LANG = {"en": "en", "es": "es"}
SCHEMA_LANG = {"en": "en-US", "es": "es-US"}
OG_LOCALE = {"en": "en_US", "es": "es_US"}

# Label for the switcher, spelled in both languages so it is legible either way.
SWITCHER_LABEL = "Language / Idioma"

# slug -> {locale: route}. Add a slug here and the page gains a canonical, a sitemap
# entry, a redirect rule and an hreflang pair automatically.
ROUTES = {
    "home": {"en": "/", "es": "/es/"},
    "what-is-contact-improvisation": {
        "en": "/what-is-contact-improvisation",
        "es": "/es/que-es-la-improvisacion-de-contacto",
    },
    "jams": {"en": "/jams", "es": "/es/jams"},
    "friday-jam": {"en": "/friday-jam", "es": "/es/jam-de-los-viernes"},
    "your-first-jam": {"en": "/your-first-jam", "es": "/es/tu-primera-jam"},
    "miami-jams": {"en": "/miami-jams", "es": "/es/jams-miami-dade-broward"},
    "faq": {"en": "/faq", "es": "/es/preguntas-frecuentes"},
    "safety-and-consent": {
        "en": "/safety-and-consent",
        "es": "/es/seguridad-y-consentimiento",
    },
    "miami": {"en": "/miami", "es": "/es/miami"},
    "classes": {"en": "/classes", "es": "/es/clases"},
    "keep-practising": {"en": "/keep-practising", "es": "/es/seguir-practicando"},
    "videos": {"en": "/videos", "es": "/es/videos"},
    "directory": {"en": "/directory", "es": "/es/directorio"},
    "glossary": {"en": "/glossary", "es": "/es/glosario"},
    "history": {"en": "/history", "es": "/es/historia"},
    "about": {"en": "/about", "es": "/es/acerca-de"},
    "events": {"en": "/events"},
    "contact": {"en": "/contact"},
    "blog": {"en": "/blog/"},
    "blog-first-jam": {"en": "/blog/five-things-before-your-first-jam"},
    "blog-weight-sharing": {"en": "/blog/weight-sharing-explained"},
    "blog-falling": {"en": "/blog/how-to-fall-without-getting-hurt"},
    "blog-consent": {"en": "/blog/consent-and-saying-no-mid-dance"},
    "blog-no-music": {"en": "/blog/why-there-is-no-music-at-a-jam"},
}

# The order the pages are written, ranked and listed in llms.txt. Purely presentational.
ORDER = [
    ("home", "en"), ("home", "es"),
    ("events", "en"), ("contact", "en"),
    ("blog", "en"), ("blog-first-jam", "en"), ("blog-weight-sharing", "en"),
    ("blog-falling", "en"), ("blog-consent", "en"), ("blog-no-music", "en"),
    ("what-is-contact-improvisation", "en"), ("what-is-contact-improvisation", "es"),
    ("miami", "en"), ("miami", "es"),
    ("miami-jams", "en"), ("miami-jams", "es"),
    ("jams", "en"), ("jams", "es"),
    ("friday-jam", "en"), ("friday-jam", "es"),
    ("classes", "en"), ("classes", "es"),
    ("your-first-jam", "en"), ("your-first-jam", "es"),
    ("keep-practising", "en"), ("keep-practising", "es"),
    ("videos", "en"), ("videos", "es"),
    ("directory", "en"), ("directory", "es"),
    ("glossary", "en"), ("glossary", "es"),
    ("history", "en"), ("history", "es"),
    ("safety-and-consent", "en"), ("safety-and-consent", "es"),
    ("faq", "en"), ("faq", "es"),
    ("about", "en"), ("about", "es"),
]


def route(slug, lang):
    """The route for a page, or None when that page does not exist in that locale."""
    return ROUTES.get(slug, {}).get(lang)


def slug_for(route_path, lang):
    """Reverse lookup: which page is this route? None when the route is not in the table.

    The shell uses this to derive the hreflang graph and the switcher from the path it
    was handed, so a page cannot be built with the wrong translation pair attached.
    """
    for slug, routes in ROUTES.items():
        if routes.get(lang) == route_path:
            return slug
    return None


def filename_for(route_path):
    """The output path for a route. `/` -> index.html, `/es/` -> es/index.html."""
    if route_path == "/":
        return "index.html"
    if route_path.endswith("/"):
        return route_path.strip("/") + "/index.html"
    return route_path.lstrip("/") + ".html"


def url_for(route_path):
    return SITE + route_path


def hreflang(lang):
    return HTML_LANG[lang]


def alternates(slug):
    """[(lang, url)] for every locale this slug exists in, in LOCALES order.

    Used for the reciprocal <link rel="alternate" hreflang> tags. A locale whose
    file is not in this table is never advertised, which is the rule that keeps a
    crawler out of a URL that does not exist.
    """
    out = []
    for lang in LOCALES:
        r = route(slug, lang)
        if r:
            out.append((lang, url_for(r)))
    return out


# Shown as the link title when the reader is being offered a different page in
# another language, because this one has no translation. Written in the language of
# the destination, which is the language of the reader who will act on it.
NO_TRANSLATION_TITLE = {
    "en": "This page has no translation yet",
    "es": "Esta página aún no está traducida",
}

# Every public page now exists in both locales, so no switcher link is a fallback any
# more. The map stays because switch_targets still supports a one-locale slug, and a
# future page added in English only must keep explaining itself.


def switch_targets(slug, lang):
    """What the switcher may offer on this page, and where each option goes.

    Returns [(locale, route, is_current, is_translation)]. Routes, not URLs: the
    switcher renders site-relative links like every other link on this site, so the
    internal-link check sees them and a broken one cannot hide behind an absolute URL.

    is_translation is False when the other locale has no version of this page and the
    link therefore goes to that locale's home. Such a link carries no hreflang:
    hreflang asserts "the same page, in another language", and a home page is not that.
    """
    out = []
    current_route = route(slug, lang)
    for other in LOCALES:
        if other == lang:
            if current_route:
                out.append((other, current_route, True, True))
            continue
        same_page = route(slug, other)
        if same_page:
            out.append((other, same_page, False, True))
            continue
        home = route("home", other)
        if home:
            out.append((other, home, False, False))
    return out
