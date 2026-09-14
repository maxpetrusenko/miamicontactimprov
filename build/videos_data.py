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

OWNERSHIP. This module holds two different things and they are never mixed:

  VIDEOS  other people's films. Embedded from the platform that hosts them, credited
          to the channel by name, and never described as this site's work.
  OWNED   films this jam shot and hosts itself. The only entries that may carry this
          site's own attribution in the page or in the VideoObject.

A third-party film is never re-hosted, re-cut or re-uploaded here, and it never gets
this site's name on it. A film of ours is never embedded from someone else's player.
"""

import html
import pathlib

import schema

# id, platform, title, channel, upload_date, duration, category, note
VIDEOS = [
    # ---------------- start here
    ("H8JiB2Nv5Qo", "youtube", "Contact Improvisation: a couple of basic exercises",
     "OKI", "2016-09-18", "9:37", "foundations",
     "The plainest demonstration in the set. Two dancers working through the underlying weight sharing, "
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

# ------------------------------------------------------------------ Spanish (es)
# The room's prose is this site's own writing, so it is translated. What is NOT
# translated: every film TITLE, every channel name and every platform string, because
# those are quoted from the platform that publishes the film — translating a quoted
# title would be inventing a citation. Keyed by video id so a new film cannot be added
# without its note being written for both locales (the missing-key fallback below is the
# English note, and a Spanish page carrying an English note is a defect, not a default).
ES_NOTES = {
    "H8JiB2Nv5Qo": "La demostración más llana del conjunto. Dos personas trabajando el compartir peso "
                   "de base, útil la semana antes de tu primera sesión.",
    "9FeSDsmIeHA": "Material de archivo del año fundacional, subido décadas después. Míralo por lo poco "
                   "que se parece a una actuación y lo mucho que se parece a estar de pie hasta que "
                   "pasa algo.",
    "u9AhpFxfEfs": "Parte de una serie documental, y responde a la pregunta de su propio título "
                   "directamente.",
    "q4wUEiHowSU": "Un dúo único y continuo, rodado como cine y no como documentación. Sin entrevista, "
                   "sin rótulos, sin hablar. La imagen más limpia que hay en YouTube de cómo se siente "
                   "el contacto sostenido desde dentro.",
    "ED8hNoulZv4": "Irene Sposetti y Johan Nilsson, cine directo, luz natural, planos largos. Lento, sin "
                   "lucimiento, estructuralmente claro.",
    "Ltq6y06E8ew": "Cámara baja, cuerpos rodando, casi ningún acontecimiento. Sigue siendo uno de los "
                   "registros más citados de la forma como conversación física y no como exhibición.",
    "NGf03Yg6fM0": "Sasha Dodo y Dolores Dewhurst Marks. Etalonado, encuadre cerrado, levantamientos "
                   "fuertes y contrapeso, sin contenido hablado.",
    "zQRF2sLK1vY": "Rodado en Earthdance, el centro de IC de larga trayectoria en Massachusetts. Cámara "
                   "en mano, sin prisa, claramente una buena sesión y no una actuación.",
    "_qnzKHrxKbA": "Material técnico cercano sobre la mecánica del levantamiento y el contrapeso. Mira "
                   "este si te han dicho que eres demasiado pesado o demasiado ligero para volar.",
    "YxLT9OELURo": "Trabajo de actuación de Body Research. Guiado por el movimiento y experimental, no "
                   "instructivo.",
    "yyaHk7KN9bY": "Una jam de festival filmada mientras se llena. Varios dúos, música ambiental, sin "
                   "narración. Esta es la forma que toma una sala llena.",
    "dE0AEE0zGmU": "Treinta y un minutos de playa y estudio en un festival tropical grande. Lo más "
                   "parecido que hay aquí a lo que podría ser una sesión al aire libre en el sur de "
                   "Florida, a gran escala.",
    "X-7izu2QpqA": "Una apertura completa: el calentamiento que alguien que viene por primera vez "
                   "debería ver antes de asistir a una jam, y después la jam misma.",
    "azDakHrdzpw": "Profesorado veterano actuando para un público de festival. Muestra el extremo "
                   "performativo de lo que la práctica puede producir cuando quien baila tiene "
                   "experiencia y la lleva al límite.",
    "TL1i9BhMQrE": "Un minuto, al aire libre, sin necesidad de contexto. El mejor clip corto de aquí "
                   "para mandárselo a alguien que nunca ha visto la forma y solo tiene un momento.",
    "v6Pt0OXK7es": "Un documental sobre Stark Smith y sobre el tacto como medio. Incluye material de "
                   "entrevista además de baile, así que es para verlo con atención y no de fondo.",
    "XGIlU89MgIQ": "Material de archivo de dos de las primeras practicantes, subido en 2020. Mudo, de "
                   "archivo, y la mejor prueba de cómo se veía la forma antes de tener un nombre que "
                   "la gente reconociera.",
    "XrUeYbUmhQA": "Clip de archivo del creador de la forma, del canal contactimprovdoc. Baja resolución "
                   "y silencioso, y la fuente primaria de por qué existe todo esto.",
    "hlIRjfto7o0": "Gregory Catellier y Kristin O'Neal sobre lo que la práctica enseña fuera de la sala. "
                   "La mejor respuesta única a un familiar escéptico que pregunta para qué sirve esto.",
    "162251068": "Documentación completa de un dúo por una pareja berlinesa conocida. Encuadre limpio, "
                 "guiado por la música, sin narración. En Vimeo la incrustación está abierta, cosa que "
                 "no siempre ocurre con el cine de danza.",
    "143397945": "Una película de danza rodada, no documentación. Pictórica, hecha para una pantalla, "
                 "merece verse por cómo se ve el trabajo de contacto cuando se compone para cámara.",
    "223688821": "Documentación de una actuación, una de las pocas subidas de actuación de IC con "
                 "producción más alta que sigue siendo pública y abiertamente incrustable en Vimeo.",
}

ES_CATEGORIES = [
    ("foundations", "Empieza por aquí", "Si nunca has visto esta danza, mira estos tres primero."),
    ("duets", "Dúos", "Trabajo sostenido de dos personas, desde la casi quietud hasta volar del todo."),
    ("festivals", "Festivales y jams", "Cómo se ve un encuentro de bailarines de IC cuando la sala se llena."),
    ("documentary", "Documental y los orígenes", "Las personas que hicieron la forma, con sus propias palabras."),
]

# Notes and link labels for the pieces in production, keyed by slug. Titles stay as
# published: they are the working titles of the films themselves.
ES_PLANNED = {
    "what-actually-happens-at-a-contact-improv-jam": (
        "rodado en una jam en Miami, que es el único filme de contact improv rodado en Miami "
        "que va a existir en cualquier parte", "/es/jams", "la página de jams"),
    "contact-improvisation-for-beginners-the-first-20-minutes": (
        "el calentamiento y los primeros ejercicios que recibe de verdad alguien que empieza",
        "/es/tu-primera-jam", "el recorrido de la primera jam"),
    "rolling-point-of-contact-weight-sharing-floorwork": (
        "la técnica que hay debajo del baile, mostrada lo bastante despacio para copiarla",
        "/es/glosario#compartir-peso", "la definición de compartir peso"),
    "is-contact-improv-sexual": (
        "la pregunta que frena a la gente para asistir, respondida sin rodeos",
        "/es/seguridad-y-consentimiento", "seguridad y consentimiento"),
    "the-small-dance": (
        "la práctica de pie, ligada a la definición que este sitio ya tiene",
        "/es/glosario#small-dance", "la definición del glosario"),
}

ES_SECTION = {
    "reference_heading": "Ver como referencia",
    "credits_heading": "Quién hizo los filmes de esta sección",
    "production_heading": "Qué estamos filmando",
    "owned_heading": "Nuestros propios filmes",
    "by": "de",
}

# Embed-verified as a muted looping background. Cinematic, no talking heads, tolerant
# of being cropped to a band, and nothing in it depends on audio.
HERO_VIDEO_ID = "q4wUEiHowSU"

# ------------------------------------------------------------------ our own films
# EMPTY, and that is the honest state: this jam has not shot a film yet. An entry
# here is a claim that a finished file exists and is hosted on this domain, so an
# entry is added only once the piece is shot, cut and published.
#
# Shape: (id, title, duration, filmedOn, location)
#   id        slug. Two files must be committed for it, both served from this
#             domain: site/media/<id>.mp4 and site/media/<id>-poster.jpg. The film
#             is ours, so it plays from our page and our player (contentUrl), not
#             from someone else's embed.
#   title     the piece's own title, as it reads on the page.
#   duration  "m:ss", read off the finished file. Never estimated, never rounded.
#   filmedOn  "YYYY-MM-DD", the day it was shot. Not the publish date.
#   location  where it was shot, e.g. "Miami, FL".
OWNED = []
OWNED_TUPLE_SHAPE = "(id, title, duration, filmedOn, location)"
OWNED_MEDIA_DIR = "media"
OWNED_EXT = ".mp4"
OWNED_POSTER_SUFFIX = "-poster.jpg"

# The films in production, in the brief's priority order. While OWNED is empty the
# page tells the reader these are planned, not available. A slug that appears in
# OWNED drops out of this list, so the same film is never both promised and shown.
# Shape: (slug, title, note, link, link_label). link is an on-site path the piece
# connects to, or "" when it connects to nothing here.
PLANNED = [
    ("what-actually-happens-at-a-contact-improv-jam",
     "What actually happens at a contact improv jam",
     "shot at a jam in Miami, which is the only Miami-shot contact improv film that "
     "will exist anywhere", "/jams", "the jams page"),
    ("contact-improvisation-for-beginners-the-first-20-minutes",
     "Contact improvisation for beginners: the first 20 minutes",
     "the warm-up and the first exercises a beginner is actually given",
     "/your-first-jam", "the first-jam walkthrough"),
    ("rolling-point-of-contact-weight-sharing-floorwork",
     "Rolling point of contact, weight sharing, floorwork",
     "the technique underneath the dancing, shown slowly enough to copy",
     "/glossary#weight-sharing", "the weight sharing definition"),
    ("is-contact-improv-sexual",
     "Is contact improv sexual?",
     "the question that stops people attending, answered plainly",
     "/safety-and-consent", "safety and consent"),
    ("the-small-dance",
     "The small dance",
     "the standing practice, tied to the definition this site already owns",
     "/glossary#small-dance", "the glossary definition"),
]

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


def embed_count():
    """Every film the room carries: ours plus the credited third-party embeds.

    The page title's bracket count is built from this, so the number in the SERP
    cannot drift away from the number of films actually on the page.
    """
    return len(OWNED) + len(VIDEOS)


# --------------------------------------------------------------------- our films

def _repo_root():
    return pathlib.Path(__file__).resolve().parent.parent


def owned_media_path(o):
    """The film as committed: what the deploy actually serves."""
    return _repo_root() / "site" / OWNED_MEDIA_DIR / f"{o[0]}{OWNED_EXT}"


def owned_poster_path(o):
    return _repo_root() / "site" / OWNED_MEDIA_DIR / f"{o[0]}{OWNED_POSTER_SUFFIX}"


def content_url(o):
    return f"{schema.SITE}/{OWNED_MEDIA_DIR}/{o[0]}{OWNED_EXT}"


def poster_url(o):
    return f"{schema.SITE}/{OWNED_MEDIA_DIR}/{o[0]}{OWNED_POSTER_SUFFIX}"


def iso_duration(mss):
    """'9:37' -> 'PT9M37S'. Raises rather than guessing at a malformed runtime."""
    parts = str(mss).split(":")
    if not all(p.isdigit() for p in parts):
        raise RuntimeError(f"duration {mss!r} is not m:ss or h:mm:ss; read it off the file")
    nums = [int(p) for p in parts]
    if len(nums) == 2:
        return f"PT{nums[0]}M{nums[1]}S"
    if len(nums) == 3:
        return f"PT{nums[0]}H{nums[1]}M{nums[2]}S"
    raise RuntimeError(f"duration {mss!r} is not m:ss or h:mm:ss; read it off the file")


def guard_owned():
    """Refuse to render a film of ours that is not actually hosted here.

    Naming a film the site does not have is the same class of false claim as an
    invented listing, so the build stops rather than shipping the claim.
    """
    for o in OWNED:
        if len(o) != 5:
            raise RuntimeError(
                f"OWNED entry {o[0]!r} has {len(o)} fields; expected {OWNED_TUPLE_SHAPE}")
        iso_duration(o[2])
        for label, p in (("film", owned_media_path(o)), ("poster", owned_poster_path(o))):
            if not p.is_file() or p.stat().st_size == 0:
                raise RuntimeError(
                    f"OWNED entry {o[0]!r} has no {label} at "
                    f"{p.relative_to(_repo_root())}. Commit the file before claiming the film.")


def planned_rows():
    """Planned pieces still unshot. A published slug is not also promised."""
    shot = {o[0] for o in OWNED}
    return [p for p in PLANNED if p[0] not in shot]


def owned_room(lang="en"):
    """The featured room: our films first, and only when there are any."""
    guard_owned()
    if not OWNED:
        return ""
    if lang == "es":
        credit_prefix, footer_note = "Rodado", ("Rodado y montado por las personas que bailan aquí. Se reproduce desde este "
                 "sitio, y el archivo es nuestro.")
    else:
        credit_prefix, footer_note = "Filmed", ("Shot and cut by the people who dance here. It plays from this site, and "
                 "the file is ours.")
    figs = []
    for o in OWNED:
        _oid, title, duration, filmed_on, location = o
        figs.append(
            '<figure><div class="frame">'
            f'<video controls preload="metadata" poster="{html.escape(poster_url(o))}" '
            f'width="1280" height="720" playsinline>'
            f'<source src="{html.escape(content_url(o))}" type="video/mp4">'
            "Your browser cannot play this file. "
            f'<a href="{html.escape(content_url(o))}">Download it instead.</a>'
            "</video></div>"
            f"<figcaption><strong>{html.escape(title)}</strong>"
            f"<span>{credit_prefix} {html.escape(filmed_on)} &middot; {html.escape(location)} &middot; "
            f"{html.escape(duration)} &middot; {'nuestro propio filme' if lang == 'es' else 'our own film'}</span>"
            f"<p>{footer_note}</p></figcaption></figure>"
        )
    heading = ES_SECTION["owned_heading"] if lang == "es" else "Our own films"
    intro = (
        "Estos se ruedan en una sesión real, por las personas que están en la sala. Se reproducen "
        "desde este sitio: el archivo es nuestro, aquí no se incrusta nada del canal de nadie, y "
        "nada de esta sección es trabajo ajeno bajo nuestro nombre."
        if lang == "es" else
        "These are shot at a real session, by the people in the room. They play from "
        "this site: the file is ours, nothing here is embedded from anyone else's channel, "
        "and nothing in this section is somebody else's work under our name."
    )
    eyebrow = "Rodado en la jam" if lang == "es" else "Filmed at the jam"
    return (
        f'<div class="prose"><p class="eyebrow">{eyebrow}</p>'
        f'<h2 id="our-films">{heading}</h2>'
        f"<p>{intro}</p></div>"
        f'<div class="media-grid">{"".join(figs)}</div>'
    )


def in_production(lang="en"):
    """The honest not-yet state. Specific about what is coming, silent on what is not known."""
    rows = planned_rows()
    if not rows:
        return ""
    lis = ""
    for _slug, title, note, link, label in rows:
        if lang == "es":
            note, link, label = ES_PLANNED.get(_slug, (note, link, label))
        line = f"<strong>{html.escape(title)}</strong> &mdash; {html.escape(note)}"
        if link:
            line += f' <a href="{html.escape(link)}">{html.escape(label)}</a>'
        lis += f"<li>{line}</li>"
    if lang == "es":
        return (
            f'<div class="prose"><h2 id="in-production">{ES_SECTION["production_heading"]}</h2>'
            "<p>Ninguno de los filmes de abajo existe todavía. Esta jam no ha rodado ningún "
            "vídeo, así que hoy no hay ningún filme nuestro que mostrarte en esta página, y "
            "esta página no va a tomar prestado el crédito haciendo pasar el filme de otra "
            "persona por nuestro. Estos están en producción, en este orden:</p>"
            f"<ul>{lis}</ul>"
            "<p>No se da duración ni fecha de rodaje para ninguno de ellos, porque ninguna de "
            "las dos se conoce aún: una duración se lee del montaje terminado, y una fecha de "
            "rodaje es un día que ya ha ocurrido. Las dos aparecen en esta página solo cuando "
            "aparece el archivo, y cuando el archivo existe la pieza sube al principio de esta "
            "página como nuestra.</p></div>"
        )
    return (
        '<div class="prose"><h2 id="in-production">What we are filming</h2>'
        "<p>None of the films below exist yet. This jam has not shot a video, so there is "
        "no film of ours to show you on this page today, and this page will not borrow the "
        "credit by passing off someone else's film as ours. These are in production, in "
        "this order:</p>"
        f"<ul>{lis}</ul>"
        "<p>No runtime and no filming date is given for any of them, because neither is "
        "known yet: a runtime is read off the finished cut and a filming date is a day that "
        "has already happened. Both appear on this page only when the file does, and when "
        "the file exists the piece moves to the top of this page as ours.</p></div>"
    )


def _figure(v, lang="en"):
    vid, platform, title, channel, _date, duration, _cat, note = v
    if lang == "es":
        note = ES_NOTES.get(vid, note)
    by = ES_SECTION["by"] if lang == "es" else "by"
    return (
        f'<figure><div class="frame">'
        f'<iframe src="{embed_url(v)}" title="{html.escape(title)} \u2014 {html.escape(channel)}" '
        f'loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        f'allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>'
        f"</div><figcaption><strong>{html.escape(title)}</strong>"
        f"<span>{by} {html.escape(channel)} &middot; {duration} &middot; {platform}</span>"
        f"<p>{html.escape(note)}</p></figcaption></figure>"
    )


def gallery(lang="en"):
    if not VIDEOS:
        raise RuntimeError("VIDEOS is empty. The video room must not ship without verified entries.")
    categories = ES_CATEGORIES if lang == "es" else CATEGORIES
    out = []
    for slug, title, blurb in categories:
        items = [v for v in VIDEOS if v[6] == slug]
        if not items:
            continue
        out.append(
            f'<div class="prose"><h3 id="{slug}">{title}</h3><p>{blurb}</p></div>'
            f'<div class="media-grid">{"".join(_figure(v, lang) for v in items)}</div>'
        )
    return "".join(out)


def reference_section(lang="en"):
    """Other people's films, named as such, with every channel credited."""
    if not VIDEOS:
        raise RuntimeError("VIDEOS is empty. The reference section must not ship without entries.")
    if lang == "es":
        return (
            f'<div class="prose"><h2 id="reference-watching">{ES_SECTION["reference_heading"]}</h2>'
            f"<p>Todo lo de esta sección es un filme de otra persona. Estas {len(VIDEOS)} piezas "
            "las hicieron y publicaron los canales que se nombran en cada una, se reproducen en los "
            "reproductores de esos canales en las plataformas que las alojan, y este sitio no posee "
            "ninguna ni rodó ninguna. Enlazamos a ellas porque son los registros que merece la pena "
            "ver, y el crédito se queda en quien las hizo.</p>"
            "<p>También son, en el momento de escribir esto, casi todo lo que existe: la oferta de "
            "filmes de Improvisación de Contacto es escasa y en gran parte antigua, y ninguno se rodó "
            "en Miami. Ese hueco es la razón de que los filmes en producción de arriba se estén "
            "haciendo aquí.</p>"
            "</div>"
            + gallery("es")
        )
    return (
        '<div class="prose"><h2 id="reference-watching">Reference watching</h2>'
        f"<p>Everything in this section is someone else's film. These {len(VIDEOS)} pieces "
        "were made and published by the channels named on each one, they play through those "
        "channels' own players on the platforms that host them, and this site owns none of "
        "them and filmed none of them. We link to them because they are the records worth "
        "watching, and the credit stays with the person who made them.</p>"
        "<p>They are also, at the time of writing, nearly all of what exists: the supply of "
        "contact improvisation film is thin and largely old, and none of it was shot in "
        "Miami. That gap is why the films in production above are being made here.</p>"
        "</div>"
        + gallery()
    )


def credits(lang="en"):
    by_channel = {}
    for v in VIDEOS:
        by_channel.setdefault(v[3], []).append((v[2], watch_url(v)))
    lis = ""
    for channel in sorted(by_channel):
        links = ", ".join(
            f'<a href="{html.escape(u)}" rel="noopener nofollow">{html.escape(t)}</a>'
            for t, u in by_channel[channel]
        )
        lis += f"<li><strong>{html.escape(channel)}</strong> &mdash; {links}</li>"
    if lang == "es":
        return (
            f'<div class="prose"><h3 id="credits">{ES_SECTION["credits_heading"]}</h3>'
            "<p>Cada filme de arriba pertenece al canal que lo hizo y se reproduce en el "
            "reproductor de ese canal, en la plataforma que lo aloja. Ninguno es trabajo de "
            "este sitio y ninguno se presenta como trabajo de este sitio. Aquí no se descarga, "
            "ni se recorta, ni se vuelve a alojar nada. Si eres propietario de alguno y "
            "prefieres que no esté incrustado, "
            '<a href="/es/acerca-de#submit">dilo</a> y baja el mismo día.</p>'
            f"<ul>{lis}</ul></div>"
        )
    return (
        '<div class="prose"><h3 id="credits">Who made the films in this section</h3>'
        "<p>Every film above belongs to the channel that made it and plays through that "
        "channel's own player on the platform that hosts it. None of it is this site's work "
        "and none of it is presented as this site's work. Nothing is downloaded, re-cut or "
        "re-hosted here. If you own one of these and would rather it were not embedded, "
        '<a href="/about#submit">say so</a> and it comes down the same day.</p>'
        f"<ul>{lis}</ul></div>"
    )


def schema_list():
    """VideoObjects for the room. Ours first, then the credited embeds.

    Attribution is decided by where the film plays: an entry with an embedUrl is
    someone else's and is credited to that channel, and only an entry whose
    contentUrl is on this domain may carry this site's name as creator or publisher.
    """
    guard_owned()
    entries = []
    for o in OWNED:
        _oid, title, duration, filmed_on, location = o
        entries.append({
            "title": title,
            "description": f"Filmed {filmed_on} in {location} by the people who dance at this jam.",
            "content": content_url(o),
            "url": schema.SITE + "/videos#our-films",
            "thumbnail": poster_url(o),
            "duration": iso_duration(duration),
            "filmed_on": filmed_on,
        })
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
    if not entries:
        raise RuntimeError(
            "The video room has no entries: neither OWNED nor VIDEOS has anything in it.")
    return schema.video_objects(entries)
