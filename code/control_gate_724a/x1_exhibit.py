#!/usr/bin/env python3
"""mg-724a — THE EXHIBIT: why this gate is a comparison and not an exit code.

THE CLAIM UNDER TEST, stated so it can lose: `code/rendered_twin_pin_9bc2/run_all.sh` exits 0
when a published ledger row in STATE.md silently moves away from its rendered twin.  If that
is false, this gate's whole design is over-engineering and `[gates] commands = ["sh
code/rendered_twin_pin_9bc2/run_all.sh"]` would have been the right answer.

WHAT IT PLANTS.  One cell of ledger row 7 in STATE.md — `any` -> `n ≤ 6` — which is a
published applicability claim narrowing, i.e. exactly the class of event mg-64cb is about.
Row 7 is chosen because it is currently UNDRIFTED and no fixture anywhere in the estate names
it; row 1 is not usable because `rendered_twin_pin_9bc2/negative_control.py` already plants a
mutation there, and mutating it makes THAT fixture unfalsifiable and the suite exits 2 — a
true red, but for the wrong reason, and it would have flattered this exhibit.  (That was
measured, not reasoned about: row 1 first, runner exit 2, negative exit 1.)

WHY THIS IS NOT PART OF THE MERGE GATE.  It writes to STATE.md.  A gate that mutates the tree
it is gating can leave that tree wrong when it is killed, and gates do get killed — the
refinery kills one at its timeout and mg-f8e5 had a re-run killed mid-mutation leaving four
files dirty.  So the LIVE control for this property is probe T1 in negative_control.py, which
tests the same thing on every merge by mutating the captured BYTES and touching nothing.
This file is the evidence for the design decision; T1 is the control that keeps it true.

RESTORATION IS CHECKED, NOT ASSUMED.  STATE.md's sha256 is taken before and after and this
producer REFUSES if they differ.  The two subject suites rewrite their own out_*.txt as they
always do; that is their design and this ticket does not edit another ticket's directory.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib724a as L  # noqa: E402

STATE = os.path.join(L.ROOT, "STATE.md")
ROW7_GOOD = "| 7 | identities GID & DG | `U-id` | **proven** | any |"
ROW7_BAD = "| 7 | identities GID & DG | `U-id` | **proven** | n ≤ 6 |"


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    print("=" * 92)
    print("mg-724a — EXHIBIT: the twin suite's EXIT CODE is blind to its own worklist growing")
    print("=" * 92)
    print()

    before_digest = sha(STATE)
    with open(STATE, "rb") as fh:
        original = fh.read()
    text = original.decode("utf-8")

    if text.count(ROW7_GOOD) != 1:
        print("SETUP FAILED — ledger row 7 does not read as this exhibit expects, so the world")
        print("this plants would not be the world it describes.  Found %d occurrence(s) of:"
              % text.count(ROW7_GOOD))
        print("    " + ROW7_GOOD)
        print()
        print("EXHIBIT VERDICT: SETUP FAILED — nothing below was run.")
        return 2

    print("§1  THE GOOD WORLD — the tree as committed")
    print("-" * 92)
    rc_good, out_good = L.run_suite(L.SUITES[0][1])
    good = L.extract({"twin": out_good}, {"twin": rc_good}, only="twin")
    print("  runner exit      : %d" % good["twin.runner_exit"])
    print("  control exit     : %d" % good["twin.control_exit"])
    print("  VERDICT grade    : %s" % good["twin.verdict_grade"])
    print("  drift worklist   : %s" % good["twin.worklist"])
    print()

    print("§2  THE BAD WORLD — ledger row 7's applicability narrowed from `any` to `n ≤ 6`")
    print("-" * 92)
    try:
        with open(STATE, "w") as fh:
            fh.write(text.replace(ROW7_GOOD, ROW7_BAD))
        rc_bad, out_bad = L.run_suite(L.SUITES[0][1])
        bad = L.extract({"twin": out_bad}, {"twin": rc_bad}, only="twin")
    finally:
        with open(STATE, "wb") as fh:
            fh.write(original)

    after_digest = sha(STATE)
    print("  runner exit      : %d" % bad["twin.runner_exit"])
    print("  control exit     : %d" % bad["twin.control_exit"])
    print("  VERDICT grade    : %s" % bad["twin.verdict_grade"])
    print("  drift worklist   : %s" % bad["twin.worklist"])
    print()
    print("  STATE.md sha256 before : %s" % before_digest)
    print("  STATE.md sha256 after  : %s" % after_digest)
    print()

    if before_digest != after_digest:
        print("EXHIBIT VERDICT: BROKEN — this producer did not put STATE.md back.  Restore it")
        print("from git before doing anything else; nothing above is citable.")
        return 2

    # ---- §3 what each instrument saw -------------------------------------------------------
    print("§3  WHAT EACH INSTRUMENT SAW")
    print("-" * 92)
    exit_blind = bad["twin.runner_exit"] == good["twin.runner_exit"]
    worklist_moved = bad["twin.worklist"] != good["twin.worklist"]

    print("  the suite's RUNNER EXIT CODE : %d -> %d   %s"
          % (good["twin.runner_exit"], bad["twin.runner_exit"],
             "UNCHANGED — blind" if exit_blind else "changed — it saw this"))
    print("  the suite's DRIFT WORKLIST   : %s -> %s   %s"
          % (good["twin.worklist"], bad["twin.worklist"],
             "grew — the suite DID see it" if worklist_moved else "unchanged — nothing saw it"))
    print()

    if not worklist_moved:
        print("EXHIBIT VERDICT: THE PLANTED WORLD WAS NOT BAD — the twin control did not react")
        print("at all, so this exhibit shows nothing about the exit code.  A fixture that has")
        print("stopped being a fixture reads exactly like a passing one; this is that refusal.")
        return 2

    if not exit_blind:
        print("EXHIBIT VERDICT: THE CLAIM IS REFUTED — the suite's exit code DID move, so a")
        print("gate wired straight to `sh code/rendered_twin_pin_9bc2/run_all.sh` would have")
        print("caught this after all.  Read that as an argument to SIMPLIFY this gate: the")
        print("comparison against BASELINE.json would then be buying less than it claims.")
        return 1

    print("EXHIBIT VERDICT: CONFIRMED — a published ledger row moved, the twin control saw it")
    print("(worklist %s -> %s), and the suite's runner still exited %d.  A merge gate wired to"
          % (good["twin.worklist"], bad["twin.worklist"], bad["twin.runner_exit"]))
    print("that exit code lands this change.  The gate in this directory reads the WORKLIST,")
    print("compares it to BASELINE.json, and goes RED — which is what probe T1 exercises on")
    print("every merge without writing a byte.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
