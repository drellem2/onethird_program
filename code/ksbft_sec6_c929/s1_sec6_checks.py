"""mg-c929 s1 -- exact checks of the KSBFT section-5/6 inequalities this deliverable consumes,
over EVERY naturally-labelled poset on n <= NMAX elements (duplicates up to isomorphism are
harmless: every check is a universal statement).

Quantities (KSBFT section 5.1, notation of the paper):
  f uniform linear extension, positions 1..n.
  h(x)   = E f(x)                                  (pair-marginal: 1 + sum_y p(y<x))
  Delta  = |h(x) - h(y)|
  d(x,y) = sd(Z_x - Z_y), Z = (n+1)F, F uniform on the order polytope.
           Coupling F_x = U_(f(x)) with U_(k) the order statistics of n iid U[0,1],
           independent of f.  Given f, Z_x - Z_y has mean k = f(x)-f(y) and variance
           |k|(n+1-|k|)/(n+2) (Beta(|k|, n+1-|k|) spacing, times (n+1)^2).  So
             d^2 = Var(f(x)-f(y)) + E[|k|(n+1-|k|)]/(n+2).
           POSITIVE CONTROL for the formula: the 2-antichain, where F is uniform on [0,1]^2
           and Var(3F_x - 3F_y) = 9/6 = 3/2 by hand.
  a_x    = E[f(x) - q(x)], q(x) = max position of a predecessor (0 if none)  (= win(x)/2)

Checks (each prints its worst slack; slack < -TOL is a FAILURE):
  C51  (5.1)  min(P[x<y], P[y<x]) >= 1/e - Delta/d                   all ordered pairs
  C52  (5.2)  P[against height order] <= exp(1 - Delta/d)            pairs with Delta > 0
  C53a (5.3)  a_x >= 1
  C53b (5.3)  d(x,y) >= a_x/sqrt3                                     all ordered pairs
  C53c AK25a Thm 2.9: sum_{x in B} a_x >= (n+1)|B|^2/(2n)            every antichain B
  C54  (5.4)  d(x,z)^2 <= d(x,y)^2 + d(y,z)^2                        all triples
  C55  Haqi-Kahn: max_{x in I} h(x) >= |I| - |max(I)| + 1            every nonempty ideal I
  CW   window-occupancy identity: sum_x (a_x - 1) = E[#{(z,x): z||x, q(x) < f(z) < f(x)}]
  C611 (6.11) on posets with delta(P) < 1/e, eps := 1/e - delta(P), gap on P-hat:
             P[against height] <= exp(1 - eps*sqrt(Delta/gap))
  C64  (6.4) height separation Delta >= eps/sqrt3, same population
"""
import itertools, math, sys
from fractions import Fraction

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
TOL = 1e-9
E = math.e


def posets(n):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for mask in range(1 << len(pairs)):
        rel = set(p for b, p in enumerate(pairs) if mask >> b & 1)
        ok = True
        for (i, j) in rel:
            for k in range(j + 1, n):
                if (j, k) in rel and (i, k) not in rel:
                    ok = False; break
            if not ok: break
        if ok:
            yield rel


def extensions(n, rel):
    out = []
    for perm in itertools.permutations(range(n)):
        pos = [0] * n
        for p, x in enumerate(perm): pos[x] = p + 1
        if all(pos[i] < pos[j] for (i, j) in rel):
            out.append(pos)
    return out


def stats(n, rel, exts):
    N = len(exts)
    h = [sum(p[x] for p in exts) / N for x in range(n)]
    less = [[sum(1 for p in exts if p[x] < p[y]) / N for y in range(n)] for x in range(n)]
    d = [[0.0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x == y: continue
            ks = [p[x] - p[y] for p in exts]
            m = sum(ks) / N
            var = sum((k - m) ** 2 for k in ks) / N
            extra = sum(abs(k) * (n + 1 - abs(k)) for k in ks) / N / (n + 2)
            d[x][y] = math.sqrt(var + extra)
    preds = [[y for y in range(n) if (y, x) in rel] for x in range(n)]
    a = [sum(p[x] - max([p[y] for y in preds[x]], default=0) for p in exts) / N for x in range(n)]
    return h, less, d, a, preds


def comparable(rel, x, y):
    return (min(x, y), max(x, y)) in rel


def main():
    # positive control for the d formula
    h, less, d, a, _ = stats(2, set(), extensions(2, set()))
    print("PC d-formula: 2-antichain d^2 = %.12f  (hand value 1.5)" % (d[0][1] ** 2))
    assert abs(d[0][1] ** 2 - 1.5) < 1e-12
    worst = {k: math.inf for k in ["C51", "C52", "C53a", "C53b", "C53c", "C54", "C55", "CW", "C611", "C64", "CINV1", "CINV2"]}
    nc = {"N1": math.inf, "N2": math.inf, "cstar": math.inf}
    npos = 0; nsub = 0; nbound = 0; deltas = []
    for n in range(2, NMAX + 1):
        for rel in posets(n):
            npos += 1
            exts = extensions(n, rel)
            N = len(exts)
            h, less, d, a, preds = stats(n, rel, exts)
            inc = [(x, y) for x in range(n) for y in range(x + 1, n) if not comparable(rel, x, y)]
            delta = max([min(less[x][y], less[y][x]) for x, y in inc], default=0.0)
            for x in range(n):
                worst["C53a"] = min(worst["C53a"], a[x] - 1)
                for y in range(n):
                    if x == y: continue
                    D = abs(h[x] - h[y])
                    worst["C51"] = min(worst["C51"], min(less[x][y], less[y][x]) - (1 / E - D / d[x][y]))
                    worst["C53b"] = min(worst["C53b"], d[x][y] - a[x] / math.sqrt(3))
                    mn = min(less[x][y], less[y][x])
                    nc["N1"] = min(nc["N1"], mn - (0.51 - D / d[x][y]))
                    nc["cstar"] = min(nc["cstar"], mn + D / d[x][y])
                    ks = [p[x] - p[y] for p in exts]; m = sum(ks) / N
                    ddisc = math.sqrt(sum((k - m) ** 2 for k in ks) / N)
                    nc["N2"] = min(nc["N2"], ddisc - a[x] / math.sqrt(3))
                    if h[y] > h[x] + 1e-12:
                        worst["C52"] = min(worst["C52"], math.exp(1 - D / d[x][y]) - less[y][x])
                    for z in range(n):
                        if z in (x, y): continue
                        worst["C54"] = min(worst["C54"], d[x][y] ** 2 + d[y][z] ** 2 - d[x][z] ** 2)
            # antichains and ideals
            for r in range(1, n + 1):
                for S in itertools.combinations(range(n), r):
                    if all(not comparable(rel, x, y) for x, y in itertools.combinations(S, 2)):
                        worst["C53c"] = min(worst["C53c"], sum(a[x] for x in S) - (n + 1) * r * r / (2 * n))
                    Sset = set(S)
                    if all(y in Sset for x in S for y in preds[x]):  # ideal
                        mx = [x for x in S if not any((x, z) in rel for z in S)]
                        worst["C55"] = min(worst["C55"], max(h[x] for x in S) - (r - len(mx) + 1))
            # window occupancy identity
            occ = 0
            for p in exts:
                for x in range(n):
                    q = max([p[y] for y in preds[x]], default=0)
                    occ += sum(1 for z in range(n) if z != x and not comparable(rel, x, z) and q < p[z] < p[x])
            worst["CW"] = min(worst["CW"], -abs(sum(ai - 1 for ai in a) - occ / N))
            # section-6 population: delta(P) < 1/e
            if inc and delta < 1 / E - 1e-12:
                nsub += 1; deltas.append(delta)
                if delta <= 1 / 3 + 1e-12: nbound += 1
                eps = 1 / E - delta
                # P-hat: adjoin min and max; heights shift by 1, and hat-n = n+2
                hs = sorted([1.0] + [hh + 1 for hh in h] + [n + 2.0])
                gap = max(hs[i + 1] - hs[i] for i in range(len(hs) - 1))
                tail_sum = 0.0; inv_h = 0.0
                for x in range(n):
                    for y in range(n):
                        if x == y: continue
                        D = abs(h[x] - h[y])
                        worst["C64"] = min(worst["C64"], D - eps / math.sqrt(3))
                        if h[y] > h[x]:
                            tail_sum += min(1.0, math.exp(1 - eps * math.sqrt(D / gap)))
                            inv_h += less[y][x]
                            worst["C611"] = min(worst["C611"], math.exp(1 - eps * math.sqrt(D / gap)) - less[y][x])
                worst["CINV1"] = min(worst["CINV1"], tail_sum - inv_h)
                worst["CINV2"] = min(worst["CINV2"], 2 * math.sqrt(3) * E * gap * n / eps ** 3 - tail_sum)
    print("CINV1: E[inv_h] <= sum_pairs min(1, exp(1 - eps sqrt(Delta/gap)))")
    print("CINV2: that sum <= 2 sqrt3 e gap n / eps^3   (the closed form of the doc's Prop. B)")
    print("posets checked (naturally labelled, n=2..%d): %d" % (NMAX, npos))
    print("  of which delta(P) < 1/e (section-6 population): %d ; of those delta <= 1/3: %d" % (nsub, nbound))
    if deltas:
        print("  delta values in that population: %s" % sorted(set(round(v, 6) for v in deltas)))
    fails = 0
    for k, v in worst.items():
        status = "ok" if v >= -TOL else "FAIL"
        fails += status == "FAIL"
        print("%-5s worst slack %+.6g  %s" % (k, v, status))
    print("VERDICT: %s" % ("ALL HOLD" if fails == 0 else "%d FAILED" % fails))
    # NEGATIVE CONTROLS: the same instrument must be able to FAIL.
    print("NEGATIVE CONTROLS (each must print FIRES):")
    print("  N1 (5.1) with 0.51 in place of 1/e, worst slack %+.6g  %s"
          % (nc["N1"], "FIRES" if nc["N1"] < -TOL else "SILENT -- instrument broken"))
    print("  N2 (5.3b) with the discrete d (continuous term dropped), worst slack %+.6g  %s"
          % (nc["N2"], "FIRES" if nc["N2"] < -TOL else "SILENT -- instrument broken"))
    print("  largest c with min(P) >= c - Delta/d over ALL pairs checked: c* = %.6f (1/e = %.6f)"
          % (nc["cstar"], 1 / E))
    print("  NOTE: c* = 1/2 here is a SMALL-n fact.  AK25a Example 11.2 (cited, not re-derived) gives")
    print("  pairs with Delta = 0 and delta <= 1/e + eps at large n, so 1/e is sharp for (5.1)'s form.")


if __name__ == "__main__":
    main()
