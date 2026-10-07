"""The /t/<CODE> short-link page.

Cloudflare Pages does not substitute placeholders in a redirect's query string, so
`/t/:code /pricing?code=:code 302` sent people to `?code=%3Acode`. Instead `_redirects`
rewrites every /t/* to this one static page (status 200, the URL stays /t/<CODE>), and
its script reads the code from the path and sends the visitor to /pricing?code=<CODE>,
where the buy buttons pick it up. Without JavaScript the link below still works.
"""

SCRIPT = r"""(function () {
  var RE = /^CI\d{2}-?[A-Z0-9]{6}$/i;
  // The last path segment is the code; anything else (no code, junk, /t/index.html)
  // goes to the plain pricing page.
  function target(pathname) {
    var seg = String(pathname || '').replace(/\/+$/, '').split('/').pop();
    try { seg = decodeURIComponent(seg); } catch (e) { return '/pricing'; }
    if (!RE.test(seg)) return '/pricing';
    var u = seg.toUpperCase().replace('-', '');
    return '/pricing?code=' + u.slice(0, 4) + '-' + u.slice(4);
  }
  location.replace(target(location.pathname));
})();"""


def page():
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Opening tickets</title>
<meta name="description" content="Opening Miami Contact Improv tickets with your discount code applied.">
<link rel="canonical" href="https://miamicontactimprov.com/pricing">
<style>body {{ font-family: Georgia, serif; max-width: 32rem; margin: 18vh auto; padding: 0 1rem; color: #171512; background: #F3EDE1; }} a {{ color: #9C5A38; }}</style>
</head>
<body>
<p><a href="/pricing">Continue to tickets</a></p>
<script>{SCRIPT}</script>
</body>
</html>
"""
