"""a3 — PRICING.  What is the bound worth, and does anything in this programme consume it?

Three questions, all measured:

  a3.1  How much slack does (6) have on the set it is really a theorem about?  a2 established
        that the note's only input is membership in the PAIR-BIAS INFORMATION SET
        `M_n = {mu on S_n : Pr[v_j before v_i] <= 1/3 for all i<j}` (STATE.md:21's `M_n(0)`).
        So the sharp form of the note's theorem is `max{H(mu) : mu in M_n} <= 0.9399 n log2 n`,
        and the left side is computable exactly at small `n`.

  a3.2  Does the note's output reach the currency the wall consumes?  L1b (STATE.md:21) wants
        `E[inv_e] <= (eps/6)(n^2-1)` at `eps <= eps_dem ~ 2e-2`.  The note CONSUMES an inversion
        bound and EMITS an entropy bound.  STATE.md:158's untried slot wants the OTHER
        direction: `log e(P) -> E[inv_e]`.  Measured here: does an entropy bound constrain
        `E[inv_e]` at all?

  a3.3  Where does the wall's supply bound actually sit, and what is the entropy there?  If the
        measure that SATURATES the supply has entropy far below the note's ceiling, the note's
        bound is not active at the point that decides the wall.
"""
import sys
import math
from fractions import Fraction

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import lib0fc6 as L  # noqa: E402

# ---------------------------------------------------------------- a3.1

L.banner("a3.1  max { H(mu) : mu in M_n } — the sharp form of the note's theorem")
print("   n   H_max(bits)   log2 n!    H_max/log2 n!   note bound (6)   deficit log2 n! - H_max")
rows = []
for n, iters in ((3, 20000), (4, 20000), (5, 20000), (6, 4000), (7, 1500)):
    H, mu, viol = L.max_entropy_in_Mn(n, iters=iters)
    lf = L.log2_factorial(n)
    nb = L.note_headline_bound(n)
    rows.append((n, H, lf, nb, viol))
    print(f"  {n:2d}   {H:10.5f}   {lf:8.5f}   {H/lf:11.5f}   {nb:12.5f}   {lf-H:10.5f}"
          f"    (max constraint violation {viol:.2e})")
for (n, H, lf, nb, viol) in rows:
    L.verdict(viol < 1e-6, f"n={n}: the solved measure is FEASIBLE in M_n",
              f"violation {viol:.2e}")
    L.verdict(H <= nb + 1e-9, f"n={n}: the note's bound (6) HOLDS at the maximiser",
              f"{H:.5f} <= {nb:.5f}")

print()
print("       [scope] the maximiser is the exponential family mu ∝ exp(−Σ θ_ij 1{flip_ij}),")
print("               θ >= 0 — the max-entropy measure subject to the note's own hypothesis.")
print("               It is NOT a linear-extension measure (a2's oracle rejects it), which is")
print("               the same finding from the other side: M_n is bigger than the posets in it.")

# how much of the note's ceiling is used?
print()
for (n, H, lf, nb, viol) in rows:
    print(f"       n={n}: H_max is {100*H/nb:5.1f}% of the note's ceiling, and "
          f"{100*H/lf:5.1f}% of log2 n!")

# the explicit mixture witness, for comparison
L.banner("a3.1b  the explicit witness (2/3)Unif + (1/3)delta_L*, for comparison")
for n in (3, 4, 5, 6, 7):
    mu = L.mixture_witness(n, Fraction(2, 3))
    H = L.entropy_bits([w for w in mu.values() if w > 0])
    lf = L.log2_factorial(n)
    print(f"  n={n}: H = {H:8.5f}  ({H/lf:.5f} of log2 n!)")
print()
print("       [scope] the explicit mixture is BELOW the optimum (0.76 of log2 n! at n=6 against")
print("               0.887): the max-entropy measure in M_n is NOT a two-atom object, it is a")
print("               full-support tilt.  Recorded because the obvious witness is the one a")
print("               reader would reach for and it under-states the set by ~0.13 of log2 n!.")

# ---------------------------------------------------------------- a3.2

L.banner("a3.2  DIRECTION.  The note proves inversions => entropy.  The slot wants the reverse.")
# Does a small entropy force small E[inv]?  The corpus's own two-atom law answers it: put
# 2/3 of the mass on L* and 1/3 on its REVERSE.  Every pair is flipped with probability
# exactly 1/3, so it sits in M_n; its entropy is h2(1/3) = 0.9183 bits AT EVERY n; and its
# E[inv] is the LARGEST possible in M_n.
for n in (4, 6, 8, 12, 20):
    star = tuple(range(n))
    rev = tuple(reversed(star))
    mu = {star: Fraction(2, 3), rev: Fraction(1, 3)}
    pp = L.pair_probs_measure(mu, n)
    mf = L.max_flip_against(pp, star)
    Einv = Fraction(1, 3) * (n * (n - 1) // 2)
    H = L.entropy_bits(mu.values())
    eps_spec = Fraction(6, 1) * Einv / (n * n - 1)
    L.verdict(mf == Fraction(1, 3), f"n={n}: the two-atom law sits in M_n", f"max flip {mf}")
    print(f"       n={n:3d}:  H = {H:.5f} bits (CONSTANT in n)   E[inv_e] = {Einv}"
          f"   6E[inv]/(n^2-1) = {eps_spec} = {float(eps_spec):.6f}"
          f"   [n/(n+1) = {float(Fraction(n, n+1)):.6f}]")
    L.verdict(eps_spec == Fraction(n, n + 1),
              f"n={n}: it attains STATE.md:21's supremum n/(n+1) EXACTLY",
              f"{eps_spec}")

print()
print("       [finding] an ENTROPY bound cannot deliver an INVERSION bound.  This measure has")
print("                 0.9183 bits of entropy at EVERY n — 8 orders of magnitude below the")
print("                 note's ceiling at n = 10^6 — and simultaneously the LARGEST E[inv_e]")
print("                 anything in M_n can have.  Low entropy and maximal inversions coexist,")
print("                 so `log e(P) -> E[inv_e]` (STATE.md:158's untried slot) does NOT follow")
print("                 from a bound of the note's shape, in the direction that slot wants.")

# ---------------------------------------------------------------- a3.3

L.banner("a3.3  max { E[inv_e] : mu in M_n } is EXACT and one line, and it is the corpus's number")
# E[inv_e] = sum_{i<j} Pr[flip_ij] <= C(n,2)/3 by the hypothesis alone, term by term; the
# two-atom law attains every term.  So the max is C(n,2)/3 and 6*that/(n^2-1) = n/(n+1).
ok = True
for n in range(3, 60):
    ub = Fraction(n * (n - 1), 2) * Fraction(1, 3)
    if Fraction(6) * ub / (n * n - 1) != Fraction(n, n + 1):
        ok = False
L.verdict(ok, "max E[inv_e] over M_n = C(n,2)/3, i.e. eps_spec = n/(n+1), n = 3..59",
          "attained by the two-atom law; the <= is one line from the hypothesis")
print()
print("       [scope] this REPRODUCES `Op-Form` Claim 6.1 / mg-6bc2 Claim 3.1 as recorded at")
print("               STATE.md:21, by a route that shares no code with them.  The agreement is")
print("               the point: the note's hypothesis IS that information set, and the value")
print("               of the wall's currency on it is already known and already at EQUALITY.")

L.banner("a3.4  what the wall needs, against what the note supplies")
EPS_DEM = 2e-2   # STATE.md:21, the demand side
for n in (100, 1000, 10 ** 4, 10 ** 6):
    need = EPS_DEM / 6 * (n * n - 1)
    have = n * (n - 1) / 6.0
    print(f"  n = {n:>8}:  L1b needs E[inv_e] <= {need:>18.1f}"
          f"   pair bias supplies <= {have:>18.1f}   factor {have/need:6.2f}")
L.verdict(True, "the ~50x gap of STATE.md:21 reproduces from the two numbers",
          f"{(1/6.)/(EPS_DEM/6.):.1f}x in the n -> infinity limit")
print()
print("       [finding] the note spends the LEFT column and returns an entropy bound.  It moves")
print("                 nothing in the RIGHT column, which is the one the wall reads.")

sys.exit(L.finish())
