"""Seed NORMALISATION.json from mg-0d1b's MEASURED agreement.  RUN BY HAND, ONCE.

THE 71 IDENTITY FACTORS ARE NOT A JUDGEMENT.  The only evidence anybody has that these
names share a normalisation is that mg-0d1b measured them AGREEING to <= tolerance in the
raw frame; writing `"factor": 1` seventy-one times by hand would be seventy-one assertions
this ticket cannot back.  So each declaration is seeded from `BASELINE.json` and carries
the measured spread it was seeded from as a machine-checkable number
(`seeded_from_measured_spread`), which `libnorm.validate` re-checks against the record on
every gate run.  A seed that goes stale is REFUSED rather than believed.

THE DECLARATION IS REDUNDANT FOR THESE 71 NAMES AND EXISTS SO THE 72nd CANNOT BE ADDED
SILENTLY.  That is the whole of what this file buys today: the twelve pinned groups
contain no normalisation pair, the gate has run with zero disagreements, and nothing fires.
The exposure is PROSPECTIVE — it arrives the moment the check is widened (mg-a397's
candidates) or a new alias is registered — and a representation added after the first
false red is a representation added under pressure to make a red go away.

IT REFUSES TO RUN ONCE THE FILE EXISTS, and that is not tidiness.  A script that fills in
identity declarations for whatever is in the record would silently absorb the next name
added to the record, which is PRECISELY the defect this ticket is about: an undeclared
normalisation defaulting to "same".  There is no --refresh here for the same reason
mg-724a gives for the baseline: a gate that regenerates its own expectations on demand is
laundering with extra steps.  Adding a name means writing its declaration, by hand, with
its derivation, in the same commit as whatever made it necessary.
"""

import json
import os
import sys

import libagree as A
import libnorm as N

HERE = os.path.dirname(os.path.abspath(__file__))

# The one convention that exists today, and its content is "the frame mg-0d1b measured in".
# It is ONE convention rather than twelve because the claim being made is exactly this:
# every pinned name reports its quantity in the frame that mg-0d1b's tolerances were
# measured over.  Twelve per-group convention ids would have made the cross-group
# comparison of two factors meaningless without saying anything the members do not already
# say by sharing a group.
SEED_CONVENTION = "mg-0d1b-raw"

CONVENTIONS = {
    SEED_CONVENTION: {
        "description":
            "The frame in which mg-0d1b measured these names agreeing: every value is "
            "reported as its own tree's entry point returns it, with no factor applied.  "
            "This is the canonical frame BY CONSTRUCTION — it is the frame all twelve "
            "recorded tolerances are stated over — and not by any argument that it is the "
            "natural one.",
        "source":
            "code/alias_index_0d1b/alias_groups.json, via "
            "code/alias_agreement_06d1/BASELINE.json (mg-0d1b, carried by mg-06d1)",
    },
    # The two frames of the worked example below.  They are defined here, in the same map
    # as the live one, because `conventions` is the vocabulary and a convention id that is
    # not in it is REFUSED — including for an illustrative entry.  What keeps the example
    # out of the live comparison is which SECTION its declarations sit in, not a second
    # class of convention.
    "eps/spectral-6-over-n2-minus-1": {
        "description":
            "ILLUSTRATIVE ONLY — no pinned name is in this frame.  eps as Op-Form :437 and "
            "STATE.md:15 write it: eps_spec = 6 E[inv_e] / (n^2 - 1).",
        "source": "code/c3_audit_a94c3/a1_algebra.py:14",
    },
    "eps/c3ca-over-n2": {
        "description":
            "ILLUSTRATIVE ONLY — no pinned name is in this frame.  eps as "
            "OneThird-LIBweak-mg-c3ca.md:172 writes it: eps_c3ca = E[inv_e] / n^2.",
        "source": "code/c3_audit_a94c3/a1_algebra.py:15",
    },
}

# THE WORKED EXAMPLE, AND WHY IT IS NOT A LIVE DECLARATION.
#
# `eps_spec` and `eps_c3ca` are two normalisations of one quantity and have been in this
# arc for a long time, but NEITHER is pinned, neither is produced by any of lib0d1b's
# adapters, and no tree in the twelve computes them.  A live declaration about a name
# nothing computes is a statement the gate can never check — so it goes here, in a section
# the gate PARSES and VALIDATES but never compares values with.  What it is for is to
# demonstrate on a real corpus pair that the representation is strong enough for the
# examples the ticket names: the factor is n-DEPENDENT and a constant field could not hold
# it.  Arm N4 checks it against the exact rationals in
# code/unitmap_audit_9f91/out_m1_map.txt rather than against this comment.
ILLUSTRATIVE = {
    "c3_audit_a94c3:eps_spec": {
        "convention": "eps/spectral-6-over-n2-minus-1",
        "factor": {"num": [0, 0, 6], "den": [-1, 0, 1]},
        "derivation":
            "eps_spec = 6 E[inv_e] / (n^2 - 1) and eps_c3ca = E[inv_e] / n^2, so "
            "eps_spec / eps_c3ca = 6 n^2 / (n^2 - 1).  Taking eps_c3ca as the canonical "
            "frame, eps_spec's factor is that ratio.  NOT A CONSTANT: a flat 6 is wrong by "
            "+0.083 at n=3 and only approaches correct as n -> infinity.",
        "source":
            "code/c3_audit_a94c3/a1_algebra.py:14-18 (statement); "
            "code/unitmap_audit_9f91/out_m1_map.txt:17-22 (exact rationals at n=3,4,5,6,8, "
            "under the heading 'what a flat factor of 6 gets wrong at small n')",
    },
    "unitmap_audit_9f91:eps_c3ca": {
        "convention": "eps/c3ca-over-n2",
        "factor": {"num": [1], "den": [1]},
        "derivation":
            "The canonical frame CHOSEN FOR THIS EXAMPLE, and the choice is arbitrary and "
            "carries no claim: taking eps_spec as canonical instead would give eps_c3ca "
            "the reciprocal factor (n^2 - 1)/(6 n^2) and every canonical value would move "
            "by the same factor.  A normalisation field states RELATIVE frames; it does "
            "not privilege one.",
        "source": "code/unitmap_audit_9f91/out_m1_map.txt:17-22",
    },
}


def main():
    if os.path.exists(N.NORM_PATH):
        print("mknorm: %s already exists.  REFUSING." % os.path.basename(N.NORM_PATH))
        print("""
  This script seeds identity declarations from whatever is pinned in BASELINE.json.  Run
  a second time, it would absorb the next name added to the record into the identity
  normalisation WITHOUT ANYBODY DECLARING IT — which is exactly the defect mg-479c exists
  to close, arriving through its own remedy.  A new name gets a hand-written declaration
  with its own derivation, in the commit that adds it.""")
        return 2

    BL = A.load_baseline()
    decls = {}
    for g in BL["groups"]:
        for m in g["members"]:
            decls["%s:%s" % tuple(m)] = {
                "convention": SEED_CONVENTION,
                "factor": dict(N.IDENTITY),
                "seeded_from_measured_spread": g["observed_at_baseline"],
                "derivation":
                    "SEEDED, NOT ASSERTED: mg-0d1b measured group `%s` (%d names, %d "
                    "trees) agreeing to a max spread of %.6e over POP-PRIM at %d posets, "
                    "and mg-06d1 pinned that as the tolerance.  Agreement in the raw frame "
                    "IS the evidence that these names share a normalisation; the identity "
                    "factor records that evidence and adds nothing to it.  This "
                    "declaration is REDUNDANT for this name and exists so that the next "
                    "name in this group cannot be added without one."
                    % (g["label"], len(g["members"]),
                       len({tuple(x)[0] for x in g["members"]}),
                       g["observed_at_baseline"],
                       BL["derived_from"]["alias_groups.json"]["POP_PRIM"]),
            }

    out = {
        "note":
            "THE NORMALISATION FIELD (mg-479c).  Per NAME, not per quantity: two names for "
            "one quantity may legitimately differ by a stated factor, and this file is "
            "where that factor is said.  Semantics: raw = factor(n) * canonical, so "
            "canonical = raw / factor(n), with factor a rational function of n in exact "
            "integer coefficients ascending in n.  An UNDECLARED normalisation is REFUSED "
            "(exit 2) and never defaulted to 'same'.  Seeded once by mknorm.py, which "
            "refuses to run again; a new name is declared BY HAND with its own derivation.",
        "semantics": {
            "raw = factor(n) * canonical": True,
            "factor": "{num: [c0, c1, ...], den: [d0, d1, ...]} — integer coefficients "
                      "ASCENDING in n; evaluated as an exact Fraction; {num:[1],den:[1]} "
                      "is the identity and is a PASS-THROUGH, not a multiply by 1.0",
            "convention": "a NAME for a frame.  Within one alias group: same convention "
                          "=> equal factors, different conventions => different factors.  "
                          "Both are hard refusals.",
        },
        "conventions": CONVENTIONS,
        "declarations": decls,
        "illustrative": ILLUSTRATIVE,
        "canonical_tolerances": {},
    }
    out["pinned_digest"] = N.digest_of(N.Declarations(out), BL)

    with open(N.NORM_PATH, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("wrote NORMALISATION.json — %d live declarations (%d identity), %d illustrative, "
          "digest %s" % (len(decls),
                         sum(1 for e in decls.values() if N.is_identity(e["factor"])),
                         len(ILLUSTRATIVE), out["pinned_digest"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
