# TEN PREDICTIONS FOR A LABEL-VS-COMPUTATION CHECK, COMMITTED BEFORE ANY ARM EXISTS

`mg-68ef` carries `mg-9d9e`'s remainder.  That branch corrected two of its own prose defects **by
re-reading rather than by a control**, and the sentence the ticket is named for is:

> A mislabelled column that prints the right number is the defect this corpus keeps finding one
> estate over.

The carry-forward asks one question and names its own legitimate close:

> whether a **label-vs-computation** check is buildable at all — comparing what a header claims
> against what the arm beneath it computes — or whether this class is irreducibly a reading
> problem, in which case **saying so is itself the deliverable**.

`AS_OF = 5ffb22e558b185f20628873848c549eed78a9780`.  Every figure below is a function of that
commit except where a section says otherwise.  The two exhibits are read **out of the tree** at
`3561300` (pre-correction) and at `AS_OF` (post-correction) and are never re-typed (`mg-d2c2`).

---

## §0  WHAT WAS ALREADY MEASURED DURING SCOPING

A prediction of something already run is a record of nothing, so these are named rather than
predicted.  Seven figures were taken by hand before this file was written:

1. **1 252** tracked `.py` at `AS_OF`.
2. **67** rule-line string literals — a literal matching `---+---`, the shape this estate writes
   under a table header — in **25** files.
3. **65** of the 67 have a `|`-bearing, non-`%`-format string literal within 6 lines above them,
   i.e. a locatable header.
4. **71** formula-shaped column labels under a first-draft byte-aligned segmentation.
5. **43** `O(...)` claims inside docstrings, across **30** files.
6. **The exhibit's table is exactly the table where the obvious splitter fails.**  Naive `|`
   splitting of `     n | node size a+b | H(word | earlier) | note's ceiling 0.9399(a+b) | overpay`
   gives **6** fields against the row template's **5** placeholders, because a column label
   contains the delimiter.  The rule line `    ---+---------------+---...` gives **5**.  Checked at
   both `3561300` and `AS_OF`.
7. **A byte-aligned segmenter is wrong on this estate.**  Two of `s1_run_the_test.py`'s seven
   tables have their rule line offset **one character left** of their header — in the source *and*
   in the committed transcript — so segment boundaries must be found by a shift search, not by
   taking the rule line's `+` columns literally.

Nothing below was run before this file was committed.  In particular the funnel of §1–§4, every
verdict, and every figure about the `O(...)` population are unmeasured at the time of writing.

---

## THE CHECK, STATED BEFORE IT IS BUILT

A **table** is a rule line, the header above it, and the `%`-format row template below it.
Column boundaries come from the rule line under the shift `δ` that best matches the header's `|`
positions.  A column label is **formula-shaped** if it carries an arithmetic operator between
symbols, a juxtaposed product (`0.9399(a+b)`), or a power.  A column is **paired** if the row
template's placeholder count matches the column count, which makes placeholder `i` the computation
of column `i`; the argument expression is taken from the `%` tuple and resolved one step through
local assignment in the enclosing scope.

The adjudication is deliberately narrow: **the numeric literals named in a formula-shaped label
must be the numeric literals of the expression that fills that column.**  Nothing here judges
algebra, and `NOT ADJUDICABLE` is a verdict rather than a pass.

---

## THE PREDICTIONS

**P1 — SEGMENTATION.**  The number of tables where naive `|` splitting and shift-aligned rule
segmentation disagree on the column count is **between 1 and 10 inclusive**, and the exhibit is
one of them.

**P2 — THE SHIFT IS REAL AND SMALL.**  **At least 5** tables need a nonzero `δ`, and **no** table
needs `|δ| > 2`.  If some table needs a larger shift the search is measuring noise rather than
alignment.

**P3 — REACHABILITY, THE HEADLINE.**  **Fewer than half** of the formula-shaped column labels pair
to a computing expression at all.  This is the prediction the deliverable turns on: a check that
cannot reach its subject is a reporting discipline and not a lint.

**P4 — ADJUDICABILITY.**  Of the paired formula labels, **at most 6** carry a numeric literal in
the label and are therefore adjudicable by the literal rule.  The rest are `NOT ADJUDICABLE` and
are counted as such rather than as passes.

**P5 — THE SWEEP RETURNS EMPTY AT `AS_OF`.**  **Zero** disagreements corpus-wide, the exhibit
having been corrected before the pin.  A nonzero result is a finding either way and is printed in
full rather than summarised.

**P6 — THE DETECTOR FIRES ON THE EXHIBIT AND ONLY THERE.**  Run against `3561300` it reports the
`(1-c)(a+b)` column as a disagreement; run against `AS_OF` it is silent on the same table.  Both
readings come out of the tree.

**P7 — EXHIBIT A IS UNREACHABLE, AND IN THE DANGEROUS DIRECTION.**  A syntactic loop-nesting-depth
proxy over `feasible_merges` returns **1** — fewer than the 2 factors of the WRONG claim `O(a*b)`
and fewer than the 3 of the corrected `O(a*b*(a+b))`.  So the proxy cannot separate them, and used
as a check it would have **licensed** the wrong claim rather than flagged it.

**P8 — THE PROXY IS A COIN ON THE WHOLE POPULATION.**  Over the 43 `O(...)` docstring claims the
loop-depth proxy equals the claimed factor count in **fewer than half** of them.

**P9 — REQUIRED-INERT, THE WRONG DIRECTION.**  Rewording a non-header note string moves **no**
figure in §1–§4.  Without this, a count that moved on prose would be measuring the corpus's
English rather than its tables.

**P10 — REFLEXIVE.**  This directory's own arms print tables of the shape they measure.  The
detector run over this directory's own files flags **0**.

---

## WHAT WOULD MAKE THIS DIRECTORY WRONG RATHER THAN MERELY REFUTED

- A funnel whose top is zero.  Every central figure here is small, and a broken walk, an
  unresolvable pin, or a narrowed class returns a small number for free — so the selftest
  establishes that the instrument sees the corpus **before** any verdict is printed.
- A detector that cannot fire on the one instance the class is named from.  P6 is that control and
  it reads the pre-correction spelling out of the tree.
- A `NOT ADJUDICABLE` silently counted as a pass.  P4 is the guard.
