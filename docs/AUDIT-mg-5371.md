# AUDIT of mg-5371 (KSBFT-L): the family refuting a poly AK25b Thm 2.6, and the ceiling `2ε/w`

`mg-2198`, 2026-09-26. Independent auditor, fresh context, not the author.

- **Under audit:** `docs/KSBFT-L-heavy-atom.md` and `code/ksbft_l_heavy_atom_5371/`.
- **Primary source:** I read AK25b (Aires–Kahn, arXiv:2510.26134v1) directly, downloaded from
  arxiv.org, §2 pp. 4–5 (Thms 2.1, 2.2, Prop 2.3, Cor 2.4, Thm 2.5, Remark, Thm 2.6 and its proof).
- **My instrument:** [`code/audit_ksbft_2198/`](../code/audit_ksbft_2198/). `./run_all.sh` takes about
  1 s on one core, uses exact `Fraction` arithmetic except §E, and has no randomness.
  - It imports **nothing** from the audited directory or from mg-b852's code.
  - The downset DP, the F(m,k) builder, the q₀→L chain and the width bound were all re-written from
    the documents' formulas.
  - Every check prints PASS/FAIL. The three negative controls print FIRES.
  - Transcript: `out_audit_2198.txt` (`ALL (after [F]): PASS`).

Marks: **PROVEN** (proof here or re-checked line by line), **EMPIRICAL** (instrument and range
named), **CITED**.

## Verdict table

| # | claim (mg-5371) | verdict |
|---|---|---|
| 1a | `F(m,k)` with `j = k/2` (and any `1 ≤ j < k`) meets **all** of Thm 2.6's hypotheses, with (4) at `ε = 1/(k+1)` | **HOLDS** |
| 1b | `P(A≺x≺B) = C(k,j)^m / (C(mk,mj)(mk+1))`, and the bound `(πk/2)^{−m/2}·√(2/(mk))` (k even, j = k/2) | **HOLDS** |
| 1c | "Thm 2.6 cannot be `poly(ε/w)` nor `(2ε)^{o(w)}`" | **HOLDS**, with a quantifier scope the doc states only partly (below) |
| 1d | "true exponent between ≈0.53–0.63·w·log(1/ε) and w²·log(1/ε)" | **OVERSTATED (minor)**: the family's coefficient is in `(1/2, 0.631]` and tends to 1/2 as ε→0. "0.53" is not a bound. The doc's own `(w/2)log(1/ε)(1−o(1))` is the correct form. |
| 2a | Ceiling: under `width ≤ w`, `δ_x ≤ 1/2−ε`, no lower bound on `q(x)` can exceed `1/((w−1)(1/(2ε)−1)+1)` | **HOLDS** for `ε ≤ 1/6`, exactly at `ε = 1/(2(k+1))` with k even |
| 2b | "…≈ 2ε/w", and the §0/§4 table row "`2ε/w` (the §2.3 ceiling); best possible" | **OVERSTATED (minor)**. The proven ceiling is `≥ 2ε/w` always, and is **1.5× larger** at ε = 1/6. There the best-possible row is `log₁₀ L* = 251.2`, not 253.5. The Thm 1.2 column (ε = 0.2236 > 1/6) has **no** family member, so "best possible" is unproven there. |
| 2c | Caveat: the ceiling does not bind the application, because `δ(F(m,k)) = 1/2` | **HOLDS** (m ≥ 2) |
| 3 | §0/§4 table (`L*`, `L(4,1/6)`, Thm 1.2 ε for 6 shapes), chained through mg-b852 | **HOLDS**. All 18 numbers reproduced independently. |
| 4 | EMPIRICAL items (non-log-concavity counts, semiorders) are not presented as proof | **HOLDS**. Where anything is off, it is under-claimed, not over-claimed. |
| — | §1 typos in AK25b (`max(C)` → `max(D)`; `|A|+1` → `|D|+1`) | **HOLDS**: both are present verbatim in the arXiv v1 text. |
| — | (L1) loss factor `C(2m,m)/2^m ≥ 2^m/(2√m)` | **HOLDS** |
| — | §3.1 Attempt 2 "product bound FALSE on F(m,2)" | **HOLDS**, but the doc's justification is heuristic. A one-line rigorous proof is below. |

Nothing is BROKEN.

---

## 1. The family against AK25b Thm 2.6

**Thm 2.6 as printed (CITED, p.4).**

- `P` is the disjoint union of `{x}`, `D`, `U`, with `D` an ideal and `U` a filter.
- `A := max(C)` (typo for `max(D)`) and `B := min(U)`, with `|A|, |B| ≤ w`.
- (4): `P(a≺x≺b) ≥ ε` for all `a ∈ A`, `b ∈ B`.
- Conclusion: `P(A≺x≺B) ≥ ε^{w²}`.

**Note:** in Thm 2.6, `w` is a bound on `|A|` and `|B|`, **not** the width of `P`. In the application
(p.5, `δ_x ≤ 1/2−ε`, `2ε` in (4)), `|A|, |B| ≤ width`.

**1a — HOLDS.** Let `D = {c_{i,l} : l ≤ j}`. It is downward closed, since chains are disjoint and
`x` is isolated. `U` is the complement of `D` minus `x`, so it is upward closed. Then
`max D = {c_{i,j}} = A` and `min U = {c_{i,j+1}} = B`. The theorem needs no relation between `x`
and `D ∪ U`.

(4) holds in both cases:
- **Same chain:** `P(a_i≺x≺b_i) = 1/(k+1)`, because x's slot among `C_i` is uniform on k+1 slots.
- **Different chains (`i ≠ l`):** `{a_i≺x≺b_l} = {a_i≺x} \ {b_l≺x}`, so
  `P ≥ (1 − j/(k+1)) − (1 − (j+1)/(k+1)) = 1/(k+1)`.

The shuffle fact (U) is standard and correct. Restricted to any set of components, the
interleaving of a disjoint union is again uniform.

My DP checks the hypotheses structurally (ideal, filter, max, min) together with min(4), for
`(m,k) ∈ {(1..5,2), (2,4), (3,4), (2,6), (2,3), (2,5)}`: PASS. It also reproduces the author's
cross-chain values 11/30, 17/70, 1129/6006, 6841/43758 exactly.

- **Negative control:** replacing `b_l` by `c_{l,j}` gives `P = 2/15 < 1/3`, so the check can fail
  (FIRES).

**1b — HOLDS.**

- **The event.** `{A≺x≺B}` is the event that the set before `x` is exactly `D`. Every `d ∈ D` lies
  below some `a`, and every `u ∈ U` above some `b`.
- **The count.** This gives `e(D)e(U)/e(P)`, with
  - `e(D) = (mj)!/(j!)^m`
  - `e(U) = (m(k−j))!/((k−j)!)^m`
  - `e(P) = (mk+1)!/(k!)^m`

  The ratio simplifies to the stated closed form. The DP matches it on all 10 instances.
  - **Negative control:** dropping the `(mk+1)` factor fails (FIRES).
- **The bound.** It uses `C(k,k/2) ≤ 2^k/√(πk/2)` and `C(mk,mk/2) ≥ 2^{mk}/√(2mk)`. These are the
  standard `C(2n,n) ≤ 4^n/√(πn)` and `C(2N,N) ≥ 4^N/(2√N)`, with `mk` even since k is even. The
  step `√(2mk)/(mk+1) ≤ √(2/(mk))` is trivial.
  - Checked in log space for k even in 2..20 and m in 1..60: PASS.
  - The k = 2 statement `2^m/(C(2m,m)(2m+1)) < 2^{−m}` was checked exactly for m ≤ 200: PASS.
  - The identity `= 2^m m!²/(2m+1)!` holds.

**1c — is "cannot be (2ε)^{o(w)}" correctly quantified? HOLDS, with this scope.**

- **Thm 2.6 form (w = |A| = |B| = m).**
  - `F(w,2)` satisfies (4) at every `ε ≤ 1/3` and has atom `< 2^{−w}`.
  - A bound `ε^{h(w)}` valid at any single `ε ≤ 1/3` therefore needs
    `h(w) ≥ w·log 2 / log(1/ε)`, which is linear.
  - So no `h = o(w)` works, and no `poly(ε/w)` works either.
- **Application form (w = width = m+1, ε_δ with `δ_x ≤ 1/2−ε_δ`).**
  - At `ε_δ = 1/6` the atom is `< 2^{−(w−1)}`, so `(2ε_δ)^{h(w)}` needs
    `h(w) ≥ 0.6309(w−1)`.
  - The author's `w` vs `w−1` bookkeeping is consistent: §0 item 1 uses the Thm 2.6 form, and the
    §2 "application" paragraph uses `2^{−(w−1)}`.
- **Scope not covered.** The family covers only `ε ≤ 1/3` in (4), equivalently `ε_δ ≤ 1/6`.
  - An `ε`-dependent statement "for ε_δ > 1/6, the exponent is o(w)" is **not refuted** by F(m,k).
  - That range includes Thm 1.2's `ε_δ = 1/2 − C_BFT ≈ 0.2236`.
  - The doc flags this for the floor row's Thm 1.2 line ("extrapolation"), but §3.5's
    "`(2ε)^{o(w)}` REFUTED" does not carry it.
  - As a statement uniform in ε (the natural reading of Thm 2.6), the refutation is correct.

**1d — minor.**

- **The coefficient.** On the family, the exponent coefficient is
  `log(1/atom)/(m log(k+1)) → (k log 2 − log C(k,k/2))/log(k+1)`. It takes the values:
  - 0.6309 at k = 2
  - 0.6094 at k = 4
  - 0.5847 at k = 10
  - 0.5484 at k = 100
  - → 1/2 as k → ∞ (`out_audit_2198.txt` [B], exact binomials at m = 2000)
- **The consequence.** "Between ≈0.53–0.63·w·log(1/ε)" misstates the lower end. The correct lower
  end is `(1/2)(1−o(1))`, which the doc also states correctly elsewhere.

## 2. The ceiling

**2a — HOLDS.**

- **The computation.** By (F4), `P(c_{i,l}≺x) = 1 − l/(k+1)`. So
  `δ_x = max_l min(l, k+1−l)/(k+1)`.
  - For **k even** this is `k/(2(k+1)) = 1/2 − 1/(2(k+1))`.
  - For **k odd** it is exactly 1/2, so odd k supplies no ceiling point. The doc correctly restricts
    to even k; DP confirms `δ_x = 1/2` for F(2,3), F(2,5), F(3,3).
  - `q(x) = 1/(mk+1)` (f(x) uniform, DP-checked). With `m = w−1` and `k = 1/(2ε) − 1`, this is
    `1/((w−1)(1/(2ε)−1)+1)`, confirmed on F(2,2), F(2,4), F(3,2).
- **Extension to other ε.** Hypotheses are monotone in ε, and `δ_x ≤ 1/2−ε_k` implies
  `δ_x ≤ 1/2−ε` for `ε ≤ ε_k`. So for any `ε ≤ 1/6`, the ceiling holds at the largest admissible
  even k. That is still `Θ(ε/w)`.
- **Scope.** For `ε ∈ (1/6, 1/2)` there is no member, and no ceiling is proven there.

**2b — minor OVERSTATEMENT.**

- **The inequality.** `(w−1)(1/(2ε)−1) + 1 ≤ w/(2ε)` always holds, so the proven ceiling is ≥ `2ε/w`.
  "No bound can beat ~2ε/w" is right only up to the factor `ceiling/(2ε/w)`:
  - 1.8 at w = 3
  - 1.5 as w → ∞, at ε = 1/6
  - → 1 as ε → 0
- **Consequence for the table.** The row labelled "2ε/w (the §2.3 ceiling); best possible" uses a
  q₀ that is 1.5× *below* the proven ceiling at ε = 1/6. The best possible under this route is:

| quantity | at the exact ceiling `1/(2w−1)` | the doc's `2ε/w` row |
|---|---|---|
| `log₁₀ L*` | **251.2** | 253.5 |
| `log₁₀ L(4,1/6)` | **72.0** | 75.4 |

- **Conclusions unaffected.** "Only a poly bound on the max atom gives `L* = poly(K₀)`, ≈10^{250}"
  is unaffected.
- **Thm 1.2 column.** Its "−229.7" at ε = 0.2236 is a hypothetical row. It is not a proven
  best-possible value there (2a scope).

**2c — HOLDS.** For m ≥ 2, `P(c_{1,l}≺c_{2,l}) = 1/2` by symmetry, so `δ(F(m,k)) = 1/2`. The
ceiling therefore concerns the local hypothesis `δ_x ≤ 1/2−ε`, not the global one `L*` actually
uses. The doc says this itself.

## 3. Consequence arithmetic — HOLDS

**Code provenance.**
- `consequences.py`'s `L_from_q0` is a verbatim copy of `code/ksbft_g_constants_b852/constants.py`
  `L_AK` after its first line. I compared them by eye.
- The author's control reproduces mg-b852's 119.107 and 1.0500e29.

**My independent re-implementation** (§E of `audit_2198.py`):
- **Source.** Written from mg-b852's *document* (§3.2–3.4 formulas: η, B, K₄.₄, T/D, D, γ, C, t,
  K₃.₂, K₃.₁, L = K₃.₁²) in float log-space. mg-b852 is audited by mg-5562.
- **Width bounds.** K₀ = 1.3011e14 and K₁₂ = 1.9441e12, recomputed from the p.25 form.
- **Coverage.** All three columns of all six rows match the doc within 0.2%:

| shape | `log₁₀ L*` | `log₁₀ L(4,1/6)` | `log₁₀ ε` (Thm 1.2) |
|---|---|---|---|
| `(2ε)^{w²}` | 1.0500e29 | 119.1 | −1.7171e25 |
| `(2ε)^{0.6309w}` | 5.0916e14 | 74.7 | −5.572e12 |
| `(2ε)^w` | 8.0703e14 | 81.6 | −8.832e12 |
| `(2ε/w)^w` | 2.4681e16 | 100.4 | −3.194e14 |
| `(2ε/w)³` | 633.67 | 100.4 | −559.0 |
| `2ε/w` | 253.54 | 75.4 | −229.7 |

- **Degree.** The local degree `d log L / d log(1/q₀)` is 13.03, which confirms "L ≈ c·q₀^{−13}".
- **Negative control:** a planted 12/13 scaling of the w² row is caught (FIRES).
- **Reproducibility.** I re-ran the author's whole `run_all.sh` in a scratch copy. All five `out_*.txt`
  files came out byte-identical to the committed ones.

The doc labels the floor row's Thm 1.2 line "extrapolated" (see 1c), and that label is right.

## 4. EMPIRICAL vs PROVEN — HOLDS

**§3.3 (chain counts).**
- **Labelling.** It is labelled EMPIRICAL in its header, in §0 item 4 and in §3.5. The 855/8,207
  and 85 counts are given with instrument, range and seed.
- **My check of the explicit instance.**
  - masks `[112,113,272,115,0,0,0,115,0]`, `x = 2`, `C = {1,3,5}`.
  - The masks are transitively closed as given.
  - C is a chain inside `Π(x) = {0,1,3,5,6,7}`, with `w(Π) = 2` and `w(Π−C) = 1`.
  - `N_C(x)` counts are `[20,120,114,138]` out of `e(P) = 392`.
  - Stanley's `f(x)` is log-concave on the same poset (control).
- **What this means.** This exact instance **proves** non-unimodality, and hence non-log-concavity
  (`114² < 120·138`). So "per-chain counts are not log-concave in general" is actually PROVEN; only
  the frequencies are empirical. The doc under-claims here, which is harmless.
- **Trivial example.** `[2,1,2,1]` confirmed.

**§3.4 (semiorders)** is labelled "EMPIRICAL, inconclusive" and claims nothing. I did not re-derive
it.

**PROVEN labels that contain heuristics**, all disclosed:
- **(L2) "PROVEN"**
  - Proven: the gap between the truth `< 2^{−m}` and AK25b's `3^{−m²}`.
  - Heuristic: the `≈2/√m` explanation, marked "(heuristic calculation, not used below)".
- **§3.1 Attempt 2 "FALSE on F(m,2)"**
  - The doc supports it with a heuristic integral for `P(A≺x) ≈ √π/(2√m)`. It is true
    rigorously: `P(A≺x) ≥ P(x last) = 1/(2m+1)`, and likewise `P(x≺B) ≥ 1/(2m+1)`. So
    `P(A≺x)P(x≺B) ≥ (2m+1)^{−2}`, while the joint event is `< 2^{−m}`.
  - My exact DP (m ≤ 6) shows the ratio joint/product falling 0.75 → 0.046, and `P(A≺x)` tracking
    `√π/(2√m)` (0.341 vs 0.362 at m = 6).
  - **Recommended edit:** cite the one-line bound instead of the integral.
- **§3.3's "PROVEN: `P(N_i = k_i) ≥ 2ε`".** I did not re-check it (see below).

## Required / recommended edits (to pm-onethird; STATE.md not touched)

1. **§0/§4 table, row "2ε/w (ceiling)".** Use the exact ceiling `1/((w−1)(1/(2ε)−1)+1)`, which is
   `1/(2w−1)` at ε = 1/6. This gives `log₁₀ L* = 251.2` and `log₁₀ L(4,1/6) = 72.0`.
   Alternatively, relabel the row "≈ ceiling up to factor 1.5". In either case, mark its Thm 1.2
   entry as not covered by F(m,k) (ε = 0.2236 > 1/6).
2. **§0 item 1.** Replace "≈0.53–0.63" with "∈ (1/2, 0.631], → 1/2 as ε → 0".
3. **§3.5 row "(2ε)^{o(w)} REFUTED".** Add "for ε_δ ≤ 1/6 (ε ≤ 1/3 in (4)); at Thm 1.2's ε_δ ≈
   0.224 no member of F(m,k) applies".
4. **§3.1 Attempt 2.** Replace the heuristic integral with `P(A≺x), P(x≺B) ≥ 1/(2m+1)`.
5. **Optional, §3.3.** The exact instance already proves non-log-concavity, so the label can say
   "PROVEN by an exact instance; frequencies EMPIRICAL".

## What I did not do

- I did **not** re-derive mg-b852's q₀→L chain *structure*: AK25b §§3–4, or the choice of constants
  in its §3.4 table. That is mg-5562's audit. I re-implemented the formulas as written and
  re-computed them.
- I did **not** independently re-count the 855/8,207 and 85 (Dilworth probe) or the 3,390/465
  (chain probe). I only re-ran the author's code (byte-identical output) and independently verified
  the one explicit instance that carries the logical weight.
- I did **not** re-check §3.3's PROVEN per-chain median atoms (`P(N_i ≤ k_i) ≥ 1/2+ε`, etc.), §3.2's
  circularity argument, or §3.4's semiorder table.
- I did **not** re-verify Prop 2.3's constant `294` or anything in AK25b beyond §2.
- I did **not** look for a family covering `ε_δ ∈ (1/6, 1/2)`, where the o(w)-refutation and the
  ceiling are currently unproven.
- **Negatives, with what I tried.** I tried to break:
  - (4) on cross pairs: exact, all ≥ 1/(k+1).
  - The closed form: 10 instances, exact match.
  - The central-binomial bound: log-space sweep of 600 (k,m) pairs, no violation.
  - The ceiling formula: it matches q(x) exactly. Odd k is not a counterexample to anything, since
    δ_x = 1/2.
  - The table: 18 numbers, all within 0.2%.

  None broke.
