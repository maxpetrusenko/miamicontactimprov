"""Spanish pages: the core set, translated.

Every page here is a translation of an English page on this site, and it may not claim
anything the English page does not claim. Three rules govern this file:

1. **No new fact.** Nothing is added in Spanish that is absent in English. The Spanish
   pages are shorter than their English counterparts in places, and that is the correct
   direction to be wrong in.
2. **Listing data is quoted, not translated.** Session names, modalities, venues,
   schedules and prices are reproduced verbatim from build/listings.py, in the language
   the organiser published them in, together with the ISO date the source was checked.
   Translating a quoted schedule would be inventing a quote. Only the field LABELS are
   Spanish, and the page says so in prosa.
3. **One term, used consistently.** The form is "Improvisación de Contacto (IC)", a jam
   is a "jam" (the loanword every Spanish-speaking CI community uses), and "contact
   improvisation" is named as an alternate on first use. The choice is recorded in
   docs/i18n.md.

Entity disambiguation: the Spanish sentence lives in build/schema.py as
DISAMBIGUATION_BY_LANG["es"], is emitted on every Spanish Organization node, and is
asserted by tools/gate.py. It is never written out by hand here.
"""

import html

from shell import (
    LAST_CHECKED_BY_LANG,
    LAST_CHECKED_ISO,
    answer,
    band,
    cards,
    cite_block,
    facts,
    page,
)
import listings
import schema
import videos_data
import content_marketing as cm

# The Spanish routes, mirroring build/locales.py. Kept as literals here so a link in
# Spanish prose is visible where it is written; tools/gate.py fails the build if any of
# them stops resolving to a file.
R_HOME = "/es/"
R_WHATIS = "/es/que-es-la-improvisacion-de-contacto"
R_JAMS = "/es/jams"
R_FRIDAY = "/es/jam-de-los-viernes"
R_FIRST = "/es/tu-primera-jam"
R_LIST = "/es/jams-miami-dade-broward"
R_FAQ = "/es/preguntas-frecuentes"
R_SAFETY = "/es/seguridad-y-consentimiento"
R_MIAMI = "/es/miami"
R_CLASSES = "/es/clases"
R_DIRECTORY = "/es/directorio"
R_GLOSSARY = "/es/glosario"
R_HISTORY = "/es/historia"
R_VIDEOS = "/es/videos"
R_KEEP = "/es/seguir-practicando"
R_ABOUT = "/es/acerca-de"
R_SUBMIT = "/es/acerca-de#submit"

SHORT = "Respuesta breve"
CITE = "Cita esta página"

# Spanish labels for the listing tables. Values are quoted verbatim in the organiser's own
# language (docs/i18n.md rule 2); only these labels are translated.
L_PREFIX = "Leído en"
L_CHECKED = "Comprobado el"
L_VERIFIED_ON = "Comprobado el"

LIST_VALUE_NOTE = (
    "Los datos de cada sesión (nombre, modalidad, lugar, horario y precio) se reproducen "
    "tal como los publica quien la organiza, en su idioma original: traducirlos sería "
    "inventar la cita. Lo que sí está en español son las etiquetas y la explicación."
)


# ------------------------------------------------------- session block (Spanish)

def _field_rows(name):
    """The labelled facts for one session, read from the same table the English page uses."""
    for row in listings.SESSIONS:
        if row[0] != name:
            continue
        _n, modality, city, venue, schedule, cost, url, verified, _note = row
        organiser = listings.SESSION_ORGANISERS.get(name, ("Sin registrar", ""))
        return [
            ("Organiza", html.escape(organiser[0])),
            ("Modalidad", html.escape(modality)),
            ("Dónde", f"{html.escape(venue)} ({html.escape(city)})"),
            ("Cuándo", html.escape(schedule)),
            ("Precio", html.escape(cost)),
        ]
    raise KeyError(name)


def _session_items():
    items = []
    for name, _modality, _city, _venue, _schedule, _cost, url, verified, note in listings.SESSIONS:
        items.append(f"""<li>
  <h3>{html.escape(name)}</h3>
  {facts(_field_rows(name))}
  <p>{html.escape(note)}</p>
  <p>Leído en <a href="{html.escape(url)}" rel="noopener nofollow">{html.escape(url)}</a></p>
  <p><strong>Comprobado el {html.escape(verified)}</strong></p>
</li>""")
    return "".join(items)


def _sessions_block():
    """The verified sessions, or the honest empty state. Never a placeholder."""
    if not listings.SESSIONS:
        return (
            '<div class="prose"><h2>Qué se está practicando en Miami-Dade y Broward</h2>'
            "<p>Ahora mismo, nada. Esta página retira una entrada en lugar de dejar una "
            "desactualizada, así que una lista vacía significa una lista verificada vacía y no "
            "una ciudad vacía. Los estudios y las personas que organizan que aparecen en el "
            f'<a href="{R_DIRECTORY}">directorio</a> son donde '
            "está realmente la respuesta.</p></div>"
        )
    return (
        '<div class="prose"><h2>Qué se está practicando en Miami-Dade y Broward</h2>'
        f"<p>{len(listings.SESSIONS)} entradas. Cada una nombra a quien la organiza, dónde es, "
        "cuándo es, cuánto cuesta y qué tipo de práctica es en realidad, y cada una lleva la "
        "fecha en que se abrió y se leyó su fuente. Aparecen en el orden en que se verificaron. "
        "Esta página no clasifica nada: ninguna entrada está pagada y ninguna se recomienda por "
        "encima de otra. Una de ellas, la jam de los viernes en Miami, la organiza quien "
        "mantiene este sitio; su entrada lo dice y se le aplican las mismas reglas que al resto.</p>"
        f'<p>{LIST_VALUE_NOTE}</p>'
        f'<ul class="dir-list">{_session_items()}</ul></div>'
    )


def _sessions_for_stage():
    """The session block for the stage pages, which carry no Event schema."""
    return _sessions_block()


# ---------------------------------------------------------------- home
def home():
    ig_embeds = "".join(cm.ig_embed(u) for u in cm.IG_POSTS)
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
      <img id="mci-logo" class="mci-hero-photo" src="{cm.IMG}/c7.jpg" alt="Una mano que se extiende, bajo una luz cálida y suave">
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
  </div>
  <div class="ig-embeds">{ig_embeds}</div>
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



# ---------------------------------------------------------------- what is CI
WHATIS_FAQ_ES = [
    ("¿Qué es la Improvisación de Contacto?",
     "La Improvisación de Contacto es una forma de danza improvisada en pareja que comenzó en 1972 con el bailarín y coreógrafo estadounidense Steve Paxton. Dos personas mantienen un punto de contacto físico en movimiento, normalmente la espalda o los hombros, y comparten peso siguiendo la gravedad, el momento y el impulso en lugar de una secuencia fija de pasos."),
    ("¿Necesito experiencia en danza para empezar?",
     "No. La Improvisación de Contacto se creó en parte para ampliar quién podía ser intérprete, y las clases para principiantes no presuponen formación previa. Lo que ayuda es estar dispuesto a caer, a estar cerca de otra persona y a decir no."),
    ("¿Es sexual la Improvisación de Contacto?",
     "No. La práctica se construye sobre el peso compartido y la escucha física, y el consentimiento se trata como continuo y revocable. La mayoría de las jams lo dicen explícitamente antes de que empiece el baile. El contacto forma parte de la forma; no es una vía hacia otra cosa, y quien lo trata así está rompiendo la forma en lugar de expresarla."),
    ("¿Qué pasa en una jam?",
     "La gente llega, calienta, baila con una o varias personas, descansa en el borde y se va. No hay profesor y normalmente hay poca o ninguna música. Muchas jams abren con un círculo breve en el que se comparten los límites y los avisos."),
    ("¿Cómo se baila sin hacerse daño?",
     "Manteniendo el contacto continuo, dejando que el suelo soporte todo el peso que pueda, rodando en lugar de bloquearse y manteniendo los pies disponibles para aterrizar. Las caídas suelen resolverse como salidas rodando hacia abajo, no como frenazos. Muchas jams mantienen a una o dos personas fuera del baile, haciendo spotting."),
    ("¿Cuál es la diferencia entre una jam, una clase y un taller?",
     "Una clase enseña una habilidad en una sesión secuenciada. Un taller concentra un tema durante horas o días. Una jam es práctica social sin guía: la sala es la enseñanza. Las tres existen en la misma escena y a menudo en el mismo estudio."),
    ("¿Existe un organismo que rija la Improvisación de Contacto?",
     "No. En 1975 un grupo de bailarines que giraba con Steve Paxton consideró registrar el término como marca y establecer una certificación de profesorado, sobre todo por preocupación por la seguridad a medida que la forma se extendía. Rechazaron ambas cosas y fundaron un boletín, que se convirtió en la revista Contact Quarterly. Desde entonces no ha existido ningún organismo que la licencie."),
    ("¿Por qué no hay música en algunas jams?",
     "Porque escuchar el peso de tu pareja forma parte de la práctica, y la música tapa parte de la información con la que funciona el baile. Muchas jams no usan música, o usan una sola pieza ambiental suave, y algunas cuentan con músicos en vivo."),
]


def what_is():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in WHATIS_FAQ_ES)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">La forma</p>
    <h1>¿Qué es la Improvisación de Contacto?</h1>
    <p class="lede">Una danza en pareja que no se puede ensayar, construida con peso compartido, un punto de contacto que rueda y la disposición a caer.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("La Improvisación de Contacto (IC), conocida en inglés como <em>contact improvisation</em> o <em>CI</em>, es una forma de danza en pareja e improvisada desarrollada por el bailarín y coreógrafo estadounidense Steve Paxton en 1972, en la que dos o más personas mantienen un punto de contacto físico en movimiento y exploran el intercambio de peso a través de la gravedad, el momento, la inercia y el tacto. No tiene programa fijo, ni organismo que la licencie, ni requiere formación previa en danza.", SHORT)}
    <div class="prose">
      <p>El baile suele empezar antes de empezar. Las personas se quedan quietas un minuto o dos primero, notando los pequeños ajustes continuos que hace el cuerpo para mantenerse de pie. Paxton llamó a esto la <strong>small dance</strong> (la pequeña danza), y es la razón de que la IC tienda a parecer escucha y no interpretación.</p>
      <p>A partir de ahí el contacto empieza en algún sitio, a menudo una mano o un hombro, y la pareja se mueve. El peso se desplaza. El apoyo de una persona se convierte en el suelo de la otra. Un levantamiento ocurre porque los dos cuerpos llegaron a la disposición correcta, no porque alguien lo planeara. Cuando sale mal, la pareja rueda hacia abajo y sale de ahí, y el baile continúa desde donde caiga.</p>
      <blockquote>
        Las exigencias de la forma dictan un modo de movimiento relajado, constantemente atento y preparado, y que fluye.
        <cite>Steve Paxton, creador de la Improvisación de Contacto</cite>
      </blockquote>
      <p>Paxton describió la relación de la forma con otros dúos con las palabras de una de sus primeras practicantes. Nancy Stark Smith, que participó en las primeras funciones y editó la revista que nació de la forma, escribió que &ldquo;se parece a otras formas de dúo conocidas, como el abrazo, la lucha, el surf, las artes marciales y el Jitterbug, y abarca un rango amplio de movimiento, desde la quietud hasta lo más atlético&rdquo;. Ese rango es real. Una sola noche puede contener cinco minutos de casi quietud y un levantamiento completamente en el aire.</p>
      <h2>Tres cosas que la hacen distinta</h2>
      <p><strong>No es coreografía.</strong> Nada está fijado de antemano, y repetir algo es una elección y no una obligación. El baile se hace en el momento por dos personas que solo pueden saber qué viene después a medida que ocurre.</p>
      <p><strong>El peso es real.</strong> Toda la masa de tu pareja puede pasar a tu espalda, tu cadera o tu hombro, que es lo que hace físicamente posibles los levantamientos y también lo que convierte el spotting y las salidas seguras en parte de la forma y no en un añadido.</p>
      <p><strong>El consentimiento es una habilidad técnica, no una advertencia legal.</strong> Como el tacto es el medio, la capacidad de rechazar, pausar o irse a mitad del baile se entrena junto con el movimiento. Un baile del que no puedes retirarte no es IC bien hecha; es IC que no se está haciendo.</p>
      <h2>Lo que no es</h2>
      <p>La Improvisación de Contacto no es acrobacia en pareja para un público, aunque quien baila con experiencia pueda hacer que lo parezca. No es una sesión de terapia, aunque mucha gente la encuentre reparadora. No es práctica sexual, y las jams defienden colectivamente esa distinción. Y no es un único método correcto: como la forma nunca se registró como marca ni se certificó, los estilos de enseñanza difieren mucho entre quien organiza y entre ciudades.</p>
      <h2>Cómo llegó a Florida</h2>
      <p>La IC se extendió por giras, enseñanza y un boletín en papel, no por una organización, y por eso la mayoría de las ciudades desarrolló su escena sin dirección central. Miami no es una excepción: aquí la práctica pasa por profesores individuales, alquileres de estudio, parques y la comunidad de danza y movimiento del sur de Florida, y no por una institución única. <a href="{R_WHATIS}">Esta página</a> describe lo que se sabe hoy, y la <a href="{R_MIAMI}">página de Miami</a> traza el mapa de lo que se ha podido verificar.</p>
      <h2>Preguntas que la gente hace de verdad</h2>
      {faq_html}
    </div>
    {band("¿Listo para probarlo?", "Lee qué pasa en una jam antes de ir, y luego busca una cerca de ti.", [("Jams en Miami", R_JAMS, "primary"), ("Tu primera jam, paso a paso", R_FIRST, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>¿Qué es la Improvisación de Contacto?</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/que-es-la-improvisacion-de-contacto", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_WHATIS,
            "¿Qué es la Improvisación de Contacto?",
            "Qué es la Improvisación de Contacto: historia, principios, qué es una jam y por qué no tiene organismo que la licencie. Qué pasa en los primeros minutos.",
            about=[{"@id": schema.SITE + "/#place"}, {"@id": schema.SITE + "/es/glosario#terms"}],
            lang="es",
        ),
        schema.breadcrumb(R_WHATIS, "¿Qué es la Improvisación de Contacto?", lang="es"),
        schema.faq(WHATIS_FAQ_ES, lang="es"),
    )
    return page(
        "¿Qué es la Improvisación de Contacto? [Guía]",
        "La Improvisación de Contacto explicada: una danza en pareja de 1972 construida sobre el peso compartido y un punto de contacto rodante. Qué es una jam y cómo empezar.",
        R_WHATIS,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- jams
JAMS_FAQ_ES = [
    ("¿Qué es una jam de Improvisación de Contacto?",
     "Una jam es una sesión abierta y sin guía de Improvisación de Contacto. No hay profesor y hay poca o ninguna música. La gente llega, baila con una o varias personas o sola, descansa en el borde y se va cuando termina. Es la forma social básica de la Improvisación de Contacto."),
    ("¿Cuál es la diferencia entre una jam abierta y una cerrada?",
     "Una jam abierta acepta a cualquiera, también a quien viene por primera vez. Una jam cerrada, para gente con experiencia o avanzada, presupone práctica previa, normalmente porque el baile va rápido y se apoya en hábitos de seguridad compartidos. Las listas deberían decir cuál es cuál."),
    ("¿Cómo encuentro una jam en Miami?",
     "La escena de IC de Miami la organizan personas y no una institución, así que las sesiones aparecen en calendarios de estudios, publicaciones en redes y de boca en boca, no en una taquilla central. Esta página lista las sesiones que hemos confirmado, y el directorio recoge los estudios y a quienes organizan y merece la pena preguntar."),
    ("¿Hay una jam hoy en Miami?",
     "Este sitio no publica un calendario en vivo, así que no puede responder eso con fiabilidad. La fuente más actual es la propia lista o cuenta de quien organiza. Si llevas una sesión recurrente y nos dices el horario, la añadimos."),
    ("¿Cuestan dinero las jams?",
     "Normalmente una entrada pequeña o una donación para cubrir la sala, fijada por quien organiza. Existen jams comunitarias gratuitas. A nadie debería negársele una primera jam sin decirle antes lo que cuesta."),
]


def jams():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in JAMS_FAQ_ES)
    sessions = _sessions_block()
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Práctica abierta</p>
    <h1>Jams: la sala es la maestra.</h1>
    <p class="lede">Una jam es donde vive realmente la Improvisación de Contacto. Sin instructor, sin música fija, sin obligación de bailar con nadie. Llegas, escuchas, te mueves, te vas.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("Una jam de Improvisación de Contacto (IC) es una sesión abierta y sin guía en la que varias personas practican IC juntas. No hay profesor y normalmente no hay música. Quien participa llega y se va con libertad, baila con quien quiera, se sienta en el borde a descansar y mirar, y para cuando quiere. Las jams son la forma principal en que se practica esta danza en el mundo, y en Miami conviven con un número pequeño de clases recurrentes y con campamentos de festival.", SHORT)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sessions}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Cómo comprobar que una entrada sigue vigente</h2>
    <div class="prose">
      <p>Miami no tiene un calendario central de IC, así que &laquo;¿hay jam hoy?&raquo; no tiene una respuesta fija y una página como esta queda desactualizada en el momento en que cambia una sala o un horario. Cada sesión de arriba lleva la fecha en que se abrió y se leyó su fuente; las entradas de terceros se volvieron a comprobar por última vez el <strong>{LAST_CHECKED_BY_LANG['es']}</strong>. Trata una fecha antigua como una pista que hay que comprobar, no como un hecho.</p>
      <p>Tres cosas lo resuelven. Abre la propia página o cuenta de quien organiza, que es la única fuente con autoridad y está enlazada en cada entrada. Busca una fecha propia: una sesión recurrente cuya fuente no se ha actualizado en meses normalmente ha parado, y una lista sin fecha no es prueba de nada. Y luego pregunta, por mensaje directo, antes de desplazarte a una sesión: quienes organizan contestan, y prefieren decírtelo a que llegues a una puerta cerrada.</p>
      <p>Lo que esta página no hará es adivinar. Una lista desactualizada publicada como actual es peor que una vacía, así que una entrada se retira cuando su fuente calla, y una sesión que nadie pudo verificar nunca se presenta como en marcha.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Cómo suele funcionar una jam</h2>
    <div class="prose">
      <p>Los formatos varían, pero la mayoría de las jams sigue una forma reconocible.</p>
      <p><strong>La llegada.</strong> La gente se cambia, estira, se saluda y busca un sitio en el suelo. Quien hace de anfitrión abre un círculo.</p>
      <p><strong>El círculo.</strong> Dos o tres minutos. Quien acoge enuncia el protocolo: el consentimiento es continuo, puedes rechazar cualquier cosa, el borde es para descansar, y aquí está el agua. Cualquiera puede añadir un límite o anunciar algo, como una lesión o que se va antes de tiempo.</p>
      <p><strong>El calentamiento.</strong> A menudo una secuencia guiada breve y luego unos minutos de <strong>small dance</strong>: quedarse de pie y seguir los microajustes del cuerpo. Si hay alguien enseñando, puede ofrecer veinte minutos de material antes de que empiece el baile abierto.</p>
      <p><strong>La jam abierta.</strong> El tramo largo del medio. Los bailes empiezan con una mirada, una mano, o simplemente porque ya estáis los dos moviéndoos. Terminan cuando cualquiera de las dos personas para. Descansar en el borde entre baile y baile es lo normal.</p>
      <p><strong>El cierre.</strong> Algunas jams acaban con un círculo, un momento de quietud, o nada en absoluto. La gente se va dispersando.</p>
      <h2>Qué se espera de ti</h2>
      <ul>
        <li>Mantén el punto de contacto en singular. Dos manos y una cadera a la vez es forcejeo, no IC.</li>
        <li>Mantén tus propios pies disponibles. Si no puedes aterrizar, no puedes recibir peso con seguridad.</li>
        <li>Rueda al caer en lugar de bloquear. El suelo es la pareja más grande de la sala.</li>
        <li>Di no cuando quieras decir no, y acepta un no sin preguntar por qué.</li>
        <li>Sal del baile cuando termina, incluso a mitad de frase, sin disculparte.</li>
        <li>No enseñes si no te lo han pedido. Una jam no es una clase.</li>
      </ul>
      <h2>Qué llevar</h2>
      {facts([
        ("Ropa", "Holgada y opaca, que cubra espalda, hombros y rodillas. Sin cremalleras, hebillas ni costuras ásperas"),
        ("Pies", "Descalzos o con calcetines blandos antideslizantes. Sin calzado en la sala"),
        ("Agua", "Una botella llena. En Miami el suelo es caluroso y húmedo"),
        ("Toalla", "Una. La vas a necesitar"),
        ("Joyas", "Fuera. Anillos, relojes y collares enganchan y cortan"),
        ("Móvil", "Silenciado, boca abajo, fuera del suelo o en el borde"),
      ])}
      <h2>Spotting y seguridad</h2>
      <p>Las sesiones donde circulan levantamientos suelen mantener a una o dos personas fuera del baile como <strong>spotters</strong>: cerca, con las manos libres, atentas a una caída que haya que frenar. Es uno de los pocos papeles técnicos y no sociales de una jam, y normalmente quien baila por primera vez puede aprenderlo. Si no tienes claro que puedas recibir el peso de alguien con seguridad, no puedes, y decirlo es la respuesta correcta.</p>
      <h2>Antes y después de tu primera visita</h2>
      <p>Qué pasa de verdad cuando entras &mdash; la llegada, el círculo de apertura, los primeros diez minutos de baile, las frases que puedes decir cuando quieres parar y cuándo irte &mdash; está en <a href="{R_FIRST}">tu primera jam, paso a paso</a>. Qué hacer en las semanas siguientes, incluidas las semanas en que no hay nada, está en <a href="{R_KEEP}">seguir practicando</a>.</p>
      <h2>Preguntas sobre las jams</h2>
      {faq_html}
    </div>
    {band("¿Organizas una jam?", "Dinos el horario, la sala y la entrada y la publicamos. Esta página existe para que la corrija quien está de verdad en la sala.", [("Publicar una jam", R_SUBMIT, "primary"), ("Buscar clase", R_CLASSES, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Jams de Improvisación de Contacto en Miami</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/jams", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_JAMS,
            "Jams de Improvisación de Contacto en Miami",
            "Qué es una jam de Improvisación de Contacto, cómo suele funcionar una sesión, qué llevar y cómo comprobar que una entrada sigue vigente, con las jams y sesiones de práctica abierta confirmadas en Miami y el sur de Florida.",
            date_modified=LAST_CHECKED_ISO,
            lang="es",
        ),
        schema.breadcrumb(R_JAMS, "Jams", lang="es"),
        schema.faq(JAMS_FAQ_ES, lang="es"),
        schema.item_list(
            R_JAMS,
            "Jams de Improvisación de Contacto verificadas en Miami",
            [(row[0], row[6], row[1]) for row in listings.SESSIONS],
            lang="es",
        ),
    )
    return page(
        "Jams de Improvisación de Contacto en Miami [Guía]",
        "Qué es una jam de Improvisación de Contacto, cómo funciona una sesión, cómo comprobar que una entrada sigue vigente y dónde bailar en Miami.",
        R_JAMS,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- your first jam

def your_first_jam():
    sessions = _sessions_for_stage()
    rank_note = (
        "La modalidad de cada entrada de arriba es la que quien organiza declara sobre su "
        "propia sesión, y cada entrada lleva la fecha en que se abrió y se leyó su fuente; las "
        f"entradas de terceros se volvieron a comprobar el <strong>{LAST_CHECKED_BY_LANG['es']}</strong>. "
        "Esta página no clasifica nada. Las "
        "entradas aparecen en el orden en que se verificaron, ninguna está pagada y este sitio "
        "no recomienda ninguna por encima de otra."
    )
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">La primera vez</p>
    <h1>Tu primera jam de improvisación de contacto, paso a paso.</h1>
    <p class="lede">Nadie en una jam te está evaluando. Llegas, alguien enuncia las reglas, el baile empieza y termina a tu alrededor, y participas tanto o tan poco como quieras.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("Llegas, calientas, y normalmente hay un círculo breve donde quienes sostienen la sala enuncian el protocolo de consentimiento. Después el baile empieza y termina a tu alrededor. No estás obligado a bailar con nadie. Sentarse en el borde toda la sesión es una forma normal de estar en una jam, e irse antes siempre está bien. No hay profesor.", SHORT)}
    <div class="prose">
      <h2>La llegada</h2>
      <p>Llegar antes del círculo de apertura hace la noche más fácil, porque ahí es donde se enuncian las reglas de la sala y donde es más sencillo incluir a quien viene por primera vez. Llegar después normalmente está bien: entra, busca un sitio en el borde y únete cuando estés listo. Nadie lleva lista de asistencia.</p>
      <p>Cámbiate a la ropa con la que vas a bailar, deja la bolsa contra la pared, llena la botella y pasa unos minutos en la sala antes de que empiece nada. Quien organiza espera que la gente llegue sin conocer a nadie. Es el caso normal, no el incómodo.</p>
      <h2>El círculo de apertura</h2>
      <p>La mayoría de las jams empiezan con dos o tres minutos de pie o sentados en círculo. Quien sostiene la sala enuncia el protocolo: el consentimiento es continuo, cualquiera puede rechazar cualquier cosa sin dar motivos, el borde es para descansar, nadie enseña si no se lo han pedido y a nadie se le graba sin su acuerdo. Cualquiera en el círculo puede añadir un límite o un aviso.</p>
      <p>Las sesiones que merecen tu tiempo enuncian su protocolo en voz alta al principio de cada sesión. Una jam sin círculo y sin protocolo declarado te está diciendo algo sobre esa sala.</p>
      <h2>Tus primeros diez minutos de baile</h2>
      <p>Normalmente primero hay un calentamiento: quedarse de pie y seguir los pequeños ajustes que hace tu cuerpo para mantenerse erguido. Eso es la práctica a volumen bajo, no un trámite antes de lo de verdad.</p>
      <p>Después el baile empieza a tu alrededor, a menudo sin ninguna señal. Un baile comienza con una mirada, una mano ofrecida, o dos personas que ya se están moviendo cerca la una de la otra. Mirar desde el borde veinte minutos es una forma normal de empezar, y empezar de inmediato también. La mayor parte de lo que hace quien tiene experiencia en los primeros minutos es escuchar, no moverse. Empezar no es una actuación.</p>
      <h2>Qué se espera de ti</h2>
      <ul>
        <li>Mantén el punto de contacto en singular. Dos manos y una cadera a la vez es forcejeo, no IC.</li>
        <li>Mantén tus propios pies disponibles. Si no puedes aterrizar, no puedes recibir peso con seguridad.</li>
        <li>Rueda al caer en lugar de bloquear. El suelo es la pareja más grande de la sala.</li>
        <li>Di no cuando quieras decir no, y acepta un no sin preguntar por qué.</li>
        <li>Sal del baile cuando termina, incluso a mitad de frase, sin disculparte.</li>
        <li>No enseñes si no te lo han pedido. Una jam no es una clase.</li>
      </ul>
      <h2>Qué llevar</h2>
      {facts([
        ("Ropa", "Holgada y opaca, que cubra espalda, hombros y rodillas. Sin cremalleras, hebillas ni costuras ásperas"),
        ("Pies", "Descalzos o con calcetines blandos antideslizantes. Sin calzado en la sala"),
        ("Agua", "Una botella llena. En Miami el suelo es caluroso y húmedo"),
        ("Toalla", "Una. La vas a necesitar"),
        ("Joyas", "Fuera. Anillos, relojes y collares enganchan y cortan"),
        ("Móvil", "Silenciado, boca abajo, fuera del suelo o en el borde"),
      ])}
      <h2>Qué puedes decir</h2>
      <p>Estas frases se sostienen solas y ninguna necesita un motivo detrás. Rechazar es una habilidad entrenada en esta forma, no un coste social.</p>
      <blockquote>
        <p>&laquo;Ahora no.&raquo;</p>
        <p>&laquo;¿Podemos ir más despacio?&raquo;</p>
        <p>&laquo;Voy a parar aquí.&raquo;</p>
        <p>&laquo;Prefiero no bailar esta.&raquo;</p>
      </blockquote>
      <p>Quien te pregunta por qué has dicho no está respondiendo a una pregunta sobre sí mismo, y eres libre de caminar hasta el borde sin contestar.</p>
      <h2>Cuándo irte</h2>
      <p>Un baile termina cuando cualquiera de las dos personas lo dice, incluso a mitad de frase y aunque sea un levantamiento que aún se está montando. La sesión termina para ti cuando tú decidas: hay quien se va a los veinte minutos y quien se queda tres horas, y las dos cosas son normales. Despídete de quien estabas bailando, o no.</p>
      <h2>Si algo va mal</h2>
      <p>Habla con quien organiza durante o después de la sesión. La mayoría de las jams nombran a una persona que sostiene la sala, y actuar ante una violación de límites es su trabajo y no un favor. Quien organiza y no actúa te está diciendo lo que necesitas saber sobre volver. Tus derechos en la sala y los hábitos de seguridad física están en <a href="{R_SAFETY}">seguridad y consentimiento</a>.</p>
    </div>
    {sessions}
    <div class="prose">
      <p>{rank_note}</p>
      <h2>Preguntas prácticas</h2>
      <p>El coste, ir solo, la forma física, mirar en lugar de bailar y el camino para principiantes están respondidos en una línea cada uno en <a href="{R_FAQ}">la página de preguntas</a>. Cómo suele desarrollarse una sesión completa está en <a href="{R_JAMS}">jams</a>, y qué enseña de verdad una clase para principiantes está en <a href="{R_CLASSES}">clases</a>. Si nunca has leído nada sobre la forma, empieza por <a href="{R_WHATIS}">qué es la Improvisación de Contacto</a>.</p>
    </div>
    {band("¿Listo para ir?", "Cada sesión de arriba enlaza con la página de quien la organiza, que es la única fuente que conoce el horario de esta semana.", [("Jams en Miami", R_JAMS, "primary"), ("Clases y talleres", R_CLASSES, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Tu primera jam de improvisación de contacto, paso a paso</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/tu-primera-jam", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_FIRST,
            "Tu primera jam de improvisación de contacto, paso a paso",
            "Qué pasa de verdad en una primera jam de Improvisación de Contacto en Miami: la llegada, el círculo de apertura, los primeros diez minutos de baile, qué puedes decir, qué llevar y cuándo irte.",
            date_modified=LAST_CHECKED_ISO,
            lang="es",
        ),
        schema.breadcrumb(R_FIRST, "Tu primera jam", lang="es"),
        schema.item_list(
            R_FIRST,
            "Sesiones verificadas en Miami-Dade y Broward",
            [(row[0], row[6], row[1]) for row in listings.SESSIONS],
            lang="es",
        ),
    )
    return page(
        "Tu primera jam de contact improv [Paso a paso]",
        "Qué pasa en una primera jam de Improvisación de Contacto: la llegada, el círculo, los primeros diez minutos, las frases que puedes decir, qué llevar y cuándo irte.",
        R_FIRST,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- the dated jam list

# What the World Jam Map's Florida page held on 14 September 2026, read at
# https://www.contactimprov.com/florida.html. Mirrors JAM_MAP_FINDINGS in
# build/content_local.py line for line; the Spanish page makes no further claim.
JAM_MAP_FINDINGS_ES = [
    ("Entradas de Miami en el mapa", "Una, publicada sin año y sin fecha de inicio"),
    ("Entradas del condado de Broward en el mapa", "Ninguna"),
    ("Enlaces titulados 'Contact Improvisation in Miami'", "Dos, y ninguno llega ya a una comunidad de IC de Miami"),
    ("tribes.tribe.net/ciseflo", "HTTP 404. Tribe.net ya no existe"),
    ("groups.yahoo.com/group/ciseflo/", "HTTP 200, pero aterriza en la portada de yahoo.com: Yahoo Groups cerró en 2020"),
    ("El resto de la página de Florida", "Entradas de Sarasota y Jacksonville Beach, ambas con apariencia de estar vigentes"),
]


def miami_jams():
    findings = facts(JAM_MAP_FINDINGS_ES)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Miami-Dade y Broward</p>
    <h1>Cada sesión de improvisación de contacto en Miami-Dade y Broward que pudimos verificar.</h1>
    <p class="lede">{len(listings.SESSIONS)} entradas, cada una con quien la organiza, la sala, el precio, la modalidad y la fecha en que se comprobó. Más las dos cosas que casi todas las listas se equivocan sobre Florida, y un relato honesto de lo que no pudimos encontrar.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("La práctica recurrente de Improvisación de Contacto que pudimos verificar en Miami-Dade y Broward es una clase semanal de todos los niveles en Dance Arts Miami los martes por la tarde-noche, una jam abierta semanal los viernes por la tarde-noche en Inner Motion Dance Studio, en el borde norte de Miami, en Hallandale Beach, desde el 2 de octubre de 2026, que organiza quien mantiene este sitio, dos talleres con fecha en Miami de una práctica adyacente al contacto que fusiona acro yoga, masaje tailandés y contact improv, un campamento anual de festival en Virginia Key, y dos encuentros recurrentes de danza consciente en el condado de Broward que anuncian un componente de contact improv entre otras prácticas. No se pudo verificar ninguna otra jam ni clase de Improvisación de Contacto en el condado de Broward a partir de una fuente que publique sobre sí misma. Cada entrada de abajo nombra la página en la que se leyó y la fecha en que se comprobó.", SHORT)}
    <div class="prose">
      <p>Última actualización: <strong>14 de septiembre de 2026</strong>. Cada entrada lleva su propia fecha de comprobación, y una sesión cuya fuente ha dejado de publicar sale de esta página en lugar de quedarse aquí pareciendo vigente.</p>
      <p>{LIST_VALUE_NOTE}</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {_sessions_block()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      <h2>Qué corrige esta página</h2>
      <p>El World Jam Map mantiene el listado global de jams de IC, y su <a href="https://www.contactimprov.com/florida.html" rel="noopener nofollow">página de Florida</a> es la única página abierta de la web que menciona una jam en Miami. Pide que la corrijan, con sus propias palabras: <em>Please also help us correct any outdated information.</em> Así que aquí está lo que contenía cuando se abrió el 14 de septiembre de 2026 y se leyó línea por línea.</p>
      {findings}
      <p>La entrada de Miami es una <em>Monday Night Community Jam / Workshop</em> en Excello Dance Space, 8700B SW 129th Terrace, el primer lunes del mes de 19:00 a 21:00, con un coste de 10 dólares, atribuida a Karen Peterson Dancers. No lleva año ni fecha de inicio, así que no hay forma de saber desde la página si ocurrió el mes pasado o la década pasada, y quien se presente confiando en ella asume un riesgo real.</p>
      <p>Karen Peterson Dancers es una compañía de Miami actual y activa, y su propia web sí nombra Excello Dance Space. Lo que su web no publica es una jam de improvisación de contacto, una sesión de lunes ni esa dirección. Así que la jam no puede confirmarse desde la organización a la que se atribuye, y este sitio no la lista como en marcha. Si eres quien la sostiene, <a href="{R_SUBMIT}">mándanos el horario</a> y entra en esta página con una fuente y una fecha, que es lo único que le ha faltado siempre.</p>
      <p>Los dos enlaces bajo <em>Contact Improvisation in Miami</em> son peores que estar sin fecha, porque parecen tener respuesta. El de Tribe.net devuelve un 404: el servidor ya no existe. El de Yahoo Groups devuelve una redirección a la portada de Yahoo, porque Yahoo Groups cerró en 2020 y los archivos del grupo con él. Quien siga cualquiera de los dos enlaces para encontrar la comunidad de Miami en IC no llega a ningún sitio y no tiene forma de saber si es una caída temporal o el estado de la escena.</p>
      <p>Y el condado de Broward no aparece en la página de Florida en absoluto. Eso no es una crítica, es la forma del problema: el listado de IC de Florida se construye con lo que han enviado quienes organizan, y desde Broward no ha enviado nada nadie.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      <h2>Qué no está en esta página, y por qué</h2>
      <p>La mayor parte de una página de listados es la parte que nadie ve. Estas son las cosas que se buscaron, se abrieron cuando fue posible y se dejaron fuera.</p>
      <h3>Una jam de improvisación de contacto en el condado de Broward organizada por otra persona</h3>
      <p>No encontrada. La única jam de esta página con dirección en Broward, la jam de los viernes en el borde norte de Miami, en Hallandale Beach, la puso en marcha quien mantiene este sitio, y aparece arriba apoyándose en la propia página de este sitio y no en la de un tercero. Más allá de ella: se buscó en Fort Lauderdale, Hollywood, Davie, Pembroke Pines, Sunrise, Plantation, Weston, Coral Springs, Hallandale Beach y Miramar, contra páginas de organizadores, listados de Eventbrite y Meetup, y directorios de danza consciente. Lo que hay en Broward es danza extática, que sí está en esta página con su modalidad declarada, y un puñado de profesores que se describen a sí mismos como de Improvisación de Contacto en el propio directorio de miembros del World Jam Map y que no publican sesión, sala ni fecha. Un nombre en un directorio no es una jam, así que no se lista aquí.</p>
      <h3>Los departamentos universitarios de danza como puerta de entrada</h3>
      <p>FIU, Miami Dade College, New World School of the Arts y la Universidad de Miami publican programas de danza, y las páginas a las que se pudo llegar son portales de matrícula o descripciones de cursos. Ninguna publica una sesión pública y recurrente de improvisación de contacto, y ninguna es una superficie de listados, así que ninguna se lista y ninguna se trata como un lugar donde anunciarse. Si un departamento abre una sesión comunitaria, eso sí es algo real que listar y nos gustaría saberlo.</p>
      <h3>Todo lo que se escribe 'improv' y no es esto</h3>
      <p>Busca improv en Miami y te aparece comedia: teatros, clubs, noches de micro abierto y jams de comedia semanales, varias en Hialeah y Fort Lauderdale, y un teatro cuyo dominio se parece lo bastante al tema de este sitio como para merecer ser nombrado como no nosotros. Son buenas noches y no son Improvisación de Contacto, y no están en esta página.</p>
      <h3>Listados sin fecha, presentables o no</h3>
      <p>Cualquier entrada sin fecha en su propia fuente queda excluida, por plausible que parezca. Es la regla que deja fuera la jam de Excello de arriba, y la regla que mantendrá esta página corta. Una lista corta y honesta es justo el objetivo: la página de Florida del CI World Jam Map es el ejemplo de lo que llega a ser una lista larga y optimista.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      <h2>Cómo usar esta lista</h2>
      <p>Trata cada entrada como una pista con fecha y no como un hecho. Abre el enlace de la fuente, que es la página o el listado de quien organiza, y busca una fecha propia: una sesión recurrente cuya fuente no se ha actualizado en meses normalmente ha parado, y un listado sin fecha no es prueba de nada. Después manda un mensaje antes de desplazarte. Quien organiza contesta, y prefiere decírtelo a que llegues a una puerta cerrada.</p>
      <p>Cómo es de verdad asistir a cada sesión y cómo transcurre una jam desde el círculo de apertura hasta el último baile está en <a href="{R_JAMS}">jams</a> y <a href="{R_FIRST}">tu primera jam, paso a paso</a>. Qué hacer en las semanas siguientes a la primera está en <a href="{R_KEEP}">seguir practicando</a>. Qué es la Improvisación de Contacto, si nunca has leído nada sobre ella, empieza en <a href="{R_WHATIS}">qué es la Improvisación de Contacto</a>.</p>
      <p>Esta página no cobra por listar ninguna de estas sesiones y no las clasifica. Una de ellas, la jam de los viernes, la organiza la persona que mantiene esta página, y su entrada lo dice. Es un mapa de una escena sin autoridad central, y no es el mapa.</p>
    </div>
    {band("¿Organizas una sesión en Miami-Dade o Broward?", "Manda el horario, la sala, el precio y dónde lo publicas. Una entrada aquí significa una sola cosa: quien la organiza lo publica y nosotros comprobamos la página. No es un aval.", [("Publicar una sesión", R_SUBMIT, "primary"), ("El directorio más amplio", R_DIRECTORY, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Jams y clases de contact improv en Miami-Dade y Broward</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/jams-miami-dade-broward", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_LIST,
            "Jams y clases de contact improv en Miami-Dade y Broward",
            "Una lista con fechas de las jams, clases y talleres de Improvisación de Contacto verificados en Miami-Dade y Broward, cada una con organizador, sede, horario, precio y modalidad.",
            date_modified="2026-09-14",
            lang="es",
        ),
        schema.breadcrumb(R_LIST, "Lista de jams de Miami-Dade y Broward", lang="es"),
        schema.item_list(
            R_LIST,
            "Jams y clases de contact improv verificadas en Miami-Dade y Broward",
            [(row[0], row[6], row[1]) for row in listings.SESSIONS],
            lang="es",
        ),
    )
    return page(
        "Jams de contact improv en Miami y Broward [2026]",
        "Una lista con fechas de cada jam, clase y taller de Improvisación de Contacto verificados en Miami-Dade y Broward, con organizador, sede, horario y modalidad.",
        R_LIST,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- safety and consent
SAFETY_FAQ_ES = [
    ("¿Es segura la Improvisación de Contacto?",
     "La Improvisación de Contacto conlleva los riesgos normales de una práctica física en pareja: caídas, choques, articulaciones forzadas y algún moratón. La forma los gestiona de manera deliberada, saliendo rodando en lugar de bloquearse, manteniendo los propios pies disponibles, manteniendo un único punto de contacto, calentando y teniendo spotters cerca de los levantamientos. Las lesiones graves son poco frecuentes pero no imposibles, sobre todo en jams rápidas y de gente con experiencia."),
    ("¿Tengo que aceptar todos los bailes que me ofrecen?",
     "No, y nadie debería hacerte sentir lo contrario. Rechazar forma parte de la forma. También puedes terminar un baile a mitad de movimiento, bajarlo de ritmo, pedir menos peso o salir de la sala por completo."),
    ("¿Qué es el spotting?",
     "Spotting es colocarse cerca de una pareja que baila con las manos libres, listo para frenar una caída si ocurre. Uno o dos spotters cerca de una zona concurrida o de levantamientos es práctica habitual en muchas jams."),
    ("¿Qué no es la improvisación de contacto?",
     "La Improvisación de Contacto no es una práctica sexual, ni un lugar para ligar, ni un servicio de masaje, ni una exhibición de acrobacia, ni un espacio para dar instrucciones no pedidas. Tocar, sostener o mover a una pareja de formas que no ha aceptado no forma parte de esta práctica, y las jams lo abordan de frente."),
    ("¿Qué hago si algo va mal en una jam?",
     "Habla con quien organiza durante o después de la sesión. La mayoría de las jams nombran a una persona que sostiene la sala y que es responsable de intervenir. Si quien organiza no actúa ante una violación de límites, eso es información sobre si volver."),
    ("¿Existe un código de conducta de la Improvisación de Contacto?",
     "No hay uno global, porque no hay un organismo global. Cada escena y cada jam escriben el suyo. Las expectativas compartidas son: consentimiento continuo, derecho a rechazar cualquier cosa, respeto por el borde, no enseñar sin que te lo pidan y no grabar sin preguntar."),
]


def safety():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in SAFETY_FAQ_ES)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Límites</p>
    <h1>La seguridad y el consentimiento son la técnica.</h1>
    <p class="lede">La Improvisación de Contacto pone a las personas en contacto físico cercano y les pide moverse bajo el peso de las demás. Eso solo funciona si rechazar está tan entrenado como levantar.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("En la Improvisación de Contacto (IC), el consentimiento es continuo y no se da una sola vez. Cualquier persona puede rechazar una invitación, pausar, bajar el ritmo, cambiar lo que está haciendo o salir de un baile en cualquier momento, sin explicación. Las jams no tienen guía ni supervisión, así que quien acoge la sesión es responsable de enunciar el protocolo y de actuar ante las violaciones.", SHORT)}
    <div class="prose">
      <h2>Tus derechos en la sala</h2>
      <ul>
        <li>Rechazar cualquier invitación a bailar, sin dar motivos.</li>
        <li>Terminar un baile en cualquier momento, incluso a mitad de movimiento.</li>
        <li>Pedir menos peso, menos velocidad o un punto de contacto distinto.</li>
        <li>Sentarte en el borde todo el tiempo que quieras, o toda la noche.</li>
        <li>Que no te toquen de formas que no has aceptado.</li>
        <li>Que no te fotografíen ni te graben sin preguntarte antes.</li>
        <li>Que no te enseñen, corrijan ni entrenen si no lo has pedido.</li>
        <li>Hablar con quien organiza y que te tomen en serio.</li>
      </ul>
      <h2>Seguridad física, en breve</h2>
      <p>La mayoría de las lesiones en IC vienen de tres cosas: bloquearse ante una caída en lugar de rodar, recibir un peso para el que no estás estructuralmente colocado, y bailar cansado. Los hábitos de la propia forma abordan las tres. Mantén tus pies disponibles para aterrizar. Rueda en lugar de frenar. Si no ves cómo se resuelve un levantamiento, no lo empieces. Para antes de agotarte.</p>
      <p>Calienta antes del baile abierto, sobre todo muñecas, hombros y columna. Si la sesión ofrece un calentamiento, úsalo. Si tienes una lesión o una condición que afecta a cómo se te puede mover, díselo a tu pareja antes de que empiece el baile, no durante.</p>
      <h2>Lo que esta práctica no es</h2>
      <p>Merece la pena ser claro, porque la Improvisación de Contacto es vecina de muchas cosas y se confunde con ellas.</p>
      <ul>
        <li>No es una práctica sexual. El tacto es el medio, no una vía hacia otra cosa.</li>
        <li>No es una sesión de terapia. Puede ser reparadora; no es tratamiento clínico.</li>
        <li>No es un lugar para ligar ni un mercado de citas.</li>
        <li>No es una actuación, salvo que un evento concreto lo diga.</li>
        <li>No es un espacio donde alguien con experiencia dirija a alguien con menos.</li>
      </ul>
      <p>Quien trata una jam como cualquiera de las cosas anteriores no está haciendo mal la Improvisación de Contacto. Está haciendo otra cosa, en una sala donde la gente no lo había aceptado.</p>
      <h2>Si ocurre algo</h2>
      <p>Díselo a quien organiza. La mayoría de las jams tienen una persona nombrada que sostiene la sala, e intervenir ante violaciones de límites es su trabajo y no un favor. Si no actúa, eso te dice lo que necesitas saber sobre volver. Este sitio lista sesiones pero no las organiza y no puede mediar, aunque retiraremos una entrada con un patrón de daño denunciado y sin resolver.</p>
      <h2>Preguntas sobre seguridad</h2>
      {faq_html}
    </div>
    {band("Una jam que se toma esto en serio", "Las sesiones que merecen tu tiempo dicen su protocolo en voz alta al principio de cada sesión. Si la tuya no lo hace, pregunta por qué.", [("Buscar una jam", R_JAMS, "primary"), ("Tu primera jam, paso a paso", R_FIRST, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Seguridad y consentimiento en la Improvisación de Contacto</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/seguridad-y-consentimiento", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_SAFETY,
            "Seguridad y consentimiento en la Improvisación de Contacto",
            "El consentimiento en la Improvisación de Contacto: tus derechos en una jam, cómo funciona la seguridad física, qué no es esta práctica y qué hacer si algo va mal.",
            lang="es",
        ),
        schema.breadcrumb(R_SAFETY, "Seguridad y consentimiento", lang="es"),
        schema.faq(SAFETY_FAQ_ES, lang="es"),
    )
    return page(
        "Seguridad y consentimiento [Guía paso a paso]",
        "El consentimiento en la Improvisación de Contacto: qué puedes rechazar siempre, cómo funciona la seguridad física y el spotting, y qué hacer cuando algo va mal.",
        R_SAFETY,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- FAQ
FIRST_JAM_FAQ_ES = [
    ("¿Qué me pongo para una jam de Improvisación de Contacto?",
     "Ropa holgada que cubra la espalda, los hombros y las rodillas, que son los puntos de contacto habituales. Evita cremalleras, hebillas, costuras duras y cualquier textura áspera. Pies descalzos o calcetines blandos antideslizantes. Lleva agua."),
    ("¿Tengo que bailar con alguien?",
     "No. Sentarse en el borde es una parte normal de una jam, y bailar solo forma parte de la forma. Puedes rechazar cualquier invitación, en cualquier momento, sin dar motivos, y puedes terminar un baile a mitad de movimiento."),
    ("¿Tengo que hablar con la gente?",
     "No mucho. Las jams suelen abrir con un círculo breve donde quien organiza enuncia el protocolo y cualquiera puede añadir un límite o un aviso. Después, casi toda la comunicación es física."),
    ("¿Cuánto dura una jam?",
     "Normalmente de dos a tres horas, a menudo con un calentamiento o una clase corta primero. La gente llega y se va a lo largo de la sesión. Llegar después del círculo de apertura suele estar bien; irse antes siempre está bien."),
    ("¿Es caro?",
     "El precio lo fija quien lleva la sesión. Las jams comunitarias suelen ser gratuitas, a donación, o una entrada pequeña que cubre el alquiler de la sala. Las tarifas de clases y talleres varían según quien enseña y las fija cada persona."),
    ("¿Y si no estoy en forma ni soy flexible?",
     "Para empezar no hace falta ninguna de las dos cosas. La forma se basa en la estructura y la gravedad y no en la fuerza ni el rango de movimiento, y las sesiones para principiantes empiezan de pie y rodando, no con levantamientos."),
    ("¿Puedo llevar a mi hijo o hija?",
     "Pregunta a quien organiza. Algunas jams tienen sesiones familiares o para todas las edades; la mayoría de las jams abiertas son espacios de adultos. No hay una regla fija, así que el listado o quien organiza tienen la última palabra."),
    ("Tengo una lesión de espalda o de articulaciones. ¿Puedo ir?",
     "Muchas personas con lesiones y condiciones crónicas practican IC, a veces con adaptaciones acordadas con sus parejas. Habla con quien organiza antes de tu primera sesión y con tu pareja antes de cada baile. Este sitio no es consejo médico."),
]

HISTORY_FAQ_ES = [
    ("¿Quién inventó la Improvisación de Contacto?",
     "Steve Paxton, bailarín y coreógrafo estadounidense. La desarrolló en 1972 a partir de experimentos en Oberlin College y una serie de funciones en Nueva York, apoyándose en su formación en gimnasia, aikido, t'ai chi, la compañía de Merce Cunningham y el Judson Dance Theater."),
    ("¿Cuándo fue la primera función de Improvisación de Contacto?",
     "En enero de 1972 Steve Paxton presentó 'Magnesium' en Oberlin College durante una residencia del Grand Union, una obra para once hombres sobre colchonetas que terminaba con varios minutos de quietud de pie. En junio de 1972 un grupo mixto recién reunido representó la obra que llegó a conocerse como Improvisación de Contacto en la John Weber Gallery de Nueva York."),
    ("¿Por qué nunca se registró como marca?",
     "En 1975 quienes giraban con Steve Paxton como ReUnion consideraron registrar el nombre y establecer una certificación de profesorado, sobre todo por preocupación por la seguridad a medida que la forma se extendía más allá de quienes la habían aprendido directamente. Decidieron no hacer ninguna de las dos cosas y fundaron un boletín. Ese boletín se convirtió en la revista Contact Quarterly."),
    ("¿Quiénes fueron las primeras personas que bailaron Improvisación de Contacto?",
     "El grupo en torno a las primeras funciones en Nueva York en 1972 incluía a Nancy Stark Smith, Nita Little, Daniel Lepkoff, Barbara Dilley, Nancy Topf, Mary Fulkerson, Laura Chapman, Alice Lusterman, Curt Siddall, David Woodberry, Leon Felder y el documentalista de vídeo Steve Christiansen. Nancy Stark Smith pasó a editar Contact Quarterly y a desarrollar el Underscore."),
]

MIAMI_FAQ_ES = [
    ("¿Hay improvisación de contacto en Miami?",
     "Sí. Hay una clase recurrente de Improvisación de Contacto de todos los niveles los martes en Dance Arts Miami, 250 NE 61st Street. Más allá de eso, la práctica del contacto en Miami vive dentro de una comunidad de movimiento más amplia: Kama Flight lleva jams y talleres adyacentes al contacto que fusionan acro yoga, masaje tailandés e Improvisación de Contacto, y Camp Contact lleva la Improvisación de Contacto al festival Love Burn en Virginia Key cada febrero. La Improvisación de Contacto se practica en el sur de Florida desde hace décadas, organizada por personas y no a través de ninguna institución."),
    ("¿Por qué buscar 'improv Miami' no encuentra esto?",
     "Porque en Miami, como en casi todas las ciudades, la palabra improv pertenece al teatro de comedia. Buscar 'improv Miami' devuelve clubs de comedia en Doral y Dania Beach. La forma de danza se encuentra por su nombre completo, 'contact improvisation', o como 'contact improv'. Ese choque de nombres es una de las razones de que la escena de danza de Miami esté poco documentada, y es por lo que este sitio lo escribe entero."),
    ("¿Dónde baila la gente Improvisación de Contacto en Miami?",
     "En espacio de estudio alquilado, en una residencia en Miami Beach, en un almacén o centro de bienestar, y al aire libre en Virginia Key durante el burn anual. La práctica en Miami sigue el mismo patrón que en cualquier otra ciudad: alguien reserva una sala dos horas, lo cuenta, y existe una jam. Las salas cambian; el formato no."),
    ("¿Necesito pareja para ir?",
     "No, y traerla no es obligatorio. Las jams están diseñadas para que la gente llegue sola y baile con quien quiera. Ir con pareja está bien, pero no se espera que pases la sesión con ella."),
    ("¿Se enseña en inglés, en español o en los dos?",
     "Miami es bilingüe, y quienes organizan en Miami-Dade suelen trabajar en los dos idiomas. La improvisación de contacto se enseña sobre todo con el tacto y la demostración, así que el idioma importa menos que en casi cualquier clase de movimiento, pero pregunta si no estás seguro."),
    ("¿Puede ocurrir la improvisación de contacto al aire libre en Miami?",
     "Ocurre, al menos una vez al año y a lo grande, en Love Burn en Virginia Key. Fuera de un festival, las limitaciones prácticas son el calor, la humedad, la arena y la lluvia. Las sesiones tienden a hacerse temprano por la mañana o después del atardecer, sobre hierba o una superficie dura y plana, con más agua de la que crees que necesitas."),
    ("¿Hay algún festival de improvisación de contacto en Florida?",
     "No a la escala de los festivales europeos o de la costa oeste. La práctica de IC en Florida se ha centrado en sesiones locales recurrentes en Miami, Sarasota, Gainesville, Orlando y Jacksonville, varias de las cuales aparecen en la página de Florida del CI World Jam Map. El gran encuentro de Miami es Love Burn, que es un burn regional con improvisación de contacto dentro y no un festival de IC. Quien viaja bailando va a los festivales nacionales e internacionales."),
    ("¿Cómo empiezo una jam en Miami?",
     "Reserva un estudio para una franja recurrente de dos horas, decide si es abierta o para gente con experiencia, escribe el protocolo y dila en voz alta al principio de cada sesión, fija una entrada que cubra la sala, y publícala en algún sitio público. Dos horas a la semana y una sala constante son toda la infraestructura."),
]

BUYER_FAQ_ES = [
    ("¿Cuánto cuesta empezar con la Improvisación de Contacto en Miami?",
     "El coste está en manos de quien lleva la sesión, no en este sitio. Las jams comunitarias suelen ser gratuitas, a donación o con una entrada pequeña que cubre el alquiler de la sala. Las clases y los talleres los pone precio quien enseña o el estudio. Pregunta antes de llegar y no habrá nada que te sorprenda."),
    ("¿Puedo ir solo o debería llevar pareja?",
     "Ve solo. La mayoría de la gente en una jam llega sola, y la forma está hecha para que una persona se encuentre con otra. Ir con pareja está bien, pero no se espera que bailes con ella toda la sesión, y nadie te preguntará por qué fuiste solo."),
    ("¿Necesito estar en forma o ser flexible?",
     "Ninguna de las dos cosas es un requisito previo. La Improvisación de Contacto funciona desde la estructura y la gravedad y no desde la fuerza ni el rango de movimiento, y las sesiones para principiantes empiezan de pie y rodando, no con levantamientos. Las adaptaciones son normales, y acordarlas con tu pareja antes de un baile forma parte de la práctica."),
    ("¿Puedo solo mirar y no bailar?",
     "Sí. Sentarse en el borde es una forma normal de pasar una jam, y mirar es participación y no ausencia. Puedes rechazar cualquier invitación sin dar motivos, y puedes unirte en cualquier momento, tarde, o nunca."),
    ("Nunca he bailado. ¿Cuál es el camino para principiantes?",
     "Empieza con una clase para principiantes si quieres que te enseñen, o con una jam abierta si prefieres aprender en la sala. Las dos son puertas de entrada legítimas. Una clase enseña las habilidades que una jam da por supuestas; una jam abierta acepta a quien viene por primera vez por definición. Nada te obliga a volver."),
]

DIRECTORY_FAQ_ES = [
    ("¿Quién enseña improvisación de contacto en Miami?",
     "La improvisación de contacto no tiene organismo de certificación, así que no hay registro que consultar. Lo que se pudo verificar cuando esta página se comprobó por última vez es una clase recurrente de todos los niveles: Contact Improv &mdash; ALL LEVELS en Dance Arts Miami, martes de 18:00 a 19:00. Todo lo demás pasa por organizaciones que responden a un mensaje directo, listadas en el <a href=\"/es/directorio\">directorio</a>."),
    ("¿Cómo aparezco aquí?",
     "Manda el nombre, la ciudad, qué enseñas u organizas y un enlace a tu propia página. No hay cuota ni membresía. Las entradas se comprueban contra tu propia información publicada antes de publicarse, y cada entrada muestra la fecha en que se comprobó."),
    ("¿Por qué hay danza extática en un sitio de improvisación de contacto?",
     "Porque son las prácticas adyacentes con las que se encontrará de verdad alguien nuevo en este tipo de movimiento en Miami, y porque cada entrada está etiquetada con lo que es. Un directorio que las mezclara en silencio sería peor que uno que lo dice."),
    ("No tengo página propia, ¿sirve igual?",
     "Una entrada aquí significa una cosa: que publicas lo que enseñas o lo que organizas en algún sitio que podemos abrir. Si no tienes página, un listado en Eventbrite o Meetup vale, y el enlace que pondremos será ese."),
]


def faq():
    # One capsule per bucket, so lifting an H2 block yields an answer rather than a
    # topic label. Every fact below is already published elsewhere on this site.
    groups = [
        ("Sobre la práctica",
         "La Improvisación de Contacto (IC) es una forma de danza en pareja e improvisada creada por Steve Paxton en 1972, construida sobre un punto de contacto que rueda y el peso compartido. No tiene organismo de certificación ni autoridad central.",
         WHATIS_FAQ_ES),
        ("Empezar",
         "Puedes empezar sin ninguna experiencia en danza. Ponte ropa cómoda que cubra espalda, hombros y rodillas, llega para el círculo de apertura y recuerda que puedes rechazar cualquier baile sin dar motivos.",
         FIRST_JAM_FAQ_ES),
        ("Jams y sesiones",
         "Una jam es práctica abierta y sin guía: sin profesor, a menudo sin música y sin obligación de bailar con nadie. Una clase enseña las habilidades que una jam da por supuestas; un taller es estudio acotado en el tiempo.",
         JAMS_FAQ_ES),
        ("Seguridad y consentimiento",
         "En la Improvisación de Contacto el consentimiento es continuo y no se da una sola vez: cualquier persona puede pausar, bajar el ritmo o terminar un baile en cualquier momento sin explicación.",
         SAFETY_FAQ_ES),
        ("Historia y orígenes",
         "Steve Paxton desarrolló la Improvisación de Contacto en 1972 en Estados Unidos, y se extendió por giras, enseñanza y un boletín en papel y no a través de ninguna organización.",
         HISTORY_FAQ_ES),
        ("Miami",
         "Miami tiene una clase recurrente de todos los niveles que pudimos verificar en la página de quien organiza, más jams que van y vienen. Esta página solo lista lo que se comprobó, con la fecha en que se comprobó.",
         MIAMI_FAQ_ES),
        ("Preguntas prácticas",
         "El coste, ir solo, la forma física y si puedes simplemente mirar: las preguntas que la gente hace antes de su primera sesión, respondidas sin discurso de venta. La noche en sí se recorre en <a href=\"/es/tu-primera-jam\">tu primera jam, paso a paso</a>, y las semanas siguientes están en <a href=\"/es/seguir-practicando\">seguir practicando</a>.",
         BUYER_FAQ_ES),
        ("Este sitio",
         "No hay membresía, ni entrada de pago, ni registro central, porque la Improvisación de Contacto no tiene organismo de certificación. Todo lo de aquí se comprobó contra la página de quien organiza.",
         DIRECTORY_FAQ_ES),
    ]
    blocks = []
    all_entries = []
    for title, capsule, entries in groups:
        qs = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in entries)
        blocks.append(f"<h2>{title}</h2><p>{capsule}</p>{qs}")
        all_entries.extend(entries)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Preguntas</p>
    <h1>Todo lo que la gente pregunta sobre esta danza.</h1>
    <p class="lede">Respondido en la primera frase, en lenguaje llano, sin misticismo.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      {''.join(blocks)}
    </div>
    {band("¿Sigue sin respuesta?", "Si falta una pregunta aquí, probablemente falta también en el sitio. Mándala.", [("Pregúntanos", R_SUBMIT, "primary"), ("Empezar por lo básico", R_WHATIS, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Preguntas frecuentes</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/preguntas-frecuentes", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_FAQ,
            "Preguntas frecuentes sobre la Improvisación de Contacto",
            "Respuestas breves sobre la Improvisación de Contacto: qué es, cómo empezar, cómo funciona una jam, seguridad y consentimiento, la historia y la escena de Miami.",
            lang="es",
        ),
        schema.breadcrumb(R_FAQ, "Preguntas frecuentes", lang="es"),
        schema.faq(all_entries, lang="es"),
    )
    return page(
        "Preguntas frecuentes de improvisación de contacto [Guía]",
        "Respuestas breves sobre la Improvisación de Contacto en Miami: qué es, cómo empezar, qué pasa en una jam, seguridad y consentimiento, la historia y la escena local.",
        R_FAQ,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ================================================================ the second slice
# Eight more English pages, now translated: miami, classes, directory, glossary,
# history, keep-practising, videos, about. Same rules as above — no new fact, listing
# values quoted verbatim with only the labels translated, one term used consistently —
# and every cross-link in this slice points at a Spanish route, because a Spanish route
# now exists for all of them.

# ---------------------------------------------------------------- Miami

def miami():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in MIAMI_FAQ_ES)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">La ciudad</p>
    <h1>La Improvisación de Contacto en Miami.</h1>
    <p class="lede">Miami es una ciudad de salas prestadas y escenas no oficiales. La improvisación de contacto funciona aquí igual: alguien que enseña con un espacio, una compañía con un estudio, una persona que baila con un número de teléfono, y quien aparezca.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("La Improvisación de Contacto (IC) se practica en el sur de Florida desde hace décadas, organizada por personas y no a través de ninguna institución. Miami no tiene una sede de IC permanente ni un calendario central. La práctica ha pasado históricamente por espacio de estudio alquilado, como la jam comunitaria listada en Excello Dance Space, y por partes de la comunidad de danza contemporánea, físicamente integrada y somática más amplia de Miami. Como la forma no tiene organismo que la licencie, la escena es lo que construyan las personas que están en ella.", SHORT)}
    {facts([
      ("País", "Estados Unidos"),
      ("Estado", "Florida"),
      ("Condados incluidos", "Miami-Dade y Broward"),
      ("Ciudades y barrios", "Miami, Miami Beach, Wynwood, Little Havana, Brickell, Coral Gables, Doral, Hialeah, Pinecrest, Fort Lauderdale"),
      ("Idiomas", "inglés y español"),
      ("Mejores meses para practicar al aire libre", "de noviembre a abril"),
      ("Meses más duros para practicar al aire libre", "de junio a septiembre: calor, humedad y lluvia"),
      ("Cómo se organiza la escena", "Individualmente. Sin organismo, sede ni calendario central"),
    ])}
    <div class="prose">
      <h2>El estado honesto de esto</h2>
      <p>Merece la pena ser directo, porque la mayoría de las guías de ciudad no lo son. La escena de improvisación de contacto de Miami es pequeña y está poco documentada en internet. Lo que existe es real pero disperso: una clase semanal de todos los niveles en Dance Arts Miami, un programa de jams y talleres adyacente al contacto que Kama Flight lleva desde Miami Beach, Camp Contact llevando la improvisación de contacto a Love Burn en Virginia Key cada febrero y, desde octubre de 2026, una jam abierta semanal los viernes en Inner Motion Dance Studio, en el borde norte de Miami, en Hallandale Beach, que organiza quien mantiene este sitio. Esas son las cosas que este sitio pudo verificar, y están listadas en <a href="{R_JAMS}">la página de jams</a> con sus fuentes y la fecha en que se comprobó cada una; la <a href="{R_FRIDAY}">jam de los viernes</a> lleva una aclaración allí donde aparece porque quien organiza y quien publica son la misma persona.</p>
      <p>El resto del cuadro es más fino de lo que a un directorio le gustaría. El mapa mundial CI World Jam Map contiene una jam comunitaria de lunes mensual en Excello Dance Space, con facilitadores rotativos y una entrada de diez dólares; ese listado no lleva fecha y este sitio no lo presenta como vigente. La organización de IC más antigua de Miami pasó por plataformas que ya no existen: un Yahoo Group y una comunidad de Tribe.net, ambas cerradas con sus servidores. La compañía de danza físicamente integrada de Miami, Karen Peterson Dancers, está activa y vigente y lleva mucho tiempo formando parte del paisaje improvisativo y de trabajo en pareja de la ciudad, y por eso aparece en el directorio y no se descarta junto a los enlaces muertos.</p>
      <h2>Dónde vive de verdad la respuesta</h2>
      <p>Nadie puede decirte desde una página web estática dónde está la jam esta noche. Los lugares que sí pueden:</p>
      <ul class="dir-list">
        <li><p><strong>Quien organiza, en persona</strong></p><p>Todos publican sus propios listados y contestan a un mensaje directo. Es la vía más rápida y más fiable, y es la razón de que exista el directorio.</p><p><a href="{R_DIRECTORY}">El directorio</a></p></li>
        <li><p><strong>CI World Jam Map, página de Florida</strong></p><p>El listado de la propia comunidad global. Es honesto sobre lo incompleto que está y pide a quien lo lea que mande correcciones.</p><p><a href="https://www.contactimprov.com/florida.html" rel="noopener nofollow">contactimprov.com/florida.html</a></p></li>
        <li><p><strong>Búsquedas que funcionan</strong></p><p><code>contact improvisation Miami</code>, <code>contact improv South Florida</code>, <code>CI jam Florida</code>. Búsquedas que no funcionan: cualquiera construida sobre la palabra suelta <code>improv</code>, que en Miami devuelve teatros de comedia en Doral y Dania Beach.</p></li>
      </ul>
      <h2>Una trampa que merece nombrarse</h2>
      <p>Una búsqueda en la web de improvisación de contacto en Miami acabará tarde o temprano sacando "Contact Improvisation Gold Coast" y eventos en "The Farm, Miami". Están en Miami, Queensland, Australia, código postal 4220. No tienen nada que ver con Florida y quedan excluidos de todos los listados de este sitio.</p>
      <h2 id="start-one">Si no hay ninguna jam cerca de ti, empieza una</h2>
      <p>Esto no es un premio de consolación. La mayoría de las jams del mundo existen porque una persona reservó una sala. La versión mínima viable cuesta unas dos horas de alquiler de estudio a la semana y una hora de administración.</p>
      <ol class="dir-list">
        <li><p><strong>Encuentra un suelo.</strong> Un estudio de danza con suelo flotante o de marley, a ser posible con colchonetas y una pared para sentarse. Los centros comunitarios y los estudios de yoga sirven. Evita el azulejo, el hormigón y la moqueta.</p></li>
        <li><p><strong>Elige una franja recurrente y mantenla.</strong> La constancia gana a la frecuencia. La misma tarde cada semana construye una sala; una tarde distinta cada mes no lo hará nunca.</p></li>
        <li><p><strong>Decide para quién es.</strong> Una jam abierta acepta a todo el mundo y necesita un calentamiento más largo. Una jam de gente con experiencia acepta a quienes ya saben caer con seguridad en pareja. Di cuál es, cada vez.</p></li>
        <li><p><strong>Escribe el protocolo y dilo en voz alta.</strong> Consentimiento continuo, derecho a rechazar cualquier cosa, no enseñar sin que te lo pidan, no grabar sin preguntar, el borde es para descansar, y aquí está quién sostiene la sala. Dos minutos al principio de cada sesión.</p></li>
        <li><p><strong>Fija una entrada que cubra la sala.</strong> No para ganar dinero: para que la jam sobreviva más allá de la tercera semana.</p></li>
        <li><p><strong>Publícala.</strong> Una página, una cuenta, una entrada de calendario recurrente y una entrada en el World Jam Map. Después <a href="{R_SUBMIT}">díselo a este sitio</a>, que no cuesta nada y lleva un minuto.</p></li>
      </ol>
      <h2>Cuestiones prácticas propias de Miami</h2>
      <ul>
        <li><strong>El calor.</strong> Una sesión de dos horas en julio necesita más agua y más descanso que la misma sesión en enero. Reserva a primera hora o por la tarde-noche para cualquier cosa al aire libre.</li>
        <li><strong>La lluvia.</strong> Las tormentas de tarde entre junio y septiembre cancelan una jam al aire libre casi con puntualidad. Las salas cubiertas no tienen ese problema, y por eso la mayoría de las jams son bajo techo.</li>
        <li><strong>El suelo.</strong> La arena y la hierba perdonan las caídas y son malas para rodar. Las jams de playa funcionan mejor para práctica baja, lenta y de compartir peso que para levantamientos.</li>
        <li><strong>Aparcamiento y distancia.</strong> Miami-Dade es ancho y dependiente del coche. Di dónde se aparca cuando anuncies una sesión, y cuenta con que la gente conduzca cuarenta minutos por una jam que merezca la pena.</li>
        <li><strong>Dos idiomas.</strong> Publica las sesiones en inglés y en español. Es un trabajo de cinco minutos y duplica a quien puede encontrarte.</li>
        <li><strong>Las temporadas.</strong> La gente que baila, enseña y alquila estudios viaja. Cuenta con una caída real de asistencia en verano y alrededor de Art Basel en diciembre.</li>
      </ul>
      <h2>Preguntas sobre la IC en Miami</h2>
      {faq_html}
    </div>
    {band("¿Sabes algo que esta página no dice?", "Si enseñas, acoges, organizas o simplemente bailas en el sur de Florida, dínoslo y entra en el mapa. Las correcciones son tan bienvenidas como las incorporaciones, incluido retirar algo que ha parado.", [("Publicar una entrada", R_SUBMIT, "primary"), ("El directorio", R_DIRECTORY, "secondary"), ("Seguir practicando", R_KEEP, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Improvisación de Contacto en Miami</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/miami", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_MIAMI,
            "Improvisación de Contacto en Miami",
            "La escena de Improvisación de Contacto de Miami: dónde se practica, cómo se organiza, las cuestiones prácticas propias de Miami y cómo empezar una jam aquí.",
            about={"@id": schema.SITE + "/#place"},
            lang="es",
        ),
        schema.breadcrumb(R_MIAMI, "Miami", lang="es"),
        schema.faq(MIAMI_FAQ_ES, lang="es"),
        {
            "@type": "Place",
            "@id": schema.SITE + "/es/miami#place",
            "name": "Miami, Florida, United States",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Miami",
                "addressRegion": "FL",
                "addressCountry": "US",
            },
            "geo": {"@type": "GeoCoordinates", "latitude": 25.7617, "longitude": -80.1918},
            "containedInPlace": {"@type": "AdministrativeArea", "name": "Miami-Dade County, Florida"},
        },
    )
    return page(
        "Improvisación de Contacto en Miami [Guía 2026]",
        "La improvisación de contacto en Miami: el estado real de la escena, dónde se practica en Miami-Dade y Broward, y cómo empezar una jam aquí.",
        R_MIAMI,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- classes

SKILLS_ES = [
    ("Compartir peso", R_CLASSES + "#first-jam",
     "Dar y recibir peso a través del esqueleto"),
    ("Caídas y rodar", R_CLASSES + "#first-jam",
     "Salidas seguras de una caída o de un levantamiento fallido"),
    ("Punto de contacto", R_CLASSES + "#first-jam",
     "Mantener un único punto de contacto deslizante"),
    ("Límites y consentimiento", R_SAFETY,
     "Rechazar, pausar y renegociar"),
    ("Levantamientos", R_CLASSES + "#first-jam",
     "Estructuras de apoyo y cuándo no usarlas"),
]


def classes():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FIRST_JAM_FAQ_ES)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Aprender</p>
    <h1>Clases, talleres y tu primera jam.</h1>
    <p class="lede">Puedes empezar con la Improvisación de Contacto sin ninguna formación en danza. Una sesión para principiantes te pone a caer con seguridad en una tarde, y el resto es tiempo en la sala.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("Una clase de Improvisación de Contacto (IC) enseña las habilidades de base: cómo compartir peso sin derrumbarse, cómo salir rodando de una caída, cómo leer el momento de tu pareja y cómo decir no. Las sesiones para principiantes no presuponen formación en danza. La mayoría de la gente asiste a clases unas semanas y después añade una jam semanal, porque la forma se aprende sobre todo bailando y no con instrucción.", SHORT)}
    <div class="prose">
      <h2 id="first-jam">Tu primera jam, paso a paso</h2>
      <p><strong>Antes.</strong> Escribe a quien organiza y di que eres nuevo. Pregunta tres cosas: si está abierta a principiantes, cuánto cuesta la entrada y si hay calentamiento antes del baile abierto. Las tres respuestas deberían ser fáciles.</p>
      <p><strong>La llegada.</strong> Llega al principio si puedes, porque el círculo de apertura es donde se fijan las reglas. Cámbiate, deja la bolsa en el borde, llena la botella.</p>
      <p><strong>El calentamiento.</strong> Quédate de pie y escucha los pequeños ajustes que hace tu cuerpo para mantenerse erguido. No es un calentamiento para lo de verdad; es lo de verdad a baja amplitud.</p>
      <p><strong>Tu primer baile.</strong> Mira a alguien. Si te devuelve la mirada, estáis bailando. Empieza con una mano, un hombro, o simplemente estando cerca. Mantén un punto de contacto. Deja que una de las dos personas dé peso despacio y mira qué hace el suelo.</p>
      <p><strong>El final.</strong> Para cuando quieras. Da un paso atrás, asiente con la cabeza, camina hasta el borde. No hace falta explicación y no se espera ninguna, en ninguna de las dos direcciones.</p>
      <p><strong>Después.</strong> Probablemente estarás cansado de una forma que no es cansancio deportivo. Bebe agua. <a href="{R_KEEP}">Vuelve</a>, y mira qué pasa después de la primera visita.</p>
      <h2>Qué enseñan de verdad las clases</h2>
      <p>Una buena serie para principiantes cubre el mismo puñado de cosas, sea cual sea el estilo de quien enseña.</p>
      {facts([
        ("Peso", "Dar y recibir peso a través del esqueleto, no agarrando"),
        ("Caídas", "Salidas rodando, encogerse, aterrizar en el suelo sin manos"),
        ("Contacto", "Mantener un único punto de contacto deslizante y seguirlo"),
        ("Escuchar", "Leer la presión y el momento en lugar de mirar"),
        ("Límites", "Rechazar, pausar, irse y renegociar a mitad del baile"),
        ("Levantamientos", "Cómo funcionan las estructuras de apoyo y cuándo no intentar uno"),
      ])}
      <h2>Cómo juzgar a quien enseña</h2>
      <p>No hay organismo de certificación de la Improvisación de Contacto, así que no puedes comprobar una licencia. Lo que sí puedes comprobar es el comportamiento. Quien enseña debería enunciar su marco de consentimiento en los primeros diez minutos en lugar de darlo por supuesto. Debería demostrar tanto como habla. Debería corregir una técnica insegura de inmediato, incluso en la sala y no en un aparte privado después. No debería exigirte que hagas pareja con una persona concreta, y debería estar cómodo cuando rechazas a alguien.</p>
      <p>Una escena sin certificación es una escena donde la reputación es todo el control de calidad. Merece la pena saberlo antes de pagar un intensivo.</p>
      <h2>Dónde aprenderlo en Miami</h2>
      <p>Se pudo verificar una clase recurrente de Improvisación de Contacto en Miami-Dade a partir de sus propios listados cuando esta página se comprobó por última vez: <strong>Contact Improv &mdash; ALL LEVELS</strong> en Dance Arts Miami, 250 NE 61st Street, Miami, 33137, los martes de 18:00 a 19:00. Se anuncia como un espacio para trabajar conexión, compartir peso, momento y formación de pareja espontánea, y no hace falta pareja. Como se publica como una serie de varias fechas en Eventbrite y se replica en Meetup, confirma la semana actual allí en lugar de fiarte de esta página.</p>
      <p>Más allá de esa clase, las vías realistas hacia la forma en Miami son las <a href="{R_JAMS}">jams, campamentos y prácticas adyacentes</a> listadas en otras partes de este sitio. Si prefieres aprender de forma estructurada y no hay ninguna clase cerca de ti, una clase de danza contemporánea o de improvisación en cualquier estudio de Miami te enseñará buena parte de la alfabetización corporal, y las jams te enseñarán el resto.</p>
      <h2>Después de la primera</h2>
      <p>Qué hacer en las semanas siguientes a tu primera sesión, incluidas las semanas en que no hay nada, está en la <a href="{R_KEEP}">página de seguir practicando</a>. Un recorrido más completo de la noche en sí &mdash; la llegada, el círculo de apertura, los primeros diez minutos de baile y las frases que puedes decir cuando quieres parar &mdash; está en <a href="{R_FIRST}">tu primera jam, paso a paso</a>.</p>
      <h2>Preguntas que la gente hace antes de su primera sesión</h2>
      {faq_html}
    </div>
    {band("Encuentra algo esta semana", "Empieza por una jam, o por una clase para principiantes si prefieres que te enseñen primero. Las dos son puertas de entrada legítimas.", [("Jams", R_JAMS, "primary"), ("Profesorado y estudios", R_DIRECTORY, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Clases de Improvisación de Contacto y primeras jams</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/clases", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_CLASSES,
            "Clases de Improvisación de Contacto y tu primera jam",
            "Cómo empezar la Improvisación de Contacto en Miami: qué cubre una clase para principiantes, qué pasa en tu primera jam, cómo juzgar a quien enseña y qué llevar.",
            lang="es",
        ),
        schema.breadcrumb(R_CLASSES, "Clases", lang="es"),
        schema.faq(FIRST_JAM_FAQ_ES, lang="es"),
        schema.item_list(
            R_CLASSES,
            "Habilidades que enseña un curso para principiantes de Improvisación de Contacto",
            SKILLS_ES,
            lang="es",
        ),
    )
    return page(
        "Clases de Improvisación de Contacto en Miami [2026]",
        "Cómo empezar la Improvisación de Contacto en Miami: qué enseña una clase para principiantes, un recorrido de tu primera jam y qué llevar.",
        R_CLASSES,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- directory

# The same nine resources as build/content_directory.GLOBAL_RESOURCES, in the same
# order, with the site's own description of each translated. The resource NAMES are the
# organisations' own names and stay as published; so do the URLs.
GLOBAL_RESOURCES_ES = [
    ("Contact Improvisation World Resource", "https://www.contactimprov.com/",
     "El centro internacional de la forma, en marcha desde los años noventa: un mapa mundial de jams, un calendario de eventos, un directorio de profesorado, listados de miembros y un índice de enlaces."),
    ("CI World Jam Map: Florida", "https://www.contactimprov.com/florida.html",
     "El listado de Florida de la propia comunidad. Es lo más parecido a un directorio de jams del sur de Florida que existe, y lo mantiene quien manda correcciones."),
    ("CI Global Calendar", "https://ciglobalcalendar.net/en",
     "Un calendario compartido y multilingüe de clases, jams, talleres y festivales de IC en todo el mundo, publicado por quienes organizan y enseñan. El mejor lugar único donde buscar algo que ocurra en cualquier parte."),
    ("Contact Quarterly", "https://www.contactquarterly.com/",
     "La revista que nació del boletín de 1975 y el archivo escrito principal de la forma durante cuatro décadas y media."),
    ("CQ CI Contacts List", "https://contactquarterly.com/contact-improvisation/contacts",
     "El directorio de referencia de Contact Quarterly para localizar clases, jams y practicantes de IC, organizado por país y estado de Estados Unidos."),
    ("Earthdance", "https://earthdance.net/",
     "Un centro de movimiento e improvisación de larga trayectoria en Plainfield, Massachusetts, que acoge talleres, residencias y jams."),
    ("Touch&Play Global", "https://touchandplay.org/",
     "Retiros, talleres y aprendizaje relacional construidos alrededor de la práctica del contacto y del consentimiento."),
    ("Contact Improvisation Dance Canada", "https://www.contactimprov.ca/",
     "Un recurso y sitio de listados nacional de IC, útil como modelo de cómo se organizan y se publican las jams de un país."),
    ("Contact improvisation (entrada de enciclopedia)", "https://en.wikipedia.org/wiki/Contact_improvisation",
     "Un punto de partida para las definiciones, el linaje y las influencias de la forma, con referencias."),
]

TEACHERS_NOTE_ES = (
    '<div class="prose"><h2 id="teachers">Profesorado</h2>'
    "<p>No existe ningún registro de profesorado de Improvisación de Contacto, en ningún sitio, porque "
    "la forma nunca se registró como marca ni se certificó. Fue una decisión deliberada en 1975 y este "
    "sitio no va a inventar la autoridad que los propios fundadores de la forma rechazaron.</p>"
    "<p>Así que la posición honesta sobre Miami: <strong>no se pudo confirmar ningún profesor o "
    "profesora de Improvisación de Contacto con base en Miami a partir de su propia información "
    "publicada</strong> en el momento de escribir esto. Aparecen nombres individuales en directorios de "
    "miembros de IC heredados de alrededor de 2010 y en publicaciones de redes sociales, y ninguno de "
    "ellos es lo bastante actual para publicarlo. Quien sabe de verdad son las organizaciones de abajo, "
    "y la vía más rápida es preguntar a la que organiza la clase a la que estás pensando ir.</p>"
    f'<p>Si enseñas aquí, <a href="{R_SUBMIT}">mándanos tu página</a>. Una entrada de profesorado en '
    "este sitio significa una sola cosa: esta persona publica qué enseña y dónde. No es un aval, y no "
    "puede serlo, en una forma sin evaluador.</p></div>"
)


def _org_rows_es(rows, heading, blurb):
    """Studio / organisation entries with Spanish labels and the values quoted verbatim."""
    if not rows:
        return ""
    items = []
    for name, kind, city, url, verified, note in rows:
        items.append(
            f'<li><p><a href="{html.escape(url)}" rel="noopener nofollow"><strong>{html.escape(name)}</strong></a>'
            f" &middot; {html.escape(kind)}</p>"
            f"<p>{html.escape(city)}</p>"
            f"<p>{html.escape(note)}</p>"
            f"<p>Comprobado el {verified}</p></li>"
        )
    return (
        f'<div class="prose"><h2>{heading}</h2><p>{blurb}</p>'
        f'<ul class="dir-list">{"".join(items)}</ul></div>'
    )


def directory():
    resources = "".join(
        f'<li><a href="{u}" rel="noopener nofollow">{n}</a><p>{d}</p></li>'
        for n, u, d in GLOBAL_RESOURCES_ES
    )
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in DIRECTORY_FAQ_ES)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Directorio</p>
    <h1>A quién preguntar, y dónde continúa el mapa.</h1>
    <p class="lede">Primero quien organiza y los estudios locales, después los recursos internacionales que sostienen los listados, los archivos y los festivales de la forma.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("La Improvisación de Contacto (IC) no tiene un directorio central porque no tiene un organismo central. Los listados locales los guardan quienes organizan. Lo más parecido a un índice global es el CI World Jam Map en contactimprov.com, que lista sesiones por país y estado, incluida una página de Florida que cubre Miami, Sarasota, Gainesville y Jacksonville.", SHORT)}
    <div class="prose">
      <h2>Recursos internacionales</h2>
      <p>Estos son los sitios que de verdad sostienen los listados, los archivos y los encuentros de la forma. Cada uno se abrió y se comprobó cuando se añadió aquí.</p>
      <ul class="dir-list">{resources}</ul>
      <p>{LIST_VALUE_NOTE}</p>
    </div>
    {TEACHERS_NOTE_ES}
    {_org_rows_es(listings.ORGS, "Estudios, compañías y organizaciones", "Cada una de estas se abrió y se comprobó. Donde una organización es adyacente al contacto y no de improvisación de contacto, la entrada lo dice. Los nombres, los tipos de organización y las notas se reproducen tal como se publicaron en la fuente.")}
    {_org_rows_es(listings.ADJACENT, "Práctica adyacente, etiquetada con honestidad", "Disciplinas distintas con comunidades muy solapadas. Aparecen porque alguien nuevo que busca este tipo de movimiento en Miami va a encontrarse con estas personas de todas formas, y porque fingir lo contrario sería el tipo de directorio que te hace perder la tarde. Otra vez: práctica distinta, comunidad vecina.")}
    <div class="prose">
      <h2>Preguntas sobre el directorio</h2>
      {faq_html}
    </div>
    {band("Añádete", "Sin cuota, sin membresía, sin comité. Si enseñas, acoges u organizas en el sur de Florida, esta página existe para señalar hacia ti.", [("Publicar una entrada", R_SUBMIT, "primary"), ("La escena de Miami", R_MIAMI, "secondary"), ("Seguir practicando", R_KEEP, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Directorio de Improvisación de Contacto</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/directorio", CITE)}
  </div>
</section>
"""
    items = [(n, u, d) for n, u, d in GLOBAL_RESOURCES_ES]
    local = [(o[0], o[3], "") for o in listings.ORGS]
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_DIRECTORY,
            "Directorio de Improvisación de Contacto: Miami y más allá",
            "Profesorado, quien organiza y estudios de improvisación de contacto en Miami, más los recursos internacionales que sostienen los listados y los archivos de la forma.",
            lang="es",
        ),
        schema.breadcrumb(R_DIRECTORY, "Directorio", lang="es"),
        schema.faq(DIRECTORY_FAQ_ES, lang="es"),
        schema.item_list(R_DIRECTORY + "#international", "Recursos internacionales de Improvisación de Contacto", items, lang="es"),
        schema.item_list(R_DIRECTORY + "#miami", "Organizaciones de movimiento de Miami", local, lang="es"),
    )
    return page(
        "Directorio de Improvisación de Contacto (100% gratis)",
        "Profesorado, quien organiza y estudios de improvisación de contacto en Miami, más los recursos internacionales con los listados y archivos de la forma.",
        R_DIRECTORY,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- glossary

# One term, one definition, same slugs as the English page so a fragment identifier keeps
# working in both locales. The retired English synonyms stay reachable as alternateName:
# the English words are what people actually search, so they are not translated away.
TERMS_ES = [
    ("contact-improvisation", "Improvisación de Contacto (IC)",
     "Una forma de danza en pareja en la que dos o más personas improvisan alrededor de puntos de contacto físico cambiantes, compartiendo peso y siguiendo la gravedad, el momento y el impulso."),
    ("jam", "Jam",
     "Una sesión abierta y sin guía donde cualquiera que esté presente puede bailar. Sin profesor, poca o ninguna música, y un borde donde sentarse a mirar."),
    ("score", "Score",
     "Una restricción enunciada que da forma a una improvisación, como bailar solo por debajo de las caderas o seguir el punto de contacto sin interrumpirlo."),
    ("small-dance", "Small dance",
     "La small dance es la práctica de pie con la que abre una sesión: te quedas quieto y sigues los microajustes que hace el cuerpo para mantenerse erguido, en lugar de intentar quedarte inmóvil."),
    ("weight-sharing", "Compartir peso",
     "Dar deliberadamente parte o todo tu peso a una pareja y recibir el suyo, con el apoyo del esqueleto y del suelo y no de la musculatura. Es la mecánica central de la forma: una persona da peso, la otra lo recibe, y los papeles se intercambian continuamente."),
    ("spotting", "Spotting",
     "Estar de pie y listo, con las manos libres, cerca de una pareja que baila, para que si una caída va mal haya alguien a mano que la frene."),
    ("underscore", "Underscore",
     "Un score grupal de formato largo desarrollado por Nancy Stark Smith, que recorre unas veinte fases nombradas y se usa para dar forma a toda una sesión de práctica o a un festival."),
    ("landing", "Aterrizaje",
     "Llegar al suelo desde una caída o un levantamiento, normalmente rodando a través del punto de contacto para que el suelo reciba el peso de forma progresiva."),
    ("solo", "Solo",
     "Bailar solo dentro de una jam. Completamente normal, y a menudo donde ocurre el trabajo más interesante."),
    ("edge", "El borde",
     "El perímetro de la sala donde la gente descansa, mira, bebe agua y vuelve a entrar. Mirar desde el borde es participación, no ausencia."),
    ("contact-point", "Punto de contacto",
     "El único lugar donde dos cuerpos se tocan. Mantenerlo en singular es lo que evita que el baile se convierta en un forcejeo."),
    ("duet", "Dúo",
     "Dos personas que bailan. La unidad básica de la forma, aunque la IC también ocurre en tríos y en grupos mayores."),
    ("open-jam", "Jam abierta",
     "Una jam sin requisito de experiencia previa. Si una jam está cerrada a principiantes, el listado lo dirá."),
    ("consent-practice", "Práctica de consentimiento",
     "El hábito de preguntar, rechazar y renegociar dentro del baile. Se trata como parte de la técnica y no como una política."),
]

TERM_ALTERNATES_ES = {
    "small-dance": "the small dance",
    "weight-sharing": "weight exchange",
}


def glossary():
    rows = "".join(
        f'<h3 id="{slug}">{term}</h3><p>{definition}</p>'
        for slug, term, definition in TERMS_ES
    )
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Vocabulario</p>
    <h1>Las palabras que la gente usa en la sala.</h1>
    <p class="lede">La Improvisación de Contacto tiene su propio lenguaje de trabajo. Nada de él hace falta para bailar, pero conocerlo hace que la primera jam sea mucho menos opaca.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("El vocabulario básico de la Improvisación de Contacto (IC) es: <strong>contacto</strong> (el punto donde dos cuerpos se tocan), <strong>compartir peso</strong> (dar y recibir el peso del cuerpo), la <strong>small dance</strong> (la práctica de pie con la que abre una sesión, siguiendo los microajustes del cuerpo en lugar de quedarse inmóvil), un <strong>score</strong> (una restricción enunciada), la <strong>jam</strong> (una sesión abierta y sin guía) y el <strong>spotting</strong> (estar listo para frenar una caída). El original inglés de cada término se nombra cuando es la palabra que la gente busca.", "La versión corta")}
    <div class="prose">
      <h2>Términos que se usan en una jam</h2>
      <p>El vocabulario de trabajo de la Improvisación de Contacto, en una frase cada uno. Nada de él hace falta para bailar; conocerlo hace que la primera jam sea mucho menos opaca.</p>
      {rows}
    </div>
    {band("Palabras aprendidas, el siguiente paso es una sala", "El vocabulario tiene sentido unos diez minutos después de tu primera jam, no antes.", [("Buscar una jam", R_JAMS, "primary"), ("Qué esperar", R_FIRST, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Glosario de Improvisación de Contacto</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/glosario", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_GLOSSARY,
            "Glosario de Improvisación de Contacto",
            "El vocabulario de trabajo de la Improvisación de Contacto: jam, score, small dance, underscore, compartir peso, spotting, aterrizaje y el borde.",
            lang="es",
        ),
        schema.breadcrumb(R_GLOSSARY, "Glosario", lang="es"),
        schema.defined_terms(TERMS_ES, path="/es/glosario", alternates=TERM_ALTERNATES_ES),
    )
    return page(
        "Glosario de Improvisación de Contacto [Lista]",
        "Definiciones en lenguaje llano de los términos de la Improvisación de Contacto: jam, score, small dance, underscore, compartir peso, spotting y el borde.",
        R_GLOSSARY,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- history

def history():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in HISTORY_FAQ_ES)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Historia</p>
    <h1>De dónde viene la Improvisación de Contacto.</h1>
    <p class="lede">Empezó en un gimnasio universitario de Ohio, recibió su nombre en una galería de Nueva York y se dejó deliberadamente sin dueño.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("La Improvisación de Contacto (IC) fue desarrollada por el bailarín y coreógrafo estadounidense Steve Paxton en 1972. Surgió de una residencia en Oberlin College en enero de 1972 y de una serie de funciones en la John Weber Gallery de Nueva York en junio de 1972, y recibió la influencia de la danza moderna, el aikido y las prácticas somáticas. La forma nunca se registró como marca y no tiene organismo que la licencie.", SHORT)}
    <div class="prose">
      <h2>Enero de 1972, Oberlin College</h2>
      <p>El colectivo improvisativo Grand Union estaba en residencia en Oberlin College, en Ohio. Paxton, miembro de ese grupo, venía dando lo que llamaba una clase suave a primera hora de la mañana, parte meditación y parte ejercicio ligero. Durante la residencia hizo una obra llamada <strong>Magnesium</strong> para once hombres sobre colchonetas, en la que se lanzaban, se atrapaban, se arrojaban y caían unos entre otros de forma continua, y que terminaba con varios minutos de quietud de pie. Ya le había pedido a una estudiante que estaba mirando, Nancy Stark Smith, que siguiera en contacto si alguna vez volvía a trabajar así.</p>
      <p>Paxton traía un conjunto de influencias poco habitual: gimnasia de competición de sus años de escuela, años de estudio de aikido en el New York Aikikai, t'ai chi, tres años en la Merce Cunningham Dance Company y la cofundación del Judson Dance Theater en 1962. La técnica release llegó con Mary Fulkerson, a quien invitó al grupo siguiente.</p>
      <h2>Junio de 1972, Nueva York</h2>
      <p>En junio reunió a un grupo mixto para cinco días de práctica continua y una muestra pública en la John Weber Gallery de Nueva York. Ese evento se llamó Contact Improvisation. El grupo incluía a Nancy Stark Smith, Nita Little, Daniel Lepkoff, Barbara Dilley, Nancy Topf, Mary Fulkerson, Laura Chapman, Alice Lusterman, Curt Siddall, David Woodberry y Leon Felder, con Steve Christiansen documentando en vídeo. La primera iteración del baile se hizo en esa semana.</p>
      <h2>1975: la decisión de no tenerlo</h2>
      <p>En 1975 quienes trabajaban con Paxton habían formado ReUnion, una compañía que se reunía una vez al año para girar por la costa oeste con funciones y clases. Discutieron registrar el término <em>contact improvisation</em> como marca y establecer una certificación de profesorado, sobre todo porque la forma se extendía más rápido que sus prácticas de seguridad. Rechazaron las dos cosas y en su lugar fundaron un boletín como forma de mantener en contacto a practicantes geográficamente dispersos.</p>
      <p>Nancy Stark Smith editó y produjo ese boletín, mecanografiando y fotocopiando ella misma los primeros números. Lisa Nelson se incorporó como coeditora en 1976, y la publicación pasó a llamarse <strong>Contact Quarterly</strong>, descrita entonces y después como un vehículo para ideas en movimiento. Se publicó durante cuatro décadas y media. La negativa a registrar la marca o certificar es la razón de que hoy no exista ninguna autoridad que licencie la Improvisación de Contacto en ningún lugar del mundo, y la razón de que la escena de cualquier ciudad tenga el aspecto que tiene: organizada localmente, enseñada informalmente y sostenida por las personas que aparecen.</p>
      <h2>Cómo se desarrolló la práctica</h2>
      <p>Stark Smith desarrolló después el <strong>Underscore</strong>, un score de formato largo que da a una improvisación grupal un arco de unas veinte fases nombradas, y los <strong>jeroglíficos</strong>, una notación para el ritmo sentido de un baile. El trabajo de Lisa Nelson sobre composición y percepción dio forma a cómo la práctica habla de ver y de ser visto. La investigación de Nita Little sobre los estados de atención conectó la IC con la ciencia cognitiva. La forma se trasladó también al trabajo de actuación, a la danza terapia, al teatro físico y a la coreografía contemporánea, de una manera que sus primeros practicantes no esperaban.</p>
      <h2>La jam como la institución real</h2>
      <p>Como nunca hubo una organización, lo que llevó la IC por todo el mundo fue la jam: una sesión informal, recurrente y sin enseñanza en una sala prestada, anunciada de boca en boca o en un listado impreso. Contact Quarterly llevó esos listados durante décadas en una sección llamada DanceMap. Esa función ocurre hoy en lugares dispersos, lo que es buena parte de la razón de que este sitio exista para Miami.</p>
      <h2>Preguntas que la gente hace sobre la historia</h2>
      {faq_html}
    </div>
    <div class="prose" style="margin-top:40px">
      <h2 style="margin-top:0">Fuentes</h2>
      <ul>
        <li><a href="https://en.wikipedia.org/wiki/Contact_improvisation" rel="noopener">Contact improvisation</a>, Wikipedia (consultado en septiembre de 2026)</li>
        <li><a href="http://sarma.be/docs/3269" rel="noopener">A Short History</a>, SARMA (consultado en septiembre de 2026)</li>
        <li><a href="https://www.nytimes.com/2020/05/27/arts/dance/nancy-stark-smith-dead.html" rel="noopener">Nancy Stark Smith, a Founder of Contact Improvisation, Dies at 68</a>, The New York Times, 27 de mayo de 2020</li>
        <li><a href="https://www.contactquarterly.com/" rel="noopener">Contact Quarterly</a>, la revista que nació del boletín de 1975</li>
      </ul>
    </div>
    {band("Baila la historia en lugar de leerla", "La forma se siente más fácilmente de lo que se describe. Busca una jam y quédate quieto en una sala con otras personas durante dos minutos.", [("Jams en Miami", R_JAMS, "primary"), ("Glosario de términos", R_GLOSSARY, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Historia de la Improvisación de Contacto</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/historia", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_HISTORY,
            "Historia de la Improvisación de Contacto",
            "Cómo empezó la Improvisación de Contacto en 1972: Steve Paxton, Magnesium en Oberlin, las primeras funciones en la John Weber Gallery y la decisión de 1975 de no registrar la forma como marca.",
            lang="es",
        ),
        schema.breadcrumb(R_HISTORY, "Historia", lang="es"),
        schema.faq(HISTORY_FAQ_ES, lang="es"),
    )
    return page(
        "Historia de la Improvisación de Contacto [Cronología]",
        "Cómo empezó la Improvisación de Contacto: Steve Paxton, Magnesium en Oberlin College y por qué la forma nunca se registró como marca ni se certificó.",
        R_HISTORY,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- keep practising

def keep_practising():
    sessions = _sessions_for_stage()
    rank_note = (
        "La modalidad de cada entrada de arriba es la que quien organiza declara sobre su "
        "propia sesión, y cada entrada lleva la fecha en que se abrió y se leyó su fuente; las "
        f"entradas de terceros se volvieron a comprobar el <strong>{LAST_CHECKED_BY_LANG['es']}</strong>. "
        "Esta página no clasifica nada. Las "
        "entradas aparecen en el orden en que se verificaron, ninguna está pagada y este sitio "
        "no recomienda ninguna por encima de otra."
    )
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Después de la primera vez</p>
    <h1>Cómo seguir practicando la improvisación de contacto en Miami.</h1>
    <p class="lede">La parte que viene después de tu primera visita: qué hacer entre jams, por qué la segunda se siente distinta y qué hacer en las semanas en que no hay nada.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("Sigues practicando volviendo. La Improvisación de Contacto se aprende en la sala y no entre sesiones, así que la respuesta honesta es una jam o una clase semanal, más un poco de práctica en solitario para las semanas en que no hay nada. Esta página cubre la parte posterior a tu primera visita, incluidas las semanas en que la respuesta es que no hay nada.", SHORT)}
    <div class="prose">
      <h2>Practicar por tu cuenta</h2>
      <p>La <a href="{R_GLOSSARY}#small-dance">small dance</a> es la versión casera de toda la forma: quédate de pie, con la mirada suave, y sigue los microajustes que hace tu cuerpo para mantenerse erguido. Dos minutos bastan para empezar.</p>
      <p>A partir de ahí, trabajo de suelo y práctica de caídas. Rodar por el suelo sin empujarte con las manos, y aprender a recibir el suelo rodando en lugar de frenarte. No tiene nada de glamuroso, y es de donde viene en realidad casi toda la seguridad de una jam. <a href="{R_SAFETY}">Seguridad y consentimiento</a> cubre la mecánica con más detalle.</p>
      <h2>Practicar con pareja</h2>
      <p>La forma la practican dos personas, así que en algún momento necesitarás una. El camino es la sala y no una aplicación: baila con gente en una jam y después pregúntale sin más si querría practicar fuera de ella. Mucha gente quiere una pareja de práctica y nunca lo pide.</p>
      <p>Acordad dos cosas antes de empezar: en qué parte del cuerpo estáis trabajando y que cualquiera de los dos puede parar en cualquier momento. Veinte minutos de compartir peso en un suelo sin música son una práctica completa.</p>
      <h2>La segunda visita</h2>
      <p>La segunda visita es más fácil y más extraña que la primera. Más fácil, porque ya conoces la forma de la noche y dónde está el agua. Más extraña, porque ahora tienes una memoria corporal de cómo se siente un baile, y el hueco entre eso y el principio del siguiente se nota.</p>
      <p>La mayoría de la gente que deja la IC la deja entre la primera y la tercera visita. Volver dos veces suele bastar para que se convierta en un hábito.</p>
      <h2>Si esta semana no hay nada</h2>
      <p>Miami no tiene un calendario central de IC, así que "¿hay jam esta noche?" no tiene una respuesta fija, y este sitio no adivina ni publica una fecha que no ha comprobado. Los lugares que pueden responder son quienes organizan, cuyas propias páginas y mensajes directos son la única fuente con autoridad, y la <a href="{R_JAMS}">página de jams</a>, donde cada entrada muestra la fecha en que se comprobó por última vez.</p>
      <p>El mapa mundial CI World Jam Map mantiene una <a href="https://www.contactimprov.com/florida.html" rel="noopener nofollow">página de Florida</a> con los listados de la propia comunidad, y es honesta sobre lo incompleta que está. El <a href="{R_DIRECTORY}">directorio</a> de aquí lista los estudios, quien organiza y las prácticas adyacentes que están vigentes y contestan a un mensaje.</p>
      <h2>Formar parte de la sala</h2>
      <p>Una escena sin institución la mantiene quien llega temprano. Tres cosas convierten la asistencia en pertenencia: llega al principio, porque el círculo de apertura es donde se fijan las reglas de la sala y donde es más fácil incluir a quien viene por primera vez. Ofrécete a ayudar a montar o a recoger, porque quienes hacen eso son quienes saben qué pasa el mes que viene. Y cuando estés listo, organiza.</p>
      <p>La mayoría de las jams del mundo existen porque una persona reservó una sala, así que <a href="{R_MIAMI}#start-one">empezar una en Miami</a> es el mecanismo real y no un premio de consolación. Si sabes dónde se baila este mes, <a href="{R_SUBMIT}">díselo a este sitio</a> y entra en el mapa.</p>
      <h2>El ritmo de un año en Miami</h2>
      <p>La práctica aquí viene por capas. Una clase o una jam semanal es el suelo. Los talleres están por encima. Una vez al año, en febrero, Love Burn en Virginia Key trae a Camp Contact, que lleva la improvisación de contacto, el acro yoga, la danza extática y el authentic relating como su programa.</p>
      <p>Ese campamento es la mayor concentración de improvisación de contacto que ocurre en Miami en un año, y es un festival y no una clase. Las fechas se mueven, así que lee la página de quien lo organiza; esta página no publica ninguna fecha.</p>
    </div>
    {sessions}
    <div class="prose">
      <p>{rank_note}</p>
      <h2>Qué no hará esta página</h2>
      <p>No te va a dar un calendario. Una fecha que no se ha verificado contra la página de quien organiza no aparece en este sitio, porque un listado desactualizado es peor que ningún listado. Una clase enseña las habilidades que una jam da por supuestas, y <a href="{R_CLASSES}">clases y talleres</a> cubre cómo juzgar una.</p>
    </div>
    {band("Dónde está de verdad el baile de esta semana", "Las páginas de quienes organizan son la única fuente actual, y cada entrada de arriba enlaza con una.", [("Jams en Miami", R_JAMS, "primary"), ("Profesorado y organizadores", R_DIRECTORY, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Cómo seguir practicando la Improvisación de Contacto en Miami</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/seguir-practicando", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_KEEP,
            "Cómo seguir practicando la Improvisación de Contacto en Miami",
            "Qué hacer después de una primera jam de Improvisación de Contacto en Miami: practicar sola y con pareja, la segunda visita, las semanas en que no hay nada y cómo mantenerte informada.",
            date_modified=LAST_CHECKED_ISO,
            lang="es",
        ),
        schema.breadcrumb(R_KEEP, "Seguir practicando", lang="es"),
    )
    return page(
        "Seguir practicando la Improvisación de Contacto",
        "Qué hacer después de tu primera jam de improvisación de contacto en Miami: practicar sola y en pareja, la segunda visita y las semanas sin nada.",
        R_KEEP,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- video room

def videos():
    count = videos_data.embed_count()
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Sala de vídeo</p>
    <h1>Nuestros propios filmes se están haciendo. Hasta entonces, esta sala es dar crédito a quien lo merece.</h1>
    <p class="lede">Esta jam todavía no ha rodado un vídeo, así que nada de esta página es nuestro. Cada filme de abajo lo hizo el canal que se nombra en él, se reproduce en el reproductor de ese canal y sigue siendo el trabajo de ese canal. Lo que estamos rodando para Miami aparece como lo que es: en producción, sin duración y sin fecha hasta que exista un archivo.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer(f"Cada filme de esta página lo hizo otra persona y se le acredita por su nombre: {count} piezas, cada una incrustada desde la plataforma que la aloja. Ninguna se rodó en Miami, y ninguna es de este sitio. Los filmes de la propia jam están en producción, listados aquí como piezas previstas; cada una sube al principio de esta página como nuestra solo cuando el archivo terminado se aloje aquí.", SHORT)}
    {videos_data.owned_room("es")}
    {videos_data.in_production("es")}
    {videos_data.reference_section("es")}
    {videos_data.credits("es")}
    {band("Ya has visto bastante", "Nada de esta página te va a enseñar lo que te enseñan dos minutos en un suelo con otra persona.", [("Jams en Miami", R_JAMS, "primary"), ("Recorrido de la primera jam", R_FIRST, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Sala de vídeo de Improvisación de Contacto</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/videos", CITE)}
  </div>
</section>
"""
    # No VideoObject here, on purpose: build/videos_data.py description strings are
    # English, and publishing English prose inside the structured data of a Spanish page
    # is the same defect that keeps Event schema off the Spanish jam pages. The list
    # below carries the film's own title and its watch URL and nothing else, and the
    # films stay published once, with full markup, from the English /videos page.
    films = [
        (v[2], videos_data.watch_url(v), "")
        for v in videos_data.VIDEOS
    ] + [
        (o[1], videos_data.content_url(o), "")
        for o in videos_data.OWNED
    ]
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_VIDEOS,
            "Sala de vídeo de Improvisación de Contacto",
            "La Improvisación de Contacto en vídeo: cada canal acreditado por su nombre, más los filmes que esta jam está rodando en Miami.",
            lang="es",
        ),
        schema.breadcrumb(R_VIDEOS, "Vídeos", lang="es"),
        schema.item_list(
            R_VIDEOS,
            "Filmes de Improvisación de Contacto en la sala de vídeo",
            films,
            lang="es",
        ),
    )
    return page(
        f"Vídeos de Improvisación de Contacto ({count})",
        "La Improvisación de Contacto en vídeo: los canales que los hicieron, con su nombre, y los filmes que esta jam rueda en Miami. Ninguno es nuestro todavía.",
        R_VIDEOS,
        body,
        jsonld=jsonld,
        lang="es",
    )


# ---------------------------------------------------------------- about

def about():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Acerca de</p>
    <h1>Qué es este sitio, y qué no es.</h1>
    <p class="lede">Una referencia independiente y sin ánimo de lucro sobre la Improvisación de Contacto en Miami. Sin membresía, sin comisión, sin estudio detrás. Organiza una única jam semanal propia, y lo dice allí donde esa jam aparece.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("miamicontactimprov.com es un recurso comunitario independiente que traza un mapa de la práctica de la Improvisación de Contacto (IC) en los condados de Miami-Dade y Broward. Publica lo que se puede verificar, dice con claridad lo que no, y acepta correcciones de cualquiera que esté en la escena. Organiza una sola sesión, la jam de los viernes en Miami, publicada en las mismas condiciones que cualquier otra entrada; no acepta reservas y no cobra nada por publicar.", SHORT)}
    <div class="prose">
      <h2>Por qué existe</h2>
      <p>La Improvisación de Contacto no tiene federación, ni licencia, ni organización central. Esa apertura es la razón de que se extendiera a todos los continentes, y es también la razón de que una ciudad como Miami pueda tener una práctica intermitente de décadas sin nada en internet que lo demuestre. Cuando la forma no tiene institución, el mapa hay que construirlo a mano.</p>
      <p>El mapa mundial CI World Jam Map de contactimprov.com lo hace a escala global desde los años noventa. Este sitio lo hace a escala de una ciudad, con más detalle del que puede llevar un listado global, y enlaza de vuelta al mapa mundial en lugar de competir con él.</p>
      <h2>Cómo funcionan aquí las entradas</h2>
      <ul>
        <li>Todo lo que se publica se comprueba antes contra la información que publica quien lo organiza.</li>
        <li>Si una sesión no se puede verificar, se lista como no verificada o se deja fuera, nunca se adivina.</li>
        <li>Nada está pagado. No hay entradas patrocinadas ni acuerdos de afiliación.</li>
        <li>Las retiradas son normales. Las sesiones terminan, los estudios cierran, quien organiza se muda, y la página se corrige.</li>
        <li>La exactitud importa más que la exhaustividad. Una página corta y honesta gana a una larga y equivocada.</li>
      </ul>
      <h2 id="submit">Publica, corrige o retira una entrada</h2>
      <p>Escribe a <a href="mailto:hello@miamicontactimprov.com">hello@miamicontactimprov.com</a>, o responde desde cualquier cuenta desde la que este sitio publique. En inglés o en español, cualquiera de los dos vale.</p>
      <p>Qué mandar para una jam o una clase:</p>
      {facts([
        ("Nombre", "Cómo se llama la sesión"),
        ("Dónde", "El nombre del estudio o del lugar, y la ciudad"),
        ("Cuándo", "Día, hora y cada cuánto"),
        ("Precio", "Entrada, donación o gratis"),
        ("Para quién es", "Abierta a todo el mundo, o se presupone experiencia previa"),
        ("Enlace", "Tu propia página, entrada de calendario o cuenta de redes"),
      ])}
      <p>Qué mandar para una entrada de profesorado: tu nombre, tu ciudad, qué enseñas y un enlace a tu propia página. Si prefieres no aparecer en ningún sitio, dilo y te retiramos sin preguntar por qué.</p>
      <p>Si eres propietario de un filme incrustado en la <a href="{R_VIDEOS}">sala de vídeo</a> y prefieres que no lo esté, una línea basta. Baja el mismo día.</p>
      <h2 id="our-jam">La única sesión que organiza este sitio</h2>
      <p>Desde octubre de 2026, quien mantiene este sitio organiza una jam abierta y semanal de Improvisación de Contacto los viernes, de 7:00 a 9:00 PM, en Inner Motion Dance Studio, en Miami (216 NE 1st Ave, Hallandale Beach). Está en la página de la <a href="{R_FRIDAY}">jam de los viernes</a> y en la <a href="{R_LIST}">lista de jams</a>, donde la entrada nombra a quien la organiza como cualquier otra. No va por encima de las demás sesiones, no es la razón de que las demás estén listadas, y se retira la semana en que deje de celebrarse. Todo lo demás en este sitio es la sesión de otra persona, publicada apoyándose en su propia página.</p>
      <h2>Correcciones</h2>
      <p>Si algo de aquí está mal, es más útil decírnoslo que ignorarlo. Las correcciones que retiran una afirmación son tan bienvenidas como las que añaden una sesión, y la página se cambia en lugar de anotarse.</p>
      <h2>Qué no es este sitio</h2>
      <ul>
        <li>No es un estudio, ni un servicio de reservas, ni una escuela. Organiza una jam y nada más.</li>
        <li>No evalúa, no certifica ni avala a profesorado. Nadie puede, en esta forma.</li>
        <li>No está afiliado a contactimprov.com, a Contact Quarterly ni a ningún festival.</li>
        <li>No media en disputas entre bailarinas o entre organizadores.</li>
      </ul>
    </div>
    {band("La página vale lo que vale la sala", "Si sabes dónde se baila este mes, eso es lo más útil que nos puedes mandar.", [("Escríbenos", "mailto:hello@miamicontactimprov.com", "primary"), ("Leer la página de Miami", R_MIAMI, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>Acerca de</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/acerca-de", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.webpage(
            R_ABOUT,
            "Acerca de Miami Contact Improv",
            "Qué es miamicontactimprov.com: un recurso comunitario independiente que traza un mapa de la Improvisación de Contacto en Miami-Dade y Broward. Cómo publicar, corregir o retirar una entrada.",
            lang="es",
        ),
        schema.breadcrumb(R_ABOUT, "Acerca de", lang="es"),
    )
    return page(
        "Acerca de Miami Contact Improv (publicar gratis)",
        "Un mapa independiente y sin ánimo de lucro de la Improvisación de Contacto en Miami. Cómo se comprueban las entradas y cómo publicar, corregir o retirar una.",
        R_ABOUT,
        body,
        jsonld=jsonld,
        lang="es",
    )




# ---------------------------------------------------------------- la jam de los viernes
FRIDAY_JAM_FAQ_ES = [
    ("¿Necesito pareja o experiencia para la jam de los viernes?",
     "No. Es una jam abierta y de todos los niveles. La mayoría llega sola, el calentamiento empieza de pie y en el suelo y no con cargadas, y puedes sentarte al borde a mirar todo el tiempo que quieras. A quien viene por primera vez se le espera, no se le tolera."),
    ("¿Hay que reservar?",
     "No. No hay entrada ni lista. Ven a la puerta de Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, entre las 7:00 y las 7:15 PM para llegar al círculo de apertura. Llegar más tarde está bien; irse antes, siempre."),
    ("¿Cuánto cuesta y cómo funciona la escala?",
     "20 dólares en la puerta, en una escala de 20 a 50. Paga lo que puedas dentro de ese rango y nadie te va a preguntar dónde te quedaste. El dinero cubre el estudio; la jam no se organiza con ánimo de lucro."),
    ("¿Dónde está exactamente?",
     "En el borde norte de Miami: Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009, justo pasada Aventura por la US-1. El código postal es de Hallandale Beach, en el condado de Broward, y el sitio lo imprime tal cual porque una dirección se copia, no se traduce. Miami Contact Improv cubre Miami-Dade y Broward."),
    ("¿Quién la organiza?",
     "Max Petrusenko, que también mantiene esta web. Por eso esta sesión aparece con una aclaración en cada página que la lista, y por eso no va por encima de ninguna otra entrada."),
    ("¿Qué ropa llevo y qué traigo?",
     "Ropa suelta que cubra espalda, hombros y rodillas, sin cremalleras ni hebillas, pies descalzos o calcetines blandos, una botella de agua llena y una toalla. Deja anillos, relojes y collares fuera. Los detalles están en la página de jams."),
    ("¿Hay música?",
     "A veces música baja durante el calentamiento, normalmente ninguna en la jam abierta. La Improvisación de Contacto se baila con la pareja, no con la pista."),
    ("¿Puedo venir solo a mirar?",
     "Sí. Mirar desde el borde es participar en esta forma, y nadie te va a sacar a la pista. Di en el círculo que hoy vienes a mirar y ahí se acaba la conversación."),
]


def friday_jam():
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FRIDAY_JAM_FAQ_ES)
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Viernes &middot; 7:00&ndash;9:00 PM &middot; Miami</p>
    <h1>La jam de los viernes en Miami.</h1>
    <p class="lede">Una jam abierta y semanal de Improvisación de Contacto en Inner Motion Dance Studio, en el borde norte de Miami. Sin pareja, sin experiencia, sin reserva. Primera sesión: viernes 2 de octubre de 2026.</p>
    <div class="btn-row">
      <a class="btn primary" href="https://maps.apple.com/?q=216+NE+1st+Ave,+Hallandale+Beach,+FL+33009" rel="noopener">216 NE 1st Ave, Hallandale Beach</a>
      <a class="btn secondary" href="{R_FIRST}">¿Nunca has ido a una jam?</a>
    </div>
    <p class="micro">20 dólares en la puerta, escala de 20 a 50. La organiza Max Petrusenko, que también lleva este sitio.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("La jam de los viernes es una jam semanal, abierta y de todos los niveles de Improvisación de Contacto en Miami, en Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009, todos los viernes de 7:00 a 9:00 PM a partir del 2 de octubre de 2026. Cuesta 20 dólares en la puerta en una escala de 20 a 50, no requiere pareja, experiencia previa ni reserva, y la organiza Max Petrusenko, quien mantiene miamicontactimprov.com.", SHORT)}
    {facts([
      ("Cuándo", "Todos los viernes, 7:00–9:00 PM"),
      ("Primera sesión", "Viernes 2 de octubre de 2026"),
      ("Dónde", "Inner Motion Dance Studio, 216 NE 1st Ave, Hallandale Beach, FL 33009"),
      ("Zona", "Borde norte de Miami, justo pasada Aventura por la US-1"),
      ("Precio", "20 dólares en la puerta, escala de 20 a 50"),
      ("Reserva", "Ninguna. Ven a la puerta"),
      ("Para quién", "Abierta y de todos los niveles. Se espera a quien viene por primera vez; mirar está bien"),
      ("Organiza", "Max Petrusenko"),
      ("Idioma", "Español e inglés"),
      ("Preguntas", "hello@miamicontactimprov.com"),
    ])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Cómo transcurre la tarde</h2>
    <div class="prose">
      <p><strong>7:00.</strong> Se abre. Cámbiate, bebe agua, busca un sitio en el suelo. Los zapatos se quedan fuera de la pista.</p>
      <p><strong>7:10, el círculo.</strong> Unos minutos. Quien organiza dice quién sostiene la sala y enuncia el protocolo: el consentimiento es continuo, puedes rechazar cualquier cosa sin dar razones, el borde es para descansar y mirar, nadie enseña sin que se lo pidan, nadie graba sin preguntar. Cualquiera puede añadir un límite o avisar de que se va antes. Si es tu primera vez, dilo; la sala te recibe en consecuencia.</p>
      <p><strong>Calentamiento.</strong> Una secuencia guiada de pie y en el suelo, y después unos minutos de <strong>pequeña danza</strong>. Algunos viernes sigue una pieza corta de material; se ofrece, no se exige.</p>
      <p><strong>La jam abierta.</strong> El tramo largo de la tarde, normalmente sin música. Las danzas empiezan con una mirada o una mano y terminan cuando cualquiera de las dos personas para. Descansar entre danzas es normal. Bailar en solitario forma parte de la forma.</p>
      <p><strong>8:50, cierre.</strong> Un círculo breve o un momento de quietud, y fuera a las 9:00 para que el estudio pueda cerrar.</p>
      <h2>La escala de precios</h2>
      <p>La puerta son 20 dólares y la escala llega a 50. El extremo bajo cubre la sala cuando viene gente suficiente; el alto es para quien pueda cargar con más y quiera que la jam siga en pie. Elige en privado, entrégalo, listo. A nadie se le deja fuera de una primera jam por dinero: si esta semana los 20 dólares son la barrera, ven igual y dilo en la puerta.</p>
      <h2>Cómo llegar</h2>
      <p>Inner Motion Dance Studio está en el 216 NE 1st Ave de Hallandale Beach, justo al este de la US-1 (Federal Highway) y al norte de Hallandale Beach Boulevard. Desde Miami es la primera ciudad pasada la línea del condado después de Aventura; desde Fort Lauderdale queda al sur de Hollywood. Si necesitas datos de aparcamiento o de acceso antes de venir, <a href="mailto:hello@miamicontactimprov.com">escribe</a> y tendrás respuesta antes del viernes.</p>
      <h2>Quién sostiene la sala</h2>
      <p>Max Petrusenko organiza la jam. También construye y mantiene esta web, y por eso esta página se lee como quien organiza describiendo su propia sesión, y por eso la <a href="{R_LIST}">lista de jams de Miami-Dade y Broward</a> lleva la misma aclaración junto a la entrada. El resto de este sitio publica las sesiones de otras personas apoyándose en sus propias páginas; esta se publica apoyándose en esta página, y se retirará la semana en que deje de celebrarse en lugar de quedarse aquí pareciendo vigente.</p>
      <h2>Reglas básicas</h2>
      <p>La versión completa está en <a href="{R_SAFETY}">seguridad y consentimiento</a>. La corta: mantén un solo punto de contacto, ten tus pies disponibles, rueda al caer en lugar de frenar con los brazos, di que no cuando quieras decir que no y acepta un no sin preguntar por qué, sal de una danza cuando termine, y no enseñes si no te lo piden.</p>
      <h2>Preguntas sobre la jam de los viernes</h2>
      {faq_html}
    </div>
    {band("¿Vienes este viernes?", "No hace falta avisar a nadie. Si quieres preguntar algo antes, con un correo basta y se responde antes del fin de semana.", [("Escribe a quien organiza", "mailto:hello@miamicontactimprov.com", "primary"), ("Tu primera jam, paso a paso", R_FIRST, "secondary"), ("Todas las sesiones verificadas", R_LIST, "secondary")])}
    {cite_block("Miami Contact Improv (2026). <em>La jam de los viernes en Miami</em>. miamicontactimprov.com. https://miamicontactimprov.com/es/jam-de-los-viernes", CITE)}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation(lang="es"),
        schema.webpage(
            R_FRIDAY,
            "Jam de Improvisación de Contacto de los viernes en Miami",
            "Una jam semanal, abierta y de todos los niveles de Improvisación de Contacto en Miami, en Inner Motion Dance Studio (216 NE 1st Ave, Hallandale Beach), los viernes de 7:00 a 9:00 PM desde el 2 de octubre de 2026. 20 dólares en la puerta, escala de 20 a 50. La organiza Max Petrusenko.",
            date_modified=listings.FRIDAY_JAM_VERIFIED,
            lang="es",
        ),
        schema.breadcrumb(R_FRIDAY, "Jam de los viernes", lang="es"),
        schema.faq(FRIDAY_JAM_FAQ_ES, lang="es"),
        listings.friday_jam_event(),
    )
    return page(
        "Jam de Improvisación de Contacto en Miami, viernes 7–9 PM",
        "Jam abierta y semanal de Improvisación de Contacto en Miami, viernes de 7 a 9 PM en Inner Motion Dance Studio, 216 NE 1st Ave. De 20 a 50 dólares, sin pareja ni reserva.",
        R_FRIDAY,
        body,
        jsonld=jsonld,
        lang="es",
    )
