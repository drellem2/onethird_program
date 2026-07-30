"""mg-f1b2 -- INDEPENDENT AUDIT of mg-8a12 (8fc5111), the NEGATIVE CONTROL 4
scoring repair.

The question this file answers is the one mg-8a12 was created to answer about
mg-2789, asked of mg-8a12's own new rows: CAN THIS ROW FAIL?

mg-8a12 removed absorbability from rows I1/I2/I3 because the answer is forced by
arithmetic, and put three things in its place:

  (N1) a scored BASELINE row  -- claim (1) holds on the uncorrupted build, 86/86
  (N2) a scored CAUSATION half of each of I1/I2/I3 -- residual == prediction
  (N3) a scored ROUTING CHECK -- "the forced/measured split SEPARATES"
  (N4) a [CANNOT FAIL] row carrying the removed property

and kept absorbability scored in row I4 on the stated ground that "the diagonal
is preserved on 3 of them, so the predicate had to decide on the off-diagonal
signs and could have returned absorbable".

Nothing here imports controls.py: the counts are rebuilt from face_complex so
that a defect in the repair's own bookkeeping cannot hide.
"""

import sys

sys.path.insert(0, "../face_geometry")

from face_complex import (                                     # noqa: E402
    boundary_matrix, linear_extensions, perm_sign, top_laplacians, at_laplacian,
    absorbable_by_diagonal_twist, not_isospectral, mat_eq,
)
from posets import all_posets                                  # noqa: E402

MUTS = [("I1", "ridge_facets"), ("I2", "split_free_as_interior"),
        ("I3", "ridge_drop"), ("I4", "facet_offbyone")]
LOCALISED = {"I1", "I2", "I3"}


def twisted(P, incidence_mode="true"):
    td = top_laplacians(P, incidence_mode=incidence_mode)
    s = [perm_sign(w) for w in td["les"]]
    L = td["L_rel"]
    m = len(s)
    return [[s[i] * L[i][j] * s[j] for j in range(m)] for i in range(m)], L


def target_of(P):
    return at_laplacian(P)[1]


def why_not_absorbable(A, B):
    """Reproduce absorbable_by_diagonal_twist's decision and report WHICH gate
    decided it.  The predicate has three early-exit gates before the parity
    system: dimension, DIAGONAL, and off-diagonal ABSOLUTE VALUE.  Only a
    decision reached in the parity system is a decision about signs.
    """
    m = len(A)
    if m != len(B):
        return "shape"
    if any(A[i][i] != B[i][i] for i in range(m)):
        return "diagonal"
    if any(abs(A[i][j]) != abs(B[i][j]) for i in range(m) for j in range(m)):
        return "magnitude"
    return "signs (parity system)" if not absorbable_by_diagonal_twist(A, B) \
        else "absorbable"


def is_antichain(P):
    return not P.less


def predicted_delta(P, mode):
    """mg-8a12's predicted_incidence_delta, re-derived here from the true build
    only, to check the prediction independently of controls.py."""
    r = top_laplacians(P, incidence_mode=mode)["mutated_ridge"]
    if r is None:
        return None
    td = top_laplacians(P)
    M, _, nc = boundary_matrix(td["facets"], td["ridges"])
    row = M.get(r, {})

    def outer(vec, sgn=1):
        D = [[0] * nc for _ in range(nc)]
        for a, va in vec.items():
            for b, vb in vec.items():
                D[a][b] += sgn * va * vb
        return D

    if mode == "split_free_as_interior":
        return outer(row)
    if mode == "ridge_drop":
        return outer(row, -1)
    if mode == "ridge_facets":
        j1, j2 = sorted(row.keys())
        j3 = next(j for j in range(nc) if j not in (j1, j2))
        g, l = outer({j1: row[j1], j3: row[j2]}), outer(row, -1)
        return [[g[i][j] + l[i][j] for j in range(nc)] for i in range(nc)]
    return None


def sweep(nmax, verbose=True):
    ps = [P for n in range(2, nmax + 1) for P in all_posets(n)]
    rows = {}
    for tag, mode in MUTS:
        app = diag_pres = absorb = spec = caused = 0
        gates, pres_posets = {}, []
        for P in ps:
            Lt, Lt_raw = twisted(P)
            target = target_of(P)
            Lm, Lm_raw = twisted(P, mode)
            if mat_eq(Lm, Lt):
                continue                                  # vacuous
            app += 1
            m = len(Lt)
            if len(Lm) != m:
                gates["shape"] = gates.get("shape", 0) + 1
                continue
            if all(Lm[i][i] == target[i][i] for i in range(m)):
                diag_pres += 1
                pres_posets.append(P)
            g = why_not_absorbable(Lm, target)
            gates[g] = gates.get(g, 0) + 1
            if absorbable_by_diagonal_twist(Lm, target):
                absorb += 1
            if not_isospectral(Lm, Lt):
                spec += 1
            if tag in LOCALISED:
                d = predicted_delta(P, mode)
                s = [perm_sign(w) for w in linear_extensions(P)]
                pred = [[s[i] * d[i][j] * s[j] for j in range(m)] for i in range(m)]
                obs = [[Lm[i][j] - target[i][j] for j in range(m)] for i in range(m)]
                caused += mat_eq(pred, obs) and any(v for r_ in pred for v in r_)
        rows[tag] = dict(app=app, diag_preserved=diag_pres, absorb=absorb,
                         spec=spec, caused=caused, gates=gates,
                         pres_antichain=sum(1 for P in pres_posets if is_antichain(P)),
                         pres_sizes=sorted(len(linear_extensions(P)) for P in pres_posets))
        if verbose:
            print("  %s app=%-3d diag_preserved=%-2d (antichains %d, |L(P)| %s) "
                  "absorb=%d spec=%d caused=%s"
                  % (tag, app, diag_pres, rows[tag]["pres_antichain"],
                     rows[tag]["pres_sizes"], absorb, spec,
                     caused if tag in LOCALISED else "-"))
            print("       gate that decided 'not absorbable': %s" % rows[tag]["gates"])
    forced = [t for t, r in rows.items() if r["diag_preserved"] == 0]
    if verbose:
        print("  forced rows (diag_preserved == 0): %s   routing condition "
              "0 < %d < 4 -> %s" % (forced, len(forced), 0 < len(forced) < 4))
    return rows, forced, len(ps)


def main():
    print("=" * 78)
    print("mg-f1b2 AUDIT OF mg-8a12 -- can the repair's own new rows fail?")
    print("=" * 78)

    print("\nA. THE COMMITTED POPULATION (n <= 5, 86 posets): rebuild of every "
          "count mg-8a12 prints, plus the gate that actually decided each "
          "'not absorbable'.")
    rows5, forced5, N5 = sweep(5)

    print("\nB. IS THE ROUTING CHECK'S ANSWER FORCED?  It is scored [PASS] on "
          "'0 < len(forced_rows) < len(muts)'.  Run the split at every n it can "
          "be run at:")
    for nm in (2, 3, 4, 5, 6):
        rows, forced, N = sweep(nm, verbose=False)
        print("  n <= %d (%3d posets): diag_preserved = %s ; forced = %s ; "
              "0 < %d < 4 -> %s"
              % (nm, N, {t: rows[t]["diag_preserved"] for t, _ in MUTS},
                 forced, len(forced), 0 < len(forced) < 4))

    print("\nC. ROW I4's STATED GROUND FOR KEEPING ABSORBABILITY SCORED: 'the "
          "diagonal is preserved on 3 of them, so the predicate had to decide "
          "on the off-diagonal signs and could have returned absorbable'.  On "
          "those 3 posets, which gate decided it?")
    ps = [P for n in range(2, 6) for P in all_posets(n)]
    for P in ps:
        Lt, _ = twisted(P)
        target = target_of(P)
        Lm, _ = twisted(P, "facet_offbyone")
        if mat_eq(Lm, Lt) or len(Lm) != len(Lt):
            continue
        m = len(Lt)
        if not all(Lm[i][i] == target[i][i] for i in range(m)):
            continue
        nmis = sum(1 for i in range(m) for j in range(m)
                   if abs(Lm[i][j]) != abs(target[i][j]))
        nsign = sum(1 for i in range(m) for j in range(m)
                    if abs(Lm[i][j]) == abs(target[i][j]) and Lm[i][j] != target[i][j])
        print("  n=%d %-22s |L(P)|=%-3d antichain=%-5s gate=%-22s "
              "off-diagonal MAGNITUDE mismatches=%d  sign-only mismatches=%d  "
              "spectrum moved=%s"
              % (P.n, P.name if hasattr(P, "name") else "", m, is_antichain(P),
                 why_not_absorbable(Lm, target), nmis, nsign,
                 not_isospectral(Lm, Lt)))

    print("\nD. IS THE CAUSATION CONDITION (residual == prediction) EQUIVALENT "
          "TO CLAIM (1) ON THE UNCORRUPTED BUILD?  pred = twist(delta) and "
          "obs = twist(L_mut) - target, so pred == obs iff twist(L_true) == "
          "target AND L_mut - L_true == delta.  Check the second conjunct "
          "separately -- if it is an identity, the scored condition is claim (1) "
          "again:")
    for tag, mode in MUTS:
        if tag not in LOCALISED:
            continue
        ident = app = 0
        for P in ps:
            Lt, Lt_raw = twisted(P)
            Lm, Lm_raw = twisted(P, mode)
            if mat_eq(Lm, Lt) or len(Lm) != len(Lt):
                continue
            app += 1
            d = predicted_delta(P, mode)
            m = len(Lt_raw)
            ident += mat_eq([[Lm_raw[i][j] - Lt_raw[i][j] for j in range(m)]
                             for i in range(m)], d)
        print("  %s: L_mut - L_true == predicted delta on %d/%d biting posets "
              "(UNTWISTED, so claim (1) is not involved)" % (tag, ident, app))

    print("\nE. THE BASELINE ROW: is 'claim (1) holds on the uncorrupted build, "
          "86/86' new to this battery?")
    same = 0
    for P in ps:
        Lt, _ = twisted(P)
        same += mat_eq(Lt, target_of(P))
    print("  claim (1) on the true build: %d/%d.  NEGATIVE CONTROL 3 line 1 "
          "prints the same computation ('true simplicial signs: claim (1) holds "
          "on 86/86'), and the probe's own headline is that claim (1) is PROVEN "
          "for every finite poset (mg-276d, audit-confirmed mg-e0ce)." % (same, len(ps)))


if __name__ == "__main__":
    main()
