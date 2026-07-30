# Per-row histories for `STATE.md`'s ledger

**A ledger row asserts CURRENT STATE. Everything a row used to say, and everything that
struck, retired or corrected it, lives here — one file per row, linked from the row.**

Landed by **mg-34bf**, 2026-07-30, on the ticket's design: *"a row must not be able to
contain a claim and its own retraction."* The defect being fixed was measured, not
aesthetic — the five consecutive attempt-index rows `:132`–`:136` were single table cells
of **8.6 / 12.7 / 10.0 / 13.2 / 15.4 KB** at the base commit `60f4dac` (cell characters —
the same figures the index below carries), and the coverage-gap reopening notice in the
`:135` cell sat 9,316 characters into that 13.2 KB cell with no structural separation
between a claim and its retraction. In mg-f7bc's words: *the thing that let the original
three-way contradiction survive is now stronger, not weaker.*

> **THOSE FIVE FIGURES WERE WRONG, here and in `57f962f`'s commit message — mg-6a2f F2,
> BROKEN, corrected in place by mg-7735.** This file said `5.4 / 9.2 / 13.5 / 10.8 / 15.4 KB`
> and the commit message said `5.4 / 8.6 / 12.7 / 10.0 / 15.4 KB`, both offered as *"five
> consecutive giants … as single table cells."* Neither list is five cells, and neither is
> five consecutive rows. Re-measured from the commits themselves:
>
> | | what it actually is |
> |---|---|
> | `5.4 / 9.2 / 13.5 / 10.8 / 11.7` | rows `:131`–`:135`, whole **lines** in **bytes**, at `db08b4c` — the ticket's list, and the source both documents inherit from |
> | this file's `5.4 / 9.2 / 13.5 / 10.8` | the first four of those, unchanged: line-byte figures for rows `:131`–`:134`, not cells |
> | its fifth, `15.4` | row `:136`'s **cell**, in characters — a row that **did not exist** at `db08b4c` (327 lines; `:136` was added later) |
> | the commit message's `8.6 / 12.7 / 10.0` | rows `:132`–`:134`'s cells, correctly measured — but still opening on the inherited `5.4` |
>
> So this file's five figures cover rows `:131`–`:134` **and** `:136` — five rows, but not
> five *consecutive* ones and not the five the sentence names, four measured as lines and one
> as a cell, from two different revisions — and both lists skip row `:135` entirely, whose
> cell is **13.2 KB, the second largest in the file**. `5.4` is not a cell at any revision:
> row `:131`'s cell is 4.9 KB, and no cell in `STATE.md`'s history rounds to 5.4 KB in either
> characters or bytes.
>
> The old *"byte 8,402 of an 11.5 KB cell"* was the same defect one clause later: 11.5 KB is
> row `:135`'s whole **line** at `db08b4c` (11,544 characters — its *bytes*, 11,727, being
> the `11.7` the ticket's fifth slot carried), and 8,402 is an offset into that line. At the
> base commit the notice sits 9,316 characters into a 13,188-character cell.
>
> **The restructure itself is untouched by this.** All ten cells were processed — row `:135`
> included, 13,188 → 7,703 characters at the landing — and nothing was lost, established
> twice by two independent constructions in mg-6a2f §1. What was mismeasured was the defect,
> never the repair of it. `57f962f`'s commit message is frozen and still carries its list, so
> this is where the correction lives.

## The rule

1. **A row asserts current state only.** What is true now, at what status, over what
   population, with its citations.
2. **Every retraction, correction, supersession and mechanism note relocates here**, and
   the row keeps a pointer naming it.
3. **RELOCATION, NOT DELETION.** Nothing was summarised, condensed, paraphrased or
   dropped. Every passage in these files is the ledger cell's own text, character for
   character. The mechanism records are the most valuable content in those cells and none
   of them was touched.
4. **If the current claim needs a "this used to say X" to be understood, the pointer goes
   in the row and the text goes here.**

## What relocated, exactly

A passage moved iff it is:

- **(a)** a report of what a row, this document, or a prior ledger row **used to say**, or
  a strike / retirement / correction of it;
- **(b)** an **adjudication of a deliverable or an audit** — over-wide, BROKEN-as-labelled,
  struck, downgraded, mislabelled — or an audit tally or nested provenance chain;
- **(c)** a **derivation, construction, enumeration or numeric evidence** supporting a
  claim the row still states;
- **(d)** a **defect-mechanism note**: why a defect survived, or what let it happen.

(a), (b) and (d) are the numbered `H1`, `H2`, … sections, which the row cites by number.
(c) is the *Supporting record* section, reachable from the row's trailing pointer.

A passage **stayed** in the row if it is a status or verdict headline, a live claim with
its scope and population, a citation, an open item, an explicit instruction, or the honest
net. Two boundary rulings, stated so they can be argued with rather than guessed at:

- **Corrections to an EXTERNAL source document** (the `.tex` sketch) are live facts about
  that source and **stayed in the row**. Only corrections to text inside this programme's
  own record relocate — that adjacency is what the ticket forbids.
- Where one sentence carried **both a claim and its evidence**, it stayed in the row. The
  cut points are sentence boundaries; nothing was cut mid-sentence.

## What was NOT touched

- **Appendix A** — byte-identical to the base commit `60f4dac`. No rule moved; no rule was
  inside a ledger cell.
- **`STATE.md:343`** at the landing — now **`:356`**, moved by `mg-ae62` (+10 lines) and
  `mg-a053` (+3), never by this change — the *"the corrected fact RELOCATES A HOLE RATHER
  THAN CLOSING ONE"* paragraph, which an audit classifies BROKEN and OPEN. It is in
  Appendix A, so it was out of scope; pm-onethird also asked for it by name. mg-6a2f §B1
  checked it and agrees: **byte-identical to its parent at the landing, not lost, not
  relocated, and mg-34bf was right not to move it** — verified again here, `57f962f:343` and
  `:356` today are the same bytes.

  **Two corrections to this bullet, from mg-6a2f §B1, made by mg-7735.** The repair is
  **`mg-3f21`'s**, at `60f4dac` — two commits before mg-34bf's parent — and **`mg-ae62`
  explicitly did *not* touch it**; this file credited the wrong commit. And *repaired* is not
  *closed*: mg-3f21 struck the **evidence** the finding was filed on, and the finding
  **survives in abstract form with no existence proof**. It is still **OPEN**, and
  pm-onethird's to size. Nothing in this change touches it.
- **The prose narrative at `STATE.md:138–176`.** Several of those paragraphs carry the same
  claim-beside-its-own-retraction shape. They are not rows and were not in scope. Named
  here so the omission is visible rather than silent.
- **Columns 1 and 2** of every row (verdict, attempt) — unchanged, which is also what makes
  the completeness check's row key stable.
- **Line numbers.** `STATE.md` has exactly the same number of lines as before and no line
  was inserted or deleted, because two live self-references (`:89` and `:132`) and
  `mg-ae62`'s brief point into the file by line. That is why this convention is documented
  here and not in a new paragraph of `STATE.md`.
- **Row numbering and row identity** — no row renumbered, added or removed.

## The index

| row | which row | history file | cell before | cell after | history bytes |
|---|---|---|---|---|---|
| `STATE.md:89` | row 11 | [`ledger-row-11-L4.md`](ledger-row-11-L4.md) | 1,556 | 1,585 | 1,449 |
| `STATE.md:114` | the **DROP (tractability only)** row | [`attempt-mg-c47a-drop.md`](attempt-mg-c47a-drop.md) | 725 | 555 | 1,652 |
| `STATE.md:124` | the **GREEN-partial · diagnostic (mg-48ab)** row | [`attempt-mg-48ab.md`](attempt-mg-48ab.md) | 1,467 | 1,621 | 1,265 |
| `STATE.md:130` | the **SOUND negative · actionable (mg-210d)** row | [`attempt-mg-210d.md`](attempt-mg-210d.md) | 2,597 | 2,052 | 2,128 |
| `STATE.md:131` | the **RED-for-lever · AMBER-redirect · CORRECTS MERGED WORK (mg-a58f)** row | [`attempt-mg-a58f.md`](attempt-mg-a58f.md) | 4,918 | 3,651 | 3,426 |
| `STATE.md:132` | the **OVERSTATED · core CONFIRMED-conditionally · RE-SHAPES (R) (mg-88bd)** row | [`attempt-mg-88bd.md`](attempt-mg-88bd.md) | 8,630 | 4,804 | 6,913 |
| `STATE.md:133` | the **RED-conditional · witness fully CONFIRMED · CORRECTS MERGED WORK (mg-63e3)** row | [`attempt-mg-63e3.md`](attempt-mg-63e3.md) | 12,696 | 6,876 | 9,808 |
| `STATE.md:134` | the **RED · UNCONDITIONAL · witness `W*` fully CONFIRMED · DISCHARGES row 11's condition (mg-3af9)** row | [`attempt-mg-3af9.md`](attempt-mg-3af9.md) | 9,974 | 6,247 | 5,752 |
| `STATE.md:135` | the **GREEN · PROVEN, all finite posets · first proof-carried generalisation in the arc (mg-276d)** row | [`attempt-mg-276d.md`](attempt-mg-276d.md) | 13,190 | 7,705 | 9,049 |
| `STATE.md:136` | the **AMBER-POSITIVE · THE BET IS PRICED (mg-a3d4)** row | [`attempt-mg-a3d4.md`](attempt-mg-a3d4.md) | 15,386 | 8,442 | 10,684 |

**`cell before` and `cell after` are measured at `60f4dac` and at the landing `57f962f`**,
not at current `HEAD`, and the pair is what the restructure did. One cell has moved since:
mg-7735's F1 correction took row `:135`'s to **7,878**. No other cell in the table has
changed, and `:136` is still the largest.

Largest cell anywhere in `STATE.md`: **15,386 → 8,442 bytes** (the mg-a3d4 row).
`STATE.md` overall: 188,870 → 161,269 bytes. **36,188 bytes of ledger text moved**, and the
ten history files total 52,126 bytes — the difference is the per-file headers, which are new.
About 5 KB of new pointer text went into the rows, which is why two small rows grew.

**Rows 132–136 are still large, and that is reported rather than fixed.** What is left in
them is live claims — the mg-a3d4 row alone asserts about forty of them. Getting those
cells below a couple of kilobytes would mean condensing prose, which the ticket forbids in
the same breath as it asks for terseness. The binding constraint was met: no row now
contains a claim and its own retraction.

## How completeness is checked

```
python3 code/state_restructure_34bf/verify_relocation.py   # nothing was lost
python3 code/state_restructure_34bf/a3_reading_path.py     # the three A3 sites
```

`verify_relocation.py` does **not** read the relocation spec and does not use the builder's
splitter. It takes each ledger cell as it stood at `60f4dac` and decomposes it into
**maximal verbatim runs** that can still be found, word for word, in the rewritten cell or
in a history file **that the rewritten cell links to**. At the landing commit: **10 cells,
11,625 words, 123 maximal runs, 0 words unaccounted for**, shortest run 8 words.

Read that result precisely. It establishes that no word was dropped and no wording inside a
run was altered, and that everything counted as kept is reachable by a reader starting at
the row. It says nothing about whether text was *added* — pointers were — and nothing about
whether the relocation was well judged. It is a completeness check, not a quality one.

It also asserts three things the restructure must not disturb: every ledger row still
present under an unchanged verdict column; Appendix A byte-identical; and the truncated-
population figure quoted in the mg-276d row absent from every file in this directory.
Appendix A pins that figure's LIVE population to three named files, one of which is that
ledger cell; relocating it here would have made a fourth, and Appendix A's paragraph false.
The checker names the figure because a scanner must; this file does not, for the same
reason Appendix A gives — *"text that exists in order to COUNT the number, not to be read
for it"* is not a coverage claim, and a summary is. So that disclosure stayed in the cell.

## The three A3 sites (`a3_reading_path.py`)

The sites that disagreed under mg-1319 — `STATE.md`'s own *"reported three incompatible
ways in one commit"* — are the mg-276d ledger row, Appendix A's *"STEP 4d … AND THEY MUST
NOT SHARE ONE TALLY"* paragraph, and template step **4d**. The row's step-4d clause used to
begin at byte 1,544 of a 14,340-byte cell and run, interleaved with the row's mathematics,
to byte 4,951; it is now the **second sentence of the cell**, 133 words, and it **states no
4d tally of its own** — it points at Appendix A's two tallies, which are 55 lines apart in
one file. Reading the three assertions in sequence: **220 words, 52.8 s at 250 wpm**, so
acceptance criterion (c) — the three assertions in under a minute — still holds.

> **`no 4d tally` is a correction, and `133` / `220` are its cost — mg-6a2f F1, BROKEN,
> corrected in place by mg-7735.** The row and this file both said *"states no **count** of
> its own"*, and `57f962f`'s commit message still does. That absolute is false: the same cell
> opens *"what **five previous rows** were missing"* — a count of the same step-4d firings,
> 399 characters and 72 words earlier — so the row stated a count of that phenomenon one
> clause before asserting that it did not. Appendix A's own resolution is *"the repair is not
> to pick a bigger number, it is to stop reporting one number"*, and the narrow claim is both
> the true one and the one that resolution asks for: no *tally* is restated in the row, so a
> recount of Appendix A cannot rot it. The correction deliberately does **not** restate the
> count in the row — that is what the row is claiming not to do — so it is recorded here
> instead. It cost site 1a 103 → 133 words and the sequence 190 → 220 words (45.6 → 52.8 s),
> re-measured with `a3_reading_path.py`, which still reports **PASS**.
>
> **How it survived, which is worth naming:** `a3_reading_path.py` checks *"states or quotes
> a firing count"* against site 1a alone — the `⚠️ STEP 4d DID FIRE HERE …` clause it matches
> by regex — while the sentence claims something about *the row*. The counterexample is in
> the row's first sentence, outside that window. A claim about a cell, checked against a
> clause: the same scope mismatch as the cell-versus-line figures above. The instrument is
> **not** changed here — re-scoping what it checks is a redesign, not a repair, and it is
> left open.

## How these files are produced

`code/state_restructure_34bf/` holds the builder. `spec.py` carries the per-row assignment
of passages plus a table of **anchor guards** — the first 44 characters each passage key
must start with at the base commit — so a change to the passage splitter fails loudly
instead of silently relocating the wrong text. That guard caught one real mis-mapping while
this change was being built. `build.py` asserts the partition (every passage emitted exactly
once) and that no relocation split a bold span, before it writes anything.
