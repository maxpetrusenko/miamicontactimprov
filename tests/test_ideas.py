#!/usr/bin/env python3
"""Tests for /ideas (pricing + ambassador plan, slice 3). Offline.

    python3 -m unittest discover -s tests
"""

import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import build  # noqa: E402
import content_checkout  # noqa: E402
import content_ideas  # noqa: E402
import shell  # noqa: E402

# Must equal IDEAS in the Worker's src/ideas.ts (id, threshold).
WORKER_IDEAS = [
    ("ci-acro", 20), ("eros-contact", 20), ("tantra-bodywork-lab", 20), ("parents-kids", 10),
    ("ci-live-music", 20), ("outdoor-beach", 20), ("extended-jam", 15),
]


class IdeasPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = content_ideas.ideas()

    def test_cards_match_the_worker(self):
        cards = re.findall(r'data-idea="([a-z-]+)" data-threshold="(\d+)"', self.html)
        self.assertEqual([(i, int(t)) for i, t in cards], WORKER_IDEAS)

    def test_parents_card_counts_families_and_kids(self):
        card = self.html.split('id="parents-kids"', 1)[1].split("</article>", 1)[0]
        self.assertIn("of 10 families", card)
        self.assertIn('class="idea-kids"', card)
        self.assertIn('data-families="1"', card)
        self.assertIn('name="adults"', self.html)
        self.assertIn('name="kids"', self.html)

    def test_eros_contact_is_consent_framed(self):
        card = self.html.split('id="eros-contact"', 1)[1].split("</article>", 1)[0]
        self.assertIn("Adults only", card)
        self.assertIn("consent", card)

    def test_three_levels_and_a_suggest_card(self):
        for level in ("definitely", "probably", "curious"):
            self.assertIn(f'data-level="{level}"', self.html)
        self.assertIn('id="idea-suggest"', self.html)

    def test_ref_attribution_and_share_line(self):
        script = content_ideas.IDEAS_SCRIPT
        self.assertIn("q.get('ref')", script)
        self.assertIn("/ideas?ref=", script)
        self.assertIn("more ' + unit + ' needed", script)

    def test_endpoint_and_labels(self):
        self.assertIn(f'data-endpoint="{shell.IDEAS_ENDPOINT}"', self.html)
        for input_id in ("idea-email", "idea-consent", "idea-adults", "idea-kids", "sg-title"):
            self.assertIn(f'for="{input_id}"', self.html)

    def test_cards_use_the_site_card_component(self):
        self.assertEqual(self.html.count('<article class="card"'), len(WORKER_IDEAS))
        self.assertIn('class="grid"', self.html)

    def test_no_badges(self):
        self.assertNotRegex(self.html, r'class="[^"]*badge')


class IdeasDiscovery(unittest.TestCase):
    def test_in_nav_and_sitemap_table(self):
        self.assertIn("ideas", [slug for slug, _ in shell.NAV])
        self.assertIn("/ideas", [row["route"] for row in build.rows()])

    def test_success_page_links_to_ideas(self):
        self.assertIn('href="/ideas"', content_checkout.success())


if __name__ == "__main__":
    unittest.main()
