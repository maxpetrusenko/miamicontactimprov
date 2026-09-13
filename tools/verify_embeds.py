#!/usr/bin/env python3
"""Re-verify every video in build/videos_data.py is still embeddable.

Network-dependent, so it is deliberately NOT wired into the deploy gate. Run it
whenever a video is added or when the video room is touched.

Exit 0 = every entry verified. Exit 1 = at least one entry needs attention.
Exit 2 = could not run.

Vimeo caveat: a 200 from the oEmbed endpoint is NOT proof of embeddability. The
payload carries domain_status_code, and 403 there means the owner restricted
embedding to specific domains even though the HTTP status is fine. Check both.
"""

import concurrent.futures
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, "build")
import videos_data  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}


def check(v):
    vid, platform = v[0], v[1]
    if platform == "youtube":
        url = ("https://www.youtube.com/oembed?url="
               + urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}", safe="")
               + "&format=json")
    else:
        url = "https://vimeo.com/api/oembed.json?url=" + urllib.parse.quote(f"https://vimeo.com/{vid}", safe="")

    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        return vid, platform, f"HTTP {e.code}", "embedding disabled by the owner" if e.code in (401, 403) else ""
    except Exception as e:  # noqa: BLE001
        return vid, platform, f"ERR {type(e).__name__}", str(e)[:80]

    if platform == "vimeo":
        code = payload.get("domain_status_code")
        if code and int(code) >= 400:
            return vid, platform, f"domain_status_code={code}", "embed restricted to an allow-list"
    if not payload.get("html"):
        return vid, platform, "no iframe html", "payload did not include an embed"
    title = (payload.get("title") or "")[:58]
    return vid, platform, "OK", title


def main():
    if not videos_data.VIDEOS:
        print("VIDEOS is empty", file=sys.stderr)
        return 2
    bad = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for vid, platform, status, note in ex.map(check, videos_data.VIDEOS):
            flag = "ok " if status == "OK" else "BAD"
            print(f"{flag} {vid:14} {platform:8} {status:20} {note}")
            if status != "OK":
                bad.append((vid, platform, status))
    print(f"\nverified {len(videos_data.VIDEOS) - len(bad)} of {len(videos_data.VIDEOS)}")
    if bad:
        print("not embeddable:", ", ".join(f"{v} ({p})" for v, p, _ in bad))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
