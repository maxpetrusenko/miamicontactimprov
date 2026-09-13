"""The video room.

Every entry below was embed-verified against the platform's own oEmbed endpoint
(HTTP 200) and, where an uploadDate is present, that date was read from the
video's own watch page rather than guessed. Nothing here is downloaded, re-cut
or re-hosted: each film plays through the platform that hosts it.

Re-verify a candidate before adding it:

    curl -s -o /dev/null -w '%{http_code}\\n' \\
      "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<ID>&format=json"

200 -> embeddable. 401/403 -> embedding disabled by the owner. Do not add those.
Vimeo additionally reports domain_status_code: 403 in the oEmbed payload when the
owner has restricted embedding to specific domains, even though the HTTP status is
200. Check the payload, not just the status.
"""

import html
import schema

# id, platform, title, channel, upload_date, duration, category, note
VIDEOS = [
    # ---------------- start here
    ("H8JiB2Nv5Qo", "youtube", "Contact Improvisation: a couple of basic exercises",
     "OKI", "2016-09-18", "9:37", "foundations",
     "The plainest demonstration in the set. Two dancers working through the underlying weight exchange, "
     "useful the week before your first session."),
    ("9FeSDsmIeHA", "youtube", "Contact Improvisation 1972",
     "klubki", "2011-09-03", "9:31", "foundations",
     "Archive material from the founding year, uploaded decades later. Watch it for how little it "
     "resembles a performance and how much it resembles standing around until something happens."),
    ("u9AhpFxfEfs", "youtube", "What happens in a Contact Improvisation jam?",
     "ci rollingpoint", "2022-11-30", "3:18", "foundations",
     "Part of a documentary series, and it answers the question in its own title directly."),

    # ---------------- duets
    ("q4wUEiHowSU", "youtube", "Embraced",
     "BeingMotion \u2014 Irene Sposetti", "2016-04-11", "4:00", "duets",
     "A single continuous duet, shot as film rather than documentation. No interview, no title cards, "
     "no talking. The cleanest picture on YouTube of what sustained contact feels like from the inside."),
    ("ED8hNoulZv4", "youtube", "Contact Improvisation: moments of practice",
     "BeingMotion \u2014 Irene Sposetti", "2011-11-07", "5:51", "duets",
     "Irene Sposetti and Johan Nilsson, cinema-verite, natural light, long takes. Slow, unshowy, "
     "structurally clear."),
    ("Ltq6y06E8ew", "youtube", "the play of weight",
     "Neige Christenson", "2009-04-29", "6:17", "duets",
     "Low camera, rolling bodies, almost no event. Still one of the most quoted records of the form "
     "as a physical conversation rather than a display."),
    ("NGf03Yg6fM0", "youtube", "Contact Improvisation: the art of jamming",
     "Sasha Dodo", "2021-01-31", "3:42", "duets",
     "Sasha Dodo and Dolores Dewhurst Marks. Colour-graded, tightly framed, strong lifts and "
     "counterbalance, no spoken content."),
    ("zQRF2sLK1vY", "youtube", "Blake Nellis and Brando at Earthdance",
     "Aaron Brandes (Brando)", "2010-05-26", "6:29", "duets",
     "Filmed at Earthdance, the long-running CI centre in Massachusetts. Handheld, unhurried, "
     "clearly a good session rather than a performance."),
    ("_qnzKHrxKbA", "youtube", "Lifting: contact and improvisation",
     "Xandy Liberato", "2015-11-08", "6:30", "duets",
     "Close technical footage of lift mechanics and counterweighting. Watch this one if you have been "
     "told you are too heavy or too light to fly."),
    ("YxLT9OELURo", "youtube", "Shaken",
     "Karl Frost", "2007-02-07", "9:31", "duets",
     "Body Research performance work. Movement-led and experimental rather than instructional."),

    # ---------------- festivals and jams
    ("yyaHk7KN9bY", "youtube", "Poland Contact Improvisation Festival: Warsaw Flow 2012, jam",
     "szimi82", "2012-07-25", "3:54", "festivals",
     "A festival jam filmed as it fills up. Multiple duets, ambient music, no narration. This is the "
     "shape a busy room takes."),
    ("dE0AEE0zGmU", "youtube", "Contact Improvisation, Goa Contact Festival, India",
     "Forgotten Land", "2013-08-17", "31:44", "festivals",
     "Thirty-one minutes of beach and studio footage from a large tropical festival. The closest thing "
     "here to what a South Florida outdoor session could look like, at scale."),
    ("X-7izu2QpqA", "youtube", "Opening jam and guided warm-up with Steve Batts",
     "virginia negru", "2017-10-15", "11:48", "festivals",
     "A complete opening: the warm-up that a first-timer should watch before attending a jam, followed "
     "by the jam itself."),
    ("azDakHrdzpw", "youtube", "Teachers' performance, Kyiv Contact Improvisation Festival",
     "Yevhen Titov", "2014-06-01", "50:03", "festivals",
     "Senior teachers performing for a festival audience. Shows the performative end of what the "
     "practice can produce when experienced dancers push it."),
    ("TL1i9BhMQrE", "youtube", "Contact Improvisation at Summer Dance",
     "Art of Contact", "2023-05-22", "1:01", "festivals",
     "One minute, outdoors, no context needed. The best short clip here to send someone who has "
     "never seen the form and only has a moment."),

    # ---------------- documentary and the originators
    ("v6Pt0OXK7es", "youtube", "The poetics of touch: Nancy Stark Smith, a pathway into contact improvisation",
     "visioniarborescenti", "2013-04-24", "24:41", "documentary",
     "A documentary on Stark Smith and on touch as the medium. Contains interview material as well as "
     "dancing, so it is an editorial watch rather than a background loop."),
    ("XGIlU89MgIQ", "youtube", "Nancy Stark Smith and Karen Nelson (1990)",
     "whitefiredancer", "2020-05-04", "16:37", "documentary",
     "Vintage footage of two of the earliest practitioners, uploaded in 2020. Silent, archival, and "
     "the best evidence of how the form looked before it had a name people recognised."),
    ("XrUeYbUmhQA", "youtube", "Steve Paxton",
     "contactimprovdoc", "2008-07-28", "6:39", "documentary",
     "Archive clip of the form's originator from the contactimprovdoc channel. Low-resolution and "
     "quiet, and the primary source for why any of this exists."),
    ("hlIRjfto7o0", "youtube", "Life lessons learned through Contact Improvisation",
     "TEDx Talks", "2023-05-23", "15:13", "documentary",
     "Gregory Catellier and Kristin O'Neal on what the practice teaches off the floor. The best single "
     "answer to a sceptical relative asking what this is for."),

    # ---------------- Vimeo
    ("162251068", "vimeo", "Elske Seidel and Joerg Hassmann: Contact Improvisation duet",
     "Katelyn Stiles", "", "7:11", "duets",
     "Full duet documentation by a well-known Berlin pair. Clean framing, music-led, no narration. "
     "Embedding is open on Vimeo, which is not always the case for dance film."),
    ("143397945", "vimeo", "Silkies",
     "Dan Farberoff", "", "4:38", "duets",
     "A shot dance film rather than documentation. Painterly, made for a screen, worth watching for "
     "what contact work looks like when it is composed for camera."),
    ("223688821", "vimeo", "CIPD",
     "Andrew Wass", "", "9:58", "festivals",
     "Performance documentation, one of the few higher-production CI performance uploads still public "
     "and openly embeddable on Vimeo."),
]

CATEGORIES = [
    ("foundations", "Start here", "If you have never seen this dance, watch these three first."),
    ("duets", "Duets", "Sustained two-person work, from near-stillness to fully airborne."),
    ("festivals", "Festivals and jams", "What a gathering of CI dancers looks like when the room fills up."),
    ("documentary", "Documentary and the originators", "The people who made the form, in their own words."),
]

# Embed-verified as a muted looping background. Cinematic, no talking heads, tolerant
# of being cropped to a band, and nothing in it depends on audio.
HERO_VIDEO_ID = "q4wUEiHowSU"

EMBED = {
    "youtube": "https://www.youtube-nocookie.com/embed/{id}?rel=0&modestbranding=1",
    "vimeo": "https://player.vimeo.com/video/{id}?byline=0&portrait=0&title=0",
}
WATCH = {
    "youtube": "https://www.youtube.com/watch?v={id}",
    "vimeo": "https://vimeo.com/{id}",
}
THUMB = {
    "youtube": "https://i.ytimg.com/vi/{id}/hqdefault.jpg",
    # Vimeo thumbnails are per-video CDN paths, confirmed live from the oEmbed payload.
    "vimeo": "https://i.vimeocdn.com/video/{id}",
}
VIMEO_THUMBS = {
    "162251068": "https://i.vimeocdn.com/video/564689283-963e12a262a1946958eab4c59ee67d3465675aa91c9d5e25438755169dfc9",
    "143397945": "https://i.vimeocdn.com/video/540978917-075ab990a37cb4869524285eefaace6173f21e5d2f53d269c7227dbcc859f",
    "223688821": "https://i.vimeocdn.com/video/642621302-c050b5cec435b81eaffeb93ad82215d059ac177e5c9e7928cef5bdabb2f8e",
}


def thumbnail(v):
    vid, platform = v[0], v[1]
    if platform == "vimeo":
        return VIMEO_THUMBS.get(vid, "")
    return THUMB[platform].format(id=vid)


def embed_url(v):
    return EMBED[v[1]].format(id=v[0])


def watch_url(v):
    return WATCH[v[1]].format(id=v[0])


def _figure(v):
    vid, platform, title, channel, _date, duration, _cat, note = v
    return (
        f'<figure><div class="frame">'
        f'<iframe src="{embed_url(v)}" title="{html.escape(title)} \u2014 {html.escape(channel)}" '
        f'loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        f'allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>'
        f"</div><figcaption><strong>{html.escape(title)}</strong>"
        f"<span>{html.escape(channel)} &middot; {duration} &middot; {platform}</span>"
        f"<p>{html.escape(note)}</p></figcaption></figure>"
    )


def gallery():
    if not VIDEOS:
        raise RuntimeError("VIDEOS is empty. The video room must not ship without verified entries.")
    out = []
    for slug, title, blurb in CATEGORIES:
        items = [v for v in VIDEOS if v[6] == slug]
        if not items:
            continue
        out.append(
            f'<div class="prose"><h2 id="{slug}">{title}</h2><p>{blurb}</p></div>'
            f'<div class="media-grid">{"".join(_figure(v) for v in items)}</div>'
        )
    return "".join(out)


def credits():
    rows = sorted({(v[2], watch_url(v)) for v in VIDEOS})
    lis = "".join(
        f'<li><a href="{html.escape(u)}" rel="noopener nofollow">{html.escape(c)}</a></li>'
        for c, u in rows
    )
    return (
        '<div class="prose"><h2>Credits</h2>'
        "<p>Every film here belongs to the channel that made it and plays through that channel's own "
        "player on the platform that hosts it. Nothing is downloaded, re-cut or re-hosted by this site. "
        "If you own one of these and would rather it were not embedded, "
        '<a href="/about#submit">say so</a> and it comes down the same day.</p>'
        f"<ul>{lis}</ul></div>"
    )


def schema_list():
    if not VIDEOS:
        return None
    entries = []
    for v in VIDEOS:
        vid, platform, title, channel, upload, _duration, _cat, note = v
        e = {
            "title": title,
            "description": note,
            "embed": embed_url(v),
            "url": watch_url(v),
            "channel": channel,
        }
        if thumbnail(v):
            e["thumbnail"] = thumbnail(v)
        if upload:
            e["upload"] = upload
        entries.append(e)
    return schema.video_objects(entries)
