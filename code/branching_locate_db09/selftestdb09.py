"""Self-test for kerndb09.  Every assertion is a fact checkable by hand or
against an independently known sequence.  Run first by run_all.sh."""

import sys
from fractions import Fraction

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kerndb09 import *          # noqa: F401,F403
from kerndb09 import (rref, rank, nullspace, MonAlg, tl_diagrams, tl_product,
                      tl_algebra, link_states, tl_gram, tl_cell_matrices,
                      hom_dim, restrict_cell, group_algebra, class_sums,
                      sym_group, perm_mul, cycle_type, embed, gz_algebra,
                      algebra_generated, centralizer, is_commutative_subspace,
                      mk_poset, all_posets, poset_classes, faces_of, tits,
                      supp, AC_by_support, AC_by_acyclicity, band_algebra,
                      set_partitions, mobius, unit_vector,
                      tl_diagram_action, tl_simples, tl_embed_diagram,
                      solve_exact, mat_mul, mat_inv)

N = 0


def ck(cond, msg):
    global N
    N += 1
    if not cond:
        raise AssertionError("SELFTEST FAILED: " + msg)


# ---- linear algebra -------------------------------------------------------
F = Fraction
ck(rank([[F(1), F(2)], [F(2), F(4)]], 2) == 1, "rank of a rank-1 matrix")
ck(rank([[F(1), F(0)], [F(0), F(1)]], 2) == 2, "rank of the identity")
ck(len(nullspace([[F(1), F(1)]], 2)) == 1, "nullspace dimension")
ck(nullspace([[F(1), F(1)]], 2)[0] == [F(-1), F(1)], "nullspace vector")
R, p = rref([[F(0), F(2)], [F(1), F(1)]], 2)
ck(p == [0, 1] and R[0] == [F(1), F(0)], "rref pivots and reduction")

# ---- Temperley-Lieb diagrams ---------------------------------------------


def catalan(n):
    c = 1
    for k in range(n):
        c = c * 2 * (2 * k + 1) // (k + 2)
    return c


for n in range(1, 7):
    ck(len(tl_diagrams(n)) == catalan(n), "TL_%d has Catalan many diagrams" % n)
d2 = tl_diagrams(2)
one2 = tuple([2, 3, 0, 1])
ck(one2 in d2, "the identity diagram of TL_2 is planar")
for a in d2:
    loops, prod = tl_product(2, one2, a)
    ck((loops, prod) == (0, a), "1 * a = a in TL_2")
    loops, prod = tl_product(2, a, one2)
    ck((loops, prod) == (0, a), "a * 1 = a in TL_2")
cup = tuple([1, 0, 3, 2])
ck(cup in d2, "the cup-cap diagram is planar")
ck(tl_product(2, cup, cup) == (1, cup), "u*u = beta*u closes one loop")
# associativity of the diagram product, TL_3 and TL_4, exhaustive
for n in (3, 4):
    ds = tl_diagrams(n)
    for a in ds:
        for b in ds:
            l1, ab = tl_product(n, a, b)
            for c in ds:
                l2, abc = tl_product(n, ab, c)
                l3, bc = tl_product(n, b, c)
                l4, abc2 = tl_product(n, a, bc)
                ck((l1 + l2, abc) == (l3 + l4, abc2),
                   "TL_%d diagram product is associative" % n)

# ---- TL algebra over Q ----------------------------------------------------
A = tl_algebra(3, 2)
ck(A.dim == 5, "dim TL_3 = 5")
ck(unit_vector(A) is not None, "TL_3 has an identity basis element")
ck(len(A.radical()) == 0, "TL_3(2) is semisimple")
A1 = tl_algebra(3, 1)
ck(len(A1.radical()) == 3, "TL_3(1) has a 3-dimensional radical")
ck(A1.verify_radical(A1.radical())[:2] == (True, True),
   "the radical of TL_3(1) is a nilpotent ideal")

# ---- link states and the Gram form ---------------------------------------
for n in range(1, 7):
    tot = sum(len(link_states(n, p)) ** 2 for p in range(n // 2 + 1))
    ck(tot == catalan(n), "sum of squares of cell dims = dim TL_%d" % n)
ck(len(link_states(4, 1)) == 3, "dim V_{4,1} = 3")
ck(len(link_states(4, 2)) == 2, "dim V_{4,2} = 2")
st, G = tl_gram(2, 1, 5)
ck(len(st) == 1 and G[0][0] == 5, "the 1x1 Gram matrix of V_{2,1} is (beta)")
st, G = tl_gram(2, 0, 5)
ck(len(st) == 1 and G[0][0] == 1, "the Gram matrix of V_{2,0} is (1)")

# ---- module actions and Hom ----------------------------------------------
st, mats = tl_cell_matrices(3, 1, 2)
ck(len(mats) == 2, "TL_3 has two generators")
for M in mats:
    ck(len(M) == len(st), "generator matrices are square of the right size")
ck(hom_dim(mats, mats, len(st), len(st)) >= 1, "Hom(V,V) is nonzero")
st1, m1 = tl_cell_matrices(2, 0, 2)
st2, r2 = restrict_cell(3, 0, 2)
ck(hom_dim(m1, r2, len(st1), len(st2)) == 1,
   "V_{3,0} restricted contains V_{2,0} once")

# ---- the diagram action, the simples and the embedding  (mg-e8b8) --------
#
# The action of a whole diagram on a cell module must AGREE with the action
# of the generators the rest of T1 uses, so the new code and the old code are
# tied together on every (n, p, beta) they share.
for n in range(2, 6):
    for p in range(0, n // 2 + 1):
        for b in (3, 2, 1, 0):
            S, dmats = tl_diagram_action(n, p, b)
            S2, gmats = tl_cell_matrices(n, p, b)
            ck(S == S2, "diagram action and generator action share a basis")
            for i in range(n - 1):
                m = [None] * (2 * n)
                for k in range(n):
                    if k in (i, i + 1):
                        continue
                    m[k] = n + k
                    m[n + k] = k
                m[i], m[i + 1] = i + 1, i
                m[n + i], m[n + i + 1] = n + i + 1, n + i
                ck(dmats[tuple(m)] == gmats[i],
                   "u_%d acts the same as its diagram on V_{%d,%d} at beta=%s"
                   % (i, n, p, b))
# the identity diagram acts as the identity matrix
for n in range(1, 6):
    ident = tuple([n + k for k in range(n)] + [k for k in range(n)])
    for p in range(0, n // 2 + 1):
        S, dmats = tl_diagram_action(n, p, 3)
        d = len(S)
        ck(dmats[ident] == [[F(1) if i == j else F(0) for j in range(d)]
                            for i in range(d)],
           "the identity diagram acts as the identity on V_{%d,%d}" % (n, p))
# the character of L(n,p) at the identity is its dimension, and the
# dimensions square-sum to the semisimple quotient
for n in range(1, 7):
    ident = tuple([n + k for k in range(n)] + [k for k in range(n)])
    for b in (3, 2, 1, 0):
        sim = tl_simples(n, b)
        for (p, dim, chi) in sim:
            ck(dim == len(link_states(n, p))
               - len(nullspace(tl_gram(n, p, b)[1], len(link_states(n, p)))),
               "dim L(%d,%d) is the rank of the Gram form at beta=%s"
               % (n, p, b))
            if dim:
                ck(chi[ident] == dim,
                   "chi_{L(%d,%d)}(1) = dim at beta=%s" % (n, p, b))
        ck(sum(d * d for (p, d, c) in sim)
           == tl_algebra(n, b).semisimple_quotient_dim(),
           "sum (dim L)^2 = dim A/rad for TL_%d(%s)" % (n, b))
# the embedding is a well-defined injection into the diagrams of TL_n and is
# multiplicative on the whole table of TL_{n-1}
for n in range(2, 6):
    emb = tl_embed_diagram(n)
    big = set(tl_diagrams(n))
    small = tl_diagrams(n - 1)
    ck(len(set(emb.values())) == len(small), "the embedding is injective")
    for d in small:
        ck(emb[d] in big, "the image of a TL_%d diagram is a TL_%d diagram"
           % (n - 1, n))
    for a in small:
        for b2 in small:
            la, da = tl_product(n - 1, a, b2)
            lb, db = tl_product(n, emb[a], emb[b2])
            ck((la, emb[da]) == (lb, db),
               "the embedding is multiplicative on TL_%d" % (n - 1))
ck(solve_exact([[F(1), F(0)], [F(0), F(1)]], [F(2), F(3)]) == ([F(2), F(3)], True),
   "solve_exact on the identity")
ck(solve_exact([[F(1), F(1)]], [F(1), F(0)])[0] is None,
   "solve_exact reports an inconsistent system")
ck(solve_exact([[F(1)], [F(1)]], [F(2)])[1] is False,
   "solve_exact reports a non-unique solution")
ck(mat_mul([[F(1), F(2)]], [[F(3)], [F(4)]]) == [[F(11)]], "mat_mul")
ck(mat_mul(mat_inv([[F(1), F(2)], [F(3), F(4)]]), [[F(1), F(2)], [F(3), F(4)]])
   == [[F(1), F(0)], [F(0), F(1)]], "mat_inv")

# ---- symmetric groups -----------------------------------------------------
ck(len(sym_group(4)) == 24, "|S_4| = 24")
ck(perm_mul((1, 0, 2), (0, 2, 1)) == (1, 2, 0), "permutation product")
ck(cycle_type((1, 0, 3, 2)) == (2, 2), "cycle type of (12)(34)")
ck(embed((1, 0), 2, 4) == (1, 0, 2, 3), "S_2 embeds into S_4")
G4 = group_algebra(4)
ck(G4.dim == 24, "dim CS_4 = 24")
ck(len(G4.radical()) == 0, "CS_4 is semisimple")
idx = {g: i for i, g in enumerate(G4.basis)}
cs = class_sums(4, 4, idx)
ck(len(cs) == 5, "S_4 has 5 conjugacy classes")
ck(sum(sum(v) for v in cs) == 24, "the class sums use every group element once")
Z = algebra_generated(G4, cs)
ck(len(Z) == 5, "the centre of CS_4 is 5-dimensional")
ck(is_commutative_subspace(G4, Z), "the centre is commutative")

# ---- posets, faces, supports ---------------------------------------------
ck(len(all_posets(3)) == 19, "19 labelled posets on 3 points")
ck(len(poset_classes(3)) == 5, "5 poset classes on 3 points")
ck(len(poset_classes(4)) == 16, "16 poset classes on 4 points")
ck(len(poset_classes(5)) == 63, "63 poset classes on 5 points")
fub = [1, 3, 13, 75, 541]
for n in range(1, 6):
    ck(len(faces_of(mk_poset(n, []))) == fub[n - 1],
       "|F(antichain_%d)| is the n-th Fubini number" % n)
bell = [1, 2, 5, 15, 52]
for n in range(1, 6):
    ck(len(set_partitions(n)) == bell[n - 1], "Bell(%d)" % n)
for n in range(1, 6):
    P = mk_poset(n, [(i, i + 1) for i in range(n - 1)])
    ck(len(faces_of(P)) == 2 ** (n - 1), "|F(chain_%d)| = 2^(n-1)" % n)
for n in range(1, 5):
    for P in poset_classes(n):
        kk = lambda L: {tuple(tuple(b) for b in X) for X in L}
        a = kk(AC_by_support(P))
        b = kk(AC_by_acyclicity(P))
        ck(a == b, "the two routes to AC agree on a class at n=%d" % n)
# the Tits product is associative and idempotent on F(P)
for P in poset_classes(3) + poset_classes(4):
    Fs = faces_of(P)
    for x in Fs:
        ck(tits(x, x) == x, "faces are idempotent")
        for y in Fs:
            ck(tits(x, y) in Fs, "F(P) is closed under the Tits product")
            for z in Fs:
                ck(tits(tits(x, y), z) == tits(x, tits(y, z)),
                   "the Tits product is associative")
            # the left regular band law
            ck(tits(tits(x, y), x) == tits(x, y), "xyx = xy")
# supp is a homomorphism to the semilattice of supports
for P in poset_classes(3):
    Fs = faces_of(P)
    for x in Fs:
        for y in Fs:
            joined = supp(tits(x, y))
            ck(all(any(set(b) <= set(c) for c in supp(x)) for b in joined),
               "supp(xy) refines supp(x)")

# ---- band algebras --------------------------------------------------------
P = mk_poset(3, [])
B = band_algebra(P)
ck(B.dim == 13, "dim kF(antichain_3) = 13")
ck(B.dim - len(B.radical()) == 5, "dim kF(antichain_3)/rad = 5 = Bell(3)")
Pc = mk_poset(3, [(0, 1), (1, 2)])
Bc = band_algebra(Pc)
ck(len(Bc.radical()) == 0, "kF(chain_3) is semisimple")

# ---- Mobius ---------------------------------------------------------------
els = [0, 1, 2]
mu = mobius(els, lambda a, b: a <= b)
ck(mu[(0, 0)] == 1 and mu[(0, 1)] == -1 and mu[(0, 2)] == 0,
   "Mobius function of a 3-chain")

print("selftest: %d assertions, all passed" % N)
