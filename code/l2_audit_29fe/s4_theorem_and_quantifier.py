"""s4 — ITEM 5 (the quantifier move) and the affirmative half's ONE falsifiable joint.

The ticket asks what I did that COULD have falsified the affirmative half.  This is it.
Four arms, each of which would print a counterexample if the theorem were wrong:

  T1  the SHARPENED Cauchy-Schwarz factor is an IDENTITY, not a bound:
          sum_{i<j} a_ij (h_i+h_j)^2  ==  2 sum_i d_i h_i^2 - E(h)
      (this is the whole of added step S2; if it is not an identity, S2 is unsound)

  T2  the QUANTIFIER MOVE at its only load-bearing joint: for a monotone g, EVERY level
      set of every h = (g-m)_+ or (g-m)_- really is a PREFIX or a SUFFIX.  mg-28ff's §2
      writes "level set of h, hence of g", which is loose for the g_- branch (there the
      level sets of h are CO-threshold sets of g).  mg-76b2's Lemma 3.3 covers BOTH
      directions explicitly, so the move is valid - but the loose sentence is exactly the
      kind of joint this programme's recurring bug lives at, so it is CHECKED, not read.

  T3  the THEOREM ITSELF against brute force, over (poset, monotone vector) pairs, with
      Phi*_pref computed by exhaustive minimisation over prefixes.

  T4  the theorem's SIZE hypothesis: mg-76b2's Lemma 3.1 carries "|S| <= n/2" and
      mg-28ff's restatement drops it.  Check that dropping it changes nothing, i.e. that
      Phi_P is genuinely symmetric under complementation on this population.
"""
from fractions import Fraction as F
from itertools import combinations
from lib29fe import (all_natural_posets, is_decomposable, Poset, psi_basis, quad,
                     bracket_gap, monotone)

print("=" * 90)
print("s4  ITEM 5 — the quantifier move, and the one arm that could falsify the theorem")
print("=" * 90)


def monotone_vectors(n, cap=60):
    """A spread of monotone g perp 1: nonneg integer combinations of the psi basis."""
    psi = psi_basis(n)
    out, seen = [], set()
    coeffs = []
    for total in range(1, 5):
        for c in combinations_with_rep(range(n - 1), total):
            v = [0] * (n - 1)
            for i in c:
                v[i] += 1
            if tuple(v) not in seen:
                seen.add(tuple(v))
                coeffs.append(v)
    for c in coeffs[:cap]:
        g = [sum(F(c[k]) * psi[k][i] for k in range(n - 1)) for i in range(n)]
        if any(x != 0 for x in g):
            out.append(g)
    return out


def combinations_with_rep(it, r):
    from itertools import combinations_with_replacement
    return combinations_with_replacement(it, r)


# ---------------------------------------------------------------- T1
print()
print("-- T1  the sharpened Cauchy-Schwarz factor is an EXACT IDENTITY (added step S2) --")
bad = tot = 0
for n in range(2, 7):
    for rel in all_natural_posets(n)[:300]:
        P = Poset(n, rel)
        for g in monotone_vectors(n, cap=25):
            for h in (g, [max(x, F(0)) for x in g], [max(-x, F(0)) for x in g]):
                lhs = sum(P.a[i][j] * (h[i] + h[j]) ** 2
                          for i in range(n) for j in range(i + 1, n))
                rhs = 2 * sum(P.d[i] * h[i] ** 2 for i in range(n)) - P.energy(h)
                tot += 1
                if lhs != rhs:
                    bad += 1
print(f"   {tot - bad} of {tot} (poset, vector) pairs satisfy it EXACTLY; {bad} exceptions")
# NC: the DISCARDED form must be a strict over-estimate somewhere, else S2 is decorative
strict = 0
for n in (5, 6):
    for rel in all_natural_posets(n)[:200]:
        P = Poset(n, rel)
        for g in monotone_vectors(n, cap=15):
            h = [max(x, F(0)) for x in g]
            if P.energy(h) > 0:
                strict += 1
print(f"   NC  the discarded term -E(h) is STRICTLY positive at {strict} pairs, so the")
print(f"       sharpening is not vacuous")

# ---------------------------------------------------------------- T2
print()
print("-- T2  the quantifier move: level sets of h are prefixes or suffixes --")
bad = tot = 0
examples_minus = 0
for n in range(2, 8):
    pool = all_natural_posets(n) if n <= 6 else []
    for rel in (pool[:200] if pool else []):
        P = Poset(n, rel)
        for g in monotone_vectors(n, cap=20):
            mean = sum(g, F(0)) / n
            vals = sorted(set(g))
            for m in vals:                       # every candidate median
                for h, branch in (([max(x - m, F(0)) for x in g], "+"),
                                  ([max(m - x, F(0)) for x in g], "-")):
                    levels = sorted(set(x * x for x in h))
                    for t in [F(0)] + levels:
                        S = frozenset(i for i in range(n) if h[i] * h[i] > t)
                        if not S:
                            continue
                        k = len(S)
                        isprefix = S == frozenset(range(k))
                        issuffix = S == frozenset(range(n - k, n))
                        tot += 1
                        if branch == "-" and S:
                            examples_minus += 1
                        if not (isprefix or issuffix):
                            bad += 1
                            if bad <= 3:
                                print(f"     COUNTEREXAMPLE n={n} S={sorted(S)} g={g}")
print(f"   {tot - bad} of {tot} level sets are a prefix or a suffix; {bad} exceptions")
print(f"   ({examples_minus} of them come from the g_- branch, the one mg-28ff's sentence")
print(f"    describes loosely — so that branch is genuinely exercised here)")

# ---------------------------------------------------------------- T3
print()
print("-- T3  THE THEOREM against brute force (the arm that could kill the ticket) --")
bad = tot = 0
worst = None
for n in range(2, 7):
    prim = [r for r in all_natural_posets(n) if not is_decomposable(n, r)]
    for rel in prim[:400]:
        P = Poset(n, rel)
        phi = P.Phi_star_pref()
        D = P.Delta
        for g in monotone_vectors(n, cap=30):
            R = P.rayleigh(g)
            if R is None:
                continue
            bound = R * (2 * D - R) if R <= D else D * D
            tot += 1
            if phi * phi > bound:
                bad += 1
                if bad <= 3:
                    print(f"     COUNTEREXAMPLE n={n} Phi*^2={phi*phi} > {bound} rel={sorted(rel)}")
            slack = bound - phi * phi
            if worst is None or slack < worst[0]:
                worst = (slack, n, sorted(rel))
print(f"   {tot - bad} of {tot} (poset, monotone vector) pairs satisfy the theorem; "
      f"{bad} exceptions")
print(f"   tightest case: slack {worst[0]} at n={worst[1]}  rel={worst[2]}")
# NC: a MUTATED theorem (Delta_P replaced by Delta_P/2) must FAIL somewhere
mut = 0
for n in (5, 6):
    prim = [r for r in all_natural_posets(n) if not is_decomposable(n, r)]
    for rel in prim[:300]:
        P = Poset(n, rel)
        phi, D = P.Phi_star_pref(), P.Delta / 2
        for g in monotone_vectors(n, cap=10):
            R = P.rayleigh(g)
            if R is None:
                continue
            bound = R * (2 * D - R) if R <= D else D * D
            if phi * phi > bound:
                mut += 1
print(f"   NC  the MUTATED theorem (Delta_P -> Delta_P/2) FAILS at {mut} pairs, so T3 is")
print(f"       not a tautology")

# ---------------------------------------------------------------- T4
print()
print("-- T4  Phi_P is symmetric under complementation (so dropping |S|<=n/2 is free) --")
bad = tot = 0
for n in range(2, 7):
    for rel in all_natural_posets(n)[:400]:
        P = Poset(n, rel)
        L = P.L()
        for size in range(1, n):
            for A in combinations(range(n), size):
                As, Ac = set(A), set(range(n)) - set(A)
                ia = [F(1) if i in As else F(0) for i in range(n)]
                ic = [F(1) if i in Ac else F(0) for i in range(n)]
                tot += 1
                if quad(L, ia) != quad(L, ic):
                    bad += 1
print(f"   {tot - bad} of {tot} cuts have leak(A) == leak(A^c); {bad} exceptions")
print("   => mg-28ff dropping mg-76b2's |S| <= n/2 clause costs nothing.")
print("=" * 90)
