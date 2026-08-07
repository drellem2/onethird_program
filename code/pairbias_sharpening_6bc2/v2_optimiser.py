"""mg-6bc2 V2 -- WHAT the optimiser is, and which joint facts it violates.

The optimum value alone does not say where the route stops.  What says it is the
WITNESS: an explicit measure that is feasible for pair bias, attains the bound,
and is not the linear-extension measure of any poset.  This prints it, and tests
it against the two already-proven joint facts the corpus has:

  * AGGREGATE adjacency symmetry   Pr[x imm-prec y] = Pr[y imm-prec x]
  * PER-SLOT adjacency symmetry    J_k(x,y) = J_k(y,x) for every position k
    (mg-92e6's form -- strictly stronger)

Both hold for the uniform measure on L(P) of any poset P, for every incomparable
pair, by the swap bijection.  So any optimiser violating either is NOT realisable.
"""

import sys
from fractions import Fraction as F

from lp6bc2 import inv_count, footrule, relaxation_lp, two_atom, measure_stats

NS = [int(a) for a in sys.argv[1:]] or [3, 4, 5]


def per_slot_violations(n, mu):
    """Ordered ((x,y),k) with J_k(x,y) != J_k(y,x)."""
    J = {}
    for p, w in mu.items():
        for k in range(n - 1):
            J[(p[k], p[k + 1], k)] = J.get((p[k], p[k + 1], k), F(0)) + w
    bad = []
    for x in range(n):
        for y in range(n):
            if x < y:
                for k in range(n - 1):
                    if J.get((x, y, k), F(0)) != J.get((y, x, k), F(0)):
                        bad.append(((x, y), k))
    return bad


for n in NS:
    print("=" * 70)
    print(f"n = {n}")
    for name, obj in (("E[inv_e]", inv_count), ("E[footrule]", footrule)):
        val, sup = relaxation_lp(n, obj)
        print(f"\n  optimiser for max {name} = {val}:")
        for p, w in sorted(sup.items(), key=lambda t: -t[1]):
            print(f"     mass {str(w):>8}  perm {p}"
                  f"   inv={inv_count(p)} F={footrule(p)}")
        ei, ef, q, asym = measure_stats(n, sup)
        ps = per_slot_violations(n, sup)
        print(f"     E[inv]={ei}  E[F]={ef}  max flip prob={q}")
        print(f"     F = 2*inv ?  {'YES -- Diaconis-Graham is TIGHT here' if ef == 2*ei else 'no'}")
        print(f"     aggregate adjacency symmetry violated at {len(asym)} ordered pairs")
        print(f"     PER-SLOT  adjacency symmetry violated at {len(ps)} (pair,slot)s")

    ta = two_atom(n)
    ei, ef, q, asym = measure_stats(n, ta)
    ps = per_slot_violations(n, ta)
    print(f"\n  two-atom law:  E[inv]={ei}  E[F]={ef}  maxflip={q}")
    print(f"     aggregate adjacency symmetry violated at {len(asym)} ordered pairs")
    print(f"     PER-SLOT  adjacency symmetry violated at {len(ps)} (pair,slot)s")
