# Species and Hopf monoids: is there ONE categorical operation with both `S_n` representation theory and the poset-quotient story as instances?

**Work item:** mg-7d75. **Date:** 2026-07-30. **Computation:** permitted, used, committed
(`code/species_7d75/`, `run_all.sh`, ~46 s, 759-assertion self-test, six test scripts, all
reporting `TOTAL BAD: 0`).

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
>   *[the `S_n` story]*

**Measured, not asserted.** The identity holds on **all 87 poset isomorphism classes to
`n ≤ 5`**, with 0 failures of closure, 0 of well-definedness, 0 of surjectivity and 0 of
nilpotency (`out_t4_one_operation.txt`, T4a/T4b; 4 classes at `n = 5` skipped for the
nilpotency step only, over a `dim ≤ 90` cap, and tested for everything else). The antichain
row reads: `|Σ_n| = 1, 3, 13, 75, 541`; `dim (kΣ_n)^{S_n} = 1, 2, 4, 8, 16 = 2^{n-1}`;
`|Π_n/S_n| = 1, 2, 3, 5, 7 = p(n)` — 0 bad (T4c).

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
of the other two).

**Daniel's specification is met on every point, including the one he flagged as the cheap
falsifier.**

| his words | what it is | checked |
|---|---|---|
| *"grading"* | the **species degree**: a species is a functor from finite sets and bijections, so degree `n` is the value on an `n`-set | T1, T5 |
| *"quotients … which form the basis of partitions in the `S_n` case"* | the **flats** `Π[n]` = set partitions of `[n]`, which are the quotients of the antichain | T1d, 0 bad |
| *"and quotient posets in the poset case"* | `AC(P)`, the partitions of `P` with acyclic quotient — the support semilattice of `F(P)` | T2a, two routes, 0 bad |
| *"grading is a constraint, so use it as one"* | applied **first**; `AC(P) ⊆ Π[n]` for all 242 labelled posets to `n ≤ 4`, 0 bad | T1e |
| *"the `S_n` side is almost certainly the Frobenius characteristic"* | it is: **`K(Π) = Sym`**, whose degree-`n` component is `⊕_n R(S_n)` with the integer partitions as basis | §4, cited |
| *"index by quotients, then take coinvariants of the grading"* | this is the **bosonic Fock functor** `K(p) = ⊕_n p[n]_{S_n}`, and it is exactly the named operation he was reaching for | §4, cited |

**And the Bell(n)-vs-p(n) gap — the one thing pm-onethird's hypothesis had to explain — is
not a discrepancy at all. It is the difference between the two Fock functors applied to one
species.** `dim K̄(Π)_n = |Π[n]| = Bell(n)` (symmetric functions in **noncommuting**
variables); `dim K(Π)_n = |Π[n]/S_n| = p(n)` (symmetric functions). Measured to `n = 7`, 0
bad (T6a). Aguiar–Mahajan §17.5, quoting their own §17.4: *"`K̄(Π)` is the algebra of
symmetric functions in noncommuting variables and `K(Π)` is the familiar Hopf algebra of
symmetric functions."*

**Three things that must be said in the same breath as the yes, because each of them limits
it.**

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

**The one place where the record was wrong, and it is on the negative side, which is where
this arc keeps breaking.** mg-af28 rejected the towers-of-algebras programme because block
concatenation fails **Bergeron–Li axiom (2)**, which demands `1_m ⊗ 1_n ↦ 1_{m+n}`. That
rejection **stands** and is reproduced here (0 of 529 labelled pairs unital, T6c). But **that
demand is not an axiom of a Hopf monoid in species**: the unit lives only in degree `∅`, and
`μ_{S,T}` carries no unitality requirement at all. The very same concatenation **is**
`μ_{S,T}`, and it passes every Hopf-monoid axiom with 0 failures on 4 399 basis elements
(T5). **The negative that closed the tower door does not close this one, and nothing in the
record separated the two.** §8.

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

Then `F(P)` is the set of faces lying in `C(P)`, and `AC(P) = supp(F(P))`. That `C(P)` is
the object the literature calls a **braid cone** is not my phrasing. Aguiar–Ardila, *Hopf
monoids and generalized permutahedra*, §12: *"Define a braid cone to be a cone in
`(ℝ^I)/ℝ^I` cut out by inequalities of the form `y(i) ≤ y(j)` for `i, j ∈ I`."* Their Table 1
pairs the combinatorial objects **posets** with the polytopes **braid cones**. Marshall–Martin,
*Hopf monoids of set families*, Australas. J. Combin. **92**(3) (2025) 419–449, §2.1:
*"geometric realization gives a bijection between preposets and convex unions of cones of
the braid arrangement."* And Aguiar–Mahajan's own chapter introduction: *"posets can be
viewed as appropriate unions of chambers (top dimensional cones, to be precise) in the
Coxeter complex of type A."*

**So the dictionary `poset ↔ braid cone` on which this whole ticket turns is not ours; it is
stated in three independent published sources, one of them the book named in the brief.**

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
Theorem 10.13 states. Three of the four columns are the control, and they fire.

### 2.3 Both instances, one identity (T4)

For every poset class `P` at `n ≤ 5`, with `G = Aut(P)`:

* the `G`-orbit sums span a subalgebra of `kF(P)` — **0 failures**;
* the induced map to functions on `AC(P)/G` is well defined (independent of the chosen
  representative of each orbit) — **0 failures**;
* it is onto — **0 failures**;
* its kernel is nilpotent — **0 failures** (4 of 63 classes at `n = 5` over the `dim ≤ 90`
  cap, tested for the other three properties).

Hence `dim (kF(P))^{Aut(P)}/rad = |AC(P)/Aut(P)|` throughout. **The antichain row:**

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

---

## 4. `Bell(n)` vs `p(n)`: THE GAP IS THE TWO FOCK FUNCTORS

Daniel: *"integer partitions are the **orbits** under the `S_n`-action, i.e. what you get
after passing to coinvariants. Taking `S_n`-coinvariants of a species is a standard
operation."* It is, and it is the **bosonic Fock functor**. Joyal, in his foreword to
Aguiar–Mahajan, defines it:

> *"By definition, we have `K(p) = ⊕_n p[n]_{S_n}`, where `p[n]_{S_n}` denotes the space of
> `S_n` coinvariants of `p[n]`."*

and Aguiar–Mahajan §17.5 records the two values on `Π`:

> *"Recall from Section 17.4 that `K̄(Π)` is the algebra of symmetric functions in
> noncommuting variables and `K(Π)` is the familiar Hopf algebra of symmetric functions."*

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

**Four controls; two fire, two do not, and the two that do not are reported rather than
replaced.**

| control | result |
|---|---|
| (i) drop the lower-set condition from the coproduct | **does not fire.** And correctly so: Aguiar–Mahajan §13.4.2's family `R_q` has the lower-set condition as its `q = 0` member and the unrestricted coproduct as `q = 1`, and both are Hopf monoids. The corruption produced a *different published Hopf monoid*, not a broken one |
| (ii) the **Tits product** of faces in place of concatenation | **fires hard**: 1 442 closure, 252 associativity, 11 020 compatibility failures |
| (iii) reverse the order of concatenation | **does not fire**, because that is the opposite monoid structure, which is compatible with the same coproduct |
| (iv) replace *"`S` is a lower set"* by *"`S` is an antichain"* | **fires**: 75 512 coassociativity failures |

**The honest reading, and it is narrower than the table looks.** A product-side control and a
coproduct-side control both fire, so the axioms are doing work. But what T5 establishes is
**closure of our two subspecies under published operations** — which is exactly the question
asked — and **not** that those operations are forced.

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

---

## 6. WHAT DOES **NOT** TRANSFER, ENUMERATED

Every item is a limitation on the yes in §0, and each is named with the measurement or the
citation that carries it.

1. **The `S_n` instance gives the character ring, not the modules.** The semisimple quotient
   is commutative of dimension `p(n)` (T4c) and the descent algebra's irreducibles are all
   one-dimensional (cited, §3). Nothing here produces `S^λ`, `f^λ`, a branching rule or a
   multiplicity. mg-af28's finding that our algebra has all irreducibles one-dimensional is
   **not** an obstruction that this framework removes — it is the same phenomenon on the
   other side too.
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
6. **The `Aut(P)`-invariant identity of §2.3 is measured, not proved, and is stated for
   `n ≤ 5`.** It is the natural equivariant form of Bidigare's radical theorem, and I did
   **not** locate it stated in that generality in the literature — see §9 row 6, and see §10
   item 2 for why that non-location is the weakest claim in this document.

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
13 of 19 at `n = 3` and 45 of 219 at `n = 4`, against 1 antichain each time. Smallest
witness with `AC(P) ≠ Π[n]`: `P = {a<c, b<d}`, where `ad|bc` has a 2-cycle. **The direction
actually used downstream — that the antichain gives all of `Π[n]` — is T1d and is 0 bad to
`n = 6`.**

---

## 9. THE CANDIDATE SPACE, ENUMERATED, WITH WHAT EACH RETURNED

| # | candidate | searched? | verdict | reason |
|---|---|---|---|---|
| **1** | **Joyal's species** (via Aguiar–Mahajan Ch. 8) | **yes, read** | **THE FRAMEWORK** | Definition 8.1 quoted. The grading Daniel names is the species degree; `S_n` rep theory is the coefficient category, not an instance |
| **2** | **Aguiar–Mahajan, *Monoidal Functors, Species and Hopf Algebras* (2010)** | **yes, PDF downloaded and searched; chapters 8, 10, 12, 13, 15, 17 read in extract** | **THE FRAMEWORK, and it contains the operation** | §10.10 (Bidigare's radical theorem), Thm 10.13 (Bidigare), §13.1.1 (Hopf monoid of posets), §8.13 (Hadamard), Ch. 11 (connected ⟹ Hopf), §17.4–17.5 (`K(Π) = Sym`, `K̄(Π) = NCSym`) |
| **3** | **Bidigare's theorem / Solomon's descent algebra** | **yes** | **INSTANCE — and it is the `S_n` half of the answer** | rebuilt from both definitions and verified as an anti-isomorphism, 0 mismatching structure constants at `n ≤ 5`, with 2 of 4 candidate identifications failing as controls (T3) |
| **4** | **Aguiar–Mahajan, *Bimonoids for Hyperplane Arrangements* (2020)** | **located, NOT READ** | **the most likely home, and unexamined** | publisher description only. Described as extending *"Joyal species from braid arrangements to an arbitrary arrangement"*. §7 item 1 |
| **5** | **Aguiar–Mahajan, *Topics in Hyperplane Arrangements* (2017)** | **located, NOT READ** | **adjacent, and it is where lunes live** | described as covering *"faces, flats, chambers, cones, gallery intervals, lunes"*. Brown calls our object a lune |
| **6** | **Aguiar–Ardila, *Hopf monoids and generalized permutahedra*** (arXiv:1709.07504; Memoirs AMS 289, 2023) | **yes, PDF downloaded and searched** | **ADJACENT, and it supplies the dictionary** | Table 1 pairs *posets* with *braid cones*; §12 defines a braid cone by `y(i) ≤ y(j)`, which is our `C(P)` verbatim. Whether our `F` is a sub-object of their `GP` is **not decided** (§7 item 2) |
| **7** | **Marshall–Martin, *Hopf monoids of set families***, Australas. J. Combin. 92(3) (2025) | **yes, PDF downloaded and searched** | **ADJACENT — the closest published analogue of §5** | a Hopf submonoid on the lattices `J(P)`; a family of posets closed under disjoint union, induced subposet and filter deletion yields a Hopf submonoid. Different coproduct, same shape of statement. **§5 must not be read as new** |
| **8** | **Saliola, *The Face Semigroup Algebra of a Hyperplane Arrangement*** (arXiv:math/0511717) | **abstract and summary only** | **ADJACENT — likely contains §2.3's citation** | reported to study the reflection-group-invariant subalgebra and to recover *"the invariant subalgebra is anti-isomorphic to Solomon's descent algebra"*. **Not read** |
| **9** | **Commins, *Invariant theory for the face algebra of the braid arrangement*** (arXiv:2404.00536, 2024) | **abstract only** | **ADJACENT — strictly beyond §2.3** | abstract quoted in §7 item 3. Answers a *harder* question than this ticket asks. **Not read** |
| **10** | **Aguiar–Bergeron–Sottile, combinatorial Hopf algebras / `QSym` terminal** | **yes** | **TRUE AND NOT DISCRIMINATING** | §6.4 |
| **11** | **Fock functors / Frobenius characteristic** | **yes, via the AM book** | **INSTANCE — resolves Bell(n) vs p(n)** | §4 |
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
2. **Attack §2.3's non-location, because it is the one place I assert a gap in the
   literature.** *"I did not locate the `Aut(P)` form of the radical theorem stated in that
   generality"* is a report on a search over an application, which is the least reliable kind
   of negative this repo produces, and §9 rows 8 and 9 name two papers I did not read that
   are the most likely to contain it. **Read Saliola and Commins before quoting §2.3 as
   anything but a measurement.**
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

---

## 11. CLAIM LEDGER

| # | claim | status | scope |
|---|---|---|---|
| **S1** | The categorical operation is `faces ↦ flats`, i.e. `A ↦ A/rad(A)` for a face algebra, and both of Daniel's cases are values of `(kF(P))^{Aut(P)}/rad = k^{AC(P)/Aut(P)}` | **MEASURED + QUOTED** | all 87 poset classes to `n ≤ 5`, 0 failures of closure / well-definedness / surjectivity / nilpotency (4 classes exempt from the nilpotency step only). AM §10.10 quoted |
| **S2** | Bidigare: `(kΣ_n)^{S_n}` is anti-isomorphic to Solomon's descent algebra | **MEASURED, from both definitions** | `n ≤ 5`; 0 mismatching structure constants for the two anti-identifications, 472 mismatches at `n = 5` for each of the two controls |
| **S3** | The `S_n` instance's semisimple quotient is `k^{Π_n/S_n}`, of dimension `p(n)` | **MEASURED** | `n ≤ 5` (T4c); `\|Π_n/S_n\| = p(n)` to `n = 7` with the orbit invariant checked complete |
| **S4** | That quotient **is** the character ring of `S_n` | **CITED, NOT DERIVED** | Solomon; Garsia–Reutenauer/Atkinson, both **from secondary sources, neither read**. §3 |
| **S5** | `Bell(n)` vs `p(n)` is the full vs bosonic Fock functor on the single species `Π` | **MEASURED + QUOTED** | `n ≤ 7`, 0 bad. Joyal's foreword and AM §17.5 quoted — **with the caveat of §10 item 1 about the dropped symbols** |
| **S6** | `F` and `AC` are closed under the product and coproduct of `P × Σ` and `P × Π` and satisfy the bimonoid axioms; `supp` is a morphism | **MEASURED** | exhaustive on the ground set `[4]`: 4 399 and 2 685 basis elements, 0 failures in 5 axioms; 2 of 4 controls fire |
| **S7** | The Tits product — the one the walk runs on — is **not** a Hopf-monoid product | **MEASURED** | 1 442 closure, 252 associativity, 11 020 compatibility failures on `[4]` |
| **S8** | The obvious map from our side to `Sym` fails, on the coproduct | **MEASURED** | 22 614 disagreements on `[4]`; 0 on the product |
| **S9** | mg-af28's Bergeron–Li negative is reproduced **and** does not transfer to Hopf monoids | **MEASURED + QUOTED** | 0 of 529 labelled pairs unital; 0 Hopf-monoid axiom failures for the same map |
| **S10** | `poset ↔ braid cone` is the literature's dictionary, not ours | **QUOTED** | Aguiar–Ardila §12 and Table 1; Marshall–Martin §2.1; AM Ch. 13 introduction |
| **S11** | The candidate space is the thirteen entries of §9; rows 4, 5, 8, 9 were **located and not read**; rows 1–3, 6, 7, 10, 11 were read at least in extract | **REPORT ON A SEARCH** | not a claim about the literature. Queries were targeted, not exhaustive |
| **S12** | The `Aut(P)` form of the radical theorem was **not located** stated in that generality | **REPORT ON A SEARCH, and the weakest claim here** | §10 item 2. **Explicitly not a novelty claim** |
| **NOT CLAIMED** | that anything here is new; that anything here is publishable; that the searches were exhaustive; that our `F` is or is not one of the published Hopf monoids; that anything about the walk, `λ₂`, `Δ_AT` or the pricing follows; that the framework says anything about `S^λ`, `f^λ` or multiplicities | | |

---

## 12. REPRODUCE

```
cd code/species_7d75 && ./run_all.sh        # ~46 s, pure Python 3, NO NETWORK
```

Committed outputs: `out_selftest.txt` (759 assertions), `out_t1_grading.txt`,
`out_t2_operation.txt`, `out_t3_bidigare.txt`, `out_t4_one_operation.txt`,
`out_t5_hopf_monoid.txt`, `out_t6_fock_and_record.txt`. All six `TOTAL BAD` lines are `0`.

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
* It does **not** edit `docs/OneThird-Landscape-Where-This-Lives.md`,
  `docs/OneThird-Branching-Graphs-Where-This-Lives.md`, `STATE.md`, the semigroup note, or
  the roadmap. §8's corrections C1 and C2 are **statements about** mg-af28, filed here;
  whether to fold them back is pm-onethird's call.
* It does **not** claim novelty for anything, including §2.3 and §5, both of which §9 and
  §10 route to specific unread papers that may already contain them.
