# AUDIT of mg-6b81 (KSBFT-M, `docs/KSBFT-M-margin-induction.md`): mg-f889

Auditor: an independent polecat with fresh context. I am not the author. The subject is
`docs/KSBFT-M-margin-induction.md` and `code/ksbft_m_margin_6b81/` as of `9a0db59`/`c261360`.
The KSBFT PDF was **not** consulted. None of the audited claims consumes it (the note says so in §5, and I checked: Lemmas 2.1–2.5, Thm 2.4 and Prop 3.1 use nothing from KSBFT).

Verdict scale: **HOLDS** (re-derived here, or re-computed independently), **BROKEN** (false as
stated), **OVERSTATED** (the true content is weaker than the words), **UNVERIFIABLE**.
Labels on my own statements: **PROVEN** (proof in this file), **PROVEN (computer)**, **EMPIRICAL**,
**CONJECTURED**.

Instrument: `code/audit_ksbft_f889/`. Run `sh run_all.sh`. It is serial (1 process), takes ~70 min, and
ends with `check_controls_f889.py`, which exits 1 on any failed expectation or silent negative control.
It prints `VERDICT: GREEN` (`out_check_controls_f889.txt`).

**Independence.** `indep_f889.py` is pure Python (exact `Fraction`s and big integers). It shares **no code** with
`pcert.c` or `onept.c`, and I wrote it from the note's *statements*. I read `pcert.c` only to audit it
(§2.4), after the design below was fixed.

| | mg-6b81 `pcert.c` (+ `onept.c`) | this audit `indep_f889.py` |
|---|---|---|
| canonical form | `onept.c`: least relation matrix over an individualisation–refinement tree | **least tuple of down-rows over all natural labellings** (linear extensions), found level by level; no refinement |
| counting | `__int128` `lecount` per sub-poset | DP over the order ideals of `Q`; `x`-before-`y` by zeroing ideals with `y ∈ I ∌ x` |
| completeness of the non-CUT list | pruned generator (Lemma 2.5(b)), cross-checked against `onept gen` | pruned generator **and** an unpruned range-≤3 census filtered by CUT afterwards, so completeness does not rest on Lemma 2.5(b) |
| Theorem 2.4 end to end | every size-11 ideal of every indecomposable `P`, `n = 12, 13` | **random** indecomposable `P` of size 22 and 30 (D=3) and 22 (D=4), every size-`t` ideal |

**Exception to independence (stated, not hidden).** At `D = 4`, `t = 14, 15` the lists have 4.2 M and 14.3 M classes, which is beyond a Python generator. For those I **re-ran the author's `pcert`** (a reproduction, not an independent check) to obtain the lists and its `cert`/`delta` output. I then applied **my** certifier to pcert's 14 `t = 14` failures, to its named `t = 14, 15` extremes, and to a 1 % stride sample of the `t = 15` list.

Controls, each of which fires (`out_check_controls_f889.txt`):
- **Canonical form.** Positive: A000112 `1 2 5 16 63 318 2045 16999` for `n ≤ 8`. NEGATIVE CONTROL: a broken canonical form that returns the input labelling's rows gives `1 2 7 40 357`, CAUGHT.
- **Certificate.** NEGATIVE CONTROL: with the interval narrowed to `[2/5, 3/5]`, 544 of the 4 224 `t = 11` classes at `D = 3` are uncertified, CAUGHT.
- **Theorem 2.4 end to end.** NEGATIVE CONTROL: with `s = t − D + 1`, one more than Lemma 2.2 allows, there are 102 bracket violations and 30 certified pairs with `dist(p_P) < rm` at `D = 3`, and 5 and 2 at `D = 4`, CAUGHT.

---

## 0. Headline

| # | claim (mg-6b81) | verdict |
|---|---|---|
| 1 | Prop 3.1: Lemma R's window transports no margin, for every `μ > 0` and every `v` with `π(v) ≥ 1` | **HOLDS** (re-derived, §1). It is in fact stronger: the window is never inside the *open* interval `(1/3, 2/3)`. |
| 2a | Lemma 2.1 (bandwidth `j − i ≤ 2D − 1`) and Lemma 2.2 (every size-`s` ideal sits inside any ideal of size `≥ s + D`) | **HOLDS** (re-derived, §2.1). Lemma 2.2's "ideals of size `s` of `P` = ideals of size `s` of `Q`" also checked by count on every `(P, Q)` of the random e2e: 0 mismatches. |
| 2b | Lemma 2.3: `p_P = Σ_J w_J p_J`, `w_J = e(J) e(P∖J)/e(P)`, `w_J > 0`, `Σ w_J = 1` | **HOLDS** (re-derived, §2.2). This is exact. It is the standard cut of the ideal lattice at level `s`. |
| 2c | Thm 2.4: "balanced in every size-`s` ideal of `Q`" ⇒ balanced in every `P ∈ Π_D` above `Q`, with `dist(p_P) ≥ rm` | **HOLDS** (§2.3). It is the same labelled pair (`x, y ∈ K = ∩𝒥`), and the combination is convex with the weights of 2b. **I could not break it.** 0 bracket violations and 0 certified-but-`dist(p_P) < rm` pairs on random `P` of size 22–30, and the off-by-one control breaks it as it should. |
| 2d | Lemma 2.5 (CUT filter; generator completeness) | **HOLDS** (re-derived, §2.4). The unpruned range-≤3 census minus its CUT members equals the pruned counts for `t ≤ 12`, and my pruned counts equal pcert's for `D = 3`, `t ≤ 13` and `D = 4`, `t ≤ 13`. |
| 3a | Thm 5.1 (Π₃): 4 224 non-CUT classes at `t = 11`, all certified at `s = 8`, worst `rm = 1/96`; base `n ≤ 11` | **HOLDS, PROVEN (computer), regenerated independently in full.** 938 / 2 001 / 4 224 / 9 307 / 20 459 classes; 13 / 4 / 0 / 0 uncertified at `t = 9..12`; the per-`s` counts at `t = 11` are identical (2158, 3462, 4069, 4121, 4215, 4224); base: 2 582 indecomposable, `n = 3..11`, the only zero is `2+1`. |
| 3b | Thm 5.2 (Π₄): 14 298 595 classes at `t = 15`, 0 failures, worst `1/150`; 14 failures at `t = 14` | **HOLDS, partly independent.** Independent in full for `t ≤ 13` (counts and 990 / 943 / 496 / 192 uncertified at `t = 10..13` match). At `t = 14, 15`: pcert re-run reproduces `AGG CT 14 4177332 0 14 0`, `AGG CT 15 14298595 0 0 0`, and the D=4 base transcript at `n = 12..15` byte for byte. My certifier confirms all 14 `t = 14` failures (worst `−1/417`), the `t = 15` worst class (`rm = 1/150` exactly), and a 1 % stride sample of `t = 15` (every 100th line: 142 986 classes, all distinct under my canonical form, all non-CUT with range ≤ 4, **0 uncertified**, worst `max_s rm` in the sample `1/105`). The completeness of the `t = 14, 15` lists rests on Lemma 2.5(b) (PROVEN) plus pcert's canonical form (controlled by mg-eedd/mg-95d3, and agreeing with mine to `t = 13`). |
| 4a | Exceptional list for the δ-margin is `{2+1}` | **HOLDS** (EMPIRICAL). Re-computed over all 14 100 indecomposable posets with `n ≤ 8` (every range) and all indecomposable members of `Π_3`, `n ≤ 11`. It also agrees with Gup26 (all posets `n ≤ 14`: equality only for ordinal sums of singletons and `2+1`). |
| 4b | `μ_3 = μ_4 = 5/318` ("the largest μ consistent with the data") | **μ_4: BROKEN** as a value. The repo already holds an indecomposable range-4 poset with `n = 21` (mg-2912's annealing witness) whose δ-margin is **721/46455 ≈ 0.015520 < 5/318 ≈ 0.015723**. I re-computed it with my own counter (`out_witness.txt`). Restricted to `n ≤ 15`, where the note measured, the figure is right. **μ_3 = 5/318: HOLDS (EMPIRICAL)** to `n ≤ 15` here, and to `n ≤ 18` exhaustive per mg-2912 (not re-run). It is not in conflict with Cor 2.6 (1/150 < 721/46455). |
| 5 | Novelty of the prefix-certificate method | **UNVERIFIABLE.** I could not reach the full text of BW92, Pec08 or Brightwell's 1999 survey. The ingredients are standard: the ideal-lattice cut identity (Lemma 2.3) is the forward/backward decomposition of De Loof–De Meyer–De Baets that Gup26 cites, and the bandwidth lemma is elementary. The *combination* (a finite certificate on a bounded prefix, valid for all `n` in `Π_D`) was not found, but that absence is weak evidence (§5). |
| 6 | Title: "Its cost rules out D ≥ 5" | **OVERSTATED.** It is EMPIRICAL cost at `t ≤ 13` plus a two-point extrapolation that the body itself labels CONJECTURED (§7 of the note). "Rules out" should read "puts `D ≥ 5` beyond exhaustive enumeration here". |

Not audited: the covariance-decay table (§4 of the note) and the `d`-distance transport table (§3), both EMPIRICAL. I did not re-run `pcert decay`.

---

## 1. Prop 3.1 (HOLDS, PROVEN)

Lemma R (KSBFT-J; HOLDS per mg-95d3): `p_P = E'[w 1_A]/E'[w]` with `w = w_v ∈ [1, r]`, `r = π(v) + 1`. Given `p' = P'(A)`, the extreme values put weight `r` on `A` and 1 on the complement, or the reverse. This gives the window `W_r(p') = [p'/(p' + r(1−p')), r p'/(r p' + 1 − p')]`, which is what the note writes.

Re-derivation. The left end is `> 1/3` iff `3p' > p' + r − r p'` iff `p'(r+2) > r` iff `p' > r/(r+2)`. The right end is `< 2/3` iff `3 r p' < 2 r p' + 2 − 2p'` iff `p'(r+2) < 2` iff `p' < 2/(r+2)`. For `r ≥ 2`, `r/(r+2) ≥ 1/2 ≥ 2/(r+2)`, so the two are incompatible. Hence **for no `p'` is `W_r(p') ⊂ (1/3, 2/3)`**, and a fortiori not `⊂ [1/3+μ, 2/3−μ]` for `μ > 0`. With non-strict inequalities, `r/(r+2) ≤ p' ≤ 2/(r+2)` forces `r = 2`, `p' = 1/2`. That matches the note, and it is KSBFT-J's Cor 1.4. `π(v) ≥ 1` for every `v` of an indecomposable `P` with `n ≥ 2` (an element comparable to all others would make `G(P)` disconnected). □

Scope: this is a statement about **Lemma R as an inference rule**, i.e. about the bound, not about posets. The note scopes it that way ("Lemma R alone"). §0.3(b), "any ε > 0 degrades μ to μ − ε", is a triviality and is correctly presented as structural, not as a theorem.

## 2. The prefix certificate: attempts to break it

### 2.1 Lemmas 2.1, 2.2 (HOLDS)

*2.1.* Let `z` sit strictly between `x` (position `i`) and `y` (position `j`) in `L`. Then `z ≮ x` and `z ≯ y` by the order of `L`, and `x < z < y` would give `x < y`. So `z ∥ x` or `z ∥ y`. `y` is one of `x`'s `π(x)` incomparables but is not between them, so at most `π(x) − 1 + π(y) − 1` elements lie between. Hence `j − i ≤ 2D − 1`. ✓

*2.2.* Take `u ∈ J` at position `j`. The `j − 1` earlier elements include at most `s − 1` from `J`. Each earlier element outside `J` is not below `u` (`J` is down-closed) and not above it (by `L`). So `π(u) ≥ j − s`, which gives `j ≤ s + D`. Now choose `L` to start with a linear extension of `Q`. This is legitimate because `Q` is an ideal. Then every size-`s` ideal of `P` lies in the first `s + D ≤ t` positions, which is `Q`. Conversely, an ideal of the poset `Q` is an ideal of `P`, because `Q` is down-closed. ✓ The inequality is tight in the direction that matters: the off-by-one control (`s = t − D + 1`) produces real bracket violations and false certificates (`out_e2e.txt`).

### 2.2 Lemma 2.3 (HOLDS). Item (b) of the ticket.

The map `L ↦ (J, L|_J, L|_{P∖J})`, with `J` the first `s` elements of `L`, is a bijection from `𝓛(P)` onto `{(J, λ, ρ) : J` a size-`s` ideal, `λ ∈ 𝓛(J)`, `ρ ∈ 𝓛(P∖J)}`. It is injective because `L` is recovered by concatenation. It is surjective because concatenation is a linear extension: no element of `P∖J` lies below an element of `J`, since `J` is down-closed. So:
- `e(P) = Σ_J e(J) e(P∖J)`, and therefore `w_J := e(J) e(P∖J)/e(P)` satisfies **`w_J > 0`** (every finite poset has `≥ 1` extension) and **`Σ_J w_J = 1`**.
- If `x, y ∈ J` for **every** `J`, then "`x` before `y` in `L`" depends on `λ` only. So `e(P) p_P = Σ_J e(P∖J) · e(J) p_J`, i.e. `p_P = Σ_J w_J p_J`. This is exact, with no error term.

The weights do **not** depend on the pair. That is what makes the combination one convex combination, not one per pair.

### 2.3 Thm 2.4 (HOLDS). Item (c).

- **Same pair.** `x, y` are fixed labelled elements of `K = ∩𝒥`. `p_J(x<y)` is computed in the induced subposet `J`, which is the same whether `J` is viewed inside `Q` or `P`. Incomparability of `x, y` is inherited. So each `p_J` concerns the same ordered pair `(x, y)`.
- **Same family.** By 2.2, `𝒥` (the size-`s` ideals of `Q`) is exactly the family summed in 2.3.
- **Convex.** By 2.3, `p_P = Σ w_J p_J` with `w ≥ 0`, `Σ w = 1`, and every `p_J ∈ [1/3 + rm, 2/3 − rm]`, which is an interval. So `p_P` lies in it too. ✓

Attempts to break it:
1. *`K` could be empty, or its pair comparable in `P`.* Then no certificate exists and nothing is claimed.
2. *`Q = P`.* Harmless: 2.2 and 2.3 hold with `P∖J` inside `P`.
3. *The `rm` reported is `max_s min_J`, but the theorem needs a single `s`.* The code takes, for each `s`, `max` over pairs of `min` over `J`, and then `max` over `s`. Each value is realised by one `(s, pair)`. ✓ (`pcert.c:67-86`; same in mine.)
4. *Integer overflow in pcert.* This cannot be excluded by reading alone. It is excluded by agreement with my big-integer computation on every class at `t ≤ 13`, the two extremes at `t = 14, 15`, and the sample.
5. *Directly.* On random indecomposable `P ∈ Π_3` of size 22 (40 posets, 103 ideals `Q`) and 30 (15 posets, 42 `Q`), and `P ∈ Π_4` of size 22 (6 posets, 19 `Q` of size 15), every pair in `K` satisfies `min_J p_J ≤ p_P ≤ max_J p_J`, and every certified pair has `dist(p_P) ≥ rm`, with `p_P` counted directly on `P`. Result: 0 violations. The minimum slack is exactly 0, attained by pairs whose `p_J` is the same for all `J`.

### 2.4 Lemma 2.5, the CUT filter, generator completeness (HOLDS). Item (d).

- *(a)* The strong cut `I` has `|I| = k ≤ t − 2D + 1`. In `L = [I | Q∖I | P∖Q]`, every `a ∈ I` is at position `≤ k` and every `b ∈ P∖Q` at position `≥ t + 1`. The gap is `≥ 2D`, so `a < b` by 2.1. With `I < Q∖I`, the set `I` has no `G(P)`-edge to its complement, which is nonempty. ✓
- *(b)* Take `P := Q'` and `Q := Q' − z`, with `z` maximal. A strong cut of `Q' − z` of size `≤ (t−1) − 2D + 1` lies below `z` by the same gap argument, so it is a strong cut of `Q'` of size `≤ t − 2D + 1`. ✓
- *(c)* A strong cut disconnects `G`. Every non-CUT `Q'` of size `t` is `(Q' − z) + z`, where `Q' − z` is non-CUT with range `≤ D` (range is hereditary) and `z`'s down-set is an ideal of `Q' − z`. So "add a maximal element with every ideal as down-set, keep range `≤ D` and non-CUT, deduplicate" is complete by induction. ✓
- *Code.* `is_cut` (`pcert.c:193`) tests exactly `1 ≤ |I| ≤ n − 2D + 1` and `I ⊆ dn[j]` for all `j ∉ I`, with `n` the current size. `mode_gencut` tries every ideal from `all_ideals`, including `∅`. `cert_one` silently returns on range `> D`. That is harmless here, because `c_tot` equals the list size (`14 298 595`), so nothing was skipped.
- *Measured.* My unpruned census of `Π_3` (23 701 classes at `t = 11`, 67 116 at `t = 12`) minus its CUT members equals the pruned counts at every `t ≤ 12`. My pruned counts equal pcert's at `D = 3`, `t ≤ 13` and at `D = 4`, `t ≤ 13`.

## 3. The computer proofs

### 3.1 Π₃ (Thm 5.1): HOLDS, independently regenerated in full

`out_gen3.txt`, `out_cert3.txt`, `out_base3.txt`:

| t | classes (mine = pcert) | uncertified (mine = pcert) | worst `max_s rm` |
|---|---|---|---|
| 9 | 938 | 13 | −1/39 |
| 10 | 2 001 | 4 | −1/39 |
| **11** | **4 224** | **0** | **1/96** (and `s = 8` alone certifies all 4 224) |
| 12 | 9 307 | 0 | 1/96 |

Base, `n = 3..11`: 2 + 7 + 15 + 32 + 59 + 131 + 289 + 643 + 1 404 = **2 582** indecomposable posets. Every per-`(n, π)` minimum equals the note's table (e.g. `n = 10`, `π = 3`: 5/318; `n = 11`, `π = 3`: 1/57). There are no negative entries, and the only zero is `2+1`.

The proof of Thm 5.1 (the decomposable reduction, the base via the lists, which contain every indecomposable poset by 2.5(c), and `n ≥ 12` via any size-11 ideal, which is non-CUT by 2.5(a)) is correct as written. Cor 2.6 (`δ ≥ 1/3 + 1/96` for indecomposable `P ∈ Π_3`, `n ≥ 12`) HOLDS.

### 3.2 Π₄ (Thm 5.2): HOLDS (independent to t = 13; t = 14, 15 by reproduction plus independent sampling)

| t | classes (mine = pcert) | uncertified (mine = pcert) | worst |
|---|---|---|---|
| 10 | 29 491 | 990 | −2/15 |
| 11 | 103 198 | 943 | −4/57 |
| 12 | 357 363 | 496 | −2/51 |
| 13 | 1 224 360 | 192 | −4/183 |
| 14 | 4 177 332 (pcert) | 14 (pcert; all 14 re-checked by mine) | −1/417 (mine agrees) |
| 15 | 14 298 595 (pcert) | 0 (pcert re-run; mine: 0 in the sample) | 1/150 (mine agrees on the named class) |

Rows 10–13 are my generator and my certifier (`out_gen4.txt`, `out_cert4.txt`). Rows 14–15 are pcert re-run (`out_pcert_rerun.txt`) plus my certifier on the named classes and the sample (`out_sample_d4.txt`).

Base `n ≤ 15` at `D = 4`: the pcert re-run of `delta` on `n = 12..15` is identical to the committed `out_base.txt`. My own base computation covers `n ≤ 8` (all ranges) and the indecomposable members of the 1 % sample at `n = 15` (72 587 indecomposable posets, minimum `δ − 1/3 = 356/10191 ≈ 0.0349`, no zero or negative). **I did not independently compute δ for all 7.2 M indecomposable `n = 15` posets.**

## 4. Empirical claims

- **Exceptional list `{2+1}`: HOLDS (EMPIRICAL).** In `out_base_all8.txt` (all 14 100 indecomposable posets `n = 2..8`, every range) and `out_base3.txt`, the only zero is `n = 3`, `P = 2+1`. It is consistent with Gup26 (arXiv:2607.23926 §1.1): through `n = 14`, `δ = 1/3` only for ordinal sums of singletons and `T = 2+1`.
- **`1/3 + 5/318 = 37/106`.** This is exactly Gup26's "least value above 1/3 at order 14, inherited from a ten-element poset". So the `n ≤ 14` part of the μ claim is an independent literature cross-check (Gup26's computation, not re-run by me), and it is not new.
- **μ₄ = 5/318: BROKEN.** mg-2912 (`docs/KSBFT-A-range-probe.md` Table 1; `code/ksbft_range_probe/out/*.jsonl`, record `search_delta D=4 n=21`) found by annealing a width-2, range-4 poset on 21 elements with `δ = 5402/15485`. I re-computed it (`witness_f889.py`, `out_witness.txt`): transitively closed, range 4, `G` connected, `δ − 1/3 = 721/46455 = 0.015520 < 5/318 = 0.015723`. So `μ_4 ≤ 721/46455`. The note's statement is correct only as "the minimum over `n ≤ 15`". The note even points at this file ("mg-2912's 0.3489 floor", "I did not recompute"), and 0.3489 < 37/106 = 0.34906 was visible there. The figure 0.348854 is close to Sah's constant β ≈ 0.348843 (cited in `docs/state-history/attempt-index.md`), which suggests the true `μ_4`, if positive, may be ≈ β − 1/3 ≈ 0.01551 (CONJECTURED). **None of this touches the theorems**: Cor 2.6's `1/150` is below it.
- **μ₃ = 5/318: HOLDS (EMPIRICAL)** on `n ≤ 11` (mine) and `n ≤ 15` (the note). mg-2912 reports exhaustive `π ≤ 3` to `n = 18` with the same minimum 37/106 and annealing to `n = 24` with nothing lower. I did not re-run that.

## 5. Novelty (UNVERIFIABLE)

`D ≤ 6` is known (BW92, Pec08), and the note says so. For the **method**, I searched briefly (web search; Gup26 full text; the Olson–Sagan survey). I could not obtain BW92, Pec08 or Brightwell's survey (Discrete Math. 201 (1999)) in full text, so I cannot say whether they condition on a bounded bottom ideal. What I can say:
- Lemma 2.3 is the ideal-lattice cut `e(P) = Σ_{|J|=s} e(J) e(P∖J)`. The forward/backward ideal-lattice recursion for mutual rank probabilities is attributed by Gup26 to De Loof, De Meyer and De Baets. The mixture identity is folklore-level.
- Lemmas 2.1/2.2 (bandwidth `≤ 2D − 1` of a linear extension in `Π_D`) are elementary. Both BW92 and Pec08 are computer proofs on thin posets, and a "finite bottom window decides it" argument is a natural candidate for what they do.
- Verdict: the method's novelty is **UNVERIFIABLE** from here. The note's own "Novelty: UNCHECKED" is the right label, and I do not upgrade it.

## 6. What I did not do, and the negatives

**Not done.**
- An independent generator at `D = 4`, `t = 14, 15`. Those lists come from pcert. My certifier was applied to a 1 % stride sample (every 100th line from line 37), not to all 14.3 M classes.
- Independent δ for all indecomposable `Π_4`, `n = 12..15` (pcert re-run only, plus the sample).
- `pcert decay` and the §3/§4 decay tables of the note (EMPIRICAL there, not audited).
- Reading BW92, Pec08, Bri99.
- Re-running mg-2912's exhaustive `π ≤ 3`, `n ≤ 18` census. I re-computed only its `n = 21` witness.

**Negatives (attempts to break the note that failed).**
1. A pair that is not the same across `J`: impossible, since it is taken in `K = ∩𝒥` (§2.3).
2. Weights depending on the pair, or not summing to 1: they do not depend on it, and they sum to 1 by the bijection (§2.2).
3. An ideal of `P` of size `s` escaping `Q`: excluded by 2.2, and exhibited when `s = t − D + 1` (control).
4. A non-CUT class missed by the pruned generator: the unpruned census agrees at `t ≤ 12` (D=3).
5. Random large `P` violating the bracket or the certified margin: 0 in 64 posets, 164 ideals.
6. A certified class at `t = 11` (D=3) or `t = 15` (D=4) that my code finds uncertified: none (all 4 224; 1 % sample).
7. An indecomposable non-`2+1` poset with `δ = 1/3`: none (`n ≤ 8`, all ranges; `Π_3`, `n ≤ 11`).

## Sources
- [Gupta, arXiv:2607.23926](https://arxiv.org/abs/2607.23926) (37/106; equality classes; De Loof–De Meyer–De Baets attribution)
- [Brightwell–Wright, SIAM J. Discrete Math. 5 (1992)](https://epubs.siam.org/doi/10.1137/0405037) (abstract only)
- [Peczarski, Order 25 (2008)](https://link.springer.com/article/10.1007/s11083-008-9081-9) (abstract only)
- [Olson–Sagan survey](https://users.math.msu.edu/users/bsagan/Papers/Old/otc.pdf) (no method description of BW92/Pec08)
