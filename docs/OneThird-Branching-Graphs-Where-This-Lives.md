# Towers of algebras and branching graphs: does this construction meet them?

**Work item:** mg-af28. **Date:** 2026-07-30. **Computation:** permitted, used, committed
(`code/branching_af28/`, `run_all.sh`, ~5 min, 27-assertion self-test).

**What this document is.** mg-d673's MAJOR finding was that row Q of
`docs/OneThird-Landscape-Where-This-Lives.md` licensed a *"no"* about the literature over a
candidate space of **two** — FI-modules and Deligne — omitting **towers of algebras /
branching graphs**, the named programme closest to Daniel's own phrasing. mg-1953 repaired
the document by withdrawing the *"no"* to a hedge and enumerating seven candidates; it did
**not** run the search, and said so. **This document runs it.** It does not touch row Q,
which mg-1953 owns.

**Scope, and it is the whole of the scope.** This is a locating exercise. It contains **no
publishability verdict and no novelty claim**. Where I did not find something I say *"not
located"*, which is a statement about my search and not about the literature. Every
relationship is reduced to **instance / special case / generalisation / adjacent / no
contact**, with a reason, and every identification is tested as an **equality** built from
the published definitions rather than asserted as a resemblance.

---

## 0. THE HEADLINE

**There is contact. It is exactly one identification, it is an equality, and it runs the
opposite way from the one the question presumes.**

> **The branching graph of the tower `ℂS_1 ⊂ ℂS_2 ⊂ ⋯` is Young's lattice, and Young's
> lattice is a distributive lattice. Its finite intervals `[∅, λ]` are exactly the `J(P)`
> for `P` a cell poset `D_λ`. So `F(D_λ)` is Brown §4.3's band on `[∅, λ]`, and the repo's
> states `L(D_λ)` are the standard Young tableaux of shape `λ` — which are, by
> Okounkov–Vershik, the Gelfand–Tsetlin basis of the irreducible `S^λ`.**

Measured, not asserted: over all **44 partitions to `n ≤ 7`**, the map "order ideal ↦ the
shape it fills" is an order isomorphism `J(D_λ) → [∅, λ]` — **0 bad**, checked on every
pair in both directions — and the maximal chains of `J(D_λ)` are exactly `SYT(λ)`, with
`e(D_λ) = f^λ` against an independently computed hook length formula, **0 bad**
(`out_young.txt`, T1). The two sides are built from different definitions: the left from
order ideals of the cell poset, the right from containment of Young diagrams and from
row-and-column-increasing fillings.

**Three consequences, and the third is the one that matters.**

1. **The direction is "ours contains theirs", not "theirs contains ours".** The repo's
   family ranges over *all* finite posets; the branching-graph programme's distributive
   piece is the cell posets. That is a **vanishing** fraction: **6 of 318** at `n = 6`,
   **8 of 2 045** at `n = 7`, **12 of 16 999** at `n = 8` (T2). So on the index sets, this
   construction **generalises** the Young case.

2. **Nothing else transfers, and the reasons are theorems rather than absences.** §2
   enumerates them: finiteness kills the differential condition outright; distributivity
   singles out Young's lattice — it is the only *distributive* 1-differential lattice
   (Stanley 1988), and the other known 1-differential lattice measurably is not
   distributive; the algebra `kF(P)` has
   **all irreducibles one-dimensional**, so a Bratteli diagram built from it carries no
   multiplicity data at all; and the monoid does not act by invertible maps, so it is not
   the `S_n`-action on the Gelfand–Tsetlin basis.

3. **Brown does not make the identification, and I did not locate it on the other side
   either.** Brown's paper — the located home of this
   construction — contains **zero** occurrences of *Young*, *tableau*, *Bratteli*,
   *branching*, *differential*, *Gelfand*, *Okounkov*, *Vershik*, *Fomin*, *dual graded*
   or *tower of algebras*, against live controls of 8 *distributive lattice*, 19 *maximal
   chains*, 6 *left regular band*, 28 *Tsetlin*, 24 *derangement* (`out_scan_brown.txt`).
   His worked `§4.3` example is the `p × q` grid of lattice paths (the "kids walk" is
   `§4.4`); that grid is `J(C_p ⊔ C_q)`, which for `p, q ≥ 1` is **not** an interval of
   Young's lattice — `D_λ` has a minimum and `C_p ⊔ C_q` does not. And I did not locate
   the identification on the branching-graph side either (§3, rows 4–7).

**The harshest available reading of consequence 1, stated because this is where enthusiasm
would be the expensive error.** The identification is about **index sets**. `SYT(λ)` is our
state space at `P = D_λ` and it is the Gelfand–Tsetlin basis of `S^λ` — but the walk's
operators are idempotent and non-invertible (T6: **0** moves out of 6 197 to `n ≤ 5` act
bijectively without acting as the identity), so they are not group elements, and the walk's
spectrum is indexed by the order-congruence lattice `O(D_λ)`, which is not a
representation-theoretic invariant of `S_n`. What is established is that the two programmes
**share this set**. Whether the walk interacts with the `S_n`-structure carried on it is
**untested**, and testing it would be new mathematics, which this ticket forbids.

---

## 1. WHAT THE PROGRAMME ACTUALLY REQUIRES, AND WHAT WE HAVE

Tested against the published definitions, one hypothesis at a time.

| the programme's hypothesis | what we have | verdict |
|---|---|---|
| **Bergeron–Li axiom (2)**: *"The (external) multiplication `ρ_{m,n} : A_m ⊗ A_n → A_{m+n}` is an injective homomorphism of algebras, for all `m` and `n` (sending `1_m ⊗ 1_n` to `1_{m+n}`)"* — quoted from `arXiv:math/0612170` §3.1 | the natural candidate is block concatenation `F(P) × F(Q) → F(P ⊔ Q)`. **Measured over all 64 pairs with `|P|,|Q| ≤ 3`:** it always lands in `F(P ⊔ Q)` (0 bad), is always injective (64/64), is always a semigroup homomorphism (0 bad products) — and is **unital in 0 of 64 cases**, because it sends `(1_P, 1_Q)` to the two-block move | **axiom fails** for this map. Whether another map satisfies it is not decided here |
| a tower is **`ℕ`-graded**: `A = ⊕_{n≥0} A_n` | our index is a *poset*, not an integer. An `ℕ`-indexed subfamily closed under the `⊔` that the external product needs satisfies `P_m ⊔ P_n = P_{m+n}`, hence `P_n = P_1^{⊔n}` (elementary, and **ours** — flagged as a derivation, not a citation) | at `P_1` = a point this is the **antichain** sequence, i.e. the classical braid case; no poset-specific tower located |
| **Okounkov–Vershik** runs on an inductive family of **semisimple** algebras, and builds the Gelfand–Tsetlin algebra as a maximal commutative subalgebra, which is maximal *iff the branching graph has no multiple edges* | `kF(P)` is very far from semisimple: measured `dim kF(P)/rad = |AC(P)|` on **all 87 classes to `n ≤ 5`** and **308 of 318 at `n = 6`** (10 over the size cap, each listed), **0 bad**. At the `n = 5` antichain that is `541` against `52` — the radical is **90.4%** of the algebra, and **95.7%** at `n = 6` | **hypothesis fails.** OV supplies the *indexing* of our state space at `P = D_λ` and nothing else |
| a **branching graph / Bratteli diagram** records restriction multiplicities of irreducibles | Brown: this class of semigroups has irreducible representations that *"can be worked out explicitly (they are all 1-dimensional)"*, indexed by the support lattice — corroborated by the measurement above | **no multiplicity data exists to record.** Any Bratteli diagram here has the support lattice as vertex set and multiplicities 0/1 by construction |
| **Stanley's differential condition** `DU − UD = rI`, `r ≥ 1` | fails for **every** finite `J(P)`: `U(1̂) = 0` while `UD(1̂) ∋ 1̂`. Measured over all **405 classes to `n ≤ 6`**: **0** satisfy it; with the top rank exempted, **exactly 1** does, and it is the one-element poset. **Positive controls in the same code path**: Young's lattice to rank 8 and the Young–Fibonacci lattice to rank 8 both return `r = 1` | **no contact**, and the obstruction is finiteness, so it is not a near miss |
| **Brown §4.3** needs a finite **distributive** lattice | of the two *known* 1-differential lattices, only Young's is distributive. Measured: **all 30 intervals `[∅, λ]`, `|λ| ≤ 6`, of Young's lattice are distributive (0 bad)**; **5 of the 33 intervals `[∅̂, w]`, `rank(w) ≤ 6`, of the Young–Fibonacci lattice are not**, smallest witness `w = 221` | the construction **reaches the Young graph and no other differential poset** |

---

## 2. WHY THE CONTACT DOES NOT EXTEND — ENUMERATED

This ticket exists because a *"no"* was given without an enumeration. So each reason is
named, with the measurement or the citation that carries it.

1. **Finiteness.** Differential posets and dual graded graphs are locally finite with a
   `0̂` and infinitely many ranks; `J(P)` for finite `P` is finite with a `1̂`. The
   identity fails at `1̂` for elementary reasons and this is not repairable by truncation
   (T3: 0 of 405; with the top rank exempted, 1 of 405, the one-element poset). *A
   truncation of an infinite lattice is not even a lattice — two elements of top rank lose
   their join — which is why T8 tests intervals and not truncations.*

2. **Distributivity.** Stanley (1988): *"Young's lattice is the only 1-differential
   distributive lattice"*; Byrnes (2012) is reported to have shown that Young's and
   Young–Fibonacci are the only 1-differential lattices at all. *(Both statements taken
   from the Wikipedia article on differential posets; **I read neither original**, and my
   argument uses only the first.)* The logic needs only Stanley: Brown §4.3's hypothesis is
   *distributive lattice*, and a differential poset that is a distributive lattice is
   Young's — so Young's is the **only** differential poset his construction can consume,
   whatever the full classification of differential lattices turns out to be. T8 measures
   the illustrative case: Young–Fibonacci, the other known 1-differential lattice, is not
   distributive (5 of its 33 intervals to rank 6 fail, smallest witness `w = 221`).

3. **The algebra is basic, not semisimple.** T5. The programme's invariant — restriction
   multiplicities between semisimple layers — has no counterpart, because there are no
   semisimple layers and all irreducibles are one-dimensional.

4. **The action is not a group action.** T6. Every move is idempotent; the ones acting
   bijectively act as the identity map. So at `P = D_λ` the monoid is not `S_n` and the
   walk is not transport of the `S_n`-action along the Gelfand–Tsetlin basis.

5. **No tower.** §1, rows 1–2: Bergeron–Li's axiom (2) fails for the natural map, and the
   `ℕ`-grading it presupposes forces disjoint powers, which lands back at the classical
   antichain case.

6. **The one bridge that does exist consumes the symmetry we do not have.** Bidigare's
   theorem — that for a finite Coxeter group `W` with reflection arrangement `A_W`, the
   descent algebra of `W` is the algebra of `W`-invariants of the face-monoid algebra
   (**as stated in the secondary literature; I did not read Bidigare's thesis**) — is
   the documented route from face-monoid algebras into the Hopf/tower programme, since the
   direct sum of the type-A descent algebras is `NSym`, which is a Grothendieck group of
   the tower of `0`-Hecke algebras (Krob–Thibon). Its input is the full group action on the
   arrangement. The subgroup of `S_n` preserving the order cone of `P` is `Aut(P)`, and
   `Aut(P) = S_n` exactly when `P` is an antichain — so the bridge is available precisely
   at the classical end. *(That last sentence is elementary and it is **ours**: if `a < b`
   in `P` then the transposition `(a b)` is not an automorphism. I did not locate a poset
   analogue of Bidigare's theorem, and the sources for the `NSym` chain are located, not
   read.)*

7. **A Bratteli diagram exists but says nothing.** Every graded graph with a root is the
   Bratteli diagram of *some* AF algebra, so "`J(P)` is a Bratteli diagram" is true and
   empty: the tower it names is built out of `J(P)` itself. The programme's content is that
   the tower arises independently — as `ℂS_n` does for Young's lattice. *This argument does
   not depend on the exact form of the realisation theorem, which I did not read: even
   granting it in the strongest form, it carries no information about `F(P)`.*

---

## 3. THE CANDIDATE SPACE, ENUMERATED, WITH WHAT EACH RETURNED

Twelve. Seven are mg-1953's row-Q list; five more are programmes the searches surfaced as
closer or as necessary context. **A negative is worth its enumeration and no more**, so
this table is the finding, not the headline.

| # | candidate | searched? | verdict | reason |
|---|---|---|---|---|
| **1** | **FI-modules / representation stability** (Church–Ellenberg–Farb) | **no — not re-run here** | booked to E10 | mg-ebd8 searched it and reported no contact; outside this ticket's brief and not re-tested. Named so the space is complete |
| **2** | **Deligne's `Rep(S_t)`** | **no — not re-run here** | booked to E10 | as above |
| **3** | **Towers of algebras** (Bergeron–Li, `arXiv:math/0612170`; Bergeron–Lam–Li) | **yes** | **ADJACENT — axiom tested and failed** | axiom (2) quoted verbatim and tested: concatenation is injective and multiplicative but **not unital**, 0 of 64 (T7). The `ℕ`-grading forces disjoint powers. §1, §2.5 |
| **4** | **Stanley's differential posets** | **yes** | **NO CONTACT, with the theorem that says why** | finiteness (T3, 0 of 405) and Stanley's uniqueness theorem. This **upgrades** row K from *"empty"* to *"no, and here is why, and here is the one place where contact does exist"* |
| **5** | **Fomin's dual graded graphs** | **yes** | **NO CONTACT** | same finiteness obstruction; and there is no second graph on our vertex set — the programme's content is a growth/RSK bijection, which needs the pair. Context on how rigid the structure is: Gaetz (`arXiv:1803.11168`) proves that for `r = 1` or `r` prime, *"wreath products of a fixed group with the symmetric groups are the only `r`-dual tower of groups"* |
| **6** | **Okounkov–Vershik / Gelfand–Tsetlin** | **yes** | **ADJACENT — and it is the source of the one real contact** | OV needs semisimple inductive families (T5 refutes the hypothesis for us). What it supplies is the identification of `SYT(λ)` as the GT basis of `S^λ`, which is our state space at `P = D_λ`. §0 |
| **7** | **Diagram algebras via Schur–Weyl** (partition, Brauer, Temperley–Lieb, rook) | **yes** | **NOT LOCATED** | these are centraliser algebras with diagram bases and multiplicity-carrying Bratteli diagrams; I located no order-cone, order-congruence or `P`-compatible-partition object among them. A search report, not a claim about the literature |
| **8** | **Bratteli diagrams / AF algebras** in general | **yes** | **VACUOUS INSTANCE** | true and contentless; §2.7 |
| **9** | **Fulman, *Commutation relations and Markov chains*** (`arXiv:0712.1375`), down-up chains on the Young, Schur and Kingman graphs | **yes** | **ADJACENT — different state space** | his chains move on the **vertices** of a branching graph, driven by the `U`/`D` operators; ours moves on the **maximal chains**. The Plancherel growth process is likewise a measure on paths, not a Markov chain on the set of paths |
| **10** | **Okada algebras and the Okada monoid** (`arXiv:2404.16733`) | **yes** | **ADJACENT — the closest structural analogue found** | a *monoid* whose algebra tower has a differential poset (Young–Fibonacci) as its Bratteli diagram: the shape of the thing Daniel's question asks for. But it is a different monoid (aperiodic, a labelled Temperley–Lieb arc-diagram model), and the lattice it realises is the one Brown §4.3 provably cannot consume (T8). **Located from abstracts; not read** |
| **11** | **Gaetz, dual towers of groups** (`arXiv:1803.11168`) | **yes** | **CONTEXT, not contact** | rigidity of the dual-graded-graph structure; see row 5 |
| **12** | **Bidigare–Solomon → `NSym`/`QSym` → the `0`-Hecke tower** | **yes** | **the one documented bridge, and it needs the symmetry we lose** | §2.6. This is the honest answer to *"is there a route from this family into the tower programme"*: yes, at the antichain end, and it dates from the 1990s (Bidigare's thesis; GKLLRT; Krob–Thibon) — *decades stated from the secondary literature, since I read none of the three* |

---

## 4. WHAT THIS DOES TO THE FRAMING OF DANIEL'S QUESTION

His commissioned priority 2 asked whether this gives *"a generalization of rep theory of
`S_n` to other categories"*. mg-ebd8's L3 answered: the generalisation on offer is of
**face-monoid / left-regular-band** representation theory, not of `S_n` representation
theory, and both of Daniel's instances already sit inside it. **That answer is unchanged by
this ticket, and now it has been tested against the programme it had not been tested
against.** What is added is a sharper statement of where the two programmes touch:

* the **combinatorics** of the `S_n` branching graph is inside this family — the intervals
  of Young's lattice are `J(P)`s, and `SYT(λ)` is `L(D_λ)` — as a **vanishing fraction** of
  it;
* the **representation theory** of the `S_n` branching graph is not: §2 enumerates seven
  reasons, four of them hypotheses of the programme that our objects measurably fail;
* so the generalisation this construction performs on the Young paradigm is a
  generalisation of its **index set**, not of its **representation theory** — and the
  object it generalises the index set *within* is Brown's, not Okounkov–Vershik's.

**One thing I did not locate, stated as a search report and not as a novelty claim.** The
walk on `SYT(λ)` obtained by taking `P = D_λ` — Brown §4.3 applied to an interval of Young's
lattice. Brown does not mention it (§0 consequence 3); the branching-graph literature I
searched does not; Ayyer–Klee–Schilling's promotion chains on linear extensions are a
different monoid on the same states and are already booked ADJACENT at row G of the
landscape document. **Not located** is not a synonym for *new*, and this arc's negative
searches have a poor record: §5 item 3 says where I would trust this one least.

---

## 5. PRE-FILED AUDIT — WHERE TO ATTACK THIS DOCUMENT

Ordered by how much I expect them to yield.

1. **Attack the one positive claim first, because it is the only one that would be
   expensive if wrong.** `J(D_λ) = [∅, λ]` and `L(D_λ) = SYT(λ)` are measured on 44
   partitions, but the *interesting* half of §0 is the chain of three identifications:
   ours `= ` Brown §4.3's band (mg-ebd8/mg-d673, re-anchored here by T0 at `n ≤ 5`), Brown
   §4.3 applies to `[∅, λ]`, and `SYT(λ)` is the GT basis of `S^λ`. The **third** link is
   the one I did not measure: it is quoted from the Okounkov–Vershik literature, and I read
   summaries and one preprint abstract, not Vershik–Okounkov in the original.

2. **Attack §2.6.** The chain *descent algebras → `NSym` → Grothendieck group of the
   `0`-Hecke tower* is three citations deep and **I read none of the three in the
   original** — Bidigare's thesis, GKLLRT, Krob–Thibon. If any link is weaker than I have
   stated, §2.6 weakens with it. Nothing else depends on it; it is the one place where I
   assert a positive route into the tower programme.

3. **Attack the negatives at rows 7 and the "not located" in §4.** Row 7 (diagram algebras)
   is the least-searched of the twelve: partition-algebra literature is very large, and the
   search that would kill this row is one paper connecting a diagram algebra to order
   congruences or to `P`-compatible ordered set partitions. §4's *"not located"* is a
   search over an *application* rather than over an object, which is the kind of negative
   §2.1 of the landscape document already flags as least reliable.

4. **Attack the Young–Fibonacci implementation.** T8's non-distributivity result depends on
   my cover rule, which I got **wrong on the first attempt** — the differential-condition
   control refused to fire, which is how it was found. The rule now in `core_af28.py` is
   taken from the four neighbour operations stated on the Young–Fibonacci lattice page, and
   it passes the control at `r = 1` with Fibonacci rank sizes. An auditor should rebuild it
   from Stanley (1988) directly.

5. **Attack the three elementary derivations, which are mine and not citations.** (a) that
   an `ℕ`-graded `⊔`-closed family of posets is a sequence of disjoint powers; (b) that the
   stabiliser of the order cone in `S_n` is `Aut(P)`, which is `S_n` only at the antichain;
   (c) that Brown's `§4.3` example lattice `{0,…,p} × {0,…,q}` is `J(C_p ⊔ C_q)` and so, for
   `p,q ≥ 1`, is not an interval of Young's lattice. All three are one-liners, all three are
   flagged in place, and all three are the kind of thing this arc breaks on.

6. **Attack the two verbatim quotations, because of how they were obtained.** Bergeron–Li's
   axiom (2) and Brown's *"they are all 1-dimensional"* were read out of the arXiv PDFs by
   the same Flate-decode-and-extract routine as `scan_brown.py`, **not** from a rendered
   page. That routine demonstrably drops `fi` ligatures (it renders *finite* as *nite*), so
   a quotation could in principle be missing characters. Both quoted strings above are
   ligature-free and were checked by eye, but an auditor should re-read both from the
   rendered PDFs.

7. **Attack the size caps.** T5 exempts 10 of 318 classes at `n = 6` for size, each listed
   with its `|F(P)|` in `out_lrb_reps.txt`; the largest is the antichain at 4 683. The
   antichain is the classical case where Brown's theorem is least in doubt, so the
   exemption is in the safe direction — but it is an exemption.

---

## 6. CLAIM LEDGER

| # | claim | status | scope |
|---|---|---|---|
| **B1** | `J(D_λ)` is the interval `[∅, λ]` of Young's lattice, by the map "ideal ↦ shape", and the maximal chains of `J(D_λ)` are `SYT(λ)` with `e(D_λ) = f^λ` | **MEASURED** | 44 partitions, `n ≤ 7`, order isomorphism checked on every pair in both directions, 0 bad; `f^λ` against an independently coded hook length formula, 0 bad |
| **B2** | the posets `P` for which `J(P)` is an interval of Young's lattice are exactly the cell posets, and they are a vanishing fraction: 6/318 (`n=6`), 8/2 045 (`n=7`), 12/16 999 (`n=8`) | **MEASURED + CITED** | shape classes computed by canonical form; the `n ≥ 7` totals are **A000112, cited not computed**; `n ≤ 6` totals are enumerated here and agree with A000112 |
| **B3** | no finite `J(P)` is a differential poset, and none is one even with the top rank exempted (bar the one-element poset) | **MEASURED, with positive controls** | 405 classes to `n ≤ 6`. Controls: Young's lattice and Young–Fibonacci both return `r = 1` in the same code path |
| **B4** | of the two 1-differential lattices only Young's is distributive, so Brown §4.3 reaches the Young graph and no other | **MEASURED + CITED** | 30 Young intervals, 0 non-distributive; 33 Young–Fibonacci intervals, 5 non-distributive, witness `w = 221`. Stanley's and Byrnes's classification statements are **cited from a secondary source and not read** |
| **B5** | `dim kF(P)/rad = |AC(P)|`, consistent with Brown's *"they are all 1-dimensional"* | **MEASURED** | trace-form rank in exact rational arithmetic; all 87 classes to `n ≤ 5` and 308 of 318 at `n = 6`, 0 bad. **The step from this to "all irreducibles are 1-dimensional" is Brown's theorem, cited, not re-derived here** |
| **B6** | no move acts on `L(P)` bijectively without acting as the identity map | **MEASURED** | 6 197 moves over 87 classes to `n ≤ 5`, 0 |
| **B7** | block concatenation `F(P) × F(Q) → F(P ⊔ Q)` is an injective semigroup homomorphism and is **not** unital, so it fails Bergeron–Li axiom (2) | **MEASURED + QUOTED** | 64 pairs, `|P|,|Q| ≤ 3`; axiom quoted verbatim from `arXiv:math/0612170` §3.1 |
| **B8** | Brown (2000) contains none of the branching-graph vocabulary | **MEASURED** | keyword census of the arXiv PDF with five present-word controls, one of which (`left regular band`) failed on the first run because Brown hyphenates it, and was fixed in the scanner, not in the finding |
| **B9** | the candidate space is the twelve programmes of §3; rows 1–2 were **not re-run**; rows 3–6, 8–12 were searched; row 7 is the least-searched | **REPORT ON A SEARCH** | not a claim about the literature. Queries were targeted, not exhaustive |
| **B10** | the walk on `SYT(λ)` given by `P = D_λ` was **not located** in either literature | **REPORT ON A SEARCH** | explicitly **not** a novelty claim; §5 item 3 |
| **NOT CLAIMED** | that anything here is new; that anything here is publishable; that the searches were exhaustive; anything about `λ₂`, `Δ_AT` or the pricing; anything about the `S_n`-structure carried on `SYT(λ)` interacting with the walk, which is untested | | |

---

## 7. REPRODUCE

```
cd code/branching_af28 && ./run_all.sh        # ~5 min, pure Python 3
```

Committed outputs: `out_selftest.txt` (27 assertions), `out_young.txt`, `out_branching.txt`,
`out_lrb_reps.txt`, `out_scan_brown.txt`. `scan_brown.py` is the only step needing network.

---

## 8. NOTE FOR pm-onethird — SCOPE DISCIPLINE

Three things this document deliberately does **not** do.

* It does **not** edit row Q of `docs/OneThird-Landscape-Where-This-Lives.md`. mg-1953 owns
  that row and correctly withdrew it to a hedge. **Operational consequence:** row Q and
  ledger row E10 now say of towers of algebras, Okounkov–Vershik and diagram algebras that
  they are *"claimed neither way — they were not searched"*. They have now been searched.
  Whether to fold this document's §3 back into row Q is pm-onethird's call, not mine.
* It does **not** develop mathematics. Two elementary one-line derivations were needed to
  test hypotheses and are flagged in place (§2.6, §1 row 2) and pre-filed for audit (§5
  item 5). Everything else compares our objects against published descriptions of other
  objects. *This is the instruction mg-ebd8 violated twice, in exactly this position, which
  is why it is called out here rather than assumed.*
* It does **not** touch `STATE.md`, the semigroup note, `λ₂`, `Δ_AT` or the roadmap
  pricing.
