# KSBFT-T3: Lemma C for interval orders. No XYZ instance kills Q12: with every triple law and every XYZ instance imposed exactly, Q12 stays feasible at ε = 1/75. The missing input is not correlation. It is **linear but multi-element**: Swap Identities used pointwise on a probability measure over extensions, and Swap Identities *conditioned* on the order of two other elements. With them all 13 LP-feasible survivors have exact rational certificates. None of these certificates is a one-step (Lemma C) certificate. Lemma C is NOT proven, and even a proof would still need the combinatorial K_C (mg-785e)

Ticket mg-785e. It is gated on mg-6c30, the audit of mg-561a (`docs/AUDIT-mg-561a.md`).
- The audit found every PROVEN statement of `docs/KSBFT-T2-two-separator.md` HOLDS, so nothing I use is broken.
- I do not use its OVERSTATED items: "first fails at n = 12", "a one-step lemma can only live at containment steps", and §6.
- I take from the audit (§1(b)) and from pm-onethird's mail of 2026-09-26 the point that **Lemma C alone is not a proof**: it needs K_C. §5 is written around that.

**Instrument.** `code/ksbft_t3_lemma_c_785e/`.
- Everything that is claimed as a proof is checked in exact `Fraction` arithmetic by pure Python: `verify_certs.py`, `xyzlp.py`, `probe8.py`.
- A float LP (scipy/HiGHS, run from a scratch venv; scipy is not installed system-wide) is used only to **propose** multipliers and to probe. Every refutation claimed below was then re-checked exactly on every linear extension.
- Generation and laws are imported read-only from the audited `iolib.py` (mg-afa4 / mg-5ecf). Covers, typed separators and the automaton DP come read-only from `t2lib.py` (mg-561a / mg-6c30). The pair-law LP is `lpcheck.build`, imported read-only.
- Per the standing rule, computation is an instrument only: probes on Q12 and the 13 named survivors, and one population census (the X-law of containment steps, n ≤ 10, on the existing populations). **No case census was extended.**

**Labels.**
- **PROVEN**: a proof is in this file, or it is an exact certificate checked by `verify_certs.py`.
- **EMPIRICAL**: exact arithmetic on a stated finite population, or a float probe (marked *float*).
- **CONJECTURED**: a guess.

**Notation** (as in mg-561a).
- `L` is the 2/3-order of a putative counterexample.
- `A(a,a')` and `B(a,a')` are the above-separators and below-separators, and `S = A ∪ B`.
- `Λ₁(a,a')` = {`a` before `a'`, no separator between}.
- A containment step is `a ≺ a'`, `L`-consecutive, with `a ⊂ a'` strictly. Inner-first is WLOG, since the outer-first case is its order dual.
- Then `S = A(a,a') = min Z`, where `Z = {z : r(a) < l(z) ≤ r(a')}`. Lemma C concerns `|S| = 2`, `S = {s, t}`.
- Q12 = `[1,1][1,2][2,3][2,5][3,4][4,5][5,6][5,8][6,7][7,8][8,9][9,9]`, with the staircase `L`. Its containment step is `a = [3,4] ≺ a' = [2,5]`, with `s = [5,6]` and `t = [5,8]`.

---

## 0. Verdict

1. **Task 1: which XYZ instance kills Q12? None.** (EMPIRICAL, *float*, with an exact part; §2.)
   - I tied the LP's joint variable `J = P[s<a', t<a']` to an exact triple law on `{s, t, a'}`. That is a linear repair, and it already moves Q12's margin from `ε* = 1/48` to `ε* = 1/75` (exact, Fractions).
   - I then added **every** XYZ instance `P[x<y, x<z] ≥ P[x<y]P[x<z]` and its dual, over all 40 triples with `x ∥ y, z`: 240 McCormick rows, then a spatial branch-and-bound on the exact products.
   - The optimum stays **1/75**, at a point that satisfies every XYZ instance to 10⁻⁹. So XYZ is **not** the missing input.
   - At the step itself there is a structural reason (PROVEN, Prop 2.1): XYZ bounds `β = P[s<a', t<a']` from **below**, which only shrinks the union that Thm 1.1 needs to be large.
2. **What does kill Q12, and all 13 survivors: linear facts in a richer space.** (PROVEN per instance, exact certificates; EMPIRICAL as a pattern; §3.)
   - Replace the pair-law LP by a probability measure `μ` on **all** linear extensions (the *full-measure lift*), and impose Swap Identities as identities of that measure.
     - Plain Swap Identities (Thm 1.1 of mg-561a), used this way, **refute 9 of the 13 survivors**. The smallest certificate charges 2 inversions and uses 6 identities (ratio 11/4 < 3).
     - The remaining 4, which are the Q12 family, need **Conditioned Swap Identities** (Prop 1.1, PROVEN, every poset): the Swap Identity holds separately on each event fixed by the exchange of `a` and `a'`. Conditioning each `L`-step on the relative order of 2 other elements refutes all 4.
   - Every refutation is an exact rational **pointwise certificate** (Prop 1.2): an inequality `G(σ) ≥ g` checked on every one of the up to 48 620 linear extensions. `verify_certs.py` reports 14/14 VALID, and its three controls are CAUGHT.
   - So "the linear facts provably stop at Q12" (mg-561a §4) is true **only for the pair-law LP**. It is false for linear facts as such.
3. **Locality: the kill is never a one-step (Lemma C) kill.** (EMPIRICAL, *float*; §3.3.)
   - On Q12, a certificate that may charge only the inversion of the containment step `[3,4] ≺ [2,5]` does not exist in any family I tried: min Σλ = 5.40 (SW2 on steps), 4.67 (SW3 on steps), 3.42 (SW2 on all pairs), all ≥ 3.
   - What does exist is a certificate that charges only the **two steps around the long interval** `[2,5]`, namely `[3,4] ≺ [2,5] ≺ [4,5]`. It is exact, ratio 2.98707 < 3.
   - That is the Two-Step triple of mg-561a Thm 3.1, but the certificate needs conditioned identities on 14 of Q12's 20 incomparable pairs, including both end pairs.
   - So the unit that works is the **two-step triple, not the containment step**, and its certificate is global.
4. **Lemma C: NOT PROVEN, and not refuted.** (§4.)
   - Lemma C cannot be refuted by computation: that would need a counterexample to 1/3–2/3.
   - Its natural one-step surrogates behave as follows.
     - The **X-local form** (no containment step with `|S| = 2` has `q, u_s, u_t < 1/3` and `s, t` unbalanced) holds for every interval order with n ≤ 10 (EMPIRICAL, exact, `out_probe8.txt`).
       - The 20 configurations at n = 9 that reach the region `q, u_s, u_t < 1/3` all have **twin** separators, so `P[s<t] = 1/2`.
       - At n = 10 there are 333 twin configurations and 29 non-twin ones. Every non-twin one has `P[t<s] ≥ 49/125 > 1/3`.
       - So the local form is really "the separators are balanced". In the examples, that balance comes from the Swap Identity of the pair `(s,t)` itself (§4.1), not from anything at the step.
     - The **XYZ route** fails (item 1).
     - The **step-only certificate** fails on Q12 (item 3).
   - Q12 is the minimal known witness for both failures.
5. **Task 3: what a proof of Lemma C would give.** (§5; complete conditional argument written for audit.)
   - Lemma C + Thm 2.1 (mg-afa4) + Thm 3.1 / 2.1\* / 3.1\* (mg-561a) + Zaguia's Lemma 7 + **K_C** ⟹ 1/3–2/3 for every interval order.
   - **K_C is EMPIRICAL only**: n ≤ 10, the staircase family, and the audit's own family.
   - **Without K_C, Lemma C gives nothing beyond n ≤ 10**, which is already known.
   - I did not run an n = 11 census (Daniel's directive of 2026-09-26; §7).
6. **Recommendation (CONJECTURED direction).** Replace "Lemma C + K_C" by the **level-k swap-certificate conjecture** (§6): every dominance-respecting `L` of a non-chain interval order has a pointwise certificate built from Swap Identities conditioned on at most k other elements, for some small fixed k.
   - k = 0 fails on Q12 (min Σλ = 3.125).
   - k = 2 on the `L`-steps suffices on every obstruction known.
   - This is a reformulation, not a proof. Its value is that the certificate *family* is uniform and every instance is checkable exactly.
7. **Not a proof.** 1/3–2/3 for interval orders remains open, as far as can be verified.

---

## 1. Two general tools (PROVEN, every finite poset)

**Proposition 1.1 (Conditioned Swap Identity).** Let `a ∥ a'`, and let `F` be any set of linear extensions that is invariant under exchanging the positions of `a` and `a'`. For example, `F` may be any event determined by the positions (hence the relative order) of the elements other than `a, a'`. Then
`|Λ₁(a,a') ∩ F| = |Λ₁(a',a) ∩ F|`, and so `P(a<a', F) − P(a'<a, F) = P(Λ₂(a,a') ∩ F) − P(Λ₂(a',a) ∩ F)`.

*Proof.*
- mg-561a Thm 1.1 (audit: HOLDS) shows that the exchange `τ` of `a` and `a'` maps `Λ₁(a,a')` bijectively onto `Λ₁(a',a)`.
- `τ` moves only `a` and `a'`. So `σ ∈ F ⟺ τσ ∈ F`, and `τ` restricts to a bijection `Λ₁(a,a') ∩ F → Λ₁(a',a) ∩ F`. □

With `F` = all extensions this is Thm 1.1. The conditioned forms are new information: the LP of mg-561a has no variable that could express them.

**Proposition 1.2 (pointwise certificates).** Let `R_1, …, R_m` be functions on the linear extensions of `P` with `Σ_σ R_r(σ) = 0` (for instance `R = 1_{Λ₁(a,a')∩F} − 1_{Λ₁(a',a)∩F}`). Let `λ_i ≥ 0` be indexed by the `L`-ordered incomparable pairs `i = (u ≺ v)`, and let `y_r` be real. Suppose that for **every** linear extension `σ`,
`G(σ) := Σ_i λ_i·[v before u in σ] + Σ_r y_r R_r(σ) ≥ g > 0`, and that `Σ_i λ_i < 3g`.
Then `L` is not the 2/3-order of a counterexample.

*Proof.*
- Average over the uniform measure: `Σ_i λ_i P[v before u] ≥ g`, since each `R_r` averages to 0.
- In a counterexample, every `L`-ordered incomparable pair has `P[v before u] < 1/3`, so the left side is `< Σλ_i / 3 < g`. Contradiction. □

**Remarks.**
- *Brightwell's step bound and Thm 3.1 are certificates of this kind.* The union bounds and the inclusions `{z<c} ⊆ Λ₂(b,c)` used in mg-561a are pointwise inequalities between indicators, and Thm 1.1 supplies zero-mean rows.
- *Injection-based facts are not rows.* Prop 2.2 and the Swap Ladder give only one-sided inequalities `|A| ≤ |B|`, so they are not rows of this form.
- *The lift hierarchy.* Call a certificate **level k** when its rows are Swap Identities conditioned on the relative order of at most k other elements (`S0` = level 0).
  - If the rows run over **every** exchange, and in particular every adjacent transposition, they force `μ` = uniform. Then a certificate exists for every `L` of every non-counterexample. That is the control `ADJ` in `mulp.py`: Q12 gives `−0.1043`, which is exactly `1/3 − 0.4376` (the true `P[[2,5]<[3,4]]`).
  - So the whole content lies in how **low** a level suffices.

**The full-measure lift** (`mulp.py`) is the LP in the variables `μ(σ) ≥ 0`, `Σμ = 1`, with the chosen rows as equalities and `μ(v before u) ≤ 1/3 − ε`. It maximises `ε`. Its dual is exactly the certificate LP of Prop 1.2 (`certify.py`).

---

## 2. Task 1: XYZ on Q12 (answer: no instance kills it)

### 2.1 The probe (`xyzlp.py`, `bnb.py`, `xyzcheck.py`)

Start from mg-561a's LP (T1 + T2 + T3, read-only; `ε* = 1/48`). Add:
- **(TRI)** an exact order law on each chosen triple: one variable per ordering consistent with `P`, total 1, with every pair marginal equal to the LP's pair law. This contains every 3-cycle row and every Fréchet bound.
- **(JT)** the LP's joint variable of each AA/BB two-separator pair, tied to its triple law. At the containment step, `J = P[s<a', t<a']`.
- **(XYZ)** for every `x` and every `y, z ∈ Inc(x)`: `P[x<y, x<z] ≥ P[x<y]P[x<z]`, and the dual `P[y<x, z<x] ≥ P[y<x]P[z<x]`.

The XYZ rows are imposed first through McCormick under-estimators on the `L`-boxes, which is a valid relaxation. Then `bnb.py` runs a spatial branch-and-bound on the exact products: it splits a pair-law box at the most violated instance until either every node is refuted or an optimum satisfies every product.

| system (Q12, staircase `L`) | `ε*` | how |
|---|---|---|
| mg-561a T1+T2+T3 | 1/48 | exact (reproduced) |
| + TRI/JT (4 triples) | **1/75** | exact, Fractions (`out_xyzlp.txt`) |
| + all 40 triples + 240 McCormick XYZ rows | 1/75 | exact, Fractions (`out_xyzlp.txt`) |
| + XYZ exactly (branch-and-bound, 17 nodes) | **1/75**, attained at a point satisfying every XYZ instance to 10⁻⁹ | *float* (`out_bnb.txt`) |

**Reading.**
- The linear repair (JT) is worth `1/48 → 1/75`: the pair-law LP did not know that `P[s<a']`, `P[t<a']`, `P[s<t]` and `J` come from one law on three elements.
- Correlation is worth nothing. The unrepaired optimum violates only 4 XYZ instances, all by ≤ 0.0043 (`out_xyzcheck.txt`). They are centred on `[2,5]` and `[5,8]`: for example `P[[4,5] < [2,5], [4,5] < [5,8]]`. Branching on those boxes moves the optimum to a point where every instance holds, at the same `ε`.

**Answer to task 1.** The minimal set of XYZ/FKG (triple) instances making the system infeasible on Q12 does not exist: the full set leaves it feasible (EMPIRICAL, *float*). Not tested: FKG / Ahlswede–Daykin in forms not reducible to triple XYZ, Stanley and Kahn–Saks log-concavity (§7).

### 2.2 Why XYZ cannot act at the containment step itself (PROVEN)

**Proposition 2.1.** Consider the local system at a containment step with `Z = S = {s,t}`, in the variables `q, γ, u_s, u_t, β`. It consists of:
- the Swap Identity `u_s + u_t − β = 1 − 2q + γ`;
- Prop 2.2: `β ≤ q − γ` and `u_s + u_t − 2β ≤ q − γ`;
- the counterexample bounds `q, u_s, u_t < 1/3`;
- `0 ≤ β ≤ min(u_s, u_t)`;
- XYZ (dual form): `β ≥ u_s u_t`.

This system is satisfiable. For example, `q = u_s = u_t = 3/10`, `γ = 0`, `β = 1/5` satisfies every constraint strictly where strictness is required.

*Proof.* Substitute:
- `u_s + u_t − β = 2/5 = 1 − 2q`;
- `β = 1/5 ≤ 3/10 = q`;
- `u_s + u_t − 2β = 1/5 ≤ 3/10`;
- `β = 1/5 ≥ 9/100 = u_s u_t`;
- `β ≤ 3/10`. □

The mechanism: the only nonlinear quantity at the step is `β`. XYZ raises its lower bound, which lowers the union `u_s + u_t − β`. But Thm 1.1 needs the union to be **large**, so the XYZ bound points the wrong way. (mg-561a §4 already noted this in words; Prop 2.1 makes it exact.)

---

## 3. What kills Q12 and the other 12 survivors (the full-measure lift)

### 3.1 Results (`mu_surv.py` → `out_mu_surv.txt`; certificates `certs.json`, exact check `out_verify.txt`)

| survivor (P) | e(P) | pair-LP `ε*` (mg-561a) | lift, S0 | lift, S0 + SW2 on `L`-steps | exact certificate (ratio Σλ/g < 3) |
|---|---|---|---|---|---|
| `[1,1][1,2][1,5][2,3][2,7][3,4][4,5][5,6][5,8][6,7][7,8][8,8]` | 19837 | 0.00980 | −0.0145 | −0.0256 | S0: 2.87500 |
| **Q12** | 2765 | 0.02083 | **+0.0133** | −0.0019 | SW2: 2.98303 |
| `[1,1][1,2][1,4][2,3][2,8][3,4][4,5][4,9][5,6][6,7][7,8][8,9][9,9]` | 40778 | 0.01190 | −0.0249 | −0.0295 | S0: 2.79167 |
| `…[1,5]…[2,7]…[5,8]…[8,9][9,9]` | 30911 | 0.00980 | −0.0145 | −0.0255 | S0: 2.87500 |
| `…[1,5]…[2,8]…[5,8]…` | 34512 | 0.00980 | −0.0145 | −0.0265 | S0: 23/8 |
| `…[1,5]…[2,8]…[5,9]…` | 41855 | 0.00980 | −0.0145 | −0.0277 | S0: 23/8 |
| `…[1,5]…[2,9]…[5,8]…` | 39111 | 0.00980 | −0.0145 | −0.0274 | S0: 2.87500 |
| `…[1,6]…[2,8]…[5,9]…` | 48620 | 0.01075 | −0.0303 | −0.0459 | S0: **11/4** |
| `…[1,6]…[2,8]…[6,9]…` | 40778 | 0.00546 | −0.0249 | −0.0295 | S0: 2.79167 |
| `…[2,6][3,8]…[6,9]…` | 31024 | 0.00980 | −0.0145 | −0.0235 | S0: 23/8 |
| `[1,1][1,2][2,3][2,5][3,4][4,5][5,6][5,9][6,7][7,8][8,9][9,10][10,10]` | 5237 | 0.02083 | +0.0133 | −0.0017 | SW2: 2.98478 |
| `…[2,6]…[5,9]…[9,10][10,10]` | 6294 | 0.02564 | +0.0108 | −0.0255 | SW2: 2.78657 |
| `…[2,6]…[6,9]…[9,10][10,10]` | 5237 | 0.02083 | +0.0133 | −0.0017 | SW2: 2.98478 |

(Full intervals of every row are in `out_mu_surv.txt` and `certs.json`.)

**PROVEN (computer-checked, exact).** For each of the 13 `(P, L)`, `certs.json` holds rational `λ, y` satisfying Prop 1.2. `verify_certs.py` rebuilds the rows, checks that each row sums to 0 over all extensions, and evaluates `G` on every linear extension in `Fraction`s. So none of the 13 survivors is the 2/3-order of a counterexample, and this uses no correlation inequality. Of course, the 13 posets are already known to satisfy 1/3–2/3 (n ≤ 14, Gupta 2026). The point is **which facts** suffice.

**Controls** (`out_verify.txt`):
- (c1) scaling `λ` by 9/10: CAUGHT.
- (c2) dropping all identity rows: CAUGHT. It must be: with no rows, `μ` = the point mass on `L` is feasible, and it charges no inversion.
- (c3) a non-identity row (`1_{Λ₁}` of one orientation only, sum 807 ≠ 0): CAUGHT.
- `mulp.py` `ADJ` reproduces the true margin of Q12, −0.10428.

### 3.2 What the small certificates are

The 11/4 certificate is on `P = [1,1][1,2][1,6][2,3][2,8][3,4][4,5][5,6][5,9][6,7][7,8][8,9][9,9]`, with `L = … [3,4] [1,6] [2,8] [4,5] …`. Its data:
- Charged inversions: `(3/2)·[[4,5] before [2,8]]` and `(5/4)·[[2,8] before [3,4]]`, the two `L`-neighbours of the long interval `c = [2,8]` (through `[1,6]`).
- Rows: the plain Swap Identities of `(c, d)` for `d ∈ {[1,2], [2,3], [3,4], [4,5], [6,7], [8,9]}`, with weights `−1/4, −1/2, −1/2, 1, 1/2, 1/2`.
- Pointwise, `G ≥ 1` on all 48 620 extensions, and `Σλ = 11/4 < 3`.

It is a **star around one long interval**: every row is a Swap Identity of `c` with one partner. The difference from Thm 3.1 is that the six identities are combined on each extension, instead of through union bounds on each one separately. The pair-LP loses exactly this joint information, because it keeps only one union-bounded scalar `B(a,a')` per pair.

Every S0 certificate in the table has this shape: 2–4 charged pairs, 6–9 rows, all rows through the one or two long intervals.

### 3.3 Locality on Q12 (`window.py`, `window3.py`, `local_q12.py`; *float*)

Restrict the charged `λ` to `L`-ordered pairs whose two `L`-positions both lie in a window, and leave the rows unrestricted. Positions: 0 `[1,1]`, 1 `[1,2]`, 2 `[2,3]`, 3 `[3,4]`, 4 `[2,5]`, 5 `[4,5]`, 6 `[5,6]`, 7 `[5,8]`, …

| rows \ charged window | [3,4] (the containment step only) | [2,5] | [1,7] | [0,5] | [0,11] (all) |
|---|---|---|---|---|---|
| S0 + SW2 on steps | 5.40 | 3.167 | 3.167 | **2.989** | 2.983 |
| S0 + SW3 on steps | 4.67 | 3.151 | 3.151 | – | 2.970 |
| S0 + SW2 on all pairs | 3.42 | **2.987** | 2.987 | – | 2.903 |

(min Σλ; below 3 = refuted.)

- **No family I tried certifies Q12 by charging the containment step alone.** A one-step Lemma C certificate for Q12 does not exist at these levels.
- With step-conditioned rows, the charged window must reach an **end** (`[0,5]` works; `[1,7]` does not, sitting at 19/6).
- With conditioning on all pairs, the window `[2,5]` suffices. The exact certificate in `certs.json` charges only `[3,4] ≺ [2,5]` (λ ≈ 1.057) and `[2,5] ≺ [4,5]` (λ ≈ 1.930): **the two-step triple around `a' = [2,5]`**, exactly Thm 3.1's unit. Its ratio is 2.98707.
- A deletion filter over the conditioned pairs (`out_local_q12.txt`) keeps 14 of the 20 incomparable pairs, including the end pair `([1,1],[1,2])`, which carries the largest row weight. The margin then drops to 2.9998. So the rows needed are global even when the charge is local.

---

## 4. Task 2: Lemma C

**Lemma C (CONJECTURED, unchanged).** In a counterexample, no `L`-consecutive containment step has exactly two separators.

**Status: NOT PROVEN.** I did not find a proof, and I found no weaker general lemma that is proven and kills all 13 survivors. The 13 refutations of §3 are per-instance certificates, not a lemma.

### 4.1 The X-local form is "the separators are balanced" (EMPIRICAL, exact, `out_probe8.txt`)

For every containment two-separator pair of every interval order with n ≤ 10, `probe8.py` computes the exact law of the relative order of `(a, a', s, t)`. It selects the pairs with `q = P[a'<a] < 1/3`, `u_s < 1/3` and `u_t < 1/3`, the region a counterexample needs.

| n | pairs in the region | twin separators (`s`, `t` equal intervals) | non-twin | min `P[t<s]` over non-twin (`s` = the likelier first) |
|---|---|---|---|---|
| ≤ 8 | 0 | – | – | – |
| 9 | 20 | 20 | 0 | – |
| 10 | 362 | 333 | 29 | **49/125 > 1/3** |

- So whenever the step itself looks like a counterexample, `s` and `t` are balanced. They are twins, or `P[t<s] ≥ 0.392`. A counterexample has no twins (twins are balanced), and it has no balanced pair.
- The reason, checked on the tightest n = 10 case (`a = [3,4]`, `a' = [2,6]`, `s = [5,6]`, `t = [6,6]`):
  - The pair `(s,t)` is a dominance pair with the single separator `[4,5]`, which lies `L`-before `s`.
  - Cor 1.2 of mg-561a gives `P[s<[4,5]] = 1 − 2P[t<s]`, and `P[s<[4,5]] < 1/3` forces `P[t<s] > 1/3`.
  - That is Thm 2.1\*, a **non-local** fact about the pair `(s,t)`.
- Reading: the local form of Lemma C is not a statement about the step. It is inherited from the separators' own pair.

### 4.2 What I tried for a proof, and where each stops

1. **XYZ on the step's elements.** Refuted as a route by Prop 2.1 and §2.1.
2. **The dual Swap Ladder beyond unique tops.**
   - The Swap Identity for the non-consecutive pair `(a', s)` (when `r(s) ≤ r(a')`) reads `P(∪_{m ∈ M_s}{a' < m}) = 1 − 2u_s`. Here `M_s = max{z : l(a') ≤ r(z) < l(s)} ∋ a`. For `M_s = {a}` this is Prop 2.4 of mg-561a.
   - With `|M_s| ≥ 2`, the other maximal elements `m` overlap `a`. When `m ≺ a` in `L` (as `[2,3]` in Q12), each event `{a' < m}` is an `L`-inversion `< 1/3`, and the identity needs only their union `> 1/3`: no contradiction.
   - This identity is already in the pair-LP, so it cannot be the missing piece.
3. **One-step certificates at any level I could compute** (§3.3). None exists on Q12.

### 4.3 A weaker statement that is supported (CONJECTURED)

**Conditioned Two-Step Conjecture.** Let `a ≺ c ≺ b` be `L`-consecutive with `a ∥ c ∥ b`, where one of the two steps is a containment step with `|S| = 2` and the other is a dominance step. Then a level-2 pointwise certificate exists that charges only `P[c<a]` and `P[b<c]`.

- Evidence: Q12 only (§3.3, ratio 2.98707), plus the fact that all 13 survivors are refuted at level ≤ 2.
- I state it so it can be attacked or refuted. It is **not** a local lemma: on Q12 its rows reach the ends.

---

## 5. Task 3: what a proof of Lemma C would give (complete conditional argument, for audit)

**Theorem 5.1 (CONDITIONAL on Lemma C and on K_C).** Assume
- **Lemma C**: in any counterexample `P` with 2/3-order `L`, no `L`-consecutive strict-containment step has exactly two separators; and
- **K_C**: every dominance-respecting linear extension `L` of every non-chain interval order contains at least one of:
  - (i) an `L`-consecutive incomparable step with `|S| ≤ 1`;
  - (ii) a Thm 3.1 triple with `k ≤ 2`, a Thm 2.1\* pair or a Thm 3.1\* triple;
  - (iii) an `L`-consecutive strict-containment step with `|S| = 2`.

Then every non-chain interval order has a balanced pair (1/3–2/3 holds for interval orders).

*Proof (each step with its source and status).*
1. Suppose `P` is a non-chain interval order with no balanced pair. Every incomparable pair then has `P[x<y] > 2/3` or `< 1/3`.
   - The relation "`x` before `y` with probability > 2/3" is a linear extension `L` of `P`: mg-afa4 Thm 2.1(a), audit mg-5ecf HOLDS.
2. `P` has no twins, since a pair of twins is balanced.
   - If `x` dominates `y` (`l(x) ≤ l(y)`, `r(x) ≤ r(y)`, not equal), then Zaguia's Lemma 7 gives `P[x<y] ≥ 1/2`, so `x ≺ y` in `L`.
   - Hence `L` is dominance-respecting. (Zaguia Lemma 7 was checked against the source in audit mg-5ecf.)
3. By K_C, `L` contains (i), (ii) or (iii).
   - (i) contradicts mg-afa4 Thm 2.1(b), Brightwell's separator injection, audited HOLDS: every consecutive incomparable step has `|S| ≥ 2`.
   - (ii) contradicts mg-561a Thm 3.1, 2.1\* or 3.1\*, audited HOLDS in mg-6c30 §2.4.
   - (iii) contradicts Lemma C.
4. So no such `P` exists. □

**What is and is not established.**

| ingredient | status |
|---|---|
| Thm 2.1(a,b) (mg-afa4) | PROVEN, audited |
| Zaguia Lemma 7 (dominance ⟹ ≥ 1/2) | PROVEN (literature), checked by audit |
| Thm 3.1, 2.1\*, 3.1\* (mg-561a) | PROVEN, audited |
| Prop 3.1 (mg-afa4: `|S| = α + β`, interval form) | PROVEN, audited; only used to identify (iii) in interval terms. Separators are computed from covers throughout. |
| **Lemma C** | **CONJECTURED** (this file, §4) |
| **K_C** | **EMPIRICAL**: census n ≤ 10 (2/2 and 29/29 `L`, reproduced by audit mg-6c30), 547 staircase posets (mg-561a), 8 survivors of the audit's own family. **Unsearched: n = 11 outside the staircase family.** Claim K, its predecessor, looked as solid through n = 8 and failed at n = 9. |

**So: "Lemma C ⟹ 1/3–2/3 for interval orders" is FALSE as stated. It is "Lemma C + K_C ⟹ 1/3–2/3 for interval orders".**
- Without K_C, a proof of Lemma C gives exactly Cor 3.2 of mg-561a (n ≤ 10, already probability-free). It adds a probability-free certificate for each `(P, L)` that contains pattern (iii), and nothing uniform in n.
- Even with K_C, no bounded-range or width hypothesis enters, so the result would be unconditional for interval orders.

---

## 6. Task 4 / what the failure means

- **Lemma C itself cannot be given a computational counterexample.** Its hypothesis ("in a counterexample") is empty unless 1/3–2/3 fails.
- What fails is each **route** to it, and Q12 is the minimal known witness for all of them:
  - the XYZ route (§2);
  - the one-step certificate route (§3.3);
  - the pair-LP route (mg-561a §4).
- The X-local form of Lemma C does not fail through n = 10 (§4.1), but it is not a statement about the step.

**What it means.** The obstruction that mg-561a located at Q12 is not a missing *correlation* inequality. It is missing *joint consistency*.
- The pair-LP keeps one union-bounded scalar per pair.
- The true constraints are the Swap Identities as identities of **one** measure: plain ones kill 9/13, and ones conditioned on two elements kill the rest.

**The natural replacement for Lemma C + K_C (CONJECTURED).**

> **Level-k certificate conjecture (LC_k).** There is a fixed k such that every dominance-respecting linear extension of every non-chain interval order admits a pointwise certificate (Prop 1.2) whose rows are Swap Identities conditioned on the relative order of at most k other elements.

- LC_k for any k implies 1/3–2/3 for interval orders (Prop 1.2 + §5 steps 1–2). It needs no K_C, because it charges no particular pattern.
- It is as unproven as K_C. Its advantages are that the family of rows is uniform, and that each instance is an exact, independently checkable object.
- Evidence: k = 0 fails at Q12 (min Σλ = 3.125). k = 2 on `L`-steps succeeds on all 13 known LP survivors. Nothing beyond them was tested.
- A proof would need a *structural* certificate: for example, the star shape of §3.2 around each long interval, together with a separate argument for staircases, where Brightwell's semiorder argument already works.

---

## 7. What I did NOT do; candidates ruled out

**Not done.**
- **No proof of Lemma C.** No proof of K_C. No proof of LC_k.
- **No n = 11 census for K_C.** pm-onethird's input asked to "prove it, or test it harder (an n = 11 census)". Daniel's directive of 2026-09-26 ("avoid more rote computation of cases") takes precedence, so K_C's gap at n = 11 outside the staircase family stays open and is flagged.
- **Float steps.** The branch-and-bound claim (XYZ does not kill Q12) and the window/locality tables are *float* (HiGHS). They are not certified exactly. The exact parts are the 1/75 values and the 14 certificates.
- **Correlation inequalities not tested:** FKG / Ahlswede–Daykin on the down-set lattice beyond triple XYZ; Graham–Yao–Yao on two chains; Stanley and Kahn–Saks log-concavity (these need position variables); XYZ inside the full-measure lift. Since linear conditioned identities already refute all 13, I did not pursue them further.
- **Certificates for other populations.** Only the 13 named survivors and Q12's window were certified. No certificate was searched for the other 9 LP-refuted survivors (they are already refuted) or for any new population.
- **The deletion filter** of `local_q12.py` is greedy, so its 14-pair set is minimal only for inclusion in that order.
- **Bounded range was not used.** Q12's maximum incomparability degree is 6 (audit mg-6c30 §1(d)). Nothing here depends on range.

**Candidates ruled out.**

| candidate | fate |
|---|---|
| XYZ on `{s, t, a'}` at the step | cannot help (Prop 2.1, PROVEN) |
| XYZ on all 40 triples of Q12, exactly | Q12 stays feasible at 1/75 (*float*) |
| triple-law consistency (linear) | 1/48 → 1/75, not enough (exact) |
| plain Swap Identities on a full measure (S0 lift) | kills 9/13; fails on the Q12 family (Q12: +1/75, min Σλ = 3.125) |
| lift + Swap Identities conditioned on 1 other element (all pairs) | Q12 stays at +1/75 (`out_mu_q12.txt`, *float*) |
| lift + pointwise exchange invariance at the two containment steps | Q12 at +1/111 (`out_mu_q12.txt`, *float*) |
| lift + SW2 on a single `L`-step, any one of the 11 | Q12 feasible, best +0.0069 at the end steps (`out_mu_q12b.txt`, *float*) |
| a one-step certificate charging the containment step alone | none on Q12 at SW2-steps / SW3-steps / SW2-all (5.40 / 4.67 / 3.42) |
| local Lemma C via the X-law | holds n ≤ 10, but only through separator balance (§4.1) |
| the dual Swap Ladder past a branch | reduces to the Swap Identity of `(a', s)`, already in the LP (§4.2) |

## 8. Files (`code/ksbft_t3_lemma_c_785e/`)

| file | content | output |
|---|---|---|
| `t3lib.py` | imports; `order_law` (exact order law of a tuple), `cont_pairs` | — |
| `probe8.py` | §4.1 X-law of containment two-separator pairs, n ≤ N (pure Python, exact) | `out_probe8.txt` |
| `xyzlp.py` | pair-LP + TRI/JT + McCormick XYZ (exact `xlp`) | `out_xyzlp.txt` |
| `flp.py`, `bnb.py`, `xyzcheck.py` | float LP; spatial branch-and-bound on exact XYZ; XYZ residuals (scipy) | `out_bnb.txt`, `out_xyzcheck.txt` |
| `mulp.py` | full-measure lift; rows S0 / SW / PT / ADJ | — |
| `mu_q12.py`, `mu_q12b.py`, `mu_surv.py` | lift values on Q12 and the 13 survivors (scipy) | `out_mu_q12.txt`, `out_mu_q12b.txt`, `out_mu_surv.txt` |
| `window.py`, `window3.py`, `local_q12.py` | §3.3 locality (scipy) | `out_window.txt`, `out_window3.txt`, `out_local_q12.txt` |
| `certify.py`, `gen_certs.py` | propose multipliers (scipy), round, exact check | `out_certify.txt`, `certs.json` |
| `verify_certs.py` | **exact** check of all 14 certificates + 3 controls (pure Python) | `out_verify.txt` |
| `survivors.py` | the 13 LP-feasible survivors, parsed read-only from mg-561a's `out_lpsurv.txt` | — |
| `run_all.sh` | regenerates the pure-Python transcripts and asserts headlines and controls; scipy probes run only if scipy is importable | — |
