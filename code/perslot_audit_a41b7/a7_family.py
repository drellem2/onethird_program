"""a7_family — brief item 3: BUILD THE MEASURE THE NEW BOUND FORBIDS, at every n.

a3_n6.py already exhibits one: at n = 6 a branch reaches 11/6 > 5/3 = (n-1)/3.
A single point is a refutation but not a family.  This script asks whether the same
shape works at every n, which is what decides whether (n-1)/3 fails once or always.

The n=6 witness lives on the branch whose incomparable set is

    I = the n-1 CONSECUTIVE pairs, PLUS the single extra pair (1,4)

i.e. the poset  i < j  iff  j >= i+2,  with the one relation 1 < 4 DELETED.  That is
still transitively closed: a forced (1,4) would need some x with (1,x) and (x,4) both
comparable, i.e. x >= 3 and x <= 2.

So the family tested here is:  FENCE(n) with k deleted relations (1,4), (5,8),
(9,12), ... spaced 4 apart so that no two deletions interact.  k = 0 recovers
mg-200d's own construction and must return exactly (n-1)/3, which is the control that
says the machinery is not simply inflating everything.

usage: python3 a7_family.py 6 7 8 9 10 11 12
"""
import sys
from fractions import Fraction as F
import liba41b7 as L
from a2_disjunctive import closure, solve_branch


def fence_minus(n, deletions):
    """C = {(i,j) : j >= i+2} with the listed pairs deleted."""
    C = set((i, j) for i in range(n) for j in range(i + 2, n))
    for d in deletions:
        C.discard(d)
    return frozenset(C)


def extras(n, k):
    """Up to k non-interacting deletions (1,4), (5,8), (9,12), ..."""
    out = []
    t = 0
    while len(out) < k:
        a, b = 4 * t + 1, 4 * t + 4
        if b >= n:
            break
        out.append((a, b))
        t += 1
    return out


NS = [int(a) for a in sys.argv[1:]] or [6, 7, 8, 9, 10]

print("=" * 78)
print("A FAMILY THAT BEATS (n-1)/3 -- fence(n) with k spaced deletions")
print("=" * 78)
print("  k = 0 is mg-200d's own construction and MUST return exactly (n-1)/3.")
print()
for n in NS:
    P_all = L.perms(n)
    target = F(n - 1, 3)
    line = []
    for k in range(0, 4):
        dels = extras(n, k)
        if len(dels) < k:
            break
        C = fence_minus(n, dels)
        if closure(n, C) != C:
            line.append("k=%d NOT-TRANSITIVE" % k)
            continue
        out = solve_branch(n, C, P_all)
        if out is None:
            line.append("k=%d empty" % k)
            continue
        r, keep, rows, obj, I = out
        if r.status != "optimal":
            line.append("k=%d %s" % (k, r.status))
            continue
        pe = L.check_primal(len(keep), rows, obj, r.x, r.value)
        de = L.check_dual(len(keep), rows, obj, r.y, r.value)
        atoms = {keep[j]: v for j, v in r.x.items()}
        rep = L.report_atoms(n, atoms)
        clean = (rep["mass"] == 1
                 and max(rep["flips"].values()) <= F(1, 3)
                 and all(rep["flips"][p] == 0 for p in C)
                 and not [z for z in rep["slot_violations"] if (z[1], z[2]) in I])
        mark = ("BEATS by %s" % (r.value - target)) if r.value > target else (
            "= (n-1)/3" if r.value == target else "below")
        line.append("k=%d |I|=%2d sup=%-4d val=%-8s %s%s%s"
                    % (k, len(I), len(keep), r.value, mark,
                       "" if pe == [] and de == [] else "  [CERT FAIL]",
                       "" if clean else "  [WITNESS FAILS SUBSTITUTION]"))
        if k == 0 and r.value != target:
            line[-1] += "   <-- CONTROL BROKEN"
    print("  n=%-3d (n-1)/3 = %-8s eps_spec target 2/(n+1) = %s" % (n, target, F(2, n + 1)))
    for z in line:
        print("        " + z)
    sys.stdout.flush()

print()
print("=" * 78)
print("The n = 6 witness, written out in full (brief item 3's deliverable)")
print("=" * 78)
n = 6
C = fence_minus(6, [(1, 4)])
r, keep, rows, obj, I = solve_branch(n, C, L.perms(n))
atoms = {keep[j]: v for j, v in r.x.items()}
rep = L.report_atoms(n, atoms)
print("  comparable C   = %s" % sorted(C))
print("  incomparable I = %s   (|I| = %d = n, one more than n-1)" % (sorted(I), len(I)))
print("  measure (%d atoms):" % len(atoms))
for s, w in sorted(atoms.items(), key=lambda t: (-t[1], t[0])):
    print("      %s   mass %s   inv = %d" % ("".join(map(str, s)), w, L.inv(s)))
print("  mass = %s   E[inv] = %s   (n-1)/3 = %s   eps_spec = %s   2/(n+1) = %s"
      % (rep["mass"], rep["einv"], F(5, 3), L.eps_spec(6, rep["einv"]), F(2, 7)))
print("  flip probabilities: %s"
      % {str(k): str(v) for k, v in sorted(rep["flips"].items()) if v != 0})
print("  every flip <= 1/3: %s" % all(v <= F(1, 3) for v in rep["flips"].values()))
print("  comparable pairs with nonzero flip: %d"
      % len([p for p in C if rep["flips"][p] != 0]))
print("  per-slot symmetry violations on incomparable pairs: %d"
      % len([z for z in rep["slot_violations"] if (z[1], z[2]) in I]))
print("  dual certificate verifies: %s" % (L.check_dual(len(keep), rows, obj, r.y, r.value) == []))
