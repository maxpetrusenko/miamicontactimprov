def home():
    ig_embeds = "".join(
        f'<blockquote class="instagram-media" data-instgrm-permalink="{u}" '
        f'data-instgrm-version="14"><a href="{u}">Ver esta publicación en Instagram</a></blockquote>'
        for u in cm.IG_POSTS
    )
    body = f"""
<div class="mci-hero" id="mci-hero">
  <div class="mci-hero-copy">
    <h1 class="mci-h">
      <span id="mci-w1">MUÉVETE.</span>
      <span id="mci-w2">ESCUCHA.</span>
      <span id="mci-w3" class="accent">IMPROVISA.</span>
    </h1>
    <p class="lede">Una jam semanal de contact improv en Miami &mdash; donde la danza se encuentra con el contacto, la confianza y el juego. No hace falta experiencia, solo un cuerpo con curiosidad.</p>
    <div class="btn-row">
      <a class="btn primary" href="{R_JAMS}">Ver próximas jams &nbsp;&rarr;</a>
      <a class="btn secondary" href="{cm.IG}" target="_blank" rel="noopener">@miamicontactimprov</a>
    </div>
  </div>
  <div class="mci-hero-stage">
    <div class="mci-layer mci-disc" id="mci-disc" aria-hidden="true"></div>
    <div class="mci-layer mci-ring" id="mci-ring" aria-hidden="true"></div>
    <div class="mci-layer mci-dot-1" id="mci-dot1" aria-hidden="true"></div>
    <div class="mci-layer mci-dot-2" id="mci-dot2" aria-hidden="true"></div>
    <div class="mci-logo-float" id="mci-logo-float">
      <img id="mci-logo" class="mci-hero-photo" src="{cm.IMG}/p3.jpg" alt="Dos bailarines entrelazados en un abrazo de contact improv, en blanco y negro">
    </div>
    <a class="mci-layer mci-stamp" id="mci-stamp" href="{R_FRIDAY}" aria-label="Primera jam, 2 de octubre, viernes 7 PM">
      <span class="small">Primera jam</span>
      <span class="big mci-h">2 OCT</span>
      <span class="small">Vie &middot; 7 PM</span>
    </a>
    <div class="mci-layer mci-chip mci-chip-1" id="mci-chip1">Viernes &middot; 7&ndash;9 PM</div>
    <div class="mci-layer mci-chip mci-chip-2" id="mci-chip2">Clase + Jam abierta</div>
  </div>
</div>

<div class="mci-panel-wrap">
  <div class="mci-panel">
    <div><p class="label mci-h">CUÁNDO</p><p>Todos los viernes, desde el 2 oct<br>7:00 &ndash; 9:00 PM<br>Clase, luego Jam abierta</p></div>
    <div><p class="label mci-h">DÓNDE</p><p>Inner Motion Dance Studio<br>216 NE 1st Ave, Hallandale Beach, FL</p></div>
    <div><p class="label mci-h">QUIÉN</p><p>Todos los niveles, todos los cuerpos.<br>Ven solo/a o con quien quieras.</p></div>
  </div>
</div>

<div class="mci-block mci-reveal">
  <p class="mci-eyebrow">Qué es</p>
  <h2 class="mci-h">UNA DANZA HECHA DE PESO, CONTACTO Y MOMENTO COMPARTIDO.</h2>
  <p class="body">El contact improv es una danza improvisada que nace del contacto físico &mdash; dos o más cuerpos explorando juntos el equilibrio, el peso compartido y el momento, instante a instante. Sin coreografía, sin espejos, sin presión de actuar.</p>
  <div class="mci-cards">
    <div class="mci-mini"><p class="t mci-h">7:00 &middot; CLASE</p><p>Calentamiento guiado y herramientas &mdash; rodar, compartir peso, caer sin hacerse daño.</p></div>
    <div class="mci-mini"><p class="t mci-h">7:45 &middot; JAM ABIERTA</p><p>Danza libre. Entra, siéntate, mira &mdash; todo es bienvenido.</p></div>
    <div class="mci-mini"><p class="t mci-h">$20 &ndash; $50</p><p>Escala móvil &mdash; paga lo que puedas. Ropa cómoda, sin zapatos.</p></div>
  </div>
  <div class="mci-actions">
    <a class="mci-textlink" href="https://www.youtube.com/watch?v=q4wUEiHowSU" target="_blank" rel="noopener">&#9654; Ver: qué es el contact improv</a>
  </div>
</div>

<div class="mci-photos mci-reveal">
  <div class="mci-tile"><img src="{cm.IMG}/p1.jpg" alt="Dos bailarines en un apoyo inclinado, en blanco y negro" loading="lazy"><span class="chip">JAM DE LOS VIERNES</span></div>
  <div class="mci-tile"><img src="{cm.IMG}/p4.jpg" alt="Una bailarina girando, larga exposición en blanco y negro" loading="lazy"><span class="chip">CLASE</span></div>
  <div class="mci-tile"><img src="{cm.IMG}/p3.jpg" alt="Dos bailarines entrelazados en la penumbra, en blanco y negro" loading="lazy"><span class="chip">JAM ABIERTA</span></div>
  <div class="mci-tile"><img src="{cm.IMG}/p7.jpg" alt="Una mano que se extiende bajo una luz suave" loading="lazy"><span class="chip">COMUNIDAD</span></div>
</div>

<div class="mci-ig mci-reveal">
  <div class="mci-ig-head">
    <h2 class="mci-h">EN INSTAGRAM</h2>
    <a href="{cm.IG}" target="_blank" rel="noopener">@miamicontactimprov &rarr;</a>
  </div>
  <div class="ig-embeds">{ig_embeds}</div>
  <script async src="https://www.instagram.com/embed.js"></script>
</div>

{cm._gallery("band-home.jpg", "Dos bailarines moviéndose juntos en larga exposición, en blanco y negro", "¿NUEVO POR AQUÍ? VEN COMO ERES.", "Síguenos en Instagram para recordatorios de jams, fotos y novedades.", f'<a class="mci-pill terracotta" href="{cm.IG}" target="_blank" rel="noopener">{cm.IG_GLYPH}<span>@miamicontactimprov</span></a>', tall=True)}
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.website("es"),
        schema.webpage(
            R_HOME,
            "Improvisación de Contacto en Miami | Miami Contact Improv",
            "Una jam semanal de contact improv en Miami: clase y luego jam abierta todos los viernes, de 7 a 9 PM, en Inner Motion Dance Studio. Todos los niveles.",
            lang="es",
        ),
        {
            "@type": "Place",
            "@id": schema.SITE + "/#place",
            "name": "Miami, Florida",
            "address": {"@type": "PostalAddress", "addressLocality": "Miami", "addressRegion": "FL", "addressCountry": "US"},
            "geo": {"@type": "GeoCoordinates", "latitude": 25.7617, "longitude": -80.1918},
        },
        listings.friday_jam_event(),
    )
    return page(
        "Contact Improv en Miami | Jam semanal y clase",
        "Una jam semanal de contact improv en Miami: clase y luego jam abierta todos los viernes, de 7 a 9 PM, en Inner Motion Dance Studio. Sin experiencia previa.",
        R_HOME,
        body,
        lang="es",
        jsonld=jsonld,
    )
