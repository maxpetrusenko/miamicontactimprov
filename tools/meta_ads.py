#!/usr/bin/env python3
"""Drive the Contact Improv Miami Fundamentals ad test through Meta's Marketing API.

Subcommands, one job each:

    plan                        print the campaign tree that the message bank and the
                                posters on disk describe. Needs no token.
Nothing is written to Meta unless a token exists *and* `--live` is passed. Without both,
the tool prints the exact requests it would send, one per line, and exits 0. Every object
it does create is PAUSED, so a mistake costs a click in Ads Manager rather than money.

Request shapes were read from developers.facebook.com on 2026-09-21:

* current version, and the versions table (`v26.0`, released 2026-07-29):
  https://developers.facebook.com/docs/graph-api/changelog/
* `POST /act_{ad_account_id}/adimages` - multipart `bytes`, returns a map keyed by file
  name with `hash` on each entry:
  https://developers.facebook.com/docs/marketing-api/reference/ad-image/
  https://developers.facebook.com/documentation/ads-commerce/marketing-api/reference/ad-account/adimages
* `POST /act_{ad_account_id}/adcreatives` - `object_story_spec` with `page_id` and
  `link_data` (`link`, `message`, `name`, `image_hash`, `call_to_action`):
  https://developers.facebook.com/docs/marketing-api/reference/ad-creative/
* `POST /act_{ad_account_id}/campaigns` - `objective`, `special_ad_categories`,
  `daily_budget`, `bid_strategy`:
  https://developers.facebook.com/documentation/ads-commerce/marketing-api/reference/ad-account/campaigns
* `POST /act_{ad_account_id}/adsets` - `campaign_id`, `billing_event`,
  `optimization_goal`, `targeting`:
  https://developers.facebook.com/docs/marketing-api/reference/ad-campaign/
* `POST /act_{ad_account_id}/ads` - `adset_id`, `creative={"creative_id": ...}`,
  `status`:
  https://developers.facebook.com/docs/marketing-api/reference/adgroup/
* `GET /{ad_set_id}/insights?level=ad&fields=...`:
  https://developers.facebook.com/docs/marketing-api/insights/

This file owns the campaign: the message bank, the naming, the commands and the kill
line. The Graph surface it calls - request builders, the sender, the Doppler reads and
the attribution join - is `tools/meta_ads_graph.py`. The bank is read by
`tools/message_bank.py`, which is standard library only, so the tool runs from cron on
whatever interpreter the machine already has.

Budget is set on the campaign and not on the ad set: the test is one CBO, and Meta rejects
an ad set budget inside a campaign that already has one, so `adset_request` deliberately
omits `daily_budget`.

`utm_content` carries the ad name rather than Meta's numeric ad id, because the creative
that holds the link is built before the ad exists. Meta returns the id afterwards, and the
name is deterministic, so `report` maps id to name and joins on that.

The join reads our own numbers from the Worker admin endpoint:

    GET {endpoint}/api/admin/attribution?utm_content=<ad names>
    -> {"counts": {"<ad name>": {"signups": n, "registrations": n, "attended": n}}}

When that read fails or the token is missing the table prints Meta's numbers with `-1` in
the count columns and says why. It never prints zeros for data it does not have, and
`prune` refuses to pause anything on Meta's numbers alone: a click is not a signup.

Secrets come from Doppler `api_keys/dev` at runtime: `META_AD_ACCOUNT_ID`,
`META_ADS_TOKEN` (system user with `ads_management` and `ads_read`), `META_PAGE_ID`,
`BRIGHTBEAN_STUDIO_PLATFORM_FACEBOOK_APP_ID`, `NEWSLETTER_ADMIN_TOKEN`. A dry run lists
which of them are present. Values are never printed, not even on failure.

Usage:
    python3 tools/meta_ads.py plan
The operator's side of this - what Max does in Ads Manager, and what the repo does - is
`docs/ads/meta-runbook.md`.
"""

import argparse
import datetime
import pathlib
import re
import sys
import urllib.parse

import message_bank
import meta_ads_graph as api

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANK = ROOT / "docs" / "ads" / "messages.yaml"
POSTERS = ROOT / "docs" / "ads" / "out"

FORMATS = ("feed", "story")

HELP = {
    "plan": "print the campaign tree; no token needed",
}


# ------------------------------------------------------------------------------ the bank
def slug(text: str) -> str:
    """Metas, file names and utm values all want this: lowercase, hyphens, nothing else."""
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")



def ad_name(family: str, identity: str, fmt: str, day=None) -> str:
    """`ci_<family>_<identity>_<format>_<yyyymmdd>`, the name used in Ads Manager."""
    day = day or datetime.date.today()
    return f"ci_{slug(family)}_{slug(identity)}_{fmt}_{day:%Y%m%d}"



def creative_name(family: str, identity: str, fmt: str) -> str:
    return f"{ad_name(family, identity, fmt)}_creative"



def landing_url(bank: dict, family: str, name: str) -> str:
    """The ad's destination. `h=` picks the headline variant on /start (slice 11)."""
    query = {"h": family, "utm_source": "meta", "utm_medium": "paid",
             "utm_campaign": api.CAMPAIGN_NAME, "utm_content": name}
    return bank["landing"].split("?")[0] + "?" + urllib.parse.urlencode(query)



def load_bank() -> dict:
    """docs/ads/messages.yaml, through the standard-library reader."""
    bank = message_bank.load(BANK)
    if not bank.get("landing") or not bank.get("families"):
        raise SystemExit("messages.yaml has no landing address or no families")
    return bank



def targets(bank: dict, exists=None):
    """One row per ad: family, identity word, message, format, poster, name and link.

    Every row is checked against its poster on disk. An ad pointing at a missing or
    half-rendered PNG is worse than no ad, because Meta would serve it. Rows with no
    poster come back in `missing` so `plan` can name them.
    """
    exists = exists or api.poster_exists
    rows, missing = [], []
    for family, spec in (bank.get("families") or {}).items():
        body = (spec.get("body") or "").strip()
        for message in spec.get("messages") or []:
            identity = message["identity"]
            for fmt in FORMATS:
                png = POSTERS / family / f"{message['slug']}-{slug(identity)}-{fmt}.png"
                if not exists(png):
                    missing.append(png)
                    continue
                name = ad_name(family, identity, fmt)
                rows.append({
                    "family": family, "identity": identity, "fmt": fmt, "png": png,
                    "name": name, "link": landing_url(bank, family, name),
                    "creative_name": creative_name(family, identity, fmt),
                    "headline": message["headline"], "subline": message["subline"],
                    "body": body,
                })
    return rows, missing



def cmd_plan(args) -> int:
    bank = load_bank()
    rows, missing = targets(bank)
    if not rows:
        # The same rule tools/gate.py holds to: a check that measured nothing is not
        # green. A plan with no ads is a broken bank or a missing render.
        print("plan produced no ads: no poster in docs/ads/out/ matched the bank",
              file=sys.stderr)
        return 2
    budget = getattr(args, "budget", 40)
    print(f"campaign  {api.CAMPAIGN_NAME}  objective=OUTCOME_TRAFFIC  "
          f"daily_budget=${budget:.0f}  status=PAUSED  (CBO: the budget is here, "
          f"not on the ad set)")
    print(f"ad set    {api.ADSET_NAME}  {api.GEO['radius']} mi around the studio, "
          f"{api.AGE_MIN}-{api.AGE_MAX}, facebook+instagram, "
          f"optimization_goal=LINK_CLICKS")
    print(f"ads       {len(rows)}")
    for row in rows:
        print(f"  {row['name']}")
        print(f"      {row['png'].relative_to(ROOT)}")
        print(f"      {row['link']}")
    if missing:
        print(f"\n{len(missing)} poster(s) named by the bank are not on disk; render them "
              f"with: python3 tools/ad_statics.py")
        for path in missing:
            print(f"  {path.relative_to(ROOT)}")
    return 0



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="meta_ads.py", description="Meta ads operator for the CI Fundamentals series")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help=HELP["plan"])
    plan.add_argument("--budget", type=float, default=40,
                      help="campaign daily budget in dollars (default 40)")

    return parser



def main() -> int:
    args = build_parser().parse_args()
    handlers = {
        "plan": cmd_plan,
    }
    return handlers[args.command](args)



if __name__ == "__main__":
    # A crash is a broken operator, not a finding: exit 2, so a cron job and a human can
    # tell it apart from a refusal to touch anything.
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        print(f"\nmeta_ads could not run: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)
