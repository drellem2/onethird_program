"""mg-e015 -- independent re-computation for docs/AUDIT-mg-c929.md.

Written without importing or copying code/ksbft_sec6_c929.  Sections:
  K  constants of Prop. B and the width bound, from KSBFT's printed formulas (p.21-25)
  P  census of every naturally-labelled poset n = 2..NMAX, built by a DIFFERENT generator
     (add element k with an order ideal of P[1..k-1] as its down-set; A006455 counts are
     the positive control), exact rational pair probabilities, then on the population
     delta(P) <= 1/3 (eps = eps0) and delta(P) < 1/e (eps = 1/e - delta):
       S1  Delta(x,y) >= eps/sqrt3 on P-hat                           (KSBFT (6.4) consequence)
       S3  P[against height] <= exp(1 - eps*sqrt(Delta/gap)) on P-hat (KSBFT (6.11))
       S5  E[inv_h] <= 2 sqrt3 e gap n / eps^3                         (Prop. B step 5)
       S6  sum_{x||y} min(p,1-p) <= E[inv_h]                           (Prop. B step 6)
       F21 E[inv_e] == sum_{x||y} min(p,1-p) exactly (delta <= 1/3 only)
     NEGATIVE CONTROL: S1 run on ALL posets (hypothesis dropped) must FIRE.
  A  the two-atom law of Prop. A, exactly, n = 5, t = 1/10
  D  d(x,y) is NOT a function of the pair marginals: two measures on S_3 with equal pair
     marginals and different Var(f(x)-f(y))
  W  two parallel chains: window sum W = 2m^2/(m+1) and I* = sum min(p,1-p) via the exact
     hypergeometric formula, cross-checked against brute force for m <= 7, extended to m = 3000
"""
import itertools, math, sys
from fractions import Fraction as Fr

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
E = math.e; S3 = math.sqrt(3); EPS0 = 1 / E - 1 / 3


def section_K():
    print("== K: constants (floats; nothing below is near a threshold)")
    for name, eps in (("eps0 = 1/e - 1/3", EPS0), ("illustrative 1/6", 1 / 6)):
        G1 = 10 * E * (1 + S3) / eps ** 3                    # (6.8)
        R = 288 / eps ** 2
        A = 64 * S3 * R / eps                                # section 6.4: gap <= A log^2 gap
        L = math.log(A)
        G2 = 73728 * S3 / eps ** 3 * math.log(18432 * S3 / eps ** 3) ** 2   # paper's display
        assert abs(A - 18432 * S3 / eps ** 3) / A < 1e-9 and abs(G2 - 4 * A * L * L) / G2 < 1e-9
        # g <= A log^2 g  =>  g <= 4A L^2 : need L > log 4 + 2 log L  (and g/log^2 g increasing past e^2)
        step = L > math.log(4) + 2 * math.log(L)
        G = max(G1, G2)
        W1 = 2 * S3 * G / eps                                 # (6.5)
        W2 = 442368 / eps ** 4 * math.log(18432 * S3 / eps ** 3) ** 2
        C = 2 * S3 * E * G / eps ** 3
        print("  %-18s G1=%.4g A=%.4g G2=%.4g step(L>log4+2logL: %.3f > %.3f)=%s" %
              (name, G1, A, G2, L, math.log(4) + 2 * math.log(L), step))
        print("  %-18s width (6.5)*G = %.4g ; paper display = %.4g ; C = 2sqrt3 e G/eps^3 = %.4g" %
              ("", W1, W2, C))
        for tgt in (1.0, 1 / 6, 0.02):
            b = 6 * C / tgt
            N = (b + math.sqrt(b * b + 4)) / 2
            print("  %-18s 6Cn/(n^2-1) <= %-8.4g  from n >= %.4g" % ("", tgt, N))
    # paper's eps = 1e-100, in log10 (eps^4 underflows a double)
    l = math.log(18432 * S3) + 300 * math.log(10)          # natural log of A
    print("  paper eps=1e-100: log10(width display) = %.3f" %
          (math.log10(442368) + 400 + math.log10(l * l)))
    # (6.12): is /eps^2 enough?  the integral step gives 5/eps^2, times (1+sqrt3 gap/eps)
    eps, gap = EPS0, 1e6
    true_pref = 2 * E * (1 + S3 * gap / eps) * 5 / eps ** 2
    print("  (6.12) prefactor at eps0, gap=1e6: 2e(1+sqrt3 gap/eps)(5/eps^2) = %.4g ;"
          " paper 10e(1+sqrt3)gap/eps^3 = %.4g ; '/eps^2' version = %.4g" %
          (true_pref, 10 * E * (1 + S3) * gap / eps ** 3, 10 * E * (1 + S3) * gap / eps ** 2))


def natural_posets(n):
    """Each naturally labelled poset on 0..n-1 exactly once: element k's strict down-set is an
    order ideal of the poset on 0..k-1.  Returns list of down-set tuples (frozensets)."""
    out = [()]
    for k in range(n):
        nxt = []
        for P in out:
            for r in range(k + 1):
                for S in itertools.combinations(range(k), r):
                    S = frozenset(S)
                    if all(P[y] <= S for y in S):      # S closed downward
                        nxt.append(P + (S,))
        out = nxt
    return out


def lin_ext(n, down):
    res = []
    for perm in itertools.permutations(range(n)):
        pos = [0] * n
        for i, x in enumerate(perm): pos[x] = i + 1
        if all(pos[y] < pos[x] for x in range(n) for y in down[x]):
            res.append(pos)
    return res


def section_P():
    print("== P: census n = 2..%d (A006455: 1,2,7,40,357,4824,63565)" % NMAX)
    A006455 = [1, 1, 2, 7, 40, 357, 4824, 63565]
    tot = 0; pop13 = 0; pope = 0
    worst = {k: math.inf for k in ("S1", "S3", "S5", "S6", "S1e", "S3e", "S5e", "S6e")}
    f21_bad = 0; nc_S1 = math.inf; ratio_max = 0.0
    for n in range(2, NMAX + 1):
        Ps = natural_posets(n)
        print("  n=%d  %d posets  (A006455 %d)  %s" % (n, len(Ps), A006455[n],
              "ok" if len(Ps) == A006455[n] else "MISMATCH"))
        tot += len(Ps)
        for down in Ps:
            ext = lin_ext(n, down); N = len(ext)
            comp = lambda x, y: x in down[y] or y in down[x]
            cnt = [[0] * n for _ in range(n)]
            for pos in ext:
                for x in range(n):
                    for y in range(n):
                        if pos[x] < pos[y]: cnt[x][y] += 1
            p = [[Fr(cnt[x][y], N) for y in range(n)] for x in range(n)]
            inc = [(x, y) for x in range(n) for y in range(x + 1, n) if not comp(x, y)]
            delta = max((min(p[x][y], p[y][x]) for x, y in inc), default=Fr(0))
            # heights on P-hat: shift by 1, plus 1 and n+2
            h = [1 + sum(p[y][x] for y in range(n) if y != x) + 1 for x in range(n)]
            hs = sorted([Fr(1)] + h + [Fr(n + 2)])
            gap = float(max(hs[i + 1] - hs[i] for i in range(len(hs) - 1)))
            # negative control: separation with hypothesis dropped
            for x in range(n):
                for y in range(x + 1, n):
                    nc_S1 = min(nc_S1, float(abs(h[x] - h[y])) - EPS0 / S3)
            for tag, cond, eps in (("", delta <= Fr(1, 3), EPS0),
                                   ("e", float(delta) < 1 / E - 1e-12, 1 / E - float(delta))):
                if not inc or not cond: continue
                if tag == "": pop13 += 1
                else: pope += 1
                invh = Fr(0)
                for x in range(n):
                    for y in range(n):
                        if x == y: continue
                        D = float(abs(h[x] - h[y]))
                        worst["S1" + tag] = min(worst["S1" + tag], D - eps / S3)
                        if h[y] > h[x]:
                            worst["S3" + tag] = min(worst["S3" + tag],
                                                    math.exp(1 - eps * math.sqrt(D / gap)) - float(p[y][x]))
                            invh += p[y][x]
                smin = sum(min(p[x][y], p[y][x]) for x, y in inc)
                worst["S5" + tag] = min(worst["S5" + tag], 2 * S3 * E * gap * n / eps ** 3 - float(invh))
                worst["S6" + tag] = min(worst["S6" + tag], float(invh - smin))
                if tag == "":
                    ratio_max = max(ratio_max, float(invh) / n)
                    # F21: weak-majority orientation, exact
                    inv_e = Fr(0)
                    for x, y in inc:
                        inv_e += min(p[x][y], p[y][x])  # orientation toward >= 2/3 side
                    # compute directly from extensions
                    direct = Fr(0)
                    for pos in ext:
                        for x, y in inc:
                            maj_xy = p[x][y] >= Fr(2, 3)       # x before y is the majority
                            if maj_xy != (pos[x] < pos[y]): direct += Fr(1, N)
                    if direct != smin: f21_bad += 1
    print("  total %d ; delta<=1/3 population %d ; delta<1/e population %d" % (tot, pop13, pope))
    for k, v in worst.items():
        print("  %-4s worst slack %+.6g %s" % (k, v, "ok" if v >= -1e-9 else "FAIL"))
    print("  F21 exact mismatches on delta<=1/3: %d" % f21_bad)
    print("  max E[inv_h]/n on delta<=1/3 population: %.6f (vs C = 2.96e17)" % ratio_max)
    print("  NEGATIVE CONTROL S1 on ALL posets (hypothesis dropped): worst %+.6g %s" %
          (nc_S1, "FIRES" if nc_S1 < -1e-9 else "SILENT -- instrument broken"))


def section_A():
    print("== A: two-atom law mu_t = (1-t) delta_id + t delta_rev, n=5, t=1/10")
    n, t = 5, Fr(1, 10)
    law = [(tuple(range(1, n + 1)), 1 - t), (tuple(range(n, 0, -1)), t)]   # pos[x] for x=0..n-1
    assert sum(w for _, w in law) == 1 and all(w > 0 for _, w in law)
    p = [[sum(w for pos, w in law if pos[x] < pos[y]) for y in range(n)] for x in range(n)]
    vals = set(p[x][y] for x in range(n) for y in range(n) if x != y)
    delta = max(min(p[x][y], p[y][x]) for x in range(n) for y in range(x + 1, n))
    h = [sum(w * pos[x] for pos, w in law) for x in range(n)]
    adj = [h[i + 1] - h[i] for i in range(n - 1)]
    invh = sum(w * sum(1 for x in range(n) for y in range(x + 1, n) if pos[y] < pos[x]) for pos, w in law)
    print("  pair marginals take values %s (all in (0,1): every pair 'incomparable', width n)" % sorted(vals))
    print("  delta = %s ; heights %s ; adjacent Delta %s (<1)" % (delta, h, sorted(set(adj))))
    print("  E[inv_h] = %s = t*C(n,2) = %s ; in M_n(eta) for eta <= 1/3 - t: %s" %
          (invh, t * n * (n - 1) // 2, max(p[y][x] for x in range(n) for y in range(x + 1, n)) <= Fr(1, 3)))


def section_D():
    print("== D: d is not a function of pair marginals (S_3)")
    perms = list(itertools.permutations(range(3)))
    pos = [[0] * 3 for _ in perms]
    for i, pm in enumerate(perms):
        for k, x in enumerate(pm): pos[i][x] = k + 1
    # kernel of the pair-marginal map: the three 'x before y' indicators and total mass
    rows = [[1] * 6] + [[1 if pos[i][x] < pos[i][y] else 0 for i in range(6)] for x, y in ((0, 1), (0, 2), (1, 2))]
    # candidate: alternating sign over the two 3-cycles vs 3 transpositions gives the kernel of mass;
    # search small integer vectors
    best = None
    for v in itertools.product(range(-1, 2), repeat=6):
        if any(v) and all(sum(r[i] * v[i] for i in range(6)) == 0 for r in rows):
            best = v; break
    u = [Fr(1, 6)] * 6
    mu2 = [u[i] + Fr(1, 12) * best[i] for i in range(6)]
    def var(mu, x, y):
        m = sum(mu[i] * (pos[i][x] - pos[i][y]) for i in range(6))
        return sum(mu[i] * (pos[i][x] - pos[i][y] - m) ** 2 for i in range(6))
    same = all(sum(r[i] * u[i] for i in range(6)) == sum(r[i] * mu2[i] for i in range(6)) for r in rows)
    print("  kernel vector %s ; mu2 = %s (nonneg %s) ; same pair marginals: %s" %
          (best, [str(w) for w in mu2], all(w >= 0 for w in mu2), same))
    for x, y in ((0, 1), (0, 2), (1, 2)):
        print("  Var(f(%d)-f(%d)): uniform %s vs mu2 %s" % (x, y, var(u, x, y), var(mu2, x, y)))


def section_W():
    print("== W: two parallel chains")
    def exact(m):
        # P[a_i before b_j] = P[#a among first i+j-1 >= i]   (1-indexed i,j)
        tot = math.comb(2 * m, m); Is = Fr(0)
        for i in range(1, m + 1):
            for j in range(1, m + 1):
                Nn = i + j - 1
                c = sum(math.comb(Nn, k) * math.comb(2 * m - Nn, m - k) for k in range(i, min(Nn, m) + 1))
                pr = Fr(c, tot); Is += min(pr, 1 - pr)
        return Is
    def brute(m):
        n = 2 * m; cnt = {}; N = 0; Wt = 0
        for Apos in itertools.combinations(range(1, n + 1), m):
            B = [q for q in range(1, n + 1) if q not in Apos]; N += 1
            for ch in (Apos, B):
                prev = 0
                for q in ch: Wt += q - prev - 1; prev = q
            for i in range(m):
                for j in range(m):
                    cnt[(i, j)] = cnt.get((i, j), 0) + (Apos[i] < B[j])
        return Fr(Wt, N), sum(min(Fr(v, N), 1 - Fr(v, N)) for v in cnt.values())
    for m in range(1, 8):
        Wb, Ib = brute(m)
        print("  m=%d brute W=%s (2m^2/(m+1)=%s) I*=%.6f exact-formula I*=%.6f %s" %
              (m, Wb, Fr(2 * m * m, m + 1), float(Ib), float(exact(m)),
               "ok" if Wb == Fr(2 * m * m, m + 1) and Ib == exact(m) else "MISMATCH"))
    def lg(a): return math.lgamma(a + 1)
    def fast(m):
        # float version via log-binomials; column sums of the hypergeometric pmf
        L = lambda a, b: lg(a) - lg(b) - lg(a - b)
        tot = L(2 * m, m); Is = 0.0
        for Nn in range(1, 2 * m):
            lo, hi = max(0, Nn - m), min(Nn, m)
            pmf = [math.exp(L(Nn, k) + L(2 * m - Nn, m - k) - tot) for k in range(lo, hi + 1)]
            tail = [0.0] * (len(pmf) + 1)
            for k in range(len(pmf) - 1, -1, -1): tail[k] = tail[k + 1] + pmf[k]
            for i in range(max(1, Nn - m + 1), min(m, Nn) + 1):   # j = Nn - i + 1 in 1..m
                pr = tail[i - lo] if i >= lo else 1.0
                Is += min(pr, 1 - pr)
        return Is
    assert abs(fast(11) - float(exact(11))) < 1e-9
    # audit's PROOF (docs/AUDIT-mg-c929.md W): I* >= sum_{N<=m} E|S_N|/2 >= sum_{m/2<=N<=m} sqrt(N)/(4 sqrt6)
    def half_EabsS(m, Nn):
        L = lambda a, b: lg(a) - lg(b) - lg(a - b)
        tot = L(2 * m, m); lo, hi = max(0, Nn - m), min(Nn, m)
        return sum(abs(2 * k - Nn) * math.exp(L(Nn, k) + L(2 * m - Nn, m - k) - tot) for k in range(lo, hi + 1)) / 2
    for m in (2, 5, 11, 50, 200):
        Is = fast(m); mid = sum(half_EabsS(m, Nn) for Nn in range(1, m + 1))
        lb = sum(math.sqrt(Nn) / (4 * math.sqrt(6)) for Nn in range(math.ceil(m / 2), m + 1))
        print("  m=%4d  I*=%.4f >= sum_{N<=m} E|S_N|/2=%.4f >= proof bound %.4f  %s ; proof bound/W = %.4f" %
              (m, Is, mid, lb, "ok" if Is >= mid - 1e-9 and mid >= lb - 1e-9 else "FAIL", lb / (2 * m * m / (m + 1))))
    for m in (11, 50, 200, 800, 3000):
        Is = fast(m); W = 2 * m * m / (m + 1)
        print("  m=%5d  I*/n^1.5 = %.5f  I*/W = %.3f  I*/(W*sqrt m) = %.5f" %
              (m, Is / (2 * m) ** 1.5, Is / W, Is / W / math.sqrt(m)))


if __name__ == "__main__":
    section_K(); section_A(); section_D(); section_W(); section_P()
