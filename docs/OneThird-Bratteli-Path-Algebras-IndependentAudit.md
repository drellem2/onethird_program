# Independent audit of mg-db09 / `03d7f91` — the Bratteli / path-algebra locating ticket

**Work item:** mg-2060, pre-filed in the same action as its parent. **Date:**
2026-07-30. **Target:** `docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md`
and `code/branching_locate_db09/`, commit `03d7f91`. **Instrument:**
`code/branching_audit_2060/`, `run_all.sh`, ~20 min, 56 940-assertion self-test,
one reproduction script and seven test scripts.

**This audit shares no code with the target.** `kern2060.py` rebuilds
Temperley–Lieb diagrams, link states, cell modules, the bilinear form, symmetric
group algebras, `F(P)`, `AC(P)` and the trace-form radical from definitions. The
four papers the target quotes were **fetched again by this audit** and the whole
`pdftotext` extraction of each is committed, with the SHA-256 of the PDF it came
from — not a line-numbered window.

---

## 0. HEADLINE

**The reproduction is total and the verdict survives, but the evidence offered
for the verdict does not: mg-db09's separating example does not hold
multiplicity-freeness fixed, and it says twice that it does.**

* **5 of 5 committed outputs regenerate BYTE-IDENTICALLY.** Every number in
  T1, T2, T3 and T4 that this audit recomputed on a disjoint instrument came
  out the same.
* **1 BROKEN.** mg-db09 §0: *"The branching graph is **measured** (not cited)
  to be the same multiplicity-free graph at each"* and *"Multiplicity-freeness
  is held **FIXED** down that column and the conclusion changes."* Measured here
  under **the definition mg-db09 itself quotes from Vershik–Okounkov** — vertices
  are the irreducible modules, edges are restriction multiplicities — the
  Temperley–Lieb tower at `β = 1` and `β = 0` has a **different vertex set** and
  **restriction multiplicities equal to 2**. Multiplicity-freeness varies down
  that column in step with semisimplicity, which is exactly what the argument
  needed it not to do.
* **The verdict D4 — semisimplicity is load-bearing, multiplicity-freeness is
  not — is nevertheless CORRECT**, because it follows from the theorem mg-db09
  quotes: a finite direct sum of endomorphism algebras *is* semisimple, so
  `A ≅ ⨁ End(V_λ)` and semisimplicity are equivalent for every
  finite-dimensional algebra, with no branching hypothesis anywhere. The two
  builds establish that both off-diagonal cells are **inhabited**; they did not
  and could not settle which hypothesis carries the conclusion.
* **6 MINOR**, four of them not named by any pre-filed list.
* **Two things get STRONGER.** D9 — the one citation mg-db09 flags as its own
  weakest, taken from Wikipedia with *"Graham–Lehrer not read"* — is confirmed
  in a refereed source with its proof indicated. And the `|F(P)| ≤ 90` cap is
  removed: `dim kF(P)/rad = |AC(P)|` now holds on **87 of 87 classes to `n ≤ 5`,
  0 bad, nothing exempt**, including the `n = 5` antichain, so the **90.4%
  figure is derived from the radical for the first time in this lineage.**

---

## 1. WHAT THE BRIEF TOLD ME TO DO, AND WHAT I DID INSTEAD OF ONLY THAT

My brief says its own list is a floor and instructs me to audit at least one
thing no list names, and to say what I chose and why.

**The rule I used, stated before the results so it cannot be back-fitted.** I
took every sentence in the delivered document that is (a) load-bearing for a
headline, (b) stated as an *equivalence* or as a *measurement*, (c) not a
quotation, and (d) absent from both mg-db09's §4 attack list and my brief. There
were four. All four are below; **two of them are wrong.**

| chosen because it fits the rule | where | outcome |
|---|---|---|
| *"a basis indexed by pairs of paths with a common endpoint exists **iff** `dim A = Σ (#paths)²`"* | T1a header, and §0's 2×2 table | **FALSE** in the "if" direction (X2) |
| *"multiplicities in `{0,1}`, **equivalently** (VO Prop. 1.4) the centralizer `Z(M,N)` is commutative"* — stated with no semisimplicity qualifier, in the table whose whole subject is dropping hypotheses | §1 table row 3 | **the equivalence fails** off semisimplicity, on mg-db09's own example (X3) |
| the **vertex set** of the branching graph, as opposed to its edge multiplicities — §4 item 3 questions only the edges | §0, T1b | **different at `β = 0`** (part of X1) |
| *"the `kF(P)` family"* as the subject of the proposed successor | §7 | **not a sequence**; no sub-family is chosen (X7) |

I also did the thing my brief asked and mg-db09's §4 item 4 asked: rebuilt the
Cartan matrix from Margolis–Saliola–Steinberg's **closed formula (4.9) with its
Möbius function**, the route mg-db09 deliberately did not take. It agrees on all
nine rows.

---

## 2. REPRODUCTION

`b0_repro.sh` copies `code/branching_locate_db09/` to a scratch directory, runs
its `run_all.sh`, and diffs.

| file | result |
|---|---|
| `out_selftest.txt` (698 963 assertions) | **IDENTICAL** |
| `out_t1_tl.txt` | **IDENTICAL** |
| `out_t2_gz.txt` | **IDENTICAL** |
| `out_t3_ours.txt` | **IDENTICAL** |
| `out_t4_quotes.txt` | **IDENTICAL** |

Beyond byte-identity, every table this audit recomputed independently agrees:

* **T1c, both routes.** The dimension of the semisimple quotient of `TL_n(β)`,
  computed here as `Σ_p (dim L(n,p))²` from Gram-form ranks and again from the
  trace form, matches mg-db09 on all 20 `(n, β)` pairs — including the three
  numbers §0 quotes, `132`, `99`, `42`.
* **All six published Temperley–Lieb controls** (Ridout–Saint-Aubin) reproduce
  in this audit's self-test.
* **T2a/T2b/T2c/T2d in full** (B7): `dim GZ(n)` = involutions for `n ≤ 5`; the
  four `ℂS_4` chains at `10, 8, 7, 5`; `S_1 ⊂ S_2 ⊂ S_3 ⊂ S_5` at `18`; the six
  centralizer dimensions `4, 7, 12, 14, 28, 66` with commutativity exactly on
  the adjacent pairs; `dim ℂS_4 = 24` with zero radical.
* **T3a, T3b, T3c, T3d** (B4), with the cap removed and the Cartan matrix by a
  different formula.

---

## 3. BROKEN — X1: THE SEPARATING EXAMPLE DOES NOT HOLD ITS HYPOTHESIS FIXED

### What mg-db09 claims

> *"**1. Multiplicity-free and NOT semisimple — the conclusion fails.** The
> Temperley–Lieb tower `TL_1 ⊂ TL_2 ⊂ ⋯` at four parameters. The branching graph
> is **measured** (not cited) to be the same multiplicity-free graph at each"*
> (§0)
>
> *"Multiplicity-freeness is held **FIXED** across those four rows and the
> conclusion changes. So multiplicity-freeness is not what carries it."* (T1d)

### What the branching graph is, in the source mg-db09 quotes

Vershik–Okounkov §1, in the passage mg-db09 quotes verbatim and this audit
re-verified against its own extraction of `arXiv:math/0503040`: the branching
graph of a chain has **the irreducible modules of the `n`-th algebra as its
vertices at level `n`** and **the restriction multiplicities as its edges**.
Multiplicity-freeness is *"the multiplicities of all restrictions are equal 0 or
1"*. It is a statement about **simple** modules.

### What T1b measures

`dim Hom_{TL_{n-1}}(V_{n-1,q}, V_{n,p}↓)` **at `β = 3` only**, plus, at every
`β`, the dimension identity `dim V(n,p) = dim V(n-1,p) + dim V(n-1,p-1)`. The
second is the Catalan-triangle identity; **neither side of it mentions `β`**, so
it cannot distinguish parameters. mg-db09's §4 item 3 discloses this and calls
it *"the dimension shadow"*. §0 does not; it says *"measured"*.

### What this audit measures — the actual branching graph

`L(n,p) := V(n,p)/rad⟨,⟩` (Graham–Lehrer). Composition multiplicities of
`L(n,p)↓_{TL_{n-1}}` are recovered from characters — in characteristic 0 the
characters of the pairwise non-isomorphic simples are linearly independent — and
**uniqueness, integrality, non-negativity and the dimension identity
`Σ_q m_q · dim L(n-1,q) = dim L(n,p)` are all checked, not assumed** (B1b).

**The vertex sets are not the same:**

| `n` | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| `β = 3` | 1 | 2 | 2 | 3 | 3 | 4 |
| `β = 2` | 1 | 2 | 2 | 3 | 3 | 4 |
| `β = 1` | 1 | 2 | 2 | 3 | 3 | 4 |
| **`β = 0`** | 1 | **1** | 2 | **2** | 3 | **3** |

At `β = 0` the tower has **fewer irreducibles at every even level**. The graph
mg-db09 calls "the same" does not have the same number of vertices.

**The multiplicities are not all 0 or 1:**

| `β` | edge | multiplicity |
|---|---|---|
| 1 | `[L(4,1)↓ : L(3,0)]` | **2** |
| 1 | `[L(6,2)↓ : L(5,1)]` | **2** |
| 0 | `[L(3,1)↓ : L(2,0)]` | **2** |
| 0 | `[L(5,1)↓ : L(4,0)]` | **2** |
| 0 | `[L(5,2)↓ : L(4,1)]` | **2** |

Each survives its own dimension check: `dim L(4,1) = 3 = 2·1 + 1·1`;
`dim L(5,2) = 5 = 1·1 + 2·2`.

| `β` | branching multiplicity-free? | semisimple at `n = 6`? |
|---|---|---|
| 3 | **yes** | yes |
| 2 | **yes** | yes |
| 1 | **NO** | no |
| 0 | **NO** | no |

**Multiplicity-freeness varies down the column in exact step with
semisimplicity and with the conclusion.** The experiment mg-db09 describes —
hold one hypothesis fixed, vary the other, watch the conclusion — was not
performed; both hypotheses moved together.

### What this does and does not cost

**It does not cost the verdict.** D4 is right, and the reason is in mg-db09's own
§0: `⨁_λ End(V_λ)` **is** semisimple, so for every finite-dimensional algebra

    A ≅ ⨁_λ End(V_λ)   ⟺   A is semisimple,

with no rank function, no branching graph and no multiplicity hypothesis. And
Remark 1.3, quoted, gives the other half: multiplicity-freeness buys the
canonicity and nothing else. **The verdict was settled by the quoted theorems
before any object was built.**

**It does cost the framing, and one cell of the table.** §0 says *"Both halves
are settled here by **BUILDING** the object each would forbid, not by
argument"*, and T1d says the conclusion changes because *semisimplicity* varies
while multiplicity-freeness is held fixed. Neither is what happened. What the
builds establish is that both off-diagonal cells are **inhabited** — which is
real, and is what §0's brief actually asked for. In the 2×2 table's
multiplicity-free-and-not-semisimple cell, the entries `TL_6(1): 99 of 132` and
(implicitly) `TL_6(0)` **do not belong there**; the entry `kF(P): 52 of 541`
does, and it is the only one that does, because `kF(P)`'s irreducibles really
are all one-dimensional so its branching really is multiplicity-free (D6).

**The sentence is true under a different reading, and that is why it survived.**
In cellular-algebra language one does speak of the branching graph of the **cell**
modules, and there the statement is correct at every `β`: `V(n,p)↓` has a
filtration by `V(n-1,p)` and `V(n-1,p-1)`, each once, and the dimensions do not
involve `β`. But the hypothesis in the theorem mg-db09 is testing is
Vershik–Okounkov's, and VO's branching graph is built from **irreducibles**. The
cell modules are parameter-independent and are what a cellular structure hands
you for free; the simple modules are not. **Reading a cellular datum as a
branching graph is a resemblance**, and mg-db09's own discipline is
*"identifications are equalities, not resemblances"*.

**Credit where it is due, and it matters for what a pre-filed list is worth.**
mg-db09's §4 item 3 points at exactly this: it says T1b's measurement at other
parameters is only *"its dimension shadow"* and that *"an auditor should check
whether that shadow is enough for what §0 claims."* **It is not**, and that is
the finding. So unlike the previous audit in this lineage — where the target's
self-named attack list was accurate everywhere it pointed and the one broken row
was the one it omitted — **here the list pointed straight at the broken row and
declined to draw the conclusion.** The list was right about where to look and
wrong about what was there. The four unnamed items in §1 are a separate matter,
and two of those are wrong too.

---

## 4. MINOR

### X2 — T1a's "iff" is false, and no list names it

T1a prints, as the definition it then tests against:

> *"A basis indexed by pairs of paths with a common endpoint exists **iff**
> `dim A = sum over the top-level vertices of (number of paths)²`."*

and §0's 2×2 table concludes *"Path-pair **basis** survives, direct sum does
not"*, and T1d *"the pairs-of-paths basis exists throughout"*.

The "only if" direction is immediate. The "if" direction is false, and the
smallest counterexample is on mg-db09's own T1c table (`TL_2(0) has a
1-dimensional radical`). **`TL_2(0) = k[e]/(e²)`**: `dim A = 2` and the path-pair
count is `1² + 1² = 2`, so the stated iff is satisfied — but the algebra is
**local**, it has **one** simple module, and *the only idempotents in it are 0
and 1* (checked exhaustively in B2b: `x = a + be`, `x² = x` forces `b = 0`).
There is no family of two orthogonal idempotents, hence no matrix units, hence
no path-pair basis in the sense Vershik–Okounkov use. At `TL_6(1)` the same
count gives 132 while `A/rad` has dimension 99; matrix units would force
semisimplicity.

What is true, and is the statement the document does not make: a **cellular**
algebra has a cellular basis indexed by pairs of paths, multiplying as
`C^λ_{s,t} C^μ_{u,v} = ⟨t,u⟩ δ_{λμ} C^λ_{s,v} + (lower cell terms)`. It
degenerates to matrix units exactly when every form is non-degenerate — exactly
when the algebra is semisimple. **The lower-cell terms are what "the basis
survives" elides.** Nothing else in the document depends on this.

### X3 — VO Prop. 1.4 is stated as an unconditional equivalence, and it is not

§1's table, in the row for the multiplicity-freeness hypothesis:

> *"multiplicities in `{0,1}`, equivalently (VO Prop. 1.4) "the centralizer
> `Z(M,N)` is commutative""*

Vershik–Okounkov state Remark 1.3 and Prop. 1.4 *"for an arbitrary inductive
family of **semisimple** algebras"* — the words are in the passage mg-db09 quotes.
§1's table is the one place in the document whose entire subject is what happens
when hypotheses are dropped, and there the qualifier is dropped.

Measured on mg-db09's own example (B1c), which mg-db09 did not do — it ran this
test only on the symmetric-group side:

| `n` | `β` | `dim Z(TL_n, TL_{n-1})` | commutative? | semisimple? | branching mult-free? |
|---|---|---|---|---|---|
| 5 | 3 | 5 | yes | yes | yes |
| 5 | 2 | 5 | yes | yes | yes |
| 5 | **1** | 5 | **yes** | no | **NO** |
| 5 | **0** | 5 | **yes** | yes | **NO** |

The centralizer criterion says "multiplicity-free" at `β = 1`, where the
multiplicities are 2. **The criterion the document adopts as the equality-form
of the hypothesis returns the wrong answer on the document's own object**, and
it does so in a way that would have caught X1 had it been run there.

### X4 — the commit message places a re-derivation next to figures that were exempted

The commit message for `03d7f91` reads:

> *"fails semisimplicity maximally — 541 vs 52 at n = 5 (90.4%), 4683 vs 203 at
> n = 6 (95.7%), re-derived on a third instrument, 67 of 87 classes to n ≤ 5, 0
> bad"*

`541` is **on T3b's own exemption list** (`|F(P)| ≤ 90` cap; the printed sizes
include `541`) and `4683` is far past it. Neither figure was re-derived by the
trace form anywhere in `code/branching_locate_db09/`. **The document's ledger row
D5 says this correctly** — *"The two percentages come from `|F|` and `|AC|`
alone"* — and T3a says it too. The commit message is where the two things sit
next to each other with nothing between them. This is a **placement** defect in
the commit message, not a false claim in the document.

**This audit closes the `n = 5` half of the gap.** B4a runs the trace form with
no cap over all 87 poset classes to `n ≤ 5`: **87 of 87, 0 bad**, including
`|F| = 541`, where `dim kF/rad = 52` and the radical is `489 / 541 = 90.4%`. The
`n = 6` figure remains arithmetic on `|F| = 4683`, `|AC| = 203` and the cited
identity; **this audit did not establish it either.**

### X5 — "each listed with its size" lists twelve sizes for twenty classes

D5 and §4 item 5 say the 20 exempt classes are *"each listed with its size"*.
T3b prints a **set**: `[102, 104, 114, 120, 126, 132, 148, 150, 176, 220, 308,
541]`, twelve numbers. Measured here with multiplicity: `102×2, 104×2, 114×2,
120×1, 126×2, 132×1, 148×1, 150×2, 176×3, 220×2, 308×1, 541×1` — twenty classes,
eight of which are not individually identifiable from the output. The count 20
is right and no class was silently dropped; the wording overstates what the
output shows.

### X6 — "four elementary one-line derivations ... each is flagged in place" undercounts

§7 lists four: (a) symmetric ∧ unitriangular ⟹ identity; (b) a band is a regular
monoid; (c) one-dimensional modules give multiplicity-free branching; (d)
`kF(P)` semisimple iff `|F| = |AC|`. The census in B6a finds **eight**
derivations that are mg-db09's own rather than located, of which **three are not
flagged**:

1. T1a's "iff" (X2) — **false**;
2. §1's unconditional reading of Prop. 1.4 (X3) — **false**;
3. T3c's *"an algebra with identity Cartan matrix and one-dimensional simples is
   semisimple"*, and with it the general statement *"the two families intersect
   only at their semisimple point"* — **true** (`dim A = Σ C = #simples =
   dim A/rad`), but it is a claim about two whole classes of algebra, not about
   `kF(P)`, and it is a fifth one-liner.

**On the instruction itself.** The brief said *"Do not develop new
mathematics"* and, three paragraphs later, *"A multiplicity-free but
non-semisimple example, or a semisimple but non-multiplicity-free one, would
settle this faster than an argument."* Those two sentences pull opposite ways;
constructing a counterexample and checking published hypotheses on it **is**
mathematics, however elementary. mg-db09 says exactly this in its §7 and I agree
with its reading. **Measured, the delivery is disciplined**: the constructions
are of published algebras with published hypotheses evaluated on them, the
derivations are one-liners, and five of the eight are flagged in place. **The
instruction was substantially complied with**; the two unflagged wrong ones are
the cost of the shortfall, and both are in the same place — the reading of a
cellular datum as a branching structure.

### X7 — the successor's subject is not a sequence

§7: *"does the **`kF(P)` family** satisfy the axioms of a tower of recollement
(Cox–Martin–Parker–Xi)?"* A tower of recollement is a family `A_0, A_1, A_2, …`
indexed by an integer with `A_{n-2} ≅ e_n A_n e_n`. The `kF(P)` family is indexed
by **posets** — 63 of them at `n = 5`, as mg-db09's own T3d counts. There is no
sequence until a sub-family is chosen and §7 does not choose one. Named by
neither list.

---

## 5. THE SUCCESSOR IS PARTLY ALREADY IN HAND

My brief: *"check no successor search is routed at something already located …
verify what it would be searching for is not already in hand."*

mg-db09 files its successor as *"**untested** by this ticket and by every earlier
one, and testing it is new mathematics, which this ticket forbids"*, and names
what is untested: *"whether the `kF(P)` family carries the **idempotent
structure** its axioms require"*.

The axioms were fetched, not paraphrased (`arXiv:math/0411395` §1; the whole
extraction is committed with the PDF's SHA-256). Taking the **antichain family**
`A_n := kF(antichain_n) = kΣ_n` — the only sub-family that is a sequence, and the
one every figure in the document is about:

> **(A1)** *"For each `n ⩾ 2` we have an isomorphism `Φ_n : A_{n-2} → e_n A_n e_n`."*

In a left regular band `x y x = x y`, so `x kB x = k(xB)` with identity `x`. Take
`e_n = ({0,…,n-3}, {n-2}, {n-1})`. Then `e_n F` is `F(antichain_{n-2}) ×
F(antichain_1) × F(antichain_1)`. **Tested as an equality** — the explicit
bijection is checked to be a bijection and to carry the Tits product to the Tits
product over the whole multiplication table (B5b):

| `n` | `dim A_n` | `dim e_n A_n e_n` | `dim A_{n-2}` | band isomorphism? |
|---|---|---|---|---|
| 2 | 3 | 1 | 1 | **YES** |
| 3 | 13 | 1 | 1 | **YES** |
| 4 | 75 | 3 | 3 | **YES** |
| 5 | 541 | 13 | 13 | **YES** |
| 6 | 4 683 | 75 | 75 | **YES** |

**(A1) holds, and nothing in that test uses anything that was not in this
repository before mg-db09** — `F(P)`, the Tits product, and `xyx = xy`, all three
in the audited instrument's own kernel and in mg-af28's before it.

**(A3)** holds in the non-unital sense: `kΣ_n ↪ kΣ_{n+1}` by appending `{n}` as a
last block is multiplicative on the whole table, and its image is the corner
`x₀ kΣ_{n+1} x₀`. Whether CMPX intend a **unital** embedding is not settled here
and would have to be, by mg-db09's own "equalities, not resemblances" rule.

**(A2)(i)** — *"The algebra `A_n / A_n e_n A_n` is semisimple"* — measured over
**every** face idempotent realising (A1), because one failing choice would prove
nothing:

| `n` | `#` valid `e` | `dim A/AeA` | `dim rad` | (A2)(i) for **any** `e`? |
|---|---|---|---|---|
| 2 | 2 | 1 | 0 | yes (degenerate) |
| 3 | 6 | 7 | 3 | **NO — fails for every one** |
| 4 | 36 | 45 | 32 | **NO — fails for every one** |

**Scope, and it is the whole strength of the claim:** exhaustive over *face*
idempotents at `n = 3, 4` only. CMPX do not require `e_n` to be a face, and
non-face idempotents are not covered, nor is `n ≥ 5`. **This is evidence that
leans negative; it is not a proof.**

**Verdict on the successor.** It is *not* the failure mode my brief cites — it
would not come back empty, it would come back with a real answer. But its
**first axiom is already answerable from facts in hand and the answer is YES**,
and that axiom is the one mg-db09 names. A successor commissioned in §7's words
would spend part of its first cycle re-deriving a three-line consequence of the
Tits product. **§2 row 3 should move from *"located, NOT evaluated"* to
*"partially evaluated, (A1) yes, (A2)(i) leaning no"*.**

---

## 6. WHAT GOT STRONGER

### D9 — mg-db09's self-declared weakest citation is confirmed

§4 item 1 and D9: *"A cellular algebra has a symmetric Cartan matrix"* was taken
from the Wikipedia article, with *"Graham–Lehrer NOT read"*, and mg-db09 says
that if it is wrong, *"§2 row 1 collapses to 'not evaluated' and the enumeration
loses a row"*.

Graham–Lehrer 1996 is not on arXiv. A refereed arXiv paper that states the fact
and attributes it is, and this audit fetched it — **Ehrig–Tubbenhauer, *Relative
cellular algebras* (`arXiv:1710.02851`)**, verbatim:

> *"it follows from [KX99, Proposition 3.2] that `C(C)` is symmetric and positive
> definite in case `C` is a cellular algebra"* (Remark 2.19)
>
> *"(Or `C = D^T D`, written as matrices.)"* (after Theorem 3.23)
>
> *"by far not all algebras are cellular since e.g. their Cartan matrix has to be
> positive definite"* (§1)

`C = DᵀD` is the reason, and a Gram matrix is symmetric. **D9 is upgraded from
"secondary source, primary not read" to "stated and attributed in a refereed
source, with the proof indicated".** §2 row 1 stands.

mg-db09's own one-line consequence is also executed (B4c). The step it does not
spell out: "unitriangular with respect to **some** linear extension" means
`PCPᵀ` is lower unitriangular for a permutation `P`; permutation similarity
preserves symmetry, so `PCPᵀ` is symmetric and lower triangular, hence diagonal,
hence the identity. The predicted equivalence holds on **9 of 9** rows.

### The Cartan matrix, rebuilt from the formula mg-db09 declined to use

§4 item 4: *"An auditor should rebuild it from formula (4.9) instead."* Done —
`C_{X,Y} = Σ_{Z ≤ X} |e_Z B ∩ L_Y| · μ(Z,X)` with the Möbius function of `Λ(B)`:

| `P` | `\|Λ\|` | `dim A` | `Σ C` | unit diag | triangular | **per-column** | symmetric |
|---|---|---|---|---|---|---|---|
| antichain 2 | 2 | 3 | 3 | yes | yes | yes | NO |
| chain 2 | 2 | 2 | 2 | yes | yes | yes | yes |
| antichain 3 | 5 | 13 | 13 | yes | yes | yes | NO |
| chain 3 | 4 | 4 | 4 | yes | yes | yes | yes |
| V-poset 3 | 5 | 6 | 6 | yes | yes | yes | NO |
| antichain 4 | 15 | 75 | 75 | yes | yes | yes | NO |
| chain 4 | 8 | 8 | 8 | yes | yes | yes | yes |
| antichain 5 | 52 | 541 | 541 | yes | yes | yes | NO |
| chain 5 | 16 | 16 | 16 | yes | yes | yes | yes |

Agrees with T3c on every row. Two things worth recording. The **order convention
mg-db09 said it was least sure of is determined, not chosen**: (4.9) returns a
matrix with unit diagonal and correct column sums only under `X ≤ Y ⟺ X refines
Y`, and that is a check, not a convention. And the check used here — the
**per-column** identity `Σ_X C_{X,Y} = |L_Y|` — is strictly stronger than
mg-db09's `Σ C = dim A`, which is its total; the total cannot see an error that
moves mass between columns.

### The `|F(P)| ≤ 90` cap is gone

87 of 87 poset classes to `n ≤ 5`, 0 bad, nothing exempt (B4a). §4 item 5 says
*"This repo's largest error to date was invisible because a measurement ranged
over the set on which a false statement happens to be true."* The set is now the
whole set at `n ≤ 5`, and the statement is still true on it.

### The target's source file is not fabricated

T4 checks quotations against `sources_db09.txt`, a file mg-db09 wrote. B3a checks
**every content line of that file** — 172 lines — against this audit's own
`pdftotext` extraction of PDFs it fetched itself. **0 not found.** The target's
source windows are what the papers say.

### Quotations in the delivered prose

22 quotations taken out of the document's own text, including **9 that T4 does
not cover**: **21 verbatim, 1 deviation**. The deviation is §1's table row 3,
which prints *"the multiplicities are simple**,** or the branching is simple"*;
the paper has no comma. Meaning unchanged; recorded because it is in a row T4
does not check. Six negative controls of this audit's own devising, all rejected.

---

## 7. WHAT I COULD NOT ESTABLISH

Stated plainly, because my brief requires it and because the last thing this
lineage needs is a silence read as a negative.

* **D10, which is the deliverable.** *"`kF(P)` is quasi-hereditary"* rests on
  Putcha's theorem quoted through Margolis–Steinberg, with *"Putcha and Nico
  located, not read"* and the characteristic hypothesis unverified against the
  primary source. **This audit did not verify it either.** It is also CMPX
  (A2′), so it is the same open statement in both places. It is the single
  largest unverified load in the delivered document and the audit leaves it
  where it found it.
* **The `n = 6` figure, 95.7%.** `|F| = 4683` puts the trace form out of reach
  here. It remains arithmetic on counts plus the cited identity.
* **§7 item (b), "a band is a von Neumann regular monoid".** Not checked.
* **CMPX (A2)(ii), (A4), (A5), (A6)**, and whether (A3) requires a unital
  embedding.
* **Whether a non-face idempotent could satisfy (A2)(i)** for `kΣ_n`, and
  anything at `n ≥ 5`.
* **The negative in §2 — "not two values of one construction" — could not be
  attacked by construction**, and I want to be exact about why rather than let
  it pass. It is a search over **named umbrellas**, and mg-db09 says so
  (*"What this enumeration is not"*). The only constructions anyone has produced
  with both axes as values are the two the document books as **vacuous** (monoid
  algebras; AF realisation). Writing a non-vacuous one down would be new
  mathematics and is out of scope for both tickets. **So the negative is
  correctly qualified and correctly labelled, and I could not strengthen or
  break it.** The one row I could move is row 3, and §5 moves it.

---

## 8. CLAIM LEDGER FOR THIS AUDIT

| # | claim | status |
|---|---|---|
| **A1** | 5 of 5 of mg-db09's committed outputs regenerate byte-identically | **MEASURED**, `b0_repro.sh` |
| **A2** | the branching graph of `TL_n(β)`, defined as Vershik–Okounkov define it, has **different vertex sets** at `β = 0` and **multiplicities 2** at `β = 1` and `β = 0`; so §0's "same multiplicity-free graph at each" and T1d's "held FIXED" are false | **MEASURED**, B1a/B1b, with uniqueness, integrality and dimension checks on every solve |
| **A3** | the verdict D4 nevertheless stands, because `A ≅ ⨁ End(V_λ) ⟺ A` semisimple for every finite-dimensional algebra | **AN ARGUMENT FROM THE THEOREM mg-db09 QUOTES**, not a measurement, and labelled as such |
| **A4** | T1a's "iff" is false in the "if" direction; `TL_2(0)` satisfies the count and has no non-trivial idempotents | **MEASURED + a two-line exhaustive check** |
| **A5** | VO Prop. 1.4's centralizer criterion, stated unconditionally in §1, returns "multiplicity-free" at `β = 1` where the multiplicity is 2 | **MEASURED**, B1c |
| **A6** | `dim kF(P)/rad = \|AC(P)\|` on **87 of 87** classes to `n ≤ 5`, no cap, including `\|F\| = 541`; radical 90.4% from the trace form | **MEASURED, fourth instrument** |
| **A7** | the Cartan matrix by MSS (4.9) with the Möbius function agrees with T3c on all 9 rows, and passes the stronger per-column check | **MEASURED**, B4b |
| **A8** | all of T2a–T2d reproduces on a disjoint instrument | **MEASURED**, B7 |
| **A9** | D9 is confirmed and attributed in a refereed source (`arXiv:1710.02851`, Remark 2.19, citing König–Xi 1999 Prop. 3.2; `C = DᵀD`) | **QUOTED**, from a PDF this audit fetched |
| **A10** | `sources_db09.txt` is not fabricated: 172 of 172 content lines present in an independent extraction | **MEASURED**, B3a |
| **A11** | CMPX (A1) holds for `kΣ_n`, `2 ≤ n ≤ 6`, with the idempotent exhibited and the isomorphism checked entry by entry | **MEASURED**, B5b |
| **A12** | (A2)(i) fails for **every face idempotent** realising (A1) at `n = 3` and `n = 4` | **MEASURED, and scoped**: face idempotents only, `n ≤ 4` only |
| **A13** | eight derivations in mg-db09 are its own rather than located; three are unflagged; two of those three are wrong | **A CENSUS, and it is a judgement** — the classification is mine and is printed in full in B6a so it can be disputed row by row |
| **NOT CLAIMED** | that `kF(P)` is or is not quasi-hereditary; that `kΣ_n` is or is not a tower of recollement; that the `n = 6` radical figure was re-derived; that mg-db09's searches were or were not exhaustive; that anything here is new mathematics; that the walk, `λ₂`, `Δ_AT` or the pricing are touched | |

---

## 9. REPRODUCE

```
cd code/branching_audit_2060 && ./run_all.sh    # ~20 min, pure Python 3, NO NETWORK
```

Committed outputs: `out_b0_repro.txt`, `out_selftest.txt` (56 940 assertions),
`out_b1_branching.txt`, `out_b2_pathbasis.txt`, `out_b3_quotes.txt`,
`out_b4_ours.txt`, `out_b5_successor.txt`, `out_b6_ledger.txt`, `out_b7_gz.txt`.
Two of the `TOTAL BAD` lines are **findings, not errors**, and the README says
which: `b1`'s `TOTAL BAD: 2` counts the two disagreements between mg-db09's
stated claim and the measured branching graph, and `b3`'s `TOTAL BAD: 1` counts
the one non-verbatim quotation. The other six scripts end `TOTAL BAD: 0`, and
those count errors in this audit's own instrument.

`./fetch2060.sh` is the one network script and `run_all.sh` does not call it.
`sources2060/` holds the **whole** `pdftotext` extraction of each paper, gzipped,
with `SHA256SUMS.txt` for the PDFs they came from.

**Sources fetched and read by this audit**

- [Vershik–Okounkov, *A new approach to the representation theory of the symmetric groups. II*](https://arxiv.org/abs/math/0503040) — **read, in extract (§1)**
- [Ridout–Saint-Aubin, *Standard modules, induction and the structure of the Temperley–Lieb algebra*](https://arxiv.org/abs/1204.4505) — **read, in extract (§4, App. B)**
- [Margolis–Saliola–Steinberg, *Cell complexes, poset topology and the representation theory of algebras…*](https://arxiv.org/abs/1508.05446) — **read, in extract (§4.7)**
- [Margolis–Steinberg, *Quivers of monoids with basic algebras*](https://arxiv.org/abs/1101.0416) — **read, in extract (§1)**
- [Ehrig–Tubbenhauer, *Relative cellular algebras*](https://arxiv.org/abs/1710.02851) — **read, in extract (§1, Rmk 2.19, Thm 3.23)** — new to this lineage
- [Cox–Martin–Parker–Xi, *Representation theory of towers of recollement*](https://arxiv.org/abs/math/0411395) — **read, in extract (§1, axioms A1–A6)** — new to this lineage; mg-db09 had it as *"located, NOT evaluated"*
- Graham–Lehrer, *Cellular algebras*, Invent. Math. **123** (1996) — **still NOT read**; the Cartan-symmetry statement is now taken from Ehrig–Tubbenhauer rather than from Wikipedia
- König–Xi, Prop. 3.2 (1999) — **located, NOT read**; quoted at second hand through Ehrig–Tubbenhauer, whose sentence naming it is checked
- Putcha, J. Algebra **205** (1998) 53–76 — **still NOT read**, and D10 is still unverified

---

## 10. NOTE FOR pm-onethird

Three corrections to make and one row to move.

1. **`docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md` §0 and T1d**
   should stop saying the Temperley–Lieb branching graph is the same
   multiplicity-free graph at every `β`, and the 2×2 table's
   multiplicity-free-and-not-semisimple cell should carry `kF(P)` and not
   `TL_6(1)`. **The verdict does not change**; the sentence that credits the
   builds with settling it should.
2. **T1a's "iff" and §1's unconditional reading of Prop. 1.4** are both false as
   stated and both take one clause to fix.
3. **§2 row 3 is no longer "located, NOT evaluated"**: (A1) holds and is
   exhibited, (A2)(i) fails for every face idempotent at `n = 3, 4`. If a
   successor is filed, it should be filed against *that* state, and it should
   name the antichain family rather than "the `kF(P)` family".

**And one thing this audit is deliberately not doing.** It does not edit the
target document, `STATE.md`, the roadmap, or any other `Where-This-Lives` file.
Whether to fold these corrections back is pm-onethird's call.
