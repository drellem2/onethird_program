"""mg-fcb2 A3 -- THE REJECTION STANDARD, ASKED OF THE ROWS THE REPAIR KEEPS.

The ticket's primary target: *take whatever standard this repair uses to reject
or discount anything, and apply it to every row it keeps.*

mg-e35b's standard is one sentence, and it is the sentence `facet_swap01` was
rejected on:

    a relabelling of the facet set is a signed-permutation conjugation, hence
    isospectral -- so a rejection there is not evidence that the battery can
    tell a construction error from a re-labelling.

mg-e35b turned that sentence on the four rows of NEGATIVE CONTROL 4 and found it
disqualifies nine (poset, row) pairs.  IT DID NOT TURN IT ANYWHERE ELSE.  The
battery keeps a whole set of scored corruption rows outside that section --
NEGATIVE CONTROL 2's M1-M5 and NEGATIVE CONTROL 3's facet-parity row -- scored
under the same acceptance bar mg-2789 was held to ("show your corruption is NOT
absorbable into a parameter the battery already varies"), and nobody has ever
asked them the gauge question.

That is what this file asks, with this audit's own detector, and it reports the
count the standard disqualifies.

A SECOND THING THE TICKET NAMES: *for each row still labelled as measured, try to
prove it.  A repair that relabels three and leaves a fourth unexamined has
reproduced the defect at the surviving row.*  Row I4 is that fourth row -- it is
the one whose absorbability answer mg-e35b left inside a scored condition.
Section A3.3 asks whether that surviving clause is a decision or a theorem.

PREDICTED EXIT: 1 -- P4g refutes "the standard has been asked of the rows kept"
battery-wide.
"""

import sys

import lib_fcb2 as L

fc, po = L.import_face_geometry()
sys.path.insert(0, L.FACE_GEOMETRY)
import controls                                                  # noqa: E402
from controls import claim1_pair                                 # noqa: E402
from controls import entry_mismatches                            # noqa: E402
from face_complex import (absorbable_by_diagonal_twist, diagonal_moves,  # noqa: E402
                          linear_extensions, mat_eq)
from posets import all_posets                                    # noqa: E402


def nc2_mutations(P):
    """NEGATIVE CONTROL 2's five, rebuilt from `negative_control_identity`'s own
    construction.  Each entry is (name, side that moves, the mutated pair)."""
    first = linear_extensions(P)[0]
    return [
        ("M1 no sign twist", "LHS", claim1_pair(P, use_twist=False)),
        ("M2 absolute Laplacian", "LHS", claim1_pair(P, use_relative=False)),
        ("M3 wrong twist", "LHS",
         claim1_pair(P, sign_fn=lambda w, f=first: (-1 if w == f else 1))),
        ("M4 target scaled by 2", "RHS", claim1_pair(P, normalise=True)),
        ("M5 one edge deleted", "RHS", claim1_pair(P, perturb_edge=True)),
    ]


def classify(A, B, cp):
    """The repair's own dichotomy, asked of an arbitrary pair: NON-SIMILAR on a
    spectral proof, GAUGE on an exhibited and reconstructed witness, otherwise
    UNCLASSIFIED.  Same discipline, different instruments."""
    if cp(A) != cp(B):
        return "NON-SIMILAR", None
    w = L.signed_perm_witness(A, B)
    if w == "BUDGET":
        return "BUDGET", None
    if w is None:
        return "UNCLASSIFIED", None
    assert L.reconstruct(A, w[0], w[1]) == B
    return "GAUGE", w


def main():
    print("== mg-fcb2 A3: the gauge standard, asked of the rows kept OUTSIDE "
          "NEGATIVE CONTROL 4 ==")
    print()

    ps = [P for n in range(2, 6) for P in all_posets(n)]
    cache = {}

    def cp(M):
        key = tuple(tuple(r) for r in M)
        if key not in cache:
            cache[key] = L.charpoly_exact(M)
        return cache[key]

    print("A3.1 -- NEGATIVE CONTROL 2's M1-M5 and NEGATIVE CONTROL 3's parity row")
    print("    The question asked of each: on the posets where the mutation "
          "BITES, is the object it corrupts a signed-permutation conjugate of "
          "the true one?  Where the mutation moves the LHS the question is asked "
          "of L^rel; where it moves the TARGET it is asked of the target, "
          "because that is the object that was corrupted.")
    print()

    tally = {}
    order = []
    for P in ps:
        truth = claim1_pair(P)
        muts = nc2_mutations(P) + [("NC3 facet-parity signs", "LHS",
                                    claim1_pair(P, sign_mode="parity"))]
        for name, side, mut in muts:
            if name not in tally:
                tally[name] = {"app": 0, "GAUGE": 0, "NON-SIMILAR": 0,
                               "UNCLASSIFIED": 0, "BUDGET": 0, "side": side,
                               "nonid": 0, "flips": 0}
                order.append(name)
            if mat_eq(mut[0], truth[0]) and mat_eq(mut[1], truth[1]):
                continue                      # vacuous: not a mutation here
            tally[name]["app"] += 1
            i = 0 if side == "LHS" else 1
            verdict, w = classify(truth[i], mut[i], cp)
            tally[name][verdict] += 1
            if w is not None:
                tally[name]["nonid"] += w[0] != list(range(len(w[0])))
                tally[name]["flips"] += sum(1 for x in w[1] if x < 0)

    for name in order:
        t = tally[name]
        pct = (100.0 * t["GAUGE"] / t["app"]) if t["app"] else 0.0
        print("    %-24s (%s)  bites on %3d  ->  %3d GAUGE (%5.1f%%), %3d "
              "NON-SIMILAR, %d unclassified"
              % (name, t["side"], t["app"], t["GAUGE"], pct, t["NON-SIMILAR"],
                 t["UNCLASSIFIED"]))
    print()

    L.check("A3.1z no pair anywhere in this section exhausted the search budget "
            "or came out unclassified, so every count above is a proof either way",
            all(t["BUDGET"] == 0 and t["UNCLASSIFIED"] == 0 for t in tally.values()))

    def frac(name):
        t = tally[name]
        return t["GAUGE"], t["app"]

    for tag, name, want in [("P4a", "M1 no sign twist", "all"),
                            ("P4b", "M3 wrong twist", "all"),
                            ("P4c", "M2 absolute Laplacian", "none"),
                            ("P4d", "M4 target scaled by 2", "none"),
                            ("P4e", "M5 one edge deleted", "none"),
                            ("P4f", "NC3 facet-parity signs", "all")]:
        g, a = frac(name)
        holds = (g == a and a > 0) if want == "all" else (g == 0 and a > 0)
        L.predicted(tag, holds, "%s is %d%% GAUGE on its %d biting posets "
                                "(predicted %s)"
                    % (name, round(100 * g / a) if a else 0, a,
                       "100% GAUGE" if want == "all" else "0% GAUGE"))
    print()

    # ---- what the standard disqualifies, and where it is disclosed --------
    print("A3.2 -- THE COUNT THE STANDARD DISQUALIFIES, AND WHOSE ROW SAYS SO")
    art = open(L.FACE_GEOMETRY + "/controls_output.txt").read()
    disqualified = [n for n in order if tally[n]["app"] and
                    tally[n]["GAUGE"] == tally[n]["app"]]
    # NEGATIVE CONTROL 3's row DISCLOSES it in its own text; NEGATIVE CONTROL 2's
    # M1 and M3 rows do not.  The disclosure is looked for in the artifact rather
    # than assumed from the source.
    nc3_disclosed = ("the corruption is the diagonal conjugation" in art
                     or "L_parity = D . L . D" in art
                     or "isospectral" in art)
    m_rows = [l for l in art.splitlines()
              if l.strip().startswith("[PASS] M1 ") or l.strip().startswith("[PASS] M3 ")]
    m_disclosed = [l for l in m_rows
                   if "gauge" in l.lower() or "signed-permutation" in l.lower()
                   or "isospectral" in l.lower()]
    print("    fully disqualified by the standard: %s" % ", ".join(disqualified))
    print("    NEGATIVE CONTROL 3's parity row discloses it in its own text: %s"
          % nc3_disclosed)
    print("    of the %d printed M1/M3 rows, %d mention the gauge question at all"
          % (len(m_rows), len(m_disclosed)))
    for l in m_rows:
        print("      %s" % l.strip()[:150])
    L.check("A3.2a every row the standard disqualifies says so in its own text",
            len(m_disclosed) == len(m_rows) and len(m_rows) > 0)
    L.predicted("P4g", len(m_disclosed) == 0 and len(m_rows) == 2
                and "M1 no sign twist" in disqualified
                and "M3 wrong twist" in disqualified,
                "the standard disqualifies TWO rows nobody has asked (M1, M3) "
                "and their text says nothing about it -- %d of %d M1/M3 rows "
                "mention it" % (len(m_disclosed), len(m_rows)))

    # THE STANDARD SEPARATES.  A standard that disqualified everything would be
    # worth nothing; the ticket asks for this explicitly when a count comes out 0,
    # and it is worth showing when it does not.
    separates = [n for n in order if tally[n]["app"] and tally[n]["GAUGE"] == 0]
    print("    ... and the standard is not a rubber stamp: it REJECTS %s, on a "
          "spectral proof each time.  So the %d it disqualifies are a decision "
          "about those rows and not a property of the detector."
          % (", ".join(separates), len(disqualified)))
    L.check("A3.2b the standard separates on this population -- it disqualifies "
            "%d of the %d rows asked and clears %d"
            % (len(disqualified), len(order), len(separates)),
            0 < len(disqualified) < len(order) and len(separates) > 0)
    print()

    # ---- the fourth row, the one still labelled as measured ---------------
    print("A3.3 -- ROW I4, THE ONE STILL SCORED AS A MEASUREMENT")
    print("    mg-8a12 routed I1, I2 and I3's absorbability answers to a "
          "[CANNOT FAIL] row because their diagonal moves on every biting poset. "
          "Row I4 keeps `absorb == 0` inside its scored condition.  The ticket: "
          "a repair that relabels three and leaves a fourth unexamined has "
          "reproduced the defect at the surviving row.  So: on the posets where "
          "I4's diagonal SURVIVES -- the only ones where the predicate is not "
          "already forced by s_i^2 = 1 -- could it have answered `absorbable`?")
    surv = []
    for P in ps:
        L_true, target = claim1_pair(P)
        L_mut, _ = claim1_pair(P, incidence_mode="facet_offbyone")
        if mat_eq(L_mut, L_true) or len(L_mut) != len(L_true):
            continue
        if not diagonal_moves(L_mut, target):
            dm, ds = entry_mismatches(L_mut, target)
            surv.append((len(L_true), dm, ds,
                         absorbable_by_diagonal_twist(L_mut, target)))
    print("    the diagonal survives on %d of row I4's biting posets:" % len(surv))
    for m, dm, ds, ab in surv:
        print("      |L(P)| = %-4d %d off-diagonal MAGNITUDES differ, %d entries "
              "differ in SIGN ALONE, predicate says absorbable = %s"
              % (m, dm, ds, ab))
    forced_here = all(dm > 0 and ds == 0 for _, dm, ds, _ in surv)
    print("    on every one of them at least one off-diagonal MAGNITUDE differs "
          "and nothing differs in sign alone, so |s_i s_j| = 1 rejects before any "
          "sign is read: the surviving clause is forced too.")
    L.check("A3.3a row I4's `absorb == 0` is a DECISION on the posets where its "
            "diagonal survives -- i.e. the predicate could have said absorbable "
            "there", not forced_here)
    # ... and whether the repair says so itself.  It does, and that is the
    # difference between an unexamined surviving row and a disclosed one.
    disclosed = ("row I4 still carries a forced clause in a scored condition and "
                 "now SAYS SO" in art)
    print("    does the repair DISCLOSE that its surviving scored clause is "
          "forced?  %s" % disclosed)
    L.check("A3.3b ... and where it is forced, the repair says so in the "
            "artifact rather than leaving the fourth row unexamined -- this is "
            "the ticket's 'reproduced the defect at the surviving row', and it "
            "is NOT reproduced here", disclosed)
    print()

    return L.finish("a3_standard_elsewhere")


if __name__ == "__main__":
    sys.exit(main())
