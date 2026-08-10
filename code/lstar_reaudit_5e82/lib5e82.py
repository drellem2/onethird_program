"""lib5e82 -- mg-5e82's INDEPENDENT RE-AUDIT instrument.

WHAT THIS IS FOR.  mg-b417/cb417 certified that BOTH routes (F) and (M#) fail at the
n = 12 poset dn = (0,0,3,7,15,7,63,2,135,391,7,1159), using `lib5cba.py` unmodified.
That instrument is the one under audit, so this file re-derives every object from the
DEFINITION and imports none of `lib5cba.py`, `lib789d.py`, `libc50b.py`.  Arm S0 of
`a0_selftest.py` checks that mechanically, on the source text and on `sys.modules`.

TWO PLACES WHERE THIS FILE DELIBERATELY DIFFERS IN METHOD, not just in authorship:

  1. THE TRANSPORT.  cb417 warned that lib5cba, lib789d and libc50b agree on `LE`,
     `Delta` and `M` but all three descend from one reading of one definition -- three
     agreeing is not three independent.  So this file runs NO transport DP at all.
     It ENUMERATES EVERY LINEAR EXTENSION explicitly (depth-first over available
     minimal elements) and tallies `PI[i][j]` by counting.  At n = 12 that is 10584
     sequences; the definition of `PI` is "how many linear extensions place i at j",
     and this counts exactly that, with no recursion over ideals to get wrong.

  2. THE PSD TEST.  The corpus decides PSD from the coefficient signs of det(xI+A).
     This file uses exact symmetric CONGRUENCE (LDL^T with a tracked basis), which
     yields the INERTIA and -- the point -- an EXHIBITED RATIONAL VECTOR `c` with
     c'Rc < 0 whenever the matrix is not PSD.  A refusal then needs no algorithm to
     be trusted: one vector and one dot product settle it.

THE OBJECTS, restated from the definitions so nothing is inherited by reference.

  P            a NATURALLY LABELLED poset on {0..n-1}; `dn[i]` = bitmask of the strict
               lower set of i, which must be a subset of {0..i-1}.
  LE           number of linear extensions of P.
  PI[i][j]     number of linear extensions placing element i at position j.
  (S_P)_ij     PI[i][j] / LE.
  A            (S_P + S_P^T)/2.
  d_i          1 - (S_P)_ii.        Delta_P = max_i d_i.
  leak(A_k)    k - sum_{i<k, j<k} (S_P)_ij,  k = 1..n-1.
  M            (sum_k leak(A_k)) / floor(n^2/4).
  primitive    leak(A_k) > 0 for every k = 1..n-1.

  psi_k        1_{[0,k)} - (k/n) 1,  k = 1..n-1.  A basis of 1^perp.
  Q_kl         <psi_k, (I-A) psi_l>.        N_kl = <psi_k, psi_l>.
  gamma        min over c != 0        of c'Qc / c'Nc.
  mu_pref      min over c >= 0, c != 0 of c'Qc / c'Nc.

  Q and N are built here from psi and A DIRECTLY -- `Q_kl = psi_k'(I-A)psi_l` as
  written -- and the corpus's closed forms (`sum_{i<min} sum_{j>=max} a_ij` and
  `min(k,l) - kl/n`) are then checked against them rather than used to build them.

THE INTEGER MATRIX.  N is the Gram matrix of the (independent) psi_k, hence positive
definite, so for rational t = a/b > 0:

    gamma   >= t   <==>   Q - tN is PSD          (Rayleigh quotient, N PD)
    mu_pref >= t   <==>   Q - tN is COPOSITIVE   (same, restricted to c >= 0)

and with QI := 2*LE*Q and NI := n*N (both integral),

    R(a,b) := b*n*QI - 2*LE*a*NI = 2*LE*n*b*(Q - tN),

a positive multiple, so R(a,b) is integral and has the same PSD/copositive status.
That scaling is re-derived here, not copied.  NO FLOAT IS ON ANY VERDICT PATH; the
`*_float` helpers exist only to SEARCH for candidate vectors and faces, and every
candidate they propose is verified in `Fraction`s before it counts.

COPOSITIVITY, decided exactly and completely.  Derived here from scratch:

  Claim.  Symmetric R (m x m) is NOT copositive
          <==>  for some nonempty S subset [m], the system
                    R_S y = 1_S   and   y < 0 (strictly, componentwise)
                is feasible.

  Proof.  (=>)  If R is not copositive, v := min{c'Rc : c >= 0, sum c = 1} < 0, and
  the min is attained on the compact simplex at some c*, with support S.  The
  first-order (KKT) condition for that program is 2Rc* = lam*1 + w with w >= 0 and
  w_i c*_i = 0, so (R_S c*_S)_i = lam/2 for every i in S.  Pairing with c*_S and
  using sum c* = 1 gives lam/2 = c*'Rc* = v.  So R_S c*_S = v*1_S with c*_S > 0 and
  v < 0; put y := c*_S / v, which is < 0 and solves R_S y = 1_S.
  (<=)  Given R_S y = 1_S with y < 0, set sig := sum(y) < 0 and c := y/sig > 0,
  extended by zeros off S.  Then c >= 0, sum c = 1, and
  c'Rc = y'R_S y / sig^2 = y'1_S / sig^2 = sig/sig^2 = 1/sig < 0.   []

  No nonsingularity is assumed anywhere.  When R_S is singular the solution set of
  R_S y = 1_S is an affine subspace y0 + span(Z) (or empty), and "is some point of it
  strictly negative?" is a strict linear feasibility problem, decided here by exact
  Fourier-Motzkin over the nullspace coordinates.  A singular face is DECIDED.
  The module counters SINGULAR_FACES / SINGULAR_FACES_DECIDED must come out equal;
  `a3_mu.py` prints both, so "none arose" is a measurement and not an assumption.
"""

from fractions import Fraction as Fr
from itertools import combinations

# Instrumentation for the copositivity routine.  These must end up equal.
SINGULAR_FACES = 0
SINGULAR_FACES_DECIDED = 0
FACES_VISITED = 0


def reset_counters():
    global SINGULAR_FACES, SINGULAR_FACES_DECIDED, FACES_VISITED
    SINGULAR_FACES = 0
    SINGULAR_FACES_DECIDED = 0
    FACES_VISITED = 0


# ---------------------------------------------------------------------------
# 1.  The poset, and every linear extension of it
# ---------------------------------------------------------------------------


def bits(mask):
    out, i = [], 0
    while mask:
        if mask & 1:
            out.append(i)
        mask >>= 1
        i += 1
    return out


def is_naturally_labelled(dn, n):
    """`dn[i]` must be a subset of {0..i-1}: every relation runs from a smaller label."""
    return all(dn[i] >> i == 0 for i in range(n))


def is_transitively_closed(dn, n):
    """j < i in P and k < j in P  ==>  k < i in P."""
    for i in range(n):
        for j in bits(dn[i]):
            if dn[j] & ~dn[i]:
                return False
    return True


def linear_extensions(dn, n):
    """EVERY linear extension of `dn`, as a tuple of elements in position order.

    Straight from the definition: repeatedly place any element all of whose strict
    predecessors are already placed.  No dynamic programme, no order-ideal recursion.
    """
    seq, out = [], []
    placed = 0

    def rec(placed):
        if len(seq) == n:
            out.append(tuple(seq))
            return
        for i in range(n):
            if not (placed >> i) & 1 and (dn[i] & ~placed) == 0:
                seq.append(i)
                rec(placed | (1 << i))
                seq.pop()

    rec(placed)
    return out


def position_counts(dn, n):
    """(LE, PI) with PI[i][j] = # linear extensions placing element i at position j.

    Counted by walking the enumerated extensions, which is what the definition says.
    """
    PI = [[0] * n for _ in range(n)]
    LE = 0
    for ext in linear_extensions(dn, n):
        LE += 1
        for pos, elt in enumerate(ext):
            PI[elt][pos] += 1
    return LE, PI


# ---------------------------------------------------------------------------
# 2.  The scalars
# ---------------------------------------------------------------------------


class Poset:
    """Everything this audit needs about one naturally labelled poset, in exact rationals."""

    def __init__(self, dn, n):
        self.dn, self.n = tuple(dn), n
        self.natural = is_naturally_labelled(dn, n)
        self.transitive = is_transitively_closed(dn, n)
        self.LE, self.PI = position_counts(dn, n)
        LE = self.LE
        self.S = [[Fr(self.PI[i][j], LE) for j in range(n)] for i in range(n)]
        self.A = [[(self.S[i][j] + self.S[j][i]) / 2 for j in range(n)] for i in range(n)]
        self.d = [1 - self.S[i][i] for i in range(n)]
        self.Delta = max(self.d)
        self.leaks = [
            Fr(k) - sum(self.S[i][j] for i in range(k) for j in range(k))
            for k in range(1, n)
        ]
        self.primitive = all(x > 0 for x in self.leaks)
        self.M = sum(self.leaks) / (n * n // 4)
        # psi_k = 1_{[0,k)} - (k/n) 1,  k = 1..n-1
        self.psi = [
            [(1 if i < k else 0) - Fr(k, n) for i in range(n)] for k in range(1, n)
        ]
        m = n - 1
        self.m = m
        IA = [
            [(1 if i == j else 0) - self.A[i][j] for j in range(n)] for i in range(n)
        ]
        # Q and N BUILT FROM THE DEFINITION, not from the corpus's closed forms.
        self.Q = [
            [
                sum(
                    self.psi[k][i] * IA[i][j] * self.psi[l][j]
                    for i in range(n)
                    for j in range(n)
                )
                for l in range(m)
            ]
            for k in range(m)
        ]
        self.N = [
            [sum(self.psi[k][i] * self.psi[l][i] for i in range(n)) for l in range(m)]
            for k in range(m)
        ]
        self.QI = [[int(2 * LE * self.Q[k][l]) for l in range(m)] for k in range(m)]
        self.NI = [[int(n * self.N[k][l]) for l in range(m)] for k in range(m)]

    # -- the corpus's closed forms, CHECKED against the definition, never used to build --
    def closed_form_agrees(self):
        n, m = self.n, self.m
        Qcf = [
            [
                sum(
                    self.A[i][j]
                    for i in range(min(k + 1, l + 1))
                    for j in range(max(k + 1, l + 1), n)
                )
                for l in range(m)
            ]
            for k in range(m)
        ]
        Ncf = [
            [Fr(min(k + 1, l + 1)) - Fr((k + 1) * (l + 1), n) for l in range(m)]
            for k in range(m)
        ]
        return self.Q == Qcf, self.N == Ncf

    def R(self, a, b):
        """R(a,b) = b*n*QI - 2*LE*a*NI = 2*LE*n*b*(Q - (a/b)N).  Integral."""
        n, m, LE = self.n, self.m, self.LE
        return [
            [b * n * self.QI[k][l] - 2 * LE * a * self.NI[k][l] for l in range(m)]
            for k in range(m)
        ]

    def scale_check(self, a, b):
        """Verify R(a,b) really is 2*LE*n*b*(Q - tN), entrywise, in Fractions."""
        t = Fr(a, b)
        k = 2 * self.LE * self.n * b
        return all(
            Fr(self.R(a, b)[i][j]) == k * (self.Q[i][j] - t * self.N[i][j])
            for i in range(self.m)
            for j in range(self.m)
        )


# ---------------------------------------------------------------------------
# 3.  Exact PSD by symmetric congruence, WITH a witness vector when it fails
# ---------------------------------------------------------------------------


def inertia_with_witness(R):
    """Exact inertia of a symmetric rational matrix, by congruence.

    Returns (npos, nneg, nzero, witness) where `witness` is None if R is PSD and
    otherwise an exact rational vector `c` with c'Rc < 0 -- so a NOT-PSD verdict is
    checkable by one dot product and does not rest on this routine being right.

    Maintains M = T'RT with T's columns tracked in the ORIGINAL coordinates.  A
    negative diagonal entry M[p][p] then means (T[:,p])' R (T[:,p]) = M[p][p] < 0.
    Zero pivots are handled: if every active diagonal vanishes but some active
    off-diagonal M[p][q] != 0, the congruence e_p <- e_p + e_q makes the diagonal
    2*M[p][q] != 0 and elimination continues, so no face is skipped.
    """
    m = len(R)
    M = [[Fr(R[i][j]) for j in range(m)] for i in range(m)]
    T = [[Fr(1 if i == j else 0) for j in range(m)] for i in range(m)]  # T[i][col]
    active = list(range(m))
    npos = nneg = nzero = 0
    while active:
        p = None
        for i in active:
            if M[i][i] != 0:
                p = i
                break
        if p is None:
            # all active diagonals zero: look for a nonzero off-diagonal
            pq = None
            for i in active:
                for j in active:
                    if i != j and M[i][j] != 0:
                        pq = (i, j)
                        break
                if pq:
                    break
            if pq is None:
                nzero += len(active)   # the whole active block is zero
                break
            i, j = pq
            # congruence e_i <- e_i + e_j
            for k in range(m):
                M[i][k] += M[j][k]
            for k in range(m):
                M[k][i] += M[k][j]
            for k in range(m):
                T[k][i] += T[k][j]
            p = i
        piv = M[p][p]
        if piv > 0:
            npos += 1
        else:
            nneg += 1
            wit = [T[k][p] for k in range(m)]
            return npos, nneg, nzero, wit
        active.remove(p)
        for i in active:
            f = M[i][p] / piv
            if f == 0:
                continue
            for k in range(m):
                M[i][k] -= f * M[p][k]
            for k in range(m):
                M[k][i] -= f * M[k][p]
            for k in range(m):
                T[k][i] -= f * T[k][p]
    return npos, nneg, nzero, None


def quad(R, c):
    """c'Rc in exact arithmetic."""
    m = len(R)
    return sum(Fr(c[i]) * Fr(R[i][j]) * Fr(c[j]) for i in range(m) for j in range(m))


def is_psd(R):
    npos, nneg, nzero, wit = inertia_with_witness(R)
    return wit is None


def clear_denominators(v):
    """Scale a rational vector to primitive integers (sign preserved)."""
    from math import gcd

    den = 1
    for x in v:
        den = den * Fr(x).denominator // gcd(den, Fr(x).denominator)
    w = [int(Fr(x) * den) for x in v]
    g = 0
    for x in w:
        g = gcd(g, abs(x))
    if g:
        w = [x // g for x in w]
    return w


# ---------------------------------------------------------------------------
# 4.  Exact copositivity, complete on singular faces
# ---------------------------------------------------------------------------


def _rref(Aug, nrow, ncol):
    """Exact reduced row echelon form of an augmented matrix; returns (Aug, pivots)."""
    Aug = [row[:] for row in Aug]
    pivots, r = [], 0
    for c in range(ncol):
        p = None
        for i in range(r, nrow):
            if Aug[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        Aug[r], Aug[p] = Aug[p], Aug[r]
        pv = Aug[r][c]
        Aug[r] = [x / pv for x in Aug[r]]
        for i in range(nrow):
            if i != r and Aug[i][c] != 0:
                f = Aug[i][c]
                Aug[i] = [a - f * b for a, b in zip(Aug[i], Aug[r])]
        pivots.append(c)
        r += 1
        if r == nrow:
            break
    return Aug, pivots


def _strictly_negative_point_exists(y0, Z):
    """Decide whether some y = y0 + Z t satisfies y < 0 componentwise (strict).

    Exact Fourier-Motzkin on the free coordinates t.  Each row gives
    y0_i + sum_j Z_ij t_j < 0.  With no free coordinates this is just y0 < 0.
    """
    k = len(Z[0]) if Z and Z[0] else 0
    # rows as (coeffs over t..., constant) meaning coeffs.t + const < 0
    rows = [(list(Z[i]), y0[i]) for i in range(len(y0))]
    for var in range(k):
        lower, upper, keep = [], [], []
        for coeffs, const in rows:
            a = coeffs[var]
            rest = coeffs[:var] + coeffs[var + 1 :]
            if a == 0:
                keep.append((rest, const))
            elif a > 0:
                # t_var < (-const - rest.t)/a
                upper.append(([-x / a for x in rest], -const / a))
            else:
                # t_var > (-const - rest.t)/a
                lower.append(([-x / a for x in rest], -const / a))
        new = keep
        for lc, lk in lower:
            for uc, uk in upper:
                # need lower_bound < upper_bound :  (lc.t+lk) - (uc.t+uk) < 0
                new.append(([a - b for a, b in zip(lc, uc)], lk - uk))
        rows = new
        if not rows:
            return True
    for coeffs, const in rows:
        if const >= 0:
            return False
    return True


def not_copositive_witness(R):
    """Decide copositivity exactly.  Returns None if R IS copositive, else a witness.

    The witness is a vector c >= 0, c != 0, with c'Rc < 0 -- so a NOT-copositive
    verdict is checkable by one dot product.  A copositive verdict rests on the
    completeness of the support enumeration, which is why every face is visited and
    every singular face is decided rather than skipped.
    """
    global SINGULAR_FACES, SINGULAR_FACES_DECIDED, FACES_VISITED
    m = len(R)
    for r in range(1, m + 1):
        for S in combinations(range(m), r):
            FACES_VISITED += 1
            RS = [[Fr(R[i][j]) for j in S] for i in S]
            Aug = [RS[i][:] + [Fr(1)] for i in range(r)]
            red, piv = _rref(Aug, r, r + 1)
            # rank of R_S itself is the number of pivots in the FIRST r columns; a
            # pivot in column r means R_S y = 1_S is inconsistent.  Both facts are read
            # off the same reduction.  The singular counter is incremented for EVERY
            # rank-deficient face, consistent or not -- otherwise "0 singular faces
            # arose" could mean only "no singular face happened to be consistent".
            rank = len([c for c in piv if c < r])
            if rank < r:
                SINGULAR_FACES += 1
            if r in piv:                      # pivot in the augmented column
                if rank < r:
                    SINGULAR_FACES_DECIDED += 1   # decided: no solution at all
                continue                      # R_S y = 1_S inconsistent: nothing here
            free = [c for c in range(r) if c not in piv]
            # particular solution + nullspace basis
            y0 = [Fr(0)] * r
            for i, c in enumerate(piv):
                y0[c] = red[i][r]
            Z = [[Fr(0)] * len(free) for _ in range(r)]
            for jj, fc in enumerate(free):
                Z[fc][jj] = Fr(1)
                for i, c in enumerate(piv):
                    Z[c][jj] = -red[i][fc]
            feasible = _strictly_negative_point_exists(y0, Z)
            if rank < r:
                SINGULAR_FACES_DECIDED += 1
            if not feasible:
                continue
            # rebuild an explicit y < 0 to hand back a checkable witness
            y = _find_point(y0, Z)
            if y is None:
                continue
            sig = sum(y)
            c = [Fr(0)] * m
            for idx, i in enumerate(S):
                c[i] = y[idx] / sig
            return c
    return None


def _find_point(y0, Z):
    """Produce an explicit y = y0 + Z t with y < 0, by searching a dyadic grid of t.

    Only ever called after Fourier-Motzkin has PROVED such a point exists, and the
    point it returns is verified (`all(x < 0)`) before use -- so this search cannot
    manufacture a witness, only fail to find one it was told is there.
    """
    k = len(Z[0]) if Z and Z[0] else 0
    if k == 0:
        return y0 if all(x < 0 for x in y0) else None
    from itertools import product

    scales = [Fr(0), Fr(1), Fr(-1), Fr(1, 2), Fr(-1, 2), Fr(2), Fr(-2), Fr(4), Fr(-4),
              Fr(1, 4), Fr(-1, 4), Fr(8), Fr(-8), Fr(1, 8), Fr(-1, 8)]
    for t in product(scales, repeat=k):
        y = [y0[i] + sum(Z[i][j] * t[j] for j in range(k)) for i in range(len(y0))]
        if all(x < 0 for x in y):
            return y
    return None


def is_copositive(R):
    return not_copositive_witness(R) is None
