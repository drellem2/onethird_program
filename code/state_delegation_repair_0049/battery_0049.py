#!/usr/bin/env python3
"""mg-0049 — NINE MUTATIONS ON THE DELEGATED SURFACE, ON THE AUDITOR'S OWN HARNESS.

WHY mg-5644's HARNESS AND NOT A SIXTH ONE.  This is the party under test writing evidence
about its own repair, and mg-bee1 argued the right way round for that position: an auditor
should build its own harness, a repair should run on the auditor's.  So nothing here has a
snapshot, a restore rule or an exit-code reader of its own — `harness5644.py` is imported
UNMODIFIED and does all three.  `git diff` over code/state_delegation_audit_5644/ is empty
and `run_all.sh` prints the proof.

WHAT IT ADDS TO mg-5644's SIX.  R1 R2 R3 R4 are mg-5644's Q1 Q2 Q3 Q4, restated here so the
repair is measured against the exact rows that broke it, with the exit codes now PREDICTED
TO BE DIFFERENT for R1 and R2 and PREDICTED TO BE UNCHANGED for R3 and R4 — a repair that
moved the bound would be an over-correction and would show up here as a surprise on R3/R4.
R5 to R9 are new and are the ones worth arguing with:

    R5  a wrapper that suppresses NOTHING and is caught by the GUARD ALONE
    R6  mg-babf's B04 shape one file out — the cited sections under a "void" heading, no
        cited byte moved, caught by the HEADING FIELD alone
    R7  a cited section deleted — the inherited mechanism, shown not to have been weakened
    R8  the blank page produced by a CLOSED comment, so the catch is not an artefact of the
        mutation being malformed
    R9  the running COST of extending default-deny to a third file, as a row

Which mechanism catches which row is not asserted here; `split_0049.py` measures it.
"""
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, os.path.join(REPO, "code", "state_delegation_audit_5644"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import harness5644 as H              # noqa: E402  — the AUDITOR's harness, unmodified
import mutations_0049 as M           # noqa: E402

ATTEMPT = H.ATTEMPT


def main():
    if ATTEMPT != M.ATTEMPT:
        raise SystemExit(f"harness and mutations disagree about the target: "
                         f"{H.ATTEMPT} vs {M.ATTEMPT}")
    tree = H.Tree([ATTEMPT])
    rows = [(rid, layer, what, want, (lambda fn: lambda orig: {ATTEMPT: fn(orig[ATTEMPT])})(fn))
            for rid, layer, what, want, fn in M.ROWS]
    got = tree.battery(
        rows,
        "mg-0049 — NINE MUTATIONS ON THE SURFACE mg-bee1 CREATED AND THIS REPAIR CLOSES",
        "Run on mg-5644's harness, imported unmodified.  Every mutation edits ONLY\n"
        f"{ATTEMPT} — the file the certified cell POINTS AT.")

    print("=" * 90)
    print("WHAT THESE NINE SAY")
    print("=" * 90)
    print("  R1 and R2 are mg-5644's Q1 and Q2, the two rows that exited 0 against mg-bee1.")
    print("  Both are now exit 1: a reader who follows the certified cell's six links and is")
    print("  shown NOTHING of the section a link names is damage, on the same footing as a")
    print("  certified region nobody is shown.  R8 is the same blank page by a well-formed")
    print("  comment, so the catch does not depend on the mutation being malformed.")
    print()
    print("  R3 and R4 are STILL exit 0 and are meant to be.  They are text a reader IS")
    print("  shown — the target's own framing, and a section nothing cites — and the bound")
    print("  is stated in those terms in delta_control.py's header and in COVERAGE.md.")
    print("  A repair that made these fire would have widened the claim past what it")
    print("  measured, which is the defect this lineage keeps repeating in the other")
    print("  direction.")
    print()
    print("  R9 is a COST, not a win: one tab in an uncited paragraph of the target now")
    print("  exits 2.  That is the price of default-deny, already paid by the two certified")
    print("  files, now paid by every declared target as well.  It is printed rather than")
    print("  buried because a re-baseline nobody expected is how a control stops being run.")
    print()
    surprises = [rid for rid, _l, _w, want, _f in M.ROWS if got[rid] != want]
    if surprises:
        print(f"  NOTE: {surprises} did not behave as predicted — read the rows above, not")
        print("  this paragraph.")
    print("=" * 90)
    return 0


if __name__ == "__main__":
    sys.exit(main())
