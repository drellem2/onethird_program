"""s0 — the forced arms of lib51f4.  Every arm ASSERTS; a silent pass is not a pass.

The arms exist because of the errors filed in PREDICTIONS.md E1-E9, and each one names the
error it guards.  Four of them are NEGATIVE controls: they assert that a deliberately broken
version of the instrument gets caught, because a control that cannot fail is not a control
(this lineage has now recorded that lesson three times).
"""

from fractions import Fraction as F
from itertools import combinations, permutations
import math
import sys

import lib51f4 as L
from lib51f4 import (Pos, all_posets, brute_T, pencil, psi, from_coeffs, is_monotone,
                     gap_greater, gap_at_least, gap_bracket, gap_float, cone_min,
                     mu_bracket, mu_pref_exact_upper, copositive, simplex_min,
                     measure, floor_msharp, sweep_bound_sq, fam_antichain,
                     fam_chain_plus_point, fam_near_ordinal_antichains)

PASS = []


def arm(name, fn):
    try:
        detail = fn()
    except AssertionError as e:
        print("  FAIL  %-6s %s" % (name, e))
        PASS.append((name, False))
        return
    print("  ok    %-6s %s" % (name, detail))
    PASS.append((name, True))


P5 = all_posets(5)
P4 = all_posets(4)
SMALL = P4 + P5


# ------------------------------------------------------------------ A1  down-sets
def a1():
    """E9: the down-set lattice is walked, not the whole subset lattice."""
    n_checked = 0
    for P in SMALL:
        n = P.n
        brute = set()
        for m in range(1 << n):
            ok = True
            for x in range(n):
                if m >> x & 1 and (P.down[x] & ~m):
                    ok = False
                    break
            if ok:
                brute.add(m)
        got = set(P.downsets())
        assert got == brute, f"{P.name}: down-set set mismatch"
        assert len(got) <= 1 << n
        n_checked += 1
    # MUTATION (E9): the mg-9461 defect -- peel ANY element whose down-set is inside the
    # remainder, which is true of every minimal element of the WHOLE poset as well, so the
    # walk leaves the down-set lattice.  It must visit strictly more states somewhere.
    worse = 0
    for P in SMALL[:60]:
        n = P.n
        seen, fr = {0}, [0]
        while fr:
            nxt = []
            for D in fr:
                for x in range(n):
                    if D >> x & 1:
                        continue
                    if P.down[x] & ~((1 << n) - 1):        # broken guard: vacuously true
                        continue
                    E = D | (1 << x)
                    if E not in seen:
                        seen.add(E)
                        nxt.append(E)
            fr = nxt
        if len(seen) > len(P.downsets()):
            worse += 1
    assert worse > 0, "the mutated walk was never larger -- the check cannot discriminate"
    return (f"{n_checked} posets: down-set lattice == brute force; the mg-9461-shaped "
            f"mutation inflates the state count at {worse} of 60")


# ------------------------------------------------------------------ A2  transport
def a2():
    """E9: the DP transport equals the n!-enumeration transport."""
    cnt = 0
    for P in SMALL:
        Tb, N = brute_T(P)
        assert N == P.nle(), f"{P.name}: linear-extension count {N} vs {P.nle()}"
        assert Tb == P.Tint(), f"{P.name}: transport mismatch"
        cnt += 1
    P6 = all_posets(6)
    for P in P6[::40]:
        Tb, N = brute_T(P)
        assert N == P.nle() and Tb == P.Tint(), f"{P.name}: n=6 transport mismatch"
        cnt += 1
    for P in [fam_antichain(7), fam_chain_plus_point(7),
              fam_near_ordinal_antichains(7, 1), fam_near_ordinal_antichains(7, 2)]:
        Tb, N = brute_T(P)
        assert N == P.nle() and Tb == P.Tint(), f"{P.name}: n=7 transport mismatch"
        cnt += 1
    return f"{cnt} posets (all n<=5, every 40th at n=6, 4 named at n=7), 0 mismatches"


# ------------------------------------------------------------------ A3  leak == cut
def a3():
    """leak from the DEFINITION equals the cut weight in S_P."""
    cnt = 0
    for P in SMALL:
        S, n = P.S(), P.n
        for k in range(1, n):
            cut = sum(S[i][j] for i in range(k) for j in range(k, n))
            assert P.leak_pref(k) == cut, f"{P.name}: leak(A_{k}) != cut"
            assert P.leak_pref(k) == P.energy([F(1)] * k + [F(0)] * (n - k)), \
                f"{P.name}: leak(A_{k}) != energy(1_A)"
            cnt += 1
    return f"{cnt} prefix cuts: leak(A_k) == w(A_k,A_k^c) == energy(1_A_k), exactly"


# ------------------------------------------------------------------ A4  the pencil
def a4():
    cnt = 0
    for P in SMALL:
        Q, N = pencil(P, closed_form=True)
        Q2, N2 = pencil(P, closed_form=False)
        assert Q == Q2 and N == N2, f"{P.name}: pencil closed form != literal"
        for k in range(1, P.n):
            assert Q[k - 1][k - 1] == P.leak_pref(k), f"{P.name}: Q_kk != leak(A_k)"
        cnt += 1
    return f"{cnt} posets: closed form == literal evaluation, and Q_kk == leak(A_k)"


# ------------------------------------------------------------------ A5  the cone
def a5():
    """{sum c_k psi_k : c >= 0} is exactly the monotone cone in 1^perp."""
    n = 6
    for c in [[F(1), F(0), F(2), F(0), F(3)], [F(0)] * 4 + [F(1)], [F(1)] * 5]:
        v = from_coeffs(n, c)
        assert sum(v) == 0, "psi combination not centred"
        assert is_monotone(v), "nonneg coefficients gave a non-monotone vector"
    # and back: a monotone centred vector decomposes with nonneg coefficients
    v = [F(-5), F(-2), F(-2), F(1), F(3), F(5)]
    assert sum(v) == 0 and is_monotone(v)
    c = [v[k] - v[k - 1] for k in range(1, n)]
    assert all(x >= 0 for x in c)
    assert from_coeffs(n, c) == v, "reconstruction from consecutive differences failed"
    # NEGATIVE: one negative coefficient must break monotonicity somewhere
    bad = from_coeffs(n, [F(1), F(-1), F(0), F(0), F(0)])
    assert not is_monotone(bad), "a negative coefficient stayed monotone"
    return "psi cone == monotone cone, both directions, and a negative coefficient breaks it"


# ------------------------------------------------------------------ A6  gap, two devices
def _faddeev_psd(A):
    """PSD of a symmetric rational matrix by the SIGNS OF THE CHARACTERISTIC POLYNOMIAL's
    elementary symmetric functions (Faddeev-LeVerrier).  A DIFFERENT DEVICE from the
    Sylvester/Bareiss minors used in lib51f4 -- this arm exists to compare them (E5)."""
    m = len(A)
    M = [[F(1) if i == j else F(0) for j in range(m)] for i in range(m)]
    for k in range(1, m + 1):
        AM = [[sum(A[i][t] * M[t][j] for t in range(m)) for j in range(m)]
              for i in range(m)]
        c = sum(AM[i][i] for i in range(m)) / k
        e = c if k % 2 == 1 else -c
        if e < 0:
            return False
        M = [[AM[i][j] - (c if i == j else F(0)) for j in range(m)] for i in range(m)]
    return True


def _gap_at_least_faddeev(P, r):
    """`gamma >= r` as PSD of (I - S_P) - r(I - J/n) on the FULL n x n space."""
    n = P.n
    S = P.S()
    B = [[(F(1) if i == j else F(0)) - S[i][j]
          - r * ((F(1) if i == j else F(0)) - F(1, n)) for j in range(n)]
         for i in range(n)]
    return _faddeev_psd(B)


def a6():
    cnt = 0
    for P in SMALL:
        for r in [F(0), F(1, 10), F(1, 4), F(1, 3), F(1, 2), F(3, 4), F(1), F(3, 2)]:
            a = gap_at_least(P, r)
            b = _gap_at_least_faddeev(P, r)
            assert a == b, f"{P.name} r={r}: pencil says {a}, Faddeev says {b}"
            cnt += 1
    P6 = all_posets(6)
    for P in P6[::20]:
        for r in [F(1, 10), F(1, 4), F(1, 2)]:
            assert gap_at_least(P, r) == _gap_at_least_faddeev(P, r), f"{P.name} n=6"
            cnt += 1
    return (f"{cnt} (poset, threshold) decisions: Sylvester-on-the-pencil == "
            f"Faddeev-on-the-Laplacian, 0 disagreements")


# ------------------------------------------------------------------ C1 negative control
def c1():
    """The A6 comparison must be able to DISAGREE, or it is not testing anything."""
    P = fam_antichain(4)

    def broken(Pp, r):                     # drops the (I - J/n) shift: wrong operator
        n = Pp.n
        S = Pp.S()
        B = [[(F(1) if i == j else F(0)) - S[i][j] - r * (F(1) if i == j else F(0))
              for j in range(n)] for i in range(n)]
        return _faddeev_psd(B)
    diff = sum(1 for r in [F(1, 10), F(1, 2), F(9, 10)]
               if gap_at_least(P, r) != broken(P, r))
    assert diff > 0, "the broken operator agreed everywhere -- A6 cannot discriminate"
    return f"a deliberately wrong Laplacian shift disagrees at {diff} of 3 thresholds"


# ------------------------------------------------------------------ A7 bracket sanity
def a7():
    cnt = 0
    for P in SMALL[:120]:
        if not P.is_primitive():
            continue
        lo, hi = gap_bracket(P, iters=40)
        g = gap_float(P)
        assert lo <= hi, f"{P.name}: inverted bracket"
        assert float(lo) - 1e-9 <= g <= float(hi) + 1e-9, \
            f"{P.name}: float gap {g} outside exact bracket [{float(lo)},{float(hi)}]"
        assert gap_greater(P, lo) and not gap_greater(P, hi), \
            f"{P.name}: bracket endpoints do not straddle"
        cnt += 1
    A = fam_antichain(5)
    lo, hi = gap_bracket(A, iters=40)
    assert lo <= F(1) <= hi, "antichain gamma is 1 and the bracket must contain it"
    return f"{cnt} primitive posets: float gap inside the exact bracket, endpoints straddle"


# ------------------------------------------------------------------ A8 copositivity
def a8():
    cases = [([[F(1), F(0)], [F(0), F(1)]], True),
             ([[F(1), F(-3)], [F(-3), F(1)]], False),
             ([[F(0), F(-1)], [F(-1), F(0)]], False),
             ([[F(1), F(-1)], [F(-1), F(1)]], True),          # singular face, min = 0
             ([[F(-1), F(2)], [F(2), F(-1)]], False),
             ([[F(2), F(-1), F(0)], [F(-1), F(2), F(-1)], [F(0), F(-1), F(2)]], True)]
    for A, want in cases:
        assert copositive(A) is want, f"copositive{A} != {want}"
    # NEGATIVE CONTROL: the Horn matrix is copositive but sits on the boundary with a
    # degenerate face.  The instrument must REFUSE rather than guess (PREDICTIONS E3).
    H = [[F(1), F(-1), F(1), F(1), F(-1)],
         [F(-1), F(1), F(-1), F(1), F(1)],
         [F(1), F(-1), F(1), F(-1), F(1)],
         [F(1), F(1), F(-1), F(1), F(-1)],
         [F(-1), F(1), F(1), F(-1), F(1)]]
    refused = False
    try:
        copositive(H)
    except ValueError:
        refused = True
    assert refused, "the Horn matrix was answered rather than refused -- the test guesses"
    assert simplex_min(H) is None
    return "6 hand cases exact; the Horn matrix is REFUSED, not guessed"


# ------------------------------------------------------------------ A9 mu bracket
def a9():
    cnt = 0
    for P in SMALL[::7]:
        if not P.is_primitive():
            continue
        lo, hi = mu_bracket(P, iters=32)
        fv, _ = cone_min(P)
        up, _ = mu_pref_exact_upper(P)
        assert lo <= up + F(1, 10 ** 6), f"{P.name}: exact lower {float(lo)} > exhibited {float(up)}"
        assert abs(float(lo) - fv) < 1e-6, \
            f"{P.name}: exact bracket {float(lo)} vs float cone min {fv}"
        glo, ghi = gap_bracket(P, iters=40)
        assert hi >= glo - F(1, 10 ** 9), f"{P.name}: mu_pref below gamma -- impossible"
        cnt += 1
    return (f"{cnt} primitive posets: exact copositivity bracket on mu_pref agrees with the "
            f"float cone minimiser to 1e-6, and never falls below gamma")


# ------------------------------------------------------------------ A10 the footrule
def a10():
    """Sum of prefix leaks == half the expected Spearman footrule (mg-28ff Sec 3).

    Taken as read as a THEOREM; asserted here as a control on MY leak and MY E[D_F].
    """
    cnt = 0
    for P in SMALL:
        s = sum(P.leak_pref(k) for k in range(1, P.n))
        assert s * 2 == P.E_footrule(), f"{P.name}: {s} vs {P.E_footrule()}"
        cnt += 1
    # NEGATIVE (C2): the mutated constant 1/3 must be satisfied by nothing with a footrule
    bad = sum(1 for P in SMALL
              if P.E_footrule() != 0
              and sum(P.leak_pref(k) for k in range(1, P.n)) * 3 == P.E_footrule())
    assert bad == 0, f"the mutated constant 1/3 was satisfied at {bad} posets"
    return f"{cnt} posets exact; the mutated constant 1/3 holds at 0 with a nonzero footrule"


# ------------------------------------------------------------------ A11 Phi*_pref
def a11():
    """The profile's minimum equals a brute-force minimum over prefixes computed straight
    from the linear extensions, with no matrix and no DP in the path."""
    cnt = 0
    for P in SMALL[::3]:
        n = P.n
        les = [p for p in permutations(range(n))
               if all(p.index(x) < p.index(y)
                      for x in range(n) for y in range(n) if P.up[x] >> y & 1)]
        best = None
        for k in range(1, n):
            A = set(range(k))
            tot = sum(len(A) - len(A & {p[i] for i in A}) for p in les)
            v = F(tot, len(les)) / min(k, n - k)
            best = v if best is None or v < best else best
        assert best == P.phi_star_pref()[0], f"{P.name}: Phi*_pref mismatch"
        cnt += 1
    return f"{cnt} posets: Phi*_pref from linear extensions == Phi*_pref from the profile"


# ------------------------------------------------------------------ A12 the floor
def a12():
    """The floor's entire content, exactly: gamma <= mu_pref at every primitive poset."""
    cnt = 0
    for P in SMALL:
        if not P.is_primitive():
            continue
        up, _ = mu_pref_exact_upper(P)
        assert not gap_greater(P, up), f"{P.name}: gamma > mu_pref -- floor refuted"
        r = measure(P, iters=44)
        assert r.c_sharp_lo >= floor_msharp(r) - F(1, 10 ** 9), \
            f"{P.name}: c# below its floor beyond bracket width"
        cnt += 1
    return f"{cnt} primitive posets n<=5: gamma <= mu_pref, so c# >= Delta_P - gamma/2"


# ------------------------------------------------------------------ C3 the red drill
def c3():
    """The pipeline must be able to print FAIL, on both routes, and must NOT print it on
    posets where the routes hold.  Both directions, or the refutations mean nothing."""
    PF = fam_near_ordinal_antichains(7, 1)
    M = PF.M_mean()
    assert not gap_at_least(PF, M * M / 2), "(F) did not fail at its own witness"
    PA = fam_antichain(6)
    MA = PA.M_mean()
    assert gap_at_least(PA, MA * MA / 2), "(F) failed at the antichain, where it holds"
    PM = fam_chain_plus_point(13)
    lo, _ = mu_bracket(PM, iters=30)
    assert not gap_at_least(PM, sweep_bound_sq(PM.delta_max(), lo) / 2), \
        "(M#) did not fail at its own witness"
    PM2 = fam_chain_plus_point(8)
    lo2, _ = mu_bracket(PM2, iters=30)
    assert gap_at_least(PM2, sweep_bound_sq(PM2.delta_max(), lo2) / 2), \
        "(M#) failed at n=8, where it holds"
    return ("(F) FAILS at near-ordinal(7) and HOLDS at antichain(6); "
            "(M#) FAILS at chain+point(13) and HOLDS at chain+point(8)")


# ------------------------------------------------------------------ C4 disjunction bite
def c4():
    """min(c#,f*) must be attained by BOTH arguments somewhere, or the disjunction is a
    relabelling of one route (PREDICTIONS.md E7).

    THIS ARM CAUGHT A DEFECT IN ITSELF AND THE REPLACEMENT IS THE FINDING.  Its first
    version asserted at n = 5 and FAILED: at all 275 primitive posets on 5 elements f* is
    the smaller of the two, so at n <= 5 the disjunction IS route (F) and nothing else.
    That is a fact about the population, not about the code — (M#) does not start binding
    anywhere until n = 6 — and the arm now asserts BOTH: the n=5 uniformity, and the n=6
    two-sidedness that makes min() non-trivial.
    """
    b5c = b5f = 0
    for P in P5:
        if not P.is_primitive():
            continue
        r = measure(P, iters=40)
        if r.c_sharp_hi < r.f_hi:
            b5c += 1
        elif r.f_hi < r.c_sharp_hi:
            b5f += 1
    assert b5c == 0 and b5f == 275, f"n=5 uniformity changed: {b5c}/{b5f}"
    byc = byf = 0
    for P in all_posets(6)[::3]:
        if not P.is_primitive():
            continue
        r = measure(P, iters=40)
        if r.c_sharp_hi < r.f_hi:
            byc += 1
        elif r.f_hi < r.c_sharp_hi:
            byf += 1
    assert byc > 0 and byf > 0, f"at n=6 the min is always the same side: {byc}/{byf}"
    return (f"n=5: f* is the smaller at all 275 primitive posets, c# at 0 — the disjunction "
            f"IS (F) there; n=6 (every 3rd poset): c# smaller at {byc}, f* at {byf}, so "
            f"min() bites from n=6 on")


# ------------------------------------------------------------------ C5 population
def c5():
    """The enumerated population is the one claimed."""
    counts = {2: 2, 3: 7, 4: 40, 5: 357}
    for n, c in counts.items():
        got = len(all_posets(n))
        assert got == c, f"n={n}: {got} posets, expected {c}"
    tot6 = len(all_posets(6))
    assert tot6 == 4824, f"n=6: {tot6}"
    assert 2 + 7 + 40 + 357 + 4824 == 5230, "totals do not reach mg-28ff's 5230"
    # every enumerated poset really has the identity as a linear extension
    for P in P5[::11]:
        assert P.nle() >= 1 and all(x < y for (x, y) in P.rel_pairs())
    return "2/7/40/357/4824 = 5230 over n=2..6, matching mg-28ff's population exactly"


print("s0 — lib51f4 forced arms")
print()
for nm, fn in [("A1", a1), ("A2", a2), ("A3", a3), ("A4", a4), ("A5", a5), ("A6", a6),
               ("C1", c1), ("A7", a7), ("A8", a8), ("A9", a9), ("A10", a10),
               ("A11", a11), ("A12", a12), ("C3", c3), ("C4", c4), ("C5", c5)]:
    arm(nm, fn)
print()
ok = sum(1 for _, v in PASS if v)
print("%d/%d arms pass" % (ok, len(PASS)))
sys.exit(0 if ok == len(PASS) else 1)
