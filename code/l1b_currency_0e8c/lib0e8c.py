"""lib0e8c -- mg-0e8c's instrument for DANIEL'S CHALLENGE TO ROW 8.

The question is whether `eps_sup < 1` discharges STATE.md row 8 AS STATED, and whether the
stated form is not merely already-satisfied but VACUOUS.  That question is decided by three
quantities and one currency conversion, so the library computes exactly those:

    lambda_std   via  S_P = ((T_P + T_P^T)/2),  M = I - S_P,  1 - lambda_std = lambda_2(M)
    E[inv_e]     the Kendall count against the distinguished order e = 0 < 1 < ... < n-1
    delta(P)     max over incomparable pairs of min(p, 1-p)          (the frozen test)
    the two forms of row 8 at a given eps, evaluated SEPARATELY and never welded

WRITTEN FROM THE CONVENTIONS AS DOCUMENTED, NOT COPIED.  The source conventions are recorded
in code/c3_audit_a94c3/libA94.py's docstring, which quotes the tex line numbers:

  :130-146   R(sigma) e_a = e_{sigma(a)};  T_P = E_{sigma in L(P)} R(sigma)
  :160-163   S_P = ((T_P + T_P^T)/2)|_H,  H = 1-perp

and sigma is POSITION -> ELEMENT (one-line notation).  This file shares no code with libA94.py;
a1_selftest.py cross-checks the two implementations against each other on every poset it can,
because two implementations agreeing is the only evidence available that the convention was read
the same way twice.

THE VACUITY TEST IS EXACT AND IS NOT AN EIGENVALUE COMPUTATION -- AND THE FIRST ORACLE WRITTEN
HERE WAS THE WRONG ONE, WHICH IS RECORDED RATHER THAN QUIETLY FIXED (this instrument's whole
subject is a claim stated in the wrong currency; filing one would have been the same defect).

  THE DEFECT.  The first draft tested `1 - lambda_std <= 1` as `S_P is POSITIVE SEMIDEFINITE`,
  on the reasoning that S_P * 1 = 1 puts the +1 eigenvector outside H.  That reasoning is
  BACKWARDS.  `lambda_std = max spec(S_P|_H)` -- the LARGEST eigenvalue on H -- so
  `lambda_std >= 0` says ONE eigenvalue is non-negative, while `S_P PSD` says ALL of them are.
  PSD is strictly stronger and it is FALSE almost everywhere: 4759 of the 4824 posets at n = 6
  have a non-PSD S_P, while `1 - lambda_std <= 1` holds at every one of them.  A test that is
  wrong in the SAFE direction (it would have reported a vacuity failure that is not there) is
  still a test of a different statement.

  THE CORRECT EXACT ORACLE, used below.  `lambda_std >= 0` iff S_P|_H is NOT negative definite.
  Take B = [b_0 ... b_{n-2}] with b_k = e_k - e_{k+1}, a rational (non-orthogonal) basis of
  H = 1-perp; then v^T (B^T S B) v = (Bv)^T S (Bv) with Bv ranging over all of H, so

        lambda_std >= 0    <=>    B^T S_P B  is NOT positive definite when negated
                           <=>    NOT is_pd_exact(-B^T S_P B)

  Positive-definiteness of a rational symmetric matrix is decided exactly by symmetric Gaussian
  elimination with a strict pivot test, so the verdict carries NO floating point.  This matters:
  a vacuity claim decided at 1e-9 tolerance is a claim about a tolerance.  Floating point appears
  only where a NUMBER is wanted for reporting, never where a VERDICT is.

  is_psd_exact is KEPT, because a2 reports the PSD census as the evidence that the wrong oracle
  was wrong -- deleting it would leave the correction unsupported.
"""

from fractions import Fraction
from itertools import combinations, permutations

# ---------------------------------------------------------------------- posets ---


def all_posets(n):
    """Every strict partial order on {0..n-1} admitting e = 0 < 1 < ... < n-1 as a linear
    extension, as a frozenset of pairs (i, j) with i < j meaning i <_P j.

    Enumerating only these is not a restriction: `e` is a FRAME, not a choice (STATE.md
    glossary), so every poset-with-distinguished-linear-extension is isomorphic to exactly one
    labelling in this family.  Built by transitive closure of upward-closed subsets rather than
    by filtering all 2^C(n,2) masks for n >= 6, where the mask loop is 2^15 = 32768 and fine.
    """
    pairs = list(combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        rel = frozenset(p for b, p in enumerate(pairs) if mask >> b & 1)
        if _transitive(rel):
            yield rel


def _transitive(rel):
    for (i, j) in rel:
        for (a, b) in rel:
            if a == j and (i, b) not in rel:
                return False
    return True


def linear_extensions(n, rel):
    """Every sigma in S_n written POSITION -> ELEMENT that extends rel."""
    out = []
    for perm in permutations(range(n)):
        pos = [0] * n
        for a, x in enumerate(perm):
            pos[x] = a
        if all(pos[i] < pos[j] for (i, j) in rel):
            out.append(perm)
    return out


def incomparable_pairs(n, rel):
    return [(i, j) for (i, j) in combinations(range(n), 2)
            if (i, j) not in rel and (j, i) not in rel]


def is_primitive(n, rel):
    """Not an ordinal sum: no k with every element of {0..k-1} below every element of {k..n-1}."""
    for k in range(1, n):
        if all((i, j) in rel for i in range(k) for j in range(k, n)):
            return False
    return True


def is_chain(n, rel):
    return len(incomparable_pairs(n, rel)) == 0


# ------------------------------------------------------- transport and spectrum ---


def T_matrix(n, exts):
    """T[x][a] = Pr[element x occupies position a].  Exact rationals."""
    L = len(exts)
    C = [[0] * n for _ in range(n)]
    for perm in exts:
        for a, x in enumerate(perm):
            C[x][a] += 1
    return [[Fraction(v, L) for v in row] for row in C]


def S_matrix(n, T):
    """S_P = (T + T^T)/2.  Symmetric, doubly stochastic, non-negative.  Exact."""
    return [[(T[i][j] + T[j][i]) / 2 for j in range(n)] for i in range(n)]


def is_psd_exact(A):
    """EXACT positive-semidefiniteness of a symmetric rational matrix.

    Symmetric Gaussian elimination.  At each step the pivot is the leading diagonal entry:
      * pivot < 0            -> NOT PSD (a negative diagonal in the reduced form is a negative
                                direction, so it is a verdict, not a heuristic)
      * pivot == 0           -> PSD requires the whole remaining row/column to vanish; if any
                                off-diagonal in it is non-zero the 2x2 minor
                                [[0, b], [b, d]] has determinant -b^2 < 0 -> NOT PSD
      * pivot > 0            -> eliminate and recurse on the Schur complement
    Returns True/False.  No tolerance appears anywhere: Fractions are exact.
    """
    n = len(A)
    M = [[Fraction(A[i][j]) for j in range(n)] for i in range(n)]
    for k in range(n):
        p = M[k][k]
        if p < 0:
            return False
        if p == 0:
            for j in range(k + 1, n):
                if M[k][j] != 0:
                    return False
            continue
        for i in range(k + 1, n):
            f = M[i][k] / p
            if f == 0:
                continue
            for j in range(k, n):
                M[i][j] -= f * M[k][j]
    return True


def is_pd_exact(A):
    """EXACT positive-DEFINITENESS (strict) of a symmetric rational matrix.

    Same elimination as is_psd_exact but the pivot test is strict: a zero pivot is a null
    direction, which is PSD-but-not-PD, so it returns False.  Returns True/False, no tolerance.
    The empty matrix (n = 0) is positive definite vacuously -- it has no non-zero vectors -- and
    that case is reachable at n = 1, where H is trivial."""
    n = len(A)
    M = [[Fraction(A[i][j]) for j in range(n)] for i in range(n)]
    for k in range(n):
        p = M[k][k]
        if p <= 0:
            return False
        for i in range(k + 1, n):
            f = M[i][k] / p
            if f == 0:
                continue
            for j in range(k, n):
                M[i][j] -= f * M[k][j]
    return True


def _H_basis(n):
    """B = [b_0 ... b_{n-2}], b_k = e_k - e_{k+1}: a rational basis of H = 1-perp.
    Full column rank and its image is exactly H, which is all the argument needs -- it is NOT
    orthonormal, and it does not need to be, because the test below is a test of a SIGN of a
    quadratic form and a change of basis preserves that."""
    return [[(Fraction(1) if i == k else (Fraction(-1) if i == k + 1 else Fraction(0)))
             for k in range(n - 1)] for i in range(n)]


def _congruent_to_H(n, S):
    """B^T S B, exact.  Its quadratic form is S's restricted to H."""
    B = _H_basis(n)
    m = n - 1
    SB = [[sum(S[i][t] * B[t][k] for t in range(n)) for k in range(m)] for i in range(n)]
    return [[sum(B[i][r] * SB[i][k] for i in range(n)) for k in range(m)] for r in range(m)]


def lambda_std_nonneg_exact(n, S):
    """EXACT verdict: is `lambda_std >= 0`, equivalently `1 - lambda_std <= 1`?

    lambda_std = max spec(S|_H).  It is >= 0 iff S|_H is not negative definite, i.e. iff
    -(B^T S B) is not positive definite.  Exact rationals throughout; no tolerance."""
    if n < 2:
        return True                      # H is trivial; lambda_std is a max over nothing
    A = _congruent_to_H(n, S)
    negA = [[-x for x in row] for row in A]
    return not is_pd_exact(negA)


def trace_T(n, T):
    """trace T_P = E_sigma[#{x : pos_sigma(x) = rank_e(x)}], exact.  The premise of the
    general-n reduction `1 - lambda_std <= (n - trace T_P)/(n-1)`."""
    return sum(T[i][i] for i in range(n))


def _jacobi(Ain, sweeps=200, tol=1e-15):
    """Cyclic Jacobi for a real symmetric matrix; eigenvalues ascending.  FLOAT -- for
    REPORTING a number only.  Every verdict in this instrument is taken from exact arithmetic."""
    import math
    n = len(Ain)
    A = [[float(x) for x in row] for row in Ain]
    for _ in range(sweeps):
        off = math.sqrt(sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-18:
                    continue
                theta = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
    return sorted(A[i][i] for i in range(n))


def one_minus_lambda_std(n, S):
    """1 - lambda_std = lambda_2(M), M = I - S.  FLOAT, for reporting.

    M is PSD with M1 = 0 (it is the Laplacian of the weighted graph whose edge weights are S's
    off-diagonal entries), so 0 is always an eigenvalue and the second-smallest of M is the one
    wanted.  The VERDICT `1 - lambda_std <= 1` is never taken from here -- it is taken from
    is_psd_exact(S), which is the same statement in exact arithmetic."""
    M = [[(Fraction(1) if i == j else Fraction(0)) - S[i][j] for j in range(n)] for i in range(n)]
    vals = _jacobi(M)
    return vals[1]


def lambda_max_of_M(n, S):
    """Largest eigenvalue of M = I - S.  FLOAT, for reporting only."""
    M = [[(Fraction(1) if i == j else Fraction(0)) - S[i][j] for j in range(n)] for i in range(n)]
    return _jacobi(M)[-1]


# ------------------------------------------------------- the two axes' quantities ---


def E_inv_e(n, exts, rel):
    """E[inv_e(sigma)] -- expected number of INCOMPARABLE pairs sigma places against e.

    Comparable pairs cannot be inverted by a linear extension, so restricting the count to
    incomparable pairs is not a choice; it is what inv_e is (STATE.md glossary).  Exact."""
    inc = incomparable_pairs(n, rel)
    tot = 0
    for perm in exts:
        pos = [0] * n
        for a, x in enumerate(perm):
            pos[x] = a
        for (i, j) in inc:
            if pos[j] < pos[i]:
                tot += 1
    return Fraction(tot, len(exts))


def pair_flip_probs(n, exts, rel):
    """For each incomparable pair (i, j), i < j: Pr[j precedes i], i.e. Pr[flipped against e]."""
    inc = incomparable_pairs(n, rel)
    L = len(exts)
    out = {}
    for (i, j) in inc:
        c = 0
        for perm in exts:
            pos = [0] * n
            for a, x in enumerate(perm):
                pos[x] = a
            if pos[j] < pos[i]:
                c += 1
        out[(i, j)] = Fraction(c, L)
    return out


def delta_P(n, exts, rel):
    """delta(P) = max over incomparable pairs of min(p, 1-p).  Returns (delta, n_incomparable).

    A poset with NO incomparable pair -- a chain -- has an empty max.  Reported as delta = 0 with
    the count 0 beside it, and NEVER without the count: 'frozen' for a chain is vacuously true and
    is a different fact from a genuinely frozen poset with incomparable pairs."""
    probs = pair_flip_probs(n, exts, rel)
    if not probs:
        return Fraction(0), 0
    return max(min(p, 1 - p) for p in probs.values()), len(probs)


def eps_spec_of(n, Einv):
    """The eps for which E[inv_e] = (eps/6)(n^2 - 1) holds with equality -- i.e. read
    E[inv_e] back into row 8's own inversion currency.  Exact."""
    return Fraction(6, 1) * Einv / (n * n - 1)


def master_bound_rhs(n, Einv):
    """mg-210d's master bound RHS: 6 E[inv_e] / (n^2 - 1).  Numerically identical to
    eps_spec_of -- which is the POINT: the master bound is what makes row 8's two forms one
    implication, and the implication runs inversions -> spectrum only."""
    return eps_spec_of(n, Einv)


def eps_sup_of(n, rel):
    """Op-Form Claim 6.1's bound in eps_spec units: eps_sup = 2m/(n^2-1) = d * n/(n+1),
    where m = #incomparable pairs and d = m / C(n,2).  Exact.

    Derivation as mg-345e §2 records it: E[inv_e] = sum over incomparable pairs of
    Pr[flipped] < m/3 under frozen, and matching m/3 against (eps/6)(n^2-1) gives
    eps = 2m/(n^2-1)."""
    m = len(incomparable_pairs(n, rel))
    return Fraction(2 * m, n * n - 1)
