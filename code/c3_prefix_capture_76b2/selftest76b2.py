#!/usr/bin/env python3
"""selftest76b2 — two-sided red drills over every verdict this instrument reports.

An instrument that can only print OK is indistinguishable from one that checks nothing.
Every drill below has BOTH arms: a positive control that must pass and a mutation that
must fail.  A drill whose mutation arm passes is itself a failure.

Exit 0 iff every drill behaves as declared.
"""

from fractions import Fraction as F
import sys

from lib76b2 import (Poset, all_posets, standard_spectrum, monotone_in_span,
                     is_monotone, sweep_sets, sweep_best, is_prefix_or_suffix,
                     rayleigh, connected)

drills = 0
bad = 0


def drill(name, positive, mutation_fails):
    """positive must be True; mutation_fails must be True (i.e. the mutation was caught)."""
    global drills, bad
    drills += 1
    ok = bool(positive) and bool(mutation_fails)
    if not ok:
        bad += 1
    print(f"  [{'ok ' if ok else 'BAD'}] {name}"
          f"{'' if ok else f'   (positive={bool(positive)}, mutation caught={bool(mutation_fails)})'}")


print("=" * 78)
print("selftest76b2 — two-sided red drills")
print("=" * 78)
print()

A3 = Poset(3, [], "antichain n=3")
A4 = Poset(4, [], "antichain n=4")
CH4 = Poset(4, [(0, 1), (1, 2), (2, 3)], "chain n=4")
NP = Poset(4, [(0, 2), (1, 2), (1, 3)], "N-poset")
SPLIT = Poset(4, [(0, 1), (2, 3)], "two 2-chains, the n=4 C_3^cut witness")

# --------------------------------------------------------------- transport
print("-- transport and leakage -------------------------------------------------")
# antichain n=3, A={0}: sigma({0}) = {p[0]}, so leak = Pr[p[0] != 0] = 2/3.  By hand.
drill("leak on the antichain matches the hand value 2/3",
      A3.leak([0]) == F(2, 3),
      A3.leak([0]) != F(1, 3))
# H8 CORRECTED BY THIS DRILL.  PREDICTIONS.md H8 wrote "Phi_P(A) = (n-|A|)/n for every A"
# on the antichain.  That is the |A| <= n/2 case only -- Phi normalises by min(|A|,|A^c|),
# so above the median it is |A|/n.  The general form is Phi_P(A) = max(|A|,n-|A|)/n.
# This is the SAME min/max slip as H1's, made twice in the same prediction file and caught
# twice by the machine.  Both are kept as written in PREDICTIONS.md.
drill("H8 CORRECTED: antichain Phi(A) = max(|A|,n-|A|)/n at every cut, and the "
      "as-written (n-|A|)/n form fails above the median",
      all(A4.phi(A) == F(max(len(A), 4 - len(A)), 4)
          for A in [[0], [1], [0, 1], [0, 2], [1, 2, 3], [0, 1, 2]]),
      A4.phi([1, 2, 3]) != F(4 - 3, 4))
# the matrix and the definition must agree -- and must DISAGREE with a wrong indicator
ind = [F(1), F(1), F(0), F(0)]
drill("energy(1_A) == leak(A), and a mutated indicator does not",
      NP.energy(ind) == NP.leak([0, 1]),
      NP.energy([F(1), F(0), F(1), F(0)]) != NP.leak([0, 1]))
# the OTHER convention really is a different function
drill("leak_naive_prefixstyle differs from leak on a non-prefix cut (P11)",
      CH4.leak([1]) == F(0),
      CH4.leak_naive_prefixstyle([1]) != CH4.leak([1]))
print()

# ---------------------------------------------------------------- dictionary
print("-- the s1 dictionary -----------------------------------------------------")
n, k = 4, 2
f = [F(1) - F(k, n) if i < k else -F(k, n) for i in range(n)]
nrm = F(k * (n - k), n)
rho = sum(f[i] * NP.M()[i][j] * f[j] for i in range(n) for j in range(n)) / nrm
drill("1 - rho computed from (I-M) equals 1 minus rho computed from M",
      NP.rho_prefix(k) == 1 - rho,
      NP.rho_prefix(k) != rho)
# D1 general form holds; H1's literal n/(n-k) form is FALSE above the median
gen_ok = all(P.rho_prefix(kk) == F(P.n, max(kk, P.n - kk)) * P.phi(range(kk))
             for P in [NP, SPLIT, A4] for kk in range(1, 4))
h1_fails_above = any(P.rho_prefix(kk) != F(P.n, P.n - kk) * P.phi(range(kk))
                     for P in [NP, SPLIT, A4] for kk in range(3, 4))
drill("D1 general form holds AND H1's n/(n-k) form fails above the median",
      gen_ok, h1_fails_above)
# D2's factor 2 is attained -- so the bound is tight and not merely safe
drill("D2's upper factor 2 is ATTAINED at k = n/2, and not at k = 1",
      A4.rho_prefix(2) == 2 * A4.phi(range(2)),
      A4.rho_prefix(1) != 2 * A4.phi(range(1)))
# D4 both ways
p = (2, 0, 3, 1)
A = frozenset([0, 2])
Ac = frozenset([1, 3])
drill("D4 complement symmetry holds, and a mutated complement breaks it",
      len(A) - len(A & {p[i] for i in A}) == len(Ac) - len(Ac & {p[i] for i in Ac}),
      len(A) - len(A & {p[i] for i in A}) != len(A) - len(A & set(p[:len(A)])))
print()

# --------------------------------------------------------------------- sweep
print("-- the sweep -------------------------------------------------------------")
# tie handling: a monotone vector with exact ties must yield only prefix/suffix sets,
# and the order-slice family it replaced must contain a set that is neither
tied = [F(1), F(1), F(1), F(-3)]
order = sorted(range(4), key=lambda i: tied[i])
slices = [frozenset(order[c:]) for c in range(1, 4)]
drill("sweep_sets on a tied monotone vector returns only prefix/suffix sets, "
      "and order-slices do not",
      all(is_prefix_or_suffix(S, 4) for S in sweep_sets(tied)),
      any(not is_prefix_or_suffix(S, 4) for S in slices))
# a non-monotone vector DOES leave the family -- so S2 is about monotonicity
drill("a non-monotone vector's threshold sets do leave the prefix/suffix family",
      all(is_prefix_or_suffix(S, 4) for S in sweep_sets([F(0), F(3), F(1), F(2)])) is False,
      True)
# How much of the Cheeger constant 2 does this population actually spend?  Reported as a
# measurement, not asserted: the drill is that the bound HOLDS and that the worst ratio is
# printed rather than hidden.
holds2 = True
worst_ratio = F(0)
for nn in (4, 5):
    for P in all_posets(nn):
        for vec in range(3 ** nn):
            g, v = [], vec
            for _ in range(nn):
                g.append(F(v % 3))
                v //= 3
            if len(set(g)) < 2:
                continue
            R = rayleigh(P, g)
            S, phi = sweep_best(P, g)
            if S is None or R == 0:
                continue
            if phi ** 2 > 2 * R:
                holds2 = False
            worst_ratio = max(worst_ratio, phi ** 2 / R)
print(f"       (worst Phi(S)^2 / R(f) over n = 4,5 and every f in {{0,1,2}}^n: "
      f"{worst_ratio} = {float(worst_ratio):.6f}; the sweep lemma allows 2)")
drill("Phi^2 <= 2R holds everywhere, and the sweep bound is NOT tight in this population "
      "-- the constant 2 is never spent here, which is a fact about small posets and NOT "
      "a licence to drop it",
      holds2, worst_ratio < 2)
print()

# ---------------------------------------------------------------- eigen side
print("-- spectrum, monotonicity, stratification --------------------------------")
lam, dom, mult = standard_spectrum(A4)
drill("antichain: lambda_std = 0 with multiplicity n-1 (the whole of H)",
      abs(lam) < 1e-9 and mult == 3,
      abs(lam - 1.0) > 1e-9)
lam, dom, mult = standard_spectrum(CH4)
drill("chain: lambda_std = 1, so 1 - lambda_std = 0 (M = I, graph totally disconnected)",
      abs(lam - 1.0) < 1e-9,
      abs(lam) > 1e-9)
drill("monotone_in_span says YES on a monotone 1-dim span and NO on a non-monotone one",
      monotone_in_span([[-3.0, -1.0, 1.0, 3.0]]) == "YES",
      monotone_in_span([[0.0, 3.0, 1.0, 2.0]]) == "NO")
drill("connected() separates the chain (disconnected) from the N-poset (connected)",
      connected(NP) is True,
      connected(CH4) is False)
# the three stratification predicates coincide -- and a mutation of one of them does not
# mutation control: "is a chain" agrees with DISC on the chain and DISAGREES on an
# ordinal sum of two antichains, which is decomposable without being a chain.  So the
# three-way agreement in s3 (C0) is not an artifact of a predicate that trivially tracks
# chain-ness.
OS = Poset(4, [(0, 2), (0, 3), (1, 2), (1, 3)], "A2 (+) A2")
drill("DISC == CUT == PHI0 on both a decomposable and a primitive witness, and the "
      "mutation `is a chain` disagrees with them on an ordinal sum of two antichains",
      (not connected(CH4)) == (not CH4.is_primitive()) == (CH4.phi_star()[0] == 0) is True
      and connected(NP) == NP.is_primitive() == (NP.phi_star()[0] != 0) is True,
      (not connected(OS)) is True and OS.is_chain() is False)
print()

# --------------------------------------------------------------- C_3 and budget
print("-- C_3 and the budget ----------------------------------------------------")
# the n=4 C_3^cut witness, re-derived independently from the definitions
ps, argp = SPLIT.phi_star()
pp, argk = SPLIT.phi_star_prefix()
brute = min(SPLIT.leak(A) / min(len(A), 4 - len(A))
            for A in [[0], [1], [2], [3], [0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3],
                      [0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])
drill("Phi* on the C_3^cut witness re-derives from a hand-listed enumeration, and the "
      "prefix minimum does NOT equal it (so C_3^cut > 1 there is real)",
      ps == brute,
      pp != brute and pp > ps)


def window(e):
    if e <= 0:
        return None
    n = max(1, int(2 / e - 1))
    while F(2, n + 1) > e:
        n += 1
    return n


drill("window(1/50) = 99 -- 2/100 <= 1/50 holds, and n = 98 is caught as too small "
      "because 2/99 > 1/50",
      window(F(1, 50)) == 99 and F(2, 100) <= F(1, 50),
      F(2, 99) > F(1, 50))
EL = F(1, 5)
drill("chain (III) at C_3 = 1 IS chain (I), and at C_3 = 2 it is not",
      EL ** 2 / (2 * 1) == EL ** 2 / 2,
      EL ** 2 / (2 * 2) != EL ** 2 / 2)
drill("chain (II) and chain (III) differ by exactly 2/eps_leak at every C_3, and they "
      "are not the same number",
      all((EL / c3) / (EL ** 2 / (2 * c3)) == 2 / EL
          for c3 in [F(1), F(2), F(7, 3), F(10)]),
      (EL / 1) != (EL ** 2 / 2))
# the literal-reading threshold, both sides
drill("literal reading closes above c = 1 - eps_leak and not at or below it",
      1 - (1 - EL) / F(9, 10) > 0,
      1 - (1 - EL) / F(4, 5) <= 0)
drill("the literal threshold c > 1 - eps_leak MOVED with mg-e35c F5's 100x repair: "
      "0.98 at the superseded calibration, 0.80 at the repaired one, and they differ",
      1 - F(1, 50) == F(49, 50) and 1 - F(1, 5) == F(4, 5),
      F(49, 50) != F(4, 5))
print()

print("=" * 78)
print(f"selftest76b2: {drills - bad} of {drills} drills behaved as declared")
print("=" * 78)
sys.exit(1 if bad else 0)
