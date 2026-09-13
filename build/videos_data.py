"""The video room. Every entry below was embed-verified against YouTube oEmbed (HTTP 200).

Verification gate used (run it again, do not trust memory):
  curl -s -o /dev/null -w '%{http_code}' \
    "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<ID>&format=json"

Nothing here is downloaded, re-cut or re-hosted. Each film plays from the channel that
made it, through the platform that owns it.

upload dates are deliberately absent: they could not be verified from an authoritative
endpoint at build time, and an unverified date is worse than no date.
"""

import html
import schema

# id, title, channel, year, category, note
VIDEOS = [
    # ---- foundations
    ("9FeSDsmIeHA", "Contact Improvisation 1972", "klubki", 1972, "foundations",
     "Early footage from the year the form was made. Worth watching for how little it looks like a performance."),
    ("uj8lhBjf_DQ", "Originators of Contact Dance / Improvisation 1972", "Randy Om", 1972, "foundations",
     "Archive material of the first generation of dancers, including Steve Paxton and Nancy Stark Smith."),
    ("H8JiB2Nv5Qo", "Contact Improvisation: a couple of basic exercises", "OKI", 2019, "foundations",
     "A short, plain demonstration of the underlying weight exchange, useful before your first session."),

    # ---- duets
    ("NGf03Yg6fM0", "Contact Improvisation: the art of jamming", "Sasha Dodo", 2019, "duets",
     "Sasha Dodo and Dolores Dewhurst Marks in a sustained duet that stays close to the floor and to listening."),
    ("ED8hNoulZv4", "Contact Improvisation: moments of practice", "BeingMotion \u2014 Irene Sposetti", 2020, "duets",
     "Irene Sposetti and Johan Nilsson. Slow, unshowy, structurally clear. The clearest picture of what the form feels like."),
    ("lSJQs3SG8KU", "Contact Improv duet", "Tiina J\u00e4\u00e4sk\u00f6", 2021, "duets",
     "Tiina J\u00e4\u00e4sk\u00f6 and Jordi Ramon, working the line between stillness and momentum."),
    ("f1o6FJL8bxM", "Contact Improvisation duet with Ming Tsai and Dolores Dewhurst", "Ming Tsai", 2020, "duets",
     "A calm, technical duet with a strong emphasis on the rolling point of contact."),
    ("1f_KhhunP3o", "Contact Improvisation duet: Tamas Baku and Sabine Parzer", "Sabine Parzer", 2018, "duets",
     "Excerpts from a longer duet, showing how much of the work happens below the hips."),
    ("zQRF2sLK1vY", "Contact Improvisation: Blake Nellis and Brando at Earthdance", "Aaron Brandes (Brando)", 2016, "duets",
     "Filmed at Earthdance, the long-running CI centre in Massachusetts. Athletic, playful, clearly unhurried."),
    ("65S9nuRzK4Q", "Moab Jam: Karen Nelson, Neige Christenson and Bradley Ellis", "Sharing Weight", 2019, "duets",
     "Three of the form's most experienced dancers in an outdoor jam. Useful for seeing how a trio works without a plan."),

    # ---- festivals
    ("y3rTq00yJ8E", "25th contactfestival freiburg", "contactfestfreiburg", 2022, "festivals",
     "One of Europe's largest annual CI gatherings, filmed across a full festival."),
    ("dE0AEE0zGmU", "Contact Improvisation, Goa Contact Festival", "Forgotten Land", 2018, "festivals",
     "Beach, heat, and a very large jam. Close to what a South Florida outdoor session could look like."),
    ("MUugUjn4sEo", "Contact Impro Festival in Tirol", "MOTION MODE DANCE THEATRE", 2021, "festivals",
     "Mountain festival footage with teaching excerpts and open jam."),
    ("yyaHk7KN9bY", "Poland Contact Improvisation Festival, Warsaw Flow", "szimi82", 2012, "festivals",
     "A well-shot record of the festival jam format: an empty room slowly filling with dancing."),
    ("n0V774lMnv0", "Italy contact festival: Artem Markov and Cleo Laigret", "Artem Markov", 2018, "festivals",
     "Festival stage work, showing the more performative end of what the practice can produce."),

    # ---- documentary
    ("u9AhpFxfEfs", "What happens in a Contact Improvisation jam?", "ci rollingpoint", 2016, "documentary",
     "Part of a documentary series on the form. Answers the question in the title directly."),
    ("hlIRjfto7o0", "Life lessons learned through Contact Improvisation", "TEDx Talks", 2019, "documentary",
     "Gregory Catellier and Kristin O'Neal on what the practice teaches off the floor."),
    ("_82Od5NM4LI", "Steve Paxton: Talking Dance", "Walker Art Center", 2014, "documentary",
     "The originator of the form in conversation. The primary source for why it was built this way."),
    ("SUthCFdF1FE", "Steve Paxton: Drafting Interior Techniques", "Emma B", 2018, "documentary",
     "A television documentary on Paxton's composition and improvisation work."),
    ("12j9JxDGlE4", "Steve Paxton and Simone Forti: In Conversation", "CalArtsREDCAT", 2011, "documentary",
     "Two of the people who reshaped what dance could be, talking through it."),
    ("VDBbyypWLJM", "Steve Paxton about dancing", "klubki", 2015, "documentary",
     "Short, direct, and unusually good on the discipline of standing still."),
]

CATEGORIES = [
    ("foundations", "Start here", "If you have never seen this dance, watch these three first."),
    ("duets", "Duets", "Sustained two-person work, from near-stillness to fully airborne."),
    ("festivals", "Festivals and jams", "What a large gathering of CI dancers looks like when the room fills up."),
    ("documentary", "Documentary and the originators", "The people who made the form, explaining it in their own words."),
]

# Verified as a muted looping background embed. Cinematic, unshowy, no talking heads.
HERO_VIDEO_ID = "ED8hNoulZv4"

EMBED = "https://www.youtube-nocookie.com/embed/{id}?rel=0&modestbranding=1"


def by_id(vid):
    for v in VIDEOS:
        if v[0] == vid:
            return v
    raise KeyError(vid)


def _figure(v):
    vid, title, channel, year, _cat, note = v
    return (
        f'<figure><div class="frame">'
        f'<iframe src="{EMBED.format(id=vid)}" title="{html.escape(title)} \u2014 {html.escape(channel)}" '
        f'loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        f'allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>'
        f"</div><figcaption><strong>{html.escape(title)}</strong>"
        f"<span>{html.escape(channel)} &middot; {year}</span>"
        f"<p>{html.escape(note)}</p></figcaption></figure>"
    )


def gallery():
    if not VIDEOS:
        raise RuntimeError("VIDEOS is empty. The video room must not ship without verified entries.")
    out = []
    for slug, title, blurb in CATEGORIES:
        items = [v for v in VIDEOS if v[4] == slug]
        if not items:
            continue
        out.append(
            f'<div class="prose"><h2 id="{slug}">{title}</h2><p>{blurb}</p></div>'
            f'<div class="media-grid">{"".join(_figure(v) for v in items)}</div>'
        )
    return "".join(out)


def credits():
    rows = sorted({(v[2], f"https://www.youtube.com/watch?v={v[0]}") for v in VIDEOS})
    lis = "".join(
        f'<li><a href="{html.escape(u)}" rel="noopener nofollow">{html.escape(c)}</a></li>'
        for c, u in rows
    )
    return (
        '<div class="prose"><h2>Credits</h2>'
        "<p>Every film on this page belongs to the channel that made it and plays through that "
        "channel's own player on the platform that hosts it. Nothing here is downloaded, re-cut or "
        "re-hosted by this site. If you own one of these and would rather it were not embedded, "
        '<a href="/about#submit">say so</a> and it comes down the same day.</p>'
        f"<ul>{lis}</ul></div>"
    )


def schema_list():
    if not VIDEOS:
        return None
    entries = [
        {
            "title": v[1],
            "description": v[5],
            "thumbnail": f"https://i.ytimg.com/vi/{v[0]}/hqdefault.jpg",
            "embed": EMBED.format(id=v[0]),
            "url": f"https://www.youtube.com/watch?v={v[0]}",
            "channel": v[2],
        }
        for v in VIDEOS
    ]
    return schema.video_objects(entries)
