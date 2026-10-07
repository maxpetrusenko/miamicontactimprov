"""Shared page shell for miamicontactimprov.com.

Every page is rendered through here so the head, nav and footer exist in exactly
one place, in every locale. Editing the nav means editing NAV below and re-running
build.py; adding a language means adding it to build/locales.py.

The locale model lives in build/locales.py. This module asks it two questions and
never invents a URL of its own: which route does this page have in that language
(`locales.route`), and which languages may this page offer (`locales.switch_targets`).
That is what stops the language switcher from pointing at a page that does not exist.

The visual system is the Miami Contact Improv marketing design: warm cream, Anton +
Poppins, a terracotta accent, a full-page grain overlay and a four-item pill nav
(Home / Events / About / Contact) plus a Follow-on-Instagram pill. The deeper library
pages (what-is, jams, classes, history, glossary, safety, directory, videos and the
Spanish tree) are kept reachable from the footer and inherit the same shell.
"""

import pathlib

import locales
import schema

SITE = locales.SITE
NAME = "Miami Contact Improv"
TAGLINE = "A working map of Contact Improvisation in Miami"

# Bump when the local listings in build/listings.py are re-checked against source.
LAST_CHECKED = "14 September 2026"
LAST_CHECKED_ES = "14 de septiembre de 2026"
LAST_CHECKED_ISO = "2026-09-14"
LAST_CHECKED_BY_LANG = {"en": LAST_CHECKED, "es": LAST_CHECKED_ES}

# The site's scope and nature, stated one way everywhere (footer, schema, llms.txt).
# schema.py owns the strings; the footer must not carry a second version of them.
SITE_SENTENCE_BY_LANG = schema.SITE_SENTENCE_BY_LANG
SITE_SENTENCE = schema.SITE_SENTENCE

INSTAGRAM_URL = "https://instagram.com/miamicontactimprov"

# The primary nav: the four marketing views. slug + the label in each locale.
# `locales.route(slug, lang)` decides the href, so a nav item can only point at a page
# this site actually builds; Events and Contact exist in English only, and a Spanish
# reader is sent to the English page with a lang annotation rather than to a 404.
NAV = [
    ("home", {"en": "Home", "es": "Inicio"}),
    ("events", {"en": "Events", "es": "Eventos"}),
    ("blog", {"en": "Blog", "es": "Blog"}),
    ("about", {"en": "About", "es": "Acerca de"}),
    ("contact", {"en": "Contact", "es": "Contacto"}),
]

# Instagram glyph, inline so the header carries no external request.
IG_GLYPH = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="6"/>'
    '<circle cx="12" cy="12" r="4.2"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" '
    'stroke="none"/></svg>'
)

# There is no "projects"/"properties" block in the footer, by decision: a sitewide
# reciprocal nav of the other sites the maintainer runs is the pattern Google's
# hidden-text-and-links policy exists to catch, and sitewide self-links are discounted
# at best. The list that used to live here and the flag that rendered it are gone rather
# than switched off, so the block cannot come back by flipping one line. What belongs on
# a page is a link earned by the page, not a footer that says it on every URL.

FOOTER_COLS = [
    ("start", {
        "en": "Start here",
        "es": "Para empezar",
    }, [
        ("what-is-contact-improvisation", {"en": "What is Contact Improvisation?", "es": "¿Qué es la Improvisación de Contacto?"}),
        ("your-first-jam", {"en": "Your first jam, step by step", "es": "Tu primera jam, paso a paso"}),
        ("glossary", {"en": "Glossary of CI terms", "es": "Glosario de términos"}),
        ("history", {"en": "History of CI", "es": "Historia de la IC"}),
        ("blog", {"en": "Blog", "es": "Blog"}),
    ]),
    ("miami", {
        "en": "In Miami",
        "es": "En Miami",
    }, [
        ("events", {"en": "Upcoming events", "es": "Próximos eventos"}),
        ("friday-jam", {"en": "Friday jam, Miami", "es": "Jam de los viernes, Miami"}),
        ("fundamentals", {"en": "Fundamentals, eight Fridays", "es": "Fundamentos, ocho viernes"}),
        ("miami", {"en": "The Miami scene", "es": "La escena de Miami"}),
        ("miami-jams", {"en": "Miami-Dade and Broward jam list", "es": "Lista de jams de Miami-Dade y Broward"}),
        ("jams", {"en": "Jams and open practice", "es": "Jams y práctica abierta"}),
        ("classes", {"en": "Classes and workshops", "es": "Clases y talleres"}),
        ("keep-practising", {"en": "Keep practising", "es": "Seguir practicando"}),
    ]),
    ("site", {
        "en": "This site",
        "es": "Este sitio",
    }, [
        ("about", {"en": "About the practice", "es": "Acerca de la práctica"}),
        ("safety-and-consent", {"en": "Safety and consent", "es": "Seguridad y consentimiento"}),
        ("faq", {"en": "Questions people ask", "es": "Preguntas frecuentes"}),
        ("directory", {"en": "Directory", "es": "Directorio"}),
        ("contact", {"en": "Contact", "es": "Contacto"}),
    ]),
]

def _css_version():
    """Short content hash of site/assets/site.css, so the stylesheet URL changes whenever
    the file does. Without this, the CDN kept serving a week-old cached site.css?v=4 while
    the HTML moved on, and the live site rendered unstyled."""
    import hashlib
    p = pathlib.Path(__file__).resolve().parent.parent / "site" / "assets" / "site.css"
    try:
        return hashlib.md5(p.read_bytes()).hexdigest()[:8]
    except OSError:
        return "5"


STYLESHEET = "/assets/site.css?v=" + _css_version()


# ------------------------------------------------------------ subscribe form
# The one endpoint a subscribe form may post to. Kept here so every form on the site
# points at the same Worker, and so changing it is one edit.
SUBSCRIBE_ENDPOINT = "https://newsletter-api.max-petrusenko.workers.dev/api/subscribe"

# The one endpoint a buy button may post to. Same Worker as the subscribe form, a
# different route. `kind` is one of 'class' | 'jam' | 'combo'; `event_date` pins it
# to a specific Friday and is omitted to let the Worker resolve the next upcoming
# one. Memberships and the intro pack are deferred -- see
# docs/plans/pricing-events-config.md -- so there is no plan/subscription concept
# here any more, only a drop-in kind.
CHECKOUT_ENDPOINT = "https://newsletter-api.max-petrusenko.workers.dev/api/checkout"

# The door payment link the /pay page hands off to. Printed on physical materials
# (door QR, posters) too, so this exact URL is the one stable thing that must never
# silently change without updating those -- see docs/plans/pricing-events-config.md.
DOOR_PAYMENT_LINK = "https://buy.stripe.com/3cIaEX1Oe13Xfxh45v4ow01"


def _posthog_config():
    """Reads POSTHOG_KEY / POSTHOG_HOST from the build environment.

    Local builds and this repo's public source never carry a real key: it is
    injected only at build time (a GitHub Actions secret in publish.yml). Unset
    here means `posthog_snippet()` emits nothing at all, and every call site that
    uses `window.posthog` already checks it exists first, so the whole analytics
    layer is a clean no-op until a key is wired in.
    """
    import os
    key = os.environ.get("POSTHOG_KEY", "").strip()
    host = os.environ.get("POSTHOG_HOST", "https://us.i.posthog.com").strip()
    return key, host


POSTHOG_KEY, POSTHOG_HOST = _posthog_config()


def posthog_snippet():
    """The PostHog bootstrap script, or "" when POSTHOG_KEY is unset.

    Uses PostHog's own loader snippet (not a CDN <script src>) so the real
    library only loads once a key exists. The `defaults` config key opts into
    PostHog's own current sane defaults (pageview/pageleave capture, etc.);
    the explicit keys after it are this site's specific requirements per Max
    (2026-10-01): autocapture on, session recording with email/phone fields
    masked by selector (not just by type, in case a form's input has no
    `type="tel"`), and `identified_only` person profiles so an anonymous
    visitor stays lightweight until `posthog.identify()` runs on a newsletter
    signup (see the subscribe-form handler below).

    Respects Do Not Track: `posthog.init` itself is skipped at runtime for a
    visitor whose browser sends DNT, so nothing starts tracking for them even
    though the loader tag is still served (cheap, inert until `init` runs).
    """
    if not POSTHOG_KEY:
        return ""
    mask_selector = 'input[type="email"], input[type="tel"], input[name="email"], input[name="phone"]'
    return f"""<script>
!function(t,e){{var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){{function g(t,e){{var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){{t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],Object.defineProperty(u,"toString",{{configurable:!0,enumerable:!0,writable:!0,value:function(t){{var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e}}}}),Object.defineProperty(u.people,"toString",{{configurable:!0,enumerable:!0,writable:!0,value:function(){{return u.toString(1)+".people (stub)"}}}}),o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagResult isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])}},e.__SV=1)}}(document,window.posthog||[]);
if (!(navigator.doNotTrack === '1' || window.doNotTrack === '1' || navigator.doNotTrack === 'yes')) {{
  posthog.init('{POSTHOG_KEY}', {{
    api_host: '{POSTHOG_HOST}',
    defaults: '2026-05-30',
    person_profiles: 'identified_only',
    capture_pageview: true,
    capture_pageleave: true,
    autocapture: true,
    session_recording: {{ maskAllInputs: true, maskTextSelector: '{mask_selector}' }}
  }});
}}
</script>"""

# The form copy, per locale. The label carries the whole offer: the discount and the
# send frequency, in one sentence. The discount code itself is never printed here; the
# welcome email that follows a signup carries it. `consent` is the one-sentence,
# required opt-in line the field sits above a checkbox for - not a hint, the actual
# legal consent statement, because a form that texts a phone number needs one.
SUBSCRIBE_COPY = {
    "en": {
        "label": "Subscribe for 10% off one event, and one email a month.",
        "name_label": "Full name",
        "name_placeholder": "First name",
        "email_label": "Email",
        "phone_label": "Phone (optional)",
        "country_label": "Country",
        "countries": [("US", "United States (+1)"), ("CA", "Canada (+1)")],
        "consent": "I agree to receive promotional emails and text messages from Miami CI. Message and data rates may apply.",
        "button": "Get my code",
        "popup_button": "SECURE YOUR SPACE",
        "no_thanks": "NO THANKS",
        "sending": "Sending.",
        "ok": "If this is your first signup, your 10% code is on its way to your email (and phone, if you left one). After that we send an occasional discount, about once a month, 20% off.",
        "error": "That did not go through. Try again, or email hello@miamicontactimprov.com.",
    },
    "es": {
        "label": "Suscríbete para un 10% de descuento en un evento, y un correo al mes.",
        "name_label": "Nombre completo",
        "name_placeholder": "Nombre",
        "email_label": "Correo",
        "phone_label": "Teléfono (opcional)",
        "country_label": "País",
        "countries": [("US", "Estados Unidos (+1)"), ("CA", "Canadá (+1)")],
        "consent": "Acepto recibir correos promocionales y mensajes de texto de Miami CI. Pueden aplicarse tarifas de mensajes y datos.",
        "button": "Quiero mi código",
        "popup_button": "ASEGURA TU LUGAR",
        "no_thanks": "NO, GRACIAS",
        "sending": "Enviando.",
        "ok": "Si es tu primera suscripción, tu código del 10% va en camino a tu correo (y a tu teléfono, si dejaste uno). Después enviamos un descuento de vez en cuando, más o menos una vez al mes, del 20%.",
        "error": "No se pudo enviar. Inténtalo otra vez o escribe a hello@miamicontactimprov.com.",
    },
}


def _attr(text):
    """Escape a string for use inside a double-quoted HTML attribute."""
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def page_slug(path):
    """A short, stable name for a page: what a signup source and a form id are built from."""
    slug = (path or "/").strip("/").replace("/", "-")
    return slug or "home"


def subscribe_form(lang="en", source="", uid="page", label=None, button=None, popup=False):
    """The subscribe form. One markup, every locale, every placement.

    It posts JSON to the Worker and writes its own result line. With JavaScript off the
    submit does nothing rather than promising something it cannot do, which is why the
    markup carries no action attribute.

    `source` travels with the signup. The Worker sends the welcome email and the 10%
    code only when the source starts with `miamicontactimprov`, so the value here is
    what decides whether a reader gets the code.

    `label` and `button` replace the shared copy for a form whose offer is written for
    the page it sits on. The label is the sentence the reader answers and this site has
    no separate hint line under the field, so a page that offers the next dates rather
    than the monthly email says so in the label itself and nowhere else.

    Phone is a second, optional field: the Worker texts the code to it when given, but
    making it required would only cost signups. The consent
    checkbox is required and is the actual legal line, not a hint - it names both
    channels because a reader who leaves a number is agreeing to be texted on it.
    The honeypot field is hidden from sighted users by CSS alone (no display:none, a
    simple bot still fills it) and read by the Worker, which drops a submission that
    fills it rather than answering it as spam.
    """
    copy = SUBSCRIBE_COPY.get(lang, SUBSCRIBE_COPY[locales.DEFAULT])
    field_id = f"subscribe-{uid}"
    name_id = f"subscribe-name-{uid}"
    phone_id = f"subscribe-phone-{uid}"
    country_id = f"subscribe-country-{uid}"
    consent_id = f"subscribe-consent-{uid}"
    hp_id = f"subscribe-hp-{uid}"
    text = label or copy["label"]
    action = button or (copy["popup_button"] if popup else copy["button"])
    # In the popup the heading carries the offer, so the label stays for screen readers only.
    label_class = "subscribe-label sr-only" if popup else "subscribe-label"
    options = "".join(f'<option value="{code}">{name}</option>' for code, name in copy["countries"])
    no_thanks = (
        f'\n  <button class="mci-popup-nothanks" type="button">{copy["no_thanks"]}</button>' if popup else ""
    )
    return f"""<form class="subscribe-form" data-source="{_attr(source)}" data-offer="{_attr(text)}" data-endpoint="{SUBSCRIBE_ENDPOINT}" data-sending="{_attr(copy['sending'])}" data-ok="{_attr(copy['ok'])}" data-error="{_attr(copy['error'])}">
  <p class="{label_class}">{text}</p>
  <div class="subscribe-fields">
    <label class="subscribe-field" for="{name_id}">
      <span>{copy['name_label']}</span>
      <input id="{name_id}" name="name" type="text" autocomplete="name" maxlength="80" placeholder="{_attr(copy['name_placeholder'])}">
    </label>
    <label class="subscribe-field" for="{field_id}">
      <span>{copy['email_label']}</span>
      <input id="{field_id}" name="email" type="email" inputmode="email" autocomplete="email" required>
    </label>
    <div class="subscribe-field subscribe-phone-row">
      <span>{copy['phone_label']}</span>
      <div class="subscribe-phone-inputs">
        <select id="{country_id}" name="country" aria-label="{_attr(copy['country_label'])}">{options}</select>
        <input id="{phone_id}" name="phone" type="tel" inputmode="tel" autocomplete="tel-national" aria-label="{_attr(copy['phone_label'])}">
      </div>
    </div>
  </div>
  <div class="subscribe-hp" aria-hidden="true">
    <label for="{hp_id}">Company</label>
    <input id="{hp_id}" name="company" type="text" tabindex="-1" autocomplete="off">
  </div>
  <label class="subscribe-consent" for="{consent_id}">
    <input id="{consent_id}" name="consent" type="checkbox" required>
    <span>{copy['consent']}</span>
  </label>
  <button class="btn primary subscribe-submit" type="submit">{action}</button>{no_thanks}
  <p class="subscribe-status" role="status" aria-live="polite"></p>
</form>"""


def subscribe_block(lang, source, offer, uid, button=None, anchor=None):
    """A subscribe form with the offer written for the page it sits on.

    There is one form, one endpoint and one Worker. What changes page by page is the
    sentence above the field and the source the signup is filed under, and those two
    belong together: a page that offers the next dates cannot file its signups against
    a page that offers something else. Putting both in one call is what keeps them
    beside each other.

    `button` replaces the shared button label for a page whose own call to action is the
    email (the acquisition page's "send me the dates"), and `anchor` names the wrapper
    for a page that links to its own form from further up.
    """
    ident = f' id="{anchor}"' if anchor else ""
    return (
        f'<div class="subscribe-block"{ident}>\n'
        f"  {subscribe_form(lang, source=source, uid=uid, label=offer, button=button)}\n"
        f"</div>"
    )


# The buy button's own result lines, mirroring the subscribe form's data-sending/
# data-error naming so the two components read as one family. The error line reuses
# the subscribe form's exact phrase, for voice consistency across the site's two forms
# of checkout. The "closed" line is filled in by JS, not printed here, because it
# carries a link built from the Worker's own response (`door_url`).
BUY_COPY = {
    "en": {
        "sending": "Opening checkout.",
        "error": "That did not go through. Try again, or email hello@miamicontactimprov.com.",
        "closed": "Online sales closed, pay at the door ($30).",
        "closed_link": "What this looks like",
    },
}


def buy_button(kind, label, uid, event_date=None, lang="en"):
    """A buy button: one click, one POST to CHECKOUT_ENDPOINT, no real form submit.

    `kind` is one of 'class' | 'jam' | 'combo' and travels as `data-kind`.
    `event_date` pins the button to one specific Friday (none are, in this
    slice); a generic "Buy ticket" button carries no `data-event-date` and the
    Worker resolves the next upcoming one for that kind itself. Today only
    `kind="class"` ever resolves to a real, open date -- see
    docs/plans/pricing-events-config.md for why jam/combo buttons aren't shown
    yet rather than shown disabled.

    The status line sits next to the button, empty until a click resolves it - this is
    feedback from an action the reader just took, not a caption explaining the button.
    """
    copy = BUY_COPY.get(lang, BUY_COPY["en"])
    btn_id = f"buy-{uid}"
    date_attr = f' data-event-date="{_attr(event_date)}"' if event_date else ""
    return (
        f'<div class="buy-button">'
        f'<button class="btn primary" type="button" id="{btn_id}" data-kind="{_attr(kind)}"{date_attr} '
        f'data-endpoint="{CHECKOUT_ENDPOINT}" data-sending="{_attr(copy["sending"])}" '
        f'data-error="{_attr(copy["error"])}" data-closed="{_attr(copy["closed"])}">{label}</button>'
        f'<p class="buy-status" role="status" aria-live="polite"></p>'
        f'</div>'
    )


# ------------------------------------------------------------ newsletter popup
# The copy for the popup heading, per locale. The form itself is the same
# subscribe_form() every inline and footer placement uses, so its own label and
# offer carry the mechanics (10% off one event, one email a month); this heading carries the
# hook that gets a reader to look at the form at all.
POPUP_HEADING = {
    "en": ("Sign up to receive", "a 10% discount code"),
    "es": ("Suscríbete y recibe", "un código de descuento del 10%"),
}

POPUP_CLOSE_LABEL = {"en": "Close", "es": "Cerrar"}


def newsletter_popup(lang, path):
    """The site-wide signup modal, injected once per page by page().

    Behaviour lives in body_script(): shown once per visitor after 5 seconds via
    localStorage, closed by the ✕, Escape or a backdrop click, focus-trapped while
    open. The form posts through the same `.subscribe-form` handler every other
    form on the site already uses - this markup only has to carry the class.
    """
    slug = page_slug(path)
    heading_id = f"mci-popup-heading-{slug}"
    eyebrow, big = POPUP_HEADING.get(lang, POPUP_HEADING["en"])
    close_label = POPUP_CLOSE_LABEL.get(lang, POPUP_CLOSE_LABEL["en"])
    form = subscribe_form(lang, source=f"miamicontactimprov:popup:{slug}", uid=f"popup-{slug}", popup=True)
    return f"""<div class="mci-popup-overlay" id="mci-popup">
  <div class="mci-popup" role="dialog" aria-modal="true" aria-labelledby="{heading_id}">
    <button class="mci-popup-close" type="button" aria-label="{close_label}">&times;</button>
    <h2 id="{heading_id}" class="mci-h"><span class="mci-popup-eyebrow">{eyebrow}</span> <span class="mci-popup-big">{big}</span></h2>
    {form}
  </div>
</div>"""


def _nav_href(slug, lang):
    """The route for a nav/footer link, in the reader's language when one exists.

    When it does not, the link still goes to the page that exists rather than to a
    404, and the anchor carries lang="en" so a screen reader and a browser's
    translator are told the destination is in English.
    """
    route = locales.route(slug, lang)
    if route:
        return route, True
    return locales.route(slug, locales.DEFAULT) or "/", False


def _link(slug, lang, label):
    href, translated = _nav_href(slug, lang)
    attr = "" if translated else f' lang="{locales.HTML_LANG[locales.DEFAULT]}" hreflang="{locales.HTML_LANG[locales.DEFAULT]}"'
    return f'<a href="{href}"{attr}>{label}</a>'


def head(title, description, path, *, jsonld="", og_type="website", extra_head="", lang="en", slug=None):
    """Return the <head> block. `path` is the site-relative route, e.g. /miami.

    Emits the reciprocal alternate set for this page and x-default. A locale appears
    in that set only when this page exists in it, so every hreflang target on this
    site is a file the build actually wrote.
    """
    url = SITE + path
    slug = slug or locales.slug_for(path, lang)
    alts = locales.alternates(slug) if slug else []
    alt_tags = "\n".join(
        f'<link rel="alternate" hreflang="{locales.HTML_LANG[code]}" href="{href}">'
        for code, href in alts
    )
    if alts:
        default_route = locales.route(slug, locales.DEFAULT)
        alt_tags += f'\n<link rel="alternate" hreflang="x-default" href="{locales.url_for(default_route)}">'
    og_locale = locales.OG_LOCALE.get(lang, "en_US")
    og_alternates = "\n".join(
        f'<meta property="og:locale:alternate" content="{locales.OG_LOCALE[code]}">'
        for code, _href in alts
        if code != lang
    )
    return f"""<!DOCTYPE html>
<html lang="{locales.HTML_LANG.get(lang, "en")}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
{alts and alt_tags or ""}
<meta name="theme-color" content="#F3EDE1">
<meta name="color-scheme" content="light">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Hallandale Beach, Florida">
<meta name="geo.position" content="25.987;-80.148">
<meta name="ICBM" content="25.987, -80.148">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{schema.OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Two hands reaching toward each other against a pink sunset sky">
<meta property="og:locale" content="{og_locale}">
{og_alternates}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{schema.OG_IMAGE}">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/favicon-96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Poppins:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{STYLESHEET}">
<link rel="alternate" type="text/plain" href="{SITE}/llms.txt" title="llms.txt">
{extra_head}{posthog_snippet()}{jsonld}
</head>"""


LANG_SWITCH_CSS_CLASS = "lang-switch"


def language_switch(path, lang):
    """The language switcher. One entry per locale this site publishes."""
    if not locales.LOCALES or len(locales.LOCALES) < 2:
        return ""
    slug = locales.slug_for(path, lang)
    if not slug:
        return ""
    items = []
    for code, href, is_current, is_translation in locales.switch_targets(slug, lang):
        label = locales.LOCALE_SHORT[code]
        if is_current:
            items.append(
                f'<span class="lang-item is-current" lang="{locales.HTML_LANG[code]}" '
                f'aria-current="true">{label}</span>'
            )
            continue
        note = locales.NO_TRANSLATION_TITLE.get(code, locales.NO_TRANSLATION_TITLE["en"])
        extra = "" if is_translation else f' title="{note}"'
        hl = f' hreflang="{locales.HTML_LANG[code]}"' if is_translation else ""
        items.append(
            f'<a class="lang-item" href="{href}" lang="{locales.HTML_LANG[code]}"'
            f'{hl}{extra}>{label}</a>'
        )
    return (
        f'<nav class="{LANG_SWITCH_CSS_CLASS}" aria-label="{locales.SWITCHER_LABEL}">'
        + "".join(items)
        + "</nav>"
    )


def header(current, lang="en"):
    links = []
    for slug, labels in NAV:
        label = labels.get(lang) or labels[locales.DEFAULT]
        href, translated = _nav_href(slug, lang)
        cur = ' aria-current="page"' if href == current else ""
        default_lang = locales.HTML_LANG[locales.DEFAULT]
        extra = "" if translated else f' lang="{default_lang}" hreflang="{default_lang}"'
        links.append(f'<a href="{href}"{cur}{extra}>{label}</a>')
    follow_label = "Follow" if lang != "es" else "Seguir"
    links.append(
        f'<a class="follow" href="{INSTAGRAM_URL}" target="_blank" rel="noopener">'
        f'{IG_GLYPH}<span>{follow_label}</span></a>'
    )
    home = locales.route("home", lang) or "/"
    return f"""<header class="site-header" id="site-header">
  <div class="header-inner">
    <a class="brand" href="{home}">
      <img src="/assets/logo.png" alt="Miami Contact Improv" width="42" height="42">
      <span class="wordmark">Miami<br>Contact Improv</span>
    </a>
    {language_switch(current, lang)}
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="primary-nav">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="primary-nav" aria-label="Primary">
      {''.join(links)}
    </nav>
  </div>
</header>"""


def footer(lang="en", path="/"):
    """The site footer: link columns and the colophon. No subscribe form lives here;
    signups come from the landing popup and the inline page forms."""
    slug = page_slug(path)
    cols = []
    for _key, titles, items in FOOTER_COLS:
        title = titles.get(lang) or titles[locales.DEFAULT]
        lis = "".join(
            f'<li>{_link(slug, lang, label.get(lang) or label[locales.DEFAULT])}</li>'
            for slug, label in items
        )
        cols.append(f'<div><h3>{title}</h3><ul>{lis}</ul></div>')
    sentence = SITE_SENTENCE_BY_LANG.get(lang, SITE_SENTENCE)
    if lang == "es":
        colophon = (
            f"Última comprobación de las sesiones locales: {LAST_CHECKED}. La Improvisación de "
            "Contacto no tiene autoridad central, ni licencia, ni membresía. Este sitio es un "
            "mapa, no el mapa."
        )
    else:
        colophon = (
            f"Local listings last checked {LAST_CHECKED}. Contact Improvisation has no central "
            "authority, no licence and no membership. This site is one map of it, not the map."
        )
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      {''.join(cols)}
    </div>
    <div class="colophon">
      <span>&copy; Miami Contact Improv &middot; {sentence}</span>
    </div>
  </div>
</footer>"""


SKIP_LABELS = {"en": "Skip to content", "es": "Saltar al contenido"}


SCROLL_CONTROLS = """<div class="scroll-controls" id="scroll-controls" aria-hidden="true">
  <button class="to-top" type="button" aria-label="Scroll to top">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>
  </button>
</div>"""


def body_script():
    return """<script>
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canHover = window.matchMedia && window.matchMedia('(hover: hover)').matches;

  // ---- mobile nav ----
  var header = document.getElementById('site-header');
  var toggle = header && header.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
    });
    header.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && header) { header.classList.remove('nav-open'); if (toggle) toggle.setAttribute('aria-expanded', 'false'); }
  });

  // ---- floating scroll controls ----
  var sc = document.getElementById('scroll-controls');
  if (sc) {
    var top = sc.querySelector('.to-top');
    var down = sc.querySelector('.to-bottom');
    var onScroll = function () {
      sc.classList.toggle('is-scrolled', window.scrollY > 400);
      var atBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 80;
      sc.classList.toggle('at-bottom', atBottom);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
    if (down) down.addEventListener('click', function () { window.scrollBy({ top: window.innerHeight * 0.85, behavior: reduce ? 'auto' : 'smooth' }); });
  }

  // ---- scroll reveal ----
  var reveals = document.querySelectorAll('.mci-reveal');
  if (reveals.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      reveals.forEach(function (el) { el.classList.add('mci-in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('mci-in'); io.unobserve(en.target); } });
      }, { threshold: 0.15 });
      reveals.forEach(function (el) { io.observe(el); });
      setTimeout(function () {
        reveals.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.top < window.innerHeight && r.bottom > 0) el.classList.add('mci-in');
        });
      }, 600);
    }
  }

  // ---- hero cursor parallax ----

  // Upcoming-jam stamp: the build bakes the next date in; refresh it in the browser so a
  // deploy from last week still shows this Friday. Friday counts as upcoming until 9 PM.
  (function () {
    var st = document.getElementById('mci-stamp');
    if (!st || !st.dataset.first) return;
    try {
      var now = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/New_York' }));
      var d = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      if (d.getDay() === 5 && now.getHours() >= parseInt(st.dataset.end, 10)) d.setDate(d.getDate() + 1);
      d.setDate(d.getDate() + ((5 - d.getDay() + 7) % 7));
      var fp = st.dataset.first.split('-');
      var first = new Date(+fp[0], +fp[1] - 1, +fp[2]);
      if (d < first) d = first;
      var isFirst = d.getTime() === first.getTime();
      var mEn = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
      var mEs = ['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC'];
      var months = st.dataset.lang === 'es' ? mEs : mEn;
      var label = isFirst ? st.dataset.labelFirst : st.dataset.labelNext;
      var lab = st.querySelector('[data-role="label"]'), dt = st.querySelector('[data-role="date"]');
      if (lab) lab.textContent = label;
      if (dt) dt.textContent = d.getDate() + ' ' + months[d.getMonth()];
      st.setAttribute('aria-label', label + ', ' + d.getDate() + ' ' + months[d.getMonth()]);
    } catch (e) {}
  })();
  var hero = document.getElementById('mci-hero');
  if (hero && canHover && !reduce) {
    var byId = function (id) { return document.getElementById(id); };
    var apply = function (hx, hy) {
      var set = function (id, t) { var el = byId(id); if (el) el.style.transform = t; };
      set('mci-disc', 'translate(' + (hx * 34).toFixed(1) + 'px,' + (hy * 34).toFixed(1) + 'px)');
      set('mci-ring', 'translate(' + (hx * -22).toFixed(1) + 'px,' + (hy * -22).toFixed(1) + 'px) rotate(' + (hx * 10).toFixed(1) + 'deg)');
      set('mci-dot1', 'translate(' + (hx * 60).toFixed(1) + 'px,' + (hy * 60).toFixed(1) + 'px)');
      set('mci-dot2', 'translate(' + (hx * -48).toFixed(1) + 'px,' + (hy * -48).toFixed(1) + 'px)');
      set('mci-logo', 'rotateY(' + (hx * 16).toFixed(1) + 'deg) rotateX(' + (-hy * 12).toFixed(1) + 'deg) translate(' + (hx * -18).toFixed(1) + 'px,' + (hy * -18).toFixed(1) + 'px)');
      set('mci-chip1', 'translate(' + (hx * 42).toFixed(1) + 'px,' + (hy * 42).toFixed(1) + 'px) rotate(' + (hx * 6).toFixed(1) + 'deg)');
      set('mci-chip2', 'translate(' + (hx * -36).toFixed(1) + 'px,' + (hy * -36).toFixed(1) + 'px) rotate(' + (hx * -5).toFixed(1) + 'deg)');
      set('mci-w1', 'translate(' + (hx * 6).toFixed(1) + 'px,' + (hy * 6).toFixed(1) + 'px)');
      set('mci-w2', 'translate(' + (hx * 12).toFixed(1) + 'px,' + (hy * 12).toFixed(1) + 'px)');
      set('mci-w3', 'translate(' + (hx * 20).toFixed(1) + 'px,' + (hy * 20).toFixed(1) + 'px)');
    };
    hero.addEventListener('mousemove', function (e) {
      var r = hero.getBoundingClientRect();
      apply((e.clientX - r.left) / r.width - 0.5, (e.clientY - r.top) / r.height - 0.5);
    });
    hero.addEventListener('mouseleave', function () { apply(0, 0); });
    var logoWrap = document.getElementById('mci-logo-float');
    var logo = byId('mci-logo');
    if (logo && logoWrap) {
      logo.addEventListener('click', function () {
        logoWrap.classList.add('pulse');
        setTimeout(function () { logoWrap.classList.remove('pulse'); }, 600);
      });
    }
  }

  // ---- photo hero: cursor parallax + scroll cue ----
  var heroP = document.getElementById('mci-hero');
  var heroBg = document.getElementById('mci-hero-bg');
  var heroIn = document.getElementById('mci-hero-inner');
  if (heroP && heroBg) {
    if (canHover && !reduce) {
      heroP.addEventListener('mousemove', function (e) {
        var r = heroP.getBoundingClientRect();
        var hx = (e.clientX - r.left) / r.width - 0.5, hy = (e.clientY - r.top) / r.height - 0.5;
        heroBg.style.transform = 'translate3d(' + (hx * -22).toFixed(1) + 'px,' + (hy * -16).toFixed(1) + 'px,0)';
        if (heroIn) heroIn.style.transform = 'translate3d(' + (hx * 10).toFixed(1) + 'px,' + (hy * 7).toFixed(1) + 'px,0)';
      });
      heroP.addEventListener('mouseleave', function () { heroBg.style.transform = ''; if (heroIn) heroIn.style.transform = ''; });
    }
    var cue = function () { heroP.classList.toggle('is-scrolled', window.scrollY > 80); };
    window.addEventListener('scroll', cue, { passive: true }); cue();
  }

  // ---- instagram frames: height follows width so no blank space below the card ----
  var fitIg = function () {
    document.querySelectorAll('.ig-frame').forEach(function (f) { var w = f.clientWidth; if (w) f.style.height = Math.round(w * 1.25 + 250) + 'px'; });
  };
  fitIg(); window.addEventListener('load', fitIg); window.addEventListener('resize', fitIg);

  // ---- read-more (home) ----
  document.querySelectorAll('.mci-more').forEach(function (btn) {
    var target = document.getElementById(btn.getAttribute('data-target'));
    if (!target) return;
    target.hidden = true;
    btn.addEventListener('click', function () {
      var open = target.hidden;
      target.hidden = !open;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      var lbl = btn.querySelector('.lbl');
      if (lbl) lbl.textContent = open ? 'Show less' : 'Read more';
    });
  });

  // ---- accordion (about FAQ) ----
  document.querySelectorAll('.mci-accordion .q').forEach(function (q) {
    q.addEventListener('click', function () {
      var item = q.closest('.item');
      var open = item.classList.toggle('open');
      q.setAttribute('aria-expanded', open ? 'true' : 'false');
      var ic = q.querySelector('.ic');
      if (ic) ic.textContent = open ? '\\u2013' : '+';
    });
  });

  // ---- mailing-list form (contact) ----
  var form = document.getElementById('mci-signup');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (form.querySelector('[name=name]') || {}).value || '';
      var email = (form.querySelector('[name=email]') || {}).value || '';
      var btn = form.querySelector('button');
      if (name && email) {
        var body = encodeURIComponent('Please add me to the Miami Contact Improv mailing list.\\n\\nName: ' + name + '\\nEmail: ' + email);
        window.location.href = 'mailto:hello@miamicontactimprov.com?subject=' + encodeURIComponent('Mailing list sign-up') + '&body=' + body;
        if (btn) btn.textContent = 'Opening your email app…';
      }
    });
  }

  // ---- background video kick (unused on the marketing views, kept for compatibility) ----
  var v = document.getElementById('video');
  if (v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }

  // Subscribe forms. The endpoint, the source and the result lines come from the
  // form's own data attributes, so this runs unchanged on every page and in both
  // locales. A signup that reaches the Worker is done: nothing is sent twice.
  //
  // The campaign fields are read at the moment of the submit, from the address the
  // reader actually arrived on: a QR code at the door carries ?src=door, a link in an
  // Instagram bio carries utm_*. `src` rides on the end of the source, which is what
  // separates a signup made in the room from one made from the bio of the same page.
  // The source the Worker keys the welcome email off is the part before it.
  var query = new URLSearchParams(window.location.search);
  var param = function (name) { return query.get(name) || ''; };
  // Kept to letters, digits, dash and underscore, and short: the Worker stores a source
  // up to 64 characters and reads it as a prefix.
  var entry = param('src').toLowerCase().replace(/[^a-z0-9_-]/g, '').slice(0, 24);
  document.querySelectorAll('form.subscribe-form').forEach(function (form) {
    var status = form.querySelector('.subscribe-status');
    var button = form.querySelector('button[type="submit"]');
    var input = form.querySelector('input[type="email"]');
    var phone = form.querySelector('input[type="tel"]');
    var fullName = form.querySelector('input[name="name"]');
    var consent = form.querySelector('input[name="consent"]');
    var company = form.querySelector('input[name="company"]');
    var say = function (key) { status.textContent = form.getAttribute('data-' + key) || ''; };
    // The country select only offers +1 (US and Canada), so a typed national number is
    // sent as +1 and ten digits; a number typed with its own + is sent as written.
    var phoneValue = function () {
      var raw = phone ? phone.value.trim() : '';
      if (!raw || raw.charAt(0) === '+') return raw;
      var digits = raw.replace(/\D/g, '');
      if (digits.length === 11 && digits.charAt(0) === '1') digits = digits.slice(1);
      return digits.length === 10 ? '+1' + digits : raw;
    };
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!input.value.trim()) { input.focus(); return; }
      if (!consent.checked) { consent.focus(); return; }
      if (company && company.value.trim()) { return; }
      button.disabled = true;
      say('sending');
      fetch(form.getAttribute('data-endpoint'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: input.value.trim(),
          name: fullName ? fullName.value.trim() : '',
          phone: phoneValue(),
          consent: consent.checked,
          company: company ? company.value.trim() : '',
          source: form.getAttribute('data-source') + (entry ? ':' + entry : ''),
          offer: form.getAttribute('data-offer') || '',
          campaign: param('utm_campaign'),
          landing_page: window.location.pathname,
          referrer: document.referrer || '',
          utm_source: param('utm_source'),
          utm_medium: param('utm_medium'),
          utm_content: param('utm_content'),
        }),
      }).then(function (response) {
        return response.json().catch(function () { return {}; }).then(function (data) {
          return response.ok && data.ok;
        });
      }).then(function (ok) {
        if (ok) {
          form.reset();
          say('ok');
          // Any successful signup, from any form, retires the landing popup for good.
          try { localStorage.setItem('mci_popup_subscribed', '1'); } catch (e) {}
          try {
            if (window.posthog && form.closest('#mci-popup')) posthog.capture('newsletter_popup_submitted');
          } catch (e) {}
          // Identify by a hashed email, never the address itself: the hash is
          // the distinct id, and the real email only ever becomes a person
          // property when the reader ticked consent for it (same checkbox
          // this handler already required before sending the subscribe call).
          try {
            if (window.posthog && window.crypto && window.crypto.subtle) {
              var emailValue = input.value.trim().toLowerCase();
              window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(emailValue)).then(function (buf) {
                var hex = Array.prototype.map.call(new Uint8Array(buf), function (b) {
                  return b.toString(16).padStart(2, '0');
                }).join('').slice(0, 32);
                posthog.identify(hex, consent.checked ? { email: emailValue } : {});
              }).catch(function () {});
            }
          } catch (e) {}
        }
        else { say('error'); button.disabled = false; }
      }).catch(function () { say('error'); button.disabled = false; });
    });
  });

  // ---- buy buttons (drop-in class / jam / combo checkout) ----
  // One handler for every [data-kind] button on the site: the kind, the date (when
  // the button carries one) and the endpoint all come off the button's own data
  // attributes, same pattern as the subscribe form above. A 200 redirects straight to
  // the Stripe-hosted Checkout URL the Worker returns; a 409 means online sales are
  // closed (or, for jam/combo today, not configured yet) and the reader pays at the
  // door instead, so the button stays disabled and the status line carries the door
  // link rather than a dead button sitting next to a message that already answered it.
  document.querySelectorAll('[data-kind]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var wrap = btn.closest('.buy-button');
      var status = wrap ? wrap.querySelector('.buy-status') : null;
      var say = function (text) { if (status) status.textContent = text; };
      var kind = btn.getAttribute('data-kind');
      var eventDate = btn.getAttribute('data-event-date');
      var payload = { kind: kind };
      if (eventDate) payload.event_date = eventDate;
      try {
        if (window.posthog) posthog.capture('buy_click', { kind: kind, event_date: eventDate || null });
      } catch (e) {}
      // Loading state lives on the button itself (spinner over the label, width
      // unchanged); data-sending is read out to screen readers instead of shown.
      var setLoading = function (on) {
        btn.classList.toggle('is-loading', on);
        if (on) { btn.setAttribute('aria-busy', 'true'); btn.setAttribute('aria-label', btn.getAttribute('data-sending') || ''); }
        else { btn.removeAttribute('aria-busy'); btn.removeAttribute('aria-label'); }
      };
      btn.disabled = true;
      say('');
      setLoading(true);
      fetch(btn.getAttribute('data-endpoint'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      }).then(function (response) {
        return response.json().catch(function () { return {}; }).then(function (data) {
          return { status: response.status, ok: response.ok, data: data };
        });
      }).then(function (result) {
        if (result.ok && result.data && result.data.url) {
          try {
            if (window.posthog) posthog.capture('checkout_started', { kind: kind });
          } catch (e) {}
          window.location.href = result.data.url;
          return;
        }
        if (result.status === 409 && result.data && result.data.closed) {
          if (status) {
            status.textContent = '';
            var msg = document.createTextNode((btn.getAttribute('data-closed') || '') + ' ');
            var link = document.createElement('a');
            link.href = result.data.door_url || '/pay';
            link.textContent = 'Pay at the door';
            link.addEventListener('click', function () {
              try {
                if (window.posthog) posthog.capture('pay_door_redirect', { from: 'checkout_closed' });
              } catch (e) {}
            });
            status.appendChild(msg);
            status.appendChild(link);
          }
          setLoading(false);
          return; // sale's closed: the button stays disabled, the message explains why
        }
        setLoading(false);
        say(btn.getAttribute('data-error') || '');
        btn.disabled = false;
      }).catch(function () {
        setLoading(false);
        say(btn.getAttribute('data-error') || '');
        btn.disabled = false;
      });
    });
  });
  // Back from Stripe via the browser's back button restores the page from bfcache
  // with the button still spinning; reset it.
  window.addEventListener('pageshow', function (e) {
    if (!e.persisted) return;
    document.querySelectorAll('.buy-button .btn.is-loading').forEach(function (b) {
      b.classList.remove('is-loading'); b.removeAttribute('aria-busy'); b.removeAttribute('aria-label'); b.disabled = false;
    });
  });

  // ---- /pricing: a plain pageview-adjacent event, not autocapture's job ----
  // Autocapture already logs the pageview; this is the specific named event the
  // funnel (pricing_viewed -> buy_click -> checkout_started -> checkout_completed)
  // is built around, so it exists even if autocapture's shape ever changes.
  if (window.location.pathname === '/pricing') {
    try { if (window.posthog) posthog.capture('pricing_viewed'); } catch (e) {}
  }

  // ---- /pay: fire tracking, then hand off to Stripe ----
  // A plain Cloudflare _redirects rule can't run JS, so it can neither fire
  // pay_door_redirect nor let PostHog attribute whatever UTM params arrived on
  // this URL (e.g. a printed door QR's ?utm_source=poster&utm_medium=qr) before
  // the visitor leaves -- which is the whole reason /pay is a real page instead.
  // The short delay gives the capture call's request a moment to leave before
  // the page unloads; the <meta http-equiv="refresh"> in this page's <head> is
  // the no-JS fallback, slower but still correct.
  if (window.location.pathname === '/pay') {
    try { if (window.posthog) posthog.capture('pay_door_redirect', { from: 'pay_page' }); } catch (e) {}
    setTimeout(function () {
      // Keep in sync with shell.DOOR_PAYMENT_LINK / content_checkout.DOOR_LINK.
      window.location.replace('https://buy.stripe.com/3cIaEX1Oe13Xfxh45v4ow01');
    }, 250);
  }

  // ---- success page: personalise from the checkout redirect's query string ----
  // No ticket ID, no QR - this page works purely off ?kind=, ?event_date= and
  // ?amount=, which is all a redirect from Stripe Checkout can hand it. The
  // server-rendered line above is already a correct generic sentence; this only
  // overwrites it when the params are present and parse cleanly.
  (function () {
    var q = new URLSearchParams(window.location.search);
    var kind = q.get('kind');
    var amount = q.get('amount');
    try {
      if (window.posthog && kind) {
        posthog.capture('checkout_completed', {
          kind: kind,
          amount: amount ? parseInt(amount, 10) : null,
        });
      }
    } catch (e) {}

    var line = document.getElementById('mci-success-line');
    if (!line) return;
    try {
      var date = q.get('event_date');
      if (!date || !/^\\d{4}-\\d{2}-\\d{2}$/.test(date)) return;
      var parts = date.split('-');
      var d = new Date(+parts[0], +parts[1] - 1, +parts[2]);
      if (isNaN(d.getTime())) return;
      var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December'];
      var when = months[d.getMonth()] + ' ' + d.getDate();
      var what = kind === 'jam' ? 'the 7:45 PM jam'
        : kind === 'combo' ? 'the full evening, class at 7:00 then jam at 7:45'
        : 'the 7:00 PM class';
      line.textContent = 'See you Friday, ' + when + ', for ' + what + '.';
    } catch (e) {}
  })();

  // ---- resubscribe notice ----
  // The Worker's confirmation link redirects to /?resubscribed=1; say so in one line.
  (function () {
    try {
      if (!/[?&]resubscribed=1(&|$)/.test(window.location.search)) return;
      var main = document.getElementById('main');
      if (!main) return;
      var es = (document.documentElement.lang || '').slice(0, 2) === 'es';
      var note = document.createElement('p');
      note.className = 'resubscribe-note';
      note.setAttribute('role', 'status');
      note.textContent = es
        ? 'Volviste a la lista. Si tu código sigue sin usar, va en tu correo.'
        : 'You are back on the list. If your code is still unused, it is in your email.';
      main.insertBefore(note, main.firstChild);
    } catch (e) {}
  })();

  // ---- newsletter popup ----
  // Shown 5 seconds after load. Closing it hides it for 7 days (timestamp in
  // mci_popup_closed_at); a successful subscribe on any form (shared handler above) sets mci_popup_subscribed and it never
  // shows again. Every read/write is wrapped so private browsing or blocked storage
  // degrades to "never shows" rather than breaking the page.
  (function () {
    var modal = document.getElementById('mci-popup');
    if (!modal) return;
    var card = modal.querySelector('.mci-popup');
    var closeBtn = modal.querySelector('.mci-popup-close');
    var closedKey = 'mci_popup_closed_at';
    var subscribedKey = 'mci_popup_subscribed';
    var WEEK_MS = 7 * 24 * 60 * 60 * 1000;
    var lastFocus = null;

    var seen = function () {
      try {
        if (localStorage.getItem(subscribedKey) === '1') return true;
        var t = parseInt(localStorage.getItem(closedKey), 10);
        return !isNaN(t) && Date.now() - t < WEEK_MS;
      } catch (e) { return true; }
    };
    var markClosed = function () {
      try { localStorage.setItem(closedKey, String(Date.now())); } catch (e) {}
    };

    var focusables = function () {
      return Array.prototype.slice.call(
        card.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])')
      );
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
      lastFocus = document.activeElement;
      modal.classList.add('is-open');
      document.addEventListener('keydown', onKeydown, true);
      var f = focusables();
      if (f.length) f[0].focus();
      try { if (window.posthog) posthog.capture('newsletter_popup_shown'); } catch (e) {}
    };

    function closeModal() {
      modal.classList.remove('is-open');
      document.removeEventListener('keydown', onKeydown, true);
      markClosed();
      try { if (window.posthog) posthog.capture('newsletter_popup_closed'); } catch (e) {}
      try {
        if (lastFocus && lastFocus.focus) lastFocus.focus();
        else document.body.focus();
      } catch (e) {}
    }

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    var noThanks = modal.querySelector('.mci-popup-nothanks');
    if (noThanks) noThanks.addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });

    if (!seen()) {
      setTimeout(function () { if (!seen()) openModal(); }, 5000);
    }
  })();
})();
</script>
</body>
</html>"""


def bg_youtube_embed(video_id):
    src = (
        f"https://www.youtube-nocookie.com/embed/{video_id}"
        "?autoplay=1&mute=1&controls=0&loop=1&playlist=" + video_id
        + "&modestbranding=1&playsinline=1&rel=0&iv_load_policy=3&disablekb=1&fs=0"
    )
    return f"""<div id="bgwrap" aria-hidden="true">
  <iframe id="video" src="{src}" title="" tabindex="-1"
    allow="autoplay; encrypted-media" frameborder="0"></iframe>
</div>"""


def page(title, description, path, body, *, jsonld="", bg_video=None, bg_youtube=None,
         og_type="website", lang="en", extra_head=""):
    """Assemble a full HTML document.

    lang: the locale this page is written in. It selects <html lang>, the reciprocal
    alternates, the switcher, the nav labels and the footer.

    extra_head: raw HTML appended into <head>, before the PostHog snippet and the
    JSON-LD. The only user today is /pay's no-JS meta-refresh fallback.
    """
    return (
        head(title, description, path, jsonld=jsonld, og_type=og_type, lang=lang, extra_head=extra_head)
        + "\n<body>\n"
        + f'<a class="skip-link" href="#main">{SKIP_LABELS.get(lang, SKIP_LABELS["en"])}</a>\n'
        + '<div id="grain" aria-hidden="true"></div>\n'
        + '<div class="page">\n'
        + header(path, lang)
        + "\n<main id=\"main\">\n"
        + body
        + "\n</main>\n"
        + SCROLL_CONTROLS
        + "\n"
        + footer(lang, path=path)
        + "\n</div>\n"
        + newsletter_popup(lang, path)
        + "\n"
        + body_script()
    )


# ---------- reusable content blocks ----------

def answer(text, label="Short answer"):
    return f'<div class="answer"><div class="label">{label}</div><p>{text}</p></div>'


def cite_block(text, label="Cite this page"):
    return f'<div class="cite"><div class="label">{label}</div><p>{text}</p></div>'


def band(title, text, buttons, band_id=None):
    bid = f' id="{band_id}"' if band_id else ""
    btns = "".join(
        f'<a class="btn {style}" href="{href}">{label}</a>' for label, href, style in buttons
    )
    return (
        f'<div class="band"{bid}><h2>{title}</h2><p>{text}</p>'
        f'<div class="btn-row">{btns}</div></div>'
    )


def facts(rows, caption=None):
    trs = "".join(
        f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows
    )
    return f'<table class="facts">{trs}</table>'


def cards(items):
    out = []
    for tag, title, text, href in items:
        out.append(
            f'<a class="card" href="{href}"><span class="tag">{tag}</span>'
            f"<h3>{title}</h3><p>{text}</p></a>"
        )
    return f'<div class="grid">{"".join(out)}</div>'
