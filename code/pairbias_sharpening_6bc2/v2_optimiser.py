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

⚠️ TWO DEFECTS REPAIRED BY mg-ba78, both downstream of the optimum and neither
touching the theorem:
  (1) the optimisers this printed were SUB-PROBABILITY measures (mass 2/3 at
      n = 3) and the diagnostics ran on them.  lp6bc2.relaxation_lp now completes
      on the identity, which changes no objective value.  n = 3's aggregate count
      goes 0 -> 2 as a result; n >= 4 was already at mass 1 and is unmoved by it.
  (2) the two columns were in DIFFERENT UNITS -- aggregate over ordered adjacency
      keys, per-slot over x < y crossed with slots.  Both are now reported per
      UNORDERED pair, and the (pair, slot) count is printed beside them as the
      strictly finer unit it is.  On the common unit the two nest:
      aggregate-violated pairs are a subset of per-slot-violated pairs, since
      sum_k J_k(x,y) != sum_k J_k(y,x) forces some slot to differ.
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


def report(n, mu, label):
    """Both diagnostics, on the COMMON unit, with the finer unit labelled."""
    npairs = n * (n - 1) // 2
    nslots = npairs * (n - 1)
    ei, ef, q, asym = measure_stats(n, mu)          # UNORDERED pairs (mg-ba78)
    ps = per_slot_violations(n, mu)                 # (unordered pair, slot)
    ps_pairs = sorted({pr for pr, _k in ps})
    assert set(asym) <= set(ps_pairs), f"{label}: nesting failed at n={n}"
    mass = sum(mu.values())
    print(f"     total mass={mass}"
          f"{'' if mass == 1 else '   <-- SUB-PROBABILITY, diagnostics are unsound'}")
    print(f"     E[inv]={ei}  E[F]={ef}  max flip prob={q}")
    print(f"     AGGREGATE adjacency symmetry violated at {len(asym)}/{npairs} UNORDERED PAIRS")
    print(f"     PER-SLOT  adjacency symmetry violated at {len(ps_pairs)}/{npairs} UNORDERED PAIRS")
    print(f"       (finer unit, not comparable to the two above:"
          f" {len(ps)}/{nslots} (pair,slot)s)")
    return ei, ef


for n in NS:
    print("=" * 70)
    print(f"n = {n}")
    for name, obj in (("E[inv_e]", inv_count), ("E[footrule]", footrule)):
        val, sup = relaxation_lp(n, obj)
        print(f"\n  optimiser for max {name} = {val}:")
        for p, w in sorted(sup.items(), key=lambda t: -t[1]):
            print(f"     mass {str(w):>8}  perm {p}"
                  f"   inv={inv_count(p)} F={footrule(p)}")
        ei, ef = report(n, sup, name)
        print(f"     F = 2*inv ?  {'YES -- Diaconis-Graham is TIGHT here' if ef == 2*ei else 'no'}")

    print("\n  two-atom law:")
    report(n, two_atom(n), "two-atom")
