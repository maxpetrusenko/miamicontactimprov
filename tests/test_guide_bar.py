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

    def test_no_landmark_role(self):
        self.assertNotIn('role="region"', guide_bar.MARKUP)

    def test_dismissed_state_script(self):
        out = render("/")
        self.assertIn("bar.hidden = true", out)
        self.assertIn("localStorage", out)
        self.assertIn("--gn-h", out)
        self.assertIn("getElementById('main')", out)

    def test_nav_offset_hook(self):
        out = render("/")
        self.assertIn("--nav-top", out)
        self.assertIn("getBoundingClientRect().bottom", out)
        css = (ROOT / "site" / "assets" / "site.css").read_text()
        self.assertIn("top: var(--nav-top, 71px)", css)
        self.assertIn("calc(100dvh - var(--nav-top, 71px))", css)
        self.assertIn("var(--gn-h, 0px)", css)
        self.assertIn("width: 44px; height: 44px", css)

    def test_copy_clean(self):
        blob = guide_bar.MARKUP + guide_bar.SCRIPT
        self.assertNotIn("—", blob)
        self.assertNotIn("&mdash;", blob)


if __name__ == "__main__":
    unittest.main()
