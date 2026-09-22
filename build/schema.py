"""JSON-LD builders. Every page emits exactly one @graph, built here."""

import json

import locales

SITE = "https://miamicontactimprov.com"
ORG_ID = SITE + "/#organisation"
SITE_ID = SITE + "/#website"


def _og_version():
    """Short content hash of site/assets/og.png. Link unfurlers (iMessage, Slack, WhatsApp,
    Facebook) and the CDN cache a social image by URL for days, so a new card at the same
    /assets/og.png keeps showing the old picture. A hash in the query string gives every
    new card a new URL."""
    import hashlib
    import pathlib
    p = pathlib.Path(__file__).resolve().parent.parent / "site" / "assets" / "og.png"
    try:
        return hashlib.md5(p.read_bytes()).hexdigest()[:8]
    except OSError:
        return "1"


OG_IMAGE = SITE + "/assets/og.png?v=" + _og_version()
ORG_NAME = "Miami Contact Improv"

# One canonical scope sentence and one disambiguation phrase PER LOCALE. These are the
# single source for the schema below, for the footer (shell.SITE_SENTENCE) and for
# llms.txt in build/build.py, and tools/gate.py reads the map back out of this module,
# so a page or discovery file that drops the disambiguation fails the build.
#
# The Spanish entries are translations of the identical claim, not a second claim:
# "no es un estudio ni organismo de membresía" asserts exactly what "not a studio or
# membership body" asserts, and nothing more.
#
# "organiser" left the phrase on 2026-09-17, when the site's maintainer started a weekly
# jam of his own (build/listings.py, FRIDAY_JAM_NAME). A property that hosts a session
# cannot describe itself as running none, so the tail now says exactly what it hosts.
SITE_SENTENCE_BY_LANG = {
    "en": (
        "Miami Contact Improv is an independent, non-commercial community resource "
        "mapping Contact Improvisation practice across Miami-Dade and Broward County, Florida."
    ),
    "es": (
        "Miami Contact Improv es un recurso comunitario independiente y sin ánimo de lucro "
        "que traza un mapa de la práctica de la Improvisación de Contacto en los condados "
        "de Miami-Dade y Broward, Florida."
    ),
}

DISAMBIGUATION_BY_LANG = {
    "en": "not a studio or membership body",
    "es": "no es un estudio ni organismo de membresía",
}

_DISAMBIGUATING_TAIL_BY_LANG = {
    "en": (
        ": it hosts one weekly community jam, on Fridays in Miami, listed on the same "
        "terms as every other session; it takes no bookings, charges no listing fee, and it is not "
        "miamiimprov.com, the comedy theatre that dominates search for the bare word 'improv'."
    ),
    "es": (
        ": organiza una única jam comunitaria semanal, los viernes en Miami, publicada "
        "en las mismas condiciones que cualquier otra sesión; no acepta reservas, no cobra por "
        "publicar, y no es miamiimprov.com, el teatro de comedia que domina las búsquedas de la "
        "palabra 'improv'."
    ),
}


def _sentence(lang):
    return SITE_SENTENCE_BY_LANG.get(lang, SITE_SENTENCE_BY_LANG["en"])


def disambiguation(lang):
    return DISAMBIGUATION_BY_LANG.get(lang, DISAMBIGUATION_BY_LANG["en"])


def disambiguating_description(lang):
    """Compose the sentence from the scope sentence + this locale's disambiguation phrase.

    The Spanish phrase already carries its own negation ("no es un estudio..."), because
    that is the substring the gate asserts and a reader needs the whole claim. So the
    Spanish branch capitalises it rather than prefixing another "No es" — which is
    exactly the "No es no es un estudio" this produced before it was caught.
    """
    tail = _DISAMBIGUATING_TAIL_BY_LANG.get(lang, _DISAMBIGUATING_TAIL_BY_LANG["en"])
    if lang == "en":
        return _sentence(lang) + " It is " + disambiguation("en") + tail
    phrase = disambiguation(lang)
    return _sentence(lang) + " " + phrase[:1].upper() + phrase[1:] + tail


# Backwards-compatible singular names. The English string stays reachable under the
# name existing callers and the gate already use, so removing it would be the change
# that breaks the check rather than the change that keeps it honest.
SITE_SENTENCE = SITE_SENTENCE_BY_LANG["en"]
DISAMBIGUATION = DISAMBIGUATION_BY_LANG["en"]
DISAMBIGUATING_DESCRIPTION = disambiguating_description("en")


def _graph(nodes):
    return (
        '<script type="application/ld+json">\n'
        + json.dumps({"@context": "https://schema.org", "@graph": nodes}, indent=2, ensure_ascii=False)
        + "\n</script>"
    )


def organisation(lang="en"):
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": ORG_NAME,
        "alternateName": ["Miami CI", "miamicontactimprov.com"],
        "url": SITE + "/",
        "sameAs": ["https://www.instagram.com/miamicontactimprov/"],
        "description": _sentence(lang),
        "disambiguatingDescription": disambiguating_description(lang),
        "foundingDate": "2026-09-13",
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "Miami-Dade County, Florida"},
            {"@type": "AdministrativeArea", "name": "Broward County, Florida"},
            {"@type": "City", "name": "Miami"},
            {"@type": "City", "name": "Miami Beach"},
            {"@type": "City", "name": "Coral Gables"},
            {"@type": "City", "name": "Wynwood"},
            {"@type": "City", "name": "Little Havana"},
            {"@type": "City", "name": "Hialeah"},
            {"@type": "City", "name": "Doral"},
            {"@type": "City", "name": "Fort Lauderdale"},
            {"@type": "City", "name": "Hallandale Beach"},
        ],
        "knowsAbout": [
            "contact improvisation",
            "contact improv",
            "dance jams",
            "improvisational dance",
            "somatic movement",
            "weight sharing",
            "contact dance",
            "movement research",
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "community submissions",
            "email": "hello@miamicontactimprov.com",
            "availableLanguage": ["en", "es"],
        },
        "inLanguage": locales.SCHEMA_LANG.get(lang, "en-US"),
    }


def website(lang="en"):
    return {
        "@type": "WebSite",
        "@id": SITE_ID,
        "url": SITE + "/",
        "name": ORG_NAME,
        "inLanguage": locales.SCHEMA_LANG.get(lang, "en-US"),
        "publisher": {"@id": ORG_ID},
        "description": (
            "Jams, classes, teachers and video for Contact Improvisation in Miami, "
            "Miami Beach, Wynwood, Little Havana, Coral Gables and South Florida."
        ),
    }


def webpage(path, title, description, *, primary_image=None, about=None,
            date_modified="2026-09-13", lang="en"):
    url = SITE + ("/" if path == "/" else path)
    node = {
        "@type": "WebPage",
        "@id": url + "#page",
        "url": url,
        "name": title,
        "description": description,
        "isPartOf": {"@id": SITE_ID},
        "inLanguage": locales.SCHEMA_LANG.get(lang, "en-US"),
        "datePublished": "2026-09-13",
        "dateModified": date_modified,
        "publisher": {"@id": ORG_ID},
    }
    if primary_image:
        node["primaryImageOfPage"] = {"@type": "ImageObject", "url": SITE + primary_image}
    if about:
        node["about"] = about
    return node


def breadcrumb(path, label, lang="en"):
    """Trail is always Home > <label>. "Home" is translated, because a Spanish reader
    reading "Home" learns nothing about where the link goes."""
    url = SITE + ("/" if path == "/" else path)
    root = "Inicio" if lang == "es" else "Home"
    return {
        "@type": "BreadcrumbList",
        "@id": url + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": root, "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": label, "item": url},
        ],
    }


def faq(entries, lang="en"):
    return {
        "@type": "FAQPage",
        "inLanguage": locales.SCHEMA_LANG.get(lang, "en-US"),
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in entries
        ],
    }


def defined_terms(terms, path="/glossary", alternates=None):
    """terms: list of (slug, name, definition). alternates: {slug: alternateName}.

    One @id per term site-wide. A retired synonym stays retrievable as an
    alternateName rather than becoming a second competing DefinedTerm.
    """
    alternates = alternates or {}

    def term_node(slug, name, definition):
        node = {
            "@type": "DefinedTerm",
            "@id": SITE + path + "#" + slug,
            "name": name,
            "description": definition,
            "inDefinedTermSet": {"@id": SITE + path + "#terms"},
        }
        if alternates.get(slug):
            node["alternateName"] = alternates[slug]
        return node

    return {
        "@type": "DefinedTermSet",
        "@id": SITE + path + "#terms",
        "name": "Contact Improvisation glossary",
        "description": (
            "Working vocabulary of Contact Improvisation: jam, score, small dance, "
            "underscore, weight sharing, landing, spotting and related terms."
        ),
        "hasDefinedTerm": [
            term_node(slug, name, definition) for slug, name, definition in terms
        ],
    }


def item_list(path, name, items, lang="en"):
    """items: list of (name, url, description). `path` may carry its own #fragment."""
    anchor = f"#{path.split('#', 1)[1]}" if "#" in path else "#list"
    page = path.split("#", 1)[0]
    return {
        "@type": "ItemList",
        "@id": SITE + page + anchor,
        "name": name,
        "inLanguage": locales.SCHEMA_LANG.get(lang, "en-US"),
        "itemListOrder": "https://schema.org/ItemListUnordered",
        "numberOfItems": len(items),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": n,
                "url": u,
                **({"description": d} if d else {}),
            }
            for i, (n, u, d) in enumerate(items)
        ],
    }


def video_objects(entries, path="/videos"):
    """entries: dicts with title, description, and EITHER
    embed + url + channel (someone else's film, embedded from its platform) OR
    content + url + thumbnail (+ optional duration) served from this domain.

    Attribution rule, and the reason this is spelled out: a VideoObject carrying an
    embedUrl is someone else's work, so the credit goes to that channel by name and
    this site is never its creator or publisher. Only an entry whose contentUrl is
    hosted on this domain may name this site. Getting this backwards puts this
    site's name on a film it did not make, which is a false claim in a search result.
    """
    def channel_node(name, url):
        # The upload channel is the only attribution the platform actually publishes,
        # so it is what gets credited. No individual creator is invented for a film
        # whose channel does not state one.
        node = {"@type": "Organization", "name": name}
        if url:
            node["url"] = url
        return node

    def node(e):
        n = {
            "@type": "VideoObject",
            "name": e["title"],
            "description": e["description"],
            "isFamilyFriendly": True,
        }
        if e.get("embed"):
            n["embedUrl"] = e["embed"]
            n["url"] = e["url"]
            if e.get("thumbnail"):
                n["thumbnailUrl"] = e["thumbnail"]
            credit = channel_node(e["channel"], e.get("url"))
            n["creator"] = credit
            n["publisher"] = credit
        else:
            n["contentUrl"] = e["content"]
            n["url"] = e["url"]
            n["thumbnailUrl"] = e["thumbnail"]
            # Ours, and only here may the site's own Organization be the credit.
            n["creator"] = {"@id": ORG_ID}
            n["publisher"] = {"@id": ORG_ID}
            if e.get("duration"):
                n["duration"] = e["duration"]
            if e.get("filmed_on"):
                n["dateCreated"] = e["filmed_on"]
        # uploadDate and thumbnailUrl are only emitted when actually verified upstream.
        if e.get("upload"):
            n["uploadDate"] = e["upload"]
        return n

    return {
        "@type": "ItemList",
        "@id": SITE + path + "#videos",
        "name": "Contact Improvisation video room",
        "numberOfItems": len(entries),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": node(e)}
            for i, e in enumerate(entries)
        ],
    }


def _flatten(nodes):
    """A builder may hand back a single node, a node, or a list of nodes. Flatten one level.

    Without this, a builder returning a list put a bare array inside @graph, which the
    validator then walked as if it were a node and crashed on.
    """
    out = []
    for n in nodes:
        if n is None or n == [] or n == {}:
            continue
        if isinstance(n, list):
            out.extend(x for x in n if x)
        else:
            out.append(n)
    return out


def render(*nodes):
    return _graph(_flatten(nodes))
