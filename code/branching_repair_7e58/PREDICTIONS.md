# `mg-7e58` — exit codes and answers predicted BEFORE running

Written before any `k*.py` in this directory was run. **Misses are kept exactly
as written**, and there are three of them.

## What was already known before these predictions were made, and how

A prediction made after the answer is not a prediction, so the starting point is
stated. Before writing this file I had run four exploratory commands by hand,
and their results are **given**, not predicted:

* `python3 g1_provenance.py` on the tree as committed exits `1` with
  `FINDINGS: 1` — the file-grain finding, exactly as `mg-321d`'s `G-1` reports.
* `python3 g4_fleet.py` on the same tree prints `touched by ed9cde4 (mg-13b2)
  : 2 -- c1_branching.py, c2_vertexsets.py` and `touched by mg-58da : 0 --
  none`, exactly as `G-2` reports.
* Running `c1_branching.py` at `286d5030` and at `ef38841` against the same
  target gives byte-identical sections (i)+(ii) — so the measurement did not
  move, which is the fact `G-1` turns on.
* `mg-321d`'s committed totals: `h1` 0, `h2` 3, `h3` 1, `h4` 2, `h5` 0.

Everything below is predicted with those four facts in hand and nothing else.
In particular **no clone had been made, no deletion probe had been fired, and
no reader in `lib7e58.py` had been run against any source.**

```
mg-7e58 EXIT-CODE AND ANSWER PREDICTIONS -- written BEFORE running.

P1  python3 selftest_7e58.py                                  -> 0
      and every reader returns {} on absent and on hostile
      input rather than a partial parse                       -> yes
      ACTUAL 0  HIT

P2  python3 k1_grain.py                                       -> 0
      THE TWO SITES.  The BEFORE state reproduces at ef38841 (g1 exits 1
      with the file-grain finding; g4 attributes c1 to ed9cde4), and after
      the repair g1 exits 0 while STILL going red on a real measurement
      regression.
      the measurement is identical across script revisions
        on both target forms                                  -> yes
      deletion probes on g1, directions predicted             -> 4 of 4
      g4's attribution matching git log, per ticket           -> 2 of 2
      ACTUAL 0  HIT -- but only on the second run, and the first run is the
      most useful thing in this file.  It booked TWO findings, and BOTH were
      defects in what I had written, not in the repair:
        * the "comparing half" probe inserted its line BEFORE c1's section
          (iii) header, which put it inside the MEASURING half.  The probe
          was testing the opposite of what it claimed to test, and g1 was
          right to fire on it.
        * the "dimensions off by one" probe made g1 raise ValueError instead
          of a finding: g1's own internal probe builds a mutated c1 from a
          source string, and in a tree where c1 was ALREADY mutated the
          string was absent.  g1 now books that as a SELF-ERROR and names
          the probe as dropped.
      I predicted 4 of 4 and got 2 of 4 first.  The prediction was right
      about the repair and wrong about my own probes.

P3  python3 k2_selfprov.py                                    -> 0
      THE MAYOR'S QUESTION: the ways this fix could exhibit the defect it
      remedies.  I expect B1 -- "does the repair survive being committed"
      -- to be the one that bites, because it is G-3's exact shape and
      G-3 is what caught mg-58da.
      g1 and g4 identical uncommitted vs committed             -> yes
      frozen records untouched                                 -> 7 of 7
      branches with a measurement or a stated reason            -> 9 of 9
      ACTUAL 0  MISS on which branch bites.  B1 passed first time.  B2 and
      B3 both booked findings, and both were MY CHECKS being wrong:
        * B2 counted mine_c/mine_v/mine_named -- names c1's comparing half
          BINDS FOR ITSELF -- as quantities inherited from the measurement.
        * B3 looked for c1's "Form read:" line in g1's output.  g1 does not
          echo c1's stdout, so it found nothing and declared its own second
          check vacuous.
      Kept as written because the shape is the ticket's own: the instrument
      that asks "are you wrong about yourself" was wrong about itself twice
      before it was right.

P4  python3 k3_setlevel.py                                    -> 0
      THE PROPERTY NOT TO BE LOST, re-derived rather than quoted.
      pairs of sources agreeing at all 24 cells               -> 10 of 10
      members re-run in place                                 -> 5 of 5
      members green                                           -> 4 of 5
        (c3_withdrawal.py red -- mg-d330's second finding, OPEN)
      c0_repro.sh committed outputs identical                 -> 5 of 5
      reader locality probes                                  -> 5 of 5
      ACTUAL 0  MISS on the probes, at the first run.  Two things went
      wrong and both are recorded in the source:
        * b1_cells() returned 0 cells.  I wrote it with mg-321d's own
          header miss on the page and then matched a ROW shape mg-2060
          does not use.  It went to the SELF-ERROR channel and withdrew
          the source, which is what that channel is for -- it was never
          scored as a disagreement -- but the reader was still wrong.
        * the locality probes aimed at beta=3, n=6, whose row beta=2
          carries identically, so 5 of 5 could not be aimed at all.  They
          now aim at beta=1, n=6 -- the only n=6 cell no other parameter
          shares -- scoped to one line.
      10 of 10 and 5 of 5 re-run were right first time.

P5  python3 k4_doccheck.py                                    -> 0
      every figure in the document gated at its own site, and every gate
      made to fire under corruption there.
      gates firing                                            -> all
      ACTUAL 0  HIT

P6  code/branching_audit_58da/run_all.sh after this repair    -> 1
      g1 0, g2 0, g3 0, g4 1.  g4 is predicted to exit 1 and mg-58da
      predicted the same: c3_withdrawal.py is red and mg-d330's e4 gate on
      the exit-code sentence is a presence test.  Neither is closed here.
      ACTUAL 1  HIT

P7  code/branching_audit_321d/h2_grain.py, mg-321d's own finder for
      G-1 and G-2, unmodified, re-run against the repaired tree
                                                              -> 0 findings
      (its committed record is 3)
      ACTUAL 0  HIT

P8  the other four of mg-321d's scripts, unmodified, must NOT move:
      h1 0, h3 1, h4 2, h5 0 -- the same totals as their committed
      records, because this repair closes G-1/G-2/G-3 and touches
      neither M-1 nor M-2 nor c3.
      ACTUAL h1 0, h3 1, h4 2, h5 0  HIT
```

## The shape of the misses

Three of the eight predictions missed, and all three missed the same way: **the
repair was right and my instrument for checking it was wrong.** `k1`'s probe was
aimed at the wrong half of `c1`, `k2`'s two checks read the wrong things, and
`k3`'s probes were aimed at a cell that two parameters share.

That is worth keeping rather than tidying, because it is this ticket's own
subject happening to this ticket's own code — an apparatus built to ask *"are
you wrong about yourself?"* getting itself wrong first. In every case the defect
surfaced because the check was **run** and its direction had been **predicted**,
and in one of the three (`b1_cells`) the damage was contained by control flow
rather than by care: a reader that returns nothing routes to the **SELF-ERROR**
channel and withdraws its source, so a blind reader could not have been scored
as agreement.
