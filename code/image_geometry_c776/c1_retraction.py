"""c1 — THE CHARACTERISATION.  The image is the fixed-point set of an idempotent retraction of
the marginal body onto itself, and — the same statement in geometry — it is the set of
VERTEX-BARYCENTRES OF THE BOX-FACES of the linear ordering polytope.

    D1 (THE CELLS).  For `pi` in `M_n`, `P(pi) = {(x,y) : pi_xy = 1}` is a strict partial order
        (mg-8b32 `T1`, cited).  So `M_n` is partitioned into CELLS `C_P = {pi : P(pi) = P}`,
        indexed by posets, and every cell is non-empty — `pi(Unif(L(P)))` is in `C_P`.

    D2 (THE BOX-FACES).  `F_P := {pi in M_n : pi_xy = 1 for all x <_P y}` is the face of `M_n`
        cut out by the BOX inequalities `pi_xy <= 1` alone.  Since `M_n = conv{delta_sigma}` and
        each `pi_xy <= 1` is valid, `F_P = conv{ delta_sigma : sigma in L(P) }` — its vertex set
        is exactly `L(P)`.  `C_P` is the part of `F_P` lying in no smaller box-face.

    T1 (THE RETRACTION).  `r(pi) := pi(Unif(L(P(pi))))` satisfies `P(r(pi)) = P(pi)`, hence
        `r . r = r`.  `r` maps `M_n` onto `R_n` and `Fix(r) = R_n`.
        PROOF of `P(r(pi)) = P(pi)`: if `x <_P y` then every linear extension puts `x` first, so
        `r(pi)_xy = 1`; if `x || y` in `P(pi)` then some extension puts each first, so
        `0 < r(pi)_xy < 1`.  QED — and note it uses only that `L(P)` is non-empty and closed
        under nothing else, which is why it is a THEOREM and not a measurement.

    C1 (THE CHARACTERISATION ASKED FOR).
        `R_n = { the barycentre of the vertex set of F : F a box-face of M_n }`,
        one point per poset, one point per cell.  `pi in R_n` iff `pi = r(pi)`.

WHAT THIS IS NOT.  It is not `b4.4`'s circular separator.  `gap(mu) = log2 e(P(pi)) - H(mu)` is
circular because its FIRST TERM IS THE QUANTITY THE PROGRAMME BOUNDS; the fixed-point condition
mentions neither `e(P)` nor an entropy, so it does not return the un-relaxed problem when
imposed.  What it costs instead is measured in `c2`, and the answer there is worse than
circularity in one respect and better in another.
"""

import math
import random
from fractions import Fraction
from itertools import combinations, permutations

import lib_c776 as L

rng = random.Random(776776)
POSETS = {n: L.all_posets(n) for n in (3, 4, 5)}

# ------------------------------------------------------------------ c1.1

L.banner("c1.1  D1 — the cells are indexed by posets, and every cell is non-empty")
bad = 0
pts = 0
for n in (3, 4, 5):
    for _ in range(150):
        mu, pi = L.rand_body_point(rng, n, rng.randrange(1, 6))
        pts += 1
        if not L.is_strict_order(L.forced_poset(pi, n), n):
            bad += 1
L.verdict(bad == 0, "P(pi) is a strict partial order at every sampled point of M_n",
          f"{pts} exact points, n = 3,4,5, {bad} failures")
missing = 0
for n in (3, 4, 5):
    for up in POSETS[n]:
        e, pi = L.e_and_marginals(up, n)
        if L.forced_poset(pi, n) != up:
            missing += 1
L.verdict(missing == 0, "and every poset's cell is non-empty — pi(Unif(L(P))) is in C_P",
          f"{sum(len(POSETS[n]) for n in (3,4,5))} posets, {missing} empty")

# ------------------------------------------------------------------ c1.2

L.banner("c1.2  D2 — the box-face F_P has vertex set exactly L(P), and r(pi) is its barycentre")
bad_face = 0
bad_bary = 0
for n in (3, 4, 5):
    pop = POSETS[n] if n <= 4 else rng.sample(POSETS[n], 300)
    for up in pop:
        S = L.linexts(up, n)
        # the vertices of M_n satisfying every box equation of P are exactly the sigma in L(P)
        verts = tuple(sorted(sig for sig in permutations(range(n))
                             if all(sig.index(x) < sig.index(y)
                                    for x in range(n) for y in range(n) if up[x] >> y & 1)))
        if verts != S:
            bad_face += 1
        bary = {k: Fraction(0) for k in L.marg_of_measure({S[0]: Fraction(1)}, n)}
        for sig in S:
            for k, v in L.marg_of_measure({sig: Fraction(1)}, n).items():
                bary[k] += v / len(S)
        if bary != L.e_and_marginals(up, n)[1]:
            bad_bary += 1
L.verdict(bad_face == 0, "vert(F_P) = L(P) — the box-face's vertex set is the linear extensions",
          f"{bad_face} mismatches")
L.verdict(bad_bary == 0, "and pi(Unif(L(P))) is exactly the barycentre of those vertices",
          "so the image is a set of face-barycentres, one per box-face")

# ------------------------------------------------------------------ c1.3

L.banner("c1.3  T1 — r is idempotent, and its fixed-point set is exactly the image")
notfix = 0
notidem = 0
for n in (3, 4, 5):
    pop = POSETS[n] if n <= 4 else rng.sample(POSETS[n], 300)
    for up in pop:
        e, pi = L.e_and_marginals(up, n)
        if L.retract(pi, n) != pi:
            notfix += 1
L.verdict(notfix == 0, "every image point is fixed by r", f"{notfix} failures")

moved = 0
fixed_offimage = 0
sampled = 0
for n in (3, 4, 5):
    for _ in range(200):
        mu, pi = L.rand_body_point(rng, n, rng.randrange(2, 6))
        sampled += 1
        r1 = L.retract(pi, n)
        if L.retract(r1, n) != r1:
            notidem += 1
        if r1 != pi:
            moved += 1
        else:
            # a sampled point that r fixes must BE an image point — check it directly
            if pi != L.e_and_marginals(L.forced_poset(pi, n), n)[1]:
                fixed_offimage += 1
L.verdict(notidem == 0, "r . r = r on sampled points of the body", f"{sampled} exact points")
L.verdict(fixed_offimage == 0, "and nothing off the image is fixed by r",
          f"{moved} of {sampled} sampled points are moved by r — the rest ARE image points")

# ------------------------------------------------------------------ c1.4  NEGATIVE CONTROL

L.banner("c1.4  NEGATIVE CONTROL — two wrong retractions, and what each one shows")
# NEAR-MISS 1: send pi to the barycentre of its face's FIRST TWO vertices instead of all of them.
# NEAR-MISS 2: drop the lexicographically first extension and average the rest.
# Both land in M_n and both agree with r on the total orders, so if c1.2/c1.3 were vacuous they
# would pass.  They do not.
def two_vertex(pi, n):
    return L.marg_of_measure(L.unif(L.linexts(L.forced_poset(pi, n), n)[:2]), n)

def drop_one(pi, n):
    S = L.linexts(L.forced_poset(pi, n), n)
    return pi if len(S) < 2 else L.marg_of_measure(L.unif(S[1:]), n)

for name, w in (("two-vertex", two_vertex), ("drop-one", drop_one)):
    wfix = widem = trials = 0
    for up in POSETS[4]:
        e, pi = L.e_and_marginals(up, 4)
        trials += 1
        q = w(pi, 4)
        if q != pi:
            wfix += 1
        if w(q, 4) != q:
            widem += 1
    L.verdict(wfix > 0, f"the planted `{name}` map does NOT fix the image",
              f"{wfix} of {trials} image points moved")
    L.note(f"`{name}`: {widem} of {trials} fail r.r = r")
L.note("AND THE TWO-VERTEX MAP IS IDEMPOTENT ON EVERY ONE OF THE 219 — measured, not assumed.")
L.note("That is worth stating rather than swapping for a control that fails more loudly:")
L.note("IDEMPOTENCE IS NOT THE CONTENT OF T1.  M_n has other retractions onto other sets, and")
L.note("what makes r the image map is WHICH set it fixes (c1.3), not that it is a retraction.")

# ------------------------------------------------------------------ c1.5

L.banner("c1.5  C1 — the image is a transversal of the cells, and its size is the poset count")
for n in (3, 4, 5):
    pts = {}
    for up in POSETS[n]:
        e, pi = L.e_and_marginals(up, n)
        pts[tuple(sorted(pi.items()))] = up
    tot = len(POSETS[n])
    vertices = sum(1 for up in POSETS[n] if L.e_and_marginals(up, n)[0] == 1)
    L.note(f"n = {n}: |R_n| = {len(pts)} of {tot} posets   vertices of M_n among them: {vertices}"
           f" = n! = {math.factorial(n)}")
    L.verdict(len(pts) == tot, f"n = {n}: the map P -> pi(Unif(L(P))) is injective",
              "mg-8b32's C2, reached here by a different marginal algorithm")
L.note("So the image is exactly one point per cell, the cells are indexed by posets, and the")
L.note("point is the cell's box-face barycentre.  That is the characterisation the ticket asked")
L.note("for, and it is EXACT.  c2 measures what it is worth.")

L.finish()
