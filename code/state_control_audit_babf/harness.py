#!/usr/bin/env python3
"""mg-babf — the shared mutation harness for this audit.  MINE, not mg-7870's, not mg-2216's.

WHY A THIRD HARNESS EXISTS.  mg-2216 wrote one and mg-7870 re-ran it; a re-run of a
predecessor's battery establishes that the repair closes THAT battery and nothing more.
This one is written from the published behaviour of `delta_control.py` and shares no code
with either.  Its table parser, its region locator and its restore discipline are
independent, so where it agrees with mg-2216 the agreement is evidence and where it
disagrees the disagreement is a finding.

WHAT IT DOES.  It mutates `STATE.md` and `docs/state-history/README.md` IN THE WORKING
TREE, runs `code/state_landing_control_2da3/delta_control.py` as a subprocess, records the
exit code and which checks fired, and restores the two files from bytes held in memory
under a `finally` — then verifies the restore by sha256 against the bytes read at start.

SAFETY, because this harness edits tracked files:
  * it REFUSES to run if either file is already dirty in git;
  * every mutation is applied to the ORIGINAL snapshot, never stacked on a previous one;
  * restore happens in a `finally`, and a post-restore sha mismatch is a hard abort with
    the recovery command printed.

INSTRUMENT DISCIPLINE:
  * characters are `len(str)`, bytes are `len(bytes)`; nothing shells out to `wc`, which
    counts bytes under this box's LC_CTYPE and would agree with `wc -c` while both are
    wrong (mg-2da3's own note, and it is right).
  * every tally prints the population it was taken over; no head/tail/limit anywhere.
  * exit codes are read from the process, never inferred from stdout.
"""
import hashlib
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

STATE = "STATE.md"
README = "docs/state-history/README.md"
CONTROL = "code/state_landing_control_2da3/delta_control.py"

ROW_KEY = "mg-276d"
EDGE = " \t\r\n"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read(path):
    with open(os.path.join(REPO, path), "rb") as fh:
        return fh.read()


def write(path, text):
    with open(os.path.join(REPO, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def refuse_if_dirty():
    out = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--", STATE, README],
                         capture_output=True, text=True, check=True).stdout.strip()
    if out:
        print("REFUSING TO RUN — these files are already modified in the working tree:")
        print(out)
        print("This harness mutates and restores them; it will not run over your edits.")
        sys.exit(3)


# ---------------------------------------------------------------------------------------
# My own table parser.  Same escaped-pipe rule as the file's convention, written from the
# file, not copied: a cell boundary is a '|' not preceded by a backslash.
# ---------------------------------------------------------------------------------------
def row_fields(line):
    if not line.startswith("|"):
        return None
    bars = [i for i, ch in enumerate(line) if ch == "|" and (i == 0 or line[i - 1] != "\\")]
    if len(bars) < 2:
        return None
    return [(bars[k] + 1, bars[k + 1]) for k in range(len(bars) - 1)]


def certified_row(text, key=ROW_KEY):
    """(0-indexed line number, [(start,end) per field]) of the unique row carrying `key`.

    Keyed on the first two fields, which is where the ledger's verdict and attempt id live.
    """
    hits = []
    for n, line in enumerate(text.split("\n")):
        spans = row_fields(line)
        if not spans or len(spans) < 3:
            continue
        if any(key in line[s:e] for s, e in spans[:2]):
            hits.append((n, spans))
    if len(hits) != 1:
        raise AssertionError(f"key {key} matched {len(hits)} rows, expected 1")
    return hits[0]


def content_field(text, key=ROW_KEY):
    """(line no, start, end) of the certified row's WIDEST field — its content cell."""
    n, spans = certified_row(text, key)
    line = text.split("\n")[n]
    s, e = max(spans, key=lambda p: p[1] - p[0])
    return n, s, e


def edit_field(text, n, s, e, fn):
    lines = text.split("\n")
    line = lines[n]
    lines[n] = line[:s] + fn(line[s:e]) + line[e:]
    return "\n".join(lines)


def edit_cell(text, fn, key=ROW_KEY):
    """Apply `fn` to the certified row's content cell, PRESERVING its edge padding.

    The padding matters to the honesty of a mutation, not to the control: `N` strips the
    region's two ends, so padding cannot be what fires a digest.  But a mutation that
    incidentally also removes two spaces is not the mutation its description claims, and
    a reader is entitled to a character delta that is exactly the edit.
    """
    n, s, e = content_field(text, key)
    def repad(raw):
        core = raw.strip(EDGE)
        i = raw.find(core)
        return raw[:i] + fn(core) + raw[i + len(core):]
    return edit_field(text, n, s, e, repad)


# ---------------------------------------------------------------------------------------
# My own README block locator.  Same "run of blockquote lines" shape the control uses —
# it has to be, or I would be testing a different region — but written independently and
# returning a half-open [start, end) line range.
# ---------------------------------------------------------------------------------------
def quote_span(text, marker):
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if marker in l]
    if len(hits) != 1:
        raise AssertionError(f"marker matched {len(hits)} lines, expected 1: {marker!r}")
    i = hits[0]

    def q(k):
        return 0 <= k < len(lines) and lines[k].lstrip().startswith(">")

    s = i
    while q(s - 1):
        s -= 1
    e = i + 1
    while q(e):
        e += 1
    return s, e


def para_span(text, marker):
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if marker in l]
    if len(hits) != 1:
        raise AssertionError(f"marker matched {len(hits)} lines, expected 1: {marker!r}")
    i = hits[0]

    def b(k):
        return (0 <= k < len(lines) and lines[k].strip()
                and not lines[k].lstrip().startswith(">"))

    s = i
    while b(s - 1):
        s -= 1
    e = i + 1
    while b(e):
        e += 1
    return s, e


# markers into the regions delta_control.py certifies.  Chosen to match its own locators,
# because a mutation aimed at a region has to find the same region it does.
M_F1 = "**`no 4d tally` is a correction"
M_F2 = "**THOSE FIVE FIGURES WERE WRONG, here and in `57f962f`'s commit message"
M_A1 = "**`b68db5d`'s HEADLINE VERIFICATION SENTENCE IS BLIND TO THE CHANGE IT CERTIFIES"
M_A1_7870 = "DID NOT ESTABLISH WHAT THE BLOCK ABOVE CLAIMS"
M_B1A3 = "**`two commits before mg-34bf's parent` was off by one"
M_INDEX = "**`cell before` and `cell after` are measured at"


class Harness:
    """Snapshot, mutate, run, restore, verify."""

    def __init__(self):
        refuse_if_dirty()
        self.orig = {STATE: read(STATE), README: read(README)}
        self.sha0 = {p: sha(b) for p, b in self.orig.items()}
        self.rows = []

    def text(self, path):
        return self.orig[path].decode("utf-8")

    def run_control(self):
        p = subprocess.run([sys.executable, CONTROL], cwd=REPO,
                           capture_output=True, text=True)
        fired = [l.strip() for l in p.stdout.split("\n")
                 if l.strip().startswith("[FAIL]") or l.strip().startswith("[MOVED]")]
        return p.returncode, fired

    def restore(self):
        for path, b in self.orig.items():
            with open(os.path.join(REPO, path), "wb") as fh:
                fh.write(b)
        bad = [p for p in self.orig if sha(read(p)) != self.sha0[p]]
        if bad:
            print("!!! RESTORE FAILED for " + ", ".join(bad))
            print("!!! recover with:  git checkout -- " + " ".join(bad))
            sys.exit(4)

    def mutate(self, mid, kind, expect, description, edits):
        """`edits` maps path -> f(original text) -> mutated text.  Never stacked."""
        try:
            for path, fn in edits.items():
                write(path, fn(self.text(path)))
            deltas = {p: len(read(p).decode("utf-8")) - len(self.text(p))
                      for p in self.orig}
            rc, fired = self.run_control()
        finally:
            self.restore()
        caught = rc != 0
        verdict = ("CAUGHT" if caught else "SILENT")
        self.rows.append((mid, kind, expect, rc, verdict, description, fired))
        print(f"{mid}  [{kind}]  expect: {expect}")
        print(f"      {description}")
        print(f"      character delta: STATE.md {deltas[STATE]:+d}, "
              f"README {deltas[README]:+d}")
        print(f"      delta_control.py exit {rc}   "
              + (f"{verdict} ({'FAIL' if rc == 1 else 'MOVED'})" if caught
                 else "SILENT — exits 0, nothing fires"))
        for f in fired:
            print(f"        {f}")
        print()
        return rc

    def positive_control(self):
        rc, fired = self.run_control()
        print(f"POSITIVE CONTROL — clean tree: delta_control.py exit {rc}"
              + ("   as expected" if rc == 0 else "   *** NOT CLEAN ***"))
        print()
        return rc

    def summary(self, title):
        print("=" * 86)
        print(f"RESTORED — STATE.md sha {sha(read(STATE))[:16]} == {self.sha0[STATE][:16]}, "
              f"README sha {sha(read(README))[:16]} == {self.sha0[README][:16]}")
        print("=" * 86)
        print(f"SUMMARY — {title}")
        print("=" * 86)
        print(f"  {'id':<6}{'class':<22}{'expect':<11}{'exit':<6}verdict")
        miss = 0
        for mid, kind, expect, rc, verdict, _d, _f in self.rows:
            flag = ""
            if expect == "catch" and verdict == "SILENT":
                flag = "   <<< SILENT MISS"
                miss += 1
            elif expect == "tolerate" and verdict != "SILENT":
                flag = "   <<< NOISY"
            print(f"  {mid:<6}{kind:<22}{expect:<11}{rc:<6}{verdict}{flag}")
        catch = sum(1 for r in self.rows if r[2] == "catch")
        tol = sum(1 for r in self.rows if r[2] == "tolerate")
        noisy = sum(1 for r in self.rows if r[2] == "tolerate" and r[4] != "SILENT")
        print()
        print(f"  {len(self.rows)} mutations: {catch - miss} of {catch} expected-catch "
              f"CAUGHT, {miss} SILENT MISSES, {tol} expected-tolerate ({noisy} noisy)")
        return miss
