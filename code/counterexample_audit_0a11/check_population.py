"""A1 -- the population, the e-groups, and whether the NEW control group is
non-vacuous.

Reproduces, from the independent kernel, every figure of

    docs/OneThird-Counterexample-Under-The-Action-Repair.md  sections 1, 2, 3

and then asks the question the repair does NOT ask of itself: for each group
it reports, WHAT WOULD A NEGATIVE RESULT HAVE LOOKED LIKE, and was it
attainable?
"""

import math
from fractions import Fraction

from kernel import Poset, enumerate_posets, qstats, restrict

NMAX = 8


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def main():
    banner("A1.0  enumeration up to isomorphism, checked against OEIS")
    lv = enumerate_posets(NMAX)
    counts = [len(lv[n]) for n in range(1, NMAX + 1)]
    orbits = [sum(math.factorial(n) // P.aut() for P in lv[n])
              for n in range(1, NMAX + 1)]
    A000112 = [1, 2, 5, 16, 63, 318, 2045, 16999]
    A001035 = [1, 3, 19, 219, 4231, 130023, 6129859, 431723379]
    print("  classes n=1..8   %s" % counts)
    print("  A000112          %s   %s" % (A000112, "OK" if counts == A000112 else "MISMATCH"))
    print("  sum n!/|Aut|     %s" % orbits)
    print("  A001035          %s   %s" % (A001035, "OK" if orbits == A001035 else "MISMATCH"))

    # ------------------------------------------------------------------
    banner("A1.1  Proposition V: every non-chain with e(P)=3 has delta=1/3")
    print("  n | non-chains e=3 | of those delta=1/3 | counterexamples to V")
    for n in range(3, NMAX + 1):
        tot = bad = ok = 0
        for P in lv[n]:
            if P.is_chain() or P.e() != 3:
                continue
            tot += 1
            if P.delta() == Fraction(1, 3):
                ok += 1
            else:
                bad += 1
        print("  %d | %14d | %18d | %d" % (n, tot, ok, bad))

    # ------------------------------------------------------------------
    banner("A1.2  the section-4 population, and both exclusions")
    print("  n | non-chains | tied | cyclic majority | population | #extremal | min delta")
    pop = {}
    for n in range(5, NMAX + 1):
        nonchain = tied = cyc = 0
        keep = []
        for P in lv[n]:
            if P.is_chain():
                continue
            nonchain += 1
            if not P.tie_free():
                tied += 1
                continue
            if P.majority_cycle() is not None:
                cyc += 1
                continue
            keep.append(P)
        pop[n] = keep
        deltas = [P.delta() for P in keep]
        mn = min(deltas)
        ext = sum(1 for d in deltas if d == Fraction(1, 3))
        print("  %d | %10d | %4d | %15d | %10d | %9d | %s"
              % (n, nonchain, tied, cyc, len(keep), ext, mn))

    # ------------------------------------------------------------------
    banner("A1.3  EVERY e-group containing an extremal poset -- no cap, no floor")
    print("  the repair's table 3.1, recomputed.  'attainable negative' asks whether")
    print("  a member of the group could have contradicted the hypothesis at all.")
    print()
    print("  n | e(P) |  N | k ext | qmass=1 | distinct delta | status      | other qmass")
    groups = []
    for n in range(5, NMAX + 1):
        byE = {}
        for P in pop[n]:
            byE.setdefault(P.e(), []).append(P)
        for ev in sorted(byE):
            grp = byE[ev]
            ext = [P for P in grp if P.delta() == Fraction(1, 3)]
            if not ext:
                continue
            qs = {}
            for P in grp:
                qf, qm, nl, good = qstats(P)
                qs[id(P)] = qm
            ones = [P for P in grp if qs[id(P)] == 1]
            dd = sorted(set(P.delta() for P in grp))
            vac = len(ext) == len(grp)
            others = sorted(set(qs[id(P)] for P in grp if P not in ext))
            print("  %d | %4d | %2d | %5d | %7d | %14d | %-11s | %s"
                  % (n, ev, len(grp), len(ext), len(ones), len(dd),
                     "VACUOUS" if vac else "non-vacuous",
                     ", ".join(str(x) for x in others) if others else "--"))
            groups.append(dict(n=n, e=ev, N=len(grp), k=len(ext),
                               ones=len(ones), vacuous=vac,
                               perfect=set(map(id, ones)) == set(map(id, ext)),
                               deltas=dd,
                               qm_ext=sorted(set(qs[id(P)] for P in ext)),
                               qm_non=others))

    # ------------------------------------------------------------------
    banner("A1.4  NON-VACUITY, established by counting the population")
    print("  A group is VACUOUS if every member is extremal (the tie cannot fail).")
    print("  For each group: k extremal of N, and the delta values actually present.")
    print()
    for g in groups:
        status = "VACUOUS" if g["vacuous"] else "non-vacuous"
        print("  n=%d e=%-3d N=%-3d extremal=%-2d non-extremal=%-2d  %s"
              % (g["n"], g["e"], g["N"], g["k"], g["N"] - g["k"], status))
        print("        delta values present: %s" % ", ".join(str(d) for d in g["deltas"]))
        print("        qmass on the extremal members     : %s"
              % ", ".join(str(x) for x in g["qm_ext"]))
        print("        qmass on the non-extremal members : %s"
              % (", ".join(str(x) for x in g["qm_non"]) if g["qm_non"] else "(none exist)"))
        if g["vacuous"]:
            print("        ATTAINABLE NEGATIVE: none -- there is no non-extremal member,")
            print("        so no assignment of qmass values could have contradicted anything.")
        else:
            print("        ATTAINABLE NEGATIVE: a non-extremal member with qmass = 1, or an")
            print("        extremal member with qmass < 1.  Both are values the statistic")
            print("        takes elsewhere in the same population, so neither is excluded")
            print("        by the definitions -- check_powered.py A5.4 counts how often the")
            print("        refuting conjunction actually occurs.  But see check_independence.py:")
            print("        NON-VACUOUS IS NOT THE SAME AS INDEPENDENT.")
        print()

    # ------------------------------------------------------------------
    banner("A1.5  the exact p-values, recomputed by enumerating C(N,k) labellings")
    print("  Statistic: mid-rank sum of qmass over the k marked members.")
    print("  Null: the k marks fall on a uniformly random k-subset of the N members.")
    print("  p = #{k-subsets with statistic >= observed} / C(N,k), enumerated in full.")
    print()
    print("  n | e | N  | k | #qmass=1 | perfect | AUC | exact p        | 1/p")
    from itertools import combinations
    for g in groups:
        if g["vacuous"]:
            continue
        n, ev = g["n"], g["e"]
        grp = [P for P in pop[n] if P.e() == ev]
        vals = [qstats(P)[1] for P in grp]
        marked = [i for i, P in enumerate(grp) if P.delta() == Fraction(1, 3)]
        N, k = len(grp), len(marked)
        # mid-ranks
        order = sorted(range(N), key=lambda i: vals[i])
        rank = [0] * N
        i = 0
        while i < N:
            j = i
            while j + 1 < N and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            mid = Fraction((i + 1) + (j + 1), 2)
            for t in range(i, j + 1):
                rank[order[t]] = mid
            i = j + 1
        obs = sum(rank[i] for i in marked)
        ge = 0
        tot = 0
        for sub in combinations(range(N), k):
            tot += 1
            if sum(rank[i] for i in sub) >= obs:
                ge += 1
        assert tot == math.comb(N, k)
        # AUC
        num = 0
        den = k * (N - k)
        for i in marked:
            for j in range(N):
                if j in marked:
                    continue
                if vals[i] > vals[j]:
                    num += 2
                elif vals[i] == vals[j]:
                    num += 1
        auc = Fraction(num, 2 * den)
        print("  %d | %d | %2d | %d | %8d | %-7s | %3s | %-14s | %d"
              % (n, ev, N, k, g["ones"], g["perfect"], auc,
                 "%d/%d" % (ge, tot), tot // ge if ge and tot % ge == 0 else 0))

    # ------------------------------------------------------------------
    print()
    print("  (the saturation control and the raw effect table are in")
    print("   check_powered.py, A5.2 and A5.3, which caches the whole-population")
    print("   qmass pass rather than recomputing it here)")


if __name__ == "__main__":
    main()
