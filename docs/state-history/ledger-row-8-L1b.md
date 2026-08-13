# Full ledger row 8 — L1b, the wall

Per-row history for `STATE.md` § *Full ledger*, row 8.
Split out of the ledger cell by **mg-bdb0, 2026-08-13 — landing A of the two-landing
protocol** (`code/rendered_twin_pin_9bc2/twin_pin.py` section 8, shipped by mg-1344).

Every passage below was **moved verbatim** out of that cell: each is a literal slice of the
cell as it stood at `092a508`, and the row keeps the rest of that cell, also verbatim, with
only the punctuation seams a removal leaves. Nothing was rewritten, condensed, summarised or
dropped, and no citation was changed. Retained text + the passages below reconstruct the old
cell character for character. The row now asserts current state and points here. See
[`README.md`](README.md) for the convention and for which passages relocate.

## Corrections, retractions, supersessions and mechanism notes

*Why this section exists: a ledger row must not be able to contain a claim and its own
retraction. The row states what is true now; what it used to say, what was struck, and why,
is here. Sections are numbered `H1`, `H2`, … and the row cites them by number.*

### H1 — what this row said until mg-0e8c

*In the row it stood between “…IFORM IN `n` IS NOT WHAT IS OPEN — ONE IS PROVEN” and “.** `ε_sup < 1` is pair-bias, `Op-Form` Claim 6.…”:*

, AND THIS ROW SAID OTHERWISE UNTIL mg-0e8c (on Daniel's challenge, which was RIGHT)

### H2 — the boundary the old phrasing was standing on

*In the row it stood between “… with **equality at the antichain at every `n`**” and “. ⚠️ **KIND OF THE VACUITY: `FP`, `n ≤ 6`** — th…”:*

— so `1` is precisely the smallest constant at which the old phrasing became a universal truth, and the row was standing on that boundary

### H3 — the note that the rest of the cell was unchanged

*In the row it stood between “…l1b_currency_0e8c/`](code/l1b_currency_0e8c/)). ” and “what the architecture consumes, **CONDITIONALLY*…”:*

The rest of this cell is unchanged and states the same two constants:

### H4 — the `η = 0` witness, and why `ATTAINED` was the wrong word (mg-832f Correction 2)

*In the row it stood between “…UM over the frozen class, NOT a maximum in it.**” and “ *(Kind marked at the claim: Claim 3.1's `≤` and…”:*

The `η = 0` witness puts **every pair at exactly `1/3`**, i.e. `δ = 1/3`, i.e. **outside the hypothesis**, so an unqualified `ATTAINED` at `η = 0` is the weaker rendering stated as the stronger one. **Nothing downstream moves** — the supremum is `n/(n+1)`, pair bias cannot go below it, and Claim 6.1 remains not improvable by pair bias — but the word must say which it is, because `ATTAINED` is exactly what makes Claim 6.1 an **equality** rather than a bound awaiting sharpening.

### H5 — mg-c4f5's audit of mg-c3ca — the tally

*In the row it stood between “…e gap is a quantifier, not a constant** (mg-c3ca” and “). The reverse arrows are **UNPROVEN — not merel…”:*

, **audited mg-c4f5 — premise CONFIRMED, 11/11 figures reproduce, 6 corrections**; verdict there is **neither proved nor blocked**

### H6 — the superseded reason for the literature-bound guard (mg-d1a2)

*In the row it stood between “…ta 2026) — **and that discharges nothing here.**” and “ **there is no threshold to exceed.** No `N₀` wo…”:*

The reason is stronger than the one this guard first carried (mg-d1a2: *an unspecified threshold is not a size any number can exceed*, still true):

### H7 — the `η` restored from the parent (mg-832f Correction 2)

*In the row it stood between “…oute below `1` must add a *realizability* fact. ” and “`M_n(η)` is *every pair flipped with probability…”:*

⚠️ **THE `η` IS RESTORED FROM THE PARENT AND IT DECIDES ONE WORD (mg-832f Correction 2).**

### H8 — mg-5ce3's independent re-derivation

*In the row it stood between “…THE CLASS AT ALL** (mg-c4f5 §5.3, landed mg-5ce3” and “). For any candidate `N₀`, `g(n) = n²` below `N₀…”:*

— re-derived independently there

## Supporting record

*`docs/state-history/README.md`'s clause (c): a derivation, construction, enumeration or
numeric evidence supporting a claim the row still states. The claim stayed in the row; the
working is here.*

### S1 — the 82 posets that separate the spectral form from the inversion form

*In the row it stood between “…master bound runs inversions ⟹ spectrum, one way” and “). ⚠️ **A CONSTANT UNIFORM IN `n` IS NOT WHAT IS…”:*

; 82 of the 4,824 posets at `n = 6` satisfy the spectral form at `ε = 1` and fail the inversion form there, mg-0e8c a3/C3

### S2 — `Op-Form` §6.3 in its own words, and the third normalisation

*In the row it stood between “…nd it **discharges the existence form outright**” and “. **AND AT THAT CONSTANT THE SPECTRAL RENDERING …”:*

— `Op-Form` §6.3 says so in its own words: *"**(LIB-const) already holds, with constant 2/3**"*, a **THIRD** normalisation this ledger does not carry (fraction-of-uniform; `(2/3)·E_unif[inv]` in `ε_spec` units **is** `n/(n+1)`, 0 mismatches on exact rationals `n = 3..12`)

### S3 — the vacuity, measured

*In the row it stood between “…at **every** poset with **no hypothesis at all**” and “, with **equality at the antichain at every `n`*…”:*

(`λ_std ≥ 0`, 0 exceptions in exact arithmetic over all 5,230 posets `n ≤ 6`)

### S4 — the reduction behind the vacuity's `FP` kind

*In the row it stood between “…ary. ⚠️ **KIND OF THE VACUITY: `FP`, `n ≤ 6`** —” and “ the **discharge** is not `FP` and needs none of…”:*

the reduction `1 − λ_std ≤ (n − trace T_P)/(n−1)` is algebra for all `n`, its premise `trace T_P ≥ 1` is measured;

### S5 — the density reading reproduces this row's own `n ≥ 100` threshold

*In the row it stood between “…2×10⁻²`, and what is open is the DENSE regime.**” and “ **THE OPEN CONTENT IS THE FACTOR OF ~50 BETWEEN…”:*

That reading reproduces this row's own `n ≥ 100 (primitive)` threshold from the opposite end (primitivity forces `d ≥ 2/n`), so it is not a new number.

### S6 — the two normalisations, and where the factor of 6 comes from

*In the row it stood between “…N TWO NORMALISATIONS, NOT A FACTOR OF 6 APART:**” and “DO NOT READ `1/6` AS A SHARPENING OF THIS `1`, b…”:*

one theorem `E[inv_e] < m/3 ≤ n(n−1)/6`, divided by `(n²−1)/6` here (`ε_spec < n/(n+1) → 1`) and by `n²` there (`ε_c3ca < (n−1)/(6n) → 1/6`, the units `E[inv_e] ≤ ε·n²` of [`OneThird-LIBweak-mg-c3ca.md:172`](docs/OneThird-LIBweak-mg-c3ca.md), already written down as *"Freezing unconditionally gives only `ε < 1/6 ≈ 0.167`"* at [`OneThird-LIBweak-mg-c4f5-IndependentAudit.md:415`](docs/OneThird-LIBweak-mg-c4f5-IndependentAudit.md)) — so `ε_spec/ε_c3ca = 6n²/(n²−1) → 6` and **the explicit `/6` this row's own `(ε_spec/6)(n²−1)` carries is the entire difference;

### S7 — how the `≥` half of Claim 3.1 was confirmed

*In the row it stood between “… `η > 0`, both directions PROVEN FOR ALL `n`** (” and “mg-6bc2 Claim 3.1), so **`Op-Form` Claim 6.1 is …”:*

the `≥` by this file's own two-atom law, machine-confirmed exactly at `n = 3,4,5,6`;

### S8 — the parallel footrule statement, whose attainment is FINITE-POPULATION

*In the row it stood between “…ndary `η = 0` is a supremum for the frozen class” and “.)* **Which `1/6` was meant is Daniel's question…”:*

; the parallel **footrule** statement `max{ 3E_μ[footrule]/(n²−1) } = n/(n+1)` has `≤` proven for all `n` but its **ATTAINMENT is FINITE-POPULATION — `n = 3,4,5,6` by exact-rational LP, `n = 8` by explicit construction, NOT proven for all `n`** (mg-6bc2 Claim 4.1)

### S9 — how mg-210d's master bound was checked

*In the row it stood between “…dering `λ_std → 1` (via mg-210d's master bound, ” and “mg-c4f5) — but **(LIB-weak) ⟹ (LIB-const) only f…”:*

re-derived by hand and tested at 0 violations over 101,658 posets n ≤ 7,

### S10 — the construction that shows NO `N₀` works for the class

*In the row it stood between “…anded mg-5ce3 — re-derived independently there).” and “ **What that closes:** *go and find `N₀`* is **n…”:*

For any candidate `N₀`, `g(n) = n²` below `N₀` and `n²/log₂ n` at and above is `o(n²)` and violates `E[inv_e] ≤ (ε_spec/6)(n²−1)` throughout `[1, N₀)`; and the tame member `n²/log₂ n` on its own first satisfies (LIB-const) at `log₂ n ≥ 6/ε_spec = 300`, i.e. **`n ≥ 2³⁰⁰ ≈ 10⁹⁰`** at the repaired `ε_spec = 2×10⁻²` (`10⁹⁰³¹` at the superseded `2×10⁻⁴`).

### S11 — what the `N₀` finding does NOT claim

*In the row it stood between “…he qualitative hypothesis never can, at any `n`.” and “ As asymptotic classes `(LIB) ⊊ (LIB-weak) ⊊ (LI…”:*

**What it does not claim:** a single family satisfying (LIB-weak) does have *some* threshold of its own — it is simply not a function of the hypothesis, so it cannot be extracted from it, and any argument that needs `N₀` must first prove something strictly stronger than (LIB-weak). So it does *not* supply the constant form this row leads with.

### S12 — why the literature bound is not falling short of an unknown number

*In the row it stood between “…till true): **there is no threshold to exceed.**” and “ it is being offered against a quantifier that *…”:*

No `N₀` works for the class (mg-c4f5 §5.3, earlier in this cell), so the bound is not falling short of an unknown number —

### S13 — the kind marked at Claim 3.1

*In the row it stood between “…ality** rather than a bound awaiting sharpening.” and “; the parallel **footrule** statement `max{ 3E_μ…”:*

*(Kind marked at the claim: Claim 3.1's `≤` and its attainment **in `M_n(η)` for each `η > 0`** are theorems for all `n`, and the value at the boundary `η = 0` is a supremum for the frozen class

### S14 — what a *rate* would give that the qualitative hypothesis cannot

*In the row it stood between “…pothesis at all, so there is nothing to compute.” and “ **What it does not claim:** a single family sat…”:*

Only a *rate* would give one ((LIB)'s `O(n)`, or `o(n²)` carrying an explicit modulus); the qualitative hypothesis never can, at any `n`.

### S15 — why a future computation of `N₀` would not change this

*In the row it stood between “…ier that **no** number, however large, addresses” and “. Separately, it also falls short of the two thr…”:*

; a future computation of `N₀` will not change this, because there is none to compute
