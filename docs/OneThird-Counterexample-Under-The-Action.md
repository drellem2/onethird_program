# A 1/3–2/3 counterexample under the semigroup action

*mg-24a3. Everything numerical here is produced by `code/counterexample_probe_24a3/probe.py`, with the
instrument's own controls in `selftest.py`; the committed outputs are `probe_output.txt` and
`selftest_output.txt`. Regenerate with `code/counterexample_probe_24a3/run_all.sh` — pure Python 3, no
dependencies, about 11 minutes, and both output files reproduce byte-identically. That directory shares no
code with `code/face_geometry/`, `code/hodge_leverage/` or `code/semigroup_note/`: it rebuilds every object
from its definition in exact rational arithmetic, and it reproduces the worked example of
`docs/OneThird-Semigroup-Walk-Family-Note.md` from scratch as a control (C10).*

***Repaired 2026-07-30 by mg-dea5**, landing the three findings of
`docs/OneThird-Counterexample-Under-The-Action-IndependentAudit.md` (mg-a7b4). Three passages changed: §4 and
its two summaries (a false universal, struck, and the signal underneath it re-measured to `n = 8`), §5.2's
Theorem 4 (generalised to every weight), and §2's sampling negative (struck; the smallest majority cycle is
at `n = 9` exactly). Every struck sentence is quoted where it stood rather than paraphrased. The figures in
the repaired passages come from `code/counterexample_repair_dea5/`, which imports nothing from
`probe_24a3/` or `audit_a7b4/`; the reasoning is in
`docs/OneThird-Counterexample-Under-The-Action-Repair.md`. **Nothing else in this document is touched, and
neither headline answer moves.***

---

## 0. The one thing to read first: what is conditional and what is not

**No counterexample to the 1/3–2/3 conjecture is known, and none exists at any size this document reaches.**
Every statement below about a counterexample has the form *if a counterexample exists then …*, and it keeps
that form. Where a real poset is measured it is a real poset. The worst-balanced posets at each `n` are used
as a **stated proxy** and are never called counterexamples — they satisfy `δ = 1/3` exactly, which is the
conjecture holding with equality, not failing.

Seven results are **proved** — Theorem 1 (§2), Proposition 2 (§3.1), Theorem 3 (§5.1), Theorem 4 and
Proposition 5 (§5.2), Proposition 6 (§5.4), Theorem 7 (§5.5). For those, the computations reported alongside
are **checks on the code, not the evidence for the claim**. Everything else in this document is a
measurement over a stated population, and is labelled as one.

**The headline, in four lines.**

1. **A counterexample's majority relation is a linear order `L*` extending `P`** — proved, two lines, and it
   is the object the rest is stated in (§2).
2. **The concentration consequence `E[inv(L,L*)] < |Inc(P)|/3` is not a usable filter**, and this is
   quantified rather than asserted: it is already satisfied by **60.3% of the non-chain posets on 7
   elements**, none of which is a counterexample, the fraction **grows** with `n`, and the posets that
   satisfy it most strongly are this programme's own canonical *unfrozen* family (§3).
3. **The quotient-side signal is real, and `e(P)` explains one of the two statistics and not the other.**
   `qfrac` is fully accounted for by the linear-extension count (`ρ|e` between `−0.01` and `+0.02`). `qmass`
   is **not**: at `ρ|e ≈ −0.27` it survives the control on 6420 posets at `n = 8`, and in all three
   `e`-groups where the comparison is capable of failing, `qmass = 1` picks out **exactly** the `δ`-extremal
   posets — 1 of 7, 3 of 13, 6 of 20 (§4). The three groups share **five cores**, so the honest exact `p` is
   **`1/5`**, not the group-level `1/38760`, and the three sizes are one observation and not three
   (mg-a893). *This
   corrects the original headline, which reported an exact tie; the tie was measured only on `e = 3` groups,
   where every member is extremal by construction (mg-dea5).*
4. **One genuine `e(P)`-independent signal exists** — the action's own balance constant `δ_walk`, computed
   from face counts with no reference to `L(P)`, tracks `δ` with per-pair correlation `0.9945` at `n = 6`.
   It is a **heuristic only**: it is not an inequality in either direction, it already misfires at the `1/3`
   threshold at `n = 6`, and its error grows with `n` while the margin it must resolve shrinks (§5.2).

---

## 1. The terms, and the two statistics

Fix a finite poset `P`. `L(P)` is its set of linear extensions and `e(P) = |L(P)|`. For an incomparable pair
`{x,y}` write

```
    p(x,y) = Pr[ x before y ]      under the UNIFORM measure on L(P),
```

and let `Inc(P)` be the incomparable pairs. The conjecture's statistic is the one in `STATE.md`'s glossary:

```
    delta(P) = max over Inc(P) of min( p, 1-p ).
```

A **counterexample** is a non-chain `P` with `δ(P) < 1/3`; equivalently every incomparable pair has
`p ∉ [1/3, 2/3]`. Following `STATE.md` we call that condition **frozen**.

From the action (the objects are exactly those of `docs/OneThird-Semigroup-Walk-Family-Note.md`, §1): a
**move** is a `P`-compatible ordered set partition, its **commitment level** is the underlying unordered
partition, `Q(P)` is the set of levels ordered by refinement, and `m_X` is the multiplicity determined by
`Σ_{Y level, Y refines X} m_Y = Π_{B ∈ X} e(P|_B)`.

**Populations.** All posets up to isomorphism on `n = 3 … 7` elements: 5, 16, 63, 318, 2045 — verified
against A000112 by two independent enumeration routes (control C1). Chains are excluded from every balance
statement, since they have no incomparable pair and the conjecture says nothing about them. Where
*primitive* posets are used (incomparability graph connected — `STATE.md` row 2, the minimal-counterexample
condition) the population is named at the point of use.

---

## 2. THEOREM: a counterexample's majority relation is a linear order

This section is Daniel's bridge object. It is a theorem, and the proof is due to Daniel (relayed by
pm-onethird); it is reproduced because the rest of the document is stated in terms of its conclusion.

> **Theorem 1.** Let `P` be a counterexample. Orient every pair by its majority: `x → y` iff `p(x,y) > 2/3`.
> Then `→` is a strict linear order on the ground set, and it extends `P`. Call it `L*`; it is a linear
> extension of `P`.

*Proof.* **Total.** `1/2` lies in the forbidden band `[1/3, 2/3]`, so no pair is tied and every pair is
oriented one way. Comparable pairs have `p = 1` and orient with `P`.

**Transitive.** Suppose `x → y` and `y → z`. Then

```
    Pr[ x<y AND y<z ]  >=  p(x,y) + p(y,z) - 1  >  2/3 + 2/3 - 1  =  1/3,
```

and `{x<y and y<z} ⊆ {x<z}`, so `p(x,z) > 1/3`. The hypothesis forbids `p(x,z) ∈ [1/3, 2/3]`, so
`p(x,z) > 2/3`, i.e. `x → z`.

A total, transitive, antisymmetric relation is a strict linear order; it contains `P`, so it is a linear
extension of `P`. ∎

**What is load-bearing, and it is worth naming.** The **forbidden middle band** closes the composition. The
weaker hypothesis "every pair has a majority" does **not** give transitivity: majority relations on linear
extensions of a general poset genuinely do have directed cycles. Both facts are checked here, and the second
one is the reason the first has to be argued rather than assumed:

- **Exhaustively, no majority cycle occurs on any poset with `n ≤ 8`** — 0 of 19,446, of which 19,440 are
  non-chains, ties included. *(Extended from `n ≤ 7` / 0 of 2447 by mg-dea5,
  `code/counterexample_repair_dea5/cycles.py`.)* That is a fact about a
  population where the counterexample hypothesis is *false*, so it is **not** evidence for Theorem 1 and is
  not offered as any. Theorem 1 needs no evidence; it has a proof.
- **A majority cycle does exist for general posets.** Witness at `n = 11`, rebuilt and re-verified in
  `probe_output.txt` §1a′ from its cover relations
  `0<2 0<6 0<9 1<3 1<9 2<10 3<6 3<7 4<5 4<6 6<10` (`e(P) = 78474`), with the 3-cycle `5 → 9 → 6 → 5` and
  margins

  | edge | `p` | as a decimal |
  |---|---|---|
  | `p(5,9)` | `597/1189` | 0.50210 |
  | `p(9,6)` | `599/1189` | 0.50378 |
  | `p(6,5)` | `1784/3567` | 0.50014 |

  Every edge is decided by a margin of about `1/2` — **inside** the band a counterexample forbids. So the
  cycle is real, and Theorem 1 excludes it for exactly the stated reason.

  > **STRUCK (mg-dea5, landing mg-a7b4 finding 3).** This paragraph previously read: *"Found by random
  > search (seed 4242); no cycle in 4200 random posets at each of `n = 8, 9, 10`. **`n = 11` is not claimed
  > to be minimal** — only that a witness exists, and hence that the exhaustive range is too small to see
  > one."* The negative was **false at `n = 9` and at `n = 10`**, and the search that produced it was not in
  > the committed instrument, so `run_all.sh` reproduced the printing of the sentence and `check_doc.py`
  > compared a string against a `print` statement. Replaced by the exhaustive statement below, which
  > `code/counterexample_repair_dea5/cycles.py` produces in full.

  **The smallest `n` carrying a majority cycle is exactly 9.** Exhaustively over every isomorphism class,
  ties included: **no cycle at `n ≤ 8`** — 19,440 non-chain posets, 16,998 of them at `n = 8` alone, the
  whole population and not a sample. At `n = 9` a cycle **exists**: `0<5 0<8 1<4 1<6 2<3 2<7 3<6 4<8 5<7`,
  `e(P) = 1431`, tie-free, no isolated element, 3-cycle `0 → 2 → 1 → 0` with all three margins exactly
  `80/159`, and no single-element deletion preserves it — consistent with the exhaustive `n = 8` sweep. At
  `n = 10` a cycle exists too, and it is the `n = 11` witness above with its **isolated element 8** deleted:
  `e(P) = 7134` (and `78474 = 11 × 7134`), identical pair probabilities, same 3-cycle. **So `n = 11` is not
  minimal, `n = 10` is not minimal, and `n = 9` is.** The same instrument also re-runs the sampling negative
  — 4200 samples at each of three densities at `n = 9`, seed 4242, **0 cycles** — and prints it
  directly beneath the witness, because that is the shape of the defect: a negative with a sample size on it
  reads as evidence, and here the phenomenon is rarer than any sampler of that size reaches while being
  present.

The methodological point is the one the corrected brief makes: an imported general caveat is not an
obstruction until it is checked against the strength of the specific hypothesis. Here the `n ≤ 7` sweep
would have been read as support for a general transitivity claim that is **false**.

---

## 3. The concentration quantity, and why it does not filter

### 3.1 The identity

> **Proposition 2.** For any `L*` extending the strict majority relation of any poset `P`,
> ```
>     E_{L ~ uniform on L(P)} [ inv(L, L*) ]  =  sum over Inc(P) of min( p, 1-p ),
> ```
> where `inv(L,L*)` counts the pairs on which `L` and `L*` disagree. In particular the left side does not
> depend on the choice of `L*` among the completions of the majority relation.

*Proof.* `L` disagrees with `L*` on a comparable pair never, and on an incomparable pair exactly when `L`
takes the minority side, which has probability `min(p, 1-p)`. Sum over pairs. A tied pair contributes `1/2`
whichever way `L*` orients it, which is the tie-break independence. ∎

Verified against direct enumeration of `L(P)` on all 398 non-chain posets with `n ≤ 6`, and the tie-break
independence verified against a second, differently-constructed completion (`probe_output.txt` §1c).

Define the normalised form of the addendum's bound:

```
    R(P) := E[inv(L,L*)] / ( |Inc(P)| / 3 )  =  3 * MEAN over Inc(P) of min(p,1-p).
```

**If a counterexample exists then `R(P) < 1`.** This is immediate from Proposition 2 and the hypothesis, and
it is a *consequence*, not a test — the brief says so and that is correct. Note also

```
    R(P) <= 3 * delta(P)          because a mean is at most a max,
```

so `R < 1` is strictly weaker than the counterexample condition `3δ < 1`. The contribution of this section
is **how much** weaker.

### 3.2 It is already satisfied by posets that are provably not counterexamples

| `n` | non-chains | `min 3δ` | `min R` | `#R < 1` | `%R < 1` | `#3δ < 1` |
|---|---|---|---|---|---|---|
| 3 | 4 | `1` | `1` | 0 | 0.0% | **0** |
| 4 | 15 | `1` | `1` | 0 | 0.0% | **0** |
| 5 | 62 | `1` | `4/5` | 11 | 17.7% | **0** |
| 6 | 317 | `1` | `3/4` | 124 | 39.1% | **0** |
| 7 | 2044 | `1` | `24/35` | **1232** | **60.3%** | **0** |

Read the last two columns together. `#3δ < 1` is `0` everywhere — no counterexample exists at these sizes,
as expected, and `min 3δ = 1` says the conjecture is **tight** at every `n` reached. `#R < 1` is not `0`: at
`n = 7`, **1232 posets satisfy the concentration condition and none of them is a counterexample**, and the
satisfying fraction rises monotonically with `n`.

### 3.3 The mechanism, and the family that makes it worst

`R` is `3 ×` the **mean** and `3δ` is `3 ×` the **max** of the same per-pair numbers. A poset with many
heavily-decided pairs and a few balanced ones has a small mean while its max stays large. The extreme case
is a disjoint union of two chains, which is this programme's own canonical **unfrozen** family
(`STATE.md`: `C_n ⊔ C_n` has `δ = 1/2`, maximally unfrozen). Exactly computed past the exhaustive range:

| family | `n` | `e(P)` | `3δ` | `R` | `R < 1`? |
|---|---|---|---|---|---|
| `C_2 ⊔ C_2` | 4 | 6 | `3/2` | `1` | no |
| `C_3 ⊔ C_3` | 6 | 20 | `3/2` | `4/5` | **yes** |
| `C_4 ⊔ C_4` | 8 | 70 | `3/2` | `24/35` | **yes** |
| `C_5 ⊔ C_5` | 10 | 252 | `3/2` | `64/105` | **yes** |
| `C_6 ⊔ C_6` | 12 | 924 | `3/2` | `128/231` | **yes** |
| `1+2` under `C_k` | 3…9 | 3 | **`1`** | **`1`** | no |

The bottom row is the family that **meets the conjecture's bound**: `δ = 1/3` exactly at every `n`. Its `R`
is exactly `1` at every `n` — it sits **on** the concentration boundary and never inside it. Meanwhile
`C_6 ⊔ C_6`, with `δ = 1/2` — the most balanced a poset can be, the furthest possible from frozen —
satisfies the concentration condition with about 45% slack.

**So the answer to the addendum's own question is the one it named as likelier.** The near-extremal families
do not approach the bound from the satisfying side; they sit exactly on it, while posets far from
extremal sit deep inside it. The reason is structural — mean versus max — not a matter of the computable
range being too small, and the slack grows with `n`. `R(P) < 1` is a true necessary condition and is not a
usable constraint on the search space.

---

## 4. The quotient side: two statistics, and `e(P)` explains only one of them

*(Heading repaired by mg-dea5. It read "a real effect, entirely explained by `e(P)`"; that is true of
`qfrac` and false of `qmass`.)*

`L*` singles out one chain inside `Q(P)`: the partitions whose blocks are contiguous **intervals** of `L*`.
There are exactly `2^{n-1}` of them and every one is a level, because ordering those blocks along `L*` is
`P`-compatible (asserted in code, so a failure would abort the run). Two statistics, both `1` for a chain:

```
    qfrac = 2^(n-1) / |Q(P)|                        share of the LEVELS
    qmass = ( sum of m_X over those levels ) / e(P)  share of the SPECTRUM
```

**Population: the tie-free non-chain posets.** A counterexample is tie-free (§2), and on a tie-free poset
`L*` is unique, so both statistics are canonical; on a poset with a tied pair they would depend on the
tie-break and are not well defined. Those posets are excluded and counted. *(mg-dea5: tie-freeness alone is
not sufficient — the majority relation must also be acyclic for `L*` to exist. Both instruments check it
rather than assume it, and it holds for every poset at `n ≤ 8`; the count of posets excluded on that ground
is 0 at every `n`, which is why the population sizes are unaffected.)*

**Raw effect — present, and in the predicted direction.** Comparing the `δ`-extremal posets against the
whole rest of the population at the same `n` (the size-matched null the brief requires, taken entire rather
than sampled):

| `n` | tie-free | `#extremal` | `qmass` extremal vs rest | `z` | `qfrac` extremal vs rest | `z` |
|---|---|---|---|---|---|---|
| 5 | 16 | 3 | 1.000 vs 0.825 | +1.16 | 0.642 vs 0.446 | +2.90 |
| 6 | 88 | 5 | 1.000 vs 0.734 | +1.95 | 0.590 vs 0.316 | +3.40 |
| 7 | 671 | 8 | 1.000 vs 0.593 | **+2.64** | 0.541 vs 0.203 | **+4.49** |
| 8 | 6420 | 12 | 1.000 vs 0.461 | **+3.72** | 0.505 vs 0.120 | **+6.91** |

*(The `n = 8` row is mg-dea5's; every other cell is mg-24a3's and reproduces exactly.)*

**One control dissolves it and the other does not, and which is which depends on the statistic.**

*Saturation.* `qmass` is bounded above by `1`, and every extremal poset attains it. "Extremal posets have
`qmass = 1`" is informative only if reaching `1` is rare, and the saturating club is large and mostly not
extremal: 6 of 16 posets at `n = 5` (50.0% of them extremal), 11 of 88 at `n = 6` (45.5%), 20 of 671 at
`n = 7` (40.0%), 36 of 6420 at `n = 8` (33.3%). This control stands and nothing below weakens it — it is a
statement **across** `e`-groups, and it turns out to be compatible with an exact separation **inside** one.
Note also what it says about selectivity: the club is `37.5%`, `12.5%`, `3.0%`, `0.6%` of the population at
`n = 5 … 8`.

*Controlling for `e(P)`.* Compare each extremal poset only against tie-free posets with the **same**
linear-extension count.

> **STRUCK (mg-dea5, landing mg-a7b4 finding 1).** This paragraph previously continued: *"Every extremal
> poset is rank 1 — and **tied with every other member of its group**: rank 1 of 3 tied with 2 at `n = 5`,
> rank 1 of 4 tied with 3 at `n = 6`, rank 1 of 5 tied with 4 at `n = 7`."* And the verdict box previously
> read: *"**Verdict on the quotient side: NULL, quantified.** The association between `qmass` and extremality
> is real as a raw correlation and is entirely accounted for by the linear-extension count. Within a fixed
> `e(P)` the statistic does not distinguish the extremal posets from anything at all — not weakly, but by an
> exact tie."* **The rank claim is true 16 of 16. The tie claim is false, and the verdict is false.** The
> nine rows printed were all `e = 3` groups — the reporting loop broke after three rows per `n` and skipped
> groups of size `< 3` — and an `e = 3` group is **vacuous by construction**: every member of it is
> extremal, so the tie could not fail. In every group where it *could* fail, it does. The full
> re-measurement is `docs/OneThird-Counterexample-Under-The-Action-Repair.md`.

**Rank 1: 16 of 16, and trivially so** — extremal posets have `qmass = 1`, which is the maximum. **Tied with
every other member of its group: 12 of 16.** The four exceptions are the extremal posets with `e(P) = 9`.

**Vacuity, which is why the control had nothing in it.** Call an `e`-group **vacuous** if every member of it
is `δ`-extremal, so that a tie is incapable of failing. Every non-chain `P` with `e(P) = 3` has `δ(P) = 1/3`
exactly — for an incomparable pair the two augmented counts are positive integers summing to `3`, hence
`{1,2}` — so **every `e = 3` group is vacuous**, and those are the only groups the instrument printed.
(Verified on all `1, 2, 3, 4, 5, 6` non-chain posets with `e = 3` at `n = 3 … 8`.) Non-vacuous means the
group contains an extremal **and** a non-extremal member.

**Every group containing an extremal poset, no cap and no size floor, out to `n = 8`.** The `e`-values
carrying extremal posets are `3` and `9` at every `n` reached; `e = 3` is always vacuous, so the whole
testable evidence is the `e = 9` groups:

| `n` | `e(P)` | group size `N` | extremal `k` | `qmass = 1` in it | separation | group-level `p` | AUC | distinct cores | core-level `p` |
|---|---|---|---|---|---|---|---|---|---|
| 5 | 3 | 3 | 3 | 3 | *vacuous* | — | — | 1 | — |
| 6 | 3 | 4 | 4 | 4 | *vacuous* | — | — | 1 | — |
| 7 | 3 | 5 | 5 | 5 | *vacuous* | — | — | 1 | — |
| 8 | 3 | 6 | 6 | 6 | *vacuous* | — | — | 1 | — |
| 6 | **9** | 7 | 1 | 1 | **perfect** | `1/7` | `1` | 5 | **`1/5`** |
| 7 | **9** | 13 | 3 | 3 | **perfect** | `1/286` | `1` | 5 | **`1/5`** |
| 8 | **9** | 20 | 6 | 6 | **perfect** | `1/38760` | `1` | 5 | **`1/5`** |

*Perfect* means both inclusions: the `qmass = 1` members are **exactly** the extremal ones, so no
non-extremal member of the group reaches `1` (the others sit at `8/9` or `2/3`). `p` is exact — every one of
the `C(N,k)` random-label assignments is enumerated. **`n = 7` generated this hypothesis and `n = 6` was in
the same table, so the test is `n = 8`**, where the pre-specified family has size **1** because there is
exactly one non-vacuous group: `p = 1/38760 = 2.6 × 10⁻⁵`. Bonferroni over all three non-vacuous groups
gives `≤ 7.7 × 10⁻⁵`; over all seven groups containing an extremal poset, counting the vacuous ones as if
they had been testable, `≤ 1.8 × 10⁻⁴`.

> **CORRECTED (mg-a893, landing mg-0a11's audit of the mg-dea5 repair).** **The group-level `p` is not the
> strength of this result and the last two columns are what to read.** Every member of the `n = 7` and
> `n = 8` groups is a smaller member with a **cut element** — an element comparable to everything —
> adjoined, and `δ` and `qmass` are inherited along that operation (a one-line theorem for `δ`; measured,
> 257 of 257, for `qmass`). The `n = 8` group is *exactly* the cut extensions of the `n = 7` group. So the
> three groups carry **five distinct cores between them, of which exactly one is extremal**, at all three
> sizes, and **the honest exact `p` is `1/5`** — the same `1/5` three times. The three group-level figures
> are one observation re-counted with more chain elements glued on, they are not independent, and no joint
> probability may be formed from them. What is *not* corrected: the separation is real, it is perfect in
> both inclusions wherever it could fail, and mg-0a11 carried it to `n = 11` and it holds there too.
> `code/counterexample_repair_dea5/cores.py` → `out_cores.txt`, and §3.4 of the repair document.

**And the powered test, on the whole population rather than the extremal dichotomy.** Pooled within-`e`
association between `qmass` and `δ`, i.e. exactly the `ρ|e` column of §6 computed for the two statistics §6
omits:

| `n` | population | `e`-groups | `qmass` `ρ|e` | `qfrac` `ρ|e` | `qmass` Kendall `τ_b` | perm `p` |
|---|---|---|---|---|---|---|
| 6 | 88 | 27 | **−0.287** | −0.009 | −0.2978 | 0.0800 |
| 7 | 671 | 127 | **−0.261** | +0.011 | −0.2626 | 0.0050 |
| 8 | 6420 | 670 | **−0.273** | +0.018 | −0.2052 | 0.0050 |

`ρ|e` is computed by §6's own recipe; the permutation `p` has a floor of `1/200 = 0.005` at 199 reps. **Every one of the nine invariants in §6's table is within `±0.10`;
`qmass` is at `≈ −0.27` and stable in `n`.** The sign is the predicted one: more of the spectrum on `L*`'s
chain goes with a **worse-balanced** poset. `qfrac` — whose *raw* effect is the larger of the two
(`z = +4.49` at `n = 7`, `+6.91` at `n = 8`) — **is** null after the control, exactly as this section
claimed for both.

> **Corrected verdict on the quotient side: NOT a null for `qmass`, and a null for `qfrac`.** The `qfrac`
> effect is entirely the linear-extension count. The `qmass` effect is not: within a fixed `e(P)` it survives
> at `ρ|e ≈ −0.27` on 6420 posets at `n = 8`, and in all three `e`-groups where an exact tie was capable of
> failing, `qmass = 1` picks out **exactly** the extremal posets. What this is **not**: it is not a statement
> about counterexamples (the extremal posets satisfy `δ = 1/3`, the conjecture holding with equality); it is
> not a filter (`qmass = 1` still retains 36 of 6420 posets at `n = 8`, only a third of them extremal, and
> `qmass` costs more to compute than `δ`); and it is not explained (`qmass = 1` holds iff every
> positive-multiplicity level is an `L*`-interval partition, and why that should coincide with `δ = 1/3`
> inside an `e`-group is open). Three groups is three groups.

---

## 5. Necessary conditions in this language

Each item states what it is: a theorem, or a faithful translation of something the programme already has, or
a measurement. Translations are labelled as such — an exact restatement that exposes a new handle has value,
but it is not new content and is not priced as if it were.

### 5.1 What the level and multiplicity data can express — and it is exactly convex restrictions

> **Theorem 3.** Every block of every commitment level of `P` is **convex** in `P` (`i < j < k` with
> `i,k ∈ B` forces `j ∈ B`). Moreover for a subset `B`, the partition `{B} ∪ singletons` is a level **iff**
> `B` is convex.

*Proof.* A block `B` and an outside element `j` with `i < j < k` for `i,k ∈ B` gives arrows `B → {j}` and
`{j} → B` in the quotient, a 2-cycle, so the partition is not acyclic and is not a level (the level
description is the theorem of the semigroup note, §8). Conversely if `B` is convex then any cycle through
`B` in the quotient by `{B} ∪ singletons` would give `i < j₁ < ⋯ < jₘ < k` with `i,k ∈ B` and the `j`'s
outside, hence `i < j₁ < k` with `j₁ ∉ B`, contradicting convexity; cycles avoiding `B` lie among singletons
and would contradict `P` being a poset. ∎

Verified: 0 bad of 3,246,401 (level, block) pairs and 0 bad of 281,977 (poset, subset) pairs, `n = 3…7`.

**The consequence, which is the useful part.** `m_X` is determined by the numbers `e(P|_B)` for `B` a block
of a level, by downward induction from the finest level. With Theorem 3 that means:

> Any necessary condition on a counterexample derivable from `(Q(P), m)` is a condition on the function
> `B ↦ e(P|_B)` over **convex** subsets `B`.

The frozen condition is not of that shape. It is a condition on `{x<y} ↦ e(P ∪ {x<y})` over incomparable
pairs — and `P ∪ {x<y}` is a *relation extension*, not an induced subposet. This locates the boundary
exactly, and §5.5 measures the gap it leaves.

### 5.2 The spectral gap is a pair statistic of exactly the same shape as `δ`

> **Theorem 4.** For **any** probability weight on the `P`-compatible moves and any non-chain `P`,
> ```
>     lambda_2  =  max over incomparable pairs {x,y} of  s(x,y),
> ```
> where `s(x,y)` is the probability that a move drawn from the weight leaves `x` and `y` in the same block,
> and `λ₂ = max{ λ_X : m_X > 0, X ≠ the finest partition }`.

*(**Generalised (mg-dea5), landing mg-a7b4 finding 2.** This was stated for the weight uniform on all moves.
The proof below uses only that `λ_X` is non-increasing as `X` coarsens — true for any distribution on moves —
and that `m_X` is a combinatorial invariant of `P`. Neither mentions the weight, so the hypothesis is
removable, and the general form is the one §5.5 needs, since §5.5's whole argument is about weights other
than the uniform-move one. Under `w_t` the theorem reads `λ₂ = t = max_{x∥y} s_{w_t}(x,y)`, which is exactly
what Theorem 7's proof computes by hand. Verified on **972 (poset, weight) cases, 891 of them non-uniform,
0 failures**, of which **228 are checked against the actual transition matrix** in exact rationals via
`trace(Mᵏ) = Σ_X m_X λ_Xᵏ` for all `k` — which pins the whole spectrum, not just `λ₂`.)*

*Proof.* `λ_X` is non-increasing as `X` coarsens, so `λ₂` is attained at a finest level above the bottom
carrying positive multiplicity. If every block of `X` is a chain then `Π_B e(P|_B) = 1`, and the bottom level
already contributes `1`, so `m_X = 0` for every such `X` other than the bottom itself. Hence a level with
`m_X > 0` and `X ≠ bottom` has a block containing an incomparable pair `{x,y}`, and `Z = {x,y} ∪ singletons`
refines `X`, is a level, and has `m_Z = e(P|_{x,y}) − 1 = 1`. So `λ₂` is attained at such a `Z`, and
`λ_Z = s(x,y)` because a move's level is coarser than or equal to `Z` exactly when it does not separate the
pair. ∎

Verified: 0 bad of 2442 non-chain posets, `n = 3…7`, under the uniform-move weight; 0 bad of 972
(poset, weight) cases over the weight families above. The supporting multiplicity fact (0 bad of 65,481
all-chain levels other than the finest; the finest always has `m = 1`) is **structural** rather than
measured: `m_X = Π_{B ∈ X} M(P|_B)` with `M(R) := m_{top(R)}`, and `M` vanishes on every chain of `≥ 2`
elements (`code/counterexample_repair_dea5/levels.py`, control C7).

So `δ` and `λ₂` are maxima over incomparable pairs of two different per-pair numbers — the **skew** of the
separating-move measure and the **mass** of the non-separating moves. **These are independent coordinates of
the same triple** `(s, q, q′)`: fixing `s` leaves the skew free and vice versa. That is the structural
reason the spectrum does not see balance, and §6 measures it.

**And this yields the one genuine `e(P)`-independent signal in the probe.** The walk's stationary pair
marginal is exact and needs no linear extensions:

> **Proposition 5.** For any weight on moves, the stationary pair marginal satisfies
> `π(x<y) = q(x<y) + s·π(x<y)`, hence `π(x<y) = q(x<y) / (q(x<y) + q(y<x))`.

Verified against the exact stationary vector of the actual transition matrix (control C8, 0 bad of 52
pairs). Define, in exact parallel with `δ`, `δ_walk(P) = max over Inc(P) of min(π, 1−π)`. Then at `n = 6`:

- per-pair Spearman `ρ(min(p,1−p), min(π,1−π)) = 0.9945` over all 2195 incomparable pairs of all 317
  non-chain posets, mean `|error| = 0.00939`;
- per-poset, on **all 317 non-chains**, `ρ(δ, δ_walk) = 0.9855` and **`0.8919` after controlling for
  `e(P)`**; on the **184 primitive non-chains** (the minimal-counterexample population, which is what §6's
  table uses) `ρ = 0.975` and **`0.849` controlled** — every other invariant in §6 collapses to
  `|ρ|e| ≤ 0.10` under the same control;
- as a one-sided filter, `δ_walk ≤` the extremal value retains **0.5%** of the primitive population at
  `n = 6`, the most selective heuristic anywhere in this probe.

**It is a heuristic and nothing more, for three measured reasons.** (i) It is **not an inequality in either
direction**: at `n = 6`, 759 of 2195 pairs have `min(π,1−π) > min(p,1−p)` and 37 of 317 posets have
`δ_walk > δ`, so it can neither certify `δ ≥ 1/3` nor witness `δ < 1/3`. (ii) It **already misfires at the
threshold**: at `n = 6` the primitive poset `0<2 0<3 1<2 2<4 3<4 3<5` has `δ_walk = 12/37 < 1/3` while
`δ = 5/14 ≥ 1/3` — a false positive, with no true positives available anywhere. (iii) The **error grows
while the margin shrinks**: max per-pair error `1/40`, `5/132`, `5/114` at `n = 4, 5, 6`, against a margin
`min δ − 1/3 = 0` at every `n`, because the extremal posets sit exactly at `1/3`. So the approximation
degrades precisely where it would have to be sharp.

### 5.3 Primitivity is exactly positive excess at every 2-block level — a translation

The 2-block levels are exactly `{A, Aᶜ}` with `A` a nontrivial order ideal or filter (0 bad of 139,765
2-block partitions). For such a level define the **excess**

```
    excess({A,A^c})  :=  e(P) - e(P|_A) e(P|_{A^c})  =  sum of m_Y over levels Y that do NOT refine it
```

— the identity holding because `Σ_{Y refines X} m_Y = Π_B e(P|_B)` and `Σ_{all Y} m_Y = e(P)` (0 bad of
139,765 levels). Then:

> `P` is **primitive** ⟺ **every** 2-block level has strictly positive excess.

Verified, 0 bad of 2447 posets. Since minimal counterexamples are primitive (`STATE.md` row 2), a minimal
counterexample must have strictly positive excess at every 2-block level.

**Priced honestly: this is a faithful translation, not new content.** `e(P) = e(P|_A)·e(P|_{Aᶜ})` for a
nontrivial ideal `A` iff `P = P|_A ⊕ P|_{Aᶜ}`, so the condition is exactly "not an ordinal sum", which is
exactly the ledger's row 2. Its value is expressibility — the condition lives on the 2-block levels of
`Q(P)`, where the multiplicity identity can read it — and nothing more.

### 5.4 Frozen forces `e(P) ≥ 4`, and the extremal posets are not near-misses there

> **Proposition 6.** If `P` is frozen then `e(P) ≥ 4`.

*Proof.* For an incomparable pair, `e(P ∪ {x<y})` and `e(P ∪ {y<x})` are positive integers summing to
`e(P)`, and frozenness requires the smaller to be `< e(P)/3`, so `e(P) > 3·1`. ∎

Trivial, but it is a **genuine constraint and not a translation**, and it prices the proxy: most of the
`δ`-extremal posets have `e(P) = 3` — 1 of 1 at `n = 3`, 2 of 2 at `n = 4`, 3 of 3 at `n = 5`, 4 of 5 at
`n = 6`, 5 of 8 at `n = 7`. So **if a counterexample exists it does not resemble the extremal posets in the
coordinate the multiplicity identity reads off**, and the extremal posets are not near-misses in it. That is
a real limit on how far the proxy can be trusted, and it applies to every measurement in this document that
uses it.

### 5.5 The exact reformulation, and the no-free-lunch obstruction

Let `W_unif(P)` be the set of weights whose walk has the uniform measure on `L(P)` as its stationary law —
i.e. the weights that carry the measure the conjecture is about. It is nonempty: the weight uniform on the
finest moves (the linear extensions read as moves) jumps to a uniform random linear extension in one step.
For `w ∈ W_unif(P)`, Proposition 5 gives `p(x<y) = q_w(x<y)/(q_w(x<y)+q_w(y<x))`, so

> **`P` is a counterexample ⟺ `P` is not a chain and for every incomparable pair `{x,y}`,
> `min(q_w, q′_w) < (1/3)(q_w + q′_w)`** — the moves that *separate* the pair are more than `2:1` lopsided.

This is an exact reformulation in the action's own coordinates. It is an equivalence, hence a translation
and not a constraint by itself.

> **Theorem 7 (no free lunch for spectral detection).** For every non-chain `P` and every `t ∈ [0,1]`, the
> weight `w_t = t·(do-nothing) + (1−t)·(uniform on the finest moves)` lies in `W_unif(P)` and has
> `λ₂(w_t) = t`. Hence `δ(P)` is the **same** for every weight in `W_unif(P)` while `λ₂` sweeps all of
> `[0,1]`.

*Proof.* Row sums: the do-nothing move fixes every state, contributing `t`; a finest move sends every state
to itself-as-an-ordering, so the finest moves contribute `(1−t)·e(P)/e(P) = 1−t`. Total `1`, and the columns
sum to `1` always, so the uniform vector is stationary. The finest moves have level = bottom, which is not
coarser than any `X ≠ bottom`, and the do-nothing move's level is the top, coarser than everything; so
`λ_X = t` for every `X ≠ bottom`, and some such `X` has `m_X > 0` whenever `e(P) > 1`. ∎

Verified, 0 bad of 57 (poset, `t`) cases at `n ≤ 4`, against the actual matrix in exact arithmetic.

**Consequence.** No spectral quantity of a measure-correct walk can be a function of `δ`. A spectral
detector must pin the weight by a rule **outside** the stationarity requirement — and the only canonical
weight the action supplies without extra input, the uniform-move weight, is **not** in `W_unif(P)`: at
`n = 6` only 717 of 2195 pairs have `min(π,1−π) = min(p,1−p)` exactly, with a worst gap of `5/114`. That is
the honest statement of the obstruction, and it is why §5.2's signal is an approximation rather than an
identity.

---

## 6. The spectral-separation sweep, as a quantified null

The original brief asked whether the worst-balanced posets separate from the rest on the quotient-lattice
and spectral invariants. The addendum calls this a fishing expedition and is right that nothing predicts
which invariant should move. It is reported because a clean quantified null closes a route cheaply.

**Method.** Five invariants of increasing fineness — `I0` `e(P)` alone (the control); `I1` level count and
level-size profile; `I2` `+` multiplicity profile; `I3` `+` the exact spectrum with multiplicities under the
uniform-move weight; `I4` the full relabelling-invariant `(Q(P), m, move-count)` fingerprint — used to
partition the population into fibers. **The null model is the population's own resolution:** the fraction of
*all* posets already alone in their fiber, and the probability that two random members collide. At `n = 6`,
primitive non-chains, `N = 184`:

| rung | #fibers | `P[collide]` | %singleton |
|---|---|---|---|
| `I0` | 54 | 0.0219 | 5.4% |
| `I1` | 88 | 0.0094 | 13.0% |
| `I2` | 111 | 0.0043 | 20.7% |
| `I3` | 111 | 0.0043 | 20.7% |
| `I4` | 111 | 0.0043 | 20.7% |

`I3` adds **nothing** to `I2`: the exact spectrum under the canonical weight refines the multiplicity
profile not at all, on this population. `I4` is not a complete invariant of the poset — 73 non-singleton
fibers at `n = 6`.

**Correlations, with the control that matters.** Spearman `ρ` with `δ`, and the same correlation computed
within groups of equal `e(P)` and pooled (`ρ|e`), at `n = 6`:

| invariant | `ρ` | perm `p` | `ρ|e` |
|---|---|---|---|
| `e(P)` (control) | 0.400 | 0.0005 | — |
| `#levels` | 0.374 | 0.0005 | **0.079** |
| `#levels with m>0` | 0.379 | 0.0005 | **−0.068** |
| `#moves` | 0.403 | 0.0005 | **−0.094** |
| `max m_X` | 0.518 | 0.0005 | **0.075** |
| `λ₂` | −0.139 | 0.0565 | **0.075** |
| `s_max` | −0.139 | 0.0565 | **0.075** |
| sign imbalance | −0.599 | 0.0005 | **−0.078** |
| width (structural control) | 0.508 | 0.0005 | 0.046 |
| **`δ_walk`** | **0.975** | 0.0005 | **0.849** |

> **Verdict: NULL, quantified — with one exception.** Every quotient-lattice and spectral invariant in the
> table has a partial correlation within `|ρ|e| ≤ 0.10`, against raw correlations ranging from `−0.599` to
> `+0.518` in magnitude — i.e. essentially all of the apparent association is the linear-extension count,
> which `STATE.md` already tracks as `log e(P)`. `λ₂` is additionally the weakest raw predictor in the table
> and the only entry that fails significance (`p = 0.0565` at `n = 6`, and `ρ = −0.020`, `p = 0.4268` at
> `n = 7`). The single exception is `δ_walk` (§5.2), which is not a quotient-lattice invariant but the
> action's own pair marginal, and which is a heuristic for the three measured reasons given there.

**Does it sharpen or wash out?** It washes out, and the resolution goes the *opposite* way from what a
detector would need. On the primitive non-chains, the fraction of posets alone in their `I4` fiber **falls**
with `n`:

| `n` | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| `N` | 4 | 7 | 31 | 184 | **1351** |
| `I4` % singleton | 50.0% | 71.4% | 35.5% | 20.7% | **7.3%** |
| `I4` non-singleton fibers | 1 | 1 | 10 | 73 | **626** |

So posets become *less* distinguishable by the full fingerprint as `n` grows, while the concentration bound
of §3 loosens monotonically and the `δ_walk` error of §5.2 grows. Every trend in this document points the
same way.

**One honest positive, and it is not a route.** Among all those fibers — including the 626 non-singleton
ones at `n = 7` — **not one contains two posets with different `δ`**. So this document does **not** establish
that the quotient data fails to determine `δ`; no collision witness was found at any `n ≤ 7`, and the
question of whether `(Q(P), m)` determines `δ` in general is left open here. What it does establish is
narrower and is the operative point: **`I4` is not a shortcut even if it does determine `δ`.** Computing it
requires `e(P|_B)` for every convex `B` (§5.1), which strictly subsumes the `O(2ⁿ·n)` count DP that yields
`δ` directly — so it is more expensive than the thing it would detect. The invariants that *are* cheaper
than `δ` — level counts, profiles, `λ₂` — are exactly the ones with partial correlation `≈ 0`.

---

## 7. The isoperimetric question, stated as a question

If a counterexample `P` exists, its uniform measure on `L(P)` has `E[inv(L,L*)] < |Inc(P)|/3` while being
supported on all `e(P)` chambers of the adjacent-transposition graph, whose degree is at most `n−1`. **Does
"most of the mass in a small inversion-ball, spread over many chambers of a bounded-degree graph" force a
contradiction?**

**The argument actually available, and it is not enough.** Unconditionally only Markov applies:
`Pr[inv ≥ t·|Inc|/3] ≤ 1/t`, so at least half the mass lies within `inv < 2|Inc|/3`. With
`|Inc| ≤ n(n−1)/2` that radius is up to `n(n−1)/3` — about two-thirds of the maximum possible inversion
count, not a small ball. The number of permutations with fewer than that many inversions is a constant
fraction of `n!`, so no counting contradiction follows. `probe_output.txt` §7 prints the radius and the exact
ball mass on the extremal and largest-`e` posets at each `n ≤ 6` to show the looseness is real and not an
artefact of the bound's algebra.

**What would be needed, and where it already lives.** Shrinking the radius from `2|Inc|/3` to `c|Inc|` with
`c` small needs a concentration inequality for `inv(L,L*)` under the linear-extension measure. The `|Inc|`
pair-indicators are not independent, and their correlation structure is exactly the FKG/XYZ
same-side-covariance obstruction `STATE.md` already carries as the `(B-cov)` half of the open `(B)`
obligation. **So this question reduces to an obligation the ledger already records as open. It is written
down as a question with its gap named, and it is not offered as a route.**

---

## 8. Summary

1. **Theorem.** If a counterexample exists, its majority relation is a linear order `L*` extending `P`
   (§2). The forbidden middle band is what closes the composition; majority cycles are real for general
   posets and are excluded here by that band. **The smallest such cycle is at `n = 9` exactly**: none at
   `n ≤ 8` exhaustively (19,440 non-chains, ties included), a verified witness at `n = 9`, and the `n = 11`
   witness reduces to `n = 10` by deleting its isolated element (mg-dea5). The exhaustive sweep finding no
   cycle is about a population where the counterexample hypothesis is false and is **not** evidence for the
   theorem.
2. **The concentration consequence does not filter.** `R(P) = 3E[inv(L,L*)]/|Inc(P)| < 1` is necessary and
   is satisfied by 60.3% of non-chain posets at `n = 7`, none of them counterexamples; the fraction grows
   with `n`; the family meeting the conjecture's bound sits exactly **on** the boundary while
   maximally-unfrozen two-chain posets sit deep inside it. Mechanism: mean versus max (§3).
3. **The quotient side splits: `qfrac` is null after control, `qmass` is not.** `qfrac` has the larger raw
   effect (`z = +4.49` at `n = 7`) and `ρ|e` within `±0.02` — entirely the linear-extension count. `qmass`
   has `ρ|e ≈ −0.27`, stable in `n`, against `|ρ|e| ≤ 0.10` for every invariant in §6's table; and in each of
   the three `e`-groups where an exact tie was capable of failing, `qmass = 1` marks exactly the extremal
   posets (1 of 7, 3 of 13, 6 of 20; group-level `p = 1/38760` at `n = 8`, but the three groups share five
   cores and the honest exact `p` is `1/5` — mg-a893, §4). The nine rows this document
   originally reported as exact ties were all `e = 3` groups, where every member is extremal by construction
   and the tie could not fail (§4, mg-dea5). Not a filter and not explained — see §4's corrected verdict.
4. **Genuine necessary conditions, labelled.** Theorems: every level block is convex, and the level data can
   express only convex-restriction counts (§5.1); `λ₂ = max_{x∥y} s(x,y)` **for every weight, not only the
   uniform-move one** (mg-dea5), a pair statistic of the same
   shape as `δ` but an independent coordinate of the same triple (§5.2); no-free-lunch — `δ` is invariant on
   the uniformising polytope while `λ₂` sweeps `[0,1]`, so spectral detection needs a weight rule external
   to stationarity (§5.5). A genuine constraint: frozen forces `e(P) ≥ 4`, which most extremal posets fail,
   so the proxy is not a near-miss (§5.4). A translation, priced as one: primitive ⟺ positive excess at
   every 2-block level (§5.3).
5. **One signal, and it is a heuristic.** `δ_walk`, the action's own balance constant from face counts
   alone, has `ρ = 0.975` with `δ` and `0.849` after controlling for `e(P)` — the only invariant here that
   survives that control. It is not an inequality in either direction, it already produces a false positive
   at the `1/3` threshold at `n = 6`, and its error grows with `n` while the margin it must resolve is `0`
   (§5.2).
6. **The spectral sweep is null in the coordinate that matters, and what is left open is stated.** Every
   cheap quotient-lattice or spectral summary has partial correlation `|ρ|e| ≤ 0.10` with `δ`; `λ₂` is the
   weakest and fails significance at both `n = 6` and `n = 7`. But **no collision witness was found**: not
   one `I4` fiber at any `n ≤ 7` — including 626 non-singleton fibers at `n = 7` — contains two posets with
   different `δ`. **So it is left open whether `(Q(P), m)` determines `δ`**, and this document does not claim
   it does not. The operative point is narrower: `I4` costs strictly more to compute than `δ` itself, so it
   is not a shortcut either way (§6).
7. **Cost.** All 2447 posets on 3…7 elements; named families to `n = 12`; one `n = 11` witness; nothing
   larger. About 11 minutes for both scripts. `n = 8` exhaustively was not attempted here — the refinement
   precompute for `Π_8` and the per-poset level work put it at roughly two orders of magnitude above the
   `n = 7` pass. **`n = 8` has since been reached for §2 and §4** by mg-dea5, which replaces the
   level-lattice inversion with the factorisation `m_X = Π_{B ∈ X} M(P|_B)` and so never builds the lattice:
   all 16,999 isomorphism classes, about 7 minutes end to end (`code/counterexample_repair_dea5/`). §3 and §6 remain at
   `n ≤ 7`. The forecast that no trend reverses at `n = 8` **held for §3 and §6 and failed for §4**, which is
   where the trend was never measured under the control that matters.

**What would change the picture.** A collision witness — two posets with the same `(Q(P), m)` and different
`δ` — would close §6's open question negatively and is the cheapest next experiment; `n = 8` is where to look
since fiber sizes are growing fast. Nothing else here is waiting on more computation.

**Nothing here proves or disproves the conjecture, no bound on `λ₂(Δ_AT)` is attempted or claimed, and the
local-to-global machinery is not used.** Integration into `STATE.md` is a separate landing.
