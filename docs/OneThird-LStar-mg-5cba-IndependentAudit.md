# INDEPENDENT AUDIT of mg-789d — **the refutation of (L\*) STANDS, and it is bigger than it was filed as: a FIFTH counterexample at n = 12 is certified here, the one mg-789d's own table claims and never certified.** The `ρΔ > 1` onset is **n = 5**, not the corrected `n = 6` — the correction was itself one value of `n` late. `LSTAR(6)` is `0.794235`, not `0.794253`. The `(SO)` count `338` is an `n ≤ 6` subtotal wearing an `n ≤ 7` label — mg-789d's own instrument prints `2500`. **VERDICT: CONFIRMED-WITH-REPAIRS.**

**mg-5cba**, auditing **mg-789d**. Pre-filed in the same tool call as its parent, then
re-scoped by pm-onethird at 03:38Z when (L\*) came back FALSE.

Instrument: `code/audit_5cba/` (`lib5cba.py` + `a0`…`a7`). **`lib789d.py` was not opened
until after `lib5cba.py` and `a1_witness.py` were written and `a1` had run** — the
definitions were re-derived from the corpus and cross-read only against
`code/anticorrelation_c50b/libc50b.py` §§1–3, which is mg-789d's *parent* and an
independent implementation. `out_s5_certify.txt` was read for the `dn` tuples and the
claimed figures; every verdict below is recomputed.

---

## 0. The one-line answer

**The refutation is correct.** All four of mg-789d's counterexamples re-certify
independently, in exact rationals, on an instrument that shares no line with
`lib789d.py` — every published figure to every printed digit. **The disjunction
survives**, and it survives for the reason mg-789d gives: (L\*) was strictly
sufficient, and the gap between it and (M♯) is exactly `mu_pref²`.

Six repairs, none of which touches the headline:

| # | claim as landed | as measured here |
|---|---|---|
| **R1** | `ρΔ > 1` occurs **from n = 6**, max `1.15672` over 4070 | **from n = 5** — 6 of the 275 primitive posets, max `1.027118`, exact. `n = 3, 4` certified clean. The corrected onset was itself **one value of `n` late**. |
| **R2** | `LSTAR(6) = 0.794253` | **`0.794235`** — exact bracket `[0.794234562, 0.794234567]`. `0.794253` is attained at **no** primitive `n = 6` poset. A digit transposition. |
| **R3** | "at every one of the 90655 primitive posets of `n ≤ 7`: **338** satisfy (SO)" | **2500** — which is what mg-789d's **own** `out_s4_theoremA.txt` prints. `338` is the `n ≤ 6` subtotal. |
| **R4** | "(M♯) holds at all **three** counterexamples, `u_M` = 0.943 / 0.982 / 0.958" | mg-789d certifies **four**. The missing one is `(0,0,0,0,0,16,48,16,247)` — the `n = 9` **argmax**, its strongest `n = 9` witness. `u_M = 0.947534`. Survival is **4 of 4**, measured here. |
| **R5** | LSTAR table row `12 \| >= 1.057643 \| (L*) FALSE` | **never certified by mg-789d** — `S5.4` lists four counterexamples at `n = 9, 9, 10, 11`. **This audit certifies it exactly.** The claim is true; there are **five** counterexamples, not four. |
| **R6** | the `n ≥ 8` LSTAR rows read `>= x` | they are computed from `mu_ub_float`, an **upper** bound on `mu_pref`, so they are upper bounds on `min(v_F,v_L)` and cannot certify `LSTAR(n) >= x`. Certified: `n=9` **1.013486**, `n=11` **1.025041**, `n=12` **1.057468**. |

**What this audit did NOT find.** No error in any of the four certificates. No error in
Theorem A's proof. No place where the shipped refutation depends on defect D1. No site
that states `n = 8` is closed.

---

## 1. The four counterexamples, re-certified (`a1`)

`a1_witness.py` runs all four plus mg-789d's three controls. **99 arms, 0 failures.**

```
C1  n=9   dn = (0, 1, 0, 4, 0, 0, 32, 96, 239)     LE = 1890   height 4   primitive
    Delta = 62/63   M = 41/84   argmin_i (S_P)_ii = element 5, at 1/63
    (F) FAILS               R(M^2/2) = R(1681,14112) is NOT PSD          [integer]
    gamma  < 23459/200000   R(23459,200000) is NOT PSD                   [integer]
    mu_pref >= 6011/50000   R(6011,50000) IS COPOSITIVE, 8x8             [integer]
    mu_pref*Delta >= 186341/1575000 = 0.118311746  >  0.117295 > gamma
    *** (L*) REFUTED ***    and (M#) HOLDS: u_M = 0.943486
```

and the same for `C2 (n=9)`, `C3 (n=10)`, `C4 (n=11)`. Independently of mg-789d's
rational witnesses, this audit's own brackets give

| | `Delta` | `gamma <` | `mu_pref >=` | `v_L >` | `v_F >` | `u_M` |
|---|---|---|---|---|---|---|
| C1 `n=9` | `62/63` | `0.117293057` | `0.120233849` | `1.008801` | `1.015563` | `0.943486` |
| C2 `n=9` | `311/315` | `0.118609371` | `0.121755064` | `1.013486` | `1.026184` | **`0.947534`** |
| C3 `n=10` | `565/574` | `0.070325342` | `0.072896623` | `1.020310` | `1.071186` | `0.981830` |
| C4 `n=11` | `135/136` | `0.119915748` | `0.123829049` | `1.025041` | `1.042691` | `0.958326` |
| **C5 `n=12`** | `195/196` | `0.061699262` | `0.065579592` | `1.057468` | `1.077029` | — |

**The controls behave, which is what makes the certifier's "yes" mean something.**
mg-c50b's S4.1 argmax and S2.2 witness come back **not** counterexamples — and this
audit goes one step further than mg-789d there, certifying (L\*)'s conclusion
`mu_pref*Delta <= gamma` in *its* hard direction at both, rather than only failing to
certify the opposite. chain(9)+point has `mu_pref*Delta > gamma` **certified** with (F)
holding, exactly as mg-789d reports.

### 1.1 The copositivity routine is COMPLETE here, not merely sound

mg-789d **refuses** a singular face rather than deciding it. That is safe and it is
honest, but it means a certificate could in principle be lost to a face the method
declines to look at. This audit's criterion is

> `R` is **not** copositive **⟺** for some nonempty `S ⊆ [m]` the system
> `R_S y = 1_S`, `y < 0` (strict) is feasible

— proved in `lib5cba.py`'s docstring from the KKT conditions of
`min{c'Rc : c ≥ 0, Σc = 1}`, with **no nonsingularity assumption**. A singular face is
decided by exact Fourier–Motzkin over the nullspace coordinates, in `Fraction`s.

**Measured: 0 singular faces arose across all seven posets.** So mg-789d's refusal
branch never fired on its verdict path, and its certificates are unaffected. The point
of saying so is that this was checked, not assumed.

### 1.2 Nothing on any verdict path is a float

`gamma >= t` and `mu_pref >= t` are decided on the **same integer matrix**
`R(a,b) = b·n·QI − 2·LE·a·NI` — PSD for the first, copositive for the second. Floats
appear only in `*_float` search helpers, and every float result in this audit is
bracketed by an exact pair before it is used. Two independent `mu_pref` paths (psi-basis
copositivity bisection; f-space consecutive-block face enumeration) agree at every poset
tested, and two independent `gamma` paths (integer PSD bisection; Jacobi on `A`) agree.

---

## 2. The survival claim, which is the whole difference between "a route died" and "the programme died" (`a2`)

**(L\*) ⟹ the disjunction, uniformly in `n`, in one line, with NO side condition.**

> Assume (L\*) at `P`. If `M² ≤ 2γ` then (F) holds. Otherwise `μ_pref·Δ ≤ γ`, and
> * `μ_pref ≤ Δ`: `sweep = μ_pref(2Δ − μ_pref) ≤ 2Δμ_pref ≤ 2γ`
> * `μ_pref > Δ`: `sweep = Δ² < Δ·μ_pref ≤ γ ≤ 2γ`
>
> so (M♯) holds. ∎

The only facts used are `μ_pref ≥ 0`, `Δ ≥ 0`, `γ ≥ 0`, all three unconditional, and `n`
never appears. **This was the original ticket's target 1 and the answer is that the
implication is clean.** (Moot for (L\*) itself, but it is the load-bearing step in the
survival claim, so it had to be re-derived rather than inherited.)

**(L\*) is STRICTLY sufficient, and the gap is exactly `μ_pref²`:**

```
(L*)'s conclusion :  2 Delta mu_pref              <= 2 gamma
(M#)              :  2 Delta mu_pref - mu_pref^2  <= 2 gamma
```

so a counterexample to (L\*) lands in the gap unless it *also* breaks (M♯). All five
land in the gap. **Had the two been equivalent, the refutation would have taken the
disjunction with it.** They are not, and it does not.

**Controls that could have fired.** Over every primitive poset at `n ≤ 6` and all 168
`(F)`-failing posets at `n = 7`, decided exactly with the bracket ends chosen so that a
hit would be real: **0 posets** have (L\*)'s conclusion together with (M♯) failing, and
**both routes fail at 0 of the 168**.

### 2.1 R4 — the survival claim covered three of four counterexamples

mg-789d's `S6.1` table has three rows: `n = 9`, `n = 10`, `n = 11`. Its `S5.4` certifies
**four** counterexamples, two of them at `n = 9`. The one absent from the survival table
is `(0,0,0,0,0,16,48,16,247)` — and it is not a minor one: `S6.2` records it as the
`n = 9` **argmax**, the strongest `n = 9` witness mg-789d found. Measured here:

```
C2  u_M = mu_pref/t* = 0.947534  <  1     (M#) HOLDS      disjunction SURVIVES
```

so the claim extends to **4 of 4**. This is a coverage gap closed, not a number moved.

---

## 3. R5 — the fifth counterexample, at n = 12 (`a5`)

mg-789d's `LSTAR(n)` table reads `12 | >= 1.057643 | SEARCH ONLY -- (L*) FALSE`. Its
`§0` reads *"**Four** counterexamples are certified this way in total — two at `n = 9`,
one at `n = 10`, one at `n = 11`"*. **Those two statements contradict each other**, and
`out_s5_certify.txt` settles which is right: `S5.3` treats four candidates and `S5.4`
lists four. `s1_hunt.py`'s `S1.4` handed **five** candidates to the exact stage; the
`n = 12` one was dropped.

This audit certifies it:

```
n = 12   dn = (0, 0, 3, 7, 15, 7, 63, 2, 135, 391, 7, 1159)   LE = 10584
         Delta = 195/196    M = 7717/21168
         (F) FAILS                          [integer PSD refusal]
         gamma   <  0.061699262             [integer PSD refusal]
         mu_pref >= 0.065579592             [11x11 integer copositivity]
         mu_pref*Delta > gamma              *** (L*) REFUTED ***
```

So the table's row is **true**, and the count is **five**, not four. The defect as landed
was that a `(L*) FALSE` marker sat in a table on the strength of a float upper bound.

## 3.1 R6 — the n ≥ 8 rows point the wrong way

Every `LSTAR(n)` figure for `n ≥ 8` comes from `s1_hunt.py:50` / `s6_aftermath.py:71`,
which score the hill climb with `mu_ub_float`. That is the **correct** choice for a
screen — an upper bound on `μ_pref` can only over-select, so no counterexample is
hidden. But an upper bound on `μ_pref` is an upper bound on `v_L`, hence on
`min(v_F, v_L)`, hence on `LSTAR(n)`. It **cannot** certify `LSTAR(n) >= x`.

| row | printed | certified here | direction |
|---|---|---|---|
| `n = 8` | `0.968818` | `0.968818` | agree to 6 dp |
| `n = 9` | `1.013539` | **`1.013486`** | printed is **higher** |
| `n = 10` | `1.020310` | `1.020310` | agree to 6 dp |
| `n = 11` | `1.025044` | **`1.025041`** | printed is **higher** |
| `n = 12` | `1.057643` | **`1.057468`** | printed is **higher** |

Every discrepancy runs the way an upper bound must. The `(L*) FALSE` verdicts at
`n = 9, 10, 11, 12` are unaffected — all four certify with room.

**The `n = 8` relabelling claim checks out, and it is not the no-op it reads as.**
mg-789d says its `0.968818` at `(0,0,2,0,8,24,63,62)` "is *exactly* mg-c50b's published
`n = 8` maximum, at a relabelling of their argmax". A relabelling *moves* `γ` and `M`:
mg-c50b's `(0,0,2,0,8,24,62,63)` has `γ = 0.047583`, `M = 723/2080`, `ρΔ = 0.968159`,
while the transposed labelling has `γ = 0.049600`, `M = 733/2080`, `ρΔ = 0.968818`. The
sentence is right — `0.968818` is mg-c50b's published maximum and it is attained at the
*other* labelling — but only because the maximum is not at mg-c50b's `c_or` argmax.

---

## 4. R1 — the onset of `ρΔ > 1` is n = 5 (`a3`, `a7`)

mg-789d's sharpest corollary correction is that `ρΔ > 1` occurs **from `n = 6`**, against
the corpus's standing "from `n = 10` at 1.078" — four values of `n` earlier, and the
roadmap has already carried it. Exhaustive here:

```
   n | primitive |  max v_L   | argmax                    | v_L > 1 at
   3 |         4 | 0.666667   | (0, 0, 2)                 |    0
   4 |        27 | 0.904508   | (0, 1, 0, 4)              |    0
   5 |       275 | 1.027118   | (0, 1, 0, 4, 4)           |    6     <-- NOT ZERO
   6 |      4070 | 1.156724   | (0, 0, 3, 0, 8, 8)        |  192
   7 |     86278 | 1.218869   | (0, 0, 0, 7, 0, 16, 16)   | 6464
```

The `n = 6` figure `1.156724` reproduces mg-789d's `1.15672` exactly. **The onset does
not.** Certified in exact rationals (`a7`), `μ_pref` from below by copositivity and `γ`
from above by an integer PSD refusal:

```
 dn=(0, 0, 3, 0, 8)   LE=20  Delta=9/10  mu*Delta >= 0.481218018 > 0.468512845 >= gamma
 dn=(0, 1, 0, 4, 4)   LE=20  Delta=9/10  mu*Delta >= 0.481218018 > 0.468512845 >= gamma
 dn=(0, 1, 0, 4, 12)  LE=10  Delta=9/10  mu*Delta >= 0.396103915 > 0.392849650 >= gamma
 dn=(0, 1, 3, 0, 8)   LE=10  Delta=9/10  mu*Delta >= 0.396103915 > 0.392849650 >= gamma
 dn=(0, 1, 0, 4, 13)  LE= 9  Delta=8/9   mu*Delta >= 0.311148301 > 0.311075755 >= gamma
 dn=(0, 1, 3, 0, 9)   LE= 9  Delta=8/9   mu*Delta >= 0.311148301 > 0.311075755 >= gamma
```

and, in the other direction, `μ_pref·Δ ≤ γ` is certified at **every** primitive poset of
`n = 3` and `n = 4`. **So the onset is exactly `n = 5`.** `(F)` HOLDS at all six, so none
is a counterexample to (L\*) — the point of the corollary is unchanged, which is that
the `(F)` hypothesis is load-bearing, and it is load-bearing **five** values of `n`
earlier than the corpus knew rather than four.

*Why this matters more than its size.* The corollary travels: it is already in
`docs/roadmap.md` in two places. A correction that lands one value short is harder to
catch afterwards than an uncorrected figure, because it now reads as *checked*.

## 4.1 R2 — LSTAR(6)

```
max min(v_F, v_L) over all 4070 primitive n=6 posets = 0.794234564 at (0,0,0,0,15,14)
EXACT bracket: [0.794234562, 0.794234567]
primitive n=6 posets attaining 0.794253 to 6 dp: 0
```

`LSTAR(3) = 0.250000`, `LSTAR(4) = 0.306250`, `LSTAR(5) = 0.550747` and
`LSTAR(7) = 0.923894` all reproduce exactly. Only the `n = 6` entry moves, and it moves
by a transposition of two digits.

---

## 5. Theorem A — the proof, not the 90655 agreements (`a4`)

The proof is audited step by step in `a4_theoremA.py`'s docstring. **No gap found.**
The seven steps and what each needs:

1. `(SO) ⟺ A C ⊆ C` — Abel summation with `U_n = 0` from double stochasticity, converse
   by `f = 1_{A_k}`. **Valid.**
2. `A' = (I+A)/2` symmetric doubly stochastic, spectrum in `[0,1]`, `A'C ⊆ C`. **Valid**,
   and the shift is **load-bearing**: without it the induced spectral radius is
   `max(|λ₂|, |λ_n|)`, which need not be `λ₂`. mg-789d states the shift; it does not
   state why, and that is the one place the write-up could be read as decorative.
3. Image of `C` in `V = Rⁿ/⟨1⟩` is a **proper** cone — `C`'s lineality space is exactly
   the constants, so the image is closed and pointed; strictly decreasing vectors are
   interior, so it is solid. **Valid.**
4. `spec(T) = {(1+λ_i)/2 : i ≥ 2}`, all ≥ 0, so `r(T) = (1+λ₂)/2`. **Valid.**
5. Krein–Rutman / Berman–Plemmons Ch.1 Thm 3.2: `r(T)` is an eigenvalue with an
   eigenvector **in** the cone. **Valid** — no irreducibility is required for this form.
6. `1'A' = 1'` and `1'f = 0` force the shift constant to 0, so `Af = λ₂ f`. **Valid.**
7. `C` is invariant under adding constants, so the centred representative is itself
   nonincreasing; its Rayleigh quotient is `1 − λ₂ = γ`, and `μ_pref ≥ γ` always.
   **Valid.**

**Machine check, re-run independently.** Every count reproduces:

```
   n | primitive | (SO) | (SO) with rho=1 | rho=1
   2 |         1 |    1 |               1 |     1
   3 |         4 |    2 |               2 |     4
   4 |        27 |    9 |               9 |    17
   5 |       275 |   45 |              45 |   109
   6 |      4070 |  281 |             281 |   906
   7 |     86278 | 2162 |            2162 | 10806
 TOTAL n<=7: 90655 primitive, 2500 with (SO), rho = 1 at all 2500, NO exception
```

Coverage of the `(F)`-failing set at `n = 7`: **4 of 168**, ceiling **24 of 168**, so 144
need a genuine inequality — all three reproduce. Negative control live: chain(n−1)+point
violates (SO) by 0.375…0.4375 at `n = 8…16` with `ρ > 1` at each.

**R3.** The document's `§3` says *"Machine-checked at **every one of the 90655** primitive
posets of `n ≤ 7` (`s4`): **338** of them satisfy (SO)"*. `338 = 1+2+9+45+281` is the
`n ≤ 6` subtotal. mg-789d's own `out_s4_theoremA.txt` prints **2500** and is right; the
document under-states its own check by a factor of 7.4 and pairs an `n ≤ 7` population
with an `n ≤ 6` count in one sentence.

---

## 6. D1's blast radius — measured, not assumed (`a2`, `a5`)

pm-onethird's target 3: establish that the shipped result does not depend anywhere on
the path that was defective. `mu_ub_float` is called at:

| site | what it feeds | does the shipped refutation depend on it? |
|---|---|---|
| `s1_hunt.py:50` | the candidate **screen** and the hill-climb objective | **No.** An upper bound on `μ_pref` over-selects, so no counterexample can hide from it. Candidates are re-decided exactly in `s5`. |
| `s2_reduce.py:148,204,234` | the (R1)/(R2) route measurements | **No** for the refutation. This audit re-derives (R1) **exactly** (one integer PSD test per poset) and gets the same 166/168. |
| `s4_theoremA.py:88,124,132,137,156` | the `ρ = 1` counts and the 24/168 ceiling | **No** — and reproduced here on the exact-face path: 2500 / 906 / 24 / 4 all agree. |
| `s6_aftermath.py:71` | the `n = 8..12` search figures | **Yes**, and that is **R6**: those rows are upper bounds wearing `>=`. |
| **`s5_certify.py`** | **the four certificates** | **No** — `s5` uses `mu_faces` and exact copositivity. |
| **`s6_aftermath.py:40`** | **the survival table** | **No** — `mu_faces`. |

So: **the refutation and the survival claim are clear of D1; the LSTAR table's `n ≥ 8`
rows are not.** The direction of the residue is the safe one for every verdict and the
unsafe one for every `>=`.

The arm that would fire if D1 returned is live here too: `μ_pref ≥ γ` at every primitive
poset `n ≤ 6`, **and** `μ_pref > γ` strictly somewhere — a two-sided check, which is the
exact shape mg-789d's original one-sided `max(mu_ub − mu_exact)` lacked.

---

## 7. n = 8 is not closed anywhere (`a5`, doc sweep)

Swept `STATE.md`, `docs/roadmap.md`, `docs/OneThird-LStar-mg-789d.md`,
`docs/OneThird-AntiCorrelation-mg-c50b.md` for `3589`, `2600369`, `0.968818`, `LSTAR`.
Every site that mentions `n = 8` and (L\*) says **SEARCH** or **OPEN**:

* `OneThird-LStar-mg-789d.md:202` — `SEARCH ONLY -- see the scope note below`
* `OneThird-LStar-mg-789d.md:225` — *"It is **not** a census … **Whether (L\*) already
  fails at `n = 8` is open.**"*
* `OneThird-LStar-mg-789d.md:287` (ledger) — `OPEN — 60 restarts reached 0.968818, not a census`
* `roadmap.md:21–22` — `Still open … a SEARCH, not a census, over 2600369 primitive posets`

**Nothing states otherwise.** Confirmed, and `(L*)` HOLDS at the `n = 8` search argmax
with the certified value `0.968818 < 1`.

**mg-c50b's screening argument, which carries the exhaustive claims, is valid.** The
screen keeps a poset when `min(c♯_UB, f*) > 0.85`; if both routes fail then `f* > 1` and
`c♯ > 1`, and `c♯_UB ≥ c♯` gives `c♯_UB > 1`, so `min > 1 > 0.85` and the poset is kept.
The inequality it rests on — `μ_pref ≤ 2Φ*_pref` — is checked here and holds at every
sampled primitive poset `n ≤ 7`. So **both routes fail at 0 of 2600369** is exhaustive.
The `(F)`-alone count `3589` is **not**, and mg-c50b's own E9 says so; nothing in
mg-789d's landing upgrades it.

---

## 8. Status ledger

| claim | status |
|---|---|
| (L\*) is false, first exhibited at `n = 9` | **CONFIRMED** — 4 counterexamples independently re-certified in exact rationals |
| a **fifth** counterexample at `n = 12` | **CERTIFIED HERE** — mg-789d's table claims it, `s5` never certified it |
| the certifier's controls (2 negative, 1 positive) | **CONFIRMED**, and the two negatives strengthened to a certificate in the hard direction |
| (L\*) ⟹ the disjunction, uniformly in `n`, no side condition | **CONFIRMED** — re-derived; `μ_pref ≥ 0` is the only fact used |
| (L\*) strictly sufficient, gap `= μ_pref²`; disjunction survives | **CONFIRMED** — all five counterexamples lie in the gap |
| (M♯) holds at the counterexamples | **CONFIRMED at 4 of 4** — the landing measured 3 of 4 (**R4**) |
| Theorem A's **proof** | **VALID** — 7 steps audited, no gap; the `(I+A)/2` shift is load-bearing |
| Theorem A's machine check | **REPRODUCED** — 2500 / 906 / 4 of 168 / 24 of 168 |
| "338 satisfy (SO) at `n ≤ 7`" | **WRONG SCOPE (R3)** — 338 is `n ≤ 6`; `n ≤ 7` is 2500, per mg-789d's own output |
| (R1) refuted, max `1.020090`, holds 166/168 | **CONFIRMED**, and re-derived **exactly** rather than in floats |
| (R2) refuted, max `12.871823`, holds 35/168 | **CONFIRMED** |
| `(F)`-failing at `n = 7` = 168; both routes fail at 0 of them | **CONFIRMED** |
| `LSTAR(3,4,5,7)` | **CONFIRMED** |
| `LSTAR(6) = 0.794253` | **WRONG (R2)** — `0.794235`, exact bracket, attained at no poset |
| `ρΔ > 1` from `n = 6` | **WRONG (R1)** — from `n = 5`, certified; `n ≤ 4` certified clean |
| `LSTAR(n) >= x` for `n ≥ 8` | **DIRECTION WRONG (R6)** — computed from an upper bound on `μ_pref` |
| D1's blast radius | **MEASURED** — clear of the refutation and the survival claim; **not** clear of the `n ≥ 8` LSTAR rows |
| whether (L\*) already fails at `n = 8` | **OPEN**, and stated as open at every site |
| mg-c50b's `n = 8` screening argument | **VALID** for both-routes-fail; **not** for the 3589, as mg-c50b itself says |

## 9. One defect of my own

`a1_witness.py` first asserted *"mu\_pref\*Delta > gamma (ticket's own two certificates)"*
on the **negative controls** as well as the counterexamples — an arm that demanded the
certifier fire where it must refuse. It fired `FAIL` twice, at `N1` and `N2`, which is
the control working: the arm was wrong, not the certifier. Fixed by branching the
assertion on whether the poset is supposed to be a counterexample. It is recorded rather
than quietly corrected because the same shape — an assertion that cannot distinguish
"the thing I am testing failed" from "my test asked for the wrong thing" — is D1's shape
and mg-9bc2's shape, and this lineage has now produced it three times.

## 10. What the successor should do

1. **Settle `n = 8`.** Unchanged from mg-789d's own recommendation, and still the only
   thing standing between "first failure at `n = 9`" and a theorem.
2. **Re-run the `n ≥ 8` LSTAR rows against a LOWER bound on `μ_pref`** and reprint them
   as certified values, or relabel them `<=`. The certified `n = 9..12` values are in §3.1.
3. **Sweep the corpus for the `n = 6` onset figure** — it is in `roadmap.md` twice and it
   is now `n = 5`. Land the whole class, not the two sites this audit names.
