"""Self-tests for libabe8, including NEGATIVE CONTROLS.

A test suite that only ever passes is unfalsifiable.  Each NC below asserts that
a DELIBERATELY WRONG variant of a routine this instrument depends on FAILS, so
that the passing tests are evidence rather than decoration.
"""

import random
import sys
from fractions import Fraction
from itertools import permutations

import libabe8 as L


FAIL = []


def check(name, cond, detail=""):
    print("%-58s %s%s" % (name, "ok" if cond else "FAIL", ("  " + detail) if detail else ""))
    if not cond:
        FAIL.append(name)


# --------------------------------------------------------------------------
print("== 1. enumeration ==")
# --------------------------------------------------------------------------
ps = {n: None for n in range(1, 8)}
cur = L.all_posets_bruteforce(1)
ps[1] = cur
for n in range(2, 8):
    cur = L.all_posets_by_extension(n, cur)
    ps[n] = cur
check("A000112 to n=7 by extension",
      [len(ps[n]) for n in range(1, 8)] == [1, 2, 5, 16, 63, 318, 2045],
      str([len(ps[n]) for n in range(1, 8)]))

bf = {n: L.all_posets_bruteforce(n) for n in range(1, 6)}
check("brute force agrees with extension, n<=5",
      all(len(bf[n]) == len(ps[n]) for n in range(1, 6)))
check("brute force gives the same ISO CLASSES, n<=5",
      all({p.canonical_key() for p in bf[n]} == {p.canonical_key() for p in ps[n]}
          for n in range(1, 6)))


# --------------------------------------------------------------------------
print("\n== 2. canonical key ==")
# --------------------------------------------------------------------------
def canon_bruteforce(P):
    best = None
    for g in permutations(range(P.n)):
        rel = tuple(sorted((g[a], g[b]) for (a, b) in P.less))
        if best is None or rel < best:
            best = rel
    return (P.n, best)


# The refined-invariant key minimises over a SUBSET of S_n, so it is NOT the
# global lex minimum -- and it is not, on most posets.  What must hold is that it
# is a COMPLETE isomorphism invariant.  Both facts are checked, and the second is
# what the enumeration actually rests on.
bad_const = 0
tot_rel = 0
for n in range(2, 6):
    for P in ps[n]:
        k = P.canonical_key()
        for g in permutations(range(n)):
            tot_rel += 1
            if L.Poset(n, [(g[a], g[b]) for (a, b) in P.less]).canonical_key() != k:
                bad_const += 1
check("key is CONSTANT on isomorphism classes (%d relabellings)" % tot_rel, bad_const == 0)
sep = all(len({P.canonical_key() for P in ps[n]}) == len({canon_bruteforce(P) for P in ps[n]})
          for n in range(2, 7))
check("key SEPARATES non-isomorphic posets, n<=6", sep)
diff5 = sum(1 for P in ps[5] if P.canonical_key() != canon_bruteforce(P))
check("key deliberately DIFFERS from the global lex min (recorded, not a defect)",
      diff5 > 0, "%d of %d at n=5" % (diff5, len(ps[5])))


# --------------------------------------------------------------------------
print("\n== 3. delta, from the definition ==")
# --------------------------------------------------------------------------
def delta_bruteforce(P):
    """delta by literally listing every linear extension."""
    n = P.n
    exts = []

    def rec(placed, word):
        if len(word) == n:
            exts.append(tuple(word))
            return
        for x in range(n):
            if (placed >> x) & 1:
                continue
            if P.dn[x] & ~placed:
                continue
            rec(placed | (1 << x), word + [x])

    rec(0, [])
    pairs = P.incomparable_pairs()
    if not pairs:
        return None
    tot = len(exts)
    best = Fraction(0)
    for (x, y) in pairs:
        c = sum(1 for w in exts if w.index(x) < w.index(y))
        p = Fraction(c, tot)
        best = max(best, min(p, 1 - p))
    return best


ok = all(L.delta(P) == delta_bruteforce(P) for n in range(2, 7) for P in ps[n])
check("DP delta == list-every-extension delta, n<=6", ok)

# The anchor mg-5998 names by hand: E = a 2-chain plus an isolated point, whose
# three linear extensions cab / acb / abc give delta(E) = 1/3 EXACTLY.
E = L.Poset(3, {(0, 1)})
check("delta(E) = 1/3 exactly (mg-5998's hand check, reproduced)",
      L.delta(E) == Fraction(1, 3), str(L.delta(E)))
# V = two minimal elements under one top.  NOT 1/3: its only incomparable pair is
# the two minimal elements, which are interchangeable, so delta(V) = 1/2.  This
# assertion was written as 1/3 and the CODE caught it -- see OUTCOMES.md.
V = L.Poset(3, {(0, 2), (1, 2)})
check("delta(V) = 1/2 (V is an ordinal sum: antichain_2 (+) point)",
      L.delta(V) == Fraction(1, 2), str(L.delta(V)))
# N = 0<2, 1<2, 1<3.  Five linear extensions; p(0,1) = 2/5, and that is the max.
N4 = L.Poset(4, {(0, 2), (1, 2), (1, 3)})
check("delta(N) = 2/5 (five linear extensions, p(0,1)=2/5)",
      L.delta(N4) == Fraction(2, 5), str(L.delta(N4)))
check("antichain on 2 is delta = 1/2", L.delta(L.Poset(2, set())) == Fraction(1, 2))
check("chain has delta None", L.delta(L.Poset(3, {(0, 1), (1, 2)})) is None)

# delta_lazy: the Theta(#ideals*n) form.  It EARLY-EXITS once a balanced pair is
# found, so it equals delta only below the threshold; what must agree everywhere
# is the frozen VERDICT, which is what a search consumes.
bad_verdict = bad_value = 0
for n in range(2, 8):
    for P in ps[n]:
        d, dl = L.delta(P), L.delta_lazy(P)
        if (d is None) != (dl is None):
            bad_verdict += 1
            continue
        if d is None:
            continue
        if (d < Fraction(1, 3)) != (dl < Fraction(1, 3)):
            bad_verdict += 1
        if d < Fraction(1, 3) and d != dl:
            bad_value += 1
check("delta_lazy gives the SAME frozen verdict as delta, n<=7", bad_verdict == 0)
check("delta_lazy equals delta whenever the poset is frozen", bad_value == 0)

frozen_counts = {n: sum(1 for P in ps[n] if L.is_frozen(P)) for n in range(2, 8)}
check("frozen class EMPTY at every n <= 7",
      all(v == 0 for v in frozen_counts.values()), str(frozen_counts))


# --------------------------------------------------------------------------
print("\n== 4. the four constraints ==")
# --------------------------------------------------------------------------
check("|Aut| of the 3-antichain is 6", L.automorphism_count(L.Poset(3, set())) == 6)
check("|Aut| of the 3-chain is 1", L.automorphism_count(L.Poset(3, {(0, 1), (1, 2), (0, 2)})) == 1)
check("|Aut(V)| = 2", L.automorphism_count(V) == 2)
check("|Aut(N)| = 1 (N is rigid)", L.automorphism_count(N4) == 1)
check("width(antichain_5) = 5", L.width(L.Poset(5, set())) == 5)
check("width(chain_5) = 1", L.width(L.Poset(5, {(i, j) for i in range(5) for j in range(i + 1, 5)})) == 1)
check("width(V) = 2", L.width(V) == 2)
check("thinness(antichain_8) = 7", L.thinness(L.Poset(8, set())) == 7)
check("thinness(chain_8) = 0", L.thinness(L.Poset(8, {(i, j) for i in range(8) for j in range(i + 1, 8)})) == 0)
check("E is primitive (incomparability graph is a path)", L.is_primitive(E))
check("V is NOT primitive (it is antichain_2 (+) point)", not L.is_primitive(V))
check("chain_3 is NOT primitive", not L.is_primitive(L.Poset(3, {(0, 1), (1, 2), (0, 2)})))
check("1 (+) antichain_2 is NOT primitive",
      not L.is_primitive(L.Poset(3, {(0, 1), (0, 2)})))
check("N is primitive", L.is_primitive(N4))

# the hand measurement H5 of PREDICTIONS: at n=8, `not 6-thin` forces P = 1 (+) Q
ps8 = L.all_posets_by_extension(8, ps[7])
n8_thin = sum(1 for P in ps8 if L.thinness(P) >= 7)
check("H5 reproduced: 2045 of 16999 posets at n=8 are not-6-thin",
      (n8_thin, len(ps8)) == (2045, 16999), "%d / %d" % (n8_thin, len(ps8)))


# --------------------------------------------------------------------------
print("\n== 5. pruning arithmetic (P14's formula, and only it) ==")
# --------------------------------------------------------------------------
check("prune_bits(total,total) == 0", L.prune_bits(100, 100) == 0.0)
check("prune_bits(half) == 1 bit", abs(L.prune_bits(50, 100) - 1.0) < 1e-12)
check("prune_bits(0) is +inf", L.prune_bits(0, 100) == float("inf"))
check("a VANISHING EXCLUDED SET prunes ~0 bits, not many (P14)",
      L.prune_bits(999999, 1000000) < 1e-5,
      "%.3e bits" % L.prune_bits(999999, 1000000))


# --------------------------------------------------------------------------
print("\n== 6. growth model ==")
# --------------------------------------------------------------------------
check("log2_N exact at n=16", abs(L.log2_N(16) - 51.9927) < 1e-3, "%.4f" % L.log2_N(16))
check("LOW model <= KR model above n=16",
      all(L.log2_N(n, "LOW") < L.log2_N(n, "KR") for n in range(17, 40)))
check("g is increasing on the exact range", all(L.g_exact(n) > L.g_exact(n - 1) for n in range(3, 17)))


# --------------------------------------------------------------------------
print("\n== 7. KR ideal count ==")
# --------------------------------------------------------------------------
rng = random.Random(20260807)
ok = True
detail = ""
for n in range(4, 15):
    l1, l2, l3 = L.kr_layer_sizes(n)
    for _ in range(4):
        P = L.kr_sample(n, rng)
        fast = L.kr_ideal_count(P, l1, l2, l3)
        slow = len(L.order_ideal_masks(P))
        if fast != slow:
            ok = False
            detail = "n=%d fast=%d slow=%d" % (n, fast, slow)
            break
    if not ok:
        break
check("kr_ideal_count == order_ideal_masks, n=4..14", ok, detail)

ok = all(sorted(L.order_ideal_masks_lazy(P)) == sorted(L.order_ideal_masks(P))
         for n in range(2, 7) for P in ps[n])
check("order_ideal_masks_lazy == the 2^n sweep, n<=6", ok)


# --------------------------------------------------------------------------
print("\n== 8. NEGATIVE CONTROLS (each must FAIL for the suite to mean anything) ==")
# --------------------------------------------------------------------------

# NC1 -- the P14 error itself: prune bits computed off the EXCLUDED fraction.
def prune_bits_wrong(surviving, total):
    excluded = total - surviving
    return -__import__("math").log2(excluded / total) if excluded else float("inf")


nc1 = prune_bits_wrong(999999, 1000000)
check("NC1: the P14-inverted formula disagrees (and wildly)",
      nc1 > 15.0 and L.prune_bits(999999, 1000000) < 1e-5,
      "wrong=%.2f bits, right=%.3e bits" % (nc1, L.prune_bits(999999, 1000000)))

# NC2 -- an enumerator that adjoins the new element as maximal but only over
# PRINCIPAL ideals must MISS posets.  If it does not, the completeness argument
# for `all_posets_by_extension` is not doing any work.
def by_extension_principal_only(n, smaller):
    seen = {}
    for Q in smaller:
        ideals = [0] + [Q.dn[i] | (1 << i) for i in range(Q.n)]
        for ideal in ideals:
            rel = set(Q.less)
            for i in range(Q.n):
                if (ideal >> i) & 1:
                    rel.add((i, n - 1))
            seen.setdefault(L.Poset(n, rel).canonical_key(), None)
    return seen


nc2 = len(by_extension_principal_only(6, ps[5]))
check("NC2: principal-ideals-only enumeration MISSES posets at n=6",
      nc2 < 318, "%d < 318" % nc2)

# NC3 -- delta with min(p,1-p) replaced by p (dropping the symmetrisation) must
# disagree somewhere, else the min is decorative.
def delta_nosym(P):
    pairs = P.incomparable_pairs()
    if not pairs:
        return None
    e = L.restriction_counts(P)
    tot = e[(1 << P.n) - 1]
    bef = L.pair_before_counts(P, e)
    return max(Fraction(bef[(x, y)], tot) for (x, y) in pairs)


nc3 = sum(1 for P in ps[5] if L.delta(P) is not None and delta_nosym(P) != L.delta(P))
check("NC3: dropping min(p,1-p) changes delta on many n=5 posets", nc3 > 10, "%d posets" % nc3)

# NC4 -- rigidity is NOT hereditary: exhibit a rigid poset with a non-rigid
# one-element-deleted subposet.  If none exists the hereditary claim in the
# report is vacuous rather than true.
def delete(P, x):
    idx = [i for i in range(P.n) if i != x]
    rank = {v: k for k, v in enumerate(idx)}
    return L.Poset(P.n - 1, {(rank[a], rank[b]) for (a, b) in P.less if a != x and b != x})


nc4 = 0
for P in ps[5]:
    if L.is_rigid(P) and any(not L.is_rigid(delete(P, x)) for x in range(P.n)):
        nc4 += 1
check("NC4: rigidity is NOT hereditary (witnesses exist at n=5)", nc4 > 0, "%d witnesses" % nc4)

# NC5 -- a KR ideal counter that forgets the L1<L3 forcing must overcount.
def kr_ideal_count_broken(P, l1, l2, l3):
    total = 0
    for bmask in range(1 << l2):
        need = 0
        for j in range(l2):
            if (bmask >> j) & 1:
                need |= P.dn[l1 + j] & ((1 << l1) - 1)
        total += (1 << (l1 - bin(need).count("1"))) * (1 << l3)
    return total


P = L.kr_sample(10, random.Random(1))
l1, l2, l3 = L.kr_layer_sizes(10)
check("NC5: forgetting the L1<L3 forcing OVERCOUNTS ideals",
      kr_ideal_count_broken(P, l1, l2, l3) > L.kr_ideal_count(P, l1, l2, l3),
      "%d > %d" % (kr_ideal_count_broken(P, l1, l2, l3), L.kr_ideal_count(P, l1, l2, l3)))


print("\n%d checks failed" % len(FAIL))
if FAIL:
    for f in FAIL:
        print("  FAILED:", f)
    sys.exit(1)
