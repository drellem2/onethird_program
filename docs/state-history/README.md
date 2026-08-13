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

## The convention was finished, not changed — mg-ea0e, 2026-08-06

**mg-34bf left this convention half-applied and mg-ea0e finished it**, on pm-onethird's
relocation spec (mg-ea0e), which is Daniel's *"it should be an executive summary"* directive
of 2026-08-06 turned into three mechanical moves. `STATE.md` went **186,710 → 32,772 bytes**
and **29,094 → 4,658 words**, and its longest line went **13,367 → 1,772 characters**.
Nothing was deleted; three things moved.

1. **The seven oversize attempt-index cells now carry their status label, their own opening
   sentence verbatim, and a link** — and each file below gained a
   `## Full cell text before the mg-ea0e relocation (2026-08-06)` section holding **that
   cell's entire text, all three columns, character for character**:
   [`attempt-mg-210d.md`](attempt-mg-210d.md), [`attempt-mg-a58f.md`](attempt-mg-a58f.md),
   [`attempt-mg-88bd.md`](attempt-mg-88bd.md), [`attempt-mg-63e3.md`](attempt-mg-63e3.md),
   [`attempt-mg-3af9.md`](attempt-mg-3af9.md), [`attempt-mg-276d.md`](attempt-mg-276d.md),
   [`attempt-mg-a3d4.md`](attempt-mg-a3d4.md). The `H1`… sections above them are untouched;
   passages mg-34bf had already relocated recur inside the appended section only because it
   is the whole cell. Rows `:114` and `:124`, under the 2,000-character acceptance
   threshold, were **not** touched.
2. **The prose narrative this file records as out of scope** — *"`STATE.md:138–176`"*, the
   § *Where the threads converge* chronology — is now
   [`threads-chronology.md`](threads-chronology.md), whole and unedited. `STATE.md` keeps a
   short current-position paragraph and the link. That bullet's observation was right: those
   paragraphs *"carry the same claim-beside-its-own-retraction shape."*
3. **Appendix A** — recorded below as *"byte-identical to the base commit `60f4dac`"*, which
   remains true of mg-34bf's change — is now
   [`../audit-stage-process.md`](../audit-stage-process.md), whole and unedited. **So the two
   Appendix-A line references below, `STATE.md:343` and `:356`, resolve into that file now,
   not into `STATE.md`.**

**The index table below is still correct and was re-checked, not assumed.** `STATE.md` lines
`1–129` are **byte-identical** to the base commit `78ae4d9`, so `:89`, `:114`, `:124` and
`:130`–`:136` still name the rows this file says they do; the mg-ea0e edits inside that range
are confined to the interiors of rows `:130`–`:136` and inserted or deleted no line. What
mg-ea0e did break is the *line-count* invariant recorded below: `STATE.md` is now 176 lines,
not 387, and every line reference **after** `:141` is stale. Re-derived by
`code/state_restructure_ea0e/verify_relocation_ea0e.py`, whose transcript is committed beside
it: **0 of the old file's 68 mg-ids unreachable, 0 correction markers lost, 0 lines or ledger
columns missing.**

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
  **`mg-3f21`'s**, at `60f4dac` — **mg-34bf's parent's parent**: ONE commit before its parent
  `97cb533`, two before the landing `57f962f` — and **`mg-ae62` explicitly did *not* touch
  it**; this file credited the wrong commit. And *repaired* is not
  *closed*: mg-3f21 struck the **evidence** the finding was filed on, and the finding
  **survives in abstract form with no existence proof**. It is still **OPEN**, and
  pm-onethird's to size. Nothing in this change touches it.

  > **`two commits before mg-34bf's parent` was off by one — mg-bd41 A3, BROKEN, corrected
  > here by mg-2da3.** The ancestry is linear `57f962f <- 97cb533 <- 60f4dac`, so `60f4dac`
  > is the parent's parent. It was wrong in this bullet and in `b68db5d`'s commit message;
  > this site CLOSES, the frozen message still carries it. **The attribution the clause sits
  > inside is CORRECT and is not disturbed** — mg-bd41 traced the paragraph across all 35
  > revisions of `STATE.md` (`d5a3043` created it at 691 bytes, `60f4dac` repaired it to
  > 2,582, byte-identical from `60f4dac` onward) and `git log -S "landed by mg-3f21"` returns
  > exactly `60f4dac`. An off-by-one in the distance, not an error in the credit.
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

## Second landing — mg-14ad, 2026-08-13: the five rows the ratchet had recorded as DEBT

**These five are a SEPARATE landing and are measured differently from the table above** —
`Result column` characters at `9dc1f87`, not whole-cell bytes at `60f4dac` — so they are
kept apart rather than appended to a table whose figures mean something else. Only the
**Result** column moved; the Status-label and Attempt columns stayed in the row (and are
reproduced in each history file for context).

Why these five and not a judgement call: `code/state_ratchet_e331/out_p1_growth.txt` §3
already named them, as *"every attempt-index row added since [mg-ea0e] — 7351 words, 44837
chars, 5 rows"*, with the remedy *"relocate attempt rows to their per-attempt files"*. They
were the only attempt-index rows that had never been relocated.

| row | which row | history file | result col before | after |
|---|---|---|---|---|
| `STATE.md:174` | the **GREEN · UNBLOCKS mg-6bc2 on its own second disjunct (mg-345e)** row | [`attempt-mg-345e.md`](attempt-mg-345e.md) | 4,231 | 208 |
| `STATE.md:177` | the **RED on the constant · RED on the rate · GREEN on one branch (mg-200d)** row | [`attempt-mg-200d.md`](attempt-mg-200d.md) | 10,099 | 483 |
| `STATE.md:178` | the **CORRECTS MERGED WORK · P6 rescored HELD (mg-ba78)** row | [`attempt-mg-ba78.md`](attempt-mg-ba78.md) | 5,483 | 199 |
| `STATE.md:179` | the **GREEN · reduces `C₃` to L2 — it does not discharge L2 (mg-76b2)** row | [`attempt-mg-76b2.md`](attempt-mg-76b2.md) | 9,954 | 571 |
| `STATE.md:180` | the **REFUTED — and a proved theorem shipped inside the refutation (mg-51f4)** row | [`attempt-mg-51f4.md`](attempt-mg-51f4.md) | 14,241 | 966 |

`STATE.md` overall: **21,328 → 14,218 words**, and `code/state_ratchet_e331/CEILING.json`
was banked to the achieved figure **in the same commit**, which is the half of the rule that
makes a cut hold. **No line number in `STATE.md` moved**: every edit rewrites a cell inside
an existing line and no line was added or removed.

**What stayed in each row is the leading bolded verdict run, verbatim** — including, where a
headline is immediately followed by its own strike-through correction (`:180`), *both*, so
that no row asserts a claim whose retraction has been moved out from under it. That is
mg-34bf's original design constraint and it is the one thing this landing could most easily
have broken.


## Third landing — mg-bdb0, 2026-08-13: the FOUR LEDGER ROWS, and the first use of the two-landing protocol

**This is the landing `docs/STATE-SPLIT-PROPOSAL-mg-14ad.md` §8.3 measured as impossible.**
Rows 3b, 6, 8 and 11 are essays inside *ledger* cells — not attempt-index cells — and
`code/rendered_twin_pin_9bc2` digests those rows per row, so moving one turns the gated
`twin.worklist` red while `reconcile()` refuses to re-pin in the same commit. mg-1344's
**section 8** breaks that: this is **landing A**, the re-pin is deferred, and
`code/rendered_twin_pin_9bc2/IN-FLIGHT.json` declares the four rows until landing B.

| row | history file | Result cell before | after | which clauses sent text out |
|---|---|---|---|---|
| `STATE.md:118`, row 3b | [`ledger-row-3b-standard-dominance.md`](ledger-row-3b-standard-dominance.md) | 374 w | 107 w | (a), (b), (c), (d) |
| `STATE.md:121`, row 6 | [`ledger-row-6-theorem-e.md`](ledger-row-6-theorem-e.md) | 299 w | 154 w | (a), (b), (c), (d) |
| `STATE.md:123`, row 8 | [`ledger-row-8-L1b.md`](ledger-row-8-L1b.md) | 1,328 w | 665 w | (a), (b), (c) |
| `STATE.md:126`, row 11 | [`ledger-row-11-L4.md`](ledger-row-11-L4.md) *(appended — mg-34bf's file)* | 235 w | 174 w | (a) |

`STATE.md` overall: **5,987 → 4,851 words**, `Full ledger` **2,814 → 1,678**, and
`code/state_ratchet_e331/CEILING.json` banked to the achieved figure **in the same commit**.
Per-row reasoning, clause by clause, is in `docs/STATE-SPLIT-PROPOSAL-mg-14ad.md` §8.3b.

**COMPLETENESS IS MECHANICAL HERE AND NOT AN ASSERTION.** Every moved passage is a *literal
slice* of the cell as it stood at `092a508`; the retained text is the rest of that cell, also
literal, with only the punctuation seams a removal leaves. **Retained + moved reconstruct each
old cell character for character**, asserted before the files were written. Each `H`/`S`
section carries an italic lead-in naming the text that stood either side of it in the row,
because several slices are mid-sentence fragments and a fragment printed bare cannot be
checked against the seam it came out of.

**One rule was applied against itself and is worth naming.** `ledger-row-11-L4.md`'s new
`H1 (continued)` is the *row-side sentence that pointed at `H1`* — a report of a supersession,
so clause (a) sends it here, even though what it reports is already here. The row keeps the
trailing pointer and nothing else of it.

**What did NOT move, deliberately:** the `Kind`, `Status` and `Width` columns of all four rows
are untouched, which is mg-34bf's own convention (`Columns 1 and 2 of every row — unchanged`)
carried to the ledger. Row 3b's `Kind` cell still carries its struck `FP` and the withdrawal
sentence, because `lib9bc2.md_kinds()` reads that exact shape and because a withdrawn mark is
a live fact about the row's warrant.

---
---

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

## What certifies a change to these files, and what does not

```
sh code/state_landing_control_2da3/run_all.sh    # the delta control + its negative control
```

> **`b68db5d`'s HEADLINE VERIFICATION SENTENCE IS BLIND TO THE CHANGE IT CERTIFIES —
> mg-bd41 A1, BROKEN, corrected here by mg-2da3 because the commit is frozen.** That commit
> opens on *"I re-ran both: `sh code/state_audit_6a2f/run_all.sh` reproduces `out_audit.txt`
> BYTE-IDENTICALLY **with these edits applied**"*. It does reproduce — 96,291 bytes,
> `cmp`-clean — and **it would reproduce if the edits were catastrophic**. mg-bd41 gutted
> `STATE.md` from **175,552 to 37,958 bytes** (200 lines deleted, line 1 replaced with
> `TOTALLY DESTROYED`) and the battery emitted the identical 96,291 bytes.
>
> **Stated plainly: that re-run is evidence about `57f962f`. It is not, and cannot be,
> evidence about `b68db5d`.** Every script in `code/state_audit_6a2f/` pins `97cb533` /
> `60f4dac` / `57f962f` and reads the committed `docs/state-history/*.md` at `57f962f`; not
> one opens the working tree or resolves `HEAD`.
>
> **The battery is not the defect and is not changed.** Reproducing an audit of a specific
> historical state is what mg-6a2f built it for, and pinning is a *feature* there — pointing
> it at the working tree would destroy the only thing it is good for. The defect is the
> citation: re-running a revision-pinned instrument in a later commit converts a valid
> control into one that **cannot fail**, and it does so **silently**, because the command
> succeeds and the bytes match.
>
> **What was missing was a second instrument, and it now exists.**
> `code/state_landing_control_2da3/delta_control.py` certifies `b68db5d`'s actual delta —
> row `:135`'s F1 repair and this file's F1 / F2 / B1 blocks — reading the **working tree**
> for everything it certifies, with `b68db5d^` used only as the *before* side of a measured
> delta. It locates the row by its attempt id rather than by line number, so it does not rot
> when lines are inserted above it, and it exits **non-zero** both when the repair is damaged
> (`1`) and when a measured constant of the landing has moved (`2`) — never green about a
> delta that is no longer the delta it was written for. `negative_control.py` proves it fires:
> under mg-bd41's exact gutting, under a revert of row `:135` alone, and under a cut of this
> file's F1 block it exits non-zero every time, while the pinned battery — same destroyed
> tree, same run — goes on reproducing its 96,291 bytes.
>
> **In fairness, `b68db5d`'s SECOND cited re-run is genuine.** `verify_relocation.py`'s
> completeness half opens the working tree, its tallies move when the file moves, and its
> **10 cells / 11,625 words / 125 maximal runs / 0 unaccounted** is a real measurement. The
> commit holds real evidence. It led with the one that was not.
>
> **And none of this touches "nothing was lost", which STANDS.** mg-6a2f established it
> twice with independently-written instruments and mg-bd41 confirmed it a **third** time from
> a different corpus construction — 0 of 31,538 baseline token occurrences unaccounted. A
> blind certification of a one-line edit is a **control** defect, not a content defect.

> **"`negative_control.py` proves it fires" DID NOT ESTABLISH WHAT THE BLOCK ABOVE CLAIMS
> — mg-2216 B1/B2, BROKEN, repaired by mg-7870.** The instrument the block above describes
> certified by asserting five chosen **substrings** were present, and mg-2216 built fourteen
> independent mutations of which **eight exited 0** — one character of the certified cell
> (*"every ridge in 1 or 2 facets"* → *"1 or 3"*), five characters inverting the row's verdict
> on its own proof, an ASCII-space → U+00A0 substitution with no visible change, two adjacent
> sentences swapped, **3,000 of the cell's 7,876 characters** replaced by `x`, this file's F1
> block **hollowed to its header, its 1,556-character body deleted**, and two falsified
> figures — *"13,188 → 7,703 characters"* and the **`175,552 to 37,958 bytes`** the A1
> correction above rests on.
>
> **The README half was blind because it tested block HEADERS, and `negative_control.py`
> cuts each block including its header.** The author's mutation was the mutation the check
> was shaped around, which is the closed loop this cluster exists to open.
>
> **The repair replaces the mechanism rather than extending the list**, because *"does it
> catch mutation X?"* is open-ended and every list is a list somebody chose. Each certified
> region now carries a **SHA-256 of its normalised bytes**; the normalisation is one stated
> rule (strip ASCII space/tab/CR/LF from the two ends, nothing else), and it is the only
> place a mutation can still hide. **`code/state_landing_control_2da3/COVERAGE.md` states
> which regions are digested and what is deliberately not covered** — the goal is bounded,
> stated coverage, not total coverage. The certified set is now **eight** regions, wider than
> the *"row `:135`'s F1 repair and this file's F1 / F2 / B1 blocks"* the block above claims:
> the A1 and A3 correction blocks and the index note are digested too.
>
> **The evidence is mg-2216's battery, not this repair's negative control.** An instrument
> whose only evidence of sensitivity is the negative control its own author wrote is the
> defect being repaired, one level up. mg-2216's fourteen mutations, re-run **unmodified**
> against the repaired instrument: **10 caught, 0 missed, 4 tolerated by design, 0 noisy** —
> captured verbatim at `code/state_landing_control_2da3/out_battery_2216_rerun.txt`.
> `code/state_control_audit_2216/out_mutations.txt` is now a frozen record of the pre-repair
> instrument and no longer reproduces; that is the finding landing, not a regression.
>
> **The pinned battery is still not touched and still reproduces `out_audit.txt`
> byte-identically** — 96,291 bytes, verified across this repair, as mg-2216 verified it
> across the last one.

> **WHETHER THESE ARE THE CERTIFIED BYTES IS NOT THE SAME QUESTION AS WHETHER A READER IS
> SHOWN THEM — mg-babf B1, BROKEN, repaired by mg-4acd.** The digest above is the right
> mechanism and is **not undone**. mg-babf re-implemented mg-2216's five survivors from
> their published prose and **all five fire**; five independent probes of the normalisation
> all landed correctly. What mg-babf found is that the blind spot had **moved one layer up,
> into the LOCATOR**. Four mutations changed **no certified byte** and exited **0**: a
> certified block moved verbatim under *"Appendix Z — superseded drafts … nothing below is
> in force"*; this file's F1 block wrapped in a fenced code block, so it renders as a code
> sample rather than as a correction; **the same block wrapped in an HTML comment, absent
> from every rendered view of this file**; and a *"RETRACTED … is void"* paragraph inserted
> immediately above a certified block.
>
> **The property now certified is that a mutation which changes what a reader SEES must
> change a digest.** Each region carries a second digest, of a four-field **presentation
> record**: whether the region is presented as prose at all or sits inside a code fence, an
> HTML comment or a raw HTML block; the heading path in force where it sits; its ordinal
> among the blocks of its section; and a hash of its text with block-quote markers removed.
> A certified region that **nobody is shown** is a FAIL, not a MOVED — the bytes being
> present is not the claim.
>
> **The cost is stated beside the mechanism rather than discovered later.** mg-babf proposed
> digesting the *rendered* text and named the cost: a dependency on a renderer, under which
> a renderer upgrade becomes a false positive. The direction is taken; the mechanism is not.
> No markdown renderer exists on this box, and every instrument in this cluster imports
> nothing. **The cost taken instead is that `presentation.py` is a MODEL of a renderer, not
> a renderer** — argued from the CommonMark and GFM block rules and *not measured against an
> implementation, because there is none here to measure against*. What bounds it is
> **default-deny**: a block construct outside its declared subset, or any raw HTML in text
> presented as prose, is reported and exits non-zero rather than passing. What is **not**
> bounded is the model being confident and wrong. That is the uncontrolled layer now, and it
> is named here so the next auditor tests it instead of discovering it.
>
> **Two of mg-2216's declared tolerances are reversed, and deliberately.** M12 (sixty lines
> inserted above the certified row) and M13 (the row moved to the end of the file,
> byte-identical) now fire. Both break the ledger table — M12 splits it so the certified row
> has no delimiter row above it, M13 lifts the row out of it entirely — so under GFM the row
> stops rendering as a table row and becomes pipes in a paragraph. That is a change to what a
> reader sees. Locating by attempt id rather than by line number is unchanged, and still buys
> what it always bought.
>
> **A correction to the block above, from mg-babf B4: the certified set was NINE regions,
> not eight.** The code, `COVERAGE.md` and mg-7870's own commit message all said nine and
> enumerated nine; only that sentence said eight. With this block it is **ten**.
>
> **`COVERAGE.md` now states what the control does NOT cover**, which is the half that was
> missing: presentation, position, inline rendering, the row's index within its table, and
> the fidelity of the model to any real renderer. A bounded coverage statement exists so the
> next auditor can test the boundary; the boundary moved, so the statement moved with it.

> **THE PROPERTY THE BLOCK ABOVE PUBLISHES IS FALSE AS PUBLISHED, AND A CERTIFIED ROW'S
> MEANING CAN LIVE IN A FILE NOTHING CERTIFIES — mg-218d B1 and B2, BROKEN, repaired by
> mg-bee1.** The mechanism above is right and is **not undone**: mg-218d verified it against
> two real GFM renderers — `marked` and `markdown-it`, **140 of 140** comparisons, including
> the M12/M13 reversal `COVERAGE.md` itself flags as unverified — and the locator fires on
> all four of the mutations the ticket asked it about. What moved is the **statement**, and
> then the layer above it.
>
> **B1. "A mutation that changes what a reader SEES must change a digest" is universally
> quantified over mutations; the mechanism is quantified over a region's OWN SECTION.**
> `heading` is the ATX path and `position` is an ordinal among the blocks *of that section*.
> Nothing outside the section is a field. mg-218d's demonstration is a pair differing by one
> line: the `RETRACTED … is void` paragraph as the first block **inside** the certified
> section exits **2**; **the same paragraph one line earlier**, as the last block of the
> section before, exits **0** — and a reader is shown the same page in both. So the mutation
> `e4426c9` leads with is caught by where its author put the paragraph, not by a property.
> Three more at that layer exit 0: a retraction in an unrelated section of this file, a new
> *"READ THIS FIRST — this document is superseded"* section near the top, and the same in
> `STATE.md`.
>
> **The repair is the sentence, in every place it was published.** The property now reads:
> *a mutation that changes how a certified region is presented — the container it renders
> in, the heading path in force over it, or its ordinal among the blocks of **its own
> section** — must change a digest*, and **cross-section context is named as uncovered**.
> An over-claimed control is worse than a narrow one, because the sentence is what the next
> reader relies on. `e4426c9`'s commit message cannot be edited and still carries the
> unqualified form; this block is the correction of record.
>
> **The obvious fix was measured and NOT taken.** A document-global `position` would close
> all four of those mutations — and it re-baselines on a block added or removed anywhere
> above a certified region, which on these two files is most commits; `code/state_delegation_repair_bee1/`
> reports the measured rate over the recent history of both. It also does **not** make the
> unqualified sentence true: a retraction that *replaces* an existing paragraph elsewhere
> changes what a reader sees, adds no block, and exits 0 under the global ordinal too. Trading
> a silent miss for a guard that cries wolf on every commit, and still not getting the
> property, is not a trade worth taking silently, so it was not taken at all.
>
> **B2. The certified ledger cell delegates its content to a file outside the certified
> set.** Row `:135`'s cell carries **six** inline links into `attempt-mg-276d.md` (seven
> occurrences of the path — one link's text is the path) and cites sections **H1–H5 by
> name**, and that file opens *"Every passage below was moved verbatim out of that cell …
> The row now asserts current state and points here."* Deleting a cited section, **inverting
> the F1 repair there** so the row and the file it sends you to say opposite things, and
> emptying the file all exited **0**. `COVERAGE.md` named `attempt-*.md` as *files* not
> covered; what was named nowhere is that the thing it *does* certify is a **pointer**.
>
> **What is delegated is what is cited.** The control now reads each certified region's own
> bytes, extracts every inline link, and digests the target sections a link cites **by
> name** — a cited section that is gone is a **FAIL**, one whose bytes moved is a **MOVED**,
> and a target cited but undeclared (or declared but no longer cited) is a **MOVED**, so the
> delegation surface cannot grow or rot silently. It is one rule over the regions' own text,
> not a list of files somebody chose. Its bound: only the **cited** sections are delegated,
> so a retraction at the top of that file, outside every cited section, still exits 0.
>
> **What is uncontrolled after this repair, named rather than left to be discovered.**
> Cross-section presentation context (B1, above — stated, not closed). The **region set**:
> a contradicting near-copy of a certified block, added under a new heading, exits 0, because
> no digest over a chosen set of regions can see a region that is not on the set — closing
> that by counting blockquotes would catch mg-218d's mutation and not the layer, which is
> the enumeration failure this lineage has already diagnosed twice. And the **instrument**:
> deleting an entry from `CERTIFIED` narrows coverage silently and exits 0. What did close
> there is narrower and is claimed as narrow — `norm()` is now checked **behaviourally**
> against the rule three documents publish for it, so widening it to `str.strip()` is a
> non-zero exit instead of the silent no-op it was.

> **`which located the source the audit did not name` is an over-claim — mg-bd41 A2, BROKEN,
> corrected here by mg-2da3.** `b68db5d` writes that of its F2 re-derivation. mg-6a2f **did**
> name the source, at `:212` of its own document — *"pm-onethird's ticket (a stale revision,
> line bytes)"* — together with the row (`:131`), the scope (the whole line, all three
> columns) and the vintage (older than the base commit). **What is new is the hash
> `db08b4c`**, which is a real contribution and is verified: 327 lines, zero occurrences of
> `mg-a3d4`. The F2 block at the top of this file states the identification without the
> over-claim; the frozen commit message still carries it.

**The general rule this generated is in `STATE.md`'s Appendix A** — *"Re-running a
REVISION-PINNED instrument certifies the revision it is pinned to, never the commit that
re-ran it"*. Read it before citing any battery in this directory's orbit as evidence for a
commit: `verify_relocation.py`'s completeness half and `a3_reading_path.py` read the working
tree and can be cited for a change to it; everything under `code/state_audit_6a2f/` cannot.

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
