"""Independent recomputation of sections 4, 5 and 6 of
docs/OneThird-Counterexample-Under-The-Action.md (mg-24a3 / f5d3485).
"""

import sys
from fractions import Fraction

from kernel import (Lattice, Poset, act, linear_extensions, levels_of,
                    multiplicities, posets_up_to_iso, restriction_counts)
from records import build_all

NS = range(3, 8)
REC = {n: build_all(n) for n in NS}
POPS = {}
prev = None
for n in range(1, 8):
    prev = posets_up_to_iso(n, prev)
    POPS[n] = prev
LATS = {n: Lattice(n) for n in NS}


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def ver(mine, doc, tol=0.0):
    if isinstance(doc, float):
        return "AGREES" if abs(mine - doc) <= tol else "DISAGREES (doc %s)" % doc
    return "AGREES" if mine == doc else "DISAGREES (doc %s)" % (doc,)


def mean_sd(v):
    n = len(v)
    if n == 0:
        return None, None
    m = sum(v) / n
    if n < 2:
        return m, 0.0
    return m, (sum((x - m) ** 2 for x in v) / (n - 1)) ** 0.5


# ===========================================================================
head("S4  THE QUOTIENT SIDE  (document section 4)")
DOC4 = {5: (16, 3, 1.000, 0.825, 1.16, 0.642, 0.446, 2.90),
        6: (88, 5, 1.000, 0.734, 1.95, 0.590, 0.316, 3.40),
        7: (671, 8, 1.000, 0.593, 2.64, 0.541, 0.203, 4.49)}
print("%-3s %9s %10s %20s %8s %20s %8s" %
      ("n", "tie-free", "#extremal", "qmass ext vs rest", "z", "qfrac ext vs rest", "z"))
for n in NS:
    pop = [r for r in REC[n] if not r.chain and r.tie_free and r.qmass is not None]
    if len(pop) < 6:
        print("%-3d %9d  (too few)" % (n, len(pop)))
        continue
    dmin = min(r.delta for r in pop)
    ext = [r for r in pop if r.delta == dmin]
    rest = [r for r in pop if r.delta != dmin]
    me, _ = mean_sd([float(r.qmass) for r in ext])
    mr, sr = mean_sd([float(r.qmass) for r in rest])
    fe, _ = mean_sd([float(r.qfrac) for r in ext])
    fr, sfr = mean_sd([float(r.qfrac) for r in rest])
    zm, zf = (me - mr) / sr, (fe - fr) / sfr
    d = DOC4.get(n)
    ok = d and (len(pop) == d[0] and len(ext) == d[1] and abs(me - d[2]) < 5e-4
                and abs(mr - d[3]) < 5e-4 and abs(zm - d[4]) < 5e-3
                and abs(fe - d[5]) < 5e-4 and abs(fr - d[6]) < 5e-4
                and abs(zf - d[7]) < 5e-3)
    print("%-3d %9d %10d   %.3f vs %.3f    %+5.2f    %.3f vs %.3f    %+5.2f   %s"
          % (n, len(pop), len(ext), me, mr, zm, fe, fr, zf,
             ("AGREES" if ok else "DISAGREES doc=%s" % (d,)) if d else ""))

print()
print("S4a  SATURATION CONTROL: the qmass = 1 club")
DOC4A = {5: (6, 50.0), 6: (11, 45.5), 7: (20, 40.0)}
for n in NS:
    pop = [r for r in REC[n] if not r.chain and r.tie_free and r.qmass is not None]
    if len(pop) < 6:
        continue
    dmin = min(r.delta for r in pop)
    sat = [r for r in pop if r.qmass == 1]
    ext = [r for r in pop if r.delta == dmin]
    pe = 100.0 * len(ext) / len(sat)
    d = DOC4A.get(n)
    print("  n=%d: %d of %d saturate (%.1f%% of the population); of those, %.1f%% are "
          "extremal   %s"
          % (n, len(sat), len(pop), 100.0 * len(sat) / len(pop), pe,
             ver((len(sat), round(pe, 1)), d) if d else ""))
    assert all(r.qmass == 1 for r in ext), "an extremal poset does NOT saturate"

print()
print("S4b  THE UNIVERSAL SENTENCE: 'EVERY extremal poset is rank 1 -- and TIED WITH")
print("     EVERY OTHER MEMBER of their group'.  Checked on EVERY extremal poset, with")
print("     no cap on the number printed and no minimum group size.")
allext = 0
notrank1 = 0
nottied = []
for n in NS:
    pop = [r for r in REC[n] if not r.chain and r.tie_free and r.qmass is not None]
    if len(pop) < 6:
        continue
    dmin = min(r.delta for r in pop)
    ext = sorted([r for r in pop if r.delta == dmin], key=lambda r: (r.e, r.cover))
    for r in ext:
        grp = [q for q in pop if q.e == r.e]
        better = sum(1 for q in grp if q.qmass > r.qmass)
        tied = sum(1 for q in grp if q.qmass == r.qmass and q is not r)
        allext += 1
        if better:
            notrank1 += 1
        flag = ""
        if tied != len(grp) - 1:
            nottied.append((n, r, len(grp), tied))
            flag = "   <-- NOT tied with every other member"
        print("    n=%d e=%-4d %-28s qmass=%-7s rank %d of %-3d TIED WITH %d%s"
              % (n, r.e, r.cover[:28], r.qmass, better + 1, len(grp), tied, flag))
print()
print("  extremal posets examined: %d;  not rank 1: %d;  NOT tied with every other"
      " member of their e-group: %d" % (allext, notrank1, len(nottied)))
for (n, r, g, t) in nottied:
    grp = [q for q in REC[n] if not q.chain and q.tie_free and q.qmass is not None
           and q.e == r.e]
    others = sorted(set(str(q.qmass) for q in grp if q is not r))
    print("    n=%d  %-30s e=%d  group size %d, tied with %d; other qmass values in the"
          " group: %s" % (n, r.cover, r.e, g, t, others))

# ===========================================================================
head("S5.1  THEOREM 3 (convexity) and its two counts")


def is_convex(P, B):
    n = P.n
    for j in range(n):
        if (B >> j) & 1:
            continue
        if (P.dn[j] & B) and (P.up[j] & B):
            return False
    return True


tot_lb = bad_lb = 0
tot_ps = bad_ps = 0
for n in NS:
    lat = LATS[n]
    for P, r in zip(POPS[n], REC[n]):
        for X in r.levels:
            for B in lat.parts[X]:
                tot_lb += 1
                if not is_convex(P, B):
                    bad_lb += 1
        for B in range(1, 1 << n):
            tot_ps += 1
            blocks = tuple(sorted([B] + [1 << i for i in range(n) if not (B >> i) & 1],
                                  key=lambda b: b & -b))
            islev = lat.index[blocks] in r.mult
            if islev != is_convex(P, B):
                bad_ps += 1
print("(level, block) pairs, n=3..7 : %d   %s   -- non-convex blocks found: %d"
      % (tot_lb, ver(tot_lb, 3246401), bad_lb))
print("(poset, nonempty subset) pairs: %d   %s   -- '{B}+singletons is a level IFF B "
      "convex' failures: %d" % (tot_ps, ver(tot_ps, 281977), bad_ps))

# ===========================================================================
head("S5.2  THEOREM 4:  lambda_2 = max over incomparable pairs of s(x,y)")
bad = tot = 0
for n in NS:
    for r in REC[n]:
        if r.chain:
            continue
        tot += 1
        if r.lam2 != r.s_max:
            bad += 1
print("non-chain posets n=3..7: %d  %s ; mismatches: %d %s"
      % (tot, ver(tot, 2442), bad, ver(bad, 0)))

print()
print("S5.2a  the supporting multiplicity fact: every all-chain level other than the")
print("       finest has m_X = 0, and the finest has m = 1")
tot_ac = bad_ac = 0
for n in NS:
    lat = LATS[n]
    for P, r in zip(POPS[n], REC[n]):
        for X in r.levels:
            allchain = True
            for B in lat.parts[X]:
                bits = [i for i in range(n) if (B >> i) & 1]
                for i in bits:
                    for j in bits:
                        if i < j and not ((P.up[i] >> j) & 1 or (P.dn[i] >> j) & 1):
                            allchain = False
                            break
                    if not allchain:
                        break
                if not allchain:
                    break
            if not allchain:
                continue
            if X == lat.bottom:
                if r.mult[X] != 1:
                    bad_ac += 1
                continue
            tot_ac += 1
            if r.mult[X] != 0:
                bad_ac += 1
print("all-chain levels other than the finest: %d  %s ; violations: %d"
      % (tot_ac, ver(tot_ac, 65481), bad_ac))

# ===========================================================================
head("S5.3  primitivity <=> strictly positive excess at every 2-block level")
tot2 = bad2 = 0
badprim = 0
for n in NS:
    lat = LATS[n]
    for P, r in zip(POPS[n], REC[n]):
        e = restriction_counts(P)
        pos_everywhere = True
        for i, blocks in enumerate(lat.parts):
            if len(blocks) != 2:
                continue
            tot2 += 1
            A, B = blocks
            isideal = not any((P.up[x] & B) and False for x in range(n))
            # {A,B} is a level iff no arrows both ways iff A is an ideal or a filter
            downA = all(not (P.dn[x] & B) for x in range(n) if (A >> x) & 1)
            upA = all(not (P.up[x] & B) for x in range(n) if (A >> x) & 1)
            islev = lat.index[blocks] in r.mult
            if islev != (downA or upA):
                bad2 += 1
            if islev:
                excess = r.e - e[A] * e[B]
                # identity: excess == sum of m_Y over levels Y that do NOT refine {A,B};
                # refiners[X] lists the partitions that refine X.
                ref = set(lat.refiners[lat.index[blocks]])
                s = sum(r.mult[Y] for Y in r.levels if Y not in ref)
                if excess != s:
                    bad2 += 1
                if excess <= 0:
                    pos_everywhere = False
        if pos_everywhere != r.primitive:
            badprim += 1
print("2-block partitions over all 2447 posets: %d  %s ; failures of the level"
      " description or of the excess identity: %d" % (tot2, ver(tot2, 139765), bad2))
print("posets where 'primitive <=> positive excess everywhere' fails: %d of %d  %s"
      % (badprim, sum(len(REC[n]) for n in NS),
         ver(sum(len(REC[n]) for n in NS), 2447)))

# ===========================================================================
head("S5.4  PROPOSITION 6 (frozen => e(P) >= 4) and the e(P) = 3 count")
DOC54 = {3: (1, 1), 4: (2, 2), 5: (3, 3), 6: (4, 5), 7: (5, 8)}
for n in NS:
    pop = [r for r in REC[n] if not r.chain]
    dmin = min(r.delta for r in pop)
    ext = [r for r in pop if r.delta == dmin]
    n3 = sum(1 for r in ext if r.e == 3)
    print("  n=%d: %d of %d extremal posets have e(P) = 3   %s"
          % (n, n3, len(ext), ver((n3, len(ext)), DOC54[n])))
print("  smallest e(P) over all non-chains with delta < 1/2 (sanity): "
      "%s" % min(r.e for n in NS for r in REC[n]
                 if not r.chain and r.delta < Fraction(1, 2)))
