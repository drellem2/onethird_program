# KSBFT-T2: the two-separator lemma. The right lemma is not a one-pair lemma: a one-step lemma at a dominance step is impossible (no-go, exact witness at n = 5). What holds is a TWO-STEP lemma (PROVEN, every poset). In it, the reverse-separator terms of two steps sharing an element cancel, and at least 3 uncancelled separators are forced. It kills O9a, O9b and every Claim-K obstruction of the n ≤ 10 census, so every interval order with n ≤ 10 has a probability-free certificate. It first fails at n = 12, where the whole linear calculus of proven facts is still feasible. No proof for interval orders (mg-561a)

Ticket mg-561a. It is gated on mg-5ecf, the audit of mg-afa4 (`docs/AUDIT-mg-afa4.md`).
- The audit found that every PROVEN statement of `docs/KSBFT-T-interval-orders.md` HOLDS, and that every census count reproduces. Nothing I use is broken.
- The one OVERSTATED item ("equivalent" in mg-afa4 §0.2) is not used here.
- From mg-afa4 I use:
  - Thm 2.1: the 2/3-relation is a linear extension `L`, and there is a separator injection;
  - Prop 3.1: `|S| = A_i + B_i`;
  - Cor 3.2: the dominance/containment case list;
  - the O9a/O9b data.
- From mg-ce69 (audit mg-6e7c HOLDS) I use the Swap Ladder Thm 1.4 and the Doubling Lemma 1.5.

**Instrument.** `code/ksbft_t2_two_separator_561a/` (Python, exact `Fraction`s). `sh run_all.sh` regenerates every transcript and asserts every headline and every control. It takes about 6 min at 3 processes.
- Generation and pair laws are imported read-only from the audited `iolib.py`.
- Separators come from the cover relation.
- Joint events (`Λ₁`, `Λ₂`, one or both separators between) come from an automaton DP over the ideal lattice.
- Per the ticket, computation is used **only as an instrument**: to probe candidate lemmas, extract LP certificates, and search for counterexamples to candidates. The n ≤ 10 enumerations are the populations of mg-afa4, on which each candidate is tested; they are not a case census of 1/3–2/3. The one stochastic search (`csearch.py`) was a counterexample search for a candidate lemma.

**Labels.**
- **PROVEN**: proof in this file.
- **EMPIRICAL**: exact arithmetic on a stated finite population.
- **CONJECTURED**: a guess.

**Notation.**
- `L` is the 2/3-order of a putative counterexample (mg-afa4 Thm 2.1(a)).
- For an ordered incomparable pair `(a,a')`:
  - `A(a,a') = {z : a ⋖ z, z ∥ a'}` (above-separators);
  - `B(a,a') = {w : w ⋖ a', w ∥ a}` (below-separators);
  - `S = A ∪ B`.
- `Λ₁(a,a')` = {`a` before `a'`, no element of `S(a,a')` strictly between}. `Λ₂(a,a')` = {`a` before `a'`, some element of `S(a,a')` strictly between}.
- For `z ∈ A(a,a')`, the event "z between" equals `{z < a'}`. For `w ∈ B(a,a')`, it equals `{a < w}`.
- Interval orders use the canonical representation (mg-afa4 Conventions).
- `a` **dominates** `a'` means `l(a) ≤ l(a')` and `r(a) ≤ r(a')`. In a general poset it means `down(a) ⊆ down(a')` and `up(a) ⊇ up(a')`.
- A **containment step** is a step whose two intervals are strictly nested.

---

## 0. Verdict

1. **Task 1: the precise statement.** "An `L`-consecutive pair with exactly two separators is impossible" is the naive two-separator lemma. For a single pair it is **false as a local statement** at dominance steps, and dominance steps are most two-separator steps.
   - **No-go (EMPIRICAL, exact witness; §2.1).** The 5-element path semiorder `P5 = [1,1][1,2][2,2][2,3][3,3]` has the pair `(a,a') = ([1,2],[2,3])`, with `S = {[1,1] below, [3,3] above}`. Every pair law among these four elements satisfies every constraint a counterexample's `L` imposes: 8/11, 8/11, 8/11 on the three `L`-ordered incomparable pairs.
   - So no inequality among the joint law of `{a, a', s, t}` can refute a two-separator step. Adding the common incomparables of `a` and `a'` still leaves 186 survivors at n = 9. Adding all incomparables of the separators leaves 8 survivors at n = 9 (§2.1).
   - What *can* be true: (i) a one-step lemma at **containment** steps only (Lemma C, §2.3); (ii) a **two-step** lemma (Thm 3.1, §3).
2. **The exact identity underneath (Thm 1.1, PROVEN, every poset).**
   `P(Λ₂(a,a')) − P(Λ₂(a',a)) = P[a<a'] − P[a'<a]`.
   - Brightwell's injection (mg-afa4 Thm 2.1(b)) is this identity with the non-negative reverse term dropped.
   - At a dominance step the reverse term vanishes, and the identity is exact: `P(Λ₂) = 1 − 2P[a'<a]` (Cor 1.2).
   - At a containment step the reverse term is positive. That is exactly the slack the two-step lemma recovers.
3. **Task 2: the lemma that works (Thm 3.1, PROVEN, every poset).** Let `a ≺ c ≺ b` be `L`-consecutive, with `a ∥ c` and `c ∥ b`. Put
   `k = |A(a,c)∖A(b,c)| + |B(a,c)| + |B(c,b)∖B(c,a)| + |A(c,b)|`.
   Then **`k ≥ 3`**.
   - Each step alone needs only ≥ 2 separators (Thm 2.1).
   - The two identities sum to `2 − 2q₁ − 2q₂ > 2/3`. The separators shared with the reverse pairs are absorbed by the reverse terms.
   - The lemma was found as the **irreducible infeasible subsystem** of an LP of proven facts, on O9a. Around the long interval `c = [2,6]`, the two containment steps' reverse separators `[1,2]` and `[6,6]` cancel.
   - A non-local form (3.1*) drops consecutiveness. It needs only that every counted event is an `L`-inversion.
4. **Tested first on O9a and O9b, as the ticket asks (EMPIRICAL, exact).**
   - Thm 3.1 kills the bad `L` of O9a (k = 2 at `[3,4] ≺ [2,6] ≺ [4,5]`) and of O9b (k = 2 at the same triple).
   - On **all 29 bad dominance-`L` of the 24 posets at n = 10**, 28 fall to Thm 3.1 and 1 to 3.1*.
   - Hence **every interval order with n ≤ 10 has a probability-free certificate of 1/3–2/3**: Thm 2.1 + Thm 3.1 + the exhaustive enumeration. (It was known to n = 14 anyway; the point is that the Brightwell route now reaches n ≤ 10 instead of n ≤ 8.)
   - In the audit's staircase family (n = 10–13), 2 505 of 2 527 bad `L` fall to Thm 2.1*/3.1/3.1*, and **22 `L` on 21 posets survive** (n = 12, 13).
5. **Where it stops (EMPIRICAL).** On the 22 survivors I ran the full **linear calculus** of proven facts: the Swap Identity on *every* pair with union bounds and exact inclusion–exclusion, the Swap Ladder, Doubling, and Prop 2.2.
   - It refutes 9 of them. **13 stay LP-feasible**, with a strictly positive margin.
   - The smallest is **Q12** = `[1,1][1,2][2,3][2,5][3,4][4,5][5,6][5,8][6,7][7,8][8,9][9,9]` with the staircase `L`, at LP margin `ε* = 1/48`.
   - So on Q12 no linear combination of these lemmas yields a contradiction. A proof needs a **non-linear (correlation) input** or a new injection. This is the minimal known configuration where the two-step lemma fails.
6. **Lemma C (CONJECTURED; the strongest candidate).** "In a counterexample, no `L`-consecutive containment step has exactly 2 separators."
   - As a rule it kills **every** known obstruction: 2/2 at n = 9, 24/24 at n = 10, 547/547 staircase posets, including all 13 LP survivors.
   - Its local form holds for n ≤ 9 and reaches the boundary exactly at n = 11 (T11, a tie `P[a<a'] = 2/3`, `P[s<a'] = 1/3`).
   - I prove it in special cases: Prop 2.3 (`Z = S` forces `4/15 < P[a'<a] < 1/3` and constrains the position laws) and Prop 2.4 (a Doubling identity kills it outright).
   - The general case is open.
7. **Task 3: general posets (EMPIRICAL).** Thms 1.1, 2.1, 3.1 and 3.1* hold for every poset. But on random general posets (n = 7–11, 19 996 posets), 23 bad `L` on 8 posets survive them, the smallest at **n = 9**. Their steps are almost all **2+2-trapped** (neither dominance nor nesting), with one above- and one below-separator.
   - For a trapped step the reverse separators of the neighbouring steps are of the wrong type to cancel: an above-separator event `{z < c}` can only cancel against another above-type event at the same `c`.
   - So the count that breaks in general is exactly the one that 2+2-freeness removes. The interval-order route does not transfer.
8. **Not a proof.** The interval-order case of 1/3–2/3 remains open, as far as can be verified (mg-afa4, audit mg-5ecf).

---

## 1. The Swap Identity (PROVEN, every finite poset)

**Theorem 1.1 (Swap Identity).** For every incomparable pair `a, a'` of any finite poset,
`|Λ₁(a,a')| = |Λ₁(a',a)|`, and hence
`P(Λ₂(a,a')) − P(Λ₂(a',a)) = P[a<a'] − P[a'<a]`.

*Proof.* Let `V` be the set of linear extensions in which exchanging the positions of `a` and `a'` again gives a linear extension. The exchange `τ` is an involution of `V`, and it swaps `V ∩ {a before a'}` with `V ∩ {a' before a}`.

Claim: `V ∩ {a before a'} = Λ₁(a,a')`.
- If a separator lies between them, the exchange is invalid. An above-separator `z > a` would precede `a`; a below-separator `w < a'` would follow `a'`.
- Conversely, suppose no separator lies between. mg-afa4 Thm 2.1(b) (audit: HOLDS) shows that nothing between is above `a` or below `a'`: a cover `a ⋖ c ≤ w` of an offending `w` would be a separator between them. So the exchange is valid.

Symmetrically, `V ∩ {a' before a} = Λ₁(a',a)`. Therefore `|Λ₁(a,a')| = |Λ₁(a',a)|`, and `P(Λ₂(a,a')) = P[a<a'] − P(Λ₁(a,a'))`. □

**Corollary 1.2 (dominance steps are exact).** If `a` dominates `a'` (`down(a) ⊆ down(a')`, `up(a) ⊇ up(a')`), then `S(a',a) = ∅`. So
`P(Λ₂(a,a')) = 2P[a<a'] − 1` exactly. (Zaguia's Lemma 7 swap is the case `Λ₂ = ∅`.)

*Proof.* `a' ⋖ z` implies `z ∈ up(a') ⊆ up(a)`, so `z` is not incomparable to `a`. Dually for `z ⋖ a`. □

**Corollary 1.3 (Brightwell = identity minus a term).** `P(Λ₂(a,a')) ≥ 2P[a<a'] − 1`, with equality iff `P(Λ₂(a',a)) = 0`. For a strict containment `a ⊂ a'` in an interval order, `S(a',a) = max{w : l(a') ≤ r(w) < l(a)} ≠ ∅`: the canonical point `l(a) − 1` is a right endpoint. So Brightwell's inequality is **lossy exactly at containment steps**.

**Check (EMPIRICAL, `out_verify.txt`).**
- Thm 1.1 holds on every ordered incomparable pair of every interval order with n ≤ 8 (123 002 pairs at n = 8), and of 3 000 random general posets with n = 5–8: 0 violations.
- **Control:** with above-separators only, the identity fails on 73 374 pairs at n = 8.
- Cor 1.2: 0 violations.

In every locally counterexample-compatible two-separator configuration (§2.1, 14 042 at n = 9), `|Λ₁| = |Λ₃|` held exactly. That is Cor 1.2: all of them are dominance steps.

---

## 2. The one-step two-separator problem

### 2.1 No local lemma exists at dominance steps (no-go; EMPIRICAL, exact)

Take an ordered incomparable pair with `S = {s,t}`, and let `X = {a, a'} ∪ S`. Call it **locally counterexample-compatible (LCC)** if:
- every incomparable pair in `X` has law outside `[1/3, 2/3]`;
- `P[a<a'] > 2/3`;
- no element of `X` sits between `a` and `a'` in the induced 2/3-order.

These are all the constraints a counterexample's `L` places on `X`. If an LCC configuration occurs **in a real poset**, then the true joint law of the order on `X` satisfies every one of those constraints, and every true inequality. So no inequality about that joint law, whatever it is, can refute an `L`-consecutive two-separator step.

`out_localcc.txt`, `out_enlarge.txt`, `out_shape.txt`: counts of two-separator ordered pairs, by type, over all interval orders.

| n | AA (dom) | AB (dom) | BB (dom) | AA/BB (containment) | LCC on X | LCC on X ∪ Y | LCC on X ∪ Y ∪ Inc(S) | LCC on all of P |
|---|---|---|---|---|---|---|---|---|
| 5 | 11 | 12 | 11 | 1 / 1 | 1 (AB) | 0 | 0 | 0 |
| 7 | 660 | 781 | 660 | 200 / 200 | 228 | 8 | 0 | 0 |
| 9 | 36 436 | 44 873 | 36 436 | 20 429 / 20 429 | 14 042 | 456 | 8 (AB) | 0 |

Here `Y` is the set of common incomparables of `a` and `a'`, the only elements that can sit between them in `Λ₁`.
- The first LCC configuration is `P5`: `a = [1,2]`, `a' = [2,3]`, `w = [1,1]`, `s = [3,3]`. The three `L`-ordered laws are all 8/11, and `|Λ₁| = |Λ₃| = 3`, `|Λ₂| = 5` of 11.
- The last column must be 0 (1/3–2/3 holds for these n), and it is. It is the sanity control.

**Reading.**
- **Every LCC configuration is a dominance step** (all 14 042 at n = 9). **No containment two-separator pair is ever LCC** (0 of 2 689 with `P[a<a'] > 2/3` at n = 9).
- So a *one-step* two-separator lemma can only live at containment steps. At dominance steps the only true one-step statement is the identity `P(Λ₂) = 1 − 2q`, with `q = P[a'<a]`. It is satisfiable with all laws unbalanced.
- By type, the identity reads:
  - AA: `P[s<a' or t<a'] = 1 − 2q`;
  - AB: `P[a<w or s<a'] = 1 − 2q`, where 2+2-freeness forces `w < s`, making `{w, a, a', s}` an N;
  - BB: dual of AA.

### 2.2 Containment steps: the split injection (PROVEN)

Let `a ⊂ a'` strictly (`l(a') < l(a) ≤ r(a) < r(a')`), with `a` first. Then `B(a,a') = ∅` (Cor 3.2 of mg-afa4), and `S = A(a,a') = min Z`, where `Z = up(a) ∖ up(a') = {z : r(a) < l(z) ≤ r(a')}`.

**Proposition 2.2.** Suppose `Z = S = {s,t}`. Let `Λ₂^(k)` be the event "`a` before `a'` with exactly `k` of `s,t` between". Then `|Λ₂^(1)| ≤ |Λ₁|` and `|Λ₂^(2)| ≤ |Λ₁|`.

*Proof.* Let `f` be the first of `s,t` after `a`, and exchange `f` with `a'`.
- `a'` moves earlier. Its down-set `down(a') ⊆ down(a)` precedes `a`, which is before `f`'s slot.
- `f` moves later. An element of `up(f)` strictly between would be above `a` and not above `a'`, so it would lie in `Z ∖ {f}`, which is the other separator. But the other separator is incomparable to `f` (both are minimal in `Z`).

So the image is a linear extension. The elements between `a` and the new `a'` are those that were between `a` and `f`, so the image lies in `Λ₁`.
- From `Λ₂^(1)`, `f` becomes the **first** separator after `a'`.
- From `Λ₂^(2)`, `f` becomes the **second** separator after `a'`: the other one is now between them.

Either way `f` is recoverable, so each restriction is injective. □

**Check.** 0 violations on 1 490 `Z = S` pairs at n = 8. **Control:** when `Z ≠ S` the inequalities fail on 537 of 577 pairs, so the hypothesis is needed (`out_verify.txt`).

**Proposition 2.3 (position-law constraints; PROVEN).** In a counterexample, let the step `a ≺ a'` be `L`-consecutive with `a ⊂ a'` and `Z = S = {s,t}`. Put:
- `q = P[a'<a]`;
- `u_s = P[s<a']`, `u_t = P[t<a']`;
- `β = P[s<a' and t<a']`;
- `γ = P(Λ₂(a',a)) ≥ 0`.

Then
`β ≥ 1 − 3q + 2γ`, `u_s + u_t ≥ 2 − 5q + 3γ`, and hence `4/15 < q < 1/3`, with `u_s, u_t > 5/3 − 5q`.

*Proof.*
- Thm 1.1 gives `P(Λ₂) = 1 − 2q + γ`, so `P(Λ₁) = q − γ`.
- Prop 2.2 gives `P(Λ₂) = P(Λ₂^(1)) + β ≤ q − γ + β`.
- Inclusion–exclusion gives `P(Λ₂) = u_s + u_t − β`.
- Since `s, t ≻ a'` (both are above `a`), `u_s, u_t < 1/3`. Then `2 − 5q < 2/3`. □

This is as far as one step goes. O9a's containment steps have `Z = S`, so Prop 2.3 applies there, but it does not contradict them.

### 2.3 Lemma C: the local form, and a Doubling kill

**Lemma C (CONJECTURED).** In a counterexample, no `L`-consecutive containment step has exactly two separators.

**Rule test (EMPIRICAL, `out_kprime.txt`).** Encode Lemma C as a rule forbidding such steps in a dominance-respecting `L`. Every Claim-K obstruction is killed:

| population | K-bad posets (control: reproduces mg-afa4 and the audit) | surviving Lemma C |
|---|---|---|
| census n = 9 | 2 | **0** |
| census n = 10 | 24 | **0** |
| staircase + 1–3 long intervals, n = 10–13 | 547 | **0** |

The dominance-only variants do not suffice: "forbid dominance-AB" leaves 4 staircase survivors, and "forbid dominance-AA/BB" leaves 13.

**Local form.** The local form says a containment two-separator configuration is never LCC. It holds for n ≤ 9, with the best slack −0.095, −0.067, −0.028 at n = 7, 8, 9 (`out_contprobe.txt`).
- A targeted hill-climb (`csearch.py`, a counterexample search for this candidate) reached slack **exactly 0** at n = 11:
  **T11** = `[1,1]² [1,2] [2,4] [3,3] [3,5]² [4,4] [4,5] [5,5]²`, with `a = [3,3]`, `a' = [2,4]`, `s = [4,4]`, `t = [4,5]`, `P[a<a'] = 2/3`, `P[s<a'] = 1/3`, `P[t<a'] = 1/5`, `P[s<t] = 43/60`.
- Varying every multiplicity up to n = 14 (`out_tiefam.txt`, 435 posets) never makes the slack positive.
- The reason is an identity, `P[s<a'] = P[a<a']/2`, visible in every row of `out_tiefam.txt` (656/983 vs 328/983, 432/647 vs 216/647, …):

**Proposition 2.4 (PROVEN; the dual Swap Ladder at a containment step).** Let `a ⊂ a'` strictly with `a` first, let `s ∈ A(a,a')` with `r(s) ≤ r(a')`, and let `D_s = {z : l(a') ≤ r(z) < l(s)}`.
- `a` is a maximal element of `D_s`. If `z > a` were in `D_s`, then `z ∈ Z` and `z < s`, contradicting the minimality of `s`.
- If `a` is the **unique** maximal element of `D_s`, then `P[a<a'] ≤ 2P[s<a']`.

So in a counterexample such a step is impossible, **whatever `|S|` is**: `P[a<a'] > 2/3` forces `P[s<a'] > 1/3`, while `s ≻ a'`.

*Proof.* `up(a') ⊆ up(s)` since `r(s) ≤ r(a')`. This is the dual H1 of mg-ce69 Thm 1.4 for the pivot `x = a'` and `b_0 = s`. The chain top of `↓s ∖ ↓a'` is `s > a`, since `a` is the unique maximal element of `D_s = ↓s ∖ ↓a' ∖ {s}`. The dual ladder gives:
- `t₀ = P[s < a']`;
- `t₁ = P[a < a' < s] ≤ t₀`;
- `P[a < a'] = t₀ + t₁ ≤ 2t₀`. □

T11 is the equality case. Unique maximality needs `l(s) = r(a) + 1` and `a` to be the only interval ending in `[l(a), r(a)]`, so Prop 2.4 covers a thin slice. O9a's step (`s = [4,5]`, `D_s ∋ [1,2], [2,3]` incomparable) is not in it.

---

## 3. The two-step lemma (answers task 2)

### 3.1 How it was found

`lpcheck.py` builds, for a pair (P, L), the LP of proven linear facts that a counterexample with 2/3-order `L` must satisfy. Its variables are the inversion probabilities `x_{uv} = P[v before u] < 1/3` (`u ≺ v`), `B(a,a') = P(Λ₂(a,a'))` for **every** ordered incomparable pair (not only consecutive ones), and the joint variables. Its constraints are:
- Thm 1.1;
- `B ≤` union of separator events, and `B ≥` each separator event;
- exact inclusion–exclusion when `|S| = 2`;
- `B = 0` when `S = ∅`;
- optionally the Swap Ladder, Doubling and Prop 2.2.

It maximises the margin `ε` in `x ≤ 1/3 − ε`.

For O9a and O9b, T1 alone gives `ε* = 0`, which is a refutation. A deletion filter (`iis.py`) extracts a 17-row irreducible infeasible subsystem, `out_iis_O9a.txt`. In words (O9a, `c = [2,6]`, with `L`-neighbours `a = [3,4] ≺ c ≺ b = [4,5]`):
- `A([3,4],c) = {[5,6], [6,6]}`, while the reverse pair `(c,[3,4])` has the below-separator `[1,2]`. So the identity reads
  `P[[5,6]<c] + P[[6,6]<c] ≥ P(Λ₂([3,4],c)) = 1 − 2x₂ + P(Λ₂(c,[3,4])) ≥ 1 − 2x₂ + P[c<[1,2]]`.
- `B(c,[4,5]) = {[1,2], [2,3]}`, while the reverse pair `([4,5],c)` has the above-separator `[6,6]`. So
  `P[c<[1,2]] + P[c<[2,3]] ≥ 1 − 2x₃ + P[[6,6]<c]`.
- Adding the two, `[1,2]` and `[6,6]` cancel:
  `P[[5,6]<c] + P[c<[2,3]] ≥ 2 − 2x₂ − 2x₃ > 2/3`.
  But both left-hand terms are `L`-inversions, each `< 1/3`. Contradiction.

O9b gives the same certificate at `c = [2,6]` (`out_iis_O9b.txt`).

This is candidate 3 of mg-afa4 §6 ("use more than one step"). The mechanism is the *reverse* term of Thm 1.1, which Brightwell's inequality throws away.

### 3.2 The lemma

**Theorem 3.1 (Two-Step Lemma, PROVEN, every finite poset).** Suppose `P` has no balanced pair, and let `L` be its 2/3-order. Let `a ≺ c ≺ b` be `L`-consecutive with `a ∥ c` and `c ∥ b`, and put `q₁ = P[c<a]` and `q₂ = P[b<c]`. Then
`Σ_{z ∈ A(a,c)∖A(b,c)} P[z<c] + Σ_{w ∈ B(a,c)} P[a<w] + Σ_{w ∈ B(c,b)∖B(c,a)} P[c<w] + Σ_{z ∈ A(c,b)} P[z<b] ≥ 2 − 2q₁ − 2q₂ > 2/3`.

Each summand is the probability of an `L`-inversion, hence `< 1/3`, so the number of summands satisfies
**`k(a,c,b) = |A(a,c)∖A(b,c)| + |B(a,c)| + |B(c,b)∖B(c,a)| + |A(c,b)| ≥ 3`.**

*Proof.*
- Thm 1.1 for `(a,c)` and for `(c,b)`, added, gives
  `P(Λ₂(a,c)) + P(Λ₂(c,b)) = (1 − 2q₁) + (1 − 2q₂) + P(Λ₂(c,a)) + P(Λ₂(b,c))`.
- Upper bounds:
  - `P(Λ₂(a,c)) ≤ P(∪_{z ∈ A(a,c) ∩ A(b,c)} {z<c}) + Σ_{A(a,c)∖A(b,c)} P[z<c] + Σ_{B(a,c)} P[a<w]`;
  - `P(Λ₂(c,b)) ≤ P(∪_{w ∈ B(c,b) ∩ B(c,a)} {c<w}) + Σ_{B(c,b)∖B(c,a)} P[c<w] + Σ_{A(c,b)} P[z<b]`.
- Lower bounds:
  - `{z<c} ⊆ Λ₂(b,c)` for `z ∈ A(b,c)` (`b ⋖ z` forces `b<z<c`), so the first union is at most `P(Λ₂(b,c))`;
  - `{c<w} ⊆ Λ₂(c,a)` for `w ∈ B(c,a)`, so the second union is at most `P(Λ₂(c,a))`.
- Substituting, the reverse terms cancel.
- Inversions:
  - `z ∈ A(a,c)` is above `a`, so `a ≺ z`, and by consecutiveness `c ≺ z`;
  - `w ∈ B(a,c)` is below `c`, so `w ≺ a`;
  - `w ∈ B(c,b)` gives `w ≺ c`;
  - `z ∈ A(c,b)` gives `z ≻ b`.
- Finally `q₁, q₂ < 1/3`. □

**Remarks.**
- With both steps dominance steps, both reverse sets are empty. Then `k = |S(a,c)| + |S(c,b)| ≥ 4`, and Thm 3.1 adds nothing. **Thm 3.1 has content only where a containment (or nested) step supplies a reverse separator.** The cancellations are between `A(a,c)` and `A(b,c)` (above `c`), and between `B(c,b)` and `B(c,a)` (below `c`).
- Summing Thm 1.1 over all steps of `L`, cancellations can only happen between the two steps that share a middle element: event types `{z<c}` / `{c<w}` must match at the same `c`. So the two-step form is the natural unit, and longer chains only chain it.

**Theorem 3.1\* and 2.1\* (non-local forms, PROVEN by the same proofs).**
- Consecutiveness was used only to make the counted events `L`-inversions. So Thm 3.1 holds for any `a ≺ c ≺ b` (pairs incomparable) whose counted separators all lie `L`-outside:
  - `z ∈ A(a,c)∖A(b,c)` after `c`;
  - `w ∈ B(a,c)` before `a`;
  - `w ∈ B(c,b)∖B(c,a)` before `c`;
  - `z ∈ A(c,b)` after `b`.
- Likewise mg-afa4 Thm 2.1 holds for any `a ≺ a'` whose separators are all `L`-outside (2.1\*).

**Check (EMPIRICAL, `out_verify3.txt`).** The unconditional inequality `(2P[a<c]−1) + (2P[c<b]−1) ≤ RHS` holds on every triple of every interval order with n ≤ 8 (363 324 triples at n = 8) and of 2 000 random general posets: 0 violations. **Control:** over-cancelling (dropping all of `A(a,c)`) fails on 62 033 triples at n = 8.

### 3.3 Results on the obstructions (EMPIRICAL, exact; `out_kts.txt`, `out_kstar.txt`)

Every dominance-respecting bad `L` was enumerated, not just one per poset.

| population | bad `L` (every step `|S| ≥ 2`) | killed by Thm 3.1 | by 2.1\* | by 3.1\* | survive |
|---|---|---|---|---|---|
| O9a, O9b (census n = 9) | 2 | 2 | – | – | **0** |
| census n = 10 (24 posets) | 29 | 28 | 0 | 1 | **0** |
| staircase + 1–3 long, n = 10–13 (547 posets) | 2 527 | 2 374 | 38 | 93 | **22** (21 posets) |

The single 3.1\* kill at n = 10 is `[1,1][1,2][1,6][2,3][2,7][3,4][4,5][5,6][6,7][7,7]`, with `L = … [3,4] [1,6] [2,7] [4,5] …`. The certificate (`out_iis_S10.txt`) is the O9a pattern at `c = [2,7]` with the non-adjacent `a = [3,4]`.

**Corollary 3.2 (PROVEN, computer-assisted).** Every interval order with n ≤ 10 satisfies 1/3–2/3 by Thm 2.1 + Thm 3.1/3.1\* alone, with no probabilities computed. The proof consists of those theorems plus the exhaustive `L`-enumeration of `kstar.py` over the certified populations (n ≤ 8 by mg-afa4's K census; n = 9, 10 here). Novel only as a *method* result: the case is known to n = 14 (Gupta 2026).

---

## 4. Where the lemma stops: the minimal configuration (EMPIRICAL)

`lpsurv.py` runs the LP of §3.1 on the 22 surviving `(P, L)` (`out_lpsurv.txt`):

| tool set | refuted |
|---|---|
| T1 (Swap Identity on all pairs + union / inclusion–exclusion) | 2 / 22 |
| T1 + Swap Ladder + Doubling (both directions) | 2 / 22 |
| T1 + T2 + Prop 2.2 | 9 / 22 |

**13 stay feasible with `ε* > 0`.** The smallest (n = 12) is:
- **Q12** = `[1,1][1,2][2,3][2,5][3,4][4,5][5,6][5,8][6,7][7,8][8,9][9,9]`, `L` = `[1,1][1,2][2,3][3,4][2,5][4,5][5,6][5,8][6,7][7,8][8,9][9,9]`: `ε* = 1/21` (T1), `1/48` (all tools);
- the second n = 12 survivor, `[1,1][1,2][1,5][2,3][2,7][3,4][4,5][5,6][5,8][6,7][7,8][8,8]`: `ε* = 1/57`, then `1/102`.

**Meaning.** On Q12 there is an assignment of all pair laws and all `Λ₂` values that satisfies every proven linear fact used here, with every `L`-inversion `≤ 1/3 − 1/48`. So no linear combination of Thm 1.1, Thm 2.1, Thm 3.1, the Swap Ladder, Doubling and Prop 2.2 can refute Q12's `L`.

**Shape.**
- Q12 is a unit staircase with two long intervals `[2,5]` and `[5,8]` that touch at the point 5. Each is placed just after the staircase interval it contains: `[3,4] ≺ [2,5] ≺ [4,5]` and `[5,6] ≺ [5,8] ≺ [6,7]`.
- Around each long interval, one step is a containment step and the other is a **dominance** step (`[2,5]` dominates `[4,5]`, and `[5,6]` dominates `[5,8]`). The dominance step has no reverse term (Cor 1.2), so only one cancellation happens, and the centre triples have `k = 3` exactly. Every other triple has `k = 4`. (Computed from the step table; O9a/O9b differ in having containment on **both** sides of `c`.)
- Lemma C *does* kill Q12: it has a containment step with exactly two separators. It remains the natural next target, and Q12 is its first test case beyond O9a/O9b.

**What would finish it (CONJECTURED directions).**
1. **Prove Lemma C.** Prop 2.3 already confines a counterexample step to `4/15 < q < 1/3` with `P[s<a', t<a'] ≥ 1 − 3q`. A non-linear input on the pair of events `{s<a'}`, `{t<a'}` could close it. That would be a negative-correlation-type bound, or a Stanley/Kahn–Saks log-concavity statement on the position of `a'` relative to `s` and `t`. (XYZ goes the wrong way: it makes them positively correlated.)
2. **A three-step lemma** that chains two two-step cancellations through a dominance step. On Q12 the LP says it cannot be linear in the present variables. It would need a joint variable over two steps' events (the LP has joint variables only within one pair).

---

## 5. Task 3: general posets (EMPIRICAL; `out_general.txt`, `out_kstar_gen.txt`)

Thms 1.1, 2.1, 3.1, 2.1\* and 3.1\* are proven for every poset. On 19 996 random non-chain general posets (n = 7–11):
- 153 have a Claim-K-bad dominance-respecting `L`;
- of their 448 bad `L`, 178 fall to Thm 3.1 and 247 to 2.1\*;
- **23 `L` on 8 posets survive**, the smallest at **n = 9** (e.g. covers `{0<2, 1<3, 1<4, 2<6, 3<5, 3<6, 4<7, 5<8, 6<7}`, `L = 1 0 3 2 4 5 6 8 7`).

Its steps are (class, |A|, |B|):
`(TRAP,2,0) (TRAP,1,1) (TRAP,1,1) (TRAP,1,1) (TRAP,1,1) (TRAP,1,1) (TRAP,1,1) (TRAP,0,2)`.
TRAP is a 2+2-trapped step, neither dominance nor nesting.

**What breaks.** A trapped `AB` step has reverse separators of both types. An above-type reverse event `{z<c}` cancels only against an above-separator of the *previous* step at the same `c`. A chain of `(1,1)` trapped steps has exactly one of each per step, so no triple reaches `k ≤ 2`. In interval orders trapped steps do not exist (mg-afa4 Lemma 1.1), and an AB step is always a dominance step (mg-afa4 Cor 3.2). This is why the interval-order reduction reaches n ≥ 12, while the general one fails at n = 9 in a random sample.

Lemma C's general form ("nested steps with |S| = 2") leaves 130 of these posets alive (`out_general.txt`, rule KC). Forbidding every two-separator step (KCT/KALL) leaves 0 non-chain survivors. So a general proof along these lines needs a two-separator lemma for **trapped** steps too. §2.1's no-go shows it cannot be local.

Caveat: random general posets almost all contain 2+2, so "the survivors contain 2+2" carries no information. The informative fact is the step classes.

---

## 6. Relation to Gaetz–Gao (pm-onethird's input)

The audit mg-5ecf (§1.3) shows that type-A generalised semiorders are exactly semiorders, and that Gaetz–Gao's Lemma 4.6 is Claim K for the natural labelling. In a semiorder, Prop 2.4 of mg-afa4 gives the prefix property, and Brightwell's count finds a step with ≤ 1 separator. Gaetz–Gao therefore **never meet the two-separator situation**, and their technique has nothing to offer past it (I did not re-read their paper; this follows from the audited type-A = semiorder identification).

Thm 3.1 is exactly the extra ingredient their framework would need outside type A (or outside semiorders): the reverse-separator term of the Swap Identity.

---

## 7. What I did NOT do, and candidates ruled out

**Not done.**
- No proof of 1/3–2/3 for interval orders. No proof of Lemma C beyond Props 2.3/2.4.
- No non-linear tool in the LP. XYZ, Stanley log-concavity and cross-product-type inequalities are not in the model, so "LP-feasible" is a statement about the linear calculus only.
- Did not extend any census. The census populations are mg-afa4's (n ≤ 10). The staircase family is the audit's. Random general posets are a labelled random sample, not a census.
- Did not search for further `L`-survivors outside the staircase family at n ≥ 11. Nothing is claimed about n = 11 interval orders beyond the staircase family (which has no n = 11 survivor).
- Did not read Gaetz–Gao myself (§6 rests on the audit).
- `csearch.py` is stochastic. Its transcripts s1–s3 predate the T11 seed (s11–s13 postdate it). T11 itself is re-derived deterministically by `tiefam.py`.

**Candidates ruled out** (each as a one-step lemma for two-separator steps).

| candidate | fate |
|---|---|
| any inequality in the joint law of `{a, a', s, t}` | **impossible** (P5, n = 5; §2.1) |
| … of `X ∪ Y` (common incomparables) | impossible (first at n = 6: the path semiorder `[1,1][1,2][2,3][3,4][4,5][5,5]`) |
| … of `X ∪ Y ∪ Inc(S)` | impossible (8 AB configurations at n = 9) |
| "forbid dominance-AB two-separator steps" (as a rule) | leaves 4 staircase obstructions |
| "forbid dominance-AA/BB two-separator steps" | leaves 13 |
| local Lemma C via `max(u_s,u_t) ≥ q`, `≥ 2q`, `≥ 1/3` given `q < 1/3` | fail (15 903, 19 864, 20 at n = 9; `out_contprobe.txt`) |
| the two-step lemma alone (Thm 3.1/3.1\*) | holds to n ≤ 10; fails at n = 12 (Q12), even with the full linear calculus |

---

## 8. Files (`code/ksbft_t2_two_separator_561a/`)

| file | content | output |
|---|---|---|
| `t2lib.py` | typed separators; automaton DP for joint events | — |
| `verify.py` | Thm 1.1, Cor 1.2, Prop 2.2 with controls | `out_verify.txt` |
| `verify3.py` | Thm 3.1 inequality with control | `out_verify3.txt` |
| `localcc.py`, `enlarge.py`, `shape.py` | §2.1 no-go | `out_localcc.txt`, `out_enlarge.txt`, `out_shape.txt` |
| `contprobe.py`, `csearch.py`, `tiefam.py` | §2.3 local Lemma C, T11, Prop 2.4 equality | `out_contprobe.txt`, `out_csearch_s*.txt`, `out_tiefam.txt` |
| `kprime.py` | step rules incl. Lemma C vs all obstructions | `out_kprime.txt` |
| `kts.py`, `kstar.py` | Thm 3.1, 2.1\*, 3.1\* vs all bad `L` | `out_kts.txt`, `out_kstar.txt` |
| `general.py`, `kstar_gen.py` | §5 general posets | `out_general.txt`, `out_kstar_gen.txt` |
| `xlp.py` | exact two-phase simplex (Fractions) | — |
| `lpcheck.py`, `iis.py`, `lpsurv.py` | LP of proven linear facts, certificates, survivors | `out_lpcheck.txt`, `out_iis_*.txt`, `out_lpsurv.txt` |
| `run_all.sh` | regenerates everything and asserts every headline and control | — |
