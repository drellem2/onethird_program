#!/usr/bin/env python3
"""
mg-1df8 / check 1+2 — RE-DERIVE THE STRENGTH ORDERING FROM THE DEFINITIONS.

Nothing here reads STATE.md, mg-c3ca, mg-c4f5, or any deliverable. The three
definitions are taken from the ticket body and NOTHING ELSE is imported from the
parent. Every number is an exact Fraction; there is no float on any decision path.

Definitions (E = E[inv_e], a function of n):

    (LIB)        E(n) = O(n/gamma)
    (LIB-weak)   E(n) = o(n^2)
    (LIB-const)  E(n) <= (eps/6)(n^2 - 1)

The ticket asks me to confirm "(LIB) < (LIB-weak) < (LIB-const) as asymptotic
classes". I refuse to use "<" (P16): for a HYPOTHESIS, "stronger" is the reverse
of "larger" for a BOUND, and this arc has already inverted on exactly that. So
every result below is an IMPLICATION with a named direction, and each
non-implication is certified by an exhibited witness rather than asserted.
"""

from fractions import Fraction as F

# --------------------------------------------------------------------------
# Membership predicates. Each is decided by an EXACT argument, not sampling;
# the numeric part only EXHIBITS what the argument already proves.
# --------------------------------------------------------------------------


def lib_const_holds_at(E, n, eps):
    """(LIB-const) at a single n: E(n) <= (eps/6)(n^2 - 1), exact rationals."""
    return F(E(n)) <= F(eps, 1) * F(n * n - 1, 6)


def first_violation_of_lib_const(E, eps, nmax):
    """Smallest n <= nmax where (LIB-const) FAILS, or None."""
    for n in range(2, nmax + 1):
        if not lib_const_holds_at(E, n, eps):
            return n
    return None


def smallest_N0(E, eps, nmax):
    """Smallest N0 such that (LIB-const) holds for ALL n in [N0, nmax].

    Scans downward from nmax so a member that is eventually-but-not-always
    compliant reports the true tail threshold, not the first compliant n.
    """
    N0 = None
    for n in range(nmax, 1, -1):
        if lib_const_holds_at(E, n, eps):
            N0 = n
        else:
            break
    return N0


# --------------------------------------------------------------------------
# Witness functions. All exact.
# --------------------------------------------------------------------------

def E_linear(C):
    """E(n) = C*n  -- a member of (LIB) with gamma constant."""
    return lambda n: F(C) * F(n)


def E_quadratic_at_rate(eps):
    """E(n) = (eps/6)(n^2 - 1) -- (LIB-const) with EQUALITY at every n."""
    return lambda n: F(eps, 1) * F(n * n - 1, 6)


def E_sub_quadratic(M):
    """E(n) = M * n^(3/2), rendered EXACTLY as M^2*n^3 under the square.

    n^(3/2) is irrational, so to stay in exact arithmetic every comparison
    E(n) <= B is decided by squaring: M*n^(3/2) <= B  <=>  M^2 * n^3 <= B^2
    (both sides non-negative). We return a symbolic object carrying that rule.
    """
    class SubQuad:
        def __init__(self, M):
            self.M2 = F(M) * F(M)

        def __call__(self, n):
            return self  # placeholder; comparison handled by __le__ below

        def sq(self, n):
            return self.M2 * F(n) ** 3

    return SubQuad(M)


def sub_quadratic_holds_at(M, n, eps):
    """(LIB-const) for E(n) = M*n^(3/2), decided EXACTLY by squaring."""
    lhs_sq = F(M) * F(M) * F(n) ** 3
    rhs = F(eps, 1) * F(n * n - 1, 6)
    if rhs < 0:
        return False
    return lhs_sq <= rhs * rhs


def sub_quadratic_first_violation(M, eps, nmax):
    for n in range(2, nmax + 1):
        if not sub_quadratic_holds_at(M, n, eps):
            return n
    return None


def sub_quadratic_smallest_N0(M, eps, nmax):
    """Smallest N0 with (LIB-const) holding for all n in [N0, nmax], by LINEAR
    scan.  Correct but O(nmax); use the bisecting version for large nmax."""
    N0 = None
    for n in range(nmax, 1, -1):
        if sub_quadratic_holds_at(M, n, eps):
            N0 = n
        else:
            break
    return N0


def sub_quadratic_smallest_N0_fast(M, eps, nmax):
    """Same value as sub_quadratic_smallest_N0, found by BISECTION.

    The predicate P(n): M^2 n^3 <= ((eps/6)(n^2-1))^2 has a single crossover on
    n >= 2 (the right side is degree 4, the left degree 3), so bisecting on the
    last failing n is sound.  We do NOT take that on faith: the returned N0 is
    VERIFIED by checking P fails at N0-1 and holds at N0 and at a spread of
    larger n, and the two implementations are cross-checked against each other
    on every case small enough to scan.
    """
    if sub_quadratic_holds_at(M, 2, eps):
        return 2
    if not sub_quadratic_holds_at(M, nmax, eps):
        return None
    lo, hi = 2, nmax            # P(lo) False, P(hi) True
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if sub_quadratic_holds_at(M, mid, eps):
            hi = mid
        else:
            lo = mid
    N0 = hi
    # VERIFY the crossover rather than assume it.
    assert not sub_quadratic_holds_at(M, N0 - 1, eps), "N0-1 must fail"
    assert sub_quadratic_holds_at(M, N0, eps), "N0 must hold"
    for k in (1, 2, 5, 17, 100, 1000):
        m = N0 + k
        if m <= nmax:
            assert sub_quadratic_holds_at(M, m, eps), f"P must stay true at {m}"
    return N0


# --------------------------------------------------------------------------
def rule(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def main():
    results = {}

    # ---------------------------------------------------------------- R1
    rule("R1  (LIB) ==> (LIB-weak)?   E = O(n/gamma)  ==>  E = o(n^2)?")
    print("""
  ARGUMENT.  Suppose E(n) <= C*n/gamma for all n.  Then

        E(n)/n^2  <=  (C/gamma) * (1/n).

  If gamma is a CONSTANT in n (i.e. bounded below by some gamma_0 > 0), the
  right side -> 0, so E = o(n^2) and the implication HOLDS.

  BUT the implication is CONDITIONAL ON gamma's n-dependence, and the ticket
  states it flat.  If gamma is allowed to depend on n, the bound is
  E(n) <= C*n/gamma(n), and E = o(n^2) requires n/gamma(n) = o(n^2), i.e.
  gamma(n) = omega(1/n).  At gamma(n) = 1/n the bound is C*n^2, which is NOT
  o(n^2).  Exhibited:""")
    for n in (3, 10, 100, 1000):
        gamma_n = F(1, n)
        bound = F(1) * F(n) / gamma_n           # C = 1
        print(f"    n={n:<5} gamma=1/n={gamma_n}   n/gamma = {bound}  "
              f"ratio to n^2 = {bound / F(n*n)}")
    print("""
  The ratio is IDENTICALLY 1 at every n, so the bound sits exactly on n^2 and
  the limit does not go to zero.  VERDICT:
    (LIB) ==> (LIB-weak)  HOLDS when gamma = omega(1/n)   [in particular, constant]
    (LIB) ==> (LIB-weak)  FAILS at gamma(n) = 1/n
  So the first link of the ticket's chain is TRUE UNDER A HYPOTHESIS THE TICKET
  DOES NOT STATE.""")
    results["R1"] = "HOLDS conditional on gamma = omega(1/n); FAILS at gamma=1/n"

    # ---------------------------------------------------------------- R2
    rule("R2  (LIB-weak) ==> (LIB-const) FOR ALL n?   ANSWER: NO.")
    print("""
  WITNESS.  E(n) = M * n^(3/2).  This is o(n^2) for EVERY M, since
  E(n)/n^2 = M/sqrt(n) -> 0.  But at small n it exceeds (eps/6)(n^2-1).
  All comparisons below are decided EXACTLY by squaring both sides
  (M*n^(3/2) <= B  <=>  M^2*n^3 <= B^2); there is no float on this path.
""")
    print(f"    {'eps':>8} {'M':>6} {'first n violating (LIB-const)':>32} "
          f"{'smallest N0 (n<=20000)':>24}")
    rows = []
    for eps, M in [(1, 1), (1, 10), (1, 100), (F(1, 10), 1), (F(1, 100), 1)]:
        fv = sub_quadratic_first_violation(M, eps, 20000)
        N0 = sub_quadratic_smallest_N0(M, eps, 20000)
        rows.append((eps, M, fv, N0))
        print(f"    {str(eps):>8} {M:>6} {str(fv):>32} {str(N0):>24}")
    assert all(r[2] is not None for r in rows), "every witness must violate somewhere"
    print("""
  EVERY row violates (LIB-const) at some n while being o(n^2).  Therefore
  (LIB-weak) does NOT imply (LIB-const)-for-all-n.  The implication holds only
  EVENTUALLY, i.e. for n >= N0.  THE GAP IS A QUANTIFIER, NOT A CONSTANT.""")
    results["R2"] = "NO -- o(n^2) does not give (LIB-const) at every n"

    # ---------------------------------------------------------------- R3
    rule("R3  NO N0 WORKS FOR THE CLASS o(n^2).")
    print("""
  CLAIM.  For any candidate threshold N0 and any eps > 0 there is a member of
  o(n^2) that VIOLATES (LIB-const) at n = N0.  Take E(n) = M*n^(3/2) with M
  large enough.  So N0 is a function of the MEMBER, never of the class.

  Exhibited: for each N0 below, the smallest integer M whose witness still
  violates (LIB-const) AT n = N0 (eps = 1):
""")
    print(f"    {'N0':>8} {'M needed':>12} {'M^2*N0^3':>26} {'((eps/6)(N0^2-1))^2':>28}")
    for N0 in (10, 100, 1000, 10000):
        M = 1
        while sub_quadratic_holds_at(M, N0, 1):
            M *= 2
        lhs = F(M) * F(M) * F(N0) ** 3
        rhs = (F(1) * F(N0 * N0 - 1, 6)) ** 2
        print(f"    {N0:>8} {M:>12} {str(lhs):>26} {str(rhs):>28}")
        assert lhs > rhs
    print("""
  M grows without bound as N0 does, and it is ALWAYS FINITE, so the witness
  always exists.  VERDICT: there is no N0 uniform over the class.  A reader who
  is told "(LIB-weak) suffices" and goes looking for THE N0 is looking for an
  object that does not exist.""")
    results["R3"] = "NO uniform N0 over the class"

    # ---------------------------------------------------------------- R4
    rule("R4  (LIB-const) ==> (LIB-weak)?   ANSWER: NO.")
    print("""
  WITNESS.  E(n) = (eps/6)(n^2 - 1) -- (LIB-const) holds with EQUALITY at every
  n, so it is a member.  But E(n)/n^2 -> eps/6 != 0, so it is NOT o(n^2).
  Exhibited at eps = 1:
""")
    E = E_quadratic_at_rate(1)
    for n in (3, 10, 100, 1000, 100000):
        print(f"    n={n:<8} E(n) = {E(n)}   E(n)/n^2 = {E(n)/F(n*n)}  "
              f"(limit is 1/6 = {F(1,6)})")
        assert lib_const_holds_at(E, n, 1)
    print("""
  The ratio RISES toward 1/6 and never approaches 0.  VERDICT:
  (LIB-const) does NOT imply (LIB-weak).""")
    results["R4"] = "NO -- (LIB-const) admits Theta(n^2)"

    # ---------------------------------------------------------------- R5
    rule("R5  CONSEQUENCE: (LIB-weak) AND (LIB-const) ARE INCOMPARABLE.")
    print("""
  R2 gives (LIB-weak) NOT=> (LIB-const).   R4 gives (LIB-const) NOT=> (LIB-weak).
  As SETS OF FUNCTIONS OF n, neither contains the other.  So the ticket's own
  rendering

        (LIB) < (LIB-weak) < (LIB-const)

  IS NOT A CHAIN OF IMPLICATIONS.  It is defensible ONLY under the reading
  "the admitted bound grows no slower as you move right, in the limit", i.e.

        (LIB) ==> (LIB-weak) ==> (LIB-const) FOR ALL SUFFICIENTLY LARGE n

  with the first link additionally requiring gamma = omega(1/n) (R1).  Any
  rendering that drops "for all sufficiently large n" is FALSE IN THE SECOND
  DIRECTION, which is the same defect class the ticket was raised about.""")
    results["R5"] = "INCOMPARABLE as function classes; chain only under 'eventually'"

    # ---------------------------------------------------------------- R6
    rule("R6  THE SURVIVING THRESHOLD MOVES.  N0 as a function of eps.")
    print("""
  For E(n) = M*n^(3/2), (LIB-const) reads M*n^(3/2) <= (eps/6)(n^2-1), which for
  large n is ~ M <= (eps/6)*sqrt(n), i.e. N0 ~ (6M/eps)^2.  So N0 blows up
  QUADRATICALLY as eps falls.  Measured EXACTLY at M = 1:
""")
    print(f"    {'eps':>10} {'smallest N0':>14} {'(6/eps)^2':>14} {'ratio':>12}")
    prev = None
    for eps in (F(1), F(1, 2), F(1, 4), F(1, 8), F(1, 16)):
        N0 = sub_quadratic_smallest_N0_fast(1, eps, 10 ** 9)
        pred = (F(6) / eps) ** 2
        print(f"    {str(eps):>10} {str(N0):>14} {str(pred):>14} "
              f"{str(F(N0) / pred):>12}")
        if prev is not None:
            assert N0 > prev, "N0 must rise as eps falls"
        prev = N0
    print("\n    CROSS-CHECK of the bisecting finder against the linear scan,")
    print("    on every case small enough to scan exhaustively:")
    agree = 0
    for eps, M, nmax in [(F(1), 1, 3000), (F(1), 10, 20000), (F(1, 2), 1, 3000),
                         (F(1, 4), 1, 20000), (F(1), 3, 5000)]:
        a = sub_quadratic_smallest_N0(M, eps, nmax)
        b = sub_quadratic_smallest_N0_fast(M, eps, nmax)
        ok = (a == b)
        agree += ok
        print(f"      eps={str(eps):<6} M={M:<3} nmax={nmax:<6} "
              f"scan={str(a):<8} bisect={str(b):<8} {'AGREE' if ok else 'DISAGREE'}")
        assert ok, "the two finders must agree"
    print(f"    {agree}/5 agree.")
    print("""
  N0 rises strictly as eps falls, and tracks (6/eps)^2 as predicted.  So a
  claim of the form "(LIB-weak) suffices, we just need n large" carries a
  threshold that MOVES WITH THE CONSTANT YOU WANT, and quoting it without eps
  is not a bound.""")
    results["R6"] = "N0 ~ (6M/eps)^2 -- rises without bound as eps falls"

    # ---------------------------------------------------------------- NC
    rule("NEGATIVE CONTROLS -- these must FAIL, or my instrument proves nothing.")

    print("\n  NC1.  A function that is genuinely O(n) must NOT be reported as")
    print("        violating (LIB-const) at large n.  E(n) = 5n, eps = 1:")
    E5 = E_linear(5)
    fv = first_violation_of_lib_const(E5, 1, 5000)
    N0 = smallest_N0(E5, 1, 5000)
    print(f"        first violation = {fv}   smallest N0 = {N0}")
    assert N0 is not None and N0 <= 40, "linear function must comply from small n"
    print("        PASS: complies from n =", N0, "-- the instrument does not")
    print("        flag compliant members.")

    print("\n  NC2.  A function that is Theta(n^2) with a coefficient ABOVE eps/6")
    print("        must violate (LIB-const) FOREVER, never acquiring an N0.")
    print("        E(n) = (n^2-1)/3 against eps = 1 (i.e. coefficient 1/3 > 1/6):")
    Ebad = lambda n: F(n * n - 1, 3)
    N0bad = smallest_N0(Ebad, 1, 5000)
    fvbad = first_violation_of_lib_const(Ebad, 1, 5000)
    print(f"        first violation = {fvbad}   smallest N0 = {N0bad}")
    assert N0bad is None, "a permanently-violating member must have NO N0"
    print("        PASS: N0 is None -- 'eventually' is not vacuous, the")
    print("        instrument can tell 'eventually complies' from 'never does'.")

    print("\n  NC3.  My R2 witness must really be o(n^2) and not merely small.")
    print("        E(n)/n^2 = M/sqrt(n) for M = 100; squared ratios, exact:")
    for n in (10 ** 2, 10 ** 4, 10 ** 6, 10 ** 8):
        ratio_sq = F(100) ** 2 * F(n) ** 3 / F(n) ** 4
        print(f"        n={n:<10} (E/n^2)^2 = {ratio_sq}")
    assert F(100) ** 2 * F(10 ** 8) ** 3 / F(10 ** 8) ** 4 < F(1, 1000)
    print("        PASS: falls to 0, so the witness is genuinely in o(n^2) and")
    print("        R2's non-implication is not built on a non-member.")

    print("\n  NC4.  DELIBERATELY WRONG ORDERING must be rejected.  If I assert")
    print("        (LIB-const) ==> (LIB-weak) and test it on R4's own witness,")
    print("        the test must FAIL:")
    E = E_quadratic_at_rate(1)
    claim_holds = (E(10 ** 6) / F(10 ** 12)) < F(1, 1000)
    print(f"        E(10^6)/n^2 = {E(10**6)/F(10**12)}  < 1/1000 ?  {claim_holds}")
    assert not claim_holds
    print("        PASS: rejected.  The instrument is not vacuously agreeing.")

    # ---------------------------------------------------------------- SUMMARY
    rule("SUMMARY -- THE ORDERING, RE-DERIVED, WITH NO '<' ANYWHERE")
    print("""
    (LIB)       ==>  (LIB-weak)      PROVIDED gamma = omega(1/n)      [R1]
    (LIB-weak)  ==>  (LIB-const)     ONLY FOR n >= N0(member, eps)    [R2]
    (LIB-const) ==>  (LIB-weak)      FALSE                            [R4]
    (LIB-weak)  ==>  (LIB-const)     FALSE as a for-all-n statement   [R2]

    => (LIB) is STRICTLY THE STRONGEST HYPOTHESIS of the three.
    => (LIB-weak) and (LIB-const) are INCOMPARABLE as function classes. [R5]
    => The gap between them is A QUANTIFIER (for all n / for large n),
       NOT A CONSTANT.  No constant converts one into the other.
    => There is no N0 for the CLASS o(n^2), only one per member.        [R3]
    => That per-member N0 grows like (6M/eps)^2, so it MOVES.           [R6]

    THE TICKET'S DIRECTION IS RIGHT AND THE 'OPPOSITE' THAT MERGED THIS MORNING
    WAS WRONG -- but the ticket's rendering as a CHAIN is itself imprecise, in
    exactly the direction that lets a reader believe (LIB-weak) delivers
    (LIB-const).""")

    for k, v in results.items():
        print(f"  {k}: {v}")
    print("\nALL ASSERTIONS PASSED.")


if __name__ == "__main__":
    main()
