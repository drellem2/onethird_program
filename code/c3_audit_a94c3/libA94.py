"""libA94 -- mg-94c3's independent audit library for mg-76b2.

Shares no code with `lib76b2.py`.  Written from the SOURCE
(`spectral_near_ordinal_sum_program.tex`) rather than from mg-76b2's
deliverable, so that a shared implementation defect is impossible:

  :130-146   R(sigma) e_a = e_{sigma(a)};  T_P = E_{sigma in L(P)} R(sigma)
  :160-163   S_P = ((T_P + T_P^T)/2)|_H,  H = 1-perp
  :220-227   <1_A, (I - S_P) 1_A> = E_sigma |A \\ sigma(A)|
  :229-237   Phi_P(A) = E|A \\ sigma(A)| / |A|,  0 < |A| <= n/2
  :270-278   Delta_1(A,B) = E|A \\ sigma(A)| / min(|A|,|B|)

CONVENTION, stated because mg-76b2 sec.8 reports a live bug in a sibling
instrument at exactly this point: sigma is a map POSITION -> ELEMENT (one-line
notation, tex:56), so sigma(A) is the set of elements occupying the positions
in A.  It is NOT `set(perm[:len(A)])`.

Exact `Fraction` arithmetic for every conductance, Rayleigh quotient and
ratio built from them.  Floating point ONLY for eigenvalues (a hand-written
Jacobi rotation solver -- there is no numpy on this machine, which is why the
eigen path had to be written rather than imported).
"""

from fractions import Fraction
from itertools import permutations, combinations
import math

# ---------------------------------------------------------------- posets ---


def all_posets(n):
    """Every strict partial order on {0..n-1} for which the identity 0<1<...<n-1
    is a linear extension.  Yielded as a frozenset of covered-or-not pairs (i,j),
    i<j, meaning i <_P j.  Transitively closed, checked."""
    pairs = list(combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        rel = set(p for b, p in enumerate(pairs) if mask >> b & 1)
        ok = True
        for (i, j) in rel:
            for (j2, k) in rel:
                if j2 == j and (i, k) not in rel:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            yield frozenset(rel)


def linear_extensions(n, rel):
    """All sigma in S_n (position -> element) that are linear extensions of rel."""
    out = []
    for perm in permutations(range(n)):
        pos = [0] * n
        for a, x in enumerate(perm):
            pos[x] = a
        if all(pos[i] < pos[j] for (i, j) in rel):
            out.append(perm)
    return out


def is_primitive(n, rel):
    """P is ordinal-sum decomposable iff some 0<k<n has every element of
    {0..k-1} below every element of {k..n-1}.  Primitive = not decomposable."""
    for k in range(1, n):
        if all((i, j) in rel for i in range(k) for j in range(k, n)):
            return False
    return True


# ------------------------------------------------------- transport / cuts ---


def T_matrix(n, exts):
    """T_P[x][a] = Pr[element x occupies position a], exact."""
    L = len(exts)
    T = [[0] * n for _ in range(n)]
    for perm in exts:
        for a, x in enumerate(perm):
            T[x][a] += 1
    return [[Fraction(v, L) for v in row] for row in T]


def leak(n, exts, A):
    """E_sigma |A \\ sigma(A)|, exact.  A is a frozenset/set of labels in [n];
    sigma(A) = {sigma[a] : a in A}, the elements at the positions in A."""
    tot = 0
    for perm in exts:
        img = set(perm[a] for a in A)
        tot += len(A - img) if isinstance(A, (set, frozenset)) else len(set(A) - img)
    return Fraction(tot, len(exts))


def delta1(n, exts, A):
    """Delta_1(A, A^c) = E|A \\ sigma(A)| / min(|A|, n-|A|), exact."""
    k = len(A)
    return leak(n, exts, A) / min(k, n - k)


def one_minus_rho(n, exts, k):
    """1 - rho(A_k) for the CENTRED prefix indicator f = 1_{A_k} - (k/n) 1.

    Derived here, not copied:  (I - S_P)1 = 0 so <f,(I-S_P)f> = <1_A,(I-S_P)1_A>
    = E|A \\ sigma(A)|; and ||f||^2 = k(1-k/n)^2 + (n-k)(k/n)^2 = k(n-k)/n.
    Hence 1 - rho = n * E|A_k \\ sigma(A_k)| / (k(n-k)).  Exact."""
    A = frozenset(range(k))
    return Fraction(n, 1) * leak(n, exts, A) / (k * (n - k))


def prefix_cuts(n):
    return [frozenset(range(k)) for k in range(1, n)]


def all_cuts(n):
    """Every A with 0 < |A| <= n/2 -- one representative per cut, since
    Delta_1 is symmetric under complementation (checked in a2)."""
    out = []
    for k in range(1, n // 2 + 1):
        for A in combinations(range(n), k):
            out.append(frozenset(A))
    return out


# --------------------------------------------------------------- spectrum ---


def laplacian(n, T):
    """M = I - (T + T^T)/2, as floats.  M is the Laplacian of the weighted
    graph a_ij (tex:207); it annihilates the all-ones vector."""
    return [[(1.0 if i == j else 0.0) - (float(T[i][j]) + float(T[j][i])) / 2.0
             for j in range(n)] for i in range(n)]


def jacobi_eig(Ain, sweeps=100, tol=1e-14):
    """Classical cyclic Jacobi eigensolver for a real symmetric matrix.
    Returns (eigenvalues ascending, eigenvectors as columns of V, reordered)."""
    n = len(Ain)
    A = [row[:] for row in Ain]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
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
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p] = c * vkp - s * vkq
                    V[k][q] = s * vkp + c * vkq
    vals = [A[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: vals[i])
    return [vals[i] for i in order], [[V[r][i] for i in order] for r in range(n)]


def spectral_gap(n, T):
    """1 - lambda_std = the SECOND-smallest eigenvalue of M = I - S_P.

    Justification, so this is not a magic index: M is PSD with M1 = 0, so 0 is
    always an eigenvalue with eigenvector 1; lambda_std = max spec(S_P|_H) means
    1 - lambda_std = min spec(M|_H) = the second-smallest eigenvalue of M
    overall.  (If the weighted graph is disconnected this is 0, correctly.)"""
    vals, vecs = jacobi_eig(laplacian(n, T))
    gap = vals[1]
    v = [vecs[r][1] for r in range(n)]
    return gap, v, vals, vecs


EIG_TOL = 1e-9


def monotone_dominant(n, T):
    """Existential test for L2's first disjunct: does the TOP eigenspace of
    S_P|_H (= the bottom non-trivial eigenspace of M) contain a vector monotone
    along the distinguished order e = 0 < 1 < ... < n-1?

    Returns 'YES', 'NO', or 'UNDECIDED'.  UNDECIDED is returned whenever that
    eigenspace has dimension > 1, where 'THE dominant eigenvector' is not well
    defined and a 1-dimensional check would be answering a different question.
    Declared as B3 in PREDICTIONS.md; reported, never silently folded in."""
    vals, vecs = jacobi_eig(laplacian(n, T))
    gap = vals[1]
    mult = sum(1 for i in range(1, n) if abs(vals[i] - gap) < EIG_TOL)
    if mult != 1:
        return "UNDECIDED"
    v = [vecs[r][1] for r in range(n)]
    up = all(v[i] <= v[i + 1] + EIG_TOL for i in range(n - 1))
    dn = all(v[i] >= v[i + 1] - EIG_TOL for i in range(n - 1))
    return "YES" if (up or dn) else "NO"


def threshold_sets(v, n):
    """Every LEVEL set of v -- {i : v_i > t} and {i : v_i < t} over all t --
    with 0 < |S| <= n/2.

    mg-76b2 records a real defect at exactly this point: an ORDER-SLICE of the
    sorted labels is not a level set, and where v ties (the antichain ties
    everywhere) a slice splits the tie and returns sets no threshold produces.
    This routine groups by VALUE, so a tie is never split."""
    out = set()
    levels = sorted(set(round(x, 12) for x in v))
    for t in levels:
        for S in (frozenset(i for i in range(n) if round(v[i], 12) > t),
                  frozenset(i for i in range(n) if round(v[i], 12) < t)):
            if 0 < len(S) <= n // 2:
                out.add(S)
    return out


def is_prefix_or_suffix(n, S):
    xs = sorted(S)
    return xs == list(range(len(S))) or xs == list(range(n - len(S), n))


# ----------------------------------------------------------------- report ---


def banner(title):
    print("=" * 78)
    print(title)
    print("=" * 78)


def fmt(fr):
    return str(fr) if fr.denominator != 1 else str(fr.numerator)
