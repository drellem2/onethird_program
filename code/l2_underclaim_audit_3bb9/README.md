# `l2_underclaim_audit_3bb9` — mg-3bb9's instrument

The audit instrument for **mg-3bb9**, the independent audit of **mg-b58d**'s seven repairs
(landed at `b45aad8` on `docs/OneThird-L2-Conditionality-mg-28ff.md`).

`mg-b58d` disclosed that it **re-ran no instrument**: every exhaustive figure it landed was
quoted from `mg-51f4`'s and `mg-29fe`'s output files, and `onethird_program` has **no quality
gates**, so nothing checked the landed text. This instrument exists to re-measure the
largest of those claims rather than re-read it.

## What it decides

| script | what it decides |
|---|---|
| `a1_reversal.py` | the **UNDER-CLAIM reversal** (repair 6): the population, the cone identity, `ρ ≥ 1`, `V00 = ρ` **from the raw bound rather than the closed form**, the four variants' failure counts and maxima at `n ≤ 6`, and an **L2 census that does not use `μ_pref`** |
| `a2_n4_exact.py` | *"it moves the first failure from `n = 5` to `n = 4`"*, at `n = 4`, with **no float on the verdict path** |
| `a3_n7_population_label.py` | repair 3's own `n = 7` population labels, against `lib28ff`'s own generators |

`lib3bb9.py` is written from the definitions as the document states them (§2, §4, §5) and
from `s3_counterfactual.py`'s docstring. It shares no line of code with `lib28ff.py`,
`lib29fe.py` or `lib51f4.py`. **Disclosed, not laundered:** I read `lib28ff.py`'s module
docstring for `S_P = (T + T^ᵀ)/2` before writing a line — that is a *definition* I could not
have guessed, and every number below is a reproduction only in the sense that it was reached
from those definitions by different code.

## Results (`out_a1_reversal.txt`, `out_a2_n4_exact.txt`, `out_a3_n7_population_label.txt`)

* population `5230 / 4377`, primitive `1 / 4 / 27 / 275 / 4070` — matches
* `V11 0/0/0/0/0`, `V10 0/0/0/6/192`, `V01 0/0/0/0/1`, `V00 0/0/10/166/3164` — matches
  `mg-29fe`'s `out_s3_counterfactual.txt` exactly, sum `3340`
* maxima at `n = 2..6` agree to **six decimals** in all four columns
  (`0.943151 / 1.156724 / 1.028754 / 1.217605` at `n = 6`)
* `ρ ≥ 1` at every one of the 4377, minimum exactly `1.000000000000`
* `V00 = ρ` is an **identity**: the raw bound `2R/(2(1−λ))` and the closed form `ρ` agree at
  **every** primitive poset, 0 disagreements — likewise for the other three cells
* the **independent** L2 census (does the top standard eigenspace meet the monotone cone?)
  is `0 / 0 / 10 / 166 / 3164 = 3340` and agrees with the `V00` column at **every `n`**
* `n = 4` exactly: **10** certified `ρ > 1`, **17** certified `ρ = 1` to `2⁻²⁰`, **0**
  undecided; `V10`, `V01`, `V11` at **0**

## Two defects of my own, both kept

* **D1 — a control that fired against me first, and it was mine that was broken.** The whole
  point of the L2-by-eigenspace column is that `mg-29fe`'s `s3` decides "L2 fails" as
  `rlo > 1`, which is *the same predicate as* `V00 > 1`, so its agreement is a tautology. My
  replacement disagreed with the `μ_pref` test at **1 poset of 275** at `n = 5` and I nearly
  published that as a crack in the identity. It was the **antichain**, where the whole space
  is the eigenspace: my search sampled directions in only 3 of the `d` dimensions and missed
  `e₁`. Rebuilt as alternating projection with a **constructive witness** (a "yes" exhibits a
  nonnegative vector and checks it; only a "no" rests on the search), after which the two
  censuses agree at all 4377.
* **D2 — `simplex_min` skipped singular faces**, including a vertex with `M_ii = 0`, which
  would have let a *non*-strictly-copositive matrix pass and inflated `μ_pref`'s lower
  bracket. Vertices are now always evaluated. `a2`'s 0 undecided posets is the arm that would
  have caught the residue.

## Not done

**I did not re-run `mg-51f4`'s exhaustive `n = 7`.** `0.340719`, `1.018707`, `1.297074`,
`168 of 86278`, `96428` are checked here only as **faithful copies** of
`code/sweep_loss_51f4/out_s3_n7.txt` — verified as copies, not as truths.
