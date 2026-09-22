"""The blog: an index at /blog/ and original articles about Contact Improvisation.

Every article is written for this site (nothing copied), makes no local claim the
listings do not already make, and links into the library pages rather than repeating
them. Add an article by appending to ARTICLES; build/locales.py and build/build.py
carry a row per slug so it gets a canonical, a sitemap entry and a redirect rule.
"""

import schema
from shell import band, cite_block, page

BLOG_ROUTE = "/blog/"
PUBLISHED = "2026-09-20"

# slug, route, title, h1, description, read minutes, body html
ARTICLES = [
    (
        "blog-first-jam",
        "/blog/five-things-before-your-first-jam",
        "Five Things to Know Before Your First Contact Improv Jam",
        "Five things nobody tells you before your first jam",
        "What actually happens at a contact improv jam, and the five things that make the first one easier: sitting out, the awkward start, leaving a dance, and what to bring.",
        5,
        """
<p>Most guides to a first jam tell you what to wear. That part is easy: loose clothes, bare feet, no jewellery. What they skip is the part that trips people up, which is the first twenty minutes of standing in a room full of strangers who all seem to know what they are doing. Here is what would have helped.</p>
<h2>1. Sitting out is participation</h2>
<p>Every jam has an edge: a wall, a row of mats, somewhere people sit with water and watch. Newcomers often treat the edge as failure, as if the only real way to be at a jam is to be in the middle of it. It is the opposite. Watching is how you learn what the room does, how people enter and leave a dance, how a lift actually happens. Some of the most experienced dancers spend half the evening on the edge. Sit there first. Nobody is counting.</p>
<h2>2. Nobody is watching you</h2>
<p>This is the hardest one to believe and the most useful. In a jam, everyone dancing is busy with the weight in front of them. The attention in the room points inward, at the point of contact, not outward at whoever just walked in. The feeling of being observed is real, but it is coming from you. It fades faster than you expect, usually the first time someone gives you their weight and you realise you are too busy not dropping them to care how you look.</p>
<h2>3. The awkward start is the form, not a failure of it</h2>
<p>If you have only danced choreography, or only danced at parties with music, the opening of a jam can feel formless. People stand still. Someone rolls slowly on the floor. Two people lean back to back and do not appear to move. You are waiting for something to begin. It has begun. Contact Improvisation is built on listening, and listening looks like nothing from the outside. Give it ten minutes before you decide anything.</p>
<h2>4. You can leave any dance, at any moment, without a reason</h2>
<p>This is the rule that carries everything else. A lifted partner can put a foot down. A held partner can step away. You do not owe anyone an explanation, and a partner who needs one is the problem, not you. Good jams say this out loud in an opening circle; the ones this site lists do. Read the <a href="/safety-and-consent">safety and consent page</a> before you go so it is already in your body when you need it.</p>
<h2>5. You will be closer to strangers than at any party</h2>
<p>Someone's whole weight may end up on your back. Your head may rest on a stranger's hip. That is the practice, and it is neither romantic nor athletic in the way it looks from outside; it is mostly a conversation about balance. Knowing that in advance makes the first close moment a relief rather than a shock. And if it is not a relief, see point four.</p>
<p>When you are ready, the step-by-step is on <a href="/your-first-jam">your first jam</a>, and the room this site hosts is the <a href="/friday-jam">Friday jam</a>.</p>
""",
    ),
    (
        "blog-weight-sharing",
        "/blog/weight-sharing-explained",
        "Weight-Sharing Explained: The Core Skill of Contact Improv",
        "Weight-sharing, explained",
        "Giving weight, receiving weight, and the rolling point of contact: the one mechanic every contact improv dance is built on, and the mistake almost every beginner makes.",
        6,
        """
<p>Strip Contact Improvisation down to one mechanic and this is it: one dancer gives some of their weight, the other receives it, and the roles trade continuously through a point of contact that moves. Everything else in the form, the lifts, the rolls, the falls, the moments that look like flying, is this one exchange at a different scale.</p>
<h2>Giving weight is not leaning</h2>
<p>The beginner version of giving weight is leaning: you tip toward a partner and hope. Leaning keeps your own muscles braced and your own feet planted, which means you have not actually given anything. Your partner feels a push, not a weight. Giving weight means letting part of your mass genuinely rest on someone else's structure, so that if they stepped away you would have to move. It is uncomfortable at first precisely because it is real.</p>
<h2>Receiving weight goes through the skeleton, not the arms</h2>
<p>The other half of the exchange is where most injuries and most of the strain come from. Receiving a partner's weight in your arms, or by tensing your shoulders, works for about a minute and then hurts. Receiving it through the skeleton, stacking their weight over your hips, your legs and the floor, works all night. The image many teachers use is that you are not holding your partner up; you are giving them a floor that happens to be at an angle.</p>
<h2>The point of contact rolls</h2>
<p>What makes this a dance rather than a static lean is that the point where two bodies touch does not stay put. It rolls: from a shoulder blade across the back, over a hip, down a thigh. Following that rolling point, keeping it singular and continuous, is the actual skill of the form. When the point of contact splits into several, a hand here and a knee there, the dance tends to become a grapple. When it stays one and keeps moving, the lifts happen on their own because both bodies arrive in the right arrangement without anyone deciding to lift.</p>
<h2>The mistake: muscling it</h2>
<p>Almost every beginner tries to make the dance happen with strength. It is understandable, because strength is what most of us have used to move other people before. It also does not work, and it is tiring for everyone. The exchange runs on gravity and momentum. If you are working hard, you are usually fighting one of those instead of using it. The correction is almost always the same: lower, slower, and closer to the floor.</p>
<h2>Two ways to practise it</h2>
<p>Back to back with a partner, both standing, and slowly trade who is leaning on whom, without using hands. Then one of you on hands and knees as a stable table while the other lays their torso across your back and lets go of their own effort. Both are dull to watch and enormously informative to do. Every class covers them; the vocabulary is in the <a href="/glossary">glossary</a>, and the longer picture of the form is on <a href="/what-is-contact-improvisation">what Contact Improvisation is</a>.</p>
""",
    ),
    (
        "blog-falling",
        "/blog/how-to-fall-without-getting-hurt",
        "How to Fall Without Getting Hurt in Contact Improv",
        "How to fall without getting hurt",
        "Falling is not a mistake in contact improv, it is a skill: lowering your centre, rolling instead of stopping, keeping your feet available, and why spotting exists.",
        6,
        """
<p>In most physical practices a fall is the thing that went wrong. In Contact Improvisation it is a technique, practised deliberately, and the dancers who look most at ease in a jam are usually the ones who have fallen the most. The reason is simple: once you trust that you can get to the floor without harm, you stop bracing against it, and everything above the floor gets lighter.</p>
<h2>Lower your centre before anything else</h2>
<p>The distance you fall is the distance from your centre of gravity to the ground. Standing tall, that is a long way. Bent at the knees with your hips low, it is not. Most of what looks like fearless falling in experienced dancers is simply that they were never very far from the floor to begin with. If you feel a fall coming, go down first, on purpose, and the fall becomes a small one.</p>
<h2>Roll, do not stop</h2>
<p>A fall hurts when it ends abruptly: a knee hitting, a hand out stiff, a hip landing square. It does not hurt when the energy keeps travelling. The skill is to convert the downward motion into rotation, so that you arrive on the floor already rolling away from the point of impact. Rolling spreads the force across a curve of your body instead of a corner of it. In a class you will spend a lot of time rolling from kneeling and from sitting, precisely so that when a real fall comes, rolling is what your body reaches for.</p>
<h2>Exhale</h2>
<p>People hold their breath when they fall. A held breath stiffens the torso, and a stiff torso lands like a plank. Breathing out on the way down softens the whole structure. It sounds too simple to matter. It matters more than almost anything else on this list.</p>
<h2>Keep your feet available</h2>
<p>In a lift or a lean, the safest position is one where you could put a foot down if you needed to. Dancers talk about keeping your feet available, or keeping a landing gear. Giving your weight fully does not mean surrendering the ability to catch yourself. The two coexist, and a good partner will never put you somewhere you cannot get out of on your own.</p>
<h2>Why spotting exists</h2>
<p>At many jams one or two people stand near a dancing pair, hands free, not dancing. They are spotting: ready to slow a fall that goes wrong. You will not always see it because it is meant to be unobtrusive, and you can do it yourself from your first evening. It is a way of participating that asks nothing of your body and teaches you a great deal about where falls come from.</p>
<p>The rest of the ground rules, including what you can always refuse, are on <a href="/safety-and-consent">safety and consent</a>. If you want to learn falling in a taught setting before trying it in a jam, the <a href="/classes">classes page</a> is where to look.</p>
""",
    ),
    (
        "blog-consent",
        "/blog/consent-and-saying-no-mid-dance",
        "Consent in Contact Improv: Saying No Mid-Dance",
        "Dancing with strangers: consent and saying no mid-dance",
        "Consent in contact improv is continuous, mostly physical and always revocable: how the negotiation works, what a good jam does about it, and what to do if something feels off.",
        5,
        """
<p>Contact Improvisation is a form in which touch is the medium, and it happens mostly between people who have never met. That combination is why the form takes consent more seriously, and more practically, than almost any other movement practice. The short version: you can stop any dance at any moment for any reason, and the dance continues without you. The longer version is worth reading before you go.</p>
<h2>Consent here is continuous, not a checkbox</h2>
<p>In many settings consent is something you give once, at the start. In a jam it is renegotiated the whole time, because the dance is changing the whole time. Agreeing to a lean is not agreeing to a lift. Agreeing to dance now is not agreeing to dance in ten minutes. Practitioners call this the negotiation, and it runs through weight, breath and small physical signals long before anyone says a word.</p>
<h2>Most of it is physical, and that is fine</h2>
<p>You do not need to announce a boundary to hold one. Taking your weight back, putting a foot down, softening out of a lift, turning away: these are all complete sentences in the form's language, and an experienced partner reads them instantly. Words are welcome too. "Not that" or "slower" or "I'm done" said quietly mid-dance is normal and nobody will think twice about it.</p>
<h2>Leaving a dance is not rude</h2>
<p>Newcomers often stay in a dance they have stopped enjoying because leaving feels like an insult. It is not. Dances in a jam are short and fluid, people drift in and out of them constantly, and ending one is as ordinary as ending a conversation at a party. The only person who takes it personally is the one who should not have been dancing with you in the first place.</p>
<h2>What a good jam does about it</h2>
<p>A well-run jam does not leave this to chance. It opens with a short circle where the ground rules are said aloud, it names someone you can talk to if something is off, and it treats a partner who ignores a no as a problem for the whole room, not a private matter. When you are choosing a jam, whether the organiser does these things tells you more than anything else about it.</p>
<h2>If something feels wrong</h2>
<p>Leave the dance. Go to the edge. If it was more than awkward, tell the organiser that evening, not next week. You will not be the first person to raise it, and raising it is how a room stays safe for the next newcomer. The full ground rules for this site's own jam, and what you may always refuse, are on <a href="/safety-and-consent">safety and consent</a>; other common questions are on the <a href="/faq">FAQ</a>.</p>
""",
    ),
    (
        "blog-no-music",
        "/blog/why-there-is-no-music-at-a-jam",
        "Why There Is No Music at a Contact Improv Jam",
        "Why there is (usually) no music at a jam",
        "Silence at a contact improv jam is not an oversight: music covers the information the dance runs on, and dancing without it changes how you move and listen.",
        4,
        """
<p>The first thing many people notice at a jam is the quiet. No playlist, no beat to move to, sometimes no sound at all beyond breathing and the occasional thud of a body meeting the floor. It reads as awkward for about a quarter of an hour. Then it reads as the point.</p>
<h2>Music covers the information the dance runs on</h2>
<p>Contact Improvisation is built on listening to a partner's weight: the small shifts, the moment they commit, the instant before a lift resolves. That listening is partly through the skin and partly through the ears. Breath, the sound of a foot finding the floor, the change in how someone's weight settles: all of it is quieter than a track and most of it disappears under one. Take the music away and the room gets suddenly, usefully loud in a different way.</p>
<h2>A beat tells you what to do; silence asks</h2>
<p>Music, especially music with a pulse, organises movement for you. That is its pleasure and, in this form, its problem. Two people moving to the same beat are not really improvising together; they are both following the same third thing. Without it, the only timing available is the one you make between you, which is the whole exercise.</p>
<h2>It is not a rule</h2>
<p>Plenty of jams use a single ambient set, a live musician who plays with the room rather than at it, or music for one part of the evening and none for the rest. There is no authority in this form to forbid any of it. Silence is a default rather than a doctrine, and organisers choose it because it makes the dance easier to hear, not because sound is banned.</p>
<h2>What to do with the self-consciousness</h2>
<p>The quiet makes some newcomers feel watched, as if the absence of music leaves nothing to hide behind. Two things help. First, look around: nobody is listening to you, they are listening to whoever they are touching. Second, move slower than feels natural. Speed is what makes silence feel exposed. Slowness turns it into something closer to concentration.</p>
<p>Where the silence came from is part of the form's history, which is on the <a href="/history">history page</a>. How a jam runs from the moment you arrive is on <a href="/jams">jams and open practice</a>.</p>
""",
    ),
]


def _article_map():
    return {slug: a for a in ARTICLES for slug in [a[0]]}


def index():
    cards = "".join(
        f'<a class="card" href="{route}"><span class="tag">{mins} min read</span>'
        f"<h3>{h1}</h3><p>{desc}</p></a>"
        for slug, route, title, h1, desc, mins, body in ARTICLES
    )
    body = f"""
<div class="mci-view">
<p class="mci-eyebrow">Blog</p>
<h1 class="mci-h">NOTES FROM THE FLOOR</h1>
<p style="font-size:17px;line-height:1.75;color:var(--body);max-width:700px;margin:0 0 34px;">Short, practical pieces about Contact Improvisation: what a jam is actually like, how the weight-sharing works, how to fall, and how the room stays safe. Written for this site, for people who are new to it.</p>
<div class="grid">{cards}</div>
{band("Reading is the easy part", "The form makes sense in a room, about ten minutes in. Come to the Friday jam and find out.", [("See upcoming jams", "/events", "primary"), ("Your first jam, step by step", "/your-first-jam", "secondary")])}
</div>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            BLOG_ROUTE,
            "Blog | Miami Contact Improv",
            "Short, practical articles about Contact Improvisation for newcomers: the first jam, weight-sharing, falling safely, consent, and why jams are quiet.",
        ),
        schema.breadcrumb(BLOG_ROUTE, "Blog"),
        schema.item_list(
            BLOG_ROUTE + "#posts",
            "Miami Contact Improv blog",
            [(h1, schema.SITE + route, desc) for _s, route, _t, h1, desc, _m, _b in ARTICLES],
        ),
    )
    return page(
        "Contact Improv Blog | Notes for Newcomers",
        "Short, practical articles about Contact Improvisation for newcomers: the first jam, weight-sharing, how to fall safely, consent in the room, and why jams are quiet.",
        BLOG_ROUTE,
        body,
        jsonld=jsonld,
    )


def _article(slug):
    _s, route, title, h1, desc, mins, body_html = _article_map()[slug]
    body = f"""
<div class="mci-view">
<p class="mci-eyebrow"><a href="{BLOG_ROUTE}" style="color:inherit;">Blog</a> &middot; {mins} min read</p>
<h1 class="mci-h">{h1.upper()}</h1>
<div class="prose">{body_html}</div>
{band("New here? Come as you are.", "A short class, then an open jam. All levels, no partner needed.", [("See upcoming jams", "/events", "primary"), ("More from the blog", BLOG_ROUTE, "secondary")])}
{cite_block(f"Miami Contact Improv (2026). <em>{h1}</em>. miamicontactimprov.com. https://miamicontactimprov.com{route}")}
</div>
"""
    url = schema.SITE + route
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(route, title, desc, date_modified=PUBLISHED),
        schema.breadcrumb(route, h1),
        {
            "@type": "BlogPosting",
            "@id": url + "#post",
            "headline": h1,
            "description": desc,
            "url": url,
            "mainEntityOfPage": {"@id": url + "#page"},
            "datePublished": PUBLISHED,
            "dateModified": PUBLISHED,
            "author": {"@id": schema.ORG_ID},
            "publisher": {"@id": schema.ORG_ID},
            "image": schema.OG_IMAGE,
            "inLanguage": "en-US",
            "isPartOf": {"@id": schema.SITE + BLOG_ROUTE + "#posts"},
        },
    )
    return page(title, desc, route, body, jsonld=jsonld, og_type="article")


def first_jam():
    return _article("blog-first-jam")


def weight_sharing():
    return _article("blog-weight-sharing")


def falling():
    return _article("blog-falling")


def consent():
    return _article("blog-consent")


def no_music():
    return _article("blog-no-music")
