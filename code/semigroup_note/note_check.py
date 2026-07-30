"""Every number in docs/OneThird-Semigroup-Walk-Family-Note.md, computed from scratch.

Written for mg-6016.  Deliberately shares NO code with code/hodge_leverage/ or
code/face_geometry/: posets, orderings, moves, the product, the action, the
commitment levels, the multiplicities and the spectra are all rebuilt here from
their definitions, in exact rational arithmetic.  The point is that the note's
arithmetic is reproducible by a reader who has only the note.

Sections, in the order the note uses them:

  A  the worked example P = {a<b, c<d}: orderings, moves, the action, one step,
     and the demonstration that a commitment made by one move is overwritten by
     a later one (so nothing accumulates and the walk is not absorbing)
  B  the two identities (x.x = x and x.y.x = x.y), plus closure and associativity
  C  the commitment levels of the example, and the acyclic-cut description
     checked against the definition (supports of moves) up to 5 elements
  D  the multiplicities of the example, computed from P alone
  E  the spectrum under three different weightings -- eigenvalues move,
     multiplicities do not
  F  the antichain: the moves are ALL ordered set partitions (Fubini numbers),
     the multiplicities are prod_B (|B|-1)!, and the classical instances --
     move-to-front / Tsetlin (derangement multiplicities) and the inverse
     a-riffle-shuffle (a^{-j} with Stirling multiplicities), the latter checked
     against a transition matrix built from the Gilbert-Shannon-Reeds
     description with no reference to the semigroup at all
  G  the boundary: the adjacent-transposition walk is not in the family

Blocks are stored as integer bitmasks throughout, for speed.
"""

import itertools
import math
import sys
import time
from fractions import Fraction

F = Fraction
T0 = time.time()


# --------------------------------------------------------------------------
# posets
# --------------------------------------------------------------------------


class Poset:
    """A strict partial order on range(n), stored transitively closed."""

    def __init__(self, n, relations, names=None):
        self.n = n
        less = set(relations)
        changed = True
        while changed:
            changed = False
            for (i, j) in list(less):
                for (k, m) in list(less):
                    if j == k and (i, m) not in less:
                        less.add((i, m))
                        changed = True
        for (i, j) in less:
            assert i != j and (j, i) not in less, "not a partial order"
        self.less = frozenset(less)
        self.names = names or [chr(ord("a") + i) for i in range(n)]

    def induced(self, elements):
        idx = {e: t for t, e in enumerate(elements)}
        rel = [(idx[i], idx[j]) for (i, j) in self.less if i in idx and j in idx]
        return Poset(len(elements), rel)

    def show(self, ordering):
        return "".join(self.names[i] for i in ordering)


def linear_extensions(P):
    out = []
    for perm in itertools.permutations(range(P.n)):
        pos = {e: t for t, e in enumerate(perm)}
        if all(pos[i] < pos[j] for (i, j) in P.less):
            out.append(perm)
    return out


def all_posets(n):
    """Every partial order on the LABELLED set range(n).

    Every poset has a linear extension, so every poset is a relabelling of a
    transitively closed subset of {(i,j) : i<j}.  Enumerate those, relabel by
    every permutation, dedupe.
    """
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    seen = {}
    for bits in range(1 << len(pairs)):
        rs = {pairs[t] for t in range(len(pairs)) if bits >> t & 1}
        if any((i, m) not in rs for (i, j) in rs for (k, m) in rs if j == k):
            continue
        for perm in itertools.permutations(range(n)):
            rel = frozenset((perm[i], perm[j]) for (i, j) in rs)
            if rel not in seen:
                seen[rel] = Poset(n, rel)
    return list(seen.values())


def iso_classes(n):
    """One representative per isomorphism class of poset on n elements."""
    reps = {}
    for P in all_posets(n):
        # NB: compare SORTED TUPLES, not frozensets -- `<` on frozensets is the
        # subset order, which is partial, so min() over frozensets is not a
        # canonical form.
        canon = min(tuple(sorted((perm[i], perm[j]) for (i, j) in P.less))
                    for perm in itertools.permutations(range(n)))
        if canon not in reps:
            reps[canon] = P
    return list(reps.values())


# --------------------------------------------------------------------------
# moves: P-compatible ordered partitions (blocks as bitmasks)
# --------------------------------------------------------------------------


def ordered_set_partitions(n):
    """Every ordered partition of range(n) as a tuple of bitmasks."""
    if n == 0:
        yield ()
        return
    for k in range(1, n + 1):
        for assign in itertools.product(range(k), repeat=n):
            if len(set(assign)) != k:
                continue
            blocks = [0] * k
            for e, b in enumerate(assign):
                blocks[b] |= 1 << e
            yield tuple(blocks)


def block_index(x, n):
    """Array giving, for each element, the index of its block in x."""
    where = [0] * n
    for t, B in enumerate(x):
        m = B
        while m:
            low = m & -m
            where[low.bit_length() - 1] = t
            m ^= low
    return where


def compatible(P, x):
    """For every i <_P j, i's block is not strictly after j's block."""
    w = block_index(x, P.n)
    return all(w[i] <= w[j] for (i, j) in P.less)


def moves_of(P):
    return [x for x in ordered_set_partitions(P.n) if compatible(P, x)]


def product(x, y):
    """x . y -- blocks B_i & C_j ordered lexicographically by (i,j), empties dropped."""
    out = []
    for B in x:
        for C in y:
            D = B & C
            if D:
                out.append(D)
    return tuple(out)


def act(x, ordering):
    """A move applied to an ordering: x's blocks in x's order, and inside each
    block the elements in the order they appear in `ordering`."""
    out = []
    for B in x:
        out.extend(e for e in ordering if B >> e & 1)
    return tuple(out)


def as_move(ordering):
    return tuple(1 << e for e in ordering)


def support(x):
    """The commitment level of a move: its underlying unordered partition."""
    return frozenset(x)


def bits(B):
    return [t for t in range(B.bit_length()) if B >> t & 1]


def show_move(P, x):
    return "(" + "|".join("".join(P.names[e] for e in bits(B)) for B in x) + ")"


def show_level(P, pi):
    return "|".join(sorted("".join(P.names[e] for e in bits(B)) for B in pi))


# --------------------------------------------------------------------------
# commitment levels and the acyclic-cut description
# --------------------------------------------------------------------------


def all_partitions(n):
    def rec(i, blocks):
        if i == n:
            yield frozenset(blocks)
            return
        for t in range(len(blocks)):
            b = blocks[t]
            blocks[t] = b | (1 << i)
            yield from rec(i + 1, blocks)
            blocks[t] = b
        blocks.append(1 << i)
        yield from rec(i + 1, blocks)
        blocks.pop()
    yield from rec(0, [])


def is_acyclic_quotient(P, pi):
    """Blocks are nodes; edge B -> C when some i in B has i <_P j for j in C.
    Acyclic = no directed cycle among distinct blocks."""
    blocks = sorted(pi)
    idx = {}
    for t, B in enumerate(blocks):
        for e in bits(B):
            idx[e] = t
    k = len(blocks)
    edge = [[False] * k for _ in range(k)]
    for (i, j) in P.less:
        if idx[i] != idx[j]:
            edge[idx[i]][idx[j]] = True
    for m in range(k):
        for i in range(k):
            if edge[i][m]:
                for j in range(k):
                    if edge[m][j]:
                        edge[i][j] = True
    return not any(edge[i][i] for i in range(k))


def commitment_levels(P, moves=None):
    mv = moves if moves is not None else moves_of(P)
    return sorted({support(x) for x in mv},
                  key=lambda pi: (len(pi), sorted(pi)))


def acyclic_partitions(P):
    return {pi for pi in all_partitions(P.n) if is_acyclic_quotient(P, pi)}


# --------------------------------------------------------------------------
# multiplicities from the poset alone
# --------------------------------------------------------------------------


def refines(pi, sigma):
    """Is pi a refinement of sigma?  (Every block of pi inside a block of sigma.)"""
    return all(any(B & ~C == 0 for C in sigma) for B in pi)


def multiplicities(P, levels=None):
    """m_X solving  sum_{Y refines X} m_Y = prod_{B in X} |L(P|_B)|."""
    lev = levels if levels is not None else commitment_levels(P)
    target = {}
    for X in lev:
        prod = 1
        for B in X:
            prod *= len(linear_extensions(P.induced(bits(B))))
        target[X] = prod
    m = {}
    for X in sorted(lev, key=lambda pi: -len(pi)):          # finest first
        s = sum(m[Y] for Y in m if Y != X and refines(Y, X))
        m[X] = target[X] - s
    return m, target


def eigenvalues(P, w, levels):
    """lambda_X = total weight of the moves whose commitment level is coarser
    than (or equal to) X -- i.e. of the moves y with X a refinement of supp(y)."""
    out = {}
    for X in levels:
        out[X] = sum((w[x] for x in w if w[x] and refines(X, support(x))), F(0))
    return out


# --------------------------------------------------------------------------
# exact linear algebra
# --------------------------------------------------------------------------


def rank(M):
    M = [row[:] for row in M]
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = F(1) / M[r][c]
        M[r] = [v * inv for v in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == rows:
            break
    return r


def transition_matrix(P, w, ords):
    idx = {c: t for t, c in enumerate(ords)}
    N = len(ords)
    M = [[F(0)] * N for _ in range(N)]
    for x, p in w.items():
        if not p:
            continue
        for c in ords:
            M[idx[c]][idx[act(x, c)]] += p
    return M


def kernel_dim(M, lam):
    N = len(M)
    A = [[M[i][j] - (lam if i == j else 0) for j in range(N)] for i in range(N)]
    return N - rank(A)


def head(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def sub(s):
    print()
    print("-- " + s)


# ==========================================================================
# A. the worked example
# ==========================================================================

EX = Poset(4, [(0, 1), (2, 3)])                 # a<b and c<d
A, B, C, D = 0, 1, 2, 3
mA, mB, mC, mD = 1, 2, 4, 8

head("A.  The worked example  P = {a<b, c<d}")

ex_ords = linear_extensions(EX)
print("orderings (|L(P)| = %d): %s"
      % (len(ex_ords), ", ".join(EX.show(c) for c in ex_ords)))

ex_moves = moves_of(EX)
all_osp = list(ordered_set_partitions(4))
print("ordered partitions of 4 elements: %d;  compatible with P (= moves): %d"
      % (len(all_osp), len(ex_moves)))
by_k = {}
for x in ex_moves:
    by_k.setdefault(len(x), []).append(x)
for k in sorted(by_k):
    print("  %d block(s): %2d   %s"
          % (k, len(by_k[k]), " ".join(show_move(EX, x) for x in by_k[k])))

sub("the action agrees with the product against a singleton move, on every"
    " (move, ordering) pair")
bad = [(x, c) for x in ex_moves for c in ex_ords
       if as_move(act(x, c)) != product(x, as_move(c))]
print("mismatches: %d of %d" % (len(bad), len(ex_moves) * len(ex_ords)))

sub("the action never leaves the set of orderings")
bad = [(x, c) for x in ex_moves for c in ex_ords if act(x, c) not in set(ex_ords)]
print("results outside L(P): %d of %d" % (len(bad), len(ex_moves) * len(ex_ords)))

sub("one step, spelled out")
X1 = (mA | mC, mB | mD)                                  # (ac|bd)
for c in ex_ords:
    print("   %s applied to %s  ->  %s"
          % (show_move(EX, X1), EX.show(c), EX.show(act(X1, c))))

sub("nothing accumulates: a commitment made by one move is overwritten by a later one")
X2 = (mA, mC, mB | mD)                                   # (a|c|bd)
Y2 = (mC | mD, mA | mB)                                  # (cd|ab)
s0 = (A, B, C, D)
s1 = act(X2, s0)
s2 = act(Y2, s1)
s3 = act(X2, s2)
print("   start                       %s" % EX.show(s0))
print("   %s applied  ->  %s   a is before c, and the move DECIDED that"
      % (show_move(EX, X2), EX.show(s1)))
print("   %s applied  ->  %s   c is before a -- the decision is GONE"
      % (show_move(EX, Y2), EX.show(s2)))
print("   %s applied  ->  %s   and back again"
      % (show_move(EX, X2), EX.show(s3)))

sub("every ordering is reachable from every ordering, so the walk mixes rather"
    " than absorbing")
reach = {c: {c} for c in ex_ords}
changed = True
while changed:
    changed = False
    for c in ex_ords:
        new = set(reach[c]) | {act(x, d) for d in reach[c] for x in ex_moves}
        if new != reach[c]:
            reach[c] = new
            changed = True
print("orderings reachable from each: %s   (|L(P)| = %d)"
      % (sorted(len(reach[c]) for c in ex_ords), len(ex_ords)))
fixed = [x for x in ex_moves if all(act(x, c) == c for c in ex_ords)]
print("moves that fix every ordering: %d  %s"
      % (len(fixed), " ".join(show_move(EX, x) for x in fixed)))
absorbing = [c for c in ex_ords if all(act(x, c) == c for x in ex_moves)]
print("absorbing orderings (no move can leave): %d" % len(absorbing))

# ==========================================================================
# B. the two identities
# ==========================================================================

head("B.  The two identities:  x.x = x  and  x.y.x = x.y")

sub("on the worked example, over all moves")
n_idem = sum(1 for x in ex_moves if product(x, x) == x)
n_lrb = sum(1 for x in ex_moves for y in ex_moves
            if product(product(x, y), x) == product(x, y))
n_closed = sum(1 for x in ex_moves for y in ex_moves
               if compatible(EX, product(x, y)))
n_assoc = sum(1 for x in ex_moves for y in ex_moves for z in ex_moves
              if product(product(x, y), z) == product(x, product(y, z)))
print("x.x = x                       : %d of %d" % (n_idem, len(ex_moves)))
print("x.y.x = x.y                   : %d of %d" % (n_lrb, len(ex_moves) ** 2))
print("closure (x.y is again a move) : %d of %d" % (n_closed, len(ex_moves) ** 2))
print("associativity                 : %d of %d" % (n_assoc, len(ex_moves) ** 3))

sub("the same two identities read as statements about the walk")
print("   x.y acts as 'y first, then x'.  So x.y.x = x.y says: doing x, then y,")
print("   then x again is the same as doing y then x -- the earlier x leaves no trace.")
for (x, y) in [(X1, Y2), (X2, Y2), (Y2, X2), (X1, X2)]:
    xyx = [act(x, act(y, act(x, c))) for c in ex_ords]
    yx = [act(x, act(y, c)) for c in ex_ords]
    via = [act(product(x, y), c) for c in ex_ords]
    xx = [act(x, act(x, c)) for c in ex_ords]
    justx = [act(x, c) for c in ex_ords]
    print("   x=%-11s y=%-11s   'x,y,x' == 'y,x': %-5s   x.y acts as 'y then x': %-5s"
          "   'x,x' == 'x': %s"
          % (show_move(EX, x), show_move(EX, y), xyx == yx, via == yx, xx == justx))

sub("exhaustively, on every LABELLED poset up to 4 elements")
for n in range(1, 5):
    ps = all_posets(n)
    bad_i = bad_l = bad_c = bad_a = tot_i = tot_p = tot_t = 0
    for P in ps:
        mv = moves_of(P)
        tot_i += len(mv)
        tot_p += len(mv) ** 2
        bad_i += sum(1 for x in mv if product(x, x) != x)
        for x in mv:
            for y in mv:
                xy = product(x, y)
                if product(xy, x) != xy:
                    bad_l += 1
                if not compatible(P, xy):
                    bad_c += 1
        if n <= 3:
            tot_t += len(mv) ** 3
            for x in mv:
                for y in mv:
                    for z in mv:
                        if product(product(x, y), z) != product(x, product(y, z)):
                            bad_a += 1
    print("n=%d  posets %4d   x.x=x: %d bad of %d   x.y.x=x.y: %d bad of %d   "
          "closure: %d bad of %d   assoc: %d bad of %s"
          % (n, len(ps), bad_i, tot_i, bad_l, tot_p, bad_c, tot_p, bad_a,
             tot_t if n <= 3 else "(not run)"))

sub("at 5 elements, on one representative of each isomorphism class")
reps5 = iso_classes(5)
bad_i = bad_l = bad_c = tot_i = tot_p = 0
for P in reps5:
    mv = moves_of(P)
    tot_i += len(mv)
    tot_p += len(mv) ** 2
    bad_i += sum(1 for x in mv if product(x, x) != x)
    for x in mv:
        for y in mv:
            xy = product(x, y)
            if product(xy, x) != xy:
                bad_l += 1
            if not compatible(P, xy):
                bad_c += 1
print("n=5  isomorphism classes %d   x.x=x: %d bad of %d   x.y.x=x.y: %d bad of %d"
      "   closure: %d bad of %d" % (len(reps5), bad_i, tot_i, bad_l, tot_p, bad_c, tot_p))
print("[t = %.1f s]" % (time.time() - T0), file=sys.stderr)

# ==========================================================================
# C. commitment levels
# ==========================================================================

head("C.  Commitment levels, and the acyclic-cut description")

lev = commitment_levels(EX, ex_moves)
acy = acyclic_partitions(EX)
allp = list(all_partitions(4))
print("partitions of {a,b,c,d}                        : %d" % len(allp))
print("commitment levels (= the supports of the moves): %d" % len(lev))
print("partitions with acyclic quotient               : %d" % len(acy))
print("the two descriptions agree                     : %s" % (set(lev) == acy))
missing = [pi for pi in allp if pi not in acy]
print("partition(s) that are NOT commitment levels    : %s"
      % ", ".join(show_level(EX, pi) for pi in missing))
sub("each level, and the moves that sit at it")
for X in lev:
    carriers = [x for x in ex_moves if support(x) == X]
    print("   %-12s <- %s"
          % (show_level(EX, X), " ".join(show_move(EX, x) for x in carriers)))

sub("supports == acyclic partitions, checked on every LABELLED poset up to 5 elements")
for n in range(1, 6):
    ps = all_posets(n)
    agree = sum(1 for P in ps if set(commitment_levels(P)) == acyclic_partitions(P))
    print("n=%d  agrees on %d of %d labelled posets" % (n, agree, len(ps)))
print("[t = %.1f s]" % (time.time() - T0), file=sys.stderr)

# ==========================================================================
# D. multiplicities
# ==========================================================================

head("D.  Multiplicities of the worked example -- from P alone, no probabilities")

m_ex, target_ex = multiplicities(EX, lev)
print("   %-12s  %-18s  %s" % ("level X", "prod_B |L(P|_B)|", "m_X"))
for X in lev:
    print("   %-12s  %10d          %d" % (show_level(EX, X), target_ex[X], m_ex[X]))
print("sum of multiplicities: %d   (|L(P)| = %d)   equal: %s"
      % (sum(m_ex.values()), len(ex_ords), sum(m_ex.values()) == len(ex_ords)))
print("levels with a NONZERO multiplicity (%d of %d): %s"
      % (sum(1 for X in lev if m_ex[X]), len(lev),
         ", ".join(show_level(EX, X) for X in lev if m_ex[X])))

# ==========================================================================
# E. the spectrum, three times
# ==========================================================================

head("E.  The spectrum under three different weightings")

U0 = (mA | mB | mC | mD,)                # (abcd)   -- the do-nothing move
U1 = (mA, mB | mC | mD)                  # (a|bcd)
U2 = (mA | mC, mB | mD)                  # (ac|bd)
U3 = (mA | mC, mB, mD)                   # (ac|b|d)
U4 = (mA, mB | mC, mD)                   # (a|bc|d)
U5 = (mC, mA | mD, mB)                   # (c|ad|b)
U6 = (mA, mC, mB | mD)                   # (a|c|bd)
U7 = (mA, mB, mC, mD)                    # (a|b|c|d)
NAMED = [U0, U1, U2, U3, U4, U5, U6, U7]
for mv in NAMED:
    assert mv in ex_moves, show_move(EX, mv)


def weight_report(P, w, label, moves, m, levels, ords):
    sub(label)
    print("   weights (the nonzero ones):")
    for x in moves:
        if w[x]:
            print("      w%-12s = %s" % (show_move(P, x), w[x]))
    print("      total = %s" % sum(w.values()))
    lam = eigenvalues(P, w, levels)
    print("   each level's number, as a partial sum of move probabilities:")
    for X in levels:
        carriers = [x for x in moves if w[x] and refines(X, support(x))]
        expr = " + ".join("w%s" % show_move(P, x) for x in carriers) or "0"
        print("      %-12s m=%d  %-42s = %s"
              % (show_level(P, X), m[X], expr, lam[X]))
    pred = {}
    for X in levels:
        if m[X]:
            pred[lam[X]] = pred.get(lam[X], 0) + m[X]
    print("   predicted spectrum: %s"
          % ", ".join("%s (x%d)" % (v, k) for v, k in sorted(pred.items(), reverse=True)))
    M = transition_matrix(P, w, ords)
    ok, tot = True, 0
    for v, k in sorted(pred.items(), reverse=True):
        d = kernel_dim(M, v)
        tot += d
        ok &= (d == k)
        print("      dim ker(M - %s I) = %d, predicted %d   %s"
              % (v, d, k, "OK" if d == k else "MISMATCH"))
    print("   dimensions sum to %d of %d  ->  %s" % (tot, len(ords),
          "spectrum confirmed and M is diagonalisable"
          if ok and tot == len(ords) else "FAILED"))
    return pred


def weighting(counts):
    w = {x: F(0) for x in ex_moves}
    for mv, c in zip(NAMED, counts):
        w[mv] = F(c, 32)
    assert sum(w.values()) == 1, sum(w.values())
    return w


#                 U0 U1 U2 U3 U4 U5 U6 U7   (thirty-secondths, summing to 32)
w1 = weighting([   4, 6, 2, 3, 5, 7, 1, 4])
w2 = weighting([   8, 4, 3, 2, 6, 3, 2, 4])
w3 = weighting([   2, 3, 5, 1, 6, 7, 4, 4])

p1 = weight_report(EX, w1, "weighting w1", ex_moves, m_ex, lev, ex_ords)
p2 = weight_report(EX, w2, "weighting w2 -- same poset, different numbers",
                   ex_moves, m_ex, lev, ex_ords)
p3 = weight_report(EX, w3, "weighting w3 -- different again", ex_moves, m_ex,
                   lev, ex_ords)

sub("the comparison that is the point of the note")
for nm, w, p in (("w1", w1, p1), ("w2", w2, p2), ("w3", w3, p3)):
    lam = eigenvalues(EX, w, lev)
    print("   %s  level->eigenvalue : %s"
          % (nm, ", ".join("%s=%s" % (show_level(EX, X), lam[X])
                           for X in lev if m_ex[X])))
    print("       distinct eigenvalues %s with multiplicities %s"
          % (", ".join(str(v) for v in sorted(p, reverse=True)),
             [p[v] for v in sorted(p, reverse=True)]))
print("   the three eigenvalue lists are pairwise different : %s"
      % (len({tuple(sorted(p)) for p in (p1, p2, p3)}) == 3))
print("   the level -> multiplicity table did not move; it never saw a probability:")
print("      %s" % ", ".join("%s:%d" % (show_level(EX, X), m_ex[X]) for X in lev))
print("   NOTE the one thing that DOES depend on w: two levels can land on the")
print("   same number, and then that number's multiplicity is the sum.  Under w2,")
print("   ac|bd and ad|b|c both give 11/32, so 11/32 has multiplicity 2 while each")
print("   LEVEL still has multiplicity 1.  Under w1 and w3 all six are distinct.")
print("[t = %.1f s]" % (time.time() - T0), file=sys.stderr)

# ==========================================================================
# F. the antichain
# ==========================================================================

head("F.  The antichain: the classical shuffle setting")

FUBINI = {1: 1, 2: 3, 3: 13, 4: 75, 5: 541}

sub("with no relations the orderings ARE S_n and the moves are ALL ordered set"
    " partitions -- the face semigroup of the braid arrangement")
for n in range(1, 6):
    AN = Poset(n, [])
    mv = set(moves_of(AN))
    allo = set(ordered_set_partitions(n))
    print("n=%d  |L(P)| = %-3d = n! : %-5s   moves %3d   all ordered set partitions %3d"
          "   equal: %-5s   = Fubini(n) = %d : %s"
          % (n, len(linear_extensions(AN)),
             len(linear_extensions(AN)) == math.factorial(n),
             len(mv), len(allo), mv == allo, FUBINI[n], len(mv) == FUBINI[n]))

sub("every partition is a commitment level, and m_X = prod_B (|B|-1)!")
for n in range(2, 6):
    AN = Poset(n, [])
    levels = commitment_levels(AN)
    m, _ = multiplicities(AN, levels)
    ok_all = len(levels) == len(list(all_partitions(n)))
    ok_form = all(m[X] == math.prod([math.factorial(len(bits(Bk)) - 1) for Bk in X])
                  for X in levels)
    print("n=%d  levels %3d  (= all partitions: %s)   m_X = prod_B (|B|-1)! : %s"
          "   sum m_X = %d = n! : %s"
          % (n, len(levels), ok_all, ok_form, sum(m.values()),
             sum(m.values()) == math.factorial(n)))


def derangements(k):
    d = [1, 0]
    while len(d) <= k:
        mm = len(d) - 1
        d.append(mm * (d[mm] + d[mm - 1]))
    return d[k]


sub("instance 1 -- move-to-front / the Tsetlin library: weight only the moves ({i}, rest)")
for n in range(2, 6):
    AN = Poset(n, [])
    levels = commitment_levels(AN)
    m, _ = multiplicities(AN, levels)
    tot = sum(range(1, n + 1))
    w = {}
    single = {}
    for i in range(n):
        rest = ((1 << n) - 1) ^ (1 << i)
        x = (1 << i, rest)
        single[i] = x
        w[x] = F(i + 1, tot)
    lam = eigenvalues(AN, w, levels)
    grp = {}
    for X in levels:
        if m[X]:
            grp[lam[X]] = grp.get(lam[X], 0) + m[X]
    classical = {}
    for r in range(n + 1):
        for S in itertools.combinations(range(n), r):
            v = sum((w[single[i]] for i in S), F(0))
            d = derangements(n - r)
            if d:
                classical[v] = classical.get(v, 0) + d
    verdict = ""
    if n <= 4:
        ords = linear_extensions(AN)
        M = transition_matrix(AN, w, ords)
        good = all(kernel_dim(M, v) == k for v, k in grp.items())
        good &= sum(kernel_dim(M, v) for v in grp) == len(ords)
        verdict = "   against the matrix: %s" % ("OK, diagonalisable" if good else "FAILED")
    print("n=%d  %2d distinct eigenvalues   Brown prediction == classical "
          "derangement spectrum (lambda_S = sum_{i in S} w_i, multiplicity D(n-|S|)): %s%s"
          % (n, len(grp), grp == classical, verdict))

sub("instance 2 -- the inverse a-riffle shuffle (Gilbert-Shannon-Reeds)")
print("   GSR: label each card i.i.d. uniform in {1..a}, stably sort by label.")
print("   That IS the action of the move whose blocks are the label classes.")
for n in range(2, 6):
    for a in (2, 3):
        AN = Poset(n, [])
        mv = moves_of(AN)
        levels = commitment_levels(AN)
        m, _ = multiplicities(AN, levels)
        w = {x: F(math.comb(a, len(x)), a ** n) for x in mv}
        assert sum(w.values()) == 1, (n, a, sum(w.values()))
        direct = {}
        for lab in itertools.product(range(a), repeat=n):
            blocks = {}
            for e, t in enumerate(lab):
                blocks[t] = blocks.get(t, 0) | (1 << e)
            x = tuple(blocks[t] for t in sorted(blocks))
            direct[x] = direct.get(x, F(0)) + F(1, a ** n)
        gsr_ok = all(direct.get(x, F(0)) == w[x] for x in mv)
        lam = eigenvalues(AN, w, levels)
        eig_ok = all(lam[X] == F(a ** len(X), a ** n) for X in levels)
        grp = {}
        for X in levels:
            if m[X]:
                grp[lam[X]] = grp.get(lam[X], 0) + m[X]
        stirling = {}
        for perm in itertools.permutations(range(n)):
            seen, cyc = set(), 0
            for s in range(n):
                if s in seen:
                    continue
                cyc += 1
                t = s
                while t not in seen:
                    seen.add(t)
                    t = perm[t]
            stirling[cyc] = stirling.get(cyc, 0) + 1
        classical = {}
        for k, cnt in stirling.items():
            v = F(a ** k, a ** n)
            classical[v] = classical.get(v, 0) + cnt
        verdict = ""
        if n <= 4:
            ords = linear_extensions(AN)
            idx = {c: t for t, c in enumerate(ords)}
            M = [[F(0)] * len(ords) for _ in ords]
            for c in ords:
                pos = {e: t for t, e in enumerate(c)}
                for lab in itertools.product(range(a), repeat=n):
                    out = tuple(sorted(c, key=lambda e: (lab[e], pos[e])))
                    M[idx[c]][idx[out]] += F(1, a ** n)
            good = all(kernel_dim(M, v) == k for v, k in grp.items())
            good &= sum(kernel_dim(M, v) for v in grp) == len(ords)
            verdict = "   GSR matrix (built with no semigroup): %s" % (
                "OK, diagonalisable" if good else "FAILED")
        print("n=%d a=%d  w == GSR law: %-5s  lambda_X = a^(|X|-n): %-5s  "
              "spectrum == classical a^-j with Stirling multiplicities: %-5s%s"
              % (n, a, gsr_ok, eig_ok, grp == classical, verdict))
print("[t = %.1f s]" % (time.time() - T0), file=sys.stderr)

sub("instance 3 -- which classical shuffles are NOT in the family")
print("   Necessary condition, no nonnegativity needed: the target matrix must lie")
print("   in the LINEAR SPAN of the matrices T_x, x a move.  Exact rank test.")


def in_span(P, target, ords):
    mv = moves_of(P)
    idx = {c: t for t, c in enumerate(ords)}
    N = len(ords)
    cols = []
    for x in mv:
        v = [F(0)] * (N * N)
        for c in ords:
            v[idx[c] * N + idx[act(x, c)]] += 1
        cols.append(v)
    b = [target[i][j] for i in range(N) for j in range(N)]
    A = [[cols[k][r] for k in range(len(cols))] for r in range(N * N)]
    Ab = [A[r] + [b[r]] for r in range(N * N)]
    return rank(A) == rank(Ab)


for n in (3, 4):
    AN = Poset(n, [])
    ords = linear_extensions(AN)
    idx = {c: t for t, c in enumerate(ords)}
    N = len(ords)

    def blank():
        return [[F(0)] * N for _ in range(N)]

    # top-to-random: take the first element, insert it in a uniform position
    ttr = blank()
    for c in ords:
        rest = c[1:]
        for pos in range(n):
            d = rest[:pos] + (c[0],) + rest[pos:]
            ttr[idx[c]][idx[d]] += F(1, n)
    # random transpositions (Diaconis-Shahshahani): pick i,j uniform, swap
    rt = blank()
    for c in ords:
        for i in range(n):
            for j in range(n):
                d = list(c)
                d[i], d[j] = d[j], d[i]
                rt[idx[c]][idx[tuple(d)]] += F(1, n * n)
    # lazy adjacent transpositions
    at = blank()
    for c in ords:
        stay = F(1)
        for t in range(n - 1):
            d = list(c)
            d[t], d[t + 1] = d[t + 1], d[t]
            at[idx[c]][idx[tuple(d)]] += F(1, 2 * (n - 1))
            stay -= F(1, 2 * (n - 1))
        at[idx[c]][idx[c]] += stay
    # random-to-top (the Tsetlin library with uniform weights) -- a control:
    # this one IS in the family, so the test must say so
    r2t = blank()
    for c in ords:
        for i in range(n):
            x = (1 << c[i], ((1 << n) - 1) ^ (1 << c[i]))
            r2t[idx[c]][idx[act(x, c)]] += F(1, n)
    for label, M in (("random-to-top (control: IS in the family)", r2t),
                     ("top-to-random", ttr),
                     ("random transpositions", rt),
                     ("lazy adjacent transpositions", at)):
        print("   n=%d  %-42s in the linear span of the moves: %s"
              % (n, label, in_span(AN, M, ords)))


# ==========================================================================
# G. the boundary
# ==========================================================================

head("G.  The boundary: the adjacent-transposition walk is not in the family")

print("The lazy AT walk gives every AT-neighbour of every ordering probability")
print("1/(2(n-1)).  Weights are nonnegative, so a move x is usable only if x.c is")
print("c or an AT-neighbour of c for EVERY ordering c.  If some AT edge is then")
print("unreachable, no weighting reproduces the walk.  (Sufficient, not necessary.)")


def at_neighbours(c, ords):
    s = set()
    for t in range(len(c) - 1):
        d = list(c)
        d[t], d[t + 1] = d[t + 1], d[t]
        d = tuple(d)
        if d in ords:
            s.add(d)
    return s


for n in range(2, 6):
    reps = iso_classes(n)
    notin = vac = undec = 0
    for P in reps:
        ords = set(linear_extensions(P))
        if len(ords) == 1:
            vac += 1
            continue
        mv = moves_of(P)
        nbr = {c: at_neighbours(c, ords) for c in ords}
        cand = [x for x in mv
                if all(act(x, c) == c or act(x, c) in nbr[c] for c in ords)]
        reachable = {(c, act(x, c)) for x in cand for c in ords if act(x, c) != c}
        needed = {(c, d) for c in ords for d in nbr[c]}
        if needed - reachable:
            notin += 1
        else:
            undec += 1
    print("n=%d  isomorphism classes %2d :  provably NOT in the family %2d   "
          "single ordering (vacuous) %d   not decided by this test %d"
          % (n, len(reps), notin, vac, undec))

sub("the antichain specifically")
for n in range(2, 6):
    AN = Poset(n, [])
    ords = set(linear_extensions(AN))
    mv = moves_of(AN)
    nbr = {c: at_neighbours(c, ords) for c in ords}
    cand = [x for x in mv if all(act(x, c) == c or act(x, c) in nbr[c] for c in ords)]
    reachable = {(c, act(x, c)) for x in cand for c in ords if act(x, c) != c}
    needed = {(c, d) for c in ords for d in nbr[c]}
    print("n=%d  usable moves %d   AT edges needed %3d   of these supplied %3d   "
          "-> AT walk in the family? %s"
          % (n, len(cand), len(needed), len(needed & reachable),
             "yes" if not (needed - reachable) else "NO"))

print()
print("=" * 78)
print("done"); print("[t = %.1f s]" % (time.time() - T0), file=sys.stderr)
print("=" * 78)
