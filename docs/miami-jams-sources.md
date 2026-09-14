# Sources: the Miami-Dade and Broward jam list

Every URL read while building `/miami-jams`, the HTTP status observed from this host on
**2026-09-14**, and what was taken from it. Where a claim could not be confirmed, it is
marked **UNVERIFIED** rather than softened.

Method: `curl -sS -L --max-time 25/30` with a current desktop Chrome user agent, and the
`web_extract` and `web_search` tools for pages that refused `curl`. A status of `000` means
the connection timed out or failed at the transport layer from this host; it is not a
statement about the site being down for everyone. `web_extract` is a different network
path from `curl`, which is why one page below has both a `000` and a `200`.

The trap that governs this file: `Contact Improvisation Gold Coast` and `The Farm, Miami
4220` are **Miami, Queensland, Australia**, and `miamiimprov.com` is a comedy theatre.
Nothing from either is in this list.

---

## 1. The listing this page exists to correct

| URL | Status | Taken from it |
|---|---|---|
| `https://www.contactimprov.com/florida.html` | `000` by curl (connect timeout, 20s); content read at `200` via `web_extract` | The Florida page and every claim this site makes about it |

What that page held on 2026-09-14:

- **`Contact Improvisation in Miami`** — links only: `http://tribes.tribe.net/ciseflo` and
  `http://groups.yahoo.com/group/ciseflo/`, plus `INFO: Collin 305 323 4731`. No venue, no
  schedule, no cost, no date.
- **`Monday Night Community Jam / Workshop, Miami`** — `WHERE: Excello, 8700B SW 129th
  Terrace, Miami, FL`, `WHEN: Every first Monday of the month with rotating facilitators
  7-9 PM`, `COST: $10`, `INFO: 305-298-5879 karen`, `WEBSITE: Map at:
  www.karenpetersondancers.org`. **No year and no start date.**
- Sarasota (Rising Tide Center, 5102 Swift Road) and Jacksonville Beach (Ananda Kula, 102
  6th Ave N, Thursdays 7:30pm) entries, both of which read as current.
- **Zero Broward County entries.**
- The page's own request: *"Please also help us correct any outdated information."*

| URL | Status | Taken from it |
|---|---|---|
| `https://contactimprov.com/` (apex) | `000` (connect timeout, 20s) | Nothing. Recorded because the apex is the canonical host form and did not resolve from here |
| `http://tribes.tribe.net/ciseflo` | `404` | The link is dead. Tribe.net is gone |
| `https://tribes.tribe.net/ciseflo` | `000` (timeout) | Nothing |
| `http://groups.yahoo.com/group/ciseflo/` | `200`, but final URL is `https://www.yahoo.com/` | The link resolves, then lands on Yahoo's homepage: Yahoo Groups was shut down in 2020. It does not reach a Miami CI community |
| `https://www.contactimprov.com/members_usa_fl.html` | **not fetched directly by me** (curl `000`) | **UNVERIFIED by this lane.** A secondary report of the fetch says it returns `200` and carries Miami and Fort Lauderdale entries in which people describe themselves as Contact Improv teachers, with no venue, no schedule and no date. That is a name in a directory, not a session, so nothing from it was listed either way |

---

## 2. Miami-Dade: the sessions that are listed

### Contact Improv — ALL LEVELS (Dance Arts Miami)

| URL | Status | Taken from it |
|---|---|---|
| `https://www.eventbrite.com/e/contact-improv-all-levels-tickets-1999219825315` | `200` | Title, organiser **Esther Frances & Dmitry Krasnyanskiy**, venue **Dance Arts Miami, 250 Northeast 61st Street, Miami, FL 33137**, "Multiple dates", advertised as "connection, weight sharing, momentum, and spontaneous partnering… No partner needed", **"Your first class is just $22!"**, refunds up to 7 days before the event |
| `https://www.meetup.com/miami-adult-dance-calsses/events/rlgzztyjcmblb/` | `200` | **"Every week on Tuesday until February 28, 2027"**, Tue 6:00–7:00 PM EDT, `250 NE 61st St, Miami, FL`, **"Your first class is just $30! ( online bookings only )"**, hosted by "DanceArts M." in the "Miami Dance Classes for Adults" group |
| `https://sweatpals.com/event/contact-improv-all-levels/2026-10-13` | `200` | A dated instance: **Tue Oct 13 2026, 6:00–7:00 PM EDT, "Repeats weekly on Tuesdays"**, `250 Northeast 61st Street, Miami, FL`, **$30**, "Cancellation policy: No refunds", host Dance Arts Miami |
| `https://danceartsmiami.com/schedule` | `200` | **Negative result:** no `contact improv` string, no Tuesday entry, no price string on the rendered page. This is why the listing says the class is verified through the three platforms and not the studio's own site |
| `https://danceartsmiami.com/contact` | `200` | `info@danceartsmiami.com` (used as the outreach recipient) |

Reported on the page: weekly Tuesdays 6–7 PM, validated to 28 February 2027 by Meetup, first
class **$22 on Eventbrite / $30 on Meetup and SweatPals**, refund terms differing by
platform. All three prices are stated rather than one being chosen, because which is
correct could not be determined.

### Kama Flight — Flight Workshop (Skanda Yoga)

| URL | Status | Taken from it |
|---|---|---|
| `https://kamaflight.com/products/flight-workshop-miami-fl-october-18-2026` | `200` | **Date: October 18**, **Time: 3:00–4:30 PM**, **Skanda Yoga: 1800 SW 1st Ave #102, Miami, FL 33129**, **Ticket Type: Partner Pair (Admission for Two) — $50.00**, "Kama Flight is a fusion of acro yoga, Thai massage, and contact improv", proceeds fund the Kama Flight Foundation 501(c)(3) |
| `https://kamaflight.com/products/flight-workshop-miami-fl-november-15-2026` | `200` | The same product for **November 15**, 3:00–4:30 PM, `1800 SW 1st Ave #102 Miami, FL 33129`, $50.00 partner pair |
| `https://kamaflight.com/` | `200` | "Kama Flight is a new partner wellness modality, based on neuroscience, that combines acro yoga, Thai massage, and impromptu dance" |

**Caveat recorded on the page and unresolved:** both product pages contain the string
`Sold Out` *and* a live `Add to cart` control. Availability is therefore reported as
unclear rather than asserted either way. **UNVERIFIED** whether either date can be booked.

### Kama Flight — jams (Miami Beach)

| URL | Status | Taken from it |
|---|---|---|
| `https://kamaflight.com/collections/jams` | `200` | Exactly **one** Miami jam product in the collection: `09-08-26-miami-fl-jam-at-private-residence`. No later Miami date published |
| `https://kamaflight.com/products/09-08-26-miami-fl-jam-at-private-residence` | `200` | "Kama Flight Donation-Based Jam — September 8, 2026 — Miami, FL", **Time: 6:30–9:00 PM**, **2345 N Bay Rd. Miami Beach, FL**, donation tiers **$10 / $20 / $30**, "Each attendee must have a ticket", "100% of the proceeds… fund the Kama Flight Foundation" |

The 8 September 2026 date is **in the past** as of 2026-09-14, so the entry is published
with its date and explicitly not presented as a running session. This is a correction to
the earlier state of `build/listings.py`, which described these as "Recurring; dates
published individually" without saying that no next date was published.

### Camp Contact at Love Burn (Virginia Key)

| URL | Status | Taken from it |
|---|---|---|
| `https://loveburn.campcontact.org/` | `200` | "Application to Join Camp Contact at Love Burn **Feb 5-8** in Miami, FL at **Virginia Key Beach Park**"; "Event starts: Thursday, the 4th of February at 12:00 pm"; "Events from 2026 are live!!! Submissions are closed"; "**Love Burn starts in 143 days!**"; the camp states it loves "**Contact Improvisation Dance, Acro Yoga, Ecstatic Dance, Tai Chi, Massage, Hugs, and Authentic Relating**" |
| `https://theloveburn.com/` | `200` | **No street address found** in the response. The address `4020 Virginia Beach Drive` in the listing is carried from this project's check on 2026-09-13 and was **not** re-confirmed on 2026-09-14, which is why that entry keeps the 2026-09-13 checked date |
| `https://theloveburn.com/faq` | `404` | Nothing |
| `https://theloveburn.com/event-details` | `404` | Nothing |

The camp page prints month and day without printing the year, while its own countdown from
2026-09-14 points at early February 2027. The page also mixes a February "4th" and a
"Feb 5-8" range inside one paragraph. **UNVERIFIED:** the year of the next edition.
Reported on the page as a reason to read the source directly.

---

## 3. Broward: the sessions that are listed

### Ecstatic Dance Miami — Full Moon Immersion (Hollywood)

| URL | Status | Taken from it |
|---|---|---|
| `https://www.eventbrite.com/e/ecstatic-dance-miami-september-26th-full-moon-immersion-tickets-1999291383347` | `200` | "**Saturday, September 26 • 7 PM - 11:59 PM**", venue line "**Hollywood Lakes, Hollywood, FL**", overview: "Our Monthly Embodiment, Full Body Healing Experience through **Contact Improv**, Ecstatic Dance, Tantra, Aquatic Healingwork and Sound Healing", "4 hours 59 minutes", refunds up to 1 day before. **No price string on the page** |
| `https://ecstaticdancemiami.com/` | `200` | The organiser's own site: "Established 2014", "12+ Years", "200+ Gatherings", "**Every Full Moon**", "**For our Immersion Series: no tickets at the door and no drop-ins**", "Immersion events often sell out". **No `contact improv` string appears on this page** — the CI component is only claimed on the listing |

**Important correction to the listing's own data:** the Eventbrite page prints the venue as
`Hollywood Lakes, 1000 Somewhere Blvd, Hollywood, FL 33020`. `1000 Somewhere Blvd` is a
stand-in street address, not a real one, and the aggregator copy states the exact location
is emailed to ticket holders on the day and asks previous attendees not to disclose it.
This site therefore publishes the **city and county only**, and says the venue is withheld
by the organiser. No street address from that listing is reproduced.

### Ecstatic Dance Fort Lauderdale (Le Sound Temple)

| URL | Status | Taken from it |
|---|---|---|
| `https://ecstaticdance.org/dance/ecstatic-dance-ft-lauderdale/` | `200` | "**Saturday 7:30 pm TO 9:30 pm**", "**Frequency Monthly / First Saturday of the month**", "**Where 2501 NE 30th St, Fort Lauderdale, FL 33306**", "**How Much $33**", "Inaugural Gathering • September 5,2026", "Doors Open: 7:00 PM ✨ Journey Begins Promptly: 7:30 PM", cacao by Shamanic Tonic, breathwork by Vibration Integration, closing mini sound bath, "church parking lot" listed for parking |
| `https://www.lesoundtemple.com/events` | `200` | The venue's own page lists Alchemy Sound Bath (Tue/Thu/Sun 7:30–9:00 PM, $33 Zelle / $30 cash), Midday Reset Sound Bath (Tue 12:00–1:00 PM, $25) and monthly full-moon ceremonies. **It does not list the monthly ecstatic dance** — a negative result, and the reason the directory listing is named as the source to check |
| `https://www.lesoundtemple.com/` | `200` | `info@LeSoundTemple.com` (used as the outreach recipient) |
| `https://www.lesoundtemple.com/contact` | `404` | Nothing |

**UNVERIFIED:** whether an October or later edition has been confirmed. The listing states a
monthly first-Saturday frequency and names only the 5 September 2026 inaugural as a dated
gathering. The entry publishes the stated frequency and says the only dated gathering named
is the inaugural.

---

## 4. Broward: what was searched and did not exist

Searched against organiser pages, Eventbrite, Meetup and the conscious-dance directories:
Fort Lauderdale, Hollywood, Davie, Pembroke Pines, Sunrise, Plantation, Weston, Coral
Springs, Hallandale Beach, Miramar; "contact improvisation Hollywood Florida"; "contact
improv Fort Lauderdale"; "somatic dance Fort Lauderdale"; "Broward College / Nova
Southeastern dance community class"; and the Eventbrite and Meetup Broward dance listings.

**Result: no recurring Contact Improvisation jam, class series or workshop in Broward
County could be verified from any source that publishes about itself.** What Broward has is
conscious dance, which is on the page with its modality stated, and self-described CI
teachers in the World Jam Map's own member directory who publish no session.

Also read, and excluded:

| URL / source | Status | Why excluded |
|---|---|---|
| `https://ecstaticdance.org/region/florida/` | reported `200` by a secondary source; **UNVERIFIED by me** | Its Florida list is reported stale and does not carry the Fort Lauderdale dance despite that page existing |
| `https://improvftl.com/` | not fetched | Comedy theatre (Ft. Lauderdale Improv, Dania Beach) |
| `https://www.thisisimprov.com/` | `200` | Comedy. Its "Comedy Improv Jam" is a comedy open-mic in Davie |
| `https://www.browardcenter.org/classes` | `200` | "Adult Comedy Improv" classes, $235-$275. Theatre improv, not CI |
| `https://www.browardcenter.org/community` | `406` (bot-blocked) | Nothing readable |
| `https://www.eventbrite.com/.../Mainstreet Playhouse` / Short Round Improv | see search results | Comedy jam in Hialeah. The trap that owns the word "improv" in Miami |
| `https://centralcommandmiami.com/blogs/events/cypher-divine-break-jam` | see search results | Breakdance cypher in Wynwood, $5. Not CI |
| `https://trybooking.com/events/landing/970597` | see search results | **Australia.** Joerg Hassmann workshop at "THE FARM, 7/18 Mountain View Ave, MIAMI 4220" — Miami, Queensland |
| `https://citreasurehunt.com/united-states` | see search results | Global aggregator, no Miami entry found. Its own submission path is Telegram-gated and returns `429` to automated requests; never bypassed |
| `https://ecstatic.events/venues/msulbbz06ifd9bnl` | reported `200` | Third-party aggregator with no organiser-owned equivalent to verify against |
| Haux In Harmonie "Inner Ignition" at Le Sound Temple | reported `200` | Aggregators only, no organiser-owned page, and both listed dates (22 May 2026, 25 July 2026) are in the past. Cadence **UNVERIFIED** |
| `https://meetup.com/alternativedancenetwork` | reported `200` | Palm Beach Gardens-based; names CI among topics but posts no Broward CI event |
| Siesta Key / Sarasota, Jacksonville Beach, Orlando, St Petersburg, Casselberry, Delray Beach, Palm Beach entries | see search results | **Outside Miami-Dade and Broward.** Out of scope for this page by instruction |

---

## 5. Universities and arts agencies

| URL | Status | Taken from it |
|---|---|---|
| `https://carta.fiu.edu/theatre/` | reported `200` | Student-facing theatre department with a dance minor. Not a public listing surface |
| `https://community.fiu.edu/thearts/performing-arts/` | reported `200` | Public arts overview, not a listings board |
| `https://dance.frost.miami.edu/` | reported `200` | Dance programme; "Classes are open to undergraduate students". Student-only |
| `https://med.miami.edu/.../osher-center/.../community-classes` | reported `200` | Genuine public community classes, but it lists the centre's own programmes, not third-party jams |
| `https://www.mdc.edu/dance/` | reported `200` | Programme content, no community listing |
| `https://www.mdc.edu/community-engagement/` | `404` | Nothing |
| `https://nwsa.mdc.edu/dance/` | reported `200` | Student high-school and college programmes. `/community/`, `/about/community/` and `/events/` are reported as `200` returning "Page Not Found" bodies |
| `https://www.broward.edu/academics/programs/dance.html` | reported as `200` soft-404 | No dance/community page exists at that URL |
| `https://www.miamidadearts.org/organizations/cultural-resource-directory` | `200` | The Cultural Resource Directory page. "**It is free and easy to submit your organization's information**… All entries are subject to **editing and approval**." Contact: **culture@miamidade.gov**, Dana Pezoldt 305-375-4634. Used as outreach recipient 02 |
| `https://www.miamidadearts.org/organizations` | `200` | Directory index |
| `https://www.broward.org/Arts` | `200` | Broward Cultural Division. **No email published, no submission path.** Links to ArtsCalendar.com. This is why the Broward draft could not be addressed confidently |
| `https://artscalendar.com/` | `403` | **Could not be read from this host.** The Broward Cultural Division's calendar is linked from `broward.org/Arts` but neither its submission terms nor its contact address could be verified here |
| `https://artscalendar.com/contact` | `403` | Nothing |
| `https://artscalendar.com/arts-calendar-event-submissions/` | `403` | Nothing. A secondary report of `200` with a "four-week minimum lead time" and a `browardarts@broward.org` address is **UNVERIFIED and not relied on** |
| `https://www.miamiandbeaches.com/events/submit-event` | `404` | Dead. A secondary report of `200` is contradicted by this fetch. Excluded as a surface |

**Conclusion recorded on the page:** none of the university pages is a public listing surface,
so none was listed and none is treated as a place to advertise. Only two agency surfaces are
both open and legitimate for a non-commercial local resource: the **Miami-Dade Cultural
Resource Directory** (free, self-registration, editor-approved) and **ArtsCalendar.com**
(account-gated, editor-reviewed, unreadable from here).

---

## 6. Adjacent practice already on the site, re-checked

| URL | Status | Taken from it |
|---|---|---|
| `https://www.karenpetersondancers.org/` | `200` | Names "**Excello Dance Space**" among its residencies. **Negative result and the key one on this page:** no `contact improv`, no `jam`, no `Monday`, no `129th`, no `improvisation` string anywhere on the rendered page — so the World Jam Map's undated Excello jam is not supported by the organisation it is credited to |
| `https://www.5rhythms.com/teachers/Nathan+Shultz` | `200` | Still published as "5Rhythms Teacher in Training", under "Southeast US Teacher Community". Entry unchanged |

---

## 7. Research queries run

`browse.sh` did **not** exist at the documented path (`~/Desktop/Projects/agent-scripts/scripts/browse.sh`),
so research ran on `curl`, the `web_extract` tool and the `web_search` tool.

Queries included: contact improv jam Miami; contact improvisation class Fort Lauderdale
Broward; contact improv Miami Eventbrite; contact improv Meetup Miami; contact
improvisation Miami-Dade; CI jam Broward / Hollywood FL / Davie / Pembroke Pines / Sunrise /
Plantation / Weston / Coral Springs / Hallandale Beach / Miramar; somatic dance Fort
Lauderdale; contemporary dance improvisation class Broward; ecstatic dance Broward; Miami
studios hosting CI or somatic dance; FIU, Miami Dade College, New World School of the Arts
and University of Miami dance departments; Eventbrite and Meetup Miami dance listings.

---

## 8. Outreach prepared, not sent

Produced by `tools/local_outreach.py` into `/tmp/mci-local-outreach/` on 2026-09-14. **Nothing
was sent.** `SENDING_ENABLED` is `False` and `send()` raises if called. Exact RFC 822 bytes
are on disk per draft (`.eml`), with a base64url transport copy (`.b64`), a stated reason
(`.reason.txt`) and an index (`MANIFEST.json`).

| Recipient | Subject | Why this is a legitimate listing surface |
|---|---|---|
| `info@danceartsmiami.com` **(verified)** | Your Tuesday contact improv class is the only one on the open web in Miami | The venue that already hosts the session. Its own schedule page carries no CI entry, so this is asking a business to publish a session it hosts on the calendar it already operates |
| `culture@miamidade.gov` **(verified)** | Cultural Resource Directory: question about a non-commercial community resource | A free, editor-reviewed county directory run by the Department of Cultural Affairs, whose page invites submissions and states entries are subject to approval. The ask is an eligibility question put to the directory's operator |
| ArtsCalendar.com submission route — **recipient UNVERIFIED** (`403` from this host) | Submitting a Broward County listings resource to ArtsCalendar | The Broward Cultural Division's own calendar, linked from the county's Cultural Division page, with hand review before posting. Read `https://artscalendar.com/register` before addressing it |
| `info@LeSoundTemple.com` **(verified)** | Your monthly ecstatic dance is the clearest recurring Broward listing I could verify | The venue hosting the monthly gathering, whose own events page already publishes its recurring sound baths and breathwork — so this adds a series it hosts to the calendar it runs |
| `moti@contactimprov.com` **(verified)** | Following up on the Florida page: two links and one undated Miami entry | The World Jam Map's published correction channel, which asks in writing to be sent outdated information. Follows this project's first message of 2026-09-13 |

Not pursued, and recorded so the omission is deliberate: **university community pages**
(every page reachable was a student registration portal or a programme description, so there
is no listing to ask for), **Eventbrite and Meetup** (self-publish channels owned by each
organiser — this site links to them rather than asking to be listed in them),
**miamiandbeaches.com** (`404`, and the submission target was a partner extranet login in any
case), **Broward Cultural Division's own pages** (no submission path and no published email),
and **CI Treasure Hunt** (`429` to automated requests, Telegram-gated submission — a rate
limit was not bypassed).

---

## 9. Known gaps in this page

- **Broward has no Contact Improvisation entry, because none could be verified.** The two
  Broward entries are conscious dance and are labelled as such every time they appear.
- **The `Sold Out` ambiguity** on both Kama Flight workshop pages is unresolved.
- **The Love Burn year** is unresolved; the camp page prints no year beside its dates.
- **The October Ecstatic Dance Fort Lauderdale edition** is not confirmed; only the
  frequency is published.
- **ArtsCalendar.com was unreadable from this host**, so one of the five outreach drafts has
  no verified recipient.
- **`https://www.contactimprov.com/` and its subpages other than `florida.html`** are
  unreachable from this host by `curl`. The Florida page content came through `web_extract`;
  `members_usa_fl.html` and `linksusa.html` did not, so nothing from them is relied on.
- **`/miami-jams` and `/jams` overlap.** Both render `listings.SESSIONS`. The new page adds a
  per-entry organiser, a labelled source URL and a checked date, and the section on what
  could not be verified; `/jams` carries the narrative. Resolving the overlap properly means
  editing `build/content_practice.py`, which this lane was told not to touch because a
  concurrent lane owns it. Flagged in the PR rather than worked around.
