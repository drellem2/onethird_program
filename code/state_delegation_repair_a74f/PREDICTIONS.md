# mg-a74f — PREDICTIONS, committed before any script of this repair exists

This file is committed **before** `visible_a74f.py`, `prose_a74f.py`, `battery_a74f.py` and
`claims_a74f.py` exist and before any repair is applied. Every number below is what this
repair expects to observe. Where a number turns out wrong the row is kept and the miss is
printed, because a prediction that is quietly corrected after the run is not a prediction.

Pre-repair revision: **`bd24efc`** — the tree this branch starts from. Every "before" figure
below is a figure at `bd24efc`; every "after" figure is at this repair's own HEAD.

The three OPENs this repair answers are mg-16eb's, filed as mg-a74f:

* **OPEN 1** — the visibility instrument measures bytes in the HTML and calls it what a
  reader is shown.
* **OPEN 2** — 6 of the 17 claims mg-0049 added do not hold; enumerate them individually,
  say of each whether it is false, unsupported or true-but-unevidenced, and repair each
  according to its class.
* **OPEN 3** — the blind spot moved three times, every time onto ground the repair itself
  laid. Name the surface *this* repair creates and say what is now measurable only through
  it.

---

## DISCLOSURE — what was probed before this file was written

One row was probed in a scratch directory before these predictions were written, and saying
so is the point of the disclosure: **V1**, below. Nothing else in this file was run. The
probe was `render16eb.py`'s own `visible_text` / `closed_details_ancestors` applied to
`mutations_0049.r8_whole_file_commented_closed`, and it is disclosed rather than presented
as a prediction because it is the finding this repair is built on and a reader is entitled to
know it was seen first.

Rows **V0, V2, V3, V4**, every row of `prose_a74f.py`, every row of `battery_a74f.py` and
every row of `claims_a74f.py` are predicted here unrun.

---

## 1. `visible_a74f.py` — the visibility instrument, repaired

Five documents on two independent GFM renderers (`marked`, `markdown-it`), five cited
sections each: **50 section observations**. Three numbers per row:

* `bytes-in-html` — the section's text is present in the serialised HTML. This is the
  property mg-0049's `render0049.py` and mg-16eb's `render16eb.py` both actually measure.
* `not-suppressed` — the section is not suppressed by any mechanism in this instrument's
  **declared set**, printed on every run. This instrument never says "shown to a reader".
* `render16eb SHOWN` — mg-16eb's own rule, computed by importing `render16eb.py` unmodified
  and applying its own two functions, so the disagreement is measured and not argued.

| row | document | bytes-in-html | not-suppressed | render16eb SHOWN |
|---|---|---|---|---|
| V0 | unmutated — positive control | 5/5 | 5/5 | 5/5 |
| V1 | the whole file inside a CLOSED HTML comment (mg-0049's R8) | 5/5 | **0/5** | **5/5** ← probed |
| V2 | `<details><summary>` at the top, never closed (mg-16eb's B3) | 5/5 | 0/5 | 0/5 |
| V3 | `<div hidden>` at the top, never closed | 5/5 | **0/5** | **5/5** |
| V4 | `<div style="display:none">` at the top, never closed | 5/5 | **0/5** | **5/5** |

**Predicted headline: on 3 of the 5 documents (V1, V3, V4) mg-16eb's rule reports every cited
section SHOWN TO A READER and no reader is shown any of them.** V1 is the sharpest, because
mg-0049's own `render0049.py` scores that same document `ANY 0/5` and `delta_control.py`
exits 1 on it calling it damage: the auditor's replacement instrument scores 5/5 the page
both earlier instruments agree is blank.

Predicted agreement between the two instruments: **2 of 5 documents** (V0, V2).

## 2. `prose_a74f.py` — an external checker for prose claims, run at both revisions

Population: every `.py`, `.md` and `.sh` in `code/state_landing_control_2da3/`,
`code/state_delegation_repair_0049/` and `code/state_delegation_repair_a74f/`, walked from a
named revision. The population size is **computed and printed**, never a hand list.

Two shapes are checked, and only two:

* **P1** every repo-relative path named in the text exists at that revision;
* **P2** every "section *N* of `run_all.sh`" reference resolves to a section of that
  `run_all.sh` whose echoed title names the thing the reference names.

Predicted:

| | at `bd24efc` | at this repair's HEAD |
|---|---|---|
| P1 path references that do not exist | **1** (`guards_only_0049.py`) | **0** |
| P2 section references that name the wrong section | **2** (both rows of mg-0049's README:105-106) | **0** |

If either "before" count is larger than predicted, the extra findings are kept and reported:
that would be a fact about the population, not about the repair, and this repair does not get
to shrink the population to match its prediction.

Third shape, predicted 0 at both revisions and included so a later table cannot slip in
unchecked: **P3** — the set of module-level dicts in `delta_control.py` keyed by repo paths
is exactly `{DELEGATED, DELEGATED_PRESENTATION}`, both of which section 2c cross-checks after
this repair. A third such table appearing later is a **fail**, not a silent pass.

## 3. `battery_a74f.py` — mg-16eb's own eight rows, on mg-16eb's own harness, unmodified

`harness16eb.py` and `mutations16eb.py` are imported unchanged. The predicted exit codes
inside `mutations16eb.py` are the auditor's, not this repair's, and they are left alone.

| row | mg-16eb predicted & observed at `bd24efc` | predicted here, after this repair |
|---|---|---|
| A1 a presentation record for a section nothing cites | 0 | **2** |
| A2 a whole TARGET FILE certified there and delegated by nobody | 0 | **2** |
| A3 a delegated section's presentation record DELETED | 2 | 2 |
| A5 a delegated section's CONTENT digest deleted (mg-bee1's table) | 2 | 2 |
| B1 two cited sections EXCHANGED | 0 | 0 |
| B2 one cited section moved under a different parent | 2 | 2 |
| B3 `<details><summary>` at the top | 2 | **2 — deliberately unchanged** |
| C1 an ordinary CODE EXAMPLE inside a cited section | 1 | **1 — deliberately unchanged** |

So mg-16eb's battery is predicted to print **"6 of 8 behaved as this audit predicted; 2 did
not"**, naming A1 and A2. That line is the repair, reported by the auditor's own instrument
with not a byte of it edited.

**B3 and C1 are predicted unchanged on purpose and this is not a dodge.** Both are refutations
of what `delta_control.py`'s exit-code table *says*, in opposite directions: B3 under-fires
(nobody is shown anything, exit 2 = drift) and C1 over-fires (the reader is shown every line,
exit 1 = "SHOWN NOTHING OF IT"). This repair narrows the sentence to the property the code
measures and prints both counterexamples beside it, rather than changing `is_presented()` —
which would move the classification of every delegated section and is a different ticket.
Predicted consequence, stated in advance: **anyone reading the narrowed sentence learns that
the instrument does not measure what a reader is shown, and B3 and C1 stay exactly as
mg-16eb found them.**

## 4. `claims_a74f.py` — the six, individually, classified, checked at both revisions

Predicted classification. mg-16eb asked for three buckets — false, unsupported,
true-but-unevidenced — and the predicted answer uses one of them and one it did not name:

| # | claim | predicted class | predicted repair |
|---|---|---|---|
| 1 | `delta_control.py:233` — the decomposition lives in `guards_only_0049.py` | **false** | correct the path to `split_0049.py` |
| 2 | `delta_control.py:234` — it runs against "all six rows" | **false** | correct the count to nine |
| 3 | `delta_control.py:798` — "the two tables cannot drift apart quietly in either direction" | **false** | **implement the missing direction** — make the sentence true |
| 4 | `delta_control.py:346` — exit 1 is "a region … NO LONGER PRESENTED TO A READER" | **false**, refuted in both directions | **narrow** to the measured property and name B3 and C1 beside it |
| 5 | mg-0049 `README.md:105-106` — the two batteries are "re-run in section 7 of `run_all.sh`" | **false** | correct the pointer to section 8 |
| 6 | `render0049.py:11` — R5 "`<details>` at the top SUPPRESSES NOTHING" | **true of a different property** — true of bytes in the HTML, false of what a reader is shown | **narrow** the wording to the measured property |

Predicted totals: **5 false, 1 true-of-a-different-property, 0 unsupported, 0
true-but-unevidenced.** Predicted checks: 6 of 6 defects present at `bd24efc`, 6 of 6 repaired
at HEAD.

## 5. The committed evidence that moves

This repair edits `delta_control.py`, `render0049.py` and mg-0049's `README.md`, so some of
the seven `out_*.txt` mg-16eb reproduced byte-for-byte will no longer reproduce against
mg-16eb's **committed** transcript. Predicted, before running:

* `code/state_landing_control_2da3/out_control.txt` — **moves** (a new check line in
  section 2c, and the narrowed header text is printed).
* `code/state_delegation_repair_0049/out_render.txt` — **moves** (the R5 verdict paragraph
  is narrowed).
* `out_battery_0049.txt`, `out_split.txt`, `out_coverage218d.txt`,
  `out_selftest_negative.txt`, `out_5644_rerun.txt` — predicted **unchanged**: none of them
  prints `delta_control.py`'s prose and none of the exit codes they record is moved by the
  cross-check, which only fires on a mutated table.

Predicted: `reproduce16eb.py`, run unmodified, reports **5 of 7 identical, 2 differing**, and
this repair regenerates and commits the two that move. **mg-16eb's own `out_reproduce.txt` is
NOT regenerated and NOT edited** — it is the auditor's transcript and it is correct about the
tree it was run on. It becomes stale by exactly those two rows, and saying so here is the
whole of the fix for that staleness.

## 6. OPEN 3 — the surface this repair creates, predicted before it is built

Three new surfaces, each named with the property that is now measurable only through it and
the way each fails:

1. **`prose_a74f.py`'s two shapes.** After this, a path reference and a `run_all.sh` section
   reference in three directories are checked. Everything else in that prose — every count,
   every "cannot", every "measured over N" — is *adjacent to* checked text and is not
   checked. Predicted next gap: **a false claim of a shape P1/P2 does not cover, in a file
   this checker walks, read as covered because its neighbours are.**
2. **The section-2c cross-check.** `DELEGATED_PRESENTATION` becomes iterated, so the
   published "either direction" sentence becomes true. It is written for two tables *by
   name*. Predicted next gap: **a third pinned table.** P3 above exists to make that gap
   fail loudly instead of quietly, and P3 is itself the fourth surface — a check on the
   *shape* of the tables, which a table of a different shape escapes.
3. **`visible_a74f.py`'s declared suppression set.** After this, "suppressed" means "by one
   of the five mechanisms in the declared set". Predicted next gap: **a suppression
   mechanism outside the set** — a stylesheet, `aria-hidden`, off-screen positioning,
   `color: transparent`, JS. The instrument fails **open** on all of them: it reports NOT
   SUPPRESSED, which is why its row is named `not-suppressed`, never `shown to a reader`.

**The prediction that outlives this instance:** the next gap will be on surface 1 or 3, not on
the repaired claims, because 1 and 3 are the two places where this repair introduces a new
name for a measured property. That is what mg-16eb's rule says, and this repair does not
expect to be the exception.
