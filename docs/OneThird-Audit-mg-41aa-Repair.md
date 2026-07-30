# Independent audit of mg-41aa / `504ab6c` — the repair of two negatives that were refuted by construction

**Work item:** mg-5800 (pre-filed by pm-onethird before mg-41aa landed).
**Date:** 2026-07-30.
**Target:** `504ab6c`, which repairs `docs/OneThird-Branching-Graphs-Where-This-Lives.md`
and `code/branching_af28/` under mg-6ad0's audit (`ae21569`), and adds
`docs/OneThird-Branching-Graphs-Repair.md` and `code/branching_repair_41aa/`.
**Instrument:** `code/branching_audit_5800/`, 9 files, 38-assertion self-test,
importing nothing from `branching_af28/`, `branching_audit_6ad0/` or
`branching_repair_41aa/`. `./run_all.sh`, ~4 min plus one network fetch.

---

## 0. VERDICT

**THE REPAIR HOLDS. 0 BROKEN, 0 OVERSTATED NUMBERS, AND NOTHING THE AUDIT
STRENGTHENED WAS WEAKENED.** Every figure it publishes reproduces on a
disjoint instrument, including the three corrected fractions and both
denominators it took from A000112. Four findings follow, all MINOR, and none
of them touches a number.

**And the two attacks mg-41aa named against itself are now closed, not
inherited.** Its §7 item 1 says the converse of X1 is its weakest link —
exhaustive only to `n ≤ 5`, with `n = 6` carried by Birkhoff rather than
measured. Here `n = 6` is measured, **without Birkhoff**: intervals of Young's
lattice are built as *sets of partitions under containment*, `J(P)` is built
from order ideals, and the two are compared **as lattices**. 318 posets against
62 interval classes at `n = 6`: **0 counterexamples**. Its §7 item 2 says the
box bound was controlled only to `n ≤ 5`, and not at the three `n` where the
published counts live; it is run here at **every** `n` to 8 — **0 movements** —
and cross-checked at `n ≤ 5` against a sweep over every raw `(μ, λ)` pair in an
`(n+2) × (n+2)` box with no trimming at all (102 060 pairs at `n = 5`,
identical class set).

| | |
|---|---|
| **BROKEN** | none |
| **CONFIRMED, reproduced on a disjoint instrument** | R1, R2, R3, R4, R5, R6, R7 — every claim in mg-41aa's §8 ledger |
| **STRENGTHENED by this audit** | S1 the converse of X1 at `n = 6` without Birkhoff; S2 the box control at `n = 6, 7, 8`; S3 a definition-free proof that no finite poset is differential |
| **MINOR** | F1 the ledger records what the audit BROKE and not what it STRENGTHENED; F2 one beyond-brief positive claim reads stronger than it is; F3 the `n = 8` provenance chain is not closed by any control; F4 the premise the new headline stands on now sits only inside struck text |
| **OBSERVATION** | F5 §3.6 calls its own object a *semi-tower* |
| **NOT ESTABLISHED HERE** | that Brown §4.3's example is the grid; Bergeron–Li (3),(4),(5); Stanley (1988); the converse of X1 beyond `n = 6` |

---

## 1. THE NEW NEGATIVES, ATTACKED BY CONSTRUCTION

Three negatives in this arc have fallen, all refuted by **construction** rather
than by argument. So every negative mg-41aa writes was attacked by building the
object it says does not exist. None of them fell.

| # | the negative mg-41aa writes | what was built to break it | result |
|---|---|---|---|
| **N1** | no poset outside the **skew cell posets** has `J(P)` isomorphic to an interval of Young's lattice | every interval `[μ, λ]` of rank `n`, built **from partitions**, canonicalised as a lattice, and matched against `J(P)` for **every** poset class, `n = 1…6` | **0 counterexamples**; 107 of 405 are interval posets, the skew set is the same 107 |
| **N2** | the counts stop at 62 / 149 / 360 | the skew class set recomputed with the bounding box grown to `n+1` and `n+2`, at **every** `n` to 8 | **0 movements**; 62, 149, 360 |
| **N3** | `C_p ⊔ C_q` is a straight cell poset `D_λ` in **0** cases | every `λ ⊢ p+q` built and compared, `p, q ≤ 6` | **0 of 36** |
| **N4** | the grid is **not** `[∅, λ]` | every `λ` of the right size, not just the ones the struck reason rules out | **0 of 25** |
| **N5** | **no differential poset is finite** | see §3 S3 — a definition-free proof, stronger than the reason the document gives | holds, and holds harder |
| **N6** | **5** of the 33 Young–Fibonacci intervals to rank 6 are **not** distributive | each of the 5 re-checked by exhibiting the failing triple `a ∧ (b ∨ c) ≠ (a∧b) ∨ (a∧c)`; each of the 28 re-checked by rebuilding it as `J(P)` | 5 and 28, witness `221`, **0 bad** reconstructions |
| **N7** | the 2-element **antichain** is no `D_λ`, and `J(it) = [(1),(2,1)]` | both 2-cell straight shapes built; the isomorphism printed element by element | holds; `|[(1),(2,1)]| = 4` |
| **N8** | Bergeron–Li §3.6 exists and af28 did not evaluate it | a **fourth** PDF extractor, both spellings, hyphenation-aware | **6 of 6 strings found, 0 absent** |

### The three corrected fractions, re-enumerated

Denominators are **not** carried. They are enumerated here by adding a maximal
element over an order ideal — every poset has a maximal element, so the route is
exhaustive — and *then* cross-checked against A000112 as published.

| `n` | straight `D_λ` | skew = interval posets | all posets (mine) | A000112 |
|---|---|---|---|---|
| 4 | 3 | 11 | 16 | 16 |
| 5 | 4 | 26 | 63 | 63 |
| 6 | **6** | **62** | **318** | 318 |
| 7 | **8** | **149** | **2 045** | 2 045 |
| 8 | **12** | **360** | **16 999** | 16 999 |

**0 disagreements with mg-41aa on any cell, and 0 disagreements with A000112.**
af28's straight column `1,1,2,3,4,6,8,12` is reproduced unchanged, which is the
control that the fix did not move the number it was not about.

### `AT n ≤ 3 EVERY POSET IS A SKEW SHAPE POSET`

The part of X1 most likely to be restated loosely, and where the small-`n` work
lives. Checked directly: **1/1, 2/2, 5/5**, and the boundary is real — at
`n = 4`, **5 of the 16** posets are not skew cell posets — the first out is
three minimal elements under a common top, which no skew diagram realises. So "vanishing" is a
statement about `n ≥ 4`, exactly as the repaired text says, and the claim is
tight rather than loose.

### X2 — the grid

Three objects from three definitions: the grid `{0..p} × {0..q}` as a **product
of integer intervals**, `J(C_p ⊔ C_q)` from order ideals, and `[(q), (q+p, q)]`
from **partitions**. All three isomorphic for every `p, q ≤ 6` — 36 pairs, past
mg-41aa's 25 — with `|[μ,λ]| = (p+1)(q+1)` in every case, **0 bad**. And the
cell poset of `(q+p,q)/(q)` is `C_p ⊔ C_q`, **0 bad**.

The struck sentence's *reason* is true and insufficient, and both halves are
measured separately: `C_p ⊔ C_q` is no `D_λ` in **0 of 36** — the independent
reason being that every `D_λ` contains the cell `(1,1)`, which is below every
cell, so `D_λ` has a minimum while `C_p ⊔ C_q` with `p, q ≥ 1` has two minimal
elements — and the grid is `[∅, λ]` for **no** `λ` at all, checked over every
`λ` rather than inferred from the reason.

---

## 2. WHAT THE AUDIT CONFIRMED AND STRENGTHENED — DID THE REPAIR PRESERVE IT?

mg-6ad0 did not merely confirm the headline. Both of its strengthenings are
re-established here on this audit's own instrument, so the question is asked
against a measured fact and not against another ticket's report.

* **B1 is a LATTICE isomorphism.** `J(D_λ) → [∅, λ]`, with the map built here
  from the cell-count rule and the interval built from partitions: **meet and
  join preserved on every pair, all 44 partitions to `n ≤ 7`, 0 bad**, and the
  order relation checked in both directions, 0 bad. Confirmed.
* **B5 with no trace form and no cited theorem.** `F(P)` built as the
  `P`-compatible ordered set partitions under the block-intersection product;
  verified a left regular band; the `|AC(P)|` characters `χ_C(x) = [C ≤ supp x]`
  built **from the product alone**; `Φ` surjective (the characters linearly
  independent, exact rational arithmetic); `ker Φ` of dimension
  `|F(P)| − |AC(P)|` and **nilpotent in exact arithmetic** — all 87 classes to
  `n ≤ 5`, **0 bad**. So `dim kF(P)/rad = |AC(P)|`. Confirmed.

**Neither was weakened. The repair does not touch either row.** That is the
right answer to the question this ticket asked — and it is also F1.

---

## 3. WHAT THIS AUDIT STRENGTHENS

* **S1 — the converse of X1 at `n = 6`, without Birkhoff.** mg-41aa's §7 item 1
  names this as the first thing to attack: *"If Birkhoff's direction were used
  wrongly here, the `n = 6` row of R1b is a claim and not a measurement."* It is
  now a measurement. Intervals are built as `{ν : μ ⊆ ν ⊆ λ}` ordered by
  containment — no cell poset, no `J`, no join-irreducible — and compared with
  `J(P)` as lattices by canonical form. **0 counterexamples in either
  direction at `n ≤ 6`.** The weakest link is closed one `n` past where the
  repair left it.
* **S2 — the box control where the published counts live.** Run at every `n` to
  8, including 6, 7 and 8: **0 movements**. And at `n ≤ 5`, a control the repair
  did not run — every raw `(μ, λ)` pair in an `(n+2) × (n+2)` box, with no
  left-edge normalisation and no empty-row ban: 102 060 pairs at `n = 5`,
  **the identical class set**. The trimming argument is no longer load-bearing
  at `n ≤ 5` and is controlled at 6, 7, 8.
* **S3 — "no differential poset is finite", without appealing to the
  definition.** The repaired text licenses this from the definition (locally
  finite, infinitely many ranks). It does not need the definition: on a
  **finite** poset `U` is a finite matrix and `D = Uᵀ`, so
  `tr(DU) = tr(UᵀU) = tr(UUᵀ) = tr(UD)`, hence `tr(DU − UD) = 0`, while
  `tr(r·I) = r·|P| > 0`. **No finite non-empty poset is `r`-differential for any
  `r ≥ 1`, on any definition that includes `DU − UD = rI`.** X4's re-scoping
  therefore does not depend on which definition of "differential poset" a reader
  brings. *(Booked as an ARGUMENT, not as evidence: running it over examples
  would be the restatement mg-3b51 flagged as R1d. The matrix version over all
  405 posets to `n ≤ 6` returns 0, and is reported as FORCED.)*

---

## 4. FINDINGS

### F1 — MINOR. The ledger gained three rows for what the audit BROKE and none for what it STRENGTHENED

The repair adds **B2′**, **B4′** and **B7′** to the claim ledger, each recording
a correction. It adds nothing for the two results mg-6ad0 strengthened. Both
rows are byte-identical to their pre-repair versions:

* **B1** still reads *"order isomorphism checked on every pair in both
  directions"* — where the measured fact, re-established in §2 above, is a
  **lattice** isomorphism, meet and join, 0 bad. (af28's own `out_young.txt`
  has printed `lattice-iso bad: 0` since before the repair, on a test that
  checked only the order — so the ledger now understates a result its own
  output has been over-labelling.)
* **B5** still reads *"trace-form rank in exact rational arithmetic … the step
  from this to 'all irreducibles are 1-dimensional' is Brown's theorem, cited,
  not re-derived here"* — where mg-6ad0 re-derived it with no trace form and no
  cited theorem, and this audit reproduces that independently.

This is **not** an over-correction and not a hedge: the strengthening *is*
recorded, in the repaired document's header note and in the repair document's
§0. The defect is where it is recorded. The repair itself quotes mg-6ad0's
reason for caring — *"the defect is in the ledger, which is what downstream
readers quote"* — and then lands the negative outcomes in the ledger and the
positive ones outside it.

**Cost of the fix: two ledger cells.**

### F2 — MINOR, and it is the recursion this ticket was filed to catch

Diffing mg-41aa's brief (X1, X2, X3, X4) against the delivered change gives five
items no one of the four requires. Four are bookkeeping or explicitly declared:
the `Two → Three` one-liner count (declared in §6 as entailed by X2), the §5
item 5(c) verdict block, the new §9 record of X5–X7, and the header note.

The fifth **carries a new positive mathematical claim**, in two places:

> §2 heading: *"At the level of finite **intervals** the index-set contact
> **does** extend — to 28 of the 33 finite Young–Fibonacci intervals."*
>
> §3 row 10: *"Row 10 therefore has the **same index-set contact** this document
> headlines for Young's, on 28 of 33 intervals."*

X4 asked only that the old reading be re-scoped or dropped. This adds a claim.
**Every number in it reproduces here** — 33 intervals, 5 non-distributive with
witness `221`, 28 distributive, 28 reconstructions 0 bad, and 30 of 30 on the
Young side. The claim is true in its weak reading. The wording is the problem:

* The Young headline is a **classification**: the intervals of Young's lattice
  are `J(P)` for `P` **exactly** the skew cell posets — a named, closed class,
  which is the whole content of X1.
* The Young–Fibonacci sentence is **Birkhoff plus a distributivity count**:
  every finite distributive lattice is `J` of its join-irreducibles, so
  "28 of the 33 intervals are `J(P)`" says precisely "28 of the 33 intervals are
  distributive", which T8 already measured. No class of `P` is named, by anyone
  in this arc.
* And the families genuinely differ. Measured: the 28 distributive
  Young–Fibonacci intervals yield only **17 distinct posets `P`**, of which
  **5 are NOT skew cell posets** — 2 of the 4 that arise at `|P| = 5`, and 3 of
  the 5 at `|P| = 6`. So it is not the same family of index sets, and the
  divergence starts exactly where the counts get interesting.

"The same index-set contact" therefore reads as parity with a classification
where what is established is that both are ideal lattices.

**Cost of the fix: one clause** — *the same kind of contact; on the
Young–Fibonacci side the class of `P` is not named and is not the same class.*

### F3 — MINOR. The `n = 8` provenance chain is not closed by any control

`run_all.sh` and `code/branching_repair_41aa/README.md` say the `n = 8` number
*"is computed, not copied"* and that *"no file in this directory hard-codes
360."* Read strictly, the second half is false: `check_doc.py:146` contains the
literal `(8, 12, 360)` and `r1b_skew8.py:43` contains the literal `360`.

The substantive point is the chain, not the literals. The `360` that reaches
**the document** and **`code/branching_af28/out_young.txt`** comes from
`cited_skew = {7: 149, 8: 360}`, typed into `code/branching_af28/t_young.py:148`.
The `SKEW8_COUNT` pipe feeds only `r1_exactly.py`'s own table. So:

> **nothing compares the computed 360 with the published 360.** If
> `r1b_skew8.py` returned 361 tomorrow, `check_doc.py` would still pass, because
> it certifies `out_young.txt`'s row against its own typed constant.

**The number is right** — 360 is enumerated independently here — and
`out_young.txt` is honest about the provenance, marking the `n = 7, 8` cells `*`
and naming both instruments. It is the **warrant** that is loose, in exactly the
category mg-6ad0 raised as X5/X6 and mg-3b51 raised as R1d: a control that
cannot fire on the thing it appears to certify.

**Cost of the fix: one line in `check_doc.py`** comparing the `SKEW8` value in
`out_r1b_skew8.txt` with the row it certifies.

### F4 — MINOR. The premise the new headline stands on is now inside a STRUCK block, and is re-affirmed nowhere

The commit subject's second half is *"Brown's OWN §4.3 example lattice IS a
Young interval"*. It has two premises: **(a)** Brown's worked §4.3 example is
the `p × q` grid of lattice paths, and **(b)** that grid is the interval
`[(q), (q+p,q)]`. **(b)** is what this audit verified, from three definitions,
36 pairs, 0 bad. **(a)** is a locating claim about Brown (2000) — and after the
repair it appears in the document **only** inside the block quote marked
**STRUCK**, in the sentence *"His worked `§4.3` example is the `p × q` grid of
lattice paths (the 'kids walk' is `§4.4`)"*, with the live prose immediately
above saying the correction *"removes the sentence that used to be offered
alongside it"*.

The repair document's §2 does separate the struck sentence into three parts —
but the part it books as surviving is *"the grid **is** `J(C_p ⊔ C_q)`"*, which
is premise **(b)**'s neighbour, not premise **(a)**. Nowhere does either
document say that **(a)** survives the strike, and nobody in this arc has read
Brown (2000) for it: **B8 is a keyword census, not a reading.** So the strongest
new sentence in the commit rests on a premise that the same commit has
typographically retired.

**Cost of the fix: one clause** — re-affirm (a) outside the strike, or attach
*"on mg-af28's reading of Brown §4.3, which nobody in this arc has re-read"* to
the headline. Nothing measured changes either way.

### F5 — OBSERVATION, not a defect

§3.6 of `arXiv:math/0612170` calls its own object a **semi-tower**: *"In [3], we
consider a semi-tower of algebras with ρ not preserving unities."* It then gives
a sketch — *"We include only a sketch of the ideas; the details can be found in
[10]"* — and adapts §§3.2–3.4 rather than restating conditions (3), (4), (5).
mg-41aa pre-files the `[10]` deferral in its §7 item 3 (correctly: `[10]` is the
reference the paper gives). It does not quote "semi-tower", which is the paper's
own name for the weakened object, and which narrows *"the paper contains two
tower definitions"* toward *"a tower definition and a sketched semi-tower
variant"*. **Nothing in X3's conclusion moves**: row 3 is a hedge either way, and
the open question is correctly left open.

---

## 5. WHAT I COULD NOT ESTABLISH, STATED RATHER THAN LEFT TO BE DISCOVERED

* **That Brown (2000) §4.3's worked example IS the `p × q` grid of lattice
  paths.** I did not obtain or read Brown (2000). Everything downstream of "the
  grid" is verified here; the *identification* of the grid with Brown's example
  is mg-af28's reading, inherited unchanged by mg-41aa, and it is now struck
  text in the target document — see **F4**. The headline sentence **"Brown's OWN
  §4.3 example lattice IS a Young interval"** is exactly as strong as that
  reading and no stronger.
* **Bergeron–Li conditions (3), (4), (5) under the §3.6 weakening.** Untested by
  mg-af28, mg-6ad0, mg-41aa and by me. Confirmed by grep over all three
  instrument directories: every hit is a `print` naming the conditions, none is
  a test. mg-41aa's refusal to manufacture a verdict is correct.
* **Stanley (1988).** Still read by nobody, including me. My Young–Fibonacci
  code is a **fourth** implementation of the same published neighbour rule, which
  is a fourth consistency check and not independence — mg-41aa's §7 item 4 says
  this about itself and it is inherited unchanged.
* **The converse of X1 beyond `n = 6`.** At `n = 7` the ideal lattices reach 128
  elements and the search was not run.

---

## 6. TWO CONTROLS THAT FIRED — ON MY OWN INSTRUMENT

Recorded because both are controls this arc relies on, and neither catches what
it appears to certify.

1. **A counting sequence is not a control on a canonical form.** My `canon`
   chose its target colour class by dict-insertion order — a function of the
   labelling — so the minimum over its search tree was not canonical, and two
   isomorphic 20-element distributive lattices came out with different codes.
   **While that bug was live, the enumeration returned A000112 exactly:
   1, 2, 5, 16, 63, 318, 2045, 16999.** What catches it is random relabelling,
   now assertion 10 of the self-test.
2. **Fibonacci rank sizes are not a control on the Young–Fibonacci cover rule.**
   My first coding used "prepend a 1, or change the leftmost 1 to a 2" and
   reproduced `1,1,2,3,5,8,13,21` exactly. It is wrong. What caught it is
   `DU − UD = I` **as an operator identity** — the control mg-41aa also runs,
   and which is doing real work.

---

## 7. CLAIM LEDGER

| # | claim | status | scope |
|---|---|---|---|
| **A1** | 62/318, 149/2 045, 360/16 999 are correct | **MEASURED** | own enumeration, own canonical form; denominators enumerated **and** matched to A000112; straight column reproduced unchanged; box grown at every `n` to 8, 0 movements |
| **A2** | the "exactly" holds in both directions to `n ≤ 6`, **without Birkhoff** | **MEASURED** | intervals from partitions, `J(P)` from ideals, compared as lattices; 107 of 405; 0 counterexamples either way; unnormalised `(μ,λ)` sweep at `n ≤ 5`, identical |
| **A3** | at `n ≤ 3` every poset is a skew cell poset, and not at `n = 4` | **MEASURED** | 1/1, 2/2, 5/5; 11 of 16 at `n = 4` |
| **A4** | the grid is `[(q),(q+p,q)]`; and is no `[∅,λ]`; and `C_p ⊔ C_q` is no `D_λ` | **MEASURED / REFUTED BY CONSTRUCTION** | 36 pairs `p,q ≤ 6` from three definitions, 0 bad; both negatives checked over every `λ`, 0 hits |
| **A5** | 33 / 5 / 28 and witness `221`; 28 reconstructions | **MEASURED** | fourth Young–Fibonacci coding, controlled by `DU − UD = I` as an operator identity; Young side 30 of 30 distributive |
| **A6** | B1 is a **lattice** isomorphism; B5 holds with no trace form and no cited theorem | **MEASURED** | meet and join, 44 partitions to `n ≤ 7`, 0 bad; `ker Φ` nilpotent in exact arithmetic, all 87 classes to `n ≤ 5`, 0 bad |
| **A7** | Bergeron–Li §3.1 and §3.6 are both present, verbatim | **QUOTED** | fourth extractor, both spellings, hyphenation-aware, 6 of 6 found |
| **A8** | `code/branching_af28/` re-runs byte-identical, and the commit does not touch `code/branching_audit_6ad0/` | **MEASURED** | `run_all.sh` re-run here; `git status` clean afterwards; `git show --stat` over the auditor's directory is empty |
| **A9** | the struck sentences survive, and none stands in live prose | **MEASURED** | `a7_doc.py` reads both documents off disk; 27 checks, 0 failed; `check_doc.py` re-run, 29 checks, 0 failed |
| **NOT CLAIMED** | that Brown §4.3's example is the grid; that Bergeron–Li (3),(4),(5) are decided in either direction; that Stanley (1988) has been read; that the converse of X1 holds beyond `n = 6`; anything about `λ₂`, `Δ_AT`, pricing or publishability | | |

---

## 8. FOR pm-onethird

* **The repair is sound and can be treated as landed.** All four findings are
  MINOR and together cost about five lines of edit. None changes a number and
  none changes a verdict.
* **F1 is the one worth doing**, because it is cheap and because it is the
  failure mode this ticket was pre-filed against: the record now reads as if the
  audit only found faults, when it also strengthened two results.
* **F2 is the beyond-brief recursion, and it recurred.** mg-41aa's own §6
  pattern 2 says beyond-brief material holds the worst finding again. It held
  this one too — the only positive claim added beyond X1–X4 is the only claim in
  the commit whose wording outruns its evidence. Third generation in a row.
* **F3 and F4 belong with X5 and X6**, which are already unrepaired in §9: all
  four are about **warrant** rather than about a false finding, and they would
  be one ticket, not four. F4 is the one with a headline attached to it.

## 9. REPRODUCE

```
cd code/branching_audit_5800 && ./run_all.sh    # ~4 min, pure Python 3
```

Committed outputs: `out_selftest.txt` (38 assertions), `out_a1_counts.txt`,
`out_a2_exactly.txt`, `out_a3_grid.txt`, `out_a4_yf.txt`, `out_a5_b1b5.txt`,
`out_a6_quotes.txt`, `out_a6_grep.txt`, `out_a7_doc.txt`. `a6_quotes.py` is the
only step needing network; if the fetch fails it prints `NOT RUN` and X3 is
reported unverified rather than verified.
