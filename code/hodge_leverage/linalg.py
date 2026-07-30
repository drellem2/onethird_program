"""Small dense/sparse symmetric eigensolvers in pure Python.

No third-party packages (the repository convention: `code/face_geometry/` uses
none either).  Two routines:

  * `jacobi_eigenvalues`  -- all eigenvalues of a small dense symmetric matrix
    by the cyclic Jacobi rotation method.  Used for link 1-skeletons, which have
    at most a few hundred vertices.
  * `smallest_nonzero`    -- the smallest eigenvalue of a sparse symmetric PSD
    operator restricted to the orthogonal complement of a known kernel, by
    Lanczos with full reorthogonalisation.  Used for lambda_2(Delta_AT), where
    the matrix reaches 720 x 720 and a dense sweep would be too slow.

Both are checked against each other, and against closed forms, in `controls.py`.
"""

import math


# --------------------------------------------------------------------------
# dense symmetric: cyclic Jacobi
# --------------------------------------------------------------------------

def jacobi_eigenvalues(Ain, tol=1e-13, max_sweeps=100):
    """All eigenvalues (ascending) of a dense symmetric matrix, as floats."""
    n = len(Ain)
    if n == 0:
        return []
    if n == 1:
        return [float(Ain[0][0])]
    A = [[float(x) for x in row] for row in Ain]
    for _ in range(max_sweeps):
        off = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                off += A[i][j] * A[i][j]
        if off <= tol * tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = A[p][q]
                if abs(apq) < 1e-18:
                    continue
                app, aqq = A[p][p], A[q][q]
                theta = (aqq - app) / (2.0 * apq)
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


# --------------------------------------------------------------------------
# sparse symmetric: Lanczos with full reorthogonalisation
# --------------------------------------------------------------------------

def _dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def _axpy(a, u, v):
    return [a * x + y for x, y in zip(u, v)]


def _scale(a, u):
    return [a * x for x in u]


def smallest_nonzero(matvec, dim, kernel, m=None, seed=12345):
    """Smallest eigenvalue of a symmetric PSD operator on `kernel`-perp.

    `matvec(v)` applies the operator; `kernel` is a list of vectors spanning
    (a superset of) the eigenvalue-0 eigenspace, which is projected out at every
    step.  Returns None if the complement is 0-dimensional.

    Lanczos on the restricted operator, with full reorthogonalisation, then
    Jacobi on the (small) tridiagonal matrix.  Deterministic: the start vector
    comes from a fixed linear congruential sequence, so reruns are identical.
    """
    # orthonormalise the kernel basis
    kb = []
    for k in kernel:
        v = [float(x) for x in k]
        for b in kb:
            v = _axpy(-_dot(v, b), b, v)
        nv = math.sqrt(_dot(v, v))
        if nv > 1e-9:
            kb.append(_scale(1.0 / nv, v))
    eff = dim - len(kb)
    if eff <= 0:
        return None

    def project(v):
        for b in kb:
            v = _axpy(-_dot(v, b), b, v)
        return v

    if m is None:
        m = min(eff, 160)
    # deterministic pseudo-random start
    x, st = [], seed
    for _ in range(dim):
        st = (1103515245 * st + 12345) % (1 << 31)
        x.append(st / float(1 << 31) - 0.5)
    x = project(x)
    nx = math.sqrt(_dot(x, x))
    if nx < 1e-12:
        return None
    q = _scale(1.0 / nx, x)
    Q = [q]
    alpha, beta = [], []
    for j in range(m):
        w = project(matvec(Q[j]))
        a = _dot(w, Q[j])
        alpha.append(a)
        w = _axpy(-a, Q[j], w)
        if j > 0:
            w = _axpy(-beta[j - 1], Q[j - 1], w)
        # full reorthogonalisation
        for b in Q:
            w = _axpy(-_dot(w, b), b, w)
        nw = math.sqrt(_dot(w, w))
        if nw < 1e-10 or j == m - 1:
            break
        beta.append(nw)
        Q.append(_scale(1.0 / nw, w))
    k = len(alpha)
    T = [[0.0] * k for _ in range(k)]
    for i in range(k):
        T[i][i] = alpha[i]
        if i + 1 < k:
            T[i][i + 1] = T[i + 1][i] = beta[i]
    return jacobi_eigenvalues(T)[0]


def dense_matvec(M):
    return lambda v: [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def sparse_matvec(rows, dim):
    """rows[i] = list of (j, value)."""
    def mv(v):
        out = [0.0] * dim
        for i, row in enumerate(rows):
            s = 0.0
            for (j, a) in row:
                s += a * v[j]
            out[i] = s
        return out
    return mv


# --------------------------------------------------------------------------
# second-largest eigenvalue of a reversible chain given as a weighted graph
# --------------------------------------------------------------------------

def lambda2_weighted_graph(nvert, edges):
    """Second-largest eigenvalue of the normalised adjacency of a weighted graph.

    `edges` is a list of (u, v, w) with w > 0, u != v.  The operator is
    P = D^{-1} W, reversible w.r.t. the vertex weights d(u) = sum_v w(u,v);
    it is conjugate to the symmetric S = D^{-1/2} W D^{-1/2}, whose eigenvalues
    are computed.  Isolated vertices (d(u) = 0) are dropped: they are separate
    components, so if any exist the graph is disconnected and lambda_2 = 1.

    Returns (lambda2, connected_flag).  lambda2 = 1.0 exactly when the graph is
    disconnected (or has an isolated vertex, or fewer than 2 vertices with
    positive degree -- in which case lambda_2 is reported as None).
    """
    if nvert < 2:
        return (None, True)
    d = [0.0] * nvert
    for (u, v, w) in edges:
        d[u] += w
        d[v] += w
    live = [u for u in range(nvert) if d[u] > 0]
    if len(live) != nvert:
        # an isolated vertex is its own connected component, and there are
        # >= 2 vertices, so the graph is disconnected: lambda_2 = 1.
        return (1.0, False)
    idx = {u: i for i, u in enumerate(live)}
    S = [[0.0] * len(live) for _ in range(len(live))]
    for (u, v, w) in edges:
        i, j = idx[u], idx[v]
        val = w / math.sqrt(d[u] * d[v])
        S[i][j] += val
        S[j][i] += val
    ev = jacobi_eigenvalues(S)
    return (ev[-2], True)
