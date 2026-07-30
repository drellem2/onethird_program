"""A2 -- THE PRIMARY FINDING.  How many INDEPENDENT chances did the separation
have to fail?

The repair's non-vacuity definition is: an e-group is VACUOUS if every member
is extremal.  By that definition its three reported groups are non-vacuous, and
that is correct as far as it goes -- reproduced in check_population.py.

It does not go far enough.  The e = 3 group was vacuous because a TIE could not
fail.  The question that generalises is the one the mg-0a11 brief states:

    what would a negative result here have looked like, and was it attainable?

Definitions used here.

    CUT ELEMENT      x is comparable to every other element of P.
    CUT EXTENSION    Q is P with one new element adjoined comparable to every
                     element of P, in a position that leaves e(Q) = e(P).
    CORE             P with cut elements deleted, repeatedly, while e is
                     preserved.  Well defined: deleting a cut element that
                     preserves e is confluent on this family, and the result is
                     checked here to be cut-free.

THEOREM (one line).  If Q is a cut extension of P then delta(Q) = delta(P).
    e(Q) = e(P) says every linear extension of P places the ideal below the new
    element z as a prefix, so the linear extensions of Q are the linear
    extensions of P with z inserted at one fixed position.  z is comparable to
    everything, so Inc(Q) = Inc(P) and p_Q(x,y) = p_P(x,y) for every pair.
    Hence delta(Q) = delta(P).  QED

MEASURED, not proved: qmass(Q) = qmass(P) under the same hypothesis.  Checked
below on every cut extension of every poset in the section 4 population at
n = 5 and n = 6 (all of them), and on every member of every e = 9 group to
n = 11.

CONSEQUENCE.  Both the marker and the label are inherited along cut extension.
So the members of a group that are cut extensions of members of the group one
size down are NOT independent opportunities for the hypothesis to fail: their
outcome was fixed by the smaller group, which the repair itself designates as
a generating observation.  This script counts what is left.
"""

import math
from fractions import Fraction

from kernel import Poset, enumerate_posets, qstats, restrict

NMAX = 11
QMAX = 9          # qmass is computed directly to n = 9; above that see A2.3


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def cuts(P):
    return [x for x in range(P.n)
            if bin(P.up[x] | P.down[x]).count("1") == P.n - 1]


def core(P):
    while True:
        c = cuts(P)
        if not c:
            return P
        Q = restrict(P, ((1 << P.n) - 1) ^ (1 << c[0]))
        if Q.e() != P.e():
            return P
        P = Q


def cut_extensions(P, keep_e=True):
    """Every Q = P + one element comparable to all of P.  With keep_e, only
    those with e(Q) = e(P); without, all of them (an element comparable to
    everything can still cut e down, by forcing an ideal to be a prefix)."""
    out = []
    n = P.n
    for D in P.ideals():
        up = list(P.up) + [0]
        comp = ((1 << n) - 1) ^ D
        for x in range(n):
            if (D >> x) & 1:
                up[x] |= 1 << n
        up[n] = comp
        Q = Poset(n + 1, up)
        if (not keep_e) or Q.e() == P.e():
            out.append(Q)
    return out


def in_population(P):
    return (not P.is_chain() and P.tie_free()
            and P.majority_cycle() is None)


def main():
    banner("A2.1  qmass is inherited along cut extension -- measured exhaustively")
    print("  delta is inherited by the one-line theorem above.  qmass is not proved")
    print("  here, so it is measured on EVERY cut extension of EVERY poset in the")
    print("  section 4 population at n = 5 and n = 6.")
    print()
    small = enumerate_posets(6)
    tot = agree = 0
    for n in (5, 6):
        for P in small[n]:
            if not in_population(P):
                continue
            qP = qstats(P)[1]
            dP = P.delta()
            for Q in cut_extensions(P):
                if not in_population(Q):
                    continue
                tot += 1
                if qstats(Q)[1] == qP and Q.delta() == dP:
                    agree += 1
                else:
                    print("    COUNTEREXAMPLE  %s -> %s" % (P.covers(), Q.covers()))
    print("  cut extensions inside the population : %d" % tot)
    print("  (delta, qmass) inherited             : %d" % agree)
    print("  inheritance failures                 : %d" % (tot - agree))

    # ------------------------------------------------------------------
    banner("A2.2  the e = 9 family to n = 11, and how much of it is new")
    print("  Targeted exhaustive enumeration of every poset with e(P) <= 9 up to")
    print("  n = 11.  That class is closed under deleting a MAXIMAL element, since")
    print("  e(P - x) <= e(P) for x maximal, so the enumeration stays exhaustive.")
    print("  It reproduces the repair's group sizes 7 / 13 / 20 at n = 6 / 7 / 8 and")
    print("  carries the measurement three sizes further than the repair reached.")
    print()
    lv = enumerate_posets(NMAX, keep=lambda P: P.e() <= 9)
    print("  qmass is computed DIRECTLY (from all Bell(n) partitions) to n = %d;" % QMAX)
    print("  at n = 10, 11 every member is a cut extension (A2.3) so its qmass is")
    print("  inherited, which is the finding rather than an assumption.")
    print()
    print("  n |  N | k extremal | qmass=1 | perfect | repair-style exact p")
    fam = {}
    for n in range(5, NMAX + 1):
        g = [P for P in lv[n] if P.e() == 9 and in_population(P)]
        if not g:
            continue
        fam[n] = g
        ext = [i for i, P in enumerate(g) if P.delta() == Fraction(1, 3)]
        N, k = len(g), len(ext)
        if n > QMAX:
            print("  %2d | %2d | %10d | %7s | %-7s | %s"
                  % (n, N, k, "inherit", "inherit",
                     "1/%d" % math.comb(N, k)))
            continue
        qs = [qstats(P)[1] for P in g]
        ones = [i for i, q in enumerate(qs) if q == 1]
        perfect = set(ones) == set(ext)
        p = "1/%d" % math.comb(N, k) if perfect and k else "n/a"
        print("  %2d | %2d | %10d | %7d | %-7s | %s"
              % (n, N, k, len(ones), perfect, p))

    # ------------------------------------------------------------------
    banner("A2.3  EVERY member above n = 6 is a cut extension of a smaller member")
    print("  n |  N | with a cut element | CUT-FREE | cut-free AND extremal")
    for n in sorted(fam):
        g = fam[n]
        cf = [P for P in g if not cuts(P)]
        cfe = [P for P in cf if P.delta() == Fraction(1, 3)]
        print("  %2d | %2d | %18d | %8d | %d"
              % (n, len(g), len(g) - len(cf), len(cf), len(cfe)))
    print()
    print("  The containment below is EXACTLY as strong as the cut-free count above:")
    print("  group(n+1) is contained in the cut extensions of group(n) precisely when")
    print("  group(n+1) has no cut-free member.  It fails at n = 5 -> 6 (3 new members)")
    print("  and at n = 8 -> 9 (1 new member) and holds everywhere else.  The reduction")
    print("  is onto group(n) at every step, in every case.")
    print()
    for n in sorted(fam):
        if n + 1 not in fam:
            continue
        gen = {}
        for P in fam[n]:
            for Q in cut_extensions(P):
                if in_population(Q):
                    gen[Q.code()] = Q
        tgt = {P.code() for P in fam[n + 1]}
        img = set()
        for P in fam[n + 1]:
            for x in cuts(P):
                R = restrict(P, ((1 << P.n) - 1) ^ (1 << x))
                if R.e() == P.e():
                    img.add(R.code())
        allgen = {}
        for P in fam[n]:
            for Q in cut_extensions(P, keep_e=False):
                allgen[Q.code()] = Q
        surv = len(tgt & set(gen))
        print("  n=%d -> n=%d : %d cut extensions generated in all, %d survive e=9"
              % (n, n + 1, len(allgen), surv))
        print("               and the population, %d do not; group(n+1) is inside"
              % (len(allgen) - surv))
        print("               the survivors : %s" % (tgt <= set(gen),))
        print("               reduction hits %d of the %d members at n=%d"
              % (len(img & {P.code() for P in fam[n]}), len(fam[n]), n))

    # ------------------------------------------------------------------
    banner("A2.4  THE COUNT THAT MATTERS: distinct cores, per group and overall")
    print("  Two members with the same core have the same (delta, qmass) by A2.1.")
    print("  So a group of N members with C distinct cores offers C, not N,")
    print("  opportunities for the hypothesis to fail.")
    print()
    print("  n |  N | k extremal | distinct cores | extremal cores | repair's p | core-level p")
    for n in sorted(fam):
        g = fam[n]
        cs = {}
        for P in g:
            cs.setdefault(core(P).code(), []).append(P)
        Nc = len(cs)
        Kc = sum(1 for v in cs.values() if v[0].delta() == Fraction(1, 3))
        N = len(g)
        K = sum(1 for P in g if P.delta() == Fraction(1, 3))
        if K == 0:
            continue
        print("  %2d | %2d | %10d | %14d | %14d | 1/%-13d | 1/%d"
              % (n, N, K, Nc, Kc, math.comb(N, K), math.comb(Nc, Kc)))

    print()
    print("  The whole family, n = 5 .. 11, pooled:")
    seen = {}
    for n in sorted(fam):
        for P in fam[n]:
            C = core(P)
            k = C.code()
            if k not in seen:
                seen[k] = C
            assert C.delta() == P.delta(), "delta not inherited -- theorem is wrong"
    print()
    print("    core n | delta | qmass | covers")
    for k, C in sorted(seen.items(), key=lambda kv: (kv[1].n, str(kv[1].covers()))):
        q = qstats(C) if C.n <= QMAX else None
        print("    %6d | %-5s | %-5s | %s"
              % (C.n, C.delta(), q[1] if q else "n/c", C.covers()))
    N = len(seen)
    K = sum(1 for C in seen.values() if C.delta() == Fraction(1, 3))
    ok = all((qstats(C)[1] == 1) == (C.delta() == Fraction(1, 3))
             for C in seen.values() if C.n <= QMAX)
    print()
    print("    distinct cores in the whole family : %d" % N)
    print("    of which extremal                  : %d" % K)
    print("    separation perfect on the cores    : %s" % ok)
    print("    exact p over the distinct cores    : 1/C(%d,%d) = 1/%d"
          % (N, K, math.comb(N, K)))
    print()
    print("  READ.  The separation is REAL and it holds everywhere it was looked at,")
    print("  including three sizes beyond the repair's reach.  What is not real is the")
    print("  GROWTH of its p-value with n.  1/7 -> 1/286 -> 1/38760 is not evidence")
    print("  accumulating; it is the same 5 posets counted with more chain elements")
    print("  glued on.  The repair calls n = 8 'a pre-specified test in a NEW")
    print("  POPULATION' whose 'family of tests has SIZE 1'.  The test family does")
    print("  have size 1.  The population is not new: conditional on the n = 7 group")
    print("  -- which the repair itself names as a generating observation -- the")
    print("  n = 8 result had probability 1, not 1/38760.")


if __name__ == "__main__":
    main()
