# `code/branching_audit_321d/` — the instrument for `mg-321d`

**Independent audit of `mg-58da` (`673b4c0`)**, which repaired
`code/branching_audit_a218/c1_branching.py` after `mg-d330` (`f9f8220`) found
that a re-run raised **24 findings** against the target where `c1`'s own parser
had gone blind.

Companion document:
`docs/OneThird-Bratteli-Path-Algebras-Mg58daRepair-IndependentAudit.md`.

```
./run_all.sh        # ~3 min, pure Python 3, NO NETWORK
```

## This instrument is not one of the five, and cannot become one

`mg-a218`'s five are `c1_branching.py`, `c2_vertexsets.py`,
`c3_withdrawal.py`, `c4_seam.py`, `c5_record.py`. This instrument:

* lives in its own directory and is invoked by no `run_all.sh` but its own;
* **writes into `code/branching_audit_a218/`, `code/branching_audit_58da/` and
  `code/branching_locate_db09/` never.** Every re-run of `c1` happens in a
  scratch tree under `$TMPDIR`; the five and `g1`/`g4` are run *in place* with
  their stdout captured here and never redirected into a committed `out_*.txt`;
* shares no reader with `c1`, with `c2`, or with `lib58da.py` — see below.

## The scripts

| | asks | exits |
|---|---|---|
| `selftest_321d.py` | is this instrument's own reader calibrated? 60 assertions | **0** |
| `h1_questions.py` | were **A** and **B** kept separate, and is each answered? | **0** |
| `h2_grain.py` | is the narrowing at the **grain** of the blindness? | **1** |
| `h3_setlevel.py` | was the agreement across **all five** re-established? | **1** |
| `h4_mine.py` | the two things this audit chose | **1** |
| `h5_doccheck.py` | does this audit's own **document** say what its own run said? Every figure read back **at its site**, each gate deletion-tested — 16 of 16 fire | **0** |

`PREDICTIONS.md` holds the exit code **and the substantive answer** predicted
for each script before it was run, with the misses kept as written.

## The third reader, and why it is written rather than borrowed

Three readers that disagree about whether a datum is *present* is the apparatus
this whole arc turns on, so this one is built:

* **`c1`'s** count form matches seven bare integers anywhere in `T1b2`.
* **`lib58da`'s** matches `beta = <b>` headers anywhere in `T1b2`.
* **this one** is not regex at all. It locates the subsection header
  `(i) THE VERTEX SET` first, stops at `(ii)`, and splits rows on literal
  delimiters. Anchoring on the **subsection** is the difference that matters:
  a stray row of digits elsewhere in `T1b2` cannot reach it, which is precisely
  the residue `h4` books against the repaired `c1`.

`selftest_321d.py` asserts the anchoring in **both directions** — the poison row
placed after `(ii)` is not read, and the same row placed inside `(i)` **is** —
so the assertion cannot pass by the reader being inert.

## THIS INSTRUMENT MADE THE ERROR IT WAS SENT TO FIND, ON ITS FIRST RUN

`h3`'s reader for `mg-2060`'s `out_b1_branching.txt` matched only
`--- beta = b ---`. `mg-2060` writes `beta=3:`. The reader recovered **0 of 24**
cells and the cross-instrument comparison duly booked **four findings** against
an instrument that agrees with the target at 24 of 24 — **absence rendered as
disagreement**, which is the exact defect this audit exists to check, happening
inside the auditing instrument.

It is recorded rather than quietly fixed, and the fix is in **two** places:

1. the pattern accepts both header forms;
2. a source the script cannot read is booked as a **`SELF-ERROR`** and
   **excluded from the compared population** — the control-flow fix, not the
   careful-reading fix.

That second half is the one that matters, and it is the same call `mg-58da`
made inside `c1`. `h3`'s output now prints *"sources this script could read: 5
of 5"* beside the pair count, so a blind reader shows up as a shrinking
population rather than as a pile of findings.

## What is NOT here

No fifth Temperley–Lieb kernel: neither this audit's questions nor its parent's
are about the mathematics, which five sources in this tree now measure and agree
on at 24 of 24 cells, 10 of 10 pairs (`h3 (iv)`). No re-derivation of
`mg-d330`'s other findings. No search here was exhaustive.
