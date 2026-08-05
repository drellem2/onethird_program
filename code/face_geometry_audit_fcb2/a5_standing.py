"""mg-fcb2 A5 -- DO NOT DISTURB WHAT STANDS.

The ticket's fourth heading, and the one it says outranks every finding above:

    `L_parity = D.L_true.D` 86/86; absorbability vs brute force 306/306;
    `facet_swap01` rejection 72/72; NC3 could not have caught any of the four.
    Re-run and report; a regression here outranks every finding above.

Every number below is RE-DERIVED, not read out of `controls_output.txt`.  Where
the battery has an instrument for a question, this file builds its own and
compares: the point of the heading is that the mathematics is undisturbed, and
reading the transcript back would establish only that the transcript has not
changed.

PREDICTED EXIT: 0 -- P6 predicts no regression.
"""

import os
import subprocess
import sys

import lib_fcb2 as L

fc, po = L.import_face_geometry()
sys.path.insert(0, L.FACE_GEOMETRY)
import controls                                                  # noqa: E402
from controls import (claim1_pair, claim1_test,                  # noqa: E402
                      gauge_candidate_perms, signed_permutation_witness)
from face_complex import (absorbable_by_diagonal_twist,           # noqa: E402
                          linear_extensions, mat_eq, not_isospectral,
                          top_laplacians)
from posets import all_posets                                    # noqa: E402

MODES = [("I1", "ridge_facets"), ("I2", "split_free_as_interior"),
         ("I3", "ridge_drop"), ("I4", "facet_offbyone")]


def main():
    print("== mg-fcb2 A5: do not disturb what stands ==")
    print()
    ps = [P for n in range(2, 6) for P in all_posets(n)]
    N = len(ps)

    # ---- P6a --------------------------------------------------------------
    print("A5.1 -- L_parity = D . L_true . D with D = diag((-1)^j)")
    print("    Built explicitly and compared entry by entry, on every poset -- "
          "not inferred from 'it is absorbable'.")
    ok = 0
    for P in ps:
        L_true, _ = claim1_pair(P)
        L_par, _ = claim1_pair(P, sign_mode="parity")
        m = len(L_true)
        D = [(-1) ** j for j in range(m)]
        rebuilt = [[D[i] * L_true[i][j] * D[j] for j in range(m)] for i in range(m)]
        ok += rebuilt == L_par
    L.check("A5.1a L_parity equals D . L_true . D on %d/%d posets" % (ok, N),
            ok == N and N == 86)
    L.predicted("P6a", ok == N == 86, "L_parity = D.L_true.D on %d/%d "
                "(predicted 86/86)" % (ok, N))
    print()

    # ---- P6b --------------------------------------------------------------
    print("A5.2 -- the absorbability predicate against brute force over all 2^m "
          "sign vectors")
    print("    The population is the one the battery's own instrument row uses: "
          "every (poset, mutation) pair with |L(P)| <= 8, over the six incidence "
          "modes the section builds.  The brute force here is this audit's, "
          "written from the definition.")
    agree = cases = 0
    modes = ["true", "facet_swap01"] + [m for _, m in MODES]
    for P in ps:
        L_true, target = claim1_pair(P)
        m = len(L_true)
        if m > 8:
            continue
        for mode in modes:
            A = claim1_pair(P, incidence_mode=mode)[0]
            brute = False
            for bits in range(1 << m):
                s = [-1 if bits >> i & 1 else 1 for i in range(m)]
                if all(s[i] * A[i][j] * s[j] == target[i][j]
                       for i in range(m) for j in range(m)):
                    brute = True
                    break
            cases += 1
            agree += brute == absorbable_by_diagonal_twist(A, target)
    L.check("A5.2a the union-find absorbability decision agrees with brute force "
            "on %d/%d (poset, mutation) pairs with |L(P)| <= 8" % (agree, cases),
            agree == cases and cases == 306)
    L.predicted("P6b", agree == cases == 306,
                "306/306 agreement (got %d/%d)" % (agree, cases))
    print()

    # ---- P6c --------------------------------------------------------------
    print("A5.3 -- facet_swap01, the candidate this section rejected")
    app = absorb = spec = gauge = nonid = 0
    for P in ps:
        L_true, target = claim1_pair(P)
        L_sw, _ = claim1_pair(P, incidence_mode="facet_swap01")
        if mat_eq(L_sw, L_true):
            continue
        app += 1
        absorb += bool(absorbable_by_diagonal_twist(L_sw, target))
        spec += bool(not_isospectral(L_sw, L_true))
        w = L.signed_perm_witness(L_true, L_sw)          # this audit's own search
        if w not in (None, "BUDGET"):
            assert L.reconstruct(L_true, w[0], w[1]) == L_sw
            gauge += 1
            nonid += w[0] != list(range(len(L_true)))
    print("    bites on %d/%d, absorbable into a diagonal twist on %d/%d, "
          "spectrum provably moves on %d/%d, GAUGE on %d/%d (%d with a "
          "NON-identity permutation)"
          % (app, N, absorb, app, spec, app, gauge, app, nonid))
    L.check("A5.3a facet_swap01 bites on 72/86, is absorbable on 0/72, its "
            "spectrum provably moves on 0/72, and it is GAUGE on 72/72",
            (app, absorb, spec, gauge) == (72, 0, 0, 72) and N == 86)
    L.predicted("P6c", (app, absorb, spec, gauge) == (72, 0, 0, 72),
                "72/86 biting, 0/72 absorbable, 0/72 spectrum moves, 72/72 gauge "
                "(got %d/%d, %d/%d, %d/%d, %d/%d)"
                % (app, N, absorb, app, spec, app, gauge, app))
    print()

    # ---- P6d --------------------------------------------------------------
    print("A5.4 -- NEGATIVE CONTROL 3 could not have caught any of the four")
    print("    mg-5630's line-F experiment, re-run here on this battery's own "
          "mutations: with each incidence corruption in place, do NEGATIVE "
          "CONTROL 3's own scored lines still come out green?  If they do, NC3 "
          "would have passed on a corrupted build -- which is why NEGATIVE "
          "CONTROL 4 exists.")
    bites_true = sum(1 for P in ps if len(linear_extensions(P)) >= 2
                     and not mat_eq(claim1_pair(P, sign_mode="parity")[0],
                                    claim1_pair(P)[0]))
    all_green = True
    for tag, mode in MODES:
        # NC3 line 2: all-+1 signs leave L^rel unchanged (its [CANNOT FAIL] row)
        silent = 0
        for P in ps:
            base = top_laplacians(P, incidence_mode=mode)["L_rel"]
            plus = top_laplacians(P, sign_mode="allplus",
                                  incidence_mode=mode)["L_rel"]
            silent += mat_eq(base, plus)
        # NC3 line 3: the facet-parity row, and its scored condition
        par_app = [P for P in ps if len(linear_extensions(P)) >= 2
                   and not mat_eq(claim1_pair(P, sign_mode="parity",
                                              incidence_mode=mode)[0],
                                  claim1_pair(P, incidence_mode=mode)[0])]
        par_rej = sum(1 for P in par_app
                      if not claim1_test(P, sign_mode="parity",
                                         incidence_mode=mode))
        green = silent == N and par_rej == len(par_app) and len(par_app) > 0
        all_green &= green
        print("    %-3s line 2 all-+1-unchanged %d/%d (%s); line 3 parity bites "
              "on %d (vs %d uncorrupted) and is rejected on %d of them -- scored "
              "condition n_rej == n_app: %s  -> NC3 %s"
              % (tag, silent, N, "SILENT" if silent == N else "differs",
                 len(par_app), bites_true, par_rej,
                 par_rej == len(par_app), "GREEN" if green else "RED"))
    L.check("A5.4a with each of I1-I4 in place NEGATIVE CONTROL 3's lines stay "
            "green, so NC3 could not have caught any of the four", all_green)
    L.predicted("P6d", all_green and bites_true == 82,
                "all four NC3 rows stay green, line 2 SILENT on 86/86, bite "
                "counts against %d uncorrupted (predicted 82)" % bites_true)
    print()

    # ---- P6e --------------------------------------------------------------
    print("A5.5 -- the probe's own runner, unmodified by this audit")
    r = subprocess.run(["sh", "run_all.sh"], cwd=L.FACE_GEOMETRY,
                       capture_output=True, text=True)
    dirty = L.git("status", "--porcelain", "code/face_geometry").strip()
    print("    `code/face_geometry/run_all.sh` exit %d" % r.returncode)
    print("    working tree under code/face_geometry after the run: %s"
          % (dirty if dirty else "clean -- it regenerated its own artifacts "
                                 "byte-identically"))
    L.check("A5.5a face_geometry/run_all.sh still exits 0 on this worktree",
            r.returncode == 0)
    L.check("A5.5b ... and regenerating its artifacts leaves the tree clean, so "
            "nothing this audit did moved the battery's own output", not dirty)
    L.predicted("P6e", r.returncode == 0,
                "run_all.sh exits 0 (got %d)" % r.returncode)
    print()

    return L.finish("a5_standing")


if __name__ == "__main__":
    sys.exit(main())
