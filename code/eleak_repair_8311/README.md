# `code/eleak_repair_8311/` — the `lib2de0.E_leak` ruling and repair (mg-8311)

Finding document: [`docs/OneThird-Eleak-Repair-mg-8311.md`](../../docs/OneThird-Eleak-Repair-mg-8311.md).
Predictions, committed **before any script here existed**: [`PREDICTIONS.md`](PREDICTIONS.md).

```
./run_all.sh          # ~55s: r1 4s, r2 20s, r3 25s, r4 5s. Writes every transcript IN FULL.
```

## What this is

mg-76b2 found, while proving `C₃ = 1`, that `lib2de0.E_leak(A)` computes
`|A| − |A ∩ set(p[:|A|])|` — the first `|A|` **positions** — where `Δ₁(A)` needs the positions
**indexed by** `A`, and that `phi_star()` calls it on every subset. It judged that outside its
own scope and offered it rather than silently repairing another instrument. This is that item.

**Headline: the defect is real, the definition wins, and exactly one published figure moves —
`strict on 65 of 431` is `16 of 431`.** No conclusion of mg-2de0 changes. The instrument was
wrong on 71.8% of its own inputs and its published verdicts were right anyway; the finding
document measures those two things separately, which is the whole discipline of the ticket.

## The four sections

| script | what it settles |
|---|---|
| `r1_witness.py` | The 2-chain witness, reproduced **before** any repair, at full grain. Then the two symmetries: `\|A∖σ(A)\| = \|A∖σ⁻¹(A)\|` (0 / 695482) so the ruling is a two-way choice; and `\|A∖σ(A)\| = \|Aᶜ∖σ(Aᶜ)\|`, which the definition satisfies (0 / 683656) and the convention violates (457132 / 683656) — **the convention is not a conductance**. Plus the narrow prefix agreement and its suffix guard. |
| `r2_divergence.py` | The divergence count, **re-derived**. The ticket's `8178 of 11316` is not an input to this script; landing on it was `PREDICTIONS.md` P1 and it could have lost. Carries to `n = 6` and cross-checks the population against mg-76b2's `5230` / `310404`. |
| `r3_ruling.py` | The ruling. `⟨1_A,(I−S_P)1_A⟩ = E\|A∖σ(A)\|` on 310404 pairs for the definition and never for the convention. An **AST** census of call sites (not a grep — mg-4d3b recorded a census that read its own prose as code). The load-bearing test the ticket asks for. Then the ruling, stated explicitly before any code changed. |
| `r4_consequences.py` | The deliverable. Every `Φ` figure mg-2de0 published, in two columns, on mg-2de0's own 431 posets / 12702 cuts. |

`lib8311.py` imports **neither `lib2de0` nor `lib76b2`**: own poset enumerator (grown-and-closed,
not masked-and-filtered), own linear extensions, own `S_P`, and **both** leak conventions
implemented side by side with neither privileged by the code. `r4` imports `lib2de0` for the
**poset population only** — both its columns are computed by `lib8311`, so it prints the same
before/after table whether the repaired or the defective `E_leak` is on disk.

## What was changed outside this directory

- `code/direct_prefix_audit_2de0/lib2de0.py` — `E_leak` repaired; module docstring now
  distinguishes `σ(A)` from "the first `|A|` positions"; the function's docstring carries the
  defect, the witness, the ruling and the moved figure.
- `code/direct_prefix_audit_2de0/selftest2de0.py` — new **`S7b`**, five drills, **every one on a
  non-prefix cut**. mg-2de0's existing `Φ` drills were all at the antichain, where the two
  readings coincide at every cut — which is exactly why a defect on 71.8% of inputs survived a
  two-sided-closure selftest. 4 of the 5 go RED against the old code (verified by running
  them against it); the 5th is labelled in the transcript as **not a detector**.
- `code/direct_prefix_audit_2de0/out_*.txt` — regenerated. **`a1`, `a2`, `a4`, `a5` are
  byte-identical**; `a3` changed one line; `selftest` gained `S7b`.
- `code/direct_prefix_audit_2de0/README.md` and
  `docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md` — the moved figure corrected **loudly**,
  with a box naming it rather than a silent replacement.
- `STATE.md` — **deliberately not touched.** It carries no `Φ*` figure from mg-2de0.

## Predictions, scored

`HIT 8 · MISSED 2 · REPRODUCTION 3 · own-error predictions NOT FIRED 2.`
Full scoring table in the finding document §6. The two losses, kept as written:

- **P9 MISSED, both clauses.** I bet 70% the convention only ever over-charges, and inferred
  the repair would lower `Φ*` and raise the strict count. It under-charges on 2122 / 11316
  expectations, and the count went **down**, 65 → 16. Why: the convention over-charges on the
  majority of cuts (6762 of 12702) and under-charges **without exception at the 431 cuts that
  attain the minimum** (0 over, 102 under, 329 equal). `Φ*` is an extremal statistic, so **an
  aggregate error sign is not a bound on an extremum.** That caution is worth more than the
  prediction was.
- **P10 MISSED.** I bet `Φ*` would move on 150–350 of 431. It moved on **65** — and on exactly
  the 65 posets A3.4's figure counts, which is forced once the direction is known.

**P5–P7 are scored REPRODUCTION, not HIT.** All three were proved by hand in `PREDICTIONS.md`
(H5–H7) before this instrument existed, so they were never forecasts. Calling them hits would
inflate the score by three.

## Defects of this instrument, kept on the page

1. **A dead assignment in `r4_consequences.py`** — a name-prefix filter for the `n = 4` posets
   that I replaced on the next line and left in, computing a discarded value. Found by
   re-reading my own source, not by any check. Removed. A filter that looks used and is not is
   how a wrong population gets published.
2. **One of my five new drills is not a detector.** `Φ*(chain n=4) == 0` passes under the old
   convention too (the chain's *prefix* cuts leak 0 either way and `Φ*` is a minimum). Found by
   the control I nearly skipped — running the new drills against the old code. Kept, with a
   note in the transcript so it cannot be miscounted.
3. **`_close()` carries an unreachable guard**, declared rather than trimmed.
4. **`r3.3` and `r4` measure the same three assertions on two populations** — redundancy, not
   coverage. `r4`'s is the one that counts.

## Not done

`STATE.md` untouched (no figure to correct). mg-76b2's instrument and `C₃ = 1` untouched —
`lib76b2` is never imported, and the identity check here is a **second** instrument on the same
population, confirming mg-76b2's population and identity, not its conclusion. The Cheeger
argument is not re-derived and `L2` is not attempted. `λ_std` is never computed. `n ≥ 7` not
measured. mg-2de0's pre-existing `S1`–`S8` drills not otherwise re-audited.
