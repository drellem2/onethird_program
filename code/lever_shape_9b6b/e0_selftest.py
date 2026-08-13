#!/usr/bin/env python3
"""mg-9b6b arm e0 — CONTROLS, AND THE TWO THAT RUN THE WRONG WAY ARE THE POINT.

Every number in this directory is downstream of four things: the enumerator, `δ`, `d`, and the
`(1_D)`/`(2_D)` predicates.  An import whose controls live in another directory is UNCHECKED FROM
HERE, so `lib6ff4` and `lib0b96` are re-checked against things that are not themselves:

  T1  the enumerator against OEIS A000112
  T2  `d_provable` — F26's `⌈(n−1)/2⌉` against the negative-floor spelling, and against F26's own
      published sharpness table
  T3  `δ` against BRUTE-FORCE enumeration of `L(P)`, every isomorphism class at `n ≤ 6`
  T4  `δ` and `d` against a hand-built table of five posets whose values are computable by eye
  T5  two PLANTED defects, each re-running the same `delta_exact` the verdicts come from

and two WRONG-DIRECTION controls, which are the ones that make the later NOs falsifiable:

  T6  THE POPULATION WARNING.  The frozen class is EMPTY at every `n ≤ 8` (P2).  Every "no
      counterexample" in `e1` and `e3` at `β = 1/3` is a zero over an empty population and this
      arm establishes that BEFORE any of them is printed.
  T7  THE MUST-FIRE CONTROL.  At `β = 2/5` the class is NOT empty, and the same machinery must
      return a real ceiling AND fire on explicit counterexamples below it.  If T7 cannot make this
      instrument say NO, then nothing it says YES to is falsifiable by this suite (P9).

EXIT 1 IF ANY CONTROL FAILS.  A green suite whose controls were never checked is the failure mode
this estate names most often, so the status is read from the arm and not from the last line.
"""

import sys
from fractions import Fraction

import lib9b6b as Y
import lib6ff4 as L


def rule(t):
    print("-" * 100)
    print(t)


def head(t):
    print("=" * 100)
    print(t)
    print("=" * 100)


FAIL = []


def check(tag, ok, detail=""):
    print("    %-6s %-7s %s" % (tag, "ok" if ok else "FAILED", detail))
    if not ok:
        FAIL.append(tag)


def main():
    head("mg-9b6b  e0  controls — and the two wrong-direction ones are the point")
    classes = L.all_classes(8)

    # ------------------------------------------------------------------ T1
    rule("T1  THE ENUMERATOR, AGAINST OEIS A000112 — an import checked against something that is "
         "not itself")
    for n in range(1, 9):
        got, want = len(classes[n]), L.A000112[n]
        check("T1.%d" % n, got == want, "n=%d  %6d classes   A000112 = %d" % (n, got, want))

    # ------------------------------------------------------------------ T2
    rule("T2  F26's CEILING — two spellings of `⌈(n−1)/2⌉`, and the published sharpness values")
    for n in range(2, 12):
        a = Y.d_provable(n)
        b = 1 - Fraction(-((1 - n) // 2), n * (n - 1) // 2)
        check("T2.%d" % n, a == b, "n=%2d  d_provable = %-8s  negative-floor spelling = %s"
              % (n, a, b))
    print()
    print("    F26 is `d <= 1 - ceil((n-1)/2)/C(n,2)`, docs/FACTS.md F26, kind U.  At the three")
    print("    orders mg-0b96 tabulated it, eps_sup = d*n/(n+1) must reproduce ITS figures:")
    for n, want in ((15, "0.8750"), (99, "0.9800"), (300, "0.9933")):
        got = float(Y.eps_sup(n, Y.d_provable(n)))
        check("T2.e%d" % n, "%.4f" % got == want,
              "n=%3d  eps_sup at F26's ceiling = %.4f   mg-0b96 d4 table says %s" % (n, got, want))

    # ------------------------------------------------------------------ T3
    rule("T3  `δ` AGAINST BRUTE FORCE — every class at n <= 6, delta from enumerated L(P)")
    bad = 0
    tested = 0
    for n in range(2, 7):
        for down in classes[n]:
            inc = L.incomparable_pairs(n, down)
            if not inc:
                continue
            exts = L.linear_extensions(n, down)
            tot = len(exts)
            best = Fraction(0)
            for (i, j) in inc:
                cnt = sum(1 for e in exts if e.index(i) < e.index(j))
                p = Fraction(cnt, tot)
                best = max(best, min(p, 1 - p))
            tested += 1
            if best != Y.delta_exact(n, down):
                bad += 1
    check("T3", bad == 0, "%d non-chain classes at n <= 6, %d disagreements between the DP and a "
          "full enumeration of L(P)" % (tested, bad))

    # ------------------------------------------------------------------ T4
    rule("T4  A HAND-BUILT TABLE — five posets whose `δ` and `d` are computable by eye")
    # down[i] = bitmask of elements strictly below i
    hand = [
        ("antichain n=3", 3, (0, 0, 0), Fraction(1, 2), Fraction(1)),
        ("chain n=3", 3, (0, 1, 3), None, Fraction(0)),
        ("a<b, c free", 3, (0, 1, 0), Fraction(1, 3), Fraction(2, 3)),
        ("antichain n=4", 4, (0, 0, 0, 0), Fraction(1, 2), Fraction(1)),
        ("V: a<b, a<c", 3, (0, 1, 1), Fraction(1, 2), Fraction(1, 3)),
    ]
    for name, n, down, wd, wdens in hand:
        gd = Y.delta_exact(n, down)
        gden = Y.density(n, down)
        check("T4", gd == wd and gden == wdens,
              "%-14s delta = %-6s (want %-6s)   d = %-5s (want %s)"
              % (name, gd, wd, gden, wdens))
    print()
    print("    `a<b, c free` is the poset that carries the whole programme's threshold: its three")
    print("    linear extensions put BOTH incomparable pairs at exactly 1/3, so delta = 1/3 and it")
    print("    is NOT frozen -- frozen is delta < 1/3, STRICT.  The V is the check in the other")
    print("    direction: an automorphism swapping b and c forces p = 1/2, which is F26's clause")
    print("    (A) on a poset small enough to verify by hand.")

    # ------------------------------------------------------------------ T5
    rule("T5  PLANTED DEFECTS — each re-runs the same `delta_exact` the verdicts come from")

    def planted_min(n, down):
        """PLANT 1: `min` where the definition says `max` over incomparable pairs."""
        inc = L.incomparable_pairs(n, down)
        if not inc:
            return None
        tot = L.count_ext(n, down)
        vals = [min(p, 1 - p) for p in
                (L.p_before(n, down, i, j, tot) for (i, j) in inc)]
        return min(vals)

    def planted_nomin(n, down):
        """PLANT 2: `p` where the definition says `min(p, 1−p)` -- drops the balance folding."""
        inc = L.incomparable_pairs(n, down)
        if not inc:
            return None
        tot = L.count_ext(n, down)
        return max(L.p_before(n, down, i, j, tot) for (i, j) in inc)

    for tag, fn, why in (("T5.1", planted_min, "max -> min over incomparable pairs"),
                         ("T5.2", planted_nomin, "min(p,1-p) -> p, the balance folding dropped")):
        caught = 0
        seen = 0
        for down in classes[6]:
            if not L.incomparable_pairs(6, down):
                continue
            seen += 1
            if fn(6, down) != Y.delta_exact(6, down):
                caught += 1
        check(tag, caught > 0, "%s: differs on %d of %d non-chain classes at n = 6" %
              (why, caught, seen))
    print()
    print("    Both plants are LIVE -- each changes an answer this directory reads.  A plant that")
    print("    came back inert would be printed here rather than swapped out, because a defect the")
    print("    domain cannot express says nothing about the control's power (mg-3da1's finding).")

    # ------------------------------------------------------------------ T6
    rule("T6  WRONG DIRECTION 1 -- THE POPULATION WARNING.  Is the frozen class empty?")
    print("    Every zero this directory prints at beta = 1/3 is a zero over THIS population, and")
    print("    it is established before any of them rather than cited after.")
    print()
    print("      %3s  %8s  %9s  %s" % ("n", "classes", "non-chain", "frozen (delta < 1/3)"))
    tot_frozen = 0
    for n in range(2, 9):
        rows = [(Y.density(n, d), Y.delta_exact(n, d)) for d in classes[n]]
        nonchain = [r for r in rows if r[1] is not None]
        frozen = [r for r in nonchain if r[1] < Y.THIRD]
        tot_frozen += len(frozen)
        print("      %3d  %8d  %9d  %d" % (n, len(classes[n]), len(nonchain), len(frozen)))
    check("T6", tot_frozen == 0,
          "0 frozen posets over every isomorphism class at n <= 8 -- a single member would REFUTE "
          "the (1/3)-(2/3) conjecture")

    # ------------------------------------------------------------------ T7
    rule("T7  WRONG DIRECTION 2 -- THE MUST-FIRE CONTROL at beta = 2/5, where the class is NOT "
         "empty")
    print("    If this instrument cannot be made to say NO, nothing it says YES to is falsifiable")
    print("    by this suite.  Same `one_D`, same `two_D`, same population -- only beta moves.")
    print()
    beta = Fraction(2, 5)
    print("      %3s  %10s  %10s  %-10s %s"
          % ("n", "|delta<2/5|", "max d", "(1_D) at D", "verdict"))
    fired = 0
    real_ceiling = 0
    for n in range(3, 8):
        rows = [(Y.density(n, d), Y.delta_exact(n, d)) for d in classes[n]]
        rows = [r for r in rows if r[1] is not None]
        members, mx = Y.ceiling_at(rows, beta, strict=True)             # delta < 2/5, STRICT
        if mx is None:
            print("      %3d  %10d  %10s  %-10s %s" % (n, members, "EMPTY", "-", "no subject"))
            continue
        if mx < 1:
            real_ceiling += 1
        D = mx - Fraction(1, n * (n - 1) // 2)          # one quantum BELOW the true ceiling
        _, ce = Y.one_D(rows, D, beta)
        if ce:
            fired += 1
        print("      %3d  %10d  %10s  %-10s %s"
              % (n, members, mx, D, "FIRED on %d counterexample(s)" % len(ce) if ce else "silent"))
    check("T7.a", real_ceiling == 5, "a ceiling strictly below 1 at every n = 3..7 -- the machinery "
          "returns a real answer when the class is non-empty")
    check("T7.b", fired == 5, "and FIRES at every n = 3..7 when the ceiling is set one density "
          "quantum too low")

    rule("VERDICT")
    if FAIL:
        print("    RED -- %d control(s) failed: %s" % (len(FAIL), ", ".join(FAIL)))
        return 1
    print("    GREEN -- every control passed, including both wrong-direction ones.")
    print()
    print("    WHAT THIS ARM DOES NOT ESTABLISH, said here so no later arm is read as having it:")
    print("    T6 is the (1/3)-(2/3) conjecture at n <= 8 and nothing more.  It is kind FP and it")
    print("    says NOTHING about n = 9 or above.  The whole subject of e2 is that this emptiness")
    print("    is a property of the HYPOTHESIS and not a limitation of the enumerator.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
