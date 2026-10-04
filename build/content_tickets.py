"""/tickets: the Friday class ticket page (pricing + ambassador slice 1).

Early $20, Community $15 (share and unlock), first class $15 for a new email,
friend-link $15 via /fr/<name>, and the door price as information. Every paid
option checks out through the Worker's POST /api/checkout, which builds a
Stripe Checkout Session and records the offer in its metadata (ticket_type,
share_channel, handle, event, referrer). See
docs/plans/pricing-ambassador-2026-10-04.md.

English only, like /pricing: a page about this site's own commercial mechanics.
"""

import listings
import schema
from shell import CHECKOUT_ENDPOINT, FIRST_CLASS_ENDPOINT, _attr, answer, page

VENUE = "Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009"

SHARE_CHANNELS = [
    ("instagram_story", "Instagram story"),
    ("whatsapp_group", "WhatsApp group"),
    ("facebook_group", "Facebook group"),
    ("other", "Somewhere else"),
]

SHARE_URL = "https://miamicontactimprov.com/fundamentals"


def _date_options():
    """One <option> per Fundamentals Friday. data-start lets the page drop the
    Fridays whose online sales have closed (two hours before 7 PM)."""
    rows = listings.EVENT_DATES[listings.FUNDAMENTALS_NAME]
    out = []
    for iso, _venue, start, _end in rows:
        start_iso = listings._local_datetime(iso, start)
        out.append(
            f'<option value="{iso}" data-start="{_attr(start_iso)}">'
            f"{listings.date_label(iso)}</option>"
        )
    return "\n".join(out)


def _channel_options():
    return "".join(f'<option value="{v}">{label}</option>' for v, label in SHARE_CHANNELS)


def tickets():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Tickets</p>
    <h1>Book your Friday class.</h1>
    <p class="lede">Contact Improv Fundamentals, Fridays 7 to 9 PM at Inner Motion, Hallandale Beach. Pick a Friday, then pick your price.</p>
  </div>
</section>

<section class="section">
  <div class="wrap" id="tk" data-checkout="{CHECKOUT_ENDPOINT}" data-first="{FIRST_CLASS_ENDPOINT}">
    {answer("A Friday class is $20 online, $15 when you share it, $15 for your first class, and $30 at the door. One price per ticket: the $15 prices do not combine with each other or with a code.")}

    <div class="tk-date">
      <label for="tk-date">Which Friday</label>
      <select id="tk-date" name="event_date">
{_date_options()}
      </select>
    </div>

    <div class="tk-referral" id="tk-referral" hidden>
      <p class="tk-kicker">Friend link</p>
      <h2><span id="tk-ref-name">A friend</span> sent you. Your class is $15.</h2>
      <div class="buy-button">
        <button class="btn primary" type="button" data-ticket="referral">Check out for $15</button>
        <p class="buy-status" role="status" aria-live="polite"></p>
      </div>
    </div>

    <div class="tk-grid">
      <article class="tk-card">
        <p class="tk-kicker">Early</p>
        <p class="tk-price">$20</p>
        <p>Buy online before Friday. Codes from our emails work here.</p>
        <div class="buy-button">
          <button class="btn primary" type="button" data-ticket="early">Buy for $20</button>
          <p class="buy-status" role="status" aria-live="polite"></p>
        </div>
      </article>

      <article class="tk-card tk-card-accent">
        <p class="tk-kicker">Community</p>
        <p class="tk-price">$15</p>
        <p>Share the class, tell us where, pay $15. We take your word for it.</p>
        <form class="tk-share" novalidate>
          <label for="tk-channel">Where you shared it</label>
          <select id="tk-channel" name="share_channel" required>
            <option value="">Choose one</option>
            {_channel_options()}
          </select>
          <label for="tk-handle">Your handle or the group name</label>
          <input id="tk-handle" name="handle" type="text" maxlength="80" autocomplete="off" required placeholder="@yourname or group name">
          <div class="buy-button">
            <button class="btn primary" type="submit" data-ticket="community">Unlock $15</button>
            <p class="buy-status" role="status" aria-live="polite"></p>
          </div>
        </form>
        <p class="tk-share-link">Link to share: <a href="{SHARE_URL}">{SHARE_URL.replace("https://", "")}</a></p>
      </article>

      <article class="tk-card tk-card-quiet">
        <p class="tk-kicker">At the door</p>
        <p class="tk-price">$30</p>
        <p>Walk in and pay on the night. Online sales close two hours before class.</p>
      </article>
    </div>

    <div class="tk-new" id="tk-new">
      <div class="tk-new-copy">
        <p class="tk-kicker">New here?</p>
        <h2>Your first class is $15.</h2>
        <p>Leave your email and check out at $15. One first class per person.</p>
      </div>
      <form class="tk-first" novalidate>
        <label for="tk-email">Email</label>
        <input id="tk-email" name="email" type="email" autocomplete="email" required placeholder="you@example.com">
        <label class="tk-consent"><input type="checkbox" name="consent" required> Email me about classes. One a month, unsubscribe any time.</label>
        <div class="subscribe-hp" aria-hidden="true"><label for="tk-company">Company</label><input id="tk-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
        <div class="buy-button">
          <button class="btn primary" type="submit" data-ticket="first">Get my $15 class</button>
          <p class="buy-status" role="status" aria-live="polite"></p>
        </div>
      </form>
    </div>

    <div class="prose">
      <p>Class runs 7:00 to 7:45, then an open jam until 9:00, at {VENUE}. If we cancel, we refund your ticket in full. All prices: <a href="/pricing">pricing</a>.</p>
    </div>
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
            "Book a Friday Contact Improv class in Hallandale Beach: $20 early, $15 community or first class, $30 at the door.",
        ),
        schema.breadcrumb("/tickets", "Tickets"),
    )
    return page(
        "Tickets | Miami Contact Improv Friday Class",
        "Book a Friday Contact Improv class in Hallandale Beach: $20 early, $15 when you share it or it is your first class, $30 at the door.",
        "/tickets",
        body,
        jsonld=jsonld,
    )


# Page-scoped behaviour. Lives here rather than in shell.body_script() because no
# other page has these controls. Every paid option goes through one function,
# go(), which POSTs to the Worker and redirects to the Stripe URL it returns.
TICKETS_SCRIPT = r"""<script>
(function () {
  var root = document.getElementById('tk');
  if (!root) return;
  var CHECKOUT = root.getAttribute('data-checkout');
  var FIRST = root.getAttribute('data-first');
  var ERR = 'That did not go through. Try again, or email hello@miamicontactimprov.com.';
  // One message for every first-class refusal: the Worker never says why.
  var UNAVAILABLE = 'The first-class price is not available for this email. The community price still works.';
  var dateSel = document.getElementById('tk-date');

  // Drop Fridays whose online sale has closed (two hours before start).
  var now = Date.now();
  Array.prototype.slice.call(dateSel.options).forEach(function (opt) {
    var start = Date.parse(opt.getAttribute('data-start'));
    if (!isNaN(start) && now >= start - 2 * 3600 * 1000) opt.remove();
  });
  if (!dateSel.options.length) {
    dateSel.disabled = true;
    root.querySelectorAll('[data-ticket]').forEach(function (b) { b.disabled = true; });
  }

  // /fr/<name> lands here as ?ref=<name>. Same rule the Worker applies.
  // /fr/<name> (served by a 200 rewrite) or /tickets?ref=<name>.
  var fromPath = location.pathname.match(/^\/fr\/([^\/?#]+)/);
  var ref = (fromPath ? decodeURIComponent(fromPath[1]) : (new URLSearchParams(location.search).get('ref') || '')).trim().toLowerCase();
  if (!/^[a-z0-9][a-z0-9-]{0,39}$/.test(ref)) ref = '';
  if (ref) {
    var panel = document.getElementById('tk-referral');
    var nice = ref.split('-').map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1); }).join(' ');
    document.getElementById('tk-ref-name').textContent = nice;
    panel.hidden = false;
  }

  function track(name, props) { try { if (window.posthog) posthog.capture(name, props); } catch (e) {} }

  function statusFor(btn) {
    var wrap = btn.closest('.buy-button');
    return wrap ? wrap.querySelector('.buy-status') : null;
  }

  function go(btn, payload) {
    var status = statusFor(btn);
    var say = function (t) { if (status) status.textContent = t; };
    payload.kind = 'class';
    if (dateSel.value) payload.event_date = dateSel.value;
    track('buy_click', { kind: 'class', ticket_type: payload.ticket_type, event_date: payload.event_date || null });
    btn.disabled = true;
    say('Opening checkout.');
    return fetch(CHECKOUT, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (d) { return { status: r.status, data: d }; });
    }).then(function (res) {
      if (res.status === 200 && res.data.url) {
        track('checkout_started', { kind: 'class', ticket_type: payload.ticket_type });
        location.href = res.data.url;
        return;
      }
      if (res.status === 409 && res.data.closed) { say('Online sales are closed for that Friday. Pay at the door ($30).'); return; }
      if (res.data.error === 'first_offer_unavailable') { say(UNAVAILABLE); return; }
      if (res.status === 429) { say('Too many tries. Wait a minute and try again.'); btn.disabled = false; return; }
      say(res.status === 400 && res.data.error ? res.data.error + '.' : ERR);
      btn.disabled = false;
    }).catch(function () { say(ERR); btn.disabled = false; });
  }

  root.querySelector('[data-ticket="early"]').addEventListener('click', function (e) {
    go(e.currentTarget, { ticket_type: 'early' });
  });

  var refBtn = root.querySelector('[data-ticket="referral"]');
  refBtn.addEventListener('click', function (e) {
    go(e.currentTarget, { ticket_type: 'referral', referrer: ref });
  });

  var share = root.querySelector('.tk-share');
  share.addEventListener('submit', function (e) {
    e.preventDefault();
    var btn = share.querySelector('[data-ticket="community"]');
    var channel = share.elements.share_channel.value;
    var handle = share.elements.handle.value.trim();
    var status = statusFor(btn);
    if (!channel) { status.textContent = 'Pick where you shared it.'; share.elements.share_channel.focus(); return; }
    if (!handle) { status.textContent = 'Add your handle or the group name.'; share.elements.handle.focus(); return; }
    go(btn, { ticket_type: 'community', share_channel: channel, handle: handle });
  });

  var first = root.querySelector('.tk-first');
  first.addEventListener('submit', function (e) {
    e.preventDefault();
    var btn = first.querySelector('[data-ticket="first"]');
    var status = statusFor(btn);
    var email = first.elements.email.value.trim().toLowerCase();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { status.textContent = 'Enter your email.'; first.elements.email.focus(); return; }
    if (!first.elements.consent.checked) { status.textContent = 'Tick the box so we can email you.'; return; }
    btn.disabled = true;
    status.textContent = 'Checking.';
    fetch(FIRST, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, consent: true, company: first.elements.company.value })
    }).then(function (r) { return r.json().then(function (d) { return { status: r.status, data: d }; }); })
      .then(function (res) {
        track('first_class_captured', {});
        if (res.status === 200 && res.data.ok) { return go(btn, { ticket_type: 'first', email: email }); }
        status.textContent = res.status === 429 ? 'Too many tries. Wait a minute and try again.' : ERR;
        btn.disabled = false;
      }).catch(function () { status.textContent = ERR; btn.disabled = false; });
  });
})();
</script>"""
