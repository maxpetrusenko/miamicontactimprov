"""Directory pages: the Miami hub, the directory, FAQ, about, 404."""

from shell import answer, band, cards, cite_block, facts, page
import schema
import listings

MIAMI_FAQ = [
    ("Is there contact improvisation in Miami?",
     "Yes. A recurring all-levels Contact Improvisation class runs weekly on Tuesdays at Dance Arts Miami, 250 NE 61st Street. Beyond that, Miami's contact practice sits inside a wider movement community: Kama Flight runs contact-adjacent jams and workshops that fuse acro yoga, Thai massage and contact improv, and Camp Contact brings contact improvisation to the Love Burn festival on Virginia Key each February. Contact improvisation has been practised in South Florida for decades, organised by individuals rather than through any institution."),
    ("Why does searching for 'improv Miami' not find this?",
     "Because in Miami, as in most cities, the word improv belongs to comedy theatre. Searching 'improv Miami' returns comedy clubs in Doral and Dania Beach. The dance form is found under its full name, 'contact improvisation', or as 'contact improv'. That naming collision is one reason the Miami dance scene is under-documented, and it is why this site spells the whole thing out."),
    ("Where do people dance contact improv in Miami?",
     "Rented studio space, a residence in Miami Beach, a warehouse or wellness venue, and outdoors at Virginia Key during the annual burn. Miami's practice follows the same pattern as every other city: someone books a room for two hours, tells people, and a jam exists. The rooms change; the format does not."),
    ("Do I need a partner to attend?",
     "No, and bringing one is not required. Jams are designed so that people arrive alone and dance with whoever is willing. Attending with a partner is fine, but you are not expected to spend the session with them."),
    ("Is it taught in English, Spanish, or both?",
     "Miami is bilingual, and organisers in Miami-Dade typically work in both. Contact improvisation is mostly taught through touch and demonstration, so language matters less than in most movement classes, but ask if you are unsure."),
    ("Can contact improvisation happen outdoors in Miami?",
     "It does, at least once a year and at scale, at Love Burn on Virginia Key. Outside a festival, the practical constraints are heat, humidity, sand and rain. Sessions tend to run early morning or after sunset, on grass or a hard flat surface, with more water than you think you need."),
    ("Is there a contact improvisation festival in Florida?",
     "Not on the scale of the European or West Coast CI festivals. Florida's CI practice has centred on recurring local sessions in Miami, Sarasota, Gainesville, Orlando and Jacksonville, several of which are listed on the CI World Jam Map's Florida page. Miami's own large gathering is Love Burn, which is a regional burn with contact improvisation inside it rather than a CI festival. Travelling dancers go to the national and international festivals."),
    ("How do I start a jam in Miami?",
     "Book a studio for a recurring two-hour slot, choose whether it is open or experienced, write the protocol down and say it out loud at the start of every session, set a door fee that covers the room, and list it somewhere public. Two hours a week and a consistent room is the entire infrastructure."),
]


def miami():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in MIAMI_FAQ)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">The city</p>
    <h1>Contact Improvisation in Miami.</h1>
    <p class="lede">Miami is a city of borrowed rooms and unofficial scenes. Contact improvisation here runs the same way: a teacher with a space, a company with a studio, a dancer with a phone number, and whoever turns up.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("Contact Improvisation has been practised in South Florida for decades, organised by individuals rather than through any institution. Miami has no standing CI venue or central calendar. Practice has historically run through rented studio space, such as the community jam listed at Excello Dance Space, and through sections of Miami's wider contemporary, physically integrated and somatic movement community. Because the form has no licensing body, the scene is whatever the people in it build.")}
    {facts([
      ("Country", "United States"),
      ("State", "Florida"),
      ("Counties in scope", "Miami-Dade and Broward"),
      ("Cities and neighbourhoods", "Miami, Miami Beach, Wynwood, Little Havana, Brickell, Coral Gables, Doral, Hialeah, Pinecrest, Fort Lauderdale"),
      ("Languages", "English and Spanish"),
      ("Best months for outdoor practice", "November to April"),
      ("Hardest months for outdoor practice", "June to September: heat, humidity and rain"),
      ("How the scene is organised", "Individually. No central body, venue or calendar"),
    ])}
    <div class="prose">
      <h2>The honest state of it</h2>
      <p>It is worth being direct, because most city guides are not. Miami's contact improvisation scene is small and largely undocumented online. What exists is real but scattered: one weekly all-levels class at Dance Arts Miami, a contact-adjacent jam and workshop programme run by Kama Flight out of Miami Beach, and Camp Contact bringing contact improvisation to Love Burn on Virginia Key each February. Those four things are what this site could verify, and they are listed on <a href="/jams">the jams page</a> with their sources and the date each was checked.</p>
      <p>The rest of the picture is thinner than a directory would like. The global CI World Jam Map carries a monthly Monday community jam at Excello Dance Space with rotating facilitators and a ten dollar door; that listing is undated and this site does not present it as current. Miami's older CI organising ran through platforms that no longer exist: a Yahoo Group and a Tribe.net community, both of which shut down with their hosts. Miami's physically integrated dance company, Karen Peterson Dancers, is active and current and has long been part of the city's improvisational and partner-work landscape, which is why it appears in the directory rather than being written off with the dead links.</p>
      <h2>Where the answer actually lives</h2>
      <p>Nobody can tell you where the jam is tonight from a static web page. The places that can:</p>
      <ul class="dir-list">
        <li><p><strong>The organisers themselves</strong></p><p>Every one of them publishes their own listings and answers a direct message. This is the fastest and most reliable route, and it is why the directory exists.</p><p><a href="/directory">The directory</a></p></li>
        <li><p><strong>The CI World Jam Map, Florida page</strong></p><p>The global community's own listing. It is honest about being patchy and asks readers to send corrections.</p><p><a href="https://www.contactimprov.com/florida.html" rel="noopener nofollow">contactimprov.com/florida.html</a></p></li>
        <li><p><strong>Searches that work</strong></p><p><code>contact improvisation Miami</code>, <code>contact improv South Florida</code>, <code>CI jam Florida</code>. Searches that do not: anything built on the bare word <code>improv</code>, which in Miami returns comedy theatres in Doral and Dania Beach.</p></li>
      </ul>
      <h2>One trap worth naming</h2>
      <p>A web search for contact improvisation in Miami will sooner or later surface "Contact Improvisation Gold Coast" and events at "The Farm, Miami". Those are in Miami, Queensland, Australia, postcode 4220. They have nothing to do with Florida and they are excluded from every listing on this site.</p>
      <h2 id="start-one">If there is no jam near you, start one</h2>
      <p>This is not a consolation prize. Most jams in the world exist because one person booked a room. The minimum viable version costs about two hours of studio rental a week and an hour of admin.</p>
      <ol class="dir-list">
        <li><p><strong>Find a floor.</strong> A dance studio with a sprung or marley floor, ideally with mats and a wall for sitting. Community centres and yoga studios work. Avoid tile, concrete and carpet.</p></li>
        <li><p><strong>Pick a recurring slot and keep it.</strong> Consistency beats frequency. The same evening every week builds a room; a different evening every month never will.</p></li>
        <li><p><strong>Decide who it is for.</strong> An open jam accepts everyone and needs a longer warm-up. An experienced jam accepts dancers who already know how to fall safely together. State which it is, every time.</p></li>
        <li><p><strong>Write the protocol down, and say it out loud.</strong> Continuous consent, the right to decline anything, no teaching uninvited, no filming without asking, the edge is for resting, and here is who is holding the room. Two minutes at the start of every session.</p></li>
        <li><p><strong>Set a door fee that covers the room.</strong> Not to make money: to make the jam survive past the third week.</p></li>
        <li><p><strong>List it.</strong> A page, an account, a recurring calendar entry, and an entry on the World Jam Map. Then <a href="/about#submit">tell this site</a>, which costs nothing and takes a minute.</p></li>
      </ol>
      <h2>Miami-specific practicalities</h2>
      <ul>
        <li><strong>Heat.</strong> A two-hour session in July needs more water and more rest than the same session in January. Book early morning or evening for anything outdoors.</li>
        <li><strong>Rain.</strong> Afternoon thunderstorms between June and September will cancel an outdoor jam roughly on schedule. Indoor rooms do not have this problem, which is why most jams are indoors.</li>
        <li><strong>Floor.</strong> Sand and grass are forgiving for falls and bad for rolling. Beach jams work best for low, slow, weight-sharing practice rather than lifts.</li>
        <li><strong>Parking and distance.</strong> Miami-Dade is wide and car-dependent. Say where the parking is when you advertise a session, and expect people to drive forty minutes for a jam worth attending.</li>
        <li><strong>Two languages.</strong> List sessions in English and Spanish. It is a five-minute job and it doubles who can find you.</li>
        <li><strong>Seasons.</strong> Dancers, teachers and studios travel. Expect a real drop-off in attendance during the summer and around Art Basel in December.</li>
      </ul>
      <h2>Questions about CI in Miami</h2>
      {faq_html}
    </div>
    {band("Know something this page does not?", "If you teach, host, organise or simply dance in South Florida, tell us and it goes on the map. Corrections are as welcome as additions, including removing something that has stopped.", [("Submit a listing", "/about#submit", "primary"), ("The directory", "/directory", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Contact Improvisation in Miami</em>. miamicontactimprov.com. https://miamicontactimprov.com/miami")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/miami",
            "Contact Improvisation in Miami",
            "The Miami Contact Improvisation scene: where practice happens, how the scene is organised, Miami-specific practicalities, and how to start a jam here.",
            about={"@id": schema.SITE + "/#place"},
        ),
        schema.breadcrumb("/miami", "Miami"),
        schema.faq(MIAMI_FAQ),
        {
            "@type": "Place",
            "@id": schema.SITE + "/miami#place",
            "name": "Miami, Florida, United States",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Miami",
                "addressRegion": "FL",
                "addressCountry": "US",
            },
            "geo": {"@type": "GeoCoordinates", "latitude": 25.7617, "longitude": -80.1918},
            "containedInPlace": {"@type": "AdministrativeArea", "name": "Miami-Dade County, Florida"},
        },
    )
    return page(
        "Contact Improvisation in Miami | Jams, Classes & How to Start",
        "Contact improvisation in Miami: the honest state of the scene, where practice happens across Miami-Dade and Broward, and how to start a jam here.",
        "/miami",
        body,
        jsonld=jsonld,
    )


GLOBAL_RESOURCES = [
    ("Contact Improvisation World Resource", "https://www.contactimprov.com/",
     "The international hub for the form, run since the 1990s: a world jam map, an event calendar, a teacher directory, member listings and a links index."),
    ("CI World Jam Map: Florida", "https://www.contactimprov.com/florida.html",
     "The community's own Florida listing. It is the closest thing to a South Florida jam directory that exists, and it is maintained by whoever sends corrections."),
    ("CI Global Calendar", "https://ciglobalcalendar.net/en",
     "A shared, multilingual calendar of CI classes, jams, workshops and festivals worldwide, posted by the organisers and teachers themselves. The best single place to look for something happening anywhere."),
    ("Contact Quarterly", "https://www.contactquarterly.com/",
     "The journal that grew out of the 1975 newsletter, and the form's main written archive for four and a half decades."),
    ("CQ CI Contacts List", "https://contactquarterly.com/contact-improvisation/contacts",
     "Contact Quarterly's referral directory for locating CI classes, jams and practitioners, organised by country and US state."),
    ("Earthdance", "https://earthdance.net/",
     "A long-running movement and improvisation centre in Plainfield, Massachusetts, hosting workshops, residencies and jams."),
    ("Touch&Play Global", "https://touchandplay.org/",
     "Retreats, workshops and relational learning built around contact and consent practice."),
    ("Contact Improvisation Dance Canada", "https://www.contactimprov.ca/",
     "A national CI resource and listing site, useful as a model for how a country's jams get organised and published."),
    ("Contact improvisation (encyclopaedia entry)", "https://en.wikipedia.org/wiki/Contact_improvisation",
     "A starting point for the form's definitions, lineage and influences, with references."),
]

MUSIC_NOTE = (
    "Live music and dance share a history in this form, and some jams run with a musician "
    "in the room rather than a recording. If you play, and you would rather play for dancers "
    "than for an audience, say so in a jam circle."
)

DIRECTORY_FAQ = [
    ("Who teaches contact improvisation in Miami?",
     "Contact improvisation has no certification body, so there is no register to consult. What could be verified when this page was last checked is one recurring all-levels class: Contact Improv \u2014 ALL LEVELS at Dance Arts Miami, Tuesdays 6:00 to 7:00 PM. Everything else runs through organisations that answer a direct message, which are listed above."),
    ("How do I get listed here?",
     "Send the name, the city, what you teach or host, and a link to your own page. There is no fee and no membership. Listings are checked against your own published information before they go up, and each entry shows the date it was checked."),
    ("Do you list jams outside Miami?",
     "The focus is Miami-Dade and Broward. Sessions elsewhere in Florida are linked through the CI World Jam Map, which covers the whole state and the world."),
    ("Why are 5Rhythms and ecstatic dance on a contact improvisation site?",
     "Because they are the adjacent practices a newcomer to this kind of movement will actually meet in Miami, and because every entry is labelled with what it is. A directory that silently mixed them together would be worse than one that says so."),
]


def directory():
    resources = "".join(
        f'<li><a href="{u}" rel="noopener nofollow">{n}</a><p>{d}</p></li>'
        for n, u, d in GLOBAL_RESOURCES
    )
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in DIRECTORY_FAQ)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Directory</p>
    <h1>Who to ask, and where the map continues.</h1>
    <p class="lede">Local organisers and studios first, then the international resources that carry the form's listings, archives and festivals.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("Contact Improvisation has no central directory because it has no central body. Local listings are held by the organisers themselves. The closest thing to a global index is the CI World Jam Map at contactimprov.com, which lists sessions by country and state, including a Florida page covering Miami, Sarasota, Gainesville and Jacksonville.")}
    <div class="prose">
      <h2>International resources</h2>
      <p>These are the sites that actually hold the form's listings, archives and gatherings. Each one was opened and checked when it was added here.</p>
      <ul class="dir-list">{resources}</ul>
    </div>
    {listings.teachers_note()}
    {listings.orgs_block()}
    {listings.adjacent_block()}
    <div class="prose">
      <h2>Questions about the directory</h2>
      {faq_html}
    </div>
    {band("Add yourself", "No fee, no membership, no committee. If you teach, host or organise in South Florida, this page exists to point at you.", [("Submit a listing", "/about#submit", "primary"), ("The Miami scene", "/miami", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Contact Improvisation directory</em>. miamicontactimprov.com. https://miamicontactimprov.com/directory")}
  </div>
</section>
"""
    items = [(n, u, d) for n, u, d in GLOBAL_RESOURCES]
    local = [(o[0], o[3], o[5][:160]) for o in listings.ORGS]
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/directory",
            "Contact Improvisation directory: Miami and beyond",
            "Miami contact improvisation teachers, organisers and studios, plus the international resources that hold the form's listings and archives.",
        ),
        schema.breadcrumb("/directory", "Directory"),
        schema.faq(DIRECTORY_FAQ),
        schema.item_list("/directory#international", "Contact Improvisation international resources", items),
        schema.item_list("/directory#miami", "Miami movement organisations", local),
    )
    return page(
        "Contact Improvisation Directory | Miami Teachers & Studios",
        "Contact improvisation directory: Miami teachers, organisers and studios, plus the international resources that hold the form's jam listings, archives and festivals.",
        "/directory",
        body,
        jsonld=jsonld,
    )


def faq():
    from content_core import WHATIS_FAQ, HISTORY_FAQ
    from content_practice import FIRST_JAM_FAQ, JAMS_FAQ, SAFETY_FAQ

    groups = [
        ("About the practice", WHATIS_FAQ),
        ("Starting out", FIRST_JAM_FAQ),
        ("Jams and sessions", JAMS_FAQ),
        ("Safety and consent", SAFETY_FAQ),
        ("History and origins", HISTORY_FAQ),
        ("Miami", MIAMI_FAQ),
        ("This directory and site", DIRECTORY_FAQ),
    ]
    blocks = []
    all_entries = []
    for title, entries in groups:
        qs = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in entries)
        blocks.append(f"<h2>{title}</h2>{qs}")
        all_entries.extend(entries)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Questions</p>
    <h1>Everything people ask about this dance.</h1>
    <p class="lede">Answered in the first sentence, in plain language, without the mystique.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      {''.join(blocks)}
    </div>
    {band("Still unanswered?", "If a question is missing here it is probably missing from the site. Send it.", [("Ask us", "/about#submit", "primary"), ("Start with the basics", "/what-is-contact-improvisation", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Frequently asked questions</em>. miamicontactimprov.com. https://miamicontactimprov.com/faq")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/faq",
            "Contact Improvisation FAQ",
            "Answers to the questions people actually ask about Contact Improvisation: what it is, what happens at a jam, safety, consent, history and how it works in Miami.",
        ),
        schema.breadcrumb("/faq", "FAQ"),
        schema.faq(all_entries),
    )
    return page(
        "Contact Improvisation FAQ | Jams, Safety, Consent & Miami",
        "Straight answers about Contact Improvisation: what it is, what happens at a jam, consent and safety, why there is no certification, and how the Miami scene works.",
        "/faq",
        body,
        jsonld=jsonld,
    )


def about():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>What this site is, and what it is not.</h1>
    <p class="lede">An independent, non-commercial reference for Contact Improvisation in Miami. No membership, no commission, no studio behind it, no organiser to promote.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("miamicontactimprov.com is an independent community resource that maps Contact Improvisation practice across Miami-Dade and Broward County. It publishes what can be verified, states plainly what cannot, and accepts corrections from anyone in the scene. It does not run sessions, take bookings, or charge for listings.")}
    <div class="prose">
      <h2>Why it exists</h2>
      <p>Contact Improvisation has no federation, no licence and no central organisation. That openness is the reason it spread to every continent, and it is also the reason a city like Miami can have a decades-long intermittent practice without anything online to show for it. When the form has no institution, the map has to be built by hand.</p>
      <p>The global CI World Jam Map at contactimprov.com has done that at world scale since the 1990s. This site does it at one-city scale, with more detail than a global listing can carry, and it links back to the world map rather than competing with it.</p>
      <h2>How listings work here</h2>
      <ul>
        <li>Everything published is checked against the organiser's own published information first.</li>
        <li>If a session cannot be verified, it is listed as unverified or left off, never guessed.</li>
        <li>Nothing is paid. There is no sponsored listing and no affiliate arrangement.</li>
        <li>Removals are normal. Sessions end, studios close, organisers move on, and the page is corrected.</li>
        <li>Accuracy matters more than completeness. A short honest page beats a long wrong one.</li>
      </ul>
      <h2 id="submit">Submit, correct, or remove a listing</h2>
      <p>Email <a href="mailto:hello@miamicontactimprov.com">hello@miamicontactimprov.com</a>, or reply to any account this site publishes from. English or Spanish, either is fine.</p>
      <p>What to send for a jam or a class:</p>
      {facts([
        ("Name", "What the session is called"),
        ("Where", "Studio or venue name, and the city"),
        ("When", "Day, time and how often"),
        ("Cost", "Door fee, donation, or free"),
        ("Who it is for", "Open to everyone, or prior experience assumed"),
        ("Link", "Your own page, calendar entry or social account"),
      ])}
      <p>What to send for a teacher listing: your name, your city, what you teach, and a link to your own page. If you would rather not be listed anywhere, say so and we will remove you without asking why.</p>
      <p>If you own a film embedded in the <a href="/videos">video room</a> and would prefer it not to be, one line is enough. It comes down the same day.</p>
      <h2>Corrections</h2>
      <p>If something here is wrong, it is more useful to tell us than to ignore it. Corrections that remove a claim are as welcome as ones that add a session, and the page is changed rather than annotated.</p>
      <h2>What this site is not</h2>
      <ul>
        <li>It is not a studio, a booking service or a school.</li>
        <li>It does not vet, certify or endorse teachers. Nobody can, in this form.</li>
        <li>It is not affiliated with contactimprov.com, Contact Quarterly or any festival.</li>
        <li>It does not mediate disputes between dancers or organisers.</li>
      </ul>
    </div>
    {band("The page is only as good as the room", "If you know where the dancing is this month, that is the single most useful thing you can send.", [("Email us", "mailto:hello@miamicontactimprov.com", "primary"), ("Read the Miami page", "/miami", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>About</em>. miamicontactimprov.com. https://miamicontactimprov.com/about")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/about",
            "About Miami Contact Improv",
            "What miamicontactimprov.com is: an independent community resource mapping Contact Improvisation across Miami-Dade and Broward. How to submit, correct or remove a listing.",
        ),
        schema.breadcrumb("/about", "About"),
    )
    return page(
        "About Miami Contact Improv | Submit a Listing",
        "An independent, non-commercial map of Contact Improvisation in Miami. How listings are verified, and how to submit, correct or remove one.",
        "/about",
        body,
        jsonld=jsonld,
    )


def not_found():
    body = """
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1>That page is not here.</h1>
    <p class="lede">Either it moved, or it never existed, or a link to it is wrong. The pages below cover most of what people come here for.</p>
    <div class="btn-row">
      <a class="btn primary" href="/">Home</a>
      <a class="btn secondary" href="/miami">Contact Improvisation in Miami</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Try one of these</h2>
    <div class="grid">
      <a class="card" href="/what-is-contact-improvisation"><span class="tag">Start</span><h3>What is Contact Improvisation?</h3><p>The definition, the principles and what a jam actually is.</p></a>
      <a class="card" href="/jams"><span class="tag">Practice</span><h3>Jams</h3><p>How a jam runs, what to bring, and where to ask.</p></a>
      <a class="card" href="/classes"><span class="tag">Learning</span><h3>Classes</h3><p>Beginners' sessions and a first-jam walkthrough.</p></a>
      <a class="card" href="/videos"><span class="tag">Watch</span><h3>Video room</h3><p>What the form looks like when it is working.</p></a>
      <a class="card" href="/directory"><span class="tag">People</span><h3>Directory</h3><p>Teachers, organisers, studios and the global map.</p></a>
      <a class="card" href="/glossary"><span class="tag">Words</span><h3>Glossary</h3><p>Jam, score, small dance, underscore and the rest.</p></a>
    </div>
  </div>
</section>
"""
    return page(
        "Page not found | Miami Contact Improv",
        "That page is not here. Find Contact Improvisation jams, classes, teachers and video for Miami instead.",
        "/404",
        body,
        jsonld=schema.render(schema.organisation()),
    )
