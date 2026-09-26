"""mg-c929 s3 -- the explicit constants of Prop. B (docs/KSBFT-D-sec6-eps-spec.md), evaluated.

Chain (all logs natural):
  eps0      = 1/e - 1/3                       frozen/boundary deficit below Gruenbaum's 1/e
  G1        = 10 e (1+sqrt3) / eps^3          gap bound when (6.8) fails
  A         = 18432 sqrt3 / eps^3             section 6.4: gap <= A (log gap)^2
  G2        = 4 A (log A)^2                   paper's 73728 sqrt3/eps^3 * log(18432 sqrt3/eps^3)^2
  G         = max(G1, G2)
  C_inv     = 2 sqrt3 e G / eps^3             E[inv_h] <= C_inv * n       (Prop. B)
  eps_spec <= 6 C_inv n / (n^2 - 1)
  N(target) = least n with 6 C_inv n/(n^2-1) <= target
Also checks the one analytic step the paper leaves to the reader: that gap <= A (log gap)^2
forces gap <= 4A (log A)^2.  Since g/(log g)^2 is increasing for g > e^2, it suffices that
g0 = 4A(log A)^2 satisfies g0 > A (log g0)^2, i.e. every g >= g0 violates the hypothesis.
"""
import math

def report(name, eps):
    s3 = math.sqrt(3); e = math.e
    G1 = 10 * e * (1 + s3) / eps ** 3
    A = 18432 * s3 / eps ** 3
    G2 = 4 * A * math.log(A) ** 2
    g0ok = G2 > A * math.log(G2) ** 2
    G = max(G1, G2)
    Cinv = 2 * s3 * e * G / eps ** 3
    print("== %s: eps = %.6g" % (name, eps))
    print("   G1 = %.4g   A = %.4g   G2 = 4A(log A)^2 = %.4g   step 'g<=A log^2 g => g<=G2' valid: %s"
          % (G1, A, G2, g0ok))
    print("   gap bound G = %.4g ;  width bound 2 sqrt3 G/eps = %.4g" % (G, 2 * s3 * G / eps))
    print("   C_inv = 2 sqrt3 e G/eps^3 = %.4g   (E[inv_h] <= C_inv * n)" % Cinv)
    for tgt, lab in [(1.0, "1 (pair-bias value)"), (1 / 6, "1/6"), (0.02, "eps_dem ~ 2e-2")]:
        # 6 C n/(n^2-1) <= tgt  <=>  n^2 - (6C/tgt) n - 1 >= 0
        b = 6 * Cinv / tgt
        N = math.ceil((b + math.sqrt(b * b + 4)) / 2)
        print("   eps_spec <= %-22s for n >= %.4g" % (lab, N))

report("frozen / boundary class (delta <= 1/3)", 1 / math.e - 1 / 3)
report("hypothetical 1/2-input (NOT available; deficit 1/2 - 1/3 = 1/6)", 1 / 6)
