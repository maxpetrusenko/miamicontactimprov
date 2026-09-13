#!/usr/bin/env python3
"""Generate the raster assets: favicons, apple-touch-icon and the 1200x630 og image.

Everything here is raster on purpose. Google ignores SVG favicons, and og:image
must be a 1200x630 raster or it is dropped from social cards.

Usage: python3 build/make_assets.py
"""

import pathlib

from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path(__file__).resolve().parent.parent / "site" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

INK = (245, 242, 234)
DARK = (12, 18, 16)
ACCENT = (231, 173, 88)
GREEN = (20, 31, 28)

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


def mark(size, pad_ratio=0.20):
    """The site mark: a gold dot on deep green, with a contact arc. Raster, transparent-friendly."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(size * (1 - pad_ratio * 2) / 2)
    cx = cy = size // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN + (255,))
    # inner arc suggesting a shared contact point
    w = max(2, int(size * 0.075))
    ar = int(r * 0.62)
    d.arc([cx - ar, cy - ar, cx + ar, cy + ar], start=200, end=20, fill=INK + (255,), width=w)
    dr = max(3, int(size * 0.11))
    d.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=ACCENT + (255,))
    return img


def favicons():
    for s in (16, 32, 48, 96, 180):
        img = mark(s)
        name = "apple-touch-icon.png" if s == 180 else f"favicon-{s}.png"
        img.save(OUT / name)
    # .ico must be a real multi-size icon or the browser silently falls back
    ico_sizes = [16, 32, 48]
    base = mark(48)
    base.save(OUT / "favicon.ico", sizes=[(s, s) for s in ico_sizes])
    (OUT.parent / "favicon.ico").write_bytes((OUT / "favicon.ico").read_bytes())


def og_image():
    """1200x630 social card. Typographic, no stock photo, no AI slop."""
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(img)

    # deep green field with a warm corner bloom, evoking a lit floor
    for i in range(H):
        t = i / H
        d.line([(0, i), (W, i)], fill=(
            int(12 + 10 * (1 - t)), int(18 + 16 * (1 - t)), int(16 + 13 * (1 - t)),
        ))
    bloom = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bloom)
    for i in range(28, 0, -1):
        a = int(5 + i * 1.1)
        bd.ellipse([W * 0.62 - i * 26, H * 0.1 - i * 12, W * 0.62 + i * 26, H * 0.1 + i * 24],
                   fill=ACCENT + (max(0, a),))
    img = Image.alpha_composite(img.convert("RGBA"), bloom).convert("RGB")
    d = ImageDraw.Draw(img)

    # two arcs: a shared contact point, drawn as plain geometry
    d.arc([120, 300, 620, 800], start=250, end=20, fill=(245, 242, 234), width=5)
    d.arc([560, 180, 1060, 680], start=200, end=340, fill=(231, 173, 88), width=5)
    d.ellipse([578, 400, 602, 424], fill=ACCENT)
    d.ellipse([280, 350, 300, 370], fill=INK)

    f_eyebrow = load_font(24)
    f_h1 = load_font(78)
    f_h2 = load_font(28)
    f_small = load_font(22)

    d.text((72, 62), "MIAMI  \u00b7  MIAMI BEACH  \u00b7  SOUTH FLORIDA", font=f_eyebrow, fill=ACCENT)
    d.text((72, 108), "Contact Improvisation", font=f_h1, fill=INK)
    d.text((72, 198), "in Miami", font=f_h1, fill=INK)
    d.text((72, 470), "Jams \u00b7 Classes \u00b7 Teachers \u00b7 Video", font=f_h2, fill=(200, 207, 198))
    d.text((72, 520), "A community map of the practice, with sources.", font=f_small, fill=(170, 180, 170))
    d.line([(72, 570), (300, 570)], fill=(231, 173, 88), width=3)
    d.text((72, 584), "miamicontactimprov.com", font=f_small, fill=INK)

    img.save(OUT / "og.png", optimize=True)


if __name__ == "__main__":
    favicons()
    og_image()
    print("assets written to", OUT)
    for p in sorted(OUT.iterdir()):
        print("  ", p.name, p.stat().st_size)
