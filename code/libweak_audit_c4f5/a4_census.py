#!/usr/bin/env python3
"""a4_census — reproduce every printed count in mg-c3ca Sec.6, then add n = 7.

mg-c3ca's own recorded defect 3 says n=7 was not attempted because its census walks
the population twice.  This instrument runs off the ideal DP instead of enumerating
linear extensions, so n=7 (96 428 naturally labelled posets) is reachable, and the
fifth point is what tests Sec.6's four-point reads.

EVERY published figure of Sec.6 is re-derived from a parser that shares no code with
lib_c3ca.  Where a figure needs a population definition that Sec.6 states in prose
("the critical family", "primitive"), BOTH readings are printed rather than one chosen.
"""
import sys
from fractions import Fraction
import lib_c4f5 as L

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7

print("=" * 78)
print("a4_census -- mg-c3ca Sec.6 reproduced and extended to n = %d" % NMAX)
print("POPULATION: every naturally labelled poset on n elements (A006455 counts).")
print("GRAIN: one naturally labelled poset.  EXACT Fractions, no tolerance.")
print("=" * 78)

# ---------------------------------------------------------------- gather once per n
data = {}
for n in range(3, NMAX + 1):
    rows = []
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        if a["delta"] is None:
            continue                       # chains: delta undefined, NOT 0
        rows.append((a["delta"], L.E_maj(a), a["primitive"], a["up"]))
    data[n] = rows
    print("  gathered n=%d : %d posets with at least one incomparable pair" % (n, len(rows)))

print()
print("-" * 78)
print("R1. min delta, ALL posets   [Sec.6: `min delta = 1/3 exactly at every n=3..6`]")
print("-" * 78)
print("%4s %14s %14s %10s" % ("n", "min delta", "as float", "== 1/3 ?"))
for n in range(3, NMAX + 1):
    md = min(r[0] for r in data[n])
    print("%4d %14s %14.6f %10s" % (n, md, float(md), md == Fraction(1, 3)))

print()
print("-" * 78)
print("R2. FROZEN COUNT   [Sec.6: `0 frozen posets found, as the conjecture requires`]")
print("-" * 78)
for n in range(3, NMAX + 1):
    f = sum(1 for r in data[n] if r[0] < Fraction(1, 3))
    at = sum(1 for r in data[n] if r[0] == Fraction(1, 3))
    print("  n=%d : delta < 1/3 -> %d      delta == 1/3 -> %d   (population %d)"
          % (n, f, at, len(data[n])))
print("  NON-VACUITY: the detector is drilled on a constructed frozen table in")
print("  selftest_c4f5.py sections G1/G4, so `0` here is a measurement and not silence.")

print()
print("-" * 78)
print("R3. min delta, PRIMITIVE ONLY   [Sec.6: `0.400, 0.364, 0.357` at n=4,5,6]")
print("-" * 78)
print("%4s %14s %12s %10s %12s" % ("n", "min delta prim", "as float", "mg-c3ca", "match"))
PUB = {4: 0.400, 5: 0.364, 6: 0.357}
for n in range(3, NMAX + 1):
    prim = [r for r in data[n] if r[2]]
    if not prim:
        print("%4d %14s" % (n, "NO PRIMITIVE POSETS"))
        continue
    md = min(r[0] for r in prim)
    pub = PUB.get(n)
    ok = "-" if pub is None else ("YES" if abs(float(md) - pub) < 5e-4 else "NO")
    print("%4d %14s %12.6f %10s %12s"
          % (n, md, float(md), "%.3f" % pub if pub else "(new)", ok))

print()
print("-" * 78)
print("R4. max E_maj ON THE PRIMITIVE CRITICAL FAMILY")
print("    [Sec.6: `0.67, 1.00, 1.55, 1.64` at n=3..6, read as Theta(n)-shaped]")
print("-" * 78)
print("`critical family` is prose.  BOTH readings printed:")
print("  (a) delta == the primitive minimum exactly")
print("  (b) delta <= the primitive minimum + 1/100  (a tolerance band)")
print()
print("%4s %12s %12s %8s %12s %8s %10s %12s"
      % ("n", "min d prim", "max E_maj(a)", "#(a)", "max E_maj(b)", "#(b)", "mg-c3ca", "match(a)"))
PUB4 = {3: 0.67, 4: 1.00, 5: 1.55, 6: 1.64}
obs = {}
for n in range(3, NMAX + 1):
    prim = [r for r in data[n] if r[2]]
    if not prim:
        continue
    md = min(r[0] for r in prim)
    fam_a = [r for r in prim if r[0] == md]
    fam_b = [r for r in prim if r[0] <= md + Fraction(1, 100)]
    ma = max(r[1] for r in fam_a)
    mb = max(r[1] for r in fam_b)
    obs[n] = float(ma)
    pub = PUB4.get(n)
    ok = "-" if pub is None else ("YES" if abs(float(ma) - pub) < 6e-3 else "NO")
    print("%4d %12s %12.4f %8d %12.4f %8d %10s %12s"
          % (n, md, float(ma), len(fam_a), float(mb), len(fam_b),
             "%.2f" % pub if pub else "(new)", ok))

print()
print("-" * 78)
print("R5. IS `0.67, 1.00, 1.55, 1.64` Theta(n)-SHAPED?  (P11)")
print("-" * 78)
print("Sec.6 reads four points as `growing like Theta(n), i.e. LIB-scale`.  A fifth")
print("point is the test.  Least-squares line through the FOUR PUBLISHED points only,")
print("then the n=%d value measured against it:" % NMAX)
xs = sorted(PUB4)
ys = [PUB4[x] for x in xs]
k = len(xs)
sx = sum(xs); sy = sum(ys)
sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
den = k * sxx - sx * sx
slope = (k * sxy - sx * sy) / den
icpt = (sy - slope * sx) / k
print("  fit through n=3..6 published: E_maj ~ %.5f n %+.5f" % (slope, icpt))
for n in sorted(obs):
    pred = slope * n + icpt
    print("    n=%d  fitted %7.4f   measured %7.4f   miss %+7.2f%%"
          % (n, pred, obs[n], 100.0 * (obs[n] - pred) / pred))
print()
print("  successive ratios of the published four: %s"
      % ["%.3f" % (ys[i + 1] / ys[i]) for i in range(len(ys) - 1)])
print("  P11 predicted the n=7 point misses the fit by more than 15%%.")

print()
print("-" * 78)
print("R6. max E_maj/n^2 over the WHOLE critical family (delta == global min)")
print("    [README: `falls 0.074 -> 0.037`;  doc Sec.6: `0.074 -> 0.046`]")
print("-" * 78)
print("  DEFECT 3 OF THIS INSTRUMENT, kept: I wrote this header as `THESE TWO PUBLISHED")
print("  PAIRS DISAGREE WITH EACH OTHER` BEFORE measuring, and they do not.  They are")
print("  the same quantity over two populations and each is correctly scoped where it")
print("  is printed -- the README's 0.037 belongs to its p1_census row (all posets) and")
print("  the doc's 0.046 to its primitive paragraph.  RESOLVED, NOT A FINDING.")
print("  What DOES survive: the all-poset sequence is NOT MONOTONE (see the column),")
print("  so `falls 0.074 -> 0.037` is an endpoint statement about a sequence that rises")
print("  in its last step.  DEFECT 4 OF THIS INSTRUMENT: I then wrote `the primitive")
print("  sequence is monotone and -> 0.046 is fair` -- and at n=7 IT RISES TOO (0.0456")
print("  -> 0.0481).  Written at n<=6, refuted by this file's own next row. Kept.")
print("%4s %14s %14s %14s" % ("n", "max E_maj/n^2", "(all critical)", "(primitive crit)"))
for n in range(3, NMAX + 1):
    md = min(r[0] for r in data[n])
    fam = [r for r in data[n] if r[0] == md]
    allc = max(r[1] for r in fam) / (n * n)
    prim = [r for r in data[n] if r[2]]
    if prim:
        mdp = min(r[0] for r in prim)
        famp = [r for r in prim if r[0] == mdp]
        pc = max(r[1] for r in famp) / (n * n)
    else:
        pc = None
    print("%4d %14.5f %14.5f %14s"
          % (n, float(allc), float(allc), "%.5f" % float(pc) if pc is not None else "-"))

print()
print("-" * 78)
print("R7. THE k-V-GADGET ORDINAL SUM   [Sec.6: `E_maj = (2/9)n exactly at every k`]")
print("-" * 78)
print("The `V-gadget` is C_2 (+) C_1 (delta = 1/3, E_maj = 2/3), NOT {0<1, 0<2}")
print("(which has delta = 1/2).  See selftest defect 1.  Ordinal sum of k copies:")
for k in (1, 2, 3, 4):
    n = 3 * k
    # ordinal sum of k copies of W_2 = C_2 (+) C_1 on 3 elements each
    pairs = []
    for b in range(k):
        base = 3 * b
        pairs.append((base, base + 1))          # the relation inside the gadget
        for c in range(b + 1, k):
            for i in range(3):
                for j in range(3):
                    pairs.append((base + i, 3 * c + j))
    P = L.poset_from_pairs(n, pairs)
    a = L.analyse(P)
    em = L.E_maj(a)
    print("  k=%d n=%2d  delta=%s  E_maj=%s   (2/9)n = %s   match %s"
          % (k, n, a["delta"], em, Fraction(2, 9) * n, em == Fraction(2, 9) * n))

print()
print("=" * 78)
print("a4_census done.")
print("=" * 78)
