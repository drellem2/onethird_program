# AUDIT of mg-b852 (KSBFT-G, `docs/KSBFT-G-constants.md`): mg-5562

Auditor: an independent polecat with fresh context. I am not the author. The subject is
`docs/KSBFT-G-constants.md` as of `a282f22`, with its instrument `code/ksbft_g_constants_b852/`.
Sources, read in full for this audit:

- KSBFT: `/Users/daniel/files/KSBFT_v7.pdf`, read with `pdftotext -layout`. It is **not in this
  repository**. Page and equation numbers are the printed ones.
- AK25b: arXiv:2510.26134**v1**, 11 pp., fetched from arxiv.org on 2026-09-26. The abstract page
  lists v1 only.

AK25a and Haq26 were **not** read. `K` is arithmetic on KSBFT's printed p.25 display, and its
validity rests on KSBFT §6, whose Prop B was audited under mg-e015.

Verdict scale:

- **HOLDS**: re-derived here, or re-computed independently.
- **BROKEN**: false as stated.
- **OVERSTATED**: the true content is weaker than the words.
- **UNVERIFIABLE**: not checkable with what I had.
- **UNDETERMINED**: checkable in principle, but the evidence does not separate the alternatives.

Instrument: `code/audit_ksbft_5562/`. Run it with `sh run_all.sh`. It takes about 6 s, runs one
process, and is deterministic.

- It shares **no code** with `constants.py`. It uses float log10 arithmetic, with the leading-order
  algebra written out from my own re-derivation in §2. The author's code uses `Decimal`.
- Part E is an **EMPIRICAL** test of Thm 2.6 as consumed. It covers every naturally-labelled poset
  on n ≤ 6 points (all isomorphism types, with repeats), using exact extension counts.
- Negative control: the false bound `q ≥ (2ε)^{1/2}` must be violated. It **FIRES** (10 810
  violations at n = 6).
- `run_all.sh` fails on any `FAIL` line or on a silent control.

---

## 0. Headline

| # | claim | verdict |
|---|---|---|
| 1a | "KSBFT eq (1.5) is NOT REPRODUCED" | **HOLDS.** No route through the printed ingredients reaches it (§1). |
| 1b | "(1.5) implies `log₃ L ≈ 1.6×10¹⁹`" | **HOLDS**, read as an *upper* bound that (1.5) needs: (1.5) is valid via Thm 1.3 iff `log₃(L+1) ≤ p − log₃(4p) ≈ 1.6×10¹⁹ − 41` (`p = 1.6×10¹⁹`). |
| 1c | "this route's floor is `5.5×10²⁴` even at the smallest §6 width bound" | **HOLDS for AK25b's proof as written, and robustly so. "Unavoidable" is OVERSTATED as to the factor 2.** The coefficient-1 floor `w²·log₃(1/2ε′) = 2.77×10²⁴` is structural (§1.2). The extra factor 2, from `π ≤ |B|²`, is a feature of the bookkeeping, not proven necessary. Both floors exceed `1.6×10¹⁹` by more than 10⁵. |
| 1d | the implied claim that *the published constant is wrong* | **UNDETERMINED.** The floor binds every route that uses KSBFT's printed Thm 1.4 width and AK25b's printed Thm 2.6. It does not bind a route the authors might have with a sharper heavy-atom bound, a smaller width bound from elsewhere (e.g. Air26), or a different case split. The paper omits the derivation (p.2). §1.3 lists what would separate these. What *can* be said: **(1.5) does not follow from the ingredients the paper prints.** |
| 2a | `q₀ = (2ε)^{w²}` (AK25b Thm 2.6) | **HOLDS**, re-derived from AK25b p.4–5. There is one edge-case defect in the doc's intermediate `(2ε)^{\|A\|\|B\|}`: it is **BROKEN when A or B is empty** (the bound would read `q ≥ 1`). The census finds 7 454 such cases at n = 6. The final `(2ε)^{w²}` is unaffected (§2.1). |
| 2b | Prop 2.3 with `294`, the easy direction `1/(64q²)`, and `η = 1/(16√(S+1))` | **HOLDS**, re-derived line by line (§2.2). |
| 2c | degree ≈ 13 in `1/η`; §3.4 table; Lemma 4.4 constant `(3B+1)(B+1)` | **HOLDS.** Every row was checked against AK25b p.8–10. The degree is `13 = 2·(3.5 + 2 + 1)`, from `C ∝ x^{3.5}`, `t ∝ x²` and the `1/η` in (13), all squared. It is read term by term in §2.3. Independent code gives 13.000000 as `η → 0`. |
| 3 | `L(4,1/6) ≤ 10^119.1`, `L(3,1/6) ≤ 10^87.9`, `L* ≤ 10^(1.050×10²⁹)`, `0.95K₀² ≤ log₁₀L* ≤ 6.2K₀²` | **HOLDS** (recomputed; relative differences ≤ 3×10⁻⁶). All are conditional on AK25b's structural steps, which neither the author nor I re-proved. The lower bracket is a floor *for this route's bookkeeping*, as labelled. |
| 4 | Thm 1.2's `ε ≈ 10^(−1.7×10²⁵)` via mg-f218 | **HOLDS**, and it is now conditional only on AK25b's structure, KSBFT §6 (AK25a, Haq26), and mg-f218 (audited HOLDS in `AUDIT-mg-f218.md`). Recomputed: `θ_W(L₁₂) = 10^(−1.717081×10²⁵)`. There is a nit about the strictness of ε′ (§4). |
| 5 | `K = 2.17×10⁴¹¹`; `K₀ = 1.301×10¹⁴`; `K₁₂ = 1.944×10¹²` | **HOLDS** (recomputed from the p.25 display). |
| 6 | "No cheaper case-(b) route (4 candidates, all negative)" | **HOLDS as a report of four failed attempts.** The doc correctly marks the existence question OPEN. Candidate 3's detail ("(5.2) at `t = Δ/d` gives `e^{1−ε₀}`") is **UNVERIFIABLE** here (AK25a not read). The candidate space is not exhausted; §5 lists untried candidates. |

**Bottom line.** Every number in the doc recomputes. The flashy claim is right in the form the doc
actually states it: "NOT REPRODUCED; inconsistent with the route as printed". It must **not** be
upgraded to "the authors' constant is wrong". That is UNDETERMINED, and §1.3 gives a concrete
reason for caution. The printed value matches, digit for digit, `L = 1/q₀ = 3^{w²}` at `ε = 1/6`
with width **exactly 4×10⁹**. That pattern suggests a specific (and different) computation on the
authors' side. It is CONJECTURED here, not established.

---

## 1. Claim 1: eq (1.5)

### 1.1 What (1.5) requires — PROVEN

KSBFT p.2 says "Our proof allows us to take `ε := 3^{−3^{16×10¹⁸}}`" and omits the derivation. p.26
says AI was used "as a way to compute the constant in (1.5)". Thm 1.2 is "Theorem 1.3 + 1.4 + 1.5"
(p.5). So:

- case (a) is width `> K`, via Thm 1.4;
- case (b) is width `< K` with `π > L`, via Thm 1.5;
- case (c) is `π ≤ L`, via Thm 1.3 at `D = L`.

`η_D = (D+1)^{−4(D+1)}/4096` is decreasing in `D`, so (1.5) is a valid choice only if
`η_L ≥ 3^{−3^p}` with `p = 1.6×10¹⁹`. That is,
`4(L+1)·log₃(L+1) + log₃ 4096 ≤ 3^p`. With `u = log₃(L+1)`, this is `u + log₃(4u) ≤ p` (the 4096
term is negligible), so `u ≤ p − log₃(4p) ≈ p − 41`.

**So (1.5) needs the authors' `L ≤ 3^{1.6×10¹⁹}`.** The doc's "implies `log₃ L ≈ 1.6e19`" is right,
read as this upper bound. That is the direction that matters: a smaller `L` would still validate
(1.5).

### 1.2 Is the floor a floor, and for what? — PROVEN for AK25b as written

**Which width case (b) must handle.** Case (a) needs Thm 1.4-type output
`δ > 1/e − ε₀ ≥ C_BFT + ε`, so `ε₀ < 1/e − C_BFT = 0.0915`. KSBFT's only large-width tool is §6,
whose p.25 bound is decreasing in `ε₀` (the instrument checks monotonicity on a grid). So the
**least width case (b) can be left with is `K₁₂ = 1.944×10¹²`**, and the paper as printed actually
uses `K = 2.17×10⁴¹¹`. Case (b) must then cover width up to `K₁₂ − 1` with target
`δ > 1/2 − ε′ ≥ C_BFT`, so `2ε′ ≤ 1 − 2C_BFT = 0.4472`.

**Floor, coefficient 1 (structural in AK25b's proof).** AK25b's only route from "`δ_x ≤ 1/2 − ε′`
for all x" to "bounded variance" is Thm 2.6 → Cor 2.4 (p.4–5). The chain is:

1. It gives `q(x) ≥ q₀ = (2ε′)^{w²}`, hence `σ² ≤ S = O(q₀⁻²)`.
2. The contradiction with Thm 3.1 needs `L_{3.1} > S`.
3. Inside Thm 3.2, the threshold `η` must satisfy `q ≤ η ⇒ σ² ≥ 2L_{3.2} > S`. Since log-concave
   laws with `σ = Θ(1/q)` exist (geometric laws), this forces `η = O(q₀)`.
4. Case 2 of (13) needs `|A| ≥ ηµ²N/20 ≥ 4Ct`, so `K₃.₂ ≥ 80Ct/(ηµ²) > 1/η`.
5. The range bound is `π ≤ |A||B| ≤ |B|² < K₃.₁²`. Even crediting only `π < K₃.₁`
   (dropping the square) gives `L ≳ 1/η ≳ 1/q₀`, i.e. `log₃ L ≳ w²·log₃(1/2ε′)`.

At `w = K₁₂`, that is **`2.77×10²⁴`** (instrument, part B).

**Floor, coefficient 2.** This is the doc's `5.54×10²⁴`. It uses `π ≤ |A||B| ≤ |B|² < K₃.₁²`, a
correct bound for this bookkeeping. I did not prove that no honest bookkeeping of AK25b can avoid
the square. So "unavoidable" is **OVERSTATED** for the factor 2 only. It does not matter: both floors
exceed the `1.6×10¹⁹` that (1.5) needs by a factor of more than 10⁵ in `log₃ L`.

**Widths that would fit.** The instrument computes these:

| floor used | `ε′ = 1/6` | `ε′ = 1/2 − C_BFT` |
|---|---|---|
| coefficient 1 (`q₀` alone) | **`4.0000×10⁹`** | `4.674×10⁹` |
| coefficient 2 | `2.83×10⁹` | `3.30×10⁹` |

p.25's formula prints a width of `4×10⁹` only at deficit `ε₀ = 0.374`, which exceeds `1/e` and is
unusable. **No width bound printed in KSBFT is small enough.**

### 1.3 Why the "the authors are wrong" reading is UNDETERMINED

The floor binds every route of the form "KSBFT §6 width, then AK25b Thm 2.6 as printed, then AK25b
Thm 1.3". It does **not** bind these alternatives, none of which the evidence excludes:

- **(R1) A sharper heavy-atom bound.** An authors' private strengthening of Thm 2.6 would change
  the floor. For example, `(2ε)^{O(w)}` would give `log₃ L = O(w)`, or about 10¹² to 10¹³ at `K₁₂`,
  which is *below* `1.6×10¹⁹`. Doc §4 candidate 2 shows this is open, not refuted.
- **(R2) A smaller width bound from outside §6.** Air26 (the Kahn–Saks resolution, cited on p.4)
  might certify `δ > 1/3` at a much smaller width. I did not read it, and its constants are unknown
  to me. **UNVERIFIABLE.**
- **(R3) A different reading of Thm 1.5's `K`.** For example, the authors may have used a width
  figure from an earlier draft of §6.
- **(R4) The pattern in (1.5) itself.**
  - `3^{16×10¹⁸}` is exactly `1/q₀ = (2ε)^{−w²}` at `ε = 1/6` (the ε the paper names on p.5,
    "by taking ε = 1/6") with `w = 4×10⁹` exactly. The instrument's row 1 above is `4.0000×10⁹`.
  - The base 3 of (1.5) is `1/(2ε)` at `ε = 1/6`.
  - This strongly suggests the authors' computation took `L ≈ 1/q₀`. That silently drops AK25b's
    polynomial loss (degree 13, i.e. `log₃ L ≈ 13w²`) and used a width of `4×10⁹` that I cannot
    source.
  - **CONJECTURED**, and it would mean (1.5) is too large by the factor that loss implies, not
    that some other route exists. But it is a reconstruction from digits, not evidence.

**What would separate these.** Any one of the following would settle it: the authors' derivation,
Air26's width constant, or a sharper Thm 2.6. None is available. **Safe statement for
pm-onethird:** "(1.5) is not derivable from the printed ingredients (Thm 1.4's §6 width plus AK25b
as written); the nearest fit is `L = (2ε)^{−w²}` at `ε = 1/6`, `w = 4×10⁹`, which omits AK25b's
Thm 1.3 loss and uses an unsourced width." Do not say "their ε is wrong". Their ε could be *valid*
under a route we have not seen, and qualitatively Thm 1.2 is unaffected either way.

---

## 2. Claim 2: the trace

### 2.1 Thm 2.6 and `q₀` — HOLDS, with one edge-case repair

**AK25b p.4–5, re-derived.** Take `a ∈ A`. Conditioned on `a ≺ x` (uniform on `E(P + a<x)`),
Thm 2.1 gives `P(x ≺ B | a ≺ x) ≥ ∏_b P(x≺b | a≺x) ≥ [ε/P(a≺x)]^{|B|}`. So
`P(a≺x≺B) ≥ ε^{|B|}·P(a≺x)^{1−|B|} ≥ ε^{|B|} ≥ ε^w`. Then, conditioned on `x ≺ B`, the same step
over `a ∈ A` gives `P(A≺x≺B) ≥ ε^{w|A|}·P(x≺B)^{1−|A|} ≥ ε^{w²}`. With `2ε` for `ε`
(`δ_x ≤ 1/2−ε` gives `P(a≺x≺b) ≥ 2ε` by a union bound), and `{A≺x≺B} = {f(x) = |D|+1}`, we get
`q(x) ≥ (2ε)^{w²}`.

- AK25b p.5 prints `P(f(x) = |A|+1)`. That is a typo for `|D|+1`, and the doc has it right.
- `D` is an ideal (`z < y ⇒ P(z≺x) ≥ P(y≺x)`) and `U` is a filter, so both claims HOLD.

**Edge case (doc §3.1, BROKEN as an intermediate).** The doc writes
`P(A≺x≺B) ≥ (2ε)^{|A||B|} ≥ (2ε)^{w²}`. If `D = ∅` (x minimal-ish, so `A = ∅`), then hypothesis
(4) is vacuous and `(2ε)^0 = 1` is false.

- Witness: `P = {0<1} + {2}`, `x = 0`. Then `δ_x = 1/3` and `U = {1,2}`, but `q(x) = 2/3 < 1`.
- The correct bound is `∏_b P(x≺b) ≥ (1/2+ε)^{|B|} ≥ (2ε)^w`. In general the exponent is
  `max(|A|,1)·max(|B|,1) ≤ w²`.
- The census (part E, n ≤ 6, 19 610 (poset, x) cases at n = 6) finds **0 violations** of the
  repaired form. It finds 7 454 violations of the literal form, all with A or B empty (the instrument
  aborts if any violation has both nonempty).
- **The final `q₀ = (2ε)^{w²}` and every downstream number are unaffected.**

### 2.2 Prop 2.3, the easy direction, and `η` — HOLDS

I checked each step of doc §3.2:

- `a ≤ 2/q`;
- `r_{j−1} < 2^{−1/a}` (nonincreasing ratios, product `< 1/2`);
- `Σt²ρ^t = ρ(1+ρ)/(1−ρ)³ ≤ 2/(1−ρ)³`;
- `1−2^{−x} ≥ x/2` on `[0,1]`;
- `36a³`, then `18qa³ ≤ 144/q²`, and `8/(3q²) + 144/q² < 147/q²`, doubled for both sides.

Easy direction: `P(|X−μ|<t) ≤ q(2t+1) = 1/2 + q ≤ 3/4` at `t = 1/(4q)`, so `Var ≥ 1/(64q²)`.
Then `q ≤ η = 1/(16√(S+1))` gives `σ² ≥ 4(S+1) = 2·L_{3.2}` with `L_{3.2} = 2(S+1)`. That is
exactly what AK25b's Thm 3.1 → 3.2 step (`2L` for `L`, `µ/4` for `µ`) needs.

### 2.3 §3.4 table and the degree — HOLDS

Each row was checked against AK25b p.8–10.

- **(17).** `P(g=j) > η ⇒ |j−Eg| < σ/√η` (Chebyshev), and `P(|g−Eg| ≥ 2σ/√η) ≤ η/4`. So
  `D = 3σ/√η = 3√300·η^{−1.5}`.
- **(22), case `j_{k+1} ≥ N/2`.**
  `(N/4−D)/(5M/µ) ≥ (N/8)(µ/5M) ≥ µ³/40`, using `N ≥ µ²M`, times `P ≥ 1−η/4 ≥ 3/4`, gives
  `3µ³/160`.
- **(22), case `j_{k+1} ≤ N/2`.** `(N−j)/M ≥ µ²/4`, times 3/4. The minimum over the two cases is
  `3µ³/160`.
- **(19).** `r_k ≥ γ − 2D/C ≥ γ/2` once `C ≥ 4D/γ`.
- **Lemma 4.4.** Re-derived in full.
  - `(m−i)/(n−ℓ+1) ≥ a(1−B/K)` and `(i−1)/ℓ ≤ b(1+2B/K)`, using `1/(1−x) ≤ 1+2x` for `x ≤ 1/2`.
  - `R ≥ 1 − (3B+1)/K·b/(1+b) ≥ 1 − (3B+1)/K`.
  - There are `B+1` disjoint events, each `≥ P/e`, so `P ≤ e/(B+1)`.
  - `ε′ = η/2` (AK25b's "≤ ε/2" in the proof of (20)) gives `B = ⌈2e/η⌉`.
- **(20).** `T = γ′C`, so `C = 2·(T/D)·D/γ`.
- **(18).** `γ′(1+D/T)^{t−2} < 3/η`, and `ln(1+x) ≥ x/2`.
- **(13).** `|I| < 2Ct ≤ |A|/2` with `|A| > ηµ²K/20`, so `K₃.₂ = 80Ct/(ηµ²)`.

**Degree in `x = 1/η`.** Term by term:

- `K₄.₄ ∝ x²`, and `T/D ∝ x²`;
- `D ∝ x^{1.5}`;
- `C ∝ (T/D)·D ∝ x^{3.5}`;
- `t ∝ x²·log x`;
- `K₃.₂ ∝ C·t·x ∝ x^{6.5}·log x`;
- `L = (2K₃.₂)² ∝ x^{13}·log²x`.

**Degree 13, HOLDS.** The instrument's ratio `log L / log x` is 13.656 at `w = 10` and
13.000000 at `w ≥ 10⁶`.

**Not re-proved (by the author or me).** These are AK25b's structural steps: Thm 4.1 reductions in
Lemmas 4.3/4.4, the chain reduction and dualisation in Thm 3.1's proof, Obs 4.2, and (7). The doc
flags this in its §3.7, correctly.

---

## 3. Claim 3: the numbers — HOLDS

These come from independent float-log code (part B). The doc's value is in parentheses.

| quantity | recomputed | doc |
|---|---|---|
| `log₁₀ L(4,1/6)` (width ≤ 3) | 119.1067 | 119.107 |
| `log₁₀ L(3,1/6)` (width ≤ 2) | 87.8825 | 87.8825 |
| `log₁₀ L*` (width ≤ `K₀`) | 1.050046×10²⁹ | 1.050046×10²⁹ |
| `log₁₀ L₁₂` (width ≤ `K₁₂`, `ε′ = 1/2−C_BFT`) | 1.717081×10²⁵ | 1.717081×10²⁵ |
| `log₁₀ L* / K₀²` | 6.2026 = 13·log₁₀3 | ≤ 6.2 |

The bracket `[2log₁₀3, 13log₁₀3] = [0.954, 6.203]` HOLDS. Its lower end is a floor for this
route's bookkeeping, with the factor-2 caveat of §1.2 (coefficient 1 gives 0.477).

---

## 4. Claim 4: Thm 1.2's ε via Thm 1.3″ — HOLDS

mg-f218 Thm 1.3″ (audited HOLDS) gives `δ ≥ C_BFT + min(θ₀, θ_W(D))`, where
`θ_W(D) = C_BFT/((5+3√5)(D+1)+1)`, for every `D ≥ 2`. At `D = L₁₂`:
`θ_W = 10^(−1.717081×10²⁵)`, which is far below `θ₀ = 6.80×10⁻⁶`. Cases (a) and (b) can be given
margins of the same size at negligible cost. So **`ε = 10^(−1.717×10²⁵)`**, which is
single-exponential and matches the doc's `≈ 10^(−1.7×10²⁵)`.

- For the 1/3 statement at `L*`, `θ_W(L*) = 10^(−1.050046×10²⁹)`, which matches.
- Paper Thm 1.3 at `L₁₂` gives `log₁₀log₁₀(1/η) = 1.717×10²⁵`, which matches.

**Dependencies now:**

- AK25b's structural steps (unaudited here);
- KSBFT §6, for `K₁₂`, which rests on AK25a and Haq26 (mg-c929, audited by mg-e015);
- mg-f218 (audited).

The doc's "if mg-f218 holds" / "UNAUDITED" labels in §0 item 5 and the §5.2 table are now stale.

**Nit.** The doc takes case (b) at `ε′ = 1/2 − C_BFT` exactly, and case (a) at deficit
`1/e − C_BFT` (the latter flagged "a hair less"). At those exact values the case gives only
`δ > C_BFT`, with no uniform margin. Both must be taken slightly smaller. The effect on
`log₁₀ L₁₂` is below the shown digits.

---

## 5. Claims 5 and 6

**K — HOLDS.** From the p.25 display `w ≤ (442368/ε⁴)·log²(18432√3/ε³)`:

- `log₁₀ K(10⁻¹⁰⁰) = 411.3374`;
- `K₀ = K(1/e−1/3) = 1.3011×10¹⁴`;
- `K₁₂ = K(1/e−C_BFT) = 1.9441×10¹²`.

The validity of the display under the largeness hypothesis (6.8) was audited under mg-e015 and is
not re-checked here.

**Negatives — HOLDS as a report, and not exhaustive.** The four candidates are:

1. Restricting to `Π(x)`. This is correct, and the exponent stays `≤ w²`.
2. Per-chain gaps. Correct: XYZ controls one-sided events only. OPEN, as the doc says.
3. §6 structure bounding `σ(x)`. The pairwise-only argument is right. The `(5.2)` arithmetic is
   **UNVERIFIABLE** without AK25a.
4. Range through width. Correct: two parallel chains have width 2 and range `n/2`.

The doc claims "none found", not "none exists". That is the right mark. Candidates **not** tried by
the doc, and not by me:

- (i) a smaller width bound for case (a) from Air26, which shrinks `w` but not the `w²` shape;
- (ii) a dimension-free heavy-atom bound via Kahn–Saks/Linial-type log-concavity on `f(x)`
  directly (e.g. Grünbaum-type, as in AK25b (9));
- (iii) proving Thm 2.6 with `|A| + |B|` in place of `|A||B|` by a single joint XYZ step. This would
  need positive correlation of `{a≺x}` and `{x≺b}`, which XYZ does not give;
- (iv) bypassing AK25b's Thm 3.1 squaring (§1.2).

---

## 6. What I did not do

- I did not re-prove AK25b's structural steps (§2.3 list). Everything L-shaped is conditional on
  them.
- I did not read AK25a, Haq26 or Air26. So candidate 3's `(5.2)` detail and route (R2) are
  UNVERIFIABLE.
- I did not audit mg-c929 or mg-f218 myself. I rely on the audits mg-e015 and `AUDIT-mg-f218.md`.
- Part E is EMPIRICAL (n ≤ 6) and tests only the Thm 2.6 inequality as consumed, not AK25b's §4.
- I did not contact the authors, so §1.3's (R4) is a digit-pattern reconstruction, CONJECTURED.
- I did not edit `STATE.md` or `docs/KSBFT-G-constants.md`. Suggested edits to the subject doc, for
  pm-onethird to route:
  - (a) repair §3.1's exponent to `max(|A|,1)·max(|B|,1)`;
  - (b) mark mg-f218 as audited;
  - (c) soften "unavoidable floor" to "floor for AK25b as written (coefficient 1 structural)";
  - (d) add §1.3's `w = 4×10⁹` observation.
