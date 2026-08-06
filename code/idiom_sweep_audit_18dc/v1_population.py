"""mg-18dc / V1 -- 109, RE-DERIVED, AND THE REVISION IT IS TRUE AT.

The brief hands me three numbers and tells me to derive them myself.  The first
one is not a number about the arc.  It is a number about a COMMIT, and mg-03d1
and mg-ec63 both measured it with a glob over a working directory, which is a
number about a DISK.  The two differ by whatever was untracked at the moment.

So this section does not ask `is it 109`.  It asks `109 AT WHAT`, and prints the
answer at every revision in the lineage, including the two that carry the claims
onto `main`.

Exit code = revisions at which the shipped figure is not reproducible.
"""

import sys

import lib18dc as B

print("mg-18dc / V1 -- THE POPULATION, RE-DERIVED AS A PROPERTY OF A COMMIT")
print("HEAD: %s" % B.head())

# The lineage.  `declared` is what the transcript produced at that revision
# printed as its own total, or None where the revision ships no total.
LINE = [
    ("9f1ecaa", "mg-03d1 predictions   (pre-rebase)", 109),
    ("6fda370", "mg-03d1 predictions   (on main)", None),
    ("d33970b", "mg-03d1 audit         (pre-rebase)", 109),
    ("eacc5e1", "mg-03d1 audit         (on main, CARRIES the 109)", 109),
    ("454f565", "mg-ec63 predictions   (pre-rebase)", None),
    ("f98ef34", "mg-ec63 predictions   (on main)", None),
    ("3fc870a", "mg-ec63 instrument    (pre-rebase, DECLARED by S1)", 110),
    ("41972fb", "mg-ec63 evidence      (pre-rebase)", 110),
    ("7fccb4e", "mg-ec63 evidence      (on main, CARRIES the 110)", 110),
]

B.hdr("V1a  THE SAME RULE AT EVERY REVISION OF THE LINEAGE")

print("  My rule: `git ls-tree -r <rev> -- code/` and keep every path of the")
print("  form `code/<dir>/run_all.sh`.  A PROPERTY OF THE COMMIT.  mg-03d1 and")
print("  mg-ec63 both globbed the working directory instead, which counts what")
print("  was on disk -- tracked or not -- at one moment that no longer exists.")
print()
print("  population: the revisions of this lineage")
print()
print("      %-9s %-46s %5s %8s" % ("REV", "WHAT IT IS", "MINE", "SHIPPED"))
sets = {}
mismatch = 0
for rev, what, declared in LINE:
    rs = B.runners_at(rev)
    sets[rev] = set(rs)
    flag = ""
    if declared is not None:
        if len(rs) != declared:
            flag = "  <- DIFFERS"
            mismatch += 1
        else:
            flag = "  <- agrees"
    print("      %-9s %-46s %5d %8s%s"
          % (rev, what, len(rs), declared if declared is not None else "-", flag))
print()
print("      ^ one unit of the MINE column is one `run_all.sh` tracked at that")
print("        revision; one unit of SHIPPED is the total that revision's own")
print("        transcript printed.")

# ---------------------------------------------------------------------------
B.hdr("V1b  109 IS TRUE AT ONE REVISION, AND IT IS NOT THE ONE ON `main`")

d09 = [r for r, _, _ in LINE if len(sets[r]) == 109]
print("  population: the %d revisions of V1a" % len(LINE))
B.plain("...REVISIONS where my rule gives exactly 109", len(d09), "one revision")
for r in d09:
    print("          %s" % r)
print()
print("  mg-03d1's transcript declares `HEAD: 9f1ecaa` and prints 109.  At")
print("  9f1ecaa my rule gives %d." % len(sets["9f1ecaa"]))
gap = sets["d33970b"] - sets["9f1ecaa"]
print("  The difference between 9f1ecaa and its own audit commit d33970b is")
print("  exactly %d tree(s):" % len(gap))
for t in sorted(gap):
    print("          %s%s" % (t, "   <- mg-03d1'S OWN" if "03d1" in t else ""))
print()
print("  So the 109 IS reproducible -- but only by counting a runner that was")
print("  UNTRACKED when the count was taken.  The counter was in the count and")
print("  not yet in the repository.  mg-03d1 recorded that its own tree joined")
print("  the population; what it did not record is that at the revision its own")
print("  transcript names, the member does not exist.")

# ---------------------------------------------------------------------------
B.hdr("V1c  AND ON `main` THE SAME RULE GIVES A DIFFERENT NUMBER ENTIRELY")

print("  A rebase preserves the DIFF and moves the BASE.  Every count in this")
print("  arc is a fact about the base.  The four pre/post-rebase twins:")
print()
for a, b in (("9f1ecaa", "6fda370"), ("d33970b", "eacc5e1"),
             ("454f565", "f98ef34"), ("41972fb", "7fccb4e")):
    pa = B.git("show", a).strip()
    pb = B.git("show", b).strip()
    import subprocess
    pid_a = subprocess.run(["git", "patch-id", "--stable"], input=pa,
                           capture_output=True, text=True,
                           cwd=B.REPO).stdout.split()[:1]
    pid_b = subprocess.run(["git", "patch-id", "--stable"], input=pb,
                           capture_output=True, text=True,
                           cwd=B.REPO).stdout.split()[:1]
    ta = B.git("rev-parse", "%s^{tree}" % a).strip()
    tb = B.git("rev-parse", "%s^{tree}" % b).strip()
    print("      %s -> %s   patch-id %-5s  tree %-5s  runners %d -> %d"
          % (a, b, "SAME" if pid_a == pid_b else "DIFF",
             "SAME" if ta == tb else "DIFF", len(sets[a]), len(sets[b])))
print()
print("  PATCH-ID IS NOT AN ORACLE and here is the reason in one table: all")
print("  four pairs are patch-id IDENTICAL and tree DIFFERENT, and the runner")
print("  population moves by up to %d across a pair that patch-id calls the same"
      % max(abs(len(sets[a]) - len(sets[b]))
            for a, b in (("9f1ecaa", "6fda370"), ("d33970b", "eacc5e1"),
                         ("454f565", "f98ef34"), ("41972fb", "7fccb4e"))))
print("  change.  The diff is identical; the tree the diff LANDS IN is not.")
print()
print("  CONSEQUENCE, and it is the finding of this section:")
print()
print("      eacc5e1 carries mg-03d1's `109 RUNNERS IN THE ARC` into a tree")
print("      holding %d." % len(sets["eacc5e1"]))
print("      7fccb4e carries mg-ec63's `110 RUNNERS IN THE ARC` into a tree")
print("      holding %d." % len(sets["7fccb4e"]))
print()
print("  Neither number was wrong when it was measured.  Both are wrong in the")
print("  commit that publishes them, and nothing in either tree says so.")

# ---------------------------------------------------------------------------
B.hdr("V1d  THE POPULATION mg-ec63 NEVER SWEPT")

never = sets["7fccb4e"] - sets["3fc870a"]
print("  mg-ec63 ran at 3fc870a and landed at 7fccb4e.  Runners present in the")
print("  landing tree and ABSENT from the tree that was swept:")
print()
print("  population: the %d runners at 7fccb4e" % len(sets["7fccb4e"]))
B.plain("...RUNNERS never in the sweep's population", len(never), "one `run_all.sh`")
for t in sorted(never):
    tag = ""
    if "03d1" in t:
        tag = "   <- THE TREE WHOSE THREE NUMBERS THE SWEEP RE-DERIVED"
    if t == B.MINE:
        tag = "   <- THIS AUDIT'S OWN"
    print("          %s%s" % (t, tag))
print()
print("  The first of those is `code/grain_axis_audit_03d1`.  mg-ec63's S1a")
print("  prints `code/grain_axis_audit_03d1 present here:  NO` and reasons from")
print("  its absence.  It is present in the commit that ships that sentence.")

# ---------------------------------------------------------------------------
B.hdr("V1e  THE ORDERING -- DID THE SWEEP RUN BEFORE THE FIX?")

print("  The brief's first item, and it is not answerable from the report's")
print("  narrative.  If a runner was repaired between the count and the sweep,")
print("  the sweep is about a partly-repaired tree and the ticket's central")
print("  question is unanswered however green the output is.")
print()
print("  The test is a MODIFICATION and not an addition: a `run_all.sh` ADDED")
print("  in the window is a new tree, not a repaired one.  `--diff-filter=M`")
print("  over the window from mg-03d1's carrier to mg-ec63's carrier:")
print()
WINDOW = "eacc5e1..7fccb4e"
mods = B.git("log", "--format=%h\t%s", "--diff-filter=M", WINDOW,
             "--", "code/*/run_all.sh").splitlines()
raw = B.git("log", "--format=COMMIT\t%h", "--name-status", WINDOW,
            "--", "code/*/run_all.sh").splitlines()
touched = []
cur = None
for line in raw:
    if line.startswith("COMMIT\t"):
        cur = line.split("\t")[1]
    elif line[:1] in ("A", "M") and cur:
        touched.append((cur, line[0], line.split("\t")[-1]))
adds = [x for x in touched if x[1] == "A"]
modl = [x for x in touched if x[1] == "M"]
own = [x for x in modl if "truncate_sweep_ec63" in x[2]]
foreign = [x for x in modl if "truncate_sweep_ec63" not in x[2]]

print("  population: every commit in %s touching a `code/*/run_all.sh`" % WINDOW)
B.plain("...RUNNERS ADDED in the window", len(adds), "one file-change")
B.plain("...RUNNERS MODIFIED in the window", len(modl), "one file-change")
B.plain("...of those, in the SWEEP'S OWN tree", len(own), "one file-change")
B.plain("...of those, in ANY OTHER tree of the arc", len(foreign), "one file-change")
print()
for h, st, p in touched:
    print("      %s  %s  %s" % (h, st, p))
print()
# existed at eacc5e1 == `git ls-tree` at eacc5e1 lists the path.  ONE
# condition, so it can fail; an `and` whose first half is always true would be
# a green clause that measures nothing, which is this ticket's own shape.
pre_existing = [x for x in foreign
                if B.git("ls-tree", "eacc5e1", "--", x[2]).strip()]
B.plain("...MODIFICATIONS of a runner that EXISTED at eacc5e1, outside the "
        "sweep's own tree", len(pre_existing), "one file-change")
print()
if not pre_existing:
    print("  ZERO.  No runner of the arc that existed when the 43 was counted")
    print("  was edited before the sweep ran.  THE SWEEP RAN AGAINST AN")
    print("  UNREPAIRED ARC and the ordering the ticket demands was kept.")
else:
    print("  *** A PRE-EXISTING RUNNER WAS MODIFIED BEFORE THE SWEEP RAN ***")
print()
print("  Two qualifications, because the clean answer is the one nobody")
print("  double-checks:")
print()
print("  (1) The modifications that DID happen are each a ticket editing ITS")
print("      OWN runner -- mg-ec63's structural repair of its own transcript")
print("      writing, and mg-1abe's revision-resolution fix.  Neither is a")
print("      member of the population being swept for the defect.")
print("  (2) ONE TREE WAS ALREADY REPAIRED BEFORE EITHER MEASUREMENT.")
print("      `runner_exit_repair_bf79` carried the `.new`+`mv` fix before")
print("      mg-03d1 counted 43 and before mg-ec63 swept.  It is the ONLY")
print("      instance in the arc with a known positive on the record -- nine")
print("      hidden labels -- and neither measurement could observe it in its")
print("      defective state.  The sweep-then-fix ordering was kept for the")
print("      other %d; for the one that matters most it was already inverted,"
      % (len(sets["3fc870a"]) - 1))
print("      by a different ticket, before this arc began.  mg-ec63 saw this")
print("      and re-ran the control at 675c2ba rather than at HEAD.")

print()
print("V1 TOTAL REVISIONS WHERE THE SHIPPED FIGURE IS NOT REPRODUCIBLE: %d"
      % mismatch)
sys.exit(min(mismatch, 120))
