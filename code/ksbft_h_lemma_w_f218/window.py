"""window.py (mg-f218) -- the numbers in docs/KSBFT-H-lemma-W.md sec. 3.

theta_0   = 0.2764 - C_BFT             (cap from Lemma 3.2(i): Case C / Cor 2.2)
theta_W(D)= C_BFT / ((5+3 sqrt5)(D+1) + 1)   (Lemma W window, Thm 1.3'')
wit_C(D)  = 1/(24.5 (D+1))             (Prop B + Prop C of mg-d707)
wit_441(D)= 1/(441 (D+1)^2)            (Prop B + printed Lemma 4.2)
eta'_D    = (D+1)^(-3(D+1))/12         (mg-d707 Thm 1.3')
eta_D     = (D+1)^(-4(D+1))/4096       (paper Thm 1.3)
Every inequality the doc asserts about these is ASSERTED here, so a wrong
claim stops the script (the asserts are the check; exit status 1 = failure)."""
from decimal import Decimal as Dm, getcontext
import math
getcontext().prec = 50
s5 = Dm(5).sqrt()
C = (5 - s5) / 10
K = 5 + 3 * s5
th0 = Dm("0.2764") - C
def thW(D): return C / (K * (D + 1) + 1)
def witC(D): return 1 / (Dm("24.5") * (D + 1))
def wit441(D): return 1 / (Dm(441) * (D + 1) ** 2)
print(f"C_BFT = {C:.12f}   5+3sqrt5 = {K:.10f}   theta_0 = 0.2764 - C_BFT = {th0:.6e}")
# D_0: largest D with theta_W(D) > theta_0
D0 = max(D for D in range(2, 10000) if thW(D) > th0)
print(f"D_0 = largest D with theta_W(D) > theta_0 : {D0}  (theta_W(D_0)={thW(D0):.6e}, theta_W(D_0+1)={thW(D0+1):.6e})")
assert thW(D0) > th0 >= thW(D0 + 1)
# Lemma W window is always below the Prop-C witness: theta_W(D) < 1/(24.5(D+1))
for D in range(2, 200000, 7): assert thW(D) < witC(D)
print("checked: theta_W(D) < 1/(24.5(D+1)) for D = 2..200000 step 7 (and it is C*24.5 < 5+3sqrt5 algebraically)")
assert C * Dm("24.5") < K
# printed 441: witness binds from D441 on
D441 = min(D for D in range(2, 10000) if wit441(D) <= th0)
print(f"with printed Lemma 4.2 (M^2/441) the witness 1/(441(D+1)^2) <= theta_0 from D = {D441}; Prop C is load-bearing for D >= {D441}")
assert all(wit441(D) < thW(D) for D in range(2, 100000, 11))
print("checked: 1/(441(D+1)^2) < theta_W(D) for all sampled D -> with 441 the witness, not Lemma W, binds")
# Lemma 2.4 / Prop C / Lemma 4.2 side conditions inside the new window
assert th0 < Dm("1e-5")
print(f"theta_0 < 1e-5 (Lemma 4.2's eps-condition, per audit mg-3a14 sec 2.7): {th0 < Dm('1e-5')}")
print()
print(" D |  new: min(theta_0, theta_W(D))  | mg-d707 eta'_D  | paper eta_D")
for D in (2, 6, 7, 10, 18, 100, 1000, D0, D0 + 1, 10**4, 10**5, 10**6):
    new = min(th0, thW(D))
    l1 = -3 * (D + 1) * math.log10(D + 1) - math.log10(12)
    l2 = -4 * (D + 1) * math.log10(D + 1) - math.log10(4096)
    print(f"{D:>7} | {float(new):.6e}  ({'theta_0' if th0 <= thW(D) else 'theta_W'} binds) | 10^{l1:.1f} | 10^{l2:.1f}")
print()
# p >= C - theta in the window, used in the proof: numeric sanity at theta_0
print(f"p >= 2*C_BFT - (C_BFT + theta_0) = {C - th0:.9f}")
print()
# sec. 4 (CONDITIONAL on the paper's unchecked Appendix A claim 67/242 for Lemma 2.3)
th67 = Dm(67) / 242 - C
D67 = max(D for D in range(2, 10000) if thW(D) > th67)
print(f"conditional (Lemma 2.3 at 67/242, unchecked): theta_0' = {th67:.4e}; constant regime up to D = {D67}")
assert Dm("4.66e-4") < th67 < Dm("4.67e-4") and D67 == 49
# sec. 1.2: with a D-free Lemma W, the Prop-C witness 1/(24.5(D+1)) binds from D = 6004 on
Dw = min(D for D in range(2, 100000) if witC(D) <= th0)
print(f"witness 1/(24.5(D+1)) <= theta_0 from D = {Dw}")
assert Dw == 6004
# sec. 1.2 table, hypothetical row c = D^(-k): theta_0 binds while D^(-k)/(5+3sqrt5) >= theta_0,
# i.e. D^k <= 1/((5+3sqrt5) theta_0) = 1.2564e4 (errata mg-9694, audit mg-e60e item 6a: was 8.6e3)
Dk = 1 / (K * th0)
print(f"D^(-k) row: theta_0 binds for D^k <= 1/((5+3sqrt5) theta_0) = {Dk:.4e}")
assert Dm("1.256e4") < Dk < Dm("1.257e4")
for k in (1, 2, 3):
    Dmax = max(D for D in range(2, 20000) if Dm(D) ** -k / K >= th0)
    print(f"  k={k}: largest D with D^(-k)/(5+3sqrt5) >= theta_0 is {Dmax}  (~(1.26e4)^(1/k) = {float(Dk) ** (1 / k):.1f})")
    assert Dm(Dmax) ** k <= Dk < Dm(Dmax + 1) ** k
# if c multiplies p (as Lemma W's does, p >= C_BFT - theta_0), the threshold is ~3.47e3
print(f"  (c*p reading: 1/((5+3sqrt5) theta_0) * (C_BFT - theta_0) = {Dk * (C - th0):.4e})")
assert Dm("3.47e3") < Dk * (C - th0) < Dm("3.48e3")
