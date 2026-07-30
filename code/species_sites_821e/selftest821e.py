"""SELFTEST for mg-821e -- the harness contract, asserted before anything runs.

Three of these assertions exist because the corresponding defect happened in
this instrument and is recorded in OUTCOMES.md.  A harness that mutates the
real worktree and runs whole shell scripts has to be shown safe before it is
believed, and "shown" means a failing case as well as a passing one: more than
half of what follows asserts that something does NOT happen.

    python3 code/species_sites_821e/selftest821e.py
"""

import os
import re
import subprocess
import sys

from kern821e import (REPO, git_status, Probe, sections, delete_at_site,
                      replace_once, preserve, out_files, NO_RECURSE,
                      WIRE_MARK, unwire, PRE_REPAIR)

n = 0
bad = 0
SCRATCH = "code/species_sites_821e/_selftest_scratch.md"


def ck(label, cond):
    global n, bad
    n += 1
    bad += (not cond)
    if not cond:
        print("  *** FAILED: %s" % label)


# ---------------------------------------------------------------------------
# 1.  sections(): a region runs to the next heading of ANY level.
# ---------------------------------------------------------------------------
DOCX = ("# Top\n\nintro\n\n## One\n\nalpha\n\n### One.a\n\nbeta\n\n"
        "## Two\n\ngamma\n")
secs = sections(DOCX)
ck("four regions", len(secs) == 4)
ck("first region is the top heading", secs[0][0] == "# Top")
ck("the top region stops at ## One", "alpha" not in secs[0][1])
ck("the top region keeps its own body", "intro" in secs[0][1])
ck("## One does NOT swallow ### One.a", "beta" not in secs[1][1])
ck("### One.a is its own region", secs[2][0] == "### One.a")
ck("## Two is last", secs[3][0] == "## Two" and "gamma" in secs[3][1])
# NOT `sum(len(b.splitlines()))`: a body ending in a blank line loses it to
# splitlines, so that sum reads 12 for a 15-line document and the assertion
# fails against a correct function.  The property that matters is that the
# regions REASSEMBLE, which is what `delete_at_site` relies on.
ck("the regions reassemble into the document",
   "\n".join(b for _h, b in secs) + "\n" == DOCX)

# a heading-shaped line that is not a heading must not split
ck("an indented hash is not a heading",
   len(sections("# A\n\n    # not a heading\n")) == 1)


# ---------------------------------------------------------------------------
# 2.  delete_at_site(): one site, and ONLY that site.
# ---------------------------------------------------------------------------
TWO = ("# Top\n\nNEEDLE here\n\n## One\n\nNEEDLE here too\n\n"
       "## Two\n\nNEEDLE a third time\n")
got = delete_at_site(r"^## One", "NEEDLE", "GONE")(TWO)
ck("the site's copy is replaced", "GONE here too" in got)
ck("the top copy survives", "NEEDLE here\n" in got)
ck("the other section's copy survives", "NEEDLE a third time" in got)
ck("exactly one copy changed", got.count("NEEDLE") == 2)
ck("the file is otherwise byte-identical",
   got.replace("GONE", "NEEDLE") == TWO)

# two byte-identical sections: a str.replace would edit the wrong one
SAME = "# Top\n\n## A\n\nsame body\n\n## A\n\nsame body\n"
got = delete_at_site(r"^## A", "same", "edited")(SAME)
ck("the FIRST matching section is the one edited",
   got.index("edited") < got.index("same"))
ck("and the second is untouched", got.count("same body") == 1)

for pat, needle in [(r"^## Nope", "NEEDLE"), (r"^## One", "ABSENT")]:
    try:
        delete_at_site(pat, needle, "x")(TWO)
        ck("a mutation that cannot apply RAISES (%s)" % pat, False)
    except AssertionError:
        ck("a mutation that cannot apply RAISES (%s)" % pat, True)

try:
    replace_once("not present anywhere", "x")("abc")
    ck("replace_once raises when its target is absent", False)
except AssertionError:
    ck("replace_once raises when its target is absent", True)


# ---------------------------------------------------------------------------
# 3.  Probe: the restore, proved rather than asserted.
# ---------------------------------------------------------------------------
BASE = git_status()
# A TRACKED file: `git status --porcelain` reports an untracked DIRECTORY as one
# `??` line whatever is inside it, so probing this instrument's own source
# would have made "git sees it" unfalsifiable -- a check that cannot fail,
# inside the self-test of an instrument auditing checks that cannot fail.
target = "code/species_repair_a4ef/s1_extent.py"
before = open(os.path.join(REPO, target), encoding="utf-8").read()

with Probe([(target, replace_once("import os", "import os  # probed"))]):
    mid = open(os.path.join(REPO, target), encoding="utf-8").read()
    ck("the mutation really lands on disk", "# probed" in mid)
    ck("git sees it", git_status() != BASE)
after = open(os.path.join(REPO, target), encoding="utf-8").read()
ck("the restore is byte-exact", after == before)
ck("git status is back to where it was", git_status() == BASE)

# a NEW file, and the directories made for it, go away again
deep = "code/species_sites_821e/_st/_deep/new.md"
with Probe([(deep, lambda _o: "hello\n")]):
    ck("a new file is created", os.path.exists(os.path.join(REPO, deep)))
ck("the new file is removed", not os.path.exists(os.path.join(REPO, deep)))
ck("and so are the directories made for it",
   not os.path.exists(os.path.join(REPO, "code/species_sites_821e/_st")))
ck("git status is clean after a created file", git_status() == BASE)

# preserve() saves without changing: this is what protects a runner's out_*.txt
scr = os.path.join(REPO, SCRATCH)
with open(scr, "w", encoding="utf-8") as fh:
    fh.write("original\n")
try:
    with Probe([(SCRATCH, preserve)]):
        with open(scr, "w", encoding="utf-8") as fh:
            fh.write("clobbered by a run\n")
        ck("preserve does not block a later write",
           open(scr, encoding="utf-8").read() == "clobbered by a run\n")
    ck("preserve puts the original back",
       open(scr, encoding="utf-8").read() == "original\n")
finally:
    os.unlink(scr)
ck("git status clean after the preserve case", git_status() == BASE)

# an exception inside the body must still restore
try:
    with Probe([(target, replace_once("import os", "import os  # boom"))]):
        raise RuntimeError("deliberate")
except RuntimeError:
    pass
ck("the restore happens even when the body raises",
   open(os.path.join(REPO, target), encoding="utf-8").read() == before)
ck("git status clean after a raising probe", git_status() == BASE)


# ---------------------------------------------------------------------------
# 4.  The wiring block, and the deletion test that removes it.
# ---------------------------------------------------------------------------
WIRED = ["species_repair_6f61", "species_remainder_f8fa", "species_repair_a4ef"]
for t in WIRED:
    p = os.path.join(REPO, "code", t, "run_all.sh")
    text = open(p, encoding="utf-8").read()
    ck("%s carries the wiring block" % t, WIRE_MARK in text)
    ck("%s calls e2 by path" % t,
       "../species_extent_d633/e2_crosssection.py" in text)
    ck("%s prints the check's output, not just the call" % t,
       'echo "$E2OUT"' in text)
    ck("%s fails the run when the check fails" % t,
       "E2 CROSS-SECTION FAILED" in text)
    stripped = unwire(text)
    ck("unwire removes the marker from %s" % t,
       WIRE_MARK not in stripped)
    ck("unwire removes every reference to E2OUT from %s" % t,
       "E2OUT" not in stripped)
    ck("unwire leaves no dangling brace in %s" % t,
       stripped.count("{") == stripped.count("}"))
    ck("unwire is a DELETION -- nothing else changes in %s" % t,
       all(ln in text.splitlines() for ln in stripped.splitlines()))
    # THE WHOLE CLAIM, MEASURED: the wiring is a pure addition, so undoing it
    # must give back the runner as committed BEFORE this ticket, byte for
    # byte.  Anything weaker leaves room for the deletion test to be removing
    # something else.  Pinned, not `HEAD` -- see `PRE_REPAIR` in kern821e.py.
    head = subprocess.run(["git", "show", "%s:code/%s/run_all.sh"
                           % (PRE_REPAIR, t)],
                          cwd=REPO, capture_output=True, text=True)
    ck("the pre-repair copy of %s is readable" % t, head.returncode == 0)
    ck("the pinned ref does NOT already carry the wiring (%s)" % t,
       WIRE_MARK not in head.stdout)
    ck("unwire(%s) is BYTE-IDENTICAL to the pre-repair copy" % t,
       stripped == head.stdout)
    ck("and the wiring really did add something to %s" % t,
       len(text) > len(head.stdout))
    try:
        unwire(stripped)
        ck("unwire refuses a runner that has no block (%s)" % t, False)
    except (AssertionError, StopIteration, ValueError):
        ck("unwire refuses a runner that has no block (%s)" % t, True)

# the tree that already called it must NOT have been given a second copy
d633 = open(os.path.join(REPO, "code/species_extent_d633/run_all.sh"),
            encoding="utf-8").read()
ck("species_extent_d633 still calls e2 exactly once",
   d633.count("e2_crosssection.py") == 1)
ck("and was not given the wiring block", WIRE_MARK not in d633)


# ---------------------------------------------------------------------------
# 5.  The subjects are where this instrument thinks they are.
# ---------------------------------------------------------------------------
for rel, needle in [
    ("code/species_repair_a4ef/s1_extent.py", "for dirpath, dirnames, "
     "filenames in os.walk(root):"),
    ("code/species_remainder_f8fa/w3_scope.py", "for _dp, _dns, _fns in "
     "os.walk(SRC):"),
    ("code/species_extent_d633/e1_extents.py", "for dp, dns, fns in "
     "os.walk(root):"),
    ("code/species_repair_6f61/check_doc.py", "C4_SITES = ["),
]:
    text = open(os.path.join(REPO, rel), encoding="utf-8").read()
    ck("%s carries the repair" % os.path.basename(rel), needle in text)

for name, rel, a, b in NO_RECURSE:
    text = open(os.path.join(REPO, rel), encoding="utf-8").read()
    ck("P1's deletion target is present in %s" % name, a in text)
    ck("P1's deletion target is UNIQUE in %s" % name, text.count(a) == 1)
    ck("P1's replacement is not already there in %s" % name, b not in text)

ck("out_files finds a tree's committed outputs",
   len(out_files("species_repair_a4ef")) >= 3)
ck("out_files returns repo-relative paths",
   all(f.startswith("code/") for f in out_files("species_repair_a4ef")))

ck("git status is unchanged by the whole self-test", git_status() == BASE)

print("selftest821e %s -- %d assertions"
      % ("OK" if bad == 0 else "*** %d FAILED ***" % bad, n))
sys.exit(1 if bad else 0)
