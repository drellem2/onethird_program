# AUDIT mg-785e (KSBFT-T3, Lemma C for interval orders): no proof of 1/3–2/3 for interval orders is claimed, and none is hidden. Every PROVEN statement HOLDS on re-derivation, and all 14 certificates re-check exactly in an independent engine. K_C is EMPIRICAL, not PROVEN. NEW: the X-local form of Lemma C is FALSE at n = 12 (X12, exact). So no argument that uses only the joint law of {a, a', s, t} can prove Lemma C (mg-f4f0)

Audit ticket mg-f4f0. Audited: `docs/KSBFT-T3-lemma-C.md` (commit aaf53af), instrument `code/ksbft_t3_lemma_c_785e/`.

My instrument is `code/audit_ksbft_f4f0/` (README there).
- It imports no code from the audited branch, from mg-561a, from `iolib.py` or from earlier audits.
- Author artefacts are read as data only: the λ/y weights in `certs.json`, and the 22 survivors in mg-561a's `out_lpsurv.txt`.
- The one exception is the author's `xyzlp.py`, re-run unmodified and labelled a reproduction.
- `sh run_all.sh` asserts every headline and control below (~2 min).

Labels: **PROVEN**, **EMPIRICAL**, **CONJECTURED** as in the audited doc. Verdicts: **HOLDS / BROKEN / OVERSTATED / UNVERIFIABLE**.

---

## 0. Verdict

1. **Does T3 prove 1/3–2/3 for interval orders? No, and it does not claim to.**
   - The only end-to-end statement is Thm 5.1, which is **conditional on Lemma C and on K_C**.
   - pm-onethird asked me to check that K_C is PROVEN if the doc claims interval orders. The doc does not claim them, and **K_C is EMPIRICAL** (§4 below).
   - The conditional argument itself HOLDS.
   - The one wording error sits at the conclusion: "Lemma C ⟹ 1/3–2/3 is FALSE as stated" is OVERSTATED. That implication is unproven, not false: if 1/3–2/3 holds for interval orders, it is vacuously true.
2. **Every PROVEN statement HOLDS.** Re-derived line by line:
   - Prop 1.1 (Conditioned Swap Identity) and Prop 1.2 (pointwise certificates);
   - Prop 2.1 (XYZ points the wrong way at the step), including the XYZ direction and hypotheses;
   - the §4.2 identity for `(a', s)`;
   - the logic of Thm 5.1.

   Tested with firing controls:
   - Prop 1.1: 3 580 exact (pair, event) checks by enumeration (general posets and interval orders, n = 5–9) and 400 automaton-DP checks on random interval orders with n = 12–20. 0 violations.
3. **The 14 certificates HOLD, re-checked independently.**
   - My own rows, built from the definitions, each checked to sum to 0, evaluated on every linear extension in `Fraction`s: 14/14 VALID.
   - Six controls are CAUGHT.
   - My own extension counts reproduce every `e(P)` in the §3.1 table.
   - One imprecision: the §3.2 prose certificate works only with the rows oriented by element index. Read literally as rows of `(c,d)`, it gives min G = 0.
4. **§3.3 locality and §6 "k = 0 fails at 3.125" HOLD** (independent float LP, own rows). Every table entry I re-ran reproduces: 5.40, 3.42, 3.167, 19/6, 2.989, 2.987, 2.983, 2.903 and 3.125. The SW3 row (4.67 / 3.151 / 2.970) was not re-run.
5. **§4.1 X-local census HOLDS exactly for n ≤ 10** (own generator, certified counts).
   - The region counts are 20/20 twins at n = 9, and 362 = 333 + 29 at n = 10 with min 49/125.
   - **The reading built on it is BROKEN beyond n = 10.** The doc says "whenever the step itself looks like a counterexample, s and t are balanced", and "the local form is really 'the separators are balanced'".
   - **X12 (n = 12)** is a containment step with |S| = 2 where `q, u_s, u_t < 1/3` and `(s,t)` is unbalanced. Three independent exact computations agree.
   - The mechanism the doc cites (Cor 1.2 on the pair `(s,t)` with a single separator) covers only **16 of the 29** n = 10 cases. X12 is the n = 10 tight case with one extra separator for `(s,t)`.
6. **New consequence (PROVEN by exact computation; §3.3 below).** X12 is *locally counterexample-compatible on X = {a, a', s, t}*.
   - So **no inequality whatsoever**, correlation, log-concavity or otherwise, combined with counterexample hypotheses on pairs inside X, can prove Lemma C.
   - This strengthens Prop 2.1 from "XYZ cannot" to "nothing X-local can". It also closes the §7 untested items (Stanley, Kahn–Saks, Ahlswede–Daykin) *as X-local routes*.
   - A proof of Lemma C must use hypotheses on pairs outside X. In X12 the first such pair is `(a', [3,5])`, with Y = the common incomparables of `a, a'`.
7. **K_C: EMPIRICAL (answers pm-onethird).**
   - My own implementation of (i)/(ii)/(iii), written from the doc text, confirms that each of the 22 staircase survivors has pattern (iii) and nothing else.
   - A bounded counterexample search found no K_C-bad `L`: 0 on 458 251 canonical staircase-type interval orders with n = 11–14, from 2 shards of 229 244 and 229 007 distinct posets that may overlap.
   - Its pipeline control fires: with (iii) allowed, the same pipeline finds 49 `L` avoiding (i) and (ii), and all contain (iii).
   - This is evidence, not a proof.

**Bottom line.** 1/3–2/3 for interval orders remains open, as far as can be verified. T3's own recommendation (drop the one-step unit; LC_k) is **reinforced** by X12. The containment step cannot be killed by its own four elements.

---

## 1. Line-by-line re-derivation of the PROVEN claims

### 1.1 Prop 1.1 (Conditioned Swap Identity): HOLDS

- The separators are `A(a,a') = {z : a ⋖ z, z ∥ a'}` and `B(a,a') = {w : w ⋖ a', w ∥ a}`. With them, `Λ₁(a,a') = V ∩ {a before a'}`, where `V` is the set of extensions in which exchanging `a` and `a'` is valid.
- Why that holds:
  - A separator between them blocks the exchange.
  - Conversely, any `x` between them with `a < x` has a cover `a ⋖ c ≤ x`. Here `c` lies between them and `c ∥ a'`: `c < a'` would give `a < a'`, and `c > a'` is impossible since `c` precedes `a'`. So `c` is a separator between them. The case `x < a'` is dual.
- The exchange `τ` moves only `a` and `a'`, so it preserves every event determined by the positions (or relative order) of the other elements. Restricting the bijection to `F` is therefore legitimate.
- The doc's example ("any event determined by the positions of the elements other than a, a'") is exactly τ-invariance.
- Test (`out_prop11.txt`):
  - Events tested: the order of 2 and of 3 others, the position of a third element, and a mixed event. 3 580 checks, 0 violations.
  - Automaton DP on interval orders with n ≤ 20: 400 checks, 0 violations.
  - Controls fire. `F = {pos(a) = k}`, which is not τ-invariant, breaks the identity on 895 pairs. A-only separators break it on 433 (enumeration) and on 83 (DP).

### 1.2 Prop 1.2 (pointwise certificates): HOLDS

Averaging `G ≥ g` over the uniform measure kills every zero-sum row. In a counterexample every L-inversion has probability `< 1/3`. Remarks:
- The strict hypothesis `Σλ < 3g` can be weakened to `Σλ ≤ 3g`. The strictness already comes from `P < 1/3`, and `Σλ > 0` is forced, since the rows alone average to 0 < g.
  - With this weakening, the §1 remark that "rows over every exchange give a certificate for every L of every non-counterexample" is correct even when a pair sits at exactly 1/3, as in (2+1).
  - In the doc's strict form, that case is a boundary exception. This is harmless.
- "Injection-based facts are not rows" is correct: one-sided inequalities are not zero-sum.
- Important for what the certificates mean: **soundness needs only Σ_σ R_r(σ) = 0**, which `verify_certs.py` and my `certs_indep.py` check directly. That the rows are *theorem instances* (Swap Identities) is what makes the certificate probability-free in principle. The check itself enumerates extensions, and the doc says so.

### 1.3 Prop 2.1 (XYZ at the step): HOLDS; direction and hypotheses checked

- **XYZ direction.** Shepp's XYZ inequality holds for every triple of every finite poset: `P[x<y, x<z] ≥ P[x<y]P[x<z]`. Its order dual is `P[y<x, z<x] ≥ P[y<x]P[z<x]`.
  - With `x = a'`, `y = s`, `z = t` it gives `β = P[s<a', t<a'] ≥ u_s u_t`. That is the row used.
  - No comparability pattern is required beyond the triple being in the poset. The application is to the uniform measure on the linear extensions of `P` itself. Correct.
- **The local system's rows**, re-derived from mg-561a:
  - The identity reads `u_s + u_t − β = 1 − 2q + γ`. Here `Λ₂(a,a') = {s<a'} ∪ {t<a'}` when `Z = S`. This is exact, because a non-minimal element of `Z` between `a` and `a'` forces a minimal one between them.
  - Prop 2.2 gives `β ≤ q − γ` and `u_s + u_t − 2β ≤ q − γ`, with `P(Λ₁) = q − γ`.
- **The witness `(3/10, 0, 3/10, 3/10, 1/5)`** satisfies every row exactly (`out_prop21.txt`).
- **The mechanism** is correct: `β` enters the union with a minus sign, so raising its lower bound can only shrink the union.
- **Strengthening (new).** X12 (§3) is a *real* poset whose true values satisfy the whole local system. Its `Z = S`, and it has q = 91/276, u_s = 269/828, u_t = 169/828, β = 127/828, and γ = 29/828 computed directly from `Λ₂(a',a)`, not from the identity. There `β/(u_s u_t) = 2.31`. So Prop 2.1's satisfiable point is not only abstract; it is realised.

### 1.4 §4.2 item 2 (the identity for `(a', s)`): HOLDS

- `r(s) ≤ r(a')` and `l(a') < l(s)` mean that `a'` dominates `s`, so `S(s,a') = ∅` and Cor 1.2 applies: `P(Λ₂(a',s)) = 1 − 2u_s`.
- `A(a',s) = ∅`, because anything above `a'` is above `s`.
- `B(a',s)` is exactly the set `M_s` of maximal elements of `D_s`. A maximal element of `D_s` covers into `s`: an intermediate `v` with `w < v < s` would lie in `D_s`. Conversely, a cover of `s` that is incomparable to `a'` lies in `D_s` and is maximal there.
- The event "`w` between `a'` and `s`" is `{a' < w}`. The displayed identity follows.

### 1.5 Thm 5.1 (conditional): the logic HOLDS

- Step 1: the 2/3-relation is a linear extension (mg-afa4 Thm 2.1(a), audited).
- Step 2: no twins, and dominance implies `P ≥ 1/2` (Zaguia Lemma 7, audited), so `L` is dominance-respecting.
- Step 3: (i) is excluded by Thm 2.1(b); (ii) by Thm 3.1/2.1\*/3.1\*, each audited HOLDS in mg-6c30; (iii) by Lemma C.
- K_C quantifies over all dominance-respecting `L`, so it covers the `L` of step 1.
- K_C is purely combinatorial, since it involves no probabilities. The statement is well typed, and the argument is complete **given** its two hypotheses.

---

## 2. The computational claims, re-tested independently

### 2.1 The 14 certificates (§3.1, §3.2): HOLD

`certs_indep.py` → `out_certs_indep.txt`.
- My rows are built from the definitions with my own covers, separators and extension list: S0, then SW over `L`-steps or all pairs, conditioned on the order of every 2-set.
- Every used row is checked to sum to 0.
- `G` is evaluated on every extension in `Fraction`s, and each charged pair is checked to be an `L`-ordered incomparable pair.
- Results:

  | certificate | VALID | ratio |
  |---|---|---|
  | 9 S0 (the non-Q12 family) | 9/9 | 23/8 to 11/4 |
  | 4 SW2-step (Q12 family) | 4/4 | 2.983, 2.985, 2.787, 2.985; they use 157–203 conditioned rows each |
  | Q12 window [2,5] | 1/1 | 2.98707, using 269 conditioned rows |

- Soundness here does not depend on matching the author's row labelling: any validated certificate built from zero-sum identity rows is a real certificate.
- **Controls CAUGHT:** Q12 λ × 9/10; the largest row weight sign-flipped; a wrong `L` (a charged pair no longer `L`-ordered); no rows; A-only rows (nonzero sum on 34 ordered pairs); `F = {pos(a) = k}`.
- **§3.2 prose.** With rows oriented as literally written ("`(c,d)`"), the stated weights give min G = 0 (INVALID). Over the 64 orientations, the one that works (min G = 1, Σλ = 11/4) orients `[1,2]` and `[2,3]` as `(d,c)`, which is index order. So the certificate HOLDS, but the prose needs "rows oriented lower-index first". This is a minor imprecision.

### 2.2 Locality (§3.3) and k = 0 (§6): HOLD (float, independent LP)

`lp_indep.py` → `out_lp_indep.txt`: own rows, own LP (HiGHS), min Σλ subject to G ≥ 1.

| rows | step [3,4] only | window [2,5] | [0,5] | [1,7] | all |
|---|---|---|---|---|---|
| S0 | infeasible | 3.25 | 3.125 | 3.25 | **3.125** |
| S0+SW2 on steps | **5.4034** | 3.1667 | **2.9895** | **3.1667 (19/6)** | 2.9830 |
| S0+SW2 on all pairs | **3.4201** | **2.9871** | 2.9064 | 2.9870 | 2.9031 |

Every entry the doc states reproduces. Not re-run: SW3 (4.67 / 3.151 / 2.970) and the greedy deletion filter (14 of 20 pairs). Q12 has 20 incomparable pairs and maximum incomparability degree 6: HOLDS.

### 2.3 §2.1 (XYZ on Q12)

| claim | verdict |
|---|---|
| exact 1/48 → 1/75 (TRI/JT), and 1/75 with 240 McCormick XYZ rows | **reproduced with the author's code** (`out_repro_xyzlp.txt`, 143 s), so not independent |
| spatial branch-and-bound: 1/75 at a point satisfying every XYZ instance | **UNVERIFIABLE** here (float, not re-run) |

The claim "XYZ is not the missing input" is in any case superseded by §3 below. At the step, nothing X-local is the missing input.

### 2.4 Q12, T11 and the survivors

Exact values, own engine (`out_mech.txt`):
- Q12: `e = 2765`, and `P[[2,5]<[3,4]] = 242/553`, so the ADJ control value `1/3 − 242/553 = −0.10428` HOLDS.
- T11: `P[a<a'] = 2/3`, `P[s<a'] = 1/3`, `P[t<a'] = 1/5`, `P[s<t] = 43/60`. These HOLD, and T11 is the tie.

The 22 staircase survivors (`out_kc.txt`):
- Each one's `L` is a dominance-respecting linear extension.
- Each has **no** (i) and no (ii) (Thm 3.1, 2.1\*, 3.1\*, implemented from the doc text), and **has** (iii).
- Every survivor listed is in canonical form.

---

## 3. The step I tried hardest to break: the X-local form of Lemma C (§4.1)

**Claim (EMPIRICAL, n ≤ 10): HOLDS exactly.**
- My generator enumerates Fishburn matrices, with counts 53 … 201 608 = A022493 for n ≤ 10.
- Containment two-separator pairs: 200 at n = 7 and 20 429 at n = 9, matching mg-561a's table. There are 200 975 at n = 10.
- In the region `q, u_s, u_t < 1/3` (`out_xlocal.txt`):

  | n | configurations in the region | twins | non-twin | min over non-twin |
  |---|---|---|---|---|
  | 9 | 20 | 20 | 0 | – |
  | 10 | 362 | 333 | 29 | 49/125 |

- The five tightest n = 10 rows match the author's transcript.

**The mechanism: OVERSTATED** (`out_mech.txt`). The doc checks the tightest case and generalises ("that balance comes from the Swap Identity of the pair (s,t) itself"). Classified by (does `s` dominate `t`, |A(s,t)|, |B(s,t)|, |S(t,s)|), the 29 non-twin cases split as:

| class | count | Cor 1.2 mechanism? |
|---|---|---|
| (True, 0, 1, 0) | 16 | yes |
| (False, 1, 0, 1) | 8 | no: `s, t` nested |
| (False, 0, 2, 1) | 4 | no |
| (False, 1, 0, 2) | 1 | no |

**The reading beyond n = 10: BROKEN.**
- Search: `xclimb.py` hill-climbs over interval orders with n = 11–20 and scores in **canonical form**. The early non-canonical version produced an n = 18 artifact; it is kept as a control in `out_canon_check.txt`.
- Results:
  - n = 11: the best slack is exactly 0, at T11 (180 s).
  - n = 12: 17 distinct failing posets.
  - n = 13: 46.
  - n = 14–20: 39.
- Two witnesses are verified exactly by three independent methods: the ideal DP, the automaton law of the 4-tuple, and brute-force enumeration of all extensions (`out_xfail.txt`):

> **X12** = `[1,1]⁴ [1,2] [1,3] [2,6] [3,4] [3,5] [4,5] [5,6] [6,6]` (canonical, e = 99 360).
> - The step is `a = [3,4] ⊂ a' = [2,6]`, with `S = A(a,a') = {s = [5,6], t = [6,6]} = min Z` and `B = ∅`.
> - `q = 91/276 = 0.3297`, `u_s = 269/828 = 0.3249`, `u_t = 169/828 = 0.2041`: all `< 1/3`.
> - `P[t<s] = 38/115 = 0.3304 < 1/3`: **unbalanced**.
>
> **X14** = `[1,1]² [1,2] [2,6] [3,3] [3,4]² [3,5] [4,7] [5,5] [6,6] [7,7]³` (e = 65 160).
> - The step is `a = [3,3] ⊂ [2,6]`, with `s = [4,7]` and `t = [5,5]` nested.
> - `q = 294/905`, `u_s = 202/905`, `u_t = 57/181`, and `P[s<t] = 60/181`.
>
> Control: the doc's n = 10 tight case evaluates to `w = 49/125`, which is not a failure. CAUGHT.

- X12 is exactly the doc's own tightest n = 10 case `[1,1]³[1,2][1,3][2,6][3,4][4,5][5,6][6,6]` with `[1,1]` and `[3,5]` added. The new `[3,5]` is a **second** below-separator of `(s,t)`: `B(s,t) = {[4,5], [3,5]}`. That disables exactly the single-separator Cor 1.2 balance the doc identifies.

**What this means (PROVEN, by exact computation on a real poset; `out_lcc12.txt`).**
- X12 and X14 are **LCC on X = {a, a', s, t}** in the sense of mg-561a §2.1:
  - every incomparable pair in X is outside `[1/3, 2/3]`;
  - the >2/3 order on X is `a, a', s, t` (resp. `a, a', t, s`);
  - `a, a'` are consecutive in it.
- They are real interval orders. So **every true inequality** (XYZ, FKG, Ahlswede–Daykin, Stanley, Kahn–Saks, or anything else) holds on them together with all counterexample constraints on pairs inside X.
- Hence:

  > **No-go (containment form).** No proof of Lemma C can use only the law of `{a, a', s, t}` and the counterexample hypotheses on pairs inside that set.

- mg-561a's P5 gave the dominance-step version of this no-go. mg-561a §2.1 said "no containment two-separator pair is ever LCC" and the doc says "the local form holds". Both statements are correct as scoped (n ≤ 9 and n ≤ 10). **X12 shows that the scope is essential.**
- X12 and X14 are **not** LCC on `X ∪ Y`: `(a', [3,5])` has law 86/207 in X12, and `(a', [3,4])` has law 329/905 in X14. So any proof must reach at least the common incomparables of `a, a'`.
- This agrees with the doc's own conclusion that "the working unit is not the containment step". It is a stronger form of it: T3 showed that the *certificate families it tried* are not one-step, and X12 shows that *no* X-local argument exists.
- **Bounded range.** X12 has maximum incomparability degree 8, and X14 has 9. Nothing here uses range, and the no-go holds at small range.

---

## 4. K_C (pm-onethird: "verify that K_C is PROVEN")

**Not PROVEN. EMPIRICAL.** The doc says so correctly: it states K_C as a hypothesis of Thm 5.1, labels it EMPIRICAL, and flags that n = 11 outside the staircase family is unsearched.

My checks, as instruments and not a census:
- **22/22 survivors** have (iii) and no (i)/(ii) (`out_kc.txt`).
- **Counterexample search** (`kc.py`, `out_kcsearch_s1{1,2}.txt`):
  - Population: 229 244 + 229 007 distinct canonical staircase-type interval orders with n = 11–14 (a unit staircase plus random intervals of length ≤ 5; the shards may overlap).
  - Method: a DFS over dominance-respecting `L` that prunes on (i), (iii) and local Thm 3.1, then filters complete `L` by 2.1\*/3.1\*.
  - Result: **0** K_C-bad `L`, and no DFS was truncated.
- **Pipeline positive control** (`out_kc_ctl.txt`): with (iii) allowed, the same generator and DFS find 49 `L` on 182 014 posets that avoid (i) and (ii). All 49 contain (iii), so K_C holds on each.
- Not searched: non-staircase shapes; n ≥ 15; exhaustive n = 11 (per the 2026-09-26 directive).

**Relation to §3.** X12 does not touch K_C or Lemma C themselves. It shows that Lemma C, if true, must be proved non-locally. So "prove Lemma C, then add K_C" is now two non-local problems. That is a further reason to prefer LC_k (§6 of the doc), which needs no K_C.

---

## 5. Verdict per claim

| # | claim (doc §) | label in doc | verdict |
|---|---|---|---|
| 1 | Prop 1.1 Conditioned Swap Identity (§1) | PROVEN | **HOLDS** (re-derived; 3 980 exact checks, controls fire) |
| 2 | Prop 1.2 pointwise certificates (§1) | PROVEN | **HOLDS** (`<` can be `≤`) |
| 3 | lift hierarchy / ADJ remark (§1) | – | **HOLDS** (boundary 1/3 case needs the `≤` form) |
| 4 | §2.1 exact 1/75 values | EMPIRICAL exact | **HOLDS** (reproduced, author code) |
| 5 | §2.1 B&B: XYZ exactly leaves 1/75 | EMPIRICAL float | **UNVERIFIABLE** here; moot after row 13 |
| 6 | Prop 2.1 (XYZ wrong way at the step) | PROVEN | **HOLDS** (direction/hypotheses correct; realised by X12) |
| 7 | 14 certificates, 13 survivors refuted (§3.1) | PROVEN (computer) | **HOLDS** (independent exact re-check) |
| 8 | §3.2 11/4 certificate as written | – | **HOLDS** with index orientation; the literal `(c,d)` orientation is INVALID (imprecise prose) |
| 9 | §3.3 locality table; Q12 not certifiable at the step alone | EMPIRICAL float | **HOLDS** (independent LP) |
| 10 | "the working unit is the two-step triple" (§0.3) | EMPIRICAL | **HOLDS** as a statement about the tried families |
| 11 | §4.1 X-local census n ≤ 10 | EMPIRICAL exact | **HOLDS** (exact reproduction) |
| 12 | §4.1 mechanism "balance comes from the pair (s,t)'s Swap Identity" | – | **OVERSTATED** (16/29) |
| 13 | §4.1 reading "local form = separators balanced"; §0.4 "whenever the step looks like a counterexample, s,t are balanced" | – | **BROKEN** at n = 12 (X12), and at n = 14 (X14) |
| 14 | §4.2 identity for `(a',s)` | – | **HOLDS** |
| 15 | §4.3 Conditioned Two-Step Conjecture | CONJECTURED | label correct; evidence Q12 only |
| 16 | Thm 5.1 conditional argument | CONDITIONAL | **HOLDS** |
| 17 | K_C | EMPIRICAL | label correct; **not PROVEN**; my search 0 bad (control fires) |
| 18 | "Lemma C ⟹ 1/3–2/3 is FALSE as stated" (§5) | – | **OVERSTATED**: unproven, not false (vacuously true if 1/3–2/3 holds) |
| 19 | "Without K_C, Lemma C gives exactly Cor 3.2" (§5) | – | **OVERSTATED** (minor): it adds per-(P) kills via (iii), as the next sentence says |
| 20 | LC_k ⟹ 1/3–2/3; k = 0 fails at Q12 (3.125); k = 2 on steps suffices on the 13 | CONJECTURED / EMPIRICAL | **HOLDS** (implication re-derived; 3.125 reproduced; 13 certificates re-checked) |
| 21 | "1/3–2/3 for interval orders remains open" | – | **HOLDS** as far as can be verified; no hidden proof |

---

## 6. What I did NOT do; candidates ruled out

**Not done.**
- No exhaustive n = 11 census of either the X-local form or K_C, per the 2026-09-26 directive. The minimal X-local failure is ≤ 12. At n = 11 the search found none (best slack 0 = T11), but that is not exhaustive.
- The float branch-and-bound (`bnb.py`), the SW3 rows and the greedy deletion filter were not re-run.
- The 1/75 LP values were reproduced only with the author's code.
- No proof of Lemma C, K_C or LC_k was attempted beyond the no-go in §3.
- K_C was searched only on staircase-type shapes.

**Candidates ruled out by this audit.**
- **Any X-local proof of Lemma C**: XYZ, FKG, Ahlswede–Daykin, Stanley, Kahn–Saks and linear identities alike, if they use only `{a, a', s, t}`. The witness is X12, and the verdict is PROVEN by exact computation.
- **"Separator balance" as the reason Lemma C holds**: false at n = 12.

## 7. Files (`code/audit_ksbft_f4f0/`)

See `README.md` there. `run_all.sh` asserts:
- 14/14 certificates, with 6 controls;
- Prop 1.1 with 0 violations and firing controls;
- the `canonical()` control;
- the X-local census numbers for n ≤ 10;
- the two X-local failures, plus the negative control;
- LCC on X for X12 and X14;
- K_C on the 22 survivors, with the Q12 control.

`PROBES=1` re-runs the stochastic searches. `PY_SCIPY` re-runs the float LP.
