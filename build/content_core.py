"""Core pages: home, what-is, history, glossary."""

from shell import answer, band, cards, cite_block, facts, page
import schema

H1 = "Contact Improvisation in Miami"


# ---------------------------------------------------------------- home
def home():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Miami &middot; Miami Beach &middot; South Florida</p>
    <h1>Two people, one shared point of contact, and whatever happens next.</h1>
    <p class="lede">Contact Improvisation is a dance form you can start tonight and never finish learning. This site is the working map of where it happens in Miami: the jams, the classes, the teachers, the vocabulary, and the history behind it.</p>
    <div class="btn-row">
      <a class="btn primary" href="/miami">Find it in Miami</a>
      <a class="btn secondary" href="/what-is-contact-improvisation">What is CI?</a>
    </div>
    <p class="micro">No membership. No central authority. This is a community resource, not a studio.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("Contact Improvisation (CI) is a partnered dance form built from a single moving point of contact, usually the back or shoulders, through which two dancers share weight and follow gravity, momentum and impulse instead of choreography. It began in the United States in 1972 with the dancer and choreographer Steve Paxton, and it has no licensing body, no required uniform and no fixed syllabus. In Miami it is practised in jams, classes and workshops across Miami-Dade and Broward County.", "What is contact improvisation in Miami?")}
    {facts([
      ("What it is", "An improvised partnered dance around shared weight and a rolling point of contact"),
      ("When it started", "1972, United States, developed by Steve Paxton"),
      ("Who can do it", "Anyone. No dance training, partner or flexibility required to begin"),
      ("What a jam is", "An open, unguided dance session. Come and go, dance or watch"),
      ("What it costs in Miami", "Set by each organiser. Community jams are typically low-cost or donation-based"),
      ("What you need", "Loose clothes, water, bare or soft feet, and a willingness to say no"),
      ("Where it happens here", "Studios, cultural centres, parks and beaches across Miami-Dade and Broward"),
    ])}
    <div class="prose">
      <p>The form is deliberately open. There is no federation that certifies who may teach it, and no governing body that decides what counts. That is why a city scene is built out of individual organisers and borrowed rooms rather than a single institution, and why a map like this one is useful.</p>
    </div>
    {cite_block("Miami Contact Improv (2026). <em>Contact Improvisation in Miami</em>. miamicontactimprov.com. Retrieved from https://miamicontactimprov.com/")}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Start from where you are</h2>
    {cards([
      ("Never done it", "Watch first, then dance", "What a jam actually looks like from the inside, and why watching is a legitimate way to participate.", "/classes#first-jam"),
      ("Looking for a session", "Jams and open practice", "What an open jam is, how the room usually runs, and what to say when you arrive.", "/jams"),
      ("Want teaching", "Classes and workshops", "Beginner series, workshops and intensives, plus what to look for in a teacher.", "/classes"),
      ("Learning the words", "Glossary", "Jam, score, small dance, underscore, spotting, weight sharing, and the rest of the working vocabulary.", "/glossary"),
      ("Curious about the form", "History and principles", "Where CI came from, who built it, and the ideas it borrowed from aikido, postmodern dance and somatics.", "/history"),
      ("Need the ground rules", "Safety and consent", "Boundaries, spotting, what is expected of you and what you may always refuse.", "/safety-and-consent"),
    ])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Why a jam is not a class</h2>
    <div class="prose">
      <p>A <strong>class</strong> gives you a skill. A <strong>jam</strong> gives you the situation in which the skill becomes useful. Most jams have no teacher and little or no music; people arrive, find a partner or dance alone, and leave when they are done. There is usually an edge of the room for sitting, watching and resting, and using it is normal rather than rude.</p>
      <p>If you have only ever danced in set choreography, the first twenty minutes of a jam can feel formless. It helps to know that this is the form, not a failure of it. You are not waiting for instruction. You are listening to a body that already knows how to fall safely and stand up again.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>The one rule that carries everything else</h2>
    <div class="prose">
      <p>Contact Improvisation works because either dancer can stop at any point, for any reason, without explanation. A lifted partner can put a foot down. A held partner can step away. The dance continues. Practitioners call this the negotiation, and it happens through weight, breath and small physical signals long before anyone speaks.</p>
      <p>Written down it sounds abstract. In the room it is the most practical thing you will learn, and it is why people who have never considered themselves dancers keep coming back.</p>
    </div>
    {band("New to Miami, or new to this?", "Tell us you exist and we will add you to the map. Jams, classes, teachers, studios, festivals and recurring practice groups all belong here.", [("Submit a listing", "/about#submit", "primary"), ("Read the directory", "/directory", "secondary")])}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/",
            H1 + " | " + "Miami Contact Improv",
            "Contact Improvisation in Miami: jams, classes, teachers, video and history. An independent community map of CI across Miami-Dade and Broward County.",
        ),
        {
            "@type": "Place",
            "@id": schema.SITE + "/#place",
            "name": "Miami, Florida",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Miami",
                "addressRegion": "FL",
                "addressCountry": "US",
            },
            "geo": {"@type": "GeoCoordinates", "latitude": 25.7617, "longitude": -80.1918},
        },
    )
    return page(
        "Contact Improvisation Miami [2026 Guide] | Jams & Classes",
        "Contact Improvisation in Miami: what it is, where the jams are, who teaches it and how to start. A community map of CI across Miami-Dade and Broward County.",
        "/",
        body,
        jsonld=jsonld,
    )


# ---------------------------------------------------------------- what is CI
WHATIS_TERMS = [
    ("contact-improvisation", "Contact Improvisation (CI)",
     "A partnered dance form in which two or more dancers improvise around shifting points of physical contact, sharing weight and following gravity, momentum and impulse."),
    ("jam", "Jam",
     "An open, unguided session where anyone present can dance. No teacher, little or no music, an edge to sit and watch."),
    ("score", "Score",
     "A stated constraint that gives an improvisation a shape, such as dancing only below the hips, or following the point of contact without interrupting it."),
    ("small-dance", "Small dance",
     "Small dance is the standing practice that opens a session: you stand still and follow the micro-adjustments the body makes to stay upright, rather than trying to hold still."),
    ("weight-sharing", "Weight sharing",
     "Deliberately giving part or all of your weight to a partner and taking theirs, with the support of the skeleton and the floor rather than muscle. It is the core mechanic of the form: one dancer gives weight, the other receives it, and the roles trade continuously."),
    ("spotting", "Spotting",
     "Standing ready, hands free, near a dancing pair, so that if a fall goes wrong there is someone in reach to slow it."),
]

# A retired synonym stays retrievable as an alternateName on the canonical term,
# so the glossary holds one DefinedTerm per term rather than two competing ones.
TERM_ALTERNATES = {
    "small-dance": "the small dance",
    "weight-sharing": "weight exchange",
}

WHATIS_FAQ = [
    ("What is Contact Improvisation?",
     "Contact Improvisation is an improvised partnered dance form that began in 1972 with the American dancer and choreographer Steve Paxton. Two dancers keep a moving point of physical contact, usually the back or shoulders, and share weight while following gravity, momentum and impulse rather than a set sequence of steps."),
    ("Do I need dance experience to start?",
     "No. Contact Improvisation was built partly as a way to widen who could be a mover, and beginners' classes assume no prior training. What helps is being willing to fall, to be close to another person, and to say no."),
    ("Is Contact Improvisation sexual?",
     "No. The practice is built on shared weight and physical listening, and consent is treated as continuous and revocable. Most jams state this explicitly before the dancing starts. Touch is part of the form; it is not a route to anything else, and a partner who treats it that way is breaking the form rather than expressing it."),
    ("What happens at a jam?",
     "People arrive, warm up, dance with one partner or several, rest at the edge, and leave. There is no teacher and usually little or no music. Many jams open with a short circle where boundaries and any announcements are shared."),
    ("How do you dance without hurting each other?",
     "By keeping contact continuous, letting the floor take as much weight as possible, rolling rather than bracing, and keeping your own feet available to land on. Falls are usually taken as low rolling exits rather than stops. Many jams keep one or two people outside the dance, spotting."),
    ("What is the difference between a jam, a class and a workshop?",
     "A class teaches a skill in a sequenced session. A workshop concentrates one theme over hours or days. A jam is unguided social practice: the room is the teaching. All three exist in the same scene and often in the same studio."),
    ("Is there a governing body for Contact Improvisation?",
     "No. In 1975 a group of dancers touring with Steve Paxton considered trademarking the term and setting up teacher certification, largely out of concern for safety as the form spread. They rejected both and started a newsletter instead, which became the journal Contact Quarterly. There has never been a licensing body since."),
    ("Why is there no music at some jams?",
     "Because listening to your partner's weight is part of the practice, and music covers some of the information the dance runs on. Many jams use no music, or a single quiet ambient set, and some use live musicians."),
]


def what_is():
    faq_html = "".join(
        f"<h3>{q}</h3><p>{a}</p>" for q, a in WHATIS_FAQ
    )
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">The form</p>
    <h1>What is Contact Improvisation?</h1>
    <p class="lede">A partnered dance you cannot rehearse, built from shared weight, a rolling point of contact, and the willingness to fall.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("Contact Improvisation (CI) is a partnered, improvised dance form developed by the American dancer and choreographer Steve Paxton in 1972, in which two or more dancers maintain a moving point of physical contact and explore the exchange of weight through gravity, momentum, inertia and touch. It has no fixed syllabus, no licensing body and no requirement of prior dance training.")}
    <div class="prose">
      <p>The dance usually begins before it begins. Dancers stand still for a minute or two first, noticing the small continuous adjustments the body makes to stay upright. Paxton called this the <strong>small dance</strong>, and it is the reason CI tends to look like listening rather than performing.</p>
      <p>From there, contact starts somewhere, often a hand or a shoulder, and the pair moves. Weight shifts. One partner's support becomes the other's floor. A lift happens because both bodies arrived in the right arrangement, not because someone planned it. When it goes wrong, the pair rolls down and out of it, and the dance continues from wherever they land.</p>
      <blockquote>
        The exigencies of the form dictate a mode of movement which is relaxed, constantly aware and prepared, and onflowing.
        <cite>Steve Paxton, originator of Contact Improvisation</cite>
      </blockquote>
      <p>Paxton described the form's relationship to other duets through the words of one of its first practitioners. Nancy Stark Smith, who took part in the earliest performances and edited the journal that grew out of the form, wrote that it "resembles other familiar duet forms, such as the embrace, wrestling, surfing, martial arts, and the Jitterbug, encompassing a wide range of movement from stillness to highly athletic." That range is real. A single evening can contain five minutes of near-stillness and a fully airborne lift.</p>
      <h2>Three things that make it different</h2>
      <p><strong>It is not choreography.</strong> Nothing is set in advance, and repeating something is a choice rather than a requirement. The dance is made in the moment by two people who can only know what happens next as it happens.</p>
      <p><strong>The weight is real.</strong> A partner's whole mass may transfer onto your back, hip or shoulder, which is what makes lifts physically possible and also what makes spotting and safe exits part of the form rather than an afterthought.</p>
      <p><strong>Consent is a technical skill, not a disclaimer.</strong> Because touch is the medium, the ability to decline, pause or leave mid-dance is trained alongside the movement. A dance in which you cannot withdraw is not CI being done well; it is CI not being done.</p>
      <h2>What it is not</h2>
      <p>Contact Improvisation is not partnered acrobatics for an audience, although experienced dancers can make it look like that. It is not a therapy session, although people often find it restorative. It is not sexual practice, and jams collectively enforce that distinction. And it is not a single correct method: because the form was never trademarked and never certificated, teaching styles differ widely between organisers and cities.</p>
      <h2>How it reached Florida</h2>
      <p>CI spread through touring, teaching and a paper newsletter rather than an organisation, which is why most cities evolved their own scene without any central direction. Miami is no exception: practice here runs through individual teachers, studio rentals, parks and the wider South Florida dance and movement community rather than a single institution. <a href="/miami">The Miami page</a> maps what is currently known.</p>
      <h2>Questions people actually ask</h2>
      {faq_html}
    </div>
    {band("Ready to try it?", "Read what happens at a jam before you go, then find one near you.", [("Jams in Miami", "/jams", "primary"), ("First jam walkthrough", "/classes#first-jam", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>What is Contact Improvisation?</em>. miamicontactimprov.com. https://miamicontactimprov.com/what-is-contact-improvisation")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/what-is-contact-improvisation",
            "What is Contact Improvisation?",
            "Contact Improvisation defined: history, principles, what a jam is, why there is no licensing body, and what happens in the first five minutes.",
            about=[
                {"@id": schema.SITE + "/#place"},
                {"@id": schema.SITE + "/glossary#terms"},
            ],
        ),
        schema.breadcrumb("/what-is-contact-improvisation", "What is Contact Improvisation?"),
        schema.faq(WHATIS_FAQ),
    )
    return page(
        "What Is Contact Improvisation? [Step-by-Step Guide]",
        "Contact Improvisation explained: a 1972 partnered dance form built on shared weight and a rolling point of contact. What a jam is, consent, spotting and how to start.",
        "/what-is-contact-improvisation",
        body,
        jsonld=jsonld,
    )


# ---------------------------------------------------------------- history
HISTORY_FAQ = [
    ("Who invented Contact Improvisation?",
     "Steve Paxton, an American dancer and choreographer. He developed it in 1972 out of experiments at Oberlin College and a series of performances in New York, drawing on his background in gymnastics, aikido, t'ai chi, Merce Cunningham's company and the Judson Dance Theater."),
    ("When was the first Contact Improvisation performance?",
     "In January 1972 Steve Paxton presented 'Magnesium' at Oberlin College during a Grand Union residency, a work for eleven men on mats that ended in several minutes of quiet standing. In June 1972 a newly assembled mixed group performed the work that became known as Contact Improvisation at the John Weber Gallery in New York City."),
    ("Why was Contact Improvisation never trademarked?",
     "In 1975 the dancers touring with Steve Paxton as ReUnion considered trademarking the name and setting up teacher certification, chiefly out of concern for safety as the form spread beyond people who had learned it directly. They decided against both and started a newsletter instead. That newsletter became the journal Contact Quarterly."),
    ("Who were the first Contact Improvisation dancers?",
     "The group around the earliest performances in New York in 1972 included Nancy Stark Smith, Nita Little, Daniel Lepkoff, Barbara Dilley, Nancy Topf, Mary Fulkerson, Laura Chapman, Alice Lusterman, Curt Siddall, David Woodberry, Leon Felder and video documentarian Steve Christiansen. Nancy Stark Smith went on to edit Contact Quarterly and to develop the Underscore."),
]


def history():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in HISTORY_FAQ)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">History</p>
    <h1>Where Contact Improvisation came from.</h1>
    <p class="lede">It started in a college gymnasium in Ohio, was named in a New York gallery, and was deliberately left unowned.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("Contact Improvisation (CI) was developed by the American dancer and choreographer Steve Paxton in 1972. It emerged from a residency at Oberlin College in January 1972 and a set of performances at the John Weber Gallery in New York in June 1972, and it was influenced by modern dance, aikido and somatic practices. The form was never trademarked and has no licensing body.")}
    <div class="prose">
      <h2>January 1972, Oberlin College</h2>
      <p>The improvisational collective Grand Union was in residency at Oberlin College in Ohio. Paxton, a member of that group, had been running what he called a soft class in the early mornings, part meditation and part mild exercise. During the residency he made a work called <strong>Magnesium</strong> for eleven men on mats, in which they threw, caught, flung and fell among one another continuously, ending in several minutes of quiet standing. He had already asked a student who was watching, Nancy Stark Smith, to stay in touch if he ever worked this way again.</p>
      <p>Paxton brought an unusual set of influences to it: competitive gymnastics from his school years, years of aikido study at the New York Aikikai, t'ai chi, three years in the Merce Cunningham Dance Company, and co-founding the Judson Dance Theater in 1962. Release technique arrived through Mary Fulkerson, whom he invited into the next group.</p>
      <h2>June 1972, New York</h2>
      <p>In June he assembled a mixed group for five days of continuous practice and a public showing at the John Weber Gallery in New York City. That event was called Contact Improvisation. The group included Nancy Stark Smith, Nita Little, Daniel Lepkoff, Barbara Dilley, Nancy Topf, Mary Fulkerson, Laura Chapman, Alice Lusterman, Curt Siddall, David Woodberry and Leon Felder, with Steve Christiansen documenting on video. The first iteration of the dance was made in that week.</p>
      <h2>1975: the decision not to own it</h2>
      <p>By 1975 the dancers working with Paxton had formed ReUnion, a company that met once a year to tour the West Coast with performances and classes. They discussed trademarking the term <em>contact improvisation</em> and establishing a teacher certification, chiefly because the form was spreading faster than its safety practices were. They rejected both, and instead started a newsletter as a way to keep geographically scattered practitioners in contact.</p>
      <p>Nancy Stark Smith edited and produced that newsletter, typing and photocopying the first issues herself. Lisa Nelson joined as co-editor in 1976, and the publication was renamed <strong>Contact Quarterly</strong>, described then and since as a vehicle for moving ideas. It ran for four and a half decades. The refusal to trademark or certificate is the reason there is no licensing authority for Contact Improvisation anywhere in the world today, and the reason any city's scene looks the way it does: locally organised, informally taught, and held together by the people who show up.</p>
      <h2>How the practice developed</h2>
      <p>Stark Smith went on to develop the <strong>Underscore</strong>, a long-form score that gives a group improvisation an arc of twenty or so named phases, and the <strong>hieroglyphs</strong>, a notation for the felt rhythm of a dance. Lisa Nelson's work on composition and perception shaped how the practice talks about seeing and being seen. Nita Little's research into attentional states connected CI to cognitive science. The form also moved into performance work, into dance therapy, into physical theatre and into contemporary choreography, in a way that its early practitioners had not expected.</p>
      <h2>The jam as the real institution</h2>
      <p>Because there was never an organisation, the thing that carried CI worldwide was the jam: an informal, recurring, untaught session in a borrowed room, advertised by word of mouth or a printed listing. Contact Quarterly carried those listings for decades in a section called DanceMap. That function now happens in scattered places, which is a large part of why this site exists for Miami.</p>
      <h2>Questions people ask about the history</h2>
      {faq_html}
    </div>
    <div class="prose" style="margin-top:40px">
      <h2 style="margin-top:0">Sources</h2>
      <ul>
        <li><a href="https://en.wikipedia.org/wiki/Contact_improvisation" rel="noopener">Contact improvisation</a>, Wikipedia (accessed September 2026)</li>
        <li><a href="http://sarma.be/docs/3269" rel="noopener">A Short History</a>, SARMA (accessed September 2026)</li>
        <li><a href="https://www.nytimes.com/2020/05/27/arts/dance/nancy-stark-smith-dead.html" rel="noopener">Nancy Stark Smith, a Founder of Contact Improvisation, Dies at 68</a>, The New York Times, 27 May 2020</li>
        <li><a href="https://www.contactquarterly.com/" rel="noopener">Contact Quarterly</a>, the journal that grew from the 1975 newsletter</li>
      </ul>
    </div>
    {band("Dance the history instead of reading it", "The form is easier to feel than to describe. Find a jam and stand still in a room with other people for two minutes.", [("Jams in Miami", "/jams", "primary"), ("Glossary of terms", "/glossary", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>History of Contact Improvisation</em>. miamicontactimprov.com. https://miamicontactimprov.com/history")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/history",
            "History of Contact Improvisation",
            "How Contact Improvisation began in 1972: Steve Paxton, Magnesium at Oberlin, the first performances at the John Weber Gallery, and the 1975 decision not to trademark the form.",
        ),
        schema.breadcrumb("/history", "History"),
        schema.faq(HISTORY_FAQ),
    )
    return page(
        "History of Contact Improvisation [Timeline] | 1962 to Now",
        "How Contact Improvisation began: Steve Paxton, Magnesium at Oberlin College, the first performances in New York in 1972, and why the form was never trademarked.",
        "/history",
        body,
        jsonld=jsonld,
    )


# ---------------------------------------------------------------- glossary
def glossary():
    rows = []
    for slug, term, definition in WHATIS_TERMS:
        rows.append(
            f'<h3 id="{slug}">{term}</h3><p>{definition}</p>'
        )
    extra = [
        ("underscore", "Underscore",
         "A long-form group score developed by Nancy Stark Smith, moving through around twenty named phases and used to shape an entire practice session or festival."),
        ("landing", "Landing",
         "Arriving on the floor from a fall or a lift, usually by rolling through the contact point so the floor takes the weight progressively."),
        ("solo", "Solo",
         "Dancing alone inside a jam. Entirely normal, and often where the most interesting work happens."),
        ("edge", "The edge",
         "The perimeter of the room where people rest, watch, drink water and re-enter. Watching from the edge is participation, not absence."),
        ("contact point", "Contact point",
         "The single place where two bodies touch. Keeping it singular is what stops the dance becoming a grapple."),
        ("duet", "Duet",
         "Two dancers. The basic unit of the form, though CI also happens in trios and larger groups."),
        ("open jam", "Open jam",
         "A jam with no experience prerequisite. If a jam is closed to beginners, the listing will say so."),
        ("consent practice", "Consent practice",
         "The habit of asking, declining and renegotiating inside the dance. Treated as part of the technique rather than a policy."),
    ]
    extra_html = "".join(f'<h3 id="{s}">{t}</h3><p>{d}</p>' for s, t, d in extra)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Vocabulary</p>
    <h1>The words people use in the room.</h1>
    <p class="lede">Contact Improvisation has its own working language. None of it is required to dance, but knowing it makes the first jam far less opaque.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("The core Contact Improvisation (CI) vocabulary is: <strong>contact</strong> (the point where two bodies touch), <strong>weight sharing</strong> (giving and receiving body weight), the <strong>small dance</strong> (the standing practice that opens a session, following the body's micro-adjustments rather than holding still), a <strong>score</strong> (a stated constraint), the <strong>jam</strong> (an open unguided session) and <strong>spotting</strong> (standing ready to catch a fall).", "The short version")}
    <div class="prose">
      <h2>Terms people use in a jam</h2>
      <p>The working vocabulary of Contact Improvisation, in one sentence each. None of it is required to dance; knowing it makes the first jam far less opaque.</p>
      {''.join(rows)}
      {extra_html}
    </div>
    {band("Words learned, next step is a room", "The vocabulary makes sense about ten minutes into your first jam, not before.", [("Find a jam", "/jams", "primary"), ("What to expect", "/classes#first-jam", "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Contact Improvisation glossary</em>. miamicontactimprov.com. https://miamicontactimprov.com/glossary")}
  </div>
</section>
"""
    terms = WHATIS_TERMS + [(s, t, d) for s, t, d in extra]
    jsonld = schema.render(
        schema.organisation(),
        schema.webpage(
            "/glossary",
            "Contact Improvisation glossary",
            "Working vocabulary of Contact Improvisation: jam, score, small dance, underscore, weight sharing, spotting, landing and the edge.",
        ),
        schema.breadcrumb("/glossary", "Glossary"),
        schema.defined_terms(terms, alternates=TERM_ALTERNATES),
    )
    return page(
        "Contact Improvisation Glossary [Checklist] | Jam, Score & More",
        "Plain-language definitions of Contact Improvisation terms: jam, score, small dance, underscore, weight sharing, spotting, landing and the edge.",
        "/glossary",
        body,
        jsonld=jsonld,
    )
