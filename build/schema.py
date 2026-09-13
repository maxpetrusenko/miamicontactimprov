"""JSON-LD builders. Every page emits exactly one @graph, built here."""

import json

SITE = "https://miamicontactimprov.com"
ORG_ID = SITE + "/#organisation"
SITE_ID = SITE + "/#website"


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


def defined_terms(terms, path="/glossary"):
    return {
        "@type": "DefinedTermSet",
        "@id": SITE + path + "#terms",
        "name": "Contact Improvisation glossary",
        "description": (
            "Working vocabulary of Contact Improvisation: jam, score, small dance, "
            "underscore, weight sharing, landing, spotting and related terms."
        ),
        "hasDefinedTerm": [
            {
                "@type": "DefinedTerm",
                "@id": SITE + path + "#" + slug,
                "name": name,
                "description": definition,
                "inDefinedTermSet": {"@id": SITE + path + "#terms"},
            }
            for slug, name, definition in terms
        ],
    }


def item_list(path, name, items):
    """items: list of (name, url, description)."""
    return {
        "@type": "ItemList",
        "@id": SITE + path + "#list",
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
    """entries: list of dicts with title, description, thumbnail, embed, url, channel."""
    def node(e):
        n = {
            "@type": "VideoObject",
            "name": e["title"],
            "description": e["description"],
            "thumbnailUrl": e["thumbnail"],
            "embedUrl": e["embed"],
            "url": e["url"],
            "publisher": {"@type": "Organization", "name": e["channel"]},
            "isFamilyFriendly": True,
        }
        # uploadDate is only emitted when it has actually been verified upstream.
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


def render(*nodes):
    return _graph([n for n in nodes if n])
