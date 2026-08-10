# mg-b417 — THE u_M FRONTIER, and the DISJUNCTION

> ## ⚠️ PENDING INDEPENDENT RE-CERTIFICATION — mg-5e82
>
> **Every verdict in this tree is CERTIFIED-PENDING-AUDIT.** The certifier is
> `code/audit_5cba/lib5cba.py`, used unmodified. That is the audited exact instrument
> of this thread — and it is now **the audited instrument auditing itself**: a
> programme-level negative resting on the one certifier, which has never itself been
> audited. pm-onethird has filed **mg-5e82**, ranked ahead of this ticket, requiring the
> devices rebuilt on an instrument that is not `lib5cba`, `lib789d` or `libc50b`.
>
> Nothing here has been relayed to `STATE.md`, `roadmap.md`, or anywhere outside this
> directory, at pm-onethird's instruction and on my agreement. **A reader who finds this
> tomorrow should treat it as unaudited.**

---

## 0. THE HEADLINE, AND IT IS NOT WHAT THE TICKET ASKED FOR

The ticket asked how close `u_M` had come to 1, and framed the answer as two futures:
approaching 1, or saturating below it.

**Neither. It crosses.** The DISJUNCTION — *(F) or (M♯) at every primitive poset* — is
**FALSE**, and the first counterexample was already committed to this repository, already
certified in exact rationals, and already published. **In two halves that nobody
multiplied.**

**THE FINDING IS A BLANK TABLE CELL.**

mg-5cba certified **five** `(L*)` counterexamples, not four. Its audit table
(`docs/OneThird-LStar-mg-5cba-IndependentAudit.md:58-64`) carries a `u_M` column:

| | n | u_M |
|---|---|---|
| C1 | 9 | 0.943486 |
| C2 | 9 | 0.947534 |
| C3 | 10 | 0.981830 |
| C4 | 11 | 0.958326 |
| **C5** | **12** | **—    ← THE DASH** |

`STATE.md` then publishes *"`(M♯)` HOLDS at **4 of 4**"* with those four figures. That
sentence is true of the four it names, **and it names four because the fifth cell was
blank**. My own ticket inherited it: *"u_M = 0.981830 at n=10 is the closest any (M♯)
witness has come to failing."* It is not the closest. **It is the closest of the four
that were computed.**

Both inputs to the missing cell were published, for that exact poset, by mg-5cba, in
`code/audit_5cba/out_a5_scope.txt:51-53`:

```
gamma in [0.061699260, 0.061699262]        mu_pref >= 0.065579592        Delta = 195/196
```

and

```
t* = Delta - sqrt(Delta^2 - 2 gamma)  <=  0.064079274  <  0.065579592  <=  mu_pref
```

so `(M♯)` **FAILS** there — and `(F)` fails there too (mg-5cba: `v_F = 1.077029`). The
multiplication is four lines of arithmetic on figures that have been on `main` since
mg-5cba landed. **A BLANK BECAME A BOUND.**

`b1` fills the cell with an integer certificate rather than with that argument:

```
dn = (0, 0, 3, 7, 15, 7, 63, 2, 135, 391, 7, 1159)   n = 12   LE = 10584
Delta = 195/196     M = 7717/21168     primitive, naturally labelled, transitively closed

gamma   <  529992611/8589934592       = 0.061699260375    [R(g_ub) NOT PSD]
mu_pref >= 550121491741/8388608000000 = 0.065579592197    [R(m_lo) COPOSITIVE, 11x11 integer]

(F)  FAILS:  gamma < M^2/2                                [R(M^2/2) NOT PSD]
(M♯) FAILS:  sweep(m_lo,Delta) - 2 g_ub = +0.002790801218 > 0

  => c# >= 1.022616164     f* >= 1.077028990
  => u_M >= 1.023413503    u_F >= 1.037800072
```

---

## 1. AND THE SEARCH PUSHED IT DOWN TO n = 10 AND UP TO 1.070

`b2` hill-climbs `J(P) = min(u_F, u_M)` — the disjunction quantity — and `b4` decides
every champion on integers. **26 distinct posets certify as counterexamples**, at
`n = 10, 11, 12, 13, 14`, from **0 refusals in 36 champions tested**.

| n | W(n) ≥ (**certified**) | refutes | height | μ_pref ≥ | argmax `dn` |
|---|---|---|---|---|---|
| 9 | 0.969347 | no | 4 | 0.071667 | `(0,1,0,0,8,8,56,125,127)` |
| **10** | **1.000546** | **YES** | 4 | 0.056389 | `(0,0,0,7,15,31,15,6,135,135)` |
| 11 | 1.027642 | YES | 4 | 0.061409 | `(0,0,0,7,15,15,63,6,135,135,647)` |
| 12 | 1.043923 | YES | 5 | 0.064629 | `(0,0,0,7,15,31,63,6,135,135,647,135)` |
| 13 | 1.057639 | YES | 5 | 0.066765 | `(0,0,0,7,15,31,63,6,135,135,903,135,2183)` |
| 14 | **1.067739** | YES | 5 | 0.068264 | `(0,0,0,7,15,31,63,6,135,135,903,135,2183,6279)` |

**SMALLEST n EXHIBITED: 10** — two independent posets there, the tighter with an exact
margin of `+0.0000583`, five orders of magnitude above the bisection precision of the
`m_lo` it uses.

**EVERY ROW IS A SEARCH FIGURE AND NONE IS A MAXIMUM.** `0.968818` at `n = 8` is barred
from being quoted as a maximum for exactly this reason and the same bar applies here.
The restart budgets — 30 / 24 / 18 / 14 / 10 / 8 at `n = 9..14` — are printed beside
every row in `out_b2_climb.txt`, and the budget *falls* where the values *rise*.

**`n = 9` DID NOT CROSS.** 30 restarts topped out at a certified `0.969347`. That is a
statement about 30 restarts and about nothing else.

**WHAT IS STILL EXHAUSTIVE AND STILL TRUE.** The disjunction holds at every primitive
poset of `n ≤ 8`: `W(3..7) = 0.000000 / 0.486136 / 0.649886 / 0.818379 / 0.890780`, and
at `n = 8` both routes fail at 0 of 2600369 with `c_or(8) = 0.943649` (mg-c50b). `b0`
arm S6 re-derives `W(7) = 0.890780` at mg-c50b's own argmax from this tree's objective,
over 86278 primitive posets, in 732 s. **What died is uniformity in `n`, not the small-`n`
record.**

---

## 2. WHAT THIS KILLS, AND WHAT IT DOES NOT

**KILLS.** The uniform-in-`n` DISJUNCTION, and therefore the `(F)`-or-`(M♯)` route to
`C₃ = 1`. `(L*)` was **sufficient for** the disjunction and never equivalent to it, and
the corpus recorded that the disjunction *survived* `(L*)`'s refutation. It does not
survive it. **The same five posets kill both, and the fifth was never asked.**

**DOES NOT KILL.** `C₃ = 1`. A dead route is a dead route, exactly as when `(L*)` died. I
make no claim about the conjecture.

**DOES NOT SETTLE.** Whether the disjunction fails at `n = 9`. Nothing here enumerates
anything at `n ≥ 9`; the last exhaustive statement in the corpus is `n = 8` and it is
clean. **"First exhibited at 10", never "first at 10".**

**UNTOUCHED.** Theorem A, the depth table, the `ρΔ_P ≤ 1 ⟹ (M♯)` implication, the
`ρΔ` onset at `n = 5`, and the `n ≤ 8` enumerations. None of them is a casualty of this.

---

## 3. THE IDENTITY THAT ORGANISES ALL OF IT

Whenever `Δ² > 2γ`,

```
u_M = v_L * D,        D = (1 + sqrt(1 - 2 gamma/Delta^2)) / 2   <  1
```

where `v_L = μ_pref·Δ/γ` is **`(L*)`'s own scalar**. Equivalently, since `(M♯)` is
`(L*)`'s conclusion relaxed by exactly `μ_pref²/2`:

```
(M#) FAILS   <=>   v_L  >  1 + rho * mu_pref / 2
```

So **the `(M♯)` frontier is the `(L*)` frontier discounted by `D`**, and the `(L*)`
violation must beat `μ_pref/2`. Checked at 3507 primitive posets of `n ≤ 6` to 7.2e-16
(`b0` S2), and it reproduces all four published `u_M` figures to six places (`b0` S1).

**IT ANSWERS WHY C5 AND NOT C3.** The bar `1 + ρμ/2` is set by `μ_pref`:

| | v_L | bar | clears? |
|---|---|---|---|
| C1 n=9 | 1.008801 | ≈1.062 | no |
| C2 n=9 | 1.013486 | ≈1.063 | no |
| C3 n=10 | 1.020310 | ≈1.038 | no |
| C4 n=11 | 1.025041 | ≈1.064 | no |
| **C5 n=12** | **1.057468** | **≈1.035** | **YES** |

C5 does not have the largest `(L*)` violation relative to a fixed bar — it has the
**smallest `μ_pref`** of the five with `Δ` still within 0.6% of 1, so its bar is the
lowest. A thin cut lowers the bar and raises `D` at the same time.

**AND THE PREDICTION IT REFUTES IS MINE.** I predicted (P4) that the thin cut is what
drives the frontier. `b3` decomposes the rise multiplicatively — `log u_M = log v_L +
log D`, residual 3.6e-16 — and across `n = 9..14`:

```
u_M  0.968129 -> 1.070221    dlog +0.100255
v_L  1.006331 -> 1.105569    dlog +0.094049    93.8% of the move
D    0.962038 -> 0.968028    dlog +0.006207     6.2% of the move
D across the searched n:  0.962  0.971  0.970  0.969  0.968  0.968   (range 0.0091)
```

The champion family holds `γ/Δ²` **near-constant** and pushes the `(L*)` violation. So
the small-`μ` mechanism is what separates a crossing witness from a non-crossing one
**at a given `n`** — it is why C5 crosses and C1/C2/C4 do not — and is **not** what
moves the frontier **across `n`**. Two different questions; I had predicted one answer
for both.

---

## 4. THE TRAP THIS TICKET WAS PHRASED INTO, MEASURED

**`u_M > 1` IS NOT AN EVENT.** A poset refutes the disjunction iff `u_F > 1` **and**
`u_M > 1`. Bare `u_M` exceeds 1 at **4 primitive posets by `n = 7`**, exhaustively (`b0`
W3 reproduces mg-c50b's count), and `(F)` **holds** at every one of them. `b2` arm B2.4
runs the same climb on bare `u_M`:

| n | bare u_M reached | u_F there | (F) fails? | refutes disjunction? |
|---|---|---|---|---|
| 9 | 1.037356 | 0.573280 | no | **no** |
| 10 | 1.201460 | 0.534588 | no | **no** |
| 12 | 1.128873 | 0.558282 | no | **no** |

A hill climb pointed at bare `u_M` reports `1.20` on day one and it means nothing. Every
figure in this tree is `min(u_F, u_M)` or is labelled as a component of it.

---

## 5. WHAT MAKES THE VERDICTS MEAN SOMETHING

**THE DIRECTIONS ARE OPPOSITE FOR THE TWO CLAIMS.** mg-5cba certified `(M♯) HOLDS` at
C1–C4 with `μ` from **above** and `γ` from **below**. Certifying `(M♯) FAILS` needs `μ`
from **below** and `γ` from **above** — and `μ` from below is the hard direction, which
no exhibited monotone vector can produce. It needs exact **copositivity** of
`b·n·QI − 2·LE·a·NI`. That is the trap mg-51f4 named, and it is why nothing here is
claimed from a float.

**THREE STAGES, AND EACH IS ONLY ALLOWED TO ERR ONE WAY.**

| stage | μ from | direction of error | may be quoted? |
|---|---|---|---|
| 1 screen (`lib789d.mu_ub_float`) | above | **over**-states `u_M` — cannot lose a counterexample | **no** |
| 2 float (`lib5cba.mu_pref_float`) | exhaustive over all `2^(n-1)` faces | float error only | as a float |
| 3 exact (`lib5cba` PSD + copositivity) | below, on integers | none | **yes** |

`b0` S3 checks the screen's direction at 4376 primitive posets of `n ≤ 6` in **both**
directions — `min` as well as `max` of `mu_ub − mu_exact` — because mg-789d's own D1 was
a one-sided control read as two-sided. Min `−1.0e-15`, max `+3.4e-05`.

**PLANTED WORLDS (`b0` S4/S5).** C1 must be **refused** by the FAILS certifier and is;
C5 must fire and does; the four `n = 7` posets with `u_M > 1` must **not** be called
counterexamples and are not; a non-primitive input gets `NOT PRIMITIVE`; a poset with
`Δ² ≤ 2γ` reads `u_M = 0` and not `+inf`. A deliberately-too-high `m_lo` and a
deliberately-too-low `g_ub` are fed in and **must** come back refused — because
`lib5cba.mu_bracket` only ever *raises* its low end, so a certificate that inherits the
bracket's seed is a float wearing a Fraction's clothes. Every certificate in this tree
re-asserts `mu_ge(m_lo)` and `gamma_ge(g_ub) is False` as standalone calls.

**AN INDEPENDENT PATH TO THE SAME CONCLUSION (`b1` B1.3).** The whole C5 verdict is
re-derived from mg-5cba's **published decimals alone**, touching no code of mine.
pm-onethird reproduced it by hand to seven significant figures. **It narrows step (iii)
only** — it establishes that *if* those two bounds hold then `(M♯)` fails, and both
bounds are `lib5cba` outputs. That is why mg-5e82 exists and why its budget belongs on
the copositivity decision.

---

## 6. THE BLANK-CELL DEFECT, REMEDIED AS A MECHANISM

pm-onethird's request after the finding: *"make a blank cell impossible or make it
loud."*

`libb417.emit_table` **refuses** any cell rendering as `''`, `' '`, `'-'`, `'--'`,
`'---'`, `'—'` or `'–'`, and refuses a short row, because a missing cell is a blank cell.
A value that was not computed must go through `cell(None)` and prints **`NOT-COMPUTED`**;
one that is genuinely inapplicable must be `cell(None, na_reason=...)` and prints
**`N/A-<reason>`** — the reason is not optional. `b0` arm S8 plants all six blank
renderings and requires all six refused. The five-row `u_M` table in `b1` is emitted
through it, so **the table that replaces mg-5cba's is structurally incapable of carrying
the defect it replaces**.

**AND MY OWN FIRST DRAFT CARRIED THE DEFECT.** `b3`'s frontier table printed `-` in the
`u_F` and `u_M` columns for the exhaustive `n ≤ 7` rows — the remedy exhibiting the
defect it remedies, inside the file reporting the defect. Those cells now read
`N/A-mg-c50b-published-min-only` (mg-c50b publishes one number per `n`, not the argmax's
components) and `N/A-c_or-not-W` at `n = 8` (`c_or` and `W` are **different readings**
that cross 1 together — putting `0.943649` in a `W` column is the `u_M`/`c#` confusion
mg-0d1b named, in a new costume).

---

## 7. DEFECTS OF MY OWN, ALL KEPT

**D1. I PASTED `2·γ_ub` INTO A `γ_ub` SLOT AND READ `u_M ≥ 0.49`.** In my first
interactive certificate, minutes after finding the witness. It was caught because the
answer moved the *wrong way*, not because anything checked it — the exact failure mode
E5 was filed against in `PREDICTIONS.md` before the instrument existed, committed before
I made it. A confident number in the wrong direction is what a mis-paired bound produces,
and only knowing which way it *should* move caught it.

**D2. MY MOVE SET CONTAINED THE IDENTITY.** `neighbours` applied its `d2 != dn` guard to
the add and delete moves and **not** to the label transposition, so when the two swapped
labels are order-isomorphic in `P` the relabelling is the identity and a poset was
returned as a neighbour of itself — 2 of 209 over the five gap witnesses. **The search
was unaffected**, and that is the point rather than the excuse: the climb accepts a move
only on `> cur + eps`, so a self-neighbour can never be selected, which is exactly why it
survived to be found by a control rather than by the search. Fixed, kept in the file with
its reasoning, and `b2` re-run so the committed transcript matches the committed code.

**D3. THE `u_M`/`c#` SPLIT IS LIVE IN MY OWN OUTPUT.** `b4`'s certified column is
`min(c#, f*)` and `b2`'s is `min(u_F, u_M)`; they are **two readings of one event** and
are **not equal** (mg-0d1b), so `b4` prints certified figures both above and below the
float `J` of the same poset. Both columns are printed at every row rather than one being
quoted and the other named.

**D4. I RAN THE `n = 7` EXHAUSTIVE SWEEP TWICE BEFORE NOTICING.** W3 and S6 each swept
86278 primitive posets with a `2^6`-face `μ_pref` at every one. Merged into one pass —
eleven minutes that were being spent proving a loop is deterministic.

**D5. THREE IMPLEMENTATIONS AGREEING IS NOT THREE INDEPENDENT DERIVATIONS.** `Δ`, `M`
and `LE` at C5 reproduce across `lib5cba`, `lib789d` and `libc50b`, and I checked that
before mailing. All three descend from the same reading of the same transport DP. It is
reported as corroboration and it is not independence; mg-5e82 is asked to re-derive the
DP from the definition.

**D6. MY RESTART BUDGET FALLS WHERE MY VALUES RISE.** 30 restarts at `n = 9` down to 8 at
`n = 14`. A rising sequence measured with a shrinking instrument cannot separate "`W`
grows" from "my search got luckier where it looked harder" — except that here the budget
falls where the values rise, which makes the rise *harder* to explain away, not easier.
That is an argument and not a proof, and `b3` §B3.4 says so in the output.

**D7. THE `(L*)`-GAP "POPULATION" IS FIVE POSETS.** Every distributional statement about
it is over ≤ 5 observations and carries its count.

---

## 8. PREDICTIONS, SCORED

Filed in `PREDICTIONS.md` at `e1b7a47`, before one line of the instrument existed, with
the dispatch-sized exposure (H1: **I had already certified the `n = 12` witness**)
disclosed rather than laundered. Nothing below bets on H1.

| # | prediction | p | outcome |
|---|---|---|---|
| P1 | a certified counterexample below `n = 12` | 0.65 | **HIT** — certified at `n = 10` and `n = 11` |
| P2 | `n = 9` specifically yields one | 0.30 | **MISS, and correctly priced low** — 30 restarts topped at 0.969347 |
| P3 | search max monotone non-decreasing over `9..14` | 0.55 | **HIT** — 0.969 / 1.001 / 1.028 / 1.044 / 1.058 / 1.068, no dip |
| P4 | the winning direction is small `μ_pref` | 0.75 | **HIT AS STATED, REFUTED AS MEANT** — champions' `μ ≈ 0.056–0.068` vs the gap median 0.120, so the literal claim holds; but the *trend* is carried entirely by `v_L`, with `D` flat. See §3 |
| P5 | `n = 14` exceeds 1.023414 by ≥ 0.02 | 0.50 | **HIT** — 1.070221, `+0.047` |
| P6 | at least one screened champion fails to certify | 0.60 | **MISS** — 0 refusals in 36. The screen was **tight** at every champion (inflation ≤ 1.8e-4), so the two-stage design bought less than I expected. It is still what licenses the claim, and I would run it again |
| P7 | the free `u_M` argmax always has `u_F < 1` | 0.70 | **HIT** — `u_F = 0.573 / 0.535 / 0.558` at `n = 9 / 10 / 12` |
| P8 | champions at `n = 12..14` have height 4 | 0.60 | **MISS** — heights 5, and C5 itself is height 5, not the 4 the other four counterexamples share |

**5 of 8.** The two misses I care about are P6 and P8, because both were bets that this
region looks like the region the corpus already knew, and both say it does not.

---

## 9. WHAT WAS NOT DONE

- **`n = 8` IS NOT ENUMERATED.** Barred by the ticket; nothing here needs it. The one
  `n = 8` poset that appears is mg-5cba's search argmax, run as a **negative control**
  (`(L*)` holds there, the FAILS certifier refuses, `(M♯)` certifies in its own
  direction).
- **`STATE.md` IS NOT EDITED**, at pm-onethird's instruction. The three clauses that go
  if mg-5e82 confirms are recorded in that ticket and are, at `STATE.md:172`:
  *"AND THE DISJUNCTION SURVIVES IT"*; *"`(M♯)` HOLDS at **4 of 4**, `u_M = 0.943486 /
  0.947534 / 0.981830 / 0.958326`"*; and *"What is lost is exactly one thing: the
  uniform-in-`n` proof."* **Nothing else in that row moves.** `STATE.md` also stands at
  **exactly 19,077 words**, exactly mg-e331's ceiling, so the correction requires raising
  it in the same commit under mg-e331's documented procedure — the ratchet binding on its
  first real test.
- **NO ATTEMPT TO RESURRECT `(L*)`.** The depth table measured that door shut.
- **NO CLAIM ABOUT `C₃`.**
- **A FOURTH SITE FLAGGED AND NOT TOUCHED.** `STATE.md:172` says the gap between `(L*)`
  and `(M♯)` is *exactly `μ_pref²`*. In the normalisation that row itself uses
  (`μΔ ≤ γ`) the gap is `μ_pref²/2`; it is `μ_pref²` in the doubled form
  `2μΔ ≤ 2γ`. Both conventions are live in the corpus. It changes no verdict, it is
  **not claimed as an error**, and it is in mg-5e82 as a normalisation to settle first —
  with one reason it matters beyond this row: a factor of 2 between two live conventions
  is indistinguishable, to mg-06d1's alias agreement check, from a genuine disagreement
  between two implementations.

---

## 10. FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed at `e1b7a47`, before the instrument existed |
| `libb417.py` | the objective, the identity, the exact certifier, the move set, the blank-refusing emitter |
| `b0_selftest.py` | S1–S8. **Nothing downstream may be believed until this passes.** ~20 min |
| `b1_witness.py` | the certificate at all five `(L*)` counterexamples, the `u_M` column whole, and the derivation from published decimals alone |
| `b2_climb.py` | the search, `n = 9..14`, every restart reported, plus the bare-`u_M` control |
| `b3_trend.py` | the trend, the multiplicative decomposition, and what the data does **not** distinguish |
| `b4_certify.py` | every champion decided on integers; refusals counted either way |
| `champions.json` | the handoff from `b2` to `b3`/`b4` |
| `run_all.sh` | `b0 → b1 → b2 → b3 → b4`. Order matters: `b2` writes `champions.json`. |
