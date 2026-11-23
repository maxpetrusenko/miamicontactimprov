"""Black Friday 2026: the strip above the header, and the shared membership/BF script.

Offer (Max, 2026-11-21): a membership bought between Nov 27 00:00 and Dec 1 23:59
America/New_York comes with one free bring-a-friend pass a month for the first three
months. No price change. The Worker (newsletter-api, src/bf.ts) decides who actually
gets the passes, on payment time; this file only decides what the page shows.

The strip is in the HTML but `hidden`; the script shows it only while the window is
active (START <= now <= END), so nothing shows before Nov 27 00:00 ET or after Dec 1
23:59:59 ET. No JS means no strip, which is the safe failure after the offer ends.
"""

# Both instants carry the EST offset: DST ended Nov 1, 2026. Keep in sync with
# newsletter-api src/bf.ts (BF_START, BF_END).
BF_START = "2026-11-27T00:00:00-05:00"
BF_END = "2026-12-01T23:59:59.999-05:00"

API = "https://newsletter-api.max-petrusenko.workers.dev/api/membership"
CHECKOUT_ENDPOINT = API + "/checkout"
SESSION_ENDPOINT = API + "/session"
PORTAL_ENDPOINT = API + "/portal"

BAR_HREF = "/membership?utm_source=site&utm_medium=bf-bar&utm_campaign=bf-2026"

# Pages that never carry the strip: checkout hand-offs, member-only pages, the short link.
HIDDEN_PATHS = ("/pay", "/success", "/membership/success", "/membership/manage", "/checkin")


def shows(path, lang):
    if lang != "en":
        return False
    if path in HIDDEN_PATHS or path.startswith("/t/") or path.startswith("/checkin/"):
        return False
    return path != "/guide" and not path.startswith("/guide/")


MARKUP = (
    '<div class="bf-bar" id="mci-bf-bar" hidden>'
    "<span>Black Friday, Nov 27 to Dec 1: join as a member and bring a friend free, once a month for three months. "
    f'<a href="{BAR_HREF}" data-bf="bar">See memberships</a></span>'
    "</div>"
)

# Shared by the strip, /membership, /membership/success and /membership/manage.
# window.mciBf: window dates, UTM first-touch kept for the tab, capture(), viewOnce().
COMMON = r"""<script>
(function () {
  if (window.mciBf) return;
  var START = Date.parse('%(start)s'), END = Date.parse('%(end)s');
  var FIELDS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  var utm = {};
  try {
    var q = new URLSearchParams(window.location.search);
    var saved = {};
    try { saved = JSON.parse(sessionStorage.getItem('mci_utm') || '{}') || {}; } catch (e) {}
    var fresh = false;
    FIELDS.forEach(function (f) { var v = q.get(f); if (v) { saved[f] = String(v).slice(0, 80); fresh = true; } });
    utm = saved;
    if (fresh) { try { sessionStorage.setItem('mci_utm', JSON.stringify(saved)); } catch (e) {} }
  } catch (e) {}
  var seen = false;
  window.mciBf = {
    start: START, end: END,
    active: function (now) { now = now || Date.now(); return now >= START && now <= END; },
    utm: function () { var o = {}; for (var k in utm) o[k] = utm[k]; return o; },
    capture: function (name, props) {
      try {
        if (!window.posthog) return;
        var p = props || {};
        for (var k in utm) if (!(k in p)) p[k] = utm[k];
        posthog.capture(name, p);
      } catch (e) {}
    },
    // bf_view: once per page load, by whichever BF surface rendered first.
    viewOnce: function (surface) {
      if (seen) return;
      seen = true;
      window.mciBf.capture('bf_view', { surface: surface, offer_active: window.mciBf.active() });
    }
  };
})();
</script>""" % {"start": BF_START, "end": BF_END}

BAR_SCRIPT = r"""<script>
(function () {
  var bar = document.getElementById('mci-bf-bar');
  if (!bar || !window.mciBf || !window.mciBf.active()) return;
  bar.hidden = false;
  window.mciBf.viewOnce('bar');
  bar.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('[data-bf]') : null;
    if (a) window.mciBf.capture('bf_click', { surface: a.getAttribute('data-bf') });
  });
})();
</script>"""


def bar(path, lang):
    if not shows(path, lang):
        return ""
    return MARKUP + "\n" + COMMON + "\n" + BAR_SCRIPT + "\n"
