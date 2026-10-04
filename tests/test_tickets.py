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

    def test_prices_match_max_2026_10_04(self):
        self.assertIn("Online, sliding scale: $20 to $40.", self.html)
        self.assertIn("Community: $15.", self.html)
        self.assertIn("First class: $15.", self.html)
        self.assertIn("At the door: $30 to $50, pay what you can.", self.html)
        for t in ("early", "referral"):
            self.assertIn(f'data-ticket="{t}"', self.html)

    def test_built_from_existing_components_only(self):
        for cls in ('class="hero"', 'class="answer"', 'class="facts"', 'class="price-list"',
                    'class="price-row"', 'class="band"', 'class="subscribe-block"', 'class="cite"'):
            self.assertIn(cls, self.html)
        self.assertNotRegex(self.html, r'class="[^"]*\btk-')
        css = (ROOT / "site" / "assets" / "site.css").read_text()
        self.assertNotIn(".tk-", css)
        self.assertNotIn(".idea-card", css)

    def test_door_row_has_no_button(self):
        door = self.html.split("At the door: $30 to $50", 1)[1].split("</div>\n  </div>", 1)[0]
        self.assertNotIn("<button", door)

    def test_community_verifies_a_post_link_or_screenshot(self):
        self.assertIn(f'data-verify="{shell.COMMUNITY_VERIFY_ENDPOINT}"', self.html)
        self.assertIn('name="share_url" type="url"', self.html)
        self.assertIn('name="screenshot" type="file"', self.html)
        script = content_tickets.TICKETS_SCRIPT
        for reason in ("no_match", "blocked", "used"):
            self.assertIn(reason, script)
        self.assertIn("verification_id: res.data.verification_id", script)

    def test_every_fundamentals_friday_is_offered_with_a_dst_correct_start(self):
        starts = re.findall(r'data-start="([^"]+)"', self.html)
        self.assertEqual(len(starts), 8)
        self.assertTrue(starts[0].startswith("2026-10-02T19:00:00-04:00"))
        self.assertTrue(starts[-1].startswith("2026-11-20T19:00:00-05:00"))

    def test_endpoints_point_at_the_worker(self):
        self.assertIn(f'data-checkout="{shell.CHECKOUT_ENDPOINT}"', self.html)
        self.assertIn(f'data-first="{shell.FIRST_CLASS_ENDPOINT}"', self.html)

    def test_inputs_have_labels(self):
        for input_id in ("tk-share-url", "tk-shot", "tk-email", "tk-consent"):
            self.assertIn(f'for="{input_id}"', self.html)

    def test_no_status_badges(self):
        self.assertNotRegex(self.html, r'class="[^"]*badge')

    def test_first_class_refusal_is_one_uniform_message(self):
        script = content_tickets.TICKETS_SCRIPT
        self.assertIn("first_offer_unavailable", script)
        self.assertNotIn("first_discount_claimed", script)

    def test_client_referrer_rule_matches_the_worker(self):
        self.assertIn("/^[a-z0-9][a-z0-9-]{0,39}$/", content_tickets.TICKETS_SCRIPT)


class PricesAgreeAcrossPages(unittest.TestCase):
    def test_pricing_and_pay_say_the_same_numbers(self):
        import content_checkout
        pricing = content_checkout.pricing()
        self.assertIn("$20 to $40, sliding scale", pricing)
        self.assertIn("$30&ndash;$50", pricing)
        self.assertIn('href="/tickets"', pricing)
        self.assertIn("$30 to $50, pay what you can", content_checkout.pay())
        self.assertIn("$30 to $50", shell.BUY_COPY["en"]["closed"])


class ReferralRedirect(unittest.TestCase):
    def test_fr_name_rewrites_to_tickets(self):
        # A 200 rewrite, not a 302 with ?ref=:name (Pages leaves query placeholders
        # unsubstituted, which was caught on the preview deploy).
        rules = build.redirects_file()
        self.assertRegex(rules, r"(?m)^/fr/\*\s+/tickets\s+200$")
        self.assertNotRegex(rules, r"(?m)^/fr/\S+\s+\S*\?ref=")
        self.assertIn("location.pathname.match(/^\\/fr\\/", content_tickets.TICKETS_SCRIPT)

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
