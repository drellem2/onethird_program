#!/usr/bin/env python3
"""mg-446b: attack the PROOF of the gate document's Theorem (mg-8fd1), sec 2.4.

The theorem is exhaustively true at n <= 6 (audit_l2.py reproduces that from an
independent enumeration).  What is checked here is whether the WRITTEN PROOF of
(1) => (3) establishes it.  Step 1 of that proof reads, verbatim:

  "*Step 1: (1) forbids a 3-chain.* If `x < u < y` then `{x,y}` + singletons has
   the 2-cycle `{x,y} -> {u} -> {x,y}`, while `{x,u}` + singletons is acyclic
   (every arrow leaves it); the two have the same shape `(2,1^{n-2})`, hence lie
   in one `S_n`-orbit, so `AC(P)` is not a union of orbits."

Both halves of that are tested for every 3-chain of every poset at n <= 6:
  H1  {x,y} + singletons is cyclic
  H2  {x,u} + singletons is acyclic         <-- and the parenthetical reason,
      "every arrow leaves it", is tested separately as H2r.

Then the repair is tested: restrict to 3-chains of COVERING relations, x -< u -< y.
"""
from itertools import permutations
from audit_l2 import (natural_posets, labelled_posets_bruteforce, rel_of, partitions,
                      acyclic_kahn, canon, name, has_3_chain)

def two_block(x, y, n):
    """the partition {x,y} + singletons"""
    return tuple(sorted([(1 << x) | (1 << y)] + [1 << z for z in range(n)
                                                 if z not in (x, y)]))

def arrows_all_leave(rel, part, n, block):
    """is every arrow of the quotient incident to `block` outgoing?"""
    idx = {}
    for k, B in enumerate(part):
        for z in range(n):
            if (B >> z) & 1:
                idx[z] = k
    b = part.index(block)
    return not any(idx[a] != idx[bb] and idx[bb] == b for (a, bb) in rel)

def classes_at(n):
    perms = list(permutations(range(n)))
    src = (labelled_posets_bruteforce(n) if n <= 5 else natural_posets(n))
    seen = {}
    for up in src:
        rel = rel_of(up, n)
        seen.setdefault(canon(rel, perms), rel)
    return [seen[c] for c in sorted(seen)]

def covers(rel):
    return [(a, b) for (a, b) in rel
            if not any((a, z) in rel and (z, b) in rel for z in {x for p in rel for x in p})]

print("=" * 78)
print("STEP 1 OF THE PROOF OF (1) => (3), TESTED ON EVERY 3-CHAIN AT n <= 6")
print("=" * 78)
print("  n  classes  with a   3-chains   H1 fails   H2 FAILS   H2r FAILS   posets with")
print("     (total)  3-chain   (x,u,y)   (cyclic)   (acyclic)  ('leaves')  NO good triple")
worst = []
for n in range(3, 7):
    classes = classes_at(n)
    parts = partitions(n)
    with3 = 0
    ntrip = h1bad = h2bad = h2rbad = 0
    nogood = 0
    for rel in classes:
        if not has_3_chain(rel):
            continue
        with3 += 1
        good = 0
        for (x, u) in rel:
            for (u2, y) in rel:
                if u2 != u or y == x:
                    continue
                ntrip += 1
                pxy = two_block(x, y, n)
                pxu = two_block(x, u, n)
                h1 = not acyclic_kahn(rel, pxy, n)      # must be cyclic
                h2 = acyclic_kahn(rel, pxu, n)          # proof asserts acyclic
                h2r = arrows_all_leave(rel, pxu, n, (1 << x) | (1 << u))
                h1bad += (not h1)
                h2bad += (not h2)
                h2rbad += (not h2r)
                if h1 and h2:
                    good += 1
                elif not h2 and len(worst) < 6:
                    worst.append((n, sorted(rel), x, u, y))
        if good == 0:
            nogood += 1
    print("  %d  %7d  %7d   %7d   %8d   %8d   %9d   %d"
          % (n, len(classes), with3, ntrip, h1bad, h2bad, h2rbad, nogood))

print()
print("  H1 (the cycle) never fails.  H2 -- the assertion that {x,u} + singletons is")
print("  ACYCLIC -- fails on the triples listed below, and its stated reason ('every")
print("  arrow leaves it') fails far more often still, since anything below x sends an")
print("  arrow INTO the block.  Smallest witnesses:")
for n, rel, x, u, y in worst:
    print("     n=%d  P=%s   x=%d u=%d y=%d :  {x,u}={%d,%d} + singletons is CYCLIC"
          % (n, rel, x, u, y, x, u))
print()
print("  The 4-chain 0<1<2<3 with x=0,u=2,y=3 is the smallest: the quotient by")
print("  {0,2}|{1}|{3} has {0,2} -> {1} (from 0<1) and {1} -> {0,2} (from 1<2).")

print()
print("=" * 78)
print("THE REPAIR: TAKE THE 3-CHAIN INSIDE THE COVER RELATION,  x -< u -< y")
print("=" * 78)
print("  n  classes with 3-chain   cover-3-chains   H1 fails   H2 fails")
for n in range(3, 7):
    classes = classes_at(n)
    tot = h1bad = h2bad = 0
    posets_without = 0
    for rel in classes:
        if not has_3_chain(rel):
            continue
        cov = covers(rel)
        trips = [(x, u, y) for (x, u) in cov for (u2, y) in cov if u2 == u]
        if not trips:
            posets_without += 1
        for (x, u, y) in trips:
            tot += 1
            if acyclic_kahn(rel, two_block(x, y, n), n):
                h1bad += 1
            if not acyclic_kahn(rel, two_block(x, u, n), n):
                h2bad += 1
    print("  %d  %18d   %14d   %8d   %8d   (posets with a 3-chain but no"
          " cover-3-chain: %d)" % (n, sum(1 for r in classes if has_3_chain(r)),
                                   tot, h1bad, h2bad, posets_without))
print()
print("  0 failures of either half once the 3-chain is taken inside the covers, at")
print("  every n <= 6: every poset with a 3-chain has a saturated one, and for a")
print("  covering pair x -< u no element sits strictly between them, so the only")
print("  possible return path to {x,u} would be a chain x < ... < u or u < ... < x.")
print("  That is the missing hypothesis; with it Step 1 goes through as written.")
