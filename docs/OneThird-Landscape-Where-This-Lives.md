# Where this construction already lives: a locating exercise

**Work item:** mg-ebd8. **Date:** 2026-07-30. **Computation:** permitted, used, committed
(`code/landscape_ebd8/`, `run_all.sh`, ~12 min).

> **⚠️ REPAIRED 2026-07-30 by mg-1953, after the independent audit mg-d673
> (`docs/OneThird-Landscape-Where-This-Lives-IndependentAudit.md`, commit `924e2ee`).
> The LOCATING was confirmed by that audit, under stronger tests than the ones run here, and
> is untouched. What is repaired is the three things this document *derived* — which the
> ticket forbade — and its arithmetic about its own instruments. Two of the three derivations
> were false. Every repaired sentence is marked ⚠️ in place and listed with its measurement in
> **§8, THE REPAIR RECORD**; nothing is silently fixed, and no repair rests on the audit's
> word — each is re-measured in `code/landscape_repair_1953/` (`run_all.sh`, ~1 min, with a 101-assertion self-test), sharing
> no code with `code/landscape_ebd8/` or `code/landscape_audit_d673/`.**

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
   exhaustively at `n ≤ 5`: bijection 0 bad of **87 classes**, product correspondence **0 bad of
   936 261 pairs**, maximal-chains-to-linear-extensions 0 bad of 87 (`out_chains_in_JP.txt`).
   ⚠️ *Repaired: this originally read "0 bad of 63 classes" and "0 bad of 922 073 pairs", which are
   the `n = 5` **row** of §3.3's table quoted as the `n ≤ 5` **total**. The totals are larger, so the
   original under-reported its own evidence. §8 R4.*

2. **The spectral theorem is Brown's Theorem 2, not his Theorem 1.** The repo cites the general
   left-regular-band theorem and then solves the multiplicity identity numerically. But §4.1–4.2 treat
   exactly this situation — a **convex set of chambers** `D` of an arrangement, cut out by sign
   conditions — and **Theorem 2** gives the multiplicities in **closed form**: `m_X = |μ(X,V)|` for `X`
   in `M_0` (the flats meeting the open set) and `0` otherwise. Specialised to the order cone that
   reads `m_X = ∏_{B∈X}(|B|−1)!` if every block of `X` is an **antichain of `P`** ⚠️ **and the quotient
   `P/X` is acyclic**, and `0` otherwise.
   Measured against the repo's own triangular solve, exhaustively over **all 318 isomorphism classes at
   `n ≤ 6`, 37 029 levels: 0 disagreements**, and the support of `m` is exactly `M_0` in every case
   (`out_brown_theorem2.txt`).

   ⚠️ **Repaired, and this was BROKEN — the acyclicity clause was missing from every prose statement
   of the closed form in the original, while `brown_theorem2.py`'s own docstring carried it.** A flat
   all of whose blocks are antichains of `P` need not meet the open order cone: the quotient must also
   be acyclic. Because the *"and `0` otherwise"* ranges over **all** flats, the original sentence is
   not an abbreviation but a false statement, and it violates Brown's own total-multiplicity identity
   `Σ_X m_X = |L(P)|` on **1 of 16** posets at `n = 4`, **10 of 63** at `n = 5` and **101 of 318** at
   `n = 6`, with **455 spurious flats** at `n = 6`. Smallest witness `P = {a<c, b<d}` (two disjoint
   2-chains, `|L(P)| = 6`): the original rule sums to **7**, on the spurious flat `ad|bc` — both blocks
   antichains, quotient a 2-cycle, so the flat misses `U`. The repaired rule sums to 6 on every poset
   at every `n ≤ 6`. **The original measurement could not see this, because its code ranged `X` over
   `AC(P)` — the set on which the wrong statement happens to be right.** §8 R1, and
   `out_closed_form_outside_AC.txt`, which ranges `X` over all flats and includes the control showing
   the restriction is what hid it.

3. **Brown's own illustration is the repo's worked example.** He takes the braid arrangement in
   `ℝ⁴` with `U` given by `x₁ > x₂` and `x₃ > x₄`, notes it contains **six chambers** — `1234, 1324,
   1342, 3124, 3142, 3412` — and draws the lune (**§4.1**); the eigenvalue table under uniform weights
   and the `6 × 6` transition matrix are in **§4.2** ⚠️ *(originally both attributed to §4.1)*. That is
   `P = {a<b, c<d}`, the poset of the note's §3–§5.

**Consequence for the two things the repo currently books as "ours".** Both reduce, and I state this
plainly because it is what the ticket asked for.

* *The identification (closure of `P`-compatibility under the product).* Brown §4.1, one line: after
  defining `G` by the sign conditions, *"Then `G` is a subsemigroup of `F`, hence a LRB (possibly
  without identity) in its own right. Its set of chambers is `D`."* The repo's lexicographic-monotonicity
  proof is a correct specialisation of a published one-line argument, for any convex set of chambers.
* *The acyclic-cut description of the levels.* This is the classical characterisation of **order
  congruences**; see §2 below. It is Czédli–Lenkehegyi's theorem, from 1983.

**Two places where the literature is ahead of the repo, not behind it** ⚠️ *(originally "one place",
while the §2 table names a second — Körtesi–Radeleczki–Szilágyi's "graded and relatively
complemented")*. Brown's Theorem 2 names the spectrum-carrying levels outright — *every block an
antichain of `P`, with acyclic quotient* — where the repo discovers them by solving a triangular
system and reports the answer as a list ("six of the fourteen levels"). The closed form is **strictly
more informative**, and it is twenty-six years old.

⚠️ **"STRICTLY SHARPER" — the phrase in this work item's own commit subject (`714aceb`) — is
REFUTED, and the refutation is the correction with the largest consequence here.** *Sharper* is a
comparison, and the original had already run it: its own `B1` column is **0 disagreements at 37 029
levels**. It then reported that agreement as sharpness — the two words were never separated. Run
again as a two-sided comparison at **every** level — the repo's solve and
Brown's closed form, level by level — there are **0 disagreements at all 39 616 levels to `n ≤ 6`**
(4, 24, 206, 2 353, 37 029 by `n`). **Brown's answer is the same answer.** What Theorem 2 supplies
is that the **28 988 of 37 029** levels carrying zero at `n = 6` (1 674 of 2 353 at `n = 5`) are
named *a priori* rather than discovered by a solve. *"Strictly more informative"* — this document's
own phrase, above — is the correct one and replaces *"strictly sharper"* everywhere, including in the
commit subject's claim as recorded; that commit message is frozen, so this paragraph is where the
correction lives. **The operational consequence is that the repo is NOT using a weaker tool, and any
ticket premised on adopting Theorem 2 to get better answers has a false premise.** §8 R3.

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
| **H** | **Björner's greedoid walks** — *Random walks, arrangements, cell complexes, greedoids, and self-organizing libraries* (Building Bridges, 2008, [arXiv:0805.0083](https://arxiv.org/abs/0805.0083)), Thm 4.15 | interval greedoids give LRBs with support lattice = **lattice of greedoid flats**. Applied to the **poset shelling antimatroid** (feasible words = prefixes of linear extensions) this does give a walk on `L(P)` | the elements are **words**, not ordered partitions. For the antichain the band is the **free LRB**, support lattice Boolean, **not** `Π_n`; it misses the riffle shuffles. ⚠️ **REPAIRED — it is *not* "a proper submonoid of ours".** The word-to-move map `w ↦ ({w₁},…,{w_k}, rest)` is **never injective** (0 of 63 at `n = 5`), and at the antichain the band is strictly **larger** than the whole of `F(P)` at `n = 2, 3` — free LRB 5 and 16 against ordered Bell 3 and 13 — so it cannot be a submonoid of it, and the *"free LRB"* and *"proper submonoid"* halves of the original cell contradicted each other. **What is true, and measured:** the map is a monoid **homomorphism** (63/63), its image lies in `F(P)` and is closed under the repo's product (63/63), so **a homomorphic image of the band is a submonoid of `F(P)` — proper exactly for `n ≥ 3`** (5/5, 16/16, 63/63; at `n = 2` the image is *all* of `F(P)`, 2 of 2). §8 R2 |
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
| **Q** ⚠️ | **"Generalise `S_n` representation theory to other categories"**, as a named programme | ⚠️ **REPAIRED — the original licensed an unhedged *"neither has any contact"* over a candidate space of exactly TWO** (FI-modules; Deligne), which omitted the named programme closest to Daniel's own phrasing and was the document's one unhedged positive assertion about the literature, covered by neither E10 nor E11. **The candidate space, enumerated:** (1) **FI-modules / representation stability** (Church–Ellenberg–Farb); (2) **Deligne's interpolation categories `Rep(S_t)`**; (3) **towers of algebras / branching graphs** (Bergeron–Li; Bergeron–Lam–Li), where a tower yields a branching graph generalising Young's lattice — *the closest match to Daniel's phrase "generalise the whole **Young lattice** paradigm to various combinatorial categories"*, and the one the original never named; (4) **differential posets** (row K) and (5) **dual graded graphs** (row L), which are the Young-lattice-generalising programmes proper and which (3) links to directly; (6) the **Okounkov–Vershik branching-graph** approach and its transport to other towers (Hecke algebras, wreath products); (7) **diagram algebras** via Schur–Weyl duality (partition, Brauer, Temperley–Lieb). **The answer is now a hedge, not a "no":** for (1) and (2) I looked and found no contact, and for (4) and (5) rows K and L report the same — all of that is a **REPORT ON A SEARCH** (E10), not a claim about the literature. **For (3), (6) and (7) I make no claim in either direction: I did not test them.** What is positively established is only where *this* construction sits: monoid / category representation theory over a support lattice (rows A, D, J). §8 R5 |

---

## L2 — THE HONEST DELTA, ITEM BY ITEM

Every claim reduced to **instance / special case / generalisation / adjacent**, with the reason.
"Adjacent" is used where it is the true answer.

| repo object | verdict | reason |
|---|---|---|
| the monoid `F(P)` of `P`-compatible ordered set partitions | **INSTANCE** | = Brown §4.3's LRB of chains in `J(P)` (measured: 0 bad of ⚠️ **936 261** product pairs, `n ≤ 5`); = MSS Example 2.14's ranking COM `R(P)`, defined there in the repo's own words; = Brown §4.1's `G` for `A` = braid, `U` = order cone — the last **now measured** by mg-d673 from a numeric realisation of the braid arrangement, 0 bad on all 86 posets at `2 ≤ n ≤ 5`, which is this document's own pre-filed item 2 |
| the states `L(P)` = chambers | **INSTANCE** | Brown §4.1's `D`; BCK/MSS: *"the topes of `R(P)` are the linear extensions of `P`"* |
| **closure** of `P`-compatibility under the product (repo's "ours" #1) | **SPECIAL CASE** | Brown §4.1 proves it in one line for *any* convex set of chambers. The repo's proof is correct and independent; it is not new |
| **the acyclic-quotient description of the levels** (repo's "ours" #2) | **SPECIAL CASE** | Czédli–Lenkehegyi (1983), quoted as Thm 3.3 in Jenča–Sarkoci: `ρ` is an order-congruence ⟺ `ρ = Ker f` for an order-preserving `f : P → Q`. Composing `f` with a linear extension of `Q` makes the codomain a chain at no cost, which is exactly the repo's "topological sort" direction |
| the support lattice `AC(P)` | **INSTANCE of a named object** | `AC(P) = O(P)`, the lattice of order congruences. Verified against the two published definitions setwise, and against Jenča–Sarkoci's homotopy theorem numerically — see §3 |
| `AC(P)` is a lattice, closed under common refinement, **not** a sublattice of `Π_n` (repo §2.6 / row Q7) | **KNOWN** | `O(P)` is an algebraic lattice (Sturm 1977, Thm 30); Jenča–Sarkoci give the meet as blockwise intersection and the join by a transitive-closure construction that is *not* `Π_n`'s join. The repo's contribution here is the **frequency** (7/16 at `n=4`, 49/63 at `n=5`), which I did **not** locate |
| antichain ⟹ `AC(P) = Π_n` | **KNOWN** | Jenča–Sarkoci Example 3.5 |
| chain ⟹ `\|AC(C_n)\| = 2^{n−1}`, Boolean, blocks convex (repo §2.3 / row Q5) | **KNOWN** | Jenča–Sarkoci Example 3.6, stated exactly |
| `AC(P)` is ranked by `n − \|π\|`; atoms are the `π_{a,b}` for `a ⋖ b` or `a ∥ b` | **KNOWN** | Jenča–Sarkoci §3; also Körtesi–Radeleczki–Szilágyi: `O(P)` is **graded and relatively complemented**. Not currently in the repo; recorded here as available |
| the eigenvalue rule `λ_X = Σ_{supp ≤ X} w` | **INSTANCE** | Brown Theorem 2 |
| the multiplicity rule (triangular counting identity) | ⚠️ **INSTANCE — and *not* a weaker form of the published one** | Brown's (10) is the same identity; his Theorem 2 solves it in closed form, and **the closed form returns the same multiplicities at every level**: two-sided comparison, 0 disagreements at all 39 616 levels to `n ≤ 6`. The gain is *informativeness* (the zero levels are named without a solve), not sharpness. ⚠️ *"a weaker form of the published one" is withdrawn — it is the "strictly sharper" claim in another costume, and it is refuted. §8 R3* |
| `m_X = ∏_B(\|B\|−1)!` on the antichain (repo §7) | **KNOWN** | the specialisation of `\|μ(X,V)\|` to `M_0 = Π_n` |
| the worked example `P = {a<b, c<d}` | **the same example** | Brown uses it to illustrate Theorem 2: the six chambers and the lune in §4.1, the eigenvalue table and the `6 × 6` matrix in ⚠️ **§4.2** |
| Ayyer–Klee–Schilling promotion chains | **ADJACENT** | same states, different monoid, 𝓡-trivial not LRB, eigenvalues only for rooted forests |
| Björner's greedoid walk on the poset shelling antimatroid | **ADJACENT** ⚠️ *(the verdict survives; its stated reason was false and is replaced)* | word-moves only; support lattice is the greedoid flat lattice, Boolean at the antichain, so the riffle shuffles are absent. ⚠️ **Not a submonoid of `F(P)`** — the band is not even a subset (words, not partitions; the map is never injective) and at the antichain it is strictly larger at `n = 2, 3`. **A homomorphic image of it is a submonoid of `F(P)`, proper for `n ≥ 3`.** §8 R2 |
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
one shape. ⚠️ **The answer is yes — but the date is the 2010s, not 2000, and the two halves of that
sentence must not be run together.** *Covered* by one theorem since Brown 2000: his §4.1–4.2 is
stated at a generality that contains both ends, and I verified that directly. *Treated as one
object* only in the 2010s: the two sources that do treat the pair as a single object — MSS's memoir
and Bandelt–Chepoi–Knauer's COMs — are both from that decade, and Brown **does not spell the pairing
out in those words**, which is exactly what this document's own ledger row E9 says about itself.
⚠️ *The original read "and it has been yes since 2000", which dates the treatment by the coverage.
§8 R6.*

**Brown §4.1–4.2 is the single covering theorem, and the two ends are its two extreme cases** ⚠️
*(originally "the single paradigm" — covering is what is established; treating the pair as a paradigm
is what MSS and BCK do, and they are later)*. The setup is: an
arrangement `A`, and a **convex set of chambers** `D` cut out by sign conditions. Then

* take the sign condition set `J = ∅`: `U` is the whole space, `D` is **all** chambers, `G` is the full
  face monoid — this is the braid/BHR/Brown–Diaconis case, states `S_n`, support lattice `Π_n`;
* take `J` = the relations of `P`: `U` is the **order cone**, `D` is `L(P)`, `G` is `F(P)` — this is
  the poset case, support lattice `O(P)`.

**One theorem covers both**, with the same eigenvalue formula and the same Möbius multiplicities, and
Brown's Theorem 2 is stated at exactly the generality that contains the pair. The intersection lattice
`M_0` interpolates: it is all of `Π_n` at one end and the antichain-blocked, acyclic-quotient order
congruences at the other. So the pairing is **not** an unstudied juxtaposition of two separately-known
halves — it is one published theorem, one of whose worked examples *is* an order cone ⚠️ *(originally
"the poset half is one of the three examples Brown chose to write out": Brown presents the
`x₁>x₂, x₃>x₄` lune as a lune in the braid arrangement, not as the order cone of a poset — the
identification is this document's, and it is correct, but it is ours and not his)*.

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
are exactly the levels **all of whose blocks are antichains of `P`** ⚠️ **and whose quotient is
acyclic**, which is what `M_0` means and what the note does not say. ⚠️ *Repaired: the original
stopped at "antichains of `P`, which is what `M_0` means". Both conditions are live and neither
implies the other — a block containing a related pair is excluded by the first, and the flat `ad|bc`
of `P = {a<c, b<d}` passes the first and fails the second. The reason the omission is invisible in
this table is that the rows of this table are the levels of `AC(P)`, where acyclicity holds by
construction; §8 R1 runs the same rule over **all** flats, where it fails.*

### 3.3 `chains_in_JP.py` — is `F(P)` Brown's §4.3 band?

| `n` | classes | moves | C1 chains ↔ moves | C2 products correspond | C3 maximal ↔ linear ext |
|---|---|---|---|---|---|
| 1 | 1 | 1 | 0 bad of 1 | 0 bad of 1 pairs | 0 bad of 1 |
| 2 | 2 | 5 | 0 bad of 2 | 0 bad of 13 pairs | 0 bad of 2 |
| 3 | 5 | 37 | 0 bad of 5 | 0 bad of 321 pairs | 0 bad of 5 |
| 4 | 16 | 397 | 0 bad of 16 | 0 bad of 13 853 pairs | 0 bad of 16 |
| 5 | 63 | 5 757 | 0 bad of 63 | **0 bad of 922 073 pairs** | 0 bad of 63 |
| **`n ≤ 5` total** ⚠️ | **87** | **6 197** | **0 bad of 87** | **0 bad of 936 261 pairs** | **0 bad of 87** |

⚠️ *The total row is added because the original quoted this table's `n = 5` row as if it were the
`n ≤ 5` total, in §0 item 1, in the L2 table and in ledger row E1 — a real slip in the conservative
direction, and one that cannot be made again with the totals written down. §8 R4.*

The move counts `1, 5, 37, 397, 5 757` are the note's own (its §2 sweep quotes `5 757` at `n = 5`), and
the worked example returns 26 moves and 6 maximal chains against the note's 26 and 6.

---

## 4. REPRODUCE

```
cd code/landscape_ebd8       && ./run_all.sh   # ~12 min, pure Python 3 — the original
cd code/landscape_repair_1953 && ./run_all.sh  # ~1 min, pure Python 3 — the repairs (§8)
```

Committed outputs: `out_identify_lattice.txt`, `out_brown_theorem2.txt`, `out_chains_in_JP.txt`;
and, for the repairs, `out_closed_form_outside_AC.txt`, `out_repaired_claims.txt`,
`out_selftest.txt` (101 assertions, including the enumeration against A000112, A000522 and
A000670, and every number §8 carries — it fails loudly if the document and the instruments drift).
The audit that found the defects reproduces from `code/landscape_audit_d673/run_all.sh` (~1.5 min).

---

## 5. CLAIM LEDGER

| # | claim | status | scope |
|---|---|---|---|
| **E1** | the monoid `F(P)`, its product, and its chambers are Brown (2000) §4.3's LRB of chains in `J(P)` | **MEASURED + QUOTED** | bijection and product correspondence exhaustive at `n ≤ 5` (⚠️ **936 261** pairs over ⚠️ **87** classes, 0 bad — the original quoted the `n = 5` row, 63 and 922 073, as the `n ≤ 5` total); the quotation is from the arXiv PDF. **Independently re-established by mg-d673 with products formed by lattice joins and meets only** |
| **E2** | the spectral result is Brown's **Theorem 2** (convex set of chambers), whose multiplicities are `\|μ(X,V)\|` in closed form ⚠️ **on the flats meeting `U` — every block an antichain of `P` AND the quotient acyclic** | **MEASURED + QUOTED**, ⚠️ **the specialisation REPAIRED** | 0 disagreements over 318 classes / 37 029 levels at `n ≤ 6`; theorem quoted verbatim. ⚠️ The *statement* of the specialisation dropped acyclicity and was **false off `AC(P)`** (§0 item 2, §8 R1); the *measurement* is sound because it ran on `AC(P)`. ⚠️ Theorem 2 is **more informative, not sharper**: 0 disagreements in a two-sided comparison at all 39 616 levels to `n ≤ 6` (§8 R3) |
| **E3** | `AC(P)` is the lattice `O(P)` of order congruences (Sturm; Czédli–Lenkehegyi; Körtesi–Radeleczki–Szilágyi; Jenča–Sarkoci) | **MEASURED + QUOTED** | two definitions agree setwise on all ⚠️ **404** classes at `2 ≤ n ≤ 6` (`identify_lattice.py`'s own range; 405 is `1 ≤ n ≤ 6`, which is not this test's population); JS's homotopy theorem reproduced via Möbius on all of them. **`AC(P) = O(P)` independently re-established by mg-d673 from Czédli–Lenkehegyi's definition with no acyclicity test anywhere, 0 disagreements on 87 posets to `n ≤ 5`** |
| **E4** | `F(P)` is MSS Example 2.14's **ranking COM `R(P)`**, origins in Reiner's 1992 Memoir, defined there in the repo's own words | **QUOTED** | quotation from `arXiv:1508.05446`; Reiner's Memoir itself **not read** (not freely available) |
| **E5** | Brown's §4.1 illustration is the repo's worked example `P = {a<b, c<d}` | **QUOTED + MEASURED** | Brown lists the six chambers and the lune in **§4.1**; the eigenvalue table and the `6×6` matrix are in ⚠️ **§4.2** *(the original attributed both to §4.1)*; our count is 6. mg-d673 checked that the six permutations Brown lists are exactly the linear extensions |
| **E6** | the repo's two "ours" items are a special case of Brown §4.1 and of Czédli–Lenkehegyi respectively | **READING OF QUOTED SOURCES** | both sources quoted; the reading is mine and is the kind of thing an audit should attack first |
| **E7** | Ayyer–Klee–Schilling is a different monoid on the same states, LRB-adjacent, rooted forests only | **QUOTED** | abstract quoted verbatim |
| **E8** ⚠️ | ⚠️ **REPLACED.** Björner's greedoid LRB applied to the poset shelling antimatroid maps onto `F(P)` by a monoid **homomorphism** whose **image** is a submonoid of `F(P)`, **proper exactly for `n ≥ 3`**; the band itself is **not** a submonoid of `F(P)` | **MEASURED** ⚠️ *(was: "a proper submonoid of `F(P)`", **READING**, not measured — and false)* | homomorphism, image inside `F(P)`, image closed under the product, identity in the image, all 63/63 at `n = 5`; proper 5/5, 16/16, 63/63 for `n = 3, 4, 5` and **not** proper 2/2 at `n = 2`; the word-to-move map is **never** injective (0 of 63); at the antichain the band is strictly larger than all of `F(P)` at `n = 2, 3` (free LRB 5, 16 vs ordered Bell 3, 13). Measured by mg-d673 and re-measured here (§8 R2). **Scope, stated because it bounds the row:** the band built for these measurements is the one *this document identifies* (feasible words of the shelling antimatroid, greedy product), not one read off Björner's page — mg-d673 could not obtain Thm 4.15 or (4.8), and neither could I. The two cardinality findings are source-independent: they are arithmetic between A000522 and A000670 |
| **E9** ⚠️ | the pairing (set-partition end and poset-quotient end) is **covered** by one theorem, Brown §4.1–4.2 (2000); it is **treated as one object** by MSS and by Bandelt–Chepoi–Knauer, both from the 2010s | **READING OF A QUOTED SOURCE** | the `J = ∅` specialisation is immediate from his setup; he does not spell it out in those words — ⚠️ *which is why L3's "it has been yes since 2000" is repaired: **covered** since 2000, **treated** since the 2010s. §8 R6* |
| **E10** ⚠️ | differential posets, dual graded graphs, species/Hopf monoids, incidence/Möbius algebras, EI/Möbius categories, combinatorial Hopf algebras ⚠️ **and, newly booked here, FI-modules and Deligne's `Rep(S_t)`** returned **no contact** | **REPORT ON A SEARCH** | not a claim about the literature. Queries were targeted, not exhaustive. ⚠️ *Row Q's "no" over FI-modules and Deligne was the document's one **unhedged** positive assertion about the literature and was booked under no ledger row at all; it is now hedged, booked here, and its candidate space is enumerated in row Q. Towers of algebras / branching graphs, Okounkov–Vershik and diagram algebras are named there and are claimed **neither way** — they were not searched.* |
| **E11** | the `S_n`-stability theorem, the invariant `G(P)`, the join-failure frequency, and any poset-specific development of Brown §4.3 were **not located** | **REPORT ON A SEARCH** | explicitly **not** a novelty claim. §2.1 records why the fourth is the least reliable negative |
| **NOT CLAIMED** | that anything here is new; that anything here is publishable; that the searches were exhaustive; anything about `λ₂`, `Δ_AT` or the pricing; anything about Aguiar–Mahajan §6.4 beyond its existence as a pointer; anything from Reiner's Memoir beyond MSS's attribution | | |

---

## 6. PRE-FILED AUDIT — where to attack this document

Filed in advance, per arc convention, and ordered by how much I expect them to yield.

> ⚠️ **EXECUTED. mg-d673 ran items 1, 2, 3, 5 and 6 and item 1 and item 3 both returned BROKEN —
> exactly as this list predicted, in the order this list predicted. The outcomes are recorded
> under each item below; item 4 (the six unread primary sources) remains open and is now the
> largest hole in this document by a wide margin.** The scoreboard is the point: a pre-filed
> audit is worth what it catches, and this one named its own two false derivations before
> anyone else read it.

1. **E8 is the weakest link.** The claim that Björner's greedoid band on the poset shelling antimatroid
   is a *proper submonoid* of `F(P)` is a derivation from his (4.8) and Thm 4.15, **not measured**. An
   auditor should build both and compare. If it is wrong, the "adjacent" verdict in the L2 table for row
   H is wrong with it. Nothing else in the document depends on it.
   ⚠️ **RESULT: BROKEN.** It was wrong, and it also contradicted the sentence beside it. The
   "adjacent" verdict **survives** — as predicted, nothing else depended on it — but on a corrected
   reason: a homomorphic **image** of the band is a submonoid, proper for `n ≥ 3`. Row H, L2 and E8
   are repaired; §8 R2.
2. **E6 is a reading, and readings are where this arc breaks.** Specifically: does Brown's §4.1
   *"`G` is a subsemigroup of `F`"* really cover the repo's closure statement, given that Brown's `G` is
   defined by `σ_i(G) ≥ 0` and the repo's by a block-order condition? I believe the two definitions
   coincide, and `chains_in_JP.py` establishes the resulting monoids coincide — but the *sign-condition
   to block-order* translation is asserted in prose and never measured on its own.
   ⚠️ **RESULT: HOLDS, and is now measured.** mg-d673 realised the braid arrangement numerically,
   read sign vectors off coordinates, and compared `G = {F : σ_i(F) ≥ 0}` with `F(P)` and the Tits
   product with the repo's: **0 bad on all 86 posets at `2 ≤ n ≤ 5`, all three columns.**
3. **The `M_0` translation.** I read *"`M_0` consists of the `X ∈ L` that intersect `U`"* and derived
   *"every block an antichain of `P`, quotient acyclic"*. `brown_theorem2.py` confirms the **consequence**
   (the closed form matches on 37 029 levels) but not the derivation. A wrong derivation that happens to
   produce the right set is possible and would be exactly this arc's signature failure.
   ⚠️ **RESULT: BROKEN — and it is the signature failure, in the precise form named here.** The
   derivation quoted in *this item* is the right one; the derivation written into §0, §3.2 and E2
   **dropped "quotient acyclic"**, and the code, by ranging over `AC(P)`, measured a set on which the
   wrong statement is right. Repaired throughout, and the missing clause is now exercised **off**
   `AC(P)`, where it fails: §8 R1.
4. **Attack the negatives.** E10 and E11 are search reports. The cheapest attack is to find one hit in
   any of the six empty neighbourhoods, or to find the `S_n`-stability statement in the order-congruence
   literature. I searched Sturm's three papers only through their citation in Jenča–Sarkoci; **I did not
   read Sturm, Czédli–Lenkehegyi, Körtesi–Radeleczki–Szilágyi, Bandelt–Chepoi–Knauer, Reiner, or
   Aguiar–Mahajan in the original.** Six unread primary sources is the largest hole here.
5. **Check the sign convention in P2.** `μ(0̂,1̂) = (−1)^{n−1}·s` was derived from "wedge of `s` spheres
   of dimension `n−3`" via the reduced Euler characteristic. It passes on ⚠️ **402** posets, which is
   strong, but the exponent was derived and not quoted.
   ⚠️ *Repaired: "405 posets" was wrong. P2 is `n/a` for `n < 3` — its own committed output says so —
   so its population is the classes with `3 ≤ n ≤ 6`, which is `5 + 16 + 63 + 318 = 402`. §8 R4.*
   ⚠️ **RESULT: HOLDS.** mg-d673 re-derived the exponent independently and it passes on all 402.
6. **The disconnected case.** P2 uses `e_C(P)` for disconnected `P`, implementing Jenča–Sarkoci's
   Definition 4.1 as ⚠️ **all** cyclic rotations of the word, closed up by union-find. If that
   relation is not transitive as they assert, my union-find implementation computes a coarser
   equivalence than theirs and P2's passes on the 80 disconnected classes at `n = 6` would be
   checking a different statement.
   ⚠️ *Repaired: this originally said **single** cyclic rotation. The code
   (`identify_lattice.py:316–320`) loops `k = 1..n−1` — all rotations. The distinction is not
   pedantic: mg-d673 built the single-rotation version **as this item described it** and it
   disagreed with the Möbius function on 5 posets to `n = 5`. The item pointed a future auditor at a
   risk the code does not carry, and in doing so described away the reading that does fail. The code
   is better than its description was.*
   ⚠️ **RESULT: the description was wrong, the code was right, and the residual worry is now
   evidenced against.** The single-rotation reading disagrees with the Möbius function; the
   all-rotations reading reproduces it on every poset to `n = 6`, disconnected ones included. That is
   not a proof that Jenča–Sarkoci's relation is transitive — the union-find closes it transitively
   either way — but it is agreement with a topological invariant computed independently of this
   programme, which the coarser-than-theirs scenario would have to explain away.

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

⚠️ **Second operational consequence, added by the repair and pointing the other way.** The claim in
this work item's commit subject that **Brown's Theorem 2 is "STRICTLY SHARPER" than what the repo
uses is refuted** (§0, §8 R3). Brown returns the *same* multiplicities at every one of 39 616 levels
to `n ≤ 6`. **A ticket to adopt Theorem 2 on the grounds that the repo is using a weaker tool would
rest on a false premise, and must not be filed on that basis.** What survives is a smaller and true
consequence: the spectrum-carrying levels can be *named* instead of *solved for*.

---

## 8. THE REPAIR RECORD (mg-1953)

**What this section is.** mg-d673 audited this document and returned *identifications hold,
overstated, with 2 BROKEN* — and **both BROKEN items were in material the ticket explicitly
forbade**: *"do not develop new mathematics — this is a locating exercise."* This document derived
three things and got two of them wrong, while getting **everything it located, quoted and measured
right**. The repairs below touch only the derivations and the document's arithmetic about its own
instruments. **The locating is not re-opened**, and it does not need to be: the audit re-tested each
identification as an *equality built from the published definitions* — a stronger test than the one
run here — and all three held.

**Nothing below rests on the auditor's word.** Every repaired sentence is re-measured in
`code/landscape_repair_1953/`, written from scratch and sharing no code with `code/landscape_ebd8/`
(this document's instruments) or `code/landscape_audit_d673/` (the audit's). Its poset enumeration
is certified against A000112 (`1, 2, 5, 16, 63, 318`), and it reproduces the two numbers the audit
reported independently: **455** spurious flats at `n = 6`, and the `n = 4` witness — which it finds
as `P = {a<c, b<d}` with spurious flat `ad|bc` where the audit found `P = {a<d, b<c}` with `ac|bd`.
**Those are the same isomorphism class** (two disjoint 2-chains) under a different labelling, which
is what an independent enumeration should be expected to produce and is a small check on both.

| # | what was wrong | what it says now | evidence |
|---|---|---|---|
| **R1** | **BROKEN.** The closed form was stated as *"`m_X = ∏(\|B\|−1)!` if every block of `X` is an antichain of `P`, and `0` otherwise"* — dropping **acyclicity**, which `brown_theorem2.py`'s own docstring carries. False, not abbreviated: the *"0 otherwise"* ranges over all flats. §0 item 2, §3.2, E2 | the antichain condition **and** *"the quotient `P/X` is acyclic"*, at every site | `out_closed_form_outside_AC.txt`. **R1a, the derivation:** `M_0` = flats meeting the open cone `U`, decided **by construction** (exhaustive search for an ordering of the blocks sending every relation forwards — no acyclicity test on that side) — equals the repaired rule **0 bad of 318** at `n = 6` and fails the original rule on **1 of 16** (`n=4`), **10 of 63** (`n=5`), **101 of 318** (`n=6`). **R1b, the consequence:** Brown's `Σ_X m_X = \|L(P)\|` over **all 64 554 flats** at `n = 6` — original rule fails on the same posets, **455 spurious flats**; repaired rule **0 bad** at every `n ≤ 6`. **R1c:** witness `P = {a<c, b<d}`, `\|L(P)\| = 6`, original sums to **7** on the spurious flat `ad\|bc`. **R1d, the control that must fire:** restricted to `AC(P)`, the original rule is **0 bad of 318** — so the restriction is *demonstrated* to be what hid the defect, not merely alleged to be |
| **R2** | **BROKEN.** E8 / row H / L2 row H: Björner's greedoid band is *"a proper submonoid of ours"* — impossible, and contradicting *"this is the free LRB"* in the same cell | a monoid **homomorphism** whose **image** is a submonoid of `F(P)`, **proper exactly for `n ≥ 3`**; the band itself is not a submonoid. **ADJACENT survives, on a corrected reason** | `out_repaired_claims.txt`. Homomorphism, image ⊆ `F(P)`, image closed under the product, identity in the image: **all 63/63** at `n = 5`. Injective: **0 of 63**. Proper: **0/2** at `n = 2` (the image is *all* of `F(P)`), **5/5, 16/16, 63/63** for `n = 3, 4, 5`. At the antichain the band is strictly larger than the whole of `F(P)`: **5 vs 3** and **16 vs 13** at `n = 2, 3` (A000522 vs A000670) |
| **R3** | **REFUTED — the commit subject's own headline.** *"Brown's Theorem 2 is STRICTLY SHARPER than what the repo uses"*, and its restatement in the L2 table as *"a weaker form of the published one"* | **"strictly more informative"** — this document's own phrase — everywhere. **Brown's answer is the same answer** | `out_repaired_claims.txt`. Two-sided, level by level, repo's triangular solve vs the repaired closed form: **0 disagreeing levels of 39 616** to `n ≤ 6` (4, 24, 206, 2 353, 37 029 by `n`), **0 posets bad of 404**. What Theorem 2 adds, counted: **28 988 of 37 029** levels at `n = 6` (**1 674 of 2 353** at `n = 5`) carry zero and are named *a priori* instead of discovered by a solve |
| **R4** | **MINOR, arithmetic about its own instruments.** E3's *"405 classes"*; §6 item 5's *"405 posets"*; *"0 bad of 63 classes"* and *"922 073 pairs"* quoted as `n ≤ 5` totals; the `6×6` matrix attributed to §4.1; *"one place where the literature is ahead"* followed by a second; *"thirty years old"* for a 2000 paper | **404** (`2 ≤ n ≤ 6`, `identify_lattice.py`'s own range); **402** (`3 ≤ n ≤ 6`; P2 is `n/a` for `n < 3`); **87** classes and **936 261** pairs, with a total row added to §3.3 so the slip cannot recur; **§4.2**; *"two places"*; **twenty-six** | `out_repaired_claims.txt` R4 rebuilds every population: classes `1, 2, 5, 16, 63, 318`; moves `1, 5, 37, 397, 5 757` (total **6 197**); levels `1, 4, 24, 206, 2 353, 37 029`; product pairs `1, 13, 321, 13 853, 922 073` (total **936 261**) |
| **R5** | **MAJOR.** Row Q licensed an unhedged *"neither has any contact"* over a candidate space of **two** (FI-modules, Deligne), omitting **towers of algebras / branching graphs** — the named programme closest to Daniel's own phrasing — and it was the document's one unhedged positive assertion about the literature, booked under **neither** E10 nor E11 | the candidate space is **enumerated to seven** named programmes; the *"no"* is **withdrawn to a hedge** and booked under E10 as a report on a search; towers of algebras, Okounkov–Vershik and diagram algebras are claimed **neither way** | not a measurement — a scope repair. **The finding is the candidate space, not a claim that any of those programmes has contact**, and this document does not make one. This is the second negative in this arc built on an unenumerated candidate space; a negative is worth its enumeration and no more |
| **R6** | **MAJOR.** L3's *"the answer is yes, and it has been yes since 2000"* dated the *treatment* by the *coverage*: the 2000 support is E9, whose own ledger line says Brown *"does not spell it out in those words"*, while the two sources that do treat the pair as one object are from the 2010s. Same slip in *"the poset half is one of the three examples Brown chose to write out"* | **covered** by one theorem since **2000**; **treated as one object** since the **2010s**. Brown's lune is presented as a lune in the braid arrangement — reading it as an order cone is *this document's* identification, correct and ours | E9 rewritten to carry both halves; L3 and its follow-on sentence repaired in place |

**Two things this repair deliberately does NOT do.** It does not re-open the locating — §§1–3's
identifications are confirmed and the audit's own re-tests are cited, not re-run. And it does not
touch `docs/OneThird-Semigroup-Walk-Family-Note.md`, `STATE.md`, `λ₂`, `Δ_AT` or the pricing; §7's
recommendation still stands unexecuted and is still pm-onethird's call.

**Also from the audit, and NOT repaired here, named so it is not mistaken for done:** its **M8** —
that §0 states *"It is Czédli–Lenkehegyi's theorem, from 1983"* flatly while E6 books the same claim
as a **READING** and §6 item 4 admits the 1983 paper was not read in the original. The audit's
instruments settle that `AC(P)` **is** the order-congruence lattice as the modern literature defines
it; they do not settle that *Sturm 1971 or Czédli–Lenkehegyi 1983 state it*, and that distinction —
*the object is the same* (established) versus *the 1983 paper says so* (a citation chain) — is not
yet visible in §0. It is outside this repair's enumerated brief and is left open on purpose.
