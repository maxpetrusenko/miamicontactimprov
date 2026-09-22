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
    """1200x630 social card: the hero photograph (two hands reaching against a sunset sky),
    cropped to the reach and given a soft dark foot so a title overlay stays legible on
    platforms that add one. Photo only, no baked-in type: the card title comes from og:title."""
    W, H = 1200, 630
    src = OUT / "img" / "hero-clean.jpg"
    photo = Image.open(src).convert("RGB")
    pw, ph = photo.size
    scale = W / pw
    photo = photo.resize((W, round(ph * scale)), Image.LANCZOS)
    # centre the crop on the reach point, about half-way down the frame
    top = max(0, min(photo.height - H, round(photo.height * 0.50 - H / 2)))
    card = photo.crop((0, top, W, top + H))
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    for i in range(H):
        t = max(0.0, (i - H * 0.55) / (H * 0.45))
        vd.line([(0, i), (W, i)], fill=(23, 21, 18, int(150 * t * t)))
    card = Image.alpha_composite(card.convert("RGBA"), veil).convert("RGB")
    card.save(OUT / "og.png", optimize=True)


if __name__ == "__main__":
    favicons()
    og_image()
    print("assets written to", OUT)
    for p in sorted(OUT.iterdir()):
        print("  ", p.name, p.stat().st_size)
