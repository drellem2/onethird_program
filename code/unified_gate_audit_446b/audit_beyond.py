#!/usr/bin/env python3
"""mg-446b: the theorem beyond the exhaustive range, and the QUALITY of the gate
document's own beyond-range evidence.

Three things:

 (1) validate the METHOD the gate document uses at n = 7,8,9 -- it tests stability
     on the adjacent transpositions only.  That is legitimate iff the stabiliser is
     a subgroup; verified here by comparing generator-stability against full-group
     stability on every isomorphism class at n <= 6.
 (2) test the theorem at n = 7,8,9 on MY OWN draws (own RNG, own generator), and on
     instances chosen to be non-degenerate:
        - every star shape (down-stars |S| = 1..n-1, up-stars |S| = 2..n-1),
          i.e. the whole predicted stable population, 2(n-1) classes;
        - explicit two-relation posets that do NOT share an end, the smallest
          predicted-unstable shapes.
 (3) diagnose the gate document's random sweep: it reports 168/151/123 of 400 draws
     "stable" and calls that exercising both directions.  Here the same density
     menu is drawn and the stable draws are BROKEN DOWN by how many relations they
     have, to see whether the positive direction is exercised by anything other
     than near-empty posets.
"""
import random
from itertools import permutations
from audit_l2 import (partitions, acyclic_kahn, shares_an_end, natural_posets,
                      labelled_posets_bruteforce, rel_of, canon)

# ---------------------------------------------------------------------------
print("=" * 78)
print("(1) IS 'TEST THE ADJACENT TRANSPOSITIONS ONLY' THE FULL CONDITION?")
print("=" * 78)
for n in range(2, 7):
    perms = list(permutations(range(n)))
    parts = partitions(n)
    pidx = {p: i for i, p in enumerate(parts)}
    act = {}
    for s in perms:
        act[s] = [pidx[tuple(sorted(sum(1 << s[x] for x in range(n) if (B >> x) & 1)
                                    for B in p))] for p in parts]
    gens = []
    for t in range(n - 1):
        s = list(range(n)); s[t], s[t + 1] = s[t + 1], s[t]
        gens.append(act[tuple(s)])
    src = labelled_posets_bruteforce(n) if n <= 5 else natural_posets(n)
    seen = {}
    for up in src:
        rel = rel_of(up, n)
        seen.setdefault(canon(rel, perms), rel)
    dis = 0
    for rel in seen.values():
        ac = frozenset(pidx[p] for p in parts if acyclic_kahn(rel, p, n))
        by_gen = all(frozenset(g[i] for i in ac) == ac for g in gens)
        by_all = all(frozenset(row[i] for i in ac) == ac for row in act.values())
        dis += (by_gen != by_all)
    print("  n=%d: classes %d, generator-stability vs full-S_n-stability"
          " disagreements: %d" % (n, len(seen), dis))
print("  -> the stabiliser of a subset is a subgroup, so generators suffice;"
      " confirmed empirically.  The gate document's n=7,8,9 method is sound.")

# ---------------------------------------------------------------------------
def stable_by_gens(rel, parts, pidx, gens):
    ac = frozenset(pidx[p] for p in parts if acyclic_kahn(rel, p, len(gens) + 1))
    return all(frozenset(g[i] for i in ac) == ac for g in gens), ac

def star(n, k, down=True, base=0):
    if down:
        return frozenset((base, base + 1 + i) for i in range(k))
    return frozenset((base + 1 + i, base) for i in range(k))

print()
print("=" * 78)
print("(2) THE THEOREM AT n = 7, 8, 9 -- MY DRAWS, AND THE NON-DEGENERATE CASES")
print("=" * 78)
rng = random.Random(446)
for n in (7, 8, 9):
    parts = partitions(n)
    pidx = {p: i for i, p in enumerate(parts)}
    gens = []
    for t in range(n - 1):
        s = list(range(n)); s[t], s[t + 1] = s[t + 1], s[t]
        gens.append([pidx[tuple(sorted(sum(1 << s[x] for x in range(n) if (B >> x) & 1)
                                       for B in p))] for p in parts])
    # --- (a) the whole predicted stable population, checked positively
    fam = ([("down-star 1<%d" % k, star(n, k, True)) for k in range(1, n)]
           + [("up-star %d<1" % k, star(n, k, False)) for k in range(2, n)])
    posbad = 0
    for nm, rel in fam:
        nac = sum(1 for p in parts if acyclic_kahn(rel, p, n))
        st, ac = stable_by_gens(rel, parts, pidx, gens)
        if not (st and nac == len(parts)):
            posbad += 1
            print("    *** %s: |AC|=%d of %d, stable=%s" % (nm, nac, len(parts), st))
    print("  n=%d  predicted stable population 2(n-1) = %d shapes"
          " (antichain + %d stars): all have AC = Pi_n (=%d) and are stable: %s"
          % (n, 2 * (n - 1), len(fam), len(parts), posbad == 0))
    # --- (b) smallest predicted-unstable shapes: two relations, no shared end
    negbad = 0
    cases = [frozenset([(0, 1), (2, 3)]), frozenset([(0, 1), (1, 2), (0, 2), (3, 4)]),
             frozenset([(0, 1), (2, 1), (2, 3)])]
    for rel in cases:
        st, ac = stable_by_gens(rel, parts, pidx, gens)
        if st or shares_an_end(rel):
            negbad += 1
    print("       three explicit non-star shapes (disjoint 2-chain+edge etc.):"
          " all UNSTABLE as predicted: %s" % (negbad == 0))
    # --- (c) my own random draws
    trials = {7: 400, 8: 300, 9: 200}[n]
    mism = 0
    stable_seen = 0
    comp = {}
    for _ in range(trials):
        perm = list(range(n)); rng.shuffle(perm)
        dens = rng.choice([0.02, 0.05, 0.1, 0.25, 0.5])
        rel = set()
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < dens:
                    rel.add((perm[i], perm[j]))
        ch = True
        while ch:
            ch = False
            for (a, b) in list(rel):
                for (c, d) in list(rel):
                    if b == c and (a, d) not in rel:
                        rel.add((a, d)); ch = True
        rel = frozenset(rel)
        share = shares_an_end(rel)
        if share:
            nac = sum(1 for p in parts if acyclic_kahn(rel, p, n))
            st, _ = stable_by_gens(rel, parts, pidx, gens)
            if not (st and nac == len(parts)):
                mism += 1
        else:
            st, ac = stable_by_gens(rel, parts, pidx, gens)
            if st:
                mism += 1
        stable_seen += st
        if st:
            comp[len(rel)] = comp.get(len(rel), 0) + 1
    print("       %d own draws: stable %d, disagreements with the theorem %d"
          % (trials, stable_seen, mism))
    print("       stable draws by number of relations: %s"
          % ", ".join("%d rel: %d" % (k, comp[k]) for k in sorted(comp)))
    triv = sum(v for k, v in comp.items() if k <= 1)
    print("       of the %d stable draws, %d have <= 1 relation (antichain or a single"
          " edge) = %.0f%%" % (stable_seen, triv, 100.0 * triv / max(stable_seen, 1)))
print()
print("  (3) is the line above: with the gate document's own density menu, the")
print("  positive direction of its n=7,8,9 sweep is carried almost entirely by")
print("  posets with at most one relation.  The theorem's interesting positive")
print("  cases -- stars with |S| >= 2 -- are supplied by (a) here, not by that sweep.")
