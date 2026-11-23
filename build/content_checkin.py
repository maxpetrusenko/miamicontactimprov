"""/checkin: the page the printed studio QR opens, and the page a single-class ticket QR opens
(/checkin/<ticketId>, rewritten to this page).

Member flow: the phone holds a member token (localStorage, set on /membership/success, by the
emailed "add to phone" link, or by the one-time link a member requests here). Opening the page
checks the member in for tonight's class. No token: enter the email, get one link by email.
Ticket flow: /checkin/<ticketId> shows valid or used and marks it used during class.
The Worker (newsletter-api, src/checkin.ts) decides everything; this page only shows the result.
Refunds and problems go to the support address, never to an automated refund.
"""

from shell import page
import schema

SUPPORT_EMAIL = "hello@miamicontactimprov.com"
API = "https://newsletter-api.max-petrusenko.workers.dev/api/checkin"

# Runs in <head>, before the PostHog loader: the member token (?m=) and the ticket id
# (/checkin/<id>) are bearer secrets, so they are read into a window variable and the address
# bar is rewritten to the bare /checkin before analytics can record the URL.
HEAD_SCRIPT = r"""<script>
(function () {
  var HEX = /^[0-9a-f]{32}$/;
  var state = { m: '', t: '' };
  try {
    var m = new URLSearchParams(window.location.search).get('m') || '';
    var seg = window.location.pathname.replace(/\/+$/, '').split('/');
    var t = seg.length > 2 ? seg[seg.length - 1] : '';
    if (HEX.test(m)) {
      state.m = m;
      try { localStorage.setItem('mci_member', m); } catch (e) {}
    }
    if (HEX.test(t)) {
      state.t = t;
      try { sessionStorage.setItem('mci_ticket', t); } catch (e) {}
    }
    window.history.replaceState(window.history.state, '', '/checkin');
  } catch (e) {}
  try { if (!state.t) { var kept = sessionStorage.getItem('mci_ticket') || ''; if (HEX.test(kept)) state.t = kept; } } catch (e) {}
  window.__mciCk = state;
})();
</script>"""

SCRIPT = r"""<script>
(function () {
  var API = '%(api)s';
  var SUPPORT = '%(support)s';
  var HEX = /^[0-9a-f]{32}$/;
  var st = window.__mciCk || { m: '', t: '' };
  var panels = ['loading', 'ok', 'already', 'denied', 'email', 'sent', 'ticket-ok', 'ticket-used', 'ticket-denied'];
  function show(name) {
    panels.forEach(function (p) { var el = document.getElementById('ck-' + p); if (el) el.hidden = p !== name; });
  }
  function text(id, value) { var el = document.getElementById(id); if (el) el.textContent = value; }
  function post(path, payload) {
    return fetch(API + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { status: r.status, data: d }; }); });
  }
  var MESSAGES = {
    outside_window: 'Check-in is open on class Fridays from 6:30 to 9:00 PM.',
    inactive: 'Your membership is not active right now.',
    expired: 'Your yearly membership has ended.',
    no_credits: 'You have no class credits left. A single class is $20.',
    week_used: 'You already used this week’s class.',
    wrong_date: 'This ticket is for a different class date.',
    unknown_ticket: 'We could not find this ticket.',
    unknown_member: 'We could not find your membership on this phone.'
  };
  function deny(panel, code) {
    var msg = MESSAGES[code] || 'Something went wrong.';
    text(panel === 'ticket-denied' ? 'ck-ticket-denied-msg' : 'ck-denied-msg', msg);
    show(panel);
  }
  function fail(panel) { text(panel === 'ticket-denied' ? 'ck-ticket-denied-msg' : 'ck-denied-msg', 'Check-in is not available right now. Try again in a minute.'); show(panel); }
  function when(iso) {
    try { return new Date(iso).toLocaleString('en-US', { timeZone: 'America/New_York', weekday: 'long', hour: 'numeric', minute: '2-digit' }); } catch (e) { return ''; }
  }

  function ticketFlow(id) {
    show('loading');
    post('/ticket', { ticket_id: id }).then(function (res) {
      var d = res.data || {};
      if (res.status === 200 && d.ok) {
        if (d.already) { text('ck-ticket-used-line', 'This ticket was already used' + (d.checked_in_at ? ' on ' + when(d.checked_in_at) : '') + '.'); show('ticket-used'); return; }
        text('ck-ticket-ok-line', d.name ? 'Welcome, ' + d.name + '.' : 'Welcome.');
        show('ticket-ok');
        return;
      }
      if (res.status === 404 || res.status === 400 || res.status === 409) { deny('ticket-denied', d.error); return; }
      fail('ticket-denied');
    }).catch(function () { fail('ticket-denied'); });
  }

  function memberFlow(token) {
    show('loading');
    post('/member', { member_id: token }).then(function (res) {
      var d = res.data || {};
      if (res.status === 200 && d.ok) {
        var who = d.name ? ', ' + d.name : '';
        var left = d.plan === 'monthly' && typeof d.credits_remaining === 'number'
          ? d.credits_remaining + (d.credits_remaining === 1 ? ' class credit' : ' class credits') + ' left.'
          : 'Yearly membership.';
        if (d.already) { text('ck-already-line', 'See you in class' + who + '. ' + left); show('already'); return; }
        text('ck-ok-line', 'See you in class' + who + '. ' + left);
        show('ok');
        return;
      }
      if (d.error === 'unknown_member') {
        // The token on this phone is not a member any more: forget it and ask for the email.
        try { localStorage.removeItem('mci_member'); } catch (e) {}
        show('email');
        return;
      }
      if (res.status === 409 || res.status === 400) { deny('denied', d.error); return; }
      fail('denied');
    }).catch(function () { fail('denied'); });
  }

  var form = document.getElementById('ck-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = document.getElementById('ck-email-input');
      var btn = document.getElementById('ck-send');
      var status = document.getElementById('ck-email-status');
      var email = input ? input.value.trim() : '';
      if (!email) return;
      btn.disabled = true;
      if (status) status.textContent = '';
      post('/link', { email: email }).then(function (res) {
        if (res.status === 200 && res.data && res.data.ok) { show('sent'); return; }
        if (status) status.textContent = res.status === 429 ? 'Too many tries. Wait a minute and try again.' : 'That does not look like an email address.';
        btn.disabled = false;
      }).catch(function () {
        if (status) status.textContent = 'Could not send right now. Try again in a minute.';
        btn.disabled = false;
      });
    });
  }

  var token = st.m;
  if (!token) { try { token = localStorage.getItem('mci_member') || ''; } catch (e) {} }
  if (HEX.test(st.t || '')) ticketFlow(st.t);
  else if (HEX.test(token || '')) memberFlow(token);
  else show('email');
})();
</script>""" % {"api": API, "support": SUPPORT_EMAIL}


def _support_line():
    return (
        f'<p>Refunds and problems: <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>'
    )


def checkin():
    body = f"""
<section class="hero">
  <div class="wrap">
    <h1>Check-in</h1>
    <div id="ck-loading"><h2>Checking you in.</h2></div>

    <div id="ck-ok" hidden>
      <h2>You&rsquo;re checked in.</h2>
      <p class="lede" id="ck-ok-line"></p>
    </div>
    <div id="ck-already" hidden>
      <h2>Already checked in.</h2>
      <p class="lede" id="ck-already-line"></p>
    </div>
    <div id="ck-denied" hidden>
      <h2>We couldn&rsquo;t check you in.</h2>
      <p class="lede" id="ck-denied-msg"></p>
      {_support_line()}
    </div>

    <div id="ck-email" hidden>
      <h2>Check in to class.</h2>
      <p class="lede">Enter the email you joined with and we will send a link for this phone.</p>
      <form id="ck-form" class="ck-form" novalidate>
        <label for="ck-email-input">Email</label>
        <input id="ck-email-input" type="email" name="email" autocomplete="email" inputmode="email" required>
        <button class="btn primary" id="ck-send" type="submit">Email me a link</button>
        <p class="buy-status" id="ck-email-status" role="status" aria-live="polite"></p>
      </form>
    </div>
    <div id="ck-sent" hidden>
      <h2>Check your email.</h2>
      <p class="lede">If that address has a membership, a link is on its way. Open it on this phone, then scan the studio QR again.</p>
      {_support_line()}
    </div>

    <div id="ck-ticket-ok" hidden>
      <h2>Ticket valid.</h2>
      <p class="lede" id="ck-ticket-ok-line"></p>
    </div>
    <div id="ck-ticket-used" hidden>
      <h2>Ticket already used.</h2>
      <p class="lede" id="ck-ticket-used-line"></p>
      {_support_line()}
    </div>
    <div id="ck-ticket-denied" hidden>
      <h2>We couldn&rsquo;t check this ticket.</h2>
      <p class="lede" id="ck-ticket-denied-msg"></p>
      {_support_line()}
    </div>
  </div>
</section>
{SCRIPT}
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/checkin",
            "Check-in | Miami Contact Improv",
            "Studio check-in for Miami Contact Improv members and ticket holders.",
        ),
    )
    return page(
        "Check-in | Miami Contact Improv",
        "Studio check-in for Miami Contact Improv members and ticket holders.",
        "/checkin",
        body,
        jsonld=jsonld,
        extra_head=HEAD_SCRIPT,
    )
