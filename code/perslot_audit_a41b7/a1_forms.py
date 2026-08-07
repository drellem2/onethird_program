"""a1_forms — the three constraint sets, solved independently, exact rationals.

  BASE      max E[inv_e] over probability measures on S_n with every pair flipped
            against e with probability <= 1/3.        (mg-6bc2's LP, the baseline)
  PERSLOT   BASE + J_k(x,y) = J_k(y,x) for EVERY slot k and EVERY unordered pair.
  AGG       BASE + J(x,y)   = J(y,x)   for every unordered pair, J = sum_k J_k.

Each is reported with its STATUS FIRST.  An infeasible system and a system whose
optimum is unimproved are different answers and are printed as different words.
Every "optimal" is verified twice: the primal by substitution, and the dual by
arithmetic, so the <= direction is a certificate rather than a solver claim.

usage: python3 a1_forms.py 3 4 5
"""
import sys
from fractions import Fraction as F
import liba41b7 as L


def solve_and_verify(name, n, P, rows, obj):
    r = L.solve(len(P), rows, obj)
    print("  %-9s status=%s" % (name, r.status), end="")
    if r.status == "infeasible":
        print("   phase-1 residual = %s  (STRICTLY POSITIVE: the polytope is EMPTY)"
              % r.phase1)
        return r
    print("   E[inv] = %s   eps_spec = 6E/(n^2-1) = %s   pivots=%d"
          % (r.value, L.eps_spec(n, r.value), r.pivots))
    pe = L.check_primal(len(P), rows, obj, r.x, r.value)
    de = L.check_dual(len(P), rows, obj, r.y, r.value)
    print("            primal verifies: %s      dual certificate verifies: %s"
          % ("YES" if pe == [] else "NO %s" % pe[:3],
             "YES" if de == [] else "NO %s" % de[:3]))
    atoms = sorted(((P[j], v) for j, v in r.x.items()), key=lambda t: -t[1])
    print("            support %d atom(s):" % len(atoms))
    for s, v in atoms[:12]:
        print("              %s  weight %s   inv=%d" % ("".join(map(str, s)), v, L.inv(s)))
    if len(atoms) > 12:
        print("              ... %d more" % (len(atoms) - 12))
    rep = L.report(n, r.x, P)
    print("            mass=%s   per-slot violations=%d   aggregate violations=%d"
          % (rep["mass"], len(rep["slot_violations"]), len(rep["agg_violations"])))
    return r


def main(ns):
    for n in ns:
        P = L.perms(n)
        obj = L.objective_inv(n, P)
        norm = L.row_normalisation(n, P)
        pb = L.rows_pairbias(n, P)
        ps = L.rows_perslot_symmetry(n, P)
        ag = L.rows_aggregate_symmetry(n, P)
        print("=" * 78)
        print("n = %d   |S_n| = %d   pair rows %d   per-slot rows %d   aggregate rows %d"
              % (n, len(P), len(pb), len(ps), len(ag)))
        print("  baseline target C(n,2)/3 = %s ; per-slot value claimed by mg-200d "
              "in this currency is (n-1)/3 = %s" % (F(n * (n - 1), 6), F(n - 1, 3)))
        solve_and_verify("BASE", n, P, [norm] + pb, obj)
        solve_and_verify("PERSLOT", n, P, [norm] + pb + ps, obj)
        solve_and_verify("AGG", n, P, [norm] + pb + ag, obj)
        # symmetry ALONE, no pair bias: what does each symmetry family force?
        for lbl, sym in (("PERSLOT", ps), ("AGG", ag)):
            r = L.solve(len(P), [norm] + sym, obj)
            print("  %s-only (no pair bias): status=%s  max E[inv]=%s   uniform gives %s"
                  % (lbl, r.status, r.value, F(n * (n - 1), 4)))
            if r.status == "optimal":
                rr = L.solve(len(P), [norm] + sym, obj, maximise=False)
                print("            min E[inv]=%s  -- max == min means the rows PIN E[inv]: %s"
                      % (rr.value, "YES" if rr.value == r.value else "no"))
            # is every pair flip pinned to 1/2?  if so no cap < 1/2 can ever be met
            worst = None
            for i, (c, sense, b) in enumerate(L.rows_pairbias(n, P)):
                lo = L.solve(len(P), [norm] + sym, c, maximise=False)
                hi = L.solve(len(P), [norm] + sym, c, maximise=True)
                lohi = (lo.value, hi.value)
                if worst is None or lohi < worst[1]:
                    worst = (L.pairs(n)[i], lohi)
                if lo.value != hi.value:
                    print("            pair %s flip is NOT pinned: [%s, %s]"
                          % (L.pairs(n)[i], lo.value, hi.value))
            print("            smallest achievable flip over all pairs: pair %s -> [%s, %s]"
                  "   (cap 1/3 needs the low end <= 1/3)"
                  % (worst[0], worst[1][0], worst[1][1]))
        sys.stdout.flush()


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or [3, 4, 5])
