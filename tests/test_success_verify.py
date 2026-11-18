#!/usr/bin/env python3
"""The /success page confirms the payment server-side before it counts a purchase.

    python3 -m unittest tests.test_success_verify
"""

import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import content_checkout  # noqa: E402
import shell  # noqa: E402


class SuccessVerify(unittest.TestCase):
    def setUp(self):
        self.html = content_checkout.success()
        self.html = self.html if isinstance(self.html, str) else str(self.html)

    def test_ticket_endpoint_is_the_worker_ticket_route(self):
        self.assertEqual(shell.TICKET_ENDPOINT, "https://newsletter-api.max-petrusenko.workers.dev/api/ticket")
        self.assertIn(shell.TICKET_ENDPOINT + "?session_id=", self.html)
        self.assertNotIn("__TICKET_ENDPOINT__", self.html)

    def test_ticket_box_starts_hidden(self):
        self.assertRegex(self.html, r'id="mci-ticket"[^>]*\bhidden\b')
        self.assertIn('id="mci-ticket-qr"', self.html)

    def test_checkout_completed_only_after_paid_and_deduped(self):
        script = self.html[self.html.index("function () {\n    var q = new URLSearchParams"):]
        capture = script.index("posthog.capture('checkout_completed'")
        paid_gate = script.index("if (!t || !t.paid) return;")
        dedupe = script.index("localStorage.getItem(key)")
        self.assertLess(paid_gate, capture)
        self.assertLess(dedupe, capture)
        # one capture site only, and not from the bare URL
        self.assertEqual(len(re.findall(r"checkout_completed'", self.html)), 1)

    def test_qr_goes_in_as_an_image_not_markup(self):
        self.assertIn("data:image/svg+xml", self.html)
        self.assertNotIn("innerHTML = t.qr_svg", self.html)


if __name__ == "__main__":
    unittest.main()
