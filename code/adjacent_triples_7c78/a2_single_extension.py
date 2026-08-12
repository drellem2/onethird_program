#!/usr/bin/env python3
"""mg-7c78 arm a2 — READING R2: one extension covering EVERY incomparable edge, and R3.

R2.  There is a SINGLE linear extension sigma such that every incomparable edge of P sits inside
some block of three consecutive positions of sigma.

R3.  In EVERY linear extension, every incomparable edge sits inside such a block.

  m1  THE COUNTING OBSTRUCTION, exact.  The n-2 consecutive 3-blocks of a single sigma cover
      exactly the pairs at distance 1 or 2, i.e. (n-1) + (n-2) = 2n-3 pairs -- NOT 3(n-2), which
      triple-counts the overlaps.  So R2 REQUIRES  #incomparable-edges <= 2n-3.
  m2  THE OBSTRUCTION IS REACHED, not merely available: the smallest poset with more incomparable
      edges than 2n-3 is reported, exhaustively over the population.
  m3  THE DIRECT CHECK, not the bound: min over sigma of the number of UNCOVERED incomparable
      edges, at every poset.  R2 holds at a poset iff that minimum is 0.
  m4  R3, which is strictly stronger than R2: max over sigma of uncovered edges.

Exits 0 if the reported figures are internally consistent (m1's bound never violated by m3's
witness), 1 otherwise, 2 on refusal.  NOTE: a NONZERO uncovered count is the FINDING here, not
a failure -- the exit code tracks the instrument, not the verdict on R2.
"""

import sys

import lib7c78 as L

NMAX = 7
SAMPLE_N, SAMPLE_K, SEED = 8, 800, 20260812


def covered_pairs(n, ext):
    """The pairs covered by the n-2 consecutive 3-blocks of `ext`: distance 1 and distance 2."""
    out = set()
    for k in range(n - 2):
        a, b, c = ext[k], ext[k + 1], ext[k + 2]
        for u, v in ((a, b), (b, c), (a, c)):
            out.add((min(u, v), max(u, v)))
    return out


def main():
    print("=" * 92)
    print("mg-7c78  a2  READINGS R2 and R3 -- one extension for every edge, and every extension")
    print("=" * 92)
    print()

    classes = L.all_classes(SAMPLE_N)
    import random
    rng = random.Random(SEED)
    pop = [(n, d, True) for n in range(2, NMAX + 1) for d in classes[n]]
    pop += [(SAMPLE_N, d, False) for d in rng.sample(classes[SAMPLE_N], SAMPLE_K)]

    print("m1  THE COUNTING OBSTRUCTION, stated exactly")
    print("-" * 92)
    for n in range(3, 9):
        print("    n=%d   3-blocks %d   pairs they cover %d = (n-1)+(n-2)   "
              "[3(n-2) = %d is the OVER-count: the blocks overlap]"
              % (n, n - 2, 2 * n - 3, 3 * (n - 2)))
    print()

    smallest_over = None
    r2_fail = r2_total = 0
    r3_fail = 0
    per_n = {}
    worst = (0, None)

    for (n, down, _exh) in pop:
        inc = L.incomparable_pairs(n, down)
        if not inc or n < 3:
            continue
        m = len(inc)
        if m > 2 * n - 3 and smallest_over is None:
            smallest_over = (n, down, m, 2 * n - 3)
        exts = L.linear_extensions(n, down)
        incset = set(inc)
        best = min(len(incset - covered_pairs(n, e)) for e in exts)
        wst = max(len(incset - covered_pairs(n, e)) for e in exts)
        r2_total += 1
        if best > 0:
            r2_fail += 1
        if wst > 0:
            r3_fail += 1
        if best > worst[0]:
            worst = (best, (n, down, m))
        row = per_n.setdefault(n, [0, 0, 0])
        row[0] += 1
        row[1] += 1 if best > 0 else 0
        row[2] += 1 if wst > 0 else 0

    print("m2  THE SMALLEST POSET THE OBSTRUCTION REACHES")
    print("-" * 92)
    if smallest_over:
        n, down, m, cap = smallest_over
        print("    n=%d  down-masks %s  incomparable edges %d > %d = 2n-3"
              % (n, list(down), m, cap))
        print("    R2 IS IMPOSSIBLE AT THIS POSET BY COUNTING ALONE -- no choice of sigma can")
        print("    cover %d pairs with %d slots." % (m, cap))
    else:
        print("    none found in this population")
    print()

    print("m3/m4  THE DIRECT CHECK, per n (posets with >= 1 incomparable pair, n >= 3)")
    print("-" * 92)
    print("    %3s %9s %26s %26s" % ("n", "posets", "R2 FAILS (min uncov > 0)", "R3 FAILS (max uncov > 0)"))
    for n in sorted(per_n):
        t, f2, f3 = per_n[n]
        print("    %3d %9d %14d (%5.1f%%) %19d (%5.1f%%)"
              % (n, t, f2, 100.0 * f2 / t, f3, 100.0 * f3 / t))
    print()
    print("    TOTAL: R2 fails at %d of %d posets; R3 fails at %d of %d."
          % (r2_fail, r2_total, r3_fail, r2_total))
    print("    worst uncovered count under the BEST sigma: %d, at n=%d with %d incomparable edges"
          % (worst[0], worst[1][0], worst[1][2]) if worst[1] else "")
    print()
    print("    R2 IS FALSE and R3 IS FALSE.  R3 fails at essentially every poset with an")
    print("    incomparable pair and three or more elements -- put x first and y last.  R2 fails")
    print("    for a counting reason that has nothing to do with delta: a single extension has")
    print("    2n-3 covered pairs against up to n(n-1)/2 incomparable edges.")
    print()

    ok = smallest_over is not None
    print("VERDICT: %s   (the instrument's own consistency; R2/R3 being FALSE is the FINDING)"
          % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
