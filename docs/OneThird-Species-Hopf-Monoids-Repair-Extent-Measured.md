# The printed extent, measured in both directions — and the retraction moved to where it is read

**Work item:** mg-d633. **Date:** 2026-07-30.
**Repairs:** mg-7dd3 (`798afb7`, `docs/OneThird-Audit-mg-7dd3-Extent-Repair.md`) findings
**A1**, **A2**, **B1** and **C1**, against mg-a4ef (`106e121`).
**Instrument:** `code/species_extent_d633/`, `run_all.sh`, ~2 min, NO NETWORK, 50-assertion
self-test, **28 probes, exit codes predicted before the run**.

---

## 0. WHAT CHANGED

**Two printed extents were wider than what the code read. Both are closed by WIDENING THE
CODE. One was narrower than what the code read, and that one is closed by NARROWING THE CLAIM.
All three are then probed from inside and from outside, per checker.** And **the AM §17.5
quotation, struck in §4 and asserted live in §0 since `83ac472`, is fixed at §0** — where a
reader meets it — with a checker added that no per-section checker could have been.

| # | finding | checker | repair | which kind |
|---|---|---|---|---|
| **A1** | *"the exclusion cannot grow unseen — 5 file(s)"*; the real exclusion was **9** | `s1_extent.py` | every regular file in every tree is read; undecodable files printed by name | **CODE WIDENED** |
| **A1** | the same extension filter, over one tree, under *"over ONE tree"* | `w3_scope.py` | the same | **CODE WIDENED** |
| **A2** | two limits named, `MIN_CHARS = 300` omitted — 6 of 17 block quotes and 65 of 124 paragraphs compared **at no similarity at all** | `s2_seam.py` | a second pass compares every passage over 60 normalised chars at 90 %; what neither pass compares is printed one passage per line | **CODE WIDENED** |
| **C1** | *"over ONE FILE … It reads no code."* It reads two | `check_doc.py` | the extent names both files and what the second is read for | **CLAIM NARROWED** |
| **B1** | the AM §17.5 quotation struck in §4, live in §0, 310 lines apart | the document | fixed **at §0**; `e2_crosssection.py` added | — |
| C3 | *"THE THREE STALENESS PATTERNS"* over a 2-row table; a literal `56%%` in the output | `s2_seam.py` | the header **formats** `len(PATTERNS)`; the `%%` is fixed | claim derived, not restated |

**Why widening rather than narrowing, for A1 and A2.** Both could have been closed by a
sentence — *"skipped by extension: …"*, *"and nothing under 300 characters"*. That would have
made the extent lines true and left the holes exactly where they were: a forbidden sentence in
a `run_all.sh` still exits 0, an exact duplicate of a short quote still exits 0. The claim was
the thing that was false, but the claim was also the thing worth keeping.

**Why narrowing, for C1.** `check_doc.py` reads a second file for five assertions and does not
need to read any more than that. There was nothing to widen; the sentence was simply wrong.

---

## 1. THE MEASUREMENT, PER CHECKER, IN BOTH DIRECTIONS

`code/species_extent_d633/e3_bothways.py`. Each probe plants **one** mutation in a fresh
sandbox copy of `docs/` and six code trees, runs **one** unmodified checker, and compares the
exit code with a prediction written before the run.

| checker | baseline | INSIDE the claimed extent → must FIRE | OUTSIDE it → must stay SILENT |
|---|---|---|---|
| `check_doc.py` | clean | **2 / 2** | **2 / 2** |
| `w3_scope.py` | clean | **2 / 2** | **2 / 2** |
| `s1_extent.py` | clean | **3 / 3** | **3 / 3** |
| `s2_seam.py` | clean | **3 / 3** | **2 / 2** |
| `e2_crosssection.py` | clean | **2 / 2** | **2 / 2** |

The two probes that carry the findings:

* **P9** — X3 planted in `code/species_7d75/run_all.sh`, a file inside a tree the extent names.
  **Exit 1.** This is mg-7dd3's **M12**, which exited **0** and is the whole of A1.
* **P14b** — an exact duplicate of the 139-character block quote, inside the one document the
  extent says it sweeps. **Exit 1**, reported at 100 %. This is mg-7dd3's **M16**, which exited
  **0** while the run reported *"worst pair 5 %"*, and is the whole of A2.

And the probes that show the extent is not merely wide:

* **P12** — X3 in `code/species_audit_73df`, a tree the extent declares silent: **exit 0**.
* **P13** — X3 in `code/species_repair_a4ef/OUTCOMES.md`, one of the five **named** exclusions:
  **exit 0**.
* **P16 / P17** — a passage of ≤ 60 characters, and a Markdown table row, duplicated exactly:
  **exit 0** for both. Those are declared silences and they are now printed, one passage per
  line, rather than summarised by a threshold no sentence carried.

**And `e1_extents.py` measures the extent lines themselves**, by running each checker under an
instrumented `open` and comparing what it read with what it printed: **20 comparisons, 0
false**. Every file count each run prints is the count it read.

> **A structural remedy is not done when it ships. It is done when its single point has been
> measured in both directions.** mg-a4ef's remedy was right — a total that names its population
> cannot turn *"not examined"* into *"examined and clean"*. It also made one line per checker
> load-bearing for everything else, and **half of that line was false one audit later**. A
> printed extent that has only been read is not a measured one.

---

## 2. B1 — THE SENTENCE §4 STRIKES, ASSERTED IN §0

§4 strikes the AM §17.5 quotation — *"mg-7d75 printed it wrong"*, *"the book's species is `Π*`
in both slots"*. §0 carried the same claim, live, unmarked, as a direct quotation with a
section citation, **310 lines above**, from `83ac472` until now. mg-6f61, mg-f8fa, mg-73df and
mg-a4ef each passed over it. **Every checker was green and every extent line was true**: the
file is read, the statement is on the one list, `S1 TOTAL BAD` is 0. `check_doc.py` requires
the struck string to occur only inside a strike, and it did — the stored string carries its
lead-in and §0's copy had a different one.

**It is fixed at §0.** Not by a pointer added at §4, not by a note in a repair document: at the
paragraph where a reader meets the claim. §0 now states that the rendering is a misquotation,
gives the book's species, and sends the reader to §4 for the extraction. **A reader of §0 has
no reason to reach §4** — which is exactly why the strike was invisible to the population
holding the wrong belief.

### The check, and why a per-section checker could not have caught it

`code/species_extent_d633/e2_crosssection.py`: **for every span the document strikes through,
the longest run of consecutive tokens it shares with the same document outside every
strike.** A run of ≥ 8
tokens that is ≥ 50 % of the strike is the claim said again. Nothing in it knows what any
particular claim is, so it cannot fall behind the document: a worker who strikes a sentence
writes the `~~`, and that is the whole input. **A list of sentences is not a list of claims.**

Measured over **100 markdown files** under `docs/` and `code/` — 12 carry a strike, 30 strikes
measured — **0 stand un-struck.** In the target document the other strikes share 45 % or less
with the rest of the file; one shared **74 %**, and that was B1.

**Exoneration is narrower here than in the arc's other three rules, and the narrowing is
measured rather than argued.** An occurrence stands only if **the paragraph carrying it says
the claim does not hold**, or if it sits in a fenced block quoting a checker's own table of
stricken strings. A ticket id nearby is not enough — E2's control (c) shows that `kerna4ef.py`'s
±6-line rule is **disarmed by an unrelated `mg-6f61` five lines below §0's misquotation**, so
the one occurrence in this repository that had to fire would not have. That is the **fourth**
recorded instance in this arc of a marker disarming a checker by accident.

**For each retraction, every other occurrence of the claim must be struck or removed too**, and
that is now checked across sections instead of within them.

---

## 3. INDEPENDENT CORROBORATION — mg-7dd3's OWN INSTRUMENT, RE-RUN UNMODIFIED

Committed as `out_d1_7dd3_after.txt`, `out_d2_7dd3_after.txt`, `out_d3_7dd3_after.txt`,
`out_d5_7dd3_after.txt`.

* **`d1_source.py`: `D1 TOTAL BAD: 0`.** Every correction mg-a4ef made is still at source, every
  extent line still exists, and nothing this repair touched retreated. **The three D1e checks
  match frozen strings** (`"EXTENT OF THAT VERDICT (added mg-a4ef)"`, `'\nprint("EXTENT.'`), and
  the rewritten extent paragraphs were written to **keep those anchors intact** — `check_doc.py`
  makes the same demand of mg-a61f's battery in its own C3, and a repair that silently breaks an
  auditor's anchors has made itself unauditable.
* **`d2_extent.py`, D2f — the lead-in test, which is where B1 was found: every one of the 11
  strikes now reads *"lead-in only"*.** Strike 5 has gone from **run 31 of 42 (74 %)** to **run
  11 of 42 (26 %)**. B1 is closed in the instrument that found it.
* **`d5_mutations.py`: M12 now exits 1** where the audit measured 0 (**A1**), and **M25 — an
  exact duplicate of a 98-character prose paragraph — now exits 1** where the audit measured 0
  (**A2**). mg-7dd3's own file reports both as *"PREDICTION MISSED"*, which is what a closed
  finding looks like in a frozen probe.

**Four assertions in that instrument still read `*** FAILS ***`, and none of them is a
regression. Named, because a re-run that is not 0 has to be accounted for line by line:**

1. *"the only file in the tree it does not read is `run_all.sh`"* — **asserts the defect is
   present.** It no longer is.
2. *"the declared exclusion is the whole exclusion"* — d2 recomputes the exclusion by
   **re-applying a hardcoded copy of the extension filter** rather than measuring what the
   checker opens, so it lists the four `run_all.sh` regardless of the repair. Its own D2b
   section, which *does* measure, reports 18 / 18, 13 / 13, 12 / 12 and 9 of 14 with the five
   named — the repair, correctly.
3. *"it opens exactly ONE file, as 'ONE FILE' reads"* — tests the **code** (file count == 1)
   where C1 was a defect in the **sentence**. The sentence now names both files; the count is
   still two, and d2's own note beside it says that is the safe direction.
4. *"every sentence the document strikes is on the one list"* — mg-7dd3's **B2**, the eleventh
   strike (mg-a61f's X8) missing from `stricken_a4ef.py`. **Not repaired here and not claimed
   to be**: it is a coverage hole in a list, not an extent that lies, and nothing is in force
   at source because of it.

`d3_seam.py` likewise reports 5, none of them a new repetition. One is a frozen count — *"the
document has 17 block quotes"*, and it now has 19, this repair having added two. Three are its
`INSPECTED_REPEATS` table, which is keyed on **line numbers** (`(119, 431)`, `(165, 475)`,
`(900, 1007)`, `(868, 1065)`) and which this repair moved. The fifth is `s2_seam.py`'s S2c
count, which d3 asserts should become **three rows**; it was closed the other way, by making the
header format `len(PATTERNS)` so that a count in prose and the artifact carrying it cannot
disagree again. **One of those four keys is B1 itself** — *"NOT deliberate — this is
the AM 17.5 quotation asserted in §0 and struck in §4"* — and that pair no longer appears in
d3's sweep at all. Its *"seen by `s2_seam.py`?"* column also restates a 300-character floor that
`s2_seam.py` no longer applies alone.

---

## 4. WHAT THIS REPAIR DID NOT DO

* **B2 is open.** The eleventh strike is on no list. Named above, unrepaired, and it is the
  finding a successor should take next.
* **C2 is open.** 25 of the arc's 31 scripts still end in an unconditional `sys.exit(0)`, and
  `c5_doc.py`'s committed output still ends `C5 TOTAL BAD: 1` with an exit code of 0. Every
  script in `code/species_extent_d633` exits on its own total; nothing else was touched.
* **A cross-DOCUMENT retraction is still invisible.** `e2_crosssection.py` compares a strike only
  against its own document. A claim struck here and asserted in another file is invisible to
  every checker in this repository. That is the next hole, named rather than closed.
* **E2 matches verbatim runs.** A claim restated in different words is invisible to it.
* **The probes are a sample.** An extent probed at two or three points is not an extent verified
  at every point, and the choice of points is the author's. They are listed by name in
  `out_e3_bothways.txt`.
* **No mathematics was touched.** Nothing in §§1–13 about species, Hopf monoids or descent
  algebras is changed, strengthened or hedged by any of this.

## 5. PREDICTIONS

`code/species_extent_d633/PREDICTIONS.md` predates every probe. **1 of 21 was wrong and is kept
as written**: P11 predicted that a statement planted at the end of
`code/species_repair_a4ef/run_all.sh` would make `s1_extent.py` fire, and it exited 0 — not
because the file is unread (it is; E1 measures that) but because line 18 of that file says
*"mg-73df's MAJOR"* about something else and the ±6-line exoneration rule cleared the hit. **The
probe was measuring the exoneration rule while claiming to measure the extent.** It was split in
two rather than retuned to pass. `OUTCOMES.md` also keeps **four defects found in this
instrument itself**, two of which inverted a result before they were caught — including a
control that restored a false belief *beside its own correction* and reported the detector
broken, which is B1 said backwards.
