# mg-cd8d — a census reading taken BEFORE the rebase, graded by the real instrument

**The ticket's step 1 was a command and not an argument, and this directory is the command.**
mg-99f4 published a figure about a shared census and said the number was only trustworthy
because of *when* it was taken: after the rebase, not before. Its carry forward asked for an
instrument. mg-05c6 then landed a corpus pin and two new verdicts, `CORPUS` and `STALE`, and
pm-onethird's dispatch note said in so many words that whether the pin **closes** the
pre-rebase case or is **blind** to it decides what is left to build — and that the two
possibilities differ in one command's output.

## §0 What was already measured, and when

**W1 through W6 were run by hand, in a scratchpad, during scoping**, before any file in this
directory existed, and they returned exactly what §1 reports. So **no `PREDICTIONS.md` is
filed**: a prediction of something already run is a record of nothing, which is this estate's own
rule (mg-585e §0, mg-fa83 §0) and it applies to the agent quoting it. What this directory adds
over the scratchpad is that the worlds are reproducible, that the harness is held to both
directions before its one-word answer is read, and that the record half of §3 is pinned.

Two things were **not** pre-run and are new here: `W7`, and §4's split of mg-9876's row, of which
scoping had checked only mg-99f4's own directory — one instance, which is what §4 turns into a
denominator.

## §1 The answer

`verdict_for` returns **`CORPUS`** for a census reading taken before the rebase. It is **not
`AGREES`**, so mg-05c6 is not blind to it, and `W2` — the same branch taking the reading after
the rebase — returns `AGREES`, so the two are distinguishable at gate time.

| world | what it is | verdict |
|---|---|---|
| W1 | the ticket's event: reading taken pre-rebase, main gained 2 directories | `CORPUS` |
| W2 | the discipline followed: reading taken after the rebase | `AGREES` |
| W3 | the innocent branch: published nothing, committed copy is main's older reading | `CORPUS` |
| W4 | 11 directories of drift, past the declared bound of 10 | `STALE` (red) |
| W5 | same pin, one figure tampered — the instrument moved on an unchanged corpus | `DISAGREES` |
| W6 | W4's branch refreshes, but with a **pre-rebase** reading | `CORPUS` |
| W7 | W1's two texts at a path that is not in `CORPUS_SCOPED` | `DISAGREES` |

Every world is **two real commits of `main`**: the corpus is `git archive`d at each, today's
producer is overlaid on both sides so the *producer* pin cannot move, and the real
`a4_sweep.py` is run over each tree as a subprocess so `lib9876.ROOT` resolves to the sandbox.
The pair is then handed to the real `lib_f771.verdict_for`, imported rather than re-spelled
(mg-d2c2). The only synthetic object anywhere is the simulated branch's own new directory, one
file holding `VALUE = 1`, and it lives only in a temporary directory.

## §2 What that discharges, and the two residues

The carry forward — *any arm publishing a figure about a shared census should refuse to emit
one computed on a tree that is not the tree being merged* — is **discharged as a detector** by
mg-05c6 (`8b169b1`, with `cead0df` and `8f977b2`). Two things it does not do:

**R1 — detected, not refused, and the grade is shared with the innocent case.** `CORPUS` is not
in `RED_VERDICTS` (read from the real constant, r0 D4), and W1 and W3 produce the same word in
the same build log beside the same instruction: *restore it rather than committing it — the
refresh is owed by whoever trips the bound, not by this branch.* In W3 that instruction is
right. In W1 the committed copy **is this branch's own pre-rebase reading**, so restoring keeps
the figure computed on a tree that is not the tree being merged. Nothing inside `verdict_for`
can separate them: it is handed two texts and a path, and who *wrote* the committed copy is not
among its arguments — which is `r0` D5, a control that must **not** fire and whose inertness is
the finding. What could separate them is outside it, and is a question about the diff against
the merge base rather than about `HEAD`.

**R2 — the bound is discharged by a reading that need not be the merged tree's.** Under
mg-05c6 the standing instruction to every branch is *restore*, so the only branch that commits
a census at all is the one whose gate went `STALE`. W4 is that branch; W6 hands it a pre-rebase
refresh and the red clears. And it buys partial credit, which is arithmetic: drift against the
committed figure goes 11 → 2 on a pre-rebase refresh against 11 → 0 on a post-rebase one, so a
wrong refresh also postpones the next honest reading.

**Both residues are reported and neither is built.** The ticket forbids building before step 1
for a stated reason — two instruments answering one question is the failure this ticket is
about — and step 1's answer changes what should be built. Successor **mg-d928** carries them.

## §3 How often, measured on the record and pinned at `b5d8a75`

**0 of the 19 commits on `main` since mg-05c6 landed have touched the census**, against 36 of
the 200 commits at that tip. That is the amortisation measured from the other side and it is
this arm's own number, not mg-05c6's 34 → 6, which was a different window. The live drift is
**3 of the bound of 10**, so the bound has not yet been tripped and the population of branches
exposed to R1 and R2 today is small. The hazard is unchanged **per occurrence**; only its
frequency is small — pm-onethird's own reading of the 82% figure, repeated rather than
re-decided.

## §4 The surviving half of mg-99f4, turned into a count (`r2`)

mg-99f4 found that its `+1` on mg-9876's row *a committed transcript records a demonstrated
failure* came from `PREDICTIONS.md` and from none of its three committed `out_*.txt`. Re-run
with a4's own `RED_TOKENS` over every directory at `b5d8a75`: **19 of the 156 members of that
row are backed by no transcript at all** — mg-99f4's directory is one, and so is
`gate_fixed_point_f771`, whose README carries the word `REFUTED` as an *example* of the pin's
declared blind spot. So the instance is 1 of 19 rather than a one-off.

**Reported and not repaired**, and the reason is mg-99f4's own: the row is mg-9876's, its
wording is mg-9876's call, and a branch that quietly re-scoped another instrument's detector
from here would be doing the worse thing even if the re-scoping would be right. Nothing under
`code/control_audit_9876/` is edited by this branch.

## §5 What this directory does not do

- **It does not build the instrument.** R1 and R2 are specified, not implemented.
- **It is not in `build.sh`.** Nothing consumes it, its subject is one already-landed
  mechanism rather than a control on this repository's own state, and it costs ~14 s against a
  gate measured at ~47.5 s. `r0` is a control on `r1`'s harness, not on the corpus.
- **It edits no other directory**, moves no `STATE.md` word (so the ratchet is untouched and no
  twin re-pin is owed), and takes no `docs/FACTS.md` entry — every measurement here is consumed
  by this landing, which is mg-3da1's homelessness test.
- **It does not print pin digests.** A corpus pin covers the content of every `.py` and `.sh`
  under `code/`, so a digest in a tracked transcript here would move whenever anybody edited
  anything — the defect this directory is about, one file over. Populations are counts at fixed
  commits and cannot move; the verdicts are a function of `verdict_for`, which is the instrument
  under test and *should* move these transcripts when it changes.

## §6 A remedy is an artifact of the same kind as the defect

This directory publishes figures about a shared corpus, which is exactly the thing it is
measuring, so the enumeration was run against itself:

1. **Every figure is pinned to a commit** (`AS_OF`, `MAIN_BEFORE`, `MAIN_FAR`, `PIN_05C6`), and
   all four are checked to resolve *and* to be ancestors of `HEAD` before anything is measured —
   a world built on a commit this checkout does not carry is a different measurement, not a
   smaller one. The arms **refuse** (exit 2) rather than answer.
2. **The laundered green is planted** (r0 D2). With the archive step suppressed the corpus is
   empty but for the producer, both readings are identical, and the verdict is `AGREES` — a
   green meaning *read nothing*, indistinguishable from the discipline being followed. It is
   caught by the population and not by the verdict, which is why every world prints its
   population.
3. **The overlay is shown to be load-bearing** (r0 D3): run each tree's own producer and a
   pre-mg-05c6 corpus prints no pin at all, so the verdict is red for the instrument's age
   rather than for when the reading was taken.
4. **A control fixture was neutralised rather than left to move a published figure.** `r0` D6
   returned **1** on its first run: the site was its own positive fixture, the literal
   `if "8 9" in out:`, counted by the §1 detector it exercises. It is assembled from parts now,
   the detector still receives the exact characters, and this directory adds **0** membership
   candidates. That is mg-05c6's own neutralisation one directory over, and finding it took
   running the control rather than reading it.
5. **This branch's own census movement is taken after the rebase**, which is the discipline the
   ticket is about, applied by the branch reporting on it. The figures are in the commit
   message.
