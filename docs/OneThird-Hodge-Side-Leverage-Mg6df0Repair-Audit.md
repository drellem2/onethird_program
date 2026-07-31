# The mg-6df0 repair, independently audited — the matrix, the refusal, and the scope of the fix

**mg-7e39.** Independent audit of `77306a7`, the repair of the mg-ec07 verdict on
`code/hodge_leverage_landing_e1d0/verify_landing.py`. Pre-filed in the same action as its parent.

    code/hodge_leverage_audit_7e39/  run_all.sh  ~2 min  exit 0
    47 checks, 39 confirmed, 8 measured, 0 refuted, 5 findings.
    0 mathematical statements are touched.

Instrument: `code/hodge_leverage_audit_7e39/audit_7e39.py`. Predictions, **committed before any
transcript existed** (`7cee1a1`): `PREDICTIONS.md`, with **six misses kept as written, three of
them this instrument's own defects**. Transcript: `out_audit_7e39.txt`.

---

## THE HEADLINE, WHICH IS THE PART THAT HOLDS

**The repair does what it says at the grain it was told to work at.** Both of mg-ec07's open
items are closed and closed at the product, not at a cell:

- **The refusal now covers the three rows the substring test excluded, and it covers them one at
  a time.** `partition` bent lossy **at a single site**, so the only blocking row refuted is that
  site's `RECORD PARTITION`, then `--reseal` on disk: **exit 1, REFUSED, `site_records.txt`
  unchanged, at 3 of 3 sites.** The same probe against the commit before the repair: **exit 0,
  BLESSED, the record rewritten, at 3 of 3.** The parent demonstrated this once with all three
  sites bent together, which is one cell of a three-cell population; this is the population.
- **Every enumerated kind fires at every site it applies to**, on a matrix built from scratch:
  my own derivations, my own write-back into the file, scored by running `verify_landing.py` as a
  **subprocess** and reading its stdout. **29 of 29 applicable cells fire; 0 silent; every one
  exits 1.**
- **Nothing confirmed was disturbed.** `37 909 of 37 909` characters of the three sites cannot be
  substituted in silence, against a control of **462 of 37 909 (1.2%)** at `eb600f7`; **847 of
  847** figure exchanges fire with `FIGURE ORDER` refuted and `SITE RECORD` green on every one.

And the two cutters I wrote **from the repair's disclosure sentences alone**, without reading its
code, reproduce its three sites **byte for byte at 3 of 3**. That is the test of whether a scope
sentence is a specification or a label, and these ones are specifications.

## THE MATRIX, BECAUSE THE BRIEF ASKED FOR A MATRIX AND NOT A TOTAL

12 kinds × 3 sites, derived and scored independently. `(rec)` = caught by `SITE RECORD` with
every `FIGURE CENSUS` and `FIGURE ORDER` row green.

| kind | the STATE.md row | §14 | H8 |
|---|---|---|---|
| K01 the LIVE figure a reader meets, corrupted | FIRES | FIRES | FIRES |
| K02 the figure DUPLICATED at the site | FIRES | FIRES | FIRES |
| K03 a WRONG figure in ORDINARY PROSE | FIRES | FIRES | FIRES |
| K04 wrong prose REUSING a figure on the roster | FIRES | FIRES | FIRES |
| K05 a NEW undeclared historical figure | FIRES | FIRES | FIRES |
| K06 two DECLARED FIGURES exchanged | FIRES | FIRES | FIRES |
| K07 two LABELS exchanged, no figure moved | FIRES (rec) | FIRES (rec) | FIRES (rec) |
| K08 two table ROW LABELS exchanged | n/a | n/a | FIRES (rec) |
| **K09 two COLUMN HEADERS exchanged — mg-ec07's X1** | **FIRES (rec)** | n/a | FIRES (rec) |
| K10 a figure inside a MARKED QUOTATION altered | n/a | FIRES (rec) | n/a |
| **K11 the table's ALIGNMENT shifted** | **FIRES (rec)** | n/a | FIRES (rec) |
| K12 a whole PARAGRAPH relocated out of the site | n/a | FIRES (rec) | FIRES |

**29 applicable, 29 fire, 0 silent, 7 n/a.** Cell by cell against the artifact's own matrix:
**35 of 36 agree**, and the single disagreement is the bolded `K11` — which the artifact calls
`n/a` and which fires. **X1 — `K09` at the `STATE.md` row, the cell that was exit 0 with the same
kind caught at H8 — is exit 1 with `SITE RECORD` refuted and every figure row green.**

## F1 — `n/a` IS WHERE A MATRIX HIDES, AND ONE OF THE EIGHT IS A FACT ABOUT THE DERIVATION

*This is the item no list in the brief names.* The repair's own predictions record that its first
matrix reported **19** applicable cells because a write-back was failing silently, and state the
lesson in as many words: **a derivation that fails silently reads exactly like a site that has no
such text.** That miss was repaired twice. So each of the eight `n/a` reasons is read here as a
**claim about the site** and measured against the site.

Seven survive. One does not:

> `K11 @ the STATE.md row` — **"no line here has two runs of two or more spaces to shift"**

The `STATE.md` site **is a table**. It is a markdown pipe table, and a markdown table's alignment
is the padding inside its cells; `k_layout` shifts runs of two-or-more spaces, which is how a
**whitespace-column** table is aligned. `_table_lines` recognises both formats and `_header_line`
recognises both; `k_layout` recognises one. So the cell reports **the shape of the derivation in
the grammar of a fact about the site** — and the site it does it at is the one the whole X1
argument turns on.

An independently derived alignment shift at that cell **FIRES**, caught by `SITE RECORD`, exit 1.
So it **understates coverage and hides no hole**: the published matrix is `28 of 28 applicable /
8 n/a` where the site supports `29 of 29 / 7`. It is a finding about the instrument, not the
gate — and it is the same shape as the defect the instrument was built to close, one level down.

The seven that survive, with the measurement behind each:

| cell | the reason, read as a claim | measured |
|---|---|---|
| `K08 @ the STATE.md row` | fewer than two figure-carrying rows inside the site | **1** — this is X2, declared open |
| `K08 @ §14`, `K09 @ §14`, `K11 @ §14` | §14 has no table | **0 pipe rows, 0 whitespace-column rows, 0 header line** |
| `K10 @ the STATE.md row`, `K10 @ H8` | marked quotations, none carrying a figure | **12 and 5 quotations, 0 and 0 carrying a figure** |
| `K12 @ the STATE.md row` | no figure-free paragraph after the first | **1 paragraph** |

## F3 — THE EXIST/TOUCHED PAIR: **1 TOUCHED, 6 EXISTED, 5 LIVE**

The brief asked for two numbers. Swept by an **AST** walk with a vocabulary **derived from the
code that prints the rows**, over every `.py` under `code/` at the repair's own commit:

| | |
|---|---|
| instances of the construct at the repair's parent `803bd50` | **6** |
| instances the repair **touched** | **1** — `verify_landing.py`'s `reseal()` |
| instances live in the commit the repair landed in | **5** |

All five carry a declared disposition keyed on the exact line, so a new occurrence anywhere makes
the sweep red — that is a real control and it is more than the arc had before. But **a
disposition is a reason, not a repair**, and four of the five select **6 gate rows where 3 were
meant**, measured here row by row:

| | exposure over the 34 live rows |
|---|---|
| `audit_a318_repair.py:326` `'READ AT THE SITE' in l` | 12 by substring, 12 by heading — **0** it was never meant to select |
| `audit_8916_repair.py:518` `'FIGURE CENSUS' in l` | 6 by substring, 3 by heading — **3** |
| `audit_ec07.py:714` `'SITE RECORD' in r` | 6 by substring, 3 by heading — **3** |
| `repair_ec07.py:303` `'SITE RECORD' in d` | 6 by substring, 3 by heading — **3** |
| `repair_835f.py:309` `'FIGURE CENSUS' in l` | 6 by substring, 3 by heading — **3** |

**In `verify_landing.py` itself the claim holds exactly**: 7 row-identifying comparisons,
**0 by substring, 7 through `heading()`**. `heading()` is the only way any caller in that file
names a row.

## F5 — THE SWEEP'S VOCABULARY IS A HAND LIST, WHICH IS A SCOPE NOBODY CHOSE ONE LEVEL UP

`ROW_NAMES` in `repair_ec07.py` names **five** row headings **by hand**. The gate prints **six**.
Same rule, three vocabularies, same 448 files:

| rule | vocabulary | occurrences |
|---|---|---|
| the parent's line regex | its own hand list of 5 | **4** — the number its transcript publishes |
| the parent's line regex | derived from the code that prints the rows | **5** |
| my AST walk | derived | **5** |

**The rule is not what hides the extra one; the hand list is.** The occurrence outside the hand
list is `audit_a318_repair.py:326`, `"READ AT THE SITE" in l`. Its measured exposure is **0** —
it selects exactly the rows it means — so nothing is wrong downstream of it. What is wrong is
that a sweep built because *a hand-picked site is a scope nobody chose* picks its **vocabulary**
the same way. The fix is one line: take the names from the code that prints them.

## F2 — THE SWEEP'S OWN POPULATION IS A FIGURE STALE IN THE COMMIT THAT PUBLISHES IT

`out_repair_6df0.txt` publishes **"429 `.py` files swept"**.

| | |
|---|---|
| `.py` files under `code/` at `77306a7`, the commit that **ships that transcript** | **448** |
| at `803bd50`, its parent — the commit the repair was measured against | **448** |
| at HEAD, after this audit's own probe file joined the population | 449 |

The gap is **not** a merge that landed after the run: the tree already held 448 at the probe
commit. **19 files are in the population and not in the number a reader is given.** The
instrument re-derives the count on every run and is live; what is frozen is the figure in the
evidence. This is mg-f922 B/C — a figure stale in the commit that publishes it — **inside the
sweep whose entire argument is that the reported line is never the population**.

## F4 — A SCOPE SENTENCE TRUE OF THE PART THE REPAIR BUILT, WRITTEN OF THE WHOLE FUNCTION

> *"AND THE NEGATIVE CONTROL NOW MUTATES THE FILE AND RE-CUTS THE SITES FROM IT — a battery that
> mutates site texts in place cannot exhibit a site-boundary defect, which is why the gap
> survived an enumeration."*

`kind_matrix`, called from `negative_control`, routes **all 36** of its attempts through
`with_site` — the file, then re-cut. The **19 further `figure_gate(...)` probes in
`negative_control`'s own body** are still handed mutated **site texts in memory**: the exact
construction the sentence names as unable to exhibit a site-boundary defect. Those 19 are
figure-side, so nothing below them is known to be missed. What is wrong is the **scope of the
sentence** — which is this repair's own subject, and the reason mg-ec07 told it to check every
scope sentence at every site.

## THE SCOPE SENTENCES, EACH TRIED AT EVERY SITE

The one the repair **inherited** was false at 1 of 3. The ones it **writes** hold:

| sentence | tried at | result |
|---|---|---|
| `EXTENT_OF["section"]` — *heading to the next heading of the same or shallower level, not the file* | §14, H8 | **2 of 2** — reproduced byte for byte from the sentence alone |
| `EXTENT_OF["framed_row"]` — *the row and the header lines it is read under, not the table's other rows* | the STATE.md row | **1 of 1**; the table is 24 header-or-verdict lines, 3 are inside the site, **22 verdict rows stay outside** — X2, declared open with its cost measured |
| *a site whose anchor has no declared extent makes the run RED* | falsified directly | the cutting function renamed and nothing else changed → **exit 1, the `DECLARED extent` row REFUTED**. A fail-closed rule that can be made to fail |
| *a site is no longer a contiguous substring of its file at 1 of 3 sites* | 3 sites | **exactly 1** — the `STATE.md` site occurs 0 times in `STATE.md`, §14 and H8 once each |
| *the record grows by 43; the reseal diff is two lines* | re-measured | **37 866 → 37 909, +43**, diff **+2/−0** |
| *282 600 of 320 509 characters (88.2%) outside every record* | re-measured | **identical to the character** |

## DO NOT DISTURB — RE-RUN, AND NOTHING MOVED

| | |
|---|---|
| every character of every site substituted alone | **37 909 of 37 909 fire.** mg-ec07 confirmed **37 866 of 37 866**; the population is larger by the repair's own **43**, and reporting it as 37 866 would be the stale figure one level up |
| the same instrument against the gate at `eb600f7` | **462 of 37 909 (1.2%)** — mg-ec07 measured 462 of 37 866, and the 43 new characters are a markdown header and delimiter carrying no figure token, so the control does not move at all |
| `RECORD PARTITION` on point mutations | **0 of 37 909** — unfalsifiable by any document edit, which is why the refusal probes had to bend the **code** |
| figure exchanges | **847 of 847 fire** — 127 / 116 / 604, unchanged |
| on those 847 | `FIGURE ORDER` refuted **847**, `SITE RECORD` green **847**, `RECORD PARTITION` green **847** |

**No regression. Nothing here outranks the findings above, because there is nothing here.**

## THIS AUDIT, CHECKED FOR THE DEFECT IT AUDITS

Its predictions and its instrument are committed at `7cee1a1`, **before any transcript existed**,
re-derived from `git log` rather than asserted. Its own row identifications go through its own
heading parse — **1 substring comparison, and it is B3a measuring the substring test itself.**

And three of its six kept misses are its own defects, two of them the same shape as its findings:

- **The first version of B3 and B5c spliced each probe's patch onto the end of
  `verify_landing.py`, after `if __name__ == "__main__"` — so `main()` had already returned
  before a line of the probe ran.** Seven probes reported the artifact blessing a lossy record
  and a renamed anchor staying green. **A probe that never reaches the code it is probing reads
  exactly like a fact about the artifact**, which is F1 in this instrument. It was caught by the
  **control**: `B3d` must bless where `B3c` refuses, and both came out identical.
- **The first version of B7b reported 0 substring comparisons in a file that contains one**,
  because the classifier whitelisted a name it saw inside an assignment's *subscript*, where the
  name is read and not stored. **A check that clears its author** — corrected, with the reason in
  the source rather than in a story.
- **B4c predicted 6 and the first run printed 6** — for the wrong reason: my rule was counting
  the heading parse written inline as the defect. Corrected to 5. **A predicted number confirmed
  by a defect is worse than a miss**, and it is only in this table because the hits were re-read
  one by one.

## WHAT IS OPEN, FOR WHOEVER TAKES IT

1. **F1** — one line in `k_layout`: a markdown table's alignment is its cell padding. The matrix
   becomes 29 of 29 / 7 n/a, and the `n/a` reasons stop being able to say "this site has no such
   text" when they mean "this derivation has no such branch". *Ranked first because `n/a` is
   the only cell in that matrix that nobody has to justify.*
2. **F5** — one line in the sweep: derive `ROW_NAMES` from the gate instead of listing it.
3. **F2** — the population figure in the transcript is 19 short of its own tree. Whatever the
   convention is for a stale figure under a committed transcript, this arc has one, and this is
   an instance of it.
4. **F4** — either narrow the sentence to the matrix, or route `negative_control`'s remaining 19
   probes through `with_site()`, which the artifact now exports.
5. **F3** — 5 live instances, all dispositioned, 4 of them selecting 6 rows where 3 were meant.
   Two are other deliverables' shipped instruments under frozen transcripts; that is a real
   constraint and not an excuse, and it wants a ticket rather than a passing edit.
