# Online ticket checkout: pricing, config model, analytics, and what is not built yet

Written alongside the `feat/ci-online-ticket-checkout` PR that added buy buttons, a
pricing page, the `/pay` door hand-off, a `/success` confirmation page, the
site-wide newsletter popup, and PostHog analytics. Everything checkout-related
below is **Stripe TEST mode only** as of this PR: no live Stripe prices exist for
any of this, and no real charge is possible through any button this site ships.

## How this PR's scope changed mid-build

This branch went through three rounds of direction from Max as the work was in
progress, and it's worth recording why the shipped result looks like it does:

1. **Round 1** — plan-based pricing: ticket $20 / intro pack $45 / monthly
   membership $60 / annual membership $540, keyed by a `plan` field.
2. **Round 2** — memberships (monthly, annual) and the intro pack deferred
   pending real data on class-vs-jam interest; replaced with a `kind`-based
   drop-in model: class $20, jam $15, class+jam combo $30.
3. **Round 3** — PostHog analytics added (a real project now exists), plus
   `/pay` rebuilt as a tracked page rather than a bare redirect.

The two builder agents assigned to this work (one for the Worker, one for the
site) each independently declined to adopt round 2 and round 3 when those
corrections arrived as inter-agent messages mid-task, on the correct grounds
that a peer agent's message cannot verify itself as coming from Max and
shouldn't authorize a scope or privacy change on its own say-so. That refusal
was the right call, not a bug to route around — so the orchestrating session
did the round 2/3 rework directly instead of pushing it back through an
unverifiable relay. If this history matters later: the plan-based build and
the class/jam/combo rework both exist in this branch's commit history, in that
order, rather than being squashed into one.

## The pricing, as shipped (confirmed by Max 2026-10-01)

- **Class, online — $20.** Promotion codes apply. The only kind with a real
  bookable date today.
- **Jam, online — $15.** Promotion codes apply. **Not bookable yet** — no
  jam-type date exists in the Worker's `EVENTS` config. `/pricing` states this
  plainly rather than hiding the row or showing a disabled button.
- **Class + jam, same day — $30.** Promotion codes apply. Same "not bookable
  yet" situation as jam, for the same reason (no `combo-capable` date exists).
- **At the door — $30–50, pay what you can.** No booking, unchanged, the
  existing live Stripe Payment Link.

**Refund policy**, stated on `/pricing`: *"If we cancel a class or jam, we
refund your ticket in full."*

### Deferred, not built, numbers recorded here only

Memberships and the intro pack are **not on the customer-facing site** — no
buttons, no mention on `/pricing`, no Stripe objects referenced from any page.
Recorded here for when class-vs-jam interest data makes them worth building:

- **Intro 3-class pack — $45.** For first-timers. Promotion codes would apply.
- **Monthly, unlimited — $60/month.**
- **Annual, prepaid — $540** (about $45/month, cancelled months would extend
  membership).

Promotion codes, if/when memberships ship, would apply to the drop-in ticket
and the intro pack only, never to memberships. Their Stripe test-mode prices
(`ci-intro-pack`, `ci-membership-monthly`, `ci-membership-annual`) already exist
from an earlier round of this PR but are unreferenced by any code — harmless to
leave, cheap to wire up again if this direction is picked back up.

## The Worker's `EVENTS` config model

The checkout Worker lives in a sibling repo, `appDevelopment-tech/maxpetrusenko.com`
(`newsletter-api/src/schedule.ts`). Its `EVENTS` config is a flat list, one entry
per dated session:

```ts
export type EventType = 'class' | 'jam' | 'combo-capable';

export interface ScheduledEvent {
  date: string;   // 'YYYY-MM-DD'
  start: string;  // full ISO-8601 with the America/New_York offset
  end: string;
  type: EventType;
  title: string;
}
```

`'class'` and `'jam'` are nights that run exactly one thing; `'combo-capable'`
is a night that runs both, so a buyer can purchase class, jam, or the combined
ticket for that date. All 8 configured Fundamentals Fridays (Oct 2 – Nov 20
2026) are `type: 'class'` — no `'jam'` or `'combo-capable'` entries exist yet.
This is deliberate future-proofing, not a gap to fill reflexively: jam and
combo nights get added to this list (with their own `ScheduledEvent` rows)
once Max schedules one, and the site/Worker need zero further changes to sell
them at that point — the button and pricing-row code is already generic over
`kind`.

`POST /api/checkout` takes `{ event_date?: 'YYYY-MM-DD', kind?: 'class' |
'jam' | 'combo' }` (default `kind: 'class'`). The drop-in price depends on
`kind`, via Stripe lookup key:

- `class` → $20, `ci-ticket-online-friday`
- `jam` → $15, `ci-jam-dropin`
- `combo` → $30, `ci-combo-dropin`

All three are one-time payments with promotion codes allowed — no Stripe
subscription mode anywhere in this slice. Requesting `jam` or `combo` today
answers `409 { closed: true, door_url: 'https://miamicontactimprov.com/pay' }`,
the same shape as a time-based sales-closed response: nothing sellable online
right now, door is the fallback either way.

## What this PR built on the site side

- `CHECKOUT_ENDPOINT` and `DOOR_PAYMENT_LINK` constants in `build/shell.py`.
- `shell.buy_button(kind, label, uid, event_date=None)` — one reusable
  component, wired to a click handler in `body_script()` that POSTs to
  `CHECKOUT_ENDPOINT` and either redirects to the returned Stripe Checkout URL,
  shows the door-sales-closed message on a 409, or shows the generic
  retry/email error line on anything else.
- A "Buy ticket – $20" button (`kind="class"`) on `/` (home) and
  `/fundamentals`, each with a "See all pricing" link to `/pricing`.
- `/pricing` — the four rows above (class / jam / combo / door), the refund
  line, no mention of memberships or the intro pack.
- `/fundamentals`'s cost copy and FAQ, and the matching line in the page's own
  `Course` JSON-LD (`build/listings.py:fundamentals_course()`), both rewritten
  earlier in this PR to drop a stale "registration runs on Luma" claim in favor
  of the real mechanism: $20 online until 2 hours before class, $30–$50
  pay-what-you-can at the door after that.
- `/pay` — a real page (`content_checkout.pay()`, a normal `PAGES` entry), not
  a bare `_redirects` rule. It fires a `pay_door_redirect` PostHog event and
  redirects via `window.location.replace(...)` after a short delay, with a
  `<meta http-equiv="refresh" content="2; ...">` no-JS fallback and a visible
  "continue to payment" link. This has to be a real page rather than a server
  redirect so that (a) the event actually fires and (b) PostHog can attribute
  whatever UTM params arrived on this URL (e.g. a printed door QR's
  `?utm_source=poster&utm_medium=qr`) before the visitor leaves for Stripe — a
  bare 302 runs no JS and would silently lose both.
- `/success` — a plain confirmation page, no `Event` JSON-LD (transactional,
  not a discovery page). Reads `?kind=`, `?event_date=` and `?amount=` from the
  query string client-side to personalize the message and fire
  `checkout_completed { kind, amount }`. No ticket ID, no QR — purely off the
  URL, by design (the webhook/entitlement work that would produce a real
  ticket ID is a later PR).
- A site-wide newsletter popup (`shell.newsletter_popup()`, injected by
  `shell.page()` on every page), shown once per visitor 5 seconds after load
  via `localStorage`, reusing the existing `subscribe_form()`/
  `subscribe_block()` component and its already-wired `.subscribe-form` submit
  handler.

## Analytics (PostHog)

A real PostHog project ("Contact Improv Miami", US cloud) now exists. The site
reads `POSTHOG_KEY` (the public `phc_...` client token — safe to appear in
built HTML, not safe to commit to this public repo's source) and
`POSTHOG_HOST` (default `https://us.i.posthog.com`) from the **build**
environment via `shell._posthog_config()`. Unset locally (the normal state of
this repo's source and of a local `python3 build/build.py` run with no env
var) → `shell.posthog_snippet()` returns an empty string, no PostHog script tag
is emitted at all, and every call site already checks `if (window.posthog)`
before using it — the whole layer is a clean no-op until a key is wired in.
Verified both ways during this PR: a build with `POSTHOG_KEY` unset emits zero
`posthog.init(` occurrences in the output; a build with a fixture key set
emits exactly one, with the right token and the right `maskTextSelector`.

**CI wiring (not done in this PR, documented here):** `.github/workflows/
publish.yml`'s build step needs `POSTHOG_KEY: ${{ secrets.POSTHOG_KEY }}` in
its env, reading a GitHub Actions secret on this repo that does not exist yet.
Max creates it (an agent should not run a command that sets a live secret) —
the exact command, once the real `phc_...` token is pulled from Doppler
`api_keys/prd CI_POSTHOG_KEY`:

```
doppler secrets get CI_POSTHOG_KEY --project api_keys --config prd --plain | gh secret set POSTHOG_KEY --repo maxpetrusenko/miamicontactimprov
```

**Client config** (`shell.posthog_snippet()`): PostHog's own loader snippet
(not a CDN `<script src>`, so the real library only loads once a key exists),
`defaults: '2026-05-30'` plus explicit `person_profiles: 'identified_only'`,
`capture_pageview: true`, `capture_pageleave: true`, `autocapture: true`, and
`session_recording: { maskAllInputs: true, maskTextSelector: 'input[type=
"email"], input[type="tel"], input[name="email"], input[name="phone"]' }` so
the newsletter form's email/phone fields are masked by selector, not just by
`type`, in case a future form's phone input lacks `type="tel"`. The whole
`posthog.init` call is skipped at runtime when the browser sends
`navigator.doNotTrack` — no cookie banner (US-only traffic, Max's call), DNT
is the only gate. UTM and referrer capture are PostHog's own automatic
`$initial_utm_*` behavior, nothing custom needed for that.

**Custom events fired**, all client-side, no PII in any property beyond the
identify exception below:

- `pricing_viewed` — on `/pricing` load.
- `buy_click { kind, event_date }` — on any buy button click, before the
  `fetch` to `/api/checkout`.
- `checkout_started { kind }` — right after a `200 { url }` response, just
  before the redirect to Stripe.
- `checkout_completed { kind, amount }` — on `/success` load, straight from its
  query string (the Worker's success URL carries `amount` in cents precisely
  so this page never has to guess or re-derive it).
- `newsletter_popup_shown` / `newsletter_popup_closed` /
  `newsletter_popup_submitted` — at the matching points in the popup
  lifecycle. `_submitted` only fires for the popup's own form instance (it
  checks `form.closest('#mci-popup')`), not every inline/footer subscribe form
  on the site.
- `pay_door_redirect { from: 'checkout_closed' | 'pay_page' }` — fired twice,
  deliberately: once on the closed-sale message's door link (click time, since
  that's a normal in-page navigation), and once on `/pay` itself (load time,
  since `/pay` is the page that actually attributes UTM params and needs to
  fire before its own redirect). The `from` property tells the two apart.

**Identify on newsletter submit**: after a successful subscribe response, the
shared `.subscribe-form` handler computes `crypto.subtle.digest('SHA-256', ...)`
over the trimmed, lowercased email and calls `posthog.identify(hash,
consentChecked ? { email } : {})`. The hash, never the raw address, is the
distinct id; the real email is attached as a person property only when the
reader ticked the consent checkbox the same handler already requires before
sending the subscribe call at all.

**Dashboard to build** (not built in this PR, PostHog project settings already
have autocapture/heatmaps/session replay/dead clicks/web vitals on at the
project level): a "CI funnel" view —

1. Traffic sources (PostHog's automatic UTM/referrer capture) → `pricing_viewed`
   → `buy_click` (broken down by `kind`) → `checkout_completed` (broken down by
   `kind`), as the core conversion funnel per drop-in kind.
2. Newsletter popup conversion: `newsletter_popup_shown` → `newsletter_popup_
   submitted`, as a separate view.
3. `pay_door_redirect` volume, broken down by the `from` property and, once
   outbound links are UTM-tagged (see below), by UTM source — to tell a
   printed-poster QR scan apart from any other route to the door link.

**Out of scope for this PR, explicitly**: tagging the actual outbound links
that would feed the funnel above with real UTM params. The printed door-QR
poster (`CI/09-print/ci-door-pay-poster.html`) and future WhatsApp/email
outreach links both live outside either repo touched by this PR — the poster
file is in `~/Desktop/Projects/CI/`, a separate, non-git, phone-number-
containing folder. `/pay` already correctly attributes whatever UTM params
arrive on it (confirmed: PostHog's automatic UTM capture needs no extra code
here), so pointing the printed QR at `/pay?utm_source=poster&utm_medium=qr`
and tagging outreach links with `?utm_source=whatsapp|email&utm_campaign=
ci-fundamentals` are both manual follow-ups for Max, not code changes.

## What is explicitly NOT built yet (next PR)

- The Stripe webhook that would actually record a completed checkout.
- Ticket and membership entitlement records in KV (or anywhere) — nothing on
  the Worker or site side currently knows whether a given purchase happened
  beyond the Stripe Checkout session itself.
- The confirmation-email QR code.
- The `/checkin` scanner page.
- Notion/CRM sync of purchases.
- Memberships and the intro pack as real, bookable, customer-facing things —
  see "Deferred, not built" above.
- Outbound UTM tagging on the printed door QR and outreach links — see above.
