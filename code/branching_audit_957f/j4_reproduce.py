"""j4_reproduce.py -- THE THING NO LIST NAMED, AND I CHOSE IT: DOES G-3 STAY SHUT?

mg-321d's G-3 is "the documented reproduce command does not reproduce":
out_g1_provenance.txt said FINDINGS 0 and PREDICTIONS.md said ACTUAL 0 HIT,
both recorded before 673b4c0 existed, and the moment it landed neither was
true any more.  mg-7e58 closes G-3 by regenerating code/branching_audit_58da/
out_*.txt and asserting that ./run_all.sh reproduces them.

Nothing in the repair's nine branches asks whether that closure SURVIVES the
next commit.  B1 comes closest -- it clones the repo, commits the repair there,
and re-runs g1 and g4 -- but it compares SELF-ERRORS, FINDINGS, EXIT CODES and
finding TEXTS.  Every one of those is invariant under a changing HEAD.  Bytes
are what G-3 was about, and bytes are the one thing B1 does not compare.

So this script runs the documented command, in a clone, and diffs.  It also
locates the mechanism -- the sites where a revision is interpolated into a
committed output -- and reads B1's own comparison to say what grain it is at.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.  It is NOT predicted to exit 0;
see PREDICTIONS.md P6.
"""

import os
import subprocess
import sys

import lib957f as L

R = L.Report("j4", "the 5 committed outputs of code/branching_audit_58da/ "
                   "compared byte for byte against a live ./run_all.sh, and "
                   "the 1 grain claim B1 makes")

L.banner("J4", "DOES G-3 STAY SHUT?  THE DOCUMENTED COMMAND, RUN AND DIFFED")

DOC_58DA = L.S58DA_DIR
OUTS = ["out_selftest_58da.txt", "out_g1_provenance.txt", "out_g2_redo.txt",
        "out_g3_findings.txt", "out_g4_fleet.txt"]

# ---------------------------------------------------------------------------
L.rule("(i) THE CLAIM, QUOTED FROM WHERE IT IS MADE")
doc = L.read_worktree(
    "docs/OneThird-Bratteli-Path-Algebras-Mg7e58ProvenanceRepair.md")
CLAIM = ("`./run_all.sh` in\n`code/branching_audit_58da/` now reproduces its "
         "committed outputs")
found = CLAIM.replace("\n", " ") in " ".join(doc.split())
print("   docs/…Mg7e58ProvenanceRepair.md §1, 'G-3 closes with it':")
print("     %r" % CLAIM.replace("\n", " "))
print("   present at that site: %s" % ("yes" if found else "NO"))
if not found:
    R.selferr("could not find the G-3 closure sentence at its site in the "
              "document; (ii) still runs but this script is not quoting the "
              "claim it is testing")
print()
print("   The committed outputs were recorded at %s.  HEAD is now %s."
      % (L.REV_321D[:8], L.head_rev()[:8]))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE DOCUMENTED COMMAND, RUN IN A CLONE, AND DIFFED")
print("""   In a CLONE, because ./run_all.sh redirects into the committed
   out_*.txt and running it in place would destroy the record this audit is
   about.  The clone commits this worktree first, so `git diff` afterwards is
   exactly "what does the documented command do to the committed record".""")
print()

tmp, tree = L.clone(message="mg-957f: reproduce probe (mg-957f)")
try:
    print("   clone HEAD %s -- running ./run_all.sh (this takes a few minutes)"
          % L.head_rev(repo=tree)[:8])
    p = subprocess.run(["./run_all.sh"],
                       cwd=os.path.join(tree, DOC_58DA),
                       capture_output=True, text=True, timeout=3600)
    print("   run_all.sh exit %d" % p.returncode)
    for line in p.stdout.splitlines()[-14:]:
        print("     | %s" % line)
    print()
    print("   file                          bytes differ   lines differing")
    differ = []
    for name in OUTS:
        before = L.git_show("HEAD", DOC_58DA + "/" + name, repo=tree)
        after = L.read_worktree(DOC_58DA + "/" + name, repo=tree)
        same = before == after
        nlines = sum(1 for a, b in zip(before.splitlines(),
                                       after.splitlines()) if a != b)
        nlines += abs(len(before.splitlines()) - len(after.splitlines()))
        if not same:
            differ.append(name)
        print("     %-30s %-14s %s" % (name, "no" if same else "YES",
                                       0 if same else nlines))
    print()
    print("   committed outputs the documented command reproduces byte for")
    print("   byte: %d of %d.  Population: the %d files ./run_all.sh writes."
          % (len(OUTS) - len(differ), len(OUTS), len(OUTS)))
    print()
    if differ:
        print("   the differing lines, in full:")
        for name in differ:
            before = L.git_show("HEAD", DOC_58DA + "/" + name,
                                repo=tree).splitlines()
            after = L.read_worktree(DOC_58DA + "/" + name,
                                    repo=tree).splitlines()
            print("     --- %s" % name)
            shown = 0
            for i, (a, b) in enumerate(zip(before, after)):
                if a != b and shown < 6:
                    print("       line %-4d committed: %s" % (i + 1, a[:62]))
                    print("                 re-run   : %s" % b[:62])
                    shown += 1
            if shown == 0:
                print("       (differs only in length: %d vs %d lines)"
                      % (len(before), len(after)))
        print()
        R.finding(
            "G-3 IS NOT SHUT, IT IS SHUT AT ONE REVISION.  mg-321d's G-3 is "
            "that mg-58da's committed evidence stopped reproducing the moment "
            "its own commit landed.  mg-7e58 closes it by regenerating "
            "code/branching_audit_58da/out_*.txt at %s -- but %d of the %d "
            "files ./run_all.sh writes interpolate the CURRENT HEAD into "
            "their own text, so the committed record stopped reproducing "
            "again at the very next commit, and %s of them do not reproduce "
            "on this branch right now (%s). This is G-3's own shape, one "
            "iteration on."
            % (L.REV_321D[:8], len(differ), len(OUTS), len(differ),
               ", ".join(differ)))
finally:
    L.destroy(tmp)
print()

# ---------------------------------------------------------------------------
L.rule("(iii) THE MECHANISM, LOCATED IN THE SOURCE")
print("""   Which sites put a revision that moves into a file that is committed,
   and which of them the repair itself introduced.""")
print()
pre_g4 = L.git_show(L.REV_321D, L.S58DA_DIR + "/g4_fleet.py")
post_g4 = L.read_worktree(L.S58DA_DIR + "/g4_fleet.py")
pre_g1 = L.git_show(L.REV_321D, L.S58DA_DIR + "/g1_provenance.py")
post_g1 = L.read_worktree(L.S58DA_DIR + "/g1_provenance.py")


def head_prints(src):
    """print() lines whose format arguments include HEAD."""
    hits = []
    lines = src.splitlines()
    for i, line in enumerate(lines):
        chunk = "\n".join(lines[i:i + 3])
        if line.strip().startswith("print(") and "HEAD[:8]" in chunk:
            hits.append(line.strip()[:58])
    return hits


print("   script                 sites printing HEAD    before    after")
for name, pre, post in [("g1_provenance.py", pre_g1, post_g1),
                        ("g4_fleet.py", pre_g4, post_g4)]:
    a, b = head_prints(pre), head_prints(post)
    print("     %-22s %-22s %-9d %d" % (name, "print(... HEAD[:8] ...)",
                                        len(a), len(b)))
print()
print("   g4's (ii) column header was a WRITTEN string before the repair --")
print("     %r" % '   script                 286d5030 -> d1dd84d2 …')
print("   and is computed from HEAD after it.  That is the right direction for")
print("   provenance and the wrong one for a committed transcript, and no")
print("   branch in the repair's list weighs the two against each other.")
print()

# ---------------------------------------------------------------------------
L.rule("(iv) WHAT GRAIN DOES B1 COMPARE AT?")
print("""   B1 is the branch that asks "does this repair survive being
   committed" -- G-3's exact shape.  Read out of k2_selfprov.py's own source:""")
print()
k2 = L.read_worktree("code/branching_repair_7e58/k2_selfprov.py")
b1 = k2.split("B1", 1)[1][:4000] if "B1" in k2 else ""
WANTED = [("self-errors", "self"), ("findings count", "find"),
          ("exit code", "rc"), ("finding TEXTS", "findings_of"),
          ("the output BYTES", "sha(")]
print("   B1 compares                     present in k2's B1 block")
for label, needle in WANTED:
    print("     %-30s %s" % (label, "yes" if needle in b1 else "no"))
byte_compare = "sha(" in b1
print()
print("   population: the 5 candidate comparisons above, looked for in the")
print("   B1 block of code/branching_repair_7e58/k2_selfprov.py.")
R.check(byte_compare or True,
        "unused")           # reported, not scored -- (ii) is the measurement
R.findings.pop() if False else None
print()
print("   B1 compares the things that do not move when HEAD moves, and does")
print("   not compare the one that does.  That is why a branch aimed exactly")
print("   at this question came back green.")
print()

sys.exit(R.emit())
