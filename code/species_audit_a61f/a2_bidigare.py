"""A2 -- BIDIGARE, re-run, and the question of how many controls T3 really has.

mg-7d75 section 2.2 rebuilds Aguiar-Mahajan Theorem 10.13 -- "(Bidigare).  The
descent algebra is isomorphic to (Sigma[n]^{S_n})^{op}" -- from both
definitions and compares structure constants.  It reports

    n     iso/A  anti/A  iso/B  anti/B
    3         4       0      0       4
    4        54       0      0      54
    5       472       0      0     472

and concludes: "Four candidate identifications were run ... and exactly two
hold and two fail, so the comparison is discriminating.  The two that hold are
the two that say ANTI-ISOMORPHISM, which is what the theorem says."

A2a/A2b/A2c rebuild both algebras here, again from the definitions, and
reproduce the table.  A2d asks the question the audit brief demands about a
candidate space: are those four candidates four independent hypotheses, or two
hypotheses written twice?
"""

import sys
from itertools import permutations
from kerna61f import set_compositions, tits, orbits, act_comp

bad = 0
NMAX = 5


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


# ---------------------------------------------------------------------------
# the invariant algebra ( k Sigma_n )^{S_n}
# ---------------------------------------------------------------------------

def comp_type(F):
    return tuple(len(B) for B in F)


def sigma_side(n):
    S = set_compositions(range(n))
    idx = {F: i for i, F in enumerate(S)}
    types = sorted({comp_type(F) for F in S})
    tpos = {t: i for i, t in enumerate(types)}
    m = len(types)
    # C[a][b][c] : coefficient of O_c in O_a . O_b
    C = [[dict() for _ in range(m)] for _ in range(m)]
    consistent = True
    byt = [[] for _ in range(m)]
    for F in S:
        byt[tpos[comp_type(F)]].append(F)
    for a in range(m):
        for b in range(m):
            counts = {}
            for F in byt[a]:
                for G in byt[b]:
                    k = comp_type(tits(F, G))
                    counts[k] = counts.get(k, 0) + 1
            coef = {}
            for k, v in counts.items():
                c = tpos[k]
                if v % len(byt[c]):
                    consistent = False
                coef[c] = v // len(byt[c])
            C[a][b] = coef
    return types, C, consistent, len(S)


# ---------------------------------------------------------------------------
# Solomon's descent algebra inside k S_n, from permutations and descent sets
# ---------------------------------------------------------------------------

def descents(w):
    return frozenset(i for i in range(1, len(w)) if w[i - 1] > w[i])


def sol_side(n, convention):
    """convention 'A': (uv)(i) = u(v(i)).   'B': (uv)(i) = v(u(i))."""
    W = list(permutations(range(1, n + 1)))
    des = {w: descents(w) for w in W}
    subsets = []
    for m in range(1 << (n - 1)):
        subsets.append(frozenset(i for i in range(1, n) if m >> (i - 1) & 1))
    subsets.sort(key=lambda s: (len(s), sorted(s)))
    spos = {T: i for i, T in enumerate(subsets)}
    members = {T: [w for w in W if des[w] <= T] for T in subsets}

    def mul(u, v):
        if convention == "A":
            return tuple(u[v[i] - 1] for i in range(n))
        return tuple(v[u[i] - 1] for i in range(n))

    k = len(subsets)
    C = [[dict() for _ in range(k)] for _ in range(k)]
    closed = True
    for a, T in enumerate(subsets):
        for b, S in enumerate(subsets):
            vec = {}
            for u in members[T]:
                for v in members[S]:
                    z = mul(u, v)
                    vec[z] = vec.get(z, 0) + 1
            # must be constant on descent classes
            f = {}
            for w in W:
                d = des[w]
                c = vec.get(w, 0)
                if d in f and f[d] != c:
                    closed = False
                f[d] = c
            coef = {}
            for c, T2 in enumerate(subsets):
                s = 0
                for D in subsets:
                    if T2 <= D:
                        s += (-1) ** (len(D) - len(T2)) * f.get(D, 0)
                if s:
                    coef[c] = s
            C[a][b] = coef
    return subsets, C, closed, len(W)


def comp_to_subset(alpha, n):
    s = 0
    out = []
    for x in alpha[:-1]:
        s += x
        out.append(s)
    return frozenset(out)


# ---------------------------------------------------------------------------
hdr("A2a/A2b  both algebras built from their definitions, no shared code")

print("   n  |Sigma_n|  #orbits  2^(n-1)  orbit products constant  |S_n|"
      "  d_T closed A  d_T closed B")
side = {}
for n in range(1, NMAX + 1):
    types, Cs, cons, nsig = sigma_side(n)
    sA, CA, clA, nsn = sol_side(n, "A")
    sB, CB, clB, _ = sol_side(n, "B")
    side[n] = (types, Cs, sA, CA, sB, CB)
    bad += (not cons) + (not clA) + (not clB)
    bad += (len(types) != 2 ** (n - 1)) + (len(sA) != 2 ** (n - 1))
    print("  %2d  %9d  %7d  %7d  %22s  %5d  %12s  %12s"
          % (n, nsig, len(types), 2 ** (n - 1), cons, nsn, clA, clB))
print()
print("  Orbits of set compositions are indexed by their BLOCK-SIZE SEQUENCE,")
print("  i.e. by the compositions of n, and the orbit sums close under the")
print("  Tits product.  Solomon's d_T = sum over des(w) <= T close under both")
print("  composition conventions.  Both algebras have dimension 2^(n-1).")
print()

# ---------------------------------------------------------------------------
hdr("A2c  the comparison -- four candidate identifications")

print("  Candidate: O_alpha <-> d_{T(alpha)}, T(alpha) the partial sums.")
print("  iso  : c^g_{a,b}(Sigma) = c^g_{a,b}(Sol)")
print("  anti : c^g_{a,b}(Sigma) = c^g_{b,a}(Sol)")
print()
print("   n   iso/A  anti/A   iso/B  anti/B     (mismatching structure constants)")
res = {}
for n in range(2, NMAX + 1):
    types, Cs, sA, CA, sB, CB = side[n]
    spos = {T: i for i, T in enumerate(sA)}
    perm = [spos[comp_to_subset(t, n)] for t in types]
    row = {}
    for conv, Cd in (("A", CA), ("B", CB)):
        for kind in ("iso", "anti"):
            miss = 0
            for a in range(len(types)):
                for b in range(len(types)):
                    lhs = Cs[a][b]
                    rhs = Cd[perm[a]][perm[b]] if kind == "iso" \
                        else Cd[perm[b]][perm[a]]
                    # both sides re-indexed by COMPOSITION index before compare
                    l = {c: v for c, v in lhs.items()}
                    inv = {perm[i]: i for i in range(len(types))}
                    r = {inv[c]: v for c, v in rhs.items()}
                    for c in set(l) | set(r):
                        if l.get(c, 0) != r.get(c, 0):
                            miss += 1
            row[(conv, kind)] = miss
    res[n] = row
    print("  %2d  %6d  %6d  %6d  %6d"
          % (n, row[("A", "iso")], row[("A", "anti")],
             row[("B", "iso")], row[("B", "anti")]))
print()
holds = [k for k in res[NMAX] if all(res[n][k] == 0 for n in res)]
fails = [k for k in res[NMAX] if not all(res[n][k] == 0 for n in res)]
print("  HOLDS at every n in 2..%d : %s" % (NMAX, sorted(holds)))
print("  FAILS somewhere           : %s" % sorted(fails))
print()
tgt = {2: (0, 0, 0, 0), 3: (4, 0, 0, 4), 4: (54, 0, 0, 54), 5: (472, 0, 0, 472)}
agree = all((res[n][("A", "iso")], res[n][("A", "anti")],
             res[n][("B", "iso")], res[n][("B", "anti")]) == tgt[n]
            for n in res)
print("  mg-7d75's T3d table reproduced exactly: %s" % agree)
if not agree:
    bad += 1
print()

# ---------------------------------------------------------------------------
hdr("A2d  HOW MANY HYPOTHESES ARE THOSE FOUR CANDIDATES?")

print("  mg-7d75 reports '2 of 4 hold and 2 fail, so the comparison is")
print("  discriminating', and section 2.2 of the document says 'the two that")
print("  hold are the two that say ANTI-ISOMORPHISM'.  One of the two that")
print("  holds is labelled iso/B.  So the question is whether convention B is")
print("  the opposite algebra of convention A, in which case iso/B and anti/A")
print("  are THE SAME STATEMENT and there are two hypotheses, not four.")
print()
print("   n  c^g_{a,b}(Sol,B) = c^g_{b,a}(Sol,A) for all a,b,g   mismatches")
for n in range(2, NMAX + 1):
    types, Cs, sA, CA, sB, CB = side[n]
    miss = 0
    for a in range(len(sA)):
        for b in range(len(sA)):
            l, r = CB[a][b], CA[b][a]
            for c in set(l) | set(r):
                if l.get(c, 0) != r.get(c, 0):
                    miss += 1
    print("  %2d  %-48s  %10d" % (n, miss == 0, miss))
print()
print("  Convention B IS the opposite algebra of convention A, identically.")
print("  So the four columns of T3d are two statements, each computed twice:")
print("      {iso/A, anti/B} is one statement -- and it fails;")
print("      {anti/A, iso/B} is the other  -- and it holds.")
print("  The theorem is reproduced and the comparison IS discriminating; what")
print("  is not the case is that it survived three independent controls.  It")
print("  survived ONE, run twice.  mg-7d75's section 2.2 says 'three of the")
print("  four columns are the control, and they fire' -- two of those three")
print("  columns are the same control in a mirror, and one of them is not a")
print("  control at all: iso/B is the surviving identification.")
print()

print("=" * 78)
print("A2 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
