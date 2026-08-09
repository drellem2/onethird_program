"""tridiag — Householder tridiagonalisation + Sturm bisection for lambda_2(L).

WHY THIS EXISTS AND NOT A BISECTION ON THE PD TEST.  `lib00b3.lambda2_gt_exact` is the
verdict-bearing route and it is exact, but each call is an O(n^3) elimination, so a
40-step bisection over 86 277 posets is ~600M inner operations in pure Python.  Reducing
`L` to tridiagonal form ONCE per poset (O(n^3), done once) makes each subsequent inertia
count O(n), so the same 40-step bisection costs ~40n instead of ~40n^3/3.

The Sturm count and the LDL pivot count are the SAME inertia; that they agree is not
assumed — a0 (E) asserts the float lambda_2 produced here against the exact rational
bracket produced by `lambda2_bracket`, at every poset of n <= 5 and a sample beyond.
"""

from math import sqrt


def tridiagonalise(n, A):
    """Symmetric A (list of lists, floats) -> (d, e) with e[0] unused.

    Householder, no eigenvectors.  Follows the standard reduction; `a` is destroyed.
    """
    a = [row[:] for row in A]
    d = [0.0] * n
    e = [0.0] * n
    for i in range(n - 1, 0, -1):
        l = i - 1
        h = 0.0
        scale = 0.0
        if l > 0:
            for k in range(l + 1):
                scale += abs(a[i][k])
            if scale == 0.0:
                e[i] = a[i][l]
            else:
                for k in range(l + 1):
                    a[i][k] /= scale
                    h += a[i][k] * a[i][k]
                f = a[i][l]
                g = -sqrt(h) if f >= 0.0 else sqrt(h)
                e[i] = scale * g
                h -= f * g
                a[i][l] = f - g
                f = 0.0
                for j in range(l + 1):
                    g = 0.0
                    for k in range(j + 1):
                        g += a[j][k] * a[i][k]
                    for k in range(j + 1, l + 1):
                        g += a[k][j] * a[i][k]
                    e[j] = g / h
                    f += e[j] * a[i][j]
                hh = f / (h + h)
                for j in range(l + 1):
                    f = a[i][j]
                    e[j] = g = e[j] - hh * f
                    for k in range(j + 1):
                        a[j][k] -= (f * e[k] + g * a[i][k])
        else:
            e[i] = a[i][l]
    for i in range(n):
        d[i] = a[i][i]
    return d, e


def sturm_count(n, d, e, q):
    """# eigenvalues of the tridiagonal (d, e) strictly less than q."""
    cnt = 0
    p = d[0] - q
    if p < 0.0:
        cnt += 1
    for i in range(1, n):
        if p == 0.0:
            p = 1e-300
        p = (d[i] - q) - e[i] * e[i] / p
        if p < 0.0:
            cnt += 1
    return cnt


def eig_k(n, d, e, k, lo=-1.0, hi=5.0, iters=60):
    """The k-th smallest eigenvalue (k = 0 based), by bisection on the Sturm count."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            break
        if sturm_count(n, d, e, mid) > k:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def lambda2(n, Lf):
    """lambda_2(L): the second-smallest eigenvalue of the Laplacian (lambda_1 = 0)."""
    d, e = tridiagonalise(n, Lf)
    return eig_k(n, d, e, 1)
