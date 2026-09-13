"""Confirmed local listings for the Miami pages.

Rules for this file:
  * Every entry must have been opened and read by a human or agent, with the date.
  * No entry may be invented. If it is not confirmed, it is not here.
  * `verified` is the date the source was last seen live.
Deleting an entry is normal. Sessions end, studios close, organisers move.
"""

import html
import schema

# name, city, venue, schedule, cost, url, verified, note
SESSIONS = []

# name, teacher or studio, level, format, url, verified, note
CLASSES = []

# name, role, city, url, verified, note
TEACHERS = []
LOCAL_ORGS = []


def _empty_block(kind, text):
    return f'<div class="prose"><h2>Recurring {kind} we can confirm today</h2><p>{text}</p></div>'


def _render(rows, kind):
    if not rows:
        return ""
    items = []
    for name, city, venue, schedule, cost, url, verified, note in rows:
        place = f"{venue}, {city}" if venue else city
        link = (
            f' <a href="{url}" rel="noopener nofollow">Details</a>'
            if url
            else ""
        )
        items.append(
            f"<li><p><strong>{html.escape(name)}</strong> &middot; {html.escape(place)}</p>"
            f"<p>{html.escape(schedule)}. {html.escape(cost)}.</p>"
            f"<p>{html.escape(note)}{link}</p></li>"
        )
    return (
        f'<div class="prose"><h2>Recurring {kind} in Miami we have confirmed</h2>'
        f'<p>Each entry was checked against the organiser\'s own listing. '
        f"Schedules change, so confirm before travelling.</p>"
        f'<ul class="dir-list">{"".join(items)}</ul></div>'
    )


def sessions_block():
    if SESSIONS:
        return _render(SESSIONS, "jams and open practice")
    return _empty_block(
        "jams",
        "We have not yet verified a recurring Contact Improvisation jam inside Miami-Dade or Broward "
        "County, and this site will not list one it has not checked. What we can tell you is where the "
        "question gets answered: the studios and organisers on the <a href=\"/directory\">directory</a> "
        "page are the people who would know, and most of them answer a direct message quickly. "
        "If you run a session, <a href=\"/about#submit\">tell us</a> and it will appear here with its "
        "schedule, room and cost stated plainly.",
    )


def classes_block():
    if CLASSES:
        return _render(CLASSES, "classes and workshops")
    return _empty_block(
        "classes",
        "No recurring Contact Improvisation class series in Miami has been verified here yet. "
        "Beginner-friendly movement classes that share CI's foundations, such as contemporary dance, "
        "somatic movement and improvisation labs, are run through the studios listed on the "
        "<a href=\"/directory\">directory</a> page.",
    )


def teachers_block():
    if TEACHERS:
        return _render(TEACHERS, "teachers and organisers")
    return _empty_block(
        "teachers",
        "Contact Improvisation has no certification body, so this list is built from what teachers and "
        "organisers publish about themselves rather than from a register. We have not yet confirmed a "
        "Miami-based CI teacher's own public listing. If you teach or organise here, "
        "<a href=\"/about#submit\">send us your page</a>.",
    )


def local_orgs_block():
    if LOCAL_ORGS:
        return _render(LOCAL_ORGS, "studios and organisations")
    return ""


def sessions_schema():
    if not SESSIONS:
        return None
    return schema.item_list(
        "/jams",
        "Contact improv jams confirmed in Miami and South Florida",
        [(n, u or schema.SITE + "/jams", s) for n, _c, _v, s, _cost, u, _ver, _note in SESSIONS],
    )
