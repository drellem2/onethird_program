#!/usr/bin/env python3
"""mg-16eb — the mutation harness for this audit.  MINE: the sixth in this lineage.

WHY A SIXTH HARNESS AND NOT mg-5644's.  This audit's brief says an inherited layer verdict
is the pinned-input defect this lineage suffered at generation one, and a harness is an
inherited verdict about *how a row is scored*.  mg-5644 argued the same way and built its
own.  So this file shares no code with `harness218d.py`, `harness5644.py` or
`battery_0049.py`: its own snapshot, its own restore discipline, its own exit-code reader.
Where it agrees with them the agreement is evidence.  mg-5644's and mg-218d's own batteries
are ALSO re-run here, unmodified, on their own harnesses, and those runs are separate files.

WHAT IT ADDS TO THE FIVE BEFORE IT.  It can mutate the INSTRUMENT as well as the documents.
mg-0049 added a second pinned table to `delta_control.py` (`DELEGATED_PRESENTATION`) and
published a precise claim about how the two tables are kept in step; a claim about the
instrument can only be tested by mutating the instrument.  `Tree` therefore takes any set of
tracked files, `delta_control.py` included, and every mutation is computed from the ORIGINAL
snapshot so no row can stack on another.

SAFETY, unchanged in substance from mg-5644's because it was right:
  * refuses to run if any file it is about to mutate is already dirty in git;
  * mutations are always computed from the original snapshot, never from a mutated tree;
  * restore is in a `finally` and a post-restore sha256 mismatch is a hard abort;
  * an anchor that does not match exactly once is a loud LookupError, never a silent no-op.

INSTRUMENT DISCIPLINE (this cluster's):
  * exit codes are read from the process, never inferred from stdout;
  * every row carries THE EXIT CODE PREDICTED BEFORE THE RUN, written into `mutations16eb.py`
    and committed before `battery16eb.py` was executed for the first time;
  * every tally prints the population it was taken over; no head/tail/limit anywhere.
"""
import hashlib
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

STATE = "STATE.md"
ATTEMPT = "docs/state-history/attempt-mg-276d.md"
CONTROL = "code/state_landing_control_2da3/delta_control.py"

PASS, FAIL, MOVED = 0, 1, 2
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
    return [line[3:].strip() for line in out.splitlines() if line.strip()]


def once(text, needle):
    """`needle` must occur exactly once in `text`.  A mutation keyed on an anchor that has
    rotted must be a loud failure, never a mutation that silently changes nothing."""
    n = text.count(needle)
    if n != 1:
        raise LookupError(f"anchor matched {n} times, need exactly 1: {needle[:70]!r}")
    return text


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

    def run_mutated(self, changes, capture=False):
        """Apply `changes` (rel -> new text), run the control, restore, return the exit
        code — or (code, stdout) when `capture` is set, which is how a row that is about
        the control's own WORDING rather than its exit code is evidenced."""
        touched = list(changes)
        try:
            for rel, text in changes.items():
                if rel not in self.orig:
                    raise AssertionError(f"{rel} is not in this Tree's snapshot")
                if text == self.orig[rel]:
                    raise AssertionError(f"{rel}: mutation is a no-op — it tests nothing")
                write(rel, text)
            proc = subprocess.run([sys.executable, path(CONTROL)], cwd=REPO,
                                  capture_output=True, text=True)
            return (proc.returncode, proc.stdout) if capture else proc.returncode
        finally:
            for rel in touched:
                write(rel, self.orig[rel])
                if sha(read(rel)) != self.sha0[rel]:
                    raise SystemExit(
                        f"HARD ABORT: {rel} did not restore.  Recover with:\n"
                        f"    git -C {REPO} checkout -- {rel}")

    def battery(self, rows, title, note=""):
        """rows: (id, surface, description, predicted exit, fn(orig snapshot) -> changes).

        Prints one line per row and returns {id: observed exit code}."""
        print("=" * 96)
        print(title)
        print("'expected' is what THIS AUDIT PREDICTED BEFORE THE RUN, written into")
        print("mutations16eb.py and committed before battery16eb.py was executed once.")
        if note:
            print(note)
        print("=" * 96)
        got, surprises = {}, []
        for rid, surface, what, want, fn in rows:
            code = self.run_mutated(fn(self.orig))
            got[rid] = code
            if code != want:
                surprises.append((rid, want, code))
            print(f"  {'OK ' if code == want else '!! '} {rid:<5s} {surface:<24s} "
                  f"{what:<62s} expected exit {want}    got {VERDICT[code]}")
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
