#!/usr/bin/env python3
"""mg-5644 — the mutation harness for this audit.  MINE: not mg-218d's, not mg-bee1's.

WHY A FIFTH HARNESS.  mg-bee1 ran its seven new mutations on `harness218d.py` and argued —
correctly — that using the auditor's harness rather than a fifth one of its own is the
stronger choice for a party under test.  The reverse holds for an AUDITOR.  This audit's
brief says an inherited verdict is the pinned-input defect this lineage already suffered
once, so nothing here imports mg-218d's harness or mg-bee1's battery: its own snapshot, its
own restore discipline, its own exit-code reader.  Where it agrees with them the agreement
is evidence; mg-218d's sixteen are ALSO re-run unmodified, on mg-218d's own harness, and
that run is a separate file.

WHAT IT DOES.  Writes mutated bytes over tracked files in the WORKING TREE, runs the
control as a subprocess, records the exit code, and restores every file it touched from
bytes held in memory under a `finally`, verifying the restore by sha256.

SAFETY:
  * refuses to run if any file it is about to mutate is already dirty in git;
  * every mutation is computed from the ORIGINAL snapshot, never stacked on a previous one;
  * restore is in a `finally`, and a post-restore sha mismatch is a hard abort.

INSTRUMENT DISCIPLINE (this cluster's):
  * characters are `len(str)`, bytes are `len(bytes)`; nothing shells out to `wc`;
  * every tally prints the population it was taken over; no head/tail/limit anywhere;
  * exit codes are read from the process, never inferred from stdout;
  * every row carries THE EXIT CODE PREDICTED BEFORE THE RUN — mg-218d's discipline, kept.
"""
import hashlib
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

STATE = "STATE.md"
README = "docs/state-history/README.md"
ATTEMPT = "docs/state-history/attempt-mg-276d.md"
CONTROL = "code/state_landing_control_2da3/delta_control.py"

FAIL, MOVED = 1, 2
VERDICT = {0: "exit 0 (PASS)", 1: "exit 1 (FAIL)", 2: "exit 2 (MOVED)"}


def path(rel):
    return os.path.join(REPO, rel)


def read(rel):
    with open(path(rel), "r", encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    with open(path(rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def dirty(rels):
    out = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--"] + list(rels),
                         capture_output=True, text=True, check=True).stdout
    return [l[3:].strip() for l in out.splitlines() if l.strip()]


class Tree:
    """A snapshot of the files a battery may mutate, plus a restoring runner."""

    def __init__(self, rels):
        self.rels = list(rels)
        bad = dirty(self.rels)
        if bad:
            raise SystemExit(
                "REFUSING TO RUN: these files are already dirty in the working tree, so a\n"
                "crash would restore the wrong bytes: " + ", ".join(bad))
        self.orig = {r: read(r) for r in self.rels}
        self.sha0 = {r: sha(self.orig[r]) for r in self.rels}

    def run_mutated(self, changes):
        """Apply `changes` (rel -> new text) computed from the ORIGINAL snapshot, run the
        control, restore.  Returns the control's exit code."""
        touched = list(changes)
        try:
            for rel, text in changes.items():
                if text == self.orig[rel]:
                    raise AssertionError(f"{rel}: mutation is a no-op — it would test nothing")
                write(rel, text)
            p = subprocess.run([sys.executable, path(CONTROL)], cwd=REPO,
                               capture_output=True, text=True)
            return p.returncode
        finally:
            for rel in touched:
                write(rel, self.orig[rel])
                if sha(read(rel)) != self.sha0[rel]:
                    raise SystemExit(
                        f"HARD ABORT: {rel} did not restore.  Recover with:\n"
                        f"    git -C {REPO} checkout -- {rel}")

    def battery(self, rows, title, note=""):
        """rows: (id, layer, description, predicted exit, fn(orig snapshot) -> changes).

        Prints one line per row and returns the observed exit codes."""
        print("=" * 90)
        print(title)
        print("'expected' is what THIS AUDIT PREDICTED BEFORE THE RUN, written into this "
              "file before it was executed.")
        if note:
            print(note)
        print("=" * 90)
        got, surprises = {}, []
        for rid, layer, what, want, fn in rows:
            code = self.run_mutated(fn(self.orig))
            got[rid] = code
            ok = "OK " if code == want else "!! "
            if code != want:
                surprises.append((rid, want, code))
            print(f"  {ok} {rid:<5s} {layer:<22s} {what:<58s} "
                  f"expected exit {want}    got {VERDICT[code]}")
        print()
        print(f"  {len(rows)} of {len(rows)} rows run; "
              f"{len(rows) - len(surprises)} behaved as this audit predicted; "
              f"{len(surprises)} did not.")
        if surprises:
            print("\n  MUTATIONS THAT SURPRISED THIS AUDIT (predicted != observed):")
            for rid, want, code in surprises:
                print(f"    {rid}  predicted exit {want}, got exit {code}")
        print()
        return got
