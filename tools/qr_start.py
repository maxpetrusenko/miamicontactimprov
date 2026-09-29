#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["reportlab"]
# ///
"""Print the door card: an A5 page carrying the QR to /start and the line to say.

One card, one destination. The code encodes the acquisition address with its entry
tag, `https://miamicontactimprov.com/start?src=door`, so the signups that come from a
phone held up at the door arrive in the Worker carrying `:door` on the end of their
source and can be told apart from the ones the Instagram bio link brings. The tag is
the only difference between this code and the address the bio link points at.

The QR is drawn as vector, not as a pasted bitmap: a code rasterised at screen
resolution and then printed at A5 scans badly under the dim light of a studio at nine
at night. paper is left white and the ink is the site's dark, because a scanner wants
contrast on paper and a card is not a poster.

It writes the file and stops. Nothing here deploys, uploads or prints.

Usage:
    python3 tools/qr_start.py            # when the interpreter already has reportlab
    uv run tools/qr_start.py             # reads the dependency declared above
"""

import pathlib
import sys

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "print" / "start-qr.pdf"

SITE = "https://miamicontactimprov.com"
# The card's destination, entry tag included. The QR payload and the printed address
# are two different strings on purpose: the reader needs the address, the scanner
# needs the tag.
TARGET = f"{SITE}/start?src=door"
PRINTED = "miamicontactimprov.com/start"

KICKER = "MIAMI CONTACT IMPROV"
OFFER = "The next month's dates, and 10% off your first class."
CUE = "Say this as people leave:"
SPOKEN = "I send next month's dates and the video references by email. QR by the door."
VENUE = "Inner Motion Dance Studio, Hallandale Beach \u00b7 Fridays, 7\u20139 PM"

# The site palette, the same values build/make_assets.py and tools/ad_statics.py use.
# On paper the light inks are the wrong way round: the card is white and the ink is
# the dark, so what reads as foreground here is the colour the site uses as its
# background.
DARK = Color(12 / 255, 18 / 255, 16 / 255)
GREEN = Color(20 / 255, 31 / 255, 28 / 255)
MUTED = Color(110 / 255, 120 / 255, 112 / 255)
ACCENT = Color(231 / 255, 173 / 255, 88 / 255)

# Same list as build/make_assets.py and tools/ad_statics.py: a printed card and a
# share image are the same two faces. First one that loads wins.
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/System/Library/Fonts/NewYork.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def register_fonts():
    """Register the card's face, and return the name to draw with."""
    for path in FONT_CANDIDATES:
        if not pathlib.Path(path).exists():
            continue
        try:
            pdfmetrics.registerFont(TTFont("Card", path))
            return "Card"
        except Exception:
            continue
    raise SystemExit(
        "none of the card fonts could be registered: " + ", ".join(FONT_CANDIDATES)
    )


def wrap(text, font, size, max_width):
    """Greedy wrap against the real metrics. A word wider than the line stays whole."""
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and pdfmetrics.stringWidth(candidate, font, size) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_centred(c, lines, font, size, leading, page_width, y, colour):
    """Draw wrapped lines centred on the page, top down. Returns the next free y."""
    for line in lines:
        c.setFont(font, size)
        c.setFillColor(colour)
        c.drawCentredString(page_width / 2, y, line)
        y -= leading
    return y


def qr_drawing(payload, size):
    """The code as a vector drawing scaled to `size` points on a side."""
    widget = QrCodeWidget(payload, barLevel="M", barBorder=0)
    x0, y0, x1, y1 = widget.getBounds()
    scale_x = size / (x1 - x0)
    scale_y = size / (y1 - y0)
    drawing = Drawing(
        size,
        size,
        transform=[scale_x, 0, 0, scale_y, -x0 * scale_x, -y0 * scale_y],
    )
    drawing.add(widget)
    return drawing


def card():
    """Compose the A5 page and return the canvas, ready to save."""
    width, height = A5
    font = register_fonts()
    c = canvas.Canvas(str(OUT), pagesize=A5)
    c.setTitle("Miami Contact Improv \u2014 next dates by email")
    c.setAuthor("Miami Contact Improv")
    c.setSubject(PRINTED)

    margin = 18 * mm
    text_width = width - margin * 2

    # Kicker, then the offer. The offer is the headline of the card for the same
    # reason it is the label of the form: it is the sentence the reader is answering.
    y = height - margin
    c.setFont(font, 9)
    c.setFillColor(ACCENT)
    c.drawCentredString(width / 2, y, " ".join(KICKER))
    y -= 14 * mm

    y = draw_centred(
        c, wrap(OFFER, font, 19, text_width), font, 19, 25, width, y, DARK
    )

    # The code. Its quiet zone is the page's own margin around it, so no frame is
    # drawn: a scanner reads the light border, not a border line.
    #
    # The page is laid out from both ends and the code takes what is left between
    # them. Everything below it (address, rule, cue, spoken line, venue) is a fixed
    # stack measured up from the bottom margin, so a longer spoken line wraps into
    # the space reserved for it instead of running off the card.
    venue_y = margin
    spoken_first = venue_y + 38
    cue_y = spoken_first + 20
    rule_y = cue_y + 12
    url_y = rule_y + 22
    qr_bottom = url_y + 18
    qr_top = y - 8 * mm

    qr_size = min(92 * mm, qr_top - qr_bottom)
    renderPDF.draw(
        qr_drawing(TARGET, qr_size), c, (width - qr_size) / 2, qr_bottom
    )

    # The address under the code, so a card whose code will not scan is still usable.
    c.setFont(font, 14)
    c.setFillColor(DARK)
    c.drawCentredString(width / 2, url_y, PRINTED)

    # The cue: the line whoever holds the room says as people leave. Printed on the
    # card rather than written down somewhere else, because the card and the line are
    # handed out together.
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.2)
    c.line(margin, rule_y, width - margin, rule_y)
    c.setFont(font, 9)
    c.setFillColor(MUTED)
    c.drawCentredString(width / 2, cue_y, CUE)
    lines = wrap(f"\u201c{SPOKEN}\u201d", font, 13, text_width)
    for i, line in enumerate(lines):
        c.setFont(font, 13)
        c.setFillColor(GREEN)
        c.drawCentredString(width / 2, spoken_first - i * 18, line)

    c.setFont(font, 9)
    c.setFillColor(MUTED)
    c.drawCentredString(width / 2, venue_y, VENUE)
    c.showPage()
    return c


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = card()
    c.save()

    # Read the page back rather than trusting the save call. A card that is not A5 is
    # not the card that was asked for.
    header = OUT.read_bytes()[:8]
    if not header.startswith(b"%PDF"):
        raise SystemExit(f"{OUT} is not a PDF")
    size = OUT.stat().st_size
    print(f"wrote {OUT} ({size} bytes, A5 {round(A5[0] / mm)}x{round(A5[1] / mm)}mm)")
    print(f"the code encodes {TARGET}")
    print(f"the card prints  {PRINTED}")
    print(f"spoken line      {SPOKEN}")
    print(
        "to test it: scan the code with a phone camera and check the address it opens "
        "ends in ?src=door, then check the signup lands in KV with ':door' on the end "
        "of its source"
    )


if __name__ == "__main__":
    sys.exit(main())
