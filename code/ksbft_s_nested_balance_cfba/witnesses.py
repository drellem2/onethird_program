"""witnesses.py (mg-cfba): every exact number the doc cites for its witnesses, recomputed with the independent
Python ideal DP of mg-ce69 (lib.analyse, Fractions) and asserted.  Exit 1 on any failure.
T8  = 8 0 0 2 6 3 e 17 5f       (in the n<=9 census; prime, range 4): every nested balanced pair is ON the boundary
T13 = 13 0 1 0 3 5 17 3f b bf 1ff 7f 7ff 47f   (search; prime, range 6): same
T14 = 14 0 0 153 12 2 1b 3 3b 53 15f 11ff 33ff bb 3ff  (search; range 5): same
N12 = 12 0 4 0 6 f 885 6 805 aff 5f 8af 5   (search; range 7; NO firing full-chain good pair): deltaN = 1/3 + 1/2346
CONTROL: with the OPEN window (1/3,2/3), 'nested balance' must FAIL on T8, T13, T14 (so the tie is load-bearing)."""
import sys
from fractions import Fraction as F
from fam import parse, is_prime, rng, connected, upmasks, pair_laws, firing_full_pairs
sys.path.insert(0, "../ksbft_q2_both_ends_ce69")
from lib import analyse

T3 = F(1, 3)
ok = True

def check(c, msg):
    global ok
    print(("OK   " if c else "FAIL ") + msg)
    ok &= bool(c)

def laws(dn):
    n = len(dn); e, B, pos = analyse(dn); up = upmasks(dn); out = []
    for a in range(n):
        for b in range(a + 1, n):
            if dn[a] >> b & 1 or dn[b] >> a & 1: continue
            p = F(B[a][b], e)
            nested = (dn[a] & ~dn[b] == 0) or (dn[b] & ~dn[a] == 0) or (up[a] & ~up[b] == 0) or (up[b] & ~up[a] == 0)
            out.append((a, b, p, nested))
    return e, pos, out

def summary(tag, s, e_exp, deltaN_exp, delta_exp, prime_exp, rng_exp):
    dn = parse(s); e, pos, L = laws(dn)
    dN = max(min(p, 1 - p) for a, b, p, nst in L if nst)
    d = max(min(p, 1 - p) for a, b, p, nst in L)
    check(e == e_exp, f"{tag}: e = {e}")
    check(dN == deltaN_exp, f"{tag}: deltaN = {dN} (best nested pair)")
    check(d == delta_exp, f"{tag}: delta = {d} (best pair overall)")
    check(connected(dn), f"{tag}: indecomposable (incomparability graph connected)")
    check(is_prime(dn) == prime_exp, f"{tag}: prime = {prime_exp}")
    check(rng(dn) == rng_exp, f"{tag}: range = {rng_exp}")
    inner_nested = [(a, b, p) for a, b, p, nst in L if nst and T3 < p < 2 * T3]
    inner_any = [(a, b, p) for a, b, p, nst in L if T3 < p < 2 * T3]
    return dn, L, inner_nested, inner_any

for tag, s, e, dN, d, pr, r in [
        ("T8", "8 0 0 2 6 3 e 17 5f", 42, T3, F(17, 42), True, 4),
        ("T13", "13 0 1 0 3 5 17 3f b bf 1ff 7f 7ff 47f", 588, T3, F(17, 42), True, 6),
        ("T14", "14 0 0 153 12 2 1b 3 3b 53 15f 11ff 33ff bb 3ff", 1395, T3, F(656, 1395), False, 5)]:
    dn, L, inn, ina = summary(tag, s, e, dN, d, pr, r)
    check(not inn and ina, f"{tag}: CONTROL open-window nested balance FAILS (no nested pair strictly inside), "
          f"while {len(ina)} non-nested pair(s) are strictly inside: {[(a, b, str(p)) for a, b, p in ina]}")

# mechanism at T8: (0;1<2<3<5) is a full-chain good pair with Doubling t1 = t0 = 1/3
dn = parse("8 0 0 2 6 3 e 17 5f"); e, pos, L = laws(dn); up = upmasks(dn)
P = {(a, b): p for a, b, p, _ in L}
check(P[(0, 1)] == T3 and P[(0, 2)] == 2 * T3, "T8 mechanism: P[0<1] = 1/3 (t0), P[0<2] = 2/3 = 2*t0 (Doubling Lemma 1.5)")
check(dn[0] == dn[1] == 0 and up[0] & ~up[1] == 0, "T8 mechanism: down(0)=down(1)=empty, up(0) subset up(1) (Doubling hypotheses)")
priv = up[1] & ~up[0]
check(priv == (1 << 2 | 1 << 3 | 1 << 5) and dn[3] >> 2 & 1 and dn[5] >> 3 & 1, "T8 mechanism: up(1)-up(0) = {2<3<5}, a chain (Zaguia good pair)")

dn, L, inn, ina = summary("N12", "12 0 4 0 6 f 885 6 805 aff 5f 8af 5", 1564, F(261, 782), F(1, 2), False, 7)
P = {(a, b): p for a, b, p, _ in L}
check(F(261, 782) - T3 == F(1, 2346), "N12: deltaN - 1/3 = 1/2346")
check(P[(0, 2)] == F(521, 1564) and P[(0, 1)] == 2 * P[(0, 2)], "N12 mechanism: P[0<1] = 2 P[0<2] = 521/782 (Doubling, t0 = 521/1564 just below 1/3)")
check(firing_full_pairs(dn, pair_laws([dn])[0]) == 0, "N12: no firing full-chain good pair (primal or dual)")
t8 = parse("8 0 0 2 6 3 e 17 5f")
check(firing_full_pairs(t8, pair_laws([t8])[0]) > 0, "T8: HAS a firing full-chain good pair (control for the detector)")
sys.exit(0 if ok else 1)
