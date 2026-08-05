"""mg-fcb2 -- this audit's OWN instruments.  Nothing here is imported from the
tree under audit except the objects being measured.

WHY THE INSTRUMENTS ARE REWRITTEN RATHER THAN IMPORTED.  The standing order for
this arc says *replication is not corroboration when the copies share a source*.
`verify_e35b.py` already re-derives the mg-e35b dichotomy -- but it re-derives it
by calling `controls.not_isospectral` and `controls.signed_permutation_witness`,
the same two functions the section under audit calls, over the same candidate
list.  A bug in either is invisible to that check by construction.  So:

  * the spectral half is done with EXACT INTEGER CHARACTERISTIC POLYNOMIALS
    (`charpoly_exact`) -- the whole polynomial, recovered over Z by CRT under a
    Hadamard coefficient bound -- and not with `det(A - kI) mod (2^31-1)` at five
    fixed shifts.  Sampling a polynomial at five points can miss; comparing every
    coefficient cannot.
  * the witness half is a BACKTRACKING SEARCH over permutations written from the
    definition (`signed_perm_witness`), refined by a Weisfeiler-Leman colouring of
    the absolute-value graph and closed by a parity union-find over the signs.  It
    takes NO candidate list from anybody: it searches all of S_m, pruned, so a
    NOT-GAUGE answer from it is not bounded by a candidate list the way the
    shipped detector's is.

Both are checked against exhaustive brute force in `selftest_fcb2.py` before
either is used on anything.
"""

import os
import subprocess
import sys
from fractions import Fraction   # noqa: F401  (kept out of the hot paths on purpose)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FACE_GEOMETRY = os.path.join(REPO_ROOT, "code", "face_geometry")


def import_face_geometry():
    """Put the tree under audit on sys.path and hand back its two modules.

    The objects measured come from there -- that is the point of an audit.  The
    JUDGEMENTS do not: see the module docstring.
    """
    if FACE_GEOMETRY not in sys.path:
        sys.path.insert(0, FACE_GEOMETRY)
    import face_complex
    import posets
    return face_complex, posets


# --------------------------------------------------------------------------
# scoring -- deliberately the smallest thing that can carry a verdict
# --------------------------------------------------------------------------

FAILED = []
CHECKS = [0]
PREDICTED = {"hit": 0, "miss": []}


def check(name, ok):
    CHECKS[0] += 1
    print("  [%s] %s" % ("PASS" if ok else "REFUTED", name))
    if not ok:
        FAILED.append(name)
    return ok


def predicted(tag, holds, text):
    """Score an observation against what PREDICTIONS.md said BEFORE any of this
    existed.  A miss is printed as a miss and is never edited into a hit."""
    if holds:
        PREDICTED["hit"] += 1
    else:
        PREDICTED["miss"].append("%s: %s" % (tag, text))
    print("    prediction %-5s %s -- %s" % (tag, "AS PREDICTED" if holds
                                            else "*** OFF PREDICTION ***", text))
    return holds


def finish(title):
    print()
    print("%s: %d checks, %d refuted; %d predictions scored, %d off prediction."
          % (title, CHECKS[0], len(FAILED), PREDICTED["hit"] + len(PREDICTED["miss"]),
             len(PREDICTED["miss"])))
    for f in FAILED:
        print("  REFUTED: %s" % f)
    for m in PREDICTED["miss"]:
        print("  OFF PREDICTION: %s" % m)
    return 1 if FAILED else 0


# --------------------------------------------------------------------------
# exact integer characteristic polynomials
# --------------------------------------------------------------------------

def _hessenberg_charpoly_mod(A, p):
    """Characteristic polynomial of A mod p, by reduction to upper Hessenberg
    form followed by the standard leading-principal-minor recurrence.

    Returns the coefficients of det(x.I - A) as a list, LOWEST degree first,
    length m+1, monic.  O(m^3) in F_p.
    """
    m = len(A)
    H = [[A[i][j] % p for j in range(m)] for i in range(m)]
    for k in range(1, m - 1):
        piv = -1
        for i in range(k, m):
            if H[i][k - 1] % p:
                piv = i
                break
        if piv < 0:
            continue
        if piv != k:
            H[piv], H[k] = H[k], H[piv]
            for r in range(m):
                H[r][piv], H[r][k] = H[r][k], H[r][piv]
        inv = pow(H[k][k - 1], p - 2, p)
        for i in range(k + 1, m):
            u = (H[i][k - 1] * inv) % p
            if not u:
                continue
            for j in range(k - 1, m):
                H[i][j] = (H[i][j] - u * H[k][j]) % p
            for r in range(m):
                H[r][k] = (H[r][k] + u * H[r][i]) % p
    # det(x.I - H) for upper Hessenberg H, by the classical recurrence on the
    # leading principal minors.
    polys = [[1]]
    for i in range(1, m + 1):
        # q(x) = (x - H[i-1][i-1]) * polys[i-1] - sum_{j<i-1} beta * polys[j]
        prev = polys[i - 1]
        q = [0] * (len(prev) + 1)
        for d, c in enumerate(prev):
            q[d + 1] = (q[d + 1] + c) % p
            q[d] = (q[d] - c * H[i - 1][i - 1]) % p
        beta = 1
        for j in range(i - 2, -1, -1):
            beta = (beta * H[j + 1][j]) % p
            if not beta:
                break
            c = (beta * H[j][i - 1]) % p
            if c:
                for d, cc in enumerate(polys[j]):
                    q[d] = (q[d] - c * cc) % p
        polys.append(q)
    return polys[m]


_PRIMES = None


def _primes_above(lo, count):
    out = []
    n = lo | 1
    while len(out) < count:
        if _is_prime(n):
            out.append(n)
        n += 2
    return out


def _is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _isqrt_ceil(n):
    r = int(n ** 0.5)
    while r * r < n:
        r += 1
    while r > 0 and (r - 1) * (r - 1) >= n:
        r -= 1
    return r


def charpoly_bound(A):
    """A rigorous bound on the absolute value of any coefficient of det(x.I - A).

    c_k is (up to sign) the sum of the k-by-k principal minors, of which there are
    C(m, k), and Hadamard bounds each by the product of the Euclidean norms of its
    rows, hence by B^k with B = max_i ||row_i||.  Integer arithmetic throughout, so
    the bound is a bound and not a float.
    """
    m = len(A)
    if m == 0:
        return 1
    B = max(_isqrt_ceil(sum(x * x for x in row)) for row in A)
    B = max(B, 1)
    best, binom = 1, 1
    for k in range(m + 1):
        if k:
            binom = binom * (m - k + 1) // k
        best = max(best, binom * B ** k)
    return best


def charpoly_exact(A):
    """The EXACT integer characteristic polynomial det(x.I - A), lowest degree
    first.  Computed mod a run of primes and lifted by CRT once the modulus
    exceeds twice the Hadamard bound, so the lift is proved and not assumed.

    This is the instrument P3e names.  It shares no line with
    `face_complex.not_isospectral`, which evaluates det(A - k.I) mod 2^31-1 at
    k in {3,5,7,11,13}: five samples of the polynomial rather than the polynomial.
    """
    global _PRIMES
    m = len(A)
    if m == 0:
        return [1]
    need = 2 * charpoly_bound(A) + 1
    if _PRIMES is None:
        _PRIMES = _primes_above(1 << 30, 200)
    mod, res = 1, None
    for idx, p in enumerate(_PRIMES):
        cp = _hessenberg_charpoly_mod(A, p)
        if res is None:
            res, mod = cp, p
        else:
            # incremental CRT, coefficient by coefficient
            inv = pow(mod % p, p - 2, p)
            new = []
            for a, b in zip(res, cp):
                t = ((b - a) % p) * inv % p
                new.append(a + mod * t)
            res, mod = new, mod * p
        if mod > need:
            break
    else:                                            # pragma: no cover - safety net
        raise RuntimeError("ran out of primes lifting a characteristic polynomial")
    half = mod // 2
    return [c - mod if c > half else c for c in res]


# --------------------------------------------------------------------------
# signed-permutation conjugation, searched from the definition
# --------------------------------------------------------------------------

def _wl_colours(A):
    """Weisfeiler-Leman refinement of the vertex colouring of the |A|-weighted
    graph.  Only used to PRUNE the search below; correctness never rests on it,
    because every witness the search returns is reconstructed and compared."""
    m = len(A)
    col = [(A[i][i],) for i in range(m)]
    for _ in range(m):
        sig = [(col[i], tuple(sorted((abs(A[i][j]), col[j]) for j in range(m) if j != i)))
               for i in range(m)]
        order = {s: k for k, s in enumerate(sorted(set(sig)))}
        new = [(order[sig[i]],) for i in range(m)]
        if new == col:
            break
        col = new
    return col


def _solve_signs(A, B, sigma):
    """Given sigma, is there a sign vector s with s_i * A[sigma(i)][sigma(j)] * s_j
    == B[i][j] for every i, j?  A parity union-find: each nonzero entry forces
    s_i * s_j, each zero entry has to already agree, and s_i^2 = 1 pins the
    diagonal.  Returns the sign vector or None."""
    m = len(A)
    parent = list(range(m))
    rel = [0] * m                       # parity of i relative to its root

    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        r = i
        for j in reversed(path):
            rel[j] ^= rel[parent[j]]
            parent[j] = r
        return r

    def union(i, j, par):
        ri, rj = find(i), find(j)
        if ri == rj:
            return (rel[i] ^ rel[j]) == par
        parent[ri] = rj
        rel[ri] = rel[i] ^ rel[j] ^ par
        return True

    for i in range(m):
        for j in range(m):
            a, b = A[sigma[i]][sigma[j]], B[i][j]
            if a == b == 0:
                continue
            if a == 0 or b == 0 or abs(a) != abs(b):
                return None
            if i == j:
                if a != b:              # s_i^2 = 1 pins every diagonal entry
                    return None
                continue
            par = 0 if a == b else 1
            if not union(i, j, par):
                return None
    for i in range(m):
        find(i)                          # compress, so rel[i] is parity vs its root
    # every root is free; setting each to +1 gives one solution of a consistent
    # system, and the caller reconstructs and compares it anyway.
    return [1 - 2 * rel[i] for i in range(m)]


def reconstruct(A, sigma, s):
    """s_i . A[sigma(i)][sigma(j)] . s_j, built in full so that a witness can be
    compared to the target ENTRY BY ENTRY rather than trusted."""
    m = len(A)
    return [[s[i] * A[sigma[i]][sigma[j]] * s[j] for j in range(m)] for i in range(m)]


def signed_perm_witness(A, B, node_budget=400000):
    """Search ALL of S_m for a signed permutation conjugating A to B, pruned by
    the WL colouring and by partial-consistency.  Returns (sigma, s) with the
    reconstruction VERIFIED entry by entry, or None.

    `node_budget` bounds the search.  When it is exhausted the function returns
    the string "BUDGET" rather than None, so that "searched and found nothing" is
    never silently reported as "no witness exists" -- which is the shape of defect
    this audit is looking for elsewhere.
    """
    m = len(A)
    if m != len(B):
        return None
    ca, cb = _wl_colours(A), _wl_colours(B)
    if sorted(ca) != sorted(cb):
        return None
    cands = [[a for a in range(m) if ca[a] == cb[i]] for i in range(m)]
    order = sorted(range(m), key=lambda i: len(cands[i]))
    sigma = [None] * m
    used = [False] * m
    nodes = [0]

    def consistent(i, a):
        for k in order:
            if k == i or sigma[k] is None:
                continue
            x, y = A[a][sigma[k]], B[i][k]
            if abs(x) != abs(y):
                return False
            if (x == 0) != (y == 0):
                return False
        return A[a][a] == B[i][i]

    def rec(d):
        if nodes[0] > node_budget:
            return "BUDGET"
        if d == m:
            s = _solve_signs(A, B, sigma)
            if s is not None and reconstruct(A, sigma, s) == B:
                return (list(sigma), s)
            return None
        i = order[d]
        hit_budget = False
        for a in cands[i]:
            if used[a] or not consistent(i, a):
                continue
            nodes[0] += 1
            sigma[i], used[a] = a, True
            r = rec(d + 1)
            sigma[i], used[a] = None, False
            if r == "BUDGET":
                hit_budget = True
                break
            if r is not None:
                return r
        return "BUDGET" if hit_budget else None

    return rec(0)


def brute_signed_perm(A, B):
    """The definition, enumerated: every permutation and every sign vector.
    Exponential, so only ever called on tiny matrices -- it exists to check
    `signed_perm_witness`, not to be used on the population."""
    import itertools
    m = len(A)
    for sigma in itertools.permutations(range(m)):
        for bits in range(1 << m):
            s = [-1 if bits >> i & 1 else 1 for i in range(m)]
            if reconstruct(A, list(sigma), s) == B:
                return (list(sigma), s)
    return None


# --------------------------------------------------------------------------
# small conveniences
# --------------------------------------------------------------------------

def mat_eq(A, B):
    return len(A) == len(B) and all(ra == rb for ra, rb in zip(A, B))


def git(*argv):
    return subprocess.run(("git",) + argv, cwd=REPO_ROOT, capture_output=True,
                          text=True, check=True).stdout
