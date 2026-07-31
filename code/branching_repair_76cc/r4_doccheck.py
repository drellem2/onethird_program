"""r4_doccheck.py -- THIS DELIVERABLE, CHECKED FOR THE DEFECT IT REMEDIES.

mg-76cc restores detection.  So it can remove detection, and the ticket that
asked for it said so: identify what kind of artifact you are producing and
check it for the defect it remedies; enumerate what you checked; and if a
branch honestly cannot exhibit the defect, say so with the reason.

The defect, stated so it can be looked for: A CHECK THAT USED TO FIRE AND NOW
DOES NOT, invisible from the new side because the thing that would have
complained is gone.

This deliverable has six branches and they are enumerated in (i) with where
each is checked -- or, for the one that cannot exhibit the defect, why not.
(ii) checks the document against the runs rather than the other way round.
(iii) checks that the G-3 claim was NARROWED and not re-asserted.  (iv) runs
the runner with a red script in it, because a runner that swallows an exit code
removes detection from everything below it at once (mg-c2b3).

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import shutil
import subprocess
import sys
import tempfile

import lib76cc as L

R = L.Report(
    selfpop="every file read, temp tree and subprocess run this script "
            "performs",
    findpop="the 6 branches of this deliverable in (i), every figure of the "
            "form 'N of M' in the mg-76cc document (ii), the 3 claim rows in "
            "(iii), and the 2 runner rows in (iv)")

HERE_REL = "code/branching_repair_76cc"
DOC_REL = "docs/repair-mg-76cc-kernel-half-and-five-outputs.md"
MG7E58_DOC = "docs/OneThird-Bratteli-Path-Algebras-Mg7e58ProvenanceRepair.md"
OUTS = ["out_r1_kernel.txt", "out_r2_reproduce.txt", "out_r3_prerepair.txt"]

L.banner("R4", "THE DELIVERABLE, CHECKED FOR THE DEFECT IT REMEDIES")
print("""
It restores detection, so it can remove detection.  Enumerated, branch by
branch, with the one branch that cannot exhibit it named and reasoned rather
than left out.
""")

# ---------------------------------------------------------------------------
L.rule("(i) THE SIX BRANCHES, AND WHERE EACH IS CHECKED")

BRANCHES = [
    ("g1_provenance.py section (v)",
     "predicate", True,
     "r1 (v): each unit mg-76cc added deleted ALONE, in the tree where its "
     "effect exists, including the one-line F-1 REINTRODUCTION which must "
     "make g1's own kernel probe MISS",
     "r1_kernel.py"),
    ("lib58da.run_c1's two new arguments",
     "tool under every predicate in the directory", True,
     "r3 (iv): the 4 scripts this repair never opened, run end to end in two "
     "clones, with the library before and after, compared under the named "
     "normalisation",
     "r3_prerepair.py"),
    ("the g1 SELF-ERRORS population line",
     "declared unit", True,
     "it was a WRITTEN formula (3 + len(paths) * 3) that could not move when "
     "its own patch moved; it is now COUNTED from the reads actually "
     "performed, and r3 (iii) runs the predicate that prints it",
     "r3_prerepair.py"),
    ("r1 / r2 / r3 -- this instrument",
     "gates", True,
     "selftest_76cc.py asserts every helper they rest on is non-vacuous, and "
     "r1 (v) and r2 (vi) each carry a control in which the gate must go red",
     "selftest_76cc.py"),
    ("run_all.sh",
     "runner", True,
     "(iv) below: a red script is put through the real runner and its exit "
     "code must survive (mg-c2b3's class)",
     "r4_doccheck.py"),
    ("PREDICTIONS.md",
     "record", False,
     "IT CANNOT EXHIBIT THE DEFECT, and the reason is that it is not read by "
     "anything: no script parses it, no gate rests on it, and deleting it "
     "changes no exit code.  It is a record of what was predicted before the "
     "run, kept with its misses; a record can be WRONG, which (ii) is about, "
     "but it cannot go quiet",
     "-"),
]

print()
print("   branch                              kind        can remove  checked "
      "in")
print("                                                   detection?")
for name, kind, can, how, where in BRANCHES:
    print("     %-33s %-11s %-11s %s"
          % (name[:33], kind[:11], "YES" if can else "no", where))
print()
for name, kind, can, how, where in BRANCHES:
    print("     %s" % name)
    for i in range(0, len(how), 68):
        print("        %s" % how[i:i + 68])
print()
checked = [b for b in BRANCHES if b[2]]
print("   branches that can exhibit the defect : %d of %d, each with a named "
      "check" % (len(checked), len(BRANCHES)))
print("   branches that cannot                 : %d, with the reason stated"
      % (len(BRANCHES) - len(checked)))
R.gate(all(b[3] for b in BRANCHES),
       "a branch of this deliverable is enumerated with no check and no "
       "reason")
for name, kind, can, how, where in BRANCHES:
    if where == "-":
        continue
    exists = os.path.exists(os.path.join(L.REPO, HERE_REL, where))
    R.gate(exists,
           "branch %r says it is checked in %s, and that file does not exist"
           % (name, where))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) EVERY FIGURE IN THE DOCUMENT, ANCHORED TO A RUN")
print("""   Figures of the form "N of M" in the mg-76cc document, each looked
   for in the stdout of the run that is supposed to have produced it.  A
   figure a reader cannot find in an output is a figure this instrument
   did not measure.""")
print()

doc = None
try:
    doc = L.read_worktree(DOC_REL)
except IOError:
    R.selferr("the document %s does not exist; (ii) is withdrawn rather than "
              "counted as passing" % DOC_REL)

corpus = ""
for name in OUTS:
    try:
        corpus += L.read_worktree(HERE_REL + "/" + name)
    except IOError:
        R.selferr("%s has not been produced; the anchoring in (ii) is over a "
                  "smaller corpus than it claims" % name)


def figures(text):
    """Every 'N of M' with N and M whole numbers, in order of appearance."""
    got, toks = [], text.replace("**", " ").replace("`", " ").split()
    for i in range(len(toks) - 2):
        a, of, b = toks[i], toks[i + 1], toks[i + 2]
        b = b.rstrip(".,;:)")
        if of == "of" and a.isdigit() and b.isdigit():
            got.append((int(a), int(b)))
    return got


if doc is not None:
    figs = figures(doc)
    seen, missing = [], []
    for a, b in figs:
        if (a, b) in seen:
            continue
        seen.append((a, b))
        forms = ["%d of %d" % (a, b), "%d of %-2d" % (a, b),
                 ": %d of %d" % (a, b)]
        if not any(f in corpus for f in forms):
            missing.append((a, b))
    print("   distinct 'N of M' figures in the document : %d" % len(seen))
    for a, b in seen:
        print("     %-10s %s" % ("%d of %d" % (a, b),
                                 "anchored" if (a, b) not in missing
                                 else "NOT FOUND in any out_r*.txt"))
    print()
    print("   unanchored : %d" % len(missing))
    R.gate(not missing,
           "%d figure(s) in %s appear in no out_r*.txt: %s"
           % (len(missing), DOC_REL,
              ", ".join("%d of %d" % m for m in missing)))
print()

# ---------------------------------------------------------------------------
L.rule("(iii) THE G-3 CLAIM WAS NARROWED, NOT RE-ASSERTED")
print("""   mg-957f's F-2 is that G-3 was shut on 1 of 5.  The answer here is
   five, under a normalisation that is named -- which means the ABSOLUTE
   claim has to go, in the document that made it, or the same sentence
   is still there saying the same wrong thing.""")
print()

ABSOLUTE = ("./run_all.sh in code/branching_audit_58da/ now reproduces its "
            "committed outputs")
NARROWED = "reproduces its committed outputs up to the revision it names"
REMAINS = "the revision token itself is not reproduced"

def flatten(text):
    """Markdown emphasis and code ticks removed, whitespace collapsed, and
    LOWERCASED -- a sentence that is present but capitalised differently is
    present.  Matching case here once cost this script a finding against a
    document that said exactly what it was asked to say."""
    for ch in ("`", "*", "_"):
        text = text.replace(ch, " ")
    return " ".join(text.lower().split())


CLAIMROWS = []
try:
    old_doc = flatten(L.read_worktree(MG7E58_DOC))
    CLAIMROWS.append(("the ABSOLUTE claim is gone from %s"
                      % MG7E58_DOC.split("/")[-1],
                      flatten(ABSOLUTE) not in old_doc))
    CLAIMROWS.append(("the NARROWED claim is present there",
                      flatten(NARROWED) in old_doc))
except IOError:
    R.selferr("could not read %s; the claim rows are withdrawn" % MG7E58_DOC)
if doc is not None:
    CLAIMROWS.append(("the mg-76cc document says WHAT REMAINS",
                      flatten(REMAINS) in flatten(doc)))

for label, ok in CLAIMROWS:
    print("     %-58s %s" % (label, "yes" if ok else "NO"))
    R.gate(ok, "%s -- it is not" % label)
print()

# ---------------------------------------------------------------------------
L.rule("(iv) THE RUNNER CANNOT SWALLOW A RED SCRIPT -- RUN, NOT READ")
print("""   mg-c2b3 swept this arc for runners whose exit code was eaten by a
   pipe.  A runner that does that removes detection from every script
   under it at once, which is this deliverable's own defect at the
   coarsest possible grain.  So the real run_all.sh is copied into a temp
   tree with every script replaced by a stub, and one stub made red.""")
print()

runner = L.read_worktree(HERE_REL + "/run_all.sh")


def real_pipes(line):
    """`|` that is a pipe, not the `||` of a shell or-list.  Counting `||` as
    a pipe is how a check reports a defect that is not there, which is the
    mirror image of this deliverable's own class."""
    n, i = 0, 0
    while i < len(line):
        if line[i] == "|":
            if i + 1 < len(line) and line[i + 1] == "|":
                i += 2
                continue
            n += 1
        i += 1
    return n


piped = [l.strip() for l in runner.splitlines()
         if not l.strip().startswith("#") and real_pipes(l)]
orlists = [l.strip() for l in runner.splitlines()
           if not l.strip().startswith("#") and "||" in l]
print("   lines in run_all.sh carrying a real pipe : %d" % len(piped))
for l in piped:
    print("     %s" % l[:80])
print("   lines carrying `||`, which is not a pipe : %d" % len(orlists))
for l in orlists:
    print("     %s" % l[:80])
R.gate(not piped,
       "run_all.sh pipes on %d line(s): %s.  A pipe there is how the exit code "
       "of everything below it stops being reported (mg-c2b3)"
       % (len(piped), "; ".join(piped)))

STUBS = ["selftest_76cc.py", "r1_kernel.py", "r2_reproduce.py",
         "r3_prerepair.py", "r4_doccheck.py"]
for red in (None, "r2_reproduce.py"):
    tmp = tempfile.mkdtemp(prefix="mg76cc-runner-")
    try:
        d = os.path.join(tmp, "dir")
        os.makedirs(d)
        with open(os.path.join(d, "run_all.sh"), "w") as fh:
            fh.write(runner)
        os.chmod(os.path.join(d, "run_all.sh"), 0o755)
        for name in STUBS:
            with open(os.path.join(d, name), "w") as fh:
                fh.write("import sys\nprint('TOTAL BAD: %d')\nsys.exit(%d)\n"
                         % ((1, 1) if name == red else (0, 0)))
        p = subprocess.run(["./run_all.sh"], cwd=d, capture_output=True,
                           text=True, timeout=600)
        rc = p.returncode
        pred = 1 if red else 0
        print("     every stub green" if red is None
              else "     %s made red" % red)
        print("       predicted exit %d   actual exit %d   %s"
              % (pred, rc, "HIT" if rc == pred else "MISS"))
        R.gate(rc == pred,
               "the runner exits %d when %s; a red script under it is %s"
               % (rc, "every script is green" if red is None
                  else "%s exits 1" % red,
                  "invisible" if red else "reported where there is none"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
print()

# ---------------------------------------------------------------------------
L.rule("VERDICT")
print("""   THE DELIVERABLE IS OF THE SAME KIND AS THE DEFECT IT REPAIRS, AND IT
   WAS CHECKED FOR IT.  %d branches, %d of which can remove detection and
   each of which has a named check; %d that cannot, with the reason given
   rather than the branch omitted.  The document's figures are anchored
   to the runs, the absolute G-3 claim is withdrawn where it was made,
   and the runner is shown propagating a red script rather than read for
   pipes.
""" % (len(BRANCHES), len(checked), len(BRANCHES) - len(checked)))

sys.exit(R.emit())
