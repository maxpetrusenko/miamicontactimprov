"""Markup and script for the verify-first signup: popup, inline forms, ribbon, card.

Three stages live inside every `form.subscribe-form`: 1 the details, 2 the one-time
code, 3 the personal 10% code. The script swaps them in place and talks to the Worker's
/api/subscribe, /api/verify and /api/resend-code. The promo code only ever arrives in
the /api/verify reply, so nothing on the page can show one before verification.
"""

STEP_COPY = {
    "en": {
        "welcome": "Welcome to",
        "brand": "Miami CI",
        "instruction": "Enter 6 digit one-time code below",
        "otp_label": "One-time code",
        "resend_prompt": "Didn't get code?",
        "resend": "Resend",
        "resend_wait": "Resend in {n}s",
        "sign_up": "SIGN UP",
        "appreciate": "We appreciate you!",
        "copy": "Copy",
        "copied": "Copied",
        "thanks": "Thank you!",
        "small": "We also emailed it to you. After this, an occasional discount about once a month, 20% off.",
        "used": "You already used your code. See you on Friday.",
        "sent_sms": "We texted you a code.",
        "sent_email": "We emailed you a code.",
        "wrong": "That code is not right. Try again.",
        "expired": "That code expired. Start again.",
        "wait": "Too many tries. Please wait a few minutes.",
        "ribbon": "GET 10% OFF",
        "ribbon_label": "Get 10% off one event",
    },
    "es": {
        "welcome": "Te damos la bienvenida a",
        "brand": "Miami CI",
        "instruction": "Escribe abajo el código de 6 dígitos",
        "otp_label": "Código de un solo uso",
        "resend_prompt": "¿No llegó el código?",
        "resend": "Reenviar",
        "resend_wait": "Reenviar en {n}s",
        "sign_up": "REGISTRARME",
        "appreciate": "¡Gracias por estar aquí!",
        "copy": "Copiar",
        "copied": "Copiado",
        "thanks": "¡Gracias!",
        "small": "También te lo enviamos por correo. Después, un descuento de vez en cuando, más o menos una vez al mes, del 20%.",
        "used": "Ya usaste tu código. Nos vemos el viernes.",
        "sent_sms": "Te enviamos un código por mensaje de texto.",
        "sent_email": "Te enviamos un código por correo.",
        "wrong": "Ese código no es correcto. Inténtalo otra vez.",
        "expired": "Ese código caducó. Empieza de nuevo.",
        "wait": "Demasiados intentos. Espera unos minutos.",
        "ribbon": "10% DE DESCUENTO",
        "ribbon_label": "Consigue un 10% de descuento en un evento",
    },
}


def _attr(text):
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def message_attrs(lang):
    """data-* attributes the script reads its result lines from."""
    c = STEP_COPY.get(lang, STEP_COPY["en"])
    pairs = {
        "wrong": c["wrong"], "expired": c["expired"], "wait": c["wait"],
        "sent-sms": c["sent_sms"], "sent-email": c["sent_email"], "used": c["used"],
        "resend-label": c["resend"], "resend-wait": c["resend_wait"], "copy-label": c["copy"], "copied": c["copied"],
    }
    return " ".join(f'data-{k}="{_attr(v)}"' for k, v in pairs.items())


def steps_two_three(lang, uid, popup):
    """Stage 2 (enter the code) and stage 3 (your code) markup."""
    c = STEP_COPY.get(lang, STEP_COPY["en"])
    otp_id = f"subscribe-otp-{uid}"
    no_thanks = ""
    if popup:
        from shell import SUBSCRIBE_COPY  # local import: shell imports this module

        no_thanks = f'\n    <button class="mci-popup-nothanks" type="button">{SUBSCRIBE_COPY.get(lang, SUBSCRIBE_COPY["en"])["no_thanks"]}</button>'
    return f"""  <div class="signup-step" data-step="2" hidden>
    <p class="signup-eyebrow">{c['welcome']}</p>
    <p class="signup-big">{c['brand']}</p>
    <p class="signup-instr">{c['instruction']}</p>
    <p class="signup-sentto" aria-live="polite"></p>
    <label class="subscribe-field" for="{otp_id}">
      <span class="sr-only">{c['otp_label']}</span>
      <input id="{otp_id}" class="signup-otp" name="otp" type="text" inputmode="numeric" autocomplete="one-time-code" maxlength="6" pattern="[0-9]*" placeholder="000000">
    </label>
    <p class="signup-resend">{c['resend_prompt']} <button class="signup-resend-btn" type="button" disabled>{c['resend']}</button></p>
    <button class="btn primary subscribe-submit" type="submit">{c['sign_up']}</button>{no_thanks}
  </div>
  <div class="signup-step" data-step="3" hidden>
    <p class="signup-eyebrow">{c['appreciate']}</p>
    <div class="signup-code-row">
      <span class="signup-code" aria-live="polite"></span>
      <button class="signup-copy" type="button">{c['copy']}</button>
    </div>
    <p class="signup-used" hidden>{c['used']}</p>
    <p class="signup-thanks">{c['thanks']}</p>
    <p class="signup-small">{c['small']}</p>
  </div>"""


def ribbon(lang):
    c = STEP_COPY.get(lang, STEP_COPY["en"])
    return f"""<div class="mci-ribbon" id="mci-ribbon" hidden>
  <button class="mci-ribbon-btn" type="button" aria-label="{_attr(c['ribbon_label'])}"><span>{c['ribbon']}</span></button>
</div>"""


SCRIPT = r"""<script>
(function () {
  var CLOSED_KEY = 'mci_popup_closed_at';
  var SUB_KEY = 'mci_popup_subscribed';
  var WEEK_MS = 7 * 24 * 60 * 60 * 1000;
  var get = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } };
  var set = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
  // Storage that cannot be read counts as "subscribed" for the popup (never nag) and as
  // "not subscribed" for the ribbon (a quiet, always available way in).
  var storageWorks = (function () { try { localStorage.getItem('x'); return true; } catch (e) { return false; } })();
  var isSubscribed = function () { return get(SUB_KEY) === '1'; };
  var recentlyClosed = function () {
    var t = parseInt(get(CLOSED_KEY), 10);
    return !isNaN(t) && Date.now() - t < WEEK_MS;
  };
  var capture = function (name) { try { if (window.posthog) posthog.capture(name); } catch (e) {} };

  var ribbon = document.getElementById('mci-ribbon');
  var syncRibbon = function () { if (ribbon) ribbon.hidden = isSubscribed(); };
  syncRibbon();

  // ---- popup ----
  var modal = document.getElementById('mci-popup');
  var card = modal ? modal.querySelector('.mci-popup') : null;
  var lastFocus = null;
  var focusables = function () {
    return Array.prototype.slice.call(
      card.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])')
    ).filter(function (el) { return !el.closest('[hidden]'); });
  };
  var onKeydown = function (e) {
    if (e.key === 'Escape') { closeModal(); return; }
    if (e.key !== 'Tab') return;
    var f = focusables();
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  };
  var openModal = function () {
    if (!modal || modal.classList.contains('is-open')) return;
    lastFocus = document.activeElement;
    modal.classList.add('is-open');
    document.body.classList.add('mci-popup-open');
    document.addEventListener('keydown', onKeydown, true);
    var f = focusables();
    if (f.length) f[0].focus();
    capture('newsletter_popup_shown');
  };
  function closeModal() {
    if (!modal) return;
    modal.classList.remove('is-open');
    document.body.classList.remove('mci-popup-open');
    document.removeEventListener('keydown', onKeydown, true);
    set(CLOSED_KEY, String(Date.now()));
    capture('newsletter_popup_closed');
    try { if (lastFocus && lastFocus.focus) lastFocus.focus(); else document.body.focus(); } catch (e) {}
  }
  if (modal) {
    var closeBtn = modal.querySelector('.mci-popup-close');
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    Array.prototype.forEach.call(modal.querySelectorAll('.mci-popup-nothanks'), function (b) { b.addEventListener('click', closeModal); });
    // Once a week: shown 5 seconds after load unless closed in the last 7 days or subscribed.
    if (storageWorks && !isSubscribed() && !recentlyClosed()) {
      setTimeout(function () { if (!isSubscribed() && !recentlyClosed()) openModal(); }, 5000);
    }
  }
  if (ribbon) {
    var rb = ribbon.querySelector('button');
    // The ribbon opens the popup even while the weekly timer is still counting.
    if (rb) rb.addEventListener('click', openModal);
  }

  // ---- signup forms ----
  var query = new URLSearchParams(window.location.search);
  var param = function (name) { return query.get(name) || ''; };
  var entry = param('src').toLowerCase().replace(/[^a-z0-9_-]/g, '').slice(0, 24);

  Array.prototype.forEach.call(document.querySelectorAll('form.subscribe-form'), function (form) {
    var q = function (s) { return form.querySelector(s); };
    var attr = function (k) { return form.getAttribute('data-' + k) || ''; };
    var steps = { 1: q('[data-step="1"]'), 2: q('[data-step="2"]'), 3: q('[data-step="3"]') };
    var status = q('.subscribe-status');
    var email = q('input[type="email"]');
    var phone = q('input[type="tel"]');
    var fullName = q('input[name="name"]');
    var consent = q('input[name="consent"]');
    var company = q('input[name="company"]');
    var otp = q('input[name="otp"]');
    var sentTo = q('.signup-sentto');
    var resendBtn = q('.signup-resend-btn');
    var codeEl = q('.signup-code');
    var copyBtn = q('.signup-copy');
    var usedEl = q('.signup-used');
    var base = attr('endpoint').replace(/\/subscribe$/, '');
    var stage = 1, timer = null, address = '';

    var say = function (key) { status.textContent = attr(key); };
    var submitBtn = function () { var s = steps[stage]; return s ? s.querySelector('button[type="submit"]') : null; };
    var show = function (n) {
      stage = n;
      [1, 2, 3].forEach(function (i) { if (steps[i]) steps[i].hidden = i !== n; });
      form.setAttribute('data-stage', String(n));
      var host = form.closest('.mci-popup');
      if (host) host.setAttribute('data-stage', String(n));
      status.textContent = '';
      var target = n === 2 ? otp : (n === 3 ? copyBtn : email);
      if (target) { try { target.focus(); } catch (e) {} }
    };
    var post = function (path, body) {
      return fetch(base + path, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (d) { return { status: r.status, data: d }; });
      });
    };
    // The select only offers +1 (US and Canada): a typed national number goes out as
    // +1 and ten digits; a number typed with its own + goes out as written.
    var phoneValue = function () {
      var raw = phone ? phone.value.trim() : '';
      if (!raw || raw.charAt(0) === '+') return raw;
      var digits = raw.replace(/\D/g, '');
      if (digits.length === 11 && digits.charAt(0) === '1') digits = digits.slice(1);
      return digits.length === 10 ? '+1' + digits : raw;
    };
    var countdown = function (seconds) {
      if (!resendBtn) return;
      clearInterval(timer);
      var n = seconds;
      var tick = function () {
        if (n <= 0) { clearInterval(timer); resendBtn.disabled = false; resendBtn.textContent = attr('resend-label'); return; }
        resendBtn.disabled = true;
        resendBtn.textContent = attr('resend-wait').replace('{n}', String(n));
        n -= 1;
      };
      tick();
      timer = setInterval(tick, 1000);
    };
    var failure = function (res, disableKey) {
      var btn = submitBtn();
      if (btn) btn.disabled = false;
      if (res && res.data && res.data.expired) { show(1); say('expired'); return; }
      say(res && res.status === 429 ? 'wait' : (disableKey || 'error'));
    };

    var startSignup = function () {
      if (!email.value.trim()) { email.focus(); return; }
      if (!consent.checked) { consent.focus(); return; }
      if (company && company.value.trim()) { return; }
      var btn = submitBtn();
      btn.disabled = true;
      say('sending');
      address = email.value.trim();
      post('/subscribe', {
        email: address,
        name: fullName ? fullName.value.trim() : '',
        phone: phoneValue(),
        consent: consent.checked,
        company: company ? company.value.trim() : '',
        source: attr('source') + (entry ? ':' + entry : ''),
        offer: attr('offer'),
        campaign: param('utm_campaign'),
        landing_page: window.location.pathname,
        referrer: document.referrer || '',
        utm_source: param('utm_source'),
        utm_medium: param('utm_medium'),
        utm_content: param('utm_content'),
      }).then(function (res) {
        btn.disabled = false;
        if (res.status === 200 && res.data.ok && res.data.step === 'verify') {
          if (form.closest('#mci-popup')) capture('newsletter_popup_submitted');
          show(2);
          if (sentTo) sentTo.textContent = attr(res.data.channel === 'sms' ? 'sent-sms' : 'sent-email');
          countdown(30);
        } else if (res.status === 200 && res.data.ok) {
          show(3);
        } else {
          failure(res);
        }
      }).catch(function () { failure(null); });
    };

    var finish = function (data) {
      if (data.code) {
        codeEl.textContent = data.code;
        codeEl.hidden = false;
        if (copyBtn) copyBtn.hidden = false;
        if (usedEl) usedEl.hidden = true;
      } else {
        codeEl.textContent = '';
        codeEl.hidden = true;
        if (copyBtn) copyBtn.hidden = true;
        if (usedEl) usedEl.hidden = false;
      }
      set(SUB_KEY, '1');
      syncRibbon();
      show(3);
      capture('newsletter_verified');
      // Identify by a hashed address, never the address itself.
      try {
        if (window.posthog && window.crypto && window.crypto.subtle) {
          var value = address.toLowerCase();
          window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(value)).then(function (buf) {
            var hex = Array.prototype.map.call(new Uint8Array(buf), function (b) { return b.toString(16).padStart(2, '0'); }).join('').slice(0, 32);
            posthog.identify(hex, consent && consent.checked ? { email: value } : {});
          }).catch(function () {});
        }
      } catch (e) {}
    };

    var verify = function () {
      var code = otp.value.replace(/\D/g, '');
      if (code.length !== 6) { otp.focus(); return; }
      var btn = submitBtn();
      btn.disabled = true;
      post('/verify', { email: address, code: code }).then(function (res) {
        btn.disabled = false;
        if (res.status === 200 && res.data.ok) { finish(res.data); return; }
        if (res.status === 400 && !res.data.expired) { say('wrong'); otp.value = ''; otp.focus(); return; }
        failure(res);
      }).catch(function () { failure(null); });
    };

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (stage === 1) startSignup();
      else if (stage === 2) verify();
    });
    if (otp) otp.addEventListener('input', function () { otp.value = otp.value.replace(/\D/g, '').slice(0, 6); });
    if (resendBtn) resendBtn.addEventListener('click', function () {
      if (resendBtn.disabled) return;
      resendBtn.disabled = true;
      post('/resend-code', { email: address }).then(function (res) {
        if (res.status === 200 && res.data.ok) { countdown(30); return; }
        if (res.data && res.data.expired) { show(1); say('expired'); return; }
        if (res.status === 429 && res.data && res.data.retry_after) { countdown(Math.min(res.data.retry_after, 3600)); say('wait'); return; }
        resendBtn.disabled = false;
        say('error');
      }).catch(function () { resendBtn.disabled = false; say('error'); });
    });
    if (copyBtn) copyBtn.addEventListener('click', function () {
      var value = codeEl.textContent;
      var done = function () {
        copyBtn.textContent = attr('copied');
        setTimeout(function () { copyBtn.textContent = attr('copy-label'); }, 2000);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(value).then(done).catch(function () {});
      } else {
        try {
          var range = document.createRange();
          range.selectNodeContents(codeEl);
          var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(range);
          document.execCommand('copy'); done();
        } catch (e) {}
      }
    });
  });
})();
</script>"""
