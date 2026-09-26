# KSBFT-P1 — every walled route, revisited under bounded range: the killing obstructions dissolve exactly where they never mattered

`mg-0b78`, 2026-09-26. This generalises mg-b447's question (`docs/KSBFT-F-L4-step6-under-bounded-range.md`,
audited `docs/AUDIT-mg-b447.md`) from L4/Step 6 to **every route the programme walled**. Daniel, 2026-09-26:
*"could bounded range make any of our many previous attempted arguments work"*. **Nothing in `STATE.md`
was edited, and no ticket was closed or re-opened. Every verdict below is a recommendation to pm-onethird.**

Marks:

- **PROVEN**: the proof is in this document and is elementary. **PROVEN (cond.)** means proven from
  **H** (a counterexample has range `π(P) ≤ L*`, conditional on AK25a/AK25b/Haq26; KSBFT-C §1.1). A
  statement proven for the class `Π_D = {P : π(P) ≤ D}` with `D` free is unconditional.
- **PROVEN (cited)**: the proof is in the cited audited document, and I re-read the step I use.
- **EMPIRICAL**: comes with its instrument and range. It proves nothing beyond that range.
- **CONJECTURED**: a belief or a proposed statement.

**Computation was used only as an instrument** (ticket rule): to *compute* the range of each witness
instead of guessing it, and as one counterexample probe in §5. Nothing was extended. Instrument:
`code/ksbft_p1_walled_0b78/` (`sh run_all.sh`, about 15 s, one process, exact arithmetic, seeded).

---

## 0. Verdict

> **1. The triage (§2: 48 table rows, split into 54 verdict entries).** Of the obstructions that killed walled routes:
> **14 DISSOLVE**, **8 are TRANSFORMED**, and **24 SURVIVE**. Of the remaining entries, 6 are not
> obstructions (corrections, a GREEN dictionary, an operational DROP) and 2 were not examined.
> - Every **DISSOLVES** is an obstruction whose witness has range `Θ(n)`. It lives in the wide,
>   dense, large-antichain or `Θ(n)`-mobility regime, exactly as the ticket predicted. The witnesses
>   are `C_n ⊔ C_n` (range `n`), `C_m ⊔ C_1` (range `m`), `C_p ⊔ A_q`, the antichain, the staircase
>   (range `n/2`), `D_k` (range `2k−2`), `C_2 ⊕ A_k ⊕ C_2` with `k = √n`, and the abstract two-atom
>   law and flat-long block-cross, whose realisations need range `Θ(n)`. All ranges were computed.
> - Every **SURVIVES** is either **structural** or witnessed at **range ≤ 3**, or by a **finite** poset.
>   Structural means the failure holds for every poset: the whole F-series, the compression
>   separators, the logical probes. The range-≤ 3 witnesses are `Z_n`, `(2+1)` and its ordinal sums,
>   `C_2 ⊔ C_2`, the fence, `W*`, and the mg-131e `n = 6` LP poset. The finite witnesses are the
>   `(L*)` and `(F)&(M♯)` refuters, which have ranges 5–9 and were computed here.
>
> **2. The pattern, which is the main finding (§3).** **Bounded range dissolves an obstruction exactly
> when the route it killed was aimed at one of seven "spread" quantities.** These are inversions,
> displacement, `Var(pos)`, incomparability density, `log e(P)`, slot-law support and flip
> probability. **Range bounds every one of the seven pointwise by a function of `D`** (Prop 3.1,
> PROVEN). So every DISSOLVED route's own target is **supplied by the standing facts** in existence
> form, at a constant `f(D)`. It stays exactly as open as before at the D-free constants the route
> needed (`ε_dem ≈ 1/50`, mg-5987's `C < 0.30`). **The routes aimed at δ itself died on thin
> witnesses (range ≤ 3) or on structural failures. Bounded range cannot touch either.** The reason
> is that H and the δ-extremal family point at the same thin region (§3.2). Put in one line:
> **H removes the part of poset space where the programme's intermediate quantities were hard, and
> the hard cases for δ were never there.**
>
> **3. What the revived routes now need (§4).** For each of the 22 DISSOLVES / TRANSFORMED rows, one
> proposition. **The standing facts F1–F7, Lemma 2.3 and Lemma W supply all but three of them in
> existence form, and none at the constant the route needed.** The three that are not supplied are:
> (a) QD_D (§5; rows A11/A12); (b) the width-3 Route-B Hyp-A inequality, which fails at every γ
> anyway; (c) the (MC_D)-equivalent forms (T)/(IB). mg-c3ca's two-element lemma (D2) was not examined.
>
> **4. Deep dive (§5): the Stanley-stability route (mg-a1ec → mg-48ab → mg-dcae), chosen by
> elimination.** It is the only DISSOLVED route that has a **δ-direct consumer**: mg-48ab's Theorem
> 5.2, *a full-support flat position law forces `δ ≥ 1/3`*. Its killing witness `C_n ⊔ C_n` has
> range `n`. The revived statement is:
> > **(QD_D) — quantised Stanley deficit.** There is `κ(D) > 0` such that for every `P ∈ Π_D`,
> > every `x` and every interior slot `i`: `N_i² > N_{i−1}N_{i+1}` implies
> > `N_i² ≥ (1+κ(D))·N_{i−1}N_{i+1}`.
>
> - **(QD_D) ⟹ (FLAT_D)** (Prop 5.4, PROVEN given Ma–Shenfeld k = 1 and mg-48ab Thm 5.2): no counterexample in `Π_D` has an
>   element whose position law, over a window of ≥ 3 slots, is within factor `1+κ(D)` of log-linear.
> - **Sharpness (PROVEN, closed form):** `κ(D) ≤ 1/(D²−1)`, from `C_2 ⊔ C_D`. An exhibited
>   range-4 poset gives `κ(4) ≤ 1/18`. So no D-uniform constant exists.
> - **Evidence (EMPIRICAL):** at fixed `D ∈ {2,3,4}` the least strict deficit is flat in `n` up to
>   `n = 16`: 1/3, 1/8, 1/15 (1/18 once).
> - **Proof attempt:** a finite local decomposition (Lemma 5.1) and weight quantisation (Lemma 5.2)
>   are PROVEN. Together they reduce (QD_D) to finitely many continuous functions on a compact box
>   (Prop 5.6).
> - **It stops at a precise obstruction (§5.5):** the closure of the realised boundary weights.
>   Strictness at *limit* points needs a Ma–Shenfeld theorem for posets with a boundary measure.
>   Positive reweighting does not preserve Stanley's inequality (Ex. 5.7, PROVEN). The one mechanism
>   by which bounded range quantises, an injection counting a positive event, does not apply to the
>   Stanley defect, which is a difference of products.
> - **Even proven, (FLAT_D) is a necessary condition on counterexamples, not (MC_D)** (§5.6).
>
> **Net.** Bounded range does not make any previously walled route work. It moves no link of the
> spectral chain beyond what KSBFT-C/F already recorded, and it revives no δ-direct route past a
> constant or a structural wall. **(MC_D) remains the whole content** (KSBFT-F §8), and the only δ-level
> tools that bounded range genuinely supplies are the *quantisation* lemmas: Lemma 3.1, Lemma 2.3,
> Lemma W, `d₁ ≥ 1/(D+1)`, Lemma R. §3.3 states the reason those help, and where they stop.

---

## 1. What "the obstruction survives" means here

A route died on an obstruction. The ticket classifies each against **H**: restrict to `Π_D`.

- **SURVIVES**: the obstruction still holds on `Π_D` for every `D ≥ D₀`, with a small `D₀`. It
  does so because
  - its witness has range bounded independently of `n` (computed, not guessed), or
  - it is finite, or
  - the obstruction is **structural**: a statement true for every poset, which restriction cannot
    change.

  Every structural obstruction survives by a one-line argument. If `Q(P)` fails for every `P`, it
  fails for every `P ∈ Π_D`.
- **DISSOLVES**: every witness needs range `→ ∞`, **or** the failing hypothesis becomes true on
  `Π_D`.
- **TRANSFORMED**: H turns the obstruction or the route's need into a different statement. That
  statement is often "the same thing at a D-dependent constant", and sometimes it is "the conjecture
  on `Π_D`".

**Abstract witnesses** (a law on permutations, a sequence, an LP point) have no range. I record the
range any **realisation** would need. For example, a law giving `Θ(n²)` inversions needs `Θ(n²)`
incomparable pairs, hence range `Θ(n)` by F3.

**A finite witness** has bounded range trivially. It refutes the universal statement on `Π_D` for
`D ≥ π(witness)`. It does **not** refute the statement restricted to `{7 ≤ π ≤ D}`, where a
counterexample must live by BW92 and Pec08 (cited, not verified). mg-b447 closed that gap for `W*` by
padding it to `W*_t` (every range window). **I did not look for paddings of the finite witnesses
below**, and I flag each such row "window [7,D] NOT EXAMINED".

**Regime flags** (the ticket asks for them): **W** wide, **Dn** dense, **AC** large antichain,
**Var** unbounded variance or `Θ(n)` mobility, **—** none.

---

## 2. The triage table

Ranges marked `†` were computed by `ranges.py` / `ranges2.py` (transcripts `out_ranges*.txt`), and the
growth law was then proved by hand. For example:

- `C_m ⊔ C_n` has range `max(m,n)`, because the bottom of one chain is incomparable to the whole
  other chain and to nothing else.
- The staircase has range `m`, because `e_{m−1}` is incomparable to `o_0 … o_{m−1}`.
- `D_k` has range `2k−2`.
- `C_2 ⊕ A_k ⊕ C_2` has range `k−1`.

"Target under H" says what happened to the thing the route was trying to prove. **auto** means the
target is supplied in existence form by F1–F7 (KSBFT-C §1.2) at a constant depending on `D`. **moot**
means the target dropped off the route (KSBFT-F §8).

### 2A. The attempt index (`docs/state-history/attempt-index.md`, 28 rows)

| # | route | obstruction that killed it | witness family → **range** | flag | verdict | target under H |
|---|---|---|---|---|---|---|
| A1 | width ≥ 4, `n ≥ 10` gap (mg-c47a DROP) | tractability only (operational) | none | — | *not an obstruction*. KSBFT-C row 13‴ already repriced it as on-route | — |
| A2 | low-δ ⟺ bounded width (mg-c47a 3.1) | none (PROVEN, kept) | — | — | *not walled* | — |
| A3 | C.md §9.5 correction | — | — | — | *not a route* | — |
| A4 | Bruhat-convexity "prefix ⟹ `O(n)` inversions" | collapses to Diaconis–Graham, `Σ K_m ≤ inv_e ≤ 2Σ K_m`: a reduction, not a counterexample | none | — | **DISSOLVES** (the target becomes true) | **auto**: `E inv_e < nD/6` for frozen `P` (F4) |
| A5 | balance → `log e(P)` → δ (Kahn–Saks/KL) | the convex relaxation's feasible set contains every δ in `[C_BFT, 1/2]` (mg-a1ec Prop 3.2). Extremal: geometric `N_i = C r^i`, `r = 1/φ` (abstract) | realised by the **Fibonacci centre pair**, `δ_centre → C_BFT` (KSBFT-A §5): `Z_n`, **range 2**† | — | **SURVIVES** at 1/3. **TRANSFORMED** below it by KSBFT Thm 1.3″: `δ > 0.2764` for `D ≤ 3471` | δ-direct |
| A6 | entropy/order-polytope → conditional inversion sum (untried) | none recorded. Deliverable: the bridge `log e(P) → E[inv_e]` | — | — | **TRANSFORMED**: both ends are bounded by range separately (F4, F6), so the bridge is not needed for existence | auto |
| A7 | convexity forbids the flat slot law | silent on the **approximate flat tail**: `x` beside a length-`Θ(n)` chain, `Θ(1)` mass at the far slot (abstract) | a slot law with mass at slot `p` needs `π(x) ≥ p`, so **range `Θ(n)`** (F1) | **Var** | **DISSOLVES** | auto (`(B)` with constant `D`, F5) |
| A8 | slot-law log-concavity of `e(P_m)` | numerically false (7 537/68 156). Smallest vector `[1,2,6]` at `n = 5` | finite, `n ≤ 7`, so range `≤ 6` | — | **SURVIVES** as a false statement (irrelevant: gap sequence, not Stanley's) | — |
| A9 | incomparability-graph conductance; "primitive ⟹ good mixer" | refuted: primitives reach `λ_std ≈ 0.96` at `n ≤ 9` (ensemble, no named poset) | finite, range `≤ 8` | — | **SURVIVES, and H makes it worse**: on `Π_D`, `1 − λ_std ≤ 4nD/(n²−1) → 0` (KSBFT-F Prop 5.1), so **every** large range-`D` poset mixes badly | moot |
| A10 | mg-a1ec entropy discontinuity; "AF saturated" | the fatal flat law and the KL optimum both lie on Stanley's equality locus. The fatal law has `L_x = Θ(n)` | flat-long block-cross, **range `Θ(n)`**. KL optimum abstract (A5). `tight3` range 2† | **Var** | **DISSOLVES** for the fatal law. The KL half **SURVIVES** (A5) | auto |
| A11 | mg-48ab AF equality case (Window Rigidity, **Thm 5.2**) | Ma–Shenfeld is qualitative, and the threat is laws with ratios `1 − 1/n` | abstract. A ratio-`1−1/n` run over `Θ(n)` slots needs **range `Θ(n)`** (F1) | **Var** | **TRANSFORMED** into (QD_D). **Deep dive, §5** | δ-direct via Thm 5.2 |
| A12 | mg-dcae k = 1 Stanley stability | `c ≤ 2/(2n−1) → 0` on `C_n ⊔ C_n` at `x = u₁` (control reproduced exactly†). Then `(B-cov)` is wrong-signed (FKG) | `C_n ⊔ C_n`: **range `n`**† | **W**, **Var** (`δ = 1/2`) | **DISSOLVES** (stability). `(B-cov)` **MOOT** (`(B)` auto) | auto / §5 |
| A13 | probe A, mg-61bb, coherence | subadditivity `β(u,w) ≤ β(u,v)+β(v,w)` is a system of upper bounds, so it forces no lower bound. Witness: `β ≡ 10⁻¹⁰⁰` (abstract) | abstract. Chains are trivial | — | **TRANSFORMED**: on `Π_D`, `β ≥ c(D) ≥ 2^{1−2D}` (KSBFT-F Lemma 2.3), so the constant witness is excluded below `c(D)`. **SURVIVES** at 1/3 | δ-direct |
| A14 | probe B, mg-92e6, diagonal capacity | the marginal-only ceiling is `≤ 1/spread`, so it dies once the spread is ≥ 4. Witness: uniform marginals on a common window, cyclic couplings (abstract) | spread 4 is realised by `x` with 3 incomparables: **range 3** | — | **SURVIVES** | δ-direct |
| A15 | probe C, mg-f82f, free slots | `δ ≥ (1−1/e)/s` is `≤ 1/s`, so it dies at `s ≥ 4`. Witnesses: `n = 6`, δ = 1/3, `s = 4` (enumerated) | range `≤ 5`. **`Z_n` has `s = n−1` free slots at range 2**† | — | **SURVIVES** | δ-direct |
| A16 | probe D, mg-e2de, co-degree | best local bound `1/C(p+q,p)`: 1/6 at co-degree 2. `G` does not determine δ | `C_2 ⊔ C_2`: **range 2**†. `n = 6` pair A/B: **range 5**† (δ = 4/9 vs 1/2†) | — | **SURVIVES**. Also on `Π_D` the co-degree is `≤ D−1`, which does not help: the decay already bites at co-degree 2 | δ-direct |
| A17 | mg-210d, constant bound on `λ_std` | best constant 0. Equality at the antichain; `d ≤ 1` degenerates. Residual (R): a frozen density ceiling | antichain, **range `n−1`**†; tree `G`; `G(n,g)` range `2g−2`† (calibration) | **Dn**, **AC** | **DISSOLVES**. (R) auto: `d ≤ D/(n−1)` (F3) | auto |
| A18 | mg-a58f, (B-bias) locality | the lemma implies LIB, which is the wall. Loss: `m_z = Θ(n)` | `W_m = C_m ⊔ C_1`: **range `m`**†. `C_p ⊕ A_k ⊕ C_p`, `k = √n`: **range `k−1`**†. Two-atom law (density 1) | **Var**, **AC** | **DISSOLVES**. (B-bias) auto: `Σ_{y∥x} P[flip] ≤ π(x)`, `< π(x)/3` if frozen | auto |
| A19 | mg-88bd, operative `λ_std` form | branch (iii) gives no contradiction for any `F > 0`. Zero slack at `P₀` | `P₀ = (2+1)`: **range 2**† | — | **SURVIVES** (KSBFT-F) | moot |
| A20 | mg-63e3, Step 6 on branch (ii) | (T) fails at modulus `Ω(ε)` | `W`: **range 3** (KSBFT-F §3.1) | — | **SURVIVES** | moot → (MC_D) |
| A21 | mg-3af9, sub-linear modulus | (T) fails at every positive modulus | `W*`: range 3. `W*_t`: range `t+1` | — | **SURVIVES** in every window `[r,D]`, `r ≥ 3` (KSBFT-F Thm 4.1) | moot → (MC_D) |
| A22 | mg-345e, pair-bias independence | the route stops at the marginal/joint boundary. Ceiling attained by the two-atom law | two-atom law: density 1, so **range `Θ(n)`** | **Dn** | **DISSOLVES** (KSBFT-C §2.3) | auto (`ε_spec ≤ Dn/(n²−1)`) |
| A23 | mg-276d, intrinsic face geometry | none: an exact dictionary, "no bound, no new tool" | — | — | *not an obstruction* | — |
| A24 | mg-a3d4, Hodge side, **Thm G** | local-to-global bound off by `2^{Θ(n)}`: `γ_i ≥ 1/2` at every level | Thm G's witness is `A_n` (range `n−1`). **The loss persists on `C_a ⊔ C_a` (γ = 1/2, range `a`) and on the fence (γ₋₁ ≈ 0.46, "still decays geometrically", range 2†)** | (**AC**) | **SURVIVES**: not an antichain effect (row M3) | δ-adjacent (`λ₂(Δ_AT)`) |
| A25 | mg-200d/131e/00a1, per-slot adjacency LP | `ε_spec = 2/(n+1)` false at `n = 6`. LP value `Θ(n²)` | `n = 6` LP poset: **range 3**† (measure abstract; the poset has δ = 5/14†). **Staircase: range `n/2`**† | **Var** (staircase) | `n = 6` refutation **SURVIVES** (finite). **Θ(n²) DISSOLVES**: value `≤ nD/6` (KSBFT-C row 13″) | auto |
| A26 | mg-ba78, correction | — | — | — | *not a route* | — |
| A27 | mg-76b2, `C₃` → L2 | reduces to L2's first disjunct, which is false (2/126 at `n = 6`) | finite, range `≤ 5` (KSBFT-F §6) | — | **SURVIVES** | moot (L2 drops out, KSBFT-F §6) |
| A28 | mg-51f4 → c50b → 789d, `(L*)`, `(F)`, `(M♯)` | `(L*)` false at `n = 9`. `(F)` and `(M♯)` fail together from `n = 10` | **`(L*)`: n=9 ranges 8, 8; n=10: 6; n=11: 9.† `(F)&(M♯)`: n=10: 5, 5; n=11: 6; n=12: 7, 7†** (widths 3–6; all have δ ≥ 13/28†) | — | **SURVIVES** on `Π_D` for `D ≥ 5`. Window `[7,D]` NOT EXAMINED | moot (`C₃` feeds L2 and L1b's consumed content) |

### 2B. The F-series and Route B (sibling repo `one_third_width_three`)

| # | route | obstruction | witness | flag | verdict |
|---|---|---|---|---|---|
| B1 | Route A, chamber-Morse (F23/F24) | no `n`-uniform rule for the critical cells `c*_n` of `Δ(PPF_n)`: "HPC-per-n" (F23:154) | none: cells of the complex of **all** posets on `[n]` | — | **SURVIVES** (structural). *Observation, PROVEN:* `{π ≤ D} ∩ PPF_n` is an **up-set** under refinement, because adding relations cannot increase any `π(x)`. A Π_D-restricted Route A would need the sphere theorem on that up-set's order complex. **NOT EXAMINED** |
| B2 | Route B, Hyp A (F25/F27) | `(c₅*)²γ³ ≥ 512w²/c₆` fails on the **whole** window: `γ_crit ≈ 27–936 ≫ 1/3` (F25:222–238). The `1/γ` comes from the window-removal perturbation `2|W|/(|X|−|W|+1) < γ/2` | none. Hypothetical deep layered width-3 γ-counterexamples | — | **TRANSFORMED, then SURVIVES.** On `Π_D`, every incomparable pair has `min(p,1−p) ≥ c(D)` (KSBFT-F Lemma 2.3), so the small-γ tail `γ < c(D)` is **empty**. But Hyp A fails at every `γ ≤ 1/2` on its constants alone, so emptying the tail changes nothing |
| B3 | hybrid spectral → cohomology (F27) | no comparison map between the links of `Δ(PPF_n)` and `G_BK(P)`: "different complexes on different vertex sets" | none | — | **SURVIVES** (structural) |
| B4 | sheaf cohomology on POSET (F28) | no candidate `F_BK` is both functorial under refinement and has a canonical map to `F_ℓ` | none | — | **SURVIVES** (structural; see B1's up-set remark) |
| B5 | Čech-bias F29 → F30 → F31 | `K_chain-loc ⊆ ker Φ_*`, so `c_BC(P) = 0` **for every P** for formal reasons (sgn-orbit sum + `H^{n−2}_triv = 0`) | none. F30 §3.5's "generic `n = 4` example" is vacuous, and its "≤ 3 incomparable pairs" is false (sub-agent report, not re-checked) | — | **SURVIVES** (structural, uniform in `P`) |
| B6 | Lean axiom `case3Witness_hasBalancedPair_outOfScope` | a finite-per-`w` enumeration gap (`card ≤ 6w+6`, `K ≤ 2w+2`) | a finite class per `w` | — | **NOT EXAMINED** beyond KSBFT-C §2.9: the slice does not obviously bound `π` below |

### 2C. The compression / code-length line

| # | route | obstruction | witness → range | flag | verdict |
|---|---|---|---|---|---|
| C1 | `compression2` (mg-0fc6) | vacuous below `n = 16 777 063`. **Realizability-blind**: everything is a function of the pair marginals | vacuity: the antichain (range `n−1`). Blindness: `μ₁` vs `μ₂`, same marginals, max flip 1/3. The realised one is `V ⊕ V` (my inference from `e = 9`), **range 2**† | **AC** | vacuity **TRANSFORMED** (KSBFT-C §2.8: `log₂ e ≤ n log₂(D+1)`). Blindness **SURVIVES** (range 2) |
| C2 | subset separators (mg-99f4) | separation and consumability live on disjoint parts of the domain: "provably zero" | `S = {id, rev}` at `n = 3` (abstract) | — | **SURVIVES** (structural) |
| C3 | L* code (mg-9d9e) | the L* tape **is** the free code. No shape-B bound `log₂ e ≤ c·log₂ n!`, `c < 1`, at every `P`. "Dense means wide" | antichain, **range `n−1`**. Kraft leak `{1<3, 2<0}` range 2† (not an obstruction) | **AC**, **Dn** | **DISSOLVES**: on `Π_D`, `log₂ e ≤ n log₂(D+1) ≤ c·log₂ n!` once `n ≳ (D+1)^{1/c}`. "Dense means wide" REFUTED (KSBFT-C) |
| C4 | mg-872c (predictions only) | P6/P7/P10: no shape-A contradiction. The frozen class is empty | boundary class `V^{⊕k} ⊕` chain: **range 2**† | — | question **answered (cond.)** by KSBFT-C §2.8 (`Θ(n)` from range). Mechanism unchanged |
| C5 | W4 rate / k-foliation (mg-409a, mg-8d66) | `α(P) ≤ 1` for **every** poset, attained, against a bar of 2–3 | attained on `Z_n` (ordinal sums of 2-antichains), **range 2**†, and on `A_n` | — | **SURVIVES** (universal operator bound, attained at range 2) |
| C6 | energy-identity consumers (mg-145f) | no consumer: the numerator is sign- and level-blind, and its share of `(B)` is `Θ(n⁻²)` | antichain, `Σ A_xy = n−1` | **AC** | **DISSOLVES** in part. Its intended use (certify `d ≤ D < 1`) is auto (F3). "No consumer" SURVIVES |
| C7 | linear standard eigenfunction (mg-bb60), novelty (mg-623a) | documentary (the claim is absent); duplicates Wilson | `n = 5` argmax: **range 3**† | — | *not obstructions of this kind* |

### 2D. The entropy → L1b line (beyond A6–A12)

| # | route | obstruction | witness → range | flag | verdict |
|---|---|---|---|---|---|
| D1 | LIB-weak (mg-c3ca, audit mg-c4f5) | quantifier: "no `N₀` works for the class". Violators need `Θ(n)` elements of macroscopic mass | block-cross; `C_p ⊔ A_q`: **range `≥ p`**† (`Θ(n²)` inversions) | **W**, **Var** | **DISSOLVES**: H supplies the rate (KSBFT-C §2.5) |
| D2 | c3ca's missing two-element lemma | "incomparable elements with near-identical position laws are near-balanced" | not given | — | **NOT EXAMINED.** Note: it is δ-direct, so if true it is on the critical side of §3. The need is recorded in §4 |
| D3 | mg-0e8c L1b restatement | the open content is the ~50× between `ε_sup` and `ε_dem` in the **dense** regime; `trace T_P ≥ 1` gap | antichain (equality) | **Dn** | **DISSOLVES**: inverted by KSBFT-C §2.2 |

### 2E. The spectral / near-ordinal-sum architecture (all but three rows are in KSBFT-F)

| # | route | obstruction | witness → range | verdict |
|---|---|---|---|---|
| E1 | L1b (row 8), L2 (row 9), L3 (row 10), row 3b, L4 (row 11), Step 6 | see KSBFT-F §0 table | `W*` 3, N-poset 2, fence 2†, finite `n ≤ 7` | as KSBFT-F: L1b/L2/L3 auto, L4 PROVEN-and-empty, Step 6 **SURVIVES**, 3b off-route |
| E2 | absent step (T) (mg-7ae5) | "a density restriction changes what is refuted, not what is absent" | refuting family for the **surrogate** `U_either`: chain + isolated `z`, **range `n−1`**† (`d = 2/n`) | the surrogate witness **DISSOLVES**, but (T) itself is **TRANSFORMED into the conjecture on `Π_D`** (KSBFT-F Prop 4.2) |
| E3 | primitivity objection (mg-f5be), lever shape/test (mg-9b6b, mg-5987), boundary ε (mg-6ff4), frozen density (mg-0b96), chain IV (mg-81ff) | `α ≤ 1` universal (fence argmax **range 2**†). Density lever false at 63 orders (`V`-family, **range 2**†). The cap family `Z_n` (**range 2**†). The boundary class (**range 2**†). The density ceiling is the conjecture by contraposition. `D_k` refuters out of regime | ranges 2, 2, 2, 2, —, `D_k`: **range `2k−2`**† | f5be, 9b6b, 5987, 6ff4: **SURVIVE**. 0b96: the ceiling is **auto** past `L*/D` and "no lever at computable `n`" survives (KSBFT-C §2.7). 81ff: **DISSOLVES** (moot) |
| E4 | realizability-image rows (mg-3da1, c776, 8748, 8b32), cyclic bias (7c32), adjacent triples (7c78), chain selection (9461) | realizability vacuous at `M_n`'s vertices; `conv(R_n)` has no inequality form; a pigeonhole fact; "Step 4 is the conjecture"; Step 6 consumes no chain | two-atom vertex (abstract, density 1); `n = 6`, `e = 9` pair (`V ⊕ V`, range 2†); none | 3da1/c776: **TRANSFORMED**, since H is a realizability fact that cuts `M_n` to `d ≤ D/(n−1)` (KSBFT-C §2.3), but only at range scale. 8748/8b32/7c32/7c78/9461: **SURVIVE** (range 2 or logical) |

**Counts.**

| verdict | rows |
|---|---|
| **DISSOLVES** (14) | A4, A7, A10 (fatal-law half), A12, A17, A18, A22, A25 (`Θ(n²)` half), C3, C6 (use half), D1, D3, E2 (surrogate), E3 (81ff) |
| **TRANSFORMED** (8) | A5 (below 1/3), A6, A11, A13, B2, C1 (vacuity), C4, E4 (3da1/c776) |
| **SURVIVES** (24) | A5 (at 1/3), A8, A9, A14, A15, A16, A19, A20, A21, A24, A25 (`n = 6`), A27, A28, B1, B3, B4, B5, C1 (blindness), C2, C5, C6 ("no consumer"), E1 (Step 6), E3 (f5be/9b6b/5987/6ff4), E4 (8748/8b32/7c32/7c78/9461) |
| not obstructions (6) | A1, A2, A3, A23, A26, C7 |
| not examined (2) | B6, D2 |

Rows are split where one row carried two obstructions, so the counts are counts of obstructions, not
of table lines.

---

## 3. The pattern: dissolution is aligned with the target, not with the route's promise

### 3.1 Seven spread quantities, all bounded pointwise by range

> **Proposition 3.1 — PROVEN.** Let `P ∈ Π_D`, `x ∈ P`, `e` any linear extension, `σ` uniform on
> `L(P)`. Then, pointwise in every `σ` or as stated:
> 1. displacement `|σ(x) − e(x)| ≤ π(x) ≤ D` (F1);
> 2. `Var(pos_σ x) ≤ π(x)²/4 ≤ D²/4`;
> 3. `inv_e(σ) ≤ nD/2`, and `E inv_e < nD/6` if `P` is frozen with majority order `e` (F3, F4);
> 4. incomparability density `d ≤ D/(n−1)` (F3);
> 5. `log₂ e(P) ≤ n·log₂(D+1)` (F6);
> 6. the slot law of `x` is supported on **exactly** `π(x)+1` consecutive slots;
> 7. every flip has probability `≥ c(D) ≥ 2^{1−2D}` (KSBFT-F Lemma 2.3).

*Proof.* Items 1, 3, 4, 5 and 7 are the audited KSBFT-C F1/F3/F4/F6 and KSBFT-F Lemma 2.3.

**Item 2.** By F1, `pos_σ x` takes values in an interval of `π(x)+1` integers. A random variable
supported on an interval of length `L = π(x)` has variance `≤ L²/4`.

**Item 6.** Support within the window is F1. Now show the support is the whole window.

- By F1's attainment argument, both endpoints `d(x)+1` and `d(x)+1+π(x)` occur.
- `N_i(x)` is log-concave (Stanley). A log-concave sequence has no internal zeros.

□

**Observation 3.1′ (PROVEN by inspection of §2).** Every DISSOLVES row in §2 is killed by a witness
that makes one of the seven quantities large. The witnesses and the quantity each makes large:

- `C_n ⊔ C_n`: item 6's support.
- `C_m ⊔ C_1` and the block-crosser: items 1–2.
- The two-atom law, `C_p ⊔ A_q` and the staircase: item 3.
- The antichain: items 4–5.
- `D_k`: item 4.

**Every DISSOLVED route's own target is one of the seven being small.** The targets are (B), LIB,
(B-bias), (R), `ε_spec`, the code-length bound, (decay), and "the slot law must decay". So on
`Π_D` the target is **supplied**, at constant `f(D)`.

The quantifier matters. The routes needed these quantities small **at a D-free constant**:

- `ε_dem ≈ 1/50` for L1b;
- `C < 37/123` for `(EQ)` (mg-5987);
- `c < 1` for shape-B at computable `n`.

Prop 3.1 gives constants `D`, `D²/4`, `D/6`, `log₂(D+1)`. Every one is on the useless side once
`D ≥ 7`, where a counterexample must live (Pec08). **Revival here means "the target is true and
useless", the same state KSBFT-C found for L1b and KSBFT-F found for L4.**

### 3.2 Why the δ-direct routes are untouched

The routes aimed at δ itself (A5, A13–A16, A24, B1–B5, C1-blindness, C5, E3) died on:

- **thin witnesses:** `Z_n`, `(2+1)` and `V^{⊕k}`, `C_2 ⊔ C_2`, the fence, all range 2; `W*` and
  the `n = 6` LP poset, range 3;
- **finite posets:** A8, A9, A28;
- or on **structural** failures that hold at every poset: B1–B5, C2, C5, A13's logic.

**This is not an accident, and it is the conceptual content of the triage.** δ's extremal landscape
is thin:

- The only posets at δ = 1/3 are `(2+1)` and its ordinal sums (range 2). That is PROVEN for
  `n ≤ 11` by exhaustion (KSBFT-A).
- Every poset found with δ < 0.35 has width 2 (EMPIRICAL, KSBFT-A §6).
- The KS/KL barrier `C_BFT` is the limit of the Fibonacci centre pair (range 2).

An obstruction to proving `δ ≥ 1/3` must be a poset where the proof's inequality is tight or wrong.
The tight posets for δ are thin, so the obstructions are thin. **H cuts poset space from the wide
side**, and the programme's intermediate quantities were hard exactly on the wide side: inversions,
density, entropy, variance. These are the quantities a counterexample was feared to have in
abundance, the "open region is DENSE" premise that KSBFT-C §2.2 inverted. So H dissolved every
obstruction that lived there, and **those were precisely the obstructions to targets that were
never δ.** Everything else stayed.

*Status of §3.2:* the classification is PROVEN for the rows as listed (each range is computed and
proved). "Every future δ-direct obstruction will be thin" is **CONJECTURED**.

### 3.3 What bounded range genuinely supplies at the δ level: quantisation

Six results on the record use range as more than a spread bound:

- KSBFT Lemma 3.1;
- KSBFT-F Lemma 2.3 (`c(D)`);
- KSBFT-H Lemma W (`P[gap ≥ 2] ≥ p/(π_N+1)`);
- KSBFT-A §3.1 (`d₁ ≥ 1/(D+1)`);
- KSBFT-J Lemma R (reweighting by `w_v ∈ [1, π(v)+1]`);
- KSBFT-M's prefix certificate.

**Each is an injection whose fibres are bounded by the number of positions an element can hop.** That
number is bounded because a hop crosses only incomparables (F1). The common form:

> **(Q)** *a local event that is possible has probability `≥ c(D)`*, or *two local events' probabilities
> are within a factor `C(D)`*.

Quantisation is the only mechanism on the record that turns "approximately" into "exactly".

- If a quantity is either 0 or `≥ c(D)`, a hypothesis "it is `< c(D)`" forces it to be 0.
- KSBFT-F §8's last bullet says any locality proof of (MC_D) needs **exact** transport. Quantisation
  is how bounded range could supply exactness.

**The limit of (Q):** it quantises **probabilities of events**, i.e. positive counts. A quantity
that is a **difference** of counts is not quantised by an injection. That limit is exactly where the
deep dive stops (§5.5).

---

## 4. What each revived route now needs, as one proposition

"Supplied?" asks whether the standing facts (F1–F7, Lemma 2.3, Lemma W, the prefix certificate)
supply the proposition. **exist.** means supplied at a `D`-dependent constant. **useful** means
supplied at the constant the route needed.

| row | the single proposition the route now needs | supplied? |
|---|---|---|
| A4 | `E inv_e = O(n)` along prefixes on `Π_D` | exist. (F4). useful: no |
| A5 | the KL relaxation, restricted to sequences on `≤ D+1` slots **plus the end structure**, has min δ `≥ 1/3` | exist. below 1/3 (Thm 1.3″: `C_BFT + min(θ₀, θ_W(D))`). **At 1/3: no.** The centre of `Z_n` sits at `C_BFT` with support 3 |
| A6 | `log e(P) → E[inv_e]` bridge | not needed: both are bounded separately by range (F4, F6) |
| A7, A10 | "the slot law decays" / `Σ a_x² = O(Σ a_x)` | exist. (support `≤ D+1`, F5). useful: no |
| A11 | **(QD_D)** | **no. §5** |
| A12 | `N_i² ≥ (1+cΦ)N_{i−1}N_{i+1}` on `Π_D` with `c = c(D)` | not supplied. `c(D) ≤ 1/(D²−1)` PROVEN (§5.3). Same obstruction as (QD_D) |
| A13 | a positive lower bound on balances forced by the subadditive profile | exist. at `c(D) = 2^{1−2D}` (Lemma 2.3). Useless at 1/3 |
| A17 | (R): frozen `d ≤ D' < 1` | exist. for `n ≥ D/D' + 1` (F3). useful at computable `n`: no (KSBFT-C §2.7) |
| A18 | `max_x Σ_{y∥x} P[{x,y} inverts] = O(1)` | exist. (`< D/3` frozen). useful: no |
| A22, D3, E4 (3da1/c776) | a realizability fact excluding the two-atom law | exist. (H is one: `d ≤ D/(n−1)`). Useful (`ε_spec ≤ ε_dem`) only at `n ≥ 50D` |
| A25 | per-slot LP value `O(n)` | exist. (`≤ nD/6`). useful: no |
| B2 | Hyp A: `(c₅*)²γ³c₆ ≥ 512w²` at some admissible γ | **no**. It fails for every `γ ≤ 1/2` on the constants alone; the γ-floor `c(D)` does not reach `γ_crit` |
| C1, C3, C4 | `log₂ e(P) ≤ c·n log₂ n` with `c < 1` / `Θ(n)` from hypothesis (1) | exist. (`n log₂(D+1)`). Non-vacuous only at `n ≳ (D+1)^{1/c}` |
| C6 | certify `d ≤ D' < 1` | exist. (F3) |
| D1 | a rate for LIB-weak | exist. (`E inv_e < nD/6`) |
| D2 | *(near-identical position laws ⟹ near-balanced)* | **not examined** |
| E2 | (T) = (IB) on `Π_D` | **it is (MC_D)** (KSBFT-F Prop 4.2). Not supplied |
| E3 (0b96, 81ff) | frozen density ceiling / chain-IV capture | exist. (F3) |

**Summary.** Every need in the table is supplied in existence form except three: (QD_D) (rows A11
and A12), B2's constant inequality, and (MC_D) itself (E2). None is supplied at the constant the
route needed. D2 is unexamined.

---

## 5. Deep dive: the Stanley-stability route under bounded range

### 5.1 Why this route, by elimination

Take the DISSOLVES and TRANSFORMED rows. Remove those whose target is **auto** or **moot** (§2). Those
targets are true and useless, and reviving their routes proves nothing new. Remove the rows whose
revived need is (MC_D) itself (E2) or a constant inequality that fails outright (B2).

**What remains is exactly A11/A12.** This is the line mg-a1ec → mg-48ab → mg-dcae. It is the only
revived route with a **δ-direct** theorem already attached: mg-48ab Theorem 5.2 (read at
`one_third_width_three/docs/OneThird-AF-EqualityCase-MaShenfeld.md:300–327`).

> **Theorem 5.2 (mg-48ab, PROVEN (cited), re-read).** If `N_·(x)` is exactly flat across its full
> support, of length `W ≥ 2`, then `δ(P) ≥ 1/3`. Sharp at `tight3 = (2+1)`.

Its residual (mg-48ab §6.2) was a **k = 1 stability theorem for Stanley's inequality**. mg-dcae killed
the unconditional form with `C_n ⊔ C_n`, where `c ≤ 2/(2n−1)` (checked exactly here for `n = 2..5`,
`out_stanley_gap.txt`). That witness has range `n`. **So this is the one place where a range-`Θ(n)`
witness stood between a δ-direct theorem and its extension.** The ticket's question has a live
answer only here.

**Notation.** `N_i = N_i(x) = #{σ ∈ L(P) : σ(x) = i}`. `d = d(x)`. The support is
`[d+1, d+1+π(x)]` (Prop 3.1(6)). An index `i` is *interior* if `i−1, i, i+1` all lie in the support.

**Ma–Shenfeld at k = 1 (PROVEN (cited), via mg-48ab §2 and the attempt-index row's verbatim check
of MS Thm 1.3(iii)/Rem. 1.8).** At an interior `i`, `N_i² = N_{i−1}N_{i+1}` holds iff every
extension with `x` at `i−1`, `i` or `i+1` has its companions incomparable to `x`. **Equality forces
`N_{i−1} = N_i = N_{i+1}`**, so the geometric ray `r ≠ 1` is excluded. *(Consistency, EMPIRICAL:
over the probe population, 3 969 interior equalities, **0** of them not flat.)*

### 5.2 The revived statement and what it would give

> **(QD_D) — CONJECTURED.** There is `κ(D) > 0` such that for all `P ∈ Π_D`, `x ∈ P` and interior `i`:
> `N_i² > N_{i−1}N_{i+1} ⟹ N_i² ≥ (1+κ(D))·N_{i−1}N_{i+1}`.

Call `x` **κ-near-log-linear** if `π(x) ≥ 2` and `N_i² < (1+κ)N_{i−1}N_{i+1}` at every interior `i`.

> **Proposition 5.4 — PROVEN (given QD_D, Ma–Shenfeld k = 1 as cited, mg-48ab Thm 5.2).** If
> (QD_D) holds, then **(FLAT_D)**: no `P ∈ Π_D` with `δ(P) < 1/3` has a `κ(D)`-near-log-linear
> element.

*Proof.* Let `x` be `κ(D)`-near-log-linear. By (QD_D), every interior index is an equality. By MS,
each equality is a flat triple, so `N` is constant on its support. The support is a window of
`W = π(x)+1 ≥ 3` slots, so the full-support law is exactly flat. By Theorem 5.2, `δ(P) ≥ 1/3`. □

**Why this is the right kind of statement.** It converts an **approximate** hypothesis into an
**exact** one through quantisation (§3.3). That is exactly the move KSBFT-F §8 said any locality
proof needs. It is also the only statement in §4 whose conclusion is δ itself.

### 5.3 Sharpness: `κ(D)` must decay at least like `D⁻²`

> **Proposition 5.5 — PROVEN.** `κ(D) ≤ 1/(D²−1)` for every `D ≥ 2`. Hence no D-uniform (QD) exists.

*Proof.* Take `P = C_m ⊔ C_n` with `x = u₁`, the bottom of `C_m`. `P` has range `max(m,n)`. With `x`
preceded by exactly `j` elements of `C_n` (they must be `v₁ … v_j`), the remaining `m−1` elements of
`C_m` interleave with the remaining `n−j` of `C_n`, so `N_{1+j} = C(n−j+m−1, m−1)`, `0 ≤ j ≤ n`. Put
`t = n+m−1−j`. From `C(t,m−1)/C(t+1,m−1) = (t−m+2)/(t+1)`:

`N_{1+j}² / (N_j N_{2+j}) = t(t−m+2)/((t+1)(t−m+1)) = 1 + (m−1)/((t+1)(t−m+1))`.

Take `m = 2`, `n = D` and `j = 1` (`t = D`). The deficit is `1/((D+1)(D−1)) = 1/(D²−1) > 0`. The range
is `max(2, D) = D`. □

*Checks.* The `m = n` case at `j = 1` gives `1/(2n−1)`, which is mg-dcae's figure, reproduced
exactly by the instrument (control). The instrument's family (a) prints `1/3, 1/8, 1/15, 1/24, 1/35`
for `D = 2..6`, which is `1/(D²−1)`.

**The bound is not tight at `D = 4` (PROVEN by exhibit).** The seeded probe found a range-4 poset on
8 elements with a smaller strict deficit. Its covers are
`0<1, 1<3, 1<5, 1<6, 2<5, 2<6, 3<4, 3<7, 6<7`, `x = 5`, and `N_·(x) = (0,0,0,15,18,19,19,19)`. At
`i = 6` the deficit is `19²/(18·19) − 1 = 1/18`. The small deficit sits **at the edge of an exact
flat run** `(19,19,19)`. That is exactly the configuration Theorem 5.2's partial-run version
(mg-48ab Prop 5.3) has to handle.

**Evidence that `κ(D) > 0` (EMPIRICAL, `stanley_gap.py 150`).** The minimum strict deficit, over
seeded random banded posets of range `≤ D`, was computed at `n = 8, 10, 12, 14, 16`, 150 posets per
cell. Every `(x, i)` was examined, with exact integers.

| D | min strict deficit, n = 8 … 16 |
|---|---|
| 2 | `1/3` at every `n` |
| 3 | `1/8` at every `n` |
| 4 | `1/18` at `n = 8`, `1/15` at `n = 10..16` |

The minimum over `Z_m` (range 2) converges to `1/φ ≈ 0.618`. **At fixed `D` the floor does not
move with `n`.**

- *Negative control:* planted floors `κ(2) ≥ 1/2`, `κ(3) ≥ 1/7` and `κ(4) ≥ 1/14` are violated in
  15/15 cells, so the probe CAUGHT them.
- *Scope:* random, not exhaustive. It proves only the upper bounds it exhibits.

### 5.4 Proof attempt: a finite local decomposition and a compact reduction

> **Lemma 5.1 (local decomposition) — PROVEN.** Let `I(x) = inc(x)` and `D↓ = down(x)`. For
> `0 ≤ j ≤ π(x)`,
> `N_{d+1+j}(x) = Σ_{J} L(J)·R(J)`, where the sum runs over the **down-sets `J` of the induced
> subposet `P[I(x)]` with `|J| = j`**. Here `L(J) = e(D↓ ∪ J)` and
> `R(J) = e(P ∖ (D↓ ∪ J ∪ {x}))`.

*Proof.* In an extension with `x` at position `d+1+j`, the prefix before `x` is an ideal `K` with
`|K| = d+j`. `K` contains `D↓` and avoids `up(x)` and `x`. So `K = D↓ ∪ J` with `J ⊆ I(x)`,
`|J| = j`.

`K` is an ideal iff `J` is closed downward **within `I(x)`**. A predecessor `w` of `z ∈ J` is not
above `x`, since `x < w < z` would give `x < z`. So `w ∈ D↓ ∪ I(x)`, and if `w ∈ I(x)` it must lie
in `J`.

Given `K`, the extensions number `e(K)·e(P ∖ K ∖ {x})`. The part after `x` is any extension of the
complement: its elements are `up(x) ∪ (I(x) ∖ J)`, none of them below `x`, and every element below
one of them either lies in `K`, is `x`, or is itself in the complement. □

> **Lemma 5.2 (weight quantisation) — PROVEN.** For down-sets `J ⊂ J ∪ {z}` of `P[I(x)]`:
> `1 ≤ L(J ∪ {z})/L(J) ≤ π(z)+1 ≤ D+1`. The same holds for `R`, reversed. Hence for any two
> admissible `J, J'`: `(D+1)^{−D} ≤ L(J)/L(J') ≤ (D+1)^{D}`, and likewise for `R`.

*Proof.* `z` is maximal in the ideal `K ∪ {z}` (`K = D↓ ∪ J`). An extension of `K ∪ {z}` is an
extension of `K` with `z` inserted after the last predecessor of `z`. The elements it may pass are in
`K`, not below `z` (they come after its last predecessor) and not above `z` (maximality). So they
are incomparable to `z`, and there are at most `π(z)` of them. That gives between 1 and `π(z)+1`
slots, and at least one, at the end. So `e(K∪{z})/e(K) ∈ [1, π(z)+1]`. Chain down to `J = ∅` and
back up. The chain has length `≤ |I(x)| ≤ D`. □

**Local type.** Call `τ(x)` the isomorphism type of `P[I(x)]`, together with, for each minimal
element `u` of `up(x)`, the set `pred(u) ∩ I(x)`, and dually for each maximal element of `D↓`.

- There are finitely many types for each `D`: at most `2^{O(D²)}` orders on `≤ D` points, and
  `≤ 2^D` subsets per boundary element, with a bounded number of **distinct** subsets.
- Ma–Shenfeld's equality condition at interior `i` asks whether some extension with `x` at `i`
  (or `i ± 1`) has a companion comparable to `x`. The companion after `x` is a minimal element of
  `P ∖ (D↓∪J∪{x})`. It is comparable to `x` iff it is a minimal element `u` of `up(x)` with
  `pred(u) ∩ I(x) ⊆ J`. **So whether `i` is an equality index depends only on `(τ(x), i)`.** All
  the weights are positive, so no cancellation can create or destroy an equality.

> **Proposition 5.6 (compact reduction) — PROVEN.** Fix `D`. Write the deficit ratio at index
> `j` as `F_{τ,j}(L,R) = (Σ_{|J|=j} LR)² / ((Σ_{|J|=j−1} LR)(Σ_{|J|=j+1} LR))`. This is a
> continuous function of the normalised weight vector `(L,R)`. By Lemma 5.2 the vector lies in the
> compact box `B_D = [(D+1)^{−D}, (D+1)^{D}]^{2·#J}`. Let `S_τ ⊆ B_D` be the set of weight vectors
> realised by finite posets in `Π_D` of type `τ`. Then **(QD_D) ⟺ for each of the finitely many
> non-equality pairs `(τ, j)`, `inf_{S_τ} F_{τ,j} > 1`**. This holds **if** `F_{τ,j} > 1` on the
> closure `S̄_τ`.

*Proof.* Lemma 5.1 gives the formula. Lemma 5.2 gives the box. For each finite list of types, the
infimum of a continuous function over `S_τ` is at least its minimum over the compact `S̄_τ`. The
number of pairs `(τ,j)` is finite. □

**This is real progress over the unconditional situation.** For general posets, `C_n ⊔ C_n` puts
the relevant weights at ratios `C(2n−2, n−1)/…`, which are unbounded. So there is no compact box
and no finite type list. **Bounded range is precisely what makes the stability question a question
about finitely many continuous functions on a compact set.**

### 5.5 Where it stops — the precise obstruction

**What remains is strictness of Stanley's inequality at the limit points `S̄_τ ∖ S_τ`.** There are
two independent reasons the standing facts do not supply it.

**(a) Stanley's inequality is not a property of the weight box.**

> **Example 5.7 — PROVEN.** Let `I(x) = {a, b}` be an antichain, so the type has `J ∈ {∅, {a}, {b}, {a,b}}`.
> For arbitrary positive weights, `N_0 = L_∅R_∅`, `N_1 = L_aR_a + L_bR_b`, `N_2 = L_{ab}R_{ab}`, and
> `N_1² ≥ N_0N_2` fails whenever `(L_aR_a + L_bR_b)² < L_∅R_∅L_{ab}R_{ab}`. For instance, take all
> weights 1 except `L_{ab} = 3` and `R_∅ = 3`: then `(N_0,N_1,N_2) = (3,2,3)` and `4 < 9`. These
> weights satisfy **every** constraint of Lemma 5.2 at `D = 2`: `L` is non-decreasing and `R`
> non-increasing as `J` grows, with every one-step factor in `[1, 3] = [1, D+1]`.

So `F_{τ,j} > 1` is **not** implied by membership in `B_D`. It depends on the realised weights
satisfying further constraints: mixed-volume structure, and the log-concavity of the parts'
own counts. Those constraints are what Stanley's proof uses. A limit of realised weights keeps
every **closed** constraint (`F ≥ 1`) and can lose every **strict** one. **Ma–Shenfeld is a
theorem about finite posets.** Strictness at a limit point would need an equality-case
classification for the objects that limits of `(L, R)` represent: **posets with a boundary
measure on the top (bottom) window**. Those are the Gibbs-type limits of KSBFT-C §3.2 / KSBFT-I's
Dobrushin analysis. **No such "weighted Ma–Shenfeld" is among the standing facts, and I did not
find a way to reduce limit points to finite posets.** Such a reduction would need `S_τ` to be closed,
or its limit points to be realised again. KSBFT-I's Dobrushin contraction shows the normalised
boundary weights **converge** as the far part grows. It does not show they **stabilise** at realised
values.

**(b) The mechanism by which bounded range quantises does not apply to the defect.** Every
quantisation lemma of §3.3 is an injection that bounds the fibres of a map between **sets of
linear extensions**. It therefore bounds a **ratio of counts** from below. The Stanley defect
`N_i² − N_{i−1}N_{i+1}` is a **difference of products of counts**, and mg-dcae records that it is
not expected to have a combinatorial (#P) interpretation. mg-dcae's own caveat also holds: that
forbids an exact interpretation, not an inequality. So there is no set of objects whose fibres
Lemma 3.1-style hopping could bound. **(QD_D) needs a lower bound on a signed quantity, and bounded
range's only quantiser works on unsigned ones.**

**Precise statement of what would finish (QD_D):**

> **(WMS_D) — CONJECTURED, the missing tool.** For every type `τ` and every non-equality interior
> index `j`, `F_{τ,j} > 1` on `S̄_τ`. Equivalently: Stanley's inequality at `x` is strict, with the
> Ma–Shenfeld equality characterisation, for every limit of range-`D` posets with `x`'s local type
> fixed.

### 5.6 What (QD_D) would buy, even if proven — and why it is still not (MC_D)

(FLAT_D) says a counterexample in `Π_D` has, at every element with `π(x) ≥ 2`, **at least one**
interior slot with Stanley deficit `≥ κ(D)`, and `κ(D) ≤ 1/(D²−1)` by Prop 5.5. That is a **necessary
condition** on counterexamples. It is not a contradiction. Nothing on the record says a
counterexample must have a near-log-linear element, and the thin extremal family says the opposite:

- the Fibonacci centre laws have deficit `→ 1/φ`, far from 1;
- `(2+1)` is exactly flat and sits at δ = 1/3.

The one place (FLAT_D) bites is the KL / Kahn–Saks relaxation (row A5). Its extremal is the geometric
law `r = 1/φ`, i.e. a **Stanley equality case**. Under (QD_D), realised laws in `Π_D` stay `κ(D)`
away from that locus. Feeding that curvature into the KL relaxation would give
`δ ≥ C_BFT + η(κ(D))` (CONJECTURED). That is the same **shape** as KSBFT Thm 1.3/1.3″, and it
does not reach 1/3. **So the deep dive's honest verdict is: revived, reduced to one precise missing
tool (WMS_D), and even with that tool it yields a structural constraint, not the conjecture.**

---

## 6. What I did NOT do, and the candidates ruled out

**Not done:**

- **Paddings of finite witnesses into the window `[7, D]`** (A8, A9, A25-n=6, A27, A28). mg-b447 did
  this for `W*` only. Each such row is marked. A finite witness at range 5–9 refutes a universal on
  `Π_D` but not on `{7 ≤ π ≤ D}`. The rows concerned are moot for other reasons (their targets drop
  out under H), so the verdicts do not depend on it.
- **B6** (the width-3 Lean axiom's enumeration gap) and **D2** (mg-c3ca's two-element lemma): not
  examined.
- **B1/B4's Π_D-restricted cohomology.** I PROVE that `{π ≤ D} ∩ PPF_n` is an up-set under
  refinement. I did not compute or bound its order complex's homology.
- **Rows A1–A28 were classified from the documents' own statements of their witnesses**, reported by
  four read-only sub-agents with file:line citations. I read myself: mg-48ab §3–§6 (the deep-dive
  source), KSBFT-A/C/F/H/J, the Hodge-side row M3, and the attempt index. **Every range in §2 was
  computed by my instrument from the witness's printed relations and then proved by hand.** The
  obstruction wording of rows I did not open is the sub-agents' quotation.
- Two witnesses were **inferred**, not read:
  - the `n = 6`, `e = 9` pair of mg-8748/8b32 as `V ⊕ V`, from `e = 9` and δ = 1/3;
  - the `λ ≈ 0.96` ensemble (A9), which names no poset.
  Both are finite, so their verdicts do not depend on the identification.
- The Ma–Shenfeld theorem itself was **not** re-read at the source. I use it as mg-48ab quotes it
  (their §2, and the attempt-index row "checked verbatim against the paper"). My probe is consistent
  with it (3 969 equalities, all flat).
- **(QD_D) is not proven.** Lemmas 5.1 and 5.2 and Props 5.4–5.6 are proven. (WMS_D) is open.
- Nothing about `L*`, `K`, AK25a/b or Haq26. No edits to STATE / EXECUTIVE-SUMMARY / CONCEPTS.

**Candidates tried and ruled out for the deep dive:**

1. *Route B's `1/γ` perturbation via Dobrushin decay* (B2). Ruled out: Hyp A fails at every `γ ≤ 1/2`
   on its constants (`γ_crit ≈ 27–936`), so no γ-side improvement can save it.
2. *Probe D with co-degree `≤ D−1`* (A16). Ruled out: the local bound is already 1/6 at co-degree 2,
   range 2.
3. *Probe B with spread `≤ D+1`* (A14). Ruled out: death at spread 4 needs only range 3.
4. *The per-slot LP / pair-bias line with window constraints* (A22, A25). Ruled out: the target
   `ε_spec` is auto (`≤ Dn/(n²−1)`) and useless below `n ≈ 50D`.
5. *Compression shape-B on `Π_D`* (C3). Ruled out: supplied at `n ≳ (D+1)^{1/c}`, never at a
   computable `n` for `D ≥ 7`.
6. *A D-uniform Stanley stability* (A12 → QD). **Refuted** by Prop 5.5: `κ(D) ≤ 1/(D²−1)`.

**Recommendations to pm-onethird (no edits made).**

1. Carry §3's pattern as the answer to Daniel's question. **No walled route is revived into a proof.**
   The routes that dissolve are the ones whose targets H already makes true and useless. The routes
   aimed at δ died on thin or structural obstructions, which H cannot touch.
2. If a δ-level tool is wanted from bounded range, it is **quantisation** (§3.3). Its known limit is
   signed quantities. (WMS_D) is the cleanest open instance of that limit and is worth a scoping
   ticket only if someone has a handle on equality cases for posets with boundary measures. That is
   a literature question: weighted/"multivariate" Stanley inequalities. It was not surveyed here.
3. Audit targets: Prop 3.1(2),(6); Lemma 5.1's down-set claim; Lemma 5.2's slot count; Prop 5.5's
   closed form; Example 5.7; and the §2 ranges (re-run `ranges*.py` or re-derive by hand).
