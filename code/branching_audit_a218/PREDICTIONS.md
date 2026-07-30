# mg-a218 — exit codes predicted BEFORE the run

Written before any script in `code/branching_audit_a218/` was executed and
before `code/branching_locate_db09/run_all.sh` was run in this worktree.
**Wrong predictions are kept as written.** Anything marked WRONG below is
corrected only in the "outcome" column, never in the "predicted" column.

**Exit-code convention for this instrument.** Every `c*.py` exits `0` iff
`SELF-ERRORS == 0` **and** `FINDINGS == 0`. A non-zero exit therefore means
*"this script has something to report"*, not *"this script is broken"* —
and both numbers are printed separately so the code is never ambiguous.
`selftest_a218.py` exits `0` iff every assertion in it passes.

| # | command | predicted exit | why I predict it |
|---|---|---|---|
| 1 | `python3 selftest_a218.py` | **0** | the kernel is standard TL; the published RSA controls should reproduce |
| 2 | `python3 c1_branching.py` | **0** | I expect mg-e8b8's `T1b2` numbers to be right — mg-2060 already measured them on a second instrument and got the same, so a third should agree |
| 3 | `python3 c2_vertexsets.py` | **1** | the document's vertex column is a **count** (`1,2,2,3,3,4` for β = 3, 2 **and 1**). I predict the vertex *sets* differ at β = 1 too — by the dimensions of the irreducibles — so the column is a second matching statistic, exactly the failure mode the repair is repairing. I also expect the repair's own new cross-instrument claim ("agrees ROW FOR ROW with mg-2060's B1a/B1b") to be only partly checkable, because mg-2060 published a count and five edges, not rows |
| 4 | `python3 c3_withdrawal.py` | **0** | reading the document, the withdrawal looks complete, D10 reads as a conjecture, the retraction is in §0 and §5, and §4 item 3 looks intact |
| 5 | `python3 c4_seam.py` | **0** | I expect no stale duplicate: the withdrawn sentence appears several times but always inside a withdrawal |
| 6 | `python3 c5_record.py` | **0** | I expect the 19:50 / 20:45 / 55-minute record to check out against git |
| 7 | `bash c0_repro.sh` (re-run the target's `run_all.sh`, diff its 5 committed outputs) | **0** | mg-e8b8 says 5 of 5 identical against the repaired code |
| 8 | `bash run_all.sh` (this audit) | **1** | it propagates the worst exit code, and I predict c2 is non-zero |

## Predicted findings, in words, before the run

1. **The vertex-set column is a count.** §0's table heading is *"# irreducibles
   at `n = 1…6`"* and it prints `1, 2, 2, 3, 3, 4` for β = 3, 2 and 1 alike.
   Measured, I predict the irreducibles at β = 1 do **not** have the same
   dimensions as at β = 3 (`L(3,1)`, `L(4,2)`, `L(5,2)`, `L(6,1)`, `L(6,3)` are
   the ones I expect to shrink), so the β = 1 graph and the β = 3 graph have
   the same number of vertices and **not the same vertices**.
2. Everything else in `T1b2` reproduces exactly.
3. No stale duplicate in the block quotes above a 0.80 similarity threshold.
