"""e4 -- the one candidate that is the RIGHT SHAPE: adjacency.

The identity emits adjacency probabilities (e1), and the programme has exactly one line that
consumes adjacency facts.  STATE.md:158, mg-92e6:

    "pins the exact marginal-only ceiling (max-flow), which dies as the pair spreads -- the
     extra juice is ONE JOINT FACT (adjacency symmetry J(k,k+1) = J(k+1,k))"

and that one joint fact is what mg-200d -> mg-131e -> mg-00a1 spent an arc on.  So this arm
asks three questions in order, and the order matters:

  (e4.1)  Is the symmetry true?                       -> yes, at every poset and every slot.
  (e4.2)  Does it NEED the identity?                  -> no.  It is one involution.
  (e4.3)  Is what the identity emits even as strong?  -> no.  The identity emits the
          PARITY-AGGREGATED adjacency A^o, A^e = sums of J over slots of one parity.  The
          per-slot J's are strictly finer, and it is the per-slot form the arc consumed.

Test 3 (connected to (1/3)-(2/3)) is then answered by the record and NOT re-measured here:
mg-00a1 refuted the rate -- per-slot adjacency symmetry buys a constant factor of at most 6,
the disjunctive per-slot value is Theta(n^2), and STATE.md:169 records the route as DEAD, not
re-based.  That is read from the ledger, not reproduced.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib145f as L  # noqa: E402

ok = True

POP = ([(3, p) for p in L.all_posets(3)]
       + [(4, p) for p in L.all_posets(4)]
       + [(5, p) for p in L.sample_posets(5, 50, 41)]
       + [(6, p) for p in L.sample_posets(6, 25, 43)])


def per_slot_J(n, LEs):
    """J[k][(x,y)] = Pr[pos(x) = k and pos(y) = k+1].  ORDERED in (x, y)."""
    N = len(LEs)
    J = [dict() for _ in range(n - 1)]
    for Lx in LEs:
        for k in range(n - 1):
            key = (Lx[k], Lx[k + 1])
            J[k][key] = J[k].get(key, Fraction(0)) + Fraction(1, N)
    return J


# ---------------------------------------------------------------------------------------
L.banner("e4.1  per-slot adjacency symmetry J_k(x,y) = J_k(y,x) for incomparable x, y")
bad = 0
checked = 0
for (n, lt) in POP:
    LEs = L.linear_extensions(n, lt)
    J = per_slot_J(n, LEs)
    for (x, y) in L.incomparable_pairs(n, lt):
        for k in range(n - 1):
            a = J[k].get((x, y), Fraction(0))
            b = J[k].get((y, x), Fraction(0))
            bad += (a != b)
            checked += 1
ok &= L.verdict(bad == 0, "J_k(x,y) = J_k(y,x) at every (poset, incomparable pair, slot)",
                f"{bad} failures / {checked}")

# ---------------------------------------------------------------------------------------
L.banner("e4.2  it needs ONE INVOLUTION, not a foliation")
print("  tau_k is a fixed-point-free involution on {L : {L_k, L_k+1} = {x,y}} and it carries")
print("  the event {x at k, y at k+1} bijectively onto {y at k, x at k+1}.  Verified as a")
print("  BIJECTION rather than inferred from the equal counts, so this is not e4.1 twice.")
bad = 0
checked = 0
for (n, lt) in POP[:100]:
    LEs = L.linear_extensions(n, lt)
    S = set(LEs)
    for (x, y) in L.incomparable_pairs(n, lt):
        for k in range(n - 1):
            fwd = [Lx for Lx in LEs if Lx[k] == x and Lx[k + 1] == y]
            rev = {Lx for Lx in LEs if Lx[k] == y and Lx[k + 1] == x}
            img = set()
            for Lx in fwd:
                assert L.swap_legal(Lx, k, lt)
                M = L.adj_swap(Lx, k)
                if M not in S:
                    bad += 1
                img.add(M)
            if img != rev:
                bad += 1
            checked += 1
ok &= L.verdict(bad == 0, "tau_k is a bijection between the two events", f"{bad} / {checked}")
print("  No block system, fiber, projection or cube appears anywhere in this check.")

# ---------------------------------------------------------------------------------------
L.banner("e4.3  what the identity emits is STRICTLY COARSER than the per-slot data")
print("  A^o_xy = sum over ODD-parity slots k of (J_k(x,y) + J_k(y,x)), and likewise A^e.")
print("  So the identity's output is the per-slot data aggregated into two parity buckets.")
bad = 0
for (n, lt) in POP:
    LEs = L.linear_extensions(n, lt)
    J = per_slot_J(n, LEs)
    A_o, A_e = L.adjacency_probs(n, lt, LEs)
    so = set(L.block_starts(L.odd_blocks(n)))
    se = set(L.block_starts(L.even_blocks(n)))
    for (x, y) in L.incomparable_pairs(n, lt):
        so_sum = sum(J[k].get((x, y), 0) + J[k].get((y, x), 0) for k in so)
        se_sum = sum(J[k].get((x, y), 0) + J[k].get((y, x), 0) for k in se)
        bad += (so_sum != A_o[(x, y)]) + (se_sum != A_e[(x, y)])
ok &= L.verdict(bad == 0, "A^o and A^e ARE the parity-aggregated per-slot adjacencies",
                f"{bad} mismatches")

print()
print("  STRICTNESS, demonstrated directly rather than by a collision search.  A^o_xy is a")
print("  SUM of the symmetrized per-slot adjacencies S_k(x,y) = J_k(x,y) + J_k(y,x) over the")
print("  odd-parity slots.  Wherever two or more of those summands are nonzero, A^o_xy does")
print("  not determine them, so the aggregation is a genuine loss and not a relabelling.")
print()
print(f"  {'n':>3} {'pairs with >=2 nonzero summands in ONE parity class':>54} {'of':>6}")
strict_total = strict_pairs = 0
for (n, lt) in POP:
    LEs = L.linear_extensions(n, lt)
    J = per_slot_J(n, LEs)
    so = sorted(L.block_starts(L.odd_blocks(n)))
    se = sorted(L.block_starts(L.even_blocks(n)))
    for (x, y) in L.incomparable_pairs(n, lt):
        strict_total += 1
        for cls in (so, se):
            nz = sum(1 for k in cls
                     if J[k].get((x, y), 0) + J[k].get((y, x), 0) != 0)
            if nz >= 2:
                strict_pairs += 1
                break
ok &= L.verdict(strict_pairs > 0,
                "the parity aggregation collapses >= 2 nonzero per-slot summands",
                f"{strict_pairs} of {strict_total} incomparable pairs in the population")

# ---------------------------------------------------------------------------------------
L.banner("e4.4  the consumer, read from the ledger and NOT re-measured")
print("""  STATE.md:169 (mg-200d -> mg-131e -> mg-00a1), verbatim in substance:

    * mg-200d's headline -- per-slot adjacency symmetry takes the relaxation value from
      Theta(n^2) down to Theta(n) -- is REFUTED (mg-00a1).  The disjunctive per-slot value
      is Theta(n^2), SUPERLINEAR, pinned n(n+5)/36 <= max <= n(n-1)/6.
    * "PER-SLOT ADJACENCY SYMMETRY BUYS A CONSTANT FACTOR OF AT MOST 6, NOT AN ORDER."
    * "THE ROUTE IS DEAD, NOT RE-BASED -- there is NO c to substitute for 1/3."
    * and the branch-free form J_k(y,x) <= J_k(x,y) "buys exactly NOTHING": value C(n,2)/3
      unchanged at n = 3,4,5,6.

  So the one adjacency-shaped consumer in the programme is refuted, and it was refuted
  against a STRONGER input than this identity emits (per-slot, not parity-aggregated).""")

L.banner("e4  RESULT")
print("  ok" if ok else "  NOT ok")
sys.exit(0 if ok else 1)
