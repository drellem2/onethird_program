# `code/lstar_landing_8d63/` — the landing instrument for mg-8d63

**One script, one question:** at which `n` does `ρ·Δ_P > 1` first occur over primitive
posets? The corpus has said **`n = 10`** (mg-c50b §4 — correctly labelled **FAMILY**) and
then **`n = 6`** (mg-789d §4). Measured here, exhaustively, the answer is **`n = 5`**, at
**6 of 275** primitive posets, `max ρΔ = 1.027118`.

> **`mg-5cba` GOT THERE FIRST AND WENT FURTHER, AND THAT IS SAID HERE RATHER THAN BURIED.**
> Its independent audit of `mg-789d` (`5c0849a`) certifies all six `n = 5` witnesses in
> **exact rationals** and certifies `μ_pref·Δ ≤ γ` at **every** primitive poset of `n = 3`
> and `n = 4` — so `n = 5` is *exactly* the onset, which a float sweep cannot establish.
> This directory is a **third** independent reproduction, on `mg-789d`'s own instrument,
> agreeing to six places. Its own contributions are the **cross-thread provenance** below
> (which `mg-5cba` does not report) and **control C3**.

```
python3 s1_onset.py        # ~11 s;  exit 0 = all four arms pass
```

## Why a landing ticket runs its own measurement

The correction mg-8d63 was sent to land is *"`n = 10` → `n = 6`"*. Carrying that by
quotation would have propagated it. `s1_onset.py` measures the column instead, and the
result is **neither** of the two numbers in the ticket.

## What it does not do

It does **not** touch `(L*)`. `(L*)`'s hypothesis is that **`(F)` fails**, and `(F)` fails
at no poset with `n ≤ 6`, so nothing in this directory bears on whether `(L*)` is true,
false, or open at any `n`. The onset of `ρΔ > 1` and the refutation of `(L*)` are two
different facts and this instrument measures only the first. `n ≥ 7` is not swept — an
onset established at `n = 5` cannot be moved by a larger `n`.

## The four arms, and what each could have caught

| arm | what it checks | why it is here |
|---|---|---|
| **S1.1** | `max ρΔ` over every primitive poset at `n = 2..6`, exhaustive | the measurement itself |
| **C1** | mg-789d's own published `n = 6` maximum `1.15672` | if this disagreed, the instrument — not the corpus — would be wrong |
| **C2** | mg-c50b's FAMILY statement: chain(`n−1`)+point crosses 1 at `n = 10`, reaches `1.078` at `n = 16` | **that sentence is TRUE and this landing must not read as striking it.** It reproduces (`0.98596` at `n=9`, `1.00636` at `n=10`, `1.07794` at `n=16`) |
| **C3** | **this script's own floor** | the mirror defect — see below |

**C3 is the arm that matters.** The defect being corrected is *a smallest-`n`-looked-at
published as a smallest-`n`-it-happens-at*. This script's first draft started its sweep at
`n = 3` and would have committed exactly that defect while reporting the correction to it:
`n = 2` has a primitive poset. C3 runs the sweep down to `n = 2` (`ρΔ = 0.5`) and **refuses**
`n = 1` rather than skipping it — `LE = 1`, so `γ = 0` and `ρ = μ_pref/γ` does not exist
there. Without C3 the `n = 5` claim would be a floor artefact wearing an onset's clothes.

## Independent agreement, and it predates both published numbers

The column measured here already existed in this corpus under another name. mg-28ff's cell
**`V10` IS `ρΔ_P`** ([`docs/OneThird-L2-Conditionality-mg-28ff.md:279`](../../docs/OneThird-L2-Conditionality-mg-28ff.md);
mg-29fe's audit table at `:366` spells the identification out), and
[`code/l2_audit_29fe/out_s3_counterfactual.txt`](../l2_audit_29fe/out_s3_counterfactual.txt)
prints the V10 maxima `0.500000 / 0.666667 / 0.904508 / 1.027118 / 1.156724` at `n = 2..6`
and states in as many words that V10 *"first exceeds 1 at n = 5, at 6 of 275 primitive
posets at n=5"*. **Every digit agrees with this run**, on an instrument (`lib789d`) that
shares no code with mg-29fe's.

So the datum refuting the `n = 10` reading was **already in the corpus, measured and
committed, before either published onset statement was written** — in a document that
nobody had reason to read as being about `(L*)`. That is the transferable finding here, and
it is worth more than the corrected integer: **the same scalar was tracked under two names
in two threads, and neither thread could see the other's measurement.**

*mg-8d63. Instrument imports `code/lstar_789d/lib789d.py` and adds no mathematics of its
own — deliberately, so that a disagreement with mg-789d would be a disagreement about the
sweep and not about the definitions.*
