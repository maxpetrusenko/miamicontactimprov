"""/ideas: what should we host next (pricing + ambassador plan, slice 3).

Each idea is a card with a public "N interested" counter and the number that
gets it scheduled. One click (email once, then remembered on this device), a
"Definitely / Probably / Just curious" follow-up, then "N more needed" with a
share link carrying the person's ?ref= code. Storage and counts live in the
Worker (src/ideas.ts in the newsletter-api repo); suggestions wait for Max's
approval before they appear. See docs/plans/pricing-ambassador-2026-10-04.md.

English only, like /tickets.
"""

import schema
from shell import IDEAS_ENDPOINT, _attr, page

# id, title, line, threshold, families. ids and thresholds must match IDEAS in
# the Worker's src/ideas.ts; tests/test_ideas.py pins them.
IDEAS = [
    ("ci-acro", "CI + Acro",
     "Contact meets partner acrobatics: basing, flying and spotting, then a jam that puts it to use.", 20, False),
    ("eros-contact", "Eros Contact",
     "Adults only. Slow, sensual contact inside clear agreements: opt-in partner work, a facilitator holding consent the whole time, and no as a full answer.", 20, False),
    ("tantra-bodywork-lab", "Tantra and Bodywork Lab",
     "Breath, touch and attention practices from bodywork and tantra traditions. Consent first, clothes on.", 20, False),
    ("parents-kids", "Parents CI + Kids Hangout",
     "You dance for two hours while the kids hang out next door with a nanny and pizza. Parents chip in for the care.", 10, True),
    ("ci-live-music", "CI + Live Music",
     "Musicians in the room following the dancers, and dancers following the music.", 20, False),
    ("outdoor-beach", "Outdoor and Beach CI",
     "Sand, grass and open sky. A morning jam on the beach or in a park.", 20, False),
    ("extended-jam", "Extended Jam",
     "Three to four hours of open floor, long enough for the slow dances to arrive.", 15, False),
]

LEVELS = [("definitely", "Definitely"), ("probably", "Probably"), ("curious", "Just curious")]


def _number_select(name, uid, label, lo, hi, default):
    opts = "".join(
        f'<option value="{n}"{" selected" if n == default else ""}>{n}</option>' for n in range(lo, hi + 1)
    )
    return (
        f'<label class="idea-num" for="{uid}-{name}">{label}'
        f'<select id="{uid}-{name}" name="{name}">{opts}</select></label>'
    )


def _card(idea_id, title, line, threshold, families):
    uid = f"idea-{idea_id}"
    count_line = (
        f'<span class="idea-n">0</span>/{threshold} families, <span class="idea-kids">0</span> kids'
        if families
        else f'<span class="idea-n">0</span> interested. At {threshold} we schedule it.'
    )
    family_fields = (
        f'<div class="idea-family">{_number_select("adults", uid, "Adults", 1, 4, 1)}'
        f'{_number_select("kids", uid, "Kids", 0, 6, 1)}</div>'
        if families
        else ""
    )
    levels = "".join(f'<button type="button" class="btn secondary" data-level="{v}">{label}</button>' for v, label in LEVELS)
    return f"""
<article class="idea-card" id="{idea_id}" data-idea="{idea_id}" data-threshold="{threshold}">
  <h3>{title}</h3>
  <p>{line}</p>
  <p class="idea-count" aria-live="polite">{count_line}</p>
  <div class="idea-bar" aria-hidden="true"><span style="width:0%"></span></div>
  <button class="btn primary idea-go" type="button">Count me in</button>
  <form class="idea-form" hidden novalidate>
    <label for="{uid}-email">Email</label>
    <input id="{uid}-email" name="email" type="email" autocomplete="email" required placeholder="you@example.com">
    {family_fields}
    <label class="tk-consent"><input type="checkbox" name="consent" required> Email me when it is scheduled.</label>
    <div class="subscribe-hp" aria-hidden="true"><label for="{uid}-company">Company</label><input id="{uid}-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
    <button class="btn primary" type="submit">Count me in</button>
  </form>
  <div class="idea-level" hidden>
    <p class="idea-q">At $20 to $30, would you come?</p>
    <div class="btn-row">{levels}</div>
  </div>
  <div class="idea-share" hidden>
    <p class="idea-more"></p>
    <div class="btn-row"><button type="button" class="btn secondary idea-copy">Copy share link</button></div>
  </div>
  <p class="buy-status" role="status" aria-live="polite"></p>
</article>"""


def ideas():
    cards = "".join(_card(*row) for row in IDEAS)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Ideas</p>
    <h1>What should we host next?</h1>
    <p class="lede">Each idea runs once enough people say they would come. Add yourself, tell us how sure you are, and share it with the people who should be there.</p>
  </div>
</section>

<section class="section">
  <div class="wrap" id="ideas" data-endpoint="{_attr(IDEAS_ENDPOINT)}">
    <div class="idea-grid">
      {cards}
      <article class="idea-card idea-suggest" id="suggest">
        <h3>Suggest something</h3>
        <p>Something missing? Tell us. We read every suggestion before it goes on the board.</p>
        <form class="idea-suggest-form" novalidate>
          <label for="sg-title">Idea</label>
          <input id="sg-title" name="title" type="text" maxlength="80" required placeholder="Contact + yoga on Sunday mornings">
          <label for="sg-detail">Anything else</label>
          <textarea id="sg-detail" name="detail" maxlength="500" rows="3"></textarea>
          <label for="sg-email">Email</label>
          <input id="sg-email" name="email" type="email" autocomplete="email" required placeholder="you@example.com">
          <div class="subscribe-hp" aria-hidden="true"><label for="sg-company">Company</label><input id="sg-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
          <button class="btn primary" type="submit">Send it</button>
        </form>
        <p class="buy-status" role="status" aria-live="polite"></p>
      </article>
    </div>
  </div>
</section>
{IDEAS_SCRIPT}
"""
    jsonld = schema.render(
        schema.organisation(),
        schema.website(),
        schema.webpage(
            "/ideas",
            "Ideas | Miami Contact Improv",
            "Vote on what Contact Improv Miami hosts next: acro, live music, beach jams, a parents class with kids care, and more.",
        ),
        schema.breadcrumb("/ideas", "Ideas"),
    )
    return page(
        "Ideas | What Miami Contact Improv Hosts Next",
        "Vote on what Contact Improv Miami hosts next: CI + acro, live music, beach jams, a parents class with kids care, an extended jam.",
        "/ideas",
        body,
        jsonld=jsonld,
    )


IDEAS_SCRIPT = r"""<script>
(function () {
  var root = document.getElementById('ideas');
  if (!root) return;
  var API = root.getAttribute('data-endpoint');
  var ERR = 'That did not go through. Try again in a minute.';
  var KEY = 'mci_idea_email';
  var q = new URLSearchParams(location.search);
  var ref = (q.get('ref') || '').trim().toLowerCase();
  if (!/^[a-z0-9][a-z0-9-]{0,39}$/.test(ref)) ref = '';

  function remembered() { try { return localStorage.getItem(KEY) || ''; } catch (e) { return ''; } }
  function remember(email) { try { localStorage.setItem(KEY, email); } catch (e) {} }
  function track(name, props) { try { if (window.posthog) posthog.capture(name, props); } catch (e) {} }
  function post(path, body) {
    return fetch(API + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { status: r.status, data: d }; }); });
  }

  function paint(card, idea) {
    if (!idea) return;
    var n = card.querySelector('.idea-n'); if (n) n.textContent = idea.count;
    var k = card.querySelector('.idea-kids'); if (k && typeof idea.kids === 'number') k.textContent = idea.kids;
    var bar = card.querySelector('.idea-bar span');
    if (bar) bar.style.width = Math.min(100, Math.round(100 * idea.count / idea.threshold)) + '%';
  }

  function moreLine(idea, families) {
    if (!idea.needed) return 'That is enough. We are scheduling it, and you hear first.';
    var unit = families ? (idea.needed === 1 ? 'family' : 'families') : (idea.needed === 1 ? 'person' : 'people');
    return idea.needed + ' more ' + unit + ' needed. Share it with someone who should be there.';
  }

  function wire(card) {
    var id = card.getAttribute('data-idea');
    var families = !!card.querySelector('.idea-family');
    var go = card.querySelector('.idea-go');
    var form = card.querySelector('.idea-form');
    var level = card.querySelector('.idea-level');
    var share = card.querySelector('.idea-share');
    var status = card.querySelector('.buy-status');
    var email = '';
    var shareUrl = '';

    function send(extra) {
      var body = { idea: id, email: email, consent: true, ref: ref };
      if (form && families) { body.adults = form.elements.adults.value; body.kids = form.elements.kids.value; }
      for (var k in extra) body[k] = extra[k];
      status.textContent = '';
      return post('/interest', body).then(function (res) {
        if (res.status !== 200 || !res.data.ok) { status.textContent = res.status === 429 ? 'Too many tries. Wait a minute.' : ERR; return null; }
        paint(card, res.data.idea);
        shareUrl = location.origin + '/ideas?ref=' + res.data.share_ref + '#' + id;
        return res.data.idea;
      }).catch(function () { status.textContent = ERR; return null; });
    }

    function counted(idea) {
      if (!idea) { go.disabled = false; return; }
      remember(email);
      track('idea_interest', { idea: id, ref: ref || null });
      go.hidden = true; if (form) form.hidden = true;
      level.hidden = false;
      share.querySelector('.idea-more').textContent = moreLine(idea, families);
    }

    go.addEventListener('click', function () {
      email = remembered();
      if (email && !families) { go.disabled = true; send({}).then(counted); return; }
      go.hidden = true; form.hidden = false;
      if (email) form.elements.email.value = email;
      form.elements.email.focus();
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      email = form.elements.email.value.trim().toLowerCase();
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { status.textContent = 'Enter your email.'; return; }
      if (!form.elements.consent.checked) { status.textContent = 'Tick the box so we can tell you when it runs.'; return; }
      if (form.elements.company.value) return;
      send({}).then(counted);
    });

    level.querySelectorAll('[data-level]').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-level');
        send({ level: v }).then(function (idea) {
          if (!idea) return;
          track('idea_level', { idea: id, level: v });
          level.hidden = true; share.hidden = false;
          share.querySelector('.idea-more').textContent = moreLine(idea, families);
        });
      });
    });

    share.querySelector('.idea-copy').addEventListener('click', function () {
      var title = card.querySelector('h3').textContent;
      if (navigator.share) { navigator.share({ title: title, url: shareUrl }).catch(function () {}); return; }
      try { navigator.clipboard.writeText(shareUrl); status.textContent = 'Link copied.'; } catch (e) { status.textContent = shareUrl; }
    });
  }

  root.querySelectorAll('.idea-card[data-idea]').forEach(wire);

  var suggest = root.querySelector('.idea-suggest-form');
  suggest.addEventListener('submit', function (e) {
    e.preventDefault();
    var status = suggest.parentNode.querySelector('.buy-status');
    var title = suggest.elements.title.value.trim();
    var email = suggest.elements.email.value.trim().toLowerCase();
    if (!title) { status.textContent = 'Add the idea.'; return; }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { status.textContent = 'Enter your email.'; return; }
    post('/suggest', { title: title, detail: suggest.elements.detail.value, email: email, company: suggest.elements.company.value })
      .then(function (res) {
        if (res.status === 200) { suggest.hidden = true; status.textContent = 'Thanks. It goes on the board once we have read it.'; track('idea_suggested', {}); }
        else status.textContent = ERR;
      }).catch(function () { status.textContent = ERR; });
  });

  // Counters, plus any suggestion Max approved, as a plain card at the end.
  fetch(API).then(function (r) { return r.json(); }).then(function (data) {
    (data.ideas || []).forEach(function (idea) {
      var card = root.querySelector('[data-idea="' + idea.id + '"]');
      if (card) paint(card, idea);
    });
    var template = root.querySelector('[data-idea="extended-jam"]');
    (data.suggestions || []).forEach(function (s) {
      var card = template.cloneNode(true);
      card.id = s.id; card.setAttribute('data-idea', s.id); card.setAttribute('data-threshold', s.threshold);
      card.querySelector('h3').textContent = s.title;
      card.querySelector('p').textContent = s.detail || '';
      card.querySelector('.idea-count').innerHTML = '<span class="idea-n">0</span> interested. At ' + s.threshold + ' we schedule it.';
      card.querySelectorAll('[id]').forEach(function (el) { el.id = el.id.replace('extended-jam', s.id); });
      card.querySelectorAll('[for]').forEach(function (el) { el.setAttribute('for', el.getAttribute('for').replace('extended-jam', s.id)); });
      root.querySelector('.idea-suggest').before(card);
      paint(card, s); wire(card);
    });
  }).catch(function () {});
})();
</script>"""
