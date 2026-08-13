"""c4 — HOW FAR THE CEILING SITS FROM THE IMAGE, AND WHETHER HYPOTHESIS (1) CONFINES YOU NEAR IT.

The ticket asks two more questions and this arm answers both at the one point where the answer
matters — the marginal vector that carries the whole `M_n` ceiling.

    `pi*` := the marginal vector of the two-atom law `(2/3) delta_id + (1/3) delta_reverse`.
    Every pair is flipped at exactly `1/3`, so `pi*` is in hypothesis (1) at `eta = 0` and
    `E[inv_e](pi*) = C(n,2)/3 = the maximum over M_n` (`mg-0fc6` `a3.3`, `mg-6bc2` Claim 3.1 —
    cited for all `n`; the witness is rebuilt here so the numbers are this file's own).

    T4.  `P(pi*)` is the ANTICHAIN — no coordinate of `pi*` is `1` — so the unique image point in
         `pi*`'s own cell is `r(pi*) = pi(Unif(S_n))`, every coordinate `1/2`.
         `||pi* - r(pi*)||_inf = 1/6` exactly, at every `n`.

    T5.  And that is the NEAREST image point of all: every other poset has a comparable pair,
         whose coordinate is `0` or `1` against `pi*`'s `1/3`, so no other image point is within
         `1/3`.  Measured exhaustively over `R_n` at `n = 3,4,5`.

    C3 (THE ANSWER TO "DOES HYPOTHESIS (1) CONFINE YOU NEAR THE IMAGE?").  No.  `pi*` satisfies
         hypothesis (1) with every pair at the bound, and the image point nearest to it is the
         ANTICHAIN — `delta = 1/2`, the single worst violator of hypothesis (1) there is.  So
         the retraction of the ceiling-carrying point leaves the hypothesis region, and it moves
         the objective the WRONG WAY: `C(n,2)/3 -> C(n,2)/2`.  "Project onto the image" is not a
         repair, it is a bigger violation.
"""

from fractions import Fraction
from itertools import combinations, permutations

import lib_c776 as L

POSETS = {n: L.all_posets(n) for n in (3, 4, 5)}
third = Fraction(1, 3)

# ------------------------------------------------------------------ c4.1

L.banner("c4.1  the ceiling-carrying point, rebuilt")
STAR = {}
for n in (3, 4, 5, 6):
    ident = tuple(range(n))
    rev = tuple(reversed(range(n)))
    pi = L.marg_of_measure({ident: Fraction(2, 3), rev: Fraction(1, 3)}, n)
    STAR[n] = pi
    C = n * (n - 1) // 2
    obj = sum(pi[(j, i)] for i, j in combinations(range(n), 2))
    ok = all(pi[(j, i)] == third for i, j in combinations(range(n), 2)) and obj == Fraction(C, 3)
    L.verdict(ok, f"n = {n}: every pair flipped at exactly 1/3, E[inv_e] = C(n,2)/3 = {obj}",
              f"eps_spec = {L.eps_spec(obj, n)} = n/(n+1) = {Fraction(n, n+1)}")

# ------------------------------------------------------------------ c4.2

L.banner("c4.2  T4 — pi* lives in the ANTICHAIN's cell, and its retraction is the uniform point")
for n in (3, 4, 5, 6):
    up = L.forced_poset(STAR[n], n)
    r = L.retract(STAR[n], n)
    unif_pt = L.marg_of_measure(L.unif(list(permutations(range(n)))), n)
    L.verdict(up == tuple([0] * n) and r == unif_pt and L.linf(STAR[n], r, n) == Fraction(1, 6),
              f"n = {n}: P(pi*) is the antichain, r(pi*) = 1/2 everywhere, "
              f"||pi* - r(pi*)||_inf = 1/6")

# ------------------------------------------------------------------ c4.3

L.banner("c4.3  T5 — and no image point is closer, over the WHOLE image")
for n in (3, 4, 5):
    best = None
    argm = None
    ties = 0
    for up in POSETS[n]:
        e, pi = L.e_and_marginals(up, n)
        d = L.linf(STAR[n], pi, n)
        if best is None or d < best:
            best, argm, ties = d, up, 1
        elif d == best:
            ties += 1
    dl, tl, ml = L.delta_and_flip(argm, n)
    L.verdict(best == Fraction(1, 6) and argm == tuple([0] * n) and ties == 1,
              f"n = {n}: min over R_n of ||pi* - .||_inf is {best}, attained uniquely",
              f"at the antichain, whose delta is {dl} — the WORST violator of hypothesis (1)")
L.note("So the point carrying the entire M_n ceiling is 1/6 from the image in the sup norm, and")
L.note("the image point it is nearest to is the one furthest OUTSIDE hypothesis (1).  Hypothesis")
L.note("(1) does not confine a measure to the neighbourhood of the image — that is C3.")

# ------------------------------------------------------------------ c4.4

L.banner("c4.4  the retraction moves the objective the WRONG WAY")
for n in (3, 4, 5, 6):
    C = n * (n - 1) // 2
    before = sum(STAR[n][(j, i)] for i, j in combinations(range(n), 2))
    r = L.retract(STAR[n], n)
    after = sum(min(r[(j, i)], r[(i, j)]) for i, j in combinations(range(n), 2))
    L.verdict(after > before, f"n = {n}: E[inv_e] goes {before} -> {after} under r",
              f"C(n,2)/3 -> C(n,2)/2, and delta goes 1/3 -> 1/2")

# ------------------------------------------------------------------ c4.5

L.banner("c4.5  how far a point of M_n can sit from the image — SAMPLED, and the cap is stated")
# This is the ticket's third question in general position.  It is a SAMPLE and it is labelled
# one: the maximum of dist(pi, R_n) over the whole body is not computed here, and a sampled
# maximum is a lower bound on it and nothing else.
import random                                                          # noqa: E402
rng = random.Random(776)
for n in (3, 4):
    image = [L.e_and_marginals(up, n)[1] for up in POSETS[n]]
    worst = Fraction(0)
    for _ in range(120):
        mu, pi = L.rand_body_point(rng, n, rng.randrange(2, 7))
        d = min(L.linf(pi, q, n) for q in image)
        if d > worst:
            worst = d
    L.note(f"n = {n}: over 120 seeded exact points of M_n, the largest distance to R_n found is "
           f"{worst} ({float(worst):.4f})")
L.verdict(True, "a sampled lower bound on sup_{pi in M_n} dist(pi, R_n), NOT a maximum",
          "the exact maximum is not computed and is not claimed")

L.finish()
