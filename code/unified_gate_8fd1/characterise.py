#!/usr/bin/env python3
"""
mg-8fd1, L2 (part 2): pin the characterisation down, and check the two things
the word "lattice" is doing in the phrase "the quotient lattice".

(A) tri-equivalence, exhaustively over every isomorphism class at n <= 6:
        (i)   AC(P) is S_n-stable
        (ii)  AC(P) = Pi_n  (every partition is acyclic)
        (iii) any two strict relations of P share their bottom or their top
    plus the intermediate fact used in the proof of (i) => (iii): stability
    forces height <= 2 (no 3-element chain).

(B) is AC(P) a sub-join-semilattice of Pi_n?  is it a lattice at all under the
    refinement order?  Witnesses printed.

(C) is P |-> AC(P) injective?  (i.e. does the quotient lattice remember P?)
    This is what makes G(P) bigger than {sigma : sigma.P in {P, P^op}}.
"""

from itertools import permutations
from quotient_symmetry import (iso_classes, set_partitions, acyclic, join,
                               relabel_poset, dual, poset_name,
                               all_pairs_share_an_end,
                               naturally_labelled_posets)


def has_3_chain(rel):
    return any((a, b) in rel and (b, c) in rel
               for (a, b) in rel for (b2, c) in rel if b == b2)


def part_str(p, n):
    return "|".join("".join(str(x) for x in range(n) if (B >> x) & 1)
                    for B in sorted(p, key=lambda B: min(
                        x for x in range(n) if (B >> x) & 1)))


def section_A(nmax):
    print("=" * 74)
    print("(A) THE TRI-EQUIVALENCE   stable <=> AC(P) = Pi_n <=> share-an-end")
    print("=" * 74)
    print(" n   classes  stable  AC=Pi_n  share-end  height<=2  all agree")
    for n in range(1, nmax + 1):
        perms = list(permutations(range(n)))
        parts = set_partitions(n)
        pidx = {p: i for i, p in enumerate(parts)}
        act = []
        for s in perms:
            row = [0] * len(parts)
            for p in parts:
                q = frozenset(sum(1 << s[x] for x in range(n) if (B >> x) & 1)
                              for B in p)
                row[pidx[p]] = pidx[q]
            act.append(row)
        classes = iso_classes(n)
        c_stab = c_full = c_share = c_h2 = 0
        agree = True
        for rel in classes:
            ac = frozenset(pidx[p] for p in parts if acyclic(rel, p))
            stab = all(frozenset(row[i] for i in ac) == ac for row in act)
            full = (len(ac) == len(parts))
            share = all_pairs_share_an_end(rel)
            h2 = not has_3_chain(rel)
            c_stab += stab
            c_full += full
            c_share += share
            c_h2 += h2
            if not (stab == full == share):
                agree = False
            if stab and not h2:
                agree = False
        print(" %d   %7d  %6d  %7d  %9d  %9d  %s"
              % (n, len(classes), c_stab, c_full, c_share, c_h2,
                 "YES" if agree else "*** NO ***"))
    print()
    print("  (height<=2 is strictly weaker than the other three, as it must be:")
    print("   it is an intermediate step of the proof, not an equivalent.)")
    print()


def section_B(nmax):
    print("=" * 74)
    print("(B) IS AC(P) A LATTICE, AND IS IT ONE INSIDE Pi_n?")
    print("=" * 74)
    witness = None          # first found overall, i.e. at the smallest n
    for n in range(2, nmax + 1):
        parts = set_partitions(n)
        classes = iso_classes(n)
        bad_join = 0
        not_lattice = 0
        for rel in classes:
            ac = [p for p in parts if acyclic(rel, p)]
            acs = set(ac)
            jb = False
            for a in ac:
                for b in ac:
                    if join(a, b, n) not in acs:
                        jb = True
                        if witness is None:
                            witness = (rel, a, b, join(a, b, n), n)
            bad_join += jb
            # lattice test under refinement order (0hat = singletons):
            # every pair needs a unique MINIMAL common coarsening inside AC
            def coarsens(x, y):        # y is coarser than or equal to x
                return all(any((B & C) == B for C in y) for B in x)
            ok = True
            for a in ac:
                for b in ac:
                    ub = [c for c in ac if coarsens(a, c) and coarsens(b, c)]
                    minimal = [c for c in ub
                               if not any(d is not c and coarsens(d, c)
                                          for d in ub)]
                    if len(minimal) != 1:
                        ok = False
            if not ok:
                not_lattice += 1
        print(" n=%d: classes=%3d   AC(P) NOT join-closed in Pi_n: %3d"
              "   AC(P) not a lattice under refinement: %d"
              % (n, len(classes), bad_join, not_lattice))
    if witness:
        rel, a, b, j, n = witness
        print()
        print(" first witness for join-failure (n=%d):  P with relations %s"
              % (n, sorted(rel)))
        print("   %s  acyclic, %s  acyclic, but their Pi_n-join %s  is CYCLIC"
              % (part_str(a, n), part_str(b, n), part_str(j, n)))

    # the document's own named witness, checked explicitly
    doc = frozenset([(0, 2), (1, 3)])          # a<c, b<d  with a,b,c,d = 0,1,2,3
    p1 = frozenset([0b1001, 0b0010, 0b0100])   # {a,d}|{b}|{c}
    p2 = frozenset([0b0001, 0b0110, 0b1000])   # {a}|{b,c}|{d}
    print()
    print(" the document's own named witness, P = {a<c, b<d} at n=4:")
    print("   %s acyclic=%s ; %s acyclic=%s ; join = %s acyclic=%s"
          % (part_str(p1, 4), acyclic(doc, p1),
             part_str(p2, 4), acyclic(doc, p2),
             part_str(join(p1, p2, 4), 4), acyclic(doc, join(p1, p2, 4))))
    print("   -- so {a,d}|{b,c} is not merely a bad REFINEMENT of an acyclic")
    print("      partition, it is the Pi_n-JOIN of two acyclic ones.")
    print()


def section_C(nmax):
    print("=" * 74)
    print("(C) DOES THE QUOTIENT LATTICE REMEMBER THE POSET?")
    print("=" * 74)
    print(" n   labelled posets   distinct AC(P)   largest fibre   |{P,P^op}|=2")
    for n in range(2, nmax + 1):
        perms = list(permutations(range(n)))
        parts = set_partitions(n)
        pidx = {p: i for i, p in enumerate(parts)}
        labelled = set()
        for rel in naturally_labelled_posets(n):
            for s in perms:
                labelled.add(relabel_poset(rel, s))
        fib = {}
        for rel in labelled:
            key = frozenset(pidx[p] for p in parts if acyclic(rel, p))
            fib.setdefault(key, []).append(rel)
        biggest = max(fib.values(), key=len)
        n_pairs = sum(1 for v in fib.values() if len(v) <= 2)
        print(" %d   %15d   %14d   %13d   %d of %d fibres"
              % (n, len(labelled), len(fib), len(biggest), n_pairs, len(fib)))
    print()
    print(" a maximal fibre at n=%d (posets sharing one quotient lattice):" % nmax)
    for rel in sorted(biggest, key=lambda r: sorted(r))[:8]:
        print("     %s" % (sorted(rel) if rel else "empty (antichain)"))
    print(" ... %d posets in that fibre." % len(biggest))
    print()


def section_D(trials=400, seed=20260730):
    """The theorem is proven for all n; n <= 6 is exhaustive. Here we test the
    equivalence (i) <=> (iii) at n = 7, 8, 9 on random posets, where we have no
    exhaustive evidence. Stability is checked on the adjacent transpositions,
    which generate S_n, so this is the full condition and not a sample of it."""
    import random
    rng = random.Random(seed)
    print("=" * 74)
    print("(D) THE EQUIVALENCE BEYOND THE EXHAUSTIVE RANGE (random posets)")
    print("=" * 74)
    for n in (7, 8, 9):
        parts = set_partitions(n)
        pidx = {p: i for i, p in enumerate(parts)}
        gens = []
        for t in range(n - 1):
            s = list(range(n))
            s[t], s[t + 1] = s[t + 1], s[t]
            row = [0] * len(parts)
            for p in parts:
                q = frozenset(sum(1 << s[x] for x in range(n) if (B >> x) & 1)
                              for B in p)
                row[pidx[p]] = pidx[q]
            gens.append(row)
        mismatch = 0
        stable_seen = 0
        for _ in range(trials):
            # random poset: random subset of a random linear order, closed up
            perm = list(range(n))
            rng.shuffle(perm)
            dens = rng.choice([0.02, 0.05, 0.1, 0.25, 0.5])
            rel = set()
            for i in range(n):
                for j in range(i + 1, n):
                    if rng.random() < dens:
                        rel.add((perm[i], perm[j]))
            changed = True
            while changed:                       # transitive closure
                changed = False
                for (a, b) in list(rel):
                    for (c, d) in list(rel):
                        if b == c and (a, d) not in rel:
                            rel.add((a, d))
                            changed = True
            rel = frozenset(rel)
            ac = frozenset(pidx[p] for p in parts if acyclic(rel, p))
            stab = all(frozenset(g[i] for i in ac) == ac for g in gens)
            stable_seen += stab
            if stab != all_pairs_share_an_end(rel):
                mismatch += 1
            if stab and len(ac) != len(parts):
                mismatch += 1
        print(" n=%d  %d random posets (%d partitions each): stable=%d,"
              "  disagreements with the theorem: %d"
              % (n, trials, len(parts), stable_seen, mismatch))
    print()


if __name__ == "__main__":
    section_A(6)
    section_B(5)
    section_C(5)
    section_D()
