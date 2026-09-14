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
    python3 tools/local_outreach.py                 # the original five, writes everything, sends nothing
    python3 tools/local_outreach.py --set followups # the follow-ups to the 2026-09-13 sends
    python3 tools/local_outreach.py --set all
    python3 tools/local_outreach.py --out DIR       # somewhere else

`DRAFTS` holds the first set. `FOLLOWUP_DRAFTS` holds the messages that follow the sends of
2026-09-13 to moti@contactimprov.com, bodydiary@ciglobalcalendar.net and info@contactquarterly.com;
they are follow-ups rather than repitches, and why is documented per draft and in
docs/listing-submissions-mic.md.

Sources for the recipient addresses, and the status each page was read at on 2026-09-14, are in
docs/miami-jams-sources.md and docs/listing-submissions-mic.md.
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
        "recipient": "browardarts@broward.org",
        "recipient_verified": (
            "Verified 2026-09-14: https://artscalendar.com/contact returns HTTP 200 and "
            "publishes, verbatim, \"Email: browardarts@broward.org\" and \"Phone: (954) 357-7457\", "
            "under \"Broward Cultural Division, Main Library, 100 S Andrews Ave 6th Floor, Fort "
            "Lauderdale, FL 33301\". The site root also returns 200. An earlier note in this file "
            "recorded HTTP 403 from this host and marked the address unverified; that was wrong "
            "for 2026-09-14 and is corrected here."
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

2. If it does belong, is there a submission route you would rather I used than this
   address? I am writing to the contact address published on your contact page, and I
   would rather be pointed at the right route than send this to the wrong desk.

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


# --- follow-ups, prepared 2026-09-14 ---------------------------------------------------------
#
# The 2026-09-13 sends already went to moti@contactimprov.com, bodydiary@ciglobalcalendar.net and
# info@contactquarterly.com. These are NOT repitches of those messages. Each one either answers a
# question the earlier message left open, corrects a fact that changed, or opens a surface that was
# not in the first pass. The reasoning and the live status of every page are in
# docs/listing-submissions-mic.md.
FOLLOWUP_DRAFTS = [
    {
        "key": "06-contactimprov-free-member-route",
        "recipient": "moti@contactimprov.com",
        "recipient_verified": (
            "Verified. Published on https://www.contactimprov.com/ as the contact for the World "
            "Jam Map, and already a live thread since the 2026-09-13 message."
        ),
        "subject": "The free member route: does a city resource qualify for it?",
        "why_legitimate": (
            "The site's own membership page states that free Basic Membership includes a member "
            "listing, and the World Jam Map pages ask in writing to be sent corrections. This is a "
            "question about the site's own product, put to the site, on a thread the site opened. "
            "It requests no link and offers nothing in return; it explicitly declines the paid "
            "listing so no one has to wonder whether the silence is a sales tactic."
        ),
        "body": """Hello Moti,

One more question on the same thread, and then I will leave it alone.

I re-read your membership page on 14 September 2026 and it says:

    FREE Basic Membership Includes: Member listing on the site.

I had assumed the only route onto the site was a listing I had to arrange, so I did not ask this
first time. Is a free Basic Membership appropriate for a non-commercial city resource like mine, or
is a member listing meant for individuals and studios?

    https://miamicontactimprov.com/miami-jams

To be clear about one thing so nobody has to guess at my motive: I am not going to buy the $5
per-event listing on the world workshop/event calendar. If the answer is that a non-commercial
resource does not belong on the site at all, that is a clean answer and I will stop asking.

If it does belong, whatever the correct route is, I will use that instead of guessing.

One correction to carry over from my earlier message, re-checked today: the two links under
"Contact Improvisation in Miami" are still unreachable. tribes.tribe.net/ciseflo returns 404, and
groups.yahoo.com/group/ciseflo/ returns 200 but lands on yahoo.com's homepage.

Thank you,
Max
miamicontactimprov.com
""",
    },
    {
        "key": "07-ciglobalcalendar-regional-snippet",
        "recipient": "bodydiary@ciglobalcalendar.net",
        "recipient_verified": (
            "Verified. Used by this project for the 2026-09-13 message; the site's own contact "
            "forms at /contactForm/compose/project-manager and /contactForm/compose/administrator "
            "are the published routes."
        ),
        "subject": "The regional snippet for Florida, and who is already registered in Miami",
        "why_legitimate": (
            "The calendar's own Get Involved page publishes the regional/country snippet route for "
            "exactly this purpose: a regional site embeds the calendar's events for its area and "
            "the calendar keeps the authority and the data. That is an integration the publisher "
            "offers, not a link exchange, and the second question is a request for the facts the "
            "site already holds so the Miami page does not duplicate them."
        ),
        "body": """Hello,

Following my message of 13 September, and re-reading your site today so this is current.

I am not asking again whether a city hub can be posted as an event. Your Help page answers that, and
I accept the answer: entries have to be Contact Improvisation events, and anything else gets removed.

What I am asking about is the route your Get Involved page offers:

    Direct access to Country/Regional contents
    If you are the developer of a regional/country website you can include a snippet that show
    just the events related to your area.

Two questions:

1. Could I have the snippet for Florida, or the pointer to how it is implemented? I would like
   miamicontactimprov.com to show the actual Contact Improvisation events already in your calendar
   for Florida, with the calendar credited as the source and linked as the place to register. The
   calendar keeps the authority; my page would just mirror the events for the state, because right
   now a reader in Miami has no single place to see what is running.

2. Which organisers in Miami are already registered with the calendar? I would rather point my jam
   list at them than duplicate or contradict them. If no Miami organiser is registered yet, that is
   useful to know too, because it tells me the state is effectively unrepresented.

Either answer helps, and I am happy to be pointed at documentation rather than have anyone spend
time explaining it to me.

Thank you,
Max
miamicontactimprov.com
""",
    },
    {
        "key": "08-contactquarterly-add-route",
        "recipient": "info@contactquarterly.com",
        "recipient_verified": (
            "Verified. Published on "
            "https://contactquarterly.com/contact-improvisation/newsletter/ as a mailto: link and "
            "used by this project for the 2026-09-13 message."
        ),
        "subject": "Your page answers my question, so only the add route is outstanding",
        "why_legitimate": (
            "The Contacts List describes itself as a referral directory that lists individuals and "
            "organizations willing to refer people to Contact activity locally, and a Miami entry "
            "is exactly that. The only outstanding item is a procedural one the page does not "
            "publish. Nothing is offered in exchange and no reciprocal link is proposed."
        ),
        "body": """Hello,

I wrote on 13 September asking whether the CI Contacts List is for individuals only. Your own page
answers it, so I am withdrawing that question rather than leaving it hanging:

    The Contacts List is a referral directory for locating Contact Improvisation classes, jams,
    and practitioners around the world. It lists individuals and organizations who are willing to
    refer people to Contact activities in their area.

So organisations qualify. The only thing still outstanding is procedural. The page offers "Log in to
edit your listing", which presumes the reader is already on the list, and I could not find a route
for proposing a new entry. What is the correct way to propose one?

For reference, and because it may be useful to whoever maintains the list rather than because it is
a complaint: Florida does not appear under United States. The state headings I can see are
California, Colorado, Connecticut, Georgia, Illinois, Maryland, Massachusetts, Michigan, Minnesota,
New Mexico, New York, North Carolina, Ohio, Pennsylvania, Rhode Island, Texas, Vermont, Washington
and Wisconsin. Miami has been effectively absent.

The resource I would propose for a Miami entry is non-commercial: https://miamicontactimprov.com
It runs no sessions, takes no bookings, charges nothing and carries no advertising, and it lists
what could be verified about practice in the county with the source and the date each entry was
checked.

If the answer is that the list is maintained only by existing members, that is a clean answer.

Thank you,
Max
miamicontactimprov.com
""",
    },
    {
        "key": "09-danceseekers-eligibility",
        "recipient": "https://danceseekers.com/get-listed (form; no address is published on the page)",
        "recipient_verified": (
            "Route verified 2026-09-14: https://danceseekers.com/get-listed returns HTTP 200 and "
            "carries the submission form. No contact address is published on that page, so this "
            "draft has no address and must NOT be sent to one that was guessed. Submit through the "
            "form, or read /contact first."
        ),
        "subject": "Eligibility question before I submit: does a city-level resource fit your four categories?",
        "why_legitimate": (
            "This is an eligibility question put to the site that operates the map, whose own page "
            "says it verifies every submission and publishes a page that links back to the "
            "organizer. Because a city-level resource is none of the four categories it accepts, "
            "submitting one anyway would be manufacturing a fit, so the question is the honest "
            "move. Nothing is offered in exchange."
        ),
        "body": """Hello,

I would like to ask about eligibility before I submit anything, because your Get Listed page names
four categories and what I have is not obviously one of them.

Your page says: "Know an event, studio, recurring social, or class series that belongs on the map?
Tell us about it - something you run, or something you love. We verify every submission, then
publish a dedicated page that links back to the organizer's website and socials. Free."

What I run is none of those four things. It is a non-commercial resource site that maps what could
be verified about Contact Improvisation practice across Miami-Dade and Broward County: a weekly
all-levels class at Dance Arts Miami on Tuesdays, two dated workshops at Skanda Yoga, and Camp
Contact at the Love Burn festival on Virginia Key each February, each entry naming its organiser,
venue, schedule and the date the source was checked.

    https://miamicontactimprov.com/miami-jams

My question: does a city-level listings resource qualify for a page, or is the site only for the four
categories you list? If it is only those four, that is a clean answer and I will not pursue it.

I noticed your Miami page shows 23 organizers and 148 events, so whoever curates it already knows the
local scene well. If it is more useful, I am happy to send the verified Miami and Broward entries as
corrections for that page instead of asking for a page of my own. Either is fine, and the second one
is probably more useful to your readers.

Thank you,
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


def prepare(drafts, out):
    manifest = []
    for d in drafts:
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
            "recipient_verified": not d["recipient_verified"].startswith(("UNVERIFIED", "Route verified")),
            "sent": False,
        })
        print(f"prepared  {d['key']:32} -> {d['recipient']}")
        print(f"          {path}")
    return manifest


def main():
    ap = argparse.ArgumentParser(description="Prepare (never send) the local-listing outreach.")
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument(
        "--set",
        choices=("drafts", "followups", "all"),
        default="drafts",
        help=(
            "drafts = the original five prepared 2026-09-14; followups = the five prepared "
            "2026-09-14 that follow the 2026-09-13 sends, written to 2026-09-14-followups; "
            "all = both"
        ),
    )
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    manifest = []
    if args.set in ("drafts", "all"):
        manifest += prepare(DRAFTS, out)
    if args.set in ("followups", "all"):
        (out / "2026-09-14-followups").mkdir(parents=True, exist_ok=True)
        manifest += prepare(FOLLOWUP_DRAFTS, out / "2026-09-14-followups")

    (out / "MANIFEST.json").write_text(
        json.dumps(
            {
                "prepared_on": PREPARED_ON,
                "set": args.set,
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
