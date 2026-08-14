"""c1 -- STEP 1: `db` IS THE CYCLIC-ORIENTATION BIAS, BY TWO ROUTES THAT SHARE NO LINE.

    (db)(x,y,z) = b(x,y) + b(y,z) + b(z,x)
                = Pr[ the induced order on {x,y,z} rotates (x,y,z) ] - 1/2

The left side is computed from the three pair marginals and never builds a linear
extension; the right side enumerates `L(P)` and reads each word.  The identity is
the whole of step 1, so computing only the left and calling it a check would be
asserting the subject.  Everything is integer / `Fraction`; nothing rounds.

No clock, no randomness, no sampling: the transcript is a function of the source.
"""

import sys
from fractions import Fraction

import lib7c32 as L

NMAX_TRIPLE = 7      # exhaustive two-route triple check
NMAX_POP = 8         # exhaustive population and marginal controls
A000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318, 7: 2045, 8: 16999}

W = 88
out = sys.stdout.write


def head(t):
    out("=" * W + "\n" + t + "\n" + "=" * W + "\n")


def sec(t):
    out("\n" + t + "\n" + "-" * W + "\n")


def main():
    head("mg-7c32  c1 -- the coboundary of the pair bias IS the cyclic-orientation bias")
    status = 0

    ps = L.posets_upto(NMAX_POP)

    # -- SS0 ---------------------------------------------------------------
    sec("§0  SELF-TEST -- the generator and the marginals, before either may count anything")
    pop = {n: len(ps[n]) for n in range(1, NMAX_POP + 1)}
    ok = all(pop[n] == A000112[n] for n in pop)
    out("  unlabelled posets n = 1..%d   %s\n" % (NMAX_POP, [pop[n] for n in sorted(pop)]))
    out("  OEIS A000112                  %s   [%s]\n"
        % ([A000112[n] for n in sorted(pop)], "PASS" if ok else "FAIL"))
    status |= 0 if ok else 1

    # canonical_key cuts the relabelling search with an invariant.  The claim is
    # NOT that the key string is unchanged -- it is not, and the count below says
    # by how much -- but that the CLASSIFICATION is unchanged.  The first draft of
    # this control asserted the strings and went red; the strings were never the
    # claim, and the partition is.
    differing = 0
    partition_bad = 0
    for n in range(1, 6):
        allp = L.all_posets_bruteforce(n)
        by_cut, by_full = {}, {}
        for P in allp:
            k1, k2 = P.canonical_key()[1], P.canonical_key_unrestricted()[1]
            if k1 != k2:
                differing += 1
            by_cut.setdefault(k1, []).append(id(P))
            by_full.setdefault(k2, []).append(id(P))
        if sorted(sorted(v) for v in by_cut.values()) != \
           sorted(sorted(v) for v in by_full.values()):
            partition_bad += 1
        # and the extension enumerator against the brute-force one
        if len(by_full) != len(ps[n]):
            partition_bad += 1
    out("  canonical_key vs unrestricted relabelling, every LABELLED poset n <= 5:\n")
    out("    key STRINGS differ on %d posets -- expected, the cut moves the representative\n"
        % differing)
    out("    induced PARTITIONS differ on %d of 5 orders, and extension- vs brute-force\n"
        "    enumeration populations differ on 0   [%s]\n"
        % (partition_bad, "PASS" if partition_bad == 0 else "FAIL"))
    status |= 0 if partition_bad == 0 else 1

    # the marginal DP against brute-force enumeration of L(P)
    bad = 0
    pairs_checked = 0
    for n in range(2, NMAX_TRIPLE + 1):
        for P in ps[n]:
            tot, p = L.marginals(P)
            exts = L.linear_extensions(P)
            if len(exts) != tot:
                bad += 1
                continue
            cnt = {}
            for w in exts:
                pos = [0] * n
                for t, v in enumerate(w):
                    pos[v] = t
                for x in range(n):
                    for y in range(n):
                        if x != y and pos[x] < pos[y]:
                            cnt[(x, y)] = cnt.get((x, y), 0) + 1
            for x in range(n):
                for y in range(n):
                    if x == y:
                        continue
                    pairs_checked += 1
                    if p[(x, y)] != Fraction(cnt.get((x, y), 0), tot):
                        bad += 1
    out("  down-set DP marginals vs brute-force L(P), all posets n <= %d: %d/%d ordered pairs"
        " disagree   [%s]\n" % (NMAX_TRIPLE, bad, pairs_checked, "PASS" if bad == 0 else "FAIL"))
    status |= 0 if bad == 0 else 1

    # -- one sweep, three sections read off it -------------------------------
    half = Fraction(1, 2)
    seen_N = set()
    ntrip = 0
    bad = 0
    checked = 0
    cap = 0
    extremes = {}
    ceiling_ordered = 0
    ceiling_chain = 0
    floor_ordered = 0
    for n in range(3, NMAX_TRIPLE + 1):
        for P in ps[n]:
            tot, p = L.marginals(P)
            exts = L.linear_extensions(P)
            for x in range(n):
                for y in range(n):
                    if y == x:
                        continue
                    for z in range(n):
                        if z == x or z == y:
                            continue
                        cyc, _, nv = L.triple_class_counts(P, exts, x, y, z)
                        seen_N |= nv
                        if x < y < z:
                            ntrip += 1
                        lhs = L.db_from_marginals(p, x, y, z)
                        rhs = Fraction(cyc, tot) - half
                        checked += 1
                        if lhs != rhs:
                            bad += 1
                        if abs(lhs) > half:
                            cap += 1
                        extremes.setdefault(lhs, (n, P, (x, y, z)))
                        if lhs == half:
                            ceiling_ordered += 1
                            if (x, y) in P.less and (y, z) in P.less:
                                ceiling_chain += 1
                        if lhs == -half:
                            floor_ordered += 1

    # -- SS1 ---------------------------------------------------------------
    sec("§1  N IN {1,2} -- the triangle inequalities, restated as a count (BASIC-FACTS fact 1)")
    ok = seen_N <= {1, 2}
    out("  N = #{x<y, y<z, z<x} over every word of every L(P), all posets n = 3..%d\n"
        % NMAX_TRIPLE)
    out("  values of N observed: %s over %d unordered triples   [%s]\n"
        % (sorted(seen_N), ntrip, "PASS" if ok else "FAIL"))
    out("  N = 0 would be a 3-antichain-cycle and N = 3 a 3-cycle; a linear order admits\n"
        "  neither, so `1 <= p(x,y) + p(y,z) + p(z,x) <= 2` is this line and not a second fact.\n")
    status |= 0 if ok else 1

    # -- SS2 ---------------------------------------------------------------
    sec("§2  STEP 1 -- (db)(x,y,z) = Pr[cyclic class is (x,y,z)] - 1/2, two routes, exhaustive")
    out("  route A  b(x,y)+b(y,z)+b(z,x) from the pair marginals, no linear extension built\n")
    out("  route B  |{w in L(P) : induced order rotates (x,y,z)}| / e(P)  -  1/2\n")
    out("  ordered triples checked: %d   route disagreements: %d   [%s]\n"
        % (checked, bad, "PASS" if bad == 0 else "FAIL"))
    out("  |db| > 1/2 instances: %d   [%s]   (the ceiling is N in {1,2}, i.e. §1)\n"
        % (cap, "PASS" if cap == 0 else "FAIL"))
    status |= 0 if (bad == 0 and cap == 0) else 1

    lo, hi = min(extremes), max(extremes)
    out("  observed range of db: [%s, %s]\n" % (lo, hi))

    # -- SS3 ---------------------------------------------------------------
    sec("§3  WHERE THE CEILING IS ATTAINED -- and why step 4 has to survive it")
    out("  ordered triples with db = +1/2 : %d      with db = -1/2 : %d\n"
        % (ceiling_ordered, floor_ordered))
    out("  of the +1/2 triples, %d have x <_P y <_P z; %d / 3 = %s, and each cyclic class\n"
        % (ceiling_chain, ceiling_ordered, ceiling_ordered // 3))
    out("  is counted once per rotation, so ON THIS POPULATION db = 1/2 HOLDS EXACTLY AT THE\n"
        "  CHAIN TRIPLES: %s   [%s]\n"
        % (ceiling_ordered == 3 * ceiling_chain,
           "PASS" if ceiling_ordered == 3 * ceiling_chain else "FAIL"))
    status |= 0 if ceiling_ordered == 3 * ceiling_chain else 1
    out("""
  THIS IS THE OBSERVATION STEP 4 HAS TO SURVIVE, AND IT IS NOT A DEFECT IN THE ARITHMETIC.
  If x <_P y <_P z then all three marginals are 1, so db = 1/2 -- the ceiling, and THREE
  TIMES the 1/6 that step 4 wants the AVERAGE to sit below.  No theorem can push the mean
  of db below 1/6 over an arbitrary star: a chain refutes it outright, and a chain is a
  poset.  Step 4 is therefore irreducibly a statement about the COUNTEREXAMPLE class and
  about a CHOSEN base point; an attempt that drops either hypothesis is attacking something
  this section has already refuted.  c3 measures how far the real population sits from that
  target once the base point is spent well.
""")

    out("\nVERDICT: %s\n" % ("PASS" if status == 0 else "FAIL"))
    return status


if __name__ == "__main__":
    sys.exit(main())
