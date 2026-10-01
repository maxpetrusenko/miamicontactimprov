"""Checkout-adjacent pages: pricing and the post-checkout success page.

Both are English-only (no Spanish route in locales.ROUTES), on the same footing as
/events, /contact and /about: a page about this site's own commercial mechanics,
not a translated library page.
"""

from shell import answer, band, buy_button, cite_block, facts, page
import schema

VENUE = "Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009"


# ---------------------------------------------------------------- pricing
def pricing():
    rows = f"""
<div class="price-list">
  <div class="price-row">
    <div class="price-text"><strong>Drop-in, online &mdash; $20.</strong><br>Promotion codes apply.
      <p class="price-note">Online sales close two hours before each class; after that it is $30&ndash;$50 pay-what-you-can at the door.</p>
    </div>
    {buy_button("ticket", "Buy ticket &ndash; $20", "pricing-ticket")}
  </div>

  <div class="price-row">
    <div class="price-text"><strong>At the door &mdash; $30&ndash;$50, pay what you can.</strong>
      <p class="price-note">No booking. Come to the door; nobody is turned away over money.</p>
    </div>
  </div>

  <div class="price-row">
    <div class="price-text"><strong>Intro 3-class pack &mdash; $45.</strong><br>For first-timers. Promotion codes apply.</div>
    {buy_button("intro", "Buy intro pack &ndash; $45", "pricing-intro")}
  </div>

  <div class="price-row">
    <div class="price-text"><strong>Monthly, unlimited &mdash; $60/month.</strong>
      <p class="price-note">Promotion codes apply to the drop-in ticket and the intro pack above. They do not apply to memberships.</p>
    </div>
    {buy_button("monthly", "Buy monthly &ndash; $60/mo", "pricing-monthly")}
  </div>

  <div class="price-row">
    <div class="price-text"><strong>Annual, prepaid &mdash; $540</strong> (about $45/month).</div>
    {buy_button("annual", "Buy annual &ndash; $540", "pricing-annual")}
  </div>
</div>
"""
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Pricing</p>
    <h1>What a class, a jam, or a membership costs.</h1>
    <p class="lede">One ticket price for the door, one for online, and two ways to pay for more than one session at a time. Every option checks out through a Stripe-hosted page; nothing here asks for a card on this site.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("A single class or jam is $20 online or $30 to $50 at the door, pay what you can. First-timers can buy a 3-class pack for $45. Coming every week costs $60 a month or $540 a year. Promotion codes apply to the $20 ticket and the $45 intro pack; they do not apply to either membership.")}
    {rows}
    {answer("If we cancel a class or jam, we refund you: tickets in full, memberships prorated.", label="Refund policy")}
    <div class="prose">
      <p>Every price above is for the same weekly Friday session at {VENUE}: a class from 7:00 to 7:45, then an open jam from 7:45 to 9:00. A ticket or a membership gets you in the door the same way a $20 to $50 cash payment always has &mdash; nothing changes about the room itself.</p>
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
            "What a Friday class or jam costs in Miami: a $20 online ticket, $30 to $50 at the door, a $45 intro pack for first-timers, or a $60 monthly or $540 annual membership.",
        ),
        schema.breadcrumb("/pricing", "Pricing"),
    )
    return page(
        "Pricing | Miami Contact Improv Classes & Jams",
        "What a Friday Contact Improv class or jam costs: $20 online, $30 to $50 at the door, a $45 intro pack, or $60 a month / $540 a year for unlimited classes.",
        "/pricing",
        body,
        jsonld=jsonld,
    )


# ---------------------------------------------------------------- success
def success():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">You're checked out</p>
    <h1>You're in.</h1>
    <p class="lede" id="mci-success-line">Your membership is active &mdash; come to any Friday class, 7&ndash;9 PM.</p>
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
    {band("See you on the floor", "No ticket ID or QR to bring - just show up. The door will have your name if you bought in advance.", [("Your first jam, step by step", "/your-first-jam", "primary"), ("All pricing", "/pricing", "secondary")])}
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
