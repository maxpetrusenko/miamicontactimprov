"""Shared page shell for miamicontactimprov.com.

Every page is rendered through here so the head, nav and footer exist in exactly
one place. Editing the nav means editing NAV below and re-running build.py.
"""

SITE = "https://miamicontactimprov.com"
NAME = "Miami Contact Improv"
TAGLINE = "A working map of Contact Improvisation in Miami"

# Bump when the local listings in build/listings.py are re-checked against source.
LAST_CHECKED = "13 September 2026"

NAV = [
    ("What is CI", "/what-is-contact-improvisation"),
    ("Miami", "/miami"),
    ("Jams", "/jams"),
    ("Classes", "/classes"),
    ("Videos", "/videos"),
    ("Directory", "/directory"),
    ("About", "/about"),
]

FOOTER_COLS = [
    ("Start here", [
        ("What is Contact Improvisation?", "/what-is-contact-improvisation"),
        ("Your first jam", "/classes#first-jam"),
        ("Glossary of CI terms", "/glossary"),
        ("History of CI", "/history"),
    ]),
    ("In Miami", [
        ("The Miami scene", "/miami"),
        ("Jams and open practice", "/jams"),
        ("Classes and workshops", "/classes"),
        ("Teachers and organisers", "/directory#teachers"),
    ]),
    ("Watch", [
        ("Video room", "/videos"),
        ("Watch a full duet", "/videos#duets"),
        ("Festival footage", "/videos#festivals"),
    ]),
    ("This site", [
        ("About and contact", "/about"),
        ("Safety and consent", "/safety-and-consent"),
        ("Questions people ask", "/faq"),
        ("Submit a listing", "/about#submit"),
    ]),
]

STYLESHEET = "/assets/site.css?v=1"


def head(title, description, path, *, jsonld="", og_type="website", extra_head=""):
    """Return the <head> block. `path` is the site-relative route, e.g. /miami."""
    url = SITE + ("/" if path == "/" else path)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0c1210">
<meta name="color-scheme" content="dark">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Two dancers in contact improvisation, one supporting the other's weight">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE}/assets/og.png">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/favicon-96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=Instrument+Serif:ital@0;1&display=swap">
<link rel="stylesheet" href="{STYLESHEET}">
<link rel="alternate" type="text/plain" href="{SITE}/llms.txt" title="llms.txt">
{extra_head}{jsonld}
</head>"""


def header(current):
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    links.append('<a class="cta" href="/about#submit">Submit a jam</a>')
    return f"""<header class="site-header" id="site-header">
  <div class="header-inner">
    <a class="brand" href="/">
      <span class="dot" aria-hidden="true"></span>
      <span>Miami Contact Improv<small>miamicontactimprov.com</small></span>
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="primary-nav" aria-label="Primary">
      {''.join(links)}
    </nav>
  </div>
</header>"""


def footer():
    cols = []
    for title, items in FOOTER_COLS:
        lis = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in items)
        cols.append(f'<div><h3>{title}</h3><ul>{lis}</ul></div>')
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      {''.join(cols)}
    </div>
    <div class="colophon">
      <span>{NAME} &middot; an independent, non-commercial resource for the Miami dance community.</span>
      <span>Local listings last checked {LAST_CHECKED}. Contact Improvisation has no central authority, no licence and no membership. This site is one map of it, not the map.</span>
    </div>
  </div>
</footer>"""


def body_script():
    return """<script>
(function () {
  var header = document.getElementById('site-header');
  var toggle = header && header.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { header.classList.remove('nav-open'); if (toggle) toggle.setAttribute('aria-expanded', 'false'); }
  });
  var v = document.getElementById('video');
  if (v) {
    var kick = function () { var p = v.play(); if (p && p.catch) p.catch(function () {}); };
    kick();
    ['pointerdown', 'scroll', 'touchstart', 'keydown'].forEach(function (ev) {
      window.addEventListener(ev, kick, { once: true, passive: true });
    });
  }
})();
</script>
</body>
</html>"""


def bg_youtube_embed(video_id):
    """YouTube background-embed: official embed player in muted loop mode.

    Nothing is downloaded or re-hosted; the film plays from the owner's channel.
    """
    src = (
        f"https://www.youtube-nocookie.com/embed/{video_id}"
        "?autoplay=1&mute=1&controls=0&loop=1&playlist=" + video_id
        + "&modestbranding=1&playsinline=1&rel=0&iv_load_policy=3&disablekb=1&fs=0"
    )
    return f"""<div id="bgwrap" aria-hidden="true">
  <iframe id="video" src="{src}" title="" tabindex="-1"
    allow="autoplay; encrypted-media" frameborder="0"></iframe>
</div>"""


def page(title, description, path, body, *, jsonld="", bg_video=None, bg_youtube=None, og_type="website"):
    """Assemble a full HTML document.

    bg_youtube: a verified YouTube id, played as a muted looping background embed.
    bg_video: a self-hosted filename stem in /assets/videos/ (poster + webm + mp4).
    """
    bg = ""
    if bg_youtube:
        bg = bg_youtube_embed(bg_youtube)
    elif bg_video:
        bg = f"""<div id="bgwrap" aria-hidden="true">
  <video id="video" autoplay loop muted playsinline preload="metadata" poster="/assets/videos/{bg_video}-poster.jpg">
    <source src="/assets/videos/{bg_video}.webm?v=1" type="video/webm">
    <source src="/assets/videos/{bg_video}.mp4?v=1" type="video/mp4">
  </video>
</div>"""
    return (
        head(title, description, path, jsonld=jsonld, og_type=og_type)
        + "\n<body>\n"
        + '<a class="skip-link" href="#main">Skip to content</a>\n'
        + bg
        + '<div id="scrim" aria-hidden="true"></div><div id="grain" aria-hidden="true"></div>\n'
        + '<div class="page">\n'
        + header(path)
        + "\n<main id=\"main\">\n"
        + body
        + "\n</main>\n"
        + footer()
        + "\n</div>\n"
        + body_script()
    )


# ---------- reusable content blocks ----------

def answer(text, label="Short answer"):
    return f'<div class="answer"><div class="label">{label}</div><p>{text}</p></div>'


def cite_block(text):
    return f'<div class="cite"><div class="label">Cite this page</div><p>{text}</p></div>'


def band(title, text, buttons, band_id=None):
    bid = f' id="{band_id}"' if band_id else ""
    btns = "".join(
        f'<a class="btn {style}" href="{href}">{label}</a>' for label, href, style in buttons
    )
    return (
        f'<div class="band"{bid}><h2>{title}</h2><p>{text}</p>'
        f'<div class="btn-row">{btns}</div></div>'
    )


def facts(rows, caption=None):
    trs = "".join(
        f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows
    )
    return f'<table class="facts">{trs}</table>'


def cards(items):
    out = []
    for tag, title, text, href in items:
        out.append(
            f'<a class="card" href="{href}"><span class="tag">{tag}</span>'
            f"<h3>{title}</h3><p>{text}</p></a>"
        )
    return f'<div class="grid">{"".join(out)}</div>'
