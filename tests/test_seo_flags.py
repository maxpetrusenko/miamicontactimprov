#!/usr/bin/env python3
"""SEO Phase 1 flags: stable hash, both arms populated, control output untouched.

    python3 -m unittest tests.test_seo_flags
"""

import copy
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import seo_flags  # noqa: E402
import seo_variants  # noqa: E402

SAMPLE = [f"/sample-page-{i}" for i in range(20)]


class Hash(unittest.TestCase):
    def test_fnv1a32_known_vectors(self):
        self.assertEqual(seo_flags.fnv1a32(""), 0x811C9DC5)
        self.assertEqual(seo_flags.fnv1a32("a"), 0xE40C292C)
        self.assertEqual(seo_flags.fnv1a32("foobar"), 0xBF9CF968)

    def test_stable_assignment(self):
        got = [seo_flags.is_variant("seo_h003_titles", p) for p in SAMPLE]
        self.assertEqual(got, [seo_flags.is_variant("seo_h003_titles", p) for p in SAMPLE])
        self.assertEqual(seo_flags.fnv1a32("seo_h003_titles:/miami"), 2490939730)

    def test_both_arms_across_20_paths(self):
        for key in seo_flags.page_keys():
            arms = {seo_flags.is_variant(key, p) for p in SAMPLE}
            self.assertEqual(arms, {True, False}, key)

    def test_normalisation(self):
        self.assertEqual(seo_flags.normalize_path("/Miami/?x=1"), "/miami")
        self.assertEqual(seo_flags.normalize_path(""), "/")
        self.assertEqual(
            seo_flags.is_variant("seo_h003_titles", "/Miami-Jams/"),
            seo_flags.is_variant("seo_h003_titles", "/miami-jams"))

    def test_homepage_always_control(self):
        for key in seo_flags.page_keys():
            self.assertFalse(seo_flags.is_variant(key, "/"))

    def test_disabled_flag_is_control_everywhere(self):
        cfg = copy.deepcopy(seo_flags.CONFIG)
        for f in cfg["flags"].values():
            f["enabled"] = False
        for key in seo_flags.page_keys(cfg):
            self.assertFalse(any(seo_flags.is_variant(key, p, cfg) for p in SAMPLE))


class Copy(unittest.TestCase):
    def test_titles(self):
        for route, t in seo_variants.TITLES.items():
            self.assertLessEqual(len(t), 60, route)
            self.assertTrue(t.endswith("| Miami Contact Improv"), route)

    def test_tldr_length(self):
        for route, t in seo_variants.TLDR.items():
            self.assertTrue(40 <= len(t.split()) <= 60, (route, len(t.split())))

    def test_related_links(self):
        import locales
        public = {locales.route(slug, "en") for slug, lang in locales.ORDER if lang == "en"}
        for route, links in seo_variants.RELATED.items():
            self.assertTrue(3 <= len(links) <= 5, route)
            for href, _label in links:
                self.assertIn(href, public, (route, href))
                self.assertNotEqual(href, route)


class Apply(unittest.TestCase):
    PAGE = ('<head><title>Old</title><meta property="og:title" content="Old">'
            '<meta name="twitter:title" content="Old">'
            '<meta name="theme-color" content="#fff">'
            '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1"></head>'
            '<body><main><h1>H</h1></main></body>')

    def test_control_only_adds_meta(self):
        out = seo_variants.apply(self.PAGE, "/", "en")
        self.assertIn('<meta name="seo-variants" content="h005=s;h021=s;h003=c;h013=c;h014=c;h015=c;h022=c">', out)
        self.assertEqual(out.replace(re.search(r'<meta name="seo-variants"[^>]*>\n', out).group(0), ""), self.PAGE)

    def test_private_pages_noindex(self):
        out = seo_variants.apply(self.PAGE, "/pay", "en")
        self.assertIn('content="noindex, follow"', out)


if __name__ == "__main__":
    unittest.main()
