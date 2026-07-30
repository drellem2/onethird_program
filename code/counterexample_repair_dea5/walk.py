"""Moves, the actual transition matrix, and the spectrum -- for arbitrary weights.

A MOVE is a P-compatible ordered set partition (B_1, ..., B_k): the blocks in that
order have no P-relation running backwards.  It acts on a linear extension by
listing B_1's elements in L-order, then B_2's, and so on.  That action is built
here from its definition and the matrix is assembled entry by entry; nothing
about the spectrum is assumed.

For a probability weight w on the moves of P:

    lambda_X  =  sum of w over moves whose LEVEL is coarser than or equal to X
    s(x,y)    =  sum of w over moves that leave x and y in the same block

and the claim under test (the target's Theorem 4, in the generality its proof
has) is that the second eigenvalue

    lambda_2  :=  max { lambda_X : m_X > 0, X != the finest partition }

equals max over incomparable pairs {x,y} of s(x,y), FOR EVERY WEIGHT.

The spectrum claim itself -- that the eigenvalues of the matrix are exactly the
lambda_X with multiplicities m_X -- is checked against the actual matrix through
the power sums trace(M^k) = sum_X m_X lambda_X^k for k = 1..N, which determine an
eigenvalue multiset uniquely (Newton's identities).  No eigensolver, no floats.
"""

from fractions import Fraction

from poset import _bits
from levels import all_levels, block_digraph, m_table


def linear_extensions(P):
    """Every linear extension of P, as a tuple of elements bottom-up."""
    n = P.n
    out = []
    full = (1 << n) - 1

    def rec(placed, seq):
        if placed == full:
            out.append(tuple(seq))
            return
        for v in range(n):
            if placed >> v & 1:
                continue
            if P.down[v] & ~placed:
                continue
            seq.append(v)
            rec(placed | (1 << v), seq)
            seq.pop()

    rec(0, [])
    return out


def topological_orders(k, adj):
    """Every linear order of 0..k-1 with all adj-arrows pointing forwards."""
    out = []

    def rec(used, seq):
        if len(seq) == k:
            out.append(tuple(seq))
            return
        for v in range(k):
            if used >> v & 1:
                continue
            # every predecessor of v must already be placed
            ok = True
            for u in range(k):
                if u != v and (adj[u] >> v & 1) and not (used >> u & 1):
                    ok = False
                    break
            if ok:
                seq.append(v)
                rec(used | (1 << v), seq)
                seq.pop()

    rec(0, [])
    return out


def all_moves(P):
    """Every P-compatible ordered set partition, as a tuple of block masks."""
    out = []
    for X in all_levels(P):
        adj = block_digraph(P, X)
        for order in topological_orders(len(X), adj):
            out.append(tuple(X[i] for i in order))
    return out


def apply_move(move, L):
    pos = {v: i for i, v in enumerate(L)}
    seq = []
    for B in move:
        seq.extend(sorted(_bits(B), key=lambda v: pos[v]))
    return tuple(seq)


def transition_matrix(P, moves, weights):
    """M[i][j] = total weight of moves sending state j to state i."""
    L = linear_extensions(P)
    idx = {s: i for i, s in enumerate(L)}
    N = len(L)
    M = [[Fraction(0) for _ in range(N)] for _ in range(N)]
    for mv, w in zip(moves, weights):
        if w == 0:
            continue
        for j, s in enumerate(L):
            t = apply_move(mv, s)
            M[idx[t]][j] += w
    return M, L


def level_of(move):
    return tuple(sorted(move))


def refines(X, Y):
    """X refines Y: every block of X sits inside a block of Y."""
    return all(any(B & C == B for C in Y) for B in X)


def lambdas(P, moves, weights):
    """{level: lambda_X} for every level X of P."""
    levs = [tuple(sorted(X)) for X in all_levels(P)]
    mlev = [level_of(mv) for mv in moves]
    out = {}
    for X in levs:
        tot = Fraction(0)
        for lv, w in zip(mlev, weights):
            if refines(X, lv):          # lv is coarser than or equal to X
                tot += w
        out[X] = tot
    return out


def same_block_mass(P, moves, weights):
    """s(x,y) for every incomparable pair."""
    out = {}
    for (x, y) in P.incomparable_pairs():
        tot = Fraction(0)
        for mv, w in zip(moves, weights):
            for B in mv:
                if (B >> x & 1) and (B >> y & 1):
                    tot += w
                    break
        out[(x, y)] = tot
    return out


def multiplicities(P, cache=None):
    """{level: m_X} from the factorisation lemma of levels.py."""
    Mm, _ = m_table(P, cache)
    out = {}
    for X in all_levels(P):
        prod = 1
        for B in X:
            prod *= Mm[B]
        out[tuple(sorted(X))] = prod
    return out


def lambda_2(lam, mult):
    """max lambda over levels with positive multiplicity other than the finest."""
    n_finest = max(len(X) for X in lam)
    best = None
    for X, v in lam.items():
        if len(X) == n_finest:
            continue                     # the finest partition: the eigenvalue 1
        if mult[X] <= 0:
            continue
        if best is None or v > best:
            best = v
    return best


def power_sums_agree(M, lam, mult):
    """trace(M^k) == sum_X m_X lambda_X^k for k = 1..N.  Exact."""
    N = len(M)
    A = [row[:] for row in M]
    for k in range(1, N + 1):
        tr = sum(A[i][i] for i in range(N))
        want = Fraction(0)
        for X, v in lam.items():
            if mult[X]:
                want += mult[X] * v ** k
        if tr != want:
            return False, k, tr, want
        if k < N:
            A = [[sum(A[i][t] * M[t][j] for t in range(N)) for j in range(N)]
                 for i in range(N)]
    return True, None, None, None
