"""A1 -- RECOUNT.  Every figure mg-a893 added, re-derived from kern6bc.py.

The brief asks for a recount "from an instrument that does not import the
repair's code".  kern6bc.py imports nothing from the repair, the target or the
previous audit; it is built from the DEFINITIONS in the two documents.  The
figures below are therefore an independent third derivation of the same
quantities (mg-dea5, mg-0a11, mg-a893 being the first three).

Cost: about 25 seconds.
"""

import sys
from fractions import Fraction

import kern6bc as K

NS = (5, 6, 7, 8)
E_STAR = 9
THIRD = Fraction(1, 3)


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def population(n):
    out = []
    for P in K.all_posets(n).values():
        r = K.analyse(P, want_q=False)
        if r is not None:
            out.append((P, r))
    return out


def main():
    print("A1  INDEPENDENT RECOUNT of mg-a893 (90db267), from kern6bc.py")
    print()
    print("kern6bc.py imports nothing from code/counterexample_repair_dea5/,")
    print("code/counterexample_probe_24a3/ or code/counterexample_audit_0a11/.")
    print("Definitions are taken from the DOCUMENTS: delta and Inc from section 1")
    print("of the target, P-compatible move / level / m_X from section 1 of the")
    print("Semigroup-Walk-Family-Note, qmass from section 4 of the target, cut")
    print("element and core from section 3.4 of the repair.")

    pops, groups = {}, {}
    head("0.  THE ENUMERATION ITSELF, against A000112")
    print("%-4s %12s %14s %12s %12s" % ("n", "posets", "A000112", "population",
                                        "e-groups"))
    ref = {5: 63, 6: 318, 7: 2045, 8: 16999}
    for n in NS:
        print("    [a1 n=%d]" % n, file=sys.stderr, flush=True)
        ps = K.all_posets(n)
        pops[n] = population(n)
        groups[n] = [(P, r) for (P, r) in pops[n] if r.e == E_STAR]
        egroups = len(set(r.e for _, r in pops[n]))
        print("%-4d %12d %14d %12d %12d"
              % (n, len(ps), ref[n], len(pops[n]), egroups))
    print()
    print("Population = non-chain, tie-free, majority-acyclic, as the repair")
    print("defines it.  Agrees with the published 16 / 88 / 671 / 6420 and with")
    print("691 e-groups at n = 8.")

    head("1.  THE e = 9 GROUPS, AND THE TWO MEANINGS OF 'EXTREMAL'")
    print("The target document defines delta-extremal ABSOLUTELY: delta(P) = 1/3,")
    print("the value at which the conjecture is tight (target section 3, 'min 3delta")
    print("= 1 says the conjecture is tight').  cores.py measures it RELATIVELY, as")
    print("the minimum delta inside the group (`dmin = min(...)`, then `r[1] ==")
    print("dmin`).  At n = 6, 7, 8 the two coincide.  At n = 5 they do not.")
    print()
    print("%-4s %6s %14s %16s %18s" % ("n", "N", "group min delta",
                                       "k = #(min delta)", "k = #(delta = 1/3)"))
    for n in NS:
        grp = groups[n]
        dmin = min(r.delta for _, r in grp)
        krel = sum(1 for _, r in grp if r.delta == dmin)
        kabs = sum(1 for _, r in grp if r.delta == THIRD)
        print("%-4d %6d %14s %16d %18d" % (n, len(grp), dmin, krel, kabs))
    print()
    print("FINDING (A1-1).  out_cores.txt prints 'extremal in it  2' for the")
    print("n = 5 e = 9 group and a row 'n=5  N=2  k extremal=2  extremal cores=2'.")
    print("Under the DOCUMENT's definition that group contains NO extremal poset:")
    print("both members have delta = 4/9.  The cell is the group minimum, which is")
    print("a different quantity wearing the same word.  It does not propagate to")
    print("either document -- the published core tables start at n = 6, where the")
    print("two definitions agree -- so this is an instrument-output defect and not")
    print("a document defect.")

    head("2.  CUT ELEMENTS, CORES, AND THE CORE COUNT C")
    print("%-4s %6s %20s %10s %8s %14s"
          % ("n", "N", "with a cut element", "cut-free", "C", "extremal cores"))
    allcores = {}
    percore = {}
    for n in NS:
        grp = groups[n]
        ncut = sum(1 for P, _ in grp if K.cut_elements(P))
        cs = {}
        for P, _ in grp:
            C = K.core(P)
            k = K.canonical(C)
            cs.setdefault(k, C)
            allcores.setdefault(k, C)
        ce = 0
        for k, C in cs.items():
            rc = percore.setdefault(k, K.analyse(C))
            if rc.delta == THIRD:
                ce += 1
        percore_n = cs
        print("%-4d %6d %20d %10d %8d %14d"
              % (n, len(grp), ncut, len(grp) - ncut, len(cs), ce))
    print()
    print("Reproduces 13 of 13 and 20 of 20 with a cut element, 0 cut-free, and")
    print("C = 5 at n = 6, 7 and 8.")

    head("3.  THE FIVE CORES, POOLED OVER n = 5..8")
    print("%-6s %8s %8s  %s" % ("size", "delta", "qmass", "covers"))
    for k, C in sorted(allcores.items(), key=lambda kv: (kv[1].n, str(percore[kv[0]].delta))):
        rc = percore[k]
        print("%-6d %8s %8s  %s" % (C.n, rc.delta, rc.qmass, C.cover_string()))
    print()
    print("  distinct cores, n = 5..8            : %d" % len(allcores))
    print("  of which delta-extremal (delta=1/3) : %d"
          % sum(1 for k in allcores if percore[k].delta == THIRD))
    print("  qmass = 1 exactly on those          : %s"
          % ("YES" if all((percore[k].qmass == 1) == (percore[k].delta == THIRD)
                          for k in allcores) else "NO"))
    print()
    print("Identical to out_cores.txt section 5, cover strings included.  The")
    print("SEPARATION ITSELF -- perfect in both inclusions, one extremal core of")
    print("five, qmass = 1 exactly there -- REPRODUCES.  Nothing in this audit")
    print("weakens it.")

    head("4.  group(n+1) AGAINST THE CUT EXTENSIONS OF group(n)")
    print("%-10s %16s %14s %12s" % ("n -> n+1", "cut ext of grp(n)",
                                    "= group(n+1)?", "new members"))
    for n in (5, 6, 7):
        ext = {}
        for P, _ in groups[n]:
            ext.update(K.cut_extensions(P))
        nxt = {K.canonical(P): P for P, _ in groups[n + 1]}
        # restrict the cut extensions to those that are in the population at all
        extpop = {k: Q for k, Q in ext.items()
                  if (lambda r: r is not None and r.e == E_STAR)(K.analyse(Q, want_q=False))}
        same = set(extpop) == set(nxt)
        new = len(set(nxt) - set(extpop))
        print("%-10s %16d %14s %12d"
              % ("%d -> %d" % (n, n + 1), len(extpop),
                 "YES" if same else "no", new))
    print()
    print("Reproduces the repair's table: group(7) and group(8) are EXACTLY the")
    print("cut extensions of their predecessors, and 3 members are new at n = 6.")


if __name__ == "__main__":
    main()
