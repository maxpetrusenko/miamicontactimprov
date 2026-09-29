#!/usr/bin/env python3
"""The Graph surface for the CI Fundamentals ads: every Meta call, and nothing else.

Request builders, the sender, the Doppler reads and the attribution join live here so
that `tools/meta_ads.py` can stay about the campaign. The URLs each shape was read from
are cited in the docstring of `tools/meta_ads.py`; the version is pinned there too.

Two rules hold in this file:

* a budget is always in the currency subunit (Meta's own unit), never dollars;
* every object this tool creates is created PAUSED.
"""

import json
import os
import pathlib
import subprocess

GRAPH = "https://graph.facebook.com"
API_VERSION = "v26.0"  # current version per the changelog; a bump should be a commit

CAMPAIGN_NAME = "ci_fundamentals"
ADSET_NAME = "ci_fundamentals_broad_25mi"
MINOR_UNITS = 100  # daily_budget is in subunits, so dollars x 100
GEO = {"latitude": 25.9862, "longitude": -80.1406, "radius": 25, "distance_unit": "mile"}
AGE_MIN, AGE_MAX = 21, 60
ATTRIBUTION_ENDPOINT = "https://newsletter-api.max-petrusenko.workers.dev"
ATTRIBUTION_PATH = "/api/admin/attribution"

ACCOUNT_SECRET = "META_AD_ACCOUNT_ID"
TOKEN_SECRET = "META_ADS_TOKEN"
PAGE_SECRET = "META_PAGE_ID"
APP_SECRET = "BRIGHTBEAN_STUDIO_PLATFORM_FACEBOOK_APP_ID"
ADMIN_SECRET = "NEWSLETTER_ADMIN_TOKEN"

# Reported as present or missing, never printed: this is the wiring Max's setup steps
# land in, and a dry run that says every secret is present is the fastest way to find
# out that one of them is not.
ALL_SECRETS = (ACCOUNT_SECRET, TOKEN_SECRET, PAGE_SECRET, APP_SECRET, ADMIN_SECRET)

_SECRETS: dict = {}


# -------------------------------------------------------------------- secrets and gate
def secret(name: str):
    """One secret from Doppler `api_keys/dev`, or None when it is not there.

    Proxy variables are stripped from the child environment: a proxy the Doppler CLI
    inherits makes the read hang instead of failing, and the Graph calls want the same
    treatment. The value goes back to the caller and is never logged.
    """
    if name in _SECRETS:
        return _SECRETS[name]
    env = {k: v for k, v in os.environ.items() if "proxy" not in k.lower()}
    done = None
    try:
        done = subprocess.run(
            ["doppler", "secrets", "get", name, "--plain", "-p", "api_keys", "-c", "dev"],
            capture_output=True, text=True, env=env, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        pass
    _SECRETS[name] = (done.stdout.strip() if done and done.returncode == 0 else "") or None
    return _SECRETS[name]


def write_allowed(live: bool):
    """(allowed, why not). A write needs a real token and an explicit `--live`."""
    if not live:
        return False, "--live not passed"
    missing = [n for n in (ACCOUNT_SECRET, TOKEN_SECRET) if not secret(n)]
    if missing:
        return False, "missing Doppler secret(s): " + ", ".join(missing)
    return True, ""


def act_id(account: str) -> str:
    """`act_<id>` once. The secret may carry the prefix already, per Meta's own docs."""
    account = str(account)
    return account if account.startswith("act_") else f"act_{account}"


def account_id() -> str:
    return secret(ACCOUNT_SECRET) or "<AD_ACCOUNT_ID>"


def secret_report() -> str:
    """One line of presence, no values: what Doppler has and what it is still missing."""
    return "secrets: " + ", ".join(
        f"{name}={'present' if secret(name) else 'missing'}" for name in ALL_SECRETS)


def minor_units(dollars) -> int:
    """Daily budget in the currency subunit. Meta rejects a budget of zero."""
    units = int(round(float(dollars) * MINOR_UNITS))
    if units <= 0:
        raise SystemExit(f"budget must be positive, got {dollars}")
    return units


# --------------------------------------------------------------------- request builders
def image_request(row: dict, account: str) -> dict:
    return {"method": "POST", "path": f"/{API_VERSION}/{act_id(account)}/adimages",
            "files": {"bytes": row["png"]}, "note": f"poster for {row['name']}"}


def creative_request(row: dict, account: str, image_hash: str) -> dict:
    story = {
        "page_id": secret(PAGE_SECRET) or "<PAGE_ID>",
        "link_data": {
            "link": row["link"],
            "message": row["body"],
            "name": row["headline"],
            "description": row["subline"],
            "image_hash": image_hash,
            "call_to_action": {"type": "SIGN_UP", "value": {"link": row["link"]}},
        },
    }
    return {"method": "POST", "path": f"/{API_VERSION}/{act_id(account)}/adcreatives",
            "params": {"name": row["creative_name"],
                       "object_story_spec": json.dumps(story)},
            "note": f"creative for {row['name']}"}


def campaign_request(account: str, budget: float) -> dict:
    return {
        "method": "POST", "path": f"/{API_VERSION}/{act_id(account)}/campaigns",
        "params": {
            "name": CAMPAIGN_NAME,
            "objective": "OUTCOME_TRAFFIC",  # the test measures cheap arrivals at /start
            "status": "PAUSED",
            "special_ad_categories": "[]",  # required on every campaign; NONE is this one
            "buying_type": "AUCTION",
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "daily_budget": str(minor_units(budget)),
        },
        "note": "one CBO, so the budget lives here and not on the ad set",
    }


def adset_request(account: str, campaign_id: str) -> dict:
    return {
        "method": "POST", "path": f"/{API_VERSION}/{act_id(account)}/adsets",
        "params": {
            "name": ADSET_NAME,
            "campaign_id": campaign_id,
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "LINK_CLICKS",
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "status": "PAUSED",
            "targeting": json.dumps({
                "geo_locations": {"custom_locations": [GEO]},
                "age_min": AGE_MIN,
                "age_max": AGE_MAX,
                "publisher_platforms": ["facebook", "instagram"],
            }),
        },
        "note": "one broad ad set: the creative is the targeting",
    }


def ad_request(row: dict, account: str, adset_id: str, creative_id: str) -> dict:
    return {"method": "POST", "path": f"/{API_VERSION}/{act_id(account)}/ads",
            "params": {"name": row["name"], "adset_id": adset_id,
                       "creative": json.dumps({"creative_id": creative_id}),
                       "status": "PAUSED"},
            "note": row["name"]}


def insight_request(adset_id: str, preset: str = "maximum") -> dict:
    fields = ",".join(["ad_id", "ad_name", "spend", "impressions",
                       "inline_link_clicks", "cost_per_inline_link_click"])
    return {"method": "GET", "path": f"/{API_VERSION}/{adset_id}/insights",
            "params": {"level": "ad", "fields": fields, "date_preset": preset,
                       "limit": "200"},
            "note": "one row per ad"}


def list_adsets_request(account: str) -> dict:
    return {"method": "GET", "path": f"/{API_VERSION}/{act_id(account)}/adsets",
            "params": {"fields": "id,name,campaign_id", "limit": "200"},
            "note": f"find {ADSET_NAME} by name"}


def pause_request(ad_id: str) -> dict:
    return {"method": "POST", "path": f"/{API_VERSION}/{ad_id}",
            "params": {"status": "PAUSED"}, "note": "pause, never delete"}


def render(request: dict) -> str:
    """One line per request: the verb, the path, then the body it would carry.

    This is what a dry run prints, so it has to be the whole request. String values are
    cut at 300 characters and marked, which is enough for every field here except a
    long-form `object_story_spec`, whose tail is the second half of an ad body.
    """
    parts = [f"{request['method']} {request['path']}"]
    for key, value in (request.get("params") or {}).items():
        text = str(value)
        parts.append(f"{key}={text if len(text) <= 300 else text[:297] + '...'}")
    for key, path in (request.get("files") or {}).items():
        size = path.stat().st_size if path.is_file() else 0
        parts.append(f"files[{key}]={path.name} ({size} bytes)")
    return "  ".join(parts)


# ------------------------------------------------------------------------------ sender
def graph(request: dict, token: str) -> dict:
    """Send one request and return the decoded body. Raises on a Graph error.

    `requests` is imported here so that `plan`, `report --help` and every dry run still
    work on a bare interpreter: nothing in this repo's tooling needs installing to print
    what it would send.
    """
    import requests

    url = GRAPH + request["path"]
    headers = {"Authorization": f"Bearer {token}"}
    if request["method"] == "GET":
        response = requests.get(url, params=request.get("params"), headers=headers,
                                timeout=60)
    else:
        files = None
        body = dict(request.get("params") or {})
        if request.get("files"):
            # Read the poster into memory rather than streaming it: 100 kB, and a file
            # handle that requests does not own is a handle nobody closes.
            files = {key: (path.name, path.read_bytes(), "image/png")
                     for key, path in request["files"].items()}
        response = requests.post(url, data=body or None, files=files, headers=headers,
                                 timeout=120)
    try:
        payload = response.json()
    except ValueError:
        payload = {"error": {"message": f"non-JSON response, HTTP {response.status_code}"}}
    if isinstance(payload, dict) and payload.get("error"):
        raise SystemExit(f"graph error on {request['method']} {request['path']}: "
                         f"{payload['error'].get('message')}")
    return payload


def resolve_adset(account: str, token: str, explicit: str) -> str:
    """The ad set id, given or looked up by name. One tree, never two."""
    if explicit:
        return explicit
    for row in (graph(list_adsets_request(account), token).get("data") or []):
        if row.get("name") == ADSET_NAME:
            return row["id"]
    raise SystemExit(f"no ad set named {ADSET_NAME} in act_{account}: run launch first")


def attribution(names) -> tuple:
    """Our own counts by `utm_content`, from the Worker admin endpoint.

    Returns (counts, reason). A missing token or a non-200 is "unavailable", never zero:
    a column of zeros reads as a campaign that failed, and prune would act on it.
    """
    if not names:
        return {}, "no ads to join"
    token = secret(ADMIN_SECRET)
    if not token:
        return {}, f"Doppler {ADMIN_SECRET} not set"
    import requests

    url = ATTRIBUTION_ENDPOINT + ATTRIBUTION_PATH
    try:
        response = requests.get(url, params={"utm_content": ",".join(sorted(names))},
                                headers={"Authorization": f"Bearer {token}"}, timeout=60)
    except Exception as exc:  # noqa: BLE001 - every transport failure is the same answer
        return {}, f"{type(exc).__name__} calling {url}"
    if response.status_code != 200:
        return {}, f"HTTP {response.status_code} from {url}"
    return ((response.json() or {}).get("counts") or {}), ""


def poster_exists(path: pathlib.Path) -> bool:
    return path.is_file()
