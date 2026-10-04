"""/tickets: the Friday class ticket page (pricing + ambassador plan).

Prices (Max, 2026-10-04): online $20 to $40 sliding scale, community $15 (share
the class and prove it: the post's link, or a screenshot), first class $15 for
a new email, friend link $15 via /fr/<name>, door $30 to $50 pay what you can.

Built only from the site's existing components, the same ones /pricing,
/fundamentals and /friday-jam use: hero, .answer, .facts, .price-list rows,
.band, .prose headings, .subscribe-block forms, .cite. The Worker builds the
Stripe Checkout Session and records the offer in its metadata. See
docs/plans/pricing-ambassador-2026-10-04.md.

English only, like /pricing.
"""

import listings
import schema
from shell import CHECKOUT_ENDPOINT, COMMUNITY_VERIFY_ENDPOINT, FIRST_CLASS_ENDPOINT, _attr, answer, cite_block, facts, page

VENUE = "Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009"
SHARE_URL = "https://miamicontactimprov.com/fundamentals"


def _date_buttons():
    """One button per Fundamentals Friday. data-start lets the page drop the
    Fridays whose online sales have closed (two hours before 7 PM)."""
    out = []
    for iso, _venue, start, _end in listings.EVENT_DATES[listings.FUNDAMENTALS_NAME]:
        start_iso = listings._local_datetime(iso, start)
        label = listings.date_label(iso).replace(" 2026", "").replace("Friday ", "Fri ")
        out.append(
            f'<button type="button" class="btn secondary" data-date="{iso}" '
            f'data-start="{_attr(start_iso)}" aria-pressed="false">{label}</button>'
        )
    return f'<div class="btn-row" id="tk-dates" role="group" aria-label="Which Friday">{"".join(out)}</div>'


def tickets():
    rows = f"""
<div class="price-list">
  <div class="price-row">
    <div class="price-text"><strong>Online, sliding scale: $20 to $40.</strong><br>Pick your price on the checkout page.
      <p class="price-note">Online sales close two hours before class.</p>
    </div>
    <div class="buy-button"><button class="btn primary" type="button" data-ticket="early">Buy ticket</button><p class="buy-status" role="status" aria-live="polite"></p></div>
  </div>
  <div class="price-row">
    <div class="price-text"><strong>Community: $15.</strong><br>Share the class, then show us the post.</div>
    <a class="btn secondary" href="#share">Share for $15</a>
  </div>
  <div class="price-row">
    <div class="price-text"><strong>First class: $15.</strong><br>New here? Your first Friday is $15.</div>
    <a class="btn secondary" href="#first">Get my $15 class</a>
  </div>
  <div class="price-row">
    <div class="price-text"><strong>At the door: $30 to $50, pay what you can.</strong>
      <p class="price-note">No booking. Nobody is turned away over money.</p>
    </div>
  </div>
</div>"""

    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Tickets &middot; Fridays 7:00&ndash;9:00 PM &middot; Hallandale Beach</p>
    <h1>Book a Friday class.</h1>
    <p class="lede">Contact Improv Fundamentals at Inner Motion Dance Studio. Online is a sliding scale from $20 to $40. Share the class or come for the first time and it is $15.</p>
  </div>
</section>

<section class="section">
  <div class="wrap" id="tk" data-checkout="{CHECKOUT_ENDPOINT}" data-first="{FIRST_CLASS_ENDPOINT}" data-verify="{COMMUNITY_VERIFY_ENDPOINT}">
    {answer("A Friday class is $20 to $40 online on a sliding scale, $15 when you share it and show us the post, $15 for your first class, and $30 to $50 at the door. One price per ticket.")}

    <div class="band" id="tk-referral" hidden>
      <h2><span id="tk-ref-name">A friend</span> sent you.</h2>
      <p>Your Friday class is $15.</p>
      <div class="buy-button"><button class="btn primary" type="button" data-ticket="referral">Check out for $15</button><p class="buy-status" role="status" aria-live="polite"></p></div>
    </div>

    {facts([
      ("Which Friday", _date_buttons()),
      ("When", "7:00&ndash;9:00 PM. Class 7:00&ndash;7:45, open jam 7:45&ndash;9:00"),
      ("Where", VENUE),
    ])}

    {rows}

    <div class="prose">
      <h2 id="share">Share it, pay $15</h2>
      <p>Post the class to your feed, story or a group, then paste the link to your post here. Private post or a story? Add a screenshot instead. The link to share: <a href="{SHARE_URL}">miamicontactimprov.com/fundamentals</a>.</p>
    </div>
    <div class="subscribe-block">
      <form class="subscribe-form" id="tk-share" novalidate>
        <label class="subscribe-label" for="tk-share-url">Link to your post</label>
        <div class="subscribe-row">
          <input id="tk-share-url" name="share_url" type="url" inputmode="url" placeholder="https://instagram.com/p/..." autocomplete="off">
        </div>
        <div class="subscribe-row" id="tk-shot-row" hidden>
          <label class="subscribe-phone" for="tk-shot"><span>Screenshot of your post</span>
            <input id="tk-shot" name="screenshot" type="file" accept="image/png,image/jpeg,image/webp">
          </label>
        </div>
        <div class="subscribe-row">
          <input id="tk-share-email" name="email" type="email" autocomplete="email" placeholder="you@example.com" aria-label="Email">
          <button class="btn primary" type="submit">Check my post</button>
        </div>
        <div class="subscribe-hp" aria-hidden="true"><label for="tk-share-company">Company</label><input id="tk-share-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
        <p class="subscribe-status" role="status" aria-live="polite"></p>
      </form>
    </div>

    <div class="prose">
      <h2 id="first">New here? Your first class is $15</h2>
      <p>Leave your email and check out at $15. One first class per person.</p>
    </div>
    <div class="subscribe-block">
      <form class="subscribe-form" id="tk-first" novalidate>
        <label class="subscribe-label" for="tk-email">Your email</label>
        <div class="subscribe-row">
          <input id="tk-email" name="email" type="email" autocomplete="email" placeholder="you@example.com">
          <button class="btn primary" type="submit">Get my $15 class</button>
        </div>
        <div class="subscribe-hp" aria-hidden="true"><label for="tk-company">Company</label><input id="tk-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
        <label class="subscribe-consent" for="tk-consent"><input id="tk-consent" name="consent" type="checkbox" required><span>Email me about classes. One a month, unsubscribe any time.</span></label>
        <p class="subscribe-status" role="status" aria-live="polite"></p>
      </form>
    </div>

    <div class="prose" style="margin-top: 34px">
      <p>Every Friday runs at {VENUE}. If we cancel, we refund your ticket in full. All prices: <a href="/pricing">pricing</a>. Ideas for what we host next: <a href="/ideas">ideas</a>.</p>
    </div>
    {cite_block("Miami Contact Improv (2026). <em>Tickets</em>. miamicontactimprov.com. https://miamicontactimprov.com/tickets")}
  </div>
</section>
{TICKETS_SCRIPT}
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/tickets",
            "Tickets | Miami Contact Improv",
            "Book a Friday Contact Improv class in Hallandale Beach: $20 to $40 online, $15 when you share it or it is your first class, $30 to $50 at the door.",
        ),
        schema.breadcrumb("/tickets", "Tickets"),
    )
    return page(
        "Tickets | Miami Contact Improv Friday Class",
        "Book a Friday Contact Improv class in Hallandale Beach: $20 to $40 online, $15 when you share it or it is your first class, $30 to $50 at the door.",
        "/tickets",
        body,
        jsonld=jsonld,
    )


# Page-scoped behaviour. Every paid option goes through go(), which POSTs to the
# Worker and redirects to the Stripe URL it returns.
TICKETS_SCRIPT = r"""<script>
(function () {
  var root = document.getElementById('tk');
  if (!root) return;
  var CHECKOUT = root.getAttribute('data-checkout');
  var FIRST = root.getAttribute('data-first');
  var VERIFY = root.getAttribute('data-verify');
  var ERR = 'That did not go through. Try again, or email hello@miamicontactimprov.com.';
  var UNAVAILABLE = 'The first-class price is not available for this email. Sharing the class still gets you $15.';
  var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  // Fridays: drop the ones past their online cutoff, select the first left.
  var eventDate = '';
  var dates = Array.prototype.slice.call(root.querySelectorAll('#tk-dates [data-date]'));
  var now = Date.now();
  dates.forEach(function (b) {
    var start = Date.parse(b.getAttribute('data-start'));
    if (!isNaN(start) && now >= start - 2 * 3600 * 1000) b.remove();
  });
  function pick(b) {
    root.querySelectorAll('#tk-dates [data-date]').forEach(function (x) {
      var on = x === b;
      x.className = on ? 'btn primary' : 'btn secondary';
      x.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    eventDate = b.getAttribute('data-date');
  }
  root.querySelectorAll('#tk-dates [data-date]').forEach(function (b) { b.addEventListener('click', function () { pick(b); }); });
  var firstDate = root.querySelector('#tk-dates [data-date]');
  if (firstDate) pick(firstDate);
  else root.querySelectorAll('[data-ticket], form button').forEach(function (b) { b.disabled = true; });

  // /fr/<name> (served by a 200 rewrite) or /tickets?ref=<name>.
  var fromPath = location.pathname.match(/^\/fr\/([^\/?#]+)/);
  var ref = (fromPath ? decodeURIComponent(fromPath[1]) : (new URLSearchParams(location.search).get('ref') || '')).trim().toLowerCase();
  if (!/^[a-z0-9][a-z0-9-]{0,39}$/.test(ref)) ref = '';
  if (ref) {
    document.getElementById('tk-ref-name').textContent = ref.split('-').map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1); }).join(' ');
    document.getElementById('tk-referral').hidden = false;
  }

  function track(name, props) { try { if (window.posthog) posthog.capture(name, props); } catch (e) {} }
  function post(url, body) {
    return fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { status: r.status, data: d }; }); });
  }

  function go(btn, say, payload) {
    payload.kind = 'class';
    if (eventDate) payload.event_date = eventDate;
    track('buy_click', { kind: 'class', ticket_type: payload.ticket_type, event_date: eventDate || null });
    btn.disabled = true;
    say('Opening checkout.');
    return post(CHECKOUT, payload).then(function (res) {
      if (res.status === 200 && res.data.url) {
        track('checkout_started', { kind: 'class', ticket_type: payload.ticket_type });
        location.href = res.data.url;
        return;
      }
      btn.disabled = false;
      if (res.status === 409 && res.data.closed) return say('Online sales are closed for that Friday. Pay at the door, $30 to $50.');
      if (res.data.error === 'first_offer_unavailable') return say(UNAVAILABLE);
      if (res.status === 429) return say('Too many tries. Wait a minute and try again.');
      say(ERR);
    }).catch(function () { btn.disabled = false; say(ERR); });
  }

  function statusOf(el) { var s = el.closest('.buy-button, form').querySelector('.buy-status, .subscribe-status'); return function (t) { if (s) s.textContent = t; }; }

  root.querySelectorAll('[data-ticket="early"], [data-ticket="referral"]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var type = btn.getAttribute('data-ticket');
      go(btn, statusOf(btn), type === 'referral' ? { ticket_type: 'referral', referrer: ref } : { ticket_type: 'early' });
    });
  });

  // Community: verify the post (link, or a screenshot when the link cannot be
  // read), then straight to a $15 checkout.
  var share = document.getElementById('tk-share');
  var shotRow = document.getElementById('tk-shot-row');
  var REASONS = {
    no_match: 'We could not find Contact Improv in that post. Check the link, or add a screenshot of the post.',
    blocked: 'That post is private or needs a login, so we cannot read it. Add a screenshot of the post instead.',
    used: 'That post was already used for a $15 ticket by someone else. Share it in your own post and try again.',
    bad_url: 'That does not look like a link to a post. Paste the full link, starting with https://',
    bad_image: 'Use a PNG or JPG screenshot.',
    ocr_failed: 'We could not read that screenshot. Try a clearer one.',
    ocr_unavailable: 'Screenshot checks are not available right now. Try the link to your post.'
  };
  function readImage(file) {
    return new Promise(function (resolve, reject) {
      var img = new Image();
      img.onload = function () {
        var scale = Math.min(1, 1280 / Math.max(img.width, img.height));
        var c = document.createElement('canvas');
        c.width = Math.round(img.width * scale); c.height = Math.round(img.height * scale);
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
        resolve(c.toDataURL('image/jpeg', 0.85));
      };
      img.onerror = reject;
      img.src = URL.createObjectURL(file);
    });
  }
  share.addEventListener('submit', function (e) {
    e.preventDefault();
    var say = statusOf(share);
    var btn = share.querySelector('button[type="submit"]');
    var email = share.elements.email.value.trim().toLowerCase();
    var url = share.elements.share_url.value.trim();
    var file = share.elements.screenshot.files && share.elements.screenshot.files[0];
    if (!url && !file) { say('Paste the link to your post.'); return; }
    if (!EMAIL_RE.test(email)) { say('Enter your email.'); return; }
    btn.disabled = true;
    say(file ? 'Reading your screenshot.' : 'Checking your post.');
    var body = { email: email, company: share.elements.company.value };
    if (url) body.share_url = url;
    (file ? readImage(file) : Promise.resolve(null)).then(function (shot) {
      if (shot) body.screenshot = shot;
      return post(VERIFY, body);
    }).then(function (res) {
      if (res.status === 200 && res.data.verified) {
        track('community_verified', { method: res.data.method });
        return go(btn, say, { ticket_type: 'community', email: email, verification_id: res.data.verification_id });
      }
      btn.disabled = false;
      if (res.status === 429) return say('Too many tries. Wait a minute and try again.');
      var reason = res.data && res.data.reason;
      if (reason && reason !== 'used' && reason !== 'bad_url') shotRow.hidden = false;
      track('community_verify_failed', { reason: reason || 'error' });
      say(REASONS[reason] || (res.data && res.data.error ? res.data.error + '.' : ERR));
    }).catch(function () { btn.disabled = false; say(ERR); });
  });

  var first = document.getElementById('tk-first');
  first.addEventListener('submit', function (e) {
    e.preventDefault();
    var say = statusOf(first);
    var btn = first.querySelector('button[type="submit"]');
    var email = first.elements.email.value.trim().toLowerCase();
    if (!EMAIL_RE.test(email)) { say('Enter your email.'); return; }
    if (!first.elements.consent.checked) { say('Tick the box so we can email you.'); return; }
    btn.disabled = true;
    say('Checking.');
    post(FIRST, { email: email, consent: true, company: first.elements.company.value }).then(function (res) {
      track('first_class_captured', {});
      if (res.status === 200 && res.data.ok) return go(btn, say, { ticket_type: 'first', email: email });
      btn.disabled = false;
      say(res.status === 429 ? 'Too many tries. Wait a minute and try again.' : ERR);
    }).catch(function () { btn.disabled = false; say(ERR); });
  });
})();
</script>"""
