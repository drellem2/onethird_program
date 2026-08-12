#!/usr/bin/env python3
"""k2 -- ITEM 1: IS THE BAR ACTUALLY k-INDEPENDENT?  Derived, not assumed.

pm-onethird's derivation, quoted from the ticket:

    E_BK(f) = (1/(n-1)) * (1/2) * sum over ALL positions p of E[(f - f.tau_p)^2]
            = sum over classes of (2/(n-1)) * E[Var(f | C_i)]
            = (2/(n-1)) * <f, (kI - sum_i Pi_i) f>
    "THE CONSTANT 2/(n-1) IS THE SAME FOR EVERY CLASS REGARDLESS OF CLASS SIZE"

TWO ANSWERS AND THEY ARE NOT THE SAME ANSWER.

  k2.1-k2.2  HIS PREMISE IS RIGHT, AND EXACTLY RIGHT.  The constant is per-position, it does
             not carry a class size, and the resulting bound holds at EVERY admissible
             partition with the SAME 2/(n-1).  The bar (n-1)/(gamma n) therefore contains no
             k.  THE BAR IS k-INDEPENDENT.

  k2.3       HIS SECOND `=` IS A `>=`.  Within one class the swaps are disjoint but they are
             not one coordinate: the fiber is a CUBE of dimension |free positions|, and
             sum_p E Var_p(f) >= E Var(f | C_i) is Efron-Stein, an EQUALITY only when f is
             affine on the fiber.  This is mg-8bc7's equality case, per class.

  k2.4       AND THE SLACK IS ORIENTED.  The finest partition is the EQUALITY case, and there
             Q is the BK generator itself rescaled.  So the direction he needs is the direction
             in which the compression gives away nothing -- and that is the direction in which
             it also gives away the theorem.  (Priced in k3/k4.)
"""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib8d66 as K

ok = True
MAXN = 130         # exact PSD is O(N^3) in rationals; population is named at every table


def rnd_vals(N, seed):
    s = (seed * 48271 + 7) & 0x7FFFFFFF
    out = []
    for _ in range(N):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        out.append(Fraction((s % 23) - 11))
    return out


def population():
    for n in (3, 4):
        for lt in K.all_posets(n):
            yield n, lt, "exhaustive"
    for lt in K.sample_posets(5, 120, 3):
        yield 5, lt, "sample(120)"
    for lt in K.sample_posets(6, 60, 5):
        yield 6, lt, "sample(60)"


POP = [(n, lt, tag) for n, lt, tag in population()]

# --------------------------------------------------------------------------------------
K.banner("k2.1  THE ANCHOR: Q_finest IS the BK generator rescaled, as an EXACT MATRIX IDENTITY")
print("""
      Q_finest  =  (n-1) I - sum_{p=0}^{n-2} Pi_p  =  ((n-1)/2) (I - P_BK)

  Pi_p = (I + T_p)/2 on the legal swaps and I on the illegal ones, so sum_p Pi_p =
  ((n-1)/2) I + (1/2) sum_p T_p and (n-1) P_BK = sum_p T_p.  Checked ENTRYWISE in exact
  rationals -- not as an eigenvalue statement, and with no test function involved.
""")
bad, cnt, skipped = 0, 0, 0
by_n = {}
for n, lt, tag in POP:
    LEs = K.linear_extensions(n, lt)
    if len(LEs) < 2:
        continue
    if len(LEs) > MAXN:
        skipped += 1
        continue
    tgt = K.mat_scale(K.mat_sub(K.identity(len(LEs)), K.bk_matrix(LEs, n, lt)),
                      Fraction(n - 1, 2))
    if not K.mat_eq(K.q_matrix(LEs, n, lt, K.finest_partition(n)), tgt):
        bad += 1
    cnt += 1
    by_n[n] = by_n.get(n, 0) + 1
ok &= K.verdict(bad == 0,
                f"Q_finest == ((n-1)/2)(I - P_BK) entrywise at {cnt} posets "
                f"({', '.join(f'n={k}:{v}' for k, v in sorted(by_n.items()))})",
                f"{bad} failures; {skipped} posets skipped for |L(P)| > {MAXN}")

# --------------------------------------------------------------------------------------
K.banner("k2.2  HIS PREMISE, TESTED: the SAME constant 2/(n-1) at EVERY admissible partition")
print("""
  If the constant carried a class size, the operator inequality below would hold at some
  partitions and fail at others.  EXACT PSD of  Q_finest - Q_S  at every admissible S.
""")
bad, cnt, worst = 0, 0, None
for n, lt, tag in POP:
    LEs = K.linear_extensions(n, lt)
    if len(LEs) < 2 or len(LEs) > MAXN:
        continue
    fin = K.q_matrix(LEs, n, lt, K.finest_partition(n))
    for S in K.admissible_partitions(n):
        d = K.mat_sub(fin, K.q_matrix(LEs, n, lt, S))
        good, why = K.psd_exact(d)
        cnt += 1
        if not good:
            bad += 1
            worst = (n, K.pstr(S), why)
ok &= K.verdict(bad == 0,
                f"((n-1)/2)(I - P_BK) - Q_S is PSD at {cnt} (poset, partition) pairs, EXACTLY",
                f"{bad} failures" + (f"  worst {worst}" if worst else ""))
print("""
      => E_BK(f) >= (2/(n-1)) <f, Q_S f>   for EVERY f and EVERY admissible partition S,
         with ONE constant 2/(n-1) that does not depend on k or on any class's size.

      => THE BAR IS k-INDEPENDENT.  alpha_k must exceed (n-1)/(gamma n), which contains no k.
         pm-onethird's premise is CONFIRMED and it is confirmed in the strong form: it is not
         that the constant happens not to move, it is that the identity is a PER-POSITION sum.
""")

# --------------------------------------------------------------------------------------
K.banner("k2.3  BUT HIS SECOND `=` IS A `>=`, AND THE SLACK IS REAL")
strict = eq = 0
first = None
for n, lt, tag in POP:
    LEs = K.linear_extensions(n, lt)
    if len(LEs) < 2 or len(LEs) > MAXN:
        continue
    for t in range(3):
        v = rnd_vals(len(LEs), 101 * n + 7 * t + len(LEs))
        rhs = Fraction(n - 1, 2) * K.bk_energy(v, LEs, n, lt)
        for S in K.admissible_partitions(n):
            lhs = K.q_form(v, LEs, n, lt, S)
            if lhs > rhs:
                print(f"  WRONG DIRECTION at n={n} S={K.pstr(S)}: {lhs} > {rhs}")
                ok = False
            elif lhs < rhs:
                strict += 1
                if first is None and len(S) < n - 1:
                    first = (n, K.pstr(S), lhs, rhs)
            else:
                eq += 1
ok &= K.verdict(strict > 0,
                f"the inequality is STRICT at {strict} of {strict+eq} (f, S) instances",
                f"equality at {eq}")
if first:
    n, s, lhs, rhs = first
    print(f"  first strict instance: n={n}  S={s}   <f,Q_S f> = {lhs} < {rhs} = ((n-1)/2)E_BK(f)")
print("""
  WHY.  Within one class the swaps act on DISJOINT pairs, so the fiber is a CUBE of dimension
  d = #free positions -- not a single coordinate.  On that cube

      sum_{p in S} E Var_p(f)  =  sum_{B} |B| fhat(B)^2   >=   sum_{B != 0} fhat(B)^2
                                                          =    E Var(f | C_S)

  with equality iff f has no Fourier weight above degree 1 on the fiber.  That is exactly
  mg-8bc7's equality case ("(*) is an equality on linear statistics and an inequality in
  general"), read one class at a time.  pm-onethird's derivation writes `=` where the
  per-class step is `>=`.
""")

# --------------------------------------------------------------------------------------
K.banner("k2.4  the equality case, exhibited both ways")
n, lt = 5, K.tclose(5, {(0, 4)})
LEs = K.linear_extensions(n, lt)
S2 = K.coarsest_partition(n)
# (a) EQUALITY: a pair indicator -- degree <= 1 on every fiber (it sees ONE swap position)
x, y = K.incomparable(n, lt)[0]
fxy = K.pair_indicator(LEs, x, y)
ok &= K.verdict(K.q_form(fxy, LEs, n, lt, S2) == Fraction(n - 1, 2) * K.bk_energy(fxy, LEs, n, lt),
                f"[EQUALITY] pair indicator f_{x}{y} sits in the equality case at k=2")
# (b) STRICT: a product of two coordinates inside one fiber -- degree 2, must lose
S = S2[0]
lab, blocks = K.orbit_fibers(LEs, n, lt, S)
b = max(blocks, key=len)
freep = K.free_positions(LEs[b[0]], lt, S)
ok &= K.verdict(len(freep) >= 2, f"a fiber of dimension {len(freep)} >= 2 exists to plant in")
par = []
for i in range(len(LEs)):
    L = LEs[i]
    s = 1
    for p in freep:
        s *= 1 if L[p] < L[p + 1] else -1
    par.append(Fraction(s) if lab[i] == lab[b[0]] else Fraction(0))
lhs = K.q_form(par, LEs, n, lt, S2)
rhs = Fraction(n - 1, 2) * K.bk_energy(par, LEs, n, lt)
ok &= K.verdict(lhs < rhs, f"[STRICT] the degree-{len(freep)} parity on that fiber loses",
                f"{lhs} < {rhs}   ratio {K.frac(lhs/rhs)}")

K.banner("k2 VERDICT: THE BAR IS k-INDEPENDENT (premise CONFIRMED); the `=` is a `>=`")
sys.exit(0 if ok else 1)
