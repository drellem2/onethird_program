"""a1 -- INDEPENDENT RE-CERTIFICATION of mg-789d's four counterexamples to (L*).

The instrument is lib5cba (audited in a0).  Nothing here reads lib789d.py.
Every verdict is an integer / Fraction decision:

    (F) FAILS        <=>  R(M^2/2) is NOT PSD
    gamma  <  g      <=>  R(g)     is NOT PSD
    mu_pref >= s     <=>  R(s)     IS COPOSITIVE
    (L*) FAILS at P  <=>  (F) fails at P  AND  mu_pref * Delta > gamma

and the last is certified from the two bracketing certificates s <= mu_pref and
gamma < g by the single rational comparison   s * Delta  >  g.
"""
import sys
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import lib5cba
from lib5cba import P5, height, copositive_int, psd_int, mu_pref_float, gamma_float

FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-62s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


# mg-789d's four certified counterexamples and its three controls, transcribed from
# out_s5_certify.txt.  Only the dn tuples and the claimed figures are taken from
# there; every verdict below is recomputed by lib5cba.
CANDIDATES = [
    ("C1  n=9   COUNTEREXAMPLE 1 (the smallest, the one the ticket names)",
     (0, 1, 0, 4, 0, 0, 32, 96, 239), 9,
     dict(LE=1890, height=4, Delta=Fraction(62, 63), M=Fraction(41, 84),
          gamma_lt=Fraction(23459, 200000), mu_ge=Fraction(6011, 50000),
          F_fails=True, refutes=True)),
    ("C2  n=9   COUNTEREXAMPLE 2",
     (0, 0, 0, 0, 0, 16, 48, 16, 247), 9,
     dict(LE=5670, height=4, Delta=Fraction(311, 315), M=Fraction(373, 756),
          gamma_lt=Fraction(118611, 1000000), mu_ge=Fraction(6087, 50000),
          F_fails=True, refutes=True)),
    ("C3  n=10  COUNTEREXAMPLE 3",
     (0, 1, 3, 0, 9, 0, 32, 96, 255, 239), 10,
     dict(LE=1148, height=4, Delta=Fraction(565, 574), M=Fraction(557, 1435),
          gamma_lt=Fraction(70327, 1000000), mu_ge=Fraction(911, 12500),
          F_fails=True, refutes=True)),
    ("C4  n=11  COUNTEREXAMPLE 4",
     (0, 1, 3, 7, 0, 1, 1, 113, 1, 257, 257), 11,
     dict(LE=57120, height=4, Delta=Fraction(135, 136), M=Fraction(7141, 14280),
          gamma_lt=Fraction(119917, 1000000), mu_ge=Fraction(12381, 100000),
          F_fails=True, refutes=True)),
    ("N1  n=7   NEGATIVE CONTROL: mg-c50b S4.1 argmax -- (L*) must HOLD",
     (0, 0, 0, 4, 4, 31, 29), 7,
     dict(LE=88, height=3, Delta=Fraction(10, 11), M=Fraction(31, 88),
          gamma_lt=Fraction(30821, 500000), mu_ge=Fraction(6263, 100000),
          F_fails=True, refutes=False)),
    ("N2  n=7   NEGATIVE CONTROL: mg-c50b S2.2 witness -- (L*) must HOLD",
     (0, 0, 0, 0, 15, 11, 15), 7,
     dict(LE=156, height=2, Delta=Fraction(10, 13), M=Fraction(305, 936),
          gamma_lt=Fraction(5423, 125000), mu_ge=Fraction(4337, 100000),
          F_fails=True, refutes=False)),
    ("P1  n=10  POSITIVE CONTROL: chain(9)+point -- mu*Delta > gamma, but (F) HOLDS",
     (0, 1, 3, 7, 15, 31, 63, 127, 255, 0), 10,
     dict(LE=10, height=9, Delta=Fraction(9, 10), M=Fraction(9, 50),
          gamma_lt=Fraction(40797, 500000), mu_ge=Fraction(4561, 50000),
          F_fails=False, refutes=False)),
]


def certify(tag, dn, n, exp=None, gsteps=34, msteps=None):
    global FAIL
    print("\n" + "-" * 78)
    print(tag)
    print("  dn = %s   n = %d" % (str(dn), n))
    p = P5(dn, n)
    D = p.Delta()
    M = p.M()
    print("  LE = %d   height = %d   primitive = %s" % (p.LE, height(dn, n), p.primitive()))
    print("  Delta   = %s = %.9f     (1 - Delta = min_i (S_P)_ii = %s)"
          % (D, float(D), 1 - D))
    print("  M       = %s = %.9f     M^2/2 = %s" % (M, float(M), M * M / 2))
    print("  argmin_i (S_P)_ii = %s  with (S_P)_ii = %s"
          % ([i for i in range(n) if p.dI[i] == p.DeltaI],
             Fraction(p.LE - p.DeltaI, p.LE)))
    arm("primitive", p.primitive())
    if exp:
        arm("LE = %d" % exp["LE"], p.LE == exp["LE"], str(p.LE))
        arm("height = %d" % exp["height"], height(dn, n) == exp["height"], str(height(dn, n)))
        arm("Delta = %s" % exp["Delta"], D == exp["Delta"], str(D))
        arm("M = %s" % exp["M"], M == exp["M"], str(M))

    # ---- (F) fails: EXACT, one integer PSD refusal -------------------------
    R, m = p.Rmat(M * M / 2)
    ok = psd_int(R, m)
    if exp:
        if exp["F_fails"]:
            arm("(F) FAILS: R(M^2/2) is NOT PSD, i.e. gamma < M^2/2", not ok)
        else:
            arm("(F) HOLDS: R(M^2/2) IS PSD, i.e. gamma >= M^2/2", ok)
    else:
        print("      (F) fails = %s" % (not ok))

    # ---- gamma upper certificate ------------------------------------------
    lo, hi = p.gamma_bracket(gsteps)
    print("  gamma in [%.12f, %.12f]  (exact bracket, %d bisections)"
          % (float(lo), float(hi), gsteps))
    if exp:
        g = exp["gamma_lt"]
        arm("gamma < %s = %.9f  (R NOT PSD)" % (g, float(g)), not p.gamma_ge(g))
    # a tight rational upper bound of our own
    g_up = hi
    arm("gamma < %.12f (our own bracket top, R NOT PSD)" % float(g_up), not p.gamma_ge(g_up))

    # ---- mu_pref lower certificate: EXACT COPOSITIVITY ---------------------
    if exp:
        s = exp["mu_ge"]
        R, m = p.Rmat(s)
        cop, w = copositive_int(R, m)
        arm("mu_pref >= %s = %.9f  (R IS COPOSITIVE, %dx%d integer)"
            % (s, float(s), m, m), cop)
    mlo, mhi = p.mu_bracket(msteps or 26, lo=Fraction(0), hi=Fraction(1))
    print("  mu_pref in [%.12f, %.12f]  (exact copositivity bracket)"
          % (float(mlo), float(mhi)))
    mf, vec = mu_pref_float(p)
    print("  mu_pref (independent f-space face path, float) = %.12f" % mf)
    arm("the two mu_pref paths agree (face path inside the exact bracket)",
        float(mlo) - 1e-9 <= mf <= float(mhi) + 1e-9)
    print("  gamma  (independent Jacobi path, float)        = %.12f" % gamma_float(p))

    # ---- the verdict --------------------------------------------------------
    print("  --- the (L*) verdict, from the two certificates only ---")
    if exp:
        lhs = exp["mu_ge"] * D
        rhs = exp["gamma_lt"]
        print("     mu_pref*Delta >= %s = %.9f" % (lhs, float(lhs)))
        print("     gamma          < %s = %.9f" % (rhs, float(rhs)))
        if exp["refutes"] or not exp["F_fails"]:
            arm("mu_pref*Delta > gamma  (ticket's own two certificates)", lhs > rhs,
                "%s > %s" % (lhs, rhs))
        else:
            arm("ticket's own certificates do NOT give mu*Delta > gamma here",
                not (lhs > rhs), "%s vs %s" % (lhs, rhs))
    lhs2 = mlo * D
    hi2 = mhi * D
    print("     our own:  mu_pref*Delta in [%s, %s] = [%.9f, %.9f]"
          % (lhs2, hi2, float(lhs2), float(hi2)))
    print("               gamma          in [%.9f, %.9f]" % (float(lo), float(g_up)))
    refuted = (not ok) and lhs2 > g_up
    holds = hi2 <= lo            # mu*Delta <= gamma certified in the OTHER direction
    if exp and exp["refutes"]:
        arm("mu_pref*Delta > gamma  (our own independent certificates)", lhs2 > g_up)
        arm("(L*) IS REFUTED AT THIS POSET: hypothesis holds, conclusion fails", refuted)
    elif exp:
        arm("(L*) is NOT refuted here (the certifier refuses, as it must)", not refuted)
        if exp["F_fails"]:
            arm("  and (L*)'s conclusion mu*Delta <= gamma is CERTIFIED to hold", holds)
        else:
            arm("  (F) holds, so (L*) is untouched here; mu*Delta > gamma anyway",
                lhs2 > g_up)
    vL = float(lhs2) / float(g_up)
    print("     v_L = mu_pref*Delta/gamma  >~ %.6f      v_F = M^2/(2 gamma) >~ %.6f"
          % (vL, float(M * M / 2) / float(g_up)))
    print("     min(v_F, v_L) >~ %.6f" % min(vL, float(M * M / 2) / float(g_up)))

    # ---- and the disjunction: does (M#) still hold here? -------------------
    # (M#) FAILS  <=>  mu(2 Delta - mu) > 2 gamma.   Certify it HOLDS by using the
    # UPPER bound on mu and the LOWER bound on gamma -- the hard direction for this
    # claim is the opposite one from (L*)'s, so the bracket ends swap.
    mu_hi = mhi
    g_lo = lo
    swp = mu_hi * (2 * D - mu_hi) if mu_hi <= D else D * D
    print("  --- (M#), certified in ITS hard direction (mu upper, gamma lower) ---")
    print("     sweep(mu_ub) = %.12f      2*gamma_lo = %.12f" % (float(swp), float(2 * g_lo)))
    arm("(M#) HOLDS here: sweep(mu_pref) <= 2 gamma", swp <= 2 * g_lo)
    import math
    if float(D) ** 2 > 2 * float(g_lo):
        tstar = float(D) - math.sqrt(float(D) ** 2 - 2 * float(g_lo))
        print("     t* = Delta - sqrt(Delta^2 - 2 gamma) = %.9f    u_M = mu/t* = %.6f"
              % (tstar, float(mu_hi) / tstar))
    return p


print("=" * 78)
print("a1  INDEPENDENT RE-CERTIFICATION of the (L*) counterexamples")
print("=" * 78)

for tag, dn, n, exp in CANDIDATES:
    certify(tag, dn, n, exp)

print("\n" + "-" * 78)
print("SINGULAR FACES met by the copositivity routine: %d, all DECIDED: %d"
      % (lib5cba.SINGULAR_FACES, lib5cba.SINGULAR_FACES_DECIDED))
arm("every singular face was DECIDED, none refused",
    lib5cba.SINGULAR_FACES == lib5cba.SINGULAR_FACES_DECIDED)

print("\n" + "=" * 78)
print("a1 RESULT: %s   (%d failing arms)" % ("ALL ARMS PASS" if FAIL == 0 else "FAILURES", FAIL))
print("=" * 78)
sys.exit(1 if FAIL else 0)
