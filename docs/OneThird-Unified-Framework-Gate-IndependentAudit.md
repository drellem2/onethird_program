# Independent audit of the unified-framework gate (mg-8fd1)

**Auditor:** mg-446b, pre-filed before mg-8fd1 committed. **Target:**
`docs/OneThird-Unified-Framework-Gate.md` + `code/unified_gate_8fd1/` at `97cb533` — the gate that
sets the scope of the research line Daniel commissioned on 2026-07-30 11:15Z.
**Instruments:** `code/unified_gate_audit_446b/` — `audit_quotes.py` (textual fidelity),
`audit_l1.py` (Proposition N2 re-derived from its definition, plus the quantifier test),
`audit_l2.py` (the whole population from scratch), `audit_crosscheck.py` (numbers the *existing*
pipeline already carries, re-derived), `audit_proof.py` (the theorem's written proof attacked),
`audit_beyond.py` (n = 7, 8, 9 and the quality of the target's own beyond-range evidence),
`audit_scope.py` (targets 3 and 4). `run_all.sh`, pure Python 3, 2 min 0 s, seven `out_*.txt`.
**Shares no code with `code/unified_gate_8fd1/` or `code/hodge_leverage/.`**

Deliberate divergences, so that a shared bug cannot hide: posets are enumerated at `n ≤ 5` by
**brute force over every relation on `[n]`** (not by the transitively-closed-upper-triangle trick),
acyclicity is decided by **Kahn peeling** and cross-checked against **"is there an ordering of the
blocks in which every arrow strictly increases the index"** (the target uses a bitmask transitive
closure; `lrb.py` uses DFS three-colouring — three routes in total), and the enumeration is certified
from **outside the repository**: isomorphism-class counts against A000112 (`1,2,5,16,63,318`) and
`Σ n!/|Aut(P)|` against A001035 (`1,3,19,219,4231,130023`), both matched at every `n ≤ 6`.

---

## VERDICT: **OVERSTATED — 1 BROKEN, 2 MAJOR, 4 MINOR. The L2 answer, the population, the theorem and the two-worlds conclusion all STAND and all reproduce. The BROKEN item is inside the theorem's own proof, in material beyond the brief — for the sixth consecutive generation.**

**What holds.** Every number in the document reproduces from a disjoint rebuild: the stable
population `1 / 2 / 4 / 6 / 8 / 10 = 2(n−1)`; `AC(P) = Π_n` on **all** of them (`203 of 203` at
`n = 6`); the members being **antichains and stars** exactly; chains **not** stable for `n ≥ 3` with
`|G(C_n)| = 2`, `|AC(C_n)| = 2^{n−1}` equal to the consecutive-interval partitions, and the **unique**
minimiser of `|AC|` at `n = 3,4,5,6`; the `|G(P)|` histogram at `n = 6` **entry for entry**
(`1×72, 2×123, 4×52, 6×12, 8×13, 12×24, 16×6, 24×2, 48×3, 72×1, 720×10`); `G(P) ⊋ D(P)` on **24 of
63** and **55 of 318**; `4231 → 1316` distinct quotient lattices with largest fibre **131**, which I
confirm is exactly the antichain plus **75** labelled down-stars plus **55** labelled up-stars;
join-failure on **7 of 16** and **49 of 63**; lattice-under-refinement on **all 86** classes; the
tri-equivalence with **0 disagreements on all 405 classes** at `n ≤ 6`; and `56` height-`≤ 2` classes
at `n = 6` against `10` stable, so the intermediate step is correctly reported as strictly weaker.
The `n = 7, 8, 9` claim survives on **my own** draws (0 disagreements) and on a positive test the
target's sweep does not contain (below, F5). **The L1 characterisation is faithful**: all three block
quotes are **verbatim** (checked programmatically against the source, after stripping quote markers
from both sides — the source's own N2 is itself inside a blockquote), every line-number citation
dereferences to what it claims, and §1.2's statement of N2's quantifiers, hypothesis and conclusion
is exactly what I get by re-deriving N2 from its definition. **Scope is clean on all four
prohibitions**: no citation appears in the document that the repository did not already carry, no
categorical formalism, `docs/roadmap.md` and `STATE.md` untouched by the commit, and nothing
developed about other set-represented categories.

**Two disagreements were made possible and neither fired.** I re-derived five numbers the existing
pipeline already carries — `|support lattice|` for the five named `n = 5` posets in
`code/hodge_leverage/lrb_output.txt`, computed there from the **left-regular-band product** and here
from **acyclicity** — and all five agree (`52, 16, 45, 37, 52`). I also re-derived
`theorems_output.txt` §N2's count (posets on which every shape-`α` face span *is* an `S_n`-submodule:
exactly **1** per `n ≤ 5`, the antichain). Worth recording: the sharpest of those five is
**`V+A_2` = `{0<1, 0<2}` with two isolated points — a star, not an antichain — whose
`|support lattice| = 52 = B_5 = |Π_5|`.** The repository has carried an instance of this document's
central positive claim, in committed output, since before mg-8fd1 existed.

**What breaks** is the proof of the document's own theorem, and the one sentence the document
nominates as the negative's bite.

| | finding | class |
|---|---|---|
| **F1** | **§2.4, Step 1 of the proof of (1)⇒(3):** *"If `x < u < y` then `{x,y}` + singletons has the 2-cycle … **while `{x,u}` + singletons is acyclic (every arrow leaves it)**."* The asserted acyclicity is **false**, and the reason given for it is false much more often. **235 counterexample triples** at `n ≤ 6` (1 at `n=4`, 17 at `n=5`, 217 at `n=6`); the smallest is the **4-chain** `0<1<2<3` with `x=0, u=2, y=3`, where `{0,2}\|{1}\|{3}` carries `{0,2} → {1}` (from `0<1`) and `{1} → {0,2}` (from `1<2`). The parenthetical *"every arrow leaves it"* fails on **752** triples — anything below `x` sends an arrow **into** the block. Ledger row **Q3** is labelled **PROVEN** for all `n` on this argument. **The theorem is TRUE** (0 disagreements on all 405 classes, and on my own beyond-range tests) and the repair is one clause — see below. | **BROKEN** |
| **F2** | **The sentence the document nominates as N2's bite drops the word *ambient*.** Line 22: *"the similarity to `S_n` cannot be an `S_n`-module structure, at any `n`, for any non-antichain"*; §1.3: reading it as *"the face space carries an `S_n`-module structure whose isotypic pieces do the work"* is *"**false for every non-antichain, proven, all `n`**"*; ledger row **Q2**, **PROVEN**. N2 proves that `span F_α(P)` is not an `S_n`-submodule **of `Ind_{S_α}^{S_n}1`** — a statement about the ambient action, as §1.3's own bullet list correctly says three paragraphs earlier. As written the claim is **wider than the source and false**: for the non-antichain `P = {0<1}` + 1 isolated at `n = 3` I exhibit an honest `S_3`-module structure on the chamber space that **commutes with `Δ_AT` exactly** (homomorphism checked on all 36 pairs in exact rationals), whose isotypic decomposition is a proper `1+2` block-diagonalisation — while N2 holds for that same poset at all three shapes. **This is this arc's signature defect, in the primary target, in the direction that kills a live line.** Repair: *"cannot be an `S_n`-module structure **inherited from the ambient action on ordered partitions**"*. | **MAJOR** |
| **F3** | **§2.6 claims a novelty the source already records, in the same sentence it quotes.** *"The source (§9.1) records that acyclic partitions are 'NOT closed under refinement' with this same witness; that they also fail the **join** appears to be unrecorded."* Source line 749–752, one sentence, both clauses: *"(Note that the acyclic partitions are not closed under refinement … So `L_P` is a lattice for the reverse-refinement order and the join is the common refinement, **not a sublattice of the partition lattice under refinement**.)"* Since `AC(P)` **is** closed under the `Π_n`-**meet** (common refinement — **0 failures on all 86 classes**, my computation, which is also ledger row **B2**), "not a sublattice under refinement" is *exactly* the join failure. The mathematics of §2.6 is right and reproduces (7/16, 49/63, and the named witness `03\|1\|2 ∨ 0\|12\|3 = 03\|12`); the attribution is wrong. Aggravating: the document uses *"join"* in the **opposite convention** to B2's *"join = common refinement"* without flagging the flip, so §2.6 reads as contradicting a PROVEN ledger row when it does not. | **MAJOR** |
| **F4** | **"Sublattice" where the theorem says "subset", which understates the theorem.** The answer line (26–29) and §2.5 say there is *"no poset … whose quotient lattice is a proper `S_n`-stable **sublattice** of `Π_n`"*. The theorem excludes any proper `S_n`-stable **subset**, which is strictly stronger — and §2.6 of the same document shows `AC(P)` is usually **not** a sublattice of `Π_n` at all, so as written the headline claim is about an empty-by-other-means category. Same wording in the commit message. | **MINOR** |
| **F5** | **The beyond-range sweep's positive direction is carried by near-empty posets.** §2.4: *"The random sweep exercises **both** directions rather than only the negative — 168/151/123 of the 400 came out stable."* With the document's own density menu (`0.02 … 0.5`), **≈ 90 % of the stable draws have at most one relation** (my draws: 160/174, 105/116, 63/70 at `n = 7/8/9`) — antichains and single edges, where stability is nearly vacuous. The interesting positive cases are the stars with `|S| ≥ 2`, and they are effectively absent. I supply them: **all `2(n−1)` predicted stable shapes at `n = 7, 8, 9`** have `AC = Π_n` (877 / 4140 / 21147 partitions each) and are stable, and three explicit non-star shapes are unstable as predicted. The claim survives; the evidence offered for it did not carry it. | **MINOR** |
| **F6** | **§3.2 makes a claim about a literature the ticket forbade surveying.** *"Any literature search framed around Young modules or isotypic decompositions of the face space **will return nothing usable**."* That is an unsupported prediction, and the document's own NOT-CLAIMED row disclaims knowledge of the literature. State it as an expectation, or drop it. (The rest of §3 is in scope: §3.4's *"premature rather than merely out of scope"* is scope-setting, which the ticket asked for, and introduces no new citation.) | **MINOR** |
| **F7** | **"WORLD ONE" is the document's own numbering, not the ticket's.** The ticket never numbers the two worlds. The commit **subject** leads with *"L2 is WORLD ONE"*, which is undecodable from the git log alone; the body and the document both gloss it correctly (*"WORLD ONE: one shape, many symmetry groups"*), so this is a label hazard, not an error. | **MINOR** |

---

## 1 — Target 1: fidelity of the L1 answer (the primary target)

**The quotations are exact.** `audit_quotes.py` extracts every block quote in the gate document,
strips markdown quote markers from **both** sides, and matches line by line: gate 43–52 → source
697–707 (Proposition N2), gate 57–63 → source 713–719 (the antichain half), gate 67–69 → source
721–723 (the interlacing residue). **No line differs.** Every line-number citation dereferences
correctly: §8 does begin at 691 and its prose does end at 723; ledger rows N2/N2′ are at 1019/1020;
the mg-86a3 rows are at 75, 475, 500, 501. The inline fragments — the N2 scope line, the auditor's
restatement, *"the Young-module dress adds nothing but costs nothing"*, *"proof checked line by
line"*, §9.4's corrected heading — are all present verbatim. There is no finding against N2 anywhere
in the mg-86a3 audit, as the document says.

I checked one thing the document does not raise, because this arc's history says to: **N2 does not
inherit mg-86a3's F2 conditional.** N2 appears at audit line 430 inside a *grouped* generalisation row
whose "holds fixed" column names **L1** — the reading of *"relative"* that makes `L^rel` well-posed —
and N2's conclusion does mention `L^rel`. But the conditional belongs to N1b, not to N2: N2's failure
happens at the level of the **decomposition of the face space**, before any operator is named, so
*"a fortiori cannot block-diagonalise `L^rel`, `L^abs` or `Δ_AT`"* holds under either reading of
"relative" and under no reading at all. The gate document's unconditional use of N2 is therefore
correct, and correct for a reason it does not state.

**The quantifiers in §1.2 are right, and I checked them by re-deriving N2 rather than by reading it.**
For every isomorphism class at `n ≤ 5` and every composition `α` with `≥ 2` parts I built the set of
`P`-compatible ordered partitions of shape `α` and tested it for `S_n`-invariance (the ambient module
has the ordered partitions as a permutation basis, so the span is a submodule iff the set is
invariant). The count of posets on which **every** shape's face set is invariant is **1 at each
`n = 2,3,4,5`, the antichain** — reproducing `theorems_output.txt` §N2 by a disjoint route. N2's
"never empty" half held on every case (a linear extension always exists), and its "proper" half held
on every non-antichain. So: universally quantified over all finite posets and all `α` with `≥ 2`
parts, the `n ≤ 5` sweep is a check and not the evidence, and §1.2 says so.

**"One route, not the leg" is the right answer.** N2's hypothesis is that `F_α(P)` is a nonempty
proper subset of a transitive `S_n`-set; its conclusion is about `Ind_{S_α}^{S_n}1`. Nothing in it
touches `Aut(P)`, any other group, or any algebra — and §9 of the same document supplies the live
mechanism whose index set is exactly Daniel's poset quotients. That reading is faithful, and the
document does not soften it: it states plainly that "very similar to `S_n`" cannot mean the ambient
`S_n`-module route, at any `n`, off the antichain, and that N2′ closes the antichain end too.

**Where it fails is the one sentence it flags as the bite — and it fails by widening.** See **F2**.
The demonstration is in `out_l1.txt`: the same non-antichain for which N2 holds at all three shapes
carries an `S_3`-module structure commuting with `Δ_AT`, whose isotypic pieces block-diagonalise it.
The widened sentence is therefore not merely unproven, it is false; the correctly quantified sentence
is proven, and the difference is one word. Both directions of the brief's test were run: I find **no
place where the negative is reported as narrower than it is** — the document states N2's bite at full
strength, states N2′ beside it, and does not use §9.4's `λ₂` limitation to soften either.

## 2 — Target 2: the population, the method, and the proof

`audit_l2.py`, from the definitions, with the enumeration certified against A000112/A001035:

| `n` | classes | stable | `2(n−1)` | `AC = Π_n` on all stable | chain `\|AC\|` | `\|G(C_n)\|` | min `\|AC\|` unique |
|---|---|---|---|---|---|---|---|
| 3 | 5 | 4 | 4 | yes (5/5) | 4 = 2² | 2 | chain |
| 4 | 16 | 6 | 6 | yes (15/15) | 8 = 2³ | 2 | chain |
| 5 | 63 | 8 | 8 | yes (52/52) | 16 = 2⁴ | 2 | chain |
| 6 | 318 | 10 | 10 | yes (203/203) | 32 = 2⁵ | 2 | chain |

The stable members are the antichain and the stars, listed individually in `out_l2.txt`, with
`n−1` down-stars and `n−2` up-stars as §2.2 says. The tri-equivalence *stable ⇔ `AC = Π_n` ⇔ every
two relations share an end ⇔ antichain-or-star* holds on **all 405 classes with 0 disagreements**,
and `AC(C_n)` is the set of consecutive-interval partitions on the nose.

**The isomorphism-class enumeration is correct, and the specific bug the brief names is absent.**
mg-8fd1's canonical form is `min` over **all of `S_n`** of the sorted relation list — a genuine
canonical form, not a `min()` over frozensets. My independent route (brute force over every relation
at `n ≤ 5`) produces the same class counts, and at `n = 6`, where brute force is unaffordable, the
natural-labelling enumeration is certified complete from outside by `Σ n!/|Aut(P)| = 130023`.

**"Stable" is distinguished from "stable up to the relabelling that induces it", and the two
coincide here.** The document defines `G(P) = {σ : σ·AC(P) = AC(P)}` and asserts the equivalent form
`{σ : AC(σP) = AC(P)}`. I verified the two sets are **equal on every class at `n ≤ 5`** (0
disagreements; the reason is the identity `AC(σP) = σ·AC(P)`), and that the **pointwise** stabiliser
is trivial for every class at `n ≥ 2` — so "stable" can only mean setwise, which is what is stated.
Testing stability on adjacent transpositions only (the `n ≥ 7` method) is legitimate because the
stabiliser of a subset is a subgroup; verified empirically as generator-vs-full-group agreement on
all 405 classes.

**The proof of the theorem does not establish it as written.** See **F1**. The repair, verified:
take the 3-chain **inside the covering relation**, `x ⋖ u ⋖ y`. Every poset with a 3-chain has one
(a saturated chain from `x` to `y` has length `≥ 2`, hence two consecutive covers; measured: **0**
posets with a 3-chain and no cover-3-chain at `n ≤ 6`), and for a covering pair there is nothing
strictly between `x` and `u`, so a cycle through `{x,u}` would need a path `x < … < u` (impossible by
the cover) or `u < … < x` (impossible by antisymmetry). Measured over all cover-3-chains at
`n ≤ 6`: **0 failures of either half** (`1 / 11 / 95 / 826` triples at `n = 3/4/5/6`). Step 2 of the
proof I checked by hand and it is sound as written: the four excluded return arrows each give a
3-chain, and paths through singletons do too.

## 3 — Targets 3 and 4: scope, and what was added beyond the brief

**All four prohibitions hold.** No citation in the gate document is new to the repository (Brown,
BHR, Diaconis, Saliola, Aldous, Caputo–Liggett–Richthammer, Young — every one already present, with
counts in `out_scope.txt`). No categorical formalism: the only category-theoretic words are
"isomorphism class" and the phrase *"graded category"* inside the quotation of Daniel's framing. The
commit touches five files, none of them `docs/roadmap.md` or `STATE.md`, and the pricing is not
restated. Nothing is developed about other set-represented categories; §3.4's judgement that they
are *"premature"* is scope-setting for the next ticket, which the ticket asked for.

**Beyond the brief:** the all-`n` theorem (§2.4), the two corrections to the ticket's own description
of chains (§2.3), the `G(P)`-as-new-invariant material (§2.5), and the join caveat (§2.6). **The
BROKEN item and one of the two MAJOR items are in that material** — F1 in the theorem's proof, F3 in
the caveat — which is the sixth consecutive generation in this arc to put its worst finding in
something it was not asked for. The rest of the added material is **true and reproduces**: the chain
corrections in full (including the uniqueness of the minimiser, which I confirm at every
`n = 3,4,5,6`), the `|G|` histogram entry for entry, `55/318` and `24/63`, and the fibre structure
`4231 → 1316` with the maximal fibre being exactly antichain-plus-labelled-stars.

## 4 — Target 5: is the two-worlds conclusion stated, and stated neutrally?

**Stated.** §2.5, the answer line, and the commit body all say *"one shape, many symmetry groups"*
and say why: `S_n`-stability holds **iff** the quotient lattice degenerates to `Π_n`, so the
non-degenerate home the ticket hoped for does not exist — as a theorem, not a coverage gap.

**Neutral, in both directions.** The document says explicitly and twice that this is *"not a
refutation of Daniel's idea"* but *"a change of its subject"*, which is what the ticket instructed;
and it does not overcorrect in the flattering direction either — §1.3's *"the two ends Daniel wants
to unify are already handled by one mechanism"* is immediately followed by the scope note that the
semigroup technique reaches `Δ_AT` only where `Δ_AT` is already free, so the positive is not sold
wider than it is. I find **no editorialising** and no place where a reader would take away either
"your idea is refuted" or "your idea is confirmed" when the truth is "reshaped". The only hazard is
the private numbering of the worlds (**F7**).

One neutral fact that belongs beside the conclusion and is missing: **the quotient lattice does not
remember the poset** is *why* `G(P)` exceeds `D(P)`, and the document says so — but the largest
fibre being precisely *antichain + all labelled stars* means the "many symmetry groups" world is
already visible in the fibre structure the pipeline had on disk (`V+A_2`, above). That strengthens
the conclusion; it does not change it.

## 5 — What I could not break

The population and every count in it; the theorem's **statement** at every `n ≤ 6` exhaustively and
at `n = 7,8,9` on independent draws and on the full predicted stable family; the chain corrections;
the `G(P)`-invariant material; the join failure and the refinement lattice; the verbatim quotations
and every line-number citation; §1.2's quantifiers, checked by re-deriving N2 itself; the two
disagreement opportunities against the existing pipeline (five LRB support-lattice sizes, and the
§N2 count), both of which agreed; the claim that the acyclicity test is independent of `lrb.py`
(`lrb.py` does use DFS three-colouring, as stated); and the scope, on all four prohibitions.

## 6 — Reproduce

```
cd code/unified_gate_audit_446b
./run_all.sh          # 2 min 0 s -> out_quotes.txt out_l1.txt out_l2.txt
                      #              out_crosscheck.txt out_proof.txt
                      #              out_beyond.txt out_scope.txt
```

## 7 — Findings ledger

| # | site | statement | class | repair |
|---|---|---|---|---|
| **F1** | §2.4 proof, Step 1; row Q3 | *"`{x,u}` + singletons is acyclic (every arrow leaves it)"* | **BROKEN** (235 witnesses, `n ≤ 6`) | take the 3-chain inside the covers; verified, 0 failures |
| **F2** | line 22, §1.3, row Q2 | *"cannot be an `S_n`-module structure … for any non-antichain"* | **MAJOR** (quantifier widened past the source; counterexample supplied) | add *"inherited from the ambient action on ordered partitions"* |
| **F3** | §2.6 | *"that they also fail the **join** appears to be unrecorded"* | **MAJOR** (source §9.1 records it in the sentence quoted) | attribute it; flag the convention flip against row B2 |
| **F4** | lines 26–29, §2.5, commit msg | *"proper `S_n`-stable **sublattice**"* | **MINOR** (understates its own theorem) | "subset" |
| **F5** | §2.4 evidence paragraph | *"exercises both directions"* | **MINOR** (≈ 90 % of stable draws have ≤ 1 relation) | test the stars with `\|S\| ≥ 2`; done here at `n = 7,8,9` |
| **F6** | §3.2 | *"will return nothing usable"* | **MINOR** (claim about an unsurveyed literature) | mark as expectation |
| **F7** | commit subject, §2.5 | *"WORLD ONE"* | **MINOR** (private numbering) | gloss it wherever it leads |

**Not claimed by this audit.** Whether the LRB/support-lattice family is the right home for the
unification; anything about the literature; anything about `λ₂`, `Δ_AT` or the pricing; whether
`G(P)` is a known invariant; and anything about other set-represented categories. The theorem's
statement is verified exhaustively to `n = 6` and tested at `n = 7,8,9`; **its proof I repair for
Step 1 only** — Steps 2 and (3)⇒(2) and (3)⇔(4) I checked and found sound, and I have not attempted
an independent proof of the whole equivalence.
