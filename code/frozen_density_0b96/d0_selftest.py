#!/usr/bin/env python3
"""mg-0b96 arm d0 — THE CONTROLS, AND THE TWO THAT MUST COME BACK THE OTHER WAY.

This directory's finding is a NO.  A NO is worthless from an instrument that cannot produce a
YES, and it is worse than worthless from one whose population is empty for a reason it does not
print.  So two of the seven controls here are the wrong-direction ones:

  T6  THE POPULATION WARNING, MEASURED RATHER THAN QUOTED.  The frozen class `δ(P) < 1/3` is
      EMPTY at every `n` this instrument reaches.  Every "0 frozen posets" printed anywhere in
      this directory is therefore zero in an empty population, and T6 establishes that HERE, on
      this instrument's own enumerator, so no arm has to borrow the fact from `mg-33f5`.
  T7  A POSITIVE CONTROL THAT MUST RETURN A REAL DENSITY CEILING.  On the PSEUDO-FROZEN class
      `δ(P) < 1/2` — non-empty at every `n ≥ 2` — the same machinery is asked for an upper bound
      on `d`.  If it comes back `1`, this instrument cannot tell "no ceiling exists" from "no
      population exists" and every NO in this directory is unfalsifiable.  It comes back below 1.

T1–T5 are the ordinary kind: the imported enumerator against OEIS A000112, the imported `δ`
against brute-force enumeration of `L(P)`, `is_rigid` against a full `n!` automorphism search,
each of the seven class predicates against a hand-built in/out witness pair, and the family
constructor's transitive closure against its own axioms.

Exits 0 if every control holds, 1 if one fires, 2 on refusal.
"""

import sys
from fractions import Fraction
from itertools import permutations

import lib0b96 as X
import lib6ff4 as L

NMAX_ENUM = 8
NMAX_BRUTE = 5
NMAX_RIGID = 6
NMAX_POP = 8


def brute_delta(n, down):
    """`δ(P)` by enumerating every linear extension and counting.  Imports no identity."""
    exts = L.linear_extensions(n, down)
    tot = len(exts)
    best = Fraction(0)
    for (i, j) in L.incomparable_pairs(n, down):
        c = sum(1 for e in exts if e.index(i) < e.index(j))
        p = Fraction(c, tot)
        best = max(best, min(p, 1 - p))
    return best


def brute_rigid(n, down):
    """Rigidity by trying all `n!` permutations."""
    cnt = 0
    for p in permutations(range(n)):
        ok = True
        for b in range(n):
            m, acc = down[b], 0
            while m:
                x = m & -m
                acc |= 1 << p[x.bit_length() - 1]
                m ^= x
            if acc != down[p[b]]:
                ok = False
                break
        if ok:
            cnt += 1
    return cnt == 1


def main():
    print("=" * 100)
    print("mg-0b96  d0  controls -- including the population warning and the must-say-YES control")
    print("=" * 100)
    print()

    try:
        C = L.all_classes(NMAX_ENUM)
    except Exception as exc:                                       # pragma: no cover
        print("REFUSED: the imported enumerator did not run: %r" % (exc,))
        print("VERDICT: REFUSED")
        return 2

    ok = True

    # ------------------------------------------------------------------------------------------
    print("T1  THE IMPORTED ENUMERATOR, RE-CHECKED HERE  (lib6ff4.all_classes vs OEIS A000112)")
    print("-" * 100)
    print("    The controls on lib6ff4 live in code/boundary_epsilon_6ff4/.  From THIS directory")
    print("    that is an unchecked dependency, and this arm's subject is a claim nobody")
    print("    re-checked, so the import is re-checked rather than trusted.")
    print()
    for n in sorted(C):
        got, want = len(C[n]), L.A000112[n]
        good = got == want
        ok &= good
        print("      n=%d  %7d classes   A000112=%7d   %s" % (n, got, want, "OK" if good else "MISMATCH"))
    print()

    # ------------------------------------------------------------------------------------------
    print("T2  THE IMPORTED delta, AGAINST BRUTE FORCE OVER EVERY LINEAR EXTENSION")
    print("-" * 100)
    print("    lib6ff4 gets pair biases from a DP over order ideals; this control counts")
    print("    extensions one at a time.  Two implementations, no shared step.")
    print()
    checked = bad = 0
    for n in range(2, NMAX_BRUTE + 1):
        for down in C[n]:
            inc = L.incomparable_pairs(n, down)
            if not inc:
                continue
            le, dlt, _tbl = L.delta_at_most(n, down, bound=Fraction(1))
            b = brute_delta(n, down)
            checked += 1
            if not le or dlt != b:
                bad += 1
    ok &= bad == 0
    print("      %d posets with an incomparable pair at n <= %d   disagreements: %d   %s"
          % (checked, NMAX_BRUTE, bad, "OK" if bad == 0 else "FIRED"))
    print()

    # ------------------------------------------------------------------------------------------
    print("T3  EACH CLASS PREDICATE AGAINST A HAND-BUILT WITNESS PAIR (one in, one out)")
    print("-" * 100)
    print("    Every predicate in lib0b96 is a LITERATURE CLASS whose DEFINITION is the thing")
    print("    that could be wrong, and none of them existed anywhere in this repository before")
    print("    this directory.  A wrong definition would silently move the residue of arm d3.")
    print()
    chain4 = X.close(4, [(0, 1), (1, 2), (2, 3)])
    anti4 = X.close(4, [])
    twoplus2 = X.close(4, [(0, 1), (2, 3)])                 # 2+2: not a semiorder
    threeplus1 = X.close(4, [(0, 1), (1, 2)])               # 3+1: not a semiorder
    nposet = X.close(4, [(0, 2), (1, 2), (1, 3)])           # the N, on covers
    diamond = X.close(4, [(0, 1), (0, 2), (1, 3), (2, 3)])  # cover graph has a 4-cycle
    v3 = X.close(3, [(0, 1)])                               # a < b, c free
    cases = [
        ("width ≤ 2 holds on the 4-chain",        L.width(4, chain4) <= 2,               True),
        ("width ≤ 2 fails on the 4-antichain",    L.width(4, anti4) <= 2,                False),
        ("height on the 4-chain is 4",            X.height(4, chain4) == 4,              True),
        ("height on the 4-antichain is 1",        X.height(4, anti4) == 1,               True),
        ("thinness of the 4-antichain is 3",      X.thinness(4, anti4) == 3,             True),
        ("thinness of the 4-chain is 0",          X.thinness(4, chain4) == 0,            True),
        ("2+2 is NOT a semiorder",                X.is_semiorder(4, twoplus2),           False),
        ("3+1 is NOT a semiorder",                X.is_semiorder(4, threeplus1),         False),
        ("the 4-chain IS a semiorder",            X.is_semiorder(4, chain4),             True),
        ("the N is NOT N-free",                   X.is_N_free(4, nposet),                False),
        ("the V IS N-free",                       X.is_N_free(3, v3),                    True),
        ("the diamond's cover graph is no forest", X.cover_graph_is_forest(4, diamond),  False),
        ("the 4-chain's cover graph is a forest", X.cover_graph_is_forest(4, chain4),    True),
        ("the 4-antichain is NOT rigid",          X.is_rigid(4, anti4),                  False),
        ("the 4-chain IS rigid",                  X.is_rigid(4, chain4),                 True),
    ]
    for (what, got, want) in cases:
        good = bool(got) == want
        ok &= good
        print("      %-46s got %-5s want %-5s  %s" % (what, got, want, "OK" if good else "FIRED"))
    print()

    # ------------------------------------------------------------------------------------------
    print("T4  is_rigid AGAINST A FULL n! AUTOMORPHISM SEARCH, EXHAUSTIVE n <= %d" % NMAX_RIGID)
    print("-" * 100)
    print("    is_rigid short-circuits on a discrete colour refinement.  That shortcut is exactly")
    print("    the kind that is right on every poset anybody tries by hand and wrong on a class.")
    print()
    for n in range(2, NMAX_RIGID + 1):
        bad = sum(1 for down in C[n] if X.is_rigid(n, down) != brute_rigid(n, down))
        ok &= bad == 0
        print("      n=%d  %6d posets   disagreements: %d  %s"
              % (n, len(C[n]), bad, "OK" if bad == 0 else "FIRED"))
    print()

    # ------------------------------------------------------------------------------------------
    print("T5  THE FAMILY CONSTRUCTOR'S CLOSURE IS A POSET (transitive, antisymmetric, irreflexive)")
    print("-" * 100)
    bad = 0
    for n in range(15, 25):
        down = X.family(n)
        if len(down) != n:
            bad += 1
            continue
        for i in range(n):
            if down[i] >> i & 1:
                bad += 1
            for j in range(n):
                if (down[i] >> j & 1) and (down[j] >> i & 1):
                    bad += 1
                if (down[i] >> j & 1) and (down[j] & ~down[i]):
                    bad += 1                                        # transitivity
    ok &= bad == 0
    print("      F(n) for n = 15..24   axiom violations: %d   %s" % (bad, "OK" if bad == 0 else "FIRED"))
    print()

    # ------------------------------------------------------------------------------------------
    print("T6  WRONG-DIRECTION CONTROL 1 -- THE POPULATION WARNING, MEASURED HERE")
    print("-" * 100)
    print("    delta(P) < 1/3 STRICT is the frozen hypothesis.  If this instrument found one, the")
    print("    (1/3)-(2/3) conjecture would be false and that would be the finding rather than")
    print("    anything in this directory.  It finds none, and the zeros elsewhere in this")
    print("    directory are zeros IN AN EMPTY POPULATION for that reason and no other.")
    print()
    for n in range(2, NMAX_POP + 1):
        froz = bnd = 0
        for down in C[n]:
            le, dlt, _t = L.delta_at_most(n, down, bound=X.THIRD)
            if le:
                if dlt < X.THIRD:
                    froz += 1
                elif dlt == X.THIRD:
                    bnd += 1
        ok &= froz == 0
        print("      n=%d  %6d posets   frozen (delta<1/3): %d   boundary (delta=1/3): %3d   %s"
              % (n, len(C[n]), froz, bnd, "OK -- empty as expected" if froz == 0 else "FROZEN POSET FOUND"))
    print()

    # ------------------------------------------------------------------------------------------
    print("T7  WRONG-DIRECTION CONTROL 2 -- THE MACHINERY MUST BE ABLE TO RETURN A YES")
    print("-" * 100)
    print("    Same question, non-empty class: max{ d(P) : delta(P) < 1/2 }, the PSEUDO-FROZEN")
    print("    population.  A number strictly below 1 here is this instrument producing exactly")
    print("    the shape of statement it reports as unavailable for the real hypothesis --")
    print("    which is what makes that report a measurement and not a limitation of the tool.")
    print()
    half = Fraction(1, 2)
    yes = True
    for n in range(3, 8):
        best = Fraction(-1)
        pop = 0
        for down in C[n]:
            if not L.incomparable_pairs(n, down):
                continue
            le, dlt, _t = L.delta_at_most(n, down, bound=half)
            if le and dlt < half:
                pop += 1
                best = max(best, X.density(n, down))
        strict = best < 1
        yes &= strict and pop > 0
        print("      n=%d  population %6d   max d = %-7s (%.4f)  %s"
              % (n, pop, best, float(best), "CEILING < 1" if strict else "NO CEILING"))
    ok &= yes
    print()
    print("      %s" % ("OK -- a real density ceiling on a real population, so a NO elsewhere in"
                        if yes else "FIRED -- the machinery cannot exhibit a ceiling even where one exists;"))
    print("      %s" % ("      this directory is a fact about the hypothesis, not about the tool."
                        if yes else "      every NO in this directory would be unfalsifiable."))
    print()

    print("=" * 100)
    print("VERDICT: %s" % ("GREEN" if ok else "RED -- a control fired"))
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
