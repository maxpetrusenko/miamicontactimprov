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
   subscriber record and checks Stripe for a past paid CI checkout → if none, straight to a $15
   Checkout with the email locked. Same email again after paying: "This email already has a
   class with us", and the community price is offered instead.
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
| `first_discount` | `true` (first only) |

Prices (lookup keys, created by `scripts/stripe_setup.py`): `ci-ticket-online-friday` $20,
`ci-class-15` $15 (one price for all three $15 offers; `ticket_type` tells them apart).

KV (`EMAIL_SUBS`, the existing subscriber store) gains two fields on the subscriber record,
merged without touching existing fields: `first_offer_issued_at` and `first_discount_claimed`.
The flag only caches a "yes" from Stripe; Stripe stays the source of truth.

**Non-stacking rules**: one price per session; `allow_promotion_codes` only on early; the
first-class price needs an issued offer for that email and no completed CI session for it;
the $15 offers are class-only (`kind` must be `class`).

## Slice 1: walking skeleton (this PR)

Site (`maxpetrusenko/miamicontactimprov`): `build/content_tickets.py` (`/tickets` page and its
script), `/fr/:name` rule in `_redirects` (and `tools/serve.py` for local), `shell.API_BASE` /
`FIRST_CLASS_ENDPOINT` (`MCI_API_BASE` env overrides the Worker origin for a local build),
`checkout_completed` now carries `ticket_type`, a `/tickets` link on `/pricing`, CSS in
`site/assets/site.css`, `tests/test_tickets.py`.

Worker (`appDevelopment-tech/maxpetrusenko.com`, `nextjs/workers/newsletter-api/newsletter-api`):
`src/tickets.ts` (ticket rules, first-class capture), `ticket_type` handling in
`src/checkout.ts`, `hasCompletedCiPurchase` and `customer_email` / PaymentIntent metadata in
`src/stripe.ts`, route `POST /api/first-class`, `test/tickets.spec.ts`.

**Proof gate (met 2026-10-04, Stripe TEST mode only):**

- Worker: `npx vitest run` 67/67 (15 new). Site: `python3 -m unittest tests.test_tickets` 11/11;
  `tools/gate.py` error=0 warn=0 over 94 pages.
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

**Before this goes live** (not done here, needs Max): deploy the Worker, create the `ci-class-15`
price in the live account (`stripe_setup.py --live --only ci-class-15 --confirm ...`), merge
and deploy the site. Until the Worker is deployed, the live `/tickets` page answers "That did not
go through" on the $15 options, so the two PRs must ship together, Worker first.

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
