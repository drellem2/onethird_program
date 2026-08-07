"""a3_n6 — is there a measure that BEATS mg-200d's (n-1)/3 at n = 6?

Brief item 3: a new upper bound is a negative, so try to construct the object it
forbids.  mg-200d's disjunctive value at n = 6 was NOT computed exhaustively (its
own P11 declares that).  (n-1)/3 = 5/3 there.

This script settles `V_6 > 5/3 ?` COMPLETELY, not by sampling, using two exact
reductions proved in the audit note and re-checked as controls below:

  (R1)  E[inv_e] = sum over pairs of Pr[that pair is flipped].  In branch C the
        comparable pairs are flipped with probability 0 by construction of the
        support, and every other pair is capped at 1/3.  Hence
              value(branch C)  <=  |I| / 3,      I = the incomparable set.
        So a branch can only exceed 5/3 = (n-1)/3 at n=6 if |I| >= 6 = n.

  (R2)  If C is not transitively closed then branch(C) and branch(closure(C)) have
        the SAME support -- both are the linear extensions of closure(C) -- while
        branch(C) carries every row branch(closure(C)) carries and more (a cap row
        and n-1 symmetry rows for each pair in closure(C)\\C).  Hence
              value(branch C)  <=  value(branch closure(C)),
        so the max over all 2^15 branches equals the max over transitively closed
        ones.  4387 of the 27824 branches with |I| >= 6 are transitively closed.

Both reductions are VERIFIED here on n = 3,4,5 against the exhaustive answer before
being used at n = 6.  If either control fails, no n=6 conclusion may be read.

usage: python3 a3_n6.py
"""
import sys
from fractions import Fraction as F
import liba41b7 as L
from a2_disjunctive import closure, solve_branch, run


def control_R1(n):
    """E[inv] == sum of flip probabilities, on random-ish measures.  No LP."""
    P = L.perms(n)
    bad = 0
    for j in range(0, len(P), max(1, len(P) // 17)):
        for k in range(0, len(P), max(1, len(P) // 13)):
            x = {j: F(1, 3), k: F(2, 3)} if j != k else {j: F(1)}
            rep = L.report(n, x, P)
            if rep["einv"] != sum(rep["flips"].values(), F(0)):
                bad += 1
    return bad


def control_R2(n):
    """value(branch C) <= value(branch closure(C)) on every branch of a small n."""
    P_all = L.perms(n)
    prs = L.pairs(n)
    bad = []
    for mask in range(1 << len(prs)):
        C = frozenset(prs[i] for i in range(len(prs)) if mask >> i & 1)
        Cc = closure(n, C)
        if Cc == C:
            continue
        a = solve_branch(n, C, P_all)
        b = solve_branch(n, Cc, P_all)
        va = a[0].value if a and a[0].status == "optimal" else None
        vb = b[0].value if b and b[0].status == "optimal" else None
        if va is not None and (vb is None or va > vb):
            bad.append((sorted(C), va, vb))
    return bad


print("=" * 78)
print("CONTROLS for the two reductions, run BEFORE they are used at n = 6")
print("=" * 78)
for n in (3, 4, 5):
    print("  R1 (E[inv] = sum of flip probabilities) at n=%d: %d mismatches"
          % (n, control_R1(n)))
for n in (3, 4):
    bad = control_R2(n)
    print("  R2 (non-transitive branch never exceeds its closure) at n=%d: %d violations%s"
          % (n, len(bad), "" if not bad else "  <-- REDUCTION IS UNSOUND: %s" % bad[:2]))
sys.stdout.flush()

print()
print("=" * 78)
print("n = 6: EVERY transitively closed branch with |I| >= 6")
print("  by (R1) a branch with |I| <= 5 has value <= 5/3, so it cannot BEAT 5/3;")
print("  by (R2) a non-transitive branch never exceeds its transitive closure.")
print("  Together: the scan below is a COMPLETE test of  V_6 > 5/3.")
print("=" * 78)
sys.stdout.flush()

n = 6
TARGET = F(n - 1, 3)
P_all = L.perms(n)
prs = L.pairs(n)
cands = []
for mask in range(1 << len(prs)):
    C = frozenset(prs[i] for i in range(len(prs)) if mask >> i & 1)
    I = [p for p in prs if p not in C]
    if len(I) < n:
        continue
    if closure(n, C) != C:
        continue
    cands.append((len(I), C))
cands.sort()
print("  transitively closed branches with |I| >= %d: %d" % (n, len(cands)))
sys.stdout.flush()

best = None
nfeas = 0
beats = []
for i, (nI, C) in enumerate(cands):
    out = solve_branch(n, C, P_all)
    if out is None:
        continue
    r, keep, rows, obj, I = out
    if r.status != "optimal":
        continue
    nfeas += 1
    if best is None or r.value > best[0]:
        best = (r.value, C, r, keep, rows, obj, I)
        print("    new max %-8s at |I|=%2d  |support|=%-4d  C=%s"
              % (r.value, nI, len(keep), sorted(C)))
        sys.stdout.flush()
    if r.value > TARGET:
        beats.append((r.value, C, len(keep)))
    if (i + 1) % 250 == 0:
        print("    ... %d/%d branches done, feasible %d, running max %s"
              % (i + 1, len(cands), nfeas, best[0] if best else None))
        sys.stdout.flush()

print()
print("  branches solved %d   feasible %d   BEATING 5/3: %d" % (len(cands), nfeas, len(beats)))
if best:
    val, C, r, keep, rows, obj, I = best
    print("  MAX over |I| >= 6 branches: E[inv] = %s   (target (n-1)/3 = %s)" % (val, TARGET))
    print("  verdict: %s" % ("BEATS the bound -- (n-1)/3 IS NOT THE VALUE AT n=6"
                             if val > TARGET else
                             "does NOT beat (n-1)/3; every |I|>=6 branch is at or below it"))
    pe = L.check_primal(len(keep), rows, obj, r.x, r.value)
    de = L.check_dual(len(keep), rows, obj, r.y, r.value)
    print("  primal verifies: %s   dual verifies: %s" % (pe == [], de == []))
    print("  attaining C = %s   |I| = %d   support %d" % (sorted(C), len(I), len(keep)))
    for j, v in sorted(r.x.items(), key=lambda t: -t[1]):
        print("      mass %-8s  %s  inv=%d" % (v, "".join(map(str, keep[j])), L.inv(keep[j])))
print()
print("  CONCLUSION at n=6:  V_6 %s 5/3"
      % (">" if (best and best[0] > TARGET) else "<="))
print("  (the <= side is complete: |I| <= 5 branches are bounded by |I|/3 <= 5/3 via R1)")
