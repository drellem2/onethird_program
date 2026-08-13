"""mg-7ae5 / A3 — IS THE ABSENT STEP ABSENT ONLY IN THE SPARSE READING?

The ticket's clause 3: mg-0e8c restated the supply as eps_sup = d*n/(n+1),
LINEAR in the incomparability density, so mg-ac0c's 'the chain never closes' is
a DENSE-regime statement (mg-ac0c §3.1 lands that correction against itself).
The question here is whether the ABSENT step is likewise absent only in the
sparse reading.

The step's refutation is mg-d3c7's family, and that family is SPARSE:
d = 2/n (a0 §C5b, exact).  So the obvious hope is: restrict to the dense
regime, the refutation goes away, and the hole is a sparse-reading artefact.

This section prices that hope, in three parts:

  A  the family's own scaling, exactly: what ceiling does it impose at each of
     its densities, and what does closure REQUIRE at that same density?
  B  the exhaustive n <= 6 sweep of REAL failures on the architecturally
     required population, stratified by density — does the ceiling rise with a
     density floor, as P5 predicts?
  C  the verdict, including the thing that must not be read off it: a
     refutation removed is not a value supplied.
"""

from fractions import Fraction
import sys

from lib7ae5 import (poset_iter, linear_extensions, density, delta, delta1,
                     cut_verdict, p_matrix, eps_sup, eps0_required_cap,
                     eps_dem_chain13)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6

print("=" * 78)
print("mg-7ae5 / A3 — THE SPARSE READING, PRICED")
print("=" * 78)

# ------------------------------------------------------------------- A -----
print("""
A. mg-d3c7's FAMILY AGAINST THE CLOSURE REQUIREMENT, AT ITS OWN DENSITY

   The family (mg-d3c7 §4): chain c_1<...<c_{n-1} plus one isolated z,
   n = 2k+1, A = {z, c_1..c_{k-1}}.  Exactly:

       Delta_1 = (k+1)/((2k+1)k) = (n+1)/(n(n-1))        d = 2/n

   Closure at density d needs eps_0 >= eps_sup/2 = d*n/(2(n+1))  [mg-7564 §4's
   chain-free cap, so this binds ANY chain, including one nobody has written].
   At d = 2/n that requirement is exactly 1/(n+1).

   So at the family's own density the two bounds are:

       REQUIRED   eps_0 >= 1/(n+1)                    (closure, at THIS n)
       CEILING    eps_0 <= (n+1)/(n(n-1))             (the family refutes above)
""")
print("   %-6s %-9s %-14s %-14s %-14s %s"
      % ('n', 'd = 2/n', 'required >=', 'family ceiling', 'margin', 'window'))
for n in (7, 9, 15, 21, 51, 101, 1001):
    d = Fraction(2, n)
    req = eps0_required_cap(n, d)
    ceil = Fraction(n + 1, n * (n - 1))
    margin = ceil / req
    print("   %-6d %-9s %-14s %-14s %-14s %s"
          % (n, str(d), str(req), str(ceil), '%.6f' % float(margin),
             'open' if ceil > req else 'EMPTY'))
print("""
   THE MARGIN IS (n+1)^2 / (n^2 - n) AND IT TENDS TO 1.
   The refuting family is calibrated, to leading order, EXACTLY to the closure
   requirement at its own density: both are ~ d/2.  Restricting to the dense
   regime raises the ceiling and the requirement by the same factor.

   ⚠ AND THE ONE PLACE THE FAMILY IS SILENT: it has a member only at
   d = 2/n <= 2/7, so for a density floor above 2/7 it imposes NOTHING and the
   ceiling there comes from other witnesses — mg-3969's Cl. 6.1 witness sits at
   d = 7/15 with Delta_1 = 17/78.  §B measures that region exhaustively.""")

# mg-0e8c's line, for the record
# The check that decides whether §B's minimality restriction can be used to
# ARGUE AWAY the refutation.  It cannot, and this is where that is established
# rather than assumed: mg-d3c7's family must be ordinal-sum INDECOMPOSABLE, or
# minimality would delete it and the whole refutation with it.
print("\n   IS THE REFUTING FAMILY ITSELF EXCLUDED BY MINIMALITY? — checked, not assumed:")
for k in (3, 4, 5):
    n = 2 * k + 1
    rel = frozenset((i, j) for i in range(1, n) for j in range(i + 1, n))
    exts = linear_extensions(n, rel)
    md = min(delta1(n, rel, exts, kk) for kk in range(1, n))
    print("      k=%d (n=%d):  min Delta_1 over prefixes = %s  -> %s"
          % (k, n, md, 'DECOMPOSABLE' if md == 0 else 'INDECOMPOSABLE'))
print("""      So NO: the family is indecomposable at every k, minimality does not
      touch it, and the refutation it carries is not an artefact of the
      population minimality removes.  (§B shows the restriction DOES move the
      n <= 6 ceiling, 1/6 -> 17/78 — but not this family.)""")

print("""
   Against mg-0e8c's line: the family is below d ~ 2e-2 — the regime where the
   wall is ALREADY DOWN, proven, L4-free — only for n >= 100 (2/n <= 1/50).
   At every 15 <= n < 100, i.e. at every size a minimal counterexample can
   currently have below 100, the family sits in the DENSE, still-open regime.
   So 'the refutation lives where the wall is already down' is FALSE as stated;
   it is true only asymptotically, and the crossing point is n = 100 — the same
   arithmetic as row 8's primitive n >= 100 threshold (mg-0e8c §4).""")

# ------------------------------------------------------------------- B -----
print("\nB. THE EXHAUSTIVE SWEEP — real failures, stratified by density (n <= %d)" % NMAX)
print("""
   Population: EVERY prefix cut of every poset on n <= %d at which at least one
   side is non-chain — the ARCHITECTURALLY REQUIRED scope (mg-d3c7 §4), not the
   both-sides-non-chain restriction mg-3969 §6's 17/78 is measured on.
   A cut FAILS U_either when some side supplies a pair balanced inside it and
   NO such pair survives in P.
""" % NMAX)

fails = []          # (eps, d, n, k, rel)
cuts = req_scope = 0
for n in range(3, NMAX + 1):
    for rel in poset_iter(n):
        exts = linear_extensions(n, rel)
        pP = p_matrix(n, rel, exts)
        d = density(n, rel)
        for k in range(1, n):
            cuts += 1
            v = cut_verdict(n, rel, exts, k, pP)
            if v['scope'] == 'NEITHER':
                continue
            req_scope += 1
            if v['fails_either']:
                fails.append((v['eps'], d, n, k, rel))

print("   cuts swept                          %d" % cuts)
print("   in the required scope               %d" % req_scope)
print("   U_either FAILURES                   %d" % len(fails))
if fails:
    thin = min(fails)
    print("   thinnest failure                    Delta_1 = %s  at n = %d, d = %s"
          % (thin[0], thin[2], thin[1]))
    print("   ceiling on a UNIVERSAL eps_0 (n <= %d)  eps_0 <= %s = %.6f"
          % (NMAX, thin[0], float(thin[0])))

print("\n   THE CEILING AS A FUNCTION OF A DENSITY FLOOR (P5):\n")
print("   %-12s %-9s %-14s %-16s %s"
      % ('floor d >=', 'failures', 'ceiling', 'required at d', 'window'))
floors = [Fraction(0), Fraction(1, 10), Fraction(1, 5), Fraction(2, 7),
          Fraction(1, 3), Fraction(2, 5), Fraction(1, 2), Fraction(3, 5),
          Fraction(4, 5)]
prev = None
monotone = True
for d0 in floors:
    elig = [f for f in fails if f[1] >= d0]
    if not elig:
        print("   %-12s %-9d %-14s %-16s %s" % (str(d0), 0, '— none —', '', 'unrefuted'))
        continue
    c = min(e[0] for e in elig)
    # the requirement is evaluated in the n -> infinity limit, which is the
    # LOOSEST reading of the window (at finite n the requirement is smaller)
    req = d0 / 2
    if prev is not None and c < prev:
        monotone = False
    prev = c
    print("   %-12s %-9d %-14s %-16s %s"
          % (str(d0), len(elig), '%s = %.4f' % (c, float(c)),
             '%s = %.4f' % (req, float(req)),
             'open x%.2f' % float(c / req) if req and c > req
             else ('EMPTY' if req else 'open')))
print("\n   ceiling monotone in the density floor?   %s" % monotone)

print("\n   THE SAME SWEEP, RESTRICTED TO INDECOMPOSABLE POSETS")
print("   (minimality forbids a decomposable counterexample — a0 §B4 —")
print("    so a failure at a decomposable poset cannot bind Step 6)\n")
ind_fails = []
for (eps, d, n, k, rel) in fails:
    exts = linear_extensions(n, rel)
    if min(delta1(n, rel, exts, kk) for kk in range(1, n)) > 0:
        ind_fails.append((eps, d, n, k, rel))
print("   failures at INDECOMPOSABLE posets   %d of %d" % (len(ind_fails), len(fails)))
if ind_fails:
    t = min(ind_fails)
    print("   thinnest such failure               Delta_1 = %s at n = %d, d = %s"
          % (t[0], t[2], t[1]))

# ------------------------------------------------------------------- C -----
print("""
C. VERDICT ON THE SPARSE READING

   1. THE REFUTATION IS SPARSE — but only in the sense that its family's
      density is 2/n.  It has a member at EVERY density 2/n <= 2/7, so it
      refutes inside the dense regime too, and it is below mg-0e8c's 2e-2 line
      only at n >= 100.

   2. RESTRICTING TO THE DENSE REGIME DOES NOT OPEN A WINDOW, because the
      closure REQUIREMENT is linear in d for exactly the same reason the supply
      is: eps_0 >= d*n/(2(n+1)).  Both walls move together and the margin
      (n+1)^2/(n^2-n) tends to 1.

   3. AND THE THING THAT MUST NOT BE READ OFF ANY OF THIS.  Every number in
      this section is a CEILING — an upper bound established by exhibiting a
      failure.  A ceiling that rises when a density floor is imposed does not
      supply a positive eps_0; it removes a refutation.  (T) needs a LOWER
      bound, and no measurement can produce one: mg-3969 Cl. 5.1/5.2.  The
      sparse reading changes what is REFUTED.  It does not change what is
      ABSENT.""")
