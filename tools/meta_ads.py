#!/usr/bin/env python3
"""Drive the Contact Improv Miami Fundamentals ad test through Meta's Marketing API.

Subcommands, one job each:

    plan                        print the campaign tree that the message bank and the
                                posters on disk describe. Needs no token.
    launch --budget 40          upload the posters, create the creatives, the campaign,
                                the ad set and the ads. Everything is created PAUSED.
    report                      spend and clicks per ad from Meta, joined to our own
                                signup, registration and attendance counts. Prints the
                                table and sends Max the digest on Telegram.
    prune --max-cpa 40 --min-spend 60
                                pause the ads past the kill line. Pauses, never deletes.

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
    python3 tools/meta_ads.py launch --budget 40                 # dry run
    python3 tools/meta_ads.py launch --budget 40 --live          # token required
    python3 tools/meta_ads.py report
    python3 tools/meta_ads.py prune --max-cpa 40 --min-spend 60  # dry run, then --live

The operator's side of this - what Max does in Ads Manager, and what the repo does - is
`docs/ads/meta-runbook.md`.
"""

import argparse
import datetime
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse

import message_bank
import meta_ads_graph as api

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANK = ROOT / "docs" / "ads" / "messages.yaml"
POSTERS = ROOT / "docs" / "ads" / "out"

FORMATS = ("feed", "story")
JOINED = ("signups", "registrations", "attended")
HEAD = ("ad", "spend", "clicks", "$/click", "sign", "$/sign", "reg", "$/reg", "att", "$/att")
WIDTH = (30, 8, 6, 8, 5, 7, 5, 7, 5, 7)
UNKNOWN = -1  # a count we do not have, which is not the same as a count of zero

HELP = {
    "plan": "print the campaign tree; no token needed",
    "launch": "create the campaign, ad set, creatives and ads, all paused",
    "report": "spend and clicks per ad, joined to our own signup counts",
    "prune": "pause the ads past the kill line; deletes nothing",
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


def launch_requests(account: str, rows, budget: float):
    """The full write list, in the order Meta needs it: campaign, ad set, then per ad.

    Image hashes and creative ids do not exist yet, so the creative and ad entries carry
    placeholders. `cmd_launch --live` fills them in as each call returns.
    """
    adset_id = f"<ADSET_ID:{api.ADSET_NAME}>"
    requests = [api.campaign_request(account, budget),
                api.adset_request(account, f"<CAMPAIGN_ID:{api.CAMPAIGN_NAME}>")]
    for row in rows:
        requests.append(api.image_request(row, account))
        requests.append(api.creative_request(row, account, f"<hash:{row['png'].name}>"))
        requests.append(api.ad_request(row, account, adset_id,
                                       f"<CREATIVE_ID:{row['name']}>"))
    return requests


# -------------------------------------------------------------------------------- table
def cells_for(row, counts) -> list:
    """One row of the report: Meta's numbers, then ours when we have them."""
    name = row.get("ad_name") or row.get("ad_id")
    spend, clicks = fetched(row, "spend"), fetched(row, "inline_link_clicks")
    cells = [str(name)[:WIDTH[0]], f"{spend:.2f}", f"{clicks:.0f}",
             money(cost_per(spend, clicks))]
    for key in JOINED:
        count = None
        if counts:
            count = (counts.get(name) or {}).get(key)
            count = int(count) if count is not None else None
        cells.append(f"{UNKNOWN if count is None else count}")
        cells.append(money(cost_per(spend, count) if count is not None else None))
    return cells


def print_table(rows, counts) -> None:
    print(" ".join(f"{head:>{width}}" for head, width in zip(HEAD, WIDTH)))
    for row in sorted(rows, key=lambda r: fetched(r, "spend"), reverse=True):
        cells = cells_for(row, counts)
        print(" ".join(f"{cell:>{width}}" for cell, width in zip(cells, WIDTH)))


def digest(rows, counts, total, max_cpa, min_spend) -> str:
    """The phone-sized version: what is working, what is over the line, and the spend.

    A ten-column table is unreadable on a phone, so Telegram gets the decision and
    stdout keeps the numbers.
    """
    scored = []
    for row in rows:
        cells = cells_for(row, counts)
        name, spend = cells[0], float(cells[1])
        signups, attended = int(cells[4]), int(cells[8])
        scored.append((name, spend, signups, attended))
    lines = [f"CI ads: ${total:.2f} across {len(scored)} ads"]
    winners = sorted([s for s in scored if s[3] > 0], key=lambda s: s[1] / s[3])[:3]
    for name, spend, _, attended in winners:
        lines.append(f"{name}: ${spend / attended:.2f} per attendee, {attended} attended")
    over = [s for s in scored if past_kill_line(s[1], s[2], s[3], max_cpa, min_spend)]
    for name, spend, signups, attended in over[:3]:
        lines.append(f"over the line: {name} ${spend:.2f}, {signups} signups, "
                     f"{attended} attended")
    if not winners and not over:
        lines.append("no attendees yet: nothing to compare")
    lines.append("full table: python3 tools/meta_ads.py report")
    return "\n".join(lines)


# ------------------------------------------------------------------------------- commands
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


def cmd_launch(args) -> int:
    bank = load_bank()
    rows, missing = targets(bank)
    if not rows:
        print("nothing to launch: no poster matched the message bank", file=sys.stderr)
        return 2
    if missing:
        print(f"skipping {len(missing)} ad(s) with no poster on disk", file=sys.stderr)

    account = api.account_id()
    requests = launch_requests(account, rows, args.budget)

    allowed, reason = api.write_allowed(args.live)
    if not allowed:
        print(f"dry run ({reason}): {len(requests)} write requests, nothing sent")
        print(api.secret_report() + "\n")
        for request in requests:
            print(api.render(request))
        print(f"\nwrite requests: {len(requests)}"
              f"  (1 campaign + 1 ad set + 3 per ad x {len(rows)} ads)")
        print(f"reads first: {api.render(api.list_adsets_request(account))}")
        return 0

    token = api.secret(api.TOKEN_SECRET)
    print(f"live: {len(requests)} writes to act_{account}, everything PAUSED\n")
    campaign_id = api.graph(api.campaign_request(account, args.budget), token)["id"]
    print(f"  campaign {campaign_id}")
    adset_id = api.graph(api.adset_request(account, campaign_id), token)["id"]
    print(f"  ad set   {adset_id}")
    for row in rows:
        images = api.graph(api.image_request(row, account), token)["images"]
        image_hash = next(iter(images.values()))["hash"]
        creative_id = api.graph(api.creative_request(row, account, image_hash),
                                token)["id"]
        ad_id = api.graph(api.ad_request(row, account, adset_id, creative_id),
                          token)["id"]
        print(f"  ad       {ad_id}  {row['name']}")
    print("\nall paused. Check the previews in Ads Manager, then set the campaign active.")
    return 0


def cmd_report(args) -> int:
    account = api.account_id()
    allowed, reason = api.write_allowed(args.live)
    if not allowed:
        print(f"dry run ({reason}): report only reads")
        print(api.secret_report())
        print(api.render(api.list_adsets_request(account)))
        print(api.render(api.insight_request(args.adset_id or
                                             f"<ADSET_ID:{api.ADSET_NAME}>")))
        print(api.render({"method": "GET", "path": api.ATTRIBUTION_PATH,
                          "params": {"utm_content": "<ad names, comma separated>"},
                          "note": f"our counts, {api.ATTRIBUTION_ENDPOINT}"}))
        return 0

    token = api.secret(api.TOKEN_SECRET)
    adset_id = api.resolve_adset(account, token, args.adset_id)
    rows = api.graph(api.insight_request(adset_id), token).get("data") or []
    if not rows:
        print(f"no insights yet for {adset_id}: the ads have not spent anything")
        return 0
    names = [row.get("ad_name") or row.get("ad_id") for row in rows]
    counts, why = api.attribution(names)
    if why:
        print(f"attribution unavailable ({why}); Meta numbers only, {UNKNOWN} below\n")
    print_table(rows, counts)
    total = sum(fetched(row, "spend") for row in rows)
    print(f"\nspend ${total:.2f} across {len(rows)} ads. Cost per attendee decides; "
          f"see docs/ads/meta-runbook.md")
    if args.notify:
        deliver(digest(rows, counts, total, args.max_cpa, args.min_spend))
    return 0


def cmd_prune(args) -> int:
    account = api.account_id()
    allowed, reason = api.write_allowed(args.live)
    if not allowed:
        print(f"dry run ({reason}): prune sends nothing")
        print(api.render(api.list_adsets_request(account)))
        print(api.render(api.insight_request(args.adset_id or
                                             f"<ADSET_ID:{api.ADSET_NAME}>")))
        print(api.render(api.pause_request("<AD_ID>")))
        print(f"pauses one ad per row with no signups, or over ${args.max_cpa:.0f} per "
              f"attendee, after ${args.min_spend:.0f} spent. Deletes nothing.")
        return 0

    token = api.secret(api.TOKEN_SECRET)
    adset_id = api.resolve_adset(account, token, args.adset_id)
    rows = api.graph(api.insight_request(adset_id), token).get("data") or []
    names = [row.get("ad_name") or row.get("ad_id") for row in rows]
    counts, why = api.attribution(names)
    if why:
        # Pausing on clicks alone would stop the ads that are working: a click is not a
        # signup, and the question the test asks is which message brings people in.
        print(f"pausing nothing: attribution unavailable ({why})", file=sys.stderr)
        return 0
    paused = 0
    for row in rows:
        name = row.get("ad_name") or row.get("ad_id")
        own = counts.get(name) or {}
        spend = fetched(row, "spend")
        signups = int(own.get("signups") or 0)
        attended = int(own.get("attended") or 0)
        if past_kill_line(spend, signups, attended, args.max_cpa, args.min_spend):
            api.graph(api.pause_request(row["ad_id"]), token)
            print(f"paused  {name}  ${spend:.2f}, {signups} signups, {attended} attended")
            paused += 1
    print(f"{paused} paused of {len(rows)}: no signups, or over ${args.max_cpa:.0f} per "
          f"attendee after ${args.min_spend:.0f} spent")
    return 0


def deliver(text: str) -> None:
    """Hand the digest to the gateway. Never a Graph endpoint, never from the site."""
    env = {k: v for k, v in os.environ.items() if "proxy" not in k.lower()}
    try:
        subprocess.run(["hermes", "send", "-t", "telegram", text], check=True, env=env,
                       timeout=120)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"could not send to Telegram: {type(exc).__name__}", file=sys.stderr)


# ------------------------------------------------------------------------------ arithmetic
def fetched(row, key) -> float:
    """A number out of a Graph row, where every number arrives as a string."""
    try:
        return float(row.get(key) or 0)
    except (TypeError, ValueError):
        return 0.0


def money(value, width=7) -> str:
    """Right-aligned money, or a dash. None is 'nothing happened', not zero dollars."""
    return f"{'-':>{width}}" if value is None else f"{value:>{width}.2f}"


def cost_per(spend: float, count):
    """Cost per thing, or None when nothing happened yet. None is not zero."""
    if not count:
        return None
    return spend / count


def past_kill_line(spend: float, signups: int, attended: int,
                   max_cpa: float, min_spend: float) -> bool:
    """Kill an ad that spent the minimum with no signups, or above the ceiling.

    Below `min_spend` nothing is judged: an ad that has spent $3 has not failed. An ad
    with signups but no attendees yet is not judged either, because people register
    before the class happens and the cost per attendee is not knowable until it has.
    """
    if spend < min_spend:
        return False
    if signups <= 0:
        return True
    per_attendee = cost_per(spend, attended)
    return per_attendee is not None and per_attendee > max_cpa


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="meta_ads.py", description="Meta ads operator for the CI Fundamentals series")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help=HELP["plan"])
    plan.add_argument("--budget", type=float, default=40,
                      help="campaign daily budget in dollars (default 40)")

    launch = sub.add_parser("launch", help=HELP["launch"])
    launch.add_argument("--budget", type=float, default=40)
    launch.add_argument("--live", action="store_true",
                        help="send the requests; without it, print them")

    report = sub.add_parser("report", help=HELP["report"])
    report.add_argument("--adset-id", help="skip discovery and use this ad set id")
    report.add_argument("--max-cpa", type=float, default=40.0)
    report.add_argument("--min-spend", type=float, default=60.0)
    report.add_argument("--live", action="store_true")
    report.add_argument("--no-notify", dest="notify", action="store_false",
                        help="keep it on stdout, do not send the digest to Max")

    prune = sub.add_parser("prune", help=HELP["prune"])
    prune.add_argument("--max-cpa", type=float, default=40.0)
    prune.add_argument("--min-spend", type=float, default=60.0)
    prune.add_argument("--adset-id")
    prune.add_argument("--live", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    handlers = {
        "plan": cmd_plan,
        "launch": cmd_launch,
        "report": cmd_report,
        "prune": cmd_prune,
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
