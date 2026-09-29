# Meta ads runbook

Two halves. The creative half, from Slice 11, covers the posters, the landing page, the
events and the weekly loop. The operator half, from Slice 12, is `tools/meta_ads.py` and
what it does to the ad account. The split matters: the repo writes everything a reader
sees, and the operator creates everything paused, so nothing spends money until Max says so.

## The creative half

### What the repo hands over

| Artifact | Where it lives | What to do with it |
| --- | --- | --- |
| 24 posters | `docs/ads/out/<family>/<slug>-<identity>-<format>.png` | Upload the ones for the family you are launching. `uv run tools/ad_statics.py` rebuilds them and overwrites the same names |
| Primary text | `body` in `docs/ads/messages.yaml`, one block for each family | Paste it as the ad's primary text, whole. The four blocks run 149 to 196 words |
| Poster text | `headline` and `subline` in `docs/ads/messages.yaml` | Already rendered into the PNG. The headline is what the reader sees first |
| Landing page | `site/start.html`, built from `build/content_practice.py` | The ad link points here. `?h=<family>` swaps the h1 and the line under it |
| Events | `POST /api/events` on the `newsletter-api` Worker | Fires Lead, CompleteRegistration and Attend into the pixel |

### Campaign structure

| Setting | Value |
| --- | --- |
| Campaigns | one, named `ci_fundamentals`, with CBO |
| Ad sets | one for the launch, plus a second for the zombie set |
| Location | 25 miles around Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach |
| Age | 21 to 60 |
| Targeting | none. No interests, no lookalikes, no custom audiences at launch |
| Ads | one for each poster, 24 in the bank today. The review suggests running 10 to 20 at a time, so launching a subset is a real choice |
| Objective | Leads, optimised for the Lead event once the pixel has a day of history |
| Second ad set | the zombie set. Ads that collected no spend move here on a small budget and get one more chance |

The creative does the targeting. A poster aimed at climbers finds climbers, and the
primary text describes the person rather than the class.

### Budget and the kill rules

The daily budget sits on the campaign and its current value is written in the operator
half, in "Numbers this test commits to". The review's phrasing is $5 to $10 for each
creative per day, and that is what it means when each ad is its own small test. Inside one
CBO there is a single pool, so the number to watch is the one on the campaign, and the
$60 threshold below only means something if the campaign can reach it inside a week.

- Thursday, pause anything with zero signups after $30 spent.
- Stop any concept that costs more than $40 for each attendee after $60 spent.
- A first-timer is worth about $75. That is $30 for each of an expected 2.5 classes.
- Cost for each attendee decides. CTR and cost for each signup are diagnostics, not
  verdicts.
- Sunday, move the budget to the winners and move the unspent ads to the zombie set.

`prune --max-cpa 40 --min-spend 60` is the same line, executed.

### Naming

`ci_<family>_<identity>_<format>_<yyyymmdd>`

- family is `movement`, `anxiety`, `social` or `exercise`
- identity is one of the eight words with its spaces written as hyphens, so `new to Miami`
  becomes `new-to-miami`
- format is `feed` or `story`
- date is the day the ad goes live, as `yyyymmdd`

Examples: `ci_anxiety_new-to-miami_feed_20260928`,
`ci_exercise_acro-people_story_20260928`.

Those same words are in the poster's file name, so an ad in Ads Manager matches a PNG in
the repo without opening either one.

### The link every ad carries

```
https://miamicontactimprov.com/start?h=anxiety&src=meta&utm_source=meta&utm_medium=paid&utm_campaign=ci_fundamentals&utm_content=ci_anxiety_new-to-miami_feed_20260928
```

- `h` picks the headline and takes `movement`, `anxiety`, `social` or `exercise`. Anything
  else, or nothing at all, leaves the page's own copy in place.
- `src=meta` rides on the end of the signup source, which becomes
  `miamicontactimprov:start:meta`. Paid signups land in the list with the welcome email,
  and they stay separable from the ones that came off the door QR or the Instagram bio.
- `utm_content` carries the ad name, which is what ties a signup record back to the poster
  that produced it.

The subscribe form reads all of it when someone submits, from the address they arrived on.
Nothing needs setting up on the page.

### Events

Three events score the test.

| Event | Means | Fired when |
| --- | --- | --- |
| Lead | a signup | right after a form submit the Worker accepted |
| CompleteRegistration | a paid place in the series | the Luma guest export or the booking confirmation |
| Attend | a body in the room | someone checks in at the door |

Cost for each attendee is the number that decides spend, so Attend is the one to keep
honest. It is a custom event name because Meta has no standard one, and it reads the same
in Events Manager.

The Worker sends these from the server. The site carries no pixel and sets no cookie, so
`fbp` and `fbc` do not exist for us and the only match key is the address, hashed with
SHA-256 inside the Worker. The hash is also the default event id, so a retried batch counts
one person once.

Create the pixel in Events Manager, then set the two secrets:

```
npx wrangler secret put META_PIXEL_ID
npx wrangler secret put META_CAPI_TOKEN
```

Until both exist, `POST /api/events` logs the event and answers 202 with
`forwarded: false`. That is not a failure. It is the endpoint saying it did its job and had
nowhere to send the result.

The admin token lives in Doppler as `NEWSLETTER_ADMIN_TOKEN` in `api_keys`, config `dev`.
Keep it in an environment variable and out of the shell history.

```
export NEWSLETTER_ADMIN_TOKEN="$(doppler secrets get NEWSLETTER_ADMIN_TOKEN -p api_keys -c dev --plain)"
curl -sS -X POST https://newsletter-api.max-petrusenko.workers.dev/api/events \
  -H "Authorization: Bearer $NEWSLETTER_ADMIN_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"event":"Lead","email":"reader@example.com","event_source_url":"https://miamicontactimprov.com/start?h=anxiety"}'
{"ok":true,"event":"Lead","forwarded":false}
```

The body takes `event`, `email`, and optionally `event_id`, `value`, `currency`,
`event_source_url`, `client_ip_address` and `client_user_agent`. Send the last two only
when they came off the attendee's own device. An address from Max's laptop tells Meta the
wrong person was there, and that costs match quality instead of buying it.

Set `META_TEST_EVENT_CODE` while rehearsing. Events carrying it stay out of the reported
numbers.

### The weekly loop

| Day | Work |
| --- | --- |
| Monday, one hour | Read what won last week. Write new messages into `docs/ads/messages.yaml`, run `uv run tools/ad_statics.py`, upload the PNGs, then let the operator create the tree paused |
| Thursday | Pause anything with zero signups after $30 spent |
| Sunday | Move the budget to the winners, move the unspent ads to the zombie set, and copy the winning headline into the page |

Copying the winning headline means two edits in one commit, then a rebuild. The poster copy
lives in `docs/ads/messages.yaml`, and the page's own copy lives in
`build/content_practice.py` at `START_HEADLINES`, where the first entry of a family is the
default.

### Who does what

| In Ads Manager, by hand | In the repo |
| --- | --- |
| Attach the payment method and connect the Page | Produces the PNG, the headline and the primary text |
| Flip an ad from paused to active | Never touches a live ad |
| Pause an ad that missed its numbers | Never deletes anything |
| Read spend, link clicks and cost for each attendee | Reads signups, registrations and attendance from its own records |

Everything that changes what a reader sees ships from this repo. Everything that spends
money waits for Max's hand on the switch.

## The operator, `tools/meta_ads.py`

Four subcommands. Nothing reaches Meta unless a token exists and `--live` is passed. Every
dry run prints the exact requests it would send and exits 0, so the tool is safe to run at
any time, including from a fresh clone with no secrets.

Every object the tool creates is PAUSED. Two paused objects and a paused ad set cost
nothing. Max sets the campaign active in Ads Manager after checking the previews.

    python3 tools/meta_ads.py plan
    python3 tools/meta_ads.py launch --budget 40
    python3 tools/meta_ads.py report
    python3 tools/meta_ads.py prune --max-cpa 40 --min-spend 60

The tool is standard library plus `requests`. `requests` is only imported when something
is actually sent, so `plan` and every dry run work on a bare interpreter. The message bank
is read by `tools/message_bank.py`, which is standard library only and deliberately
refuses YAML it does not understand (quotes, flow collections, folded scalars) instead of
guessing at ad copy.

### plan

Reads `docs/ads/messages.yaml` and `docs/ads/out/**.png`, then prints the campaign tree:
one campaign, one ad set, and one line per ad with its poster and its landing link. 24 ads
when the bank and the renderer agree.

An ad whose poster is missing is listed as missing and left out of the tree. Nothing is
invented to fill the gap, and a plan that finds no ads at all exits 2, because a check that
measured nothing is not a pass.

### launch

Uploads each poster to `/adimages`, builds one creative per ad with the family body copy
as the primary text, then creates one campaign, one ad set and the ads.

Budget sits on the campaign, not on the ad set: this test is one CBO, and Meta rejects an
ad set budget inside a campaign that already has one. `--budget 40` is dollars per day.

The dry run ends with a count of the write requests and the read that runs first, so a
change in the number of ads is visible before anything is sent.

`utm_content` carries the ad name, for example `ci_movement_climbers_feed_20260921`, not
Meta's numeric ad id. The creative holds the link and is built before the ad exists, so
there is no id to put in it yet. The name is deterministic and the report maps id to name,
so the join lands on the same ad either way.

### report

Reads `/insights` at the ad level for the ad set: spend, link clicks, cost per link click.
It then asks the Worker admin endpoint for our own counts by `utm_content`, and prints
signups, registrations and attendance alongside Meta's numbers.

A count we do not have prints as `-1`, never as `0`, and its cost column prints `-`. A
column of zeros reads like a campaign that failed, and a real zero has to mean a real zero.
When the join is unavailable the table says why and still prints everything Meta knows.

The table goes to stdout. A short digest of the same numbers goes to Max on Telegram
through `hermes send`: the three cheapest ads by cost per attendee, anything over the line,
and the total spend. `--no-notify` keeps it on stdout, which is what the cron job uses
because the cron delivers the table itself.

### prune

Pauses ads past the kill line. Nothing is ever deleted. It refuses to pause anything when
the attribution join is unavailable: a click is not a signup, and stopping the ads that
work is the expensive mistake here.

The kill line is `--max-cpa 40 --min-spend 60`, read as cost per attendee, with the weekly
loop's faster rule available by passing `--min-spend 30` and reading the signup column.

An ad is paused when either of these is true:

* it has spent the minimum and has no signups at all;
* it has spent the minimum and its cost per attendee is over `--max-cpa`.

Below the minimum spend nothing is judged. An ad with signups and no attendees yet is not
judged either, because people register before the class and cost per attendee is not
knowable until the class has happened.

### Cron

Two jobs run `report`, Thursdays 09:00 and Sundays 09:00 ET, from max-mini. Each prints
the table, and the job delivers that output to Telegram.

`prune` has no cron. It runs when Max replies `prune ci`, which is the point: the kill
decision stays with a human until the numbers have earned the automation.

## Secrets

Read at runtime from Doppler `api_keys/dev`, with the proxy variables removed from the
child environment so the read does not hang:

| secret | what it is |
| --- | --- |
| `META_AD_ACCOUNT_ID` | the ad account id, `act_…` added by the tool if missing |
| `META_ADS_TOKEN` | system user token with `ads_management` and `ads_read` |
| `META_PAGE_ID` | the Contact Improv Miami Page, from the `fb` worker |
| `BRIGHTBEAN_STUDIO_PLATFORM_FACEBOOK_APP_ID` | the existing app the token belongs to |
| `NEWSLETTER_ADMIN_TOKEN` | reads our own counts for the report join |

A dry run prints which of them are present and never a value. Missing secrets are a dry
run, not an error, and exit 0.

## Max's three steps

Nothing else in this tool is manual.

1. Create the ad account under the Meta Business and attach a payment method.
2. Create a System User with `ads_management` on it, then put the token and the account id
   in Doppler `api_keys/dev` as `META_ADS_TOKEN` and `META_AD_ACCOUNT_ID`.
3. Connect the Contact Improv Miami Page to the ad account, once the `fb` worker has
   created it, and put the page id in Doppler as `META_PAGE_ID`.

Until step 3 lands, `launch` will not run live: the creative needs a `page_id`, and a
creative without one is rejected by Meta rather than created in a broken state.

## Numbers this test commits to

* 24 statics: four families, three messages each, feed and story.
* One campaign `ci_fundamentals`, one ad set `ci_fundamentals_broad_25mi`.
* 25 mile radius around the studio, age 21 to 60, Facebook and Instagram.
* $40 per day at the campaign, `LOWEST_COST_WITHOUT_CAP`.
* Names: `ci_<family>_<identity>_<format>_<yyyymmdd>`, one ad per identity word.
* Kill line: $40 per attendee after $60 spent, or no signups after the minimum spend.
* Landing: `/start?h=<family>&utm_source=meta&utm_medium=paid&utm_campaign=ci_fundamentals&utm_content=<ad name>`.

## Tests

    python3 -m unittest discover -s tests

Covers the bank reader against both a fixture and the real `messages.yaml`, the naming, the
plan arithmetic (24 ads, two objects plus three calls per ad, everything paused, the budget
on the campaign), and the kill line. No network, no secrets, no `requests`.

## When something looks wrong

* `plan` reports fewer ads than 24: the bank and the posters disagree. Run
  `python3 tools/ad_statics.py`, then `plan` again. The missing posters are named.
* Every count column reads `-1`: the attribution join did not answer. The line above the
  table says why, usually a missing `NEWSLETTER_ADMIN_TOKEN` or a non-200.
* `launch --live` stops on a Graph error: the message names the request. Check the ad
  account id and whether the Page is connected to the ad account.
* Nothing is created unpaused, so cleanup after a bad launch is deleting paused objects in
  Ads Manager, not stopping spend.
