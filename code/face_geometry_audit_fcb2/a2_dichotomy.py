"""mg-fcb2 A2 -- THE GAUGE/NON-SIMILAR DICHOTOMY, RE-DERIVED FROM THE DEFINITION.

The ticket's fourth heading: *do not disturb what stands*.  mg-e35b's central
mathematical claim is the dichotomy 297 = 288 + 9 + 0, and a regression there
outranks every finding in A1.  So it is re-derived here -- not read from the
transcript, and not re-derived the way `verify_e35b.py` re-derives it.

WHY THAT DISTINCTION IS THE POINT.  `verify_e35b.py` calls
`face_complex.not_isospectral` and rebuilds the witness search over
`gauge_candidate_perms`' candidate list.  Those are the two things the section
under audit uses, so a bug in either is invisible to it: *replication is not
corroboration when the copies share a source.*  This file uses

  * EXACT INTEGER characteristic polynomials -- the whole polynomial, lifted over
    Z by CRT under a Hadamard bound -- where the shipped route evaluates
    det(A - k.I) mod (2^31-1) at five fixed shifts, and
  * a backtracking search over ALL of S_m, which takes no candidate list.

The second matters for a reason the shipped row states about itself: its
NOT-GAUGE answers are *bounded by the candidate list*.  A search over all of S_m
is not, so where the two agree the bound is discharged rather than restated.

PREDICTED EXIT: 0 -- P3 predicts the repair's dichotomy is right.
"""

import itertools
import sys

import lib_fcb2 as L

fc, po = L.import_face_geometry()
sys.path.insert(0, L.FACE_GEOMETRY)
import controls                                                  # noqa: E402
from controls import (claim1_pair, gauge_candidate_perms,         # noqa: E402
                      signed_permutation_witness)
from face_complex import linear_extensions, not_isospectral, mat_eq  # noqa: E402
from posets import all_posets                                    # noqa: E402

MODES = [("I1", "ridge_facets"), ("I2", "split_free_as_interior"),
         ("I3", "ridge_drop"), ("I4", "facet_offbyone")]
SWAP = ("swap01", "facet_swap01")

# What mg-e35b's artifact prints, quoted here so that "reproduced exactly" is a
# comparison against a written-down expectation and not against whatever comes
# out.  Per row: (biting, non-similar, gauge).
SHIPPED = {"I1": (72, 66, 6), "I2": (82, 82, 0), "I3": (82, 82, 0),
           "I4": (61, 58, 3), "swap01": (72, 0, 72)}


def main():
    print("== mg-fcb2 A2: the dichotomy, re-derived by exact charpolys and a "
          "search over all of S_m ==")
    print()

    ps = [P for n in range(2, 6) for P in all_posets(n)]
    cp_cache = {}

    def charpoly(M):
        key = tuple(tuple(r) for r in M)
        if key not in cp_cache:
            cp_cache[key] = L.charpoly_exact(M)
        return cp_cache[key]

    rows = {}
    contradictions = []
    budget_hits = []
    witnesses = []
    spectral_disagree = []
    tot = {"app": 0, "nonsim": 0, "gauge": 0, "unclassified": 0}

    print("A2.1 -- every biting pair classified independently")
    for tag, mode in MODES + [SWAP]:
        app = nonsim = gauge = unclassified = 0
        for P in ps:
            L_true, _ = claim1_pair(P)
            L_mut, _ = claim1_pair(P, incidence_mode=mode)
            if mat_eq(L_mut, L_true):
                continue
            app += 1
            # (a) the EXACT spectral question, asked of the whole polynomial
            exact_sep = charpoly(L_true) != charpoly(L_mut)
            # (b) the witness question, asked over ALL of S_m and not a list
            w = L.signed_perm_witness(L_true, L_mut)
            if w == "BUDGET":
                budget_hits.append((tag, len(L_true)))
                w = None
            # (c) the shipped modular verdict, recorded beside the exact one
            modular_sep = bool(not_isospectral(L_mut, L_true))
            if exact_sep != modular_sep:
                spectral_disagree.append((tag, len(L_true), exact_sep, modular_sep))
            if exact_sep and w is not None:
                contradictions.append((tag, len(L_true)))
            if exact_sep:
                nonsim += 1
            elif w is not None:
                gauge += 1
                witnesses.append((tag, P, L_true, L_mut, w))
            else:
                unclassified += 1
        rows[tag] = (app, nonsim, gauge, unclassified)
        if tag != "swap01":
            for k, v in zip(("app", "nonsim", "gauge", "unclassified"),
                            (app, nonsim, gauge, unclassified)):
                tot[k] += v
        print("    %-7s %3d biting = %3d NON-SIMILAR + %2d GAUGE + %d unclassified "
              "  (artifact: %d = %d + %d)"
              % (tag, app, nonsim, gauge, unclassified,
                 SHIPPED[tag][0], SHIPPED[tag][1], SHIPPED[tag][2]))
    print("    %-7s %3d biting = %3d NON-SIMILAR + %2d GAUGE + %d unclassified "
          "  (artifact: 297 = 288 + 9 + 0)"
          % ("TOTAL", tot["app"], tot["nonsim"], tot["gauge"], tot["unclassified"]))
    print()

    agrees = all(rows[t][:3] == SHIPPED[t] for t in SHIPPED)
    L.check("A2.1a every row of the dichotomy is reproduced exactly by an "
            "instrument that shares no line with the shipped one", agrees)
    L.predicted("P3a", agrees and (tot["app"], tot["nonsim"], tot["gauge"],
                                   tot["unclassified"]) == (297, 288, 9, 0),
                "297 = 288 + 9 + 0, per row I1 66/6, I2 82/0, I3 82/0, I4 58/3, "
                "swap01 0/72 -- got %d = %d + %d + %d, per row %s"
                % (tot["app"], tot["nonsim"], tot["gauge"], tot["unclassified"],
                   ", ".join("%s %d/%d" % (t, rows[t][1], rows[t][2])
                             for t, _ in MODES + [SWAP])))
    L.check("A2.1b the search never ran out of node budget, so no NOT-GAUGE "
            "answer here is 'searched and gave up' (%d exhausted)"
            % len(budget_hits), not budget_hits)

    # ---- P3b: the bucket the shipped `elif` cannot see --------------------
    print("A2.2 -- THE CHECK THE REPAIR DOES NOT CONTAIN: is any pair BOTH "
          "spectrally separated AND a gauge?")
    print("    The shipped bin is `if not_isospectral: ... elif witness: ...`, so "
          "a pair that is both is filed NON-SIMILAR and the contradiction has no "
          "row to land in.  Both questions are asked of all %d pairs here."
          % (tot["app"] + rows["swap01"][0]))
    L.check("A2.2a no pair is both spectrally separated and a gauge (%d found) "
            "-- a signed-permutation conjugation is a similarity, so one would "
            "mean an instrument is broken, not that the repair is wrong"
            % len(contradictions), not contradictions)
    L.predicted("P3b", not contradictions,
                "0 contradictions between the two instruments (found %d)"
                % len(contradictions))
    print()

    # ---- P3c: every witness reconstructed --------------------------------
    print("A2.3 -- the GAUGE witnesses, reconstructed entry by entry")
    good = 0
    for tag, P, A, B, (sigma, s) in witnesses:
        rec = L.reconstruct(A, sigma, s)
        ok = rec == B
        good += ok
        print("    %-7s |L(P)| = %-3d pi is %s, %d sign flips -- reconstruction "
              "%s the corrupted matrix"
              % (tag, len(A), "the identity" if sigma == list(range(len(A)))
                 else "NOT the identity", sum(1 for x in s if x < 0),
                 "EQUALS" if ok else "DIFFERS FROM"))
    L.check("A2.3a all %d GAUGE witnesses over the four scored rows reconstruct "
            "to the corrupted matrix entry by entry" % tot["gauge"],
            good == len(witnesses) and tot["gauge"] == 9)
    L.predicted("P3c", good == len(witnesses) and tot["gauge"] == 9,
                "9 of 9 gauge witnesses reconstruct (got %d of %d, over %d gauge "
                "pairs in the four scored rows)"
                % (good, len(witnesses), tot["gauge"]))
    print()

    # ---- P3d: exhaustive agreement where m! is enumerable ----------------
    print("A2.4 -- exhaustive m! x 2^m agreement on every biting pair with "
          "|L(P)| <= 6")
    ex_agree = ex_tot = 0
    for tag, mode in MODES + [SWAP]:
        for P in ps:
            L_true, _ = claim1_pair(P)
            if len(L_true) > 6:
                continue
            L_mut, _ = claim1_pair(P, incidence_mode=mode)
            if mat_eq(L_mut, L_true):
                continue
            ex_tot += 1
            brute = L.brute_signed_perm(L_true, L_mut) is not None
            shipped = signed_permutation_witness(
                L_true, L_mut, gauge_candidate_perms(P, mode)) is not None
            ex_agree += brute == shipped
    L.check("A2.4a brute force over all m! permutations x 2^m sign vectors "
            "agrees with the SHIPPED classification on %d/%d biting pairs with "
            "|L(P)| <= 6 -- and this is where the shipped row's own disclosure "
            "that a NOT-GAUGE answer is 'bounded by the candidate list' is "
            "actually discharged" % (ex_agree, ex_tot),
            ex_agree == ex_tot and ex_tot > 0)
    L.predicted("P3d", ex_agree == ex_tot and ex_tot > 0,
                "full agreement between exhaustive search and the shipped "
                "classification on the |L(P)| <= 6 pairs (%d/%d)"
                % (ex_agree, ex_tot))

    # ... and the same question above the brute-force size, where the shipped
    # bound really is a bound and this file's search is not.
    unbounded_agree = unbounded_tot = 0
    for tag, mode in MODES + [SWAP]:
        for P in ps:
            L_true, _ = claim1_pair(P)
            if len(L_true) <= 6:
                continue
            L_mut, _ = claim1_pair(P, incidence_mode=mode)
            if mat_eq(L_mut, L_true):
                continue
            unbounded_tot += 1
            mine = L.signed_perm_witness(L_true, L_mut)
            shipped = signed_permutation_witness(
                L_true, L_mut, gauge_candidate_perms(P, mode)) is not None
            unbounded_agree += (mine not in (None, "BUDGET")) == shipped
    L.check("A2.4b ... and on the %d pairs ABOVE that size, where the shipped "
            "answer is bounded by a three-source candidate list, a search over "
            "all of S_m agrees on %d.  So no NOT-GAUGE answer in this section "
            "rests on the bound at any size."
            % (unbounded_tot, unbounded_agree),
            unbounded_agree == unbounded_tot and unbounded_tot > 0)
    print()

    # ---- P3e: exact vs modular ------------------------------------------
    print("A2.5 -- the exact spectral verdict against the shipped modular one")
    print("    `not_isospectral` is ONE-SIDED: it evaluates det(A - k.I) mod "
          "2^31-1 at k in {3,5,7,11,13} and says True only on a difference.  A "
          "disagreement can therefore only be 'exact separates, modular did "
          "not'.  Over %d pairs there are %d."
          % (tot["app"] + rows["swap01"][0], len(spectral_disagree)))
    for tag, m, e, mod in spectral_disagree[:10]:
        print("      %-7s |L(P)| = %-3d exact says %s, modular says %s"
              % (tag, m, e, mod))
    L.check("A2.5a the exact integer characteristic polynomial agrees with the "
            "shipped five-shift modular verdict on every biting pair (%d "
            "disagreements)" % len(spectral_disagree), not spectral_disagree)
    L.predicted("P3e", not spectral_disagree,
                "full agreement between exact charpolys and the modular verdict "
                "on all %d pairs (found %d disagreements)"
                % (tot["app"] + rows["swap01"][0], len(spectral_disagree)))
    print()

    return L.finish("a2_dichotomy")


if __name__ == "__main__":
    sys.exit(main())
