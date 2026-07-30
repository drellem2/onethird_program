"""Self-test for kern5800.  Every assertion here is against a fact this audit
did NOT take from mg-af28, mg-6ad0 or mg-41aa: OEIS A000112 (unlabelled
posets), A000041 (partitions), the Fibonacci rank sizes of the
Young-Fibonacci lattice, Birkhoff as an equality on hand-built examples,
M3 and N5 as the two forbidden sublattices, and hand-computed small cases.

If any assertion fires, NOTHING this instrument reports is admissible.
"""
import sys
from kern5800 import (bits, popcount, check_poset, canon, decode, ideals,
                      enumerate_posets, ideal_lattice, join_irreducibles,
                      induced, is_lattice, is_distributive, skew_shapes,
                      skew_cell_poset, straight_shapes, partitions_between,
                      interval_poset, shape_to_mu_lam, yf_words, yf_covers,
                      yf_poset, down_of, yf_down_covers)

N = [0]
def ok(cond, label):
    N[0] += 1
    if not cond:
        print("FAIL %2d  %s" % (N[0], label))
        sys.exit(1)
    print("  ok %2d  %s" % (N[0], label))


# ---- bit utils
ok(bits(0b1011) == [0, 1, 3], "bits")
ok(popcount(0b1011) == 3, "popcount")

# ---- posets: hand cases
chain3 = (0b110, 0b100, 0)
check_poset(3, chain3)
anti3 = (0, 0, 0)
vee3 = (0b110, 0, 0)          # 0 < 1, 0 < 2
wedge3 = (0b100, 0b100, 0)    # 0 < 2, 1 < 2
c2p1 = (0b010, 0, 0)          # 0 < 1, 2 isolated
ok(len({canon(3, p) for p in [chain3, anti3, vee3, wedge3, c2p1]}) == 5,
   "the five 3-element posets are pairwise non-isomorphic")
ok(canon(3, (0b110, 0b100, 0)) == canon(3, (0, 0b001, 0b011)),
   "canon is label-independent on the 3-chain")

# ---- A000112: unlabelled posets 1,2,5,16,63,318,2045
A000112 = [1, 2, 5, 16, 63, 318, 2045]
ps = enumerate_posets(7)
ok([len(ps[n]) for n in range(1, 8)] == A000112,
   "enumerate_posets reproduces A000112 to n=7: %s" % [len(ps[n]) for n in range(1, 8)])

# ---- ideals / J(P)
ok(len(ideals(3, anti3)) == 8, "J(antichain_3) has 8 elements")
ok(len(ideals(3, chain3)) == 4, "J(chain_3) has 4 elements")
m, jup, _ = ideal_lattice(3, anti3)
ok(is_lattice(m, jup) and is_distributive(m, jup), "J(antichain_3) is a distributive lattice")

# ---- Birkhoff as an equality on every poset to n=5
bad = 0
for n in range(1, 6):
    for code in ps[n]:
        up = decode(n, code)
        m, jup, _ = ideal_lattice(n, up)
        k, kup = join_irreducibles(m, jup)
        if (k, canon(k, kup)) != (n, canon(n, up)):
            bad += 1
ok(bad == 0, "Birkhoff: Irr(J(P)) = P for all 87 posets to n<=5, 0 bad")


# ---- canon is label-independent on LARGE structures too.  This control was
# added after it FIRED: an earlier version of canon chose its target colour
# class by dict-insertion order, which is label-dependent, and split two
# isomorphic 20-element distributive lattices into two classes.  Rank sizes
# and A000112 both passed while that bug was live, so neither is a control on
# it; random relabelling is.
import random
rng = random.Random(20260730)
worst = 0
for n in range(1, 6):
    for code in ps[n]:
        up0 = decode(n, code)
        m, jup, _ = ideal_lattice(n, up0)
        base = canon(m, jup)
        for _ in range(3):
            perm = list(range(m))
            rng.shuffle(perm)
            relab = [0] * m
            for i in range(m):
                for j in bits(jup[i]):
                    relab[perm[i]] |= 1 << perm[j]
            if canon(m, tuple(relab)) != base:
                worst += 1
ok(worst == 0, "canon is invariant under random relabelling of J(P) for all 87 "
   "posets to n<=5, 3 relabellings each (261 lattices, up to 32 elements)")

# ---- M3 and N5 are lattices and are NOT distributive; C2xC2 is
m3 = (0b1110, 0b1000, 0b1000, 0)                       # bottom, 3 atoms, top
m3 = (0b11110, 0b10000, 0b10000, 0b10000, 0)
ok(is_lattice(5, m3) and not is_distributive(5, m3), "M3 is a non-distributive lattice")
# N5: 0 < a < b < 1, 0 < c < 1
n5 = (0b11110, 0b11000, 0b10000, 0b10000, 0)
ok(is_lattice(5, n5) and not is_distributive(5, n5), "N5 is a non-distributive lattice")
c2c2 = (0b1110, 0b1000, 0b1000, 0)
ok(is_lattice(4, c2c2) and is_distributive(4, c2c2), "C2 x C2 is distributive")

# ---- partitions: A000041
A000041 = [1, 2, 3, 5, 7, 11, 15, 22]
ok([len(straight_shapes(n)) for n in range(1, 9)] == A000041,
   "straight_shapes reproduces A000041 to n=8")

# ---- intervals of Young's lattice, built from partitions only
ok(len(partitions_between((), (2, 1))) == 5, "|[(), (2,1)]| = 5")
ok(len(partitions_between((1,), (2, 1))) == 4,
   "|[(1), (2,1)]| = 4  (the 2-antichain's ideal lattice, hand-checked: "
   "(1),(1,1),(2),(2,1))")
m, up, els = interval_poset((), (2, 1))
ok(is_lattice(m, up) and is_distributive(m, up), "[(), (2,1)] is a distributive lattice")

# ---- skew shapes: cell counts
sh = skew_shapes(3, 3)
ok(all(skew_cell_poset(s)[0] == 3 for s in sh), "every 3-cell skew shape has 3 cells")
# the 2-antichain is a skew cell poset and is NOT a straight one
sh2 = skew_shapes(2, 2)
c2 = {canon(*skew_cell_poset(s)) for s in sh2}
st2 = {canon(*skew_cell_poset(s)) for s in straight_shapes(2)}
ok(canon(2, (0, 0)) in c2, "2-antichain IS a skew cell poset")
ok(canon(2, (0, 0)) not in st2, "2-antichain is NOT a straight cell poset")

# ---- Young-Fibonacci: Fibonacci rank sizes
byr = yf_words(7)
ok([len(byr[r]) for r in range(8)] == [1, 1, 2, 3, 5, 8, 13, 21],
   "Young-Fibonacci rank sizes are Fibonacci to rank 7")
ok(sorted(yf_covers((1,))) == [(1, 1), (2,)], "'1' is covered by '11' and by '2'")
ok(sorted(yf_down_covers((2, 1))) == [(1, 1), (2,)],
   "'21' covers '11' (2 left of the leftmost 1) and '2' (delete the leftmost 1)")
ok(sorted(yf_down_covers((1, 2))) == [(2,)],
   "'12' covers only '2' -- the 2 is to the RIGHT of the leftmost 1")

# ---- DU - UD = I on the Young-Fibonacci graph, as an OPERATOR identity
m, up, els, idx, cov = yf_poset(7)
byrank = {}
for i, w in enumerate(els):
    byrank.setdefault(sum(w), []).append(i)
dcov = [[] for _ in range(m)]
for w in range(m):
    for y in cov[w]:
        dcov[y].append(w)
viol = 0
for r in range(0, 6):
    for x in byrank[r]:
        vec = {}
        for y in cov[x]:                       # U : rank r -> r+1
            for z in dcov[y]:                  # D : rank r+1 -> r
                vec[z] = vec.get(z, 0) + 1
        for w in dcov[x]:                      # D : rank r -> r-1
            for z in cov[w]:                   # U : rank r-1 -> r
                vec[z] = vec.get(z, 0) - 1
        for k, v in vec.items():
            want = 1 if k == x else 0
            if v != want:
                viol += 1
ok(viol == 0, "DU - UD = I as an operator identity on YF below rank 6, 0 violations")

# ---- every interval [0, w] of YF is a lattice
badl = 0
for i, w in enumerate(els):
    if sum(w) > 5:
        continue
    sub = [j for j in range(m) if j == i or ((up[j] >> i) & 1)]
    k, kup = induced(m, up, sub)
    if not is_lattice(k, kup):
        badl += 1
ok(badl == 0, "every YF interval [0,w] with rank(w) <= 5 is a lattice")

# ---- hook length formula / sum (f^lam)^2 = n! via SYT counted as maximal
# chains of the interval [(), lam]  (an independent handle on Young's lattice)
def nchains(mu, lam):
    m, up, els = interval_poset(mu, lam)
    dn = down_of(m, up)
    order = sorted(range(m), key=lambda x: sum(els[x]))
    cnt = [0] * m
    for x in order:
        if dn[x] == 0:
            cnt[x] = 1
        else:
            tot = 0
            for y in bits(dn[x]):
                if not (dn[x] & up[y]):
                    tot += cnt[y]
            cnt[x] = tot
    top = max(range(m), key=lambda x: sum(els[x]))
    return cnt[top]

import math

def hook_f(lam):
    """f^lam by the hook length formula."""
    lam = [x for x in lam if x]
    n = sum(lam)
    conj = [sum(1 for r in lam if r > j) for j in range(lam[0])]
    prod = 1
    for i, r in enumerate(lam):
        for j in range(r):
            prod *= (r - j) + (conj[j] - i) - 1
    return math.factorial(n) // prod

for n in range(1, 7):
    lams = [tuple(b for a, b in s) for s in straight_shapes(n)]
    ok(all(nchains((), lam) == hook_f(lam) for lam in lams),
       "maximal chains of [(), lam] = hook length formula, all lam |- %d" % n)
    ok(sum(hook_f(lam) ** 2 for lam in lams) == math.factorial(n),
       "sum (f^lam)^2 = n! = %d at n=%d" % (math.factorial(n), n))

print("\nSELFTEST 5800: %d assertions, 0 failures" % N[0])
