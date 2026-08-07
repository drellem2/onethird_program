"""a3b_level — one |I| level of the n=6 scan, so the levels can run in parallel.

Same computation as a3_n6.py, partitioned by |I| so that the complete answer is
available in wall-clock time.  The reductions R1/R2 and their controls live in
a3_n6.py and are not repeated here; this script assumes them and says so.

usage: python3 a3b_level.py <n> <|I|>
"""
import sys
from fractions import Fraction as F
import liba41b7 as L
from a2_disjunctive import closure, solve_branch

n = int(sys.argv[1])
lvl = int(sys.argv[2])
TARGET = F(n - 1, 3)

P_all = L.perms(n)
prs = L.pairs(n)
cands = []
for mask in range(1 << len(prs)):
    C = frozenset(prs[i] for i in range(len(prs)) if mask >> i & 1)
    if len(prs) - len(C) != lvl:
        continue
    if closure(n, C) != C:
        continue
    cands.append(C)

print("n=%d  |I|=%d  transitively closed branches: %d" % (n, lvl, len(cands)))
sys.stdout.flush()

best = None
nfeas = 0
for i, C in enumerate(cands):
    out = solve_branch(n, C, P_all)
    if out is None:
        continue
    r, keep, rows, obj, I = out
    if r.status != "optimal":
        continue
    nfeas += 1
    if best is None or r.value > best[0]:
        best = (r.value, C, r, keep, rows, obj)
        print("  |I|=%d new max %s  support=%d  C=%s"
              % (lvl, r.value, len(keep), sorted(C)))
        sys.stdout.flush()

print("n=%d |I|=%d DONE  branches=%d feasible=%d  MAX=%s  target (n-1)/3=%s  %s"
      % (n, lvl, len(cands), nfeas, best[0] if best else None, TARGET,
         "BEATS" if best and best[0] > TARGET else "does not beat"))
if best:
    val, C, r, keep, rows, obj = best
    pe = L.check_primal(len(keep), rows, obj, r.x, r.value)
    de = L.check_dual(len(keep), rows, obj, r.y, r.value)
    print("  certificates: primal %s  dual %s" % (pe == [], de == []))
    for j, v in sorted(r.x.items(), key=lambda t: -t[1]):
        print("      mass %-8s %s inv=%d" % (v, "".join(map(str, keep[j])), L.inv(keep[j])))
sys.stdout.flush()
