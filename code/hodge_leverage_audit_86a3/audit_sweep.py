"""Independent rebuild of §4, §5 and §6's numbers: the codimension-2 link
census (Theorem H), the gamma_i sweep, the (LG) check, and the exact constants
(2.62, 404, 2^{3-n}).

lambda_2(Delta_AT) is obtained here by Lanczos with FULL reorthogonalisation on
the shifted operator cI - Delta restricted to 1-perp, written from scratch, and
cross-checked against (a) a dense Jacobi solve wherever |L(P)| <= 130 and
(b) the closed form 2 - 2cos(pi/n) on the antichains.
"""

import math
import sys
import time
from fractions import Fraction

from audit_core import (posets_upto_iso, linexts, facet_of, all_faces, blocks,
                        induced, at_graph, canon, link_1skeleton,
                        lambda2_weighted, jacobi_eigenvalues, proper_ideals_of)


# --------------------------------------------------------------------------
# lambda_2 of the AT Laplacian
# --------------------------------------------------------------------------

def lambda2_at(P, adj=None):
    if adj is None:
        _, adj = at_graph(P)
    m = len(adj)
    if m < 2:
        return None
    c = 2.0 * (P.n - 1) + 1.0

    def matvec(v):
        # (cI - Delta) v  with Delta = D - A
        out = [0.0] * m
        for i in range(m):
            out[i] = (c - len(adj[i])) * v[i]
            s = 0.0
            for j in adj[i]:
                s += v[j]
            out[i] += s
        return out

    # deflate constants
    def project(v):
        mu = sum(v) / m
        return [x - mu for x in v]

    # Lanczos with full reorthogonalisation
    import random
    rng = random.Random(20260730)
    q = project([rng.random() - 0.5 for _ in range(m)])
    nrm = math.sqrt(sum(x * x for x in q))
    q = [x / nrm for x in q]
    Q = [q]
    alpha, beta = [], []
    kmax = min(m - 1, 300)
    for k in range(kmax):
        w = project(matvec(Q[-1]))
        a = sum(w[i] * Q[-1][i] for i in range(m))
        alpha.append(a)
        w = [w[i] - a * Q[-1][i] for i in range(m)]
        if beta:
            w = [w[i] - beta[-1] * Q[-2][i] for i in range(m)]
        for u in Q:                       # full reorthogonalisation
            d = sum(w[i] * u[i] for i in range(m))
            if d:
                w = [w[i] - d * u[i] for i in range(m)]
        b = math.sqrt(sum(x * x for x in w))
        if b < 1e-12:
            break
        beta.append(b)
        Q.append([x / b for x in w])
    k = len(alpha)
    T = [[0.0] * k for _ in range(k)]
    for i in range(k):
        T[i][i] = alpha[i]
        if i + 1 < k:
            T[i][i + 1] = T[i + 1][i] = beta[i]
    ev = jacobi_eigenvalues(T)
    return c - max(ev)


def lambda2_at_dense(P, adj=None):
    if adj is None:
        _, adj = at_graph(P)
    m = len(adj)
    if m < 2:
        return None
    A = [[0.0] * m for _ in range(m)]
    for i in range(m):
        A[i][i] = float(len(adj[i]))
        for j in adj[i]:
            A[i][j] = -1.0
    ev = sorted(jacobi_eigenvalues(A))
    return ev[1]


# --------------------------------------------------------------------------
# gamma_i
# --------------------------------------------------------------------------

_CK = {}


def block_key(P, mask):
    k = (P.n, tuple(sorted(P.lt)), mask)
    if k not in _CK:
        _CK[k] = canon(bin(mask).count("1"), induced(P, mask).lt)
    return _CK[k]


def face_key(P, sigma):
    return tuple(sorted(block_key(P, b) for b in blocks(P, sigma)))


def gammas(P, facets, memo=None, use_memo=True):
    """gamma_i for i = -1 .. n-4, each the max over faces of that dimension of
    lambda_2 of the weighted link 1-skeleton."""
    fs = all_faces(P)
    out = {}
    for i in range(-1, P.n - 3):
        best = None
        for sigma in fs.get(i, []):
            if use_memo:
                k = face_key(P, sigma)
                if memo is not None and k in memo:
                    lam = memo[k]
                else:
                    v, ew = link_1skeleton(P, sigma, facets)
                    lam = lambda2_weighted(len(v), ew)
                    if memo is not None:
                        memo[k] = lam
            else:
                v, ew = link_1skeleton(P, sigma, facets)
                lam = lambda2_weighted(len(v), ew)
            if lam is None:
                continue
            if best is None or lam > best:
                best = lam
        out[i] = best
    return out


def lg_bound(g):
    b = 2.0
    for i in sorted(g):
        if g[i] is None:
            continue
        b *= (1.0 - g[i])
    return b


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print("=" * 78)
    print("AUDIT §4/§5/§6: codim-2 census, the gamma sweep, the constants")
    print("=" * 78)

    # ---- Theorem H census -------------------------------------------------
    print("\nH. codimension-2 links, independently enumerated (4 <= n <= 6)")
    names = {}
    census = {}
    for n in range(4, min(hi, 6) + 1):
        for P in posets_upto_iso(n):
            facets = [facet_of(P, w) for w in linexts(P)]
            fs = all_faces(P)
            for sigma in fs.get(P.n - 4, []):
                v, ew = link_1skeleton(P, sigma, facets)
                nv = len(v)
                ne = len(ew)
                deg = [0] * nv
                for (a, b) in ew:
                    deg[a] += 1
                    deg[b] += 1
                shape = ("C_%d" % nv if nv == ne and nv > 0 and all(d == 2 for d in deg)
                         else "P_%d" % nv if ne == nv - 1 and nv > 0
                         and sorted(deg) == [1, 1] + [2] * (nv - 2)
                         else "other(nv=%d,ne=%d)" % (nv, ne))
                lam = lambda2_weighted(nv, ew)
                bt = tuple(sorted(block_key(P, b) for b in blocks(P, sigma)
                                  if bin(b).count("1") > 1))
                key = (shape, round(lam, 9) if lam is not None else None)
                census[key] = census.get(key, 0) + 1
                names.setdefault(shape, set()).add(bt)
    tot = 0
    for (shape, lam), cnt in sorted(census.items()):
        print("    %-8s  lambda_2=%-8s  count=%6d" % (shape, lam, cnt))
        tot += cnt
    print("    TOTAL codim-2 links: %d   distinct shapes: %d"
          % (tot, len(census)))

    # ---- Theorem L spot check (memo key soundness) ------------------------
    print("\nL/P5. same block-type multiset => same link lambda_2 (memo disabled)")
    for n in range(2, min(hi, 5) + 1):
        seen = {}
        clash = 0
        keys = 0
        for P in posets_upto_iso(n):
            facets = [facet_of(P, w) for w in linexts(P)]
            fs = all_faces(P)
            for d in fs:
                for sigma in fs[d]:
                    v, ew = link_1skeleton(P, sigma, facets)
                    lam = lambda2_weighted(len(v), ew)
                    if lam is None:
                        continue
                    k = face_key(P, sigma)
                    if k in seen:
                        if abs(seen[k] - lam) > 1e-9:
                            clash += 1
                    else:
                        seen[k] = lam
                        keys += 1
        print("    n=%d  distinct block-type keys=%3d  clashes=%d" % (n, keys, clash))

    # ---- the sweep --------------------------------------------------------
    print("\nA. full population sweep, 2 <= n <= %d" % hi)
    memo = {}
    all_ratios = []
    attained = 0
    all_below = []
    npos = 0
    maxgamma = None
    for n in range(2, hi + 1):
        t0 = time.time()
        viol = 0
        ratios = []
        cnt = 0
        mg = None
        for P in posets_upto_iso(n):
            npos += 1
            les, adj = at_graph(P)
            facets = [facet_of(P, w) for w in linexts(P)]
            g = gammas(P, facets, memo)
            b = lg_bound(g)
            tru = lambda2_at(P, adj)
            gv = [x for x in g.values() if x is not None]
            if gv:
                mm = max(gv)
                if mg is None or mm > mg:
                    mg = mm
                if maxgamma is None or mm > maxgamma:
                    maxgamma = mm
                if any(abs(x - 0.5) < 1e-9 for x in gv):
                    attained += 1
                else:
                    all_below.append(P.tag())
            if tru is None:
                continue
            cnt += 1
            if tru < b - 1e-9:
                viol += 1
                print("      (LG) VIOLATION", n, P.tag(), tru, b)
            ratios.append(tru / b)
        ratios.sort()
        med = ratios[len(ratios) // 2] if len(ratios) % 2 else \
            (ratios[len(ratios) // 2 - 1] + ratios[len(ratios) // 2]) / 2
        all_ratios += ratios
        print("    n=%d  posets=%3d  (LG) violations=%d  max gamma=%s   "
              "truth/bound: min=%.4f median=%.4f max=%.4f   [%.1fs]"
              % (n, len(posets_upto_iso(n)), viol,
                 ("%.6f" % mg) if mg is not None else "-",
                 ratios[0], med, ratios[-1], time.time() - t0))
    print("    posets swept (n >= 2): %d" % npos)
    print("    max gamma over the whole population: %.9f" % maxgamma)
    print("    posets attaining gamma_i = 1/2 at some level: %d of %d"
          % (attained, npos))
    print("    posets with every gamma_i < 1/2: %d" % len(all_below))
    print("      tags:", "; ".join(all_below))
    print("    global max truth/bound: %.4f" % max(all_ratios))

    # ---- antichain family, exact ------------------------------------------
    print("\nB. the antichain family: is 2^{3-n} exact or fitted?")
    print("    bound = 2 * prod_{i=-1}^{n-4} (1 - gamma_i);  #levels = n-2")
    for n in range(2, min(hi, 6) + 1):
        P = [Q for Q in posets_upto_iso(n) if not Q.lt][0]
        facets = [facet_of(P, w) for w in linexts(P)]
        g = gammas(P, facets, memo)
        b = lg_bound(g)
        tru = 2 - 2 * math.cos(math.pi / n)
        gv = [g[i] for i in sorted(g) if g[i] is not None]
        print("    n=%d  levels=%d  gamma=%s  bound=%.9f  2^{3-n}=%.9f  "
              "equal=%s  truth=%.6f  ratio=%.2f"
              % (n, len(gv), ",".join("%.4f" % x for x in gv), b,
                 2.0 ** (3 - n), abs(b - 2.0 ** (3 - n)) < 1e-9, tru, tru / b))

    # ---- cross-checks on the solver ---------------------------------------
    print("\nC. lambda_2 solver cross-checks (Lanczos vs dense Jacobi vs closed form)")
    worst = 0.0
    for n in range(2, min(hi, 5) + 1):
        for P in posets_upto_iso(n):
            les, adj = at_graph(P)
            if len(les) < 2 or len(les) > 130:
                continue
            a = lambda2_at(P, adj)
            b = lambda2_at_dense(P, adj)
            worst = max(worst, abs(a - b))
    print("    max |Lanczos - dense Jacobi| over all n<=5 posets: %.3e" % worst)
    for n in range(2, min(hi, 6) + 1):
        P = [Q for Q in posets_upto_iso(n) if not Q.lt][0]
        a = lambda2_at(P)
        b = 2 - 2 * math.cos(math.pi / n)
        print("    A_%d  Lanczos=%.12f  2-2cos(pi/n)=%.12f  diff=%.2e"
              % (n, a, b, abs(a - b)))


if __name__ == "__main__":
    main()
