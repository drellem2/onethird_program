# AUDIT of mg-7bfc (KSBFT-R): the padded witnesses and the revived Step-6 (T∃) route

`mg-244e`, 2026-09-26. The subject is `docs/KSBFT-R-window-padding.md` (commit `fc3a42c`), together
with `code/ksbft_r_window_padding_7bfc/`. I am not its author. I re-derived every proof by hand before
reading the author's code. I then rebuilt every padded poset from the doc's own words, in code that
shares nothing with the author's.

**Instrument.** `code/audit_ksbft_244e/` (`sh run_all.sh`: about 1 min, exact `Fraction`s, fixed
seeds, 1 process). It uses different mechanics from the author's:
- `e(S)` is memoised top-down over subsets;
- `P[x<y] = e(P + x<y)/e(P)`.

It has 0 failed checks, and all 5 planted controls fire (listed in §6).

**Conditionality.** Every sentence below that places something "in the window" `𝒲 = {8 ≤ π ≤ L*}`,
or that says a least counterexample has `π ≥ 8`, is **CONDITIONAL**. It rests on two things:
- **[H]**, AK25a/AK25b/Haq26;
- **[D≤7]**, the range ≤ 7 computer proof of KSBFT-I.

[D≤7] has since been audited and HOLDS (`docs/AUDIT-mg-e8b4.md`, ticket mg-9268, commit `08eb0d3`).
It is still marked CONDITIONAL here, as the ticket requires. KSBFT-R's "audit mg-9268 pending" is now
stale.

Marks: **HOLDS / BROKEN / OVERSTATED / UNVERIFIABLE** per claim. Statements of mine are marked
PROVEN / EMPIRICAL / CONJECTURED.

---

## 0. Verdict in one screen

- **All of the padded exhibits HOLD.** I reproduced them exactly and independently: Thm 2.1's closed
  form, `attach_both(F_20,8)` with max certificate 13627/46282, the double hub with 5336/27441, and
  insulated `W*` (16,6,16) with `p_xy` = 5702887/39150182.
  - **Upgrade:** primality of `attach_low(F_N,R)` is **PROVEN** here for every `R ≥ 4`, `N ≥ R+2`
    (§2). The doc had it EMPIRICAL for `N ≤ 30`. So the A5 exhibit is proven prime for every
    `R ∈ [8, L*]`.
  - The A14 and A16 hosts also have ≥ 3 minimal and ≥ 3 maximal elements. So they satisfy KSBFT-Q's
    end condition O1 at **both** ends, which the doc did not check.
- **The minimal-counterexample structure (Prop 3.1) HOLDS.** It is genuinely forced: modules are
  chains, and the poset is connected both ways. The range ≥ 8 part is CONDITIONAL.
- **BROKEN: "mg-b447 Thm 4.1's refutation is of the continuity form"** (recommendation 2 and §4.2).
  - mg-b447's (T) is **existential**: "some balanced pair of `P[A]` or `P[B]` is still balanced in
    `P`" (`KSBFT-F` §1).
  - `W*` refutes that existential form, because `{x,y}` is the only incomparable pair on either side
    (recomputed, §4).
  - KSBFT-R's own §4.2 says as much ("what made `W*` a counterexample to (T∃)…").
  - The correct statement is narrower. mg-b447 refuted the existential (T) **on decomposable
    posets**, and that refutation does not reach prime posets.
- **OVERSTATED: the headline "padding kills every δ-direct route … inside the minimal-counterexample
  shape".**
  - The hosts satisfy (M1)+(M2), and in fact O1 too. They do **not** satisfy (M3): they have
    δ ≥ 0.45.
  - So what is killed is each route's lemma **as a class lemma on (M1)+(M2)**. A route that uses
    counterexample-only hypotheses (no balanced pair, `n`-minimality) is not touched.
  - The doc says this correctly in the §4 preamble. The headline, verdict 3 and recommendation 1
    drop it.
  - "Every" also rests on structural rows I did not audit, and A24 is undecided by the doc's own
    account.
- **OVERSTATED: "exactly three exact paddings", and "inside `𝒦_min` the witness can only appear
  reweighted".**
  - The completeness claim is false. A prime, both-connected 5-element poset holds the 2-antichain
    witness with its law **exactly** preserved, and the witness is not a module there (§3).
  - For the `2+2` witness I found no such prime host (EMPIRICAL negative, 4000 random prime hosts,
    `n ≤ 8`, control fires).
  - No downstream conclusion depends on this, because the doc goes on to analyse reweighted
    embeddings anyway.
- **The revived route (T∃^any), Prop 5.1: HOLDS as an implication, and it is CONDITIONAL.**
  - Two weaknesses the doc does not state:
    1. As written (ideals only), (T∃^any) fails on any poset whose only balanced pair is two maximal
       elements. The V poset is an example (control, §5). The fix is to allow filters too, i.e.
       mg-b447's "`P[A]` or `P[B]`".
    2. It is at least as strong as the conjecture on `𝒦_min ∩ 𝒲`. The doc's own §5.4(3) says so.
  - On prime, both-connected hosts it had 0 failures in 158 random samples with `n ≤ 8` (EMPIRICAL,
    far below the window).
  - "Best candidate" is a judgement, CONJECTURED.
- **Thm 2.3, Thm 5.2 and Cor 5.3 HOLD.**
  - Cor 5.3 is vacuous whenever `n < h(D,μ)`, and `h(D,μ) ≳ 10¹⁶` at `D = 8`. So §5.2's "a least
    counterexample is **exactly** a poset in which this happens at every cut" is OVERSTATED. It
    characterises nothing at the sizes a counterexample might have.
- **Cor 5.4 has two defects.**
  - Its proof is **off by one**. The argument needs `n ≥ 2h+2D+1`, not `2h+2D`.
  - It cites Thm 5.2 in the wrong direction. It needs Thm 2.3's symmetric bound, which does suffice.
  - It also assumes `P` already has a balanced pair, so it contributes nothing toward the
    conjecture. It is vacuous on a counterexample.
  - Verdict: minor repair, OVERSTATED as a lever.
- **(T_cont) "refuted inside `𝒦_min`-shaped window posets" is OVERSTATED as written, and the family
  bears it out.**
  - The doc shows a single point, and a single point cannot refute a modulus statement.
  - I computed the family `(M,6,M)` for `M = 16, 20, 24, 30` at range 9:
    - `p_xy` = 0.1457 at every size, to 4 dp;
    - `Δ₁` = 0.044 → 0.024.
  - `Δ₁ → 0` is **PROVEN** (KSBFT-F Lemma 2.1). That `p_xy` stays away from 1/2 is **EMPIRICAL**.
    The doc labels these the other way round.
  - Primality was checked at `n = 34` only.

---

## 1. Section 1: padding lemmas

| claim | verdict | how checked |
|---|---|---|
| Lemma 1.1 (module transfer: law of a module is uniform) | **HOLDS** | Re-derived: refill the module's slot set with any `τ ∈ L(M)`. External constraints are uniform over `M`, so fibres have equal size. |
| Cor 1.2: the three paddings are exact; the range formulas | **HOLDS** | Each is a substitution, so `W` is a module. Ranges re-derived (`π_{Q[q←W]}(w) = π_W(w) + π_Q(q)`: `w` is incomparable to `q`'s incomparables). |
| Cor 1.2 / Verdict 2: "**exactly** three exact paddings"; "inside `𝒦_min` the witness can only appear **reweighted**" | **OVERSTATED** (completeness false) | §3: a non-module embedding with the exact law in a prime host. The true statement is: *a module padding* never yields `𝒦_min`. |
| Lemma 1.3(1) `ext(τ) = C(m+k,k) − C(p_τ−1+k,k)`, and the spread `≤ (m+k)/k` | **HOLDS** | Re-derived (the violating shuffles put the whole chain before position `p_τ`), and checked exactly for all 6 `τ` of the single hub (`out_audit.txt` §C). |
| Lemma 1.3(2) "`G(H_k)` is connected since `c_1` is incomparable to all of `W`" | **BROKEN at the edge case `U = W`** (harmless) | If `U = W`, then `c_k` is comparable to everything and isolated in `G`. Instrument: `hub(2+2, U=W)` has disconnected `G`. Every use in the doc has `U ≠ W`. Repair: require `U ⊊ W`. |
| Lemma 1.3(3),(4) (ranges; `{c_1..c_{k−1}}` a chain module) | **HOLDS** | Read off the construction. |

## 2. Section 2: Fibonacci insulation and bottom insulation

**Lemma 2.0 — HOLDS.** Displacements are at most 1, so the extensions are products of disjoint adjacent
transpositions. Hence `e(F_N) = F_{N+1}`, and a domino at `{i,i+1}` leaves `F_i·F_{N−i}`. The Binet limit is
`1/(√5φ) = (5−√5)/10`, which I checked.

**Thm 2.1 — HOLDS.**
- (1) Re-derived: `π(z) = R`, the other elements have `π ≤ 3`, `G` is the path plus `z−x_1`, and `z < x_N`.
- (2) Re-derived: `z` has `w(T) = R+1−1_A(T)` slots, and the formula rearranges exactly. `P(A∩B)` is
  `F_R·F_a·F_{N−i}/F_{N+1}`, since the gap between the dominoes has length `a−1`.
- (3) Re-derived: the powers of φ cancel because `a+N+1 = (N−R)+i`, every Binet exponent is `≥ a`,
  and `P(A)P(B) ≤ 1`, `R+1−P(A) ≥ R`.
- Instrument: the closed form equals the exact count at **every** admissible `i`, not only the centre.
  That is 56 pairs over `(N,R) ∈ {(12,4),(14,5),(20,8),(26,8),(30,11)}`. Bound (3) holds on each.
  **Control:** replacing `P(A∩B)` by `P(A)P(B)` is rejected (FIRES).

**Primality of `attach_low(F_N,R)` — upgraded EMPIRICAL → PROVEN (this audit), for `R ≥ 4`,
`N ≥ R+2`.**

*Proof.*
1. `F_N` is prime for `N ≥ 4`: its incomparability graph is the path `P_N`, and a path on `≥ 4`
   vertices has no nontrivial module.
2. Let `M` be a proper module of `P = F_N ∪ {z}` with `|M| ≥ 2`. Then `M ∩ F_N` is a module of `F_N`.
3. **Case `z ∉ M`.** Then `M = F_N`. But `z ∥ x_1` and `z < x_N`, so `z` does not relate uniformly to
   `F_N`. Contradiction.
4. **Case `z ∈ M`.** Then `M ∩ F_N` is a single element `x_j`, since `M = P` is excluded.
   - If `j ≤ R`: every `x_l` with `l ≤ R`, `l ≠ j`, must be incomparable to `x_j` (as `z ∥ x_l`). So
     `|l−j| ≤ 1` for all `l ≤ R`, which is impossible for `R ≥ 4`.
   - If `j ≥ R+1`: `x_1 ∥ z` forces `x_1 ∥ x_j`, i.e. `j ≤ 2`, which contradicts `j ≥ R+1`. □
5. **R = 3 is sharp.** The module is `{x_2, z}`, which is the author's control.

Instrument: the checker agrees at every even `N ∈ [6,40]` and every `R ≤ min(N−2, 14)`. So
**the A5 exhibit lies in the (M1)+(M2)-shape for every `R ∈ [8, L*]`** (the window membership is
CONDITIONAL).

**Lemma 2.2 (cited) and Thm 2.3 — HOLD.**
- (i) Re-derived: `e(x) > k+D ⟹ d(x) ≥ k`, and dually.
- (ii) The prefix identity with `ρ_J = P_{P[J]}[a<b]`.
- (iii) KSBFT-I Lemma 6 was re-derived and HOLDS in `docs/AUDIT-mg-e8b4.md` row 10.
- Thm 2.3's index bookkeeping checks out:
  - `k₀ = max e + D` puts `a, b` in every `J ∈ V_{k₀}`;
  - `k = k₀ + 2Dj ≤ K−D−1` puts every size-`k` ideal inside `A`;
  - so `V_k(P) = V_k(P[A])`, and the `ρ_J` are the same.
- The bound is **symmetric** in `P` and `P[A]`. That matters for Cor 5.4 (§5).

## 3. Section 3: the forced structure, and the exactness dichotomy

**Prop 3.1 — HOLDS** (re-derived).
- A proper non-chain module is a smaller non-chain, so by minimality it has a balanced pair. That
  pair keeps its probability in `P` by Lemma 1.1.
- `A ⊕ B`: both summands are modules, hence chains, so `P` is a chain.
- `A + B`: `P` has width 2, and Linial's theorem applies.
- This is the one place the minimal-counterexample structure is used, and it **is** forced.

| (M·) | verdict |
|---|---|
| M1 (both connected, only chain modules) | **HOLDS** |
| M2 (`8 ≤ π ≤ L*`) | **CONDITIONAL** on [D≤7] and [H] |
| M3 | HOLDS (definition) |
| M4 (O1/O2 at both ends) | cited, KSBFT-Q Thm 3.1, audited HOLDS in mg-3345. Not re-derived here |
| M5 | cited; not re-derived |
| M6 (Cor 5.3) | **HOLDS**, but vacuous for `n < h(D,μ)` (§5) |
| M7 | CONJECTURED, not audited |

**The exactness dichotomy — OVERSTATED.**
- Take `P = {z1<u, z2<v, z1<w, z2<w}`. It is prime and both-connected (instrument §E).
- `W = {u,v}` is **not** a module (`z1 < u`, `z1 ∥ v`).
- Yet `P[u<v] = 1/2` **exactly**, by the automorphism `(z1 z2)(u v)`.
- So an exact law does not require a module, and "exactly three exact paddings" is false as a
  completeness statement.
- What is true, and all the doc uses, is this: a *module* padding of a non-chain witness is never
  `𝒦_min`-shaped.
- For the `2+2` witness (6 extensions), a uniform-law non-module embedding into a prime host was
  **not found**. That is EMPIRICAL: 4000 random hosts, `n ≤ 8`.
  - **Control:** the same detector FIRES on the module embedding `2+2+C_2`.
  - The symmetry trick cannot work there, because `Aut(2+2)` has order 2 and cannot act
    transitively on 6 extensions.

## 4. Section 4: the per-route padded witnesses

Every host was rebuilt from the doc's text.

| row | claim | verdict | recomputed |
|---|---|---|---|
| A5 | Fibonacci centre pair → `C_BFT` inside a range-exactly-`R`, both-connected poset | **HOLDS**. Prime now PROVEN (§2). "Dead" as a route is the doc's reading of mg-a1ec's relaxation, which I did not re-read | exact at all `i`; the top end has only 2 maximal elements, so O1 fails there. `attach_both` would repair that |
| A14 | `attach_both(F_20,8)`: prime, range 8, δ ≈ 0.456, max probe-B certificate 13627/46282 < 1/3 | **HOLDS** (exact reproduction, incomparable pairs × all slots) | also: ≥ 3 min / ≥ 3 max (O1 both ends); `F_26`: 29341/99654 = 0.2944 (stable, insulation); `attach_both(F_20,10)` (range 11): 0.311 < 1/3; one-sided `attach_low(F_16,8)` certifies 887/2322 = 0.382 at the free top. **Control:** certifies on bare `F_12` (89/233) |
| A16 | double hub `k = 8`: range 18, only chain modules, both connected, separating number 2, `P[b₂<a₁]` = 5336/27441 | **HOLDS** (exact); `k = 16` gives 9236/50429 | O1 at both ends (4 min, 3 max). "Co-degree" reading: **UNVERIFIABLE** (the source never defines it). The standard graph co-degree (common neighbours in `G`) is **0** for `(a₁,b₂)` in `2+2`, which contradicts the source's "1/6 at co-degree m=2 via `C_p ⊔ C_q`". The author's symmetric-difference reading gives 2, which fits. So the author's reading is the consistent one |
| A13, A15, B1–B5, C1, C5, f5be, E3/5987, E4 | structural exclusions | **UNVERIFIABLE here**: not re-audited. A15's logic (a counterexample has `s ≥ 3` by the probe's own theorem, where the bound is `< 1/3`) HOLDS as stated | — |
| E3/9b6b | "[H] makes the lever finite" | not re-derived | — |
| A28 | (L*) refuters at `n = 9, 9, 11` have ranges 8, 8, 9 and connected `G` | **HOLDS** on the bitmasks as quoted in `ksbft_p1_walled_0b78/ranges2.py`. Provenance to mg-5cba/789d not traced. They have non-chain modules, so they are in `𝒲`, not `𝒦_min`, which is what the doc says | §F |
| A8 | `e(P_m + C_8) = C(|P_m|+8,8)·e(P_m)` | **HOLDS** (trivial) | — |

**The global "dead" verdicts are OVERSTATED** (see §0). Each exhibit refutes the route's lemma on the
(M1)+(M2)(+O1) shape. None of them is a counterexample-shaped host, which is (M3). The doc's §4 preamble
states the right criterion, but the summary drops it.

**§4.2 (Step 6).**

- **`W*_t = C_{a−2} ⊕ ({x} + C_{t+1}) ⊕ C_{b−t}` — HOLDS.**
  - Re-derived from mg-b447's text: `c_{a−2}` is below all, and `b_{t+1}` is above all.
  - Recomputed at `(t,a,b) = (2,4,4), (3,4,8), (7,9,9)`, with `p_xy = 1/(t+2)`.
- **"mg-b447 Thm 4.1 is a statement about the continuity form" — BROKEN.**
  - mg-b447 §1 states (T) existentially.
  - Instrument §D: the sides of `W*_t` have exactly one incomparable pair, `{x,y}`. So `W*` refutes
    the **existential** form, on decomposable posets.
- **Insulated `W*` — HOLDS**, reproduced exactly:
  - (8,2,8): range 5, `Δ₁` 0.0618, `p_xy` 0.2526;
  - (16,6,16): range 9, `Δ₁` 0.0443, `p_xy` 5702887/39150182;
  - in both, the surviving balanced pairs are `(f₁,f₂)` and `(f_M, y)`.
  - Minor: the table's `f_0` is 0-indexed; the text is 1-indexed.
  - **(T∃) holds on these instances — HOLDS** (exact).
  - Attributing the survival to Thm 2.3 is **OVERSTATED**. Thm 2.3's guarantee needs depth
    `h(D,μ) ≈ 1.8·10⁹` at `D = 5`, `μ = 0.05`, and `M = 8, 16` are nowhere near it. The survival is an
    exact computation, not insulation.
- **(T_cont) refuted on prime window posets — OVERSTATED as written, supported by the family
  (EMPIRICAL).** See §0 for the family and the swapped labels.

## 5. Section 5: the deep dive

**Prop 5.1 — HOLDS** (re-derived; CONDITIONAL on [H]+[D≤7] for membership in `𝒦_min ∩ 𝒲`).
- The `Δ₁`-hypothesis is indeed not needed: minimality supplies the side's balanced pair.

**Weaknesses of the candidate (T∃^any)** — PROVEN (control) and EMPIRICAL (probe):

1. **Ideal-only is the wrong shape.**
   - Suppose a poset's only balanced pair is two maximal elements. No proper ideal contains both,
     so (T∃^any) fails even though the conjecture holds.
   - The V poset (two elements over one) is such a case. The instrument's **positive control
     FIRES** on it.
   - A `𝒦_min`-shaped instance would need all balanced pairs among the maximal elements.
   - No failure was found on prime, both-connected hosts, for either the ideal-only or the
     ideal-or-filter form (158 random hosts with `n ≤ 8`; EMPIRICAL, far below the window).
   - Recommendation: state (T∃^any) with "ideal **or filter**", as mg-b447 did.
2. **Strength.** (T∃^any) on `𝒦_min ∩ 𝒲` implies the conjecture there, and I see no converse. So
   it may be *stronger* than what is needed. "Best candidate" is CONJECTURED.

**Thm 5.2 — HOLDS** (it is Thm 2.3 with `θ_D^j ≤ μ`).

**Cor 5.3 — HOLDS**, with the vacuity for `n < h(D,μ)` noted in §0.

**Cor 5.4 — OVERSTATED (minor repair).**
- Let `v₁` (maximal) and `v₂` (minimal) both fail. Then some extension has
  `max(e₁(a),e₁(b)) ≥ n−h`, and some has `min(e₂(a),e₂(b)) ≤ h+1`.
- The cross-extension window gives `e₁(b) − e₂(a) ≤ π(a)+π(b)−1 ≤ 2D−1`. (This is KSBFT-F Lemma 2.0's
  proof, which bounds positions via `d(·)` and so works across different extensions.)
- So both fail only when `n ≤ 2h+2D`. The claim needs `n ≥ 2h+2D+1`.
- The proof "applies Thm 5.2", but Thm 5.2 transfers `P[A] → P`, and Cor 5.4 needs `P → P−v`. Thm
  2.3's bound is symmetric, so the repair is immediate.
- Cor 5.4 presupposes a robust balanced pair in `P`. So it does nothing for the conjecture, and on
  a counterexample it is vacuous.

**§5.4, the obstruction — HOLDS as a description.** Its item 3 correctly says the missing lemma is the
conjecture on `𝒦_min ∩ 𝒲`, rephrased.

## 6. What I did NOT do, and what was ruled out

- **Not re-audited:**
  - the structural-exclusion rows (A13, B1–B5, C1, C5, f5be, E3, E4). The doc got these from a
    sub-agent;
  - A24;
  - (M7);
  - E3/9b6b's finiteness;
  - the route readings of A5 (mg-a1ec) and probe B/D beyond `attempt-index.md:30–33`, which I read:
    probe D's "co-degree" really is undefined there;
  - anything about `L*`, AK25a/b or Haq26;
  - KSBFT-Q Thm 3.1, beyond citing its audit.
- **Primality** of insulated `W*` was checked at `n ≤ 34` only (`M = 8, 16`). The `M = 20, 24, 30`
  rows are not primality-checked.
- **No census or search was extended.** Two small random samples were used as instruments, each
  with a control that fires:
  - uniform-law `2+2` embeddings;
  - (T∃^any) failures.
  All other computation is on named posets.
- **Candidates ruled out:**
  - "`W*` refutes (T) only in continuity form" (BROKEN, §4);
  - "exact padding requires a module" (§3);
  - "`attach_low` primality needs `N ≤ 30`" (now proven for all `N`);
  - the ideal-only form of (T∃^any) as the right statement (§5).
- **Controls** (all FIRE, asserted by `run_all.sh`):
  - the wrong closed form is rejected;
  - probe B certifies on `F_12`;
  - the uniform-law detector fires on a module embedding;
  - the module detector finds the single hub's module;
  - the (T∃) detector fails on V.

**Recommended errata to KSBFT-R:**
1. Recommendation 2's first sentence: "Thm 4.1 refutes the existential (T) on decomposable posets;
   the refutation does not reach `𝒦_min`."
2. "Dead" becomes "dead as a class lemma on (M1)+(M2)".
3. Drop "exactly" from "three exact paddings".
4. Cor 5.4: `n ≥ 2h+2D+1`, and use Thm 2.3.
5. Lemma 1.3: `U ⊊ W`.
6. (T∃^any): ideal or filter.
7. Primality of `attach_low` is PROVEN.
8. "audit mg-9268 pending" → HOLDS (`AUDIT-mg-e8b4.md`).
