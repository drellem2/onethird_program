"""selftesta94c3 -- NEGATIVE CONTROLS.  Every detector in this audit, shown failing.

A check that has never been seen to fail is not evidence.  Each control below
breaks something on purpose and asserts that the corresponding section of this
instrument NOTICES.  A control that passes silently is itself a failure and is
reported as one.
"""

from fractions import Fraction as F
from itertools import permutations
import re
from libA94 import (all_posets, linear_extensions, T_matrix, threshold_sets,
                    is_prefix_or_suffix, spectral_gap, banner)

fails = 0


def expect(cond, name, detail=""):
    global fails
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    if not cond:
        fails += 1


def min_n(supply, demand):
    for n in range(2, 300000):
        if supply(n) <= demand(n):
            return n
    return None


# --------------------------------------------------------------------------
banner("NC1. THE THRESHOLD DETECTOR MUST REJECT A WRONG CLOSED FORM")
print("""  a1 compares a brute-force search against the closed form.  If that
  comparison were vacuous -- e.g. because the search silently used the closed
  form -- a1 could not catch a dropped factor.  Feed it three WRONG forms.
""")
leak, C3 = F(1, 5), F(1)
dem = leak * leak / (2 * C3)
truth = min_n(lambda n: F(2, n + 1), lambda n: dem)
expect(truth == 99, "control: the correct threshold is still 99", f"got {truth}")
for label, wrong in (("4C_3/L^2  (the -1 dropped)", 100),
                     ("2C_3/L^2  (the 4 halved)", 49),
                     ("4C_3/(6 L^2) - 1  (the factor 6 WRONGLY inserted)", 16)):
    expect(truth != wrong, f"rejects {label}", f"wrong form gives {wrong}")

print("""
  NC1b -- and the MIXED-UNIT arm must be caught by the same comparison:""")
mixed = min_n(lambda n: F(n - 1, 3 * n * n), lambda n: dem)
expect(mixed != truth, "mixed-unit solve differs from the correct one",
       f"{mixed} vs {truth}, ratio {truth/mixed:.3f}")
expect(5.5 < truth / mixed < 6.5, "and it differs by ~6, not by some other factor")

# --------------------------------------------------------------------------
banner("NC2. THE SWEEP DETECTOR MUST NOTICE AN ORDER-SLICE MASQUERADING AS A LEVEL SET")
print("""  mg-76b2 records a real defect: its first sweep returned SLICES of the
  sorted order rather than LEVEL sets, and where v ties -- the antichain ties
  everywhere -- a slice splits the tie and returns sets no threshold produces.
  If my threshold_sets() were accidentally slice-shaped, a2's Lemma 3.3 check
  would be vacuous.  Build both and compare on the antichain.
""")


def order_slices(v, n):
    idx = sorted(range(n), key=lambda i: v[i])
    return set(frozenset(idx[:k]) for k in range(1, n // 2 + 1)) | \
           set(frozenset(idx[n - k:]) for k in range(1, n // 2 + 1))


n = 4
exts = linear_extensions(n, frozenset())          # the antichain: every perm
T = T_matrix(n, exts)
gap, vfied, vals, vecs = spectral_gap(n, T)
# A DEFECT OF MINE, KEPT.  The first version of this control used whatever
# vector Jacobi happened to return for the antichain -- [0.707,-0.707,0,0],
# which is NOT monotone -- and then asserted Lemma 3.3's conclusion about it.
# Lemma 3.3 has a hypothesis; the control had dropped it, and duly "failed"
# against correct code.  The antichain's S_P|_H is the ZERO matrix, so EVERY
# vector in H is a dominant eigenvector; the one that exhibits the tie-splitting
# defect is the source's own (a,a,a,-3a), whose negation is monotone.
v = [1.0, 1.0, 1.0, -3.0]
print(f"  antichain n=4: 1-lambda_std = {gap:.6f}; S_P|_H = 0, so every vector")
print(f"  in H is dominant.  Using the source's tied vector v = {v}")
print(f"  (Jacobi's arbitrary pick was {[round(x,4) for x in vfied]} -- not monotone,")
print(f"   which is why asserting Lemma 3.3 about IT was my error, not the code's.)")
lv = threshold_sets(v, n)
sl = order_slices(v, n)
bad_lv = [S for S in lv if not is_prefix_or_suffix(n, S)]
bad_sl = [S for S in sl if not is_prefix_or_suffix(n, S)]
print(f"  level sets      : {sorted(sorted(s) for s in lv)}   non-prefix/suffix: {len(bad_lv)}")
print(f"  order slices    : {sorted(sorted(s) for s in sl)}   non-prefix/suffix: {len(bad_sl)}")
expect(len(bad_lv) == 0,
       "level sets of the MONOTONE tied vector stay in the prefix family")
expect(len(bad_sl) > 0, "order slices DO leave it -- so the check is not vacuous",
       f"{len(bad_sl)} spurious sets")

# --------------------------------------------------------------------------
banner("NC3. THE MATRIX-vs-DEFINITION CHECK MUST CATCH THE lib2de0 CONVENTION")
print("""  mg-76b2 sec.8 reports that lib2de0 computes |A| - |A cap set(p[:|A|])| --
  the first |A| POSITIONS rather than the positions indexed by A.  If a2's
  section B were computing both sides the same way, it would pass under that
  bug too.  Run the bug through it.
""")


def leak_matrix(n, T, A):
    s = F(0)
    for x in A:
        for a in A:
            s += T[x][a]
    return len(A) - s


def leak_buggy(n, exts, A):
    tot = 0
    for perm in exts:
        img = set(perm[:len(A)])
        tot += len(set(A) - img)
    return F(tot, len(exts))


dis = tot = 0
for nn in (2, 3, 4, 5):
    for rel in all_posets(nn):
        ex = linear_extensions(nn, rel)
        Tm = T_matrix(nn, ex)
        for mask in range(1, (1 << nn) - 1):
            A = [i for i in range(nn) if mask >> i & 1]
            tot += 1
            if leak_matrix(nn, Tm, A) != leak_buggy(nn, ex, A):
                dis += 1
print(f"  {dis} of {tot} (poset, cut) pairs at n <= 5 disagree under the bug.")
print("  (A DEFECT OF MINE, KEPT: the first version of this loop ran n = 3,4,5 and")
print("   reported 8177/11312.  mg-76b2's 'n <= 5' INCLUDES n = 2, and the single")
print("   missing disagreement is the 2-chain witness the document itself names.)")
print(f"  mg-76b2 sec.8 reports 8178 of 11316 at n <= 5: {(dis, tot) == (8178, 11316)}")
expect(dis > 0, "the check is not vacuous -- the bug IS detected")
expect((dis, tot) == (8178, 11316),
       "and mg-76b2's sec.8 figure reproduces exactly", f"{dis}/{tot}")
print("""
  The smallest witness mg-76b2 names is the 2-chain 0 < 1 with A = {1}:""")
ex2 = linear_extensions(2, frozenset({(0, 1)}))
T2 = T_matrix(2, ex2)
print(f"    L(P) = {ex2};  definition gives "
      f"{leak_matrix(2, T2, [1])};  the buggy convention gives "
      f"{leak_buggy(2, ex2, [1])}")
expect(leak_matrix(2, T2, [1]) == 0 and leak_buggy(2, ex2, [1]) == 1,
       "witness reproduces (0 vs 1)")

# --------------------------------------------------------------------------
banner("NC4. THE L4 CENSUS MUST FIRE ON A FILE THAT REALLY DOES READ F")
PAT = re.compile(r"\bL4\b|modulus|F\(\s*(?:0\.|eps|\\vare|ε)")
CLEAN = "eps_leak = 0.20 comes from mg-3ce3's survives envelope.\nn >= 4/eps^2 - 1\n"
DIRTY = "eps_leak = F(0.02)   # read off L4's modulus\nbudget = eps_leak**2/2\n"
expect(not PAT.search(CLEAN), "does not fire on an F-free calibration line")
expect(bool(PAT.search(DIRTY)), "DOES fire on a line that reads F(0.02)")

SPAT = re.compile(r"\bF\b|modulus|envelope|C_lin|alpha")
expect(not SPAT.search("survives=(len(surviving) > 0),"),
       "predicate scanner is quiet on mg-3ce3's actual survives line")
expect(bool(SPAT.search("survives=(D <= F(eps)),")),
       "and DOES fire on a survives line that consults the modulus")

# --------------------------------------------------------------------------
banner("NC5. THE mg-200d CENSUS MUST DISTINGUISH LABELLED FROM BARE")
# A DEFECT OF MINE, KEPT: the first classifier counted the word "window" as a
# conditional marker.  It is not -- it is the NOUN the conditional qualifies --
# and the control below is what caught it.  Removing it changes no verdict in
# a4 (all three labelled sites carry "CONDITIONAL", "*if*" or "not assumed").
LBL = re.compile(r"CONDITIONAL|conditional|\bif\b|mg-131e|not assumed|labelled")
a = "| 17 | window n <= 98 | **CONDITIONAL** on the mg-200d conjecture |"
b = "The window still owed is n <= 98."
expect(bool(LBL.search(a)), "labels a CONDITIONAL row as labelled")
expect(not LBL.search(b), "flags an unqualified 'n <= 98' sentence as BARE")

# --------------------------------------------------------------------------
banner("NC6. C_3^gap >= 1 IDENTICALLY -- the hand claim H7, tested rather than asserted")
print("""  H7 says C_3^gap = min_k(1-rho(A_k))/(1-lambda_std) >= 1 for EVERY poset,
  because 1-lambda_std is the minimum of the Rayleigh quotient over all of H and
  a centred prefix indicator lives in H.  If that were false somewhere, my
  reading of P4 would be wrong in the other direction.
""")
viol = checked = 0
worst = None
for nn in (3, 4, 5, 6):
    for rel in all_posets(nn):
        ex = linear_extensions(nn, rel)
        Tm = T_matrix(nn, ex)
        g, v, vals, vecs = spectral_gap(nn, Tm)
        if g < 1e-12:
            continue
        omr = min(F(nn) * leak_matrix(nn, Tm, list(range(k))) / (k * (nn - k))
                  for k in range(1, nn))
        r = float(omr) / g
        checked += 1
        if r < 1 - 1e-9:
            viol += 1
        worst = r if worst is None else min(worst, r)
print(f"  {checked} posets with a positive gap; {viol} with C_3^gap < 1; "
      f"smallest ratio seen {worst:.9f}")
expect(viol == 0, "H7 holds -- C_3^gap is never below 1")
expect(worst is not None and abs(worst - 1.0) < 1e-6,
       "and 1 IS attained, so the bound is tight and not slack")

banner("SELFTEST SUMMARY")
print(f"  {fails} failing control(s)")
raise SystemExit(1 if fails else 0)
