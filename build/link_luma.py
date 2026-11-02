#!/usr/bin/env python3
"""Point every Luma RSVP link on miamicontactimprov.com at the NEXT event.

Today `build/content_marketing.py:23` hardcodes `LUMA = ".../3l7gfin7"` (or an
older slug). When that Friday passes, every RSVP button on the site lands on a
"Past Event" page. This makes the build ask Luma which event is next, every
time the site is built.

Design:
  - `tools/luma_next.py` resolves the next upcoming event from the public
    calendar page. It never invents a slug.
  - `LUMA_LAST_KNOWN` in content_marketing.py is the fallback. The build tries
    the live value first; on any failure it keeps the last known-good URL and
    prints a warning. A stale link is a bug; a fabricated link is a lie.
  - `LUMA_CALENDAR` is published next to the RSVP link so a visitor whose
    Friday has passed can always find the current one.

Run from the repo root:  python3 build/link_luma.py
Exit 0 = link resolved live or fallback valid. Exit 1 = neither, do not deploy.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "build" / "content_marketing.py"
RESOLVER = ROOT / "tools" / "luma_next.py"
CALENDAR = "https://luma.com/miamicontactimprov"

_HEADER = '''# --- Luma RSVP link -------------------------------------------------------
# The event this site sells changes every Friday. `build/link_luma.py` rewrites
# the two values below from the public Luma calendar before every build; never
# edit them by hand. LUMA_LAST_KNOWN is the fallback used when Luma cannot be
# read, so a network blip degrades to the last good event instead of a broken
# RSVP button.
LUMA_CALENDAR = "{calendar}"
LUMA_LAST_KNOWN = "{url}"
LUMA = LUMA_LAST_KNOWN  # alias kept: existing call sites use LUMA
'''

_BLOCK_START = "# --- Luma RSVP link"
_BLOCK_END_RE = re.compile(r"^LUMA = LUMA_LAST_KNOWN.*\n?", re.M)


def _block_end(text: str, start: int) -> int:
    """Index just past the managed block's final line."""
    m = _BLOCK_END_RE.search(text, start)
    if m is None:
        raise SystemExit("link_luma: Luma block has no LUMA assignment; refusing to rewrite")
    return m.end()


def read_current(text: str) -> tuple[str, str]:
    m_url = re.search(r'^LUMA_LAST_KNOWN\s*=\s*"([^"]+)"', text, re.M)
    m_cal = re.search(r'^LUMA_CALENDAR\s*=\s*"([^"]+)"', text, re.M)
    if m_url and m_cal:
        return m_url.group(1), m_cal.group(1)
    m_old = re.search(r'^LUMA\s*=\s*"([^"]+)"', text, re.M)
    return (m_old.group(1) if m_old else ""), CALENDAR


def resolve_live() -> str | None:
    if not RESOLVER.exists():
        return None
    try:
        p = subprocess.run(
            [sys.executable, str(RESOLVER)], capture_output=True, text=True, timeout=60
        )
    except Exception as e:  # noqa: BLE001 - any failure means "use fallback"
        print(f"link_luma: resolver crashed: {e}", file=sys.stderr)
        return None
    if p.returncode != 0:
        print(f"link_luma: resolver exit {p.returncode}: {p.stderr.strip()}", file=sys.stderr)
        return None
    url = p.stdout.strip()
    if not re.fullmatch(r"https://luma\.com/[a-z0-9]{6,12}", url):
        print(f"link_luma: resolver returned an unusable URL: {url!r}", file=sys.stderr)
        return None
    return url


def rewrite(text: str, url: str, calendar: str) -> str:
    """Return `text` with the Luma block set to `url`.

    Idempotent: if the managed block is already present with the right values,
    the text comes back unchanged. Replacing the whole block (comments plus
    values) rather than patching the assignment keeps the two in sync and makes
    a half-rewritten file impossible.
    """
    header = _HEADER.format(calendar=calendar, url=url)
    start = text.find(_BLOCK_START)
    if start != -1:
        end = _block_end(text, start)
        return text[:start] + header + text[end:]
    legacy = re.compile(r"^LUMA\s*=\s*\"[^\"]*\"[^\n]*\n", re.M)
    if legacy.search(text):
        return legacy.sub(header, text, count=1)
    raise SystemExit("link_luma: no LUMA assignment found in content_marketing.py")


def main() -> int:
    if not TARGET.exists():
        print(f"link_luma: missing {TARGET}", file=sys.stderr)
        return 1
    text = TARGET.read_text(encoding="utf-8")
    fallback, calendar = read_current(text)
    live = resolve_live()
    url = live or fallback
    if not url:
        print("link_luma: no live event and no fallback; refusing to write", file=sys.stderr)
        return 1
    if live:
        print(f"link_luma: {url} (live)", file=sys.stderr)
    else:
        print(f"link_luma: {url} (last known good; Luma unavailable)", file=sys.stderr)
    new_text = rewrite(text, url, calendar)
    if new_text == text and url == fallback:
        return 0
    TARGET.write_text(new_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
