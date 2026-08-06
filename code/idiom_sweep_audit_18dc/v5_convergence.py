"""mg-18dc / V5 -- THE FIX'S CONVERGENCE, AND THE RESTORE THAT IS SCOPED SMALLER
THAN THE RUN.

The brief asks two things of mg-03d1's A4d, which verified 6-of-6 transcripts
byte-identical over two consecutive runs of `runner_exit_repair_bf79`:

  (i)  re-verify on a tree it did NOT use
  (ii) check the restore to committed bytes actually restored them --
       COMPARE HASHES, NOT STATUS

and there is a third thing A4d's own source shows without being asked:

  (iii) the restore is `git status --porcelain -- <tree>`, ONE DIRECTORY.  The
        run is not scoped to one directory.  A restore scoped to the population
        being measured misses exactly the places the measurement spills into --
        which is mg-ec63's b9fc6a9 finding, arrived at from the other end.

All of it happens in a disposable clone, so an incomplete restore here damages
nothing.  That is also why it can be tested at all: the honest way to check a
restore is to break it.

Exit code = failures of the fix or of the restore.
"""

import hashlib
import os
import re
import subprocess
import sys

import lib18dc as B

REV = "3fc870a"
FAIL = 0

print("mg-18dc / V5 -- CONVERGENCE AND RESTORE")
print("HEAD: %s" % B.head())
print("MEASURED AT: %s" % REV)

sbx = B.sandbox(REV, tag="%s-v5" % REV)
TREES = B.runners_at(REV)

newmv = []
for t in TREES:
    src = open(os.path.join(sbx, t, "run_all.sh")).read()
    if re.search(r"\.new", src) and re.search(r"\bmv\b", src):
        newmv.append(t)

# ---------------------------------------------------------------------------
B.hdr("V5a  WHICH TREES CARRY THE FIX AT ALL")

print("  population: the %d runners tracked at %s" % (len(TREES), REV))
B.plain("...RUNNERS carrying the `.new`+`mv` structural fix", len(newmv),
        "one `run_all.sh`")
for t in newmv:
    print("          %s" % t.replace("code/", ""))
B.plain("...RUNNERS NOT carrying it", len(TREES) - len(newmv), "one `run_all.sh`")
print()
print("  mg-03d1's A4d took `subjects[0]` -- the first `.new`+`mv` tree that is")
print("  not its own -- which was and is `runner_exit_repair_bf79`.  A tree it")
print("  did NOT use is therefore any other member of this set.")

# ---------------------------------------------------------------------------
B.hdr("V5b  CONVERGENCE ON A TREE mg-03d1 DID NOT USE")


def hashes(d):
    out = {}
    for f in sorted(os.listdir(d)):
        if f.startswith("out_") and f.endswith(".txt"):
            out[f] = hashlib.sha256(open(os.path.join(d, f), "rb").read()).hexdigest()
    return out


def committed_hashes(tree):
    out = {}
    ls = B.git("ls-tree", "-r", "--name-only", REV, "--", tree).splitlines()
    for p in ls:
        b = os.path.basename(p)
        if b.startswith("out_") and b.endswith(".txt"):
            blob = subprocess.run(["git", "show", "%s:%s" % (REV, p)],
                                  cwd=B.REPO, capture_output=True).stdout
            out[b] = hashlib.sha256(blob).hexdigest()
    return out


targets = [t for t in newmv if "bf79" not in t] or newmv
for tree in targets:
    d = os.path.join(sbx, tree)
    print("  SUBJECT: %s" % tree)
    print("  population: the transcripts `%s` writes" % tree.replace("code/", ""))
    snaps = []
    to = False
    for k in (1, 2):
        try:
            subprocess.run(["sh", "./run_all.sh"], cwd=d, capture_output=True,
                           timeout=1200)
        except subprocess.TimeoutExpired:
            to = True
        snaps.append(hashes(d))
    if to:
        print("      *** a run was KILLED at 1200 s -- this row is UNMEASURED ***")
        FAIL += 1
    same = [f for f in snaps[0] if snaps[0][f] == snaps[1].get(f)]
    B.plain("...TRANSCRIPTS written by each run", len(snaps[0]), "one file")
    B.plain("...TRANSCRIPTS byte-identical across two consecutive runs",
            len(same), "one file")
    B.plain("...TRANSCRIPTS that still differ on the second run",
            len(snaps[0]) - len(same), "one file")
    for f in sorted(set(snaps[0]) - set(same)):
        print("          differs: %s" % f)
    if len(same) != len(snaps[0]):
        FAIL += 1

    # -- (ii) restore BY HASH, and over the WHOLE tree
    print()
    print("  THE RESTORE, CHECKED BY CONTENT AND NOT BY STATUS:")
    cm = committed_hashes(tree)
    before_bad = [f for f in cm if cm[f] != snaps[1].get(f)]
    B.plain("...TRANSCRIPTS differing from committed BEFORE the restore",
            len(before_bad), "one file")
    subprocess.run(["git", "checkout", "--quiet", "--", tree], cwd=sbx,
                   capture_output=True)
    subprocess.run(["git", "clean", "-qfd", "--", tree], cwd=sbx,
                   capture_output=True)
    now = hashes(d)
    after_bad = [f for f in cm if cm[f] != now.get(f)]
    B.plain("...TRANSCRIPTS differing from committed AFTER the restore",
            len(after_bad), "one file")
    for f in after_bad:
        print("          *** NOT RESTORED: %s ***" % f)
    if after_bad:
        FAIL += 1
    print()
    print("  A run that leaves 0 files differing before the restore would make")
    print("  the restore untestable -- there would be nothing to restore.  The")
    print("  BEFORE row is printed for exactly that reason.")
    print()

# ---------------------------------------------------------------------------
B.hdr("V5c  THE RESTORE IS SCOPED TO ONE DIRECTORY.  THE RUN IS NOT.")

print("  mg-03d1's A4d asserts `git status --porcelain -- <tree>` and goes red")
print("  if that one directory is dirty.  Here is the same run measured over")
print("  THE WHOLE WORKING TREE, which is the scope the run actually has.")
print()
subject = "code/runner_exit_repair_bf79"
B.sandbox_reset(sbx)
d = os.path.join(sbx, subject)
try:
    subprocess.run(["sh", "./run_all.sh"], cwd=d, capture_output=True, timeout=1200)
except subprocess.TimeoutExpired:
    pass
allpaths = B.dirty(sbx)
inside = [p for p in allpaths if p.startswith(subject)]
outside = [p for p in allpaths if not p.startswith(subject)]
print("  population: every path in the clone differing from %s after ONE run" % REV)
print("              of `%s/run_all.sh`" % subject.replace("code/", ""))
B.plain("...PATHS dirty inside the subject directory", len(inside), "one path")
B.plain("...PATHS dirty OUTSIDE it -- invisible to A4d's assertion",
        len(outside), "one path")
for p in outside[:40]:
    print("          %s" % p)
if outside:
    print()
    print("  A4d would have printed `the tree is restored to its committed")
    print("  bytes: yes` with those still on disk.  The check is true and the")
    print("  sentence it licenses is wider than the check.")
B.sandbox_reset(sbx)

print()
print("V5 TOTAL FAILURES OF THE FIX OR THE RESTORE: %d" % FAIL)
sys.exit(min(FAIL, 120))
