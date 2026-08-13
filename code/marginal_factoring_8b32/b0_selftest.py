"""b0 — CONTROLS ON THE LIBRARY, before any of it is used to decide a question.

Every later arm in this directory rests on four objects: the poset enumerator, the linear-extension
enumerator, the marginal map and the realizability oracle.  Three of the four are re-derivations of
things `lib0fc6.py` already has, and the reason for re-deriving them is that this ticket's whole
argument is a statement about when two objects AGREE.  An instrument that agrees with itself is
worth nothing, so each is checked against a route that shares no code with it.
"""

from fractions import Fraction
from itertools import permutations

import lib8b32 as L

L.banner("b0.1  the poset enumerator, against the known labelled counts (OEIS A001035)")
KNOWN = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231}
POSETS = {}
for n in (1, 2, 3, 4, 5):
    POSETS[n] = L.all_posets(n)
    L.verdict(len(POSETS[n]) == KNOWN[n], f"n = {n}: labelled strict partial orders",
              f"{len(POSETS[n])} (expected {KNOWN[n]})")

L.banner("b0.2  the linear-extension enumerator, against brute force over all n! permutations")
ok = True
for n in (3, 4):
    for lt in POSETS[n]:
        want = tuple(sorted(
            sig for sig in permutations(range(n))
            if all(sig.index(x) < sig.index(y)
                   for x in range(n) for y in range(n) if lt[x][y])))
        if L.linexts(n, lt) != want:
            ok = False
            break
L.verdict(ok, "L(P) agrees with filtering S_n by the order relation",
          "all 19 posets at n=3, all 219 at n=4")

L.banner("b0.3  the marginal map, against a direct count over the support")
ok = True
for n in (3, 4):
    for lt in POSETS[n]:
        S = L.linexts(n, lt)
        pi = L.marg_set(S, n)
        for x in range(n):
            for y in range(n):
                if x == y:
                    continue
                c = sum(1 for sig in S if sig.index(x) < sig.index(y))
                if pi[(x, y)] != Fraction(c, len(S)):
                    ok = False
L.verdict(ok, "pi_xy = (# extensions with x before y) / e(P)", "n = 3, 4 exhaustive")

L.banner("b0.4  the realizability oracle, against BRUTE FORCE over every poset")
ok = True
checked = 0
for n in (3, 4):
    # positive population: every uniform linear-extension measure
    for lt in POSETS[n]:
        mu = L.unif(L.linexts(n, lt))
        a, _ = L.realizable(mu, n)
        b = L.realizable_bruteforce(mu, n, POSETS[n])
        checked += 1
        if not (a and b):
            ok = False
    # negative population: every uniform measure on an ARBITRARY non-empty subset of L(P)
    for lt in POSETS[n]:
        S = L.linexts(n, lt)
        for k in range(1, len(S)):
            mu = L.unif(S[:k])
            a, _ = L.realizable(mu, n)
            b = L.realizable_bruteforce(mu, n, POSETS[n])
            checked += 1
            if a != b:
                ok = False
L.verdict(ok, "oracle and brute force agree on every case", f"{checked} measures, n = 3 and 4")

L.banner("b0.5  NEGATIVE controls — the oracle must be able to say NO")
n = 4
S = L.linexts(n, L.antichain(n))
mu = L.unif(S)
bad = dict(mu)
bad[S[0]] += Fraction(1, 100)
bad[S[1]] -= Fraction(1, 100)
r, why = L.realizable(bad, n)
L.verdict(not r, "a non-uniform tilt of Unif(S_4) is REJECTED", why)
r, why = L.realizable({S[0]: Fraction(1, 2), S[-1]: Fraction(1, 2)}, n)
L.verdict(not r, "the two-atom measure is REJECTED", why)
r, _ = L.realizable(mu, n)
L.verdict(r, "Unif(S_4) itself is ACCEPTED", "it is L(antichain)")

L.banner("b0.6  the majority order L*, and the kernel of the marginal map")
chain_lt = tuple(tuple(x < y for y in range(4)) for x in range(4))
L.verdict(L.lstar(L.marg_set(L.linexts(4, chain_lt), 4), 4) == (0, 1, 2, 3),
          "L* of a 4-chain is the chain itself")
L.verdict(L.lstar(L.marg_set(S, 4), 4) is None,
          "L* of the antichain does not exist", "every pair is tied at 1/2")

ok = True
dims = []
for n in (3, 4):
    for lt in POSETS[n]:
        Sx = L.linexts(n, lt)
        if len(Sx) < 2:
            continue
        cols, basis = L.kernel_basis(Sx, n)
        dims.append(len(basis))
        for v in basis:
            mu0 = L.unif(Sx)
            plus = {sig: mu0[sig] + Fraction(1, 1000) * v[i] for i, sig in enumerate(cols)}
            if L.marg(plus, n) != L.marg(mu0, n) or sum(plus.values()) != 1:
                ok = False
L.verdict(ok, "every returned kernel vector really moves NO pair marginal",
          f"n = 3, 4 exhaustive; kernel dimensions seen: {sorted(set(dims))}")
L.verdict(max(dims) > 0, "the kernel is non-trivial somewhere",
          "so the fiber over a realizable marginal vector is not always a point")

L.finish()
