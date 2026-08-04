# mg-f3ff — predictions, committed BEFORE any script of this repair exists

The brief: the dropped-verdict census of 2026-07-31 04:12–04:22Z was built from **mail routing**,
not from the tree, and is proven wrong on 1 of its 4 rows. Re-derive all four from the commit log
and repair the **method**.

This file is committed first, before `treecensus.py`, `s1_rows.py`, `s2_controls.py` or any output
of theirs exists. Everything below is a prediction about what those scripts will print.

## DISCLOSURE — what was already run before this file was written

Predictions written after looking are worth less than predictions written before, and pretending
otherwise is the defect this ticket is about. So, in full:

Before writing this file I ran, by hand, **read-only** `git log` and `grep` at the terminal:

1. `git log --all --pretty='%h %ad %cd %s' | grep -i <parent-id>` in both repos — **subject line
   only**. It returned, for `mg-fcf1`, nothing but `mg-fcf1`'s own audit commits.
2. `git log main --grep=<parent-id> -i` in both repos — **full message**. It returned successor
   commits for `mg-fcf1` and for `mg-d112`, and none for `mg-16eb` or `mg-5800` before the filing
   instants.
3. `git log -1 --pretty='%B'` on `8fc5111`, `f024985`, `b169561`, `1b00147`, `2697c07`.
4. `grep -rl <parent-id> ~/.macguffin/work` — which tickets name each parent.

So P1–P4 below are **not blind**. They are predictions that the instrument will reproduce what a
hand grep already showed, which is a weaker claim, and is stated as such. P5–P11 concern things the
hand greps did **not** settle, and those are blind.

Nothing was run against the mail store beyond `grep -rl` counts (18 / 9 / 101 / 22 files naming the
four parents) and `head -25` on one message to learn the header format. No mail-window query has
been run.

## The four rows

| row | dropped-verdict ticket | filed (UTC) | parent | parent's repo |
|---|---|---|---|---|
| 1 | mg-e35b | 2026-07-31T04:13:24Z | mg-fcf1 | onethird_program |
| 2 | mg-fccb | 2026-07-31T04:12:41Z | mg-d112 | one_third_width_three |
| 3 | mg-a74f | 2026-07-31T04:22:15Z | mg-16eb | onethird_program |
| 4 | mg-dffa | 2026-07-31T04:22:50Z | mg-5800 | onethird_program |

Each row's title asserts, of its parent, some form of *no landing commit* / *no successor*.

## Predictions

**P1 (not blind).** Row 1 — `mg-fcf1` — **REFUTED**. Successor commits exist in the population at
`2026-07-31T04:13:24Z`. **Generations ≥ 3.**

**P2 (not blind).** Row 2 — `mg-d112` — **REFUTED**, and refuted in **both** repos: at least one
successor commit in `one_third_width_three` and at least one in `onethird_program`, all authored on
2026-07-29, **two days before** the row was filed.

**P3 (not blind).** Row 3 — `mg-16eb` — **UPHELD**. Zero successor commits at
`2026-07-31T04:22:15Z`. The premise is true as written.

**P4 (not blind).** Row 4 — `mg-5800` — **UPHELD**. Zero successor commits at
`2026-07-31T04:22:50Z`. The premise is true as written.

**P5 (blind).** The census's accuracy comes out **2 of 4 rows correct**, i.e. **2 of 4 refuted** on a
population of **4** — the four DROPPED VERDICT tickets pm-onethird filed between 04:12:41Z and
04:22:50Z on 2026-07-31. The brief's own figure, *1-of-1 refuted on a population of 4*, will be
**superseded**: it is 4-of-4 checked, 2 refuted.

**P6 (blind).** The **subject-only** negative control reproduces the census's wrong answer on row 1:
reading only `%s`, the instrument finds **0** successor commits for `mg-fcf1` where the full-message
reader finds ≥ 1. Predicted the same on row 2. **This is the point of the control** — the census's
error is not only that it read mail; a tree-reader that reads only subject lines fails identically.

**P7 (blind).** The **mail** negative control — messages in the mg mail store naming the parent,
dated strictly between the parent's own landing commit and the row's filing instant — returns
**0 messages that name any successor ticket** for row 1. Lower confidence on the other three; the
mail store is large (101 files name `mg-5800`) and I have not queried it.

**P8 (blind).** The **ticket-reference-graph** reader finds at least one successor commit on row 1
that the direct parent-id message grep does **not** — i.e. transitive descent through ticket bodies
buys real coverage over grepping the parent id.

**P9 (blind).** On rows 3 and 4 the ticket graph will name successor **tickets** (they exist:
`mg-0d85`, `mg-70c7` for `mg-16eb`; `mg-19ec`, `mg-56dc`, `mg-c742`, `mg-fe59` for `mg-5800`) whose
**commits are all authored after** the filing instant. So the rows are upheld on **commits**, and a
ticket-only census would have reported them refuted. Predicted: **the commit date, not the ticket's
existence, is what makes rows 3 and 4 true.**

**P10 (blind).** At least one of the four rows was already refuted **by the polecat sent to work it**,
in that polecat's own commit message, before this ticket existed. (Row 1 is known to be — the brief
says so. Predicted: a **second** row too.)

**P11 (blind).** Of the declared blind spots, at least one is demonstrated to **bite on this very
population** rather than merely being listed — that is, some real successor work is invisible to the
new method as specified.

## What is predicted to be reported as NOT DONE

- This repair does **not** reopen `mg-e35b`, `mg-fccb`, `mg-a74f` or `mg-dffa`. All four are done.
- It does **not** re-audit the mathematics of any parent.
- It does **not** rewrite the four ticket bodies. A census is repaired by replacing the instrument,
  not by editing the rows it produced.
