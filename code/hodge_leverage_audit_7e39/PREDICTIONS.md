# mg-7e39 — predictions, written BEFORE the first run

Independent audit of the **mg-6df0 repair** (`77306a7`) of the **mg-ec07 verdict**.

Every verdict below was written before `audit_7e39.py` was executed once. This file and the
probe file are committed in **their own commit, before any transcript**, for the same reason
mg-ec07 asked mg-6df0 to commit its probes first: an ordering that is not in git is not
observable afterwards even when it was followed. `B7a` re-derives the ordering from `git log`
rather than asserting it here.

**Misses are kept as written**, with the reason underneath, in the table at the bottom. The
parent kept six, four of them its own instrument's defects, and that is the standard here.

## What is under audit, and what I read before predicting

I read `verify_landing.py`, `repair_ec07.py`, the repair's `README.md` and `PREDICTIONS.md`,
and the committed transcript `out_repair_6df0.txt`. So some rows below are **confirm/refute of
a published figure** rather than blind guesses, and each such row says so with ⟨inherited⟩.
Rows marked ⟨derived⟩ are numbers I worked out from the source myself before running, and rows
marked ⟨blind⟩ are ones where I have no published figure to lean on.

## B0 — preflight

| id | prediction |
|---|---|
| `B0a` | the runner on a clean tree: **exit 0**, 72 checks, **0 refuted** ⟨inherited⟩ |
| `B0b` | the figure gate returns **34 rows** ⟨derived: 3 sites × 4 census rows = 12, plus 12 `READ AT THE SITE` rows over the 12 (site, key) pairs, plus 10 `WRITTEN ONCE` rows — 10 because `copy` is the one non-live key and it occurs at 2 of the 3 sites … which gives 12+12+10 = 34⟩ |
| `B0c` | the three site files restore **sha256-identical** after every on-disk probe: **3 of 3**, every probe |

## B1 — THE MATRIX: SITES × KINDS, built by me

The parent's defect was an enumeration over **kinds** checked at **one site each**. The parent
repaired that with a 12 × 3 matrix of its own. **A matrix built by the party under audit is the
thing being audited, not the evidence for it**, so B1 builds the product again: my own
derivation for each of the 12 enumerated kinds, applied to **the file**, sites re-cut from the
file by **my own cutters**, and scored by running `verify_landing.py` **as a subprocess** —
exit code and refuted `GATE @` rows parsed from its stdout. Nothing is imported from the
artifact to decide a cell.

| id | prediction |
|---|---|
| `B1a` | **36 cells** attempted, 12 kinds × 3 sites, none skipped |
| `B1b` | **29 applicable, 29 FIRES, 0 SILENT, 7 n/a** ⟨derived⟩. That is **one more applicable cell than the artifact's own matrix reports** (28/8), and the extra cell is `K11 @ the STATE.md row` — see `B2` |
| `B1c` | every firing cell exits **1**; no mutated tree exits 0 |
| `B1d` | the label-side kinds (`K07`–`K11`) are caught by **SITE RECORD** with every `FIGURE CENSUS` and `FIGURE ORDER` row green, at **every applicable label-side cell** ⟨inherited: the artifact claims 8 of 8; I predict 9 of 9 on my matrix, the extra being `K11 @ the STATE.md row`⟩ |
| `B1e` | my matrix and the artifact's agree on **FIRES/SILENT at every cell both call applicable** — 28 of 28. The only disagreement is applicability, at 1 cell |

## B2 — the n/a cells: is the reason a fact about the SITE or about the DERIVATION?

**This is the item no list in my brief names, and it is my floor.** `n/a` is where a matrix
hides. The parent's own `PREDICTIONS.md` records that its first matrix reported **19**
applicable cells because a write-back was failing silently, and says in as many words that *a
derivation that fails silently reads exactly like a site that has no such text*. That miss was
repaired twice. B2 asks whether it is gone, by reading each of the 8 `n/a` reasons **as a claim
about the site** and trying to falsify it.

| id | prediction |
|---|---|
| `B2a` | of the artifact's **8** `n/a` cells, **7** are facts about the site and **1** is a fact about the derivation ⟨derived⟩ |
| `B2b` | the one is **`K11 @ the STATE.md row`** — *"no line here has two runs of two or more spaces to shift"*. The `STATE.md` site **is a table**; it is a markdown pipe table, and `k_layout` only recognises whitespace-aligned columns. `_table_lines` recognises both formats, `_header_line` recognises both, `k_layout` recognises one. So the cell reports the shape of the derivation in the grammar of a fact about the site |
| `B2c` | a markdown-aware alignment shift at that site **FIRES**, caught by `SITE RECORD`, `FIGURE CENSUS` and `FIGURE ORDER` green — i.e. the false `n/a` **understates coverage and hides no hole**. Runner **exit 1** |
| `B2d` | the other seven survive falsification: `K08 @ the STATE.md row` (one figure-carrying row inside the site — this is X2, declared open), `K08/K09/K11 @ §14` (§14 contains **no table of any format**: 0 pipe rows, 0 whitespace-column lines), `K10 @ the STATE.md row` and `K10 @ H8` (marked quotations present — 12 and 5 — but **none carries a figure**), `K12 @ the STATE.md row` (a 3-line site has no second paragraph) |

## B3 — the refusal, over all 34 rows, and each of the 3 that were excluded

| id | prediction |
|---|---|
| `B3a` | `"SITE RECORD"` as a **substring** selects **6 of 34** rows; as a **heading**, **3**. The 3 that differ are the `RECORD PARTITION` rows, one per site ⟨inherited⟩ |
| `B3b` | of the 34 rows, **31 BLOCK** a reseal when refuted and **3 are excluded by design** (the `SITE RECORD` rows, which are what a reseal exists to rewrite). Under the pre-repair substring test it was **28 block / 6 excluded** ⟨derived⟩ |
| `B3c` | **on disk, one site at a time.** `partition` bent lossy **at exactly one site**, so the only blocking row refuted is that site's `RECORD PARTITION`, then `--reseal`. **3 of 3 → exit 1, REFUSED**, `site_records.txt` sha256 **unchanged** ⟨blind at the per-site grain: the parent demonstrated this once, with all three sites bent together⟩ |
| `B3d` | **the control, at the commit where the defect is still present.** The same three probes against `verify_landing.py` and `site_records.txt` as of the commit before the repair: **3 of 3 → exit 0, BLESSED**, sha256 **CHANGED**. If the control does not bless, my probe is not reaching the defect |
| `B3e` | a wrong **live figure** is still refused after the repair: `--reseal` → **exit 1** at 3 of 3 sites. The half that already worked is not weakened ⟨inherited: the parent's R1d, at one site; I do it at three⟩ |

## B4 — the construct: how many exist, how many the repair touched

**Those two numbers are the finding.** The parent's own sweep is a line-based regex over a
**hand-written list of five row names**, requiring the right operand to be a bare identifier on
the same line. A hand list is a scope nobody chose, one level up, so mine derives its
vocabulary from **the live gate rows** and matches on the **AST** rather than on the line.

| id | prediction |
|---|---|
| `B4a` | `.py` files under `code/` at HEAD: **448**. The committed transcript publishes **429**. ⟨derived⟩ **19 files entered the population between the run and the commit that ships the transcript, and the number a reader meets was never re-derived.** This is mg-f922 B/C — a figure stale in the commit that publishes it — in the sweep whose whole argument is *the reported line is never the population* |
| `B4b` | re-running the parent's own sweep **now** reports **448** files and **4** hits, **0** undispositioned — i.e. the instrument is live and the transcript is stale, and none of the 19 unswept files holds the construct |
| `B4c` | **instances that exist, by my rule: 6.** ⟨blind — the parent's rule finds 4; mine adds the ones whose right operand is not a bare name and the ones whose row name is not on the hand list. I may be wrong in either direction and the number is the finding either way⟩ |
| `B4d` | **instances the repair touched: 1** — `reseal()`'s. ⟨derived from the diff⟩ |
| `B4e` | in `verify_landing.py` itself — *"`heading()` is now the only way any caller in that file names a row"* — **0** instances of the construct remain, and **every** row-identifying comparison in the file goes through `heading()` |
| `B4f` | files that are **not** `.py` and key on a gate row name by substring: **0** live ones ⟨blind⟩ |

## B5 — the scope sentences, each read as a claim, each tested at 3 of 3 sites

| id | sentence | prediction |
|---|---|---|
| `B5a` | `EXTENT_OF["section"]`: *the markdown SECTION, heading to the next heading of the same or shallower level — not the file that contains it* | **true at 2 of 2 sites it is claimed of** (§14, H8), re-derived by my own cutter |
| `B5b` | `EXTENT_OF["framed_row"]`: *the table ROW and the HEADER LINES it is read under — not the table's other rows* | **true at 1 of 1**, and the ledger's other rows are outside: `STATE.md` holds **24** ledger rows and the site holds **1** ⟨blind on 24⟩ |
| `B5c` | *a site whose anchor has no declared extent makes the run RED* | **falsifiable and it fires**: rename the cutting function so its `__name__` is not in `EXTENT_OF` → runner **exit 1** with the `DECLARED extent` row refuted |
| `B5d` | *a site is no longer a contiguous substring of its file at 1 of 3 sites* | **exactly 1 of 3**: the `STATE.md` site occurs **0** times in `STATE.md`; §14 and H8 occur **1** time each |
| `B5e` | *the record grows by 43 characters, 37 866 → 37 909* | **+43**, and the `site_records.txt` diff at the repair commit is **exactly 2 added lines** ⟨inherited⟩ |
| `B5f` | *282 600 of 320 509 characters (88.2%) are outside every record* | re-derived **identically**, to the character |
| `B5g` | *every mutation goes through the FILE and the sites are re-cut from it* | true of `kind_matrix`; **false of the rest of `negative_control`**, which still mutates site **texts** in place ⟨derived from reading: the `corrupt`/`prose`/`duplicate` probes at lines 2186–2240 call `figure_gate` on mutated text dicts⟩. The claim is scoped to the matrix in the source and to *the negative control* in the commit message; I predict the commit message's version is the wider one |

## B6 — do not disturb what is confirmed

| id | prediction |
|---|---|
| `B6a` | every character of every site substituted alone, at HEAD: **37 909 of 37 909 fire**. The population **grew by 43** from mg-ec07's 37 866 — that is the repair's declared effect and not a regression, and reporting it as `37 866` would be the stale figure one level up |
| `B6b` | the same instrument against the gate at the pre-`c7f9079` commit: **462 of 37 909** ⟨derived: mg-ec07 measured 462 of 37 866; the 43 new characters are a markdown header and delimiter line carrying no figure token, and the pre-repair gate catches only figure-row breaks, so it catches **0** of the 43 and the count does not move⟩. **1.2%** |
| `B6c` | `RECORD PARTITION` fires on **0 of 37 909** point mutations — unfalsifiable by any document edit, exactly as mg-ec07 said ⟨inherited⟩ |
| `B6d` | every unordered pair of asserted figure slots with differing values, exchanged: **847 of 847 fire** — 127 / 116 / 604 over the three sites, unchanged, because the two lines the site gained carry no figure token ⟨inherited on 847, derived on *unchanged*⟩ |
| `B6e` | on those 847: `FIGURE ORDER` refuted **847 of 847**, `SITE RECORD` green **847 of 847**, `RECORD PARTITION` green **847 of 847** |
| `B6f` | **any regression in B6 outranks every finding above.** I predict **none** |

## B7 — this deliverable, checked for the defect it audits

| id | prediction |
|---|---|
| `B7a` | this file and `audit_7e39.py` **precede** the transcript in git, re-derived from `git log` |
| `B7b` | my own report states **no total without naming its population**, checked mechanically: every figure in my report's tables carries an "of N" or a named denominator |
| `B7c` | my own instrument contains the construct it hunts **0 times outside a declared measurement of it** |

## What I expect to be wrong

Written in advance, because a predictions file with no exposure is a formality.

- **`B4c`'s 6.** I am guessing how many occurrences an AST rule finds that a line regex does
  not. If it lands at 4 my rule adds nothing and that is the honest result; if it lands above 8
  I will have counted something that is not the construct.
- **`B2a`'s 7-of-8.** I have read the eight reasons and checked the site texts for the
  structures they deny, but only by eye. A second false `n/a` would not surprise me, and would
  be the better finding.
- **`B3d`.** I do not know that the pre-repair reseal blesses when only **one** site's
  `RECORD PARTITION` is refuted; the parent bent all three together. If the pre-repair state
  refuses, my per-site bend is reaching a row I did not intend.
- **`B1b`'s 29.** My derivations are mine, so a cell the artifact calls applicable and mine
  cannot derive is a defect in **my** instrument, and I will report it as one.

---

# The misses, kept as written

Filled in after the runs. Nothing above was edited.

| id | predicted | observed | what the miss was |
|---|---|---|---|
| `B3c` / `B3d` / `B5c` (first run) | `B3c` refuses at HEAD, `B3d` blesses at the pre-repair commit, `B5c` goes red | **all seven probes said the opposite**: `--reseal` BLESSED a lossy record at HEAD with the record unchanged, the control at the pre-repair commit also blessed but changed nothing, and a renamed anchor left the run green | **my instrument's own defect, and the largest thing in this file.** I spliced each probe's patch onto the END of `verify_landing.py`, after its `if __name__ == "__main__": sys.exit(main())` — so `main()` had already run and returned before a single line of the probe was executed. A probe that never reaches the code it is probing produces output that reads exactly like a fact about the artifact. **That is B2's finding, in this instrument.** What caught it was the CONTROL: I had predicted that `B3d` must bless where `B3c` refuses, and both came out identical, which is the one shape a real result could not have. A probe with no control would have shipped "the repaired refusal blesses a lossy record" as a finding |
| `B7b` (first run) | this instrument contains the construct only where it declares it is measuring it | **0 substring comparisons reported, in a file that contains at least one** | my classifier collected "names bound from a heading parse" by walking assignment TARGETS for `Name` nodes — and `kinds[row_kind(d)] = ...` has `d` *inside the subscript*, where it is READ, not stored. So `d` was whitelisted and my own `"SITE RECORD" in d` was exonerated. **A check that clears its author is this arc's own defect**; the fix is `isinstance(n.ctx, ast.Store)` and the comment is kept in the source rather than the story |
| `B4c` | **6** instances of the construct exist by my rule | **5** — and my first run did print 6 | the sixth was `audit_ec07.py:716`, `r.split(" -- ")[0].endswith("SITE RECORD")` — the heading parse **written inline** rather than called. That is the remedy spelled out, not the defect, and my rule was calling it a hit. **The predicted number was right for a reason that was wrong**, which is worse than a miss: had I not re-read the hits one by one, 6 would have gone into the report as a confirmation |
| `B4a` | **448** `.py` files under `code/` at HEAD | **449** at HEAD, 448 at the commit the repair ships in | this audit's own probe file joined the population it counts, between the prediction and the run. The finding is unaffected — it is stated against the repair's own commit, where the count is 448 against a published 429 — but the census reading its own author in is mg-ec07's `B0` and it happened here too, and the row now names all three trees |
| `B0c` | a printed row saying the three site files restore 3 of 3 | **no such row exists** | the restore is enforced FAIL-CLOSED after every probe and again at the end — a failed restore is `SystemExit` or exit 2, never a recorded check. I predicted a check that a stronger design does not have. Kept because "predicted a row, built a refusal instead" is worth more than a quietly renumbered id |
| `B5b` | **24** ledger rows in `STATE.md` | **24** header-or-verdict lines in the row's own table (25 with the delimiter), **22** verdict rows outside the site | the blind guess landed on the right number for a slightly different object. The 22 matches the repair's own declared X2 cost |

**Six misses, three of them this instrument's own defects, and two of those the same shape as
the findings this audit makes** — a probe whose silent failure reads as a fact about the subject
(`B3c`), and a check whose scope quietly exonerates its author (`B7b`). Both were caught by rows
that compare a number against a second way of getting it, which is the only reason they are in
this table rather than in the next audit.
