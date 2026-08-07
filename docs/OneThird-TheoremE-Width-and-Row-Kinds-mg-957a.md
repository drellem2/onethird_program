# Theorem E's width, and the kind of every ledger row (mg-957a)

*Landed against `STATE.md` and `docs/state-of-the-wall.html`. Filed by pm-onethird as mg-957a,
relaying mg-e768's correction of pm-onethird's own earlier framing.*

---

## 0. The headline, and it corrects the ticket that commissioned it

The ticket is titled *"Theorem E's width is WRONG in the ledger and has been for months"* and
instructs: **"DO NOT SPLIT THE DIFFERENCE. One of the two documents is wrong."**

**Neither document states a falsehood.** `STATE.md`'s `any` is correct mathematics; `step8.tex`'s
`width-3` is a true-but-narrow statement, narrower than its own proof. The ticket itself offered
this as its second branch — *"the theorem generalises and the source is merely stated narrowly →
say what the general statement is and what proves it"* — and that branch is the one that holds, so
the *"one of the two is wrong"* instruction is the part that does not survive. **What was actually
wrong is the ledger's WARRANT, not its CLAIM:** row 6 asserted `any` while citing a source that
says `width-3`, with nothing recorded in between, and an auditor who noticed
(mg-e35c **F12**) was ruled out of scope. A correct claim carried without its derivation is
indistinguishable from a wrong one until somebody reads the source — which is exactly what
happened for months.

And the ticket's *own* diagnosis of the deeper defect is the part that does survive, verbatim:

> *"A sentence that says 'all proven' over a set containing an `n ≤ 7` empirical row is FALSE
> however true each row is individually."*

That is a different defect from any individual row being wrong, and it is the one that survives
fixing rows one at a time. §2 is the repair for it.

---

## 1. Theorem E's width — settled by reading the source

### 1.1 What was known going in

mg-e768 Part B established that **the width-3 hypothesis is PRESENT** in Theorem E's statement and
in both of its lemmas. It did **not** establish that the hypothesis is **ESSENTIAL**. Those are
different questions and mg-e768 correctly declined to answer the second. This section answers it.

### 1.2 Where the hypothesis appears — 5 sites

All references are to `one_third_width_three/step8.tex` (3,544 lines) at the revision read on
2026-08-07.

| site | text | role |
|---|---|---|
| `:21` | *"Throughout, `P = (X, ≤_P)` is a finite poset of width 3"* | **blanket Setup hypothesis for the whole file** |
| `:60` | *"If `P` is a width-3 indecomposable `γ`-counterexample on `n ≥ 2` elements"* | Theorem E statement |
| `:158` | *"…in every width-3 indecomposable counterexample…"* | prose preamble to the lemma |
| `:196` | *"Let `P` be a width-3 indecomposable `γ`-counterexample…"* | Lemma `frozen-pair-existence` statement |
| `:332` | *"Let `P` be a width-3 indecomposable `γ`-counterexample…"* | Theorem E proof, restating its own hypothesis |

The `:21` site is the origin of the other four. `step8.tex` is the final-assembly section of a paper
whose **own main theorem is the width-3 case of 1/3–2/3** (`:531–533`, *"Width-3 1/3–2/3, conditional
on Steps 1–7 and on Hypothesis…"*). Every statement in that file inherits the phrase whether or not
it needs it. **That is the legitimate somewhere the `any` could have come from** — the third branch
the ticket offered — but nobody had written it down, which is why the row read as a contradiction.

### 1.3 Where the hypothesis is consumed — 0 sites

Theorem E's proof is four short pieces. I read each and recorded which hypotheses each step actually
spends:

| piece | lines | what its proof consumes | width used? |
|---|---|---|---|
| Lemma `dirichlet-conductance` | `:122–152` | `π(S)π(Sᶜ) ≤ min(π(S), π(Sᶜ))` and the definitions of `Φ`, `E`, `vol`. A general reversible-chain inequality. | **no** |
| Lemma `indec-incompairs` (`I(P) ≥ n/2`) | `:167–195` | indecomposability only: if some `x` is comparable to everything then `P = (A ∪ {x}) ⊕ B` (or a degenerate variant), contradicting indecomposability. | **no** |
| Lemma `frozen-pair-existence` | `:196–270` | **Step 1** at most `n−1` adjacent positions per `σ`, giving `Σ_{x∥y} E(f_xy) ≤ 1/2`; **Step 2** the `γ`-counterexample hypothesis, giving `Var(f_xy) = p(1−p) ≥ γ(1−γ) ≥ γ/2`; **Step 3** `I(P) ≥ n/2` from the previous lemma; **Step 4** `min ≤` ratio of sums. | **no** |
| Theorem E proof | `:330–370` | the previous lemma, plus `β(P) ≥ γ ⟹ p_xy ≥ γ` and `1 − p_xy ≥ γ` for the volume bound. | **no** |

**No step of any of the four consumes the width.** Nor do the ambient definitions: the BK graph, the
Dirichlet form, `Φ`, `vol`, and *`γ`-counterexample* (`:31–34` — a condition on incomparable pairs)
are all width-free.

### 1.4 The general statement, and what proves it

> **Theorem E (general form).** Set `c₀ := γ` and `η(γ,n) := 2/(γn)`. If `P` is an **indecomposable**
> `γ`-counterexample on `n ≥ 2` elements — **no width hypothesis** — then there is a cut
> `S ⊆ L(P)` with `vol(S) ≥ c₀·vol(L(P))` and `Φ(S) ≤ η(γ,n)`.

**What proves it: delete `width-3` from `step8.tex:60` and the same four proofs stand verbatim.**
Nothing is added, nothing is repaired, no step is re-argued. That is the whole content of the
generalisation, and it is why the ledger's `any` was right all along.

### 1.5 What this does NOT cover — stated because it is the part that could still bite

- **The Step-8 cascade downstream of Theorem E is genuinely width-3 and is untouched here.**
  Proposition `G2` and everything after (`:424` ff) runs on *layered width-3 decompositions* with a
  Step-7 *interaction width*, and `:696` explicitly says Lemma 4.2 of `step5.tex` *"exhausts all
  width-3 posets."* This document generalises **Theorem E alone** — the single object ledger row 6
  names. It says nothing about the width-3 paper's main theorem, which is and remains width-3.
- **No machine check.** This is a reading of the LaTeX. The steps are short and elementary and I
  followed each; that is a different assurance from a proof assistant.
- **The Lean artifact was not inspected.** `step8.tex:548` cites
  `lean/OneThird/MainTheorem.lean`, `width3_one_third_two_thirds`. A formalisation may carry
  `width-3` as a real hypothesis of the formal statement even where the paper proof does not use it.
  If anybody cites *"Theorem E, formalised"* at any width, that has to be checked first.
- **I did not re-verify the mathematics of the four proof steps as mathematics** beyond following
  them. The claim landed here is about *which hypotheses the written argument spends*, which is a
  weaker and more checkable claim than *the argument is correct*.

---

## 2. The actual deliverable — kinds at the row, weakest kind in aggregating prose

### 2.1 The cut, and whose it is

pm-onethird supplied an **individual-vs-category** cut and has **withdrawn it**: nothing in the 19
rows is categorical. mg-e768 replaced it, and the replacement is what is landed:

| mark | name | meaning | usable against a minimal counterexample? |
|---|---|---|---|
| `U` | **pointwise-universal** | proven for **every** finite poset; instantiates at the counterexample's own `n` for free | **yes** |
| `U-id` | **identity** | an exact identity or definitional equivalence — holds by algebra, consumes no hypothesis | **yes**, and it transfers freely |
| `FP` | **finite population** | an exhaustive check over a finite set of small posets; says nothing above the largest `n` checked | **NO** |
| `FP✗` | **finite population, refuting** | a finite population exhibiting a **counterexample** | **yes, at universal strength** |
| `OPEN` | — | no warrant of any kind | no |

**The `FP`/`FP✗` split is not decoration.** A finite population can **refute** a universal outright
and can **never establish** one. Ledger row 9 (*L2 monotonicity, false as stated, 2/126 at n=6*) is
`FP✗` and is as strong as anything in the table. Rows 3b and 10 are `FP` and are not evidence at
unbounded `n` at all — which is the entire problem, because a minimal counterexample's `n` is
unknown and unbounded.

### 2.2 The standing rule

> **Every row carries its kind, at the row. Any prose that AGGREGATES rows must state the WEAKEST
> kind in the set it names.**

Aggregation order: `U`/`U-id` ≻ `FP` ≻ `OPEN`. `FP✗` is a refutation rather than support; a set
asserted to *support* something is not repaired by relabelling one member `FP✗` — it is false in a
second way and should be reworded.

This is the durable half of the deliverable. **Marking rows is not a substitute for the rule**: the
aggregation defect survives fixing every row individually, which is exactly how it survived until
now.

### 2.3 The marks

| # | row | kind | why |
|---|---|---|---|
| 1 | `λ_std = 1 ⟺ ordinal sum` | `U` | proven for every finite poset |
| 2 | ordinal sum ⟺ incomparability graph disconnected | `U-id` | equivalence of definitions |
| 3a | `S_P = ρ_std(η_P)` | `U-id` | an identity |
| 3b | **standard dominance** | ~~⚠️ `FP`~~ → ⚠️ **`FP✗`** (uncond.) / **`OPEN`** (cond. = row 8) | ~~empirical `0/132`, `n ≤ 7`~~ — **SUPERSEDED (mg-55f2, on mg-65f5 §1.5): the `0/132` is a SAMPLING ARTIFACT** (frame: `n ≤ 6` exhaustive + `n = 7` top-λ spot only), the unconditional form is **REFUTED** by 166 moderate-λ `n = 7` refuters outside that frame (mg-8b64, read-not-measured), and the conditional form **is L1b**. **load-bearing, see §3.1** |
| 4 | (A) SPREAD | `U` | proven |
| 5 | easy/Buser, every cut | `U` | proven |
| 6 | **Theorem E** | `U` | proven; the width warrant is §1 |
| 7 | identities GID & DG | `U-id` | identities |
| 8 | L1b — the wall | `OPEN` | |
| 9 | L2 monotonicity | `FP✗` | false as stated, `2/126` at `n=6` — a refutation, universal-strength |
| 10 | **L3 best-cut-is-a-prefix** | ⚠️ `FP` | `125/126`, `n ≤ 6` — **load-bearing, and not unanimous** |
| 11 | L4 | `OPEN` | |

**Scope of the column, so it is not over-read.** These marks classify **the kind of warrant each
row's own recorded `Status` claims** — they do not re-verify the mathematics. A row whose status
says *proven* is marked `U`/`U-id` on the ledger's authority; a row whose status says *empirical
`k/N` at `n ≤ m`* is `FP` **by construction of that status**, and that half of the column is not a
judgement at all. Re-auditing the proofs behind the `U` rows was not attempted.

### 2.4 The aggregating sentences repaired

Five sites in `STATE.md`, four in `docs/state-of-the-wall.html`:

| site | was | now |
|---|---|---|
| `STATE.md` one-paragraph state | *"…along with **all the machinery** that reduces the whole conjecture to one implication"* | names the `FP` member and states the weakest kind |
| `STATE.md` chain summary | *"the rest are **proven or empirical**"* | a disjunction naming both kinds and committing to neither → names rows 3b, 10, 9 and states weakest = `FP` |
| `STATE.md` machinery sentence (**the ticket's defect 2**) | *"(**all proven**, any-width)"* | per-item kinds + weakest-kind banner + §3.1's unresolved question |
| `STATE.md` mermaid link C→D | *"PROVEN+emp"* | `WEAKEST KIND FP`, with row 5 `U` and row 10 `FP` named separately |
| `STATE.md` width-3 baggage note | *"The skeleton above has zero width dependence."* | same claim, now with row 6's warrant attached |
| `state-of-the-wall.html` ×4 | mirrors of the above, plus a `Kind` column added to its ledger | as above |

**The HTML was repaired rather than left**, because it is reader-facing and carried the identical
false sentence verbatim; fixing the `.md` alone would have been the same one-row-at-a-time failure
in a second file. It remains a **2026-07-19 rendering** and is stale in other respects — that is now
said on its face rather than inferable from the date line.

---

## 3. Two live ambiguities — NOT resolved here, and deliberately

The ticket names both and instructs: *"If your work depends on either, STOP and say so rather than
picking a reading."* Neither is resolved, and the landed prose is **correct under both readings** of
each.

### 3.1 Does L1b's reduction consume row 3a alone, or does it need row 3b?

`STATE.md`'s machinery sentence names **"standard dominance"** and glosses it *"the gap lives in the
standard sector, so a combinatorial bound controls `λ_std`."* **The gloss is row 3a**
(`S_P = ρ_std(η_P)`, `U-id`, **proven**). **The name is row 3b** (~~`FP`, `0/132`, `n ≤ 7`~~ — see
the correction below).

> **CORRECTION (mg-55f2, landing mg-65f5 §1.5).** Row 3b's `0/132` **cannot be quoted bare**: it is
> `0` failures inside the frame its own source declares — *"`n ≤ 6` exhaustive + `n = 7` top-λ
> spot"* (mg-b0a6 `:286`) — and `mg-8b64`'s **166 explicit refuters at moderate-λ `n = 7`** sit
> outside it, which L1b's own document states at `:310–313`. So **unconditional** standard
> dominance is **refuted** (`FP✗`), and the **all-pairs-frozen conditional** that remains open **is
> L1b**. The fork below is also settled — and **neither branch is right**: mg-65f5 finds row 3b is
> L1b's *conclusion*, not an input, so the error was a **CIRCULARITY**. That repair is `mg-a1db`'s
> and is not applied here. (`166`/`0/132` read from the probe documents, **not re-measured**.)

- If **3a alone** suffices, the old *"all proven"* was a **NAME/GLOSS SLIP** — right rows, wrong
  label.
- If **3b** is genuinely needed, it was a **FALSE BELIEF** about the reduction's own footing, and
  L1b's machinery rests on an `n ≤ 7` exhaustive check.

**These are materially different findings and I did not pick one.** mg-e768 could not settle it;
re-searched at mg-957a, the phrase *standard dominance* occurs in exactly three places in the whole
corpus — `STATE.md:74` (the sentence itself), `STATE.md:109` (row 3b), and
`docs/OneThird-LIBweak-mg-c3ca.md:258` (which repeats the status, not the dependency). **Nothing in
the corpus records what L1b's reduction actually consumes.** The repaired sentence states the
weakest kind present and records the fork, which is true either way.

*Third worker to flag this rather than guess.*

### 3.2 Is Theorem E's width-3 hypothesis essential?

This one **is** answered — §1 — and it is answered by **reading `step8.tex`'s four proofs and
recording which hypotheses each step spends**, not by picking a reading. The distinction the ticket
draws (*present* vs *essential*) is exactly right and is why the answer needed the source rather
than the ledger. The residual uncertainties are named in §1.5 and are about the **Lean artifact**
and the **downstream cascade**, not about the theorem.

---

## 4. What I did not do

- **I did not resolve §3.1** (3a-vs-3b), and no sentence landed depends on its resolution.
- **I did not audit the mathematics of the `U` rows.** The `Kind` column classifies the kind of
  warrant a row's status claims, not whether that status is earned.
- **I did not machine-check Theorem E**, and **I did not open the Lean formalisation** (§1.5).
- **I did not generalise anything downstream of Theorem E.** The Step-8 cascade is width-3 and
  stays so.
- **I did not determine what row 10's failing instance is.** `125/126` means one poset at `n ≤ 6`
  already fails L3, so L3-as-a-universal has a known exception; whether the statement survives
  excluding that instance is untouched here and is flagged at the row.
- **I did not sweep the attempt index for aggregation defects.** Its cells carry *per-attempt
  verdicts*, not claims over sets of ledger rows, so the standing rule has no purchase on them as
  written — but that is a judgement about their current wording, not a guarantee, and I did not
  audit all 24 of them for it.
- **I did not regenerate `state-of-the-wall.html`.** It is a hand-built 2026-07-19 rendering; I
  repaired the kind-relevant sites and marked its staleness, and left its other drift (e.g. its row
  8 still says `λ_std → 1` where `STATE.md` now leads with `1 − λ_std ≤ ε_spec`) alone.
- **I did not edit `one_third_width_three/step8.tex`.** It is a different repository and its
  narrow statement is not false. Deleting `width-3` from `:60` there is a one-line change that
  §1.4 licenses, and it is somebody's call, not mine.
