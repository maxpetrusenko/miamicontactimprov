#!/usr/bin/env python3
"""Footer carries the one-email-a-month form; the popup offers 10% off the first class, opens at 10s or 40% scroll, and remembers 7 days."""

import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import shell  # noqa: E402
import signup  # noqa: E402


class FooterAndPopup(unittest.TestCase):
    def test_footer_has_one_email_a_month_form_without_discount(self):
        for lang, heading in (("en", "One email a month"), ("es", "Un correo al mes")):
            html = shell.footer(lang, "/")
            self.assertEqual(html.count("<form"), 1)
            self.assertIn("subscribe-form", html)
            self.assertIn(heading, html)
            self.assertIn(shell.SUBSCRIBE_ENDPOINT, html)
            self.assertIn('data-source="miamicontactimprov:footer:', html)
            visible = re.sub(r"<[^>]+>", " ", html.split('<div class="signup-step" data-step="2"')[0])
            self.assertNotIn("%", visible)
            self.assertNotIn("discount", visible.lower())

    def test_built_pages_have_footer_form(self):
        pages = list((ROOT / "site").rglob("*.html"))
        self.assertGreater(len(pages), 20)
        for page in pages:
            text = page.read_text()
            m = re.search(r'<footer class="site-footer">.*?</footer>', text, re.S)
            if m:
                self.assertEqual(m.group(0).count("<form"), 1, str(page))

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
        self.assertIn("Join the list", html)
        self.assertIn("10% off your first class", html)
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

    def test_popup_triggers_ten_seconds_or_forty_percent_scroll(self):
        js = signup.SCRIPT
        self.assertIn("setTimeout(function () { fire('time'); }, 10000)", js)
        self.assertIn(">= 0.4) fire('scroll')", js)
        self.assertNotIn("5000", js)
        self.assertIn("{ trigger:", js)

    def test_popup_is_bottom_sheet_on_mobile(self):
        css = (ROOT / "site" / "assets" / "site.css").read_text()
        self.assertIn("@media (max-width: 640px)", css)
        self.assertIn("align-items: flex-end", css)

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
            self.assertIn('class="signup-emailed" hidden', html)
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
        self.assertIn("rb.addEventListener('click', function () { openModal('ribbon'); })", js)
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

    def test_emailed_line_only_when_worker_says_emailed_and_no_plain_email_to_posthog(self):
        js = signup.SCRIPT
        self.assertIn("emailedEl.hidden = data.emailed !== true", js)
        self.assertIn("posthog.identify(hex);", js)
        self.assertNotIn("posthog.identify(hex,", js)

    def test_verify_endpoints_derive_from_subscribe_endpoint(self):
        js = signup.SCRIPT
        for path in ("'/subscribe'", "'/verify'", "'/resend-code'"):
            self.assertIn(path, js)
        self.assertIn("30", js)


if __name__ == "__main__":
    unittest.main()
