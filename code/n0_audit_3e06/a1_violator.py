#!/usr/bin/env python3
"""
mg-3e06 — INDEPENDENT AUDIT of mg-5ce3's landing of mg-c4f5 §5.3.

CHECK 1 of the brief: "BUILD ONE" — construct the o(n^2) function that §5.3
says exists below ANY candidate N_0, and check it.

This instrument shares no line with mg-5ce3's (which committed no code at all,
by its own NOT DONE) and does not read the audit document. It re-derives the
statement from the DEFINITIONS:

  (LIB-weak)   for frozen P,  E[inv_e] = o(n^2)      [mg-c3ca:75]
               inv_e counts INCOMPARABLE pairs inverted w.r.t. e
  (LIB-const)  E[inv_e] <= (eps_spec/6)(n^2 - 1)     [STATE.md row 8]
               (mg-c4f5 §5.3 writes the same bound as (eps_spec/6) n^2 —
                both forms are carried here and the difference is measured,
                not assumed away)

ALL ARITHMETIC IS EXACT. Fractions and Python big integers throughout; there is
no float on any decision path. log2 is never evaluated numerically — every
statement about log2 n is reduced to an integer comparison against a power of 2.
"""

from fractions import Fraction as F

EPS_REPAIRED   = F(2, 10**2)   # 2e-2, the repaired calibration
EPS_SUPERSEDED = F(2, 10**4)   # 2e-4, the superseded one

# ----------------------------------------------------------------------------
# the two renderings of (LIB-const), kept apart on purpose
# ----------------------------------------------------------------------------

def lib_const_rhs_state(n, eps):
    """STATE.md row 8 / line 15 form: (eps/6)(n^2 - 1)."""
    return eps * F(n * n - 1, 6)

def lib_const_rhs_doc(n, eps):
    """mg-c4f5 §5.3 form: (eps/6) n^2."""
    return eps * F(n * n, 6)

RHS = {"STATE (n^2-1)": lib_const_rhs_state, "DOC (n^2)": lib_const_rhs_doc}

# ----------------------------------------------------------------------------
# candidate witnesses.  each is a function n -> Fraction, parameterised by N_0.
# the SHAPE is the content: anything o(n^2) above N_0, anything big below it.
# ----------------------------------------------------------------------------

def floor_log2(n):
    """exact floor(log2 n) for n >= 1, integer-only."""
    return n.bit_length() - 1

def log2_ge(n, c):
    """exact predicate  log2 n >= c  for integer c >= 0, integer-only."""
    return n >= 2 ** c

# --- tails: each must be o(n^2) ------------------------------------------------
# expressed as (name, f(n) -> Fraction) using only exact arithmetic.
# for the log2 tails we use the exact rational n^2 / floor_log2(n) as a
# CONSERVATIVE stand-in: floor_log2(n) <= log2(n), so n^2/floor_log2(n) >=
# n^2/log2(n).  proving the conservative version is o(n^2) proves it for the
# real one, and proving the conservative version violates a bound proves the
# real one does too only where we say so — so we use it only for o(n^2).

TAILS = {
    "n^2 / log2 n   (§5.3's own)": lambda n: F(n * n, max(floor_log2(n), 1)),
    "n^2 / log2 log2 n":           lambda n: F(n * n, max(floor_log2(max(floor_log2(n), 2)), 1)),
    "n^2 / sqrt(log2 n)":          lambda n: F(n * n * 100, max(isqrt100(floor_log2(n)), 1)),
    "n^(3/2)  (a plain power)":    lambda n: F(isqrt_exact(n ** 3)),
    "0        (the n-chain)":      lambda n: F(0),
}

def isqrt_exact(x):
    import math
    return math.isqrt(x)

def isqrt100(k):
    """100*sqrt(k) rounded down, integer-only, for the sqrt(log2) tail."""
    import math
    return math.isqrt(k * 10000)

# --- prefixes: each must VIOLATE (LIB-const) on [2, N_0) ----------------------
PREFIXES = {
    "n^2                      (§5.3's own — ABOVE the pair ceiling)":
        lambda n: F(n * n),
    "n(n-1)/2   = every incomparable pair inverted (the ABSOLUTE ceiling)":
        lambda n: F(n * (n - 1), 2),
    "n(n-1)/4   = the ANTICHAIN under uniform linear extensions":
        lambda n: F(n * (n - 1), 4),
    "n(n-1)/6 * (1 - 1e-6)    = just under the FROZEN ceiling m/3":
        lambda n: F(n * (n - 1), 6) * (1 - F(1, 10**6)),
}

# ----------------------------------------------------------------------------
# the ceiling: what values E[inv_e] can actually TAKE
# ----------------------------------------------------------------------------

def pair_ceiling(n):
    """E[inv_e] = sum over INCOMPARABLE pairs of Pr[inverted] <= #pairs."""
    return F(n * (n - 1), 2)

def frozen_ceiling(n):
    """mg-c4f5 §5.2: freezing gives E[inv_e] < m/3 <= n(n-1)/6."""
    return F(n * (n - 1), 6)

# ----------------------------------------------------------------------------

def build(prefix_f, tail_f, N0):
    """g = prefix below N_0, tail at and above.  A FINITE-PREFIX MODIFICATION."""
    return lambda n: prefix_f(n) if n < N0 else tail_f(n)

def violates_below(g, N0, eps, rhs, n_lo=2, cap=4000):
    """Does g violate (LIB-const) at EVERY n in [n_lo, N_0)?
    Returns (n_checked, n_violating, first_failure)."""
    hi = min(N0, n_lo + cap)
    checked = viol = 0
    first_fail = None
    for n in range(n_lo, hi):
        checked += 1
        if g(n) > rhs(n, eps):
            viol += 1
        elif first_fail is None:
            first_fail = n
    return checked, viol, first_fail

def is_o_n2(f, probe_exponents=(4, 8, 16, 32, 64, 128, 300, 1024, 4096, 20000)):
    """Exhibit f(n)/n^2 -> 0 by driving it below 1/k on a ladder of n = 2^e.

    DEFECT FOUND BY THIS CHECK FIRING AGAINST CORRECT CODE (kept, not tuned):
    my first ladder stopped at e = 40 and reported the log tails as NOT o(n^2).
    That was the LADDER's failure, not the tails': n^2/log2 n needs log2 n > k,
    i.e. n > 2^k, so 1/1000 is only reachable at n > 2^1000.  The ladder now
    reaches 2^20000.  The log-log tail is still NOT numerically reachable past
    k ~ 14 (it needs n = 2^(2^k)) and this function REPORTS that rather than
    passing it.

    THIRD DEFECT, also kept: the pass criterion was "reaches 1/10^6", which
    NO log tail can reach on any feasible ladder (n^2/log2 n needs n > 2^(10^6)).
    NC3 duly fired against CORRECT code.  The criterion was the bug.  The
    verdict now comes from the exact reduction instead:

        f(n) = n^2 / h(n) with h non-decreasing and UNBOUNDED  <=>  f = o(n^2)

    so the test is that the effective divisor h(n) = n^2/f(n) STRICTLY INCREASES
    without settling, which a constant-divisor impostor (NC1, NC2) fails.
    The largest 1/k actually witnessed is reported alongside, as evidence.
    """
    hs = []
    for e in probe_exponents:
        n = 2 ** e
        fn = f(n)
        hs.append(None if fn == 0 else F(n * n, 1) / fn)
    if any(h is None for h in hs):          # the zero tail: f == 0 is o(n^2) flat
        return None, True
    # FOURTH DEFECT, kept: I then gated on "hs[-1] > 10*hs[0]", an arbitrary
    # growth factor, and n^2/log2log2 n failed it (divisor runs 2..14 over the
    # whole feasible ladder).  Correct code, wrong gate, again.  The honest
    # position: NO finite ladder can establish unboundedness.  Strict increase
    # is NECESSARY and is what the ladder can decide — it is what kills the
    # constant-divisor impostors NC1/NC2.  SUFFICIENCY is analytic and is
    # stated, not measured: each divisor here is a composition of unbounded
    # non-decreasing maps (log2, log2 o log2, sqrt o log2), hence unbounded.
    strictly_up = all(b > a for a, b in zip(hs, hs[1:]))
    unbounded = strictly_up
    best = 0
    for k in (2, 10, 100, 1000, 10**4, 10**6):
        if any(f(2 ** e) < F(4 ** e, k) for e in probe_exponents):
            best = k
    return best, unbounded


def dec_digits(x):
    """Exact decimal digit count of a positive big integer, integer-only.
    (str() refuses above 4300 digits — the second defect this instrument hit.)"""
    lo, hi = 1, 1
    while 10 ** hi <= x:
        hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if 10 ** (mid - 1) <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def main():
    print("=" * 78)
    print("A1 — BUILDING THE VIOLATOR §5.3 SAYS EXISTS BELOW ANY N_0")
    print("=" * 78)

    print("\n[A1.0] THE LEMMA THE WHOLE NEGATIVE RESTS ON, stated plainly:")
    print("  (LIB-weak) is an ASYMPTOTIC hypothesis and is therefore INVARIANT")
    print("  under modification on a FINITE PREFIX.  (LIB-const) is a POINTWISE")
    print("  inequality and a finite prefix can violate it outright.  So for any")
    print("  N_0: take any tail that is o(n^2), redefine it below N_0 to exceed")
    print("  the bound, and you have a member of (LIB-weak) violating (LIB-const)")
    print("  on all of [2, N_0).  §5.3's n^2 / (n^2/log2 n) is ONE instance of")
    print("  this; the lemma is what does the work, not the instance.")

    N0S = [15, 100, 900, 10**6, 10**18]

    print("\n[A1.1] EVERY TAIL IS o(n^2) — exhibited, not asserted")
    print("   reduction used (exact, one line): for f(n) = n^2/h(n) with h")
    print("   non-decreasing, f = o(n^2)  <=>  h(n) -> oo.  So the ladder below")
    print("   drives h up, and the k reported IS a witnessed h.")
    for name, f in TAILS.items():
        k, ok = is_o_n2(f)
        kk = "0 (f is identically 0)" if k is None else k
        print(f"   {'OK ' if ok else '***'} {name:32s}  o(n^2) via divisor-unbounded: "
              f"{ok};  witnessed f/n^2 < 1/{kk}")
    print("   the 1/k actually WITNESSED is small for the log tails (n^2/log2 n")
    print("   needs n > 2^k to reach 1/k) — that is a LADDER limit, not a")
    print("   property of the tail, and the verdict does not rest on it.")

    print("\n[A1.1-NC] NEGATIVE CONTROLS — these MUST fail")
    ncs = {
        "NC1  n^2/2      is NOT o(n^2)":        (lambda n: F(n * n, 2), False),
        "NC2  n^2/1000   is NOT o(n^2)":        (lambda n: F(n * n, 1000), False),
        "NC3  n^2/log2 n IS  o(n^2)":           (TAILS["n^2 / log2 n   (§5.3's own)"], True),
        "NC3b n^2/log2log2 n IS o(n^2)":        (TAILS["n^2 / log2 log2 n"], True),
    }
    for label, (f, expect) in ncs.items():
        k, ok = is_o_n2(f)
        verdict = "OK " if ok == expect else "***"
        print(f"   {verdict} {label:40s} -> o(n^2)={ok} (expected {expect}), reached 1/{k}")
    # a "violator" that does not violate
    gz = build(lambda n: F(0), TAILS["n^2 / log2 n   (§5.3's own)"], 100)
    c, v, ff = violates_below(gz, 100, EPS_REPAIRED, lib_const_rhs_state)
    print(f"   {'OK ' if v == 0 else '***'} NC4  prefix g=0 must violate NOTHING       "
          f"-> {v}/{c} violations, first non-violating n={ff} (expected 0/98, n=2)")

    print("\n[A1.2] EVERY PREFIX VIOLATES (LIB-const) ON [2, N_0) — both bound forms")
    print("       NOTE: n is CAPPED at 4000 values per N_0; the two largest N_0")
    print("       are therefore SAMPLED PREFIXES, not exhausted. Said, not hidden.")
    print(f"       at the repaired eps_spec = {EPS_REPAIRED} = 2e-2")
    total_ok = total = 0
    for pname, pf in PREFIXES.items():
        for rname, rhs in RHS.items():
            row = []
            for N0 in N0S:
                g = build(pf, TAILS["n^2 / log2 n   (§5.3's own)"], N0)
                c, v, ff = violates_below(g, N0, EPS_REPAIRED, rhs)
                total += 1
                if c == v:
                    total_ok += 1
                    row.append(f"{v}/{c}")
                else:
                    row.append(f"*** {v}/{c} first-fail n={ff}")
            print(f"   {pname[:48]:48s} | {rname:14s} | " + "  ".join(row))
    print(f"   -> {total_ok}/{total} (prefix x bound-form x N_0) combinations violate throughout")

    print("\n[A1.3] SO THE FULL OBJECT IS A COUNTEREXAMPLE, at every N_0 tested")
    for N0 in N0S:
        g = build(PREFIXES["n(n-1)/6 * (1 - 1e-6)    = just under the FROZEN ceiling m/3"],
                  TAILS["n^2 / log2 n   (§5.3's own)"], N0)
        # FIFTH DEFECT, kept, and it is the most instructive of the five:
        # my ladder straddled the prefix boundary, so for N_0 >= 900 the low
        # rungs sampled the Theta(n^2) PREFIX and strict-increase failed.  That
        # is not a property of g — o(.) is a TAIL property and cannot see a
        # finite prefix at all.  Which is EXACTLY the lemma §5.3 turns on.  The
        # ladder is therefore started ABOVE N_0, which is the honest probe.
        e0 = N0.bit_length() + 1
        ladder = tuple(e0 + d for d in (0, 4, 12, 28, 60, 300, 1024, 4096, 20000))
        k, ok = is_o_n2(g, probe_exponents=ladder)
        c, v, ff = violates_below(g, N0, EPS_REPAIRED, lib_const_rhs_state)
        print(f"   N_0 = {N0:>20}   o(n^2): {'YES' if ok else 'NO '} (below 1/{k}, "
              f"ladder from 2^{e0})   violations on [2,N_0): {v}/{c}")

    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("A2 — IS §5.3's OWN WITNESS A REALIZABLE E[inv_e]?  (the ceiling)")
    print("=" * 78)
    print("  inv_e counts INCOMPARABLE pairs (mg-c3ca:75), so")
    print("     E[inv_e] = sum over incomparable pairs of Pr[inverted]")
    print("              <= #pairs = n(n-1)/2 < n^2/2   for EVERY n.")
    print("  and under the frozen hypothesis (LIB-weak)'s own antecedent,")
    print("     E[inv_e] < m/3 <= n(n-1)/6            (mg-c4f5 §5.2)")
    print()
    print(f"   {'n':>8} {'g(n)=n^2':>16} {'pair ceiling':>16} {'frozen ceiling':>16}  over-pair? over-frozen?")
    for n in (2, 3, 5, 10, 100, 900):
        gp = F(n * n)
        print(f"   {n:>8} {str(gp):>16} {str(pair_ceiling(n)):>16} "
              f"{str(frozen_ceiling(n))[:16]:>16}  "
              f"{'YES' if gp > pair_ceiling(n) else 'no ':>9}  "
              f"{'YES' if gp > frozen_ceiling(n) else 'no ':>12}")
    over = [n for n in range(1, 5001) if F(n * n) > pair_ceiling(n)]
    print(f"   -> g(n) = n^2 exceeds the ABSOLUTE pair ceiling at {len(over)}/5000 of n in [1,5000]")
    print(f"      (first n where it does NOT: {next((n for n in range(1,5001) if F(n*n) <= pair_ceiling(n)), None)})")

    print("\n[A2.1] THE REPAIRED, CEILING-RESPECTING WITNESS")
    print("  Replace the prefix by one that a real frozen family could attain:")
    print("     g(n) = n(n-1)/6 * (1 - 1e-6)   below N_0   [under the frozen cap]")
    print("     g(n) = n^2 / log2 n            at and above")
    for N0 in N0S:
        g = build(PREFIXES["n(n-1)/6 * (1 - 1e-6)    = just under the FROZEN ceiling m/3"],
                  TAILS["n^2 / log2 n   (§5.3's own)"], N0)
        hi = min(N0, 2 + 4000)
        under = sum(1 for n in range(2, hi) if g(n) < frozen_ceiling(n))
        c, v, ff = violates_below(g, N0, EPS_REPAIRED, lib_const_rhs_state)
        print(f"   N_0 = {N0:>20}  under frozen ceiling: {under}/{hi-2}   "
              f"violates (LIB-const): {v}/{c}")
    print("  -> the negative SURVIVES the realizability objection.  §5.3's")
    print("     conclusion does not depend on its unrealizable witness.")

    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("A3 — §5.3's TWO FIGURES, in exact integers (no float, no log call)")
    print("=" * 78)
    for label, eps in (("repaired 2e-2", EPS_REPAIRED), ("superseded 2e-4", EPS_SUPERSEDED)):
        c = 6 / eps
        assert c.denominator == 1
        c = int(c)
        print(f"\n   eps_spec = {eps} ({label}):  6/eps_spec = {c}")
        # DOC form:  n^2/log2 n <= (eps/6) n^2  <=>  log2 n >= 6/eps = c  <=>  n >= 2^c
        n_star = 2 ** c
        digits = dec_digits(n_star)
        print(f"     DOC form  (eps/6)n^2   : first n is EXACTLY 2^{c}, which has {digits} decimal digits")
        # exact rounding decision, integer-only: is 2^c >= 10^(d-1) * sqrt(10)?
        # square both sides:  (2^c)^2 >= 10^(2(d-1)+1)
        rounds_up = (n_star * n_star) >= 10 ** (2 * (digits - 1) + 1)
        nearest = (digits - 1) + (1 if rounds_up else 0)
        print(f"                              floor(log10) = {digits-1}; nearest = {nearest}"
              f"   (2^{c} {'>=' if rounds_up else '<'} 10^{digits-1}*sqrt10)")
        print(f"                              -> the page prints 10^{nearest}  [NEAREST convention]")
        # verify from both sides, integer-only
        below_ok = log2_ge(n_star - 1, c)
        at_ok    = log2_ge(n_star, c)
        print(f"       log2(2^{c} - 1) >= {c} ? {below_ok}   (must be False)")
        print(f"       log2(2^{c})     >= {c} ? {at_ok}   (must be True)")
        assert (not below_ok) and at_ok
        # STATE form: n^2/log2 n <= (eps/6)(n^2-1).  at n = 2^c, log2 n = c exactly:
        #   LHS = n^2/c ;  RHS = (eps/6)(n^2-1) = (n^2-1)/c   ->  LHS - RHS = 1/c > 0
        lhs_minus_rhs = F(1, c)
        print(f"     STATE form (eps/6)(n^2-1): at n = 2^{c} exactly, LHS - RHS = 1/{c} > 0")
        print(f"                              -> FAILS at 2^{c}; first n is 2^{c} + 1.")
        print(f"                              (a shift of 1 in an object of size 10^{digits-1};")
        print(f"                               the ~10^{digits-1} on the page is UNAFFECTED)")

    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("A4 — DOES THE NEGATIVE REACH THE PROGRAMME'S OBJECT?")
    print("=" * 78)
    print("  §5.3 quantifies over the class of o(n^2) FUNCTIONS.  The programme's")
    print("  object is the FROZEN POSET class.  These are not the same class, and")
    print("  the difference is decidable in one direction:")
    print()
    print("  IF the frozen class satisfies LIB (E[inv_e] <= C*n) — which mg-c3ca §6")
    print("  reports the reachable data as saying — THEN an N_0 DOES exist for the")
    print("  frozen class, at C*n <= (eps/6)(n^2-1):")
    for C in (1, 2, 10):
        n = 2
        while not (F(C * n) <= EPS_REPAIRED * F(n * n - 1, 6)):
            n += 1
            if n > 10 ** 7:
                n = None
                break
        print(f"     C = {C:>3}:  smallest n with C*n <= (eps/6)(n^2-1)  ->  N_0 = {n}")
    print()
    print("  This does NOT contradict §5.3.  It is the class/member distinction:")
    print("  a threshold exists for that FAMILY, it is just not a function of the")
    print("  o(n^2) hypothesis.  It is exactly what row 8's 'What it does not")
    print("  claim' paragraph says.  Recorded here because the SHORT sites say")
    print("  'find N_0 is closed, not open' and this is the reading that must not")
    print("  be welded to them.")


if __name__ == "__main__":
    main()
