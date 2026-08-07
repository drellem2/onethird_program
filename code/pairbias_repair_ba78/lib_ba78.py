"""mg-ba78 -- the repair library for mg-6bc2's SECTION 5 adjacency diagnostics.

WHAT IS WRONG UPSTREAM, stated so this file cannot be read as a rewrite.

mg-6bc2's LP (code/pairbias_sharpening_6bc2/lp6bc2.py) is correct AS AN LP: it
maximises E[objective] over measures on S_n with every pair-flip probability
<= 1/3.  Its OPTIMUM VALUE is right, its theorem is right, and mg-200d
reproduced that theorem exactly at n = 3,4,5,6 on an independent two-phase
solver.  NOTHING HERE TOUCHES IT.

Two things downstream of the optimum are wrong.

DEFECT 1 -- SUB-PROBABILITY MEASURES.  The LP's normalisation constraint is
`sum mu <= 1`, an INEQUALITY, because the standard form it uses (Ax <= b, x >= 0,
b >= 0) needs the origin to be feasible so that phase 1 can be skipped.  The
objectives (inversions, footrule) both vanish at the identity, so the simplex has
no reason to place the leftover mass anywhere, and returns a SUB-probability
measure.  At n = 3 the returned support carries total mass 2/3.  The optimum
value is unaffected -- completing the measure on the identity adds 0 to E[inv],
0 to E[F], and 0 to every pair's flip probability, so the completion is feasible
with the same objective, which is exactly why the theorem survives.  But the
ADJACENCY DIAGNOSTICS are not linear functionals of the measure; they are
equality tests between two masses, and a missing 1/3 changes their answers.

DEFECT 2 -- TWO COLUMNS, TWO UNITS.  `measure_stats` builds `adj` keyed by
ORDERED adjacent pairs and then filters that dict, so a violated unordered pair
{x,y} is counted once or twice depending on whether both directions happen to
occur with positive mass.  `per_slot_violations` iterates x < y, i.e. UNORDERED
pairs, crossed with slots.  The two columns of mg-6bc2's section 5 table are
therefore in different units and "6 vs 8" at n = 4 is not a comparison.

THE REPAIR.  Complete every measure to a probability measure before diagnosing,
and report every count on UNORDERED pairs, with the (pair, slot) count kept as a
separate, explicitly labelled column.  On that unit the two diagnostics NEST --
aggregate-violated pairs are a subset of per-slot-violated pairs, because
sum_k J_k(x,y) != sum_k J_k(y,x) forces some slot to differ -- so the comparison
means something and the inclusion is checked below rather than assumed.
"""

import os
import sys
from fractions import Fraction as F
from itertools import permutations

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "..", "pairbias_sharpening_6bc2"),
)

from lp6bc2 import (  # noqa: E402
    inv_count, footrule, flipped_pairs, simplex_max, two_atom,
)


# --------------------------------------------------------- the LP, AS PUBLISHED
#
# Assembled here rather than imported, deliberately.  mg-ba78 also repairs
# lp6bc2.relaxation_lp in place, so importing it would make the "as published"
# arm below depend on whether that repair is present -- and this file's whole
# job is to show the difference between the two.  What IS imported is the part
# that was never in doubt: the exact simplex, and the combinatorial primitives.
# The constraint block is mg-6bc2's, transcribed with its `sum mu <= 1`.

def lp_as_published(n, objective, cap=F(1, 3)):
    """mg-6bc2's relaxation LP with its original `sum mu <= 1` normalisation.

    Returns (optimum, support) with the support NOT completed -- i.e. exactly
    what its section 5 diagnostics were computed on.
    """
    perms = list(permutations(range(n)))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    pidx = {p: k for k, p in enumerate(pairs)}

    rows = [[F(0)] * len(perms) for _ in pairs]
    for col, p in enumerate(perms):
        for q in flipped_pairs(p):
            rows[pidx[q]][col] = F(1)
    A = list(rows) + [[F(1)] * len(perms)]
    b = [cap] * len(pairs) + [F(1)]

    c = [F(objective(p)) for p in perms]
    val, x = simplex_max(A, b, c)
    return val, {perms[k]: x[k] for k in range(len(perms)) if x[k] != 0}


# ------------------------------------------------------------------ completion

def total_mass(mu):
    return sum(mu.values(), F(0))


def complete(n, mu):
    """Return mu with the missing mass placed on the identity.

    The identity has inv = 0, footrule = 0, and flips no pair, so this adds
    nothing to either objective and nothing to any flip probability.  Hence:
    feasible in, feasible out; same objective value; total mass exactly 1.
    Callers that want to know whether anything moved should compare
    total_mass(mu) against 1 BEFORE calling this.
    """
    deficit = F(1) - total_mass(mu)
    if deficit < 0:
        raise ValueError(f"mass {total_mass(mu)} exceeds 1 -- not a sub-probability measure")
    out = dict(mu)
    if deficit > 0:
        ident = tuple(range(n))
        out[ident] = out.get(ident, F(0)) + deficit
    return out


def max_flip_prob(n, mu):
    q = {(i, j): F(0) for i in range(n) for j in range(i + 1, n)}
    for p, w in mu.items():
        for pr in flipped_pairs(p):
            q[pr] += w
    return max(q.values())


def expect(mu, f):
    return sum(w * f(p) for p, w in mu.items())


# ------------------------------------------------- diagnostics, one unit each

def slot_masses(n, mu):
    """J[(x, y, k)] = mass of measures placing x immediately before y at slot k."""
    J = {}
    for p, w in mu.items():
        for k in range(n - 1):
            key = (p[k], p[k + 1], k)
            J[key] = J.get(key, F(0)) + w
    return J


def aggregate_masses(n, mu):
    """A[(x, y)] = sum_k J[(x, y, k)] -- the AGGREGATE adjacency mass."""
    A = {}
    for (x, y, _k), w in slot_masses(n, mu).items():
        A[(x, y)] = A.get((x, y), F(0)) + w
    return A


def aggregate_violated_pairs(n, mu):
    """UNORDERED pairs {x<y} with A(x,y) != A(y,x).  Sorted, so it is a set."""
    A = aggregate_masses(n, mu)
    return sorted((x, y) for x in range(n) for y in range(x + 1, n)
                  if A.get((x, y), F(0)) != A.get((y, x), F(0)))


def per_slot_violated_pair_slots(n, mu):
    """((x<y), k) with J_k(x,y) != J_k(y,x) -- the FINER unit, kept separate."""
    J = slot_masses(n, mu)
    return sorted(((x, y), k)
                  for x in range(n) for y in range(x + 1, n)
                  for k in range(n - 1)
                  if J.get((x, y, k), F(0)) != J.get((y, x, k), F(0)))


def per_slot_violated_pairs(n, mu):
    """UNORDERED pairs violated at AT LEAST ONE slot -- comparable to aggregate."""
    return sorted({pr for pr, _k in per_slot_violated_pair_slots(n, mu)})


# ------------------------------------------------------- mg-6bc2's own predicate

def published_aggregate_count(n, mu):
    """mg-6bc2's `measure_stats` asym, reproduced exactly, defects included.

    Iterates the ORDERED keys of the adjacency dict, so it counts a violated
    unordered pair twice when both directions carry mass and once when only one
    does.  Present so the published numbers can be reproduced rather than
    asserted, and so the repaired ones can be shown to differ for a stated reason.
    """
    A = aggregate_masses(n, mu)
    return len([(x, y) for (x, y) in A if A.get((x, y), F(0)) != A.get((y, x), F(0))])


# --------------------------------------------------------------------- drivers

OBJECTIVES = (("E[inv_e]", inv_count), ("E[footrule]", footrule))


def row(n, objective):
    """Everything section 5 needs for one (n, objective), published and repaired."""
    val, raw = lp_as_published(n, objective)
    done = complete(n, raw)
    return {
        "n": n,
        "opt": val,
        "mass_raw": total_mass(raw),
        "mass_done": total_mass(done),
        "support_raw": len(raw),
        "support_done": len(done),
        # the theorem's quantities, before and after completion
        "E_inv_raw": expect(raw, inv_count),
        "E_inv_done": expect(done, inv_count),
        "E_F_raw": expect(raw, footrule),
        "E_F_done": expect(done, footrule),
        "maxflip_done": max_flip_prob(n, done),
        # published numbers: mg-6bc2's predicate on the UNcompleted measure
        "pub_aggregate": published_aggregate_count(n, raw),
        "pub_per_slot": len(per_slot_violated_pair_slots(n, raw)),
        # repaired numbers: one unit, completed measure
        "agg_pairs": len(aggregate_violated_pairs(n, done)),
        "ps_pairs": len(per_slot_violated_pairs(n, done)),
        "ps_pair_slots": len(per_slot_violated_pair_slots(n, done)),
        "n_pairs": n * (n - 1) // 2,
        "n_pair_slots": n * (n - 1) // 2 * (n - 1),
        "nested": set(aggregate_violated_pairs(n, done))
                  <= set(per_slot_violated_pairs(n, done)),
        "raw": raw,
        "done": done,
    }
