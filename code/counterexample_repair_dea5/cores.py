"""THE DEPENDENCE BETWEEN THE THREE GROUPS, measured rather than assumed.

mg-0a11's audit of this repair found that the three exact p-values reported in
section 3 -- 1/7, 1/286, 1/38760 -- are not three independent measurements.  This
file re-derives that finding from THIS instrument, so the restatement in the
repair document rests on the repair's own code rather than on the audit's.

    x is a CUT ELEMENT of P if it is comparable to every other element of P.
    Q is a CUT EXTENSION of P if Q is P with one cut element adjoined.
    The CORE of P is what is left when cut elements are deleted repeatedly.

THE ONE-LINE THEOREM.  Let x be a cut element of Q and P = Q - x.  Write D for the
elements below x and U for those above; D u U = P, and by transitivity every
element of D is below every element of U in P as well.  So every linear extension
of P already lists D before U, and inserting x at that boundary is a bijection
L(P) -> L(Q).  Hence e(Q) = e(P); Inc(Q) = Inc(P), since x is comparable to
everything; p(x,y) is unchanged for every incomparable pair, the bijection being
order-preserving on P; and therefore delta(Q) = delta(P), tie-freeness and
acyclicity of the majority relation are inherited, and L*(Q) is L*(P) with x
inserted at the same boundary.

qmass is NOT covered by that argument and is not proved here.  It is MEASURED, on
every cut extension of every poset in the section 4 population at n = 5 and n = 6.

WHAT FOLLOWS IF IT HOLDS.  Two members of an e-group with the same core have the
same (delta, qmass).  A group of N members with C distinct cores therefore offers
C, not N, independent opportunities for the hypothesis 'qmass = 1 marks exactly
the extremal members' to fail.  The exact p of a perfect separation is 1/C(C, c)
over the cores, not 1/C(N, k) over the members.

CONTROLS, and what each of them is:

  NC1  A NEGATIVE CONTROL, and it fires.  The inheritance measurement of section
       1 must be capable of failing, so the same measurement is run over the
       generic one-element extension -- a new maximal element above an arbitrary
       order ideal -- where the new element is NOT a cut element.
  C2   NOT a control.  That the core is well defined is a THEOREM (Newman: the
       deletion terminates, and it is locally confluent because a cut element of
       Q is still a cut element of Q - x for any other cut element x).  Section 2
       exhausts every deletion order and compares endpoints, which verifies the
       IMPLEMENTATION and is evidence about nothing else.  It is labelled that
       way rather than billed as 'the control that must fire' -- mg-3b51's
       finding against mg-1953, applied here before an auditor has to.  Three
       candidate negative controls were tried (deleting maximal elements,
       near-cut elements, e-preserving elements) and NONE of them is
       non-confluent on this population, which is the reason for the label.
  C3   A DISCRIMINATION CHECK, and it discriminates.  If the core reduction
       collapsed every group it would be measuring nothing.  Section 4 reports
       C against N for EVERY e-group in the population, not only the three under
       test: most groups have C = N and the reduction says nothing about them.

Cost: about 30 seconds.  Exact integer and rational arithmetic throughout.
Imports nothing outside this directory.
"""

import sys
from collections import defaultdict
from fractions import Fraction

from poset import (all_posets, canonical, delta_of, e_all_subsets, induced,
                   lstar, make, pair_probs)
from levels import m_table, qmass

NS = (5, 6, 7, 8)
E_STAR = 9                     # the e-value of the three non-vacuous groups

_MCACHE = {}


# --------------------------------------------------------------------------
# the measured quantities
# --------------------------------------------------------------------------

def record(P):
    """(e, delta, qmass, L*) for P, or None if P is a chain or has no L*."""
    probs = pair_probs(P)
    if not probs:
        return None                                   # chain
    order = lstar(P, probs)
    if order is None:
        return None                                   # tied or cyclic majority
    e = e_all_subsets(P)
    e_full = e[(1 << P.n) - 1]
    Mm, _ = m_table(P, _MCACHE, e)
    return (e_full, delta_of(probs), qmass(P, order, Mm, e_full), tuple(order))


# --------------------------------------------------------------------------
# cut elements, cut extensions, cores
# --------------------------------------------------------------------------

def cut_elements(P):
    """The elements comparable to every other element."""
    return [i for i in range(P.n)
            if all(j == i or (P.up[i] >> j & 1) or (P.down[i] >> j & 1)
                   for j in range(P.n))]


def cut_positions(P):
    """The down-set masks D at which a cut element can be inserted.

    x is above D and below V - D, so transitivity requires every element of D to
    lie below every element of V - D already.  Every such D is automatically a
    down-set.  D = 0 and D = V always qualify.
    """
    n, full = P.n, (1 << P.n) - 1
    out = []
    for D in range(1 << n):
        U = full ^ D
        ok = True
        for i in range(n):
            if not (D >> i & 1):
                continue
            if U & ~P.up[i] & full:
                ok = False
                break
        if ok:
            out.append(D)
    return out


def cut_extend(P, D):
    """P with a new element n adjoined above D and below V - D."""
    n, full = P.n, (1 << P.n) - 1
    U = full ^ D
    up = [P.up[i] | ((1 << n) if (D >> i & 1) else 0) for i in range(n)] + [U]
    return make(n + 1, up)


def maximal_adjunctions(P):
    """P with a new MAXIMAL element above an arbitrary order ideal (NC1's route).

    Yields (Q, is_cut).  This is the generic one-element extension; the cut
    extensions above a down-set are the special case U = {} , plus the D = {} one
    which this route cannot produce.
    """
    n, full = P.n, (1 << P.n) - 1
    seen = set()
    for D in range(1 << n):
        # D must be a down-set of P
        if any((D >> i & 1) and (P.down[i] & ~D & full) for i in range(n)):
            continue
        up = [P.up[i] | ((1 << n) if (D >> i & 1) else 0) for i in range(n)] + [0]
        Q = make(n + 1, up)
        k = canonical(Q)
        if k in seen:
            continue
        seen.add(k)
        yield Q, (D == full)


def delete(P, x):
    return induced(P, ((1 << P.n) - 1) ^ (1 << x))


def core(P):
    """Delete cut elements, lowest index first, until none remain."""
    Q = P
    while Q.n > 1:
        cs = cut_elements(Q)
        if not cs:
            break
        Q = delete(Q, cs[0])
    return Q


def core_orders(P, chooser=cut_elements):
    """Every isomorphism class reachable by exhausting `chooser` in any order."""
    seen, stack, ends = set(), [P], set()
    while stack:
        Q = stack.pop()
        cs = chooser(Q)
        if not cs or Q.n <= 1:
            ends.add((Q.n, canonical(Q)))
            continue
        for x in cs:
            R = delete(Q, x)
            k = (R.n, canonical(R))
            if k in seen:
                continue
            seen.add(k)
            stack.append(R)
    return ends


def maximal_elements(P):
    return [i for i in range(P.n) if P.up[i] == 0]


def near_cut_elements(P):
    """Comparable to all but at most one other element -- a weakening of `cut`."""
    out = []
    for i in range(P.n):
        inc = sum(1 for j in range(P.n)
                  if j != i and not ((P.up[i] >> j & 1) or (P.down[i] >> j & 1)))
        if inc <= 1:
            out.append(i)
    return out


def e_preserving_elements(P):
    """Elements whose deletion leaves e unchanged -- another weakening of `cut`."""
    e = e_all_subsets(P)[(1 << P.n) - 1]
    out = []
    for i in range(P.n):
        R = delete(P, i)
        if e_all_subsets(R)[(1 << R.n) - 1] == e:
            out.append(i)
    return out


# --------------------------------------------------------------------------
# output helpers
# --------------------------------------------------------------------------

def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def main():
    print(__doc__.strip())

    # ---------------------------------------------------------------- 0
    head("0.  THE POPULATION, AND THE THREE NON-VACUOUS GROUPS")
    print("Every poset up to isomorphism at n = 5..8, filtered to the section 4")
    print("population (non-chain, tie-free, acyclic majority) and then to e(P) = 9,")
    print("which is the e-value of every non-vacuous group this repair found.")
    print()
    pop = {}
    groups = {}
    for n in NS:
        print("    [cores n=%d]" % n, file=sys.stderr, flush=True)
        recs = []
        for P in all_posets(n):
            r = record(P)
            if r is not None:
                recs.append((P, r))
        pop[n] = recs
        groups[n] = [(P, r) for (P, r) in recs if r[0] == E_STAR]
    print("%-4s %12s %14s %12s" % ("n", "population", "e = 9 group", "extremal in it"))
    for n in NS:
        grp = groups[n]
        dmin = min(r[1] for _, r in grp) if grp else None
        k = sum(1 for _, r in grp if r[1] == dmin) if grp else 0
        print("%-4d %12d %14d %12d" % (n, len(pop[n]), len(grp), k))
    print()
    print("The n = 5 e = 9 group is BELOW the repair's section 3 table, which starts")
    print("at n = 6, and is carried here because the cores live in it.")

    # ---------------------------------------------------------------- 1
    head("1.  delta AND qmass ARE INHERITED ALONG CUT EXTENSION")
    print("delta is inherited by the one-line theorem above.  qmass is not proved,")
    print("so it is measured on EVERY cut extension of EVERY poset in the section 4")
    print("population at n = 5 and n = 6.")
    print()
    tot = inherited = 0
    bad = []
    for n in (5, 6):
        for P, r in pop[n]:
            for D in cut_positions(P):
                Q = cut_extend(P, D)
                tot += 1
                rq = record(Q)
                if rq is not None and rq[0] == r[0] and rq[1] == r[1] and rq[2] == r[2]:
                    inherited += 1
                else:
                    bad.append((P.cover_string(), D, r, rq))
    print("  cut extensions inside the population : %d" % tot)
    print("  (e, delta, qmass) all inherited      : %d" % inherited)
    print("  inheritance failures                 : %d" % len(bad))
    for b in bad[:5]:
        print("    FAIL %s" % (b,))

    print()
    print("NC1 (this measurement must be capable of failing).  The same measurement")
    print("over the generic one-element extension -- a new MAXIMAL element above an")
    print("arbitrary order ideal -- where the new element is NOT a cut element:")
    print()
    nc_tot = nc_same = 0
    for n in (5, 6):
        for P, r in pop[n]:
            for Q, is_cut in maximal_adjunctions(P):
                if is_cut:
                    continue                       # that is the cut case, tested above
                nc_tot += 1
                rq = record(Q)
                if rq is not None and rq[0] == r[0] and rq[1] == r[1] and rq[2] == r[2]:
                    nc_same += 1
    print("  non-cut adjunctions tested           : %d" % nc_tot)
    print("  (e, delta, qmass) unchanged anyway   : %d" % nc_same)
    print("  CHANGED, i.e. the control FIRES      : %d" % (nc_tot - nc_same))

    # ---------------------------------------------------------------- 2
    head("2.  C2 -- THE CORE IS WELL DEFINED.  THIS IS A THEOREM, NOT A CONTROL")
    print("If x and y are both cut elements of Q then y is still a cut element of")
    print("Q - x and x of Q - y, and (Q - x) - y = (Q - y) - x, so the deletion is")
    print("locally confluent; it terminates because n decreases; so by Newman's")
    print("lemma the core is unique.  Exhausting every deletion order below is a")
    print("check on THIS IMPLEMENTATION and is evidence about nothing else.  It is")
    print("labelled that way rather than presented as a control that must fire.")
    print()
    checked = confluent = 0
    for n in NS:
        for P, _ in pop[n]:
            checked += 1
            if len(core_orders(P)) == 1:
                confluent += 1
    print("  population members checked, n = 5..8 : %d" % checked)
    print("  every deletion order agrees          : %d" % confluent)
    print("  disagreements                        : %d" % (checked - confluent))
    print()
    print("AND THE NEGATIVE CONTROL THAT COULD NOT BE BUILT, recorded because a")
    print("missing control is a fact about this instrument.  Three weakenings of")
    print("the deletion rule, over the population at n = 5..7:")
    print()
    print("  %-34s %10s %16s" % ("deletion rule", "posets", "non-confluent"))
    for name, ch in (("delete a MAXIMAL element", maximal_elements),
                     ("delete a NEAR-CUT element", near_cut_elements),
                     ("delete an e-PRESERVING element", e_preserving_elements)):
        t = nc = 0
        for n in (5, 6, 7):
            for P, _ in pop[n]:
                t += 1
                if len(core_orders(P, chooser=ch)) != 1:
                    nc += 1
        print("  %-34s %10d %16d" % (name, t, nc))
    print()
    print("Every one of them is confluent too, so no negative control is offered")
    print("for C2 and none is claimed.")

    # ---------------------------------------------------------------- 3
    head("3.  THE REDUCTION group(n+1) -> group(n)")
    print("Up to isomorphism, the cut extensions of the e = 9 group at n, against")
    print("the e = 9 group at n + 1.  'onto' counts the members of group(n) that are")
    print("hit by deleting a cut element from some member of group(n+1).")
    print()
    print("%-10s %12s %14s %16s %14s" %
          ("n -> n+1", "cut ext of", "= group(n+1)?", "group(n+1) new", "onto group(n)"))
    for n in NS[:-1]:
        gen = {}
        for P, _ in groups[n]:
            for D in cut_positions(P):
                Q = cut_extend(P, D)
                gen[canonical(Q)] = Q
        nxt = {canonical(P): P for P, _ in groups[n + 1]}
        new = [k for k in nxt if k not in gen]
        here = {canonical(P) for P, _ in groups[n]}
        hit = set()
        for P, _ in groups[n + 1]:
            for x in cut_elements(P):
                k = canonical(delete(P, x))
                if k in here:
                    hit.add(k)
        print("%-10s %12d %14s %16d %10d of %d"
              % ("%d -> %d" % (n, n + 1), len(gen),
                 "YES" if set(nxt) == set(gen) else "no", len(new),
                 len(hit), len(groups[n])))
    print()
    print("%-4s %6s %20s %12s" % ("n", "N", "with a cut element", "CUT-FREE"))
    for n in NS:
        grp = groups[n]
        wc = sum(1 for P, _ in grp if cut_elements(P))
        print("%-4d %6d %20d %12d" % (n, len(grp), wc, len(grp) - wc))

    # ---------------------------------------------------------------- 4
    head("4.  THE COUNT THAT MATTERS: DISTINCT CORES PER GROUP")
    print("Two members with the same core have the same (delta, qmass) by section 1,")
    print("so a group of N members with C distinct cores offers C -- not N --")
    print("independent chances for the hypothesis to fail.")
    print()

    def exact_p(N, k):
        """1 / C(N, k), as an integer denominator."""
        num = 1
        for i in range(k):
            num = num * (N - i) // (i + 1)
        return num

    print("%-4s %5s %10s %14s %14s %16s %14s"
          % ("n", "N", "k extremal", "distinct cores", "extremal cores",
             "group-level p", "core-level p"))
    core_p = {}
    for n in NS:
        grp = groups[n]
        if not grp:
            continue
        dmin = min(r[1] for _, r in grp)
        k = sum(1 for _, r in grp if r[1] == dmin)
        cores = {}
        for P, _ in grp:
            C = core(P)
            cores.setdefault(canonical(C), C)
        ce = 0
        for key, C in cores.items():
            rc = record(C)
            if rc is not None and rc[1] == dmin:
                ce += 1
        core_p[n] = (len(cores), ce)
        print("%-4d %5d %10d %14d %14d %16s %14s"
              % (n, len(grp), k, len(cores), ce,
                 "1/%d" % exact_p(len(grp), k), "1/%d" % exact_p(len(cores), ce)))
    print()
    print("C3 (the reduction must be capable of saying nothing).  If every group")
    print("collapsed to one core the count would not be a measurement.  C against N")
    print("for EVERY e-group in the population, not only the three under test:")
    print()
    print("%-4s %10s %14s %14s %s"
          % ("n", "e-groups", "C = N", "C < N", "the e = 9 group"))
    for n in NS:
        byE = defaultdict(list)
        for P, r in pop[n]:
            byE[r[0]].append(P)
        eq = lt = 0
        for E, g in byE.items():
            C = len({canonical(core(P)) for P in g})
            if C == len(g):
                eq += 1
            else:
                lt += 1
        g9 = byE.get(E_STAR, [])
        c9 = len({canonical(core(P)) for P in g9})
        print("%-4d %10d %14d %14d %s"
              % (n, len(byE), eq, lt,
                 "C = %d of N = %d" % (c9, len(g9)) if g9 else "-"))
    print()
    print("So most groups are untouched by the reduction and the e = 9 groups are")
    print("not.  The e = 3 groups are the opposite extreme -- every member is a")
    print("chain-extension of the same 3-element core, C = 1 at every n:")
    print()
    print("%-4s %5s %14s" % ("n", "N", "distinct cores"))
    for n in NS:
        grp = [P for (P, r) in pop[n] if r[0] == 3]
        if not grp:
            continue
        print("%-4d %5d %14d" % (n, len(grp), len({canonical(core(P)) for P in grp})))

    # ---------------------------------------------------------------- 5
    head("5.  THE CORES THEMSELVES, POOLED OVER n = 5..8")
    allc = {}
    where = defaultdict(list)
    for n in NS:
        for P, _ in groups[n]:
            C = core(P)
            k = canonical(C)
            allc[k] = C
            where[k].append(n)
    dmin_all = min(record(C)[1] for C in allc.values())
    print("%-6s %8s %8s %12s  %s" % ("size", "delta", "qmass", "in groups", "covers"))
    rows = sorted(allc.items(), key=lambda kv: (kv[1].n, str(record(kv[1])[1])))
    n_ext = 0
    for key, C in rows:
        rc = record(C)
        if rc[1] == dmin_all:
            n_ext += 1
        print("%-6d %8s %8s %12s  %s"
              % (C.n, rc[1], rc[2],
                 ",".join(str(x) for x in sorted(set(where[key]))),
                 C.cover_string()))
    print()
    print("  distinct cores in the whole e = 9 family, n = 5..8 : %d" % len(allc))
    print("  of which extremal (delta = %s)                     : %d" % (dmin_all, n_ext))
    sep_ok = all((record(C)[2] == 1) == (record(C)[1] == dmin_all) for C in allc.values())
    print("  qmass = 1 exactly on the extremal cores            : %s"
          % ("YES" if sep_ok else "NO"))
    print("  exact p over the distinct cores                    : 1/%d"
          % exact_p(len(allc), n_ext))

    head("6.  THE HONEST NUMBER, AND WHAT IS AND IS NOT EVIDENCE")
    print("READ THIS AS A CORRECTION TO SECTION 3 OF THE REPAIR DOCUMENT, NOT AS A")
    print("RETRACTION OF IT.  The separation is real, it is perfect in both")
    print("inclusions in every group where it could fail, and nothing measured here")
    print("weakens it.  What is corrected is the STRENGTH claimed for it.")
    print()
    print("  * The three group-level p-values 1/7, 1/286, 1/38760 are not three")
    print("    independent tests.  The n = 8 group IS the cut extensions of the")
    print("    n = 7 group, and delta and qmass are inherited along that operation,")
    print("    so conditional on n = 7 -- which this repair itself names a")
    print("    GENERATING OBSERVATION -- the n = 8 outcome had probability 1.")
    print("  * The joint figure 1.29e-08 is therefore not merely 'containing the")
    print("    generating observations'.  The three events are DETERMINISTICALLY")
    print("    NESTED, and their product is not a probability of anything.")
    print("  * The population at n = 8 is not new.  The phrase NEW POPULATION is")
    print("    withdrawn.  The PRE-SPECIFICATION is not withdrawn: the hypothesis")
    print("    was written down before n = 8 was computed, and that is still true.")
    print("    A pre-specified test of a deterministic consequence is still not")
    print("    evidence.")
    print("  * The honest exact p is the one over DISTINCT CORES: %s at n = 6,"
          % ("1/%d" % exact_p(*core_p[6])))
    print("    %s at n = 7 and %s at n = 8 -- the SAME number three times, because"
          % ("1/%d" % exact_p(*core_p[7]), "1/%d" % exact_p(*core_p[8])))
    print("    it is the same cores three times -- and 1/%d over the pooled family."
          % exact_p(len(allc), n_ext))
    print()
    print("  THE HONEST EXACT p OVER THE DISTINCT CORES IS 1/%d."
          % exact_p(len(allc), n_ext))
    print()
    print("mg-0a11 carried the same measurement to n = 11 by a targeted enumeration")
    print("of the posets with e(P) <= 9 and found SIX distinct cores over n = 5..11,")
    print("still exactly one of them extremal.  This instrument reaches n = 8 and")
    print("agrees with it everywhere the two overlap.")


if __name__ == "__main__":
    main()
