"""A5 -- the POWERED test, recomputed, and the saturation control.

The repair's section 4 is where it says the claim actually lives: the pooled
within-e(P) association between qmass and delta over the WHOLE population, by
the target's own section 6 recipe.  It reports

    n     population   e-groups   qmass rho|e   qfrac rho|e
    6     88           27         -0.287        -0.009
    7     671          127        -0.261        +0.011
    8     6420         670        -0.273        +0.018

This recomputes all of it from the independent kernel, plus the saturation
control ("qmass = 1 retains 36 of 6420 at n = 8, a third of them extremal")
and the raw effect table.

Recipe, read off the repair: mean-centre the RAW values inside each e-group of
size >= 3, pool, then Spearman on the pooled columns.  tau_b is Kendall's
tie-corrected coefficient on within-group pairs, and z uses Kendall's
tie-corrected null variance summed over the groups.  A third, differently
ordered recipe is reported alongside as a sensitivity check.
"""

import math
import os
import pickle
import sys
from collections import Counter
from fractions import Fraction

from kernel import Poset, enumerate_posets, qstats

NMAX = 8
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".records.pkl")


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def records():
    if os.path.exists(CACHE):
        return pickle.load(open(CACHE, "rb"))
    lv = enumerate_posets(NMAX)
    out = {}
    for n in range(5, NMAX + 1):
        rows = []
        for P in lv[n]:
            if P.is_chain() or not P.tie_free() or P.majority_cycle() is not None:
                continue
            qf, qm, nlev, good = qstats(P)
            rows.append((P.e(), P.delta(), qm, qf, nlev))
        out[n] = rows
        print("    [records n=%d: %d]" % (n, len(rows)), file=sys.stderr)
    pickle.dump(out, open(CACHE, "wb"))
    return out


def midranks(vals):
    n = len(vals)
    order = sorted(range(n), key=lambda i: vals[i])
    r = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        m = ((i + 1) + (j + 1)) / 2.0
        for t in range(i, j + 1):
            r[order[t]] = m
        i = j + 1
    return r


def rho_target_recipe(groups, xi, yi):
    """The recipe the repair states it used, and the target's section 6 recipe:
    mean-centre the RAW values inside each e-group of size >= 3, pool, then
    Spearman (mid-rank both pooled columns, Pearson on the ranks)."""
    px, py = [], []
    for g in groups:
        if len(g) < 3:
            continue
        a = [float(r[xi]) for r in g]
        b = [float(r[yi]) for r in g]
        ma, mb = sum(a) / len(a), sum(b) / len(b)
        px += [t - ma for t in a]
        py += [t - mb for t in b]
    if len(px) < 4:
        return None
    rx, ry = midranks(px), midranks(py)
    n = len(rx)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((u - mx) * (v - my) for u, v in zip(rx, ry))
    dx = math.sqrt(sum((u - mx) ** 2 for u in rx))
    dy = math.sqrt(sum((v - my) ** 2 for v in ry))
    return num / (dx * dy) if dx and dy else None


def rho_within(groups, xi, yi):
    """Mean-centre ranks inside each group, pool, Pearson."""
    xs, ys = [], []
    for g in groups:
        if len(g) < 3:
            continue
        rx = midranks([row[xi] for row in g])
        ry = midranks([row[yi] for row in g])
        mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
        xs.extend(v - mx for v in rx)
        ys.extend(v - my for v in ry)
    sxy = sum(a * b for a, b in zip(xs, ys))
    sxx = sum(a * a for a in xs)
    syy = sum(b * b for b in ys)
    if sxx == 0 or syy == 0:
        return 0.0, 0
    return sxy / math.sqrt(sxx * syy), sum(1 for g in groups if len(g) >= 3)


def tau_b_within(groups, xi, yi, minsize=2):
    """Kendall's tau_b on WITHIN-group pairs only, and the tie-corrected z.

    tau_b = (C - D) / sqrt((n0 - n1)(n0 - n2)) with n1, n2 the tied-pair counts
    in x and in y; z = sum(C - D) / sqrt(sum of Kendall's TIE-CORRECTED null
    variance over the independent groups, which is the variance the repair says
    it uses).
    """
    c = d = xo = yo = 0
    S = 0.0
    var = 0.0
    used = 0
    for g in groups:
        n = len(g)
        if n < minsize:
            continue
        used += 1
        gc = gd = 0
        for i in range(n):
            for j in range(i + 1, n):
                a = g[i][xi] - g[j][xi]
                b = g[i][yi] - g[j][yi]
                if a == 0 and b == 0:
                    continue
                elif a == 0:
                    xo += 1
                elif b == 0:
                    yo += 1
                elif (a > 0) == (b > 0):
                    gc += 1
                else:
                    gd += 1
        c += gc
        d += gd
        S += gc - gd
        t = list(Counter(r[xi] for r in g).values())
        u = list(Counter(r[yi] for r in g).values())
        st1 = sum(x * (x - 1) * (2 * x + 5) for x in t)
        su1 = sum(x * (x - 1) * (2 * x + 5) for x in u)
        st2 = sum(x * (x - 1) * (x - 2) for x in t)
        su2 = sum(x * (x - 1) * (x - 2) for x in u)
        st3 = sum(x * (x - 1) for x in t)
        su3 = sum(x * (x - 1) for x in u)
        v = (n * (n - 1) * (2 * n + 5) - st1 - su1) / 18.0
        if n > 2:
            v += st2 * su2 / (9.0 * n * (n - 1) * (n - 2))
        v += st3 * su3 / (2.0 * n * (n - 1))
        var += v
    den = math.sqrt((c + d + yo) * (c + d + xo))
    tb = (c - d) / den if den else 0.0
    z = S / math.sqrt(var) if var > 0 else 0.0
    return tb, z, used


def main():
    rec = records()

    banner("A5.1  the powered test: pooled within-e(P) association")
    print("  repair reports  qmass rho|e = -0.287 / -0.261 / -0.273  at n = 6/7/8")
    print("                  qfrac rho|e = -0.009 / +0.011 / +0.018")
    print()
    print("  TARGET'S RECIPE (mean-centre the RAW values in each group, pool, Spearman)")
    print("  -- this is the recipe the repair states it used, so this is the check.")
    print()
    print("  n | population | e-groups | used(>=3) | qmass rho|e | qfrac rho|e")
    for n in range(5, NMAX + 1):
        rows = rec[n]
        byE = {}
        for r in rows:
            byE.setdefault(r[0], []).append(r)
        groups = list(byE.values())
        used = sum(1 for g in groups if len(g) >= 3)
        rq = rho_target_recipe(groups, 2, 1)
        rf = rho_target_recipe(groups, 3, 1)
        f = lambda v: "n/a" if v is None else "%+.3f" % v
        print("  %d | %10d | %8d | %9d | %11s | %11s"
              % (n, len(rows), len(groups), used, f(rq), f(rf)))
    print()
    print("  KENDALL tau_b AND THE TIE-CORRECTED z, on within-group pairs.")
    print()
    print("  n | population | groups(>=2) | qmass tau_b |    z    | qfrac tau_b |    z")
    for n in range(5, NMAX + 1):
        rows = rec[n]
        byE = {}
        for r in rows:
            byE.setdefault(r[0], []).append(r)
        groups = list(byE.values())
        tq, zq, used = tau_b_within(groups, 2, 1)
        tf, zf, _ = tau_b_within(groups, 3, 1)
        print("  %d | %10d | %11d | %+11.4f | %+7.2f | %+11.4f | %+7.2f"
              % (n, len(rows), used, tq, zq, tf, zf))
    print()
    print("  repair reports  qmass tau_b / z  -0.2978/-1.76  -0.2626/-5.65  -0.2052/-16.60")
    print("                  qfrac tau_b / z  -0.2259/-1.53  -0.0569/-1.29  +0.0064/+0.54")
    print()
    print("  SENSITIVITY, a third recipe: rank INSIDE each group first, then centre")
    print("  the ranks, then pool.  Same intent, different order of operations.")
    print("  Reported because a headline that moves under it is a headline about the")
    print("  recipe rather than about the data.")
    print()
    print("  n | groups(>=3) | qmass rho | qfrac rho")
    for n in range(5, NMAX + 1):
        rows = rec[n]
        byE = {}
        for r in rows:
            byE.setdefault(r[0], []).append(r)
        groups = list(byE.values())
        rq, ng = rho_within(groups, 2, 1)
        rf, _ = rho_within(groups, 3, 1)
        print("  %d | %11d | %+9.3f | %+9.3f" % (n, ng, rq, rf))

    banner("A5.2  the saturation control -- the 'not a filter' clause")
    print("  n | population | qmass=1 | of those extremal | share of population")
    for n in range(5, NMAX + 1):
        rows = rec[n]
        club = [r for r in rows if r[2] == 1]
        ext = sum(1 for r in club if r[1] == Fraction(1, 3))
        print("  %d | %10d | %7d | %17d | %6.1f%%"
              % (n, len(rows), len(club), ext, 100.0 * len(club) / len(rows)))
    print()
    print("  repair / target say: 6 of 16, 11 of 88, 20 of 671, 36 of 6420, with")
    print("  50.0%% / 45.5%% / 40.0%% / 33.3%% of the club extremal.")

    banner("A5.3  the raw effect table (target section 4), recomputed")
    print("  n | tie-free | #extremal | qmass ext | qmass rest | qfrac ext | qfrac rest")
    for n in range(5, NMAX + 1):
        rows = rec[n]
        ext = [r for r in rows if r[1] == Fraction(1, 3)]
        rest = [r for r in rows if r[1] != Fraction(1, 3)]
        f = lambda s, i: float(sum(r[i] for r in s) / len(s))
        print("  %d | %8d | %9d | %9.3f | %10.3f | %9.3f | %10.3f"
              % (n, len(rows), len(ext), f(ext, 2), f(rest, 2), f(ext, 3), f(rest, 3)))

    banner("A5.4  ATTAINABILITY over the whole population")
    print("  Is the refuting conjunction -- NON-extremal with qmass = 1 -- realisable?")
    print()
    print("  n | non-extremal with qmass=1 | of all non-extremal | extremal with qmass<1")
    for n in range(5, NMAX + 1):
        rows = rec[n]
        ne = [r for r in rows if r[1] != Fraction(1, 3)]
        ee = [r for r in rows if r[1] == Fraction(1, 3)]
        a = sum(1 for r in ne if r[2] == 1)
        b = sum(1 for r in ee if r[2] != 1)
        print("  %d | %25d | %18.2f%% | %21d"
              % (n, a, 100.0 * a / len(ne), b))
    print()
    print("  So the hypothesis IS falsifiable as a statement about posets: the")
    print("  refuting conjunction occurs, and is the MAJORITY of the qmass = 1 club.")
    print("  What is claimed is that it never occurs INSIDE an e-group containing an")
    print("  extremal poset.  That is a real restriction -- see check_independence.py")
    print("  for how many INDEPENDENT chances it had to fail.")


if __name__ == "__main__":
    main()
