"""A3 -- THE CONSTRUCTION.  The repair asserts a negative: the dependence
between the three e = 9 groups is the cut extension, and the honest exact p
over what is independent is 1/5.

The brief: "If the repair claims the dependence is FULLY characterised by cut
elements, that is a negative about every other dependence route: try to
construct a group member related to another by something that is not a cut
extension."

It is constructed here.  ORDER DUALITY.

Cost: about 20 seconds.
"""

import sys
from fractions import Fraction

import kern6bc as K

THIRD = Fraction(1, 3)


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
    print("A3  A SECOND DEPENDENCE ROUTE, BUILT RATHER THAN ARGUED ABOUT")

    head("1.  THE ARGUMENT, which is the repair's own with one word changed")
    print("""
    The repair's step is: two members with the same core have the same
    (delta, qmass) by a theorem, so they are not two independent chances for
    the hypothesis "qmass = 1 marks exactly the extremal members" to fail; a
    group of N members with C distinct cores offers C such chances, and the
    exact p of a perfect separation is 1/C(C, c) rather than 1/C(N, k).

    That step does not mention cut elements.  It only needs a map that FIXES
    (delta, qmass) and is not the identity.  Cut extension is one.  Here is
    another, and it is not a cut extension of anything:

      P -> P^op, the ORDER DUAL.  Inc(P^op) = Inc(P) and p_{P^op}(x,y) =
      p_P(y,x), so min(p, 1-p) is unchanged pair by pair and delta(P^op) =
      delta(P); e(P^op) = e(P) by reversing every linear extension; the
      majority relation reverses, so L*(P^op) is L* read backwards and the
      partitions into L*-intervals are the SAME partitions; a partition's
      block digraph reverses, so it is a level of P^op iff it is a level of P,
      and e(P|_B) = e(P^op|_B) block by block, so every m_X is unchanged.
      Hence qmass(P^op) = qmass(P).  EXACTLY, with nothing measured.

    Duality relates two DISTINCT CORES.  It is not a cut extension: both are
    cut-free by definition of core, so neither is an extension of the other.
""")

    head("2.  THE INVARIANCE, measured over the whole population")
    for n in (5, 6, 7):
        print("    [a3 dual n=%d]" % n, file=sys.stderr, flush=True)
        pop = {}
        for P in K.all_posets(n).values():
            r = K.analyse(P)
            if r is not None:
                pop[K.canonical(P)] = (P, r)
        closed = bad = 0
        for k, (P, r) in pop.items():
            d = K.canonical(P.dual())
            if d in pop:
                closed += 1
                rd = pop[d][1]
                if (r.e, r.delta, r.qmass) != (rd.e, rd.delta, rd.qmass):
                    bad += 1
        print("  n = %d   population %4d   dual in population %4d   "
              "(e, delta, qmass) differs %d" % (n, len(pop), closed, bad))
    print()
    print("The population is CLOSED under duality and the three statistics are")
    print("invariant on it, 775 of 775, 0 failures.  This is stronger evidence")
    print("than the repair has for qmass inheritance along cut extension (257")
    print("measured cases), because for duality it is also proved.")

    head("3.  THE FIVE CORES ARE THREE DUALITY CLASSES")
    cores = {}
    for n in (5, 6, 7, 8):
        print("    [a3 cores n=%d]" % n, file=sys.stderr, flush=True)
        for P in K.all_posets(n).values():
            r = K.analyse(P, want_q=False)
            if r is not None and r.e == 9:
                C = K.core(P)
                cores.setdefault(K.canonical(C), C)
    lab = {}
    for i, (k, C) in enumerate(sorted(cores.items(),
                                      key=lambda kv: (kv[1].n, kv[0]))):
        lab[k] = "C%d" % (i + 1)
    print("%-5s %6s %8s %8s %8s %10s  %s"
          % ("core", "size", "delta", "qmass", "dual", "self-dual", "covers"))
    for k, C in sorted(cores.items(), key=lambda kv: lab[kv[0]]):
        rc = K.analyse(C)
        d = K.canonical(C.dual())
        assert d in cores, "the family is NOT closed under duality"
        rd = K.analyse(C.dual())
        assert (rc.e, rc.delta, rc.qmass) == (rd.e, rd.delta, rd.qmass)
        print("%-5s %6d %8s %8s %8s %10s  %s"
              % (lab[k], C.n, rc.delta, rc.qmass, lab[d],
                 "yes" if d == k else "no", C.cover_string()))
    seen, classes = set(), []
    for k in sorted(cores, key=lambda x: lab[x]):
        if k in seen:
            continue
        d = K.canonical(cores[k].dual())
        cl = sorted({k, d}, key=lambda x: lab[x])
        seen |= set(cl)
        classes.append(cl)
    print()
    print("  duality classes : %s"
          % "  ".join("{%s}" % ",".join(lab[x] for x in cl) for cl in classes))
    nc = len(classes)
    ext = [cl for cl in classes if K.analyse(cores[cl[0]]).delta == THIRD]
    print("  classes                     : %d" % nc)
    print("  extremal classes            : %d" % len(ext))
    print("  qmass = 1 classes           : %d"
          % len([cl for cl in classes if K.analyse(cores[cl[0]]).qmass == 1]))
    print()
    print("FINDING (A3-1) -- THE HEADLINE.  The repair's `1/5` counts C1 and C2")
    print("as two independent chances for the hypothesis to fail, and C3 and C4")
    print("as two more.  They are not.  C2 = C1^op and C4 = C3^op, so their")
    print("(delta, qmass) agree by the same kind of theorem the repair uses to")
    print("collapse 20 members to 5 cores -- and a stronger one, since duality")
    print("needs no measurement.  Applying the repair's OWN rule to its own")
    print("cores gives %d independent units, not 5, and" % nc)
    print()
    print("      THE HONEST EXACT p OVER THE DUALITY CLASSES IS 1/%d, NOT 1/5."
          % choose(nc, len(ext)))
    print()
    print("This is a correction in the SAME direction as the repair's own -- the")
    print("evidence is weaker again, by a further factor of 5/3 -- and it is")
    print("found the way the repair's three predecessors' negatives were found:")
    print("by building the object the negative forbids, not by arguing about")
    print("sufficiency of evidence.")
    print()
    print("WHAT IT DOES NOT TOUCH.  The separation is still perfect in both")
    print("inclusions; the extremal class is still exactly the qmass = 1 class;")
    print("the section 4 null is still false.  Only the strength moves.")


if __name__ == "__main__":
    main()
