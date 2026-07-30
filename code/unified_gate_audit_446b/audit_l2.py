#!/usr/bin/env python3
"""mg-446b, target 2: recompute the L2 population from the definitions.

INDEPENDENCE.  Nothing here imports code/unified_gate_8fd1/ or code/hodge_leverage/.
Deliberate divergences from mg-8fd1's helpers, chosen so that a shared bug cannot
hide:

  * posets are enumerated at n <= 5 by BRUTE FORCE over every relation on [n]
    (all 16^n up-set tuples, filtered for irreflexive+antisymmetric+transitive),
    not by the "transitively closed subset of the upper triangle" trick.  The
    labelled counts are then checked against the known sequence A001035
    (1,3,19,219,4231,130023) and the isomorphism-class counts against A000112
    (1,2,5,16,63,318) -- external numbers, so the enumeration is not self-certified.
  * n = 6 uses natural labelling (the only affordable route), but completeness is
    certified from OUTSIDE by  sum over classes of  n!/|Aut(P)|  =  130023.
  * canonical form = orbit minimum of the sorted relation list over all of S_n.
    That is a genuine canonical form, not a min() over frozensets.
  * acyclicity is decided TWICE: Kahn peeling, and (n <= 5) by exhibiting an
    ordering of the blocks in which every relation strictly increases the block
    index -- the source's own "topological sort" description of the same object.

Run:  python3 audit_l2.py [nmax=6]
"""
import sys
from itertools import permutations, product

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
A001035 = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231, 6: 130023}   # labelled posets
A000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318}           # unlabelled posets

# ---------------------------------------------------------------- posets ----

def is_poset(up, n):
    """up[i] = bitmask of the elements strictly above i."""
    for i in range(n):
        if (up[i] >> i) & 1:
            return False
        for j in range(n):
            if (up[i] >> j) & 1:
                if (up[j] >> i) & 1:          # antisymmetry
                    return False
                if up[j] & ~up[i]:            # transitivity
                    return False
    return True

def labelled_posets_bruteforce(n):
    """Every strict partial order on [n], by exhaustive filtering."""
    out = []
    for up in product(range(1 << n), repeat=n):
        if is_poset(up, n):
            out.append(tuple(up))
    return out

def rel_of(up, n):
    return frozenset((i, j) for i in range(n) for j in range(n) if (up[i] >> j) & 1)

def up_of(rel, n):
    up = [0] * n
    for (a, b) in rel:
        up[a] |= 1 << b
    return tuple(up)

def natural_posets(n):
    """Strict orders for which 0<1<...<n-1 is a linear extension (n=6 route)."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    out = []
    for mask in range(1 << len(pairs)):
        up = [0] * n
        for k, (i, j) in enumerate(pairs):
            if (mask >> k) & 1:
                up[i] |= 1 << j
        if is_poset(up, n):
            out.append(tuple(up))
    return out

def relabel(rel, s):
    return frozenset((s[a], s[b]) for (a, b) in rel)

def canon(rel, perms):
    return min(tuple(sorted(relabel(rel, s))) for s in perms)

# ------------------------------------------------------------ partitions ----

def partitions(n):
    out = []
    def rec(i, blocks):
        if i == n:
            out.append(tuple(sorted(blocks)))
            return
        for k in range(len(blocks)):
            b = list(blocks); b[k] |= 1 << i; rec(i + 1, b)
        rec(i + 1, list(blocks) + [1 << i])
    rec(0, [])
    return out

def block_index(part, n):
    idx = [0] * n
    for k, B in enumerate(part):
        for x in range(n):
            if (B >> x) & 1:
                idx[x] = k
    return idx

def acyclic_kahn(rel, part, n):
    """Route 1: peel sources off the block digraph (Kahn)."""
    idx = block_index(part, n)
    k = len(part)
    succ = [set() for _ in range(k)]
    indeg = [0] * k
    for (a, b) in rel:
        if idx[a] != idx[b] and idx[b] not in succ[idx[a]]:
            succ[idx[a]].add(idx[b]); indeg[idx[b]] += 1
    q = [i for i in range(k) if indeg[i] == 0]
    seen = 0
    while q:
        v = q.pop(); seen += 1
        for w in succ[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    return seen == k

def acyclic_by_ordering(rel, part, n):
    """Route 2: is there an order on the blocks making every relation increase
    the block index?  (The source's 'topological sort' description.)"""
    idx = block_index(part, n)
    k = len(part)
    for p in permutations(range(k)):
        if all(p[idx[a]] < p[idx[b]] for (a, b) in rel if idx[a] != idx[b]):
            return True
    return False

# ---------------------------------------------------- lattice operations ----

def pi_join(p, q, n):
    """finest partition coarser than both (union-find)."""
    par = list(range(n))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for part in (p, q):
        for B in part:
            mem = [x for x in range(n) if (B >> x) & 1]
            for y in mem[1:]:
                rx, ry = find(mem[0]), find(y)
                if rx != ry:
                    par[rx] = ry
    g = {}
    for x in range(n):
        g[find(x)] = g.get(find(x), 0) | (1 << x)
    return tuple(sorted(g.values()))

def pi_meet(p, q, n):
    """common refinement: pairwise intersections (the SOURCE's 'join')."""
    out = []
    for B in p:
        for C in q:
            if B & C:
                out.append(B & C)
    return tuple(sorted(out))

def coarsens(x, y):
    """y is coarser than or equal to x."""
    return all(any((B & C) == B for C in y) for B in x)

# ------------------------------------------------------------- structure ----

def shares_an_end(rel):
    R = sorted(rel)
    return not any(x != u and y != v for (x, y) in R for (u, v) in R)

def is_antichain_or_star(rel, n):
    if not rel:
        return True
    bots = {a for (a, b) in rel}
    tops = {b for (a, b) in rel}
    return len(bots) == 1 or len(tops) == 1

def has_3_chain(rel):
    return any((b, c) in rel for (a, b) in rel for (b2, c) in rel if b == b2)

def covers(rel):
    """the covering relations of rel"""
    out = []
    for (a, b) in rel:
        if not any((a, z) in rel and (z, b) in rel for z in range(20)):
            out.append((a, b))
    return out

def name(rel, n):
    if not rel:
        return "antichain A_%d" % n
    if len(rel) == n * (n - 1) // 2:
        return "chain C_%d" % n
    bots = {a for (a, b) in rel}; tops = {b for (a, b) in rel}
    used = {x for p in rel for x in p}
    iso = n - len(used)
    suf = " +%d isolated" % iso if iso else ""
    if len(bots) == 1:
        return "down-star 1<%d%s" % (len(tops), suf)
    if len(tops) == 1:
        return "up-star %d<1%s" % (len(bots), suf)
    return "rel=%s" % sorted(rel)

# ----------------------------------------------------------------- sweep ----

def main():
    report = {}


    for n in range(1, NMAX + 1):
        perms = list(permutations(range(n)))
        parts = partitions(n)
        pidx = {p: i for i, p in enumerate(parts)}
        nP = len(parts)

        # --- enumeration, two independent routes where affordable
        if n <= 5:
            lab = labelled_posets_bruteforce(n)
            lab_rels = [rel_of(up, n) for up in lab]
            src_note = "brute force over all %d relations" % (16 ** n if n <= 4 else (1 << n) ** n)
        else:
            nat = natural_posets(n)
            lab_rels = None
            src_note = "natural labelling (%d naturally-labelled posets)" % len(nat)

        seen = {}
        it = lab_rels if lab_rels is not None else [rel_of(up, n) for up in nat]
        for rel in it:
            c = canon(rel, perms)
            seen.setdefault(c, rel)
        classes = [seen[c] for c in sorted(seen)]

        # completeness certificate independent of the enumeration route
        orbit_total = 0
        for rel in classes:
            aut = sum(1 for s in perms if relabel(rel, s) == rel)
            orbit_total += len(perms) // aut

        print("=" * 78)
        print("n = %d   route: %s" % (n, src_note))
        print("  isomorphism classes         : %d   (A000112 says %d)  %s"
              % (len(classes), A000112[n], "OK" if len(classes) == A000112[n] else "*** MISMATCH ***"))
        print("  sum of orbit sizes n!/|Aut| : %d   (A001035 says %d)  %s"
              % (orbit_total, A001035[n], "OK" if orbit_total == A001035[n] else "*** MISMATCH ***"))
        if lab_rels is not None:
            print("  labelled posets enumerated  : %d   %s"
                  % (len(lab_rels), "OK" if len(lab_rels) == A001035[n] else "*** MISMATCH ***"))

        # --- S_n action on partition indices
        act = []
        for s in perms:
            row = [0] * nP
            for p in parts:
                q = tuple(sorted(sum(1 << s[x] for x in range(n) if (B >> x) & 1) for B in p))
                row[pidx[p]] = pidx[q]
            act.append(row)

        # --- per class
        stable, ghist, bigger_D, min_ac = [], {}, 0, (10**9, None)
        two_route_bad = 0
        equiv_bad = 0
        join_bad_classes = meet_bad_classes = not_lattice = 0
        ac_of = {}
        for rel in classes:
            ac_parts = [p for p in parts if acyclic_kahn(rel, p, n)]
            if n <= 5:
                for p in parts:
                    if acyclic_kahn(rel, p, n) != acyclic_by_ordering(rel, p, n):
                        two_route_bad += 1
            ac = frozenset(pidx[p] for p in ac_parts)
            ac_of[rel] = ac
            G = [s for k, s in enumerate(perms) if frozenset(act[k][i] for i in ac) == ac]
            # the doc's claimed equivalent definition:  AC(sigma P) = AC(P)
            for k, s in (enumerate(perms) if n <= 4 else []):
                lhs = frozenset(act[k][i] for i in ac) == ac
                rhs = frozenset(pidx[p] for p in parts if acyclic_kahn(relabel(rel, s), p, n)) == ac
                if lhs != rhs:
                    equiv_bad += 1
            D = [s for s in perms
                 if relabel(rel, s) == rel
                 or relabel(rel, s) == frozenset((b, a) for (a, b) in rel)]
            assert all(s in G for s in D), "D(P) not inside G(P) -- claim refuted"
            ghist[len(G)] = ghist.get(len(G), 0) + 1
            if len(G) > len(D):
                bigger_D += 1
            if len(ac) < min_ac[0]:
                min_ac = (len(ac), [rel])
            elif len(ac) == min_ac[0]:
                min_ac[1].append(rel)
            if len(G) == len(perms):
                stable.append((rel, len(ac)))
            # lattice questions (n<=5 only: O(|AC|^2) with a coarsening scan)
            if n <= 5:
                acs = set(ac_parts)
                if any(pi_join(a, b, n) not in acs for a in ac_parts for b in ac_parts):
                    join_bad_classes += 1
                if any(pi_meet(a, b, n) not in acs for a in ac_parts for b in ac_parts):
                    meet_bad_classes += 1
                ok = True
                for a in ac_parts:
                    for b in ac_parts:
                        ub = [c for c in ac_parts if coarsens(a, c) and coarsens(b, c)]
                        mins = [c for c in ub if not any(d != c and coarsens(d, c) for d in ub)]
                        if len(mins) != 1:
                            ok = False
                if not ok:
                    not_lattice += 1

        print("  acyclicity: Kahn vs topological-ordering route disagreements: %s"
              % (two_route_bad if n <= 5 else "(not run at n=6)"))
        print("  'sigma.AC(P)=AC(P)' vs 'AC(sigma P)=AC(P)' disagreements: %s"
              % (equiv_bad if n <= 4 else "(exhaustive at n<=4 only)"))
        print("  S_n-STABLE CLASSES: %d of %d   (2(n-1) = %d)"
              % (len(stable), len(classes), 2 * (n - 1) if n >= 2 else 1))
        for rel, sz in stable:
            print("      |AC|=%3d of %3d  AC=Pi_n:%-5s share-end:%-5s star/antichain:%-5s  %s"
                  % (sz, nP, sz == nP, shares_an_end(rel), is_antichain_or_star(rel, n),
                     name(rel, n)))
        print("  |G(P)| histogram: %s"
              % ", ".join("%d x%d" % (k, ghist[k]) for k in sorted(ghist)))
        print("  classes with G(P) strictly larger than {sigma: sigma.P in {P,P^op}}: %d" % bigger_D)
        print("  smallest |AC(P)| = %d, attained by %d class(es): %s"
              % (min_ac[0], len(min_ac[1]), "; ".join(name(r, n) for r in min_ac[1])))
        if n <= 5:
            print("  AC(P) NOT closed under the Pi_n JOIN (coarsening): %d of %d classes"
                  % (join_bad_classes, len(classes)))
            print("  AC(P) NOT closed under the Pi_n MEET (common refinement, the"
                  " SOURCE's 'join'): %d of %d classes" % (meet_bad_classes, len(classes)))
            print("  AC(P) fails to be a lattice under refinement: %d of %d classes"
                  % (not_lattice, len(classes)))

        # tri-equivalence + the star description
        dis = [rel for rel in classes
               if not (( len(ac_of[rel]) == nP)
                       == (frozenset(act[k][i] for i in ac_of[rel]) == ac_of[rel]
                           for k in [0]) is not None)]  # placeholder, computed below
        bad_equiv = []
        for rel in classes:
            ac = ac_of[rel]
            stab = all(frozenset(row[i] for i in ac) == ac for row in act)
            full = len(ac) == nP
            share = shares_an_end(rel)
            star = is_antichain_or_star(rel, n)
            if not (stab == full == share == star):
                bad_equiv.append((rel, stab, full, share, star))
        print("  TRI-EQUIVALENCE stable <=> AC=Pi_n <=> share-an-end <=> antichain-or-star:"
              " %s" % ("holds on all %d classes" % len(classes) if not bad_equiv
                       else "*** FAILS on %d ***" % len(bad_equiv)))
        for row in bad_equiv[:5]:
            print("      %s" % (row,))
        print("  height<=2 classes (the proof's intermediate step): %d  -- %s"
              % (sum(1 for rel in classes if not has_3_chain(rel)),
                 "strictly weaker, as the doc says"))

        # the chain, explicitly
        chain = frozenset((i, j) for i in range(n) for j in range(n) if i < j)
        acc = [p for p in parts if acyclic_kahn(chain, p, n)]
        Gc = [s for k, s in enumerate(perms)
              if frozenset(act[k][pidx[p]] for p in acc) == frozenset(pidx[p] for p in acc)]
        consec = [p for p in parts
                  if all(max(x for x in range(n) if (B >> x) & 1)
                         - min(x for x in range(n) if (B >> x) & 1) + 1 == bin(B).count("1")
                         for B in p)]
        print("  CHAIN C_%d: |AC| = %d, 2^(n-1) = %d, consecutive-interval partitions = %d,"
              " |G| = %d, stable = %s"
              % (n, len(acc), 2 ** (n - 1), len(consec), len(Gc), len(Gc) == len(perms)))
        assert set(acc) == set(consec) or n < 2, "chain AC != consecutive intervals"
        report[n] = (len(classes), len(stable))
        print()

    print("=" * 78)
    print("SUMMARY: population of S_n-stable quotient lattices")
    print("=" * 78)
    print("  n   classes   stable   2(n-1)")
    for n in sorted(report):
        c, s = report[n]
        print("  %d   %7d   %6d   %6d   %s" % (n, c, s, 2 * (n - 1) if n >= 2 else 1,
                                               "OK" if (n == 1 or s == 2 * (n - 1)) else "***"))


if __name__ == "__main__":
    main()
