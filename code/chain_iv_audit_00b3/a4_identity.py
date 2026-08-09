"""a4 — THE HEADLINE, CHECKED SEPARATELY: `CHAIN (IV) IS CHAIN (II)`.

The ticket: `Verify the algebra rather than the narrative.`  So the narrative is set aside
and three things are checked in order:

  (I1) the identity  c = (1 - C3gap*gap)/(1-gap)  — and what it does and does not assert
  (I2) the demand algebra  eps_dem^(IV) = eps_leak/C3gap = eps_dem^(II), re-derived here
       from mg-76b2's sec 6 formulae and not from mg-81ff's two lines, with a live
       negative control
  (I3) THE JOINT: the algebra is POINTWISE in the one unknown.  Chains are quantified over
       a CLASS.  Does the equality survive that quantifier?
"""

from fractions import Fraction as F

import sweep as S

LEAK = F(1, 5)
SPEC = F(1, 50)

print("=" * 78)
print("a4 — IS CHAIN (IV) CHAIN (II)?")
print("=" * 78)

print("""
------------------------------------------------------------------------------
(I1) THE IDENTITY — TRUE, AND TRUE BY SUBSTITUTION
------------------------------------------------------------------------------
     C3gap := min_k Q_k / gap        c := (1 - min_k Q_k)/(1 - gap)
  =>  c = (1 - C3gap*gap)/(1 - gap)          because C3gap*gap IS min_k Q_k.

  So the identity is an ALGEBRAIC REARRANGEMENT of two definitions, and checking it at
  90 654 posets checks the arithmetic, not the mathematics.  mg-81ff says as much (`the
  identity is FORMAL`), and it is right, but its sec 0.4 presents `verified as an exact
  rational identity at all 90 654 primitive posets n <= 7` as the part that is NEW.  The
  substance of sec 4 is not this line; it is (I2).  Checked anyway, on my own sweep:""")
bad = tot = 0
for n in (5, 6, 7):
    for r in S.informative(S.load(n)):
        gapq = F(r[1]).limit_denominator(10 ** 9)
        tot += 1
        if (1 - (r[2] / gapq) * gapq) / (1 - gapq) != (1 - r[2]) / (1 - gapq):
            bad += 1
print("     %d informative posets n = 5..7: %d failures" % (tot, bad))
print("""
  WHAT IS GENUINELY THERE, AND IS THE REAL CONTENT: `c` and `C3gap` are two normalisations
  of ONE measured quantity, min_k Q_k — one divided by the gap, the other subtracted from
  1 and divided by lambda_std.  Nobody can improve one without moving the other.  That
  claim is correct and it is the useful half of mg-81ff sec 4.""")

print("""
------------------------------------------------------------------------------
(I2) THE DEMAND ALGEBRA — re-derived from mg-76b2 sec 6, not from mg-81ff
------------------------------------------------------------------------------
  mg-76b2 sec 6's table, row (IV):  Phi <= 1 - c(1-eps_spec),  eps_dem = 1 - (1-eps_leak)/c
  mg-76b2 sec 6, gap-form of (II):  eps_dem = eps_leak / C3

  Under chain (II)'s hypothesis min_k Q_k <= g*gap, the worst c on {gap <= e} is
  (1 - g*e)/(1 - e)  [it is decreasing in gap for g >= 1, so the worst is at gap = e].
  Put e = eps_dem and solve:

      1 - (1-L)(1-e)/(1 - g e) = e
      (1 - g e) - (1-L)(1-e)   = e(1 - g e)
      1 - g e - 1 + e + L - L e = e - g e^2
      L(1 - e)                  = g e (1 - e)
      e = L/g                                              [1 - e != 0]

  MY DERIVATION AGREES WITH mg-81ff's.  Checked against both chains' own formulae:""")
print("       g          eps_dem^(II)   c = (1-g e)/(1-e)   eps_dem^(IV)   EQUAL?")
for g in (F(1), F(3, 2), F(2), F(2386087, 10 ** 6), F(3075271, 10 ** 6),
          F(4875800, 10 ** 6), F(5), F(10), F(20)):
    e = LEAK / g
    c = (1 - g * e) / (1 - e)
    iv = 1 - (1 - LEAK) / c
    print("     %8.4f      %.6f       %.6f          %.6f       %s"
          % (float(g), float(e), float(c), float(iv), iv == e))
print("""
  NEGATIVE CONTROL — the algebra must be able to FAIL.  A chain (IV) mis-derived so that
  it DOES pay a Cheeger square delivers Phi <= sqrt(2(1 - c(1-eps))) and its demand solves
  differently; if the equality above were vacuous arithmetic this would reproduce it too:""")
for g in (F(1), F(3, 2), F(2), F(5), F(10)):
    e = LEAK / g
    c = (1 - g * e) / (1 - e)
    good = 1 - (1 - LEAK) / c
    bad_ = 1 - (1 - LEAK * LEAK / 2) / c
    print("     g=%5.2f   correct eps_dem = %9.6f   square-paying variant = %9.6f   %s"
          % (float(g), float(good), float(bad_),
             "differs (good)" if bad_ != good else "*** IDENTICAL — CHECK IS VACUOUS"))

print("""
------------------------------------------------------------------------------
(I3) THE JOINT: THE ALGEBRA IS POINTWISE.  THE CHAINS ARE QUANTIFIED OVER A CLASS.
------------------------------------------------------------------------------
  (I2) fixes ONE value of the one unknown and shows the two chains demand the same thing
  of it.  That is correct and I confirm it.  But neither chain is invoked at a value; each
  is invoked over the class {gap <= eps_spec}, where the constants are

      g(e) := max C3gap over {gap <= e}          c(e) := min c over {gap <= e}

  and the step `the worst c is (1 - g e)/(1 - e)` needs the worst C3gap to be attained AT
  gap = e.  It is not.  Measured on the exhaustive population:""")
rows = {n: S.informative(S.load(n)) for n in (6, 7)}
print("      n     e      g(e)    argmax's own gap   (1-g e)/(1-e)   c(e) ACTUAL   slack")
for n in (6, 7):
    for e in (0.20, 0.15, 0.10, 0.08):
        sub = [r for r in rows[n] if r[1] <= e]
        if len(sub) < 2:
            continue
        amax = max(sub, key=S.C3gap_of)
        g = S.C3gap_of(amax)
        c = min(S.c_of(r) for r in sub)
        pred = (1 - g * e) / (1 - e)
        print("      %d   %.2f  %7.4f       %.6f          %.6f      %.6f    +%.6f"
              % (n, e, g, amax[1], pred, c, c - pred))
print("""
  THE WORST C3gap IS NEVER AT THE CAP: at n = 7 it is attained at gap = 0.054196 (the
  staircase S_7) for every cap from 0.20 down to 0.06.  So the chain (II) translation
  UNDERSTATES the c that chain (IV) actually gets, and the two demands are NOT equal on a
  class — they are ordered.  Evaluated self-consistently at each n's own fixed point:""")
print("      n    chain (II): eps_dem = L/g    chain (IV): eps_dem = 1-(1-L)/c(e)   ratio")
for n in (6, 7):
    g = max(S.C3gap_of(r) for r in rows[n])
    e2 = float(LEAK) / g
    sub = [r for r in rows[n] if r[1] <= e2]
    gg = max(S.C3gap_of(r) for r in sub)
    assert abs(gg - g) < 1e-9, "the fixed point must be self-consistent"
    c = min(S.c_of(r) for r in sub)
    e4 = 1 - 0.8 / c
    print("      %d          %.6f                    %.6f                  %.4fx"
          % (n, e2, e4, e4 / e2))
print("""
  >>> SO `CHAIN (IV) BUYS NO WEAKER DEMAND THAN CHAIN (II)` IS A `>=`, NOT AN `=`, AND ON
      THE MEASURED POPULATION IT IS STRICT: chain (IV) tolerates 1.23x (n=6) and 1.42x
      (n=7) the eps_spec that chain (II) does.  The direction is the SAFE one — mg-81ff's
      conclusion is conservative against chain (IV), not optimistic — so this is a
      qualification of the headline and not a defect in it.

  >>> AND a3's STAIRCASE MAKES THE SAME POINT WITHOUT A LIMIT ARGUMENT.  On the class
      {gap <= eps_spec} that Step 2 actually supplies:
        chain (II) needs a universal g with min_k Q_k <= g*gap, and closing needs
          g <= eps_leak/eps_spec = 10.  S_25 is primitive, has gap = 0.0043572625 <= 1/50
          and forces g >= 10.1654, EXACTLY.  So chain (II)'s route does not close there.
        chain (IV) needs c >= 40/49 = 0.816327.  S_25 gives c = 0.9598890, and its
          per-poset closing condition min_k Q_k = 300/6773 <= 1/5 holds with 4.5x to spare.
      ONE EXACT WITNESS, IN THE REGIME, ON WHICH ONE CHAIN CLOSES AND THE OTHER DOES NOT.
      mg-81ff names the mechanism correctly — chain (II)'s bound is RELATIVE and chain
      (IV)'s ABSOLUTE — but files it as `an advantage in PROVABILITY, not in the constant`.
      On this witness it is an advantage in what closes.

------------------------------------------------------------------------------
(I4) THE WALL TABLE, WITH AN IN-REGIME ROW IT DID NOT HAVE
------------------------------------------------------------------------------
  mg-81ff sec 5 prices the wall at 5*C3gap and tabulates 1 (5x), 2.386 (11.9x, out of
  regime), 3.075 (15.4x, out of regime), 10 (50x, hypothetical).  Every measured row was
  out of regime.  The staircase supplies measured IN-REGIME rows:""")
print("      poset          gap          in regime?   C3gap      wall = 5*C3gap")
for lbl, C3, gp in (("N(10)", 1.0650, 0.014446), ("N(16)", 1.0275, 0.003743),
                    ("S_12 ", 4.8758, 0.018778), ("S_20 ", 8.1271, 0.006801),
                    ("S_25 ", 10.1654, 0.004357)):
    print("      %s        %.6f     %-6s      %7.4f    %6.1fx"
          % (lbl, gp, "YES", C3, 5 * C3))
print("""
  >>> THE 5x ROW IS NOT MERELY `THE EXTREME POINT`, WHICH IS mg-81ff's READING AND IS
      RIGHT.  It is also the row its ONE in-regime family happens to sit on.  A different
      in-regime family, primitive and exact, puts the same wall at 24x and then 53x.
      `THE TICKET'S PREMISE SURVIVES ON THE ONLY POSETS ANYONE HAS EXHIBITED INSIDE THE
      REGIME` was true when written; it is not true now, and the sentence that replaces it
      should say WHICH posets.

==============================================================================
a4 VERDICT.  (I1) correct and correctly labelled formal.  (I2) correct — I
re-derived it independently and the negative control fires.  (I3) the equality is
POINTWISE; over a class it is an inequality, strict on this population, in chain
(IV)'s favour — and on the staircase the two chains do not even agree on whether
they close.  `CHAIN (IV) IS CHAIN (II)` holds for the UNKNOWN and fails for the
HYPOTHESIS, which is a distinction mg-81ff draws itself and then does not carry
into its headline.
==============================================================================""")
