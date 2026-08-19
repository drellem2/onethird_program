"""mknorm — SEED NORMALISATION.json, ONCE, FROM THE RECORD.  Never run by the gate.

WHY THIS EXISTS AT ALL, AND WHY IT REFUSES TO RUN TWICE
-------------------------------------------------------
The 71 names mg-06d1 pins all need a normalisation declaration, because ticket item 3 says
an undeclared normalisation must be REFUSED and not defaulted to "same".  Writing
`"factor": 1` seventy-one times by hand would be seventy-one assertions I cannot back — I
have no independent knowledge of what convention `chain_iv_c_81ff:lambda2_bracket` is in.

What I DO have is mg-0d1b's measurement: every one of these groups was measured agreeing to
within `max_spread`, and two names that agree to 4.7e-10 over 306 posets are in ONE
normalisation.  So the identity declarations are DERIVED FROM THAT MEASUREMENT and the
measurement is quoted in each entry's `source`.  Filed in advance as E1.

The declaration is therefore REDUNDANT for these 71 names — it records what mg-0d1b already
measured — and it exists so that the 72nd cannot be added silently.  That is the whole of
the claim and NORMALISATION.json's own note says the same thing.

**IT REFUSES TO RUN IF THE FILE EXISTS.**  A script that fills in identity declarations for
whatever is in the record would silently absorb the next name added to the record, which is
precisely the defect this ticket is about — the `--refresh` hazard mg-724a named, wearing a
new hat.  Filed in advance as E2.  After the seed, declarations are a human act with a diff,
a source, and a reason, exactly like a tolerance.

THE WORKED EXAMPLE IS NOT A DECLARATION
----------------------------------------
`eps_spec` / `eps_c3ca` are two normalisations of one quantity and are the ticket's own
second example.  No adapter produces either, so an entry for them in `declarations` would be
a statement the gate can never check — filed in advance as E6.  They go in
`worked_examples`, which is not consulted by the comparison at all, and `g3_normalisation.py`
checks the declared factor against mg-9f91's committed eleven-row table of exact rationals.
Their purpose is to demonstrate that the representation reaches a REAL corpus normalisation
with an n-DEPENDENT factor, rather than a constant somebody invented for a test.
"""

import ast
import json
import os
import sys

import libagree as A
import libnorm as N

GROUPS_PATH = os.path.join(A.INDEX_DIR, "alias_groups.json")
X2_PATH = os.path.join(A.INDEX_DIR, "x2_index.py")

# Carried from `code/c3_audit_a94c3/a1_algebra.py`, which states it in these words:
#
#     eps_spec = 6 E[inv_e] / (n^2 - 1)        <- Op-Form :437, STATE.md:15
#     eps_c3ca =   E[inv_e] / n^2              <- OneThird-LIBweak-mg-c3ca.md:172
#     eps_spec / eps_c3ca = 6 n^2 / (n^2 - 1) -> 6
#
# TYPED HERE AND CHECKED AGAINST TWO INDEPENDENT COMMITTED RECORDS, which is not the same as
# typed and asserted: `g3_normalisation.py` re-derives it at every n in mg-9f91's table of
# exact rationals AND greps the identity out of a94c3's source, so a mistyped coefficient
# fails loudly at eleven values of n rather than sitting there being decorative.
EPS_FACTOR = {"num": [0, 0, 6], "den": [-1, 0, 1]}          # 6n^2 / (n^2 - 1)
EPS_CITE_FILE = os.path.join(os.path.dirname(A.INDEX_DIR), "c3_audit_a94c3", "a1_algebra.py")
EPS_CITE_TEXT = "eps_spec / eps_c3ca = 6 n^2 / (n^2 - 1)"


def carried_labels():
    """x2_index.py's LABELS table, by parse — the same route mkbaseline.py takes."""
    with open(X2_PATH) as fh:
        tree = ast.parse(fh.read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", None) == "LABELS" for t in node.targets):
            return [ast.literal_eval(e) for e in node.value.elts]
    raise SystemExit("mknorm: no LABELS table in %s" % X2_PATH)


def main():
    if os.path.exists(N.NORM_PATH):
        raise SystemExit(
            "mknorm: %s already exists and this script REFUSES to rewrite it.\n"
            "        Seeding is a one-shot derivation from mg-0d1b's measured agreement.  A\n"
            "        script that re-derives identity declarations on demand would absorb the\n"
            "        next name added to the record silently, which is the exact defect\n"
            "        mg-479c exists to close.  Add the entry by hand, with its source."
            % os.path.basename(N.NORM_PATH))

    with open(GROUPS_PATH) as fh:
        G = json.load(fh)
    labels = carried_labels()
    if len(G["groups"]) != len(labels):
        raise SystemExit("mknorm: %d groups but %d labels — refusing to guess the mapping."
                         % (len(G["groups"]), len(labels)))
    if not os.path.exists(EPS_CITE_FILE):
        raise SystemExit("mknorm: %s is gone; the worked example has no source."
                         % EPS_CITE_FILE)
    with open(EPS_CITE_FILE) as fh:
        if EPS_CITE_TEXT not in fh.read():
            raise SystemExit("mknorm: %r is no longer in %s — the worked example's identity "
                             "is not where it is cited from."
                             % (EPS_CITE_TEXT, EPS_CITE_FILE))

    decls = {}
    for i, g in enumerate(G["groups"]):
        label, spread = labels[i][0], g["max_spread"]
        for d in g["names"]:
            key = "%s:%s" % (d["tree"], d["name"])
            if key in decls:
                raise SystemExit("mknorm: %s appears in two groups; refusing." % key)
            decls[key] = {
                "convention": label,
                "to_canonical": {"num": [1], "den": [1]},
                "source": "DERIVED, not asserted: mg-0d1b measured this group's %d names "
                          "agreeing to max_spread %.6e over 306 primitive posets "
                          "(alias_groups.json groups[%d].max_spread), which is what it "
                          "means for them to be in ONE normalisation.  Redundant for this "
                          "name; present so that the next name added to this group cannot "
                          "be added without one." % (len(g["names"]), spread, i),
            }

    out = {
        "note": (
            "mg-479c — THE NORMALISATION FIELD, per NAME and not per quantity.  Two names "
            "for one quantity may legitimately differ by a stated factor and this file is "
            "where that is SAID.  THE DIRECTION IS STATED AND NOT LEFT TO BE READ OFF THE "
            "NAME, because a field whose direction is ambiguous is this ticket's own defect "
            "wearing the remedy's clothes: canonical_value = raw_value * num(n)/den(n).  A "
            "name whose values are TWICE the group's canonical ones declares num=[1], "
            "den=[2].  Integer coefficients, low order first, evaluated in exact Fraction "
            "arithmetic; the identity is [1]/[1] and is applied as a pass-through, never as "
            "a multiply by 1.0.  An "
            "UNDECLARED name is REFUSED by the gate (exit 2), never defaulted to `same`.  "
            "The 71 seeded entries are DERIVED from mg-0d1b's measured agreement and are "
            "redundant; they exist so the 72nd cannot be added silently.  A declared factor "
            "is an escape hatch this machinery cannot close — see README §7 — which is why "
            "every non-identity factor is printed on every run, green as well as red."),
        "seeded_by": "mknorm.py (one-shot; it refuses to run once this file exists)",
        "declarations": decls,
        "canonical_tolerances": {},
        "canonical_tolerances_note": (
            "EMPTY, AND THAT IS THE CORRECT STATE TODAY.  mg-0d1b measured every tolerance "
            "as the max spread of RAW values.  While every member of a group is in the "
            "identity normalisation the canonical frame IS the raw frame and the carried "
            "number governs what it always governed.  The moment a group gains a member "
            "with a non-identity factor, the carried number is stated in a frame the "
            "comparison no longer happens in, and it is NOT rescalable — members with "
            "different factors admit no single multiplier.  The gate then REFUSES until the "
            "registrant records a canonical-frame tolerance here with its own measured "
            "source.  Rescaling the frame while keeping the number that governs it would be "
            "mg-479c's own defect one level up."),
        "worked_examples": {
            "eps": {
                "note": (
                    "TWO LIVE NORMALISATIONS OF ONE QUANTITY, and the ticket's own second "
                    "example.  NOT pinned by BASELINE.json, NOT produced by any adapter, and "
                    "NOT consulted by the comparison: an entry in `declarations` for a name "
                    "nothing computes would be a statement the gate can never check.  It is "
                    "here because it is the corpus's proof that a per-name CONSTANT factor "
                    "would have been the wrong representation — the factor is n-DEPENDENT, "
                    "and code/unitmap_audit_9f91/out_m1_map.txt tabulates what a flat 6 gets "
                    "wrong at small n (+0.0833 at n=3).  g3 re-derives it at every n in that "
                    "table rather than asserting it."),
                "names": {
                    "a94c3-doc:eps_spec": {
                        "convention": "eps_spec  = 6 E[inv_e] / (n^2 - 1)",
                        "to_canonical": {"num": [1], "den": [1]},
                        "source": "Op-Form :437, STATE.md:15, cited at "
                                  "code/c3_audit_a94c3/a1_algebra.py:16.  Canonical frame "
                                  "for this worked example by choice of presentation only; "
                                  "no claim is made that it is the right one.",
                    },
                    "a94c3-doc:eps_c3ca": {
                        "convention": "eps_c3ca  =   E[inv_e] / n^2",
                        "to_canonical": EPS_FACTOR,
                        "source": "OneThird-LIBweak-mg-c3ca.md:172, cited at "
                                  "code/c3_audit_a94c3/a1_algebra.py:17; the factor is that "
                                  "file's own line 18, `eps_spec / eps_c3ca = 6 n^2 / "
                                  "(n^2 - 1)`, checked by g3 against the eleven exact "
                                  "rationals in code/unitmap_audit_9f91/out_m1_map.txt.",
                    },
                },
            },
        },
        "not_declared": {
            "note": (
                "mg-479c REGISTERS NOTHING ABOUT THE (L*)/(M#) GAP, DELIBERATELY.  "
                "STATE.md:172 says `the gap between (L*) and (M#) is exactly mu_pref^2`; in "
                "the normalisation that row itself uses (mu*Delta <= gamma) it is "
                "mu_pref^2/2, and it is mu_pref^2 in the doubled form 2*mu*Delta <= 2*gamma.  "
                "BOTH READINGS ARE IN THE CORPUS.  Ticket item 4: this ticket builds the "
                "machinery to REPRESENT the answer and does not decide it — that is mg-5e82's "
                "business and a mathematical question.  Registering a factor of 1 or of 2 for "
                "either name would decide it under this ticket's cover, so neither is "
                "registered, and g3's arm N7 goes RED if one ever appears in this file "
                "without the arm being updated."),
            "names": ["mu_pref^2 gap (L*) vs (M#)  — STATE.md:172, owned by mg-5e82"],
        },
    }

    with open(N.NORM_PATH, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("wrote %s — %d declarations, %d worked-example names"
          % (os.path.basename(N.NORM_PATH), len(decls),
             sum(len(b["names"]) for b in out["worked_examples"].values())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
