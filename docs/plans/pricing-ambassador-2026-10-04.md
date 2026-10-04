---
read_when: changing ticket prices, /tickets, /fr/<name> referral links, the Worker's /api/checkout or /api/first-class, or anything that reads Stripe Checkout metadata (ambassador ledger, CRM sync).
---

# Pricing and ambassadors: Phase 0 brief and slice plan (2026-10-04)

Source: Max's direction notes, `~/Desktop/Projects/CI/01-plan/pricing-ambassador-ideas-2026-10-04.md`
(approved for build on 2026-10-04). This doc covers slice 1 as built, and the slices after it.

## Problem

The Friday class sells through three channels that don't share data: Luma (most of the Oct 2
registrations), the live Stripe Payment Link behind `/pay` (door QR), and the test-mode
`/api/checkout` from PR #14 ($20 online). Nobody can tell which attendee brought whom, there is no
reward for spreading the class, and a newcomer sees one price ($20) with no reason to commit
before Friday.

Max's direction: three visible prices (door $30, early $20, community $15), a $15 first class for
people who leave an email, a personal `/fr/<name>` link per attendee, and Stripe as the single
record of which offer each sale used.

## How tickets sell today (as of 2026-10-04)

- **Luma** event pages (`luma.com/hau1fq5t` for Oct 2): registration and payment. 13 of 15 Going
  paid, $260. Luma owns that data; no referral attribution.
- **`/pay`**: redirects to a live Stripe Payment Link (`buy.stripe.com/3cIa...`), door price
  $30 to $50 pay-what-you-can. Gleb paid $30 through it on Oct 2.
- **Website $20 checkout** (PR #14 site, PR #23 Worker): `POST /api/checkout` on the
  `newsletter-api` Worker builds a Stripe Checkout Session from lookup key
  `ci-ticket-online-friday`, promotion codes on. The Stripe "Friday class (online)" product.
  Gloribel paid $20 this way on Oct 2.
- **Codes**: Luma coupon `6SEYIV` (10%, public), the newsletter 20% Luma code.

## Prior art and mechanics checked

- **Stripe Checkout metadata**: `metadata[...]` on the session plus
  `payment_intent_data[metadata][...]` puts the same keys on the PaymentIntent, so a refund or
  dashboard search from either object shows the offer. Values up to 500 chars; an empty value
  means "unset", so empty fields are not sent.
- **Stripe promotion codes**: a code can carry metadata and a `max_redemptions`, and a session's
  `allow_promotion_codes` is all or nothing. That is why the $15 sessions turn codes off: it is
  the only way to stop a 20% code stacking on $15.
- **Stripe list Checkout Sessions** accepts `status=complete` and `customer_details[email]`
  (verified against the test account). That answers "has this email paid for a class before"
  with no webhook and no database, which is what makes the first-class offer enforceable in
  slice 1.
- **Referral link patterns** (Dropbox, Uber, Luma-less community studios): a short vanity path
  that sets attribution, plus a fallback code for people who type rather than tap. Cloudflare
  Pages `_redirects` supports placeholders (`/fr/:name /tickets?ref=:name 302`), so a static
  site can carry the link with no server.
- **Verification**: the plan rejects screenshots and Instagram API checks for a $5 difference.
  Community is self-reported; spot-check later.

## User flows (slice 1)

1. **Early $20.** `/tickets` → pick a Friday → "Buy for $20" → Stripe Checkout (codes allowed).
2. **Community $15.** Share the class link → on `/tickets` pick the channel (Instagram story,
   WhatsApp group, Facebook group, somewhere else) and type a handle or group name → "Unlock
   $15" → Stripe Checkout at $15, codes off. No verification.
3. **New here, $15.** Email + consent → `POST /api/first-class` records the offer on the
   subscriber record (always answers `{ ok: true }`) → `/api/checkout` with `ticket_type: first`
   checks KV and Stripe → a $15 Checkout with the email locked. If the price is not available
   (paid before, a session already open, offer never issued, Stripe unreachable) the answer is
   one uniform 409 `first_offer_unavailable`, and the page offers the community price.
4. **Friend link.** `miamicontactimprov.com/fr/maya-lopez` → 302 → `/tickets?ref=maya-lopez` →
   a dark panel "Maya Lopez sent you. Your class is $15." → $15 Checkout with `referrer`.
5. **Door $30.** Information only on `/tickets`. The `/pay` link and its $30 to $50 range are
   unchanged (see decisions).

## Data model: Stripe metadata is the record

Every session from `/api/checkout` carries, on the session and its PaymentIntent:

| key | values |
|---|---|
| `ticket_type` | `early`, `community`, `first`, `referral` |
| `event` | Friday date, `YYYY-MM-DD` (also kept as `class_date` for PR #23 compatibility) |
| `kind`, `product` | `class`, `ci-class` |
| `share_channel` | `instagram_story`, `whatsapp_group`, `facebook_group`, `other` (community only) |
| `handle` | free text, 80 chars max (community only) |
| `referrer` | `/fr/<name>` slug, `^[a-z0-9][a-z0-9-]{0,39}$` (referral only) |
| `referrer_verified` | `true` when the slug is in the `AMBASSADORS` allowlist, else `false` (referral only) |
| `first_discount` | `true` (first only) |

Prices (lookup keys, created by `scripts/stripe_setup.py`): `ci-ticket-online-friday` $20,
`ci-class-15` $15 (one price for all three $15 offers; `ticket_type` tells them apart).

KV (`EMAIL_SUBS`, the existing subscriber store) gains three fields on the subscriber record,
merged without touching existing fields: `first_offer_issued_at`, `first_discount_claimed`
(cached "yes" from Stripe or set by the webhook) and `first_pending_until`. Stripe stays the
source of truth. Emails are trimmed and lowercased everywhere before they are stored, compared
or sent to Stripe.

`AMBASSADORS` KV (separate namespace, keys `ambassador:<slug>`) is the allowlist. An unknown slug
still buys at $15 (the link worked for the buyer) but is tagged `referrer_verified=false`, so
the credit ledger can skip it. Seeding from the CRM promoter flag is slice 2; for now:
`wrangler kv key put --binding AMBASSADORS ambassador:max '{"name":"Max"}'`.

**Non-stacking and double-claim rules**:

- One price per session; `allow_promotion_codes` only on early; the $15 offers are class-only.
- First class needs an issued offer, no completed CI session for that email in Stripe, no
  `first_discount_claimed` flag, and no unexpired `first_pending_until`.
- Before a first-class session is created the Worker writes `first_pending_until` (now + 32
  min) and gives the session `expires_at` = minute bucket + 31 min (Stripe's minimum is 30). A
  second request while the marker stands gets the 409.
- KV has no compare-and-set, so two requests that both read before either writes can both pass.
  They send the same `Idempotency-Key` (sha256 of `email|event|first|minute`) and identical
  parameters, so Stripe returns one session to both. The remaining gap is two concurrent
  requests for different Fridays in the same instant; closing it fully needs a Durable Object.
- `POST /api/stripe/webhook` (signature checked with `STRIPE_WEBHOOK_SECRET`, 5 minute
  tolerance): `checkout.session.completed` (paid) and `async_payment_succeeded` set
  `first_discount_claimed` and clear the pending marker; `checkout.session.expired` on a
  first-class session clears the marker. It only updates existing subscriber records.
- Other ticket types use `sha256(client IP|event|type|channel|handle|referrer|minute)` as the
  idempotency key, or a random key when there is no IP, so a double click returns one session
  and two strangers never share one.

**Accepted $5 risks** (not worth more code at this price):

- Email aliases (`name+1@gmail.com`, dots in Gmail, a second address) get a second first class.
- People who paid through Luma or the `/pay` door link have no CI Checkout Session in Stripe
  under their email, so the first-class price still looks open to them.
- Community $15 is self-reported. Spot-check tags later.

**Abuse controls**: one 409 for every first-class refusal (no "has paid" oracle);
`POST /api/first-class` always answers `{ ok: true }`; Cloudflare rate limiting binding
`API_LIMITER`, 10 requests per 60 s per `CF-Connecting-IP` on every `/api/*` route except the
webhook; CORS locked to `miamicontactimprov.com` (and `www.`) for checkout routes, plus
`maxpetrusenko.com` for `/api/subscribe`, plus `EXTRA_ORIGINS` for local dev. Turnstile is
skipped for now: add it to `/api/first-class` if the rate limit is not enough.

**Stripe mode guard**: `STRIPE_MODE` (`test` by default, set in `wrangler.jsonc`) must match the
key prefix (`sk_test_`/`rk_test_` or `sk_live_`/`rk_live_`); a mismatch refuses checkout before
any Stripe call.

## Slice 1: walking skeleton (this PR)

Site (`maxpetrusenko/miamicontactimprov`): `build/content_tickets.py` (`/tickets` page and its
script), `/fr/:name` rule in `_redirects` (and `tools/serve.py` for local), `shell.API_BASE` /
`FIRST_CLASS_ENDPOINT` (`MCI_API_BASE` env overrides the Worker origin for a local build),
`checkout_completed` now carries `ticket_type`, a `/tickets` link on `/pricing`, CSS in
`site/assets/site.css`, `tests/test_tickets.py`.

Worker (`appDevelopment-tech/maxpetrusenko.com`, `nextjs/workers/newsletter-api/newsletter-api`):
`src/tickets.ts` (ticket rules, first-class capture), `ticket_type` handling in
`src/checkout.ts` (pending marker, expiry, idempotency key), `src/stripe.ts` (purchase lookup,
`customer_email`, PaymentIntent metadata, mode guard), `src/webhook.ts`, `src/http.ts` (CORS,
rate limit), routes `POST /api/first-class` and `POST /api/stripe/webhook`,
`test/tickets.spec.ts`, `test/hardening.spec.ts`, CI workflow
`.github/workflows/newsletter-api-tests.yml`. The site's `publish.yml` now runs
`python3 -m unittest discover -s tests` before deploy.

**Proof gate (met 2026-10-04, Stripe TEST mode only):**

- Worker: `npx vitest run` 84/84 (32 new: tickets, concurrent first-class sessions, mixed-case
  email, the uniform 409, idempotency, webhook signature and effects, allowlist, rate limit,
  CORS, mode guard). `tsc` clean; `wrangler deploy --dry-run` shows the rate limit binding.
- Site: `python3 -m unittest discover -s tests` 53/53 (after `tools/ad_statics.py`);
  `tools/gate.py` error=0 warn=0 over 94 pages.
- The E2E below ran before the review fixes, against the first version of the Worker.
- Local E2E (Playwright, local site → `wrangler dev` → Stripe test API): referral, community and
  first-class sessions created; first-class paid with test card 4242 and redirected to
  `/success?...&ticket_type=first`; same email refused afterwards. Session metadata read back
  with `stripe checkout sessions retrieve`. Screenshots: `docs/media/pricing-ambassador/`.

Local run:

```bash
# Worker: .dev.vars needs STRIPE_SECRET_KEY (test key). On Max's Mac, SSL_CERT_FILE points at
# the agent-vault MITM CA, which makes workerd reject Stripe's real certificate. Unset it:
env -u SSL_CERT_FILE -u NODE_EXTRA_CA_CERTS -u HTTPS_PROXY -u HTTP_PROXY npx wrangler dev --port 8787
# Site, pointed at the local Worker, built to a throwaway folder (never commit this build):
MCI_API_BASE=http://localhost:8787 python3 build/build.py --out /tmp/mci-local
```

### Go-live order (Max, not done in these PRs)

1. Decide the live Stripe account (open decision below).
2. Create the live price: `python3 scripts/stripe_setup.py --live --only ci-class-15 --confirm "I am creating a LIVE Stripe object"`.
3. Create the allowlist namespace: `wrangler kv namespace create AMBASSADORS`, add the binding
   with its id to `wrangler.jsonc`, seed the first slugs.
4. In Stripe (live), add a webhook endpoint `https://newsletter-api.max-petrusenko.workers.dev/api/stripe/webhook`
   for `checkout.session.completed`, `checkout.session.async_payment_succeeded`,
   `checkout.session.expired`; `wrangler secret put STRIPE_WEBHOOK_SECRET` with its `whsec_`.
5. `wrangler secret put STRIPE_SECRET_KEY` with the live key and set `STRIPE_MODE` to `live` in
   `wrangler.jsonc` in the same change (the guard refuses a mismatch).
6. Merge and deploy the Worker PR. Smoke-test: `/api/checkout` early returns a live Checkout URL.
7. Merge the site PR (deploys from main). Until step 6 is live, the $15 buttons on `/tickets`
   answer "That did not go through".
8. Buy one $15 ticket end to end, check the metadata in the dashboard, refund it.

## Next slices

2. **Ambassador credit ledger.** `checkout.session.completed` webhook on the Worker → count paid
   sessions per `referrer` (plus per-ambassador Stripe promotion codes like `MAX15` with
   `metadata.ambassador`, for people who type a code) → at 2 paid referrals, issue a one-use
   free-class promotion code; at 5, the second perk. Sync counts to the Notion CI CRM credit
   fields. Self-referral check by email. Proof: two test referrals produce one free code and the
   Notion row updates.
3. **/ideas demand page.** Idea cards with a public "N interested" counter and a threshold
   ("at 20+ we schedule it"), one click for identified people (signed token from email or
   `/success`), email capture otherwise, Definitely / Probably / Just curious follow-up, internal
   weights (past attendee 2). Counters in Worker KV. "What should we host next?" on `/success`.
   Proof: a click from `/success` increments the counter and records attendee weight.
4. **Parents CI with kids count.** An idea card (and later a ticket type) that records adults and
   kids separately, so the nanny + pizza cost per family can be priced. Proof: interest rows
   carry `adults` and `kids`; the card shows both totals.
5. Bring-a-friend bundles ($30 for 2, $40 for 3), webhook ticket records, QR check-in, CRM sync
   of every sale.
