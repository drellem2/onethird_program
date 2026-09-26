"""mg-5371 -- the family F(m,k): m disjoint chains C_1..C_m of length k, plus an isolated x.
a_i = j-th element of C_i, b_i = (j+1)-th, D = union of the first j of each chain, U = rest.

Claims checked here (proofs in docs/KSBFT-L-heavy-atom.md sec 2):
  (F1) P(A<x<B) = C(k,j)^m / ( C(mk, mj) (mk+1) )          [Thm 2.6's atom]
  (F2) f(x) is uniform on [mk+1], so q(x) = 1/(mk+1)        [the atom L* actually needs]
  (F3) P(a_i<x<b_i) = 1/(k+1); P(a_i<x<b_l), i != l, >= 1/(k+1)  -> (4) holds with eps4 = 1/(k+1)
  (F4) P(c_{i,l} < x) = 1 - l/(k+1)  -> delta_x = 1/2 - 1/(2(k+1)) for k even, j = k/2
Brute-force DP (lib.Poset) on small (m,k) is the positive control; a deliberately wrong (F1)
(the (mk+1) factor dropped) is the negative control and must mismatch."""
from fractions import Fraction
from math import comb, log
from lib import *

def build(m, k):
    n = m * k + 1
    x = m * k
    rel = set()
    for i in range(m):
        for l in range(k - 1):
            rel.add((i * k + l, i * k + l + 1))
    return Poset(n, closure(n, rel)), x

def F1(m, k, j): return Fraction(comb(k, j) ** m, comb(m * k, m * j) * (m * k + 1))
def F1_wrong(m, k, j): return Fraction(comb(k, j) ** m, comb(m * k, m * j))

def pair_gap_exact(k, j):
    """P(c_{1,j} < x < c_{2,j+1}) in F(2,k); by uniform-shuffle restriction this equals the
    value in every F(m,k), m >= 2 (proof: sec 2.1).  Elements numbered 1-based in chains."""
    P, x = build(2, k)
    tot = P.total()
    a = 0 * k + (j - 1); b = 1 * k + j
    c = sum(w for S, w in P.placements(x) if (S >> a) & 1 and not (S >> b) & 1)
    return Fraction(c, tot)

print("== brute-force controls (exact DP)")
ok = True; neg_fires = False
for (m, k, j) in [(1, 2, 1), (2, 2, 1), (3, 2, 1), (4, 2, 1), (5, 2, 1), (2, 4, 2), (3, 4, 2), (2, 6, 3), (3, 3, 1)]:
    P, x = build(m, k)
    tot = P.total()
    Dm_ = sum(1 << (i * k + l) for i in range(m) for l in range(j))
    pl = P.placements(x)
    atom = Fraction(sum(w for S, w in pl if S == Dm_), tot)
    fx = [0] * (m * k + 1)
    for S, w in pl: fx[popcount(S)] += w
    unif = all(Fraction(v, tot) == Fraction(1, m * k + 1) for v in fx)
    # (F3) same-chain gap and (F4) heights
    same = Fraction(sum(w for S, w in pl if (S >> (j - 1)) & 1 and not (S >> j) & 1), tot)
    f4 = all(Fraction(sum(w for S, w in pl if (S >> (l - 1)) & 1), tot) == 1 - Fraction(l, k + 1)
             for l in range(1, k + 1))
    good = atom == F1(m, k, j) and unif and same == Fraction(1, k + 1) and f4
    ok &= good
    if atom != F1_wrong(m, k, j): neg_fires = True
    print(f"  m={m} k={k} j={j}: atom={atom} F1={F1(m,k,j)} uniform f(x)={unif} "
          f"same-chain gap={same} F4={f4} -> {'MATCH' if good else 'MISMATCH'}")
print("  positive control (F1-F4 vs DP):", "PASS" if ok else "FAIL")
print("  negative control (F1 without (mk+1)):", "FIRES" if neg_fires else "DOES NOT FIRE")

print("\n== (F3) cross-chain gap P(a_i<x<b_l), i != l, vs 1/(k+1)")
for (k, j) in [(2, 1), (4, 2), (6, 3), (8, 4)]:
    g = pair_gap_exact(k, j)
    print(f"  k={k} j={j}: cross = {g} = {float(g):.5f}  >= 1/(k+1) = {1/(k+1):.5f} : {g >= Fraction(1, k+1)}")

print("\n== exponents: log(1/atom) vs Thm 2.6's w^2 log(1/eps4), w = |A| = |B| = m, width m+1")
print("  k  j   eps4      m    atom          q(x)=1/(mk+1)   log(1/atom)/(m log(1/eps4))   AK25b bound eps4^(m^2)")
for (k, j) in [(2, 1), (4, 2), (8, 4), (16, 8)]:
    e4 = Fraction(1, k + 1)
    for m in [5, 10, 20, 50, 100, 1000]:
        a = F1(m, k, j)
        la = -log(a.numerator) + log(a.denominator)
        ratio = la / (m * log(1 / e4))
        print(f"  {k:<2} {j:<2} {float(e4):.4f}  {m:>5}  {float(a):.3e}  {1/(m*k+1):.3e}      {ratio:.4f}"
              f"                        1e{-m*m*log(1/e4)/log(10):.1f}")
print("\n  asymptotic: log(1/atom)/m -> log(2^(k H(j/k)) / C(k,j)) ; per unit of log(1/eps4):")
for (k, j) in [(2, 1), (4, 2), (8, 4), (16, 8), (64, 32), (1024, 512)]:
    from math import log2
    H = -(j/k)*log2(j/k) - (1-j/k)*log2(1-j/k)
    rate = (k * H) * log(2) - log(comb(k, j))
    print(f"  k={k:<5} rate={rate:.4f}  rate/log(k+1)={rate/log(k+1):.4f}")
