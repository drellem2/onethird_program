"""mg-5371 -- what each heavy-atom shape q0(w, eps) gives for L* and Thm 1.2's eps.
The Thm 1.3 half (q0 -> L) is mg-b852's explicit chain, copied VERBATIM from
code/ksbft_g_constants_b852/constants.py (L_AK after its first line), re-parametrised by log10 q0.
Control: at q0 = (2eps)^(w^2) it must reproduce mg-b852's log10 L(4,1/6) = 119.1 and
log10 L* = 1.050e29 (printed as MATCH/MISMATCH).  No randomness."""
from decimal import Decimal as Dm, getcontext
import math

ctx = getcontext(); ctx.prec = 40; ctx.Emax = 10**17; ctx.Emin = -10**17
E = Dm(1).exp(); S3 = Dm(3).sqrt()
def lg(x): return x.log10()

def width_bound(eps):
    eps = Dm(eps)
    G1 = 10 * E * (1 + S3) / eps ** 3
    A = 18432 * S3 / eps ** 3
    G2 = 4 * A * A.ln() ** 2
    return 2 * S3 * max(G1, G2) / eps

def L_from_q0(log10_q0):
    """log10 L given log10 q0 (<= 0).  Body identical to mg-b852's L_AK after q0."""
    log10_q0 = Dm(log10_q0)
    q0 = Dm(10) ** log10_q0 if log10_q0 > -10**6 else None
    if q0 is not None:
        S = 300 / q0 ** 2
        eta = 1 / (16 * (S + 1).sqrt())
        log10_eta = lg(eta)
    else:
        log10_eta = log10_q0 - lg(16 * Dm(300).sqrt())
    mu = Dm(1) / 4
    gam = 3 * mu ** 3 / 160
    def P(a): return Dm(10) ** a
    if log10_eta > -300:
        eta_ = P(log10_eta)
        B = Dm(math.ceil(2 * float(E) / float(eta_)))
        K44 = (3 * B + 1) * (B + 1)
        TD = 4 * K44 + 1
        sig = Dm(300).sqrt() / eta_
        Dw = 3 * sig / eta_.sqrt()
        C = 2 * TD * Dw / gam
        t = 2 + 2 * TD * (6 / (gam * eta_)).ln()
        K32 = 80 * C * t / (eta_ * mu * mu)
        K31 = 2 * K32 + 2
        return 2 * lg(K31)
    lx = -log10_eta
    lnx = lx * Dm(10).ln()
    lg_K44 = lg(Dm(12)) + 2 * lg(E) + 2 * lx
    lg_TD = lg(Dm(4)) + lg_K44
    lg_Dw = lg(3 * Dm(300).sqrt()) + Dm('1.5') * lx
    lg_C = lg(Dm(2)) + lg_TD + lg_Dw - lg(gam)
    lg_t = lg(Dm(2)) + lg_TD + lg((6 / gam).ln() + lnx)
    lg_K32 = lg(Dm(80)) + lg_C + lg_t + lx - 2 * lg(mu)
    return 2 * (lg(Dm(2)) + lg_K32)

def fmt(x):
    x = Dm(x)
    if abs(x) < Dm(10) ** 15: return "%.6g" % float(x)
    return "%.4e" % float(x)

K0 = Dm(math.floor(width_bound(1 / E - Dm(1) / 3)))
C_BFT = (5 - Dm(5).sqrt()) / 10
K12 = width_bound(1 / E - C_BFT).to_integral_value()
sixth = Dm(1) / 6; epsT = Dm(1) / 2 - C_BFT

shapes = [
    ("AK25b Thm 2.6 as printed: (2e)^(w^2)",           lambda w, e: w * w * lg(2 * e)),
    ("best ANY bound on Thm 2.6's atom could give at eps=1/6 (F(m,2), sec 2): (2e)^(0.6309 w)  [Thm 1.2 line: extrapolated]",
                                                        lambda w, e: Dm('0.6309') * w * lg(2 * e)),
    ("hypothetical linear exponent: (2e)^w",            lambda w, e: w * lg(2 * e)),
    ("hypothetical w log w exponent: (2e/w)^w",         lambda w, e: w * lg(2 * e / w)),
    ("hypothetical poly, cubic: (2e/w)^3",              lambda w, e: 3 * lg(2 * e / w)),
    ("hypothetical poly, best possible shape: 2e/w  (ceiling, sec 2.3)", lambda w, e: lg(2 * e / w)),
]

print("== control: reproduce mg-b852")
c1 = L_from_q0(3 * 3 * lg(2 * sixth)); c2 = L_from_q0(K0 * K0 * lg(2 * sixth))
print("   log10 L(4,1/6) = %s (mg-b852: 119.1) -> %s" % (fmt(c1), "MATCH" if abs(c1 - Dm('119.1')) < Dm('0.1') else "MISMATCH"))
print("   log10 L*       = %s (mg-b852: 1.050e29) -> %s" % (fmt(c2), "MATCH" if abs(c2 / Dm('1.050e29') - 1) < Dm('0.001') else "MISMATCH"))
wrong = L_from_q0(K0 * lg(2 * sixth))
print("   negative control: exponent w instead of w^2 gives %s -> %s" % (fmt(wrong), "FIRES (differs)" if abs(wrong / c2 - 1) > Dm('0.5') else "DOES NOT FIRE"))

print("\n== table: K0 = %s (counterexample width, mg-c929), K12 = %s (Thm 1.2 case (a))" % (fmt(K0), fmt(K12)))
print("   Thm 1.2 eps via mg-f218 Thm 1.3'': eps = min(6.8e-6, 0.0236/(L12+1)); L12 = L(width K12, 1/2 - C_BFT)")
for name, f in shapes:
    lq4 = f(Dm(3), sixth); l4 = L_from_q0(lq4)
    lqs = f(K0, sixth); ls = L_from_q0(lqs)
    lq12 = f(K12, epsT); l12 = L_from_q0(lq12)
    le = min(lg(Dm('6.8e-6')), lg(Dm('0.0236')) - l12)
    print("  * %s" % name)
    print("      width<=3 : log10(1/q0) = %-10s log10 L(4,1/6) = %s" % (fmt(-lq4), fmt(l4)))
    print("      width<=K0: log10(1/q0) = %-10s log10 L*       = %s" % (fmt(-lqs), fmt(ls)))
    print("      Thm 1.2  : log10(1/q0) = %-10s log10 L12      = %-10s log10 eps(Thm 1.2) = %s" % (fmt(-lq12), fmt(l12), fmt(le)))
