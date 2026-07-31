# `mg-58da` — exit codes and answers predicted BEFORE running

Written before any `g*.py` in this directory was run.  **Misses are kept
exactly as written.**

## What was already known before these predictions were made, and how

Honesty about the starting point, because a prediction made after the answer
is not a prediction.  Before writing this file I ran three exploratory
commands by hand, and their results are *given*, not predicted:

* `c1_branching.py` re-run out of a `git archive` of `286d503` exits `0` with
  `TOTAL BAD: 0` — the 198-cell reproduction.
* `c1_branching.py` run against the working tree exits `1` with `TOTAL BAD:
  24`, exactly as `mg-d330`'s `out_e4_rerun.txt` already recorded.
* `c1_branching.py` and `kern_a218.py` are byte-identical at `286d503` and at
  `d1dd84d`; `c2_vertexsets.py` is not.

Everything below is predicted with those three facts in hand and nothing else.
In particular **no comparison of the target's new vertex block against
anything had been run**, and no corruption probe had been fired.

```
mg-58da EXIT-CODE AND ANSWER PREDICTIONS -- written BEFORE running.

P1  python3 selftest_58da.py                                  -> 0
P2  python3 g1_provenance.py                                  -> 0
      and the 286d503 re-run is BYTE-IDENTICAL to the committed
      out_c1_branching.txt                                    -> yes
      and c1's read path is exactly ONE external file         -> yes
      and exactly ONE commit touched it since 286d503         -> yes (ed9cde4)
      and c1's own sections (i)+(ii) -- the MEASUREMENT -- are
      byte-identical between the two revisions                -> yes

P3  python3 g2_redo.py                                        -> 0
      QUESTION B, second half.  The 24 vertex cells the target no longer
      states as counts are RECOVERABLE from the set block mg-13b2 put in
      their place, and all 24 recovered counts equal c1's own.
      cells recovered from the HEAD target                    -> 24 of 24
      recovered counts agreeing with c1's measurement         -> 24 of 24
      recovered SETS agreeing with c1's measurement           -> 24 of 24
      instruments agreeing on all 24 cells                    -> 4 of 4
      corruption probes that fire                             -> all

P4  python3 g3_findings.py                                    -> 0
      QUESTION A.  All 24 findings are PARSER ARTIFACTS: 0 CONFIRMED,
      0 UNKNOWN.  The reason is that the datum is present in the target
      in a STRICTLY RICHER form and agrees.
      lines in the HEAD target matching c1's count regex       -> 0
      lines in the 286d503 target matching it                  -> 4
      THE NON-FINDINGS, which is the harder half: every one of the
      corruption probes on the 53 dimension cells and the 121 edge
      cells makes the UNREPAIRED c1 go red, so those 174 comparisons
      are live and their 0 disagreements carry information.
      probes fired -> all fire

P5  python3 g4_fleet.py                                       -> 1
      THE SET-LEVEL PROPERTY.  It does NOT fully hold and I do not
      expect it to: c3_withdrawal.py exits 1 on the repaired tree for
      a reason that is mg-d330's second finding and is not repaired
      here.  g4 books that as a FINDING and exits 1.
      of mg-a218's five scripts, touched by ed9cde4            -> 1 (c2)
      of the five, touched by THIS ticket                      -> 1 (c1)
      instruments agreeing on the 24 vertex cells              -> all
      c0_repro.sh, 5 of 5 outputs identical                    -> yes
      five scripts green after this ticket's repair            -> 4 of 5

P6  code/branching_audit_a218/c1_branching.py, AFTER the widening,
      run against the working tree                             -> 0
      with 24 + 53 + 121 = 198 cells compared and 0 disagreements.
P7  the SAME widened c1, run against the 286d503 target        -> 0
      (backward compatible: the count form must still be read).
P8  the SAME widened c1, run against a target with the vertex block
      REMOVED -> SELF-ERROR, not FINDING, and exit 1.  This is the
      whole point of the repair: a parser that cannot read must say
      so about ITSELF, not accuse the target.

P9  code/branching_audit_a218/run_all.sh after this ticket    -> 1
      (c3 only).
```

## Results — 8 of 9 hit, and the miss is kept as written

```
P1  selftest_58da.py            ACTUAL 0   HIT   (99 assertions, 0 failures)
P2  g1_provenance.py            ACTUAL 0   HIT
      byte-identical to committed out_c1_branching.txt   ACTUAL yes  HIT
      c1's read path is exactly ONE external file        ACTUAL yes  HIT
      exactly ONE commit touched it (ed9cde4)            ACTUAL yes  HIT
      sections (i)+(ii) byte-identical, 125 lines        ACTUAL yes  HIT
      the re-run: 24 + 53 + 121 = 198 cells, 0 disagreements, exit 0.

P3  g2_redo.py                  ACTUAL 0   HIT
      cells recovered from the HEAD target   ACTUAL 24 of 24   HIT
      recovered counts agreeing with c1      ACTUAL 24 of 24   HIT
      recovered SETS agreeing with c1        ACTUAL 24 of 24   HIT
      instruments agreeing on all 24 cells   ACTUAL 4 of 4, 6 of 6 pairs  HIT
      corruption probes that fire            ACTUAL 24 of 24   HIT

P4  g3_findings.py              ACTUAL 0   HIT
      CONFIRMED 0, PARSER ARTIFACT 24, UNKNOWN 0          HIT
      lines matching c1's count regex, HEAD      ACTUAL 0   HIT
      lines matching it at 286d5030             ACTUAL 4   HIT
        (4 rows x 6 counts = the 24 cells)
      probes fired                              ACTUAL 7 of 7 -- see the MISS

P5  g4_fleet.py                 ACTUAL 1   HIT, and for the predicted reason
      -- with ONE FINDING MORE THAN PREDICTED, and it was not predicted
      because it did not exist until this ticket made its own correction:
      mg-d330's e4 gate on mg-a218's exit-code sentence is a PRESENCE TEST
      and cannot distinguish a sentence STRUCK IN PLACE from one left
      standing.  Section (vii), added after the first run of g4, with its
      three variants each predicted before evaluation and 3 of 3 hit.
      of the five, touched by ed9cde4           ACTUAL 1 (c2)   HIT
      of the five, touched by this ticket       ACTUAL 1 (c1)   HIT
      instruments agreeing on the 24 cells      ACTUAL all      HIT
      c0_repro.sh, 5 of 5 identical             ACTUAL yes      HIT
      five scripts green after the repair       ACTUAL 4 of 5   HIT
        the red one is c3_withdrawal.py, exactly as predicted.

P6  widened c1 vs the working tree  ACTUAL 0, 24+53+121 = 198 cells, 0 findings  HIT
P7  widened c1 vs the 286d5030 target   ACTUAL 0, 24 cells read as COUNT         HIT
P8  widened c1 vs a blinded target      ACTUAL 24 SELF-ERRORS, 0 FINDINGS, exit 1 HIT
      and the same input on the UNREPAIRED c1 gives 0 SELF-ERRORS and 24
      FINDINGS, so the deletion test shows the 24 MOVING between channels.
P9  code/branching_audit_a218/run_all.sh after this ticket -> 1 (c3 only)  HIT
      (not re-run through run_all.sh, which redirects into the committed
      outputs; the five are run individually by g4 and c3 is the only red)
```

### THE MISS — `P4`, and it is a bookkeeping miss, not a channel miss

`P4` predicted *"probes fired -> all fire"*. On the first run **6 of 7** fired.
The one that did not was
`one digit of one EDGE cell (beta=0, [L(4,2)] of L(5,2) dim 1)`.

**It went RED. What was wrong was my label.** The row
`L(5,2) dim 1  ->  [L(4,0)]=0  [L(4,1)]=0  [L(4,2)]=1` is unique inside
`T1b2 (ii)` — which is why `replace_in_t1b2` accepted it — but it sits in the
`beta = 1` block, not `beta = 0`. The probe's *predicted finding text* named
`beta=0`, the finding it produced named `beta=1`, and the shape match failed.
Two other probe labels were wrong the same way.

Kept as written because the distinction matters and cuts the ticket's own way: a
probe that fires with a wrong label is a bookkeeping error, and a probe that does
not fire is a dead channel. Nothing in the conclusion moves — the channel was
live in both readings. The labels are corrected in `g3_findings.py` with the
correction recorded in the source, and all 7 now fire.

I predicted my own probe labels would be right and they were not, which is the
third time in this arc that an instrument's *description of what it measured*
went wrong while the measurement itself was fine.

---

## Addendum, `mg-7e58` (2026-07-31) — `P2` and `P5` were right; the instrument drifted away from them

`mg-321d` audited this ticket and found that **the record above was correct and
`g1` and `g4` stopped agreeing with it the instant `673b4c0` landed.** Nothing
in this file is rewritten; what follows is what became of two of its
predictions.

* **`P2  python3 g1_provenance.py -> 0` … ACTUAL 0 HIT.** True when recorded and
  false one commit later. `g1` answered *"did the measuring half change?"* with
  a **file sha**; this ticket's own edit moved `c1_branching.py` and did not
  move the measurement, so from `673b4c0` onward `g1` exited **1** on a finding
  its own section (iv) refutes. `P2`'s own sub-prediction — *"c1's own sections
  (i)+(ii) — the MEASUREMENT — are byte-identical between the two revisions →
  yes"* — is the fact that refutes it, and it is still true. `mg-7e58` moves the
  predicate to that grain and shows it firing; `g1` exits `0` again, and `P2`
  reproduces.

* **`P5 … of mg-a218's five scripts, touched by ed9cde4 -> 1 (c2)`, `of the
  five, touched by THIS ticket -> 1 (c1)`.** Both right, and `g4` printed
  **2 and 0** on the tree as committed, because it attributed by *"committed sha
  vs working-tree sha"* rather than by commit — an expression true for exactly
  as long as the change was uncommitted. `mg-7e58` derives the attribution from
  `git log` and gates the summary against `g4`'s own rows, and `g4` now prints
  the two figures `P5` predicted.

The general point, and it is why this addendum is here rather than an edit
above: **a prediction can be honestly made, honestly recorded, verified, and
still stop being true — and the thing that made it stop was this ticket's own
commit.** Evidence taken before its own commit exists is evidence about a tree
that will not survive the commit. `mg-7e58`'s `k2` branch `B1` is the check that
falls out of it: clone the worktree, commit the repair there, re-run.
