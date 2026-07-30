# Independent audit — mg-34bf / `57f962f`: the `STATE.md` ledger restructure

**Auditor:** mg-6a2f. **Subject:** `57f962f` (mg-34bf), against its parent `97cb533`.
`STATE.md` is byte-identical at `97cb533` and at `60f4dac`, the base commit mg-34bf names,
so there is exactly one baseline and no ambiguity about what "before" means.

**Instruments:** `code/state_audit_6a2f/` (`sh code/state_audit_6a2f/run_all.sh`, ~5 s, no
dataset, no enumeration; full output committed as `out_audit.txt`). Every script was written
from scratch for this audit. **None of them imports, reads or executes anything under
`code/state_restructure_34bf/`** — not the relocation spec, not the builder's splitter, and
not the author's completeness checker. The brief forbade using the author's checker as the
evidence, and it was not used.

---

## VERDICT

**On the one question that matters — WAS ANYTHING LOST? — NO. Nothing was lost. Established
by construction, twice, with instruments that do not share the author's.** Both of my
measurements independently reproduce the author's headline figures exactly.

**Composite verdict: OVERSTATED, 2 BROKEN.** Both BROKEN items are in the landing's
description of *itself*. **Zero defects in relocated content, zero words lost, zero
citations dropped, zero files touched beyond the brief.** The relocation is clean; the
account of it is not.

**And separately, as the dispatch requires: `STATE.md` still contains the paragraph a
previous audit called BROKEN.** See §B1. It was not lost, it was not relocated, and mg-34bf
was right not to relocate it. Its finding is still **OPEN**. Those are two findings, not
one, and the clean completeness verdict above does not cover it.

| | |
|---|---|
| words lost | **0** of 11,625 (per-cell, reachable-from-row) |
| baseline token occurrences unaccounted | **0** of 30,388 (whole file, order-free) |
| citations dropped | **0** of 64 distinct / 156 occurrences |
| rows renumbered / added / removed | **0** (58 → 58, row keys byte-identical) |
| Appendix A | **byte-identical** |
| files beyond the brief | **0** |
| BROKEN | **2**, both in self-description |
| MINOR | **4** |

---

## 1. WAS ANYTHING LOST? Measured, not sampled, and measured twice

Two independent constructions, because a single method has a single blind spot.

### 1a. Whole-file token multiset (order-free, global)

Every whitespace-token *occurrence* in the baseline `STATE.md` must be matched by an
occurrence somewhere in {after `STATE.md`} ∪ {`docs/state-history/*.md`}. This is coarse —
it ignores order — but it is **global**: it would catch a drop on any of the 367 lines, not
only the ten the commit says it touched.

```
baseline token occurrences : 30,388 (8,357 distinct)
after-corpus occurrences   : 35,360 (8,911 distinct)
RESULT: 0 baseline token occurrences unaccounted for.
```

### 1b. Per-cell maximal-run decomposition, constrained to reachable-from-row

For each changed cell, greedily decompose the baseline cell's token sequence into maximal
contiguous runs that still occur, **in order**, in the union of (the after version of *that*
cell) ∪ (the history files *that cell links to*). A run of length 0 is a token unreachable
from its own row.

```
line  89 col 1 |   250 words ->    3 runs, shortest  42, LOST 0   ledger-row-11-L4.md
line 114 col 2 |   117 words ->    3 runs, shortest  11, LOST 0   attempt-mg-c47a-drop.md
line 124 col 2 |   220 words ->    3 runs, shortest  20, LOST 0   attempt-mg-48ab.md
line 130 col 2 |   426 words ->    5 runs, shortest  10, LOST 0   attempt-mg-210d.md
line 131 col 2 |   772 words ->    9 runs, shortest  10, LOST 0   attempt-mg-a58f.md
line 132 col 2 |  1396 words ->   21 runs, shortest   8, LOST 0   attempt-mg-88bd.md
line 133 col 2 |  2151 words ->   21 runs, shortest  11, LOST 0   attempt-mg-63e3.md
line 134 col 2 |  1631 words ->   23 runs, shortest  15, LOST 0   attempt-mg-3af9.md
line 135 col 2 |  2155 words ->   13 runs, shortest  27, LOST 0   attempt-mg-276d.md
line 136 col 2 |  2507 words ->   24 runs, shortest  11, LOST 0   attempt-mg-a3d4.md

TOTAL: 10 cells, 11,625 words, 125 maximal runs, 0 unaccounted, shortest run 8
mg-34bf reported: 10 cells, 11,625 words, 125 maximal runs, 0 unaccounted, shortest run 8
```

**An independently written checker reproduces all four headline numbers exactly.** That is
the strongest form this claim can take: the same measurement arrived at twice, from two
codebases that share no line. The completeness claim is **CONFIRMED**, not accepted.

Read it precisely, as the author himself asks: it establishes that no word was dropped, no
wording inside a run was altered, and everything counted as kept is reachable by a reader
who starts at the row. It says nothing about additions or judgement. §3 and §4 cover those.

### 1c. The mechanism sentences — the passages whose loss would be hardest to notice

The brief named three by name and asked me to hunt for them specifically, because nothing
downstream cites them.

| the mechanism record | baseline site | after |
|---|---|---|
| joins are joins and **joins suppress `λ₂`** — *"Theorem L's link becomes a genuine join, which suppresses `λ₂` by `p/(p+q+1) < 1`"* | `:241` (Appendix A) + `:136` (a restructured row) | present, verbatim, both sites |
| *"the pipeline **SURVIVED the control it was missing**"* | `:286` (Appendix A) | present, verbatim |
| *"coverage went from **ZERO to ONE ABSORBABLE SIGN GAUGE**"* | `:135` (a restructured row) + `:284` | present, verbatim, both sites |

All three survive. Occurrence counts are conserved exactly (`suppress` 4 → 4; `pipeline` 1 →
1; `control it was missing` 1 → 1; `absorbable` 11 → 9 + 2; `ABSORBABLE` 4 → 4).

**One correction to the record, which is the ticket's and not mg-34bf's.** The ticket calls
these three *"the most valuable content **in those cells**"*. Two of the three were never in
a ledger cell — they are in **Appendix A**, which was out of scope and is byte-identical, so
they were never at risk. Only the sign-gauge one was in a restructured cell (`:135`), and it
**stayed in the row**. mg-34bf's claim that the three *"are all present and none was
touched"* is true, and truer than it needed to be.

Relocated mechanism notes generally (rule (d)) are covered by §1b: 0 unaccounted, all
reachable from their row.

### 1d. Citations

Every `mg-`id, document filename, commit sha, `§`-reference and arXiv number appearing in a
baseline changed cell must reappear at ≥ its baseline multiplicity in the row or a file the
row links to. **64 distinct references, 156 occurrences, 0 short.**

---

## 2. DID MEANING CHANGE WHILE MOVING? No.

### 2a. No relocated passage was paraphrased

Decomposing the *other* direction — after-corpus against baseline — every token run in the
history files that does not occur in the baseline is new text. The inserted spans in the
history files are **section headings and per-file preambles only**. Inside the relocated
passages themselves there are no insertions, which is the mechanical form of "not
paraphrased".

### 2b. Nothing was cut mid-sentence

The claim is verifiable directly rather than through run boundaries: **137 relocated
paragraphs, all whole-sentence-bounded** (open on a sentence start, close on terminal
punctuation). The two flagged by my start-of-paragraph regex open on an `mg-`id in lowercase
(`mg-210d Thm 2.4 builds it…`, `mg-5630's absorbability test…`) and are fine.

My run-boundary test flagged 11 apparent mid-sentence cuts. **All 11 are artifacts of my own
greedy decomposition**, not defects: they occur where a new pointer headline shares a word
with the passage it points at, e.g. the row now reads `**Four corrections landed against
prior text…**` while the history file carries `**Four corrections:** (1) …`, so the greedy
matcher swallows `**Four` into the kept run. Reported here so the number is not mistaken for
a finding by a later reader of my output.

### 2c. No bold span was split; the table is intact

`**` parity is even in every one of the ten rewritten cells and in every history file and
every `H`-section. No cell contains an unescaped `|`. The column-count vector of the whole
file is identical before and after.

### 2d. References re-pointed by relocation — one degraded, one false alarm

This is the failure mode token completeness is blind to by construction: the tokens are all
there and they now point somewhere else.

- **MINOR (F6).** `docs/state-history/attempt-mg-276d.md` carries *"⭐ THAT PROBE WAS RUN AND
  IS AUDITED — mg-a3d4, audited mg-86a3, landed by mg-a806; **see the next row**."* Inside a
  standalone file there is no next row. Recoverable — the target is named three ways in the
  same clause — but the deixis is dangling. It is the only one of the 11 relocated deictic
  phrases that does not resolve; the rest are `this row` / `that row`, which the per-file
  preamble names explicitly.
- **NOT a defect.** Row `:114`'s *"The 'shrinking trend' support is circular (see below)"*
  survives verbatim and still resolves: its referent is row `:116`, which is below it and
  was not touched. The reference was already cell-external in the baseline.

### 2e. No mathematics was fixed inside the restructure

Checked by the insertion enumeration: no new mathematical statement, no changed numeral, no
inserted or deleted negation anywhere in relocated content. The one clause where the row's
pointer differs in wording from the history file's copy — `NOT LANDED — a decision, not an
omission` in the row versus `NOT LANDED — this is a decision, not an omission` in the file —
drops two function words from a headline; the full original is verbatim in the file, and the
qualifier `it rests on an invalid quantifier step` that the row adds is baseline text, not
new.

---

## 3. THE STATED PROPERTIES

### 3a. Largest resulting cell — number right, **unit wrong**

| | baseline | after |
|---|---|---|
| largest cell (`:136`, mg-a3d4 row), **characters** | 15,386 | 8,442 |
| the same cell, **bytes** | **15,674** | **8,577** |

**F3 (MINOR) — the unit label is wrong, systematically.** Every cell and file size mg-34bf
reports as *"bytes"* is a **character** count. The commit's `15,386 → 8,442 bytes` and the
README's whole index table match my character counts to the character (the two-count offset
is the cell's padding spaces, which they include and I stripped). In bytes the figures are
15,674 → 8,577, and the file is 192,898 → 164,577 rather than the README's `188,870 →
161,269`. Understatement is 1.9–2.1% and no conclusion moves. It is worth recording because
the same document uses the label correctly elsewhere: *"the ten history files total 52,126
bytes"* **is** bytes (measured: 52,126 bytes, 51,082 chars). One document, one label, two
units.

Independent of the unit: 8,442 is the largest cell **anywhere** in the after file, as
claimed. The acceptance asked for the number and it was stated rather than optimised, which
is the right call.

### 3b. **F2 (BROKEN)** — the "five consecutive giants" figures are wrong in both documents, and the two documents disagree

| source | the five figures |
|---|---|
| commit message | 5.4 / 8.6 / 12.7 / 10.0 / **15.4** KB |
| `docs/state-history/README.md` | 5.4 / **9.2** / **13.5** / **10.8** / 15.4 KB |
| **measured** (rows 132–136, cell chars / 1000) | **8.6 / 12.7 / 10.0 / 13.2 / 15.4** |
| pm-onethird's ticket (a stale revision, line bytes) | 5.4 / 9.2 / 13.5 / 10.8 / 11.7 |

Rows 132–136 is unambiguously the intended set: the commit's *after* list — `rows 132-136
land at 4.8 / 6.9 / 6.2 / 7.7 / 8.4 KB` — matches my measurement of exactly those five cells
to the tenth of a KB. Against that:

1. **Row 135's cell — 13,188 characters, the second-largest cell in the file — appears in
   neither list.** The commit's list has five entries for five cells and row 135 is not one
   of them.
2. **Both lists open with a `5.4` that is not a cell.** 5.4 KB is row **131**'s whole *line*
   (all three columns) at a revision older than the base commit; it is inherited verbatim
   from the ticket. No cell in `STATE.md` has ever been 5.4 KB.
3. **The README's middle three figures (9.2 / 13.5 / 10.8) are the ticket's stale line-byte
   figures, not measurements**; the correct cell figures are 8.6 / 12.7 / 10.0. So the README
   is a hybrid of four inherited numbers and one measured one, and the commit message is a
   hybrid of one inherited and four measured.

So the sentence that opens the landing's account of the defect it fixed — *"the five
consecutive giants (5.4 / 8.6 / 12.7 / 10.0 / 15.4 KB as single table cells)"* — is false
about two of the five, and the durable convention document is false about four. The
restructure itself is unaffected; all ten cells were processed and row 135 was restructured
correctly (13,188 → 7,703 chars). What is broken is the measurement, in a landing whose
ticket opens by faulting a predecessor for *"a figure that commit itself reported as +7.6%,
understated 2.24x"*.

### 3c. **F5 (MINOR)** — the README gives two sizes for the same cell

The index table says row `:135`'s cell is `13,190`. Eleven lines later the same file says the
step-4d clause *"used to begin at byte 1,544 of a **14,340**-byte cell"*. 14,340 is the whole
**line** — all three columns — at 97cb533; the cell is 13,188 characters. Both numbers are
labelled the same way in the same document.

*(The 1,544 and 4,951 offsets are correct as character offsets into the line: `line[1544:]`
begins `After **five consecutive over-wide generalisations** (mg-d112, …` and the clause runs
to `**The mathematics.**` at ~4,951. The interval claim checks out; only its denominator is
misdescribed.)*

### 3d. The three A3 sites read in sequence — **PASSES**, on my own reading and timing

| | claimed | measured |
|---|---|---|
| site 1 position | second sentence of the cell | second sentence, starts at char 212 of 7,703 ✓ |
| site 1 length | 103 words | **103 words** ✓ (99 without the pointer link) |
| sites 2 and 3 | Appendix A, 55 lines apart, one file | `:200` and `:255` → **55 lines apart**, same file ✓ |
| three assertions in sequence | 190 words, 45.6 s @ 250 wpm | **224 words, 53.8 s** @ 250 wpm |

My word count is higher because I read the full provenance parenthetical at each Appendix A
site rather than the assertion sentence alone. **Acceptance criterion (c) — under a minute —
holds on either cut.** The improvement is real and large: the same clause used to run from
char 1,544 to 4,951 of the line, interleaved with the row's mathematics.

### 3e. **F1 (BROKEN)** — the new sentence certifying the A3 repair is false, and its counterexample is 399 characters earlier in the same cell

mg-34bf added this to row `:135`, at char 448:

> *"**This row states no count of its own** and points at Appendix A's two tallies instead,
> so it cannot rot on the next recount."*

The same cell's **first sentence**, at char 49, is:

> *"⭐ THE METHOD FINDING FIRST, because it is what **five previous rows** were missing…"*

Those five rows are precisely the five step-4d firings the count is about. The baseline made
that explicit in the very next sentence — *"After **five consecutive over-wide
generalisations** (mg-d112, mg-e35c, mg-f825, mg-c8c6, mg-09ea — see Appendix A step 4d)"* —
and mg-34bf relocated **that** sentence to `attempt-mg-276d.md` while leaving `five previous
rows` in the row. So the row does state a count of its own, of the same phenomenon, one
clause before asserting that it does not.

Appendix A's own resolution, which mg-34bf relocated into the history file and therefore
read, is *"the repair is not to pick a bigger number, it is to stop reporting one number"*.
The row still reports one number.

**Consequence: nil for mathematics, and the rot risk is genuinely low** — "five previous
rows" is anchored to the rows preceding this one and does not move when Appendix A recounts,
which is more than could be said for the tally figure that was removed. The narrow reading
("this row states no *4d tally* of its own") is true. But the sentence as written is an
absolute claim about the row, added by this commit, at the A3 repair site, with a visible
counterexample 72 words earlier in the same cell — which is the defect class this arc has now found in
seven consecutive generations, and it recurs here in the sentence written to certify the
repair.

### 3f. **F4 (MINOR)** — the completeness figure is reported as two different numbers

The commit message says **125** maximal runs. `docs/state-history/README.md` says **123**.
No checker output is committed, so nothing in the repository arbitrates. My independent
count is **125**; the commit message is right and the README is wrong. Small, but it is the
headline of the evidence for the binding constraint, and it disagrees with itself across the
two places it appears.

### 3g. No renumbering, no dropped rows, no collateral column edits

- 58 table rows before, 58 after. The `(line, column 1, column 2)` key of every row in the
  attempt index is **byte-identical**.
- The Full ledger's `#` column is identical: `1, 2, 3a, 3b, 4, 5, 6, 7, 8, 9, 10, 11`.
- In each of the ten changed rows **exactly one** column changed, and every other column in
  that row is byte-identical.
- 367 lines before and after; the ten changed lines are the *only* differences in the file,
  so no line was inserted or deleted. The line-number self-references (`:89`, `:132`) and
  mg-ae62's `around line 180` all still land where they did.

### 3h. Appendix A byte-identical — verified two ways

The Appendix A heading is at `:180`; the highest changed line is `:136`. Lines 180–367 are
byte-identical. **No rule moved, and no rule was inside a ledger cell.**

### 3i. No row contains a claim and its own retraction — checked all 58 rows, not the ten

I scanned every table cell in the after file for 26 strike / retraction / supersession /
correction markers and adjudicated each hit by hand. **The binding constraint holds.** What
remains in rows is exactly the three permitted kinds:

1. **Pointers naming what was struck, with the text relocated** — `:89` (`the conditional
   form this clause used to carry is SUPERSEDED … — [row history H1]`), `:114`, `:130`,
   `:132`, `:135`. This is design point 4 executed literally.
2. **Live claims that some *other* document's statement is refuted or struck** — `:122`,
   `:125`, `:133`, `:134`, `:136`. No row asserts a claim and its own retraction.
3. **Appendix A's step-4d tally rows** (`:236`–`:241`), whose purpose *is* to record
   adjudications, and which were out of scope and are untouched.

The only judgement calls worth naming: `:133` quotes the struck text (*"there is no modulus
`F` for which transport is true"*) in the row while pointing at H2 for the record, and `:136`
keeps the `G″` strike's mechanism note beside the strike. In both cases the row asserts the
*current* status of a claim it never made itself, so neither creates the forbidden adjacency.

### 3j. Both boundary rulings are real, not conveniences

The brief asked whether the stated reasons hold up. They do, and they are applied
consistently in both directions:

- **Corrections to the external `.tex` sketch stayed in the row.** Row `:135` keeps *"Three
  corrections to the source, all audit-confirmed"* — (i) the twist attaches to claim (2) too,
  (ii) the sketch does not say which side `s_i` acts on, (iii) the "precisely" overstatement.
  These are live facts about a document outside this programme's record.
- **An adjudication of a deliverable's *handling* of that source moved.** Row `:133`'s
  scope-check passage — *"all five cited `.tex` ranges (`:464–474`, … ) were pulled and
  verified verbatim by the auditor"* — is an audit finding about a deliverable, and it is in
  `attempt-mg-63e3.md`. Same document, opposite ruling, correctly distinguished.
- **The truncated-population disclosure stayed in row `:135` for a reason that is real, not
  convenient.** `38/38` occurs twice in `STATE.md` and in **zero** history files. Appendix A
  pins that figure's live population to three named files, one of which is that ledger cell;
  relocating it would have created a fourth and made Appendix A's paragraph false. Verified.

### 3k. The honest negatives are honest

- **The prose narrative at `:138–176` carries the same claim-beside-its-own-retraction shape
  and was left alone.** Verified: those lines are byte-identical, and `:140`, `:150`, `:163`,
  `:170`, `:172`, `:174`, `:176` do carry `Framing correction` / `Retired` / `refuted` /
  `OVERSTATED` beside live claims. The omission is named in both the commit message and the
  README rather than left silent. **That is compliance, not a failure** — the ticket's design
  is scoped to rows.
- **Rows 132–136 are still 4.7–8.2 KB and that is reported rather than fixed**, with the
  reason stated (condensing prose is forbidden by the same ticket). Correct: acceptance (a)
  asks for the number, not a target.

---

## 4. WHAT DID IT ADD BEYOND ITS BRIEF? **Zero.**

Target was zero on the standing rule mg-f2e1 landed and mg-ae62 upgraded, and **zero is what
it hit**. `57f962f` touches 20 files and every one is inside the brief:

```
STATE.md                             the ten cells, and nothing else in the file
docs/state-history/                  the artifact the brief asked for
code/state_restructure_34bf/         the checker the acceptance asked for
```

No file outside those three paths. No new ledger row. No repair to any finding. No
mathematics changed. In an enormous diff where every line has moved — the brief's own
description of a good hiding place — **there is nothing hidden.** That is the first landing
in this arc to hit the target, and it should be said plainly.

The additions to `STATE.md` itself are 8.2 KB gross / ~3.4 KB of words not previously in the
file, and they are pointer headlines plus `[row history Hn](…)` links. One of them is F1
above; the rest are accurate characterisations of what they point at.

---

## B1 — THE KNOWN-BROKEN PARAGRAPH: not lost, not relocated, and mg-34bf was right

The dispatch requires this stated separately from the clean completeness verdict, and it is
the check with the highest value, so it gets its own section.

**Status: NOT LOST. Byte-identical, at the same line, and findable.**

```
:343 at 7f04902  the raw B1 paragraph, as mg-e720 classified it BROKEN
:343 at 60f4dac  mg-3f21 REPAIRED it in place — evidence struck, finding survives
:343 at 97cb533  identical to 60f4dac (97cb533 does not touch STATE.md)
:343 at 57f962f  BYTE-IDENTICAL to its parent.  mg-34bf did not touch it.
:353 at HEAD     still present; moved by mg-ae62 (bdcb006), not by mg-34bf
```

**mg-34bf was correct not to relocate it, and it reported its location.** The paragraph is
in **Appendix A** (heading at `:180`), which the ticket put out of scope, and the commit
message names it explicitly: *"`STATE.md:343` — the BROKEN-and-OPEN relocated-hole paragraph
— is in Appendix A and was never in scope."* The README repeats it. So the reporting
obligation the mayor's relocation default was betting on was discharged, by name, in two
places.

**The dispatch note in my brief is stale, and this is worth recording so the next reader does
not act on it.** It says mg-34bf was instructed to relocate B1 and to report its new
location. By the time mg-34bf ran, `mg-3f21` had already repaired B1 and merged as `60f4dac`
— two commits before mg-34bf's parent — and pm-onethird had ruled *"GATE CLEARED — dispatch
with NO exclusion… the repair made the special case unnecessary,"* explicitly superseding and
removing the relocate-and-report instruction. **Judging mg-34bf against the withdrawn
instruction would penalise it for following the live one.**

**What the artifact still carries, and this is the part the clean verdict does not cover.**
The paragraph's finding is still **OPEN** — it opens *"AND THE CORRECTED FACT RELOCATES A
HOLE RATHER THAN CLOSING ONE — **OPEN**, and pm-onethird's to size"*. mg-3f21 struck the
**evidence** the finding was filed on (the `f6756c0` case, refuted by re-measurement: four
files, three of them a harness, a sweep script and instrument output, so the pre-existing
instrument clause did fire) and the finding **survives in abstract form with no existence
proof**. So the honest composite is:

> **Nothing was lost, AND `STATE.md` still contains an OPEN finding that a previous audit
> classified BROKEN, now carried without an existence proof.**

Whether mg-3f21's repair is adequate is not this audit's question — it is a research
judgement for pm-onethird, and mg-3f21 has its own audit path. I did not touch `STATE.md`.

---

## 5. FINDINGS, ranked

| # | sev | finding |
|---|---|---|
| **F1** | **BROKEN** | Row `:135`'s new sentence *"This row states no count of its own"* is false — the same cell's first sentence says *"what **five previous rows** were missing"*, a count of the same step-4d firings, 399 characters (72 words) earlier. In text mg-34bf added, at the A3 repair site, certifying the repair. §3e |
| **F2** | **BROKEN** | The "five consecutive giants" figure list is wrong in both the commit message and the README, and the two disagree. Row 135's cell — 13.2 KB, the second-largest in the file — is in neither list; both open with a `5.4` that is row 131's *line* size at a stale revision, inherited from the ticket. §3b |
| **F3** | MINOR | Every size labelled *"bytes"* is a **character** count (largest cell 15,674 → 8,577 bytes, not 15,386 → 8,442; file 192,898 → 164,577, not 188,870 → 161,269) — while the history-file total *"52,126 bytes"* in the same document really is bytes. §3a |
| **F4** | MINOR | The completeness figure is **125** maximal runs in the commit message and **123** in the README, with no committed checker output to arbitrate. Correct value is 125. §3f |
| **F5** | MINOR | The README gives two sizes for the same cell: `13,190` in the index table, *"a 14,340-byte cell"* eleven lines later (that is the whole line, all three columns). §3c |
| **F6** | MINOR | `attempt-mg-276d.md` carries *"see the next row"* inside a standalone file where there is no next row — the one deictic reference of eleven that relocation broke. §2d |

**Zero findings in relocated content. Zero in mathematics. Zero beyond the brief.** All six
are in the landing's arithmetic about itself, and F2/F3/F5 are all the same root cause: size
figures assembled partly from measurement and partly from the ticket, with the units and the
scope (cell vs line, chars vs bytes) not pinned.

---

## 6. WHAT THIS AUDIT DOES NOT ESTABLISH

- **It does not certify the relocation was well *judged*.** §1 proves nothing was lost and
  §3i–3j check the rules were applied consistently and for real reasons. Whether a given
  passage belongs in a row or a history file is a judgement, and mine agreeing with
  mg-34bf's on the cases I read is not proof.
- **It does not audit Appendix A or the `:138–176` prose.** Both are out of mg-34bf's scope
  and untouched; both still carry the shape the ticket set out to remove. The `:138–176`
  prose is a live, named, unrepaired instance of the defect this restructure was built for.
- **It does not settle B1.** See §B1.
- **My own instruments have one shared blind spot with the author's**: a passage relocated to
  a position where its surrounding context changes what it means, without changing a token,
  would be invisible to both. §2d is my partial answer — I enumerated the phrases most likely
  to suffer that and found one degraded case — but the class is not closed by construction.
