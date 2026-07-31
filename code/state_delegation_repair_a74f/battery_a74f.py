#!/usr/bin/env python3
"""mg-a74f — mg-16eb's OWN EIGHT ROWS, ON mg-16eb's OWN HARNESS, UNMODIFIED.

A repair that scores itself on a battery it wrote is worth nothing.  Nothing in
`code/state_delegation_audit_16eb/` is edited by this repair — `git diff` over that
directory is checked at the top of this file's own `run_all.sh` — and this file runs the
auditor's work in two ways, which answer two different questions:

    SECTION 1  `battery16eb.py` re-run AS A SUBPROCESS, verbatim, its output printed
               verbatim.  The question it answers is what the auditor's instrument says
               about the repaired tree, in the auditor's own words, scored against the
               auditor's own predicted exit codes.  A1 and A2 are predicted 0 there and are
               now 2, so that run is expected to print "6 of 8 behaved as this audit
               predicted; 2 did not" and to name them.  THAT LINE IS THE REPAIR.  mg-0049
               was reported the same way by mg-5644's Q1 and Q2 and the precedent is
               deliberate: the auditor's file is not edited to agree with the repair.

    SECTION 2  the same eight rows run through `harness16eb.Tree` directly, scored against
               THIS repair's predictions, which were committed in PREDICTIONS.md before any
               script of this repair existed.  Exit codes are read from the process by the
               auditor's harness, never inferred from its stdout — reading section 1's text
               to learn the codes would be exactly the inherited-verdict defect this arc
               keeps finding.

`harness16eb.Tree` refuses to run on a dirty tree, mutates from a snapshot, restores in a
`finally` and hard-aborts on a post-restore sha mismatch.  Run this on a committed tree.
"""
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
A16 = os.path.join(REPO, "code/state_delegation_audit_16eb")
sys.path.insert(0, A16)

import harness16eb as H              # noqa: E402
import mutations16eb as M            # noqa: E402

# What THIS repair predicted, in PREDICTIONS.md, before any script of it existed.  mg-16eb's
# own predictions stay where they are, in mutations16eb.ROWS, unedited.
PREDICTED = {"A1": 2, "A2": 2, "A3": 2, "A5": 2, "B1": 0, "B2": 2, "B3": 2, "C1": 1}

# The rows this repair deliberately does NOT move, and why, so a reader does not have to
# infer it from an unchanged number.
UNMOVED = {
    "B3": "under-fires: a page a reader is shown nothing of, at exit 2 (drift).  The "
          "exit-code table is narrowed to the state-set predicate and names this row; the "
          "predicate itself is not changed here.",
    "C1": "over-fires: a section a reader is shown every line of, at exit 1 printing "
          "'SHOWN NOTHING OF IT'.  Same narrowing, same reason.",
}


def section1():
    print("=" * 96)
    print("1.  mg-16eb's OWN BATTERY, RE-RUN AS A SUBPROCESS, VERBATIM")
    print("=" * 96)
    diff = subprocess.run(["git", "-C", REPO, "diff", "HEAD", "--stat", "--",
                           "code/state_delegation_audit_16eb/"],
                          capture_output=True, text=True).stdout.strip()
    clean = "0 bytes — the auditor's files are not edited by this repair"
    print(f"    git diff over code/state_delegation_audit_16eb/: {diff or clean}")
    print()
    proc = subprocess.run([sys.executable,
                           os.path.join(A16, "battery16eb.py")],
                          cwd=REPO, capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    if proc.stderr.strip():
        sys.stdout.write("--- stderr ---\n" + proc.stderr)
    print(f"    (battery16eb.py exited {proc.returncode})")
    print()
    return proc.returncode


def section2():
    print("=" * 96)
    print("2.  THE SAME EIGHT ROWS, SCORED AGAINST THIS REPAIR'S OWN COMMITTED PREDICTIONS")
    print("=" * 96)
    print("    Exit codes read from the process by harness16eb.Tree, not from section 1's")
    print("    stdout.  mutations16eb.py is imported unmodified; only the scoring column is")
    print("    this repair's.")
    print()
    tree = H.Tree([M.ATTEMPT, M.CONTROL])
    got, surprises = {}, []
    for rid, surface, what, mg16_want, rel, fn in M.ROWS:
        code = tree.run_mutated({rel: fn(tree.orig[rel])})
        got[rid] = code
        want = PREDICTED[rid]
        if code != want:
            surprises.append((rid, want, code))
        print(f"  {'OK ' if code == want else '!! '} {rid:<4s} {surface:<24s} "
              f"{what:<62s} mg-16eb predicted {mg16_want}   mg-a74f predicted {want}   "
              f"got {H.VERDICT[code]}")
    print()
    print(f"  {len(M.ROWS)} rows run; {len(M.ROWS) - len(surprises)} behaved as THIS REPAIR "
          f"predicted; {len(surprises)} did not.")
    for rid, want, code in surprises:
        print(f"    {rid}  predicted exit {want}, got exit {code}")
    print()
    moved = [rid for rid, _s, _w, mg16_want, _r, _f in M.ROWS if got[rid] != mg16_want]
    print(f"  ROWS THIS REPAIR MOVED, against mg-16eb's observations at bd24efc: "
          f"{moved or '(none)'}")
    for rid, _s, what, mg16_want, _r, _f in M.ROWS:
        if got[rid] != mg16_want:
            print(f"    {rid}  {what}")
            print(f"         exit {mg16_want} -> exit {got[rid]}: the second pinned table is "
                  f"now iterated and cross-checked at both grains")
    print()
    print("  ROWS THIS REPAIR DELIBERATELY DID NOT MOVE:")
    for rid, why in UNMOVED.items():
        print(f"    {rid}  exit {got[rid]}, unchanged.  {why}")
    print()
    return got, surprises


def main():
    print("=" * 96)
    print("mg-a74f — THE AUDITOR'S BATTERY, UNMODIFIED, ON THE REPAIRED TREE")
    print("=" * 96)
    print()
    rc = section1()
    got, surprises = section2()
    print("=" * 96)
    print("WHAT THESE TWO SECTIONS SAY TOGETHER")
    print("=" * 96)
    print("  Section 1 is the auditor's own instrument reporting on the party it audited,")
    print("  with not a byte of it edited.  Section 2 is this repair's prediction column")
    print("  over the same eight processes.  A1 and A2 are the two rows that move, from")
    print("  exit 0 to exit 2, and they are the two rows mg-16eb built to show that the")
    print("  sentence 'the two tables cannot drift apart quietly in either direction' was")
    print("  true in one direction only.")
    print()
    print("  B3 and C1 do not move, and that is stated in advance rather than discovered:")
    print("  they refute what the exit-code TABLE said, in opposite directions, and this")
    print("  repair narrows the table to the predicate the code applies instead of changing")
    print("  the predicate.  Changing it would move the classification of every delegated")
    print("  section; it is named as open, here and in delta_control.py's own header.")
    print()
    print(f"  battery16eb.py exited {rc}; "
          f"{len(M.ROWS) - len(surprises)} of {len(M.ROWS)} rows behaved as this repair "
          f"predicted.")
    print("=" * 96)
    return 1 if surprises else 0


if __name__ == "__main__":
    sys.exit(main())
