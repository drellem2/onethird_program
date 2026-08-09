"""a0 — controls.  Nothing in a1-a4 is worth reading until every line here says `ok`.

The controls that matter for an AUDIT are not the ones that show my numbers agree with
mg-81ff's — agreement is the thing under test, so an instrument that assumes it proves
nothing.  They are the ones that show MY instrument is not the one that is wrong when we
disagree.  Each has a live negative arm: a deliberately broken version that must FAIL.
"""

from fractions import Fraction as F
from itertools import permutations
import sys

import lib00b3 as L
import tridiag as TD

ok = fail = 0


def chk(cond, msg):
    global ok, fail
    if cond:
        ok += 1
        print("    ok:   " + msg)
    else:
        fail += 1
        print("    FAIL: " + msg)


print("=" * 78)
print("a0 — CONTROLS for mg-00b3's audit instrument")
print("=" * 78)

# ---------------------------------------------------------------- (A)
print("""
------------------------------------------------------------------------------
(A) THE TWO DOWN-SET ENUMERATORS AGREE — and the lattice walk is not the scan
------------------------------------------------------------------------------
  `downsets_scan` visits all 2^n subsets; `downsets_walk` never leaves the down-set
  lattice.  a3 needs the walk (2^28 is not affordable) so the walk must be right.

  >>> THIS CONTROL WAS WRONG ON ITS FIRST RUN AND THE RECORD IS KEPT.  It compared the
  two enumerators as LISTS and failed at 3280 of 5230 posets.  The sets are identical at
  every one of the 5230 (0 set-differences); what differs is the order WITHIN a popcount,
  because the scan discovers by increasing mask value and the walk by BFS.  The push DP
  needs exactly one property of the order — popcount non-decreasing — and both have it.
  So the failure was my control's, not the instrument's, and asserting list equality
  would have made a3's n = 28 rows unreachable for a reason that does not exist.  The
  control now asserts the two things that are actually load-bearing.""")
bad = badpc = 0
tot = 0
for n in range(2, 7):
    for down in L.all_posets(n):
        tot += 1
        a, b = L.downsets_scan(n, down), L.downsets_walk(n, down)
        if set(a) != set(b) or len(a) != len(b):
            bad += 1
        for lst in (a, b):
            pc = [x.bit_count() for x in lst]
            if pc != sorted(pc):
                badpc += 1
chk(bad == 0, f"scan and walk enumerate the SAME SET at all {tot} posets n <= 6 "
              f"(and the same count — neither duplicates)")
chk(badpc == 0, "both enumerators are popcount-monotone at all of them — the only "
                "ordering property the push DP consumes")
n, dn = L.S_n(16)
chk(set(L.downsets_scan(n, dn)) == set(L.downsets_walk(n, dn)),
    "scan == walk (as sets) on the staircase S_16 (the family a3 pushes to n = 28)")
# negative arm: a walk that forgets the down-closure test must OVER-count
seen = {0}
frontier = [0]
cnt = 1
while frontier:
    nxt = []
    for S in frontier:
        for i in range(16):
            if S >> i & 1:
                continue
            U = S | (1 << i)          # <-- the missing `down[i] & ~S` test
            if U not in seen:
                seen.add(U)
                nxt.append(U)
                cnt += 1
    frontier = nxt
chk(cnt > 10 * len(L.downsets_walk(16, dn)),
    f"NEGATIVE ARM: dropping the closure test walks {cnt} states, not "
    f"{len(L.downsets_walk(16, dn))} — the guard is load-bearing")

# ---------------------------------------------------------------- (B)
print("""
------------------------------------------------------------------------------
(B) THE PUSH DP AGREES WITH n! — EXHAUSTIVELY, NOT ON A SAMPLE
------------------------------------------------------------------------------
  mg-9461's s0 caught a defect in exactly this DP that no numbers-only check at small n
  could see, and mg-81ff records the same one.  So the check is against n!, on the
  WHOLE population, on the integer transport matrix and not on a derived scalar.""")
bad = 0
tot = 0
for n in range(2, 7):
    for down in L.all_posets(n):
        tot += 1
        if L.transport_int(n, down) != L.transport_factorial(n, down):
            bad += 1
chk(bad == 0, f"Tint and e(P) agree with the n! path at all {tot} posets n <= 6, "
              f"entry by entry")

# ---------------------------------------------------------------- (C)
print("""
------------------------------------------------------------------------------
(C) THE CUT FORM OF Q_k AGREES WITH THE EDGE SUM
------------------------------------------------------------------------------
  This file evaluates Q_k as an INTEGER CUT COUNT, having observed that the centred
  prefix indicator jumps by exactly n across the cut and by 0 elsewhere.  mg-81ff sums
  over weighted edges.  If my observation is wrong every number in a1-a3 is wrong.""")
bad = 0
tot = 0
for n in range(2, 7):
    for down in L.all_posets(n):
        T, N = L.transport_int(n, down)
        Q = L.prefix_Q_all(n, T, N)
        for k in range(1, n):
            tot += 1
            f = [F(n - k, n) if i < k else F(-k, n) for i in range(n)]
            if Q[k - 1] != L.energy_edgesum(n, T, N, f) / F(k * (n - k), n):
                bad += 1
chk(bad == 0, f"cut form == edge sum at all {tot} (poset, k) pairs n <= 6")
# negative arm: the UNCENTRED indicator must disagree
diff = 0
tot2 = 0
for n in range(4, 6):
    for down in L.all_posets(n):
        T, N = L.transport_int(n, down)
        Q = L.prefix_Q_all(n, T, N)
        for k in range(1, n):
            tot2 += 1
            g = [F(1) if i < k else F(0) for i in range(n)]
            if L.energy_edgesum(n, T, N, g) / F(k) != Q[k - 1]:
                diff += 1
chk(diff > 0.5 * tot2,
    f"NEGATIVE ARM: the UNCENTRED reading of f_A disagrees at {diff} of {tot2} "
    f"(poset, k) pairs n = 4,5 — so the centring is a real choice, not a no-op")

# ---------------------------------------------------------------- (D)
print("""
------------------------------------------------------------------------------
(D) THE EIGENROUTINE — exact PD test vs float Sturm, both arms
------------------------------------------------------------------------------
  The exact route is `lambda_2 > q  <=>  L - q(I - J/n) + J/n positive definite`; the
  float route is Householder + Sturm bisection.  They share no line.  a2's 86 277-row
  sweep uses the FLOAT one, so it has to be inside the exact bracket everywhere.""")
bad = 0
tot = 0
worst = 0.0
for n in range(2, 7):
    for down in L.all_posets(n):
        T, N = L.transport_int(n, down)
        g = TD.lambda2(n, L.L_floats(n, T, N))
        lo, hi = L.lambda2_bracket(n, L.L_fractions(n, T, N), F(1, 10 ** 9))
        tot += 1
        if not (float(lo) - 1e-7 <= g <= float(hi) + 1e-7):
            bad += 1
        worst = max(worst, abs(g - float(lo)))
chk(bad == 0, f"float lambda_2 lies in the exact bracket at all {tot} posets n <= 6 "
              f"(worst deviation {worst:.2e})")
# negative arm: a wrong q must be rejected
n, dn = L.D_k(3)
T, N = L.transport_int(n, dn)
Lx = L.L_fractions(n, T, N)
chk(L.lambda2_gt_exact(n, Lx, F(1, 2)) and not L.lambda2_gt_exact(n, Lx, F(3, 5)),
    "NEGATIVE ARM: on D_3 (gap 0.5584) the PD test accepts q = 1/2 and REJECTS q = 3/5")

# ---------------------------------------------------------------- (E)
print("""
------------------------------------------------------------------------------
(E) min_k Q_k >= gap, AND c <= 1, AT EVERY POSET — asserted, not assumed
------------------------------------------------------------------------------
  Q_k is a Rayleigh quotient of a vector in H, so it cannot be below lambda_2.  Every
  reading in a2/a3 rests on it (it is why C3gap >= 1 and c <= 1), and it is exactly the
  kind of fact an instrument inherits from prose without checking.""")
bad1 = bad2 = 0
tot = 0
for n in range(3, 7):
    for down in L.all_posets(n):
        if not L.is_primitive(n, down):
            continue
        T, N = L.transport_int(n, down)
        mq = min(L.prefix_Q_all(n, T, N))
        Lx = L.L_fractions(n, T, N)
        tot += 1
        if L.lambda2_gt_exact(n, Lx, mq):        # lambda_2 > minQ would break it
            bad1 += 1
        g = TD.lambda2(n, L.L_floats(n, T, N))
        if g < 1.0 - 1e-12 and (1.0 - float(mq)) / (1.0 - g) > 1.0 + 1e-9:
            bad2 += 1
chk(bad1 == 0, f"min_k Q_k >= lambda_2 at all {tot} primitive posets n <= 6 (exact)")
chk(bad2 == 0, f"c <= 1 at all informative posets n <= 6")

# ---------------------------------------------------------------- (F)
print("""
------------------------------------------------------------------------------
(F) `informative` IS EXACTLY `not an antichain` — the exclusion is named, not tuned
------------------------------------------------------------------------------
  `c` is undefined at lambda_std = 0, i.e. gap = 1.  a1 reports `informative` counts one
  below `primitive` at every n and it should be obvious WHICH poset is dropped.""")
for n in range(3, 8):
    drop = []
    if n <= 6:
        for down in L.all_posets(n):
            if not L.is_primitive(n, down):
                continue
            T, N = L.transport_int(n, down)
            if TD.lambda2(n, L.L_floats(n, T, N)) > 1.0 - 1e-12:
                drop.append(down)
        chk(len(drop) == 1 and all(d == 0 for d in drop[0]),
            f"n = {n}: exactly one poset has gap = 1 and it is the ANTICHAIN")

# ---------------------------------------------------------------- (G)
print("""
------------------------------------------------------------------------------
(G) primitive <=> connected, at n <= 6 — mg-81ff's `DISC <=> CUT`, re-derived
------------------------------------------------------------------------------
  mg-81ff uses this to collapse two loop filters into one and reports it at n = 7 over
  96 428 posets.  It is cheap to check at n <= 6 and it is NOT assumed anywhere here —
  a1/a2/a3 filter on `is_primitive` alone, so if it were false the populations would
  differ from mg-81ff's and a1 (P1) would say so.""")
for n in range(2, 7):
    bad = 0
    for down in L.all_posets(n):
        T, N = L.transport_int(n, down)
        w = {(i, j) for i in range(n) for j in range(i + 1, n) if T[i][j] + T[j][i]}
        adj = {i: set() for i in range(n)}
        for (i, j) in w:
            adj[i].add(j)
            adj[j].add(i)
        seen2, st = {0}, [0]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen2:
                    seen2.add(y)
                    st.append(y)
        conn = len(seen2) == n
        if conn != L.is_primitive(n, down):
            bad += 1
    chk(bad == 0, f"n = {n}: connected(a_ij) <=> primitive, 0 exceptions")

print()
print("=" * 78)
print(f"a0: {ok} controls pass, {fail} fail")
print("=" * 78)
sys.exit(1 if fail else 0)
