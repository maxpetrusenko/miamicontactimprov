"""The Miami-Dade and Broward jam list: every session this site could verify, dated.

Why this page exists. The best-known Contact Improvisation listing for Florida is the
World Jam Map's Florida page, and when it was opened on 14 September 2026 it carried one
Miami entry with no year on it and two links that no longer reach a Miami community. A
list that shows the date each entry was checked, names the organiser for each one, and
says plainly what could not be found is the only version of this page worth publishing.

Nothing here is ranked, nothing is paid for, and an entry comes down rather than going
stale. Every source URL and the HTTP status it was read at is in
docs/miami-jams-sources.md.
"""

import html

COUNT_WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}


def _count():
    n = len(listings.SESSIONS)
    return COUNT_WORDS.get(n, str(n))

from shell import LAST_CHECKED, answer, band, cite_block, facts, page
import listings
import schema

PAGE_CHECKED = "2026-09-14"

# What the World Jam Map's Florida page looked like on 14 September 2026, read at
# https://www.contactimprov.com/florida.html. Recorded here as prose because it is the
# comparison this page exists to make, and because the map itself asks to be corrected.
JAM_MAP_FINDINGS = [
    ("Miami entries on the map", "One, printed with no year and no start date"),
    ("Broward County entries on the map", "None"),
    ("'Contact Improvisation in Miami' links", "Two, and neither reaches a Miami CI community any more"),
    ("tribes.tribe.net/ciseflo", "HTTP 404. Tribe.net is gone"),
    ("groups.yahoo.com/group/ciseflo/", "HTTP 200, but it lands on yahoo.com's homepage: Yahoo Groups was shut down in 2020"),
    ("The rest of the Florida page", "Sarasota and Jacksonville Beach entries, both of which read as current"),
]


def _field_rows(name):
    """The labelled facts for one session, in the order the honesty rules need them."""
    for row in listings.SESSIONS:
        if row[0] != name:
            continue
        _n, modality, city, venue, schedule, cost, url, verified, _note = row
        organiser = listings.SESSION_ORGANISERS.get(name, ("Not recorded", ""))
        return [
            ("Organiser", html.escape(organiser[0])),
            ("Modality", html.escape(modality)),
            ("Where", f"{html.escape(venue)} ({html.escape(city)})"),
            ("When", html.escape(schedule)),
            ("Cost", html.escape(cost)),
        ]
    raise KeyError(name)


def _session_items():
    items = []
    for name, _modality, _city, _venue, _schedule, _cost, url, verified, note in listings.SESSIONS:
        items.append(f"""<li>
  <h3>{html.escape(name)}</h3>
  {facts(_field_rows(name))}
  <p>{html.escape(note)}</p>
  <p>Read at <a href="{html.escape(url)}" rel="noopener nofollow">{html.escape(url)}</a></p>
  <p><strong>Checked {html.escape(verified)}</strong></p>
</li>""")
    return "".join(items)


def _sessions_block():
    if not listings.SESSIONS:
        return (
            '<div class="prose"><h2>What is running in Miami-Dade and Broward</h2>'
            "<p>Nothing currently. This page removes an entry rather than leaving a stale one, so an "
            "empty list means an empty verified list and not an empty city. The studios and organisers "
            "on the <a href=\"/directory\">directory</a> are where the answer actually lives.</p></div>"
        )
    return (
        '<div class="prose"><h2>What is running in Miami-Dade and Broward</h2>'
        f"<p>{_count()} entries. Each one names who runs it, where it is, when it is, what it costs and what kind "
        "of practice it actually is, and each carries the date its source was opened and read. This page ranks "
        "nothing: none of these is paid for, and no entry is recommended over another. One of them, the Friday "
        "jam in Miami, is hosted by the maintainer of this site; its entry says so, and it is held to "
        "the same rules as the rest.</p>"
        f'<ul class="dir-list">{_session_items()}</ul></div>'
    )


def miami_jams():
    findings = facts(JAM_MAP_FINDINGS)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Miami-Dade and Broward</p>
    <h1>Every contact improv session in Miami-Dade and Broward we could verify.</h1>
    <p class="lede">{_count()} entries, each with the organiser, the room, the price, the modality and the date it was checked. Plus the two things most lists get wrong about Florida, and an honest account of what could not be found.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("The recurring Contact Improvisation practice we could verify in Miami-Dade and Broward is one weekly all-levels class at Dance Arts Miami on Tuesday evenings, one weekly open jam on Friday evenings at Inner Motion Dance Studio on the north edge of Miami, in Hallandale Beach, from 2 October 2026, which is hosted by the maintainer of this site, two dated workshops in Miami from a contact-adjacent practice that fuses acro yoga, Thai massage and contact improv, one annual festival camp on Virginia Key, and two recurring conscious-dance gatherings in Broward County that advertise a contact improv component among other practices. No other Contact Improvisation jam or class in Broward County could be verified from a source that publishes about itself. Every entry below names the page it was read on and the date it was checked.")}
    <div class="prose">
      <p>Last updated <strong>14 September 2026</strong>. Every entry carries its own checked date, and a
      session whose source has gone quiet comes off this page rather than sitting here looking current.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {_sessions_block()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      <h2>What this page corrects</h2>
      <p>The World Jam Map keeps the global listing of CI jams, and its <a href="https://www.contactimprov.com/florida.html" rel="noopener nofollow">Florida page</a> is the one page on the open web that mentions a Miami jam. It asks to be corrected, in its own words: <em>Please also help us correct any outdated information.</em> So here is what it held when it was opened on 14 September 2026 and read line by line.</p>
      {findings}
      <p>The Miami entry is a <em>Monday Night Community Jam / Workshop</em> at Excello Dance Space, 8700B SW 129th Terrace, on the first Monday of the month from 7 to 9 PM, with a $10 cost, credited to Karen Peterson Dancers. It carries no year and no start date, so there is no way to tell from the page whether it ran last month or last decade, and a reader who turns up on the strength of it is taking a real chance.</p>
      <p>Karen Peterson Dancers is a current, active Miami company, and its own site does name Excello Dance Space. What its site does not publish is a contact improvisation jam, a Monday session, or that address. So the jam cannot be confirmed from the organisation it is credited to, and this site does not list it as running. If you are the person who holds it, <a href="/about#submit">send us the schedule</a> and it goes on this page with a source and a date, which is all it has ever been missing.</p>
      <p>The two links under <em>Contact Improvisation in Miami</em> are worse than undated, because they look answerable. The Tribe.net one returns a 404: the host is gone. The Yahoo Groups one returns a redirect to Yahoo's homepage, because Yahoo Groups was shut down in 2020 and the group archives with it. A reader following either link to find the Miami community arrives nowhere and has no way to know whether that is a temporary outage or the state of the scene.</p>
      <p>And Broward County does not appear on the Florida page at all. That is not a criticism, it is the shape of the problem: Florida's CI listing is built from what organisers have sent in, and Broward organisers have not sent anything.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      <h2>What is not on this page, and why</h2>
      <p>Most of a listing page is the part nobody sees. These are the things that were searched for, opened where possible, and left out.</p>
      <h3>A contact improvisation jam in Broward County run by anyone else</h3>
      <p>Not found. The one jam on this page with a Broward address, the Friday jam on the north edge of Miami in Hallandale Beach, was started by the maintainer of this site, and it is listed above on the strength of this site's own page rather than a third party's. Beyond it: Fort Lauderdale, Hollywood, Davie, Pembroke Pines, Sunrise, Plantation, Weston, Coral Springs, Hallandale Beach and Miramar were all searched, against organiser pages, the Eventbrite and Meetup listings, and the conscious-dance directories. What Broward has is ecstatic dance, which is on this page with its modality stated, and a handful of self-described Contact Improvisation teachers in the World Jam Map's own member directory who publish no session, no room and no date. A name in a directory is not a jam, so it is not listed here.</p>
      <h3>University dance departments as a route in</h3>
      <p>FIU, Miami Dade College, New World School of the Arts and the University of Miami all publish dance programmes, and the pages that could be reached are student registration portals or course descriptions. None of them publishes a public, recurring contact improvisation session, and none of them is a listings surface, so none is listed and none is treated as a place to advertise. If a department does open a community session, that is a real thing to list and we would like to hear about it.</p>
      <h3>Everything spelled 'improv' that is not this</h3>
      <p>Search for improv in Miami and you are shown comedy: theatres, clubs, open-mic nights and weekly comedy jams, several of them in Hialeah and Fort Lauderdale, and one theatre whose domain is close enough to this one's subject to be worth naming as not us. Those are good evenings and they are not Contact Improvisation, and they are not on this page.</p>
      <h3>Undated listings, presentable or not</h3>
      <p>Any entry with no date on its own source is excluded, however plausible it looks. That is the rule that removes the Excello jam above, and it is the rule that will keep this page short. A short honest list is the whole point: the CI World Jam Map's Florida page is the cautionary example of what a long optimistic one becomes.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      <h2>How to use this list</h2>
      <p>Treat every entry as a lead with a date on it rather than a fact. Open the source link, which is the organiser's own page or listing, and check for a date of its own: a recurring session whose source has not been posted to in months has usually stopped, and a listing with no date is evidence of nothing. Then send a message before you travel. Organisers answer, and they would rather tell you than have you arrive at a locked door.</p>
      <p>What each session is actually like to attend, and how a jam runs from the opening circle to the last dance, is on <a href="/jams">jams</a> and <a href="/your-first-jam">your first jam, step by step</a>. What to do in the weeks after your first one is on <a href="/keep-practising">keep practising</a>. What Contact Improvisation is, if you have never read anything about it, starts at <a href="/what-is-contact-improvisation">what is Contact Improvisation</a>.</p>
      <p>This page takes no money for listing any of these sessions and does not rank them. One of them, the Friday jam, is run by the person who maintains this page, and its entry says so. It is one map of a scene with no central authority, and it is not the map.</p>
    </div>
    {band("Run a session in Miami-Dade or Broward?", "Send the schedule, the room, the price and where you publish it. A listing here means one thing: the organiser publishes it and we checked the page. It is not an endorsement.", [("Submit a session", "/about#submit", "primary"), ("The wider directory", "/directory", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Contact improv jams and classes in Miami-Dade and Broward</em>. miamicontactimprov.com. https://miamicontactimprov.com/miami-jams")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/miami-jams",
            "Contact improv jams and classes in Miami-Dade and Broward",
            "A dated list of the Contact Improvisation jams, classes, workshops and recurring movement "
            "sessions verified in Miami-Dade and Broward County, each with its organiser, venue, schedule, "
            "price, stated modality and the date its source was checked.",
            date_modified=PAGE_CHECKED,
        ),
        schema.breadcrumb("/miami-jams", "Miami-Dade and Broward jam list"),
        schema.item_list(
            "/miami-jams",
            "Contact improv jams and classes verified in Miami-Dade and Broward",
            [(row[0], row[6], row[1]) for row in listings.SESSIONS],
        ),
        listings.events_schema(),
    )
    return page(
        "Miami & Broward Contact Improv Jams [Updated for 2026]",
        "A dated list of every Contact Improvisation jam, class and workshop verified in Miami-Dade and "
        "Broward County, with organiser, venue, schedule, price and modality for each.",
        "/miami-jams",
        body,
        jsonld=jsonld,
    )
