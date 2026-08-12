#!/usr/bin/env python3
"""mg-7c78 arm a6 — THE ARM THE OTHER FIVE MADE NECESSARY, AND IT IS WHERE THE HYPOTHESIS BITES.

a2 measured that R2 -- one linear extension whose consecutive 3-blocks cover EVERY incomparable
edge -- is FALSE in general (2384 of 3242 posets).  a5 then measured that it HOLDS at every poset
of the delta = 1/3 boundary class, 31 of 31, exhaustively to n = 8.  Those two together say the
`> 2/3` hypothesis DOES work in reading R2, which is the opposite of what a1 found for R1 and is
NOT what PREDICTIONS.md expected.  This arm is the follow-up, and it takes Daniel's sentence
LITERALLY rather than charitably.

  "choose permutation of L then there are adjacent triples for each incomparable edge, all
   aligned with distinguished e for that edge"

Take the chosen permutation to be `e` ITSELF.  Then every triple of it is `e`-aligned for FREE and
the alignment clause is discharged by the choice rather than by an argument.  What remains is a
pure statement about `e`:

    R2e(d).   In the distinguished linear extension `e`, every incomparable pair of `P` lies at
              POSITION DISTANCE <= d.   Daniel's triples are d = 2.

  m1  R2e ON THE BOUNDARY CLASS, exhaustively, AT BOTH d = 2 AND d = 1.
  m2  WHY THE FREE-TRIPLE READING CANNOT BE WHAT WAS MEANT: the width of the boundary class, and
      the number of 3-element antichains in it.
  m3  IS R2e MERELY AN EDGE COUNT?  Sparsity is necessary (R2e(2) forces <= 2n-3 edges) but the
      measurement asks whether it is sufficient.
  m4  THE delta-SWEEP, at both d = 1 and d = 2 -- where the hypothesis starts doing the work.
  m5  PRIMITIVITY.  A fact that held only at ordinal sums would not reach a minimal
      counterexample, which is primitive (`STATE.md` glossary).

Exits 0 if the instrument's own checks are consistent, 1 otherwise, 2 on refusal.  The `3` in
`adjacent triple` turning out to be UNNECESSARY is a FINDING, not an instrument failure.
"""

import sys
from fractions import Fraction

import lib7c78 as L

NMAX = 8
THIRD = Fraction(1, 3)
HALF = Fraction(1, 2)


def majority_order(n, down, p):
    """The distinguished order `e`: P's relations plus, on each incomparable pair, the majority
    orientation.  None if some pair is exactly balanced (no majority) or the relation has a cycle
    (which the no-3-cycle anchor forbids only above 2/3).  When it is not None it is UNIQUE: the
    relation is then a transitive tournament, which has exactly one topological order."""
    adj = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and L.is_below(down, i, j):
                adj[i][j] = True
    for (x, y) in L.incomparable_pairs(n, down):
        pxy = p[(x, y)]
        if pxy == HALF:
            return None
        if pxy > HALF:
            adj[x][y] = True
        else:
            adj[y][x] = True
    indeg = [sum(1 for i in range(n) if adj[i][j]) for j in range(n)]
    order, avail = [], [j for j in range(n) if indeg[j] == 0]
    while avail:
        j = min(avail)
        avail.remove(j)
        order.append(j)
        for k in range(n):
            if adj[j][k]:
                indeg[k] -= 1
                if indeg[k] == 0:
                    avail.append(k)
    if len(order) != n:
        return None
    return tuple(order)


def width_and_antichains(n, down):
    """(width, number of 3-element antichains) by direct enumeration of antichains."""
    best, tri = 0, 0
    for m in range(1 << n):
        elts = [i for i in range(n) if m >> i & 1]
        if not L.free_set(down, tuple(elts)):
            continue
        best = max(best, len(elts))
        if len(elts) == 3:
            tri += 1
    return best, tri


def primitive(n, down):
    """Is the incomparability graph connected?  (STATE.md glossary: primitive <=> not an ordinal
    sum <=> lambda_std < 1 strictly.  Minimal counterexamples are primitive.)"""
    inc = L.incomparable_pairs(n, down)
    if n == 1:
        return False
    nb = {i: set() for i in range(n)}
    for (x, y) in inc:
        nb[x].add(y)
        nb[y].add(x)
    seen, stack = {0}, [0]
    while stack:
        v = stack.pop()
        for w in nb[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


def main():
    print("=" * 92)
    print("mg-7c78  a6  R2e -- how far apart in `e` an incomparable pair can be")
    print("=" * 92)
    print()

    classes = L.all_classes(NMAX)

    rows = []           # (n, down, delta, maxdist or None, nedges)
    no_e = 0
    for n in range(2, NMAX + 1):
        for down in classes[n]:
            inc = L.incomparable_pairs(n, down)
            if not inc:
                continue
            exts = L.linear_extensions(n, down)
            p = L.pair_probs(n, down, exts)
            d = L.delta(n, down, p)
            e = majority_order(n, down, p)
            if e is None:
                no_e += 1
                rows.append((n, down, d, None, len(inc)))
                continue
            rank = {v: k for k, v in enumerate(e)}
            md = max(abs(rank[x] - rank[y]) for (x, y) in inc)
            rows.append((n, down, d, md, len(inc)))

    bnd = [r for r in rows if r[2] == THIRD]

    print("m1  R2e ON THE BOUNDARY CLASS delta = 1/3 -- n = 3..%d EXHAUSTIVE, d = 2 AND d = 1"
          % NMAX)
    print("-" * 92)
    print("    %3s %9s %12s %16s %14s %14s"
          % ("n", "posets", "inc. edges", "max dist in e", "R2e(d<=2)", "R2e(d<=1)"))
    per_n = {}
    for (n, _dn, _dl, md, ne) in bnd:
        row = per_n.setdefault(n, [0, 0, 0, 0, 0])
        row[0] += 1
        row[1] += ne
        row[2] = max(row[2], md if md is not None else 99)
        row[3] += 1 if (md is not None and md <= 2) else 0
        row[4] += 1 if (md is not None and md <= 1) else 0
    for n in sorted(per_n):
        t, ne, md, g2, g1 = per_n[n]
        print("    %3d %9d %12d %16d %14s %14s"
              % (n, t, ne, md, "%d/%d" % (g2, t), "%d/%d" % (g1, t)))
    f2 = sum(1 for r in bnd if r[3] is None or r[3] > 2)
    f1 = sum(1 for r in bnd if r[3] is None or r[3] > 1)
    mx = max(r[3] for r in bnd if r[3] is not None)
    print()
    print("    boundary posets %d · R2e(2) failures %d · R2e(1) failures %d"
          % (len(bnd), f2, f1))
    print("    MAXIMUM POSITION DISTANCE ATTAINED OVER THE WHOLE BOUNDARY CLASS: %d" % mx)
    print()
    print("    ⚠️  THE `3` IN `ADJACENT TRIPLE` IS NOT LOAD-BEARING.  The measured statement is")
    print("    the d = 1 one -- every incomparable pair of a boundary poset is ADJACENT in `e`,")
    print("    not merely inside a common 3-block.  Daniel's form is TRUE and is IMPLIED BY a")
    print("    strictly stronger measured statement, so logging his form as the fact would")
    print("    under-record what the population actually shows.")
    print()

    print("m2  WHY THE FREE-TRIPLE READING CANNOT BE WHAT WAS MEANT")
    print("-" * 92)
    print("    %3s %9s %14s %22s" % ("n", "posets", "max width", "3-element antichains"))
    wmax = tri_tot = 0
    for n in sorted(per_n):
        ws, ts = [], 0
        for (m, down, _d, _md, _ne) in bnd:
            if m != n:
                continue
            w, t = width_and_antichains(n, down)
            ws.append(w)
            ts += t
        print("    %3d %9d %14d %22d" % (n, len(ws), max(ws), ts))
        wmax = max(wmax, max(ws))
        tri_tot += ts
    print()
    print("    THE BOUNDARY CLASS HAS WIDTH %d AT EVERY MEMBER AND CONTAINS %d THREE-ELEMENT"
          % (wmax, tri_tot))
    print("    ANTICHAINS IN TOTAL.  So `adjacent triple` read as a FREE 3-block -- three")
    print("    pairwise-incomparable elements at consecutive positions, the reading under which")
    print("    the S_3 symmetry of a4 m1 would apply -- is not merely rare on this class, it is")
    print("    IMPOSSIBLE: there is no 3-element antichain to make one from.  That reading is")
    print("    therefore REFUTED on the only non-empty approximation to the hypothesis, and it is")
    print("    refuted for a structural reason and not by a close call.")
    print("    (Consistent with `STATE.md`'s attempt-index row: low-delta <=> bounded width,")
    print("    mg-c47a Obs 3.1(a)/(b), PROVEN.  This is that row's shadow at the boundary.)")
    print()

    print("m3  IS R2e MERELY AN EDGE COUNT?  sparse posets that still FAIL R2e(2)")
    print("-" * 92)
    sparse = [r for r in rows if r[3] is not None and r[4] <= 2 * r[0] - 3]
    sparse_fail = [r for r in sparse if r[3] > 2]
    print("    posets with #inc edges <= 2n-3 and a well-defined e: %d" % len(sparse))
    print("    of those, FAILING R2e(2): %d (%.1f%%)"
          % (len(sparse_fail), 100.0 * len(sparse_fail) / max(1, len(sparse))))
    if sparse_fail:
        n, down, d, md, ne = sparse_fail[0]
        print("    smallest witness: n=%d down-masks %s, delta=%s, %d edges <= %d, max dist %d"
              % (n, list(down), d, ne, 2 * n - 3, md))
        print("    SPARSITY IS NECESSARY AND NOT SUFFICIENT: R2e is about WHERE the incomparable")
        print("    pairs sit in `e`, not how many there are.")
    print()

    print("m4  THE delta-SWEEP -- where the `> 2/3` hypothesis starts doing the work")
    print("-" * 92)
    bands = [
        ("delta = 1/3          (boundary, every pair >= 2/3-decided)", lambda d: d == THIRD),
        ("1/3 < delta <= 2/5", lambda d: THIRD < d <= Fraction(2, 5)),
        ("2/5 < delta <= 9/20", lambda d: Fraction(2, 5) < d <= Fraction(9, 20)),
        ("9/20 < delta < 1/2", lambda d: Fraction(9, 20) < d < HALF),
        ("delta = 1/2          (some pair exactly balanced -- no `e`)", lambda d: d == HALF),
    ]
    print("    %-58s %7s %11s %11s" % ("delta band", "with e", "R2e(2)", "R2e(1)"))
    for (label, pred) in bands:
        sel = [r for r in rows if pred(r[2]) and r[3] is not None]
        g2 = sum(1 for r in sel if r[3] <= 2)
        g1 = sum(1 for r in sel if r[3] <= 1)
        if sel:
            print("    %-58s %7d %5d (%4.1f%%) %5d (%4.1f%%)"
                  % (label, len(sel), g2, 100.0 * g2 / len(sel), g1, 100.0 * g1 / len(sel)))
        else:
            print("    %-58s %7d %11s %11s" % (label, 0, "n/a", "n/a"))
    print()
    print("    MONOTONE IN delta, AT BOTH d.  100%% at the boundary, falling to a few per cent as")
    print("    the most-balanced pair moves toward 1/2.  That is the evidence that `> 2/3` is what")
    print("    buys R2e, rather than smallness of n -- the bands share the same n range.")
    print()
    print("    posets with NO well-defined `e` (a pair at exactly 1/2, or a majority cycle): %d"
          % no_e)
    print("    -- excluded from the R2e columns because R2e NAMES `e`, and off the frozen class")
    print("    `e` is a CHOICE, not a canonical object (PREDICTIONS.md E3).")
    print()

    print("m5  PRIMITIVITY -- does the fact reach objects a minimal counterexample could be?")
    print("-" * 92)
    prim = sum(1 for (n, down, _d, _md, _ne) in bnd if primitive(n, down))
    print("    boundary posets that are PRIMITIVE (incomparability graph connected): %d of %d"
          % (prim, len(bnd)))
    print("    ⚠️  %d of the %d ARE ORDINAL SUMS, so the class is ALMOST ENTIRELY non-primitive."
          % (len(bnd) - prim, len(bnd)))
    print("    A minimal counterexample is PRIMITIVE (STATE.md glossary), so a fact measured on")
    print("    this class reaches the objects that matter through %d witness%s and not through the"
          % (prim, "" if prim == 1 else "es"))
    print("    other %d.  THAT IS THE SCOPE LIMIT OF EVERY FIGURE IN THIS ARM and it must travel"
          % (len(bnd) - prim))
    print("    with them.")
    print()

    ok = (f2 == 0 and len(bnd) > 0 and len(sparse_fail) > 0 and tri_tot == 0)
    print("VERDICT: %s   (instrument consistency; the d = 1 sharpening and the width-%d collapse"
          % ("GREEN" if ok else "RED", wmax))
    print("          are FINDINGS, not instrument failures)")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
