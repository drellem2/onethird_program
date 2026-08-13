"""c0 — DO THE FOUR OBJECTS EVERYTHING BELOW RESTS ON WORK?

`c1`-`c4` make statements about a set of points nobody can see directly: the image of
`P -> pi(Unif(L(P)))`.  Every one of them is a comparison between two vectors of exact
rationals, so a bug in the enumerator, in `L(P)`, or in the marginal DP does not make an arm
fail — it makes it AGREE, which is the direction this estate has been caught in before.  So
each object is checked against a route that shares no reasoning with it:

    the poset enumerator      against OEIS A001035, and against `lib8b32`'s independent filter
    `L(P)`                    against filtering all of `S_n`
    the marginal DP           against enumerating `L(P)` and counting
    the capped `delta`        against the uncapped one on every poset it will ever be used on
    the chain restriction     against the full enumeration filtered by `P subset of identity`

AND THE ONLY IMPORT OF ANOTHER INSTRUMENT IN THIS DIRECTORY IS HERE.  `lib8b32` is imported by
`c0` and by nothing else: two implementations sharing no algorithm and agreeing on 238 posets is
evidence, and importing it in an ARM would turn the same agreement into a tautology.  That is
`mg-8b32` §3's own discipline applied to `mg-8b32`.
"""

import os
import random
import sys
from fractions import Fraction
from itertools import combinations, permutations

import lib_c776 as L

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "marginal_factoring_8b32"))
import lib8b32 as F                                                   # noqa: E402

# ------------------------------------------------------------------ c0.1

L.banner("c0.1  the poset enumerator against OEIS A001035")
A001035 = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231, 6: 130023}
POSETS = {}
ok = True
for n in range(1, 7):
    POSETS[n] = L.all_posets(n)
    got = len(POSETS[n])
    if got != A001035[n]:
        ok = False
    L.note(f"n = {n}: {got} labelled posets   published {A001035[n]}   "
           f"[{'ok' if got == A001035[n] else 'MISMATCH'}]")
L.verdict(ok, "labelled strict orders reproduce A001035 at n = 1..6",
          "extension-by-a-new-element, not filtering — the route that reaches n = 6")
L.verdict(all(L.is_strict_order(up, n) for n in range(1, 7) for up in POSETS[n]),
          "and every enumerated relation is irreflexive, asymmetric and transitive")

# ------------------------------------------------------------------ c0.2

L.banner("c0.2  L(P) against filtering all of S_n, and the marginal DP against counting L(P)")
rng = random.Random(20260813)
bad_lin = bad_marg = 0
tested = 0
for n in (3, 4, 5):
    pop = POSETS[n] if n <= 4 else rng.sample(POSETS[n], 400)
    for up in pop:
        tested += 1
        brute = tuple(sorted(sig for sig in permutations(range(n))
                             if all(sig.index(x) < sig.index(y)
                                    for x in range(n) for y in range(n) if up[x] >> y & 1)))
        mine = L.linexts(up, n)
        if brute != mine:
            bad_lin += 1
            continue
        e, pi = L.e_and_marginals(up, n)
        if e != len(brute):
            bad_marg += 1
            continue
        ref = L.marg_of_measure(L.unif(brute), n)
        if ref != pi:
            bad_marg += 1
L.verdict(bad_lin == 0, "L(P) agrees with the S_n filter", f"{tested} posets, {bad_lin} mismatches")
L.verdict(bad_marg == 0, "the down-set DP agrees with counting L(P) directly",
          f"{tested} posets, every ordered pair compared exactly, {bad_marg} mismatches")

# ------------------------------------------------------------------ c0.3  NEGATIVE CONTROL

L.banner("c0.3  NEGATIVE CONTROL — the comparison in c0.2 can fail")
# A marginal routine that drops the LAST element's contribution.  If c0.2's comparison were
# vacuous — comparing a thing with itself, or comparing nothing — this would pass it.
def broken_marginals(up, n):
    e, pi = L.e_and_marginals(up, n)
    out = dict(pi)
    for k in out:
        if k[1] == n - 1:
            out[k] = Fraction(0)
    return e, out

caught = 0
trials = 0
for up in POSETS[4]:
    trials += 1
    e, pi = broken_marginals(up, 4)
    if pi != L.marg_of_measure(L.unif(L.linexts(up, 4)), 4):
        caught += 1
L.verdict(caught > 0 and caught == trials - sum(1 for up in POSETS[4]
                                                if all(L.e_and_marginals(up, 4)[1][(x, 3)] == 0
                                                       for x in range(3))),
          "a planted defect in the marginal map is caught by c0.2's comparison",
          f"{caught} of {trials} posets at n = 4 detect it")

# ------------------------------------------------------------------ c0.4

L.banner("c0.4  against lib8b32 — two implementations that share no algorithm")
# lib8b32 enumerates by filtering 3^C(n,2) sign patterns and computes marginals by walking the
# support of the measure.  This file extends posets one element at a time and computes marginals
# by a down-set DP.  Agreement here is agreement between two routes, which is the only kind of
# agreement worth having.
dis = 0
pairs = 0
for n in (3, 4):
    theirs = F.all_posets(n)
    mine = set()
    for up in POSETS[n]:
        mine.add(tuple(tuple(bool(up[x] >> y & 1) for y in range(n)) for x in range(n)))
    if set(theirs) != mine:
        dis += 1
    for lt in theirs:
        pairs += 1
        up = tuple(sum(1 << y for y in range(n) if lt[x][y]) for x in range(n))
        S = F.linexts(n, lt)
        if S != L.linexts(up, n):
            dis += 1
        their_pi = F.marg_set(S, n)
        e, my_pi = L.e_and_marginals(up, n)
        if their_pi != my_pi:
            dis += 1
        if F.forced_poset(their_pi, n) != tuple(tuple(bool(L.forced_poset(my_pi, n)[x] >> y & 1)
                                                      for y in range(n)) for x in range(n)):
            dis += 1
L.verdict(dis == 0, "poset sets, L(P), the marginal vector and P(pi) all agree with lib8b32",
          f"{pairs} posets at n = 3,4, {dis} disagreements")

# ------------------------------------------------------------------ c0.5

L.banner("c0.5  the capped delta against the uncapped one, and the chain restriction")
capbad = 0
for n in (3, 4, 5):
    pop = POSETS[n] if n <= 4 else rng.sample(POSETS[n], 400)
    for up in pop:
        d0, t0, m0 = L.delta_and_flip(up, n)
        d1, t1, m1 = L.delta_and_flip(up, n, cap=Fraction(1, 3))
        if (d0 <= Fraction(1, 3)) != (d1 <= Fraction(1, 3)):
            capbad += 1
        if d0 <= Fraction(1, 3) and (d0, t0, m0) != (d1, t1, m1):
            capbad += 1
L.verdict(capbad == 0, "the early abort decides `delta <= 1/3` exactly as the full scan does",
          "and returns identical values wherever it does not abort")

subbad = 0
for n in (3, 4, 5):
    got = set(L.chain_subrelations(n))
    want = set(up for up in POSETS[n]
               if all(not (up[y] >> x & 1) for x, y in combinations(range(n), 2)))
    if got != want:
        subbad += 1
    L.note(f"n = {n}: {len(got)} posets compatible with the identity order")
L.verdict(subbad == 0, "chain_subrelations is exactly {P : x <_P y implies x < y} from the full "
                       "enumeration", "n = 3,4,5")

# ------------------------------------------------------------------ c0.6

L.banner("c0.6  every marginal vector produced here lies in the linear ordering polytope")
# M_n is the linear ordering polytope: pi_xy + pi_yx = 1 and the 3-dicycle inequalities
# 1 <= pi_xy + pi_yz + pi_zx <= 2 are valid on it.  These are not used as a definition anywhere
# below — they are checked because a "marginal vector" that violated them would not be a
# marginal vector at all, and c1's cell decomposition would be describing nothing.
viol = 0
checked = 0
for n in (3, 4, 5):
    pop = POSETS[n] if n <= 4 else rng.sample(POSETS[n], 200)
    for up in pop:
        e, pi = L.e_and_marginals(up, n)
        checked += 1
        for x, y in combinations(range(n), 2):
            if pi[(x, y)] + pi[(y, x)] != 1:
                viol += 1
        for x, y, z in combinations(range(n), 3):
            for a, b, c in ((x, y, z), (x, z, y)):
                s = pi[(a, b)] + pi[(b, c)] + pi[(c, a)]
                if not (1 <= s <= 2):
                    viol += 1
L.verdict(viol == 0, "pi_xy + pi_yx = 1 and 1 <= pi_xy + pi_yz + pi_zx <= 2",
          f"{checked} image points, {viol} violations")

L.finish()
