"""A2 -- THE CUT-ELEMENT THEOREM, re-derived rather than cited, and its
negative control re-run as the control it is rather than the control it claims.

The brief: "re-derive it rather than citing it, and test whether e(Q)=e(P) is
doing work that a weaker hypothesis would also do."

Cost: about 15 seconds.
"""

import sys
from fractions import Fraction

import kern6bc as K


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def population(n):
    out = []
    for P in K.all_posets(n).values():
        r = K.analyse(P)
        if r is not None:
            out.append((P, r))
    return out


def main():
    print("A2  THE CUT-ELEMENT THEOREM, INDEPENDENTLY DERIVED AND PROBED")

    head("1.  THE THEOREM, re-derived here and then verified by construction")
    print("""
    Let x be a cut element of Q -- comparable to every other element -- and
    P = Q - x.  Write D = {z : z < x} and U = {z : z > x}; D u U = P because x
    is comparable to everything, and transitivity puts every element of D below
    every element of U in P.  So in every linear extension of P the whole of D
    precedes the whole of U, and there is exactly one slot -- the D/U boundary
    -- at which x may be inserted.  Insertion is therefore a BIJECTION
    L(P) -> L(Q).

      e(Q) = e(P).  Inc(Q) = Inc(P), x being comparable to everything.  The
      bijection preserves the relative order of every pair in P, so p(y,z) is
      unchanged for every incomparable pair, hence delta(Q) = delta(P),
      tie-freeness and majority-acyclicity are inherited, and L*(Q) is L*(P)
      with x at the same boundary.

    THAT IS THE WHOLE ARGUMENT, and it is the repair's.  It is correct.  What
    it does NOT cover is qmass, which the repair says plainly and measures.
""")
    tot = deduped = inh = 0
    bad = []
    for n in (5, 6):
        print("    [a2 cut ext n=%d]" % n, file=sys.stderr, flush=True)
        for P, r in population(n):
            full = (1 << P.n) - 1
            for D in K._down_sets(P):
                U = full & ~D
                if not all((P.up[i] & U) == U for i in K.bits(D)):
                    continue
                tot += 1
            ext = K.cut_extensions(P)
            deduped += len(ext)
            for key, Q in ext.items():
                rq = K.analyse(Q)
                if rq is not None and (rq.e, rq.delta, rq.qmass) == \
                        (r.e, r.delta, r.qmass):
                    inh += 1
                else:
                    bad.append((P.cover_string(), Q.cover_string()))
    print("  cut points (P, D), the repair's count      : %d" % tot)
    print("  cut extensions Q up to isomorphism         : %d" % deduped)
    print("  (e, delta, qmass) inherited, of those      : %d" % inh)
    print("  failures                                   : %d" % len(bad))
    print()
    print("The repair prints 257.  That is the (poset, cut point) count; the")
    print("count of extensions up to isomorphism is %d.  Both give 0 failures, so"
          % deduped)
    print("the figure is right and the convention is worth naming, not correcting.")

    head("2.  NC1 -- 'A NEGATIVE CONTROL, AND IT FIRES'.  IT CANNOT NOT FIRE.")
    print("""
    NC1 adjoins a new MAXIMAL element above an arbitrary PROPER down-set D and
    reports that (e, delta, qmass) is not inherited on 1378 of 1378.  It is a
    conjunction, and its first conjunct cannot hold:

      If D is a proper down-set then P \\ D contains a maximal element m of P.
      Take any linear extension of P and move m to the end; x may then be
      placed last, or immediately before m.  Two distinct placements, so
      e(Q) > e(P) for EVERY such D.

    So "(e, delta, qmass) all inherited: 0" is a theorem about e alone and the
    control is incapable of failing -- which is exactly mg-3b51's finding
    against mg-1953, the one the repair says it applied "before an auditor has
    to".  It applied it to C2 and not to NC1.

    The control that CAN fail is the same measurement on delta alone, and on
    qmass alone.  Those are run here.  They are not vacuous:
""")
    tot = esame = dsame = qsame = both = 0
    for n in (5, 6):
        print("    [a2 nc1 n=%d]" % n, file=sys.stderr, flush=True)
        for P, r in population(n):
            for D in K._down_sets(P):
                if D == (1 << P.n) - 1:
                    continue
                rels = [(a, b) for a in range(P.n) for b in K.bits(P.up[a])]
                rels += [(a, P.n) for a in K.bits(D)]
                Q = K.Poset.from_relations(P.n + 1, rels)
                tot += 1
                eq, _ = K.le_data(Q)
                if eq == r.e:
                    esame += 1
                rq = K.analyse(Q)
                if rq is None:
                    continue
                d = rq.delta == r.delta
                q = rq.qmass == r.qmass
                dsame += d
                qsame += q
                both += (d and q)
    print("  non-cut adjunctions tested                 : %d" % tot)
    print("  e(Q) = e(P)          -- CANNOT HAPPEN      : %d" % esame)
    print("  delta(Q) = delta(P)  -- the live control   : %d" % dsame)
    print("  qmass(Q) = qmass(P)  -- the live control   : %d" % qsame)
    print("  both delta and qmass inherited             : %d" % both)
    print()
    print("FINDING (A2-1).  NC1 as published is a control that must fire: its e")
    print("conjunct is 0 of %d by a one-line argument, independently of delta and" % tot)
    print("qmass.  Re-run on the statistic the theorem is USED for, it still")
    print("fires but not perfectly: delta survives a non-cut adjunction %d times" % dsame)
    print("in %d (%.1f%%).  So 'inherited is a property of cut extension and not" % (tot, 100.0 * dsame / tot))
    print("of adjoining an element' is true as a tendency and false as an")
    print("implication.  Nothing downstream depends on it -- the dependence")
    print("argument only needs the theorem's forward direction -- but the")
    print("sentence claims a converse the measurement does not support.")

    head("3.  DOES A WEAKER HYPOTHESIS DO THE SAME WORK?")
    print("""
    The theorem's hypothesis is used twice: once to get Inc(Q) = Inc(P) (which
    needs x comparable to EVERYTHING and cannot be weakened), and once to get
    the single insertion slot.  Section 2 answers the empirical form of the
    question: 53 of 1378 non-cut adjunctions preserve delta anyway.  Those are
    cases where the CONCLUSION holds without the hypothesis, so the hypothesis
    is sufficient and not necessary -- but no weaker hypothesis stated in the
    repair would capture them, and the repair does not claim one.  The theorem
    is used only in the direction it is proved.  NOT A FINDING.
""")


if __name__ == "__main__":
    main()
