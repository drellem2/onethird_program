"""R2 -- THE FIGURE WITH NO ANCHOR, AND THE CENSUS THAT FINDS ITS KIND.

THE FINDING (mg-dee4's F2).  The published document stated *"anchored to the
pin the byte-comparison sees 154 changed files"*.  `s4_unpin.py`'s own
committed transcript printed 166 for that measurement; `1ee1f1b` against the
pin is 257 and `1ee1f1b^` is 240, and on a worktree it grows with the arc.
**No anchor reproduces 154.**  And `c252f96` had applied *"a number that moves
belongs in a transcript"* to the 2x2 totals three paragraphs above it.

A RULE STATED IN PROSE IS APPLIED WHERE THE AUTHOR WAS LOOKING.  So the repair
is not only to move that one figure -- it is to make the rule a CHECK:

  R2a  the four anchors, computed, so `no anchor reproduces it` is measured;
  R2b  a FIGURE CENSUS over mg-7522's reader-facing artifacts: every number,
       against every figure its own transcripts print;
  R2c  the same census over THIS tree's artifacts, because a census that stops
       at someone else's document has a population defined by an author.

THE BACKING TEST IS WEAK IN ONE DIRECTION AND SAYS SO: it asks whether a figure
appears in a transcript at all, not whether it appears as the answer to the same
question.  Every row prints the figure and the line, so the sense is checkable
by eye; a weak test that runs beats a strong one that is a promise.
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib70c7 as M

BAD = 0

M.bar("R2  A NUMBER THAT MOVES BELONGS IN A TRANSCRIPT -- AS A CHECK")

# ---------------------------------------------------------------------------
M.hdr("R2a  THE FOUR ANCHORS, COMPUTED")


def changed(ref, at=None):
    """`git diff --name-only <ref>` at a revision, or against the worktree."""
    args = ["diff", "--name-only", ref] + ([at] if at else [])
    return len([f for f in M.git(*args).split() if f])


print("  The measurement is `git diff --name-only bee07a1 --`, which is what")
print("  `s4_unpin.changed_since(PINNED)` runs.  Four anchors, all four read")
print("  here rather than quoted:")
print()
rows = [("the worktree, right now", changed(M.PINNED),
         "MOVES -- grows with the arc"),
        ("%s, the repair" % M.REPAIR_REV, changed(M.PINNED, M.REPAIR_REV),
         "fixed"),
        ("%s^, the commit before" % M.REPAIR_REV,
         changed(M.PINNED, M.REPAIR_REV + "^"), "fixed"),
        ("`main` as it stands", changed(M.PINNED, "main"),
         "MOVES -- grows with the arc")]
for label, n, kind in rows:
    print("      %-34s %5d   %s" % (label, n, kind))
print()
print("      the figure the document stated                154")
print("      mg-7522's own transcript printed              166")
print()
hits = [label for label, n, _k in rows if n == 154]
if hits:
    BAD += 1
    print("  *** an anchor DOES reproduce 154: %s ***" % ", ".join(hits))
else:
    print("  NO ANCHOR REPRODUCES IT, re-derived.  And two of the four move,")
    print("  which is the reason the sentence now points at `out_s4_unpin.txt`")
    print("  rather than carrying a number: the transcript records what the")
    print("  tree was when the probe ran, and prose cannot.")

# ---------------------------------------------------------------------------
M.hdr("R2b  THE FIGURE CENSUS -- mg-7522's ARTIFACTS AGAINST ITS TRANSCRIPTS")

# THE CORPUS IS THE TRANSCRIPTS OF THE TREES THE ARTIFACT IS THE RECORD OF.
# `OneThird-RunnerExit-PopulationRepair.md` is now the record of two repairs --
# mg-7522's and this one -- and it cites both trees by path, so both trees'
# transcripts back it.  Widening the corpus to the whole arc would let any
# figure anywhere back any claim, which is why it is these two and not `all`.
SUB_OUTS = M.outs(M.SUBJECT) + M.outs(M.TREE)
CORPUS = M.transcript_numbers(SUB_OUTS)
SUB_ART = ["%s/README.md" % M.SUBJECT, "%s/OUTCOMES.md" % M.SUBJECT,
           "%s/PREDICTIONS.md" % M.SUBJECT, M.DOC]

# A figure that is a QUOTATION of the subject's own sentence is backed by the
# SUBJECT's transcript, not by mg-7522's.  Dispositioned by hand, one at a
# time, with the transcript that does carry it -- rather than by widening the
# corpus, which would let any figure anywhere in the arc back any claim.
DISPOSED = {
    (M.DOC, 63): ("a QUOTATION of mg-c2b3's own scoping sentence "
                  "(`63 run_all.sh, 23 containing | tee`), not a claim of this "
                  "document; backed by code/runner_exit_c2b3/out_k1_census.txt"),
}


# A figure on a line that is CORRECTING a past figure is a QUOTATION of it,
# not a claim under it.  Counted as its own class and printed in full, not
# dropped: the alternative is a census that can only be satisfied by DELETING
# the record of what was repaired, which is the defect R1e's first draft had
# and is recorded in OUTCOMES.md.
FIXING = re.compile(r"used to|no longer|mg-dee4|mg-70c7|was a count|"
                    r"is not|did not|reproduces it|corrected|stood here|"
                    r"printed \d+ at the time", re.I)


def census(label, artifacts, corpus, outs, disposed):
    global BAD
    print("  %s" % label)
    print("      transcripts in the corpus                    %3d" % len(outs))
    print("      distinct figures they print                  %3d" % len(corpus))
    print()
    total = un = quoted = 0
    for p in artifacts:
        lines = M.read(p, None).splitlines()
        for i, line in enumerate(lines, 1):
            figs = M.figures(line)
            if not figs:
                continue
            total += len(figs)
            miss = [v for v in figs if v not in corpus]
            if not miss:
                continue
            # ONE LINE IN EITHER DIRECTION, which is F4's own rule turned on
            # this census.  Its first draft asked whether THIS line was
            # correcting, and a correction that wraps -- "no anchor reproduces
            # it" on one line, "257 and 240" on the next -- scored as an
            # assertion of the figures it was correcting.  A line-local test
            # inside the repair of a line-local test.  Recorded in OUTCOMES.md.
            if any(FIXING.search(x) for x in lines[max(0, i - 2):i + 1]):
                quoted += len(miss)
                print("      QUOTED-IN-A-CORRECTION %s:%d  %s"
                      % (os.path.basename(p), i,
                         ", ".join(str(v) for v in miss)))
                print("          %s" % line.strip()[:62])
                continue
            why = disposed.get((p, i)) or disposed.get((p, miss[0]))
            if why:
                print("      DISPOSITIONED %s:%d  %s"
                      % (os.path.basename(p), i,
                         ", ".join(str(v) for v in miss)))
                for k in range(0, len(why), 62):
                    print("          %s" % why[k:k + 62])
                continue
            un += len(miss)
            BAD += 1
            print("      *** UNBACKED %s:%d  %s"
                  % (os.path.basename(p), i, ", ".join(str(v) for v in miss)))
            print("          %s" % line.strip()[:66])
    print()
    print("      figures examined                             %3d" % total)
    print("      quoted inside a correction of themselves     %3d" % quoted)
    print("      UNBACKED and undispositioned                 %3d" % un)
    print()
    return total, un


census("mg-7522's four reader-facing artifacts:", SUB_ART, CORPUS, SUB_OUTS,
       {(M.DOC, 63): DISPOSED[(M.DOC, 63)]})
print("  THE ONE THIS CENSUS EXISTS FOR.  Before mg-70c7 the document's line")
print("  151 read `154 changed files` and no transcript of that tree printed")
print("  154 as a figure.  It reads as a pointer now, and this census is what")
print("  keeps it one.")
print()
print("  A DEFECT IN THIS CENSUS, RECORDED RATHER THAN SMOOTHED AWAY.  Its")
print("  first draft built the corpus by matching every number in the")
print("  transcript text.  Under that rule `154` came back BACKED -- by the")
print("  string `s3_figure.py:154` in `out_s5_self.txt`.  A LINE NUMBER was")
print("  backing a measurement, and the census would have blessed the exact")
print("  figure it was written to catch.  The corpus is now built with the")
print("  same `figures()` rule the claim side uses, line by line.")

# ---------------------------------------------------------------------------
M.hdr("R2c  THE SAME CENSUS, ON THIS TREE -- population defined by a path")

MY_OUTS = M.outs(M.TREE)
MY_ART = ["%s/README.md" % M.TREE, "%s/OUTCOMES.md" % M.TREE,
          "%s/PREDICTIONS.md" % M.TREE, M.MY_DOC]
MY_ART = [p for p in MY_ART
          if subprocess.run(["test", "-f", os.path.join(M.REPO, p)]).returncode
          == 0]
# This tree's own dispositions.  PREDICTIONS.md is a special case and it is
# named rather than excluded by a rule: a prediction is a figure written BEFORE
# the run, so by construction no transcript of this tree can back it -- that is
# what makes it a prediction.  Excluding the file would hide the reasoning; the
# row says it instead.
MY_DISPOSED = {}
for _i in range(1, 4000):
    MY_DISPOSED[("%s/PREDICTIONS.md" % M.TREE, _i)] = (
        "a PREDICTION, written and committed before any probe in this tree "
        "ran.  A figure a transcript could back would not be a prediction; "
        "OUTCOMES.md is where each becomes a claim and is scored.")
print("  THE CENSUS OF MY OWN ARTIFACTS IS IN `R6b`, NOT HERE, and the reason")
print("  is an ordering fact worth stating rather than a preference.")
print("  `run_all.sh` truncates each transcript with `>` before its probe")
print("  runs, so THIS probe cannot read `out_r2_anchor.txt` -- it is writing")
print("  it.  Every figure this section prints, including the four anchors")
print("  above, would come back UNBACKED for that reason and for no other.")
print("  `r6_self.py` runs last, when every other transcript of this run is")
print("  complete, so that is where the census of this tree's own prose")
print("  belongs.  Running it in both places would give this tree two")
print("  answers to one question, and the wrong one would be the loud one.")
print()
print("      my reader-facing artifacts, censused in R6b        %3d"
      % len(MY_ART))
for p in MY_ART:
    print("          %s" % p)
print()
print("      `PREDICTIONS.md` is excluded there and the reason is named: a")
print("      prediction is a figure written BEFORE the run, so a figure a")
print("      transcript could back would not be a prediction.")

print()
M.bar("R2 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts an anchor that reproduces 154, and a")
print("figure in a reader-facing artifact that no transcript of its own tree")
print("prints and that carries no disposition.  It ranges over mg-7522's four")
print("reader-facing artifacts and this tree's own, against the `out_*.txt` of")
print("each.  It does NOT range over mg-c2b3's artifacts -- `s3_figure.py` is")
print("their control -- and it does not check that a backed figure is backed")
print("BY THE RIGHT MEASUREMENT, which is the weak direction and is stated")
print("above rather than implied.")
sys.exit(1 if BAD else 0)
