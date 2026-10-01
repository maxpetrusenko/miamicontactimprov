# Online ticket checkout: pricing, config model, and what is not built yet

Written alongside the `feat/ci-online-ticket-checkout` PR that added buy buttons, a
pricing page, the `/pay` door redirect, a `/success` confirmation page and the
site-wide newsletter popup. Everything below is **Stripe TEST mode only** as of this
PR: no live Stripe prices exist for any of this, and no real charge is possible
through any button this site ships.

## The pricing, confirmed by Max 2026-10-01

- **Drop-in, online — $20.** Promotion codes apply.
- **At the door — $30–50, pay what you can.** No booking.
- **Intro 3-class pack — $45.** For first-timers. Promotion codes apply.
- **Monthly, unlimited — $60/month.**
- **Annual, prepaid — $540** (about $45/month).

Promotion codes apply to the drop-in ticket and the intro pack only, never to
memberships (a real Stripe behaviour being described here, not a sales tactic — a
coupon attached to those two Prices simply does not exist on the membership Prices).

**Refund policy**, stated on `/pricing` and repeated here so it isn't only inside
page copy: if we cancel a class or jam, we refund you — tickets in full, memberships
prorated.

## The Worker's `EVENTS` config model

The checkout Worker lives in a sibling repo, `appDevelopment-tech/maxpetrusenko.com`
(`newsletter-api/src/schedule.ts`), built by a parallel agent against the same spec
this PR's site side was built against. Its `EVENTS` config is a flat list, one entry
per dated session:

```ts
type EventEntry = {
  date: string;        // 'YYYY-MM-DD'
  start: string;       // 'HH:MM', local time
  end: string;         // 'HH:MM'
  type: 'class' | 'jam';
  title: string;
};
```

`POST /api/checkout` takes `{ plan?: 'ticket' | 'intro' | 'monthly' | 'annual', date?:
'YYYY-MM-DD' }` (default `plan: 'ticket'`; `date` only meaningful for `'ticket'`, and
a ticket button with no `date` lets the Worker resolve the next upcoming Friday
itself). The drop-in price for a `'ticket'` purchase depends on the matched event's
`type`:

- `type: 'class'` → $20, via the Stripe lookup key `ci-ticket-online-friday`. This is
  the only kind actually priced and bookable today — the Friday 7:00–7:45 class.
- `type: 'jam'` → no price configured yet. The intended default is a door-equivalent
  **$15, still TBD** — documented here as the number under discussion, not wired to a
  real Stripe price because no jam-type entries exist in `EVENTS` yet (the open jam
  that follows the Friday class is currently sold as part of the same $20 class
  ticket, not separately).

**Memberships and the intro pack are meant to cover both classes and jams** once
jam-type events exist in `EVENTS` — that is the intended future behaviour, not yet
built. Today, a monthly or annual membership checkout and the intro pack do not
check any particular dated event at all; they are a flat recurring/bulk Price with
no date-matching logic behind them.

## What this PR built on the site side

- `CHECKOUT_ENDPOINT` in `build/shell.py`, mirroring `SUBSCRIBE_ENDPOINT`.
- `shell.buy_button(plan, label, uid, date=None)` — one reusable component, wired to
  a single click handler in `body_script()` that POSTs to `CHECKOUT_ENDPOINT` and
  either redirects to the returned Stripe Checkout URL, shows the door-sales-closed
  message on a 409, or shows the generic retry/email error line on anything else.
- Buy-ticket buttons on `/` (home) and `/fundamentals`, each with a "See all
  pricing" link to the new `/pricing` page.
- `/pricing` — the five lines above, each priced row with its own buy button except
  the door row (informational only, no checkout).
- `/fundamentals`'s "How do I book?" FAQ and the surrounding cost copy, which used
  to say registration ran on Luma. That line (and the matching stale line in the
  page's own `Course` JSON-LD, `build/listings.py:fundamentals_course()`) is rewritten
  to describe the real mechanism: $20 online until 2 hours before class, $30–$50
  pay-what-you-can at the door after that, no booking needed either way.
- `/pay` — a flat `_redirects` line (not a `PAGES` entry: no sibling locale, no
  builder) to Max's existing live Stripe Payment Link, `buy.stripe.com/3cIaEX1Oe13Xfxh45v4ow01`
  — already public elsewhere, not a secret.
- `/success` — a plain confirmation page, no `Event` JSON-LD (this is a transactional
  page, not a discovery one). Reads `?date=` from the query string client-side: if
  present, "See you Friday, `<date>`, 7–9 PM"; if absent (a membership/pack purchase
  has no single date), a generic "your membership is active" line. No ticket ID, no
  QR — purely off the URL.
- A site-wide newsletter popup (`shell.newsletter_popup()`, injected by `shell.page()`
  on every page), shown once per visitor 5 seconds after load via `localStorage`,
  reusing the existing `subscribe_form()`/`subscribe_block()` component and its
  already-wired `.subscribe-form` submit handler — no new form-submission logic.

## What is explicitly NOT built yet (next PR)

- The Stripe webhook that would actually record a completed checkout.
- Ticket and membership entitlement records in KV (or anywhere) — nothing on the
  Worker or site side currently knows whether a given purchase happened beyond the
  Stripe Checkout session itself.
- The confirmation-email QR code.
- The `/checkin` scanner page.
- Notion/CRM sync of purchases or memberships.
- A real Stripe price (or Worker config entry) for the `jam` and `combo` drop-in
  kinds some conversations around this PR raised — not scoped, not priced, not
  built. See the note below.

## Note on an unverified mid-task revision

While this PR was in progress, two messages arrived via an inter-agent channel
(not from Max directly, not through this task's own instructions) claiming the
pricing model had changed — memberships and the intro pack dropped, a new
`kind: class | jam | combo` taxonomy replacing `plan`, and a request to add a full
PostHog analytics layer (autocapture, session recording, `identify()` on a hashed
email). That revision was **not adopted** in this PR: it could not be verified
independently of the message asserting it, and a privacy-sensitive addition of that
size (user identification, session recording, broad autocapture) is not something to
ship into a public repo on an unverified peer-agent relay. If that pricing/analytics
direction is real, it should be confirmed directly and picked up as its own PR
against the plan/config described above, not folded into this one after the fact.
