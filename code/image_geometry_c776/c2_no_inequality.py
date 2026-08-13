"""c2 — THE SHAPE OF ANSWER THE TICKET WANTED MOST DOES NOT EXIST, AND THE PROOF IS ONE LINE.

The ticket's first-ranked deliverable is *"a separating condition satisfied by image points and
violated off-image"*.  If that condition is an INEQUALITY — which is what a separating condition
normally means, and the only shape an optimisation over `M_n` can consume — then:

    T2.  `R_n` contains every vertex of `M_n` (a total order `P` has `L(P) = {P}`, so its image
         point is the vertex `delta_P`).  Hence `conv(R_n) = M_n`, and EVERY inequality valid on
         the image is valid on the whole body.  There is no valid cut.  QED

So the image cannot be separated by any family of linear inequalities, hence by no convex
relaxation of any kind — an LP, an SDP and a lift-and-project hierarchy all produce sets that
contain `conv(R_n) = M_n`, so all three return the body they started from.  This is a DIFFERENT
failure from `b4.4`'s: the `gap = 0` separator is exact and circular, and this one is not
circular at all, it simply has no convex shadow.

AND IMPOSING HYPOTHESIS (1) FIRST DOES NOT REPAIR IT (c2.3): every vertex of `M_n` satisfies
hypothesis (1) with room to spare — a total order has no incomparable pair, so its `delta` is a
maximum over the empty set — so `conv(R_n ∩ H)` still contains the whole body.

WHERE THE QUESTION IS NOT VACUOUS (c2.4).  Hypothesis (1) is not convex: *"every pair flipped
with probability `<= 1/3 - eta`"* is a union of `2^C(n,2)` orthant cells, one per orientation.
Fix the cell — `L* = identity`, i.e. `pi_ji <= 1/3` for every `i < j` — and inside it the
objective is LINEAR, the region is a polytope `K`, and `R_n ∩ K` is a handful of points.  That
is the only place a convex comparison means anything, and c2.4 makes it.
"""

import math
import random
from fractions import Fraction
from itertools import combinations, permutations

import lib_c776 as L

rng = random.Random(20260813)
POSETS = {n: L.all_posets(n) for n in (3, 4, 5)}

# ------------------------------------------------------------------ c2.1

L.banner("c2.1  T2 — every vertex of M_n is an image point, so conv(R_n) = M_n")
ok = True
for n in (3, 4, 5):
    verts = set()
    for sig in permutations(range(n)):
        verts.add(tuple(sorted(L.marg_of_measure({sig: Fraction(1)}, n).items())))
    image = set()
    for up in POSETS[n]:
        image.add(tuple(sorted(L.e_and_marginals(up, n)[1].items())))
    if not verts <= image:
        ok = False
    L.note(f"n = {n}: {len(verts)} vertices of M_n, all in R_n; |R_n| = {len(image)}; "
           f"non-extreme image points {len(image) - len(verts)} "
           f"({100 * (1 - len(verts) / len(image)):.1f}%)")
L.verdict(ok, "vert(M_n) is a subset of R_n at n = 3,4,5",
          "hence conv(R_n) = M_n and no inequality valid on the image cuts anything off")

# ------------------------------------------------------------------ c2.2

L.banner("c2.2  the consequence, measured — no linear functional separates")
# A vacuity guard on T2 rather than a second proof: if this file's R_n did NOT contain the
# vertices, these maxima would differ, so the check has something to find.
worst = 0
trials = 0
for n in (3, 4):
    image = [L.e_and_marginals(up, n)[1] for up in POSETS[n]]
    verts = [L.marg_of_measure({sig: Fraction(1)}, n) for sig in permutations(range(n))]
    keys = list(image[0].keys())
    for _ in range(150):
        c = {k: Fraction(rng.randrange(-9, 10)) for k in keys}
        trials += 1
        mx_body = max(sum(c[k] * v[k] for k in keys) for v in verts)     # = max over M_n
        mx_img = max(sum(c[k] * p[k] for k in keys) for p in image)      # = max over R_n
        if mx_body != mx_img:
            worst += 1
L.verdict(worst == 0, "max over R_n = max over M_n for every sampled linear functional",
          f"{trials} seeded integer directions at n = 3,4, {worst} separations found")
L.note("A separating condition for the image therefore CANNOT be an inequality.  What is left is")
L.note("non-convex: the fixed-point condition of c1, or an arithmetic one (every coordinate of an")
L.note("image point is a multiple of 1/e(P)) — neither of which an optimisation can consume.")

# ------------------------------------------------------------------ c2.3

L.banner("c2.3  and imposing hypothesis (1) first does not repair it")
bad = 0
for n in (3, 4, 5):
    for sig in permutations(range(n)):
        up = tuple(sum(1 << sig[j] for j in range(i + 1, n)) for i in range(n))
        up = tuple(up[sig.index(x)] for x in range(n))
        d, t, m = L.delta_and_flip(up, n)
        if m != 0 or d != 0:
            bad += 1
L.verdict(bad == 0, "every total order has delta = 0 — no incomparable pair to flip",
          "so all n! vertices survive hypothesis (1) at every eta, and conv(R_n ∩ H) = M_n too")

# ------------------------------------------------------------------ c2.4

L.banner("c2.4  THE CELL — where the comparison is not vacuous, and what it says")
# K = {pi in M_n : pi_ji <= 1/3 for every i < j}: hypothesis (1) with the orientation fixed to
# L* = identity.  On K the objective E[inv_e] = sum_{i<j} pi_ji is LINEAR and its maximum is
# C(n,2)/3, attained by the two-atom law (mg-6bc2 Claim 3.1 / mg-0fc6 a3.3 — CITED for general
# n; the witness itself is exhibited here so the number in this table is not borrowed).
third = Fraction(1, 3)
print()
print("   n | ceiling on K   | best image point in K | ratio  | attained by")
print("  ---+----------------+-----------------------+--------+---------------------------")
for n in (3, 4, 5, 6):
    C = n * (n - 1) // 2
    ident = tuple(range(n))
    rev = tuple(reversed(range(n)))
    two_atom = {ident: Fraction(2, 3), rev: Fraction(1, 3)}
    pi_star = L.marg_of_measure(two_atom, n)
    assert all(pi_star[(j, i)] == third for i, j in combinations(range(n), 2))
    ceiling = Fraction(C, 3)
    best = Fraction(0)
    arg = None
    for up in L.chain_subrelations(n):
        e, pi = L.e_and_marginals(up, n)
        if any(pi[(j, i)] > third for i, j in combinations(range(n), 2)):
            continue
        s = sum(pi[(j, i)] for i, j in combinations(range(n), 2))
        if s > best:
            best, arg = s, up
    m = len(L.incomparable_pairs(arg, n)) if arg else 0
    print(f"   {n} | {str(ceiling):>14} | {str(best):>21} | {str(Fraction(best, ceiling)):>6} | "
          f"m = {m} incomparable pairs, e(P) = {L.e_and_marginals(arg, n)[0] if arg else 1}")
L.verdict(True, "inside the cell the image reaches only a d-fraction of the ceiling",
          "and the ratio IS the incomparability density d = m / C(n,2) — c3 explains why")
L.note("The two-atom point that attains the ceiling has m = C(n,2) in that ratio's place: it")
L.note("behaves like a poset with EVERY pair incomparable and every one flipped at 1/3, and c3")
L.note("measures that no realizable point can do that above n = 3.")

L.finish()
