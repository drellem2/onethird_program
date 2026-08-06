"""F2 -- HOW MUCH OF THE ARC'S PUBLISHED ARITHMETIC MOVES?

`mg-5035` step 2: *measure the contamination.  A fix with no measurement leaves
every prior count in the same unknown state.*

THE TWO SIDES ARE NOT THE SAME DEFECT AND ARE COUNTED APART.

  THE CLAIM SIDE.  `figures(line)` over a prose line decides what must be
  backed.  A revision counted here becomes A FIGURE NO TRANSCRIPT BACKS -- a
  false accusation.  This is what bit mg-bf79.

  THE BACKING SIDE.  `transcript_figures(paths)` builds the set of numbers a
  claim may be backed BY.  A revision counted here can make a genuinely
  unbacked figure look BACKED -- a false acquittal, and the more dangerous
  direction, because the check exists to catch exactly that.

Both are re-derived here.  NEITHER IS RE-RUN: regenerating another tree's
committed transcripts to agree with a rule I changed would destroy the evidence
this measurement is about, and PREDICTIONS says so in advance.  Every number
below is re-derived by me at HEAD and labelled as mine.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5035 as B                                              # noqa: E402

BAD = 0

B.bar("F2  THE CONTAMINATION, WITH ITS DENOMINATOR")

# ---------------------------------------------------------------------------
B.hdr("F2a  THE CLAIM SIDE -- every tracked file, before and after")

files = B.corpus()                       # SUBJECT: the arc, this tree excluded
allfiles = B.corpus(include_self=True)   # and the whole repository beside it
per_file = {}
for p in files:
    d = 0
    for line in B.read(p).splitlines():
        d += len(B.dropped(line))
    if d:
        per_file[p] = d
tot_drop = sum(per_file.values())
print("  population: the %d tracked .md/.txt/.py files at HEAD EXCLUDING this"
      % len(files))
print("  tree -- the SUBJECT is the arc as it stood before this repair.  The")
print("  whole-repository figure over %d files is printed beneath, and the gap"
      % len(allfiles))
print("  between them is this instrument measuring itself (see `lib5035.corpus`).")
B.plain("...FILES with at least one number that stops being a figure",
        len(per_file))
print("      ^ one unit of that number is one file")
B.plain("...NUMBERS that stop being figures, counted with multiplicity",
        tot_drop)
print("      ^ one unit of that number is one number on one line")
print()
print("  DENOMINATOR, so the number above means something.  Over the same %d"
      % len(files))
print("  files, counted the same way:")
tot_fig = 0
for p in files:
    for line in B.read(p).splitlines():
        tot_fig += len(B.A.figures(line, small=2))
B.plain("...NUMBERS the PRE-REPAIR rule read as figures", tot_fig)
print("      ^ one unit of that number is one number on one line")
print("      so the repair changes %s of them -- %.4f%%"
      % (tot_drop, 100.0 * tot_drop / max(1, tot_fig)))
print()
self_drop = 0
for p in [q for q in allfiles if q.startswith(B.SELF)]:
    for line in B.read(p).splitlines():
        self_drop += len(B.dropped(line))
B.plain("...NUMBERS that stop being figures INSIDE THIS TREE'S OWN FILES",
        self_drop)
print("      ^ one unit of that number is one number on one line")
print("      The instrument prints declared revisions AS EVIDENCE, so it")
print("      contaminates its own census.  Excluded from the headline and")
print("      counted here rather than silently dropped.")
print()
print("  EVERY AFFECTED FILE, listed rather than summarised:")
for p in sorted(per_file, key=lambda k: (-per_file[k], k)):
    print("      %-66s %3d" % (p[:66], per_file[p]))

# ---------------------------------------------------------------------------
B.hdr("F2b  THE BACKING SIDE -- was any figure BACKED ONLY BY A REVISION?")

print("  This is the dangerous direction.  `transcript_figures` is the set of")
print("  numbers a claim may be backed by; a revision in it can acquit an")
print("  unbacked figure.  Re-derived over mg-70c7's own population.")
print()
tpaths = B.transcripts()
before_set, after_set = set(), set()
for p in tpaths:
    for line in B.read(p).splitlines():
        before_set.update(B.A.figures(line, small=2))
        after_set.update(B.L.figures(line))
print("  population: the %d committed `out_*.txt` under `code/`" % len(tpaths))
B.plain("...DISTINCT FIGURES in the backing corpus, PRE-repair", len(before_set))
print("      ^ one unit of that number is one distinct integer")
B.plain("...DISTINCT FIGURES in the backing corpus, POST-repair", len(after_set))
print("      ^ one unit of that number is one distinct integer")
lost = before_set - after_set
B.plain("...DISTINCT INTEGERS that leave the backing corpus", len(lost))
print("      ^ one unit of that number is one distinct integer")
print()
print("  THE INTEGERS THEMSELVES, because a count without them is unchaseable:")
for v in sorted(lost):
    print("      %-16d resolves as a git object: %s"
          % (v, "yes" if B.resolves(str(v)) else "no"))
print()
print("  AND THE VERDICT THAT DEPENDS ON IT.  A claim was WRONGLY ACQUITTED if")
print("  it names a figure that was in the backing corpus ONLY because a")
print("  revision put it there.  Those are exactly the %d integers above, and"
      % len(lost))
print("  the question is whether any prose line in the arc CLAIMS one:")
claimers = []
for p in B.corpus():
    if os.path.basename(p).startswith("out_"):
        continue
    for i, line in enumerate(B.read(p).splitlines(), 1):
        for v in B.L.figures(line):
            if v in lost:
                claimers.append((p, i, v, line))
print()
print("  population: every tracked non-transcript file at HEAD")
B.plain("...CLAIM LINES naming an integer that leaves the backing corpus",
        len(claimers))
print("      ^ one unit of that number is one line")
for p, i, v, line in claimers:
    print("      %-16d %s:%d" % (v, p, i))
    print("          %s" % line.strip()[:88])
if not claimers:
    print("      NONE.  No claim in the arc was acquitted by a revision.  The")
    print("      false-acquittal direction is real, is reachable, and its")
    print("      realised count at HEAD is 0.")
else:
    BAD += len(claimers)

# ---------------------------------------------------------------------------
B.hdr("F2c  `docs/` -- the human-facing prose (PREDICTIONS/P3c)")

docs = [p for p in per_file if p.startswith("docs/")]
print("  population: the %d tracked files under `docs/`"
      % len([p for p in files if p.startswith("docs/")]))
B.plain("...`docs/` FILES with a number that stops being a figure", len(docs))
print("      ^ one unit of that number is one file")
for p in sorted(docs):
    print("      %-66s %3d" % (p[:66], per_file[p]))
    for i, line in enumerate(B.read(p).splitlines(), 1):
        if B.dropped(line):
            print("          %s:%d  %s" % (os.path.basename(p), i,
                                           line.strip()[:74]))
print()
print("  WHAT THIS DOES AND DOES NOT SAY.  `figures()` never RAN over `docs/`")
print("  -- no probe in the arc censuses it.  So a `docs/` row here is not a")
print("  published count that was wrong; it is a count that WOULD have been")
print("  wrong had anybody censused the prose the humans read.  That is a")
print("  smaller claim and it is the one the evidence supports.")

# ---------------------------------------------------------------------------
B.hdr("F2d  THE PUBLISHED COUNTS THEMSELVES, re-derived before and after")

print("  mg-bf79's `p4_figures.py` published three counts over the transcript")
print("  corpus.  ITS NUMBERS, over ITS population, at ITS commit: 1284")
print("  distinct figures, 31 of magnitude >= 1e6, 6 resolving.  I did not")
print("  re-run it -- I RE-DERIVE the same three at HEAD, both ways, and the")
print("  populations differ (the arc has grown), so the pre-repair column is")
print("  NOT expected to reproduce 1284 and is not evidence of anything if it")
print("  does not.  The column that carries the ticket's answer is the DELTA.")
print()
for name, s in (("PRE-repair ", before_set), ("POST-repair", after_set)):
    big = sorted(v for v in s if v >= 10 ** 6)
    res = [v for v in big if B.resolves(str(v))]
    print("      %s   distinct figures %5d   >= 1e6 %4d   resolving %3d"
          % (name, len(s), len(big), len(res)))
print()
pre_res = [v for v in before_set if v >= 10 ** 6 and B.resolves(str(v))]
post_res = [v for v in after_set if v >= 10 ** 6 and B.resolves(str(v))]
print("  population: the committed transcript corpus at HEAD, %d files"
      % len(tpaths))
B.plain("...RESOLVING large integers the repair removes from it",
        len(pre_res) - len(post_res))
print("      ^ one unit of that number is one distinct integer")
print()
print("  THE SURVIVORS, NAMED -- a resolving integer still in the backing")
print("  corpus is a revision this rule did not reach, and F1d says why:")
for v in sorted(post_res):
    print("      %-16d still a figure" % v)

print()
B.bar("F2 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts one thing only: a claim line in the")
print("arc that names an integer which was in the backing corpus solely")
print("because a revision put it there -- a FALSE ACQUITTAL.  It does not")
print("count the false accusations of F2a, which are the reported defect and")
print("are a measurement here rather than a fault of this tree.")
print()
print(B.finding("F2a", "the repair moves %d of %d numbers read as figures "
                       "across %d of %d tracked files (%.4f%%); the backing "
                       "corpus over %d committed transcripts loses %d of %d "
                       "distinct integers, and %d claim line(s) in the arc "
                       "were acquitted by one"
                % (tot_drop, tot_fig, len(per_file), len(files),
                   100.0 * tot_drop / max(1, tot_fig), len(tpaths),
                   len(lost), len(before_set), len(claimers))))
sys.exit(min(BAD, 120))
