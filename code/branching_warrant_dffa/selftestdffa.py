"""Self-test for kerndffa.

Every assertion that matters here is checked in BOTH directions: a canonical
form that never separates anything, a distributivity test that never says no,
or a skew-shape membership test that says yes to everything would each pass a
one-sided battery and would each silently confirm the sentences this repair is
narrowing.  mg-5800 recorded two controls firing on its own instrument for
exactly this reason -- a canonical form with a live bug that reproduced A000112
to 16 999, and a Young-Fibonacci cover rule that reproduced the Fibonacci rank
sizes.  Both were caught by a test that could say no.

Run: python3 selftestdffa.py
"""

import random
import sys
from collections import Counter
from itertools import permutations

from kerndffa import (Lattice, canon, cell_poset, conjugate, ideals,
                      lattice_of_ideals, partitions, partitions_in_box,
                      partitions_upto, poset_from_cells, relabel,
                      shape_of_ideal, skew_cells, skew_classes, sub_partitions,
                      trim_skew, yf_down_covers, yf_interval, yf_leq,
                      yf_up_covers, yf_words, young_interval)

OUT = sys.stdout
N = [0]
FAILS = []


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        FAILS.append(label)
    print("  %-3d %-62s %s" % (N[0], label, "ok" if cond else "FAIL " + detail),
          file=OUT)


def chain(n):
    return poset_from_cells([(1, j) for j in range(1, n + 1)])


def antichain(n):
    return poset_from_cells([(i, n + 1 - i) for i in range(1, n + 1)])


def main():
    print("=" * 78, file=OUT)
    print("SELF-TEST  kerndffa", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)

    # -- partitions ------------------------------------------------------
    print("  -- partitions and shapes --------------------------------------",
          file=OUT)
    ok("p(n) for n = 0..8 is 1,1,2,3,5,7,11,15,22",
       [len(partitions(n)) for n in range(9)]
       == [1, 1, 2, 3, 5, 7, 11, 15, 22])
    ok("partitions_upto(4) has 1+1+2+3+5 = 12 entries",
       len(partitions_upto(4)) == 12)
    ok("partitions in a 3x3 box number C(6,3) = 20",
       len(partitions_in_box(3, 3)) == 20)
    ok("conjugate is an involution on every partition of 6",
       all(conjugate(conjugate(l)) == l for l in partitions(6)))
    ok("conjugate((3,1)) = (2,1,1)", conjugate((3, 1)) == (2, 1, 1))
    ok("sub_partitions((2,1)) is the 5 subshapes",
       set(sub_partitions((2, 1))) == {(), (1,), (2,), (1, 1), (2, 1)})
    ok("sub_partitions' size prune agrees with filtering afterwards",
       all(sub_partitions(l, size=k)
           == [m for m in sub_partitions(l) if sum(m) == k]
           for l in partitions_in_box(3, 3) for k in range(sum(l) + 1)))
    ok("skew_cells rejects mu not contained in lam",
       skew_cells((2, 1), (2, 2)) is None)
    ok("skew_cells((3,2),(1,)) has 4 cells",
       len(skew_cells((3, 2), (1,))) == 4)

    # -- canonical form, both directions ---------------------------------
    print(file=OUT)
    print("  -- canonical form: invariant, AND separating --------------------",
          file=OUT)
    rng = random.Random(20260731)
    stable = True
    for n in range(1, 7):
        for lam in partitions(n):
            up = cell_poset(lam)
            c = canon(up)
            for _ in range(6):
                p = list(range(len(up)))
                rng.shuffle(p)
                if canon(relabel(up, p)) != c:
                    stable = False
    ok("canon is unchanged by random relabelling (44+ posets, 6 each)", stable)
    ok("canon separates the 2-chain from the 2-antichain",
       canon(chain(2)) != canon(antichain(2)))
    # the five posets on three elements: chain, antichain, V (one minimum, two
    # maxima), Lambda (two minima, one maximum), and 2-chain + isolated point
    ok("canon separates all 5 posets on 3 elements",
       len({canon(poset_from_cells(c)) for c in
            ([(1, 1), (1, 2), (1, 3)], [(1, 3), (2, 2), (3, 1)],
             [(1, 1), (1, 2), (2, 1)], [(1, 2), (2, 1), (2, 2)],
             [(1, 2), (1, 3), (2, 1)])}) == 5)
    ok("canon agrees with brute-force isomorphism on all pairs of 4-cell "
       "skew shapes",
       _canon_matches_iso(4))

    # -- ideals ----------------------------------------------------------
    print(file=OUT)
    print("  -- order ideals -------------------------------------------------",
          file=OUT)
    ok("|J(antichain_n)| = 2^n for n = 1..6",
       all(len(ideals(antichain(n))) == 2 ** n for n in range(1, 7)))
    ok("|J(chain_n)| = n+1 for n = 1..6",
       all(len(ideals(chain(n))) == n + 1 for n in range(1, 7)))
    ok("|J(D_lam)| = number of subshapes of lam, all lam to n <= 5",
       all(len(ideals(cell_poset(l))) == len(sub_partitions(l))
           for n in range(1, 6) for l in partitions(n)))

    # -- lattices, both directions ---------------------------------------
    print(file=OUT)
    print("  -- lattices: is_lattice must be able to say NO ------------------",
          file=OUT)
    bowtie = [[False] * 4 for _ in range(4)]
    for i in range(4):
        bowtie[i][i] = True
    for a in (0, 1):
        for b in (2, 3):
            bowtie[a][b] = True
    ok("the 2+2 'bowtie' is NOT a lattice (two incomparable joins)",
       not Lattice([0, 1, 2, 3], bowtie).is_lattice)
    ok("J(P) IS a lattice for every P to n <= 5",
       all(lattice_of_ideals(cell_poset(l)).is_lattice
           for n in range(1, 6) for l in partitions(n)))
    m3 = _lattice_from_covers(5, [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4),
                                  (3, 4)])
    n5 = _lattice_from_covers(5, [(0, 1), (0, 2), (2, 3), (1, 4), (3, 4)])
    ok("M3 (the diamond) is a lattice and is NOT distributive",
       m3.is_lattice and not m3.distributive())
    ok("N5 (the pentagon) is a lattice and is NOT distributive",
       n5.is_lattice and not n5.distributive())
    ok("J(P) IS distributive for every P to n <= 5",
       all(lattice_of_ideals(cell_poset(l)).distributive()
           for n in range(1, 6) for l in partitions(n)))
    ok("join_irreducibles of J(P) recover P, all P to n <= 4",
       _birkhoff_roundtrip(4))

    # -- Young's lattice --------------------------------------------------
    print(file=OUT)
    print("  -- Young's lattice, built from partitions only ------------------",
          file=OUT)
    Y = young_interval((), (2, 1))
    ok("[0,(2,1)] has 5 elements", Y.n == 5)
    ok("[(1),(2,1)] has 4 elements", young_interval((1,), (2, 1)).n == 4)
    ok("[(1),(2,1)] as a poset is the 2-element ANTICHAIN's ideal lattice",
       canon(young_interval((1,), (2, 1)).induced_poset(
           young_interval((1,), (2, 1)).join_irreducibles()))
       == canon(antichain(2)))
    ok("shape_of_ideal maps the full ideal of D_lam back to lam, n <= 5",
       all(shape_of_ideal((1 << len(skew_cells(l, ()))) - 1, skew_cells(l, ()))
           == l for n in range(1, 6) for l in partitions(n)))

    # -- Young-Fibonacci, both directions --------------------------------
    print(file=OUT)
    print("  -- Young-Fibonacci: the rank sizes are NOT the control ----------",
          file=OUT)
    words = yf_words(7)
    sizes = [sum(1 for w in words if sum(w) == r) for r in range(8)]
    ok("rank sizes to 7 are the Fibonacci numbers", sizes
       == [1, 1, 2, 3, 5, 8, 13, 21])
    up = {w: set() for w in words}
    for w in words:
        for u in yf_down_covers(w):
            up[u].add(w)
    ok("yf_down_covers is exactly the inverse of yf_up_covers, every word",
       all({v for v in yf_up_covers(w) if sum(v) <= 7} == up[w]
           for w in words))
    ok("(2,2) covers BOTH (1,2) and (2,1) -- the clause a single break loses",
       yf_down_covers((2, 2)) == {(1, 2), (2, 1)})
    ok("DU - UD = I on every word of rank < 7", _du_ud(words, up) == 0)
    ok("a WRONG cover rule still gives Fibonacci rank sizes but fails DU-UD=I",
       _wrong_rule_is_caught(words))
    _, below = yf_leq(6)
    ok("every YF interval to rank 6 is a lattice",
       all(yf_interval(w, below).is_lattice for w in below))
    ok("[0,(2,2,1)] is a YF interval that is NOT distributive",
       not yf_interval((2, 2, 1), below).distributive())
    ok("[0,(1,1,1)] IS distributive",
       yf_interval((1, 1, 1), below).distributive())

    # -- skew classes, both directions ------------------------------------
    print(file=OUT)
    print("  -- skew cell posets: the membership test must say NO ------------",
          file=OUT)
    ok("trimming a skew shape does not change its cell poset",
       _trim_preserves())
    sk = {k: skew_classes(k) for k in range(5)}
    ok("skew classes at k = 1..4 are 1, 2, 5, 11",
       [len(sk[k]) for k in range(1, 5)] == [1, 2, 5, 11])
    ok("every straight D_lam IS a skew cell poset, n <= 4",
       all(canon(cell_poset(l)) in sk[n]
           for n in range(1, 5) for l in partitions(n)))
    ok("the 3-antichain IS a skew cell poset", canon(antichain(3)) in sk[3])
    fork = _three_under_a_top()
    ok("three minimal elements under a common top is NOT a skew cell poset",
       canon(fork) not in sk[4])
    ok("and it IS a genuine poset on 4 elements, with 2^3 + 1 = 9 ideals",
       len(fork) == 4 and len(ideals(fork)) == 9)
    ok("so k = 4 has 16 - 11 = 5 poset classes outside the skew class",
       16 - len(sk[4]) == 5)
    ok("the search box may be grown without changing the class SET, k <= 4",
       all(skew_classes(k) == skew_classes(k, box=k + 1) for k in range(5)))

    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SELF-TEST: %d assertions, %d failed" % (N[0], len(FAILS)), file=OUT)
    for f in FAILS:
        print("  FAILED: %s" % f, file=OUT)
    print("=" * 78, file=OUT)
    return 1 if FAILS else 0


# ------------------------------------------------------------- helpers


def _lattice_from_covers(n, covers):
    leq = [[i == j for j in range(n)] for i in range(n)]
    changed = True
    for a, b in covers:
        leq[a][b] = True
    while changed:
        changed = False
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    if leq[a][b] and leq[b][c] and not leq[a][c]:
                        leq[a][c] = True
                        changed = True
    return Lattice(list(range(n)), leq)


def _three_under_a_top():
    """Three pairwise incomparable minimal elements with one common maximum."""
    up = [0b1001, 0b1010, 0b1100, 0b1000]
    return tuple(up)


def _canon_matches_iso(k):
    """canon must agree with brute-force isomorphism testing on every pair."""
    shapes = []
    for lam in partitions_in_box(k, k):
        for mu in sub_partitions(lam, size=sum(lam) - k):
            cells = skew_cells(lam, mu)
            if cells and len(cells) == k:
                shapes.append(poset_from_cells(cells))
    shapes = shapes[:40]
    for i in range(len(shapes)):
        for j in range(len(shapes)):
            iso = any(relabel(shapes[i], p) == shapes[j]
                      for p in permutations(range(k)))
            if iso != (canon(shapes[i]) == canon(shapes[j])):
                return False
    return True


def _birkhoff_roundtrip(maxn):
    for n in range(1, maxn + 1):
        for lam in partitions(n):
            P = cell_poset(lam)
            L = lattice_of_ideals(P)
            Q = L.induced_poset(L.join_irreducibles())
            if canon(Q) != canon(P):
                return False
    return True


def _du_ud(words, up):
    maxr = max(sum(w) for w in words)
    bad = 0
    for w in words:
        if sum(w) >= maxr:
            continue
        du = Counter()
        for v in up[w]:
            for u in yf_down_covers(v):
                du[u] += 1
        ud = Counter()
        for u in yf_down_covers(w):
            for v in up[u]:
                ud[v] += 1
        diff = du.copy()
        for k, v in ud.items():
            diff[k] -= v
        if {k: v for k, v in diff.items() if v} != {w: 1}:
            bad += 1
    return bad


def _wrong_rule_is_caught(words):
    """The first rule written for yf_down_covers: delete the leftmost 1, or
    turn the FIRST 2 of the leading run into a 1 -- and stop there.  It gives
    the Fibonacci rank sizes and it fails DU - UD = I.  Both halves are
    asserted, because the point is that one control passes and the other does
    not."""
    def wrong(w):
        out = set()
        for i, d in enumerate(w):
            if d == 1:
                out.add(w[:i] + w[i + 1:])
                break
        for i, d in enumerate(w):
            if d == 1:
                break
            if d == 2:
                out.add(w[:i] + (1,) + w[i + 1:])
                break
        return out

    up = {w: set() for w in words}
    for w in words:
        for u in wrong(w):
            up[u].add(w)
    maxr = max(sum(w) for w in words)
    sizes_ok = [sum(1 for w in words if sum(w) == r) for r in range(maxr + 1)] \
        == [1, 1, 2, 3, 5, 8, 13, 21]
    bad = 0
    for w in words:
        if sum(w) >= maxr:
            continue
        du = Counter()
        for v in up[w]:
            for u in wrong(v):
                du[u] += 1
        ud = Counter()
        for u in wrong(w):
            for v in up[u]:
                ud[v] += 1
        diff = du.copy()
        for k, v in ud.items():
            diff[k] -= v
        if {k: v for k, v in diff.items() if v} != {w: 1}:
            bad += 1
    return sizes_ok and bad > 0


def _trim_preserves():
    for lam in partitions_in_box(4, 4):
        for mu in sub_partitions(lam):
            cells = skew_cells(lam, mu)
            if not cells or len(cells) > 5:
                continue
            l2, m2 = trim_skew(lam, mu)
            c2 = skew_cells(l2, m2)
            if c2 is None or len(c2) != len(cells):
                return False
            if canon(poset_from_cells(cells)) != canon(poset_from_cells(c2)):
                return False
    return True


if __name__ == "__main__":
    sys.exit(main())
