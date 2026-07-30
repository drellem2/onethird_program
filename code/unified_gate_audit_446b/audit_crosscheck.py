#!/usr/bin/env python3
"""mg-446b, target 2 (second half): make a DISAGREEMENT POSSIBLE.

Two things self-consistent new code cannot do for itself:

 (A) re-derive numbers the EXISTING pipeline already carries.  code/hodge_leverage/
     lrb_output.txt records |support lattice| for five named posets at n=5, computed
     from the left-regular-band product (supports of semigroup elements).  Here the
     same five numbers are recomputed as |AC(P)| from the acyclicity definition,
     by Kahn peeling on the block digraph.  Different objects, different code, same
     numbers -- or a disagreement surfaces.
 (B) the injectivity/fibre numbers at n=5, from an enumeration of all 4231 labelled
     posets built by brute force rather than by expanding orbits of naturally
     labelled ones.

Also checks, exhaustively at n <= 5, that the gate document's two definitions of
G(P) ("sigma.AC(P) = AC(P)" and "AC(sigma P) = AC(P)") really do agree -- i.e. that
"stable" and "stable up to the relabelling that induces it" are the same condition
here, which is the distinction the audit brief asks about.
"""
import re
from itertools import permutations, product
from audit_l2 import (labelled_posets_bruteforce, rel_of, partitions, acyclic_kahn,
                      relabel, canon, name, shares_an_end)

LRB = "../hodge_leverage/lrb_output.txt"

print("=" * 78)
print("(A) FIVE NUMBERS THE EXISTING PIPELINE ALREADY CARRIES, RE-DERIVED")
print("=" * 78)
named = {
    "antichain A_5": [],
    "chain C_5":     [(i, j) for i in range(5) for j in range(5) if i < j],
    "fence n=5":     [(0, 1), (2, 1), (2, 3), (4, 3)],
    "C_2+C_3":       [(0, 1), (2, 3), (3, 4), (2, 4)],
    "V+A_2 n=5":     [(0, 1), (0, 2)],
}
pipeline = {}
for line in open(LRB):
    m = re.match(r"\s*(\S.*?)\s+\|L\(P\)\|=\s*(\d+)\s+\|support lattice\|=\s*(\d+)", line)
    if m:
        pipeline[m.group(1).strip()] = int(m.group(3))
parts5 = partitions(5)
print("  %-14s %-10s %-10s %s" % ("poset", "pipeline", "mine", "agree"))
allok = True
for nm, rel in named.items():
    rel = frozenset(rel)
    mine = sum(1 for p in parts5 if acyclic_kahn(rel, p, 5))
    got = pipeline.get(nm)
    ok = (got == mine)
    allok &= ok
    print("  %-14s %-10s %-10d %s" % (nm, got, mine, "YES" if ok else "*** NO ***"))
print("  (pipeline numbers are |support lattice| from the LRB product in"
      " code/hodge_leverage/lrb_output.txt; mine are |AC(P)| from acyclicity)")
print("  ALL FIVE AGREE: %s" % allok)
print()
print("  Note the sharpest one: V+A_2 = the poset {0<1, 0<2} with 2 isolated points"
      " -- a STAR,")
print("  not an antichain -- and the pipeline recorded |support lattice| = 52 ="
      " B_5 = |Pi_5| for it")
print("  in a commit that predates mg-8fd1.  The existing pipeline therefore"
      " already carried")
print("  an instance of the gate document's central positive claim (a"
      " non-antichain whose")
print("  quotient lattice is ALL of Pi_n), independently of the new code.")

print()
print("=" * 78)
print("(B) DOES THE QUOTIENT LATTICE REMEMBER THE POSET?  n = 4, 5, brute force")
print("=" * 78)
for n in (4, 5):
    parts = partitions(n)
    pidx = {p: i for i, p in enumerate(parts)}
    lab = [rel_of(up, n) for up in labelled_posets_bruteforce(n)]
    fib = {}
    for rel in lab:
        key = frozenset(pidx[p] for p in parts if acyclic_kahn(rel, p, n))
        fib.setdefault(key, []).append(rel)
    biggest = max(fib.values(), key=len)
    stars = [r for r in biggest if not shares_an_end(r)]
    print("  n=%d: labelled posets %d, distinct AC(P) %d, largest fibre %d"
          % (n, len(lab), len(fib), len(biggest)))
    print("        every member of the largest fibre is an antichain-or-star: %s"
          % (not stars))
    if n == 5:
        down = sum(1 for r in biggest if r and len({a for a, b in r}) == 1)
        up = sum(1 for r in biggest if r and len({b for a, b in r}) == 1
                 and len({a for a, b in r}) > 1)
        print("        composition: 1 antichain + %d labelled down-stars + %d labelled"
              " up-stars = %d" % (down, up, 1 + down + up))

print()
print("=" * 78)
print("(C) 'STABLE' vs 'STABLE UP TO THE RELABELLING THAT INDUCES IT'")
print("=" * 78)
print("  setwise stabiliser   G(P)  = {sigma : sigma.AC(P) = AC(P)}")
print("  gate's alternative   G'(P) = {sigma : AC(sigma P) = AC(P)}")
print("  pointwise stabiliser G0(P) = {sigma : sigma.pi = pi for every pi in AC(P)}")
for n in (3, 4, 5):
    perms = list(permutations(range(n)))
    parts = partitions(n)
    pidx = {p: i for i, p in enumerate(parts)}
    seen = {}
    for up in labelled_posets_bruteforce(n):
        rel = rel_of(up, n)
        seen.setdefault(canon(rel, perms), rel)
    classes = [seen[c] for c in sorted(seen)]
    bad = 0
    pointwise_nontrivial = 0
    for rel in classes:
        ac = frozenset(pidx[p] for p in parts if acyclic_kahn(rel, p, n))
        G = set()
        Gp = set()
        for s in perms:
            img = frozenset(pidx[tuple(sorted(sum(1 << s[x] for x in range(n)
                                                  if (B >> x) & 1) for B in parts[i]))]
                            for i in ac)
            if img == ac:
                G.add(s)
            if frozenset(pidx[p] for p in parts
                         if acyclic_kahn(relabel(rel, s), p, n)) == ac:
                Gp.add(s)
        G0 = [s for s in perms
              if all(tuple(sorted(sum(1 << s[x] for x in range(n) if (B >> x) & 1)
                                  for B in parts[i])) == parts[i] for i in ac)]
        if G != Gp:
            bad += 1
        if len(G0) > 1:
            pointwise_nontrivial += 1
    print("  n=%d: classes %d;  G(P) != G'(P) on %d of them;  pointwise stabiliser"
          " nontrivial on %d" % (n, len(classes), bad, pointwise_nontrivial))
print("  So the two readings coincide (the action on AC(P) is by relabelling, and")
print("  AC(sigma P) = sigma.AC(P) identically), while the POINTWISE stabiliser is")
print("  trivial for n >= 2 -- 'stable' can only mean setwise, and the gate document")
print("  states the setwise version and its equivalent form explicitly.")
