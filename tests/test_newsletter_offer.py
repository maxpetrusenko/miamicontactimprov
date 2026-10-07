#!/usr/bin/env python3
"""Footer has no subscribe form; the popup offers 10% off one event and remembers 7 days."""

import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import shell  # noqa: E402
import signup  # noqa: E402


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
            self.assertIn("10%", " ".join(shell.POPUP_HEADING[lang]))
            self.assertIn("10%", shell.SUBSCRIBE_COPY[lang]["label"])
            html = shell.newsletter_popup(lang, "/")
            self.assertIn("10%", html)
            self.assertNotIn("next two months", html)
            self.assertNotIn("dos meses", html)

    def test_success_line_names_monthly_discount(self):
        for lang in ("en", "es"):
            ok = shell.SUBSCRIBE_COPY[lang]["ok"]
            self.assertIn("20%", ok)
            self.assertNotIn("\u2014", ok)

    def test_no_monthly_dates_heading_in_built_site(self):
        for page in (ROOT / "site").rglob("*.html"):
            text = page.read_text()
            self.assertNotIn("The monthly dates", text, page.name)
            self.assertNotIn("Las fechas del mes", text, page.name)

    def test_popup_fields_order_and_buttons(self):
        html = shell.newsletter_popup("en", "/")
        pos = [html.index(m) for m in ('name="name"', 'name="email"', 'name="country"', 'name="phone"', 'name="consent"', "SECURE YOUR SPACE", "NO THANKS")]
        self.assertEqual(pos, sorted(pos))
        self.assertIn('placeholder="First name"', html)
        self.assertIn("Sign up to receive", html)
        self.assertIn("a 10% discount code", html)
        self.assertIn('<option value="US">United States (+1)</option>', html)
        self.assertEqual(html.count("<option"), 2)
        self.assertIn("I agree to receive promotional emails and text messages from Miami CI. Message and data rates may apply.", html)
        self.assertNotIn("Miami Contact Improv", html)

    def test_inline_form_uses_get_my_code(self):
        html = shell.subscribe_form("en", source="x", uid="t")
        self.assertIn("Get my code", html)
        self.assertNotIn("NO THANKS", html)
        self.assertIn('name="name"', html)

    def test_popup_script_uses_seven_day_and_subscribed_keys(self):
        js = signup.SCRIPT
        self.assertIn("mci_popup_closed_at", js)
        self.assertIn("mci_popup_subscribed", js)
        self.assertIn("7 * 24 * 60 * 60 * 1000", js)
        self.assertNotIn("mci_popup_seen", js)

    def test_stage_markup_in_popup_inline_and_card(self):
        for html in (
            shell.newsletter_popup("en", "/"),
            shell.subscribe_form("en", source="x", uid="t"),
            shell.newsletter_card("en"),
        ):
            for stage in ("1", "2", "3"):
                self.assertIn(f'data-step="{stage}"', html)
            self.assertIn("novalidate", html)
            self.assertIn('autocomplete="one-time-code"', html)
            self.assertIn('inputmode="numeric"', html)
            self.assertIn('maxlength="6"', html)
            self.assertIn("Enter 6 digit one-time code below", html)
            self.assertIn("Didn't get code?", html)
            self.assertIn("SIGN UP", html)
            self.assertIn("We appreciate you!", html)
            self.assertIn("Thank you!", html)
            self.assertIn("We also emailed it to you.", html)
            self.assertIn("Welcome to", html)
            self.assertIn("Miami CI", html)
        # a promo code is never in the markup; only the verify reply can supply one
        self.assertNotIn("CI10-", shell.newsletter_popup("en", "/"))
        self.assertIn("NO THANKS", shell.newsletter_popup("en", "/"))
        self.assertIn("NO, GRACIAS", shell.newsletter_popup("es", "/es"))

    def test_ribbon_markup_and_visibility_logic(self):
        for lang, label in (("en", "GET 10% OFF"), ("es", "10% DE DESCUENTO")):
            html = signup.ribbon(lang)
            self.assertIn(label, html)
            self.assertIn("aria-label=", html)
            self.assertIn("<button", html)
            self.assertIn("hidden", html)
        js = signup.SCRIPT
        # shown only when not subscribed, opens the popup regardless of the weekly timer,
        # hidden while the popup is open
        self.assertIn("ribbon.hidden = isSubscribed()", js)
        self.assertIn("rb.addEventListener('click', openModal)", js)
        self.assertIn("mci-popup-open", js)
        css = (ROOT / "site" / "assets" / "site.css").read_text()
        self.assertIn(".mci-popup-open .mci-ribbon", css)
        self.assertIn("@media (max-width: 480px) { .mci-ribbon", css)
        page = (ROOT / "site" / "index.html").read_text()
        self.assertIn('id="mci-ribbon"', page)

    def test_card_on_home_and_jams_not_footer(self):
        for path in ("index.html", "jams.html", "es/index.html", "es/jams.html"):
            html = (ROOT / "site" / path).read_text()
            self.assertEqual(html.count('data-source="miamicontactimprov:newsletter-card"'), 1, path)
            self.assertIn("newsletter-card-big", html)
            m = re.search(r'<footer class="site-footer">.*?</footer>', html, re.S)
            self.assertNotIn("newsletter-card", m.group(0))
        en = (ROOT / "site" / "index.html").read_text()
        self.assertIn("Join the jam list", en)
        self.assertIn("Be the first to know", en)
        self.assertIn("I want to subscribe to your mailing list.", en)

    def test_verify_endpoints_derive_from_subscribe_endpoint(self):
        js = signup.SCRIPT
        for path in ("'/subscribe'", "'/verify'", "'/resend-code'"):
            self.assertIn(path, js)
        self.assertIn("30", js)


if __name__ == "__main__":
    unittest.main()
