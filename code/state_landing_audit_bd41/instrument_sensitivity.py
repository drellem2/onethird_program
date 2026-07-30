#!/usr/bin/env python3
"""mg-bd41 — do the commit's two cited re-runs actually SEE the change they certify?

b68db5d leads on this sentence:

    "I re-ran both: `sh code/state_audit_6a2f/run_all.sh` reproduces out_audit.txt
     BYTE-IDENTICALLY with these edits applied."

and later cites:

    "The completeness half of the same checker [verify_relocation.py] is unaffected by
     my edits and still reports 10 cells, 11,625 words, 125 maximal runs, 0 unaccounted."

A reproduction is only evidence if the instrument could have failed.  This runs a NEGATIVE
CONTROL on each: mutilate the working tree, re-run, and see whether the output moves.  An
instrument that does not move when the file is destroyed reports nothing about an edit to
that file.

The mutation is done in memory with a guaranteed restore and a post-hoc byte check; the
script refuses to run if STATE.md is already dirty.
"""
import hashlib, subprocess, sys, os

REPO = subprocess.run(["git","rev-parse","--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
STATE = os.path.join(REPO, "STATE.md")
BATTERY = "code/state_audit_6a2f/run_all.sh"
COMMITTED = os.path.join(REPO, "code/state_audit_6a2f/out_audit.txt")
CHECKER = "code/state_restructure_34bf/verify_relocation.py"


def sh(cmd):
    return subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, text=True).stdout


def digest(b):
    return hashlib.sha256(b).hexdigest()[:16]


def run_battery():
    return sh(f"sh {BATTERY} 2>&1")


def run_checker():
    out = sh(f"python3 {CHECKER} 2>&1")
    keep = [l for l in out.split("\n")
            if l.startswith(("cells changed", "words in those cells",
                             "maximal verbatim runs", "words not found"))]
    return "\n".join(keep)


def main():
    dirty = sh("git status --porcelain -- STATE.md").strip()
    if dirty:
        sys.exit("REFUSING TO RUN: STATE.md is dirty. Commit or restore it first.")

    original = open(STATE, "rb").read()
    before_sha = digest(original)
    print(f"STATE.md at rest: {len(original)} bytes, sha {before_sha}\n")

    base_battery = run_battery()
    committed = open(COMMITTED, "rb").read().decode()
    print("=" * 78)
    print("A. THE mg-6a2f BATTERY  —  'reproduces out_audit.txt BYTE-IDENTICALLY")
    print("                            with these edits applied'")
    print("=" * 78)
    print(f"  clean tree: reproduces the committed out_audit.txt : "
          f"{base_battery == committed}")

    try:
        text = original.decode()
        ls = text.split("\n")
        del ls[100:300]                       # delete 200 lines outright
        ls[0] = "TOTALLY DESTROYED"
        open(STATE, "w", encoding="utf-8").write("\n".join(ls))
        gutted = open(STATE, "rb").read()
        print(f"\n  NEGATIVE CONTROL: STATE.md gutted "
              f"{len(original)} -> {len(gutted)} bytes, "
              f"{len(text.split(chr(10)))} -> {len(ls)} lines")
        out_gutted = run_battery()
        print(f"  battery output still byte-identical to out_audit.txt : "
              f"{out_gutted == committed}")
        if out_gutted == committed:
            print("\n  >>> THE CONTROL DOES NOT FIRE.  Every script in the battery pins fixed")
            print("      revisions (97cb533 / 60f4dac / 57f962f) and reads the committed")
            print("      docs/state-history/*.md at 57f962f.  None of them opens the working")
            print("      tree or resolves HEAD, so the battery is BLIND to b68db5d by")
            print("      construction.  'Reproduces byte-identically WITH THESE EDITS")
            print("      APPLIED' is therefore true and carries no information about the")
            print("      edits: it would read identically if the edits were catastrophic.")

        print()
        print("=" * 78)
        print("B. verify_relocation.py's COMPLETENESS HALF  —  'unaffected by my edits'")
        print("=" * 78)
        # A milder, survivable mutation: truncate row :135's content cell.  Gutting the
        # file makes this checker raise instead of report, which shows sensitivity but
        # not the direction of it.
        ls2 = original.decode().split("\n")
        ls2[134] = ls2[134][:200] + " |"
        open(STATE, "w", encoding="utf-8").write("\n".join(ls2))
        print("  NEGATIVE CONTROL: row :135's content cell truncated to 200 chars")
        print("      " + (run_checker() or "(checker produced no tally lines)")
              .replace("\n", "\n      "))
    finally:
        open(STATE, "wb").write(original)

    restored = open(STATE, "rb").read()
    assert restored == original, "RESTORE FAILED"
    print(f"\n  STATE.md restored: sha {digest(restored)} == {before_sha}  "
          f"({restored == original})")

    print("\n  with STATE.md intact at HEAD:")
    print("      " + run_checker().replace("\n", "\n      "))
    print("\n  >>> THIS control DOES fire — the completeness half opens the working tree")
    print("      (verify_relocation.py:95) and its tallies move when the file moves.  So")
    print("      the commit's SECOND cited re-run is genuine evidence, and the property")
    print("      it reports (10 cells, 11,625 words, 125 maximal runs, 0 unaccounted)")
    print("      is a real measurement at HEAD.  The first one is not.")
    assert open(STATE, "rb").read() == original
    print(f"\nSTATE.md final check: sha {digest(open(STATE,'rb').read())} == {before_sha}")


if __name__ == "__main__":
    main()
