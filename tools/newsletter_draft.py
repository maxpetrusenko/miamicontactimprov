#!/usr/bin/env python3
"""Draft next month's email for the Contact Improv Miami list.

The draft is built from what the site already says: the class dates in the
EVENT_DATES row for the Fundamentals series, and, separately, what changed in
build/listings.py over the last month. The dates go into the email. The change list
goes to stdout only, because a commit subject is not reader copy; whoever sends the
broadcast reads it and decides what to say in their own words.

It creates a Resend broadcast and stops. Sending is a click in the Resend dashboard,
which is where it should stay: the draft is a starting point, not a decision.

Usage
    RESEND_API_KEY=... python3 tools/newsletter_draft.py
    RESEND_API_KEY=... python3 tools/newsletter_draft.py --month 2026-11
    python3 tools/newsletter_draft.py --dry-run        # print the email, post nothing

The key comes from Doppler api_keys/dev (RESEND_API_KEY) on the machine that runs it.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "build"))

import listings  # noqa: E402  (needs build/ on the path first)

AUDIENCE_ID = os.environ.get("CI_NEWSLETTER_AUDIENCE", "6da7e1c7-6fe5-446d-b306-00a52f5b9d07")
FROM = "Contact Improv Miami <hello@miamicontactimprov.com>"
SITE = "https://miamicontactimprov.com"
SERIES_URL = SITE + "/fundamentals"
VENUE = "Inner Motion, 216 NE 1st Ave, Hallandale Beach"
COUNT_WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}


def month_start(today, offset):
    first = today.replace(day=1)
    for _ in range(offset):
        first = (first + timedelta(days=32)).replace(day=1)
    return first


def month_name(when):
    return when.strftime("%B %Y")


def series_dates():
    """Every dated class of the series, earliest first."""
    return sorted(
        iso for iso, _venue, _start, _end in listings.EVENT_DATES[listings.FUNDAMENTALS_NAME]
    )


def in_month(dates, when):
    return [iso for iso in dates if iso[:7] == when.strftime("%Y-%m")]


def upcoming(dates, when, limit=4):
    """The next few classes after the month, used when the month itself is empty."""
    return [iso for iso in dates if iso >= when.strftime("%Y-%m-01")][:limit]


def draft_body(when, dates, today):
    """The email, as plain text. One link. No code: the welcome email carries that."""
    month = month_name(when)
    lines = []
    if dates:
        count = COUNT_WORDS.get(len(dates), str(len(dates)))
        noun = "Friday" if len(dates) == 1 else "Fridays"
        lines.append(f"{count} {noun} in {month}, {VENUE}.")
        lines.append("7:00 to 9:00 PM:")
        lines.append("")
        lines.extend(f"  {listings.date_label(iso)}" for iso in dates)
        lines.append("")
        lines.append(
            "Drop in at any of them, or come to all eight. No partner and no experience "
            "needed. $20 to $50 for each class, paid at the door or booked online."
        )
    else:
        lines.append(f"Nothing is on the calendar yet for {month}.")
        later = upcoming(dates, when)
        if later:
            lines.append("")
            lines.append("The next classes are:")
            lines.append("")
            lines.extend(f"  {listings.date_label(iso)}" for iso in later)
    lines.append("")
    lines.append(f"Dates, the venue, and what each class covers: {SERIES_URL}")
    lines.append("")
    lines.append("One email a month. Reply if you want off the list.")
    lines.append("")
    lines.append("Max")
    return "\n".join(lines)


def draft_subject(when, dates):
    if not dates:
        return f"Contact Improv Miami, {month_name(when)}"
    count = COUNT_WORDS.get(len(dates), str(len(dates)))
    noun = "Friday" if len(dates) == 1 else "Fridays"
    return f"{count} {noun} in {month_name(when)} at Contact Improv Miami"


def listing_changes(since):
    """Commit subjects that touched build/listings.py in the window."""
    try:
        out = subprocess.run(
            ["git", "log", f"--since={since}", "--format=%h %s", "--", "build/listings.py"],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [line for line in out.splitlines() if line.strip()]


def create_broadcast(key, subject, text, when):
    payload = {
        "audience_id": AUDIENCE_ID,
        "from": FROM,
        "reply_to": "hello@miamicontactimprov.com",
        "subject": subject,
        "name": f"Contact Improv Miami, {month_name(when)}",
        "text": text,
    }
    request = urllib.request.Request(
        "https://api.resend.com/broadcasts",
        data=json.dumps(payload).encode(),
        method="POST",
    )
    request.add_header("Content-Type", "application/json")
    request.add_header("Authorization", f"Bearer {key}")
    request.add_header("User-Agent", "curl/8.7.1")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        raw = error.read().decode()
        try:
            return error.code, json.loads(raw)
        except ValueError:
            return error.code, raw


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--month", help="YYYY-MM to write about (default: next month)")
    parser.add_argument("--since", help="git log window for the change list (default: 35 days)")
    parser.add_argument("--dry-run", action="store_true", help="print the email, post nothing")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="print the receipt and the change list only, not the email body (what the cron job sends)",
    )
    args = parser.parse_args()

    today = date.today()
    if args.month:
        year, month = (int(part) for part in args.month.split("-"))
        when = date(year, month, 1)
    else:
        when = month_start(today, 1)

    dates = series_dates()
    body = draft_body(when, in_month(dates, when), today)
    subject = draft_subject(when, in_month(dates, when))

    if args.quiet:
        print(f"subject: {subject}")
    else:
        print(f"--- subject ---\n{subject}\n--- body ---\n{body}\n--- end ---")

    changes = listing_changes(args.since or f"{today - timedelta(days=35)}")
    if changes:
        print(f"\nlisting data changed since {args.since or today - timedelta(days=35)}:")
        for line in changes:
            print(f"  {line}")
    else:
        print("\nlisting data: no commits in the window.")

    if args.dry_run:
        print("\ndry run: nothing posted.")
        return 0

    key = os.environ.get("RESEND_API_KEY")
    if not key:
        print("\nRESEND_API_KEY is not set, so no draft was created.", file=sys.stderr)
        return 1
    status, payload = create_broadcast(key, subject, body, when)
    if status >= 300:
        print(f"\nResend refused the draft: {status} {payload}", file=sys.stderr)
        return 1
    if not isinstance(payload, dict) or not payload.get("id"):
        print(f"\nResend answered {status} without an id: {payload}", file=sys.stderr)
        return 1
    print(f"\ndraft created, not sent: https://resend.com/broadcasts/{payload['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
