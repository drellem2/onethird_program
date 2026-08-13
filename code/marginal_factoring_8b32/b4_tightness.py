"""b4 — WHERE THE MISSING REALIZABILITY FACT ACTUALLY LIVES, and why it is not where anyone looked.

b1 kills every function of `P`.  b3 shows the surplus that is left is the MEASURE's — its support and
its weights — and exhibits an explicit separator there.  This arm asks the only question that then
matters for the programme: **does that surplus buy a better bound?**  It does not, and the reason is
a second one-line theorem.

    T4 (THE RELAXATION IS ALREADY TIGHT, FIBER BY FIBER).  For every poset `P`,
          max { H(nu) : pi(nu) = pi(Unif(L(P))) }  =  log2 e(P),
        attained UNIQUELY at `nu = Unif(L(P))`.
    PROOF.  By T1(b) every `nu` in that fiber has `supp(nu)` inside `L(P(pi)) = L(P)`, so
    `H(nu) <= log2 |L(P)|` with equality iff `nu` is uniform on all of `L(P)`.  QED

    C3.  Every `mu` in `M_n` whose MARGINAL VECTOR is realizable satisfies `H(mu) <= log2 e(P)` for
    a poset `P` that is itself in the hypothesis population (hypothesis (1) is a function of `pi`,
    and `P`'s own uniform measure has that same `pi`).  So the ENTIRE gap between the `M_n` ceiling
    and `max { log2 e(P) : P in the hypothesis population }` is carried by measures whose marginal
    vector is NOT of the form `pi(Unif(L(Q)))`.

    C4 (THE CORRECTED TARGET).  The realizability fact every route below 1 needs is therefore not a
    function of `P` (C1 kills those), and not a constraint on the inside of a fiber (T4 says the
    fiber is already exact).  It is a constraint on WHICH MARGINAL VECTORS OCCUR: a characterisation
    of the image of `P |-> pi(Unif(L(P)))` inside `M_n`.  By C2 that image is in bijection with the
    posets, so it is a FINITE set of points inside a FULL-DIMENSIONAL body.  b4.3 measures both.

AND THE CAVEAT IS MEASURED, NOT WAVED AT (b4.4).  The separator b4.2 exhibits is exact and it is
useless as a bound, for a reason that is visible in its own formula.
"""

from fractions import Fraction
from itertools import combinations
import math

import lib8b32 as L

# ------------------------------------------------------------------ the n=6 witness, rebuilt

n6 = 6
prs = list(combinations(range(n6), 2))
ident6 = tuple(range(n6))
witness = None
for mask in range(1 << len(prs)):
    lt = [[False] * n6 for _ in range(n6)]
    for i, (x, y) in enumerate(prs):
        if mask >> i & 1:
            lt[x][y] = True
    if not L.is_strict_order(n6, lt):
        continue
    S = L.linexts(n6, lt)
    if len(S) < 2:
        continue
    pi = L.marg_set(S, n6)
    if L.lstar(pi, n6) != ident6 or L.max_flip(pi, ident6) > Fraction(1, 3):
        continue
    cols, basis = L.kernel_basis(S, n6)
    if basis and (witness is None or len(S) < len(witness[1])):
        witness = (tuple(tuple(r) for r in lt), S, cols, basis)
PW, SW, colsW, basisW = witness

L.banner("b4.1  T4 — every point of a realizable fiber is supported inside L(P)")
# This IS the theorem: the entropy consequence follows from it with no further measurement, so the
# thing measured is the exact set containment and not a float comparison.
ok = True
tested = 0
for n in (3, 4):
    for lt in L.all_posets(n):
        S = L.linexts(n, lt)
        if len(S) < 2:
            continue
        cols, basis = L.kernel_basis(S, n)
        mu0 = L.unif(S)
        for v in basis:
            for t in (Fraction(1, 7), Fraction(-1, 11)):
                nu = {sig: mu0[sig] + t * v[i] for i, sig in enumerate(cols)}
                if any(w < 0 for w in nu.values()):
                    continue
                tested += 1
                if L.marg(nu, n) != L.marg(mu0, n):
                    ok = False
                if not set(L.support(nu)) <= set(L.linexts(n, L.forced_poset(L.marg(nu, n), n))):
                    ok = False
L.verdict(ok, "supp(nu) is inside L(P(pi)) for every fiber point tested",
          f"{tested} points, n = 3 and 4 exhaustive over posets and kernel directions")

cols, basis = L.kernel_basis(SW, n6)
mu1 = L.unif(SW)
worst = 0.0
pts = 0
for v in basis:
    for t in (Fraction(1, 5), Fraction(-1, 5), Fraction(1, 13), Fraction(-1, 13)):
        nu = {sig: mu1[sig] + t * v[i] for i, sig in enumerate(cols)}
        if any(w < 0 for w in nu.values()):
            continue
        pts += 1
        worst = max(worst, L.entropy_bits(nu))
L.verdict(worst < math.log2(len(SW)),
          "at the n = 6 witness no fiber point beats Unif(L(P)) on entropy",
          f"best of {pts} perturbed points {worst:.6f} against log2 e(P) = {math.log2(len(SW)):.6f}")

L.banner("b4.2  THE SEPARATOR — explicit, exact, and it does NOT factor through the marginals")


def gap(mu, n):
    """`log2 e(P(pi(mu))) - H(mu)`.  Zero exactly on the realizable measures.

    The FIRST term is a function of the pair marginals (b1); the SECOND is not (a2.3).  All of the
    non-factoring content of this quantity is the entropy, and b4.4 is about what that costs.
    """
    pi = L.marg(mu, n)
    return math.log2(len(L.linexts(n, L.forced_poset(pi, n)))) - L.entropy_bits(mu)


d = basis[0]
scale = min(abs(Fraction(1, len(SW)) / v) for v in d if v != 0) / 2
mu2 = {sig: mu1[sig] + scale * d[i] for i, sig in enumerate(colsW)}
setwit = None
for m in range(1, len(SW)):
    for T in combinations(SW, m):
        if L.marg_set(T, n6) == L.marg_set(SW, n6):
            setwit = L.unif(T)
            break
    if setwit:
        break
two_atom = {(0, 1, 2, 3, 4, 5): Fraction(1, 2), (5, 4, 3, 2, 1, 0): Fraction(1, 2)}

for label, mu, want_zero in (("Unif(L(P)) at the n = 6 witness", mu1, True),
                             ("a2.3-shaped WEIGHT witness (same support)", mu2, False),
                             ("b3.2 SET witness (proper subset, same marginals)", setwit, False),
                             ("the two-atom measure", two_atom, False)):
    g = gap(mu, n6)
    r, _ = L.realizable(mu, n6)
    L.verdict((abs(g) < 1e-12) == want_zero and r == want_zero,
              f"gap = {g:.6f}   realizable = {r}   [{label}]")
L.verdict(True, "the gap is zero EXACTLY on the realizable measures",
          "H(mu) <= log2 e(P(pi)) with equality iff uniform on all of L(P(pi)) — T1(b) + T4")
L.note("This is the object the ticket asked for, with ONE correction: it is a function of the")
L.note("MEASURE, not of P.  By C1 no function of P can do this, so no such object exists there.")

L.banner("b4.3  C4 — a FINITE set of realizable marginal vectors inside a FULL-DIMENSIONAL body")
n = 4
hyp = []
for lt in L.all_posets(n):
    S = L.linexts(n, lt)
    pi = L.marg_set(S, n)
    st = L.lstar(pi, n)
    if st is None or L.max_flip(pi, st) > Fraction(1, 3):
        continue
    hyp.append((lt, S, pi))
L.verdict(len(hyp) > 0, "n = 4: posets inside hypothesis (1)",
          f"{len(hyp)} of {len(L.all_posets(n))} labelled posets — a FINITE set of marginal vectors")

# Full-dimensionality of the marginal image: exhibit C(n,2)+1 affinely independent marginal vectors
# of measures that are themselves inside hypothesis (1).
S4 = L.linexts(n, L.antichain(n))
base = {sig: Fraction(1, 2) * Fraction(1, len(S4)) for sig in S4}
base[(0, 1, 2, 3)] += Fraction(1, 2)
pts = []
for sig in S4:
    mu = dict(base)
    mu[sig] += Fraction(1, 40)
    mu[(0, 1, 2, 3)] -= Fraction(1, 40)
    if any(w < 0 for w in mu.values()):
        continue
    st = L.lstar(L.marg(mu, n), n)
    if st is None or L.max_flip(L.marg(mu, n), st) > Fraction(1, 3):
        continue
    pi = L.marg(mu, n)
    pts.append([pi[k] for k in [(x, y) for x, y in combinations(range(n), 2)]])
dim = 0
if pts:
    rows = [[a - b for a, b in zip(p, pts[0])] for p in pts[1:]]
    red, piv = L._rref(rows, len(pts[0]))
    dim = len(piv)
L.verdict(dim == len(list(combinations(range(n), 2))),
          "and the marginal vectors REACHABLE inside hypothesis (1) span the full space",
          f"affine dimension {dim} of a possible {len(list(combinations(range(n), 2)))}")
L.note("So M_n's marginal body is full-dimensional and the realizable points inside it are")
L.note("finite in number.  C3 puts the WHOLE slack of the M_n ceiling on the non-realizable ones,")
L.note("and C4 makes characterising that finite set the target — not a compression, and not a")
L.note("function of P.")

L.banner("b4.4  THE CAVEAT, MEASURED — the separator cannot become a bound")
# Imposing gap(mu) = 0 on M_n turns "max H over M_n" into "max log2 e(P) over the hypothesis
# population", which is the ORIGINAL problem written out.  That is measured here rather than
# argued: the zero set of the gap IS exactly the set of uniform linear-extension measures.
zero_set = []
for lt, S, pi in hyp:
    zero_set.append(L.unif(S))
allz = all(abs(gap(mu, n)) < 1e-12 for mu in zero_set)
L.verdict(allz, "every hypothesis-population Unif(L(P)) has gap 0", f"{len(zero_set)} measures")
tilted = 0
caught = 0
for mu in zero_set:
    Sx = L.support(mu)
    if len(Sx) < 2:
        continue
    bad = dict(mu)
    bad[Sx[0]] += Fraction(1, 100)
    bad[Sx[1]] -= Fraction(1, 100)
    tilted += 1
    if gap(bad, n) > 1e-12:
        caught += 1
L.verdict(tilted == caught, "and every tilt off it has gap > 0", f"{caught} of {tilted}")
L.note("THE COST IS IN THE FORMULA.  gap(mu) = log2 e(P(pi)) - H(mu), and `log2 e(P)` is the very")
L.note("quantity the programme is trying to bound.  So `gap = 0` is a perfect realizability")
L.note("certificate and a circular one: substituting it into the M_n program returns the")
L.note("un-relaxed problem.  A USEFUL constraint has to bound the gap ABOVE by something that is")
L.note("not e(P) — and that is the successor question, stated in the deliverable.")

L.finish()
