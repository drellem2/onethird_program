# Independent audit of mg-7870 / `e924590` — the content-digest repair of the working-tree control

**mg-babf**, 2026-07-30. Pre-filed at the same time as the ticket it audits. **Third control
in this lineage**: the first (`b68db5d`'s headline re-run) was blind because it pinned fixed
revisions; the second (`bf17716`) was blind because it tested substrings its own author
chose; this one replaces the mechanism with a SHA-256 per certified region and states its
coverage boundary.

Reproduce: `sh code/state_control_audit_babf/run_all.sh` (~3 min, most of it the pinned
battery run twice). Six outputs committed beside it — `out_claims.txt`, `out_regression.txt`,
`out_mutations.txt`, `out_statements.txt`, `out_preservation.txt` and the driver's own
`out_all.txt` — **all six reproduce byte-identically at this commit.** Step 3 exits 1
because it found silent misses; that is the finding, and the driver prints each step's code
rather than aborting on it.

`run_all.sh` steps 2, 3 and 5 **mutate `STATE.md` and `docs/state-history/README.md` in the
working tree** and restore them under a `finally` plus a sha256 check. They refuse to run if
either file is already dirty.

---

## VERDICT — OVERSTATED with 4 BROKEN, and the mechanism change itself is CONFIRMED

**The central move is right and it works.** mg-2216's finding closes: all five B2 mutations
that exited `0` against the substring control are now non-zero, established here by an
implementation written from their published descriptions that shares no code with mg-2216's
battery or with mg-7870's repair. All nine certified digests recompute exactly under my own
parser and locators. `COVERAGE.md`'s table agrees with the code in every id and every
character count. The pinned battery is byte-identical and still reproduces `out_audit.txt` at
96,291 bytes — **third verification** — "nothing was lost" is untouched, and all three record
corrections re-derive TRUE from source, including mg-2216's `:212`, which lands on the exact
line.

**The normalisation is not where the blind spot is, and I want to say that plainly because
it is where I was told to look.** It is one rule, it is stated in full, and it survives every
probe I could aim at it. U+00A0 appended at a certified region's *outer edge* **fires**,
while four ASCII spaces at the same edge are tolerated — that pair is the entire content of
the rule and it holds exactly as written. A single trailing space on an *interior* line
fires; one ASCII `-` → U+2010 fires; a zero-width space mid-word in the certified cell fires.
**I could not construct a mutation that the normalisation itself lets through.**

**The blind spot is one layer up, in the locator, and it is the larger surface.** A region is
"the maximal run of blockquote lines containing this marker", so its digest is a function of
the block's bytes and of **nothing else** — not its position, not the heading above it, not
whether it is inside a code fence or an HTML comment, not what the line before it says. Four
mutations leave every certified byte exactly as certified and exit `0`, including
**`b68db5d`'s own F1 correction block wrapped in an HTML comment, absent from every rendered
view of the README**. `COVERAGE.md`'s exclusion list names five things and position is not
among them; the marker-based locating is published only as a virtue.

**And 1,150 characters of the certified row are digested by nothing.** The digest covers the
row's *widest* field. Row `:135` has three, and the other two — 842 characters carrying the
row's own **GREEN · PROVEN** verdict, and 304 carrying its foundation-claims text and doc
pointer — are outside every digest. `COVERAGE.md`'s "Not covered, on purpose" section says
*"every row but `:135`"*, which says `:135` is covered. Inverting the headline verdict to
**RED · REFUTED** exits `0`.

| | |
|---|---|
| **B1** | **The digest is blind to position and context, and the coverage statement does not say so.** Four mutations that change no certified byte all exit `0`: a certified block moved verbatim under *"Appendix Z — superseded drafts … nothing below is in force"*; `b68db5d`'s F1 correction block wrapped in a ` ```text ` fence; the same block wrapped in an HTML comment; a *"RETRACTED … is void"* paragraph inserted immediately above a certified block. |
| **B2** | **A region the commit certifies is not digested.** `delta_control.py` names *"`STATE.md` row `:135`"* and `COVERAGE.md` excludes *"every row but `:135`"*, but only the row's widest field is digested — **1,150 of 9,028 raw characters (12.7%)**, including the row's own verdict, are covered by nothing. Two mutations exit `0`. |
| **B3** | **The statements and the control still disagree, and `COVERAGE.md` claims they don't.** *"the control was widened to match the wider statements rather than the statements narrowed to match the control"* — but S1 and S3 are universals, `COVERAGE.md`'s own five-bullet exclusion list is the enumeration of the mismatch, and **nine** of my fifteen mutations mutate the file and exit `0`. Neither of mg-2216's two offered repairs was applied to either statement. |
| **B4** | **"the certified set is now *eight* regions" is false — and it is inside a digested region.** The code has nine, `COVERAGE.md` says nine, the commit message says nine. `README.md:250` sits inside `readme.A1.7870`, which `delta_control.py` digests, so the wrong figure is now certified byte-for-byte. |

**Two MINOR, in the documented recovery path** — reported separately below because neither is
a certification defect.

**Beyond the brief: one item, and it is the highest-reach thing here.** S3 is not about this
instrument. It is `STATE.md`'s Appendix A item (4) — the **convention this cluster publishes
for every future instrument in this repo** — and it is a universal that its own worked
example does not satisfy. mg-2216 scored zero beyond the brief; this is one, and it is the
finding with the longest life.

---

## How this was built, and what it deliberately does not do

**It does not re-run mg-7870's negative control and read the result as evidence.** mg-7870
says so itself, in `negative_control.py`'s own docstring, and it is right.

**It does not re-run mg-2216's fourteen and read *that* as evidence either.** mg-7870 built
against them and re-ran them as its headline evidence, which makes them the repair's
**known-answer set**. A control tuned to a known-answer set and a control that works are the
same thing from inside, and that is the closed loop this lineage exists to open — twice
already. I read the fourteen **in order to avoid them**, exactly as mg-2216 read NC3 in order
to avoid it. Every mutation in `mutations_babf.py` is mine and none is one of the fourteen.

**The one exception is the regression, and it is not evidence about coverage.** mg-2216's
five B2 mutations are re-run because *"did the repair close its own stated finding?"* is a
question only they can answer. They are **re-implemented** in `regression_2216_b2.py` from
mg-2216's published prose descriptions — my own cell locator, my own sentence splitter, my
own filler construction — so agreement between the two implementations is information rather
than a copy. Where a description admits more than one implementation (the sentence swap), the
invariants it names are asserted in code: length preserved, token multiset preserved.

Three separate instruments, all mine, sharing only a harness: `claims_audit.py` parses
`CERTIFIED` out of `delta_control.py`'s **source** rather than importing it, so a mistake here
cannot be a mistake inherited from there.

---

## THE REGRESSION — mg-2216's B2 closes, all five

`out_regression.txt`. Every one of these exited `0` against the pre-repair instrument.

| | class | mutation | exit | verdict |
|---|---|---|---|---|
| **M01** | single-character | *"every ridge in 1 or **2** facets"* → *"1 or **3**"* | **2** | CAUGHT |
| **M02** | length-preserving | *"the proof is **sound**"* → *"**bogus**"* | **2** | CAUGHT |
| **M03** | whitespace-only | the spaces in `**The mathematics.**` → U+00A0 | **2** | CAUGHT |
| **M05** | reordering | two adjacent sentences swapped; length **and** token multiset preserved, asserted in code | **2** | CAUGHT |
| **M06** | bulk-but-quiet | last **3,000 of 7,876** characters → `x`, `**` count preserved | **2** | CAUGHT |

**5 of 5 CAUGHT, 0 silent.** Each fires `[MOVED] cell.tree` and nothing else, which is the
right shape: the digest is what catches them, not a length constant and not a substring.
M06 additionally does not disturb `**`-parity by construction, so the whole-file invariant in
section 6 cannot be what fired.

**B2 CLOSES.** A repair that does not close its own stated finding is not a repair; this one
does.

I did not re-implement the other three of mg-2216's eight (M09/M10/M11, all README-region
mutations). Their mechanism is the README region digest, which my B09, B11 and B12 exercise
independently and which fires in all three. I also confirmed `out_battery_2216_rerun.txt`
**reproduces byte-identically** when mg-2216's battery is re-run — that is a check on
mg-7870's reported evidence, not a substitute for my own.

---

## MY BATTERY — 15 mutations, none of them mg-2216's

`out_mutations.txt`. Expectations declared before the run. "tolerate" is used **only** where
`COVERAGE.md` says in words that the thing is out of scope, so a `tolerate` row that exits 0
is a boundary *confirmed*, not a pass.

| | class | mutation | exit | |
|---|---|---|---|---|
| **B01** | certified-row | row `:135` field 1: `**GREEN · PROVEN, all finite posets` → `**RED · REFUTED, no finite poset` | **0** | **SILENT MISS** |
| **B02** | certified-row | row `:135` field 2: *"foundation claims (1)–(3) supply"* → *"FABRICATED claims (1)–(9) supply"* | **0** | **SILENT MISS** |
| **B03** | certified-row | text appended **after** the row's closing pipe | 0 | tolerated (boundary) |
| **B04** | locator-position | the mg-7870 correction block **moved verbatim** under *"Appendix Z — superseded drafts … nothing below is in force"* | **0** | **SILENT MISS** |
| **B05** | locator-context | `b68db5d`'s F1 block wrapped in a ` ```text ` fence — renders as a code sample | **0** | **SILENT MISS** |
| **B06** | locator-context | the same block wrapped in an **HTML comment** — absent from the rendered page | **0** | **SILENT MISS** |
| **B07** | locator-context | *"RETRACTED 2026-08-01 … is void"* inserted immediately above a certified block | **0** | **SILENT MISS** |
| **B09** | normalisation | **U+00A0** appended at the F2 block's **outer edge** | 2 | CAUGHT |
| **B10** | normalisation | four **ASCII spaces** at the same edge | 0 | tolerated (the stated tolerance) |
| **B11** | normalisation | one trailing space on an **interior** line | 2 | CAUGHT |
| **B12** | normalisation | one ASCII `-` → **U+2010 HYPHEN**, visually identical | 2 | CAUGHT |
| **B13** | normalisation | **U+200B** mid-word in `pseudomanifold` in the certified cell | 2 | CAUGHT |
| **B14** | stated-boundary | the index table's own `7,705` → `9,705` | 0 | tolerated (stated) |
| **B15** | stated-boundary | `STATE.md` Appendix A's convention sentence **inverted** | 0 | tolerated (stated) |
| **B16** | parser | the certified row indented by **one space** | 1 | CAUGHT (FAIL) |

**11 expected-catch: 5 CAUGHT, 6 SILENT. 4 expected-tolerate, 0 noisy.**

**B09 against B10 is the normalisation's whole claim, measured.** Same edge, same block, one
character each: the ASCII space is tolerated and the U+00A0 fires. `COVERAGE.md` says
*"U+00A0 is not whitespace to this rule — Python's `str.strip()` would eat it,
`.strip(" \t\r\n")` does not"*, and that is exactly what happens. The temptation in a repair
like this is to reach for `str.strip()` or NFKC; either would have swallowed mg-2216's M03,
and neither was reached for. **This is the best thing in the commit.**

### B1 — the digest is blind to position and context

B04–B07 change **no certified byte**. B05 and B06 are the sharp ones: `b68db5d`'s F1
correction block — one of the three blocks `delta_control.py`'s own header names as what it
certifies — can be turned into a code sample or removed from the rendered document entirely,
and the control reports `PASS — every check above read the working tree and every one held,
including 9 region digests`.

This is the blind spot the brief predicted, one layer up from where it predicted it. The
normalisation decides what is insignificant *within* a region; **the locator decides what the
region is**, and it decides that position and surroundings are insignificant. Only the first
of those two decisions is stated.

`COVERAGE.md` presents the marker-based locating as a virtue — *"so the instrument survives
commits that insert lines above them"* — which is true and is a real design win against
line-pinning. The flip side is not written down anywhere, and it is what a reader needs.

### B2 — a certified region that is not digested

Row `:135` is 9,028 raw characters in three fields of 842 / 304 / 7,878 (plus the four
boundary pipes: 842 + 304 + 7,878 + 4 = 9,028). `widest(cells)` takes the third, so
**1,150** characters — the two other fields and the pipes — are digested by nothing. The two
fields hold the row's verdict on its own proof — the string
`**GREEN · PROVEN, all finite posets · first proof-carried generalisation in the arc` — and
its doc pointer.

`COVERAGE.md`'s **table** is precise: *"row `mg-276d`'s content cell"*. Its **exclusion
list** is not: *"The rest of `STATE.md`'s ledger — every row but `:135`"*. So the document
contradicts itself, and the sentence that is wrong is the one in the section a reader goes to
in order to find out what is **not** covered. `delta_control.py`'s header repeats the error:
*"WHAT IT CERTIFIES … `STATE.md` row `:135`, the F1 repair (one line, +173 characters)"* —
the line named as a whole.

**In fairness to the scope:** `b68db5d` changed only field 3 of that row, so the *delta* this
instrument was written for is fully digested. The defect is in the statement, not in the
choice of region — and the statement is the thing the next auditor will trust instead of
re-deriving. *"A region certified but not digested is the whole defect returning"*, and this
is the mild form of it: certified in prose, not in the table, not in fact.

---

## THE COVERAGE STATEMENT, AUDITED AS A CLAIM

`out_claims.txt`. 21 claims checked against the code and the files, never against mg-7870's
summary of either: **17 TRUE, 4 FALSE, 0 UNTESTED.**

**TRUE, and several of them are load-bearing:**

- All **nine** digests recompute exactly under my own extractors (C3.1).
- `COVERAGE.md`'s table lists exactly the ids in `CERTIFIED`, in order, and every character
  count matches the code's constant (C2.1, C2.2).
- *"On this material `.strip()` and `.strip(" \t\r\n")` agree"* — checked on **all nine**
  regions, 0 differ, so the rule change genuinely moved no published number (C4.1). The cell
  is 7,876 stripped / 7,878 raw as published (C4.2).
- Every README region **starts at its block head**, so hollowing a block while keeping its
  header changes the digest — mg-2216's B1, closed (C5.1).
- **No marker keys on a figure its own region certifies** (C5.2). This is mg-7870's own NC5
  finding, self-found and self-fixed, and it holds. *Necessary, not sufficient*: a marker
  could still key on a non-numeric claim, which is not mechanically decidable, and I say so
  rather than counting the check as a clean pass.
- `out_battery_2216_rerun.txt`'s summary is as quoted, `out_control.txt`'s exit codes are as
  quoted (clean 0, NC1–NC3 → 1, NC4–NC6 → 2), and `code/state_control_audit_2216/out_mutations.txt`
  is **byte-identical to its pre-repair state** — genuinely frozen, as claimed (C7.1–C7.3).

**FALSE:** C1.3 (the "eight"), C6.1 (the certified row), C6.2 (position/context absent from
the exclusion list), C8.2 (the docstring repeating C6.1).

### B4 — "the certified set is now **eight** regions"

`docs/state-history/README.md:250`. The code has nine; `COVERAGE.md` says nine; the commit
message says *"Nine regions"* and enumerates all nine correctly. The sentence goes on to
enumerate what makes the set wider — *"the A1 and A3 correction blocks and the index note are
digested too"* — and the count simply does not include this repair's own correction block,
which is `readme.A1.7870`, which **is** digested, and which **is the block the sentence is
written in**.

It is a small number in a large repair. It is filed because of *where* it is: inside a
digested region, so the digest now holds a false figure in place byte-for-byte, and because
this arc's recurring defect is precisely *the commit's arithmetic about itself*.

---

## THE STATEMENTS AND THE CONTROL — B3

`out_statements.txt`. mg-2216's closing instruction named two acceptable repairs: **fix the
control, or narrow the statements.** Either makes them agree.

| | where | statement | still exceeded by |
|---|---|---|---|
| **S1** | mg-2da3's ticket, item 1 | *"must fail when the file is mutated"* | B01 B02 B03 B04 B05 B06 B07 B14 B15 — **nine** mutations of the two files, all exit `0` |
| **S2** | README A1 block *(a digested region)* | *"never green about a delta that is no longer the delta it was written for"* | B06 — see the reading note below |
| **S3** | `STATE.md` Appendix A, item (4) | *"ships with a negative control … showing it exits non-zero when that tree is mutated"* | B01 B02 B04 B05 B06 B07 |
| **S4** | `COVERAGE.md` | *"the control was widened to match the wider statements rather than the statements narrowed to match the control"* | its own page |

**S1 and S3 are universals.** A bounded control cannot be widened to match a universal, and
`COVERAGE.md`'s five-bullet *"Not covered, on purpose"* section is the written enumeration of
the gap. Neither statement was touched by the repair — verified: both are byte-present at
`6b1eacf` and at `e924590`.

**S4 is false on its own page and needs no mutation to show it.** The control **was**
strengthened, substantially and correctly. It was not widened *to match the wider
statements*, because it cannot be.

**S2 — I give both readings and do not adjudicate.** Under *"the delta = the bytes `b68db5d`
wrote"*, B06 leaves them in the file and the sentence survives. Under *"the delta = what
`b68db5d` added to the document"*, B06 removes the F1 correction block from every rendered
view while the control stays green, and the sentence is falsified. I cannot settle which
reading the author intended from the text. Reading (b) is the one a reader of the README takes
and the one under which the sentence is doing work; I record that opinion as an opinion.

**What the repair *did* add, so the finding is not overstated:** two bounded-coverage
statements that did not exist before — *"the goal is bounded, stated coverage, not total
coverage"* in the README correction block **directly beneath S2**, and *"The goal is not a
control that catches everything"* as `COVERAGE.md`'s opening line. These are real and they
matter. What they are not is a narrowing **of** S1, S2 or S3 — a general disclaimer added
nearby does not strike an absolute sentence still published as written, and **S1 and S3 are
not in either of the two documents the disclaimers were added to.**

### Beyond the brief: S3 is the one with the longest reach

S1 is about one ticket. S2 is about one README block. **S3 is the convention** — `STATE.md`'s
Appendix A, *"added 2026-07-30, from mg-bd41 A1"*, published as a rule for every future
instrument in this repo, and `code/state_landing_control_2da3/` is named in it as the
**worked example, both halves**. The rule requires a negative control *"showing it exits
non-zero when that tree is mutated"*. Its own worked example exits `0` on six of my fifteen
mutations of that tree.

The convention is right in substance and its mechanical test — *"does any script open the
working tree or resolve `HEAD`?"* — is excellent and checks out (0 of the 6 pinned scripts
do). The universal quantifier in item (4) is what needs the same bounded-coverage language
mg-7870 wrote for `COVERAGE.md`. This is beyond the four targets I was given and is filed as
such.

---

## PRESERVATION — all three hold, nothing was swapped for anything

`out_preservation.txt`. **11 checks, 11 HOLD, 0 BROKEN.** This is the axis on which a
replace-the-mechanism repair usually trades one defect for another. It did not.

- **P1** — `code/state_audit_6a2f/` is byte-identical across the repair **and** against
  `main`; it exits 0 and reproduces `out_audit.txt` at **96,291 bytes exactly**. Third
  verification in this lineage.
- **P1.4** — and I re-established mg-bd41's A1 from a **fourth** independent mutation: with
  `b68db5d`'s F1 correction block HTML-commented out, the pinned battery emits the identical
  96,291 bytes. mg-bd41 gutted the file, mg-2216 damaged one cell, I removed a block from a
  different file; same verdict every time. The finding does not depend on the shape of the
  damage. **Nothing here asks the battery to change** — pinning is a feature there and the
  repair correctly leaves it alone.
- **P2** — *"nothing was lost"* is not re-opened: the repair's diff over `STATE.md` and the
  state-history README has **0 removed lines** (pure insertion, +37), it touches only the
  control's own directory and the README, and the control-vs-content framing sentence is
  present and unaltered. The framing is correct and I have nothing to add to it.
- **P3** — the three record corrections, re-derived from source, not read off a predecessor's
  document: **A3** the `%p` chain gives `57f962f ← 97cb533 ← 60f4dac`, so *"two commits before
  mg-34bf's parent"* was off by one; **A2** mg-6a2f's document names the source at
  **`:212`** — mg-2216 published `:212` and it lands exactly — and `db08b4c:STATE.md` is
  **327 lines with 0** occurrences of `mg-a3d4`; **A1** as above, plus the mechanical check.

---

## MINOR — the documented recovery path

Neither is a certification defect. Both are in `--emit-baseline`, which is what
`delta_control.py` and `COVERAGE.md` both tell a reader to reach for when a digest fires.

- **N1 — it is not pasteable, though both documents say to paste it.** `emit_baseline`'s own
  docstring says *"Print a pasteable `CERTIFIED` table"* and the header says *"when you paste
  the result in, say in the commit message WHICH COMMIT MOVED IT"*. It emits
  `("cell.tree", ...)  # STATE.md:135` — a literal ellipsis in place of the label, kind and
  marker — so the output is a two-line note per region, not a row that can be pasted into a
  six-tuple table.
- **N2 — it crashes on exactly the tree it exists for.** `extract` raises `LookupError` and
  `emit_baseline` does not catch it, so if **any one** region is unlocatable the command
  exits 1 with a traceback and emits **nothing at all**, including for the eight regions that
  are fine. Measured: with the F1 block deleted, `--emit-baseline` exits 1 on
  `LookupError: marker matched 0 lines, need exactly 1`.

---

## What I could not establish

Stated so the next auditor does not read silence as coverage.

- **Which reading of S2 the author intended.** Both are given above; neither is asserted.
- **Whether B03 renders.** Text after the row's closing pipe is outside every field the
  parser returns — outside the digests, outside the three-column check, outside the
  whole-file `**`-parity tally, which is taken over between-pipe fragments only. GFM drops
  cells past the header's arity, so it most likely does **not** render, which is why it is
  filed as a parser boundary and **not** as damage. I did not render the file to confirm.
- **The marker rule beyond arithmetic.** C5.2 tests that no marker keys on a *figure* its
  region certifies. A marker keyed on a non-numeric claim would be self-defeating in the same
  way and is not mechanically decidable; I did not audit the seven markers by hand for that.
- **Non-UTF-8 or CRLF trees.** `N` removes CR from the two ends only, so a wholesale
  CRLF↔LF conversion would fire on every region. I did not test it and do not claim it.
- **`negative_control.py`'s internals.** I read its reported exit codes out of
  `out_control.txt` and confirmed the file reproduces. I did not audit what NC1–NC6 actually
  mutate, because mg-7870 is right that it is not evidence and I did not want to spend the
  budget treating it as though it were.
- **Whether `readme.A1.7870`'s digest constant was computed before or after the "eight"
  sentence was written.** It matches the tree now; the ordering inside the commit is not
  recoverable and does not change the finding.

---

## Summary

| | |
|---|---|
| mg-2216's B2 regression | **CLOSES — 5 of 5**, re-implemented independently |
| the normalisation | **holds in every direction I could probe** — 5 probes, 5 correct |
| the nine digests | **recompute exactly** under my own extractors |
| `COVERAGE.md`'s table | **exact** — ids and character counts |
| my battery | 15 mutations, **6 SILENT MISSES**, 0 noisy |
| coverage claims | 21 checked: **17 TRUE, 4 FALSE** |
| statements vs control | **4 statements, 4 still disagree, 0 narrowed** |
| preservation | **11 of 11 HOLD** |
| beyond the brief | **1** — S3, the convention in Appendix A |

**The mechanism change was the right call and it is confirmed.** What is BROKEN is the
boundary around it: one discard that is not stated (position and context), one region
certified in prose that is not digested (the certified row's other two fields), a claim that
the statements now agree when they still do not, and a wrong region count sitting inside a
region the instrument certifies.

**A digest closes the question "does it catch mutation X?" for everything inside a region.
It does not close it for what a region is.** That is the boundary the fourth control in this
lineage will need to state, if there is one.
