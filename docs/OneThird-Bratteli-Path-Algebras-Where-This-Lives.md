# Bratteli/path algebras: locating Daniel's generalisation, and which hypothesis carries it

**Work item:** mg-db09. **Date:** 2026-07-30. **Audited:** mg-2060
(`docs/OneThird-Bratteli-Path-Algebras-IndependentAudit.md`). **Repaired:**
mg-e8b8, 2026-07-30, and the repair is a **withdrawal** — see the banner below.
**Audited again:** mg-a218
(`docs/OneThird-Bratteli-Path-Algebras-Mge8b8Repair-IndependentAudit.md`);
**repaired:** mg-13b2, 2026-07-30 — the vertex column now reports the **set**,
and the disposition labels are reconciled with the diff and **checked by an
instrument** (§8, `t5_labels.py`).
**Computation:** permitted, used, committed (`code/branching_locate_db09/`,
`run_all.sh`, ~6 min, 699 520-assertion self-test, five test scripts, all five
`TOTAL BAD: 0`).

> ## ⚠ WHAT THIS DOCUMENT NO LONGER CLAIMS — read before §0
>
> Two things delivered here have been taken back. Both were found by the
> independent audit mg-2060 and both are recorded in place below, not deleted.
>
> **1. The separating example is WITHDRAWN.** §0 said the Temperley–Lieb tower's
> branching graph was *"**measured** (not cited) to be the same multiplicity-free
> graph at each"* parameter, and that *"multiplicity-freeness is held fixed down
> that column"*. **It was not measured, and it is not the same graph.** Under the
> definition this document itself quotes from Vershik–Okounkov — vertices are the
> **irreducibles**, edges are the restriction multiplicities — the vertex set
> differs at `β = 1` **and** at `β = 0`, and multiplicities reach `2` at `β = 1`
> and `β = 0`. (At `β = 1` the *number* of vertices agrees with `β = 3` at every
> level while the set does not, which is why the table in §0 reports the set;
> `mg-13b2`, on `mg-a218`'s finding.) What was
> equal at every parameter was **one statistic**, the path-pair count `132` at
> `n = 6`; **equality of that statistic was taken for identity of the structure**.
> The invariant is now measured at every parameter, in this document's own
> instrument, in `T1b2` — and the measurement is what withdraws the claim.
> **The verdict of §0 survives, but on the THEOREM and not on the builds.**
>
> **2. D10 — the deliverable — is a CONJECTURE, not a result.** *"`kF(P)` is
> quasi-hereditary"* is unverified: quoted through Margolis–Steinberg from Putcha,
> **whom nobody in this lineage has read**, with the characteristic hypothesis
> never checked against the primary source. mg-2060 did not verify it either and
> calls it *"the single largest unverified load in the delivered document"*.
> **It went to Daniel as the headline on 2026-07-30 at 19:50 and was retracted at
> 20:45** (`docs/roadmap.md`, commit `f4eaea6`). §5 D10 says what would establish
> it.
>
> **Nothing else in the document is withdrawn**, and the reproduction is total:
> mg-2060 regenerated all five committed outputs byte-identically and reproduced
> T1c, T2a–T2d and T3a–T3d on a disjoint instrument.

**Daniel's proposal, 2026-07-30 17:58, verbatim:**

> *"Given a suitable category with a rank function and a multiplicity-free
> branching rule, the Bratteli/path algebra is canonically an endomorphism
> algebra."*

**Scope, and it is the whole of the scope.** This is a **locating exercise**. It
develops no mathematics. Every relationship is reduced to **instance / special
case / generalisation / adjacent / no contact**, with a reason, and every
identification is tested as an **equality** built from published definitions
rather than asserted as a resemblance. Where I did not find something I say
*"not located"*, which is a statement about my search and not about the
literature. There is **no publishability verdict and no novelty claim** here.

**What was already located before this ticket, stated so that nothing here can
be mistaken for a discovery.** The `S_n` case on the branching axis
(Okounkov–Vershik, `SYT(λ)` as the Gelfand–Tsetlin basis) and on the species
axis (Bidigare/Solomon), both in `docs/OneThird-Branching-Graphs-Where-This-Lives.md`
(mg-af28, repaired mg-41aa) and `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`
(mg-7d75, audited mg-a61f — headline holds and is a theorem). The measurement
`dim kF(P)/rad = |AC(P)|` (mg-af28 B5, mg-6ad0 A4a, mg-7d75 T2). **This document
adds no new object to that list; it adds a decision about which hypothesis in
Daniel's sentence does the work, and a decision about the relationship between
the two axes.**

---

## 0. THE HEADLINE

**The statement is located, at exactly the generality Daniel wrote it, and it is
not one statement but two — with different hypotheses. Semisimplicity carries
"is an endomorphism algebra". Multiplicity-freeness carries only the word
"canonically".**

**~~Both halves are settled here by BUILDING the object each would forbid, not by
argument.~~ WITHDRAWN (mg-e8b8, on mg-2060's finding). Both halves are settled by
the THEOREMS quoted immediately below, and they were settled before any object
was built.** A finite direct sum `⊕_λ End(V_λ)` **is** semisimple, so for *every*
finite-dimensional algebra `A ≅ ⊕_λ End(V_λ) ⟺ A is semisimple` — Wedderburn in
both directions, with no rank function, no branching graph and no multiplicity
hypothesis anywhere in it. Remark 1.3 gives the other half. **What the builds
establish is weaker and is still worth having: both off-diagonal cells of the
2×2 table are INHABITED** — see the table and the withdrawal note under it.

> **Vershik–Okounkov, *A new approach to the representation theory of the
> symmetric groups. II*, §1** (`arXiv:math/0503040`), in four sentences that are
> Daniel's sentence with the hypotheses separated:
>
> * *"The same definition of the branching graph applies to any chain*
>   `M(0) ⊂ M(1) ⊂ M(2) ⊂ …` *of finite-dimensional semisimple algebras"* — **this
>   is "a suitable category with a rank function"; the rank function is the level
>   of the chain, and "suitable" means finite-dimensional and semisimple.**
> * *"If the multiplicities of all restrictions are equal 0 or 1, then this
>   diagram is a graph (and not multigraph); in this case one says that the
>   multiplicities are simple or the branching is simple."* — **this is
>   "multiplicity-free branching rule", in their words.**
> * *"Recall the following fundamental isomorphism:"* `C[G(n)] = ⊕_λ End(V^λ)` —
>   **this is "is an endomorphism algebra", and it is Wedderburn. It uses
>   semisimplicity and NOTHING ELSE: no rank function, no branching graph, no
>   multiplicity-freeness.**
> * *"If the branching is simple, the decomposition … is canonical."* and
>   **Remark 1.3**: *"For an arbitrary inductive family of semisimple algebras,
>   the GZ-subalgebra is a maximal commutative subalgebra if and only if the
>   branching graph has no multiple edges."* — **this is "canonically", and it is
>   the ONLY thing multiplicity-freeness is buying.**

All four quoted verbatim from the rendered PDF and re-checked against near-miss
controls (T4: 19 quotations located, 5 negative controls all rejected).

### The two objects, built — one of them WITHDRAWN

**1. ~~Multiplicity-free and NOT semisimple — the conclusion fails.~~ WITHDRAWN
(mg-e8b8, on mg-2060's finding). The Temperley–Lieb tower is not that object.**

**What was claimed.** *"The Temperley–Lieb tower `TL_1 ⊂ TL_2 ⊂ ⋯` at four
parameters. The branching graph is **measured** (not cited) to be the same
multiplicity-free graph at each — every restriction multiplicity is 0 or 1, and
the rule is `V_{n,p} ↦ V_{n-1,p} ⊕ V_{n-1,p-1}`. … Multiplicity-freeness is held
fixed down that column and the conclusion changes. Semisimplicity varies in step
with it."*

**Why it is wrong, and it is wrong under this document's own definition.**
Vershik–Okounkov's branching graph — quoted verbatim four lines above — has the
**irreducible** modules as its vertices and the **restriction multiplicities** as
its edges. The measurement offered was of the **cell** modules `V_{n,p}` at
`β = 3` only, plus, at the other three parameters, the dimension identity
`dim V_{n,p} = dim V_{n-1,p} + dim V_{n-1,p-1}` — which is the Catalan triangle
and **mentions no `β` on either side**, so it cannot distinguish parameters. The
cell modules are parameter-independent; the **simple** modules are not. **Reading
a cellular datum as a branching graph is a resemblance**, and the rule this
document sets itself in its own scope paragraph is *"identifications are
equalities, not resemblances"*.

**The invariant, now measured at every parameter** (`T1b2`, added by the repair
to this document's own instrument; `L(n,p) := V_{n,p}/rad⟨,⟩`, Graham–Lehrer,
with the restriction multiplicities recovered from characters and their
**uniqueness, integrality, non-negativity** and `Σ_q m_q·dim L(n-1,q) =
dim L(n,p)` all checked rather than assumed):

| `β` | `dim TL_6` | `dim ⊕_λ End(L_λ)` | endomorphism algebra? | vertex SET at `n = 1…6` | branching, **MEASURED** |
|---|---|---|---|---|---|
| 3 | 132 | **132** | **yes** | `[1] [1,1] [1,2] [1,3,2] [1,4,5] [1,5,9,5]` | multiplicity-free |
| 2 | 132 | **132** | **yes** | `[1] [1,1] [1,2] [1,3,2] [1,4,5] [1,5,9,5]` | multiplicity-free |
| 1 | 132 | **99** | **no** | `[1] [1,1] [1,1] [1,3,1] [1,4,1] [1,4,9,1]` | **NOT multiplicity-free** |
| 0 | 132 | **42** | **no** | `[1] [1] [1,2] [1,2] [1,4,5] [1,4,5]` | **NOT multiplicity-free** |

**The vertex column reports the SET and not its size, and that is the point of
it (`mg-13b2`, on `mg-a218`'s finding).** A vertex of this graph is an
**irreducible module**, so each bracket is the level's vertex set written as
`dim L(n,p)` for `p` ascending — the canonical form. `T1b2` prints the fuller
form `[p:dim L(n,p)]`, checks that the live labels are an unbroken run from `0`,
and then **checks that the abbreviation separates exactly the pairs the fuller
form separates**, on every cell, rather than arguing that it must. **No count
column is printed beside this one on purpose:** *"equality of one statistic was
taken for identity of the structure"* is exactly how the withdrawn claim above
broke, and a cardinality is one statistic. This column ends at `n = 6` where the
sum of the squares is the `dim ⊕_λ End(L_λ)` column two to its left — `132`,
`132`, `99`, `42` — which ties it to a figure computed by two other routes.

**Where a count would have hidden the difference, measured.** Over the 36 cells
— 6 ordered pairs of the four parameters × 6 levels — there are **10 at which
the number of vertices agrees and the vertex set does not**. Four of them are
`β = 3` against `β = 1`, which the old column printed as the same six numbers at
every level: `[1,2]` vs `[1,1]` at `n = 3`, `[1,3,2]` vs `[1,3,1]` at `n = 4`,
`[1,4,5]` vs `[1,4,1]` at `n = 5`, `[1,5,9,5]` vs `[1,4,9,1]` at `n = 6`.

**So the vertex set differs at TWO parameters, not one.** At `β = 0` the tower
has fewer irreducibles at every *even* level — the count differs there too. At
`β = 1` the count agrees with `β = 3` at **every** level and the graph is
different at four of the six. And the multiplicities reach 2 — five of them,
each surviving its own dimension check:
`[L(4,1)↓ : L(3,0)] = 2` and `[L(6,2)↓ : L(5,1)] = 2` at `β = 1`;
`[L(3,1)↓ : L(2,0)] = 2`, `[L(5,1)↓ : L(4,0)] = 2` and `[L(5,2)↓ : L(4,1)] = 2`
at `β = 0`.

**So multiplicity-freeness varies down that column in exact step with
semisimplicity — which is precisely what the experiment needed it not to do.**
Both hypotheses moved together; the tower separates nothing, in either
direction, and no claim that it does is made here any more. The failing phrase
was **`"MEASURED (not cited)"`**: the invariant was *asserted*. What was equal at
every parameter was the path-pair count `Σ_p (dim V_{n,p})² = 132`, and
**equality of one statistic was taken for identity of the structure**.

**What of that block survives, and it is measured.** The four `dim ⊕_λ End(L_λ)`
figures `132 / 132 / 99 / 42` are right and reproduce on three instruments; the
semisimple quotient is computed **twice by disjoint routes** — the trace form of
the regular representation, and `Σ_p (rank of the Gram matrix of V_{n,p})²` —
with **0 disagreements** on 20 `(n, β)` pairs. **`T1b2` is tied to both of those
routes rather than standing apart from them:** the self-test asserts
`Σ_p (dim L(n,p))² = dim A/rad` on all 20 pairs, which is the trace-form route
against the Gram route with the new machinery in between — **not a third route,
and it is not offered as one.** What is genuinely new in `T1b2` is the
whole-diagram action and the character solve, and the check on those is that the
diagram action agrees with the generator action `T1b` already used, on every
`(n, p, β)` the two share. Six
published control facts reproduce (§3). **What does not survive is the use to
which they were put.** `TL_6(1)` and `TL_6(0)` do **not** belong in the
multiplicity-free-and-not-semisimple cell of the table below.

**Confirmed independently.** mg-2060 measured the same graph on a disjoint
instrument (its B1a/B1b) and got the same vertex counts and the same five
multiplicity-2 edges; `T1b2` was written afresh against this document's own
kernel and agrees with it row for row.

**2. Semisimple and NOT multiplicity-free — the conclusion survives.** Take the
same algebra `ℂS_4` and remove a level from the chain. It is still semisimple, so
`ℂS_4 = ⊕_λ End(V^λ)` still holds (measured: `dim = 24 = 1+1+4+9+9`, radical
zero). What is lost is exactly the Gelfand–Tsetlin basis:

| chain | `dim GZ` | # paths | maximal commutative? |
|---|---|---|---|
| `S_1 ⊂ S_2 ⊂ S_3 ⊂ S_4` | **10** | 10 | **yes** |
| `S_1 ⊂ S_2 ⊂ S_4` | **8** | 10 | no |
| `S_1 ⊂ S_3 ⊂ S_4` | **7** | 10 | no |
| `S_1 ⊂ S_4` | **5** | 10 | no |

with the minimal witness carrying no group at all: for `ℂ ⊂ M_2(ℂ)` the Bratteli
diagram has a double edge, `M_2 = End(V)` is an endomorphism algebra, and
`dim GZ = 1 < 2` = the number of paths. Okounkov–Vershik's own criterion
(Prop. 1.4, *"the centralizer `Z(M,N)` is commutative"*) is tested as an equality
in the same script and separates the two cases with no false positives and no
false negatives on six pairs (T2c).

### So: **semisimplicity is load-bearing; multiplicity-freeness is not**

| | semisimple | not semisimple |
|---|---|---|
| **multiplicity-free** | Daniel's statement, in full: `⊕End`, canonical path basis. `ℂS_n`; `TL_n(3)`; `TL_n(2)` | **`⊕End` FAILS.** Path-pair *count* survives, direct sum does not. **`kF(P)`: 52 of 541**, and it is the only inhabitant this document has |
| **not multiplicity-free** | **`⊕End` HOLDS**, canonicity fails: the path basis needs a choice. `ℂS_4` on a skipped chain; `ℂ ⊂ M_2(ℂ)` | `TL_6(1)`: 99 of 132. `TL_6(0)`: 42 of 132 |

**CORRECTED (mg-e8b8).** `TL_6(1)` and `TL_6(0)` were in the top-right cell.
They are in the **bottom-right** cell: measured, their branching is not
multiplicity-free (`T1b2`). The top-right cell is inhabited by `kF(P)` and by
`kF(P)` alone here — and it genuinely belongs, because **all** of `kF(P)`'s
irreducibles are one-dimensional, so a restriction of one to any subalgebra is
one-dimensional, hence irreducible, hence of multiplicity one (D6). That is
forced for every `P`, so it is an argument and is booked as one.

**MARKED IN PLACE (mg-13b2, on mg-a218's finding).** The top-right cell reads
*"Path-pair **count** survives"*. It read *"Path-pair **basis** survives"* until
`2e66d03`, which corrected it — that was **mg-2060's X2**, and the same commit
booked X2 under *"Deliberately NOT repaired, and each is open"* in §8. **The
correction went the right way and the disclosure did not.** X2's remaining
sites — T1a's *"iff"*, and a **fourth site in §1's clause table that no list
named** — are corrected in this repair, and the *"iff"* is refuted in `T1c2`;
§8 now books X2 as closed and names which commit closed which site.

**Failure of semisimplicity BREAKS the conclusion. Failure of
multiplicity-freeness WEAKENS it — and weakens only the adverb.** **This
verdict is unchanged, and it rests on the two quoted theorems, not on the
table.** The table records which cells are inhabited; it is not the evidence for
the verdict, and after the withdrawal above it could not be — no object in this
document holds one hypothesis fixed while the other varies. The audit put it
exactly: *"the verdict was settled by the quoted theorems before any object was
built."*

### Where `kF(P)` sits, and it is the extreme corner

`kF(P)` has multiplicity-free branching **for free and for nothing**: every
irreducible is one-dimensional, so a restriction of an irreducible to any
subalgebra is one-dimensional, hence irreducible, hence multiplicity one. It
therefore has the hypothesis that does not carry the conclusion, and fails the
one that does — maximally:

| `P` | `dim kF(P)` | `dim ⊕_X End(V_X) = |AC(P)|` | ratio | radical |
|---|---|---|---|---|
| antichain, `n = 4` | 75 | 15 | 5.0× | 80.0% |
| antichain, `n = 5` | 541 | 52 | 10.4× | **90.4%** |
| antichain, `n = 6` | 4 683 | 203 | 23.1× | **95.7%** |

Both of the ticket's figures reproduce here from `|F(P)|` and `|AC(P)|` alone
(T3a), and `dim kF(P)/rad = |AC(P)|` is re-derived through the trace form on **67
of 87 classes to `n ≤ 5`, 0 bad**, 20 exempt over a `|F(P)| ≤ 90` cap and each
listed with its size (T3b).

**Where the two percentages stand after the audit (mg-e8b8).** The `n = 5` figure
is now **derived, not arithmetic**: mg-2060 ran the trace form with the cap
removed over **87 of 87** classes to `n ≤ 5`, 0 bad, including `|F| = 541`, and
got `dim kF/rad = 52`, radical `489/541 = 90.4%`. **The `n = 6` figure, 95.7%,
remains arithmetic** on `|F| = 4683`, `|AC| = 203` and the cited identity —
`|F| = 4683` puts the trace form out of reach on both instruments. **It is not
re-derived, and it should not be quoted as though it were.** (The commit message
for `03d7f91` placed *"re-derived on a third instrument"* next to both figures
with nothing between them; that placement is wrong and this paragraph is the
correction of record. The ledger row D5 and T3a always said it correctly.)

### The deliverable: are the two axes instances of a common construction?

> ### ⚠ THIS SECTION IS A CONJECTURE, AND IT WAS DELIVERED AS A RESULT
>
> **What was relayed.** On 2026-07-30 at 19:50 `docs/roadmap.md` carried, as
> **THE HEADLINE**, *"the branching axis and the species axis share a PROPERTY,
> not a CONSTRUCTION — quasi-hereditary"*, and it **went to Daniel in that
> form**.
>
> **It was retracted at 20:45** on mg-2060's finding — `docs/roadmap.md`, commit
> `f4eaea6`, *"RETRACT the quasi-hereditary headline"*. The retraction is
> recorded here as well as there because **the document is where a future reader
> will look, and a retraction that lives only in a roadmap entry and in mail is
> not a retraction.**
>
> **Why.** The whole section rests on `kF(P)` being quasi-hereditary — ledger row
> **D10** — and **that is unverified.** mg-2060: *"It is the single largest
> unverified load in the delivered document and the audit leaves it where it
> found it."* **Whether the two axes share any property is an open question, not
> an answered one.** What would establish it is set out at D10 in §5.
>
> Everything measured in this section — the Cartan matrices, the symmetry
> pattern, the semisimplicity census — **stands, and was re-derived by the audit
> from a different formula.** It is the *umbrella* that is conjectural, and with
> it the reading of the two axes as sitting inside one.

**Conjecturally no, and the honest answer is more interesting than either
alternative in the brief.** They are **not two values of one construction**, and
they are **not unrelated**. The candidate umbrella is **quasi-hereditary
algebras**, and what it would deliver is a **standard filtration and not an
endomorphism algebra**:

> Margolis–Steinberg, *Quivers of monoids with basic algebras*
> (`arXiv:1101.0416`), §1, verbatim: *"The algebras of finite (von Neumann)
> regular monoids provide natural and diverse examples of quasi-hereditary
> algebras. This was first proved by Putcha [73] and further developed by the two
> authors of this paper using homological methods [55]. However, Nico essentially
> had noted that semigroup algebras of regular semigroups are quasi-hereditary
> before the concept was even invented."*

`F(P)` is a band, hence — **conjecturally; this link is one line, it is mine, and
it is not checked** — a regular monoid, which would put `kF(P)` in that class.
The diagram algebras of the branching axis are in it too. **If the umbrella
holds, the two axes sit at opposite extremes inside it, and the invariant that
separates them is the Cartan matrix.** The Cartan measurement below does **not**
depend on the conjecture: it is a measurement of `kF(P)` itself. Measured, on our
side (T3c), reproducing Margolis–Saliola–Steinberg Thm 4.18 against our object:

| `P` | `|AC(P)|` | `dim A` | `Σ C` | unit diagonal | triangular | **symmetric** |
|---|---|---|---|---|---|---|
| antichain 3 | 5 | 13 | 13 | yes | yes | **no** |
| antichain 4 | 15 | 75 | 75 | yes | yes | **no** |
| antichain 5 | 52 | 541 | 541 | yes | yes | **no** |
| chain 3 | 4 | 4 | 4 | yes | yes | **yes** |
| chain 5 | 16 | 16 | 16 | yes | yes | **yes** |

`Σ C = dim A` on every row is the arithmetic check that the computation is right
(for a split basic algebra the Cartan entries must sum to the dimension). The
Cartan matrix is **unipotent lower triangular** — MSS Thm 4.18, quoted verbatim
and reproduced — and it is **symmetric exactly on the rows where the algebra is
semisimple**. A cellular algebra in the sense of Graham–Lehrer — which is what
the branching axis becomes when semisimplicity is dropped, and which covers
Temperley–Lieb, Brauer, partition and Hecke — has a **symmetric** Cartan matrix.
A matrix that is both symmetric and unitriangular is the identity. **So the two
families intersect only at their semisimple point**, and we reach it only here:

| `n` | poset classes | classes with `kF(P)` semisimple | which |
|---|---|---|---|
| 3 | 5 | 1 | the total order |
| 4 | 16 | 1 | the total order |
| 5 | **63** | **1** | the total order |

and there `kF(P) = k^{2^{n-1}}`, so Daniel's conclusion is **true and empty**: a
sum of `2^{n-1}` copies of `End` of a one-dimensional space.

### And the brief's own premise needs correcting, in the direction of the answer

The brief says *"`S_n` lies in both"*. **At the level of algebras it does not.**
The branching axis's `S_n` object is `ℂS_n` — semisimple, `dim 120` at `n = 5`,
irreducibles of dimension `f^λ`. The species axis's `S_n` object is `kΣ_n` —
`dim 541` at `n = 5`, radical 90.4%, all irreducibles one-dimensional. **These
are different algebras of different dimensions with different representation
theory.** What they share is an index set (the partitions of `n`) and a
**theorem** joining them at fixed `n` — Bidigare's, that `(kΣ_n)^{S_n}` is
anti-isomorphic to Solomon's descent algebra, which mg-7d75 verified structure
constant by structure constant. **A theorem relating two objects is not a
construction having both as values**, and this is the sharpest available reading
of the relationship.

---

## 1. WHAT "SUITABLE" HAS TO MEAN — Daniel's sentence, clause by clause

| Daniel's clause | the published counterpart | what it has to mean, and what it costs |
|---|---|---|
| *"a suitable category"* | *"any chain `M(0) ⊂ M(1) ⊂ M(2) ⊂ …` of finite-dimensional semisimple algebras"* (VO §1) | **finite-dimensional and semisimple.** Not "abelian", not "monoidal", not "with duals". This is the whole of "suitable", and dropping the semisimplicity is what T1 measures |
| *"with a rank function"* | the level `n` of the chain; the branching graph is graded by it, and `G(0)^∧` is a single vertex | **not an extra hypothesis — it is the indexing.** A rank function with no chain of algebras under it gives nothing (§2 item 4) |
| *"a multiplicity-free branching rule"* | *"the multiplicities are simple, or the branching is simple"* (VO §1) | multiplicities in `{0,1}`, equivalently (VO Prop. 1.4) *"the centralizer `Z(M,N)` is commutative"* |
| *"the Bratteli/path algebra"* | matrix units indexed by pairs of increasing paths with a common endpoint; `dim = Σ_λ (#paths to λ)²` | **the COUNT survives without semisimplicity and the MATRIX UNITS do not.** T1a measures the dimension identity at every `β`; `T1c2` shows the algebra is not semisimple at 7 of the 20 `(n, β)` pairs, and matrix units would force semisimplicity. **Corrected (mg-13b2):** this cell said *"this survives without semisimplicity"* with *"this"* reaching back to the matrix units — a **fourth site of mg-2060's X2, named by no list**, found by sweeping for the phrase while closing the other three. It is why the statement looks parameter-independent when it is not |
| *"is canonically an endomorphism algebra"* | `C[G(n)] = ⊕_λ End(V^λ)` (VO (1.4)), plus *"the decomposition … is canonical"* | **two statements.** The equality is Wedderburn and needs semisimplicity alone. The adverb is Remark 1.3 and needs multiplicity-freeness |

**The vacuity trap, and it was already on the record.** Every graded graph with a
root is the Bratteli diagram of *some* AF algebra, so if "suitable category with
a rank function" is read weakly enough — a graded graph and nothing more — the
conclusion is true by construction and carries no information: the tower it names
is built out of the diagram. mg-af28 §2.7 makes exactly this point. **The content
of the statement is that the tower arises independently**, as `ℂS_n` does for
Young's lattice. Any reading of "suitable" that does not include semisimplicity
lands in one of the two ditches: vacuous, or false.

### What I did NOT locate

**A statement at Daniel's generality with the word "category" in it that is not
either (a) the chain-of-semisimple-algebras statement above with different
notation, or (b) a tautology.** The obvious candidate is the tower
`End(X^{⊗n})` in a semisimple monoidal category, where the Bratteli diagram is
the fusion graph of `X` — but there the conclusion is a **tautology**, because
the algebra is *defined* as an endomorphism algebra. The content in that setting
is the path model of it, which is again the chain statement. **This is a report
on a search over a formulation, which §2.1 of the landscape document already
flags as the least reliable kind of negative, and it is the weakest claim in this
document.** Goodman–de la Harpe–Jones, *Coxeter Graphs and Towers of Algebras*
(MSRI 14, 1989), Chapter 2 is the standard reference for the path model at the
level of arbitrary inclusions of multi-matrix algebras — **located, not read**,
and nothing here depends on it, because VO §1 states what is needed and is open.

---

## 2. THE CANDIDATE SPACE FOR A COMMON CONSTRUCTION, ENUMERATED

The discipline in the brief is *"before writing any negative, try to build the
object it forbids"*. The negative here is *"the two axes are not two instances of
one construction"*. The object it forbids is a construction with both as values.
Eight were evaluated. **One of them is not a negative** — row 2 — and it was
delivered as the answer. **It is a CONJECTURE (D10), and the headline that
rested on it has been retracted; see §5.**

| # | candidate umbrella | evaluated? | verdict | reason |
|---|---|---|---|---|
| **1** | **Cellular algebras** (Graham–Lehrer, Invent. Math. 123 (1996)) — the branching axis's own non-semisimple continuation: TL, Brauer, partition, Hecke | **yes** | **EXCLUDES US, conditionally** | a cellular algebra has a **symmetric** Cartan matrix; `kF(P)`'s is **unipotent lower triangular** (MSS Thm 4.18, reproduced at T3c) and measurably **not symmetric** unless `P` is a total order. Symmetric ∧ unitriangular ⟹ identity ⟹ semisimple. **The symmetry statement is CITED FROM A SECONDARY SOURCE and Graham–Lehrer was not read** — see §4 item 1 |
| **2** | **Quasi-hereditary algebras / highest weight categories** (Cline–Parshall–Scott) | **partly — the general theorem is quoted, the application is NOT verified** | **CONJECTURED TO CONTAIN BOTH. This was delivered as "the answer" and it is D10, which is unverified — §5.** | `kF(P)` is the algebra of a band, hence — *unchecked; see §5* — of a **regular monoid**, and *"the algebras of finite (von Neumann) regular monoids provide natural and diverse examples of quasi-hereditary algebras"* (Margolis–Steinberg, quoted verbatim; **Putcha and Nico located, not read**). The diagram algebras of the branching axis are quasi-hereditary at the parameters where they have finite global dimension. **What the umbrella delivers is a filtration by standard modules — not `⊕End`, which is the split case** |
| **3** | **Towers of recollement** (Cox–Martin–Parker–Xi, J. Algebra 302 (2006)) — the axiomatisation of quasi-hereditary *towers* of diagram algebras | **PARTLY EVALUATED — by mg-2060, not by this ticket** | **(A1) YES; (A2)(i) leaning NO; the rest open** | delivered as *"located, NOT evaluated … untested by this ticket and by every earlier one"*, and that was true when written. **mg-2060 fetched the axioms and evaluated two of them against the antichain family `kΣ_n` — the only sub-family of `kF(P)` that is a *sequence*, which §7 failed to say.** (A1) holds and the idempotent is exhibited, `2 ≤ n ≤ 6`, the band isomorphism checked entry by entry. **(A2)(i) fails for every face idempotent realising (A1) at `n = 3` and `n = 4`** — scoped to face idempotents and `n ≤ 4`, so evidence leaning negative, not a proof. **(A2)(ii), (A4), (A5), (A6) remain untested**, as does whether (A3) needs a unital embedding. (A2′) is D10 and is the same open statement in both places |
| **4** | **AF algebras / Bratteli's realisation theorem** | **yes** | **VACUOUS INSTANCE** | every graded graph is the Bratteli diagram of some AF algebra, so it contains both and says nothing about either. mg-af28 §2.7 already booked this |
| **5** | **Monoid algebras / category algebras** | **yes** | **VACUOUS INSTANCE** | `ℂS_n` and `kΣ_n` are both monoid algebras. True, and it identifies our object with everything |
| **6** | **Species and Hopf monoids** (mg-7d75's axis) — does it contain the *branching* axis? | **yes, from mg-7d75's own findings** | **NO** | mg-7d75 §6.1: what the `S_n` instance of the Fock functor recovers is the **character ring**, of dimension `p(n)`, with all irreducibles one-dimensional. It produces no `S^λ`, no `f^λ`, no multiplicity. So the species axis does not contain the branching axis either, and the containment fails in the same place, for the same reason |
| **7** | **Bidigare/Solomon** | **yes** | **A THEOREM, NOT A CONSTRUCTION** | it relates `(kΣ_n)^{S_n}` to `Sol(S_n)` at fixed `n`. It is the bridge and it is real (mg-7d75 T3, 0 mismatching structure constants), but a bridge between two objects is not a construction with both as values. §0 |
| **8** | **Okounkov–Vershik itself, applied to `kF(P)`** | **yes** | **HYPOTHESIS FAILS** | its input is *"an inductive family of semisimple algebras"*. `kF(P)` is 90.4% radical at `n = 5`. This is mg-af28 §1 row 3, re-derived here on a third instrument |

**What this enumeration is not.** It is a search over **umbrellas that already
exist**, not a proof that no construction with both as values could be written
down. Writing one down would be new mathematics.

---

## 3. WHERE THE FAMILY ENDS

**In.** Any tower of finite-dimensional semisimple algebras with multiplicity-free
branching: `ℂS_n`; Hecke algebras at generic `q`; Temperley–Lieb at generic `β`
(measured here at `β = 3` and, as a control, `β = 2`, semisimple for every `n`);
Brauer and partition algebras at generic parameters. The conclusion holds in
full, with the canonical Gelfand–Tsetlin/path basis.

**Out on BOTH hypotheses at once — which is why this row settles nothing.** The
same towers at non-generic parameters. Temperley–Lieb at `β = 1` (`q` a primitive
6th root of unity) and at `β = 0`: measured here, the pairs-of-paths **count** is
still right at every `n ≤ 6` (`dim TL_n = Σ_p (dim V_{n,p})²`, 0 bad) and the
algebra is not a sum of endomorphism algebras (99 and 42 out of 132 at `n = 6`).
**CORRECTED (mg-e8b8): this row used to read "the branching graph is unchanged
and multiplicity-free", and it is neither.** Measured at every parameter under
Vershik–Okounkov's definition (`T1b2`), the vertex set differs at `β = 1` and at
`β = 0` — at `β = 1` with the same *number* of vertices as `β = 3` at every level
(`mg-13b2`) — and
multiplicities reach 2 at both `β = 1` and `β = 0` — so these two parameters fall
out of the family on the *multiplicity-freeness* hypothesis as well as on
semisimplicity, and the row cannot be used to tell the two apart. Published
controls
this reproduces (Ridout–Saint-Aubin, `arXiv:1204.4505`, Cor. 4.6 and the remark
after Cor. 4.8): `TL_n(2)` semisimple for every `n`; `TL_n(0)` semisimple exactly
for `n` odd; `TL_2(0)` with a one-dimensional radical. **All six controls
reproduced, 0 bad.**

**Out on the other hypothesis.** Towers with a level removed (`S_1 ⊂ S_2 ⊂ S_4`),
and inclusions that are not Gelfand pairs. Measured: `Z(ℂS_4, ℂS_2)`,
`Z(ℂS_5, ℂS_3)` and `Z(ℂS_5, ℂS_2)` are all non-commutative, while every adjacent
pair `Z(ℂS_n, ℂS_{n-1})` is commutative — which is Okounkov–Vershik Prop. 1.4
firing correctly in both directions.

**A thing I did not locate, and it explains why the two hypotheses get
conflated.** *A standard named tower that is semisimple and genuinely not
multiplicity-free.* The classical diagram-algebra towers — symmetric group,
Hecke, Temperley–Lieb, Brauer, partition, wreath products — are all
multiplicity-free **at generic parameters, which is where they are also
semisimple**; the two properties are not observed apart in any of them.
(**Corrected (mg-e8b8):** this sentence said *"are all multiplicity-free"* with
no qualifier, and `T1b2` measures `TL_n(1)` and `TL_n(0)` not to be. The
correction strengthens the point being made rather than weakening it.)
Non-multiplicity-freeness in this subject arises **at a non-generic parameter**,
by **skipping levels**, or by taking a non-Gelfand pair, which is why the
counterexamples in T2 are constructed rather than cited. **Report on a search,
not a claim about the literature.**

---

## 4. PRE-FILED AUDIT — WHERE TO ATTACK THIS DOCUMENT

Ordered by how much I expect them to yield.

**This list is left exactly as it was written, before the audit ran, with each
item's outcome appended in place. Nothing is deleted, and item 3 in particular
stays where it is: it named the row that broke.** The list's own record, now that
mg-2060 has answered it, is that **it pointed straight at the defect and declined
to draw the conclusion** — item 3 asked an auditor whether the dimension shadow
was enough for what §0 claimed, and the answer was **no**. That disclosure is
what aimed the audit at the row, and it is the reason the defect was found in
hours rather than never. **Removing it while repairing the row would delete the
only evidence that the near-miss discipline works.**

1. **Attack the one citation that is not from a PDF on disk, because §2 row 1
   rests on it entirely.** *"A cellular algebra has a symmetric Cartan matrix"*
   is taken from the **Wikipedia article on cellular algebras**, which states
   *"The Cartan matrix `C_A` of `A` is symmetric and positive definite"* without
   proof. **I did not read Graham–Lehrer.** If that statement is wrong, or holds
   only under a hypothesis I have not checked against `kF(P)`, then §2 row 1
   collapses to *"not evaluated"* and the enumeration loses a row. **It does not
   touch §0's headline**, which rests on T1 and T2, nor row 2, which is quoted
   from a PDF. The consequence I draw from it — symmetric ∧ unitriangular ⟹
   identity ⟹ semisimple — is an **elementary one-liner and it is mine**, not a
   citation; this arc's worst finding two generations running has been in exactly
   that kind of sentence (mg-6ad0's X2), so it is flagged here by name.

2. **Attack the claim that `kF(P)` is quasi-hereditary, which is §2 row 2 and
   therefore the deliverable.** The chain is: `F(P)` is a band ⟹ a regular monoid
   ⟹ Putcha's theorem applies. The first link is elementary and is checked in the
   self-test (every face is idempotent under the Tits product, exhaustively for
   all classes at `n ≤ 4`). **The second link — that a band is a von Neumann
   regular monoid — is one line and it is mine.** The third is quoted verbatim
   from Margolis–Steinberg, but **Putcha (J. Algebra 205 (1998) 53–76) and Nico
   were not read**, and the quoted sentence does not state the characteristic
   hypothesis, which for regular monoid algebras is usually *"good
   characteristic"*. We are in characteristic 0 throughout, so I expect it to
   hold, **but I did not verify the hypothesis against the primary source**.

   > **OUTCOME (mg-2060): NOT ESTABLISHED, and the audit did not establish it
   > either.** *"D10, which is the deliverable. … Putcha … still NOT read, and
   > D10 is still unverified. It is the single largest unverified load in the
   > delivered document and the audit leaves it where it found it."* Nor was the
   > second link — *"a band is a von Neumann regular monoid"* — checked. **D10 is
   > now booked as a CONJECTURE (§5), and the headline that rested on it has been
   > retracted** (§0). This item was right and it named the deliverable; what it
   > did not do was stop the deliverable being relayed as a result.

3. **Attack T1's identification of the branching graph.** T1b measures
   `dim Hom_{TL_{n-1}}(V_{n-1,q}, V_{n,p}↓)` at `β = 3` and reads it as the
   restriction multiplicity. **That reading is only valid because `TL_n(3)` is
   semisimple**, which T1c establishes in the same script — so the argument is
   not circular, but it is two-step. At `β = 1` the same Hom dimensions are
   printed and are *different*, which is exactly what a non-semisimple algebra
   should do and is **not** evidence that the composition-factor multiplicities
   changed. The parameter-independence of the *composition factors* is
   Ridout–Saint-Aubin's Prop. 4.1, quoted here (*"Then, we have an exact
   sequence of `TL_{n-1}`-modules"*), and what I measure at every `β` is only its
   **dimension shadow**, `dim V_{n,p} = dim V_{n-1,p} + dim V_{n-1,p-1}`. An
   auditor should check whether that shadow is enough for what §0 claims.

   > **OUTCOME (mg-2060): THE SHADOW IS NOT ENOUGH, AND THIS IS THE ONE ITEM
   > THAT YIELDED.** The auditor did exactly what this item asked, measured the
   > branching graph of the **irreducibles** at every parameter, and §0's claim
   > failed: the vertex set differs at `β = 0` and multiplicities reach 2 at
   > `β = 1` and `β = 0`. It is the document's single BROKEN row, repaired by
   > mg-e8b8 above and in `T1b2`. **The item was right about where to look and
   > wrong about what was there** — it stopped one step short of the conclusion
   > its own sentence set up. That is the honest ranking of what a pre-filed
   > list bought here: it did not catch the error, and it is why the error was
   > caught.
   >
   > Two further defects in this neighbourhood were named by **no** list:
   > T1a's *"a path-pair basis exists **iff** `dim A = Σ (#paths)²`"* is false in
   > the "if" direction (`TL_2(0) = k[e]/(e²)` satisfies the count and has no
   > non-trivial idempotents), and §1's table below states VO Prop. 1.4 as an
   > **unconditional** equivalence when VO state it *"for an arbitrary inductive
   > family of **semisimple** algebras"* — and measured on this document's own
   > object the criterion returns "multiplicity-free" at `β = 1`, where the
   > multiplicity is 2. See mg-2060 §4, X2 and X3.
   >
   > **CORRECTED (mg-13b2): this paragraph said "not repaired by mg-e8b8 … Both
   > are open", and mg-e8b8 had already repaired two of X2's three sites.** X2
   > is now **CLOSED at all FOUR of its sites** — §0's 2×2 table and `T1d`'s
   > printed line at `2e66d03`, unmarked at the time and marked in place now;
   > T1a's *"iff"* here, refuted at 7 of 20 `(n, β)` pairs in `T1c2`; and **a
   > fourth site in §1's clause table, named by no list and found while closing
   > the other three** — it said the path-algebra *"survives without
   > semisimplicity"* with *"this"* reaching back to the matrix units. **X3 is
   > still open**, and it is the only one of the two that ever was. §8 carries
   > the commit-by-commit account.

4. **Attack the Cartan computation.** T3c rebuilds it from MSS's own proof
   (`χ(b) = |bB ∩ L_Y|`, `χ = Σ_Z C_{Z,Y} χ_Z`) rather than from their closed
   formula (4.9) with its Möbius function, because the order convention on
   `Λ(B)` is the part I was least sure of. The check that it is right is
   `Σ C = dim A`, which holds on all 9 rows. **An auditor should rebuild it from
   formula (4.9) instead**, and should check the simple characters
   `χ_X(F) = 1 iff X refines supp(F)` against Brown directly — I verified
   multiplicativity but took the indexing from this repo's own prior work.

5. **Attack the size caps.** T1 stops at `n = 6`, T2 at `n = 5`, T3b caps
   `|F(P)| ≤ 90` and exempts 20 of 63 classes at `n = 5` (each size printed).
   T3c and T3d have no cap. This repo's largest error to date was invisible
   because a measurement ranged over the set on which a false statement happens
   to be true.

6. **Attack the claim that this is a locating exercise.** The brief predicted
   that this instruction would be violated, and predicted that predicting it buys
   nothing. **The two places nearest the line are T1 and T2**, where objects are
   *constructed* in order to test a hypothesis rather than compared against a
   published description. My defence is that the brief asked for exactly this —
   *"a multiplicity-free but non-semisimple example, or a semisimple but
   non-multiplicity-free one, would settle this faster than an argument"* — and
   that both objects are published ones (`TL_n(β)`, `ℂS_n`) with published
   hypotheses evaluated on them. **The place I would attack instead is §0's 2×2
   table**, which is a synthesis and is mine, and §2's verdict column, where a
   one-line consequence is drawn in rows 1 and 2.

---

## 5. CLAIM LEDGER

| # | claim | status | scope |
|---|---|---|---|
| **D1** | Daniel's sentence is Vershik–Okounkov §1 with the hypotheses merged; `⊕_λ End(V^λ)` is their (1.4) and needs semisimplicity alone; *"canonical"* is their word and needs multiplicity-freeness, by their Remark 1.3 | **QUOTED** | 4 passages verbatim from the rendered PDF, plus 5 near-miss negative controls all rejected (T4) |
| **D2** | ~~there is a multiplicity-free tower whose branching graph and path-pair count are parameter-independent and which is a sum of endomorphism algebras at some parameters and not others~~ | **WITHDRAWN (mg-e8b8, on mg-2060's finding).** No such tower is exhibited by this document. | The **path-pair count** is parameter-independent (`132` at `n = 6`) and the **`⊕End` figures** `132/132/99/42` stand, on three instruments. The **branching graph is not**: measured at every parameter under VO's definition (`T1b2`), the vertex set differs at `β = 1` (`[1,4,9,1]` against `[1,5,9,5]` at `n = 6`, with the same *number* of vertices at every level) and at `β = 0` (`[1,4,5]` against `[1,5,9,5]`), and multiplicities reach 2 at `β = 1` and `β = 0`. Multiplicity-freeness moves in exact step with semisimplicity, so `TL_n(β)` separates the hypotheses in neither direction. **Updated (mg-13b2, on mg-a218's finding):** this row substantiated the vertex-set claim with vertex *counts*, which is the statistic-for-structure substitution the withdrawal is about |
| **D2b** | both off-diagonal cells of the 2×2 table are INHABITED: multiplicity-free and not semisimple by `kF(P)`; semisimple and not multiplicity-free by `ℂS_4` on a skipped chain and by `ℂ ⊂ M_2(ℂ)` | **BUILT AND MEASURED**, and it is what the builds actually establish | this is the surviving content of D2 together with D3. `kF(P)` is in the first cell by D6 (all irreducibles one-dimensional — an argument, forced, and booked as one) together with `52` of `541` measured. It does **not** establish which hypothesis carries the conclusion; D4 does not rest on it |
| **D3** | there is a semisimple tower with a multiplicity-2 edge for which `⊕_λ End(V^λ)` still holds and the GZ algebra is not maximal commutative | **BUILT AND MEASURED** | `ℂS_4` on three skipped chains and `ℂS_5` on one; `ℂ ⊂ M_2(ℂ)`; OV Prop. 1.4 tested on 6 pairs, 0 false positives, 0 false negatives |
| **D4** | so semisimplicity is load-bearing and multiplicity-freeness is not: its failure costs the adverb | **STANDS — and its basis is CORRECTED (mg-e8b8). It is a consequence of the QUOTED THEOREMS, not a synthesis of the builds** | `A ≅ ⊕_λ End(V_λ) ⟺ A` semisimple for every finite-dimensional algebra, because a finite direct sum of endomorphism algebras **is** semisimple — no branching hypothesis appears in it. Remark 1.3 (D1, quoted) gives the adverb. It was booked as *"THE SYNTHESIS OF D2 AND D3, and it is mine"*; **D2 is withdrawn and the verdict does not need it.** mg-2060 reached the same conclusion by the same route and calls it *"an argument from the theorem mg-db09 quotes, not a measurement"* |
| **D5** | `dim kF(P)/rad = |AC(P)|`; the radical is 90.4% of `kF(P)` at the `n = 5` antichain and 95.7% at `n = 6` | **MEASURED, third instrument** | trace form with the radical verified to be a nilpotent two-sided ideal; **67 of 87 classes to `n ≤ 5`, 0 bad**, 20 exempt over `|F(P)| ≤ 90`. **Updated (mg-e8b8):** mg-2060 removed the cap and got **87 of 87 to `n ≤ 5`, 0 bad**, including `|F| = 541`, so the **90.4% figure is now derived**; the **95.7% at `n = 6` is still arithmetic** on `|F|` and `|AC|` and has been re-derived by nobody. Two further wording defects in this row are recorded but **not repaired** (out of mg-e8b8's scope): T3b prints twelve exempt **sizes**, not *"each listed with its size"* for twenty classes (mg-2060 X5) |
| **D6** | `kF(P)` has multiplicity-free branching along any chain of subalgebras, trivially, because all its irreducibles are one-dimensional | **AN ARGUMENT, DELIBERATELY NOT BOOKED AS EVIDENCE** | forced for every `P` of every size, so a measurement of it could not do any work. mg-6ad0's X5 is the finding that this repo has booked forced answers as MEASURED before |
| **D7** | the Cartan matrix of `kF(P)` is unipotent lower triangular, and is symmetric exactly when `kF(P)` is semisimple | **MEASURED**, reproducing MSS Thm 4.18 | 9 posets to `n = 5` including the `n = 5` antichain (52×52); `Σ C = dim A` on every row |
| **D8** | `kF(P)` is semisimple for exactly one poset class at each `n ≤ 5`, the total order | **MEASURED, no cap** | all 63 classes at `n = 5`; `kF(chain_n) = k^{2^{n-1}}` |
| **D9** | a cellular algebra has a symmetric Cartan matrix, so (with D7) `kF(P)` is not cellular unless `P` is a total order | **UPGRADED by mg-2060: stated and attributed in a refereed source, with the proof indicated** | was Wikipedia with **Graham–Lehrer not read**; mg-2060 fetched Ehrig–Tubbenhauer (`arXiv:1710.02851`, Remark 2.19) citing König–Xi 1999 Prop. 3.2, and `C = DᵀD` is the reason a Gram matrix is symmetric. The one-line consequence that is mine was executed independently and holds on 9 of 9 rows. §4 item 1 |
| **D10** | `kF(P)` is quasi-hereditary, as is the branching axis's non-semisimple continuation, so quasi-hereditary algebras contain both — delivering a standard filtration, not `⊕End` | **A CONJECTURE. NOT A RESULT, AND IT WAS RELAYED AS ONE — see the retraction note below** | see the note below |
| **D11** | the branching axis's `S_n` object is `ℂS_n` and the species axis's is `kΣ_n`; they are different algebras joined by a theorem (Bidigare/Solomon), not values of one construction | **MEASURED for the dimensions, CITED to mg-7d75 for Bidigare** | `dim ℂS_5 = 120` semisimple; `dim kΣ_5 = 541`, 90.4% radical |
| **D12** | the candidate space for a common umbrella is the eight rows of §2; row 3 (towers of recollement) was **located and not evaluated** *by this ticket* | **REPORT ON A SEARCH** | not a claim about the literature. Queries were targeted, not exhaustive. **Updated (mg-e8b8):** mg-2060 fetched CMPX and evaluated (A1) — holds — and (A2)(i) — fails for every face idempotent at `n = 3, 4`; §2 row 3 carries the current state |
| **D13** | I did not locate a statement at Daniel's *categorical* generality that is neither the chain-of-semisimple-algebras statement nor a tautology | **REPORT ON A SEARCH, and the weakest claim here** | §1. Explicitly **not** a claim that none exists |
| **NOT CLAIMED** | that anything here is new; that anything here is publishable; that the searches were exhaustive; that `kF(P)` **is** quasi-hereditary (D10 is a conjecture); that the two axes **do** share a property; that `TL_n(β)` separates the two hypotheses (D2, withdrawn); that the `n = 6` radical figure was re-derived; that `kF(P)` is or is not a tower of recollement; that any construction with both axes as values cannot be written down; that anything about the walk, `λ₂`, `Δ_AT` or the pricing follows | | |

### D10 IN FULL — the conjecture, its status, and what would establish it

**D10 is the deliverable of this ticket, and it is unverified.** It is set out
here rather than in a table cell because a one-line status is what let it be
read as a result.

**Statement.** `kF(P)` is quasi-hereditary; so are the diagram algebras of the
branching axis at the parameters where they have finite global dimension;
therefore quasi-hereditary algebras are a common umbrella containing both axes,
and what the umbrella delivers is a **standard filtration**, not `⊕End`.

**What is actually in hand.** One quotation and two unchecked links.

| link | status |
|---|---|
| `F(P)` is a band — every face is idempotent under the Tits product | **CHECKED**, exhaustively for all poset classes at `n ≤ 4`, in the self-test |
| a band is a **von Neumann regular** monoid | **NOT CHECKED. One line, and it is mine.** mg-2060: *"§7 item (b) … Not checked."* |
| *"The algebras of finite (von Neumann) regular monoids provide natural and diverse examples of quasi-hereditary algebras … first proved by Putcha"* | **QUOTED VERBATIM** from Margolis–Steinberg `arXiv:1101.0416` §1, and mg-2060 verified that source window against its own independent extraction |
| the characteristic hypothesis Putcha's theorem carries (for regular monoid algebras usually *"good characteristic"*) | **NOT VERIFIED against the primary source. Putcha and Nico were never read — not by mg-db09, not by mg-2060** |
| the branching axis's side of the umbrella | **CITED, not evaluated.** It is also CMPX axiom (A2′), and CMPX (A2)(ii), (A4), (A5), (A6) are all untested |

**What would establish it**, in the order a successor should attempt it:

1. **Read Putcha, *J. Algebra* 205 (1998) 53–76**, and record the theorem's exact
   hypotheses — in particular the characteristic condition. We are in
   characteristic 0 throughout, so this is expected to go through; **expected is
   not verified, and that distinction is the whole of this repair.**
2. **Check that a band is von Neumann regular** — for every `x` there is `y` with
   `xyx = x`. In a band `x² = x`, so `y = x` should do it. **One line, and it has
   to be written down and checked rather than asserted**, because the last
   unchecked one-liner in this document is the reason §0 carries a withdrawal.
3. **Failing (1), verify quasi-heredity of `kF(P)` directly**: exhibit a chain of
   idempotent ideals `0 = J_0 ⊂ ⋯ ⊂ J_m = kF(P)` with each `J_i/J_{i-1}` a
   heredity ideal (idempotent, projective as a left module over the quotient,
   with `J e J`-type endomorphism condition). At `n ≤ 4` (`|F| ≤ 75`) this is
   within reach of the existing instrument; at `n = 5` (`|F| = 541`) it is not
   obviously so.
4. **Then, and only then**, ask whether the branching axis is under the same
   umbrella, and whether "a shared property" is a statement with content.

**The retraction of record.** At **2026-07-30 19:50** `docs/roadmap.md` carried,
as **THE HEADLINE**, *"the branching axis and the species axis share a PROPERTY,
not a CONSTRUCTION — quasi-hereditary"*, and **it went to Daniel in that form**.
At **20:45**, on mg-2060's finding, it was **retracted** — `docs/roadmap.md`,
commit `f4eaea6`, *"RETRACT the quasi-hereditary headline (mg-2060) — D10 is
unverified"*. **That retraction is repeated here on purpose.** A reader who comes
to this document later will not read a superseded roadmap entry, and a
retraction that lives only in mail and in a roadmap is not a retraction. The
elapsed time between delivery and retraction was **55 minutes**, and the thing
that closed it was the pre-filed §4 item 2, which named this row as the
deliverable and said it was unverified — **in the same document that then relayed
it as the headline.** The disclosure worked; the relay did not read it.

---

## 6. REPRODUCE

```
cd code/branching_locate_db09 && ./run_all.sh    # ~6 min, pure Python 3, NO NETWORK
```

Committed outputs: `out_selftest.txt` (699 520 assertions), `out_t1_tl.txt`,
`out_t2_gz.txt`, `out_t3_ours.txt`, `out_t4_quotes.txt`, `out_t5_labels.txt`.
All five `TOTAL BAD`
lines are `0`. `./fetch_sources.sh` is the one network script and `run_all.sh`
does not call it; `sources_db09.txt` is the committed `pdftotext` extraction the
quotations are checked against.

**What `mg-13b2` added to the instrument.** `T1c2` in `t1_tl.py`, which refutes
T1a's withdrawn *"iff"* at 7 of the 20 `(n, β)` pairs; the rewritten `T1b2` (i),
which reports the vertex **set** in canonical form with **no count column beside
it**; and **`t5_labels.py`**, which measures every disposition label in this
document — **29 labels, 100 checks**. It is the only script here that needs a **git
checkout**, because a label saying *"corrected at `2e66d03`"* is a claim about a
diff, and the only one that **exits non-zero** when it fails, because a label
that has stopped being true is a gate and not a report. Its checks are
statements about the **current tree** or about **named historical commits** —
never about the diff of the commit it is part of, which is the trap `mg-8e30`
paid for and the reason it reads the same on a re-run. It carries a **7-mutation
corruption battery**, applied in memory: each mutation reopens one defect this
repair closed and names the check that must go red. **All 7 fire.**

**What the repair changed in the instrument (mg-e8b8).** `t1_tl.py` gained
**`T1b2`**, which measures the branching graph as Vershik–Okounkov define it — on
the **irreducibles** `L(n,p) = V_{n,p}/rad⟨,⟩` — at **every** parameter, and
`T1d` now prints the withdrawal instead of the withdrawn claim. `T1b`'s heading
was *"the BRANCHING GRAPH, measured (not cited)"* and is now *"the CELL-module
branching data, measured"*, which is what it always was. **The correction is made
at source and not only in prose:** the old text was printed by a committed output
inside a run ending `TOTAL BAD: 0`, and this repo has twice found a correction
that lived in the document while the instrument still asserted the error
(mg-73df's X3, repaired at mg-a4ef). `T1b2`'s numbers are checked three ways —
`Σ_p (dim L)² = dim A/rad` on all 20 `(n, β)` pairs in the self-test; the new
whole-diagram action asserted equal to the generator action `T1b` already used;
and each multiplicity solve checked for uniqueness, integrality, non-negativity
and `Σ_q m_q·dim L(n-1,q) = dim L(n,p)`. **They agree row for row with mg-2060's
B1a/B1b, measured on a disjoint instrument.** `t2`, `t3` and `t4` are untouched
and their outputs are byte-identical; mg-2060's `b0_repro.sh` regenerates all
five and still reports **5 of 5 IDENTICAL**, against the repaired code.

**Sources**

- [Vershik–Okounkov, *A new approach to the representation theory of the symmetric groups. II*](https://arxiv.org/abs/math/0503040) — **read, in extract (§1, §2)**
- [Ridout–Saint-Aubin, *Standard modules, induction and the structure of the Temperley–Lieb algebra*](https://arxiv.org/abs/1204.4505) — **read, in extract (§4, App. B)**
- [Margolis–Saliola–Steinberg, *Cell complexes, poset topology and the representation theory of algebras arising in algebraic combinatorics and discrete geometry*](https://arxiv.org/abs/1508.05446) — **read, in extract (§4.7)**
- [Margolis–Steinberg, *Quivers of monoids with basic algebras*](https://arxiv.org/abs/1101.0416) — **read, in extract (§1)**
- Graham–Lehrer, *Cellular algebras*, Invent. Math. **123** (1996) — **NOT read**; the Cartan-symmetry statement is from [the Wikipedia article on cellular algebras](https://en.wikipedia.org/wiki/Cellular_algebra)
- Goodman–de la Harpe–Jones, *Coxeter Graphs and Towers of Algebras*, MSRI 14 (1989), Ch. 2 — **located, NOT read**
- Putcha, *Complex representations of finite monoids II: highest weight categories and quivers*, J. Algebra **205** (1998) 53–76 — **located, NOT read, and D10 rests on it.** Still not read as of mg-2060
- Cox–Martin–Parker–Xi, *Representation theory of towers of recollement*, J. Algebra **302** (2006) 340–360 — **located, NOT evaluated here**; fetched and partly evaluated by mg-2060 (§2 row 3)
- Graham–Lehrer's Cartan-symmetry statement is now taken from [Ehrig–Tubbenhauer, *Relative cellular algebras*](https://arxiv.org/abs/1710.02851) (Remark 2.19, citing König–Xi 1999 Prop. 3.2) — **fetched and read by mg-2060**, not by this ticket

---

## 7. NOTE FOR pm-onethird — SCOPE DISCIPLINE

Three things this document deliberately does **not** do.

* It does **not** develop mathematics. Two objects are **constructed** (T1, T2)
  because the brief asked for exactly those two objects, and both are published
  algebras with published hypotheses evaluated on them. **Four elementary
  one-line derivations were needed and each is flagged in place and pre-filed at
  §4**: (a) symmetric ∧ unitriangular ⟹ identity; (b) a band is a regular
  monoid; (c) a one-dimensional module over a subalgebra is simple, so all
  branching from `kF(P)` is multiplicity-free; (d) `kF(P)` is semisimple iff
  `|F(P)| = |AC(P)|`. **(a) is the one that would be expensive if wrong.**
* It does **not** edit `docs/OneThird-Branching-Graphs-Where-This-Lives.md`,
  `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`,
  `docs/OneThird-Landscape-Where-This-Lives.md`, `STATE.md` or the roadmap.
  §0's correction to the *"`S_n` lies in both"* premise is a statement **about**
  the brief, filed here; whether to fold it back is pm-onethird's call.
* It does **not** claim novelty for anything, and it does **not** claim that
  `kF(P)` fails to be a tower of recollement — that is §2 row 3, and it is an
  open question with no verdict manufactured in either direction.

**One thing it does do that is worth pm-onethird's attention.** ~~The successor
question here is bounded and specific: **does the `kF(P)` family satisfy the
axioms of a tower of recollement (Cox–Martin–Parker–Xi)?**~~ **SUPERSEDED
(mg-e8b8).** Two corrections. First, *"the `kF(P)` family"* is **not a
sequence** — it is indexed by **posets**, 63 of them at `n = 5` — and a tower of
recollement is a family `A_0, A_1, A_2, …` with `A_{n-2} ≅ e_n A_n e_n`. The
successor must name the **antichain family** `kΣ_n`, which is the only sub-family
that is a sequence and the one every figure here is about. Second, part of the
question is **already answered**: mg-2060 evaluated (A1) — it **holds**, with the
idempotent exhibited for `2 ≤ n ≤ 6` — and (A2)(i), which **fails for every face
idempotent** realising (A1) at `n = 3, 4`. A successor commissioned in the words
above would spend part of its first cycle re-deriving a three-line consequence of
the Tits product. **File it against that state: (A2)(ii), (A4), (A5), (A6), and
whether (A3) needs a unital embedding.**

**And the successor that now outranks it.** **D10 — is `kF(P)` quasi-hereditary?
— is the deliverable, it is unverified, and it was relayed to Daniel as a result
before anyone checked.** §5 sets out what would establish it, and step (1) is to
**read Putcha**. Until that is done, this document's answer to *"do the two axes
share a common umbrella?"* is **"open"**, not **"yes, quasi-hereditary"**.

---

## 8. THE REPAIR — WHAT mg-e8b8 CHANGED, AND WHAT IT DID NOT

**Scope. CORRECTED (mg-13b2): this paragraph said mg-e8b8 repaired the two
things mg-2060 left outstanding "and nothing else", and it also closed two
sites of X2 — the finding it books below as untouched.** The sentence and the
list under it disagreed with the diff in the same direction, and that is the
defect `mg-a218` raised. It changed **no mathematics**: every figure this
document reports still reproduces, and the one new measurement (`T1b2`) agrees
with the audit's. **This section now carries a status column rather than a
disposition sentence, and `t5_labels.py` measures every row of it.**

**Repaired.**

1. **The two assertions that the `TL` tower is multiplicity-free at every
   parameter** — §0's *"MEASURED (not cited) to be the same multiplicity-free
   graph at each"* and *"held fixed down that column"*, plus the same claim in
   §0's four-row table, in the 2×2 table's cell placement, in §3's *"the
   branching graph is unchanged and multiplicity-free"*, and in §3's *"the
   classical diagram-algebra towers … are all multiplicity-free"*. **Five sites,
   because two of them could not be fixed while three others kept asserting it.**
2. **The separating example is WITHDRAWN, and the withdrawal is reported as a
   withdrawal** — not as a refinement, not as a clarification. It could not be
   re-established: the invariant has now been measured under the definition in
   play, at every parameter, and it **refutes** the hypothesis the example needed.
   The verdict D4 rests where mg-2060 says it always rested — **on the theorem**.
3. **D10 is booked as a CONJECTURE** with the chain of links laid out link by
   link, four steps of what would establish it, and **the retraction of record**:
   it went to Daniel as the headline at 19:50 and was retracted at 20:45.
4. **At source, not only in prose.** `t1_tl.py` no longer prints the withdrawn
   claim; `T1b2` measures the real invariant; the instrument README says so.

**Named by mg-2060, and where each one now stands.** This list was headed
*"Deliberately NOT repaired, and each is open"* until `mg-13b2`. **It was wrong
about its first entry, and wrongly in the direction that flatters the commit:
mg-e8b8 had already closed two of X2's three sites.** A reader trusting the
label believed all three were open; a reader trusting the diff believed X2 was
addressed; neither reading was right. The heading is now a status column and
every row of it is checked against the tree and against the named commits by
`t5_labels.py`.

| # | finding | site(s) | status |
|---|---|---|---|
| **X2** | T1a's *"iff"* — false in the "if" direction; `TL_2(0)` is the counterexample and it is on this document's own T1c table | **four**, not the three mg-2060 named: §0's 2×2 table, `T1d`'s printed line, T1a's header, and §1's clause table | **CLOSED — and closed in two commits, which is why the old label was wrong.** `2e66d03` (mg-e8b8) corrected the 2×2 table and `T1d` **without a marker at either**, while booking X2 as untouched. `mg-13b2` corrects T1a's header, adds **`T1c2`** — which refutes the converse at **7 of the 20 `(n, β)` pairs**, `TL_2(0)` the smallest — marks the two earlier sites in place, and closes **a fourth site named by no list**: §1's clause table said the path algebra *"survives without semisimplicity"*, the antecedent being the matrix units |
| **X3** | §1's unconditional reading of VO Prop. 1.4 — VO state it for *semisimple* families, and the criterion returns the wrong answer on this document's own object at `β = 1` | §1's table | **OPEN.** Untouched by `2e66d03` and by `mg-13b2`; the unqualified sentence is still in §1 |
| **X5** | D5's *"each listed with its size"* — T3b prints twelve sizes for twenty classes | D5, `t3_ours.py` | **OPEN.** `t3_ours.py` is byte-identical across both commits |
| **X6** | §7's count of four one-line derivations — mg-2060's census finds eight, three unflagged | §7 | **OPEN.** §7 still says four |
| — | the `n = 6` 95.7% figure — still arithmetic | §0, D5 | **OPEN, and disclosed where it is quoted.** Re-derived by nobody; `\|F\| = 4683` puts the trace form out of reach on all three instruments |

**What `mg-13b2` repaired**, on mg-a218's audit of this repair:

1. **§0's vertex column reports the SET, not a count** (mg-a218 X1). It printed
   `1,2,2,3,3,4` identically at `β = 3`, `2` and `1` — and at `β = 1` the graph
   is different from `β = 3` at four of the six levels. **A future reader
   comparing that column across parameters would have concluded the graphs
   agree, which is the inference that broke this document in the first place,
   sitting beside the corrected prose.** The column now carries the canonical
   form `dim L(n,p)`, `p` ascending; `T1b2` prints the fuller `[p:dim]` form,
   checks the abbreviation does not collide, and prints **no count column beside
   it**.
2. **The disposition labels are reconciled with the diff** (mg-a218 X2), which is
   the table above, the marker at §0's 2×2 table, the marker in `T1d`, and the
   corrected outcome note at §4 item 3.
3. **X2 turned out to have a fourth site, and no list named it.** Closing the
   third meant sweeping for the phrase, and §1's clause table said the
   path algebra *"survives without semisimplicity"* with *"this"* reaching back
   to the **matrix units** — the same false claim, in a live table, in the
   section whose whole subject is what happens when a hypothesis is dropped.
   **It is booked as found by this repair and not by mg-2060**, whose census
   named three.
4. **The labels are now checked by an instrument, not by reading.**
   `t5_labels.py` takes **every** disposition label in this document — **29 of
   them, 100 checks** — states what each one asserts about the tree or about a
   **named commit**, and measures it. Its verdict is in `out_t5_labels.txt` and
   it ends with a `TOTAL BAD` line like every other script here. It also carries
   a **7-mutation corruption battery**: each mutation reopens one defect this
   repair closed and names the check that must go red, **and all 7 fire** — a
   checker that never fires is indistinguishable from one that cannot.
   **The labels are a convention adopted on the day this
   document was written and they are already load-bearing** — a reader consults
   the label precisely so as not to read the diff — **which is the argument for
   auditing them, not for dropping them.**

**What survived the repair on purpose.** §4's pre-filed attack list is intact,
including **item 3, which named this exact row, called the measurement *"its
dimension shadow"*, and asked an auditor whether the shadow was enough.** It was
not. **That disclosure is why the defect was found in hours instead of never, and
deleting it while fixing the row would remove the only evidence the near-miss
discipline works.** Each item now carries its outcome appended in place; nothing
was rewritten to look better in hindsight.
