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

## Decisions from Max (2026-10-04, after the first preview)

- **Stripe account:** the same one the tests ran on ("Blindfolded Experience",
  acct_1L2x...). Its rename or a new account is handled elsewhere; nothing here touches
  account settings.
- **Prices:** online ticket is a **$20 to $40 sliding scale** (Stripe `custom_unit_amount`,
  preset $20, lookup key `ci-class-sliding`); the door is **$30 to $50**, pay what you can;
  community and first class stay **$15**. `/tickets`, `/pricing`, `/pay` and the buy buttons
  say the same. Stripe refuses promotion codes on a custom-amount price, so **no online
  ticket takes a code now**; the newsletter's 20% code (a Luma code) no longer applies to
  the website ticket.
- **Community $15 is verified, not trusted** (below).

## Community $15 verification (`src/verify.ts`)

`POST /api/community/verify { email, share_url? , screenshot? }`:

1. **Link:** normalised (https only, no IP hosts, tracking params and fragment stripped, our
   own pages and Luma refused), fetched with a named bot user agent, read from `og:title`,
   `og:description`, `<title>` and body text. Pass = it contains one of `miamicontactimprov`,
   `ci miami`, `contact improvisation`, `contact improv`, `contactimprov`.
2. **Screenshot** (offered after any failed link: Instagram and Facebook usually show a login
   page): downscaled in the browser to 1280 px JPEG, read by Workers AI
   `@cf/meta/llama-4-scout-17b-16e-instruct` on the same Worker. The keyword check runs on
   the text the model returns, never on its own judgement.
3. **One post per email:** `post:<sha256(url)>` and `img:<sha256(bytes)>` belong to the first
   email that verified them; another email gets `used`.
4. **Evidence:** every attempt, pass or fail, is stored as `evidence:<id>` (email, method,
   URL, matched keyword, 400-char excerpt) in `COMMUNITY` KV; admins list it with
   `GET /api/community/evidence`.
5. Checkout `{ ticket_type: community, email, verification_id }` needs verified evidence for
   that email, younger than 24 h, and writes `share_url`, `verified=true`, `method=url|ocr`
   and `verification_id` into Stripe metadata. The email is locked on the Checkout page.

**Known gap:** any public page that mentions contact improv passes the link check (the
preview test used the Wikipedia article). If that gets abused, narrow the keywords for links
to `miamicontactimprov` / `ci miami` / the event link, which a real share carries.

## User flows (slice 1)

1. **Online $20 to $40.** `/tickets` → pick a Friday → "Buy ticket" → Stripe Checkout with the price editable from $20 to $40 (no codes).
2. **Community $15.** Share the class → paste the link to the post (or a screenshot) and an
   email on `/tickets` → verified → Stripe Checkout at $15 (superseded the self-reported
   channel + handle version; see "Community $15 verification").
3. **New here, $15.** Email + consent → `POST /api/first-class` records the offer on the
   subscriber record (always answers `{ ok: true }`) → `/api/checkout` with `ticket_type: first`
   checks KV and Stripe → a $15 Checkout with the email locked. If the price is not available
   (paid before, a session already open, offer never issued, Stripe unreachable) the answer is
   one uniform 409 `first_offer_unavailable`, and the page offers the community price.
4. **Friend link.** `miamicontactimprov.com/fr/maya-lopez` → `/tickets` via a 200 rewrite (the
   page reads the name from the path; Pages leaves `:name` unsubstituted in a query string, so a
   302 to `/tickets?ref=:name` arrived as `ref=%3Aname`, caught on the preview) →
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
| `share_url` | the verified post link, normalised (community, link method) |
| `verified`, `method`, `verification_id` | `true`, `url` or `ocr`, evidence id (community only) |
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

## Slice 3: /ideas (built in these PRs, preview only)

`/ideas` (site `build/content_ideas.py`, Worker `src/ideas.ts`, KV binding `IDEAS`): seven idea
cards (CI + Acro, Eros Contact, Tantra and Bodywork Lab, Parents CI + Kids Hangout, CI + Live
Music, Outdoor and Beach CI, Extended Jam) plus "Suggest something". Each shows "N interested.
At T we schedule it." and a bar; Parents shows "N/10 families, K kids". Click → email + consent
once (remembered on the device) → Definitely / Probably / Just curious → "N more needed" with a
share link `/ideas?ref=<share code>#<idea>`; `?ref=` is stored on the interest row. One row per
person per idea; internal weight 2 for a past ticket buyer, the public number is people.
Suggestions are stored as pending and shown only after `POST /api/ideas/suggestions/approve`
(admin token). Linked from the nav ("Ideas") and the ticket success page.

## Preview (Stripe TEST, 2026-10-04)

- Site: https://mci-pricing-preview.pages.dev (separate Pages project `mci-pricing-preview`,
  `X-Robots-Tag: noindex`). A branch preview of the `miamicontactimprov` project cannot work:
  the account-level `pages_dev_canonicalization` Bulk Redirect (include_subdomains) 301s every
  `*.miamicontactimprov.pages.dev` host to production.
- Worker: https://newsletter-api-preview.max-petrusenko.workers.dev (`wrangler deploy --env
  preview`, own KV namespaces `preview-EMAIL_SUBS`/`-AMBASSADORS`/`-IDEAS`, Stripe test key,
  test-mode webhook endpoint `we_1UMv3AGR8ZpP3RhoPzbhEn9n`, no Resend, admin token in Doppler
  `api_keys/dev CI_IDEAS_PREVIEW_ADMIN_TOKEN`).
- Rebuild the preview site: `MCI_API_BASE=https://newsletter-api-preview.max-petrusenko.workers.dev
  python3 build/build.py --out <copy of site/>`, append the noindex header to its `_headers`,
  `wrangler pages deploy <dir> --project-name=mci-pricing-preview --branch=main`.
- Playwright on the preview (third round): `/tickets` → "Buy ticket" opens Stripe at $20 with
  the price editable up to $40; community link `https://example.com/` fails with the retry
  message and the screenshot field appears; a link that mentions contact improvisation passes
  → $15 Checkout → test card 4242 → `/success` → "Add your vote" → `/ideas` count +1,
  Definitely, "N more people needed"; a second buyer's Instagram link fails, a screenshot
  (`ocr-test-story.jpg`) is read by Workers AI and passes → $15 Checkout. Stripe metadata:
  `ticket_type=community, verified=true, method=url|ocr, share_url`. Screenshots (desktop and
  phone): `docs/media/pricing-ambassador/preview/`.
- /tickets and /ideas now use only the site's existing components (hero, `.answer`, `.facts`,
  `.price-list`, `.band`, `.card` in `.grid`, `.subscribe-block` forms, `.cite`). The form block's
  label and consent text were near-invisible on its sage background; they are cream now, which
  also fixes the same form on `/fundamentals`.

### Go-live order (Max, not done in these PRs)

1. Live Stripe account: the same one as test (decided by Max 2026-10-04).
2. Create the live price: `python3 scripts/stripe_setup.py --live --only ci-class-15 --confirm "I am creating a LIVE Stripe object"`.
3. Create the live sliding price: `python3 scripts/stripe_setup.py --live --only ci-class-sliding --confirm "I am creating a LIVE Stripe object"`.
4. Create the production KV namespaces `AMBASSADORS`, `IDEAS` and `COMMUNITY`
   (`wrangler kv namespace create ...`), add both bindings with their ids to the top level of
   `wrangler.jsonc`, seed the first ambassador slugs. Without `IDEAS` the live `/ideas` page
   shows zeros and its buttons fail; without `COMMUNITY` the $15 community option fails.
   Workers AI (`ai` binding) is already in `wrangler.jsonc`; it bills per use on the account.
5. In Stripe (live), add a webhook endpoint `https://newsletter-api.max-petrusenko.workers.dev/api/stripe/webhook`
   for `checkout.session.completed`, `checkout.session.async_payment_succeeded`,
   `checkout.session.expired`; `wrangler secret put STRIPE_WEBHOOK_SECRET` with its `whsec_`.
6. `wrangler secret put STRIPE_SECRET_KEY` with the live key and set `STRIPE_MODE` to `live` in
   `wrangler.jsonc` in the same change (the guard refuses a mismatch).
7. Merge and deploy the Worker PR. Smoke-test: `/api/checkout` early returns a live Checkout URL.
8. Merge the site PR (deploys from main). Until step 7 is live, the $15 buttons on `/tickets`
   answer "That did not go through".
9. Buy one $15 ticket end to end, check the metadata in the dashboard, refund it.

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
