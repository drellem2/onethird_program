# The §4 null is false, and the signal under it replicates at `n = 8`

*mg-dea5, landing `docs/OneThird-Counterexample-Under-The-Action-IndependentAudit.md` (mg-a7b4) into
`docs/OneThird-Counterexample-Under-The-Action.md` (mg-24a3, `f5d3485`). Everything numerical here is produced
by `code/counterexample_repair_dea5/`, which **imports nothing** from `code/counterexample_probe_24a3/` (the
target) or `code/counterexample_audit_a7b4/` (the audit) and shares no code with either. Regenerate with
`code/counterexample_repair_dea5/run_all.sh` — pure Python 3, no dependencies, about 7 minutes; the committed
outputs are `out_controls.txt`, `out_theorem4.txt`, `out_section4.txt`, `out_cycles.txt`, `out_check_doc.txt`.
Exact integer and rational arithmetic throughout.*

---

## VERDICT: the claimed null was measured on a vacuous control, and the signal it hid REPLICATES

| | |
|---|---|
| **PRIMARY — the null is false, and the effect is real** | In all three `e`-groups where the comparison was *capable* of failing, `qmass = 1` picks out **exactly** the `δ`-extremal posets: 1 of 7 at `n = 6`, 3 of 13 at `n = 7`, **6 of 20 at `n = 8`**. The `n = 8` group is a pre-specified replication in a population neither the target nor the audit reached, its test family has size **1**, and its exact `p` is **`1/38760 = 2.6 × 10⁻⁵`**. On the powered test — pooled within-`e` association over the whole population, which is the recipe of the target's own §6 — `qmass` sits at **`ρ|e ≈ −0.27`** against `|ρ|e| ≤ 0.10` for **every one** of the nine invariants in that table. |
| **AND A CLEAN SPLIT, which is the part that makes it credible** | `qfrac`, whose *raw* effect is the **larger** of the two (`z = +4.49` at `n = 7`, `+6.91` at `n = 8`), **is** null after the control: `ρ|e` between `−0.01` and `+0.02`. So the target's §4 verdict is correct for one statistic and false for the other, and the instrument that found the effect also finds the null next to it. |
| **DEFLATION, stated because it is true** | Inside those groups the separation does **not** need `L*`: no non-extremal member reaches `qmass = 1` on **any** linear extension, so `max_{L ∈ L(P)} qmass(L) = 1` gives the same split and `L*` merely attains the maximum. And `L*` is **not** the argmax in general (583 of 669 at `n = 7`), so that is not a theorem either. |
| **ALSO — Theorem 4 generalised** | The weight hypothesis is removable: `λ₂ = max_{x∥y} s(x,y)` for **every** weight. 972 (poset, weight) cases, 891 non-uniform, **0 failures**, of which 228 are checked against the actual transition matrix in exact rationals — pinning the whole spectrum, not just `λ₂`. |
| **ALSO — the sampling negative, replaced by an exhaustive one** | The smallest `n` carrying a majority cycle is **exactly 9**: none at `n ≤ 8` over all 19,440 non-chain posets up to isomorphism (ties included), a verified witness at `n = 9`, and `n = 10` from the target's own `n = 11` witness minus its isolated element. The document's "no cycle in 4200 random posets at each of `n = 8, 9, 10`" was **false at 9 and at 10**. |

**Neither headline answer moves.** The bridge object is still a theorem; the concentration quantity is still
not a filter. The target's §3, §5.1, §5.3, §5.5, §6 and §7 are untouched, and the seven proved results are all still
proved — one of them in more generality than it was stated.

---

## 0. Scope: what was asked, and what is here

The brief (mg-dea5) asked for four things, and this document is those four things and nothing else:

1. strike §4's universal and replace it with what the data support;
2. re-run over **non-vacuous** `e`-groups only, with "non-vacuous" defined explicitly, the three-rows-per-`n`
   break and the size-`< 3` skip removed, and effect size + a null-model `p`-value per group, with the
   multiple-comparison position stated honestly;
3. state Theorem 4 in the generality it has;
4. produce the `n = 8, 9, 10` cycle negative **from the committed instrument**, and record `n = 8` as open
   rather than absent.

Item 4 turned out better than "open": `n = 8` is now **settled**, exhaustively, so it is recorded as closed.
Nothing else was added. In particular: `STATE.md` is untouched (integration remains a separate landing), the
minor items 1–8 of the audit are **not** actioned here, and no new question is opened.

---

## 1. Why the control had nothing in it

### 1.1 The reporting loss

`probe.py`'s `e(P)`-controlled loop breaks after three printed rows per `n` and skips any `e`-group of size
`< 3`:

```python
    if len(grp) < 3:
        continue
    ...
    lines += 1
    if lines >= 3:
        break
```

Nine rows were committed, three per `n`, and **every one of them is an `e = 3` group**. Both restrictions are
gone here: every `e`-group containing an extremal poset is reported, at every `n`, with no cap and no floor.

### 1.2 The `e = 3` group cannot fail — Proposition V

> **Proposition V.** Every non-chain poset with `e(P) = 3` has `δ(P) = 1/3` exactly, hence is `δ`-extremal.

*Proof.* For an incomparable pair `{x,y}`, `e(P ∪ {x<y})` and `e(P ∪ {y<x})` are positive integers summing to
`e(P) = 3`, hence `{1,2}`, so `min(p, 1−p) = 1/3` for **every** incomparable pair; the max over pairs is
`1/3`, and `1/3` is the minimum over the population because the conjecture is tight. ∎

So in an `e = 3` group **every member is extremal**, and "the extremal poset is tied with every other member
of its group" is a tautology with no non-extremal poset in it to be distinguished from. Verified over every
non-chain poset at `n = 3 … 8`, ties included:

| `n` | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| non-chains with `e = 3` | 1 | 2 | 3 | 4 | 5 | 6 |
| of those, `δ = 1/3` | 1 | 2 | 3 | 4 | 5 | 6 |
| counterexamples to V | 0 | 0 | 0 | 0 | 0 | 0 |

**The definition used from here on.** An `e`-group is **VACUOUS** if every member is extremal, so that a tie
is incapable of failing; **NON-VACUOUS** if it contains at least one extremal **and** at least one
non-extremal member.

Note that the vacuity is not a coincidence of the reporting loop. The target's §5.4 already records that
most extremal posets have `e(P) = 3` — 1 of 1, 2 of 2, 3 of 3, 4 of 5, 5 of 8 at `n = 3 … 7` (and 6 of 12 at
`n = 8`). The `e = 3` groups are therefore the *first* ones any such loop reaches, and they are exactly the
ones that carry no information.

---

## 2. The population, and what is excluded from it

Both of the target's §4 statistics need `L*` to be a linear order. Tie-freeness alone is not enough — the majority relation
also has to be acyclic — so both are checked rather than assumed, and both exclusions are counted:

| `n` | non-chains | excluded: tied | excluded: cyclic majority | population | `#`extremal |
|---|---|---|---|---|---|
| 5 | 62 | 46 | 0 | 16 | 3 |
| 6 | 317 | 229 | 0 | 88 | 5 |
| 7 | 2044 | 1373 | 0 | 671 | 8 |
| 8 | **16998** | **10578** | **0** | **6420** | **12** |

`min δ = 1/3` at every `n`, so "extremal" means `δ = 1/3` throughout. The `cyclic` column is zero at every
`n`, so the population sizes are unaffected by the check; §7 below is what establishes that it is zero, and
establishes it exhaustively rather than by sampling. The target's instrument also refuses an `L*` on a cyclic
majority relation (`bridge.py`: `self.acyclic = self.Lstar is not None`), so this is a confirmation of its
convention and not a correction to it.

**How `n = 8` became reachable.** Both prior instruments build the level lattice `Q(P)`, sort it by
refinement and invert `Σ_{Y ≤ X} m_Y = Π_B e(P|_B)` downward. That is what put `n = 8` at "two orders of
magnitude above the `n = 7` pass". This instrument never builds the lattice, using instead:

> **Lemma (multiplicativity).** For every level `Y` of `P`,  `m_Y = Π_{B ∈ Y} M(P|_B)`, where
> `M(R) := m_{top(R)}` and `top(R)` is the one-block partition of `R`.

*Proof.* Fix a level `Y` with blocks `B_1 … B_k`. If `Z` refines `Y`, any directed cycle of `P/Z` projects to
a cycle or a loop of `P/Y`, and `P/Y` is acyclic, so every cycle of `P/Z` stays inside one block of `Y`. The
relations of `P` inside `B_i` are exactly those of `P|_{B_i}`, so `Z` is a level of `P` iff each `Z|_{B_i}` is
a level of `P|_{B_i}`: the interval below `Y` is the **product** of the level sets of the `B_i`. Put
`g(Z) = Π_i m^{P|_{B_i}}_{Z|_{B_i}}`. Then `Σ_{Z ≤ Y'} g(Z) = Π_{B ∈ Y'} e(P|_B)` for every `Y'` refining `Y`,
which is the defining system for `m` on that interval; the system is triangular in the refinement order and
so determines its solution, whence `g = m` below `Y`, and at `Z = Y` this is the claim. ∎

Two corollaries are used. `M(R) = 0` for every chain with `≥ 2` elements, so the target's measured supporting
fact ("0 bad of 65,481 all-chain levels other than the finest have `m = 0`") becomes **structural**; and
since every `m_X ≥ 0`,

> `qmass = 1` **iff** every level with positive multiplicity is an interval partition of `L*`.

That is the exact combinatorial content of the statistic. The Lemma is checked against the level-lattice
inversion on every level of every poset at `n ≤ 5` (control C7, 2583 levels, 0 bad), and the mutation that
replaces `M` by `e` makes that control fail on 190 levels (negative control N2).

---

## 3. THE PRIMARY MEASUREMENT

### 3.1 Every group containing an extremal poset, no cap and no floor

| `n` | `e(P)` | `N` | `k` extremal | `qmass = 1` in it | distinct `δ` | status | other `qmass` present |
|---|---|---|---|---|---|---|---|
| 5 | 3 | 3 | 3 | 3 | 1 | *VACUOUS* | — |
| 6 | 3 | 4 | 4 | 4 | 1 | *VACUOUS* | — |
| 7 | 3 | 5 | 5 | 5 | 1 | *VACUOUS* | — |
| 8 | 3 | 6 | 6 | 6 | 1 | *VACUOUS* | — |
| 6 | **9** | 7 | 1 | 1 | 2 | **non-vacuous** | `8/9`, `2/3` |
| 7 | **9** | 13 | 3 | 3 | 2 | **non-vacuous** | `8/9`, `2/3` |
| 8 | **9** | 20 | 6 | 6 | 2 | **non-vacuous** | `8/9`, `2/3` |

The `e`-values carrying extremal posets are `3` and `9` at every `n` reached, and `e = 3` is always vacuous.
So the entire testable evidence is the `e = 9` groups: one at `n = 6`, one at `n = 7`, one at `n = 8`, and
**nothing at all at `n = 5`** — the `n = 5` row of the document's nine is not merely uninformative, it is the
only group that exists there.

### 3.2 The test

**Hypothesis.** Within an `e`-group, `qmass = 1` marks exactly the extremal posets.
**Statistic.** The mid-rank sum of `qmass` over the `k` extremal members (mid-ranks, so ties inside the group
do not favour the marked set).
**Null.** The `k` extremal labels fall on a uniformly random `k`-subset of the `N` members. The group is the
size-matched comparison set and is taken **entire**, not sampled.
**`p` is exact** — every one of the `C(N,k)` labellings is enumerated, not simulated.

| `n` | `e` | `N` | `k` | `#qmass = 1` | separation | AUC | exact `p` | `1/p` |
|---|---|---|---|---|---|---|---|---|
| 6 | 9 | 7 | 1 | 1 | **perfect** | `1` | `1/7` | 7 |
| 7 | 9 | 13 | 3 | 3 | **perfect** | `1` | `1/286` | 286 |
| 8 | 9 | 20 | 6 | 6 | **perfect** | `1` | **`1/38760`** | 38760 |

*Perfect* is both inclusions: the `qmass = 1` members are exactly the extremal ones, so **no** non-extremal
member of the group reaches `1`. The non-extremal values are `8/9` and `2/3` in all three groups. AUC — the
probability that a random extremal member exceeds a random non-extremal one, ties counted `1/2` — is `1`
exactly in all three, which is what perfect separation means as an effect size.

### 3.3 What is a hypothesis and what is a test of it

This is stated first because it is the part most easily overclaimed.

**The `n = 7` group is where mg-a7b4 found this, and the `n = 6` group was in the same table. Those two are
the generating observations, and their `p`-values are not evidence** — they are the reason the hypothesis
exists. `1/286` found after the fact among the groups that happened to be non-vacuous is a hypothesis.

**The `n = 8` group is a pre-specified test in a new population.** The target document stops at `n = 7`; so
does the audit; the hypothesis was written down (in the mg-dea5 brief, and in the 15:15 roadmap) before
`n = 8` was computed. And at `n = 8` there is exactly **one** non-vacuous group containing an extremal poset,
so the family of tests has **size 1** and there is no multiplicity to correct for.

> **PRE-SPECIFIED REPLICATION, `n = 8`, `e = 9`: 6 of 20, perfect, exact `p = 1/38760 = 2.58 × 10⁻⁵`,
> AUC `= 1`.**

Stated three further ways, all of which survive:

* Bonferroni over all **3** non-vacuous groups ever run: `p ≤ 7.7 × 10⁻⁵`.
* Bonferroni over all **7** groups containing an extremal poset — counting the four vacuous ones as if they
  had been testable, which is the most conservative reading of "how many tests could I have run": `p ≤ 1.8 ×
  10⁻⁴`.
* Joint probability of all three groups separating perfectly under the independent random-label null:
  `1.29 × 10⁻⁸`. **This one contains the generating observations** and is reported for completeness, not as
  the test.

---

## 4. THE POWERED TEST, and the split that makes it credible

The dichotomy above uses only the extremal/non-extremal split, which at `n = 8` is 6 posets against 6414. But
§4's actual claim is wider — that the effect is *"entirely accounted for by the linear-extension count"* — and
that is testable on the **whole** population, in every `e`-group, extremal or not. §6 of the target measures
exactly this quantity (`ρ|e`) for nine invariants and reports `|ρ|e| ≤ 0.10` for all nine. **`qmass` and
`qfrac` are not among the nine.**

Pooled within-group association: pairs are compared only inside a fixed `e(P)`, so everything the
linear-extension count explains is removed by construction. `ρ|e` is computed by the target's own recipe
(mean-centre inside each `e`-group of size `≥ 3`, pool, Spearman) so the numbers are directly comparable with
its table. `τ_b` is Kendall's tie-corrected coefficient, `z` uses Kendall's exact null variance summed over
the independent groups, and `perm p` shuffles `δ` inside each group (199 reps, seed 20260730, so its floor is `1/200 = 0.005`).

| `n` | population | `e`-groups | `qmass` `ρ|e` | `qmass` `τ_b` | `z` | perm `p` | `qfrac` `ρ|e` | `qfrac` `τ_b` |
|---|---|---|---|---|---|---|---|---|
| 6 | 88 | 27 | **−0.287** | −0.2978 | −1.76 | 0.0800 | −0.009 | −0.2259 |
| 7 | 671 | 127 | **−0.261** | −0.2626 | −5.65 | 0.0050 | +0.011 | −0.0569 |
| 8 | 6420 | 670 | **−0.273** | −0.2052 | **−16.60** | 0.0050 | +0.018 | +0.0064 |

Three things to read off, and the third is the important one.

1. **The sign is the predicted one.** Negative means higher `qmass` goes with **lower** `δ`: more of the
   spectrum sitting on `L*`'s chain goes with a worse-balanced poset, which is the direction the raw effect
   had.
2. **It does not wash out.** `ρ|e ≈ −0.27` and stable in `n`, on 6420 posets and 670 groups at `n = 8`, with
   `z = −16.6`. At `n = 6` the permutation `p` is `0.0800` — not significant, and said so; the population is
   88 posets. By `n = 7` it is at the 199-rep floor of `0.005`, and the exact `z` is what carries the
   magnitude beyond that.
3. **`qfrac` IS null after the control, and its raw effect is the BIGGER of the two.** `z = +2.90 / +3.40 /
   +4.49 / +6.91` raw at `n = 5 … 8` for `qfrac` against `+1.16 / +1.95 / +2.64 / +3.72` for `qmass` — and
   after the control `qfrac` collapses to `±0.02` while `qmass` does not. So the target's §4 verdict is **right about
   one statistic and wrong about the other**, and the same instrument that reports the effect reports the
   null beside it. That is the strongest available argument that the effect is not an artefact of the method:
   the method finds the null when the null is there.

---

## 5. THE DEFLATION: `L*` is not what separates

`qmass` is defined against `L*`, but the interval partitions of **any** linear extension are levels, so the
statistic can be computed against every `L ∈ L(P)`. Doing that inside the three non-vacuous groups:

* **Every member's `qmass(L*)` is its maximum over all 9 linear extensions.**
* **The members whose best linear extension reaches `qmass = 1` are exactly the extremal ones** — 1 of 7,
  3 of 13, 6 of 20. No non-extremal member reaches `1` on **any** linear extension; the best a `8/9` member
  can do is `8/9`, and a `2/3` member `2/3`.

So inside these groups the separation **does not need `L*`**: the predicate `max_{L ∈ L(P)} qmass(L) = 1`
gives the same split, and `L*` merely attains that maximum. The separating content is that the whole spectrum
fits on **some** interval chain, not that it fits on the **majority** one.

And "`L*` maximises `qmass`" is **false** as a general statement, so it is not offered as one:

| `n` | posets tested | `L*` attains the max | the max is unique |
|---|---|---|---|
| 5 | 16 | 14 | 13 |
| 6 | 88 | 83 | 59 |
| 7 | 669 | 583 | 309 |

(Two of 671 posets at `n = 7` are skipped for cost, `e(P) > 400`.) The powered test of §4 of THIS document
**is** about `L*`, since `qmass(L*)` is its variable; §3's dichotomy is not.

---

## 6. Theorem 4 holds for every weight

> **Theorem 4 (general form).** For **any** probability weight `w` on the `P`-compatible moves and any
> non-chain `P`,  `λ₂ = max over incomparable pairs {x,y} of s_w(x,y)`, where `s_w(x,y)` is the `w`-mass of
> the moves leaving `x` and `y` in the same block and `λ₂ = max{ λ_X : m_X > 0, X ≠ the finest partition }`.

The committed proof (target §5.2) uses exactly two inputs: that `λ_X` is non-increasing as `X` coarsens —
true for any distribution on moves, since coarsening `X` can only shrink the set of moves whose level is
coarser than or equal to `X` — and that `m_X` is a combinatorial invariant of `P`. Neither mentions the
weight. **The general form is what §5.5 needs**, because §5.5's whole argument is about weights other than the
uniform-move one, and under `w_t` the theorem reads `λ₂ = t = max_{x∥y} s_{w_t}(x,y)`, which is exactly the
computation Theorem 7's proof performs by hand.

Two things were tested, both against the actual matrix where the matrix is affordable.

* **The spectrum claim itself** — that the eigenvalues of the transition matrix are exactly the `λ_X` with
  multiplicities `m_X` — via `trace(Mᵏ) = Σ_X m_X λ_Xᵏ` for `k = 1 … |L(P)|` in exact rationals. Equality for
  all `k` forces the eigenvalue multiset by Newton's identities, so this pins the **whole** spectrum with no
  eigensolver and no floats. **228 (poset, weight) cases at `n ≤ 4`, 0 failures.**
* **The identity `λ₂ = max_{x∥y} s(x,y)`** on a wider population. **972 (poset, weight) cases at `n ≤ 5`, of
  which 891 use a weight that is not the uniform-move one, 0 failures.**

Weight families: the uniform-move weight; three random rational weights per poset (seeded); `w_t` at
`t = 0, 1/4, 1/3, 1/2, 3/4, 1`; and two degenerate corners (all mass on a single move), because a universal
claim has to survive the corners.

---

## 7. The cycle negative, replaced

The document's §2 asserted *"no cycle in 4200 random posets at each of `n = 8, 9, 10`"*. Three problems, and
the third is fatal: the search is **not in the committed instrument**, so `run_all.sh` reproduces the printing
of the sentence and `check_doc.py` compares a string against a `print` statement; there **is** a cycle at
`n = 9`; and there **is** one at `n = 10`.

What this instrument establishes instead:

| `n` | statement | how |
|---|---|---|
| `≤ 8` | **no majority cycle** | exhaustive over every isomorphism class, ties included: 19,440 non-chains, **16,998 at `n = 8` alone** |
| 9 | a cycle **exists** | witness `0<5 0<8 1<4 1<6 2<3 2<7 3<6 4<8 5<7`, `e(P) = 1431`, tie-free, no isolated element, 3-cycle `0 → 2 → 1 → 0`, all three margins exactly `80/159`, and **no single-element deletion preserves it** — consistent with the exhaustive `n = 8` sweep |
| 10 | a cycle **exists** | the document's own `n = 11` witness with its isolated element `8` deleted: `e(P) = 7134`, `78474 = 11 × 7134`, identical pair probabilities, same 3-cycle |
| 11 | the document's witness | reproduced exactly: `e(P) = 78474`, `p(5,9) = 597/1189`, `p(9,6) = 599/1189`, `p(6,5) = 1784/3567` |

> **So the smallest `n` carrying a majority cycle is exactly 9.** mg-a7b4 left `n = 8` open, correctly, as a
> limit of its own search (0 in 30,000 across six densities, not enumerated). It is now closed, and closed by
> enumeration rather than sampling.

**And the same instrument re-runs the sampling negative, deliberately.** 4200 random posets — the document's
own sample size — at each of three densities at `n = 9`, seed 4242: **0 cycles**, printed directly beneath the
witness that proves the region is non-empty. That is the shape of the defect and the reason the exhaustive
sweep was worth the cost: a negative with a sample size attached reads as evidence, and here the phenomenon is
rarer than a sampler of that size reaches while being present. Every negative in this repair is either
exhaustive over a stated population or is printed next to the witness that refutes it.

---

## 8. Controls, including four that fire

`out_controls.txt`. Twelve positive controls; where a route exists outside the repository the external
sequence is used, and where the alternative is a slower route the slow route is run and compared.

| | |
|---|---|
| **C1** | enumeration up to isomorphism against **A000112**: `1, 1, 2, 5, 16, 63, 318, 2045, 16999` |
| **C2** | the labelled count as an orbit sum `Σ n!/\|Aut(P)\|` against **A001035**: `1, 1, 3, 19, 219, 4231, 130023, 6129859` — detects over- **and** under-merging of isomorphism classes, which a class count cannot |
| **C3** | the canonical form against brute force over all `n!` relabellings, `n ≤ 5`, plus 24 relabellings of every class at `n = 4, 5` |
| **C4** | `e(P\|_S)` for **every** subset against direct enumeration of `L(P\|_S)`: 2312 pairs, 0 bad |
| **C5** | `p(x,y)` against direct counting over the enumerated `L(P)`: 337 pairs, 0 bad |
| **C6** | "level = acyclic quotient" against brute force over all block **orders**: 3541 (poset, partition) pairs, 0 bad |
| **C7** | the multiplicativity Lemma against the level-lattice inversion, on every level: 2583 levels, 0 bad |
| **C8** | `Σ_X m_X = e(P)` and `m_X ≥ 0`: 2447 posets, 0 bad, 0 negative multiplicities |
| **C9 / C9b** | the `M ≠ 0` prune and the convexity prune each drop no level: 402 posets apiece, 0 disagreements |
| **C10** | the spectrum against the actual transition matrix, exactly, at `n ≤ 4` |
| **C11** | move counts: the antichain against **A000670** (Fubini `1, 3, 13, 75, 541`), the chain against `2ⁿ⁻¹` |
| **C12** | `qmass` and `qfrac` against a slow independent route — `m` from the lattice inversion, summed over interval partitions found by filtering all levels rather than by the composition DP: 107 posets, 0 disagreements |

**And four negative controls, each of which fires.** A control that has never failed is not known to be a
control (mg-2da3's lesson, applied here to a deliverable whose whole content is a measurement):

| | mutation | must fail | did |
|---|---|---|---|
| **N1** | drop acyclicity from the definition of "level" | C6 | 34 disagreements |
| **N2** | replace `M(R)` by `e(R)` in the Lemma | C7 | 190 mismatches |
| **N3** | compute `qmass` on the intervals of a fixed labelling instead of `L*` | the two must differ | 25 posets differ, 79 agree |
| **N4** | a poset with a majority tie must be refused a unique `L*` | 46 of 46 refused | fires |

**Reproducibility, checked rather than asserted.** `run_all.sh` was run twice from the same tree and all four
measurement outputs are **byte-identical**. The only randomness is seeded (`20260730` for the permutation
tests, `4242` — the target's own seed — for the cycle search), and unlike the negative this repair replaces,
the searches themselves are in the committed instrument, so re-running reproduces the *search* and not merely
the printing of its result.

### 8.1 And the hole in the target's own checker is closed

mg-a7b4's finding 1 ended: *"The document's `check_doc.py` cannot catch this: its entry for these rows checks
that the string `rank 1 of 5 tied with 4` appears in both the prose and the output. It does, and the
arithmetic behind it is right. The defect is entirely in the quantifier."*

That is still true after this repair, and **worse**: the struck sentences are quoted verbatim inside their
epitaphs, so a checker that only looks for the string finds it and passes — now certifying a **retracted**
claim. Two changes close it.

* `code/counterexample_probe_24a3/check_doc.py` gains a `STRUCK` set and an inverted assertion for its four
  affected entries: the string must be present **and every occurrence must lie inside a `> **STRUCK`
  blockquote**. If a later edit puts one back into live prose, that file fails. All 53 figures still verify.
* `code/counterexample_repair_dea5/check_doc_repair.py` does the same job for this repair — 42 figures across
  both documents against the four committed outputs, the four struck sentences confined to their epitaphs,
  the three replacement sentences confirmed live, and guards against unconditional or overclaiming language.

The guard earned its keep on the first run: it **failed**, because the replacement text in §2 of the target
used the phrase "4200 random posets" in live prose while re-running the search. The live sentence was
reworded. That is the whole value of a checker that can tell prose from an epitaph.

---

## 9. What this does NOT show

* **Not a counterexample statement.** The extremal posets satisfy `δ = 1/3`, which is the conjecture holding
  with **equality**. Nothing here is evidence about any poset with `δ < 1/3`. The target's §5.4 already prices the proxy:
  frozen forces `e(P) ≥ 4`, and 6 of the 12 extremal posets at `n = 8` have `e(P) = 3`. The separation lives
  at `e = 9`, so it is at least in the part of the proxy Proposition 6 does not exclude — and that is all
  that can be said.
* **Not a filter.** `qmass = 1` still retains 36 of 6420 posets at `n = 8` (`0.6%`, a third of them
  extremal), and computing `qmass` costs strictly more than computing `δ`. It excludes nothing a cheaper
  quantity does not.
* **Not explained.** `qmass = 1` iff every positive-multiplicity level is an `L*`-interval partition (§2 of this document). Why
  that should coincide with `δ = 1/3` inside an `e`-group is **open**, and the coincidence of `e = 9` across
  three sizes is unexplained. A mechanism would be worth more than another `n`.
* **Not about `L*`, inside those groups** — §5 of this document.
* **Three groups is three groups.** All three non-vacuous groups that exist at `n ≤ 8` have `e(P) = 9`, and
  the `τ_b` magnitude of the powered test **decays** with `n` (`−0.2978`, `−0.2626`, `−0.2052`), which is the
  direction every other trend in the target document also points. What does not decay is the target's own
  `ρ|e` statistic (`−0.287`, `−0.261`, `−0.273`).
* **`n = 9` is not reached** for the `e`-group measurement. Its structure at `n = 9` is the next experiment, and the
  factorisation Lemma is what would make it affordable.

---

## 10. Files

```
code/counterexample_repair_dea5/poset.py       posets, enumeration up to isomorphism, e/p/delta/L*
code/counterexample_repair_dea5/levels.py      levels, the multiplicativity Lemma, qmass and qfrac
code/counterexample_repair_dea5/walk.py        moves, the actual transition matrix, the spectrum
code/counterexample_repair_dea5/records.py     per-poset records and the section 4 population
code/counterexample_repair_dea5/section4.py    THE RE-MEASUREMENT             -> out_section4.txt
code/counterexample_repair_dea5/theorem4.py    Theorem 4 for every weight     -> out_theorem4.txt
code/counterexample_repair_dea5/cycles.py      majority cycles, exhaustive    -> out_cycles.txt
code/counterexample_repair_dea5/controls.py    12 controls + 4 that fire      -> out_controls.txt
code/counterexample_repair_dea5/check_doc_repair.py  the prose, and the STRUCK guard -> out_check_doc.txt
code/counterexample_repair_dea5/run_all.sh     regenerates all five, ~7 min
```

*Repair by mg-dea5. `STATE.md` is untouched; integration remains a separate landing. The audit of this repair
is pre-filed as mg-0a11.*
