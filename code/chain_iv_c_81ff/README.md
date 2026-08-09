# `code/chain_iv_c_81ff/` — mg-81ff's instrument

**Question.** Is `Op-Form §4.3`'s literal capture fraction `c` establishable above its
threshold (`> 1 − ε_leak = 0.80` in prose, `≥ (1−ε_leak)/(1−ε_spec) = 40/49 = 0.8163`
self-consistently), so that chain (IV) — which never spends the Cheeger square — becomes
usable?

**Deliverable.** [`docs/OneThird-ChainIV-CaptureFraction-mg-81ff.md`](../../docs/OneThird-ChainIV-CaptureFraction-mg-81ff.md)

**Answer, in one line.** Refuted on the full population by an explicit family, which
settles nothing because every member is 23×–33× outside the regime; supported at
`c = 0.9999` on the one poset shape this instrument exhibits inside the regime; and **`c`
is not an independent unknown at all — it is chain (II)'s `C₃^gap` in another currency,
with an algebraically equal demand.**

> **⚠️ ERRATA (`mg-b3ab`), after `mg-00b3`'s independent audit landed at `8eec6d2`.** Four
> statements in this instrument's transcripts were re-scoped in place; every erratum is
> printed **in** the transcript, at the line it corrects, and each begins `*** ERRATUM`.
>
> 1. **`s2 (R3)`'s "A SECOND FAMILY" is not a second family.** `N` and `N'` are the same
>    poset under two labellings — `K_{a,a}` minus one relation, and `Aut(K_{a,a})` is
>    transitive on its `a²` relations. `s2 (R3)` now **exhibits an explicit isomorphism at
>    every `n = 6..16` and asserts it**, with a live negative arm (a two-relation deletion,
>    which must and does fail the same test).
> 2. **`s2 (R3)`'s `N'` table dropped `min_k Q_k`** — the one column `§1.2` shows decides
>    whether chain (IV) closes. Restored, together with the `n = 6` row, and the equality
>    with `N`'s column is now **asserted** rather than left to the eye. *This omission is
>    why (1) was not visible on its face.*
> 3. **`s3 (I3)`'s "the premise survives on the only posets anyone has exhibited inside the
>    regime" is now FALSE** — that set has grown. The staircase `S_n` is primitive and
>    in-regime from `n = 12` with `c = 0.9258259`, `ε_dem^(IV) = 0.1359` and slack `2.2`,
>    against this instrument's family's `0.9999` and `52`.
> 4. **`s2 (R1)`'s "monotonically" and "the fall is the gap, not `n`" are both over-stated.**
>    The monotonicity is a property of the chosen partition, and `(R4)` of this same script
>    measures `min c` falling with `n` at a fixed gap cap.
>
> `s3 (I1)`'s hedge that a rising `C₃^gap` is *"a direction in both currencies and a verdict
> in neither"* is re-scoped to **its own rows** — `C₃^gap` is now measured in regime, and
> `s3 (I5)` carries three such rows. **No figure computed by this instrument was withdrawn**;
> `s0` and `s1` are untouched. The staircase figures are `mg-00b3`'s, cited and labelled.

## Run

```sh
python3 s0_selftest.py    # controls — nothing below is worth reading until this passes
python3 s1_minc.py        # the sequencing directive: mg-76b2's min c, checked and extended
python3 s2_regime.py      # the scope: c stratified by gap; the in-regime families
python3 s3_identity.py    # c <-> C_3^gap, and the demand identity
```

`s1` ~4 min, `s2` ~4 min, `s3` ~4 min, `s0` ~6 min (the `n!` cross-check at `n ≤ 6` and the
`n = 7` stratification dominate). Pure Python 3, no third-party packages — there is no
`numpy` on this machine and the eigenroutine is hand-rolled for that reason.

## Files

| file | what it is |
|---|---|
| `lib81ff.py` | posets, down-set DP transport, exact `Q_k`, **exact `λ₂` by Sylvester's criterion**, float Jacobi (search only) |
| `s0_selftest.py` | eight controls, `(A)`–`(H)` |
| `s1_minc.py` | `min c` at `n = 3..7`; the minimiser family `D_k` to `n = 16`, exactly |
| `s2_regime.py` | gap stratification; envelopes; the in-regime families `N(n)`, `N'(n)` |
| `s3_identity.py` | the `c ↔ C₃^gap` identity; the demand identity; a negative control |
| `out_*.txt` | transcripts, committed |

## Design commitments

**No shared code.** This ticket's first job is to *check* `mg-76b2`'s numbers, and an
instrument inheriting `lib76b2` could only re-print them. Different enumeration (by
extension, not by masking `2^C(n,2)`), different transport (down-set DP, not `n!`),
different eigenroutine, different verdict path.

**No float on any verdict path.** `min_k Q_k` is exact `Fraction` always. `λ₂` is decided
by `λ₂ > q ⟺ A − qG` positive definite (exact symmetric elimination on the rational basis
`b_i = e_i − e_{n−1}` of `H`), bisected to an exact rational bracket. `math.sqrt` and the
Jacobi routine appear only in `float_c`, which finds candidates; every figure quoted is
restated on the bracket. `s0 (F)` checks the bracket contains the Jacobi value at all 5228
posets `n ≤ 6` and includes a negative control that a wrong `q` is rejected.

**Every count names its population at the print site.**

## Two defects of my own, both caught by controls, both kept in the history

1. **The central identity was written backwards in this file's own module docstring** —
   `c = (1−minQ)/λ₂` where the truth is `(1−minQ)/(1−λ₂)` — and `c_bracket` was written
   from the prose and inherited it, while `float_c` was written from the definition and
   was right. `s0 (E)` is the control that pins it now: `ρ(A_k)` computed from `M`
   directly against `1 − Q_k` computed from the Laplacian, 25 682 `(poset, k)` pairs, 0
   mismatches. Written down because the ticket's whole subject is a currency error and
   this instrument made one in its first draft.

2. **`s0 (C)`'s mutation control was built wrong and the first run said so.** I wrote it to
   assert that the broken down-set peel — `down[i] ⊆ S\{i}`, which is true of *every* `i`
   in a down-set, minimal ones included — gives **wrong numbers**. It does not: the bogus
   states contribute nothing and the mutant is numerically correct at every poset tested.
   So the control was rebuilt to assert **both** halves, the numbers agreeing **and** the
   state count exceeding the down-set lattice (12 841 peels offered, 8 460 landing, 34.1%
   bogus). That is independently the design `mg-9461`'s own `s0 (C)` records, arrived at
   by making the same mistake.

The first version of the DP crashed on its first call (`KeyError`) for the same reason,
which is the only cheap luck in this directory.

## No `PREDICTIONS.md`, and why

This corpus's convention is to commit predictions before the instrument exists. **I did
not, and back-dating one now would be a fabrication rather than a record.** The exposure a
predictions file would have disclosed, stated instead:

- The ticket body printed `mg-76b2`'s four `min c` figures (`0.750, 0.618, 0.536, 0.453`),
  **both** thresholds on `c`, chain (IV)'s formula `ε_dem = 1 − (1−ε_leak)/c` and its
  `→ 0.20` limit **verbatim**. So `s1`'s reproduction of `n = 3..6` is a **check**, not a
  discovery, and `s0 (H)` labels it as a control for that reason.
- `mg-9461`'s landed document and `STATE.md:164`/`:169` were read before any code was
  written, which is where the four-chain table and `mg-94c3`'s `1023/1032` come from.
- **What is not pre-answered, and is therefore this instrument's own:** `n = 7` (`min c`
  `0.412700`, `max C₃^gap` `3.075`, `DISC ⟺ CUT` on 96 428 posets), the minimiser family
  `D_k` and its exact values to `n = 16`, the gap stratification, the two in-regime
  families and the fact that the budget is reachable at all, and the `c ↔ C₃^gap` identity
  with the equal-demand corollary.

## Not done

No `n = 8` sweep (~2.8M posets; the box was under load-management instruction). No proof
that `c(D_k) → 0`. No attempt at L2, L3, L4, `C₃` or the growth bound. `STATE.md` untouched.
