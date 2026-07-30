# Independent audit of mg-7d75 / `6a22fbc` — species, Hopf monoids, and "one categorical operation"

**Work item:** mg-a61f (pre-filed by the mayor after mg-7d75 went out without an audit).
**Date:** 2026-07-30. **Target:** `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`
and `code/species_7d75/` (`6a22fbc`).
**Instrument:** `code/species_audit_a61f/`, 8 files, 456 328-assertion self-test, sharing no
code with the audited directory. `./run_all.sh`, ~2 min, no network; `./fetch_sources.sh`
is the one network script and `run_all.sh` does not call it.

---

## 0. VERDICT

**The mathematics holds. Every one of the 21 numeric claims I could recompute reproduces
exactly from a disjoint instrument except one, and the headline answer to Daniel's question
survives everything I could throw at it — including being carried past mg-7d75's stated
reach and then proved outright.**

> **The headline is CONFIRMED and is stronger than mg-7d75 claims it is.**
> `(kF(P))^{Aut(P)} / rad = k^{AC(P)/Aut(P)}` holds on **all 87 isomorphism classes to
> `n ≤ 5` with no size cap** — closing the 4 classes mg-7d75 exempted — and on **179 of the
> 318 classes at `n = 6`**, measured through the **trace form**, the one route mg-7d75 says
> it deliberately did not use (A1a, A1c; two primes, agreeing everywhere).
> **And it is a three-line corollary of the theorem mg-7d75 itself quotes** (A1d), so no `n`
> could ever have broken it.

**BROKEN — 1**

| # | where | what |
|---|---|---|
| **X1** | §8 **C3**; `t1_grading.py` T1e; `out_t1_grading.txt` | *"The smallest poset with `AC(P) ≠ Π[n]` is `{a<c, b<d}`"* is **false**. The smallest is the **3-element chain**, with `{min,max} \| {mid}` cyclic in the quotient. mg-7d75's own T1e row *"13 of 19 at `n = 3`"* records **6 labelled witnesses at `n = 3`**, sixty lines above the claim. **Internal contradiction, and it is the one derivation §10 item 6 does not point the auditor at** |

**MISCLASSIFIED — 1, and it is the reason this audit's verdict differs from the document's own**

| # | where | what |
|---|---|---|
| **X2** | ledger **S1**, **S12**; §2.3; §6 item 6; §10 item 2 | the headline identity is filed as *"MEASURED, NOT PROVED"*, capped at `n ≤ 5`, exempted on 4 classes over a `dim ≤ 90` cap, and its absence from the literature called *"the weakest claim in this document"*. **It is a corollary of Aguiar–Mahajan §10.10 — which the document quotes in full — plus the Reynolds operator.** Three lines, no size dependence, and there is nothing left for a citation search to find |

**OVERSTATED — 3**

| # | where | what |
|---|---|---|
| **X3** | §0 *"HOPF MONOID AXIOMS CHECKED… 0 failures across 5 axioms on 4 399 basis elements"*; §5 table; ledger **S6** | **three of the five columns cannot fail.** Fed a subset of `F` closed under nothing, the identical battery still returns assoc 0, coassoc 0, compat 0 while its closure columns fire (A3b). And the two columns that *can* fail return 0 for the **full ambient `P × Σ`** and for a **deliberately wrong pairing** as well as for ours. §5's own *"the honest reading"* paragraph says exactly this; **§0 does not, and §0 is what gets quoted** |
| **X4** | §2.2; `out_t3_bidigare.txt` T3d; ledger **S2** | *"Four candidate identifications were run… exactly two hold and two fail"* and *"three of the four columns are the control"*. Convention **B is identically the opposite algebra of convention A** (A2d, 0 mismatches at every `n ≤ 5`), so the four columns are **two statements each computed twice**. One control, run twice — not three. The theorem itself is reproduced correctly and exactly |
| **X5** | §5 control (ii); §6 item 5; ledger **S7** | the Tits-product control's 1 442 product-closure failures are **exactly** the 1 442 of 11 301 pairs whose two factors have **disjoint non-empty ground sets** (A3c). The Tits product intersects blocks; across disjoint sets every intersection is empty. The control fires on a **type mismatch**, not a near-miss. The conclusion it supports — the band structure is invisible to the Hopf monoid — is right and important; these numbers are not evidence for it |

**QUOTATION DEFECTS — 2 divergences of 13, and one truncation**

| # | where | what |
|---|---|---|
| **X6** | §4; ledger **S5** | the AM §17.5 block quote reads `K̄(Π)` / `K(Π)`; **the book says `Π*` in both slots**. §10 item 1 predicted this exact quote would be wrong and it is. Mathematically harmless — the book says on the same page *"Since `Π` and `Π*` are isomorphic"* — but it is inside quotation marks and it is not the book's text |
| **X7** | §1; ledger **S10** | the Aguiar–Ardila quote reads *"a cone in `(ℝ^I)/ℝ^I` cut out by inequalities of the form `y(i) ≤ y(j)`"*. **The PDF as served says `(R^I)* = R^I` and `y(i) ≥ y(j)`.** `(ℝ^I)/ℝ^I` is not an expression the paper contains. **Not pre-filed** |
| **X8** | §1 *"stated in three independent published sources"* | the Marshall–Martin quote stops **one sentence** before *"(These objects are called 'braid cones' in [14], but we reserve that term for single cones of the braid arrangement.)"* — and [14] is Aguiar–Ardila. The third source is not a third agreement; it is a source recording that the two papers use the term for **the two different objects this ticket is about** (`C(P)` vs an element of `F(P)`) |

**Beyond the brief — the primary target of this ticket.** mg-7d75's brief predicted that
*"do not develop new mathematics"* is the instruction most likely to be violated, and the
document pre-filed the attack at §10 item 6, naming **§2.3 and §5**.

**Tested directly. Neither named place is over the line** — §2.3 is a corollary of a quoted
theorem (X2) and §5 establishes closure under published operations, which is what the brief
asked for (X3). **The list is not complete, and the row it omits is the only broken one:
§8 C3.** Self-awareness did not fail here by buying cover for a violation; it failed by
**directing attention**. The document reasoned carefully about where new mathematics would
enter, named two candidates, and then made its one false mathematical statement in a third
place it had already stopped watching. §11.

---

## 1. X1 — §8 C3's "smallest witness" is false, and the document's own table refutes it

**What C3 says.** *"`AC(P) = Π[n]` holds for 3 of 3 posets at `n = 2`, 13 of 19 at `n = 3`
and 45 of 219 at `n = 4`, against 1 antichain each time. **Smallest witness with
`AC(P) ≠ Π[n]`: `P = {a<c, b<d}`**, where `ad|bc` has a 2-cycle."* With the reason:
*"a cycle needs two blocks `B`, `C` with `b₁ < c₁` and `c₂ < b₂`, which no poset on ≤ 2
elements admits."*

**Every count in that sentence is right.** 3/3, 13/19, 45/219 all reproduce (A4a), and so
does *"`AC(P) ⊆ Π[n]` for all 242 labelled posets to `n ≤ 4`"*.

**The extremal claim is wrong.** The stated reason rules out `n ≤ 2` — the two blocks need
`|B| ≥ 2` and `|C| ≥ 1`, so at least **three** elements — and the document then jumps to a
four-element example. The witness at `n = 3` is the **3-chain**:

```
P = a < b < c ,   X = {a,c} | {b}
a < b sends {a,c} → {b} ;  b < c sends {b} → {a,c} .   2-cycle.
```

`out_a4_counts.txt` A4b prints all **6** labelled witnesses at `n = 3` — one isomorphism
class, the 3-chain, in its 6 labellings — and the count of witnesses by `n`:

| `n` | labelled posets | with `AC(P) ≠ Π[n]` |
|---|---|---|
| 1 | 1 | 0 |
| 2 | 3 | 0 |
| **3** | **19** | **6** |
| 4 | 219 | 174 |

**`{a<c, b<d}` is a witness. It is not the smallest one.** And the row *"13 of 19 at
`n = 3`"* is sixty lines above the claim, in the same section, in the document's own table:
19 − 13 = 6 is exactly the count that contradicts it.

**Consequence: none downstream.** C3 is a record of a refuted hypothesis of the author's
own, kept deliberately; nothing in §0–§7 or the ledger depends on it. The direction that
*is* used downstream — *"the antichain gives all of `Π[n]`"*, T1d — is 0 bad and reproduces
(A4a). **What the error costs is not a result; it is the claim in §13 that the document
develops no mathematics.** §11.

---

## 2. X2 — the headline is a corollary, and four separate hedges treat it as an observation

### 2.1 What the document says about its own headline

`(kF(P))^{Aut(P)}/rad = k^{AC(P)/Aut(P)}` is §0's boxed formula and ledger row **S1**. Four
places qualify it:

* **S1** status: *"MEASURED + QUOTED"*, scope *"all 87 poset classes to `n ≤ 5`… (4 classes
  exempt from the nilpotency step only)"*;
* **§6 item 6**: *"measured, not proved, and is stated for `n ≤ 5`"*;
* **§10 item 2**: *"the one place I assert a gap in the literature… the least reliable kind
  of negative this repo produces"*;
* **S12**: *"the `Aut(P)` form… was **not located**… **the weakest claim here**"*.

### 2.2 The proof

Write `A = kF(P)`, `G = Aut(P)`, `k` of characteristic 0.

1. **`A/rad A = k^{AC(P)}`.** This is Bidigare's radical theorem. mg-7d75 quotes it in full
   from Aguiar–Mahajan §10.10 and I verified that quotation against the rendered PDF
   (§7): *"Bidigare [45] showed that `J` is precisely the kernel of its support map… Thus,
   `A/J` is the algebra of flats `Π[I]`."*
2. **`G` acts on `A` by algebra automorphisms** — it permutes `F(P)` and the Tits product is
   equivariant (checked, `selftesta61f.py`) — and `|G|` is invertible, so the Reynolds
   operator `e = (1/|G|) Σ_g g` makes `(−)^G` **exact**. Apply it to
   `0 → rad A → A → k^{AC} → 0`:
   `A^G / (rad A)^G = (k^{AC})^G = k^{AC/G}`.
3. **`(rad A)^G` is a nilpotent ideal of `A^G`**, so it sits inside `rad(A^G)`; and the
   quotient just computed is a product of copies of `k`, hence semisimple, so `rad(A^G)`
   sits inside `(rad A)^G`. They are equal, and `A^G/rad(A^G) = k^{AC(P)/G}`.

**Both steps checked exactly over `Q`** on all 24 classes to `n ≤ 4` (A1d): `dim (rad A)^G =
dim rad(A^G)` and `dim A^G/(rad A)^G = |AC(P)/G|`, 0 failures.

### 2.3 What that changes

| the document says | what is actually the case |
|---|---|
| *"measured, not proved"* | proved in three lines from a theorem it quotes |
| *"stated for `n ≤ 5`"* | no `n` dependence at all |
| 4 classes exempt over a `dim ≤ 90` cap | the cap is unnecessary; A1a runs all 87 with no cap and 0 failures |
| *"not located… the weakest claim"* | there is nothing to locate: it is a corollary, not a gap. **S12 should be withdrawn, not strengthened by a better search** |

**This is under-claiming, and it is the mirror image of the failure the brief was written to
catch.** §10 item 2 sends a future auditor to read Saliola and Commins *"before quoting §2.3
as anything but a measurement"*. That errand is now unnecessary. (Saliola and Commins remain
worth reading for §7 item 3 — whether the `Aut(P)` form is *stated* somewhere is still a
literature question — but nothing in this document waits on the answer.)

### 2.4 The identity carried further than mg-7d75 took it

**No cap, `n ≤ 5`** (A1a). All 87 classes, trace-form rank modulo `2147483647` and
`1000003`, agreeing on every class:

| `n` | classes | with `\|Aut\| > 1` | identity holds | fails | max `dim kF(P)` |
|---|---|---|---|---|---|
| 1–4 | 24 | 15 | 24 | 0 | 75 |
| 5 | 63 | 44 | 63 | 0 | 541 |

**Out of sample, `n = 6`** (A1c), on classes built by adjoining a maximal element to each
`n = 5` class — 318, matching A000112(6): **179 tested** (`|F(P)| ≤ 300`), **179 hold, 0
fail**, 139 skipped over the cap and counted.

**The rows between the two mg-7d75 prints** (A1b). §2.3 shows only `|Aut| = n!` (the
antichain) and `|Aut| = 1`. At `n = 5`:

| `\|Aut(P)\|` | classes | identity holds | of which `\|AC/Aut\| < \|AC\|` |
|---|---|---|---|
| 1 | 19 | 19 | 0 |
| 2 | 27 | 27 | 27 |
| 4 | 6 | 6 | 6 |
| 6 | 6 | 6 | 6 |
| 12 | 2 | 2 | 2 |
| 24 | 2 | 2 | 2 |
| 120 | 1 | 1 | 1 |

**43 classes sit strictly between the two rows the document prints, and on all 43 the
quotient by `Aut(P)` is strictly smaller than `AC(P)`** — so the group is doing work
everywhere in between, not only at the antichain. All 43 hold. **The document's "one
formula, two rows" reading is better supported than the document supports it.**

**Controls on the index set** (A1e), which mg-7d75 does not run — its T4d varies the *group*,
not the *index set*:

| `n` | classes | `Π[n]/G` disagrees | `Π[n]/G` agrees | open-cone flats disagree | agree |
|---|---|---|---|---|---|
| 2 | 2 | 0 | 2 | 1 | 1 |
| 3 | 5 | 1 | 4 | 4 | 1 |
| 4 | 16 | 10 | 6 | 15 | 1 |
| 5 | 63 | 55 | 8 | 62 | 1 |

Both fire. The second substitute is this repo's own largest recorded error — the
**open-cone** flats that mg-1953 R1 repaired — and it disagrees with the measured dimension
on 62 of 63 classes at `n = 5`. **The right-hand side of the identity is not a free
parameter.**

---

## 3. X3 — three of §5's five columns cannot fail, and the two that can do not separate us from anything

**What §0 says.** *"F and AC are closed subspecies of the Hadamard products `P × Σ` and
`P × Π` with 0 failures across 5 axioms on 4 399 and 2 685 basis elements."*

**Reproduced exactly** from code written here (A3a): 4 399 and 2 685 basis elements on `[4]`,
0 in every column.

**Then the same battery, unmodified, on three other collections** (A3b):

| collection | dim `[4]` | prod | coprod | assoc | coassoc | compat |
|---|---|---|---|---|---|---|
| `F` (ours) | 4 399 | 0 | 0 | 0 | 0 | 0 |
| **the full ambient `P × Σ`** | 16 425 | 0 | 0 | 0 | 0 | 0 |
| **`F`-opposite** (poset paired with faces of the **opposite** cone) | 4 399 | 0 | 0 | 0 | 0 | 0 |
| **`F` broken** (every second element, closed under nothing) | 2 200 | **195** | **5 610** | **0** | **0** | **0** |

**Reading.** Associativity, coassociativity and compatibility return 0 for a collection that
is closed under nothing. They cannot fail for *any* set of `(poset, face)` pairs, because the
operations are inherited from the ambient Hadamard product and associativity of
**concatenation** and coassociativity of **restriction** are identities of tuples and sets.
And the two columns that *can* fail return 0 for the full ambient and for a semantically
wrong pairing as well as for ours.

**So the fact established is one fact — our two subspecies are closed — not five**, and
`4 399` is the size of the ambient degree-4 component, not a count of independent tests.
The same applies to T5d: `supp : F → AC` is a morphism because `supp : Σ → Π` is one and the
Hadamard product of morphisms is a morphism; the 0/0/0 is inherited, not discovered.

**mg-7d75 says this itself, in §5:** *"what T5 establishes is **closure** of our two
subspecies under published operations, which is exactly the question asked, and **not** that
the operations are forced."* **That is correct and it is the right reading.** §0's phrasing
is the one that overstates it, and §0 is the part a successor quotes.

**And the honest reading is not a small result.** Marshall–Martin's proposition —
verified verbatim in §7 — is a published theorem of exactly this shape, and §9 row 7 already
routes §5 to it with *"§5 must not be read as new"*. **That routing is correct.**

---

## 4. X4 — the four Bidigare candidates are two statements written twice

**The theorem is reproduced and it holds.** A2 rebuilds both algebras from their definitions
— the descent algebra from permutations and descent sets in `kS_n`, the invariant algebra
from orbit sums of set compositions under the Tits product — with no code shared with
`code/species_7d75/`, and gets mg-7d75's T3d table **entry for entry**:

| `n` | iso/A | anti/A | iso/B | anti/B |
|---|---|---|---|---|
| 3 | 4 | **0** | **0** | 4 |
| 4 | 54 | **0** | **0** | 54 |
| 5 | 472 | **0** | **0** | 472 |

**The control count is what does not hold.** mg-7d75 §2.2: *"Two of four hold, two fail…
Three of the four columns are the control, and they fire."* But conventions A and B differ by
the order of composition in `S_n`, so `c^γ_{α,β}(Sol, B) = c^γ_{β,α}(Sol, A)` identically —
**0 mismatches at every `n ≤ 5`** (A2d). Therefore:

* `{anti/A, iso/B}` is **one** statement, and it holds;
* `{iso/A, anti/B}` is **one** statement, and it fails.

So the comparison **is** discriminating — iso is separated from anti, decisively, 472
mismatching structure constants at `n = 5` — and it survived **one** control, computed twice.
Not three. One of the three columns called "the control" (`iso/B`) is the surviving
identification in a mirror.

**A second thing a rendered reading of the source adds** (§7): Aguiar–Mahajan **§10.8.3**,
three pages before Theorem 10.13, already says *"This yields subalgebras of `S_n`-invariants
`(Σ[n])^{S_n} ↪ Σ[n]`… A basis for the subalgebra `(Σ[n])^{S_n}` is given by"* the orbit
sums. T3a and T3b measure that, correctly, and report it as a measurement; it is also stated
on the facing page of the theorem being reproduced. Likewise T4a's *"the `Aut(P)`-orbit sums
span a subalgebra — 0 failures"* is the same fact for a general finite group, and holds for
**every** group acting by algebra automorphisms on **any** algebra with a permuted basis.

---

## 5. X5 — control (ii) fires on a type mismatch

`μ_{S,T}` takes a face of a cone on `S` and a face of a cone on the **disjoint** set `T`. The
Tits product `F·G` is *"intersect the blocks of `F` with the blocks of `G`"* — so across
disjoint ground sets **every intersection is empty**. Both mg-7d75's `mu_tits` and mine paper
over that with a guard falling back to concatenation when either factor is empty.

**A3c counts it.** Of the **11 301** `(x, y)` pairs the product-closure sweep examines,
exactly **1 442** have both factors non-empty with disjoint ground sets — and the control
reports **1 442** product-closure failures. **The two numbers are the same number.**

So control (ii) does not show that the Tits product is a *near miss* for the Hopf-monoid
product. It shows the two maps are of different kinds, which is true and is exactly what §5's
own commentary says: *"They are different maps."* **§6 item 5's conclusion — the walk, its
eigenvalues and `λ₂` are not functions of the Hopf-monoid structure — is correct and is the
most consequential single line in the document for this repo's other arcs.** The 1 442 / 252
/ 11 020 add no evidence to it.

Controls (i) and (iii) are all-zero here too, and mg-7d75's explanations for both — the
`R_q` family at `q = 1`, and the opposite monoid — are consistent with what I measure.
Control (iv) reproduces at 75 512 coassociativity failures.

---

## 6. What reproduces, exactly

`out_a4_counts.txt` recomputes 21 claims from a disjoint kernel. **20 agree; 1 is X1.**

| claim | doc | measured |
|---|---|---|
| `Bell(n)`, `n ≤ 7` | 1,2,5,15,52,203,877 | ✔ |
| `p(n)` as `S_n`-orbits of `Π[n]` | 1,2,3,5,7,11,15 | ✔ |
| `\|Σ_n\|`, `n ≤ 5` | 1,3,13,75,541 | ✔ |
| labelled posets / classes | 1,3,19,219 / 1,2,5,16,63 | ✔ |
| `AC(P) ⊆ Π[n]`, 242 labelled posets | all | ✔ |
| `AC(P) = Π[n]` counts | 1,3,13,45 | ✔ |
| **smallest witness `AC(P) ≠ Π[n]`** | **`n = 4`** | **`n = 3` — X1** |
| `dim (kΣ_n)^{S_n} = 2^{n-1}` | 1,2,4,8,16 | ✔ |
| `\|Π_n/S_n\| = p(n)` | 1,2,3,5,7 | ✔ |
| classes with `Aut(P) = 1` | 1,1,2,5,19 | ✔ |
| T2's skipped classes at `n = 5` | 24 | ✔ |
| T4d, non-antichain classes | 1/4/15, all fired | ✔ |
| `dim K̄(F)_n` | 1,7,121,4399 | ✔ |
| `dim K(F)_n` | 1,4,24,218 | ✔ |
| `dim K̄(AC)_n` | 1,6,89,2685 | ✔ |
| `dim K(AC)_n` | 1,4,20,152 | ✔ |
| Bergeron–Li pairs / unital | 529 / 0 | ✔ |
| forgetful map to `Π`: product / coproduct | 0 / 22 614 | ✔ |
| T3d, every entry `n = 2..5` | 0/0/472 pattern | ✔ (A2c) |
| T5 basis elements | 4 399 / 2 685 | ✔ (A3a) |
| T5e controls (ii), (iv) | 1442/252/11020, 75512 | ✔ (A3c) |

**Two of these are true with no exceptions available to find**, and should not be read as
measurements that could have come out differently:

* **`0 of 529 unital`.** Concatenating two non-empty tuples gives at least two blocks; the
  identity face has one. The count is 0 for every pair of non-empty posets by inspection.
  mg-af28's 64 → mg-7d75's 529 is a wider net over a statement with no exceptions. The
  **correction** C1 rests on — that a Hopf monoid imposes no unitality on `μ_{S,T}` at all —
  is right, and is the most useful thing in §8.
* **T4d**, that `S_n` does not preserve a non-antichain cone. True because the cone has a
  smaller symmetry group. The substantive control on the identity varies the **index set**,
  and mg-7d75 does not run one; A1e does.

---

## 7. The quotations — mg-7d75's own attack #1, executed

§10 item 1: *"Every verbatim quote… was extracted… by a Flate-decode-and-string-scrape
routine, **not** read from a rendered page… An auditor should re-read §17.4, §10.10, Theorem
10.13 and §13.1.1 from rendered PDFs."*

**Done.** All three PDFs re-fetched and re-extracted with poppler's `pdftotext`, a
renderer-grade extractor. Passages committed in `code/species_audit_a61f/quotes_a61f.txt`;
`fetch_sources.sh` regenerates them. **11 of 13 quotations check out; 2 diverge.**

**The four passages §10 item 1 names: three clean, one wrong — and it is the one the document
already said was reconstructed.**

| quotation | verdict |
|---|---|
| **AM §10.10**, Bidigare's radical theorem | **verbatim**, word for word |
| **AM Theorem 10.13** | **verbatim**; the book does print the superscript `op`, so §2.2's anti-isomorphism reading is the book's |
| **AM §13.1.1**, the Hopf monoid of posets | **verbatim** |
| **AM §17.4/17.5** | **DIVERGES — X6.** The book's species is **`Π*`** in *both* slots, not `Π` |
| AM Definition 8.1, species | verbatim, including the `Set^×` description |
| AM §13.4.2, `e_{S,T}(p) = 0 ⟺ S` a lower set; posets are `P_0` | verbatim, both |
| AM §8.13, the Hadamard product of Hopf monoids | verbatim (from the book's introduction; §8.13 is indeed the Hadamard chapter) |
| AM "connected bimonoid… automatically a Hopf monoid" | verbatim, from a paragraph the book itself heads *"Antipode formulas (Chapter 11)"*. Attribution defensible; the result is also in §8.4 |
| Joyal's foreword, `K(p) = ⊕_n p[n]_{S_n}` | verbatim |
| AM "posets… as appropriate unions of chambers" | verbatim |
| **Aguiar–Ardila §12**, braid cone | **DIVERGES — X7** |
| Marshall–Martin §2.1, geometric realization | verbatim, **but truncated — X8** |
| Marshall–Martin's closure proposition | accurate |

**X6.** The §17.5 quote is presented as the book's text and is not: the species is `Π*`.
§10 item 1 says outright *"the species names in that quote are my inference from the
surrounding text"* — the inference got the **functor** right and the **species** wrong.
**Mathematically harmless:** §17.4.1 says *"Since `Π` and `Π*` are isomorphic"*, and the
whole table is there — `K(Π) = Λ`, `K̄(Π)` the symmetric functions in noncommuting variables.
**So §4's Bell(n)-vs-p(n) resolution is confirmed against the source**, with the species
corrected.

**And the reconstruction was not needed.** Three lines below the Joyal-foreword passage the
document already quotes, in clean prose with no dropped symbols:

> *"The Hopf algebra `K(Π)` is the algebra of symmetric functions `Λ` (when `k` is of
> characteristic 0), and it is self dual, since `Π` is self-dual."*

**X7, not pre-filed.** Aguiar–Ardila §12 as served reads *"a cone in `(R^I)* = R^I` cut out
by inequalities of the form `y(i) ≥ y(j)`"*. mg-7d75 has `(ℝ^I)/ℝ^I` and `y(i) ≤ y(j)`. The
direction flip is harmless (relabel `i ↔ j`); `(ℝ^I)/ℝ^I` is a symbol-drop artefact — the
same defect §10 item 1 describes, in a second place it did not predict. **Everything §1 does
with the quote — that `C(P)` is the literature's braid cone — survives it.**

**X8.** §1 concludes *"the dictionary `poset ↔ braid cone`… is stated in three independent
published sources"*. Marshall–Martin's next sentence, immediately after the words quoted:

> *"(These objects are called "braid cones" in [14], but we reserve that term for single
> cones of the braid arrangement.)"*

[14] is Aguiar–Ardila. **So the third source records that the term denotes two different
things in the two papers — and the two things are `C(P)` and an element of `F(P)`, the two
objects this ticket is about.** Two sources and a third that flags the terminology as
non-standard. Nothing mathematical breaks; the count does.

---

## 8. The candidate space — the defect this ticket's parent was filed over

mg-7d75 exists because a "no" was given twice over a candidate space of two. **§9 is the
correction and it works.** Thirteen rows, each with an explicit *searched / read / not read*
status. Against mg-a61f's list of five things that had to be *evaluated* rather than *named*:

| the brief asks | mg-7d75 | this audit |
|---|---|---|
| **species** | Definition 8.1 quoted and used as the grading | **evaluated.** Quote verified verbatim |
| **Hopf monoids** | axioms run on `F` and `AC`, four controls | **evaluated** — and what it establishes is closure, X3 |
| **combinatorial Hopf algebras (Aguiar–Bergeron–Sottile)** | §6 item 4: applies, and applies to everything, so identifies our object with nothing | **evaluated, and the negative is the right one.** Not independently checked here |
| **the Frobenius characteristic route** | §4, via `K(Π) = Sym` | **cited, not independently evaluated.** The `K(Π) = Λ` half is now verified against the source (§7); the identification of `K(Π)_n` with `⊕_n R(S_n)` as a **ring** rests on S4 |
| **coinvariants** | Bell(n) vs p(n) measured to `n = 7` | **evaluated**, reproduced (A4a, A4e) |

**Four of five evaluated, one cited.** Rows 4, 5, 8 and 9 of §9 — AM 2020, AM 2017, Saliola,
Commins — are marked **located and not read**, and that is honest and correctly labelled.
**This audit did not read them either**, so §9's non-locations are not re-searched here.

**The one load-bearing step this audit could not check is S4**, and mg-7d75 labels it
correctly: *"CITED, NOT DERIVED — Solomon; Garsia–Reutenauer/Atkinson, both from secondary
sources, **neither read**."* Everything from `k^{Π_n/S_n}` to *"the character ring of `S_n`"*
rests on it, and the sources are not among the three PDFs I fetched. **The entire `S_n` half
of the headline depends on an unread citation, and the document says so in the right place.**
It also states the un-tested residue precisely — that Solomon's labelling by cycle types
agrees with the orbit labelling by block sizes is not checked — and I add nothing to that.

---

## 9. Auditing the brief, not only the author

mg-a61f's instruction: *"the proposed resolution is pm-onethird's hypothesis and is
unverified… it came from the brief, so its author has no reason to doubt it."*

**The brief's hypothesis was: set partitions are a species; integer partitions are its
`S_n`-orbits, i.e. coinvariants.** Both halves reproduce (A4a, A4e), and §7 verifies the
Joyal and §17.4 statements that name the operation. **The brief was right, and mg-7d75
tested it rather than adopting it** — T1b computes the orbits *with actual permutations* and
checks that the block-size invariant is complete rather than assuming it, with a control
(the coarser "number of blocks" invariant) that fires at 4 of 6 values of `n`. That is the
right shape.

**Two places where the brief's framing is looser than the document's answer, and the document
does not flag either:**

1. **"ONE categorical operation" is answered by a composite of two.** §0 says *"The operation
   is `faces ↦ flats`"*. The §0 specification table then says Daniel's *"index by quotients,
   then take coinvariants of the grading"* is *"the **bosonic Fock functor**… and it is
   exactly the named operation he was reaching for"*. These are different operations —
   `A ↦ A/rad` on a face algebra, and `⊕_n p[n]_{S_n}` on a species — and §0 calls each of
   them "the" operation. **The formula is genuinely one formula in one argument** (A1b shows
   it holding across all seven values of `|Aut(P)|` at `n = 5`, not just the two extremes),
   so the answer is sound; what is loose is the word *one*, which is the word Daniel asked
   about.
2. **Invariants and coinvariants are used interchangeably and are never identified.** §2.3
   takes `(kF(P))^{G}` — **invariants**. §4 takes `p[n]_{S_n}` — **coinvariants**. In
   characteristic 0 these agree for a finite group, which is why the numbers match; the
   document never says so. The proof in §2.2 above supplies the missing step (the Reynolds
   operator is exactly what identifies them). **Not an error; a stated assumption that is
   not stated.**

---

## 10. Where mg-7d75 is stronger than it claims

Status language both ways, per this ticket's standing.

1. **The headline identity is a theorem, not a measurement.** §2 above. Every hedge on S1 and
   S12 can be dropped, and the `n ≤ 5` and `dim ≤ 90` caps with them.
2. **It holds across the whole range of `|Aut(P)|`, not only at the ends.** 43 intermediate
   classes at `n = 5`, all with `|AC/Aut| < |AC|`, all correct (A1b). The document prints
   only the two extreme rows, which is the weakest possible presentation of its own result.
3. **Bidigare is reproduced entry for entry from a second independent instrument** (A2c),
   including the 472-mismatch controls.
4. **The correction C1 is right and is the useful part of §8.** A Hopf monoid in species
   imposes no unitality on `μ_{S,T}`; mg-af28's Bergeron–Li negative does not transfer. Any
   successor citing af28 B7 against this route does have a false premise.
5. **§6's enumeration of what does not transfer is the most valuable section in the
   document,** and every item in it that I could check reproduces. Item 5 in particular — the
   band product is invisible to the Hopf structure, so nothing about the walk, `λ₂` or
   `Δ_AT` follows — is a load-bearing negative for this repo's other arcs and it is correct
   (even though its numbers are weaker evidence than they look, X5).
6. **§9's thirteen-row candidate space with per-row read/not-read status is the fix the
   parent ticket was filed to get**, and it is a real improvement over what mg-af28 and
   mg-6ad0 did.

---

## 11. THE PRIMARY TARGET — the prediction about itself

**The brief's prediction.** *"This is a locating exercise. Do not develop new mathematics.
Note that both BROKEN items in mg-af28, and the worst finding in three prior generations, sat
in beyond-brief derivations — so this instruction is the one most likely to be violated
here, and it will be audited."*

**The document's pre-file, §10 item 6.** *"The two places to check are §2.3 — where an
identity is measured that I did not find stated — and §5, where axioms are checked on objects
assembled here. In both cases what was done is evaluate published axioms against our objects,
which is what the brief asked for; but both are the shape of thing that becomes new
mathematics one sentence later, and neither takes that sentence."*

**mg-a61f's instruction.** *"Self-awareness is not a control… A ticket that predicted it
would derive new mathematics, and then did, has not been self-aware; it has been accurate."*

### 11.1 Every derivation classified

`out_a6_boundary.txt` prints the full table; the classification is anchored to strings in the
document, so it fails loudly if the document drifts. Summary:

| where | classification | verdict |
|---|---|---|
| §0 / S1, *the operation is faces ↦ flats* | **LOCATED** | AM §10.10, quotation verified |
| §2.3 / S1, the `Aut(P)` identity | **COROLLARY** | three lines from the quoted theorem (§2 above). **Not over the line — misclassified in the other direction** |
| §2.2 / S2, Bidigare | **LOCATED** | Theorem 10.13, reproduced exactly |
| §3 / S4, the character ring | **LOCATED, sources unread** | correctly labelled; the one thing this audit cannot check |
| §4 / S5, the two Fock functors | **LOCATED** | Joyal's foreword, verbatim |
| §5 / S6, the Hopf submonoids | **MEASURED (closure)** | what the brief asked for. **Not over the line** — X3 is about how it is described |
| §6.5 / S7, the Tits product | **MEASURED** | sound conclusion, weak evidence — X5 |
| §6.3 / S8, the map to `Sym` | **MEASURED** | sound |
| §8 C1 / S9, Bergeron–Li | **MEASURED + reasoning** | sound |
| §1 / S10, the braid-cone dictionary | **LOCATED** | X7, X8 |
| **§8 C3, "the smallest poset with `AC(P) ≠ Π[n]`"** | **DEVELOPED HERE** | a general extremal claim, cited to nobody — **and false. X1** |
| T6b, the Fock functors on **our** species | **DEVELOPED, then halted** | new invariants of a new object; the instrument's own output stops at *"identifying it would be new mathematics"* and does not identify it. **The line is respected.** Not in the document body and not in §10 item 6 |

### 11.2 The verdict

**1. Neither place §10 item 6 names is over the line.** §2.3 is a corollary of a quoted
theorem — the opposite of new mathematics. §5 establishes closure of two subspecies under
published operations, which is verbatim what the brief asked for, and A3b shows it
establishes nothing more. **On the substance, the boundary held.**

**2. The list is not complete, and the row it omits is the only broken one.** §8 C3's
extremal claim is a general mathematical statement, formed here, attributed to nobody, in a
section headed *CORRECTIONS TO THE RECORD* — and it is false, contradicted by the document's
own table sixty lines earlier. §10 item 6 aims the auditor at §2.3 and §5. **The error is in
§8.**

**3. So self-awareness failed as a control, and not in the predicted way.** It did not fail
by buying cover for a violation; there is no violation at either named place. **It failed by
directing attention.** The document reasoned carefully about where new mathematics would
enter, named the two candidates, argued correctly that neither crosses — and then made its
one false mathematical statement in a third place it had already stopped watching. **A named
failure mode is a searchlight, and everything outside the beam gets darker.** The pattern the
brief warned about ("a claim that reads as self-aware goes unchecked") is real here, but its
object is not the named claim; it is everything the naming excluded.

**4. The brief's formulation does not apply, and the document's actual failure is its
mirror.** *"A ticket that predicted it would derive new mathematics, and then did, has not
been self-aware; it has been accurate."* This ticket predicted it and then did not. What it
did instead was **misclassify the corollary it did produce**: four separate hedges treat a
two-line consequence of a quoted theorem as an unlocated measurement, and route a future
ticket to a literature search that cannot find anything because there is nothing missing
(X2). **Under-claiming, in the one arc that has over- and under-claimed within a day.**

**5. For the record on the standing pattern.** mg-3b51 found the first generation in this arc
where beyond-brief material was correct; mg-6ad0 found that exception did not hold. **Here it
half-holds:** of the two beyond-brief items the document identifies, both are correct and
both are correctly bounded; of the two it does not identify, one is correct and halted (T6b)
and one is false (§8 C3). **The instruction is now failing at the classification step rather
than at the derivation step** — the document knows what the line is and can argue about it
accurately; what it no longer does reliably is notice when it has stepped over one somewhere
it was not looking.

---

## 12. WHAT I COULD NOT ESTABLISH

Stated explicitly, per this ticket's standing.

1. **Anything about Solomon's theorem or Garsia–Reutenauer/Atkinson.** Not fetched, not read.
   The step from `k^{Π_n/S_n}` to *"the character ring of `S_n`"* — ledger **S4**, the whole
   `S_n` half of the headline — is **unverified by this audit**. mg-7d75 labels it
   correctly and I add nothing.
2. **Whether the `Aut(P)` form of the radical theorem is *stated* in Saliola or Commins.**
   Not read here either. §2's proof makes the question academic for this document's purposes,
   but it does not answer it.
3. **Anything about Aguiar–Mahajan 2020 or 2017.** §7 item 1 calls reading them the
   highest-value next action. I agree and did not do it. **That recommendation stands
   unaudited and I believe it is right.**
4. **Whether our `F` is a published Hopf monoid under a different name.** §7 item 2's
   question — Aguiar–Ardila's `P` inside `GP`, Marshall–Martin's `LOI`, AM's `P_q` — is
   untouched here. Marshall–Martin's closure proposition (verified verbatim) makes it more
   pressing, not less: a family of posets closed under disjoint union, induced subposet and
   filter deletion **is** what §5 measures on the `P` factor.
5. **The `n = 6` identity for the 139 of 318 classes with `|F(P)| > 300`,** and the whole
   `n ≥ 7` range. §2's proof covers them; **no measurement here does.**
6. **Whether the four candidate identifications in T3 were *designed* as two or as four.**
   A2d establishes that they *are* two. Whether mg-7d75 knew that is not a question code can
   answer, and §2.2's sentence *"the two that hold are the two that say anti-isomorphism"* is
   consistent with either reading.
7. **The Aguiar–Ardila PDF version.** X7 compares against the file served on 2026-07-30. If
   mg-7d75 read a different version, the divergence could be version drift rather than
   extraction damage. `(ℝ^I)/ℝ^I` is not a well-formed expression under either reading.

---

## 13. LEDGER

| # | claim | status | scope |
|---|---|---|---|
| **X1** | §8 C3's *"smallest poset with `AC(P) ≠ Π[n]` is `{a<c, b<d}`"* is **false**; the smallest is the 3-chain | **BROKEN** | all 242 labelled posets to `n ≤ 4`; 6 labelled witnesses printed at `n = 3`. Contradicts mg-7d75's own T1e row |
| **X2** | the headline identity is a **three-line corollary** of the quoted AM §10.10, not an unlocated measurement | **PROVED, and both steps checked exactly over `Q`** | all 24 classes to `n ≤ 4` for the exact check; the proof has no `n` dependence |
| **X3** | 3 of §5's 5 columns cannot fail; both closure columns pass for the full ambient and for a wrong pairing | **MEASURED** | ground set `[4]`; the broken subset fires 195/5 610 on closure and 0/0/0 on the rest |
| **X4** | T3d's four candidates are two statements each computed twice | **MEASURED** | `c^γ_{a,b}(Sol,B) = c^γ_{b,a}(Sol,A)`, 0 mismatches, every `n ≤ 5` |
| **X5** | control (ii)'s 1 442 product failures **are** the 1 442 disjoint-ground-set pairs | **MEASURED** | 1 442 of 11 301 pairs on `[4]` |
| **X6** | the AM §17.5 quote's species is `Π*`, not `Π` | **VERIFIED against a rendered PDF** | pre-filed by mg-7d75 at §10 item 1. Mathematically harmless |
| **X7** | the Aguiar–Ardila quote is not the paper's text | **VERIFIED against a rendered PDF** | not pre-filed. Mathematically harmless |
| **X8** | the Marshall–Martin quote is truncated one sentence before the paper contradicts the use made of it | **VERIFIED against a rendered PDF** | reduces *"three independent sources"* to two plus a caveat |
| **A1** | the headline identity holds on **87 of 87** classes to `n ≤ 5` with **no cap**, and **179 of 179** tested at `n = 6` | **MEASURED, by the trace form** | two primes agreeing on every class; mg-7d75's 4 exemptions closed |
| **A2** | mg-7d75's T3d, T5b/c, T5e, T1e, T4c, T4d, T6a–d tables reproduce **entry for entry** | **MEASURED from disjoint code** | 20 of 21 recomputed claims agree; the 21st is X1 |
| **A3** | 11 of 13 quotations are verbatim against poppler-rendered extractions | **VERIFIED** | including all four passages §10 item 1 names |
| **A4** | the primary target: §10 item 6's list of beyond-brief places is **incomplete**, and the omitted row is the only broken one | **CLASSIFIED, anchored to the document's text** | §11 |
| **NOT ESTABLISHED** | S4 and everything resting on it; the AM 2020/2017 recommendation; whether `F` is a published Hopf monoid; the identity for `n ≥ 7`; §12 items 1–7 | | |

---

## 14. REPRODUCE

```
cd code/species_audit_a61f && ./run_all.sh      # ~2 min, pure Python 3, NO NETWORK
./fetch_sources.sh                              # the one network script; not called above
```

Committed outputs: `out_selftest.txt` (456 328 assertions), `out_a1_headline.txt`,
`out_a2_bidigare.txt`, `out_a3_hopf.txt`, `out_a4_counts.txt`, `out_a5_quotes.txt`,
`out_a6_boundary.txt`, and the verified passages in `quotes_a61f.txt`.
`A4 TOTAL BAD: 1` is X1 and is the intended finding; every other `TOTAL BAD` is 0.

**Sources re-read for §7**

- [Aguiar–Mahajan, *Monoidal Functors, Species and Hopf Algebras*](https://pi.math.cornell.edu/~maguiar/a.pdf)
- [Aguiar–Ardila, *Hopf monoids and generalized permutahedra*](https://arxiv.org/abs/1709.07504)
- [Marshall–Martin, *Hopf monoids of set families*](https://ajc.maths.uq.edu.au/pdf/92/ajc_v92_p419.pdf)

---

## 15. NOTE FOR pm-onethird

Three things this audit deliberately does **not** do.

* It does **not** edit `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`,
  `STATE.md`, the roadmap, or any prior document. X1 is a statement **about** mg-7d75, filed
  here; whether and how to repair it is pm-onethird's call. The repair is one sentence.
* It does **not** re-open §9's non-locations. Rows 4, 5, 8, 9 stay *located and not read*.
* It does **not** claim novelty for anything, including the proof in §2.2, which is standard
  characteristic-0 invariant theory applied to a quoted theorem and is offered as the reason
  a claim should be **downgraded from a gap to a corollary**, not as a result.

**The one action item that is not pm-onethird's judgement call:** any successor that reads
§10 item 2 and goes off to read Saliola and Commins *"before quoting §2.3 as anything but a
measurement"* is being sent on an errand that §2.2 above has already closed.
