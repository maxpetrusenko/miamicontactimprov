#!/usr/bin/env python3
"""The free-guide announcement bar: on English pages, absent on the guide and checkout.

    python3 -m unittest tests.test_guide_bar
"""

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import guide_bar  # noqa: E402
import shell  # noqa: E402


def render(path, lang="en"):
    return shell.page("T", "d", path, "<p>x</p>", lang=lang)


class GuideBar(unittest.TestCase):
    def test_on_home(self):
        out = render("/")
        self.assertIn('id="mci-guide-bar"', out)
        self.assertIn("Download the PDF", out)
        self.assertIn('download data-gn="pdf"', out)
        self.assertLess(out.index("mci-guide-bar"), out.index('class="site-header"'))

    def test_absent_on_guide_and_checkout(self):
        for path in ("/guide/", "/guide/print", "/guide/what-is-contact-improvisation", "/pay", "/success", "/t/"):
            self.assertNotIn("mci-guide-bar", render(path), path)

    def test_absent_on_spanish(self):
        self.assertNotIn("mci-guide-bar", render("/es/", "es"))

    def test_copy_clean(self):
        blob = guide_bar.MARKUP + guide_bar.SCRIPT
        self.assertNotIn("—", blob)
        self.assertNotIn("&mdash;", blob)


if __name__ == "__main__":
    unittest.main()
