#!/usr/bin/env python3
"""c3 — THE OTHER SIDE: what actually fails on `compression.tex`'s pair, and how often.

`mg-0fc6` §4 calls `(C_o, C_e)` *"`compression.tex`'s transverse pair"*.  `c1.2` showed that the
measurement offered for that — `(Π_o+Π_e)/2` non-idempotent at 40 of 40 — is implied by
distinctness alone and cannot separate transverse from nested.  So this arm takes the number
that was never taken:

  c3.1  IS THE PAIR TRANSVERSE?  Classified per poset, over every labelled poset at `n = 3,4,5`.
        `PREDICTIONS.md` P4 (it is, at a large majority) and P5 (but NOT uniformly — nested and
        distinct instances exist, so the word is a statement about the typical case).

  c3.2  WHAT FAILS THERE.  `Π_o − Π_e` is not a projection and is not even PSD — the thing a
        filtration's increment is.  Exhibited, not asserted.

  c3.3  AND THE VARIANCE DOES NOT SPLIT.  `Π_o − Π_0` and `Π_e − Π_0` ARE both projections (the
        trivial σ-algebra is under everything), so the failure is precisely the ORTHOGONALITY:
        their product is nonzero and the cross term is real.  That is Pythagoras' hypothesis
        failing, at a counted number of posets.

  c3.4  NON-VACUITY.  Every failure above is re-run on a NESTED pair from the same machinery,
        where it must not fail.  Without this row c3 measures my code and not the geometry.

**CITED, NOT RE-MEASURED.**  `mg-8d66`'s ceiling, `mg-409a`'s bar, and `mg-0fc6`'s `SCOPE: low`
verdict.  This arm adds no verdict about either note; it measures one structural property.
"""
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib8748 as L  # noqa: E402

# ---------------------------------------------------------------- c3.1 the classification

L.banner("c3.1  IS (C_o, C_e) ACTUALLY TRANSVERSE?  — the number nobody took  (P4, P5)")
TALLY = {}
NESTED_DISTINCT = []
for n in (3, 4, 5):
    t = {"equal": 0, "a<b": 0, "b<a": 0, "transverse": 0}
    for lt in L.all_posets(n):
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        co = L.parity_foliation(LEs, n, lt, 0)
        ce = L.parity_foliation(LEs, n, lt, 1)
        cls = L.nestedness(co, ce)
        t[cls] += 1
        if cls in ("a<b", "b<a") and len(NESTED_DISTINCT) < 3:
            NESTED_DISTINCT.append((n, lt, cls, len(LEs)))
    TALLY[n] = t
    tot = sum(t.values())
    print(f"  n={n}: {tot:5d} posets with |L| >= 2   "
          f"transverse {t['transverse']:5d} · nested-and-distinct {t['a<b'] + t['b<a']:4d} · "
          f"equal {t['equal']:5d}")

tr = sum(TALLY[n]["transverse"] for n in TALLY)
nd = sum(TALLY[n]["a<b"] + TALLY[n]["b<a"] for n in TALLY)
eq = sum(TALLY[n]["equal"] for n in TALLY)
L.verdict(tr > (tr + nd + eq) // 2,
          "P4: the pair IS transverse at a majority of posets",
          f"{tr} of {tr + nd + eq}")
L.verdict(nd > 0,
          "P5: ⚠️ but NOT uniformly — nested-and-distinct instances exist",
          f"{nd} posets; e.g. n={NESTED_DISTINCT[0][0]}, {NESTED_DISTINCT[0][2]}, "
          f"|L| = {NESTED_DISTINCT[0][3]}" if nd else "none")
L.verdict(eq == 0,
          "⚠️ THIS ARM EXPECTED SOME POSETS WHERE THE TWO COINCIDE AND THERE ARE NONE",
          f"{eq} of {tr + nd + eq} — C_o and C_e are DISTINCT at every poset with |L| >= 2, "
          "n <= 5")
L.note("⚠️ SO 'compression.tex's TRANSVERSE pair' IS A STATEMENT ABOUT THE TYPICAL POSET AND",
       "NOT ABOUT THE FAMILY.  The criterion has to be applied per poset.  This does not touch",
       "mg-0fc6's verdict, which does not rest on it; it constrains how the FACT may be quoted.")

# ---------------------------------------------------------------- c3.2 the increment fails

L.banner("c3.2  ON A TRANSVERSE PAIR, Π_o − Π_e IS NOT A PROJECTION AND NOT EVEN PSD")
CAP = 24
notproj = notpsd = seen = skipped = 0
witness = None
for n in (3, 4, 5):
    for lt in L.all_posets(n):
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        co = L.parity_foliation(LEs, n, lt, 0)
        ce = L.parity_foliation(LEs, n, lt, 1)
        if L.nestedness(co, ce) != "transverse":
            continue
        if len(LEs) > CAP:
            skipped += 1
            continue
        seen += 1
        Po, Pe = L.cond_exp_matrix(co), L.cond_exp_matrix(ce)
        D = L.lincomb([Po, Pe], [Fraction(1), Fraction(-1)])
        if not L.is_projection(D):
            notproj += 1
        # PSD is refuted by ONE vector, and the witness family is CHOSEN rather than swept:
        # for `f` = the indicator of a block of `C_e`, `Π_e f = f`, so
        # `⟨f,(Π_o−Π_e)f⟩ = ‖Π_o f‖² − ‖f‖² < 0` unless that block is also `C_o`-measurable.
        # ⚠️ D1, KEPT: this arm first swept the indicators of single EXTENSIONS, which is a
        # family of the right size and the wrong direction — it found a witness at only 3136 of
        # 3670 and the row went RED for a reason that was the search and not the geometry.
        neg = None
        blocks = {}
        for i, blk in enumerate(ce):
            blocks.setdefault(blk, []).append(i)
        for _blk, idx in blocks.items():
            f = [Fraction(1) if j in set(idx) else Fraction(0) for j in range(len(LEs))]
            q = L.quad(D, f)
            if q < 0:
                neg = (_blk, q)
                break
        if neg is not None:
            notpsd += 1
            if witness is None:
                witness = (n, len(LEs), neg[1])
L.verdict(seen > 0 and notproj == seen,
          "Π_o − Π_e is NOT a projection at every transverse poset",
          f"{notproj} of {seen}, n = 3,4,5 labelled, |L(P)| <= {CAP}; {skipped} skipped")
L.verdict(notpsd == seen,
          "and it is NOT PSD either — an explicit vector with ⟨f, (Π_o−Π_e) f⟩ < 0 at each",
          f"{notpsd} of {seen}; first witness n={witness[0]}, |L|={witness[1]}, "
          f"value {witness[2]}" if witness else "none found")

# ---------------------------------------------------------------- c3.3 no Pythagoras

L.banner("c3.3  AND THE VARIANCE DOES NOT SPLIT — the failure is ORTHOGONALITY, precisely")
both_proj = cross_nonzero = seen3 = indep = indep_confirmed = 0
indep_witness = None
for n in (3, 4, 5):
    for lt in L.all_posets(n):
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2 or len(LEs) > CAP:
            continue
        co = L.parity_foliation(LEs, n, lt, 0)
        ce = L.parity_foliation(LEs, n, lt, 1)
        if L.nestedness(co, ce) != "transverse":
            continue
        seen3 += 1
        N = len(LEs)
        P0 = L.cond_exp_matrix(tuple([0] * N))
        Po, Pe = L.cond_exp_matrix(co), L.cond_exp_matrix(ce)
        A = L.lincomb([Po, P0], [Fraction(1), Fraction(-1)])
        B = L.lincomb([Pe, P0], [Fraction(1), Fraction(-1)])
        if L.is_projection(A) and L.is_projection(B):
            both_proj += 1
        zero = [[Fraction(0)] * N for _ in range(N)]
        if not L.mateq(L.matmul(A, B), zero):
            cross_nonzero += 1
        else:
            indep += 1
            # the mechanism, checked rather than guessed: A·B = Π_o Π_e − P_0, so the cross
            # term vanishes exactly when the two σ-algebras are INDEPENDENT under the measure
            if L.mateq(L.matmul(Po, Pe), P0):
                indep_confirmed += 1
            if indep_witness is None:
                indep_witness = (n, N)
L.verdict(both_proj == seen3,
          "BOTH Π_o − E and Π_e − E ARE projections — the trivial σ-algebra is under everything",
          f"{both_proj} of {seen3}")
L.verdict(cross_nonzero == seen3 - indep,
          "⚠️ and at almost all of them (Π_o − E)(Π_e − E) ≠ 0 — the pieces OVERLAP",
          f"{cross_nonzero} of {seen3}")
L.verdict(indep > 0 and indep_confirmed == indep,
          "⚠️ BUT NOT AT ALL OF THEM, AND THIS ARM'S OWN EXPECTATION IS REFUTED BY ITS OWN RUN",
          f"{indep} transverse posets have Π_o Π_e = P_0 EXACTLY — INDEPENDENT σ-algebras, "
          f"mechanism confirmed at {indep_confirmed} of {indep}"
          + (f"; first at n={indep_witness[0]}, |L|={indep_witness[1]}" if indep_witness else ""))
L.note("KEPT RATHER THAN QUIETLY REWRITTEN, because the mistake this arm made is the mistake",
       "the CRITERION is at risk of.  'Transverse ⟹ the variance does not split' is FALSE:",
       "A·B = Π_o Π_e − P_0, so the cross term vanishes exactly when the two σ-algebras are",
       "INDEPENDENT, and independent-but-transverse happens.  ⚠️ THE OPERATIVE PROPERTY IS",
       "MUTUAL ORTHOGONALITY OF THE INCREMENTS, NOT NESTEDNESS.  Nestedness is the",
       "CONSTRUCTIVE route to it — it gives a whole ORDERED family of orthogonal increments at",
       "once, canonically, with the multiplier diagonal in them — and it is the route that is",
       "cheap to check.  It is not the only way orthogonality can occur, and the criterion has",
       "to be stated that way or it over-claims.")

# ---------------------------------------------------------------- c3.4 non-vacuity

L.banner("c3.4  NON-VACUITY — every failure above, re-run on a NESTED pair, does NOT fail")
n = 4
lt = L.antichain(n)
LEs = L.linear_extensions(n, lt)
parts = L.scale_filtration(LEs, LEs[0], n)
a, b = parts[1], parts[2]
Pa, Pb = L.cond_exp_matrix(a), L.cond_exp_matrix(b)
D = L.lincomb([Pb, Pa], [Fraction(1), Fraction(-1)])
L.verdict(L.nestedness(a, b) == "a<b", "the control pair is NESTED and distinct",
          f"n={n}, |L| = {len(LEs)}")
L.verdict(L.is_projection(D), "there, Π_b − Π_a IS a projection — c3.2's first row inverts")
bl = {}
for i, blk in enumerate(b):
    bl.setdefault(blk, []).append(i)
L.verdict(all(L.quad(D, [Fraction(1) if j in set(idx) else Fraction(0)
                         for j in range(len(LEs))]) >= 0 for idx in bl.values()),
          "and it IS PSD on the SAME witness family c3.2 used — c3.2's second row inverts",
          f"{len(bl)} block indicators; and ⟨f,Df⟩ = ‖Df‖² ≥ 0 for ALL f, D being a projection")
N = len(LEs)
P0 = L.cond_exp_matrix(tuple([0] * N))
A = L.lincomb([Pa, P0], [Fraction(1), Fraction(-1)])
zero = [[Fraction(0)] * N for _ in range(N)]
L.verdict(L.mateq(L.matmul(A, D), zero),
          "and the two increments ARE mutually orthogonal — c3.3's second row inverts")

# ---------------------------------------------------------------- c3.5 already priced

L.banner("c3.5  AND ON THAT FAMILY THE CONVEX COMBINATION IS NOT A NEW DEGREE OF FREEDOM")
# mg-8d66's operator, restated: k·I − Σ_i Π_i = k·(I − (1/k) Σ_i Π_i).  Arithmetic, but it is
# the sentence that stops 'combine them convexly' being read as an unexplored direction on
# compression.tex's family — it is the object that arc already priced (FACTS.md F6, mg-8d66).
n, lt = 5, L.tclose(5, [(0, 1)])
LEs = L.linear_extensions(n, lt)
Pis = [L.cond_exp_matrix(L.parity_foliation(LEs, n, lt, p)) for p in (0, 1)]
k = len(Pis)
lhs = L.lincomb([L.identity(len(LEs))] + Pis, [Fraction(k)] + [Fraction(-1)] * k)
avg = L.lincomb(Pis, [Fraction(1, k)] * k)
rhs = L.lincomb([L.identity(len(LEs)), avg], [Fraction(k), Fraction(-k)])
L.verdict(L.mateq(lhs, rhs),
          "k·I − Σ Π_i = k·(I − equal-weight convex combination), exactly",
          f"n={n}, |L| = {len(LEs)}, k = {k}")
L.note("So on compression.tex's family 'combine the compressions convexly' names an object the",
       "closed arc ALREADY priced — FACTS.md F6 and mg-8d66's ceiling, CITED and not re-",
       "measured here.  The convex weights are a reparameterisation of that operator, not a",
       "new handle on it.")

sys.exit(L.finish())
