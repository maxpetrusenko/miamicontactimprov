#!/usr/bin/env python3
"""H006 kill switch: with seo_h006 off, a build over an existing site/ removes the pages.

    python3 -m unittest tests.test_buyer_flag
"""

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

from buyer_routes import ROUTES  # noqa: E402


class KillSwitch(unittest.TestCase):
    def test_flag_off_prunes_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            shutil.copytree(ROOT / "build", tmp / "build", ignore=shutil.ignore_patterns("__pycache__"))
            cfg = json.loads((ROOT / "seo-flags.json").read_text())
            out = tmp / "out"
            for enabled in (True, False):
                cfg["flags"]["seo_h006"]["enabled"] = enabled
                (tmp / "seo-flags.json").write_text(json.dumps(cfg))
                subprocess.run([sys.executable, str(tmp / "build" / "build.py"), "--out", str(out)],
                               check=True, capture_output=True, cwd=tmp)
                for route in ROUTES.values():
                    stem = route.strip("/")
                    for rel in (f"{stem}.html", f"{stem}/index.html"):
                        self.assertEqual((out / rel).exists(), enabled, rel)
                self.assertEqual("h006=s" in (out / "index.html").read_text(), enabled)


if __name__ == "__main__":
    unittest.main()
