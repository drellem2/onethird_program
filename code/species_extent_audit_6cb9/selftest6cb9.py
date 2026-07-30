"""SELF-TEST for mg-6cb9's instrument.

The probe harness in this tree mutates THE REAL WORKTREE.  That buys fidelity
-- every checker runs against a live `.git`, so `s1_extent.py`'s two historical
controls are armed, which they are not in the sandbox mg-d633's own E3 uses --
and it costs safety, so the safety is asserted here rather than assumed.

Roughly half of these assertions are that something does NOT happen: the
restore leaves nothing behind, the mutation helper refuses to no-op, the
bytecode cache does not survive a restore.  A self-test that only ever
confirms the happy path is the vacuous check this whole arc is about.

    python3 code/species_extent_audit_6cb9/selftest6cb9.py
"""

import os
import re
import subprocess
import sys
import tempfile

from kern6cb9 import (REPO, git_status, Probe, run_checker, plant,
                      replace_once, flat, norm_toks, purge_pycache)

n = bad = 0


def ck(label, cond):
    global n, bad
    n += 1
    bad += (not cond)
    print("  %-66s %s" % (label[:66], "ok" if cond else "*** FAILED ***"))


print("=" * 78)
print("selftestd6cb9 -- the harness, and the half of it that must NOT happen")
print("=" * 78)
print()

BASE = git_status()
DOC = "docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md"
TMPREL = "code/species_extent_audit_6cb9/_selftest_scratch.md"
SUBREL = "code/species_extent_audit_6cb9/_sub/_leak.md"

print("  1  the restore contract")
p = os.path.join(REPO, DOC)
before = open(p, encoding="utf-8").read()
with Probe([(DOC, plant("\n\nprobe text\n"))]):
    during = open(p, encoding="utf-8").read()
after = open(p, encoding="utf-8").read()
ck("a plant CHANGES the file while the probe is open", during != before)
ck("and the file is byte-identical afterwards", after == before)
ck("git status is unchanged afterwards", git_status() == BASE)

print()
print("  2  new files and new directories, and that they do NOT survive")
with Probe([(TMPREL, lambda _o: "created\n")]):
    ck("a new file exists inside the probe",
       os.path.exists(os.path.join(REPO, TMPREL)))
ck("and is GONE afterwards", not os.path.exists(os.path.join(REPO, TMPREL)))
with Probe([(SUBREL, lambda _o: "created\n")]):
    ck("a new file in a new SUBDIRECTORY exists inside the probe",
       os.path.exists(os.path.join(REPO, SUBREL)))
ck("the file is gone afterwards", not os.path.exists(os.path.join(REPO,
                                                                 SUBREL)))
ck("and so is the directory it needed",
   not os.path.isdir(os.path.dirname(os.path.join(REPO, SUBREL))))
ck("git status is still unchanged", git_status() == BASE)

print()
print("  3  the mutation helper refuses to do nothing")
try:
    with Probe([(DOC, replace_once("a string that is not in the document",
                                   "x"))]):
        pass
    raised = False
except AssertionError:
    raised = True
ck("replace_once RAISES when its target is absent", raised)
ck("the tree survived that raise", git_status() == BASE)
with Probe([(DOC, replace_once("Bell(n)", "BELL(n)"))]):
    text = open(p, encoding="utf-8").read()
    ck("replace_once changes exactly ONE occurrence",
       text.count("BELL(n)") == 1)
ck("and it is undone", open(p, encoding="utf-8").read() == before)

print()
print("  4  a restored .py must not leave live bytecode behind")
print("     (this is the defect that inverted A3d's seam probe, kept in")
print("     OUTCOMES.md; the source and the mutant are the same SIZE and the")
print("     restore lands in the same SECOND, so the .pyc validates)")
KERN = "code/species_extent_d633/kernd633.py"
purge_pycache()
with Probe([(KERN, replace_once("RUN_FRAC = 0.50", "RUN_FRAC = 2.00"))]):
    c_dis, _ = run_checker("code/species_extent_d633/e2_crosssection.py")
c_ok, out_ok = run_checker("code/species_extent_d633/e2_crosssection.py")
pyc = os.path.join(REPO, "code/species_extent_d633/__pycache__")
ck("disarming RUN_FRAC makes e2 red (its own controls catch it)", c_dis == 1)
ck("and e2 is green again immediately after the restore", c_ok == 0)
ck("no __pycache__ survives the probe",
   not os.path.isdir(pyc) or not os.listdir(pyc))
ck("the run after the restore reports its controls firing",
   "fires, 1 finding -- ok" in out_ok)

print()
print("  5  the checkers are green on the tree as found")
for rel in ["code/species_repair_6f61/check_doc.py",
            "code/species_remainder_f8fa/w3_scope.py",
            "code/species_repair_a4ef/s1_extent.py",
            "code/species_repair_a4ef/s2_seam.py",
            "code/species_extent_d633/e1_extents.py",
            "code/species_extent_d633/e2_crosssection.py"]:
    c, _ = run_checker(rel)
    ck("%s exits 0 unmutated" % os.path.basename(rel), c == 0)

print()
print("  6  s1_extent.py's historical controls are ARMED here")
c, out = run_checker("code/species_repair_a4ef/s1_extent.py")
ck("no 'git unavailable' line in a run from the real worktree",
   "git unavailable" not in out)
ck("control (a) at ebecd89 reports a count", re.search(
    r"\(a\) at ebecd89.*?\d+ asserted", out) is not None)
ck("control (b) at 83ac472 reports a count", re.search(
    r"\(b\) at 83ac472.*?\d+ asserted", out) is not None)
ck("mg-d633's sandbox does NOT copy .git",
   ".git" not in open(os.path.join(REPO,
                                   "code/species_extent_d633/kernd633.py"),
                      encoding="utf-8").read())

print()
print("  7  the small helpers")
ck("flat collapses whitespace", flat("a  b\n c") == "a b c")
ck("norm_toks lowercases and splits",
   norm_toks("The  Term\nHere") == ["the", "term", "here"])
ck("norm_toks of a 7-word phrase has 7 tokens",
   len(norm_toks("as three independent agreements about the term")) == 7)
ck("run_checker returns a nonzero code for a checker that fails",
   run_checker("code/species_extent_audit_6cb9/_nonexistent.py")[0] != 0)

print()
print("  8  and nothing above changed the worktree")
ck("git status --porcelain is what it was at line 1", git_status() == BASE)
ck("the audited document is byte-identical",
   open(p, encoding="utf-8").read() == before)

print()
print("=" * 78)
print("selftestd6cb9: %d assertion(s), %d failed" % (n, bad))
print("=" * 78)
sys.exit(1 if bad else 0)
