"""Derive BASELINE.json from mg-0d1b's committed record.  RUN BY HAND, NOT BY THE GATE.

THE GATE NEVER RUNS THIS FILE.  mg-724a's rule, adopted: "There is no --refresh MODE,
because a gate that rewrites its own expectations on demand is laundering with extra
steps."  `run_all.sh` does not invoke this script; regenerating the baseline is a human
act that shows up as a diff to a committed file, with a reason, in the same commit as
whatever made it necessary.

WHAT IS CARRIED AND WHAT IS DERIVED
-----------------------------------
The ticket says: "CARRY c0d1b's TOLERANCES, do not invent new ones."  So every tolerance
here is READ OUT of `code/alias_index_0d1b/alias_groups.json` — x3's own machine output,
the same file `x2_index.py` builds INDEX.md from — and never retyped.  Retyping is not a
hypothetical risk: the ticket body itself quotes the tolerances as "4.7e-10 / 9.1e-13 /
7.3e-12 / 1.1e-07" where the record says 4.666e-10 / 9.097e-13 / 7.310e-12 / 1.108e-07,
and a gate built from the ticket's rounding would be looser than the observed agreement
by a factor of ~1.007 on the gamma row.  Loose by any factor is decorative.

The LABELS are likewise carried, by parsing them out of `x2_index.py` rather than
re-typing them, so the rows in this gate's output are the rows a reader finds in INDEX.md.
x2 assigns them POSITIONALLY (`LABELS[i]`).  That is fine for a document regenerated in
one pass and would be a live hazard for a pinned baseline, so this script freezes the
label TOGETHER WITH the member set, and from here on `libagree` matches groups by their
members.  A future reordering of x3's clustering can no longer silently relabel a row.

Only two things are derived rather than carried, and both are properties this gate needs
that mg-0d1b had no reason to record:

  comparable[]  how many posets each pinned column is actually comparable at.  `spread()`
                skips None/NaN/inf, so a column decaying toward all-None would agree with
                everything over an ever-smaller set.  Pinning the count makes that RED.
  predicate     the primitivity vector over POP-ALL and its digest.  Ten predicates
                agreeing with EACH OTHER is invariant under a change to the POPULATION;
                only pinning the vector itself catches that.
"""

import ast
import hashlib
import json
import os
import sys
import time

import libagree as A
import libnorm as N
import predicates as PR

L = A.L
HERE = os.path.dirname(os.path.abspath(__file__))
GROUPS_PATH = os.path.join(A.INDEX_DIR, "alias_groups.json")
X2_PATH = os.path.join(A.INDEX_DIR, "x2_index.py")


def carried_labels():
    """The LABELS table out of x2_index.py, by parse — not retyped."""
    with open(X2_PATH) as fh:
        tree = ast.parse(fh.read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", None) == "LABELS" for t in node.targets):
            return [ast.literal_eval(e) for e in node.value.elts]
    raise SystemExit("mkbaseline: no LABELS table in %s" % X2_PATH)


def digest(vec):
    return hashlib.sha256(bytes(1 if v else 0 for v in vec)).hexdigest()[:16]


def main():
    t0 = time.time()
    with open(GROUPS_PATH) as fh:
        G = json.load(fh)
    labels = carried_labels()
    if len(G["groups"]) != len(labels):
        raise SystemExit("mkbaseline: %d groups but %d labels — x2's positional mapping "
                         "no longer covers the record; refusing to guess."
                         % (len(G["groups"]), len(labels)))

    POP_ALL = L.population(L.POP_SPEC)
    POP_PRIM = [(n, dn) for (n, dn) in POP_ALL if L.primitive_here(dn, n)]
    if len(POP_ALL) != G["population"]["POP_ALL"] or \
            len(POP_PRIM) != G["population"]["POP_PRIM"]:
        raise SystemExit("mkbaseline: population moved (%d/%d now, %d/%d recorded) — the "
                         "tolerances are stated over the recorded one; refusing."
                         % (len(POP_ALL), len(POP_PRIM),
                            G["population"]["POP_ALL"], G["population"]["POP_PRIM"]))

    print("capturing %d trees over POP-PRIM (%d posets) ..."
          % (len(L.ADAPTERS), len(POP_PRIM)))
    cols, kind, broken = A.capture(POP_PRIM)
    if broken:
        raise SystemExit("mkbaseline: trees failed to run: %s" % broken)
    print("  %d columns captured in %.1fs" % (len(cols), time.time() - t0))

    groups = []
    for i, g in enumerate(G["groups"]):
        members = [(d["tree"], d["name"]) for d in g["names"]]
        missing = [m for m in members if m not in cols]
        if missing:
            raise SystemExit("mkbaseline: recorded member not produced today: %s" % missing)
        # The recorded spread IS the tolerance.  Re-measuring it here and taking the max
        # of the two would be a way for the gate to relax itself on a bad day, so the
        # recorded value is used as-is and the re-measurement is only checked against it.
        tol = g["max_spread"]
        now = A.worst_pair(cols, members)[0]
        if now > tol:
            raise SystemExit(
                "mkbaseline: %s already disagrees by %.6e against the recorded %.6e.  "
                "That is a FINDING and gets a ticket; it is not a tolerance to widen."
                % (labels[i][0], now, tol))
        groups.append({
            "label": labels[i][0],
            "definition": labels[i][1],
            "tolerance": tol,
            "tolerance_source": "alias_groups.json groups[%d].max_spread (mg-0d1b)" % i,
            "observed_at_baseline": now,
            "population": "POP-PRIM",
            "members": [list(m) for m in members],
            "kinds": {"%s:%s" % m: kind[m] for m in members},
            "comparable": {"%s:%s" % m: sum(1 for v in cols[m] if A.finite(v))
                           for m in members},
        })

    # ---- mg-479c.  THE REFUSAL LIVES IN BOTH PLACES, AND THAT IS NOT BELT-AND-BRACES.
    #
    # This script is where a NEW NAME is registered, so this is where "registered without a
    # normalisation" is a thing that can happen.  The gate checks it too, over the pinned
    # members it reads out of BASELINE.json, because a refusal here alone is bypassed by a
    # hand-edit to that file and a refusal there alone lets a bad baseline be written and
    # only fails at the next merge.  Filed in advance as P9, and I did in fact write the
    # gate's copy first.
    decls = N.load()
    undeclared = [m for g in groups for m in
                  [tuple(x) for x in g["members"]] if not decls.has(m)]
    if undeclared:
        raise SystemExit(
            "mkbaseline: %d pinned name(s) have NO declared normalisation: %s.\n"
            "            Refusing to write a baseline the gate would have to guess at.  Add "
            "an entry to NORMALISATION.json naming the convention, the factor to this "
            "group's canonical frame, and the source it is carried from."
            % (len(undeclared), ", ".join("%s:%s" % m for m in undeclared)))
    N.check_consistency(decls.decls,
                        [(g["label"], ["%s:%s" % tuple(m) for m in g["members"]])
                         for g in groups])
    for g in groups:
        members = [tuple(m) for m in g["members"]]
        frame, why = N.tolerance_frame(members, decls)
        g["tolerance_frame"] = frame
        g["tolerance_frame_why"] = why
        g["normalisation"] = {"%s:%s" % m: {
            "convention": decls.decls["%s:%s" % m]["convention"],
            "to_canonical": "%s" % decls.decls["%s:%s" % m]["factor"].as_text()}
            for m in members}
        if frame == "CANONICAL" and decls.canonical_tolerance(g["label"]) is None:
            raise SystemExit(
                "mkbaseline: %s — %s, but its tolerance %.6e is mg-0d1b's max spread of RAW "
                "values and is not stated in the frame the comparison now happens in.  It "
                "is NOT rescalable (members with different factors admit no single "
                "multiplier).  Record a canonical-frame tolerance for this group in "
                "NORMALISATION.json with its measured source."
                % (g["label"], why, g["tolerance"]))

    vecs, types = PR.vectors(POP_ALL)
    pred = {
        "population": "POP-ALL",
        "n_posets": len(POP_ALL),
        "names": sorted(k for k in vecs if k != "lib0d1b:primitive_here"),
        "true_count": sum(vecs["lib0d1b:primitive_here"]),
        "vector_digest": digest(vecs["lib0d1b:primitive_here"]),
        "return_types": types,
    }
    for k, v in vecs.items():
        if digest(v) != pred["vector_digest"]:
            raise SystemExit("mkbaseline: %s disagrees with the population at baseline "
                             "— that is a finding, not a baseline." % k)

    out = {
        "note": "Pinned from mg-0d1b's alias_groups.json.  Regenerated by hand only; see "
                "mkbaseline.py.  A disagreement is a finding and gets a ticket, not an "
                "edit to this file.",
        "derived_from": {
            "alias_groups.json": G["population"],
            "trees": G["trees"],
        },
        "groups": groups,
        "predicate": pred,
        # RESTRICTED TO THE PINNED MEMBERS, deliberately.  A digest over the whole of
        # NORMALISATION.json would send the gate RED the day somebody declares a
        # normalisation for a name this gate does not pin — say while preparing mg-a397's
        # widening — and a red for a non-reason is mg-479c's own thesis about how gates get
        # disabled, shipped inside its remedy.  Filed in advance as E9.
        "normalisation_digest": decls.digest_over(
            [tuple(m) for g in groups for m in g["members"]]),
    }
    with open(A.BASELINE_PATH, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("wrote BASELINE.json — %d groups, %d predicates, %.1fs"
          % (len(groups), len(pred["names"]), time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
