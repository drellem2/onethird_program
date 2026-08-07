"""mg-eaa1 A4 -- AUDIT CHECK 4: audit the NEGATIVE as hard as the positive.

My brief: if the parent claims "ad hoc", audit it as a negative -- is the ABSENCE of a pattern
EXHIBITED, or is it the author not finding one?  mg-131e does not say "ad hoc"; it says the
natural n-indexed shape is *excluded* at the one informative point, which is a much stronger
claim than "not found" and therefore has to be checked rather than accepted.  Two of its
load-bearing negatives are re-derived here on my own rows and my own solver:

  A4.1  THE DUAL OPTIMAL FACE at the two informative hard branches (n = 5).  mg-131e reports
        `lambda in [-1995/2, -1]` and `t_(1,3) in [0,0]`, several coordinates marked "(boxed)"
        because its ranging LP carried a +/-1000 box.  A conclusion drawn from a boxed range is
        a conclusion about the box.  Recomputed here WITHOUT any box on the two coordinates the
        argument actually uses, so that "excluded" means excluded.

  A4.2  PART B2, THE MECHANISM CLAIM, WHERE THE CAVEAT WAS DROPPED.  d2's transcript says
        "at every value-positive branch the optimum flips only consecutive pairs" and then
        caveats itself: "the optimum reported is one vertex of the optimal face, so 0 means no
        REPORTED optimum does, not no optimal measure CAN."  **That caveat is in the transcript
        and is absent from both the document (Section 4) and STATE.md row 167.**  So the
        published sentence is stronger than the measurement under it.  This settles it: over
        the WHOLE optimal face of every value-positive branch at n = 5, maximise the flip mass
        on each NON-consecutive pair.  If every maximum is 0 the sentence is true as published;
        if any is positive it is false as published and true only as transcribed.
"""

import sys
import time
from fractions import Fraction as F

import lib_eaa1 as L

NS = [int(a) for a in sys.argv[1:]] or [5]
fails, notes = [], []


def ok(cond, msg):
    print(f"  [{'OK ' if cond else 'FAIL'}] {msg}")
    if not cond:
        fails.append(msg)
    return cond


HARD5 = [frozenset({(0, 2), (0, 3), (1, 4), (2, 4)}),
         frozenset({(0, 2), (0, 3), (0, 4), (1, 4), (2, 4)})]

print("=" * 92)
print("A4.1  THE DUAL OPTIMAL FACE, UNBOXED, at the two informative hard branches (n = 5).")
print("      mg-131e's ranges are computed with a +/-1000 box; the two coordinates its")
print("      argument rests on are recomputed here with NO box at all.")
print("=" * 92)
for C in HARD5:
    perms, rows, c, labels = L.program(5, C)
    val, _ = L.branch_value(5, C)
    idx, nv = L._layout(rows)
    drows = []
    for j in range(len(c)):
        co = {}
        for i, (rc, _, _) in enumerate(rows):
            a = rc.get(j)
            if a:
                for k, v in L._terms(idx, i, a).items():
                    co[k] = co.get(k, F(0)) + v
        drows.append(({k: v for k, v in co.items() if v}, ">=", F(c[j])))
    ocoef = {}
    for i, (_, _, rhs) in enumerate(rows):
        if rhs:
            for k, v in L._terms(idx, i, F(rhs)).items():
                ocoef[k] = ocoef.get(k, F(0)) + v
    face = drows + [({k: v for k, v in ocoef.items() if v}, "<=", F(val))]

    def extreme(i, sign):
        """max (sign * y_i) over the dual OPTIMAL face.  No box."""
        obj = [F(0)] * nv
        for k, v in L._terms(idx, i, F(sign)).items():
            obj[k] += v
        try:
            v_, _ = L.lp_max(nv, face, obj)
            return v_ * sign if sign == 1 else -v_
        except L.Unbounded:
            return None
        except L.NoSolution:
            return "EMPTY"

    print(f"\n  branch C = {sorted(C)}   val = {val}")
    lam_hi, lam_lo = extreme(0, 1), extreme(0, -1)
    print(f"      lambda  (sum mu = 1)  : max = {lam_hi}   min = "
          f"{'UNBOUNDED BELOW (no box)' if lam_lo is None else lam_lo}")
    ok(lam_hi is not None and lam_hi < 0,
       f"      lambda < 0 across the WHOLE optimal face (max lambda = {lam_hi}) "
       f"-- no certificate here has lambda = 0.  EXCLUDED, not unfound.")
    if lam_lo is None:
        notes.append("lambda is unbounded BELOW on the optimal face at n=5's hard branches, "
                     "so mg-131e's published lower end -1995/2 is an artefact of its "
                     "+/-1000 box.  Its CONCLUSION (lambda < 0 throughout) rests only on the "
                     "upper end, which is -1 and is NOT boxed, so the conclusion survives.")
    for i, lab in enumerate(labels):
        if lab[0] == "cap" and lab[1] == (1, 3):
            hi, lo = extreme(i, 1), extreme(i, -1)
            print(f"      t(1,3)                : max = {hi}   min = {lo}")
            ok(hi == 0, f"      t_(1,3) is forced to 0 across the whole optimal face "
                        f"(max = {hi}) -- so no certificate here has `t` an indicator vector")

print()
print("=" * 92)
print("A4.2  PART B2 -- THE SENTENCE WHOSE CAVEAT WAS DROPPED BETWEEN TRANSCRIPT AND PAGE.")
print("      Over the WHOLE optimal face of every value-positive branch at n = 5, what is the")
print("      largest flip mass ANY optimal measure can put on a NON-consecutive pair?")
print("=" * 92)
for n in NS:
    t0 = time.time()
    cons = set(L.consecutive(n))
    npos = 0
    any_positive = []
    worst = F(0)
    for C in L.all_branches(n):
        perms, rows, c, labels = L.program(n, C)
        if not perms:
            continue
        try:
            val, _ = L.branch_value(n, C)
        except L.NoSolution:
            continue
        if val <= 0:
            continue
        npos += 1
        # the OPTIMAL FACE: the branch constraints plus `objective >= val`, which forces
        # equality because `val` is the maximum.
        face = list(rows) + [({j: c[j] for j in range(len(c)) if c[j]}, ">=", F(val))]
        for i, lab in enumerate(labels):
            if lab[0] != "cap" or lab[1] in cons:
                continue
            obj = [F(0)] * len(c)
            for j, v in rows[i][0].items():
                obj[j] = v
            try:
                qmax, _ = L.lp_max(len(c), face, obj)
            except (L.NoSolution, L.Unbounded):
                continue
            if qmax > 0:
                any_positive.append((sorted(C), lab[1], val, qmax))
                worst = max(worst, qmax)
    print(f"  n={n}: {npos} value-positive branches   [{time.time() - t0:.1f}s]")
    print(f"  branches where SOME optimal measure flips a NON-consecutive pair: "
          f"{len({tuple(a[0]) for a in any_positive})}   "
          f"(branch, pair) instances: {len(any_positive)}   max such flip mass: {worst}")
    for Cs, pr, val, qm in any_positive[:10]:
        print(f"      C={Cs}  pair {pr}  val={val}  max q over the optimal face = {qm}")
    if len(any_positive) > 10:
        print(f"      ... and {len(any_positive) - 10} more")
    if any_positive:
        notes.append(
            f"PART B2's published sentence is FALSE AS PUBLISHED at n={n}: on "
            f"{len({tuple(a[0]) for a in any_positive})} of the {npos} value-positive "
            f"branches SOME optimal measure does flip a non-consecutive pair (max mass "
            f"{worst}).  d2's TRANSCRIPT caveats exactly this and is correct; the document "
            f"Section 4 and STATE.md row 167 drop the caveat and are not.")
    else:
        notes.append(
            f"PART B2's published sentence is TRUE AS PUBLISHED at n={n}: over the whole "
            f"optimal face of all {npos} value-positive branches, NO optimal measure puts "
            f"any mass on a non-consecutive flip.  d2's transcript caveat was sound "
            f"caution; the unqualified sentence on the page happens to be correct, and is "
            f"now checked rather than assumed.")

print()
print("=" * 92)
print("A4 NOTES")
for nte in notes:
    print("  *", nte)
print()
print(f"A4 RESULT: {'ALL CHECKS PASS' if not fails else str(len(fails)) + ' FAILURES'}")
for f in fails:
    print("   FAILED:", f)
print("=" * 92)
sys.exit(1 if fails else 0)
