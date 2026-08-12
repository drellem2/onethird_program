#!/usr/bin/env python3
"""mg-6ff4 arm c1 — THE CENSUS AND THE DISTRIBUTION.  `ε_spec = 6·E[inv_e]/(n²−1)` at every
poset with `δ(P) = 1/3` EXACTLY, `n = 3 … NMAX`, EXHAUSTIVE over every isomorphism class.

  m1  CENSUS.  posets with an incomparable pair · min `δ` · #{δ = 1/3} · #{δ < 1/3}.
      The last column is the frozen class and it is EMPTY BY CONSTRUCTION — `δ < 1/3` IS the
      counterexample condition and the conjecture is verified to `n = 14` (`mg-33f5`).  It is
      printed so the `0` cannot be re-quoted as a clean sweep.
  m2  THE FULL BOUNDARY POPULATION, one row per poset: `m`, `d`, `q̄`, `E[inv_e]`, `ε`, width,
      primitive?, and the ordinal decomposition.
  m3  THE DISTRIBUTION per `n`: min / median / max of `ε`, and the poset attaining the max,
      printed as its cover relation so it can be checked by hand.
  m4  THE STRUCTURE.  Is every boundary poset an ordinal sum of singletons and copies of the
      3-element `V`?  Checked, not assumed — the closed form in `c3` is worth nothing if it is
      not, and this is the check that would kill it.

Default `NMAX = 9`; pass an integer argument to override.  `n = 9` is 183 231 isomorphism classes
and takes a few minutes; the early exit in `delta_at_most` is what makes it affordable.

Exits 0 if the census is internally consistent and the frozen count is 0, 1 otherwise, 2 on
refusal.
"""

import sys
from fractions import Fraction

import lib6ff4 as L

V_CANON = L.canon(3, (0, 1, 0))          # the 3-element V, in canonical form


def cover_string(n, down):
    """The cover relations, as `a<b` pairs, so the poset can be read by hand."""
    cov = []
    for j in range(n):
        for i in range(n):
            if L.is_below(down, i, j):
                if not any(L.is_below(down, i, k) and L.is_below(down, k, j) for k in range(n)):
                    cov.append("%d<%d" % (i, j))
    return " ".join(cov) if cov else "(antichain)"


def median(vals):
    v = sorted(vals)
    k = len(v)
    if k == 0:
        return None
    if k % 2:
        return v[k // 2]
    return (v[k // 2 - 1] + v[k // 2]) / 2


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    print("=" * 100)
    print("mg-6ff4  c1  eps_spec on the boundary class delta = 1/3, EXHAUSTIVE n = 2..%d" % nmax)
    print("=" * 100)
    print()
    print("  eps_obs(P) = 6*E[inv_e]/(n^2-1),  e = the >= 2/3 majority order (see c4 for how it is")
    print("  chosen and whether that choice is forced).  Exact rationals throughout; no float on")
    print("  any verdict path.")
    print()

    classes = L.all_classes(nmax)
    census = {}
    boundary = []
    for n in range(2, nmax + 1):
        tot = at3 = be3 = 0
        mn = None
        for down in classes[n]:
            if not L.incomparable_pairs(n, down):
                continue
            tot += 1
            ok, d, tbl = L.delta_at_most(n, down)
            if not ok:
                continue
            if mn is None or d < mn:
                mn = d
            if d == L.THIRD:
                at3 += 1
                boundary.append((n, down, tbl))
            else:
                be3 += 1
        if mn is None:
            # nothing at or below 1/3 at this n: recompute the true minimum without early exit
            for down in classes[n]:
                inc = L.incomparable_pairs(n, down)
                if not inc:
                    continue
                t = L.count_ext(n, down)
                dd = max(min(p, 1 - p) for p in
                         (L.p_before(n, down, i, j, t) for (i, j) in inc))
                if mn is None or dd < mn:
                    mn = dd
        census[n] = (tot, mn, at3, be3)
        print("    ... n = %d done: %d posets, %d at the boundary" % (n, tot, at3), flush=True)
    print()

    print("m1  CENSUS -- EXHAUSTIVE over every isomorphism class")
    print("-" * 100)
    print("    %3s %11s %14s %14s %22s" % ("n", "posets", "min delta", "delta = 1/3",
                                           "delta < 1/3 (FROZEN)"))
    for n in sorted(census):
        tot, mn, at3, be3 = census[n]
        print("    %3d %11d %14s %14d %22d" % (n, tot, str(mn), at3, be3))
    total_frozen = sum(v[3] for v in census.values())
    print()
    print("    FROZEN POSETS FOUND: %d." % total_frozen)
    print("    ⚠️  THAT ZERO CARRIES NO INFORMATION.  delta < 1/3 IS the counterexample condition")
    print("    and the conjecture is verified to n = 14, so the frozen population any enumerator")
    print("    can reach is EMPTY BY CONSTRUCTION.  NOTHING BELOW IS A FROZEN-CLASS NUMBER.")
    print()

    print("m2  THE BOUNDARY POPULATION, every member")
    print("-" * 100)
    print("    %3s %4s %8s %8s %8s %10s %6s %5s %-9s %s"
          % ("n", "m", "d", "qbar", "E[inv_e]", "eps", "width", "prim", "summands", "covers"))
    rows = []
    for (n, down, tbl) in boundary:
        mm = L.measure(n, down, tbl)
        w = L.width(n, down)
        prim = L.is_primitive(n, down)
        summ = L.ordinal_summands(n, down)
        sig = tuple(sorted((k, "V" if (k == 3 and d == V_CANON) else
                            ("1" if k == 1 else "?")) for k, d in summ))
        kV = sum(1 for k, d in summ if k == 3 and d == V_CANON)
        other = [(k, d) for k, d in summ if not (k == 1 or (k == 3 and d == V_CANON))]
        rows.append((n, mm, w, prim, kV, other, down))
        print("    %3d %4d %8s %8s %8s %10s %6d %5s %-9s %s"
              % (n, mm["m"], str(mm["d"]), str(mm["qbar"]), str(mm["Einv"]), str(mm["eps"]),
                 w, "yes" if prim else "no",
                 ("%dxV" % kV) + ("+%d" % len(other) if other else ""),
                 cover_string(n, down)))
    print()

    print("m3  THE DISTRIBUTION OF eps, per n")
    print("-" * 100)
    print("    %3s %7s %12s %12s %12s %11s   %s"
          % ("n", "count", "min eps", "median eps", "max eps", "max (dec)", "argmax poset"))
    per_n = {}
    for (n, mm, w, prim, kV, other, down) in rows:
        per_n.setdefault(n, []).append((mm["eps"], down, kV))
    trend = {}
    for n in sorted(per_n):
        vals = [r[0] for r in per_n[n]]
        mx = max(vals)
        arg = [r for r in per_n[n] if r[0] == mx][0]
        trend[n] = (min(vals), median(vals), mx)
        print("    %3d %7d %12s %12s %12s %11.6f   %s"
              % (n, len(vals), str(min(vals)), str(median(vals)), str(mx), float(mx),
                 cover_string(n, arg[1])))
    print()
    print("    THE TREND, max eps against n:")
    ns = sorted(trend)
    print("      " + "  ".join("n=%d:%s" % (n, trend[n][2]) for n in ns))
    falling = all(trend[ns[i]][2] > trend[ns[i + 1]][2] for i in range(len(ns) - 1))
    print("      strictly FALLING at every step: %s" % falling)
    print("    THE TREND, min eps against n:")
    print("      " + "  ".join("n=%d:%s" % (n, trend[n][0]) for n in ns))
    print()

    print("m4  THE STRUCTURE -- is every boundary poset an ordinal sum of singletons and V's?")
    print("-" * 100)
    bad_struct = [(n, down, other) for (n, mm, w, prim, kV, other, down) in rows if other]
    prim_members = [(n, down) for (n, mm, w, prim, kV, other, down) in rows if prim]
    widths = sorted({w for (n, mm, w, prim, kV, other, down) in rows})
    print("    boundary posets: %d   ·   NOT a sum of singletons and V's: %d"
          % (len(rows), len(bad_struct)))
    for n, down, other in bad_struct:
        print("        ⚠️  n=%d  %s   non-{1,V} summands %s" % (n, cover_string(n, down), other))
    print("    widths present: %s" % (widths,))
    print("    PRIMITIVE boundary posets: %d" % len(prim_members))
    for n, down in prim_members:
        print("        n=%d   %s" % (n, cover_string(n, down)))
    print()
    print("    A minimal counterexample is PRIMITIVE (STATE.md row 2 / :55).  The primitive count")
    print("    above is therefore the scope limit of every figure in this instrument, and it")
    print("    travels with them.")
    print()
    print("    THE CLOSED FORM THIS LICENSES (and only at the n it was checked at):")
    print("      a boundary poset on n elements is k >= 1 copies of V ordinally summed with")
    print("      n - 3k singletons, so   m = 2k,  qbar = 1/3,  E[inv_e] = 2k/3,")
    print("      eps = 4k/(n^2-1),  and the count at each n is  sum_k C(n-2k, k).")
    pred_counts = {}
    for n in sorted(census):
        c = 0
        k = 1
        while 3 * k <= n:
            a, b = n - 2 * k, k
            num = 1
            for t in range(b):
                num = num * (a - t) // (t + 1)
            c += num if a >= b else 0
            k += 1
        pred_counts[n] = c
    agree = all(pred_counts[n] == census[n][2] for n in census)
    print("      predicted counts  %s" % {n: pred_counts[n] for n in sorted(census)})
    print("      measured  counts  %s" % {n: census[n][2] for n in sorted(census)})
    print("      agree: %s" % agree)
    eps_agree = all(mm["eps"] == Fraction(4 * kV, n * n - 1)
                    for (n, mm, w, prim, kV, other, down) in rows)
    print("      eps = 4k/(n^2-1) at every member: %s" % eps_agree)
    print()

    ok = total_frozen == 0 and len(rows) > 0 and not bad_struct and agree and eps_agree
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
