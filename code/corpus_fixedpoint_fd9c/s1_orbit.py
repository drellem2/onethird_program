"""mg-fd9c / S1 -- THE OSCILLATION IS NOT AN OSCILLATION.

THE TICKET'S ITEM 1 IS `REPRODUCE THE OSCILLATION INDEPENDENTLY ... run enough
to characterise the period, or establish that it does not have one.`  This
probe establishes something stronger and less comfortable: **there is no
period, because there is no orbit.**  The census map settles at run 2 and stays
settled, and the two values D7 reports are the same settled corpus read under
two write disciplines, differing by exactly the observer's own transcript.

  S1a  THE ARITHMETIC, at HEAD, from the corpus on this disk.
  S1b  THE OBSERVER'S WEIGHT FOR EVERY TREE IN THE ARC -- the generalisation,
       and the number nobody has computed.
  S1c  THE ORBIT, iterated in memory over the real corpus, with three
       DESIGNED-PERIOD controls so that `period 1` is a measurement and not a
       thing my detector always says.
  S1d  what S1 cannot do from inside a worktree, and which probe does it.

Exit code = number of S1 checks that fail.
"""

import sys

import libfd9c as U

BAD = 0

U.bar("mg-fd9c / S1 -- THE OSCILLATION IS NOT AN OSCILLATION")
print("HEAD: %s   subject: the arc-wide census over `code/*/out_*.txt`"
      % U.head())
print("Reported by c9160 as defect D7: `the row count OSCILLATES between 1984")
print("and 1966 and does NOT converge`, over seven consecutive runs.")

# ---------------------------------------------------------------------------
U.hdr("S1a  THE TWO VALUES ARE ONE CORPUS UNDER TWO WRITE REGIMES")

PROBE = "code/grain_arity_9160/out_s1_reproduce.txt"
paths = U.B.all_transcripts()
pres, absent, delta = U.own_weight(PROBE, paths)

print("  A probe that censuses `code/*/out_*.txt` is inside its own")
print("  population.  What its census reads therefore depends on how its own")
print("  transcript is being written AT THE MOMENT IT RUNS:")
print()
print("      a plain `>`      truncates the file before python starts, so the")
print("                       probe reads its own transcript as EMPTY;")
print("      `.new` + `mv`    leaves the previous run's transcript in place,")
print("                       so the probe reads its own PREVIOUS output.")
print()
print("  mg-bf79 introduced the second; mg-9160's `run_all.sh` adopts it and")
print("  says why, in its own comment, naming this as `the arc's defect #7`.")
print("  Both disciplines are in the arc RIGHT NOW, and a figure produced")
print("  under one is not the figure produced under the other.")
print()
U.pop("the corpus `%s` globs, at HEAD, read twice" % PROBE)
print("      %-56s %s" % ("regime", U.HEADFMT))
print("      %-56s %s" % ("`.new` + `mv`  -- its own transcript PRESENT",
                          U.fmt(pres)))
print("      %-56s %s" % ("a plain `>`    -- its own transcript EMPTY",
                          U.fmt(absent)))
print("      %-56s %s" % ("the difference: THE OBSERVER'S OWN WEIGHT",
                          "%6d %6d %6d %6d %6d"
                          % tuple(delta[f] for f in U.FIELDS)))
print()
own = delta["rows"]
print("      one unit of that row count is one line `lib56dc.count_rows`")
print("      returns from `%s`" % PROBE)
print()
c1 = delta["files"] == 0
print("      THE TRUNCATION FINGERPRINT: `files` does not move            %s"
      % ("yes -- `>` truncates, it does not unlink" if c1 else "*** NO"))
BAD += not c1
print()
print("  AND NOW D7's TWO NUMBERS.  c9160 ran at a corpus this branch has")
print("  since grown past, so the pair below is ITS pair and not mine; what")
print("  transfers is the RULE, and the rule is checkable on its own numbers:")
print()
print("      c9160's `.new`+`mv` reading                             1984")
print("      c9160's plain `>` reading                               1966")
print("      the difference                                            18")
print("      count_rows of its own `out_s1_reproduce.txt` AT HEAD      %d" % own)
print()
same = own == 18
print("      the difference IS the observer's weight                 %s"
      % ("yes -- 18 = 18" if same else
         "*** the weight has moved to %d since; see S1d" % own))
if not same:
    print("      (that is not a failure of the rule.  The probe's own row")
    print("       count is itself a measurement and it moves with the probe.")
    print("       X1b runs both regimes AT c9160's OWN REF and gets 1984 and")
    print("       1966 out of one corpus.)")
print()
print("  WHAT THIS COSTS D7.  `oscillates ... and does NOT converge` is a")
print("  claim about a SEQUENCE.  Two readings of one state are not a")
print("  sequence.  D7's observation is real and its mechanism is not the one")
print("  it names: the corpus including its own auditors is TRUE (that is D6)")
print("  and is NOT sufficient for non-convergence -- see S1c.")

# ---------------------------------------------------------------------------
U.hdr("S1b  THE OBSERVER'S WEIGHT, FOR EVERY TREE IN THE ARC")

print("  D7 is a special case of a quantity nobody in this arc has computed:")
print("  for a census over `code/*/out_*.txt`, HOW MUCH OF THE ANSWER IS THE")
print("  CENSOR?  Below, per tree: the rows its own transcripts contribute,")
print("  which is the width of the interval between its two regimes.")
print()
stats = U.file_stats(paths)
trees = sorted({p.split("/")[1] for p in paths})
rows_tot = pres["rows"]
weights = []
for t in trees:
    pre = "code/" + t + "/"
    d = U.weight_of(stats, lambda p, _pre=pre: p.startswith(_pre))
    if d["rows"]:
        weights.append((d["rows"], t, d))
weights.sort(reverse=True)
U.pop("every `code/<tree>/` holding at least one count row, at HEAD")
print("      %-42s %6s %6s   %s" % ("tree", "rows", "share", "of which "
                                    "e-rows/e-ints/words"))
for r, t, d in weights[:14]:
    print("      %-42s %6d %5.1f%%   %d / %d / %d"
          % (t, r, 100.0 * r / rows_tot, d["erows"], d["eints"], d["words"]))
print("      %-42s %6d %5.1f%%" % ("... %d further trees" % max(0, len(weights) - 14),
                                   sum(r for r, _t, _d in weights[14:]),
                                   100.0 * sum(r for r, _t, _d in weights[14:])
                                   / rows_tot))
print("      %-42s %6d %5.1f%%" % ("TOTAL", rows_tot, 100.0))
print("      ^ one unit of every number in that column is one printed line")
print()
mx, mt, _md = weights[0]
print("      the heaviest single observer in the arc: `%s` at %d rows, %.1f%%"
      % (mt, mx, 100.0 * mx / rows_tot))
print()
print("  READ THAT AS AN ERROR BAR AND IT IS THE ANSWER TO ITEM 4.  A tree")
print("  that censuses this corpus while writing into it publishes a figure")
print("  whose value depends on a write discipline, and the width of that")
print("  dependence is its own row on this table.  S4 turns that into a")
print("  published form.")

# ---------------------------------------------------------------------------
U.hdr("S1c  THE ORBIT, ITERATED IN MEMORY, WITH DESIGNED-PERIOD CONTROLS")

print("  `T -> render(census(corpus + T))`, from the empty transcript, over")
print("  the REAL corpus on this disk.  In memory, because a probe that")
print("  iterates by writing cannot be run twice without changing its own")
print("  answer -- which is the disease.")
print()
base = U.census(U.read_all(paths))
U.pop("the %d transcripts on disk at HEAD, plus one virtual transcript"
      % base["files"])
print()
print("      %-52s %8s %8s" % ("transcript shape", "start", "period"))
o, st, per = U.orbit(U.r_fixed, k=16, paths=paths)
print("      %-52s %8s %8s"
      % ("r_fixed -- the shape EVERY arc probe has", st, per))
okf = per == 1
BAD += not okf
for P in (2, 3, 5):
    _o, s2, p2 = U.orbit(U.make_cycler(base["rows"], P), k=60, paths=paths)
    print("      %-52s %8s %8s"
          % ("make_cycler(P=%d) -- CONTROL, shape follows value" % P, s2, p2))
    BAD += p2 != P
print()
print("      period 1 is a FIXED POINT.  The three controls are transcript")
print("      shapes whose ROW COUNT depends on the value they report; each is")
print("      built to a named period and the detector returns that period, so")
print("      `period 1` above is a measurement and not a default.")
print()
print("      the fixed point r_fixed lands on:   %s" % U.fmt(o[-1][0]))
print("      the corpus without any observer:    %s" % U.fmt(base))
print()
print("  THE SUFFICIENT CONDITION, and it is the whole explanation:")
print()
print("      if a probe prints a number of count rows that does not depend on")
print("      the VALUES it prints, then one application of the map fixes the")
print("      corpus row count, and every later application is the identity.")
print()
print("  Every probe in `mg-9160` and `mg-03d1` has that shape.  So does every")
print("  probe here.  SELF-INCLUSION ALONE CONVERGES; what does not converge")
print("  is a corpus that GROWS, and that is S2.")

# ---------------------------------------------------------------------------
U.hdr("S1d  WHAT THIS PROBE CANNOT DO, AND WHICH ONE DOES IT")

print("  Everything above is computed from the corpus ON THIS DISK, without")
print("  running anything.  That is deliberate -- my ticket forbids")
print("  regenerating another tree's transcripts, and a probe in `run_all.sh`")
print("  that ran mg-03d1's suite three times would take a quarter of an hour")
print("  and rewrite six files it does not own.")
print()
print("  So the two arms that need actual runs live in `x1_orbit.py`, which")
print("  clones this repository into a directory you name and refuses to")
print("  start if that directory is inside it:")
print()
print("      X1a  mg-9160's suite iterated from c9160's own corpus state")
print("      X1b  the two regimes at c9160's own ref -- 1984 and 1966 out of")
print("           ONE corpus")
print("      X1c  mg-03d1's suite iterated at HEAD")
print()
print("  Its transcript is committed as `out_x1_orbit.txt`.  IT IS NOT")
print("  REGENERATED BY `run_all.sh`, so it is a dated measurement and it will")
print("  go stale exactly the way every other figure in this arc does.  That")
print("  is stated here rather than discovered later, and S4 gives it a class.")

print()
print("S1 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
