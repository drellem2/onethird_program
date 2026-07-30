"""Controls for the mg-a7b4 audit kernel.  Nothing in the audit is quoted unless
these pass.  Run:  python3 selfcheck.py
"""

import sys
from fractions import Fraction
from itertools import permutations

from kernel import (Poset, Lattice, aut_size, canonical_key, canonical_key_allperms,
                    count_topological_sorts, delta_R, is_level, level_move_counts,
                    levels_of, linear_extensions, majority_relation, moves_of,
                    multiplicities, pair_data, posets_up_to_iso, quotient_adj,
                    restriction_counts, act)

FAIL = []


def check(name, ok, detail=""):
    print("  [%s] %s%s" % ("ok " if ok else "BAD", name, ("   " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)


# A000112 posets up to iso; A001035 labelled posets; A000670 ordered set partitions
A000112 = [1, 1, 2, 5, 16, 63, 318, 2045, 16999]
A001035 = [1, 1, 3, 19, 219, 4231, 130023, 6129859]
A000670 = [1, 1, 3, 13, 75, 541, 4683, 47293]

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7

print("C1  enumeration up to isomorphism, against A000112 (external sequence)")
pops = {0: posets_up_to_iso(0)}
prev = None
for n in range(1, NMAX + 1):
    pops[n] = posets_up_to_iso(n, prev)
    prev = pops[n]
    check("n=%d : %d classes" % (n, len(pops[n])), len(pops[n]) == A000112[n],
          "expected %d" % A000112[n])

print("C2  canonical form is CONSTANT on isomorphism classes (all n! relabellings of")
print("    every class) and SEPARATES the classes -- the property a canonical form")
print("    must have.  (It need not equal the all-perms lexicographic minimum: the")
print("    search is restricted to invariant-respecting relabellings, which is sound")
print("    because every isomorphism respects the invariant.)")
for n in range(1, min(NMAX, 6) + 1):
    bad = 0
    keys = set()
    for P in pops[n]:
        k0 = canonical_key(P)
        keys.add(k0)
        for g in permutations(range(n)):
            rel = [(g[a], g[b]) for a in range(n) for b in range(n)
                   if (P.up[a] >> b) & 1]
            if canonical_key(Poset.from_relations(n, rel)) != k0:
                bad += 1
                break
    check("n=%d : %d classes, %d distinct keys" % (n, len(pops[n]), len(keys)),
          bad == 0 and len(keys) == len(pops[n]), "%d not invariant" % bad)

print("C3  orbit count: sum over classes of n!/|Aut| == A001035 (labelled posets)")
fact = [1]
for i in range(1, 12):
    fact.append(fact[-1] * i)
for n in range(1, min(NMAX, 7) + 1):
    tot = sum(fact[n] // aut_size(P) for P in pops[n])
    check("n=%d : %d labelled" % (n, tot), tot == A001035[n], "expected %d" % A001035[n])

print("C4  e(P) by subset DP == |L(P)| by direct enumeration")
for n in range(1, min(NMAX, 6) + 1):
    bad = 0
    for P in pops[n]:
        if restriction_counts(P)[(1 << n) - 1] != len(linear_extensions(P)):
            bad += 1
    check("n=%d" % n, bad == 0, "%d bad of %d" % (bad, len(pops[n])))

print("C5  p(x,y) via e(P+{x<y}) == direct count over L(P)")
for n in range(2, min(NMAX, 6) + 1):
    bad = tot = 0
    for P in pops[n]:
        les = linear_extensions(P)
        _, e, ps = pair_data(P)
        for (x, y), p in ps.items():
            tot += 1
            cnt = sum(1 for w in les if w.index(x) < w.index(y))
            if p != Fraction(cnt, len(les)):
                bad += 1
    check("n=%d" % n, bad == 0, "%d bad of %d pairs" % (bad, tot))

print("C6  levels: DFS acyclicity == 'some block order is P-compatible' (brute force)")
for n in range(1, min(NMAX, 5) + 1):
    lat = Lattice(n)
    bad = 0
    for P in pops[n]:
        for i, blocks in enumerate(lat.parts):
            bof = lat.blockof[i]
            k = len(blocks)
            brute = False
            for order in permutations(range(k)):
                posn = [0] * k
                for t, bi in enumerate(order):
                    posn[bi] = t
                if all(posn[bof[a]] <= posn[bof[b]]
                       for a in range(n) for b in range(n) if (P.up[a] >> b) & 1):
                    brute = True
                    break
            if brute != is_level(P, blocks, bof):
                bad += 1
    check("n=%d" % n, bad == 0, "%d bad" % bad)

print("C7  #moves: sum of per-level topological-sort counts == explicit enumeration;")
print("    and for the ANTICHAIN it must be the Fubini number A000670 (external)")
for n in range(1, min(NMAX, 6) + 1):
    lat = Lattice(n)
    bad = 0
    for P in pops[n]:
        lv = levels_of(P, lat)
        if sum(level_move_counts(P, lat, lv).values()) != len(moves_of(P, lat)):
            bad += 1
    check("n=%d counts agree" % n, bad == 0, "%d bad of %d" % (bad, len(pops[n])))
    anti = Poset.from_relations(n, [])
    nm = len(moves_of(anti, lat))
    check("n=%d antichain #moves = %d" % (n, nm), nm == A000670[n],
          "expected %d" % A000670[n])

print("C8  multiplicities: m_X >= 0 and sum over ALL levels == e(P)")
for n in range(1, min(NMAX, 6) + 1):
    lat = Lattice(n)
    bad = neg = 0
    for P in pops[n]:
        e = restriction_counts(P)
        lv = levels_of(P, lat)
        m = multiplicities(P, lat, lv, e)
        if sum(m.values()) != e[(1 << n) - 1]:
            bad += 1
        if any(v < 0 for v in m.values()):
            neg += 1
    check("n=%d" % n, bad == 0 and neg == 0,
          "%d sum-bad, %d with a negative multiplicity" % (bad, neg))

print("C9  spectrum: dim ker(M - lambda I) over Q equals the predicted multiplicity,")
print("    on the ACTUAL transition matrix under the uniform-move weight")


def rank_of(rows, ncol):
    rows = [list(r) for r in rows]
    piv = 0
    for c in range(ncol):
        p = None
        for r in range(piv, len(rows)):
            if rows[r][c] != 0:
                p = r
                break
        if p is None:
            continue
        rows[piv], rows[p] = rows[p], rows[piv]
        inv = rows[piv][c]
        rows[piv] = [v / inv for v in rows[piv]]
        for r in range(len(rows)):
            if r != piv and rows[r][c] != 0:
                f = rows[r][c]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[piv])]
        piv += 1
        if piv == len(rows):
            break
    return piv


for n in range(2, min(NMAX, 5) + 1):
    lat = Lattice(n)
    bad = tested = 0
    for P in pops[n]:
        les = linear_extensions(P)
        if len(les) > 40:
            continue
        idx = {w: i for i, w in enumerate(les)}
        mvs = moves_of(P, lat)
        N = len(les)
        M = [[Fraction(0) for _ in range(N)] for _ in range(N)]
        for mv in mvs:
            for w in les:
                M[idx[w]][idx[act(mv, w)]] += Fraction(1, len(mvs))
        lv = levels_of(P, lat)
        e = restriction_counts(P)
        mult = multiplicities(P, lat, lv, e)
        mc = level_move_counts(P, lat, lv)
        lam = {}
        for X in lv:
            tot = 0
            for Y in lv:
                if X in lat.refiners[Y]:
                    tot += mc[Y]
            lam[X] = Fraction(tot, len(mvs))
        want = {}
        for X in lv:
            if mult[X]:
                want[lam[X]] = want.get(lam[X], 0) + mult[X]
        tested += 1
        for val, mu in want.items():
            rows = [[M[i][j] - (val if i == j else 0) for j in range(N)] for i in range(N)]
            if N - rank_of(rows, N) != mu:
                bad += 1
    check("n=%d" % n, bad == 0, "%d bad eigenvalue multiplicities over %d posets" % (bad, tested))

print("C10 majority relation: totality/acyclicity computed two ways agree")
for n in range(2, min(NMAX, 5) + 1):
    bad = 0
    for P in pops[n]:
        _, _, ps = pair_data(P)
        edges, tf, ac, L = majority_relation(P, ps)
        if tf:
            if len(edges) != n * (n - 1) // 2:
                bad += 1
            if ac:
                pos = {x: i for i, x in enumerate(L)}
                if any(pos[a] > pos[b] for (a, b) in edges):
                    bad += 1
    check("n=%d" % n, bad == 0, "%d bad" % bad)

print()
if FAIL:
    print("FAILURES: %s" % ", ".join(FAIL))
    sys.exit(1)
print("ALL CONTROLS PASS")
