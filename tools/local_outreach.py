#!/usr/bin/env python3
"""Prepare the local-listing outreach for miamicontactimprov.com. SENDS NOTHING.

This file is deliberately not a sender. It writes each draft to disk as exact RFC 822
bytes (headers included) so the message that would go out is auditable, and then stops.
There is no transport here, no `gws` call, no SMTP, no mailto. `send()` below raises if
it is ever called, so wiring this into something that sends has to be a conscious edit
rather than a flag someone flips.

Why each surface is a legitimate listing and not a link scheme. Every recipient is
either the venue that already hosts the session, or a public agency directory that
accepts submissions from arts organisations for free and reviews them by hand before
publishing. None of them is a reciprocal-link swap, a paid placement, a guest post, or a
directory that exists to sell followed links. Nothing here asks for a link back and
nothing offers anything in return, which is the line that matters.

Run:
    python3 tools/local_outreach.py            # writes everything, sends nothing
    python3 tools/local_outreach.py --out DIR  # somewhere else

Sources for the recipient addresses, and the status each page was read at on
2026-09-14, are in docs/miami-jams-sources.md.
"""

import argparse
import base64
import json
import pathlib

FROM = "max.petrusenko@gmail.com"
REPLY_TO = "hello@miamicontactimprov.com"
DEFAULT_OUT = "/tmp/mci-local-outreach"

# No code path in this module sends. Kept as a named constant so a reviewer can see
# the intent without reading the whole file.
SENDING_ENABLED = False
PREPARED_ON = "2026-09-14"


# (recipient, subject, body, why-this-is-a-listing-not-a-link-scheme, recipient_verified)
DRAFTS = [
    {
        "key": "01-dance-arts-miami",
        "recipient": "info@danceartsmiami.com",
        "recipient_verified": (
            "Verified. Published on https://danceartsmiami.com/contact, read 2026-09-14 "
            "(HTTP 200)."
        ),
        "subject": "Your Tuesday contact improv class is the only one on the open web in Miami",
        "why_legitimate": (
            "Dance Arts Miami is the venue that already hosts the session. Their own schedule "
            "page is the authoritative place a newcomer would look, and it currently carries no "
            "contact improvisation entry, so the class is only findable through Eventbrite, "
            "Meetup and SweatPals. Asking a business to list a session it hosts on its own "
            "calendar is listing the thing they are the publisher of, not asking for a link."
        ),
        "body": """Hello,

My name is Max. I run a non-commercial resource site for Contact Improvisation in Miami
and I wanted to flag something about your Tuesday evening class, because I think it is
costing you bookings rather than traffic.

    https://miamicontactimprov.com/miami-jams

The class is "Contact Improv - ALL LEVELS", Tuesdays 6 to 7 PM at 250 NE 61st Street, and
as far as I can find it is the only recurring Contact Improvisation class published
anywhere in Miami-Dade County. I listed it with the organiser named as Esther Frances and
Dmitry Krasnyanskiy, and I linked to your Eventbrite, Meetup and SweatPals listings.

Two things I noticed while checking, which you are welcome to ignore:

1. Your own schedule page at danceartsmiami.com/schedule did not show a contact
   improvisation entry when I opened it on 14 September 2026. The class is only findable
   through the three listing platforms, which is how I found it. Someone searching your
   studio for it on your own site would come up empty.

2. The three listings price it differently from each other: Eventbrite says a first class
   is $22, Meetup and SweatPals say $30, and Eventbrite allows refunds up to 7 days
   before while SweatPals says no refunds. I have stated all three on my page rather than
   picking one, because I cannot know which is right. If you would rather it read one way,
   tell me and I will correct it.

If you do add it to your own calendar, send me the URL and I will point my page at your
schedule rather than at the third-party listings, since yours is the source of truth.

I am not asking for a link back and there is nothing on my site for sale. If you would
rather not be listed at all, say so and the entry comes down the same day.

Max
miamicontactimprov.com
""",
    },
    {
        "key": "02-miami-dade-cultural-affairs",
        "recipient": "culture@miamidade.gov",
        "recipient_verified": (
            "Verified. The contact address published on "
            "https://www.miamidadearts.org/organizations/cultural-resource-directory, read "
            "2026-09-14 (HTTP 200), where the page also names Dana Pezoldt, 305-375-4634."
        ),
        "subject": "Cultural Resource Directory: question about a non-commercial community resource",
        "why_legitimate": (
            "The County's own Cultural Resource Directory is a free, editor-reviewed listing "
            "that the Department of Cultural Affairs operates for arts organisations in the "
            "county, and the page says all entries are subject to editing and approval. This "
            "is an eligibility question put to the operator of a public directory, which is "
            "the honest way to approach one. No payment is offered and no link is exchanged."
        ),
        "body": """Hello,

I have read the Cultural Resource Directory page, which says participation is free and
that all entries are subject to editing and approval. I am writing before registering,
because I am not certain my case belongs in the directory and I would rather ask than add
something you would have to remove.

    https://miamicontactimprov.com

What it is: a non-commercial community resource that maps Contact Improvisation practice
across Miami-Dade and Broward County. It is not a studio, not an organiser and not a
membership body. It runs no sessions, takes no bookings and charges no listing fee, and
there is no advertising or sponsorship on it.

What it publishes about the county: a dated list of every Contact Improvisation jam,
class and workshop that could be verified locally, each entry naming its organiser, venue,
schedule, price and the date the source was checked, plus what could not be verified and
why. For Miami-Dade that currently means a weekly all-levels class at Dance Arts Miami on
Tuesday evenings, two dated workshops at Skanda Yoga, and Camp Contact at the Love Burn
festival on Virginia Key each February.

My question: does a resource of that kind qualify for the Cultural Resource Directory, or
is the directory intended for organisations that produce or present cultural programmes?
If it is the latter, that is a clean answer and I will not pursue it. If there is a better
fit inside the Department's listings, I would rather be pointed at it than guess.

Either way, the directory looks genuinely useful for residents trying to find dance
studios and classes by neighbourhood, and I am glad it exists.

Thank you,
Max
miamicontactimprov.com
""",
    },
    {
        "key": "03-broward-arts-calendar",
        "recipient": "arts calendar submission route, Broward Cultural Division",
        "recipient_verified": (
            "UNVERIFIED, and this is why: ArtsCalendar.com returned HTTP 403 to every request "
            "from this host on 2026-09-14, including / and /contact, so its submission terms "
            "and its contact address could not be read here. The address browardarts@broward.org "
            "appeared in a secondary report and is NOT verified. Broward.org/Arts (HTTP 200) "
            "links to ArtsCalendar.com but publishes no email. Before this draft is sent, open "
            "https://artscalendar.com/register and read the submission page, then address the "
            "message to whatever it publishes."
        ),
        "subject": "Submitting a Broward County listings resource to ArtsCalendar",
        "why_legitimate": (
            "ArtsCalendar.com is the Broward Cultural Division's own calendar, linked from the "
            "county's Cultural Division page, and it reviews submissions by hand before posting "
            "them. Asking a county-run arts calendar to consider an entry is a submission to a "
            "public listing service, which is categorically different from asking a blog for a "
            "link."
        ),
        "body": """Hello,

I would like to ask how to submit a resource to ArtsCalendar, and whether it is the right
place for what I have.

    https://miamicontactimprov.com/miami-jams

I run a non-commercial resource that maps Contact Improvisation practice across Miami-Dade
and Broward County. It is not a studio, an organiser or a membership body, it runs no
sessions, it takes no bookings and it charges no listing fee.

The relevant page is a dated list of every Contact Improvisation jam, class and workshop
that could be verified in the two counties, with each entry naming its organiser, venue,
schedule, price and the date its source was checked, and with a section saying plainly
what could not be verified and why. For Broward that currently means two recurring
conscious-dance gatherings, one of them at Le Sound Temple in Fort Lauderdale, because no
recurring Contact Improvisation session in Broward County could be verified from a source
that publishes about itself at all.

Two questions:

1. Does an entry of this kind belong on ArtsCalendar, or is the calendar for individual
   events and performances only? If it is events only, no problem at all, tell me and I
   will not pursue it.

2. If it does belong, what is the correct submission route? I could not read the
   submission page from here, so I would rather be told the right one than guess.

Either answer is useful, and I would rather ask than submit something you would have to
reject.

Thank you,
Max
miamicontactimprov.com
""",
    },
    {
        "key": "04-le-sound-temple",
        "recipient": "info@LeSoundTemple.com",
        "recipient_verified": (
            "Verified. Published on https://www.lesoundtemple.com/, read 2026-09-14 "
            "(HTTP 200)."
        ),
        "subject": "Your monthly ecstatic dance is the clearest recurring Broward listing I could verify",
        "why_legitimate": (
            "Le Sound Temple is the venue hosting the monthly gathering. Its own events page "
            "already lists its recurring sound baths and breathwork sessions, so the ask is to "
            "add a series it hosts to the calendar it already publishes, not to insert a third "
            "party's link."
        ),
        "body": """Hello,

My name is Max. I run a non-commercial resource site for Contact Improvisation in Miami
and Broward County, and I wanted to write to you about the monthly gathering at your
venue.

    https://miamicontactimprov.com/miami-jams

The Ecstatic Dance Fort Lauderdale gathering at 2501 NE 30th St is the clearest recurring
movement event in Broward County that I was able to verify at all, and I have listed it
with its actual modality stated as ecstatic dance, not as contact improvisation. I am
listing it because someone looking for contact improvisation in Broward has nowhere else
to start, and I would rather point them at something real and correctly labelled than
leave the county blank. If that framing is wrong for you, tell me and the entry comes
down.

One thing worth knowing: your own events page at lesoundtemple.com/events lists your
Alchemy Sound Bath, your Midday Reset and your full moon ceremonies, but not the monthly
dance. The only place the dance is published is the ecstaticdance.org directory. If you
added it to your own calendar, I would point my page at yours, because yours is the
source of truth for your own room.

For reference, the details I published are: monthly, first Saturday, 7:30 to 9:30 PM with
doors at 7:00 PM, $33. If any of that is out of date, send the correction and I will
update it the same day.

I am not asking for a link back and there is nothing on my site for sale.

Max
miamicontactimprov.com
""",
    },
    {
        "key": "05-contactimprov-followup",
        "recipient": "moti@contactimprov.com",
        "recipient_verified": (
            "Verified. Published on https://www.contactimprov.com/ as the contact for the "
            "World Jam Map, and already used by this project for a first message on 2026-09-13."
        ),
        "subject": "Following up on the Florida page: two links and one undated Miami entry",
        "why_legitimate": (
            "The World Jam Map is the global listing for CI jams and its own page asks, in "
            "writing, to be sent corrections and outdated information. This is the correction "
            "channel the recipient publishes for exactly this purpose, and it follows an "
            "earlier message rather than opening an unsolicited thread."
        ),
        "body": """Hello Moti,

Following up on the message I sent on 13 September, and re-checking the Florida page on
14 September 2026 so the detail below is current.

Everything here is meant as a correction you can use, not a complaint. Your page says
"Please also help us correct any outdated information", so this is that.

1. Under "Contact Improvisation in Miami", both links are now unreachable:

   - http://tribes.tribe.net/ciseflo returns HTTP 404. Tribe.net is gone.
   - http://groups.yahoo.com/group/ciseflo/ returns HTTP 200, but it redirects to
     yahoo.com's homepage. Yahoo Groups was shut down in 2020 and the group archives
     went with it.

   Neither link gets anyone to a Miami community, and a reader has no way to tell whether
   that is a temporary outage or the state of the scene. The same pair is duplicated on
   your linksyahoogroups page.

2. The "Monday Night Community Jam / Workshop" at Excello, 8700B SW 129th Terrace, first
   Monday of the month, 7 to 9 PM, $10, is credited to Karen Peterson Dancers. It carries
   no year and no start date. I checked Karen Peterson Dancers' own site, which does name
   Excello Dance Space but publishes no jam, no Monday session and not that address, so I
   cannot confirm the jam is running and I have deliberately not listed it as current on
   mine. If you know whether it is live, I will list it properly with a source and a date.
   If it has stopped, deleting it makes the Florida page more useful, not less.

3. Two things that may be worth adding for balance: Broward County currently has no entry
   on the Florida page at all, and there is nothing I could find to add there, which is
   itself worth knowing. And the Florida page's other entries, Sarasota and Jacksonville
   Beach, both read as current and are more useful than a longer list that is not.

What I verified on my side, for whatever it is worth to the map: a weekly all-levels class
at Dance Arts Miami, Tuesdays 6 to 7 PM at 250 NE 61st Street, published on Eventbrite by
Esther Frances and Dmitry Krasnyanskiy with the recurrence running to 28 February 2027 on
Meetup; Kama Flight running a first workshop at Skanda Yoga on 18 October and a second on
15 November 2026, which is a fusion of acro yoga, Thai massage and contact improvisation
rather than CI on its own; and Camp Contact at Love Burn on Virginia Key each February.

My page is at https://miamicontactimprov.com/miami-jams, and every entry on it names the
source it was read on and the date it was checked.

I am happy to keep being a correction contact for the Florida page. If anything on it goes
stale, send it over and I will check it against what is actually running.

Max
miamicontactimprov.com
""",
    },
]


def build_raw(to, subject, body):
    """The exact bytes that would be sent, RFC 822, base64url for transport."""
    msg = (
        f"From: Miami Contact Improv <{FROM}>\r\n"
        f"To: {to}\r\n"
        f"Subject: {subject}\r\n"
        f"Reply-To: {REPLY_TO}\r\n"
        "MIME-Version: 1.0\r\n"
        "Content-Type: text/plain; charset=UTF-8\r\n"
        "Content-Transfer-Encoding: 8bit\r\n"
        "X-Draft-Status: UNSENT\r\n"
        "\r\n"
        + body.replace("\n", "\r\n")
    )
    return base64.urlsafe_b64encode(msg.encode("utf-8")).decode("ascii")


def eml_bytes(d):
    return (
        f"From: Miami Contact Improv <{FROM}>\r\n"
        f"To: {d['recipient']}\r\n"
        f"Subject: {d['subject']}\r\n"
        f"Reply-To: {REPLY_TO}\r\n"
        "MIME-Version: 1.0\r\n"
        "Content-Type: text/plain; charset=UTF-8\r\n"
        "Content-Transfer-Encoding: 8bit\r\n"
        "X-Draft-Status: UNSENT\r\n"
        f"X-Draft-Prepared: {PREPARED_ON}\r\n"
        "\r\n"
        + d["body"].replace("\n", "\r\n")
    )


def send(*_a, **_kw):
    raise RuntimeError(
        "This module prepares drafts and sends nothing. Sending the local-outreach "
        "messages is a separate, deliberate action outside this file."
    )


def main():
    ap = argparse.ArgumentParser(description="Prepare (never send) the local-listing outreach.")
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    manifest = []
    for d in DRAFTS:
        path = out / f"{d['key']}.eml"
        path.write_bytes(eml_bytes(d).encode("utf-8"))
        b64 = build_raw(d["recipient"], d["subject"], d["body"])
        (out / f"{d['key']}.b64").write_text(b64, encoding="ascii")
        (out / f"{d['key']}.reason.txt").write_text(
            "RECIPIENT\n" + d["recipient"] + "\n\n"
            "RECIPIENT PROVENANCE\n" + d["recipient_verified"] + "\n\n"
            "WHY THIS IS A LEGITIMATE LISTING SURFACE AND NOT A LINK SCHEME\n"
            + d["why_legitimate"] + "\n",
            encoding="utf-8",
        )
        manifest.append({
            "key": d["key"],
            "recipient": d["recipient"],
            "subject": d["subject"],
            "eml": str(path),
            "b64": str(out / f"{d['key']}.b64"),
            "reason": str(out / f"{d['key']}.reason.txt"),
            "recipient_verified": not d["recipient_verified"].startswith("UNVERIFIED"),
            "sent": False,
        })
        print(f"prepared  {d['key']:32} -> {d['recipient']}")
        print(f"          {path}")

    (out / "MANIFEST.json").write_text(
        json.dumps(
            {
                "prepared_on": PREPARED_ON,
                "sending_enabled": SENDING_ENABLED,
                "sent": 0,
                "drafts": manifest,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\n{len(manifest)} drafts written to {out}/ — nothing sent (sending_enabled={SENDING_ENABLED})")
    print(f"manifest: {out / 'MANIFEST.json'}")
    unverified = [m["key"] for m in manifest if not m["recipient_verified"]]
    if unverified:
        print(f"recipient needs confirming before sending: {', '.join(unverified)}")


if __name__ == "__main__":
    main()
