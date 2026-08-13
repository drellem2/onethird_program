#!/usr/bin/env python3
"""c2 — WHAT NESTEDNESS BUYS, AND THE IFF THAT MAKES IT A CRITERION.

`c1` established that combining the COMPRESSIONS convexly is never a compression, on any family.
This arm is the other half: on a NESTED family the right object exists, it is canonical, and
nestedness is exactly — an `iff` — the condition for its existence.

    THEOREM B.  Let `Π_0 ≤ Π_1 ≤ … ≤ Π_K` be conditional expectations of a FILTRATION
    (`Π_a Π_b = Π_min(a,b)`).  Put `D_l = Π_l − Π_{l−1}`.  Then each `D_l` is an orthogonal
    projection, `D_l D_m = 0` for `l ≠ m`, `Σ_l D_l = Π_K − Π_0`, and for any weights
    `λ ∈ ℝ^K` the operator `M = Σ_l λ_l D_l` is self-adjoint, commutes with every `Π_k`, and
    satisfies `M D_l = λ_l D_l` — so its spectrum is exactly `{λ_l}` on the increment spaces.
    With `Π_0 = E` and `Π_K = I`, `Var(f) = Σ_l ‖D_l f‖²` exactly.  That operator is a
    LITTLEWOOD–PALEY MULTIPLIER and it is the object Daniel's convex combination should be.

    THEOREM C (= `PREDICTIONS.md` R2).  For projections `A`, `B`: `B − A` is a projection
    ⟺ `Ran A ⊆ Ran B`.  Proof in `PREDICTIONS.md`; `c2.5` measures it exhaustively.

⚠️ THE HONEST SCOPING, CARRIED VERBATIM FROM `mg-0fc6` §4 RATHER THAN IMPROVED:

    *the variance identity is Pythagoras and holds for ANY filtration.  The content is the
    NESTEDNESS, which is by construction of the dyadic tree.  It is still a real structural
    difference from the transverse pair, and it is the one place Daniel's stated design is
    strictly better than the objects the closed arc used.*

`a4.3b` measured this at ONE poset — the `n = 4` antichain, 3 levels, 5 random `f`.  What is new
here is the population (`n = 4, 6, 8` over several posets), STRUCTURED `f` rather than only
random ones, and Theorem C's `iff`, which `a4.3b` did not state.
"""
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib8748 as L  # noqa: E402

# posets carrying the dyadic scale family, chosen so |L(P)| stays inside the exact-matrix
# budget.  The family under test is a function of `n` and `L*` and NOT of the relation, so the
# relation's only job here is to keep the space small enough to multiply exactly.
POSETS = [
    (4, [], "antichain — a4.3b's own poset, reproduced"),
    (4, [(0, 3)], "one relation"),
    (5, [(0, 1), (1, 2)], "a 3-chain and 2 free"),
    (6, [(0, 1), (1, 2), (3, 4), (4, 5)], "two 3-chains"),
    (6, [(0, 1), (1, 2), (2, 3)], "a 4-chain and 2 free"),
    (7, [(0, 1), (1, 2), (2, 3), (3, 4)], "a 5-chain and 2 free"),
    (8, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (6, 7)], "a 6-chain and a 2-chain"),
]
# ⚠️ CAP, STATED RATHER THAN DISCOVERED.  Every row below is an EXACT |L| × |L| matrix product
# in rationals, so the population is chosen for |L(P)| <= 42, not sampled from anything.  These
# rows say NOTHING about larger spaces; what carries above them is the PROOF (Theorems B and C),
# and c2.5's exhaustive partition sweep, which is about projections and has no poset in it.


def build(n, rel):
    lt = L.tclose(n, rel)
    LEs = L.linear_extensions(n, lt)
    parts = L.scale_filtration(LEs, LEs[0], n)
    return lt, LEs, parts


# ---------------------------------------------------------------- c2.1 it is a filtration

L.banner("c2.1  compression2's SCALES ARE NESTED — both routes, at every poset measured")
built = []
for (n, rel, label) in POSETS:
    lt, LEs, parts = build(n, rel)
    built.append((n, rel, label, lt, LEs, parts))
    cheap = L.is_filtration(parts)
    Pis = [L.cond_exp_matrix(p) for p in parts]
    expensive = all(L.mateq(L.matmul(Pis[a], Pis[b]), Pis[min(a, b)])
                    for a in range(len(Pis)) for b in range(len(Pis)))
    L.verdict(cheap and expensive,
              f"n={n} ({label}): Π_a Π_b = Π_min(a,b), and refinement agrees",
              f"|L| = {len(LEs)}, {len(parts)} levels")
L.verdict(all(L.mateq(L.cond_exp_matrix(b[5][-1]), L.identity(len(b[4]))) for b in built),
          "the FINEST level is the IDENTITY at every poset — losslessness, as an operator",
          f"{len(built)} posets")
L.verdict(all(len(set(b[5][0])) == 1 for b in built),
          "and the COARSEST level is the trivial partition, so Π_0 f = E f")

# ---------------------------------------------------------------- c2.2 the increments

L.banner("c2.2  THE INCREMENTS ARE MUTUALLY ORTHOGONAL PROJECTIONS  (Theorem B)")
INCS = {}
for (n, rel, label, lt, LEs, parts) in built:
    Pis = [L.cond_exp_matrix(p) for p in parts]
    D = [L.lincomb([Pis[k + 1], Pis[k]], [Fraction(1), Fraction(-1)])
         for k in range(len(Pis) - 1)]
    INCS[(n, tuple(rel))] = (LEs, parts, Pis, D)
    allproj = all(L.is_projection(d) for d in D)
    zero = [[Fraction(0)] * len(LEs) for _ in range(len(LEs))]
    orth = all(L.mateq(L.matmul(D[i], D[j]), zero)
               for i in range(len(D)) for j in range(len(D)) if i != j)
    tot = L.lincomb(D, [Fraction(1)] * len(D))
    sums = L.mateq(tot, L.lincomb([Pis[-1], Pis[0]], [Fraction(1), Fraction(-1)]))
    L.verdict(allproj, f"n={n} ({label}): every increment D_l is a PROJECTION",
              f"{len(D)} increments")
    L.verdict(orth, f"n={n} ({label}): and D_l D_m = 0 for l ≠ m")
    L.verdict(sums, f"n={n} ({label}): and Σ_l D_l = I − Π_0")

# ---------------------------------------------------------------- c2.3 Pythagoras

L.banner("c2.3  Var(f) = Σ_l ‖D_l f‖², EXACTLY — random f AND structured f")
random.seed(20260813)
for (n, rel, label, lt, LEs, parts) in built:
    _LEs, _parts, Pis, D = INCS[(n, tuple(rel))]
    star = LEs[0]
    tests = []
    for _ in range(8):
        tests.append(("random", [Fraction(random.randint(-9, 9)) for _ in LEs]))
    # STRUCTURED statistics — the ones this programme actually spends
    pos = {x: i for i, x in enumerate(star)}
    tests.append(("inv_e", [Fraction(sum(1 for i in range(n) for j in range(i + 1, n)
                                         if pos[Lx[i]] > pos[Lx[j]])) for Lx in LEs]))
    tests.append(("pos_x0", [Fraction(Lx.index(0)) for Lx in LEs]))
    tests.append(("disp²", [Fraction(sum((Lx.index(x) - pos[x]) ** 2 for x in range(n)))
                            for Lx in LEs]))
    worst = Fraction(0)
    for _kind, f in tests:
        lhs = L.var(f)
        rhs = sum(L.norm2(L.apply_mat(d, f)) for d in D)
        worst = max(worst, abs(lhs - rhs))
    L.verdict(worst == 0,
              f"n={n} ({label}): exact at all {len(tests)} statistics",
              f"8 random + inv_e + pos_x0 + disp², max |Var − Σ| = {worst}")

# ---------------------------------------------------------------- c2.4 the multiplier

L.banner("c2.4  THE CONVEX COMBINATION OF INCREMENTS IS A LITTLEWOOD–PALEY MULTIPLIER")
for (n, rel, label, lt, LEs, parts) in built:
    _LEs, _parts, Pis, D = INCS[(n, tuple(rel))]
    K = len(D)
    lams = [Fraction(1, k + 2) for k in range(K)]          # arbitrary, distinct, in (0,1]
    tot = sum(lams)
    lams = [x / tot for x in lams]                          # CONVEX: non-negative, summing to 1
    M = L.lincomb(D, lams)
    commutes = all(L.mateq(L.matmul(M, P), L.matmul(P, M)) for P in Pis)
    eig = all(L.mateq(L.matmul(M, D[l]), L.lincomb([D[l]], [lams[l]])) for l in range(K))
    selfadj = L.is_symmetric(M)
    idem = L.mateq(L.matmul(M, M), M)
    nontrivial = any(0 < x < 1 for x in lams)
    L.verdict(commutes and eig and selfadj,
              f"n={n} ({label}): M = Σ λ_l D_l commutes with every Π_k, and M D_l = λ_l D_l",
              f"λ = {[str(x) for x in lams]}")
    L.verdict((not idem) and nontrivial,
              f"n={n} ({label}): and it is NOT idempotent — a multiplier, not a compression")

L.note("THIS is the object Daniel's instinct is right about, and it is right ONLY here:",
       "a convex combination of the INCREMENTS of a NESTED family.  It is diagonal in the",
       "scale decomposition, its spectrum is exactly the weights, and it mixes the scales in",
       "whatever proportion is asked for — 'one that mixes what we want the right amount',",
       "in his words, made precise.  ⚠️ AND THE SCOPING TRAVELS WITH IT: the variance identity",
       "is Pythagoras and holds for ANY filtration.  The content is the NESTEDNESS, which for",
       "compression2 is by construction of the dyadic tree.")

# ---------------------------------------------------------------- c2.5 the iff

L.banner("c2.5  THEOREM C — 'the increment is a projection' IFF 'nested'  (P6)")


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
    ps = all_partitions(N)
    Pis = {p: L.cond_exp_matrix(p) for p in ps}
    bad = nested = notproj = total = 0
    for a in ps:
        for b in ps:
            total += 1
            isnested = L.refines(a, b)            # b refines a  <=>  Ran Pi_a ⊆ Ran Pi_b
            Dm = L.lincomb([Pis[b], Pis[a]], [Fraction(1), Fraction(-1)])
            isproj = L.is_projection(Dm)
            if isnested != isproj:
                bad += 1
            nested += isnested
            notproj += (not isproj)
    L.verdict(bad == 0,
              f"N={N}: Π_b − Π_a is a projection IFF Π_a's σ-algebra is coarser",
              f"{total} ordered pairs ({len(ps)} partitions), {bad} exceptions")
    L.verdict(notproj > total // 2,
              f"N={N}: and the failing side is the MAJORITY — the criterion discriminates",
              f"not a projection at {notproj} of {total}; nested at {nested}")

L.note("P6 CONFIRMED, exhaustive over all set partitions of a 4- and 5-point space.",
       "⚠️ THIS IS THE WHOLE CRITERION, AND IT IS AN IFF, NOT A HEURISTIC: increments exist",
       "exactly when the family is nested.  Everything else — orthogonality, Pythagoras, the",
       "multiplier — follows from having them.  Nestedness is checkable in one pass over the",
       "partitions (c0.5), so the check costs nothing.")

sys.exit(L.finish())
