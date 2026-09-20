#!/usr/bin/env python3
"""Negative controls for the Event endDate / performer rules in tools/gate.py.

A rule that has never been seen to fail is not known to work. Each case below breaks one
thing - a field on a served Event, or a row in the listing tables the field is built from -
and asserts that the real gate reports the finding it is supposed to report, with exit code
1. Exit 0 means the rule did not fire, exit 2 means the gate could not run at all; both are
failures here, because neither proves anything about the rule.

The baseline is checked first: the unmodified site must pass, so a later finding can only
have been caused by the injection.

Usage:  python3 tools/negative_control_events.py [--site site] [--keep]
"""

import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "tools" / "gate.py"
LD_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

JAM_ID = "#event"
KAMA_ID = "2026-10-18-kama-flight"
ECSTATIC_ID = "2026-09-26-ecstatic-dance-miami"


def _node(graph, suffix):
    """Exactly one node whose @id ends with `suffix`, or an assertion about the fixture."""
    hits = [n for n in graph.get("@graph", [])
            if isinstance(n, dict) and str(n.get("@id", "")).endswith(suffix)]
    assert len(hits) == 1, f"fixture expects one node ending {suffix!r}, found {len(hits)}"
    return hits[0]


def strip_field(suffix, field):
    def apply(graph):
        node = _node(graph, suffix)
        assert field in node, f"fixture expects {field!r} on {suffix!r}, it is not there"
        del node[field]
        return True
    return apply


def set_field(suffix, field, value):
    def apply(graph):
        node = _node(graph, suffix)
        assert field in node, f"fixture expects {field!r} on {suffix!r}, it is not there"
        assert node[field] != value, f"fixture value for {field!r} is already the served value"
        node[field] = value
        return True
    return apply


# Markup cases: the built page is broken, the tables stay honest.
PAGE_CASES = [
    ("jams.html", strip_field(KAMA_ID, "performer"), "event-performers",
     "carries no performer", "performer removed from /jams Kama Event"),
    ("jams.html", strip_field(KAMA_ID, "endDate"), "event-dates",
     "carries no endDate", "endDate removed from /jams Kama Event"),
    ("jams.html", set_field(KAMA_ID, "endDate", "2026-10-18T14:00:00-04:00"), "event-dates",
     "ends at or before it starts", "endDate moved before startDate on /jams"),
    ("jams.html", set_field(KAMA_ID, "endDate", "2026-10-18T17:45:00-04:00"), "event-dates",
     "but the source publishes 16:30", "endDate disagrees with the row that built it"),
    ("jams.html", set_field(KAMA_ID, "performer", {"@type": "Person", "name": "Someone Else"}),
     "event-performers", "but build/listings.py names", "performer credits the wrong party"),
    ("miami-jams.html", strip_field(ECSTATIC_ID, "endDate"), "event-dates",
     "carries no endDate", "endDate removed from /miami-jams Ecstatic Dance Event"),
    ("es/jam-de-los-viernes.html", strip_field(JAM_ID, "performer"), "event-performers",
     "carries no performer", "performer removed from the Spanish Friday jam"),
]

# Data cases: the served page is untouched and the listing row that justifies a field is
# changed instead. These run the gate from a copy of build/ and tools/, so the real tables in
# this working tree are never edited.
DATA_CASES = [
    (
        'EVENT_DATES["Kama Flight \\u2014 Flight Workshop"] = [\n'
        '    ("2026-10-18", "Skanda Yoga, Miami, FL", "15:00"),\n'
        '    ("2026-11-15", "Skanda Yoga, Miami, FL", "15:00", "16:30"),\n'
        ']\n',
        [("event-dates", "no source for this occurrence publishes an end time"),
         ("local-listings", "occurrence row has 3 fields")],
        "the served endDate is no longer backed by a row with an end time",
    ),
    (
        'EVENT_PERFORMERS.pop("Ecstatic Dance Miami \\u2014 Full Moon Immersion", None)\n',
        [("event-performers", "that build/listings.py does not"),
         ("local-listings", "has no EVENT_PERFORMERS entry")],
        "a served performer is no longer backed by a row that names it",
    ),
    (
        'del EVENT_PERFORMERS[FRIDAY_JAM_NAME]\n',
        [("event-performers", "that build/listings.py does not"),
         ("local-listings", "the Friday jam has no EVENT_PERFORMERS entry")],
        "the Friday jam's performer row is gone, so the served credit is unexplained",
    ),
]


def run_gate(site, root=ROOT):
    proc = subprocess.run(
        [sys.executable, str(root / "tools" / "gate.py"), "--site", str(site)],
        capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def mutate_page(path, apply):
    """Rewrite the JSON-LD graph of `path` with `apply`; True if it changed anything."""
    changed = False
    holder = {}

    def repl(match):
        nonlocal changed
        graph = json.loads(match.group(2))
        if not apply(graph):
            return match.group(0)
        holder["graph"] = graph
        changed = True
        return match.group(1) + json.dumps(graph, ensure_ascii=False) + match.group(3)

    rewritten = LD_RE.sub(repl, path.read_text(encoding="utf-8"))
    if not changed:
        return False
    path.write_text(rewritten, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=str(ROOT / "site"))
    ap.add_argument("--keep", action="store_true",
                    help="keep the scratch copies for inspection")
    args = ap.parse_args()
    site = pathlib.Path(args.site).resolve()
    if not site.is_dir():
        print(f"negative-control: no site at {site}", file=sys.stderr)
        return 2

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="negative-control-"))
    failures = []

    try:
        # Baseline: the site as built must pass before anything is broken.
        code, out = run_gate(site)
        if code != 0:
            print("negative-control: the site does not pass the gate unmodified - fix that "
                  "first, the injections below would prove nothing")
            print(out)
            return 2
        print("baseline: gate exits 0 on the built site, so any finding below is injected")

        # Markup cases: one working copy of the site, one page restored per case.
        clean = tmp / "site"
        shutil.copytree(site, clean)
        print(f"markup cases ({len(PAGE_CASES)}): site copy at {clean}")
        for page, apply, check, needle, label in PAGE_CASES:
            target = clean / page
            pristine = site / page
            shutil.copyfile(pristine, target)
            if not mutate_page(target, apply):
                failures.append(f"{label}: the fixture did not change the page (vacuous test)")
                print(f"  FAIL {label}: fixture did not apply")
                continue
            code, out = run_gate(clean)
            ok = code == 1 and check in out and needle in out
            if ok:
                print(f"  ok   exit=1 [{check}] {needle!r} <- {label}")
            else:
                why = ("green, so the rule did not fire" if code == 0 else
                       f"exit={code}" + (", the gate could not run" if code == 2 else ""))
                if code == 1 and (check not in out or needle not in out):
                    why = f"exit=1 but no [{check}]/{needle!r} in the output"
                failures.append(f"{label}: {why}")
                print(f"  FAIL {label}: {why}")
                print("\n".join(line for line in out.splitlines()
                                if line.startswith("[") or line.startswith("findings")))

        # Data cases: copied build/ + tools/, so the served pages stay exactly as built.
        for index, (snippet, expectations, label) in enumerate(DATA_CASES, start=1):
            root = tmp / f"tree{index}"
            (root / "tools").mkdir(parents=True)
            shutil.copytree(ROOT / "build", root / "build")
            shutil.copyfile(GATE, root / "tools" / "gate.py")
            with (root / "build" / "listings.py").open("a", encoding="utf-8") as handle:
                handle.write(f"\n\n# negative-control injection\n{snippet}")
            code, out = run_gate(site, root=root)
            missing = [(c, n) for c, n in expectations if not (c in out and n in out)]
            if code == 1 and not missing:
                print(f"  ok   exit=1 {[n for _c, n in expectations]} <- {label}")
            else:
                why = ("green, so the rule did not fire" if code == 0 else
                       f"exit={code}" + (", the gate could not run" if code == 2 else ""))
                if code == 1 and missing:
                    why = f"exit=1 but missing {missing}"
                failures.append(f"{label}: {why}")
                print(f"  FAIL {label}: {why}")
                print("\n".join(line for line in out.splitlines()
                                if line.startswith("[") or line.startswith("findings")))
    finally:
        if args.keep:
            print(f"negative-control: kept {tmp}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    total = len(PAGE_CASES) + len(DATA_CASES)
    if failures:
        print(f"\nnegative-control: {len(failures)}/{total} cases did not behave:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"\nnegative-control: {total}/{total} cases produced the finding they inject")
    return 0


if __name__ == "__main__":
    sys.exit(main())
