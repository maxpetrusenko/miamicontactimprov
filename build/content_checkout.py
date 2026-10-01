"""Checkout-adjacent pages: pricing, the door-payment redirect, and the
post-checkout success page.

All three are English-only (no Spanish route in locales.ROUTES), on the same
footing as /events, /contact and /about: pages about this site's own
commercial mechanics, not translated library pages.
"""

from shell import answer, buy_button, cite_block, facts, page, DOOR_PAYMENT_LINK
import schema

VENUE = "Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009"

# Kept here, not just in shell.DOOR_PAYMENT_LINK, because pay() needs it for the
# no-JS <meta refresh> fallback. Both must read the same value; shell.py's
# comment on DOOR_PAYMENT_LINK is the source of truth if these ever drift.
DOOR_LINK = DOOR_PAYMENT_LINK


# ---------------------------------------------------------------- pricing
def pricing():
    rows = f"""
<div class="price-list">
  <div class="price-row">
    <div class="price-text"><strong>Class, online &mdash; $20.</strong><br>Promotion codes apply.
      <p class="price-note">Online sales close two hours before each class; after that it is $30&ndash;$50 pay-what-you-can at the door.</p>
    </div>
    {buy_button("class", "Buy ticket &ndash; $20", "pricing-class")}
  </div>

  <div class="price-row">
    <div class="price-text"><strong>Jam, online &mdash; $15.</strong><br>Promotion codes apply.
      <p class="price-note">Not bookable yet: no jam night has its own date in the schedule yet. This row becomes a button once one does.</p>
    </div>
  </div>

  <div class="price-row">
    <div class="price-text"><strong>Class + jam, same day &mdash; $30.</strong><br>Promotion codes apply.
      <p class="price-note">Not bookable yet, for the same reason as the jam row above.</p>
    </div>
  </div>

  <div class="price-row">
    <div class="price-text"><strong>At the door &mdash; $30&ndash;$50, pay what you can.</strong>
      <p class="price-note">No booking. Come to the door; nobody is turned away over money.</p>
    </div>
  </div>
</div>
"""
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Pricing</p>
    <h1>What a class or a jam costs.</h1>
    <p class="lede">One ticket price for the door, one for online. Every online option checks out through a Stripe-hosted page; nothing here asks for a card on this site.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("A class is $20 online or $30 to $50 at the door, pay what you can. Promotion codes apply to every online ticket.")}
    {rows}
    {answer("If we cancel a class or jam, we refund your ticket in full.", label="Refund policy")}
    <div class="prose">
      <p>Every Friday runs at {VENUE}: a class from 7:00 to 7:45, then an open jam from 7:45 to 9:00. A ticket gets you in the door the same way a cash payment always has &mdash; nothing changes about the room itself.</p>
    </div>
    {cite_block("Miami Contact Improv (2026). <em>Pricing</em>. miamicontactimprov.com. https://miamicontactimprov.com/pricing")}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/pricing",
            "Pricing | Miami Contact Improv",
            "What a Friday class or jam costs in Miami: a $20 online ticket or $30 to $50 at the door, pay what you can.",
        ),
        schema.breadcrumb("/pricing", "Pricing"),
    )
    return page(
        "Pricing | Miami Contact Improv Classes & Jams",
        "What a Friday Contact Improv class or jam costs: $20 online or $30 to $50 at the door, pay what you can.",
        "/pricing",
        body,
        jsonld=jsonld,
    )


# ---------------------------------------------------------------- pay
def pay():
    """Door-payment hand-off. A real page, not a bare _redirects rule, so

    PostHog can fire `pay_door_redirect` and attribute whatever UTM params
    arrived here (a printed door QR, for instance) before the visitor leaves
    for Stripe. See shell.body_script()'s `/pay` block for the JS redirect;
    this page's <meta refresh> in <head> is the no-JS fallback.
    """
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Door payment</p>
    <h1>Taking you to payment.</h1>
    <p class="lede">If this does not redirect automatically in a moment, <a href="{DOOR_LINK}">continue to payment</a>.</p>
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/pay",
            "Door Payment | Miami Contact Improv",
            "Redirects to the Stripe-hosted door payment page for Miami Contact Improv.",
        ),
    )
    return page(
        "Door Payment | Miami Contact Improv",
        "Redirects to the Stripe-hosted door payment page for Miami Contact Improv.",
        "/pay",
        body,
        jsonld=jsonld,
        extra_head=f'<meta http-equiv="refresh" content="2; url={DOOR_LINK}">',
    )


# ---------------------------------------------------------------- success
def success():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">You're checked out</p>
    <h1>You're in.</h1>
    <p class="lede" id="mci-success-line">Come to the door with your name &mdash; details below.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {facts([
      ("Where", VENUE),
      ("When", "Fridays, 7:00–9:00 PM. Class 7:00–7:45, open jam 7:45–9:00"),
    ])}
    <div class="prose">
      <h2>What to wear and bring</h2>
    </div>
    {facts([
      ("Clothing", "Loose, opaque, covers back, shoulders and knees. No zips, buckles or rough seams"),
      ("Feet", "Bare or soft non-slip socks. No shoes on the floor"),
      ("Water", "A full bottle. The floor is hot and humid in Miami"),
      ("Towel", "One. You will need it"),
      ("Jewellery", "Leave it off. Rings, watches and necklaces catch and cut"),
      ("Phone", "Silenced, face down, off the floor or at the edge"),
    ])}
    <div class="prose">
      <p>First time? <a href="/your-first-jam">Your first jam, step by step</a> walks through arriving, the opening circle and what the first ten minutes look like. Questions before Friday: <a href="mailto:hello@miamicontactimprov.com">hello@miamicontactimprov.com</a>.</p>
    </div>
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/success",
            "You're in | Miami Contact Improv",
            "Checkout confirmation for Miami Contact Improv: where the Friday class and jam are, what to wear, and what to bring.",
        ),
        schema.breadcrumb("/success", "Checkout complete"),
    )
    return page(
        "You're In | Miami Contact Improv",
        "Checkout confirmation for Miami Contact Improv: venue, what to wear, and what to bring to your first class or jam.",
        "/success",
        body,
        jsonld=jsonld,
    )
