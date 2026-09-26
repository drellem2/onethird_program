# AUDIT of mg-b447 (KSBFT-F) — every PROVEN claim re-derived, witness ranges recomputed

`mg-de37`, 2026-09-26. The subject is `docs/KSBFT-F-L4-step6-under-bounded-range.md` (commit
`ea18bc8`), together with `code/ksbft_f_b447/`. I am not its author. I read the doc and its
transcript. I did **not** read `check.py` before writing my own instrument.

- Instrument: `code/audit_ksbft_de37/indep_de37.py` (exhaustive at `n ≤ 6`, witnesses at any size)
  and `tau_search_de37.py` (exhaustive at `n = 7`).
- Runner: `sh code/audit_ksbft_de37/run_all.sh`. It takes about 12 s, uses exact `Fraction`s, and
  has no clock and no randomness.
- Transcripts: `out_indep_de37.txt` and `out_tau_search_de37.txt`.
- My poset enumerator is independent of the author's. It reproduces A006455 (`1, 2, 7, 40, 357, 4824,
  96428` at `n = 1..7`), which is its positive control.

Verdicts: **HOLDS** / **BROKEN** / **OVERSTATED** / **UNVERIFIABLE** (checkable only against a
source I could not read).

---

## 0. Summary

> **The flashiest claim holds.** L4 restricted to `Π_D` is a theorem, with a linear modulus and
> discharged through branch (ii) alone (Thm 3.1). Every step re-derives. It holds under both
> readings of `ε` and both readings of "modify".
>
> **One claim is BROKEN, and it cuts in the author's favour.** Negative #6 says a sharper interface
> bound than `2D−1` is "refuted as a universal: `τ/(2D−1) = 1` is attained at `n ≤ 6`". But
> **`τ ≤ D` always holds (PROVEN below, §2).** The ratio 1 is attained only at `D = 1`, where
> `2D−1 = D`.
>
> - At `n ≤ 7` the maximum of `τ` for each `D` is `1, 2, 3, 3, 3, 3` against `2D−1 = 1, 3, 5, 7, 9, 11`.
>   There are **0** cuts with `τ > D` among 578 562 (EMPIRICAL).
> - A staircase family attains `τ = D` for every `D`, so `D` is sharp.
> - Consequences: the moduli improve. `F_D` in Thm 3.1 can take `D` in place of `2D−1`, and so can
>   `N(D,ε)` in Prop 4.2. **No verdict of the doc changes.**
>
> **Two OVERSTATED:**
>
> 1. Prop 4.2's "⟺" is literally false as stated. The ⟸ direction needs the conjecture at
>    `n < N`, which the doc's own parenthesis concedes. Its proof also uses reading (E1), although
>    §1 claims "everything below holds under both".
> 2. "Every obstruction on record has range `≤ 3`" sits beside the doc's own table row
>    `C_a ⊕ C_a minus t crosses: range t`, a family with arbitrary `t` in mg-63e3 row 22.
>
> Prop 7.1's strict `<` fails at `π(x) = 0`. That is a nit.
>
> **Every witness range recomputes exactly:**
>
> - `W*_t`: range `t+1`, `p_xy = 1/(t+2)`, `EK = t/(t+2)`, `τ = 1`, for all 9 parameter triples I
>   ran, including `t = 9, 12` beyond the author's.
> - `W = W*(a,a,2)`: range 3.
> - `2+2`, the `n = 4` N-poset, the mg-f5be fence (closure `Z_8`) and `Z_3..Z_14`: range 2 each.
> - The `W*(4,4,2)`, `v = b₁` one-point refutation re-computes pair for pair.
>
> **Every negative-control count the author printed reproduces:** 47, 37 588, 137 and 5 224. I add
> the firing control §S lacked: the "for every `v`" variant fails on 113 posets, while "exists `v`"
> fails on 0.

---

## 1. Claim-by-claim table

| # | claim (doc §) | doc's mark | verdict | note |
|---|---|---|---|---|
| 1 | Fact 2.1: no `b < a` across a prefix cut | cited | **HOLDS** | `e(b) > e(a)` |
| 2 | Lemma 2.0: `a ∥ b` ⟹ `\|g(a)−g(b)\| ≤ π(a)+π(b)−1` in every LE | PROVEN | **HOLDS** | re-derived; 0 violations of `≤ 2D−1` over every LE at `n ≤ 6` |
| 3 | mg-3af9 Thm A (∗): `X_σ × Y_σ` pairwise incomparable | re-checked | **HOLDS** | `y < x` is excluded by Fact 2.1. `x < y` is excluded because `y` is in `σ`'s first `k` and `x` is not |
| 4 | Lemma 2.1: `K(σ) ≤ D`, `Δ₁ ≤ D/min(k,n−k)` | PROVEN | **HOLDS** | re-derived; control `K ≤ D−1` FIRES 47 |
| 5 | Prop 2.2(a): min modification certificate `= τ`, removal `≤ τ` | PROVEN | **HOLDS** | ⊇: `P ∪ (A×B)` is `P[A]⊕P[B]` by Fact 2.1 |
| 6 | Prop 2.2(b): `τ ≤ \|I_A\| ≤ 2D−1` | PROVEN | **HOLDS, not sharp** | **`τ ≤ D`** (§2) |
| 7 | Lemma 2.3: `P[b before a] ≥ c(D) = 1/(1+f(D)) ≥ 2^{1−2D}` | PROVEN | **HOLDS** | re-derived (§3); `f(1..6) = 1, 6, 25, 98, 381, 1485` recomputed; `c(D) ≥ 2^{1−2D}` for `D ≤ 30` |
| 7a | aside: `c(D)` beats KSBFT's `q₂` | not consumed | **HOLDS** | `(D+1)^{2D+2} ≥ 2^{2D+2} > 2^{2D−1}` |
| 8 | Thm 3.1: L4 on `Π_D` via branch (ii), `F_D(ε) = (2D−1)ε/(2c(D))` | PROVEN | **HOLDS** | under (E1) and (E2): `F_D` is linear, so `F_D(Δ₁)n ≥ 2D−1` directly; 0 violations in the check at `ε = Δ₁` |
| 9 | "L4 on `Π_D` is empty" / "pushes every instance into (ii)" | PROVEN (cond.) as logic | **HOLDS, wording** | (ii) is always *available*, so the disjunction carries no information. It does not say (i)/(iii) *fail*; "pushes" is loose |
| 10 | Thm 4.1: `(T)` false on `{r ≤ π ≤ D}`, every `3 ≤ r ≤ D`, every modulus | PROVEN | **HOLDS** | `W*_t` recomputed (§4) |
| 11 | "`[7, L*]` is the window": counterexample has `π ≥ 7` | cited (BW92, Pec08) | **UNVERIFIABLE here** | literature, not re-verified by author or auditor |
| 12 | Prop 4.2: (IB)`\|Π_D` ⟺ conj. on `Π_D`, `n ≥ N(D,ε)` | PROVEN | **OVERSTATED** | ⟹ holds (E1). ⟸ for `n < N` needs the conjecture at small `n`. Under (E2), `G(Δ₁)n ≥ τ` is not automatic (§5) |
| 13 | §4.3 "for every `v`" one-point transport false at `W*(4,4,2)`, `v = b₁` | PROVEN by hand | **HOLDS** | `P−b₁`: `1/3, 2/3`; `P`: `1/4, 3/4`; `(x,b₁)` at `1/2` is not in `P−b₁` |
| 14 | §4.3 "exists `v`": 0 failures on 5 224 non-chains, `n ≤ 6` | EMPIRICAL | **HOLDS as EMPIRICAL** | reproduced; the control I add FIRES 113; the `v`-list in `W*` recomputes |
| 15 | Prop 5.1: middle cut `β ≥ (n−1)/(2n)`, `Δ₁ ≤ 2D/(n−1)`, leak ratio `≤ 4nD/(n²−1)` | PROVEN | **HOLDS** | `⌊n/2⌋⌈n/2⌉ ≥ (n²−1)/4` |
| 15a | "`1 − λ_std ≤ 4nD/(n²−1)` by row 5" | PROVEN (cond.) | **UNVERIFIABLE** | row-5 normalisation not read (author says so too) |
| 16 | L3 / L2 / 3b refuters at `n ≤ 7` have range `≤ 6` | by size | **HOLDS** | `π(x) ≤ n−1` |
| 17 | L2 second disjunct's product automatic; 3b off-route | PROVEN (cond.) | **HOLDS as logic** | rests on the audited KSBFT-C / mg-05ec, which I did not re-audit |
| 18 | U-id: `h(x)−e(x) = Σ_{later} P[y≺x] − Σ_{earlier} P[x≺y]` | PROVEN | **HOLDS** | re-derived; 0 violations |
| 19 | Prop 7.1: frozen ⟹ `\|h−e\| < max(λ,ε)/3 ≤ π(x)/3` | PROVEN | **HOLDS (nit)** | strict `<` fails at `π(x) = 0` (`0 < 0`); true as `≤`, strict for `π(x) ≥ 1`. The majority order exists (§6) |
| 20 | "useless at `C < 0.30`" | — | **HOLDS** | the *bound* is `< 0.30` only at `max(λ,ε)=0`; the doc says undecided whether (EQ) itself is |
| 21 | `Π_D` closed under induced subposets; (MC_{L*}) finishes the conjecture under H | PROVEN (cond.) | **HOLDS** | minimal counterexample argument re-run (§7) |
| 22 | "for `n ≥ 50L*` there is no smaller statement coming from this architecture" | inside a PROVEN (cond.) paragraph | **OVERSTATED as proof** | true of the links the doc enumerates; a meta-claim, not a theorem |
| 23 | §0/§3.1 "every obstruction on record has range `≤ 3`" | EMPIRICAL + hand | **OVERSTATED** | the doc's own table lists `C_a⊕C_a − t crosses`, range `t`, arbitrary `t` (mg-63e3 row 22) |
| 24 | §9 negative #6: sharper-than-`2D−1` interface bound "refuted as a universal" | negative | **BROKEN** | `τ ≤ D` is PROVEN; attainment of `2D−1` is only at `D = 1` (§2) |
| 25 | negatives #1–#5 | negatives | **HOLD** (#1, #3 re-derived) / inherited (#2, #4, #5) | see §8 |
| 26 | L4, `(T)`, Step 6, Fact 2.1 as quoted from mg-63e3/mg-3af9 | not verified at source | **UNVERIFIABLE** | I also could not read the `.tex` |

**EMPIRICAL-as-proof check.** The doc labels X1–X5, §S and §T as checks and not proofs, and §S is
explicitly EMPIRICAL. The one place where an observation carries a universal conclusion is negative
#6. It uses the observed `max τ/(2D−1) = 1` to refute any sharper bound. That is item 24, and it
fails because the observation is at `D = 1` only.

---

## 2. `τ ≤ D` — PROVEN, sharp (this breaks negative #6)

**Claim.** Let `(A,B)` be a prefix cut of a linear extension of `P`. Then the vertex-cover number `τ`
of the cross-incomparability graph `G_cut` satisfies `τ ≤ π(P)`.

**Up-closure.** If `a ∥ b` (`a ∈ A`, `b ∈ B`) and `a < a'` with `a' ∈ A`, then `a' ∥ b`:

- `a' < b` would give `a < b`;
- `b < a'` is impossible by Fact 2.1.

**Proof.**

1. By König, `τ` equals the size `m` of a maximum matching `{(a_i, b_i)}` in `G_cut`.
2. Let `a₁` be `P`-maximal among `{a_1..a_m}`.
3. For each `i ≠ 1`, `a_i > a₁` is excluded by maximality, which leaves two cases:
   - `a_i ∥ a₁`, and `a_i` is an incomparable of `a₁`;
   - `a_i < a₁`, and then `a₁ ∥ b_i` by up-closure.
4. Either way, each `i ≠ 1` contributes one incomparable of `a₁`. These are distinct across `i`,
   since the matching's vertices are distinct, and all differ from `b₁`, which is itself
   incomparable to `a₁`.
5. So `π(a₁) ≥ m`, and `τ = m ≤ π(a₁) ≤ π(P)`. □

**Sharpness.** The staircase `S_m`:

- two chains `u₁<…<u_m` and `v₁<…<v_m`, with `u_i < v_j ⟺ j > i` and no `v` below any `u`;
- `A = {u}` is a prefix, and `u_i ∥ v_i` is a matching of size `m`;
- `π(u_m) = π(v_1) = m = π(S_m)`, so `τ = D = m`.

The transcript checks `m = 1..6`, and prints `2D−1 = 1, 3, 5, 7, 9, 11` beside `τ = 1..6`.

**EMPIRICAL corroboration.** The maximum of `τ` for each `D` is:

| `n` | `D = 1` | `D = 2` | `D = 3` | `D = 4` | `D = 5` | `D = 6` |
|---|---|---|---|---|---|---|
| `≤ 6` | 1 | 2 | 3 | 3 | 3 | — |
| `7` | 1 | 2 | 3 | 3 | 3 | 3 |

There are **0** cuts with `τ > D` among 578 562 cuts at `n = 7`. The control "`τ ≤ D−1`" FIRES 137
times at `n ≤ 6`, which matches the author's count.

**Consequences, none of them changing a verdict:**

- Prop 2.2(b)'s bound on `τ` improves to `D`. `|I_A| ≤ 2D−1` is still true; I did not check whether
  it is sharp.
- Thm 3.1 holds with `F_D(ε) = D·ε/(2c(D))`, by the same proof.
- Prop 4.2's `N(D,ε)` can use `D/G(ε)` in place of `(2D−1)/G(ε)`.
- Negative #6 is BROKEN as stated. The universal "`τ ≤ D`" is the sharper bound it said was refuted.

---

## 3. Lemma 2.3 re-derived

The setup: take `σ` with `a` before `b`. Let `Z = {z : σ(a) < σ(z) ≤ σ(b), z ≤ b}`, let `R` be the
rest of the gap, and move the block `Z` to just before `a`.

**The moved order `σ'` is a linear extension:**

- `Z ⊆ inc(a)`. `z` after `a` excludes `z < a`, and `a < z ≤ b` would give `a < b`.
- No `r ∈ R` lies below any `z ∈ Z`, since that would put `r ≤ b`, so `r ∈ Z`.

**The map `σ ↦ σ'` has bounded fibres:**

- `σ` is recovered from `σ'` by `(j, r)` and an interleaving of `Z∖{b}` with `R`, with `b` last in
  the gap.
- `j ≤ π(a) ≤ D`, and `j − 1 + r = σ(b) − σ(a) − 1 ≤ 2D − 2` by Lemma 2.0.
- So the fibre size is at most `f(D)`, and `P[a≺b] ≤ f(D)·P[b≺a]`.

**The bound `f(D) < 2^{2D−1}`:**

- Group by `m = j−1+r`. Each group contributes `Σ_j C(m, j−1) ≤ 2^m`.
- Summing gives `f ≤ 2^{2D−1} − 1`. Hence `1 + f ≤ 2^{2D−1}` and `c ≥ 2^{1−2D}`.

The recomputed `f(D)` agree with the author's `c(D)` denominators. There are 0 violations over
86 340 ordered pairs at `n ≤ 6`, and the control "`≥ 1/2`" FIRES 37 588, the author's figure. **HOLDS.**

---

## 4. Witness ranges, recomputed independently

I built each witness from its verbal definition in the doc or in the source doc, not from
`check.py`. `W*_t(a,b)` is `C_{a−2} < {x,y} < C_b`, with `x < b_1..b_t` removed. Its
transitivity was asserted in code.

| `(a,b,t)` | range | `π(x)` | others `≤ 1` | `p_xy` | `EK` | `Δ₁` | `τ` | sides' incomparable pairs |
|---|---|---|---|---|---|---|---|---|
| (3,3,2) | 3 | 3 | yes | 1/4 | 1/2 | 1/6 | 1 | A: `{x,y}`; B: none |
| (4,4,2) | 3 | 3 | yes | 1/4 | 1/2 | 1/8 | 1 | same |
| (4,28,2) | 3 | 3 | yes | 1/4 | 1/2 | 1/8 | 1 | same (`Δ₁` independent of `b` ✔) |
| (5,9,2) | 3 | 3 | yes | 1/4 | 1/2 | 1/10 | 1 | same |
| (4,8,3) | 4 | 4 | yes | 1/5 | 3/5 | 3/20 | 1 | same |
| (4,9,6) | 7 | 7 | yes | 1/8 | 3/4 | 3/16 | 1 | same |
| (4,10,7) | 8 | 8 | yes | 1/9 | 7/9 | 7/36 | 1 | same |
| (4,12,9) | 10 | 10 | yes | 1/11 | 9/11 | 9/44 | 1 | same (beyond the author's range) |
| (6,20,12) | 13 | 13 | yes | 1/14 | 6/7 | 1/7 | 1 | same (beyond the author's range) |

**Hand derivation.** The rest of the poset is a single chain, so `x` has exactly `t+2` slots
(`c_{a−2} < x < b_{t+1}`). So `p_xy = 1/(t+2)`. `K = 1` exactly when `x` falls after `b_1`, which is
`t` slots, so `EK = t/(t+2)` and `Δ₁ = t/((t+2)·min(a,b))`.

**Theorem 4.1's argument.**

- Fix `a` and `ε = Δ₁ > 0`. The cut is within 1 modification of `P[A]⊕P[B]`.
- `1 ≤ F(ε)(a+b)` once `b ≥ 1/F(ε)`.
- The sides' only incomparable pair `{x,y}` is at `1/(t+2) ≤ 1/4 < 1/3` in `P`.
- So `(T)` fails at range `r = t+1`, for every `r ≥ 3`. **HOLDS.**

**Other witnesses:**

- `W` of mg-63e3 is `W*(a,a,2)` (`docs/OneThird-L4-Branch-ii-Consumability.md:407–409`), range 3.
- `2+2` and `{0<2, 0<3, 1<3}` have range 2 each.
- mg-f5be's `n = 8` argmax (`docs/OneThird-Primitivity-Objection-mg-f5be.md:331`) is
  `i < j` for `j−i ∈ {2,3}`. Its transitive closure is `j−i ≥ 2`, which is `Z_8`, and `|L| = 34` is
  the Fibonacci number.
- `Z_3..Z_14` all have range 2. **HOLDS.**

**`W*(4,4,2)` one-point table** (§4.3). `P` has `x∥y : 1/4`, `x∥b₁ : 1/2`, `x∥b₂ : 3/4`.

| deleted `v` | pairs balanced in `P−v` | of those, balanced in `P` |
|---|---|---|
| `b₁` | `(x,y)`, `(x,b₂)` | **none** |
| `y`, `b₂` | two pairs each | `(x,b₁)` |
| `c₁`, `c₂`, `b₃`, `b₄` | `(x,b₁)` | `(x,b₁)` |
| `x` | none (chain) | — |

This matches the doc's list `{c₁, c₂, y, b₂, b₃, b₄}` exactly. **HOLDS.**

---

## 5. Prop 4.2 — why OVERSTATED

Write `R_N` for "every non-chain `P ∈ Π_D` with `n ≥ N` has a balanced pair".

**The ⟹ direction.** (IB)`|Π_D` gives `R_N`.

- Take the middle cut. `Δ₁ ≤ D/⌊n/2⌋ ≤ 2D/(n−1) ≤ ε` for `n ≥ 2D/ε + 1`.
- `τ ≤ 2D−1 ≤ G(ε)n`. (`D` suffices, by §2.)
- **HOLDS under (E1),** where any `ε ≥ Δ₁` may be used with `G(ε)`.
- **Under (E2),** where `ε = Δ₁`, the hypothesis is `τ ≤ G(Δ₁)n`. Here `Δ₁` can be as small as
  about `2c(D)/n`, so for a `G` with `G(ε) → 0` (a linear `G`, say) `G(Δ₁)n` is bounded. It can fall
  below `τ`, and then the proof does not go through. §1's "everything below holds under both" is
  therefore not established for Prop 4.2. (IB) as quoted in the doc reads "`Δ₁ ≤ ε`", which is
  (E1), so the proposition is correct for the quoted form.

**The ⟸ direction.** `R_N` ⟹ (IB)`|Π_D` fails as stated.

- (IB) on `Π_D` includes the instances with `n < N`, and `R_N` says nothing about them.
- The doc's parenthesis concedes that these need the conjecture on `Π_D` at small `n`.
- The correct statement is "(IB)`|Π_D, n≥N` ⟺ `R_N`", or equivalently
  "(IB)`|Π_D` ⟹ `R_N`, and conj`|Π_D` ⟹ (IB)`|Π_D`".

The doc's *use* of the proposition ("(IB) is the conjecture on the counterexample class, not a
reduction") survives in the corrected form.

---

## 6. Prop 7.1 — the majority order exists; strictness nit

The doc assumes that a frozen `P` has a "majority order `e`". This is true, and I prove it here.

1. Suppose `P[x≺y] > 2/3` and `P[y≺z] > 2/3`. Then `P[x≺z] > 1 − 1/3 − 1/3 = 1/3`.
2. Frozen means `P[x≺z] ∉ [1/3, 2/3]`, so `P[x≺z] > 2/3`.
3. The mixed cases (one pair comparable) are immediate.
4. So the majority relation is a linear order that extends `P`.

Every probability in the U-id is then a flip against `e`, and each is `< 1/3`.

- If `λ ≥ 1` the first sum lies in `[0, λ/3)`, and if `λ = 0` it is `0`. The same holds for the
  second sum with `ε`.
- So `|h−e| < max(λ,ε)/3` when `π(x) ≥ 1`.
- At `π(x) = 0` both sides are `0`, and the strict inequality is false. **HOLDS with `≤`.**

---

## 7. (MC_D) and the net

**Closure.** Induced subposets preserve incomparability, so `Π_D` is closed under induced
subposets.

**Minimal counterexample.** Take a minimum-size counterexample `P`.

- `P` is itself a counterexample, so under H it lies in `Π_{L*}`.
- Each non-chain `P−v` is smaller, so `δ(P−v) ≥ 1/3`.
- (MC_{L*}) then gives `δ(P) ≥ 1/3`, a contradiction.

**HOLDS (cond. on H).**

**ONE-PT_D ⟹ MC_D** is trivial, since its conclusion includes "balanced in `P`". **HOLDS.**

"No smaller statement from this architecture" is true relative to the links tabulated in §8 of the
doc, but it is a claim about a list and not a theorem (item 22).

---

## 8. Negatives (the doc's §9), checked against the candidate space

| # | candidate | verdict |
|---|---|---|
| 1 | range window excluding `W*` | **HOLDS.** `W*_t` covers `[r,D]` for every `r ≥ 3` (recomputed to `t = 12`). |
| 2 | balanced cuts / F-bal | **Inherited.** It rests on mg-f825 F4 and mg-3af9 §5.4, which were not re-audited. The Prop 5.1 part holds. |
| 3 | one-point transport for every `v` | **HOLDS** (§4). |
| 4 | approximate locality | **HOLDS as a remark on method.** `1/3 − η` is not `≥ 1/3`. Decay is unproven, and the doc says so. |
| 5 | frozenness added to `(T)` | **Inherited** ("renames the problem", mg-3af9 §4.1). |
| 6 | sharper interface bound | **BROKEN** (§2). |

**Candidates the doc did not try, which I checked:**

- A width- or size-based window instead of a range window. `W*_t` has width 2 and `n` arbitrary, so
  it lies in any width `≥ 2` window. Not a repair.
- A cut other than the prefix at `|A| = a`. Not examined, by the doc or by me.

---

## 9. What I did not do

- I did **not** read `spectral_near_ordinal_sum_program.tex`. I, like the author, took L4, `(T)`,
  Step 6 and (IB) from the mg-63e3 / mg-3af9 quotes (item 26).
- I did **not** verify BW92, Pec08 or Gup26 (item 11).
- I did **not** read the row-5 normalisation of `leak` (item 15a).
- I did **not** re-audit KSBFT-C, mg-05ec, mg-3af9, mg-f825 or mg-63e3. The doc's conclusions resting
  on them (L1b automatic, node B unconsumed, Cor. A2/A3, F4) are inherited, and so is this audit's
  acceptance of them.
- My exhaustive checks stop at `n = 6`, and at `n = 7` for `τ` alone. Every universal verdict above
  rests on the written proof, never on the check.
- I did **not** check whether `|I_A| ≤ 2D−1` is sharp, or whether `c(D)` improves KSBFT Thm 1.3.
- **Nothing here consumes** KSBFT Lemma 4.2, the constant `441` or eq. (1.5).
- I did not read `code/ksbft_f_b447/check.py`. The agreement between the two instruments is between
  independently written code.
