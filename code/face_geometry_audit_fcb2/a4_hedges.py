"""mg-fcb2 A4 -- WHAT IS INSIDE EVERY REMAINDER THE REPAIR WRITES.

The ticket's third heading: *enumerate what is inside every "no claim is made
either way" remainder the repair writes.  The parent's hedge covered exactly the
cases that falsified the sentence it was attached to.  A hedge is not
automatically honest.*

mg-e35b exists partly because that was true of its predecessor: the sentence
*"THIS FILE makes no claim either way on the remainder"* covered exactly the nine
pairs where the answer was known and adverse.  The repair withdrew it.  What it
wrote in its place contains four narrower remainders, and each one is opened
here and its contents listed.

  A4.1  "no answer in this row rests on the bound"            (P5a)
  A4.2  the two shape-guard clauses, disclosed as NOT COVERED (P5b)
  A4.3  "on the remaining 25 the pipeline does not see it"    (P5c)
  A4.4  the withdrawn hedge is gone AS AN ASSERTION           (P5d)
  A4.5  "the spectral invariants still do not separate those pairs"

PREDICTED EXIT: 0 -- P5 predicts every hedge's disclosure is accurate.
"""

import os
import shutil
import subprocess
import sys
import tempfile

import lib_fcb2 as L

fc, po = L.import_face_geometry()
sys.path.insert(0, L.FACE_GEOMETRY)
import controls                                                  # noqa: E402
from controls import (claim1_pair, gauge_candidate_perms,        # noqa: E402
                      mutated_facet_set_differs, mutation_applied_at_site,
                      signed_permutation_witness)
from face_complex import (linear_extensions, mat_eq,             # noqa: E402
                          not_isospectral, top_laplacians)
from posets import all_posets                                    # noqa: E402

MODES = [("I1", "ridge_facets"), ("I2", "split_free_as_interior"),
         ("I3", "ridge_drop"), ("I4", "facet_offbyone")]

GUARD = ("    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):\n"
         "        return None\n")


def deletion_test():
    """Delete each clause of the witness's shape guard, one at a time, and see
    whether `controls_output.txt` moves a single byte.

    The baseline is REGENERATED on the unmodified copy rather than taken from the
    committed transcript.  A committed artifact is a measurement at the commit
    that made it, and this repository has already been caught once treating one
    as a live property; comparing a fresh deletion against a stale baseline would
    charge arc-wide drift to the deletion.
    """
    results = []
    tmp = tempfile.mkdtemp(prefix="fcb2_del_")
    try:
        tree = os.path.join(tmp, "face_geometry")
        shutil.copytree(L.FACE_GEOMETRY, tree)
        cpath = os.path.join(tree, "controls.py")
        pristine = open(cpath).read()
        assert GUARD in pristine, "the shape guard's text moved"

        def build(label, src):
            open(cpath, "w").write(src)
            r = subprocess.run([sys.executable, "controls.py", "5"],
                               capture_output=True, text=True, cwd=tree)
            return label, r.stdout, r.returncode

        _, baseline, base_rc = build("baseline", pristine)
        variants = [
            ("clause 1 -- `m != len(B)` deleted",
             pristine.replace(GUARD,
                              "    if any(len(A[i]) != len(B[i]) "
                              "for i in range(m)):\n        return None\n")),
            ("clause 2 -- the ragged-row check deleted",
             pristine.replace(GUARD,
                              "    if m != len(B):\n        return None\n")),
            ("both clauses -- the whole guard deleted",
             pristine.replace(GUARD, "")),
        ]
        for label, src in variants:
            assert src != pristine, "deletion %r changed nothing in the source" % label
            _, out, rc = build(label, src)
            results.append((label, out == baseline, rc, base_rc))
        committed = open(os.path.join(L.FACE_GEOMETRY,
                                      "controls_output.txt")).read()
        return results, baseline == committed
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print("== mg-fcb2 A4: every remainder the repair writes, opened ==")
    print()
    ps = [P for n in range(2, 6) for P in all_posets(n)]
    art = open(os.path.join(L.FACE_GEOMETRY, "controls_output.txt")).read()

    # ---- A4.1 -------------------------------------------------------------
    print("A4.1 -- 'here every not-gauge pair is settled by the spectral proof "
          "instead, so no answer in this row rests on the bound'")
    print("    The bound is real: `signed_permutation_witness`'s NEGATIVE answer "
          "says no permutation IN THE CANDIDATE LIST works, not that none "
          "exists.  The row's claim is that no answer it prints depends on that. "
          "Every not-gauge pair is opened and asked which route settled it.")
    on_bound, by_proof, total = [], 0, 0
    for tag, mode in MODES:
        for P in ps:
            L_true, _ = claim1_pair(P)
            L_mut, _ = claim1_pair(P, incidence_mode=mode)
            if mat_eq(L_mut, L_true):
                continue
            is_gauge = signed_permutation_witness(
                L_true, L_mut, gauge_candidate_perms(P, mode)) is not None
            if is_gauge:
                continue
            total += 1
            if not_isospectral(L_mut, L_true):
                by_proof += 1
            else:
                on_bound.append((tag, len(L_true)))
    print("    %d not-gauge pairs; %d settled by a spectral PROOF, %d resting on "
          "the candidate list" % (total, by_proof, len(on_bound)))
    for t, m in on_bound[:10]:
        print("      resting on the bound: %s, |L(P)| = %d" % (t, m))
    L.check("A4.1a no not-gauge answer in the dichotomy row rests on the "
            "candidate-list bound (%d of %d rest on it)" % (len(on_bound), total),
            not on_bound and total > 0)
    L.predicted("P5a", not on_bound and total == 288,
                "0 of the %d not-gauge answers rest on the bound (predicted 0 of "
                "288)" % total)
    print()

    # ---- A4.2 -------------------------------------------------------------
    print("A4.2 -- the two clauses of the witness's shape guard, disclosed as "
          "NOT COVERED")
    print("    The repair's own words: 'deletion establishes nothing about them, "
          "because no call site in this battery passes matrices of different "
          "order or a ragged one'.  That is a claim about what deleting them "
          "does, and it is run here rather than taken.")
    results, base_matches_committed = deletion_test()
    for label, identical, rc, base_rc in results:
        print("    %-44s artifact byte-identical: %-5s (exit %d vs baseline %d)"
              % (label, identical, rc, base_rc))
    all_identical = all(r[1] for r in results)
    L.check("A4.2a deleting either clause of the shape guard leaves "
            "controls_output.txt byte-identical, i.e. the NOT COVERED "
            "disclosure is accurate", all_identical)
    L.predicted("P5b", all_identical,
                "both deletions leave the artifact byte-identical (%d of %d "
                "variants identical)" % (sum(1 for r in results if r[1]),
                                         len(results)))
    print("    (the freshly regenerated baseline is byte-identical to the "
          "COMMITTED controls_output.txt: %s -- reported because a committed "
          "transcript is a measurement at its own commit, not a live property)"
          % base_matches_committed)
    print()

    # ---- A4.3 -------------------------------------------------------------
    print("A4.3 -- 'on the remaining 25 the pipeline does not see the corruption "
          "at all': what is IN those 25")
    blind, set_differs, order_only = 0, 0, []
    for P in ps:
        L_true, _ = claim1_pair(P)
        L_mut, _ = claim1_pair(P, incidence_mode="facet_offbyone")
        if not mat_eq(L_mut, L_true):
            continue                                     # not vacuous
        if not mutation_applied_at_site(P, "facet_offbyone"):
            continue                                     # did not apply
        blind += 1
        if mutated_facet_set_differs(P, "facet_offbyone"):
            set_differs += 1
        else:
            order_only.append(P)
    print("    %d vacuous-but-applied posets; on %d the facet SET itself differs, "
          "leaving %d where the mutation applied, PRESERVED the facet multiset, "
          "and left L^rel fixed" % (blind, set_differs, len(order_only)))
    for P in order_only:
        td = top_laplacians(P)
        tdm = top_laplacians(P, incidence_mode="facet_offbyone")
        print("      |L(P)| = %d, n = %d, covers %s -- true facets %s, mutated "
              "facets %s (same multiset, different order)"
              % (len(linear_extensions(P)), P.n, po.cover_string(P),
                 td["facets"], tdm["facets"]))
    small = all(len(linear_extensions(P)) <= 2 for P in order_only)
    L.check("A4.3a the remainder is fully enumerated: blind = "
            "facet-set-differs + relabelling-only (%d = %d + %d)"
            % (blind, set_differs, len(order_only)),
            blind == set_differs + len(order_only) and blind == 25)
    L.predicted("P5c", len(order_only) == 1 and small,
                "exactly 1 poset where the mutation applied, preserved the facet "
                "multiset and left L^rel fixed, with |L(P)| <= 2 (found %d, "
                "|L(P)| <= 2: %s)" % (len(order_only), small))
    print("    THIS IS A RELABELLING-SHAPED BLINDNESS AND NO LINE NAMES IT.  The "
          "artifact splits the 25 into 'facet SET differs' (24) and the rest, and "
          "prints the 24; the 1 left over is a poset where the corrupted "
          "enumeration is the true one PERMUTED -- the same gauge the whole "
          "section is about, occurring inside the vacuity remainder rather than "
          "inside the biting population.  It is not adverse to any sentence the "
          "repair writes, and it is not written down either.")
    print()

    # ---- A4.4 -------------------------------------------------------------
    print("A4.4 -- the withdrawn hedge")
    asserted = "THIS FILE makes no claim either way on the remainder" in art
    quoted = "'no claim is made either way on the remainder'" in art
    stated = "WHAT IS IN THE REMAINDER IS NOW STATED" in art
    print("    the old sentence AS AN ASSERTION: %s" % asserted)
    print("    the old wording surviving as a QUOTATION inside its own "
          "withdrawal: %s" % quoted)
    print("    the replacement present: %s" % stated)
    L.check("A4.4a 'no claim is made either way' no longer appears as an "
            "assertion anywhere in the artifact", not asserted)
    L.predicted("P5d", not asserted and stated,
                "the hedge is gone as an assertion and survives only inside the "
                "sentence that withdraws it")
    print()

    # ---- A4.5 -------------------------------------------------------------
    print("A4.5 -- 'the spectral invariants used here still do not separate those "
          "pairs -- that limit is real and unchanged'")
    print("    A limit claimed about the nine gauge pairs.  It is not merely that "
          "these five shifts miss them: they are PROVABLY isospectral, because "
          "each is an exhibited signed-permutation conjugate, and this audit's "
          "exact integer characteristic polynomials agree on every one.")
    gauge_pairs = []
    for tag, mode in MODES:
        for P in ps:
            L_true, _ = claim1_pair(P)
            L_mut, _ = claim1_pair(P, incidence_mode=mode)
            if mat_eq(L_mut, L_true):
                continue
            if signed_permutation_witness(
                    L_true, L_mut, gauge_candidate_perms(P, mode)) is None:
                continue
            same_cp = L.charpoly_exact(L_true) == L.charpoly_exact(L_mut)
            gauge_pairs.append((tag, len(L_true), bool(not_isospectral(L_mut, L_true)),
                                same_cp))
    for tag, m, modsep, same in gauge_pairs:
        print("      %-3s |L(P)| = %-4d modular shifts separate: %-5s   exact "
              "charpolys equal: %s" % (tag, m, modsep, same))
    L.check("A4.5a the nine gauge pairs are not merely unseparated by five "
            "modular shifts, they are EXACTLY isospectral -- so the stated limit "
            "is a property of the pairs and not of the instrument",
            len(gauge_pairs) == 9
            and all(same and not modsep for _, _, modsep, same in gauge_pairs))
    print()

    return L.finish("a4_hedges")


if __name__ == "__main__":
    sys.exit(main())
