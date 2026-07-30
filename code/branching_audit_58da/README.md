# `code/branching_audit_58da` — the instrument for mg-58da

`mg-d330` returned PARTIAL with one item open, and it was two questions wearing
one label. This directory answers them **separately**, because they have
different answers.

> **A. Are the 24 findings real?** — a question about `c1_branching.py`'s parser
> **now**.
> **B. Does the 198-cell reproduction still stand?** — a question about
> **provenance**, settled by re-running at the old revision.

```
./run_all.sh          # ~1 min, pure Python 3, no dependencies, NO NETWORK
```

Committed outputs: `out_selftest_58da.txt`, `out_g1_provenance.txt`,
`out_g2_redo.txt`, `out_g3_findings.txt`, `out_g4_fleet.txt`.

**Exit codes are the finding channel.** Every `g*.py` exits `0` iff
`SELF-ERRORS == 0` **and** `FINDINGS == 0`, and both numbers are printed
separately, so a non-zero exit never means the instrument is broken. `g4` exits
`1`, and it was predicted to. Every count names its population.
`PREDICTIONS.md` holds the exit code and the substantive answer predicted for
each script **before** it was run, together with the one miss, kept as written.

## The two answers, up front

**B. THE REPRODUCTION STANDS AT `286d5030902d`, and it is redone at HEAD.**
`c1_branching.py` and `kern_a218.py` are byte-identical at `286d5030` and at
`d1dd84d2`; `c1` reads exactly **one** external file
(`code/branching_locate_db09/out_t1_tl.txt`); exactly **one** commit (`ed9cde4`)
touched it. Re-run at `286d5030` just now: 24 + 53 + 121 = **198 cells
compared, 0 disagreements, exit 0**, and the output is **byte-identical** to the
committed `out_c1_branching.txt`. `ed9cde4` *did* touch the read path, so the
comparison was redone at HEAD — and it comes out **stronger**, not weaker: the
24 cells that were compared as cardinalities are now compared as **labelled
sets**, 24 of 24 agreeing, on 4 independent kernels, 6 of 6 pairs.

**A. ALL 24 FINDINGS ARE PARSER ARTIFACTS. 0 CONFIRMED, 0 UNKNOWN.** Each was
established individually before any was called a defect. At every one of the 24
cells the target states the vertex **set** — strictly more than the count `c1`
looks for — and it agrees with `c1`'s own measurement label for label. The
target disagrees with `c1` nowhere. The real defect is `c1`'s: `mg-13b2` deleted
the count table on `c1`'s **own** finding X1, `c1`'s parser was not widened with
`c2`'s, and `tgt_counts.get(beta, [None] * 6)[n - 1] != mine_c` renders
**absence as disagreement**.

And the half a count cannot answer: a blind parser produces findings *and
non-findings* with equal confidence, so `c1`'s **0 disagreements over the other
174 cells** is worth nothing until it is probed. It is probed — 7 of 7
corruption probes fire, so those 174 are a measurement.

**One new finding, produced by making this ticket's own correction.**
`mg-d330`'s `e4_rerun.py` gate on mg-a218's exit-code sentence is a **presence
test** (`if CLAIM in adoc`), so a sentence **struck in place** with a correction
beside it is indistinguishable from one left standing, and `e4`'s finding
text — *"left unchanged and unmarked"* — is now false of the tree while its exit
code is unchanged. **Booked, not worked around:** rewriting the sentence to dodge
the substring would turn the gate green while leaving it blind, which is the
defect this arc keeps paying for.

## What each file decides

| file | what it decides |
|---|---|
| `lib58da.py` | the reading and re-running apparatus. `run_c1()` re-runs `c1_branching.py` **at a named revision** against target text the caller supplies, in a scratch tree — which is what lets the same script be run at the old revision, at the new one, and against a target corrupted one character at a time. The parsers share no line with `c1`'s, which is the reason the two can disagree about whether the datum is there |
| `selftest_58da.py` | the apparatus before it is used: **99 assertions**, including a cell-locality sweep over all 24 vertex cells (corrupting one must move the parse **at** that cell and **nowhere else**), the parsers' behaviour on absent and hostile input, and `replace_once` refusing to corrupt zero sites or two |
| `g1_provenance.py` | **QUESTION B.** The revision named; `c1`'s read path found in its source rather than assumed; every commit touching each part; `sha256` of the measuring half at both revisions; the re-run at `286d5030` byte-compared against the committed record; and whether the **measurement** moved or only the **comparison** (it did not move — sections (i)+(ii) are byte-identical, 125 lines) |
| `g2_redo.py` | **QUESTION B at HEAD.** The 24 vertex cells recovered from the set block `mg-13b2` installed and compared as sets and as counts; the same 24 on all four kernels in the tree, pairwise; and **24 corruption probes**, one per cell, each required to go red at that cell and nowhere else |
| `g3_findings.py` | **QUESTION A.** The mechanism measured (4 rows match `c1`'s regex at `286d5030`, 0 at HEAD); the 24 classified **one at a time** into CONFIRMED / PARSER ARTIFACT / UNKNOWN; and the **non-findings** audited — 7 corruption probes on the dimension and edge channels, plus a null probe and a control on the count channel *at the old revision, where it was live* |
| `g4_fleet.py` | **the property that lives BETWEEN the instruments.** The five named; who touched which member and by which commit; all five run at three revisions; the figures more than one member carries compared across members and across instruments; `c0_repro.sh`; the repair deletion-tested in the direction that matters — the widened `c1`, handed a target it cannot read, must raise **SELF-ERRORS and not FINDINGS**; and **(vii)**, found by making this ticket's own correction: `mg-d330`'s `e4` gate on the exit-code sentence is a **presence test** with no state for *present and marked*, evaluated on three variants |

## What this ticket changed outside its own directory

Two things, both because this ticket's own change moved them.

* **`code/branching_audit_a218/c1_branching.py` is widened**, with the note in
  the source and its reason, per this repo's convention. It reads either form,
  prefers the **set** (a stronger comparison than the audit originally made),
  still reads the **count** so a re-run at `286d5030` still compares all 24, and
  books a cell it **cannot** read as a `SELF-ERROR`. Its committed
  `out_c1_branching.txt` is **not** regenerated — the call `mg-a318` made for
  `mg-8a5c` and `mg-13b2` made for `c2` — and `g1` re-runs the script at
  `286d5030` and confirms that file byte for byte, so the record is *checkable*
  rather than merely preserved.
* **`docs/…-Mge8b8Repair-IndependentAudit.md` §10's exit-code sentence** is
  struck and corrected with a table of all three revisions. It was
  present-tense instructions to a reader who would run the code and get another
  answer — `mg-d330`'s F9 — and this ticket's own change moves it again, so
  leaving it would be the same defect one commit later.

## No fifth kernel, deliberately

Neither question is about Temperley–Lieb. The mathematics is measured by four
instruments already — `t1_tl.py` (mg-db09), `b1_branching.py` (mg-2060),
`kern_a218.py` (mg-a218), `kern_d330.py` (mg-d330) — and `g2` shows all four
agreeing on all 24 vertex cells, 6 of 6 pairs. What this ticket needs to be
independent about is the **parsing** and the **re-running**, so that is what is
written fresh here.

## One thing corrected during construction, not silently

`g2`'s reader for `mg-2060`'s `out_b1_branching.txt` was first written with the
beta-header pattern `r"\s*beta = (\d+)\s*$"`, copied from the shape `T1b2` and
`e1` use. `b1` writes `    beta=3:`. The parser matched nothing, returned 0
cells, and the script booked **three findings** saying mg-2060's instrument
disagreed with the other three about all 24 cells. It agrees at 24 of 24.

That is this ticket's own subject happening to this ticket's own code, and it is
left recorded because it is the cheapest possible demonstration of the thing
being audited. Two things changed as a result and both are load-bearing: the
pattern accepts both header forms, **and** a parse that yields no cells now
raises a `SELF-ERROR` and **withdraws** the instrument from the comparison
instead of scoring it as a disagreement — because *"I could not read it"* and
*"it disagrees"* are different statements and only the second is a finding
against anyone else. That distinction is now in the control flow rather than
left to care, in this directory and in `c1_branching.py` both.

Three of `g3`'s probe labels named `beta = 0` for rows that sit in the `beta = 1`
block. Every probe still **fired**; the labels and one predicted finding-text
were wrong, and the miss is kept in `PREDICTIONS.md` as written.
