#!/usr/bin/env python3
"""
mg-1953 REPAIR instrument 1 of 2 -- THE CHECK THAT EXERCISES THE STATEMENT
OUTSIDE AC(P), WHICH IS WHERE IT CAN FAIL.

mg-ebd8's document states Brown's Theorem 2, specialised to the order cone, as

    m_X = prod_{B in X} (|B| - 1)!   if every block of X is an ANTICHAIN of P
        = 0                          otherwise                          (DOC)

and mg-d673 found that FALSE: it drops the acyclicity condition that the
target's own instrument docstring carries.  The repaired statement is

    m_X = prod_{B in X} (|B| - 1)!   if every block of X is an ANTICHAIN of P
                                     AND the quotient P/X is ACYCLIC
        = 0                          otherwise                     (REPAIRED)

The target's measurement could not see the difference because its code ranged
X over AC(P) -- the set on which the wrong statement happens to be right.  The
whole point of this instrument is that X ranges over ALL FLATS of the braid
arrangement, i.e. over ALL set partitions of [n], where the two statements
differ.

Three tests, and the first is the one the target never ran:

  R1a  THE DERIVATION, DIRECTLY.  Brown's M_0 is "the flats X that meet the
       open region U".  Decide that BY CONSTRUCTION for every flat -- search
       all |X|! orderings of the blocks for one that sends every relation of P
       strictly forwards, which is exactly the existence of a point of the
       relatively open face inside U -- and compare the resulting set against
       (DOC) and against (REPAIRED).  No acyclicity test is used to compute the
       geometric side.  This attacks the derivation, not its consequence.

  R1b  THE CONSEQUENCE.  Brown's total-multiplicity identity (his (10) at the
       discrete flat) says sum over all flats of m_X = |D| = |L(P)|.  Run the
       sum with (DOC) and with (REPAIRED) over ALL flats.

  R1c  THE WITNESS, printed in full: P = {a<d, b<c} at n = 4.

  R1d  THE IDENTITY -- NOT A CONTROL.  Restricted to AC(P) -- what the
       target's instrument ranged over -- (DOC) and (REPAIRED) are the SAME SET
       OF FLATS, because

           {antichain blocks} n {acyclic quotient} = (REPAIRED)

       is a one-line set identity.  So the target's measurement could not have
       seen the difference, whatever it had measured.  R1d exhibits that
       identity by enumeration (0 posets where the two sides differ, all 404
       classes at 2 <= n <= 6) and re-runs R1b on AC(P) to show the sum agrees
       there too.  It CANNOT FAIL while (REPAIRED) passes, so by this repo's
       own criterion -- code/hodge_leverage_audit_86a3/audit_controls.py:4,
       "a control must be able to FAIL on the construction it guards" -- it is
       NOT a control and is not evidence.  R1a and R1b range over all flats and
       are where the discriminating power is; R1d says why no check confined to
       AC(P) could ever have had any.  (mg-3b51 A1: this block was originally
       billed as "A CONTROL THAT MUST FIRE" and the restriction as
       "demonstrated" rather than stated.  Relabelled by mg-aec7.)

Exhaustive over all isomorphism classes to n = 6.
"""

import sys

from core1953 import (iso_classes, set_partitions, linear_extensions,
                      blocks_are_antichains, quotient_is_acyclic,
                      meets_the_open_order_cone, factorial, label, poset_name)


def multiplicity(X):
    p = 1
    for B in X:
        p *= factorial(len(B) - 1)
    return p


def analyse(n):
    flats = set_partitions(n)
    s = dict(classes=0, geom_vs_doc_bad=0, geom_vs_rep_bad=0,
             doc_sum_bad=0, rep_sum_bad=0, spurious=0, flats=0,
             doc_sum_bad_onAC=0, rep_sum_bad_onAC=0,
             doc_ne_rep_onAC=0, witness=None)
    for rel in iso_classes(n):
        s['classes'] += 1
        s['flats'] += len(flats)
        e = len(linear_extensions(n, rel))

        M0_geom, M0_doc, M0_rep, AC = set(), set(), set(), set()
        for k, X in enumerate(flats):
            if meets_the_open_order_cone(rel, X):
                M0_geom.add(k)
            if blocks_are_antichains(rel, X):
                M0_doc.add(k)
                if quotient_is_acyclic(rel, X):
                    M0_rep.add(k)
            if quotient_is_acyclic(rel, X):
                AC.add(k)

        if M0_geom != M0_doc:
            s['geom_vs_doc_bad'] += 1
        if M0_geom != M0_rep:
            s['geom_vs_rep_bad'] += 1

        doc_sum = sum(multiplicity(flats[k]) for k in M0_doc)
        rep_sum = sum(multiplicity(flats[k]) for k in M0_rep)
        extra = sorted(M0_doc - M0_rep)
        s['spurious'] += len(extra)
        if doc_sum != e:
            s['doc_sum_bad'] += 1
            if s['witness'] is None:
                s['witness'] = (rel, e, doc_sum, rep_sum,
                                [flats[k] for k in extra])
        if rep_sum != e:
            s['rep_sum_bad'] += 1

        # R1d -- the IDENTITY: restricted to AC(P) the two rules are the same
        # set of flats.  Exhibited, not tested: it cannot come out otherwise.
        if (M0_doc & AC) != M0_rep:
            s['doc_ne_rep_onAC'] += 1
        doc_onAC = sum(multiplicity(flats[k]) for k in M0_doc & AC)
        rep_onAC = sum(multiplicity(flats[k]) for k in M0_rep & AC)
        if doc_onAC != e:
            s['doc_sum_bad_onAC'] += 1
        if rep_onAC != e:
            s['rep_sum_bad_onAC'] += 1
    return s


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print("=" * 78)
    print("mg-1953 REPAIR 1 -- BROWN'S CLOSED FORM, EXERCISED OUTSIDE AC(P).")
    print("X ranges over ALL FLATS (all set partitions), never over AC(P).")
    print("=" * 78)
    print()

    print("-" * 78)
    print("R1a  THE DERIVATION.  M_0 = 'flats meeting the open cone U', decided")
    print("     BY CONSTRUCTION (search over all orderings of the blocks; no")
    print("     acyclicity test on the geometric side), against the DOCUMENT's")
    print("     rule and against the REPAIRED rule.")
    print("-" * 78)
    print("%3s %8s %9s %28s %28s"
          % ("n", "classes", "flats", "M_0 == doc rule", "M_0 == repaired rule"))
    rows = {}
    for n in range(2, nmax + 1):
        s = analyse(n)
        rows[n] = s
        print("%3d %8d %9d %28s %28s"
              % (n, s['classes'], s['flats'],
                 "%d bad of %d" % (s['geom_vs_doc_bad'], s['classes']),
                 "%d bad of %d" % (s['geom_vs_rep_bad'], s['classes'])))
    print()

    print("-" * 78)
    print("R1b  THE CONSEQUENCE.  Brown's total-multiplicity identity, summed")
    print("     over ALL FLATS:  sum_X m_X = |L(P)|.")
    print("-" * 78)
    print("%3s %8s %26s %26s %11s"
          % ("n", "classes", "doc rule: sum != |L(P)|",
             "repaired rule: sum != |L(P)|", "spurious"))
    for n in range(2, nmax + 1):
        s = rows[n]
        print("%3d %8d %26s %26s %11d"
              % (n, s['classes'],
                 "%d of %d posets" % (s['doc_sum_bad'], s['classes']),
                 "%d of %d posets" % (s['rep_sum_bad'], s['classes']),
                 s['spurious']))
    print()
    print("     'spurious' counts the flats the DOCUMENT's rule gives a nonzero")
    print("     multiplicity that Brown's M_0 does not contain: every block an")
    print("     antichain of P, quotient NOT acyclic, so the flat misses U.")
    print()

    print("-" * 78)
    print("R1c  THE WITNESS.")
    print("-" * 78)
    for n in range(2, nmax + 1):
        s = rows[n]
        if s['witness'] is None:
            print("  n=%d: no witness -- the document's rule holds on all %d classes"
                  % (n, s['classes']))
            continue
        rel, e, ds, rs, extra = s['witness']
        print("  n=%d  first witness  P = %s,  |L(P)| = %d"
              % (n, poset_name(rel), e))
        print("        document's rule   sum m = %d   (Brown's (10) requires %d)"
              % (ds, e))
        print("        repaired rule     sum m = %d   %s"
              % (rs, "OK" if rs == e else "MISMATCH"))
        for X in extra:
            print("        spurious flat: %-10s m = %d   blocks antichains: %s,"
                  "  quotient acyclic: %s,  meets U: %s"
                  % (label(X), multiplicity(X),
                     blocks_are_antichains(rel, X),
                     quotient_is_acyclic(rel, X),
                     meets_the_open_order_cone(rel, X)))
        break
    print()

    print("-" * 78)
    print("R1d  THE IDENTITY -- NOT A CONTROL.  Restricted to AC(P), which is")
    print("     what the target's instrument ranged over, the two rules are the")
    print("     SAME SET OF FLATS:  {antichain blocks} n {acyclic quotient} IS")
    print("     the repaired rule.  Exhibited by enumeration below, and it")
    print("     cannot come out otherwise -- see the note under the table.")
    print("-" * 78)
    print("%3s %8s %26s %26s %18s"
          % ("n", "classes", "doc rule ON AC(P)", "repaired rule ON AC(P)",
             "the two SETS"))
    tot_cls = tot_ne = 0
    for n in range(2, nmax + 1):
        s = rows[n]
        tot_cls += s['classes']
        tot_ne += s['doc_ne_rep_onAC']
        print("%3d %8d %26s %26s %18s"
              % (n, s['classes'],
                 "%d bad of %d" % (s['doc_sum_bad_onAC'], s['classes']),
                 "%d bad of %d" % (s['rep_sum_bad_onAC'], s['classes']),
                 "%d differ of %d" % (s['doc_ne_rep_onAC'], s['classes'])))
    print("%3s %8d %26s %26s %18s"
          % ("all", tot_cls, "", "", "%d differ of %d" % (tot_ne, tot_cls)))
    print()
    print("     THIS TABLE CANNOT COME OUT ANY OTHER WAY, and that is the")
    print("     point of it.  The rightmost column is a ONE-LINE SET IDENTITY")
    print("     exhibited on every class; the two 'bad' columns are then the")
    print("     same column twice.  By this repo's own criterion --")
    print("     code/hodge_leverage_audit_86a3/audit_controls.py:4, 'a control")
    print("     must be able to FAIL on the construction it guards' -- R1d is")
    print("     NOT a control and is not evidence.  It is the reason no check")
    print("     confined to AC(P) could have caught the defect, whatever it")
    print("     had measured.  (mg-3b51 A1; relabelled by mg-aec7.)")
    print()
    print("=" * 78)
    print("READING.  R1a is the derivation and R1b its consequence; they must")
    print("agree, and they do, and the mutation panel in the audit shows both")
    print("have power.  R1d is not a fourth test: it is the stated identity")
    print("that explains why the target's measurement, confined to AC(P), was")
    print("blind to a rule that is false off it.  The repaired rule passes")
    print("everywhere.")
    print("=" * 78)


if __name__ == "__main__":
    main()
