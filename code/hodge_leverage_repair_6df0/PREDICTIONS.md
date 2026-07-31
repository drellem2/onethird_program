# mg-6df0 — predictions, written BEFORE the first run

Every verdict below was written before `repair_ec07.py` was executed once, and **before**
`verify_landing.py` was touched. Misses are kept as written, with the reason underneath — a
prediction edited after the run is not a prediction.

**And the probes are committed BEFORE the fix.** mg-ec07's closing note on its parent is that
*"enumerate before fixing" is not evidenced by the repository — 0 of 7 probes exist at any commit
before the commit that lands the fix*. So this deliverable's probe file and this predictions file
are committed in their own commit, against the **unrepaired** artifact, with the transcript of
that run committed beside them. `R6` re-derives that ordering from git rather than asserting it
here.

## The two states this instrument is run in

| state | what is on disk |
|---|---|
| **PRE** | `verify_landing.py` as merged at `8cdda32` — the substring refusal, the one-line `STATE.md` site, the kind-per-site battery |
| **POST** | the same file with this repair applied |

Rows below give the prediction for each state where they differ.

## R1 — the refusal, keyed on the row's HEADING (mg-ec07 E-5, and OPEN 3's control)

| id | prediction |
|---|---|
| `R1a` | of the **34** gate rows, **6** contain the string `SITE RECORD` anywhere and **3** have a HEADING that ends with it. The 3 that differ are the `RECORD PARTITION` rows, one per site. Identical in PRE and POST — this is a property of the row *texts*, which the repair deliberately does not change |
| `R1b` | `partition` bent lossy (mg-ec07's B2 shape), then `--reseal`. **PRE: exit 0, BLESSED**, `site_records.txt` sha256 CHANGES. **POST: exit 1, REFUSED**, sha256 unchanged |
| `R1c` | **the control, at the finest unit.** POST source with the refusal reverted to `"SITE RECORD" not in d` and nothing else changed → **exit 0, BLESSED again**. If this does not go back to blessing, the fix is not what is doing the work. In PRE the revert has nothing to revert and is reported `NOT APPLIED` |
| `R1d` | a wrong LIVE FIGURE, `--reseal` → **exit 1, REFUSED in both states**. The repair must not weaken the refusal that already worked (mg-ec07 B1) |
| `R1e` | the runner's own exit code and refuted-row count are unchanged by R1's probes after restoration: **exit 0, 0 refuted**, and every mutated file restored sha256-identical |

## R2 — the sweep: every occurrence of the construct, from the tree

`R2` is the answer to *a fix with a scope nobody chose*. It greps the **tree**, not this author's
memory.

| id | prediction |
|---|---|
| `R2a` | live `.py` files under `code/` that identify a gate row by a **substring test over the whole row**: **PRE 1** (`verify_landing.py`'s `reseal`), **POST 0** undispositioned. Every remaining hit carries a declared disposition keyed on its exact line, so a new occurrence anywhere fires |
| `R2b` | the sentence *"a site is a section"* in **live instrument source**: **PRE 3** in `verify_landing.py` (two comments and one printed line) + **1** in `repair_9207.py`. **POST: 0 in `verify_landing.py`**, and `repair_9207.py`'s is dispositioned as a shipped transcript's prose, corrected in its own report rather than edited under its transcript |
| `R2c` | `verify_landing.py`'s `section()` docstring says *"A SITE IS A SECTION, NOT THE FILE THAT CONTAINS IT"* about `section()` itself. That one is **true of the function it documents** and is kept — dispositioned, not repaired |

## R3 — the enumeration at the right grain: SITES × KINDS (mg-ec07 E-4)

| id | prediction |
|---|---|
| `R3a` | the runner prints a **matrix**, not a total: every one of its declared KINDS attempted at every one of the 3 SITES. **POST: 36 cells** (12 kinds × 3 sites), 0 missing. PRE: no matrix exists and the row reads `NOT PRESENT` |
| `R3b` | every **applicable** cell FIRES. I do not know the applicable count in advance; I predict **between 24 and 33** of 36, the rest `n/a` with a derived reason (no table at §14; no marked quotation at the `STATE.md` row; no paragraph structure in a one-line row) |
| `R3c` | the label-side kinds are caught **by `SITE RECORD` with every figure row green**, at every applicable cell — mg-ff3e's attribution claim, at the product rather than at one cell per row |
| `R3d` | **X1 on disk** (the two COLUMN HEADERS of `STATE.md`'s ledger table exchanged, the mutation mg-ec07 measured at exit 0): **PRE exit 0, 0 refuted. POST exit 1**, with `SITE RECORD @ the STATE.md row` refuted and every FIGURE row green |
| `R3e` | **X3 on disk** (the same kind at H8, inside a site): **exit 1 in both states**. It is the discrimination control; if it moved, X1's move would be my probe rather than the repair |
| `R3f` | **X2 on disk** (the verdict labels of two ledger rows that are *not* the site's row): **exit 0 in both states — still silent, and declared.** Covering it means freezing the whole 24-row ledger table; the cost is measured here and the decision is pm-onethird's, not this repair's |
| `R3g` | the `STATE.md` site is **3 lines** POST (the two header lines and the row) against 1 line PRE, and the byte population of the three records grows from **37 866** to **37 866 + 42** = 37 908 characters. If the site record does not grow by exactly the header's length, the frame is not what I think it is |

## R4 — the instrument that raised it, re-run unmodified

| id | prediction |
|---|---|
| `R4a` | `audit_ec07.py` re-run, no edits: **E-1 is NOT emitted** (X1 is no longer silent) |
| `R4b` | **E-5 IS still emitted.** Its condition is `unintended`, a property of the ROW TEXTS, and this repair keys the refusal on the heading rather than rewriting the rows' explanations. Its `A7-B2` row — the *behavioural* one — moves from exit 0 to **exit 1**. I predict this before running it because it would otherwise read as the repair failing |
| `R4c` | **E-2 IS still emitted**: `finding("E-2", …)` is called unconditionally in `a6()`. What moves is its `A6` rows — the `said` row goes **REFUTED**, because the sentence it looks for is gone |
| `R4d` | `A1`'s byte census grows to the new population and stays **all of it** — every character of every site still fires |
| `R4e` | the audit's own exit code stays **1**: it raises findings, and two of its six are emitted unconditionally or from row text. An audit that went green would mean I had edited it |

## R5 — the extent, derived rather than written (mg-ec07 E-2)

| id | prediction |
|---|---|
| `R5a` | the runner prints, per site, **what that site is** — the name of the function that produced it, its line and character count, and the characters of its file outside it — and every number matches this instrument's independent re-measurement |
| `R5b` | **88.2%** of the three files was outside every record before; POST it is **88.2%** still, to one decimal. 42 characters do not move a ratio over 320 509. The repair closes a *kind*, not the residue, and saying otherwise would be the same defect one level up |
| `R5c` | every site's anchor function has a **declared extent sentence**, and a site whose anchor has none makes the run RED. This is the structural half: the sentence is keyed to the code's own function name, so a new site cannot inherit a false one |

## R6 — this deliverable, checked for the defect it repairs

| id | prediction |
|---|---|
| `R6a` | **the probes precede the fix, in git**: the first commit containing `repair_ec07.py` does NOT contain the heading-keyed refusal. Measured from `git log`, not asserted |
| `R6b` | every comparison in **this** instrument that identifies a gate row does so by `heading()`, enumerated with the reason, and the one place that deliberately uses a substring is `R1a`'s measurement of the substring test itself — declared, because it is measuring the defect and not committing it |
| `R6c` | every scope sentence this deliverable writes is checked at **all three sites**, not at the site it was written for. `R5a` is that check |

## What I expect to be wrong

Written in advance, because a predictions file with no exposure is a formality:

- **`R3b`'s range.** I am guessing at how many derived kinds apply at a one-line site. If it lands
  outside 24–33 the miss is the guess, not the matrix.
- **`R3g`'s 42.** The frame may need a joining newline that the record counts.
- **`R4`'s row-by-row account.** I have read `audit_ec07.py` but not run it against a repaired
  tree; the rows that move may be a superset of the four above.
