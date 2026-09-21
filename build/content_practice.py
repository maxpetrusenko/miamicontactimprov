"""Practice pages: jams, classes, safety and consent, video room."""

from shell import LAST_CHECKED, LAST_CHECKED_ISO, answer, band, cards, cite_block, facts, page
import schema
import listings
import videos_data

FIRST_JAM_FAQ = [
    ("What do I wear to a Contact Improvisation jam?",
     "Loose clothing that covers your back, shoulders and knees, since those are the usual contact points. Avoid zips, buckles, hard seams and anything with a rough texture. Bare feet or soft non-slip socks. Bring water."),
    ("Do I have to dance with anyone?",
     "No. Sitting at the edge is a normal part of a jam, and dancing solo is part of the form. You may decline any invitation, at any point, without giving a reason, and you may end a dance mid-movement."),
    ("Do I have to talk to people?",
     "Not much. Jams often open with a short circle where the organiser states the protocol and anyone can add a boundary or a note. After that, most of the communication is physical."),
    ("How long is a jam?",
     "Typically two to three hours, often with a warm-up or a short class first. People arrive and leave throughout. Arriving after the opening circle is usually fine; leaving early always is."),
    ("Is it expensive?",
     "Costs are set by whoever runs the session. Community jams are commonly free, donation-based, or a small door fee that covers the room hire. Rates for classes and workshops vary by teacher and are set individually."),
    ("What if I am not fit or flexible?",
     "Neither is required to begin. The form is built on structure and gravity rather than strength or range, and beginners' sessions start from standing and rolling, not from lifts."),
    ("Can I bring my child?",
     "Ask the organiser. Some jams run family or all-ages sessions; most open jams are adult spaces. There is no fixed rule, so the listing or the organiser is the authority."),
    ("I have a back or joint condition. Can I still come?",
     "Many people with injuries and chronic conditions practise CI, sometimes with adaptations agreed with their partners. Talk to the organiser before your first session and to your partner before each dance. This site is not medical advice."),
]

JAMS_FAQ = [
    ("What is a Contact Improvisation jam?",
     "A jam is an open, unguided Contact Improvisation session. There is no teacher and little or no music. People arrive, dance with one or more partners or alone, rest at the edge, and leave when they are done. It is the basic social form of Contact Improvisation."),
    ("What is the difference between an open jam and a closed jam?",
     "An open jam accepts anyone, including first-timers. A closed, experienced or advanced jam assumes prior practice, usually because the dancing moves fast and relies on shared safety habits. Listings should state which one it is."),
    ("How do I find a jam in Miami?",
     "Miami's CI scene is organised by individuals rather than an institution, so sessions appear through studio calendars, social posts and word of mouth rather than one central box office. This page lists the sessions we have confirmed, and the directory lists the studios and organisers worth asking."),
    ("Is there a jam tonight in Miami?",
     "This site does not publish a live calendar, so it cannot answer that reliably. The most current source is the organiser's own listing or social account. If you run a recurring session and tell us the schedule, we will add it."),
    ("Do jams cost money?",
     "Usually a small door fee or a donation to cover the room, set by the organiser. Free community jams exist. Nobody should be turned away from a first jam without being told the cost in advance."),
]


def jams():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in JAMS_FAQ)
    sessions = listings.sessions_block() or listings.sessions_or_none()
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Open practice</p>
    <h1>Jams: the room is the teacher.</h1>
    <p class="lede">A jam is where Contact Improvisation actually lives. No instructor, no set music, no obligation to dance with anyone. You arrive, you listen, you move, you leave.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("A Contact Improvisation (CI) jam is an open, unguided session where people practise Contact Improvisation together. There is no teacher and usually no music. Participants arrive and leave freely, dance with whoever is willing, sit at the edge to rest and watch, and stop at any time. Jams are the primary way the form is practised worldwide, and in Miami they sit alongside a small number of recurring classes and festival camps.")}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sessions}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>How to check a listing is still current</h2>
    <div class="prose">
      <p>Miami has no central CI calendar, so "is there a jam tonight?" has no static answer and a page like this one goes stale the moment a room or a schedule changes. Every session above carries the date its source was last opened and read; the third-party listings were last re-checked on <strong>{LAST_CHECKED}</strong>. Treat an old date as a lead to check rather than a fact.</p>
      <p>Three things settle it. Open the organiser's own page or account, which is the only authoritative source and is linked from each entry. Look for a date of its own: a recurring session whose source has not been posted to in months has usually stopped, and an undated listing is evidence of nothing. Then ask, by direct message, before travelling to a session — organisers answer, and they would rather tell you than have you arrive at a locked door.</p>
      <p>What this page will not do is guess. A stale listing published as current is worse than an empty one, so an entry comes down when its source goes quiet, and a session nobody could verify is never presented as running.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>How a jam usually runs</h2>
    <div class="prose">
      <p>Formats vary, but most jams follow a recognisable shape.</p>
      <p><strong>Arrival.</strong> People change, stretch, greet each other, and find a place on the floor. Someone who is hosting opens a circle.</p>
      <p><strong>The circle.</strong> Two or three minutes. The host states the protocol: consent is continuous, you may decline anything, the edge is for resting, and here is where the water is. Anyone may add a boundary or announce something, such as an injury or that they are leaving early.</p>
      <p><strong>Warm-up.</strong> Often a short guided sequence, then a few minutes of <strong>small dance</strong>: standing still and following the body's micro-adjustments. If there is a teacher present, they may offer twenty minutes of material before the open dancing begins.</p>
      <p><strong>The open jam.</strong> The long middle. Dances start with a look, a hand, or simply the two of you already moving. They end when either partner stops. Resting at the edge between dances is normal.</p>
      <p><strong>Closing.</strong> Some jams end with a circle, a moment of stillness, or nothing at all. People drift out.</p>
      <h2>What is expected of you</h2>
      <ul>
        <li>Keep the contact point singular. Two hands and a hip at once is grappling, not CI.</li>
        <li>Keep your own feet available. If you cannot land, you cannot safely take weight.</li>
        <li>Roll out of falls rather than bracing. The floor is the biggest partner in the room.</li>
        <li>Say no when you mean no, and accept no without asking why.</li>
        <li>Leave the dance when it is over, including mid-phrase, without apologising.</li>
        <li>Do not teach unless you were asked to. A jam is not a class.</li>
      </ul>
      <h2>What to bring</h2>
      {facts([
        ("Clothing", "Loose, opaque, covers back, shoulders and knees. No zips, buckles or rough seams"),
        ("Feet", "Bare or soft non-slip socks. No shoes on the floor"),
        ("Water", "A full bottle. The floor is hot and humid in Miami"),
        ("Towel", "One. You will need it"),
        ("Jewellery", "Leave it off. Rings, watches and necklaces catch and cut"),
        ("Phone", "Silenced, face down, off the floor or at the edge"),
      ])}
      <h2>Spotters and safety</h2>
      <p>Sessions where lifts are circulating often keep one or two people outside the dance as <strong>spotters</strong>: standing close, hands free, watching for a fall that needs slowing. It is one of the few roles in a jam that is technical rather than social, and new dancers are usually welcome to learn it. If you are not sure whether you can safely take someone's weight, you cannot, and saying so is the correct answer.</p>
      <h2>Before and after your first visit</h2>
      <p>What actually happens when you walk in &mdash; arriving, the opening circle, the first ten minutes of dancing, the lines you can say when you want to stop and when to leave &mdash; is on <a href="/your-first-jam">your first jam, step by step</a>. What to do in the weeks after it, including the weeks when nothing is running, is on <a href="/keep-practising">keep practising</a>.</p>
      <h2>Questions about jams</h2>
      {faq_html}
    </div>
    {band("Run a jam?", "Tell us the schedule, the room and the door fee and we will list it. This page exists to be corrected by the people who are actually in the room.", [("Submit a jam", "/about#submit", "primary"), ("Find a class", "/classes", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Contact improv jams in Miami</em>. miamicontactimprov.com. https://miamicontactimprov.com/jams")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/jams",
            "Contact improv jams in Miami",
            "What a Contact Improvisation jam is, how a session usually runs, what to bring, and how to check a listing is still current, with the confirmed jams and open practice sessions in Miami and South Florida.",
            date_modified=LAST_CHECKED_ISO,
        ),
        schema.breadcrumb("/jams", "Jams"),
        schema.faq(JAMS_FAQ),
        listings.events_schema(),
    )
    return page(
        "Contact Improv Jams in Miami [Step-by-Step] | What to Expect",
        "What a Contact Improvisation jam is, how a session runs, how to check a listing is still current, and where to dance in Miami. What to bring, and when to leave.",
        "/jams",
        body,
        jsonld=jsonld,
    )


def classes():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FIRST_JAM_FAQ)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Learning</p>
    <h1>Classes, workshops and your first jam.</h1>
    <p class="lede">You can start Contact Improvisation with no dance background at all. A beginners' session gets you falling safely in an afternoon, and the rest is time in the room.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("A Contact Improvisation (CI) class teaches the underlying skills: how to share weight without collapsing, how to roll out of a fall, how to read your partner's momentum, and how to say no. Beginner sessions assume no dance training. Most people attend classes for a few weeks and then add a weekly jam, because the form is learned mostly by dancing rather than by instruction.")}
    <div class="prose">
      <h2 id="first-jam">Your first jam, step by step</h2>
      <p><strong>Before.</strong> Message the organiser and say you are new. Ask three things: is it open to beginners, what is the door fee, and is there a warm-up before the open dancing. All three answers should be easy.</p>
      <p><strong>Arriving.</strong> Get there for the start if you can, because the opening circle is where the rules are set. Change, leave your bag at the edge, fill your bottle.</p>
      <p><strong>The warm-up.</strong> Stand still and listen to the small adjustments your body makes to stay upright. This is not a warm-up for the real thing; it is the real thing at low amplitude.</p>
      <p><strong>Your first dance.</strong> Look at someone. If they look back, you are dancing. Start with a hand, a shoulder, or simply standing nearby. Keep one point of contact. Let one of you slowly give weight and see what the floor does.</p>
      <p><strong>Ending.</strong> Stop when you want to. Step back, nod, walk to the edge. No explanation needed and none expected, in either direction.</p>
      <p><strong>After.</strong> You will probably be tired in a way that is not athletic tired. Drink water. <a href="/keep-practising">Come back</a> &mdash; and see what happens after the first visit.</p>
      <h2>What teachers actually teach</h2>
      <p>A good beginner series covers the same handful of things, whatever the teacher's style.</p>
      {facts([
        ("Weight", "Giving and receiving weight through the skeleton, not by gripping"),
        ("Falling", "Rolling exits, tucking, landing on the floor without hands"),
        ("Contact", "Maintaining a single sliding point of contact and following it"),
        ("Listening", "Reading pressure and momentum instead of watching"),
        ("Boundaries", "Declining, pausing, leaving, and re-negotiating mid-dance"),
        ("Lifts", "How support structures work, and when not to attempt one"),
      ])}
      <h2>How to judge a teacher</h2>
      <div class="prose">
        <p>There is no certification body for Contact Improvisation, so you cannot check a licence. What you can check is behaviour. A teacher should state their consent framework in the first ten minutes rather than assuming it. They should demonstrate as much as they talk. They should correct unsafe technique immediately, including in the room rather than in a private aside afterwards. They should not require you to partner with a particular person, and they should be comfortable when you decline one.</p>
        <p>A scene with no certification is a scene where reputation is the entire quality control. That is worth knowing before you pay for an intensive.</p>
      </div>
      <h2>Where to learn it in Miami</h2>
      <div class="prose">
        <p>One recurring Contact Improvisation class in Miami-Dade could be verified from its own listings when this page was last checked: <strong>Contact Improv &mdash; ALL LEVELS</strong> at Dance Arts Miami, 250 NE 61st Street, Miami, 33137, on Tuesdays from 6:00 to 7:00 PM. It is advertised as covering connection, weight sharing, momentum and spontaneous partnering, and no partner is needed. Because it is published as a multi-date series on Eventbrite and mirrored on Meetup, confirm the current week there rather than trusting this page.</p>
        <p>Beyond that class, the realistic routes into the form in Miami are the <a href="/jams">jams, camps and adjacent practice</a> listed elsewhere on this site. If you would rather learn in a structured way and no class is running near you, a contemporary dance or improvisation class at any Miami studio will teach you most of the body literacy, and the jams will teach you the rest.</p>
      </div>
      <h2>After the first one</h2>
      <p>What to do in the weeks after your first session, including the weeks when nothing is running, is on the <a href="/keep-practising">keep-practising page</a>. A fuller walkthrough of the evening itself &mdash; arriving, the opening circle, the first ten minutes of dancing, and the lines you can say when you want to stop &mdash; is on <a href="/your-first-jam">your first jam, step by step</a>.</p>
      <h2>Questions people ask before their first session</h2>
      {faq_html}
    </div>
    {band("Find something this week", "Start with a jam, or a beginners' class if you would rather be taught first. Both are legitimate entry points.", [("Jams", "/jams", "primary"), ("Teachers and studios", "/directory", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Contact Improvisation classes and first jams</em>. miamicontactimprov.com. https://miamicontactimprov.com/classes")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/classes",
            "Contact Improvisation classes and your first jam",
            "How to start Contact Improvisation in Miami: what a beginners' class covers, what happens at your first jam, how to judge a teacher, and what to bring.",
        ),
        schema.breadcrumb("/classes", "Classes"),
        schema.faq(FIRST_JAM_FAQ),
        listings.course_schema(),
        schema.item_list(
            "/classes",
            "Skills taught in a Contact Improvisation beginners' course",
            [
                ("Weight sharing", "/classes#first-jam", "Giving and receiving weight through the skeleton"),
                ("Falling and rolling", "/classes#first-jam", "Safe exits from a fall or a broken lift"),
                ("Contact point", "/classes#first-jam", "Maintaining a single sliding point of contact"),
                ("Boundaries and consent", "/safety-and-consent", "Declining, pausing and renegotiating"),
                ("Lifts", "/classes#first-jam", "Support structures and when not to use them"),
            ],
        ),
    )
    return page(
        "Contact Improvisation Classes Miami [Updated for 2026]",
        "How to start Contact Improvisation in Miami: what a beginners' class teaches, a step-by-step first jam walkthrough, how to judge a teacher, and what to bring.",
        "/classes",
        body,
        jsonld=jsonld,
    )


SAFETY_FAQ = [
    ("Is contact improvisation safe?",
     "Contact Improvisation carries the normal risks of a partnered physical practice: falls, collisions, strained joints and the occasional bruise. The form manages these deliberately, through rolling exits rather than bracing, keeping your own feet available, keeping a single contact point, warming up, and having spotters near lifts. Serious injury is uncommon but not impossible, particularly in fast experienced jams."),
    ("Do I have to accept every dance I am offered?",
     "No, and nobody should make you feel otherwise. Declining is part of the form. You can also end a dance mid-movement, slow it down, ask for less weight, or leave the floor entirely."),
    ("What is spotting?",
     "Spotting means standing close to a dancing pair with your hands free, ready to slow a fall if one happens. One or two spotters near a crowded or lifting area is standard practice in many jams."),
    ("What is not contact improvisation?",
     "Contact Improvisation is not a sexual practice, a dating venue, a massage service, an acrobatics display, or a space for uninvited instruction. Touching, holding or moving a partner in ways they have not agreed to is not part of this form, and jams address it directly."),
    ("What do I do if something goes wrong in a jam?",
     "Speak to the organiser during or after the session. Most jams name a person who holds the room and is responsible for intervening. If an organiser will not act on a boundary violation, that is information about whether to return."),
    ("Is there a code of conduct for Contact Improvisation?",
     "There is no global one, because there is no global body. Individual scenes and jams write their own. The shared expectations are: continuous consent, the right to decline anything, respect for the edge, no teaching uninvited, and no recording without asking."),
]


def safety():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in SAFETY_FAQ)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Boundaries</p>
    <h1>Safety and consent are the technique.</h1>
    <p class="lede">Contact Improvisation puts people in close physical contact and asks them to move under each other's weight. That only works if refusing is as trained as lifting.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("In Contact Improvisation (CI), consent is continuous rather than given once. Any dancer may decline an invitation, pause, slow down, change what they are doing or leave a dance at any point, without explanation. Jams are unguided and unsupervised, so the person hosting the session is responsible for stating the protocol and acting on violations.")}
    <div class="prose">
      <h2>Your rights in the room</h2>
      <ul>
        <li>To decline any invitation to dance, with no reason given.</li>
        <li>To end a dance at any moment, including mid-movement.</li>
        <li>To ask for less weight, less speed, or a different point of contact.</li>
        <li>To sit at the edge for as long as you like, or all evening.</li>
        <li>To not be touched in ways you have not agreed to.</li>
        <li>To not be photographed or filmed without being asked first.</li>
        <li>To not be taught, corrected or coached unless you asked for it.</li>
        <li>To speak to the organiser and be taken seriously.</li>
      </ul>
      <h2>Physical safety, briefly</h2>
      <p>Most injuries in CI come from three things: bracing against a fall instead of rolling, taking weight you are not structurally placed to take, and dancing tired. The form's own habits address all three. Keep your own feet available to land on. Roll out rather than stop. If you cannot see how a lift resolves, do not begin it. Stop before you are exhausted.</p>
      <p>Warm up before the open dancing, particularly wrists, shoulders and spine. If a session offers a warm-up, use it. If you have an injury or a condition that affects how you can be moved, tell your partner before the dance starts, not during it.</p>
      <h2>What this practice is not</h2>
      <p>It is worth being plain, because Contact Improvisation is adjacent to a lot of things and gets confused for them.</p>
      <ul>
        <li>It is not a sexual practice. Touch is the medium, not a route to anything else.</li>
        <li>It is not a therapy session. It can be restorative; it is not clinical treatment.</li>
        <li>It is not a dating venue or a pickup scene.</li>
        <li>It is not a performance, unless a specific event says so.</li>
        <li>It is not a space where an experienced dancer may direct a less experienced one.</li>
      </ul>
      <p>A person who treats a jam as any of the above is not doing Contact Improvisation badly. They are doing something else, in a room where people did not agree to it.</p>
      <h2>If something happens</h2>
      <p>Tell the organiser. Most jams have one named person holding the room, and intervening on boundary violations is that person's job rather than a favour. If they will not act, that tells you what you need to know about returning. This site lists sessions but does not run them and cannot mediate, though we will remove a listing that has an unresolved, reported pattern of harm.</p>
      <h2>Questions about safety</h2>
      {faq_html}
    </div>
    {band("A jam that takes this seriously", "The sessions worth your time say their protocol out loud at the start of every session. If yours does not, ask why.", [("Find a jam", "/jams", "primary"), ("Your first jam, step by step", "/your-first-jam", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Safety and consent in Contact Improvisation</em>. miamicontactimprov.com. https://miamicontactimprov.com/safety-and-consent")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/safety-and-consent",
            "Safety and consent in Contact Improvisation",
            "What consent means in Contact Improvisation, your rights in a jam, how physical safety works, what the practice is not, and what to do when something goes wrong.",
        ),
        schema.breadcrumb("/safety-and-consent", "Safety and consent"),
        schema.faq(SAFETY_FAQ),
    )
    return page(
        "Contact Improv Safety & Consent [Step-by-Step Guide]",
        "Consent in Contact Improvisation: what you may always decline, how physical safety works, spotting, what the practice is not, and what to do when something goes wrong.",
        "/safety-and-consent",
        body,
        jsonld=jsonld,
    )


def videos():
    count = videos_data.embed_count()
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Video room</p>
    <h1>Our own films are being made. Until then, this room is credit where it is due.</h1>
    <p class="lede">This jam has not shot a video yet, so nothing on this page is ours. Every film below was made by the channel named on it, plays through that channel's own player, and stays that channel's work. What we are shooting for Miami is listed as what it is: in production, with no runtime and no date until a file exists.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer(f"Every film on this page was made by someone else and is credited to them by name: {count} pieces, each embedded from the platform that hosts it. None of them was shot in Miami, and none of them is this site's. The jam's own films are in production, listed here as planned pieces; each one moves to the top of this page as ours only when the finished file is hosted here.")}
    {videos_data.owned_room()}
    {videos_data.in_production()}
    {videos_data.reference_section()}
    {videos_data.credits()}
    {band("Watched enough", "Nothing on this page will teach you what two minutes on a floor with another person will.", [("Jams in Miami", "/jams", "primary"), ("First jam walkthrough", "/classes#first-jam", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Contact Improvisation video room</em>. miamicontactimprov.com. https://miamicontactimprov.com/videos")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/videos",
            "Contact Improvisation video room",
            "Contact Improvisation on film: every channel credited by name, plus the films this jam is shooting in Miami.",
        ),
        schema.breadcrumb("/videos", "Videos"),
        videos_data.schema_list(),
    )
    return page(
        "Contact Improvisation Videos | Free Films & Documentary",
        "Contact Improvisation on film: the channels that made it, credited by name, plus the Miami films this jam is shooting. None of it is ours yet.",
        "/videos",
        body,
        jsonld=jsonld,
    )


# --------------------------------------------------------------- stage pages
# /your-first-jam owns the first-visit stage (what actually happens when you walk
# in); /keep-practising owns the after stage (how the practice continues).
# Neither page carries Event schema. A recurring, organiser-set session modelled
# as an Event would publish a date this site cannot keep true, which is the rule
# that keeps the listings honest. Session entries carry the modality the
# organiser states and the date the source was checked, and rank nothing.

SESSIONS_RANK_NOTE = (
    "The modality in each entry above is the one the organiser states about their own session, "
    "and every entry carries the date its source was last opened and read; the third-party "
    f"listings were last re-checked on <strong>{LAST_CHECKED}</strong>. This page ranks nothing. The entries appear in the order "
    "they were verified, none of them is paid for, and this site recommends none of them over "
    "another."
)


def your_first_jam():
    sessions = listings.sessions_block() or listings.sessions_or_none()
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">The first time</p>
    <h1>Your first contact improv jam, step by step.</h1>
    <p class="lede">Nobody at a jam is assessing you. You arrive, someone states the rules, dancing starts and stops around you, and you take part as much or as little as you want.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("You arrive, you warm up, and there is usually a short circle where the people holding the room state the consent protocol. Then dancing starts and stops around you. You are not required to dance with anyone. Sitting at the edge for the whole session is a normal part of a jam, and leaving early is always fine. There is no teacher.")}
    <div class="prose">
      <h2>Arriving</h2>
      <p>Getting there before the opening circle makes the evening easier, because that is where the room's rules are stated and where a newcomer is easiest to include. Arriving after it is usually fine: walk in, find a place at the edge, and join when you are ready. Nobody is keeping a register.</p>
      <p>Change into what you will dance in, leave your bag against the wall, fill your bottle, and spend a few minutes on the floor before anything starts. Organisers expect people to arrive not knowing anybody. That is the ordinary case rather than the awkward one.</p>
      <h2>The opening circle</h2>
      <p>Most jams begin with two or three minutes of standing or sitting in a circle. Whoever holds the room states the protocol: consent is continuous, anyone may decline anything without giving a reason, the edge is for resting, nobody teaches unless they were asked to, and nobody is filmed without agreeing to it. Anyone in the circle may add a boundary or a note.</p>
      <p>The sessions worth your time state their protocol out loud at the start of every session. A jam with no circle and no stated protocol is telling you something about the room.</p>
      <h2>Your first ten minutes of dancing</h2>
      <p>A warm-up usually comes first: standing still and following the small adjustments your body makes to stay upright. That is the practice at low volume rather than a formality before the real thing.</p>
      <p>Then dancing starts around you, often without any signal at all. A dance begins with a look, an offered hand, or two people already moving near each other. Watching from the edge for twenty minutes is a normal way to begin, and so is beginning immediately. Most of what an experienced dancer does in the first minutes is listen rather than move. Beginning is not a performance.</p>
      <h2>What is expected of you</h2>
      <ul>
        <li>Keep the contact point singular. Two hands and a hip at once is grappling, not CI.</li>
        <li>Keep your own feet available. If you cannot land, you cannot safely take weight.</li>
        <li>Roll out of falls rather than bracing. The floor is the biggest partner in the room.</li>
        <li>Say no when you mean no, and accept no without asking why.</li>
        <li>Leave the dance when it is over, including mid-phrase, without apologising.</li>
        <li>Do not teach unless you were asked to. A jam is not a class.</li>
      </ul>
      <h2>What to bring</h2>
      {facts([
        ("Clothing", "Loose, opaque, covers back, shoulders and knees. No zips, buckles or rough seams"),
        ("Feet", "Bare or soft non-slip socks. No shoes on the floor"),
        ("Water", "A full bottle. The floor is hot and humid in Miami"),
        ("Towel", "One. You will need it"),
        ("Jewellery", "Leave it off. Rings, watches and necklaces catch and cut"),
        ("Phone", "Silenced, face down, off the floor or at the edge"),
      ])}
      <h2>What you can say</h2>
      <p>These lines are complete on their own, and none of them needs a reason attached to it. Declining is a trained skill in this form rather than a social cost.</p>
      <blockquote>
        <p>"Not right now."</p>
        <p>"Can we go slower?"</p>
        <p>"I'm going to stop here."</p>
        <p>"I'd rather sit this one out."</p>
      </blockquote>
      <p>A partner who asks why you said no is answering a question about themselves, and you are free to walk to the edge without replying.</p>
      <h2>When to leave</h2>
      <p>A dance ends when either partner says so, including mid-phrase and including a lift that is still being set up. The session ends for you whenever you decide: people leave after twenty minutes and people stay for three hours, and both are ordinary. Say goodbye to whoever you were dancing with, or do not.</p>
      <h2>If something goes wrong</h2>
      <p>Speak to the organiser during or after the session. Most jams name one person who holds the room, and acting on a boundary violation is that person's job rather than a favour. An organiser who will not act tells you what you need to know about returning. Your rights in the room and the physical-safety habits are set out on <a href="/safety-and-consent">safety and consent</a>.</p>
    </div>
    {sessions}
    <div class="prose">
      <p>{SESSIONS_RANK_NOTE}</p>
      <h2>Practical questions</h2>
      <p>Cost, coming on your own, fitness, watching instead of dancing and the beginner path are answered one line each on the <a href="/faq">question page</a>. How a whole session usually runs is on <a href="/jams">jams</a>, and what a beginner class actually teaches is on <a href="/classes">classes</a>. If you have never read anything about the form, start with <a href="/what-is-contact-improvisation">what Contact Improvisation is</a>.</p>
    </div>
    {band("Ready to go?", "Every session above links to the organiser's own page, which is the only source that knows this week's schedule.", [("Jams in Miami", "/jams", "primary"), ("Classes and workshops", "/classes", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Your first contact improv jam, step by step</em>. miamicontactimprov.com. https://miamicontactimprov.com/your-first-jam")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/your-first-jam",
            "Your first contact improv jam, step by step",
            "What actually happens at a first Contact Improvisation jam in Miami: arriving, the opening circle, the first ten minutes of dancing, what you can say, what to bring, and when to leave.",
            date_modified=LAST_CHECKED_ISO,
        ),
        schema.breadcrumb("/your-first-jam", "Your first jam"),
    )
    return page(
        "Your First Contact Improv Jam [Step-by-Step] | Walkthrough",
        "What happens at a first Contact Improvisation jam: arriving, the opening circle, the first ten minutes, the lines you can say, what to bring, and when to leave.",
        "/your-first-jam",
        body,
        jsonld=jsonld,
    )


def keep_practising():
    sessions = listings.sessions_block() or listings.sessions_or_none()
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">After the first time</p>
    <h1>How to keep practising contact improvisation in Miami.</h1>
    <p class="lede">The part that follows your first visit: what to do between jams, why the second one feels different, and what to do in the weeks when nothing is running.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("You keep practising by going back. Contact Improvisation is learned in the room rather than between sessions, so the honest answer is a weekly jam or class, plus a little solo practice for the weeks when nothing is running. This page covers the part after your first visit, including the weeks when the answer is 'nothing is on'.")}
    <div class="prose">
      <h2>Practising on your own</h2>
      <p>The <a href="/glossary#small-dance">small dance</a> is the home version of the whole form: stand still, eyes soft, and follow the micro-adjustments your body makes to stay upright. Two minutes is enough to start.</p>
      <p>From there, floor work and falling practice. Rolling along the floor without pushing yourself with your hands, and learning to meet the ground by rolling rather than catching yourself. It is unglamorous, and it is where most of the safety in a jam actually comes from. <a href="/safety-and-consent">Safety and consent</a> covers the mechanics in more detail.</p>
      <h2>Practising with a partner</h2>
      <p>The form is practised by two people, so at some point you need one. The route is the room rather than an app: dance with people at a jam, and afterwards simply ask whether they would want to practise outside it. Plenty of people want a practice partner and never ask.</p>
      <p>Agree two things before you start: where on the body you are working, and that either of you can stop at any time. Twenty minutes of weight sharing on a floor with no music is a complete practice.</p>
      <h2>The second visit</h2>
      <p>The second visit is easier and stranger than the first. Easier, because you know the shape of the evening and where the water is. Stranger, because you now have a body memory of what a dance feels like, and the gap between that and the beginning of the next one is palpable.</p>
      <p>Most people who stop doing CI stop between the first and third visit. Going back twice is usually enough to make it a habit.</p>
      <h2>If nothing is running this week</h2>
      <p>Miami has no central CI calendar, so "is there a jam tonight?" has no static answer, and this site does not guess or publish a date it has not checked. The places that can answer are the organisers themselves, whose own pages and direct messages are the only authoritative source, and the <a href="/jams">jams page</a> where each entry shows the date it was last checked.</p>
      <p>The global CI World Jam Map keeps a <a href="https://www.contactimprov.com/florida.html" rel="noopener nofollow">Florida page</a> of the community's own listings, and it is honest about being patchy. The <a href="/directory">directory</a> here lists the studios, organisers and adjacent practices that are current and answer a message.</p>
      <h2>Becoming part of the room</h2>
      <p>A scene with no institution is maintained by whoever shows up early. Three things turn attendance into membership: arrive at the start, because the opening circle is where the room's rules are set and where a newcomer is easiest to include. Offer to help set up or pack down, since the people doing that are the people who know what is happening next month. And when you are ready, host.</p>
      <p>Most jams in the world exist because one person booked a room, so <a href="/miami#start-one">starting one in Miami</a> is the actual mechanism rather than a consolation prize. If you know where the dancing is this month, <a href="/about#submit">tell this site</a> and it goes on the map.</p>
      <h2>The rhythm of a year in Miami</h2>
      <p>Practice here comes in layers. A weekly class or jam is the floor. Workshops sit above it. Once a year, in February, Love Burn on Virginia Key brings Camp Contact, which runs contact improvisation, acro yoga, ecstatic dance and authentic relating as its programme.</p>
      <p>That camp is the largest concentration of contact improvisation that happens in Miami in a year, and it is a festival rather than a class. Dates move, so read the organiser's own page; this page publishes no dates at all.</p>
    </div>
    {sessions}
    <div class="prose">
      <p>{SESSIONS_RANK_NOTE}</p>
      <h2>What this page will not do</h2>
      <p>It will not give you a calendar. A date that has not been verified against the organiser's own page does not appear on this site, because an out-of-date listing is worse than no listing. A class teaches the skills a jam assumes, and <a href="/classes">classes and workshops</a> covers how to judge one.</p>
    </div>
    {band("Where this week's dancing actually is", "The organisers' own pages are the only current source, and each entry above links to one.", [("Jams in Miami", "/jams", "primary"), ("Teachers and organisers", "/directory", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>How to keep practising Contact Improvisation in Miami</em>. miamicontactimprov.com. https://miamicontactimprov.com/keep-practising")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/keep-practising",
            "How to keep practising Contact Improvisation in Miami",
            "What to do after a first Contact Improvisation jam in Miami: practising alone and with a partner, the second visit, the weeks when nothing is running, and how to stay informed.",
            date_modified=LAST_CHECKED_ISO,
        ),
        schema.breadcrumb("/keep-practising", "Keep practising"),
    )
    return page(
        "Keep Practising Contact Improv [2026 Guide] | Next Steps",
        "What to do after your first contact improv jam in Miami: practising alone and with a partner, the second visit, weeks when nothing is running, and staying informed.",
        "/keep-practising",
        body,
        jsonld=jsonld,
    )


# ---------------------------------------------------------------- the Friday jam
FRIDAY_JAM_FAQ = [
    ("Do I need a partner or any experience for the Friday jam?",
     "No. It is an open, all-levels jam. Most people arrive alone, the warm-up starts from standing and rolling rather than lifts, and you may sit at the edge and watch for as long as you like. First-timers are expected, not tolerated."),
    ("Do I have to book?",
     "No. There is no ticket and no list. Come to the door at Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, between 7:00 and 7:15 PM so you catch the opening circle. Arriving later is fine; leaving early always is."),
    ("How much is it, and how does the sliding scale work?",
     "$20 at the door, on a sliding scale of $20 to $50. Pay what you can within that range and nobody will ask where you landed. The money covers the studio; the jam is not run for profit."),
    ("Where exactly is it?",
     "On the north edge of Miami: Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009, just past Aventura on US-1. The postcode is Hallandale Beach, Broward County, and the site prints it that way because an address is copied, not rounded. Miami Contact Improv covers both Miami-Dade and Broward."),
    ("Who runs it?",
     "Max Petrusenko, who also maintains this website. That is why this session is listed with a disclosure on every page that carries it, and why it is ranked no higher than any other entry."),
    ("What should I wear and bring?",
     "Loose clothing that covers your back, shoulders and knees, no zips or buckles, bare feet or soft socks, a full water bottle and a towel. Leave rings, watches and necklaces off. Details are on the jams page."),
    ("Is there music?",
     "Sometimes quiet music during the warm-up, usually none in the open jam. Contact Improvisation is danced to the partner, not the track."),
    ("Can I just come and watch?",
     "Yes. Watching from the edge is participation in this form, and nobody will pull you onto the floor. Tell the host at the circle that you are watching tonight and that is the end of the conversation."),
]


def friday_jam():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FRIDAY_JAM_FAQ)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Fridays &middot; 7:00&ndash;9:00 PM &middot; Miami</p>
    <h1>The Friday jam in Miami.</h1>
    <p class="lede">A weekly open Contact Improvisation jam at Inner Motion Dance Studio on the north edge of Miami. No partner, no experience, no booking. First session Friday 2 October 2026.</p>
    <div class="btn-row">
      <a class="btn primary" href="https://maps.apple.com/?q=216+NE+1st+Ave,+Hallandale+Beach,+FL+33009" rel="noopener">216 NE 1st Ave, Hallandale Beach</a>
      <a class="btn secondary" href="/your-first-jam">Never been to a jam?</a>
    </div>
    <p class="micro">$20 at the door, sliding scale $20&ndash;50. Hosted by Max Petrusenko, who also runs this site.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("The Friday jam is a weekly, open, all-levels Contact Improvisation jam in Miami, held at Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009, every Friday from 7:00 to 9:00 PM, starting 2 October 2026. It costs $20 at the door on a sliding scale of $20 to $50, needs no partner, no prior experience and no booking, and is hosted by Max Petrusenko, the maintainer of miamicontactimprov.com.")}
    {facts([
      ("When", "Every Friday, 7:00–9:00 PM"),
      ("First session", "Friday 2 October 2026"),
      ("Where", "Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009"),
      ("Area", "North edge of Miami, just past Aventura on US-1"),
      ("Cost", "$20 at the door, sliding scale $20–$50"),
      ("Booking", "None. Come to the door"),
      ("Who it is for", "Open and all levels. First-timers welcome, watching is fine"),
      ("Host", "Max Petrusenko"),
      ("Language", "English and Spanish"),
      ("Questions", "hello@miamicontactimprov.com"),
    ])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>How the evening runs</h2>
    <div class="prose">
      <p><strong>7:00.</strong> Doors. Change, drink water, find a place on the floor. Shoes stay off the dance floor.</p>
      <p><strong>7:10, the circle.</strong> A few minutes. The host says who is holding the room and states the protocol: consent is continuous, you may decline anything without a reason, the edge is for resting and watching, nobody teaches uninvited, nobody films without asking. Anyone can add a boundary or say they are leaving early. If it is your first time, say so; the room will meet you accordingly.</p>
      <p><strong>Warm-up.</strong> A guided sequence from standing and the floor, then a few minutes of <strong>small dance</strong>. On some Fridays a short piece of material follows; it is offered, not required.</p>
      <p><strong>The open jam.</strong> The long middle of the evening, usually with no music. Dances begin with a look or a hand and end when either person stops. Resting between dances is normal. Solo dancing is part of the form.</p>
      <p><strong>8:50, closing.</strong> A short circle or a moment of stillness, then out by 9:00 so the studio can close.</p>
      <h2>The sliding scale</h2>
      <p>The door is $20 and the scale runs to $50. The lower end covers the room when enough people come; the upper end is for anyone who can carry more of it and would like the jam to keep running. Choose in private, hand it over, done. Nobody is turned away from a first jam over money: if $20 is the barrier this week, come anyway and say so at the door.</p>
      <h2>Getting there</h2>
      <p>Inner Motion Dance Studio is at 216 NE 1st Ave in Hallandale Beach, just east of US-1 (Federal Highway) and north of Hallandale Beach Boulevard. From Miami it is the first city over the county line after Aventura; from Fort Lauderdale it is south of Hollywood. If you need parking or access details before you come, <a href="mailto:hello@miamicontactimprov.com">email</a> and you will get an answer before Friday.</p>
      <h2>Who is holding the room</h2>
      <p>Max Petrusenko hosts the jam. He also builds and maintains this website, which is why this page reads as the organiser describing his own session, and why the <a href="/miami-jams">Miami-Dade and Broward jam list</a> carries the same disclosure next to the entry. The rest of this site lists other people's sessions on the strength of their own published pages; this one is listed on the strength of this page, and it will come down the week it stops running rather than sit here looking current.</p>
      <h2>Ground rules</h2>
      <p>The full version is on <a href="/safety-and-consent">safety and consent</a>. The short version: keep the contact point singular, keep your own feet available, roll out of falls rather than bracing, say no when you mean no and accept no without asking why, leave a dance when it is over, and do not teach unless asked.</p>
      <h2>Questions about the Friday jam</h2>
      {faq_html}
    </div>
    {band("Coming this Friday?", "You do not need to tell anyone. If you want to ask something first, one email is enough and it gets answered before the weekend.", [("Email the host", "mailto:hello@miamicontactimprov.com", "primary"), ("Your first jam, step by step", "/your-first-jam", "secondary"), ("All verified sessions", "/miami-jams", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>The Friday jam in Miami</em>. miamicontactimprov.com. https://miamicontactimprov.com/friday-jam")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/friday-jam",
            "Friday Contact Improv Jam in Miami",
            "A weekly open, all-levels Contact Improvisation jam in Miami at Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, Fridays 7:00 to 9:00 PM from 2 October 2026. $20 at the door on a sliding scale of $20 to $50. Hosted by Max Petrusenko.",
            date_modified=listings.FRIDAY_JAM_VERIFIED,
        ),
        schema.breadcrumb("/friday-jam", "Friday jam"),
        schema.faq(FRIDAY_JAM_FAQ),
        listings.friday_jam_event(),
    )
    return page(
        "Friday Contact Improv Jam in Miami [Weekly 7–9 PM]",
        "Weekly open Contact Improvisation jam in Miami, Fridays 7 to 9 PM at Inner Motion Dance Studio, 216 NE 1st Ave. $20 sliding scale, no partner or booking. From 2 October 2026.",
        "/friday-jam",
        body,
        jsonld=jsonld,
    )
