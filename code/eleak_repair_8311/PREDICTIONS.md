# mg-8311 — PREDICTIONS for the `lib2de0.E_leak` defect, its ruling, and its consequences

**Committed before any script of this instrument exists.** `git log --diff-filter=A` on
this directory will show this file landing before `r1_witness.py`, `r2_divergence.py`,
`r3_ruling.py`, `r4_consequences.py`, or any repair to `lib2de0.py`.

The ticket (mg-8311) hands me a defect found by p76b2 and explicitly *not* repaired by it:
`lib2de0.E_leak(A)` computes `|A| − |A ∩ set(p[:|A|])|` — the first `|A|` **positions** —
rather than the positions **indexed by** `A`. `phi_star()` calls it on every subset. The
ticket's own figures are **8178 of 11316** diverging pairs at `n ≤ 5` and a 2-chain witness.
**The ticket instructs me not to take those numbers from its body.** So they are not
predictions here either — P1 below is a prediction that *my own* recount lands on 8178, and
it can lose.

---

## 0. HAND MEASUREMENTS ALREADY MADE — disclosed, not laundered into predictions

Everything in this section was measured or derived **by hand / by one-liner before any
script of this instrument existed**, and is therefore **not** predictive. It is here so
that no reader mistakes a thing I already knew for a thing I forecast. Six of the eight
below constrain the consequence assessment so tightly that the honest scoring of P5–P7 is
"reproduction", not "hit".

- **H1 — the witness reproduces, by hand, first.** 2-chain `0 < 1`, the single linear
  extension `(0,1)`, `A = {1}`. Position-image `σ(A) = {p[1]} = {1}` → `|A∖σ(A)| = 0`.
  `lib2de0`'s `set(p[:1]) = {0}` → `1`. **The ticket's smallest witness is real.** Measured
  with a 6-line `python3 -c` before this file was written. The ticket said to stop and
  report if it did not reproduce; it reproduced, so I proceed.

- **H2 — the two natural readings of `σ(A)` agree, so the ruling is a two-way choice and
  not a three-way one.** `|A∖σ(A)| = |A∖σ⁻¹(A)|` for every `σ` and `A`, because
  `|A ∩ σ(A)| = |σ⁻¹(A) ∩ A|` (apply the bijection `σ⁻¹` to both sides of the
  intersection). Checked at the witness: both give `0`. So "image of a position set" and
  "image of an element set" are **the same number**, and `set(p[:|A|])` is neither. This is
  p76b2's observation; I re-derived the proof rather than citing it.

- **H3 — `K_k` and therefore every `Δ₁(A_k)` figure of mg-2de0 is UNTOUCHED, by
  construction.** `A_k = {0,…,k−1}`, so "the positions indexed by `A_k`" *is* "the first `k`
  positions". `lib2de0.K_k` is correct, and `delta_1_prefix` routes through `E_K`, not
  `E_leak`. Read from source. The defect is confined to `phi` / `phi_star`.

- **H4 — the convention BREAKS Lemma 3.2 at the witness.** mg-76b2's Lemma 3.2 is
  `|A∖σ(A)| = |Aᶜ∖σ(Aᶜ)|`, i.e. `Φ_P` is a function of the *cut*, not the *side*. At the
  2-chain with `A = {1}`, `Aᶜ = {0}`: the convention gives `1` on one side and `0` on the
  other. Hand-computed. **This, not "the definition is the definition", is the substance of
  the ruling I expect to make.**

- **H5 — at the ANTICHAIN the two conventions COINCIDE, exactly, at every cut.** Over all
  `n!` permutations both `σ(A)` and `set(p[:a])` are uniform random `a`-subsets, so
  `E|A ∩ ·| = a²/n` either way and both leaks equal `a(n−a)/n`. Hand-derived. So mg-2de0's
  `A3.5` (`Φ* = min over prefixes at the antichain`, `0/6`) and its `1/2` / `2/3` / `√2`
  arithmetic **cannot move**, and neither can `selftest` `S7`'s two antichain drills.

- **H6 — `Φ_P(A) ≤ 1` holds under BOTH conventions, provably.** Under the convention,
  `tot = |A∖P|` with `P = set(p[:|A|])` and `|P| = |A|`, so `|A∖P| = |P∖A| ≤ n−|A|`, and
  trivially `≤ |A|`; hence `tot ≤ min(|A|,|Aᶜ|)`. Hand-derived. So `P9`'s **first** half
  cannot move.

- **H7 — `Φ* ≤ min_k Δ₁(A_k)` holds under BOTH conventions, structurally.** `Φ*` is a
  minimum over a family containing the prefixes, and by H3 the two conventions agree on
  prefixes. Hand-derived. So `P9`'s **second** half cannot move either.

- **H8 — the population behind `11316` is arithmetic I already did.** mg-2de0's `A3`
  states `all 40 labelled n=4` and `all 357 labelled n=5`. With `2^n−2` cuts:
  `40·14 = 560`, `357·30 = 10710`, and `11316 − 560 − 10710 = 46 = 2·2 + 7·6`. So the
  ticket's population is `all_posets(n)` for `n = 2..5` with poset counts `2, 7, 40, 357`,
  and `7` at `n=3` is the 8 up-closed pair-sets minus the one non-transitive
  `{(0,1),(1,2)}`. Deduced by hand. I will still re-derive the counts from my own
  enumerator; a matching total is then a real check, but it is not a *forecast*.

- **H9 — the call sites are grep'd, not guessed.** `E_leak` is reached only via `phi` and
  `phi_star`, which appear at `a3_nonvacuity.py:84,136,160,162` and
  `selftest2de0.py:139,141,144,145,148`. `a1`, `a2`, `a4`, `a5` never compute `Φ`;
  `a4_requirements.py` mentions `Φ*` in **prose only**.

---

## 1. PREDICTIONS

| # | prediction | conf. |
|---|---|---|
| **P1** | My own independent recount — my own poset enumerator, my own leak functions, no import of `lib2de0` and no import of `lib76b2` — lands on **exactly 8178 of 11316** diverging `(poset, cut)` pairs for `n = 2..5`. | 80% |
| **P2** | The per-`n` poset counts come out `2, 7, 40, 357` (H8's hand arithmetic confirmed by machine), so the `11316` denominator is reproduced and not merely matched by luck. | 90% |
| **P3** | **The ruling goes to the DEFINITION.** I will find the convention is not load-bearing anywhere, and the reason I give will be H4 (the convention is not a function of the cut, so it is not a conductance) plus the quadratic-form identity, **not** "the definition is the definition". | 95% |
| **P4** | The quadratic-form identity `⟨1_A,(I−S_P)1_A⟩ = E|A∖σ(A)|` — re-derived by me, with `S_P` built by me from the transport matrix, not taken from `lib76b2` — holds for the definition with **0** exceptions and **fails** for the convention on **> 2000** of the 11316 pairs. | 85% |
| **P5** | `P9`'s first half does not move: `Φ_P(A) ≤ 1` on `0 / 12702` under **both** conventions. *(Forced by H6 — score as reproduction, not hit.)* | 97% |
| **P6** | `P9`'s second half does not move: `Φ* ≤ min_k Δ₁(A_k)` on `0 / 431` under **both** conventions. *(Forced by H7 — score as reproduction.)* | 97% |
| **P7** | `A3.5` does not move: `Φ* = min over prefixes at the antichain`, `0 / 6`, unchanged. *(Forced by H5 — score as reproduction.)* | 98% |
| **P8** | **`A3.4`'s published `strictly smaller on 65 of 431` DOES move.** This is the figure I expect to have to announce loudly. | 75% |
| **P9** | And it moves **UP** (more than 65 posets have `Φ* <` prefix minimum after repair), because I predict the convention **over**-charges: `E_leak_convention(A) ≥ E_leak_definition(A)` pointwise on all 11316 pairs, with 0 exceptions. | 70% |
| **P10** | The number of the 431 posets whose `Φ*` value itself changes lands in **[150, 350]**. | 50% |
| **P11** | `mg-2de0`'s three headline *verdicts* on Priority 2 — `2/3` confirmed as the repaired bound, `√2` confirmed and vacuous, the comparison conservative in the direct route's favour — all **survive** the repair unchanged. The defect moves a count, not a conclusion. | 90% |
| **P12** | No document **outside** `code/direct_prefix_audit_2de0/` and `docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md` carries a figure that moves. Specifically `STATE.md` carries **no** `Φ*` number sourced from mg-2de0. | 85% |
| **P13** | `run_all.sh` re-runs green (`A3 TOTAL BAD: 0`, selftest all-ok) after the repair, on the first attempt after the `65` drill is retargeted. | 70% |

---

## 2. MY TWO MOST LIKELY ERRORS, FILED IN ADVANCE

- **P14 — the prefix/interval slip.** H3 and H7 rest on "the two conventions agree on
  prefixes". What is actually true is narrower: they agree when `A = {0,…,a−1}`, a prefix
  **of the reference order `e`**. They do **not** agree on suffixes, on general intervals,
  or on prefixes **of `σ`**. My most likely error is stating the wide version somewhere —
  in a docstring, in the audit document, or in the ruling — and thereby licensing a
  conclusion the measurement does not carry. I bet **35%** I commit this at least once and
  have to catch it.

- **P15 — reporting a moved function as a moved verdict.** This lineage has twice conflated
  currencies (mg-345e P8; mg-76b2 P14). The neighbouring error here is a *scoring* one: the
  underlying function `E_leak` changes on 72% of inputs, and the temptation is to announce
  `P9 REFUTED` or "mg-2de0's non-vacuity result is wrong" on the strength of that. H5–H7
  say the opposite: the verdicts are structurally robust and it is a **count** that moves.
  I bet **30%** that my first draft of the finding overstates the blast radius, and I am
  committing in advance to the discipline that **"the instrument was wrong" and "the
  published conclusion was wrong" are two claims needing two separate measurements.**

---

## 3. WHAT I AM NOT DOING

Declared in advance so that absence is not read as oversight:

- **I will not touch `code/c3_prefix_capture_76b2/` or `lib76b2.py`.** The ticket forbids
  it and `C₃ = 1` does not rest on `lib2de0`. My re-derivations are written fresh in this
  directory; where I check the same identity mg-76b2 checked, that is a *second*
  instrument, not a re-run of theirs.
- **I will not re-derive the Cheeger argument and I will not attempt L2.** Instructed.
- **I will not compute `λ_std`.** `S_P` appears here only as a matrix whose quadratic form
  is compared against a combinatorial count; no eigenvalue is taken.
- **`n = 6` is a stretch goal, not a promise.** `5230` posets × `62` cuts × up to `720`
  linear extensions may not finish in a reasonable time. If it does not, the transcript
  will say where it stopped rather than omitting it.
