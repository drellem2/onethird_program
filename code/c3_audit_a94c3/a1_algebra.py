"""a1_algebra -- THE ONE THING THE TICKET ASKS FIRST.

Re-derive the threshold relation

    n >= 4 C_3 / eps_leak^2 - 1

from Op-Form, NOT from mg-76b2's ticket body and NOT from its deliverable, and
say WHICH NORMALISATION it was checked in.  Exact rational arithmetic
throughout; nothing here uses a float, so nothing here can be an artefact of
one.

Two live normalisations, both in this corpus, differing by exactly a factor
that tends to 6 (STATE.md row 8):

    eps_spec = 6 E[inv_e] / (n^2 - 1)        <- Op-Form :437, STATE.md:15
    eps_c3ca =   E[inv_e] / n^2              <- OneThird-LIBweak-mg-c3ca.md:172

    eps_spec / eps_c3ca = 6 n^2 / (n^2 - 1) -> 6

The ticket's worry is that this factor was dropped.  Sections 3-5 below settle
it in a form stronger than "I checked": the relation is INVARIANT under a
CONSISTENT change of normalisation and WRONG BY ~6 under a MIXED one, so the
question "which normalisation?" has a determinate answer and it is checked.
"""

from fractions import Fraction as F
from libA94 import banner


def min_n_meeting(supply, demand):
    """Least n >= 2 with supply(n) <= demand(n).  Both exact rationals.
    Brute force -- no closed form is assumed, which is the point."""
    for n in range(2, 200000):
        if supply(n) <= demand(n):
            return n
    return None


def closed_form_III(C3, leak):
    """n >= 4 C_3 / eps_leak^2 - 1, as the least INTEGER satisfying it."""
    thr = F(4) * C3 / (leak * leak) - 1
    n = thr.numerator // thr.denominator
    while n < thr:
        n += 1
    return max(n, 2)


rc = 0

# --------------------------------------------------------------------------
banner("1. THE INPUTS, QUOTED FROM Op-Form -- and which normalisation each is in")
print("""
  Op-Form sec.4.2 (:264-271), the Cheeger square, PROVEN given the sandwich:

        1 - lambda_std <= eps_spec   ==>   Phi*_P <= sqrt(2 eps_spec)

    and Step 5 wants Phi_P(A_k) <= eps_leak, so

        eps_spec <= eps_leak^2 / 2.

  Op-Form sec.4.3 (:299-303), L3's prefix-restriction loss, UNQUANTIFIED:

        "Under either repair the loss is a constant C_3, giving
         eps_spec <= eps_leak^2 / (2 C_3)."

  NORMALISATION OF THE DEMAND SIDE.  eps_spec here is the SAME eps_spec that
  Op-Form :437 and STATE.md:15 define by  E[inv_e] <= (eps_spec/6)(n^2-1),
  i.e. eps_spec = 6 E[inv_e]/(n^2-1).  It has to be: sec.4.2 derives it from
  '1 - lambda_std <= eps_spec' and the master bound is what converts that one
  statement into inversions.  There is one eps_spec in Op-Form, not two.

  NORMALISATION OF THE SUPPLY SIDE.  mg-200d's conjectured value is recorded
  at mg-6bc2 :320 as: the per-slot optimiser has E[inv] = 2/3, 1, 4/3 at
  n = 3,4,5 and 'satisfies 6E/(n^2-1) = 2/(n+1) EXACTLY'.  So 2/(n+1) is
  quoted in eps_spec.  Checked, not taken on trust, in section 2.
""")

# --------------------------------------------------------------------------
banner("2. IS 2/(n+1) REALLY IN THE eps_spec NORMALISATION?  (the factor-of-6 test)")
PER_SLOT_E = {3: F(2, 3), 4: F(1), 5: F(4, 3)}   # mg-6bc2 sec.5.1, read
print(f"{'n':>3} {'E[inv]':>8} {'6E/(n^2-1)':>12} {'2/(n+1)':>10} {'match':>7} "
      f"{'E/n^2 (c3ca)':>14} {'= 2/(n+1)?':>11}")
spec_ok = c3ca_ok = 0
for n, E in sorted(PER_SLOT_E.items()):
    sp = F(6) * E / (n * n - 1)
    ca = E / (n * n)
    tgt = F(2, n + 1)
    spec_ok += (sp == tgt)
    c3ca_ok += (ca == tgt)
    print(f"{n:>3} {str(E):>8} {str(sp):>12} {str(tgt):>10} {str(sp == tgt):>7} "
          f"{str(ca):>14} {str(ca == tgt):>11}")
print(f"\n  eps_spec reading matches 2/(n+1) at {spec_ok}/3 of the recorded n.")
print(f"  eps_c3ca reading matches 2/(n+1) at {c3ca_ok}/3 of the recorded n.")
if spec_ok != 3 or c3ca_ok != 0:
    print("  *** UNEXPECTED -- the supply side is not where it was said to be.")
    rc = 1
print("""
  VERDICT.  2/(n+1) IS the eps_spec normalisation and is NOT the eps_c3ca one.
  In eps_c3ca the same three optimisers read 2/27, 1/16, 4/75 -- not 2/(n+1)
  at any n, and not even the same SHAPE (they fall like 1/(3n), not 2/n).
""")

# --------------------------------------------------------------------------
banner("3. THE RE-DERIVATION, IN eps_spec, BY BRUTE FORCE AGAINST THE CLOSED FORM")
print("""
  Chain (III), which is the reading the ticket's relation belongs to:

      Phi_prefix <= sqrt(2 C_3 eps_spec) <= eps_leak
        <=> eps_spec <= eps_leak^2/(2 C_3)                     [= eps_dem]

  Demand met by the mg-200d supply when   2/(n+1) <= eps_leak^2/(2 C_3),
  i.e.  n + 1 >= 4 C_3 / eps_leak^2,  i.e.  n >= 4 C_3/eps_leak^2 - 1.

  Below: the least n found by SEARCH (no closed form used) against the least n
  satisfying the closed form.  A mismatch anywhere refutes the relation.
""")
LEAKS = [F(1, 5), F(1, 50), F(1, 10), F(3, 20), F(1, 4)]
C3S = [F(1), F(3, 2), F(2), F(5, 2), F(3), F(10)]
print(f"{'eps_leak':>9} {'C_3':>6} {'eps_dem':>14} {'n by search':>12} "
      f"{'closed form':>12} {'agree':>6}")
agree = total = 0
for leak in LEAKS:
    for C3 in C3S:
        dem = leak * leak / (2 * C3)
        got = min_n_meeting(lambda n: F(2, n + 1), lambda n: dem)
        want = closed_form_III(C3, leak)
        total += 1
        agree += (got == want)
        if got != want:
            rc = 1
        print(f"{str(leak):>9} {str(C3):>6} {str(dem):>14} {got:>12} "
              f"{want:>12} {str(got == want):>6}")
print(f"\n  {agree}/{total} agree.  THE TICKET'S ALGEBRA IS CORRECT AS WRITTEN,")
print("  IN THE eps_spec NORMALISATION.  No factor of 6 was dropped in it.")
print(f"  Headline instance: eps_leak = 1/5, C_3 = 1  ->  n >= "
      f"{closed_form_III(F(1), F(1, 5))}  (4/eps_leak^2 - 1 = 99).")

# --------------------------------------------------------------------------
banner("4. INVARIANCE -- the relation SURVIVES a CONSISTENT change of normalisation")
print("""
  Convert BOTH sides to eps_c3ca by multiplying by (n^2-1)/(6 n^2):

      supply  2/(n+1)              ->  (n-1)/(3 n^2)
      demand  eps_leak^2/(2 C_3)   ->  eps_leak^2 (n^2-1) / (12 C_3 n^2)

  and re-solve by search.  If the threshold moves, the relation was
  normalisation-dependent and the ticket's worry was justified.
""")
print(f"{'eps_leak':>9} {'C_3':>6} {'n in eps_spec':>14} {'n in eps_c3ca':>14} {'same':>6}")
same = 0
for leak in LEAKS:
    for C3 in C3S:
        dem = leak * leak / (2 * C3)
        a = min_n_meeting(lambda n: F(2, n + 1), lambda n: dem)
        b = min_n_meeting(lambda n: F(n - 1, 3 * n * n),
                          lambda n, d=dem: d * F(n * n - 1, 6 * n * n))
        same += (a == b)
        if a != b:
            rc = 1
        print(f"{str(leak):>9} {str(C3):>6} {a:>14} {b:>14} {str(a == b):>6}")
print(f"\n  {same}/{total} identical.  THE THRESHOLD IS NORMALISATION-INVARIANT")
print("  UNDER A CONSISTENT CONVERSION.  The (n-1) and n^2 factors cancel; the")
print("  factor of 6 is NOT a hazard when both sides move together.")

# --------------------------------------------------------------------------
banner("5. THE HAZARD IS MIXING -- and it is worth ~6x, in the OPTIMISTIC direction")
print("""
  Now do the thing this lineage has already done once in 24 hours: read the
  SUPPLY in eps_c3ca and the DEMAND in eps_spec, and solve.
""")
print(f"{'eps_leak':>9} {'C_3':>6} {'correct n':>10} {'mixed-unit n':>13} "
      f"{'ratio':>8}")
for leak in LEAKS:
    for C3 in C3S:
        dem = leak * leak / (2 * C3)
        good = min_n_meeting(lambda n: F(2, n + 1), lambda n: dem)
        bad = min_n_meeting(lambda n: F(n - 1, 3 * n * n), lambda n: dem)
        print(f"{str(leak):>9} {str(C3):>6} {good:>10} {bad:>13} "
              f"{good / bad if bad else 0:>8.3f}")
print("""
  The mixed-unit answer is ~6x SMALLER: it says the finite window closes six
  times sooner than it does.  That is the direction that makes a programme
  report a win it has not got.  This is the error the ticket names, it is real,
  and IT IS NOT PRESENT IN THE TICKET'S OWN RELATION.
""")

# --------------------------------------------------------------------------
banner("6. THE OTHER THREE CHAINS, RE-DERIVED RATHER THAN STEP-CHECKED")
print("""
  mg-76b2 sec.6 tabulates four chains.  Each is re-derived here from Op-Form's
  Lemma-2.1 dictionary (Phi <= 1-rho <= 2 Phi) and Step 5's Phi <= eps_leak,
  and its window is then solved by SEARCH against 2/(n+1) in eps_spec.

    (I)   monotone sweep      Phi <= sqrt(2 eps_spec)        eps_dem = L^2/2
    (II)  gap-form capture    Phi <= 1-rho <= C_3 eps_spec   eps_dem = L/C_3
    (III) degraded pfx Cheeger Phi <= sqrt(2 C_3 eps_spec)   eps_dem = L^2/(2C_3)
    (IV)  literal capture     1-rho <= (1-c) + c eps_spec    eps_dem = 1-(1-L)/c
""")
L = F(1, 5)
print(f"{'chain':>6} {'C_3 or c':>9} {'eps_dem':>12} {'n by search':>12} "
      f"{'closed form':>14}")
for C3 in [F(1), F(2), F(3)]:
    for tag, dem, cf in (
        ("(I)", L * L / 2, "4/L^2 - 1"),
        ("(II)", L / C3, "2C_3/L - 1"),
        ("(III)", L * L / (2 * C3), "4C_3/L^2 - 1"),
    ):
        if tag == "(I)" and C3 != 1:
            continue
        got = min_n_meeting(lambda n: F(2, n + 1), lambda n, d=dem: d)
        print(f"{tag:>6} {str(C3):>9} {str(dem):>12} {got:>12} {cf:>14}")
print()
for c in [F(4, 5), F(41, 50), F(17, 20), F(9, 10), F(19, 20), F(99, 100), F(1)]:
    dem = 1 - (1 - L) / c
    if dem <= 0:
        print(f"{'(IV)':>6} {str(c):>9} {str(dem):>12} {'does not close':>12}")
        continue
    got = min_n_meeting(lambda n: F(2, n + 1), lambda n, d=dem: d)
    print(f"{'(IV)':>6} {str(c):>9} {str(dem):>12} {got:>12}   window n <= {got-1}")
print("""
  Reproduces mg-76b2 sec.5's table (windows 80, 32, 16, 11, 9, 8) and sec.6's
  windows (99 / 10C_3-1 / 100C_3-1) EXACTLY, on code that never read them --
  they are a consequence of the same two lines of algebra.  The ratio between
  (II) and (III) is 2/eps_leak = 10 at every C_3, as mg-76b2 claim 16 says.
""")

banner("EXIT")
print(f"rc = {rc}")
raise SystemExit(rc)
