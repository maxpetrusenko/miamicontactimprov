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


def _count_line(threshold, families):
    if families:
        return f'<span class="idea-n">0</span> of {threshold} families, <span class="idea-kids">0</span> kids'
    return f'<span class="idea-n">0</span> interested. At {threshold} we schedule it.'


def _card(idea_id, title, line, threshold, families):
    # .card from the home page and the directory: white, bordered, h3 + p.
    return f"""
<article class="card" id="{idea_id}" data-idea="{idea_id}" data-threshold="{threshold}" data-families="{'1' if families else ''}">
  <h3>{title}</h3>
  <p>{line}</p>
  <p class="idea-count"><strong>{_count_line(threshold, families)}</strong></p>
  <div class="btn-row"><button class="btn secondary idea-go" type="button">Count me in</button></div>
</article>"""


def _number_select(name, label, lo, hi, default):
    opts = "".join(f'<option value="{n}"{" selected" if n == default else ""}>{n}</option>' for n in range(lo, hi + 1))
    return f'<label class="subscribe-phone" for="idea-{name}"><span>{label}</span><select id="idea-{name}" name="{name}">{opts}</select></label>'


def ideas():
    cards = "".join(_card(*row) for row in IDEAS)
    levels = "".join(f'<button type="button" class="btn secondary" data-level="{v}">{label}</button>' for v, label in LEVELS)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Ideas &middot; What we host next</p>
    <h1>What should we host next?</h1>
    <p class="lede">Each idea runs once enough people say they would come. Add yourself, say how sure you are, and share it with the people who should be there.</p>
  </div>
</section>

<section class="section">
  <div class="wrap" id="ideas" data-endpoint="{_attr(IDEAS_ENDPOINT)}">
    <div class="grid">
      {cards}
    </div>

    <div class="subscribe-block" id="idea-panel" hidden>
      <form class="subscribe-form" id="idea-form" novalidate>
        <label class="subscribe-label" for="idea-email">Count me in for <strong id="idea-title"></strong></label>
        <div class="subscribe-row">
          <input id="idea-email" name="email" type="email" autocomplete="email" placeholder="you@example.com">
          <span id="idea-family" hidden>{_number_select("adults", "Adults", 1, 4, 1)}{_number_select("kids", "Kids", 0, 6, 1)}</span>
          <button class="btn primary" type="submit">Count me in</button>
        </div>
        <div class="subscribe-hp" aria-hidden="true"><label for="idea-company">Company</label><input id="idea-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
        <label class="subscribe-consent" for="idea-consent"><input id="idea-consent" name="consent" type="checkbox" required><span>Email me when it is scheduled.</span></label>
      </form>
      <div id="idea-level" hidden>
        <p class="subscribe-label">At $20 to $30, would you come?</p>
        <div class="btn-row">{levels}</div>
      </div>
      <div id="idea-share" hidden>
        <p class="subscribe-label" id="idea-more"></p>
        <div class="btn-row"><button type="button" class="btn primary" id="idea-copy">Copy share link</button></div>
      </div>
      <p class="subscribe-status" role="status" aria-live="polite"></p>
    </div>

    <div class="prose">
      <h2 id="suggest">Suggest something</h2>
      <p>Something missing? Tell us. It goes on the board once we have read it.</p>
    </div>
    <div class="subscribe-block">
      <form class="subscribe-form" id="idea-suggest" novalidate>
        <label class="subscribe-label" for="sg-title">Your idea</label>
        <div class="subscribe-row">
          <input id="sg-title" name="title" type="text" maxlength="80" placeholder="Contact + yoga on Sunday mornings">
        </div>
        <div class="subscribe-row">
          <input id="sg-email" name="email" type="email" autocomplete="email" placeholder="you@example.com" aria-label="Email">
          <button class="btn primary" type="submit">Send it</button>
        </div>
        <div class="subscribe-hp" aria-hidden="true"><label for="sg-company">Company</label><input id="sg-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
        <p class="subscribe-status" role="status" aria-live="polite"></p>
      </form>
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
  var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  var q = new URLSearchParams(location.search);
  var ref = (q.get('ref') || '').trim().toLowerCase();
  if (!/^[a-z0-9][a-z0-9-]{0,39}$/.test(ref)) ref = '';

  var panel = document.getElementById('idea-panel');
  var form = document.getElementById('idea-form');
  var level = document.getElementById('idea-level');
  var share = document.getElementById('idea-share');
  var family = document.getElementById('idea-family');
  var status = panel.querySelector('.subscribe-status');
  var current = null, email = '', shareUrl = '';

  function remembered() { try { return localStorage.getItem(KEY) || ''; } catch (e) { return ''; } }
  function remember(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function track(name, props) { try { if (window.posthog) posthog.capture(name, props); } catch (e) {} }
  function post(path, body) {
    return fetch(API + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { status: r.status, data: d }; }); });
  }
  function paint(card, idea) {
    if (!card || !idea) return;
    var n = card.querySelector('.idea-n'); if (n) n.textContent = idea.count;
    var k = card.querySelector('.idea-kids'); if (k && typeof idea.kids === 'number') k.textContent = idea.kids;
  }
  function isFamilies() { return current && current.getAttribute('data-families') === '1'; }
  function moreLine(idea) {
    if (!idea.needed) return 'That is enough. We are scheduling it, and you hear first.';
    var unit = isFamilies() ? (idea.needed === 1 ? 'family' : 'families') : (idea.needed === 1 ? 'person' : 'people');
    return idea.needed + ' more ' + unit + ' needed. Share it with someone who should be there.';
  }
  function show(step) {
    form.hidden = step !== 'form'; level.hidden = step !== 'level'; share.hidden = step !== 'share';
  }
  function send(extra) {
    var id = current.getAttribute('data-idea');
    var body = { idea: id, email: email, consent: true, ref: ref, company: form.elements.company.value };
    if (isFamilies()) { body.adults = form.elements.adults.value; body.kids = form.elements.kids.value; }
    for (var k in extra) body[k] = extra[k];
    status.textContent = '';
    return post('/interest', body).then(function (res) {
      if (res.status !== 200 || !res.data.ok || !res.data.idea) { status.textContent = res.status === 429 ? 'Too many tries. Wait a minute.' : ERR; return null; }
      paint(current, res.data.idea);
      shareUrl = location.origin + '/ideas?ref=' + res.data.share_ref + '#' + id;
      return res.data.idea;
    }).catch(function () { status.textContent = ERR; return null; });
  }
  function counted(idea) {
    if (!idea) return;
    remember(email);
    track('idea_interest', { idea: current.getAttribute('data-idea'), ref: ref || null });
    document.getElementById('idea-more').textContent = moreLine(idea);
    show('level');
  }

  function open(card) {
    current = card;
    document.getElementById('idea-title').textContent = card.querySelector('h3').textContent;
    family.hidden = !isFamilies();
    status.textContent = '';
    panel.hidden = false;
    card.after(panel);
    email = remembered();
    if (email && !isFamilies()) { show('level'); send({}).then(counted); }
    else { show('form'); if (email) form.elements.email.value = email; }
    panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function wire(card) { card.querySelector('.idea-go').addEventListener('click', function () { open(card); }); }
  root.querySelectorAll('.card[data-idea]').forEach(wire);

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    email = form.elements.email.value.trim().toLowerCase();
    if (!EMAIL_RE.test(email)) { status.textContent = 'Enter your email.'; return; }
    if (!form.elements.consent.checked) { status.textContent = 'Tick the box so we can tell you when it runs.'; return; }
    send({}).then(counted);
  });

  level.querySelectorAll('[data-level]').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-level');
      send({ level: v }).then(function (idea) {
        if (!idea) return;
        track('idea_level', { idea: current.getAttribute('data-idea'), level: v });
        document.getElementById('idea-more').textContent = moreLine(idea);
        show('share');
      });
    });
  });

  document.getElementById('idea-copy').addEventListener('click', function () {
    var title = current.querySelector('h3').textContent;
    if (navigator.share) { navigator.share({ title: title, url: shareUrl }).catch(function () {}); return; }
    try { navigator.clipboard.writeText(shareUrl); status.textContent = 'Link copied.'; } catch (e) { status.textContent = shareUrl; }
  });

  var suggest = document.getElementById('idea-suggest');
  suggest.addEventListener('submit', function (e) {
    e.preventDefault();
    var st = suggest.querySelector('.subscribe-status');
    var title = suggest.elements.title.value.trim();
    var em = suggest.elements.email.value.trim().toLowerCase();
    if (!title) { st.textContent = 'Add the idea.'; return; }
    if (!EMAIL_RE.test(em)) { st.textContent = 'Enter your email.'; return; }
    post('/suggest', { title: title, email: em, company: suggest.elements.company.value }).then(function (res) {
      if (res.status === 200) { suggest.querySelectorAll('.subscribe-row').forEach(function (r) { r.hidden = true; }); st.textContent = 'Thanks. It goes on the board once we have read it.'; track('idea_suggested', {}); }
      else st.textContent = ERR;
    }).catch(function () { st.textContent = ERR; });
  });

  // Counters, plus any suggestion Max approved, as one more card.
  fetch(API).then(function (r) { return r.json(); }).then(function (data) {
    (data.ideas || []).forEach(function (idea) { paint(root.querySelector('[data-idea="' + idea.id + '"]'), idea); });
    var grid = root.querySelector('.grid');
    (data.suggestions || []).forEach(function (s) {
      var card = document.createElement('article');
      card.className = 'card'; card.id = s.id;
      card.setAttribute('data-idea', s.id); card.setAttribute('data-threshold', s.threshold);
      var h = document.createElement('h3'); h.textContent = s.title;
      var p = document.createElement('p'); p.textContent = s.detail || '';
      var c = document.createElement('p'); c.className = 'idea-count';
      c.innerHTML = '<strong><span class="idea-n">0</span> interested. At ' + Number(s.threshold) + ' we schedule it.</strong>';
      var row = document.createElement('div'); row.className = 'btn-row';
      row.innerHTML = '<button class="btn secondary idea-go" type="button">Count me in</button>';
      card.append(h, p, c, row); grid.appendChild(card);
      paint(card, s); wire(card);
    });
    if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView({ block: 'center' }); }
  }).catch(function () {});
})();
</script>"""
