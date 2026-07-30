"""mg-66a6 AUDIT, target 2: the ONE claim pm-onethird flagged as UNVERIFIED --
that on an antichain the family COINCIDES WITH THE CLASSICAL SHUFFLE WALKS
studied by this method -- settled here independently of the note's answer.

Strategy.  Do NOT accept the "moves = faces of the braid arrangement"
dictionary; rebuild the braid arrangement from its own definition and check it.

  * faces of the braid arrangement A_{n-1} = the realisable sign vectors
    sigma_{ij} = sign(x_i - x_j) over points x in R^n.  Enumerated here from
    integer points, with NO reference to ordered set partitions.
  * the classical face product is the TITS product on sign vectors:
    (xy)_H = x_H if x_H != 0, else y_H.  That is the definition
    Bidigare-Hanlon-Rockmore / Brown-Diaconis use; it mentions no partitions.
  * the classical walk is: draw a face x with probability w(x), move to the
    chamber x.c (Tits product).

If the note's moves/product/action agree with those under a bijection, the
families of walks are literally the same set of Markov chains.  Then the two
NAMED classical walks are checked against their independently-known spectra.
"""

import sys
from fractions import Fraction
from itertools import permutations, product as iproduct

from audit_lib import (poset, orderings, moves, act, product, level, levels,
                       lstr, mstr, multiplicities, eigenvalue,
                       transition_matrix, nullity, sub_scalar, rank_Q,
                       ordered_set_partitions, set_partitions, refines)

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


def antichain(n):
    return poset(n, [])


# --------------------------------------------------------------------------
# the braid arrangement, from its own definition
# --------------------------------------------------------------------------

def pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def sign_vector(x, n):
    return tuple((x[i] > x[j]) - (x[i] < x[j]) for (i, j) in pairs(n))


def braid_faces(n):
    """Every realisable sign vector of the arrangement {x_i = x_j}.  Every face
    is met by a point whose coordinates are integers in 0..n-1, so enumerating
    those integer points enumerates the faces."""
    seen = {}
    for x in iproduct(range(n), repeat=n):
        seen.setdefault(sign_vector(x, n), x)
    return seen


def tits(a, b):
    """(ab)_H = a_H if a_H != 0 else b_H."""
    return tuple(u if u != 0 else v for u, v in zip(a, b))


def osp_to_point(x, n):
    """B_1 gets the LARGEST coordinate, B_2 the next, ...  (The convention is
    not assumed -- it is checked below, and the reverse convention is checked
    too so that a failure cannot be a convention slip.)"""
    v = [0] * n
    k = len(x)
    for i, B in enumerate(x):
        for e in B:
            v[e] = k - i
    return tuple(v)


def osp_to_point_rev(x, n):
    v = [0] * n
    for i, B in enumerate(x):
        for e in B:
            v[e] = i + 1
    return tuple(v)


print(__doc__)
NMAX_FACE = 5
print("=" * 78)
print("SECTION A -- the antichain's moves ARE the faces of the braid")
print("             arrangement, with the SAME product and the SAME action")
print("=" * 78)

FUBINI = {1: 1, 2: 3, 3: 13, 4: 75, 5: 541}
BELL = {2: 2, 3: 5, 4: 15, 5: 52}

for n in range(1, NMAX_FACE + 1):
    P = antichain(n)
    MV = moves(P)
    allosp = list(ordered_set_partitions(range(n)))
    check("n=%d: P-compatibility vacuous, moves = all %d ordered set "
          "partitions" % (n, FUBINI[n]), (len(MV), len(allosp)),
          (FUBINI[n], FUBINI[n]))
    faces = braid_faces(n)
    check("n=%d: the braid arrangement has %d faces (rebuilt from sign "
          "vectors)" % (n, FUBINI[n]), len(faces), FUBINI[n])

    # the dictionary, both conventions
    fwd = {x: sign_vector(osp_to_point(x, n), n) for x in MV}
    rev = {x: sign_vector(osp_to_point_rev(x, n), n) for x in MV}
    check("n=%d: 'B_1 largest' is a bijection moves -> faces" % n,
          (len(set(fwd.values())), set(fwd.values()) == set(faces)),
          (FUBINI[n], True))
    check("n=%d: 'B_1 smallest' is also a bijection moves -> faces" % n,
          (len(set(rev.values())), set(rev.values()) == set(faces)),
          (FUBINI[n], True))

    # chambers
    ords = orderings(P)
    check("n=%d: the states are all n! orderings" % n, len(ords),
          len(list(permutations(range(n)))))
    chambers = [s for s in faces if 0 not in s]
    check("n=%d: the chambers (no zero sign) number n!" % n, len(chambers),
          len(ords))

    # product and action, under the 'B_1 largest' dictionary
    badp = badp_rev = 0
    for x in MV:
        for y in MV:
            if fwd[product(x, y)] != tits(fwd[x], fwd[y]):
                badp += 1
            if rev[product(x, y)] != tits(rev[x], rev[y]):
                badp_rev += 1
    check("n=%d: note's product == Tits product on sign vectors, 0 bad of %d"
          % (n, len(MV) ** 2), badp, 0)
    # (the reverse convention agrees too, and must: negating every sign vector
    # commutes with the Tits product.  So the useful non-vacuity control is
    # whether the test can see the ORDER of the product, and whether a wrong
    # bijection is rejected.)
    badorder = sum(1 for x in MV for y in MV
                   if fwd[product(x, y)] != tits(fwd[y], fwd[x]))
    if n >= 3:
        check("n=%d: CONTROL -- the test detects the order: agreement FAILS "
              "against tits(y,x)" % n, badorder > 0, True)
        # a wrong bijection: compose with a transposition of two faces
        fl = sorted(fwd.values())
        swap = {fl[0]: fl[1], fl[1]: fl[0]}
        wrong = {x: swap.get(v, v) for x, v in fwd.items()}
        badw = sum(1 for x in MV for y in MV
                   if wrong[product(x, y)] != tits(wrong[x], wrong[y]))
        check("n=%d: CONTROL -- a bijection perturbed by one transposition "
              "FAILS the product test" % n, badw > 0, True)
    bada = 0
    as_move = lambda c: tuple(frozenset([e]) for e in c)
    for x in MV:
        for c in ords:
            if fwd[as_move(act(x, c))] != tits(fwd[x], fwd[as_move(c)]):
                bada += 1
    check("n=%d: note's action x.c == Tits product x*c on chambers, "
          "0 bad of %d" % (n, len(MV) * len(ords)), bada, 0)

    LV = levels(P)
    if n >= 2:
        check("n=%d: every partition is a level (%d = Bell)" % (n, BELL[n]),
              (len(LV), len(list(set_partitions(range(n))))),
              (BELL[n], BELL[n]))

print()
print("  CONCLUSION OF SECTION A.  For each n <= 5 the note's move set, its")
print("  product and its action on orderings are carried by a bijection onto")
print("  the faces, the Tits product and the face action of the braid")
print("  arrangement.  So {transition matrix of weight w} is the SAME SET of")
print("  Markov chains as the BHR / Brown-Diaconis braid hyperplane walks.")
print("  The claim is CONFIRMED, and it is an identity of families, not an")
print("  inclusion.")

print()
print("=" * 78)
print("SECTION B -- the closed-form multiplicities on an antichain")
print("=" * 78)


def fact(k):
    r = 1
    for i in range(2, k + 1):
        r *= i
    return r


for n in range(2, 6):
    P = antichain(n)
    LV = levels(P)
    M = multiplicities(P, LV)
    bad = []
    for X in LV:
        cf = 1
        for B in X:
            cf *= fact(len(B) - 1)
        if M[X] != cf:
            bad.append((lstr(X), M[X], cf))
    check("n=%d: m_X = prod_B (|B|-1)! on all %d levels" % (n, len(LV)),
          bad, [])
    check("n=%d: multiplicities sum to n! = %d" % (n, fact(n)),
          sum(M.values()), fact(n))
    if n == 3:
        one = frozenset([frozenset(range(3))])
        check("n=3: the one-block level already has multiplicity 2! = 2",
              M[one], 2)

print()
print("=" * 78)
print("SECTION C -- named walk 1: move-to-front / Tsetlin library")
print("=" * 78)

DERANGE = {0: 1, 1: 0, 2: 1, 3: 2, 4: 9, 5: 44}


def derange(k):
    """Independent recomputation: permutations of k with no fixed point."""
    return sum(1 for w in permutations(range(k))
               if all(w[i] != i for i in range(k)))


for k in range(6):
    check("D(%d) = %d by brute force" % (k, DERANGE[k]), derange(k),
          DERANGE[k])

for n in range(2, 6):
    P = antichain(n)
    MV = moves(P)
    LV = levels(P)
    M = multiplicities(P, LV)
    # weights w_i proportional to i+1 on the move ({i}, rest)
    tot = sum(i + 1 for i in range(n))
    W = {}
    for i in range(n):
        rest = frozenset(e for e in range(n) if e != i)
        x = (frozenset([i]),) + ((rest,) if rest else ())
        assert x in set(MV)
        W[x] = Fraction(i + 1, tot)
    check("n=%d: Tsetlin weights sum to 1" % n, sum(W.values()), 1)

    # the CLASSICAL statement: eigenvalue sum_{i in S} w_i, multiplicity
    # D(n - |S|), over all subsets S of [n].
    classical = {}
    for mask in range(1 << n):
        S = [i for i in range(n) if mask >> i & 1]
        mult = derange(n - len(S))
        if mult:
            lam = sum(W[(frozenset([i]),) +
                        ((frozenset(e for e in range(n) if e != i),)
                         if n > 1 else ())] for i in S)
            classical[lam] = classical.get(lam, 0) + mult

    # what the commitment-level machinery gives
    machinery = {}
    for X in LV:
        if M[X]:
            lam = eigenvalue(P, W, X, MV)
            machinery[lam] = machinery.get(lam, 0) + M[X]
    check("n=%d: level machinery reproduces the classical Tsetlin spectrum "
          "(value -> multiplicity)" % n, machinery, classical)
    check("n=%d: total multiplicity n! = %d" % (n, fact(n)),
          sum(machinery.values()), fact(n))
    print("       n=%d: %d distinct eigenvalues with w_i proportional to i"
          % (n, len(machinery)))
    generic = sum(1 for mask in range(1 << n)
                  if derange(n - bin(mask).count("1")))
    print("       n=%d: %d distinct eigenvalues for GENERIC w_i "
          "(= subsets S with D(n-|S|) > 0)" % (n, generic))
    if n <= 4:
        ords = orderings(P)
        T = transition_matrix(P, W, ords, MV)
        dims = {}
        for lam in machinery:
            dims[lam] = nullity(sub_scalar(T, lam))
        check("n=%d: dim ker(M - lambda I) matches predicted multiplicity "
              "for every lambda" % n, dims, machinery)
        check("n=%d: dimensions sum to n! (diagonalisable)" % n,
              sum(dims.values()), fact(n))

print()
print("=" * 78)
print("SECTION D -- named walk 2: inverse GSR a-riffle shuffle")
print("=" * 78)


def stirling_first(n):
    """Unsigned Stirling numbers of the first kind c(n,m) = number of
    permutations of n with m cycles.  Recomputed by brute-force cycle count as
    a cross-check for small n."""
    c = [[0] * (n + 1) for _ in range(n + 1)]
    c[0][0] = 1
    for i in range(1, n + 1):
        for m in range(1, i + 1):
            c[i][m] = c[i - 1][m - 1] + (i - 1) * c[i - 1][m]
    return c


def cycles(w):
    seen = set()
    k = 0
    for i in range(len(w)):
        if i not in seen:
            k += 1
            j = i
            while j not in seen:
                seen.add(j)
                j = w[j]
    return k


for n in range(2, 6):
    c = stirling_first(n)
    brute = {}
    for w in permutations(range(n)):
        brute[cycles(w)] = brute.get(cycles(w), 0) + 1
    check("n=%d: Stirling c(n,m) recurrence == brute-force cycle counts" % n,
          {m: c[n][m] for m in range(1, n + 1)}, brute)

for n in range(2, 6):
    for a in (2, 3):
        P = antichain(n)
        MV = moves(P)
        LV = levels(P)
        M = multiplicities(P, LV)
        ords = orderings(P)

        # (i) the law induced by the LABELLING procedure, move by move.
        # Label each card independently and uniformly with one of a labels,
        # then stably sort by label.  The move performed is: blocks = label
        # classes, in increasing label order.
        lawn = {}
        for lab in iproduct(range(a), repeat=n):
            blocks = {}
            for e in range(n):
                blocks.setdefault(lab[e], set()).add(e)
            x = tuple(frozenset(blocks[l]) for l in sorted(blocks))
            lawn[x] = lawn.get(x, 0) + 1
        W = {x: Fraction(v, a ** n) for x, v in lawn.items()}
        check("n=%d a=%d: labelling law is a probability on moves" % (n, a),
              (sum(W.values()), all(x in set(MV) for x in W)), (1, True))
        # closed form C(a,k)/a^n
        def binom(p, q):
            if q < 0 or q > p:
                return 0
            r = 1
            for i in range(q):
                r = r * (p - i) // (i + 1)
            return r
        bad = [(mstr(x), v) for x, v in W.items()
               if v != Fraction(binom(a, len(x)), a ** n)]
        check("n=%d a=%d: w(x) = C(a, #blocks)/a^n exactly" % (n, a), bad, [])

        # (ii) eigenvalue at a level X is a^{|X| - n}
        bad = []
        for X in LV:
            lam = eigenvalue(P, W, X, MV)
            want = Fraction(1, a ** (n - len(X)))
            if lam != want:
                bad.append((lstr(X), str(lam), str(want)))
        check("n=%d a=%d: lambda_X = a^{|X|-n} on all %d levels"
              % (n, a, len(LV)), bad, [])

        # (iii) multiplicities are the Stirling counts
        agg = {}
        for X in LV:
            if M[X]:
                agg[len(X)] = agg.get(len(X), 0) + M[X]
        cst = stirling_first(n)
        check("n=%d a=%d: total multiplicity at |X| = m is c(n,m) "
              "(permutations of n with m cycles)" % (n, a), agg,
              {m: cst[n][m] for m in range(1, n + 1) if cst[n][m]})

        # (iv) against a matrix built DIRECTLY from the labelling description
        if n <= 4:
            idx = {c_: i for i, c_ in enumerate(ords)}
            m = len(ords)
            T = [[Fraction(0)] * m for _ in range(m)]
            for lab in iproduct(range(a), repeat=n):
                for j, c_ in enumerate(ords):
                    # stable sort of the current ordering by label
                    newc = tuple(sorted(c_, key=lambda e: (lab[e],
                                                           list(c_).index(e))))
                    T[idx[newc]][j] += Fraction(1, a ** n)
            Tsemi = transition_matrix(P, W, ords, MV)
            check("n=%d a=%d: GSR matrix from the labelling == matrix from "
                  "the semigroup weight" % (n, a), T, Tsemi)
            dims = {}
            pred = {}
            for X in LV:
                if M[X]:
                    lam = eigenvalue(P, W, X, MV)
                    pred[lam] = pred.get(lam, 0) + M[X]
            for lam in pred:
                dims[lam] = nullity(sub_scalar(T, lam))
            check("n=%d a=%d: dim ker matches predicted multiplicities"
                  % (n, a), dims, pred)
            check("n=%d a=%d: dimensions sum to n! (diagonalisable)" % (n, a),
                  sum(dims.values()), fact(n))

print()
print("=" * 78)
print("SECTION E -- which classical shuffles are NOT in the family")
print("=" * 78)


def move_matrices(P, ords, MV):
    idx = {c: i for i, c in enumerate(ords)}
    m = len(ords)
    out = []
    for x in MV:
        v = [0] * (m * m)
        for j, c in enumerate(ords):
            v[idx[act(x, c)] * m + j] = 1
        out.append(v)
    return out


def in_span(vecs, target):
    r0 = rank_Q(vecs)
    r1 = rank_Q(vecs + [target])
    return r0 == r1, r0, r1


def flat(T):
    m = len(T)
    return [T[i][j] for i in range(m) for j in range(m)]


for n in (3, 4):
    P = antichain(n)
    MV = moves(P)
    ords = orderings(P)
    idx = {c: i for i, c in enumerate(ords)}
    m = len(ords)
    vecs = move_matrices(P, ords, MV)

    def blank():
        return [[Fraction(0)] * m for _ in range(m)]

    # random-to-top (control: it IS in the family)
    T = blank()
    for i in range(n):
        rest = frozenset(e for e in range(n) if e != i)
        x = (frozenset([i]), rest)
        for j, c in enumerate(ords):
            T[idx[act(x, c)]][j] += Fraction(1, n)
    r2t = in_span(vecs, flat(T))

    # top-to-random
    T = blank()
    for j, c in enumerate(ords):
        top, tail = c[0], c[1:]
        for p in range(n):
            newc = tail[:p] + (top,) + tail[p:]
            T[idx[newc]][j] += Fraction(1, n)
    t2r = in_span(vecs, flat(T))

    # random transpositions (positions i,j uniform and independent)
    T = blank()
    for j, c in enumerate(ords):
        for i in range(n):
            for k in range(n):
                v = list(c)
                v[i], v[k] = v[k], v[i]
                T[idx[tuple(v)]][j] += Fraction(1, n * n)
    rt = in_span(vecs, flat(T))

    # lazy adjacent transpositions: stay with prob 1/2, else a uniform
    # adjacent swap
    T = blank()
    for j, c in enumerate(ords):
        T[j][j] += Fraction(1, 2)
        for t in range(n - 1):
            v = list(c)
            v[t], v[t + 1] = v[t + 1], v[t]
            T[idx[tuple(v)]][j] += Fraction(1, 2 * (n - 1))
    lat = in_span(vecs, flat(T))

    print("  n=%d  (rank of the move span = %d of %d)" % (n, r2t[1], m * m))
    for name, res, want in (("random-to-top (control)", r2t, True),
                            ("top-to-random", t2r, False),
                            ("random transpositions", rt, False),
                            ("lazy adjacent transpositions", lat, False)):
        print("     %-30s in span? %-5s (rank %d -> %d)"
              % (name, res[0], res[1], res[2]))
        check("n=%d: %s in the linear span of the moves = %s"
              % (n, name, want), res[0], want)

print()
print("=" * 78)
print("%d checks, %d FAILURES" % (CHECKS[0], len(FAIL)))
for f in FAIL:
    print("  FAILED: %s" % f)
print("=" * 78)
sys.exit(1 if FAIL else 0)
