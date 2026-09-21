"""The four marketing views from the Miami Contact Improv handoff: Home, Events,
About and Contact.

These are the primary site now. The deeper library pages (what-is, jams, classes,
history, glossary, safety, directory, videos and the Spanish tree) are kept as
secondary pages reachable from the footer and rendered through the same shell.

Design: a warm cream editorial base with full-bleed dark "gallery" bands that carry
the movement photography edge to edge, so the site reads bright and airy with moody,
cinematic pockets. Black-and-white frames run in the structured grids; the warmer
colour frames carry the dark bands and the social feed.

The handoff mock used Thursday / Oct 1 as sample content. The real recurring session
is the Friday jam the rest of the site documents (build/listings.py), so the copy here
uses Fridays, first session 2 October 2026, and reuses the verified Event node.
"""

import listings
import schema
from shell import page

IG = "https://instagram.com/miamicontactimprov"
IMG = "/assets/img"
IG_GLYPH = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="6"/>'
    '<circle cx="12" cy="12" r="4.2"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" '
    'stroke="none"/></svg>'
)

# Real @miamicontactimprov post permalinks. Add them here (e.g.
# "https://www.instagram.com/p/ABC123/") and the "On Instagram" section renders live
# post embeds via Instagram's official embed.js. Empty is the honest default: no
# fabricated posts. When empty, the section shows the real jam photography below,
# linked to the profile, and no third-party script is loaded.
IG_POSTS = [
    "https://www.instagram.com/p/Ddh7ZhVOc6f/",
    "https://www.instagram.com/p/Ddb99EDytsx/",
    "https://www.instagram.com/reel/DPrOYR8jYjU/",
    "https://www.instagram.com/reel/DPZt8AxjOAO/",
    "https://www.instagram.com/reel/DVjMRgUDv0P/",
]
# Max's own reel: embedded on the About page beside the facilitator bio.
MAX_REEL = "https://www.instagram.com/reel/DVjMRgUDv0P/"


# Media aspect (height / width) per post so the frame can be cropped just below the
# likes row. Instagram renders reels and square posts at 1:1 in the embed; portrait
# photo posts are 4:5. Posts not listed default to square.
IG_RATIOS = {"Ddh7ZhVOc6f": 1.25}


def ig_embed(url):
    """A live Instagram post as a direct /embed/ iframe: no embed.js, no blocker-prone
    script, no fallback link. Height is set by JS from width x ratio + chrome."""
    kind = "reel" if "/reel/" in url else "post"
    ratio = IG_RATIOS.get(url.rstrip("/").rsplit("/", 1)[-1], 1.0)
    return (f'<iframe class="ig-frame ig-{kind}" data-ratio="{ratio}" src="{url}embed/" title="Instagram {kind}" loading="lazy" scrolling="no" '
            f'allow="encrypted-media" referrerpolicy="strict-origin-when-cross-origin"></iframe>')


def _ig_pill(kind="terracotta", label="@miamicontactimprov"):
    return (
        f'<a class="mci-pill {kind}" href="{IG}" target="_blank" rel="noopener">'
        f'{IG_GLYPH}<span>{label}</span></a>'
    )


def _gallery(image, alt, title, text, cta_html, *, eyebrow=None, tall=False):
    """A full-bleed dark gallery band: edge-to-edge photograph, dark veil, light text."""
    eb = f'<p class="eyebrow-l">{eyebrow}</p>' if eyebrow else ""
    cls = "mci-gallery tall" if tall else "mci-gallery"
    return f"""
<section class="{cls}">
  <img class="bg" src="{IMG}/{image}" alt="{alt}">
  <div class="veil"></div>
  <div class="inner">
    {eb}<h2 class="mci-h">{title}</h2>
    <p>{text}</p>
    {cta_html}
  </div>
</section>"""


def _ig_section():
    """The 'On Instagram' section: live post embeds when IG_POSTS is set, otherwise the
    real jam photography as a feed-style preview linked to the profile."""
    head = f"""
  <div class="mci-ig-head">
    <h2 class="mci-h">ON INSTAGRAM</h2>
  </div>"""
    if IG_POSTS:
        cards = "".join(ig_embed(url) for url in IG_POSTS)
        return f"""
<div class="mci-ig mci-reveal">{head}
  <div class="ig-embeds">{cards}</div>
</div>"""
    # Fallback: real photography, feed-style, each tile opening the profile.
    tiles = [
        ("c2.jpg", "Contact improv duet in soft green light"),
        ("p4.jpg", "A dancer mid-turn, long-exposure black and white"),
        ("c6.jpg", "A dancer arched back over a partner's shoulder"),
        ("p3.jpg", "Two dancers folded together, black and white"),
        ("c5.jpg", "A close contact improv duet outdoors"),
        ("p7.jpg", "A reaching hand in soft light"),
    ]
    cells = "".join(
        f'<a class="mci-tile" href="{IG}" target="_blank" rel="noopener">'
        f'<img src="{IMG}/{src}" alt="{alt}" loading="lazy"></a>'
        for src, alt in tiles
    )
    return f"""
<div class="mci-ig mci-reveal">{head}
  <div class="mci-ig-grid">{cells}</div>
  <p class="mci-ig-note">Follow <a href="{IG}" target="_blank" rel="noopener">@miamicontactimprov</a> for jam reminders, photos and clips.</p>
</div>"""


# ---------------------------------------------------------------- Home
def home():
    body = f"""
<section class="mci-hero-full plain" id="mci-hero">
  <div class="bg-wrap" id="mci-hero-bg"><img class="bg" src="/assets/img/hero-clean.jpg" alt="Two hands reaching toward each other against a pink sunset sky"></div>
  <div class="veil"></div>
  <div class="inner" id="mci-hero-inner">
    <p class="eyebrow-l rise" style="--d:.15s">Every Friday &middot; 7&ndash;9 PM &middot; Hallandale Beach</p>
    <h1 class="mci-h"><span class="rise" style="--d:.3s">MOVE.</span><span class="rise" style="--d:.42s">LISTEN.</span><span class="rise accent" style="--d:.54s">IMPROVISE.</span></h1>
    <p class="lede rise" style="--d:.72s">A weekly contact improv class and open jam in Miami &mdash; where dance meets touch, trust, and play. No experience needed, just a curious body.</p>
    <div class="btn-row rise" style="--d:.88s">
      <a class="btn primary" href="/events">See upcoming jams &nbsp;&rarr;</a>
      <a class="btn secondary" href="{IG}" target="_blank" rel="noopener">@miamicontactimprov</a>
    </div>
  </div>
  <a class="scroll-cue" href="#mci-when" aria-label="Scroll to details"><span class="line"></span><span class="txt">Scroll</span></a>
</section>

<div class="mci-panel-wrap" id="mci-when">
  <div class="mci-panel">
    <div>
      <p class="label mci-h">WHEN</p>
      <p>Every Friday, starting Oct 2<br>7:00 &ndash; 9:00 PM<br>Class, then Open Jam</p>
    </div>
    <div>
      <p class="label mci-h">WHERE</p>
      <p>Inner Motion Dance Studio<br>216 NE 1st Ave, Hallandale Beach, FL</p>
    </div>
    <div>
      <p class="label mci-h">WHO</p>
      <p>All levels, all bodies.<br>Come solo or bring a friend.</p>
    </div>
  </div>
</div>

<div class="mci-block mci-reveal">
  <p class="mci-eyebrow">What is it</p>
  <h2 class="mci-h">A DANCE FORM BUILT ON WEIGHT, TOUCH &amp; SHARED MOMENTUM.</h2>
  <p class="body">Contact improv is an improvised dance form rooted in physical contact &mdash; two or more bodies exploring balance, weight-sharing, and momentum together, moment to moment. No choreography, no mirrors, no performance pressure.</p>
  <div class="mci-cards">
    <div class="mci-mini"><p class="t mci-h">7:00 &middot; CLASS</p><p>Guided warm-up and skills &mdash; rolling, weight-sharing, safe falling.</p></div>
    <div class="mci-mini"><p class="t mci-h">7:45 &middot; OPEN JAM</p><p>Free-form dancing. Join in, sit out, watch &mdash; everything is welcome.</p></div>
    <div class="mci-mini"><p class="t mci-h">$20 &ndash; $50</p><p>Sliding scale &mdash; pay what fits. Bring comfy clothes, no shoes needed.</p></div>
  </div>
  <div class="mci-actions">
    <a class="mci-textlink" href="https://www.youtube.com/watch?v=q4wUEiHowSU" target="_blank" rel="noopener">&#9654; Watch: what is contact improv</a>
  </div>
</div>

<div class="mci-photos mci-reveal">
  <div class="mci-tile"><img src="{IMG}/p1.jpg" alt="Two dancers in a supported lean, motion-blurred black and white" loading="lazy"><span class="chip">FRIDAY JAM</span></div>
  <div class="mci-tile"><img src="{IMG}/p4.jpg" alt="A dancer mid-turn, shirt open, long-exposure black and white" loading="lazy"><span class="chip">CLASS</span></div>
  <div class="mci-tile"><img src="{IMG}/p3.jpg" alt="Two dancers folded together in the dark, black and white" loading="lazy"><span class="chip">OPEN JAM</span></div>
  <div class="mci-tile"><img src="{IMG}/p7.jpg" alt="A reaching hand caught in soft light" loading="lazy"><span class="chip">COMMUNITY</span></div>
</div>

{_ig_section()}

{_gallery("band-home.jpg", "Two dancers moving together in long exposure, black and white",
          "NEW HERE? COME AS YOU ARE.",
          "Follow along on Instagram for jam reminders, photos, and updates.",
          _ig_pill("terracotta"), tall=True)}
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/",
            "Contact Improvisation in Miami | Miami Contact Improv",
            "A weekly contact improv jam in Miami: class then open jam every Friday, 7 to 9 PM, at Inner Motion Dance Studio. All levels, no experience needed.",
        ),
        {
            "@type": "Place",
            "@id": schema.SITE + "/#place",
            "name": "Miami, Florida",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Miami",
                "addressRegion": "FL",
                "addressCountry": "US",
            },
            "geo": {"@type": "GeoCoordinates", "latitude": 25.7617, "longitude": -80.1918},
        },
        listings.friday_jam_event(),
    )
    return page(
        "Contact Improvisation Miami | Weekly Jam & Class",
        "A weekly contact improv jam in Miami where dance meets touch, trust and play. Class then open jam every Friday, 7 to 9 PM, at Inner Motion Dance Studio. No experience needed.",
        "/",
        body,
        jsonld=jsonld,
    )


# ---------------------------------------------------------------- Events
def events():
    body = f"""
<div class="mci-view">
<p class="mci-eyebrow">Jams &amp; workshops</p>
<h1 class="mci-h">UPCOMING EVENTS</h1>

<div class="mci-jam-card">
  <div>
    <p class="label mci-h">WEEKLY JAM</p>
    <p>Every Friday from Oct 2, 2026 &middot; 7:00&ndash;9:00 PM<br>Class 7:00&ndash;7:45, Open Jam 7:45&ndash;9:00<br>Inner Motion Dance Studio &middot; 216 NE 1st Ave, Hallandale Beach<br><a href="/friday-jam" style="color:var(--peach);text-decoration:underline;">Full details &rarr;</a></p>
  </div>
  <span class="price">$20 &ndash; $50 sliding scale</span>
</div>

<p class="mci-label">Registered events</p>
<div class="mci-two">
  <div class="mci-info-card">
    <div class="head"><span>EVENTBRITE</span></div>
    <div class="body">
      <h3>Ticketed sessions</h3>
      <p>Online registration will open here once ticketing is live. The weekly jam needs no booking &mdash; just come to the door.</p>
    </div>
  </div>
  <div class="mci-info-card">
    <div class="head"><span>LUMA</span></div>
    <div class="body">
      <h3>Special workshops</h3>
      <p>One-off workshops and intensives will be bookable here. In the meantime, follow Instagram for announcements.</p>
    </div>
  </div>
</div>
</div>

{_gallery("band-events.jpg", "A contact improv duet in soft green light, one dancer lifted",
          "THE ROOM IS THE TEACHING.",
          "A short class to warm up the tools, then an open jam where anyone can dance. Come solo or bring a friend.",
          '<a class="mci-pill terracotta" href="/friday-jam">About the jam &rarr;</a>',
          eyebrow="Every Friday")}

<div class="mci-view">
<p class="mci-label" style="margin-top:56px;">More Contact Improv in Miami</p>
<div class="grid">
  <a class="card" href="/miami-jams"><span class="tag">Verified list</span><h3>Miami &amp; Broward jams</h3><p>Every recurring Contact Improv session we could verify across Miami-Dade and Broward, with sources and checked dates.</p></a>
  <a class="card" href="/classes"><span class="tag">Learn</span><h3>Classes &amp; workshops</h3><p>Where to take a class, what to expect, and what to look for in a teacher.</p></a>
  <a class="card" href="/your-first-jam"><span class="tag">New here</span><h3>Your first jam</h3><p>Step by step: what to wear, when to arrive, and what actually happens in the room.</p></a>
</div>

<div class="mci-center">
  <p>Follow Instagram for the fastest updates on jam changes and special events.</p>
  {_ig_pill("dark")}
</div>
</div>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/events",
            "Upcoming events | Miami Contact Improv",
            "Upcoming contact improv jams and workshops in Miami: the weekly Friday jam at Inner Motion Dance Studio, plus verified local sessions and classes.",
        ),
        schema.breadcrumb("/events", "Events"),
        listings.friday_jam_event(),
    )
    return page(
        "Contact Improv Miami | Upcoming Jams & Events",
        "Upcoming contact improv jams and workshops in Miami: the weekly Friday jam at Inner Motion Dance Studio, 7 to 9 PM, plus verified local sessions and classes.",
        "/events",
        body,
        jsonld=jsonld,
    )


# ---------------------------------------------------------------- About
ABOUT_FAQ = [
    ("Do I need dance experience?",
     "No. Most people who come have zero dance background. We start every session with a short class covering the basics of weight-sharing and safe falling."),
    ("What should I wear?",
     "Comfortable clothes you can move in. No shoes &mdash; we dance barefoot or in socks. Avoid zippers, buckles, or jewellery that could catch on a partner."),
    ("Is it a partner dance like tango?",
     "No fixed roles or steps &mdash; contact improv is improvised. You will dance with many different people over a session, and no partner is required to attend."),
    ("How much does it cost?",
     "The weekly jam is $20&ndash;$50 sliding scale &mdash; pay what fits your budget. Special workshops may have a set price, listed on the event page."),
]


def about():
    faq_items = "".join(
        f'<div class="item"><button class="q" type="button" aria-expanded="false">'
        f'<span class="qt mci-h">{q}</span><span class="ic">+</span></button>'
        f'<p class="a">{a}</p></div>'
        for q, a in ABOUT_FAQ
    )
    body = f"""
<div class="mci-view">
<p class="mci-eyebrow">About the practice</p>
<h1 class="mci-h">WHAT IS CONTACT IMPROV?</h1>
<p style="font-size:17px;line-height:1.75;color:var(--body);max-width:700px;margin:0 0 20px;">Contact improvisation is an improvised dance form built on physical contact between two or more moving bodies. Rather than following set steps, dancers respond in real time to weight, momentum, and touch &mdash; rolling, lifting, falling, and catching as the moment calls for it.</p>
<div class="mci-video">
  <iframe src="https://www.youtube.com/embed/q4wUEiHowSU?rel=0" title="What is Contact Improv" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
<p style="font-size:17px;line-height:1.75;color:var(--body);max-width:700px;margin:0 0 24px;">Miami Contact Improv is a community jam for anyone curious about the form &mdash; dancers, movers, and total beginners alike. Every week starts with a short class to warm up the tools, followed by an open jam where anyone can dance. Anyone can stop at any moment, for any reason &mdash; the dance simply continues. Want the longer version? Read <a href="/what-is-contact-improvisation">what contact improvisation is</a>, or how <a href="/safety-and-consent">safety and consent</a> work in the room.</p>
</div>

{_gallery("band-about.jpg", "Two dancers folded together in low light, black and white",
          "NO CHOREOGRAPHY. NO MIRRORS. NO PRESSURE.",
          "Just weight, momentum and touch, shared moment to moment &mdash; and the freedom to stop whenever you need to.",
          "", eyebrow="The practice")}

<div class="mci-view">
<p class="mci-label" style="margin-top:56px;">Facilitator</p>
<div class="mci-facilitator">
  <div class="photo"><img src="/assets/facilitator.png" alt="Max Petrusenko, facilitator of Miami Contact Improv"></div>
  <div class="bio">
    <p class="name mci-h">MAX PETRUSENKO</p>
    <p class="role">Facilitator &middot; Somatic practitioner</p>
    <p>Max hosts the weekly Miami Contact Improv jam and works as a somatic practitioner between South Florida and Bali. His approach to contact improv centres on presence &mdash; listening through weight, momentum, and touch &mdash; with clear, ongoing consent at the heart of every session.</p>
    <p>He also co-creates blindfolded movement experiences with Blindfold Miami, exploring how we move and connect when sight steps aside.</p>
    <div class="links">
      <a class="fill" href="https://www.instagram.com/max.petrusenko/" target="_blank" rel="noopener">@max.petrusenko</a>
      <a class="line" href="https://www.maxpetrusenko.com/somatic" target="_blank" rel="noopener">Somatic work &rarr;</a>
    </div>
  </div>
</div>

<p class="mci-label">FAQ</p>
<div class="mci-accordion">
  {faq_items}
</div>

<div id="submit" style="margin-top:56px;">
  <p class="mci-label">About this site &amp; listings</p>
  <div class="prose">
    <p>miamicontactimprov.com is an independent, non-commercial community resource. It hosts the weekly jam above and also maps the wider Contact Improvisation scene across Miami-Dade and Broward &mdash; jams, classes and teachers &mdash; publishing only what can be verified and saying plainly what cannot.</p>
    <p>Run a jam, class or workshop in South Florida? Email <a href="mailto:hello@miamicontactimprov.com">hello@miamicontactimprov.com</a> and we will add it to the <a href="/directory">directory</a>. A listing is free, is never ranked, and links to your own page.</p>
  </div>
</div>
</div>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/about",
            "About Miami Contact Improv",
            "What contact improvisation is, who facilitates the Miami jam, and answers to the questions newcomers ask most.",
            about=[{"@id": schema.SITE + "/what-is-contact-improvisation#page"}, {"@id": schema.SITE + "/about#facilitator"}],
        ),
        {
            "@type": "Person",
            "@id": schema.SITE + "/about#facilitator",
            "name": "Max Petrusenko",
            "jobTitle": "Facilitator, Miami Contact Improv",
            "description": "Hosts the weekly Miami Contact Improv class and open jam; somatic practitioner working between South Florida and Bali.",
            "url": "https://www.maxpetrusenko.com",
            "sameAs": ["https://www.instagram.com/max.petrusenko/", "https://www.maxpetrusenko.com/somatic"],
            "affiliation": {"@id": schema.ORG_ID},
            "image": schema.SITE + "/assets/facilitator.png",
        },
        schema.breadcrumb("/about", "About"),
        schema.faq([(q, a.replace("&mdash;", "—").replace("&ndash;", "–")) for q, a in ABOUT_FAQ]),
    )
    return page(
        "About Contact Improv in Miami & the Facilitator",
        "What contact improvisation is, who facilitates the weekly Miami jam, and answers to the questions newcomers ask most about coming to their first jam.",
        "/about",
        body,
        jsonld=jsonld,
    )


# ---------------------------------------------------------------- Contact
def contact():
    body = f"""
<div class="mci-view">
<p class="mci-eyebrow">Say hi</p>
<h1 class="mci-h">GET IN TOUCH</h1>

<div class="mci-contact-grid">
  <div class="intro">
    <p>Questions about a jam, want to bring a group, or interested in facilitating a workshop? Reach out &mdash; or find us on Instagram for the fastest reply. You can also email <a href="mailto:hello@miamicontactimprov.com">hello@miamicontactimprov.com</a>.</p>
    {_ig_pill("dark")}
  </div>

  <form class="mci-form" id="mci-signup">
    <p class="title mci-h">JOIN THE MAILING LIST</p>
    <input type="text" name="name" placeholder="Your name" autocomplete="name" aria-label="Your name">
    <input type="email" name="email" placeholder="Email address" autocomplete="email" aria-label="Email address">
    <button type="submit">Sign up</button>
    <p class="note">Sign-up opens your email app with a message to us &mdash; we add you by hand and never share your address.</p>
  </form>
</div>
</div>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/contact",
            "Contact | Miami Contact Improv",
            "Get in touch with Miami Contact Improv: ask about a jam, bring a group, propose a workshop, or join the mailing list.",
        ),
        schema.breadcrumb("/contact", "Contact"),
    )
    return page(
        "Contact | Miami Contact Improv",
        "Get in touch with Miami Contact Improv: ask about a jam, bring a group, propose a workshop, or join the mailing list for jam reminders and updates.",
        "/contact",
        body,
        jsonld=jsonld,
    )
