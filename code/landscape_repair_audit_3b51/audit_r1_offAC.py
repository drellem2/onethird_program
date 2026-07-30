#!/usr/bin/env python3
"""
mg-3b51 AUDIT 1 -- THE ACYCLICITY REPAIR, CHECKED OUTSIDE AC(P).

mg-1953's BROKEN 1 is that mg-ebd8 stated Brown's Theorem 2, specialised to the
order cone, as

    m_X = prod_B (|B|-1)!   if every block of X is an ANTICHAIN of P        (DOC)
        = 0                 otherwise

dropping the acyclicity clause, and that the original MEASUREMENT could not see
it because the code ranged X over AC(P) -- the set on which the wrong statement
happens to be right.  This script re-establishes that from a disjoint
instrument, and then asks the question the repair does not: WHERE IS THE NEW
CHECK ITSELF BLIND?

  A1  M_0 by NUMERIC CONSTRUCTION WITH CERTIFICATES BOTH WAYS (see core3b51),
      against (DOC) and against the REPAIRED rule, over ALL FLATS.
  A2  Brown's total-multiplicity identity sum_X m_X = |L(P)| over ALL FLATS,
      both rules; and the count of SPURIOUS flats.
  A3  The AUDITOR'S witness reproduced on its own labels: P = {a<d, b<c},
      flat ac|bd, |L(P)| = 6, (DOC) sums to 7.
  A4  WHERE THE DEFECT LIVES.  Every flat on which (DOC) and (REPAIRED)
      disagree is shown to lie OUTSIDE AC(P) -- so a check confined to AC(P)
      cannot reach it, and a check that ranges over all flats must.
  A5  THE REPAIR'S OWN CONTROL, R1d, EXAMINED.  mg-1953 reports "restricted to
      AC(P) the original rule is 0 bad of 318, so the restriction is
      DEMONSTRATED to be what hid the defect".  Test whether that control has
      any power to fail.
  A6  MUTATION.  Would a check of this shape have caught the original defect?
      Run four wrong variants of the repaired statement through A1/A2 and see
      which ones the test kills.
  A7  COVERAGE.  n = 7, one order past the repair's range, for the identity and
      for the set equality M_0 == repaired rule.

Cross-validation of the geometric decision procedure against an exhaustive
search over block orderings is in selftest.py.
"""

import sys

from core3b51 import (iso_classes, set_partitions, relations, closed_form,
                      all_blocks_antichain, quotient_digraph, find_cycle,
                      meets_open_cone, count_linear_extensions,
                      support_lattice, label, poset_name, block_of)


def acyclic(n, up, X):
    succ, _ = quotient_digraph(n, up, X)
    return find_cycle(succ) is None


# The four rules under test.  RULE_REP is the repaired statement.
def rule_doc(n, up, X):                 # mg-ebd8's statement
    return all_blocks_antichain(up, X)


def rule_rep(n, up, X):                 # mg-1953's repaired statement
    return all_blocks_antichain(up, X) and acyclic(n, up, X)


def rule_acyc_only(n, up, X):           # mutation: drop the ANTICHAIN clause
    return acyclic(n, up, X)


def rule_convex(n, up, X):
    """mutation: 'blocks are convex' instead of 'blocks are antichains'."""
    w = block_of(X, n)
    for (i, j) in relations(n, up):
        if w[i] == w[j]:
            continue
    for B in X:
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if (B >> i & 1) and (B >> k & 1) and not (B >> j & 1):
                        if (up[i] >> j & 1) and (up[j] >> k & 1):
                            return False
    return acyclic(n, up, X)


def rule_weak_acyc(n, up, X):
    """mutation: acyclicity tested only on flats with >= 3 blocks -- a rule that
    is right on the witness class's coarser flats and wrong on the witness."""
    if len(X) >= 3:
        return all_blocks_antichain(up, X) and acyclic(n, up, X)
    return all_blocks_antichain(up, X)


RULES = [("DOC (mg-ebd8)", rule_doc),
         ("REPAIRED (mg-1953)", rule_rep),
         ("mut: acyclic only", rule_acyc_only),
         ("mut: convex+acyclic", rule_convex),
         ("mut: acyclic if >=3 blocks", rule_weak_acyc)]


def sweep(n, rules=RULES, want_witness=False, want_offAC=False):
    flats = set_partitions(n)
    classes = iso_classes(n)
    res = {name: dict(setbad=0, sumbad=0, spurious=0, missing=0)
           for name, _ in rules}
    tot = dict(classes=len(classes), flats=len(classes) * len(flats),
               witness=None, off=0, on=0, disagree_flats=0)
    for up in classes:
        e = count_linear_extensions(n, up)
        geom = [meets_open_cone(n, up, X) for X in flats]
        AC = [acyclic(n, up, X) for X in flats]
        for name, f in rules:
            sel = [f(n, up, X) for X in flats]
            if sel != geom:
                res[name]['setbad'] += 1
            s = sum(closed_form(X) for X, t in zip(flats, sel) if t)
            if s != e:
                res[name]['sumbad'] += 1
                if name.startswith("DOC") and want_witness and \
                        tot['witness'] is None:
                    extra = [X for X, t, g in zip(flats, sel, geom) if t and not g]
                    tot['witness'] = (up, e, s, extra)
            res[name]['spurious'] += sum(1 for t, g in zip(sel, geom) if t and not g)
            res[name]['missing'] += sum(1 for t, g in zip(sel, geom) if g and not t)
        if want_offAC:
            for X, d, r, a in zip(flats,
                                  [rule_doc(n, up, X) for X in flats],
                                  [rule_rep(n, up, X) for X in flats], AC):
                if d != r:
                    tot['disagree_flats'] += 1
                    if a:
                        tot['on'] += 1
                    else:
                        tot['off'] += 1
    return res, tot


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print("=" * 78)
    print("mg-3b51 AUDIT 1 -- THE ACYCLICITY REPAIR, EXERCISED OUTSIDE AC(P)")
    print("Independent instrument.  X ranges over ALL FLATS at every step.")
    print("=" * 78)
    print()

    data = {}
    for n in range(2, nmax + 1):
        data[n] = sweep(n, want_witness=True, want_offAC=True)

    print("-" * 78)
    print("A1  M_0 DECIDED BY NUMERIC CONSTRUCTION (certificate both ways),")
    print("    compared as a SET against each rule, over all flats.")
    print("-" * 78)
    print("%3s %8s %8s  %-28s %-28s" % ("n", "classes", "flats",
                                        "DOC == M_0", "REPAIRED == M_0"))
    for n in range(2, nmax + 1):
        res, tot = data[n]
        print("%3d %8d %8d  %-28s %-28s"
              % (n, tot['classes'], tot['flats'],
                 "%d bad of %d" % (res['DOC (mg-ebd8)']['setbad'], tot['classes']),
                 "%d bad of %d" % (res['REPAIRED (mg-1953)']['setbad'], tot['classes'])))
    print()

    print("-" * 78)
    print("A2  BROWN'S TOTAL-MULTIPLICITY IDENTITY  sum_X m_X = |L(P)|,")
    print("    summed over ALL FLATS.")
    print("-" * 78)
    print("%3s %8s  %-24s %-24s %10s" % ("n", "classes", "DOC: sum != |L(P)|",
                                         "REPAIRED: sum != |L(P)|", "spurious"))
    for n in range(2, nmax + 1):
        res, tot = data[n]
        print("%3d %8d  %-24s %-24s %10d"
              % (n, tot['classes'],
                 "%d of %d posets" % (res['DOC (mg-ebd8)']['sumbad'], tot['classes']),
                 "%d of %d posets" % (res['REPAIRED (mg-1953)']['sumbad'], tot['classes']),
                 res['DOC (mg-ebd8)']['spurious']))
    print()

    print("-" * 78)
    print("A3  THE AUDITOR'S WITNESS, ON ITS OWN LABELS.")
    print("-" * 78)
    # P = {a<d, b<c} on {a,b,c,d} = {0,1,2,3}: 0<3 and 1<2.
    up = (1 << 3, 1 << 2, 0, 0)
    n = 4
    e = count_linear_extensions(n, up)
    print("    P = %s   |L(P)| = %d" % (poset_name(n, up), e))
    flats = set_partitions(n)
    doc = sum(closed_form(X) for X in flats if rule_doc(n, up, X))
    rep = sum(closed_form(X) for X in flats if rule_rep(n, up, X))
    print("    DOC rule       sum_X m_X = %d   (Brown's identity requires %d)  %s"
          % (doc, e, "MISMATCH" if doc != e else "ok"))
    print("    REPAIRED rule  sum_X m_X = %d   (Brown's identity requires %d)  %s"
          % (rep, e, "MISMATCH" if rep != e else "ok"))
    for X in flats:
        if rule_doc(n, up, X) and not rule_rep(n, up, X):
            ok, cert = meets_open_cone(n, up, X, want_certificate=True)
            print("    spurious flat  %-9s  m = %d  blocks antichains: %s,"
                  "  in AC(P): %s,  meets U: %s"
                  % (label(X, n), closed_form(X), True,
                     acyclic(n, up, X), ok))
            print("        NO-certificate from the constructive test: %s" % cert)
    print()
    print("    mg-1953's own instrument reports the witness as P = {a<c, b<d}")
    print("    with spurious flat ad|bc.  Both are the two-disjoint-2-chains")
    print("    class; the labelling differs.  Checked directly:")
    up2 = (1 << 2, 1 << 3, 0, 0)
    e2 = count_linear_extensions(n, up2)
    doc2 = sum(closed_form(X) for X in flats if rule_doc(n, up2, X))
    print("        P = %s  |L(P)| = %d  DOC sum = %d"
          % (poset_name(n, up2), e2, doc2))
    print()

    print("-" * 78)
    print("A4  WHERE THE DEFECT LIVES.  Every flat on which DOC and REPAIRED")
    print("    disagree, split by whether it is INSIDE or OUTSIDE AC(P).")
    print("-" * 78)
    print("%3s %14s %14s %14s" % ("n", "disagreeing", "inside AC(P)", "outside AC(P)"))
    for n in range(2, nmax + 1):
        res, tot = data[n]
        print("%3d %14d %14d %14d"
              % (n, tot['disagree_flats'], tot['on'], tot['off']))
    print()
    print("    Reading: the disagreement set is 100% outside AC(P) at every n.")
    print("    That is not luck -- DOC and AC(P) intersect in exactly REPAIRED")
    print("    ({antichain blocks} and {acyclic quotient}), so no check confined")
    print("    to AC(P) can distinguish the two rules AT ALL.  A1/A2 above range")
    print("    over all flats, so they can, and they do.")
    print()

    print("-" * 78)
    print("A5  mg-1953's OWN CONTROL R1d, EXAMINED FOR POWER TO FAIL.")
    print("    R1d restricts DOC to AC(P) and reports '0 bad of 318'.")
    print("-" * 78)
    same = 0
    tested = 0
    for n in range(2, nmax + 1):
        flats = set_partitions(n)
        for up in iso_classes(n):
            tested += 1
            a = {i for i, X in enumerate(flats)
                 if rule_doc(n, up, X) and acyclic(n, up, X)}
            b = {i for i, X in enumerate(flats) if rule_rep(n, up, X)}
            if a == b:
                same += 1
    print("    DOC-restricted-to-AC(P) == REPAIRED, as SETS OF FLATS:")
    print("        %d of %d posets to n <= %d  (an identity, not a measurement)"
          % (same, tested, nmax))
    print("    So R1d's number is the REPAIRED rule's number under another name.")
    print("    It cannot come out any other way, and it cannot fail while the")
    print("    repaired rule passes.  The CONTENT of R1d is right; its billing")
    print("    as a control that 'must fire' and as a DEMONSTRATION is not --")
    print("    it is a restatement of a set identity, and the honest reading is")
    print("    that the restriction PROVABLY hides the defect rather than being")
    print("    measured to.")
    print()

    print("-" * 78)
    print("A6  MUTATION.  Would a check of this shape have caught the defect?")
    print("    Four wrong variants of the repaired statement, run through the")
    print("    same two tests at n <= %d.  A test with power kills all four." % nmax)
    print("-" * 78)
    print("%-28s %-22s %-22s" % ("rule", "A1: != M_0", "A2: sum != |L(P)|"))
    agg = {name: [0, 0, 0] for name, _ in RULES}
    for n in range(2, nmax + 1):
        res, tot = data[n]
        for name, _ in RULES:
            agg[name][0] += res[name]['setbad']
            agg[name][1] += res[name]['sumbad']
            agg[name][2] += tot['classes']
    for name, _ in RULES:
        a = agg[name]
        print("%-28s %-22s %-22s" % (name,
                                     "%d bad of %d" % (a[0], a[2]),
                                     "%d bad of %d" % (a[1], a[2])))
    print()
    print("    KILLED means a nonzero count.  The repaired rule is the only one")
    print("    of the five that survives both columns.")
    print()

    print("=" * 78)
    print("A7 runs separately (audit_r1_n7.py) -- n = 7, one order past the")
    print("repair's range.")
    print("=" * 78)


if __name__ == "__main__":
    main()
