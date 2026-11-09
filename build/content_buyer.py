"""Buyer-intent landing pages (SEO hack H006, flag seo_h006, site scope).

Short, conversion-focused pages for purchase-intent searches. Keyword in title, H1 and slug,
one clear CTA. English only. Every fact below is copied from /pricing and /fundamentals; no
new prices, dates or claims. The jam has no online ticket yet, so the jam page's CTA is the
class ticket (the jam follows the class every Friday) and the pricing page.

These pages exist only while the flag is on: build/locales.py and build/build.py both read
PAGES here through seo_flags.site_enabled("seo_h006").
"""

from shell import answer, buy_button, cite_block, facts, page
import schema

VENUE = "Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009"

from buyer_routes import ROUTES, SITEMAP  # noqa: E402


def class_tickets():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Tickets &middot; Fridays &middot; Hallandale Beach</p>
    <h1>Contact improv class tickets in Miami: $20 online.</h1>
    <p class="lede">Buy a ticket for the Friday contact improv class at Inner Motion Dance Studio. No partner and no dance experience needed.</p>
    <div class="btn-row">
      {buy_button("class", "Buy ticket &ndash; $20", "buyer-class-hero")}
      <a class="btn secondary" href="/fundamentals">See the eight-week series</a>
    </div>
    <p class="micro">Promotion codes apply. Online sales close two hours before class.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("A contact improv class ticket in Miami costs $20 online. After online sales close, the door takes $30 to $50, pay what you can. Classes are Fridays, 7:00 to 7:45 PM, in Hallandale Beach.")}
    {facts([
      ("Ticket", "$20 online, promotion codes apply"),
      ("At the door", "$30&ndash;$50, pay what you can, no booking needed"),
      ("When", "Fridays, class 7:00&ndash;7:45 PM, then an open jam until 9:00 PM"),
      ("Where", VENUE),
      ("Online sales", "Close two hours before each class"),
      ("Refunds", "If we cancel a class, we refund your ticket in full"),
    ])}
    <div class="prose">
      <h2>Before you buy</h2>
      <p>Checkout opens on a Stripe-hosted page; this site never asks for a card. If $20 is the reason you are hesitating, pay what you can at the door instead. Nobody is turned away over money.</p>
      <p>Want to know what the class teaches first? <a href="/fundamentals">Fundamentals</a> covers the eight Fridays, and <a href="/your-first-jam">your first jam</a> explains the open dance afterwards. Full prices are on the <a href="/pricing">pricing page</a>.</p>
    </div>
    <div class="btn-row">
      {buy_button("class", "Buy ticket &ndash; $20", "buyer-class-foot")}
    </div>
    {cite_block("Miami Contact Improv (2026). <em>Contact improv class tickets in Miami</em>. miamicontactimprov.com. https://miamicontactimprov.com" + ROUTES["buy-class-tickets"])}
  </div>
</section>
"""
    path = ROUTES["buy-class-tickets"]
    desc = "Contact improv class tickets in Miami: $20 online or $30 to $50 pay-what-you-can at the door. Fridays in Hallandale Beach."
    return page(
        "Contact Improv Class Tickets, Miami | Miami Contact Improv",
        desc, path, body,
        jsonld=schema.render(
            schema.organisation(), schema.website(),
            schema.webpage(path, "Contact Improv Class Tickets in Miami", desc),
            schema.breadcrumb(path, "Contact improv class tickets in Miami"),
        ),
    )


def jam_cost():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Cost &middot; Fridays &middot; Hallandale Beach</p>
    <h1>Contact improv jam cost in Miami: pay what you can at the door.</h1>
    <p class="lede">The Friday jam takes $30 to $50 at the door, pay what you can, with no booking. The class ticket before it is $20 online.</p>
    <div class="btn-row">
      {buy_button("class", "Buy class ticket &ndash; $20", "buyer-jam-hero")}
      <a class="btn secondary" href="/friday-jam">Friday jam details</a>
    </div>
    <p class="micro">There is no online jam-only ticket yet. See <a href="/pricing">pricing</a> for what is bookable.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("A contact improv jam in Miami costs $30 to $50 at the door, pay what you can, and needs no booking. Every Friday a class runs 7:00 to 7:45 PM and the open jam follows until 9:00 PM at Inner Motion Dance Studio in Hallandale Beach.")}
    {facts([
      ("Door price", "$30&ndash;$50, pay what you can"),
      ("Booking", "None needed at the door"),
      ("Class ticket", "$20 online, promotion codes apply"),
      ("When", "Fridays, class 7:00&ndash;7:45 PM, open jam 7:45&ndash;9:00 PM"),
      ("Where", VENUE),
      ("Money", "Nobody is turned away over money"),
    ])}
    <div class="prose">
      <h2>What you get for it</h2>
      <p>A jam is an open session with no teacher. You dance with whoever is willing, sit out when you like, and decline any invitation. <a href="/jams">How a jam works</a> and <a href="/safety-and-consent">how consent works in the room</a> are worth reading before your first one.</p>
      <p>New to this? Buy the class ticket above: the class teaches the basics, then you stay for the jam.</p>
    </div>
    {cite_block("Miami Contact Improv (2026). <em>Contact improv jam cost in Miami</em>. miamicontactimprov.com. https://miamicontactimprov.com" + ROUTES["buy-jam-cost"])}
  </div>
</section>
"""
    path = ROUTES["buy-jam-cost"]
    desc = "Contact improv jam cost in Miami: $30 to $50 pay what you can at the door, no booking. Fridays in Hallandale Beach."
    return page(
        "Contact Improv Jam Cost in Miami | Miami Contact Improv",
        desc, path, body,
        jsonld=schema.render(
            schema.organisation(), schema.website(),
            schema.webpage(path, "Contact Improv Jam Cost in Miami", desc),
            schema.breadcrumb(path, "Contact improv jam cost in Miami"),
        ),
    )


# slug, builder, sitemap priority, changefreq. Consumed by build.py when the flag is on.
PAGES = [
    ("buy-class-tickets", class_tickets, *SITEMAP["buy-class-tickets"]),
    ("buy-jam-cost", jam_cost, *SITEMAP["buy-jam-cost"]),
]
