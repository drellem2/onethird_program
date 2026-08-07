# `libweak_audit_c4f5` — the instrument behind `docs/OneThird-LIBweak-mg-c4f5-IndependentAudit.md`

Independent audit of mg-c3ca (`docs/OneThird-LIBweak-mg-c3ca.md`, commit `81214a9`).

**Nothing here imports `lib_c3ca`.** The poset representation, the linear-extension counting, the
pair probabilities and the eigensolver are all written from scratch. The one deliberate overlap is
the **population** (naturally labelled posets on `[n]`) — sharing the population is the point of a
reproduction; sharing the parser would defeat it. That the two agree is checkable: this instrument
reproduces mg-c3ca's own pair-population sizes `11 / 130 / 1 984 / 41 044` line for line.

Exact `Fraction`/integer arithmetic throughout. **One tolerance in the whole audit** — `1e-9`, at
the eigenvalue step, because `λ_std` needs an eigenvalue — and it is declared at its call site.
No sampling. No randomness.

## Run

```
python3 selftest_c4f5.py        # 68 checks, exit 0        -> out_selftest_c4f5.txt
python3 a1_premise.py 7         # ~30 min (the L-sweep)    -> out_a1_premise.txt
python3 a2_maths.py 7           #                          -> out_a2_maths.txt
python3 a3_construct.py 7       #                          -> out_a3_construct.txt
python3 a4_census.py 7          #                          -> out_a4_census.txt
python3 a5_window.py 7          # ~10 min                  -> out_a5_window.txt
python3 a6_calibration.py       #                          -> out_a6_calibration.txt
./a7_history.sh                 #                          -> out_a7_history.txt
```

## Population and grain, repeated at every printed count

**POPULATION** — every *naturally labelled* poset on `[n]`: every transitively closed subset of
`{(i,j) : i<j}`. Counts `1, 1, 2, 7, 40, 357, 4824, 96428` (A006455), asserted in `selftest` §A
so a wrong population cannot pass silently. This is **not** the labelled-poset count
(`1,1,3,19,219,4231,130023`) and the two are routinely confused.
**GRAIN** — one poset (`a1`–`a4`); one incomparable pair (`a5`); one `mg` item (`a7`).

`n = 7` is reachable here and was not in `libweak_c3ca` because everything runs off an
**order-ideal DP** rather than an enumeration of `L(P)`: for each ideal `S`, `nin[S]·nout[S∪{x}]`
counts the linear extensions placing `x` at position `|S|`, which gives positions, pair orders and
the footrule with no linear extension ever written down.

## What each pass is for, and what it found

| pass | question | answer |
|---|---|---|
| `selftest` | can this instrument be trusted, and can it report both answers? | **68/68.** DP checked against brute-force enumeration on every poset `n ≤ 5` (`e(P)`, every `q_{xy}`, the footrule — max error `0`). Eigensolver drilled on four matrices with hand-known spectra. Ledger row 1 (`λ_std = 1 ⟺ not primitive`) used as a control: 397 posets, 0 mismatches. §G drills the `δ` detector on a **constructed frozen table** so a null in `a4` is a measurement. Every check that could pass vacuously is paired with a NON-VACUITY assertion. |
| `a1_premise` | does `(LIB-weak) ⟹ λ_std → 1`? is `λ_std` even well defined? | master bound: **0 violations over 101 658 posets, `n ≤ 7`**, both forms. And `λ_std` **moves with the reference linear extension** — 4 069 of 4 824 at `n = 6`, spread `1/3`. |
| `a2_maths` | are §1's iff and §4's Prop 4.1 right? | both **CONFIRMED**, 0 violations. Plus: Prop 4.1 is **vacuous for `ε ≥ 1/(2e²) ≈ 0.068`**, and freezing gives only `ε < 1/6`. |
| `a3_construct` | build the `Θ(n)`-elements-of-`Θ(n)`-mass object §3's supporting sentence argues against | **built, exactly**: `C_p ⊔ A_q`, `E_maj/n² = 0.125`, `δ = 1/2`. Plus the `δ`-ceiling **frontier**, a measurement §3 wanted and did not take. |
| `a4_census` | reproduce every printed figure of §6, then add `n = 7` | **11 of 11 reproduce exactly.** The fifth point breaks two four-point reads: primitive min `δ` **rises** (`0.357 → 0.359`), and `E_maj/n²` is not monotone in either population. |
| `a5_window` | audit §5's own refutation probe | **the largest finding.** Reproduces `16/351/8088` exactly under the predicate `p3_window.py` evaluates, and finds **0** counterexamples to the inequality the document names, over 1 168 036 pairs at `n ≤ 7`. |
| `a6_calibration` | the `(LIB-weak)`/`(LIB-const)` gap; `Δ_AT` drift; bound words | `~50` vs the parent's `~5×10³`; **no `N₀` exists**; **no `Δ_AT` drift** (1 occurrence, in "what I did not do"). |
| `a7_history` | is (LIB-weak) really "never attacked by any arc"? | **YES** — 0 of the 4 pre-c3ca items among 2 360 had it as a deliverable. Population printed before the answer. |

## Reach caveat

`n ≤ 7`. A `Θ(n)`-mobility configuration in the asymptotic sense cannot appear at this size. None
of these numbers is evidence about the limit; they are evidence about the boundary, and the audit
document says so where it uses them. `a3`'s explicit families run to `n = 20` and are exact, but
they are constructions, not a census.

## Recorded defects of this instrument

1. **My first positive control asserted `δ(V) = 1/3` for `V = {0<1, 0<2}`, matching mg-c3ca's
   README by NAME.** `V` has `δ = 1/2`; the `δ = 1/3` three-element object is `C_2 ⊔ C_1`. **The
   code was right and my assertion was wrong** — the same shape as mg-c3ca's own recorded defect 1,
   committed by its auditor. Kept in place at `selftest` §D1 with the diagnosis.
2. **I asserted mg-c3ca's `W_m` hand formula against `E[inv_L]`, the natural-labelling inversion
   count.** It is the formula for `E_maj = E[inv_e]`. Both numbers are right and they are
   different numbers; the assertion conflated two reference orders. Both are now asserted
   separately — which turned out to be the distinction the whole of §7 of the audit rests on, so
   the defect found a finding.
3. **`a4` §R6 accused two published figures of contradicting each other, in a header written
   BEFORE the measurement.** They do not: they are one quantity over two populations, each
   correctly scoped where it is printed. Header replaced by the resolution, not deleted.
4. **Having repaired defect 3 I then wrote "the primitive sequence is monotone" — and the `n = 7`
   value one row below refutes it** (`0.0456 → 0.0481`). Written at `n ≤ 6`, refuted by the same
   file's next row. Kept.
5. **`a6` §C2 was a search loop capped at `n = 10⁶` that found nothing and PRINTED `None` as
   though `None` were the answer.** A cap reported as a measurement — inside the section whose
   entire subject is a predicate reported as a different predicate. Replaced by the closed form,
   which is why the number is now `2³⁰⁰`.
