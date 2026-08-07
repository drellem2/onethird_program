"""mg-00a1 / s1 -- THE VERDICT.  The disjunctive per-slot value is SUPERLINEAR.

NO LP ANYWHERE IN THIS SCRIPT.  The measure is written down by the construction in
`lib00a1.witness` and every property is re-derived from it by direct `Fraction` arithmetic
through `mg-200d`'s own `measure_report`.  A simplex could not make this wrong and does not
appear.

Usage:  python3 s1_witness.py [max_n]     (default 24; even and odd both covered)
"""

import sys
from fractions import Fraction as F

from lib00a1 import (
    comparable_from_I, eps_spec, expected_descents, is_transitively_closed, staircase_I,
    trivial_dual_bound, verify_measure, witness, witness_target,
)


def main(max_n=24):
    print("=" * 100)
    print("mg-00a1 / s1 -- THE TRUE GROWTH OF THE DISJUNCTIVE PER-SLOT VALUE")
    print("=" * 100)
    print()
    print("THE QUESTION (mg-131e's successor, deliberately unanswered there): is the value")
    print("c*n + O(1), or superlinear?  Below: an EXPLICIT feasible measure on an EXPLICIT")
    print("transitively closed branch, at every n, with E[inv] = n(n+5)/36.  QUADRATIC.")
    print()
    print("Every number in this script is computed by direct Fraction arithmetic from the")
    print("measure.  There is no simplex in the path.  mg-131e's asymmetry is KEPT: each row")
    print("is a LOWER bound on a NAMED branch, so the true maximum at that n may be larger.")
    print("A larger maximum leaves a superlinear verdict standing; it would destroy a linear")
    print("one.  That is why the verdict is stated in this direction and not the other.")
    print()

    print("-" * 100)
    print("PART A -- the witness, checked at every n by arithmetic")
    print("-" * 100)
    print()
    hdr = (f"{'n':>4} {'E[inv]':>12} {'n(n+5)/36':>12} {'mass':>5} {'maxflip':>8} "
           f"{'symviol':>8} {'compflip':>9} {'neg':>4} {'atoms':>6} {'|I|':>5} {'eps_spec':>10}  ok")
    print(hdr)
    print("-" * len(hdr))
    rows, failures = [], []
    for n in range(4, max_n + 1):
        I = staircase_I(n)
        mu = witness(n)
        v = verify_measure(n, mu, I)
        tgt = witness_target(n)
        hits = v["E_inv"] == tgt
        ok = v["ok"] and hits
        if not ok:
            failures.append(n)
        rows.append((n, v["E_inv"], len(I)))
        print(f"{n:>4} {str(v['E_inv']):>12} {str(tgt):>12} {str(v['mass']):>5} "
              f"{str(v['max_flip']):>8} {len(v['sym_violations_on_I']):>8} "
              f"{len(v['comparable_pairs_flipped']):>9} {len(v['negative_atoms']):>4} "
              f"{v['atoms']:>6} {len(I):>5} {str(eps_spec(n, v['E_inv'])):>10}  "
              f"{'OK' if ok else '**FAIL**'}")
    print()
    print(f"  {len(rows) - len(failures)} of {len(rows)} n checked and clean"
          f"{'' if not failures else '   FAILURES AT n = ' + str(failures)}")
    print()
    print("  Read the columns: mass is exactly 1, no atom is negative, the largest flip")
    print("  probability is exactly 1/3 (AT the cap, never over), NO incomparable pair has a")
    print("  single per-slot symmetry violation, and NO comparable pair is ever flipped.")
    print("  So the measure is feasible in mg-200d's disjunctive per-slot relaxation on this")
    print("  branch, and E[inv] is therefore a lower bound for that branch's value.")
    print()

    print("-" * 100)
    print("PART B -- the branch is a GENUINE comparability pattern (transitively closed)")
    print("-" * 100)
    print()
    print("mg-200d imposes no transitivity, which is what keeps its value an UPPER bound; a")
    print("witness on a non-transitive branch would be much weaker.  Checked, not asserted:")
    print()
    bad = []
    for n in range(4, max_n + 1):
        C = comparable_from_I(n, staircase_I(n))
        if not is_transitively_closed(n, C):
            bad.append(n)
    print(f"  transitively closed at every n in [4, {max_n}]:  "
          f"{'YES, all ' + str(max_n - 3) if not bad else '**NO** at ' + str(bad)}")
    print()

    print("-" * 100)
    print("PART C -- the growth, read off rather than fitted")
    print("-" * 100)
    print()
    print("The closed form is proved for every even n in the document; the table above is a")
    print("machine check of the proof at each n, not the evidence for it.  Second differences")
    print("in m = n/2 are constant, which is what 'quadratic' means:")
    print()
    ev = [(n, val) for (n, val, _) in rows if n % 2 == 0]
    print(f"    {'n':>4} {'value':>10} {'1st diff':>10} {'2nd diff':>10}")
    for k, (n, val) in enumerate(ev):
        d1 = ev[k][1] - ev[k - 1][1] if k >= 1 else None
        d2 = (ev[k][1] - 2 * ev[k - 1][1] + ev[k - 2][1]) if k >= 2 else None
        print(f"    {n:>4} {str(val):>10} {str(d1) if d1 is not None else '-':>10} "
              f"{str(d2) if d2 is not None else '-':>10}")
    print()
    print("  Constant second difference 2/9 in m.  Leading coefficient 1/9 per m^2, i.e.")
    print("  n^2/36.  This is NOT a fit through the table: the document derives")
    print("  E[inv] = m(2m-1)/18 + m/3 = m(2m+5)/18 = n(n+5)/36 term by term from the")
    print("  construction, and the table is the check.")
    print()

    print("-" * 100)
    print("PART D -- the matching upper bound, so the class is pinned on BOTH sides")
    print("-" * 100)
    print()
    print("mg-131e's H2 (the trivial dual, a theorem at every n): val(C) <= |I_active|/3.")
    print("Since |I_active| <= C(n,2), val(C) <= n(n-1)/6 for EVERY branch at EVERY n.")
    print()
    print(f"    {'n':>4} {'lower (witness)':>16} {'upper n(n-1)/6':>16} {'ratio':>8}")
    for n in range(6, max_n + 1, 2):
        lo = witness_target(n)
        hi = F(n * (n - 1), 6)
        print(f"    {n:>4} {str(lo):>16} {str(hi):>16} {float(lo / hi):>8.4f}")
    print()
    print("  n(n+5)/36  <=  max over branches  <=  n(n-1)/6.")
    print("  BOTH SIDES ARE QUADRATIC.  The growth class is THETA(n^2), settled.")
    print()

    print("-" * 100)
    print("PART E -- why the descent identity was never going to give a linear bound")
    print("-" * 100)
    print()
    print("mg-131e's H6 is a theorem at every n: every descent sits on an incomparable pair,")
    print("per-slot symmetry forces E[des] = E[asc_I], and E[des] + E[asc_I] <= n-1, so")
    print("E[des] <= (n-1)/2.  It bounds DESCENTS, and inv >= des pointwise runs the wrong")
    print("way.  On the witness the two diverge without limit, so the identity is not merely")
    print("insufficient -- it is off by an unbounded factor:")
    print()
    print(f"    {'n':>4} {'E[inv]':>10} {'E[des]':>10} {'(n-1)/2':>9} {'E[inv]/E[des]':>14}  E[des] <= (n-1)/2")
    des_bad = []
    for n in range(6, max_n + 1, 2):
        mu = witness(n)
        ei = witness_target(n)
        ed = expected_descents(n, mu)
        ok = ed <= F(n - 1, 2)
        if not ok:
            des_bad.append(n)
        print(f"    {n:>4} {str(ei):>10} {str(ed):>10} {str(F(n - 1, 2)):>9} "
              f"{float(ei / ed):>14.4f}  {'OK' if ok else '**VIOLATED**'}")
    print()
    print("  E[des] obeys its bound at every n -- as it must, it is a theorem -- while the")
    print("  ratio grows.  Bounding descents can never bound inversions here.")
    print()

    print("=" * 100)
    print("VERDICT")
    print("=" * 100)
    print()
    print("  The disjunctive per-slot value is SUPERLINEAR -- Theta(n^2), not c*n + O(1).")
    print()
    print("  So the ticket's second branch is the one that fires: DANIEL'S ROUTE IS DEAD,")
    print("  not merely re-based.  There is no constant c to put in place of 1/3, because")
    print("  the per-slot value does not have the form c*n + O(1) at all.")
    print()
    print("  And a second result, which mg-131e explicitly left standing: mg-200d's")
    print("  Theta(n^2) -> Theta(n) headline is REFUTED.  Per-slot adjacency symmetry buys a")
    print("  CONSTANT FACTOR (at most 6: n^2/6 down to at least n^2/36), not an order.")
    print()
    print("  WHAT THIS DOES NOT TOUCH.  The disjunctive value is an UPPER BOUND on the")
    print("  frozen-poset object.  Showing an upper bound is LARGER than believed weakens")
    print("  the bound and says nothing whatever about the statement underneath.  (LIB) and")
    print("  the frozen-poset conjecture are exactly where mg-131e left them.  What is dead")
    print("  is this route as a wall-breaker.")
    print()
    return 1 if failures or bad or des_bad else 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 24))
