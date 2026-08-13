#!/usr/bin/env python3
"""c1 — COMBINING THE COMPRESSIONS THEMSELVES IS NEVER A COMPRESSION, ON EITHER FAMILY.

DANIEL'S WORDS, 2026-08-13T00:40Z: *"we can combine them in convex combinations to get one that
mixes what we want the right amount"*.  Taken literally — combine the COMPRESSIONS — the step
fails, and it fails for a reason that has nothing to do with which family they came from:

    THEOREM A.  For orthogonal projections `A`, `B` on a real inner-product space and
    `t ∈ (0,1)`, `M = tA + (1−t)B` is idempotent  ⟺  `A = B`.

    Proof.  `M² = t²A + (1−t)²B + t(1−t)(AB + BA)`, so `M² = M` iff `AB + BA = A + B`.
    Compress with `A` on both sides: `ABA + ABA − A − ABA = 0`, i.e. `ABA = A`.  For a unit
    `x ∈ Ran A`, `⟨ABAx, x⟩ = ‖BAx‖² = ‖x‖² = ‖Ax‖²`, and `‖Bv‖ ≤ ‖v‖` with equality iff
    `v ∈ Ran B`; so `Ran A ⊆ Ran B`.  Symmetrically `Ran B ⊆ Ran A`.  □

`mg-0fc6`'s `a4.3a` measured `(Π_o + Π_e)/2` non-idempotent at **40 of 40** posets where the two
differ, and that measurement is quoted for the proposition that `compression.tex`'s pair is
TRANSVERSE.  IT DOES NOT SHOW THAT.  By Theorem A the non-idempotence follows from
`Π_o ≠ Π_e` alone, and `a4.3a`'s own population is *"posets where the two differ"* — so the
40 of 40 is a measurement of distinctness.  `c1.3` measures it on a NESTED pair, where it comes
out identically, which is the direct demonstration that the row cannot separate the two cases.
Transversality is measured separately, in `c3`, and it is not uniform (`c3.1`).

This is `PREDICTIONS.md` R1 (a report, zero credit) and P4 (live).
"""
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib8748 as L  # noqa: E402

TS = [Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(9, 10)]

# ---------------------------------------------------------------- c1.1 the theorem, exhaustive

L.banner("c1.1  THEOREM A, exhaustively over all partition pairs of a 4- and 5-point space")


def all_partitions(N):
    out = []
    rgs = [0] * N

    def rec(i, mx):
        if i == N:
            out.append(tuple(rgs))
            return
        for v in range(mx + 1):
            rgs[i] = v
            rec(i + 1, max(mx, v + 1))

    rec(0, 0)
    return out


for N in (4, 5):
    parts = all_partitions(N)
    Pis = {p: L.cond_exp_matrix(p) for p in parts}
    bad = 0
    idem_equal = idem_distinct = 0
    distinct_nested = 0
    for i, a in enumerate(parts):
        for b in parts[i:]:
            same = L.nestedness(a, b) == "equal"
            nested = L.nestedness(a, b) in ("a<b", "b<a")
            for t in TS:
                M = L.lincomb([Pis[a], Pis[b]], [t, 1 - t])
                idem = L.mateq(L.matmul(M, M), M)
                if idem != same:
                    bad += 1
                if idem and same:
                    idem_equal += 1
                if idem and not same:
                    idem_distinct += 1
                if nested and not idem:
                    distinct_nested += 1
    L.verdict(bad == 0,
              f"N={N}: tA+(1−t)B is idempotent IFF A = B, at every pair and every t",
              f"{len(parts)}² pairs × {len(TS)} values of t, {bad} exceptions")
    L.verdict(idem_distinct == 0 and idem_equal > 0,
              f"N={N}: and the equality case is non-vacuous",
              f"idempotent at {idem_equal} (equal) and {idem_distinct} (distinct)")
    L.verdict(distinct_nested > 0,
              f"N={N}: ⚠️ NESTED-AND-DISTINCT pairs fail too — nestedness does NOT rescue this",
              f"{distinct_nested} (pair, t) instances nested, distinct, NOT idempotent")

# ---------------------------------------------------------------- c1.2 compression.tex's pair

L.banner("c1.2  compression.tex's (Π_o, Π_e) — reproducing a4.3a's 40 of 40 independently")
# CAP, STATED RATHER THAN DISCOVERED: posets with |L(P)| > 24 are SKIPPED AND COUNTED.  The
# check is an exact |L| × |L| matrix product; the n = 5 antichain alone is 120 × 120 in
# rationals and dominates the whole suite's runtime for a row that is already decided.
CAP = 24
differ = nonidem = skipped = 0
for n in (3, 4, 5):
    for lt in L.all_posets(n):
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        co = L.parity_foliation(LEs, n, lt, 0)
        ce = L.parity_foliation(LEs, n, lt, 1)
        if L.nestedness(co, ce) == "equal":
            continue
        if len(LEs) > CAP:
            skipped += 1
            continue
        differ += 1
        M = L.lincomb([L.cond_exp_matrix(co), L.cond_exp_matrix(ce)],
                      [Fraction(1, 2), Fraction(1, 2)])
        if not L.mateq(L.matmul(M, M), M):
            nonidem += 1
L.verdict(differ > 0 and nonidem == differ,
          "(Π_o+Π_e)/2 is NOT idempotent at every poset where the two differ",
          f"{nonidem} of {differ} posets, n = 3,4,5 labelled, |L(P)| <= {CAP}; "
          f"{skipped} skipped and counted")

# ---------------------------------------------------------------- c1.3 the same on a filtration

L.banner("c1.3  THE SAME MEASUREMENT ON compression2's NESTED SCALES — it comes out IDENTICAL")
rows = []
for n, rel in ((4, []), (6, [(0, 1), (2, 3), (4, 5)]),
               (8, [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7)])):
    # posets chosen so that |L(P)| stays inside the exact-matrix budget; the STRUCTURE under
    # test is the dyadic scale family, which is a function of `n` and `L*`, not of the relation
    lt = L.tclose(n, rel)
    LEs = L.linear_extensions(n, lt)
    parts = L.scale_filtration(LEs, LEs[0], n)
    Pis = [L.cond_exp_matrix(p) for p in parts]
    bad = 0
    tried = 0
    for i in range(len(Pis)):
        for j in range(i + 1, len(Pis)):
            if parts[i] == parts[j]:
                continue
            for t in TS[:2]:
                tried += 1
                M = L.lincomb([Pis[i], Pis[j]], [t, 1 - t])
                if L.mateq(L.matmul(M, M), M):
                    bad += 1
    rows.append((n, len(LEs), len(parts), tried, bad))
    L.verdict(tried > 0 and bad == 0,
              f"n={n}: a convex combination of two DISTINCT SCALES is never idempotent either",
              f"{tried} (pair, t) instances, {bad} idempotent, |L| = {len(LEs)}")
L.verdict(all(r[4] == 0 for r in rows),
          "so the a4.3a row separates NOTHING — the nested family fails it the same way")

L.note("R1 CONFIRMED (a REPORT — the proof is in this file's docstring and predates the code).",
       "P4's first half CONFIRMED: a4.3a's 40 of 40 is a measurement of DISTINCTNESS.  It is",
       "TRUE, it is correctly reported at source, and it does not carry the weight it is",
       "quoted for.  ⚠️ THE CONSEQUENCE FOR HOW THE FACT IS WRITTEN DOWN: 'convex combinations",
       "of nested compressions are canonical' is FALSE.  What is canonical is a convex",
       "combination of the INCREMENTS, and increments are what nestedness buys (c2).")

sys.exit(L.finish())
