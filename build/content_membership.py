"""Membership pages: /membership (plans and the Black Friday offer), /membership/success
(confirms the payment with the Worker, links the Stripe portal) and /membership/manage
(the link in the welcome email: opens the Stripe Customer Portal).

English only, on the same footing as /pricing and /success. Checkout, confirmation and the
portal all run through the newsletter-api Worker; nothing here asks for a card.
"""

from shell import answer, cite_block, facts, page
import bf_bar
import plan_cards
import schema

VENUE = "Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009"


def _plan_button(plan, label):
    return (
        f'<div class="buy-button">'
        f'<button class="btn primary" type="button" id="member-{plan}" data-plan="{plan}">{label}</button>'
        f'<p class="buy-status" role="status" aria-live="polite"></p>'
        f"</div>"
    )


MEMBERSHIP_SCRIPT = r"""<script>
(function () {
  var bf = window.mciBf;
  if (!bf) return;
  var ENDPOINT = '%(endpoint)s';
  var section = document.getElementById('mci-bf');
  if (section && bf.active()) {
    section.hidden = false;
    bf.viewOnce('landing');
  }
  document.querySelectorAll('[data-plan]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var plan = btn.getAttribute('data-plan');
      var wrap = btn.closest('.buy-button');
      var status = wrap ? wrap.querySelector('.buy-status') : null;
      var say = function (t) { if (status) status.textContent = t; };
      var setLoading = function (on) {
        btn.classList.toggle('is-loading', on);
        if (on) btn.setAttribute('aria-busy', 'true'); else btn.removeAttribute('aria-busy');
      };
      var props = { plan: plan, bf: bf.active() };
      bf.capture('membership_checkout_click', props);
      var payload = { plan: plan };
      var u = bf.utm();
      for (var k in u) payload[k] = u[k];
      btn.disabled = true;
      say('');
      setLoading(true);
      fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok, data: d }; }); })
        .then(function (res) {
          if (res.ok && res.data && res.data.url) {
            bf.capture('membership_checkout_started', props);
            setTimeout(function () { window.location.href = res.data.url; }, 150);
            return;
          }
          setLoading(false);
          say('Checkout is not available right now. Please try again in a minute.');
          btn.disabled = false;
        })
        .catch(function () {
          setLoading(false);
          say('Checkout is not available right now. Please try again in a minute.');
          btn.disabled = false;
        });
    });
  });
  window.addEventListener('pageshow', function (e) {
    if (!e.persisted) return;
    document.querySelectorAll('[data-plan]').forEach(function (b) {
      b.classList.remove('is-loading'); b.removeAttribute('aria-busy'); b.disabled = false;
    });
  });
})();
</script>""" % {"endpoint": bf_bar.CHECKOUT_ENDPOINT}


def membership():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Membership</p>
    <h1>Come every Friday.</h1>
    <p class="lede">Two ways to make the Friday class a habit. Both check out through a Stripe-hosted page, and you can cancel any time from a link in your confirmation email.</p>
  </div>
</section>

<section class="section" id="mci-bf" hidden>
  <div class="wrap">
    <div class="bf-offer">
      <h2>Black Friday: bring a friend free</h2>
      <p>Join between Friday, November 27 and Tuesday, December 1 and your membership comes with a free bring-a-friend pass every month for your first three months. The prices stay the same.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {plan_cards.grid(plan_cards.monthly(_plan_button("monthly", "Join monthly")), plan_cards.yearly(_plan_button("yearly", "Join yearly")))}
    {answer("Memberships cover the Friday class, not jams or workshops. Monthly gives 4 classes each billing month; unused classes don't carry over. If we cancel a class, the credit goes back to your balance.", label="What it covers")}
    {facts([
      ("Where", VENUE),
      ("When", "Fridays, 7:00&ndash;9:00 PM"),
      ("Single class", '$20 online, <a href="/pricing">see pricing</a>'),
      ("Refunds and problems", '<a href="mailto:hello@miamicontactimprov.com">hello@miamicontactimprov.com</a>'),
    ])}
    {cite_block("Miami Contact Improv (2026). <em>Membership</em>. miamicontactimprov.com. https://miamicontactimprov.com/membership")}
  </div>
</section>
{bf_bar.COMMON}
{MEMBERSHIP_SCRIPT}
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/membership",
            "Membership | Miami Contact Improv",
            "Monthly ($40, 4 classes) and yearly ($260, a class every week) memberships for the Friday Contact Improv class in Hallandale Beach.",
        ),
        schema.breadcrumb("/membership", "Membership"),
    )
    return page(
        "Membership | Miami Contact Improv Friday Class",
        "Join the Friday Contact Improv class: $40 a month for 4 classes or $260 a year for a class every week.",
        "/membership",
        body,
        jsonld=jsonld,
    )


SUCCESS_SCRIPT = r"""<script>
(function () {
  var bf = window.mciBf;
  var q = new URLSearchParams(window.location.search);
  var sid = q.get('session_id');
  var plan = q.get('plan') === 'yearly' ? 'yearly' : 'monthly';
  // Take the session id out of the address bar before PostHog can read it for $current_url.
  if (sid) {
    try {
      q.delete('session_id');
      var qs = q.toString();
      window.history.replaceState(window.history.state, '', window.location.pathname + (qs ? '?' + qs : '') + window.location.hash);
    } catch (e) {}
  }
  if (!sid || !/^cs_(test|live)_[A-Za-z0-9]+$/.test(sid) || !window.fetch) return;
  function confirmMember(attempt) {
    fetch('%(endpoint)s?session_id=' + encodeURIComponent(sid))
      .then(function (r) {
        if (r.status === 502 && attempt < 3) { setTimeout(function () { confirmMember(attempt + 1); }, 1000 * Math.pow(2, attempt)); return null; }
        return r.ok ? r.json() : null;
      })
      .then(function (m) {
        if (!m || !m.paid) return;
        // The webhook has not written the member yet, so the stored Black Friday decision is not
        // readable: wait and ask again rather than count the purchase with a guess.
        if (m.pending && attempt < 4) { setTimeout(function () { confirmMember(attempt + 1); }, 1500 * (attempt + 1)); return; }
        var key = 'mci_membership_completed_' + sid;
        var seen = false;
        try { seen = !!localStorage.getItem(key); } catch (e) {}
        if (!seen && bf) {
          // Marked seen only after capture ran, so a blocked PostHog does not burn the one count.
          try {
            if (window.posthog) {
              bf.capture('membership_checkout_completed', { plan: m.plan || plan, bf: !!m.bf });
              try { localStorage.setItem(key, '1'); } catch (e) {}
            }
          } catch (e) {}
        }
        // Keep the member token on this phone so scanning the studio QR checks in. The token is
        // the id in the manage link; the address bar never shows it.
        try {
          var tok = (String(m.manage_url || '').match(/[?&]m=([0-9a-f]{32})/) || [])[1];
          if (tok) {
            localStorage.setItem('mci_member', tok);
            var ready = document.getElementById('mci-checkin-ready');
            if (ready) ready.hidden = false;
          }
        } catch (e) {}
        var link = document.getElementById('mci-manage-link');
        if (link && m.manage_url) { link.href = m.manage_url; document.getElementById('mci-manage').hidden = false; }
        var passes = document.getElementById('mci-bf-passes');
        if (passes && m.bf) passes.hidden = false;
      })
      .catch(function () {});
  }
  confirmMember(0);
})();
</script>""" % {"endpoint": bf_bar.SESSION_ENDPOINT}


def membership_success():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Welcome</p>
    <h1>You're a member.</h1>
    <p class="lede">A confirmation is on its way to your inbox. Come to the door with your name on Friday.</p>
    <p id="mci-bf-passes" hidden>Your membership includes three bring-a-friend passes, one a month for your first three months. Reply to the confirmation email the week you want to use one.</p>
    <p id="mci-checkin-ready" hidden>This phone is set up for check-in. On Fridays, scan the QR at the studio.</p>
    <p id="mci-manage" hidden><a class="btn secondary" id="mci-manage-link" href="#">Manage your membership</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {facts([
      ("Where", VENUE),
      ("When", "Fridays, 7:00&ndash;9:00 PM"),
    ])}
    <div class="prose">
      <p>First time? <a href="/your-first-jam">Your first jam, step by step</a> walks through arriving and the opening circle. Refunds and problems: <a href="mailto:hello@miamicontactimprov.com">hello@miamicontactimprov.com</a>.</p>
    </div>
  </div>
</section>
{bf_bar.COMMON}
{SUCCESS_SCRIPT}
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/membership/success",
            "Welcome | Miami Contact Improv",
            "Membership confirmation for Miami Contact Improv.",
        ),
    )
    return page(
        "Welcome, Member | Miami Contact Improv",
        "Membership confirmation for Miami Contact Improv: where and when the Friday class runs.",
        "/membership/success",
        body,
        jsonld=jsonld,
    )


# The member id in the emailed link is a bearer secret. This runs in <head>, before the
# PostHog snippet, so analytics never reads it from the address bar: it is moved into a
# window variable and the URL is rewritten to the bare path.
MANAGE_HEAD = r"""<script>
(function () {
  try {
    var m = new URLSearchParams(window.location.search).get('m') || '';
    window.__mciManageId = m;
    window.history.replaceState(window.history.state, '', window.location.pathname + window.location.hash);
  } catch (e) {}
})();
</script>"""

MANAGE_SCRIPT = r"""<script>
(function () {
  var id = window.__mciManageId || '';
  var msg = document.getElementById('mci-manage-msg');
  var fail = function () { if (msg) msg.textContent = 'This link did not work. Reply to your confirmation email and we will sort it out.'; };
  if (!/^[0-9a-f]{32}$/.test(id) || !window.fetch) { fail(); return; }
  fetch('%(endpoint)s', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ member_id: id }) })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (d) { if (d && d.url) window.location.replace(d.url); else fail(); })
    .catch(fail);
})();
</script>""" % {"endpoint": bf_bar.PORTAL_ENDPOINT}


def membership_manage():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Membership</p>
    <h1>Opening your membership.</h1>
    <p class="lede" id="mci-manage-msg">One moment.</p>
  </div>
</section>
{MANAGE_SCRIPT}
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/membership/manage",
            "Manage Membership | Miami Contact Improv",
            "Opens the Stripe billing portal for a Miami Contact Improv membership.",
        ),
    )
    return page(
        "Manage Membership | Miami Contact Improv",
        "Opens the Stripe billing portal for a Miami Contact Improv membership.",
        "/membership/manage",
        body,
        jsonld=jsonld,
        extra_head=MANAGE_HEAD,
    )
