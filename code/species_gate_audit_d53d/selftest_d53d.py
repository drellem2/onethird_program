"""SELFTEST for mg-d53d -- the instrument, checked against constructed inputs.

Every section of this audit rests on four mechanisms, and each of the four is
capable of failing SILENTLY in the direction that makes the audit look clean:

  * the sandbox.  If the clone were missing git, three controls in the runners
    it executes would print "git unavailable -- SKIPPED" and the deletion
    sweep would certify a runner with two of its own controls switched off.
  * the deletion.  If `Deletion` restored the file wrongly, every row after
    the first would be measuring a file this audit had edited.
  * the plant.  If the planted strike were exonerated -- `kernd633.NEGATES`
    matches sixteen words -- every sweep would run against a GREEN tree and
    report `the gate held` 806 times.
  * the disposition.  If `GATE LOST` were decided on anything but the exit
    code, mg-6ef4's own finding would classify as a pass.

So each is given an input whose right answer is known, INCLUDING the inputs
that must make it say NO.  A mechanism only ever seen to say yes is worth
nothing, which is the sentence this whole arc keeps re-deriving.

    python3 code/species_gate_audit_d53d/selftest_d53d.py
"""

import os
import sys

import kern_d53d as K

bad = 0


def row(label, ok, detail=""):
    global bad
    bad += (not ok)
    print("  %-64s %s" % (label[:64], "ok" if ok else "*** FAILED ***"))
    for ln in str(detail).splitlines():
        if ln:
            print("        %s" % ln)


K.hdr("S1  THE SANDBOX IS A GIT CLONE OF THIS WORKTREE")

root = K.clone()
rc, head_here = K.sh(["git", "-C", K.REPO, "rev-parse", "HEAD"])
rc2, head_there = K.sh(["git", "-C", root, "rev-parse", "HEAD"])
row("the clone's HEAD is this worktree's HEAD",
    head_here.strip() == head_there.strip() and head_here.strip() != "",
    "%s vs %s" % (head_here.strip()[:12], head_there.strip()[:12]))

rc, status = K.sh(["git", "-C", root, "status", "--porcelain"])
row("the clone is clean, so `git status` in a probe means what it says",
    rc == 0 and not status.strip(), status[:200])

rc, _ = K.sh(["git", "-C", root, "archive", "ebecd89"])
row("`git archive` resolves in the clone -- s1_extent.py's two historical "
    "controls can run", rc == 0,
    "Without this they print `git unavailable -- SKIPPED` and the deletion\n"
    "sweep certifies a runner with two of its controls silently off.")

rc, out = K.run_script(root, os.path.join("code", "species_repair_a4ef",
                                          "s1_extent.py"))
# The string to look for is `git unavailable -- SKIPPED`, not `SKIPPED`: this
# transcript uses the bare word for an unrelated and correct exclusion
# (`SKIPPED, NAMED, so the exclusion cannot grow unseen -- 5 file(s)`), and
# the first version of this row matched it and reported the sandbox broken.
# A selftest that fires on the right output is a selftest that would have
# been silenced by weakening it, so the STRING is narrowed and both are
# counted below.
skipped = "git unavailable -- SKIPPED" in out
row("and they DID run in this clone, not merely could", not skipped,
    "s1_extent.py exit %s; `git unavailable -- SKIPPED` in its output: %s\n"
    "(the bare word SKIPPED appears %d time(s), all of them the file-level\n"
    "exclusion this checker states on purpose)"
    % (rc, skipped, out.count("SKIPPED")))
row("and the two historical controls printed a MEASUREMENT, not a skip",
    "at ebecd89" in out and "at 83ac472" in out and not skipped,
    "\n".join(ln.strip() for ln in out.splitlines()
              if "ebecd89" in ln or "83ac472" in ln)[:300])

for t in ("docs", os.path.join("code", "species_extent_d633"),
          os.path.join("code", "species_7d75")):
    row("the clone carries %s" % t, os.path.isdir(os.path.join(root, t)))


K.hdr("S2  DELETION -- IT REMOVES ONE LINE AND PUTS IT BACK EXACTLY")

REL = os.path.join("code", "species_repair_a4ef", "run_all.sh")
path = os.path.join(root, REL)
with open(path, encoding="utf-8") as fh:
    before = fh.read()
n = len(K.source_lines(root, REL))
row("the runner is %d lines by the rule the population uses" % n, n == 83,
    "a trailing newline does not make a final empty line")

with K.Deletion(root, REL, 5) as d:
    with open(path, encoding="utf-8") as fh:
        during = fh.read()
    row("line 6 is the one removed", d.text.strip() == K.SETE, repr(d.text))
    row("exactly one line fewer while deleted",
        len(during.split("\n")) == len(before.split("\n")) - 1)
    row("and it is the RIGHT line that is gone",
        K.SETE not in during.split("\n"))
with open(path, encoding="utf-8") as fh:
    after = fh.read()
row("the file is byte-identical afterwards", after == before,
    "%d bytes before, %d after" % (len(before), len(after)))

# the negative: a deletion that does nothing must be visible as doing nothing
with K.Deletion(root, REL, 7):
    pass
with open(path, encoding="utf-8") as fh:
    row("restored after a second, unrelated deletion too",
        fh.read() == before)


K.hdr("S3  THE PLANT -- IT ARMS, AND IT CAN BE DISARMED")

rc, out = K.run_e2(root)
row("e2 is GREEN on the clean clone", rc == 0 and K.E2_SAYS not in out,
    "exit %s" % rc)

K.plant_strike(root)
rc, out = K.run_e2(root)
row("e2 is RED with the plant, and says why",
    rc == 1 and out.count("*** %s ***" % K.E2_SAYS) == 1,
    "exit %s, %d occurrence(s) STANDING"
    % (rc, out.count("*** %s ***" % K.E2_SAYS)))

# THE NEGATIVE CONTROL.  The same sentence in a paragraph that says it does
# not hold must NOT fire -- otherwise the plant is not measuring the rule, it
# is measuring the presence of a `~~`.
p = os.path.join(root, K.STRIKE_REL)
with open(p, "w", encoding="utf-8") as fh:
    fh.write("# planted by mg-d53d's selftest\n\n~~%s~~\n\n"
             "This sentence is a misquotation and does not hold: %s\n"
             % (K.CLAIM, K.CLAIM))
rc, out = K.run_e2(root)
row("the SAME sentence in a paragraph that retracts it does NOT fire",
    rc == 0 and K.E2_SAYS not in out,
    "exit %s -- so the plant in G1/G2 arms the RULE and not the `~~`" % rc)
K.unplant_strike(root)

rc, out = K.run_e2(root)
row("and the tree is green again once the plant is removed",
    rc == 0 and K.E2_SAYS not in out, "exit %s" % rc)


K.hdr("S4  DISPOSITION -- THE THREE CLASSES, AND THE ONE THAT MATTERS")

row("exit 0 is GATE LOST even when the finding was printed in full",
    K.disposition(0, "... *** %s ***" % K.E2_SAYS) == "GATE LOST",
    "This is mg-6ef4's F3 exactly: printed and green.  If this row were\n"
    "written the other way the audit could not see its own subject.")
row("non-zero with the sentence is GATE HELD",
    K.disposition(1, "*** %s ***" % K.E2_SAYS) == "GATE HELD")
row("non-zero without it is DIED BEFORE THE GATE",
    K.disposition(2, "IndentationError") == "DIED BEFORE THE GATE")
row("a timeout is its own class and never a pass",
    K.disposition(None, "") == "TIMED OUT")


K.hdr("S5  STEP SUBSTITUTION KEEPS THE WIRING IT IS MEASURING")

steps = K.steps_of(root, "species_repair_a4ef")
row("a4ef has 4 python3 steps", len(steps) == 4,
    "\n".join("line %d: %s" % (n, t[:56]) for n, t in steps))
rel, i, was = K.force_step(root, "species_repair_a4ef", 0)
now = K.read_lines(root, rel)[i]
row("the redirect and the guard survive the substitution",
    now.endswith("> out_selftest.txt || {") and "FORCED RED" in now,
    "was:  %s\nnow:  %s" % (was, now))
lines = K.read_lines(root, rel)
lines[i] = was
K.write_lines(root, rel, lines)
row("and the runner file is restored",
    K.read_lines(root, rel)[i] == was)


K.hdr("S6  THE PARALLEL POOL HANDS EACH TASK A WHOLE TREE")


def _boom(_root, i):
    if i == 2:
        raise ValueError("constructed failure")
    return i


def _raises(p):
    try:
        p.map(list(range(4)), _boom)
    except RuntimeError:
        return True
    return False


pool = K.Pool(3)
row("3 distinct sandbox roots", len(set(pool.roots)) == 3)
got = pool.map(list(range(9)), lambda r, i: (r, i))
row("every task ran and none was dropped",
    len(got) == 9 and sorted(i for _r, i in got) == list(range(9)))
row("a task that raises is reported, never dropped silently",
    _raises(pool),
    "A sweep that loses a row reports `the gate held` for a line it never\n"
    "measured, which is the failure this whole audit is about.")

print()
print("=" * 78)
print("selftest_d53d.py: %d check(s) failed" % bad)
print("=" * 78)
K.cleanup()
sys.exit(1 if bad else 0)
