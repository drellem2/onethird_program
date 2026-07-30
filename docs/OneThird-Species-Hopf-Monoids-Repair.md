# Repair of mg-7d75 / `6a22fbc` under mg-a61f's audit — one false extremal claim, one headline that disagreed with its own caveat, and a search that had to be *cancelled* rather than filed

**Work item:** mg-6f61. **Date:** 2026-07-30.
**Target:** `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md` and `code/species_7d75/`.
**Audit landed:** `docs/OneThird-Audit-mg-7d75-Species-Hopf-Monoids.md` (mg-a61f, `8e61d1a`).
**Instrument:** `code/species_repair_6f61/`, 6 Python files, 3 188-assertion self-test, sharing no code
with either audited directory. `./run_all.sh`, ~30 s, **no network**.

---

## 0. VERDICT

**This is a repair, not a retraction, and most of it runs *upward*.** mg-a61f confirmed the
headline — and made it stronger than mg-7d75 claimed: `(kF(P))^{Aut(P)}/rad =
k^{AC(P)/Aut(P)}` holds on **87 of 87 classes to `n ≤ 5` with no size cap** and **179 of 179
tested at `n = 6`**, measured through the trace form, and it is a **three-line corollary** of
the theorem mg-7d75 itself quotes. **20 of 21 numeric claims reproduce from a disjoint
instrument, and 11 of 13 quotations are verbatim against poppler-rendered PDFs.** None of that
is re-opened here.

**Eight items were landed. Three of the eight are corrections of statements that were false or
overstated; five are the document being harsher on itself than the evidence warranted.**

| # | mg-a61f's finding | direction | what this repair does |
|---|---|---|---|
| **X1** | §8 **C3**: *"the smallest poset with `AC(P) ≠ Π[n]` is `{a<c, b<d}`"* is **FALSE** | over, and broken | **corrected at source** — in the document and in `code/species_7d75/t1_grading.py`, where the claim is now **computed** instead of asserted. §1 |
| **X3** | §0's *"0 failures across 5 axioms on 4 399 basis elements"* — **three columns cannot fail** | over | **§0 brought into agreement with §5**, which was right; **every column's capacity to fail stated and demonstrated**, predicted-first. §2 |
| **X6 / X7 / X8** | AM §17.5 diverges (**pre-flagged**), Aguiar–Ardila §12 diverges (**not** pre-flagged), Marshall–Martin truncated | over | **both quotations corrected against the rendered extraction**, the truncation restored, and **which divergences were anticipated is now stated**. §3 |
| **terminology** | *"braid cone"* = `C(P)` in Aguiar–Ardila, = an element of `F(P)` in Marshall–Martin | — | **collision named in a boxed note in §1 of the target, usage fixed**, so the next reader does not re-import it. §4 |
| **S4** | the `S_n` half of the correspondence is **not verified** — two unread sources | under-stated | **stated in §0 and at every occurrence**, naming S4, Solomon, and Garsia–Reutenauer/Atkinson; §4's Fock functors marked **located, not re-derived**. §5 |
| **X2** | §2.3 filed as an unlocated measurement in **four** places, routing a successor to a search | **UNDER** | **all four hedges corrected, and the successor search CANCELLED.** §6 |
| **X4** | T3d's *"four candidates, three of them controls"* | over, control count only | **one control, computed twice.** The theorem is untouched. §7 |
| **X5** | control (ii)'s 1 442 failures **are** the 1 442 disjoint-ground-set pairs | over, evidence only | accounting corrected **and the conclusion explicitly marked as surviving.** §7 |

**And the finding that outlives the ticket: a self-aware prediction does not need to be WRONG
to do damage — it only needs to be INCOMPLETE, because it tells the reader where to look.**
Recorded as §14 of the target document, with the same limitation stated beside it. §8.

**mg-a61f's own battery was re-run UNMODIFIED against the repaired document** — see §9.

---

## 1. X1 — a general extremal claim, false, refuted by the document's own table sixty lines above

**What was wrong.** §8 C3, and the same sentence printed by `t1_grading.py` into
`out_t1_grading.txt`:

> ~~*"Smallest witness with `AC(P) ≠ Π[n]`: `P = {a<c, b<d}`, where `ad|bc` has a 2-cycle."*~~

**It is false. The smallest is the 3-element chain.**

```
P = a < b < c ,   X = {a,c} | {b}
a < b sends the block {a,c} to the block {b} ;  b < c sends {b} to {a,c} .   2-cycle.
```

**WHAT WAS CHECKED** (`out_r1_smallest.txt`, `r1_smallest.py`), on a third instrument sharing
no code with `code/species_7d75/` or `code/species_audit_a61f/` — posets carried as **tuples
of up-masks** and enumerated as the **fixed points of the transitive closure**, faces as
**block-index functions**, quotient acyclicity by **Kahn's algorithm**:

| `n` | labelled posets | `AC ⊆ Π[n]` | `AC = Π[n]` | **witnesses** | antichains |
|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | **0** | 1 |
| 2 | 3 | 3 | 3 | **0** | 1 |
| **3** | **19** | 19 | **13** | **6** | 1 |
| 4 | 219 | 219 | 45 | **174** | 1 |

All **6** witnesses at `n = 3` are printed with the partition each one loses; they are **one
isomorphism class — the 3-chain — in its 6 labellings**, and every lost partition has block
sizes `{2,1}`. `AC(P)` was computed **two ways** (as `supp(F(P))` and by acyclicity of the
quotient) and the routes agree on all 242 posets.

**THE PREDICTIONS WERE WRITTEN BEFORE THE RUN. 11 of 11 met**, including the two that carry
the finding: *smallest `n` = 3* and *6 labelled witnesses there*.

**THE CONTROL: the search must be able to return `n = 2`.** The identical sweep with
acyclicity replaced by the strictly stronger *"the quotient digraph has no edges at all"* —
under which `AC'(P) = Π[n]` iff `P` is an antichain — returns **`n = 2`**. So *3* is a fact
about posets and not a floor of the instrument.

**WHY C3'S OWN REASON DOES NOT SUPPORT ITS CONCLUSION.** The stated reason — *"a cycle needs
two blocks `B`, `C` with `b₁ < c₁` and `c₂ < b₂`"* — forces `|B| ≥ 2` and `|C| ≥ 1`, hence
`n ≥ 3`. **The reason is correct and it gives the bound 3.** The sentence then jumped to a
four-element example. **`{a<c, b<d}` is a witness** — verified here — **and is not the
smallest.**

**AND THE SHAPE OF THIS ERROR IS THE POINT.** It was a **general extremal claim, cited to
nobody, asserted rather than computed**, inside a section headed *CORRECTIONS TO THE RECORD*.
**The refuting evidence was already in the document**: T1e's own row *"13 of 19 at `n = 3`"*
sits sixty lines above the claim, in the table the paragraph is commenting on, and
`19 − 13 = 6`. Nothing had to be researched, fetched or re-derived. **It had to be read
up-page.** This is not a research failure and it should not be filed as one.

**FIXED AT SOURCE.** `t1_grading.py`'s T1e now **computes** the smallest witness from the same
sweep that prints the table, and **`bad` is incremented if it is not the 3-chain with 6
labellings** — so the assertion can no longer drift away from the measurement beside it. The
docstring records what the block used to say and why it was wrong. `out_t1_grading.txt` is
regenerated.

**CONSEQUENCE DOWNSTREAM: none.** Nothing in §0–§7 or the ledger depends on C3, and the
direction that *is* used downstream — the antichain gives all of `Π[n]`, T1d — is 0 bad to
`n = 6`.

---

## 2. X3 — three of the five columns could not fail, and §0 disagreed with §5 inside one document

**What was wrong, and it is not what it looks like.** §5 already said the right thing:

> *"what T5 establishes is **closure** of our two subspecies under published operations, which
> is exactly the question asked, and **not** that the operations are forced."*

and §0 said

> ~~*"it passes every Hopf-monoid axiom with 0 failures on 4 399 basis elements"*~~.

**Those are two sentences in one document that do not agree, and §0 is the part a successor
quotes.** The defect is the disagreement. **It is repaired by bringing §0 to §5, not by
weakening §5.**

**WHAT WAS CHECKED** (`out_r2_columns.txt`, `r2_columns.py`). mg-a61f's A3b establishes that
three columns do not respond to the *collection*; it does not ask whether they respond to
anything, so *"cannot fail"* was left as an inference. Here **each column gets a two-part
verdict and both halves are demonstrated**: the collection varied with the operations fixed,
then the operations varied with the collection fixed at `F`.

**Axis 1 — the collection varies, the operations are the published ones:**

| collection | on `[4]` | prod | coprod | assoc | coassoc | compat |
|---|---|---|---|---|---|---|
| `F` (ours) | 4 399 | 0 | 0 | 0 | 0 | 0 |
| the full ambient `P × Σ` | 16 425 | 0 | 0 | 0 | 0 | 0 |
| `F`-opposite (faces of the **opposite** cone) | 4 399 | 0 | 0 | 0 | 0 | 0 |
| `F`-broken (every 2nd element, closed under nothing) | 2 200 | **216** | **6 988** | 0 | 0 | 0 |
| chains only (not closed under ⊔; **is** closed under restriction) | 192 | **396** | 0 | 0 | 0 | 0 |
| even number of blocks (an arbitrary predicate) | 2 200 | 0 | **12 186** | 0 | 0 | 0 |

**Axis 2 — the operations vary, the collection is `F`:**

| mutation | prod | coprod | assoc | coassoc | compat |
|---|---|---|---|---|---|
| product = rotate(concat) | 7 984 | 0 | **12 192** | 0 | 20 388 |
| coproduct = restriction, tensor factors swapped | 0 | 40 468 | 0 | **266 459** | 0 |
| product = merge last block with first | 0 | 0 | 0 | 0 | **3 408** |

**THE PER-COLUMN VERDICT:**

| column | fails on a COLLECTION? | fails on an OPERATION? | so it is evidence about |
|---|---|---|---|
| product closure | **YES** | yes | **our subspecies** |
| coproduct closure | **YES** | yes | **our subspecies** |
| associativity | **NO — pinned at 0** | **YES** | the **ambient** operations |
| coassociativity | **NO — pinned at 0** | **YES** | the **ambient** operations |
| compatibility | **NO — pinned at 0** | **YES** | the **ambient** operations |

Associativity of concatenation and coassociativity of restriction are identities of tuples and
of sets, inherited from the Hadamard product; **no choice of sub-collection can move those
three columns.** They are verified **once**, not 4 399 times. **The honest count is two
columns**, and 4 399 is the size of the ambient degree-4 component, not a number of
independent tests. **And both closure columns return 0 for the full ambient and for the
deliberately wrong pairing as well as for ours**, so what they establish is **closure**, not
identification.

**A BONUS THE REPAIR OWES BACK.** The third operation mutation — *concatenate, merging the
last block of `F` with the first block of `G`* — stays inside the cone, is associative, keeps
the coproduct, and **breaks compatibility alone (3 408, everything else 0)**. §5's four
controls had no isolated compatibility control; this is one, and it is added to §5's table as
control (v).

### 2.1 Two of the 45 predicted cells missed, and both are kept

**A battery whose expectations are written after the run cannot be wrong, which is the same as
saying it cannot be evidence.** All 45 cells were written down before execution. Two missed,
and both are informative:

* **even-block-count, product closure: predicted `+`, got `0`.** I called it *"an arbitrary
  predicate with no closure meaning"*. It is not arbitrary: **concatenation adds block
  counts**, so parity survives it, and only the coproduct sees the predicate. **A predicate
  with no geometric content whatsoever passes the product-closure column** — which is X3's
  point about that column, arriving by an accident I did not foresee. It makes the reading
  stronger, not weaker.
* **swapped coproduct, compatibility: predicted `+`, got `0`.** Interchanging the two tensor
  factors is a **symmetry** of the compatibility axiom: swapping `Δ` on both sides permutes
  the four corners consistently and the two sides move together. Coassociativity is not
  symmetric that way and it fires, 266 459 times. **The lesson is X5's, one level up: a
  corruption is not a control until you know which column it can reach.**

Neither miss changes a per-column verdict — every column still has a demonstrated failure on
one axis or the other — so `R2 TOTAL BAD` counts **undemonstrated columns** (0) and the misses
are reported on their own line, `R2 PREDICTIONS MISSED: 2 of 45`. **A finding that is counted
as a fault gets edited away.**

---

## 3. X6, X7 — the quotations, and which divergence was anticipated

mg-a61f executed §10 item 1's own attack: all thirteen quotations re-extracted with poppler's
`pdftotext` from all three PDFs. **11 verbatim, 2 divergent, 1 truncated.**
`r3_quotes.py` re-derives each verdict here from the committed extraction
(`code/species_audit_a61f/quotes_a61f.txt`), **offline**, and additionally requires that the
**wrong text survives only inside the strike that replaces it**.

| quotation | pre-flagged by mg-7d75? | correction |
|---|---|---|
| **AM §17.5** — the species is `Π*` in both slots, not `Π` | **YES**, §10 item 1 says outright the species names were an inference | corrected in §4, and the **clean** sentence — three lines below the Joyal passage the document already quotes — is now quoted instead: *"The Hopf algebra `K(Π)` is the algebra of symmetric functions `Λ`…"*. **The reconstruction was never needed** |
| **Aguiar–Ardila §12** — `(ℝ^I)/ℝ^I` is not an expression the paper contains, and the inequality runs the other way | **NO** | corrected in §1 and in §9 row 6. The direction flip is harmless (`C(P)` is their braid cone of the opposite order); `(ℝ^I)/ℝ^I` is a symbol-drop artefact |
| **Marshall–Martin §2.1** — stopped one sentence short | **NO** | the omitted sentence is restored, and it is the terminology collision of §4 below |

**AN UNPREDICTED DIVERGENCE IN AN EXECUTED CHECK IS WORTH MORE THAN A PREDICTED ONE**, and the
document now says so in §4. The predicted one confirms the author knew the extraction was
lossy — it costs nothing and was already caveated. **The two unpredicted ones measure how far
the lossiness reached**, which is exactly what a pre-file structurally cannot tell you, because
a pre-file enumerates the places its author already suspects.

And note what found all three: **the check was executed rather than asserted.** mg-7d75 named
the right attack, ranked it first, and did not run it. A named attack that is not executed
produces the pre-flagged row and neither of the other two.

---

## 4. The terminology trap, named rather than merely fixed

**"Braid cone" denotes two different objects in the two sources §1 quotes, and they are the
two objects this ticket is about.** Marshall–Martin's very next sentence — the one mg-7d75's
quotation stopped short of:

> *"(These objects are called "braid cones" in [14], but we reserve that term for single cones
> of the braid arrangement.)"*

and [14] is Aguiar–Ardila. So:

| source | *"braid cone"* means | in our notation |
|---|---|---|
| **Aguiar–Ardila §12** | a cone cut out by `y(i) ≥ y(j)` — a **union** of cones of the arrangement | **`C(P)`** |
| **Marshall–Martin §2.1** | a **single** cone of the braid arrangement | **an element of `F(P)`** |

**`C(P)` and an element of `F(P)` are not the same kind of object**, and the whole of §2's
construction is the passage from one to the other. **Usage fixed** in the target: unqualified
*"braid cone"* means `C(P)`, Aguiar–Ardila's sense; a single cone is a **face**, never a braid
cone. **And a boxed note naming the collision is left in §1**, because the next reader will
otherwise re-import it from whichever of the two papers they open first.

**One count changes.** §1 concluded the dictionary is *"stated in three independent published
sources"*. It is stated in two; the third is a source recording that **the term is not
standard**. The dictionary `poset ↔ cone` is unaffected — nothing mathematical breaks. **The
word is what is contested.**

---

## 5. The boundary: the `S_n` half is UNVERIFIED

**The poset half is confirmed independently.** mg-a61f re-measured `(kF(P))^{Aut(P)}/rad =
k^{AC(P)/Aut(P)}` through the **trace form** — the one route mg-7d75 says it deliberately did
not use — on **87 of 87 classes to `n ≤ 5` with no size cap**, closing mg-7d75's 4 exemptions,
and **179 of 179 tested classes out of sample at `n = 6`**, two primes agreeing on every class.

**The `S_n` half was not independently verified, by anyone.** What is measured is Bidigare's
anti-isomorphism to `n ≤ 5` and that the semisimple quotient has dimension `p(n)` indexed by
`Π_n/S_n`. **The step from `k^{Π_n/S_n}` to *the character ring of `S_n`* is ledger S4, cited
to Solomon (1976) and to Garsia–Reutenauer/Atkinson — and neither was fetched or read, by
mg-7d75 or by mg-a61f.** The same applies to §4: the **Fock-functor statement is located in
the literature, not re-derived here**; what §4 measures is `Bell(n)` against `p(n)`.

**mg-7d75 labelled S4 correctly in the ledger from the start. What was missing is that it was
labelled only there** — §0, which is the part that gets quoted, presented the two halves as
one confirmed correspondence. **This repair states the boundary in §0 as the fourth thing that
must be said in the same breath as the yes, and marks it at every occurrence:** §0's headline
box, §0's specification table, §3 (with a two-row status table naming both unread sources),
§6 item 1, §9 rows 3 and 11, and ledger rows **S4** and **S5**.

**Being located is a real result. Presenting it as verified is not**, and the difference is
the difference between *"someone has proved this"* and *"we have checked this"*.

---

## 6. X2 — the correction that runs upward, and the search that was CANCELLED

**Four places in mg-7d75 treat §2.3's identity as an unlocated measurement**: ledger **S1**'s
scope, **§6 item 6** (*"measured, not proved, and is stated for `n ≤ 5`"*), **§10 item 2**
(*"the one place I assert a gap in the literature… the least reliable kind of negative this
repo produces"*), and **S12** (*"the weakest claim here"*).

**It is a three-line corollary of Aguiar–Mahajan §10.10 — which the document quotes in full —
plus the Reynolds operator.** `G` acts on `A = kF(P)` by algebra automorphisms and `|G|` is
invertible in characteristic 0, so `(−)^G` is exact; applied to `0 → rad A → A → k^{AC} → 0`
it gives `A^G/(rad A)^G = k^{AC/G}`, and `(rad A)^G` is a nilpotent ideal of `A^G` with
semisimple quotient, hence **is** `rad(A^G)`. mg-a61f checked both steps exactly over `Q` on
all 24 classes to `n ≤ 4`. **The argument has no `n` dependence**, so the `n ≤ 5` and
`dim ≤ 90` caps bound the instrument and not the statement.

**All four hedges are corrected**, and §2.3 in the target now says so in place.

**And the consequential part is the errand.** §10 item 2 sent a successor to *"read Saliola
and Commins before quoting §2.3 as anything but a measurement."*

> **That search cannot find anything, because nothing is missing.** It would come back
> *"no antecedent located"* — a sentence that enters the record as a **negative result about
> the literature** when it is a **fact about the routing**. **A wasted cycle is the cheap half
> of that. The false record is the expensive half**, because *"we searched and found no
> antecedent"* is exactly the kind of sentence that gets cited later.

**So the search is withdrawn rather than filed**, in §10 item 2, in S12 and in §7 item 3 of
the target. Saliola and Commins remain worth reading on their own account — Commins asks a
strictly harder question — and **if that ticket is filed, its brief must state that §2.3 is
already located as a corollary, so a null result reads as *"not stated"* and not as *"not
true"*.**

---

## 7. X4 and X5 — two over-claims of evidence, neither touching a conclusion

**X4 — the control count.** §2.2 said *"four candidate identifications… three of the four
columns are the control"*. Conventions A and B differ only by the order of composition in
`S_n`, so `c^γ_{α,β}(Sol, B) = c^γ_{β,α}(Sol, A)` identically — **0 mismatches at every
`n ≤ 5`** (mg-a61f A2d). `{anti/A, iso/B}` is **one** statement and it holds; `{iso/A, anti/B}`
is **one** statement and it fails. **One control, computed twice, and it fires.** The
separation of *isomorphism* from *anti-isomorphism* is unaffected and decisive — 472
mismatching structure constants at `n = 5` — and the theorem reproduces entry for entry from
mg-a61f's disjoint instrument. **Corrected in §0, §2.2 and ledger S2.**

**X5 — control (ii)'s numbers, and the conclusion that must not look retracted.** The Tits
control's **1 442** product-closure failures are **exactly** the 1 442 of 11 301 pairs whose
two factors have disjoint non-empty ground sets. `μ_{S,T}` takes factors on **disjoint** sets;
the Tits product intersects blocks; across disjoint sets every intersection is empty. **The
control fires on a type mismatch, not a near miss.**

**Its conclusion is right and is explicitly marked as surviving**, in §5, §6 item 5 and ledger
S7 — because a corrected number left beside an unmarked conclusion reads as a retraction. The
conclusion rests on the **structural** fact rather than on the counts, and it is load-bearing
elsewhere in this repo: **the band product is invisible to the Hopf structure, so nothing about
the walk, `λ₂` or `Δ_AT` follows from anything in mg-7d75.** Nothing downstream needs revising.

---

## 8. THE FINDING THAT OUTLIVES THE TICKET

**A self-aware prediction does not need to be WRONG to do damage. It only needs to be
INCOMPLETE, because it tells the reader where to look.**

mg-7d75 pre-filed an attack on itself at §10 item 6, naming §2.3 and §5. **Both arguments are
correct** — mg-a61f tested them directly and neither place is over the line. And the
document's one false mathematical statement is in a **third** place, §8 C3, inside a section
headed *CORRECTIONS TO THE RECORD*. The pre-file did not cover for it; **it aimed away from
it.** A named failure mode is a searchlight, and everything outside the beam gets darker.

Three properties of this failure mode, all visible here:

1. **It survives being right.** Both predictions held and the document still lost its one
   broken claim to the omission.
2. **It is invisible to its author by construction.** A pre-file enumerates the places the
   author already suspects, so re-reading one's own list can never lengthen it.
3. **It repeats at every scale.** §10 item 1 correctly predicted the AM §17.5 quote would be
   damaged; the **two** other divergences were found only because the check was **executed**.

**What follows is not "write longer lists".** A pre-filed attack list is a *contribution to* an
audit and never a *substitute* for one. Its value is highest where it names a **mechanism**
(*"the extraction drops ligatures and symbols"*) and lowest where it names **locations**
(*"check §2.3 and §5"*), because a mechanism generalises to places the author did not think of
and a location does not. **And the check that actually caught C3 was not a search at all: it
was reading up-page.**

This is recorded as **§14 of the target document**, where a future reader of mg-7d75 will meet
it, rather than only here.

> **THE SAME LIMITATION APPLIES TO THIS REPAIR, AND IT IS STATED BESIDE THE FINDING RATHER
> THAN LEFT FOR THE NEXT AUDITOR.** §14's list of *what mg-6f61 fixed* is a list of the places
> **mg-a61f named**, plus four folded in from a second filing that was shelved on collision —
> so it is complete only to the extent that those two were. **This repair conducted no
> independent search for defects mg-a61f missed.** A ninth defect, if one exists, is in exactly
> the position §8 C3 was in.
>
> **And there is direct evidence that one list is not enough: two readers of the same audit
> produced two different work-lists, and neither was a subset of the other.** The four items
> that arrived second — X2, X4, X5 and the sharpening of S4 — include **the single most
> consequential edit in this repair**, the cancellation of §10 item 2's search. Had the second
> filing not existed, this repair would have shipped without it and would have said so
> confidently.
>
> The instrument reports **2 of 45 predicted cells missed** (§2.1). Published rather than
> tidied.

---

## 9. WHAT WAS RE-RUN, AND WHAT THE REPAIR'S OWN CHECKER ENFORCES

**mg-a61f's battery, unmodified.** `code/species_audit_a61f/run_all.sh` reads the target
document in two of its six scripts (`a5_quotes.py` checks that every quotation it classifies is
still present; `a6_boundary.py` anchors its whole classification to three strings and fails
loudly on drift). **Re-run against the repaired document with no edits: `A1`–`A3`, `A5`, `A6`
`TOTAL BAD: 0`, and `A4 TOTAL BAD: 1`, which is X1 and is that battery's intended finding.**
Identical to its pre-repair run. Every struck sentence was left in place inside its strike
precisely so this would hold — **a repair that deletes the text an audit points at makes itself
unauditable.**

**`code/species_7d75/run_all.sh`, re-run after the source fix.** Six scripts, all
`TOTAL BAD: 0`, self-test 759 assertions. `t1_grading.py` now **fails** if the smallest witness
is not the 3-chain with 6 labellings.

**`check_doc.py` — and its negative half is the load-bearing half.** Ten false or superseded
sentences are each required to occur in the document **and to occur nowhere outside a
`~~struck~~` span**; twenty-five corrections are each required to be present; and the sixteen
strings mg-a61f's own scripts depend on are asserted to survive. A repair that adds a
correction beside a false sentence and leaves the false sentence in force has repaired nothing.

---

## 10. WHAT THIS REPAIR DID NOT DO

1. **It did not re-open the headline, the 20 reproducing numbers, or the 11 verbatim
   quotations.** mg-a61f confirmed all of them from a disjoint instrument and this repair takes
   that as given.
2. **It did not read Solomon, Garsia–Reutenauer/Atkinson, Aguiar–Mahajan 2020 or 2017, Saliola
   or Commins.** §5 above states the boundary that follows; it does not close it.
3. **It did not file, and explicitly recommends against filing, the §10 item 2 literature
   search.** §6.
4. **It did not conduct an independent search for defects mg-a61f missed.** §8, boxed.
5. **It did not edit `STATE.md`, the roadmap, or any other document.** The corrections C1 and
   C2 that mg-7d75 filed *about* mg-af28 are still unfolded; whether to fold them back remains
   pm-onethird's call, unchanged by this repair.
6. **It did not touch `code/species_audit_a61f/`.** The audit's outputs describe the document
   **as audited**; its verdict strings (*"DIVERGES"*, *"document still says it: yes"*) are
   correct about the pre-repair text and remain the record of what was found. `r3_quotes.py` is
   where the post-repair verdicts live.

---

## 11. REPRODUCE

```
cd code/species_repair_6f61  && ./run_all.sh    # ~30 s, pure Python 3, NO NETWORK
cd code/species_7d75         && ./run_all.sh    # ~46 s, the repaired source instrument
cd code/species_audit_a61f   && ./run_all.sh    # ~2 min, the auditor's battery, UNMODIFIED
```

Committed outputs: `out_selftest.txt` (3 188 assertions), `out_r1_smallest.txt`,
`out_r2_columns.txt`, `out_r3_quotes.txt`, `out_check_doc.txt`.
`R1`, `R3` and `CHECK_DOC` report no problems; **`R2 PREDICTIONS MISSED: 2 of 45` is not zero
and is meant to be read** (§2.1).
