"""SELFTEST for mg-1d26 -- every moving part of this instrument given an input
whose right answer is known, INCLUDING THE ONES THAT MUST SAY NO.

A probe that can only say yes has not been shown to be a probe.  Each block
below has at least one case whose correct answer is a refusal, and those are
the cases that make the passes mean anything.

    python3 code/verdict_path_repair_1d26/selftest1d26.py
"""

import os
import shutil
import sys
import tempfile

from kern1d26 import (hdr, Rows, REPO, E2, KERN, PRE_E2, PRE_KERN, LIVE,
                      ATTRIBUTIONS, SIX_PRE, SIX_POST, clone, cleanup,
                      Deletion, locate, disposition, attribution, neutralise,
                      source_lines, verdict_path, run_e2, sh)

R = Rows()


# ---------------------------------------------------------------------------
hdr("S1  locate() -- BY CONTENT, AND IT REFUSES WHEN IT CANNOT BE SURE")
# ---------------------------------------------------------------------------

tmp = tempfile.mkdtemp(prefix="mg1d26_st_")
rel = "toy.py"
with open(os.path.join(tmp, rel), "w", encoding="utf-8") as fh:
    fh.write("a = 1\nelse:\n    keep\nelse:\n    drop\nunique = 0\n")

R.row("finds a line that occurs once", locate(tmp, rel, "unique = 0", None) == 5)
R.row("finds the right one of two identical lines, by its successor",
      locate(tmp, rel, "else:", "keep") == 1
      and locate(tmp, rel, "else:", "drop") == 3)


def refuses(*a):
    try:
        locate(*a)
    except RuntimeError:
        return True
    return False


R.row("REFUSES a line that is not there", refuses(tmp, rel, "nope", None),
      "The row that must say no.  A lookup that silently resolves to nothing\n"
      "is a probe that measures nothing while printing a row.")
R.row("REFUSES an ambiguous line with no successor given",
      refuses(tmp, rel, "else:", None))
R.row("REFUSES a successor that does not follow it",
      refuses(tmp, rel, "else:", "a = 1"))
shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
hdr("S2  Deletion -- REMOVES EXACTLY ONE LINE AND PUTS THE FILE BACK")
# ---------------------------------------------------------------------------

tmp = tempfile.mkdtemp(prefix="mg1d26_st_")
p = os.path.join(tmp, rel)
ORIG = "one\ntwo\nthree\n"
with open(p, "w", encoding="utf-8") as fh:
    fh.write(ORIG)
with Deletion(tmp, rel, 1) as d:
    with open(p, encoding="utf-8") as fh:
        during = fh.read()
with open(p, encoding="utf-8") as fh:
    after = fh.read()
R.row("the deleted line is reported verbatim", d.text == "two")
R.row("exactly that line is gone", during == "one\nthree\n")
R.row("the file is byte-identical afterwards", after == ORIG,
      "Not `looks the same`: the bytes.")

with open(p, "w", encoding="utf-8") as fh:
    fh.write("one\ntwo")            # no trailing newline
with Deletion(tmp, rel, 0):
    with open(p, encoding="utf-8") as fh:
        during = fh.read()
R.row("a file with no trailing newline keeps having none", during == "two")
R.row("and its line count is what wc -l would say",
      len(source_lines(tmp, rel)) == 2)
shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
hdr("S3  disposition() -- FOUR STATES, EACH GIVEN AN INPUT THAT IS IT")
# ---------------------------------------------------------------------------

CASES = [
    (0, "anything at all", "GATE LOST"),
    (0, "*** STANDING UN-STRUCK ***", "GATE LOST"),
    (1, "*** STANDING UN-STRUCK ***", "GATE HELD, ATTRIBUTED"),
    (2, "E2 FOUND NOTHING TO CHECK -- THIS IS NOT A PASS.",
     "GATE HELD, ATTRIBUTED"),
    (9, "*** NO VERDICT WAS DELIVERED.", "GATE HELD, ATTRIBUTED"),
    (1, "Traceback (most recent call last):\nIndentationError",
     "GATE HELD, UNATTRIBUTED"),
    (None, "half a run\nTIMED OUT", "TIMED OUT"),
]
for rc, out, want in CASES:
    got, _w = disposition(rc, out)
    R.row("exit %-4s + %-34s -> %s" % (rc, out.splitlines()[0][:34], want),
          got == want, "got %s" % got)
R.row("a GREEN run PRINTING the finding is still GATE LOST",
      disposition(0, "*** STANDING UN-STRUCK ***")[0] == "GATE LOST",
      "mg-6ef4's F3 is exactly this case.  Printing the finding while exiting\n"
      "0 is never a mitigation: a reader's `&&` sees the code.")


# ---------------------------------------------------------------------------
hdr("S4  attribution() -- IT NAMES WHAT FIRED, AND SAYS SO WHEN NOTHING DOES")
# ---------------------------------------------------------------------------

for needle, what in ATTRIBUTIONS:
    R.row("recognises %-52s" % ("`%s`" % needle[:50]),
          attribution("noise\n%s\nnoise" % needle) == what)
R.row("returns nothing for output that names nothing",
      attribution("Traceback (most recent call last):\n  File x\nValueError")
      is None,
      "The row that must say no.  If this predicate matched anything, every\n"
      "traceback would be counted as a control naming itself, and `loud` and\n"
      "`mute` would stop being different columns.")


# ---------------------------------------------------------------------------
hdr("S5  THE SANDBOX IS GIT-BACKED, MEASURED BY RUNNING A CONTROL THAT NEEDS IT")
# ---------------------------------------------------------------------------

R.note("A plain file copy has no `.git`, and in one the checker's census")
R.note("anchor prints `NO REVISION` while every verdict still looks right.  A")
R.note("sweep in such a sandbox would be certifying a checker with a control")
R.note("silently switched off.  This is not asserted; the control is run and")
R.note("its output is read.")
print()

base = clone()
rc, out = run_e2(base)
anchored = [ln for ln in out.splitlines() if ln.startswith("MEASURED AT ")]
said = anchored[0] if anchored else "(the anchor line is absent)"
R.row("the checker's census anchor resolves to a revision in the sandbox",
      bool(anchored) and "NO REVISION" not in said, said[:70])


# ---------------------------------------------------------------------------
hdr("S6  neutralise() -- AND WHAT IT DOES THE SECOND TIME")
# ---------------------------------------------------------------------------

rel_live, n1 = neutralise(base)
rel_live, n2 = neutralise(base)
R.row("it removes at least one strike marker the first time", n1 > 0,
      "%s carried %d `~~` marker(s)" % (rel_live, n1))
R.row("and none the second time", n2 == 0,
      "The row that must say no.  If this said `%d` again the count would be\n"
      "of markers in a file it had already rewritten." % n1)
rc_clean, out_clean = run_e2(base)
R.row("the neutralised sandbox is GREEN",
      rc_clean == 0 and "*** STANDING UN-STRUCK ***" not in out_clean,
      "exit %s" % rc_clean)


# ---------------------------------------------------------------------------
hdr("S7  THE PRE-REPAIR COPIES ARE THE PRE-REPAIR FILES")
# ---------------------------------------------------------------------------

R.note("Their identity is established by WHAT THEY CONTAIN and by WHAT THEY")
R.note("DO, never by a revision: the refinery rebases before merging, so a")
R.note("recorded SHA is displaced on main and `git merge-base --is-ancestor`")
R.note("gives a FALSE NEGATIVE (mg-c067, mg-a74f).  P2b's reproduction of")
R.note("mg-d53d's six is the other half of this evidence and is the stronger")
R.note("half.")
print()

pre_e2 = open(PRE_E2, encoding="utf-8").read()
pre_kern = open(PRE_KERN, encoding="utf-8").read()
now_e2 = open(os.path.join(REPO, E2), encoding="utf-8").read()
now_kern = open(os.path.join(REPO, KERN), encoding="utf-8").read()

R.row("the pre copy of e2 carries `sys.exit(1 if bad else 0)`",
      "\nsys.exit(1 if bad else 0)\n" in pre_e2)
R.row("and does not know about the dead man's switch",
      "arm_verdict" not in pre_e2 and "deliver(" not in pre_e2)
R.row("the pre copy of the kernel has no deliver() and no arm_verdict()",
      "def deliver" not in pre_kern and "def arm_verdict" not in pre_kern)
R.row("the repaired e2 has both, and no bare sys.exit of its own",
      "arm_verdict()" in now_e2 and 'deliver("E2"' in now_e2
      and "\nsys.exit(" not in now_e2)
R.row("the repaired kernel has both", "def deliver" in now_kern
      and "def arm_verdict" in now_kern)
R.row("the two pairs differ", pre_e2 != now_e2 and pre_kern != now_kern,
      "The row that must say no: if the copies matched the repaired files,\n"
      "P2b would be sweeping the repair and calling the result a before-state.")

for label, src, six in (("PRE", pre_e2, SIX_PRE), ("POST", now_e2, SIX_POST)):
    missing = [t for rel_, t, _n in six if rel_ == E2 and t not in src]
    R.row("every %s entry naming e2 is present in that copy of e2"
          % label, not missing, "\n".join(missing))


# ---------------------------------------------------------------------------
hdr("S8  verdict_path() -- ON A TOY TREE WHOSE ANSWER IS KNOWN")
# ---------------------------------------------------------------------------

tmp = tempfile.mkdtemp(prefix="mg1d26_st_")
os.makedirs(os.path.join(tmp, "code", "toy_runner"))
os.makedirs(os.path.join(tmp, "code", "toy_checker"))
with open(os.path.join(tmp, "code", "toy_runner", "run_all.sh"), "w") as fh:
    fh.write("set -e\npython3 first.py\n# a comment after the gate\n"
             "python3 ../toy_checker/gate.py\n# and one more comment\n")
with open(os.path.join(tmp, "code", "toy_checker", "gate.py"), "w") as fh:
    fh.write("import os\nimport sys\nfrom helper import thing\n")
with open(os.path.join(tmp, "code", "toy_checker", "helper.py"), "w") as fh:
    fh.write("import re\nfrom deeper import x\n")
with open(os.path.join(tmp, "code", "toy_checker", "deeper.py"), "w") as fh:
    fh.write("thing = 1\n")

rel_, cmd, files, unres = verdict_path(tmp, "toy_runner")
R.row("a COMMENT after the gate is not the last command",
      cmd == "python3 ../toy_checker/gate.py", "got: %s" % cmd)
R.row("the closure is transitive -- gate, helper AND deeper",
      sorted(files) == sorted([os.path.join("code", "toy_runner",
                                            "run_all.sh"),
                               os.path.join("code", "toy_checker", "gate.py"),
                               os.path.join("code", "toy_checker",
                                            "helper.py"),
                               os.path.join("code", "toy_checker",
                                            "deeper.py")]),
      "got: %s" % ", ".join(sorted(files)))
R.row("standard-library imports are not in it",
      not any(f.endswith(("os.py", "sys.py", "re.py")) for f in files))

with open(os.path.join(tmp, "code", "toy_checker", "gate.py"), "a") as fh:
    fh.write("from nowhere import y\n")
rel_, cmd, files, unres = verdict_path(tmp, "toy_runner")
R.row("an import it cannot resolve is REPORTED and not dropped",
      unres == ["nowhere"], "got: %s" % unres)

with open(os.path.join(tmp, "code", "toy_runner", "run_all.sh"), "a") as fh:
    fh.write("echo appended\n")
rel_, cmd, files, unres = verdict_path(tmp, "toy_runner")
R.row("a runner whose last command is not a python3 call is reported",
      unres == ["the last command is not a python3 call"] and len(files) == 1,
      "The row that must say no.  A rule that quietly returned only the\n"
      "runner file would report a one-file verdict path as a complete one.")
shutil.rmtree(tmp, ignore_errors=True)

R.tail("SELFTEST1D26")
print()
print("EXTENT.  These rows are about THIS INSTRUMENT's own helpers -- the")
print("lookup, the deletion operator, the two classifiers, the sandbox, the")
print("neutralisation, the pre-repair copies and the population rule.  They")
print("say NOTHING about the repair itself; P1, P2 and P3 do that, and this")
print("file exists so that a reader knows whether their machinery works before")
print("reading what it measured.")

cleanup()
sys.exit(1 if R.bad else 0)
