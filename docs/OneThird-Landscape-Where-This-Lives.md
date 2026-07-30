# Where this construction already lives: a locating exercise

**Work item:** mg-ebd8. **Date:** 2026-07-30. **Computation:** permitted, used, committed
(`code/landscape_ebd8/`, `run_all.sh`, ~12 min).

**Scope, and it is the whole of the scope.** This document says what is known, where, and by whom.
It contains **no publishability verdict and no novelty claim**, by instruction. Where I did not find
something I say *"not located"*, which is a statement about my search and not about the literature.
pm-onethird and Daniel make the significance call; a polecat asserting novelty is the failure mode
this arc has produced six generations running, and it is the least falsifiable kind of claim there is.

---

## 0. THE HEADLINE, FIRST, BECAUSE IT IS THE MOST VALUABLE THING IN THIS TICKET

**The construction is a known special case of something standard, and the standard thing is not merely
"Brown's theorem" in the general form the repo already cites. It is a specific, named, worked section
of Brown's paper.**

> **Brown, *Semigroups, rings, and Markov chains*, J. Theoret. Probab. **13** (2000) 871–938
> ([arXiv:math/0006145](https://arxiv.org/abs/math/0006145)), §4.1–§4.3.**

Three things follow, and each is checked in `code/landscape_ebd8/` rather than asserted.

1. **The monoid is Brown's.** §4.3 verbatim: *"If `L` is a finite distributive lattice, there is a LRB
   `S` whose elements are chains `0̂ = x_0 < x_1 < ⋯ < x_l = 1̂`. To construct the product of two such
   chains, we use the second factor to refine the first … We can therefore use the results of Section
   4.2 to analyze a random walk on the maximal chains of `L`, driven by weights on arbitrary chains."*
   Take `L = J(P)`, the lattice of order ideals of `P` — every finite distributive lattice is one, by
   Birkhoff. Then Brown's chains **are** the repo's `P`-compatible ordered set partitions, his product
   **is** the repo's product, and his maximal chains **are** the repo's linear extensions. Measured
   exhaustively at `n ≤ 5`: bijection 0 bad of 63 classes, product correspondence **0 bad of 922 073
   pairs**, maximal-chains-to-linear-extensions 0 bad of 63 (`out_chains_in_JP.txt`).

2. **The spectral theorem is Brown's Theorem 2, not his Theorem 1.** The repo cites the general
   left-regular-band theorem and then solves the multiplicity identity numerically. But §4.1–4.2 treat
   exactly this situation — a **convex set of chambers** `D` of an arrangement, cut out by sign
   conditions — and **Theorem 2** gives the multiplicities in **closed form**: `m_X = |μ(X,V)|` for `X`
   in `M_0` (the flats meeting the open set) and `0` otherwise. Specialised to the order cone that
   reads `m_X = ∏_{B∈X}(|B|−1)!` if every block of `X` is an **antichain of `P`**, and `0` otherwise.
   Measured against the repo's own triangular solve, exhaustively over **all 318 isomorphism classes at
   `n ≤ 6`, 37 029 levels: 0 disagreements**, and the support of `m` is exactly `M_0` in every case
   (`out_brown_theorem2.txt`).

3. **Brown's own illustration of §4.1 is the repo's worked example.** He takes the braid arrangement in
   `ℝ⁴` with `U` given by `x₁ > x₂` and `x₃ > x₄`, notes it contains **six chambers** — `1234, 1324,
   1342, 3124, 3142, 3412` — draws the lune, tabulates the eigenvalues under uniform weights and prints
   the `6 × 6` transition matrix. That is `P = {a<b, c<d}`, the poset of the note's §3–§5.

**Consequence for the two things the repo currently books as "ours".** Both reduce, and I state this
plainly because it is what the ticket asked for.

* *The identification (closure of `P`-compatibility under the product).* Brown §4.1, one line: after
  defining `G` by the sign conditions, *"Then `G` is a subsemigroup of `F`, hence a LRB (possibly
  without identity) in its own right. Its set of chambers is `D`."* The repo's lexicographic-monotonicity
  proof is a correct specialisation of a published one-line argument, for any convex set of chambers.
* *The acyclic-cut description of the levels.* This is the classical characterisation of **order
  congruences**; see §2 below. It is Czédli–Lenkehegyi's theorem, from 1983.

**One place where the literature is ahead of the repo, not behind it.** Brown's Theorem 2 names the
spectrum-carrying levels outright — *every block an antichain of `P`* — where the repo discovers them
by solving a triangular system and reports the answer as a list ("six of the fourteen levels"). The
closed form is strictly more informative and it is thirty years old.

---

## L1 — WHERE DOES THIS ALREADY LIVE?

Every neighbourhood I searched is listed, **including the ones that returned nothing**. "Searched"
means I ran targeted queries and, where a primary source existed and was reachable, downloaded it and
read the relevant section rather than a summary. Paraphrases from search snippets were not trusted:
one of them invented a reference list, which is why every quotation below is from a PDF I extracted
myself.

### 1.1 The neighbourhoods that returned the construction

| # | neighbourhood | what is there | primary source read |
|---|---|---|---|
| **A** | **Brown's LRB random walks** | §4.1–4.2 walks on a **convex set of chambers**; §4.3 walks on **maximal chains of a distributive lattice**. Both are this construction. | `math/0006145`, §4 read in full |
| **B** | **Bidigare–Hanlon–Rockmore / Brown–Diaconis hyperplane walks** | the antichain case, already recorded in the repo as an identity of families (mg-66a6). Brown–Diaconis (Ann. Probab. **26** (1998) 1813–1854) is the chamber-walk half; the convex-set extension is Brown 2000 §4, which says the §4 examples *"were first treated in unpublished joint work with Persi Diaconis"* | abstract + Brown §4 |
| **C** | **Order congruences / order-preserving partitions of a poset** | **the support lattice `AC(P)` is this named object**, `O(P)`. Sturm 1971/73/77; Czédli–Lenkehegyi 1983; Körtesi–Radeleczki–Szilágyi, *Math. Pannon.* **16** (2005) 39–55; Jenča–Sarkoci, *JCTA* **122** (2014) 28–38 ([arXiv:1112.5782](https://arxiv.org/abs/1112.5782)); survey [arXiv:2303.03765](https://arxiv.org/abs/2303.03765) | Jenča–Sarkoci read in full |
| **D** | **Oriented matroids / COMs** | Margolis–Saliola–Steinberg, *Cell complexes, poset topology and the representation theory of algebras…* (AMS Memoir 1345, [arXiv:1508.05446](https://arxiv.org/abs/1508.05446)), **Example 2.14, "Ranking COM of a poset"** — defines `R(P)` as the braid arrangement cut by `x_i < x_j` for `i ≺ j`, states *"The topes of `R(P)` are the linear extensions of `P`"*, and then, verbatim: *"`R(P)` is the right ideal of `F(A)` consisting of those ordered partitions satisfying `i ≺ j` implies the block of `i` comes before the block of `j`."* That is the repo's definition of a move, word for word. Attributed to Bandelt–Chepoi–Knauer, *COMs: complexes of oriented matroids*, with *"see [96] for the origins of this example"* — **Reiner, *Quotients of Coxeter complexes and P-partitions*, Memoirs AMS 460 (1992)** | MSS §2.14 read |
| **E** | **Stanley's order polytope / P-partition theory** | MSS: *"The COM `R(P)` is closely connected to the order polytope of `P`"* (Stanley, *Two poset polytopes*, DCG **1** (1986)). The moves are the weakly order-preserving surjections `P →` chain, i.e. the `P`-partitions with chain image | via MSS + Jenča–Sarkoci Thm 3.3 |
| **F** | **Aguiar–Mahajan, *Topics in Hyperplane Arrangements*** (AMS Surveys **226**, 2017) | Part I treats faces, flats, chambers, **cones** and lunes with the **Tits monoid** central; MSS point to *"[6, Section 6.4] for more details on the connections between posets and the braid arrangement"*. I did **not** obtain the book text — this is a located pointer, not a read source | **not read** (paywalled) |

### 1.2 The neighbourhoods that returned something adjacent but different

| # | neighbourhood | what is there | why it is not this |
|---|---|---|---|
| **G** | **Markov chains on linear extensions via monoids** — Ayyer–Klee–Schilling, *Combinatorial Markov chains on linear extensions*, JACO **39** (2014) ([arXiv:1205.7074](https://arxiv.org/abs/1205.7074)); Ayyer–Schilling–Steinberg–Thiéry, *Markov chains, R-trivial monoids and representation theory* | **same state space `L(P)`, different monoid.** Their operators are generalised **promotion** operators; the monoid is **𝓡-trivial**, not a left regular band, and they obtain explicit eigenvalues **only when `P` is a rooted forest**, via Steinberg's extension of Brown's theory | our monoid is an LRB for **every** `P`, and the spectrum is available for every `P` |
| **H** | **Björner's greedoid walks** — *Random walks, arrangements, cell complexes, greedoids, and self-organizing libraries* (Building Bridges, 2008, [arXiv:0805.0083](https://arxiv.org/abs/0805.0083)), Thm 4.15 | interval greedoids give LRBs with support lattice = **lattice of greedoid flats**. Applied to the **poset shelling antimatroid** (feasible words = prefixes of linear extensions) this does give a walk on `L(P)` | the elements are **words**, not ordered partitions — the sub-monoid of moves of the form (singletons…, rest). For the antichain this is the **free LRB**, support lattice Boolean, **not** `Π_n`; it misses the riffle shuffles. A proper submonoid of ours |
| **I** | **Saliola–Thomas, oriented interval greedoids**; Chung–Graham graph LRBs; Athanasiadis–Diaconis, *Functions of random walks on hyperplane arrangements* | further LRB families and refinements of the walk analysis | different families; no poset/order-cone instance located |
| **J** | **Representation theory of LRB algebras** — Saliola (quiver of an LRB algebra); Margolis–Saliola–Steinberg (global dimension, poset topology); Reiner–Saliola–Welker (symmetrised walks) | this is the live representation-theoretic account of the family, and `R(P)` sits inside it as an example | it is *semigroup* representation theory, not `S_n` representation theory — consistent with the repo's own L1 finding (mg-8fd1) |

### 1.3 The neighbourhoods the ticket named that returned NOTHING for this construction

Reported as empty, deliberately.

| # | neighbourhood searched | result |
|---|---|---|
| **K** | **Stanley's differential posets** | **empty.** Differential posets (`DU − UD = rI`) generalise the *enumerative* consequences of RSK on Young's lattice. `O(P)` is graded, but no differential structure is claimed anywhere and none of the mechanism transfers. No contact located |
| **L** | **Fomin's dual graded graphs** | **empty**, same reason. Dual graded graphs generalise RSK/growth-diagram combinatorics; the follow-on literature (Kac–Moody dual graded graphs, quantized DGGs, dual filtered graphs) is about Schensted correspondences, not about walks on chambers. No contact located |
| **M** | **Combinatorial species / Hopf monoids in species** (Aguiar–Mahajan) | **empty for the poset case.** Species and Hopf monoids are built over the braid arrangement, so the antichain end is deeply developed there; I located **no** order-cone / poset-quotient analogue. Not a negative result about the literature — a negative result about my search |
| **N** | **Incidence algebras and Möbius algebras** | **empty as a home.** Möbius functions are *used* throughout (the multiplicities are `|μ(X,V)|`), but I located nothing that treats this construction as an incidence-algebra object |
| **O** | **EI-categories and Möbius categories** | **empty.** Located the general frameworks (Haigh's and Leinster's Möbius categories, fine vs coarse Möbius inversion; K-theoretic Möbius inversion for quasi-finite EI categories; decomposition spaces, Gálvez-Carrillo–Kock–Tonks) but **no** treatment of this construction or of the pairing in them |
| **P** | **Combinatorial Hopf algebras** | **empty.** No contact located |
| **Q** | **"Generalise `S_n` representation theory to other categories"**, as a named programme | the named programmes with that shape are **FI-modules / representation stability** (Church–Ellenberg–Farb) and **Deligne's interpolation categories `Rep(S_t)`**. Both are about *stabilising or interpolating the categories of `S_n`-representations themselves*. **Neither has any contact with this construction**, which is semigroup representation theory over a support lattice. Named here so the phrase is not left floating |

---

## L2 — THE HONEST DELTA, ITEM BY ITEM

Every claim reduced to **instance / special case / generalisation / adjacent**, with the reason.
"Adjacent" is used where it is the true answer.

| repo object | verdict | reason |
|---|---|---|
| the monoid `F(P)` of `P`-compatible ordered set partitions | **INSTANCE** | = Brown §4.3's LRB of chains in `J(P)` (measured: 0 bad of 922 073 product pairs, `n ≤ 5`); = MSS Example 2.14's ranking COM `R(P)`, defined there in the repo's own words; = Brown §4.1's `G` for `A` = braid, `U` = order cone |
| the states `L(P)` = chambers | **INSTANCE** | Brown §4.1's `D`; BCK/MSS: *"the topes of `R(P)` are the linear extensions of `P`"* |
| **closure** of `P`-compatibility under the product (repo's "ours" #1) | **SPECIAL CASE** | Brown §4.1 proves it in one line for *any* convex set of chambers. The repo's proof is correct and independent; it is not new |
| **the acyclic-quotient description of the levels** (repo's "ours" #2) | **SPECIAL CASE** | Czédli–Lenkehegyi (1983), quoted as Thm 3.3 in Jenča–Sarkoci: `ρ` is an order-congruence ⟺ `ρ = Ker f` for an order-preserving `f : P → Q`. Composing `f` with a linear extension of `Q` makes the codomain a chain at no cost, which is exactly the repo's "topological sort" direction |
| the support lattice `AC(P)` | **INSTANCE of a named object** | `AC(P) = O(P)`, the lattice of order congruences. Verified against the two published definitions setwise, and against Jenča–Sarkoci's homotopy theorem numerically — see §3 |
| `AC(P)` is a lattice, closed under common refinement, **not** a sublattice of `Π_n` (repo §2.6 / row Q7) | **KNOWN** | `O(P)` is an algebraic lattice (Sturm 1977, Thm 30); Jenča–Sarkoci give the meet as blockwise intersection and the join by a transitive-closure construction that is *not* `Π_n`'s join. The repo's contribution here is the **frequency** (7/16 at `n=4`, 49/63 at `n=5`), which I did **not** locate |
| antichain ⟹ `AC(P) = Π_n` | **KNOWN** | Jenča–Sarkoci Example 3.5 |
| chain ⟹ `\|AC(C_n)\| = 2^{n−1}`, Boolean, blocks convex (repo §2.3 / row Q5) | **KNOWN** | Jenča–Sarkoci Example 3.6, stated exactly |
| `AC(P)` is ranked by `n − \|π\|`; atoms are the `π_{a,b}` for `a ⋖ b` or `a ∥ b` | **KNOWN** | Jenča–Sarkoci §3; also Körtesi–Radeleczki–Szilágyi: `O(P)` is **graded and relatively complemented**. Not currently in the repo; recorded here as available |
| the eigenvalue rule `λ_X = Σ_{supp ≤ X} w` | **INSTANCE** | Brown Theorem 2 |
| the multiplicity rule (triangular counting identity) | **INSTANCE, and a weaker form of the published one** | Brown's (10) is the same identity; his Theorem 2 solves it in closed form. Measured agreement: 0 bad of 318 classes / 37 029 levels at `n ≤ 6` |
| `m_X = ∏_B(\|B\|−1)!` on the antichain (repo §7) | **KNOWN** | the specialisation of `\|μ(X,V)\|` to `M_0 = Π_n` |
| the worked example `P = {a<b, c<d}` | **the same example** | Brown §4.1 uses it to illustrate Theorem 2, including the `6 × 6` matrix |
| Ayyer–Klee–Schilling promotion chains | **ADJACENT** | same states, different monoid, 𝓡-trivial not LRB, eigenvalues only for rooted forests |
| Björner's greedoid walk on the poset shelling antimatroid | **ADJACENT** (strictly: a proper **submonoid**) | word-moves only; support lattice is the greedoid flat lattice, Boolean at the antichain, so the riffle shuffles are absent |
| differential posets; dual graded graphs; species/Hopf monoids; incidence and Möbius algebras; EI/Möbius categories; combinatorial Hopf algebras | **NO CONTACT LOCATED** | see the table in §1.3. This is a report on my search, not a claim about the literature |

### 2.1 What I did NOT locate

Stated as *not located*, which is **not** a synonym for *new*. Each of these is a place where a
targeted search returned nothing; none of them was searched to exhaustion, and the negative-search
literature in this arc has a poor record.

1. **The `S_n`-stability theorem** (mg-8fd1 rows Q3/Q4): `AC(P)` is `S_n`-stable ⟺ `AC(P) = Π_n` ⟺
   every two relations of `P` share an end ⟺ `P` is an antichain or a star, giving `2(n−1)` classes.
   The relabelling action of `S_n` on `O(P)` is a natural question for the order-congruence literature
   and I did not find it asked there. **Not located.**
2. **The invariant `G(P) = {σ : σ·AC(P) = AC(P)}`** and its distribution (mg-8fd1 row Q6). **Not located.**
3. **The frequency of the join failure** — that `AC(P)` fails to be a `Π_n`-sublattice *typically*
   rather than exceptionally (7/16, 49/63). The *fact* is published; the *frequency* I did not find.
4. **Any development of Brown §4.3 specifically for `L = J(P)`** — mixing times, comparison with the
   adjacent-transposition walk, or the `Δ_AT` question. Brown states the construction and moves on to
   the "kids walk"; I located no follow-up aimed at posets. Nestoridi (strong stationary times) and
   Pike (eigenfunctions) develop the chamber-walk side, not the convex-set side. **Not located** — and
   this is the one where I would least trust a negative, because it is a search over applications
   rather than over objects.

---

## L3 — IS THE PAIRING TREATED AS A SINGLE PARADIGM?

Daniel's structural point is that finite-set/partition and poset/quotient-poset are two instances of
one shape. **The answer is yes, and it has been yes since 2000.**

**Brown §4.1–4.2 is the single paradigm, and the two ends are its two extreme cases.** The setup is: an
arrangement `A`, and a **convex set of chambers** `D` cut out by sign conditions. Then

* take the sign condition set `J = ∅`: `U` is the whole space, `D` is **all** chambers, `G` is the full
  face monoid — this is the braid/BHR/Brown–Diaconis case, states `S_n`, support lattice `Π_n`;
* take `J` = the relations of `P`: `U` is the **order cone**, `D` is `L(P)`, `G` is `F(P)` — this is
  the poset case, support lattice `O(P)`.

**One theorem covers both**, with the same eigenvalue formula and the same Möbius multiplicities, and
Brown's Theorem 2 is stated at exactly the generality that contains the pair. The intersection lattice
`M_0` interpolates: it is all of `Π_n` at one end and the antichain-blocked order congruences at the
other. So the pairing is **not** an unstudied juxtaposition of two separately-known halves — it is one
published theorem, and the poset half is one of the three examples Brown chose to write out.

Two further places treat the pair as one object:

* **MSS's memoir** puts both under **CW left regular bands**: the braid face monoid and the ranking COM
  `R(P)` are examples in the same chapter, with a common representation theory (quiver, global
  dimension, poset topology of the support lattice).
* **Bandelt–Chepoi–Knauer's COMs** are explicitly a common generalisation of oriented matroids (the
  `J = ∅` end) and their convex "complexes" (the poset end).

**What this does to the framing.** *"Does this give us a generalisation of rep theory of `S_n` to other
categories"* has a precise answer at the level of location: the generalisation on offer is not of `S_n`
representation theory but of the **face-monoid / left-regular-band** representation theory, and both of
Daniel's instances are already inside it. This is the same conclusion the repo reached from the other
direction in mg-8fd1 §1 — *"a dead `S_n` route and a live semigroup-representation route whose index
set is the object Daniel identified"* — and the survey now confirms that the live route is a populated
research area with the poset instance already named in it.

**One thing that is genuinely different about the second instance, stated without inflation.** At the
antichain end the support lattice is `Π_n` and the ambient symmetric group acts on everything. At the
poset end the support lattice is `O(P)`, and mg-8fd1's theorem says `S_n`-stability happens *only* where
`O(P)` degenerates back to `Π_n`. So the two instances share a mechanism but not a symmetry group. That
observation is the repo's; I did not locate it in the literature, and per §2.1 that is a statement
about my search.

---

## 3. THE IDENTIFICATION, MEASURED RATHER THAN ASSERTED

Three instruments in `code/landscape_ebd8/`, sharing no code with `code/hodge_leverage/`,
`code/face_geometry/`, `code/unified_gate_8fd1/` or `code/semigroup_note/`. Every predicted number is
**read off a paper**; nothing is fitted.

### 3.1 `identify_lattice.py` — is `AC(P)` the order-congruence lattice `O(P)`?

Predictions taken from Jenča–Sarkoci and Körtesi–Radeleczki–Szilágyi. Exhaustive over all isomorphism
classes to `n = 6`.

| `n` | classes | connected | **P2**: `μ(0̂,1̂) = (−1)^{n−1}·spheres` | P1 defs agree | P5 rank | P6 atoms | P7 meet |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 1 | n/a (`n<3`) | 0 bad of 2 | 0 bad | 0 bad | 0 bad |
| 3 | 5 | 3 | 0 bad of 5 | 0 bad of 5 | 0 bad | 0 bad | 0 bad |
| 4 | 16 | 10 | 0 bad of 16 | 0 bad of 16 | 0 bad | 0 bad | 0 bad |
| 5 | 63 | 44 | 0 bad of 63 | 0 bad of 63 | 0 bad | 0 bad | 0 bad |
| 6 | 318 | 238 | **0 bad of 318** | 0 bad of 318 | 0 bad | 0 bad | 0 bad |

**P2 is the sharp one.** Jenča–Sarkoci prove the order complex of `Ô(P)` is a wedge of spheres of
dimension `n−3`, the number of spheres being `e(P)` for connected `P` and the number of **cyclic
classes** of linear extensions in general. That number is a topological invariant computed with no
reference to this programme; the Möbius function of the repo's `AC(P)` reproduces it, with the right
sign, on every poset to `n = 6` — including the disconnected ones, where the count is `e_C(P)` and not
`e(P)`, so the test discriminates.

Also reproduced: `|AC| = |Π_n|` on antichains and `2^{n−1}` with convex blocks on chains, `n ≤ 6`
(JS Examples 3.5, 3.6); and **JS Example 3.7** — `P = B₂`, the 4-element Boolean lattice — gives
`|O(P)| = 11` and 2 spheres, both hit exactly.

### 3.2 `brown_theorem2.py` — is the spectrum Brown's **Theorem 2**?

| `n` | classes | levels | B1 closed form = solved | B2 support = `M_0` | B3 total = `\|L(P)\|` |
|---|---|---|---|---|---|
| 2 | 2 | 4 | 0 bad of 2 | 0 bad of 2 | 0 bad of 2 |
| 3 | 5 | 24 | 0 bad of 5 | 0 bad of 5 | 0 bad of 5 |
| 4 | 16 | 206 | 0 bad of 16 | 0 bad of 16 | 0 bad of 16 |
| 5 | 63 | 2 353 | 0 bad of 63 | 0 bad of 63 | 0 bad of 63 |
| 6 | 318 | **37 029** | **0 bad of 318** | **0 bad of 318** | 0 bad of 318 |

On the worked example the closed form reproduces the note's §5a table entry for entry: the six levels
carrying multiplicity are exactly `ac|bd`, `ac|b|d`, `ad|b|c`, `a|bd|c`, `a|bc|d`, `a|b|c|d` — and they
are exactly the levels **all of whose blocks are antichains of `P`**, which is what `M_0` means and
what the note does not say.

### 3.3 `chains_in_JP.py` — is `F(P)` Brown's §4.3 band?

| `n` | classes | moves | C1 chains ↔ moves | C2 products correspond | C3 maximal ↔ linear ext |
|---|---|---|---|---|---|
| 1 | 1 | 1 | 0 bad of 1 | 0 bad of 1 pairs | 0 bad of 1 |
| 2 | 2 | 5 | 0 bad of 2 | 0 bad of 13 pairs | 0 bad of 2 |
| 3 | 5 | 37 | 0 bad of 5 | 0 bad of 321 pairs | 0 bad of 5 |
| 4 | 16 | 397 | 0 bad of 16 | 0 bad of 13 853 pairs | 0 bad of 16 |
| 5 | 63 | 5 757 | 0 bad of 63 | **0 bad of 922 073 pairs** | 0 bad of 63 |

The move counts `1, 5, 37, 397, 5 757` are the note's own (its §2 sweep quotes `5 757` at `n = 5`), and
the worked example returns 26 moves and 6 maximal chains against the note's 26 and 6.

---

## 4. REPRODUCE

```
cd code/landscape_ebd8 && ./run_all.sh        # ~12 min, pure Python 3
```

Committed outputs: `out_identify_lattice.txt`, `out_brown_theorem2.txt`, `out_chains_in_JP.txt`.

---

## 5. CLAIM LEDGER

| # | claim | status | scope |
|---|---|---|---|
| **E1** | the monoid `F(P)`, its product, and its chambers are Brown (2000) §4.3's LRB of chains in `J(P)` | **MEASURED + QUOTED** | bijection and product correspondence exhaustive at `n ≤ 5` (922 073 pairs, 0 bad); the quotation is from the arXiv PDF |
| **E2** | the spectral result is Brown's **Theorem 2** (convex set of chambers), whose multiplicities are `\|μ(X,V)\|` in closed form | **MEASURED + QUOTED** | 0 disagreements over 318 classes / 37 029 levels at `n ≤ 6`; theorem quoted verbatim |
| **E3** | `AC(P)` is the lattice `O(P)` of order congruences (Sturm; Czédli–Lenkehegyi; Körtesi–Radeleczki–Szilágyi; Jenča–Sarkoci) | **MEASURED + QUOTED** | two definitions agree setwise on all 405 classes at `n ≤ 6`; JS's homotopy theorem reproduced via Möbius on all of them |
| **E4** | `F(P)` is MSS Example 2.14's **ranking COM `R(P)`**, origins in Reiner's 1992 Memoir, defined there in the repo's own words | **QUOTED** | quotation from `arXiv:1508.05446`; Reiner's Memoir itself **not read** (not freely available) |
| **E5** | Brown's §4.1 illustration is the repo's worked example `P = {a<b, c<d}` | **QUOTED + MEASURED** | Brown lists the six chambers and the `6×6` matrix; our count is 6 |
| **E6** | the repo's two "ours" items are a special case of Brown §4.1 and of Czédli–Lenkehegyi respectively | **READING OF QUOTED SOURCES** | both sources quoted; the reading is mine and is the kind of thing an audit should attack first |
| **E7** | Ayyer–Klee–Schilling is a different monoid on the same states, LRB-adjacent, rooted forests only | **QUOTED** | abstract quoted verbatim |
| **E8** | Björner's greedoid LRB applied to the poset shelling antimatroid is a proper submonoid of `F(P)` | **READING**, not measured | Björner Thm 4.15 and his product (4.8) read in full; the submonoid claim is my derivation and is **not** checked by code. Weakest structural claim in this document |
| **E9** | the pairing (set-partition end and poset-quotient end) is treated as one paradigm, by Brown §4.1–4.2 | **READING OF A QUOTED SOURCE** | the `J = ∅` specialisation is immediate from his setup; he does not spell it out in those words |
| **E10** | differential posets, dual graded graphs, species/Hopf monoids, incidence/Möbius algebras, EI/Möbius categories, combinatorial Hopf algebras returned **no contact** | **REPORT ON A SEARCH** | not a claim about the literature. Queries were targeted, not exhaustive |
| **E11** | the `S_n`-stability theorem, the invariant `G(P)`, the join-failure frequency, and any poset-specific development of Brown §4.3 were **not located** | **REPORT ON A SEARCH** | explicitly **not** a novelty claim. §2.1 records why the fourth is the least reliable negative |
| **NOT CLAIMED** | that anything here is new; that anything here is publishable; that the searches were exhaustive; anything about `λ₂`, `Δ_AT` or the pricing; anything about Aguiar–Mahajan §6.4 beyond its existence as a pointer; anything from Reiner's Memoir beyond MSS's attribution | | |

---

## 6. PRE-FILED AUDIT — where to attack this document

Filed in advance, per arc convention, and ordered by how much I expect them to yield.

1. **E8 is the weakest link.** The claim that Björner's greedoid band on the poset shelling antimatroid
   is a *proper submonoid* of `F(P)` is a derivation from his (4.8) and Thm 4.15, **not measured**. An
   auditor should build both and compare. If it is wrong, the "adjacent" verdict in the L2 table for row
   H is wrong with it. Nothing else in the document depends on it.
2. **E6 is a reading, and readings are where this arc breaks.** Specifically: does Brown's §4.1
   *"`G` is a subsemigroup of `F`"* really cover the repo's closure statement, given that Brown's `G` is
   defined by `σ_i(G) ≥ 0` and the repo's by a block-order condition? I believe the two definitions
   coincide, and `chains_in_JP.py` establishes the resulting monoids coincide — but the *sign-condition
   to block-order* translation is asserted in prose and never measured on its own.
3. **The `M_0` translation.** I read *"`M_0` consists of the `X ∈ L` that intersect `U`"* and derived
   *"every block an antichain of `P`, quotient acyclic"*. `brown_theorem2.py` confirms the **consequence**
   (the closed form matches on 37 029 levels) but not the derivation. A wrong derivation that happens to
   produce the right set is possible and would be exactly this arc's signature failure.
4. **Attack the negatives.** E10 and E11 are search reports. The cheapest attack is to find one hit in
   any of the six empty neighbourhoods, or to find the `S_n`-stability statement in the order-congruence
   literature. I searched Sturm's three papers only through their citation in Jenča–Sarkoci; **I did not
   read Sturm, Czédli–Lenkehegyi, Körtesi–Radeleczki–Szilágyi, Bandelt–Chepoi–Knauer, Reiner, or
   Aguiar–Mahajan in the original.** Six unread primary sources is the largest hole here.
5. **Check the sign convention in P2.** `μ(0̂,1̂) = (−1)^{n−1}·s` was derived from "wedge of `s` spheres
   of dimension `n−3`" via the reduced Euler characteristic. It passes on 405 posets, which is strong,
   but the exponent was derived and not quoted.
6. **The disconnected case.** P2 uses `e_C(P)` for disconnected `P`, implementing Jenča–Sarkoci's
   Definition 4.1 as *single* cyclic rotation of the word. If that relation is not transitive as they
   assert, my union-find implementation computes a coarser equivalence than theirs and P2's passes on
   the 80 disconnected classes at `n = 6` would be checking a different statement.

## 7. NOTE FOR pm-onethird — SCOPE DISCIPLINE

Not relayed to Daniel, per the ticket. Three things this document deliberately does **not** do:

* it does not say whether any of this is publishable, and the §2.1 "not located" list must not be read
  as a novelty list — it is a list of places I looked and came up empty, in an arc where negative
  searches have been unreliable;
* it does not develop any mathematics: the three instruments only compare the repo's objects against
  published descriptions of other objects;
* it does not touch `λ₂`, `Δ_AT`, roadmap pricing, or the mg-8fd1 gate's conclusions.

The one operational consequence worth surfacing: **the note `docs/OneThird-Semigroup-Walk-Family-Note.md`
§8 currently books two items as "ours" that reduce to Brown §4.1 and to Czédli–Lenkehegyi 1983.** That is
a status error running in the *opposite* direction from the one mg-66a6 found (it upgraded two items from
"verified to five elements" to "elementary theorems"). Both corrections are about the same two sentences.
Whether to amend the note is pm-onethird's call, not mine; I have not edited it.
