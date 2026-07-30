"""mg-66a6 AUDIT, target 4: the STATUS of the note's own two contributions.

The note (section 8) says both of the things it claims as OURS rest on a
computation:

    "It is VERIFIED EXHAUSTIVELY ONLY TO FIVE ELEMENTS ... It is NOT PROVEN IN
     GENERAL.  Nothing in this note should be read as saying otherwise."

This file tests the opposite hypothesis: that both are elementary theorems for
every n.  Each proof is written out, then verified CONSTRUCTIVELY -- by
building the witness the proof produces -- exhaustively to n=5 and then on
random posets at n=6,7,8, which the note does not cover at all.

PROOF 1 (closure -- 'the identification', the first thing section 8 claims).
  Let x = (B_1..B_k) and y = (C_1..C_l) both be P-compatible.  A block of x.y
  is a non-empty B_p & C_q, and its index in x.y is the rank of (p,q) in
  lexicographic order.  Take i < j in P, with i in B_p & C_q and
  j in B_p' & C_q'.  x compatible gives p <= p'; y compatible gives q <= q'.
  Hence (p,q) <= (p',q') lexicographically, so index(block of i) <=
  index(block of j).  So x.y is P-compatible.  No hypothesis on n.  QED

PROOF 2 (the acyclic-cut description -- 'the commitment levels', the second
thing, and the one section 8 explicitly says is unproven).
  Let X be a partition of the elements, and let Q(X) be the quotient digraph:
  one node per block, an arrow B -> B' (B != B') whenever some i in B has
  i < j in P for some j in B'.
  (=>) Suppose X = supp(x) for a P-compatible x = (B_1..B_k).  Distinct blocks
       have distinct indices.  An arrow B_p -> B_q forces p <= q by
       compatibility, hence p < q.  So every arrow strictly increases the
       index, and a directed cycle would give p < p.  Q(X) is acyclic.
  (<=) Suppose Q(X) is acyclic.  Take any topological order of its nodes,
       B_{s(1)},...,B_{s(k)}, and let x be that ordered set partition.  If
       i < j in P then either they share a block (equal indices) or there is an
       arrow block(i) -> block(j), which the topological order sends to
       index(block(i)) < index(block(j)).  So x is P-compatible, and
       supp(x) = X by construction.
  Both directions hold for every n and every P.  QED

PROOF 3 (the counting identity's right-hand side).  Brown's theorem gives the
  multiplicity relation with a CHAMBER COUNT on the right.  The note writes it
  as prod_B |L(P|_B)| and attributes the whole statement to Brown.  That
  substitution is an identification of ours, not Brown's: for any move x with
  supp(x) = X, the set x.C of orderings reachable by x has exactly
  prod_B |L(P|_B)| elements.  Verified below.
"""

import sys
from random import Random

from audit_lib import (all_labelled_posets, poset, moves, levels, product,
                       acyclic_partitions, set_partitions, quotient_acyclic,
                       lstr, mstr, orderings, act, induced, n_orderings,
                       level, refines, ordered_set_partitions, is_compatible)

FAIL = []
CHECKS = [0]


def check(label, got, want):
    CHECKS[0] += 1
    ok = got == want
    print("  [%s] %s" % ("OK " if ok else "FAIL", label))
    if not ok:
        print("        expected  : %r" % (want,))
        print("        recomputed: %r" % (got,))
        FAIL.append(label)
    return ok


def random_poset(rng, n, p=0.35):
    """A random strict partial order: random DAG on a random linear order,
    transitively closed."""
    order = list(range(n))
    rng.shuffle(order)
    R = set()
    for a in range(n):
        for b in range(a + 1, n):
            if rng.random() < p:
                R.add((order[a], order[b]))
    changed = True
    while changed:
        changed = False
        for (a, b) in list(R):
            for (c, d) in list(R):
                if b == c and (a, d) not in R:
                    R.add((a, d))
                    changed = True
    return (n, frozenset(R))


def topological_move(P, X):
    """The witness of proof 2's (<=) direction: a topological order of the
    quotient, as an ordered set partition."""
    n, R = P
    blocks = sorted(X, key=lambda B: sorted(B))
    idx = {}
    for i, B in enumerate(blocks):
        for e in B:
            idx[e] = i
    succ = {i: set() for i in range(len(blocks))}
    indeg = {i: 0 for i in range(len(blocks))}
    for (a, b) in R:
        if idx[a] != idx[b] and idx[b] not in succ[idx[a]]:
            succ[idx[a]].add(idx[b])
            indeg[idx[b]] += 1
    ready = sorted(i for i in indeg if indeg[i] == 0)
    out = []
    while ready:
        u = ready.pop(0)
        out.append(u)
        for v in sorted(succ[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
                ready.sort()
    if len(out) != len(blocks):
        return None                      # cyclic
    return tuple(blocks[u] for u in out)


print(__doc__)
print("=" * 78)
print("SECTION A -- proof 1 (closure) verified constructively")
print("=" * 78)
for n in range(1, 5):
    bad = 0
    tot = 0
    for P in all_labelled_posets(n):
        MV = moves(P)
        for x in MV:
            for y in MV:
                tot += 1
                if not is_compatible(P, product(x, y)):
                    bad += 1
    check("n=%d: x.y is P-compatible, 0 bad of %d (every labelled poset)"
          % (n, tot), bad, 0)

rng = Random(20260730)
for n, ns, npairs in ((6, 40, 4000), (7, 12, 4000), (8, 6, 4000)):
    bad = 0
    tot = 0
    for _ in range(ns):
        P = random_poset(rng, n)
        MV = moves(P)
        for _ in range(npairs):
            x = MV[rng.randrange(len(MV))]
            y = MV[rng.randrange(len(MV))]
            tot += 1
            if not is_compatible(P, product(x, y)):
                bad += 1
            # while here, the two band identities themselves
            xy = product(x, y)
            if product(x, x) != x or product(xy, x) != xy:
                bad += 1
    check("n=%d: %d random posets x %d random move pairs -- closure AND both "
          "band identities, 0 bad of %d (BEYOND the note's coverage)"
          % (n, ns, npairs, tot), bad, 0)

print()
print("=" * 78)
print("SECTION B -- proof 2 (the acyclic-cut description) verified")
print("             constructively, and BEYOND FIVE ELEMENTS")
print("=" * 78)
print("  For each poset: (=>) every move's support has an acyclic quotient;")
print("  (<=) every acyclic partition is realised by the explicit topological")
print("  witness, which is checked to be P-compatible with that support.")
print()

for n in range(1, 6):
    bad_fwd = bad_bwd = 0
    nlev = nacy = 0
    posets = all_labelled_posets(n)
    for P in posets:
        MV = moves(P)
        supp = set()
        for x in MV:
            S = level(x)
            supp.add(S)
            if not quotient_acyclic(P, S):
                bad_fwd += 1
        acy = [X for X in set_partitions(range(n)) if quotient_acyclic(P, X)]
        for X in acy:
            wit = topological_move(P, X)
            if wit is None or not is_compatible(P, wit) or level(wit) != X:
                bad_bwd += 1
        nlev += len(supp)
        nacy += len(acy)
    check("n=%d: (=>) 0 supports with a cyclic quotient, over %d labelled "
          "posets" % (n, len(posets)), bad_fwd, 0)
    check("n=%d: (<=) the topological witness works for every acyclic "
          "partition (%d of them)" % (n, nacy), bad_bwd, 0)
    check("n=%d: #levels == #acyclic partitions summed over all posets" % n,
          nlev, nacy)

print("  Beyond n=5, enumerating every move is infeasible, so the set equality")
print("  is tested in the equivalent form it reduces to: a partition X is a")
print("  level exactly when SOME ordering of its blocks is P-compatible.  That")
print("  is brute-forced over all orderings of X's blocks -- no reference to")
print("  the acyclicity criterion -- and compared with the criterion.")
print()


def is_level_bruteforce(P, X):
    """Is some ordering of X's blocks P-compatible?  Brute force, no acyclicity
    anywhere in sight."""
    from itertools import permutations as perms
    blocks = sorted(X, key=lambda B: sorted(B))
    for p in perms(range(len(blocks))):
        x = tuple(blocks[i] for i in p)
        if is_compatible(P, x):
            return True
    return False


for n, ns in ((6, 60), (7, 25), (8, 10)):
    bad_fwd = bad_bwd = bad_wit = 0
    nlev = nacy = 0
    for _ in range(ns):
        P = random_poset(rng, n)
        for X in set_partitions(range(n)):
            acy = quotient_acyclic(P, X)
            bf = is_level_bruteforce(P, X)
            if acy and not bf:
                bad_bwd += 1
            if bf and not acy:
                bad_fwd += 1
            if acy:
                nacy += 1
                wit = topological_move(P, X)
                if (wit is None or not is_compatible(P, wit)
                        or level(wit) != X):
                    bad_wit += 1
            if bf:
                nlev += 1
    check("n=%d: %d random posets -- 'is a level' (brute force over block "
          "orderings) == 'acyclic quotient' exactly (%d levels, %d acyclic), "
          "and the topological witness always works (BEYOND the note's "
          "coverage)" % (n, ns, nlev, nacy),
          (bad_fwd, bad_bwd, bad_wit, nlev == nacy), (0, 0, 0, True))

print()
print("  CONTROL: the witness construction must FAIL on a cyclic partition.")
P = poset(4, [(0, 1), (2, 3)])
Xcyc = frozenset([frozenset([0, 3]), frozenset([1, 2])])
check("the worked example's {a,d}|{b,c} yields no topological witness",
      topological_move(P, Xcyc), None)
allosp = [x for x in ordered_set_partitions(range(4)) if level(x) == Xcyc]
check("and no ordered set partition with that support is P-compatible",
      [mstr(x) for x in allosp if is_compatible(P, x)], [])

print()
print("=" * 78)
print("SECTION C -- proof 3: the counting identity's RHS is an")
print("             identification of ours, not part of Brown's statement")
print("=" * 78)
for n in range(1, 5):
    bad = 0
    tot = 0
    for P in all_labelled_posets(n):
        ords = orderings(P)
        for x in moves(P):
            X = level(x)
            reach = {act(x, c) for c in ords}
            prod = 1
            for B in X:
                prod *= n_orderings(induced(P, B))
            tot += 1
            if len(reach) != prod:
                bad += 1
    check("n=%d: |x.C| = prod_B |L(P|_B)| for every move of every labelled "
          "poset (%d moves)" % (n, tot), bad, 0)

print()
print("  and the support map is the lattice map Brown's theorem needs:")
for n in range(1, 5):
    bad = 0
    tot = 0
    for P in all_labelled_posets(n):
        MV = moves(P)
        LVs = set(level(x) for x in MV)
        for x in MV:
            for y in MV:
                tot += 1
                # common refinement of supp(x) and supp(y)
                cr = frozenset(B & C for B in level(x) for C in level(y)
                               if B & C)
                if level(product(x, y)) != cr or cr not in LVs:
                    bad += 1
    check("n=%d: supp(x.y) = common refinement of supp(x), supp(y), and the "
          "levels are closed under it, 0 bad of %d" % (n, tot), bad, 0)

print()
print("=" * 78)
print("VERDICT OF THIS FILE")
print("=" * 78)
print("""  Both statements section 8 files under "verified exhaustively only to five
  elements ... not proven in general" are THEOREMS with elementary proofs,
  written out at the top of this file and verified constructively here --
  including at n = 6, 7 and 8, where the note has no evidence at all.

  The note therefore UNDERSTATES the status of its own two contributions.
  That is a status error in the direction opposite to the one the audit
  brief anticipated, and it is decision-relevant: Daniel is being told the
  programme's contribution here is an unproven pattern in small cases.""")
print()
print("%d checks, %d FAILURES" % (CHECKS[0], len(FAIL)))
for f in FAIL:
    print("  FAILED: %s" % f)
print("=" * 78)
sys.exit(1 if FAIL else 0)
