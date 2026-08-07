"""mg-6bc2 V1 -- the marginal-relaxation optimum, both forms of the master bound.

Prints, for each n:
  * max E[inv_e]  over the relaxation, and C(n,2)/3 (the value Claim 6.1 asserts)
  * the resulting eps_spec = 6 E[inv]/(n^2-1)
  * max E[footrule] over the relaxation, and the resulting 3 E[F]/(n^2-1)
  * the same two numbers for the two-atom law and the hierarchical construction
  * whether each optimiser violates adjacency symmetry
"""

import sys
from fractions import Fraction as F

from lp6bc2 import (inv_count, footrule, relaxation_lp, two_atom,
                    hierarchical, measure_stats)

NS = [int(a) for a in sys.argv[1:]] or [3, 4, 5, 6]


def show(x):
    return f"{x} = {float(x):.6f}"


print("=" * 78)
print("V1  MARGINAL RELAXATION: max over ALL measures on S_n with every pair-flip <= 1/3")
print("    (this is 'pair bias alone'.  No posets are enumerated.)")
print("=" * 78)

for n in NS:
    half = F(n * (n - 1), 2)
    print(f"\n--- n = {n} ---   C(n,2) = {half},  C(n,2)/3 = {half/3},  n/(n+1) = {F(n, n+1)}")

    vi, si = relaxation_lp(n, inv_count)
    eps_inv = 6 * vi / (n * n - 1)
    print(f"  max E[inv_e]           = {show(vi)}")
    print(f"    Claim 6.1's m/3      = {show(half/3)}   -> P1 {'HELD' if vi == half/3 else 'REFUTED'}")
    print(f"    eps_spec = 6E/(n^2-1)= {show(eps_inv)}")
    print(f"    n/(n+1)              = {show(F(n, n+1))}   -> {'MATCH' if eps_inv == F(n, n+1) else 'DIFFER'}")
    print(f"    optimiser support    = {len(si)} permutations")

    vf, sf = relaxation_lp(n, footrule)
    eps_f = 3 * vf / (n * n - 1)
    print(f"  max E[footrule]        = {show(vf)}")
    print(f"    3E[F]/(n^2-1)        = {show(eps_f)}")
    print(f"    (n^2-1)/3 = eps 1 at = {show(F(n*n-1, 3))}")
    print(f"    optimiser support    = {len(sf)} permutations")

    ta = two_atom(n)
    ei, ef, q, asym = measure_stats(n, ta)
    print(f"  two-atom law: E[inv]={ei}  eps_inv={show(6*ei/(n*n-1))}"
          f"  E[F]={ef}  eps_F={show(3*ef/(n*n-1))}")
    print(f"    attains inv optimum? {'YES' if ei == vi else 'no'}"
          f"   attains footrule optimum? {'YES' if ef == vf else 'no'}")
    print(f"    adjacency symmetry violated at {len(asym)} ordered pairs")

    if n % 4 == 0:
        h = hierarchical(n, levels=3)
        ei2, ef2, q2, asym2 = measure_stats(n, h)
        print(f"  hierarchical: E[inv]={ei2}  E[F]={ef2}  eps_F={show(3*ef2/(n*n-1))}"
              f"  maxflip={q2}")

    _, _, _, asym_i = measure_stats(n, si)
    _, _, _, asym_f = measure_stats(n, sf)
    print(f"  P6: inv-optimiser violates adjacency symmetry: "
          f"{'YES' if asym_i else 'NO'} ({len(asym_i)} ordered pairs)")
    print(f"      F-optimiser   violates adjacency symmetry: "
          f"{'YES' if asym_f else 'NO'} ({len(asym_f)} ordered pairs)")
