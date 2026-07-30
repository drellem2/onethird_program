"""The mg-5630 test applied to mg-a3d4's negative-control battery.

mg-5630's lesson was not "add construction-side controls" -- mg-a3d4 did that.
It was sharper: a control must be able to FAIL on the construction it guards.
mg-5630 killed NEGATIVE CONTROL 3 by showing (i) its corruption was absorbable
into a parameter the battery already varied, and (ii) a positive-control-on-the-
control -- injecting a realistic construction bug -- left it silent.

Applied here, the interesting case is X2.  controls.py:287-288 states the
criterion as "the vertex count must stop matching sum_i #proper ideals of Q_i"
-- a comparison against an INDEPENDENT prediction (Theorem L).  controls.py:304
implements a different criterion: `mut == set(verts)`, i.e. "the mutated vertex
set differs from the link as this codebase computes it".

  Q1  does X2-as-implemented still PASS when the link construction it is
      supposed to guard is itself replaced by a buggy one?
  Q2  does X2-as-described (Theorem L vertex count) fire?
  Q3  does the X2 mutation falsify (LG), i.e. break something downstream?
  Q4  X1a: is "uniform weights inflate gamma" empirical or structural?
"""

import sys

from audit_core import (posets_upto_iso, linexts, facet_of, all_faces, blocks,
                        induced, proper_ideals_of, link_1skeleton,
                        lambda2_weighted, at_graph)
from audit_sweep import lambda2_at, lg_bound


def true_link_verts(P, sigma, facets):
    v, _ = link_1skeleton(P, sigma, facets)
    return set(v)


def buggy_link_verts(P, sigma, facets):
    """A realistic construction bug: require comparability only with the TOP
    ideal of sigma instead of with all of it.  (This is exactly the error X2
    was written to guard against.)"""
    pid = proper_ideals_of(P)
    if not sigma:
        return set(pid)
    top = sigma[-1]
    return {K for K in pid if K not in sigma and
            ((K & top) == K or (K & top) == top)}


def x2_mutation(P, sigma, facets):
    return buggy_link_verts(P, sigma, facets)


def theorem_L_vertex_count(P, sigma):
    """sum_i #proper nonempty ideals of the induced subposet on block i."""
    t = 0
    for b in blocks(P, sigma):
        if bin(b).count("1") >= 2:
            t += len(proper_ideals_of(induced(P, b)))
    return t


def main():
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("=" * 78)
    print("AUDIT §10: the mg-5630 test applied to the negative-control battery")
    print("=" * 78)

    print("\nQ1/Q2/Q3  X2, scored three ways")
    print("     as-implemented : mutated vertex set != this codebase's link")
    print("     as-described   : mutated vertex count != Theorem L's prediction")
    print("     downstream     : the mutated links make (LG) FALSE")
    impl_true = [0, 0]
    impl_buggy = [0, 0]
    desc = [0, 0]
    truecount_ok = 0
    truecount_tot = 0
    down_fire = down_vac = 0
    for n in range(3, min(hi, 5) + 1):
        for P in posets_upto_iso(n):
            facets = [facet_of(P, w) for w in linexts(P)]
            fs = all_faces(P)
            mut_g = {}
            for d in sorted(fs):
                for sigma in fs[d]:
                    tv = true_link_verts(P, sigma, facets)
                    bv = buggy_link_verts(P, sigma, facets)
                    mv = x2_mutation(P, sigma, facets)
                    # as-implemented, against the correct construction
                    impl_true[0 if mv == tv else 1] += 1
                    # as-implemented, against a construction that already has
                    # the very bug X2 exists to catch
                    impl_buggy[0 if mv == bv else 1] += 1
                    # as-described: Theorem L's prediction for the vertex count
                    pred = theorem_L_vertex_count(P, sigma)
                    truecount_tot += 1
                    if len(tv) == pred:
                        truecount_ok += 1
                    desc[0 if len(mv) == pred else 1] += 1
            # downstream: does the X2 mutation falsify (LG)?
            gm = {}
            for i in range(-1, P.n - 3):
                best = None
                for sigma in fs.get(i, []):
                    mv = sorted(x2_mutation(P, sigma, facets))
                    idx = {v: j for j, v in enumerate(mv)}
                    s = set(sigma)
                    ew = {}
                    for f in facets:
                        if not s <= set(f):
                            continue
                        r = sorted(set(f) - s)
                        r = [v for v in r if v in idx]
                        for a in range(len(r)):
                            for b in range(a + 1, len(r)):
                                k = (idx[r[a]], idx[r[b]])
                                ew[k] = ew.get(k, 0) + 1
                    lam = lambda2_weighted(len(mv), ew)
                    if lam is None:
                        continue
                    if best is None or lam > best:
                        best = lam
                gm[i] = best
            b = lg_bound(gm)
            tru = lambda2_at(P)
            if tru is None:
                continue
            if tru < b - 1e-9:
                down_fire += 1
            else:
                down_vac += 1
    print("    as-implemented, vs the CORRECT link : fires on %d faces, vacuous on %d"
          % (impl_true[1], impl_true[0]))
    print("    as-implemented, vs the BUGGY  link  : fires on %d faces, vacuous on %d"
          % (impl_buggy[1], impl_buggy[0]))
    print("      -> so X2 is NOT a gauge in disguise: injecting the very bug it")
    print("         mutates toward makes it go silent (0 fires => FAIL).  It is")
    print("         a DISTINGUISHABILITY check -- it certifies the link is not")
    print("         that one alternative object -- and nothing more.  Contrast")
    print("         X1b/X3/X4/X5, which are scored by a downstream FAILURE.")
    print("    the correct link's vertex count matches Theorem L on %d of %d faces"
          % (truecount_ok, truecount_tot))
    print("    as-described (Theorem L count)      : fires on %d faces, vacuous on %d"
          % (desc[1], desc[0]))
    print("    downstream ((LG) falsified)         : fires on %d posets, vacuous on %d"
          % (down_fire, down_vac))

    print("\nQ4  X1a's diagnosis, tested at the two levels it could be meant")
    print("    §10: 'uniform link weights come out with lambda_2 at least as")
    print("    large as the induced-measure ones on every poset here, so the")
    print("    mutated bound is smaller and still true'.")
    worse = tot = 0
    gam_worse = bound_bigger = fires = vac = changed = nposet = 0
    for n in range(3, min(hi, 5) + 1):
        for P in posets_upto_iso(n):
            facets = [facet_of(P, w) for w in linexts(P)]
            fs = all_faces(P)
            gt, gm = {}, {}
            any_change = False
            for i in range(-1, P.n - 3):
                bt = bm = None
                for sigma in fs.get(i, []):
                    v, ew = link_1skeleton(P, sigma, facets)
                    if not ew:
                        continue
                    a = lambda2_weighted(len(v), ew)
                    u = lambda2_weighted(len(v), {k: 1 for k in ew})
                    if a is None or u is None:
                        continue
                    tot += 1
                    if u < a - 1e-9:
                        worse += 1
                    if abs(u - a) > 1e-9:
                        any_change = True
                    bt = a if bt is None else max(bt, a)
                    bm = u if bm is None else max(bm, u)
                gt[i], gm[i] = bt, bm
            for i in gt:
                if gt[i] is not None and gm[i] is not None and gm[i] < gt[i] - 1e-9:
                    gam_worse += 1
            tru = lambda2_at(P)
            if tru is None:
                continue
            nposet += 1
            bt, bm = lg_bound(gt), lg_bound(gm)
            if any_change and abs(bt - bm) > 1e-12:
                changed += 1
            if bm > bt + 1e-12:
                bound_bigger += 1
            if tru < bm - 1e-9:
                fires += 1
            else:
                vac += 1
    print("    at the LINK level: uniform gives a SMALLER lambda_2 on %d of %d"
          " links  -> the sentence as written is FALSE at this level" % (worse, tot))
    print("    at the GAMMA level: uniform gives a smaller gamma_i on %d levels"
          % gam_worse)
    print("    mutated bound strictly LARGER than the true bound on %d posets"
          % bound_bigger)
    print("    X1a fires (mutated bound exceeds the truth) on %d posets;"
          " vacuous on %d; bound value changed on %d" % (fires, vac, changed))
    print("    -> the OPERATIVE half ('X1a cannot fire') is confirmed; the")
    print("       per-link monotonicity offered as its reason is not true.")


if __name__ == "__main__":
    main()
