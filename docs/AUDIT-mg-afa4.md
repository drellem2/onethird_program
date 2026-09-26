# AUDIT of mg-afa4 (KSBFT-T, interval orders): no proof of 1/3–2/3 for interval orders is claimed and none is hidden; "NOT FOUND in the literature" HOLDS on a literature pass I redid myself; every PROVEN statement HOLDS on re-derivation; every EMPIRICAL count reproduces exactly with independent code; one wording is OVERSTATED ("equivalent" in §0 item 2)

`mg-5ecf`, 2026-09-26. The subject is `docs/KSBFT-T-interval-orders.md` (commit `1778880`) and `code/ksbft_t_interval_orders_afa4/`. I am not its author and started from a fresh context.

**Instrument:** `code/audit_ksbft_5ecf/` (`sh run_all.sh`, about 3.5 min at 3 processes; exit 1 on any failed assertion). It shares **no code** with the author's `iolib.py`.
- It has its own canonical-interval generator. Its completeness is certified two ways:
  - counts equal OEIS A022493 for n ≤ 10;
  - every output equals the Fishburn canonical form recomputed from the poset alone (`eng.recanon`, down-set ranks). So outputs are pairwise non-isomorphic.
- Separators are computed from the **cover relation**, not from the interval formula. That makes Prop 3.1 a genuine cross-check.
- The bad-`L` search is a DP over (ideal, last element), not the author's prefix-pruned DFS.
- Every negative has a firing control:
  - a planted law error is caught;
  - a general poset with 2+2 has a bad `L`, and the author's quoted `L` is bad;
  - the "above-separators only" injection fails 653 times;
  - the non-dominance `L` break Prop 2.4 (6 774 cases);
  - Doubling fails off the down-twin classes (9 022 cases);
  - a planted SL2 violation is rejected.
- Witness constructors for `Q_m` (mg-ce69) and the mg-7bfc hosts are imported read-only. All computation on them is mine.

Verdicts: **HOLDS** (re-derived or recomputed), **BROKEN** (false as stated), **OVERSTATED** (true only in a weaker form), **UNVERIFIABLE** (cannot be checked from here). Labels on my own statements: PROVEN / EMPIRICAL / CONJECTURED.

---

## 0. Summary

| # | claim (doc §) | verdict |
|---|---|---|
| 1 | 1/3–2/3 for interval orders is NOT FOUND in the literature (§0.1, §1) | **HOLDS.** Literature pass redone by me, from sources I opened myself (§1). Nothing proves it, and nothing lists interval orders as a known class. "Open" is **UNVERIFIABLE**: no source says so either way, and the doc itself says only "open as far as can be verified". |
| 2 | No proof of 1/3–2/3 on interval orders is claimed | **HOLDS.** §0.7 and §7 say so explicitly, and nothing in §2–§6 amounts to one. The only sufficient condition offered, Claim K, is shown **false** by the doc itself, and I reproduce that. There was no "claimed new theorem" to attack, so task item (2) is vacuous; §3 below attacks everything that *could* have been one. |
| 3 | Thm 2.1(a): with no balanced pair, `P[x<y] > 2/3` is a linear extension (§2) | **HOLDS** (PROVEN, re-derived). It is the standard "no 3-cycle since the three events are jointly impossible" argument, and is very likely folklore. The doc claims no novelty. |
| 4 | Thm 2.1(b): `P[a<a', some z∈S between] ≥ 2P[a<a']−1`; hence ≥ 2 separators at `L`-consecutive incomparable pairs (§2) | **HOLDS** (PROVEN, re-derived line by line). EMPIRICAL: the unconditional injection `|Λ₁| ≤ |Λ₃|` has 0 violations on every ordered incomparable pair of T8, T13, T14, N12, P9, Q_0/Q_4/Q_14, A14, attach_low(F_12,8), attach_low(F_16,10), both double hubs, F_12, O9a, O9b, and 400 random interval orders with n = 10–24 (15 864 pairs). Control (above-separators only): 653 violations, which is the author's number. |
| 5 | §0.2: the semiorder count "is equivalent to" every `down(z)` being an `L`-prefix | **OVERSTATED.** Only "prefix ⟹ count" holds, and that is the only direction the argument uses. Counterexample to the converse: `[1,1][1,3][2,2][3,3]` with `L` in that order, which respects dominance. There are 292 such dominance-respecting (P, L) with n ≤ 6 (`out_misc.txt`). Harmless. |
| 6 | Cor 2.2: K for `P` ⟹ 1/3–2/3 for `P`; dominance-respecting `L` suffice (§2) | **HOLDS** (PROVEN). The dominance step is Zaguia's Lemma 7 (critical pair ⟹ `P ≥ 1/2`), checked against the source. |
| 7 | Prop 2.4: prefix/suffix properties fail exactly on strict-containment pairs; both hold iff semiorder (§2) | **HOLDS** (PROVEN, re-derived; "containment" here must be read as *strict*, which the proof does). EMPIRICAL: 0 failures over all 2 540 (poset, dominance-`L`) cases with n ≤ 6. Control: 6 774 failures for non-dominance `L`. |
| 8 | Semiorders = interval orders with no strict containment, in the canonical representation (Conventions) | **HOLDS** (PROVEN here, §3.3: a strict containment plus canonicity yields a 3+1, and conversely). |
| 9 | Prop 3.1 (exact interval form of `|S|`) and Cor 3.2 (a strict dominance step has `|S| ≥ 2`; case list for `|S| ≤ 1`) (§3.1) | **HOLDS.** Re-derived. EMPIRICAL: 0 mismatches against the cover-based count on all 143 990 ordered incomparable pairs with n ≤ 8, and 0 violations of Cor 3.2. |
| 10 | Claim K holds for every `L` of every non-chain interval order with n ≤ 8; fails on exactly 2 at n = 9 (O9a, O9b, with the quoted `L`); 26 (any `L`) / 24 (dominance) at n = 10; all contain 3+1, with 1–3 long intervals (§3.2–3.3) | **HOLDS**, reproduced exactly with independent code (`out_census_k.txt`, `out_props.txt`). My DP finds the **same** witness `L` for O9a and O9b as the doc quotes. |
| 11 | O9a/O9b: δ = 228/515 and 22/53; `P[[1,1]<[1,2]] = 0.655`; `S([2,3],[1,5]) = {[4,5],[5,6]}` (§3.3) | **HOLDS**, exact (135/206 = 0.6553). |
| 12 | §3.4: both n = 9 obstructions survive SL1/SL2 and duals; at n = 10, 16 of 24 posets and 20 of 29 `L` survive | **HOLDS.** Reproduced exactly (`out_sl.txt`), with my own implementation of the constraints from the mg-ce69 Thm 1.4 text. SL1 and SL2 re-derived (§3.4 below). |
| 13 | §4 Swap Ladder in interval terms: H1 ⟺ `l(x) ≤ l(b)` direction; dominance ⟹ `W = {b}`; containment ⟹ `W = {b} ∪ Z_right`; Cor 4.2 two-sided ladder | **HOLDS.** Re-derived. Cor 4.2's "some `(x,·)` is balanced" is right, because Zaguia's Thm 2 proof produces the balanced pair `(a, b_r)` with the **same** `a` (checked in the source). |
| 14 | §4 down-twin Doubling: `l(x)=l(y)`, `r(x)<r(y)`, unique minimal `b_1` of `Z` ⟹ `P[y<b_1] = 2P[y<x]` | **HOLDS.** It is mg-ce69 Lemma 1.5 with pivot `y` and `b_0 = x`. EMPIRICAL: 0 violations on 11 533 pairs with n ≤ 8. Control: 9 022 failures with `l(x) < l(y)`. |
| 15 | §0.6 / §5: T8, T13, T14, N12 are not interval orders; only 2+1 attains δ = 1/3 among indecomposable twin-free interval orders with n ≤ 9; min δ is 14/39 at n = 7 and 50/139 at n = 9 (zigzags); non-semiorder minimum 8/21 at n = 7 and 5/13 at n = 8, 9; the path semiorder gives 5/13 at n = 6 and 13/34 at n = 8 | **HOLDS**, all exact (`out_census_delta.txt`, `out_witnesses.txt`). The population is ordinal-indecomposable and twin-free; its counts 160 / 866 / 5 198 reproduce. 14/39 is also Saks's 1985 width-3 value, as Wikipedia cites it. |
| 16 | §5 table: C1, C2, C7 failure counts 31/169/934, 11/41/163, 1/1/3 | **HOLDS**, reproduced exactly. The **L1, L2 and Zaguia-Thm-3 rows were NOT reproduced** (UNVERIFIED by me, not refuted). |
| 17 | §1: Chan–Pak Thm 13.2 verbatim, §11.6 contents; Zaguia ×3 class lists; Gupta 2026; Wikipedia | **HOLDS.** Chan–Pak Thm 13.2 matches the arXiv v2 text word for word. |
| 18 | §1: Trotter 1997 §11 reproduces Brightwell for semiorders, then mentions only TGF and LEM cycles | **HOLDS** for the part I could read. The Trotter PDF is a scan whose right-hand page is cut at the spine. The proof skeleton the doc uses (left-endpoint labelling, `L` from `Prob < 1/3`, separations from above/below, `Λ₁ → Λ₃` swap, `|Λ₃|/t < 1/3`) is legible and matches §2. One sentence ("It is an …", before the LEM remark) is truncated: **UNVERIFIABLE**. |
| 19 | §7: Gaetz–Gao's generalised semiorders "stay (3+1)-free" (flagged unverified by the author) | **HOLDS in type A** (PROVEN here, §1.3): type-A generalised semiorders are exactly semiorders. So they do not cover O9a/O9b or any interval order with 3+1. Their proof is Brightwell's injection in root-system form (§1.3). |

**Net:** mg-afa4 is sound. It claims exactly what it proves. The literature label is right. The one inaccuracy is a harmless "equivalent" that should read "implies".

---

## 1. Literature status, redone (task item 1)

I did not reuse the author's list. I searched afresh (web search; arXiv full texts via `pdftotext`; author pages) for any statement or proof of 1/3–2/3 for interval orders, and for any statement that the case is open.

### 1.1 Sources opened and what they say

| source (opened by me) | interval orders? |
|---|---|
| Chan–Pak, *Linear extensions of finite posets*, arXiv:2311.02743v2, Thm 13.2 and §11.6 | Thm 13.2's list is verbatim as the doc quotes it; (3) is "semiorders [Bri89] (a concise proof was given in [Bri99, Thm. 2.3])". §11.6 "Interval orders and semiorders" treats only extremal counts `e(n,k)` and #LE. **No interval orders in the balance list.** |
| Brightwell's own research page (maths.lse.ac.uk/personal/graham/research-pos.html) | "In the paper below, it is proved for semiorders". Interval orders appear only in "Interval orders and LEM cycles" (with Fishburn and Winkler), about 1/2-majority cycles. **No claim for interval orders.** |
| Zaguia arXiv:1107.5626, 1610.00809, 2002.11604 (full text) | Known-class lists: automorphism, width 2, semiorders, bipartite, 5/6-thin. The word "interval" appears only as "real interval" or "interval = module". |
| Gaetz–Gao arXiv:2005.09719 (full text, §4) | Generalises Brightwell to "generalized semiorders" in Weyl groups; type A = semiorders (§1.3). |
| Olson–Sagan arXiv:1706.04985 (abstract); Eppstein arXiv:1302.5967 (abstract); Chen arXiv:1709.05753 and arXiv:2410.12494 (full text) | No mention of interval orders. 2410.12494 lists semiorders. |
| Gupta arXiv:2607.23926 (full text) | Verifies through n = 14; no occurrence of "interval order" or "semiorder". |
| Wikipedia, raw wikitext | Classes: width 2, height 2, ≤ 11 elements, 6-thin, series-parallel, N-free, semiorders, polytrees, 2026 preprint to 14. **No interval orders.** |
| Trotter, *New perspectives on interval orders and interval graphs* (1997), trotter.math.gatech.edu papers/103.pdf, scan p. 256–257 | Thm 11.4 (Brightwell) is for semi-orders. It is followed by "other special classes … height 2 … LEM cycles … interval orders having dimension at most two". The legible text makes no balance claim for interval orders. |
| Trotter, *Balancing pairs in partially ordered sets* (papers/86.pdf); BFT 1995 (papers/97.pdf); TGF 1992 (papers/82.pdf), full text | Brightwell cited for semiorders only. TGF's introduction: "does likewise for every nonlinear semiorder". Nothing on interval orders. |
| Web searches: "1/3-2/3 conjecture interval orders", "'interval orders' '1/3-2/3 conjecture' proof", "… 'remains open' OR 'is open'", "1/3–2/3 'interval order' 2024–2026" | No hit states or proves the interval-order case, and no hit calls it open. |

**Not accessible to me:**
- Brightwell 1989 (Springer paywall; academia.edu 403);
- Brightwell 1999 survey (Discrete Math. 201; no open copy found);
- Olson's 2025 AWM chapter and the MSU thesis (403 / restricted);
- the right-hand column of Trotter p. 257.

The 1999 survey is the one place a remark could hide. Chan–Pak, writing in 2023–2025 and citing that survey's Thm 2.3 specifically for **semiorders**, is strong indirect evidence that it contains no interval-order theorem.

### 1.2 Verdict on item 1

**NOT FOUND: HOLDS.** A known result mislabelled as open is the likeliest failure mode, and I looked for it specifically. Nothing surfaced: every list, survey and citing paper I opened stops at semiorders.
- "Open" remains **UNVERIFIABLE** (absence of evidence).
- The doc is careful here ("open as far as can be verified"; "No source says the case is open").

### 1.3 Gaetz–Gao in type A (PROVEN here; resolves the doc's §7 caveat)

In type A, a generalised semiorder is `C = W^A` with `A` an order ideal of the root poset `{e_i − e_j}`. There, `e_{i'} − e_{j'} ≤ e_i − e_j` iff `[i', j'] ⊆ [i, j]`. The poset has `p_i < p_j` (`i < j`) iff `e_i − e_j ∉ A`, so the comparable pairs are closed under **enlarging** the index interval.

Such a poset is (3+1)-free. Take `a < b < c` and `d` incomparable to all three, with indices `i_a < i_b < i_c`:
- `i_d ≤ i_a` gives `[i_d, i_b] ⊇ [i_a, i_b]`, so `d < b`;
- `i_a < i_d < i_b` gives `[i_d, i_c] ⊇ [i_b, i_c]`, so `d < c`;
- `i_d ≥ i_b` gives `[i_a, i_d] ⊇ [i_a, i_b]`, so `a < d`.

Each case is a contradiction. 2+2 is excluded the same way. So the type-A class is exactly the semiorders (Gaetz–Gao's Def. 4.1 direction is in their text).

Worth recording for the programme: their proof of Thm 4.4 is Brightwell's injection. Lemma 4.5 is the swap `Λ₃ ↔ Λ₁`. Lemma 4.6 asks for a simple root `α_i` (an `L`-consecutive pair in the natural labelling) with **at most one** `β` (at most one separator). So Lemma 4.6 is exactly **Claim K for the natural labelling**. That is the lemma KSBFT-T shows fails for interval orders at n = 9. The obstruction the doc found is precisely the step that is type-dependent even in Gaetz–Gao.

---

## 2. Is a proof claimed or hidden? (task item 2)

No. I read every section for a statement which, if PROVEN, would imply 1/3–2/3 on interval orders:
- **Cor 2.2 (K ⟹ 1/3–2/3):** a conditional; K is refuted in §3.3.
- **Cor 4.2:** gives a balanced pair only when both `Z_left` and `Z_right` are chains. That is a special configuration, not all interval orders.
- **§4 Doubling / Lemma 2.1 of mg-cfba:** constraints on a counterexample, not a contradiction.
- **§6:** explicitly CONJECTURED directions.

So there is no claimed new theorem. I still stress-tested the one statement that is new-ish and general, Thm 2.1, on the ticket's witnesses (T8, Q_m, the mg-7bfc hosts, random interval orders; #4 above).

**Side result for the programme (EMPIRICAL, `out_props.txt`).**
- Among the witnesses, the interval orders are P9, Q_0, Q_4, Q_14, A14 = attach_both(F_20,8), attach_low(F_12,8), attach_low(F_16,10) and F_12. (T8, T13, T14, N12 and the double hubs contain 2+2.)
- **Claim K holds on every one of them.** By Cor 2.2 this is a probability-free certificate of 1/3–2/3 for those posets. Their δ is already known exactly, so it adds nothing to the record.
- K fails **often** in the targeted family "unit staircase + 1–3 long intervals" at n = 10–13: 547 of 6 634 labelled constructions have a bad dominance-respecting `L` (constructions, not isomorphism classes).

So K's failure is not a small-n accident. The doc's "sparse" is correct only as census density: 26 of 201 607 at n = 10.

---

## 3. Line-by-line on the PROVEN parts

### 3.1 Thm 2.1

**(a)**
- With no balanced pair, each incomparable pair has exactly one orientation above 2/3, and comparable pairs have P = 1. So `≺` is a tournament extending `P`.
- A 3-cycle needs the three events `x<y`, `y<z`, `z<x` to have probabilities summing above 2. No linear extension satisfies all three, so the sum is ≤ 2.
- Transitive tournament ⟹ linear order. **HOLDS.**

**(b)** Fix `λ ∈ Λ₁`.
- If some `w` strictly between `a` and `a'` had `a < w`, pick a cover `a ⋖ c ≤ w`. Then `c` is also strictly between them: after `a` since `c > a`, before `a'` since `c ≤ w`.
  - `c < a'` would force `a < a'`;
  - `c > a'` contradicts position;
  - so `c ∥ a'`, `c ∈ S`, which is impossible in `Λ₁`.
- Dually nothing between is below `a'`.
- So the transposition of `a` and `a'` is a linear extension in `Λ₃`, and the map is injective. Hence `P(Λ₂) ≥ 2P[a<a'] − 1 > 1/3`.
- For `S = {z}` with `a ⋖ z`, `Λ₂ ⊆ {z before a'}`. Then `P[z<a'] > 1/3` ⟹ `> 2/3` ⟹ `z ≺ a'`, and `a ≺ z`. This contradicts `L`-consecutiveness. **HOLDS.**

### 3.2 Prop 2.4 and Cor 3.2

**Prop 2.4.**
- In `down(z) = {c : r(c) < l(z)}`, a violation "`y` before `x`, `x ∈ down(z)`, `y ∉ down(z)`" forces `x ∥ y` and `r(x) < l(z) ≤ r(y)`.
- Dominance-respect then rules out `l(y) ≥ l(x)`. So `y` strictly contains `x`.
- The converse uses the canonical point `r(x)+1 ≤ r(y)` as some `l(z)`. **HOLDS.**

**Cor 3.2.**
- With `α, β ≥ 1` and `ρ(r_i) ≥ r_i + 1`, a step with `l_i < l_{i+1}` and `r_i < r_{i+1}` has `A_i ≥ 1` and `B_i ≥ 1`.
- The remaining cases give the three listed forms: `B_i = 0` when `l_{i+1} ≤ l_i`, and `A_i = 0` when `r_{i+1} ≤ r_i`. **HOLDS.**
- Note: the doc's "containment" includes weak containment (`l` equal). Such pairs are also dominance pairs, so the two classes overlap. This is harmless.

### 3.3 Semiorder ⟺ no strict containment (canonical form)

- **(⟹ 3+1 exists)** If `l(x) < l(y)` and `r(y) < r(x)`, canonicity gives:
  - `a` with `r(a) = l(y) − 1 ≥ l(x)`;
  - `c` with `l(c) = r(y) + 1 ≤ r(x)`.
  
  Then `a < y < c` and `x` is incomparable to all three: a 3+1.
- **(⟸)** Conversely, a 3+1 `a<y<c ∥ x` forces `l(x) ≤ r(a) < l(y)` and `r(y) < l(c) ≤ r(x)`. **HOLDS.**

### 3.4 SL1 / SL2 (used in §3.4 of the doc)

**SL1.**
- In a counterexample, `b ≺ x` means `t_0 = P[x<b] < 1/3`.
- The Swap Ladder steps are non-increasing, so each is ≤ `t_0 < 1/3`.
- If `x ≺ b_m`, the cumulative law would jump from `< 1/3` to `> 2/3` in steps `< 1/3`. That passes through `[1/3, 2/3]`, which is impossible. **HOLDS.**

**SL2.**
- If the chain bottom exhausts `W` and `b ≺ x`, then SL1 gives `P[x<b_m] < 1/3`.
- The last step `P[b_m < x] ≤ t_0 < 1/3` then makes the total law below 1. **HOLDS.**

### 3.5 Zaguia and Fishburn uses, checked against source (task item 3)

| use | source text | verdict |
|---|---|---|
| Good pair: `D(a) ⊆ D(b)`, `U(b)∖U(a)` a chain, `P(a≺b) ≤ 1/2`, in `P` or its dual (§4) | 1610.00809 Def. 1, verbatim | **HOLDS** |
| Thm 2: a good pair ⟹ a balanced pair; the balanced pair is `(a, b_r)` with the same `a` (used in Cor 4.2 as "some `(x,·)`") | proof of Thm 2, §2: `q_j` ladder and `r` chosen so `q_r > 1/3`, contradiction ⟹ `(a, b_{r−1})` or `(a, b_r)` balanced | **HOLDS** |
| Lemma 7: critical pair ⟹ `P ≥ 1/2` (Cor 2.2, Prop 2.4 "the swap gives `P ≥ 1/2`") | Lemma 7, verbatim | **HOLDS** (orientation: `D(x) ⊆ D(y)`, `U(y) ⊆ U(x)` ⟹ `P(x≺y) ≥ 1/2`) |
| Thm 3 (i)–(iii) configurations certify balance; Brightwell's semiorder pair is (i) (§5) | Thm 3 and "Brightwell [2] proved that every semiorder has a pair (x,y) satisfying condition (i) of Theorem 3" | **HOLDS** |
| "Partial coverage: N-free interval orders (Zaguia 2012)" (§0.1) | 1107.5626 proves N-free (Hasse diagram) | **HOLDS** (a sub-case, as stated) |
| Fishburn canonical representation: endpoints `1..h`, every point is a left and a right end, `x<y ⟺ r(x)<l(y)`, the multiset is a complete invariant (Conventions) | Fishburn 1985 (not re-read); **re-derived computationally** | **HOLDS.** `eng.recanon` builds the representation from down-set ranks for every interval order with n ≤ 9. It returns exactly the generated multiset (31 240 of 31 240 at n = 9), and distinct multisets give non-isomorphic posets. |

---

## 4. What I did NOT do

- Did not read Brightwell 1989 or Brightwell 1999 (paywalled). The right-hand column of Trotter p. 257 is truncated in the scan.
- Did not reproduce the §5 rows L1, L2 and Zaguia-Thm-3 (1/1/3/13), nor `bwstats`/`bwinc`/`onesided`/`gaps`/`bwrefine`/`bwrules`/`tight` (§3.2 "structure" and "ruled-out routes"). These are EMPIRICAL side observations, not load-bearing. They remain the author's, unaudited.
- Did not test the author's random-sample claim (1 560 random interval orders with n = 10–30, none bad). My targeted family (§2) shows the random negative is uninformative, which the doc itself says.
- Did not run anything at range ≥ 8 beyond the named hosts (A14 has range 8). No case census was extended, per the ticket rule.
- Candidates ruled out: none of the author's PROVEN statements failed. The only candidate "known result mislabelled open" (Gaetz–Gao's generalisation) is ruled out by §1.3.

## 5. Files (`code/audit_ksbft_5ecf/`)

| file | output | content |
|---|---|---|
| `eng.py` | — | independent engine (generator, canonical form, covers, separators, bad-`L` DP, exact laws) |
| `controls.py` | `out_controls.txt` | laws / badL vs brute force with planted controls; Prop 3.1, Cor 3.2 |
| `census_k.py` | `out_census_k.txt` | Claim K, all interval orders with n ≤ 10 |
| `census_delta.py` | `out_census_delta.txt` | δ census and C1/C2/C7, n ≤ 9 |
| `witnesses.py` | `out_witnesses.txt` | named witnesses, Thm 2.1(b), random interval orders, control |
| `props.py` | `out_props.txt` | Prop 2.4; n = 10 shape; K on bounded-range witnesses and the staircase family |
| `sl.py` | `out_sl.txt` | §3.4 Swap-Ladder survival |
| `misc.py` | `out_misc.txt` | §4 Doubling; the §0 "equivalent" wording |
| `run_all.sh` | — | regenerates and asserts everything |
