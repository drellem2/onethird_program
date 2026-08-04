# mg-65eb — PREDICTIONS, COMMITTED BEFORE ANY SCRIPT OF THIS AUDIT EXISTS

This is the INDEPENDENT AUDIT of mg-a74f, the repair of mg-16eb's three OPENs on mg-0049.
The parent is **merged** and is not re-done here. Every figure below is written before any
`.py` or `.sh` in `code/state_visibility_audit_65eb/` exists, and every one is scored in
`README.md` with the misses kept as written.

## What was probed BEFORE this file was written, and it is disclosed rather than hidden

mg-a74f disclosed one probed row (`V1`) and this audit owes the same. Four things were run
before this file existed, all of them by hand at a `python3 -` prompt or a `git` command,
none of them by a script in this directory:

1. `visible_a74f.suppressors()` called directly on three hand-written HTML documents
   (`class="hidden"`, `<details title="open me">`, and an entity-prefixed `<div hidden>`).
   The three results in rows R2a/R2b/R2c below are therefore **observations, not
   predictions**, and are marked `← probed`.
2. `git cat-file -t` / `git merge-base --is-ancestor` on the six shas named in the prose of
   `code/state_delegation_repair_a74f/` and `code/state_delegation_repair_0049/`. Row A1's
   verdict is therefore **probed** and is marked so.
3. `grep` for `section N` references in mg-a74f's three declared directories, and a read of
   `code/state_delegation_repair_0049/README.md:165` at `bd24efc` and at the tree. Row
   S5b is **probed**.
4. `git ls-tree cfd2af5` over mg-a74f's own directory.

**Everything else in this file is written before the fact**, including every figure in the
end-to-end renderer constructions (R1, R2c through two real GFM renderers), every row of the
population-gap constructions (R4–R7), every classification in section 3, every exit code in
section 5, and every figure in section 4.

---

## 1. The primary target: property CLAIMED beside quantity COMPUTED, for every row

mg-a74f publishes **nine rows** (`claims_a74f.py`, "EVERY INSTRUMENT THIS REPAIR ADDS, AND
WHETHER ITS ROW NAME IS ITS MEASUREMENT"): eight `MATCHES` and one `DOES NOT MATCH,
deliberately`. This audit takes that table as the thing under test and, for each row, writes
the property the row NAMES beside the quantity the code COMPUTES and tries to **construct a
document or a tree that separates them**. A row that cannot be separated is reported as
NOT SEPARATED with the reason.

**Predicted headline: 4 of the 9 rows mg-a74f publishes as `MATCHES` are separable, and
three of the four separations are in `visible_a74f.py` — the instrument the repair built to
answer OPEN 1.**

| row | property CLAIMED | quantity COMPUTED | predicted |
|---|---|---|---|
| R1 `visible_a74f` `bytes-in-html` | the section marker is present in the serialised HTML | the marker is present in `html.unescape(out)` | **SEPARABLE** — a target whose marker is written `H1 &mdash; ` renders to HTML with no such bytes and is scored `bytes-in-html 5/5` on both engines |
| R2a `visible_a74f` `not-suppressed` / S4 | not inside an element carrying the `hidden` **attribute** | some ancestor's attribute text matches `hidden` as a word — `class="hidden"` matches | **SEPARABLE, and it fails CLOSED** ← probed |
| R2b `visible_a74f` `not-suppressed` / S1 | not inside a `<details>` carrying no `open` attribute | that `<details>`'s attribute text contains no `open` word — `title="open me"` counts as `open` | **SEPARABLE** ← probed |
| R2c `visible_a74f` `not-suppressed` / offset | the mechanisms suppressing **the marker's position** | the mechanisms suppressing an offset taken in the UNESCAPED string and spent in the ESCAPED one | **SEPARABLE** ← probed at the function; predicted to survive both real renderers |
| R3 `visible_a74f` `r16 SHOWN` | mg-16eb's rule under mg-16eb's name | exactly that | NOT SEPARABLE — and mg-a74f already reports this row as `DOES NOT MATCH` |
| R4 `prose_a74f` P1 | every repo-relative path named in the text exists **at the revision being read** | on the working tree, existence is `os.path.exists` over the whole working directory — untracked and ignored files included | **SEPARABLE** |
| R5 `prose_a74f` P2 | every `section N` reference **to a run_all.sh** resolves | every `section N` on a line that ALSO contains the literal `run_all.sh`, or the literal `re-run in section` | **SEPARABLE** |
| R6 `prose_a74f` P3 | every module-level dict of `delta_control.py` **keyed by repo paths** is iterated | every module-level dict **all** of whose keys match `^(code\|docs)/` and contain a `.` | **SEPARABLE** — one non-path key removes the table from the population |
| R7 `prose_a74f` P4 | the number equals **that script's** own `ROWS` | the number equals the `ROWS` of the nearest `.py` basename in the preceding 400 characters | **SEPARABLE** |
| R8 `battery_a74f` exit codes | read from the process by `harness16eb.Tree` | exactly that | NOT SEPARABLE |
| R9 `claims_a74f` before/after | a text or AST predicate over the two revisions | exactly that, except that "the tree" is the working directory | NOT SEPARABLE as named (the row says "the tree"); the untracked-file case of R4 moves `in_tree(None, …)` too and is reported beside it |

Predicted: **4 SEPARATED (R1, R2, R4–R7 counted as four rows: R1, R2, R4, R5, R6, R7 — six
separations over five published rows), 3 NOT SEPARATED (R3, R8, R9), 0 rows where the
construction is impossible to state.**

To be precise about the arithmetic, because a bare total is what this arc keeps refusing:
the population is **9 published rows**. Predicted **6 separated** (R1, R2, R4, R5, R6, R7 —
where R2 is one published row separated three different ways), **3 not separated** (R3, R8,
R9). R3 is not separated because mg-a74f already declares it a mismatch.

## 2. The direction of the error, which is the parent's own safety argument

`visible_a74f.py`'s docstring and mg-a74f's `README.md` both say the instrument **FAILS
OPEN**: "a suppression mechanism outside the set is scored NOT SUPPRESSED". That
one-directional claim is the whole of why the column may be trusted.

**Predicted: R2a refutes it.** `class="hidden"` is a mechanism outside the declared set —
`NOT_COVERED` names "any rule from an external or embedded stylesheet, including
`display:none` on a class" explicitly — and it is scored **SUPPRESSED**, not NOT SUPPRESSED.
A document with no stylesheet at all shows that text to a reader and the instrument says a
mechanism suppressed it. That is a failure in the **closed** direction, in the row whose
declared failure mode is open-only.

## 3. The six claims, re-classified from scratch

Predicted: **this audit's independent classification agrees with mg-a74f's on all six** —
5 FALSE and 1 TRUE OF A DIFFERENT PROPERTY, 0 UNSUPPORTED, 0 TRUE-BUT-UNEVIDENCED — and
finds **no downgrade**: no claim mg-16eb refuted is parked in a softer bucket than it
deserves. The specific hazard the brief names (a false claim relabelled "unsupported") is
predicted **absent**, because both soft buckets are empty.

Predicted secondary findings on the six:

- **S5a**: claim 5's repair (README rows 105–106, "section 7" → "section 8") is predicted
  **sound**: mg-0049's `run_all.sh` section 8 runs mg-5644's whole suite and mg-5644's own
  section 5 is mg-218d's sixteen, so both rows are true as rewritten.
- **S5b** ← probed: `code/state_delegation_repair_0049/README.md:165` says "section 7's
  re-runs mutate tracked files" at `bd24efc` **and at the tree** — the repair did not touch
  it. Predicted verdict: **REFUTED as a seventh broken claim.** Section 7 re-runs
  `coverage218d.py`, which does mutate tracked files through `harness218d.Tree`, so the
  sentence is defensible and this audit reports its own candidate as refuted rather than
  banking it. **What survives is the population finding**: that line is a `section N`
  reference in a file `prose_a74f.py` walks, and P2 never looks at it (row R5).

## 4. Do not disturb what is confirmed

mg-16eb's confirmed figures are **7 of 7 committed outputs byte-identical** and **8 of 8
rows as predicted**. Both moved under mg-a74f. Predicted, re-measured here from scratch:

| figure | mg-16eb | predicted now | predicted verdict |
|---|---|---|---|
| `reproduce16eb.py` on the tree | 7 of 7 | **5 of 7** | NOT a regression of this repair |
| the same at `bd24efc`, in a throwaway worktree | — | **5 of 7, the same two** | the staleness predates `bd24efc` |
| the two that differ | — | `out_coverage218d.txt`, `out_selftest_negative.txt` | cause: `STATE.md` grew |
| `battery16eb.py` (mg-16eb's own words) | 8 of 8 | **6 of 8; A1 and A2 named** | that line IS the repair |
| `battery_a74f.py` section 2 | — | **8 of 8 against mg-a74f's predictions** | no surprise |
| A1, A2 exit code | 0 | **2 (MOVED)** | correct classification — an inconsistency between two pinned tables is drift in the record, not damage in the target; `kind=MOVED` is argued in `delta_control.py`'s own comment |
| B3, C1 | 2, 1 | **2, 1 unchanged** | deliberate and pre-filed |

Additionally predicted, and re-derived rather than read: **`STATE.md` at `bd24efc` is
already larger than the size `out_selftest_negative.txt` records**, which is the measurement
that separates "this repair broke it" from "it was already stale". Predicted: the recorded
figure is 177464 bytes and the figure at `bd24efc` is larger.

**Predicted regressions attributable to mg-a74f: NONE.**

## 5. The floor — one thing no list in the brief names: THE ANCHORS THIS REPAIR SPENDS

The brief names rows, claims, surfaces and a re-run. It does not name **the revisions the
repair pins its own integrity claim to**. mg-a74f's central integrity claim is
"`PREDICTIONS.md` was committed before any script in this directory existed (`739f7bd`)".

- **A1** ← probed: `739f7bd` **resolves** as a commit and **is not an ancestor of `HEAD`**.
  It is the pre-rebase copy of `cfd2af5`, reachable only from the leftover branch
  `polecat-a74f`. Predicted verdict: **the property is TRUE and the anchor is STALE** —
  verified independently at `cfd2af5`, whose tree under `code/state_delegation_repair_a74f/`
  holds `PREDICTIONS.md` and nothing else.
- **A2**: predicted — `bd24efc` (mg-a74f's pinned pre-repair revision) and `8ce78fb`
  (mg-0049's baseline) **are** ancestors of `HEAD` and resolve.
- **A3**: predicted — **no checker anywhere in the three declared directories resolves a
  single sha.** `prose_a74f.py` checks paths, sections, tables and counts; shas are not one
  of its four shapes. Predicted count of sha references checked by any program: **0**.
- **A4**: predicted — a `git cat-file -e` style check would pass `739f7bd` today and is the
  wrong instrument; ancestry, not existence, is the property the sentence needs.

## 6. The third question: the surface, and the single point of failure

Predicted: the surface this repair lays is `visible_a74f.py`'s **declared suppression set**,
and **one claim is now verifiable only through it**. `render0049.py`'s R5 was narrowed from
"SUPPRESSES NOTHING" to "the text is in the page" and now **points at `visible_a74f.py`** for
the suppression question; `render16eb.py`'s `SHOWN` column is demonstrated wrong by that same
file. So after this repair, *nothing else in the repository measures suppression at all*.

Predicted verdict: **that is a single point of failure the repair introduced, and it is not
merely theoretical** — rows R2a/R2b/R2c are three defects in the only instrument that
measures it, and no other instrument in the repository would contradict any of them.

## 7. Predicted exit codes — every one of them, before any of it runs

| # | command | predicted exit |
|---|---|---|
| 0 | `git diff HEAD --stat` over the three audited directories | empty (0 bytes) |
| 1 | `rows65eb.py` — the row ledger and its constructions | **1** (a separation exists at HEAD; the defect is present at the commit the control is demonstrated on) |
| 2 | `anchor65eb.py` — the shas this repair spends | **1** (`739f7bd` is not an ancestor of `HEAD`) |
| 3 | `six65eb.py` — the six, re-classified | **0** (no disagreement with mg-a74f, no downgrade) |
| 4 | `rerun65eb.py` — the confirmed figures re-measured | **0** (the two revisions agree on which transcripts reproduce) |
| 5 | `python3 …/delta_control.py` | **0** |
| 6 | `python3 …/prose_a74f.py` (tree) | **0** |
| 7 | `python3 …/prose_a74f.py --rev bd24efc` | **1** (4 findings) |
| 8 | `python3 …/visible_a74f.py` | **0** |
| 9 | `python3 …/claims_a74f.py` | **0** |
| 10 | `python3 …/battery_a74f.py` | **0** |
| 11 | `python3 …/battery16eb.py` (inside section 10) | **0** — it returns 0 unconditionally even with 2 surprises |
| 12 | `python3 …/reproduce16eb.py` | **non-zero** (5 of 7) |

**A prediction this audit expects to be wrong somewhere.** If every one of the twelve lands,
that is itself worth saying, because four consecutive zero-finding verdicts in this arc were
read as a signal and not as convergence.

## 8. What this audit will NOT do

- It will not repair anything in `code/state_delegation_repair_a74f/`,
  `code/state_delegation_repair_0049/`, `code/state_landing_control_2da3/` or
  `code/state_delegation_audit_16eb/`. **`git diff` over all four is predicted 0 bytes** at
  the end of the run, and section 0 prints it.
- It will not re-litigate mg-16eb's verdict or mg-a74f's OPEN-2 classification, both of
  which are predicted to stand.
- Its constructions against the tree (R4, R6) mutate tracked files and are applied under a
  snapshot-and-`finally` restore with a post-restore sha check, or in a throwaway
  worktree. **Predicted: the tree is byte-identical after the run.**
