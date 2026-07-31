"""mg-19ec's self-test.  Every assertion that matters is checked in BOTH
directions: the thing that should hold, and a deliberately broken object that
must be REFUSED.

Two of these exist because this arc recorded them firing on somebody else's
instrument, and an audit that cannot reproduce the control has no standing to
quote it:

  * A CHEAPER CANONICAL FORM CAN REPRODUCE A000112 AND STILL BE WRONG
    (mg-5800).  So `canon` is the plain n! minimum and is checked against
    brute-force isomorphism testing, not against a counting sequence.

  * THE FIBONACCI RANK SIZES ARE NOT A CONTROL ON THE COVER RULE (mg-dffa,
    and mg-5800 independently).  A wrong rule is built here and is REQUIRED to
    reproduce 1, 1, 2, 3, 5, 8, 13 and to FAIL `DU - UD = I`.

And one exists because it is the thing mg-19ec was told to protect:

  * `iso` MUST NOT BE BIRKHOFF.  It is checked to agree with `canon` on every
    ordered pair of the 63 posets on 5 elements -- 3 969 comparisons -- and
    `canon` is a relabelling minimum that knows nothing about lattices.
"""

import itertools
import random
import sys

import kern19ec as K

OUT = sys.stdout
N = [0]
BAD = [0]


def ck(label, ok):
    N[0] += 1
    if not ok:
        BAD[0] += 1
    print("  %-66s %s" % (label, "ok" if ok else "BAD"), file=OUT)
    return ok


def chain(n):
    return K.from_relations(n, [(i, j) for i in range(n) for j in range(i + 1, n)])


def antichain(n):
    return K.poset(n, set())


def main():
    print("=" * 78, file=OUT)
    print("SELF-TEST mg-19ec -- kern19ec, both directions", file=OUT)
    print("=" * 78, file=OUT)
    rnd = random.Random(19)

    # ---- posets ---------------------------------------------------------
    print("\n-- poset hygiene", file=OUT)
    ck("a 4-chain is a poset", K.check_poset(chain(4)))
    ck("a 4-antichain is a poset", K.check_poset(antichain(4)))
    ck("an untransitive relation is REFUSED",
       not K.check_poset(K.poset(3, {(0, 1), (1, 2)})))
    ck("a relation with a 2-cycle is REFUSED",
       not K.check_poset(K.poset(2, {(0, 1), (1, 0)})))
    ck("height of a 5-chain is 4", K.height(chain(5)) == 4)
    ck("height of a 5-antichain is 0", K.height(antichain(5)) == 0)

    # ---- canon ----------------------------------------------------------
    print("\n-- canon: the plain n! minimum", file=OUT)
    posets3 = []
    for pairs in itertools.chain.from_iterable(
            itertools.combinations([(i, j) for i in range(3) for j in range(3)
                                    if i != j], r) for r in range(4)):
        P = K.from_relations(3, pairs)
        if K.check_poset(P):
            posets3.append(P)
    cls3 = {K.canon(P) for P in posets3}
    ck("canon separates the 5 posets on 3 elements into exactly 5", len(cls3) == 5)
    ok = True
    for P in [chain(4), antichain(4), K.from_relations(4, [(0, 1), (0, 2), (0, 3)]),
              K.from_relations(4, [(0, 2), (1, 2), (2, 3)])]:
        c = K.canon(P)
        for _ in range(6):
            perm = list(range(4))
            rnd.shuffle(perm)
            if K.canon(K.relabel(P, perm)) != c:
                ok = False
    ck("canon invariant under 6 random relabellings of 4 shapes", ok)
    ck("canon SEPARATES a 3-chain from a 3-antichain",
       K.canon(chain(3)) != K.canon(antichain(3)))

    # ---- iso agrees with canon, and is not Birkhoff ---------------------
    print("\n-- iso: an order isomorphism search, checked against canon", file=OUT)
    posets5 = []
    seen = set()
    edges5 = [(i, j) for i in range(5) for j in range(5) if i != j]
    for r in range(len(edges5) + 1):
        if r > 6:
            break
        for pairs in itertools.combinations(edges5, r):
            P = K.from_relations(5, pairs)
            if K.check_poset(P):
                c = K.canon(P)
                if c not in seen:
                    seen.add(c)
                    posets5.append(P)
    ck("the poset classes on 5 elements found by canon: 63", len(posets5) == 63)
    agree = True
    for a in range(len(posets5)):
        for b in range(len(posets5)):
            want = K.canon(posets5[a]) == K.canon(posets5[b])
            if K.iso(posets5[a], posets5[b]) != want:
                agree = False
    ck("iso agrees with canon on all %d ordered pairs at n=5"
       % (len(posets5) ** 2), agree)
    ck("iso REFUSES a 4-chain against a 4-antichain",
       not K.iso(chain(4), antichain(4)))

    # ---- ideals and lattice ops ----------------------------------------
    print("\n-- ideals, glb/lub by search, distributivity", file=OUT)
    B3 = K.poset_of_sets(K.ideals(antichain(3)))
    ck("J(3-antichain) has 8 elements", B3[0] == 8)
    ck("J(3-antichain) is a lattice", K.is_lattice(B3))
    ck("J(3-antichain) is distributive", K.is_distributive(B3))
    ids = K.ideals(antichain(3))
    M = K.meet_table(B3)
    J = K.join_table(B3)
    okmj = all(ids[M[a][b]] == ids[a] & ids[b] and ids[J[a][b]] == ids[a] | ids[b]
               for a in range(8) for b in range(8))
    ck("glb/lub found BY SEARCH agree with intersection/union on J(A_3)", okmj)
    # M3 and N5 must come out non-distributive.
    M3 = K.from_relations(5, [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)])
    N5 = K.from_relations(5, [(0, 1), (0, 3), (1, 2), (2, 4), (3, 4)])
    ck("M3 is a lattice and is NOT distributive",
       K.is_lattice(M3) and not K.is_distributive(M3))
    ck("N5 is a lattice and is NOT distributive",
       K.is_lattice(N5) and not K.is_distributive(N5))
    bowtie = K.from_relations(4, [(0, 2), (0, 3), (1, 2), (1, 3)])
    ck("the 2+2 bowtie is REFUSED as a lattice at all", not K.is_lattice(bowtie))
    alldist = True
    for n in range(1, 5):
        for P in posets_upto(n):
            if not K.is_distributive(K.poset_of_sets(K.ideals(P))):
                alldist = False
    ck("J(P) is distributive for every poset class to n <= 4", alldist)

    # ---- partitions and Young intervals --------------------------------
    print("\n-- partitions, Young intervals, skew shapes", file=OUT)
    ck("p(6) = 11", len(K.partitions(6)) == 11)
    ck("partitions with 0 <= n <= 7 number 45", len(K.partitions_upto(7)) == 45)
    elts, L = K.young_interval((), (3, 1))
    ck("|[(), (3,1)]| = 7", len(elts) == 7)
    ck("that interval is a distributive lattice", K.is_distributive(L))
    ck("its height is 4 = |lambda|", K.height(L) == 4)
    ck("skew cells of (3,1)/(1) number 3",
       len(K.skew_cells((3, 1), (1,))) == 3)
    ck("the cell poset of (q+p,q)/(q) with p=q=2 is 2+2 disjoint chains",
       K.canon(K.cell_poset(K.skew_cells((4, 2), (2,))))
       == K.canon(K.from_relations(4, [(0, 1), (2, 3)])))
    cls = K.skew_shape_classes(4)
    ck("skew cell poset classes with 4 cells: 11", len(cls) == 11)
    ck("the 3-antichain IS a skew cell poset",
       K.canon(antichain(3)) in K.skew_shape_classes(3))
    three_under_one = K.from_relations(4, [(0, 3), (1, 3), (2, 3)])
    ck("three minima under a common top is a genuine 4-element poset",
       K.check_poset(three_under_one) and three_under_one[0] == 4)
    ck("  ... with 9 order ideals", len(K.ideals(three_under_one)) == 9)
    ck("  ... and it is REFUSED as a skew cell poset",
       K.canon(three_under_one) not in K.skew_shape_classes(4))
    ck("the search box grown from k to k+1 gives the IDENTICAL class SET at k=4",
       set(K.skew_shape_classes(4).keys())
       == set(K.skew_shape_classes(4, box=6).keys()))

    # ---- Young-Fibonacci, and the control the rank sizes are NOT --------
    print("\n-- Young-Fibonacci: the operator identity is the control", file=OUT)
    ranks = K.yf_words(6)
    sizes = [len(r) for r in ranks]
    ck("rank sizes to 6 are 1,1,2,3,5,8,13", sizes == [1, 1, 2, 3, 5, 8, 13])
    ck("total words of rank <= 6 is 33", sum(sizes) == 33)
    ck("down-covers invert up-covers on every word of rank <= 5",
       all(all(w in K.yf_up_covers(u) for u in K.yf_down_covers(w))
           and len(K.yf_down_covers(w))
               == len([u for u in ranks[sum(w) - 1] if w in K.yf_up_covers(u)])
           for r in range(1, 6) for w in ranks[r]))
    ck("DU - UD = I on every word of rank <= 5 (RIGHT rule)",
       du_ud_failures(K.yf_up_covers, 5) == 0)

    def wrong_up_covers(w):
        """A WRONG rule: insert the new 1 only at the FRONT of the leading
        2-block, never inside it."""
        a = 0
        while a < len(w) and w[a] == 2:
            a += 1
        rest = w[a:]
        out = {(1,) + (2,) * a + rest}
        if rest and rest[0] == 1:
            out.add((2,) * (a + 1) + rest[1:])
        return out

    wranks = words_from(wrong_up_covers, 6)
    ck("the WRONG rule reproduces the Fibonacci rank sizes 1,1,2,3,5,8,13",
       [len(r) for r in wranks] == [1, 1, 2, 3, 5, 8, 13])
    ck("the WRONG rule FAILS DU - UD = I  (this is the whole control)",
       du_ud_failures(wrong_up_covers, 5) > 0)

    # ---- the Birkhoff-free comparison itself ---------------------------
    print("\n-- the Birkhoff-free comparison, in both directions", file=OUT)
    _, IL = K.young_interval((2,), (4, 2))
    JP = K.poset_of_sets(K.ideals(K.cell_poset(K.skew_cells((4, 2), (2,)))))
    ck("J(C_2 + C_2) IS isomorphic to [(2),(4,2)], by order search alone",
       K.iso(JP, IL))
    _, IL2 = K.young_interval((), (2, 2))
    ck("J(C_2 + C_2) is NOT isomorphic to [(),(2,2)]", not K.iso(JP, IL2))
    JT = K.poset_of_sets(K.ideals(three_under_one))
    hits = 0
    for lam in K.partitions(4) + K.partitions(5) + K.partitions(6):
        for mu in K.partitions_upto(sum(lam)):
            if K.contains(lam, mu) and len(K.skew_cells(lam, mu)) == 4:
                _, I = K.young_interval(mu, lam)
                if K.iso(JT, I):
                    hits += 1
    ck("J(three-under-one) matches NO Young interval with 4 cells", hits == 0)

    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SELF-TEST: %d assertions, %d failed" % (N[0], BAD[0]), file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


def posets_upto(n):
    """One representative of each poset class on exactly n elements."""
    edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    seen, out = set(), []
    for r in range(len(edges) + 1):
        for pairs in itertools.combinations(edges, r):
            P = K.from_relations(n, pairs)
            if K.check_poset(P):
                c = K.canon(P)
                if c not in seen:
                    seen.add(c)
                    out.append(P)
    return out


def words_from(up, max_rank):
    ranks = [[()]]
    for r in range(1, max_rank + 1):
        cur = set()
        for w in ranks[r - 1]:
            for v in up(w):
                if sum(v) == r:
                    cur.add(v)
        ranks.append(sorted(cur))
    return ranks


def du_ud_failures(up, max_rank):
    """(DU - UD)w must equal w, as a vector, for every w of rank <= max_rank."""
    ranks = words_from(up, max_rank + 2)
    down = {}
    for r in range(1, len(ranks)):
        for w in ranks[r]:
            down[w] = [u for u in ranks[r - 1] if w in up(u)]
    bad = 0
    for r in range(0, max_rank + 1):
        for w in ranks[r]:
            vec = {}
            for v in up(w):
                for u in down.get(v, []):
                    vec[u] = vec.get(u, 0) + 1
            for u in down.get(w, []):
                for v in up(u):
                    vec[v] = vec.get(v, 0) - 1
            vec = {k: v for k, v in vec.items() if v}
            if vec != {w: 1}:
                bad += 1
    return bad


if __name__ == "__main__":
    sys.exit(main())
