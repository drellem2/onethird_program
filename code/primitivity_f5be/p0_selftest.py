"""p0 -- SELF-TEST AND CONTROLS.  Nothing downstream is worth reading until this is green.

Every arm below is here because a specific way of being silently wrong was identified in
PREDICTIONS.md's error list, and each control is checked to FIRE on a planted defect as well
as to pass on the real object.  A control that cannot fail is not a control (mg-409a D1).
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libf5be as F  # noqa: E402
import lib409a as L  # noqa: E402

ok = True

# --------------------------------------------------------------------------------------
F.banner("p0.1  POSITIVE CONTROL ON THE ENUMERATION -- the iso-class count sequence (E5)")

# OEIS A000112: posets on n unlabeled points.
KNOWN = {0: 1, 1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318}
for n in range(0, 7):
    got = len(F.posets_up_to_iso(n))
    ok &= F.verdict(got == KNOWN[n], f"n={n}: {got} iso classes", f"(expected {KNOWN[n]})")

# and the labeled count, cross-checked against lib409a's independent brute-force generator
# A001035: labeled posets 1, 3, 19, 219, 4231
LAB = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231}
for n in (1, 2, 3, 4, 5):
    got = len(list(L.all_posets(n)))
    ok &= F.verdict(got == LAB[n], f"n={n}: {got} LABELED posets (lib409a generator)",
                    f"(expected {LAB[n]})")

print("""
  Both sequences are the standard ones and neither generator has seen the other: mine
  augments by a maximal element and dedups by brute-force canonical form; lib409a's filters
  3^C(n,2) relation-assignments.  Agreement at n <= 5 on the labeled count and the known
  unlabeled sequence to n = 6 is the warrant for calling n <= 6 EXHAUSTIVE below.""")

# --------------------------------------------------------------------------------------
F.banner("p0.2  NEGATIVE CONTROL ON THE ENUMERATION -- a broken augmentation must be caught")

# Plant E5: augment only over ANTICHAIN down-sets instead of all down-sets.  This must
# undercount, and the control must notice.
def broken_posets(n):
    if n == 0:
        return [frozenset()]
    smaller = broken_posets(n - 1)
    seen, out = set(), []
    for lt in smaller:
        for S in F.down_sets(n - 1, lt):
            if any((a, b) in lt for a in S for b in S):   # skip non-antichain down-sets
                continue
            rel = set(lt) | {(v, n - 1) for v in S}
            key = F.canonical(n, rel)
            if key in seen:
                continue
            seen.add(key)
            out.append(frozenset(rel))
    return out

bad4 = len(broken_posets(4))
ok &= F.verdict(bad4 != KNOWN[4], f"planted defect UNDERCOUNTS at n=4: {bad4} != 16",
                "control FIRES")

# --------------------------------------------------------------------------------------
F.banner("p0.3  PRIMITIVITY -- named posets, checked against what the literature says")

def mk(n, pairs):
    return L.close_rel(n, set(pairs))

CASES = [
    ("A_2  (2-antichain)",        2, [],                                   True,  None),
    ("C_2  (2-chain)",            2, [(0, 1)],                             True,  None),
    ("A_3  (3-antichain)",        3, [],                                   False, None),
    ("V    (0<1, 0<2)",           3, [(0, 1), (0, 2)],                     False, None),
    ("N    (0<2, 1<2, 1<3)",      4, [(0, 2), (1, 2), (1, 3)],             True,  None),
    ("A_4",                       4, [],                                   False, None),
    ("Z_4  (ordinal sum 2+2)",    4, [(0, 2), (0, 3), (1, 2), (1, 3)],     False, None),
    ("C_4  (4-chain)",            4, [(0, 1), (1, 2), (2, 3)],             False, None),
]
for name, n, prs, want_prime, _ in CASES:
    lt = mk(n, prs)
    got = F.is_prime(n, lt)
    ok &= F.verdict(got == want_prime, f"{name:28s} prime={got}", f"(expected {want_prime})")

print("""
  The N-poset is THE standard smallest primitive poset and it is the reason primitivity is
  only interesting from n = 4: on n = 3 every poset has a nontrivial module (p0.3 checks
  A_3 and V explicitly).  n <= 2 is vacuously prime by the definition's own range and is
  reported as such rather than special-cased away.""")

# no prime poset on exactly 3 elements
n3 = [lt for lt in F.posets_up_to_iso(3) if F.is_prime(3, lt)]
ok &= F.verdict(len(n3) == 0, f"no prime poset on n=3: {len(n3)} found")

# --------------------------------------------------------------------------------------
F.banner("p0.4  alpha -- the EXACT `==1` test and the float power iteration, cross-checked")

# lib409a's Jacobi is the reference.  Agreement at every n <= 4 iso class, plus n = 5.
worst = 0.0
tested = 0
for n in (2, 3, 4, 5):
    for lt in F.posets_up_to_iso(n):
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        a_ref = L.alpha_measured(LEs, n)
        a_pow = F.alpha_power(LEs, n)
        worst = max(worst, abs(a_ref - a_pow))
        tested += 1
ok &= F.verdict(worst < 1e-8, f"power iteration vs lib409a Jacobi at {tested} posets",
                f"worst |diff| = {worst:.3e}")

# The EXACT test must agree with the float at every poset, in both directions.
mismatch = []
for n in (2, 3, 4, 5):
    for lt in F.posets_up_to_iso(n):
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        exact_one, _w = F.alpha_is_one_exact(LEs, n)
        a = F.alpha_power(LEs, n)
        if exact_one != (abs(a - 1.0) < 1e-7):
            mismatch.append((n, sorted(lt), exact_one, a))
ok &= F.verdict(not mismatch, f"EXACT alpha==1 test agrees with the float at every n<=5 poset",
                f"{len(mismatch)} mismatches")
for m in mismatch[:5]:
    print("      MISMATCH", m)

# --------------------------------------------------------------------------------------
F.banner("p0.5  NEGATIVE CONTROL on the exact test -- it must be able to say NO")

# Z_4 must come back True; the antichain A_4 must come back False.  If both came back the
# same way the test is a constant function and everything downstream is vacuous.
z4 = L.two_block_ordinal_sum(4)
LEz = L.linear_extensions(4, z4)
a4 = frozenset()
LEa = L.linear_extensions(4, a4)
tz, _ = F.alpha_is_one_exact(LEz, 4)
ta, wit = F.alpha_is_one_exact(LEa, 4)
ok &= F.verdict(tz is True, "Z_4: exact test says alpha == 1", "(mg-409a r1.3 agrees)")
ok &= F.verdict(ta is False, "A_4: exact test says alpha != 1", f"witness {wit[2]} != 0")
print(f"      measured: alpha(Z_4) = {F.frac(F.alpha_power(LEz, 4))}   "
      f"alpha(A_4) = {F.frac(F.alpha_power(LEa, 4))}   (mg-409a section 4: 6/(n(n+1)) = 0.3)")

# --------------------------------------------------------------------------------------
F.banner("p0.6  delta / mu -- E1 and E6, both planted")

# E6: a chain has NO incomparable pair, so delta and mu are maxima/minima over the empty
# set.  They must RAISE, not return a number that prints like a measurement.
chain = mk(3, [(0, 1), (1, 2)])
LEc = L.linear_extensions(3, chain)
st = F.all_pair_stats(3, chain, LEc)
raised = False
try:
    F.delta_of(st)
except ValueError:
    raised = True
ok &= F.verdict(raised, "delta on a 3-chain RAISES rather than returning 0", "(E6 control)")

# E1: delta and mu must actually differ somewhere, or I have written the same function twice.
diff_found = None
for lt in F.posets_up_to_iso(5):
    LEs = L.linear_extensions(5, lt)
    if len(LEs) < 2:
        continue
    st = F.all_pair_stats(5, lt, LEs)
    if not st:
        continue
    d, m = F.delta_of(st), F.mu_of(st)
    if d != m:
        diff_found = (sorted(lt), d, m)
        break
ok &= F.verdict(diff_found is not None, "delta and mu are DIFFERENT functions",
                f"e.g. delta={diff_found[1]} mu={diff_found[2]}" if diff_found else "")

# and mu <= delta everywhere, which is the direction the frozen implication needs
bad = 0
for n in (3, 4, 5):
    for lt in F.posets_up_to_iso(n):
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        st = F.all_pair_stats(n, lt, LEs)
        if not st:
            continue
        if not (F.mu_of(st) <= F.delta_of(st)):
            bad += 1
ok &= F.verdict(bad == 0, "mu <= delta at every n<=5 poset (exact)", f"{bad} violations")

# --------------------------------------------------------------------------------------
F.banner("p0.7  pair statistics -- p_xy and P(adjacent) against hand values")

# A_2: one incomparable pair, p = 1/2, always adjacent.
LE = L.linear_extensions(2, frozenset())
p, a = F.pair_stats(2, frozenset(), LE, 0, 1)
ok &= F.verdict(p == Fraction(1, 2) and a == Fraction(1, 1), f"A_2: p={p} P_adj={a}")

# A_3: p = 1/2 by symmetry; P(adjacent) = 2/3 (6 linear extensions, 4 have them adjacent).
LE = L.linear_extensions(3, frozenset())
p, a = F.pair_stats(3, frozenset(), LE, 0, 1)
ok &= F.verdict(p == Fraction(1, 2) and a == Fraction(2, 3), f"A_3: p={p} P_adj={a}")

# V-poset 0<1, 0<2: the pair {1,2} has p = 1/2, and they are always adjacent (positions 1,2).
v = mk(3, [(0, 1), (0, 2)])
LE = L.linear_extensions(3, v)
p, a = F.pair_stats(3, v, LE, 1, 2)
ok &= F.verdict(p == Fraction(1, 2) and a == Fraction(1, 1), f"V, pair (1,2): p={p} P_adj={a}")

# --------------------------------------------------------------------------------------
print()
print("=" * 88)
print("p0 OVERALL: " + ("PASS" if ok else "FAIL"))
print("=" * 88)
sys.exit(0 if ok else 1)
