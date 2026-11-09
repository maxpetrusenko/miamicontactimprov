#!/usr/bin/env python3
"""The beginner's guide: chapter length, quotation budget, routes and the committed PDF.

    python3 -m unittest tests.test_guide
"""

import html
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import guide_chapters  # noqa: E402
import locales  # noqa: E402

PDF = ROOT / "build" / "static" / "guide" / "contact-improvisation-beginners-guide.pdf"


def words(fragment):
    text = re.sub(r"<[^>]+>", " ", fragment)
    return len(html.unescape(text).split())


class Guide(unittest.TestCase):
    def test_eight_chapters_with_routes(self):
        self.assertEqual(len(guide_chapters.CHAPTERS), 8)
        for c in guide_chapters.CHAPTERS:
            self.assertEqual(locales.route("guide-" + c["slug"], "en"), "/guide/" + c["slug"])
            self.assertIsNone(locales.route("guide-" + c["slug"], "es"))

    def test_chapter_length(self):
        for c in guide_chapters.CHAPTERS:
            n = words(c["html"])
            self.assertTrue(500 <= n <= 900, f"{c['slug']} has {n} words")

    def test_no_em_dashes_or_emoji(self):
        for c in guide_chapters.CHAPTERS:
            blob = c["html"] + c["lede"] + c["answer"]
            self.assertNotIn("—", blob, c["slug"])
            self.assertNotIn("&mdash;", blob, c["slug"])
            self.assertFalse(re.search("[\U0001F300-\U0001FAFF☀-➿]", blob), c["slug"])

    def test_quotation_budget(self):
        """At most four quotations of Keogh in the whole guide, each inside a link to martinkeogh.com."""
        linked = 0
        for c in guide_chapters.CHAPTERS:
            linked += len(re.findall(r'<a href="https://martinkeogh\.com[^"]*"[^>]*>[^<]*"[^<]*</a>', c["html"]))
        self.assertLessEqual(linked, 4)
        self.assertGreaterEqual(linked, 1)

    def test_internal_links_resolve(self):
        known = {r for routes in locales.ROUTES.values() for r in routes.values()}
        known |= {"/guide/"}
        for c in guide_chapters.CHAPTERS:
            for href in re.findall(r'href="(/[^"#]*)', c["html"]):
                self.assertIn(href, known, f"{c['slug']} links to unknown route {href}")

    def test_pdf_is_committed(self):
        self.assertTrue(PDF.is_file(), "run tools/make_guide_pdf.py and commit the PDF")
        data = PDF.read_bytes()
        self.assertGreater(len(data), 20 * 1024)
        self.assertTrue(data.startswith(b"%PDF"))

    def test_pdf_matches_guide_text(self):
        """The PDF was rendered from the current guide text (hash of the print page's main + CSS)."""
        import content_guide
        stamp = PDF.with_name(PDF.name + ".sha256")
        self.assertTrue(stamp.is_file(), "run python3 tools/make_guide_pdf.py")
        self.assertEqual(stamp.read_text().strip(), content_guide.print_fingerprint(),
                         "guide text changed since the PDF was made: run python3 tools/make_guide_pdf.py")

    def test_fingerprint_is_deterministic(self):
        import content_guide
        self.assertEqual(content_guide.print_fingerprint(), content_guide.print_fingerprint())


if __name__ == "__main__":
    unittest.main()
