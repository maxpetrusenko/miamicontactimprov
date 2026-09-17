"""Confirmed local listings for the Miami pages.

Rules for this file, enforced by review rather than by code:
  * Every entry was opened and read. `verified` is the date the source was last seen live.
  * Nothing is inferred. `modality` states what the organiser actually advertises, so a
    contact-adjacent practice is never presented as Contact Improvisation.
  * An empty list is a valid, honest state. Deleting a dead entry is a normal change.
  * No prices are copied unless the organiser publishes them on the page we link to.

Every entry carries its own checked date. Every source URL, and the HTTP status it
was read at, is recorded in docs/miami-jams-sources.md.
"""

import html
import schema

# Org and adjacent-practice entries: the date their own pages were last opened and read.
VERIFIED = "2026-09-13"

# Sessions in Miami-Dade and Broward: re-opened and re-read on this date.
SESSIONS_VERIFIED = "2026-09-14"

# The Friday jam this site hosts: the date its schedule was set down by the organiser.
FRIDAY_JAM_VERIFIED = "2026-09-17"
FRIDAY_JAM_NAME = "Friday Contact Improv Jam \u2014 Hallandale Beach"
FRIDAY_JAM_FIRST_DATE = "2026-10-02"

# name, modality, city, venue, schedule, cost, url, verified, note
# name, modality, city, venue, schedule, cost, url, verified, note
SESSIONS = [
    (
        "Contact Improv \u2014 ALL LEVELS",
        "Contact Improvisation",
        "Miami",
        "Dance Arts Miami, 250 NE 61st Street, Miami, FL 33137",
        "Weekly, Tuesdays 6:00\u20137:00 PM EDT; the Meetup listing states the recurrence runs to 28 February 2027",
        "$22 for a first class on Eventbrite, $30 on Meetup and SweatPals",
        "https://www.eventbrite.com/e/contact-improv-all-levels-tickets-1999219825315",
        SESSIONS_VERIFIED,
        "The most established recurring Contact Improvisation class found in Miami-Dade. Published on Eventbrite "
        "by Esther Frances & Dmitry Krasnyanskiy and hosted at Dance Arts Miami. Advertised as exploring "
        "connection, weight sharing, momentum and spontaneous partnering, with no partner needed, and mirrored "
        "on Meetup and SweatPals. The three listings disagree with each other, so read the one you are actually "
        "booking through: a first class is $22 on Eventbrite and $30 on Meetup and SweatPals, and refunds run "
        "to 7 days before the event on Eventbrite while SweatPals states none. Dance Arts Miami's own schedule "
        "page carried no contact improvisation entry when it was opened, so this class is verified through its "
        "Eventbrite, Meetup and SweatPals listings rather than the studio's own site, and the current week is "
        "always worth confirming there.",
    ),
    (
        "Kama Flight \u2014 Flight Workshop",
        "Contact-adjacent (acro yoga, Thai massage, Contact Improvisation)",
        "Miami",
        "Skanda Yoga, 1800 SW 1st Ave #102, Miami, FL 33129",
        "October 18, 2026 and November 15, 2026, 3:00\u20134:30 PM on both dates",
        "$50, sold as a partner pair (admission for two)",
        "https://kamaflight.com/products/flight-workshop-miami-fl-october-18-2026",
        SESSIONS_VERIFIED,
        "Described by the organisers as a fusion of acro yoga, Thai massage and Contact Improvisation, and as a "
        "new partner wellness modality built on the neuroscience of play and connection. Proceeds fund the Kama "
        "Flight Foundation, a registered 501(c)(3) nonprofit. Booked in pairs with friends welcome, which makes "
        "it a gentler first step than an open jam if physical contact with strangers is the thing giving you "
        "pause. One thing we could not resolve: both the October and the November product pages render an 'Add "
        "to cart' control and also the words 'Sold Out', so treat availability as unclear and ask "
        "info@kamaflight.com before planning around either date.",
    ),
    (
        "Kama Flight \u2014 jams",
        "Contact-adjacent (acro yoga, Thai massage, Contact Improvisation)",
        "Miami Beach",
        "Private residence, 2345 N Bay Rd, Miami Beach, FL 33140",
        "Most recent published Miami jam: 8 September 2026, 6:30\u20139:00 PM. No later Miami date was published when we checked.",
        "Donation, with $10, $20 and $30 offered as suggested amounts, booked in advance",
        "https://kamaflight.com/collections/jams",
        SESSIONS_VERIFIED,
        "Recurring donation-based jams at a private residence, which has to be booked in advance and is why the "
        "exact address is confirmed to ticket holders. The organiser's own jams collection listed exactly one "
        "Miami jam when it was opened, dated 8 September 2026 and therefore already past, with no next Miami "
        "date published beside it. That is why this entry carries its date instead of being presented as a "
        "running session: check the organiser's page for the next one rather than trusting any list, including "
        "this one.",
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
        "improvisation, acro yoga, ecstatic dance, tai chi, massage and authentic relating as its programme. The "
        "camp's own page states that the camp loves 'Contact Improvisation Dance, Acro Yoga, Ecstatic Dance, Tai "
        "Chi, Massage, Hugs, and Authentic Relating'. This is the largest concentration of contact improvisation "
        "that happens in Miami in a year, and it is a festival rather than a class. The page prints the dates "
        "5-8 February without printing the year beside them, while its own countdown points at early February "
        "2027, so read the page directly rather than treating a month and a day from this site as a confirmed "
        "booking date.",
    ),
    (
        "Ecstatic Dance Miami \u2014 Full Moon Immersion",
        "Contact-adjacent (ecstatic dance, with a Contact Improv component the listing advertises). Not a CI jam.",
        "Hollywood, Broward County",
        "Exact venue not published by the organiser. The listing names Hollywood Lakes, Hollywood, FL, and sends the location to ticket holders on the day.",
        "Saturday 26 September 2026, 7:00\u201311:59 PM EDT. Monthly, on the full moon.",
        "Not published on the pages we read; advance tickets only",
        "https://www.eventbrite.com/e/ecstatic-dance-miami-september-26th-full-moon-immersion-tickets-1999291383347",
        SESSIONS_VERIFIED,
        "The organiser's own listing describes the evening as a monthly embodiment and healing experience "
        "through Contact Improv, ecstatic dance, tantra, aquatic healing work and sound healing, so contact "
        "improvisation is one part of a longer programme rather than the whole of it. The organiser states "
        "plainly that there are no tickets at the door and no drop-ins. Their site has been running since 2014 "
        "and gathers every full moon. The trade-off of carrying this entry is the one thing we cannot verify "
        "for you: the venue is deliberately withheld until a ticket is bought, so the county is Broward and the "
        "city is Hollywood, and nothing more specific is published for us to check.",
    ),
    (
        "Ecstatic Dance Fort Lauderdale",
        "Contact-adjacent (ecstatic dance). Not Contact Improvisation, and the listing makes no CI claim.",
        "Fort Lauderdale, Broward County",
        "Le Sound Temple, 2501 NE 30th St, Fort Lauderdale, FL 33306",
        "Monthly, first Saturday of the month, 7:30\u20139:30 PM with doors at 7:00 PM. The only dated gathering the listing names is its inaugural, 5 September 2026.",
        "$33",
        "https://ecstaticdance.org/dance/ecstatic-dance-ft-lauderdale/",
        SESSIONS_VERIFIED,
        "An evening of cacao, breathwork, ecstatic dance and a closing sound bath, carried on ecstaticdance.org, "
        "the global conscious-dance directory, in the organiser's own words. It is listed here because it is "
        "the clearest recurring movement gathering in Broward County that could be verified at all, and because "
        "no contact improvisation jam in Broward could be found to list instead. It is not contact "
        "improvisation, and this site will not imply otherwise. The venue's own events page publishes sound "
        "baths and breathwork but not this dance, so the directory listing above is the source to check.",
    ),
    (
        "Friday Contact Improv Jam \u2014 Hallandale Beach",
        "Contact Improvisation",
        "Hallandale Beach, Broward County",
        "Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009",
        "Weekly, Fridays 7:00\u20139:00 PM, from Friday 2 October 2026",
        "$20 at the door, on a sliding scale of $20\u2013$50; pay what you can within that range",
        "https://miamicontactimprov.com/friday-jam",
        FRIDAY_JAM_VERIFIED,
        "The one session this site runs itself. It is hosted by Max Petrusenko, who also maintains "
        "miamicontactimprov.com, so the disclosure comes first: this entry is the organiser describing his "
        "own jam, on the same terms as every other entry on this page and ranked no higher for it. An open, "
        "all-levels Contact Improvisation jam with a short opening circle, a warm-up and open dancing until "
        "nine; no partner and no experience needed, and no booking, you come to the door. Hallandale Beach is "
        "in Broward County, a few minutes north of the Miami-Dade line on US-1. Inner Motion Dance Studio's "
        "own public schedule did not yet show this session when it was opened on the checked date, so the "
        "source linked here is this site's own page for the jam, which is where the schedule is kept current.",
    ),
]


# Who runs each session, in the words that organiser publishes about itself. Kept beside
# SESSIONS rather than inside it so the session tuple keeps its shape; tools/gate.py
# asserts that every session names an organiser here and that nothing here is orphaned,
# so the two cannot drift apart.
SESSION_ORGANISERS = {
    FRIDAY_JAM_NAME: (
        "Max Petrusenko, who also maintains this site",
        "https://www.maxpetrusenko.com",
    ),
    "Contact Improv \u2014 ALL LEVELS": (
        "Esther Frances & Dmitry Krasnyanskiy, hosted at Dance Arts Miami",
        "https://www.eventbrite.com/e/contact-improv-all-levels-tickets-1999219825315",
    ),
    "Kama Flight \u2014 Flight Workshop": (
        "Kama Flight", "https://kamaflight.com/",
    ),
    "Kama Flight \u2014 jams": (
        "Kama Flight", "https://kamaflight.com/",
    ),
    "Camp Contact at Love Burn": (
        "Camp Contact", "https://loveburn.campcontact.org/",
    ),
    "Ecstatic Dance Miami \u2014 Full Moon Immersion": (
        "Ecstatic Dance Miami", "https://ecstaticdancemiami.com/",
    ),
    "Ecstatic Dance Fort Lauderdale": (
        "Ecstatic Dance Fort Lauderdale", "https://ecstaticdance.org/dance/ecstatic-dance-ft-lauderdale/",
    ),
}

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
    "Ecstatic Dance Miami \u2014 Full Moon Immersion": [
        ("2026-09-26", "Hollywood Lakes, Hollywood, FL"),
    ],
}

# The organiser and locality behind each dated occurrence. Separate from EVENT_DATES so
# that mapping keeps its shape. events_schema() skips any occurrence with no entry here,
# so a date can never be published under a guessed organiser, and tools/gate.py asserts
# the two mappings cover each other and that every key names a session that exists.
EVENT_ORGS = {
    "Kama Flight \u2014 Flight Workshop": {
        "slug": "kama-flight",
        "organiser": "Kama Flight",
        "organiser_url": "https://kamaflight.com/",
        "locality": "Miami",
        "ticketed": True,
    },
    "Ecstatic Dance Miami \u2014 Full Moon Immersion": {
        "slug": "ecstatic-dance-miami",
        "organiser": "Ecstatic Dance Miami",
        "organiser_url": "https://ecstaticdancemiami.com/",
        "locality": "Hollywood",
        "ticketed": None,
    },
}


def friday_jam_event():
    """The recurring Event for the jam this site hosts.

    This is the one Event on the property whose organiser is the site itself, so it is
    built here rather than through EVENT_DATES: a weekly session is one Event with an
    eventSchedule, not a fresh dated node per Friday, and the offer is the sliding
    scale the organiser actually charges.
    """
    return {
        "@type": "Event",
        "@id": f"{schema.SITE}/friday-jam#event",
        "name": FRIDAY_JAM_NAME,
        "description": (
            "A weekly open, all-levels Contact Improvisation jam in Hallandale Beach, Broward County, "
            "hosted by Max Petrusenko at Inner Motion Dance Studio. Fridays 7:00 to 9:00 PM from "
            "2 October 2026. $20 at the door on a sliding scale of $20 to $50. No partner, no "
            "experience and no booking needed."
        ),
        "startDate": FRIDAY_JAM_FIRST_DATE + "T19:00:00-04:00",
        "endDate": FRIDAY_JAM_FIRST_DATE + "T21:00:00-04:00",
        "eventSchedule": {
            "@type": "Schedule",
            "byDay": "https://schema.org/Friday",
            "startTime": "19:00",
            "endTime": "21:00",
            "startDate": FRIDAY_JAM_FIRST_DATE,
            "repeatFrequency": "P1W",
            "scheduleTimezone": "America/New_York",
        },
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {
            "@type": "Place",
            "name": "Inner Motion Dance Studio",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "216 NE 1st Ave",
                "addressLocality": "Hallandale Beach",
                "addressRegion": "FL",
                "postalCode": "33009",
                "addressCountry": "US",
            },
        },
        "organizer": {
            "@type": "Person",
            "name": "Max Petrusenko",
            "url": "https://www.maxpetrusenko.com",
            "affiliation": {"@id": schema.ORG_ID},
        },
        "offers": {
            "@type": "Offer",
            "price": "20",
            "priceCurrency": "USD",
            "description": "Sliding scale $20 to $50, paid at the door",
            "availability": "https://schema.org/InStock",
            "url": schema.SITE + "/friday-jam",
        },
        "isAccessibleForFree": False,
        "url": schema.SITE + "/friday-jam",
        "image": schema.SITE + "/assets/og.png",
    }


def events_schema():
    """Only occurrences with a date read off the organiser's own page are emitted.

    An occurrence with no EVENT_ORGS entry is skipped rather than attributed to a
    default organiser, and `ticketed` is written only where the price is published.
    """
    nodes = []
    for name, modality, city, venue, schedule, cost, url, verified, note in SESSIONS:
        dates = EVENT_DATES.get(name)
        meta = EVENT_ORGS.get(name)
        if not dates or not meta:
            continue
        for iso, location in dates:
            node = {
                "@type": "Event",
                "@id": f"{schema.SITE}/jams#{iso}-{meta['slug']}",
                "name": name,
                "description": note,
                "startDate": iso,
                "eventStatus": "https://schema.org/EventScheduled",
                "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "location": {
                    "@type": "Place",
                    "name": location,
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": meta["locality"],
                        "addressRegion": "FL",
                        "addressCountry": "US",
                    },
                },
                "organizer": {
                    "@type": "Organization",
                    "name": meta["organiser"],
                    "url": meta["organiser_url"],
                },
                "url": url,
                "image": schema.SITE + "/assets/og.png",
            }
            if meta["ticketed"] is not None:
                node["isAccessibleForFree"] = not meta["ticketed"]
            nodes.append(node)
    nodes.append(friday_jam_event())
    return nodes


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
