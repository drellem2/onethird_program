"""mg-79ba A2 -- MY TICKET'S LITERAL QUESTION: DOES AN ADDED ROW GO RED WHEN
THE BLINDNESS IS FIXED?

THE BLINDNESS.  NEGATIVE CONTROL 4's row I4 corrupts `le_to_facet` by one.  On
25 of the 86 posets the corruption APPLIES -- a different facet enumeration is
built, and on 24 of those a genuinely different facet SET -- and claim (1)
still holds, so L^rel is unchanged and the pipeline never sees it.  mg-e35b
declined to score that split and gave the reason my ticket quotes: a row
scoring "the split separates" would go RED the day somebody FIXED the
blindness.

WHAT "FIXED" MEANS HERE, AND WHAT IT DOES NOT.  A fixed pipeline is one whose
invariant separates the corrupted build from the true build on those 25.  This
audit does not have one -- constructing it is a mathematical change to claim
(1) and is out of scope -- so the fix is SIMULATED at the point where it would
show: `L_mut` on a blind poset is replaced by a matrix that differs from the
true one.  FOUR WAYS IT COULD DIFFER are run, because the answer is not the
same in all four and a single world would have hidden that:

  FB-diag    the new pair moves a diagonal entry        (forced gate 1 blocks)
  FB-mag     it moves an off-diagonal MAGNITUDE only    (forced gate 2 blocks)
  FB-gauge   it is a genuine diagonal +-1 conjugation   (CLEARS BOTH GATES)
  FB-sign    it flips ONE off-diagonal SIGN pair, on posets where the parity
             system that would absorb it is INCONSISTENT      (CLEARS BOTH
             GATES and is still not absorbable)

These are injections, not corruptions. They say what the section DOES when its
counters move that way; they do not say the mathematics permits it. Two of the
four are known to be reachable in principle -- I4 already has 3 biting posets
whose diagonal survives (FB-mag's class) and 3 classed GAUGE (FB-gauge's).

THE ANSWER, and it is not the one my ticket expects (see PREDICTIONS.md P5/P6):

  * On the three worlds where the newly-seen pairs are BLOCKED, nothing mg-17aa
    added goes red.  The [CANNOT FAIL] row and the falsifiability row both stay
    green.  My ticket's headline question gets NO.
  * On FB-gauge it is different, and the difference is worth the ticket: row I4
    routes back to scored, `absorb == 0` returns to its condition and is FALSE,
    and BOTH mg-17aa rows go red.  That red is CORRECT and not wrong-direction:
    the section is reporting that on those posets the corruption is a gauge,
    which is the thing NEGATIVE CONTROL 4 exists to find out.  A control that
    reddens because the corruption turned out to be absorbable is pointing the
    right way.

So on the question as asked, mg-17aa PASSES -- and the reason the [CANNOT FAIL]
row passes is not the reason its prose gives.  A1 has that.

Run: python3 a2_fixed_blindness.py
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern79ba import (                                          # noqa: E402
    ANCHOR_LMUT, BAR, PRELUDE, Score, head, mutate, rows, row_diff, run,
    sandbox,
)

# The shim is inserted immediately before NEGATIVE CONTROL 4's own function, so
# that `claim1_pair`, `mat_eq` and `mutation_applied_at_site` are all defined
# and every caller below it -- the sweep AND `nc4_row_stats` -- sees the same
# pipeline.
ANCHOR_SHIM = "def negative_control_incidence(nmax):"


S = Score()

# The two rows mg-17aa ADDED or CHANGED THE CONDITION OF.  Everything else in
# the battery predates it, and a red there is not this ticket's question.
ADDED = {
    "PROVEN PROPERTY, not a control row":
        "[CANNOT FAIL] row -- condition changed by mg-17aa to "
        "`theorem_absorb == 0 and theorem_blocked == theorem_app`",
    "falsifiability check, replacing the mg-8a12 routing row":
        "the row mg-17aa ADDED, replacing the wrong-direction routing row",
}

# What the fixed pipeline's L^rel looks like on a blind poset, as source lines
# operating on `L`.  Indented into place by `inject_fix`.
BODIES = {
    "FB-diag": ["L[0][0] += 1"],
    "FB-mag": ["L[0][1] += 1", "L[1][0] += 1"],
    "FB-gauge": ["_s = [-1 if _i == 0 else 1 for _i in range(len(L))]",
                 "L = [[_s[_i] * L[_i][_j] * _s[_j] for _j in range(len(L))]",
                 "     for _i in range(len(L))]"],
    # The first off-diagonal sign pair whose flip the parity system CANNOT
    # absorb -- chosen by asking the shipped predicate, not by guessing, and
    # left alone where no such pair exists.
    "FB-sign": ["for _i in range(len(L)):",
                "    for _j in range(_i + 1, len(L)):",
                "        if not L[_i][_j]:",
                "            continue",
                "        _c = [r[:] for r in L]",
                "        _c[_i][_j] = -_c[_i][_j]",
                "        _c[_j][_i] = -_c[_j][_i]",
                "        if not absorbable_by_diagonal_twist(_c, t):",
                "            L = _c",
                "            break",
                "    else:",
                "        continue",
                "    break"],
}

# A FIFTH WORLD WAS BUILT AND IS NOT RUN, and the reason is stated rather than
# the world quietly dropped.  FB-shape made the fixed pipeline return a SMALLER
# square L^rel.  It does not produce a red: it CRASHES `controls.py` with an
# IndexError in the brute-force agreement instrument check at
# `code/face_geometry/controls.py:1478`, which indexes `A[i][j]` over
# `range(len(L_true))`.  That is a pre-existing fragility -- the line predates
# mg-17aa and is present verbatim in the pinned pre-mg-17aa blob -- and it is
# unreachable by any shipped corruption, because no `incidence_mode` changes
# the facet count and the file says so where it classifies `shape_ok == app` as
# FORCED BY CONSTRUCTION.  It is also not a model of THIS blindness: fixing the
# pipeline's sensitivity does not change how many facets there are.  Reported
# here, not fixed here, and not counted as a finding against mg-17aa.


def body(kind, indent, var="L"):
    return "\n".join(" " * indent + ln.replace("L", var) if var != "L" else
                      " " * indent + ln for ln in BODIES[kind])


def inject_fix(kind, faithful=True):
    """Simulate a pipeline that SEES the corruption on row I4's blind posets.

    APPLIED INSIDE `claim1_pair` AND NOT AT THE SWEEP, and that is the whole
    difference between A2.0 and A2.1 below.  `negative_control_incidence`
    computes its counters twice -- once in its own loop and once through
    `nc4_row_stats`, the second route mg-17aa added -- and a real change to the
    pipeline moves both.  Patching only the sweep does not, and mg-17aa's own
    `agree` check exists to catch exactly that.  `faithful=False` reproduces
    the unfaithful version so the catch can be RUN rather than described.

    Applied only where the corruption already applied at the site and L^rel did
    not move -- i.e. exactly the 25 the artifact calls `applied-but-unseen`.
    `len(L) > 1` because a 1x1 Laplacian has no off-diagonal and no smaller
    square, so three of the four worlds cannot be built there; how many posets
    each world actually reached is PRINTED rather than assumed.
    """
    if not faithful:
        return (ANCHOR_LMUT,
                ANCHOR_LMUT + "\n"
                "            if (mode == 'facet_offbyone' and mat_eq(L_mut, L_true)\n"
                "                    and mutation_applied_at_site(P, mode)\n"
                "                    and len(L_mut) > 1):\n"
                "                L_mut = [r[:] for r in L_mut]\n"
                + body(kind, 16, "L_mut") + "\n")
    return (ANCHOR_SHIM,
            "# ---- mg-79ba FIXED-BLINDNESS SHIM (%s) ----------------------\n"
            "_real_claim1_pair79ba = claim1_pair\n"
            "\n"
            "\n"
            "def claim1_pair(P, *a, **kw):\n"
            "    L, t = _real_claim1_pair79ba(P, *a, **kw)\n"
            "    if kw.get('incidence_mode') != 'facet_offbyone' or len(L) < 2:\n"
            "        return L, t\n"
            "    L0, _ = _real_claim1_pair79ba(P)\n"
            "    if not (mat_eq(L, L0)\n"
            "            and mutation_applied_at_site(P, 'facet_offbyone')):\n"
            "        return L, t\n"
            "    L = [r[:] for r in L]\n"
            "%s\n"
            "    _fx79ba[0] += 1\n"
            "    _fx79ba[1] += not mat_eq(L, L0)\n"
            "    return L, t\n"
            "\n"
            "\n" % (kind, body(kind, 4)) + ANCHOR_SHIM)


REPORT = ("    print('    * mg-79ba FIXED-BLINDNESS INJECTION: reached %d of "
          "row I4's blind posets; %d of them now differ from the true build'\n"
          "          % (_fx79ba[0], _fx79ba[1]))")


def build(kind, faithful=True):
    tree = sandbox()
    missed = mutate(tree, [PRELUDE,
                           ("_inj79ba = {}", "_inj79ba = {}\n_fx79ba = [0, 0]"),
                           inject_fix(kind, faithful)])
    return tree, missed


def show(base, out, code):
    changed, gone, appeared = row_diff(base, rows(out))
    reds = [(a, b, k) for a, b, k in changed if b == "[FAIL]"]
    print("  exit %d; %d row verdict change(s), %d of them to FAIL"
          % (code, len(changed), len(reds)))
    for a, b, k in changed:
        tag = ""
        for key, why in ADDED.items():
            if k.startswith(key):
                tag = "   <== %s" % why
        print("    %s -> %s : %s%s" % (a, b, k[:64], tag))
    for t, k in gone:
        print("    ROW TEXT CHANGED (was %s): %s" % (t, k[:64]))
    for t, k in appeared:
        print("    ROW TEXT CHANGED (now %s): %s" % (t, k[:64]))
    return [k for _, b, k in reds
            if any(k.startswith(key) for key in ADDED)]


def main():
    print(BAR)
    print("mg-79ba A2 -- FIXED-BLINDNESS WORLDS, RUN AGAINST THE BATTERY")
    print(BAR)

    base_tree = sandbox()
    code0, out0 = run(base_tree)
    base = rows(out0)
    S.claim("baseline: the shipped battery exits 0 with %d scored rows"
            % len(base), code0 == 0)
    S.claim("and the artifact states the blindness this section is about: row "
            "I4's 25 vacuous posets are ALL `applied-but-unseen`, 0 "
            "`did-not-apply`, while I1/I2/I3 have none",
            "I4 25 vacuous = 0 did-not-apply + 25 applied-but-unseen" in out0
            and "I1 14 vacuous = 14 did-not-apply + 0 applied-but-unseen" in out0,
            "so the fix has somewhere to bite in exactly one row")
    shutil.rmtree(base_tree, ignore_errors=True)

    # ------------------------------------------------------------- A2.0
    head("A2.0 -- MY OWN FIRST INJECTION WAS UNFAITHFUL, AND mg-17aa's OWN "
         "AGREEMENT CHECK IS WHAT CAUGHT IT.  KEPT, NOT SMOOTHED AWAY")
    print("  The first version of this file patched `L_mut` inside the sweep")
    print("  and nowhere else.  `negative_control_incidence` computes its five")
    print("  counters TWICE -- once in that loop and once through")
    print("  `nc4_row_stats`, the second route mg-17aa added -- so the patch")
    print("  moved one route and not the other.  That is not a fixed pipeline,")
    print("  it is a corrupted instrument, and I reported it as an mg-17aa")
    print("  finding for as long as it took to run the faithful version.")
    print()
    tree, missed = build("FB-diag", faithful=False)
    S.claim("the unfaithful injection lands", not missed)
    code, out = run(tree)
    red_unfaithful = show(base, out, code)
    S.claim("the UNFAITHFUL world turns mg-17aa's falsifiability row RED, and "
            "it is RIGHT to: that row requires `nc4_row_stats` to reproduce "
            "the sweep's own counters on the real input before any exhibit is "
            "believed, and here it cannot.  mg-17aa's own docstring says why "
            "the check is there -- 'two procedures computing one quantity is "
            "how this lineage got a gate name that was not the code's' -- and "
            "this is that check firing on a live example",
            any("falsifiability check" in k for k in red_unfaithful),
            "mg-17aa rows red: %s" % ([k[:60] for k in red_unfaithful] or "none"))
    agr = [l.strip() for l in out.split("\n")
           if "reproduce the main sweep's counters on the real input first" in l]
    S.claim("and the ROW SAYS WHICH HALF FAILED rather than only that it did -- "
            "the agreement count is printed in the row itself, so a reader can "
            "tell 'my second route disagrees' from 'no falsifying input exists'",
            bool(agr) and "does on 4/4 rows" not in agr[0],
            (agr[0][agr[0].index("does on"):][:60] if agr and "does on" in agr[0]
             else "agreement clause not found in the row"))
    shutil.rmtree(tree, ignore_errors=True)

    # ------------------------------------------------------------- A2.1
    verdicts = {}
    for kind in ("FB-diag", "FB-mag", "FB-sign", "FB-gauge"):
        head("A2.1 -- FAITHFUL FIXED-BLINDNESS WORLD %s" % kind)
        tree, missed = build(kind, faithful=True)
        S.claim("%s: every anchor matched exactly once" % kind, not missed,
                "; ".join("%r x%d" % (o[:36], c) for o, c in missed) or "ok")
        code, out = run(tree)
        added_red = show(base, out, code)
        vac = [l.strip() for l in out.split("\n")
               if "TWO MEANINGS OF 'VACUOUS'" in l]
        moved = bool(vac) and "I4 25 vacuous" not in out
        S.claim("%s: the fix reached row I4's blind posets -- the artifact's "
                "own vacuity line moved off `I4 25 vacuous`" % kind, moved,
                (vac[0][vac[0].index("I4 "):][:80] if vac and "I4 " in vac[0]
                 else "vacuity line not found"))
        verdicts[kind] = (code, added_red, out)
        shutil.rmtree(tree, ignore_errors=True)

    head("A2 -- THE ANSWER TO THE TICKET AS ASKED")
    for kind, why in (("FB-diag", "moves a diagonal entry, so forced gate 1 "
                                  "blocks it"),
                      ("FB-mag", "moves an off-diagonal MAGNITUDE with the "
                                 "diagonal intact, so forced gate 2 blocks it")):
        code, added_red, _ = verdicts[kind]
        S.claim("%s -- the pipeline now SEES the corruption on the blind "
                "posets and each newly-seen pair %s.  Row I4 stays forced, and "
                "NO row mg-17aa added or re-conditioned goes red: exit %d"
                % (kind, why, code), added_red == [] and code == 0,
                "mg-17aa rows red: %s" % ([k[:60] for k in added_red] or "none"))

    code, added_red, out = verdicts["FB-sign"]
    S.claim("FB-sign -- THE SHARPEST WORLD, AND THE ONE THE DESIGN IS FOR.  "
            "The newly-seen pairs CLEAR BOTH FORCED GATES (same diagonal, same "
            "magnitudes) and are still NOT absorbable -- the flip is chosen by "
            "asking the shipped predicate, not by guessing.  So the routing "
            "correctly returns row I4 to a SCORED absorbability decision, "
            "`absorb == 0` comes back into its condition and is TRUE, the "
            "[CANNOT FAIL] row covers the other three, and the battery exits "
            "%d with nothing red.  This is mg-17aa's `forced = (blocked == "
            "app)` doing the job its comment claims: 'a corruption that CAN be "
            "absorbed puts the clause back with no edit'" % code,
            added_red == [] and code == 0,
            "mg-17aa rows red: %s" % ([k[:60] for k in added_red] or "none"))

    code, added_red, out = verdicts["FB-gauge"]
    S.claim("FB-gauge -- the newly-seen pairs are a genuine diagonal +-1 "
            "conjugation, so they clear both gates AND are absorbable.  Row I4 "
            "routes back to scored, `absorb == 0` is FALSE, and row I4 plus "
            "mg-17aa's falsifiability row both go red (exit %d).  READ THE "
            "DIRECTION BEFORE READING THE RED: what reddens is the section "
            "reporting that its own corruption is a GAUGE on those posets -- "
            "the question NEGATIVE CONTROL 4 exists to answer.  A control that "
            "reddens because the corruption turned out to be absorbable points "
            "the RIGHT way; it is not mg-e35b's shape" % code,
            code != 0 and len(added_red) >= 1,
            "mg-17aa rows red: %s" % ([k[:60] for k in added_red] or "none"))

    S.claim("SO THE TICKET'S HEADLINE QUESTION IS ANSWERED NO.  In three of "
            "four fixed-blindness worlds -- including the two where the "
            "routing has to make a different decision than it makes today -- "
            "NO row mg-17aa added goes red.  In the fourth it does, and the "
            "cause is what the fix REVEALED about the corruption and not the "
            "fix.  The two are separated by running four fixes that reveal "
            "different things, which is why one world would not have been an "
            "answer",
            all(verdicts[k][1] == [] and verdicts[k][0] == 0
                for k in ("FB-diag", "FB-mag", "FB-sign")),
            "and the reason the [CANNOT FAIL] row survives all four is NOT the "
            "reason its own prose gives -- see a1_cannot_fail.py")

    return S.report()


if __name__ == "__main__":
    sys.exit(main())
