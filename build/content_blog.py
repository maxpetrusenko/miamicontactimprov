"""The blog: an index at /blog/ and original articles about Contact Improvisation.

Every article is written for this site (nothing copied), makes no local claim the
listings do not already make, and links into the library pages rather than repeating
them. Add an article by appending to ARTICLES; build/locales.py and build/build.py
carry a row per slug so it gets a canonical, a sitemap entry and a redirect rule.
"""

import datetime
import re

import schema
from shell import answer, band, cite_block, page

BLOG_ROUTE = "/blog/"
PUBLISHED = "2026-09-20"
# Articles published after the first batch carry their own date; the rest use PUBLISHED.
DATES = {
    "blog-miami-class": "2026-10-06",
    "blog-levels": "2026-10-06",
    "blog-small-dance": "2026-10-05",
    "blog-solo-practice": "2026-10-04",
}


# A one-paragraph answer shown at the top of each article and used as the BlogPosting
# abstract: self-contained, so a search or AI answer can quote it without the page.
ANSWERS = {
    "blog-miami-class": "The Friday contact improv class in Miami meets at Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, every Friday from 7:00 to 9:00 PM: a 45-minute guided class, then an open jam. A class is $20 booked online or $30 to $50 pay-what-you-can at the door. No partner or dance experience needed.",
    "blog-levels": "Contact improvisation moves between three levels: the floor, a middle level of kneeling and crouching, and standing. Classes start on the floor because it teaches how to give weight safely, and the core skill is travelling smoothly between levels by spiralling and rolling rather than pushing or dropping.",
    "blog-small-dance": "The small dance is a contact improvisation exercise in which you stand still and notice the tiny, constant reflexes that keep you balanced. It trains the sensitivity dancers use to feel a partner's weight through the point of contact, and it takes two or three minutes with no equipment.",
    "blog-solo-practice": "You can practise contact improvisation without a partner. Five solo exercises cover the core skills: rolling on the floor, going down and coming up without hands, the small dance, giving real weight to a wall, and rolling the spine. A few minutes a day makes the next jam noticeably easier.",
    "blog-first-jam": "At a first contact improv jam it helps to know five things: sitting out at the edge counts as taking part, nobody is watching you, the slow and quiet start is normal, you can leave any dance at any moment without a reason, and you will be physically closer to strangers than at a party.",
    "blog-weight-sharing": "Weight-sharing is the core skill of contact improvisation: one dancer gives part of their weight, the other receives it through the skeleton rather than the arms, and the point of contact rolls between bodies. The common beginner mistake is using muscle; the fix is to go lower, slower and closer to the floor.",
    "blog-falling": "In contact improvisation, falling safely is a skill: lower your centre so the fall is short, roll instead of stopping so the force spreads, breathe out on the way down, keep your feet available, and use spotters who stand ready to slow a fall that goes wrong.",
    "blog-consent": "Consent in contact improvisation is continuous and can be withdrawn at any moment: agreeing to one movement is not agreeing to the next. Boundaries are mostly communicated physically, leaving a dance is never rude, and a good jam states its ground rules aloud and names someone to talk to if something feels wrong.",
    "blog-no-music": "Most contact improv jams have no music because sound covers the small cues the dance depends on, such as breath and shifts in weight, and a beat organises movement for you instead of letting partners find their own timing. It is a common default, not a rule.",
}

KEYWORDS = {
    "blog-miami-class": ["contact improv Miami", "contact improvisation class Miami", "dance class Hallandale Beach", "Friday jam Miami", "Inner Motion Dance Studio"],
    "blog-levels": ["contact improvisation levels", "floor work", "contact improv technique", "contact improv Miami"],
    "blog-small-dance": ["small dance", "standing meditation dance", "contact improvisation exercise", "contact improv Miami"],
    "blog-solo-practice": ["contact improv solo practice", "contact improvisation exercises", "rolling", "contact improv Miami"],
}


def _date(slug):
    return DATES.get(slug, PUBLISHED)


def _date_label(slug):
    d = datetime.date.fromisoformat(_date(slug))
    return f"{d.strftime('%b')} {d.day}, {d.year}"

# slug, route, title, h1, description, read minutes, body html
ARTICLES = [
    (
        "blog-miami-class",
        "/blog/contact-improv-class-miami-what-to-expect",
        "Contact Improv Class in Miami: What to Expect on Friday",
        "Contact improv in Miami: what to expect on a Friday",
        "A newcomer's guide to the Friday contact improv class and jam in Miami at Inner Motion Dance Studio, Hallandale Beach: schedule, online vs door prices, how to book.",
        5,
        """
<p>If you have searched for a contact improv class in Miami, you have probably found a handful of listings and very little about what actually happens when you walk in. This is the plain version for the Friday class and open jam that this site runs, written for someone who has never done Contact Improvisation before.</p>
<h2>Where it is</h2>
<p>The class meets at Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009. That is the north edge of Miami: just past Aventura on US-1, east of Federal Highway and north of Hallandale Beach Boulevard. From downtown Miami it is the first city over the Broward county line; from Fort Lauderdale it is south of Hollywood. Directions and the rest of the logistics are on the <a href="/friday-jam">Friday jam page</a>.</p>
<h2>How the evening runs</h2>
<p>Every Friday from 7:00 to 9:00 PM. The first 45 minutes are a guided class: a warm-up from the floor and standing, the basics of giving and receiving weight, and how to roll out of a fall. Each week has a theme; this week's is moving through levels, from the floor to standing, which is covered in <a href="/blog/floor-to-standing-dancing-through-levels">floor to standing</a>. From 7:45 the room opens into a jam: free dancing, usually without music, where you can join a dance, dance alone, or sit at the edge and watch. Everything is optional, and the evening starts with a short circle where the ground rules are said out loud.</p>
<h2>What it costs</h2>
<p>A class is <strong>$20 when you book online</strong>. At the door it is <strong>$30 to $50, pay what you can</strong>, so booking ahead saves you at least $10. Online sales close two hours before class; after that the door price applies. Nobody is turned away from a first class over money. The full breakdown is on the <a href="/pricing">pricing page</a>.</p>
<h2>How to book</h2>
<p>You can buy a ticket on this site, register on Luma or Eventbrite, or book with ClassPass credits. The 10% code from the monthly email works at online checkout on this site. All of them are linked from the <a href="/events">events page</a>. You do not need to bring a partner, and you do not need any dance experience.</p>
<h2>What to bring</h2>
<p>Clothes you can roll on the floor in, with long sleeves and long legs if you can, since you will be in contact with the floor and with other people. No shoes on the dance floor; bare feet or socks. Leave off jewellery, zips and buckles that could catch a partner. Bring water. That is it.</p>
<h2>If you are nervous</h2>
<p>Most people are, the first time. Sitting out is participation, nobody is watching you, and you can leave any dance at any moment without a reason. Those three ideas are explained in <a href="/blog/five-things-before-your-first-jam">five things nobody tells you before your first jam</a>, and the full ground rules are on <a href="/safety-and-consent">safety and consent</a>. The class is taught in English, and Spanish speakers are welcome.</p>
""",
    ),
    (
        "blog-levels",
        "/blog/floor-to-standing-dancing-through-levels",
        "Floor to Standing: Dancing Through Levels in Contact Improv",
        "Floor to standing: dancing through levels",
        "Contact improv moves between the floor, a middle level and standing. Why the floor comes first, how dancers travel between levels, and what changes at each height.",
        5,
        """
<p>Watch a jam for ten minutes and you will see bodies at every height: two people rolling across the floor, a pair crouched low and folding over each other, a dancer briefly resting across someone's shoulders. That range is not decoration. Moving between levels, from the floor to standing and back, is one of the foundations of Contact Improvisation, and it is where a lot of the form's ease comes from.</p>
<h2>Why the floor comes first</h2>
<p>Most classes start on the ground, and not because it is gentle. The floor is the most reliable partner in the room. It takes all of your weight, all of the time, without negotiation. Rolling, sliding and spiralling on it teach you what giving weight actually feels like before you try giving it to a person. They also teach you that the floor is not somewhere you fall to but somewhere you can arrive, which changes how you dance everywhere above it.</p>
<h2>The middle level is where most of the dance happens</h2>
<p>Between lying down and standing is a wide band of positions: kneeling, crouching, on hands and knees, sitting back on the heels. Beginners tend to skip it, going straight from the floor to standing tall. Experienced dancers live there. A low centre makes you stable, keeps falls short, and puts your hips close to a partner's hips, which is where weight is easiest to share. Many of the lifts that look spectacular from the edge of the room start at this level with very little effort.</p>
<h2>Travelling between levels is the skill</h2>
<p>The interesting part is not any single height but the journey between them. Rising from the floor by spiralling up through the hips rather than pushing up with the arms. Coming down from standing by folding and rolling rather than dropping. Using a partner's back as a temporary floor on the way up, and letting them become the floor on your way down. When these transitions are smooth, the dance never has to stop and restart; it just changes altitude.</p>
<h2>What changes at each height</h2>
<p>On the floor, you have the most contact and the least momentum, so the dance is about listening and slow weight. At the middle level, you have stability and leverage, so the dance is about sharing weight and small lifts. Standing, you have speed and space, so the dance is about momentum and catching it. None of these is more advanced than the others. A good dance usually visits all three.</p>
<h2>Try it this week</h2>
<p>Next time you dance, notice which level you default to and spend five minutes deliberately somewhere else. If you always stand, stay low. If you always end up on the floor, practise the way up. The tools for both are in the <a href="/glossary">glossary</a>, falling safely between levels is covered in <a href="/blog/how-to-fall-without-getting-hurt">how to fall without getting hurt</a>, and the room to practise it in is the <a href="/friday-jam">Friday jam</a>.</p>
""",
    ),
    (
        "blog-small-dance",
        "/blog/the-small-dance-standing-still",
        "The Small Dance: What Standing Still Teaches You",
        "The small dance: what standing still teaches you",
        "The small dance is a contact improv exercise in standing still and noticing the constant tiny adjustments that keep you upright. What it is, how to do it, and why it matters.",
        4,
        """
<p>One of the oldest exercises in Contact Improvisation involves almost no visible movement at all. You stand, eyes soft or closed, and pay attention to what your body is doing to keep you upright. It is usually called the small dance, and it has been part of how the form is taught since its early years. It looks like nothing. It is one of the most useful things you can practise.</p>
<h2>Standing is not still</h2>
<p>Stand quietly for a minute and you will notice that you are never completely still. Your weight drifts slightly forward, then your ankles catch it. It shifts to one side and something in your hips adjusts. These corrections are tiny and constant, and they happen without you deciding anything. The small dance is the practice of noticing them: the reflexes that keep you balanced, running underneath your attention all the time.</p>
<h2>Why it matters in a duet</h2>
<p>When two people share weight, those same small reflexes are what make the dance work. A partner leaning on you is constantly adjusting, and so are you. If you can feel your own small dance, you can start to feel theirs through the point of contact: the moment they commit their weight, the moment they are about to move. That sensitivity is what lets a dance change direction without anyone leading it.</p>
<h2>How to do it</h2>
<p>Stand with your feet under your hips, knees soft, arms hanging. Let your eyes close or rest on the floor. Do not try to stand straight; let your skeleton hold you up rather than your muscles. Then simply notice. Where is your weight right now? What moved to catch it? Stay for two or three minutes. If your mind wanders, return to the soles of your feet. That is the whole exercise.</p>
<h2>Using it in a jam</h2>
<p>The small dance is a good way to arrive. Before you start dancing with anyone, spend a minute standing at the edge of the room and let your attention drop into your own balance. It also makes a gentle entry into a duet: stand back to back with a partner and do the small dance together, noticing how two sets of adjustments start to talk to each other. Often a dance grows out of that without either of you starting it.</p>
<p>For more ways to practise on your own between sessions, see <a href="/keep-practising">keep practising</a>. Where the exercise and the form came from is on the <a href="/history">history page</a>.</p>
""",
    ),
    (
        "blog-solo-practice",
        "/blog/solo-practice-between-jams",
        "Five Solo Exercises to Practise Between Contact Improv Jams",
        "Five things to practise on your own between jams",
        "You do not need a partner to get better at contact improv. Five short solo exercises for rolling, falling, the spine and balance that make your next jam easier.",
        5,
        """
<p>Contact Improvisation is a partner form, so it is easy to assume you can only practise it with a partner. In fact most of the skills that make a duet feel easy, the soft landings, the rolling spine, the trust in the floor, are solo skills. A few minutes a day on your own makes a noticeable difference by the next jam. None of these need more than a clear patch of floor.</p>
<h2>1. Rolling on the floor</h2>
<p>Lie down and roll slowly across the room, letting each part of your back meet the floor in turn. Do not push with your arms; let your head, then your shoulders, then your hips lead the turn. The goal is to feel the floor as something that receives you rather than something you bump into. It is the same quality you want when a partner receives your weight.</p>
<h2>2. Going down and coming up</h2>
<p>From standing, lower yourself to the floor as smoothly as you can, then come back up, without using your hands as props. Try spiralling: folding at the knees and hips and turning as you go, so you arrive on the side of a hip rather than on your knees. Repeat it ten times, slower each time. This is the solo version of moving through levels, and it is how you learn to fall without stopping.</p>
<h2>3. The small dance</h2>
<p>Stand still for two minutes and notice the constant small adjustments that keep you upright. It trains the sensitivity you use to feel a partner's weight. There is a longer description in <a href="/blog/the-small-dance-standing-still">the small dance</a>.</p>
<h2>4. A wall as a partner</h2>
<p>Lean your back, then your side, then your shoulder against a wall and practise giving it real weight, enough that you would have to move if it disappeared. Then roll your point of contact along it, from shoulder blade to hip, without losing the connection. A wall is a very patient partner, and it is honest: you can feel straight away whether you are really giving weight or just leaning.</p>
<h2>5. Rolling the spine</h2>
<p>Standing, let your head drop forward and roll down through your spine, one vertebra at a time, until you are hanging forward with soft knees. Then roll back up the same way. Lifts and weight-sharing ask the spine to curve and support at the same time, and this keeps it supple and familiar. Do it slowly and breathe out on the way down.</p>
<p>If any of these feels strange, that is normal; most of them feel strange the first week. More practice ideas are on <a href="/keep-practising">keep practising</a>, the mechanics behind them are in <a href="/blog/weight-sharing-explained">weight-sharing, explained</a>, and the place to try them with other people is the <a href="/friday-jam">Friday jam</a>.</p>
""",
    ),
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
        f'<a class="card" href="{route}"><span class="tag">{_date_label(slug)} &middot; {mins} min read</span>'
        f"<h3>{h1}</h3><p>{desc}</p></a>"
        for slug, route, title, h1, desc, mins, body in ARTICLES
    )
    body = f"""
<div class="mci-view">
<p class="mci-eyebrow">Blog</p>
<h1 class="mci-h">NOTES FROM THE FLOOR</h1>
<p style="font-size:17px;line-height:1.75;color:var(--body);max-width:700px;margin:0 0 34px;">Short, practical pieces about Contact Improvisation in Miami: what the Friday class is like, how weight-sharing works, how to fall, what to practise at home, and how the room stays safe. Written for this site, for people who are new to it.</p>
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
<p class="mci-eyebrow"><a href="{BLOG_ROUTE}" style="color:inherit;">Blog</a> &middot; {_date_label(slug)} &middot; {mins} min read</p>
<h1 class="mci-h">{h1.upper()}</h1>
{answer(ANSWERS[slug]) if slug in ANSWERS else ""}
<div class="prose">{body_html}</div>
{band("New here? Come as you are.", "A short class, then an open jam. All levels, no partner needed.", [("See upcoming jams", "/events", "primary"), ("More from the blog", BLOG_ROUTE, "secondary")])}
{cite_block(f"Miami Contact Improv (2026). <em>{h1}</em>. miamicontactimprov.com. https://miamicontactimprov.com{route}")}
</div>
"""
    url = schema.SITE + route
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(route, title, desc, date_modified=_date(slug)),
        schema.breadcrumb(route, h1),
        {
            "@type": "BlogPosting",
            "@id": url + "#post",
            "headline": h1,
            "description": desc,
            "url": url,
            "mainEntityOfPage": {"@id": url + "#page"},
            "datePublished": _date(slug),
            "dateModified": _date(slug),
            "author": {"@id": schema.ORG_ID},
            "publisher": {"@id": schema.ORG_ID},
            "image": schema.OG_IMAGE,
            "inLanguage": "en-US",
            "isPartOf": {"@id": schema.SITE + BLOG_ROUTE + "#posts"},
            "articleSection": "Contact Improvisation",
            "wordCount": len(re.sub(r"<[^>]+>", " ", body_html).split()),
            "about": {"@type": "Thing", "name": "Contact improvisation",
                      "sameAs": "https://en.wikipedia.org/wiki/Contact_improvisation"},
            "spatialCoverage": {"@type": "City", "name": "Miami",
                                "containedInPlace": {"@type": "State", "name": "Florida"}},
            "keywords": ", ".join(KEYWORDS.get(slug, ["contact improvisation", "contact improv Miami"])),
            **({"abstract": re.sub(r"<[^>]+>", "", ANSWERS[slug])} if slug in ANSWERS else {}),
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


def levels():
    return _article("blog-levels")


def small_dance():
    return _article("blog-small-dance")


def solo_practice():
    return _article("blog-solo-practice")


def miami_class():
    return _article("blog-miami-class")
