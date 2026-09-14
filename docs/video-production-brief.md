# Video production brief

The films this jam shoots for `miamicontactimprov.com/videos`, in the order they
should be shot. `/videos` currently carries 22 films that belong to other people.
This brief is the plan to replace borrowed supply with our own.

Read `SKILL.md` for the property and `build/videos_data.py` for the code contract.
The page reads its planned list from `videos_data.PLANNED`; this document is the
source of truth for what each piece is, who it is for, and when it counts as ours.

## The rule that makes a film ours

A piece becomes ours only when **all** of these are true:

1. We shot it. Not re-cut, not re-uploaded, not downloaded from anywhere.
2. The finished file is committed at `site/media/<slug>.mp4` with a poster at
   `site/media/<slug>-poster.jpg`, so it is served from `miamicontactimprov.com`
   itself. The deploy copies `site/` as-is, so committing the file is publishing it.
3. It is added to `OWNED` in `build/videos_data.py` as
   `(slug, title, duration, filmedOn, location)`:
   - `duration` is read off the finished file (`ffprobe` or the player's own clock).
     Never estimated. It renders as an ISO 8601 duration in the schema.
   - `filmedOn` is the day the camera rolled, `YYYY-MM-DD`. Never the publish date.
   - `location` is where it was shot.
4. Its `VideoObject` carries `contentUrl` pointing at our own file, and
   `creator`/`publisher` both reference this site's Organization (`#organisation`).
   That is the only case where our name goes on a film.
5. The title's bracket count is recounted. It is now built from
   `videos_data.embed_count()`, so it cannot drift, and `tools/gate.py` fails the
   build if the number in the title does not equal the number of films on the page.

What never happens: a third-party film gets our name put on it, and a film of ours
is embedded from someone else's player. A film that is not yet shot does not get a
duration, a date, or a video element — it stays a title in the planned list with no
claims attached.

`tools/gate.py::check_video_room` enforces the credit side. `guard_owned()` stops the
build if an `OWNED` entry has no committed file, so the page cannot name a film that
does not exist.

## Production order

Priority is not by effort. It is by what nobody else has and what the search supply
is missing.

### 1. What actually happens at a contact improv jam

- **Target query shape:** `contact improv miami` / `contact improvisation miami` —
  local intent, the query the site exists to answer. Secondary: `what happens at a
  contact improv jam`, `contact jam what to expect`.
- **Why first:** the 2026 research pass found nothing shot in Miami at all. There is
  no competing local film, so this is the one piece of supply we can own outright.
  It is also the piece that answers the hesitation that keeps people home.
- **Page title:** `What actually happens at a contact improv jam (Miami)`
- **Meta description:** `Walk into a Miami contact improv jam and see it end to end:
  the opening circle, the first five minutes, what nobody tells you, and how to leave.`
- **H1 on the embed page:** the same as the title, minus the bracket.
- **On-page tags/topics:** jam, Miami, first jam, what to expect, opening circle,
  etiquette, boundaries.
- **Target length:** 6–9 minutes. Long enough to hold the whole arc of a session,
  short enough to be watched before going.
- **Filmed where:** at a real Miami jam, with the organiser's written permission
  before the camera comes out. Consent from everyone who may end up in frame; anyone
  who does not want to be on film is framed out or the shot is not used. No faces
  without a release.
- **Shape:** opening circle → the first dances → the moment someone sits down and
  comes back → the end, when the room empties. Narration only where the picture does
  not carry it.
- **Extra rule for this one:** the title must stay true if the jam it was shot at
  changes its format later. Do not generalise "this jam" into "every jam".

### 2. Contact improvisation for beginners: the first 20 minutes

- **Target query shape:** `contact improvisation for beginners`, `contact improv
  basics`, `contact improv warm up`, `how to start contact improvisation`.
- **Why second:** the top YouTube result for the beginner query is nine years old.
  Beginner intent is the largest slice of the search and has the stalest supply.
- **Page title:** `Contact improvisation for beginners: the first 20 minutes`
- **Meta description:** `The first twenty minutes of a beginner contact improv
  session, start to finish: the warm-up, the first exercise, the first weight
  share, and what to do when you do not know what to do.`
- **On-page tags/topics:** beginners, warm up, first class, weight sharing, rolling,
  exercises, no experience needed.
- **Target length:** 18–24 minutes, and it should be cut so the first 3 minutes work
  standalone as the answer to `how do I start`.
- **Filmed where:** a real beginners' session or a jam's warm-up, in a studio with
  enough light to see bodies and floor. Not a staged demo in an empty room: the
  point is that a beginner can recognise themselves in it.
- **Shape:** the warm-up as it is actually given → one exercise, explained once,
  then shown at full speed → the first weight share → a note on what to do when it
  goes wrong. Chapter markers at each step.

### 3. Rolling point of contact, weight sharing, floorwork

- **Target query shape:** `contact improvisation exercises`, `contact improv
  techniques`, `rolling point of contact`, `weight sharing`, `contact improv lift`,
  `floor work contact improv`, `contact improvisation tutorial`.
- **Why third:** technique intent repeats every week and is served almost entirely
  by unedited workshop footage. This is also the piece the rest of our pages can
  cite, because the glossary already defines these terms.
- **Page title:** `Rolling point of contact, weight sharing and floorwork`
- **Meta description:** `Rolling point of contact, weight sharing and floorwork shown
  slowly enough to copy: the mechanics, the common mistake, and the way back to
  standing.`
- **On-page tags/topics:** exercises, techniques, tutorial, floor work, lift, carry,
  counterbalance, spotting, rolling point of contact.
- **Target length:** 25–40 minutes total, split into 4–6 chapters of 4–8 minutes so
  each term has its own answerable segment.
- **Filmed where:** a studio, on a floor we are allowed to mark, with two dancers who
  already work together. Cut between the wide shot and a close-up of the contact
  point; the close-up is the whole value of this piece.
- **Shape:** one idea per chapter, named with the glossary term it belongs to, and
  linked back to `/glossary#<term>`. Slow shots, then full speed, then the mistake.

### 4. Is contact improv sexual?

- **Target query shape:** `is contact improv sexual`, `contact improvisation
  boundaries`, `is contact improv inappropriate`, `contact improv touching`.
- **Why fourth, and why it cannot be skipped:** it is high-intent, it has no good
  video supply, and it is the single question that stops people attending. Answering
  it in text on `/safety-and-consent` is already done; a video is what makes the
  answer travel.
- **Page title:** `Is contact improv sexual?`
- **Meta description:** `A direct answer, with the boundaries that make contact
  improvisation safe: what consent means in a jam, what you may always decline, and
  what the practice is not.`
- **On-page tags/topics:** consent, boundaries, safety, what CI is not, touch,
  first jam, saying no.
- **Target length:** 5–8 minutes. This is an answer, not a survey.
- **Filmed where:** a studio or the same room the jam uses, talking to camera with
  dance footage cut under it. People answering in their own words, not a narrator.
- **Content rules:** no claims about how other scenes run; state what this practice's
  protocol is and what a jam's stated boundaries are. Nothing presented as legal or
  medical advice. This site is not a teacher and does not invent authority — that
  rule holds on film exactly as it does in the listings.
- **Link:** this piece belongs next to `/safety-and-consent` and should be embedded
  there as well as on `/videos`.

### 5. The small dance

- **Target query shape:** `the small dance`, `small dance contact improvisation`,
  `standing practice contact improv`, `Steve Paxton small dance`.
- **Why fifth:** the site already owns the definition of this term — one
  `DefinedTerm` at `/glossary#small-dance` — so the film has a page to land on and
  the page has a film to gain. It is the cheapest piece to shoot and the clearest
  demonstration of the whole point of the form.
- **Page title:** `The small dance`
- **Meta description:** `The small dance as it is practised: standing, letting the
  body find its own balance, and noticing the movement that is already happening.
  Defined in the glossary.`
- **On-page tags/topics:** the small dance, standing practice, stillness, balance,
  Paxton, awareness, solo.
- **Target length:** 8–12 minutes, shot in one take with no cuts if possible. A
  practice film that is edited like a performance piece has already missed it.
- **Filmed where:** anywhere with a floor and no traffic — a studio, a dock, a shaded
  yard. Natural sound. No music: the point is noticing.
- **Link:** the page must link to `/glossary#small-dance` as the definition of the
  term it is teaching, and the glossary entry links back to the film.

## After the first five

The reference section stays. It is not a placeholder to be deleted once we have our
own films: other people's work, credited by name, is a legitimate part of the room.
The change is that the top of the page is ours.

Candidates for the next round, in the order they pay: a full jam from a corner
camera with no commentary; a lift-and-carry piece for people told they are the wrong
size to fly; a "what a jam is not" piece on performance versus practice; and one
film in Spanish, because Miami.
