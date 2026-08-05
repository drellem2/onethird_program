"""p4_gate.py -- F-A: THE GATE WHOSE INPUT CANNOT CONTAIN WHAT IT TESTS FOR.

From the same verdict as this ticket's headline:

    t1_population.py:430 gates on `not [r for r in pinned if r["kind"] ==
    "OLDEST"]`, where `pinned` is ANCHORS.tsv -- four rows drawn from a
    population HISTORY_KINDS EXCLUDES OLDEST FROM BY CONSTRUCTION.

Two things are done here and they are different.  (a) The gate's input domain
is traced through the code that fills it, which is a PROOF that it cannot
fire.  (b) The absorption is CONSTRUCTED in a clone, which is a demonstration
that the thing it is supposed to catch can happen while it stays silent.  A
proof without the construction is an argument; a construction without the
proof is one example.

Nothing here writes into the repo.  The mutation is a copy under the system
temp directory, and `code/repair_b2af/` is not modified by this branch except
for the STILL-OPEN sentence in its README, which p3 is about.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.  It is expected to exit 1.
"""

import os
import re
import shutil
import sys

import lib6e58 as L

sys.path.insert(0, os.path.join(L.REPO, "code", "repair_b2af"))
import lib_b2af as B2AF                                    # noqa: E402

R = L.Report(selfpop="the construction in a clone under /tmp",
             findpop="the OLDEST gate at code/repair_b2af/t1_population.py:430")

T1 = "code/repair_b2af/t1_population.py"

print("=" * 74)
print("p4 -- F-A: A GATE WHOSE INPUT CANNOT CONTAIN THE THING IT GATES ON")
print("=" * 74)
print()

# ---------------------------------------------------------------------------
print("-- (i) THE GATE, READ FROM THE FILE")
print()

t1src = open(os.path.join(L.REPO, T1)).read().splitlines()
gate_ln = [i + 1 for i, ln in enumerate(t1src)
           if 'r["kind"] == "OLDEST"' in ln and "R.check" in ln]
R.check(len(gate_ln) == 1,
        "expected exactly one OLDEST gate in %s, found %d" % (T1,
                                                              len(gate_ln)))
for ln in gate_ln:
    for k in range(ln - 1, min(ln + 2, len(t1src))):
        print("   %s:%-4d %s" % (T1, k + 1, t1src[k]))
print()

# ---------------------------------------------------------------------------
print("-- (ii) THE PROOF.  WHERE `pinned` COMES FROM")
print()
print("   `pinned` is `L.read_anchors()`, i.e. `ANCHORS.tsv`, and t1 writes")
print("   that file from `spendable`:")
print()
chain = [
    ('hist = sorted(wt["_hist"], ...)', "t1", "the history-derived rows"),
    ("refined = [(r, L.refine(r)) for r in hist]", "t1", "refined from hist"),
    ('spendable = [(r, ref) for r, ref in refined if ref["spendable"]]', "t1",
     "a subset of refined"),
    ('hist = [r for r in rows if r["kind"] in HISTORY_KINDS]', "lib_b2af",
     "and HISTORY_KINDS is where the domain is fixed"),
]
for code, where, what in chain:
    print("      %-62s  %s" % (code[:62], what))
print()
print("   HISTORY_KINDS = %s" % (B2AF.HISTORY_KINDS,))
print("   `OLDEST` in HISTORY_KINDS : %s" % ("OLDEST" in B2AF.HISTORY_KINDS))
print()

pinned = B2AF.read_anchors()
kinds_in_file = sorted({r["kind"] for r in pinned})
print("   rows in ANCHORS.tsv          : %d" % len(pinned))
print("   kinds present in ANCHORS.tsv : %s" % ", ".join(kinds_in_file))
print("   kinds it CAN contain         : %s" % ", ".join(B2AF.HISTORY_KINDS))
print()
print("   SO THE GATE IS A TAUTOLOGY.  `[r for r in pinned if r[\"kind\"] ==")
print("   \"OLDEST\"]` is empty for every possible content of ANCHORS.tsv")
print("   that t1 itself can write.  It is green because its question")
print("   cannot be asked of its input, not because the answer is no.")
print()

R.check(set(kinds_in_file) <= set(B2AF.HISTORY_KINDS),
        "ANCHORS.tsv contains a kind outside HISTORY_KINDS; the domain "
        "argument below does not hold at this tree")
R.gate("OLDEST" in B2AF.HISTORY_KINDS,
       "THE GATE AT %s:%s CANNOT FIRE: `pinned` is ANCHORS.tsv, whose rows "
       "t1 draws from `_hist`, which `lib_b2af` filters to HISTORY_KINDS = "
       "%s.  `OLDEST` is not in that tuple, so the tested set is empty by "
       "construction and the check is green for every input it can receive."
       % (T1, gate_ln[0] if gate_ln else "?", B2AF.HISTORY_KINDS))

# ---------------------------------------------------------------------------
print("-- (iii) THE CONSTRUCTION.  ABSORPTION, IN A CLONE")
print()
print("   An absorption is: a site that WAS `OLDEST` -- the class mg-330a")
print("   named as safe and mg-b2af declined to treat -- becomes one of the")
print("   history-derived kinds, so the treated population grows by")
print("   swallowing a class that does not have the defect.  Constructed by")
print("   deleting `--reverse` from ONE `OLDEST` site in a copy of `code/`.")
print()

tmp = L.tmpdir()
try:
    L.clone_repo(tmp)
    calls, _u = L.all_calls(repo=tmp)
    before = L.census(L.POP_C, calls=calls)
    old_before = [r for r in before["_rows"] if r["kind"] == "OLDEST"]
    R.check(bool(old_before), "no OLDEST site to mutate in the clone")

    victim = sorted(old_before, key=L.site_key)[0]
    print("   victim site : %s" % L.site_key(victim))
    print("   its line    : %s" % victim["src"][:70])

    path = os.path.join(tmp, victim["file"])
    with open(path) as fh:
        src = fh.read()
    lines = src.splitlines(True)
    i = victim["line"] - 1
    mutated = re.sub(r'\s*,?\s*"--reverse"', "", lines[i], count=1)
    R.check(mutated != lines[i],
            "`--reverse` is not on the victim's own line; the mutation did "
            "not happen and everything below would be measuring nothing")
    lines[i] = mutated
    with open(path, "w") as fh:
        fh.write("".join(lines))
    print("   after       : %s" % mutated.strip()[:70])
    print()

    calls2, _u2 = L.all_calls(repo=tmp)
    after = L.census(L.POP_C, calls=calls2)

    print("   %-22s %8s %8s" % ("kind", "before", "after"))
    for k in ("OLDEST",) + L.HISTORY_KINDS + ("ALL", "HISTORY"):
        print("   %-22s %8d %8d" % (k, before[k], after[k]))
    print()

    moved = [r for r in after["_rows"]
             if L.site_key(r) == L.site_key(victim)]
    newkind = moved[0]["kind"] if moved else "GONE"
    print("   the victim is now classified : %s" % newkind)
    print("   it is a HISTORY-DERIVED kind : %s"
          % (newkind in L.HISTORY_KINDS))
    print()

    R.check(after["OLDEST"] == before["OLDEST"] - 1,
            "OLDEST did not drop by exactly 1 (%d -> %d); the construction "
            "did something other than what it says"
            % (before["OLDEST"], after["OLDEST"]))
    R.check(newkind in L.HISTORY_KINDS,
            "the mutated site did not enter a history-derived kind (%s); "
            "there is no absorption to be silent about" % newkind)

    # ---- the gate, evaluated on the mutated tree -------------------------
    print("-- (iv) THE GATE, EVALUATED ON THAT TREE")
    print()
    pinned_after = B2AF.read_anchors()
    gate_says = not [r for r in pinned_after if r["kind"] == "OLDEST"]
    print("   the gate's own expression, on the mutated tree:")
    print("      not [r for r in pinned if r[\"kind\"] == \"OLDEST\"]  ->  %s"
          % gate_says)
    print("   OLDEST went %d -> %d and the gate is %s."
          % (before["OLDEST"], after["OLDEST"],
             "SILENT" if gate_says else "RED"))
    print()

    R.gate(not gate_says,
           "AND IT IS SILENT: OLDEST went %d -> %d in the clone, the "
           "absorbed site is now %s -- a history-derived kind -- and the "
           "gate at %s:%s still evaluates True.  A gate whose input cannot "
           "contain the thing it gates on."
           % (before["OLDEST"], after["OLDEST"], newkind, T1,
              gate_ln[0] if gate_ln else "?"))

    # ---- a gate that can see it -----------------------------------------
    print("-- (v) A GATE THAT CAN SEE IT")
    print()
    print("   The repair is not a bigger ANCHORS.tsv.  It is to gate on the")
    print("   TREE, where OLDEST lives, instead of on the pinned file, where")
    print("   it cannot.  `gate_absorption` below takes the site-set of the")
    print("   OLDEST class at two trees and fires when a member leaves it")
    print("   for a treated kind.  It is stated as a set difference so that")
    print("   it cannot be satisfied by a count that happens to match.")
    print()

    def gate_absorption(before_rows, after_rows):
        """[(site, was, now)] for every site that was OLDEST and is now a
        treated kind.  Empty means no absorption.

        The population is the TREE's classification at two points, not a
        pinned file: the class this gate is about is excluded from the
        pinned file by construction, which is the whole finding.
        """
        was = {L.site_key(r): r["kind"] for r in before_rows}
        now = {L.site_key(r): r["kind"] for r in after_rows}
        return [(k, was[k], now.get(k, "GONE")) for k in sorted(was)
                if was[k] == "OLDEST"
                and now.get(k, "GONE") in L.HISTORY_KINDS]

    fired = gate_absorption(before["_rows"], after["_rows"])
    print("   on the MUTATED clone   : %d row(s)" % len(fired))
    for k, w, n in fired:
        print("      %-56s %s -> %s" % (k, w, n))
    quiet = gate_absorption(before["_rows"], before["_rows"])
    print("   on the UNMUTATED clone : %d row(s)   <- the negative control"
          % len(quiet))
    print()
    print("   A gate that has never been seen to go red is a gate whose red")
    print("   is unmeasured.  That sentence is mg-330a's, and it is the one")
    print("   its own successor's gate does not satisfy.")
    print()

    R.check(len(fired) == 1,
            "the replacement gate did not fire exactly once on the "
            "constructed absorption (%d)" % len(fired))
    R.check(not quiet,
            "the replacement gate fires on an unmutated tree; it is not a "
            "gate, it is a constant")

    print("-- (vi) WHAT THIS TICKET DOES ABOUT IT, AND WHAT IT DOES NOT")
    print()
    print("   NOT DONE: `t1_population.py:%s` is not edited."
          % (gate_ln[0] if gate_ln else "?"))
    print("   mg-b2af's transcripts are committed evidence of a run of that")
    print("   script.  Changing the script without regenerating them makes")
    print("   the pair inconsistent, and regenerating them re-runs another")
    print("   ticket's suite from inside mine -- which is how a repair ends")
    print("   up owning a figure it did not measure.  The working gate is")
    print("   HERE, run against the same population, shown red on a")
    print("   construction and green on a control.")
    print("   DONE: `code/repair_b2af/README.md` gains a note that the")
    print("   OLDEST gate cannot fire, pointing at this transcript.")
    print()

    print("-- SCORING PREDICTIONS.md")
    print()
    L.score(R, "P4-a", True,
            len([r for r in pinned if r["kind"] == "OLDEST"]) == 0
            and "OLDEST" not in B2AF.HISTORY_KINDS,
            note="0 OLDEST rows, and the domain excludes them")
    L.score(R, "P4-b", -1, after["OLDEST"] - before["OLDEST"],
            note="OLDEST drops by exactly 1")
    L.score(R, "P4-c", True, gate_says, note="the gate stays silent")
    L.score(R, "P4-d", 1, len(fired), note="the replacement gate fires")
    print()
finally:
    shutil.rmtree(tmp, ignore_errors=True)

raise SystemExit(R.emit())
