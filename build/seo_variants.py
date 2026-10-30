"""Variant copy for the SEO Phase 1 experiment (seo-p1-2026-11).

Each table is keyed by route. A page not listed for a flag has no variant for it and always
renders control. `apply()` post-processes a finished English page: control pages come back
byte-identical apart from the seo-variants meta tag.

H015 (open FAQ) has no table on purpose: no page on this site hides FAQ answers in an
accordion or <details>. Every answer is already plain visible HTML, so there is nothing to
open and nothing to test.
"""

import re

import seo_flags

# H003. Keyword first, concrete benefit, brand last, <= 60 characters.
TITLES = {
    "/what-is-contact-improvisation": "What Is Contact Improv? Plain Answer | Miami Contact Improv",
    "/miami": "Contact Improv in Miami: Start Here | Miami Contact Improv",
    "/miami-jams": "Contact Improv Jams in Miami | Miami Contact Improv",
    "/jams": "Contact Improv Jams: What to Expect | Miami Contact Improv",
    "/friday-jam": "Friday Contact Improv Jam, 7-9 PM | Miami Contact Improv",
    "/fundamentals": "Contact Improv Classes: 8 Fridays | Miami Contact Improv",
    "/classes": "Contact Improv Classes for Beginners | Miami Contact Improv",
    "/your-first-jam": "First Contact Improv Jam Walkthrough | Miami Contact Improv",
    "/safety-and-consent": "Contact Improv Consent: Your Rights | Miami Contact Improv",
    "/glossary": "Contact Improv Glossary for Jams | Miami Contact Improv",
    "/history": "Contact Improv History, 1972 to Now | Miami Contact Improv",
    "/keep-practising": "How to Keep Practising Contact Improv | Miami Contact Improv",
    "/directory": "Contact Improv Directory: Who to Ask | Miami Contact Improv",
    "/faq": "Contact Improv FAQ: Jams & Consent | Miami Contact Improv",
}

# H013. (old, new) exact substitutions inside the page: the H1 and the start of the lede.
# Slugs and URLs never change. An entry that no longer matches the page raises at build time.
KEYWORD = {
    "/what-is-contact-improvisation": [
        ("A partnered dance you cannot rehearse,",
         "Contact Improvisation is a partnered dance you cannot rehearse,"),
    ],
    "/miami": [
        ("Miami is a city of borrowed rooms and unofficial scenes. Contact improvisation here runs the same way:",
         "Contact improvisation in Miami runs on borrowed rooms and unofficial scenes:"),
    ],
    "/miami-jams": [
        ("<h1>Every contact improv session in Miami-Dade and Broward we could verify.</h1>",
         "<h1>Contact improv jams and classes in Miami-Dade and Broward: every session we could verify.</h1>"),
    ],
    "/jams": [
        ("<h1>Jams: the room is the teacher.</h1>", "<h1>Contact improv jams: the room is the teacher.</h1>"),
        ("A jam is where Contact Improvisation actually lives.",
         "A contact improv jam is where Contact Improvisation actually lives."),
    ],
    "/friday-jam": [
        ("<h1>The Friday jam in Miami.</h1>", "<h1>The Friday contact improv jam in Miami.</h1>"),
        ("A weekly open Contact Improvisation jam at Inner Motion",
         "The weekly contact improv jam in Miami, open to everyone, at Inner Motion"),
    ],
    "/fundamentals": [
        ("<h1>Contact improv fundamentals: eight Fridays from the ground up.</h1>",
         "<h1>Contact improv fundamentals in Miami: eight Fridays from the ground up.</h1>"),
        ("A taught class series that starts Contact Improvisation",
         "Contact improv fundamentals in Miami is a taught class series that starts Contact Improvisation"),
    ],
    "/classes": [
        ("<h1>Classes, workshops and your first jam.</h1>",
         "<h1>Contact improv classes, workshops and your first jam.</h1>"),
        ("You can start Contact Improvisation with no dance background at all.",
         "Contact improv classes in Miami need no dance background at all."),
    ],
    "/your-first-jam": [
        ("Nobody at a jam is assessing you.", "Nobody at your first contact improv jam is assessing you."),
    ],
    "/safety-and-consent": [
        ("<h1>Safety and consent are the technique.</h1>",
         "<h1>Contact improv safety and consent are the technique.</h1>"),
    ],
    "/glossary": [
        ("<h1>The words people use in the room.</h1>",
         "<h1>Contact improv glossary: the words people use in the room.</h1>"),
    ],
    "/history": [
        ("<h1>Where Contact Improvisation came from.</h1>",
         "<h1>The history of Contact Improvisation: where it came from.</h1>"),
        ("It started in a college gymnasium", "Contact Improvisation started in a college gymnasium"),
    ],
    "/keep-practising": [
        ("The part that follows your first visit:", "Keeping up contact improv after your first visit:"),
    ],
    "/directory": [
        ("<h1>Who to ask, and where the map continues.</h1>",
         "<h1>Contact improv directory: who to ask, and where the map continues.</h1>"),
        ("Local organisers and studios first,", "Local contact improv organisers and studios first,"),
    ],
    "/faq": [
        ("<h1>Everything people ask about this dance.</h1>",
         "<h1>Contact improvisation FAQ: everything people ask about this dance.</h1>"),
        ("Answered in the first sentence,", "Contact improv questions, answered in the first sentence,"),
    ],
}

# H014. 40-60 words, answer first, plain visible text, inserted right under the H1.
TLDR = {
    "/what-is-contact-improvisation": "Contact Improvisation is a partnered, improvised dance Steve Paxton developed in 1972. Two or more dancers keep a moving point of contact and trade weight through gravity and momentum. There are no set steps, no licensing body and no dance training required, which is why most people try it first at an open jam.",
    "/miami": "Contact improv in Miami has no central venue and no shared calendar. Sessions run through individual organisers and rented studios, so finding one means asking around. This page explains how the local scene works. For a weekly session we can verify, start with the Friday jam in Hallandale Beach or the jam list.",
    "/miami-jams": "Every entry on this page names the organiser, the room, the price and the date we last checked it. The weekly ones are a Tuesday class at Dance Arts Miami and a Friday open jam at Inner Motion Dance Studio in Hallandale Beach. Anything we could not verify is left off, and the page says so.",
    "/jams": "A contact improv jam is an open session with no teacher and little or no music. You arrive, dance with whoever is willing or sit and watch, and leave when you like. You can decline any invitation. In Miami, the weekly one is the Friday jam at Inner Motion Dance Studio in Hallandale Beach.",
    "/friday-jam": "The Friday jam is a weekly open contact improv session at Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, from 7 to 9 PM, starting 2 October 2026. It costs $20 at the door on a $20 to $50 sliding scale. You need no partner, no experience and no booking.",
    "/fundamentals": "Fundamentals is eight Friday contact improv classes, 7 to 9 PM at Inner Motion Dance Studio in Hallandale Beach, from 2 October to 20 November 2026. Each class stands alone, so join any week. Max Petrusenko teaches it. It costs $20 online or $30 to $50 at the door, pay what you can, with no partner or experience needed.",
    "/classes": "A contact improv class teaches the skills underneath the dance: sharing weight without collapsing, rolling out of a fall, reading a partner's momentum and saying no. Beginner classes assume no dance training. Most people take classes for a few weeks, then add a weekly jam, because the form is learned mostly by dancing.",
    "/your-first-jam": "At your first contact improv jam you arrive, warm up, and usually join a short circle where the hosts state the consent rules. Then dancing starts and stops around you. Nobody expects you to dance with anyone. Sitting at the edge for the whole session is normal, and leaving early is always fine.",
    "/safety-and-consent": "In contact improv, consent is continuous. You can decline an invitation, slow down, pause, change what you are doing or leave a dance at any point, without explaining. Jams have no teacher or supervisor, so whoever hosts the session is responsible for stating the protocol and acting when someone breaks it.",
    "/glossary": "The terms you will hear most at a contact improv jam: contact, the point where two bodies touch; weight sharing, giving and receiving body weight; the small dance, the standing practice that opens a session; a score, a stated constraint; the jam, an open session with no teacher; and spotting, standing ready to catch a fall.",
    "/history": "Steve Paxton developed contact improvisation in 1972, after a residency at Oberlin College in January and performances at the John Weber Gallery in New York in June. It drew on modern dance, aikido and somatic practice. In 1975 the dancers decided against trademarking or licensing it, and it has stayed unowned.",
    "/keep-practising": "You keep practising contact improv by going back: a weekly jam or class, plus a little solo practice in the weeks when nothing is running. The form is learned in the room, not between sessions. This page covers what happens after your first visit, including what to do when nothing is on.",
    "/directory": "Contact improv has no central directory because it has no central body, so listings sit with the organisers. The nearest thing to a global index is the CI World Jam Map at contactimprov.com, which has a Florida page. This directory starts with local organisers and studios, then lists international resources.",
    "/faq": "These are the questions people ask most about contact improv: what it is, what to wear, whether you need a partner, how consent works and how jams and classes run in Miami. Each answer opens with a direct sentence, so you can read the first line and move on if that is enough.",
}

# H022. 3-5 contextual links to other public pages, descriptive anchors.
RELATED = {
    "/what-is-contact-improvisation": [
        ("/history", "The history of Contact Improvisation, from Oberlin to now"),
        ("/glossary", "Contact improv glossary: the words used in a jam"),
        ("/safety-and-consent", "How consent works in contact improv"),
        ("/your-first-jam", "What happens at your first contact improv jam"),
    ],
    "/miami": [
        ("/miami-jams", "Every contact improv jam and class we could verify in Miami-Dade and Broward"),
        ("/friday-jam", "The Friday contact improv jam in Hallandale Beach"),
        ("/directory", "Contact improv organisers, studios and global resources"),
        ("/classes", "Contact improv classes for beginners"),
    ],
    "/miami-jams": [
        ("/friday-jam", "The Friday jam: time, place and price"),
        ("/fundamentals", "Contact improv fundamentals, eight Fridays"),
        ("/your-first-jam", "What to expect at your first jam"),
        ("/miami", "How the Miami contact improv scene works"),
    ],
    "/jams": [
        ("/your-first-jam", "Your first contact improv jam, step by step"),
        ("/safety-and-consent", "Safety and consent at a contact improv jam"),
        ("/friday-jam", "The Friday jam in Hallandale Beach"),
        ("/miami-jams", "Verified contact improv sessions in Miami-Dade and Broward"),
    ],
    "/friday-jam": [
        ("/pricing", "What a contact improv class or jam costs"),
        ("/fundamentals", "The eight-week Fundamentals class series"),
        ("/your-first-jam", "What to expect at your first jam"),
        ("/safety-and-consent", "How consent works in the room"),
    ],
    "/fundamentals": [
        ("/friday-jam", "The Friday contact improv jam that follows each class"),
        ("/classes", "More on contact improv classes and what teachers teach"),
        ("/pricing", "Class and jam pricing"),
        ("/glossary", "Contact improv glossary"),
    ],
    "/classes": [
        ("/fundamentals", "Contact improv fundamentals: eight Fridays in Hallandale Beach"),
        ("/your-first-jam", "Your first contact improv jam"),
        ("/keep-practising", "How to keep practising between sessions"),
        ("/safety-and-consent", "Safety and consent in contact improv"),
    ],
    "/your-first-jam": [
        ("/jams", "What a contact improv jam is"),
        ("/safety-and-consent", "Consent and your rights in the room"),
        ("/friday-jam", "A weekly beginner-friendly jam in Hallandale Beach"),
        ("/keep-practising", "What to do after your first jam"),
    ],
    "/safety-and-consent": [
        ("/your-first-jam", "What happens at your first contact improv jam"),
        ("/jams", "How a contact improv jam is run"),
        ("/glossary", "Contact improv glossary"),
        ("/faq", "Contact improv questions answered"),
    ],
    "/glossary": [
        ("/what-is-contact-improvisation", "What Contact Improvisation is"),
        ("/jams", "How a contact improv jam works"),
        ("/safety-and-consent", "Consent and safety in contact improv"),
        ("/history", "Where the vocabulary came from: a history of the form"),
    ],
    "/history": [
        ("/what-is-contact-improvisation", "What Contact Improvisation is"),
        ("/glossary", "Contact improv glossary"),
        ("/miami", "Contact improvisation in Miami"),
        ("/videos", "Contact improv films from the people who made them"),
    ],
    "/keep-practising": [
        ("/jams", "How contact improv jams work"),
        ("/friday-jam", "The weekly Friday jam in Hallandale Beach"),
        ("/classes", "Contact improv classes"),
        ("/videos", "Contact improv videos to practise from"),
    ],
    "/directory": [
        ("/miami-jams", "Verified contact improv sessions in Miami-Dade and Broward"),
        ("/miami", "How the Miami contact improv scene works"),
        ("/classes", "Contact improv classes"),
        ("/what-is-contact-improvisation", "What Contact Improvisation is"),
    ],
    "/faq": [
        ("/what-is-contact-improvisation", "What Contact Improvisation is"),
        ("/your-first-jam", "Your first contact improv jam"),
        ("/safety-and-consent", "Safety and consent in contact improv"),
        ("/miami-jams", "Contact improv jams in Miami-Dade and Broward"),
    ],
}

TABLES = {
    "seo_h003_titles": TITLES,
    "seo_h013_keyword_placement": KEYWORD,
    "seo_h014_tldr": TLDR,
    "seo_h022_internal_links": RELATED,
}

# H021: transactional pages that stay reachable but should not be indexed or listed.
PRIVATE_ROUTES = ("/pay", "/success")


def has_content(key, path):
    return path in TABLES.get(key, {})


def is_private(path):
    return seo_flags.site_enabled("seo_h021_indexing") and seo_flags.normalize_path(path) in PRIVATE_ROUTES


def _once(html, old, new, route):
    if html.count(old) != 1:
        raise SystemExit(f"seo_variants: {route}: expected exactly one match for {old[:60]!r}, got {html.count(old)}")
    return html.replace(old, new)


def _related_html(links):
    items = "".join(f'<li><a href="{href}">{label}</a></li>' for href, label in links)
    return (
        '<section class="section"><div class="wrap"><h2>Related</h2>'
        f'<div class="prose"><ul>{items}</ul></div></div></section>'
    )


def apply(html, path, lang="en"):
    """Return `html` with this page's variants applied and the seo-variants meta added."""
    route = seo_flags.normalize_path(path)
    en = lang == "en"
    variants = seo_flags.variant_map(
        route, (lambda key: en and has_content(key, route)))
    if en:
        if variants["h003"] == "v":
            m = re.search(r"<title>(.*?)</title>", html, re.S)
            old, new = m.group(1), TITLES[route].replace("&", "&amp;")
            for pat in ("<title>{}</title>", '<meta property="og:title" content="{}">',
                        '<meta name="twitter:title" content="{}">'):
                html = _once(html, pat.format(old), pat.format(new), route)
        if variants["h013"] == "v":
            for old, new in KEYWORD[route]:
                html = _once(html, old, new, route)
        if variants["h014"] == "v":
            block = f'<div class="answer"><div class="label">TL;DR</div><p>{TLDR[route]}</p></div>'
            html = _once(html, "</h1>", "</h1>\n    " + block, route)
        if variants["h022"] == "v":
            html = _once(html, "\n</main>", "\n" + _related_html(RELATED[route]) + "\n</main>", route)
    if is_private(route):
        html = _once(html, 'content="index, follow, max-image-preview:large, max-snippet:-1"',
                     'content="noindex, follow"', route)
    return _once(html, '<meta name="theme-color"', seo_flags.meta_tag(variants) + '\n<meta name="theme-color"', route)
