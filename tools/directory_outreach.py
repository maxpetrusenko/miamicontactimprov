#!/usr/bin/env python3
"""Send the directory-submission emails for miamicontactimprov.com via gws (main Gmail).

Writes each message to disk first so the exact bytes sent are auditable, then sends
through the Gmail API and prints the returned message id and thread id as proof.
"""

import base64
import json
import pathlib
import subprocess
import sys

FROM = "max.petrusenko@gmail.com"
OUT = pathlib.Path("/tmp/mci-outreach")
OUT.mkdir(exist_ok=True)

MESSAGES = {
    "contactimprov": {
        "to": "moti@contactimprov.com",
        "subject": "Miami CI resource site, plus two dead links on your Florida page",
        "body": """Hello Moti,

My name is Max. I have put together a resource site for Contact Improvisation in
Miami and I would like to ask you to consider it for the links page, since your
Miami entry is currently the only thing on the open web pointing at this city.

    https://miamicontactimprov.com

It is non-commercial, there is no membership and nothing on it is paid for. It
covers what the form is, how a jam runs, safety and consent, the history from
Magnesium at Oberlin through to the 1975 decision not to trademark, a glossary,
a video room of embed-verified films, and an honest directory of what could be
verified in Miami.

Two things on your Florida page that you may want to know about, since I found
them while building this:

1. The "Contact Improv Southeast Florida" entry points at
   tribes.tribe.net/ciseflo and groups.yahoo.com/group/ciseflo. Both Tribe.net
   and Yahoo Groups are gone, so those two links are dead for anyone who clicks
   them. The same entry is duplicated on your linksyahoogroups page.

2. The "Monday Night Community Jam / Workshop" at Excello, 8700B SW 129th
   Terrace, has no date on it. I could not confirm it is still running, so I have
   intentionally not listed it as current on my site. If you know whether it is
   live, I will list it properly with a source.

What I did verify, in case it is useful for the map: a weekly all-levels class at
Dance Arts Miami, Tuesdays 6 to 7pm at 250 NE 61st Street, confirmed through
Eventbrite and SweatPals; Kama Flight running contact-adjacent workshops and jams
out of Miami Beach; and Camp Contact bringing contact improvisation to Love Burn
on Virginia Key each February.

I am happy to be a standing correction contact for the Florida page. If anything
on it goes stale, send it over and I will check it against what is actually
running.

Max
miamicontactimprov.com""",
    },
    "ciglobalcalendar": {
        "to": "bodydiary@ciglobalcalendar.net",
        "subject": "Question about listing a city-level CI resource on the CI Global Calendar",
        "body": """Hello,

I have read the Help page, so I understand the calendar is built by organizers and
teachers entering their own events, and that content which is not about Contact
Improvisation is removed. I am writing before doing anything, because I am not
sure my case fits your model and I would rather ask than add something you would
have to delete.

I have built a resource site for Contact Improvisation in Miami:

    https://miamicontactimprov.com

It is a city-level hub, not an organizer. It is non-commercial, it has no
membership, and it does not take bookings. It carries what could be verified about
practice in Miami, in English, with sources and a checked date on every listing:

  - a weekly all-levels class at Dance Arts Miami, Tuesdays 6 to 7pm
  - Kama Flight workshops and jams in Miami and Miami Beach
  - Camp Contact at Love Burn, Virginia Key, February

My question: is there a place in the CI Global Calendar for a city-level resource
that points people to the organizers who are already in your directory, or is the
calendar strictly for the organizers and teachers themselves? If Miami organizers
should enter their own events, I will leave it to them and stop there, and I will
point my own pages at your calendar instead so people find the authoritative
listing.

Either answer is useful. Thank you for keeping this running.

Max
miamicontactimprov.com""",
    },
    "contactquarterly": {
        "to": "info@contactquarterly.com",
        "subject": "Adding a Miami entry to the CI Contacts List",
        "body": """Hello,

The CI Contacts List page says to log in to edit an existing listing, but I could
not find the route for proposing a new one, so I am asking by email.

I have built a non-commercial resource site for Contact Improvisation in Miami:

    https://miamicontactimprov.com

It maps what could be verified about practice in Miami: a weekly all-levels class
at Dance Arts Miami on Tuesdays, Kama Flight running contact-adjacent workshops
and jams out of Miami Beach, and Camp Contact at the Love Burn festival on
Virginia Key. It also carries what the form is, how a jam runs, consent and
safety, the history from 1972 through the 1975 decision not to trademark the
form, a glossary and a video room.

Two questions:

1. Can a city-level resource be added to the CI Contacts List under Florida, or
   is that list only for individual practitioners and teachers? If it is only for
   individuals, no problem at all, just tell me and I will not pursue it.

2. Whoever maintains the contacts list may want to know that Florida's entry is
   thin. Only Sarasota and Jacksonville surface as clearly current, and Miami has
   been effectively missing. If a Miami practitioner wants to be listed, I can
   point them at the form.

I am also happy to be a Miami correction contact if that is useful to whoever
maintains the list.

Thank you,
Max
miamicontactimprov.com""",
    },
}


def build_raw(to, subject, body):
    msg = (
        f"From: Miami Contact Improv <{FROM}>\r\n"
        f"To: {to}\r\n"
        f"Subject: {subject}\r\n"
        f"Reply-To: hello@miamicontactimprov.com\r\n"
        "MIME-Version: 1.0\r\n"
        "Content-Type: text/plain; charset=UTF-8\r\n"
        "Content-Transfer-Encoding: 8bit\r\n"
        "\r\n"
        + body.replace("\n", "\r\n")
    )
    return base64.urlsafe_b64encode(msg.encode("utf-8")).decode("ascii")


def send(key):
    m = MESSAGES[key]
    raw = build_raw(m["to"], m["subject"], m["body"])
    (OUT / f"{key}.eml").write_text(m["body"], encoding="utf-8")

    payload = json.dumps({"raw": raw})
    p = subprocess.run(
        ["gws", "gmail", "users", "messages", "send",
         "--params", '{"userId": "me"}', "--json", payload, "--format", "json"],
        capture_output=True, text=True,
    )
    if p.returncode != 0:
        print(f"FAIL {key}: {p.stderr.strip()[:400]}")
        return False
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        print(f"FAIL {key}: unparseable response {p.stdout[:300]}")
        return False
    print(f"sent {key:20} -> {m['to']:38} id={d.get('id')} thread={d.get('threadId')} labels={d.get('labelIds')}")
    return True


if __name__ == "__main__":
    targets = sys.argv[1:] or list(MESSAGES)
    ok = all(send(k) for k in targets)
    sys.exit(0 if ok else 1)
