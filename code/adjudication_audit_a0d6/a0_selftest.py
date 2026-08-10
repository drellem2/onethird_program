"""a0 — FORCED ARMS AND PLANTED WORLDS.

Every arm here can fail. Three of them exist only to make an agreement elsewhere mean
something: A2 checks the down-set DP against `n!` permutation filtering (E1/E5), A3 checks
`leak` computed from the transport against `leak` computed from the DEFINITION over linear
extensions, and A7/A8 plant worlds in which the exact certifiers MUST refuse.
"""

from fractions import Fraction as F
from itertools import permutations
import sys

from liba0d6 import (naturally_labelled, is_primitive, transport_counts,
                     transport_counts_bruteforce, leak_prefix_numerators,
                     leak_prefix_from_extensions, M_exact, laplacian_exact,
                     gamma_float, certify_fail, certify_hold, is_psd_exact,
                     energy_exact, rel_pairs)

FAILS = []


def arm(name, ok, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("   " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


print("=" * 78)
print("a0 — FORCED ARMS")
print("=" * 78)
print()

# --------------------------------------------------------------------- A1
print("A1  THE POPULATION IS THE NATURALLY LABELLED POSETS — counted two ways")
counts = {}
for n in range(1, 8):
    ps = naturally_labelled(n)
    counts[n] = len(ps)
print("      naturally labelled posets, n = 1..7 :", [counts[n] for n in range(1, 8)])
# the same count by BRUTE FORCE at n <= 5: every transitively closed subset of {(i,j): i<j}
def brute_count(n):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    tot = 0
    for m in range(1 << len(pairs)):
        rel = {pairs[b] for b in range(len(pairs)) if m >> b & 1}
        if all((a, d) in rel for (a, b) in rel for (c, d) in rel if b == c):
            tot += 1
    return tot
bc = [brute_count(n) for n in range(1, 6)]
print("      the same by transitive-closure brute force, n = 1..5 :", bc)
arm("A1 the two enumerations agree at n <= 5",
    bc == [counts[n] for n in range(1, 6)])
arm("A1b n = 2..7 totals are 2/7/40/357/4824/96428",
    [counts[n] for n in range(2, 8)] == [2, 7, 40, 357, 4824, 96428],
    str([counts[n] for n in range(2, 8)]))
prim = {}
for n in range(2, 8):
    prim[n] = sum(1 for d in naturally_labelled(n) if is_primitive(n, d))
print("      primitive, n = 2..7 :", [prim[n] for n in range(2, 8)])
arm("A1c primitive counts are 1/4/27/275/4070/86278",
    [prim[n] for n in range(2, 8)] == [1, 4, 27, 275, 4070, 86278],
    str([prim[n] for n in range(2, 8)]))
print()

# --------------------------------------------------------------------- A2
print("A2  THE DOWN-SET DP versus FILTERING n! PERMUTATIONS  (PREDICTIONS E1/E5)")
bad = 0
tested = 0
for n in range(1, 7):
    for d in naturally_labelled(n):
        c1, n1 = transport_counts(n, d)
        c2, n2 = transport_counts_bruteforce(n, d)
        tested += 1
        if c1 != c2 or n1 != n2:
            bad += 1
arm("A2 transport agrees at every poset n <= 6", bad == 0,
    "%d posets, %d disagreements" % (tested, bad))
print()

# --------------------------------------------------------------------- A3
print("A3  leak FROM THE TRANSPORT versus leak FROM THE DEFINITION over linear extensions")
bad = 0
tested = 0
for n in range(2, 6):
    for d in naturally_labelled(n):
        cnt, N = transport_counts(n, d)
        nums = leak_prefix_numerators(n, cnt)
        for k in range(1, n):
            tested += 1
            if F(nums[k - 1], N) != leak_prefix_from_extensions(n, d, k):
                bad += 1
arm("A3 leak agrees on every prefix cut, n <= 5", bad == 0,
    "%d cuts, %d disagreements" % (tested, bad))
print()

# --------------------------------------------------------------------- A4
print("A4  leak(A) == <1_A, L 1_A>  — the definition against the matrix")
bad = 0
tested = 0
for n in range(2, 6):
    for d in naturally_labelled(n):
        cnt, N = transport_counts(n, d)
        L = laplacian_exact(n, cnt, N)
        nums = leak_prefix_numerators(n, cnt)
        for k in range(1, n):
            ind = [F(1) if i < k else F(0) for i in range(n)]
            tested += 1
            if energy_exact(L, ind) != F(nums[k - 1], N):
                bad += 1
arm("A4 the two routes to leak agree", bad == 0,
    "%d cuts, %d disagreements" % (tested, bad))
print()

# --------------------------------------------------------------------- A5
print("A5  T IS DOUBLY STOCHASTIC and L annihilates the constant vector")
bad = 0
for n in range(2, 7):
    for d in naturally_labelled(n):
        cnt, N = transport_counts(n, d)
        if any(sum(cnt[x]) != N for x in range(n)):
            bad += 1
        if any(sum(cnt[x][a] for x in range(n)) != N for a in range(n)):
            bad += 1
        L = laplacian_exact(n, cnt, N)
        if any(sum(L[i]) != 0 for i in range(n)):
            bad += 1
arm("A5 rows, columns and the kernel all check", bad == 0, "%d violations" % bad)
print()

# --------------------------------------------------------------------- A6
print("A6  is_psd_exact IS NON-VACUOUS — it must accept AND refuse")
I3 = [[F(1) if i == j else F(0) for j in range(3)] for i in range(3)]
NEG = [[F(-1) if i == j else F(0) for j in range(3)] for i in range(3)]
SING = [[F(1), F(1), F(0)], [F(1), F(1), F(0)], [F(0), F(0), F(0)]]
INDEF = [[F(1), F(2), F(0)], [F(2), F(1), F(0)], [F(0), F(0), F(1)]]
arm("A6a accepts the identity", is_psd_exact(I3))
arm("A6b refuses -I", not is_psd_exact(NEG))
arm("A6c accepts a SINGULAR psd matrix (the boundary case every verdict here sits on)",
    is_psd_exact(SING))
arm("A6d refuses an indefinite matrix whose diagonal is positive", not is_psd_exact(INDEF))
print()

# --------------------------------------------------------------------- A7
print("A7  PLANTED WORLD — the failure certifier must REFUSE a poset where (F) holds")
d = None
for cand in naturally_labelled(4):
    if is_primitive(4, cand) and len(rel_pairs(4, cand)) == 0:
        d = cand
arm("A7a the n = 4 antichain is in the population", d is not None)
cnt, N = transport_counts(4, d)
L = laplacian_exact(4, cnt, N)
M = M_exact(4, cnt, N)
t = M * M / 2
lam, vec = gamma_float(4, cnt, N)
w = certify_fail(L, t, vec)
arm("A7b certify_fail REFUSES it (it cannot manufacture a failure)", w is None,
    "M=%s gamma~%.6f f*~%.6f" % (M, lam, float(M * M) / (2 * lam)))
arm("A7c certify_hold CONFIRMS it", certify_hold(L, t))
print()

# --------------------------------------------------------------------- A8
print("A8  PLANTED WORLD — the two certifiers must never BOTH answer yes")
both = 0
checked = 0
for n in range(3, 7):
    for dd in naturally_labelled(n):
        if not is_primitive(n, dd):
            continue
        cnt, N = transport_counts(n, dd)
        L = laplacian_exact(n, cnt, N)
        M = M_exact(n, cnt, N)
        t = M * M / 2
        lam, vec = gamma_float(n, cnt, N)
        checked += 1
        if certify_fail(L, t, vec) is not None and certify_hold(L, t):
            both += 1
arm("A8 no poset is certified BOTH failing and holding", both == 0,
    "%d primitive posets n <= 6, %d contradictions" % (checked, both))
print()

# --------------------------------------------------------------------- A9
print("A9  A MUTATION CONTROL — perturb M upward and the certifier MUST flip")
dd = [d for d in naturally_labelled(5) if is_primitive(5, d)][0]
cnt, N = transport_counts(5, dd)
L = laplacian_exact(5, cnt, N)
lam, vec = gamma_float(5, cnt, N)
M = M_exact(5, cnt, N)
base = certify_fail(L, M * M / 2, vec) is not None
huge = certify_fail(L, F(10), vec) is not None          # t = 10 >> gamma: MUST certify
arm("A9a the unmutated poset does not certify as failing", not base)
arm("A9b the same poset with t = 10 DOES certify — the arm can fire", huge)
print()

# --------------------------------------------------------------------- A10
print("A10  M BY A SECOND, UNSHARED ROUTE — E[D_F] / (2 floor(n^2/4))")
print("     This arm exists because of a4's C2: the ONE line liba0d6 shares verbatim with")
print("     lib51f4 is `den = sum(min(k, n - k) for k in range(1, n))`, M's denominator.")
print("     A shared line is a shared mistake waiting to happen, so M is recomputed here")
print("     from the FOOTRULE — a different formula, over linear extensions, touching")
print("     neither leak nor that denominator.")
bad = 0
tested = 0
for n in range(3, 7):
    for d in naturally_labelled(n):
        cnt, N = transport_counts(n, d)
        M = M_exact(n, cnt, N)
        tot, cN = 0, 0
        for p in permutations(range(n)):
            pos = [0] * n
            for a, x in enumerate(p):
                pos[x] = a
            if all(pos[x] < pos[y] for y in range(n) for x in range(n) if d[y] >> x & 1):
                cN += 1
                tot += sum(abs(i - pos[i]) for i in range(n))
        tested += 1
        if M != F(tot, cN) / (2 * (n * n // 4)):
            bad += 1
arm("A10 M agrees with E[D_F]/(2 floor(n^2/4)) at every poset n <= 6", bad == 0,
    "%d posets, %d disagreements — so the shared denominator line is CONFIRMED by a\n"
    "     route that does not contain it" % (tested, bad))
print()

print("=" * 78)
if FAILS:
    print("SELFTEST FAILED: " + ", ".join(FAILS))
    sys.exit(1)
print("a0 — ALL FORCED ARMS PASS")
print("=" * 78)
