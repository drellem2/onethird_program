# Independent audit of mg-7735 / `b68db5d` — the landing of the mg-6a2f audit

**mg-bd41, 2026-07-30. Pre-filed by the mayor before mg-7735 ran, so this audit does not
depend on anyone remembering to ask for it.**

**VERDICT: OVERSTATED — 3 BROKEN, 5 MINOR.**

**Zero defects in the measurement work.** Every figure the F1, F2 and B1 repairs rest on
reproduces *exactly* from instruments written for this audit that read none of the author's
code: all five corrected cell sizes, all five source line-byte figures, both word counts and
both reading times, the 399-character / 72-word gap, the whole 20-figure index table, the
byte-identity of the B1 paragraph, and a 23,920-measurement universal over every revision of
`STATE.md`. **56 checks, 55 pass.** The one arithmetic failure and the two other BROKEN items
are not in the repairs — they are, once again and for the seventh consecutive generation, in
what the commit says **about itself and about its own evidence**.

The single most important thing in this document: **the commit's headline verification
sentence is blind to the change it certifies, and I demonstrated that with a negative control
rather than inferring it.**

| | finding | class |
|---|---|---|
| **A1** | *"`run_all.sh` reproduces `out_audit.txt` BYTE-IDENTICALLY **with these edits applied**"* — the battery pins fixed revisions and cannot see the working tree. Negative control: with `STATE.md` **gutted from 175,552 to 37,958 bytes**, the output is *still* byte-identical. | **BROKEN** |
| **A2** | *"which located the source the audit did not name"* — mg-6a2f named it: *"pm-onethird's ticket (a stale revision, line bytes)"*, plus the row, the unit and the vintage. Only the hash `db08b4c` is new. | **BROKEN** |
| **A3** | *"`60f4dac` … two commits before mg-34bf's parent"* — it is **one**. In the commit message **and** in the durable README bullet. | **BROKEN** |
| **A4** | The raw-vs-stripped cell convention splits *inside the change*: `13,188 / 7,703 / 7,876 / 8,440` against `13,190 / 7,705 / 7,878 / 8,442` for the same cells at the same revisions. | MINOR |
| **A5** | *"8,402 is an offset into that line"* — no offset equal to 8,402 exists in 71,424 (line, coordinate, anchor) triples across all 35 revisions. | MINOR |
| **A6** | `9,316` is measured from `BUT`, not from the notice's own start (`9,311`/`9,312`); the anchor is not stated. | MINOR |
| **A7** | The index-table annotation is material beyond the ticket's list and is not counted in the beyond-brief tally, whose baseline is the *audit's findings* rather than the *brief*. | MINOR |
| **A8** | The README's `188,870 → 161,269` is called *"a character count"*; it is characters **minus newlines** (`189,237 → 161,636`). | MINOR |

Reproduce: `sh code/state_landing_audit_bd41/run_all.sh` (output committed as
`out_audit.txt`, ~8 s).

---

## 0. Instruments, and why they are not the author's

`code/state_landing_audit_bd41/` was written from scratch for this audit. It imports nothing
from `code/state_restructure_34bf/` or `code/state_audit_6a2f/`. `instrument_sensitivity.py`
*executes* two of the author's scripts, but only to test claims **about** those scripts —
never to obtain a figure.

Three hazards this arc has already been bitten by, all of which bear directly on
self-arithmetic:

- **`wc -m` counts BYTES on this box.** Confirmed live: `LC_CTYPE=C`, and
  `wc -m STATE.md` = `wc -c STATE.md` = `175552`, while `LC_ALL=en_US.UTF-8 wc -m` gives
  `172499`. Cross-checking the two would have read as confirmation while both were wrong.
  **Nothing here shells out to `wc`**: characters are `len(str)`, bytes are `len(bytes)`.
- **Units are part of a measurement.** Every figure below names *chars* or *bytes*, and —
  new for this artifact — every cell figure names its **convention** (raw / stripped).
- **A bounded read manufactures false absences.** No `head`, `tail`, `sed -n A,Bp` or
  `--limit` appears anywhere in the battery. Every negative prints the population it was
  taken over: 210 cells, 35 revisions, 23,920 measurements, 71,424 triples.

One definitional note, because it bit my own first pass: literal pipes inside `STATE.md`
cells are escaped `\|`, so a naive `|`-split shatters row `:135` into nine fragments. The
battery splits on pipes **not preceded by a backslash**. And because `STATE.md` holds tables
of different arities — the ledger rows are 3-column, row `:89` sits in a 4-column table —
"the third column" is not a portable definition of *the cell*; the battery uses the row's
**widest** cell.

---

## 1. A1 (BROKEN) — the re-run that cannot see the change

The commit opens its evidence paragraph with this:

> I re-ran both: `sh code/state_audit_6a2f/run_all.sh` reproduces `out_audit.txt`
> BYTE-IDENTICALLY **with these edits applied**.

It does reproduce byte-identically. I confirmed it: 96,291 bytes, `cmp`-clean.

**It would reproduce byte-identically if the edits had been catastrophic.** Every script in
the mg-6a2f battery pins fixed revisions — `97cb533`, `60f4dac`, `57f962f` — and reads the
committed `docs/state-history/*.md` **at `57f962f`**. Not one of them opens the working tree
or resolves `HEAD`. The battery is blind to `b68db5d` by construction.

I did not infer this from reading the source. I ran the control:

```
NEGATIVE CONTROL: STATE.md gutted 175552 -> 37958 bytes, 381 -> 181 lines
battery output still byte-identical to out_audit.txt : True
```

Two hundred lines deleted outright and line 1 replaced with `TOTALLY DESTROYED`, and the
audit battery reports the identical 96,291 bytes. The clause **"with these edits applied"**
is doing evidentiary work the run cannot support: it invites the reader to conclude that
mg-6a2f's conclusions were re-established against the new file, and no such thing happened.

**In fairness, and it matters:** the commit's *second* cited re-run is genuine. The
completeness half of `verify_relocation.py` opens the working tree (`verify_relocation.py:95`),
and my positive control confirms it moves when the file moves — truncating row `:135`'s cell
takes it from `10 cells / 11,625 words / 125 maximal runs` to `9 / 9,470 / 112`. At HEAD it
reports **10 cells, 11,625 words, 125 maximal runs, 0 unaccounted**, exactly as claimed. So
the commit *does* hold real evidence for its invariant. It simply leads with the one that
isn't, and that is the sentence a reader will quote.

This is filed BROKEN rather than MINOR because it is a landing whose entire subject is
claims that outrun their evidence, and because "landed cleanly, re-verified byte-identically"
is precisely the tidy narrative the ticket exists to stop recurring.

---

## 2. A2 (BROKEN) — the source the audit did name

> F2 (BROKEN) — … Verbatim from the audit's table, then re-derived from the commits rather
> than accepted, **which located the source the audit did not name**.

mg-6a2f's F2 section, `docs/OneThird-STATE-Restructure-IndependentAudit.md:212` and the two
numbered points beneath it:

```
:212      | pm-onethird's ticket (a stale revision, line bytes) | 5.4 / 9.2 / 13.5 / 10.8 / 11.7 |

point 2   "5.4 KB is row 131's whole *line* (all three columns) at a revision older
           than the base commit; it is inherited verbatim from the ticket."

point 3   "The README's middle three figures (9.2 / 13.5 / 10.8) are the ticket's
           stale line-byte figures, not measurements."
```

The audit named the origin (the ticket), the unit (line bytes), the scope (the whole line,
all three columns), the row (`:131`), and the vintage (older than the base commit). What
mg-7735 adds is the specific hash, `db08b4c` — a real contribution, and I verified it
(`git merge-base --is-ancestor db08b4c 60f4dac` passes; 23 commits separate them; the
mg-34bf ticket carries `13,487 / 10,824 / 11,727 bytes`, which are exactly `db08b4c`'s
`:133`/`:134`/`:135` line bytes). **But the sentence claims novelty over the audit for
material the audit supplied,** and that is a status error in the over-claiming direction,
about the very document it is landing.

---

## 3. A3 (BROKEN) — one commit, not two

> It is mg-3f21's, at `60f4dac`, **two commits before mg-34bf's parent**

and, written into the durable convention document:

> The repair is **`mg-3f21`'s**, at `60f4dac` — **two commits before mg-34bf's parent** —

The ancestry is linear: `57f962f` (mg-34bf) ← `97cb533` ← `60f4dac`.

```
commits from 60f4dac to mg-34bf's PARENT : 1
commits from 60f4dac to mg-34bf ITSELF   : 2
```

`60f4dac` is **one** commit before mg-34bf's parent — it *is* the parent's parent. "Two
commits before mg-34bf" would have been right. This is a wrong count, in a durable document,
in the paragraph a landing wrote while correcting a wrong attribution — the target class
exactly.

**The attribution itself is correct, and impressively so.** Tracing the B1 paragraph across
all 35 revisions of `STATE.md`:

```
d5a3043 (mg-7d5a)  :343   691 bytes   <<< created
60f4dac (mg-3f21)  :343  2582 bytes   <<< repaired
57f962f (mg-34bf)  :343  2582 bytes
bdcb006 (mg-ae62)  :353  2582 bytes
672915e (mg-a053)  :356  2582 bytes
b68db5d (mg-7735)  :356  2582 bytes
```

The repair is mg-3f21's at `60f4dac`; mg-ae62 did **not** touch it; `57f962f:343` and
`b68db5d:356` are byte-identical; and the paragraph moved `+10` then `+3` lines, matching
the file's `367 → 377 → 380`. Every one of those claims reproduces. The stated method also
reproduces — `git log -S "landed by mg-3f21" -- STATE.md` returns exactly `60f4dac`.

---

## 4. A4 (MINOR) — the convention split inside the change

A markdown cell can be measured with or without its bounding spaces. `b68db5d` uses **both**,
in the same change, and labels neither:

| site | `:135` before | `:135` after | `:136` | convention |
|---|---|---|---|---|
| README index table (+ its new annotation) | `13,190` | `7,705` → **`7,878`** | `8,442` | **raw** |
| README's new F2 block | **`13,188`** | **`7,703`** | — | **stripped** |
| commit message, *SCOPE AND INVARIANTS* | `7,703` | **`7,876`** | **`8,440`** | **stripped** |
| measured (this audit) | 13,190 / 13,188 | 7,705 / 7,703 → 7,878 / 7,876 | 8,442 / 8,440 | raw / stripped |

Every figure is correct under one convention. The defect is that they sit in one change and
do not agree, and specifically:

- The new F2 block says its figures are *"cell characters — **the same figures the index
  below carries**"*, then thirty lines later gives *"13,188 → 7,703 characters at the
  landing"* for a cell the index below records as `13,190 → 7,705`. The `13,188 / 7,703`
  pair is imported verbatim from mg-6a2f, which uses the stripped convention, into a document
  that does not.
- The commit message certifies *"`:136` remains the largest cell at **8,440**, so the
  README's largest-cell claim still holds"* — and the README's largest-cell claim is
  `8,442`. The conclusion is true (I confirmed `:136` is the largest of all 210 cells at
  HEAD). It is justified with a number the artifact does not contain.

This is the F5 shape — *the README gives two sizes for the same cell* — recurring inside the
commit that left F5 open, at a magnitude of 2 characters rather than 1,150. Filed MINOR on
that basis, and reported because a two-character silent convention change is exactly the kind
of thing the next recount inherits.

---

## 5. A5 / A6 (MINOR) — the two offsets

**A5.** The commit diagnoses the old figure:

> 11.5 KB is row `:135`'s whole LINE at `db08b4c` (11,544 characters; its bytes, 11,727 …)
> and **8,402 is an offset into that line**.

The first half is exact and is a genuinely good find — `11,544` chars and `11,727` bytes both
reproduce, and they explain the mg-34bf ticket's *"byte 8,402 of an 11,544-byte cell"*
precisely: `11,544` is the **line** in **characters**, mislabelled a cell in bytes.

The second half does not reproduce. Searching every revision of `STATE.md`, every line, six
coordinate systems and three anchor choices — **71,424 triples** — for an offset equal to
`8,402`:

```
offsets equal to 8,402 found : 0
nearest at db08b4c :135      : 8,373 line-chars / 8,501 line-bytes (notice start)
```

`8,402` lands 29 characters *inside* the notice, in the middle of `RELOCATED, NOT CLOSED`. So
the sentence is true only in the vacuous sense that `8,402 < 11,544`. In a paragraph headed
*"THE SOURCE, found"* whose other four figures are exact, an unestablished correspondence
reads as a fifth measurement.

**A6.** The replacement figure — *"the notice sits **9,316** characters into a
**13,188**-character cell"* — is measured from `BUT THE COVERAGE GAP`, i.e. **skipping** the
notice's own `**⚠️ ` prefix. From the notice's start it is `9,311` (stripped) / `9,312` (raw).
Correct, but anchor-dependent by five characters with the anchor unstated, in a clause whose
predecessor failed for anchor-and-unit reasons.

---

## 6. Second target — the completeness property, re-verified rather than re-read

mg-6a2f's result is that **nothing was lost**, and it is the best-evidenced completeness
claim in this arc. A landing that edits `STATE.md` can break that property while carrying the
sentence that asserts it. mg-7735 *did* edit `STATE.md` content (row `:135` grew by 173
characters), so the cheap boundary argument — "it touched only the arithmetic" — is not
available. **I re-established the property.**

`multiset_whole.py` rebuilds the check from scratch: tokenize `STATE.md@60f4dac` into a
case-folded multiset of maximal alphanumeric runs, tokenize the whole after-corpus
(`STATE.md` + every `docs/state-history/*.md`) the same way, and count baseline occurrences
that the after-corpus cannot cover. Order-free and global.

```
at the LANDING (57f962f) : 31,538 baseline token occurrences,   0 UNACCOUNTED
at HEAD        (b68db5d) : 31,538 baseline token occurrences,   4 UNACCOUNTED
```

**The restructure lost nothing — CONFIRMED a third time,** by a different tokenizer and a
different corpus construction from either mg-34bf's or mg-6a2f's. (My occurrence total,
31,538, differs from mg-6a2f's 30,388 because the tokenizations differ; the *property* — zero
unaccounted — is what reproduces, and it does, exactly.)

**mg-7735 did not break it.** Isolating across the three commits between the landing and HEAD:

```
57f962f  mg-34bf  (the landing)             unaccounted= 0
bdcb006  mg-ae62                            unaccounted= 5   counterexample, primary, should, treat, you
672915e  mg-a053  (mg-7735's PARENT)        unaccounted= 5   counterexample, primary, should, treat, you
b68db5d  mg-7735  (the change under audit)  unaccounted= 4   primary, should, treat, you
```

The erosion is **mg-ae62's**, at `bdcb006`, which dropped five baseline token occurrences when
it rewrote Appendix A's template step 4d. mg-7735 **restored one of the five** —
`counterexample`, via its new README paragraph — taking 5 to 4. The landing's effect on the
property is net positive.

**Reported because nothing watches this.** `verify_relocation.py`'s completeness half checks
only that the ten *restructured* cells' words remain reachable, so it reports `0 unaccounted`
at HEAD and is structurally unable to see a whole-file drop somewhere else. The four
occurrences have been unaccounted since `bdcb006` and no instrument has said so. This is not
mg-7735's defect and I am not filing it against this commit — it is pm-onethird's to size.

---

## 7. Third target — material beyond the brief

The ticket's list is F1, F2 and B1, with *"do not add material beyond this list"* and Appendix
A's `TARGET ZERO` rule at `STATE.md:268` making the **brief** the baseline. Diffing the brief
against the 77 added README lines gives four blocks:

| block | in the brief? |
|---|---|
| the F2 correction (rewritten opening + the `THOSE FIVE FIGURES WERE WRONG` blockquote and its table) | **yes** — F2 |
| the B1 bullet rewrite + *"Two corrections to this bullet"* | **yes** — B1/P3 |
| the F1 correction (`no 4d tally`, `133`/`220`, the `no 4d tally is a correction` blockquote) | **yes** — F1 |
| **the index-table annotation** (*"`cell before` and `cell after` are measured at `60f4dac` …"*) | **no** |

Plus, inside the F2 block, the `8,402` / `11.5 KB` clause, which the commit **names as beyond
scope itself** and offers as revertible — that disclosure is exemplary and I am not counting
it against the change.

**A7 is the index-table annotation.** It *is* disclosed in *SCOPE AND INVARIANTS* (*"the index
table is now labelled as measured at the landing with the one moved figure named"*), so this
is not a smuggled addition. But the commit's beyond-brief accounting is headed *"ONE CLAUSE
BEYOND **THE AUDIT'S SIX FINDINGS**"* — the audit's findings, not the ticket's brief — and
under `TARGET ZERO` the baseline is what the commit was **asked for**. Counted against the
brief, there are two additions, not one.

And the arc's pattern holds: **the new figure that disagrees with the rest of the change —
`7,878` against the commit message's `7,876` — is in the block that was not asked for.** Its
substance is nonetheless correct: I verified all twenty of the index table's figures, and
*"No other cell in the table has changed"* and *"`:136` is still the largest"* both hold.

---

## 8. What reproduces exactly

Recomputed from the artifact with my own instruments, never by reading the author's numbers
or re-running the author's script:

- **F2's five corrected cells**, `:132`–`:136` at `60f4dac` in characters —
  `8,630 / 12,696 / 9,974 / 13,190 / 15,386` → `8.6 / 12.7 / 10.0 / 13.2 / 15.4 KB`. All five.
  And *"the same figures the index below carries"* is true of these five.
- **F2's five source figures**, rows `:131`–`:135`'s whole lines in **bytes** at `db08b4c` —
  `5,351 / 9,228 / 13,487 / 10,824 / 11,727` → `5.4 / 9.2 / 13.5 / 10.8 / 11.7 KB`. All five,
  and this is the finding that closes F2's provenance.
- **The 5.4 KB universal.** 35 revisions × every cell × {raw, stripped} × {chars, bytes} =
  **23,920 measurements, 0 rounding to 5.4 KB.** Row `:131`'s cell is 4,918 chars = 4.9 KB.
- `db08b4c` has **327 lines** and **zero** occurrences of `mg-a3d4`.
- **F1's cost, with my own word counter**: site 1a `103 → 133` words; the three-assertion
  sequence `190 → 220` words; `45.6 → 52.8 s` at 250 wpm; sites 2 and 3 `55` lines apart;
  acceptance criterion (c) holds with 7.2 s of margin. `a3_reading_path.py` reports **PASS**.
- **F1's gap**: from *"five previous rows"* to *"This row states no …"* is **399 characters
  and 72 words** — both exact, in the cell before *and* after.
- **The scope invariants**: exactly one `STATE.md` line changed (`:135`); 380 lines before and
  after; three columns; `**` parity even in **all 210 cells**; the whole file's column-count
  vector identical; `:136` still the largest cell of all 210.
- **`verify_relocation.py`'s `FAIL Appendix A changed`** is correctly attributed to
  `bdcb006`/`672915e` and not to this change — `b68db5d` touches only line 135, and Appendix A
  begins at `STATE.md:180`, well below it.
- **F3's real-byte figures**: `192,898 → 164,577` bytes. Exact. (A8: the README's
  `188,870 → 161,269` is characters *minus newlines*, not "a character count" — actual
  characters are `189,237 → 161,636`. The substance of F3 — labelled bytes, is not bytes —
  holds either way.)
- **F4 correctly left open**: the README still reads `123 maximal runs` where the instrument
  says 125.
- **The frozen commit message quoted correctly**: `57f962f`'s message does say
  *"the five consecutive giants (5.4 / 8.6 / 12.7 / 10.0 / 15.4 KB as single table cells)"*.

## 9. Status language

Checked in both directions, as the brief asks.

**Over-claiming:** A1 and A2 above — an evidentiary sentence that cannot support its clause,
and a novelty claim over material the audit supplied.

**Under-claiming:** none found. If anything the commit prices its own best work low. The
`db08b4c` identification is a real result reached by a real method, the `11,544` / `11,727`
pair genuinely explains a mislabel nobody had explained, and the 34-revision scan supplies
evidence for a universal that mg-6a2f asserted without it. Those are stated in one sub-clause
each while the vacuous re-run leads the commit.

**CLOSES versus RELOCATES** — correct, and the reasoning is sound. Each false claim exists in
`STATE.md`, in the README, and in `57f962f`'s frozen commit message; the first two are repaired
and the README names the third as still carrying the error. Calling either CLOSED would have
been wrong, and the commit does not.

**"landed cleanly" is not claimed anywhere**, and the commit's disclosure discipline is the
best in this arc: it names the beyond-scope clause and offers to revert it, names the four
MINOR findings it left open, names the pre-existing `verify_relocation.py` failure and
attributes it rather than assuming, names an instrument scope mismatch it deliberately did not
re-scope, and records that its own first attempt at the F1 fix broke an acceptance criterion.
None of the three BROKEN items is a concealment. All three are the same thing the ticket was
about: **the content is right and the claims about the content are wrong** — this time in a
commit written to repair exactly that, by the same author, with the same method, in the same
blind spot. That is the seventh consecutive generation.
