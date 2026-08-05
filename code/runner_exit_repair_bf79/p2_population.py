"""P2 -- O2.  THE STRICTEST SELF-RULE RANGED OVER ONE DIRECTORY'S TRANSCRIPTS.

THE FINDING (mg-56dc/T2a).  `r6_self.py`'s E1 -- *is every count's grain
stated?*, the strictest rule mg-70c7 applies to anything -- iterated
`M.outs(M.TREE)`: the `out_*.txt` of ONE DIRECTORY.

> A self-check whose population is a directory is a population defined by a
> path, which this arc has now named three times.

AND THE THIRD TIME WAS INSIDE THE TREE THAT REPAIRED THE OTHER TWO.  mg-dee4's
F5 was *a population defined by a list of two NAMES* and mg-70c7 repaired it
with `libc2b3.targets`, a property.  Its own self-check kept the shape.

THE REPAIR.  `lib70c7.published_by` -- a PROPERTY, put to the whole repository:
*a tracked file that a commit of this deliverable ADDED, that still exists, and
that a reader reads as its record.*  It lives in the library of the tree whose
rule ranges over it, which is R4's own standard for where a property belongs.

WHAT THIS PROBE ESTABLISHES.  The old population, the new one, that nothing was
lost, that the new one reaches an artifact no path in that tree could have, and
what the widening FOUND -- which is the number I predicted wrong.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libbf79 as B

BAD = 0
R6 = "%s/r6_self.py" % B.SUBJECT
TAG = B.M.MY_TAG

B.bar("P2  THE POPULATION OF THE STRICTEST SELF-RULE")

# ---------------------------------------------------------------------------
B.hdr("P2a  THE OLD POPULATION AND THE NEW ONE, BOTH DERIVED")

old = B.M.outs(B.SUBJECT)
new = B.published_by(TAG)
commits = B.provenance_commits(TAG)
print("  The old rule's population, re-derived by calling the function it")
print("  called; the new one by calling the property.  Both here, so the")
print("  movement is a measured pair of numbers and not a claim about an edit.")
print()
print("      the tag the property searches for                  %s" % TAG)
print("      COMMITS carrying that tag, as log ITEMS           %3d" % len(commits))
print("      ARTIFACTS in the OLD population (one dir's out_*) %3d" % len(old))
print("      ARTIFACTS in the NEW population (the property)    %3d" % len(new))
print("      ...of those, TRANSCRIPTS                          %3d"
      % len([p for p in new if os.path.basename(p).startswith("out_")]))
print("      ...of those, PROSE FILES                          %3d"
      % len([p for p in new if p.endswith(".md")]))
print("      ...ARTIFACTS outside the subject's own directory   %3d"
      % len([p for p in new if not p.startswith(B.SUBJECT + "/")]))
print()
print("  THE COMMITS THE PROPERTY READ, so the query is visible rather than")
print("  trusted -- a population whose derivation is invisible is a hand-list")
print("  with a plumbing accent:")
print()
for sha, subj in commits:
    print("      %s  %s" % (sha, subj[:64]))
print()
print("  AND THE MEMBERS, each marked with whether the old rule had it:")
print()
for p in new:
    print("      %-56s %s" % (p, "old" if p in old else "*** NEW ***"))

# ---------------------------------------------------------------------------
B.hdr("P2b  DOES THE WIDENING LOSE ANYTHING?  the direction that matters")

lost = [p for p in old if p not in new]
print("  A widened rule that drops a member it used to have is not a widening.")
print("  R4c asks this of the target property; it is asked of the population")
print("  property here on the same terms.")
print()
print("      ARTIFACTS the old rule had                        %3d" % len(old))
print("      ...ARTIFACTS still in the population              %3d"
      % (len(old) - len(lost)))
print("      ...ARTIFACTS LOST by the widening                 %3d" % len(lost))
for p in lost:
    print("          *** %s" % p)
BAD += len(lost)
print()
print("      the old population is a strict SUBSET of the new    %s"
      % ("yes" if not lost and len(new) > len(old) else "*** NO ***"))
if lost or len(new) <= len(old):
    BAD += 1

# ---------------------------------------------------------------------------
B.hdr("P2c  THE ARTIFACT NO PATH IN THAT TREE COULD HAVE REACHED")

outside = [p for p in new if not p.startswith(B.SUBJECT + "/")]
print("  The test of a property is whether it reaches something a path could")
print("  not.  mg-05eb's OPEN 2 was ONE FIGURE WRONG IN FOUR ARTIFACTS and")
print("  THREE of them were prose; mg-dee4's F3 was a self-facing population")
print("  that excluded every `.md`.  So the member that matters is the one")
print("  outside the directory:")
print()
for p in outside:
    d = os.path.dirname(p)
    print("      %-56s in `%s`" % (p, d))
print()
print("      ARTIFACTS the property reaches outside that tree   %3d"
      % len(outside))
if not outside:
    BAD += 1
    print("      *** a property that reaches nothing a path could not is a")
    print("          path with extra steps ***")

# ---------------------------------------------------------------------------
B.hdr("P2d  WHAT THE WIDENING FOUND -- and the prediction it refutes")

print("  `r6_self.py` is run live and its E1 rows are read out of its output.")
print("  Both runs are reported: this is the FIRST run in which the widened")
print("  population exists, and the final committed one is `out_r6_self.txt`.")
print()
code, text = B.run_probe(R6)
print("      exit STATUS of the repaired self-check, 1 RUN      %3s"
      % ("-" if code is None else code))
rowrx = {
    "artifacts of mine it published":
        r"artifacts of mine it published\s+(\d+)",
    "members of it the property LOST":
        r"members of it the property LOST\s+(\d+)",
    "artifact lines reporting a count over source":
        r"artifact lines reporting a count over source\s+(\d+)",
    "quoting another artifact's line, excluded":
        r"quoting another artifact's line, excluded\s+(\d+)",
    "with NO GRAIN WORD in the window":
        r"with no grain word in the window\s+(\d+)",
}
got = {}
for label, rx in rowrx.items():
    m = re.search(rx, text)
    got[label] = int(m.group(1)) if m else None
    print("      %-50s %3s" % (label, "-" if m is None else m.group(1)))
    if m is None:
        BAD += 1
missing = got["with NO GRAIN WORD in the window"]
print()
print("      E1 population members (ARTIFACTS)                 %3d" % len(new))
print("      the OLD population, for the same rule (ARTIFACTS) %3d" % len(old))
print()
print("  THE PREDICTIONS THIS REFUTES, kept as written.  `PREDICTIONS` P2d")
print("  says widening will find AT LEAST ONE count row in mg-70c7's own")
print("  reader-facing prose with no grain word in the window, and puts the")
print("  number between 1 and 12.  Measured: %s.  P2e says `r6_self.py` will"
      % ("%d" % missing if missing is not None else "unreadable"))
print("  exit 1 on the FIRST run after the widening and 0 on the final one.")
print("  Measured: it exits %s.  BOTH MISS."
      % ("-" if code is None else code))
print()
print("  AND THE ONE TIME IT DID EXIT 1, THE CAUSE WAS NOT THE WIDENING.  The")
print("  full sequence, because the middle of it is a finding: the first run")
print("  after the widening exited 0.  It then exited 1 for one run, on")
print("  `UNBACKED README.md 3738079` -- because the repaired README named a")
print("  REVISION and E2's `figures()` read the seven-digit revision as a")
print("  MEASUREMENT no transcript backs.  It exits 0 again now, because the")
print("  prose no longer names an unstable revision.  Neither of those runs is")
print("  the `1` P2e predicted; P2e predicted the widened rule would find")
print("  something, and what it found was my own citation format.")
print()
print("  AND THE MISS IS NOT NEW -- IT IS MY AUDITOR'S, REPEATED.  mg-56dc's")
print("  own T2a is scored *MISS -- 0 flagged*, with the reason kept: *I")
print("  reasoned that prose unchecked by a rule would fail it.  It does not.*")
print("  I read that sentence, filed it under `what was already run before this")
print("  file was written`, and then predicted the same number for the same")
print("  wrong reason.  The prose passes because the prose was written by")
print("  people who name their grains, not because a rule made them.  A rule")
print("  that is not run has not passed -- that is a statement about REACH --")
print("  and predicting a DEFECT COUNT from it is a different claim, which is")
print("  the one that keeps being wrong.")
print()
print("  WHAT THE WIDENING DID ESTABLISH, then, stated plainly so the zero is")
print("  not read as nothing: the rule now REACHES %d artifacts instead of %d,"
      % (len(new), len(old)))
print("  including %d outside its own directory, and the reach is what O2 asked"
      % len(outside))
print("  for.  `Widen it to the artifacts the rule is about, and state what it")
print("  covers` -- the coverage is stated above and it is %d of %d."
      % (len(new), len(new)))
print()
print("  AND THE COVERAGE SENTENCE IS NOT A TAUTOLOGY, which mg-fcb2 recorded")
print("  as its own headline defect -- a coverage line whose 86/86 was true of")
print("  the code path and false as a sentence.  `%d of %d` here is the" % (len(new), len(new)))
print("  population against ITSELF and would be 100%% however wrong the rule")
print("  was, so it is NOT offered as evidence: the evidence is the OLD count")
print("  beside it (%d), the LOST count (%d), and the member list above."
      % (len(old), len(lost)))

# ---------------------------------------------------------------------------
B.hdr("P2e  IS THE POPULATION STILL DEFINED BY A PATH?  asked of the source")

src = B.read(R6, None)
lib = B.read("%s/lib70c7.py" % B.SUBJECT, None)
checks = [
    ("r6_self.py's E1 loop no longer iterates `M.outs(M.TREE)`",
     len(re.findall(r"for out in MY_OUTS", src)), 0, "=="),
    ("...it iterates the property's result",
     len(re.findall(r"for out in E1_POP", src)), 1, "=="),
    ("r6_self.py calls the property",
     len(re.findall(r"M\.published_by\(", src)), 1, ">="),
    ("lib70c7.py DEFINES the property",
     len(re.findall(r"^def published_by\(", lib, re.M)), 1, "=="),
    ("...and states it in its own words at the rule",
     len(re.findall(r"THE PROPERTY, STATED WHERE THE CHECK LIVES", lib)),
     1, ">="),
    ("...and names its LIMIT at the rule",
     len(re.findall(r"THE LIMIT, stated at the rule", lib)), 1, ">="),
    ("r6_self.py PRINTS the tag and the commit count",
     len(re.findall(r"the tag searched|commits whose subject carries it", src)),
     2, ">="),
]
for label, n, want, op in checks:
    ok = (n == want) if op == "==" else (n >= want)
    if not ok:
        BAD += 1
    print("      %-54s %2d   %s"
          % (label, n, "OK" if ok else "*** want %s%d ***" % (op, want)))
print()
print("  AND THE PROPERTY IS NOT PATH-FREE BY MAGIC.  `published_by` names no")
print("  directory, but it does select on the FORM of a basename -- `out_*.txt`")
print("  or `*.md`.  That is this arc's transcript-and-prose convention, and it")
print("  is the same disposition `r6_self.py` already gives for `outs()`: a")
print("  name appears; it is not a population filter over CONTENT.  The")
print("  distinction is that the set of DIRECTORIES is not written down")
print("  anywhere, which is what made the old rule a path.")

print()
B.bar("P2 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts an artifact the widening LOST, a new")
print("population that is not a strict superset, a property that reaches")
print("nothing outside its own tree, an unreadable E1 row in the repaired")
print("output, an E1 loop still iterating the directory, and a property that")
print("is not defined or not stated or not limit-stated at the rule.  It ranges")
print("over the %d ARTIFACTS the property returns and the %d the old rule had."
      % (len(new), len(old)))
print("It does NOT establish that the rule is SUFFICIENT -- `r6_self.py` says")
print("in its own transcript that a count labelled `executions` that is really")
print("sites would pass it, and P1f is the measurement of that.")
print()
print(B.finding("P2a", "E1, the strictest rule mg-70c7 applies to anything, "
                       "ranged over ONE DIRECTORY'S %d transcripts and now "
                       "ranges over %d ARTIFACTS derived by provenance from the "
                       "whole repository -- %d of them prose and %d outside "
                       "that directory, 0 members lost"
                       % (len(old), len(new),
                          len([p for p in new if p.endswith('.md')]),
                          len(outside))))
print(B.finding("P2b", "the widening found %s count row(s) with no grain word "
                       "against my prediction of 1-12, and the repaired "
                       "self-check exits %s against my predicted first-run 1 -- "
                       "BOTH MISSES, and they are mg-56dc's own T2a miss "
                       "repeated by the ticket repairing it: REACH IS NOT A "
                       "DEFECT COUNT, and the one run that did exit 1 did so "
                       "because a seven-digit git REVISION in my own repaired "
                       "prose was read as a FIGURE, not because the widening "
                       "found anything"
                       % (missing, "-" if code is None else code)))
sys.exit(1 if BAD else 0)
