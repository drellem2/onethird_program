# `mg-957f` — exit codes and answers predicted BEFORE running

Written before any `j*.py` in this directory was run, and before any clone was
made. **Misses are kept exactly as written.**

## What was already known when these predictions were made, and how

A prediction made after the answer is not a prediction, so the starting point is
stated. Before writing this file I had read `g1_provenance.py`,
`g4_fleet.py`, `lib58da.py`, `4372fae`'s diff, `code/branching_repair_7e58/`'s
`README.md` and `PREDICTIONS.md`, and the repair's document — and I had run
exactly two commands by hand, whose results are **given**, not predicted:

* `git log 286d5030..HEAD -- code/branching_audit_a218/<member>` for each of the
  five, and `git show --name-only` for each commit it named. Ground truth:
  `673b4c0` touched `c1_branching.py`; `ed9cde4` touched `c2_vertexsets.py`;
  `c3_withdrawal.py`, `c4_seam.py`, `c5_record.py` were touched by nothing in
  the range. Two routes, agreeing.
* `git rev-parse HEAD` → `2d23d880`. The committed `out_g*.txt` were recorded at
  `ef388417`.

No script in this directory had been run, no clone made, no probe fired, and no
reader here run against any source.

```
mg-957f EXIT-CODE AND ANSWER PREDICTIONS -- written BEFORE running.

P1  python3 selftest_957f.py                                   -> 0
      every reader returns {} on absent and on hostile input rather
      than a partial parse                                     -> yes

P2  python3 j1_attribution.py                                  -> 0
      EVERY ATTRIBUTION THE APPARATUS MAKES, RE-DERIVED FROM git log HERE.
      I expect g4 to agree with my derivation at every one, because I have
      already derived the ground truth by hand and it matches the figures
      the repair's document prints.
      attributions agreeing with my own derivation             -> all
      wrong-commit attributions                                -> 0
      unverifiable attributions                                -> 0
      AND THE DERIVATION IS TESTED BY CHANGING THE HISTORY, not by reading
      the code: in a clone I land a NEW commit touching a member the range
      did not touch, and g4's attribution must grow a row for it with no
      other edit.
      clones in which the attribution followed the history     -> 3 of 3

P3  python3 j2_silencing.py                                    -> 1
      HOW g1 WAS RECONCILED.  I predict it was NOT silenced in the c1 case:
      the disposition is stated in three places and the replacement predicate
      goes red on a real measuring-half regression.  I predict 1 finding, on
      a fourth clone nobody has run:

        g1's OLD predicate compared the sha of TWO files, c1_branching.py
        AND kern_a218.py -- the file g1's own section (ii) labels "the
        measuring half".  The replacement runs both c1 revisions through
        L.run_c1(..., script_rev=L.REV_A218), which loads kern_a218.py at
        REV_A218 for BOTH runs.  So a kernel that moved between REV_A218
        and HEAD cannot reach either side of the comparison.

      Predicted, before the clone was made:
        g1 @ HEAD in a clone whose c1 dimensions are off by one -> exit 1
        g1 @ HEAD in a clone whose c1 comparing half moved      -> exit 0
        g1 @ HEAD in a clone whose kern_a218.py is mutated      -> exit 0
        g1 @ ef38841 (PRE-repair) in that same kernel clone     -> exit 1,
          with a finding naming kern_a218.py
        and the mutated kernel really does move c1's measurement -> yes

P4  python3 j3_setlevel.py                                     -> 0
      THE SET-LEVEL PROPERTY, RE-DERIVED ON READERS WRITTEN HERE, all five
      members and not only the ones the repair touched (it touched none).
      pairs of sources agreeing at all 24 cells                -> 10 of 10
      cells compared over those pairs                          -> 240
      mg-a218's members re-run in place                        -> 5 of 5
      members green                                            -> 4 of 5
        (c3_withdrawal.py red -- mg-d330's second finding, OPEN)
      reader locality probes moving their own cell and no other -> 5 of 5

P5  python3 j4_doccheck.py                                     -> 0
      every figure in this audit's document gated at its own site against a
      committed out_j*.txt, each gate deletion-tested with a null probe.

P6  code/branching_audit_58da/run_all.sh re-run at TODAY's HEAD, then
      `git diff --stat` on that directory                      -> NOT EMPTY
      THE THING NO LIST NAMES, and I chose it: mg-321d's G-3 is "the
      documented reproduce command does not reproduce", and the repair
      closes it by regenerating out_*.txt at ef388417.  But g1 and g4 both
      PRINT HEAD[:8] into their own output, so the committed record stops
      reproducing the moment any commit lands -- including the commit that
      landed the repair.  k2's B1 clones the repo, commits the repair and
      compares self-errors, findings, exit codes and finding TEXTS -- which
      are all invariant under a changing HEAD.  Bytes are what G-3 was about
      and bytes are what B1 does not compare.
      files differing after a re-run                           -> 2 of 5
        (out_g1_provenance.txt and out_g4_fleet.txt; g2, g3 and the
         selftest do not print HEAD)
      run_all.sh exit code                                     -> 1

P7  code/branching_audit_321d/h2_grain.py, mg-321d's own finder for G-1 and
      G-2, unmodified, re-run against the repaired tree at TODAY's HEAD
                                                               -> 0 findings
      (its committed record is 3)
```

## Results, filled in AFTER the runs

Nothing above this line was written with an answer in hand. The `ACTUAL` rows
below were added after `./run_all.sh`.

```
P1  selftest_957f.py                          -> 0     ACTUAL 0   HIT
      74 assertions, 0 failed.
      But not on the first run: 2 of the 74 failed and both were mine.
      REV_7E58 was written "4372faee" and the sha is 4372fae9; and the
      kernel-bending probe inserted `pass` as the FIRST STATEMENT of
      vertices(), which is a no-op -- a corruption probe that corrupts
      nothing.  It was caught because assertion (vii) requires the probe to
      REACH c1's OUTPUT, not merely to edit the file.

P2  j1_attribution.py                         -> 0     ACTUAL 0   HIT
      attributions agreeing with my derivation  -> all  ACTUAL 17 of 17
      wrong-commit attributions                 -> 0    ACTUAL 0
      unverifiable attributions                 -> 0    ACTUAL 0
      clones in which the attribution followed  -> 3/3  ACTUAL 3 of 3

P3  j2_silencing.py                           -> 1     ACTUAL 1   HIT
      g1 @ HEAD, c1 dimensions off by one       -> 1    ACTUAL exit 1, 1/3
      g1 @ HEAD, c1 comparing half moved        -> 0    ACTUAL exit 0, 0/0
      g1 @ HEAD, kern_a218.py bent              -> 0    ACTUAL exit 0, 0/0
      g1 @ ef38841 (PRE-repair), same clone     -> 1    ACTUAL exit 1, 0/2,
        with a finding naming kern_a218.py             and it names it
      the bent kernel really moves the measure  -> yes  ACTUAL 24 of 24 cells
      All five rows and the finding, as predicted.  This is F-1.

      MISS INSIDE P3, kept as written.  The per-return deletion test in (v)
      was first written expecting the bent-c1 clone to carry ONE finding, so
      that deleting (v)'s measurement-invariance return would take FINDINGS to
      0.  It carries THREE: g1 builds its probe baseline from c1 @ REV_A218 and
      its probe SOURCES from c1 @ HEAD, and HEAD's c1 is the bent one in that
      clone, so g1's own null probe fires and is scored MISS -- twice.  The
      repair was right and my check was wrong.  Rewritten to require each
      deletion to remove ITS OWN finding and leave the other standing, which is
      the stronger test: 3 -> 2 for the measurement return, 3 -> 1 for the
      probe return.

P4  j3_setlevel.py                            -> 0     ACTUAL 0   HIT
      pairs agreeing at all 24 cells            -> 10/10  ACTUAL 10 of 10
      cells compared over those pairs           -> 240    ACTUAL 240
      members re-run in place                   -> 5/5    ACTUAL 5 of 5
      members green                             -> 4/5    ACTUAL 4 of 5
      reader locality probes                    -> 5/5    ACTUAL 5 of 5

P5  j5_doccheck.py                            -> 0     ACTUAL 0   HIT
      22 gates, 22 of 22 figures present at their own site, 22 of 22 null
      probes green, 22 of 22 corruption probes red.

P5b ./run_all.sh in THIS directory              -> 1     ACTUAL 1   HIT
      selftest 0, j1 0, j2 1, j3 0, j4 1, j5 0; worst 1.  Two scripts
      predicted red and exactly those two are red.

P6  code/branching_audit_58da/run_all.sh at TODAY's HEAD, diffed
      committed outputs that stop reproducing   -> 2 of 5
                                                       ACTUAL 4 of 5   MISS
      run_all.sh exit code                      -> 1    ACTUAL 1        HIT
      THE MISS, KEPT.  I found the HEAD[:8] interpolation in g1 and g4 by
      reading their format strings and did not look in g2 or g3, which print
      the revision in PROSE rather than in a format string:
        out_g2 line 100  "The reproduction is REDONE at ef38841710ed …"
        out_g3 line   6  "… run against out_t1_tl.txt at ef388417."
      The direction was right and the population was undercounted by half --
      which is exactly the failure a "no bare totals, name the population"
      rule exists to expose, committed by the audit applying it.  This is F-2.

P7  code/branching_audit_321d/h2_grain.py, unmodified, at today's HEAD
                                                -> 0 findings  ACTUAL 0   HIT
      (its committed record is 3)
      and the other four unmoved: h1 0, h3 1, h4 2, h5 0
                                                               ACTUAL same, 5/5
```

## The shape of the misses

Two, and both are the shape this lineage keeps producing: **the thing being
audited was right and my instrument for checking it was wrong.** `P3`'s
deletion test misjudged how many of `g1`'s own returns the probe clone would
trip, and `P6` undercounted its own population by reading for a format string
where two of the four sites use prose.

One more never reached a prediction because the self-test caught it first: the
kernel probe inserted `pass` as a function's first statement and changed
nothing. Assertion (vii) requires the probe to reach `c1`'s **output**, so an
inert probe fails there rather than silently certifying that a hole does not
exist.

And one that would have inverted `F-1` if it had survived: the kernel probe was
first written to bend `kern_a218.py` in a clone's **working tree** without
committing it. `g1` reads the kernel with `git_show(HEAD, …)`, never from the
worktree, so both `g1` revisions came back silent — which reads exactly like
*"the old predicate does not fire either, so there is no coverage to have
lost."* It does fire; the probe had to be a **commit**. That is `G-2`'s own
shape: a question about a commit, asked of a working tree.
