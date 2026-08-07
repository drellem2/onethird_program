"""selftesta41b7 — self-tests and negative controls for liba41b7.

The load-bearing one is NC1: an INFEASIBLE system and a FEASIBLE system whose
optimum is 0 must come back as DIFFERENT statuses.  That is prediction P14's
guard, and no LP result in this audit may be reported if NC1 does not fire.
"""
import sys
from fractions import Fraction as F
import liba41b7 as L

ok = 0
bad = []


def check(name, cond, detail=""):
    global ok
    if cond:
        ok += 1
        print("  PASS  %s" % name)
    else:
        bad.append(name)
        print("  FAIL  %s   %s" % (name, detail))


print("== combinatorics ==")
check("|S_3| = 6", len(L.perms(3)) == 6)
check("|S_5| = 120", len(L.perms(5)) == 120)
check("|S_6| = 720", len(L.perms(6)) == 720)
check("perms distinct", len(set(L.perms(5))) == 120)
check("inv(e) = 0", L.inv((0, 1, 2, 3)) == 0)
check("inv(rev e) = C(4,2)", L.inv((3, 2, 1, 0)) == 6)
check("inv(1,0,2) = 1", L.inv((1, 0, 2)) == 1)
# inversion distribution of S_4 is the Gaussian binomial 1,3,5,6,5,3,1
dist = [0] * 7
for s in L.perms(4):
    dist[L.inv(s)] += 1
check("S_4 inversion distribution 1,3,5,6,5,3,1", dist == [1, 3, 5, 6, 5, 3, 1], str(dist))
check("mean inv over S_5 = C(5,2)/2", F(sum(L.inv(s) for s in L.perms(5)), 120) == F(10, 2))

print("== simplex, textbook cases ==")
# max 3x + 5y  s.t. x <= 4, 2y <= 12, 3x + 2y <= 18   -> 36 at (2,6)
rows = [({0: F(1)}, "<=", F(4)),
        ({1: F(2)}, "<=", F(12)),
        ({0: F(3), 1: F(2)}, "<=", F(18))]
r = L.solve(2, rows, {0: F(3), 1: F(5)})
check("textbook LP optimum 36", r.status == "optimal" and r.value == 36, repr(r))
check("textbook LP witness (2,6)", r.x.get(0) == 2 and r.x.get(1) == 6, str(r.x))
check("textbook LP primal verifies", L.check_primal(2, rows, {0: F(3), 1: F(5)}, r.x, r.value) == [])
check("textbook LP dual verifies", L.check_dual(2, rows, {0: F(3), 1: F(5)}, r.y, r.value) == [])

# equality-constrained: max x+y s.t. x+y = 1, x - y = 0  -> 1 at (1/2,1/2)
rows = [({0: F(1), 1: F(1)}, "=", F(1)), ({0: F(1), 1: F(-1)}, "=", F(0))]
r = L.solve(2, rows, {0: F(1), 1: F(1)})
check("equality LP optimum 1", r.status == "optimal" and r.value == 1, repr(r))
check("equality LP witness (1/2,1/2)", r.x.get(0) == F(1, 2) and r.x.get(1) == F(1, 2), str(r.x))
check("equality LP dual verifies", L.check_dual(2, rows, {0: F(1), 1: F(1)}, r.y, r.value) == [])

# >= row, forcing phase 1 to work.
#   max x + 2y  s.t.  x + y <= 10,  x >= 3   ->   17 at (3,7).
#   DEFECT OF MINE, KEPT: this check was first written expecting 20, and FAILED
#   against correct code -- the solver returned 17 and its dual verified at 17.
#   The expectation was wrong (x >= 3 is a floor on x, not a ceiling on y), so a
#   negative control of mine fired against a correct simplex.  Corrected here and
#   recorded rather than quietly retuned.
rows = [({0: F(1), 1: F(1)}, "<=", F(10)), ({0: F(1)}, ">=", F(3))]
r = L.solve(2, rows, {0: F(1), 1: F(2)})
check(">= row optimum 17 at (3,7)",
      r.status == "optimal" and r.value == 17 and r.x.get(0) == 3 and r.x.get(1) == 7, repr(r))
check(">= row dual verifies", L.check_dual(2, rows, {0: F(1), 1: F(2)}, r.y, r.value) == [])

print("== NC1: infeasible vs feasible-with-optimum-0 (guard for P14) ==")
inf_rows = [({0: F(1)}, ">=", F(2)), ({0: F(1)}, "<=", F(1))]
r_inf = L.solve(1, inf_rows, {0: F(1)})
check("NC1a infeasible reported as infeasible", r_inf.status == "infeasible", repr(r_inf))
check("NC1a phase-1 residual is strictly positive",
      r_inf.status == "infeasible" and r_inf.phase1 > 0, repr(r_inf))

zero_rows = [({0: F(1)}, "<=", F(0)), ({0: F(1)}, ">=", F(0))]
r_zero = L.solve(1, zero_rows, {0: F(1)})
check("NC1b feasible-with-value-0 reported as OPTIMAL, value 0",
      r_zero.status == "optimal" and r_zero.value == 0, repr(r_zero))
check("NC1b phase-1 residual is exactly 0",
      r_zero.status == "optimal" and r_zero.phase1 == 0, repr(r_zero))
check("NC1 the two are DISTINGUISHED", r_inf.status != r_zero.status)

nz_rows = [({0: F(1)}, "<=", F(7)), ({0: F(1)}, ">=", F(2))]
r_nz = L.solve(1, nz_rows, {0: F(1)})
check("NC1c feasible with nonzero optimum 7", r_nz.status == "optimal" and r_nz.value == 7, repr(r_nz))

# an infeasible EQUALITY system (the shape the per-slot rows actually take)
inf_eq = [({0: F(1), 1: F(1)}, "=", F(1)),
          ({0: F(1), 1: F(1)}, "=", F(2))]
r = L.solve(2, inf_eq, {0: F(1)})
check("NC1d infeasible equality system reported infeasible", r.status == "infeasible", repr(r))

print("== NC2: the dual verifier must REJECT a wrong dual ==")
rows = [({0: F(1)}, "<=", F(4)), ({0: F(3), 1: F(2)}, "<=", F(18)), ({1: F(2)}, "<=", F(12))]
obj = {0: F(3), 1: F(5)}
r = L.solve(2, rows, obj)
bad_y = [v + F(1) for v in r.y]
check("NC2 tampered dual is rejected", L.check_dual(2, rows, obj, bad_y, r.value) != [])
check("NC2 negated dual is rejected", L.check_dual(2, rows, obj, [-v for v in r.y], r.value) != [])

print("== NC3: the primal verifier must REJECT an infeasible point ==")
check("NC3 x out of the polytope is rejected",
      L.check_primal(2, rows, obj, {0: F(100), 1: F(100)}, F(800)) != [])
check("NC3 right point, wrong claimed value is rejected",
      L.check_primal(2, rows, obj, r.x, r.value + 1) != [])

print("== row builders ==")
P3 = L.perms(3)
check("pairbias rows: 3 at n=3", len(L.rows_pairbias(3, P3)) == 3)
check("perslot rows: (n-1)*C(n,2) = 6 at n=3", len(L.rows_perslot_symmetry(3, P3)) == 6)
check("aggregate rows: C(n,2) = 3 at n=3", len(L.rows_aggregate_symmetry(3, P3)) == 3)
P5 = L.perms(5)
check("perslot rows: 4*10 = 40 at n=5", len(L.rows_perslot_symmetry(5, P5)) == 40)

# uniform satisfies every symmetry row, at every n
for n in (3, 4, 5):
    P = L.perms(n)
    u = {j: F(1, len(P)) for j in range(len(P))}
    rep = L.report(n, u, P)
    check("uniform has no per-slot violation at n=%d" % n, rep["slot_violations"] == {})
    check("uniform has no aggregate violation at n=%d" % n, rep["agg_violations"] == {})
    check("uniform flips are all 1/2 at n=%d" % n,
          all(v == F(1, 2) for v in rep["flips"].values()))

# the two-atom law: mu = (2/3)d_e + (1/3)d_{rev e}
for n in (3, 4, 5, 6, 7):
    e = tuple(range(n))
    rev = tuple(reversed(e))
    x = L.measure_from_atoms(n, {e: F(2, 3), rev: F(1, 3)})
    rep = L.report(n, x, L.perms(n))
    check("two-atom law: mass 1 at n=%d" % n, rep["mass"] == 1)
    check("two-atom law: E[inv] = C(n,2)/3 at n=%d" % n,
          rep["einv"] == F(n * (n - 1), 6), str(rep["einv"]))
    check("two-atom law: every flip is exactly 1/3 at n=%d" % n,
          all(v == F(1, 3) for v in rep["flips"].values()))
    check("two-atom law: eps_spec = n/(n+1) at n=%d" % n,
          L.eps_spec(n, rep["einv"]) == F(n, n + 1))

print()
print("PASS %d   FAIL %d" % (ok, len(bad)))
if bad:
    print("failed:", bad)
sys.exit(1 if bad else 0)
