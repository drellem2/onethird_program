# `code/branching_audit_d330` — the instrument for mg-d330

The independent audit of the **mg-13b2** repair (`ed9cde4`) of
`docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md`.

```
./run_all.sh          # ~4 min, pure Python 3, no dependencies, NO NETWORK
```

Committed outputs: `out_selftest_d330.txt`, `out_e1_vertexsets.txt`,
`out_e2_labels.txt`, `out_e3_dispositions.txt`, `out_e4_rerun.txt`,
`out_e5_seam.txt`.

**Exit codes are the finding channel.** Every `e*.py` exits `0` iff
`SELF-ERRORS == 0` **and** `FINDINGS == 0`, and both numbers are printed
separately, so a non-zero exit never means the instrument is broken.
`e2` and `e4` exit `1`. Every count in every output names its population.
`PREDICTIONS.md` holds the exit code predicted for each script **before** it
was run, with the three misses kept as written.

## What each file decides

| file | what it decides |
|---|---|
| `kern_d330.py` | Temperley–Lieb half-diagrams, the cellular bilinear form, and `dim L(n,p) =` rank of the Gram matrix over `Q`, built from the combinatorial definition. **Shares no code** with `kerndb09.py` (mg-db09), `kern2060.py` (mg-2060) or `kern_a218.py` (mg-a218). It is the **fourth** instrument to measure this object. It names three different things three different ways on purpose — `vertex_set` (the labelled set), `dims_render` (the delivered column's rendering of it) and `len(...)` (a count) — because conflating them is the defect this whole arc is about |
| `selftest_d330.py` | the kernel, before it is used: **867 assertions**, non-crossing matchings against Catalan, half-diagram counts against `C(n,p) − C(n,p−1)`, Gram symmetry and entry shape, `rank` against a determinant route on 60 random matrices, semisimplicity at `β = 3`, and the rendering properties `e1` depends on |
| `e1_vertexsets.py` | **is the repaired column a SET or a rendering of one?** All 24 vertex sets re-measured; section 0's four rows compared character for character; injectivity of the rendering over **all 276** unordered pairs of the 24 cells, not the 36 the target checks; **a constructed pair of genuinely different vertex sets** that the column shows as equal; and a **deletion test** proving the two guards that make the rendering faithful are load-bearing. Also: is a count column retained, and is any figure a digest |
| `e2_labels.py` | **is "every disposition label" every disposition label?** The denominator, derived by sweeping the document for the disposition vocabulary rather than taken from `t5_labels.py`'s hand-written list of 29; and the seven sites at which figures about `t5` are restated with none deriving them |
| `e3_dispositions.py` | **every row of section 8's status table, against the diff, both directions**, written afresh against `git show` and sharing nothing with `t5_labels.py`. X2's four sites one at a time in both directions, X3/X5/X6/95.7% in the harder direction (an OPEN label is falsified by a silent closure), `Repaired 1`'s five sites, and a **whole-tree sweep for a fifth site of X2** with a calibration probe |
| `e4_rerun.py` | **the thing no list names.** mg-a218's own five `c*.py` scripts, re-run against the repaired tree, each verdict classified |
| `e5_seam.py` | the seam between mg-a218 and mg-13b2: 38 passages `ed9cde4` deleted against 1 619 swept units in 6 files, **61 522 comparisons**, threshold **0.80**, with two calibration probes built from lines the repair really deleted |

## Independence

Written fresh for this ticket. It imports nothing from `branching_locate_db09`,
`branching_audit_2060` or `branching_audit_a218`. It **reads** their files, and
`e4` **runs** mg-a218's scripts — with their stdout captured here, never
redirected into their committed outputs, because a committed audit output is
the record of what that audit found and not a live gate.

## Two things widened or corrected during construction, neither silently

Per this repo's convention, each is recorded in the source with its reason
rather than in a commit message.

* `e1`'s marked-window for the withdrawn count rendering was **widened** from
  the line to the line and its predecessor, because section 8's own repair note
  wraps and put the marker `It printed` at the end of the line above.
* `e3`'s whole-tree sweep vocabulary was **widened** from the
  withdrawal/correction words to include the words a refutation uses, and its
  window from 4 to 8 lines, after the first run returned 17 sites none of which
  was an assertion. Because that is a real loosening it is **calibrated**: an
  injected bare assertion must still be caught and a marked one must not.
* `e5`'s calibration probes were **corrected** from sentences I wrote to lines
  the repair really deleted, after the script's own self-error channel said the
  invented ones could not reach the threshold. `e2`'s block-coverage test was
  corrected in the direction that **removes** findings.
* `selftest_d330.py` had one assertion written `... or True`, which cannot
  fail. It is replaced by the real statement and the replacement is recorded in
  place, because a decorative assertion counted in an assertion total is this
  arc's own worst habit.
