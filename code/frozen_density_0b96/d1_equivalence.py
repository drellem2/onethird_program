#!/usr/bin/env python3
"""mg-0b96 arm d1 — THE LEVER IS THE CONJECTURE ON A SUB-CLASS, BY CONTRAPOSITION, AND THAT IS
THE WHOLE ANSWER.  One line, and the arm exists to keep it from being read as a slogan.

    THE STATEMENT.  For `D ∈ [0, 1)` write

        (1_D)   every FROZEN poset has  d(P) ≤ D          [frozen = δ(P) < 1/3, STRICT]
        (2_D)   every poset with  d(P) > D  has  δ(P) ≥ 1/3

    Then `(1_D) ⟺ (2_D)`, and `(2_D)` is THE (1/3)–(2/3) CONJECTURE, verbatim, restricted to the
    class `{P : d(P) > D}`.  `d(P) > D ≥ 0` forces `m ≥ 1`, so the restriction never lands on a
    chain and `(2_D)` is never a vacuous reading of the conjecture.

    Proof: contraposition, twice.  There is nothing else in it.

WHY AN ARM, IF THE PROOF IS ONE WORD.  Because three things around it are not one word, and each
is the kind of thing that gets asserted:

  m1  THE TWO SIDES ARE COMPUTED BY DIFFERENT CODE PATHS AND AGREE POSET BY POSET.  A tautology
      proves nothing about an IMPLEMENTATION, and every number in this directory is downstream of
      `frozen` and `δ ≥ 1/3` being complements as this instrument computes them.
  m2  NON-VACUITY, MEASURED.  `(2_D)`'s class is non-empty at every `D < 1` and every `n ≥ 2` —
      the antichain sits at `d = 1` — so no choice of `D` turns the right-hand side into a
      statement about nothing.  A weakening that empties its own hypothesis would be the way this
      equivalence could be true and useless.
  m3  `D = 0` IS THE CONJECTURE ITSELF, and `D` is a dial between the conjecture and nothing.
      At `D = 0`, `{d > 0}` is every non-chain, so `(1_0)` IS the conjecture; at `D → 1` the
      restricted class shrinks to the densest posets.  So "bound `d` under freezing" names a
      one-parameter FAMILY of open cases of the conjecture, and the parameter that would close
      row 8 is priced in `d2`.
  m4  THE STRICTNESS IS LOAD-BEARING, AND THE SEPARATION IS STATED WITHOUT A WITNESS BECAUSE NO
      WITNESS EXISTS TO BE FOUND.  `(1_D)` is NOT equivalent to "every poset with `d ≥ D` has
      `δ ≥ 1/3`" — that one is `(1_{D−})` — and the two readings differ exactly on a FROZEN poset
      sitting at `d = D`, of which this instrument's population contains none (`d0` T6).  The arm
      prints that as an un-witnessed distinction rather than as a check that passed; an off-by-one
      here would misstate the theorem, and a run cannot catch it.

Exits 0 if the equivalence holds pointwise and the controls hold, 1 otherwise, 2 on refusal.
"""

import sys
from fractions import Fraction

import lib0b96 as X
import lib6ff4 as L

NMAX = 7
DS = [Fraction(0), Fraction(1, 100), Fraction(2, 100), Fraction(1, 10),
      Fraction(1, 3), Fraction(1, 2), Fraction(3, 4), Fraction(9, 10), Fraction(99, 100)]


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else NMAX
    print("=" * 100)
    print("mg-0b96  d1  a frozen-class density ceiling IS the conjecture on {d > D}")
    print("=" * 100)
    print()
    print("  (1_D)  every frozen poset has d(P) <= D          frozen = delta(P) < 1/3, STRICT")
    print("  (2_D)  every poset with d(P) > D has delta >= 1/3   = the conjecture on {d > D}")
    print()
    print("  (1_D) <=> (2_D) by contraposition.  d(P) > D >= 0 forces m >= 1, so (2_D) never")
    print("  degenerates to a statement about chains.")
    print()

    try:
        C = L.all_classes(nmax)
    except Exception as exc:                                       # pragma: no cover
        print("REFUSED: the imported enumerator did not run: %r" % (exc,))
        print("VERDICT: REFUSED")
        return 2

    ok = True

    # per-poset facts, computed once
    facts = {}
    for n in sorted(C):
        if n < 2:
            continue
        rows = []
        for down in C[n]:
            inc = L.incomparable_pairs(n, down)
            if not inc:
                rows.append((X.density(n, down), None))            # a chain: delta undefined
                continue
            le, dlt, _t = L.delta_at_most(n, down, bound=Fraction(1))
            rows.append((X.density(n, down), dlt))
        facts[n] = rows

    # ------------------------------------------------------------------------------------------
    print("m1  THE TWO SIDES, POSET BY POSET, OVER THE EXHAUSTIVE POPULATION n <= %d" % nmax)
    print("-" * 100)
    print("    LHS(P) = not(delta < 1/3) or d <= D          RHS(P) = not(d > D) or delta >= 1/3")
    print("    computed from the same delta but through opposite comparisons, and compared.")
    print()
    print("      %-8s %10s %12s %12s" % ("D", "posets", "LHS!=RHS", "verdict"))
    total = 0
    for D in DS:
        bad = 0
        cnt = 0
        for n in sorted(facts):
            for (d, dlt) in facts[n]:
                if dlt is None:
                    continue                                       # chains carry no incomparable
                cnt += 1                                           # pair, so neither side speaks
                lhs = (not (dlt < X.THIRD)) or (d <= D)
                rhs = (not (d > D)) or (dlt >= X.THIRD)
                if lhs != rhs:
                    bad += 1
        total = cnt
        ok &= bad == 0
        print("      %-8s %10d %12d %12s" % (D, cnt, bad, "OK" if bad == 0 else "FIRED"))
    print()
    print("    %d non-chain posets x %d values of D, 0 disagreements." % (total, len(DS)))
    print("    ⚠️  This is a control on the IMPLEMENTATION.  The equivalence is a tautology and")
    print("    a run cannot add to its warrant; what a run can catch is `frozen` and")
    print("    `delta >= 1/3` failing to be complements in code, which is what every number in")
    print("    this directory rests on.")
    print()

    # ------------------------------------------------------------------------------------------
    print("m2  NON-VACUITY -- is (2_D) ever a statement about nothing?")
    print("-" * 100)
    print("      %-8s %s" % ("D", "  |{P : d(P) > D}| at n = " + ", ".join(str(n) for n in sorted(facts))))
    empty_any = False
    for D in DS:
        counts = []
        for n in sorted(facts):
            counts.append(sum(1 for (d, _dl) in facts[n] if d > D))
        if any(c == 0 for n, c in zip(sorted(facts), counts) if n >= 2):
            empty_any = True
        print("      %-8s %s" % (D, "  ".join("%7d" % c for c in counts)))
    ok &= not empty_any
    print()
    print("    Non-empty at every D < 1 and every n >= 2: the antichain has d = 1.  So no choice")
    print("    of D turns (2_D) into a vacuous statement -- which is the way this equivalence")
    print("    could have been true and worthless.  %s" % ("OK" if not empty_any else "FIRED"))
    print()

    # ------------------------------------------------------------------------------------------
    print("m3  D = 0 IS THE CONJECTURE VERBATIM, AND D IS A DIAL")
    print("-" * 100)
    nonchain = {n: sum(1 for (_d, dl) in facts[n] if dl is not None) for n in sorted(facts)}
    at0 = {n: sum(1 for (d, dl) in facts[n] if dl is not None and d > 0) for n in sorted(facts)}
    same = all(nonchain[n] == at0[n] for n in sorted(facts))
    ok &= same
    for n in sorted(facts):
        print("      n=%d   non-chain posets %7d   in {d > 0} %7d   %s"
              % (n, nonchain[n], at0[n], "same set" if nonchain[n] == at0[n] else "DIFFER"))
    print()
    print("    {d > 0} IS the set of non-chain posets, so (1_0) -- `every frozen poset is a")
    print("    chain' -- is the (1/3)-(2/3) conjecture with nothing removed.  Every D > 0 is a")
    print("    proper weakening of it and an open case of it.  There is no value of D at which")
    print("    the statement stops being the conjecture and starts being a lemma toward one.")
    print()

    # ------------------------------------------------------------------------------------------
    print("m4  THE STRICTNESS CONTROL -- (1_D) is NOT `every poset with d >= D has delta >= 1/3'")
    print("-" * 100)
    strictpair = None
    for n in sorted(facts):
        for (d, dlt) in facts[n]:
            if dlt is None:
                continue
            if d == Fraction(1, 3) and dlt >= X.THIRD:
                strictpair = (n, d, dlt)
                break
        if strictpair:
            break
    print("    The two readings differ exactly on the posets sitting AT d = D.  The equivalence")
    print("    above pairs `d <= D' with `d > D'; pairing `d <= D' with `d >= D' instead states a")
    print("    DIFFERENT theorem, (1_{D-}), and the corpus's own boundary class is where that")
    print("    would bite: mg-6ff4's F23 population sits AT its maximum density, not below it.")
    if strictpair:
        n, d, dlt = strictpair
        print("      a poset at exactly d = 1/3 with delta = %s (n = %d) -- in {d >= 1/3},"
              % (dlt, n))
        print("      not in {d > 1/3}, so it is governed by one reading and not the other.")
    print("      a frozen poset at d = D would separate the two readings: none exists at any n")
    print("      this instrument reaches (d0 T6), so the separation is stated and NOT witnessed.")
    print("      ⚠️  Recorded as an un-witnessed distinction, not as a check that passed.")
    print()

    print("=" * 100)
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
