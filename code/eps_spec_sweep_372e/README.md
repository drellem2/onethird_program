# `mg-372e` — the `ε_spec = 2/(n+1)` staleness sweep

`mg-131e` refuted `ε_spec = 2/(n+1)` at `n = 6`. `mg-b488` landed that into `STATE.md` and
scoped itself there, saying so at `STATE.md:168`. **The source documents were never corrected.**
This instrument is the count behind that correction — a staleness sweep is a CHORE, not a claim,
so there is no independent audit and the reportable count is the control instead.

| script | what it does |
|---|---|
| `s1_census.py` | sweeps **six spellings** across the whole repo and prints the distribution by spelling and by file. Names what the count is a count of. |
| `s2_classify.py` | carries the hand classification of every `docs/` occurrence and **checks** that in the two repaired documents every occurrence is either marked with the refutation or on an explicit leave-alone allowlist. Exits non-zero if not. |
| `s3_control.py` | mutates the repaired documents **in memory** and asserts the `s2` detector fires. Nothing on disk is touched. |

`sh run_all.sh` runs all three (~1 s).

## Why six spellings and not one

The ticket named `2/(n+1)`. A sibling sweep tonight missed a live defect because its ticket
named one spelling and the live site was written another way. So the patterns are
whitespace-tolerant and cover the same statement in **three currencies**:

* `EPS` — `2/(n+1)`, spaced forms, `\frac{2}{n+1}` — the `ε_spec` normalisation
* `EINV` — `(n−1)/3` — **the same conjecture in `E[inv]` units**, which is how `mg-200d`'s
  Conjecture 4.3 is actually stated
* `DQ` — `2/(3n)` — the same conjecture in `d·q̄` units, `mg-200d §6`
* `PROSE` — *"two over n plus one"*, *"the per-slot constant"*

`s3`'s **M3** plants a live site spelled `2/(n + 1)` with spaces and confirms it is caught. A
sweep grepping the literal string `2/(n+1)` would have returned a clean zero on it.

## The classification, and why most sites are NOT defects

Three kinds, and only the first is a defect:

* **LIVE** — printed as a current value, or as a thing the programme still has. An *open
  conjecture* counts: the reader is not told it is false. **Repaired: struck in place with the
  refutation beside it**, this corpus's own practice.
* **CITED** — named as the refuted formula, or as historical/superseded. Already correct.
* **DERIVED** — inside `mg-131e`'s or `mg-94c3`'s own argument *about* it. Correcting these
  would make a document disagree with its own subject.

A fourth class the ticket did not anticipate and the sweep found:

* **COLLISION** — the same expression, a **different quantity**. `1 − λ_std(W_n) ≤ 2/(n+1)` is
  the Cheeger bound on the witness poset `W_n = C_n ⊔ C_1` and has nothing to do with the
  per-slot value; `n(n−1)/3` is an inversion *radius*. **A blanket edit on the string would have
  corrupted three documents.**

## What the controls establish, and what they do not

`s3` runs four mutations, each pre-declared. **M0 is declared NOT to fire and does not:**
stripping the `~~` glyphs alone leaves the words *"REFUTED"* and *"mg-131e"* in the same block,
so the refutation still travels with the site and the detector is right not to complain. That is
reported rather than tuned away — the detector is keyed on the refutation being *said*, not on
the glyph. `M1`/`M2` strip the glyphs **and** every marker word and fire at 7 and 20 sites.

`s2`'s first version was scoped to the **line** and fired 13 times against correctly-marked
prose, because a markdown strike routinely opens on one line and closes two lines later. It was
widened to the enclosing **block** — the unit a reader actually reads. **No site was moved onto
the allowlist to silence that**; the two allowlist entries added afterwards are inside
`mg-372e`'s own banner, where the formula is printed in order to say which sites were left, and
they are named there with that reason. A pattern relaxed until it returns `0` is unfalsifiable.

## ⛔ ONE ALLOWLIST ENTRY IS NOW WRONG — *"the headline left"* (`mg-00a1`, recorded by `mg-910c`)

`s2`'s `mg-200d` allowlist reads *"8 LIVE struck in place; THEOREM 4.2, the `n ≤ 5` table and
**the headline** left"*, and the README above classes allowlisted sites as *"true as written"*.
**The headline is no longer true as written.** `mg-00a1` proved the disjunctive per-slot value
is `Θ(n²)`, so *"per-slot adjacency symmetry buys a factor that grows with `n`, not a constant"*
is REFUTED — what it buys is a constant factor of at most `6`.

**This instrument is not edited and its outputs are not regenerated**, because the decision it
records was CORRECT WHEN MADE: this sweep swept the FORMULA `2/(n+1)`, and it ran **before**
`mg-00a1` returned. The RATE is a different string and was out of its reach, by timing and by
pattern. `mg-910c` is the sweep of the rate; the headline and the eight other rate sites are
struck there, and `s2` still **PASSES** unchanged against those strikes (checked, `2026-08-07`).
Nothing above this section is retracted.

**What this does NOT establish.** It does not check the mathematics — `mg-131e` did that and is
cited, not restated. It does not classify `code/` occurrences: those are instrument transcripts
and pre-registration artefacts (`mg-ba78` set the precedent of leaving `PREDICTIONS.md`
byte-identical), and they are counted but deliberately not repaired. And a classification is a
**judgement**: `s2` checks that each site is marked or allowlisted, not that the class is right.

## ⛔ THE COMMITTED `out_s*.txt` ARE STALE AT HEAD, AND THEY ARE DELIBERATELY NOT REGENERATED (`mg-188d`, `2026-08-10`)

`mg-2f44` measured that the staleness is not its doing — a run with its two files reverted
differs from the committed outputs identically — and left it. `mg-188d` was sent to decide it,
with an instruction to say which way it went rather than to quietly refresh. **DECIDED: NOT
REGENERATED.** Three reasons, in the order they were established.

**1. The interaction the ticket named has already resolved, and it was never the cause.** The
ticket said to weigh regeneration against `mg-e331`, open at the time on `STATE.md` growing with
no ratchet, on the ground that these outputs go stale from that growth so a refresh would expire
the same way. `mg-e331` is **DONE** — the ratchet landed at `42b5bb0` and is wired into
`build.sh` — so there is nothing left to wait for. **And it would not have helped:** the sweep's
population is the whole repository, and `STATE.md` is **0.24%** of the drift. Measured, both runs
committed against each other:

| | committed | re-run at HEAD |
|---|---|---|
| form-hits, all files | 288 | 709 |
| of which `STATE.md` | 3 | 4 |
| files carrying a spelling | 50 | 137 |

**+421 hits, of which `STATE.md` contributes +1.** 87 files joined the corpus and carry 412 of
them. A ratchet on one file cannot bound a count over 137, so *"wait for the ratchet"* was the
wrong question and *"regenerate now"* would have been answered by the wrong reason.

**2. Nothing stale here is a verdict.** `s2` and `s3` were re-run at HEAD and both still **exit
0**: every `docs/` site is still marked or allowlisted, and all four pre-declared mutations still
score as declared. What moved is `s1`'s **census**, which this file's own header calls *a count of
textual occurrences, NOT a count of defects*. A dated reading is expected to go stale; an
expectation is not, and the expectations still hold — `mg-724a`'s recorded/gated distinction,
applied to a transcript rather than to a gate.

**3. Regenerating would overwrite the only dated reading there is, with an undated one.** The
committed transcripts are the record of what the corpus looked like when the classification was
made, and that record is what makes *"correct when made"* in the section above checkable. A
refresh replaces it with a number that is stale again at the next landing and carries no date at
all — `mg-2ff6`'s convention, and the failure it names.

**WHAT WOULD CHANGE THIS.** A re-run in which `s2` or `s3` exits **non-zero**: that is a
classification going wrong rather than a count moving, and it is a defect rather than staleness.
Look at the exit codes, not at the counts — and **do NOT use `sh run_all.sh` to look**:

```sh
python3 code/eps_spec_sweep_372e/s2_classify.py >/dev/null; echo "s2 $?"
( cd code/eps_spec_sweep_372e && python3 s3_control.py >/dev/null ); echo "s3 $?"
```

**`run_all.sh` PIPES EVERY SCRIPT THROUGH `tee` INTO THE COMMITTED `out_s*.txt`**, so the one
command an ordinary reader would reach for to check this decision **destroys the dated readings
the decision rests on** — and it does it silently, leaving three modified files that look like an
edit somebody meant. mg-188d did exactly that while writing this section and caught it in
`git status`, which is the whole of the defence; nothing warns. That is this section's own subject
committed by the instruction telling you how to check this section, and it is kept here rather
than quietly corrected in the draft. (It is also a second `| tee`: the exit code `run_all.sh`
returns is `tee`'s, the defect `mg-9bc2` records fixing in its own runner. Both are left standing —
repairing another ticket's runner is not mg-188d's to do, and `set -e` on line 3 means the first
non-zero script stops the run, so the staleness verdict above does not depend on it.)

**This section deliberately quotes NO swept spelling and NO count from `s1`'s by-file table**, so
that adding it changes neither the census it reports on nor `s2`'s classification — a note about
a stale count that moved the count would be this file's own subject wearing a footnote. Verified:
`README.md`'s own form-hits are unchanged by this edit.
