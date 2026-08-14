#!/usr/bin/env python3
"""mg-372e — NEGATIVE CONTROL: prove s2's detector can FAIL.

s2 passes.  A check that has never failed is indistinguishable from a check that
cannot fail, so this mutates the repaired documents IN MEMORY and asserts the
detector fires.  Nothing on disk is touched.

Four mutations.  M0 is EXPECTED NOT TO FIRE and is kept for what it shows:

  M0  strip every `~~` from mg-6bc2 -- the strike GLYPHS vanish, the prose stays.
      This does NOT fire, and that is correct rather than a miss: the detector is
      keyed on the REFUTATION TRAVELLING WITH THE SITE, not on the glyph, and the
      words "REFUTED"/"mg-131e" survive the mutation in the same block, so a
      reader still learns the formula is false.  Reported, not tuned away.
  M1  undo the repair in mg-6bc2 -- strip the glyphs AND every marker word
  M2  the same for mg-200d
  M3  plant a fresh LIVE site in mg-6bc2, spelled the way the ticket did NOT
      name it (`2/(n + 1)`, spaced) -- the failure mode a sibling sweep hit
      tonight, where the live site was written in a spelling the ticket missed

PINNED AT ONE COMMIT SINCE mg-528e, AND IT NO LONGER CARRIES ITS OWN COPY OF THE
DETECTOR.  The documents it mutates are read at `lib372e.AS_OF`, so the four
pre-declared outcomes on stdout are a function of one commit.  `check()` below
used to be a RE-STATEMENT of s2's loop, so the control proving the detector can
fire was proving it about a second spelling of the detector; it calls
`s2_classify.unmarked` now (mg-1344's P5).  The live half -- the same four
mutations against the WORKING TREE -- is on stderr and in the exit code, so the
manual re-run the README used to instruct a reader to do by hand happens on every
invocation.
"""
import re
import sys

import lib372e
import s2_classify as S


def check(rel, lines):
    """s2's marked-or-allowlisted check, run against supplied lines.

    ONE spelling, imported.  See s2_classify.unmarked's docstring for why, and
    P57 for the control that the extraction moved no outcome.
    """
    return [(ln, line.strip()[:80]) for ln, line in S.unmarked(rel, lines)]


def load(rel):
    return lib372e.read_lines(rel)


BC = "docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md"
PS = "docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md"

MARKERS = re.compile(r"~~|REFUTED|STRUCK|VOID|mg-131e|mg-372e|mg-00a1|⛔")


def undo(ls):
    """Undo the repair: remove the strike glyphs AND every marker word."""
    return [MARKERS.sub("", l) for l in ls]


# THE FOUR PRE-DECLARED WORLDS, IN ONE PLACE SO BOTH HALVES RUN THE SAME ONES.
# The pinned half scores them at AS_OF and prints to stdout; the live half scores
# THE SAME FOUR against the working tree and prints to stderr.  Two lists would
# be two controls, and only one of them would be the one the README names.
MUTATIONS = [
    ("M0  strip only the `~~` glyphs from mg-6bc2 (PRE-DECLARED: NO FIRE)", BC,
     lambda ls: [l.replace("~~", "") for l in ls], False),
    ("M1  undo the repair in mg-6bc2 (glyphs AND marker words)", BC, undo, True),
    ("M2  undo the repair in mg-200d (glyphs AND marker words)", PS, undo, True),
    ("M3  plant a LIVE site in an UNNAMED spelling", BC,
     lambda ls: ls + ["", "The per-slot form buys `eps_spec = 2/(n + 1)` today.", ""], True),
]


def score(loader, emit, examples=2, prefix=""):
    """Run all four worlds through `loader`, report with `emit`, return failures."""
    bad = 0
    for name, rel, mutate, expect in MUTATIONS:
        base = loader(rel)
        clean = check(rel, base)
        dirty = check(rel, mutate(base))
        fired = len(dirty) > len(clean)
        ok = (fired == expect)
        emit(f"{prefix}{name}")
        emit(f"{prefix}    unmutated: {len(clean)}   mutated: {len(dirty)}   "
             f"-> {'FIRED' if fired else 'DID NOT FIRE'}   "
             f"(pre-declared {'FIRE' if expect else 'NO FIRE'}: {'ok' if ok else 'MISMATCH'})")
        for ln, txt in dirty[:examples]:
            emit(f"{prefix}      e.g. {rel}:{ln}  {txt}")
        if not ok:
            bad += 1
        emit(prefix.rstrip())
    return bad


def main():
    print("mg-372e NEGATIVE CONTROL — does the s2 detector fire when the repair is undone?")
    print("=" * 78)
    print()
    lib372e.banner()
    rc = 1 if score(load, print) else 0

    # M3 deserves its own note: it is the ticket's named hazard, and it is the
    # reason the sweep patterns tolerate whitespace rather than one literal.
    print("M3 is the hazard the ticket names: a live site written `2/(n + 1)` with spaces.")
    print("The EPS pattern is whitespace-tolerant, so the plant is caught.  A sweep that")
    print("grepped the literal string `2/(n+1)` would have returned a clean zero.")
    print()
    print("CONTROL PASSED — every mutation behaved as pre-declared" if rc == 0
          else "CONTROL FAILED — a mutation did not behave as pre-declared")

    # THE LIVE HALF (mg-528e).  The README used to tell a reader to run this by
    # hand, and warned that the one command they would reach for destroys the
    # transcripts.  It runs on every invocation now, on stderr, and its verdict
    # is in the exit code.
    say = lambda s: print(s, file=sys.stderr)
    say("[live] s3 re-scored against the WORKING TREE (not part of the transcript)")
    try:
        live_bad = score(lib372e.read_worktree, say, examples=1, prefix="[live]   ")
    except OSError as exc:
        say("[live]   COULD NOT READ THE WORKING TREE: %s" % exc)
        live_bad = 1
    say("[live]   -> %d of %d world(s) disagree with their pre-declaration"
        % (live_bad, len(MUTATIONS)))
    return 1 if live_bad else rc


# IMPORTABLE WITHOUT RUNNING, SINCE mg-528e.  Everything above is definitions, so
# `asof_census_20ee`'s P57 can score the four worlds through THIS table rather
# than through a fourth spelling of it -- a control that re-typed the mutations
# would be checking that two hand-written lists agree.  It used to run at import,
# print a page and call sys.exit, so it could not be imported at all.
if __name__ == "__main__":
    sys.exit(main())
