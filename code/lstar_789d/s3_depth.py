"""s3 -- HOW MUCH OF THE MONOTONE CONE DOES (L*) ACTUALLY NEED?

mu_pref is a minimum over a cone of dimension n-1.  (L*) says mu_pref * Delta <= gamma.
A proof has to produce, at each (F)-failing poset, SOME nonincreasing f cheap enough to
witness that.  The question this script answers is how complicated that f has to be.

Let  mu_j  =  min over nonincreasing f taking at most j+1 distinct values
            =  min over faces of the monotone cone with at most j cuts,
so mu_1 <= ... are decreasing in j, mu_1 is the best single PREFIX INDICATOR, and
mu_{n-1} = mu_pref.  Write  v_j = mu_j * Delta / gamma.  Then

    v_1 >= v_2 >= ... >= v_{n-1} = v_L,

and (L*) needs only v_{n-1} <= 1, but a PROOF that uses j-cut test functions needs
v_j <= 1.  The smallest j for which v_j <= 1 across the (F)-failing set is the depth of
cone the theorem cannot avoid -- and it is a fact about the posets, not a choice.

WHY THIS IS THE RIGHT QUESTION AFTER mg-c50b.  The obstruction rules out proofs built
from the five scalars.  The next thing anyone would try is the cheapest structural
object above them: a single prefix cut, which is what routes (F) and c_true are already
phrased in.  If v_1 <= 1 on the (F)-failing set then (L*) reduces to a one-cut statement
and the corpus's existing prefix machinery applies to it directly.  This script settles
that, and settles it in the direction that costs the corpus an attempt rather than
granting it one.
"""

import sys, time
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib789d import P789, gen_posets, height, gen_eig_min, fam_bipartite_minus


def mu_depth(P, maxcuts):
    """min over nonincreasing f constant on at most `maxcuts`+1 consecutive blocks.
    EXHAUSTIVE over those faces; the minimiser is checked to lie in the cone."""
    n = P.n
    A = P.Amat()
    best = float("inf")
    from itertools import combinations
    for j in range(1, maxcuts + 1):
        for cuts in combinations(range(1, n), j):
            blocks, start = [], 0
            for c in cuts:
                blocks.append((start, c))
                start = c
            blocks.append((start, n))
            r = len(blocks)
            Lt = [[0.0] * r for _ in range(r)]
            for s in range(r):
                for t in range(r):
                    acc = 0.0
                    for i in range(blocks[s][0], blocks[s][1]):
                        for jj in range(blocks[t][0], blocks[t][1]):
                            acc -= A[i][jj]
                    Lt[s][t] = acc
                Lt[s][s] += blocks[s][1] - blocks[s][0]
            sz = [b[1] - b[0] for b in blocks]
            Nt = [[(sz[s] if s == t else 0) - sz[s] * sz[t] / n for t in range(r)]
                  for s in range(r)]
            rr = r - 1
            T = [[0.0] * rr for _ in range(r)]
            for s in range(rr):
                T[s][s] = 1.0
                T[r - 1][s] = -sz[s] / sz[r - 1]
            Lp = [[sum(T[a][i] * Lt[a][b] * T[b][jj] for a in range(r) for b in range(r))
                   for jj in range(rr)] for i in range(rr)]
            Np = [[sum(T[a][i] * Nt[a][b] * T[b][jj] for a in range(r) for b in range(r))
                   for jj in range(rr)] for i in range(rr)]
            lam, y = gen_eig_min(Lp, Np, rr)
            if lam is None:
                continue
            v = [sum(T[s][jj] * y[jj] for jj in range(rr)) for s in range(r)]
            if v[0] < v[-1]:
                v = [-x for x in v]
            if any(v[s] - v[s + 1] < -1e-11 for s in range(r - 1)):
                continue
            if lam < best:
                best = lam
    return best


print("=" * 78)
print("S3.1  THE n = 7 (F)-FAILING SET")
print("=" * 78)
t0 = time.time()
FF = []
for dn in gen_posets(7):
    P = P789(dn, 7)
    if not P.primitive():
        continue
    g = P.gamma_float()
    M = float(P.M())
    if M * M > 2 * g * (1 - 1e-7):
        Mx = P.M()
        if not P.gap_ge(Mx * Mx / 2):
            FF.append(dn)
print("  rebuilt: %d posets   (%.0fs)" % (len(FF), time.time() - t0))
sys.stdout.flush()

print()
print("=" * 78)
print("S3.2  DEPTH TABLE -- max over the 168 of  mu_j * Delta / gamma")
print("=" * 78)
print("   j (cuts allowed) |  max v_j  | v_j <= 1 at | argmax dn")
tab = {}
for j in range(1, 7):
    mx, arg = -1.0, None
    okc = 0
    for dn in FF:
        P = P789(dn, 7)
        mu = mu_depth(P, j)
        v = mu * float(P.Delta()) / P.gamma_float()
        if v <= 1.0 + 1e-12:
            okc += 1
        if v > mx:
            mx, arg = v, dn
    tab[j] = mx
    print("   %d               | %9.6f | %3d of %3d  | %s" % (j, mx, okc, len(FF), str(arg)))
    sys.stdout.flush()

print()
print("  READING.")
first_ok = min([j for j in tab if tab[j] <= 1.0], default=None)
if first_ok is None:
    print("  NO depth j <= 6 gives v_j <= 1 -- which would contradict (L*) itself.")
else:
    print("  The shallowest cone depth that carries (L*) across the whole n = 7")
    print("  (F)-failing set is j = %d.  Every j < %d is REFUTED there, by exhibited"
          % (first_ok, first_ok))
    print("  posets, so no proof of (L*) can be built from monotone test functions with")
    print("  fewer than %d cuts.  In particular:" % first_ok)
    if tab[1] > 1.0:
        print("    j = 1 (a SINGLE PREFIX INDICATOR) is refuted at max v_1 = %.6f." % tab[1])
        print("    That is the object routes (F) and c_true are phrased in, so the corpus's")
        print("    existing prefix machinery cannot reach (L*) on its own.")

print()
print("=" * 78)
print("S3.3  THE SAME TABLE ON THE FAMILIES, AT LARGER n")
print("=" * 78)
print("   family                | n  | (F) fails |   v_1    |   v_2    |   v_3    |   v_L")
cases = []
for a in range(3, 7):
    for b in range(3, 7):
        if a + b > 11:
            continue
        dn, n = fam_bipartite_minus(a, b, [(a - 1, b - 1)])
        cases.append(("K_{%d,%d} - 1" % (a, b), dn, n))
for name, dn, n in cases:
    P = P789(dn, n)
    if not P.primitive():
        continue
    g = P.gamma_float()
    D = float(P.Delta())
    M = float(P.M())
    vs = [mu_depth(P, j) * D / g for j in (1, 2, 3)]
    vL = P.mu_faces()[0] * D / g
    print("   %-21s | %2d | %9s | %8.5f | %8.5f | %8.5f | %8.5f"
          % (name, n, "YES" if M * M > 2 * g else "no", vs[0], vs[1], vs[2], vL))
    sys.stdout.flush()
