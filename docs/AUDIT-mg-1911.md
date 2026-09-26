# AUDIT of mg-1911 — `docs/KSBFT-C-programme-repricing.md`

`mg-2ec1`, 2026-09-26. This is an independent audit with fresh context. The subject is the document as
landed at `381273a`, and it was **not edited**. The paper is `/Users/daniel/files/KSBFT_v7.pdf`, read with
`pdftotext -layout`, and page numbers are the printed ones.

## 0. Verdict

**The mathematics holds. No boxed or headline PROVEN claim is broken.** The core facts F1–F7 are right,
including F2's sharper `−1`. So are H_w and H, the two L1b thresholds (`L*/ε+1` frozen, `3L*/ε+1`
unconditional), the `Z_n` zero-orders argument, and the width-3 reduction. I re-derived each of them
here. I also re-read KSBFT Lemma 3.1's proof (p.9–10) line by line, and it is correct.

**The defects are in the surrounding prose.**

- **One BROKEN inequality.** §2.10 says the `n ≈ 900C` threshold is `≪ N₁`. By the document's own
  identification it is `150L* > N₁`. Correctly normalised it is `≈ 50L* ≈ N₁`, the same crossover.
  Behind this is a normalisation slip in §4: it says `C = L*/6` where it means `C/γ = L*/6`.
- **Six OVERSTATEMENTS**, listed in §3. Two matter:
  - "Past `N₁` the whole remaining content is rows 10, 11 and Step 6" omits row 9 (L2 as a
    disjunction, OPEN) and row 3b.
  - "`n log₂ w` is not vacuous on counterexamples" holds only for `n ≳ e·min(K, L*+1)`.
- **One UNVERIFIABLE.** "Width 3 needs AK25b ALONE" is true of KSBFT as written. I did not read
  whether AK25b's own proof leans on AK25a.

**KSBFT usage is clean.** The document consumes only three things from the paper:

- the statements of Thms 1.4 and 1.5 (p.4–5, checked verbatim);
- the citations BW92 and Pec08 (p.3, "6-thin", with footnote 1: thin means `π(P) ≤ D`);
- Lemma 3.1, whose proof I re-checked (§2, F7).

It consumes **neither Lemma 4.2 nor `441` nor eq. (1.5)**. I confirmed this by grep: the only mentions
are its own disclaimers (lines 163–164 and 467). Line 342 uses `C_BFT + η_D < 1/3`, which holds for any
positive constant in place of `4096`.

**Empirical content is not passed off as proof.** Appendix A is labelled EMPIRICAL and reproduces
exactly: the sha1 matches and the output is byte-identical. Every PROVEN fact it checks also has a
written proof. The one place a probe *found* a result (F2's `−1`) is followed by a proof, which I
re-derived.

**Successor needed:** one small errata ticket against the mg-1911 document (§5). Nothing here blocks
pm-onethird's use of the document's §5 recommendations. STATE.md was not edited by mg-1911, so no
ledger row is wrong.

---

## 1. Every PROVEN claim, with its verdict

Enumerated from §0 (the boxed list and the table), §1, §2.1–2.10, §3.2, §4 (every row marked PROVEN)
and Appendix A. `D := π(P)`. **cond.** means conditional on the preprints, exactly as the source uses the
word.

### 1a. Core facts (§1)

| # | claim (source §) | verdict | re-derivation / note |
|---|---|---|---|
| H_w | a counterexample has `w ≤ K` (§1.1) | **HOLDS** (cond. AK25a, Haq26) | Thm 1.4 p.4 is verbatim `w > K ⟹ δ > e⁻¹ − 10⁻¹⁰⁰`, and `e⁻¹ − 10⁻¹⁰⁰ > 1/3`. `K` need not be an integer: `w ≤ K ⟹ w < K+1` either way. |
| H | a counterexample has `π ≤ L* := L(K+1, 1/6)` and `w ≤ L*+1` (§1.1) | **HOLDS** (cond. all three) | Thm 1.5 p.5 is verbatim `w < K`, `π > L ⟹ δ > 1/2 − ε`. At `(K+1, 1/6)` the conclusion is `δ > 1/3`, so a counterexample has `π ≤ L*`. An antichain of size `w` gives `π ≥ w−1`. |
| — | the majority order `e` is a linear extension (§1.1) | **HOLDS** | Suppose the oriented tournament had a 3-cycle. Its three cyclic probabilities would sum to `> 2` (each is `> 2/3` or `= 1`). But at most two of the three cyclic events hold in any order, so the expected count is `≤ 2`. |
| F1 | `d(x)+1 ≤ g(x) ≤ d(x)+1+π(x)`, so `\|g(x)−e(x)\| ≤ π(x)`, and the window is attained when `π(x)>0` | **HOLDS** | Upper bound: the `u(x) = n−1−d(x)−π(x)` successors all follow `x`. Attainment: the prefix is `D(x) ∪ I(x) ∪ ⋃_{z∈I(x)} D(z)`. For `z ∥ x`, no element of `D(z)` is `≻ x` (else `x ≺ z`), and `x ∉ D(z)`. So the prefix has size `d(x)+π(x)`. **Attainment for EVERY `x` was checked here (A1)**; Appendix A's N1 checks only that some `x` attains it. |
| F2 | `x ∥ y ⟹ d(x) − d(y) ≤ π(y) − 1`, and `\|g(x)−g(y)\| ≤ π(x)+π(y)−1 ≤ 2D−1` | **HOLDS** | Each `v ≺ x` is `≺ y` or `∥ y`. `v = y` and `v ≻ y` are both excluded by `x ∥ y`. The `∥ y` ones lie in `I(y) ∖ {x}`, which has size `π(y) − 1`. Then use F1. The direction of the inequality is right, and the result is symmetric in `x, y`. |
| F3 | `m = ½Σπ(x) ≤ nD/2`, so `d ≤ D/(n−1)` | **HOLDS** | `(nD/2)/C(n,2) = D/(n−1)`. |
| F4 | `inv_e ≤ m`. If frozen, `E[inv_e] < m/3 ≤ nD/6`, and `ε_spec < d·n/(n+1) ≤ Dn/(n²−1)` | **HOLDS** | Only incomparable pairs can be inverted. The identity `ε_spec = 6E/(n²−1) = 3dq̄·n/(n+1)` was re-derived from `m = d·n(n−1)/2`. The strict `<` needs `m ≥ 1`, i.e. a non-chain. |
| F5 | `Σ disp² ≤ D·Σ\|disp\|` pointwise | **HOLDS** | `\|disp(x)\| ≤ π(x) ≤ D` (F1). This also holds if `disp` is measured from `h(x)`, because `h(x)` lies in the same window. |
| F6 | `log₂ e(P) ≤ Σ log₂(π(x)+1) ≤ n log₂(D+1)` | **HOLDS**, with one citation nit | The position vector determines `g`. **Nit:** KSBFT (3.3) at `U = ∅` states only the coarser `(D+1)^n`; the finer product is in the proof line above (3.3), not in (3.3) itself. |
| F7 | `x ∥ y ⟹ P[g(y) < g(x)] ≥ q₂ = (D+1)^{−2(D+1)}` | **HOLDS** | KSBFT Lemma 3.1 (p.9–10) was re-read line by line and is correct. |

Notes on F7, step by step:

- **The path step is sound.** A `Q`-path from `u` to `v` that uses an added comparison passes through
  some `s ∈ S`. Both `u, v ∈ U` are `P`-comparable to `s`. The orientation is forced by antisymmetry
  in `Q ⊇ P`.
- **(3.2) is sound.** Restriction `L(Q) → L(Q[U])` is surjective.
- **(3.3) is sound.** It is F1 plus the order on `U`.
- **`|T| ≤ Σ_{s∈S}(1+π(s))` is sound.**
- **It applies here.** The event `{g(y) < g(x)}` is `{x,y}`-dependent, and it has positive probability
  because `x ∥ y`.
- **It uses nothing from §4.**

### 1b. Thresholds and range arguments (§0, §2.1–2.9)

| # | claim (source §) | verdict | re-derivation / note |
|---|---|---|---|
| §2.1(a) | without frozenness, `E ≤ nL*/2 ≤ (ε/6)(n²−1)` for `n ≥ 3L*/ε + 1` | **HOLDS** (cond.) | The condition is `n² − (3L*/ε)n − 1 ≥ 0`, i.e. `n(n − 3L*/ε) ≥ 1`. At `n ≥ 3L*/ε+1` the left side is `≥ n ≥ 1`. It holds for every range-`≤ L*` poset and every `e`. |
| §2.1(b) | frozen: the same conclusion for `n ≥ L*/ε + 1` | **HOLDS** (cond.) | The condition is `n(n − L*/ε) ≥ 1`. `N₁ = ⌈L*/ε⌉ + 1` suffices. The `50·C₃·L*` refinement agrees with mg-6bc2 `:442` (`ε_dem = 1/50` at `C₃ = 1`, and `C₃ ≥ 1` is a loss). |
| §2.1 box | under H, L1b ⟺ a statement about the finitely many frozen posets on `< N₁` elements | **HOLDS** (cond.) | Row 8 (`STATE.md:123`) quantifies over frozen posets, i.e. `δ < 1/3`. Chains are trivial. Finitely many isomorphism classes exist below `N₁`. |
| §0.2 / §2.1 ⚠️ | past `N₁`, "the programme's **whole** remaining content is rows 10 and 11 and the Step-6 hole" | **OVERSTATED** | The L1b half is right. But the sweep omits **row 9** (L2 as a disjunction: **OPEN**, `STATE.md:124`) and row 3b (its conditional form is ⟺ L1b as a *universal*, which does not transfer per `n`). Neither is priced anywhere in the document. See D2. |
| §0.3 | "KSBFT's residual region is **exactly** the region where the wall is already down" | **OVERSTATED** | The residual region is `{π ≤ L*}` at all `n`, and the wall is down there only for `n ≥ N₁`. The next sentence gives the correct overlap `{π ≤ L*, n ≤ 50L*}`. |
| §2.2 | the dense regime contains no counterexample once `n > 50L*+1` | **HOLDS** (cond.) | `d ≤ L*/(n−1) < 1/50` once `n − 1 > 50L*`. |
| §2.2 | the residual gap "is a finite question, and not a computable one" | **OVERSTATED** (wording) | It is finite, and decidable once `L*` is known. It is *infeasible*, and currently unstated because `L*` is not explicit. It is not uncomputable. |
| §2.3 | H excludes the two-atom witness, and `ε_spec ≤ L*n/(n²−1)` | **HOLDS** (cond.) | F4. `Θ(n²)` inversions need `Θ(n²)` incomparable pairs, but there are only `≤ nL*/2`. |
| §2.4 | `(B)` with constant `L*`; `(LIB)` with `E < nL*/6` independent of `γ` | **HOLDS** (cond.) | F5 and F4. |
| §2.5 | `N₀ = ⌈L*/ε⌉+1`, and mg-c4f5 §5.3 is not contradicted | **HOLDS** (cond.) | H supplies `O(n)`, which is not an `o(n²)` hypothesis. §5.3 is about the latter. |
| §2.6 | `(EQ)` existence form `≤ L*` | **HOLDS** (cond.) | Average F1: `h(x)` and `e(x)` both lie in the same window of width `π(x)`. Checked empirically as A4. mg-5987's constants `37/123`, `2/5` and `8/25` match `OneThird-LeverTest-mg-5987.md:41-42`. |
| §2.7 | `(1_D)` holds for `n ≥ L*/D + 1` | **HOLDS** (cond.) | `L*/(n−1) ≤ D`. |
| §2.7 | "KSBFT proves the conjecture on `{d > D, n > L*/D+1}`" | **HOLDS** (cond.) | A counterexample would have `d ≤ L*/(n−1) < D < d`. |
| §2.7 | H gives nothing at `n ≤ 98` because "`50L* ≫ 98` unless `L* ≤ 1`" | **HOLDS**, imprecise | At `L* = 2`, `50L* = 100` is not `≫ 98`. But `N₁ = ⌈L*/ε⌉+1 ≥ 101 > 98` for every `L* ≥ 2`. And `L* ≤ 6` would, with Pec08, prove the conjecture outright. So the conclusion stands. |
| §2.7 | `Z_n` is primitive with `π = 2` at every `n`, so KSBFT delivers zero whole orders | **HOLDS** for `n ≥ 4` | Checked (A5): `Z_n` is **prime** (no non-trivial module) for `4 ≤ n ≤ 10` and **not prime at `n = 3`**. The controls, `Z_3` and the ordinal sum `2⊕2`, both come back non-prime. For `n ≥ 4` in general: `inc(Z_n)` is the path `P_n`, which has no non-trivial module. "At every `n`" is false only at `n ≤ 3`, which is irrelevant, since every order in play is `≥ 15`. |
| §2.8 | `log₂ e(P) ≤ n log₂ min(K, L*+1)` | **HOLDS** (cond.) | Two routes: F6, and `e(P) ≤ w^n` (every step picks among the minimal elements, which form an antichain). |
| §2.8 | shape-A `c·n log₂ n` targets are automatic for `n ≥ min(K,L*+1)^{1/c}` | **HOLDS** (cond.) | Nit: the text then says "that is `n ≥ K^{1.064}`, astronomically past 16,777,063". `K^{1.064}` is a *sufficient* threshold. The actual one is `min(K,L*+1)^{1.064}`, whose size is unknown. |
| §2.8 | "dense means wide" **REFUTED under H**; "`n log₂ w` is **not** vacuous on counterexamples" | **OVERSTATED** | (i) "Dense means wide" is refuted **unconditionally**, by the document's own §1.1 example: two chains, `w = 2`, `d → 1/2`. What H adds is "counterexamples are narrow". (ii) The bound `n log₂ w ≤ n log₂ K` beats the trivial `log₂ n!` only for `n ≳ e·min(K, L*+1)`, which is astronomical by the document's own estimate. So it is still vacuous at every `n` the programme can reach. |
| §2.9 | small range is an infinite family, so H plus a finite check does not settle width 3 | **HOLDS** | Witness at width exactly 3: `x_i ≺ x_j ⟺ j − i ≥ 3` has `w = 3` and `π = 4` at every `n ≥ 7`. |
| §2.9 | width-3 1/3–2/3 ⟸ AK25b + "no width-`≤ 3` poset with `7 ≤ π ≤ L(4,1/6)` is a counterexample" | **HOLDS** (cond.); "ALONE" **UNVERIFIABLE** | Thm 1.5 at `K = 4` gives `w < 4`. BW92 and Pec08 are cited on p.3 for `π ≤ 5` and `π ≤ 6`. Thm 1.4 is indeed not needed. **But** "AK25b alone" is a claim about AK25b's own proof, which neither the source nor I read. The arXiv abstract (fetched) names no companion dependence, and that is not evidence either way. |
| §3.2 | the finite-state / transfer-matrix description of range-`≤ D` posets is **PROVEN** | **HOLDS**, gap filled here | The document says "state = the down-set's frontier inside the window" without proving it. **Proof:** let `I` be a down-set, `j = max_ℓ I`, and `x ∉ I` with `ℓ(x) < j`. Then `x ⊀ j` (else `x ∈ I`), and `j ⊀ x` (`ℓ` is a linear extension), so `x ∥ j`. By F2, `j − ℓ(x) ≤ 2D − 1`. So `I` = (every position `≤ j − 2D`) ∪ (a subset of the last `2D − 1` positions), giving `≤ n·2^{2D−1}` states. Checked as A2 (control A2n fires). The transitivity and range constraints are also local to the window, so the word family is a sliding-window language. |

### 1c. §4 sweep rows marked PROVEN

The source's own "read?" column says which passages the author read.

| # | claim (source §) | verdict | re-derivation / note |
|---|---|---|---|
| §4 abe8 | range-`≤ D` posets on `n` elements number `≤ 2^{(2D−1)n}` up to isomorphism | **HOLDS** | Every class has a natural labelling. By F2, all pairs at label distance `≥ 2D` are forced. There are `≤ (2D−1)n` remaining pairs, each one bit. |
| §4 C3/Var | `Var(pos_x) ≤ (L*+1)²/4` | **HOLDS** (loose) | Popoviciu gives `π(x)²/4`, checked as A3, with control A3n at `(π−1)²/4` firing. |
| §4 0b96 | the dense family `d ≥ 0.838` exceeds `L*` for large `n` | **HOLDS** (cond.) | `max π ≥ 2m/n = d(n−1)`. The quote was spot-checked at `OneThird-FrozenDensity-mg-0b96.md:44-47`. |
| §4 Op-Form 7.4 | "`C = L*/6`, and the crossover is at `n ≈ 50L*`" | **BROKEN label, right number** | Op-Form's (LIB) is `E ≤ Cn/γ`, with crossover `n ≈ (C/γ)/(ε/6)`, i.e. `900C` at `γ = 1/3` (`OneThird-lambda-std-Operative-Form.md:634-645`). F4 gives `C/γ = L*/6`, **not** `C = L*/6`. The crossover `L*/ε = 50L*` is right. See D1. |
| §2.10 | literature and threshold `n`-bounds, including `n ≈ 900C`, are "each `≪ N₁`" | **BROKEN** for the `900C` item | Under the document's own `C = L*/6`, `900C = 150L* > N₁ ≈ 50L*`. Under the correct `C = γL*/6 = L*/18`, `900C = 50L* ≈ N₁`: it is the same crossover, not "≪". The other items hold for `L* ≥ 2` (`N₁ ≥ 101`). |
| §4 00a1 | per-slot LP value `≤ nL*/6` via mg-131e's trivial dual | **HOLDS** as cited | mg-131e `:14-15` states the trivial dual `val ≤ n(n−1)/6`, i.e. `C(n,2)/3`. Its range-`≤ L*` analogue `m/3` is F4 again. |
| §4 others | rows marked `agent` | **UNVERIFIABLE as to the quoted site** | The mathematics in each (substituting `D = L*` into F1–F4) holds. Whether each site says what the sub-agent quoted is not established. I spot-checked two, mg-0b96 `:44-47` and mg-9d9e `:222`, and both match. |

### 1d. Appendix A

| # | claim (source §) | verdict | re-derivation / note |
|---|---|---|---|
| App. A | 5 230 posets, C1–C6 hold, N1–N5 fire | **REPRODUCED** (EMPIRICAL) | The script was extracted from the document. Its sha1 is `351c990d…3342` (matches), and its output is byte-identical (2.4 s). `5230 = 2+7+40+357+4824` is the naturally-labelled counts, A006455 at `n = 2..6`. Correctly labelled EMPIRICAL, and not load-bearing. |

---

## 2. Negatives checked against the candidate space

| negative (source) | candidates tried | verdict |
|---|---|---|
| bounded range does not bound `n` | `Z_n` | **HOLDS**. One witness settles a universal negative. |
| H plus a finite check does not settle width 3 (§2.9) | the family `j − i ≥ 3` (mine; the source used `Z_n` plus an existence assertion) | **HOLDS**. The residual set is infinite. |
| H does not lower `(EQ)`/`(B-cov)` to mg-5987's constants (§6) | **one**: F1 | **OVERSTATED as a flat "No"**. There are two separate questions. **Range alone** cannot do it, and I can prove that: the 2-antichain has `π = 1 ≤ L*` and `max\|h − rank_e\| = 1/2 ≥ 2/5`. **Range plus frozenness** has not been examined, because the frozen class is empty wherever anyone has looked, so no witness exists. The source's "I found no sub-`L*` bound" is the honest form. The headline "No" is not. |
| H gives nothing at `n ≤ 98` (§2.7) | the arithmetic `N₁ ≥ 101` | **HOLDS** for `L* ≥ 2`. |
| the Case-3 axiom's regime does not force `π ≥ 7` (§2.9 item 4) | one consideration: interaction width `w` is an upper bound on reach | **UNVERIFIABLE here**, and correctly labelled by the source as "not a proof of impossibility". The axiom exists at `one_third_width_three/lean/OneThird/Step8/Case3Residual.lean:208`, with `hCard : card ≤ 6w+6`. I did not read the definition of `L.w`. |
| density alone does not fill `(T)` under H (§4, mg-7ae5) | — | **CONJECTURED**, and labelled so by the source. Not audited. |
| `L* ≥ K`? | — | Neither claimed nor denied. Nothing to audit. |

---

## 3. Defects (numbered for the successor)

- **D1 (BROKEN, minor).** Op-Form row: `C = L*/6` should be `C/γ = L*/6`. §2.10's "`900C ≪ N₁`" is
  then false: it is `≈ N₁`, the same crossover. Under the document's own label it would be `3N₁`.
- **D2 (OVERSTATED).** §0.2 and §2.1 say "the whole remaining content is rows 10, 11 and Step 6".
  Row 9 (L2 disjunction, OPEN) and row 3b are not priced. The answer to pm-onethird's question ("does
  the weight sit ENTIRELY on L4 and Step 6?") should list them or say why they drop out.
- **D3 (OVERSTATED).** §2.8 has two problems. "Dense means wide" is refuted *unconditionally*, not
  "under H". And "`n log₂ w` is not vacuous on counterexamples" holds only for
  `n ≳ e·min(K, L*+1)`.
- **D4 (OVERSTATED).** §2.2 calls the residual gap "not computable". The right word is *infeasible,
  and unstated while `L*` is inexplicit*.
- **D5 (OVERSTATED).** §0.3 says "exactly the region where the wall is already down". The next
  sentence already corrects it.
- **D6 (OVERSTATED).** §6 answers the `(EQ)`/`(B-cov)` negative with a flat "No". It should be split:
  range alone is provably insufficient (2-antichain witness, §2 above), and range plus frozenness is
  unexamined.
- **D7 (UNVERIFIABLE).** "AK25b ALONE" in §2.9 and §0 row 12. It is true at the level of KSBFT's
  statement. Say "KSBFT's Thm 1.5 only; AK25b's own dependencies unread".
- **Nits (no verdict change):**
  - F6's "(3.3) with `U = ∅`" states only the coarse form.
  - `50L* ≫ 98` is loose at `L* = 2`.
  - `K^{1.064}` vs `min(K, L*+1)^{1.064}`.
  - "`Z_n` primitive at every `n`" fails at `n = 3`.
  - Appendix A's N1 tests attainment for *some* `x`, while F1 claims it for every `x` (A1 below
    closes this).
  - §3.2's "follows from F1/F2" omits the down-set shape lemma, which is supplied in §1b above.

None of D1–D7 moves a verdict in the source's §0 table **except** as follows:

- Row 13′/§2.10's literature line loses "≪" for `900C` (D1).
- Row 11's "REFUTED under H" becomes "refuted unconditionally; counterexamples are narrow under H"
  (D3).
- Row 12's "AK25b alone" gets its caveat (D7).

---

## 4. Instrument (EMPIRICAL, not proof)

The instrument is standard-library Python with exact rationals. It is **inlined, not committed as
`code/`**, for the source's reason: no census or gate transcript moves. It uses its own enumerator,
written independently of Appendix A's.

- **What it checks:** what Appendix A does *not* check. A1 (window attained for **every** `x`), A2
  (down-set shape, §3.2), A3 (Popoviciu variance), A4 (`(EQ)` existence form), and A5 (`Z_n` range and
  primality, `n ≤ 10`).
- **Range:** all 5 230 naturally-labelled posets with `2 ≤ n ≤ 6`.
- **Controls:** each inequality has a one-unit-tightened negative control, and every one fired. A1 is
  an equality test, so an enumerator that drops or invents extensions would fail it. A5 has two
  non-prime controls.
- **Run:** `python3 audit_2ec1.py 6`, about 3 s.

The script is reproduced verbatim below.

```python
"""mg-2ec1 audit: independent checks of claims in docs/KSBFT-C-programme-repricing.md that its
Appendix A does NOT test.  Own enumerator (recursive extension by maximal element), own code.
A1 F1 attainment for EVERY x with pi(x)>0 (App. A's N1 tests only existence of one such x)
A2 down-set shape (sec 3.2 transfer matrix): in a reference extension l, every down-set I with
   max position j contains every position < j - (2D-1); tested as: x before j in l, x not in I,
   j = max(I) => j - x <= 2D-1.
A3 Var(pos x) <= pi(x)^2/4 (Popoviciu; doc states the looser (L*+1)^2/4)
A4 |h(x) - e(x)| <= pi(x)  ((EQ) existence form)
A1 is an EQUALITY test (hi-lo == pi(x) for every x), so it fails on an enumerator that drops
or invents extensions.  Negative controls (tightened by one unit, must fail somewhere):
A2n distance bound 2D-2; A3n (pi-1)^2/4; A4n pi(x)-1.
A5 Z_n (x_i < x_j iff j-i>=2): pi = 2 for n>=3, and PRIME (no nontrivial module) for n>=4,
   with control: Z_3 must be non-prime, and a 2+2 ordinal sum must be non-prime."""
import itertools, sys
from fractions import Fraction as Fr
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6

def all_posets(n):
    # strict orders on range(n) compatible with natural labelling, closed under transitivity
    pairs = [(i, j) for j in range(n) for i in range(j)]
    for bits in itertools.product((0, 1), repeat=len(pairs)):
        lt = {p for p, b in zip(pairs, bits) if b}
        if all((a, c) in lt for (a, b) in lt for (b2, c) in lt if b == b2):
            yield lt

def exts(n, lt):
    res = []
    def go(rem, seq):
        if not rem: res.append(seq); return
        for x in rem:
            if not any((a, x) in lt for a in rem if a != x):
                go(rem - {x}, seq + [x])
    go(frozenset(range(n)), [])
    return res

def downsets(n, lt):
    out = []
    for mask in range(1 << n):
        S = {i for i in range(n) if mask >> i & 1}
        if all(a in S for (a, b) in lt if b in S): out.append(S)
    return out

c = dict(A1=0, A2=0, A3=0, A4=0, A2n=0, A3n=0, A4n=0, P=0)
for n in range(2, NMAX + 1):
    for lt in all_posets(n):
        c["P"] += 1
        comp = lambda a, b: (a, b) in lt or (b, a) in lt
        pi = [sum(1 for y in range(n) if y != x and not comp(x, y)) for x in range(n)]
        D = max(pi)
        L = exts(n, lt); N = len(L)
        P = [{x: i + 1 for i, x in enumerate(s)} for s in L]
        lo = [min(p[x] for p in P) for x in range(n)]; hi = [max(p[x] for p in P) for x in range(n)]
        ok1 = all(hi[x] - lo[x] == pi[x] for x in range(n))
        c["A1"] += ok1
        # A2 on reference extension = identity (natural labelling is a linear extension)
        worst = 0
        for S in downsets(n, lt):
            if not S: continue
            j = max(S)
            for x in range(n):
                if x not in S and x < j: worst = max(worst, j - x)
        c["A2"] += (D == 0) or worst <= 2 * D - 1
        c["A2n"] += (D > 0) and worst > 2 * D - 2
        # A3/A4
        h = [Fr(sum(p[x] for p in P), N) for x in range(n)]
        var = [Fr(sum(p[x] ** 2 for p in P), N) - h[x] ** 2 for x in range(n)]
        c["A3"] += all(var[x] <= Fr(pi[x] ** 2, 4) for x in range(n))
        c["A3n"] += any(pi[x] > 0 and var[x] > Fr((pi[x] - 1) ** 2, 4) for x in range(n))
        e = P[0]
        c["A4"] += all(abs(h[x] - e[x]) <= pi[x] for x in range(n))
        c["A4n"] += any(abs(h[x] - e[x]) > pi[x] - 1 for x in range(n) if pi[x] > 0)
print("posets n<=%d: %d" % (NMAX, c["P"]))
for k in ["A1", "A2", "A3", "A4"]:
    print("  %s holds on %d / %d" % (k, c[k], c["P"]))
for k in ["A2n", "A3n", "A4n"]:
    print("  %s control fires on %d posets -> %s" % (k, c[k], "OK" if c[k] else "CONTROL DID NOT FIRE"))

def prime(n, lt):
    comp = lambda a, b: (a, b) in lt or (b, a) in lt
    for k in range(2, n):
        for M in itertools.combinations(range(n), k):
            Ms = set(M)
            if all(len({((a, z) in lt, (z, a) in lt) for a in M}) == 1 for z in range(n) if z not in Ms):
                return False
    return True
Z = lambda n: {(i, j) for i in range(n) for j in range(n) if j - i >= 2}
for n in range(3, 11):
    lt = Z(n)
    pi = [sum(1 for y in range(n) if y != x and (x, y) not in lt and (y, x) not in lt) for x in range(n)]
    print("  Z_%d: pi=%d prime=%s" % (n, max(pi), prime(n, lt)))
ord22 = {(a, b) for a in (0, 1) for b in (2, 3)}
print("  control: 2+2 ordinal sum prime=%s (must be False)" % prime(4, ord22))
```

Output:

```
posets n<=6: 5230
  A1 holds on 5230 / 5230
  A2 holds on 5230 / 5230
  A3 holds on 5230 / 5230
  A4 holds on 5230 / 5230
  A2n control fires on 103 posets -> OK
  A3n control fires on 4622 posets -> OK
  A4n control fires on 2923 posets -> OK
  Z_3: pi=2 prime=False
  Z_4: pi=2 prime=True
  Z_5: pi=2 prime=True
  Z_6: pi=2 prime=True
  Z_7: pi=2 prime=True
  Z_8: pi=2 prime=True
  Z_9: pi=2 prime=True
  Z_10: pi=2 prime=True
  control: 2+2 ordinal sum prime=False (must be False)
```

---

## 5. What I did NOT do, and the successor

- I did **not** read AK25a, AK25b or Haq26. For AK25b I read only its arXiv abstract page.
- I did **not** audit KSBFT Lemma 4.2, `441`, eq. (1.5), or §6. The subject document does not consume
  them, and I confirmed that by grep.
- I did **not** read the definition of `L.w` in the width-3 Lean code, so D-item §2.9.4 stays
  UNVERIFIABLE.
- I did **not** re-read every §4 row marked `agent`. I spot-checked two, and both match.
- I did **not** audit the CONJECTURED items (§3.1, the §3.2 decay lemma, row 13′). Their labels are
  honest.
- I did **not** audit mg-d707's later document (`code/ksbft_case_c_d707`). It is out of scope.
- I did **not** edit the source document, STATE.md or any ticket.

**Successor ticket needed:** *errata to `docs/KSBFT-C-programme-repricing.md` for D1–D7.* It is
prose-only, with no new mathematics, except that D2 asks whether row 9 (L2) drops out under H, and
that is a short question. The priority is low: no headline claim moves, and STATE.md carries none of
these sentences.
