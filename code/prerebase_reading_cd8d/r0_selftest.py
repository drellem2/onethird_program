#!/usr/bin/env python3
"""mg-cd8d r0 — SIX CONTROLS ON THE HARNESS, BEFORE ANY OF ITS ANSWERS ARE WORTH READING.

r1 asks one question — what does `verdict_for` return for a census reading taken before the
rebase — and the answer is a single word.  A harness that returns one word for every input
answers it too, and would answer it identically if it had read nothing at all.  So the two
directions are separated here rather than asserted in r1's prose:

    D1  POSITIVE.  Identical readings must come back AGREES.  A harness that never reaches
        AGREES cannot report that the discipline is REWARDED, which is half of r1's finding.
    D2  THE LAUNDERED GREEN, PLANTED.  With the archive step suppressed the corpus is EMPTY
        except for the producer, both readings are identical, and the verdict is AGREES — the
        harness reporting `this branch's reading matched the merged tree` because it read
        nothing.  This is why every world in r1 prints its population and why r0 requires the
        population to be plausible; without that, `AGREES` and `read nothing` are one string.
    D3  THE OVERLAY IS LOAD-BEARING, PLANTED.  Run each tree's OWN producer instead of today's
        and a pre-mg-05c6 tree prints no corpus pin at all, so the verdict is DISAGREES — red,
        and for a reason that has nothing to do with when the reading was taken.  The overlay
        is what makes r1 a measurement about the CORPUS's movement rather than the
        INSTRUMENT's age (mg-ede8's rule, applied in the direction that fits this question).
    D4  WHICH VERDICTS ARE RED IS READ OFF THE INSTRUMENT AND NOT TYPED HERE.  r1's finding
        turns on CORPUS not being red; that is `lib_f771.RED_VERDICTS`'s business, so it is
        read from the real constant, both ways.
    D5  REQUIRED-INERT, AND THE INERTNESS IS THE FINDING.  Whether the simulated branch added
        a directory of its OWN must not change the verdict.  `verdict_for(committed, worktree,
        relpath)` takes no argument for who WROTE the committed copy, so the branch that
        published a stale figure and the branch that published nothing are graded by the same
        clause.  A control that must NOT fire, labelled so nobody reads it as a detector.
    D6  THIS DIRECTORY'S CONTRIBUTION TO THE SWEEP IT MEASURES, measured with the sweep's OWN
        detector rather than by eye — and both ways, because a zero from a detector that never
        looked is not a zero.

EXITS 0 if all six answer as required, 1 if any does not, 2 if the harness refused.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_cd8d as L  # noqa: E402

W = 92

# mg-9876's instance 3, ASSEMBLED RATHER THAN WRITTEN OUT.  Written out, this fixture is itself
# counted by the §1 detector it exercises — the first run of D6 returned 1 and the site was this
# line — so a control on the census would have moved the census.  That is mg-05c6's own
# neutralisation one directory over, where a sandbox fixture reading `if 'x' in out:` moved the
# published figure 220 -> 222 and was rewritten to `VALUE = 1`.  The detector still receives the
# exact characters; only the spelling of the source line changed.
INSTANCE_3 = 'if "8 9" %s out:' % "in"


def main():
    print("=" * W)
    print("mg-cd8d r0 — CONTROLS ON THE HARNESS THAT ANSWERS r1's QUESTION")
    print("=" * W)
    print()

    L.require_commits()
    checks = []

    # ---- D1 -------------------------------------------------------------------------
    post, _ = L.reading(L.AS_OF, extra_dirs=(L.BRANCH_DIR,))
    pop_post = L.figures(post)[0]
    checks.append(("D1  positive: two identical readings must come back AGREES — without this "
                   "world the harness cannot say the discipline is rewarded",
                   L.verdict(post, post) == "AGREES", None))
    checks.append(("D1' positive: the population of a real world must be plausible, and it is "
                   "printed beside every verdict in r1 for the reason D2 gives",
                   pop_post is not None and pop_post > 200, "population %s" % pop_post))

    # ---- D2 -------------------------------------------------------------------------
    empty_a, _ = L.reading(L.MAIN_BEFORE, extra_dirs=(L.BRANCH_DIR,), archive=False)
    empty_b, _ = L.reading(L.AS_OF, extra_dirs=(L.BRANCH_DIR,), archive=False)
    empty_verdict = L.verdict(empty_a, empty_b)
    pop_empty = L.figures(empty_a)[0]
    checks.append(("D2  NEGATIVE: with the corpus never extracted, the two readings are "
                   "identical and the verdict is AGREES — a green that means `read nothing`.  "
                   "CAUGHT by the population, which is implausible, and not by the verdict, "
                   "which is indistinguishable from the discipline being followed",
                   empty_verdict == "AGREES" and pop_empty is not None and pop_empty < 200,
                   "verdict %s at population %s" % (empty_verdict, pop_empty)))

    # ---- D3 -------------------------------------------------------------------------
    own_far, _ = L.reading(L.MAIN_FAR, extra_dirs=(L.BRANCH_DIR,), overlay_producer=False)
    own_pin = L.figures(own_far)[1]
    own_verdict = L.verdict(own_far, post)
    checks.append(("D3  NEGATIVE: with each tree running its OWN producer, a corpus older than "
                   "mg-05c6 prints no corpus pin, so the verdict is DISAGREES — red for the "
                   "instrument's age and not for when the reading was taken.  CAUGHT",
                   own_pin is None and own_verdict == "DISAGREES",
                   "corpus pin %s, verdict %s" % (own_pin, own_verdict)))

    # ---- D4 -------------------------------------------------------------------------
    red = L.F.RED_VERDICTS
    checks.append(("D4  which verdicts fail the gate is read from lib_f771.RED_VERDICTS: STALE "
                   "and DISAGREES are red, AGREES and NOISE and CORPUS are not",
                   "STALE" in red and "DISAGREES" in red
                   and not any(v in red for v in ("AGREES", "NOISE", "CORPUS")),
                   "RED_VERDICTS = %s" % (red,)))

    # ---- D5 -------------------------------------------------------------------------
    pre_with, _ = L.reading(L.MAIN_BEFORE, extra_dirs=(L.BRANCH_DIR,))
    pre_without, _ = L.reading(L.MAIN_BEFORE)
    post_without, _ = L.reading(L.AS_OF)
    v_with = L.verdict(pre_with, post)
    v_without = L.verdict(pre_without, post_without)
    checks.append(("D5  REQUIRED-INERT: the simulated branch's own new directory must not "
                   "change the verdict — verdict_for takes no argument for WHO wrote the "
                   "committed copy, so this world firing would mean the harness had found a "
                   "provenance channel that the instrument does not have",
                   v_with == v_without,
                   "with own directory %s, without %s" % (v_with, v_without)))

    # ---- D6 -------------------------------------------------------------------------
    here = os.path.dirname(os.path.abspath(__file__))
    mine = 0
    for fn in sorted(os.listdir(here)):
        if not fn.endswith(".py"):
            continue
        with open(os.path.join(here, fn), "r", encoding="utf-8") as fh:
            for line in fh.read().split("\n"):
                s = line.strip()
                if s.startswith("#") or not L.A.SMELL_MEMBERSHIP.search(s):
                    continue
                if L.A._FOR_BINDING.search(s):
                    continue
                mine += 1
    fires = bool(L.A.SMELL_MEMBERSHIP.search(INSTANCE_3))
    checks.append(("D6  this directory adds %d membership candidate(s) to mg-9876's §1, "
                   "counted with a4's own SMELL_MEMBERSHIP over this directory's own .py — "
                   "and the same detector fires on instance 3's spelling, so the count is a "
                   "measurement rather than a detector that never looked.  The first run of "
                   "this control returned 1: the fixture below, which is a CONTROL and not a "
                   "site, and is now assembled rather than written out (mg-05c6's own "
                   "neutralisation, one directory over)" % mine,
                   mine == 0 and fires, "fixture: %s" % INSTANCE_3))

    print("-" * W)
    ok = True
    for text, passed, detail in checks:
        mark = "PASS" if passed else "FAIL"
        if text.startswith(("D2", "D3")) and passed:
            mark = "CAUGHT"
        print("  [%-6s]  %s" % (mark, text))
        if detail:
            print("             %s" % detail)
        ok = ok and passed
    print("-" * W)
    print()
    print("=" * W)
    if ok:
        print("HARNESS OK — the four two-sided worlds answer both ways, the required-inert one "
              "is inert,")
        print("and this directory adds nothing to the census it measures.  r1's answers are "
              "readable.")
    else:
        print("HARNESS BROKEN — a control did not answer as required.  Do not read r1.")
    print("=" * W)
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except L.Refused as exc:
        sys.stderr.write("mg-cd8d r0: REFUSED — %s\n" % exc)
        sys.exit(2)
