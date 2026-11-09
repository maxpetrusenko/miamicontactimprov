#!/usr/bin/env python3
"""Render /guide/print to the committed guide PDF with headless Chrome.

    python3 build/make_assets.py && python3 build/build.py --out site
    python3 tools/make_guide_pdf.py
    python3 build/build.py --out site      # copies the PDF into site/guide/

The PDF is a committed SOURCE file (build/static/guide/...). CI has no Chrome step, so
build/build.py only copies it and tools/gate.py only checks that it exists, is over 20 KB
and starts with %PDF. Re-run this script whenever the chapter text changes.

Serves site/ with tools/serve.py on a free port so the print page loads its stylesheet and
fonts the way a visitor would, then prints it. Exit 0 and one line on success; non-zero
with the reason otherwise.
"""

import argparse
import pathlib
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "static" / "guide" / "contact-improvisation-beginners-guide.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MIN_BYTES = 20 * 1024


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for(url, seconds=10):
    end = time.time() + seconds
    while time.time() < end:
        try:
            urllib.request.urlopen(url, timeout=1).read(1)
            return True
        except Exception:  # noqa: BLE001
            time.sleep(0.2)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chrome", default=CHROME)
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    if not pathlib.Path(args.chrome).exists():
        print(f"Chrome not found at {args.chrome}", file=sys.stderr)
        return 2
    if not (ROOT / "site" / "guide" / "print.html").is_file():
        print("site/guide/print.html missing: run python3 build/build.py --out site first", file=sys.stderr)
        return 2

    port = free_port()
    server = subprocess.Popen(
        [sys.executable, str(ROOT / "tools" / "serve.py"), str(port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    profile = tempfile.mkdtemp(prefix="guide-pdf-")
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(profile) / "guide.pdf"
    try:
        url = f"http://127.0.0.1:{port}/guide/print"
        if not wait_for(url):
            print("local server did not start", file=sys.stderr)
            return 2
        subprocess.run(
            [args.chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             f"--user-data-dir={profile}", "--virtual-time-budget=15000",
             f"--print-to-pdf={tmp}", url],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
        )
        data = tmp.read_bytes() if tmp.is_file() else b""
        if not data.startswith(b"%PDF") or len(data) < MIN_BYTES:
            print(f"Chrome produced {len(data)} bytes that are not a usable PDF", file=sys.stderr)
            return 1
        out.write_bytes(data)
        print(f"wrote {out} ({len(data)} bytes)")
        return 0
    finally:
        server.terminate()
        shutil.rmtree(profile, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
