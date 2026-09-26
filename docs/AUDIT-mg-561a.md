# AUDIT of mg-561a (KSBFT-T2, the two-separator lemma): no proof of 1/3–2/3 for interval orders is claimed and none is hidden; every PROVEN statement HOLDS on re-derivation and on exact tests with firing controls; every census number I re-ran reproduces exactly with independent code (O9a, O9b, the n = 10 set, the §2.1 no-go table); two wordings are OVERSTATED ("first fails at n = 12"; "a one-step lemma can only live at containment steps"), one is speculative (§6 "exactly the extra ingredient")

`mg-6c30`, 2026-09-26. The subject is `docs/KSBFT-T2-two-separator.md` (commit `f7edeb9`) and `code/ksbft_t2_two_separator_561a/`. I am not its author and started from a fresh context.

**Instrument:** `code/audit_ksbft_6c30/` (`sh run_all.sh`, about 5.5 min at 3 processes; `check.py` exits 1 on any failed assertion).
- It shares **no code** with the author's `t2lib.py`, with `iolib.py`, or with the mg-5ecf audit engine. The one exception is the LP probe (`lpprobe*.py`). It imports the author's LP builder read-only, and it is labelled as such below.
- It has its own canonical interval-order generator (`eng.gen`). Its counts equal OEIS A022493 for n ≤ 10, and all outputs are distinct.
- Separators come from the **cover relation**.
- Laws come from an ideal-lattice DP with forward/backward counts. Joint events (`Λ₁`, `Λ₂^(k)`) come from an automaton DP.
- The bad-`L` search is a DFS with a dead-state memo on (ideal, last element). It enumerates **every** dominance-respecting K-bad `L`.
- The kill rules (Thm 3.1 consecutive "TS", 2.1\*, 3.1\*) are re-implemented from the doc's **text**, not from `kstar.py`. The doc's classification is first-match. I record the full set of rules that fire as well.

Verdicts: **HOLDS** (re-derived or recomputed), **BROKEN** (false as stated), **OVERSTATED** (true only in a weaker form), **UNVERIFIABLE** (not checkable from here, or not checked). My own statements carry the labels PROVEN / EMPIRICAL / CONJECTURED.

Per the ticket, computation here is an instrument (re-checks, controls, a counterexample search for the scope of Thm 3.1). No case census was extended past the author's n ≤ 10.

---

## 0. Summary

| # | claim (doc §) | verdict |
|---|---|---|
| 1 | No proof of 1/3–2/3 for interval orders is claimed (§0.8, §7) | **HOLDS.** Nothing in §1–§6 implies it. See §1 below for exactly what a proof of the two-separator lemma would and would not give. |
| 2 | Thm 1.1 Swap Identity `|Λ₁(a,a')| = |Λ₁(a',a)|`, every poset (§1) | **HOLDS** (PROVEN, re-derived, §2.1). EMPIRICAL: 0 violations on 22 868 ordered pairs of 1 000 random interval orders (n = 9–13) and 18 186 of 1 000 random general posets (n = 7–10). Control (above-separators only) fires 10 816 / 12 086 times. |
| 3 | Cor 1.2 (dominance: `S(a',a) = ∅`, identity exact); Cor 1.3 (Brightwell = identity minus a term, lossy exactly at strict containment) | **HOLDS** (re-derived, §2.1). |
| 4 | §2.1 no-go: no inequality in the joint law of `X = {a,a'} ∪ S` refutes an `L`-consecutive two-separator dominance step; P5 is the witness | **HOLDS** as stated, for the X-local notion (§2.3). P5 recomputes exactly: `e = 11`, three laws `8/11`, `(Λ₁,Λ₂,Λ₃) = (3,5,3)`. The AA/BB dominance types are covered too, by the n = 7 witness (recomputed). The whole LCC table reproduces **exactly** for n ≤ 9 with independent code, row for row. |
| 5 | §0.1 / §2.1 "a one-step two-separator lemma can only live at containment steps" | **OVERSTATED.** It is true only for lemmas in the joint law of X (or X ∪ Y). At the next scope the author tested, X ∪ Y ∪ Inc(S), the AA/BB dominance steps have **0** LCC configurations for every n ≤ 9 (author's table, reproduced). Only AB dominance steps have witnesses there (8 at n = 9). So a one-step lemma for AA/BB dominance steps that looks at the separators' incomparables is **not** excluded. §7's table states the X∪Y∪Inc(S) row correctly ("8 AB configurations"); §0.1 and §2.1 "Reading" do not. |
| 6 | Prop 2.2 (split injection, `Z = S`) | **HOLDS** (PROVEN, re-derived, §2.2). EMPIRICAL: 0 / 640 violations. Control `Z ≠ S`: 151 / 194 violate. |
| 7 | Prop 2.3 (`4/15 < q < 1/3`, `β ≥ 1 − 3q + 2γ`, `u_s + u_t ≥ 2 − 5q + 3γ`) | **HOLDS** (re-derived line by line, §2.2). |
| 8 | Prop 2.4 (unique maximal `a` of `D_s` ⟹ `P[a<a'] ≤ 2P[s<a']`) via the audited dual Swap Ladder | **HOLDS** (§2.2). The hypotheses of mg-ce69 Thm 1.4 (dual) are checked. EMPIRICAL: 0 / 1 015 violations. Control (a maximal but not unique): 3 177 / 3 688 violate. T11 recomputes exactly (`2/3, 1/3, 1/5, 43/60`, equality in Prop 2.4). |
| 9 | Thm 3.1 Two-Step Lemma, `k ≥ 3`, every poset; Thm 2.1\*, 3.1\* (§3.2) | **HOLDS** (PROVEN, re-derived line by line, §2.4, including the cases `z = b ∈ A(a,c)` and `w = a ∈ B(c,b)`). EMPIRICAL: the unconditional inequality has 0 violations on 212 342 interval-order triples and 158 294 general-poset triples. Control (cancel all of `A(a,c)`): 23 064 / 22 847 violations. |
| 10 | O9a/O9b killed by Thm 3.1 at `[3,4] ≺ [2,6] ≺ [4,5]`, k = 2; the IIS certificate (§3.1, §3.3) | **HOLDS**, reproduced exactly. The separator sets `A(a,c) = {[5,6],[6,6]}`, `A(b,c) = {[6,6]}`, `B(c,a) = {[1,2]}`, `B(c,b) = {[1,2],[2,3]}` and the two counted events recompute. 3.1\* also fires on both. |
| 11 | n = 10: 24 posets, 29 bad dominance-`L`, 28 by Thm 3.1, 1 by 3.1\* (the S10 poset quoted), 0 survive; n ≤ 8: no bad `L` (§3.3) | **HOLDS**, reproduced exactly with independent code (`out_badl_4_9.txt`, `out_badl_10.txt`). Full kill sets at n = 10: {TS, 2.1\*, 3.1\*} on 9, {TS, 3.1\*} on 19, {3.1\*} only on 1. |
| 12 | Cor 3.2: every interval order with n ≤ 10 has a probability-free certificate (Thm 2.1 + 3.1/3.1\* + enumeration) | **HOLDS** (PROVEN, computer-assisted; the logic is checked in §2.5). "Probability-free" means that no numerical law is computed; the proof still uses Zaguia's Lemma 7 (dominance ⟹ `P ≥ 1/2`) to restrict to dominance-respecting `L`. |
| 13 | Staircase family: 2 527 bad `L`, 22 survivors on 21 posets (n = 12, 13) (§0.4, §3.3) | **Not reproduced as a count** (the family is the author's/audit's construction). Reproduced **in kind** with my own independently built family: 498 bad `L` → 464 TS, 8 by 2.1\*, 18 by 3.1\*, **8 survive** (7 posets, n = 12–14), including the author's first survivor verbatim. |
| 14 | Headline "It first fails at n = 12" | **OVERSTATED.** It first fails at n = 12 **within the staircase family**. At n = 11, only that family was searched (the doc's own §7 says so). My sample adds no n = 11 survivor, but it is a sample. Correct wording: "the smallest known failure is at n = 12". |
| 15 | §4: Q12 stays LP-feasible, `ε* = 1/21` (T1), `1/48` (all tools); second n = 12 survivor `1/57`, `1/102`; 13 of 22 feasible | **HOLDS for Q12 and the second survivor on re-run, but with the author's LP code, so not independent.** 13/22 was not re-run. Probes (§3): adding every distribution-free 3-cycle inequality (600 rows) does not move `ε*`, and neither does adding Thm 3.1 explicitly as a linear row for every triple (120 rows). My engine confirms that Q12's `L` is dominance-respecting and K-bad, that none of TS/2.1\*/3.1\* fires, and that the centre triples have `k = 3`, the others 4. |
| 16 | Lemma C (CONJECTURED) kills every known obstruction: 2/2, 24/24 (29/29 `L`), 547/547 | **HOLDS for n = 9, 10** (reproduced), and for all 8 survivors of my own family. 547 was not re-run. As a conjecture it is correctly labelled. |
| 17 | §5 general posets: survivors from n = 9, all steps 2+2-trapped | **HOLDS for the quoted n = 9 example** (recomputed: dominance-respecting, K-bad, no kill, every step non-dominance with `(|A|,|B|) = (2,0),(1,1)×6,(0,2)`, `δ = 1/45`). The sample counts (19 996 / 153 / 448 / 23) were not re-run. |
| 18 | §6: "Thm 3.1 is exactly the extra ingredient their [Gaetz–Gao] framework would need outside type A" | **OVERSTATED** (speculative). The doc's own §4 shows Thm 3.1 is not sufficient beyond n = 10. Nothing shows it is necessary. |
| 19 | Uses of mg-afa4 (Thm 2.1, Prop 3.1, Cor 3.2) and mg-ce69 (Thm 1.4, Lemma 1.5) | **HOLDS.** They are used as audited in `docs/AUDIT-mg-afa4.md` (§2.6). The OVERSTATED "equivalent" of afa4 §0.2 is not used. "Containment step" is defined as **strict** nesting, which is the reading the afa4 audit requires for Prop 2.4. |

**Net:** mg-561a is sound. It claims what it proves, and it labels the rest. The new mathematics is a real advance on the Brightwell route: the Swap Identity, and the Two-Step Lemma it enables. Every piece of it is correct. The route is **not** a proof, and §1 makes precise how far it is from one.

---

## 1. "Any two-separator proof is a claimed proof": what would a proof of the lemma actually give?

The ticket treats any two-separator lemma, combined with Thm 2.1, as a claimed proof of 1/3–2/3 for interval orders. So I asked exactly which implications are PROVEN and which are EMPIRICAL.

**(a) The chain that is PROVEN.** Suppose `P` is a counterexample. Then its 2/3-order `L` is a dominance-respecting linear extension (afa4 Thm 2.1(a) + Zaguia Lemma 7), and `L` avoids every forbidden pattern of Thm 2.1, 3.1, 2.1\* and 3.1\*. Hence 1/3–2/3 holds for `P` whenever **every** dominance-respecting `L` of `P` contains one of those patterns. That is a finite, probability-free check, done for n ≤ 10.

**(b) What Lemma C would add.** Lemma C forbids one more pattern: an `L`-consecutive strict-containment step with exactly 2 separators. A proof of Lemma C gives 1/3–2/3 for interval orders **only together with** the combinatorial statement

> **K_C (EMPIRICAL, not stated in the doc in this form).** Every dominance-respecting linear extension of a non-chain interval order contains one of: a consecutive incomparable step with `|S| ≤ 1`; a TS / 2.1\* / 3.1\* pattern; a consecutive strict-containment step with `|S| = 2`.

- K_C is exactly what the doc's "Lemma C kills every known obstruction" tests.
- It holds on the n ≤ 10 census (reproduced: 2/2 and 29/29 `L`) and on every staircase survivor either of us found.
- It is **not proven**. Claim K, its predecessor, looked equally solid through n = 8 and died at n = 9.
- So **a proof of Lemma C is not a proof for interval orders**. It would move the gap from a probabilistic lemma to the combinatorial K_C.
- The doc does not claim otherwise, but it also does not say so. I recommend stating K_C explicitly next to Lemma C.

**(c) The naive global lemma.** Consider "in a counterexample, no `L`-consecutive step has exactly 2 separators", as a *global* statement.
- It is not refuted by §2.1. The no-go refutes only *proofs* that look at X (or X ∪ Y).
- Combined with Thm 2.1, it would reduce 1/3–2/3 to "every `L` has a consecutive incomparable step with `|S| ≤ 2`". That is again an unproven combinatorial statement. For general posets, the doc's `general.py` reports 0 non-chain survivors of the rule on a random sample.
- So the naive lemma, too, is a reduction and not a proof.

**(d) Bounded range (the "new environment").** Nothing in mg-561a uses bounded range.
- Every obstruction found is a unit staircase plus a few long intervals.
- In Q12 no element is incomparable to more than 6 others (the maximum, 6, is attained by the long intervals `[2,5]` and `[5,8]`; every other element has 1–4). So its incomparability degree is small.
- So bounded range does not remove the survivors. The two-step obstruction occurs at incomparability degree ≤ 6, well inside any range window the programme considers.
- (EMPIRICAL remark from the witness list; I did not compute `π` in the programme's normalisation.)

---

## 2. Line-by-line on the PROVEN parts

### 2.1 Thm 1.1 and Cor 1.2 / 1.3

**Thm 1.1.**
- Let `V` be the set of extensions in which exchanging the positions of `a` and `a'` again gives an extension. The exchange is an involution on `V`, and it swaps the two orientations.
- Claim: `V ∩ {a before a'} = Λ₁(a,a')`.
  - (⊆) Suppose a separator lies between. An above-separator `z` (with `a ⋖ z`) would end up before `a`; a below-separator would end up after `a'`. Either way the exchange is invalid.
  - (⊇) With no separator between, the afa4 Thm 2.1(b) cover argument (audited HOLDS) shows that nothing between is above `a` or below `a'`. Also `down(a')` lies entirely before `a`'s slot, since nothing between is below `a'`. So the exchange is valid.
- The reverse orientation is symmetric, with `S(a',a)`. Hence `|Λ₁(a,a')| = |V|/2 = |Λ₁(a',a)|`. **HOLDS.**

**Cor 1.2.**
- `a' ⋖ z` gives `z ∈ up(a') ⊆ up(a)`, so `z` is comparable to `a`. Dually for `z ⋖ a`.
- So `S(a',a) = ∅` and `Λ₂(a',a) = ∅`. **HOLDS.**

**Cor 1.3.**
- For strict `a ⊂ a'`: `A(a',a) = ∅`, since `l(z) > r(a') > r(a)`.
- `B(a',a)` consists of the maximal elements of `{w : l(a') ≤ r(w) < l(a)}`. Such a `w` is covered by `a`, because any `u` with `w < u < a` also lies in that set.
- It is non-empty by canonicity: `l(a) − 1 ≥ l(a')` is a right endpoint. **HOLDS.**

### 2.2 Props 2.2, 2.3, 2.4

**Prop 2.2.**
- With `a ⊂ a'` strict and `a` first: `B(a,a') = ∅`, since `w < a'` gives `r(w) < l(a') < l(a)`, so `w < a`.
- Exchange the first separator `f` after `a` with `a'`:
  - `a'` moves earlier. `down(a') ⊆ down(a)` precedes `a`, so this is valid.
  - `f` moves later. An element `u` between with `u > f` has `u > a`, and `u` is not above `a'` (it precedes `a'`). So `u ∈ Z ∖ {f} = {g}`, but `g ∥ f`. So this is valid too.
- The image has only the pre-`f` elements between `a` and `a'`, so it lies in `Λ₁`.
- Recovery: `f` is the first (from `Λ₂^(1)`) or the second (from `Λ₂^(2)`) separator after `a'`. The map is injective on each part. `Z = S` is used exactly at "`u ∈ {g}`, `g ∥ f`". **HOLDS.**

**Prop 2.3.**
- `Λ₂^(2) = {s before a', t before a'}` exactly, since `s, t > a`. So `P(Λ₂^(2)) = β`.
- The rest is linear algebra: `P(Λ₂) = 1 − 2q + γ` (Thm 1.1), `P(Λ₁) = q − γ`, `P(Λ₂) ≤ (q − γ) + β` (Prop 2.2), and `P(Λ₂) = u_s + u_t − β`.
- `s, t ≻ a'` holds since `s, t ≻ a`, `s, t ≠ a'`, and the step is consecutive. **HOLDS**, all four inequalities.

**Prop 2.4.**
- `D_s = ↓s ∖ ↓a' ∖ {s} = {z : l(a') ≤ r(z) < l(s)}`, and `a ∈ D_s`.
- Suppose `z > a` lies in `D_s`. Then `r(a) < l(z) ≤ r(z) < l(s) ≤ r(a')`, so `z ∈ Z` and `z < s`. This contradicts `s ∈ min Z`. So `a` is maximal in `D_s`.
- mg-ce69 Thm 1.4 (dual) needs `a' ∥ s` and `up(a') ⊆ up(s)`. The latter holds since `r(s) ≤ r(a')`.
- The chain top of `↓s ∖ ↓a'` is `s`, then the unique maximal element `a`. Then `t₀ = P[s<a']`, `t₁ = P[a<a'<s] ≤ t₀`, and `P[a<a'] = t₀ + t₁`, because `{s<a'} ⊆ {a<a'}`. **HOLDS.**

### 2.3 The no-go (§2.1): what it does and does not refute

- The LCC constraints are exactly what a counterexample's `L` imposes on the joint law of X.
- An LCC configuration inside a real poset therefore satisfies every *true* inequality on that joint law. So no such inequality refutes the configuration.
- This is valid as meta-reasoning, since the witness has the same local structure: separator roles, covers and induced order.
- Witnesses exist for the AB dominance type from n = 5 (P5) and for the AA/BB dominance types from n = 7 (recomputed: laws 25/37, 180/259, 30/37, 25/37). So the X-local statement **HOLDS for every dominance type**.
- **Scope (item 5 above).** At X ∪ Y ∪ Inc(S), AA/BB dominance has 0 witnesses for n ≤ 9. A one-step lemma for those types at that scope is open. So "only containment steps can carry a one-step lemma" is true only at X ∪ Y scope.
- The rule test in §2.3 ("forbid dominance-AA/BB leaves 13") shows that such a lemma would not suffice on its own. That is a separate point.

### 2.4 Thm 3.1 (and 3.1\*, 2.1\*)

- **Identities.** `Λ₂(a,c) = ∪_{z∈A(a,c)}{z<c} ∪ ∪_{w∈B(a,c)}{a<w}` exactly, because `z > a` and `w < c` force the orientation.
- **Lower bounds.**
  - For `z ∈ A(b,c)`: `{z<c}` forces `b < z < c`, so it lies in `Λ₂(b,c)`.
  - For `w ∈ B(c,a)`: `{c<w}` forces `c < w < a`, so it lies in `Λ₂(c,a)`.
  - The union of the shared events is bounded by the reverse term, and the reverse terms cancel. The sum identity is `2 − 2q₁ − 2q₂`.
- **Inversion check.** Every counted event is an `L`-inversion.
  - `z ∈ A(a,c)`: `z ≻ a` and `z ≠ c`, so by consecutiveness `z ≻ c`. This includes `z = b` when `a ⋖ b`; the event is then `{b<c}`, with probability `q₂ < 1/3`.
  - `w ∈ B(a,c)`: `w ≺ c` and `w ≠ a`, so `w ≺ a`.
  - `w ∈ B(c,b)`: `w ≺ b` and `w ≠ c`, so `w ≺ c`. This includes `w = a`, with probability `q₁`.
  - `z ∈ A(c,b)`: `z ≻ c` and `z ≠ b`, so `z ≻ b`.
- **Count.** Each counted event has probability `< 1/3` and the sum is `> 2/3`, so `k ≥ 3`. **HOLDS.**
- **3.1\* and 2.1\*.** Consecutiveness is used only in the inversion check, and the "`L`-outside" hypothesis replaces it verbatim. The RHS needs only `a ≺ c`, `c ≺ b`. **HOLDS.**
- **Remark "both steps dominance ⟹ k = |S(a,c)| + |S(c,b)| ≥ 4".** The cancelled sets `A(b,c) ⊆ S(b,c)` and `B(c,a) ⊆ S(c,a)` are empty by Cor 1.2. **HOLDS.**

### 2.5 Cor 3.2, the certificate logic

- A counterexample has no twins (twins are balanced).
- Its `L` puts `x` before `y` whenever `down(x) ⊆ down(y)` and `up(x) ⊇ up(y)` (Zaguia Lemma 7: `P ≥ 1/2`, so `≻` cannot hold). In canonical form this is interval dominance.
- So a counterexample with n ≤ 10 would have one of the enumerated `L`, and each of them carries a pattern forbidden by a theorem. The enumeration is complete: it is a DFS over all extensions of `P ∪ dominance`, pruned only by the `|S| ≥ 2` rule.
- n ≤ 8: my engine finds 0 bad dominance-`L` (afa4's K census, audited, found 0 even without the dominance restriction). **HOLDS.**

### 2.6 Imports

- afa4 Thm 2.1(a,b), Cor 3.2 and Prop 3.1 are used as the afa4 audit verified them.
  - Prop 3.1 is cited, but nothing in T2 depends on the interval formula, since separators are computed from covers.
  - "Containment step" = strict, consistent with the audit's note on Prop 2.4.
- mg-ce69 Thm 1.4 (dual) is used with its hypotheses checked (§2.2). Lemma 1.5 appears only in the LP.
- afa4's OVERSTATED "equivalent" (§0.2) does not appear in T2.

---

## 3. The LP claims (§4), probed

- I did not build an independent LP: no LP library is available here (no scipy), and a second exact simplex was out of scope. `lpprobe.py` re-runs the author's `lpcheck.build` + `xlp.solve` read-only. On Q12 it returns `1/21` (T1) and `1/48` (T1+T2+T3); on the second n = 12 survivor, `1/57` and `1/102`. These match the doc.
- **Code review of the LP rows.**
  - T1 has the Swap Identity for every ordered incomparable pair, `B ≤ P[a<a']`, `B ≥` each separator event, the union bound, exact inclusion–exclusion with `J` when `|S| = 2`, and `B = 0` when `S = ∅`.
  - T2 has the chain-bottom ladders in `P` and in the dual for every H1 pair, plus the Doubling equality exactly under Lemma 1.5's hypotheses (and its dual).
  - T3 is Prop 2.2.
  - Every row is a theorem. So "refuted" is sound; "feasible" is a statement about this row set only.
- **Gap found in the row set, and why it does not matter here.**
  - Thm 3.1's proof bounds the *union* of the shared events by `B(b,c)`. The LP has only per-event bounds `B(b,c) ≥ e_z` and a *sum* upper bound on `B(a,c)`. So when two or more events are shared, Thm 3.1 is **not** a linear consequence of the LP rows. The doc's list "no linear combination of Thm 1.1, 2.1, **3.1**, …" therefore claims a little more than the LP contains.
  - I added the proven unconditional Thm 3.1 inequality as a row for every incomparable triple (120 rows on Q12; 8 triples share two or more events). `ε*` stays `1/21` and `1/48` (`out_lpprobe2.txt`). **So the claim HOLDS for Q12** after the repair.
- **Distribution-free rows.** The 3-cycle inequalities `1 ≤ P[u<v] + P[v<w] + P[w<u] ≤ 2` (600 rows) do not move `ε*` either.
- The doc's reading "a proof needs a non-linear input or a new injection" is consistent with both probes.

---

## 4. What I did NOT do, and candidates ruled out

**Not done.**
- No independent LP solver. The §4 values are re-run on the author's code for Q12 and the second n = 12 survivor only; "13 of 22 feasible" was not re-run.
- The author's staircase family (547 posets / 2 527 `L` / 22 survivors) was not re-run. I used my own construction instead (§0 item 13).
- The §5 random general-poset counts, `contprobe.py` slacks, `csearch.py` and the 435-poset `tiefam.py` sweep were not re-run. T11 itself was recomputed.
- No census beyond n = 10. In particular, no n = 11 interval orders outside the staircase family (hence item 14).
- No literature pass (nothing new is cited beyond afa4's audited sources). Gaetz–Gao was not re-read (§6 of the doc rests on the afa4 audit, as the doc says).
- Range `π` was not computed in the programme's normalisation (§1(d) is a remark).

**Attacks that failed (the doc survived them).**
- Swap Identity off interval orders: 1 000 random general posets, 0 violations.
- Thm 3.1 unconditional form on general posets: 0 violations.
- A `z = b` or `w = a` edge case breaking the inversion step: handled (§2.4).
- Prop 2.2 without `Z = S`: fails, as the doc says (control).
- Prop 2.4 without uniqueness: fails, as the doc says (control).
- The LP missing Thm 3.1 / 3-cycle rows making Q12 look feasible spuriously: ruled out (§3).
- A bad `L` at n = 9, 10 escaping the kills through an enumeration gap: the independent DFS finds the same 2 + 29, with 0 survivors.
- A uniform random interval order (3 000, n = 11–14) with a K-bad dominance `L`: none found. As afa4 already noted, that negative is uninformative; the targeted family is the positive control and does find bad `L`.

## 5. Files (`code/audit_ksbft_6c30/`)

| file | output | content |
|---|---|---|
| `eng.py` | — | independent engine: generator, covers, separators, dominance, ideal/automaton DP |
| `t_gen.py` | `out_gen.txt` | generator vs OEIS A022493 |
| `badl.py` | `out_badl_4_9.txt`, `out_badl_10.txt` | every dominance-respecting K-bad `L`, n ≤ 10; TS / 2.1\* / 3.1\* kill sets |
| `props.py` | `out_props.txt` | Thm 1.1, Thm 3.1, Prop 2.2, Prop 2.4 on random interval orders and general posets, with controls |
| `witnesses.py` | `out_witnesses.txt` | P5, the n = 7 AA witness, T11, the O9a certificate, the §5 general survivor |
| `lcc.py` | `out_lcc.txt` | §2.1 LCC table, n ≤ 9 |
| `lemmac_census.py`, `lemmac.py` | `out_lemmac_census.txt`, `out_lemmac.txt` | Lemma C as a rule |
| `rand_badl.py` | `out_rand_badl.txt` | the certificate pipeline on random interval orders and on my own staircase family |
| `lpprobe.py`, `lpprobe2.py` | `out_lpprobe.txt`, `out_lpprobe2.txt` | Q12 with the author's LP (read-only), plus 3-cycle rows and explicit Thm 3.1 rows |
| `check.py`, `run_all.sh` | — | regenerates and asserts everything (31 checks) |
