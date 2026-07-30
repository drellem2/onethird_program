#!/usr/bin/env python3
"""mg-16eb — DOES mg-0049's COMMITTED EVIDENCE REPRODUCE?  Re-run it and diff the bytes.

A committed `out_*.txt` is a claim about what a program printed.  This audit's brief says an
inherited verdict is the pinned-input defect this lineage suffered at generation one, and
reading a committed output IS inheriting a verdict.  So every one of the seven evidence files
mg-0049's two commits added or changed is regenerated here by running the producer named in its own directory's README, and
compared BYTE FOR BYTE against the committed copy.  sha256 of both is printed on every row,
so a reader can check the comparison rather than take it.

This is the check that catches a fabricated figure, and mg-0049's own evidence commit records
that its first draft had one (out_control.txt regenerated from delta_control.py alone when it
is run_all.sh's output, dropping the NC1..NC10 rows).  That defect was caught by mg-218d's
coverage218d.py.  Nothing catches the same defect in the other six files, which is why this
file runs all seven.

~10 min.  Sections that mutate the working tree do so through the producing script's own
restore discipline; nothing here writes to a tracked file itself.  Three of the seven need the
renderers (see run_all.sh's header); without them those two rows report the producer's
exit 3 and are counted as NOT REPRODUCED, never as reproduced.
"""
import hashlib
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

R0049 = "code/state_delegation_repair_0049"
CTL = "code/state_landing_control_2da3"

# (committed file, how to produce it, needs the renderers)
ROWS = [
    (f"{R0049}/out_battery_0049.txt",
     [sys.executable, f"{R0049}/battery_0049.py"], False),
    (f"{R0049}/out_split.txt",
     [sys.executable, f"{R0049}/split_0049.py"], False),
    (f"{R0049}/out_coverage218d.txt",
     [sys.executable, "code/state_layer_audit_218d/coverage218d.py"], False),
    (f"{R0049}/out_selftest_negative.txt", None, False),   # composite; see below
    (f"{R0049}/out_render.txt",
     [sys.executable, f"{R0049}/render0049.py"], True),
    (f"{R0049}/out_5644_rerun.txt",
     ["sh", "code/state_delegation_audit_5644/run_all.sh"], True),
    (f"{CTL}/out_control.txt",
     ["sh", f"{CTL}/run_all.sh"], True),
]

# out_selftest_negative.txt is the two self-tests concatenated, in the order run_all.sh runs
# them.  Reconstructed rather than guessed: if the reconstruction is wrong the row reports
# NOT REPRODUCED and says so, which is the honest outcome for a file whose producer is a
# shell pipeline rather than one script.
COMPOSITE = [[sys.executable, f"{CTL}/presentation.py"],
             [sys.executable, f"{CTL}/negative_control.py"]]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(cmd):
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    return p.stdout + p.stderr, p.returncode


def main():
    print("=" * 96)
    print("mg-16eb — mg-0049's COMMITTED EVIDENCE, REGENERATED AND DIFFED BYTE FOR BYTE")
    print("=" * 96)
    print(f"population: all {len(ROWS)} out_*.txt files mg-0049's two commits added or "
          f"changed.")
    print()
    same = 0
    for rel, cmd, _needs in ROWS:
        with open(os.path.join(REPO, rel), "rb") as fh:
            committed = fh.read()
        if cmd is None:
            parts = []
            for c in COMPOSITE:
                text, _rc = run(c)
                parts.append(text)
            # run_all.sh puts a bare `echo` between the two sections.
            out = "\n".join(parts)
        else:
            out, _rc = run(cmd)
        produced = out.encode("utf-8")
        ok = produced == committed
        same += ok
        print(f"  [{'IDENTICAL' if ok else 'DIFFERS  '}] {rel}")
        print(f"              committed sha256 {sha(committed)}  {len(committed):>7} bytes")
        print(f"              produced  sha256 {sha(produced)}  {len(produced):>7} bytes")
        if not ok:
            cl, pl = committed.decode().splitlines(), produced.decode().splitlines()
            print(f"              {len(cl)} committed lines vs {len(pl)} produced; first "
                  f"differing line:")
            for i in range(max(len(cl), len(pl))):
                a = cl[i] if i < len(cl) else "(absent)"
                b = pl[i] if i < len(pl) else "(absent)"
                if a != b:
                    print(f"                {i + 1}  committed: {a[:90]}")
                    print(f"                {i + 1}  produced : {b[:90]}")
                    break
    print()
    print("=" * 96)
    print(f"{same} of {len(ROWS)} of mg-0049's committed evidence files reproduce "
          f"BYTE-IDENTICALLY")
    print("from this audit's own runs.")
    if same == len(ROWS):
        print("0 figures in this repair are unreproduced.")
    else:
        print(f"{len(ROWS) - same} did NOT reproduce; read the rows above, not this line.")
    print("=" * 96)
    return 0 if same == len(ROWS) else 1


if __name__ == "__main__":
    sys.exit(main())
