#!/usr/bin/env python3
"""mg-0e8c a1 -- SELF-TEST.  Nothing this instrument reports is worth reading until this is
green, and it is FIRST rather than last because the verdict it supports is a verdict about a
DEFINITION.  If `lambda_std` or `E[inv_e]` is computed under a different convention from the
corpus's, the whole finding is a currency error of exactly the kind the ledger warns about --
which would be an unusually embarrassing way to file a report ABOUT a currency error.

SIX CHECKS.

  T1  poset counts.  Posets on {0..n-1} admitting the identity as a linear extension are counted
      against the corpus's own enumerator (code/c3_audit_a94c3/libA94.all_posets), which was
      written independently from the tex.  Two enumerators agreeing is the only evidence
      available that "poset" means the same thing in both.
  T2  CROSS-IMPLEMENTATION AGREEMENT on 1 - lambda_std.  libA94.spectral_gap vs this file's
      one_minus_lambda_std, every poset to n = 5.  They share no code.
  T3  the antichain, computed BY HAND and checked.  T = J/n, so S = J/n, M = I - J/n, whose
      spectrum is {0} u {1}^(n-1): 1 - lambda_std = 1 EXACTLY.  And E[inv_e] = C(n,2)/2 there
      by symmetry.  Both are hand-derivable, so this pins the code to arithmetic a reader can
      redo on paper.
  T4  the chain.  One linear extension, T = I, S = I, M = 0, 1 - lambda_std = 0; E[inv_e] = 0.
  T5  the master bound direction.  6 E[inv_e]/(n^2-1) >= 1 - lambda_std on every poset tested.
      This is mg-210d's bound; it is INHERITED, not re-derived here, and this check is a test
      that our two quantities are on the sides of it the corpus says they are.
  T6  PSD oracle.  is_psd_exact is checked against hand-built matrices with known verdicts,
      including the boundary cases (zero pivot with a non-zero off-diagonal; the exactly-
      singular PSD case) that a tolerance-based test gets wrong.

EXITS 0 green, 1 red.
"""

import os
import sys
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "c3_audit_a94c3"))

import lib0e8c as L                                        # noqa: E402
import libA94 as A                                          # noqa: E402

FAIL = []


def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + ("   " + detail if detail else ""))
    if not ok:
        FAIL.append(name)


print("=" * 78)
print("mg-0e8c a1 -- SELF-TEST")
print("=" * 78)

# ---- T1 -------------------------------------------------------------------------------
print("\nT1  poset enumeration vs the corpus's independent enumerator")
for n in range(1, 7):
    mine = sorted(L.all_posets(n))
    theirs = sorted(A.all_posets(n))
    check("n=%d  counts and sets agree" % n, mine == theirs,
          "%d posets" % len(mine))

# ---- T2 -------------------------------------------------------------------------------
print("\nT2  cross-implementation agreement on 1 - lambda_std (no shared code)")
for n in range(2, 6):
    worst = 0.0
    for rel in L.all_posets(n):
        exts = L.linear_extensions(n, rel)
        T = L.T_matrix(n, exts)
        mine = L.one_minus_lambda_std(n, L.S_matrix(n, T))
        theirs = A.spectral_gap(n, A.T_matrix(n, A.linear_extensions(n, rel)))[0]
        worst = max(worst, abs(mine - theirs))
    check("n=%d  max |mine - libA94|" % n, worst < 1e-9, "%.2e" % worst)

# ---- T3 -------------------------------------------------------------------------------
print("\nT3  the ANTICHAIN, against hand arithmetic")
for n in range(2, 8):
    rel = frozenset()
    exts = L.linear_extensions(n, rel)
    S = L.S_matrix(n, L.T_matrix(n, exts))
    g = L.one_minus_lambda_std(n, S)
    check("n=%d  1 - lambda_std == 1 exactly (hand: spec(I - J/n) = {0, 1^(n-1)})" % n,
          abs(g - 1.0) < 1e-9, "%.12f" % g)
    Einv = L.E_inv_e(n, exts, rel)
    hand = Fraction(n * (n - 1), 4)
    check("n=%d  E[inv_e] == C(n,2)/2 (hand: each pair flipped w.p. 1/2)" % n,
          Einv == hand, "%s vs %s" % (Einv, hand))

# ---- T4 -------------------------------------------------------------------------------
print("\nT4  the CHAIN")
for n in range(2, 8):
    rel = frozenset(combinations(range(n), 2))
    exts = L.linear_extensions(n, rel)
    check("n=%d  exactly one linear extension" % n, len(exts) == 1, str(len(exts)))
    S = L.S_matrix(n, L.T_matrix(n, exts))
    g = L.one_minus_lambda_std(n, S)
    check("n=%d  1 - lambda_std == 0" % n, abs(g) < 1e-9, "%.12f" % g)
    check("n=%d  E[inv_e] == 0" % n, L.E_inv_e(n, exts, rel) == 0)

# ---- T5 -------------------------------------------------------------------------------
print("\nT5  master bound 1 - lambda_std <= 6 E[inv_e]/(n^2-1), inherited from mg-210d")
for n in range(2, 7):
    viol = 0
    tight = 0
    for rel in L.all_posets(n):
        exts = L.linear_extensions(n, rel)
        Einv = L.E_inv_e(n, exts, rel)
        rhs = float(L.master_bound_rhs(n, Einv))
        lhs = L.one_minus_lambda_std(n, L.S_matrix(n, L.T_matrix(n, exts)))
        if lhs > rhs + 1e-9:
            viol += 1
        if abs(lhs - rhs) < 1e-9:
            tight += 1
    check("n=%d  violations" % n, viol == 0, "%d violations, %d tight" % (viol, tight))

# ---- T6 -------------------------------------------------------------------------------
print("\nT6  is_psd_exact on hand-built matrices with known verdicts")
F = Fraction
cases = [
    ("identity 2x2", [[F(1), F(0)], [F(0), F(1)]], True),
    ("negative diagonal", [[F(-1), F(0)], [F(0), F(1)]], False),
    ("PSD singular  [[1,1],[1,1]]", [[F(1), F(1)], [F(1), F(1)]], True),
    ("indefinite    [[1,2],[2,1]]", [[F(1), F(2)], [F(2), F(1)]], False),
    ("zero pivot with off-diag [[0,1],[1,1]]", [[F(0), F(1)], [F(1), F(1)]], False),
    ("zero pivot clean [[0,0],[0,1]]", [[F(0), F(0)], [F(0), F(1)]], True),
    ("Laplacian of an edge [[1,-1],[-1,1]]", [[F(1), F(-1)], [F(-1), F(1)]], True),
    ("3x3 borderline det 0", [[F(2), F(1), F(1)], [F(1), F(2), F(1)], [F(1), F(1), F(2)]], True),
    ("3x3 negative minor", [[F(1), F(2), F(0)], [F(2), F(1), F(0)], [F(0), F(0), F(1)]], False),
]
for name, M, want in cases:
    check("PSD(%s) == %s" % (name, want), L.is_psd_exact(M) is want)

print("\nT6b  is_pd_exact (STRICT) on hand-built matrices")
pd_cases = [
    ("identity 2x2", [[F(1), F(0)], [F(0), F(1)]], True),
    ("PSD but SINGULAR [[1,1],[1,1]]", [[F(1), F(1)], [F(1), F(1)]], False),
    ("negative definite [[-1,0],[0,-2]]", [[F(-1), F(0)], [F(0), F(-2)]], False),
    ("[[2,1],[1,2]]", [[F(2), F(1)], [F(1), F(2)]], True),
]
for name, M, want in pd_cases:
    check("PD(%s) == %s" % (name, want), L.is_pd_exact(M) is want)

# THE ORACLE THE VACUITY VERDICT ACTUALLY RESTS ON.  The first draft of this instrument tested
# `S_P PSD`, which is a DIFFERENT (strictly stronger) statement -- see lib0e8c's docstring.  The
# check below is against the float spectrum of the correct quantity: lambda_std = 1 - lambda_2(M).
print("\nT6c  exact `lambda_std >= 0` oracle agrees with the float value of 1 - lambda_2(M)")
for n in range(2, 6):
    dis = 0
    for rel in L.all_posets(n):
        exts = L.linear_extensions(n, rel)
        S = L.S_matrix(n, L.T_matrix(n, exts))
        exact = L.lambda_std_nonneg_exact(n, S)
        flt = (1.0 - L.one_minus_lambda_std(n, S)) >= -1e-9
        if exact != flt:
            dis += 1
    check("n=%d  disagreements" % n, dis == 0, "%d" % dis)

# and the separation itself, stated as a check so the correction is not just prose
print("\nT6d  the two oracles are DIFFERENT statements (this is the recorded defect)")
sep = 0
for rel in L.all_posets(5):
    exts = L.linear_extensions(5, rel)
    S = L.S_matrix(5, L.T_matrix(5, exts))
    if L.lambda_std_nonneg_exact(5, S) and not L.is_psd_exact(S):
        sep += 1
check("n=5  posets with lambda_std >= 0 but S_P NOT PSD", sep > 0,
      "%d such posets -- the wrong oracle would have called every one of them a vacuity failure"
      % sep)

print("\n" + "=" * 78)
if FAIL:
    print("RED -- %d failing check(s): %s" % (len(FAIL), "; ".join(FAIL)))
    sys.exit(1)
print("GREEN -- every check passed.")
sys.exit(0)
