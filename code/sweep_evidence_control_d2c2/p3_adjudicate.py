#!/usr/bin/env python3
"""p3 — IS EACH GAP REAL, OR AN ARTEFACT OF THE DETECTOR'S DEFINITION?

mg-d2c2's item 2, answered per directory and then bounded over the population.

PART A adjudicates the two directories p1 named.  The adjudication is not a word count: it
is a list of PINNED LITERALS, each one a line in a committed file of that directory that
records a falsification attempt.  Each literal is located at run time and printed with its
file and line number, so the adjudication is checkable by reading four files.  If a literal
has moved, this file REFUSES rather than reporting a stale verdict — the adjudication is
allowed to rot, and is required to say so when it does.

PART B bounds how much of the whole 27-name list is the same artefact, with a WIDER screen
whose limits are stated up front:

  * The screen is ITSELF a vocabulary test.  It is a wider vocabulary, not a different kind
    of instrument, and proposing it as the repair would be this ticket's own defect in a
    bigger costume.  It is here to BOUND the artefact, not to replace the probe.
  * It is deliberately conservative — bare `mutation`, bare `control`, bare `fail` are all
    excluded — so the number it returns is a LOWER BOUND on the artefacts among the 27.
  * Every directory it counts prints the exhibit line it was counted on.  A screen whose
    output is a number is a screen nobody can check.
  * It was written AFTER p2's five worlds existed, so its 5-of-5 score on them is not
    evidence about the screen.  It is stated because leaving it out would let the score be
    read as a validation it is not.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_d2c2 as L  # noqa: E402


# ---------------------------------------------------------------------- PART A exhibits
#
# (directory, [(file, pinned literal, what it shows)])
EXHIBITS = {
    "compression_novelty_623a": [
        ("a1_identities.py", "A5  CONTROL, MUST GO RED",
         "an arm declared in the module docstring as required to go red"),
        ("a1_identities.py", "scored INVERTED",
         "the scoring rule stated in source: a failure here is the control working"),
        ("a1_identities.py", "*** CONTROL DID NOT FIRE ***",
         "the branch that prints when the control FAILS to fail — the arm can go wrong"),
        ("out_a1_identities.txt", "[control: failure is the pass]",
         "the committed transcript recording three such arms actually firing"),
        ("out_a1_identities.txt", "A7 -- NAMED CONTROL on V_k",
         "a fourth arm: a named control on a family whose answer is known in advance"),
        ("out_a3_sites.txt", "POSITIVE CONTROLS:",
         "a second, independent set of positive controls, scored in a second transcript"),
    ],
    "audit_successor_consolidation_9134": [
        ("consolidate_9134.py", "Raised when the control cannot reach a verdict at all",
         "a refusal path: the control distinguishes `did not fire` from `did not run`"),
        ("out_consolidate.txt", "[N1] THE TRAP THE ORDER AVOIDS",
         "the first of four planted worlds, each mutating the store and requiring a warn"),
        ("out_consolidate.txt", "THE SURVIVING NAME IS LOAD-BEARING",
         "N3: strip the tag and the detector must go red, or its green means nothing"),
        ("out_consolidate.txt", "MY OWN CONTROL'S FAILURE MODE, REPRODUCED ON PURPOSE",
         "ARM D: the control's own blindness reproduced deliberately and measured"),
        ("out_consolidate.txt", "the identical mutation that fires in N3 is",
         "the recorded outcome of ARM D — the mutation goes SILENT, as predicted"),
    ],
    # Two of the ORIGINAL 25, to test whether the baseline was ever a count of real gaps.
    "counterexample_audit_a7b4": [
        ("selfcheck.py", "these pass.  Run:",
         "a file literally named for a self-check — missed because the probe's regex "
         "spells it `selftest|self_test` and this is `selfcheck`, one character out"),
    ],
    "sibling_sweep_7085": [
        ("out_r1_sweep_FIRSTRUN_2FAIL.txt", "ANTI-VACUITY",
         "a whole section requiring the broken arms to be broken for the right reason"),
        ("out_r1_sweep_FIRSTRUN_2FAIL.txt", "and it ACTUALLY FAILED at least once",
         "a recorded firing — missed because RED_TOKENS wants `FAILED TO`, not `FAILED`"),
    ],
}

BASELINE_25_SAMPLE = ("counterexample_audit_a7b4", "sibling_sweep_7085")


# ---------------------------------------------------------------------- PART B screen
#
# Each marker asserts an INVERTED EXPECTATION or records a DEMONSTRATED FIRING.  Bare
# `control`, bare `mutation`, bare `fail` are deliberately absent: they are the words that
# appear in prose about controls, and counting them would reproduce the defect being
# measured.  This list is printed in the output so it can be argued with.
SCREEN_MARKERS = [
    r"MUST FAIL", r"MUST GO RED", r"must go red", r"must fail",
    r"\[MUST\b", r"failure is the pass", r"scored INVERTED",
    r"must be nonzero", r"must NOT fire", r"must fire",
    r"planted", r"known[- ]bad", r"ACTUALLY FAILED", r"ANTI-VACUITY",
    r"REPRODUCED", r"self[- ]?check", r"negative control", r"mutation arm",
    r"mutated", r"wrong[- ]way", r"demonstrated to fail", r"expected to fail",
]
SCREEN = re.compile("|".join(SCREEN_MARKERS))


def screen_dir(path):
    """Return (fired, exhibit) where exhibit is (relfile, lineno, line) or None."""
    for f in L.SWEEP.files(path, (".py", ".sh", ".txt", ".md")):
        for i, ln in enumerate(L.read(f).split("\n"), 1):
            m = SCREEN.search(ln)
            if m:
                return True, (os.path.relpath(f, L.ROOT), i, ln.strip()[:96])
    return False, None


def adjudicate(name):
    """Print the full adjudication of one directory.  Returns (verdict, ok)."""
    path = os.path.join(L.CODE, name)
    bare, why = L.probe(path)
    print("-" * 92)
    print(f"  code/{name}")
    print("-" * 92)
    print(f"    the sweep's §3 probe says : {'BARE' if bare else 'HAS EVIDENCE'}")
    print(f"      sources it looked at    : {', '.join(why['sources'])}")
    print(f"      filename probe matched  : {why['filename_probe_hits'] or '(nothing — no '
          f'filename contains negative/selftest/self_test/positive/control/falsif)'}")
    print(f"      token probe matched     : {why['token_probe_hits'] or '(nothing — no '
          f'transcript contains HOLE/CAUGHT/MISMATCH/REFUTED/FAILED TO/SETUP FAILED/'
          f'NEGATIVE CONTROL)'}")
    print()
    print("    WHAT THE DIRECTORY ACTUALLY SHIPS, located at run time:")
    missing = []
    for fname, literal, meaning in EXHIBITS[name]:
        hit = L.find_literal(os.path.join(path, fname), literal)
        if hit is None:
            missing.append((fname, literal))
            print(f"      !! code/{name}/{fname}: `{literal}` NOT FOUND")
            continue
        lineno, line = hit
        print(f"      code/{name}/{fname}:{lineno}")
        print(f"          {line[:88]}")
        print(f"          -> {meaning}")
    print()
    if missing:
        print(f"    REFUSED — {len(missing)} pinned exhibit(s) have moved.  This "
              f"adjudication is stale and must be redone, not repaired by loosening "
              f"the pins.")
        return "REFUSED", False
    verdict = "DETECTOR ARTEFACT" if bare else "PROBE ALREADY CREDITS IT"
    n = len(EXHIBITS[name])
    print(f"    VERDICT: {verdict} — the directory ships {n} committed "
          f"exhibit{'' if n == 1 else 's'} of a")
    print(f"    falsification attempt and the probe scored it "
          f"{'BARE' if bare else 'as having evidence'}.")
    return verdict, True


def main():
    print("=" * 92)
    print("mg-d2c2 §3 — REAL GAP, OR DETECTOR ARTEFACT?")
    print("=" * 92)
    print()

    ok = True

    print("PART A1 — THE TWO DIRECTORIES ADDED TODAY, ADJUDICATED")
    print()
    verdicts = {}
    for name in sorted(L.TICKET_EXPECTS):
        v, good = adjudicate(name)
        verdicts[name] = v
        ok = ok and good
        print()

    print("=" * 92)
    print("PART A2 — WAS THE BASELINE 25 EVER A COUNT OF REAL GAPS?")
    print("=" * 92)
    print("  If the answer is no, then today's 25 -> 27 is not two new hygiene gaps against")
    print("  a clean baseline; it is two more misreadings on top of an unknown number of")
    print("  them.  Two of the ORIGINAL 25 are adjudicated by the same method.")
    print()
    for name in BASELINE_25_SAMPLE:
        v, good = adjudicate(name)
        verdicts[name] = v
        ok = ok and good
        print()

    # ---------------------------------------------------------------- PART B
    print("=" * 92)
    print("PART B — HOW MUCH OF THE 27 IS THE SAME ARTEFACT?  A LOWER BOUND.")
    print("=" * 92)
    print()
    print("  The screen below is a WIDER VOCABULARY TEST and is not proposed as the repair.")
    print("  It excludes bare `control`, bare `mutation`, bare `fail` — the words that occur")
    print("  in prose ABOUT controls — so it under-counts on purpose.  Markers:")
    for i in range(0, len(SCREEN_MARKERS), 4):
        print("      " + "  ".join(m.ljust(22) for m in SCREEN_MARKERS[i:i + 4]))
    print()

    print("  THE SCREEN'S OWN TWO-SIDED CHECK — it must answer both ways or it is not a")
    print("  screen.  DISCLOSED: these five worlds are p2's, and this screen was written")
    print("  after they existed, so 5 of 5 is a floor and NOT a validation.")
    import p2_two_sided_control as P2  # noqa: E402
    import shutil
    import tempfile
    sandbox = tempfile.mkdtemp(prefix="d2c2-screen-")
    screen_right = 0
    try:
        for title, _why, correct_bare, files in P2.WORLDS:
            wpath = P2.build(os.path.join(sandbox, title.split()[0]), files)
            fired, _ex = screen_dir(wpath)
            right = (not fired) == correct_bare
            screen_right += right
            print(f"    [{'PASS' if right else 'FAIL'}]  {title.split()[0]}: correct="
                  f"{'BARE' if correct_bare else 'EVIDENCE'}, screen says "
                  f"{'EVIDENCE' if fired else 'BARE'}")
            shutil.rmtree(os.path.dirname(wpath))
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)
    print(f"    screen: {screen_right} of {len(P2.WORLDS)}   "
          f"(a4_sweep's §3 probe, same worlds: 2 of {len(P2.WORLDS)})")
    print()
    print("    D1 — THE SCREEN'S OWN FALSE POSITIVE, KEPT.  It scores W4 wrong, and W4 is")
    print("    the world whose README says a control is ABSENT: `Wiring up a negative")
    print("    control is left for a successor ticket.`  The marker `negative control`")
    print("    matches the sentence that denies one exists.  This is the SAME defect the")
    print("    whole file is about, committed by the instrument written to measure it, and")
    print("    it is left in rather than tuned out: deleting the marker would make the")
    print("    screen score 5 of 5 and would delete the demonstration that a wider")
    print("    vocabulary is still a vocabulary.  It also means Part B's `EVIDENCE` column")
    print("    is itself a candidate list — which is why every row prints its exhibit.")
    if screen_right < 2:
        print("    The screen does not answer both ways on worlds with known answers.")
        print("    Its population figures below are not usable.")
        ok = False
    print()

    live = L.run_sweep_live()
    bare_now, population, _ = L.parse_bare_list(live, "live run")
    print(f"  THE {len(bare_now)} NAMES THE SWEEP CALLS BARE, SCREENED "
          f"(population {population}):")
    print()
    fired_names, quiet_names = [], []
    for name in bare_now:
        fired, ex = screen_dir(os.path.join(L.CODE, name))
        if fired:
            fired_names.append(name)
            print(f"    [EVIDENCE]  {name}")
            print(f"                {ex[0]}:{ex[1]}")
            print(f"                {ex[2]}")
        else:
            quiet_names.append(name)
    print()
    print(f"  THE SWEEP CALLS BARE AND THE SCREEN DOES NOT: {len(quiet_names)}")
    for name in quiet_names:
        print(f"    [quiet]     {name}")
    print()

    print("-" * 92)
    print("  READING THESE TWO NUMBERS HONESTLY")
    print("-" * 92)
    print(f"    the sweep's field, live, this tree     : {len(bare_now)} of {population}")
    print(f"    of those, carrying an inverted arm     : {len(fired_names)}  "
          f"(each with an exhibit line above)")
    print(f"    remaining, on this wider reading       : {len(quiet_names)} of {population}")
    print()
    print("    The third number is a CANDIDATE count in mg-9876's own sense and is a LOWER")
    print("    BOUND on the real gaps — the screen under-counts by construction, and a")
    print("    directory it leaves quiet may still ship evidence it has no words for.  What")
    print("    it is NOT is 27: the field cannot be read as a count of directories that")
    print("    ship code nothing has ever tried to break.")
    print()

    print("=" * 92)
    if not ok:
        print("P3 ADJUDICATION — REFUSED: an exhibit moved or the screen did not answer "
              "both ways.  No count above may be cited.")
        print("=" * 92)
        return 2
    artefacts = sum(1 for v in verdicts.values() if v == "DETECTOR ARTEFACT")
    print(f"P3 ADJUDICATION — {artefacts} of {len(verdicts)} adjudicated directories are "
          f"DETECTOR ARTEFACTS, including both added today; the field reads "
          f"{len(bare_now)} of {population} and bounds at {len(quiet_names)}.")
    print("=" * 92)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except L.Refused as exc:
        print()
        print("=" * 92)
        print(f"P3 ADJUDICATION — REFUSED: {exc}")
        print("=" * 92)
        sys.exit(2)
