#!/usr/bin/env python3
"""mg-218d — the mutation harness for this audit.  MINE: not mg-2216's, not mg-babf's.

WHY A FOURTH HARNESS.  mg-2216 wrote one, mg-babf wrote a second from mg-7870's published
prose, and mg-4acd re-ran both unmodified.  Re-running a predecessor's battery establishes
that the repair closes THAT battery — and after two repairs those batteries are the
author's KNOWN-ANSWER SET.  This one is written from `delta_control.py`'s published
behaviour and shares no code with any of the three: its own locator, its own restore
discipline, its own exit-code reader.  Where it agrees with them the agreement is
evidence; where it disagrees the disagreement is a finding.

WHAT IT DOES.  It writes mutated bytes over any set of tracked files in the WORKING TREE,
runs a command as a subprocess, records the exit code and stdout, and restores every file
it touched from bytes held in memory under a `finally`, verifying the restore by sha256.

SAFETY, because this edits tracked files:
  * it REFUSES to run if any file it is about to mutate is already dirty in git;
  * every mutation is computed from the ORIGINAL snapshot, never stacked on a previous one;
  * restore is in a `finally`, and a post-restore sha mismatch is a hard abort with the
    recovery command printed.

INSTRUMENT DISCIPLINE (this cluster's, adopted deliberately):
  * characters are `len(str)`, bytes are `len(bytes)`; nothing shells out to `wc`;
  * every tally prints the population it was taken over; no head/tail/limit anywhere;
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
PRESENTATION = "code/state_landing_control_2da3/presentation.py"
COVERAGE = "code/state_landing_control_2da3/COVERAGE.md"

FAIL, MOVED = 1, 2
VERDICT = {0: "exit 0 (PASS)", 1: "exit 1 (FAIL)", 2: "exit 2 (MOVED)"}


def path(rel):
    return os.path.join(REPO, rel)


def read(rel):
    with open(path(rel), "rb") as fh:
        return fh.read()


def write(rel, data):
    with open(path(rel), "wb") as fh:
        fh.write(data)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dirty(rels):
    """The subset of `rels` that git reports as modified in the working tree."""
    out = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--"] + list(rels),
                         capture_output=True, text=True, check=True).stdout
    return [l[3:].strip() for l in out.splitlines() if l.strip()]


def run(cmd):
    """(exit code, stdout+stderr) of `cmd` run from the repo root."""
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def control_cmd():
    return [sys.executable, CONTROL]


class Tree:
    """A snapshot of the files a battery is allowed to mutate, with restore discipline."""

    def __init__(self, rels):
        self.rels = list(rels)
        already = dirty(self.rels)
        if already:
            raise SystemExit(
                "REFUSING TO RUN: these files are already modified in the working tree:\n  "
                + "\n  ".join(already)
                + "\n(this harness restores from bytes read at start; it will not run on a "
                  "dirty tree, because a crash would then restore the wrong bytes.)")
        self.orig = {r: read(r) for r in self.rels}
        self.sha0 = {r: sha(v) for r, v in self.orig.items()}

    def text(self, rel):
        return self.orig[rel].decode("utf-8")

    def probe(self, edits, cmd=None):
        """Apply `edits` ({rel: str}), run `cmd`, restore, return (code, output).

        Every edit is computed by the caller from `self.text(...)`, i.e. from the ORIGINAL
        snapshot.  Nothing stacks.
        """
        for rel in edits:
            if rel not in self.orig:
                raise SystemExit(f"harness: {rel} was not snapshotted; refusing to mutate it")
        try:
            for rel, new in edits.items():
                write(rel, new.encode("utf-8"))
            return run(cmd or control_cmd())
        finally:
            self.restore()

    def restore(self):
        bad = []
        for rel, data in self.orig.items():
            write(rel, data)
            if sha(read(rel)) != self.sha0[rel]:
                bad.append(rel)
        if bad:
            raise SystemExit(
                "RESTORE FAILED for: " + ", ".join(bad)
                + "\nrecover with:  git -C " + REPO + " checkout -- " + " ".join(bad))


# -----------------------------------------------------------------------------------------
# My own locator.  Independent of delta_control.py's quote_block/paragraph and of the two
# earlier harnesses': written from the published rule, not copied from any of them.
# -----------------------------------------------------------------------------------------
def marker_line(text, marker):
    hits = [i for i, l in enumerate(text.split("\n")) if marker in l]
    if len(hits) != 1:
        raise LookupError(f"marker matched {len(hits)} lines, need exactly 1: {marker!r}")
    return hits[0]


def quote_span(text, marker):
    """[first, last) of the maximal blockquote run containing `marker` (0-based)."""
    lines = text.split("\n")
    i = marker_line(text, marker)

    def q(k):
        return 0 <= k < len(lines) and lines[k].lstrip().startswith(">")

    if not q(i):
        raise LookupError("marker line is not a blockquote line")
    s, e = i, i + 1
    while q(s - 1):
        s -= 1
    while q(e):
        e += 1
    return s, e


def row_index(text, key):
    """0-based line index of the single ledger row whose first cell carries `key`."""
    hits = []
    for i, line in enumerate(text.split("\n")):
        if not line.startswith("|"):
            continue
        bounds = [j for j, ch in enumerate(line) if ch == "|" and (j == 0 or line[j - 1] != "\\")]
        if len(bounds) < 2:
            continue
        first = line[bounds[0] + 1:bounds[1]]
        if key in first:
            hits.append(i)
    if len(hits) != 1:
        raise LookupError(f"key {key} matched {len(hits)} rows, need exactly 1")
    return hits[0]


def report(rows, title, note=""):
    """Print a battery table.  Columns: id, layer, expectation, verdict, agreement."""
    print("=" * 90)
    print(title)
    if note:
        print(note)
    print("=" * 90)
    w = max(len(r["desc"]) for r in rows)
    for r in rows:
        mark = "OK " if r["agrees"] else ">>>"
        print(f"  {mark} {r['id']:<5} {r['layer']:<22} {r['desc']:<{w}}  "
              f"expected {r['expect']:<9} got {VERDICT[r['code']] if r['code'] in VERDICT else 'exit ' + str(r['code'])}")
    print()
    agree = sum(1 for r in rows if r["agrees"])
    print(f"  {agree} of {len(rows)} mutations behaved as this audit predicted; "
          f"{len(rows) - agree} did not.")
    return rows
