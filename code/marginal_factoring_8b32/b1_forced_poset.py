"""b1 — THE ANSWER, AND IT IS ONE LINE: `P = {(x,y) : pi_xy = 1}`.

THE QUESTION THIS TICKET WAS FILED TO ASK.  `mg-0fc6`'s `a2.3` proves that realizability is not a
function of the pair marginals, so any map whose input factors through them is realizability-blind.
Daniel's follow-up asked which functions of the POSET `P` factor through the pair marginals, on the
premise — stated in the ticket — that "the poset `P` is strictly more than its pair marginals".

**THAT PREMISE IS FALSE, AND ITS FAILURE IS THE ANSWER.**

    T1.  For any probability measure `mu` on `S_n` with marginal vector `pi = pi(mu)`, put
         `P(pi) := {(x,y) : pi_xy = 1}`.  Then
           (a) `P(pi)` is a strict partial order;
           (b) `supp(mu)` is contained in `L(P(pi))`;
           (c) if `mu` is realizable — uniform on `L(Q)` for some poset `Q` — then `Q = P(pi)`;
           (d) `P(pi)` is a function of `pi` and of nothing else.

    PROOF.  `pi_xy = 1` says exactly that `x` precedes `y` in EVERY order in `supp(mu)`, so the
    relation is an intersection of linear orders: irreflexive, asymmetric and transitive, which is
    (a), and (b) is the same sentence read the other way.  For (c): if `mu = Unif(L(Q))` then
    `x <_Q y` gives `pi_xy = 1`, and `x || _Q y` gives some extension each way, so `pi_xy < 1` —
    the two sets coincide.  (d) is the definition.  QED

    C1 (THE COLLAPSE).  Every function of `P` factors through the pair marginals.  Hence no
    function of `P` — none, at any tier — takes different values on `a2.3`'s two measures, and by
    `a2.3` no function of `P` can inject realizability.

    C2.  `P |-> pi(Unif(L(P)))` is INJECTIVE: distinct posets have distinct marginal vectors.

This arm measures (a), (b), (c) and C2, and then exhibits C1 on a witness of the same shape as
`a2.3`'s, found by an independent route (b2/b3 use the same witness).
"""

from fractions import Fraction
from itertools import combinations
import math

import lib8b32 as L

L.banner("b1.1  C2 — distinct posets have distinct marginal vectors, and P is read off as {pi = 1}")
for n in (3, 4, 5):
    posets = L.all_posets(n)
    seen = {}
    recovered = True
    collide = None
    for lt in posets:
        pi = L.marg_set(L.linexts(n, lt), n)
        key = tuple(pi[k] for k in L.ordered_pairs(n))
        if key in seen and seen[key] != lt:
            collide = (seen[key], lt)
        seen[key] = lt
        if L.forced_poset(pi, n) != lt:
            recovered = False
    L.verdict(recovered, f"n = {n}: P = {{pi = 1}} recovers the poset EXACTLY",
              f"all {len(posets)} labelled posets")
    L.verdict(collide is None and len(seen) == len(posets),
              f"n = {n}: the marginal vector determines the poset",
              f"{len(seen)} distinct marginal vectors for {len(posets)} posets")

L.banner("b1.2  T1(a) and T1(b) — on measures that are NOT linear-extension measures")
# The population is deliberately not the realizable one: T1 is a statement about every measure in
# the information set, and testing it only on posets would test the easy half.
n = 4
S4 = L.linexts(n, L.antichain(n))
pop = []
pop.append(("Unif(S_4)", L.unif(S4)))
pop.append(("two antipodal atoms",
            {(0, 1, 2, 3): Fraction(1, 2), (3, 2, 1, 0): Fraction(1, 2)}))
pop.append(("a single atom", {(0, 1, 2, 3): Fraction(1)}))
pop.append(("(2/3)Unif + (1/3)delta", {sig: Fraction(2, 3) * Fraction(1, 24) for sig in S4}))
pop[-1][1][(0, 1, 2, 3)] += Fraction(1, 3)
pop.append(("a lopsided three-atom", {(0, 1, 2, 3): Fraction(1, 2), (0, 2, 1, 3): Fraction(1, 3),
                                      (2, 0, 1, 3): Fraction(1, 6)}))
ok_a = ok_b = True
for label, mu in pop:
    pi = L.marg(mu, n)
    P = L.forced_poset(pi, n)
    if not L.is_strict_order(n, P):
        ok_a = False
    if not set(L.support(mu)) <= set(L.linexts(n, P)):
        ok_b = False
L.verdict(ok_a, "T1(a): {pi = 1} is a strict partial order on every measure tested",
          f"{len(pop)} measures, none of them a poset's except the first")
L.verdict(ok_b, "T1(b): supp(mu) is contained in L(P(pi)) on every measure tested")

L.banner("b1.3  the n = 6 witness — SAME SHAPE AS a2.3, FOUND BY A DIFFERENT SEARCH")
# a2.3 found its witness by looking for a COMMUTING SQUARE of two disjoint adjacent swaps.  This
# looks for a non-trivial KERNEL of the marginal map, which is the whole space of such directions
# rather than one construction of one of them.  Landing on the same n and the same e(P) by the
# second route is worth more than landing on it by the first twice.
#
# THE SEARCH IS RESTRICTED AND THE RESTRICTION IS EXACT, NOT A SAMPLE: `L*` is always a linear
# extension of `P` (if `x <_P y` then `pi_xy = 1 > 1/2`), so every poset with a coherent `L*` is a
# subrelation of the total order `L*`.  Relabelling so `L* = (0,...,n-1)`, the whole hypothesis
# population at n = 6 is among the transitive subrelations of the 6-chain — 2^15 candidates, not
# 3^15 — and enumerating those is exhaustive for this question, not a sampling.
n = 6
prs = list(combinations(range(n), 2))
ident = tuple(range(n))
witness = None
hyp_pop = 0
for mask in range(1 << len(prs)):
    lt = [[False] * n for _ in range(n)]
    for i, (x, y) in enumerate(prs):
        if mask >> i & 1:
            lt[x][y] = True
    if not L.is_strict_order(n, lt):
        continue
    S = L.linexts(n, lt)
    if len(S) < 2:
        continue
    pi = L.marg_set(S, n)
    if L.lstar(pi, n) != ident:
        continue
    if L.max_flip(pi, ident) > Fraction(1, 3):
        continue
    hyp_pop += 1
    cols, basis = L.kernel_basis(S, n)
    if basis and (witness is None or len(S) < len(witness[1])):
        witness = (tuple(tuple(r) for r in lt), S, cols, basis)
L.verdict(witness is not None,
          "a hypothesis-population poset at n = 6 whose marginal fiber is NOT a point",
          f"e(P) = {len(witness[1])}, kernel dimension {len(witness[3])}")
L.note(f"the whole n = 6 hypothesis population with L* = identity is {hyp_pop} posets")

PW, SW, colsW, basisW = witness
mu1 = L.unif(SW)
d = basisW[0]
scale = min(abs(Fraction(1, len(SW)) / v) for v in d if v != 0) / 2
mu2 = {sig: mu1[sig] + scale * d[i] for i, sig in enumerate(colsW)}
r1, _ = L.realizable(mu1, n)
r2, why2 = L.realizable(mu2, n)
L.verdict(L.marg(mu1, n) == L.marg(mu2, n), "mu1 and mu2 have IDENTICAL pair marginals")
L.verdict(r1, "mu1 IS a linear-extension measure")
L.verdict(not r2, "mu2 is NOT a linear-extension measure", why2)
L.verdict(L.support(mu1) == L.support(mu2), "and they share a SUPPORT",
          "so every predicate reading only the support agrees on them — b3's subject")
L.note(f"H(mu1) = {L.entropy_bits(mu1):.6f}   H(mu2) = {L.entropy_bits(mu2):.6f}"
       f"   log2 e(P) = {math.log2(len(SW)):.6f}   — b4's subject")

L.banner("b1.4  C1 — THE COLLAPSE, on that witness")
pi1, pi2 = L.marg(mu1, n), L.marg(mu2, n)
P1, P2 = L.forced_poset(pi1, n), L.forced_poset(pi2, n)
L.verdict(P1 == P2 == PW, "P(mu1) = P(mu2) = P, recovered from the marginals alone",
          "so the two measures do not even disagree about WHICH POSET they are about")
L.verdict(L.linexts(n, P1) == L.linexts(n, P2),
          "hence L(P) is the same set for both — every SET-level function of L(P) agrees")
L.verdict(L.lstar(pi1, n) == L.lstar(pi2, n), "hence L* is the same for both")
L.note("C1: any function whose input is P — or L(P), or anything built from either — is a")
L.note("function of pi, takes ONE value on this pair, and cannot inject realizability.")

L.banner("b1.5  VACUITY CONTROL — the recovery does NOT recover the measure")
# Without this, b1.1 could be read as "the marginals determine everything", which is the exact
# opposite of a2.3 and would make this whole directory incoherent.  The poset is recoverable; the
# measure is not, and the two statements live at different places.
two_atom = {(0, 1, 2, 3, 4, 5): Fraction(1, 2), (5, 4, 3, 2, 1, 0): Fraction(1, 2)}
pi_two = L.marg(two_atom, 6)
anti6 = L.antichain(6)
pi_anti = L.marg_set(L.linexts(6, anti6), 6)
L.verdict(pi_two == pi_anti,
          "the two-atom measure and Unif(S_6) have IDENTICAL pair marginals", "every pair at 1/2")
L.verdict(L.forced_poset(pi_two, 6) == anti6 == L.forced_poset(pi_anti, 6),
          "and both recover the SAME poset — the antichain")
ra, _ = L.realizable(L.unif(L.linexts(6, anti6)), 6)
rb, whyb = L.realizable(two_atom, 6)
L.verdict(ra and not rb, "yet one is realizable and the other is not", whyb)
L.verdict(len(L.support(two_atom)) != len(L.linexts(6, anti6)),
          "AND THEIR SUPPORTS DIFFER — 2 against 720",
          "which is what b3 needs and a2.3's witness cannot supply")
L.note("So `pi` determines P and does NOT determine mu.  The whole surplus is in the MEASURE:")
L.note("its support and its weights.  Nothing about the poset is left over to be surplus.")

L.finish()
