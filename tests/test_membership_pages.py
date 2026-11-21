#!/usr/bin/env python3
"""Membership pages and the Black Friday strip.

    python3 -m unittest tests.test_membership_pages
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
import content_checkout  # noqa: E402
import content_membership  # noqa: E402
import guide_bar  # noqa: E402
import locales  # noqa: E402
import seo_variants  # noqa: E402


def html(fn):
    out = fn()
    return out if isinstance(out, str) else str(out)


class Window(unittest.TestCase):
    def test_window_is_nov_27_to_dec_1_eastern(self):
        self.assertEqual(bf_bar.BF_START, "2026-11-27T00:00:00-05:00")
        self.assertEqual(bf_bar.BF_END, "2026-12-01T23:59:59.999-05:00")

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_script_window_boundaries(self):
        # Run the real COMMON script against a stub window and probe active()/open().
        script = re.search(r"<script>(.*)</script>", bf_bar.COMMON, re.S).group(1)
        probe = (
            "var window = { location: { search: '' } }; var sessionStorage = { getItem: function () { return null; }, setItem: function () {} };\n"
            + script
            + "\nvar b = window.mciBf; var t = function (s) { return Date.parse(s); };\n"
            "console.log(JSON.stringify({"
            "before: b.active(t('2026-11-26T23:59:59.999-05:00')),"
            "start: b.active(t('2026-11-27T00:00:00-05:00')),"
            "end: b.active(t('2026-12-01T23:59:59.999-05:00')),"
            "after: b.active(t('2026-12-02T00:00:00-05:00')),"
            "openBefore: b.open(t('2026-11-21T00:00:00-05:00')),"
            "openAfter: b.open(t('2026-12-02T00:00:00-05:00'))}));"
        )
        out = subprocess.run(["node", "-e", probe], capture_output=True, text=True, check=True).stdout
        self.assertEqual(
            json.loads(out),
            {"before": False, "start": True, "end": True, "after": False, "openBefore": True, "openAfter": False},
        )


class Strip(unittest.TestCase):
    def test_starts_hidden_and_links_with_utm(self):
        self.assertIn('id="mci-bf-bar" hidden', bf_bar.MARKUP)
        self.assertIn("utm_source=site&utm_medium=bf-bar&utm_campaign=bf-2026", bf_bar.MARKUP)
        self.assertIn("/membership?", bf_bar.MARKUP)

    def test_where_it_shows(self):
        self.assertTrue(bf_bar.shows("/", "en"))
        self.assertTrue(bf_bar.shows("/pricing", "en"))
        self.assertTrue(bf_bar.shows("/membership", "en"))
        for path in ("/pay", "/success", "/membership/success", "/membership/manage", "/t/CI10ABCDEF", "/guide/", "/guide/sharing-weight"):
            self.assertFalse(bf_bar.shows(path, "en"), path)
        self.assertFalse(bf_bar.shows("/es/", "es"))

    def test_guide_bar_stays_off_member_pages(self):
        self.assertFalse(guide_bar.shows("/membership/success", "en"))
        self.assertFalse(guide_bar.shows("/membership/manage", "en"))
        self.assertTrue(guide_bar.shows("/membership", "en"))

    def test_view_event_fires_once_per_page(self):
        self.assertIn("bf_view", bf_bar.COMMON)
        self.assertIn("if (seen) return;", bf_bar.COMMON)


def main_of(page):
    return page[page.index("<main"):page.index("</main>")]


class MembershipPage(unittest.TestCase):
    def setUp(self):
        self.page = html(content_membership.membership)
        self.main = main_of(self.page)

    def test_two_plans_and_prices(self):
        self.assertIn('data-plan="monthly"', self.page)
        self.assertIn('data-plan="yearly"', self.page)
        self.assertIn("$40 a month", self.page)
        self.assertIn("$260 a year", self.page)
        self.assertIn("up to 8 banked", self.page)
        self.assertIn("not jams or workshops", self.page)

    def test_checkout_goes_to_the_worker_membership_route(self):
        self.assertEqual(bf_bar.CHECKOUT_ENDPOINT, "https://newsletter-api.max-petrusenko.workers.dev/api/membership/checkout")
        self.assertIn(bf_bar.CHECKOUT_ENDPOINT, self.page)

    def test_offer_section_starts_hidden_and_promises_no_discount(self):
        self.assertRegex(self.page, r'id="mci-bf"[^>]*\bhidden\b')
        self.assertIn("bring-a-friend pass every month for your first three months", self.page)
        self.assertIn("The prices stay the same", self.page)
        self.assertNotRegex(self.main, r"(?i)% off|discount")

    def test_funnel_events_carry_plan_bf_and_utm(self):
        for name in ("bf_view", "membership_checkout_started"):
            self.assertIn(name, self.page)
        self.assertIn("bf.utm()", self.page)
        self.assertIn("bf.capture('membership_checkout_started', props)", self.page)
        # started only after the Worker answered with a Stripe url
        self.assertLess(self.page.index("res.data.url"), self.page.index("membership_checkout_started"))

    def test_no_helper_text_or_status_badges(self):
        self.assertNotIn("price-note", self.main)
        self.assertNotIn("badge", self.main.lower())


class SuccessPage(unittest.TestCase):
    def setUp(self):
        self.page = html(content_membership.membership_success)

    def test_completed_only_after_paid_and_deduped(self):
        paid = self.page.index("if (!m || !m.paid) return;")
        dedupe = self.page.index("localStorage.getItem(key)")
        capture = self.page.index("membership_checkout_completed")
        stored = self.page.index("localStorage.setItem(key, '1')")
        self.assertLess(paid, capture)
        self.assertLess(dedupe, capture)
        self.assertLess(capture, stored)

    def test_waits_for_the_stored_offer_decision_before_counting(self):
        pending = self.page.index("m.pending && attempt < 4")
        capture = self.page.index("membership_checkout_completed")
        self.assertLess(pending, capture)
        self.assertNotIn("session.created", self.page)

    def test_session_id_leaves_the_address_bar(self):
        self.assertIn("q.delete('session_id')", self.page)
        self.assertIn("history.replaceState", self.page)

    def test_manage_link_and_passes_start_hidden(self):
        self.assertRegex(self.page, r'id="mci-manage"[^>]*\bhidden\b')
        self.assertRegex(self.page, r'id="mci-bf-passes"[^>]*\bhidden\b')
        self.assertIn(bf_bar.SESSION_ENDPOINT + "?session_id=", self.page)


class ManagePage(unittest.TestCase):
    def setUp(self):
        self.page = html(content_membership.membership_manage)

    def test_posts_member_id_to_the_portal_route(self):
        self.assertIn(bf_bar.PORTAL_ENDPOINT, self.page)
        self.assertIn("[0-9a-f]{32}", self.page)

    def test_member_id_leaves_the_url_before_posthog_loads(self):
        head = self.page[: self.page.index("</head>")]
        strip = head.index("window.__mciManageId = m;")
        self.assertIn("history.replaceState", head[strip:])
        # extra_head is emitted immediately before the PostHog loader (the loader is empty
        # in a build without POSTHOG_KEY, so check the template rather than the output)
        shell_src = (ROOT / "build" / "shell.py").read_text()
        self.assertIn("{extra_head}{posthog_snippet()}", shell_src)
        body = self.page[self.page.index("<main"):]
        self.assertNotIn("location.search", body)
        self.assertIn("window.__mciManageId", body)


class Routes(unittest.TestCase):
    def test_registered_and_private(self):
        self.assertEqual(locales.route("membership", "en"), "/membership")
        self.assertEqual(locales.route("membership-success", "en"), "/membership/success")
        self.assertEqual(locales.route("membership-manage", "en"), "/membership/manage")
        self.assertIn("/membership/success", seo_variants.PRIVATE_ROUTES)
        self.assertIn("/membership/manage", seo_variants.PRIVATE_ROUTES)
        self.assertNotIn("/membership", seo_variants.PRIVATE_ROUTES)

    def test_pricing_links_to_membership(self):
        self.assertIn('href="/membership"', html(content_checkout.pricing))

    def test_no_dark_mode_in_the_stylesheet(self):
        css = (ROOT / "site" / "assets" / "site.css").read_text()
        self.assertNotIn("prefers-color-scheme: dark", css)


if __name__ == "__main__":
    unittest.main()
