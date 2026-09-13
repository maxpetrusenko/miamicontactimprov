"""Practice pages: jams, classes, safety and consent, video room."""

from shell import answer, band, cards, cite_block, facts, page
import schema
import listings
import videos_data

FIRST_JAM_FAQ = [
    ("What do I wear to a contact improv jam?",
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
    ("What is a contact improv jam?",
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
    {answer("A contact improv jam is an open, unguided session where people practise Contact Improvisation together. There is no teacher and usually no music. Participants arrive and leave freely, dance with whoever is willing, sit at the edge to rest and watch, and stop at any time. Jams are the primary way the form is practised in Miami and worldwide.")}
    {listings.sessions_block()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>How a jam usually runs</h2>
    <div class="prose">
      <p>Formats vary, but most jams follow a recognisable shape.</p>
      <p><strong>Arrival.</strong> People change, stretch, greet each other, and find a place on the floor. Someone who is hosting opens a circle.</p>
      <p><strong>The circle.</strong> Two or three minutes. The host states the protocol: consent is continuous, you may decline anything, the edge is for resting, and here is where the water is. Anyone may add a boundary or announce something, such as an injury or that they are leaving early.</p>
      <p><strong>Warm-up.</strong> Often a short guided sequence or the small dance, standing still and following the body's micro-adjustments. If there is a teacher present, they may offer twenty minutes of material before the open dancing begins.</p>
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
            "What a contact improv jam is, how a session usually runs, what to bring, and the jams and open practice sessions confirmed in Miami and South Florida.",
        ),
        schema.breadcrumb("/jams", "Jams"),
        schema.faq(JAMS_FAQ),
        listings.sessions_schema(),
    )
    return page(
        "Contact Improv Jams in Miami | What to Expect & Where to Go",
        "What a contact improv jam is and how a session runs, plus the open practice sessions confirmed in Miami and South Florida. What to wear, what to bring, how to leave a dance.",
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
    {answer("A Contact Improvisation class teaches the underlying skills: how to share weight without collapsing, how to roll out of a fall, how to read your partner's momentum, and how to say no. Beginner sessions assume no dance training. Most people attend classes for a few weeks and then add a weekly jam, because the form is learned mostly by dancing rather than by instruction.")}
    <div class="prose">
      <h2 id="first-jam">Your first jam, step by step</h2>
      <p><strong>Before.</strong> Message the organiser and say you are new. Ask three things: is it open to beginners, what is the door fee, and is there a warm-up before the open dancing. All three answers should be easy.</p>
      <p><strong>Arriving.</strong> Get there for the start if you can, because the opening circle is where the rules are set. Change, leave your bag at the edge, fill your bottle.</p>
      <p><strong>The warm-up.</strong> Stand still and listen to the small adjustments your body makes to stay upright. This is not a warm-up for the real thing; it is the real thing at low amplitude.</p>
      <p><strong>Your first dance.</strong> Look at someone. If they look back, you are dancing. Start with a hand, a shoulder, or simply standing nearby. Keep one point of contact. Let one of you slowly give weight and see what the floor does.</p>
      <p><strong>Ending.</strong> Stop when you want to. Step back, nod, walk to the edge. No explanation needed and none expected, in either direction.</p>
      <p><strong>After.</strong> You will probably be tired in a way that is not athletic tired. Drink water. Come back.</p>
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
      {listings.classes_block()}
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
        "Contact Improvisation Classes in Miami | Beginners Welcome",
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
    ("Is there a code of conduct for contact improv?",
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
    {answer("In Contact Improvisation, consent is continuous rather than given once. Any dancer may decline an invitation, pause, slow down, change what they are doing or leave a dance at any point, without explanation. Jams are unguided and unsupervised, so the person hosting the session is responsible for stating the protocol and acting on violations.")}
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
    {band("A jam that takes this seriously", "The sessions worth your time say their protocol out loud at the start of every session. If yours does not, ask why.", [("Find a jam", "/jams", "primary"), ("Read about jams", "/jams", "secondary")])}
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
        "Contact Improv Safety & Consent | Your Rights in a Jam",
        "Consent in Contact Improvisation: what you may always decline, how physical safety works, spotting, what the practice is not, and what to do when something goes wrong.",
        "/safety-and-consent",
        body,
        jsonld=jsonld,
    )


def videos():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Video room</p>
    <h1>What it looks like when it is working.</h1>
    <p class="lede">Contact Improvisation is difficult to describe and immediately recognisable on film. These are the performances, jams and documentary records worth watching before your first session.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("Contact Improvisation on video falls into three useful categories: performance work, where trained dancers push the form to its physical limits; jam footage, which shows what an ordinary session actually looks like; and documentary and teaching material, which explains the principles behind what you are seeing.")}
    {videos_data.gallery()}
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
            "Contact Improvisation on film: performance work, jam footage and documentary records, with sources and channels.",
        ),
        schema.breadcrumb("/videos", "Videos"),
        videos_data.schema_list(),
    )
    return page(
        "Contact Improvisation Videos | Performance, Jams & Documentary",
        "Contact Improvisation on film: performance work, jam footage and documentary records worth watching before your first session.",
        "/videos",
        body,
        jsonld=jsonld,
    )
