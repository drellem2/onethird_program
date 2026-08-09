"""s1 — THE EXHAUSTIVE CENSUS, n <= 6.

Population: EVERY poset on {0..n-1} for which the identity is a linear extension,
n = 2..6.  Nothing here is a sample and nothing here is a family: every maximum printed in
this file is a maximum over a fully enumerated population, and its size is printed beside it.

What it measures, in the ticket's terms: the sweep's loss, decomposed, as a function of n.
"""

from fractions import Fraction as F
import sys
import time

from lib51f4 import (all_posets, measure, floor_msharp, floor_footrule, gap_greater,
                     mu_pref_exact_upper)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6


def hdr(t):
    print()
    print("=" * 104)
    print(t)
    print("=" * 104)


ALL = {}
for n in range(2, NMAX + 1):
    t0 = time.time()
    ps = all_posets(n)
    rs = [measure(p, iters=50) for p in ps]
    ALL[n] = rs
    print("n=%d: %d posets, %d primitive   (%.1fs)"
          % (n, len(ps), sum(1 for r in rs if r.primitive), time.time() - t0))
    sys.stdout.flush()


def prim(n):
    return [r for r in ALL[n] if r.primitive]


# --------------------------------------------------------------------------------- 1
hdr("S1.1  [FORMALITY] REPRODUCTION OF mg-28ff's CONSTANTS ON AN INDEPENDENT INSTRUMENT")
print("Pre-answered by my ticket body (PREDICTIONS.md H1): these are a CONTROL on lib51f4,")
print("not a finding.  The transport here comes from a DOWN-SET dynamic program, not from")
print("enumerating n! permutations, so agreement is a real cross-check of two algorithms.")
print()
print("  n  | posets | primitive |   c_true   |     c#     |     f*     ")
print(" ----+--------+-----------+------------+------------+------------")
for n in range(2, NMAX + 1):
    pr = prim(n)
    print("  %d  | %6d | %9d | %10.6f | %10.6f | %10.6f"
          % (n, len(ALL[n]), len(pr),
             float(max(r.c_true_hi for r in pr)),
             float(max(r.c_sharp_hi for r in pr)),
             float(max(r.f_hi for r in pr))))
tot = sum(len(ALL[n]) for n in range(2, NMAX + 1))
totp = sum(len(prim(n)) for n in range(2, NMAX + 1))
print()
print("  totals over n = 2..%d:  %d posets, %d primitive   "
      "(mg-28ff reports 5230 and 4377)" % (NMAX, tot, totp))
print()
print("  NOT REPRODUCED, DELIBERATELY (PREDICTIONS.md E8): the L2 census — mg-28ff's 1037")
print("  primitive posets exhibiting L2's first disjunct and 3340 where it fails, and the")
print("  1032-vs-1037 discrepancy it left open.  Deciding `mu_pref == gamma` exactly means")
print("  comparing two algebraic numbers, my first attempt at it was wrong (it asked whether")
print("  a RATIONALISED mu_pref landed inside a 2^-49-wide bracket, and answered 53), and a")
print("  number that is already established on two instruments is not worth a third that")
print("  might be broken.  The cone penalty mu_pref/gamma in S1.4 is the quantitative form of")
print("  the same question and is what this ticket actually uses.")


# --------------------------------------------------------------------------------- 2
hdr("S1.2  THE FLOOR — c#(P) >= Delta_P - gamma/2 AT EVERY POSET, EXACT, 0 EXCEPTIONS")
print("The whole content of the floor is `gamma <= mu_pref`, because")
print("    c# - (Delta - gamma/2) = [ sweep(mu,Delta) - 2 Delta gamma + gamma^2 ] / (2 gamma)")
print("and with sweep(mu,Delta) = mu(2Delta-mu) the bracket is q(gamma) where")
print("    q(t) = t^2 - 2 Delta t + mu(2Delta-mu) = (t - mu)(t - (2Delta - mu)) >= 0 for t <= mu,")
print("while in the other branch sweep = Delta^2 and q(t) = (t-Delta)^2 >= 0 outright.")
print("So the machine check is ONE EXACT DECISION PER POSET — `gamma > mu_pref` must be")
print("FALSE — and it involves no bracket and no float.")
print()
viol = 0
checked = 0
for n in range(2, NMAX + 1):
    for r in prim(n):
        checked += 1
        if gap_greater(r.P, r.mu):        # would mean gamma > mu_pref: impossible
            viol += 1
print("  `gamma > mu_pref` at %d of %d primitive posets n <= %d   (exact; 0 is the theorem)"
      % (viol, checked, NMAX))
print()
print("  MUTATION CONTROL (PREDICTIONS.md E3b): the floor with the sign flipped,")
print("  Delta_P + gamma/2, must FAIL somewhere or the checking code cannot discriminate.")
bad = 0
for n in range(2, NMAX + 1):
    for r in prim(n):
        if r.c_sharp_lo < r.dmax + r.gamma_lo / 2:
            bad += 1
print("  c# < Delta_P + gamma/2 at %d of %d — the mutant is violated, so the check bites."
      % (bad, checked))
print()
print("  n  |  max c#   | max floor | floor at c#'s OWN argmax | floor/c# there | "
      "median floor/c#")
print(" ----+-----------+-----------+--------------------------+----------------+----------------")
for n in range(3, NMAX + 1):
    pr = prim(n)
    am = max(pr, key=lambda r: r.c_sharp_hi)
    mf = max(float(floor_msharp(r)) for r in pr)
    ratios = sorted(float(floor_msharp(r) / r.c_sharp_hi) for r in pr)
    med = ratios[len(ratios) // 2]
    print("  %d  | %9.6f | %9.6f | %24.6f | %14.4f | %16.4f"
          % (n, float(am.c_sharp_hi), mf, float(floor_msharp(am)),
             float(floor_msharp(am) / am.c_sharp_hi), med))
print()
print("  READ THIS COLUMN, NOT THE HEADLINE: at n = %d the floor already accounts for" % NMAX)
pr = prim(NMAX)
am = max(pr, key=lambda r: r.c_sharp_hi)
print("  %.1f%% of c#.  Even a PERFECT monotone test vector — one attaining mu_pref = gamma,"
      % (100 * float(floor_msharp(am) / am.c_sharp_hi)))
print("  which is exactly L2's first disjunct — leaves c# at %.4f there."
      % float(floor_msharp(am)))


# --------------------------------------------------------------------------------- 3
hdr("S1.3  ROUTE (F) HAS NO COMPARABLE FLOOR")
print("From `leak(A_k) >= gamma k(n-k)/n` (the centred prefix indicator is a test vector),")
print("    M >= rho_n gamma   with rho_n = (n^2-1)/(6 floor(n^2/4)) -> 2/3,")
print("so f* >= rho_n^2 gamma / 2.  That floor VANISHES with gamma instead of rising to 1.")
print()
print("  n  | rho_n   | max over primitive of f*'s floor | max f*  ")
print(" ----+---------+----------------------------------+---------")
for n in range(3, NMAX + 1):
    pr = prim(n)
    rho = F(n * n - 1, 6 * (n * n // 4))
    mf = max(float(floor_footrule(n, r.gamma_lo)) for r in pr)
    print("  %d  | %7.5f | %32.6f | %7.4f"
          % (n, float(rho), mf, float(max(r.f_hi for r in pr))))
print()
print("  So the two routes do NOT share a degrading factor: (M#) carries a floor that rises")
print("  toward 1 and (F) does not.  The common object is the population, not the mechanism.")


# --------------------------------------------------------------------------------- 4
hdr("S1.4  THE SWEEP'S LOSS, DECOMPOSED — WHAT EACH ROUTE THROWS AWAY")
print("Pointwise, by definition,   c#(P) = Lam_M(P) * c_true(P)   and   f*(P) = Lam_F(P)^2 * c_true(P)")
print("with  Lam_M = sweep(mu,Delta)/Phi*_pref^2   THE SWEEP'S LOSS (Cauchy-Schwarz + the")
print("degree rounding + the cone penalty), and  Lam_F = M/Phi*_pref  THE MEDIANT LOSS (the")
print("m-weighted MEAN of the prefix-conductance profile over its MINIMUM).")
print()
print("  n  |  max Lam_M  | max Lam_F | max spread phi_max/phi_min | max cone penalty mu/gamma")
print(" ----+-------------+-----------+----------------------------+--------------------------")
for n in range(3, NMAX + 1):
    pr = prim(n)
    lm = max(float(r.c_sharp_lo / r.c_true_hi) for r in pr)
    lf = max(float(r.M / r.phistar) for r in pr)
    sp = max(float(r.phimax / r.phistar) for r in pr)
    cp = max(float(r.mu / r.gamma_hi) for r in pr)
    print("  %d  | %11.3f | %9.3f | %26.3f | %25.4f" % (n, lm, lf, sp, cp))
print()
print("  The loss is NOT converging and it is NOT the thing that has to converge: what the")
print("  architecture consumes is the PRODUCT Lam * c_true, and c_true falls exactly where")
print("  the loss rises.  A uniform bound on the loss is neither available nor needed.")


# --------------------------------------------------------------------------------- 5
hdr("S1.5  THE TWO ROUTES FAIL IN OPPOSITE REGIMES")
for n in range(4, NMAX + 1):
    pr = prim(n)
    a = max(pr, key=lambda r: r.c_sharp_hi)
    b = max(pr, key=lambda r: r.f_hi)
    print("  n=%d" % n)
    for tag, r in (("argmax c#", a), ("argmax f*", b)):
        print("     %-10s gamma=%.6f  Delta=%.5f  Phi*=%.5f  M=%.5f | c_true=%.4f "
              "c#=%.4f f*=%.4f  min=%.4f   %s"
              % (tag, float(r.gamma_lo), float(r.dmax), float(r.phistar), float(r.M),
                 float(r.c_true_hi), float(r.c_sharp_hi), float(r.f_hi),
                 float(min(r.c_sharp_hi, r.f_hi)), list(r.P.rel_pairs())))
print()
pr = prim(NMAX)
xs = [(float(r.c_sharp_hi), float(r.f_hi)) for r in pr]
mx = sum(x for x, _ in xs) / len(xs)
my = sum(y for _, y in xs) / len(xs)
cov = sum((x - mx) * (y - my) for x, y in xs)
vx = sum((x - mx) ** 2 for x, _ in xs) ** 0.5
vy = sum((y - my) ** 2 for _, y in xs) ** 0.5
print("  Pearson correlation of c# and f* over the %d primitive posets at n=%d:  %+.4f"
      % (len(pr), NMAX, cov / (vx * vy)))
hi = [r for r in pr if r.c_sharp_hi > F(4, 5) and r.f_hi > F(4, 5)]
print("  primitive posets at n=%d with BOTH c# > 0.8 AND f* > 0.8:  %d of %d"
      % (NMAX, len(hi), len(pr)))
print("  (PREDICTIONS.md E4: a mechanism, not a correlation — a poset where c# > f*:")
w1 = max(pr, key=lambda r: r.c_sharp_hi - r.f_hi)
w2 = max(pr, key=lambda r: r.f_hi - r.c_sharp_hi)
print("     c# %.4f  f* %.4f  gamma %.5f   %s" %
      (float(w1.c_sharp_hi), float(w1.f_hi), float(w1.gamma_lo), list(w1.P.rel_pairs())))
print("   and one where f* > c#:")
print("     c# %.4f  f* %.4f  gamma %.5f   %s)" %
      (float(w2.c_sharp_hi), float(w2.f_hi), float(w2.gamma_lo), list(w2.P.rel_pairs())))


# --------------------------------------------------------------------------------- 6
hdr("S1.6  THE DISJUNCTION CONSTANT — THE OBJECT THE ARCHITECTURE ACTUALLY CONSUMES")
print("c_or(n) = max over PRIMITIVE posets of min(c#(P), f*(P)).  Legitimate because (M#)")
print("and (F) are each separately sufficient for C_3^(III) = 1 at a poset: the theorem needs")
print("ONE route to fire there, not both.  Scope: primitive, exhaustive, n <= %d." % NMAX)
print()
print("  n  | primitive |  c_true  |    c#    |    f*    |  c_or = max min(c#,f*) | c_or/c_true")
print(" ----+-----------+----------+----------+----------+------------------------+------------")
prev = None
for n in range(3, NMAX + 1):
    pr = prim(n)
    ct = max(r.c_true_hi for r in pr)
    cs = max(r.c_sharp_hi for r in pr)
    fs = max(r.f_hi for r in pr)
    co = max(min(r.c_sharp_hi, r.f_hi) for r in pr)
    d = "" if prev is None else "   (%+0.4f)" % (float(co) - prev)
    prev = float(co)
    print("  %d  | %9d | %8.6f | %8.6f | %8.6f | %22.6f | %10.4f%s"
          % (n, len(pr), float(ct), float(cs), float(fs), float(co), float(co / ct), d))
print()
am = max(prim(NMAX), key=lambda r: min(r.c_sharp_hi, r.f_hi))
print("  c_or's argmax at n=%d: %s" % (NMAX, list(am.P.rel_pairs())))
print("     gamma=%.6f Delta=%.5f Phi*=%.6f M=%.6f c_true=%.4f c#=%.4f f*=%.4f"
      % (float(am.gamma_lo), float(am.dmax), float(am.phistar), float(am.M),
         float(am.c_true_hi), float(am.c_sharp_hi), float(am.f_hi)))


# --------------------------------------------------------------------------------- 7
hdr("S1.7  WHY THE DISJUNCTION SURVIVES — THE TWO LOSSES ARE ANTI-CORRELATED IN gamma")
print("This is the mechanism behind S1.6, and it is a statement about the SWEEP, not about")
print("either route.  The sweep's loss has two parts that respond to gamma in OPPOSITE ways:")
print()
print("  * THE CONE PENALTY  mu_pref/gamma  — the price of insisting the test vector be")
print("    monotone.  It is what makes c# exceed its floor, so it is the only part of (M#)")
print("    a better vector could ever attack.")
print("  * THE MEDIANT LOSS  M/Phi*_pref    — the m-weighted MEAN of the prefix-conductance")
print("    profile over its MINIMUM.  It is the whole of (F)'s loss.")
print()
print("Binned by gamma over the %d primitive posets at n = %d (EXHAUSTIVE):" % (len(prim(NMAX)), NMAX))
print()
print("   gamma bin      | count | max mu/gamma | max M/Phi* | max c# | max f* | max min(c#,f*)")
print("  ---------------+-------+--------------+------------+--------+--------+---------------")
edges = [F(0), F(1, 20), F(1, 10), F(1, 5), F(3, 10), F(1, 2), F(2)]
for a, b in zip(edges, edges[1:]):
    sel = [r for r in prim(NMAX) if a <= r.gamma_lo < b]
    if not sel:
        continue
    print("   [%.3f,%.3f) | %5d | %12.4f | %10.3f | %6.4f | %6.4f | %13.4f"
          % (float(a), float(b), len(sel),
             max(float(r.mu / r.gamma_hi) for r in sel),
             max(float(r.M / r.phistar) for r in sel),
             max(float(r.c_sharp_hi) for r in sel),
             max(float(r.f_hi) for r in sel),
             max(float(min(r.c_sharp_hi, r.f_hi)) for r in sel)))
print()
print("  The cone penalty collapses to 1 exactly where the mediant loss explodes.  A poset")
print("  with a very thin bottleneck has a Fiedler vector that IS monotone (L2's first")
print("  disjunct holds there), which pins c# to its floor Delta - gamma/2 < 1; and a poset")
print("  whose Fiedler vector is badly non-monotone has a fat profile, which keeps M/Phi*")
print("  small.  Neither statement is proved here.  Both are exhaustive at n <= %d." % NMAX)
