#!/usr/bin/env python3
"""mg-d3f3 -- the audit harness: a private copy of the tree that can be mutated.

WHAT THIS FILE IS FOR.  Every claim in this audit is of the form "apply input X
to the repository and row R does / does not go red".  That is only evidence if
the row is scored THE WAY THE REPOSITORY SCORES IT, so nothing here re-implements
a verdict: each construction is run through `verify_e35b.py` AS A SUBPROCESS and
the verdicts are read out of its printed `[PASS]`/`[FAIL]` lines and its exit
code.  A row this audit scored itself would be a third opinion about a
disagreement between two files, which is not what is being asked.

WHAT IS COPIED, AND WHY THE LAYOUT MATTERS.  `verify_e35b.py` computes
`PROBE = ../face_geometry` from its own `__file__`, imports `face_complex`,
`posets` and `controls` from there, and shells out to `python3 controls.py 5` in
that directory.  So the sandbox reproduces the two directories side by side
under one temporary root rather than copying files into one flat directory.

NOTHING UNDER `code/` IS WRITTEN TO.  Every mutation lands in the sandbox and
the sandbox is removed.  This is checked, not asserted: `sandbox_is_clean()`
compares the real tree's bytes before and after every construction.
"""

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.normpath(os.path.join(HERE, ".."))
PROBE = os.path.join(CODE, "face_geometry")
REPAIR = os.path.join(CODE, "face_geometry_repair_e35b")
EIGHT = os.path.join(CODE, "face_geometry_repair_8af0")

_ROW = re.compile(r"^\s*\[(PASS|FAIL)\]\s+(.*)$")

# The row names this audit refers to by short tag.  A row is identified by the
# PREFIX of its printed label, because the labels carry measured numbers in them
# and keying on the whole label would make every tag stale the moment a count
# moved -- which is the defect class this audit is about.
TAGS = {
    "V6a": "V6a ANCHORED",
    "V6b": "V6b CENSUS",
    "V6c": "V6c REGENERATED",
    "V6d": "V6d REACH",
    "V7":  "`le_to_facet` is corrupted at the SITE",
}


def digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def tree_digest(paths):
    return {p: digest(p) for p in paths if os.path.isfile(p)}


def real_tree_paths():
    out = []
    for d in (PROBE, REPAIR, EIGHT):
        for f in sorted(os.listdir(d)):
            if f.endswith(".py") or f.endswith(".txt") or f.endswith(".sh"):
                out.append(os.path.join(d, f))
    return out


class Sandbox(object):
    """A private copy of face_geometry/ + face_geometry_repair_e35b/ + 8af0/."""

    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="mgd3f3-")
        for src in (PROBE, REPAIR, EIGHT):
            dst = os.path.join(self.root, os.path.basename(src))
            os.makedirs(dst)
            for f in os.listdir(src):
                if f.endswith((".py", ".txt", ".sh")):
                    shutil.copy(os.path.join(src, f), os.path.join(dst, f))
        self.probe = os.path.join(self.root, "face_geometry")
        self.repair = os.path.join(self.root, "face_geometry_repair_e35b")
        self.eight = os.path.join(self.root, "face_geometry_repair_8af0")

    # -- reading and writing the copy ------------------------------------
    def read(self, rel):
        return open(os.path.join(self.root, rel)).read()

    def write(self, rel, text):
        open(os.path.join(self.root, rel), "w").write(text)

    def artifact(self):
        return self.read("face_geometry/controls_output.txt")

    def regenerate(self):
        """Run controls.py the way the repository does and store the output."""
        proc = subprocess.run([sys.executable, "controls.py", "5"],
                              cwd=self.probe, capture_output=True, text=True)
        self.write("face_geometry/controls_output.txt", proc.stdout)
        return proc.stdout, proc.returncode

    # -- running the repository's own scorers ----------------------------
    def verify(self):
        """Run verify_e35b.py.  Returns (exit code, {row prefix: bool}, stdout)."""
        proc = subprocess.run([sys.executable, "verify_e35b.py"],
                              cwd=self.repair, capture_output=True, text=True)
        rows = {}
        for line in proc.stdout.splitlines():
            m = _ROW.match(line)
            if m:
                rows[m.group(2)] = (m.group(1) == "PASS")
        return proc.returncode, rows, proc.stdout + proc.stderr

    def run_script(self, rel):
        d, f = os.path.split(rel)
        proc = subprocess.run([sys.executable, f],
                              cwd=os.path.join(self.root, d),
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


def row(rows, tag):
    """The verdict of the row whose label starts with TAGS[tag].

    Raises if no row matches or if more than one does.  A tag that silently
    matched nothing would report GREEN for an absent row, which is the shape of
    every defect this audit is looking for.
    """
    want = TAGS[tag]
    hits = [(k, v) for k, v in rows.items() if k.startswith(want)]
    if len(hits) != 1:
        raise KeyError("tag %r matched %d rows, not 1" % (tag, len(hits)))
    return hits[0][1]


def reds(rows):
    return sorted(k for k, v in rows.items() if not v)


class Report(object):
    """Printing with a running tally, and every printed count classified.

    `count(label, value, verdict, why)` is the only way a number reaches this
    audit's transcripts.  `verdict` is FORCED or COULD MOVE, in mg-e35b's own
    vocabulary, and mg-d3f3's PREDICTIONS.md P10a commits to using it, because an
    audit of an instrument that does not classify its own counts would be the
    instrument's defect wearing the auditor's coat.
    """

    def __init__(self, title):
        self.bad = []
        self.n = 0
        self.counts = []
        print(title)

    def check(self, label, ok, detail=""):
        self.n += 1
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                               ("  -- " + detail) if detail else ""))
        if not ok:
            self.bad.append(label)
        return ok

    def count(self, label, value, verdict, why):
        self.counts.append((label, value, verdict, why))
        print("    %-22s %-34s = %s  -- %s" % (verdict, label, value, why))

    def note(self, text):
        print("  %s" % text)

    def finish(self):
        print()
        if self.counts:
            forced = sum(1 for _, _, v, _ in self.counts if v.startswith("FORCED"))
            print("  %d printed counts, %d FORCED and named above.  This tally is "
                  "itself FORCED (it is a count of this file's own rows) and is "
                  "printed, not scored." % (len(self.counts), forced))
        if self.bad:
            print("%d checks, %d REFUTED:" % (self.n, len(self.bad)))
            for b in self.bad:
                print("  - %s" % b)
            return 1
        print("%d checks, 0 refuted." % self.n)
        return 0
