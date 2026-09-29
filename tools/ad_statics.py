#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml", "pillow"]
# ///
"""Generate the static ad posters for the Contact Improv Miami ad test.

One poster per message per format: four creative families, three messages each,
two formats, so 24 files. Every poster is typography on the site's own palette,
with the venue and the landing address on it. Nothing is drawn that the site does
not already claim, and no discount code appears anywhere on a poster; the code
belongs to the welcome email.

Real class photographs replace crops of these once the first class has produced
some. Until then a poster that says one thing clearly beats a stock image.

File names are deterministic: re-running overwrites rather than accumulating, so
`docs/ads/out/` always holds exactly the set the message bank describes.

Usage:
    python3 tools/ad_statics.py     # when the interpreter already has Pillow and PyYAML
    uv run tools/ad_statics.py      # reads the dependencies declared above
"""

import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

try:
    import yaml
except ImportError:  # the message bank is YAML; say how to get a reader rather than traceback
    print(
        "this tool needs PyYAML: uv run --with pyyaml python3 tools/ad_statics.py",
        file=sys.stderr,
    )
    raise SystemExit(2)

ROOT = pathlib.Path(__file__).resolve().parent.parent
MESSAGES = ROOT / "docs" / "ads" / "messages.yaml"
OUT = ROOT / "docs" / "ads" / "out"

# name, width, height. The two placements Meta wants for this test.
FORMATS = [
    ("feed", 1080, 1080),
    ("story", 1080, 1920),
]

# The site palette, the same values build/make_assets.py draws with. Kept in step
# with site/assets/site.css: --dark-2, --dark, --ink, --ink-soft, --muted, --accent.
DARK = (12, 18, 16)
GREEN = (20, 31, 28)
INK = (245, 242, 234)
INK_SOFT = (220, 226, 215)
MUTED = (170, 180, 170)
ACCENT = (231, 173, 88)

# Same list as build/make_assets.py, so a poster and the share card are the same
# two faces. First one that loads wins.
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/System/Library/Fonts/NewYork.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def slug(text):
    """`new to Miami` -> `new-to-miami`. One form, so a file name is predictable."""
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def wrap(draw, text, font, max_width):
    """Greedy wrap. A word wider than the line stays whole rather than being cut."""
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and draw.textlength(candidate, font=font) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def contact_badge(d, cx, cy, r):
    """The site mark in its smallest form: a dot held by two arcs."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN)
    d.arc([cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78],
          start=200, end=20, fill=INK, width=max(2, int(r * 0.13)))
    dr = max(3, int(r * 0.22))
    d.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=ACCENT)


def poster(headline, subline, identity, venue, url_line, width, height):
    """One poster. Returns the image, or raises if the copy cannot fit the canvas.

    The layout is top-aligned except for the footer strip, which is the venue and
    the landing address on every file. Copy that will not fit is a build failure:
    a headline that runs under the footer is unreadable, not a smaller poster.
    """
    img = Image.new("RGB", (width, height), DARK)
    d = ImageDraw.Draw(img)

    # Deep green field, warm at the top so type does not sit on flat colour.
    for i in range(height):
        t = i / height
        d.line([(0, i), (width, i)], fill=(
            int(12 + 8 * (1 - t)), int(18 + 13 * (1 - t)), int(16 + 11 * (1 - t)),
        ))
    bloom = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bloom)
    for i in range(30, 0, -1):
        bd.ellipse([width * 0.72 - i * (width * 0.018), -i * 14,
                    width * 0.72 + i * (width * 0.018), i * 26],
                   fill=ACCENT + (max(0, int(4 + i * 0.9)),))
    img = Image.alpha_composite(img.convert("RGBA"), bloom).convert("RGB")
    d = ImageDraw.Draw(img)

    feed = height == width
    margin = int(width * 0.082)
    top = margin + int(height * (0.05 if feed else 0.06))
    size_kicker = int(width * 0.032)
    size_head = int(width * (0.078 if feed else 0.089))
    size_sub = int(width * 0.039)
    size_venue = int(width * 0.028)
    f_kicker = load_font(size_kicker)
    f_head = load_font(size_head)
    f_sub = load_font(size_sub)
    f_venue = load_font(size_venue)
    f_url = load_font(int(width * 0.030))
    text_width = width - margin * 2

    # Kicker first: one word for who is reading. This is the line a duplicate of
    # a winner swaps, so it stays on its own.
    kicker = identity.upper()
    d.text((margin, top), kicker, font=f_kicker, fill=ACCENT)

    cursor = top + int(size_kicker * 1.6) + int(height * 0.045)
    for line in wrap(d, headline, f_head, text_width):
        d.text((margin, cursor), line, font=f_head, fill=INK)
        cursor += int(size_head * 1.18)

    cursor += int(height * 0.022)
    for line in wrap(d, subline, f_sub, text_width):
        d.text((margin, cursor), line, font=f_sub, fill=INK_SOFT)
        cursor += int(size_sub * 1.34)

    # Footer strip. Both lines sit on every poster, so a downloaded image can be
    # traced back to the site it is advertising.
    rule_y = height - int(height * (0.218 if feed else 0.156))
    if cursor > rule_y - int(height * 0.03):
        raise SystemExit(
            f"copy runs into the footer strip at {width}x{height}: {headline!r}"
        )
    d.line([(margin, rule_y), (margin + int(width * 0.16), rule_y)], fill=ACCENT, width=3)
    d.text((margin, rule_y + int(height * 0.026)), venue, font=f_venue, fill=MUTED)
    d.text((margin, rule_y + int(height * 0.026) + int(size_venue * 1.7)),
           url_line, font=f_url, fill=INK)

    contact_badge(d, width - margin - int(width * 0.05), top + int(width * 0.05), int(width * 0.05))
    return img


def load_bank():
    """Read the message bank and fail closed on anything the posters cannot use.

    Every check here exists because a typo in YAML renders a poster nobody reads.
    """
    bank = yaml.safe_load(MESSAGES.read_text(encoding="utf-8"))
    known = bank.get("identities") or []
    families = bank.get("families") or {}
    if not known:
        raise SystemExit("messages.yaml lists no identity words")
    if not families:
        raise SystemExit("messages.yaml lists no creative families")

    render = []
    for family, spec in families.items():
        identities = spec.get("identities") or []
        body_words = len((spec.get("body") or "").split())
        if not 120 <= body_words <= 200:
            raise SystemExit(
                f"family {family}: body copy is {body_words} words, and the ad text "
                "runs between 120 and 200"
            )
        for word in identities:
            if word not in known:
                raise SystemExit(f"family {family}: identity {word!r} is not one of the eight")
        messages = spec.get("messages") or []
        if not messages:
            raise SystemExit(f"family {family}: no messages")
        for message in messages:
            for field in ("slug", "identity", "headline", "subline"):
                if not message.get(field):
                    raise SystemExit(f"family {family}: a message has no {field}")
            if message["identity"] not in identities:
                raise SystemExit(
                    f"family {family}: message {message['slug']} uses "
                    f"{message['identity']!r}, which this family does not address"
                )
            render.append((family, message))
    if not render:
        raise SystemExit("messages.yaml produced no posters to render")
    return bank, render


def main():
    bank, render = load_bank()
    venue = bank.get("venue") or ""
    url_line = (bank.get("landing") or "").split("://")[-1].rstrip("/")
    if not venue or not url_line:
        raise SystemExit("messages.yaml has no venue or landing address")

    written = []
    for family, message in render:
        folder = OUT / family
        folder.mkdir(parents=True, exist_ok=True)
        stem = f"{slug(message['slug'])}-{slug(message['identity'])}"
        for name, width, height in FORMATS:
            img = poster(
                message["headline"], message["subline"], message["identity"],
                venue, url_line, width, height,
            )
            path = folder / f"{stem}-{name}.png"
            img.save(path, optimize=True)
            # A file that is not the size the format claims is not a poster. Read
            # the header back rather than trusting the save call.
            with Image.open(path) as check:
                if check.size != (width, height):
                    raise SystemExit(f"{path} is {check.size}, not {(width, height)}")
            written.append(path)

    unused = sorted(set(bank["identities"]) - {m["identity"] for _f, m in render})
    if unused:
        print(f"identity words with no poster yet: {', '.join(unused)}")
    print(f"{len(written)} posters in {OUT}")
    for family in sorted({f for f, _m in render}):
        count = len([p for p in written if p.parent.name == family])
        print(f"  {family}: {count} files")


if __name__ == "__main__":
    main()
