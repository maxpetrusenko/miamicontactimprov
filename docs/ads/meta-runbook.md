# Meta ads runbook

The Slice 11 half of this runbook (campaign structure, naming, the weekly loop, what Max
does in Ads Manager against what the repo produces) is not in the tree yet. The operator
half below is the Slice 12 tool, `tools/meta_ads.py`. Append the Slice 11 section above it
rather than editing it.

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
