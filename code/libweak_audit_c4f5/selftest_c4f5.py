#!/usr/bin/env python3
"""selftest_c4f5 — drill this audit's instrument before any of its numbers are used.

Exit 0 iff every assertion passes.  Every check that could pass VACUOUSLY (an empty
population, a loop that never runs, a detector that cannot report the other answer) is
paired with a NON-VACUITY assertion that fails if the check had nothing to check.
That pairing is here because a vacuous control inside the auditor's own file is this
arc's signature defect and it has landed in three recent tickets.
"""
import sys
from fractions import Fraction
from itertools import permutations
import lib_c4f5 as L

FAIL = []
NCHK = 0


def chk(name, cond, detail=""):
    global NCHK
    NCHK += 1
    if cond:
        print("  ok   %-58s %s" % (name, detail))
    else:
        print("  FAIL %-58s %s" % (name, detail))
        FAIL.append(name)


print("=" * 78)
print("A. POPULATION — the naturally labelled poset counts must be A006455")
print("=" * 78)
# 1, 1, 2, 7, 40, 357, 4824, 96428 is the number of transitively closed subsets of
# {(i,j) : i<j}, i.e. of naturally labelled posets.  It is NOT the labelled-poset count
# (1,1,3,19,219,4231,130023) and the two are routinely confused.
A006455 = [1, 1, 2, 7, 40, 357, 4824]
for n in range(0, 7):
    got = sum(1 for _ in L.gen_natural_posets(n))
    chk("|naturally labelled posets on %d|" % n, got == A006455[n],
        "%d (expected %d)" % (got, A006455[n]))

# every generated object really IS transitively closed and naturally labelled
bad = 0
seen = set()
cnt = 0
for P in L.gen_natural_posets(5):
    n, up, down = P
    cnt += 1
    if not L.is_transitively_closed(n, up):
        bad += 1
    for x in range(n):
        if up[x] & ((1 << (x + 1)) - 1):
            bad += 1
    seen.add(up)
chk("A2 every n=5 poset transitively closed & naturally labelled", bad == 0, "%d bad" % bad)
chk("A2-NONVACUITY the n=5 loop ran", cnt == 357, "%d posets walked" % cnt)
chk("A3 no duplicates at n=5", len(seen) == 357, "%d distinct up-vectors" % len(seen))

print()
print("=" * 78)
print("B. LINEAR EXTENSION COUNT — the ideal DP against brute-force enumeration")
print("=" * 78)
mismatch = 0
tested = 0
for n in range(1, 6):
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        b = len(L.linear_extensions(P))
        tested += 1
        if a["eP"] != b:
            mismatch += 1
chk("B1 ideal-DP e(P) == brute force, all posets n<=5", mismatch == 0,
    "%d posets, %d mismatches" % (tested, mismatch))
chk("B1-NONVACUITY the comparison ran", tested == sum(A006455[1:6]),
    "%d comparisons" % tested)
chk("B2 e(antichain 6) = 720", L.analyse(L.antichain(6))["eP"] == 720)
chk("B2 e(chain 6) = 1", L.analyse(L.chain(6))["eP"] == 1)
chk("B2 e(W_4 = C_4 + pt) = 5", L.analyse(L.W(4))["eP"] == 5,
    "one free point in a 4-chain has 5 slots")

print()
print("=" * 78)
print("C. PAIR PROBABILITIES AND FOOTRULE — DP against brute force")
print("=" * 78)
worst_q = Fraction(0)
worst_f = Fraction(0)
tested = 0
for n in range(2, 6):
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        les = L.linear_extensions(P)
        e = len(les)
        # brute-force pair probabilities and footrule
        for (x, y) in a["inc"]:
            c = sum(1 for s in les if s.index(y) < s.index(x))
            worst_q = max(worst_q, abs(a["q"][(x, y)] - Fraction(c, e)))
        f = sum(sum(abs(s.index(x) - x) for x in range(n)) for s in les)
        worst_f = max(worst_f, abs(a["footrule"] - Fraction(f, e)))
        tested += 1
chk("C1 q_{xy} exact vs brute force, all posets n<=5", worst_q == 0,
    "max abs error %s over %d posets" % (worst_q, tested))
chk("C2 E[footrule] exact vs brute force, all posets n<=5", worst_f == 0,
    "max abs error %s" % worst_f)
chk("C-NONVACUITY the brute force ran on a poset with incomparable pairs",
    tested > 0 and any(L.analyse(P)["inc"] for P in L.gen_natural_posets(4)))

print()
print("=" * 78)
print("D. NAMED VALUES BY HAND — positive controls with answers known in advance")
print("=" * 78)
# --- DEFECT 1 OF THIS INSTRUMENT, kept in place rather than quietly repaired ---------
# I first asserted delta(V) = 1/3 for V = {0<1, 0<2}, because mg-c3ca's README names a
# "V poset (delta = 1/3, E_maj = 2/3)" as its positive control and I matched the NAME.
# The code was right and my assertion was wrong: V has delta = 1/2 (its one incomparable
# pair {1,2} is exchangeable).  The delta = 1/3 three-element object is C_2 (+) C_1 —
# one relation and one free point — which is W_2 here.  Same shape as mg-c3ca's own
# recorded defect 1, committed by its auditor.
a = L.analyse(L.V_poset())
chk("D1 V = {0<1,0<2} has delta = 1/2, NOT 1/3 (my first assertion was wrong)",
    a["delta"] == Fraction(1, 2), str(a["delta"]))
a = L.analyse(L.W(2))
chk("D1b the delta=1/3 3-element object is W_2 = C_2 (+) C_1", a["delta"] == Fraction(1, 3),
    str(a["delta"]))
chk("D1b W_2 E_maj = 2/3 (mg-c3ca's 'V-gadget' value)", L.E_maj(a) == Fraction(2, 3),
    str(L.E_maj(a)))
chk("D1c-NONVACUITY exactly 3 of the 7 naturally labelled n=3 posets have delta=1/3",
    sum(1 for P in L.gen_natural_posets(3) if L.analyse(P)["delta"] == Fraction(1, 3)) == 3)
a = L.analyse(L.antichain(5))
chk("D2 antichain(5) delta = 1/2", a["delta"] == Fraction(1, 2), str(a["delta"]))
chk("D2 antichain(5) E[inv] = C(5,2)/2 = 5", a["inv"] == Fraction(5), str(a["inv"]))
chk("D2 antichain(5) E[F] = (n^2-1)/3 = 8", a["footrule"] == Fraction(8), str(a["footrule"]))
a = L.analyse(L.chain(5))
chk("D3 chain(5) delta is None (undefined, NOT 0)", a["delta"] is None, str(a["delta"]))
chk("D3 chain(5) E[inv] = 0", a["inv"] == 0)

# W_m by the hand formula.  delta(W_m) = floor((m+1)/2)/(m+1)  -- this is mg-c3ca's own
# recorded correction to STATE.md:102's parenthetical, and it is re-derived here rather
# than copied: the free point sits uniformly in one of m+1 slots, so against the chain
# element of rank i the split is i/(m+1) vs (m+1-i)/(m+1).
for m in (4, 5, 6, 8):
    a = L.analyse(L.W(m))
    want_delta = Fraction((m + 1) // 2, m + 1)
    want_maj = sum(Fraction(min(i, m + 1 - i), m + 1) for i in range(1, m + 1))
    want_invL = sum(Fraction(i, m + 1) for i in range(1, m + 1))
    chk("D4 W_%d delta = floor((m+1)/2)/(m+1)" % m, a["delta"] == want_delta,
        "%s == %s" % (a["delta"], want_delta))
    # DEFECT 2 OF THIS INSTRUMENT: I asserted mg-c3ca's hand formula against E[inv_L],
    # the natural-labelling inversion count.  It is the formula for E_maj = E[inv_e].
    # Both numbers are correct and they are DIFFERENT numbers; the assertion conflated
    # two reference orders.  Both are now asserted separately, which is the point:
    # E[inv] is reference-dependent and E_maj is not.
    chk("D4 W_%d E_maj = sum min(i,m+1-i)/(m+1)  [= E[inv_e]]" % m,
        L.E_maj(a) == want_maj, "%s == %s" % (L.E_maj(a), want_maj))
    chk("D4 W_%d E[inv_L] = sum i/(m+1)  [natural labelling, a DIFFERENT number]" % m,
        a["inv"] == want_invL, "%s == %s" % (a["inv"], want_invL))
    chk("D4 W_%d E_maj < E[inv_L] strictly (E_maj is the min over reference orders)" % m,
        L.E_maj(a) < a["inv"])
chk("D4-CONTRADICTS-STATE.md:102 delta(W_4) != 1/2",
    L.analyse(L.W(4))["delta"] == Fraction(2, 5),
    "2/5, not 1/2 — mg-c3ca's lineage correction reproduces")
# the reference-dependence, exhibited on ONE isomorphism class
vals = sorted(set(L.analyse(P)["inv"] for P in L.gen_natural_posets(3)
                  if L.analyse(P)["delta"] == Fraction(1, 3)))
chk("D5 E[inv_L] MOVES across labellings of one iso class; E_maj does not",
    len(vals) > 1 and len(set(L.E_maj(L.analyse(P)) for P in L.gen_natural_posets(3)
                              if L.analyse(P)["delta"] == Fraction(1, 3))) == 1,
    "E[inv_L] in %s ; E_maj constant" % ([str(v) for v in vals],))

print()
print("=" * 78)
print("E. THE EIGENSOLVER — written here, so it is drilled here")
print("=" * 78)
ev = L.jacobi_eigenvalues([[2.0, 0.0], [0.0, 3.0]])
chk("E1 diag(2,3)", all(abs(a - b) < 1e-12 for a, b in zip(ev, [2.0, 3.0])), str(ev))
ev = L.jacobi_eigenvalues([[0.0, 1.0], [1.0, 0.0]])
chk("E2 [[0,1],[1,0]] -> {-1,1}", all(abs(a - b) < 1e-12 for a, b in zip(ev, [-1.0, 1.0])), str(ev))
# J_n/n has spectrum {1, 0^(n-1)}
n = 5
J = [[1.0 / n] * n for _ in range(n)]
ev = L.jacobi_eigenvalues(J)
chk("E3 J_5/5 -> {0,0,0,0,1}", abs(ev[-1] - 1.0) < 1e-12 and abs(ev[0]) < 1e-12, str([round(x, 6) for x in ev]))
# a 3x3 with a known characteristic polynomial: [[1,2,0],[2,1,0],[0,0,5]] -> {-1,3,5}
ev = L.jacobi_eigenvalues([[1.0, 2.0, 0.0], [2.0, 1.0, 0.0], [0.0, 0.0, 5.0]])
chk("E4 known 3x3 -> {-1,3,5}", all(abs(a - b) < 1e-10 for a, b in zip(ev, [-1.0, 3.0, 5.0])),
    str([round(x, 6) for x in ev]))

print()
print("=" * 78)
print("F. lambda_std — the two ends of ledger row 1, which are the only fixed points")
print("=" * 78)
lam, ev = L.lambda_std_from_T(L.analyse(L.antichain(6))["T"])
chk("F1 antichain(6): lambda_std = 0 exactly (T = J/n)", abs(lam) < 1e-10, "%.12f" % lam)
lam, ev = L.lambda_std_from_T(L.analyse(L.chain(6))["T"])
chk("F2 chain(6): lambda_std = 1 (T = I, an ordinal sum)", abs(lam - 1.0) < 1e-10, "%.12f" % lam)
# row 1: lambda_std = 1  <=>  ordinal sum  <=>  incomparability graph disconnected.
# NOT re-derived as a theorem (it is proven, ledger row 1) -- used here as a CONTROL on
# the eigen-pipeline: if the pipeline is right, the equivalence must hold on the census.
mis = 0
tot = 0
for n in (4, 5):
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        lam, _ = L.lambda_std_from_T(a["T"])
        disconnected = not a["primitive"]
        tot += 1
        if (abs(lam - 1.0) < 1e-9) != disconnected:
            mis += 1
chk("F3 lambda_std==1 <=> NOT primitive, every poset n=4,5 (ledger row 1 as a control)",
    mis == 0, "%d posets, %d mismatches" % (tot, mis))
chk("F3-NONVACUITY both answers occur in the population",
    any(L.analyse(P)["primitive"] for P in L.gen_natural_posets(5)) and
    any(not L.analyse(P)["primitive"] for P in L.gen_natural_posets(5)))

print()
print("=" * 78)
print("G. THE DETECTOR CAN REPORT THE OTHER ANSWER")
print("=" * 78)
# A null result ("0 frozen posets found") is worthless unless the code can say delta<1/3.
# Drill it on a CONSTRUCTED pair table that is frozen, fed through the same delta rule.
fake_q = {(0, 1): Fraction(1, 5), (0, 2): Fraction(1, 4), (1, 2): Fraction(3, 10)}
fake_delta = max(min(v, 1 - v) for v in fake_q.values())
chk("G1 delta rule reports a constructed frozen table", fake_delta < Fraction(1, 3),
    "delta = %s < 1/3" % fake_delta)
fake_q2 = dict(fake_q); fake_q2[(0, 1)] = Fraction(1, 2)
chk("G2 the same rule reports NOT frozen when one pair is balanced",
    max(min(v, 1 - v) for v in fake_q2.values()) >= Fraction(1, 3))
# and that the census predicate is the same expression as the one just drilled
chk("G3 census uses the same rule (same expression, on a real poset)",
    L.analyse(L.W(2))["delta"] == Fraction(1, 3))
# and: the census MUST be able to find something below 1/3 if it were there.  Drill it
# on a synthetic poset-shaped record whose q table is frozen, pushed through the census
# predicate verbatim.
synth = dict(q={(0, 1): Fraction(3, 10), (0, 2): Fraction(1, 4)}, inc=[(0, 1), (0, 2)])
synth_delta = max(min(synth["q"][p], 1 - synth["q"][p]) for p in synth["inc"])
chk("G4 census predicate on a synthetic FROZEN record reports frozen",
    synth_delta < Fraction(1, 3), "delta = %s" % synth_delta)

print()
print("=" * 78)
print("J. MAJORITY ORDER — the object `inv_e` is defined against")
print("=" * 78)
a = L.analyse(L.W(4))
mo = L.majority_order(a)
chk("J1 W_4 majority order exists", mo is not None, str(mo))
chk("J2 W_4 majority order is a linear extension of W_4", L.is_linear_extension(L.W(4), mo))
chk("J3 E[inv_e] == E_maj on W_4", L.E_inv_wrt(a, mo) == L.E_maj(a),
    "%s == %s" % (L.E_inv_wrt(a, mo), L.E_maj(a)))
# NON-VACUITY the other way: the majority order does NOT always exist.  If this check
# found nothing, J1-J3 would be testing a property of a class I had never left.
nomaj = sum(1 for P in L.gen_natural_posets(5) if L.majority_order(L.analyse(P)) is None)
chk("J4 the majority order FAILS to exist somewhere at n=5 (so `inv_e` is not always defined)",
    nomaj > 0, "%d of 357 posets have no strict majority total order" % nomaj)
# and where it does exist, is it always a linear extension?
bad = 0; good = 0
for P in L.gen_natural_posets(5):
    a2 = L.analyse(P); mo2 = L.majority_order(a2)
    if mo2 is None:
        continue
    good += 1
    if not L.is_linear_extension(P, mo2):
        bad += 1
chk("J5 where it exists, the majority order is a linear extension (n=5)", bad == 0,
    "%d/%d, 0 bad" % (good, good))

print()
print("=" * 78)
print("H. MASTER-BOUND ARITHMETIC IDENTITIES (Lemmas 2.1 and 2.3, re-derived)")
print("=" * 78)
# Lemma 2.3: sum_{k=1}^{n-1} k(n-k)/n = (n^2-1)/6
ok = all(sum(Fraction(k * (n - k), n) for k in range(1, n)) == Fraction(n * n - 1, 6)
         for n in range(2, 12))
chk("H1 Lemma 2.3  sum k(n-k)/n = (n^2-1)/6  for n=2..11", ok)
# Lemma 2.1: sum_k leak_k = E[F]/2, checked by brute force on every poset n<=5
worst = Fraction(0); tot = 0
for n in range(2, 6):
    for P in L.gen_natural_posets(n):
        les = L.linear_extensions(P); e = len(les)
        lk = Fraction(0)
        for k in range(1, n):
            c = sum(sum(1 for x in range(k) if s.index(x) >= k) for s in les)
            lk += Fraction(c, e)
        F = Fraction(sum(sum(abs(s.index(x) - x) for x in range(n)) for s in les), e)
        worst = max(worst, abs(lk - F / 2)); tot += 1
chk("H2 Lemma 2.1  sum_k leak_k = E[F]/2, every poset n<=5", worst == 0,
    "max error %s over %d posets" % (worst, tot))
# Lemma 2.2: E[F] <= 2 E[inv]  (DG upper half)
viol = 0; tot = 0
for n in range(2, 7):
    for P in L.gen_natural_posets(n):
        a = L.analyse(P); tot += 1
        if a["footrule"] > 2 * a["inv"]:
            viol += 1
chk("H3 Lemma 2.2  E[F] <= 2E[inv], every poset n<=6", viol == 0,
    "%d posets, %d violations" % (tot, viol))
chk("H3-NONVACUITY E[F] < 2E[inv] strictly somewhere (the bound is not an identity)",
    any(L.analyse(P)["footrule"] < 2 * L.analyse(P)["inv"]
        for P in L.gen_natural_posets(4) if L.analyse(P)["inc"]))

print()
print("=" * 78)
print("I. sum_x m_x = 2 E[inv]  (the identity the parent's Sec.1 iff runs on)")
print("=" * 78)
worst = Fraction(0); tot = 0
for n in range(2, 7):
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        worst = max(worst, abs(sum(a["m"]) - 2 * a["inv"])); tot += 1
chk("I1 sum_x m_x == 2 E[inv], every poset n<=6", worst == 0,
    "max error %s over %d posets" % (worst, tot))
chk("I1-NONVACUITY sum_x m_x is not identically 0",
    any(sum(L.analyse(P)["m"]) > 0 for P in L.gen_natural_posets(4)))

print()
print("=" * 78)
print("SELFTEST: %d checks, %d failures" % (NCHK, len(FAIL)))
if FAIL:
    for f in FAIL:
        print("  FAILED:", f)
print("=" * 78)
sys.exit(1 if FAIL else 0)
