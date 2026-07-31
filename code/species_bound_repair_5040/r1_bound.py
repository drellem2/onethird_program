"""R1 -- OPEN 1.  The bound of "every regular file", stated and enforced.

mg-4700's OPEN 1: "EVERY REGULAR FILE ... AT ANY DEPTH" was true for a SECOND
generation by accident.  First it held because no tree had a subdirectory; the
walk was made to recurse; it then held because no tree had a SYMLINKED
DIRECTORY.  Each widening buys exactly one generation.

WHICH OF THE TWO OPTIONS THIS REPAIR TOOK, SAID ONCE AND PLAINLY:

    OPTION 1.  STATE THE WALK'S ACTUAL BOUND, so that the claim and the code
    describe the same set.

Not option 2.  Making a filesystem walk total means `followlinks=True` plus
cycle detection, and a walk that follows links still stops at a mount
boundary, still declines a device node, and still cannot enter a directory the
process has no permission for.  "Total" would be a third widening wearing a
stronger word, and it would buy one generation like the two before it.

But a bound written in prose is a copy of the code, and this arc has watched
copies rot for four tickets.  So the bound is stated IN THE ENUMERATION: each
walk returns every entry it declined and why, and a declined entry that is not
the one stated `__pycache__` rule is counted into that checker's TOTAL BAD.

That is a SUBTRACTION and not a widening.  What generated the generations was
never the depth rule or the symlink rule -- it was the SILENCE, the fact that
`os.walk` drops things without saying so and a sentence quantified over the
result.  The silence is removed.  The list of what a walk declines is a
MEASUREMENT of what happened, not a list of the rules somebody remembered, so
it covers the rule nobody has thought of yet.  R1c is the evidence for that
last sentence: two of the four structures probed here are ones no extent line
in this repository has ever mentioned, and they arrive named.
"""

import os
import sys

from kern5040 import (hdr, CHECKERS, Probe, run_checker, extract, PRE, REPO)

bad = 0
missed = 0
PLANT_TREE = "code/species_7d75"

# TWO COUNTERS, AND THEY ARE SEPARATE ON PURPOSE (mg-4700's convention).
# `bad` counts outcomes that contradict THIS REPAIR'S OWN CLAIMS -- if it is
# not 0, the repair does not do what it says.  `missed` counts PREDICTIONS in
# PREDICTIONS.md that were wrong.  A wrong prediction about the tree as it
# stood BEFORE the repair is information and not a defect, and rolling the two
# into one number would leave a reader unable to tell "the repair is broken"
# from "I did not know what the old code did".  Both are printed.

STRUCTURES = [
    ("a SYMLINKED DIRECTORY holding a forbidden statement",
     "slink",
     lambda pr, rel: pr.symlink_dir(
         rel, {"leak.md": "T3d says three are controls.\n"})),
    ("a FIFO", "pipe", lambda pr, rel: pr.fifo(rel)),
    ("a BROKEN SYMLINK named leak.md", "leak.md",
     lambda pr, rel: pr.broken_symlink(rel)),
    ("a DIRECTORY THIS PROCESS CANNOT READ", "noread",
     lambda pr, rel: pr.unreadable_dir(rel)),
]


def probe_all(root, label_prefix):
    """Plant each structure in turn, run all four checkers, report."""
    rows = []
    for what, name, make in STRUCTURES:
        rel = os.path.join(PLANT_TREE, name)
        with Probe("%s %s" % (label_prefix, what), root=root) as pr:
            try:
                make(pr, rel)
            except OSError as e:
                print("  could not plant %s: %s" % (what, e))
                continue
            for label, d, script in CHECKERS:
                rc, out = run_checker(d, script, root=root)
                names = name in out
                rows.append((what, label, rc, names))
        if root == REPO and not pr.restored:
            print("  *** THE WORKTREE WAS NOT RESTORED after %s ***" % what)
    return rows


def show(rows, expect, counter):
    """expect: {(what, checker): (exit, names)}.  `counter` is "bad" for rows
    that are this repair's own claims and "missed" for rows that are only
    predictions about code this repair did not write.  Anything not in
    `expect` is printed and not scored, with the reason given beside it."""
    global bad, missed
    seen = {}
    for what, label, rc, names in rows:
        seen[(what, label)] = (rc, names)
        print("      %-46s %-20s exit %d   %s"
              % (what[:46], label, rc,
                 "NAMES IT" if names else "does not name it"))
    print()
    for key in sorted(expect):
        want = expect[key]
        got = seen.get(key)
        ok = got == want
        if not ok:
            if counter == "bad":
                bad += 1
            else:
                missed += 1
        print("  %-56s %s" % ("%s / %s" % (key[1], key[0][:34]),
                              "ok" if ok else "*** %s, predicted %s ***"
                              % (got, want)))


# ---------------------------------------------------------------------------
# R1a  the clean tree.  A repair that fires on everything is not a repair.
# ---------------------------------------------------------------------------
hdr("R1a  THE CLEAN TREE -- all four checkers, nothing planted")

print("  P1f.  This is the row that stops every row below meaning nothing.")
print()
clean = {}
for label, d, script in CHECKERS:
    rc, out = run_checker(d, script)
    clean[label] = rc
    has_residue = "declined" in out.lower()
    ok = (rc == 0) and has_residue
    bad += (not ok)
    print("  %-24s exit %d   residue printed: %-3s   %s"
          % (label, rc, "yes" if has_residue else "NO", "ok" if ok else "***"))
print()
print("  P1g.  All four print what their walk declined.  That list is the")
print("  bound, and it is a measurement rather than a sentence somebody")
print("  maintains: nothing below required this file to know in advance")
print("  which structures exist.")
print()


# ---------------------------------------------------------------------------
# R1b  the four structures, against the tree as it ships
# ---------------------------------------------------------------------------
hdr("R1b  FOUR STRUCTURES PLANTED IN THE REAL WORKTREE")

print("  Each is planted, all four checkers are run, and the worktree is put")
print("  back and PROVED back with `git status --porcelain` AND the full")
print("  `git diff`, both compared against the state at entry.")
print()
after = probe_all(REPO, "after:")
S, F, B, N = (STRUCTURES[0][0], STRUCTURES[1][0], STRUCTURES[2][0],
              STRUCTURES[3][0])
show(after, {
    (S, "w3_scope.py"): (1, True),
    (S, "s1_extent.py"): (1, True),
    (S, "e1_extents.py"): (1, True),
    (S, "e2_crosssection.py"): (1, True),
    (F, "w3_scope.py"): (1, True),
    (F, "s1_extent.py"): (1, True),
    (F, "e1_extents.py"): (1, True),
    (B, "w3_scope.py"): (1, True),
    (B, "s1_extent.py"): (1, True),
    (B, "e1_extents.py"): (1, True),
    (B, "e2_crosssection.py"): (1, True),
    (N, "w3_scope.py"): (1, True),
    (N, "s1_extent.py"): (1, True),
    (N, "e1_extents.py"): (1, True),
}, "bad")
print()
print("  NOT SCORED, AND THE REASON IS THE POINT: e2_crosssection.py against")
print("  a fifo.  Its extent is every *.md, and a fifo named `pipe` is not in")
print("  it -- so silence there is CORRECT, and scoring it would be asking a")
print("  checker to widen its claim to cover a probe.  The broken symlink is")
print("  named `leak.md` for exactly this reason: it is inside e2's stated")
print("  extent, so e2 is scored on it.")
print()


# ---------------------------------------------------------------------------
# R1c  the same four structures against the PINNED pre-repair tree
# ---------------------------------------------------------------------------
hdr("R1c  THE SAME FOUR, AGAINST %s -- THE TREE BEFORE THIS REPAIR" % PRE)

print("  Anchored on %s, which git cannot move.  Not on HEAD: mg-821e" % PRE)
print("  anchored two comparisons on HEAD and they stopped comparing")
print("  anything the moment its own repair landed (mg-4700, F3).")
print()
pre_root = extract(PRE, os.path.join(os.environ.get("TMPDIR", "/tmp"),
                                     "mg5040-pre-%s" % PRE))
print("  extracted %s -> %s" % (PRE, pre_root))
print("  It has no .git, which matters for one row only and is stated there.")
print()
before = probe_all(pre_root, "before:")
show(before, {
    (S, "w3_scope.py"): (0, False),
    (S, "e1_extents.py"): (0, False),
    (S, "e2_crosssection.py"): (0, False),
    (F, "w3_scope.py"): (0, False),
    (F, "s1_extent.py"): (0, False),
    (F, "e1_extents.py"): (0, False),
    (F, "e2_crosssection.py"): (0, False),
    (B, "w3_scope.py"): (0, False),
    (B, "e1_extents.py"): (0, False),
    (N, "w3_scope.py"): (0, False),
    (N, "s1_extent.py"): (0, False),
    (N, "e1_extents.py"): (0, False),
}, "missed")
print()
_loud_at_pin = sorted(set(w for w, lab, rc, _n in before
                          if lab == "s1_extent.py" and rc == 1))
print("  DERIVED FROM THE ROWS ABOVE, not from a belief: at the pin,")
print("  s1_extent.py exits 1 on %d of the %d structures --"
      % (len(_loud_at_pin), len(STRUCTURES)))
for _w in _loud_at_pin:
    print("      %s" % _w)
print("  and in each case the reason is its control, which copies the tree")
print("  with shutil.copytree: copytree FOLLOWS a symlinked directory, and it")
print("  RAISES on a fifo and on a directory it cannot read.  So the")
print("  pre-repair tree is LOUD and the diagnosis a reader is handed is that")
print("  the injection control broke, while its own scan reports 0 entries")
print("  below the root and a forbidden statement sits live.  mg-4700 found")
print("  this shape once, at D2b, and predicted silence here; it is three of")
print("  four.  An exit code alone would have scored the old tree as catching")
print("  these, which is why every row above carries the NAMES IT column too.")
print()
print("  s1_extent.py against a symlinked directory is NOT scored at the pin.")
print("  mg-4700 measured it exiting 1 there -- for a reason that has nothing")
print("  to do with the extent: its control copies the tree with")
print("  shutil.copytree, which FOLLOWS the link, materialises the planted")
print("  file, and reports the injection control as broken.  A row that")
print("  scored the exit code alone would read that as the pre-repair tree")
print("  catching the symlink, which it does not.")
print()


# ---------------------------------------------------------------------------
# R1d  the row `want <= got` cannot see
# ---------------------------------------------------------------------------
hdr("R1d  E1 FIRES ON A ROW ITS OWN `want <= got` CANNOT REACH")

print("  mg-4700 F1: e1_extents.py walks the way its subjects walk, so when")
print("  both decline the same thing `want` and `got` agree and E1 CERTIFIES")
print("  THE EXTENT AS TRUE.  Widening E1's walk would fix this instance and")
print("  buy one generation.  The row below fires with `want <= got` holding")
print("  everywhere, because it compares the walk against ITSELF.")
print()
with Probe("E1 residue row") as pr:
    pr.symlink_dir(os.path.join(PLANT_TREE, "slink"),
                   {"leak.md": "T3d says three are controls.\n"})
    rc, out = run_checker("species_extent_d633", "e1_extents.py")
inclusion_rows_ok = "*** FALSE ***" not in "\n".join(
    ln for ln in out.splitlines() if "reads every" in ln)
residue_row_red = any("declined nothing unstated" in ln
                      and "FALSE" in ln for ln in out.splitlines())
for label, ok in (("e1_extents.py exits 1", rc == 1),
                  ("every `reads every ...` inclusion row is still ok",
                   inclusion_rows_ok),
                  ("the row that fails is the RESIDUE row", residue_row_red),
                  ("the worktree was restored", pr.restored)):
    bad += (not ok)
    print("  %-58s %s" % (label, "ok" if ok else "*** FALSE ***"))
print()


print("=" * 78)
print("R1 TOTAL BAD: %d      R1 PREDICTIONS MISSED: %d" % (bad, missed))
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  Four structures planted in ONE tree")
print("(%s), each measured against FOUR checkers, twice: against" % PLANT_TREE)
print("the worktree as it ships and against an extraction of %s." % PRE)
print("It says NOTHING about trees outside code/species_*, nothing about any")
print("checker not in the four, and nothing about whether a walk that")
print("FOLLOWED symlinks would be correct -- that is option 2 and this repair")
print("did not take it.  The four structures are not a claim to have")
print("enumerated the ways a walk can decline something: the repair's whole")
print("point is that the enumeration is not maintained by hand, and the fifth")
print("structure, whatever it is, will arrive in the same printed list.")
sys.exit(1 if bad else 0)
