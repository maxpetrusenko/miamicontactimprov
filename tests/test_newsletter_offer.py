#!/usr/bin/env python3
"""Footer has no subscribe form; the popup offers 10% off one event and remembers 7 days."""

import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import shell  # noqa: E402


class FooterAndPopup(unittest.TestCase):
    def test_footer_has_no_subscribe_form(self):
        for lang in ("en", "es"):
            html = shell.footer(lang, "/")
            self.assertNotIn("subscribe-form", html)
            self.assertNotIn("<form", html)
            self.assertNotIn("footer-subscribe", html)

    def test_built_pages_have_no_footer_form(self):
        for page in (ROOT / "site").glob("*.html"):
            m = re.search(r'<footer class="site-footer">.*?</footer>', page.read_text(), re.S)
            if m:
                self.assertNotIn("<form", m.group(0), page.name)

    def test_popup_copy_is_ten_percent_one_event(self):
        for lang in ("en", "es"):
            self.assertIn("10%", shell.POPUP_HEADING[lang])
            self.assertIn("10%", shell.SUBSCRIBE_COPY[lang]["label"])
            html = shell.newsletter_popup(lang, "/")
            self.assertIn("10%", html)
            self.assertNotIn("20%", html)

    def test_popup_script_uses_seven_day_and_subscribed_keys(self):
        src = (ROOT / "build" / "shell.py").read_text()
        self.assertIn("mci_popup_closed_at", src)
        self.assertIn("mci_popup_subscribed", src)
        self.assertIn("7 * 24 * 60 * 60 * 1000", src)
        self.assertNotIn("mci_popup_seen", src)


if __name__ == "__main__":
    unittest.main()
