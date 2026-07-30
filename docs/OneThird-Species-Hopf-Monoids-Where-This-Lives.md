# Species and Hopf monoids: is there ONE categorical operation with both `S_n` representation theory and the poset-quotient story as instances?

**Work item:** mg-7d75. **Date:** 2026-07-30. **Computation:** permitted, used, committed
(`code/species_7d75/`, `run_all.sh`, ~46 s, 759-assertion self-test, six test scripts, all
reporting `TOTAL BAD: 0`).

> **REPAIRED 2026-07-30 (mg-6f61), after the independent audit mg-a61f
> (`docs/OneThird-Audit-mg-7d75-Species-Hopf-Monoids.md`, `8e61d1a`).** Eight things changed.
> **Downward:** §8 **C3**'s extremal claim was **false** and is corrected (§8); §0's
> *"5 axioms"* count is brought into agreement with §5, which was right all along (§0, §5);
> the **Aguiar–Ardila §12** and **Aguiar–Mahajan §17.5** quotations are corrected against
> rendered PDFs and the **Marshall–Martin** one un-truncated (§1, §4); the **"braid cone"
> terminology collision** is named (§1); §2.2's *"three of the four columns are the control"*
> is **one control computed twice** (§2.2); and control (ii)'s accounting is corrected —
> **its conclusion explicitly survives** (§5, §6 item 5). **Upward:** §2.3's identity is a
> **corollary, not an unlocated measurement**, so four hedges are withdrawn **and the
> successor literature search they routed is cancelled** (§0, §2.3, §6 item 6, §10 item 2,
> S1, S12). **And the boundary is now stated where it is read:** the **`S_n` half of the
> correspondence is located in the literature and not verified here**, at every occurrence
> and by name (§0 item 4, §3, §6 item 1, §9 rows 3 and 11, **S4**, **S5**).
>
> The reasoning and the instrument are in `docs/OneThird-Species-Hopf-Monoids-Repair.md` and
> `code/species_repair_6f61/`. Every repaired passage is marked in place; **nothing false has
> been deleted without being quoted where it stood.**
>
> **AND THE SAME CORRECTIONS ARE NOW AT SOURCE (mg-f8fa, `docs/OneThird-Species-Hopf-Monoids-Repair-Remainder.md`,
> `code/species_remainder_f8fa/`).** Three of the corrections above were made **in this
> document and left standing in `code/species_7d75/`**, which is the copy a successor
> re-runs: `t3_bidigare.py` still headed T3d *"three are controls"*; the instrument README
> still read control (ii)'s counts as measuring *"how differently"* the two products behave;
> and `t4_one_operation.py` / `t6_fock_and_record.py` still printed the identification with the
> **character ring of `S_n`** unmarked, inside runs ending `TOTAL BAD: 0`. mg-6f61's
> `check_doc.py` could not have caught any of it — **it reads this file and nothing else.**
> All three are repaired at source, **T3d's count and control (ii)'s set equality are now
> COMPUTED rather than restated**, and `w3_scope.py` is the checker for the instrument: it
> reports **12 problems** against the pre-repair tree and **0** now. **No claim in this
> document is softened by any of it** — one is strengthened (§5, control (ii)).

**What this document is.** Daniel asked a question that two prior tickets did not answer.
mg-ebd8 and mg-af28 both answered *"does our construction reproduce `S_n` representation
theory"*, and the answer is no. He had already excluded that reading. His question, in his
own words:

> *"this poset quotient stuff should give us an intuition that perhaps there's a categorical
> core behind `S_n` rep theory and that we could reframe that subject. Then there might be a
> more general link to posets even though the naive application of group reps wouldn't
> apply: bc they both could be explained by the same categorical operation"*

and, refining it four minutes later:

> *"my intuition is that the categorical feature that matters here is the **grading +
> quotients** which form the basis of partitions in the `S_n` case and quotient posets in
> the poset case"*

**Scope, and it is the whole of the scope.** This is a **locating exercise**. It develops no
mathematics. Every relationship is reduced to **instance / special case / generalisation /
adjacent / no contact**, with a reason. Every identification is tested as an **equality**
built from published definitions rather than asserted as a resemblance. Where I did not find
something I say *"not located"*, which is a statement about my search and not about the
literature. There is **no publishability verdict and no novelty claim** here.

---

## 0. THE HEADLINE

**Yes. There is one categorical operation, it is named, it is the founding morphism of the
species/Hopf-monoid programme, and both of Daniel's cases are values of a single formula.**

> **The operation is `faces ↦ flats` — the support map — which linearised is
> `A ↦ A/rad(A)`.**
>
> Aguiar–Mahajan, *Monoidal Functors, Species and Hopf Algebras*, §10.10:
> *"Let `A` be the algebra of faces `Σ[I]`, and let `J` be its Jacobson radical. Bidigare
> [45] showed that `J` is precisely the kernel of its support map. This result was
> generalized to left regular bands by Brown [70] … Thus, `A/J` is the algebra of flats
> `Π[I]`, and the quotient map is the support map."*
>
> Applied to the faces lying in the **braid cone of a poset `P`**, and combined with passage
> to the symmetry of that cone, it reads
>
> **`( k F(P) )^{Aut(P)} / rad  =  k^{ AC(P) / Aut(P) }`**
>
> and Daniel's two cases are two rows of that one identity:
>
> * **`Aut(P)` trivial** → `k F(P)/rad = k^{AC(P)}`, indexed by the **quotients of `P`**.
>   *[the poset-quotient story]*
> * **`P` the antichain, `Aut(P) = S_n`** → the left side is **Solomon's descent algebra**
>   and the right side is `k^{Π_n/S_n}`, indexed by the **integer partitions of `n`**.
>   *[the `S_n` story — **and the last step of it, from `k^{Π_n/S_n}` to `S_n`'s character
>   ring, is ledger **S4**: CITED to Solomon and to Garsia–Reutenauer/Atkinson, and NOT
>   VERIFIED here or by the audit. See item 4 below.** (marked, mg-6f61)]*

**Measured, not asserted.** The identity holds on **all 87 poset isomorphism classes to
`n ≤ 5`**, with 0 failures of closure, 0 of well-definedness, 0 of surjectivity and 0 of
nilpotency (`out_t4_one_operation.txt`, T4a/T4b; 4 classes at `n = 5` skipped for the
nilpotency step only, over a `dim ≤ 90` cap, and tested for everything else). The antichain
row reads: `|Σ_n| = 1, 3, 13, 75, 541`; `dim (kΣ_n)^{S_n} = 1, 2, 4, 8, 16 = 2^{n-1}`;
`|Π_n/S_n| = 1, 2, 3, 5, 7 = p(n)` — 0 bad (T4c).

> **AND IT IS A THEOREM, NOT ONLY A MEASUREMENT (mg-6f61, on mg-a61f's X2 — this document
> UNDER-claimed its own headline in four places).** The identity is a **three-line corollary
> of Aguiar–Mahajan §10.10, which this document quotes in full**, plus the Reynolds operator:
> `G` acts on `A = kF(P)` by algebra automorphisms and `|G|` is invertible in characteristic
> 0, so `(−)^G` is exact; applying it to `0 → rad A → A → k^{AC} → 0` gives
> `A^G/(rad A)^G = k^{AC/G}`, and `(rad A)^G` is a nilpotent ideal of `A^G` whose quotient is
> semisimple, so it **is** `rad(A^G)`. **Both steps checked exactly over `Q` on all 24 classes
> to `n ≤ 4`** (mg-a61f A1d), and the argument has **no `n` dependence at all**. mg-a61f also
> re-measured it through the **trace form**: **87 of 87 classes to `n ≤ 5` with no size cap**,
> closing the 4 exemptions above, and **179 of 179 tested classes out of sample at `n = 6`**.
>
> **So `n ≤ 5` and the `dim ≤ 90` cap are limits of this ticket's instrument, not of the
> statement**, and every hedge on **S1**, **S12**, §6 item 6 and §10 item 2 is weaker than the
> evidence. **DO NOT FILE THE SUCCESSOR LITERATURE SEARCH** that §10 item 2 asks for: there is
> nothing missing for it to find, so it would return *"no antecedent located"* — which reads
> as a negative result about the literature when it is a fact about the routing. If a
> successor is filed anyway (Saliola and Commins remain worth reading on their own account,
> §7 item 3), **its brief must state that §2.3 is already located as a corollary, so that a
> null result cannot be mistaken for a finding.**

**And the `S_n` half is Bidigare's theorem, which mg-af28 named as *"the documented route"*
and did not follow. This ticket follows it.** Aguiar–Mahajan's Theorem 10.13 — *"(Bidigare).
The descent algebra is isomorphic to `(Σ[n]^{S_n})^{op}`"* — is **rebuilt here from the two
definitions and compared structure constant by structure constant**, the descent algebra
inside `kS_n` from permutations and their descent sets, the invariant algebra inside `kΣ_n`
from set compositions, sharing no code. Four candidate identifications were run —
{isomorphism, anti-isomorphism} × {two composition conventions} — and **exactly two hold and
two fail**, so the comparison is discriminating. The two that hold are the two that say
*anti-isomorphism*, which is what the theorem says (`out_t3_bidigare.txt`, T3d: 0
mismatching structure constants at `n ≤ 5` for those two; 472 mismatches at `n = 5` for each
of the other two). **The four columns are TWO statements each computed twice, not four —
convention B is identically the opposite algebra of convention A — so this is ONE control,
run twice, and it fires (corrected mg-6f61; §2.2).**

**Daniel's specification is met on every point, including the one he flagged as the cheap
falsifier.**

| his words | what it is | checked |
|---|---|---|
| *"grading"* | the **species degree**: a species is a functor from finite sets and bijections, so degree `n` is the value on an `n`-set | T1, T5 |
| *"quotients … which form the basis of partitions in the `S_n` case"* | the **flats** `Π[n]` = set partitions of `[n]`, which are the quotients of the antichain | T1d, 0 bad |
| *"and quotient posets in the poset case"* | `AC(P)`, the partitions of `P` with acyclic quotient — the support semilattice of `F(P)` | T2a, two routes, 0 bad |
| *"grading is a constraint, so use it as one"* | applied **first**; `AC(P) ⊆ Π[n]` for all 242 labelled posets to `n ≤ 4`, 0 bad | T1e |
| *"the `S_n` side is almost certainly the Frobenius characteristic"* | it is: **`K(Π) = Sym`**, whose degree-`n` component is `⊕_n R(S_n)` with the integer partitions as basis | §4, **CITED, NOT VERIFIED HERE — ledger S5** *(marked, mg-6f61)* |
| *"index by quotients, then take coinvariants of the grading"* | this is the **bosonic Fock functor** `K(p) = ⊕_n p[n]_{S_n}`, and it is exactly the named operation he was reaching for | §4, cited |

**And the Bell(n)-vs-p(n) gap — the one thing pm-onethird's hypothesis had to explain — is
not a discrepancy at all. It is the difference between the two Fock functors applied to one
species.** `dim K̄(Π)_n = |Π[n]| = Bell(n)` (symmetric functions in **noncommuting**
variables); `dim K(Π)_n = |Π[n]/S_n| = p(n)` (symmetric functions). Measured to `n = 7`, 0
bad (T6a). Aguiar–Mahajan §17.5, quoting their own §17.4: *"`K̄(Π)` is the algebra of
symmetric functions in noncommuting variables and `K(Π)` is the familiar Hopf algebra of
symmetric functions."*

**Four things that must be said in the same breath as the yes, because each of them limits
it.** *(The fourth was added by the repair mg-6f61; it was stated correctly in §3 and in
ledger **S4** from the start and was missing from §0, which is the part that gets quoted.)*

1. **What the `S_n` instance recovers is the CHARACTER RING, not the module category.** The
   semisimple quotient of the descent algebra is a **commutative split** algebra of dimension
   `p(n)` — all its irreducibles are one-dimensional. It carries the *index set* and, via
   Solomon's homomorphism, the *ring*; it does not carry `S^λ`, `f^λ`, or any multiplicity.
   §6.1.
2. **`S_n` representation theory is not, in species, an *instance* of an operation. It is the
   AMBIENT CATEGORY.** A vector species *is* a sequence of `S_n`-modules. So the honest form
   of the yes is: *one operation, taking place in a category whose objects are `S_n`
   representations, with our poset story as one value and the `S_n` character ring as
   another after coinvariants.* §6.2.
3. **Our construction is not, as it stands, an object of that programme — it is a
   sub-object of one, and placing it properly is work this ticket does not do.** §7 says
   exactly what that work is.
4. **THE `S_n` HALF OF THE CORRESPONDENCE IS NOT VERIFIED HERE.** *(added by mg-6f61.)*
   What is measured on the `S_n` side is that the semisimple quotient of `(kΣ_n)^{S_n}` has
   dimension `p(n)` and is indexed by `Π_n/S_n`, and that Bidigare's anti-isomorphism holds
   structure constant by structure constant to `n ≤ 5` (T3, reproduced entry for entry by
   mg-a61f from disjoint code). **The step from `k^{Π_n/S_n}` to *the character ring of
   `S_n`* is ledger S4 — cited to Solomon and to Garsia–Reutenauer/Atkinson, neither of
   which was read, here or by the audit.** The **Fock-functor statement of §4 is likewise
   *located* in the literature and not re-derived**: what is measured is `Bell(n)` against
   `p(n)`; that those are `K̄` and `K` of one species is Joyal's and Aguiar–Mahajan's
   sentence, quoted. **Being located is a real result. It is not the same as being
   verified**, and the two must not be read as one — the poset half of §0 is confirmed
   (trace form, 87/87 with no size cap, 179/179 out of sample at `n = 6`; mg-a61f A1a/A1c);
   the `S_n` half is not.

**The one place where the record was wrong, and it is on the negative side, which is where
this arc keeps breaking.** mg-af28 rejected the towers-of-algebras programme because block
concatenation fails **Bergeron–Li axiom (2)**, which demands `1_m ⊗ 1_n ↦ 1_{m+n}`. That
rejection **stands** and is reproduced here (0 of 529 labelled pairs unital, T6c). But **that
demand is not an axiom of a Hopf monoid in species**: the unit lives only in degree `∅`, and
`μ_{S,T}` carries no unitality requirement at all. The very same concatenation **is**
`μ_{S,T}`, and ~~it passes every Hopf-monoid axiom with 0 failures on 4 399 basis elements
(T5)~~ — **corrected (mg-6f61): what 4 399 basis elements measure is CLOSURE, and only
closure.** Of §5's five columns, **two can fail on our subspecies and three cannot**: with the
operations held fixed, associativity, coassociativity and compatibility return 0 for a
collection closed under nothing, for one closed under half the operations, and for an
arbitrary predicate — they are identities of the **ambient** Hadamard product, verified once,
not 4 399 times. Each of the five is nevertheless **demonstrated to be capable of failing**,
under mutations whose outcome was written down before the run
(`code/species_repair_6f61/out_r2_columns.txt`, 45 predicted cells, 2 missed and both
reported). **The negative that closed the tower door does not close this one, and nothing in
the record separated the two.** §8.

---

## 1. WHAT A SPECIES IS, AND WHY THE QUESTION IS WELL-POSED THERE

Aguiar–Mahajan, Definition 8.1, verbatim:

> *"A set species is a functor `Set^× → Set`. A vector species is a functor `Set^× → Vec`."*

where `Set^×` is defined immediately above as the category *"whose objects are finite sets
and whose morphisms are bijections between finite sets"*.

That is the whole of the grading Daniel names: the **degree** of a species is the finite set
it is evaluated on, and a vector species is the same data as a sequence of `S_n`-modules,
one for each `n`. So *"grading + quotients, with the degree-`n` basis indexed by quotients
of the degree-`n` object"* is a specification that either is or is not met by a given
species, and it is decidable.

Two species carry the whole story.

* **`Σ`, the species of set compositions** = the **faces** of the braid arrangement. A face
  `(B_1, …, B_k)` is the set of `x ∈ ℝ^I` constant on each block with values increasing in
  the block index.
* **`Π`, the species of set partitions** = the **flats** of the braid arrangement.

and one map between them: **`supp : Σ → Π`, forget the order of the blocks.** That is the
operation.

**Our objects are exactly the restriction of these two to a cone.** For a poset `P` on `[n]`
put

    C(P) = { x ∈ ℝ^n : x_i ≤ x_j whenever i < j in P }.

Then `F(P)` is the set of faces lying in `C(P)`, and `AC(P) = supp(F(P))`.

**CORRECTED QUOTATION (mg-6f61).** The passage as mg-7d75 printed it —
~~*"Define a braid cone to be a cone in `(ℝ^I)/ℝ^I` cut out by inequalities of the form
`y(i) ≤ y(j)` for `i, j ∈ I`"*~~ — **is not the paper's text.** Aguiar–Ardila, *Hopf monoids
and generalized permutahedra*, §12, from a `pdftotext` extraction of the served PDF:

> *"Define a braid cone to be a cone in `(ℝ^I)* = ℝ^I` cut out by inequalities of the form
> `y(i) ≥ y(j)` for `i, j ∈ I`."*

Two divergences: `(ℝ^I)/ℝ^I` is a symbol-drop artefact and is not a well-formed expression;
and the paper's inequality runs the **other way**, so `C(P)` above is Aguiar–Ardila's braid
cone of the **opposite** order (equivalently, of `P` after `i ↔ j`). Neither changes anything
this document does with the quote. Their Table 1 pairs the combinatorial objects **posets**
with the polytopes **braid cones**. Marshall–Martin, *Hopf monoids of set families*,
Australas. J. Combin. **92**(3) (2025) 419–449, §2.1: *"geometric realization gives a
bijection between preposets and convex unions of cones of the braid arrangement."* And
Aguiar–Mahajan's own chapter introduction: *"posets can be viewed as appropriate unions of
chambers (top dimensional cones, to be precise) in the Coxeter complex of type A."*

> **⚠ TERMINOLOGY COLLISION — "braid cone" denotes two different objects in the two sources
> this section quotes, and they are the two objects this ticket is about.** *(Named here by
> mg-6f61 so the next reader does not re-import it.)* Marshall–Martin's very next sentence,
> which mg-7d75's quotation stopped one sentence short of, is:
>
> > *"(These objects are called "braid cones" in [14], but we reserve that term for single
> > cones of the braid arrangement.)"*
>
> and [14] is Aguiar–Ardila. So:
>
> | source | *"braid cone"* means | in our notation |
> |---|---|---|
> | **Aguiar–Ardila §12** | a cone cut out by `y(i) ≥ y(j)` inequalities — a **union** of cones of the braid arrangement | **`C(P)`** |
> | **Marshall–Martin §2.1** | a **single** cone of the braid arrangement | **an element of `F(P)`** |
>
> **`C(P)` and an element of `F(P)` are not the same kind of object** — one is the cone the
> poset cuts out, the other is a face lying inside it — and this document uses `F(P)` and
> `C(P)` for exactly that distinction. **Usage fixed accordingly:** where this document says
> *"braid cone"* unqualified it means **`C(P)`, Aguiar–Ardila's sense**; a single cone of the
> arrangement is called a **face** throughout and never a braid cone.
>
> **Consequence for the count below.** Marshall–Martin is not a third *agreement* about the
> term; it is a source recording that the term is **not standard**. Two sources use the
> dictionary; the third flags the word.

**So the dictionary `poset ↔ braid cone` on which this whole ticket turns is not ours; it is
stated in three independent published sources, one of them the book named in the brief** —
~~as three independent agreements about the term~~ **corrected (mg-6f61): as two sources
using the term for `C(P)` and a third that uses it for a single face and says so in the
sentence after the one quoted. The dictionary `poset ↔ cone` is unaffected; the word is what
is contested.**

---

## 2. THE OPERATION, AND BOTH INSTANCES, ON ONE INSTRUMENT

### 2.1 The operation, on our side (T2)

`Φ = (χ_X)_{X ∈ AC(P)} : kF(P) → k^{AC(P)}`, where `χ_X(F) = 1` iff `X` refines `supp(F)`.
Measured on every poset class to `n ≤ 5` with `|F(P)| ≤ 80`:

| `n` | classes | tested | skipped | `AC` two routes differ | `supp` not a hom | `Φ` not onto | kernel not nilpotent |
|---|---|---|---|---|---|---|---|
| 1–4 | 24 | 24 | 0 | 0 | 0 | 0 | 0 |
| 5 | 63 | 39 | 24 | 0 | 0 | 0 | 0 |

Surjective with nilpotent kernel gives `kF(P)/rad = k^{AC(P)}` with **no trace form and no
citation**. This re-anchors mg-af28's B5 and mg-6ad0's A4a from code that shares nothing
with either. **Control:** the same nilpotency routine, fed the kernel enlarged by an
idempotent, reports *not nilpotent* on all 23 classes tested — so the routine discriminates
(T2d).

### 2.2 The operation, on the `S_n` side (T3) — Bidigare, tested as an equality

Both algebras built from their definitions, no shared code:

* `(kΣ_n)^{S_n}`: the `S_n`-orbit sums of set compositions. Orbits **are** the compositions
  of `n` (T3a, 0 bad), the orbit sums **do** span a subalgebra (T3b: products constant on
  orbits, 0 exceptions at every `n ≤ 5`), and `dim = 2^{n-1}`.
* `Sol(S_n) = span{ d_T : T ⊆ [n-1] }`, `d_T = Σ_{des(w) ⊆ T} w`, exactly as Aguiar–Mahajan
  write it at (10.43). Closed under multiplication under both composition conventions
  (T3c, 0 bad), `dim = 2^{n-1}`, and `|{w : des(w) ⊆ T(α)}| = |O_α|` for every composition
  `α` (0 bad).

The comparison, `O_α ↔ d_{T(α)}` with `T(α)` the partial sums:

| `n` | iso/A | anti/A | iso/B | anti/B |
|---|---|---|---|---|
| 3 | 4 | **0** | **0** | 4 |
| 4 | 54 | **0** | **0** | 54 |
| 5 | 472 | **0** | **0** | 472 |

*(entries are counts of mismatching structure constants)*

**Two of four hold, two fail.** The identification is an **anti-isomorphism**, which is what
Theorem 10.13 states. ~~Three of the four columns are the control, and they fire.~~

> **CORRECTED (mg-6f61, on mg-a61f's X4): the four columns are TWO STATEMENTS, EACH COMPUTED
> TWICE — so there is ONE control, run twice, not three.** Conventions A and B differ only by
> the order of composition in `S_n`, so `c^γ_{α,β}(Sol, B) = c^γ_{β,α}(Sol, A)` identically —
> **0 mismatches at every `n ≤ 5`** (mg-a61f A2d). Hence `{anti/A, iso/B}` is one statement
> and it holds, and `{iso/A, anti/B}` is one statement and it fails. `iso/B`, listed above as
> a control, is the surviving identification in a mirror.
>
> **What survives, and it is the whole substance:** the comparison **is** discriminating —
> *isomorphism* is separated from *anti-isomorphism* decisively, by **472 mismatching
> structure constants at `n = 5`** — and the theorem itself is reproduced exactly, entry for
> entry, by mg-a61f's disjoint instrument. **Only the control COUNT was overstated.**
> Read: *one control, computed twice, and it fires.*
>
> **AND IT IS NOW COMPUTED, NOT RESTATED (mg-f8fa).** `t3_bidigare.py` went on printing
> *"three are controls"* after this box was written; it now carries a **T3e** that measures
> `c^U_{S,T}(Sol, B) = c^U_{T,S}(Sol, A)` — **0 mismatches at every `n ≤ 5`** — and **fails**
> if it is false. Its own control, the un-swapped comparison, must fire and does: **2, 26,
> 170 at `n = 3, 4, 5`**, and cannot fire at `n ≤ 2` where `kS_n` is commutative. Both
> columns reproduce independently in `code/species_remainder_f8fa/w1_opposite.py`.

### 2.3 Both instances, one identity (T4)

For every poset class `P` at `n ≤ 5`, with `G = Aut(P)`:

* the `G`-orbit sums span a subalgebra of `kF(P)` — **0 failures**;
* the induced map to functions on `AC(P)/G` is well defined (independent of the chosen
  representative of each orbit) — **0 failures**;
* it is onto — **0 failures**;
* its kernel is nilpotent — **0 failures** (4 of 63 classes at `n = 5` over the `dim ≤ 90`
  cap, tested for the other three properties).

Hence `dim (kF(P))^{Aut(P)}/rad = |AC(P)/Aut(P)|` throughout. **And it holds for every `n`,
because it is a corollary of the theorem quoted in §0 rather than a measurement — see the
proof boxed there (mg-6f61). The caps above bound this instrument, not the identity.**
**The antichain row:**

| `n` | `|Σ_n|` | `dim (kΣ_n)^{S_n}` | `2^{n-1}` | `|Π_n/S_n|` | `p(n)` |
|---|---|---|---|---|---|
| 3 | 13 | 4 | 4 | 3 | 3 |
| 4 | 75 | 8 | 8 | 5 | 5 |
| 5 | 541 | 16 | 16 | 7 | 7 |

**The trivial-`Aut` rows:** 19 of the 63 classes at `n = 5` have `Aut(P) = 1`, and for every
one of them `|AC(P)/Aut(P)| = |AC(P)|` — the identity degenerates to `kF(P)/rad = k^{AC(P)}`,
which is §2.1.

**Control (T4d).** Replacing `Aut(P)` by the full `S_n` must break, because `S_n` does not
preserve the cone. It does: on all 20 non-antichain classes to `n ≤ 4`, some `S_n`-image of
a face of `F(P)` leaves `F(P)`. So the group in the identity is doing work.

**This is the answer to Daniel's question, and it is one table.** The two stories are not
analogous; they are the same measurement at two values of one argument, and what varies
between them is the size of the symmetry group of the cone.

---

## 3. THE STEP FROM `k^{Π_n/S_n}` TO `S_n` REPRESENTATION THEORY — CITED, NOT DERIVED

`k^{Π_n/S_n}` is measured here to be the semisimple quotient of the invariant algebra, and
`Π_n/S_n` is measured to be the integer partitions of `n` (T1b, 0 bad, orbits computed with
actual permutations and the block-size invariant **checked** to be complete rather than
assumed). The identification of that with the character ring of `S_n` is **Solomon's
theorem and I did not re-derive it**:

* Solomon (1976) constructs a homomorphism from the descent algebra of a finite Coxeter
  group to its character ring; for `S_n` **the natural map from the descent algebra to the
  character ring is a surjection whose kernel is the Jacobson radical** — *stated from the
  secondary literature; I did not read Solomon's paper*.
* Garsia–Reutenauer / Atkinson: **the irreducible representations of the descent algebra are
  all one-dimensional and are naturally indexed by the conjugacy classes of parabolic
  subgroups** — for `S_n`, the Young subgroups up to conjugacy, i.e. the integer partitions
  — *also stated from the secondary literature and not read in the original*.

**What is measured here and what is cited must not be blurred.** Measured: the semisimple
quotient has dimension `p(n)` and is indexed by `Π_n/S_n`. Cited: that this quotient *is*
the character ring. **Not established here:** that the labelling by block-size partitions
agrees with the labelling by cycle types. Both index sets are the integer partitions of `n`
and both have `p(n)` elements (T1b, T1c), but the two labellings agreeing is a statement
about Solomon's map that I did not test.

> **THE BOUNDARY, STATED ONCE AND NAMED (mg-6f61).** This section is **ledger S4**, and S4
> is **the whole `S_n` half of §0's headline**. The two sources it rests on are
> **Solomon (1976)** and **Garsia–Reutenauer / Atkinson**. **Neither was fetched and neither
> was read** — not by mg-7d75, and not by the independent audit mg-a61f, which states the
> same limitation at its §12 item 1 and adds nothing to it.
>
> | half of the correspondence | status |
> |---|---|
> | **the poset half** | **CONFIRMED, independently.** Re-measured by mg-a61f through the trace form — the one route this ticket says it did not use — **87 of 87 classes to `n ≤ 5` with no size cap** and **179 of 179 tested classes out of sample at `n = 6`**, two primes agreeing on every class; and proved outright as a corollary (§0) |
> | **the `S_n` half** | **NOT INDEPENDENTLY VERIFIED.** What is measured is Bidigare's anti-isomorphism to `n ≤ 5` (T3, reproduced entry for entry) and `dim = p(n)` indexed by `Π_n/S_n`. The step from there to *the character ring* is **located in the literature and cited to two unread sources** |
>
> **Being located is a real result. Presenting it as verified is not**, and the difference is
> the difference between *"someone has proved this"* and *"we have checked this"*. The same
> distinction applies to §4's Fock functors, which are **quoted, not evaluated here**.
>
> **AND THE BOUNDARY IS NOW STATED IN THE INSTRUMENT TOO (mg-f8fa).** `t4_one_operation.py`
> printed `Sol(S_n)/rad = k^{Π_n/S_n} = the character ring of S_n` and
> `t6_fock_and_record.py` printed the `K(Π)` half — **both unmarked, inside runs ending
> `TOTAL BAD: 0`**, so a reader of the output had nothing telling them the two equalities in
> that line are not of the same kind. Both now name **S4** (and **S5**), both unread sources,
> and the specific untested link: that **Solomon's labelling by cycle types agrees with the
> orbit labelling by block sizes** is not checked anywhere.
> `code/species_remainder_f8fa/w3_scope.py` enforces it over **every** occurrence in
> `code/species_7d75` — eight of them — and fails if a ninth is added unmarked.

---

## 4. `Bell(n)` vs `p(n)`: THE GAP IS THE TWO FOCK FUNCTORS

Daniel: *"integer partitions are the **orbits** under the `S_n`-action, i.e. what you get
after passing to coinvariants. Taking `S_n`-coinvariants of a species is a standard
operation."* It is, and it is the **bosonic Fock functor**. Joyal, in his foreword to
Aguiar–Mahajan, defines it:

> *"By definition, we have `K(p) = ⊕_n p[n]_{S_n}`, where `p[n]_{S_n}` denotes the space of
> `S_n` coinvariants of `p[n]`."*

and, three lines below that passage in the same foreword, in clean prose with no dropped
symbols — **the sentence mg-7d75 reconstructed §17.5 to get, and did not need to
(mg-6f61)**:

> *"The Hopf algebra `K(Π)` is the algebra of symmetric functions `Λ` (when `k` is of
> characteristic 0), and it is self dual, since `Π` is self-dual."*

Aguiar–Mahajan §17.5 records the two values as well, and **mg-7d75 printed it wrong**:
~~*"Recall from Section 17.4 that `K̄(Π)` is the algebra of symmetric functions in
noncommuting variables and `K(Π)` is the familiar Hopf algebra of symmetric functions"*~~.
**The book's species is `Π*` in both slots.** As `pdftotext` serves it:

> *"Recall from Section 17.4 that `K(Π*)` is the algebra of symmetric functions in
> noncommuting variables and `K(Π*)` is the familiar Hopf algebra of symmetric functions."*

*(The two `K`s are distinguished in the book by an overline on the first; no extraction
available here renders it, so the overline above is supplied and marked rather than quoted.)*
The `Π`-vs-`Π*` difference is **mathematically harmless and the book says why on the same
page**: §17.4.1, *"Since `Π` and `Π∗` are isomorphic"*.

Measured (T6a), 0 bad:

| `n` | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| `dim K̄(Π)_n = |Π[n]| = Bell(n)` | 1 | 2 | 5 | 15 | 52 | 203 | 877 |
| `dim K(Π)_n = |Π[n]/S_n| = p(n)` | 1 | 2 | 3 | 5 | 7 | 11 | 15 |

**So the objection pm-onethird raised against its own hypothesis dissolves.** There was never
a count to reconcile: `Bell(n)` and `p(n)` are the dimensions of the same species under the
**full** and the **bosonic** Fock functor, and the second is precisely *"pass to orbits under
the symmetry"*. The hypothesis in the brief — *"index the representation theory by the
quotient lattice of the underlying object, with `S_n` theory recovered by passing to orbits
under the symmetry"* — **is correct in shape**, and every piece of it has a published name.

**And "has a published name" is the whole of what §4 establishes (mg-6f61).** `Bell(n)` and
`p(n)` are measured here to `n = 7`. That they are `K̄` and `K` of one species is **quoted,
not re-derived** — the Fock functors are Joyal's definition and Aguiar–Mahajan's table, and
this ticket evaluates neither functor on `Π` from its definition. **Located, not verified.**

**WHICH QUOTATION DIVERGENCES WERE ANTICIPATED, AND WHICH WERE NOT (mg-6f61).** mg-a61f
executed §10 item 1's own attack — all thirteen quotations re-extracted with poppler's
`pdftotext` from all three PDFs, **11 verbatim, 2 divergent, 1 truncated**. The distinction
matters more than the count:

| divergence | pre-flagged? | consequence |
|---|---|---|
| **AM §17.5**, species `Π` where the book has `Π*` | **YES** — §10 item 1 says outright *"the species names in that quote are my inference from the surrounding text"* | none: §17.4.1 says `Π ≅ Π*`. A predicted divergence in a passage the document already labelled as reconstructed |
| **Aguiar–Ardila §12**, `(ℝ^I)/ℝ^I` and a flipped inequality | **NO** | none mathematically — but it is the **same defect** §10 item 1 describes, in a **second place the pre-file did not name**, and it was found only because the check was *executed* rather than asserted |
| **Marshall–Martin §2.1**, stopped one sentence short | **NO** | the omitted sentence is the terminology collision above, and it costs the *"three independent sources"* count |

**An unpredicted divergence in an executed check is worth more attention than a predicted
one.** The predicted one confirms the document knew its extraction was lossy. The two
unpredicted ones are the measurement of **how far** that lossiness reached — which is
precisely what a pre-file cannot tell you, because a pre-file names the places its author
already suspects. See §14.

---

## 5. DOES OUR CONSTRUCTION CARRY THE STRUCTURE? (T5)

Daniel's point 1 asked this directly, with axioms rather than analogy. The question is
decidable, and this is the decision.

**The published inputs, all quoted from Aguiar–Mahajan:**

* §13.1.1, **the Hopf monoid of posets `P`**: *"Given a finite set `I`, let `P[I]` be the
  vector space with basis the set of all partial orders on `I`."* Product: disjoint union.
  Coproduct via §13.4.2, which records *"`e_{S,T}(p) = 0 ⟺ S` is a lower set of `p`"* and
  *"the Hopf monoid of posets of Section 13.1.1 is `P_0`"* — i.e. `Δ_{S,T}(p) = p|_S ⊗ p|_T`
  when `S` is a lower set of `p`, and `0` otherwise.
* Chapter 12: the Hopf monoids of **set compositions** and **set partitions**, product
  concatenation / disjoint union, coproduct restriction.
* §8.13: *"the Hadamard product `h₁ × h₂` of two Hopf monoids `h₁` and `h₂` is again a Hopf
  monoid."*
* Chapter 11: *"a connected bimonoid in species is automatically a Hopf monoid."*

**The two candidate subspecies:**

    F[I]  = { (p, F) : p a poset on I, F a face in the braid cone of p }   ⊆  P × Σ
    AC[I] = { (p, X) : p a poset on I, X ∈ AC(p) }                        ⊆  P × Π

**The measurement**, exhaustive on the ground set `[4]`:

| species | basis elts on `[4]` | product closure | coproduct closure | assoc | coassoc | compatibility |
|---|---|---|---|---|---|---|
| `F` | 4 399 | 0 | 0 | 0 | 0 | 0 |
| `AC` | 2 685 | 0 | 0 | 0 | 0 | 0 |

*(every column is a **failure** count)*. Both are connected (`h[∅]` one-dimensional), so by
the Chapter 11 statement the bimonoid axioms are the whole of what has to be checked. And
the operation of §2 lifts: **`supp : F → AC`, `(p,F) ↦ (p, supp F)`, is a morphism of
bimonoids on the nose** — 0 failures on lands-in, 0 on the product, 0 on the coproduct
(T5d).

**WHICH OF THOSE FIVE COLUMNS CAN FAIL — stated per column and demonstrated (mg-6f61,
`code/species_repair_6f61/out_r2_columns.txt`).** A zero is evidence only where a non-zero
was available. Two axes were run: the **collection** varied with the operations held fixed,
and the **operations** varied with the collection held fixed at `F`. Every one of the 45
cells carries an outcome written down **before** the run.

| column | can it fail by varying the COLLECTION? | can it fail by varying the OPERATIONS? | what our 0 is evidence of |
|---|---|---|---|
| product closure | **YES** — 216 on a subset closed under nothing, 396 on chains-only | yes | **our subspecies** |
| coproduct closure | **YES** — 6 988, and 12 186 on a parity predicate | yes | **our subspecies** |
| associativity | **NO** — pinned at 0 on all five collections tried | YES — 12 192 under a non-associative product | the **ambient** operations |
| coassociativity | **NO** — pinned at 0 | YES — 266 459 under a swapped coproduct | the **ambient** operations |
| compatibility | **NO** — pinned at 0 | YES — 3 408 under a block-merging product | the **ambient** operations |

The five collections: `F` itself; the **full ambient** `P × Σ` (16 425 elements on `[4]`);
**`F`-opposite**, the poset paired with the faces of the *opposite* cone; **`F`-broken**,
every second element, closed under nothing; and **even-block-count**, an arbitrary predicate.
Associativity of concatenation and coassociativity of restriction are identities of tuples
and of sets, inherited from the Hadamard product, so **no choice of sub-collection can move
those three columns**. They are verified **once**, not 4 399 times.

**So the honest count is two columns, not five**, and 4 399 is the size of the degree-4
component of the ambient rather than a number of independent tests. **And the two columns
that can fail return 0 for the full ambient and for the deliberately wrong pairing as well
as for ours**, so what they establish is **closure**, not identification. Both closure
columns do respond to something — that is what the 216 / 6 988 / 396 / 12 186 rows show —
and the response is to closure alone.

*Two of the 45 predicted cells missed, and both are kept on the record rather than
re-written: the even-block-count predicate turned out to be closed under the product (block
counts **add** under concatenation, so parity survives — an arbitrary-looking predicate
passing that column, which is the section's own point arriving by an accident I did not
foresee), and swapping the two tensor factors of the coproduct turned out to be a symmetry
of the compatibility axiom, so it fires on coassociativity and not on compatibility.*

**Four controls; two fire, two do not, and the two that do not are reported rather than
replaced.**

| control | result |
|---|---|
| (i) drop the lower-set condition from the coproduct | **does not fire.** And correctly so: Aguiar–Mahajan §13.4.2's family `R_q` has the lower-set condition as its `q = 0` member and the unrestricted coproduct as `q = 1`, and both are Hopf monoids. The corruption produced a *different published Hopf monoid*, not a broken one |
| (ii) the **Tits product** of faces in place of concatenation | ~~**fires hard**: 1 442 closure, 252 associativity, 11 020 compatibility failures~~ **fires on a TYPE MISMATCH, not a near miss** *(corrected, mg-6f61, on mg-a61f's X5)*. The 1 442 product-closure failures are **exactly** the 1 442 of 11 301 pairs whose two factors have **disjoint non-empty ground sets**: `μ_{S,T}` takes factors on disjoint sets, the Tits product intersects blocks, and across disjoint sets every intersection is empty. The counts are not evidence of a near miss. **The conclusion drawn from this control is unaffected and is NOT withdrawn** — see below and §6 item 5 |
| (iii) reverse the order of concatenation | **does not fire**, because that is the opposite monoid structure, which is compatible with the same coproduct |
| (iv) replace *"`S` is a lower set"* by *"`S` is an antichain"* | **fires**: 75 512 coassociativity failures |
| **(v) merge the last block of `F` with the first block of `G`** *(added by mg-6f61)* | **fires on compatibility ALONE**: 0 product closure, 0 coproduct closure, 0 assoc, 0 coassoc, **3 408 compatibility**. It stays inside the cone and it is associative, so it is the isolated compatibility control the four above do not provide — mg-a61f's X5 shows that control (ii)'s 1 442 product failures are exactly the 1 442 disjoint-ground-set pairs, i.e. a type mismatch rather than a near miss |

**The honest reading, and it is narrower than the table looks.** A product-side control and a
coproduct-side control both fire, so the axioms are doing work. But what T5 establishes is
**closure of our two subspecies under published operations** — which is exactly the question
asked — and **not** that those operations are forced.

> **This paragraph was right, and §0 disagreed with it (mg-6f61).** The defect mg-a61f
> found — X3 — was not that this reading is wrong. It is that the same document's §0 said
> *"0 failures across 5 axioms on 4 399 basis elements"*, and **§0 is the part a successor
> quotes**. The repair brought §0 to this paragraph, not the other way round. A caveat that
> contradicts the headline of its own document is not a caveat; it is an unresolved
> disagreement with a reader-facing side and a buried side.

**And a statement of this shape is already in the literature, so T5 must not be read as
new.** Marshall–Martin (2025) prove that *any family of posets closed under disjoint union,
induced subposet and deletion of order filters gives rise to a Hopf submonoid of the Hopf
monoid of lattices of order ideals.* Their objects are the lattices `J(P)` and their
coproduct is a different one, so it is not the same statement; but it is the same *kind* of
statement about the same *kind* of family, and it was published before this ticket existed.
**Adjacent, and closer than anything else located.**

**Control (ii) is the most important line in this section**, because it forbids the reading
this ticket is most likely to be misquoted as supporting. **The product of the Hopf monoid
is concatenation. The product of our band — the one the walk runs on, the one all of
mg-ebd8's and mg-af28's spectral work uses — is the Tits product. They are different maps,
and the Tits product is not a Hopf-monoid product.** What sits inside the Hopf monoid is the
*underlying species* of faces-in-a-cone, not the band structure on it.

**AND THAT CONCLUSION SURVIVES THE CORRECTION TO ITS NUMBERS (mg-6f61).** mg-a61f's X5 shows
the 1 442 / 252 / 11 020 are weaker evidence than they look — the product-closure column
fires because the two maps have **different domains of definition**, not because the Tits
product nearly works. **The conclusion is right anyway, and for a better reason than the
counts: `μ_{S,T}` is defined on factors with disjoint ground sets, and on disjoint sets the
Tits product's block intersections are all empty.** It is a statement about the two maps'
types, which no count could strengthen and no re-count can weaken. **Nothing downstream that
cites "the band product is invisible to the Hopf structure" — mg-ebd8's and mg-af28's
spectral work, `λ₂`, `Δ_AT` — needs revising.**

**AND IT IS NOW MEASURED AS A SET EQUALITY, AT SOURCE (mg-f8fa).** The 1 442 failures and the
1 442 both-non-empty pairs are the **same pairs**, not merely the same count, and every one of
them returns the **empty composition** — checked in `t5` control (ii) itself and again from
disjoint code in `code/species_remainder_f8fa/w2_typemismatch.py`, four predictions written
before the run and four met. **Two controls make it a reading rather than a story:** a
type-**correct** corruption of the product (mg-6f61's control (v)) fails this column **0**
times, and control (ii) with its own guard removed fails it **11 300** of 11 301. **The column
is a type check. It is not a distance.** The instrument README had gone on describing the
counts as measuring *"how differently"* the two products behave — in its *"conventions that
have bitten this repo before"* section — and no longer does.

---

## 6. WHAT DOES **NOT** TRANSFER, ENUMERATED

Every item is a limitation on the yes in §0, and each is named with the measurement or the
citation that carries it.

1. **The `S_n` instance gives the character ring, not the modules.** The semisimple quotient
   is commutative of dimension `p(n)` (T4c) and the descent algebra's irreducibles are all
   one-dimensional (cited, §3). Nothing here produces `S^λ`, `f^λ`, a branching rule or a
   multiplicity. mg-af28's finding that our algebra has all irreducibles one-dimensional is
   **not** an obstruction that this framework removes — it is the same phenomenon on the
   other side too. **And "gives the character ring" is itself ledger S4: cited to Solomon
   and to Garsia–Reutenauer/Atkinson, neither read here or by the audit. §3** *(marked,
   mg-6f61)*.
2. **`S_n` representation theory is the ambient category, not an instance.** A vector species
   *is* a functor from finite sets and bijections, i.e. a sequence of `S_n`-modules. So the
   framework does not derive `S_n` rep theory from something more primitive; it takes it as
   the coefficient category and asks what structures live over it. This is the sharpest
   correction available to the framing of Daniel's question, and it *strengthens* rather
   than weakens the answer: the thing that generalises from `S_n` to posets in
   Aguiar–Mahajan's 2020 sequel is not the operation but the **category itself**. §9 row 4.
3. **The obvious map from our side to `Sym` fails, and it fails on the coproduct.** The
   candidate `AC → Π`, `(p, X) ↦ X`, commutes with the product (0 disagreements) and **not**
   with the coproduct (22 614 disagreements over the ground set `[4]`, T6d): `Π`'s coproduct
   is restriction and is never zero, ours is zero unless `S` is a lower set. So Daniel's
   point 2 — *"check whether the poset side maps into the same target"* — is answered **no**
   for the obvious candidate.
4. **The universal property that does apply does not discriminate.** Aguiar–Bergeron–Sottile:
   every connected graded Hopf algebra with a character maps uniquely to `QSym`. That applies
   to our side. It also applies to every other object in the class, which is why it
   identifies our object with nothing. *"Both land in one graded Hopf algebra by the same
   universal property"* is **true and empty**; the content is at the species level.
5. **The band structure is not carried by the Hopf monoid.** T5 control (ii), §5. The Tits
   product fails product closure, associativity and compatibility. So the walk, its
   eigenvalues, `λ₂`, and everything mg-ebd8 and mg-af28 measured are **not** functions of
   the Hopf-monoid structure. The Hopf monoid sees the faces; the band sees how they
   multiply.
   **THIS CONCLUSION SURVIVES THE REPAIR AND IS NOT WITHDRAWN (mg-6f61).** mg-a61f's X5
   corrects the *accounting* behind control (ii) — its 1 442 product-closure failures are
   exactly the 1 442 of 11 301 pairs whose two factors have **disjoint non-empty ground
   sets**, so the control fires on a **type mismatch** and not on a near miss (see §5). The
   numbers are weaker evidence than they look. **The conclusion they were cited for is
   right, and it rests on the structural fact rather than on the counts:** `μ_{S,T}` takes
   factors on **disjoint** sets and the Tits product intersects blocks, so across disjoint
   sets every intersection is empty — the two maps are of different kinds. **Nothing
   downstream that cites "the band product is invisible to the Hopf structure" needs
   revising.**
6. ~~**The `Aut(P)`-invariant identity of §2.3 is measured, not proved, and is stated for
   `n ≤ 5`.**~~ **CORRECTED (mg-6f61): it is PROVED, in three lines, from the theorem this
   document quotes in §0, and it has no `n` dependence.** It is the natural equivariant form
   of Bidigare's radical theorem, obtained from it by the Reynolds operator — see the boxed
   proof in §0. I did **not** locate it *stated* in that generality in the literature, and
   that remains a report on a search (§9 row 6); but **the statement is not waiting on the
   search**, and §10 item 2's errand is closed. What is genuinely limited here is the
   *instrument*: `t4` runs to `n ≤ 5` with a `dim ≤ 90` cap. mg-a61f's disjoint instrument
   removes both.

---

## 7. WHAT IT WOULD TAKE TO PLACE OUR CONSTRUCTION INSIDE THE FRAMEWORK

The brief asked for this explicitly. Four steps, in order of how much they are worth, none
of them taken here.

1. **Read Aguiar–Mahajan, *Bimonoids for Hyperplane Arrangements* (CUP, Encyclopedia of
   Mathematics and its Applications 173, 2020).** This is the book the whole question points
   at and **I did not read it** — I have its publisher description only: *"The goal of this
   monograph is to develop Hopf theory in a new setting which features centrally a real
   hyperplane arrangement. The new theory is parallel to the classical theory of connected
   Hopf algebras, and relates to it when specialized to the braid arrangement … how these
   notions may be viewed as an extension of corresponding notions in Joyal species from
   braid arrangements to an arbitrary arrangement."* **If a poset-indexed family of cones in
   the braid arrangement has a home in that programme, it is in this book, and locating it
   is the single highest-value next action available.** Their earlier *Topics in Hyperplane
   Arrangements* (AMS Surveys 226, 2017) is described as treating *"faces, flats, chambers,
   cones, gallery intervals, lunes"* — and Brown calls our object a lune (§4.1 of Brown
   2000, per mg-ebd8). **A ticket that reads the lunes chapter of AM 2017 and the species
   chapter of AM 2020 against our `F(P)` is the correct successor to this one.**
2. **Decide whether the Hopf submonoid of §5 is one already in the literature.** The
   candidates to check are Aguiar–Ardila's poset Hopf monoid `P` inside `GP` (they realise
   posets *as braid cones*, which is our object), Marshall–Martin's `LOI`, and Aguiar–
   Mahajan's `P_q` family. **I did not determine whether our `F` is isomorphic to, a
   Hadamard factor of, or genuinely distinct from any of these**, and that is a bounded
   literature question, not a research question.
3. **Test the equivariant radical statement of §2.3 for a citation.** Saliola's *The Face
   Semigroup Algebra of a Hyperplane Arrangement* studies the reflection-group-invariant
   subalgebra and recovers Solomon; Commins, *Invariant theory for the face algebra of the
   braid arrangement* (arXiv:2404.00536, 2024), goes further — *"what is the structure of
   the face algebra as a simultaneous representation of the symmetric group and Solomon's
   descent algebra?"* **Neither was read here beyond its abstract.** If the `Aut(P)` form is
   in either, §2.3 is a special case rather than an observation.
   **RE-SCOPED, AND DEMOTED (mg-6f61).** §2.3 is a corollary of AM §10.10 (§0, boxed), so
   this step can no longer *establish* anything about the statement — at most it finds out
   whether someone has written the equivariant form down. **It is not a prerequisite for
   anything and it should not be filed as one**; whoever files it must record in the brief
   that the statement is already located as a corollary, so that a *"not found"* cannot be
   read as *"not true"*. Its remaining value is Commins' strictly harder question, which is
   about the joint `S_n` × descent-algebra structure and is worth reading on its own account.
4. **Only then ask whether anything about our walk is a Hopf-theoretic invariant.** §6.5 says
   the band product is invisible to the Hopf structure, so the honest prior is that the
   answer is no. Asking it before steps 1–3 would be the mistake this arc has made three
   times.

---

## 8. CORRECTIONS TO THE RECORD

**C1 — the Bergeron–Li negative does not transfer, and nothing in the record said so.**
mg-af28 §1 row 1 and §2 item 5 reject the towers-of-algebras programme because block
concatenation *"is unital in 0 of 64 cases"* and so fails Bergeron–Li axiom (2). Reproduced
here over 529 labelled pairs: **0 unital** (T6c). **That rejection stands.** What did not
follow, and what nothing in the record separated, is that the same map fails elsewhere: in a
Hopf monoid in species there is no `1_S` for non-empty `S` and no unitality condition on
`μ_{S,T}`, and that same concatenation is `μ_{S,T}` and passes every axiom (T5). **The
operational consequence: any successor ticket that cites mg-af28's B7 as evidence against
the species/Hopf-monoid route has a false premise.**

**C2 — mg-af28 §2.6's "the bridge is available precisely at the classical end" is right and
was never run; it is run now, and it is the whole `S_n` half of §0.** That section says
Bidigare's theorem *"is the documented route from face-monoid algebras into the Hopf/tower
programme"*, notes that *"its input is the full group action on the arrangement"*, and
concludes the bridge exists only at the antichain. **All of that is correct.** What was
missing is that the antichain end *is* where `S_n` representation theory lives, so *"the
bridge is available precisely at the classical end"* is not a limitation on the answer —
it is the answer. The measurement mg-af28 did not make is T3, and it comes out 0 bad.

**C3 — a hypothesis of mine, tested and refuted, kept on the record.** T1e was written
expecting `AC(P) = Π[n]` **iff** `P` is an antichain. **False.** `AC(P)` is the partitions
with *acyclic quotient*, and a cycle needs two blocks `B`, `C` with `b₁ < c₁` and `c₂ < b₂`,
which no poset on ≤ 2 elements admits. `AC(P) = Π[n]` holds for 3 of 3 posets at `n = 2`,
13 of 19 at `n = 3` and 45 of 219 at `n = 4`, against 1 antichain each time.

> **BROKEN, AND CORRECTED AT SOURCE (mg-6f61, on mg-a61f's X1).** The sentence that stood
> here read:
>
> > ~~*"Smallest witness with `AC(P) ≠ Π[n]`: `P = {a<c, b<d}`, where `ad|bc` has a
> > 2-cycle."*~~
>
> **It is false.** `{a<c, b<d}` **is** a witness — that much is right — but it is not the
> smallest. **The smallest is the 3-ELEMENT CHAIN.**
>
> ```
> P = a < b < c ,   X = {a,c} | {b}
> a < b sends the block {a,c} to the block {b} ;  b < c sends {b} to {a,c} .   2-cycle.
> ```
>
> **6 labelled posets at `n = 3` are witnesses — one isomorphism class, the 3-chain, in its
> 6 labellings — and 174 at `n = 4`** (`code/species_repair_6f61/out_r1_smallest.txt`, all
> 11 predictions written before the run and met; the search is shown able to return `n = 2`
> by a control that does). **The stated reason above is sound and the conclusion drawn from
> it is not:** two blocks `B`, `C` with `b₁ < c₁` and `c₂ < b₂` force `|B| ≥ 2` and
> `|C| ≥ 1`, hence `n ≥ 3` — and `n = 3` is attained. The claim read its own bound as 4.
>
> **THE SHAPE OF THIS ERROR MATTERS MORE THAN THE ERROR.** It was a **general extremal
> claim, cited to nobody, asserted rather than computed** — in a section headed *CORRECTIONS
> TO THE RECORD* — and **the refuting evidence was already in this document**: T1e's own row
> *"13 of 19 at `n = 3`"*, sixty lines above, in the table this very paragraph is
> commenting on. `19 − 13 = 6` is exactly the count that contradicts it. Nothing had to be
> researched, fetched or re-derived to catch it; it had to be **read up-page**. The one
> mathematical statement this document formed itself and located nowhere is the one that
> broke, and it broke against its own table.

**Corrected: the smallest witness with `AC(P) ≠ Π[n]` is the 3-element chain `a < b < c`,
where `{a,c}|{b}` has a 2-cycle in the quotient — 6 labelled posets at `n = 3`, one
isomorphism class. `{a<c, b<d}` is a witness and is not the smallest.** **The direction
actually used downstream — that the antichain gives all of `Π[n]` — is T1d and is 0 bad to
`n = 6`**, and nothing in §0–§7 or the ledger depends on C3 either way.

---

## 9. THE CANDIDATE SPACE, ENUMERATED, WITH WHAT EACH RETURNED

| # | candidate | searched? | verdict | reason |
|---|---|---|---|---|
| **1** | **Joyal's species** (via Aguiar–Mahajan Ch. 8) | **yes, read** | **THE FRAMEWORK** | Definition 8.1 quoted. The grading Daniel names is the species degree; `S_n` rep theory is the coefficient category, not an instance |
| **2** | **Aguiar–Mahajan, *Monoidal Functors, Species and Hopf Algebras* (2010)** | **yes, PDF downloaded and searched; chapters 8, 10, 12, 13, 15, 17 read in extract** | **THE FRAMEWORK, and it contains the operation** | §10.10 (Bidigare's radical theorem), Thm 10.13 (Bidigare), §13.1.1 (Hopf monoid of posets), §8.13 (Hadamard), Ch. 11 (connected ⟹ Hopf), §17.4–17.5 (`K(Π) = Sym`, `K̄(Π) = NCSym`) |
| **3** | **Bidigare's theorem / Solomon's descent algebra** | **yes** | **INSTANCE — and it is the `S_n` half of the answer** | rebuilt from both definitions and verified as an anti-isomorphism, 0 mismatching structure constants at `n ≤ 5`, with **one control (computed twice) failing at 472** (T3; corrected mg-6f61, §2.2). **Solomon's own 1976 paper and Garsia–Reutenauer/Atkinson were NOT fetched and NOT read — ledger S4, §3** |
| **4** | **Aguiar–Mahajan, *Bimonoids for Hyperplane Arrangements* (2020)** | **located, NOT READ** | **the most likely home, and unexamined** | publisher description only. Described as extending *"Joyal species from braid arrangements to an arbitrary arrangement"*. §7 item 1 |
| **5** | **Aguiar–Mahajan, *Topics in Hyperplane Arrangements* (2017)** | **located, NOT READ** | **adjacent, and it is where lunes live** | described as covering *"faces, flats, chambers, cones, gallery intervals, lunes"*. Brown calls our object a lune |
| **6** | **Aguiar–Ardila, *Hopf monoids and generalized permutahedra*** (arXiv:1709.07504; Memoirs AMS 289, 2023) | **yes, PDF downloaded and searched** | **ADJACENT, and it supplies the dictionary** | Table 1 pairs *posets* with *braid cones*; §12 defines a braid cone by ~~`y(i) ≤ y(j)`~~ **`y(i) ≥ y(j)`** (corrected, mg-6f61), which is our `C(P)` up to reversing the order. Whether our `F` is a sub-object of their `GP` is **not decided** (§7 item 2). **Their *"braid cone"* is `C(P)`; Marshall–Martin's is a single face — see the collision note in §1** |
| **7** | **Marshall–Martin, *Hopf monoids of set families***, Australas. J. Combin. 92(3) (2025) | **yes, PDF downloaded and searched** | **ADJACENT — the closest published analogue of §5** | a Hopf submonoid on the lattices `J(P)`; a family of posets closed under disjoint union, induced subposet and filter deletion yields a Hopf submonoid. Different coproduct, same shape of statement. **§5 must not be read as new** |
| **8** | **Saliola, *The Face Semigroup Algebra of a Hyperplane Arrangement*** (arXiv:math/0511717) | **abstract and summary only** | **ADJACENT — likely contains §2.3's citation** | reported to study the reflection-group-invariant subalgebra and to recover *"the invariant subalgebra is anti-isomorphic to Solomon's descent algebra"*. **Not read** |
| **9** | **Commins, *Invariant theory for the face algebra of the braid arrangement*** (arXiv:2404.00536, 2024) | **abstract only** | **ADJACENT — strictly beyond §2.3** | abstract quoted in §7 item 3. Answers a *harder* question than this ticket asks. **Not read** |
| **10** | **Aguiar–Bergeron–Sottile, combinatorial Hopf algebras / `QSym` terminal** | **yes** | **TRUE AND NOT DISCRIMINATING** | §6.4 |
| **11** | **Fock functors / Frobenius characteristic** | **yes, via the AM book** | **INSTANCE — resolves Bell(n) vs p(n)** | §4. **LOCATED, not re-derived: the counts `Bell(n)`/`p(n)` are measured to `n = 7`; that they are `K̄` and `K` of one species is quoted from Joyal's foreword and AM §17.4–17.5, and neither functor is evaluated from its definition here** *(marked, mg-6f61)* |
| **12** | **Towers of algebras (Bergeron–Li)** | **not re-run; mg-af28 owns it** | **still rejected, and the rejection does not transfer** | §8 C1 |
| **13** | **FI-modules, Deligne's `Rep(S_t)`, differential posets, dual graded graphs, Okounkov–Vershik, diagram algebras, Okada** | **not re-run** | booked to mg-ebd8 E10 / mg-af28 §3 | outside this brief; named so the space is complete |

---

## 10. PRE-FILED AUDIT — WHERE TO ATTACK THIS DOCUMENT

Ordered by expected yield.

1. **Attack the quotations, because of how they were obtained.** Every verbatim quote from
   Aguiar–Mahajan, Aguiar–Ardila and Marshall–Martin was extracted from the arXiv/journal
   PDF by a Flate-decode-and-string-scrape routine, **not** read from a rendered page. That
   routine **demonstrably drops `fi` and `fl` ligatures** — it renders *finite* as *nite* and
   *flats* as *rats* — and it **drops mathematical symbols entirely**, which is why the
   §17.5 quote in §4 reads `K̄(Π)`/`K(Π)` where the extraction produced two blanks. **The
   species names in that quote are my inference from the surrounding text** (the passage
   concerns the morphism from graphs and the chromatic symmetric function), not from
   characters I saw. mg-af28 pre-filed exactly this attack and it is the right one again.
   An auditor should re-read §17.4, §10.10, Theorem 10.13 and §13.1.1 from rendered PDFs.
2. ~~**Attack §2.3's non-location, because it is the one place I assert a gap in the
   literature.** *"I did not locate the `Aut(P)` form of the radical theorem stated in that
   generality"* is a report on a search over an application, which is the least reliable kind
   of negative this repo produces, and §9 rows 8 and 9 name two papers I did not read that
   are the most likely to contain it. **Read Saliola and Commins before quoting §2.3 as
   anything but a measurement.**~~

   > **THIS ITEM IS CLOSED AND ITS ERRAND IS WITHDRAWN (mg-6f61, on mg-a61f's X2).** It was
   > attacked, and the attack came back the **other way**: §2.3 is a **three-line corollary**
   > of Aguiar–Mahajan §10.10, which this document already quotes in full, plus the Reynolds
   > operator — proved and checked exactly over `Q` in mg-a61f §2.2. **There is no gap, so
   > there is nothing for a literature search to locate.** Anyone sent to *"read Saliola and
   > Commins before quoting §2.3 as anything but a measurement"* would come back
   > *"no antecedent found"*, and that sentence would enter the record as a negative result
   > about the literature when it is a fact about this routing. **Do not file that search.**
   > Saliola and Commins are still worth reading, for the separate question of whether the
   > `Aut(P)` form is *stated* somewhere (§7 item 3) — and a brief for that question must say
   > up front that §2.3 is a corollary, so a null result reads as *"not stated"* and not as
   > *"not true"*.
3. **Attack §5 for over-reach.** What is measured is closure on the ground set `[4]`. It is
   not a proof, it is not asymptotic, and §9 row 7 records a published theorem of the same
   shape. If an auditor can show our `F` is a known Hopf monoid under a different name, §5
   becomes a re-derivation and should be relabelled.
4. **Attack the identification of the semisimple quotient with the character ring.** §3
   separates what is measured from what is cited, and the un-tested link is that Solomon's
   labelling by cycle types agrees with the orbit labelling by block sizes. **Both sets are
   the integer partitions; that they are matched up correctly is not checked here.**
5. **Attack the size caps.** `t3` and `t4` stop at `n = 5`; `t5` is exhaustive only on `[4]`;
   `t2` skips 24 of 63 classes at `n = 5`. Each cap is stated in place and in the README, but
   each is a cap, and this repo's largest error to date (mg-1953 R1) was invisible precisely
   because a measurement ranged over the set on which a false statement happens to be true.
6. **Attack the claim that this is a locating exercise.** The brief predicted that the
   beyond-brief instruction is the one most likely to be violated here, and pm-onethird
   warned that naming the failure mode buys no free pass. **The two places to check are §2.3
   — where an identity is measured that I did not find stated — and §5, where axioms are
   checked on objects assembled here.** In both cases what was done is *evaluate published
   axioms against our objects*, which is what the brief asked for; but both are the shape of
   thing that becomes new mathematics one sentence later, and neither takes that sentence.

   > **THIS LIST IS INCOMPLETE, AND THE ROW IT OMITS IS THE ONLY BROKEN ONE (mg-a61f;
   > recorded here by mg-6f61).** Both named places were tested directly and **neither is
   > over the line**: §2.3 is a three-line corollary of the theorem this document quotes in
   > full, and §5 establishes closure under published operations, which is verbatim what the
   > brief asked for. **The one general mathematical statement this document formed itself
   > and located nowhere is §8 C3 — and it is false.** The list is not wrong. It is short by
   > one, and the missing one is the only one that mattered. **See §14; the finding
   > generalises past this ticket and is the reason §14 exists.**

---

## 11. CLAIM LEDGER

| # | claim | status | scope |
|---|---|---|---|
| **S1** | The categorical operation is `faces ↦ flats`, i.e. `A ↦ A/rad(A)` for a face algebra, and both of Daniel's cases are values of `(kF(P))^{Aut(P)}/rad = k^{AC(P)/Aut(P)}` | **QUOTED + PROVED, and separately MEASURED** *(upgraded from "MEASURED + QUOTED", mg-6f61)* | AM §10.10 quoted and verified verbatim against a rendered PDF; the `Aut(P)` form is a **three-line corollary** of it plus the Reynolds operator, with **no `n` dependence** (both steps checked exactly over `Q` on all 24 classes to `n ≤ 4`, mg-a61f A1d). Measured here on all 87 classes to `n ≤ 5`, 0 failures (4 classes exempt from the nilpotency step only over a `dim ≤ 90` cap) — and by mg-a61f through the trace form on **87 of 87 with no cap** and **179 of 179 at `n = 6`**. **The caps bound the instrument, not the claim** |
| **S2** | Bidigare: `(kΣ_n)^{S_n}` is anti-isomorphic to Solomon's descent algebra | **MEASURED, from both definitions** | `n ≤ 5`; 0 mismatching structure constants, 472 mismatches at `n = 5` for the control. **Corrected (mg-6f61): T3d's four columns are TWO statements each computed twice, so this is ONE control run twice, not two (or three, as §2.2 said).** The separation of *iso* from *anti* is unaffected and the theorem is reproduced entry for entry by mg-a61f from disjoint code |
| **S3** | The `S_n` instance's semisimple quotient is `k^{Π_n/S_n}`, of dimension `p(n)` | **MEASURED** | `n ≤ 5` (T4c); `\|Π_n/S_n\| = p(n)` to `n = 7` with the orbit invariant checked complete |
| **S4** | That quotient **is** the character ring of `S_n` | **CITED, NOT DERIVED — and this is the whole `S_n` half of §0** | Solomon; Garsia–Reutenauer/Atkinson, both **from secondary sources, neither read**, here or by mg-a61f's audit. §3, and §0 item 4 |
| **S5** | `Bell(n)` vs `p(n)` is the full vs bosonic Fock functor on the single species `Π` | **MEASURED (the counts) + LOCATED (the functors)** | `n ≤ 7`, 0 bad. Joyal's foreword quoted verbatim and verified against a rendered PDF; **AM §17.5 was misquoted and is corrected in §4 (mg-6f61): the book's species is `Π*` in both slots.** Neither Fock functor is evaluated from its definition here |
| **S6** | `F` and `AC` are **CLOSED** under the product and coproduct of `P × Σ` and `P × Π`; `supp` is a morphism | **MEASURED — two columns, not five** *(corrected, mg-6f61)* | exhaustive on `[4]`: 4 399 and 2 685 basis elements, 0 failures in **the two closure columns, which are the two that can fail on a sub-collection**. Associativity, coassociativity and compatibility are identities of the **ambient** Hadamard product, pinned at 0 for every collection tried including one closed under nothing; each is nevertheless shown able to fail under an operation mutation. 2 of 4 of mg-7d75's controls fire, plus mg-6f61's control (v), which isolates compatibility |
| **S7** | The Tits product — the one the walk runs on — is **not** a Hopf-monoid product | **STRUCTURAL, and separately measured** *(re-based, mg-6f61)* | The reason is a **type mismatch**: `μ_{S,T}` takes factors on **disjoint** ground sets and the Tits product intersects blocks, so every intersection is empty there. The counts 1 442 / 252 / 11 020 on `[4]` reproduce, and mg-a61f's X5 shows the 1 442 **are** the 1 442 disjoint-ground-set pairs, so they measure the mismatch rather than a near miss. **The claim itself is unchanged and is not withdrawn** |
| **S8** | The obvious map from our side to `Sym` fails, on the coproduct | **MEASURED** | 22 614 disagreements on `[4]`; 0 on the product |
| **S9** | mg-af28's Bergeron–Li negative is reproduced **and** does not transfer to Hopf monoids | **MEASURED + QUOTED** | 0 of 529 labelled pairs unital; 0 Hopf-monoid axiom failures for the same map |
| **S10** | `poset ↔ cone` is the literature's dictionary, not ours — **but the word *"braid cone"* denotes two different objects across the sources quoted** *(corrected, mg-6f61)* | **QUOTED, with the term contested** | Aguiar–Ardila §12 (corrected quotation) and Table 1; Marshall–Martin §2.1, **untruncated**, which reserves *"braid cone"* for a single face; AM Ch. 13 introduction. Two sources for `C(P)`, a third that flags the term. §1 |
| **S11** | The candidate space is the thirteen entries of §9; rows 4, 5, 8, 9 were **located and not read**; rows 1–3, 6, 7, 10, 11 were read at least in extract | **REPORT ON A SEARCH** | not a claim about the literature. Queries were targeted, not exhaustive |
| **S12** | ~~The `Aut(P)` form of the radical theorem was **not located** stated in that generality, and this is the weakest claim here~~ | **WITHDRAWN as a claim about the literature** *(mg-6f61, on mg-a61f's X2)* | It is a **corollary** of the quoted AM §10.10 plus the Reynolds operator, so **there is no gap to locate and nothing here waits on a search**. What survives is a much narrower and uninteresting report: I did not find the equivariant form *written down*, and I did not look hard. **No successor literature search should be filed on this row** — see §10 item 2 |
| **S13** *(mg-6f61)* | §8 C3's *"the smallest poset with `AC(P) ≠ Π[n]` is `{a<c, b<d}`"* was **FALSE**; the smallest is the **3-element chain** | **MEASURED, corrected at source** | 242 labelled posets to `n ≤ 4`; 6 labelled witnesses at `n = 3` in one isomorphism class, 174 at `n = 4`; 11 predictions written before the run, 11 met; a control shows the search can return `n = 2` |
| **S14** *(mg-f8fa)* | Three of mg-6f61's corrections — **X4's control count, X5's reading of control (ii), and S4/S5's scope** — were made in this document and **left standing in `code/species_7d75/`**, the copy a successor re-runs | **MEASURED, and repaired at source** | `code/species_remainder_f8fa/w3_scope.py`, the same checker, reports **12 problems** against the tree at `83ac472` and **0** after. T3d's count and control (ii)'s set equality are now **computed** by the source instrument and it **fails** if either is wrong. **No claim is softened; §5's control (ii) conclusion is strengthened from a count on `[4]` to a statement about the two maps' types at every ground set.** mg-6f61's `check_doc.py` reads one file and could not have caught any of it |
| **NOT CLAIMED** | that anything here is new; that anything here is publishable; that the searches were exhaustive; that our `F` is or is not one of the published Hopf monoids; that anything about the walk, `λ₂`, `Δ_AT` or the pricing follows; that the framework says anything about `S^λ`, `f^λ` or multiplicities | | |

---

## 12. REPRODUCE

```
cd code/species_7d75         && ./run_all.sh # ~46 s, pure Python 3, NO NETWORK
cd code/species_repair_6f61  && ./run_all.sh # ~30 s, the mg-6f61 repair, NO NETWORK
cd code/species_remainder_f8fa && ./run_all.sh # ~15 s, the mg-f8fa remainder, NO NETWORK
```

Committed outputs: `out_selftest.txt` (759 assertions), `out_t1_grading.txt`,
`out_t2_operation.txt`, `out_t3_bidigare.txt`, `out_t4_one_operation.txt`,
`out_t5_hopf_monoid.txt`, `out_t6_fock_and_record.txt`. All six `TOTAL BAD` lines are `0`.
The repair's outputs are `code/species_repair_6f61/out_r1_smallest.txt`,
`out_r2_columns.txt`, `out_r3_quotes.txt` and `out_check_doc.txt`; its
`R2 PREDICTIONS MISSED` line is **not** zero and is meant to be read.

The remainder's outputs are `code/species_remainder_f8fa/out_selftest.txt` (2 114 assertions),
`out_w1_opposite.txt`, `out_w2_typemismatch.txt` and `out_w3_scope.txt`; **`out_w3_scope_before.txt`
is the same checker run against the pre-repair tree and reports `FAIL (12 problems)`. It is
committed on purpose** — a checker written after the fix and never seen to fail is not a
checker. mg-6f61's battery and mg-a61f's battery both re-run **unmodified** against the
repaired tree; `CHECK_DOC` is `PASS`, and mg-a61f's output is **byte-identical**
(`A4 TOTAL BAD: 1`, which is X1, and 0 elsewhere).

**Sources**

- [Aguiar–Mahajan, *Monoidal Functors, Species and Hopf Algebras*](https://pi.math.cornell.edu/~maguiar/a.pdf)
- [Aguiar–Ardila, *Hopf monoids and generalized permutahedra*](https://arxiv.org/abs/1709.07504)
- [Marshall–Martin, *Hopf monoids of set families*, Australas. J. Combin. 92(3) (2025)](https://ajc.maths.uq.edu.au/pdf/92/ajc_v92_p419.pdf)
- [Commins, *Invariant theory for the face algebra of the braid arrangement*](https://arxiv.org/abs/2404.00536)
- [Saliola, *The Face Semigroup Algebra of a Hyperplane Arrangement*](https://arxiv.org/abs/math/0511717)
- [Aguiar–Mahajan, *Bimonoids for Hyperplane Arrangements* (publisher page)](https://www.cambridge.org/core/books/abs/bimonoids-for-hyperplane-arrangements/introduction/64C9656DFCB1F56A0A4C11A6C6333FDB)

---

## 13. NOTE FOR pm-onethird — SCOPE DISCIPLINE

Three things this document deliberately does **not** do.

* It does **not** develop mathematics. Everything in §2 and §5 is a **published axiom or a
  published theorem evaluated against our objects**, which is what the brief asked for. The
  two places nearest the line are pre-filed at §10 item 6.
  **— CORRECTED (mg-6f61). There was exactly one exception and it is now repaired: §8 C3's
  extremal claim was a general mathematical statement formed here, attributed to nobody, and
  false. Both places §10 item 6 names are clean; the exception is in neither of them.** The
  sentence above is true of §2 and §5 and was not true of the document.
* It does **not** edit `docs/OneThird-Landscape-Where-This-Lives.md`,
  `docs/OneThird-Branching-Graphs-Where-This-Lives.md`, `STATE.md`, the semigroup note, or
  the roadmap. §8's corrections C1 and C2 are **statements about** mg-af28, filed here;
  whether to fold them back is pm-onethird's call.
* It does **not** claim novelty for anything, including §2.3 and §5, both of which §9 and
  §10 route to specific unread papers that may already contain them.

---

## 14. WHAT THE AUDIT FOUND ABOUT THE PRE-FILED LIST — added by the repair, mg-6f61

**A SELF-AWARE PREDICTION DOES NOT NEED TO BE *WRONG* TO DO DAMAGE. IT ONLY NEEDS TO BE
*INCOMPLETE*, BECAUSE IT TELLS THE READER WHERE TO LOOK.**

That is mg-a61f's formulation and it is sharper than the one in the brief that commissioned
it. The evidence is this document.

§10 item 6 reasoned carefully about where new mathematics could enter, named two places —
§2.3 and §5 — and argued that neither crosses the line. **Both arguments are correct.**
mg-a61f tested both directly: §2.3 is a three-line corollary of the theorem quoted in §0, and
§5 establishes closure under published operations, which is verbatim what the brief asked
for. **Nothing in the pre-file is false.**

And the document's one false mathematical statement is in **§8 C3**, a third place — inside a
section headed *CORRECTIONS TO THE RECORD*, which is the last place a reader looking for
over-reach would search. The pre-file did not cover for it. **It aimed away from it.** A
named failure mode is a searchlight, and everything outside the beam gets darker: the two
named places got an audit each, and the row nobody named got none.

**Three properties of this failure mode, each visible in this document:**

1. **It survives being right.** Both predictions held. The list did its stated job and still
   cost the document its one broken claim.
2. **It is invisible to the author, by construction.** A pre-file enumerates the places the
   author already suspects. What it omits is exactly what the author does not suspect, so
   re-reading one's own list can never lengthen it.
3. **It repeats at every scale.** The same shape appears in §10 item 1: the quotation attack
   correctly predicted that the **AM §17.5** quote would be damaged — and the **two**
   quotations that also diverge, Aguiar–Ardila §12 and the truncated Marshall–Martin, were
   found only because the check was **executed** rather than trusted. **A predicted
   divergence confirms the author knew. An unpredicted one measures how far the defect
   reached.** §4.

**What follows operationally, and it is not "write longer lists".** A pre-filed attack list
is a *contribution to* an audit and never a *substitute* for one; its value is highest where
it names a mechanism (*"the extraction drops ligatures and symbols"*) and lowest where it
names locations (*"check §2.3 and §5"*), because a mechanism generalises to places the author
did not think of and a location does not. **The check that caught C3 was not a search. It was
reading up-page**: the refuting count sat in this document's own T1e row, sixty lines above
the claim.

> **THE SAME LIMITATION APPLIES TO THIS SECTION, AND IT IS STATED HERE RATHER THAN LEFT FOR
> THE NEXT AUDITOR TO FIND.** §14 is itself a self-assessment written by a repair about the
> document it repaired. Its own list of *what mg-6f61 fixed* — the five items in the banner
> at the top — is a list of the places **mg-a61f named**, and it is therefore complete only
> to the extent that mg-a61f's audit was. **This repair did not conduct an independent
> search for defects mg-a61f missed**, so an eighth defect, if there is one, is in exactly
> the position §8 C3 was in: outside every beam currently pointed at this document. The
> repair's own instrument reports **2 of 45 predicted cells missed**, both explained in
> §5 — that number is published rather than tidied because the alternative is a battery that
> cannot be wrong.

### 14.1 The correction ran in BOTH directions, and most of it ran upward

**Of the eight findings mg-a61f raised, five say this document was harsher on itself than the
evidence warranted.** That is worth naming, because the reflex after a BROKEN finding is to
hedge, and hedging is not free.

| mg-a61f | direction | what the repair did |
|---|---|---|
| **X1** — §8 C3's extremal claim | **over**-claim, and FALSE | corrected at source, in the document and in `t1_grading.py`, and the claim is now **computed** rather than asserted |
| **X3** — *"0 failures across 5 axioms"* | **over**-claim | §0 brought into agreement with §5, per column, with each column's capacity to fail demonstrated |
| **X6/X7/X8** — three quotation defects | **over**-claim (accuracy) | corrected against rendered PDFs; the terminology collision named |
| **X2** — §2.3 filed as an unlocated measurement, in four places | **UNDER**-claim | all four hedges corrected; the identity is a **corollary with no `n` dependence**, and **the successor literature search is withdrawn rather than filed** |
| **X4** — *"four candidates, three of them controls"* | **over**-claim, of the control count only | §2.2 now reads *one control, computed twice*. The theorem is untouched and reproduces entry for entry |
| **X5** — control (ii)'s 1 442 | **over**-claim, of the evidence only | accounting corrected; **the conclusion it supports is stated explicitly to SURVIVE**, because a corrected number beside an unmarked conclusion reads as a retraction |
| **S4** — the `S_n` half | **under**-stated *location* of a real limit | now named in every occurrence, with its two unread sources, rather than only in the ledger |

**The single most consequential edit in this repair is not a correction of a false statement.
It is the withdrawal of a search.** §10 item 2 routed a successor to *"read Saliola and
Commins before quoting §2.3 as anything but a measurement"*. That search **cannot find
anything, because nothing is missing** — and it would have returned *"no antecedent
located"*, a sentence that enters the record as a claim about the literature when it is a
fact about the routing. **A wasted cycle is the cheap half of that; the false record is the
expensive half.**

### 14.2 The limitation that applies to this section

> **THE SAME LIMITATION APPLIES TO §14 ITSELF, AND IT IS STATED HERE RATHER THAN LEFT FOR
> THE NEXT AUDITOR TO FIND.** §14 is a self-assessment written by a repair about the document
> it repaired. Its list of *what mg-6f61 fixed* is a list of the places **mg-a61f named**,
> plus four folded in from a second, shelved filing — so it is complete only to the extent
> that those two were. **This repair conducted no independent search for defects mg-a61f
> missed.** An eighth defect, if one exists, is in exactly the position §8 C3 was in: outside
> every beam currently pointed at this document. **That the second filing found four items
> the first did not is the direct evidence for this — two readers of one audit produced two
> different lists, and neither was a subset of the other.**
>
> The repair's own instrument reports **2 of 45 predicted cells missed** (§5). Both are
> published rather than tidied, because the alternative is a battery that cannot be wrong.

### 14.3 The eighth defect was found, and it was in the code — added by mg-f8fa

**§14.2 predicted that a further defect, if one existed, would be *"outside every beam
currently pointed at this document"*. It was, and the reason is sharper than "nobody looked":
every beam was pointed at the document.**

mg-6f61 built the strongest control in this arc — `check_doc.py`, which requires every false
sentence to survive **only** inside the strike that replaces it. It passes. **It opens one
file.** Three of the corrections it certifies were made here and left in force in
`code/species_7d75/`: T3d's header still read *"three are controls"*, the instrument README
still read control (ii)'s counts as a near miss — in a section titled *"conventions that have
bitten this repo before"*, which exists to stop exactly that — and the character-ring
identification printed unmarked inside runs ending `TOTAL BAD: 0`.

**Three properties, and the third is the one that generalises:**

1. **A passing checker is read as coverage.** `check_doc.py` reporting `PASS, 0 problems` is
   what made the instrument look repaired. Nothing said which files it read.
2. **The defect landed in the section written to prevent it.** *"Conventions that have bitten
   this repo before"* was carrying one.
3. **The fix is one line of scope, not more diligence: when a repair corrects a statement that
   also appears in code or in committed output, the checker for that repair must take the code
   directory as a target too.** `w3_scope.py` does, it takes the directory as an argument so
   it can be aimed at any tree, and **it was observed to fail before it was observed to pass** —
   12 problems at `83ac472`, 0 now.

**And the same failure was found one level down, inside that checker, and is kept on the
record.** Its first version accepted a bare *"REPAIRED"* near a forbidden string as evidence
the string was being quoted rather than asserted. The pre-repair README disarmed it **by
accident** — an unrelated *"the error mg-1953 repaired"* four lines above the near-miss bullet
made the bullet score `ok` on a tree where it was plainly false. **A checker that an adjacent
unrelated word can disarm reports coverage it does not have**, which is this section's finding
arriving against its own instrument. The marker now has to name the repair.

**Nothing in §14.3 is a retraction.** Every conclusion the corrected numbers were cited for
survives, and control (ii)'s is now stronger than the version that was corrected.
