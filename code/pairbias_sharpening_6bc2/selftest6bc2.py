"""mg-6bc2 -- self-test.  Positive AND negative controls, declared exit value 0.

A self-test that only checks the happy path is a vacuous pass, which is this
arc's signature defect.  Every construction below either asserts a value I
computed BY HAND before the script existed, or is a MUTATION that must fail.
"""

import sys
from fractions import Fraction as F
from itertools import permutations

from lp6bc2 import (inv_count, footrule, flipped_pairs, relaxation_lp,
                    two_atom, hierarchical, measure_stats, simplex_max)

fails = []


def check(name, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: got {got}, want {want}")
    if not ok:
        fails.append(name)


print("S1  combinatorial primitives, against hand values")
# reversal of 4: inversions = C(4,2) = 6; footrule = |0-3|+|1-2|+|2-1|+|3-0| = 8
check("inv(reversal,n=4)", inv_count((3, 2, 1, 0)), 6)
check("footrule(reversal,n=4)", footrule((3, 2, 1, 0)), 8)
check("inv(identity,n=4)", inv_count((0, 1, 2, 3)), 0)
# half-rotation of 4: (2,3,0,1).  each element moves 2 -> footrule 8;
# flipped pairs are exactly those crossing the middle: {0,1}x{2,3} = 4
check("footrule(halfrot,n=4)", footrule((2, 3, 0, 1)), 8)
check("inv(halfrot,n=4)", inv_count((2, 3, 0, 1)), 4)
check("halfrot saturates DG (F=2I)", footrule((2, 3, 0, 1)), 2 * inv_count((2, 3, 0, 1)))
check("reversal does NOT saturate DG", footrule((3, 2, 1, 0)) == 2 * inv_count((3, 2, 1, 0)), False)

print("S2  simplex, against a hand-solved 2-variable LP")
# max 3x+2y s.t. x+y<=4, x<=2  ->  x=2,y=2, value 10
val, x = simplex_max([[F(1), F(1)], [F(1), F(0)]], [F(4), F(2)], [F(3), F(2)])
check("simplex value", val, F(10))
check("simplex argmax", x, [F(2), F(2)])

print("S3  the two-atom law -- hand value H2/H3, n=5")
n = 5
ei, ef, qmax, asym = measure_stats(n, two_atom(n))
check("two-atom max flip prob", qmax, F(1, 3))
check("two-atom E[inv] = C(n,2)/3", ei, F(10, 3))
# reversal of 5 has footrule 4+2+0+2+4 = 12; E[F] = 12/3 = 4
check("two-atom E[footrule]", ef, F(4))
check("two-atom VIOLATES adjacency symmetry", len(asym) > 0, True)

print("S4  NEGATIVE CONTROL -- a measure that must FAIL the frozen cap")
# uniform on S_n has every flip prob 1/2 > 1/3
uni = {p: F(1, 120) for p in permutations(range(5))}
_, _, qmax_u, asym_u = measure_stats(5, uni)
check("uniform max flip prob is 1/2 (infeasible)", qmax_u, F(1, 2))
check("uniform SATISFIES adjacency symmetry", asym_u, [])

print("S5  NEGATIVE CONTROL -- mutate the cap, the optimum must move")
for cap, want in ((F(1, 3), F(1)), (F(1, 6), F(1, 2))):
    v, _ = relaxation_lp(3, inv_count, cap=cap)
    check(f"LP inv optimum at cap {cap} = 3*cap", v, want)

print("S6  NEGATIVE CONTROL -- a broken objective must not reproduce the answer")
v_bad, _ = relaxation_lp(3, lambda p: 0)
check("zero objective gives 0 (detector is not constant)", v_bad, F(0))

print("S7  hierarchical construction, n=8, hand value H4")
h = hierarchical(8, levels=3)
ei8, ef8, q8, _ = measure_stats(8, h)
check("hierarchical max flip prob <= 1/3", q8 <= F(1, 3), True)
check("hierarchical E[F] = 2 E[inv] (all atoms saturate DG)", ef8, 2 * ei8)
# levels give F = 32, 16, 8 at n=8 -> E[F] = (32+16+8)/3 = 56/3
check("hierarchical E[footrule] = 56/3", ef8, F(56, 3))

print()
if fails:
    print(f"SELFTEST FAILED: {fails}")
    sys.exit(1)
print("SELFTEST OK -- 7 constructions, 3 of them negative controls")
sys.exit(0)
