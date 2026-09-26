# KSBFT-A — bounded-range posets computed exactly (mg-2912)

**Status:** data deliverable for the KSBFT-B proof side. Every number here is **EMPIRICAL**
(exact rational arithmetic over a finite, stated population) unless marked **PROVEN** (proof
in this document) or **CONJECTURED**. A probe is not a proof. Instrument, controls and
reproduction: [`code/ksbft_range_probe/README.md`](../code/ksbft_range_probe/README.md).
Paper: KSBFT_v7 (Aires–Chan–Pak–Panova, 2026-09-25), `/Users/daniel/files/KSBFT_v7.pdf`,
pages as printed. `C_BFT = (5−√5)/10 ≈ 0.276393`.

## 0. Verdict

- **PROVEN (new, §3.1):** for every finite poset with connected incomparability graph and
  `π(P) ≤ D`, **`M ≥ d_1 ≥ 1/(D+1)`**. That replaces `q_2 = (D+1)^{−2(D+1)}` in the paper's
  eq. (4.11), and the M-step of Theorem 1.3 stops being the bottleneck. **The bottleneck then moves
  to Lemma 3.2(iii)**, whose eq. (3.6) needs `(5+3√5)η < q_3 = (D+1)^{−3(D+1)}`. So, taking Lemmas 3.2
  and 4.2 as stated, the theorem's gap improves only from `(D+1)^{−4(D+1)}/4096` to about
  `(D+1)^{−3(D+1)}/(5+3√5)`. It is still exponentially small in `D` (§3.1). The bound is tight for `d_1` at
  every `D`, and for `M` at `D = 1, 2`.
- **EMPIRICAL:** nothing comes near `C_BFT`. Over every non-chain poset on `n ≤ 11`
  elements, over every poset with `π ≤ 3` on `n ≤ 18`, `π ≤ 4` on `n ≤ 15`, `π ≤ 5` on
  `n ≤ 13`, and `π ≤ 6` on `n ≤ 12`, the only posets with `δ < 0.3490` are the (2+1)
  poset and its ordinal sums with chains (`δ = 1/3`). The smallest δ found anywhere among the
  others is `5402/15485 ≈ 0.348854` (annealing, `n = 21`, `π = 4`). That is 0.0155 above 1/3
  and 0.0725 above `C_BFT`.
- **EMPIRICAL, the key question (§3):** for fixed `D`, `M` has an `n`-independent floor. Across `D`, the
  minimum over `π ≤ D` moves DOWN as `D` grows: 0.3333 (D=2), 0.3077 (3), 0.2985 (4), 0.2869 (5),
  0.2858 (6). Then it **stalls**: annealing at `π ≤ 8`, `n ≤ 24`, finds nothing below the `π = 6`
  witness 0.285753. That is consistent with a `D`-independent floor near 0.285 (CONJECTURED, not
  shown). For fixed `D` the minimum is flat in `n` once `n` is past about 11–20. The
  shrinking family is **not** Fibonacci. `F_N` has the LARGEST limit, `(3−√5)/2`. The
  minimisers are width-3 posets whose `M` sits at an END.
- **Lemma 4.2 (§4):** no violation. The lemma cannot be tested under its own hypothesis,
  because no poset in the population satisfies `δ ≤ C_BFT + η_D`. The unconditional form is
  **PROVEN false** (the antichain on 21 elements). On the triples that have the Lemma 3.2
  shape, the best constant in the data is `c ≈ 0.51`, against the paper's 1/441.
- **Fibonacci (§5):** confirmed exactly for `N ≤ 81`: `δ(F_N) = F_{N−1}/F_{N+1} → (3−√5)/2`,
  attained ONLY at the two end pairs, with `M = δ(F_N)`. The centre adjacent pair tends to
  `C_BFT`. The paper's p.13 displacement formula is right in absolute value but **wrong in sign**: the true signs alternate.
- **Structure (§6):** every poset in the data with `δ < 0.35` has width 2 and attains `δ` at an END
  pair. For each of them `δ = M = d_1`, and each extreme element has exactly one incomparable.

## 1. Population and method (summary; details in the README)

| population | exhaustive? | count at the top level |
|---|---|---|
| every poset, `n ≤ 11` | yes | 46 749 427 at n=11 (= OEIS A000112) |
| `π ≤ 3`, `n ≤ 18` | yes | 34 677 549 at n=18 |
| `π ≤ 4`, `n ≤ 15` | yes | 34 593 068 at n=15 |
| `π ≤ 5`, `n ≤ 13` | yes | 24 861 893 at n=13 |
| `π ≤ 6`, `n ≤ 12` | yes | 31 723 092 at n=12 |
| `π ≤ D`, `D ∈ {3,4,5,6,8}`, `12 ≤ n ≤ 24` (`out/searchtab.txt`) | **no — simulated annealing, HEURISTIC** | best witness per `(D, n)`, two seeds for `M` |

The analysis covers posets whose incomparability graph `G(P)` is connected. **PROVEN**
(README P1): `δ`, `π` and `M` of any poset are the maxima over its `G`-components, so every
"min over non-chain posets with `π ≤ D` on `≤ n` elements" equals the minimum over the
connected-`G` posets with `2 ≤ |P| ≤ n`. All `e(P)`, heights, pair probabilities, `δ` and `M`
are exact integers or rationals. Controls: OEIS counts, the ordinal-sum identity, the
paper's p.12 formula, brute force = DP = C++ on 300 random posets, one planted negative
control, and exact Python re-derivation of all 2 535 distinct kept extreme records and
annealing witnesses (`out/controls.txt`, `out/rederive.txt`). The annealer re-finds every
exhaustive minimum it was tested against: `π ≤ 3` for `12 ≤ n ≤ 18`, `π ≤ 5` for `n = 10, 11`.

## 2. Question 1 — min δ per range `D`

**Table 1 (EMPIRICAL).** Minimum of `δ` over connected-`G` posets with `π = D` exactly. The
minimum is cumulative over `n` up to the stated coverage. The last column adds the annealing
witnesses (`π ≤ D` search, reported at the witness's exact `π`).

| D | min δ (exhaustive) | at n | exhaustive to n | margin over 1/3 | with annealing to n=24 |
|---|---|---|---|---|---|
| 1 | 1/2 | 2 | 18 | +0.1667 | — |
| 2 | 1/3 | 3 (the (2+1)) | 18 | 0 | for `n ≥ 4`: `F_{N−1}/F_{N+1}` → 0.381966 (§5) |
| 3 | 37/106 = 0.349057 | 10 | 18 | +0.0157 | 601/1720 = 0.349419 (n=21); no improvement |
| 4 | 103/292 = 0.352740 | 14 | 15 | +0.0194 | **5402/15485 = 0.348854** (n=21) |
| 5 | 6/17 = 0.352941 | 10 | 13 | +0.0196 | 757/2102 = 0.360133 (n=13); none lower |
| 6 | 134/375 = 0.357333 | 11 | 12 | +0.0240 | none lower (best π=6 witness 0.375257) |
| 7 | 20/53 = 0.377358 | 11 | 11 | +0.0440 | — |
| 8 | 152/411 = 0.369830 | 11 | 11 | +0.0365 | — |
| 9, 10 | 2/5 | 11 | 11 | +0.0667 | — |

- **Does anything approach `C_BFT`? No.** Leave out the (2+1) family, whose `δ` is exactly 1/3.
  Every other poset in the population has `δ ≥ 0.3488`, a margin of `≥ 0.0725` over
  `C_BFT`. This is consistent with Gup26 (every poset on `≤ 14` elements) and
  Brightwell–Wright / Peczarski (`π ≤ 6`). It goes further only in `n` for `π ≤ 3, 4, 5`, and there
  only empirically.
- **How the margin behaves with `n`:** for fixed `D` the per-`n` minimum settles within a
  few elements and then oscillates in the 4th decimal (Table 1 of `out/report.txt`). For
  `D = 3` it is 0.3491–0.3505 for all `10 ≤ n ≤ 24`. For `D = 4` it drifts from 0.3527
  (n=14) to 0.34885 (n=21, annealing). No trend toward 1/3 is visible; a slow drift can't
  be excluded at this `n`. Over ALL ranges, the per-`n` minimum of `δ` among connected-`G`
  posets with `n ≥ 4` is 0.4, 0.3636, 0.3571, 0.3590, 0.3556, 0.3529, **0.3491**, 0.3509 for
  `n = 4..11`.
- **The minimum is not monotone in `D`:** the lowest values come from `D = 3, 4`. Larger
  range buys larger `δ` in this data, which is consistent with Theorem 1.4's picture.

## 3. Question 2 — min `M` over `π ≤ D`, and the key question

**Table 2 (EMPIRICAL).** Minimum of `M` over connected-`G` posets with `π ≤ D`, taking the
minimum over all `n` in the coverage:

| D | min M, exhaustive | at n | exhaustive to n | annealing (π ≤ D, n ≤ 24) | large-`n` plateau |
|---|---|---|---|---|---|
| 1 | 1/2 | 2 | — | — | — |
| 2 | 1/3 | 3 | 18 | — | `F_{N−1}/F_{N+1}` → 0.381966 |
| 3 | 4/13 = 0.307692 | 6 | 18 | 0.338378 (n=14; = exhaustive) | ≈ 0.3385 for n = 14..24 |
| 4 | 20/67 = 0.298507 | 11 | 15 | 0.299176 (n=15) | 0.299–0.304 for n = 11..24 |
| 5 | 13/45 = 0.288889 | 11 | 13 | 871/3036 = 0.286891 (n=14) | ≈ 0.29–0.30 |
| 6 | 13/45 | 11 | 12 | **26653/93273 = 0.285753** (n=20) | 0.286–0.291 for n = 14..22 |
| 8 | 13/45 (n ≤ 11 is all ranges) | 11 | 11 | 0.285753 (the π=6 witness); best with π=7: 0.287683, with π=8: 1193/4173 = 0.285885 (n=15) | 0.286–0.30 for n = 15..24 |

**KEY QUESTION — is `M` bounded below by a constant independent of `D` and `n`?**
- **Independent of `n` for fixed `D`: EMPIRICALLY yes.** For each `D` the minimum reaches its
  plateau by `n ≈ 11–20` and stays there to `n = 24`. The reason is visible in the minimisers:
  `M` is attained at an END (`d_1` or `−d_n`), where it is set by a bounded "end gadget", and
  in the interior `|d_i|` is smaller.
- **Independent of `D`: NOT SETTLED, and the data leans toward yes.** The plateau
  moves down with `D`: 0.3333, 0.3077, 0.2985, 0.2869, 0.2858 for `D = 2..6`. The steps shrink
  (0.026, 0.009, 0.012, 0.001), and at `D = 8` the annealer finds nothing lower (best π=8 witness
  0.285885). That suggests convergence to a positive limit near 0.285 but does not show it. The
  annealer is a heuristic, and exhaustive coverage at `D ≥ 7` stops at `n = 11`.
- **Is the shrinking family Fibonacci-like? No.** `F_N` (π=2) has `M → 0.381966`, the
  LARGEST small-range value. The minimisers have width 3 and range 5–6. Their bottom is
  `v_1 ∥ v_2` only, `v_2 ∥ {v_1, v_3, v_4}` with `v_3 ∥ v_4`, and one long-range element of
  degree `D` in `G` that feeds the balance. At the optimum `d_1 ≈ d_2`, e.g.
  `d = (+0.286, +0.285, −0.072, …)` at n=20. The top is the mirror image. See
  `describe.py` on the `min_M` records.
- **What is PROVEN** is a floor that shrinks with `D`, but only polynomially:

### 3.1 PROVEN: `M ≥ d_1 ≥ 1/(D+1)`

**Claim.** Let `P` be finite with `n ≥ 2`, `G(P)` connected, `π(P) ≤ D`. Let `v_1` be an
element of minimum height. Then `P[f(v_1) ≠ 1] ≥ 1/(D+1)`, and hence
`M ≥ d_1 = h(v_1) − 1 ≥ 1/(D+1)`.

*Proof.* Let `W ≠ ∅` be the set of elements incomparable to `v_1` (`G` connected).
(a) *Every `u ∉ W ∪ {v_1}` satisfies `u ≻ v_1`.* Otherwise `u ≺ v_1`, so `f(u) < f(v_1)` in
every extension and `h(u) < h(v_1)`, which contradicts minimality.
(b) *No `u ∉ W ∪ {v_1}` lies below any `w ∈ W`.* Otherwise `v_1 ≺ u ≺ w`.
Let `A` be the set of extensions with `v_1` first. For `g ∈ A` let `w` be the first element of `W` in
`g` and let `Φ(g)` be `g` with `w` moved to the front. Every element that `w` passes is `v_1` or
an element of type (a), and by (b) none of them is below `w`. So `Φ(g)` is a linear extension, and it
starts `w, v_1`. A given image `Φ(g)` has at most `π(w) ≤ D` preimages: `w` is reinserted after
`v_1`, before the first element of `W∖{w}` and before the first element above `w`. The
elements it can skip are not in `W`, not above `w` and, by (b), not below `w`. So they are incomparable to `w`,
and there are at most `π(w) − 1` of them (`v_1` is already one of `w`'s incomparables). That
gives at most `π(w)` positions. Hence `|A| ≤ D · #{extensions not starting with v_1}`, so
`P[f(v_1) = 1] ≤ D/(D+1)`. Finally `d_1 = E[f(v_1)] − 1 ≥ P[f(v_1) ≠ 1]`. ∎

*Checks (EMPIRICAL, `d1bound.py`):* zero violations over every connected-`G` labelled poset on
`n ≤ 6` (4 377) and over all 2 535 records kept (`out/d1bound.txt`). The planted false bound `d_1 ≥ 1/D` is caught
617 times. **Tightness:** `d_1 = 1/(D+1)` holds with equality for every `D`. The example is a
chain on `D` elements plus one element incomparable to every element of the chain (`d_1 = 1/(D+1)` exactly, checked for `D ≤ 6`). But `M = d_1` at equality only for
`D = 1, 2` (the 2-antichain and the (2+1)). For `D ≥ 3` the data puts `M` far above
`1/(D+1)` (Table 2).

**What it buys KSBFT-B, and what it does not.** In the paper's §4.3, eq. (4.11) uses Lemma 3.1 to
get `M ≥ q_2 = (D+1)^{−2(D+1)}`, and the theorem takes `η_D = q_2²/4096`. The claim gives
`M ≥ 1/(D+1)` directly. Now rerun the paper's §4.3 with a smaller-exponent `η`. Assume
`δ(P) ≤ C_BFT + η`. Lemma 3.2 is invoked inside Lemma 4.2, and its proof of (iii) needs
`(5+3√5)η < q_3` (eq. (3.6), p.11). Lemma 3.2(i) and Lemma 4.2 need only `η < 0.2764 − C_BFT ≈ 6.8·10⁻⁶`.
Lemma 4.2 then gives `δ ≥ C_BFT + M²/441 ≥ C_BFT + 1/(441(D+1)²)`, which contradicts the assumption
as soon as `η < 1/(441(D+1)²)`. So, **conditional on Lemmas 3.2 and 4.2 exactly as stated
(LOW-ASSURANCE, not re-derived here)**, any
`η < min(q_3/(5+3√5), 1/(441(D+1)²), 6.8·10⁻⁶) = (D+1)^{−3(D+1)}/(5+3√5)` works for `D ≥ 2`. That is
an exponent of `3(D+1)` in place of `4(D+1)`. **The loss is still `(D+1)^{−Θ(D)}`, and after this
step it comes from Lemma 3.2(iii)'s use of Lemma 3.1 (`q_3`), not from `M`.** Consequence for
the ticket's KEY QUESTION: a `D`-independent lower bound on `M` would **not**, by itself, make
Theorem 1.3's gap uniform in `D`. Lemma 3.2(iii) would have to be redone as well. This is a proof
about one step, and it should get an independent audit before anyone consumes it.

**CONJECTURED (from the data, for KSBFT-B to attack or refute):** `inf M ≥ 0.28` over all
finite connected-`G` posets. That would remove `D` from the M-step. As just explained, it would
not remove `D` from Lemma 3.2(iii).

## 4. Question 3 — Lemma 4.2 numerically

- **Hypothesis never met.** Lemma 4.2 assumes `δ(P) ≤ C_BFT + η_D < 0.2764`. Every poset in
  the population has `δ ≥ 1/3`. So a literal check of the lemma is **vacuous**, and the
  "positive control" asked for cannot be run as asked. Said plainly: this is not evidence for the lemma.
- **The unconditional form is PROVEN false** (README P3). The antichain `A_n` has `δ = 1/2` and
  `M = (n−1)/2`, and `δ ≥ C_BFT + M²/441` fails for `n ≥ 21`. The hypothesis `δ ≤ C_BFT + η_D` is
  what keeps `M` small in the lemma's proof (`M ≤ 21√ε`).
- **No violation in the data, in any form tested** (86 146 388 bucket-records; `out/report.txt`
  Table 3). `δ < C_BFT + M²/441` occurs 0 times. `max(δ(x,y), δ(y,z)) < C_BFT + M²/441` on the
  Lemma-4.1 triple occurs 0 times. **Lemma 4.1 checks out:** every poset with `n ≥ 3` has a
  candidate `k`, and every candidate is a genuine BFT triple, non-chain with span `≤ 2`. The
  single exception is `n = 2`, which has no triple.
- **Best constant `c` with `δ ≥ C_BFT + c·M²`:** over everything it tends to 0 (antichains).
  Restricted to `π = D`: 0.0994, 0.0559, 0.0358, 0.0248, 0.0183, 0.0140 for `D = 3..8`,
  attained at `n = D+1` by wide posets with `M ≈ D/2`. That is roughly `1.1–1.6/(D+1)²`,
  so no `D`-uniform `c` exists in the global form.
- **On the object the lemma is actually about** — consecutive triples with the full Lemma 3.2
  shape (Case D, `z` covers `x`, `y` incomparable only to `x, z`, (3.4)–(3.5), span `≤ 2`):
  `a ≥ C_BFT + c·M_loc²` holds with `M_loc = max(|d_k|, |d_{k+2}|)` and best
  `c = 0.512` (the (2+1)), otherwise 0.58–0.66 for `π = 3..8`. That is 230× the paper's
  `1/441 ≈ 0.00227`. The regimes differ: in the data `ε = a − C_BFT ≥ 0.057`, while in the lemma
  `ε < 10^{−5}`. So this says 441 is loose where it can be measured, and says nothing about
  the `ε → 0` limit, where the Fibonacci centre lives.

## 5. Question 4 — the finite Fibonacci posets

`F_N`: `x_i ≺ x_j ⇔ j − i ≥ 2`, `N = 3..81` elements (the paper's `F_m` is `N = 2m+1`),
exact (`out/fib.txt`). **EMPIRICAL for every `N ≤ 81`:**
- `e(F_N) = F_{N+1}`. The height order equals the index order.
- `δ(F_N) = F_{N−1}/F_{N+1}` (1/3, 2/5, 3/8, 5/13, …) → `(3−√5)/2 = 0.381966`. It is attained
  **only** at the two end pairs `{x_1,x_2}` and `{x_{N−1},x_N}` (at N=3 both pairs are end pairs).
- `M(F_N) = δ(F_N) = d_1 = −d_N`, attained at the two endpoints only.
- The centre adjacent pair gives 0.294118 (N=8), 0.278970 (N=12), 0.276448 (N=20) and 0.276393 (N=41), tending to `C_BFT` with oscillation (the `centre-adjacent` column of `out/fib.txt`).
- **The endpoint-pair ≈ 0.382 picture is CONFIRMED.** The paper's p.12 adjacent-pair formula
  holds exactly (control C2).
- **The paper's p.13 formula `h(x_i) − (m+i+1) = F_{2|i|}/F_{2m+2}` is wrong in sign.** It holds
  in absolute value for every odd `N ≤ 81` and fails as signed. The exact form, verified for every odd `N ≤ 81`
  (`corrected:OK` in `out/fib.txt`), is **`d(x_i) = sgn(−i)·(−1)^{m−|i|}·F_{2|i|}/F_{2m+2}`**: the
  signs ALTERNATE along the poset (e.g. `m = 4`: `21/55, −8/55, 3/55, −1/55, 0, 1/55, −3/55, 8/55, −21/55`).
  This is harmless to the paper's use, which needs only `|d|`, but it is a data point on its assurance level.
- Consequence for the proof side: in `F_N` the balance-attaining pair and the
  displacement-attaining element are the same end, which is exactly the mechanism Lemma 4.1
  aims at. With `π = 2`, the connected-`G` posets for `n ≥ 5` are **exactly** `F_n` (one poset
  per `n`, `n = 5..18`, EMPIRICAL). So `D = 2` is completely described by this section.

## 6. Question 5 — structure of the small-range posets closest to 1/3

Population: the kept low-`δ` records (top-K per `(n, π)` and the annealing witnesses), 142 with
`δ < 0.36` and 33 with `δ < 0.35` (`out/structure.txt`). **EMPIRICAL:**

| property | δ < 0.36 | δ < 0.35 |
|---|---|---|
| width 2 | 132 / 142 | **33 / 33** |
| δ attained at an END pair ({v_1,v_2} or {v_{n−1},v_n}) | 107 / 142 | **33 / 33** |
| δ = M | 107 / 142 | **33 / 33** |
| both extreme elements have exactly one incomparable | **142 / 142** | 33 / 33 |
| displacement antisymmetric (d_i = −d_{n+1−i}) | 84 / 142 | 28 / 33 |
| contains a Lemma-3.2-shape triple | 28 / 142 | 3 / 33 |
| range | 2–6 | 2–4 |

**Reading (EMPIRICAL, with one PROVEN identity):** near 1/3, small range means **width 2 and the
worst pair is at the end**. When `v_1` has exactly one incomparable `w`, a direct count gives
**`δ(v_1, w) = d_1 = 1/(1 + E[k])`** (PROVEN, the special case of §3.1 where `W = {w}`). Here
`k` is the number of slots available to `w` in a uniform extension of `P − {v_1, w}`, and
`1 ≤ k ≤ π(w)`. (Count: `v_1 ≺` everything except `w` by (a), so an extension starts `w, v_1` or starts with `v_1`. There are `e(P−{v_1,w})` of the first kind and `Σ_g k_g` of the second, and `f(v_1) − 1` is the indicator of the first kind.) So `δ` near 1/3 requires `E[k]` near 2, which means `w` is incomparable to `v_1`
and to about one more element on average. That is the (2+1) configuration at the boundary.
Aigner's width-2 extremal case (the (2+1) and its ordinal sums with chains) is the only
exact 1/3 in the data, as expected. The near-extremal posets are width-2 "zig-zags" with range
3–4, the (2+1)-like corner at each end, and an interior arranged so that central pairs balance
WORSE than the ends (the Fibonacci phenomenon, in reverse). Lemma-3.2-shape triples are rare
among them (3/33). The proof side's Case-D machinery is not where these posets live.

## 7. What was NOT done, and negatives

- **Not done:** exhaustive `n = 12` over all ranges; exhaustive `π ≤ 7, 8` beyond `n = 11`,
  `π ≤ 4` beyond 15, `π ≤ 5` beyond 13, `π ≤ 6` beyond 12; annealing beyond `n = 24` (the
  enumerator uses 32-bit masks, `MAXN = 24`); annealing at `D = 7` or `D ≥ 9` as its own cap; any proof of the EMPIRICAL or CONJECTURED items; any re-derivation of
  Lemma 4.2's algebra. The step `α* + β* ≤ v − 2ρ` and the constants 11, 50, 20, 21 were read,
  not re-proved.
- **Negatives, with what was tried:**
  - A poset with `δ < 1/3`: none. Tried: all 46.7 M posets on `n ≤ 11`, all `π ≤ 3` to n=18,
    `π ≤ 4` to 15, `π ≤ 5` to 13, `π ≤ 6` to 12, and annealing `π ≤ 3..6` to n=24.
  - A poset with `M < 0.2857`: none. Tried the same populations plus annealing at `π ≤ 8`. The annealing minimising `M`
    ran with two seeds per `(D, n)`.
  - A violation of (4.1) in any form: none (§4). **The positive control on the lemma could not be run**, because the hypothesis is unsatisfied.
  - A Lemma-4.1 candidate that is not a BFT triple: none for `n ≥ 3`.
