#!/usr/bin/env python3
"""Tests for /tickets and the /fr/<name> referral link (pricing + ambassador slice 1).

    python3 -m unittest discover -s tests

Offline: renders the page builder and the redirects file in-process. The Worker
side (prices, metadata, first-class eligibility) is tested in the Worker repo.
"""

import importlib
import os
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import build  # noqa: E402
import content_tickets  # noqa: E402
import shell  # noqa: E402


class TicketsPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = content_tickets.tickets()

    def test_three_prices_and_the_first_class_offer(self):
        for price in ("$20", "$15", "$30"):
            self.assertIn(f'<p class="tk-price">{price}</p>', self.html)
        self.assertIn('data-ticket="early"', self.html)
        self.assertIn('data-ticket="community"', self.html)
        self.assertIn('data-ticket="first"', self.html)
        self.assertIn('data-ticket="referral"', self.html)
        self.assertIn("Your first class is $15.", self.html)

    def test_door_is_information_only(self):
        door = self.html.split('tk-card-quiet', 1)[1].split("</article>", 1)[0]
        self.assertNotIn("<button", door)

    def test_share_channels_match_the_worker(self):
        # Must equal SHARE_CHANNELS in the Worker's src/tickets.ts.
        values = re.findall(r'<option value="([a-z_]+)">', self.html)
        self.assertEqual(values, ["instagram_story", "whatsapp_group", "facebook_group", "other"])

    def test_every_fundamentals_friday_is_offered_with_a_dst_correct_start(self):
        starts = re.findall(r'data-start="([^"]+)"', self.html)
        self.assertEqual(len(starts), 8)
        self.assertTrue(starts[0].startswith("2026-10-02T19:00:00-04:00"))
        self.assertTrue(starts[-1].startswith("2026-11-20T19:00:00-05:00"))

    def test_endpoints_point_at_the_worker(self):
        self.assertIn(f'data-checkout="{shell.CHECKOUT_ENDPOINT}"', self.html)
        self.assertIn(f'data-first="{shell.FIRST_CLASS_ENDPOINT}"', self.html)
        self.assertTrue(shell.FIRST_CLASS_ENDPOINT.endswith("/api/first-class"))

    def test_inputs_have_labels(self):
        for input_id in ("tk-date", "tk-channel", "tk-handle", "tk-email"):
            self.assertIn(f'for="{input_id}"', self.html)

    def test_no_status_badges(self):
        self.assertNotRegex(self.html, r'class="[^"]*badge')

    def test_first_class_refusal_is_one_uniform_message(self):
        # The Worker answers every first-class refusal with first_offer_unavailable;
        # the page must not branch on a reason it is never told.
        script = content_tickets.TICKETS_SCRIPT
        self.assertIn("first_offer_unavailable", script)
        self.assertNotIn("first_discount_claimed", script)
        self.assertNotIn("eligible", script)

    def test_client_referrer_rule_matches_the_worker(self):
        self.assertIn("/^[a-z0-9][a-z0-9-]{0,39}$/", content_tickets.TICKETS_SCRIPT)


class ReferralRedirect(unittest.TestCase):
    def test_fr_name_redirects_to_tickets_with_ref(self):
        rules = build.redirects_file()
        self.assertRegex(rules, r"(?m)^/fr/:name\s+/tickets\?ref=:name\s+302$")

    def test_tickets_is_a_real_page_in_the_sitemap_table(self):
        routes = [row["route"] for row in build.rows()]
        self.assertIn("/tickets", routes)


class ApiBaseOverride(unittest.TestCase):
    def test_local_api_base_swaps_every_endpoint(self):
        os.environ["MCI_API_BASE"] = "http://localhost:8787/"
        try:
            reloaded = importlib.reload(shell)
            self.assertEqual(reloaded.CHECKOUT_ENDPOINT, "http://localhost:8787/api/checkout")
            self.assertEqual(reloaded.FIRST_CLASS_ENDPOINT, "http://localhost:8787/api/first-class")
        finally:
            del os.environ["MCI_API_BASE"]
            importlib.reload(shell)


if __name__ == "__main__":
    unittest.main()
