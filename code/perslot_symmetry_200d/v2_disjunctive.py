"""mg-200d V2 -- the DISJUNCTIVE value: exactly what realisability forces, no slack.

Realisability, with `e` the identity and a linear extension of `P`, says of each pair `x<y`:

    EITHER  x,y are comparable      -- then `Pr[y before x] = 0`
    OR      x,y are incomparable    -- then `J_k(x,y) = J_k(y,x)` for every slot k

That is a DISJUNCTION, not a linear constraint, so the feasible set is a union of
`2^C(n,2)` polytopes and the exact value is the maximum over them.  This script computes
that maximum in exact rationals, and reports the branch that attains it.

THREE runs, and the third is the control that decides whether the finding is real:

  per-slot    -- symmetry on incomparable pairs, per slot          (mg-92e6's form)
  aggregate   -- symmetry on incomparable pairs, summed over slots (the weaker form)
  CONTROL     -- the same branching with NO symmetry at all.  `{q=0}` union `{q<=1/3}`
                 IS `{q<=1/3}`, so this MUST return C(n,2)/3.  If it does not, the gain
                 is an artefact of the branch structure and the headline is wrong (P13).

NO POSET IS ENUMERATED.  Transitivity is never imposed, so the branch family is a strict
superset of the comparability patterns of actual posets -- which is exactly what makes the
maximum a valid upper bound rather than a search over a class the corpus believes empty.
"""

import sys
from fractions import Fraction as F
from itertools import combinations

from lp200d import (Infeasible, inv_count, relaxation, measure_report, eps_spec, pairs_of,
                    uniform_le_measure)

NS = [int(a) for a in sys.argv[1:]] or [3, 4]

RUNS = [("per-slot", "slot_eq"), ("aggregate", "agg_eq"), ("CONTROL no-symmetry", "none")]


def is_transitive(n, comp):
    """Is the declared comparable set already a partial order (so a real poset)?"""
    return all((x, w) in comp for (x, y) in comp for (z, w) in comp if y == z)


def disjunctive(n, form):
    """(best value, best comparable-set, witness, #feasible, #branches, max #incomparable)."""
    prs = pairs_of(n)
    best, best_comp, best_mu, nfeas, max_inc = None, None, None, 0, 0
    for r in range(len(prs) + 1):
        for comp in combinations(prs, r):
            try:
                val, mu = relaxation(n, form, comparable=frozenset(comp))
            except Infeasible:
                continue
            nfeas += 1
            # only branches that can carry positive flip mass count toward the sparsity claim
            inc = len(prs) - len(comp)
            if val > 0:
                max_inc = max(max_inc, inc)
            if best is None or val > best:
                best, best_comp, best_mu = val, frozenset(comp), mu
    return best, best_comp, best_mu, nfeas, 2 ** len(prs), max_inc


print("=" * 78)
print("V2  DISJUNCTIVE VALUE -- max over the 2^C(n,2) comparable/incomparable branches")
print("=" * 78)

for n in NS:
    base = F(n * (n - 1), 6)
    print(f"\n### n = {n}   baseline C(n,2)/3 = {base}   baseline eps_spec = {F(n, n + 1)}")
    for label, form in RUNS:
        best, comp, mu, nfeas, ntot, max_inc = disjunctive(n, form)
        if best is None:
            print(f"  {label:22s} EVERY BRANCH INFEASIBLE (0/{ntot})")
            continue
        es = eps_spec(n, best)
        print(f"  {label:22s} max E[inv] = {str(best):>8}   eps_spec = {str(es):>8}"
              f" = {float(es):.6f}   x baseline = {best / base}"
              f"   ({nfeas}/{ntot} branches feasible)")
        print(f"  {'':22s} conjecture check: (n-1)/3 = {F(n - 1, 3)}"
              f"   -> {'MATCH' if best == F(n - 1, 3) else 'DIFFERS'}"
              f"    2/(n+1) = {F(2, n + 1)} -> {'MATCH' if es == F(2, n + 1) else 'DIFFERS'}")
        print(f"  {'':22s} attained on comparable = "
              f"{sorted(comp) if comp else '{} (all pairs incomparable)'}"
              f"   [{'IS' if is_transitive(n, comp) else 'is NOT'} a partial order]")
        print(f"  {'':22s} incomparable there = {len(pairs_of(n)) - len(comp)};"
              f"  max incomparable over value>0 branches = {max_inc}  (n-1 = {n - 1})")
        rep = measure_report(n, mu)
        print(f"  {'':22s} witness: {len(mu)} atoms, mass {rep['mass']}, max flip {rep['max_flip']}")
        for p, w in sorted(mu.items(), key=lambda t: (-t[1], t[0])):
            print(f"  {'':24s} mass {str(w):>8}  perm {p}  inv={inv_count(p)}")
        # IS THE BOUND ATTAINED BY A REAL POSET?  One named poset, read off the LP's own
        # optimal branch -- no enumeration.
        if is_transitive(n, comp):
            pmu = uniform_le_measure(n, comp)
            pr = measure_report(n, pmu)
            inM = pr["max_flip"] <= F(1, 3)
            print(f"  {'':22s} REALISABILITY CONTROL: uniform L(P) of that very poset has"
                  f" |L(P)|={len(pmu)}, E[inv]={pr['E_inv']}, max flip={pr['max_flip']}"
                  f" ({'in M_n' if inM else 'NOT in M_n'})")
            print(f"  {'':22s}   -> bound {'ATTAINED BY A REAL POSET' if (inM and pr['E_inv'] == best) else 'NOT attained by that poset'}"
                  f"  (gap {best - pr['E_inv']})")
    sys.stdout.flush()
