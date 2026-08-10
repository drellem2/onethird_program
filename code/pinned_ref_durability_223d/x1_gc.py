"""mg-223d / X1 -- THE EXHIBIT.  A tag survives `gc`; a deleted branch's commit
does not; and a tree hash written into a file survives nothing at all.

NOT IN `run_all.sh`.  It clones this repository and runs `git gc --prune=now`,
which is exactly the operation this ticket is about, and running it in a
worktree would be the joke telling itself.  It refuses to start unless you give
it a sandbox path OUTSIDE this repository.

    python3 x1_gc.py --sandbox /tmp/223d-gc

WHAT IT IS FOR.  P3 says a tag survives the failure mode and a branch-held
commit does not.  That is a claim about `git gc`'s reachability rule, it is easy
to believe, and believing it is not the same as having watched it happen.  E5 is
the way this exhibit fails: an object surviving because of the REFLOG rather
than the tag.  So the run has THREE arms and the middle one exists only to catch
that -- gc is run once WITHOUT expiring the reflog, where the prediction is that
BOTH commits survive for the wrong reason.

The committed transcript is a DATED measurement, not a regenerated one.
"""
import argparse
import os
import shutil
import subprocess
import sys

import lib223d as L


def sh(*args, cwd=None, ok=(0,)):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if r.returncode not in ok:
        print("    ! %s -> exit %d\n      %s"
              % (" ".join(args[:4]), r.returncode, r.stderr.strip()[:200]))
    return r


def alive(repo, obj):
    return sh("git", "cat-file", "-e", obj, cwd=repo, ok=(0, 1, 128)
              ).returncode == 0


ap = argparse.ArgumentParser()
ap.add_argument("--sandbox", required=True)
a = ap.parse_args()
box = os.path.abspath(a.sandbox)
if box.startswith(L.REPO + os.sep) or box == L.REPO:
    sys.exit("REFUSING: --sandbox is inside the repository under test (%s)" % box)

led = L.Ledger("mg-223d / X1 -- DOES A TAG ACTUALLY SAVE IT?  RUN, NOT ASSERTED")

# The two subjects.  A is TAGGED, B is not, and they are otherwise identical in
# every respect that matters: both off-history, both held only by a polecat
# branch, both pinned by tracked code.
A_SHORT, B_SHORT = "9f1ecaa", "d33970b"
A_BR, B_BR = "polecat-z03d1", "polecat-z03d1"   # same branch holds both
A = L.resolve(A_SHORT)
B = L.resolve(B_SHORT)
TREE = L.git("rev-parse", A + "^{tree}").strip()

led.head("X1a  THE SANDBOX")
if os.path.exists(box):
    shutil.rmtree(box)
os.makedirs(box)
sh("git", "init", "-q", box)
# `--no-tags` IS THE WHOLE OF A DEFECT I COMMITTED AND KEPT (D12).  Without it,
# `git fetch` auto-follows tags that point into the fetched history -- which now
# means MY OWN `pin/*` tags, created by the repair this exhibit exists to test.
# The first run of this probe after `mktags.sh --push` therefore fetched
# `pin/d33970b` into the sandbox, kept the CONTROL commit alive, and turned a
# clean refutation into a false green.  A repair contaminating its own exhibit
# is the exact mirror defect this ticket is about, and it fired for real.
#
# Fetching `main` into `refs/heads/base` and not `refs/heads/main` is the second
# half: `git init` checks out `main`, and git refuses to fetch into a
# checked-out branch.  That refusal was TOLERATED SILENTLY by the first version
# of this probe, which is a second defect of the same family -- an arm that
# cannot tell `it ran` from `it was refused`.
r1 = sh("git", "fetch", "-q", "--no-tags", L.REPO,
        "refs/heads/main:refs/heads/base", cwd=box)
r2 = sh("git", "fetch", "-q", "--no-tags", L.REPO,
        "refs/remotes/origin/%s:refs/heads/%s" % (A_BR, A_BR), cwd=box)
if r1.returncode or r2.returncode:
    led.self_error("a sandbox fetch failed -- every arm below is void")
stray = [t for t in sh("git", "tag", "-l", "pin/*", cwd=box).stdout.split() if t]
if stray:
    sh("git", "tag", "-d", *stray, cwd=box)
led.record(not stray, "pin/* tags that leaked into the sandbox anyway: %d "
           "(deleted before the experiment)" % len(stray))
print()
print("      sandbox                     %s" % box)
print("      commit A (to be TAGGED)     %s  %s" % (A_SHORT, A[:12]))
print("      commit B (left UNTAGGED)    %s  %s" % (B_SHORT, B[:12]))
print("      A's TREE object             %s" % TREE[:12])
print("      both held in the sandbox by refs/heads/%s and nothing else" % A_BR)
led.record(alive(box, A) and alive(box, B), "both commits present in the sandbox")
led.record(alive(box, TREE), "A's tree object present in the sandbox")

led.head("X1b  THE TAG -- THE REPAIR, APPLIED TO A ONLY")
rt = sh("git", "tag", "-a", L.tag_name(A), A, "-m", "keep-alive anchor (mg-223d)",
        cwd=box)
tags = sh("git", "tag", "-l", cwd=box).stdout.split()
led.record(L.tag_name(A) in tags and rt.returncode == 0,
           "tag %s created HERE, by this probe (exit %d)"
           % (L.tag_name(A), rt.returncode))
print("      B GETS NOTHING.  That asymmetry is the whole experiment: A and B")
print("      are on the same branch, pinned the same way, differing in one ref.")

led.head("X1c  THE FAILURE MODE, PERFORMED -- prune the merged branch")
sh("git", "branch", "-D", A_BR, cwd=box)
print()
print("      refs remaining in the sandbox:")
for r in sh("git", "for-each-ref", "--format=%(refname)", cwd=box).stdout.split():
    print("        %s" % r)
print("""
      That is the real sequence and nothing about it is exotic: the branch was
      MERGED, so deleting it is hygiene.  `pogo refinery prune` does it.
      GitHub offers it on every merge.  `git fetch --prune` then drops the
      remote-tracking copy.""")

led.head("X1d  ARM 1 -- gc WITHOUT expiring the reflog (THE E5 TRAP)")
sh("git", "gc", "--prune=now", "-q", cwd=box, ok=(0, 1))
a1, b1 = alive(box, A), alive(box, B)
print()
print("      A (tagged)    survives: %s" % a1)
print("      B (untagged)  survives: %s" % b1)
led.record(None, "arm 1 -- A=%s B=%s" % (a1, b1))
print("""      IF B SURVIVES HERE IT IS NOT EVIDENCE FOR ANYTHING.  `git gc`
      treats the reflog as a root, and a freshly-fetched branch has one.  This
      arm exists so that a survival I could not attribute to the tag is on the
      page instead of being quietly absent.""")

led.head("X1e  ARM 2 -- reflog expired, THEN gc.  The real question.")
sh("git", "reflog", "expire", "--expire=now", "--expire-unreachable=now",
   "--all", cwd=box, ok=(0, 1))
sh("git", "gc", "--prune=now", "-q", cwd=box, ok=(0, 1))
a2, b2 = alive(box, A), alive(box, B)
t2 = alive(box, TREE)
print()
print("      A (TAGGED)      survives: %-5s   <- the repair" % a2)
print("      B (untagged)    survives: %-5s   <- the control" % b2)
print("      A's TREE object survives: %-5s" % t2)
led.record(a2, "THE TAGGED COMMIT SURVIVED `git gc --prune=now`")
led.record(not b2, "THE UNTAGGED COMMIT DID NOT -- the mechanism is real and "
           "it is one prune plus one gc away")

led.head("X1f  ARM 3 -- AND THE OPTION THAT LOOKS CHEAPEST DOES NOTHING")
print("""
  The ticket's second option is `committing the two tree hashes with the
  figure`.  The sandbox now answers it, and the answer is not a matter of
  degree:""")
b_tree = L.git("rev-parse", B + "^{tree}").strip()
bt = alive(box, b_tree)
print()
print("      B's tree sha, as it would be WRITTEN INTO A COMMITTED FILE:")
print("          %s" % b_tree)
print("      that object, after the prune and the gc:  %s" % ("present" if bt else "GONE"))
led.record(not bt, "A TREE SHA IN A TEXT FILE IS NOT A REF.  `gc` collects an "
           "unreachable tree exactly as it collects an unreachable commit; "
           "recording the hash records WHICH object you needed, not the object")
print("""
      SO OPTION (b) IS NOT A WEAKER VERSION OF OPTION (a).  It is a record of
      the loss, written in advance, in a format that reads like a remedy.
      That is worth stating plainly because it is the option a reader reaches
      for first: it needs no ref, no push, and no permission.""")

print()
print("      sandbox left in place for inspection: %s" % box)
sys.exit(led.done())
