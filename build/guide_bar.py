"""The free-guide announcement bar: a thin strip above the header on English pages.

Renders in the HTML with no JS. The inline script right after it only adds the dismiss
(localStorage, 30 days) and the PostHog events, and hides the bar before first paint when
it was dismissed, so there is no flash and no layout shift for the ribbon or popup.
"""

PDF_PATH = "/guide/contact-improvisation-beginners-guide.pdf"
DISMISS_KEY = "mci_guide_bar_closed"

def shows(path, lang):
    """English pages only; not the guide (index, chapters, /guide/print) or checkout."""
    if lang != "en":
        return False
    if path in ("/pay", "/success") or path.startswith("/t/"):
        return False
    return path != "/guide" and not path.startswith("/guide/")


MARKUP = (
    '<div class="gn-bar" id="mci-guide-bar">'
    '<a class="gn-tag" href="/guide/" data-gn="guide">Free</a>'
    '<span><span class="gn-long"><a class="gn-title" href="/guide/" data-gn="guide">'
    "Contact Improvisation, a Beginner&rsquo;s Guide.</a> </span>"
    '<span class="gn-short">Free beginner&rsquo;s guide. </span>'
    f'<a class="gn-pdf" href="{PDF_PATH}" download data-gn="pdf">Download the PDF</a></span>'
    '<button class="gn-x" type="button" aria-label="Dismiss">'
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>'
    "</button></div>"
)

SCRIPT = r"""<script>
(function () {
  var bar = document.getElementById('mci-guide-bar');
  if (!bar) return;
  var KEY = '%(key)s';
  var DAY = 24 * 60 * 60 * 1000;
  var capture = function (name, props) { try { if (window.posthog) posthog.capture(name, props); } catch (e) {} };
  try {
    var t = parseInt(localStorage.getItem(KEY), 10);
    if (!isNaN(t) && Date.now() - t < 30 * DAY) { bar.hidden = true; return; }
  } catch (e) {}
  var root = document.documentElement;
  var setH = function () { root.style.setProperty('--gn-h', (bar.hidden ? 0 : bar.offsetHeight) + 'px'); };
  setH();
  window.addEventListener('resize', setH);
  bar.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('[data-gn]') : null;
    if (a) capture('guide_bar_click', { target: a.getAttribute('data-gn') });
  });
  bar.querySelector('.gn-x').addEventListener('click', function () {
    bar.hidden = true;
    setH();
    var main = document.getElementById('main');
    if (main) { if (!main.hasAttribute('tabindex')) main.setAttribute('tabindex', '-1'); main.focus({ preventScroll: true }); }
    try { localStorage.setItem(KEY, String(Date.now())); } catch (e) {}
    capture('guide_bar_dismiss');
  });
})();
</script>""" % {"key": DISMISS_KEY}


def bar(path, lang):
    return (MARKUP + "\n" + SCRIPT + "\n") if shows(path, lang) else ""
