"""SEO Phase 1 experiment flags (seo-p1-2026-11).

Assignment is decided here, at build time, from the page path alone, so Googlebot and
users get the same HTML. Nothing is decided on the client. To revert a flag set
`enabled: false` in seo-flags.json at the repo root, rebuild and redeploy: every page
then renders exactly as it did before the experiment.
"""

import json
import pathlib

FLAGS_PATH = pathlib.Path(__file__).resolve().parent.parent / "seo-flags.json"

# Short code used in <meta name="seo-variants"> and in the PostHog property names.
SHORT = {
    "seo_h005_ai_crawlers": "h005",
    "seo_h021_indexing": "h021",
    "seo_h003_titles": "h003",
    "seo_h013_keyword_placement": "h013",
    "seo_h014_tldr": "h014",
    "seo_h015_open_faq": "h015",
    "seo_h022_internal_links": "h022",
}


def load(path=FLAGS_PATH):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


CONFIG = load()


def fnv1a32(text):
    h = 0x811C9DC5
    for b in text.encode("utf-8"):
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return h


def normalize_path(path):
    path = (path or "/").split("?", 1)[0].split("#", 1)[0].lower()
    if not path.startswith("/"):
        path = "/" + path
    if len(path) > 1:
        path = path.rstrip("/") or "/"
    return path


def site_enabled(key, config=None):
    flag = (config or CONFIG)["flags"].get(key, {})
    return bool(flag.get("enabled"))


def is_variant(key, path, config=None):
    """True when `path` is in the variant arm of page-scope flag `key`.

    The homepage is always control: it is the money page.
    """
    flag = (config or CONFIG)["flags"].get(key)
    if not flag or not flag.get("enabled") or flag.get("scope") != "page":
        return False
    norm = normalize_path(path)
    if norm == "/":
        return False
    return fnv1a32(f"{key}:{norm}") % 100 < int(round(flag["split"] * 100))


def page_keys(config=None):
    return [k for k, f in (config or CONFIG)["flags"].items() if f.get("scope") == "page"]


def variant_map(path, has_content, config=None):
    """{short code: 'v' | 'c' | 's'} for one page.

    `has_content(key)` says whether this page has a variant written for that flag. A page
    assigned to the variant arm with nothing written for it is reported as control, so the
    analysis never counts an untreated page as treated.
    """
    cfg = config or CONFIG
    out = {}
    for key, flag in cfg["flags"].items():
        if flag.get("scope") == "site":
            out[SHORT[key]] = "s"
        else:
            out[SHORT[key]] = "v" if is_variant(key, path, cfg) and has_content(key) else "c"
    return out


def meta_tag(variants):
    content = ";".join(f"{k}={v}" for k, v in variants.items())
    return f'<meta name="seo-variants" content="{content}">'
