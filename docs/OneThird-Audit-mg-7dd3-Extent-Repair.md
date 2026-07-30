# Independent audit — the mg-a4ef extent repair, and whether a printed extent is true

**Work item:** mg-7dd3. **Date:** 2026-07-30.
**Subject:** `106e121` (mg-a4ef), `docs/OneThird-Species-Hopf-Monoids-Repair-Extent.md`,
`code/species_repair_a4ef/`, and the state it leaves
`docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`, `code/species_7d75`,
`code/species_repair_6f61`, `code/species_remainder_f8fa` in.
**Audit repaired:** mg-73df, `ebecd89` — 0 BROKEN, 1 MAJOR, 4 MINOR.
**Instrument:** `code/species_audit_7dd3/`, `run_all.sh`, ~3 min, NO NETWORK, 46-assertion
self-test, **34 mutations each with its exit code predicted before the run**, sharing no code
with any instrument it audits.

---

## 0. THE VERDICT

**ALL FIVE OF mg-73df's FINDINGS ARE CLOSED AT SOURCE, AND I CHECKED THEM AT SOURCE RATHER
THAN THROUGH ANY CHECKER.** `D1 TOTAL BAD: 0` over seven claimed corrections in six files
plus the document, opening the bytes directly. X3 is gone from `t6_fock_and_record.py` and
from its committed output; the AM §17.5 quotation there reads `Π*` in both slots; §0's
headline box and `t4_one_operation.py:22` both read **anti**-isomorphic; the §14 limitation
box is down to one copy and §14.3's by-name answer still resolves against it; both docstrings
agree with their own runs. **Nothing retreated** — 15 of 15 survivals, 5 of 5 still struck,
**zero hedging words added**, and every verdict line in every tree unmoved. All four trees
regenerate **byte for byte**, and mg-73df's `c4_scope.py` / `c5_doc.py`, re-run unmodified,
reproduce mg-a4ef's committed `*_73df_after.txt` **byte for byte**.

**And the structural half — every checker now prints its own extent — is real and is worth
keeping.** It is also, as pm-onethird predicted when it strengthened this brief mid-flight,
the place the trust moved to. **So I measured the extent lines instead of reading them.**

| # | severity | what |
|---|---|---|
| **A1** | **BROKEN** *(by the strengthened brief's own rule)* | `s1_extent.py` prints *"SKIPPED, NAMED, so the exclusion cannot grow unseen — 5 file(s)"*. The real exclusion is **9**. Four `run_all.sh` sit inside the four trees the extent claims, are dropped by an extension filter that appears in **no** extent line and in **no** printed list, and a forbidden sentence planted in one exits **0** |
| **A2** | **BROKEN** *(same rule)* | `s2_seam.py`'s EXTENT paragraph names two limits — cross-document, and paraphrase below 45 % — and omits a third that removes **6 of 17 block quotes and 65 of 124 prose paragraphs from the comparison entirely**. An **exact, 100 %-identical** duplicate of a short block quote, inside the one document it sweeps, exits **0** and the run reports *"worst pair 5 %"* |
| **B1** | **MAJOR** | **The AM §17.5 quotation is struck in §4 and asserted, live and unmarked, in §0** — same document, 310 lines apart, since `83ac472`. It is on the one list. Every checker passes, and **every extent line is true**: the file is read, the statement is enumerated, the run is clean. The list stores the sentence **with its lead-in**, and §0's copy has a different one |
| **B2** | **MAJOR** | The document strikes **11** sentences. The *"one list"* — declared as the union of `check_doc.py`'s ten and `w3_scope.py`'s two, plus Y2 — carries **10**. The missing one is **mg-a61f's X8**, which is on **mg-73df's `c4_scope.py`**, the third list in the arc and the one mg-a4ef re-ran unmodified as its own corroboration |
| **C1** | MINOR | `check_doc.py`'s extent says *"over ONE FILE … It reads no code."* Measured by instrumenting `open`: it reads **two**, and the second carries five of its own assertions. Narrower than reality, which is the safe direction and still a false statement |
| **C2** | MINOR | mg-a4ef disclosed, beyond mg-73df's five, that `w3_scope.py` *"ended with `sys.exit(0)` unconditionally"* and fixed it. **`c5_doc.py` still does** — and its committed `out_c5_doc_73df_after.txt`, which mg-a4ef commits as its independent corroboration, ends **`C5 TOTAL BAD: 1`** with an exit code of **0**. 25 of the arc's 31 scripts exit 0 unconditionally |
| **C3** | MINOR | `s2_seam.py` calls S2c *"THE THREE STALENESS PATTERNS"* and its `PATTERNS` table has **2** rows; and `out_s2_seam.txt` carries a literal `56%%` from a `print` with no format operator. A count in prose that no artifact carries, in the file written to catch a count in prose that no artifact carries |

**0 mathematically false statements found.** Neither BROKEN finding makes any claim about
species, Hopf monoids or descent algebras untrue. They are graded BROKEN because the brief
that commissioned this audit fixed that grade in advance for exactly this: *"If any printed
extent is wider than what the code reads, that is a BROKEN finding and outranks everything
else in this audit."* I measured two, and I am applying the rule as written rather than
softening it because the consequence is bookkeeping. **B1 is the finding I would lead with if
the brief had not.**

---

## 1. WHAT I CHOSE TO AUDIT THAT NO LIST NAMED

The brief says its list is a floor. I picked three, and **all three findings above that are
not the brief's own came from them**:

1. **The document's own `~~strike~~` markers as the enumeration**, instead of any checker's
   table. It is the only list in this arc that cannot fall behind the document, because it
   **is** the document: a worker who strikes a sentence writes the `~~`; a worker who strikes
   a sentence and forgets the table row does not write the row. → **B2**, and the frame for
   **B1**.
2. **The reach of the exoneration rule, measured rather than argued.** Three workers have now
   narrowed *when* a hit is exonerated, each after a recorded false negative. Nobody has asked
   **how many independent clauses hold each hit down**. → the measurement in §5, and the M10
   result.
3. **The exit code, across every instrument in the arc** — not the two mg-a4ef names. → **C2**.

---

## 2. A1 — `s1_extent.py`'s NAMED EXCLUSION IS NOT THE EXCLUSION

`stricken_a4ef.py`'s comment is explicit about why the list is named one by one:

> *"an exclusion that is a short list is auditable, an exclusion that is a heuristic is a
> hole. `s1_extent.py` prints this list in its extent declaration so it cannot grow without a
> reader seeing it."*

And the run prints:

```
  SKIPPED, NAMED, so the exclusion cannot grow unseen -- 5 file(s):
      OUTCOMES.md
      PREDICTIONS.md
      out_c4_scope_73df_after.txt
      out_c5_doc_73df_after.txt
      stricken_a4ef.py
```

`tree_files()` filters on `.py/.txt/.md` **before** the named exclusion is consulted. So:

```
  SILENTLY OUTSIDE THE SCAN, NOT NAMED ANYWHERE:  code/species_7d75/run_all.sh
  SILENTLY OUTSIDE THE SCAN, NOT NAMED ANYWHERE:  code/species_repair_6f61/run_all.sh
  SILENTLY OUTSIDE THE SCAN, NOT NAMED ANYWHERE:  code/species_remainder_f8fa/run_all.sh
  SILENTLY OUTSIDE THE SCAN, NOT NAMED ANYWHERE:  code/species_repair_a4ef/run_all.sh
```

**Measured, not read off the source.** I ran `s1_extent.py` with `open` instrumented and
recorded every text read: 49 files, and per tree exactly the `.py/.txt/.md` less the five
named. Then the mutation the brief asks for, **inside the region the extent claims**:

| probe | exit | predicted |
|---|---|---|
| **M13** X3 planted in a new `.md` in `code/species_7d75` | **1** | 1 |
| **M12** X3 planted in `code/species_7d75/run_all.sh` | **0** | 0 |
| **M19** X3 planted in `code/species_audit_73df` (declared silent) | **0** | 0 |
| **M20** X3 planted in another `docs/` file (declared silent) | **0** | 0 |

M19 and M20 are the extent working: named silences, honoured. **M12 is not.**
`code/species_7d75` is one of the four trees the extent names by name; `run_all.sh` is inside
it; it is not one of the five files the run says it skipped; and nothing in the output reveals
that it was skipped. The extent, as printed, is **wider than what the code reads**.

**Two honest mitigations.** No `run_all.sh` in this repository contains a listed statement, so
nothing is in force there today. And the per-tree file counts the run prints (17 / 12 / 11 / 8)
are the counts it actually scanned, so a reader who compares them against `ls` can find the
gap. **Neither is the claim.** The claim is that the exclusion cannot grow unseen, and it
already has.

**The fix is two lines:** put the extension filter in `EXCLUDE`'s comment and print it in the
declaration — *"skipped by extension: everything not `.py`, `.txt`, `.md` — 4 file(s): …"*.

---

## 3. A2 — `s2_seam.py`'s SWEEP CANNOT SEE AN EXACT DUPLICATE

Its EXTENT paragraph, in full:

> *"S2a is a similarity sweep over ONE document and cannot see a duplicate spread across two
> documents, or one paraphrased below 45 %."*

Two limits named. The third is `MIN_CHARS = 300`, and it is not a threshold on similarity —
it removes passages from the comparison **altogether**:

| | passages | at or below 300 normalised chars | pairs never compared, at ANY similarity |
|---|---|---|---|
| block quotes | 17 | **6** | **81 of 136** |
| prose paragraphs | 124 | **65** | **2 475 of 4 186** |

The probe, both directions:

| probe | exit | predicted |
|---|---|---|
| **M17** an **exact** duplicate of a long block quote (1 495 chars) | **1**, reported at 100 % | 1 |
| **M16** an **exact** duplicate of a short block quote (139 chars) | **0**, run reports *"worst pair 5 %"* | 0 |
| **M5** restore `ebecd89`'s document — the real duplicate returns | **1**, reported at 56 % | 1 |
| **M8** delete the *"Eight things changed"* banner | **1** | 1 |
| **M9** rename the heading `### 14.2` to `### 14.5` | **1**, *"REFERS TO NOTHING"* + *"DANGLING"* | 1 |

**M16 is the finding.** A hundred-per-cent-identical duplicate, inside the one document the
extent says it sweeps, neither cross-document nor paraphrased — and the run says *"worst pair
5 %"*, which reads as *"the worst thing here is 5 % similar"* and is not what it means.

**The mitigation, stated:** the S2a line does print *"17 passage(s), 11 longer than 300
characters"*, so the filter is visible one paragraph above. The EXTENT sentence — the line
pm-onethird's strengthening identifies as the one everything now rests on — does not carry it.
**The fix is four words** in that sentence.

### And the sweep re-run, which the brief asked for by name

*"Re-run the duplicate sweep yourself over all 17 block quotes … verify no second pair sits
just under whatever threshold was used, and report the threshold."*

**Threshold: 45 %, deliberately the same as mg-a4ef's. Floor: 60 normalised characters, not
300 — 60 only removes Markdown `---` rules. So 17 of 17 block quotes and 92 of 124 prose
paragraphs are compared, against mg-a4ef's 11 and 59.** The whole ranked list down to 25 % is
in `out_d3_seam.txt`.

**Nothing sits just under.** The highest block-quote pair below 45 % is **38.4 %**, 6.6 points
under; the highest prose pair is **40.9 %**, 4.1 points under. **One pair is above 45 %** —
lines 472–473 against 480–481, at **52.8 %** — and I predicted zero, so that is a miss I keep.
I read it: **it is not a duplicate**, it is two different Aguiar–Mahajan quotations sharing
*"the algebra of symmetric functions"*. **It is also invisible to `s2_seam.py`**, both
passages being under 300 characters.

**Ratio was the wrong instrument and I changed it.** Two quotations of one book score 52.8 %
on vocabulary; §14's two boxes scored 55.7 %. What separates them is the **longest shared
verbatim run**: 6 words against **17**. Ranked that way, and with the same code run
unmodified against the document at `ebecd89` as a control, the sweep **finds mg-73df's pair
where it was** and finds no said-twice pair at HEAD that is not deliberate — four long runs,
all four inspected and named in `d3_seam.py`, three of them a passage quoting another back on
purpose.

**The fourth is B1.**

---

## 4. B1 — THE SENTENCE §4 STRIKES, ASSERTED IN §0

The lead-in test: for each of the document's 11 strikes, the longest run of consecutive tokens
it shares with the document **outside every strike**, as a fraction of the strike.

```
  strike 5   run 31  of 42  ( 74%)  line 169   *** THE CLAIM ITSELF, SAID AGAIN ***
      shared: ` k ̄ ( π ) ` is the algebra of symmetric functions in noncommuting
              variables and ` k ( π ) ` is the familiar hopf algebra of symmetric functions
```

Ten strikes share a lead-in and nothing more — 45 % or less, most under 30 %. **One shares
the claim.**

**§4, line 476, struck:**

> ~~*"Recall from Section 17.4 that `K̄(Π)` is the algebra of symmetric functions in
> noncommuting variables and `K(Π)` is the familiar Hopf algebra of symmetric functions"*~~.
> **The book's species is `Π*` in both slots.**

**§0, line 169, live, unstruck, unmarked:**

> Aguiar–Mahajan §17.5, quoting their own §17.4: *"`K̄(Π)` is the algebra of symmetric
> functions in noncommuting variables and `K(Π)` is the familiar Hopf algebra of symmetric
> functions."*

The document attributes to the book, as a direct quotation with a section citation, the exact
rendering it declares 310 lines later to be a misquotation — *"**mg-7d75 printed it wrong**"*.
Both have been in this file since **`83ac472`**, the commit that made the strike. **mg-6f61,
mg-f8fa, mg-73df and mg-a4ef have each passed over it.**

### Why every checker is clean, and why that is the point

* `check_doc.py` requires the STRICKEN string to occur once and be struck. It **does** — the
  stored string begins *"Recall from Section 17.4 that"* and §0's copy does not.
* `stricken_a4ef.py`'s X7 row stores the same sentence, and its source pattern is anchored on
  the same lead-in.
* `w3_scope.py` does not carry X7.
* `c4_scope.py`'s X6/X7 patterns **are** lead-in-free — and `c4_scope.py` scans code trees and
  never the document.

**No extent line is false here.** `check_doc.py` reads the whole document; the statement is on
the one list; `s1_extent.py` runs the list over the document and reports `S1 TOTAL BAD: 0`.
This is the arc's own shape one turn further out, and it is worth writing down plainly:

> **mg-6f61 fixed prose and left code. mg-f8fa widened what the checker READS. mg-a4ef
> widened what it LOOKS FOR and printed the extent. A statement can still be enumerated,
> inside a target that is read, inside a total that names its population — and be asserted
> somewhere the enumeration does not reach, because the enumeration is a SENTENCE and the
> assertion is a CLAIM. A list of sentences is not a list of claims.**

### Severity, and the honest half

**MAJOR, not BROKEN.** The mathematics is harmless and the document itself says why: AM
§17.4.1, *"Since `Π` and `Π*` are isomorphic"*, quoted at §4 and again at
`t6_fock_and_record.py:24`. This is the same grade mg-73df gave the same statement when it
was in force at source. **I did not re-fetch the PDF and I make no new claim about what the
book says** — only that §0 and §4 of this document disagree about it, and that §4 is the one
that carries the extraction.

**The fix is one line:** strike §0's copy, or replace it with §4's corrected form. It cannot
be caught by adding a row, because it is already a row.

---

## 5. B2 — THE ELEVENTH STRIKE IS ON NO LIST

The document strikes **11** sentences. `stricken_a4ef.py` has 11 rows, one of which (Y2) has
no struck sentence. **10 of 11.**

The one it lacks is §1's ~~*"as three independent agreements about the term"*~~ —
**mg-a61f's X8**, corrected by mg-6f61 to *"two sources using the term for `C(P)` and a third
that uses it for a single face"*.

| list | carries X8? |
|---|---|
| `check_doc.py`'s `STRICKEN` (10 rows) | no |
| `w3_scope.py`'s `FORBIDDEN` (2 rows) | no |
| `stricken_a4ef.py`'s `CORRECTIONS` — **"the ONE list"** (11 rows) | **no** |
| **mg-73df's `c4_scope.py`'s `CORRECTIONS`** (6 rows, covering 8 findings) | **yes** |

The union was taken over **two of the three lists that existed**, and the third is the one
mg-a4ef re-runs unmodified and commits as `out_c4_scope_73df_after.txt` — its independent
corroboration. Probed:

| probe | exit | predicted |
|---|---|---|
| **M14a/b/c** un-strike §1's X8 — restore it to live prose — then `check_doc.py` / `s1_extent.py` / `s2_seam.py` | **0 / 0 / 0** | 0 / 0 / 0 |
| **M15a** X8 asserted unmarked in `code/species_7d75`, `s1_extent.py` | **0** | 0 |
| **M15b** the same, `c4_scope.py` | **0**, printing `C4 TOTAL BAD: 1` | **1 — MISSED** |

**Nothing is in force today**, which is why this is MAJOR and not BROKEN: X8 is a coverage
hole, not a live falsehood. But mg-a4ef's own closing sentence is *"the next defect will be
one nobody has enumerated"*, and this one **was** enumerated — twice, by mg-a61f and by
mg-73df — and fell out of the union that was built to stop exactly that.

M15b is a prediction I missed and kept, and the miss became **C2**.

---

## 6. THE EXONERATION RULE, MEASURED — AND WHETHER THE MARKER IS LOAD-BEARING

Nobody in this arc has measured how many **independent clauses** hold each hit down. Over the
56 occurrences of a listed statement inside the declared extent:

```
      held by 1 clause(s):  23 occurrence(s)
      held by 2 clause(s):  20 occurrence(s)
      held by 3 clause(s):  13 occurrence(s)

      clause names-a-repair   fires on  19 of 56
      clause negates          fires on  30 of 56
      clause own-negation     fires on  31 of 56
      clause declared-table   fires on  22 of 56

  OVER-DETERMINED (2+ clauses): 33 of 56 = 59%
```

**Not a defect. A property nothing else prints, and it has a consequence:**

| probe | exit | predicted |
|---|---|---|
| **M10** delete the `CORRECTED AT SOURCE (mg-a4ef …)` line from `t6_fock_and_record.py`, leaving the struck sentence | **0** | **0** |
| **M11b** delete it **and** the three other clauses in the same window | **1** | 1 |

**The marker the repair points at is not what holds its number up.** I said in
`PREDICTIONS.md` that M10 was the one I was most likely to be wrong about. It held.

**And the same rule has now disarmed a checker a third time.** B1's occurrence at §0 line 169
sits five lines above *"(The fourth was added by the repair mg-6f61 …)"* — a note about a
**different** correction to the same section. Under `NAMES_A_REPAIR` that alone exonerates it.
This arc has recorded the identical mechanism twice before: `w3_scope.py`'s bare *"REPAIRED"*
disarmed by *"the error mg-1953 repaired"* four lines above, and `c4_scope.py`'s generic
negation disarmed by *"is not the framework this ticket is about"*. **A document that names
five ticket ids throughout cannot use proximity to a ticket id as evidence that a particular
sentence is withdrawn.** My own lead-in test therefore counts only a strike or an explicit
negation, and prints the ticket-id proximity rather than crediting it.

---

## 7. EACH PRINTED EXTENT, BOTH DIRECTIONS, AS THE BRIEF REQUIRES

| checker | its extent line says | inside → fires? | outside → silent? | verdict |
|---|---|---|---|---|
| `check_doc.py` | 10 statements × **1 file**, *"reads no code"* | **M18** un-strike §4's X7 → **exit 1** ✓ | **M2b** X3 in `species_7d75` → **exit 0** ✓ | **NARROWER than reality** — it opens two files (C1). Reads no code: measured true |
| `w3_scope.py` | X4, X5 + the character-ring rule, over **1 tree** | **M21** X4 in `species_7d75` → **exit 1** ✓ | **M22** X4 in `species_repair_6f61` → **exit 0** ✓ | **NARROWER** — W3c also enforces six positive readings in three named files, which the extent omits. Aimed at its two historical trees it is exact: **M23** `83ac472` → `FAIL (12 problems)`, exit 1; **M24** `ebecd89` → `PASS`, exit 0 |
| `s1_extent.py` | 11 statements × document + **4 trees**; 5 named skips | **M13** → **exit 1** ✓ | **M19/M20** → **exit 0** ✓ | **WIDER — A1.** M12, inside a claimed tree, exits 0 |
| `s2_seam.py` | one document; cannot see cross-document or < 45 % | **M17** → **exit 1** ✓ | — | **WIDER — A2.** M16, 100 % identical, exits 0 |

**Two of four are wider than what the code reads. Two are narrower.** Every statement count
is exact — no extent overstates **what** it looks for. Both overstatements are about **which
text is read**, which is the half §14.3 got right and the half A1/A2 get wrong.

---

## 8. WHAT REPRODUCES, AND WHAT DID NOT RETREAT

| tree | result |
|---|---|
| `code/species_7d75` | T1–T6 all `TOTAL BAD: 0`, 759 assertions — **seven committed outputs byte for byte**, `git status` clean |
| `code/species_repair_6f61` | `CHECK_DOC: PASS`, `R2 PREDICTIONS MISSED: 2 of 45`, 3 188 assertions — byte for byte |
| `code/species_remainder_f8fa` | `W3 SCOPE: PASS`, 2 114 assertions — byte for byte |
| `code/species_repair_a4ef` | `S1 TOTAL BAD: 0`, `S2 TOTAL BAD: 0`, 133 assertions — byte for byte |
| `c4_scope.py` / `c5_doc.py` re-run **unmodified** | reproduce mg-a4ef's `out_c4_scope_73df_after.txt` / `out_c5_doc_73df_after.txt` **byte for byte** |

**Over-correction: none.** **15 of 15** of mg-73df's required survivals present, restated here
as sentences rather than as `c5_doc.py`'s regexes so that a survival reworded into something
weaker would fail. **5 of 5** withdrawn sentences still only inside a strike or beside a named
repair. **Zero hedging words** in the 106 added lines, against a list of eleven. Every one of
the 20 removed lines has 6+ of its tokens still present at HEAD except one, which is the
stale *"an eighth defect, if there is one"* — so mg-a4ef's *"nothing the deleted copy said is
lost — it said less"* is **measured**, not taken. `T6/T5/T3 TOTAL BAD`, `CHECK_DOC`,
`R2 TOTAL BAD` and `W3 SCOPE` all unmoved.

The one narrowing in the diff — §0's banner from *"`w3_scope.py` is the checker for the
instrument"* to *"the checker for **two of those corrections**"* — is the correction mg-73df's
MAJOR demanded, not a retreat.

**And §14.3 still reads correctly against the copy that survived**, which the brief flagged as
the way a resolved duplicate moves rather than closes: §14.3 names §14.2, §14.2 exists once,
and the sentence §14.3 quotes back — *"outside every beam currently pointed at this
document"* — is in it. `s2_seam.py` checks the first two and **not** the third: it assigns
that sentence to a local `quoted` and **never uses it** (the identifier appears once in the
file). Had it been wired up it would have **failed**, because its stored form carries a hard
newline the document does not have. **The check that is missing is also the check that was
wrong.**

---

## 9. WHAT THIS AUDIT DID NOT DO

* **No PDF was fetched and no quotation battery re-run.** B1 is a disagreement between §0 and
  §4 of this document. I make **no** claim about what Aguiar–Mahajan says.
* **Solomon, Garsia–Reutenauer/Atkinson, AM, Saliola and Commins were not read.** Ledger S4
  and S5 are unchanged by this audit.
* **No mathematics was re-derived.** I did not rebuild a single algebra. The figures are
  mg-a61f's and mg-73df's and I neither extended nor re-checked them.
* **`Sol(S_n) ≇ Sol(S_n)^{op}` is still not established**, and Y2 remains wording.
* **My statement patterns are hand-written.** `selftest7dd3.py` exercises all 12 in both
  directions — fires on the withdrawn form, does **not** fire on the corrected one — but a
  claim phrased in a way none of them matches is a claim I did not look for. **That is B1's
  own mechanism, and I have no reason to believe I escaped it.**
* **`d6` reads 31 exit statements and RUNS two.** The other 29 are a static reading.
* **My whole-repository sweep reads `.py/.txt/.md/.sh` only** — 644 files. No PDF, no
  `.html`, no `.gz`.

---

## 10. PREDICTED FIRST, AND WHAT I GOT WRONG

`code/species_audit_7dd3/PREDICTIONS.md` was written **before any script here ran** and is
unedited. **72 predictions, 66 held, 6 missed, all kept as written** (`OUTCOMES.md`). Three are
worth naming:

* **D2** — I predicted no block-quote pair above 45 %. There is one, at **52.8 %**. It is not
  a duplicate, and I found that out by reading it rather than by moving the threshold.
* **G4 / M15b** — I predicted `c4_scope.py` would exit 1 on a statement its own list carries.
  It exits **0** while printing `C4 TOTAL BAD: 1`. **That miss is finding C2.**
* **C9** — my declared beyond-brief bet was a *percentage of exonerated ground*. I replaced the
  metric with a better one before measuring it, so the bet is unscored, and unscored counts as
  missed. The replacement is §6.

**And seven defects in this instrument, kept on the record.** Five are the same shape as
something this audit reports against the work it audits:

* **`d1_source.py` matched a wrapped sentence against raw bytes and failed on a sentence that
  is present** — the identical defect this audit had already predicted in `s2_seam.py`'s dead
  `quoted` variable, committed in the same session by the instrument that predicted it.
* **`d2_extent.py`'s lead-in test reported the CORRECTED line as the leak.** It extracted
  words with `[0-9a-z]+`, which collapses `K̄(Π)` and `K(Π*)` to the same token `k` — throwing
  away the star and the Greek letter, **which are the entire correction**.
* **`d4_survivals.py` tested "nothing was lost" against a list of phrases** and reported five
  re-wrapped lines as deletions. A list of phrases is the failure mode this audit is about; it
  was replaced by a measurement.
* **`d3_seam.py` reported "mg-af28 §2.6" as a dangling internal reference** — a checker firing
  on a convention instead of a defect, which is the false positive `s2_seam.py`'s own comment
  says its first version had.
* **A `print` with no format operator**, which is the defect I report in `out_s2_seam.txt`.
  Mine crashed; theirs is committed.

---

## 11. LEDGER

| # | claim | status |
|---|---|---|
| **D1** | All seven corrections mg-a4ef claims are true **at source**, read from the bytes and through no checker | **MEASURED**, 0 bad |
| **D4** | 15 of 15 survivals, 5 of 5 still struck, 0 hedges added, 6 of 6 verdict lines unmoved, every removed line accounted for | **MEASURED**, 0 bad |
| **REPRO** | four trees byte-identical; mg-73df's two instruments re-run unmodified reproduce mg-a4ef's committed `*_after.txt` byte for byte | **MEASURED** |
| **A1** | `s1_extent.py`'s named exclusion is 5; the real one is 9; a statement in the 4 unnamed files exits 0 | **BROKEN — MEASURED**, M12 vs M13 |
| **A2** | `s2_seam.py` cannot see an exact duplicate of a passage ≤ 300 chars; 6 of 17 block quotes and 65 of 124 paragraphs are never compared | **BROKEN — MEASURED**, M16 vs M17 |
| **B1** | the AM §17.5 quotation is struck in §4 and asserted live in §0, since `83ac472`, past four passes, inside a clean run of every checker | **MAJOR — MEASURED**, 31 of 42 tokens |
| **B2** | the document strikes 11; the one list carries 10; the missing one is mg-a61f's X8, on `c4_scope.py`'s list alone | **MAJOR — MEASURED**, M14/M15 |
| **C1** | `check_doc.py` says "ONE FILE" and opens two | **MINOR — MEASURED** by instrumenting `open` |
| **C2** | `c5_doc.py` prints `C5 TOTAL BAD: 1` and exits 0; 25 of 31 scripts in the arc exit 0 unconditionally | **MINOR — MEASURED**, 2 run |
| **C3** | S2c says "three named patterns" over a 2-row table; `out_s2_seam.txt` carries a literal `56%%` | **MINOR** |
| **M10** | the marker naming the repair is **not** load-bearing: deleting it leaves the total at 0; 59 % of hits are held by 2+ clauses | **MEASURED** |
| **NOT CLAIMED** | that anything here is mathematically false; that any PDF was read; that any range was extended; that my patterns are complete — B1's mechanism applies to them too | |

---

## 12. REPRODUCE

```
cd code/species_audit_7dd3 && ./run_all.sh    # ~3 min, pure Python 3, NO NETWORK
```

Outputs: `out_selftest.txt` (46 assertions), `out_d1_source.txt`, `out_d2_extent.txt`,
`out_d3_seam.txt`, `out_d4_survivals.txt`, `out_d5_mutations.txt`, `out_d6_exitcodes.txt`.
`TOTAL BAD` counts **findings against the audited work**, following `code/species_audit_73df`;
`D5 PREDICTIONS MISSED` is on its own line and is not folded in.

**Every one of the seven prints its own EXTENT under its total** — because the discipline
mg-a4ef introduced is right, and because A1 and A2 are what happens when it is followed
imprecisely. An extent line is not a formality; it is a claim, and it can be false in the one
direction that costs the reader everything.
