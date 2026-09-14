"""Confirmed local listings for the Miami pages.

Rules for this file, enforced by review rather than by code:
  * Every entry was opened and read. `verified` is the date the source was last seen live.
  * Nothing is inferred. `modality` states what the organiser actually advertises, so a
    contact-adjacent practice is never presented as Contact Improvisation.
  * An empty list is a valid, honest state. Deleting a dead entry is a normal change.
  * No prices are copied unless the organiser publishes them on the page we link to.

Verified 2026-09-13.
"""

import html
import schema

VERIFIED = "2026-09-13"

# name, modality, city, venue, schedule, cost, url, verified, note
SESSIONS = [
    (
        "Contact Improv \u2014 ALL LEVELS",
        "Contact Improvisation",
        "Miami",
        "Dance Arts Miami, 250 NE 61st Street, Miami, FL 33137",
        "Weekly, Tuesdays 6:00\u20137:00 PM EDT",
        "Set by the organiser; see the listing",
        "https://www.eventbrite.com/e/contact-improv-all-levels-tickets-1999219825315",
        VERIFIED,
        "The most established recurring Contact Improvisation class found in Miami-Dade. Advertised as "
        "exploring connection, weight sharing, momentum and spontaneous partnering, with no partner needed. "
        "Listed as a multi-date series on Eventbrite and mirrored on Meetup and SweatPals, so the studio's "
        "own site is not the authoritative place to check it. Confirm the current week before travelling.",
    ),
    (
        "Kama Flight \u2014 Flight Workshop",
        "Contact-adjacent (acro yoga, Thai massage, Contact Improvisation)",
        "Miami",
        "Skanda Yoga, Miami, FL",
        "October 18, 2026 and November 15, 2026",
        "Published on the organiser's own product pages",
        "https://kamaflight.com/products/flight-workshop-miami-fl-october-18-2026",
        VERIFIED,
        "Described by the organisers as a fusion of acro yoga, Thai massage and Contact Improvisation. Proceeds "
        "fund the Kama Flight Foundation, a registered 501(c)(3) nonprofit. Booked in pairs with friends "
        "welcome, which makes it a gentler first step than an open jam if physical contact with strangers "
        "is the thing giving you pause.",
    ),
    (
        "Kama Flight \u2014 jams and Kama Floor workshops",
        "Contact-adjacent (acro yoga, Thai massage, Contact Improvisation)",
        "Miami Beach",
        "Private residence, 2345 N Bay Road, Miami Beach, FL 33140 (parking on Alton Road)",
        "Recurring; dates published individually",
        "Donation-based for jams",
        "https://kamaflight.com/",
        VERIFIED,
        "Recurring donation-based jams and floor workshops. Because these run in a private residence and "
        "the dates are published one at a time, always check the organiser's own page for the next date "
        "rather than relying on any listing, including this one.",
    ),
    (
        "Camp Contact at Love Burn",
        "Contact Improvisation (as a core camp offering)",
        "Miami",
        "Historic Virginia Key Beach Park, 4020 Virginia Beach Drive, Miami, FL 33149",
        "February, annually",
        "Festival ticket",
        "https://loveburn.campcontact.org/",
        VERIFIED,
        "Love Burn is Miami's Burning Man regional, held on Virginia Key, and Camp Contact runs contact "
        "improvisation, acro yoga, ecstatic dance and authentic relating as its programme. This is the "
        "largest concentration of contact improvisation that happens in Miami in a year, and it is a "
        "festival rather than a class. Dates move, so read the organiser's page.",
    ),
]

# name, kind, city, url, verified, note
ORGS = [
    (
        "Karen Peterson Dancers",
        "Physically integrated dance company",
        "Miami",
        "https://www.karenpetersondancers.org/",
        VERIFIED,
        "A Miami company working with dancers with and without disabilities, running the Forward Motion "
        "Dance Festival and residencies across Miami-Dade schools. Its studio work has historically been "
        "connected to contact practice in the city, and its founder's name is the one attached to the "
        "Miami jam still listed on the CI World Jam Map. The company itself is active and current; the "
        "jam listing on the world map is not dated, so this site does not present it as running.",
    ),
    (
        "Dance Arts Miami",
        "Dance studio (ballet, modern, social, adult classes)",
        "Miami",
        "https://danceartsmiami.com/schedule",
        VERIFIED,
        "Hosts the weekly Contact Improv \u2014 ALL LEVELS class and runs a broad adult programme. "
        "Its own schedule page did not surface a dedicated contact improvisation entry when checked, "
        "so the class listing is verified through Eventbrite and Meetup rather than here.",
    ),
    (
        "Kama Flight",
        "Movement studio and 501(c)(3) foundation",
        "Miami and Miami Beach",
        "https://kamaflight.com/",
        VERIFIED,
        "Acro yoga, Thai massage and Contact Improvisation. Runs workshops, jams and teacher trainings, and "
        "publishes its own code of conduct.",
    ),
    (
        "Ecstatic Dance Miami",
        "Conscious dance community (contact-adjacent)",
        "Miami",
        "https://ecstaticdancemiami.com/",
        VERIFIED,
        "Running since 2014, with gatherings around the full moon. Some events sequence yoga, contact "
        "improvisation and ecstatic dance in one evening, so it is a realistic way into the wider "
        "Miami movement community even though the dancing is not CI.",
    ),
    (
        "EXPANSION Ecstatic Dance",
        "Conscious dance series (contact-adjacent)",
        "Miami (Edgewater, Little Haiti, Ironside)",
        "https://ecstatic-flow.com/",
        VERIFIED,
        "A recurring series with rotating venues including Boho Miami and Lion's Den. Some editions "
        "include partner embodiment work.",
    ),
    (
        "Love Burn",
        "Burning Man regional festival",
        "Miami",
        "https://theloveburn.com/",
        VERIFIED,
        "Miami's regional burn, held annually on Virginia Key. The place contact improvisation reaches "
        "its largest Miami audience, through Camp Contact.",
    ),
]

# name, discipline, city, url, verified, note
ADJACENT = [
    (
        "Nathan Shultz",
        "5Rhythms (teacher in training), breathwork, yoga",
        "Miami Beach",
        "https://5rhythms.com/teachers/Nathan+Shultz",
        VERIFIED,
        "Teaches at Hanu Wellness, 736 6th Street, Miami Beach. 5Rhythms is conscious movement, not "
        "contact improvisation. Listed here because the two communities overlap heavily in practice "
        "and in people.",
    ),
    (
        "Liliana De La Vega",
        "5Rhythms (certified, Waves)",
        "Miami",
        "https://5rhythms.com/teachers/Liliana+De+La+Vega",
        VERIFIED,
        "Certified 5Rhythms teacher, dancing since 2018 and teaching since 2024. Works in Spanish and "
        "English. Again: a different practice, adjacent community.",
    ),
]


def _rows(rows, kind, heading, blurb):
    if not rows:
        return ""
    items = []
    for name, modality, city, venue, schedule, cost, url, verified, note in rows:
        items.append(
            f"<li><p><strong>{html.escape(name)}</strong> &middot; {html.escape(modality)}</p>"
            f"<p>{html.escape(venue)}</p>"
            f"<p>{html.escape(schedule)}. {html.escape(cost)}.</p>"
            f"<p>{html.escape(note)}</p>"
            f'<p><a href="{html.escape(url)}" rel="noopener nofollow">The organiser\'s own listing</a> '
            f"&middot; checked {verified}</p></li>"
        )
    return (
        f'<div class="prose"><h2>{heading}</h2><p>{blurb}</p>'
        f'<ul class="dir-list">{"".join(items)}</ul></div>'
    )


def _org_rows(rows, heading, blurb):
    """Studio / organisation entries: name, kind, city, url, verified, note."""
    if not rows:
        return ""
    items = []
    for name, kind, city, url, verified, note in rows:
        items.append(
            f"<li><p><a href=\"{html.escape(url)}\" rel=\"noopener nofollow\"><strong>{html.escape(name)}</strong></a>"
            f" &middot; {html.escape(kind)}</p>"
            f"<p>{html.escape(city)}</p>"
            f"<p>{html.escape(note)}</p>"
            f"<p>Checked {verified}</p></li>"
        )
    return (
        f'<div class="prose"><h2>{heading}</h2><p>{blurb}</p>'
        f'<ul class="dir-list">{"".join(items)}</ul></div>'
    )


def sessions_block():
    return _rows(
        SESSIONS, "sessions",
        "Recurring sessions in Miami we have verified",
        "Each of these was checked against the organiser's own page on the date shown. Schedules change, "
        "so confirm before you travel. Nothing on this list is paid for, sponsored, or added without the "
        "organiser's own page saying it.",
    )


def sessions_or_none():
    """The honest fallback, used if every session entry is ever removed."""
    return (
        '<div class="prose"><h2>Recurring sessions in Miami we have verified</h2>'
        "<p>Nothing currently. This site removes listings rather than leaving stale ones, so an empty "
        "list means an empty verified list, not an empty city. The studios and organisations below are "
        "where the answer actually lives.</p></div>"
    )


def orgs_block():
    return _org_rows(
        ORGS,
        "Studios, companies and organisers",
        "Every one of these was opened and checked. Where an organisation is contact-adjacent rather "
        "than a contact improvisation outfit, the entry says so.",
    )


def adjacent_block():
    return _org_rows(
        ADJACENT,
        "Adjacent practice, honestly labelled",
        "Different disciplines with heavily overlapping communities. Listed because a newcomer looking "
        "for this kind of movement in Miami will meet these people anyway, and because pretending "
        "otherwise would be the sort of directory that wastes your evening.",
    )


def teachers_note():
    return (
        '<div class="prose"><h2 id="teachers">Teachers</h2>'
        "<p>There is no register of Contact Improvisation teachers, anywhere, because the form was never "
        "trademarked and never certificated. That was a deliberate decision in 1975 and this site is not "
        "going to invent the authority that the form's own founders refused.</p>"
        "<p>So the honest position on Miami: <strong>no Miami-based Contact Improvisation teacher could be "
        "confirmed from their own published information</strong> at the time of writing. Individual names "
        "appear in legacy CI member directories from around 2010 and in social media posts, and none of "
        "those are current enough to publish. The people who actually know are the organisations below, "
        "and the fastest route is to ask the one hosting the class you are thinking of attending.</p>"
        '<p>If you teach here, <a href="/about#submit">send us your page</a>. A teacher listing on this '
        "site means one thing only: this person publishes what they teach and where. It is not an "
        "endorsement, and it cannot be, in a form with no assessor.</p></div>"
    )


# ---------------------------------------------------------------- schema

def _parse(s):
    """'October 18, 2026 and November 15, 2026' -> ['2026-10-18', '2026-11-15']"""
    import re
    months = {m: i + 1 for i, m in enumerate(
        ["January", "February", "March", "April", "May", "June", "July", "August",
         "September", "October", "November", "December"])}
    out = []
    for mon, day, year in re.findall(r"([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})", s):
        if mon in months:
            out.append(f"{year}-{months[mon]:02d}-{int(day):02d}")
    return out


EVENT_DATES = {
    "Kama Flight \u2014 Flight Workshop": [
        ("2026-10-18", "Skanda Yoga, Miami, FL"),
        ("2026-11-15", "Skanda Yoga, Miami, FL"),
    ],
}


def events_schema():
    """Only events with a date read off the organiser's own page are emitted."""
    nodes = []
    for name, modality, city, venue, schedule, cost, url, verified, note in SESSIONS:
        dates = EVENT_DATES.get(name)
        if not dates:
            continue
        for iso, location in dates:
            nodes.append({
                "@type": "Event",
                "@id": f"{schema.SITE}/jams#{iso}-kama-flight",
                "name": name,
                "description": note,
                "startDate": iso,
                "eventStatus": "https://schema.org/EventScheduled",
                "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "location": {
                    "@type": "Place",
                    "name": location,
                    "address": {"@type": "PostalAddress", "addressLocality": "Miami",
                                "addressRegion": "FL", "addressCountry": "US"},
                },
                "organizer": {"@type": "Organization", "name": "Kama Flight", "url": "https://kamaflight.com/"},
                "url": url,
                "image": schema.SITE + "/assets/og.png",
                "isAccessibleForFree": False,
            })
    return nodes or None


def course_schema():
    """The one recurring CI class we verified, as a Course with dates that keep it current."""
    return {
        "@type": "Course",
        "@id": schema.SITE + "/classes#contact-improv-all-levels",
        "name": "Contact Improv \u2014 ALL LEVELS",
        "description": (
            "A weekly all-levels Contact Improvisation class in Miami covering weight sharing, "
            "momentum and spontaneous partnering. No partner or prior experience required."
        ),
        "provider": {
            "@type": "Organization",
            "name": "Dance Arts Miami",
            "url": "https://danceartsmiami.com/",
        },
        "inLanguage": "en",
        "teaches": (
            "Contact Improvisation: weight sharing, rolling point of contact, momentum, "
            "falling safely and spontaneous partnering"
        ),
        "hasCourseInstance": {
            "@type": "CourseInstance",
            "courseMode": "onsite",
            "courseWorkload": "PT1H",
            "location": {
                "@type": "Place",
                "name": "Dance Arts Miami",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "250 NE 61st Street",
                    "addressLocality": "Miami",
                    "addressRegion": "FL",
                    "postalCode": "33137",
                    "addressCountry": "US",
                },
                "geo": {"@type": "GeoCoordinates", "latitude": 25.8307, "longitude": -80.1878},
            },
            "courseSchedule": {
                "@type": "Schedule",
                "byDay": "https://schema.org/Tuesday",
                "startTime": "18:00",
                "endTime": "19:00",
                "repeatFrequency": "P1W",
                "scheduleTimezone": "America/New_York",
            },
        },
        "url": "https://www.eventbrite.com/e/contact-improv-all-levels-tickets-1999219825315",
    }
