# `mg-d330` --- exit codes predicted BEFORE running

Written before any script in this directory was run, and before mg-a218's
instrument was re-run.  **The misses are kept exactly as written.**  Three of
eighteen are wrong, and two of the three are wrong in the same direction: I
predicted the auditing instrument would be in a better state than it is.

```
mg-d330 EXIT-CODE PREDICTIONS -- written BEFORE running. Misses kept as written.

P1  python3 code/branching_locate_db09/t5_labels.py            -> 0   ACTUAL 0   HIT
P2  python3 code/branching_locate_db09/t1_tl.py                -> 0   ACTUAL 0   HIT
      and out byte-identical to committed                       -> yes ACTUAL yes HIT
P3  python3 code/branching_audit_a218/c2_vertexsets.py         -> 0   (doc says it now prints CLOSED)
P4  diff live c2 output vs committed out_c2_vertexsets.txt     -> DIFFER (doc says not regenerated)
P5  code/branching_audit_a218/run_all.sh                       -> 1   (c4,c5 still find X2/seam)
P6  mg-a218 doc sentence "c2, c4 and c5 exit 1" now stale      -> STALE, and unmarked
P3  ACTUAL 0      HIT
P4  ACTUAL DIFFER HIT
P5  ACTUAL 1      HIT (but for DIFFERENT reasons than predicted: c4 and c5
      now exit 0 -- the repair closed them -- while c1 exits 1 with TOTAL BAD 24
      and c3 exits 1. Predicted "c4,c5 still find X2/seam": WRONG in substance.)
P7  code/branching_audit_a218/c0_repro.sh                      -> 0  ACTUAL 0 HIT
P8  c1_branching.py's 24 BAD are SELF-ERRORS (a stale parser), not FINDINGS
P9  c3_withdrawal.py's 1 BAD is a FINDING (a withdrawn phrase now unmarked)
P8  ACTUAL: WRONG. c1's 24 BAD are booked as FINDINGS ("target ?"), not
      SELF-ERRORS. The instrument accuses the target of disagreeing when its
      own parser can no longer read the target's rewritten output. Kept as
      written: I predicted the milder failure mode.
P9  ACTUAL 1 FINDING  HIT (c3: 4 unmarked occurrences of two withdrawn
      phrases, all four inside mg-13b2's OWN new t5_labels.py and its output)
P10 c4_seam.py live   -> 0  ACTUAL 0 HIT (the repair marked t1_tl.py:368)
P11 c5_record.py live -> 0  ACTUAL 0 HIT (section 8's list is now accurate)
P12 e1_vertexsets.py -> 0.  Predicted BEFORE running: the four rows reproduce
      on my fourth instrument; the rendering is injective on all 276 pairs
      (0 collisions); the constructed pair B collides with A in the column but
      the guards go RED on it and GREEN when deleted; no count column.
P13 e2_labels.py -> 1.  Predicted BEFORE running: t5's LABELS is a hand-written
      list with no derived denominator, so some disposition-marked lines will
      be unreached (D9's "UPGRADED by mg-2060" and section 2 row 3's "PARTLY
      EVALUATED" are my named guesses); and the 29/100/7 figures are restated
      at several sites and derived at none.
P14 e3_dispositions.py -> 0.  Predicted BEFORE running: all four X2 sites are
      genuinely closed in both directions and the two-commit attribution holds;
      X3/X5/X6/95.7% are genuinely open; the five sites of "Repaired 1" are all
      marked; and the whole-tree sweep finds NO fifth site of X2.
P15 e4_rerun.py -> 1.  Predicted BEFORE running: c1 goes red with 24 stale
      "target ?" count cells and 0 dimension/edge disagreements; c3 goes red on
      mg-13b2's own t5_labels.py; c4 and c5 go green because the repair closed
      them; and mg-a218's document's "c2, c4 and c5 exit 1" is now false.
P16 selftest_d330.py -> 0
P17 e5_seam.py -> 0.  Predicted BEFORE running: mg-13b2 marked its edits in
      place, so every survivor above 0.80 is marked; both calibration probes
      reach the threshold.
P18 run_all.sh -> 1 (e2 and e4 report; the rest are clean)

```

## Scoreboard

| # | what | predicted | actual | |
|---|---|---|---|---|
| P1 | `t5_labels.py` | 0 | 0 | right |
| P2 | `t1_tl.py`, and byte-identical | 0 / yes | 0 / yes | right |
| P3 | `c2_vertexsets.py` | 0 | 0 | right |
| P4 | c2 output vs its committed copy | differ | differ | right |
| P5 | mg-a218's `run_all.sh` | 1 | 1 | **right in the code, WRONG in the reason** |
| P7 | `c0_repro.sh` | 0 | 0 | right |
| P8 | c1's 24 BAD are SELF-ERRORS | self | **findings** | **WRONG** |
| P9 | c3's 1 BAD is a finding | finding | finding | right |
| P10 | `c4_seam.py` | 0 | 0 | right |
| P11 | `c5_record.py` | 0 | 0 | right |
| P12 | `e1_vertexsets.py` | 0 | 0 | right |
| P13 | `e2_labels.py` | 1 | 1 | right |
| P14 | `e3_dispositions.py` | 0 | 0 | right |
| P15 | `e4_rerun.py` | 1 | 1 | right, in all four parts |
| P16 | `selftest_d330.py` | 0 | 0 | right |
| P17 | `e5_seam.py` | 0 | **1, then 0** | **WRONG** --- my own calibration probes were invented sentences and did not reach the threshold; the script said so and I rewrote them from real deleted lines |
| P18 | `run_all.sh` | 1 | 1 | right |

**15 of 18 right.** The two substantive misses:

* **P8.** I predicted `c1_branching.py`'s breakage would be booked as
  SELF-ERRORS --- the milder failure. It is booked as 24 **FINDINGS**, so the
  instrument accuses the target of disagreeing at cells where its own parser
  went blind. I predicted the wrong failure mode and the real one is worse.
* **P5.** I got the exit code right for the wrong reason: I predicted `c4` and
  `c5` would still be red. They are green --- the repair genuinely closed both
  --- and the 1 comes from `c1` and `c3` instead. The number was right and
  every word behind it was wrong, which is exactly what a bare exit code hides.
* **P17** is a miss against my own instrument, not the target's, and it is the
  reason the seam sweep's calibration is now built from passages the repair
  really deleted rather than from sentences I wrote.
