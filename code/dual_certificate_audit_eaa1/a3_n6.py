"""mg-eaa1 A3 -- AUDIT CHECK 3: EXTRAPOLATE THE CLAIMED PATTERN TO n = 6 AND TRY TO BREAK IT.

My brief says an "n-indexed" verdict reads as a route to the wall, so three points is very
little evidence and the pattern must be pushed out of sample.  mg-131e's claimed n-indexed
object is precise enough to extrapolate without interpretation:

    lam = 0,  t = 1 on every cap row,  s = 0        -- feasible in EVERY branch at EVERY n,
    with bound |I_active| / 3, and on the CONSECUTIVE-PAIRS branch |I_active| = n-1.

So the prediction at n = 6 is: that vector is dual-feasible on the consecutive branch, its
bound is exactly 5/3, and mg-200d's fence attains it.  A3.1 tests that -- and it is the one
place in this audit where a pattern could have failed its first out-of-sample prediction.

IT DOES NOT FAIL.  Which is why A3.2 exists.  The `<=` direction is not a statement about ONE
branch; it is a statement about the MAXIMUM over all 2^C(n,2) of them.  So the way to break the
route is not to break the dual, it is to find a branch the dual does not cover -- and A3.2
searches for one WITHOUT using mg-131e's witness, over a declared, restricted family.

A3.3 then verifies mg-131e's own n = 6..10 witnesses by substitution in MY arithmetic; A3.4
re-derives the (5n-8)/12 sub-family claim as a branch OPTIMUM rather than a lower bound; and
A3.5 checks the realisability/tightness question the whole arc must not quietly answer.
"""

import sys
import time
from fractions import Fraction as F
from itertools import combinations

import lib_eaa1 as L

DEPTH = int(sys.argv[1]) if len(sys.argv) > 1 else 2

fails = []


def ok(cond, msg):
    print(f"  [{'OK ' if cond else 'FAIL'}] {msg}")
    if not cond:
        fails.append(msg)
    return cond


def branch_of(n, I):
    return frozenset(pr for pr in L.all_pairs(n) if pr not in set(I))


print("=" * 92)
print("A3.1  THE CLAIMED n-INDEXED PATTERN, EXTRAPOLATED OUT OF SAMPLE TO n = 6..12.")
print("      Predicted dual: lam = 0, t = 1 on every cap row, s = 0, on the consecutive-pairs")
print("      branch.  Predicted bound: (n-1)/3.  Verified by SUBSTITUTION, no solver.")
print("=" * 92)
for n in range(3, 13):
    I = L.consecutive(n)
    C = branch_of(n, I)
    fast = L.columns_consecutive_branch(n)
    if n <= 8:   # cross-check the direct generator against brute force while n! is affordable
        ok(fast == sorted(L.columns(n, C)),
           f"n={n:2d}: the direct column generator agrees with brute-force filtering of n! "
           f"({len(fast)} columns)")
    perms, rows, c, labels = L.program(n, C, perms=fast)
    y = L.trivial_dual(rows, labels)
    cert = L.verify_dual(rows, c, y)
    act = L.active_pairs(n, C, perms=fast)
    fence = L.fence(n)
    rep = L.check_measure(n, fence, C)
    target = F(n - 1, 3)
    ok(cert.ok and cert.bound == target and len(act) == n - 1 and rep["ok"]
       and rep["E_inv"] == target,
       f"n={n:2d}: cols={len(perms):3d} caps={len(act)}(=n-1) | dual feasible={cert.ok} "
       f"bound={cert.bound} | fence feasible={rep['ok']} E[inv]={rep['E_inv']} "
       f"| upper==lower={cert.bound == rep['E_inv']} = (n-1)/3 = {target}")
print("  ==> THE PATTERN SURVIVES ITS FIRST OUT-OF-SAMPLE PREDICTION AT n = 6, and at 7..12.")
print("      It is a THEOREM about the consecutive-pairs branch, and it is not the `<=`")
print("      direction, which is a maximum over 2^C(n,2) branches.")

print()
print("=" * 92)
print(f"A3.2  SO BREAK IT WHERE IT LIVES.  Independent, DECLARED, NON-exhaustive probe at")
print(f"      n = 6: every branch whose incomparable set is `consecutive U S` with")
print(f"      |S| <= {DEPTH} over the 10 non-consecutive pairs.  mg-131e's witness is NOT used.")
print("=" * 92)
n = 6
target = F(5, 3)
nonconsec = [pr for pr in L.all_pairs(n) if pr[1] != pr[0] + 1]
best, results, nfeas, nsolved = None, [], 0, 0
t0 = time.time()
for r in range(DEPTH + 1):
    for S in combinations(nonconsec, r):
        I = list(L.consecutive(n)) + list(S)
        C = branch_of(n, I)
        if not L.columns(n, C):
            continue
        nsolved += 1
        try:
            val, mu = L.branch_value(n, C)
        except L.NoSolution:
            continue
        nfeas += 1
        results.append((val, S, mu, C))
        if best is None or val > best[0]:
            best = (val, S, mu, C)
print(f"  branches probed = {nsolved}   primal-feasible = {nfeas}   [{time.time() - t0:.1f}s]")
beating = sorted({(v, S) for v, S, _, _ in results if v > target}, key=lambda t: (-t[0], t[1]))
print(f"  branches with value > (n-1)/3 = {target}: {len(beating)}")
for v, S in beating[:12]:
    print(f"      S = {list(S)}   value = {v} = {float(v):.4f}   excess = {v - target}")
if len(beating) > 12:
    print(f"      ... and {len(beating) - 12} more")
ok(bool(beating), f"n=6: an INDEPENDENTLY found branch beats (n-1)/3 = {target}")
if best:
    val, S, mu, C = best
    print(f"  BEST FOUND: S = {list(S)}  value = {val} = {float(val):.4f}"
          f"  eps_spec = {L.eps_spec(n, val)}  (conjectured 2/(n+1) = {F(2, n + 1)})")
    rep = L.check_measure(n, mu, C)
    for k, v in rep["checks"].items():
        ok(v, f"  best witness: {k}")
    ok(rep["E_inv"] == val, f"  best witness: E[inv] recomputed by substitution = "
                            f"{rep['E_inv']} (matches the solver's {val})")
    ok(L.is_transitive(C), f"  best witness: its comparable set IS transitive -- a genuine "
                           f"comparability pattern, not an artefact of the non-transitive "
                           f"superset")
    print(f"  the witness ({len(mu)} atoms):")
    for p, w in sorted(mu.items(), key=lambda t: (-t[1], t[0])):
        print(f"      mass {str(w):>6}  perm {p}  inv={L.inv(p)}")
    print(f"  flip probabilities: "
          + ", ".join(f"{pr}={rep['q'][pr]}" for pr in sorted(rep['q']) if rep['q'][pr]))
    ok(val >= F(11, 6),
       f"  my independent best {val} is >= mg-131e's published 11/6 "
       f"(a smaller value would mean I failed to find their branch, not that they are wrong)")

print()
print("=" * 92)
print("A3.3  mg-131e's OWN WITNESSES AT n = 6..10, BY SUBSTITUTION IN MY ARITHMETIC.")
print("      Transcribed by hand from d3_refutation.py; every primitive below is mine.")
print("=" * 92)
THEIRS = {
    6: ([(1, 4)], {(0, 1, 2, 3, 5, 4): F(1, 6), (0, 1, 3, 2, 5, 4): F(1, 6),
                   (0, 2, 1, 4, 3, 5): F(1, 6), (0, 2, 4, 1, 3, 5): F(1, 6),
                   (1, 0, 2, 3, 4, 5): F(1, 6), (1, 0, 3, 2, 4, 5): F(1, 6)}, F(11, 6)),
    7: ([(1, 4), (2, 5)], {(0, 1, 2, 3, 4, 5, 6): F(1, 9), (0, 1, 2, 4, 3, 5, 6): F(1, 9),
                           (0, 1, 3, 5, 2, 4, 6): F(1, 9), (0, 2, 1, 3, 5, 4, 6): F(1, 9),
                           (0, 2, 1, 4, 3, 6, 5): F(1, 9), (0, 2, 4, 1, 3, 6, 5): F(1, 9),
                           (1, 0, 2, 3, 4, 6, 5): F(1, 9), (1, 0, 3, 2, 4, 5, 6): F(1, 9),
                           (1, 0, 3, 2, 5, 4, 6): F(1, 9)}, F(20, 9)),
    8: ([(1, 4), (3, 6)], {(0, 1, 2, 3, 5, 4, 7, 6): F(1, 6), (0, 1, 3, 2, 5, 4, 6, 7): F(1, 6),
                           (0, 2, 1, 4, 3, 6, 5, 7): F(1, 6), (0, 2, 4, 1, 6, 3, 5, 7): F(1, 6),
                           (1, 0, 2, 3, 4, 5, 7, 6): F(1, 6), (1, 0, 3, 2, 4, 5, 6, 7): F(1, 6)},
        F(8, 3)),
    9: ([(1, 4), (2, 5), (3, 6), (4, 7)],
        {(0, 1, 2, 3, 4, 5, 6, 8, 7): F(1, 9), (0, 1, 2, 4, 3, 5, 7, 6, 8): F(1, 9),
         (0, 1, 3, 5, 2, 7, 4, 6, 8): F(1, 9), (0, 2, 1, 3, 5, 4, 7, 6, 8): F(1, 9),
         (0, 2, 1, 4, 3, 6, 5, 8, 7): F(1, 9), (0, 2, 4, 1, 6, 3, 5, 8, 7): F(1, 9),
         (1, 0, 2, 3, 4, 6, 5, 7, 8): F(1, 9), (1, 0, 3, 2, 4, 5, 6, 7, 8): F(1, 9),
         (1, 0, 3, 2, 5, 4, 6, 7, 8): F(1, 9)}, F(28, 9)),
    10: ([(1, 4), (3, 6), (5, 8)],
         {(0, 1, 2, 3, 5, 4, 7, 6, 9, 8): F(1, 6), (0, 1, 3, 2, 5, 4, 6, 7, 9, 8): F(1, 6),
          (0, 2, 1, 4, 3, 6, 5, 8, 7, 9): F(1, 6), (0, 2, 4, 1, 6, 3, 8, 5, 7, 9): F(1, 6),
          (1, 0, 2, 3, 4, 5, 7, 6, 8, 9): F(1, 6), (1, 0, 3, 2, 4, 5, 6, 7, 8, 9): F(1, 6)},
         F(7, 2)),
}
for m in sorted(THEIRS):
    chords, mu, claimed = THEIRS[m]
    I = list(L.consecutive(m)) + list(chords)
    C = branch_of(m, I)
    rep = L.check_measure(m, mu, C)
    tgt = F(m - 1, 3)
    allok = rep["ok"] and rep["E_inv"] == claimed and rep["E_inv"] > tgt
    ok(allok,
       f"n={m:2d}: chords={chords} | feasible={rep['ok']} | E[inv]={rep['E_inv']} "
       f"(claimed {claimed}) > (n-1)/3 = {tgt} | eps_spec={L.eps_spec(m, rep['E_inv'])} "
       f"> 2/(n+1) = {F(2, m + 1)}")
    if not rep["ok"]:
        print(f"        violations: comp_flipped={rep['comparable_flipped']} "
              f"over_cap={rep['over_cap']} sym={rep['sym_violations'][:4]}")
    ok(L.is_transitive(C), f"n={m:2d}: its comparable set is TRANSITIVE")

print()
print("=" * 92)
print("A3.4  THE (5n-8)/12 SUB-FAMILY.  d3 says `the value IS (5n-8)/12 at n = 6,8,10`.")
print("      A witness only ever gives `>=`.  Re-solved here as a branch OPTIMUM.")
print("=" * 92)
for m in (6, 8):
    chords = [(2 * j + 1, 2 * j + 4) for j in range((m - 4) // 2 + 1)
              if 2 * j + 4 <= m - 1]
    I = list(L.consecutive(m)) + chords
    C = branch_of(m, I)
    t0 = time.time()
    try:
        val, mu = L.branch_value(m, C)
    except L.NoSolution:
        val, mu = None, None
    pred = F(5 * m - 8, 12)
    ok(val == pred,
       f"n={m}: chords={chords}  branch OPTIMUM = {val}   (5n-8)/12 = {pred}"
       f"   (n-1)/3 = {F(m - 1, 3)}   [{time.time() - t0:.1f}s]")
print("  n=10 not re-solved as an optimum here -- declared, see NOT DONE.")

print()
print("=" * 92)
print("A3.5  TIGHTNESS / REALISABILITY -- the thing a dual certificate says NOTHING about.")
print("      One NAMED relation per line.  No poset is enumerated anywhere in this audit.")
print("=" * 92)
for m, Cname in ((3, frozenset({(0, 2)})),):
    mu = L.uniform_linear_extensions(m, Cname)
    rep = L.check_measure(m, mu, Cname)
    ok(rep["max_flip"] <= F(1, 3) and rep["E_inv"] == F(m - 1, 3),
       f"n={m}: uniform L(0<2) has |L|={len(mu)} E[inv]={rep['E_inv']} "
       f"max flip={rep['max_flip']} -- IN M_n and ATTAINS.  Tightness holds AT n = 3.")
C6 = branch_of(6, list(L.consecutive(6)) + [(1, 4)])
mu6 = L.uniform_linear_extensions(6, C6)
rep6 = L.check_measure(6, mu6, C6)
ok(rep6["max_flip"] > F(1, 3),
   f"n=6: uniform L(P) of the REFUTING branch's own poset has |L|={len(mu6)} "
   f"E[inv]={rep6['E_inv']} max flip={rep6['max_flip']} > 1/3 -- NOT in M_6, so the "
   f"n=6 witness is NOT a realisability claim")
for m in (4, 5):
    Cm = {4: frozenset({(0, 2), (0, 3), (1, 3)}),
          5: frozenset({(0, 2), (0, 3), (1, 4), (2, 4)})}[m]
    mu_m = L.uniform_linear_extensions(m, Cm)
    rep_m = L.check_measure(m, mu_m, Cm)
    ok(rep_m["max_flip"] > F(1, 3),
       f"n={m}: uniform L(P) of the ATTAINING branch has max flip={rep_m['max_flip']} > 1/3 "
       f"-- NOT in M_n, so tightness is NOT established at n={m} and must not be claimed")

print()
print("=" * 92)
print(f"A3 RESULT: {'ALL CHECKS PASS' if not fails else str(len(fails)) + ' FAILURES'}")
for f in fails:
    print("   FAILED:", f)
print("=" * 92)
sys.exit(1 if fails else 0)
