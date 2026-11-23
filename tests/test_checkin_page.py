#!/usr/bin/env python3
"""The studio check-in page and the support address on the member pages.

    python3 -m unittest tests.test_checkin_page
"""

import json
import pathlib
import re
import shutil
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import bf_bar  # noqa: E402
import build  # noqa: E402
import content_checkin  # noqa: E402
import content_membership  # noqa: E402
import guide_bar  # noqa: E402
import locales  # noqa: E402
import seo_variants  # noqa: E402

SUPPORT = "hello@miamicontactimprov.com"
ID = "a" * 32
TID = "b" * 32


def html(fn):
    out = fn()
    return out if isinstance(out, str) else str(out)


def main_of(page):
    return page[page.index("<main"):page.index("</main>")]


class Routing(unittest.TestCase):
    def test_route_private_and_rewritten(self):
        self.assertEqual(locales.route("checkin", "en"), "/checkin")
        self.assertIn("/checkin", seo_variants.PRIVATE_ROUTES)
        self.assertEqual(build.CHECKIN_REWRITE, "/checkin/*  /checkin  200")

    def test_no_strips_on_the_checkin_page(self):
        self.assertFalse(bf_bar.shows("/checkin", "en"))
        self.assertFalse(bf_bar.shows("/checkin/" + TID, "en"))
        self.assertFalse(guide_bar.shows("/checkin", "en"))


class Page(unittest.TestCase):
    def setUp(self):
        self.page = html(content_checkin.checkin)
        self.main = main_of(self.page)

    def test_one_h1_and_every_panel_starts_hidden(self):
        self.assertEqual(self.main.count("<h1"), 1)
        for panel in ("ok", "already", "denied", "email", "sent", "ticket-ok", "ticket-used", "ticket-denied"):
            self.assertRegex(self.main, rf'id="ck-{panel}" hidden')

    def test_denied_screens_carry_the_support_address(self):
        for panel in ("denied", "sent", "ticket-used", "ticket-denied"):
            block = self.main[self.main.index(f'id="ck-{panel}"'):]
            block = block[: block.index("</div>")]
            self.assertIn(f'mailto:{SUPPORT}', block, panel)

    def test_secrets_leave_the_address_bar_before_analytics(self):
        head = self.page[: self.page.index("</head>")]
        self.assertIn("window.__mciCk = state;", head)
        self.assertIn("history.replaceState(window.history.state, '', '/checkin')", head)
        self.assertIn("{extra_head}{posthog_snippet()}", (ROOT / "build" / "shell.py").read_text())
        self.assertNotIn("location.search", self.main)

    def test_email_form_posts_to_the_link_route_only(self):
        self.assertIn(content_checkin.API, self.page)
        self.assertEqual(content_checkin.API, "https://newsletter-api.max-petrusenko.workers.dev/api/checkin")
        self.assertIn("post('/link', { email: email })", self.page)
        self.assertIn('for="ck-email-input"', self.main)
        self.assertEqual(self.main.count('id="ck-email-input"'), 1)

    def test_no_badges_or_helper_captions(self):
        self.assertNotIn("badge", self.main.lower())
        self.assertNotIn("price-note", self.main)


NODE_HARNESS = r"""
var out = [];
function el(id) { return { id: id, hidden: false, textContent: '', value: '', disabled: false, addEventListener: function () {} }; }
var els = {};
function getEl(id) { if (!els[id]) els[id] = el(id); return els[id]; }
var store = %(store)s;
var calls = [];
var responses = %(responses)s;
var window = { __mciCk: %(state)s, location: { search: '' }, history: { state: null, replaceState: function () {} } };
var document = { getElementById: getEl };
var localStorage = { getItem: function (k) { return k in store ? store[k] : null; }, setItem: function (k, v) { store[k] = v; }, removeItem: function (k) { delete store[k]; } };
var fetch = function (url, init) {
  calls.push({ url: url, body: init && init.body ? JSON.parse(init.body) : null });
  var r = responses.shift();
  return Promise.resolve({ status: r.status, json: function () { return Promise.resolve(r.body); } });
};
%(script)s
setTimeout(function () {
  var visible = Object.keys(els).filter(function (k) { return k.indexOf('ck-') === 0 && els[k].hidden === false && ['ck-loading','ck-ok','ck-already','ck-denied','ck-email','ck-sent','ck-ticket-ok','ck-ticket-used','ck-ticket-denied'].indexOf(k) >= 0; });
  console.log(JSON.stringify({ visible: visible, calls: calls, store: store, text: { ok: els['ck-ok-line'] && els['ck-ok-line'].textContent, already: els['ck-already-line'] && els['ck-already-line'].textContent, denied: els['ck-denied-msg'] && els['ck-denied-msg'].textContent, ticketOk: els['ck-ticket-ok-line'] && els['ck-ticket-ok-line'].textContent, ticketUsed: els['ck-ticket-used-line'] && els['ck-ticket-used-line'].textContent, ticketDenied: els['ck-ticket-denied-msg'] && els['ck-ticket-denied-msg'].textContent } }));
}, 20);
"""


def run_page(state, store, responses):
    script = re.search(r"<script>(.*)</script>", content_checkin.SCRIPT, re.S).group(1)
    code = NODE_HARNESS % {
        "store": json.dumps(store),
        "responses": json.dumps(responses),
        "state": json.dumps(state),
        "script": script,
    }
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class Flows(unittest.TestCase):
    def test_member_with_a_stored_token_checks_in(self):
        r = run_page({"m": "", "t": ""}, {"mci_member": ID}, [{"status": 200, "body": {"ok": True, "already": False, "name": "Ana", "plan": "monthly", "credits_remaining": 3}}])
        self.assertEqual(r["visible"], ["ck-ok"])
        self.assertEqual(r["calls"], [{"url": content_checkin.API + "/member", "body": {"member_id": ID}}])
        self.assertIn("Ana", r["text"]["ok"])
        self.assertIn("3 class credits left", r["text"]["ok"])

    def test_second_scan_shows_already(self):
        r = run_page({"m": ID, "t": ""}, {}, [{"status": 200, "body": {"ok": True, "already": True, "name": "", "plan": "yearly", "credits_remaining": None}}])
        self.assertEqual(r["visible"], ["ck-already"])
        self.assertIn("Yearly membership", r["text"]["already"])

    def test_no_token_asks_for_the_email_and_calls_nothing(self):
        r = run_page({"m": "", "t": ""}, {}, [])
        self.assertEqual(r["visible"], ["ck-email"])
        self.assertEqual(r["calls"], [])

    def test_denials_say_why(self):
        for code, words in (("no_credits", "no class credits"), ("outside_window", "6:30 to 9:00 PM"), ("inactive", "not active"), ("week_used", "this week")):
            r = run_page({"m": "", "t": ""}, {"mci_member": ID}, [{"status": 409, "body": {"ok": False, "error": code}}])
            self.assertEqual(r["visible"], ["ck-denied"], code)
            self.assertIn(words, r["text"]["denied"], code)

    def test_a_token_the_server_does_not_know_is_dropped_and_the_email_form_shows(self):
        r = run_page({"m": "", "t": ""}, {"mci_member": ID}, [{"status": 404, "body": {"ok": False, "error": "unknown_member"}}])
        self.assertEqual(r["visible"], ["ck-email"])
        self.assertNotIn("mci_member", r["store"])

    def test_network_failure_is_a_denied_screen_not_a_blank_page(self):
        r = run_page({"m": "", "t": ""}, {"mci_member": ID}, [{"status": 500, "body": {}}])
        self.assertEqual(r["visible"], ["ck-denied"])
        self.assertIn("not available", r["text"]["denied"])

    def test_ticket_valid_then_used(self):
        r = run_page({"m": "", "t": TID}, {"mci_member": ID}, [{"status": 200, "body": {"ok": True, "already": False, "name": "Bo"}}])
        self.assertEqual(r["visible"], ["ck-ticket-ok"])
        self.assertEqual(r["calls"][0]["url"], content_checkin.API + "/ticket")
        self.assertEqual(r["calls"][0]["body"], {"ticket_id": TID})
        r = run_page({"m": "", "t": TID}, {}, [{"status": 200, "body": {"ok": True, "already": True, "checked_in_at": "2026-12-05T00:10:00.000Z"}}])
        self.assertEqual(r["visible"], ["ck-ticket-used"])
        self.assertIn("already used", r["text"]["ticketUsed"])

    def test_ticket_denials(self):
        r = run_page({"m": "", "t": TID}, {}, [{"status": 409, "body": {"ok": False, "error": "outside_window"}}])
        self.assertEqual(r["visible"], ["ck-ticket-denied"])
        r = run_page({"m": "", "t": TID}, {}, [{"status": 404, "body": {"ok": False, "error": "unknown_ticket"}}])
        self.assertIn("could not find", r["text"]["ticketDenied"])


class MemberPages(unittest.TestCase):
    def test_support_address_on_membership_and_success(self):
        for fn in (content_membership.membership, content_membership.membership_success):
            main = main_of(html(fn))
            self.assertIn(f"mailto:{SUPPORT}", main)

    def test_success_page_keeps_the_token_on_the_phone(self):
        page = html(content_membership.membership_success)
        self.assertIn("localStorage.setItem('mci_member', tok)", page)
        self.assertRegex(page, r'id="mci-checkin-ready"[^>]*\bhidden\b')


if __name__ == "__main__":
    unittest.main()
