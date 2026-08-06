"""mg-03d1 / A4 -- THE `>`-BEFORE-PROBE SHAPE, SWEPT ACROSS THE WHOLE ARC.

The parent's self-reported defect #7: `run_all.sh` redirected each probe's
output with `>`, which TRUNCATES THE FILE BEFORE THE PROBE STARTS -- so the
probe whose job is to census every count this tree prints had its own
transcript, alone of all artifacts, empty while it read them.  It hid NINE
offending labels.  Fixed structurally in ONE directory.

THE PARENT FIXED ITS OWN AND DID NOT SWEEP, and the addendum says so.  This is
the sweep.  The number that matters is not `how many runners truncate` -- that
is nearly all of them and mostly harmless.  It is HOW MANY TRUNCATE A FILE THAT
A PROBE OF THE SAME RUN THEN READS, because that is where the shape bites.

Exit code = trees where the shape bites (a finding, not a breakage).
"""

import os
import re
import sys

import lib03d1 as B

A = B.A

print("mg-03d1 / A4 -- THE TRUNCATE-BEFORE-PROBE SWEEP")
print("HEAD: %s" % B.head())

# ---------------------------------------------------------------------------
B.hdr("A4a  THE POPULATION, AND HOW EACH RUNNER REDIRECTS")

TREES = B.trees()
print("  population: every directory under `code/` holding a `run_all.sh`,")
print("  found by a glob over the whole of `code/` -- a PROPERTY, not a list")
B.plain("...RUNNERS in the arc", len(TREES))
print("      ^ one unit of that number is one `run_all.sh`")
print()

MINE = "code/%s" % os.path.basename(os.path.dirname(os.path.abspath(__file__)))
TRUNC = re.compile(r"(?<![>2])>\s*[\"']?\$?\{?_?[oO]|(?<![>2])>\s*[\"']?out_")
trunc, newmv, neither = [], [], []
for t in TREES:
    src = B.read("%s/run_all.sh" % t)
    if re.search(r"\.new", src) and re.search(r"\bmv\b", src):
        newmv.append(t)
    elif TRUNC.search(src):
        trunc.append(t)
    else:
        neither.append(t)
print("  population: the %d RUNNERS above, by how each writes its transcripts"
      % len(TREES))
B.plain("...RUNNERS that redirect with a plain `>`", len(trunc))
print("      ^ one unit of that number is one `run_all.sh`")
B.plain("...RUNNERS that write `.new` and `mv` it", len(newmv))
print("      ^ one unit of that number is one `run_all.sh`")
for t in newmv:
    print("          %s%s" % (t, "   <- THIS AUDIT'S OWN" if t == MINE else ""))
B.plain("...of those, RUNNERS of the arc this audit is about",
        len([t for t in newmv if t != MINE]))
print("      ^ one unit of that number is one `run_all.sh`")
B.plain("...RUNNERS doing neither (no transcript redirect)", len(neither))
print("      ^ one unit of that number is one `run_all.sh`")
print()
print("  BOTH NUMBERS ARE PRINTED BECAUSE THE AUDITOR JOINED THE POPULATION.")
print("  A4b was pre-registered as `exactly 1 -- the parent's` and the arc")
print("  had exactly 1 when that was written.  It has %d now, because adopting"
      % len(newmv))
print("  the parent's fix in this tree's own runner ADDED A MEMBER TO THE SET")
print("  I AM COUNTING.  Excluding myself to protect the prediction would be")
print("  the population defect this arc keeps recording, so the total stands")
print("  at %d and the sub-count is printed beside it." % len(newmv))
subjects = [t for t in newmv if t != MINE]

# ---------------------------------------------------------------------------
B.hdr("A4b  AND WHERE THE SHAPE ACTUALLY BITES")

print("  A truncating runner is harmless unless a probe of the SAME RUN reads")
print("  a transcript that run has already emptied.  The test, per tree:")
print()
print("    (i)  the runner truncates `out_X.txt` before running probe X, AND")
print("    (ii) some probe of that tree reads `out_*.txt` of its OWN tree --")
print("         by `outs(...)`, by a glob, or by naming an `out_` path.")
print()
print("  Then, on every run, at least one member of the census is empty at the")
print("  moment it is censused, and the census cannot see it.")
print()
READS_OWN = re.compile(r"\bouts\s*\(|glob\.glob\([^)]*out_|[\"']out_[a-z0-9_]*"
                       r"\.txt[\"']|\bout_\*\.txt\b")
bites = []
for t in trunc:
    probes = sorted(f for f in os.listdir(os.path.join(B.REPO, t))
                    if f.endswith(".py"))
    hits = []
    for f in probes:
        try:
            s = B.read("%s/%s" % (t, f))
        except OSError:
            continue
        if READS_OWN.search(s):
            hits.append(f)
    if hits:
        bites.append((t, hits))
print("  population: the %d TRUNCATING RUNNERS of A4a" % len(trunc))
B.plain("...RUNNERS whose own probes read `out_*.txt`", len(bites))
print("      ^ one unit of that number is one `run_all.sh`")
B.plain("...RUNNERS where the shape is inert", len(trunc) - len(bites))
print("      ^ one unit of that number is one `run_all.sh`")
print()
print("  THE TREES WHERE IT BITES, with the reading probes named so each row")
print("  can be checked:")
print()
for t, hits in bites:
    print("      %-44s %s" % (t, ", ".join(hits[:3])
                              + (" +%d" % (len(hits) - 3) if len(hits) > 3
                                 else "")))
print()
print("  THIS IS A FINDING AND NOT A REPAIR.  Fixing %d runners would rewrite"
      % len(bites))
print("  %d trees' committed transcripts, every one of them another ticket's" % len(bites))
print("  evidence, and this is an audit.  What the sweep establishes is that")
print("  the parent's defect #7 is a PROPERTY OF THE ARC'S RUNNER IDIOM and not")
print("  of one script: %d of %d runners carry the shape and %d of them have a"
      % (len(trunc), len(TREES), len(bites)))
print("  probe that reads what the runner just emptied.  %d of the %d have the"
      % (len(newmv), len(TREES)))
print("  structural fix: the one that found the defect, and this audit.")

# ---------------------------------------------------------------------------
B.hdr("A4c  AND THE FIX'S OWN LIMIT, RE-DERIVED RATHER THAN QUOTED")

print("  The parent states the limit of its own `mv`: a probe KILLED mid-write")
print("  leaves an `out_X.txt.new`, which no corpus picks up because it does")
print("  not end in `.txt`.  Checked here against the corpus rule that would")
print("  have to pick it up:")
print()
stale = [p for p in os.listdir(os.path.join(B.REPO, subjects[0]))
         if p.endswith(".new")] if subjects else []
globbed = A.outs(subjects[0]) if subjects else []
print("  population: the files on disk in `%s`"
      % (subjects[0] if subjects else "(none)"))
B.plain("...FILES ending `.new` left behind", len(stale))
print("      ^ one unit of that number is one file")
B.plain("...ARTIFACTS `lib56dc.outs()` picks up there", len(globbed))
print("      ^ one unit of that number is one file")
print()
print("  The claim `no corpus picks up a .new` is a claim about the GLOB, so")
print("  it is checked against the glob: `out_*.txt` cannot match a name ending")
print("  `.new`, and %d of %d files there are picked up.  The guarantee is that"
      % (len(globbed), len(globbed) + len(stale)))
print("  small, and the parent says so in the runner itself.")

# ---------------------------------------------------------------------------
B.hdr("A4d  DOES THE FIX CONVERGE?  RUN IT TWICE AND DIFF -- THEN RESTORE")

print("  The parent's claim is that with the `mv`, the previous run's bytes")
print("  survive the probe, so TWO CONSECUTIVE RUNS CONVERGE.  That is a claim")
print("  about running it twice and is checked by running it twice.")
print()
print("  THIS PROBE WRITES.  It regenerates another ticket's committed")
print("  transcripts and then RESTORES THE EXACT BYTES with `git checkout --`,")
print("  asserting cleanliness afterwards and going red if the restore fails.")
print("  That is mg-7522's S2 idiom.  The brief forbids LEAVING another")
print("  ticket's evidence regenerated; it does not forbid running it.")
print()
print("  AND THE SUBJECT OF THIS SECTION IS NAMED, NOT TAKEN BY POSITION.")
print("  Its first version took `newmv[0]` -- the first tree with the fix --")
print("  which was the parent's until this tree adopted the fix, and then it")
print("  was THIS ONE, alphabetically first.  The probe ran its own runner,")
print("  which ran this probe, which ran its own runner.  See a6_self.py/AS7:")
print("  a population that silently includes the auditor, which is O2's shape")
print("  a third time, in the sweep that measures O2's runner defect.")
print()
FAIL = 0
if subjects:
    import subprocess
    tree = subjects[0]
    d = os.path.join(B.REPO, tree)
    before = B.git("status", "--porcelain", "--", tree).strip()
    try:
        snaps = []
        for k in (1, 2):
            subprocess.run(["sh", "./run_all.sh"], cwd=d, capture_output=True,
                           text=True, timeout=1800)
            snaps.append({f: open(os.path.join(d, f), "rb").read()
                          for f in sorted(os.listdir(d))
                          if f.startswith("out_") and f.endswith(".txt")})
        same = [f for f in snaps[0] if snaps[0][f] == snaps[1].get(f)]
        print("  population: the TRANSCRIPTS `%s` writes" % tree)
        B.plain("...TRANSCRIPTS written by each run", len(snaps[0]))
        print("      ^ one unit of that number is one file")
        B.plain("...TRANSCRIPTS byte-identical across two runs", len(same))
        print("      ^ one unit of that number is one file")
        B.plain("...TRANSCRIPTS that still differ on the second run",
                len(snaps[0]) - len(same))
        print("      ^ one unit of that number is one file")
        for f in sorted(set(snaps[0]) - set(same)):
            print("          differs: %s" % f)
        print()
        print("  A transcript that differs between two consecutive runs at a")
        print("  FIXED tree is a probe reading something the run itself moved.")
        print("  Under the old `>` idiom the self-census could never converge,")
        print("  because its own transcript was empty when it read it and full")
        print("  when it was compared.")
    finally:
        for f in os.listdir(d):
            if f.endswith(".new"):
                os.remove(os.path.join(d, f))
        B.git("checkout", "--", tree)
        after = B.git("status", "--porcelain", "--", tree).strip()
        ok = after == before
        print()
        print("      the tree is restored to its committed bytes    %s"
              % ("yes" if ok else "*** NO -- RESTORE FAILED ***"))
        if not ok:
            FAIL += 1
            print("          %s" % after[:300])
else:
    print("      (no `.new`/`mv` runner found -- nothing to converge)")

print()
print("A4 TOTAL FINDINGS: %d" % (len(bites) + FAIL))
sys.exit(min(len(bites) + FAIL, 120))
