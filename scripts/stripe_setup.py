#!/usr/bin/env python3
"""Create the Stripe objects the checkout endpoints depend on.

Creates, idempotently (keyed on `lookup_key`, never on name or id), the
product and price for each entry in `PRICES`:

    ci-ticket-online-friday    $20.00  one-time   drop-in class ticket
    ci-intro-pack              $45.00  one-time   3-class intro pack (first-timers)
    ci-membership-monthly      $60.00  /month     unlimited membership
    ci-membership-annual      $540.00  one-time   12-month prepaid membership

Run in TEST mode by default against the `mindfold` Stripe CLI profile (account
acct_1L2xjuGR8ZpP3Rho, "Blindfolded Experience"). The Worker's checkout
endpoint reads each price by its `lookup_key`, never by a hardcoded price id,
so this script can be re-run to backfill either mode without Worker config
changing, and can be extended with more rows (e.g. a jam drop-in price) later.

Test mode (safe, default):
    python3 scripts/stripe_setup.py

Live mode (deliberately not run by an agent -- the CLI's live key on this
account is read-only for products per GBrain `miami-ci-community`, so a live
run needs Max's full secret key loaded in the `stripe` CLI's keychain profile,
and needs him to type the confirmation phrase below):

    python3 scripts/stripe_setup.py --live --confirm "I am creating a LIVE Stripe object"

Requires the `stripe` CLI on PATH, authenticated as the `mindfold` project
(`stripe config --list --project-name mindfold`). Never prints a secret key;
everything here reads/writes product and price IDs, which are not secrets.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

PROJECT = "mindfold"
CURRENCY = "usd"

# Each row is one Stripe product + price, matched for idempotency on
# `lookup_key` alone. `recurring_interval` is None for a one-time price.
PRICES = [
    {
        "lookup_key": "ci-ticket-online-friday",
        "product_name": "Contact Improv Miami - Friday class (online)",
        "description": (
            "One ticket, one Friday 7-9pm Contact Improv class, Inner Motion Dance "
            "Studio, Hallandale Beach FL. Online sales close 2 hours before class "
            "start; after that, pay at the door."
        ),
        "unit_amount": 2000,
        "recurring_interval": None,
    },
    {
        "lookup_key": "ci-jam-dropin",
        "product_name": "Contact Improv Miami - Jam drop-in (online)",
        "description": (
            "One ticket, one open jam night, Inner Motion Dance Studio, Hallandale "
            "Beach FL. Online sales close 2 hours before the jam starts; after that, "
            "pay at the door."
        ),
        "unit_amount": 1500,
        "recurring_interval": None,
    },
    {
        "lookup_key": "ci-combo-dropin",
        "product_name": "Contact Improv Miami - Class + jam same day (online)",
        "description": (
            "One ticket covering both the class and the jam on a day that runs "
            "both, Inner Motion Dance Studio, Hallandale Beach FL. Online sales "
            "close 2 hours before the class starts; after that, pay at the door."
        ),
        "unit_amount": 3000,
        "recurring_interval": None,
    },
    {
        "lookup_key": "ci-intro-pack",
        "product_name": "Contact Improv Miami - Intro 3-class pack",
        "description": (
            "Three classes or jams for first-timers. Credits are tracked by the "
            "Worker (KV), not by Stripe; this price exists once per person's first "
            "pack. Promotion codes apply."
        ),
        "unit_amount": 4500,
        "recurring_interval": None,
    },
    {
        "lookup_key": "ci-membership-monthly",
        "product_name": "Contact Improv Miami - Monthly unlimited membership",
        "description": (
            "Unlimited classes and jams, billed monthly. Promotion codes do not "
            "apply to memberships."
        ),
        "unit_amount": 6000,
        "recurring_interval": "month",
    },
    {
        "lookup_key": "ci-membership-annual",
        "product_name": "Contact Improv Miami - Annual membership",
        "description": (
            "Twelve months unlimited, prepaid once (about $45/mo). Promotion codes "
            "do not apply to memberships."
        ),
        "unit_amount": 54000,
        "recurring_interval": None,
    },
]

# The `stripe` CLI inherits whatever HTTP(S)_PROXY is in the shell, and a
# stale local proxy makes every call fail with a TLS error that has nothing to
# do with Stripe. Clearing it here is the same workaround AGENTS.md documents
# for `gh`.
_NO_PROXY_ENV = {
    **os.environ,
    "HTTPS_PROXY": "",
    "HTTP_PROXY": "",
    "https_proxy": "",
    "http_proxy": "",
    "ALL_PROXY": "",
}

LIVE_CONFIRM_PHRASE = "I am creating a LIVE Stripe object"


def run_stripe(args: list[str]) -> dict:
    """Run a `stripe` CLI command and return its parsed JSON stdout.

    Never pass `--live` through here directly; callers add it to `args` only
    after `main()` has checked the confirmation phrase.
    """
    cmd = ["stripe", *args, "--project-name", PROJECT, "--confirm"]
    result = subprocess.run(cmd, capture_output=True, text=True, env=_NO_PROXY_ENV)
    if result.returncode != 0:
        sys.stderr.write(f"stripe {' '.join(args)} failed:\n{result.stderr}\n")
        raise SystemExit(1)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        sys.stderr.write(f"stripe {' '.join(args)} did not return JSON:\n{result.stdout}\n")
        raise SystemExit(1)


def find_existing_price(lookup_key: str, live: bool) -> dict | None:
    args = ["prices", "list", "--lookup-keys", lookup_key, "--limit", "1"]
    if live:
        args.append("--live")
    payload = run_stripe(args)
    data = payload.get("data") or []
    return data[0] if data else None


def create_product(name: str, description: str, live: bool) -> str:
    args = ["products", "create", "--name", name, "--description", description]
    if live:
        args.append("--live")
    product = run_stripe(args)
    return product["id"]


def create_price(product_id: str, row: dict, live: bool) -> dict:
    args = [
        "prices", "create",
        "--product", product_id,
        "--unit-amount", str(row["unit_amount"]),
        "--currency", CURRENCY,
        "--lookup-key", row["lookup_key"],
    ]
    if row["recurring_interval"]:
        args += ["--recurring.interval", row["recurring_interval"]]
    if live:
        args.append("--live")
    return run_stripe(args)


def ensure_price(row: dict, live: bool) -> dict:
    existing = find_existing_price(row["lookup_key"], live)
    if existing:
        print(f"[stripe_setup] {row['lookup_key']}: already exists, price {existing['id']} (product {existing['product']})")
        return {"price_id": existing["id"], "product_id": existing["product"], "lookup_key": row["lookup_key"]}

    product_id = create_product(row["product_name"], row["description"], live)
    price = create_price(product_id, row, live)
    print(f"[stripe_setup] {row['lookup_key']}: created product {product_id}, price {price['id']}")
    return {"price_id": price["id"], "product_id": product_id, "lookup_key": row["lookup_key"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--live", action="store_true", help="Create in LIVE mode instead of test mode.")
    parser.add_argument("--confirm", default="", help=f'Required with --live: must equal "{LIVE_CONFIRM_PHRASE}".')
    parser.add_argument("--only", default="", help="Comma-separated lookup_keys to limit this run to (default: all rows in PRICES).")
    args = parser.parse_args()

    if args.live and args.confirm != LIVE_CONFIRM_PHRASE:
        sys.stderr.write(
            "Refusing to create a LIVE Stripe object without the exact confirmation phrase.\n"
            f'Pass --confirm "{LIVE_CONFIRM_PHRASE}" if this is deliberate, and prefer running\n'
            "this by hand rather than from an agent.\n"
        )
        return 1

    mode = "LIVE" if args.live else "test"
    only = {key.strip() for key in args.only.split(",") if key.strip()}
    rows = [row for row in PRICES if not only or row["lookup_key"] in only]
    if not rows:
        sys.stderr.write(f"--only matched no rows in PRICES (gave: {args.only!r})\n")
        return 1

    print(f"[stripe_setup] mode={mode} rows={[r['lookup_key'] for r in rows]}")
    results = [ensure_price(row, args.live) for row in rows]
    print(json.dumps({"mode": mode, "prices": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
