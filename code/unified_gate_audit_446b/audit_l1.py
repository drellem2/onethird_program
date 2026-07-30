#!/usr/bin/env python3
"""mg-446b, target 1 (computational half): what Proposition N2 establishes, and
what the gate document's "where it bites" sentence says instead.

(A) N2 IS AN AMBIENT STATEMENT, RE-DERIVED.  For every isomorphism class of poset
    at n <= 5 and every composition alpha of n with >= 2 parts, the set of
    P-compatible ordered partitions of shape alpha is tested for S_n-INVARIANCE
    (the ambient module has the ordered partitions as a permutation basis, so the
    span is a submodule iff the set is invariant).  This re-derives the number the
    existing pipeline carries in code/hodge_leverage/theorems_output.txt SS N2:
    exactly one poset per n, the antichain.

(B) WHAT THE WIDENED SENTENCE WOULD NEED.  The gate document says (line 22 and
    ledger row Q2) that "the similarity to S_n cannot be an S_n-module structure,
    at any n, for any non-antichain", and (SS1.3) that reading it as "the face space
    carries an S_n-module structure whose isotypic pieces do the work" is "false for
    every non-antichain, proven, all n".  N2 proves no such thing: its subject is
    the AMBIENT action on OP_alpha.  Exhibited here for a non-antichain at n = 3:
    an S_3-module structure on the chamber space that COMMUTES with Delta_AT, so its
    isotypic decomposition block-diagonalises the operator -- while N2 holds for
    that same poset.  Exact integer arithmetic, no floating point.
"""
from fractions import Fraction
from itertools import permutations, product
from audit_l2 import (labelled_posets_bruteforce, rel_of, canon, name)

# ------------------------------------------------------------------ (A) ----
def compositions(n, minparts=2):
    out = []
    def rec(rem, cur):
        if rem == 0:
            if len(cur) >= minparts:
                out.append(tuple(cur))
            return
        for k in range(1, rem + 1):
            rec(rem - k, cur + [k])
    rec(n, [])
    return out

def ordered_partitions_of_shape(n, alpha):
    """all ordered set partitions (B_1..B_k) with |B_i| = alpha_i, as tuples of
    frozensets in order."""
    elems = list(range(n))
    out = []
    def rec(rest, i, cur):
        if i == len(alpha):
            out.append(tuple(cur))
            return
        from itertools import combinations
        for c in combinations(sorted(rest), alpha[i]):
            rec(rest - set(c), i + 1, cur + [frozenset(c)])
    rec(set(elems), 0, [])
    return out

def compatible(rel, op):
    idx = {}
    for k, B in enumerate(op):
        for x in B:
            idx[x] = k
    return all(idx[a] <= idx[b] for (a, b) in rel)

print("=" * 78)
print("(A) N2 RE-DERIVED FROM THE DEFINITION -- AND IT IS A STATEMENT ABOUT THE")
print("    AMBIENT ACTION ON ALL ORDERED PARTITIONS OF SHAPE alpha")
print("=" * 78)
print("  n  classes   classes where EVERY shape-alpha face set is S_n-invariant"
      "   which")
for n in range(2, 6):
    perms = list(permutations(range(n)))
    seen = {}
    for up in labelled_posets_bruteforce(n):
        rel = rel_of(up, n)
        seen.setdefault(canon(rel, perms), rel)
    classes = [seen[c] for c in sorted(seen)]
    alphas = compositions(n)
    ops = {a: ordered_partitions_of_shape(n, a) for a in alphas}
    good = []
    for rel in classes:
        allinv = True
        for a in alphas:
            F = set(op for op in ops[a] if compatible(rel, op))
            assert F, "N2's 'never empty' half fails -- a linear extension exists"
            inv = True
            for s in perms:
                for op in F:
                    img = tuple(frozenset(s[x] for x in B) for B in op)
                    if img not in F:
                        inv = False
                        break
                if not inv:
                    break
            if not inv:
                allinv = False
                break
        if allinv:
            good.append(rel)
    print("  %d  %7d   %-56d %s"
          % (n, len(classes), len(good), ", ".join(name(r, n) for r in good)))
print("  pipeline (code/hodge_leverage/theorems_output.txt SS N2) records 1 per n,")
print("  the antichain, for n = 2..5 -- reproduced above from a disjoint route.")
print()
print("  So the gate document's SS1.2 report of N2 -- universally quantified over all")
print("  finite posets and all alpha with >= 2 parts, hypothesis 'OP_alpha transitive")
print("  and F_alpha(P) nonempty proper', conclusion 'span F_alpha(P) is not an")
print("  S_n-submodule of Ind_{S_alpha}^{S_n}1' -- is FAITHFUL to what is provable,")
print("  and the n <= 5 sweep is indeed a check and not the evidence.")

# ------------------------------------------------------------------ (B) ----
print()
print("=" * 78)
print("(B) THE WIDENED SENTENCE, TESTED: A NON-AMBIENT S_3-MODULE STRUCTURE ON A")
print("    NON-ANTICHAIN'S CHAMBER SPACE THAT COMMUTES WITH Delta_AT")
print("=" * 78)
n = 3
rel = frozenset([(0, 1)])                     # 0 < 1, element 2 isolated
print("  P = {0 < 1} with 2 isolated  (a non-antichain, so N2 applies to it)")
# chambers = linear extensions, as tuples
chambers = [p for p in permutations(range(n))
            if all(p.index(a) < p.index(b) for (a, b) in rel)]
print("  chambers (linear extensions): %s" % (chambers,))
def adj(c, d):
    diff = [i for i in range(n) if c[i] != d[i]]
    return len(diff) == 2 and diff[1] == diff[0] + 1 and \
        c[diff[0]] == d[diff[1]] and c[diff[1]] == d[diff[0]]
N = len(chambers)
A = [[1 if adj(chambers[i], chambers[j]) else 0 for j in range(N)] for i in range(N)]
D = [sum(A[i]) for i in range(N)]
Delta = [[(D[i] if i == j else 0) - A[i][j] for j in range(N)] for i in range(N)]
print("  Delta_AT = D - A on the AT graph:")
for row in Delta:
    print("      %s" % row)
# exact eigenvectors of the path P_3 Laplacian
vecs = {0: [1, 1, 1], 1: [1, 0, -1], 3: [1, -2, 1]}
def mv(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]
for lam, v in vecs.items():
    got = mv(Delta, v)
    assert got == [lam * x for x in v], (lam, v, got)
print("  exact eigenpairs verified: %s" % ", ".join(
    "lambda=%d on %s" % (l, v) for l, v in vecs.items()))
# rho(sigma) = diag(1, sgn, sgn) in the eigenbasis, pushed to the chamber basis
def sgn(s):
    inv = sum(1 for i in range(n) for j in range(i + 1, n) if s[i] > s[j])
    return -1 if inv % 2 else 1
B = [[Fraction(vecs[l][i]) for l in (0, 1, 3)] for i in range(3)]   # columns = eigvecs
def inv3(M):
    det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
           - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
           + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    assert det != 0
    C = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            m = [[M[r][c] for c in range(3) if c != i] for r in range(3) if r != j]
            C[i][j] = ((-1) ** (i + j)) * (m[0][0] * m[1][1] - m[0][1] * m[1][0]) / det
    return C
Binv = inv3(B)
def mm(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def rho(s):
    Dg = [[Fraction(0)] * 3 for _ in range(3)]
    Dg[0][0] = Fraction(1); Dg[1][1] = Fraction(sgn(s)); Dg[2][2] = Fraction(sgn(s))
    return mm(mm(B, Dg), Binv)
perms3 = list(permutations(range(3)))
hom = all(rho(s) == mm(rho(t), rho(u)) for t in perms3 for u in perms3
          for s in [tuple(t[u[i]] for i in range(3))])
Df = [[Fraction(x) for x in row] for row in Delta]
comm = all(mm(rho(s), Df) == mm(Df, rho(s)) for s in perms3)
print("  rho: S_3 -> GL(C^chambers), rho(sigma) = diag(1, sgn, sgn) in the eigenbasis")
print("      is a group homomorphism (all 36 pairs, exact rationals): %s" % hom)
print("      commutes with Delta_AT exactly: %s" % comm)
print("      isotypic decomposition: trivial on span(1,1,1), sign on span{(1,0,-1),"
      "(1,-2,1)}")
print("      -> a PROPER decomposition into Delta_AT-invariant isotypic pieces,"
      " 1 + 2")
print()
print("  and for the SAME poset, N2 holds -- every shape-alpha face set with >= 2"
      " parts:")
alphas = compositions(3)
ops = {a: ordered_partitions_of_shape(3, a) for a in alphas}
for a in alphas:
    F = set(op for op in ops[a] if compatible(rel, op))
    inv = all(tuple(frozenset(s[x] for x in Bk) for Bk in op) in F
              for s in perms3 for op in F)
    print("      alpha=%-9s |OP_alpha|=%-3d |F_alpha(P)|=%-3d nonempty proper: %-5s"
          "  S_3-invariant: %s"
          % (str(a), len(ops[a]), len(F), 0 < len(F) < len(ops[a]), inv))
print()
print("  CONCLUSION.  N2 is exactly what the gate document's SS1.2 says it is, and")
print("  its 'one route, not the leg' answer is right.  But the sentence the gate")
print("  document nominates as the negative's BITE -- 'the similarity to S_n cannot")
print("  be an S_n-module structure, at any n, for any non-antichain' (line 22, and")
print("  ledger row Q2 labelled PROVEN) -- drops the word AMBIENT, and what is left")
print("  is not what N2 proves: above is a non-antichain, an honest S_3-module")
print("  structure on its face/chamber space, and a block-diagonalisation of Delta_AT")
print("  by its isotypic pieces.  The repair is one word: 'cannot be an S_n-module")
print("  structure INHERITED FROM THE AMBIENT ACTION ON ORDERED PARTITIONS'.")
