# The §4 null is false, and the signal under it replicates at `n = 8`

*mg-dea5, landing `docs/OneThird-Counterexample-Under-The-Action-IndependentAudit.md` (mg-a7b4) into
`docs/OneThird-Counterexample-Under-The-Action.md` (mg-24a3, `f5d3485`). Everything numerical here is produced
by `code/counterexample_repair_dea5/`, which **imports nothing** from `code/counterexample_probe_24a3/` (the
target) or `code/counterexample_audit_a7b4/` (the audit) and shares no code with either. Regenerate with
`code/counterexample_repair_dea5/run_all.sh` — pure Python 3, no dependencies, about 9 minutes; the committed
outputs are `out_controls.txt`, `out_theorem4.txt`, `out_section4.txt`, `out_cycles.txt`, `out_cores.txt`,
`out_check_doc.txt`. Exact integer and rational arithmetic throughout.*

> **AMENDED by mg-a893, landing mg-0a11's audit of this document.** Two of mg-0a11's findings are actioned
> here and neither of them touches a measurement. **§3.4 is new**: the three `e = 9` groups are not three
> independent samples, the exact `p` over what is actually independent is **`1/5`**, and the phrase *"new
> population"* is withdrawn — see the epitaph in §3.3. **§8.2 is new**: `check_doc_repair.py` compared the
> two documents *concatenated*, so a figure could be wrong throughout one of them and still be found in the
> other; it now checks per document, per output file and per section, and mg-0a11's own 14-mutation battery
> is re-run **unmodified** as the acceptance gate. Everything measured in this document reproduced from
> mg-0a11's disjoint instrument and nothing measured is changed.

---

## VERDICT: the claimed null was measured on a vacuous control, and the signal it hid REPLICATES

| | |
|---|---|
| **PRIMARY — the null is false, and the effect is real** | In all three `e`-groups where the comparison was *capable* of failing, `qmass = 1` picks out **exactly** the `δ`-extremal posets: 1 of 7 at `n = 6`, 3 of 13 at `n = 7`, **6 of 20 at `n = 8`**. On the powered test — pooled within-`e` association over the whole population, which is the recipe of the target's own §6 — `qmass` sits at **`ρ|e ≈ −0.27`** against `|ρ|e| ≤ 0.10` for **every one** of the nine invariants in that table. |
| **AND THE STRENGTH OF IT, corrected — `1/5`, not `1/38760`** | The group-level exact `p` at `n = 8` is `1/38760 = 2.6 × 10⁻⁵`, **and that is not the strength of the evidence.** Every one of the 20 members of the `n = 8` group is a member of the `n = 7` group with one **cut element** — an element comparable to everything — adjoined, and `δ` and `qmass` are *inherited* along that operation, by a one-line theorem and by measurement respectively. So the three groups carry **five distinct cores between them, of which exactly one is extremal, at `n = 6`, `7` and `8` alike**. The honest exact `p` over the cores is **`1/5`**, it is the same `1/5` three times, and the joint `1.29 × 10⁻⁸` is a product of **deterministically nested** events rather than of independent ones. **§3.4, `out_cores.txt`.** |
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

| `n` | `e` | `N` | `k` | `#qmass = 1` | separation | AUC | group-level `p` | `1/p` | distinct cores `C` | core-level `p` |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 9 | 7 | 1 | 1 | **perfect** | `1` | `1/7` | 7 | 5 | **`1/5`** |
| 7 | 9 | 13 | 3 | 3 | **perfect** | `1` | `1/286` | 286 | 5 | **`1/5`** |
| 8 | 9 | 20 | 6 | 6 | **perfect** | `1` | **`1/38760`** | 38760 | 5 | **`1/5`** |

**The last two columns are the ones to read, and §3.4 is why.** The group-level `p` counts each member of a
group as an independent chance for the hypothesis to fail. Most of them are not: `δ` and `qmass` are
inherited when an element comparable to everything is adjoined, so members sharing a core share their verdict.
Five cores, one of them extremal, at every one of the three sizes — **the same five**.

*Perfect* is both inclusions: the `qmass = 1` members are exactly the extremal ones, so **no** non-extremal
member of the group reaches `1`. The non-extremal values are `8/9` and `2/3` in all three groups. AUC — the
probability that a random extremal member exceeds a random non-extremal one, ties counted `1/2` — is `1`
exactly in all three, which is what perfect separation means as an effect size.

### 3.3 What is a hypothesis and what is a test of it

This is stated first because it is the part most easily overclaimed.

**The `n = 7` group is where mg-a7b4 found this, and the `n = 6` group was in the same table. Those two are
the generating observations, and their `p`-values are not evidence** — they are the reason the hypothesis
exists. `1/286` found after the fact among the groups that happened to be non-vacuous is a hypothesis.

**What is true about `n = 8` is the PRE-SPECIFICATION, and only that.** The target document stops at
`n = 7`; so does the audit; the hypothesis was written down (in the mg-dea5 brief, and in the roadmap
`b196b2c`) before `n = 8` was computed. At `n = 8` there is exactly **one** non-vacuous group containing an
extremal poset, so the family of tests has **size 1** and there is no multiplicity to correct for.
Multiplicity, however, was never the problem. **Dependence is**, and §3.4 is that.

> **STRUCK (mg-a893, landing mg-0a11 BROKEN 1).** This subsection previously continued:
>
> **The `n = 8` group is a pre-specified test in a new population.**
>
> — and drew from it a headline **PRE-SPECIFIED REPLICATION, `n = 8`, `e = 9`: 6 of 20, perfect, exact
> `p = 1/38760 = 2.58 × 10⁻⁵`, AUC `= 1`**, together with a joint figure of `1.29 × 10⁻⁸` across the three
> groups. The pre-specification is genuine and is *not* withdrawn. **The phrase that fails is "new
> population."** The `n = 8` group is exactly the cut extensions of the `n = 7` group, `δ` and `qmass` are
> inherited along that operation, and so *conditional on `n = 7`, which this document itself names a
> generating observation, the `n = 8` outcome had probability `1`, not `1/38760`.* A pre-specified test of a
> deterministic consequence of the data that generated the hypothesis is still not evidence. The three
> `p`-values were never three measurements, so their product is not a joint probability of anything.

The three multiple-comparison statements below are arithmetically correct and are kept, **struck through in
their interpretation rather than in their arithmetic**: each is a correction for *multiplicity*, and
multiplicity is not what is wrong here.

* Bonferroni over all **3** non-vacuous groups ever run: `p ≤ 7.7 × 10⁻⁵`.
* Bonferroni over all **7** groups containing an extremal poset — counting the four vacuous ones as if they
  had been testable, which is the most conservative reading of "how many tests could I have run": `p ≤ 1.8 ×
  10⁻⁴`.
* Joint probability of all three groups separating perfectly under the independent random-label null:
  `1.29 × 10⁻⁸`. **This one contains the generating observations** and is reported for completeness, not as
  the test. **It also assumes independence that does not hold** — see §3.4 — so it is not a probability of
  anything and is retained only because it was published.

---

### 3.4 THE DEPENDENCE: five cores, not forty, and the honest `p` is `1/5`

*`code/counterexample_repair_dea5/cores.py` → `out_cores.txt`. Every figure in this subsection is produced by
that file, which shares `poset.py` and `levels.py` with the rest of this instrument and nothing else. It was
written to check mg-0a11's finding rather than to accept it, and it reproduces every number of it that lies
within this instrument's reach.*

> **Definition.** `x` is a **cut element** of `P` if it is comparable to **every** other element. `Q` is a
> **cut extension** of `P` if `Q` is `P` with one cut element adjoined. The **core** of `P` is what remains
> when cut elements are deleted repeatedly; it is well defined (the deletion terminates, and it is locally
> confluent because a cut element of `Q` is still one of `Q − x`, so Newman's lemma applies).

> **Theorem (inheritance).** Let `x` be a cut element of `Q` and `P = Q − x`, with `D` the elements below `x`
> and `U` those above. Transitivity puts every element of `D` below every element of `U` in `P` too, so every
> linear extension of `P` already lists `D` before `U` and inserting `x` at that boundary is a **bijection**
> `L(P) → L(Q)`. Hence `e(Q) = e(P)`; `Inc(Q) = Inc(P)`, `x` being comparable to everything; every `p(x,y)`
> is unchanged; and therefore `δ(Q) = δ(P)`, tie-freeness and acyclicity are inherited, and `L*(Q)` is `L*(P)`
> with `x` inserted at the same boundary. ∎

`qmass` is **not** covered by that argument and is not proved here. It is **measured**, on every cut extension
of every poset in the §2 population at `n = 5` and `n = 6`:

| | |
|---|---|
| cut extensions inside the population | **257** |
| `(e, δ, qmass)` all inherited | **257** |
| inheritance failures | **0** |

**And the control fires.** Run the same measurement over the *generic* one-element extension — a new maximal
element above an arbitrary order ideal, where the new element is **not** a cut element — and the inheritance
breaks on **1378 of 1378**. So "inherited" is a property of cut extension and not of adjoining an element.

**The `n = 8` group is exactly the cut extensions of the `n = 7` group.** Up to isomorphism, and both
directions:

| `n → n+1` | cut extensions of group(`n`) | `=` group(`n+1`)? | members of group(`n+1`) that are new | reduction onto group(`n`) |
|---|---|---|---|---|
| 5 → 6 | 4 | no | **3** | 2 of 2 |
| 6 → 7 | 13 | **YES** | 0 | 7 of 7 |
| 7 → 8 | 20 | **YES** | 0 | 13 of 13 |

| `n` | `N` | members with a cut element | **cut-free** |
|---|---|---|---|
| 5 | 2 | 0 | 2 |
| 6 | 7 | 4 | **3** |
| 7 | 13 | **13** | **0** |
| 8 | 20 | **20** | **0** |

The two tables say the same thing twice: `group(n+1)` sits inside the cut extensions of `group(n)` exactly
when `group(n+1)` has no cut-free member, and after `n = 6` it has none. **Nothing enters the family after
`n = 6`.**

So the count that matters is the number of **distinct cores**, because two members with the same core have
the same `(δ, qmass)`:

| `n` | `N` | `k` extremal | distinct cores `C` | extremal cores | group-level `p` | **core-level `p`** |
|---|---|---|---|---|---|---|
| 6 | 7 | 1 | 5 | 1 | `1/7` | **`1/5`** |
| 7 | 13 | 3 | 5 | 1 | `1/286` | **`1/5`** |
| 8 | 20 | 6 | 5 | 1 | `1/38760` | **`1/5`** |

**And the reduction is capable of saying nothing, which is why it says something here.** Over *every*
`e`-group in the population — 691 of them at `n = 8`, not just the three under test — `C = N` in **553** and
`C < N` in **138**. The reduction is inert on four groups in five. It is not inert on these.

The five cores, pooled over `n = 5 … 8`, are the whole of the family:

| size | `δ` | `qmass` | in groups | covers |
|---|---|---|---|---|
| 5 | `4/9` | `8/9` | 5,6,7,8 | `0<2 1<3 1<4 2<4` |
| 5 | `4/9` | `8/9` | 5,6,7,8 | `0<2 0<3 1<3 2<4` |
| **6** | **`1/3`** | **`1`** | 6,7,8 | `0<2 1<3 1<4 2<3 2<4 3<5` |
| 6 | `4/9` | `2/3` | 6,7,8 | `0<2 0<3 1<3 3<4 4<5` |
| 6 | `4/9` | `2/3` | 6,7,8 | `0<2 1<5 2<3 3<4 3<5` |

> **THE HONEST EXACT `p` OVER THE DISTINCT CORES IS `1/5`**, and it is `1/5` at `n = 6`, at `n = 7` and at
> `n = 8` alike — the same number three times because it is the same five cores three times.

**Read this as a correction to the strength claimed, not as a retraction of the finding.** Everything §3.1
and §3.2 measure is unchanged and reproduced: the separation is perfect in both inclusions in every group
where it was capable of failing, `qmass = 1` marks the one extremal core and no other, and mg-0a11 carried
the same measurement to `n = 11` — three sizes beyond this instrument's reach — and found the separation
still perfect, over **six** distinct cores with still exactly one extremal. `1/7 → 1/286 → 1/38760` is not
evidence accumulating with `n`. It is one observation re-counted with more chain elements glued on.

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

**Reproducibility, checked rather than asserted.** `run_all.sh` was run twice from the same tree and all five
measurement outputs are **byte-identical** — and mg-0a11 re-ran it a third time from a clean tree, from
outside this instrument, with the same result. `out_cores.txt` (mg-a893) is byte-identical across independent
runs too, and `out_controls.txt`, `out_cycles.txt` and `out_theorem4.txt` did not move a byte when §3.4 and
the `n = 8` prose were added. The only randomness is seeded (`20260730` for the permutation
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

### 8.2 And the hole in THIS repair's checker is closed (mg-a893)

mg-0a11 put 14 meaning-changing mutations against `check_doc_repair.py` as it stood after §8.1 and **10 of
them exited 0**. The four that were caught were the four the file was built for. The mechanism was a list of
`(string in the prose, string in the output)` pairs matched against **`target + repair` concatenated** and
against **all four outputs concatenated**, so a figure was certified if it appeared *anywhere in either
document* and its value appeared *anywhere in any output*. The sharpest consequence, mg-0a11's M1a: the
headline `1/38760` could be made **wrong in every occurrence throughout this document** and the file still
passed, because the target document carries its own copy of the string.

**Six properties replace the concatenation, and none of them is a longer list.**

| | property | mutations it closes |
|---|---|---|
| **P1** | **Per document.** Every figure names the document it must appear in, and **how many times**. | M1a, M11 |
| **P2** | **Per output.** Every figure names the **one** output file that must have printed it. | — |
| **P3** | **Per section.** Every figure names the ATX heading path its occurrences must sit under. | M7a |
| **P4** | **Per table row.** A table cell is located by its **row key** and checked against the row the instrument printed, so two cells cannot be swapped between rows and both still be "present". | M5, M6 |
| **P5** | **Live prose.** Framing, caveats and status language are named and required, in a named section, outside every epitaph. | M7b, M8, M9, M10 |
| **P6** | **Quoted, not asserted.** A struck sentence may appear in **either** document only inside an epitaph or inside double quotation marks. Epitaphs are now located in the repair document too, not only in the target. | M12 |

`code/counterexample_probe_24a3/check_doc.py` gains the repaired §0 headline as a **LIVE** entry, which is
mg-0a11's M13: the sentence the whole repair exists to install could be quietly reverted from *"picks out
**exactly** the `δ`-extremal posets"* to *"**some of**"* and that file, whose subject is precisely that
document, exited 0.

> **THE ACCEPTANCE GATE IS mg-0a11'S OWN BATTERY, RE-RUN UNMODIFIED.**
> `code/counterexample_audit_0a11/check_locator.py` is not edited, not re-parameterised and not re-ordered;
> its output against this repair is committed as `out_battery_0a11_rerun.txt`. **SILENT MISSES: 10 → 0.**
> The four self-mutations at the bottom of that battery, which test the audit's *own* checker, still fire.

**The cross-check against mg-4acd's presentation-record digest (`e4426c9`), which the brief asked to answer
rather than assume.** That mechanism certifies chosen *regions* of `STATE.md` and `docs/state-history/README.md`
with two SHA-256 digests — one of the region's bytes, one of a four-field **presentation record** (`state`,
`heading`, `position`, `presented`) that answers *"is a reader shown these bytes, in the same place?"*. Three
findings, and the third is the one that matters:

* **It would cover most of this, and by brute force.** Nine of mg-0a11's ten silent misses are edits *inside*
  document text. If both documents were certified regions, a content digest would fire on all nine — and on
  every legitimate edit as well, including the ones this ticket is making. A digest cannot tell a repair from
  a defacement; it can only tell you that somebody moved. That is the right trade for a **frozen ledger cell**
  and the wrong one for a document still under repair.
* **One of the ten is outside its reach in either configuration.** mg-0a11's M3 alters `out_section4.txt` —
  an *instrument output*, not a document. No digest over the documents sees it. This file catches it, because
  its subject is the correspondence between the two.
* **The idea that transfers is the LOCATOR, and it is the one taken.** mg-4acd's insight was that the blind
  spot had moved from "are these the certified bytes?" up into "**which** bytes are the certified ones?".
  That is exactly this file's defect, one layer over: it certified a string with **no location at all**. P1,
  P3 and P4 above are `heading` and `position` in the vocabulary of a quote-checker rather than of a digest.
  `presented` has no analogue here and is not claimed: **a figure of this document wrapped in an HTML comment
  would still pass this file**, and that is stated as the coverage boundary rather than left to be found.

So the two mechanisms are **complementary, not redundant**: a digest answers *"did anything change?"* and
cannot answer *"does the prose agree with the instrument?"*; this file answers the second and not the first.
The honest summary is that mg-4acd's approach covers 9 of the 10 misses, at a cost this document should not
pay yet, and misses the tenth; and that its *locating* idea is what actually fixes this file.

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
* **Not three independent sizes.** The three groups share five cores; `n = 7` and `n = 8` add no core that
  `n = 6` did not already have, and every member of both is a cut extension of a smaller member. The exact
  `p` is `1/5`, not `1/38760`, and the three sizes are one observation seen three times (§3.4). What the
  extra sizes *do* establish is that the separation does not break as `n` grows — mg-0a11 carried it to
  `n = 11` and it does not break there either — and that is worth having, but it is not `1.29 × 10⁻⁸`.
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
code/counterexample_repair_dea5/run_all.sh     regenerates all six, ~9 min
```

*Repair by mg-dea5. `STATE.md` is untouched; integration remains a separate landing. The audit of this repair
was pre-filed as mg-0a11 and is at `docs/OneThird-Counterexample-Under-The-Action-IndependentAudit-mg0a11.md`;
its two BROKEN items are actioned by mg-a893 in §3.4 and §8.2 above.*
