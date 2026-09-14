# miamicontactimprov.com — listing follow-up plan

**Prepared:** 2026-09-14. **Status:** preparation only. Nothing was sent, no account was created,
nothing was purchased, no terms were accepted.

**This document is a follow-up plan, not a repeat.** Submissions already went out by email on
**2026-09-13**:

| Recipient | What was sent |
|---|---|
| `moti@contactimprov.com` | The links page, two dead Florida-page links, and the undated Excello jam |
| `bodydiary@ciglobalcalendar.net` | A question; CIGC is self-organiser-only |
| `info@contactquarterly.com` | A Miami entry, plus Florida missing from the CI Contacts List |

Do **not** re-pitch any of those three with the same content. Everything below either answers a
question one of those messages left open, corrects a fact that has changed, or opens a surface that
was not in the first pass.

`tools/local_outreach.py` already holds five prepared-and-unsent drafts. **That file is extended, not
duplicated**: the follow-up messages live in the same file in a `FOLLOWUP_DRAFTS` list, reachable with
`--set followups`. Its `SENDING_ENABLED = False` guard and its raising `send()` are unchanged, and
they apply to the new set too.

**All statuses and quotes below were read on 2026-09-14** with `curl -L` and a desktop Chrome UA, with
the HTML tag-stripped to read the body text. Anything that could not be read is marked **UNVERIFIED**
with the reason. No address was guessed.

---

## 1. What changed since 2026-09-13, re-checked 2026-09-14

| Surface | Yesterday's state | Today, read live | Consequence for the follow-up |
|---|---|---|---|
| contactimprov.com Florida page | Two dead links, one undated jam | **Unchanged.** Still publishes `http://tribes.tribe.net/ciseflo`, `http://groups.yahoo.com/group/ciseflo/`, and the Excello entry with no year | The correction is still valid. No new correction to add |
| contactimprov.com — **free route** | Not previously read | **New finding.** `becomemember.html` (200) states: *"**FREE Basic Membership** Includes: Member listing on the site. Option to purchase individual event listings"* | The earlier message implied the only route was a listing. There **is** a free member listing. This is the single most useful thing to add |
| contactimprov.com — paid route | Not previously read | `worldjammap.html` (200): *"Purchase individual events listings on the world workshop/event calendar for **$5 per listing** by becoming a free member (profile display optional)"* | The $5 is a paid add-on, not a prerequisite. Say so explicitly so nobody pays by accident |
| ciglobalcalendar.net | Asked a question; told self-organiser-only | **New route found.** `/post/get-involved` (200): *"Direct access to Country/Regional contents — If you are the developer of a regional/country website you can include a **snippet that show just the events related to your area**."* | There is a legitimate integration path that is not a listing. Ask for it |
| contactquarterly.com Contacts List | Asked whether the list is individuals-only | **Answered by the page itself** (200): *"The Contacts List is a referral directory … It lists **individuals and organizations** who are willing to refer people to Contact activities in their area."* | Stop asking that question — it is answered. Ask only for the **add route** |
| contactquarterly.com — Florida gap | Reported missing | **Confirmed by direct read**: the state headings under United States are CA, CO, CT, GA, IL, MA, MD, MI, MN, NM, NY, NC, OH, PA, RI, TX, VT, WA, WI. **Florida is absent** | The evidence for the ask is now quotable rather than asserted |
| Broward ArtsCalendar | Draft 03 recorded **HTTP 403** and marked the address **UNVERIFIED** | **Corrected.** `artscalendar.com/contact` returns **200** and publishes *"Email: **browardarts@broward.org**"* plus *"(954) 357-7457"*. The root returns 200 | Draft 03's provenance line is wrong and its question 2 ("what is the correct submission route? I could not read the submission page") is no longer true. Both are fixed in the extension |
| contactquarterly.com newsletter | Treated as a live channel | **Downgraded.** The page (200) does carry *"We welcome your reports, writings, essays (1,500 words max)"*, but the only deadline banner rendered is *"NEXT NEWSLETTER DEADLINE: September 1, 2019 — For the next CI Newsletter: Vol. 45 #1, Winter/Spring 2020"* | **UNVERIFIED as a live channel.** Pitching a newsletter whose last visible deadline is 2019 is a wasted send. Do not draft for it until a current deadline is seen |

---

## 2. The follow-up queue, in order

Order is by (a) whether the recipient already opened the thread, (b) how cheap the ask is, and
(c) whether the surface is a real publisher of a listing rather than a place to leave a link.

### 2.1 contactimprov.com — Moti (World Jam Map) — **first**
**Send:** `06-contactimprov-free-member-route.eml` → `moti@contactimprov.com`
**Re-checked:** Florida page 200; `becomemember.html` 200; `worldjammap.html` 200, all 2026-09-14.

**What to ask now.** One question only: does a non-commercial city-level resource site qualify for the
**free Basic Membership member listing**, given the page says Basic Membership "Includes: Member
listing on the site"? Add the plain statement that the project will not buy the $5 per-event listing,
so nobody has to wonder whether the silence is a sales tactic.

**What a legitimate listing looks like here.** A member-directory entry is the site's own product,
published by the site, for a member. The site asks in writing to *"help us correct any outdated
information"*. Both are publisher actions.

**What would be a link scheme.** Paying $5 for an event listing purely to obtain a followed link,
or offering a reciprocal link in exchange for placement. Neither is proposed.

**Risk note.** No address, no entity, no fee required for the free route. The contact name and phone
number on the Florida page belong to third parties (Collin, Karen Peterson Dancers) and must not be
reproduced or contacted.

### 2.2 ciglobalcalendar.net — **second**
**Send:** `07-ciglobalcalendar-regional-snippet.eml` → `bodydiary@ciglobalcalendar.net`
**Re-checked:** `/post/get-involved` 200, `/post/help-how-to-insert-contents` 200, 2026-09-14.

**What to ask now.** Do not re-ask whether a city hub can be an event — the Help page still answers no,
and *"if the topic of the event is not about Contact Improvisation it will be removed and your account
will be disabled by the administrator."* Ask instead for the **regional/country snippet** so
miamicontactimprov.com can surface the real Florida CI events already in the calendar and cite the
calendar as the source of truth. Second ask: which Miami organisers are already registered, so the site
points at them rather than duplicating them.

**What a legitimate listing looks like here.** An embedded events feed sourced from the calendar, with
the calendar credited as the publisher. The calendar keeps the authority; the site becomes a mirror.

**What would be a link scheme.** Registering an account to post a "Miami resource" pseudo-event whose
only purpose is to emit a backlink. That is exactly what the editor disables accounts for.

**Risk note.** Free, no address required. Contact routes are the site's own forms
(`/contactForm/compose/project-manager`, `/contactForm/compose/administrator`) — use those rather than
assuming an address.

### 2.3 contactquarterly.com — **third**
**Send:** `08-contactquarterly-add-route.eml` → `info@contactquarterly.com`
**Re-checked:** Contacts List 200, 2026-09-14.

**What to ask now.** Cite the line back — *"It lists individuals and organizations"* — and state that
this answers the earlier question, so the only thing outstanding is the **add route**: the page offers
*"Log in to edit your listing"*, which presumes the reader is already listed, and no route for
proposing a new entry is published. Attach the Florida gap as a one-line fact with the evidence that
Florida is absent from the state headings.

**What a legitimate listing looks like here.** A referral-directory entry in a directory that says it
lists organisations. That is a listing in the plain sense.

**What would be a link scheme.** Offering to add a reciprocal link to CQ from the Miami site in
exchange for an entry. Not proposed, and it should not be offered if asked.

**Risk note.** No fee, no address, no entity. Do not chase the newsletter in the same message — see
§1, its deadline banner is from 2019 and the channel is **UNVERIFIED as live**.

### 2.4 Broward Cultural Division — ArtsCalendar — **fourth**
**Send:** corrected `03-broward-arts-calendar.eml` → `browardarts@broward.org`
**Re-checked:** `artscalendar.com/contact` **200**, 2026-09-14.

**What changed.** This draft's provenance line said the host returned 403 and that the address was
unverified. Both are now wrong: the page loads and publishes the address. The body's question 2
(*"I could not read the submission page from here, so I would rather be told the right one than
guess"*) is also no longer accurate and now reads as false. The extension rewrites both.

**What to ask now.** Whether a non-commercial listings resource belongs on a county arts calendar, or
whether the calendar is for dated events and performances only. That is still the open question —
eligibility was never readable from the page.

**Risk note.** No fee. A county-run calendar is a public listing service; no address is requested of
the submitter, though the calendar's own office address and phone are published.

### 2.5 DanceSeekers — **fifth, and only as a question**
**Send:** `09-danceseekers-eligibility.eml` → the `/get-listed` form (no address is published on the
page that was read; do not guess one)
**Re-checked:** `danceseekers.com/get-listed` **200**, `/communities` **200**, 2026-09-14.

The page invites exactly four things and says so verbatim: *"Know an event, studio, recurring social,
or class series that belongs on the map? Tell us about it - something you run, or something you love.
**We verify every submission**, then publish a dedicated page that links back to the organizer's
website and socials. **Free.**"*

A city-level resource hub is none of the four categories. It also runs a Miami scene page
(*"Miami, FL 23 organizers · 148 events"*), so someone there already knows the local scene better than
the site does. **Ask, do not submit.** If a hub does not fit, the correct next move is to point their
Miami page at the verified jams, not to get a listing.

**Risk note.** Free. But this is the one target in the set where the *only* thing on offer is
"a dedicated page that links back to the organizer's website and socials" — i.e. if an entry were
manufactured to fit one of the four categories, that is a link scheme. Flagged as such.

---

## 3. Surfaces checked and NOT pursued, with the reason

| Surface | HTTP (2026-09-14) | Why it is out |
|---|---|---|
| **DanceUs.org** — `danceus.org/about/contribute/` | 200 | **Link scheme.** *"The stories should be unique and non-promotional."* and *"We do not pay for contributed content at this time."* The directory side sells *"School, Studio or Venue listing (SEO)"*. A guest post placed for the link is the reciprocal-link pattern this project avoids |
| **CI Treasure Hunt** — `citreasurehunt.com` | **429** | Rate-limited on `/`, `/faq` and `/submit`. Recorded and **not retried or bypassed**. The status is the finding. Note: a secondary web result claims a contact address for this site — that address was **not** read on the site, so it must not be used |
| **Earthdance — "Regional Resources"** | 200 | **Wrong kind of page.** It is visitor logistics: *"Nearest gas stations: Mobil in Ashfield, MA-12 miles…"*. Earthdance's CI page links only its own events calendar; it publishes no third-party CI directory |
| **contactimpro.org** | 200 | Québec/Montréal association only. Publishes `info@contactimpro.org`, but there is no US-facing listing surface |
| **contactquarterly.com CI Newsletter** | 200 | **UNVERIFIED as a live channel** — last rendered deadline is 2019/2020. See §1 |
| **contactimprov.com World Workshop/Event Calendar, paid route** | 200 | **$5 per listing.** The free member route is preferred; do not pay for a calendar entry |

---

## 4. Drafts and where they are

Extended in place in `tools/local_outreach.py` (no second helper was created):

```bash
python3 tools/local_outreach.py                 # the original 5, writes to /tmp/mci-local-outreach
python3 tools/local_outreach.py --set followups # the 5 follow-ups, same writer, same guard
python3 tools/local_outreach.py --set all       # both
```

Each draft is written as exact RFC 822 bytes (`.eml`), a base64url transport copy (`.b64`), and a
`.reason.txt` carrying the recipient's provenance, the one-line reason the surface is a legitimate
listing rather than a link scheme, and what needs Max. `MANIFEST.json` records
`"sending_enabled": false` and `"sent": 0`.

| Key | Recipient | Subject |
|---|---|---|
| `03-broward-arts-calendar` (corrected) | browardarts@broward.org | Submitting a Broward County listings resource to ArtsCalendar |
| `06-contactimprov-free-member-route` | moti@contactimprov.com | The free member route: does a city resource qualify? |
| `07-ciglobalcalendar-regional-snippet` | bodydiary@ciglobalcalendar.net | Regional snippet for Florida, and who is already registered |
| `08-contactquarterly-add-route` | info@contactquarterly.com | The Contacts List add route, and Florida |
| `09-danceseekers-eligibility` | form at danceseekers.com/get-listed | Eligibility question: does a city resource fit your four categories? |

## 5. What needs Max's hands

1. **Approve a Broward sender identity.** `browardarts@broward.org` is a county desk; the corrected
   draft uses the public project identity only, and that is the correct choice here.
2. **Decide the newsletter question.** If the CQ CI Newsletter is to be used at all, someone has to
   confirm it is still running — its published deadline is from 2019.
3. **DanceSeekers:** if the ask is rejected on eligibility, decide whether to offer the Miami jam
   list to their Miami scene page as a correction instead.
4. **CI Treasure Hunt:** needs a human browser session, because this host rate-limited the reader. Do
   not retry from a script.

## 6. Blockers

- **CI Treasure Hunt** — 429 from this host on 2026-09-14. Unblock condition: a browser session reads
  `/faq` and `/submit` and takes the contact route from the page itself.
- **CQ CI Newsletter** — UNVERIFIED cadence. Unblock condition: a current deadline banner is read on
  the newsletter page.
- **DanceSeekers contact address** — none published on `/get-listed`. Unblock condition: read `/contact`
  or the form's own response page; do not guess the pattern.
