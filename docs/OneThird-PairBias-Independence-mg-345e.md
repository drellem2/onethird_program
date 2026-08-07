# Is the pair-bias derivation of `ε_spec` INDEPENDENT of L4's modulus question?

**Work item.** `mg-345e` (repo `onethird_program`). Filed by `pm-onethird` as the second
disjunct of `mg-6bc2`'s own gate, which nobody had filed.
**Instrument.** `code/pairbias_independence_345e/` · **Predictions** committed at `eb1f4b9`,
before any script of this instrument existed.
**Method.** Reading plus a small dependency/reachability instrument and an exact-rational
check of this document's own algebra. **No poset enumeration** — see §9 for why that is a
deliberate refusal and not an omission.

---

## 0. Verdict

> ## **(A) INDEPENDENT — and the independence is structurally forced, not incidental.**
>
> The pair-bias derivation of an explicit absolute `ε_spec` — equivalently **(LIB-const)**
> `E[inv_e] ≤ (ε_spec/6)(n²−1)`, uniform in `n` — **does not invoke L4 at any step, and does
> not care whether L4 admits an `n`-free modulus.** Its dependency list is exhibited in §2 and
> L4 is not on it. **`mg-6bc2` unblocks on its own second disjunct.**
>
> It unblocks *for the half of `mg-6bc2` that its conjecture is about.* The other half — the
> half its **title** is about — stays gated, and **the gate is not the one `mg-6bc2` names**:
>
> | | what it asks | gated on L4? |
> |---|---|---|
> | **SUPPLY** — `mg-6bc2`'s *conjecture*: "pair bias ALONE should give 1/6" | what constant can we **prove**? | **NO.** §2–§3 |
> | **DEMAND** — `mg-6bc2`'s *title*: "EXACTLY what constant the architecture consumes" | what constant **suffices**? | **YES, but narrower than named, and not only on L4.** §4–§5 |
>
> **Two corrections to the gate as written**, both in §5:
>
> 1. **NARROWER.** The demand side does not need L4's **modulus** `F`. On every branch Step 6
>    can consume, `F` does not appear: (i) is trivial and `F`-free; (ii) is unconsumable for
>    **every strictly positive** `F` (`mg-3af9`, UNCONDITIONAL, audited `mg-c8c6`); (iii) under
>    the repair `mg-e35c` F5 recommends is `F`-free. What the demand needs is the `n`-freeness
>    and the **value of L4's threshold `ε₀`** — a *different property of L4* from the one the
>    gate names.
> 2. **INSUFFICIENT.** Even a complete answer to every L4 question leaves the demand constant
>    undetermined, because `ε_dem = ε_leak²/(2C₃)` and **`C₃` is unquantified and is not an L4
>    question at all** — it is L3 / prefix capture, whose source conjecture is open *and*, as
>    literally worded, too weak to use (`Op-Form:§4.3`, `§8.1`). **`mg-6bc2`'s FIRST disjunct
>    would not have unblocked its title question either.**
>
> **And the route's actual stopping point is not L4** (§6). Pair bias alone reaches a constant
> uniform in `n`, and **the constant it reaches is `1`** — already proven, already in the
> corpus, at `Op-Form` Claim 6.1 / ledger claim 26. Everything below `1` requires a
> *realizability* fact about real posets, which is exactly the boundary `STATE.md:17` and
> `mg-92e6`'s own ticket already name. **The route stops at the marginal/joint boundary, and
> that boundary has nothing to do with L4.**

---

## 1. The split that has to happen before the question can be answered

`ε_spec` names two different numbers, and `mg-6bc2` asks about both in consecutive sentences.

| | definition | who fixes it |
|---|---|---|
| **`ε_sup`** (supply) | the smallest `c` for which we can **prove** `E[inv_e] ≤ (c/6)(n²−1)` for every frozen `P` | the mathematics of frozen posets |
| **`ε_dem`** (demand) | the largest `c` for which `1 − λ_std ≤ c` makes the architecture's downstream **fire** | L4, L3, Cheeger |

`(LIB-const)` is a *true statement* at `ε_sup` and a *useful* one iff `ε_sup ≤ ε_dem`. The wall
is the inequality, not either number. Daniel's ask carries both halves in two sentences:

> *"we now need to know exactly what constant is consumed"* — that is `ε_dem`.
> *"We should get 1/6 or something via pair bias alone!"* — that is `ε_sup`.

**This split is doing the work in this document and it is also where I predicted I would fail**
(`PREDICTIONS.md` P8): it is the neighbour of the conflation `pm-onethird` made on 2026-08-07 —
mistaking a *consumption* result for a *provability* result. I am making the split explicit
rather than trusting myself to hold it.

---

## 2. (A) for the supply side — the dependency list, exhibited

**Claim 2.1.** *The derivation of an explicit absolute `ε_sup`, uniform in `n`, from pair bias
has the following complete dependency list.* **[PROVEN — the derivation is `Op-Form` Claim 6.1,
already labelled PROVEN and audited; what is established here is the list]**

| # | ingredient | where |
|---|---|---|
| 1 | `inv_e(σ)` = incomparable pairs flipped against the distinguished order `e` | `STATE.md` glossary |
| 2 | the frozen hypothesis `δ(P) < 1/3`, i.e. `Pr[j ≺_σ i] < 1/3` for each incomparable pair | minimal-counterexample condition |
| 3 | coherence: the `>2/3` majorities cohere into a single linear order `e` — a *consequence* of 2, not an extra hypothesis (`mg-61bb`, proven) | `STATE.md` glossary, attempt index |
| 4 | linearity of expectation | — |
| 5 | *(only for the `λ_std` rendering)* `mg-210d`'s master bound `1 − λ_std ≤ 6E[inv]/(n²−1)` | `Op-Form:§6.1` |

**L4 is not on this list, and neither is `Δ₁`, a prefix, a cut, Cheeger, `C₃`, or Step 6.**

The derivation is three lines and is already in the corpus:

`E[inv_e] = Σ_{i<j, i∥j} Pr[j ≺_σ i] < m/3` where `m` = #incomparable pairs
(`Op-Form` Claim 6.1). Writing `d = m/C(n,2)` and matching against `(ε/6)(n²−1)`:

```
ε_sup  ≤  2m/(n²−1)  =  d · n/(n+1)  <  1        for every n, uniformly.
```

**Machine check (`out_p1_ledger_depgraph.txt`).** Parsing `mg-88bd`'s own claim ledger
(`Op-Form:§9`, 36 rows, 11 recorded dependency edges) and taking the transitive closure:

* transitive dependents of ledger **claim 4** ("L4's `F` is `n`-free") = **`[12, 17, 18, 23]`**;
* **0 of 5** supply-path claims — `21, 22, 25, 26, 27` — reach claim 4. Claims **25 and 26
  carry no `CONDITIONAL on` clause of any kind**; they are labelled flat **PROVEN**.

**Machine check (`out_p3_algebra.txt`), exact rationals, no floating point.** `E_unif[footrule]
= (n²−1)/3` reproduces by brute force to `n = 7` and by re-derived sum to `n = 59`; the
conversion `ε = 2m/(n²−1) = d·n/(n+1)` holds at **0 mismatches** over the `(n, m)` grid; and
feeding `m/3` through the master bound reproduces `Op-Form:§6.3`'s recorded `d·n/(n+1)` — the
same degenerate bound `mg-210d` recorded — at **0 mismatches**.

> **So the pair-bias derivation of an explicit absolute `ε_spec` is not merely independent of
> L4; it already exists, it is already proven, and it lands at `1`.** What `mg-6bc2` would be
> unblocked to do is *sharpen* it — and every sharpening tool it names (`mg-92e6`'s
> diagonal-capacity bound, the per-element bias `b_x`, the Diaconis–Graham conversions) sits on
> the same L4-free list. None of them takes a `Δ₁`, a prefix, or a modulus as input.

---

## 3. Why the independence is *forced*, and the one named escape

"Does not happen to invoke L4" is weaker than "cannot invoke L4". The stronger form holds,
conditionally, and the condition is worth stating because the corpus contains its escape.

L4's **hypothesis** is `Δ₁(A, B) ≤ ε`. In the architecture as stated, the only route from the
frozen hypothesis to a thin prefix runs **through L1b's conclusion** — the very statement being
derived. Reachability, `out_p2_architecture_graph.txt`, arm A:

```
frozen -> pair bias -> [1 - λ_std ≤ ε_spec] -> thin prefix -> L4 fires     (1 path)
frozen -> ...                    avoiding    [1 - λ_std ≤ ε_spec] ...      (0 paths)
```

**So a derivation of L1b that invoked L4 would be circular.** The independence is not a
stylistic choice available to whoever writes the derivation; it is the only non-circular option.
**[PROVEN, on the hand-transcribed step graph of §ARCH_EDGES — the transcription is declared and
its provenance is printed per edge.]**

**The escape, and I went looking for it rather than waiting to be shown it.** The direct-prefix
route (`mg-00b9` Lemma A/B, **repaired** by `mg-2de0`) converts an inversion bound to prefix
thinness **with no spectral statement**. Adding that one edge, arm B:

```
frozen -> pair bias -> thin prefix -> L4 fires        (1 path avoiding L1b)
```

Three things about it, in order of importance:

1. **What it would buy is not an L4-dependent `ε_spec`. It is a vacuous one.** L4 fired from a
   thin prefix reached without L1b contradicts `δ(P) < 1/3` outright — the frozen class is empty,
   and every statement about minimal counterexamples is vacuously true, `ε_spec` included. That
   **dissolves** the pair-bias question rather than answering it; it does not make the pair-bias
   derivation depend on L4.
2. **It is not open today.** The repaired direct route reaches `Δ₁ ≤ 2/3`
   (`mg-2de0:§0`, and `2/3` is that audit's *improvement* on `mg-00b9`'s own headline); L4 is
   calibrated at `ε_leak ≈ 0.20`. `2/3 > 0.20`.
3. **It is the same `ε_leak`.** `mg-2de0:§4` traced both routes symbol by symbol and confirmed
   the direct and spectral requirements are the requirement for the same conclusion at the same
   `ε_leak` — so this escape is measured against the same threshold, not a different one.

**Therefore §3's conclusion is CONDITIONAL, and the condition is named:** the independence is
forced *unless* the direct-prefix route is pushed from `2/3` to `≈0.20`, at which point the
question dissolves instead.

---

## 4. (B) for the demand side — the step, exhibited

The demand chain, backwards, with each conversion's status:

```
ε_dem  ≤  ε_leak² / (2·C₃)            Cheeger sandwich, Op-Form §4.2  [PROVEN as a relation]
                    ^        ^
                    |        +-- C₃ : L3 / prefix-restriction loss    [UNQUANTIFIED, §4.3/§8.1]
                    +----------- ε_leak : the threshold at which L4 fires  [L4]
```

**The step, named exactly.** `Op-Form:§6.4`, the row *"read off modulus"* — superseded by
`mg-e35c` F5 and replaced by *"the `ε` at which `mg-3ce3`'s `survives` predicate first fails"*.
That is the single site where an L4 fact enters the value of `ε_dem`, and everything downstream
of it (`Cheeger`, `master bound`) is `n`-free arithmetic on whatever number it produces.

**What it needs from L4:** the threshold `ε₀` below which L4's Step-6-consumable content holds,
and the `n`-freeness of that threshold. It is currently supplied **empirically** —
`mg-3ce3`'s 0 RED over 6681 posets up to `ε = 0.20` — which is a calibration, not a derivation.

**A machine observation I did not expect.** Ledger claim **28** — the constant budget itself —
**does not reach claim 4** in the recorded dependency graph. Its label does not record it as
conditional on the modulus; it records it as **"BROKEN as derived (mg-e35c F5)"**. The residue
channel (which surfaces integers in a label that the edge parser did not capture, precisely so
they are adjudicated rather than dropped) flags claim 28's label as mentioning both `L4` and
`C₃` with no captured edge to either. **Hand adjudication: both are genuine dependencies that
the ledger cannot express as claim numbers, because neither L4 nor `C₃` is a claim in this
ledger.** The correct reading of claim 28 is not "L4-conditional" — it is **not derived at all**.

---

## 5. The gate `mg-6bc2` names is the wrong gate, twice over

### 5.1 Narrower than named — the demand does not consume the *modulus*

`mg-6bc2` gates on *"L4's modulus question"*. Take the three branches in turn and ask, for each,
whether `F` appears in anything **Step 6 can consume**:

| branch | does `F` appear in what Step 6 consumes? | authority |
|---|---|---|
| (i) `P` contains a 1/3-balanced pair | **no** — trivial closure, `F`-free | `Op-Form:§3.3` |
| (ii) remove/modify `≤ F(ε)n` interface elements | **moot** — unconsumable by Step 6's stated transfer for **every strictly positive** `F`, `o(ε)` included | `mg-3af9`, UNCONDITIONAL, audited `mg-c8c6` |
| (iii) repaired: *a balanced pair remains in `[1/3,2/3]`* | **no** — the repair `mg-e35c` F5 recommends removes `F` from (iii) entirely | `mg-e35c` F5 |

> **So what Step 6 consumes is an `F`-free statement: "if `Δ₁ ≤ ε₀` then (i) or (iii-exact)".
> The demand's dependency on L4 is a dependency on that statement's THRESHOLD `ε₀`, not on its
> MODULUS `F`.**

**SCOPE DISCIPLINE — read this before citing the row above.** Every entry is a statement about
what Step 6 **consumes**. **None of it says L4-as-stated is or is not provable at an `n`-free
modulus.** That question is untouched here and stays open. `mg-345e`'s own body warns that
`pm-onethird` conflated consumption with provability on 2026-08-07 and had to reverse; the claim
made here is the consumption one only, and it is *narrower* than the provability question rather
than a substitute for it. The `n`-freeness of `F` remains exactly as open as it was — this
document's point is that **Step 6 does not consume its answer**, so answering it would not, by
itself, pin `ε_dem`.

### 5.2 Insufficient — `C₃` is a second gate and it is not an L4 question

`ε_dem = ε_leak²/(2C₃)`. `Op-Form:§8.1` records `C₃` as unquantified, and the Prefix-capture
conjecture that would quantify it as **(a) open** and **(b) as literally worded, too weak to
use** — literally worded it gives a *constant floor*, not a small gap, so under that reading
"the chain does not merely acquire an `n` — it breaks outright" (`Op-Form:§4.3`).

**Consequence:** answering L4's modulus question in the affirmative tomorrow would still leave
`ε_dem` undetermined. **`mg-6bc2`'s first disjunct is not sufficient for its title question.**
The second disjunct — this ticket — is what is actually available.

### 5.3 A rider on the live figure, found on the way

`ε_dem` is carried at `STATE.md:15` as `ε_spec ≲ 2×10⁻²`. Exactly: `0.20²/2 = 1/50`. **That is
the `C₃ = 1` value** (`out_p3_algebra.txt`, C5) — the live headline drops `C₃` even though the
same document records it as unquantified. `C₃` is a **loss** factor (`≥ 1`), so dropping it
yields the **largest** budget: **the omission runs in the optimistic direction.** This is not
new mathematics — `Op-Form:§6.4`'s master-bound row does carry the `/C₃` — it is the observation
that the figure most often quoted is the one where it was dropped.

**And the published gap factor is a ratio across the split.** `d101026` landed "the repaired gap
factor is ~50, not ~5×10³". `out_p3_algebra.txt` C6 reproduces `50` exactly and identifies both
ends: **numerator = the pair-bias supply constant `1`; denominator = the L4-calibrated demand
`1/50`.** So the corpus's headline distance-to-the-wall is `ε_sup/ε_dem` — the ratio of an
L4-**independent** quantity to an L4-**dependent** one. Shrinking it from the left needs no L4
answer at all.

---

## 6. Where the route actually stops — and it is not L4

Answer (C) of the ticket's menu is not the verdict, but the ticket is right that "where it stops"
is the useful thing to say, so:

**The route reaches a constant. It stops at *usefulness*, not at *constancy*, and it stops at
the marginal/joint boundary.**

`ε_sup ≤ sup_{frozen P} d·n/(n+1)`. To get below `1` there are exactly two levers:

1. **Improve the per-pair `1/3`.** The frozen hypothesis gives `Pr[flip] < 1/3` per pair, and
   `E[inv_e] = Σ Pr[flip]` is an identity — so `m/3` is *saturated* by the per-pair information.
   Improving it means showing that not all incomparable pairs can sit at `1/3` **at once**,
   which is a joint fact about a real poset's linear-extension measure.
2. **Bound `d` above for frozen posets.** `d` is not pair-bias information at all — it is
   structural.

**Both levers are outside "pair bias alone", and the corpus already says so from two directions.**
`STATE.md:17` and the *why it is hard* paragraph: both faces of the single lemma are **false for
abstract frozen distributions**, so the proof *must* use that `σ` ranges over a genuine poset's
linear extensions. `mg-92e6`'s own ticket states the identical boundary from the matrix side:
*"`Pr[x before y]` is a functional of the JOINT distribution of the pair, NOT of the
single-element marginals"* — and `mg-92e6`'s landed result **pins the exact marginal-only
ceiling** and identifies the extra juice as one *joint* fact (adjacency symmetry).

**Prediction P5, run.** A grep for a frozen-conditional **upper** bound on incomparability
density returns **0** — the two hits are both the *required* density in `Op-Form:§7.3`'s
arithmetic, not a proven one. Every density fact on record runs the other way: primitivity
forces `m ≥ n−1`, and `mg-e2de` forces co-degree `≥ 2`. **Lower bounds only.**

> **So, read literally — per-pair marginals ALONE — the constant is `1`, and `1` is all that
> information contains.** That is a statement about the *information content* of pair bias, not a
> verdict on `mg-6bc2`'s conjecture: the moment `mg-92e6`'s diagonal-capacity bound, `b_x`, or a
> Diaconis–Graham conversion is admitted, the route is no longer "pair bias alone" — and **all
> three of those are still L4-free**, so the independence verdict is unaffected either way.
> **[PROVEN for the saturation of `m/3`; the density claim is the P5 grep, which is a survey of
> this corpus and not a theorem.]**

**On the `1/6` itself — routing only, not an attempt.** `1/6` occurs twice in this corpus and
neither occurrence is a supply-side derivation. `Op-Form:§6.4`'s *"slack `≤ 1/6` for a centred
pair"* is a **demand**-side number and `mg-e35c` F5 ruled that row **BROKEN as labelled** (it
reads a *necessary* condition at the *maximum possible* slack as a calibration point). `mg-e2de`'s
`1/6` is the collapse value of a **local `δ` lower bound** at co-degree 2. **Whether either is
Daniel's `1/6` is `mg-6bc2`'s question and I have not attempted it.**

---

## 7. What this means for `mg-6bc2`

1. **Its second disjunct is satisfied. It unblocks now, on this finding, not on L4.** The
   pair-bias route to an explicit absolute `ε_spec` is L4-free, and §3 shows it *must* be.
2. **The unblocked work is the SUPPLY half — sharpening `1`.** That is `mg-6bc2`'s conjecture
   and it is fully available today.
3. **Its TITLE half — "exactly what constant the architecture consumes" — is a different
   question and remains gated.** Recommend `pm-onethird` either split it or restate its gate as:
   *"blocked on (a) L4's consumable threshold `ε₀`, and (b) `C₃`"* — **not** on L4's modulus,
   which §5.1 shows Step 6 does not consume, and **not** on L4 alone, which §5.2 shows is
   insufficient.
4. **Nothing here discharges L4.** Row 11 is untouched. The modulus question is exactly as open
   as it was this morning.

---

## 8. Predictions, scored — including the refuted ones, kept as written

| # | prediction | outcome |
|---|---|---|
| P1 | claim 23 in dependents-of-4; 25, 26 outside | **HELD** — `[12, 17, 18, 23]` |
| P2 | dependents-of-4 has 4–8 members | **HELD, at the boundary** — exactly 4 |
| P3 | 0 supply-path claims reach 4 | **HELD** — 0 of 5 |
| P4 | algebra reproduces `d·n/(n+1)` and `(n²−1)/3` at 0 mismatches | **HELD** |
| P5 | corpus contains no frozen-conditional upper bound on `d` | **HELD** — 0 hits |
| P6 | mutation control fires | **HELD** — S2 and S3 both |
| P7 | I will write a sentence stating the independence without naming which `ε_spec` | **HELD — and it was the verdict box.** The first draft's headline read "the pair-bias derivation is INDEPENDENT of L4" with the supply/demand table added afterwards. Repaired before landing by putting the table *inside* the verdict rather than below it. |
| P8 | my most likely error: conflating "constant" with "sufficient" | **HELD as a risk, and the split in §1 is the guard I built against it.** Whether it survived contact is for `mg-6bd1` to say, not me. |
| **P9** | **11–20 dependency edges** | **REFUTED — 11.** I predicted `12–20` and the ledger records **11**. Kept as written. The direction matters: I over-estimated how much of this document's dependency structure is *recorded* rather than *implicit*, which is the same over-trust in the ledger that §4's claim-28 finding punishes. |
| P10 | the instrument cannot express the `ε₀`-vs-`F` finding | **HELD.** §5.1 is a reading of what Step 6 consumes and no dependency graph over a claim ledger can carry it. **The mechanised part of this ticket was the cheap part.** |

---

## 9. Defects of this instrument, and what I did not do

**Defect 1 — my dependency parser under-read, and my own selftest caught it, not my eye.**
The first form of `DEP` used a lazy quantifier, so `CONDITIONAL on 1, 4, 13, 16` parsed as
`1, 4` and **silently dropped two edges, including `17 ← 13`**. Construction S4 failed and named
it. It is fixed, the comment in `lib345e.py` records it, and the construction is kept. **A
dependency parser that under-reads is exactly the failure mode this ticket is about** — it would
have made things look *more* independent than they are, i.e. it fails in the direction that
flatters this document's verdict.

**Defect 2 — the ledger graph scores a claim by its label, not by its mathematics.** A claim
whose recorded label understates its dependencies is scored independent here. This is printed at
the top of every `p1` run and it is why §2's argument does not rest on the graph: the graph
corroborates a dependency list derived by reading, and claim 28 (§4) is the case where the label
and the mathematics visibly disagree.

**Defect 3 — `ARCH_EDGES` is a hand transcription.** §3's reachability result is only as good as
that transcription. Its provenance is printed per edge so a wrong edge is contestable rather
than buried, but nothing mechanical checks it against the source `.tex`.

### Not done, deliberately

- **No poset enumeration of any kind.** The 1/3–2/3 conjecture is verified for **all** posets to
  `n = 14` (`mg-33f5`), so **the frozen class is empty at every `n` this corpus can enumerate.**
  Any empirical calibration of `ε_sup` would be measuring a hypothetical population, and a
  near-frozen sweep would be measuring non-counterexamples. **The attractive cheap check is
  declared and refused**, not overlooked.
- **No attempt at L4.** Row 11 is untouched. Whether L4-as-stated is provable at an `n`-free
  modulus is exactly as open as before.
- **No attempt at the `ε_spec` derivation.** That is `mg-6bc2`'s job once unblocked. §6 says
  where the route stops; it does not try to push past it. **No claim is made here about whether
  `1/6` is the right answer.**
- **No re-derivation** of `mg-92e6`'s diagonal-capacity bound, the per-element bias `b_x`, the
  Diaconis–Graham conversions, or `mg-210d`'s master bound. Claim 2.1 places them on the
  dependency list; it does not re-prove them.
- **`C₃` is not quantified here.** §5.2 establishes that it gates the demand constant and that it
  is not an L4 question. It does not attempt prefix capture.
- **No edit to `one_third_width_three`** (different repo).
- **The source `.tex` was not opened.** Every `tex:` line reference in this document is quoted at
  second hand from `Op-Form`, which is audited (`mg-e35c`). §3's step graph inherits that.
