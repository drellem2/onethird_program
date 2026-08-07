# `mg-910c` — the RATE staleness sweep

`mg-00a1` proved the disjunctive per-slot value is `Θ(n²)`, SUPERLINEAR. That refutes
`mg-200d`'s headline — *"per-slot adjacency symmetry buys `Θ(n²) → Θ(n)`"* — and not merely its
formula. **Per-slot buys a constant factor of at most `6`, not an order.** The claim was live on
`main` in three documents and one instrument docstring and no ticket covered it. This is the
count behind that correction. A staleness sweep is a CHORE, not a claim, so there is no
independent audit and the reportable count is the control instead.

| script | what it does |
|---|---|
| `r1_census.py` | sweeps **six spellings** across the whole repo and prints the distribution by spelling and by file. Marks which files a NARROW spelling reached. Counts; does not classify. |
| `r2_classify.py` | carries the hand classification of **26 sites**, one row each, and **checks** that every site classed `LIVE`/`LIVE-OPEN` now carries this ticket's marker and a word saying it is wrong, in the block a reader reads. Exits non-zero if not. |
| `r3_control.py` | four pre-declared mutations, including running `r2` against the unrepaired tree at `main`. Nothing on disk is touched — every mutation is applied to a copy in a temp directory. |

`sh run_all.sh` runs all three (~2 s). Committed transcripts are `out_*.txt`.

## Why this is not `mg-372e`'s sweep run again

`mg-372e` swept `ε_spec = 2/(n+1)` — the **FORMULA** — and swept it well: 13 LIVE sites struck
across two documents, and it named the `COLLISION` class that saved three more. **It could not
have caught this**, for two independent reasons:

1. **The RATE is a different string.** A document can carry a correct strike of the formula and
   assert the rate one paragraph later. `mg-6bc2` and `mg-200d` both do exactly that.
2. **It ran BEFORE `mg-00a1` returned.** At that moment the rate was *"three points and no
   proof"* — thin, but not false. `mg-372e` said so, in those words, and left it standing
   deliberately. That was the right call on the evidence it had.

`mg-372e`'s sweep still **PASSES** unchanged against every strike this ticket made, and its four
negative controls still fire as pre-declared. Checked, not assumed.

## Five classes, and why the fifth was needed

`mg-372e` had four. This sweep needed one more, because the rate had already been *half*
corrected once — and a half-correction leaves a claim behind.

* **LIVE** — asserted as current. Struck in place with `mg-00a1` cited beside it.
* **LIVE-OPEN** — asserted as an **open question**: *"the rate is UNKNOWN"*, *"what IS the true
  growth?"*. **This is also a claim and it is also now false**, because `mg-00a1` settled it.
  Ten of the nineteen repairs are this class, and every one of them is `mg-372e`'s own correct
  strike of the formula, which routed the reader to `mg-00a1` as *the open question*. It was
  right when written and it stopped being right the same evening.
* **CITED** — named as the refuted claim, or already inside a `~~strike~~` that says so. LEAVE.
* **SURVIVES** — a `Θ(n)` statement about **ONE BRANCH**: `mg-131e` §2's consecutive-pairs
  theorem `val = (n−1)/3`, and the `(5n−8)/12` chord sub-family. Both are **correct and
  linear**; a max-over-all-branches result does not touch them. LEAVE, and make sure no reader
  thinks the strikes reached them.
* **COLLISION** — `Θ(n²)` or `Θ(n)` describing a **different quantity**. LEAVE, and say so.

**The collision class is the trap here and it is worse than in `mg-372e`'s sweep.** `Θ(n²)` is
also the correct answer for the baseline `n(n−1)/6`, for the two-atom law's inversion count
(obstruction 4), for `(LIB-const)` against the uniform footrule — **and for `mg-00a1`'s own new
theorem.** `Θ(n)` is the correct answer for the consecutive-pairs branch and for `LIBweak`'s
mobility configurations. `r1`'s last two patterns are deliberately over-wide and reach **104
line-hits across 32 files that no narrow spelling touches at all** — every one of them left; a
blanket edit on the string would have struck the theorem that motivated the sweep.

## What the controls establish, and what they do not

**Three of the four controls FAILED on first run, against code I had just written**, and each
failure was a real defect rather than a mis-declaration:

* **`N3` did not fire.** The plant writes each half in its own code span —
  `` `Theta( n^2 )` to `Theta(n)` `` — and the first `ARROW` pattern required *whitespace*
  between them, so backticks defeated it. **This is the `mg-7085` hazard, and it fired against
  this sweep's own instrument before it could fire against a document.** The pattern now
  tolerates markup between the halves — and re-running the widened census on `main` found **one
  further real site**, `mg-200d:60`, written `` from `Θ(n²)` to `Θ(n)` ``, which the first
  pattern had returned a clean zero on. It is in the table as `ARROW`, and it had been found by
  reading before the control found it.
* **`N0` reported 7 unrepaired sites on `main` instead of 19.** The detector accepted `mg-00a1`
  *or* `mg-910c` as the citation — and `mg-372e`'s strikes **already cite `mg-00a1`**, as the
  open question. Citing `mg-00a1` is exactly what a `LIVE-OPEN` defect does; it is not evidence
  of repair. Narrowed to this ticket's own marker.
* **`N2` destroyed 13 of its own anchors.** It stripped every marker word, including `Θ(n²)`,
  which is *in* the anchors. A mutation that deletes the thing it is measuring is not a control.
  It now strips the citation only — the minimal mutation that undoes repair as `r2` defines it.

`N1` behaved as pre-declared first time: stripping the `~~` glyphs alone does **not** fire,
because the detector is keyed on the refutation being *said*, not on the glyph. Same result
`mg-372e`'s `M0` got, reported the same way rather than tuned away.

**What this does NOT establish.** It does not check the mathematics — `mg-00a1` did that and is
cited, not restated, and this ticket was forbidden from re-deriving it. `r2` checks that each
site is **marked**, not that its **class** is right; the classification is a judgement and it is
written out in full so it can be disagreed with per row. And `r2`'s check, stated at the
strength it has, is *"`mg-910c` touched this block and said something in it was wrong"* — the
substance is the table, not the regex.

## Out of scope, deliberately

`STATE.md` carries the rate at `:167` and `:168`. **It is not edited here**: `mg-bb87` owns
those sites and is serialising through `main` behind another `STATE.md` writer. `r1` counts them
and `r2` does not list them.

## `mg-372e`'s sweep, re-run against these strikes

`out_mg372e_rerun.txt` is `mg-372e`'s own three scripts run against this branch, captured
**here** rather than by overwriting its committed transcripts — those are its record of its run,
not a checkable of mine. It **PASSES**, and its four negative controls all still fire as
pre-declared. So nothing struck here has broken the formula sweep that preceded it.
