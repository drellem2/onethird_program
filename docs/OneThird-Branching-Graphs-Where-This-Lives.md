# Towers of algebras and branching graphs: does this construction meet them?

**Work item:** mg-af28. **Date:** 2026-07-30. **Computation:** permitted, used, committed
(`code/branching_af28/`, `run_all.sh`, ~6 min, 31-assertion self-test).

***Repaired 2026-07-30 by mg-41aa**, landing four findings of
`docs/OneThird-Audit-mg-af28-Branching-Graphs.md` (mg-6ad0): the two **BROKEN** items X1 and
X2, both of which were refuted by construction and both of which are on the **negative**
side, and the two re-scopings X3 and X4. **The headline is untouched and comes out stronger,
not weaker** — mg-6ad0 confirmed `J(D_λ) → [∅, λ]` as a **lattice** isomorphism, and X2's
correction says Brown's own worked example lattice **is** an interval of Young's lattice, so
the contact is closer than this document argued. Every struck sentence is quoted where it
stood. Figures in the repaired passages come from `code/branching_repair_41aa/`, which
imports nothing from `branching_af28/` or `branching_audit_6ad0/`; the reasoning, and a
per-claim statement of what was checked and what a falsifier would have looked like, is in
`docs/OneThird-Branching-Graphs-Repair.md`. **mg-6ad0's X5, X6 and X7 are deliberately NOT
landed here — they are outside this repair's brief and have no successor ticket; see §9.***

***Repaired again 2026-07-31 by mg-dffa**, landing the four MINOR findings of
`docs/OneThird-Audit-mg-41aa-Repair.md` (mg-5800). **All four were WARRANT, not error: no
number moves and no measurement is withdrawn or added to.** Two ledger cells were widened to
what had already been measured (F1, rows B1 and B5); two sentences were narrowed to what
their evidence carries (F2, §2's heading note and §3 row 10); one premise was **re-affirmed
by reading Brown `§4.3`** rather than hedged (F4, §0 consequence 3); and one control that
could not fire was closed in `code/branching_repair_41aa/check_doc.py` (F3). Evidence:
`code/branching_warrant_dffa/`, which imports nothing from the four earlier instruments. The
sentence-by-sentence account — as written, evidence, as narrowed — is
`docs/OneThird-Warrant-Repair-mg-dffa.md`.***

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
   piece is the posets whose ideal lattice is an interval of Young's lattice — the **skew**
   cell posets `λ/μ`, of which the straight `D_λ` are the sub-family realising the intervals
   `[∅, λ]`. Both are a **vanishing** fraction (T2):

   | `n` | straight `D_λ`, i.e. `J(P) = [∅, λ]` | skew `λ/μ`, i.e. `J(P) = [μ, λ]` | all posets |
   |---|---|---|---|
   | 6 | 6 (0.0189) | **62** (0.1950) | 318 |
   | 7 | 8 (0.0039) | **149** (0.0729) | 2 045 |
   | 8 | 12 (0.0007) | **360** (0.0212) | 16 999 |

   So on the index sets, this construction **generalises** the Young case.

   > **CORRECTED (mg-41aa, landing mg-6ad0's X1).** This item previously read: *"the
   > branching-graph programme's distributive piece is the cell posets. That is a **vanishing**
   > fraction: **6 of 318** at `n = 6`, **8 of 2 045** at `n = 7`, **12 of 16 999** at
   > `n = 8`."* The three numbers are correct and are reproduced unchanged — but they count
   > the **straight** cell posets, and the class this sentence names is the **skew** ones,
   > which is 10 to 30 times larger. The **direction** of the item survives on either column
   > and is why this is a correction and not a retraction. **At `n ≤ 3` every poset is a skew
   > cell poset** (1/1, 2/2, 5/5), so the "vanishing" is a statement about `n ≥ 4` only.

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
   And I did not locate the identification on the branching-graph side either (§3,
   rows 4–7). **What this rests on is the keyword census and nothing else** — see the
   correction immediately below, which removes the sentence that used to be offered
   alongside it.

   > **STRUCK (mg-41aa, landing mg-6ad0's X2).** This item previously continued: *"His
   > worked `§4.3` example is the `p × q` grid of lattice paths (the "kids walk" is `§4.4`);
   > that grid is `J(C_p ⊔ C_q)`, which for `p, q ≥ 1` is **not** an interval of Young's
   > lattice — `D_λ` has a minimum and `C_p ⊔ C_q` does not."* **The reason is true and the
   > conclusion is false.** "`D_λ` has a minimum" rules out intervals of the form `[∅, λ]`
   > and says nothing about a general `[μ, λ]`, whose poset is a skew shape and need not
   > have a minimum. Constructed and verified pair by pair for every `p, q ≤ 5`:
   > `λ/μ = (q+p, q)/(q) ≅ C_p ⊔ C_q`, so **Brown's own `§4.3` example lattice IS the
   > interval `[(q), (q+p, q)]` of Young's lattice**, with `|[μ, λ]| = (p+1)(q+1)`, **0 bad
   > of 25** (`code/branching_repair_41aa/out_r2_grid.txt`). This is one of the three
   > elementary derivations §5 item 5 flags as mine rather than a citation, and it is the
   > one that was wrong. Consequence 3's actual claim is untouched, and the correction runs
   > **toward** the headline: the located source's worked example is an instance of the very
   > contact this document reports.

   **THE PREMISE THAT CORRECTION STANDS ON, RE-AFFIRMED OUTSIDE THE STRIKE — AND READ
   (mg-dffa, landing mg-5800's F4).** *"Brown's own `§4.3` example lattice is a Young
   interval"* has two premises: **(a)** Brown's worked `§4.3` example is the `p × q` grid,
   and **(b)** that grid is the interval `[(q), (q+p, q)]`. **(b)** is measured — 25 pairs by
   mg-41aa, 36 by mg-5800 from three definitions, 0 bad. **(a)** was mg-af28's reading of
   Brown, and after the strike above it appeared in this document **only inside struck
   text**, which is not a place a live claim may rest. It was therefore not hedged but
   **read**: `§4.3` of `arXiv:math/0006145` is titled *"Distributive lattices"*; it
   introduces exactly one example — *"As an example of a distributive lattice, consider the
   product `{0,1,…,p} × {0,1,…,q}` of a chain of length `p` by a chain of length `q`"* —
   whose *"maximal chains are the lattice paths from `(0,0)` to `(p,q)`"*; and *"The kids
   walk"* is `§4.4`. All located **by position, strictly between the two section headings**
   (`code/branching_warrant_dffa/out_w3_brown.txt`). Brown prints no size for the lattice; he
   counts the chains `0̂ < x < 1̂` at `(p+1)(q+1) − 2`, which agrees with the `(p+1)(q+1)`
   above. **What is now read is `§4.3` and the opening of `§4.4`, and nothing else: the rest
   of Brown (2000) remains unread by this arc and B8 remains a keyword census.**

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
| **Bergeron–Li axiom (2)**: *"The (external) multiplication `ρ_{m,n} : A_m ⊗ A_n → A_{m+n}` is an injective homomorphism of algebras, for all `m` and `n` (sending `1_m ⊗ 1_n` to `1_{m+n}`)"* — quoted from `arXiv:math/0612170` **§3.1, titled *"Tower of Algebras (Preserving unities)"*** | the natural candidate is block concatenation `F(P) × F(Q) → F(P ⊔ Q)`. **Measured over all 64 pairs with `|P|,|Q| ≤ 3`:** it always lands in `F(P ⊔ Q)` (0 bad), is always injective (64/64), is always a semigroup homomorphism (0 bad products) — and is **unital in 0 of 64 cases**, because it sends `(1_P, 1_Q)` to the two-block move | **§3.1's axiom fails** for this map, on unitality and on nothing else. **The same paper's §3.6, *"Tower of Algebras (not Preserving unities)"*, takes as input *"an algebra injection not necessarily preserving unities"* — exactly what is measured here — and was not evaluated** (mg-41aa, landing mg-6ad0's X3; §2 item 5) |
| a tower is **`ℕ`-graded**: `A = ⊕_{n≥0} A_n` | our index is a *poset*, not an integer. An `ℕ`-indexed subfamily closed under the `⊔` that the external product needs satisfies `P_m ⊔ P_n = P_{m+n}`, hence `P_n = P_1^{⊔n}` (elementary, and **ours** — flagged as a derivation, not a citation) | at `P_1` = a point this is the **antichain** sequence, i.e. the classical braid case; no poset-specific tower located |
| **Okounkov–Vershik** runs on an inductive family of **semisimple** algebras, and builds the Gelfand–Tsetlin algebra as a maximal commutative subalgebra, which is maximal *iff the branching graph has no multiple edges* | `kF(P)` is very far from semisimple: measured `dim kF(P)/rad = |AC(P)|` on **all 87 classes to `n ≤ 5`** and **308 of 318 at `n = 6`** (10 over the size cap, each listed), **0 bad**. At the `n = 5` antichain that is `541` against `52` — the radical is **90.4%** of the algebra, and **95.7%** at `n = 6` | **hypothesis fails.** OV supplies the *indexing* of our state space at `P = D_λ` and nothing else |
| a **branching graph / Bratteli diagram** records restriction multiplicities of irreducibles | Brown: this class of semigroups has irreducible representations that *"can be worked out explicitly (they are all 1-dimensional)"*, indexed by the support lattice — corroborated by the measurement above | **no multiplicity data exists to record.** Any Bratteli diagram here has the support lattice as vertex set and multiplicities 0/1 by construction |
| **Stanley's differential condition** `DU − UD = rI`, `r ≥ 1` | fails for **every** finite `J(P)`: `U(1̂) = 0` while `UD(1̂) ∋ 1̂`. Measured over all **405 classes to `n ≤ 6`**: **0** satisfy it; with the top rank exempted, **exactly 1** does, and it is the one-element poset. **Positive controls in the same code path**: Young's lattice to rank 8 and the Young–Fibonacci lattice to rank 8 both return `r = 1` | **no contact**, and the obstruction is finiteness, so it is not a near miss |
| **Brown §4.3** needs a finite **distributive** lattice | of the two *known* 1-differential lattices, only Young's is distributive. Measured: **all 30 intervals `[∅, λ]`, `|λ| ≤ 6`, of Young's lattice are distributive (0 bad)**; **5 of the 33 intervals `[∅̂, w]`, `rank(w) ≤ 6`, of the Young–Fibonacci lattice are not**, smallest witness `w = 221` | **at the level of WHOLE lattices**: Young's is the only *distributive* 1-differential lattice, and every interval `[∅, λ]` of it is distributive. **Not** *"reaches the Young graph and no other differential poset"* — Brown §4.3 needs a **finite** lattice and no differential poset is finite, so at that level the statement consumes nothing at all. At the level where the contact actually lives — finite intervals — **28 of the 33** Young–Fibonacci intervals to rank 6 **are** distributive (mg-41aa, landing mg-6ad0's X4; §2 item 2) |

---

## 2. WHY THE CONTACT DOES NOT EXTEND — ENUMERATED

This ticket exists because a *"no"* was given without an enumeration. So each reason is
named, with the measurement or the citation that carries it.

*(**mg-41aa**: items 2 and 5 are re-scoped below, and the re-scoping makes this heading too
strong in one respect. At the level of finite **intervals** a contact of the same **kind**
extends: **28 of the 33** finite Young–Fibonacci intervals are distributive, so each is
`J(P)` for some `P`, item 2. What does not extend is the **representation theory**, which is
items 3, 4, 6 and 7, and those are untouched.)*

*(**mg-dffa**, landing mg-5800's F2, narrowing the sentence above and not the measurement
under it. **It is a contact of the same kind and it is not the same contact.** The Young
headline is a **classification** — the intervals of Young's lattice are `J(P)` for `P`
**exactly** the skew cell posets, a named closed class, which is the whole content of §0
consequence 1. The Young–Fibonacci sentence is **Birkhoff plus a distributivity count**:
every finite distributive lattice is `J` of its join-irreducibles, so "28 of the 33 are
`J(P)`" says precisely "28 of the 33 are distributive", and **names no class of `P`**. The
families also differ. Measured on a fourth instrument: the 28 distributive Young–Fibonacci
intervals yield **17 distinct `P`** up to isomorphism, of which **5 are not skew cell
posets** — 2 of the 4 at `|P| = 5`, 3 of the 5 at `|P| = 6`
(`code/branching_warrant_dffa/out_w2_family.txt`). On the Young side the same measurement
returns **30 of 30** intervals distributive and **0** of the resulting `P` outside the skew
class.)*

1. **Finiteness.** Differential posets and dual graded graphs are locally finite with a
   `0̂` and infinitely many ranks; `J(P)` for finite `P` is finite with a `1̂`. The
   identity fails at `1̂` for elementary reasons and this is not repairable by truncation
   (T3: 0 of 405; with the top rank exempted, 1 of 405, the one-element poset). *A
   truncation of an infinite lattice is not even a lattice — two elements of top rank lose
   their join — which is why T8 tests intervals and not truncations.*

2. **Distributivity, and it is a statement about whole lattices only.** Stanley (1988):
   *"Young's lattice is the only 1-differential distributive lattice"*; Byrnes (2012) is
   reported to have shown that Young's and Young–Fibonacci are the only 1-differential
   lattices at all. *(Both statements taken from the Wikipedia article on differential
   posets; **I read neither original**, and my argument uses only the first.)* **What
   Stanley licenses:** among differential posets that are distributive lattices, Young's is
   the only one. T8 measures the illustrative case: Young–Fibonacci, the other known
   1-differential lattice, is not distributive as a whole (5 of its 33 intervals to rank 6
   fail, smallest witness `w = 221`).

   > **RE-SCOPED (mg-41aa, landing mg-6ad0's X4).** This item previously continued: *"Brown
   > §4.3's hypothesis is `distributive lattice`, and a differential poset that is a
   > distributive lattice is Young's — so Young's is the **only** differential poset his
   > construction can consume, whatever the full classification of differential lattices
   > turns out to be."* **At the level of whole differential posets that is true and
   > empty:** Brown §4.3's hypothesis is a **finite** distributive lattice, and no
   > differential poset is finite — item 1 above says exactly that — so Brown consumes
   > **none** of them, Young's lattice included. The level at which this document's own
   > contact lives is the finite **intervals**, and there the claim is false: of the **33**
   > intervals `[0̂, w]` of Young–Fibonacci with `rank(w) ≤ 6`, the **28** that T8 finds
   > distributive are finite distributive lattices, so Brown §4.3 consumes each of them, and
   > by Birkhoff each is `J(P)` for a poset `P` built from its join-irreducibles — **28
   > reconstructions, 0 bad** (`code/branching_repair_41aa/out_r3_rescope.txt`, reproducing
   > mg-6ad0's A6 on a third instrument, with T8's 33/5 and its witness `w = (2,2,1)`
   > reproduced exactly). **T8's measurement is right; only its reading was too wide.**

3. **The algebra is basic, not semisimple.** T5. The programme's invariant — restriction
   multiplicities between semisimple layers — has no counterpart, because there are no
   semisimple layers and all irreducibles are one-dimensional.

4. **The action is not a group action.** T6. Every move is idempotent; the ones acting
   bijectively act as the identity map. So at `P = D_λ` the monoid is not `S_n` and the
   walk is not transport of the `S_n`-action along the Gelfand–Tsetlin basis.

5. **No tower under §3.1's definition, and an OPEN QUESTION under §3.6's.** §1, rows 1–2:
   Bergeron–Li's axiom (2) as stated in **§3.1, *"Tower of Algebras (Preserving unities)"***,
   fails for the natural map — measured, on unitality, 0 of 64 — and the `ℕ`-grading it
   presupposes forces disjoint powers `P_n = P_1^{⊔n}`.

   > **RE-SCOPED (mg-41aa, landing mg-6ad0's X3).** This item previously read: *"**No
   > tower.** §1, rows 1–2: Bergeron–Li's axiom (2) fails for the natural map, and the
   > `ℕ`-grading it presupposes forces disjoint powers, which lands back at the classical
   > antichain case."* The measurement is right and is not withdrawn. **The negative it
   > licensed is not.** The cited paper contains **two** tower definitions, and this document
   > tested one: §3.1 is titled *"Tower of Algebras (Preserving unities)"* and **§3.6 is
   > titled *"Tower of Algebras (not Preserving unities)"***, taking as input *"an algebra
   > injection not necessarily preserving unities"* — which is precisely what block
   > concatenation was measured to be (injective, multiplicative, non-unital). All four
   > strings located verbatim in the PDF, in both the printed spelling and the spelling a
   > ligature-dropping extractor produces (`code/branching_repair_41aa/out_r3_rescope.txt`;
   > mg-6ad0's `out_a6_quotes.txt` located three of them independently).
   >
   > **THE OPEN QUESTION, NAMED RATHER THAN ANSWERED.** *Does `A_n = kF(P_1^{⊔n})` satisfy
   > Bergeron–Li's §3.6 conditions?* Conditions (3), (4) and (5) — projectivity of `A_{m+n}`
   > over `A_m ⊗ A_n`, the idempotent condition, and the Mackey-type identity — are
   > **untested by mg-af28, by mg-6ad0 and by mg-41aa**. Testing them is new mathematics,
   > which every ticket in this lineage forbids, so **no verdict is manufactured here.** Row
   > 3 of §3 is a **hedge, not a "no"** — the same repair mg-1953 correctly applied to row Q,
   > and the reason this repair exists: a negative was licensed over a definition space of
   > one, in a paper containing two, inside the very enumeration filed to cure a negative
   > licensed over a candidate space of two.
   >
   > *The clause "which lands back at the classical antichain case" is separately wrong —
   > `P_1` is arbitrary (mg-6ad0's X7) — and is **not** repaired here; see §9.*

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
| **3** | **Towers of algebras** (Bergeron–Li, `arXiv:math/0612170`; Bergeron–Lam–Li) | **yes — one of the paper's two definitions** | **ADJACENT — §3.1's axiom (2) fails on unitality; §3.6 weakens exactly that clause and was not evaluated** | axiom (2) of **§3.1** *("Preserving unities")* quoted verbatim and tested: concatenation is injective and multiplicative but **not unital**, 0 of 64 (T7). The `ℕ`-grading forces disjoint powers. **§3.6** *("not Preserving unities")* takes an injection *"not necessarily preserving unities"* as its input; its conditions (3),(4),(5) are untested by anyone and testing them is new mathematics. **This is a hedge, not a "no"** *(re-scoped by mg-41aa under mg-6ad0's X3; §1, §2.5)* |
| **4** | **Stanley's differential posets** | **yes** | **NO CONTACT, with the theorem that says why** | finiteness (T3, 0 of 405) and Stanley's uniqueness theorem. This **upgrades** row K from *"empty"* to *"no, and here is why, and here is the one place where contact does exist"* |
| **5** | **Fomin's dual graded graphs** | **yes** | **NO CONTACT** | same finiteness obstruction; and there is no second graph on our vertex set — the programme's content is a growth/RSK bijection, which needs the pair. Context on how rigid the structure is: Gaetz (`arXiv:1803.11168`) proves that for `r = 1` or `r` prime, *"wreath products of a fixed group with the symmetric groups are the only `r`-dual tower of groups"* |
| **6** | **Okounkov–Vershik / Gelfand–Tsetlin** | **yes** | **ADJACENT — and it is the source of the one real contact** | OV needs semisimple inductive families (T5 refutes the hypothesis for us). What it supplies is the identification of `SYT(λ)` as the GT basis of `S^λ`, which is our state space at `P = D_λ`. §0 |
| **7** | **Diagram algebras via Schur–Weyl** (partition, Brauer, Temperley–Lieb, rook) | **yes** | **NOT LOCATED** | these are centraliser algebras with diagram bases and multiplicity-carrying Bratteli diagrams; I located no order-cone, order-congruence or `P`-compatible-partition object among them. A search report, not a claim about the literature |
| **8** | **Bratteli diagrams / AF algebras** in general | **yes** | **VACUOUS INSTANCE** | true and contentless; §2.7 |
| **9** | **Fulman, *Commutation relations and Markov chains*** (`arXiv:0712.1375`), down-up chains on the Young, Schur and Kingman graphs | **yes** | **ADJACENT — different state space** | his chains move on the **vertices** of a branching graph, driven by the `U`/`D` operators; ours moves on the **maximal chains**. The Plancherel growth process is likewise a measure on paths, not a Markov chain on the set of paths |
| **10** | **Okada algebras and the Okada monoid** (`arXiv:2404.16733`) | **yes** | **ADJACENT — the closest structural analogue found** | a *monoid* whose algebra tower has a differential poset (Young–Fibonacci) as its Bratteli diagram: the shape of the thing Daniel's question asks for. It is a different monoid (aperiodic, a labelled Temperley–Lieb arc-diagram model). **Located from abstracts; not read.** *Re-scoped by mg-41aa under mg-6ad0's X4: this row previously added "and the lattice it realises is the one Brown §4.3 provably cannot consume (T8)". That reason does not hold — **28 of the 33** finite Young–Fibonacci intervals to rank 6 are distributive, so Brown §4.3 consumes them and each is a `J(P)`. Row 10 therefore has an index-set contact of the **same kind** as the one this document headlines for Young's, on 28 of 33 intervals; what keeps it ADJACENT is that it is a different monoid, which is the reason above and not the withdrawn one.* **Narrowed by mg-dffa under mg-5800's F2: it is not the SAME contact. The Young headline classifies its index sets — `P` exactly the skew cell posets — whereas here no class of `P` is named, and the 28 intervals yield 17 distinct `P` of which 5 are not skew cell posets (§2 item 2; `code/branching_warrant_dffa/out_w2_family.txt`).** |
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

   > **THIS ATTACK LANDED, AND IT WAS THE WORST FINDING IN THE DOCUMENT (mg-6ad0, landed by
   > mg-41aa).** Of the three: (b) is correct and correctly used (brute force over all 87
   > classes to `n = 5`, 0 counterexamples). (a) is correct **as a derivation** but is
   > mis-used downstream in §2 item 5 — mg-6ad0's X7, **not repaired here**, §9. **(c) is
   > FALSE**, and its second half is struck at §0 consequence 3: the grid *is* the interval
   > `[(q), (q+p, q)]`. Only the first half of (c) survives — the grid *is* `J(C_p ⊔ C_q)`,
   > re-verified for all 25 pairs `p, q ≤ 5`. **This is the second consecutive document in
   > this arc in which beyond-brief material carries the worst finding**, and it was
   > pre-filed here by name, which is the only reason it was cheap to find.

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
| **B1** | `J(D_λ)` is the interval `[∅, λ]` of Young's lattice, by the map "ideal ↦ shape", and the maximal chains of `J(D_λ)` are `SYT(λ)` with `e(D_λ) = f^λ` | **MEASURED — and it is a LATTICE isomorphism** *(widened by mg-dffa, landing mg-5800's F1)* | 44 partitions, `n ≤ 7`. **Meet and join preserved on every pair, not the order alone**: measured three times on disjoint instruments — mg-6ad0 (`code/branching_audit_6ad0/out_a1_contact.txt`), mg-5800 (`code/branching_audit_5800/out_a5_b1b5.txt`) and mg-dffa (`code/branching_warrant_dffa/out_w1_ledger.txt`, 5 464 ordered pairs, the two sides built from order ideals and from containment of **partitions** respectively) — **0 bad each time**. T1 in `code/branching_af28/` itself tests the **order** isomorphism only, on every pair in both directions, 0 bad, though it prints the label `lattice-iso bad`. `f^λ` against an independently coded hook length formula, 0 bad |
| **B2** | the posets `P` for which `J(P)` is an interval `[μ, λ]` of Young's lattice are exactly the **SKEW** cell posets `λ/μ`, a vanishing fraction: **62/318** (`n=6`), **149/2 045** (`n=7`), **360/16 999** (`n=8`); those with `J(P) = [∅, λ]` are exactly the straight cell posets `D_λ`, 6/318, 8/2 045, 12/16 999 | **MEASURED both columns; the "exactly" now TESTED** | straight and skew classes by canonical form (T2, `n ≤ 6` here; `n = 7, 8` skew from `code/branching_repair_41aa`, agreeing with mg-6ad0). The "exactly" is tested **in both directions** in `r1_exactly.py`: for all **405** poset classes to `n ≤ 6` an isomorphism `J(P) → [μ, λ]` is **constructed and checked on every pair**, and no poset outside the skew class matches any interval of the right size (exhaustive to `n ≤ 5`). `n ≥ 7` totals are **A000112, cited not computed** |
| **B2′** | *(the version this replaces, mg-6ad0's X1)* — B2 formerly read *"the posets `P` for which `J(P)` is an interval of Young's lattice are **exactly** the cell posets, … 6/318, 8/2 045, 12/16 999"* | **BROKEN — the "exactly" was FALSE and was never tested** | the 2-element antichain is not a `D_λ` and `J(it) = [(1), (2,1)]`; T2 measured `{canon(D_λ) : λ ⊢ n}` and nothing else. The three numbers were right about the straight class and understated the named class by 10× to 30× |
| **B3** | no finite `J(P)` is a differential poset, and none is one even with the top rank exempted (bar the one-element poset) | **MEASURED, with positive controls** | 405 classes to `n ≤ 6`. Controls: Young's lattice and Young–Fibonacci both return `r = 1` in the same code path |
| **B4** | **as whole lattices**: every interval `[∅, λ]` of Young's lattice is distributive and the Young–Fibonacci lattice is not, and Young's is the only *distributive* 1-differential lattice | **MEASURED + CITED** | 30 Young intervals, 0 non-distributive; 33 Young–Fibonacci intervals, 5 non-distributive, witness `w = 221` — all reproduced by mg-6ad0 and by mg-41aa. Stanley's and Byrnes's classification statements are **cited from a secondary source and not read** |
| **B4′** | *(the reading this replaces, mg-6ad0's X4)* — B4 formerly concluded *"so Brown §4.3 reaches the Young graph and no other differential poset"* | **RE-SCOPED — true and empty at the level stated, false at the level that matters** | Brown §4.3 needs a **finite** distributive lattice and no differential poset is finite, so at whole-poset level it consumes none, Young's included. At interval level, **28 of 33** Young–Fibonacci intervals are distributive and each is `J(P)` for an explicitly constructed `P`, **0 bad** |
| **B5** | `dim kF(P)/rad = |AC(P)|`, consistent with Brown's *"they are all 1-dimensional"* | **MEASURED — and the step to Brown's theorem has since been DERIVED, twice** *(widened by mg-dffa, landing mg-5800's F1)* | trace-form rank in exact rational arithmetic; all 87 classes to `n ≤ 5` and 308 of 318 at `n = 6`, 0 bad. **The step from this to "all irreducibles are 1-dimensional" is Brown's theorem, cited and not re-derived in `code/branching_af28/`** — but it has since been derived without it: `Φ : kF(P) → k^{AC(P)}` built from the product alone, surjective, `ker Φ` a nilpotent ideal, 0 bad — by mg-6ad0 on 67 of the 87 classes to `n ≤ 5` (20 over its cap of 90 on the size of `F(P)`, each listed) *"by a route that uses no theorem of Dickson and no trace form"*, and by mg-5800 on all 87 *"with NO trace form and NO cited theorem"* (`code/branching_audit_6ad0/out_a4_algebra.txt`, `code/branching_audit_5800/out_a5_b1b5.txt`). **mg-dffa LOCATED both results in those committed outputs; it did not re-run them and does not re-derive the step itself** |
| **B6** | no move acts on `L(P)` bijectively without acting as the identity map | **MEASURED** | 6 197 moves over 87 classes to `n ≤ 5`, 0 |
| **B7** | block concatenation `F(P) × F(Q) → F(P ⊔ Q)` is an injective semigroup homomorphism and is **not** unital, so it fails Bergeron–Li axiom (2) **of §3.1, *"Tower of Algebras (Preserving unities)"*** | **MEASURED + QUOTED** | 64 pairs, `|P|,|Q| ≤ 3`; axiom quoted verbatim from `arXiv:math/0612170` §3.1, quotation re-verified by mg-6ad0 and by mg-41aa |
| **B7′** | *(the scope this adds, mg-6ad0's X3)* — the same paper's **§3.6, *"Tower of Algebras (not Preserving unities)"***, takes as input *"an algebra injection not necessarily preserving unities"*, which is what B7 measures concatenation to be | **QUOTED; the consequence is an OPEN QUESTION, not a verdict** | both section titles and the input clause located verbatim, in both spellings, on a third extractor. Bergeron–Li conditions (3),(4),(5) under the §3.6 weakening are **untested by anyone** and testing them is new mathematics. **B7 does not license a "no tower"; it licenses "§3.1's axiom fails"** |
| **B8** | Brown (2000) contains none of the branching-graph vocabulary | **MEASURED** | keyword census of the arXiv PDF with five present-word controls, one of which (`left regular band`) failed on the first run because Brown hyphenates it, and was fixed in the scanner, not in the finding |
| **B9** | the candidate space is the twelve programmes of §3; rows 1–2 were **not re-run**; rows 3–6, 8–12 were searched; row 7 is the least-searched | **REPORT ON A SEARCH** | not a claim about the literature. Queries were targeted, not exhaustive |
| **B10** | the walk on `SYT(λ)` given by `P = D_λ` was **not located** in either literature | **REPORT ON A SEARCH** | explicitly **not** a novelty claim; §5 item 3 |
| **NOT CLAIMED** | that anything here is new; that anything here is publishable; that the searches were exhaustive; anything about `λ₂`, `Δ_AT` or the pricing; anything about the `S_n`-structure carried on `SYT(λ)` interacting with the walk, which is untested; **(mg-41aa)** that a tower of algebras exists over this family under Bergeron–Li §3.6, which is an open question and not a claim in either direction; that mg-6ad0's X5, X6 and X7 are answered here — they are not | | |

---

## 7. REPRODUCE

```
cd code/branching_af28      && ./run_all.sh   # ~6 min, pure Python 3
cd code/branching_repair_41aa && ./run_all.sh # ~4 min, pure Python 3  (mg-41aa)
```

Committed outputs: `out_selftest.txt` (31 assertions), `out_young.txt`, `out_branching.txt`,
`out_lrb_reps.txt`, `out_scan_brown.txt`. `scan_brown.py` is the only step needing network.

mg-41aa's repair instrument is `code/branching_repair_41aa/` (36-assertion self-test,
sharing no code with `branching_af28/` or `branching_audit_6ad0/`): `out_r1_exactly.txt`,
`out_r1b_skew8.txt`, `out_r2_grid.txt`, `out_r3_rescope.txt`, `out_check_doc.txt`. The
audit it lands is `docs/OneThird-Audit-mg-af28-Branching-Graphs.md` (mg-6ad0,
`code/branching_audit_6ad0/`), and that battery was re-run **unmodified** against the
repair — see `docs/OneThird-Branching-Graphs-Repair.md` §5.

mg-dffa's warrant instrument is `code/branching_warrant_dffa/` (42-assertion self-test,
importing nothing from the four earlier instrument directories): `out_w1_ledger.txt`,
`out_w2_family.txt`, `out_w3_brown.txt`, `out_w4_control.txt`, `out_w5_doc.txt`. `w3_brown.py`
is the only step needing network. The account of what it changed and why is
`docs/OneThird-Warrant-Repair-mg-dffa.md`.

```
cd code/branching_warrant_dffa && ./run_all.sh # ~5 s, pure Python 3  (mg-dffa)
```

---

## 8. NOTE FOR pm-onethird — SCOPE DISCIPLINE

Three things this document deliberately does **not** do.

* It does **not** edit row Q of `docs/OneThird-Landscape-Where-This-Lives.md`. mg-1953 owns
  that row and correctly withdrew it to a hedge. **Operational consequence:** row Q and
  ledger row E10 now say of towers of algebras, Okounkov–Vershik and diagram algebras that
  they are *"claimed neither way — they were not searched"*. They have now been searched.
  Whether to fold this document's §3 back into row Q is pm-onethird's call, not mine.
* It does **not** develop mathematics. **Three** elementary one-line derivations were
  needed to test hypotheses and are flagged in place (§2.6, §1 row 2, §0 consequence 3) and
  pre-filed for audit (§5 item 5). Everything else compares our objects against published
  descriptions of other objects. *This is the instruction mg-ebd8 violated twice, in exactly
  this position, which is why it is called out here rather than assumed.* **(mg-41aa: this
  bullet said "Two" while §5 item 5 listed three — the under-count is corrected, and the
  third derivation is the one that turned out to be false. See §5 item 5 and §9.)**
* It does **not** touch `STATE.md`, the semigroup note, `λ₂`, `Δ_AT` or the roadmap
  pricing.

---

## 9. WHAT mg-41aa's REPAIR DELIBERATELY LEFT OPEN

mg-6ad0 raised seven items. This repair was scoped by the filing mayor to **four** — X1, X2
(both BROKEN, both refuted by construction, both on the negative side) and X3, X4 (both
re-scoped above). The remaining three are recorded here, unrepaired and with **no successor
ticket**, so that pm-onethird makes the call rather than the record losing them:

* **X5 — ledger rows B6 and B7 are booked MEASURED with sample sizes that cannot do any
  work.** Both answers are forced for every poset of every size: `F(P)` is a band, so an
  idempotent bijection of a finite set is the identity (B6); and concatenation sends
  `(1_P, 1_Q)` to a two-block move, which is `1_{P⊔Q}` only if a block is empty (B7). Both
  arguments **are** stated in prose in `out_young.txt` and `out_branching.txt`; the defect
  is that §6 books them as evidence. This is mg-3b51's R1d finding one document later.
* **X6 — B8's five present-word controls could not have caught B8's one documented failure
  mode.** The extractor drops `fi`/`ff` ligatures (`finite` → `nite`, 57 times); 2 of the 12
  absent keywords bear a ligature and 0 of the 5 controls does, so a genuine *"differential"*
  in Brown would have scored 0 with every control green. **B8's conclusion survives** a
  ligature-aware re-run — all twelve keywords absent in both spellings — and mg-41aa's own
  quotation search (§2 item 5) is ligature-aware for exactly this reason. It is the
  **warrant** in B8's scope column that is wrong, not the finding.
* **X7 — §2 item 5's clause "which lands back at the classical antichain case" drops a
  condition its own §1 row 2 states.** The derivation forces `P_n = P_1^{⊔n}` for an
  **arbitrary** finite `P_1`; only `P_1` = a point gives the antichain sequence. The clause
  is left standing in the struck text quoted at §2 item 5 and is flagged there.

**And the pattern the audit named, which is the reason this repair exists at all.** mg-af28
was filed because mg-d673 found a *"no"* licensed over a candidate space of **two**. Inside
the enumeration written to cure that, X3 is a *"no"* licensed over a definition space of
**one, in a paper containing two** — the ticket's own defect recurring in its own apparatus.
And X2, the worst finding, sits in beyond-brief material that this document flagged as its
own and pre-filed by name: the second consecutive generation in this arc where the unbriefed
one-liners are the least controlled part of the deliverable.
