"""mg-fd9c / S4 -- THE ERROR BAR, AND A CHECKER THAT ENFORCES IT.

THE TICKET'S ITEM 4: *If a figure is drawn from an oscillating population, the
honest published form of it is not a number.  Whatever this arc publishes next
needs a convention for that, and this ticket is where it gets decided.*

Two corrections to the premise before the convention, both earned in S1 and S2:

  the population does not OSCILLATE, it GROWS  -- S2d: 245 commits, 1 decrease
    in `files` and 2 in `rows`, and both decreases are named there.  So the
    honest form is not `a range because the value wobbles`; it is `a value with
    a DATE, because the value is a timestamp`.

  and there IS a range, of a different kind -- S1a: the same corpus reads two
    ways depending on the write discipline in force while the probe runs, and
    the width of that is the observer's own weight.  THAT is the interval.

So the published form has two parts and they answer two different questions,
and a convention that supplies only one of them is the failure this ticket is
about.

  S4a  THE THREE CLASSES, adopted from `corpus_universe_1d6c` and generalised
  S4b  THE FORM, applied to every figure S2b recomputed
  S4c  THE CHECKER -- because a convention that cannot be checked is a style
       guide (PREDICTIONS.md/E8), and this one is run against the whole arc
       AND against this tree
  S4d  WHAT IT COSTS, and the one thing it does not fix

Exit code = number of S4 checks that fail.
"""

import re
import sys

import libfd9c as U

BAD = 0
A = U.A
B = U.B

U.bar("mg-fd9c / S4 -- THE ERROR BAR, AND A CHECKER THAT ENFORCES IT")
print("HEAD: %s" % U.head())

# ---------------------------------------------------------------------------
U.hdr("S4a  THE THREE CLASSES")

print("  `corpus_universe_1d6c` already named this idea, for one file list,")
print("  and never generalised it.  Its `p2_population.py` runs its census at")
print("  STATE A (a commit), STATE B (another commit) and STATE C (the working")
print("  tree, INCLUDING MY OWN FILES), and its README says in advance:")
print()
print("      *STATE C is not stable.  It includes my own prose, so it moves")
print("       with my next commit.  Any reader re-running this suite after")
print("       this commit should expect STATE A and B to be fixed and STATE C")
print("       to have drifted -- and if it has not, that is worth a question.*")
print()
print("  That is the convention, complete, for one ticket's file list.  Here it")
print("  is as a rule any figure in this arc can be classified by:")
print()
for k in ("FROZEN", "GROWING", "OBSERVED"):
    import textwrap
    lines = textwrap.wrap(U.CLASSES[k], 60)
    print("      %-10s %s" % (k, lines[0]))
    for ln in lines[1:]:
        print("      %-10s %s" % ("", ln))
print()
print("  and the rule that assigns it, which takes two facts and nothing else:")
print()
print("      %-30s %-14s %s" % ("population is a REF?", "censor inside?",
                                "class"))
for a in (True, False):
    for b in (False, True):
        print("      %-30s %-14s %s" % (a, b, U.state_of(a, b)))
print()
print("      ^ a REF-pinned population cannot contain the censor, because the")
print("        censor's transcript is untracked while it runs (S3b/1) -- so")
print("        the top two rows are the same class and that is not an")
print("        oversight.")

# ---------------------------------------------------------------------------
U.hdr("S4b  THE FORM, ON EVERY FIGURE S2b RECOMPUTED")

paths = B.all_transcripts()
stats = U.file_stats(paths)
now = U.census_from(stats)
w03d1 = U.weight_of(stats, lambda p: p.startswith("code/grain_axis_audit_03d1/"))
w9160 = U.weight_of(stats, lambda p: p.startswith("code/grain_arity_9160/"))

print("  A figure computed against the disk glob by a tree that is IN the")
print("  glob is OBSERVED.  Its low end is the census with the censor's own")
print("  transcripts empty -- what a plain `>` gives -- and its high end is")
print("  the census with them present.  Both ends are real readings; neither")
print("  is an error bar in the statistical sense and calling it one would be")
print("  the theatre E8 warns about.  It is a range because the apparatus")
print("  admits two answers.")
print()
U.pop("the arc-wide corpus, read by mg-03d1 and by mg-9160, at HEAD")
print()
print("      %-34s %-12s %s" % ("figure", "class", "honest published form"))
FIG = [
    ("mg-03d1 A1d ARTIFACTS", "files", w03d1),
    ("mg-03d1 A1d count ROWS", "rows", w03d1),
    ("mg-03d1 A1d grain WORDS", "words", w03d1),
    ("mg-03d1 AF1 e-rows", "erows", w03d1),
    ("mg-03d1 AF1 e-ints", "eints", w03d1),
    ("mg-9160 S1b files", "files", w9160),
    ("mg-9160 S1b rows", "rows", w9160),
    ("mg-9160 S1b words", "words", w9160),
]
for name, field, wt in FIG:
    hi = now[field]
    lo = hi - wt[field]
    print("      %-34s %-12s %s"
          % (name, "OBSERVED", U.render_figure(hi, "OBSERVED", low=lo,
                                               ref=U.at())))
print()
recon = U.census(B.read(p, r) for p, r in U.G.parent_corpus())
print("      %-34s %-12s %s"
      % ("the reconstruction, for contrast", "FROZEN",
         U.render_figure(recon["rows"], "FROZEN",
                         ref="%s+%s" % (U.G.PARENT_REV, U.G.PARENT_PUB))))
print()
print("  READ THE `files` ROWS.  Their interval is EMPTY -- low equals high --")
print("  because `>` truncates and does not unlink, so a file count cannot")
print("  tell the two regimes apart (S1a's fingerprint).  A convention that")
print("  printed a range on every figure regardless would be decorating the")
print("  one figure that is not at risk, which is how an error bar stops")
print("  meaning anything.")

# ---------------------------------------------------------------------------
U.hdr("S4c  THE CHECKER")

print("  THE RULE, mechanically: a count row whose LABEL is about the arc-wide")
print("  corpus obeys the convention if the nearest `population:` line ABOVE")
print("  IT IN ITS OWN SECTION carries a ref -- 7 to 40 hex characters after")
print("  an `@`, or the word `at` and a ref.  The search stops at the section")
print("  bar (`====`), because a population declared in a previous section is")
print("  not a population declared for this figure.  Nothing else counts; a")
print("  paragraph three screens away saying which commit this was is not a")
print("  date on a figure.")
print()
print("  THE FIRST FORM OF THIS RULE USED A 12-LINE WINDOW and scored MY OWN")
print("  TREE at 1 of 2 -- not because the second figure was undated but")
print("  because it sat in a 22-row table whose population line was 14 lines")
print("  up.  A convention whose checker fails on long tables would push")
print("  every author towards short ones, so the window is gone and the")
print("  section is the unit.  It costs me the only failing row I had.")
print()
CORPUS_LABEL = re.compile(
    r"\b(ARTIFACTS in that corpus|count ROWS in them|grain WORDS|"
    r"in the corpus|arc-wide|the disk at HEAD)", re.I)
REF = re.compile(r"@[0-9a-f]{7,40}\b|\bat [0-9a-f]{7,40}\b")


def audit(paths):
    tot = dated = 0
    per = {}
    for p in paths:
        try:
            txt = B.read(p)
        except OSError:
            continue
        lines = txt.splitlines()
        for i, label, _n in A.count_rows(txt):
            if not CORPUS_LABEL.search(label):
                continue
            tot += 1
            ok = False
            for j in range(i - 1, -1, -1):
                ln = lines[j]
                if "population:" in ln:
                    ok = bool(REF.search(ln))
                    break
                if ln.startswith("====") or ln.startswith("----"):
                    break
            dated += ok
            k = p.split("/")[1]
            a, b = per.get(k, (0, 0))
            per[k] = (a + 1, b + ok)
    return tot, dated, per


mine = [p for p in paths if p.startswith(U.TREE + "/")]
others = [p for p in paths if not p.startswith(U.TREE + "/")]
tot_o, dated_o, per_o = audit(others)
tot_m, dated_m, per_m = audit(mine)

print("  AND IT OVER-COLLECTS, DELIBERATELY.  This is a rule about the LABEL,")
print("  so a PER-TREE census whose label happens to say `in the corpus` is")
print("  flagged too.  That is the safe direction -- every figure it flags")
print("  really is undated -- but it means the total below is an UPPER BOUND")
print("  on arc-wide figures and must not be used to rescue P4, which named a")
print("  population before seeing this one.  S5a refuses that rescue by name.")
print()
U.pop("every count row in the arc's %d transcripts whose LABEL is about the "
      "arc-wide corpus" % len(others))
print("      ...arc-wide corpus figures found                          %d"
      % tot_o)
print("      ...of them carrying a DATED population line               %d"
      % dated_o)
print("      ^ one unit of each is one printed line")
print()
for k in sorted(per_o):
    print("          %-44s %3d found, %3d dated" % (k, per_o[k][0],
                                                    per_o[k][1]))
print()
U.pop("the same rule turned on THIS TREE's own %d transcripts" % len(mine))
print("      ...arc-wide corpus figures found                          %d"
      % tot_m)
print("      ...of them carrying a DATED population line               %d"
      % dated_m)
print()
if not mine:
    print("      THIS TREE HAS NO TRANSCRIPTS ON DISK YET.  On the run that")
    print("      writes them for the first time they are untracked and this")
    print("      count is 0 -- which is S3b/1 happening to me, in my own")
    print("      self-check, on the first run.  The committed transcript is")
    print("      from a SECOND run and shows the real number.")
else:
    okself = tot_m > 0 and dated_m == tot_m
    print("      this tree obeys its own convention at every figure    %s"
          % ("yes" if okself else "*** NO -- %d of %d undated"
             % (tot_m - dated_m, tot_m)))
    BAD += not okself
print()
U.note("S4c", "THE CONVENTION IS ENFORCEABLE AND THE ARC DOES NOT MEET IT: "
       "%d of %d arc-wide corpus figures in the arc's transcripts carry a "
       "dated population line.  This is a CHECK and not a style note -- it "
       "runs here, it fails there, and it is one function." % (dated_o, tot_o))

# ---------------------------------------------------------------------------
U.hdr("S4d  WHAT IT COSTS, AND THE ONE THING IT DOES NOT FIX")

print("  THE COST, in full:")
print()
print("      a ref on every population line   -- one `git rev-parse`, cached;")
print("                                          this tree's `pop()` has no")
print("                                          form that omits it")
print("      an interval on OBSERVED figures  -- one call to `own_weight`, one")
print("                                          extra census of the same file")
print("                                          list with one tree emptied")
print("      a class on each figure           -- two booleans, S4a's table")
print()
print("  WHAT IT DOES NOT FIX, and this is the honest limit: a dated figure")
print("  is still WRONG TOMORROW.  The convention does not stop the drift; it")
print("  makes the drift READABLE, so that a reader who re-runs a probe and")
print("  gets a different number knows they have measured the arc's growth")
print("  and not found a defect.  S2d's shelf-life column is what that reader")
print("  would otherwise have to rediscover, and c9160 did rediscover it --")
print("  its P7 was scored a MISS for exactly this and the miss was correct.")
print()
print("  AND IT DOES NOT MAKE A GROWING FIGURE COMPARABLE TO ITSELF.  Two")
print("  dated readings of `count ROWS in them` are two facts about two")
print("  corpora.  Subtracting them is a measurement of the arc, not of the")
print("  classifier -- which is the mistake `517 does not reproduce` would")
print("  have been, and is the reason this convention exists.")

print()
print("S4 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
