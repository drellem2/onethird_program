# mg-365a — PREDICTIONS, COMMITTED BEFORE ANY ARM EXISTS

The ticket asks two questions and says the honest options include *nothing*:

1. whether a self-inclusive count is a problem worth solving, or the only truthful way to count;
2. whether this is already discharged by mg-05c6, **testable the same way mg-cd8d is — a command,
   not an argument**.

This file is the record of what was expected before the command was written.

---

## §0 — WHAT WAS ALREADY MEASURED BY HAND DURING SCOPING

**A prediction of something already run is a record of nothing.**  Four figures below were taken
by hand with `git log` / `git show` before this file was written, and they are therefore NOT
predictions.  They are listed here so that no reader mistakes them for confirmed forecasts, and
so that the arms can be checked against a written-down expectation rather than against memory.

| already measured, by hand, at `HEAD = b5d8a75` | value |
| --- | --- |
| committed versions of `out_g0_fixed_point.txt` | **38** (31 at mg-585e's pin `0cb0fa4`) |
| commits whose entire diff is that one file | **10** (7 at `0cb0fa4`) |
| main landings since `bd07d70` (the deletion) | **8** |
| of those 8, how many touched that transcript | **0** |
| of those 8, how many committed ≥1 other watched `out_*.txt` | **6** |
| chronological index of mg-585e's own refresh `15af11d3` | **#9** |

The last row is the one that started this directory: `15af11d3`'s own commit message, and the
ticket quoting it, both say **"this is the 8th"**.

## §1 — THE PREMISE THIS TICKET IS WRITTEN ON IS EXPECTED TO BE STALE

**P1.**  `lib_f771.SELF_EXCLUDED` does not exist at `AS_OF_365A`.  The ticket describes it in the
present tense (*"`out_g0_fixed_point.txt` **is** mg-f771's single self-exemption"*), and `bd07d70`
— *delete: THE SELF-EXEMPTION IS GONE AND THE WATCHED CLASS IS TOTAL* — is expected to be an
ancestor of this branch.  The ticket was filed 2026-08-14 from p585e's commit; the deletion landed
at 00:41Z.  A successor carrier filed while its cause was live outlived the cause, which is the
mayor's own caution of 00:22Z arriving on the ticket that quotes it.

## §2 — THE FIGURE THAT LOOKS LIKE THE ANSWER IS EXPECTED TO BE WORTHLESS

**P2 — the RED count goes to zero for the wrong reason.**  `v1_oscillation.is_red` tests for the
string `DISAGREEMENTS, SHOWN` on a line starting `§2`.  `bd07d70` *deleted that heading*.  So
re-running v1's predicate at a newer pin is expected to report **0 RED among the 7 post-`0cb0fa4`
versions**, and that zero measures **the marker's deletion, not the oscillation's end**.  A reader
who re-takes mg-585e's headline figure and reports "it stopped" will have measured nothing.

Predicted: the arm must import `v1_oscillation.is_red` rather than re-spell it (mg-d2c2), and must
print the zero **beside** the reason it is uninformative, or not print it at all.

**P3 — the honest predicate is the solo count, which is defined without reference to §2's text.**
"Commits whose entire diff is that one file" survives the heading's deletion because it never read
the heading.  Predicted: it is the figure that carries the finding.

## §3 — THE DISCHARGE IS EXPECTED TO BE REAL, AND `0 of 8` IS EXPECTED TO BE TOO WEAK ALONE

**P4 — 8 landings is not enough on its own.**  mg-585e priced the pre-deletion rate at ~30 touches
per 129 code/ commits (≈23%).  At that rate 8 quiet landings has probability ≈ 0.77⁸ ≈ **0.12** —
*not significant*.  Predicted: the arm states this and does **not** rest on `0 of 8`.

**P5 — the counterfactual is what carries it, and it is exact in the safe direction.**  `./build.sh`
regenerates transcripts into the worktree and *then* g0 compares worktree against HEAD, so the old
§2's disagreement set `D(T)` **contains** every watched transcript the landing went on to commit.
A landing that committed ≥1 regenerated watched transcript therefore *provably* had `D(T) ≠ {}`,
would have carried a RED §2, and would have owed a refresh.  Predicted: **6 of the 8** post-deletion
landings are in that class and **0** paid the toll — 6 owed, 0 paid, rather than a quiet window.

Predicted: the class is computed with `lib_f771.is_watched` **imported**, not with a re-typed glob,
because a re-statement drifts (mg-1344's P5).  Predicted: importing it gives the same 6 the hand
grep gave — and if it does not, the imported answer wins and this line is the record of the miss.

## §4 — THE TICKET IS EXPECTED TO NAME THE WRONG FIX

**P6.**  Carry-forward item 2 asks whether this is *"already discharged by mg-05c6"*.  Predicted:
**no — mg-05c6 paid the toll rather than removing it.**  `65c647bf`, a solo refresh commit, is
mg-05c6's own and is expected to sit at chronological index **#8** in the solo population.  The
discharge is `bd07d70`, which is mg-c15e's.  An instrument that answers "is it discharged" without
saying *by what* would confirm the ticket's question while getting its subject wrong.

## §5 — THE PUBLISHED COUNT IS EXPECTED TO BE OFF BY ONE, AND THE MECHANISM IS THE PIN

**P7 — "the 8th" is a 9th.**  `15af11d3` is mg-585e's own refresh, and both it and this ticket call
it the 8th.  That number is `7 + 1`: mg-585e's *pinned* figure at `0cb0fa4`, incremented, rather
than re-walked.  Between the pin and the claim, `65c647bf` landed.  Predicted: re-walking puts
`15af11d3` at **#9**, and the skipped commit is mg-05c6's — the very ticket carry-forward item 2
asks about.

This is not a typo and is the general defect worth carrying: **a count derived by incrementing a
pinned figure is wrong exactly when something landed between the pin and the increment**, and it is
wrong silently, because the arithmetic is right.

## §6 — THE SELF-INCLUSION QUESTION IS EXPECTED TO ANSWER ITSELF BY MEASUREMENT

**P8.**  Question 1 asks whether a self-inclusive count is a defect or the only truthful arrangement.
Predicted: it was **neither — it was a property of the exemption, and it is already gone.**  The
counting directory joined the population it counted because *counting required a `./build.sh` run,
and a `./build.sh` run moved that transcript*.  With the exemption deleted the transcript no longer
moves on a landing that does not touch `lib_f771.py`.

Predicted, and checkable at the end of this branch rather than asserted: **this directory counts the
population and does not enter it** — `out_g0_fixed_point.txt` is untouched by this branch, so no
9th, 10th or 11th solo commit is filed by the arm that reports there were ten.  If that prediction
fails, this directory is the instance and must say so in its own transcript.

## §7 — CONTROLS THE ARMS MUST CARRY, PRE-COMMITTED

**P9 — a scan that read nothing must REFUSE, not report 0.**  An empty history, an unresolvable pin,
or a `git log` failure must exit 2 with a named reason.  A `0 of 8` printed because the walk found
nothing is indistinguishable, on the page, from a `0 of 8` that is the finding — and this directory's
entire subject is a zero.

**P10 — the pin must be checked, not declared.**  `AS_OF_365A` must resolve and be an ancestor of
`origin/main`, or the arm refuses.  Every figure here is a function of that commit, so that this
transcript does not go stale on the next landing — which is the defect mg-585e's v1 avoided the same
way, and which this directory would otherwise commit while reporting on it.

**P11 — the negative controls must fire.**  Planted defects, each of which must be CAUGHT:
re-narrowing the watched-class predicate; a truncated history; a pin that resolves but is not an
ancestor; and the loose-vs-anchored RED predicate disagreeing.  A control that is only ever run in
the direction where it passes is not a control.
