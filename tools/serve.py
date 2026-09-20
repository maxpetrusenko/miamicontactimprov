#!/usr/bin/env python3
"""Local dev server for site/ that mimics Cloudflare Pages clean URLs.

`python3 -m http.server` serves files literally, so /events 404s (the file is
events.html). This maps /events -> site/events.html, /es/ -> site/es/index.html,
and serves site/404.html for misses, the way production does.

Usage:  python3 tools/serve.py [port]    # default 8000
"""
import http.server, socketserver, os, sys, urllib.parse

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def translate_path(self, path):
        fs = super().translate_path(urllib.parse.urlparse(path).path)
        if os.path.isdir(fs):
            idx = os.path.join(fs, "index.html")
            return idx if os.path.exists(idx) else fs
        if os.path.exists(fs):
            return fs
        if not os.path.splitext(fs)[1] and os.path.exists(fs + ".html"):
            return fs + ".html"
        return fs

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            page = os.path.join(ROOT, "404.html")
            if os.path.exists(page):
                body = open(page, "rb").read()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
        return super().send_error(code, message, explain)


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"serving site/ at http://localhost:{port}  (clean URLs, like production)")
    print("Ctrl+C to stop")
    httpd.serve_forever()
