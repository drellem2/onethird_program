"""Independent check of A6 (the claim mg-1319 upgraded from '86/86' to 'a THEOREM').

Claim: the simplicial sign of an incidence depends only on the RIDGE, so
       d_true = diag(row signs) . d_allplus
and a row rescaling cannot be seen by d^T d -- hence both top Laplacians are
unchanged, for every finite poset.

I check the FACTORISATION entrywise (not the Laplacian equality, which is the
weaker consequence), plus the two side conditions the argument needs and does
not state:
  (S1) no entry of d_true cancels to 0 (else the support differs and the
       'row rescaling' has a zero row where allplus does not);
  (S2) the interior/free ridge classification is sign_mode-independent, since
       L^rel drops rows and a rescaling only commutes with a FIXED row set.
"""
import sys
sys.path.insert(0, "../face_geometry")
from posets import all_posets
from face_complex import (Poset, linear_extensions, le_to_facet,
                          boundary_matrix, top_laplacians, mat_eq)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6

tot = fact_ok = s1_ok = s2_ok = lrel_ok = labs_ok = 0
worst = []
for n in range(1, NMAX + 1):
    for P in all_posets(n):
        les = linear_extensions(P)
        facets = [le_to_facet(w) for w in les]
        ridge_set = set()
        for f in facets:
            for i in range(len(f)):
                ridge_set.add(f[:i] + f[i + 1:])
        ridges = sorted(ridge_set)
        Mt, nr, nc = boundary_matrix(facets, ridges, sign_mode="true")
        Mp, _, _ = boundary_matrix(facets, ridges, sign_mode="allplus")
        tot += 1

        # (S1) no cancellation anywhere
        s1 = all(v != 0 for row in Mt.values() for v in row.values()) and \
             all(v != 0 for row in Mp.values() for v in row.values())
        s1_ok += s1

        # factorisation: one sign per ROW reproduces d_true from d_allplus
        ok = True
        for r in range(nr):
            rt, rp = Mt.get(r, {}), Mp.get(r, {})
            if set(rt) != set(rp):
                ok = False; break
            sgns = {rt[j] // rp[j] for j in rt}          # rp[j] is always +1
            if len(sgns) > 1:                             # sign not fixed by ridge
                ok = False
                worst.append((n, P, r, sorted(sgns)))
                break
        fact_ok += ok

        # (S2) interior/free classification identical under both modes
        cls_t = {r: len(Mt.get(r, {})) for r in range(nr)}
        cls_p = {r: len(Mp.get(r, {})) for r in range(nr)}
        s2_ok += (cls_t == cls_p)

        tdt, tdp = top_laplacians(P), top_laplacians(P, sign_mode="allplus")
        lrel_ok += mat_eq(tdt["L_rel"], tdp["L_rel"])
        labs_ok += mat_eq(tdt["L_abs"], tdp["L_abs"])

print("population: all posets (labelled) with n <= %d  ->  %d posets" % (NMAX, tot))
print("  factorisation d_true = diag(row signs) . d_allplus : %d/%d" % (fact_ok, tot))
print("  (S1) no incidence cancels to zero                  : %d/%d" % (s1_ok, tot))
print("  (S2) interior/free row set is sign_mode-independent: %d/%d" % (s2_ok, tot))
print("  L^rel unchanged                                    : %d/%d" % (lrel_ok, tot))
print("  L^abs unchanged                                    : %d/%d" % (labs_ok, tot))
if worst:
    print("  COUNTEREXAMPLES:", worst[:5])
print()
print("VERDICT:", "A6 theorem CONFIRMED on this population"
      if fact_ok == s1_ok == s2_ok == lrel_ok == labs_ok == tot else "A6 BROKEN")
