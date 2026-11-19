#!/usr/bin/env python3
"""Resolve the next live Luma event for the site's RSVP links.

The site hardcoded one Luma event slug (build/content_marketing.py:23). Every
week that slug aged into a "Past Event" page and every RSVP button on the site
sent visitors into the past. This resolves the next upcoming event instead.

Contract:
  - Reads the PUBLIC calendar page for CALENDAR_SLUG (no auth, no API key).
  - Luma inlines the upcoming events as JSON in the page: each event carries
    "start_at" (UTC ISO-8601) and "url" (the slug).
  - Picks the earliest event whose start is in the future.
  - Prints the resolved URL on stdout; diagnostics on stderr.
  - Exit 0 with a URL, 1 when nothing upcoming exists, 2 when the page could
    not be read or the shape changed.
  - Never invents a slug. The caller keeps the last known-good value on
    non-zero exit: a stale link is a bug, a fabricated link is a lie.
"""

from __future__ import annotations

import re
import sys
import urllib.request
from datetime import datetime, timezone

CALENDAR_SLUG = "miamicontactimprov"
TIMEOUT = 25
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/156.0 Safari/537.36"
)

# A Luma event object inlined in the calendar page: each start_at travels with
# the event's own "url" slug. We do not parse the whole document.
_EVENT_RE = re.compile(
    r'"start_at":"(?P<start>[0-9T:\-\.]+Z)".{0,600}?"url":"(?P<slug>[a-z0-9]{6,12})"',
    re.S,
)


def fetch_calendar(slug: str = CALENDAR_SLUG) -> str:
    req = urllib.request.Request(f"https://luma.com/{slug}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def upcoming_events(html: str, now: datetime | None = None) -> list[tuple[datetime, str]]:
    now = now or datetime.now(timezone.utc)
    seen: dict[str, datetime] = {}
    for m in _EVENT_RE.finditer(html):
        try:
            start = datetime.fromisoformat(m.group("start").replace("Z", "+00:00"))
        except ValueError:
            continue
        slug = m.group("slug")
        if start <= now:
            continue
        if slug not in seen or start < seen[slug]:
            seen[slug] = start
    return sorted((s, slug) for slug, s in seen.items())


def resolve(slug: str = CALENDAR_SLUG) -> str:
    events = upcoming_events(fetch_calendar(slug))
    if not events:
        raise LookupError(f"no upcoming events on luma.com/{slug}")
    start, event_slug = events[0]
    print(f"luma-resolve: next is {event_slug} at {start.isoformat()}", file=sys.stderr)
    return f"https://luma.com/{event_slug}"


def main() -> int:
    try:
        url = resolve()
    except LookupError as e:
        print(f"luma-resolve: {e}", file=sys.stderr)
        return 1
    except Exception as e:  # network, HTTP, decoding
        print(f"luma-resolve: calendar unreadable: {e}", file=sys.stderr)
        return 2
    print(url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
