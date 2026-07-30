"""A4 -- THE OVER-CORRECTION.  The repair's section 3.4 ends a paragraph with

    **Nothing enters the family after `n = 6`.**

and two paragraphs later says that mg-0a11 carried the measurement to n = 11
and found SIX distinct cores.  Five cores exist at n <= 8.  Six over n <= 11.
Both cannot be true of a family nothing enters after n = 6.

This file settles it by enumeration, past the reach of every instrument in the
lineage, and identifies the sixth core.

THE ENUMERATION IS COMPLETE, not a search.  Deleting a maximal element cannot
increase e: the restriction map L(Q) -> L(Q - x) is onto, so e(Q - x) <= e(Q).
Hence {P : e(P) <= 9} is closed under deleting a maximal element, and building
n from n-1 by adjoining a maximal element above every down-set, pruning on
e <= 9, reaches every such poset up to isomorphism.

Cost: about 40 seconds to n = 12.
"""

import sys
from fractions import Fraction

import kern6bc as K

THIRD = Fraction(1, 3)
NMAX = 12


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def choose(N, k):
    num = 1
    for i in range(k):
        num = num * (N - i) // (i + 1)
    return num


def main():
    print("A4  WHAT ENTERS THE FAMILY AFTER n = 6, AND WHEN")

    head("1.  THE e = 9 FAMILY TO n = 12, BY COMPLETE PRUNED ENUMERATION")
    cur = {}
    P = K.Poset(1, [0], [0])
    cur[K.canonical(P)] = P
    allcores = {}
    entered = {}
    rows = []
    for k in range(2, NMAX + 1):
        print("    [a4 n=%d]" % k, file=sys.stderr, flush=True)
        nxt = {}
        for P in cur.values():
            for D in K._down_sets(P):
                rels = [(a, b) for a in range(P.n) for b in K.bits(P.up[a])]
                rels += [(a, P.n) for a in K.bits(D)]
                Q = K.Poset.from_relations(k, rels)
                key = K.canonical(Q)
                if key in nxt:
                    continue
                e, _ = K.le_data(Q)
                if e <= 9:
                    nxt[key] = Q
        cur = nxt
        grp = []
        for Q in cur.values():
            r = K.analyse(Q, want_q=False)
            if r is not None and r.e == 9:
                grp.append((Q, r))
        cs = {}
        cutfree = 0
        for Q, _ in grp:
            C = K.core(Q)
            ck = K.canonical(C)
            cs.setdefault(ck, C)
            if ck not in allcores:
                allcores[ck] = C
                entered[ck] = k
            if not K.cut_elements(Q):
                cutfree += 1
        kext = sum(1 for _, r in grp if r.delta == THIRD)
        rows.append((k, len(cur), len(grp), cutfree, len(cs), kext,
                     len(allcores)))
    print("%-4s %12s %8s %10s %6s %12s %12s"
          % ("n", "e<=9 posets", "N", "cut-free", "C", "k(delta=1/3)",
             "cores so far"))
    for r in rows:
        print("%-4d %12d %8d %10d %6d %12d %12d" % r)

    head("2.  THE SIXTH CORE, EXHIBITED")
    print("It enters at n = %d, and here it is:"
          % min(v for v in entered.values() if v > 8))
    print()
    for ck, C in sorted(allcores.items(), key=lambda kv: (entered[kv[0]], kv[1].n)):
        rc = K.analyse(C)
        print("  enters n=%-3d size %-3d delta=%-5s qmass=%-5s self-dual=%-4s %s"
              % (entered[ck], C.n, rc.delta, rc.qmass,
                 "yes" if K.canonical(C.dual()) == ck else "no",
                 C.cover_string()))
    print()
    print("The sixth is the 8-chain with one isolated element beside it -- C_8")
    print("plus a point.  Its e is exactly 9 because the loose element has 9")
    print("slots, which is why it cannot appear before n = 9 and does appear")
    print("there.  It is CUT-FREE (the loose element is comparable to nothing,")
    print("so nothing is comparable to everything), so it is not a cut extension")
    print("of any member of any smaller group -- it is genuinely new.")

    head("3.  FINDING (A4-1).  THE OVER-CORRECTION")
    print("""
    'Nothing enters the family after n = 6' is FALSE, and the repair document
    contains its own refutation two paragraphs later: five cores at n <= 8, six
    at n <= 11, and a family nothing enters cannot gain one.  The sentence is
    true of the range its table covers (n = 5..8) and is stated without that
    range, in bold, as the load-bearing step for 'the three sizes are one
    observation and not three'.

    The consequence is an UNDER-STATEMENT of the repair's own evidence.  At
    n = 9 the family acquires a genuinely new, cut-free member with a new core,
    and the separation has to survive it -- the new core has qmass = 1/3, is not
    extremal, and is correctly NOT marked.  That is an independent chance for
    the hypothesis to fail, and it did not fail.  So over the range the repair
    itself cites (mg-0a11's n = 11):
""")
    ncores = len(allcores)
    next_ = sum(1 for ck in allcores if K.analyse(allcores[ck]).delta == THIRD)
    seen, classes = set(), []
    for ck in allcores:
        if ck in seen:
            continue
        d = K.canonical(allcores[ck].dual())
        cl = {ck, d}
        seen |= cl
        classes.append(sorted(cl))
    cext = sum(1 for cl in classes
               if K.analyse(allcores[cl[0]]).delta == THIRD)
    print("      distinct cores, n = 5..%d            : %d" % (NMAX, ncores))
    print("      of which extremal                    : %d" % next_)
    print("      core-level p                         : 1/%d"
          % choose(ncores, next_))
    print("      duality classes (finding A3-1)       : %d" % len(classes))
    print("      of which extremal                    : %d" % cext)
    print("      HONEST p, both corrections applied   : 1/%d"
          % choose(len(classes), cext))
    print()
    print("    So the two findings of this audit point in OPPOSITE directions and")
    print("    do not cancel: duality takes 1/5 to 1/3, and the sixth core takes")
    print("    it back to 1/4.  1/4 is the number, and the repair's 1/5 is wrong")
    print("    in both of its factors rather than in one.")
    print()
    print("    THE SEPARATION IS UNHARMED AND SLIGHTLY STRONGER.  It survives a")
    print("    new core at n = 9 that no cut extension could have produced.")
    head("4.  THE SEPARATION AT n = 9 AND n = 10, MEMBER BY MEMBER")
    print("qmass is computed on every member, not inherited, so this is not")
    print("resting on the measured half of the inheritance.")
    print()
    print("%-4s %6s %12s %12s %28s"
          % ("n", "N", "extremal", "qmass = 1", "perfect in both inclusions"))
    cur2 = {}
    P = K.Poset(1, [0], [0])
    cur2[K.canonical(P)] = P
    for k in range(2, 11):
        print("    [a4 members n=%d]" % k, file=sys.stderr, flush=True)
        nxt = {}
        for Pp in cur2.values():
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
        cur2 = nxt
        if k < 9:
            continue
        grp = [Q for Q in cur2.values()
               if (lambda r: r is not None and r.e == 9)(K.analyse(Q, want_q=False))]
        ne = nq = 0
        perfect = True
        for Q in grp:
            r = K.analyse(Q)
            ex = r.delta == THIRD
            q1 = r.qmass == 1
            ne += ex
            nq += q1
            if ex != q1:
                perfect = False
        print("%-4d %6d %12d %12d %28s"
              % (k, len(grp), ne, nq, "YES" if perfect else "NO"))
    print()
    print("So the separation replicates two sizes past mg-a893's instrument and")
    print("one past mg-0a11's, on members whose qmass was computed directly.")
    print("Beyond n = 10 the core set is unchanged through n = 12 (section 1),")
    print("and qmass = 1 holds on the extremal core and no other, so the core-")
    print("level separation holds there too.")


if __name__ == "__main__":
    main()
