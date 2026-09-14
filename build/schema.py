"""JSON-LD builders. Every page emits exactly one @graph, built here."""

import json

SITE = "https://miamicontactimprov.com"
ORG_ID = SITE + "/#organisation"
SITE_ID = SITE + "/#website"

# One canonical scope sentence and one disambiguation phrase, used by the schema
# below AND by llms.txt in build/build.py. tools/gate.py asserts on
# DISAMBIGUATION, so a page or discovery file that drops it fails the build.
SITE_SENTENCE = (
    "Miami Contact Improv is an independent, non-commercial community resource "
    "mapping Contact Improvisation practice across Miami-Dade and Broward County, Florida."
)
DISAMBIGUATION = "not a studio, organiser or membership body"
DISAMBIGUATING_DESCRIPTION = (
    SITE_SENTENCE
    + " It is "
    + DISAMBIGUATION
    + ": it runs no sessions, takes no bookings and charges no listing fee, and it is not "
    "miamiimprov.com, the comedy theatre that dominates search for the bare word 'improv'."
)


def _graph(nodes):
    return (
        '<script type="application/ld+json">\n'
        + json.dumps({"@context": "https://schema.org", "@graph": nodes}, indent=2, ensure_ascii=False)
        + "\n</script>"
    )


def organisation():
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "Miami Contact Improv",
        "alternateName": ["Miami CI", "miamicontactimprov.com"],
        "url": SITE + "/",
        "description": (
            "An independent, non-commercial community resource mapping Contact Improvisation "
            "practice across Miami-Dade and Broward County, Florida."
        ),
        "disambiguatingDescription": DISAMBIGUATING_DESCRIPTION,
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
        "inLanguage": "en-US",
    }


def website():
    return {
        "@type": "WebSite",
        "@id": SITE_ID,
        "url": SITE + "/",
        "name": "Miami Contact Improv",
        "inLanguage": "en-US",
        "publisher": {"@id": ORG_ID},
        "description": (
            "Jams, classes, teachers and video for Contact Improvisation in Miami, "
            "Miami Beach, Wynwood, Little Havana, Coral Gables and South Florida."
        ),
    }


def webpage(path, title, description, *, primary_image=None, about=None, date_modified="2026-09-13"):
    url = SITE + ("/" if path == "/" else path)
    node = {
        "@type": "WebPage",
        "@id": url + "#page",
        "url": url,
        "name": title,
        "description": description,
        "isPartOf": {"@id": SITE_ID},
        "inLanguage": "en-US",
        "datePublished": "2026-09-13",
        "dateModified": date_modified,
        "publisher": {"@id": ORG_ID},
    }
    if primary_image:
        node["primaryImageOfPage"] = {"@type": "ImageObject", "url": SITE + primary_image}
    if about:
        node["about"] = about
    return node


def breadcrumb(path, label):
    """Trail is always Home > <label>."""
    url = SITE + ("/" if path == "/" else path)
    return {
        "@type": "BreadcrumbList",
        "@id": url + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": label, "item": url},
        ],
    }


def faq(entries):
    return {
        "@type": "FAQPage",
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


def item_list(path, name, items):
    """items: list of (name, url, description). `path` may carry its own #fragment."""
    anchor = f"#{path.split('#', 1)[1]}" if "#" in path else "#list"
    page = path.split("#", 1)[0]
    return {
        "@type": "ItemList",
        "@id": SITE + page + anchor,
        "name": name,
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
