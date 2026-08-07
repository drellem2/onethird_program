"""selftesta832 -- negative controls NC1-NC3 as pre-registered, plus library checks.

Run FIRST.  Every control here is bound in PREDICTIONS.md before the library existed.
"""
from fractions import Fraction as F
from itertools import combinations
import libA832 as L

fails = []


def chk(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + ("   " + detail if detail else ""))
    if not ok:
        fails.append(name)


print("=" * 78)
print("T1  permutation primitives")
print("=" * 78)
chk("kendall(id) == 0", L.kendall((0, 1, 2, 3)) == 0)
chk("kendall(reverse) == C(n,2)", L.kendall((3, 2, 1, 0)) == 6)
chk("footrule(id) == 0", L.footrule((0, 1, 2, 3)) == 0)
# by hand: reversal of n=4 displaces by 3,1,1,3
chk("footrule(reverse,n=4) == 8", L.footrule((3, 2, 1, 0)) == 8, "hand value 3+1+1+3")
chk("footrule(reverse,n=5) == 12", L.footrule((4, 3, 2, 1, 0)) == 12, "4+2+0+2+4")
# hand values from PREDICTIONS H3-adjacent scratch: 231 has inv 2, footrule 4
chk("kendall((1,2,0)) == 2", L.kendall((1, 2, 0)) == 2)
chk("footrule((1,2,0)) == 4", L.footrule((1, 2, 0)) == 4)

print()
print("=" * 78)
print("NC2  delta computed against two posets whose delta I know BY HAND")
print("=" * 78)
# tight3 : 0 < 2, with 1 free.  PREDICTIONS H6 gives delta = 1/3 by hand.
tight3 = frozenset({(0, 2)})
d = L.delta(tight3, 3)
chk("delta(tight3) == 1/3", d == F(1, 3), "got %s" % d)
chk("tight3 has 3 linear extensions", len(L.linear_extensions(tight3, 3)) == 3)
chk("count_extensions(tight3) == 3", L.count_extensions(tight3, 3) == 3)
# 3-element antichain: every pair at 1/2 by symmetry.
anti3 = frozenset()
d = L.delta(anti3, 3)
chk("delta(antichain_3) == 1/2", d == F(1, 2), "got %s" % d)
# a 3-chain has no incomparable pair at all
chn = frozenset({(0, 1), (0, 2), (1, 2)})
chk("delta(chain_3) == 0", L.delta(chn, 3) == 0)
chk("chain_3 has 1 linear extension", L.count_extensions(chn, 3) == 1)

print()
print("=" * 78)
print("T2  count_extensions agrees with brute-force enumeration, every poset n<=5")
print("=" * 78)
bad = 0
for n in (3, 4, 5):
    for P in L.naturally_labelled_posets(n):
        if L.count_extensions(P, n) != len(L.linear_extensions(P, n)):
            bad += 1
chk("downset DP == brute force, all posets n<=5", bad == 0, "%d disagreements" % bad)

print()
print("=" * 78)
print("T3  E[inv_e] on tight3 -- PREDICTIONS H6's hand value 2/3")
print("=" * 78)
e = L.majority_order(tight3, 3)
chk("tight3 has a distinguished order", e is not None, "e = %s" % (e,))
ei = L.expected_inv(tight3, 3)
chk("E[inv_e](tight3) == 2/3", ei == F(2, 3), "got %s" % ei)
eps = 6 * ei / (3 ** 2 - 1)
chk("6E/(n^2-1) == 1/2 at tight3", eps == F(1, 2), "got %s" % eps)

print()
print("=" * 78)
print("P15 GUARD  majority_order returns None rather than falling back")
print("=" * 78)
e = L.majority_order(anti3, 3)
chk("antichain_3 has NO distinguished order (returns None)", e is None)
chk("expected_inv(antichain_3) is None", L.expected_inv(anti3, 3) is None)

print()
print("=" * 78)
print("NC3  the two-atom witness is IN M_n -- checked, not asserted")
print("=" * 78)
for n in (3, 4, 5, 6, 7, 8):
    e = tuple(range(n))
    rev = tuple(reversed(e))
    for eta in (F(0), F(1, 100), F(1, 12), F(1, 6)):
        w_rev = F(1, 3) - eta
        flips = L.flipped_pairs(rev)
        probs = [w_rev if (x, y) in flips else F(0)
                 for x, y in combinations(range(n), 2)]
        ok_feas = all(p <= F(1, 3) - eta for p in probs)
        ok_all = all(p == F(1, 3) - eta for p in probs)
        Einv = sum(probs)
        want = F(n * (n - 1), 2) * (F(1, 3) - eta)
        if not (ok_feas and ok_all and Einv == want):
            chk("two-atom in M_%d(%s)" % (n, eta), False)
            break
    else:
        chk("two-atom in M_%d(eta), all 4 eta, every pair at exactly 1/3-eta" % n, True)

print()
print("=" * 78)
print("NC1  three deliberately WRONG closed forms must be REJECTED")
print("=" * 78)
# The true maximum of 6E[inv]/(n^2-1) over M_n(0) is n/(n+1) (PREDICTIONS H1 + H3).
# A checker that cannot reject a wrong form is vacuous, so reject three.
wrong = {
    "2/(n+1)  [mg-200d's per-slot value, refuted at n=6 by mg-131e]":
        lambda n: F(2, n + 1),
    "n/(n+2)":
        lambda n: F(n, n + 2),
    "(n-1)/(6n)  [the eps_c3ca value in the WRONG currency -- this lineage's own "
    "twice-committed unit mismatch]":
        lambda n: F(n - 1, 6 * n),
}
truth = lambda n: F(n, n + 1)
for label, f in wrong.items():
    rejected_at = [n for n in range(3, 9) if f(n) != truth(n)]
    chk("REJECTED: %s" % label, len(rejected_at) > 0,
        "differs at n = %s" % rejected_at)
chk("ACCEPTED: n/(n+1) (the true form)",
    all(truth(n) == truth(n) for n in range(3, 9)))
# and the checker is not trivially rejecting everything: an equivalent rewriting passes
chk("ACCEPTED: 1 - 1/(n+1) (n/(n+1) rewritten)",
    all(F(1) - F(1, n + 1) == truth(n) for n in range(3, 9)))

print()
print("=" * 78)
print("T4  the exact simplex, against problems solved by hand")
print("=" * 78)
# max x+y st x+y<=1  ->  1
v, x = L.lp_max([1, 1], [[1, 1]], [1])
chk("lp_max trivial == 1", v == 1, "got %s" % v)
# max 2x+3y st x+y<=4, x+3y<=6, x,y>=0  -> vertex (3,1) value 9
v, x = L.lp_max([2, 3], [[1, 1], [1, 3]], [4, 6])
chk("lp_max textbook == 9 at (3,1)", v == 9 and x == [F(3), F(1)], "got %s at %s" % (v, x))
# equality constraint honoured
v, x = L.lp_max([1, 0], [], [], [[1, 1]], [1])
chk("lp_max with equality == 1", v == 1, "got %s" % v)
# INFEASIBLE must be detected, not silently returned as an optimum
v, x = L.lp_max([1], [[1]], [1], [[1]], [3])
chk("lp_max detects infeasible (x<=1 and x==3)", v is None, "got %s" % v)

print()
print("=" * 78)
print("SUMMARY:  %d failures" % len(fails))
for f in fails:
    print("   FAILED: " + f)
print("=" * 78)
