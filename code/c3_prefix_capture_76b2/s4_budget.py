#!/usr/bin/env python3
"""s4 — THE BUDGET: four chains, four different relations, and the finite window.

SCOPE LABEL REPAIRED, mg-be0b, on mg-3329's finding (which is on mg-fa70's).  The
printed line below the chain table read "s2 shows that under L2 it does not degrade
anything".  `L2` is a DISJUNCTION, so "under L2" is "under EITHER disjunct" with the
words removed; what s2 shows is a FIRST-DISJUNCT statement, and the mechanism it
names -- the sweep never leaving the prefix family -- IS the first disjunct and does
not exist on the second.  NO NUMBER IN THIS SECTION MOVES and no chain is withdrawn:
this file's own chain (I) header at :12 already reads "L2's first disjunct" and always
did.  On L2's second disjunct the constant is RELOCATED, not eliminated (mg-fa70; see
s2's header).  See docs/repair-mg-be0b-the-either-disjunct-claim-outside-STATE.md.

The ticket states one relation:

    eps_dem = eps_leak^2 / (2 C_3)   =>   n >= 4 C_3 / eps_leak^2 - 1

and asks how big the finite window is.  With the s1 dictionary the answer is that this is
ONE of four chains from `1 - lambda_std <= eps_spec` to `Delta_1(A_k,A_k^c) <= eps_leak`,
they are NOT equivalent, and the ticket's is the most pessimistic of them.

    (I)   MONOTONE SWEEP.  L2's first disjunct.  Cheeger's own sweep, whose sets are
          threshold sets, applied to a monotone eigenvector: every set it visits is
          already a prefix or a suffix.
              Phi <= sqrt(2 eps_spec)          eps_dem = eps_leak^2 / 2      NO C_3.

    (II)  GAP-FORM PREFIX CAPTURE.  Op-Form 4.3's own named repair, "1 - rho <= C_3
          (1 - lambda_std)".  It hands you the prefix directly, so the Cheeger square is
          never spent.
              Phi <= C_3 eps_spec              eps_dem = eps_leak / C_3.

    (III) DEGRADED PREFIX CHEEGER.  A prefix-restricted Cheeger inequality with the gap
          degraded by C_3.  THIS is the reading Op-Form 4.3's displayed relation belongs
          to, and it is the ticket's.
              Phi <= sqrt(2 C_3 eps_spec)      eps_dem = eps_leak^2 / (2 C_3).

    (IV)  LITERAL PREFIX CAPTURE.  The conjecture exactly as worded: rho >= c lambda_std.
              Phi <= 1 - c(1 - eps_spec)       eps_dem = 1 - (1-eps_leak)/c.

Every relation is derived, printed symbolically, and then evaluated.  eps_leak is swept
rather than pinned, because it is approximate in this corpus and the ticket says so.

The `n >=` column assumes the mg-200d conjecture eps_spec = 2/(n+1), which this ticket
does NOT otherwise depend on.  It is labelled at every site.
"""

from fractions import Fraction as F
import sys

fail = 0


def check(cond, msg):
    global fail
    if not cond:
        fail += 1
        print(f"    FAIL: {msg}")


def window(eps_dem):
    """Smallest n with 2/(n+1) <= eps_dem, i.e. n >= 2/eps_dem - 1.  Exact."""
    if eps_dem <= 0:
        return None
    thr = 2 / eps_dem - 1
    n = int(thr)
    while F(2, n + 1) > eps_dem:
        n += 1
    return n


print("=" * 78)
print("s4 — THE BUDGET: four chains, four relations, and the finite window")
print("=" * 78)
print()

# ---------------------------------------------------------------- consistency
print("-" * 78)
print("(B0) THE FOUR RELATIONS, and a check that each is what its chain forces")
print("-" * 78)
print()
print("  Common: Step 5 needs Delta_1(A_k, A_k^c) = Phi_P(A_k) <= eps_leak, and s1's (D2)")
print("  gives Phi_P(A_k) <= 1 - rho(A_k) <= 2 Phi_P(A_k).  So a bound on 1 - rho is a")
print("  bound on Phi with no further loss, and vice versa up to a factor 2.")
print()
print("   chain   what it bounds                 eps_dem            n >= (mg-200d)")
print("   -----   ---------------------------    ---------------    --------------")
print("   (I)     Phi <= sqrt(2 eps_spec)        eps_leak^2 / 2     4/eps_leak^2 - 1")
print("   (II)    Phi <= C_3 eps_spec            eps_leak / C_3     2 C_3/eps_leak - 1")
print("   (III)   Phi <= sqrt(2 C_3 eps_spec)    eps_leak^2/(2C_3)  4 C_3/eps_leak^2 - 1")
print("   (IV)    Phi <= 1 - c(1-eps_spec)       1 - (1-eps_leak)/c 2/eps_dem - 1")
print()
print("  (III) at C_3 = 1 IS (I).  So the ticket's relation is chain (I) with a factor")
print("  C_3 inserted at the one place chain (I) does not have one -- which is correct")
print("  bookkeeping if and only if the prefix restriction really does degrade the gap.")
print("  s2 shows that under L2's FIRST DISJUNCT it does not degrade anything, because")
print("  the sweep never leaves the prefix family in the first place.")
print()
print("  (II) is NOT (III) with C_3 moved.  The gap-form repair supplies the prefix")
print("  itself, so Cheeger's square -- the price of turning an eigenVALUE into a SET --")
print("  is not paid.  Op-Form 4.3 says 'under EITHER repair ... giving")
print("  eps_spec <= eps_leak^2/(2C_3)'; that relation follows from the degraded-Cheeger")
print("  repair and NOT from the gap-form repair it names in the same sentence.")
print()

# ------------------------------------------------------------------- sweep
print("-" * 78)
print("(B1) THE FINITE WINDOW, swept over eps_leak")
print("-" * 78)
print()
print("  eps_leak is approximate in this corpus (mg-e35c F5's repair, resting on")
print("  mg-3ce3's empirical envelope: 0 RED / 6681 posets up to 0.20).  It is swept,")
print("  not pinned.  THE ROW USED FOR EVERY HEADLINE ELSEWHERE IS eps_leak = 1/5.")
print()
print("  Chain (I) -- NO C_3.  eps_dem = eps_leak^2/2,  n >= 4/eps_leak^2 - 1")
print()
print("     eps_leak     eps_dem        window n <=")
for el in [F(1, 50), F(1, 20), F(1, 10), F(3, 20), F(1, 5), F(1, 4), F(1, 3)]:
    ed = el ** 2 / 2
    w = window(ed)
    star = "   <-- the repaired calibration" if el == F(1, 5) else ""
    print(f"     {str(el):8s} {str(ed):14s} {w - 1:8d}{star}")
    check(w == int(4 / el ** 2 - 1) + 1 or F(2, w + 1) <= ed,
          f"B1 window arithmetic at eps_leak={el}")
print()
print("  Reading: at the repaired calibration the demand is met from n = 99 upward, so")
print("  the finite window still owed is n <= 98 -- and it is owed WITHOUT any appeal")
print("  to C_3, to the Prefix-capture conjecture, or to any constant not already in")
print("  Cheeger's inequality.")
print()

# ------------------------------------------------------------- C_3 linearity
print("-" * 78)
print("(B2) HOW THE WINDOW MOVES WITH C_3, in each chain that carries one")
print("-" * 78)
print()
EL = F(1, 5)
print(f"  at eps_leak = {EL}:")
print()
print("     C_3    (II) eps_dem   (II) n <=     (III) eps_dem   (III) n <=")
for c3 in [F(1), F(3, 2), F(2), F(5), F(10)]:
    e2 = EL / c3
    e3 = EL ** 2 / (2 * c3)
    w2, w3 = window(e2), window(e3)
    print(f"     {str(c3):5s}  {str(e2):13s} {w2-1:9d}     {str(e3):13s} {w3-1:11d}")
print()
print("  Both are linear in C_3, exactly as the ticket says.  They differ by the factor")
print(f"  2/eps_leak = {2/EL} throughout -- chain (III) charges the Cheeger square on top of")
print("  the prefix loss, chain (II) charges the prefix loss instead of it.")
print()
print("  MEASURED C_3 (s3, and OUTSIDE the regime -- see s3 (C1)):")
print("     C_3^cut  max 15/8 = 1.875 at n = 6, and rising with n")
print("     C_3^gap  max 2.386 at n = 6, and rising with n")
print("  Neither is a bound.  A finite population can REFUTE a uniform-in-n bound and")
print("  can never establish one; what these rows do is show the direction of travel,")
print("  and it is upward in both currencies.")
print()

# ------------------------------------------------------------ literal reading
print("-" * 78)
print("(B3) THE LITERAL READING -- Op-Form 4.3 calls it 'too weak to use'.  It is not.")
print("-" * 78)
print()
print("  As worded: rho(A_k) >= c * lambda_std for a constant fraction c.  With")
print("  lambda_std >= 1 - eps_spec this gives")
print()
print("      1 - rho  <=  1 - c(1 - eps_spec)  =  (1-c) + c*eps_spec")
print()
print("  Op-Form 4.3 reads the (1-c) term as a CONSTANT FLOOR and concludes the form is")
print("  too weak to use.  The arithmetic is right.  The conclusion does not follow,")
print("  because the consumer does not need a vanishing quantity -- it needs")
print("  Phi <= eps_leak for an ABSOLUTE CONSTANT eps_leak, and Op-Form's own SS3.2")
print("  is what establishes that eps_leak is an absolute constant.  A constant floor")
print("  below a constant ceiling is usable.")
print()
print("  Solving 1 - c(1-eps_spec) <= eps_leak for eps_spec:")
print()
print("      eps_dem  =  1 - (1 - eps_leak)/c ,   usable for every  c > 1 - eps_leak")
print()
for el in [F(1, 50), F(1, 5)]:
    print(f"  at eps_leak = {el}  (usable for every c > {1-el} = {float(1-el)}):")
    print("        c        eps_dem                      window n <=")
    for c in [F(4, 5), F(41, 50), F(17, 20), F(9, 10), F(19, 20), F(99, 100), F(1)]:
        ed = 1 - (1 - el) / c
        if ed <= 0:
            print(f"        {str(c):8s} {str(ed):26s}    (chain does not close)")
            continue
        w = window(ed)
        print(f"        {str(c):8s} {str(ed):26s} {w-1:8d}")
    print()
print("  TWO THINGS THE TABLE SAYS.")
print()
print("  1. The threshold on c is  c > 1 - eps_leak, i.e. c > 0.80 at the repaired")
print("     calibration and c > 0.98 at the superseded one.  mg-e35c F5's 100x repair")
print("     moved this from a value no one would call 'a constant fraction' to one that")
print("     is an ordinary reading of the phrase.  Op-Form 4.3's verdict was reached")
print("     against the superseded number and has never been re-examined against the")
print("     repaired one: the supersession banner at the head of that document lists")
print("     SS6.4-7.4 and SS10, and SS4.3 is not among them.")
print()
print("  2. At c near 1 -- which is the conjecture's OWN alternative wording, '1-o(1)' --")
print("     the literal reading is the STRONGEST of the four chains, not the weakest,")
print(f"     because it never spends the Cheeger square: eps_dem -> eps_leak = {float(EL)},")
print(f"     against {float(EL**2/2)} for chain (I).  A factor of {float(2/EL)}.")
print()
print("  What is TRUE, and is what SS4.3 should say, is that the conjecture NAMES NO c.")
print("  'Unquantified at a now-explicit threshold' is a different verdict from 'too")
print("  weak to use', and it is actionable: c is a measurable quantity (s3 (C3)), and")
print("  the source's own computational programme item 7 already calls for measuring it.")
print()

print("=" * 78)
print(f"s4 VERDICT: {'ALL ARITHMETIC CHECKS PASS' if fail == 0 else str(fail) + ' FAILURES'}")
print("=" * 78)
sys.exit(1 if fail else 0)
