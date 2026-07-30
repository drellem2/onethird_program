# Repair of mg-af28 / `358beff` under mg-6ad0's audit — the two BROKEN negatives and the two over-wide readings

**Work item:** mg-41aa. **Date:** 2026-07-30.
**Target:** `docs/OneThird-Branching-Graphs-Where-This-Lives.md` and `code/branching_af28/`.
**Audit landed:** `docs/OneThird-Audit-mg-af28-Branching-Graphs.md` (mg-6ad0, `ae21569`).
**Instrument:** `code/branching_repair_41aa/`, 7 files, 36-assertion self-test, sharing no
code with either audited directory. `./run_all.sh`, ~4 min plus one network fetch.

---

## 0. VERDICT

**This is a repair, not a retraction. The headline survives and comes out stronger on both
of the BROKEN items.**

> mg-6ad0 confirmed B1 as a **lattice** isomorphism `J(D_λ) → [∅, λ]` — meet and join
> preserved on every pair over 44 partitions to `n ≤ 7`, **0 bad** — and confirmed B5 by a
> route using no trace form and no cited theorem. Neither is touched here. And the two
> BROKEN items both correct the record **toward** the contact, not away from it: X1 says the
> family of posets whose ideal lattice is an interval of Young's lattice is **10 to 30 times
> larger** than mg-af28 counted, and X2 says **Brown's own worked `§4.3` example lattice is
> an interval of Young's lattice** — on a sentence mg-af28 offered as evidence that it was
> not.

| # | mg-6ad0's finding | what this repair does |
|---|---|---|
| **X1** | ledger **B2**'s *"exactly the cell posets"* is FALSE; the three fractions count a strictly smaller class | **fixed at source** in §0 consequence 1, in the ledger, in `t_young.py`'s T2 and in `out_young.txt`; the "exactly" is now **tested**, in both directions, exhaustively |
| **X2** | §0 consequence 3's grid sentence is FALSE | **struck at source**, quoted where it stood, and replaced by the constructed interval |
| **X3** | row 3's *"no tower"* was licensed against one of the cited paper's **two** tower definitions | **re-scoped to a hedge plus a NAMED OPEN QUESTION.** No proof is manufactured: conditions (3),(4),(5) under §3.6 are untested by anyone and testing them is new mathematics |
| **X4** | *"reaches the Young graph and no other differential poset"* is true only where it is vacuous | **re-scoped** in §1 row 6, §2 item 2, §3 row 10 and ledger B4 to the level at which it has content |
| **X5, X6, X7** | — | **NOT repaired.** Outside this ticket's brief; recorded in the target document's new §9 so they are not lost. See §6 below |

**mg-6ad0's own battery was re-run UNMODIFIED against the repair** — see §5.

---

## 1. X1 — the word "exactly", and the test nobody ran

**What was wrong.** Ledger B2, the T2 docstring in `code/branching_af28/t_young.py`, and the
header of the committed `out_young.txt` all said: *"the posets `P` for which `J(P)` is an
interval of Young's lattice are **exactly** the cell posets"*, and gave 6/318, 8/2 045,
12/16 999. T2 computed `{canon(D_λ) : λ ⊢ n}` — the **straight** cell posets — and nothing
else. The word "exactly" was asserted in three places and tested in none.

**What is true.** An interval `[μ, λ]` is the set of `ν` with `μ ⊆ ν ⊆ λ`; under
`ν ↦ ν/μ` it is the ideal lattice of the **skew** cell poset `λ/μ`. So the class named is
the skew cell posets, which strictly contains the straight ones.

**WHAT WAS CHECKED.** Three things, on an instrument that shares no code with either
predecessor.

1. **The smallest witness, with the isomorphism constructed rather than asserted** (R1a).
   Both 2-cell straight shapes `(2)` and `(1,1)` give the 2-**chain**, so the 2-element
   **antichain** is no `D_λ`; the skew shape `(2,1)/(1)` *is* the 2-antichain; and the
   induced map `J(2-antichain) → [(1), (2,1)]` is printed element by element and verified a
   bijection and order-preserving in both directions.
2. **The forward direction, exhaustively to `n ≤ 6`** (R1b). For **all 405** isomorphism
   classes of poset on `n ≤ 6` elements, decide whether `J(P)` is an interval by
   **constructing** an explicit map `J(P) → [μ, λ]` — ideal `I ↦` the partition whose row `i`
   is `μ_i` plus the number of cells of `φ(I)` in row `i` — and checking it on **every pair
   of ideals in both directions**. Result: **107** of the 405 are interval posets, **0 bad
   maps**, and the class af28's "exactly" names contains only **17** of them. **90 posets
   to `n ≤ 6` are interval posets that B2's wording excludes.**
3. **The converse, exhaustively to `n ≤ 5`, plus the reason the search is complete** (R1c).
   For every poset class that is *not* a skew shape, `J(P)` was tested against **every**
   interval `[μ, λ]` of the right rank and the right size — **4 700** isomorphism
   tests (180 at `n = 4`, 4 520 at `n = 5`), **0 hits**. And the structural reason: an
   order isomorphism of finite lattices carries
   join-irreducibles to join-irreducibles, and the join-irreducibles of `J(P)` are the
   principal ideals, i.e. `P`; measured, the join-irreducible poset of `[μ, λ]` is the cell
   poset of `λ/μ` on **every** skew shape to `n ≤ 6`, **0 bad**.

**WHAT A FALSIFIER WOULD HAVE LOOKED LIKE.** For the *corrected* claim: a poset in one class
and not the other — either a skew shape whose constructed map fails a check (⊆ direction), or
a non-skew poset whose `J(P)` matches some interval (⊇ direction). Both were searched for
exhaustively in the stated ranges and neither exists. For the *enumeration*: mg-6ad0
pre-filed the attack itself (its §11 item 4) — the counts are bounded by the claim that a
skew diagram with `n` cells fits in the `n × n` box after trimming, and if that is wrong the
counts are lower bounds. **Checked by growing the box**: at `n = 1…5` the class count is
identical for box `n`, `n+1` and `n+2`, **0 movements**.

**THE CORRECTED NUMBERS**, reproduced independently and agreeing with mg-6ad0's to the digit:

| `n` | straight `D_λ` (af28's number) | skew = interval posets | all posets | af28's fraction | corrected |
|---|---|---|---|---|---|
| 4 | 3 | 11 | 16 | 0.1875 | 0.6875 |
| 5 | 4 | 26 | 63 | 0.0635 | 0.4127 |
| 6 | **6** | **62** | 318 | **0.0189** | **0.1950** |
| 7 | **8** | **149** | 2 045 | **0.0039** | **0.0729** |
| 8 | **12** | **360** | 16 999 | **0.0007** | **0.0212** |

At `n ≤ 3` **every** poset is a skew cell poset (1/1, 2/2, 5/5), so the word "vanishing" is a
statement about `n ≥ 4`.

**WHAT SURVIVES.** Consequence 1's *direction* — ours contains theirs, as a vanishing
fraction — survives on either column, which is why this is a correction and not a
retraction. §0's **headline** was correctly restricted all along (*"its finite intervals
`[∅, λ]` are exactly the `J(P)` for `P` a cell poset `D_λ`"*) and is untouched; the defect
was that the restriction was dropped in the ledger, in the code and in the output, and one
downstream sentence was false because of it (§2 below).

**FIXED AT SOURCE.** `t_young.py`'s T2 now states both classes, measures both to `n ≤ 6`,
prints the witness, and marks its `n = 7, 8` skew counts with the two instruments that
produced them. `core_af28.py` gains `skew_cell_poset` and `skew_shape_classes`.
`selftest.py` gains four assertions on the skew column and the witness (27 → 31), and
`out_young.txt` is regenerated.

---

## 2. X2 — Brown's own example lattice **is** an interval of Young's lattice

**What was wrong.** §0 consequence 3 read: *"that grid is `J(C_p ⊔ C_q)`, which for
`p, q ≥ 1` is **not** an interval of Young's lattice — `D_λ` has a minimum and `C_p ⊔ C_q`
does not."* This is one of the three elementary derivations mg-af28 flagged as its own and
pre-filed for audit by name at its §5 item 5(c).

**The reason is TRUE and the conclusion is FALSE.** "`D_λ` has a minimum" rules out
intervals of the form `[∅, λ]` and says nothing about `[μ, λ]` with `μ ≠ ∅`, whose poset is
a skew shape and need not have a minimum. It is the same gap X1 opens, one sentence
downstream.

**WHAT WAS CHECKED**, separating the sentence's three parts so that a right half and a wrong
half are not confused:

* **the first half** — the grid **is** `J(C_p ⊔ C_q)`. Built the grid `{0..p} × {0..q}`
  **directly as a product of two integer intervals**, not as `J` of anything, and checked it
  isomorphic to `J(C_p ⊔ C_q)`: all 25 pairs `p, q ≤ 5`, **0 bad**. af28 is right here.
* **the stated reason** — `C_p ⊔ C_q` is not any `D_λ` with `p+q` cells: **0 of 25** are, so
  the reason is true, and what it establishes is that the grid is not `[∅, λ]`. That is all
  it establishes.
* **the conclusion** — take `λ = (q+p, q)`, `μ = (q)`. Row 0 keeps columns `q … q+p-1`, row
  1 keeps columns `0 … q-1`, so the two blocks are incomparable and `λ/μ ≅ C_p ⊔ C_q`. The
  map grid `→ [μ, λ]` is **constructed and verified pair by pair in both directions**, all
  25 pairs `p, q ≤ 5`, with `|[μ, λ]| = (p+1)(q+1)` in every case, **0 bad**.

**WHAT A FALSIFIER WOULD HAVE LOOKED LIKE.** A pair `(p, q)` for which no order isomorphism
grid `→ [(q), (q+p, q)]` exists, or for which the constructed map fails bijectivity or
order-preservation in either direction. mg-6ad0 found none over 16 pairs on its instrument;
this repair finds none over 25 on a third, with the grid built from a different definition.

**WHAT SURVIVES.** Consequence 3's actual claim — *Brown does not make the identification* —
rests on the keyword census (ledger **B8**), which mg-6ad0 re-ran ligature-aware and
confirmed: all twelve keywords absent in both spellings. That claim is untouched. What is
lost is one supporting sentence, and it is lost in exactly the category the ticket named.
**And the correction runs toward the headline**: the located source's own worked example
turns out to be an instance of the very contact the document reports.

---

## 3. X3 — re-scoped to a hedge and a named open question, and no proof is manufactured

**What was wrong.** §3 row 3 books towers of algebras *"ADJACENT — axiom tested and failed"*,
and §2 item 5 books *"No tower"*, on Bergeron–Li's axiom (2) quoted from `arXiv:math/0612170`
**§3.1**, which is titled *"Tower of Algebras (Preserving unities)"*. The **same paper's
§3.6** is titled *"Tower of Algebras (not Preserving unities)"* and takes as input *"an
algebra injection not necessarily preserving unities"* — which is exactly what mg-af28
measured block concatenation to be: injective, multiplicative, **non-unital**, 64 of 64.
Unitality is the **only** clause the measurement found to fail.

**WHAT WAS CHECKED.** All four strings — §3.1's title, §3.6's title, §3.6's input clause,
and the axiom-(2) clause mg-af28 quotes — re-read from the PDF on a **third** extractor (one
that also decodes hex strings and kerning-split arrays), and searched **twice**: as the paper
spells them, and as a ligature-dropping reader renders them. mg-6ad0's X6 established that
the extractor used by both earlier instruments silently drops `fi`/`ff`, so a search in one
spelling is not a search. Result: **4 of 4 found in both spellings, 0 missing**.

**WHAT A FALSIFIER WOULD HAVE LOOKED LIKE.** Any of the four strings absent — in which case
X3 collapses and row 3's *"no"* stands as written. This is the cheapest possible falsifier
and it is the one that matters, because X3 is entirely a claim about what the cited paper
contains.

**WHAT IS NOT CLAIMED, AND WHY THE OUTPUT IS A QUESTION.** Bergeron–Li's conditions (3), (4)
and (5) — projectivity of `A_{m+n}` over `A_m ⊗ A_n`, the idempotent condition, and the
Mackey-type identity — are **untested by mg-af28, by mg-6ad0 and by this repair**. Testing
them is new mathematics, which every ticket in this lineage forbids. So:

> **OPEN QUESTION, NAMED AND NOT ANSWERED.** *Does `A_n = kF(P_1^{⊔n})` satisfy
> Bergeron–Li's §3.6 conditions for a tower of algebras not preserving unities?* Nothing in
> this repo bears on it in either direction.

Row 3 is now a **hedge, not a "no"** — the same repair mg-1953 correctly applied to row Q of
the landscape document, and mg-6ad0's own recommendation.

**AND THIS IS THE TICKET'S OWN DEFECT, INSIDE THE ENUMERATION FILED TO CURE IT.** mg-af28
exists because mg-d673 found a *"no"* licensed over a candidate space of **two**. Row 3's
*"no"* was licensed over a definition space of **one, in a paper containing two**. A cure
that reproduces the disease in its own apparatus is the finding, not a footnote — and the
operational consequence is that **enumerating the candidates is not enough; the definition
space inside each candidate has to be enumerated too.**

---

## 4. X4 — re-scoped to the level at which it has content

**What was wrong.** Three places said a version of *"Brown §4.3 reaches the Young graph and
no other differential poset"*: ledger **B4**, §2 item 2, and §3 row 10 (*"the lattice it
realises is the one Brown §4.3 provably cannot consume"*).

**At the level of whole differential posets it is true and empty.** Brown §4.3 needs a
**finite** distributive lattice. No differential poset is finite — they are locally finite
with infinitely many ranks, which is mg-af28's **own** §2 item 1 and the reason its T3 finds
0 of 405. So Brown consumes **no** differential poset at all, Young's lattice included. The
contact mg-af28 reports is therefore not with Young's lattice; it is with its finite
**intervals**.

**At that level it is false.** **WHAT WAS CHECKED**: the Young–Fibonacci lattice rebuilt
from the published neighbour rule (a third coding), under three controls that all PASS —
rank sizes are Fibonacci `1,1,2,3,5,8,13`; `DU − UD = I` **as an operator identity**, not
just on the diagonal, below the top rank, 0 violations; every interval `[0̂, w]` is a lattice,
0 failures. Then: **33** intervals with `rank(w) ≤ 6`, **5** non-distributive with smallest
witness `w = (2,2,1)` — T8's numbers and T8's witness, reproduced exactly — leaving **28**
that **are** finite distributive lattices. For each of the 28, `P` was built from the
join-irreducibles and `J(P) ≅` the interval verified: **28 reconstructions, 0 bad**.

**WHAT A FALSIFIER WOULD HAVE LOOKED LIKE.** 33 or 5 coming out differently — which would
make T8 itself wrong rather than its reading — or a distributive interval admitting no `P`,
which would make Birkhoff wrong. Neither happened. The reading that fails is the only thing
that fails.

**CONSEQUENCE FOR ROW 10.** The Okada monoid's branching graph has **the same index-set
contact** with this construction that mg-af28 headlines for Young's, on 28 of its 33 finite
intervals. Row 10 stays ADJACENT — it is a different monoid, aperiodic, on a labelled
Temperley–Lieb arc-diagram model — but the reason it gave is withdrawn.

**WHAT SURVIVES.** Young's lattice is still the only *distributive* 1-differential lattice
(Stanley 1988, cited by mg-af28 from a secondary source and read by nobody in this arc), and
every interval `[∅, λ]` of it is distributive — 30 of 30. That is a statement about **whole
lattices** and B4 keeps it.

---

## 5. THE BATTERY, RE-RUN UNMODIFIED

mg-4acd's discipline, applied here: **the battery that certified the corrections is the
auditor's, and it is re-run without a byte changed.**

* **`code/branching_audit_6ad0/run_all.sh`, re-run UNMODIFIED** — `git diff` over that
  directory is empty before the run — against the repaired tree, with `SKEW8=1`, the flag
  mg-6ad0 put its `n = 8` row behind. Every committed output comes back **byte-identical**
  except the one line the flag controls, and that line now prints what mg-6ad0 stated with
  provenance rather than computed: `8   12   360   16999   0.0007   0.0212`. Its four
  summary lines:

  ```
  SUMMARY a1_contact: ord 0, lat 0, f 0, chains 0 (all should be 0)
  SUMMARY a2_intervals: witness constructions bad 0; skew-path check bad 0
  SUMMARY a3_hypotheses: truncated-passers 1; YF intervals distributive 28 of 33
    (non-dist 5), reconstruction bad 0; non-idempotent moves 0; forced non-unital 64 of 64
  SUMMARY a4_algebra: B5 route bad [0,0,0,0,0] (20 skipped); Aut counterexamples 0
  ```

  **The auditor's directory is then restored to its committed state and is not touched by
  this commit** — the re-run is evidence, not an edit to another ticket's record. And the
  honest reading of it: mg-6ad0's instruments do not read the document, so re-running them
  cannot *fail* because of a documentation repair. What the re-run establishes is narrower
  and is still worth having — that the numbers this repair writes into the document
  (62, 149, 360; 33, 5, 28) are the auditor's own numbers, produced now, on unchanged code,
  rather than transcribed from a committed file.
* **`code/branching_af28/run_all.sh`**, re-run after the source fix. Everything outside T2
  is unchanged; T2 now prints two columns instead of one and `selftest.py` goes 27 → 31
  assertions, 0 failures. The straight column — 1, 1, 2, 3, 4, 6, 8, 12 — is **byte-identical
  to what it printed before**, which is the control that the fix did not disturb the number
  it was not about.
* **`code/branching_repair_41aa/check_doc.py`** reads the repaired document off disk and
  checks, per finding, both that the correction is present **and** that each struck sentence
  survives **exactly once and only inside the block quote that strikes it**. The negative
  half is the load-bearing half: a repair that adds a correction beside a false sentence and
  leaves the false sentence in force has not repaired anything. mg-aec7 had to fix an
  earlier check in this repo that compared a string against a `print` statement instead of
  against the document, which is why this one opens the file.

---

## 6. WHAT THIS REPAIR DELIBERATELY DOES NOT DO

mg-6ad0 raised **seven** items. This ticket was scoped to four. The other three are landed
**as a record only**, in the target document's new §9, with no successor ticket and with
pm-onethird owning the call:

* **X5** — ledger B6 and B7 are booked MEASURED with sample sizes (6 197 moves; 64 pairs)
  that cannot do any work; both answers are forced for every poset of every size by a
  two-line argument. Neither is *wrong*, and mg-af28 states both arguments in prose; the
  defect is in the ledger, which is what downstream readers quote.
* **X6** — B8's five present-word controls could not have caught B8's one documented failure
  mode, because 2 of the 12 absent keywords bear a ligature and 0 of the 5 controls does.
  **B8's conclusion survives** mg-6ad0's ligature-aware re-run. It is the warrant that is
  wrong. *(This repair's own quotation search is ligature-aware for exactly this reason —
  §3 above.)*
* **X7** — §2 item 5's clause *"which lands back at the classical antichain case"* drops the
  condition its own §1 row 2 states: `P_1` is arbitrary. The clause now stands only inside
  the struck text quoted at §2 item 5, and is flagged there and in §9.

**One further correction was made because landing X2 entailed it**: §8's *"Two elementary
one-line derivations"* is now *"Three"*, matching §5 item 5, which listed three all along —
and the third is the one that was false.

**THE TWO PATTERNS, RESTATED BECAUSE THEY OUTLIVE THESE FOUR FIXES.**

1. **The ticket's own defect recurred inside the enumeration meant to cure it.** mg-af28 was
   filed because a *"no"* had been licensed over a candidate space of two. X3 is a *"no"*
   licensed over one of two definitions **in the paper mg-af28 itself cited**. Enumerating
   candidates is not enough.
2. **Beyond-brief material holds the worst finding again.** X2 is one of the three
   elementary derivations mg-af28 flagged as its own and outside its brief. mg-3b51 recorded
   the first generation in this arc where beyond-brief material was correct; that exception
   did not hold. The unbriefed one-liners remain the least controlled part of every
   deliverable in this lineage — and the only reason X2 was cheap to find is that mg-af28
   **pre-filed it by name**.

---

## 7. PRE-FILED AUDIT OF *THIS* REPAIR — WHERE TO ATTACK IT

1. **Attack the converse direction of X1, which stops at `n ≤ 5`.** The exhaustive
   lattice-level search for a non-skew poset with `J(P)` an interval runs to `n = 5` (37
   non-skew classes, 4 520 isomorphism tests). At `n = 6` the ideal lattices reach 64
   elements and the search was not run; what covers `n = 6` is the join-irreducible argument,
   which is a **theorem** (Birkhoff) verified on every skew shape rather than a measurement
   over every poset. If Birkhoff's direction were used wrongly here, the `n = 6` row of R1b
   is a claim and not a measurement. **This is the weakest link in X1 and it is the first
   thing to attack.**
2. **Attack the box-growth control as too weak.** It shows the skew class count is stable
   for boxes `n`, `n+1`, `n+2` at `n ≤ 5`. It does not *prove* the trimming argument, and it
   was not run at `n = 6, 7, 8` where the counts that matter live. If the bound fails first
   at some larger `n`, 62 / 149 / 360 are lower bounds — and note that all three agree with
   mg-6ad0's independent enumeration, which uses **the same bound**, so the two instruments
   are independent in code and not in argument.
3. **Attack X3 by reading Bergeron–Li §3.6 properly.** mg-6ad0 pre-filed this and it is
   inherited unchanged: §3.6 defers its details to reference [10] (Li's thesis), which
   nobody in this arc has read. If §3.6's weakened conditions are unsatisfiable by anything
   of our shape for a reason visible in [10], X3 weakens to a bookkeeping complaint and row
   3's hedge should go back to a "no".
4. **Attack the Young–Fibonacci implementation, for the third time.** mg-af28 pre-filed it,
   mg-6ad0 declined to discharge it (its §10 item 2: *"an independent implementation is not
   an independent definition"*), and this repair is a **third implementation of the same
   published neighbour rule**, not a reading of Stanley (1988). Three agreeing
   implementations of one rule is consistency, not independence. **Nobody in this arc has
   read Stanley (1988).**
5. **Attack `check_doc.py`'s negative assertions as under-specified.** They pin four struck
   strings. A repair could satisfy all four and still leave a fifth false sentence standing
   somewhere the check does not look. The check is a control on *this* repair's four
   findings, not a proof that the document is now free of false sentences, and it should not
   be read as one.
6. **Attack the claim that the headline is untouched.** X1 widens the class of index sets
   this construction shares with the branching-graph programme by a factor of 10 to 30, and
   X2 puts Brown's own example inside it. Someone could argue that a headline whose
   *supporting* consequence moved that far should itself be restated. I think not — §0's
   headline sentence is about `[∅, λ]` and was correctly restricted — but the reading is
   mine.

---

## 8. CLAIM LEDGER

| # | claim | status | scope |
|---|---|---|---|
| **R1** | B2's *"exactly"* is false and the class is the skew cell posets | **MEASURED, both directions** | forward: all 405 poset classes to `n ≤ 6`, isomorphism **constructed** and checked on every pair of ideals, 0 bad, 107 interval posets against af28's 17. Converse: exhaustive to `n ≤ 5`, 4 700 interval comparisons, 0 hits; plus join-irreducible reconstruction on every skew shape to `n ≤ 6`, 0 bad |
| **R2** | the corrected fractions are 62/318, 149/2 045, 360/16 999 | **MEASURED** | third independent enumeration; agrees with mg-6ad0 exactly; af28's straight column 6, 8, 12 reproduced unchanged; box-growth control 0 movements at `n ≤ 5`; `n ≥ 7` denominators are **A000112, cited** |
| **R3** | §0 consequence 3's grid sentence is false; the grid **is** `[(q), (q+p, q)]` | **REFUTED BY CONSTRUCTION** | 25 pairs `p, q ≤ 5`, grid built as a **product of chains**, map verified pair by pair both directions, 0 bad; `|[μ,λ]| = (p+1)(q+1)` in every case |
| **R4** | the sentence's stated *reason* is true and insufficient | **MEASURED** | `C_p ⊔ C_q` is a straight cell poset in 0 of 25 cases, so it does rule out `[∅, λ]` — and only that |
| **R5** | Bergeron–Li contains a second, weaker tower definition at §3.6 that mg-af28 does not mention | **QUOTED** | 4 strings, third extractor, searched in both the printed and the ligature-dropped spelling, 4 of 4 found, 0 missing |
| **R6** | 28 of 33 finite Young–Fibonacci intervals are distributive, each `= J(P)` for an explicit `P` | **MEASURED** | third Young–Fibonacci implementation under three passing controls; T8's 33/5 and its witness `(2,2,1)` reproduced; 28 reconstructions, 0 bad |
| **R7** | the repaired document says what this repair says, and the struck sentences are struck | **MEASURED** | `check_doc.py` reads the file off disk: **29 checks, 0 failed** — 17 presence checks, **6 quoted-only checks** (each struck string occurs exactly once, in a block that also carries a strike marker; a struck string that has been quietly *deleted* fails too), and 6 checks against the regenerated `out_young.txt`. Matching is on whitespace-flattened blocks with block-quote markers removed, so a re-flow cannot fake a pass |
| **NOT CLAIMED** | that a tower of algebras exists over this family under §3.6 — that is the open question of §3, untested in either direction; that mg-6ad0's X5, X6 or X7 is answered; that mg-af28's headline is wrong in any respect; that Stanley (1988) has been read by anyone here; anything about `λ₂`, `Δ_AT`, the pricing, or publishability | | |

---

## 9. REPRODUCE

```
cd code/branching_repair_41aa && ./run_all.sh   # ~4 min, pure Python 3
cd code/branching_af28        && ./run_all.sh   # ~6 min, the repaired source
cd code/branching_audit_6ad0  && ./run_all.sh   # ~30 s, UNMODIFIED
```

Committed outputs: `out_selftest.txt` (36 assertions), `out_r1_exactly.txt`,
`out_r1b_skew8.txt`, `out_r2_grid.txt`, `out_r3_rescope.txt`, `out_check_doc.txt`.
`r3_rescope.py` is the only step needing network.

---

## 10. NOTE FOR pm-onethird

* **This repair edits `docs/OneThird-Branching-Graphs-Where-This-Lives.md` and
  `code/branching_af28/`, and adds one document and one instrument directory.** It does not
  touch `STATE.md` (no row exists for this work item), the landscape document, row Q, the
  semigroup note, `λ₂`, `Δ_AT` or the roadmap pricing.
* **X5, X6 and X7 are unrepaired and have no successor ticket.** They are recorded in the
  target document's §9 and in §6 above. Whether they are worth a ticket is your call; X5 and
  X6 are both about **warrant** rather than about a false finding, and X7 is one clause.
* **X3 re-opens a candidate; it does not close one.** Row 3 is now a hedge with a named open
  question attached. Answering it requires testing Bergeron–Li conditions (3), (4), (5),
  which is new mathematics and is forbidden by every ticket in this lineage — so if it is
  ever to be answered, that has to be commissioned deliberately.
* **The operational lesson, if only one is taken:** mg-af28 was filed to cure a negative
  licensed over too small a candidate space, and shipped a negative licensed over too small a
  **definition** space inside a candidate it did search. The next enumeration in this arc
  should enumerate the definitions as well as the programmes.
