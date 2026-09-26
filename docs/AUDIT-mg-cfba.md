# AUDIT of mg-cfba (KSBFT-S, Nested Balance): no proof of (NB) is claimed and none is hiding; every PROVEN lemma holds; T8 is the unique smallest indecomposable tie; (PNB) survives the full n ≤ 9 census; the "hosts are interval orders" and "no margin argument can prove it" claims are overstated

`mg-ebbe`, 2026-09-26. The subject is `docs/KSBFT-S-nested-balance.md` (commit `9d2b6f0`) and `code/ksbft_s_nested_balance_cfba/`. I am not its author. I re-derived every PROVEN claim by hand before running code. I attacked the doc for any hidden proof of (NB): such a proof would prove 1/3–2/3 on that class. I found none, and the doc claims none beyond inherited classes.

**Instrument:** `code/audit_ksbft_ebbe/` (`sh run_all.sh`: one process, about 20 s, exit 1 on any failure). It shares no probability code with the author's `nb.c` or with mg-ce69's `lib.py`.
- `aud.c` computes forward × backward ideal counts.
- It agrees with explicit permutation enumeration on 804 posets (every poset with n ≤ 6, plus 400 random ones with n = 7), with 0 mismatches.
- Every negative has a firing control:
  - a planted primal classifier disagrees on 120 posets;
  - the planted "top-only" trap rule and the tripling rule fire on 1 031 and 1 356 posets with n = 7;
  - the 2+2 detector fires on 2+2;
  - the good-pair detector fires on T8 (8 pairs).
- The census comes from mg-6b81's generator. Its counts are asserted equal to OEIS A000112 (1, 2, 5, 16, 63, 318, 2 045, 16 999, 183 231). Labelled completeness was certified independently by audit mg-6e7c.

Verdicts: **HOLDS** (re-derived or recomputed), **BROKEN** (false as stated), **OVERSTATED** (true only in a weaker form), **UNVERIFIABLE** (cannot be checked from here). Labels on my own statements: PROVEN / EMPIRICAL / CONJECTURED.

---

## 0. Summary

| # | claim (doc §) | verdict |
|---|---|---|
| 1 | Lemma 1.1: non-nested ⟺ top pair of an induced 2+2 **and** bottom pair of one (§1.2) | **HOLDS**. Re-derived. EMPIRICAL: 0 mismatches over every incomparable pair of every poset with n ≤ 9. The control fires. |
| 2 | Prop 1.2: on untrapped posets (NB) ⟺ 1/3–2/3; interval orders and height ≤ 2 are untrapped (§1.2) | **HOLDS**. Re-derived. |
| 3 | (NB) for height ≤ 2 and for semiorders is KNOWN (§1.2) | **HOLDS**. Follows from 2 plus TGF 1992 and Brightwell 1989 (both recalled, not re-read). |
| 4 | "1/3–2/3 for interval orders is OPEN" (so (NB) contains an open case verbatim) (§0.1, §1.2) | **HOLDS as "not found"**, and is **UNVERIFIABLE** as "open". My own literature pass also found no proof (sources in §2). The implication "(NB) ⟹ 1/3–2/3 on interval orders" is PROVEN either way. |
| 5 | Zaguia 1610.00809: Def. 1, Def. 5, Thm 2, Lemma 7, class list, no good-pair conjecture (§1.1) | **HOLDS** against the arXiv v3 text (§2). One sentence ("two lower covers of one element") is **UNVERIFIABLE** and not load-bearing. |
| 6 | Zaguia 1107.5626 (N-free): delete the minimum, take the top level with two elements having the same lower covers, Lemma 4, same step lemma (§1.1) | **HOLDS**. "Top level containing …" means the highest level that contains such a pair, which is what the paper does. |
| 7 | (NB) is NOT FOUND in the literature (§1.1) | **HOLDS** within the sources read. The unread sources (Brightwell 1999 survey, Linial, TGF, Peczarski) are UNVERIFIABLE. |
| 8 | T8: e = 42, δ = 17/42 at the non-nested (3,4), δ_N = 1/3 exactly, prime, range 4, open-window (NB) fails (§0.2, §2.4) | **HOLDS**, exact, own engine. |
| 9 | T8 is "the smallest tie" (§2.3); minimality "not checked" (§5) | **HOLDS, upgraded.** EMPIRICAL, full census: T8 is the **only** non-chain poset with n ≤ 9 that is indecomposable and has δ_N = 1/3. The other 51 ties are all decomposable. |
| 10 | Open-window 1/3–2/3 fails only on decomposable posets, while open-window (NB) fails on the prime T8 (§0.2) | **HOLDS** for n ≤ 9. Open-window 1/3–2/3 fails on 49 posets, 0 of them indecomposable. Open-window (NB) fails on 52: 51 decomposable plus T8. |
| 11 | T13, T14, N12 exact values; N12 has no firing full-chain good pair; N12 δ_N = 1/3 + 1/2346 (§2.3–2.4) | **HOLDS**. Exact, own engine, own good-pair detector. |
| 12 | "Every tie is a ladder equality (Zaguia good pair + Doubling at t_0 = 1/3)" (§2.4) | **HOLDS** for T8, T13, T14 (I checked T13 and T14; the author asserted only T8). T13 is `(x,b_0) = (2,0)`, `b_1 = 1`; T14 is `(0,1)`, `b_1 = 4`. |
| 13 | Lemma 2.1: a Doubling pair gives (NB) unless `t_0 < 1/6` (§2.4) | **HOLDS**. Re-derived, including the direction of Zaguia's Lemma 7. EMPIRICAL: the Doubling identity and `t_0 ≤ 1/2` show 0 violations on all 270 909 Doubling configurations with n ≤ 9. The control fires. |
| 14 | "So the search's floor is a real barrier …" (§2.4) | **OVERSTATED**. The barrier binds only posets that have a Doubling pair. A poset with no pair `down(x) = down(b_0)`, `up(x) ⊆ up(b_0)` (either orientation) is untouched by it. |
| 15 | "Zero margin ⟹ no margin or robustness argument can prove (NB)" (§0.2, §3.3, §4) | **OVERSTATED**. T8 kills one schema: a uniform margin `δ_N ≥ 1/3 + μ` on indecomposables. It does not kill margin arguments on another statistic, or ones that treat exact ties separately. 1/3–2/3 itself has zero margin at 2+1, and margin methods are still used on it. Compare with ONE-PT's 5/318: that is a different quantity on a different class (range ≤ 3, where T8 does not live, since its range is 4). |
| 16 | §2.1 / §4(a): "`P_9`, `rec11`, `Q_m`, `F_m` **and the mg-7bfc hosts** are interval orders"; "the programme's hand-built witnesses all live there" | **OVERSTATED** (partly false). `hub(2+2,{0,1,2},8)`, which is in the doc's own table, **contains an induced 2+2**. So do `W8`, `B7+tail r = 2, 3` and T8. What is true, and what the argument needs, is that all 54 named members have **0 non-nested pairs** (untrapped). So on every one of them (NB) ⟺ 1/3–2/3 still holds. |
| 17 | §2.1 table "`Q_m`, m = 0…14", "Fibonacci `F_5 … F_30`" | **OVERSTATED** (coverage). The author computed m ∈ {0,2,4,6,10,14} and 5 Fibonacci members. I checked all 15 `Q_m` and all `F_5..F_30` structurally (interval order, 0 non-nested pairs), and exact laws for n ≤ 22. |
| 18 | mg-2912 records: 0 NB failures; 1 023 of 2 534 are interval orders; 1 of the 44 with δ < 0.35 is one (§2.1) | **HOLDS**. Reproduced exactly. |
| 19 | §2.2 random prime range 8–14 (1 600 posets); §2.3 search minima 0.33577 / 0.33523 / 0.33425 | **UNVERIFIABLE** here. Not re-run: `aud.c` is dense in 2^n, and the samples are not stored. They are negatives about the posets visited, and nothing downstream depends on them. |
| 20 | Lemma 3.1 (a)–(d): a least (NB)-counterexample is indecomposable, comparability-connected, has chain modules, and (NB) is self-dual (§3.1) | **HOLDS**. Re-derived. |
| 21 | §3.2: the end theory (Local Linial, Q Thm 3.1, mg-ce69 Thm 4.1) transfers verbatim to a least (NB)-counterexample | **HOLDS**. Re-checked Q Thm 3.1's proof and Thm 4.1's items 1–4. Every pair whose non-balance is used is `(x, ·)` with `x` minimal, a pair of down-twins, or an explicitly nested pair. |
| 22 | §3.3 deletion: primal nesting is stable under deleting a maximal element, not a minimal one | **HOLDS**. The Lemma R constant (0.1716) and ONE-PT's 5/318 are cited, not re-checked. |
| 23 | §3.4 table: bounded range, D ≤ 7 and Lemma W "do NOT transfer" | **OVERSTATED** in the table's "NO", which should read "not known to". The prose ("not known to have range ≥ 8") is right. Whether AK25a/b or Haq26's balanced pair can be chosen nested is **UNVERIFIABLE** without the preprints. |
| 24 | Cor 3.4: (NB) on `Π_2` (§3.4) | **HOLDS**. It uses the audited classification (mg-eedd Lemma 4.2; my census shows exactly one ordinal- and disjoint-indecomposable range-≤ 2 poset per n = 4..9, an interval order each time), and reductions 3.1(a) **and (b)**; the doc cites only (a). |
| 25 | §3.5(iii): (PNB) "not refuted" | **HOLDS, strengthened.** EMPIRICAL: (PNB) and dual-(PNB) show 0 failures over the **whole n ≤ 9 census**, which the doc did not run. It is non-trivial there: `δ_P < δ_N` on 21 926 posets at n = 9. They also show 0 failures on the 2 534 records. |
| 26 | Verdict: (NB) is plausible but not a better target than 1/3–2/3 (§4) | **HOLDS**. It follows from rows 2, 4, 8–10 and 20–23 alone. It does not need the overstated rows 14–16. |

**No claimed proof of (NB) exists in the subject.** The PROVEN statements that bear on (NB) are the ones listed here, and none extends 1/3–2/3:
- inheritance on untrapped classes (Prop 1.2);
- the pair-local reductions (Lemma 3.1);
- Lemma 2.1, which is a conditional per-pair statement (`t_0 ≥ 1/6`);
- Cor 3.4, which rests on 1/3–2/3 already known on `Π_2`.

---

## 1. Re-derivations (the PROVEN claims)

**Lemma 1.1.** Suppose `down(x) ⊄ down(y)`. Then there is some `a < x` with `a ≮ y`.
- `a > y` would give `y < a < x`, and `a = y` would give `y < x`. So `a ∥ y`.
- Symmetrically there is some `c < y` with `c ∥ x`.
- `a < c` gives `a < y`, and `c < a` gives `c < x`. So `a ∥ c`, and `{a<x, c<y}` is an induced 2+2 with top pair `{x,y}`.
- Non-nestedness is the conjunction of the two primal non-inclusions (giving the top 2+2) and the two dual ones (giving the bottom 2+2).
- The converse is immediate.

Census check: 0 mismatches over all pairs with n ≤ 9. The control "top 2+2 alone" mismatches on 1 031 posets with n = 7.

**Prop 1.2.** Interval orders are exactly the posets whose down-sets form a chain under inclusion (Fishburn), so every pair is primal-nested. At height ≤ 2, take an incomparable pair:
- if both are minimal, then `down = ∅` for both;
- if both are maximal, then `up = ∅` for both;
- if one is minimal and the other maximal, then `∅ ⊆ down(other)`.

So on these classes the nested restriction is vacuous, and (NB) ⟺ 1/3–2/3.

**Lemma 2.1.** Zaguia calls `(X,Y)` critical when `U(Y) ⊆ U(X)` and `D(X) ⊆ D(Y)`; then `P(X≺Y) ≥ 1/2` (Lemma 7, v3). Take `X = b_0` and `Y = x`:
- `U(x) ⊆ U(b_0)` and `D(b_0) = D(x)`, so `P[b_0 < x] ≥ 1/2`, i.e. `t_0 ≤ 1/2`.

I re-derived the injection myself. Take an extension with `x` at slot `i` before `b_0` at slot `j`, and swap them:
- elements strictly between the two slots that lie above `x` also lie above `b_0`, so they come after `j`, and there are none;
- `down(b_0) = down(x)` precedes slot `i`.

Doubling needs `b_1` to be the **unique minimum** of `(↑b_0 ∖ ↑x) ∖ {b_0}`. The inverse swap of `b_0 < x < b_1` is then valid, because any `w ∈ ↑b_0 ∖ ↑x` lying between the two slots satisfies `w ≥ b_1`, so it comes after `x`. Then:
- `P[x<b_1] = 2t_0`;
- `t_0 ∈ [1/6, 1/3)` gives `2t_0 ∈ [1/3, 2/3)`;
- `(x,b_1)` is incomparable (`x < b_1` would put `b_1 ∈ ↑x`, and `b_1 < x` would force `b_0 < x`) and nested (`down(x) = down(b_0) ⊆ down(b_1)`).

The doc's "b_1 exists" must be read as "the chain bottom continues past `b_0`", which matches Thm 1.4's definition. Census: 270 909 configurations, 0 violations, and the tripling control fires on 1 356 posets with n = 7.

**Lemma 3.1.**
- (a) A non-chain ordinal summand keeps its law, and its down-sets and up-sets only gain whole summands.
- (b) A non-chain disjoint-union part keeps its law and its sets. Two chains give width 2, and Linial's pair has `x` minimal (primal-nested).
- (c) For a module `M`, the restriction to `M` of a uniform extension is uniform on `L(M)`, and `down_P = down_M ∪ D_M`.
- (d) Nesting is duality-symmetric.

All four hold, and they apply to a least counterexample within any class closed under summands and parts. That is what Cor 3.4 needs, where it uses (b) implicitly.

**§3.2 transfer.**
- Q Thm 3.1's proof (re-read, `docs/KSBFT-Q-local-width2.md`) uses only the contrapositives of Thm 2.1 and Cor 2.2. Those concern pairs `(x, c_j)` with `x` minimal, so `down(x) = ∅` and the pairs are primal-nested. The existence of `x` with `P[x first] ≤ 2/3` uses no balance.
- mg-ce69 Thm 4.1:
  - item 2 is stated for nested pairs;
  - item 3 (Cor 1.6) concerns nested full-chain ladders;
  - item 4 uses `(x,u)` and `(x,v)` with `x` minimal, plus the down-twins `(u,v)`.
- **HOLDS.** One caveat: statements phrased with `D` (e.g. `k < (D+1)/3`) transfer as implications, but a least (NB)-counterexample has no known `D`. The doc says so itself in §3.4.

**Deletion.** If `v` is maximal, then `v ∉ down(u)` for every `u ≠ v`, so the down-sets are unchanged. **HOLDS.**

## 2. Zaguia and the interval-order status (checked against the arXiv texts)

A sub-agent read `arXiv:1610.00809v3` and `arXiv:1107.5626v2` in full via pdftotext and quoted the text.

- **Def. 1:** "(i) D(a) ⊆ D(b) and U(b) \ U(a) is a chain (possibly empty); and (ii) P(a ≺ b) ≤ 1/2", "simultaneously in P or in its dual". This matches the doc.
- **Def. 5:** `D(a) = D(b)` and both private up-sets are chains. Matches.
- **Thm 2:** "A finite ordered set that has a good pair has a balanced pair." The proof steps `q_{n+1} ≤ … ≤ q_1` along `[U(b)∖U(a)] ∪ {b} = b_1 < … < b_n` and uses a first crossing. The pair is never named, but it is implicitly `(a, b_j)`, so it is nested, as the doc says.
  - Paper slip, not the doc's: `Σ_{j≤r} q_j = P(a≺b_r)` is undefined at `r = n+1`. The contradiction survives, because `q_{n+1} ≥ 1/2`.
- **Lemma 7:** direction as used above. Matches.
- **Classes:** width 2 ("Observe that every ordered set of width two has a very good pair", no proof); semiorders (Brightwell's pair); forests (Thm 6, via fences). Matches.
- **No conjecture that every poset has a good pair**, and no poset without one is exhibited. Matches.
- **1107.5626:** the unique minimum is deleted; `i` is "the largest with the property that `P_i` contains two distinct elements with the same set of lower covers"; Lemma 4 gives "`U(x) ∪ {x}` is a chain"; the step lemma has `D(a) = D(b)`. Matches the doc, reading "top level containing …" as "highest such level".
- **Not verified:** the doc's sentence "in every case the pair is two minimal elements, two maximal elements, or two lower covers of one element" (§1.1). It is not load-bearing, since nestedness already follows from Def. 5.

**Interval orders.** Sources checked, none of which lists interval orders as a solved class:
- Wikipedia's known-cases list: width 2, height 2, ≤ 13 elements, ≤ 6 incomparabilities per element, series-parallel, N-free, semiorders, polytrees;
- the Zaguia 2012 and 2019 introductions;
- Chan–Pak–Panova (Sorting20);
- Sah, arXiv:1811.01500;
- arXiv:2410.12494;
- Olson–Sagan;
- several web searches.

Brightwell 1999 and the citers of Brightwell 1989 were **not** checked. Verdict: "not found", as the doc says.

Two side remarks (PROVEN, trivial):
- **Series-parallel posets.** They are on Wikipedia's list and satisfy (NB) outright, by induction with Lemma 3.1(a)(b).
- **Automorphisms.** The Ganter–Hafner–Poguntke balanced pair need not be nested, so that case does **not** transfer to (NB) for free.

## 3. What I computed (EMPIRICAL, exact)

- **Full census n ≤ 9** (202 680 posets, including chains):
  - 0 failures of (NB), (PNB), dual-(PNB), Lemma 1.1 or Doubling;
  - 32 646 posets have a non-nested pair (3 / 68 / 1 444 / 31 131 at n = 6 / 7 / 8 / 9).
- **Ties.** 52 posets have `δ_N = 1/3`, and exactly one of them, T8, is indecomposable. That same poset is the only indecomposable open-window (NB) failure.
- **Open-window 1/3–2/3** fails on 49 posets, none of them indecomposable. This matches the "only 2+1 family" reading.
- **Witnesses:** T8, T13, T14 and N12 recomputed exactly (`out_witnesses.txt`), including primality and range, and the mechanism pairs for all three ties.
- **Families:** 54 named members (`out_witnesses.txt`). All have 0 non-nested pairs. Not interval orders: `W8`, `B7+tail r = 2, 3`, `hub`. Exact laws were computed for n ≤ 22, and (NB) holds on each.
- **Records:** 2 534, with 0 failures of (NB), (PNB) and dual-(PNB). 1 023 are interval orders; 1 of the 44 with δ < 0.35 is one.

## 4. What I did NOT do

- I did not re-run §2.2's random prime sampler or §2.3's beam searches (row 19). My engine is dense in `2^n`, and extending searches is outside the ticket rule. Their negatives are not audited here.
- I did not read Brightwell 1989/1999, Linial, TGF or Peczarski. I did not check the published (journal) numbering of Zaguia's papers.
- I did not re-check mg-eedd's Lemma R constant, ONE-PT's 5/318, or KSBFT-I. All are cited from their own audits.
- I did not recompute exact laws for family members with n > 22. `Q_m` for m ∈ {0,2,4,6,10,14} was recomputed by audit mg-6e7c. For m ∈ {3,5,7,8,9,11,12,13} nobody has computed δ. Their (NB) status equals their 1/3–2/3 status (0 non-nested pairs), which is CONJECTURED true by the frozen-margin argument of mg-ce69.
- I did not try to prove (NB) for interval orders, or to construct an (NB) counterexample beyond the census. The candidate space I checked is: every poset with n ≤ 9, the records, the 54 named family members, and the four witnesses.
- Census generation reuses mg-6b81's generator. I asserted only the counts (A000112); the labelled-completeness certificate is audit mg-6e7c's.
