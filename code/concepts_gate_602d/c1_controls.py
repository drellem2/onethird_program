#!/usr/bin/env python3
"""mg-602d — CAN THE GATE FIRE?  Planted worlds, in both directions.

A gate that has never gone red is indistinguishable from a gate that cannot.  So this arm writes
corrupted copies of `docs/CONCEPTS.md` beside the real one (see `run_against` for why *beside* and
not below), runs `c0` against each, and checks that the verdict is the one the corruption deserves.
The real file is never written to, and the two planted files are removed in a `finally`.

SIX MUST-FIRE worlds, one per rule c0 claims to enforce, plus the anchor world which must REFUSE
rather than pass -- a reworded heading has to be loud, and 'could not tell' must never map onto
'nothing wrong'.

AND ONE WRONG-DIRECTION WORLD, which MUST STAY GREEN and is the point of including it: a row whose
pointer is swapped for a DIFFERENT, WELL-FORMED item id sails through.  c0 checks that a pointer is
THERE, not that it is RIGHT, and this world is the measurement of that limit rather than a sentence
about it.  A reader who takes c0's green as 'the citations were checked' is reading this world's
result backwards.

EXITS 0 if every world lands where it should, 1 if any does not, 2 if the harness could not run.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import c0_concept_discipline as c0  # noqa: E402

REAL_CONCEPTS = c0.CONCEPTS
REAL_STATE = c0.STATE


def run_against(concepts_text, state_text, paths):
    """Run c0 against a planted pair of files; return its exit code, output suppressed.

    THE PLANTED DOCUMENT MUST SIT IN docs/ ITSELF, not in a subdirectory of it.  c0 resolves
    relative links against the document's OWN directory, so a copy one level deeper makes every
    honest link (`FACTS.md`, `../STATE.md`) dead and every world comes back red for a reason
    that has nothing to do with what it plants.  That is exactly how this harness first ran:
    both the positive control and the wrong-direction world went red, and the two worlds whose
    job is to prove the gate is not simply always-red are the two it broke.  Kept as a comment
    rather than quietly fixed, because a harness that can only produce reds is the failure this
    arm exists to rule out, and it produced one on its first execution.
    """
    cpath, spath = paths
    with open(cpath, "w", encoding="utf-8") as fh:
        fh.write(concepts_text)
    with open(spath, "w", encoding="utf-8") as fh:
        fh.write(state_text)
    c0.CONCEPTS, c0.STATE = cpath, spath
    devnull = open(os.devnull, "w")
    stdout = sys.stdout
    try:
        sys.stdout = devnull
        return c0.main()
    finally:
        sys.stdout = stdout
        devnull.close()
        c0.CONCEPTS, c0.STATE = REAL_CONCEPTS, REAL_STATE


def strip_last_pointer(text):
    """Blank the pointer cell of the last row of the killed-intuitions table."""
    lines = text.splitlines()
    body_start = next(i for i, ln in enumerate(lines)
                      if ln.startswith("## ") and "Intuitions that have been killed" in ln)
    for i in range(len(lines) - 1, body_start, -1):
        ln = lines[i].strip()
        if ln.startswith("|") and ln.endswith("|") and ln.count("|") == 4:
            cells = [c.strip() for c in ln[1:-1].split("|")]
            if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                lines[i] = "| %s | %s |  |" % (cells[0], cells[1])
                return "\n".join(lines) + "\n"
    raise RuntimeError("no killed-intuitions row found to corrupt")


def unmark_a_belief(text):
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("- **BELIEF"):
            lines[i] = ln.replace("**BELIEF — ", "**", 1)
            return "\n".join(lines) + "\n"
    raise RuntimeError("no BELIEF item found to corrupt")


def swap_a_pointer(text):
    """Replace one real item id with a different, well-formed one.  Still a pointer."""
    return text.replace("`mg-8d66`", "`mg-0000`", 1)


def main():
    concepts = open(REAL_CONCEPTS, encoding="utf-8").read()
    state = open(REAL_STATE, encoding="utf-8").read()

    filler = ("\n\nPADDING. " * 400)

    worlds = [
        ("REAL FILE (positive control)", concepts, state, 0,
         "the document as it stands must be green, or every red below means nothing"),
        ("pointer cell blanked in S5", strip_last_pointer(concepts), state, 1,
         "a killed intuition with no artifact behind it"),
        ("BELIEF marker removed in S6", unmark_a_belief(concepts), state, 1,
         "an unearned claim reading exactly like an earned one"),
        ("word ceiling blown", concepts + filler, state, 1,
         "silent growth into a second STATE.md"),
        ("dead relative link", concepts + "\n\nSee [x](NoSuchFile-602d.md).\n", state, 1,
         "a pointer that points nowhere on disk"),
        ("STATE.md pointer removed", concepts,
         state.replace("docs/CONCEPTS.md", "docs/nothing-here.md"), 1,
         "a document nobody can reach from the canonical file"),
        ("S6 heading reworded", concepts.replace("## 6. What we believe and cannot prove",
                                                 "## 6. Open questions"), state, 2,
         "an anchor that no longer matches MUST refuse, never pass"),
        ("pointer swapped for a WRONG one", swap_a_pointer(concepts), state, 0,
         "WRONG-DIRECTION: c0 checks presence, not correctness -- green here is the LIMIT"),
    ]

    print("=" * 88)
    print("mg-602d  can the concepts gate fire?  planted worlds, both directions")
    print("=" * 88)
    print()

    docs = os.path.dirname(REAL_CONCEPTS)
    paths = (os.path.join(docs, ".plant-602d-concepts.md"),
             os.path.join(docs, ".plant-602d-state.md"))
    bad = 0
    try:
        for name, ctext, stext, want, why in worlds:
            got = run_against(ctext, stext, paths)
            ok = got == want
            bad += 0 if ok else 1
            print("  [%s] %-34s want exit %d, got %d" % ("ok " if ok else "BAD", name, want, got))
            print("        %s" % why)
    finally:
        for p in paths:
            if os.path.exists(p):
                os.remove(p)

    print()
    print("-" * 88)
    if bad:
        print("VERDICT: %d world(s) landed in the wrong place.  The gate does not do what its"
              % bad)
        print("         docstring says, and its green on the real file cannot be trusted.")
        return 1
    print("VERDICT: green.  Every must-fire world fires, the anchor world REFUSES rather than")
    print("         passing, and the wrong-pointer world stays green -- which is c0's stated")
    print("         limit measured rather than asserted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
