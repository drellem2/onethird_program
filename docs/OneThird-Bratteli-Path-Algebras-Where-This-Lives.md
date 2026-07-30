# Bratteli/path algebras: locating Daniel's generalisation, and which hypothesis carries it

**Work item:** mg-db09. **Date:** 2026-07-30. **Computation:** permitted, used,
committed (`code/branching_locate_db09/`, `run_all.sh`, ~6 min, 698 963-assertion
self-test, four test scripts, all four `TOTAL BAD: 0`).

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
"canonically". Both halves are settled here by BUILDING the object each would
forbid, not by argument.**

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

### The two objects, built

**1. Multiplicity-free and NOT semisimple — the conclusion fails.** The
Temperley–Lieb tower `TL_1 ⊂ TL_2 ⊂ ⋯` at four parameters. The branching graph is
**measured** (not cited) to be the same multiplicity-free graph at each — every
restriction multiplicity is 0 or 1, and the rule is `V_{n,p} ↦ V_{n-1,p} ⊕
V_{n-1,p-1}` — and the pairs-of-paths count `Σ_p (dim V_{n,p})²` is `132` at
`n = 6` at every parameter, because the cell-module dimensions do not depend on
the parameter at all:

| `β` | `dim TL_6` | `dim ⊕_λ End(L_λ)` | endomorphism algebra? | branching |
|---|---|---|---|---|
| 3 | 132 | **132** | **yes** | multiplicity-free |
| 2 | 132 | **132** | **yes** | multiplicity-free |
| 1 | 132 | **99** | **no** | multiplicity-free |
| 0 | 132 | **42** | **no** | multiplicity-free |

Multiplicity-freeness is held fixed down that column and the conclusion changes.
Semisimplicity varies in step with it. (T1c/T1d; the semisimple quotient is
computed **twice by disjoint routes** — the trace form of the regular
representation, and `Σ_p (rank of the Gram matrix of V_{n,p})²` — with **0
disagreements** on 20 `(n, β)` pairs.)

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
| **multiplicity-free** | Daniel's statement, in full: `⊕End`, canonical path basis. `ℂS_n`; `TL_n(3)` | **`⊕End` FAILS.** Path-pair *basis* survives, direct sum does not. `TL_6(1)`: 99 of 132. **`kF(P)`: 52 of 541** |
| **not multiplicity-free** | **`⊕End` HOLDS**, canonicity fails: the path basis needs a choice. `ℂS_4` on a skipped chain; `ℂ ⊂ M_2(ℂ)` | both fail |

**Failure of semisimplicity BREAKS the conclusion. Failure of
multiplicity-freeness WEAKENS it — and weakens only the adverb.**

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

### The deliverable: are the two axes instances of a common construction?

**No — and the honest answer is more interesting than either alternative in the
brief.** They are **not two values of one construction**, and they are **not
unrelated**. There is a common umbrella, it is **quasi-hereditary algebras**, and
what it delivers is a **standard filtration and not an endomorphism algebra**:

> Margolis–Steinberg, *Quivers of monoids with basic algebras*
> (`arXiv:1101.0416`), §1, verbatim: *"The algebras of finite (von Neumann)
> regular monoids provide natural and diverse examples of quasi-hereditary
> algebras. This was first proved by Putcha [73] and further developed by the two
> authors of this paper using homological methods [55]. However, Nico essentially
> had noted that semigroup algebras of regular semigroups are quasi-hereditary
> before the concept was even invented."*

`F(P)` is a band, hence a regular monoid, so `kF(P)` is in that class. The
diagram algebras of the branching axis are in it too. **Inside that umbrella the
two axes sit at opposite extremes, and the invariant that separates them is the
Cartan matrix.** Measured, on our side (T3c), reproducing
Margolis–Saliola–Steinberg Thm 4.18 against our object:

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
| *"the Bratteli/path algebra"* | matrix units indexed by pairs of increasing paths with a common endpoint; `dim = Σ_λ (#paths to λ)²` | **this survives without semisimplicity** — T1a measures it at every `β` — which is precisely why the statement looks parameter-independent when it is not |
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
Eight were evaluated. **One of them is not a negative** — row 2 — and it is the
answer.

| # | candidate umbrella | evaluated? | verdict | reason |
|---|---|---|---|---|
| **1** | **Cellular algebras** (Graham–Lehrer, Invent. Math. 123 (1996)) — the branching axis's own non-semisimple continuation: TL, Brauer, partition, Hecke | **yes** | **EXCLUDES US, conditionally** | a cellular algebra has a **symmetric** Cartan matrix; `kF(P)`'s is **unipotent lower triangular** (MSS Thm 4.18, reproduced at T3c) and measurably **not symmetric** unless `P` is a total order. Symmetric ∧ unitriangular ⟹ identity ⟹ semisimple. **The symmetry statement is CITED FROM A SECONDARY SOURCE and Graham–Lehrer was not read** — see §4 item 1 |
| **2** | **Quasi-hereditary algebras / highest weight categories** (Cline–Parshall–Scott) | **yes** | **CONTAINS BOTH — this is the answer** | `kF(P)` is the algebra of a band, hence of a **regular monoid**, and *"the algebras of finite (von Neumann) regular monoids provide natural and diverse examples of quasi-hereditary algebras"* (Margolis–Steinberg, quoted verbatim; **Putcha and Nico located, not read**). The diagram algebras of the branching axis are quasi-hereditary at the parameters where they have finite global dimension. **What the umbrella delivers is a filtration by standard modules — not `⊕End`, which is the split case** |
| **3** | **Towers of recollement** (Cox–Martin–Parker–Xi, J. Algebra 302 (2006)) — the axiomatisation of quasi-hereditary *towers* of diagram algebras | **located, NOT evaluated** | **THE OPEN QUESTION, named rather than answered** | this is the branching axis's own framework for the non-semisimple case, and it is a framework for *towers*. Whether the `kF(P)` family carries the idempotent structure its axioms require is **untested by this ticket and by every earlier one**, and testing it is new mathematics, which this ticket forbids. **No verdict is manufactured.** It is the single highest-value successor question here |
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

**Half in — the conclusion fails, the basis survives.** The same towers at
non-generic parameters. Temperley–Lieb at `β = 1` (`q` a primitive 6th root of
unity) and at `β = 0`: measured here, the pairs-of-paths basis is still of the
right size at every `n ≤ 6` (`dim TL_n = Σ_p (dim V_{n,p})²`, 0 bad), the
branching graph is unchanged and multiplicity-free, and the algebra is not a sum
of endomorphism algebras (99 and 42 out of 132 at `n = 6`). Published controls
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
multiplicity-free. Non-multiplicity-freeness in this subject arises by **skipping
levels** or by taking a non-Gelfand pair, which is why the counterexamples in T2
are constructed rather than cited. **Report on a search, not a claim about the
literature.**

---

## 4. PRE-FILED AUDIT — WHERE TO ATTACK THIS DOCUMENT

Ordered by how much I expect them to yield.

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
| **D2** | there is a multiplicity-free tower whose branching graph and path-pair count are parameter-independent and which is a sum of endomorphism algebras at some parameters and not others | **BUILT AND MEASURED** | `TL_n(β)`, `n ≤ 6`, `β ∈ {3,2,1,0}`; semisimple quotient by **two disjoint routes**, 0 disagreements on 20 pairs; 6 published controls reproduced |
| **D3** | there is a semisimple tower with a multiplicity-2 edge for which `⊕_λ End(V^λ)` still holds and the GZ algebra is not maximal commutative | **BUILT AND MEASURED** | `ℂS_4` on three skipped chains and `ℂS_5` on one; `ℂ ⊂ M_2(ℂ)`; OV Prop. 1.4 tested on 6 pairs, 0 false positives, 0 false negatives |
| **D4** | so semisimplicity is load-bearing and multiplicity-freeness is not: its failure costs the adverb | **THE SYNTHESIS OF D2 AND D3, and it is mine** | the 2×2 table in §0. Neither cell is a citation |
| **D5** | `dim kF(P)/rad = |AC(P)|`; the radical is 90.4% of `kF(P)` at the `n = 5` antichain and 95.7% at `n = 6` | **MEASURED, third instrument** | trace form with the radical verified to be a nilpotent two-sided ideal; **67 of 87 classes to `n ≤ 5`, 0 bad**, 20 exempt over `|F(P)| ≤ 90`, each listed. The two percentages come from `\|F\|` and `\|AC\|` alone |
| **D6** | `kF(P)` has multiplicity-free branching along any chain of subalgebras, trivially, because all its irreducibles are one-dimensional | **AN ARGUMENT, DELIBERATELY NOT BOOKED AS EVIDENCE** | forced for every `P` of every size, so a measurement of it could not do any work. mg-6ad0's X5 is the finding that this repo has booked forced answers as MEASURED before |
| **D7** | the Cartan matrix of `kF(P)` is unipotent lower triangular, and is symmetric exactly when `kF(P)` is semisimple | **MEASURED**, reproducing MSS Thm 4.18 | 9 posets to `n = 5` including the `n = 5` antichain (52×52); `Σ C = dim A` on every row |
| **D8** | `kF(P)` is semisimple for exactly one poset class at each `n ≤ 5`, the total order | **MEASURED, no cap** | all 63 classes at `n = 5`; `kF(chain_n) = k^{2^{n-1}}` |
| **D9** | a cellular algebra has a symmetric Cartan matrix, so (with D7) `kF(P)` is not cellular unless `P` is a total order | **CITED FROM A SECONDARY SOURCE + a one-line consequence that is MINE** | Wikipedia's article on cellular algebras; **Graham–Lehrer not read**. §4 item 1 |
| **D10** | `kF(P)` is quasi-hereditary, as is the branching axis's non-semisimple continuation, so quasi-hereditary algebras contain both — delivering a standard filtration, not `⊕End` | **QUOTED for the general theorem; the application is a one-line check that is MINE** | Margolis–Steinberg quoted verbatim; **Putcha and Nico located, not read**; the characteristic hypothesis not verified against the primary source. §4 item 2 |
| **D11** | the branching axis's `S_n` object is `ℂS_n` and the species axis's is `kΣ_n`; they are different algebras joined by a theorem (Bidigare/Solomon), not values of one construction | **MEASURED for the dimensions, CITED to mg-7d75 for Bidigare** | `dim ℂS_5 = 120` semisimple; `dim kΣ_5 = 541`, 90.4% radical |
| **D12** | the candidate space for a common umbrella is the eight rows of §2; rows 3 (towers of recollement) was **located and not evaluated** | **REPORT ON A SEARCH** | not a claim about the literature. Queries were targeted, not exhaustive |
| **D13** | I did not locate a statement at Daniel's *categorical* generality that is neither the chain-of-semisimple-algebras statement nor a tautology | **REPORT ON A SEARCH, and the weakest claim here** | §1. Explicitly **not** a claim that none exists |
| **NOT CLAIMED** | that anything here is new; that anything here is publishable; that the searches were exhaustive; that `kF(P)` is or is not a tower of recollement; that any construction with both axes as values cannot be written down; that anything about the walk, `λ₂`, `Δ_AT` or the pricing follows | | |

---

## 6. REPRODUCE

```
cd code/branching_locate_db09 && ./run_all.sh    # ~6 min, pure Python 3, NO NETWORK
```

Committed outputs: `out_selftest.txt` (698 963 assertions), `out_t1_tl.txt`,
`out_t2_gz.txt`, `out_t3_ours.txt`, `out_t4_quotes.txt`. All four `TOTAL BAD`
lines are `0`. `./fetch_sources.sh` is the one network script and `run_all.sh`
does not call it; `sources_db09.txt` is the committed `pdftotext` extraction the
quotations are checked against.

**Sources**

- [Vershik–Okounkov, *A new approach to the representation theory of the symmetric groups. II*](https://arxiv.org/abs/math/0503040) — **read, in extract (§1, §2)**
- [Ridout–Saint-Aubin, *Standard modules, induction and the structure of the Temperley–Lieb algebra*](https://arxiv.org/abs/1204.4505) — **read, in extract (§4, App. B)**
- [Margolis–Saliola–Steinberg, *Cell complexes, poset topology and the representation theory of algebras arising in algebraic combinatorics and discrete geometry*](https://arxiv.org/abs/1508.05446) — **read, in extract (§4.7)**
- [Margolis–Steinberg, *Quivers of monoids with basic algebras*](https://arxiv.org/abs/1101.0416) — **read, in extract (§1)**
- Graham–Lehrer, *Cellular algebras*, Invent. Math. **123** (1996) — **NOT read**; the Cartan-symmetry statement is from [the Wikipedia article on cellular algebras](https://en.wikipedia.org/wiki/Cellular_algebra)
- Goodman–de la Harpe–Jones, *Coxeter Graphs and Towers of Algebras*, MSRI 14 (1989), Ch. 2 — **located, NOT read**
- Putcha, *Complex representations of finite monoids II: highest weight categories and quivers*, J. Algebra **205** (1998) 53–76 — **located, NOT read**
- Cox–Martin–Parker–Xi, *Representation theory of towers of recollement*, J. Algebra **302** (2006) 340–360 — **located, NOT evaluated**

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

**One thing it does do that is worth pm-onethird's attention.** The successor
question here is bounded and specific: **does the `kF(P)` family satisfy the
axioms of a tower of recollement (Cox–Martin–Parker–Xi)?** That is the branching
axis's own framework for the non-semisimple case, it is a framework for towers
rather than for single algebras, and it is the only row of §2 that was located
and not evaluated. It is also the row where an affirmative answer would change
the deliverable's verdict from *"a shared property"* to *"a shared
construction"*.
