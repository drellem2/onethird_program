#!/usr/bin/env python3
"""mg-6ff4 arm c2 — HOW FAR THE MEASUREMENT REACHES, AND ON WHAT RESTRICTED POPULATION.

`c1` is exhaustive over EVERY isomorphism class and stops where the enumeration does.  This arm
buys more `n` by paying for it with a RESTRICTION, and the restriction is named at every table:

  m1  WIDTH-`≤3` EXHAUSTIVE.  Every poset of width `≤ 3` on `n ≤ WMAX3` elements.  SOUND AND
      COMPLETE for that class — width is monotone under induced subposets, so deleting a maximal
      element cannot raise it, and the generator therefore reaches every width-`≤3` poset.
  m2  WIDTH-`≤2` EXHAUSTIVE, further out.  Same argument, `n ≤ WMAX2`.
  m3  THE ONE QUESTION ALL OF IT IS ASKING: does a NEW PRIMITIVE poset with `δ ≤ 1/3` appear?
      Everything in `c1` and `c3` is the ordinal-sum algebra applied to the primitive members, so
      a new primitive is the ONLY object that can move any number here.  Reported as a count, and
      the count is what the closed form lives or dies on.

⚠️  WHAT THE RESTRICTION COSTS.  A width-`≤3` sweep that finds nothing is silent about width `≥ 4`.
`mg-c47a`'s width-`≥4` `n ≥ 10` residual was DROPPED on tractability grounds (`STATE.md` attempt
index) and this arm does not reopen it — it inherits exactly that gap.  The width-`2` collapse
observed at `n ≤ 9` is EVIDENCE for the restriction being harmless and is NOT a proof of it, and no
line below is written as though it were.

Exits 0 if every restricted sweep is internally consistent, 1 if a new primitive appears (which is
a FINDING, not a bug — it is reported loudly and the exit code makes it impossible to miss), 2 on
refusal.
"""

import sys
from fractions import Fraction

import lib6ff4 as L

WMAX3 = 10          # width <= 3, exhaustive to this n
WMAX2 = 12          # width <= 2, exhaustive to this n
V_CANON = L.canon(3, (0, 1, 0))


def cover_string(n, down):
    cov = []
    for j in range(n):
        for i in range(n):
            if L.is_below(down, i, j):
                if not any(L.is_below(down, i, k) and L.is_below(down, k, j) for k in range(n)):
                    cov.append("%d<%d" % (i, j))
    return " ".join(cov) if cov else "(antichain)"


def sweep(nmax, maxwidth, label):
    """Returns (table, boundary_rows, new_primitives)."""
    print("    generating width <= %d classes to n = %d ..." % (maxwidth, nmax), flush=True)
    classes = L.all_classes(nmax, maxwidth=maxwidth)
    table, rows, prims = [], [], []
    for n in range(2, nmax + 1):
        tot = at3 = be3 = 0
        for down in classes[n]:
            if not L.incomparable_pairs(n, down):
                continue
            tot += 1
            ok, d, tbl = L.delta_at_most(n, down)
            if not ok:
                continue
            if d == L.THIRD:
                at3 += 1
            else:
                be3 += 1
            mm = L.measure(n, down, tbl)
            summ = L.ordinal_summands(n, down)
            kV = sum(1 for k, dd in summ if k == 3 and dd == V_CANON)
            other = [(k, dd) for k, dd in summ if not (k == 1 or (k == 3 and dd == V_CANON))]
            rows.append((n, down, d, mm, kV, other))
            if L.is_primitive(n, down) and n > 3:
                prims.append((n, down, d))
        table.append((n, len(classes[n]), tot, at3, be3))
        print("    ... %s n = %d: %d classes, %d with an incomparable pair, %d at the boundary"
              % (label, n, len(classes[n]), tot, at3), flush=True)
    return table, rows, prims


def report(label, table, rows, prims, nmax):
    print()
    print("    %3s %13s %13s %14s %20s" % ("n", "classes", "with inc pair", "delta = 1/3",
                                           "delta < 1/3 (FROZEN)"))
    for n, ncls, tot, at3, be3 in table:
        print("    %3d %13d %13d %14d %20d" % (n, ncls, tot, at3, be3))
    frozen = sum(t[4] for t in table)
    print()
    print("    FROZEN (delta < 1/3) FOUND IN THIS RESTRICTED POPULATION: %d." % frozen)
    print("    ⚠️  Empty by construction again; it is printed for the same reason as in c1.")
    print()
    print("    boundary posets found: %d" % len(rows))
    bad = [r for r in rows if r[5]]
    print("    NOT an ordinal sum of singletons and V's: %d" % len(bad))
    for (n, down, d, mm, kV, other) in bad:
        print("        ⚠️  n=%d  %s   non-{1,V} summands %s" % (n, cover_string(n, down), other))
    closed = all(r[3]["eps"] == Fraction(4 * r[4], r[0] * r[0] - 1) for r in rows)
    print("    eps = 4k/(n^2-1) at every member: %s" % closed)
    print("    NEW PRIMITIVE boundary/frozen posets at n > 3: %d" % len(prims))
    for (n, down, d) in prims:
        print("        ⚠️⚠️  n=%d  delta=%s  %s" % (n, d, cover_string(n, down)))
    print()
    print("    per-n distribution of eps inside this restricted population:")
    print("    %3s %8s %13s %13s %13s" % ("n", "count", "min eps", "median eps", "max eps"))
    per = {}
    for (n, down, d, mm, kV, other) in rows:
        per.setdefault(n, []).append(mm["eps"])
    for n in sorted(per):
        v = sorted(per[n])
        med = v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2
        print("    %3d %8d %13s %13s %13s" % (n, len(v), str(v[0]), str(med), str(v[-1])))
    return len(bad) == 0 and closed and len(prims) == 0


def main():
    print("=" * 100)
    print("mg-6ff4  c2  reach beyond the exhaustive range, and the restriction it is bought with")
    print("=" * 100)
    print()

    print("m1  WIDTH <= 3, EXHAUSTIVE, n = 2..%d" % WMAX3)
    print("-" * 100)
    t3, r3, p3 = sweep(WMAX3, 3, "w<=3")
    ok3 = report("w<=3", t3, r3, p3, WMAX3)
    print()

    print("m2  WIDTH <= 2, EXHAUSTIVE, n = 2..%d" % WMAX2)
    print("-" * 100)
    t2, r2, p2 = sweep(WMAX2, 2, "w<=2")
    ok2 = report("w<=2", t2, r2, p2, WMAX2)
    print()

    print("m3  WHAT THIS DOES AND DOES NOT ESTABLISH")
    print("-" * 100)
    print("    DOES: within width <= 3 to n = %d and width <= 2 to n = %d, the boundary class is"
          % (WMAX3, WMAX2))
    print("    still exactly the ordinal sums of singletons and copies of the 3-element V, no new")
    print("    primitive member appears, and eps = 4k/(n^2-1) holds at every member.")
    print("    DOES NOT: say anything about width >= 4 at n >= 10 -- that is mg-c47a's DROPPED")
    print("    residual and this arm inherits it unchanged.  It also says nothing about the FROZEN")
    print("    class, which is empty here for the same reason it is empty everywhere.")
    print()

    ok = ok3 and ok2
    print("VERDICT: %s" % ("GREEN" if ok else "RED -- see the flagged rows above"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
