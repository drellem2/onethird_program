# KSBFT-S: Nested Balance, i.e. "every non-chain poset has a balanced pair with comparable down-sets or up-sets". It is not in the literature. It holds on everything tested. It is boundary-tight on a prime 8-element poset, it contains the interval-order case of 1/3–2/3 (not found proven in the literature) exactly, and it forfeits the bounded-range environment. Not a better target than 1/3–2/3 (mg-cfba)

**Errata (mg-555c, per audit mg-ebbe, `docs/AUDIT-mg-cfba.md`).** No proof of (NB) is claimed, and every PROVEN lemma HOLDS on re-derivation. The verdict ("(NB) is not a better target than 1/3–2/3") **HOLDS**; it follows from Prop 1.2, T8 and §3.1–3.4 alone and does not need any of the overstated claims below. Corrected in place:
- **OVERSTATED (partly false): "the mg-7bfc hosts are interval orders" (§0.4a, §2.1, §4a).** `hub(2+2,{0,1,2},8)`, in this doc's own table, contains an induced `2+2`; so do `W8` and `B7`+tail r = 2, 3 (and T8). The `attach_both`/`attach_low` hosts, `P_9`, `rec11`, all `Q_m` and all `F_m` are interval orders. What is true, and what the argument needs: all **54** named family members (audit's list) have **0 non-nested pairs** (untrapped), so on every one of them (NB) ⟺ 1/3–2/3 still holds (Prop 1.2).
- **OVERSTATED: "zero margin ⟹ no margin or robustness argument can prove (NB)" (§0.2, §0.4, §3.3, §4).** T8 kills exactly one schema: a **uniform** margin `δ_N ≥ 1/3 + μ` on indecomposable posets. It does not kill margin arguments on another statistic, or arguments that treat exact ties separately (1/3–2/3 itself has zero margin at 2+1). ONE-PT's 5/318 is a different comparison quantity on a different class (range ≤ 3; T8 has range 4), so it is not "a better margin than T8's 0" for the same statement.
- **OVERSTATED: "the search's floor is a real barrier" (§2.4).** Lemma 2.1 binds only posets that **have a Doubling pair** (`down(x) = down(b_0)`, `up(x) ⊆ up(b_0)`, either orientation). A poset with no such pair is untouched by it.
- **OVERSTATED: the §3.4 table's "NO"** reads **"not known to"**, matching the prose. Whether AK25a/b's or Haq26's balanced pair can be chosen nested is UNVERIFIABLE without the preprints.
- **OVERSTATED (coverage): §2.1's "`Q_m`, m = 0…14" and "Fibonacci `F_5 … F_30`".** Laws were computed here for **6** `Q_m` (m ∈ {0,2,4,6,10,14}) and **5** Fibonacci members. The audit checked all 15 `Q_m` and all `F_5..F_30` structurally (interval order, 0 non-nested pairs) and recomputed exact laws for n ≤ 22.
- **UPGRADE: T8 is the UNIQUE indecomposable poset with `δ_N = 1/3` for n ≤ 9** (audit, full census, EMPIRICAL). The other 51 ties with n ≤ 9 are decomposable. This settles §5's "minimality of T8 not checked", and T8 is also the only indecomposable open-window (NB) failure at n ≤ 9. The audit also found T13 and T14's ties are Doubling at `t_0 = 1/3`.
- **UPGRADE: the full n ≤ 9 census has 0 failures of (NB), (PNB) and dual-(PNB)** (audit, EMPIRICAL; also 0 failures of Lemma 1.1 and of the Doubling identity over 270 909 Doubling configurations). (PNB) is non-trivial there: `δ_P < δ_N` on 21 926 posets at n = 9.
- **"1/3–2/3 for interval orders is open" (§0.1, §1.2, §4a):** "not found" **HOLDS** (the audit's own literature pass also found no proof); "open" is **UNVERIFIABLE** (Brightwell 1999 and citers of Brightwell 1989 unread). Read every "open" below as "not found proven".

Gated on audit mg-6e7c (`docs/AUDIT-mg-6e7c.md`), which I read first. That audit showed the SL-conjecture of mg-ce69 is **equivalent** to Nested Balance, and that the "(L3)-gap" is a strengthening of 1/3–2/3, not a reduction. Nothing here uses a claim that audit breaks. From mg-ce69 (`docs/KSBFT-Q2-both-ends.md`) I use only what the audit HOLDS: Thm 1.4 (Swap Ladder), Lemma 1.5 (Doubling), Thm 4.1.

**Instrument:** `code/ksbft_s_nested_balance_cfba/`.
- `nb.c` computes exact pair laws over the ideal lattice with `__int128` counts. Its balance tests are exact integer comparisons `3B ≥ e`, `3B ≤ 2e`.
- `sh run_all.sh` takes 32 s on one process and exits 1 on any failed assertion.
- `sh run_search.sh` runs the adversarial searches: 3 processes, about 25 min.

Computation was used only as an instrument (ticket rule): to cross-check, to probe named families, to sample, and to run adversarial searches for a counterexample. No census was extended.

**Labels.**
- **PROVEN**: proof in this file.
- **KNOWN**: in the literature, with the source read (by me or by the literature sub-agent, as stated).
- **EMPIRICAL**: exact arithmetic over a stated finite population.
- **CONJECTURED**: a guess.

**Conventions.**
- `down(x)`, `up(x)` are strict. A pair `x ∥ b` is **nested** if `down(x) ⊆ down(b)` or the reverse (**primal**), or `up(x) ⊆ up(b)` or the reverse (**dual**).
- **(NB)**: every finite non-chain poset has a nested pair with `P[x<b] ∈ [1/3, 2/3]`.
- **(PNB)**: the same with primal nesting only.
- `δ = max_{x∥y} min(p, 1−p)` over all pairs, and `δ_N` is the same maximum over nested pairs only. (NB) ⟺ `δ_N ≥ 1/3`.

---

## 0. Verdict

1. **Status: NOT FOUND in the literature, as a conjecture, theorem or counterexample (§1).**
   - Every proof of 1/3–2/3 in the good-pair lineage produces a nested balanced pair. That covers Linial (width 2), Zaguia 2012 (N-free), Zaguia 2019 (forest cover graphs; semiorders via Brightwell's pair) and Olson–Sagan 2018 (Young-diagram posets).
   - Height ≤ 2 (Trotter–Gehrlein–Fishburn) gives (NB) for free, because there every pair is nested.
   - Nobody states (NB) or the chain-bottom form of the ladder. Zaguia's step lemma needs the whole private up-set to be a chain.
   - **Cost: (NB) is exactly 1/3–2/3 on interval orders (Prop 1.2), and 1/3–2/3 for interval orders is not proven anywhere we could find.** So (NB) contains verbatim a case of the conjecture we found no proof of ("open" is unverifiable; errata).
2. **Plausibility: 0 failures everywhere (EMPIRICAL), but with zero margin (§2).**
   - Named extremal families: 24 posets here (`Q_m` to n = 46, the mg-7bfc hosts, Fibonacci to n = 30, `P_9`, `rec11`, `W8`).
   - 1 600 random prime indecomposable posets of range 8–14, n = 14–26. 1 449 of them have non-nested pairs, so (NB) is non-trivial there.
   - All 2 534 mg-2912 records.
   - 11 456 random indecomposable posets with n ≤ 10.
   - Adversarial searches (§2.3).
   - **But (NB) is tight on a prime poset.** `T8 = 8 0 0 2 6 3 e 17 5f` (n = 8, range 4, prime, `e = 42`) has `δ = 17/42` and `δ_N = 1/3` exactly. Every nested balanced pair sits on the boundary (1/3 or 2/3). The only interior balanced pair, `(3,4)` at 17/42, is non-nested.
   - Consequences:
     - **(NB) with the open interval is FALSE at n = 8 on a prime poset**, whereas for 1/3–2/3 the boundary is attained (EMPIRICAL) only by the decomposable 2+1 family.
     - **"`δ_N ≥ 1/3 + μ` on indecomposable posets" is false for every μ > 0** (a uniform margin; errata). The corresponding margin for `δ` is 0.3489 − 1/3 ≈ 0.016 (mg-2912, EMPIRICAL).
     - The adversarial search found more exact ties: `T13` (prime, range 6) and `T14`.
     - Where no full-chain good pair fires, it found `N12` (range 7) at `δ_N = 1/3 + 1/2346` while `δ = 1/2`.
   - Every tie and near-miss is **explained by a PROVEN ladder mechanism at equality**: Zaguia's good pair plus the Doubling Lemma, with `t_0 = 1/3` or just below it. None is an accident of search.
3. **Inductiveness: no gain, some loss (§3).**
   - The pair-local reductions survive: ordinal sum, disjoint union, non-chain modules, duality (PROVEN).
   - The whole local end theory (Local Linial, mg-5f14 Thm 3.1, Swap Ladder, mg-ce69 Thm 4.1) transfers verbatim, because it only ever used nested pairs (PROVEN, by inspection).
   - Transport under deletion is exactly the ONE-PT problem (Lemma R) with an extra constraint. Primal nesting is stable only under deleting a maximal element.
   - **The global half of the environment is lost:**
     - the bounded range `π ≤ L*` and width bound (AK25a/b, Haq26 bound `δ`, not a nested pair);
     - the D ≤ 7 finite-state proof (KSBFT-I certifies arbitrary pairs and LP combinations);
     - Lemma W and Thm 1.3'' (bounds on `δ`).
   - A least (NB)-counterexample could therefore have range ≤ 7.
   - A ladder proof of (NB) in a new class: I found none. Range ≤ 2 is PROVEN (Cor 3.4), but only by the existing exact computation.
4. **Verdict: (NB) is NOT a better target than 1/3–2/3. As a replacement target it is a dead end.**
   - It is strictly stronger and contains an open case verbatim.
   - It has zero slack on a prime poset, so no argument through a uniform `δ_N` margin on indecomposables can prove it (errata: other margin schemas are not excluded).
   - It gains nothing inductively, and it gives up the bounded-range environment.
   - Its one real attraction: the swap and ladder tools reach exactly the nested pairs. But that attraction is already fully cashed out by the end theory, which transfers unchanged to both problems.
   - **Two by-products are worth keeping (§4):**
     - **(a)** The programme's hand-built extremal witnesses all have **0 non-nested pairs** (untrapped), and most (`P_9`, `rec11`, `Q_m`, `F_m`, the `attach_both`/`attach_low` hosts) are **interval orders**, where every pair is nested and every pair carries a Swap Ladder. `hub`, `W8` and `B7`+tail r = 2, 3 contain `2+2` (errata). "1/3–2/3 for interval orders" is a natural, ladder-friendly subproblem with no proof found.
     - **(b)** (PNB) is **prefix-determined**: down-sets and pair laws are both fixed by the bottom window. So KSBFT-I's finite-state machine could certify it at small D with no new theory. That is the one cheap computation that would show whether nested balance is bottom-local.

---

## 1. Novelty and status

### 1.1 What the literature has (KNOWN)

The literature sub-agent read Zaguia 1610.00809 v3, Zaguia 1107.5626, Olson–Sagan 1706.04985 and Zaguia 2002.11604 in full, and the relevant passages of Sah, Chen, Chan–Pak–Panova, Billey–Swanson, Dolores-Cuenca et al., Gupta 2607.23926 and Haqi 2608.12678. It could **not** read Brightwell's 1999 survey, Brightwell 1989 (semiorders), Linial 1984, Trotter–Gehrlein–Fishburn 1992 or Peczarski 2008 (paywalled). Statements about those are marked "inferred".

- **Zaguia 2019 (Order 36, arXiv 1610.00809).**
  - *Def. 1 (good pair):* `(a, b)` such that, in `P` or in its dual, `D(a) ⊆ D(b)`, `U(b) ∖ U(a)` is a chain (possibly empty), and `P(a≺b) ≤ 1/2`.
  - *Def. 5 (very good pair):* `D(a) = D(b)` and both private up-sets are chains.
  - *Thm 2:* a good pair implies a balanced pair. The proof is the step lemma `q_{n+1} ≤ … ≤ q_1` along `b = b_1 < … < b_n` plus a first-crossing argument.
  - *Lemma 7:* a critical pair has `P ≥ 1/2`.
  - The pair produced is `(a, b_j)` with `D(a) ⊆ D(b) ⊆ D(b_j)`, so it is **nested**.
  - Classes: width 2 has a very good pair ("observe", no proof); semiorders have one (Brightwell's pair); forest cover graphs have one (Thm 6, via fences). In every case the pair is two minimal elements, two maximal elements, or two lower covers of one element: `D(a) = D(b)` or the dual.
  - There is **no conjecture** that every poset has a good pair, and no example of a poset without one.
- **Zaguia 2012 (EJC 19(2) P29, arXiv 1107.5626), N-free in the Hasse sense.**
  - Delete a unique minimum.
  - Take the top level containing two elements `a, b` with the same lower covers.
  - Lemma 4 makes `U(x) ∪ {x}` a chain.
  - Apply the same step lemma (stated for `D(a) = D(b)`, but only `⊆` is used).
  - The pair is nested.
- **Olson–Sagan (Order 2018):** the only citer that uses the pairs. It renames very good pairs "almost twins" and exhibits them in Young-diagram posets, so those balanced pairs are nested too. It notes an almost-twin pair need not be balanced. Its open questions are dimension 2 and distributive lattices; it does not ask about nested pairs or interval orders.
- **Other citers** (Sah, Chen, Chan–Pak–Panova, Billey–Swanson, Dolores-Cuenca et al., Zaguia 2021 greedy): no use of nested or good pairs beyond citation.
- **Width 2 (Linial; inferred, paper not read).** The standard proof takes `x` minimal and ladders up the chain `Inc(x)`. The pair `(x, c_r)` has `down(x) = ∅`, so it is nested. mg-5f14's Local Linial Thm is this argument, PROVEN in-repo, with `x` minimal.
- **Brightwell's view** (research page, via the sub-agent): 1/3–2/3 cannot be proved by "any sort of averaging argument"; one must argue at the top or bottom. That fits (NB), and fits the ticket's original item 3 (an averaging identity over ladders) badly.
- **Exhaustive checks:** Gupta 2607.23926 checks 1/3–2/3 (and the Gold Partition Conjecture) through n = 14. That says nothing about nested pairs.

**Novelty verdict.**
- (NB) itself: **NOT FOUND**, whether conjectured, proved or refuted.
- The **chain-bottom / 2/3 form** of the step lemma (mg-ce69 Thm 1.4): **NOT FOUND** in Zaguia 2012, Zaguia 2019, Olson–Sagan or the other citers. All of them need the whole private up-set to be a chain. The audit showed this form is irrelevant to whether (NB) holds, since rung 0 suffices.
- Caveat: the unread sources (Brightwell's survey, Linial, TGF, Peczarski) could contain a remark. The sub-agent's search terms were "good pair", "almost twin", down-set inclusion, "comparable down-sets" and "interval orders 1/3-2/3".

### 1.2 Where (NB) is the conjecture itself (PROVEN)

**Lemma 1.1 (non-nested ⟺ doubly trapped).** `x ∥ y` is non-nested iff `{x, y}` is the **top** pair of an induced `2+2` and also the **bottom** pair of an induced `2+2`.

*Proof.*
- `down(x) ⊄ down(y)` gives `a < x` with `a ≮ y`. And `a > y` is impossible, since then `y < a < x`. So `a ∥ y`.
- Symmetrically there is `c < y` with `c ∥ x`.
- `a ∥ c`: `a < c` gives `a < y`, and `c < a` gives `c < x`.
- So `{a < x, c < y}` is an induced `2+2`. Failure of `up`-comparability gives the upper `2+2` dually.
- Conversely, such `2+2`s witness both non-inclusions in each direction. □

**Prop 1.2.** Call `P` *untrapped* if no pair is doubly trapped. On untrapped posets, (NB) ⟺ 1/3–2/3. Untrapped classes include:
- **interval orders**, i.e. `2+2`-free posets (Fishburn): down-sets are linearly ordered by inclusion, so every pair is primal-nested and every pair is the start of a Swap Ladder;
- **height ≤ 2**: every element is minimal (`down = ∅`) or maximal (`up = ∅`).

*Proof.* Lemma 1.1. □

**Consequences.**
- **(NB) for height ≤ 2 is KNOWN** (TGF 1992; which pair TGF find is irrelevant).
- **(NB) for semiorders is KNOWN** (Brightwell 1989, which is Zaguia's very good pair).
- **(NB) for interval orders is exactly 1/3–2/3 for interval orders.** Neither the sub-agent nor I found a proof of that: it is absent from Wikipedia's list of known cases and from every citation list read. I treat it as **not found** ("open" is UNVERIFIABLE, audit mg-ebbe). So (NB) is at least as hard as a special case of the conjecture with no known proof.

---

## 2. Is it plausible?

All figures are exact per poset, from `nb.c`.
- `nb.c` agrees with explicit enumeration of linear extensions on 401 random posets, with 0 mismatches in `e`, `δ`, `δ_N`, `δ_P` or the pair counts (`out_xcheck.txt`).
- The classifier discriminates: the cross-check population includes posets with non-nested balanced pairs, and posets with `δ_P ≠ δ_N`.
- The `3+3` control has exactly one non-nested pair, the middle one.

### 2.1 The structured extremal families (`families.py`, `out_families.txt`): 24 posets, 0 failures

| family | n | range | δ | δ_N | non-nested pairs |
|---|---|---|---|---|---|
| `P_9`, `rec11`, `W8` | 9, 11, 8 | 5, 6, 6 | 0.4010, 0.3573, 0.4541 | same | 0, 0, 0 |
| `Q_m`, m ∈ {0,2,4,6,10,14} computed here (all 15 structurally by the audit) | 18–46 | 5 | 0.3936–0.3941 | same | **0** |
| `B7` + tail(12), r = 1, 2, 3 | 19 | 5–6 | 0.497, 0.429, 0.493 | same | 0 |
| Fibonacci, 5 members of `F_5 … F_30` computed here (all structurally by the audit) | 5–30 | 2 | → 0.38197 | same | 0 |
| `attach_both(F_N, R)`, `attach_low(F_N, R)`, `hub` | 13–26 | 3–10 | 0.456–0.500 | same | 0 |

**Finding (EMPIRICAL, `io.py`, `out_io.txt`).**
- `P_9`, `rec11`, `Q_m`, `F_m` and the `attach_both`/`attach_low` hosts are **interval orders**: no induced `2+2`, and the positive control finds `2+2` in `2+2`.
- **Errata:** the mg-7bfc `hub(2+2,{0,1,2},8)`, `W8`, `B7`+tail r = 2, 3 (and `T8`) **contain** `2+2`. All 54 named family members nevertheless have **0 non-nested pairs** (audit mg-ebbe, `code/audit_ksbft_ebbe/out_witnesses.txt`).
- So on the programme's hand-built extremal witnesses, (NB) **is** 1/3–2/3 (untrapped, Prop 1.2). They cannot distinguish the two statements.

The mg-2912 records are different. Only 1 of the 44 records with `δ < 0.35` is an interval order; they are width 2, where Linial gives (NB) anyway. Overall, 1 023 of the 2 534 records are interval orders (`out_records.txt`).

### 2.2 Random prime posets of range ≥ 8 (`randprime.py`, `out_randprime.txt`)

This is the only region where a 1/3–2/3 counterexample can live, given the D ≤ 7 result (audit mg-9268 HOLDS).

**Sampler.**
- Natural labelling. `i < j` is forced when `j − i > w`, and is random with probability `q` otherwise.
- Take the transitive closure.
- Keep posets with range 8–14 that are indecomposable and **prime** (no module of size 2..n−1).

**Results over 4 seeds × 400 posets (1 600 posets, n = 14–26):**
- **0 NB failures.**
- 1 449 posets have ≥ 1 non-nested pair.
- min `δ_N` = 0.4457, min `δ` = 0.4533.
- The "price of nesting" `δ − δ_N` is positive on 216 posets, with maximum 0.0479.
- On average 87% of balanced pairs are nested.

Random posets are far from the extremal region. This shows only that (NB) is not violated generically.

### 2.3 Adversarial search for a counterexample (`search.py`, `search2.py`, `run_search.sh`)

**Method.** Beam search over posets (toggle a relation, add an element, delete an element; indecomposable only), minimising `δ_N`. The four objectives were:
- `δ_N`;
- a smooth surrogate (the total excess of near-balanced nested pairs);
- `δ_N` restricted to posets with **no firing full-chain good pair**, i.e. no nested `(a, b)` with a chain private set and `P[a<b] ≤ 2/3` (or the dual), which is exactly where Zaguia/Thm 1.4 does not already force (NB);
- `δ_P`, for primal only.

Starts: random posets, `T13`, `Q_0` and `rec11`. n = 9–22.

| search | best `δ_N` found | its `δ` | where |
|---|---|---|---|
| `δ_N`, n = 10 / 11 / 12 (4 seeds each) | 0.33577 / 0.33523 / 0.33425 | 0.44–0.47 | range 3–6 |
| `δ_N`, n = 13 | **1/3 exactly** (`T13`, prime, range 6) | 17/42 | |
| variable n, `δ_N` key, from random (n ≤ 22) | **1/3 exactly** (`T14`, range 5) | 656/1395 | |
| from `Q_0` (n = 18) | 0.39038 | 0.4033 | the local moves cannot leave the P_9 basin |
| **no firing full-chain good pair** | **1/3 + 1/2346** (`N12`, range 7) | **1/2** | |
| `δ_P` (primal only) | 1/3 exactly (n = 6, n = 8) | | |

**No counterexample: `δ_N ≥ 1/3` in every run, and `δ_P ≥ 1/3` too.** The mg-2912 records already contain the smallest tie: `T8` (n = 8) is in the n ≤ 9 census, which audit mg-6e7c found NB-clean, at **equality**. Audit mg-ebbe's full census shows T8 is the **unique** indecomposable `δ_N = 1/3` tie with n ≤ 9 (the other 51 ties are decomposable), and 0 (NB)/(PNB)/dual-(PNB) failures.

### 2.4 The ties are ladder equalities, not accidents (PROVEN mechanism; values exact, `witnesses.py`)

**`T8 = 8 0 0 2 6 3 e 17 5f`.**
- `0` and `1` are minimal down-twins with `up(0) ⊆ up(1)`, and `up(1) ∖ up(0) = {2 < 3 < 5}` is a chain. So `(0; 1 < 2 < 3 < 5)` is a full-chain good pair satisfying Doubling's hypotheses.
- Its steps satisfy `t_0 = t_1 ≥ t_2 ≥ t_3 ≥ t_4`, summing to 1 (Thm 1.4, Lemma 1.5).
- In `T8`, `t_0 = P[0<1] = 1/3`, so `P[0<2] = 2t_0 = 2/3`. Both sit exactly on the boundary.
- The top is the same configuration: `(5,6) = 1/3`, `(5,7) = 2/3`.
- **Control (asserted):** with the **open** interval, no nested pair of `T8`, `T13` or `T14` is balanced, while 1, 2 and 4 non-nested pairs respectively lie strictly inside.

**`N12 = 12 0 4 0 6 f 885 6 805 aff 5f 8af 5`.** No full-chain good pair fires, and the nested balance is carried by a **Doubling** pair:
- `P[0<2] = t_0 = 521/1564`, just below 1/3;
- `P[0<1] = 2t_0 = 521/782`, just below 2/3.

**Lemma 2.1 (PROVEN, a restatement of mg-ce69 Thm 4.1 item 4 for (NB)).** If `(x, b_0)` satisfies Doubling's hypotheses (`down(x) = down(b_0)`, `up(x) ⊆ up(b_0)`) and `b_1` exists, then (NB) holds at that pair unless `P[x<b_0] < 1/6`.

*Proof.*
- `t_0 ≤ 1/2`, by the swap: the pair is critical in the sense of Zaguia's Lemma 7.
- If `t_0 ∈ [1/3, 1/2]`, then `(x, b_0)` is balanced.
- If `t_0 ∈ [1/6, 1/3)`, then `P[x<b_1] = 2t_0 ∈ [1/3, 2/3)`, so `(x, b_1)` is balanced.
- Both pairs are nested. □

So, **for posets with a Doubling pair**, the search's floor is a barrier (errata: a poset with no Doubling pair in either orientation is untouched by Lemma 2.1). To escape it, a counterexample must move every Doubling pair's `t_0` from about 1/3 to below 1/6, and must break every good pair's chain. Local moves cannot do that, and nothing says it is impossible.

**Reading.**
- (NB) is attained with equality inside prime posets, by the very mechanism (good pairs, doubling) that proves it in the known classes.
- For 1/3–2/3 the same posets have `δ ≈ 0.40–0.50`: the conjecture's balance there is carried by **non-nested** pairs, far from the boundary.
- So (NB) is "barely true" exactly where 1/3–2/3 is comfortable. That is the opposite of what a good strengthening looks like.

---

## 3. Is it more inductive?

### 3.1 Reductions that survive (PROVEN)

**Lemma 3.1.** A least (NB)-counterexample `P` has these properties:
- (a) `P` is ordinal-indecomposable, i.e. `G(P)` is connected. Pair laws inside an ordinal summand are those of the summand, and down-sets and up-sets only gain whole summands, which preserves inclusions.
- (b) `P` is comparability-connected. If `P = A + B` has a non-chain part, that part's nested balanced pair keeps its law and its nesting. If both parts are chains, `P` has width 2 and Linial's pair `(x, c_r)` with `x` minimal is nested.
- (c) Every proper module of `P` is a chain. For a module `M`, the restriction of a uniform extension of `P` to `M` is uniform on `L(M)`, and `down_P(x) = down_M(x) ∪ D_M` with `D_M` common to `M`, so inclusions transfer.
- (d) (NB) is self-dual.

This is the same reduction list as for 1/3–2/3 (mg-7bfc Prop 3.1, audited): **no new reduction**.

### 3.2 The end theory transfers verbatim (PROVEN, by inspection of the pairs used)

- mg-5f14's Local Linial Thm 2.1 and Cor 2.2 use only pairs `(x, c_j)` with `x` minimal. These are primal-nested.
- Q Thm 3.1 (a low 3-antichain or Y-gadget at both ends) uses only Thm 2.1 and Cor 2.2 (I re-read its proof).
- mg-ce69 Thm 4.1 uses:
  - Swap-Ladder rungs, which are nested;
  - Lemma 2.1 dominance, applied only to antichains of minimal elements, which are pairwise nested;
  - the gadget dichotomy on `(x, u)` with `x` minimal;
  - Doubling.

So **every structural statement the programme has about the ends of a counterexample holds for a least (NB)-counterexample too**. Duals are handled by dual nesting, and even by (PNB) at the bottom. The flip side matters more: *the end theory never used anything beyond nested pairs*. (NB) is therefore not a new lever on the ends. It is the name of what the ends already give.

### 3.3 Deletion, and ONE-PT (PROVEN observations)

- If `v` is **maximal**, `down_{P−v} = down_P` on `P − v`, so primal nesting in `P − v` ⟺ primal nesting in `P`. If `v` is **minimal**, a pair primal-nested in `P − v` need not be primal-nested in `P`. Up-sets behave dually.
- The **law** transport is unchanged: it is mg-eedd's Lemma R (`|p_P − p_{P−v}| ≤ (√r−1)/(√r+1)`, sharp 0.1716 at `π(v) = 1`).
- So an (NB)-analogue of ONE-PT ("some maximal `v` and a primal-nested pair balanced in both `P` and `P − v`") faces **exactly** ONE-PT's obstruction: the transport moves `p` by up to 0.17. Its uniform `δ_N` margin on indecomposables is 0 (the prime `T8`, range 4). ONE-PT's 5/318 is a different comparison quantity on a different class (indecomposable, `7 ≤ n ≤ 16`, range ≤ 3, where T8 does not live), so the two numbers are not the same margin compared (errata).
- A margin-based induction that needs a **uniform** `δ_N ≥ 1/3 + μ` on indecomposables cannot prove (NB), because that margin is 0 (§2.4). Margins on other statistics, or schemes that handle exact ties separately, are not excluded (errata). I did not test the (NB)-ONE-PT statement itself.

### 3.4 What is lost

| environment fact | transfers to (NB)? | why |
|---|---|---|
| Bounded range `π ≤ L*`, width `≤ L*+1` (AK25a/b, Haq26, KSBFT Thms 1.4/1.5) | **not known to** | They bound `δ`, not `δ_N`. Large range forces some near-1/2 pair, whose nesting is uncontrolled. |
| D ≤ 7 finite-state proof (KSBFT-I, audit mg-9268) | **not known to**, as it stands | Its certificates are arbitrary pairs and Gordan/LP combinations. It could be re-run with primal-nested certificates (§4b). |
| Lemma W, Thm 1.3'', `δ ≤ 1/e − ε` consequences | not known to | They are statements about `δ`. |
| F1/F2 windows, prefix certificate (mg-6b81 Thm 2.4) | YES | They are statements about positions and laws, pair-agnostic. |
| Chain-modules-only, indecomposable (Lemma 3.1) | YES | |
| Both-ends gadget structure (§3.2) | YES | |

A least (NB)-counterexample is therefore **not known to have range ≥ 8**, or any range bound at all. That is a strict loss of the "new environment".

**Cor 3.4 (PROVEN, modulo mg-eedd Lemma 4.2, audited HOLDS).** (NB) holds on `Π_2` (range ≤ 2).
- The indecomposable members of `Π_2` are `A_3`, `2+2` and `F_m`. In `A_3` and `2+2`, a pair of minimal elements has law 1/2 by an automorphism. `F_m` is a semiorder, hence untrapped, and 1/3–2/3 holds on it (exact law, mg-eedd Thm 4.3).
- Apply Lemma 3.1(a).
- This is **not** a ladder proof. I found no class where a ladder or averaging argument proves (NB) while 1/3–2/3 is known only otherwise. For range ≤ 3 I did not prove (NB). mg-ce69's "Cor 1.6 covers every indecomposable range-≤3 poset" remains CONJECTURED, and would give it.

### 3.5 The original item 3 (averaging over ladders)

I found no averaging identity over nested ladders that forces a first rung ≤ 2/3 and reaching 1/3. Linial's `Σ_{x minimal} P[x first] = 1` gives the start condition for **one** ladder (minimal `x`, empty down-set). It says nothing about where that ladder's chain bottom branches, which is the entire content (Thm 4.1). Any identity would also have to be exact at `T8`, where every nested ladder that fires does so at equality. Brightwell's remark (§1.1) points the same way. Candidates tried and dropped:
- **(i) "Every Doubling pair has `t_0 ∈ [1/6, 1/2]`."** False. It is exactly the escape route Lemma 2.1 leaves open.
- **(ii) Restrict to posets with no firing full-chain good pair.** They exist (n = 12–13, range 7–8, found by search), and (NB) still holds there, via rung-0 or Doubling pairs.
- **(iii) Primal nesting only, (PNB).** Not refuted: 0 failures on all populations above, floor exactly 1/3. It is **stronger** than (NB) and still open.

---

## 4. Verdict and recommendations

**Nested Balance is plausible but it is the wrong target.**
- It is strictly stronger than 1/3–2/3. It contains the interval-order case (no proof found) **verbatim** (Prop 1.2).
- It is **boundary-tight on a prime 8-element poset** (`T8`), so its strict form is false and no uniform-`δ_N`-margin method on indecomposables can reach it.
- It keeps every pair-local reduction and all of the end theory. But it adds nothing to them (§3.2) and loses the bounded-range environment (§3.4).
- Proving it is at least as hard as the conjecture, and in the one respect that matters for this programme, bounded range, it is harder.

It is not a dead end *as a fact*: I expect it is true (CONJECTURED, on §2's evidence). It is a dead end **as a replacement target**.

**By-products worth a ticket.**
- **(a) 1/3–2/3 for interval orders.** In an interval order, every incomparable pair is nested (Prop 1.2) and so starts a Swap Ladder. Most of the programme's hand-built witnesses (`P_9`, `rec11`, `Q_m`, `F_m`, the `attach_*` hosts) live there; `hub`, `W8`, `B7`+tail r = 2, 3 do not, though all are untrapped (§2.1, errata). The case is not proven in the literature we found, and it is the natural class where the ladder machinery applies to **every** pair. Semiorders are KNOWN (Brightwell), so the gap is "interval but not unit interval".
- **(b) (PNB) under the KSBFT-I machine.** Primal nesting of a pair, like its law certificate, is determined by the bottom prefix. So KSBFT-I's tree, with certificates restricted to primal-nested pairs (single-pair and LP), would decide "(PNB) for range ≤ D" for small D with no new theory. This is the one cheap test of whether nested balance is bottom-local. **Not run** (ticket rule; it is a pm call).

---

## 5. What I did NOT do

- I did not read Zaguia's papers myself. The sub-agent read 1610.00809 and 1107.5626 in full, and I re-derived the step lemma it quotes (it is mg-ce69 Thm 1.4 with a full chain, audited). Brightwell 1989/1999, Linial 1984, TGF 1992 and Peczarski 2008 were **not read** (paywalled). "1/3–2/3 for interval orders is open" means **not found**, not verified.
- I did not prove (NB) in any class beyond those it inherits (Prop 1.2, Cor 3.4). I did not attempt range ≤ 3.
- I did not check minimality of `T8`: whether a smaller poset attains `δ_N = 1/3` with every nested balanced pair on the boundary, beyond the `2+1` family. The n ≤ 7 census would decide it; it was not re-run. **Settled by audit mg-ebbe:** T8 is the unique indecomposable `δ_N = 1/3` poset with n ≤ 9.
- I did not re-run the n ≤ 9 census for (NB). Audit mg-6e7c did (`EQV = 0`, NESTBAL on all). I did not run (PNB) on the census; only on 11 456 random posets with n ≤ 10, the records and the search populations. **Audit mg-ebbe ran it:** 0 failures of (NB), (PNB) and dual-(PNB) over the full n ≤ 9 census (and 270 909 Doubling configurations).
- I did not test the (NB)-ONE-PT analogue (§3.3), or re-run KSBFT-I with nested certificates (§4b).
- The random and adversarial searches are instruments. Their negatives say nothing beyond the posets visited. The searches start from few seeds, the local moves cannot leave the `Q_0` basin, and `n ≤ 22`.
- `nb.c` uses `__int128` counts with an overflow guard (`e < 4·10³⁷`). It never triggered on the posets here, all with `e ≤ 10¹¹`.

## 6. Files

`code/ksbft_s_nested_balance_cfba/`:
- `nb.c` — the engine.
- `fam.py` — helpers, reusing mg-ce69's `grow`/`dual`/`glue` and mg-7bfc's constructions.
- `xcheck.py` — engine vs explicit enumeration.
- `witnesses.py` — exact `T8`/`T13`/`T14`/`N12` values, mechanism and open-window control, asserted.
- `families.py`, `io.py`, `randprime.py`, `records.py`, `primal.py`.
- `search.py`, `search2.py`, `run_search.sh`.
- `out_*.txt` transcripts.
