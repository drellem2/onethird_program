# The repair of mg-73df — X3 at source, the seam resolved, and the extent stated

**Work item:** mg-a4ef. **Date:** 2026-07-30.
**Target:** `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`, `code/species_7d75`,
`code/species_repair_6f61`, `code/species_remainder_f8fa`.
**Audit repaired:** mg-73df, `ebecd89`,
`docs/OneThird-Audit-mg-73df-Species-Repair-Final-State.md` — **0 BROKEN, 1 MAJOR, 4 MINOR.**
**Instrument:** `code/species_repair_a4ef/`, `run_all.sh`, ~5 s, no network, 133-assertion
self-test.

---

## 0. WHAT WAS DONE

**All five of mg-73df's findings are closed, and the MAJOR is closed AT SOURCE rather than in
the prose about the source.** One statement it did not name is closed with them, found by
running the whole list over the whole tree rather than the named list over the named places.

| # | mg-73df | what mg-a4ef did |
|---|---|---|
| **Y1** | **MAJOR** — X3 and the AM §17.5 quotation corrected in the document and **still asserted in `t6_fock_and_record.py`**, X3 also in a committed output inside a run ending `T6 TOTAL BAD: 0`; `w3_scope.py` cannot see either | **corrected at source**, both, and the output regenerated. `stricken_a4ef.py` is now the **union** of `check_doc.py`'s ten `STRICKEN` rows and `w3_scope.py`'s two `FORBIDDEN` rows; `s1_extent.py` runs it over **the document and all four code trees**; **and each checker's extent is printed in its own output** |
| **Y2** | MINOR — §0's headline box says the left side **is** Solomon's descent algebra where five other places, and AM Thm 10.13 as §0 itself quotes it, say **anti**-isomorphic | corrected in §0 **and at source in `t4_one_operation.py`**, which carried the same reading and which nothing on any list named. Added to the one list as a row, so it cannot recur unenforced |
| **Y3** | MINOR — §14's limitation box appears twice, 56 % similar, disagreeing; one copy calls an eight-item banner *"the five items"* | **resolved to one copy.** §14.2 survives — it traces the list to **two** sources and carries the evidence. The miscount left with the copy that made it |
| **Y4** | MINOR — §14.2 calls mg-f8fa's filing *"shelved"*; §14.3 eleven lines below is its record | *"a second, shelved filing"* → *"a second filing of the same audit"*, with the correction stated in place |
| **Y5** | MINOR — `w3_scope.py` says **6** problems where its evidence says **12**; `r2_columns.py` says **40** cells where it prints **45** | both docstrings corrected against their own committed runs |

**Nothing is withdrawn and no figure changes.** Every `TOTAL BAD` in every tree is what it was.

---

## 1. THE MAJOR: THE SCOPE WAS WIDENED AND THE LIST WAS NOT

mg-f8fa's §14.3 stated its own fix: *"one line of scope: the checker must take the code
directory as a target too."* It widened the **target**. It did not widen the **list**.

* `check_doc.py` declares **ten** stricken sentences and enforces them **in one file**.
* `w3_scope.py` enforces **two** of them over a **directory**, and reports `PASS, 0 problems`.
* **X3 and the AM §17.5 quotation were in force in `code/species_7d75` the whole time**, and
  X3 was in a **committed output**, inside a run ending `T6 TOTAL BAD: 0` — which is the
  property §14.3 itself identifies as why the previous three went unnoticed: *"a passing
  checker is read as coverage."*

> **A checker has two scopes — what it reads and what it looks for — and fixing one reads as
> fixing both.** Between the two checkers every file was covered and every statement was
> covered, and **no statement was covered in every file.**

**This is the third generation of the same defect on this document, and the second time it
recurred inside the repair that fixed it.** mg-6f61 fixed prose and left code; mg-f8fa fixed
that code; the correction mg-f8fa itself centres on was still live at source.

### The two halves of the fix

**One list.** `code/species_repair_a4ef/stricken_a4ef.py` holds the union, each row carrying
both the exact document sentence — matched against the document, where it must survive only
inside its `~~strike~~` — and the source patterns, matched against every tree, where it must
not be asserted at all. `s1_extent.py` runs it over all of them and prints a matrix of
statements against targets.

**And the extent, printed.** This is the half nobody's brief asked for, and it is the half that
makes the next `TOTAL BAD: 0` mean something:

| checker | statements | targets |
|---|---|---|
| `check_doc.py` (mg-6f61) | 10 of 11 | **1 file** — the document, no code |
| `w3_scope.py` (mg-f8fa) | **2 of 11** | 1 tree — `code/species_7d75` |
| `s1_extent.py` (mg-a4ef) | **11 of 11** | the document **+ 4 code trees** |

Both older checkers now print that statement in their own output, so a `PASS` from either
carries its own limit. `s1_extent.py`'s `TOTAL BAD: 0` is followed by what it is silent
about: the other documents in `docs/`, the two audit trees, and any statement not on the list.

### Demonstrated, with four controls

| control | result |
|---|---|
| **(a)** the detector at `ebecd89`, the state mg-73df audited | **4 still asserted**, naming X3 at `out_t6_fock_and_record.txt:66` and `t6_fock_and_record.py:149` — against **0** now |
| **(b)** at `83ac472`, before mg-f8fa | **9 still asserted**, catching X4 and X5, the two `w3_scope` covers — so the control tests the detector, not the coverage claim |
| **(c)** a statement injected into a scratch copy | 0 → **1**. Not reporting a constant |
| **(d)** three phrases that have actually disarmed a checker in this arc | **none disarms it**, and a marker naming the repair still does exonerate |

**And independently, from an instrument this repair did not write:** mg-73df's own
`c4_scope.py`, re-run **unmodified**, goes from **4 still-asserted to 0**, with its own
`83ac472` control unchanged at 8. Committed as
`code/species_repair_a4ef/out_c4_scope_73df_after.txt`.

---

## 2. Y2, AND THE ROW IT ADDED TO THE LIST

§0's headline box read *"the left side **is** Solomon's descent algebra"*. §2.2, §9 rows 3 and
8, ledger **S2**, and **AM Thm 10.13 as §0 itself quotes it thirty lines below** all say
**anti**-isomorphic, and T3d measures the plain reading to fail by **472** structure constants
at `n = 5`. It is now *"anti-isomorphic to"*, with the correction marked in place.

**It was also at source**, in `code/species_7d75/t4_one_operation.py:22`, unmarked. No brief
named that occurrence and no checker's list carried it — it was found by scanning the whole
list across the whole tree, which is the same act that found the MAJOR. It is corrected there
too, and **Y2 is now a row of the one list**, because a correction that is not on the list is a
correction that recurs.

mg-73df tried to refute Y2 outright — if the two algebras were both isomorphic and
anti-isomorphic then `dim{x ∈ J : Jx = 0} = dim{x ∈ J : xJ = 0}` — and computed them equal at
every `n ≤ 5`. **Inconclusive, not negative.** This repair does not change that: Y2 is
**wording**, `Sol(S_n) ≇ Sol(S_n)^{op}` is **not** established here, and no mathematics is
added.

---

## 3. THE SEAM

Two workers edited one document. Each was complete against its own brief. **Nobody's brief
covered the seam**, and it carried two of the five findings.

§14's limitation box appeared **twice**, at 56 % similarity, in versions that disagreed: one
called mg-6f61's list *"the five items in the banner at the top"* where the banner says
**eight** and traced it to mg-a61f alone; the other traced it to two sources and carried the
evidence. **§14.3, added by the second worker, answers §14.2 by name** — so the stale copy was
load-bearing for a later section, and sat twelve lines above a paragraph reporting the eighth
defect **found** while still saying *"an eighth defect, if there is one"*.

**Resolved to one copy: §14.2 survives**, because it is the version that traces two sources
and carries the evidence. The five-versus-eight left with the copy that made it. §14.3 needed
**no edit** — the sentence it quotes back is in §14.2, not in the deleted copy. §14.2's
*"a second, **shelved** filing"* is now *"a second filing of the same audit"*, with the
correction stated in place: that filing was dispatched as mg-f8fa, it ran, and §14.3 is its
record.

**A duplicate sweep is now part of the instrument** (`s2_seam.py`), deliberately more general
than the pair it was written for: block quotes **and** prose paragraphs, at a **45 %**
threshold set below the 56 % that was found, plus cross-reference resolution and three named
staleness patterns. The worst remaining block-quote pair is **5 %**.

### One thing this repair did NOT do, and why

mg-73df's `c5_doc.py` requires that **no** passage says *"an eighth defect, if there is one"*
once §14.3 reports it found. **One still does — §14.2 — and it should.** That is the
prediction mg-6f61 made before mg-f8fa ran, and §14.3 answers it by name. Editing it now would
be tidying a prediction after its outcome is known, which is the one thing this arc's standard
forbids.

So `c5_doc.py`'s check is **over-broad**: it could only be cleared by rewriting a prediction,
and it flagged two passages before this repair for the same reason it flags one after.
`s2_seam.py` replaces it with the precise rule — **every occurrence must lie inside §14.2, the
passage a later section resolves by name** — which passes now and would still have caught the
deleted copy, which sat outside the exchange. The finding is reported here rather than made to
go away.

---

## 4. Y5, AND ONE MORE THAT WAS NOT ON THE LIST

`w3_scope.py`'s docstring said it *"reported 6 problems"* against the pre-repair tree; its own
committed `out_w3_scope_before.txt` says `FAIL (12 problems)`, and so do §14.3 and ledger
**S14**. `r2_columns.py`'s docstring said *"all 40 cells"*; its own run prints `45 cells` and
`MISSED: 2 of 45`. **The document and the outputs were right; only the docstrings were wrong.**
Both corrected, against their own runs, and neither change alters a committed output.

**Beyond mg-73df's five, and disclosed rather than folded in:** `w3_scope.py` ended with
`sys.exit(0)` **unconditionally**, so a run printing `W3 SCOPE: FAIL (12 problems)` still
exited 0. That is the same shape as the finding the file exists to carry — a clean signal that
does not mean what it reads as. It now exits 1 on failure. `check_doc.py` already did.

---

## 5. WHAT REPRODUCES

| tree | result |
|---|---|
| `code/species_7d75` | re-run: **T1–T6 all `TOTAL BAD: 0`**, 759-assertion self-test. **Exactly one committed output changed** — `out_t6_fock_and_record.txt`, which is the correction. The other six regenerate **byte for byte** |
| `code/species_repair_6f61` | `CHECK_DOC: PASS (0 problems)`, `R1/R2/R3 TOTAL BAD: 0`, `R2 PREDICTIONS MISSED: 2 of 45`, 3 188 assertions. Only `out_check_doc.txt` changed, and only by the extent block |
| `code/species_remainder_f8fa` | `W3 SCOPE: PASS`, 2 114 assertions; **12 problems** still against `83ac472`, unchanged |
| `code/species_audit_a61f`, re-run **unmodified** | **456 328 assertions, `A4 TOTAL BAD: 1` (which is X1) and 0 elsewhere — byte-identical**, `git status` clean |
| `code/species_repair_a4ef` | `S1 TOTAL BAD: 0`, `S2 TOTAL BAD: 0`, 133 assertions |

**`code/species_audit_73df` will NOT regenerate byte-identically, on purpose.** Its committed
outputs are the record of what that audit found when it looked, and overwriting them with
`no near-duplicate block quotes` would delete the evidence for the ticket this repair closes.
The post-repair run is committed **separately**, as
`code/species_repair_a4ef/out_c4_scope_73df_after.txt` and `out_c5_doc_73df_after.txt` —
the same convention `w3_scope.py` uses with `out_w3_scope_before.txt`.

---

## 6. PREDICTED FIRST, AND FIVE MISSED

`code/species_repair_a4ef/PREDICTIONS.md` was written **before any edit and before any run**
and has not been touched since. `OUTCOMES.md` scores it: **22 predictions, 17 held, 5 missed,
and the misses are kept as written.**

The one I care about is **P3**, my single declared beyond-brief bet: that the stricken
inequality direction `y(i) ≤ y(j)` was still live at source in `code/species_7d75`. **It is
not there at all.** The same reasoning produced **P7**, which was right and found Y2 at source
where no list named it. The method was sound; that particular bet lost. The value was not in
guessing the location — it was in running the whole list over the whole tree.

**And five defects in this repair's own instrument, kept on the record.** Two are worth
naming here:

* **The instrument written to catch `t6_fock_and_record.py:149` missed
  `t6_fock_and_record.py:149`.** Flattening whitespace does not cross the `")` and `print("`
  that sit between *"axiom with"* and *"0 failures"* — which is why mg-73df's own detector had
  to reduce X3 from a sentence to a co-occurrence of *"axiom"* with *"4399"* within three
  lines. Fixed by masking the scaffolding with spaces of equal length.
* **Then the mask blanked the newlines too**, costing one line of the count per mask, so the
  first hit was reported **thirty lines above where it is**. A detector with a wrong line
  number is a detector a reader cannot check.

The first version also reported **19 hits of which 14 were false positives** — including
`r1_smallest.py`, the file whose whole purpose is to **refute** X1 — because it re-derived the
exoneration rule from scratch instead of adopting the one **two** previous workers had each
narrowed after a recorded false negative. That is its own small instance of this document's
recurring shape, and it is in `OUTCOMES.md`.

---

## 7. WHAT THIS REPAIR DID NOT DO

* **No PDF was re-fetched and no quotation battery re-run.** The AM §17.5 correction at source
  copies the text §4 of the document already carries, extracted by mg-a61f; **no new claim is
  made about what the book says.**
* **Solomon, Garsia–Reutenauer/Atkinson, AM 2020/2017, Saliola and Commins were not read**, so
  ledger **S4** and **S5** are unchanged by this repair, as they were by mg-73df and mg-f8fa.
* **`Sol(S_n) ≇ Sol(S_n)^{op}` is not established.** Y2 is corrected as **wording**; mg-73df's
  refutation attempt was inconclusive at `n ≤ 5` and this repair adds nothing to it.
* **No range was extended and no figure recomputed.** Every number in the document is the
  number that was there.
* **The list is still a list.** It is the union of two lists, and mg-73df's own finding is that
  a union of lists is still a list. **The next defect will be one nobody has enumerated.** The
  only structural improvement offered here is that a correction now has **one** place to be
  recorded instead of two, and that every checker states what it ranged over.
