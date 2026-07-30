"""SELFTEST -- controls on THIS audit's own instrument.

An auditor's instrument needs the same treatment the auditor gives the subject.
Each item below says what it is: a POSITIVE control (a known answer reproduced),
a NEGATIVE control (a deliberate break that must be detected), or a THEOREM WITH
AN IMPLEMENTATION CHECK (mg-3b51's distinction, applied here rather than after
being asked).

Cost: about 20 seconds.
"""

import sys
from fractions import Fraction
from itertools import permutations

import kern6bc as K

fails = []


def check(kind, label, ok, detail=""):
    print("  [%-8s] %-56s %s" % (kind, label, "ok" if ok else "FAIL"))
    if detail:
        print("             %s" % detail)
    if not ok:
        fails.append(label)


def main():
    print("=" * 78)
    print("SELFTEST -- controls on kern6bc.py")
    print("=" * 78)
    print()

    # ---------------------------------------------------------------- P1
    ref = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318, 7: 2045}
    got = {n: len(K.all_posets(n)) for n in ref}
    check("POSITIVE", "enumeration against A000112, n = 1..7",
          got == ref, "%s" % got)

    # ---------------------------------------------------------------- P2
    A = K.Poset.from_relations(4, [])                    # antichain
    C = K.Poset.from_relations(4, [(0, 1), (1, 2), (2, 3)])
    eA, _ = K.le_data(A)
    eC, _ = K.le_data(C)
    check("POSITIVE", "e(antichain_4) = 24 and e(chain_4) = 1",
          (eA, eC) == (24, 1), "got %d and %d" % (eA, eC))

    # ---------------------------------------------------------------- T1
    # The defining identity of m_X, at the coarsest level: sum over ALL levels
    # of m_X is e(P), because the one-block partition's product is e(P) and
    # every level refines it.  This is a THEOREM about the definition; running
    # it checks the Mobius implementation and nothing else.
    bad = []
    nchecked = 0
    for n in (4, 5):
        for P in K.all_posets(n).values():
            r = K.analyse(P)
            if r is None:
                continue
            eB = K.sub_le_counts(P)
            levels = {}
            for blocks in K._partitions(list(range(P.n))):
                key = tuple(sorted(blocks))
                if key not in levels and K._is_level(P, key):
                    levels[key] = None
            m = {}
            for X in sorted(levels, key=len, reverse=True):
                prod = 1
                for B in X:
                    prod *= eB[B]
                m[X] = prod - sum(m[Y] for Y in K._refinements(X)
                                  if Y != X and Y in levels)
            nchecked += 1
            if sum(m.values()) != r.e:
                bad.append(P.cover_string())
    check("THEOREM", "sum of m_X over ALL levels = e(P), n = 4, 5",
          not bad, "%d posets checked, %d disagreements" % (nchecked, len(bad)))

    # ---------------------------------------------------------------- N1
    # NEGATIVE.  Break the level test so every partition counts as a level.
    # qmass must then change on at least one poset, or the level test is not
    # doing anything.
    orig = K._is_level
    try:
        K._is_level = lambda P, blocks: True
        changed = 0
        tot = 0
        for P in K.all_posets(5).values():
            r0 = orig, None
            K._is_level = orig
            a = K.analyse(P)
            K._is_level = lambda P, blocks: True
            b = K.analyse(P)
            if a is None:
                continue
            tot += 1
            if a.qmass != b.qmass:
                changed += 1
    finally:
        K._is_level = orig
    check("NEGATIVE", "breaking the level test changes qmass",
          changed > 0, "%d of %d posets at n = 5 change" % (changed, tot))

    # ---------------------------------------------------------------- N2
    # NEGATIVE for A3.  The duality measurement must be capable of failing.
    # Run the identical loop on a statistic that is NOT dual-invariant.
    pop = {}
    for P in K.all_posets(6).values():
        r = K.analyse(P, want_q=False)
        if r is not None:
            pop[K.canonical(P)] = P
    differ = 0
    for k, P in pop.items():
        d = K.canonical(P.dual())
        if d not in pop:
            continue
        nmin_P = sum(1 for i in range(P.n) if P.down[i] == 0)
        Q = pop[d]
        nmin_Q = sum(1 for i in range(Q.n) if Q.down[i] == 0)
        if nmin_P != nmin_Q:
            differ += 1
    check("NEGATIVE", "the same loop on #minimal elements DOES differ",
          differ > 0,
          "%d of %d posets at n = 6 -- so 'invariant under duality' is a\n"
          "             measurement and not a property of the loop" % (differ, len(pop)))

    # ---------------------------------------------------------------- N3
    # NEGATIVE for A1.  delta computed as a MEAN rather than a MAX must change
    # which posets are extremal.
    diff = 0
    tot = 0
    for P in K.all_posets(5).values():
        r = K.analyse(P, want_q=False)
        if r is None:
            continue
        e, cnt = K.le_data(P)
        inc = [(x, y) for x in range(P.n) for y in range(x + 1, P.n)
               if not (P.up[x] >> y & 1) and not (P.down[x] >> y & 1)]
        mean = sum(Fraction(min(cnt[x][y], cnt[y][x]), e) for x, y in inc) / len(inc)
        tot += 1
        if (mean == Fraction(1, 3)) != (r.delta == Fraction(1, 3)):
            diff += 1
    check("NEGATIVE", "mean-instead-of-max changes the extremal set",
          diff > 0, "%d of %d posets at n = 5 change status" % (diff, tot))

    # ---------------------------------------------------------------- P3
    # The pruned enumeration of A4 must agree with the full enumeration of A1
    # wherever both reach.  This is the control on the pruning argument.
    full = {}
    for n in (5, 6, 7, 8):
        for P in K.all_posets(n).values():
            e, _ = K.le_data(P)
            if e <= 9:
                full.setdefault(n, set()).add(K.canonical(P))
    cur = {}
    P = K.Poset(1, [0], [0])
    cur[K.canonical(P)] = P
    agree = True
    detail = []
    for k in range(2, 9):
        nxt = {}
        for Pp in cur.values():
            for D in K._down_sets(Pp):
                rels = [(a, b) for a in range(Pp.n) for b in K.bits(Pp.up[a])]
                rels += [(a, Pp.n) for a in K.bits(D)]
                Q = K.Poset.from_relations(k, rels)
                key = K.canonical(Q)
                if key in nxt:
                    continue
                e, _ = K.le_data(Q)
                if e <= 9:
                    nxt[key] = Q
        cur = nxt
        if k >= 5:
            if set(cur) != full[k]:
                agree = False
            detail.append("n=%d %d/%d" % (k, len(cur), len(full[k])))
    check("POSITIVE", "pruned enumeration = full enumeration on e <= 9, n = 5..8",
          agree, "  ".join(detail))

    # ---------------------------------------------------------------- P4
    # canonical() must be blind to relabelling.
    bad = 0
    P = K.Poset.from_relations(6, [(0, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 5)])
    k0 = K.canonical(P)
    for perm in list(permutations(range(6)))[:120]:
        rels = []
        for a in range(6):
            for b in K.bits(P.up[a]):
                rels.append((perm[a], perm[b]))
        if K.canonical(K.Poset.from_relations(6, rels)) != k0:
            bad += 1
    check("POSITIVE", "canonical() is blind to 120 relabellings", bad == 0,
          "%d disagreements" % bad)

    print()
    print("=" * 78)
    if fails:
        print("SELFTEST FAILURES: %d" % len(fails))
        for f in fails:
            print("  %s" % f)
        return 1
    print("ALL SELFTESTS PASS, AND THE THREE NEGATIVE CONTROLS FIRE.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
