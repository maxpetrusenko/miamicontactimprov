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

# The Spanish routes, mirroring build/locales.py. Kept as literals here so a link in
# Spanish prose is visible where it is written; tools/gate.py fails the build if any of
# them stops resolving to a file.
R_HOME = "/es/"
R_WHATIS = "/es/que-es-la-improvisacion-de-contacto"
R_JAMS = "/es/jams"
R_FIRST = "/es/tu-primera-jam"
R_LIST = "/es/jams-miami-dade-broward"
R_FAQ = "/es/preguntas-frecuentes"
R_SAFETY = "/es/seguridad-y-consentimiento"

# English-only pages. Linked with an explicit lang note in the anchor so a reader is
# told the destination is in English before they click.
R_MIAMI = "/miami"
R_CLASSES = "/classes"
R_DIRECTORY = "/directory"
R_GLOSSARY = "/glossary"
R_HISTORY = "/history"
R_VIDEOS = "/videos"
R_KEEP = "/keep-practising"
R_SUBMIT = "/about#submit"

SHORT = "Respuesta breve"
CITE = "Cita esta página"

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
            '<a href="/directory" lang="en" hreflang="en">directorio (en inglés)</a> son donde '
            "está realmente la respuesta.</p></div>"
        )
    return (
        '<div class="prose"><h2>Qué se está practicando en Miami-Dade y Broward</h2>'
        f"<p>{len(listings.SESSIONS)} entradas. Cada una nombra a quien la organiza, dónde es, "
        "cuándo es, cuánto cuesta y qué tipo de práctica es en realidad, y cada una lleva la "
        "fecha en que se abrió y se leyó su fuente. Aparecen en el orden en que se verificaron. "
        "Esta página no clasifica nada: ninguna entrada está pagada y ninguna se recomienda por "
        "encima de otra.</p>"
        f'<p>{LIST_VALUE_NOTE}</p>'
        f'<ul class="dir-list">{_session_items()}</ul></div>'
    )


def _sessions_for_stage():
    """The session block for the stage pages, which carry no Event schema."""
    return _sessions_block()


# ---------------------------------------------------------------- home
def home():
    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Miami &middot; Miami Beach &middot; South Florida</p>
    <h1>Dos personas, un punto de contacto compartido, y lo que pase después.</h1>
    <p class="lede">La Improvisación de Contacto es una forma de danza que puedes empezar hoy y no terminar de aprender nunca. Este sitio es el mapa de trabajo de dónde ocurre en Miami: las jams, las clases, quienes enseñan, el vocabulario y la historia que hay detrás.</p>
    <div class="btn-row">
      <a class="btn primary" href="{R_JAMS}">Encuéntralo en Miami</a>
      <a class="btn secondary" href="{R_WHATIS}">¿Qué es la IC?</a>
    </div>
    <p class="micro">Sin membresía. Sin autoridad central. Este es un recurso comunitario, no un estudio.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("La Improvisación de Contacto (IC), conocida internacionalmente como <em>contact improvisation</em> o <em>CI</em>, es una forma de danza en pareja construida a partir de un único punto de contacto en movimiento, normalmente la espalda o los hombros, a través del cual dos personas comparten peso y siguen la gravedad, el momento y el impulso en lugar de una coreografía. Comenzó en Estados Unidos en 1972 con el bailarín y coreógrafo Steve Paxton, y no tiene organismo que la licencie, ni uniforme, ni programa fijo. En Miami se practica en jams, clases y talleres en los condados de Miami-Dade y Broward.", SHORT)}
    {facts([
      ("Qué es", "Una danza improvisada en pareja alrededor del peso compartido y un punto de contacto rodante"),
      ("Cuándo empezó", "1972, Estados Unidos, desarrollada por Steve Paxton"),
      ("Quién puede practicarla", "Cualquiera. Para empezar no hacen falta formación en danza, pareja ni flexibilidad"),
      ("Qué es una jam", "Una sesión abierta y sin guía. Se llega y se sale cuando se quiere, se baila o se mira"),
      ("Cuánto cuesta en Miami", "Lo fija quien organiza. Las jams comunitarias suelen ser económicas o a donación"),
      ("Qué hay que llevar", "Ropa cómoda, agua, pies descalzos o calzado blando, y disposición a decir no"),
      ("Dónde ocurre aquí", "Estudios, centros culturales, parques y playas en Miami-Dade y Broward"),
    ])}
    <div class="prose">
      <p>La forma es deliberadamente abierta. No hay federación que certifique quién puede enseñarla, ni organismo que decida qué cuenta como tal. Por eso la escena de una ciudad se construye con personas que organizan por su cuenta y salas prestadas, y no con una institución única; y por eso un mapa como este resulta útil.</p>
    </div>
    {cite_block("Miami Contact Improv (2026). <em>Improvisación de Contacto en Miami</em>. miamicontactimprov.com. Recuperado de https://miamicontactimprov.com/es/", CITE)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Empieza desde donde estás</h2>
    {cards([
      ("Nunca lo he hecho", "Mirar primero, bailar después", "Cómo se ve una jam desde dentro, y por qué mirar es una forma legítima de participar.", R_FIRST),
      ("Busco una sesión", "Jams y práctica abierta", "Qué es una jam abierta, cómo suele funcionar la sala y qué decir al llegar.", R_JAMS),
      ("Quiero que me enseñen", "Clases y talleres", "Series para principiantes, talleres e intensivos, y qué mirar en quien enseña.", R_CLASSES),
      ("Aprender el vocabulario", "Glosario", "Jam, score, small dance, underscore, spotting, compartir peso y el resto del vocabulario de trabajo.", R_GLOSSARY),
      ("Curiosidad por la forma", "Historia y principios", "De dónde viene la IC, quién la construyó y qué ideas tomó del aikido, la danza posmoderna y la somática.", R_HISTORY),
      ("Necesito las reglas básicas", "Seguridad y consentimiento", "Límites, spotting, qué se espera de ti y qué puedes rechazar siempre.", R_SAFETY),
    ])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Por qué una jam no es una clase</h2>
    <div class="prose">
      <p>Una <strong>clase</strong> te da una habilidad. Una <strong>jam</strong> te da la situación en la que esa habilidad se vuelve útil. La mayoría de las jams no tienen profesor y tienen poca o ninguna música; la gente llega, encuentra pareja o baila sola, y se va cuando termina. Normalmente hay un borde de la sala para sentarse, mirar y descansar, y usarlo es lo normal, no una descortesía.</p>
      <p>Si solo has bailado coreografías fijas, los primeros veinte minutos de una jam pueden parecer sin forma. Ayuda saber que eso es la forma, y no su fracaso. No estás esperando instrucciones: estás escuchando a un cuerpo que ya sabe caer sin hacerse daño y volver a levantarse.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>La única regla que sostiene todas las demás</h2>
    <div class="prose">
      <p>La Improvisación de Contacto funciona porque cualquiera de las dos personas puede parar en cualquier momento, por cualquier motivo, sin explicación. Quien está siendo levantado puede poner un pie en el suelo. Quien está siendo sostenido puede apartarse. La danza continúa. Quienes la practican llaman a esto la negociación, y ocurre a través del peso, la respiración y pequeñas señales físicas mucho antes de que alguien hable.</p>
      <p>Escrito suena abstracto. En la sala es lo más práctico que vas a aprender, y es la razón por la que vuelve gente que nunca se había considerado bailarina.</p>
    </div>
    {band("¿Nuevo en Miami o nuevo en esto?", "Dinos que existes y te añadimos al mapa. Jams, clases, profesorado, estudios, festivales y grupos de práctica recurrente tienen cabida aquí.", [("Publica una entrada", R_SUBMIT, "primary"), ("Leer el directorio (en inglés)", R_DIRECTORY, "secondary")])}
  </div>
</section>
"""
    jsonld = schema.render(
        schema.organisation("es"),
        schema.website("es"),
        schema.webpage(
            R_HOME,
            "Improvisación de Contacto en Miami | Miami Contact Improv",
            "Improvisación de Contacto en Miami: jams, clases, quién enseña, vídeo e historia. Un mapa comunitario e independiente de la IC en Miami-Dade y Broward.",
            lang="es",
        ),
        {
            "@type": "Place",
            "@id": schema.SITE + "/#place",
            "name": "Miami, Florida",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Miami",
                "addressRegion": "FL",
                "addressCountry": "US",
            },
            "geo": {"@type": "GeoCoordinates", "latitude": 25.7617, "longitude": -80.1918},
        },
    )
    return page(
        "Improvisación de Contacto en Miami [Guía 2026]",
        "Improvisación de Contacto en Miami: qué es, dónde están las jams, quién la enseña y cómo empezar. Un mapa comunitario de la IC en Miami-Dade y Broward.",
        R_HOME,
        body,
        jsonld=jsonld,
        lang="es",
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
      <p>La IC se extendió por giras, enseñanza y un boletín en papel, no por una organización, y por eso la mayoría de las ciudades desarrolló su escena sin dirección central. Miami no es una excepción: aquí la práctica pasa por profesores individuales, alquileres de estudio, parques y la comunidad de danza y movimiento del sur de Florida, y no por una institución única. <a href="{R_WHATIS}">Esta página</a> describe lo que se sabe hoy, y la <a href="/miami" lang="en" hreflang="en">página de Miami (en inglés)</a> traza el mapa de lo que se ha podido verificar.</p>
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
            about=[{"@id": schema.SITE + "/#place"}, {"@id": schema.SITE + "/glossary#terms"}],
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
      <p>Miami no tiene un calendario central de IC, así que &laquo;¿hay jam hoy?&raquo; no tiene una respuesta fija y una página como esta queda desactualizada en el momento en que cambia una sala o un horario. Cada sesión de arriba lleva la fecha en que se abrió y se leyó su fuente: <strong>{LAST_CHECKED_BY_LANG['es']}</strong>. Trata una fecha antigua como una pista que hay que comprobar, no como un hecho.</p>
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
      <p>Qué pasa de verdad cuando entras &mdash; la llegada, el círculo de apertura, los primeros diez minutos de baile, las frases que puedes decir cuando quieres parar y cuándo irte &mdash; está en <a href="{R_FIRST}">tu primera jam, paso a paso</a>. Qué hacer en las semanas siguientes, incluidas las semanas en que no hay nada, está en <a href="{R_KEEP}" lang="en" hreflang="en">seguir practicando (en inglés)</a>.</p>
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
        "propia sesión, y cada entrada lleva la fecha en que se abrió y se leyó su fuente: "
        f"<strong>{LAST_CHECKED_BY_LANG['es']}</strong>. Esta página no clasifica nada. Las "
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
      <p>El coste, ir solo, la forma física, mirar en lugar de bailar y el camino para principiantes están respondidos en una línea cada uno en <a href="{R_FAQ}">la página de preguntas</a>. Cómo suele desarrollarse una sesión completa está en <a href="{R_JAMS}">jams</a>, y qué enseña de verdad una clase para principiantes está en <a href="{R_CLASSES}" lang="en" hreflang="en">clases (en inglés)</a>. Si nunca has leído nada sobre la forma, empieza por <a href="{R_WHATIS}">qué es la Improvisación de Contacto</a>.</p>
    </div>
    {band("¿Listo para ir?", "Cada sesión de arriba enlaza con la página de quien la organiza, que es la única fuente que conoce el horario de esta semana.", [("Jams en Miami", R_JAMS, "primary"), ("Clases y talleres (en inglés)", R_CLASSES, "secondary")])}
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
    <p class="lede">Seis entradas, cada una con quien la organiza, la sala, el precio, la modalidad y la fecha en que se comprobó. Más las dos cosas que casi todas las listas se equivocan sobre Florida, y un relato honesto de la jam de Broward que no pudimos encontrar.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {answer("La práctica recurrente de Improvisación de Contacto que pudimos verificar en Miami-Dade y Broward es una clase semanal de todos los niveles en Dance Arts Miami los martes por la tarde-noche, dos talleres con fecha en Miami de una práctica adyacente al contacto que fusiona acro yoga, masaje tailandés y contact improv, un campamento anual de festival en Virginia Key, y dos encuentros recurrentes de danza consciente en el condado de Broward que anuncian un componente de contact improv entre otras prácticas. No se pudo verificar ninguna jam ni clase recurrente de Improvisación de Contacto en el condado de Broward a partir de una fuente que publique sobre sí misma. Cada entrada de abajo nombra la página en la que se leyó y la fecha en que se comprobó.", SHORT)}
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
      <h3>Una jam de improvisación de contacto en el condado de Broward</h3>
      <p>No encontrada. Se buscó en Fort Lauderdale, Hollywood, Davie, Pembroke Pines, Sunrise, Plantation, Weston, Coral Springs, Hallandale Beach y Miramar, contra páginas de organizadores, listados de Eventbrite y Meetup, y directorios de danza consciente. Lo que hay en Broward es danza extática, que sí está en esta página con su modalidad declarada, y un puñado de profesores que se describen a sí mismos como de Improvisación de Contacto en el propio directorio de miembros del World Jam Map y que no publican sesión, sala ni fecha. Un nombre en un directorio no es una jam, así que no se lista aquí.</p>
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
      <p>Cómo es de verdad asistir a cada sesión y cómo transcurre una jam desde el círculo de apertura hasta el último baile está en <a href="{R_JAMS}">jams</a> y <a href="{R_FIRST}">tu primera jam, paso a paso</a>. Qué hacer en las semanas siguientes a la primera está en <a href="{R_KEEP}" lang="en" hreflang="en">seguir practicando (en inglés)</a>. Qué es la Improvisación de Contacto, si nunca has leído nada sobre ella, empieza en <a href="{R_WHATIS}">qué es la Improvisación de Contacto</a>.</p>
      <p>Esta página no organiza ninguna de estas sesiones, no cobra por listarlas y no las clasifica. Es un mapa de una escena sin autoridad central, y no es el mapa.</p>
    </div>
    {band("¿Organizas una sesión en Miami-Dade o Broward?", "Manda el horario, la sala, el precio y dónde lo publicas. Una entrada aquí significa una sola cosa: quien la organiza lo publica y nosotros comprobamos la página. No es un aval.", [("Publicar una sesión", R_SUBMIT, "primary"), ("El directorio más amplio (en inglés)", R_DIRECTORY, "secondary")])}
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
     "La improvisación de contacto no tiene organismo de certificación, así que no hay registro que consultar. Lo que se pudo verificar cuando esta página se comprobó por última vez es una clase recurrente de todos los niveles: Contact Improv &mdash; ALL LEVELS en Dance Arts Miami, martes de 18:00 a 19:00. Todo lo demás pasa por organizaciones que responden a un mensaje directo, listadas en el <a href=\"/directory\" lang=\"en\" hreflang=\"en\">directorio (en inglés)</a>."),
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
         "El coste, ir solo, la forma física y si puedes simplemente mirar: las preguntas que la gente hace antes de su primera sesión, respondidas sin discurso de venta. La noche en sí se recorre en <a href=\"/es/tu-primera-jam\">tu primera jam, paso a paso</a>, y las semanas siguientes están en <a href=\"/keep-practising\" lang=\"en\" hreflang=\"en\">seguir practicando (en inglés)</a>.",
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


