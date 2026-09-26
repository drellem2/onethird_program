# AUDIT of mg-0b78 — `docs/KSBFT-P1-walled-routes-under-bounded-range.md`

`mg-af00`, 2026-09-26. Independent audit, fresh context, not the author. **No edits to KSBFT-P1,
STATE.md or any other doc.** Instrument: `code/audit_ksbft_af00/` (`sh run_all.sh`, about 70 s,
one process, exact, seeded). It shares no code with `code/ksbft_p1_walled_0b78/`.

Verdicts: **HOLDS** / **BROKEN** / **OVERSTATED** / **UNVERIFIABLE**. Marks on my own statements:
PROVEN / EMPIRICAL / CONJECTURED, as in the audited doc.

---

## 0. Verdict

**Nothing that carries weight in the document is BROKEN, and its main conclusion stands.** Bounded range revives
no walled route into a proof. Every mathematical result in §5 HOLDS on re-derivation:

- Prop 3.1;
- Lemmas 5.1 and 5.2;
- Props 5.4, 5.5 and 5.6;
- the κ(4) ≤ 1/18 exhibit;
- Example 5.7.

Prop 5.5's closed form was also brute-forced with zero mismatches.

**One classification is BROKEN: row B2 (Route B, Hyp A), "TRANSFORMED".** The doc says that on
`Π_D` Lemma 2.3's floor `c(D)` makes Hyp A's small-γ tail `γ < c(D)` empty. That is a misreading
of γ. In F25, γ is the **deficit below 1/3** (window `(0, 1/3 − δ_KL)`). Small γ means δ close to
1/3, and bounded range says nothing there. Lemma 2.3 bounds pair balances from below, and so caps
γ from **above**. Row B2's final verdict, SURVIVES, is unaffected. The tally therefore becomes
**14 DISSOLVE / 7 TRANSFORMED / 25 SURVIVE**, not 14/8/24.

**Eight items are OVERSTATED.** All are minor, and none changes the net verdict:

1. §0's "every DISSOLVES witness has range Θ(n)":
   - A4 has no witness;
   - `C_2 ⊕ A_k ⊕ C_2` at `k = √n` has range `Θ(√n)`.
2. A28 "SURVIVES for D ≥ 5". The `(L*)` refuters have ranges 6, 8, 8, 9, so on this evidence
   `(L*)` survives only for D ≥ 6.
3. §3.2 relabels KSBFT-A's EMPIRICAL "only `(2+1)` and its ordinal sums sit at 1/3" as "PROVEN for
   n ≤ 11".
4. §0 says that "routes aimed at δ died on thin or structural witnesses". The doc's own A11/A12
   (δ-direct via mg-48ab Thm 5.2) died on `C_n ⊔ C_n`, which has range n.
5. §0/§4 say "all but three needs supplied". §4's own A5 row gives a fourth "no".
6. §3.3 says "each quantiser is an injection with bounded fibres". The KSBFT-M prefix certificate
   is not.
7. §5.5(b) says "bounded range's quantiser cannot act on the Stanley defect". (QD_D) is a ratio of
   two set sizes, and mg-dcae itself says the injective route is not blocked. §5.5 below exhibits a
   sub-family where the quantiser does act.
8. §0's paraphrase of Ex. 5.7 as "positive reweighting".

**Flashiest claims, attacked first:**

- *"No walled route is revived into a proof"* (§0 Net): HOLDS. No route's revived need is
  supplied at the constant the route needed.
- *Prop 5.5, `κ(D) ≤ 1/(D²−1)`*: HOLDS, re-derived and brute-forced.
- *The §3 pattern "H dissolves exactly the obstructions to non-δ targets"*: HOLDS as a description
  of the listed rows, with the A11/A12 exception the doc itself makes the subject of §5.

---

## 1. Per-claim table

"re-derived" means I redid the proof by hand. "instr." means my instrument re-computed it. "cited"
means I checked the cited statement in its source and its hypotheses.

### 1A. §3.1, Proposition 3.1 (the seven spread quantities)

| # | claim (P1 location) | verdict | how checked |
|---|---|---|---|
| 1 | (1) `\|σ(x)−e(x)\| ≤ π(x)` | **HOLDS** | F1 (KSBFT-C:134) re-read; both positions lie in `[d+1, d+1+π]` |
| 2 | (2) `Var(pos x) ≤ π(x)²/4` | **HOLDS** | Popoviciu on an interval of length π |
| 3 | (3) `inv_e ≤ nD/2`; `E inv_e < nD/6` if frozen w.r.t. majority order | **HOLDS** | F3/F4 (KSBFT-C:154–160): at most `m ≤ nD/2` incomparable pairs, each flipped w.p. `< 1/3` |
| 4 | (4) `d ≤ D/(n−1)` | **HOLDS** | `(nD/2)/C(n,2)` |
| 5 | (5) `log₂ e(P) ≤ n log₂(D+1)` | **HOLDS** | F6. Independently: insert elements along a linear extension, each with `≤ π+1` slots (the Lemma 5.2 argument) |
| 6 | (6) support is **exactly** `π(x)+1` consecutive slots | **HOLDS** (statement). **Proof step defective, repaired here** | See §2.1. "A log-concave sequence has no internal zeros" is false for the inequality Stanley proves: `(1,0,0,1)` satisfies `N_i² ≥ N_{i−1}N_{i+1}` (instr. control). Repair: P[I(x)] has a down-set of every size j, so Lemma 5.1 gives `N_{d+1+j} ≥ L(J)R(J) > 0`. Instr.: 0 violations over 5 530 posets |
| 7 | (7) flip probability `≥ c(D) ≥ 2^{1−2D}` | **HOLDS** (cited) | KSBFT-F Lemma 2.3 (line 159) says exactly this, for every incomparable pair |

### 1B. §0 and §2, triage claims

| # | claim | verdict | how checked |
|---|---|---|---|
| 8 | Witness ranges: `C_m ⊔ C_n` = max(m,n); antichain n−1; staircase m; `D_k` 2k−2; `C_2⊕A_k⊕C_2` k−1; Z_m, fence, N, `(2+1)^{⊕m}`, `V⊕V` = 2; `W*` 3; `G(n,g)` 2g−2 | **HOLDS** | Growth laws re-derived by hand. Example: the bottom of one 2-chain in `D_k` is incomparable to all `2k−2` others. P1's transcript `out_ranges*.txt` read line by line |
| 9 | Finite-witness ranges: (L*) 8, 8, 6, 9; (F)&(M♯) 5, 5, 6, 7, 7 | **HOLDS** | Re-decoded with my own closure (`out_subfamily_af00.txt`). Bitmasks spot-checked against the source transcripts (`code/audit_5cba`, `code/lstar_reaudit_5e82`, `code/um_frontier_b417`) |
| 10 | §0: "Every DISSOLVES is an obstruction whose witness has range Θ(n)" | **OVERSTATED** | A4 DISSOLVES with witness "none": the target became true. A18's `C_2⊕A_k⊕C_2` at `k=√n` has range `√n − 1 = Θ(√n)`. Both still meet §1's actual definition ("range → ∞, **or** the failing hypothesis becomes true"), so no verdict moves. Only the headline's "Θ(n)" is wrong |
| 11 | §0: "Every SURVIVES is structural, range ≤ 3, or finite" | **HOLDS**, with one ambiguity | Checked all 24 labels against their witnesses. Ambiguous: C6 "no consumer" lists the antichain (range n−1) as witness. It survives only if read as structural (sign-blindness of the numerator), which the row does not say |
| 12 | A5: `δ > 0.2764` for `D ≤ 3471` via Thm 1.3″ | **HOLDS** (cited) | KSBFT-H:23–25, 172–173; audit mg-f218 items 2, 2‴. Note that `θ₀ = 0.2764 − C_BFT`, so the "> 0.2764" is exactly the θ₀ cap |
| 13 | A9: `1 − λ_std ≤ 4nD/(n²−1)` on `Π_D` | **HOLDS** (cited) | KSBFT-F Prop 5.1 (line 328), including its row-5 normalisation caveat |
| 14 | A13: on `Π_D`, `β ≥ c(D)` excludes `β ≡ 10⁻¹⁰⁰` | **HOLDS** | β are pair balances (attempt-index:30). Lemma 2.3 applies |
| 15 | A17/A18/A22/A25/C3/C6/D1/E3 "auto" targets | **HOLDS** | F3/F4/F6 arithmetic. For C3, `n log₂(D+1) ≤ c log₂ n!` needs `n ≳ 2.7(D+1)^{1/c}`, which is consistent with "≳" |
| 16 | **B2: "TRANSFORMED — on Π_D the small-γ tail γ < c(D) is empty"** (also §4 row B2, "the γ-floor c(D) does not reach γ_crit") | **BROKEN** | See §2.2. The final "SURVIVES" HOLDS |
| 17 | B2: "Hyp A fails at every γ ≤ 1/2 on its constants alone (γ_crit ≈ 27–936)" | **HOLDS**, with a caveat | F25:192–236. `γ_crit = (512w²/((c₅*)²c₆))^{1/3}`. With F25's bounds `c₅* < 1`, `c₆ < 1/8`, `w ≥ 1` this gives `γ_crit > 16`. The Hyp-A window is only `(0, 0.057)`; "γ ≤ 1/2" is harmless overreach. F25 itself hedges `w ≥ 1` ("may be fractional but not vanishingly small") |
| 18 | B1: `{π ≤ D} ∩ PPF_n` is an up-set under refinement | **HOLDS** | Adding relations only removes incomparabilities |
| 19 | E2: (T)/(IB) on `Π_D` ⟺ the conjecture on `Π_D`, past N(D,ε) | **HOLDS** (cited) | KSBFT-F Prop 4.2 (line 281) re-read; proof checked |
| 20 | A28: "SURVIVES on Π_D for D ≥ 5" | **OVERSTATED** (off by one for half the row) | The `(F)&(M♯)` refuters have range ≥ 5, so D ≥ 5 is right for them. The `(L*)` refuters have ranges 6, 8, 8, 9, so on the listed witnesses `(L*)` is refuted on `Π_D` only for D ≥ 6. No consequence: the row is moot |
| 21 | Counts 14/8/24/6/2 over 54 entries (48 table lines) | **Arithmetic HOLDS; content becomes 14/7/25** | Re-tallied every label. Because of #16, B2 moves from TRANSFORMED to SURVIVES. "Counts of obstructions" is loose: E1 carries L1b/L2/L3 "auto" and E3 carries 0b96, and none of these is tallied |

### 1C. §3.1′–§3.3, the pattern

| # | claim | verdict | how checked |
|---|---|---|---|
| 22 | Obs 3.1′ (PROVEN by inspection): every DISSOLVES witness makes one of the seven quantities large | **HOLDS** | Row by row. The E2 surrogate (chain + isolated z) makes item 6 large, and the doc does not list it. That is harmless |
| 23 | Obs 3.1′: "every DISSOLVED route's own target is one of the seven being small, so supplied at f(D)" | **HOLDS**, with a note | This is true if A12's target is read as (B) (auto via F5). A12's own intermediate need, a Stanley stability at `c(D)`, is **not** supplied (§4 row A12). The doc says so in §4 but not in §3.1 |
| 24 | §3.1: Prop 3.1's constants are "on the useless side once D ≥ 7" | **OVERSTATED** (for the density items) | Items 3–4 are `n`-dependent: `d ≤ D/(n−1)` beats `ε_dem ≈ 1/50` once `n ≥ 50D`. The doc's own §4 says "useful only at n ≥ 50D". "True and useless" should read "true, and useless at computable n" |
| 25 | §3.2: "only posets at δ = 1/3 are (2+1) and its ordinal sums, **PROVEN** for n ≤ 11 by exhaustion (KSBFT-A)" | **OVERSTATED** (label) | KSBFT-A:19–22 labels it **EMPIRICAL** ("ordinal sums **with chains**"), and so does audit mg-6b81 item 4a ("HOLDS (EMPIRICAL)"). The enumeration is complete (46 749 427 = A000112 at n = 11), so "computer-exhaustive for n ≤ 11" would be defensible. Promoting it to PROVEN is a relabel that no audit made. Gup26 extends the statement to n ≤ 14 |
| 26 | §3.2 and §0: "the routes aimed at δ itself died on thin witnesses (range ≤ 3) or structural failures" | **OVERSTATED** | A11/A12 is δ-direct (the table's target column: "δ-direct via Thm 5.2"), and its killing witness `C_n ⊔ C_n` has range n. The doc concedes this in §0.4/§5.1, but the headline sentence and §3.2's list omit it. D2 (δ-direct) is unexamined. The **CONJECTURED** tag on "future δ-direct obstructions will be thin" is correct |
| 27 | §3.2: "C_BFT is the limit of the Fibonacci centre pair" | **HOLDS** as EMPIRICAL (N ≤ 81, KSBFT-A:208) | The doc does not mark it PROVEN. My Z_m instrument confirms the related "least deficit → 1/φ" (0.618056 at m = 14), EMPIRICAL |
| 28 | §3.3: the six range-quantisers are "each an injection whose fibres are bounded by the number of positions an element can hop" | **OVERSTATED** (not marked PROVEN) | True of Lemma 3.1/F7, Lemma 2.3, Lemma W, `d₁ ≥ 1/(D+1)` and Lemma R. **Not** true of KSBFT-M's prefix certificate, which is a window containment ("every size-s ideal lies inside any size-(s+D) ideal") plus an exact convex combination. It involves no injection |

### 1D. §5, the deep dive

| # | claim | verdict | how checked |
|---|---|---|---|
| 29 | Ma–Shenfeld k = 1: interior equality ⟺ companions incomparable, and equality forces `N_{i−1}=N_i=N_{i+1}` | **HOLDS** (cited) | Attempt-index:28 records a verbatim check of MS Thm 1.3(iii) and Rem. 1.8 (this is also Shenfeld–van Handel's k = 1 theorem). Instr. consistency: 19 354 interior equalities over 5 530 posets, **0 not flat** |
| 30 | mg-48ab Thm 5.2: full-support flat law ⟹ δ ≥ 1/3 | **HOLDS** (cited). My probe of it is **vacuous** | Attempt-index:28: "proof independently verified, non-circular". My instrument found 3 952 full-support-flat elements and 0 with δ < 1/3, but **no poset on n ≤ 8 has δ < 1/3 at all**, so the probe cannot fail. I report it as a non-test |
| 31 | **Prop 5.4**: (QD_D) ⟹ (FLAT_D) | **HOLDS** (given #29, #30) | Re-derived. Near-log-linearity at every interior index plus (QD_D) forces Stanley equality there. MS then gives flat triples, which overlap and cover the support. `π ≥ 2` gives `W ≥ 3`, and Thm 5.2 applies. **Wording:** §0's "over a window of ≥ 3 slots" must mean *the full support*. A sub-window reading is false, because a flat partial run does not give Thm 5.2 (that is mg-48ab Prop 5.3's separate, partial-run statement) |
| 32 | **Prop 5.5**: `κ(D) ≤ 1/(D²−1)` via `C_2 ⊔ C_D`, and no D-uniform (QD) | **HOLDS** | See §2.3. Closed form re-derived; brute force over m ≤ 4, n ≤ 7 at every interior j gives **0 mismatches**; D = 2..8 prints `1/(D²−1)` exactly, with range D |
| 33 | κ(4) ≤ 1/18 exhibit (range-4, n = 8) | **HOLDS** | Instr.: range 4, `N(x=5) = (0,0,0,15,18,19,19,19)`, deficit `1/18` at i = 6 |
| 34 | §5.3 table (floors 1/3, 1/8, 1/15, 1/18 flat in n) | **EMPIRICAL**, correctly labelled; not re-run | Scope stated in the doc ("random, not exhaustive"). Its negative control is described |
| 35 | **Lemma 5.1** (local decomposition over down-sets of `P[I(x)]`) | **HOLDS** | Re-derived, including both directions of "K is an ideal ⟺ J is down-closed in I(x)". Instr.: 0 mismatches on exhaustive labelled n ≤ 6 plus 300 random n = 7, 8. The planted false variant (sum over **all** j-subsets) FIRES 1 795 times |
| 36 | **Lemma 5.2**: `L(J∪z)/L(J) ∈ [1, π(z)+1]`, R reversed; box `[(D+1)^{−D}, (D+1)^{D}]` | **HOLDS** (with slack) | Re-derived. The phrase "the chain has length ≤ D" is loose: the path `J → ∅ → J′` has two legs, each of length ≤ D, and that is what the bound uses. **Sharpening, PROVEN:** `x ∈ inc(z)` is never in K, so the ratio lies in `[1, π(z)]`. Instr.: 0 exceedances of π(z). The planted `π(z)−1` bound FIRES 2 770 times |
| 37 | Local type τ is finite per D, and "equality index depends only on (τ, i)" | **HOLDS** | Re-derived. The companion before x is a maximal element of D↓ whose successors avoid J; the companion after x is a minimal element of up(x) whose predecessors in I(x) lie in J. τ must record the *set* (not multiset) of distinct boundary subsets, which the doc says ("bounded number of distinct subsets") |
| 38 | **Prop 5.6** (compact reduction) | **HOLDS** | F is 0-homogeneous in L and in R separately, and continuous and positive on the box. There are finitely many (τ, j). The "⟺" is definitional plus finiteness; the "if" is compactness. **Note:** the reduction is sound but thin. All of the difficulty sits in `S̄_τ`, as §5.5 says |
| 39 | **Example 5.7** | **HOLDS** | Instr.: `(3,2,3)`, `4 < 9`. The weights meet every Lemma 5.2 constraint at D = 2. The §0 paraphrase "positive reweighting does not preserve Stanley" is **OVERSTATED**: the example is an unrealised box point, not a reweighting of a realised poset |
| 40 | §5.5(b): "(QD_D) needs a lower bound on a signed quantity; bounded range's only quantiser works on unsigned ones" | **OVERSTATED** (not marked PROVEN, but used as the "precise obstruction") | See §2.4 |
| 41 | (WMS_D), (QD_D), §5.6's `δ ≥ C_BFT + η(κ)` | CONJECTURED, correctly labelled | — |

### 1E. §4 and §6 bookkeeping

| # | claim | verdict |
|---|---|---|
| 42 | §4 summary / §0.3: "supplied in existence form except three" | **OVERSTATED**. §4's A5 row reads "At 1/3: no", which is a fourth. It can be excused only because A5 at 1/3 is SURVIVES, not revived, and §4's header says "each revived route" |
| 43 | §6 candidates ruled out (1)–(6) | (1) **HOLDS** only on the corrected γ reading: Hyp A fails on the whole window by F25's constants, and bounded range does not touch small γ. (2)–(5) HOLD. (6) HOLDS (Prop 5.5) |
| 44 | §6 disclosures (sub-agent-sourced wording, two inferred witnesses, MS not re-read) | **HOLDS**. They are honest and complete as far as I checked. `V⊕V = (2+1)⊕(2+1)` gives e = 9 and δ = 1/3, which confirms the inference |

---

## 2. Details

### 2.1 Prop 3.1(6), the support claim

The doc's proof reads: "`N_i(x)` is log-concave (Stanley). A log-concave sequence has no internal
zeros." Stanley proves `N_i² ≥ N_{i−1}N_{i+1}`, and that inequality allows internal zeros:
`(1,0,0,1)` satisfies it at both interior indices. "No internal zeros" is a *separate* clause in
the usual definition of log-concavity, and here it has to be proven. **Repair (PROVEN):**

1. `P[I(x)]` has down-sets of every size `0..π(x)`: take prefixes of any of its linear extensions.
2. Lemma 5.1 then gives `N_{d+1+j} ≥ L(J)R(J) > 0` for each `j`.

The statement stands, and so does its use in §5.1 (the support equals the window).

### 2.2 Row B2 is BROKEN: the direction of γ

F25 §0.1 (`one_third_width_three/docs/compatibility-geometry-F25-hypothesis-A-constants-audit.md`)
states Hyp A for `γ ∈ (0, 1/3 − δ_KL)`, and notes that "for `γ ≥ 1/3 − δ_KL` Kahn–Linial excludes
counterexamples". So a γ-counterexample has `δ ≤ 1/3 − γ`. Small γ means **nearly balanced**, and
large γ means very unbalanced.

KSBFT-F Lemma 2.3 gives `min(p, 1−p) ≥ c(D)` for every incomparable pair, hence `δ ≥ c(D)`. That
excludes γ-counterexamples with `γ > 1/3 − c(D)`, the **large**-γ end. Kahn–Linial already
excludes that end, since `c(D) ≤ 2^{1−2D}·(…) ≪ δ_KL`.

It does **not** empty `γ < c(D)`: a range-D poset with δ = 1/3 − 10⁻⁹ is not excluded by any
standing fact. The row's "TRANSFORMED" step and §4's "the γ-floor c(D) does not reach γ_crit"
therefore rest on reading γ as a pair balance.

**Consequence.** The row should be plain **SURVIVES**, witness-free and structural: F25's `1/γ` is
a proof-architecture fact. Every downstream statement survives: B2 "SURVIVES", §5.1's elimination
of B2, and §6 candidate 1.

**Does bounded range act on B2 at all?** I did not find any way. Theorem 1.3″ raises the δ floor
only to `C_BFT + θ₀`, which again acts at the large-γ end.

### 2.3 Prop 5.5, re-derived

- For `P = C_m ⊔ C_n` and `x = u₁`: x at position `1+j` forces `v₁…v_j` before x. The rest
  interleave, so `N_{1+j} = C(n−j+m−1, m−1)`.
- Put `t = n+m−1−j` and `k = m−1`. Then
  `N_{1+j}²/(N_j N_{2+j}) = [(t−k+1)/(t+1)]·[t/(t−k)] = t(t−m+2)/((t+1)(t−m+1))`.
- The numerator minus the denominator is `m−1`, which gives the stated formula.
- `m = 2`, `n = D`, `j = 1` gives `1/(D²−1)`, at interior index 2 (support `1..D+1`, D ≥ 2). The
  range is `π(u₁) = D`.
- Within this family `m = 2` is optimal: with `j = 1` and `m = n = D` the deficit is `1/(2D−1)`.
- Instrument: 0 mismatches over m ≤ 4, n ≤ 7 at every interior j.

### 2.4 §5.5(b): the quantiser is not blocked by "signedness"

(QD_D) is `|L_i × L_i| ≥ (1+κ)|L_{i−1} × L_{i+1}|`, a **ratio of the sizes of two sets**. That is
exactly the form an injection `L_{i−1}×L_{i+1} → L_i×L_i` with a `κ`-fraction surplus would
prove. The "defect ∉ #P" results forbid an exact combinatorial interpretation of the difference;
they do not forbid such an inequality. mg-dcae says so itself (attempt-index:29: "injective route
**not** blocked"), and P1 quotes that caveat before overriding it.

**A sub-family where bounded range's quantiser does control the deficit (PROVEN here, narrow; instr.
`out_subfamily_af00.txt`).** Take the following configuration:

- `I(x) = {a < b}`;
- `a` is above all of `D↓`, so the L-factor is 1;
- `b`'s successors in `up(x)` are all of `up(x)` except one minimal element `d` that is
  incomparable to `a` and `b`.

Let `f` be the position of `b`'s first successor in a uniform extension of `up(x)`. Then
`f ∈ {1, 2}`, and `P[f = 2] = q := P[d first]`. The deficit at the interior index equals
`2E[f]²/(E[f²]+E[f]) − 1 = q²/(1+2q)`.

Lemma 5.2 applied inside `up(x)` gives `q ≥ 1/(π(d)+1) ≥ 1/(D+1)`. So in this sub-family
`κ ≥ 1/(3(D+1)²)`: (QD_D) holds there *because* of a quantised probability. The instrument
confirms the formula exactly for `up(x) = {d} ⊔ C_k`, `k = 1..6`. The deficit there is
`1/((k+1)(k+3)) = 1/(D²−1)` at range `D = k+2`, the same value as Prop 5.5, so this family attains
Prop 5.5's bound.

This does not prove (QD_D). It shows that §5.5(b)'s "the one mechanism ... does not apply to the
Stanley defect" is too strong. §5.5(a), the closure of realised weights, remains a genuine
obstruction, and (WMS_D) is a fair statement of what is missing.

---

## 3. Controls

All controls are in `out_check_af00.txt`. `run_all.sh` asserts every one.

- **Positive.** Prop 5.5 brute force reproduces the closed form, and the κ(4) exhibit reproduces
  1/18. `δ(2+1) = 1/3`, `δ(A_2) = 1/2`, `δ(N) = 2/5`. A planted non-contiguous support is detected.
- **Negative.**
  - Lemma 5.1 summed over all j-subsets FIRES 1 795 times.
  - Lemma 5.2 with bound `π(z)−1` FIRES 2 770 times.
  - `(1,0,0,1)` passes the weak Stanley test, which shows why the Prop 3.1(6) proof step needs
    repair.
- **Vacuous, reported as such.** The Thm 5.2 probe (#30) cannot fire at n ≤ 8.

---

## 4. What I did NOT do

- I did not re-read Ma–Shenfeld or mg-48ab's Thm 5.2 proof. I rely on the attempt-index record
  that both were verified, and my probe of Thm 5.2 is vacuous.
- I did not open the 28 attempt-index sources to re-check each row's *obstruction wording*. I
  checked witnesses and ranges, and the sources of rows B2 (F25), A5 (KSBFT-H), A13 (61bb), E2/A9
  (KSBFT-F) and §3.2 (KSBFT-A).
- I did not re-run P1's `stanley_gap.py` table (#34).
- I did not examine B6 or D2, which P1 also left unexamined, or paddings of the finite witnesses
  into `[7, D]`.
- I did not search for a counterexample to (QD_D) beyond §2.4's sub-family.
- The A28 ranges come from bitmasks. I re-decoded them, but I matched only two of them to the source
  transcripts by grep.

**Candidates ruled out as failure modes of P1:**

- **The ranges could be mis-decoded.** Ruled out: independent closure, identical ranges.
- **The Prop 5.5 closed form could be off by an index.** Ruled out: brute force.
- **Lemma 5.1 could need all subsets, not only down-sets.** Ruled out: that variant fails.
- **Lemma 5.2's `+1` could be wrong.** Ruled out: it is not wrong, only slack.
- **The κ(4) exhibit could have range > 4.** Ruled out: its range is 4.
- **Row A5's 0.2764 could be unsupported.** Ruled out: it is audited in mg-f218.
