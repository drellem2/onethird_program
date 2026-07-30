#!/usr/bin/env python3
"""
mg-d673 INDEPENDENT AUDIT of mg-ebd8 / 714aceb -- instrument 1 of 3.

POPULATIONS, RECOMPUTED FROM THE DEFINITIONS, SHARING NO CODE WITH THE TARGET
(code/landscape_ebd8/) OR WITH ANY OTHER INSTRUMENT IN THE REPO.

What this establishes:
  A. My own enumeration of posets up to isomorphism, with a TRUE canonical form
     (minimum over the full S_n orbit -- not min() over a frozenset), certified
     against OEIS A000112 (posets on n unlabelled points) and A000608
     (connected posets).  The arc has already produced one silent
     canonicalisation bug of exactly this shape.
  B. |F(P)| (P-compatible ordered set partitions) summed over iso classes,
     against the target's 1, 5, 37, 397, 5757 AND against the number the
     EXISTING pipeline already carries (docs/OneThird-Hodge-Side-Leverage.md
     Theorem L: 1+5+37+397+5757 = 6197 faces; the note's sec 2 sweep quotes
     5757 and 922073 at n=5).
  C. |AC(P)| computed TWO ways that share no logic:
       (i)  set partitions whose quotient digraph is acyclic;
       (ii) the SET OF SUPPORTS of the brute-force enumerated P-compatible
            ordered set partitions.
     (ii) is definition-free: it just enumerates and collects.  Their agreement
     is an independent check on the repo's own "level description" theorem
     (note sec 8, "ours" #2) as well as on the target's level counts
     4, 24, 206, 2353, 37029.
  D. The Pi_n-join failure frequency, against the repo's own 7/16 at n=4 and
     49/63 at n=5 (unified_gate row Q7).
  E. mu(0-hat, 1-hat) of AC(P) against (-1)^(n-1) * (number of cyclic classes
     of linear extensions), i.e. Jenca-Sarkoci's homotopy theorem -- the
     target's "sharp test" P2 -- and the exact population that test covers.
  F. Whether "every block an antichain" alone characterises the M_0 levels, or
     whether acyclicity is independently needed (the target's sec 0 item 2 and
     its L2 table both drop acyclicity from the closed form).

Pure Python 3, no third-party imports.
"""

import sys
from itertools import permutations, combinations
from functools import lru_cache

# --------------------------------------------------------------------------
# A. posets, and a canonical form that really is one
# --------------------------------------------------------------------------


def transitive(rel, n):
    """rel: set of strict pairs (i,j) meaning i < j.  Is it transitive?"""
    for (i, j) in rel:
        for (k, l) in rel:
            if j == k and (i, l) not in rel:
                return False
    return True


def naturally_labelled_posets(n):
    """Every finite poset is isomorphic to one whose order relation is
    contained in the natural order on {0..n-1} (relabel by a linear
    extension).  So enumerating transitive subsets of the strict upper
    triangle hits every isomorphism class at least once."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    m = len(pairs)
    out = []
    for mask in range(1 << m):
        rel = set(pairs[k] for k in range(m) if mask >> k & 1)
        if transitive(rel, n):
            out.append(frozenset(rel))
    return out


def canon(rel, n):
    """CANONICAL FORM: the minimum, over ALL n! relabellings, of the sorted
    tuple of relation pairs.  This is a minimum over the whole orbit, so
    two posets have the same canon iff they are isomorphic.  It is NOT
    min() applied to a frozenset of anything."""
    best = None
    for sigma in permutations(range(n)):
        t = tuple(sorted((sigma[i], sigma[j]) for (i, j) in rel))
        if best is None or t < best:
            best = t
    return best


def iso_classes(n):
    seen = {}
    for rel in naturally_labelled_posets(n):
        c = canon(rel, n)
        if c not in seen:
            seen[c] = rel
    return [seen[c] for c in sorted(seen)]


def leq_matrix(rel, n):
    """reflexive-transitive closure as a boolean matrix"""
    le = [[i == j for j in range(n)] for i in range(n)]
    for (i, j) in rel:
        le[i][j] = True
    return le


def is_connected(rel, n):
    """connected comparability graph"""
    if n == 0:
        return True
    adj = {i: set() for i in range(n)}
    for (i, j) in rel:
        adj[i].add(j)
        adj[j].add(i)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


# --------------------------------------------------------------------------
# B. F(P): P-compatible ordered set partitions, by brute force
# --------------------------------------------------------------------------


def set_partitions(elems):
    elems = list(elems)
    if not elems:
        yield []
        return
    first, rest = elems[0], elems[1:]
    for sub in set_partitions(rest):
        for k in range(len(sub)):
            yield sub[:k] + [[first] + sub[k]] + sub[k + 1:]
        yield [[first]] + sub


def ordered_set_partitions(n):
    for part in set_partitions(range(n)):
        blocks = [frozenset(b) for b in part]
        for perm in permutations(blocks):
            yield tuple(perm)


def compatible(osp, rel):
    """i < j in P  =>  index of i's block <= index of j's block"""
    idx = {}
    for p, B in enumerate(osp):
        for x in B:
            idx[x] = p
    return all(idx[i] <= idx[j] for (i, j) in rel)


def F_of_P(rel, n):
    return [osp for osp in ordered_set_partitions(n) if compatible(osp, rel)]


# --------------------------------------------------------------------------
# C. AC(P) two ways
# --------------------------------------------------------------------------


def quotient_acyclic(part, rel):
    """part: tuple of frozensets.  Build the digraph on blocks induced by the
    relations of P between DISTINCT blocks and test for a directed cycle."""
    idx = {}
    for p, B in enumerate(part):
        for x in B:
            idx[x] = p
    k = len(part)
    succ = {p: set() for p in range(k)}
    for (i, j) in rel:
        if idx[i] != idx[j]:
            succ[idx[i]].add(idx[j])
    # Kahn
    indeg = {p: 0 for p in range(k)}
    for p in succ:
        for q in succ[p]:
            indeg[q] += 1
    q0 = [p for p in range(k) if indeg[p] == 0]
    done = 0
    while q0:
        p = q0.pop()
        done += 1
        for q in succ[p]:
            indeg[q] -= 1
            if indeg[q] == 0:
                q0.append(q)
    return done == k


def AC_by_acyclicity(rel, n):
    out = set()
    for part in set_partitions(range(n)):
        pt = tuple(sorted((frozenset(b) for b in part), key=lambda s: sorted(s)))
        if quotient_acyclic(pt, rel):
            out.add(pt)
    return out


def AC_by_supports(moves):
    """the support of a move is just the underlying unordered partition"""
    return set(tuple(sorted(m, key=lambda s: sorted(s))) for m in moves)


# --------------------------------------------------------------------------
# D. refinement order, Pi_n meet/join, Moebius
# --------------------------------------------------------------------------


def refines(a, b):
    """a refines b: every block of a is inside some block of b"""
    return all(any(A <= B for B in b) for A in a)


def pin_meet(a, b):
    """common refinement"""
    out = []
    for A in a:
        for B in b:
            C = A & B
            if C:
                out.append(C)
    return tuple(sorted(out, key=lambda s: sorted(s)))


def pin_join(a, b):
    """finest common coarsening: union-find"""
    elems = sorted(set().union(*a))
    parent = {x: x for x in elems}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for part in (a, b):
        for B in part:
            bs = sorted(B)
            for x in bs[1:]:
                union(bs[0], x)
    groups = {}
    for x in elems:
        groups.setdefault(find(x), set()).add(x)
    return tuple(sorted((frozenset(v) for v in groups.values()),
                        key=lambda s: sorted(s)))


def moebius_bottom_to_top(elements):
    """mu(0-hat, 1-hat) for the poset `elements` ordered by refinement.
    0-hat = all singletons, 1-hat = one block."""
    els = sorted(elements, key=lambda p: (len(p), sorted(sorted(b) for b in p)))
    n = len(next(iter(elements)) and sorted(set().union(*next(iter(elements)))))
    bot = tuple(sorted((frozenset([x]) for x in range(n)),
                       key=lambda s: sorted(s)))
    top = (frozenset(range(n)),)
    assert bot in elements and top in elements
    # mu(bot, y) by recursion upward
    order = sorted(elements, key=lambda p: -len(p))  # finest first
    mu = {}
    for y in order:
        if y == bot:
            mu[y] = 1
            continue
        if not refines(bot, y):
            continue
        s = 0
        for z in order:
            if z == y:
                continue
            if z in mu and refines(z, y):
                s += mu[z]
        mu[y] = -s
    return mu[top]


# --------------------------------------------------------------------------
# E. linear extensions and cyclic classes
# --------------------------------------------------------------------------


def linear_extensions(rel, n):
    le = [[] for _ in range(n)]
    for (i, j) in rel:
        le[j].append(i)
    out = []

    def rec(prefix, used):
        if len(prefix) == n:
            out.append(tuple(prefix))
            return
        for x in range(n):
            if x in used:
                continue
            if all(p in used for p in le[x]):
                rec(prefix + [x], used | {x})

    rec([], frozenset())
    return out


def cyclic_classes(rel, n):
    """Jenca-Sarkoci Def. 4.1: f ~ g iff f = w w' and g = w' w as words, i.e.
    g is ANY cyclic rotation of f that is again a linear extension.  Union-find
    over all n-1 rotations, so the answer does not depend on the relation being
    transitive on the nose.

    NOTE FOR THE AUDIT: sec 6 item 6 of the target's document describes its own
    instrument as implementing this "as *single* cyclic rotation of the word".
    Its code (identify_lattice.py:316-320) in fact loops k in 1..n-1, i.e. all
    rotations.  The document mis-describes its own instrument, in the safe
    direction.  My first pass implemented the *single*-rotation version the
    document describes and it disagreed with the Moebius function on 5 posets
    to n=5; the all-rotation version agrees.  The Moebius number is the
    independent quantity and it adjudicates in the code's favour."""
    exts = set(linear_extensions(rel, n))
    parent = {w: w for w in exts}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for w in exts:
        for k in range(1, n):
            r = w[k:] + w[:k]
            if r in exts:
                union(w, r)
    return len(set(find(w) for w in exts))


# --------------------------------------------------------------------------
# main sweep
# --------------------------------------------------------------------------

A000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318}      # posets, unlabelled
A000608 = {1: 1, 2: 1, 3: 3, 4: 10, 5: 44, 6: 238}      # connected posets

TARGET_MOVES = {1: 1, 2: 5, 3: 37, 4: 397, 5: 5757}
TARGET_LEVELS = {2: 4, 3: 24, 4: 206, 5: 2353, 6: 37029}
TARGET_CONNECTED = {2: 1, 3: 3, 4: 10, 5: 44, 6: 238}
REPO_JOINFAIL = {4: (7, 16), 5: (49, 63)}


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print("=" * 78)
    print("mg-d673 AUDIT INSTRUMENT 1 -- POPULATIONS, RECOMPUTED FROM SCRATCH")
    print("Canonical form = min over the FULL S_n orbit.  No code shared with")
    print("code/landscape_ebd8/ or any other instrument in the repo.")
    print("=" * 78)
    print()

    bad = 0
    rows = []
    for n in range(1, nmax + 1):
        classes = iso_classes(n)
        nc = len(classes)
        conn = sum(1 for r in classes if is_connected(r, n))
        ok_a = "OK" if A000112.get(n) == nc else "*** MISMATCH ***"
        ok_c = "OK" if A000608.get(n) == conn else "*** MISMATCH ***"
        if A000112.get(n) != nc or A000608.get(n) != conn:
            bad += 1
        rows.append((n, classes, nc, conn))
        print(f"  n={n}: {nc:5d} iso classes  (A000112 says {A000112.get(n)}) {ok_a}"
              f"   | connected {conn:5d}  (A000608 says {A000608.get(n)}) {ok_c}")
    print()
    print("  [certification against two external OEIS sequences: "
          f"{'PASS' if bad == 0 else 'FAIL'}]")
    print()

    # --- B, C, D, E per n ---
    print("-" * 78)
    print("B/C: |F(P)| and |AC(P)| summed over isomorphism classes")
    print("-" * 78)
    print(f"{'n':>2} {'classes':>8} {'sum|F(P)|':>10} {'target':>8} {'':4}"
          f"{'sum|AC|acyc':>12} {'sum|AC|supp':>12} {'target':>8}")
    tot_moves = 0
    all_data = {}
    for (n, classes, nc, conn) in rows:
        sm = 0
        sa = 0
        ss = 0
        per = []
        for rel in classes:
            moves = F_of_P(rel, n)
            acA = AC_by_acyclicity(rel, n)
            acS = AC_by_supports(moves)
            sm += len(moves)
            sa += len(acA)
            ss += len(acS)
            if acA != acS:
                print(f"    *** AC MISMATCH at n={n} rel={sorted(rel)}: "
                      f"acyclic {len(acA)} vs supports {len(acS)}")
                bad += 1
            per.append((rel, moves, acA))
        all_data[n] = per
        tot_moves += sm
        tm = TARGET_MOVES.get(n)
        tl = TARGET_LEVELS.get(n)
        f1 = "OK" if tm is None or tm == sm else "*** MISMATCH ***"
        f2 = "OK" if tl is None or tl == sa else "*** MISMATCH ***"
        if (tm is not None and tm != sm) or (tl is not None and tl != sa):
            bad += 1
        print(f"{n:>2} {nc:>8} {sm:>10} {str(tm):>8} {f1:4} {sa:>12} {ss:>12} "
              f"{str(tl):>8} {f2}")
    print()
    print(f"  sum of |F(P)| over iso classes, n=1..5  = "
          f"{sum(len(m) for n in range(1,6) for (_,m,_) in all_data.get(n,[]))}"
          f"   (repo Theorem L carries 6197)")
    print()

    # --- D: join failure frequency ---
    print("-" * 78)
    print("D: AC(P) closed under the Pi_n MEET (common refinement)?  under the")
    print("   Pi_n JOIN?  -- against the repo's own 7/16 (n=4), 49/63 (n=5)")
    print("-" * 78)
    for n in range(2, min(nmax, 6) + 1):
        meetbad = 0
        joinbad = 0
        for (rel, moves, ac) in all_data[n]:
            mb = jb = False
            acl = sorted(ac)
            for a in acl:
                for b in acl:
                    if pin_meet(a, b) not in ac:
                        mb = True
                    if pin_join(a, b) not in ac:
                        jb = True
                    if mb and jb:
                        break
                if mb and jb:
                    break
            meetbad += mb
            joinbad += jb
        exp = REPO_JOINFAIL.get(n)
        note = ""
        if exp:
            note = (f"   repo says {exp[0]}/{exp[1]} -> "
                    + ("OK" if (joinbad, len(all_data[n])) == exp
                       else "*** MISMATCH ***"))
            if (joinbad, len(all_data[n])) != exp:
                bad += 1
        print(f"  n={n}: meet-failures {meetbad}/{len(all_data[n])}, "
              f"join-failures {joinbad}/{len(all_data[n])}{note}")
    print()

    # --- E: Moebius vs Jenca-Sarkoci ---
    print("-" * 78)
    print("E: mu(0,1) of AC(P) vs (-1)^(n-1) * (# cyclic classes of lin ext)")
    print("   -- Jenca-Sarkoci.  NOTE the population this test actually covers:")
    print("   it is n/a for n<3, so it does NOT cover all 405 posets to n=6.")
    print("-" * 78)
    covered = 0
    p2bad = 0
    for n in range(3, min(nmax, 6) + 1):
        nb = 0
        for (rel, moves, ac) in all_data[n]:
            mu = moebius_bottom_to_top(ac)
            eC = cyclic_classes(rel, n)
            pred = ((-1) ** (n - 1)) * eC
            if mu != pred:
                nb += 1
            covered += 1
        p2bad += nb
        print(f"  n={n}: {nb} bad of {len(all_data[n])}")
    print(f"  posets on which P2 is even DEFINED (n>=3, n<=  {min(nmax,6)}): {covered}")
    print(f"  posets with n>=1 up to n={min(nmax,6)}: "
          f"{sum(len(all_data[n]) for n in range(1, min(nmax,6)+1))}")
    print(f"  posets with n>=2 up to n={min(nmax,6)}: "
          f"{sum(len(all_data[n]) for n in range(2, min(nmax,6)+1))}")
    bad += p2bad
    print()

    # --- E': connected => e_C = e ? ---
    print("-" * 78)
    print("E': is 'cyclic classes' = 'linear extensions' exactly on the")
    print("    CONNECTED posets?  (if it were equal everywhere the test would")
    print("    not discriminate, which is the target's claim)")
    print("-" * 78)
    for n in range(3, min(nmax, 6) + 1):
        cdiff = 0
        ddiff = 0
        dtot = 0
        for (rel, moves, ac) in all_data[n]:
            e = len(linear_extensions(rel, n))
            eC = cyclic_classes(rel, n)
            if is_connected(rel, n):
                if e != eC:
                    cdiff += 1
            else:
                dtot += 1
                if e != eC:
                    ddiff += 1
        print(f"  n={n}: connected with e != e_C: {cdiff} (expect 0)"
              f"   | disconnected: {dtot}, of which e != e_C: {ddiff}"
              f"  -> discriminating on {ddiff} of {dtot}")
    print()

    # --- F: does 'every block an antichain' need acyclicity too? ---
    print("-" * 78)
    print("F: is 'every block is an antichain of P' ALONE the same set as")
    print("   'in AC(P) and every block an antichain'?  The target's sec 0")
    print("   item 2 and its L2 table state the closed form without the")
    print("   acyclicity side condition.")
    print("-" * 78)
    for n in range(2, min(nmax, 6) + 1):
        witness = None
        cnt = 0
        for (rel, moves, ac) in all_data[n]:
            le = leq_matrix(rel, n)
            for part in set_partitions(range(n)):
                pt = tuple(sorted((frozenset(b) for b in part),
                                  key=lambda s: sorted(s)))
                anti = all(not (le[i][j] or le[j][i])
                           for B in pt for i in B for j in B if i != j)
                if anti and pt not in ac:
                    cnt += 1
                    if witness is None:
                        witness = (rel, pt)
        print(f"  n={n}: partitions with all blocks antichains but NOT in AC(P): "
              f"{cnt}")
        if witness and n <= 4:
            rel, pt = witness
            print(f"        witness P = {sorted(rel)}  pi = "
                  f"{'|'.join(''.join(chr(97+x) for x in sorted(B)) for B in pt)}")
    print()

    print("=" * 78)
    print(f"INSTRUMENT 1 TOTAL DISAGREEMENTS: {bad}")
    print("=" * 78)


if __name__ == "__main__":
    main()
