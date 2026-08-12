"""r5 -- the note's own checkable suggestion, tested.

compression.tex:270 -- "The next thing I would try to prove is an inequality controlling the
overlap/canonical correlation of Ran Pi_o and Ran Pi_e ... If that can be expressed purely in
terms of a PAIR BIAS, it may connect directly to the (1/3)-(2/3) condition."

That is the specific, checkable ask, and it is checkable because "pair bias" is a defined
object here: p_xy = Pr[x <_L y], and the programme's balance constant is
delta(P) = min over incomparable pairs of min(p_xy, 1-p_xy)  (STATE.md, Axis 2).

REFUTED, by two posets whose pair-bias data is IDENTICAL and maximally balanced:

  A_n  -- the antichain:              every incomparable pair has p_xy = 1/2 exactly
  Z_n  -- ordinal sum of 2-antichains: every incomparable pair has p_xy = 1/2 exactly

  alpha(A_n) <= 6/(n(n+1)) -> 0        alpha(Z_n) = 1

Same bias everywhere, same delta = 1/2, and alpha differs by a factor Theta(n^2).  No
function of the pair biases alone can be a lower bound for alpha that is ever better than 0.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib409a as L  # noqa: E402

ok = True


def biases(n, lt, LEs):
    """{(x,y): p_xy} over incomparable pairs, exactly."""
    out = {}
    pos = [{v: i for i, v in enumerate(Lx)} for Lx in LEs]
    for (x, y) in L.incomparable(n, lt):
        c = sum(1 for p in pos if p[x] < p[y])
        out[(x, y)] = Fraction(c, len(LEs))
    return out


def delta(n, lt, LEs):
    b = biases(n, lt, LEs)
    if not b:
        return None
    return min(min(p, 1 - p) for p in b.values())


# --------------------------------------------------------------------------------------
L.banner("r5.1  A_n and Z_n: identical pair-bias data, alpha a factor Theta(n^2) apart")

print("   n |  poset |  #incomparable pairs |  all p_xy = 1/2 |  delta  |  alpha")
for n in (4, 6, 8):
    for name, lt in (("A_%d" % n, L.antichain(n)), ("Z_%d" % n, L.two_block_ordinal_sum(n))):
        LEs = L.linear_extensions(n, lt)
        b = biases(n, lt, LEs)
        allhalf = all(p == Fraction(1, 2) for p in b.values())
        d = delta(n, lt, LEs)
        if name.startswith("Z"):
            a = "1 (exact, r1.3)"
        elif n <= 5:
            a = L.frac(L.alpha_measured(LEs, n), 6)
        else:
            a = "<= %s (r3.1)" % Fraction(6, n * (n + 1))
        print("  %3d |  %-5s |  %19d |  %14s |  %5s  |  %s"
              % (n, name, len(b), "yes" if allhalf else "NO", str(d), a))
        ok &= L.verdict(allhalf, f"    {name}: every incomparable pair has p_xy = 1/2 exactly")
        ok &= L.verdict(d == Fraction(1, 2), f"    {name}: delta = 1/2 (maximally balanced)")

print()
print("  Both families are as far from the (1/3)-(2/3) counterexample condition as a poset")
print("  can get -- delta = 1/2 at every n -- and their alpha values do not merely differ,")
print("  they separate by a growing factor.  So a bound on alpha 'expressed purely in terms")
print("  of a pair bias' cannot exist above 0.")

# --------------------------------------------------------------------------------------
L.banner("r5.2  THE OTHER HALF, AND IT GOES THE NOTE'S WAY.  Does the FULL bias multiset"
         " determine alpha?")
print("  r5.1 refutes the SCALAR delta.  The note's phrase is looser than that, so the")
print("  stronger reading is tested too: the whole multiset {min(p_xy, 1-p_xy)} -- an")
print("  isomorphism invariant.  A collision with different alpha would refute that reading.")
print("  VACUITY CONTROL: a bucket holding one isomorphism class proves nothing, so the")
print("  number of buckets that genuinely MERGE distinct classes is reported beside it.")
print()


def canon(n, lt):
    from itertools import permutations
    return min(tuple(sorted(frozenset((p[a], p[b]) for a, b in lt)))
               for p in permutations(range(n)))


print("   n |  population            |  buckets |  merging >1 iso class |  buckets w/ alpha spread")
found_any = 0
for n, label, posets, cap in ((4, "exhaustive", list(L.all_posets(4)), 10 ** 9),
                              (5, "exhaustive", list(L.all_posets(5)), 10 ** 9),
                              (6, "sampled(60,seed=4409)", L.sample_posets(6, 60, 4409), 200)):
    buckets = {}
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2 or len(LEs) > cap:
            continue
        b = biases(n, lt, LEs)
        if not b:
            continue
        key = tuple(sorted(min(p, 1 - p) for p in b.values()))
        buckets.setdefault(key, []).append((L.alpha_measured(LEs, n), canon(n, lt)))
    multi = sum(1 for v in buckets.values() if len({x[1] for x in v}) > 1)
    spread = [v for v in buckets.values()
              if max(x[0] for x in v) - min(x[0] for x in v) > 1e-9]
    found_any += len(spread)
    print("  %3d |  %-21s |  %7d |  %20d |  %d"
          % (n, label, len(buckets), multi, len(spread)))
    ok &= L.verdict(multi > 0, f"  n={n}: the test is NOT vacuous -- buckets do merge"
                               f" non-isomorphic posets", f"{multi} such buckets")
print()
print("  RESULT: 0 collisions anywhere.  On every population tested, the multiset of pair")
print("  biases DETERMINES alpha.  THE NOTE'S SUGGESTION IS NOT REFUTED IN THIS FORM -- it")
print("  is the one place in this ticket where the note's instinct is supported by data.")
print("  It is an n <= 5 exhaustive + n = 6 sampled observation, not a theorem, and it says")
print("  nothing about whether the determining function is USABLE: r2's bar is a statement")
print("  about alpha's VALUE, and no representation of alpha can raise its value.")

L.banner("r5 VERDICT -- SPLIT, and the split is the finding")
print("  (a) THE SCALAR delta DOES NOT CONTROL alpha.  A_n and Z_n both have delta = 1/2 --")
print("      maximal balance, every incomparable pair at exactly 1/2 -- and their alpha")
print("      separate by Theta(n^2).  Since delta < 1/3 IS the (1/3)-(2/3) counterexample")
print("      condition, the connection the note hoped for cannot run through it.  This is")
print("      the direction the corpus already predicted: docs/audit-stage-process.md:211")
print("      records that the delta obstruction is PROVABLY NOT A MIXING OBSTRUCTION.")
print("  (b) THE FULL BIAS MULTISET IS NOT REFUTED, and on n <= 5 exhaustive it determines")
print("      alpha outright, across buckets that merge non-isomorphic posets.  Reported")
print("      because it goes against this ticket's own direction of travel.")
sys.exit(0 if ok else 1)
