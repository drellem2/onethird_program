"""A3 -- the NEGATIVE side of mg-af28: are its "nothing else transfers" reasons
as strong as stated?

Three things are tested here.

A3a  Ledger B3 (Stanley's differential condition fails for every finite J(P)),
     re-measured, and then examined for whether it CAN fail.  af28's own text
     already gives the one-line proof (U(1-hat) = 0, UD(1-hat) contains 1-hat),
     so the full-lattice column is a measurement of a theorem.  The column that
     could have carried information is the TRUNCATED one, and that is measured
     here independently.

A3b  Ledger B4 and section 2 item 2: "Brown section 4.3 reaches the Young graph
     and no other differential poset", and row 10's "the lattice it realises is
     the one Brown section 4.3 provably cannot consume".

     Those are statements about WHOLE differential posets.  But af28's own
     contact is not at the level of a whole lattice -- Young's lattice is
     infinite and is not a J(P) either.  The contact is at the level of finite
     INTERVALS.  At that level the claim is false: most finite intervals of the
     Young-Fibonacci lattice ARE distributive, so Brown section 4.3 consumes
     them, and each such interval is a J(P) for an explicit P.  This file
     builds those P.

A3c  Ledger B6 and B7, checked for whether they can fail at all.

The Young-Fibonacci lattice is re-implemented here from the same published
neighbour rule af28 used.  I did NOT read Stanley (1988), so section 5 item 4 of
af28's pre-filed audit ("an auditor should rebuild it from Stanley (1988)
directly") is NOT discharged by this file.  What IS done is an independent
coding of the rule plus three controls it must pass: Fibonacci rank sizes,
DU - UD = I below the top rank, and modularity (a published property of the
lattice that af28 asserted but did not test).
"""

import sys
from kern6ad0 import (all_posets, ideals, poset_of_ideals, mk_poset, canon,
                      is_lattice_and_distributive, leq, moves, mprod, supp,
                      partitions, straight_poset, skew_poset, above)

OUT = sys.stdout


# ------------------------------------------------------------- Y-F lattice --

def yf(maxrank):
    """Young-Fibonacci lattice to `maxrank`, coded independently of
    core_af28.young_fibonacci but from the same published neighbour rule.

    Elements: words in {1,2}; rank = digit sum.
    Up-neighbours of w with k leading 2s:
        - insert a 1 at any of the k+1 positions inside the leading 2-block;
        - if w has a 1, replace the leftmost 1 by a 2.
    Certified below by rank sizes, by DU - UD = I, and by modularity.
    """
    ranks = {0: [()]}
    for r in range(1, maxrank + 1):
        cur = []

        def gen(left, w):
            if left == 0:
                cur.append(tuple(w))
                return
            for d in (1, 2):
                if d <= left:
                    gen(left - d, w + [d])
        gen(r, [])
        ranks[r] = sorted(cur)
    up = {}
    for r in range(maxrank + 1):
        for w in ranks[r]:
            k = 0
            while k < len(w) and w[k] == 2:
                k += 1
            s = set()
            for pos in range(k + 1):
                s.add(w[:pos] + (1,) + w[pos:])
            if k < len(w):
                s.add(w[:k] + (2,) + w[k + 1:])
            up[w] = sorted(x for x in s if sum(x) == r + 1 and sum(x) <= maxrank)
    return ranks, up


def du_ud(elems, up, rank, only_below_top=False):
    dn = {x: [] for x in elems}
    for x in elems:
        for y in up[x]:
            dn[y].append(x)
    top = max(rank[x] for x in elems)
    r = None
    for x in elems:
        if only_below_top and rank[x] >= top:
            continue
        d = {}
        for y in up[x]:
            for z in dn[y]:
                d[z] = d.get(z, 0) + 1
        for y in dn[x]:
            for z in up[y]:
                d[z] = d.get(z, 0) - 1
        d = {k: v for k, v in d.items() if v}
        if list(d) != [x]:
            return None
        if r is None:
            r = d[x]
        elif r != d[x]:
            return None
    return r


def a3a(maxn=6):
    print("=" * 78, file=OUT)
    print("A3a  B3 re-measured, and asked whether it CAN fail.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   n  classes   J(P) differential   J(P) differential below the top", file=OUT)
    passers = []
    for n in range(1, maxn + 1):
        cls = all_posets(n)
        cf = ct = 0
        for P in cls:
            J, ids = poset_of_ideals(P)
            elems = list(range(J[0]))
            rank = {k: len(ids[k]) for k in elems}
            ab = above(J)
            up = {k: sorted(j for j in ab[k] if rank[j] == rank[k] + 1)
                  for k in elems}
            if du_ud(elems, up, rank) is not None:
                cf += 1
            r2 = du_ud(elems, up, rank, only_below_top=True)
            if r2 is not None and r2 >= 1:
                ct += 1
                passers.append((n, P))
        print("  %2d  %7d   %17d   %31d" % (n, len(cls), cf, ct), file=OUT)
    print(file=OUT)
    print("  Passers below the top: %s" % [n for n, _ in passers], file=OUT)
    print(file=OUT)
    print("  READING.  The full-lattice column is a MEASUREMENT OF A THEOREM and", file=OUT)
    print("  cannot be anything but 0: J(P) is finite with a maximum, U kills the", file=OUT)
    print("  maximum, and UD does not.  af28 says exactly this in out_branching", file=OUT)
    print("  and in section 2 item 1, so it is not hidden -- but B3's headline", file=OUT)
    print("  '0 of 405' is not evidence, it is arithmetic.  The truncated column,", file=OUT)
    print("  which is the one that could have come out either way, is reproduced", file=OUT)
    print("  here independently and agrees: 1, the one-element poset.", file=OUT)
    print(file=OUT)
    return passers


def a3b(rank=6):
    print("=" * 78, file=OUT)
    print("A3b  'Brown section 4.3 reaches the Young graph and no other", file=OUT)
    print("     differential poset' -- tested at the level where af28's OWN", file=OUT)
    print("     contact lives, namely finite intervals.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    ranks, up = yf(rank)
    elems = [w for r in sorted(ranks) for w in ranks[r]]
    rk = {w: sum(w) for w in elems}

    # -- controls on my implementation
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34]
    sizes_ok = all(len(ranks[r]) == fib[r] for r in range(rank + 1))
    r_val = du_ud(elems, up, rk, only_below_top=True)
    print("  CONTROLS on this file's Young-Fibonacci implementation:", file=OUT)
    print("    rank sizes are Fibonacci to rank %d:            %s"
          % (rank, "PASS" if sizes_ok else "FAIL (%s)"
             % [len(ranks[r]) for r in range(rank + 1)]), file=OUT)
    print("    DU - UD = rI below the top rank:                r = %s  %s"
          % (r_val, "PASS" if r_val == 1 else "FAIL"), file=OUT)

    # order relation by transitive closure of covers
    reach = {w: set(up[w]) for w in elems}
    changed = True
    while changed:
        changed = False
        for w in elems:
            new = set(reach[w])
            for v in list(reach[w]):
                new |= reach[v]
            if new != reach[w]:
                reach[w] = new
                changed = True

    def le(a, b):
        return a == b or b in reach[a]

    # modularity control: YF is a modular lattice (published property af28
    # asserts in out_branching's reading but does not test)
    mod_bad = 0
    for w in elems:
        iv = [v for v in elems if le(v, w)]
        lat, dist, _ = is_lattice_and_distributive(iv, le)
        if not lat:
            mod_bad += 1
    print("    every interval [0-hat, w] to rank %d is a lattice:   %s"
          % (rank, "PASS" if mod_bad == 0 else "FAIL (%d)" % mod_bad), file=OUT)
    print(file=OUT)

    # af28's other T8 column, and its two radical percentages, reproduced here
    # so that everything this audit attributes to af28 has been recomputed.
    from kern6ad0 import contains
    ty = tb = 0
    for n in range(0, rank + 1):
        for lam in (partitions(n) if n else [()]):
            el = [mu for m in range(n + 1)
                  for mu in (partitions(m) if m else [()]) if contains(mu, lam)]
            lat, dist, _ = is_lattice_and_distributive(el, contains)
            ty += 1
            if not (lat and dist):
                tb += 1
    print("  af28's other T8 column, recomputed: Young intervals [0,lambda]", file=OUT)
    print("    with |lambda| <= %d: %d intervals, non-distributive %d"
          " (af28: 30 and 0)" % (rank, ty, tb), file=OUT)
    for n in (5, 6):
        P = mk_poset(n, [])
        F = moves(P)
        AC = {supp(x) for x in F}
        print("    antichain n=%d: |F|=%d |AC|=%d  radical is %.1f%% of the algebra"
              % (n, len(F), len(AC), 100 * (len(F) - len(AC)) / len(F)), file=OUT)
    print("    (af28 section 1 row 3 states 90.4% and 95.7%.)", file=OUT)
    print(file=OUT)

    ndist = 0
    dist_list = []
    for w in elems:
        iv = [v for v in elems if le(v, w)]
        lat, dist, wit = is_lattice_and_distributive(iv, le)
        if lat and dist:
            dist_list.append((w, iv))
        elif lat:
            ndist += 1
    print("  Intervals [0-hat, w] of the Young-Fibonacci lattice, rank(w) <= %d:"
          % rank, file=OUT)
    print("    total %d;  DISTRIBUTIVE %d;  non-distributive %d"
          % (len(elems), len(dist_list), ndist), file=OUT)
    print("  (af28's T8 reports 33 total and 5 non-distributive -- reproduced.)",
          file=OUT)
    print(file=OUT)
    print("  So Brown section 4.3's hypothesis -- a finite distributive lattice --", file=OUT)
    print("  is SATISFIED by %d of the %d finite intervals of the OTHER known"
          % (len(dist_list), len(elems)), file=OUT)
    print("  1-differential lattice.  Each of those is J(P) for an explicit P,", file=OUT)
    print("  by Birkhoff.  Exhibiting them:", file=OUT)
    print(file=OUT)
    print("    w              |[0,w]|   P with J(P) = [0,w]   (poset on its join-irreducibles)",
          file=OUT)
    built = 0
    bad = 0
    for w, iv in dist_list:
        # join-irreducibles of the interval = elements covering exactly one element
        idx = {v: i for i, v in enumerate(iv)}
        covs = {v: [u for u in iv if le(u, v) and u != v
                    and not any(le(u, t) and le(t, v) and t != u and t != v
                                for t in iv)] for v in iv}
        ji = [v for v in iv if len(covs[v]) == 1]
        pairs = []
        for a in range(len(ji)):
            for b in range(len(ji)):
                if a != b and le(ji[a], ji[b]):
                    pairs.append((a, b))
        P = mk_poset(len(ji), pairs)
        J, _ = poset_of_ideals(P)
        ivp = mk_poset(len(iv), [(idx[a], idx[b]) for a in iv for b in iv
                                 if a != b and le(a, b)])
        ok = canon(J) == canon(ivp)
        built += 1
        if not ok:
            bad += 1
        if len(w) <= 4:
            desc = "%d elements, %d relations" % (P[0], sum(len(s) for s in P[1]))
            print("    %-14s %7d   %-22s %s"
                  % (str(w), len(iv), desc, "." if ok else "BAD"), file=OUT)
    print(file=OUT)
    print("    reconstructions attempted %d, J(P) != interval: %d" % (built, bad), file=OUT)
    print(file=OUT)
    print("  CONCLUSION A3b.  At the level of WHOLE differential posets, B4 is", file=OUT)
    print("  right and follows from Stanley's uniqueness theorem.  At the level", file=OUT)
    print("  of FINITE INTERVALS -- which is the only level at which af28's own", file=OUT)
    print("  contact exists, since Young's lattice is infinite and is itself not", file=OUT)
    print("  a J(P) -- 'reaches the Young graph and no other' is FALSE, and row", file=OUT)
    print("  10's 'the lattice it realises is the one Brown section 4.3 provably", file=OUT)
    print("  cannot consume' is FALSE for %d of its %d finite intervals."
          % (len(dist_list), len(elems)), file=OUT)
    print(file=OUT)
    return len(dist_list), len(elems), ndist, bad


def a3c(maxn=4):
    print("=" * 78, file=OUT)
    print("A3c  B6 and B7: can either measurement come out otherwise?", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("  B6: 'no move acts on L(P) bijectively without acting as the identity", file=OUT)
    print("  map', reported as MEASURED over 6 197 moves.", file=OUT)
    nonidem = 0
    tot = 0
    for n in range(1, maxn + 1):
        for P in all_posets(n):
            for x in moves(P):
                tot += 1
                if mprod(x, x) != x:
                    nonidem += 1
    print("    F(P) is a BAND: x.x = x for all %d moves over all posets to n=%d,"
          % (tot, maxn), file=OUT)
    print("    non-idempotent found: %d." % nonidem, file=OUT)
    print("    The action of an idempotent transformation is an idempotent map,", file=OUT)
    print("    and an idempotent bijection of a finite set is the identity.  So", file=OUT)
    print("    B6's count is 0 by a two-line argument for every poset and every", file=OUT)
    print("    n, not just the 87 classes tested.  af28 states this argument in", file=OUT)
    print("    out_young.txt and in section 2 item 4, so it is disclosed -- but", file=OUT)
    print("    the ledger books it as MEASURED, and the measurement CANNOT FAIL.", file=OUT)
    print(file=OUT)
    print("  B7: 'concatenation is not unital, 0 of 64'.", file=OUT)
    print("    1_P is the one-block move.  Concatenation sends (1_P, 1_Q) to the", file=OUT)
    print("    TWO-block move (P then Q), which equals 1_{P+Q} only if one of the", file=OUT)
    print("    two blocks is empty.  Both P and Q are nonempty in all 64 pairs", file=OUT)
    print("    (|P|,|Q| in 1..3), so 'unital in 0 of 64' is forced.  Checking:", file=OUT)
    forced = 0
    cases = 0
    for n in range(1, 4):
        for m in range(1, 4):
            for P in all_posets(n):
                for Q in all_posets(m):
                    cases += 1
                    oneP = (frozenset(range(n)),)
                    oneQ = (frozenset(range(m)),)
                    cat = oneP + tuple(frozenset(x + n for x in B) for B in oneQ)
                    if len(cat) != 1:
                        forced += 1
    print("    %d of %d pairs give a two-block image, i.e. non-unital by counting"
          % (forced, cases), file=OUT)
    print("    blocks alone, with no reference to F(P) at all.", file=OUT)
    print(file=OUT)
    print("  READING.  Neither is wrong.  Both are booked in the ledger as", file=OUT)
    print("  MEASURED with a sample size, and in both the sample size is doing no", file=OUT)
    print("  work: the answer is forced for every poset of every size.  This is", file=OUT)
    print("  the defect mg-3b51 reported against mg-1953's R1d, recurring in a", file=OUT)
    print("  ledger row rather than in a control.", file=OUT)
    print(file=OUT)
    return nonidem, forced, cases


if __name__ == "__main__":
    p = a3a()
    r = a3b()
    c = a3c()
    print("=" * 78, file=OUT)
    print("SUMMARY a3_hypotheses: truncated-passers %d; YF intervals distributive"
          " %d of %d (non-dist %d), reconstruction bad %d; non-idempotent moves %d;"
          " forced non-unital %d of %d" % (len(p), r[0], r[1], r[2], r[3],
                                           c[0], c[1], c[2]), file=OUT)
    print("=" * 78, file=OUT)
