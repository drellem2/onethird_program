#!/usr/bin/env python3
"""z0 -- THE CONTROLS.  Run FIRST, and for a reason.

z1's central figures are a 0 (`this directory collapses nothing`), a 61 and a
24.  A BROKEN WALK, AN UNRESOLVABLE PIN OR A NARROWED CLASS RETURNS A SMALL
NUMBER FOR FREE, and every one of those returns a page that looks exactly like
a healthy one.  So D0 establishes that the instrument can see the corpus at
all, before any arm prints a count over it.

THE TWO DIRECTIONS ARE BOTH HERE AND NEITHER IS OPTIONAL.

  MUST FIRE   -- the collapsing spelling of mg-9b6b's own `G`, reconstructed
                 from its library.  A detector that cannot flag the one
                 demonstrated instance in this estate is measuring something
                 else, whatever else it flags.
  MUST NOT    -- the spelling that SHIPPED, READ OUT OF THE TREE AT THE PIN
                 rather than re-typed (mg-d2c2: a re-statement drifts, and the
                 subject here IS the spelling).  A detector that also flags the
                 repair condemns the fix and makes the rule unfollowable.

PLANTS.  Five defects, each broken ONE function at a time, with the CLEAN
library asserted green BEFORE AND AFTER every plant and re-measured rather
than assumed.  Two worlds are REQUIRED-INERT: a plant that changes nothing is
a claim until it is run.

The plants are monkeypatches rather than sandbox copies, and that is a
deliberate exception to this estate's usual `run the real thing in a sandbox`
rule.  `lib3c92.classify` is a PURE FUNCTION OF SOURCE TEXT -- it touches no
path, no revision and no worktree -- so a patched module and a patched copy
answer identically, and a copy would only add a second place for the spelling
to drift.  The corpus-reading half (`census`, `tracked_py`, `source_at`) is
NOT patched anywhere here.

EXIT 0 GREEN, 1 A CONTROL FAILED, 2 REFUSED.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib3c92 as L  # noqa: E402

BAD = 0


def arm(name, ok, detail=""):
    global BAD
    if not ok:
        BAD += 1
    print("    [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                             ("   %s" % detail) if detail else ""))
    return ok


def kinds_in(src, strict=True):
    got, err = L.classify("<fixture>", src, strict=strict)
    if err:
        return None, err
    return got, None


# --------------------------------------------------------------------------
# fixtures.  Each is the smallest source that exhibits ONE shape.
# --------------------------------------------------------------------------

# mg-9b6b's `G(s) = max{d : delta <= s}` is EMPTY below 1/3.  This is what the
# collapsing version of that computation looks like -- the shape its README
# says would have made the route read as open.  It is a RECONSTRUCTION and is
# labelled one: mg-9b6b never shipped it, which is the whole point of D2.
F_COLLAPSE = "g = max(ds) if ds else 0\n"

F_INDICATOR = "M = [[(deg[i] if i == j else 0) for j in R] for i in R]\n"
F_EXITCODE = "sys.exit(1 if bad else 0)\n"
F_FRACTION = "lam2 = max(cands) if cands else Fraction(0)\n"
F_RATE = "pct = 100.0 * hits / total if total else 0.0\n"
F_PRESERVE = "g = max(ds) if ds else None\n"
F_COMMENTED = "# a reworded comment, and a renamed local\ng2 = max(ds) if ds else 0\n"


def main():
    L.head("z0 -- EMPTY IS NOT ZERO: the controls",
           "mg-3c92, run before any arm prints a count")

    # ---------------------------------------------------------------- D0
    L.rule("D0.  THE INSTRUMENT CAN SEE THE CORPUS  (before any zero is "
           "printed)")
    full, reachable = L.check_pin()
    arm("the pin resolves", bool(full), full[:12])
    if not arm("the pin is an ancestor of origin/main", reachable):
        print()
        print("*** REFUSED: every figure in this directory is about a tree no")
        print("    other reader can reach.  Nothing below is worth running.")
        return 2
    sites, broken, paths = L.census()
    arm("the corpus is large enough to be the corpus", len(paths) > 1000,
        "%d tracked .py under code/" % len(paths))
    arm("every file parsed", not broken,
        L.count_or_empty(len(broken), paths) + " unparseable")
    guarded = [s for s in sites if s.kind == L.GUARDED]
    arm("the class this directory is about is NOT empty", bool(guarded),
        "%d guarded site(s)" % len(guarded))
    print()
    print("    A zero is what a broken walk returns for free, so the walk is")
    print("    asserted non-trivial before z1 prints a zero over it.")

    # ---------------------------------------------------------------- D1
    L.rule("D1.  MUST FIRE -- mg-9b6b's OWN COLLAPSE, RECONSTRUCTED  (P4)")
    got, err = kinds_in(F_COLLAPSE)
    hit = [s for s in got if s.kind == L.GUARDED]
    arm("the reconstructed spelling is flagged", len(hit) == 1)
    if hit:
        arm("its operation is MAXMIN", hit[0].op == L.MAXMIN, hit[0].op)
        arm("its computed verdict is COLLAPSE", hit[0].verdict == L.COLLAPSE,
            hit[0].verdict)
    print()
    print("    `max(∅)` has no value.  Whatever is printed for it is a choice,")
    print("    and 0 is the choice that cannot be told from an answer.")

    # ---------------------------------------------------------------- D2
    L.rule("D2.  MUST NOT FIRE -- THE SPELLING THAT SHIPPED  (P4)")
    src = L.source_at(L.AS_OF, L.WITNESS_PATH)
    lineno = None
    for i, line in enumerate(src.splitlines(), 1):
        if L.WITNESS_MARK in line:
            lineno = i
    arm("the shipped spelling is still in the tree at the pin",
        lineno is not None, "%s:%s" % (L.WITNESS_PATH, lineno))
    if lineno is None:
        print()
        print("    Read out of the tree and NOT re-typed (mg-d2c2).  If this")
        print("    ever fails, the witness moved and this control is now")
        print("    asking about a line nobody wrote -- which is worse than")
        print("    failing, so it fails loudly rather than passing quietly.")
        return 1
    got, err = kinds_in(src)
    at = [s for s in got if s.line == lineno]
    arm("it is NOT in the collapsing class",
        not any(s.kind == L.GUARDED for s in at))
    arm("it is in NO class at all", not at,
        ", ".join(s.kind for s in at) or "no site")
    print()
    print("    The shipped line is")
    print("        %s" % L.WITNESS_MARK)
    print("    and it is out on TWO INDEPENDENT GROUNDS: the guard is a")
    print("    COMPARISON rather than a bare emptiness test, and the fallback")
    print("    is a STRING rather than a number.  `no class at all` is a")
    print("    weaker statement than `preserving`, and it is the true one.")
    print()
    print("    WHICH GROUND DOES THE WORK IS MEASURED RATHER THAN ASSERTED,")
    print("    and both variants below are DERIVED FROM THE SHIPPED LINE BY")
    print("    SUBSTITUTION rather than re-typed:")
    bare = L.WITNESS_MARK.replace("mx is not None", "mx")
    numeric = bare.replace('"EMPTY"', "0")
    v1, _ = kinds_in("v = " + bare + "\n")
    v2, _ = kinds_in("v = " + numeric + "\n")
    arm("    %-46s -> PRESERVING" % bare,
        any(s.kind == L.PRESERVING for s in v1),
        ", ".join(s.kind for s in v1) or "no class")
    arm("    %-46s -> COLLAPSE" % numeric,
        any(s.kind == L.GUARDED for s in v2),
        ", ".join(s.kind for s in v2) or "no class")
    print()
    print("    So the guard alone keeps it out of BOTH classes, and the")
    print("    fallback alone decides which class it would land in once the")
    print("    guard is bare.  Neither ground is doing the other's work.")

    # ---------------------------------------------------------------- D3
    L.rule("D3.  MUST NOT FIRE -- THE TWO SHAPES THAT FLOOD A `else 0` GREP")
    ind, _ = kinds_in(F_INDICATOR)
    arm("a matrix indicator is not flagged",
        not any(s.kind == L.GUARDED for s in ind))
    ext, _ = kinds_in(F_EXITCODE)
    arm("an exit-code ternary is not flagged",
        not any(s.kind == L.GUARDED for s in ext))
    ext_loose, _ = kinds_in(F_EXITCODE, strict=False)
    arm("...and it IS in the loose class, so it is the requirement that "
        "excludes it", any(s.kind == L.GUARDED for s in ext_loose))
    print()
    print("    The third row is what makes the first two mean something.  A")
    print("    shape excluded by ACCIDENT -- by a parse failure, by a typo in")
    print("    the matcher -- looks identical to one excluded on purpose.")

    # ---------------------------------------------------------------- D4
    L.rule("D4.  THE EXACT-RATIONAL FALLBACK IS RECOGNISED")
    fr, _ = kinds_in(F_FRACTION)
    arm("`Fraction(0)` counts as a numeric zero",
        any(s.kind == L.GUARDED and s.zero for s in fr))
    print()
    print("    This corpus does exact rationals on every verdict path, so the")
    print("    literal zero an author writes is very often a CALL.  A matcher")
    print("    that only knew `0` would report a smaller class for a reason")
    print("    that is about Python and not about this estate.")

    # ---------------------------------------------------------------- D5
    L.rule("D5.  PLANTED -- THE GUARD TEST IS DISABLED  (must CATCH)")
    clean, _ = kinds_in(F_INDICATOR)
    arm("clean library: the indicator is not flagged",
        not any(s.kind == L.GUARDED for s in clean))
    saved = L._bare_guard
    try:
        L._bare_guard = lambda test: True
        broke, _ = kinds_in(F_INDICATOR)
        arm("CAUGHT: with the guard test disabled it IS flagged",
            any(s.kind == L.GUARDED for s in broke))
    finally:
        L._bare_guard = saved
    again, _ = kinds_in(F_INDICATOR)
    arm("clean library restored, and re-measured rather than assumed",
        not any(s.kind == L.GUARDED for s in again))

    # ---------------------------------------------------------------- D6
    L.rule("D6.  PLANTED -- THE DIVISION SHAPE IS BLINDED  (must CATCH)")
    clean, _ = kinds_in(F_RATE)
    arm("clean library: a rate is COLLAPSE",
        any(s.verdict == L.COLLAPSE and s.op == L.DIV for s in clean))
    saved_op = L._op
    try:
        L._op = lambda node: L.OP_OTHER
        broke, _ = kinds_in(F_RATE)
        arm("CAUGHT: blinded, the same site becomes UNDECIDED",
            any(s.verdict == L.UNDECIDED for s in broke))
    finally:
        L._op = saved_op
    again, _ = kinds_in(F_RATE)
    arm("clean library restored",
        any(s.verdict == L.COLLAPSE for s in again))
    print()
    print("    An UNDECIDED site goes to z1's hand table, and a hand table")
    print("    with a site missing REFUSES.  So this plant is caught twice:")
    print("    once here, and once as a refusal in the arm that consumes it.")

    # ---------------------------------------------------------------- D7
    L.rule("D7.  PLANTED -- `None` IS TREATED AS A NUMBER  (must CATCH)")
    clean, _ = kinds_in(F_PRESERVE)
    arm("clean library: `else None` is PRESERVING",
        any(s.kind == L.PRESERVING for s in clean))
    saved_pres = L._is_preserving
    try:
        L._is_preserving = lambda node: False
        broke, _ = kinds_in(F_PRESERVE)
        arm("CAUGHT: with `None` no longer preserving, the site leaves the "
            "compliant class",
            not any(s.kind == L.PRESERVING for s in broke))
    finally:
        L._is_preserving = saved_pres
    again, _ = kinds_in(F_PRESERVE)
    arm("clean library restored",
        any(s.kind == L.PRESERVING for s in again))
    print()
    print("    z1 §3's 88.8%% and 86.3%% are the two figures this directory")
    print("    would most like to be true, so the predicate they rest on is")
    print("    the one most worth breaking on purpose.")

    # ---------------------------------------------------------------- D8
    L.rule("D8.  REQUIRED-INERT -- PROSE DOES NOT MOVE THE COUNT")
    a, _ = kinds_in(F_COLLAPSE)
    b, _ = kinds_in(F_COMMENTED)
    arm("a reworded comment and a renamed local move NOTHING",
        len([s for s in a if s.kind == L.GUARDED])
        == len([s for s in b if s.kind == L.GUARDED]))
    print()
    print("    This is the wrong direction and it MUST NOT MOVE.  A detector")
    print("    that answers differently when the prose changes is measuring")
    print("    text, and every figure in z1 would be about the writing.")

    # ---------------------------------------------------------------- D9
    L.rule("D9.  REQUIRED-INERT -- THE `%` OF A NON-STRING IS NOT A PRINT")
    mod, _ = kinds_in("r = (a % b) + (max(xs) if xs else 0)\n")
    arm("an arithmetic `%` does not make a site PRINTED",
        all(not s.printed for s in mod if s.kind == L.GUARDED))
    pr, _ = kinds_in('print("%d" % (max(xs) if xs else 0))\n')
    arm("...and a real format string does",
        any(s.printed for s in pr if s.kind == L.GUARDED))
    print()
    print("    z1 §7's headline is `24 of 61 reach a page`.  If `%` alone")
    print("    counted, that numerator would be a fact about modular")
    print("    arithmetic in a corpus that does a great deal of it.")

    # --------------------------------------------------------------- D10
    L.rule("D10. THE HAND TABLE IS COMPLETE, AND ITS REFUSAL WORKS")
    import z1_census  # noqa: E402
    undecided = {s.key for s in guarded if s.verdict == L.UNDECIDED}
    arm("every undecided site carries a hand verdict",
        not (undecided - set(z1_census.HAND)),
        "%d undecided, %d judged" % (len(undecided), len(z1_census.HAND)))
    arm("no hand verdict names a site the census did not find",
        not (set(z1_census.HAND) - {s.key for s in guarded}))
    holed = dict(z1_census.HAND)
    if undecided:
        holed.pop(sorted(undecided)[0])
    arm("CAUGHT: with one verdict removed, the completeness test fails",
        bool(undecided - set(holed)))
    print()
    print("    The refusal is checked here as well as in z1 because z1's")
    print("    refusal path is the one that never runs on a green day, and a")
    print("    refusal nobody has seen fire is a promise.")

    print()
    print("=" * 78)
    print("z0: %s   (%d control(s) failed)"
          % ("GREEN" if not BAD else "RED", BAD))
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
