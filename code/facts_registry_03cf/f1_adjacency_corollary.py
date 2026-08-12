#!/usr/bin/env python3
"""mg-03cf — the ONE registry entry whose statement is not verbatim in its source document.

`docs/FACTS.md` F1 registers `P(x,y adjacent) <= 2*min(p_xy, 1-p_xy)`, which IS mg-8d66 §4.2
Step 2 read from that document.  Its COROLLARY at a frozen poset --

    delta(P) < 1/3  ==>  P(x,y adjacent) <= 2*delta(P) < 2/3  for EVERY incomparable pair

-- is one line from Step 2 and STATE.md:42's definition of `delta`, and it is stated NOWHERE
in the corpus.  A registry entry carrying a derivation nobody has run is the defect the
registry exists to prevent, so this arm runs what CAN be run, and prints what cannot.

WHAT THIS ARM CAN AND CANNOT DO, and the second half is the point.  F1 itself is checkable and
is checked here on a second implementation.  The COROLLARY is VACUOUS on every population any
instrument can enumerate: `delta(P) < 1/3` is the (1/3)-(2/3) counterexample condition, and the
conjecture is verified to n = 14 (mg-33f5, STATE.md).  So NO frozen poset exists in reach, this
arm reports `0 frozen posets` by construction, and that zero is NOT evidence for the corollary.
The corollary's entire warrant is the one-line derivation.  This file exists to say so at the
site, rather than let a future reader mistake an empty population for a clean sweep -- which is
STATE.md row 3b's `0/132` defect in a new costume.

Imports nothing from this repository: agreement with the arc's instruments would otherwise be a
second reading of one implementation.  External corroboration is that the generator returns
3, 19, 219, 4231 labeled posets at n = 2, 3, 4, 5 (OEIS A001035).

EXITS 0 if every check passes and the self-test holds, 1 otherwise.
"""

import itertools
import random
import sys
from fractions import Fraction

EXHAUSTIVE = (3, 4, 5)
SAMPLED = ((6, 400, 20260812),)     # (n, sample size, deterministic seed)


def posets(n):
    """Every labeled poset on {0..n-1} as a frozenset of strict pairs (x,y) meaning x < y.

    Built by extension: a poset on {0..k-1} plus a choice of the new element k's strict
    down-set D and strict up-set U.  Transitivity forces D down-closed, U up-closed, and
    every element of D below every element of U; antisymmetry forces D and U disjoint.
    """
    if n == 0:
        yield frozenset()
        return
    for rel in posets(n - 1):
        k = n - 1
        below = {x: {y for y in range(n - 1) if (y, x) in rel} for x in range(n - 1)}
        above = {x: {y for y in range(n - 1) if (x, y) in rel} for x in range(n - 1)}
        elems = list(range(n - 1))
        for dbits in itertools.product([0, 1], repeat=n - 1):
            D = {e for e, b in zip(elems, dbits) if b}
            if any(not below[d] <= D for d in D):          # D must be down-closed
                continue
            # U must avoid D and everything at-or-below D, be up-closed, and sit above all of D
            forced_out = set(D) | {y for d in D for y in below[d]}
            cand = [e for e in elems if e not in forced_out]
            for ubits in itertools.product([0, 1], repeat=len(cand)):
                U = {e for e, b in zip(cand, ubits) if b}
                if any(not above[u] <= U for u in U):      # U must be up-closed
                    continue
                if any(u not in above[d] for d in D for u in U):
                    continue
                new = set(rel)
                new.update((d, k) for d in D)
                new.update((k, u) for u in U)
                yield frozenset(new)


def linear_extensions(n, rel):
    """Enumerate legal linear extensions directly, rather than filtering all n! permutations."""
    below = [{y for y in range(n) if (y, x) in rel} for x in range(n)]
    out = []
    order = []
    placed = set()

    def rec():
        if len(order) == n:
            out.append(tuple(order))
            return
        for x in range(n):
            if x in placed or not below[x] <= placed:
                continue
            placed.add(x)
            order.append(x)
            rec()
            order.pop()
            placed.discard(x)

    rec()
    return out


def measure(n, rel):
    """Return {incomparable pair: (p, P(adj))} in exact rationals, or None if no such pair."""
    inc = [(x, y) for x in range(n) for y in range(x + 1, n)
           if (x, y) not in rel and (y, x) not in rel]
    if not inc:
        return None
    LEs = linear_extensions(n, rel)
    N = len(LEs)
    idx = [None] * N
    for i, L in enumerate(LEs):
        pos = [0] * n
        for j, v in enumerate(L):
            pos[v] = j
        idx[i] = pos
    data = {}
    for (x, y) in inc:
        before = adj = 0
        for pos in idx:
            if pos[x] < pos[y]:
                before += 1
            if abs(pos[x] - pos[y]) == 1:
                adj += 1
        data[(x, y)] = (Fraction(before, N), Fraction(adj, N))
    return data


def population():
    """Yield (n, rel, tag) over the declared population.  Sampling is deterministic."""
    for n in EXHAUSTIVE:
        for rel in posets(n):
            yield n, rel, "exhaustive"
    for (n, size, seed) in SAMPLED:
        allp = list(posets(n))
        rng = random.Random(seed)
        for rel in rng.sample(allp, min(size, len(allp))):
            yield n, rel, "sampled(%d of %d, seed %d)" % (min(size, len(allp)), len(allp), seed)


def main():
    ok = True

    print("=" * 88)
    print("mg-03cf  docs/FACTS.md F1, and the status of its frozen corollary")
    print("=" * 88)
    print()

    print("§0  SELF-TEST -- the generator, before it may count anything")
    print("-" * 88)
    counts = [len(list(posets(k))) for k in range(2, 6)]
    a001035 = [3, 19, 219, 4231]
    good = counts == a001035
    ok &= good
    print("  labeled posets at n = 2,3,4,5   %s   vs OEIS A001035 %s   [%s]"
          % (counts, a001035, "PASS" if good else "FAIL"))
    le_anti = len(linear_extensions(5, frozenset()))
    le_chain = len(linear_extensions(5, frozenset((i, j) for i in range(5) for j in range(5) if i < j)))
    good = (le_anti, le_chain) == (120, 1)
    ok &= good
    print("  |L(antichain_5)| = %d (want 120), |L(chain_5)| = %d (want 1)   [%s]"
          % (le_anti, le_chain, "PASS" if good else "FAIL"))
    print()

    f1_fail = []
    cor_fail = []
    pairs = posets_seen = frozen_posets = frozen_pairs = 0
    tightest = None
    tightest_at = None
    per_n = {}
    per_n_pairs = {}

    for (n, rel, _tag) in population():
        data = measure(n, rel)
        if data is None:
            continue
        posets_seen += 1
        per_n[n] = per_n.get(n, 0) + 1
        per_n_pairs[n] = per_n_pairs.get(n, 0) + len(data)
        for ((x, y), (p, pa)) in data.items():
            pairs += 1
            slack = 2 * min(p, 1 - p) - pa
            if slack < 0:
                f1_fail.append((n, sorted(rel), (x, y), str(p), str(pa)))
            if tightest is None or slack < tightest:
                tightest, tightest_at = slack, (n, (x, y), str(p), str(pa))
        delta = max(min(p, 1 - p) for (p, _) in data.values())
        if delta < Fraction(1, 3):
            frozen_posets += 1
            for ((x, y), (p, pa)) in data.items():
                frozen_pairs += 1
                if pa > 2 * delta:
                    cor_fail.append((n, sorted(rel), (x, y), str(delta), str(pa)))

    print("§1  POPULATION, printed rather than left to be inferred")
    print("-" * 88)
    print("  n = 3, 4, 5 exhaustive; n = 6 sampled(%d, seed %d)" % (SAMPLED[0][1], SAMPLED[0][2]))
    print("  posets with at least one incomparable pair, by n:  %s"
          % ", ".join("n=%d: %d" % (k, per_n[k]) for k in sorted(per_n)))
    print("  incomparable pairs, by n:  %s"
          % ", ".join("n=%d: %d" % (k, per_n_pairs[k]) for k in sorted(per_n_pairs)))
    print("  total %d posets, %d incomparable pairs" % (posets_seen, pairs))
    sub5 = sum(per_n_pairs[k] for k in (3, 4, 5) if k in per_n_pairs)
    print("  CROSS-CHECK against mg-8d66 k4.2's own population: its n = 3,4,5 exhaustive sweep")
    print("  reports 18 373 incomparable pairs; this generator reports %d over the same n." % sub5)
    print()

    print("§2  F1 -- P(x,y adjacent) <= 2*min(p_xy, 1-p_xy), every incomparable pair")
    print("-" * 88)
    ok &= not f1_fail
    print("  [%s]  %d failures / %d pairs" % ("PASS" if not f1_fail else "FAIL", len(f1_fail), pairs))
    print("  tightest instance on this population: 2*min(p,1-p) - P(adj) = %s at %s"
          % (tightest, tightest_at))
    print("  (mg-8d66 k4.2 checked the same statement exhaustively at n = 3,4,5 over 18 373")
    print("   incomparable pairs; this is a SECOND implementation, not a second population.)")
    print()

    print("§3  THE COROLLARY -- and why this arm CANNOT be evidence for it")
    print("-" * 88)
    print("  claim   delta(P) < 1/3  ==>  P(adj) <= 2*delta(P) < 2/3 at every incomparable pair")
    print("  frozen posets found on this population: %d" % frozen_posets)
    ok &= not cor_fail
    print("  [%s]  %d failures / %d pairs at frozen posets"
          % ("PASS" if not cor_fail else "FAIL", len(cor_fail), frozen_pairs))
    if frozen_posets == 0:
        print()
        print("  VACUOUS, AND THAT IS THE EXPECTED RESULT, NOT A DEFECT IN THIS ARM.")
        print("  delta(P) < 1/3 IS the (1/3)-(2/3) counterexample condition and the conjecture is")
        print("  verified to n = 14 (mg-33f5).  No frozen poset is enumerable, here or anywhere,")
        print("  so `0 failures` above is zero failures in an EMPTY population and carries no")
        print("  information whatsoever.  The corollary's warrant is its one-line derivation from")
        print("  F1 -- which §2 does check -- and nothing else.  docs/FACTS.md F1 says so in its")
        print("  own SCOPE line; if that line is ever softened, this paragraph is the counter.")
    print()

    for f in f1_fail[:5]:
        print("  F1 FAILURE     ", f)
    for f in cor_fail[:5]:
        print("  COROLLARY FAIL ", f)

    print("VERDICT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
