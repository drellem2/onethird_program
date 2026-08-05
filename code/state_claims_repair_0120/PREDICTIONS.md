# mg-0120 — PREDICTIONS, committed before any script of this repair exists

**This file is committed in its own commit, and no `.py` or `.sh` of
`code/state_claims_repair_0120/` exists at that commit.** The anchor for that claim is
written at the bottom of this file *after* the fact, in the README, and it is written as a
commit that is an **ancestor of `main`** — not as the sha this branch happens to carry,
because this branch will be rebased and that sha will not survive. That is the second half
of this ticket and it would be absurd to commit the defect while repairing it.

---

## WHAT THIS REPAIR IS FOR

`code/state_delegation_audit_16eb/claims16eb.py` is named *"THE CLAIMS mg-0049 ADDED,
**CHECKED**"*. mg-65eb read it with `ast` and found that some of its verdicts are not
computed from anything — they are literals typed into the source. A verdict that is a
constant returns the same answer on every tree it is ever run against. It has never been
shown capable of returning anything else, so it is not a check, whatever the row is called.

The repair is not "replace the literal with an expression". An expression that happens to
return the right answer today is indistinguishable from a constant unless someone has seen it
return the *other* answer. **So every verdict this repair makes real must be accompanied by a
constructed input that flips it.** That is what `flip_0120.py` is for and it is the part of
this work that can fail.

---

## P-0 — DISCLOSURES. These are MEASUREMENTS ALREADY TAKEN, not predictions.

Recording them as predictions would be a lie about when they were known. mg-b2af set this
precedent in this arc and it is followed here.

**D-1 — the population of constants is 6 of 17, not 4 of 17.** Read with `ast` at
`b1c3467`, `claims16eb.py` has **16 `claim()` call sites** and prints **17 rows** (one site,
line 174, sits in a `for` over three figures; one site, line 72, is the `else`-less guard
branch of an `if` and does not run on a tree where the anchor resolves).

Of the 16 sites, **7 carry a constant verdict**:

| site | literal | on the printed path? |
|---|---|---|
| `claims16eb.py:72` | `False` | **no** — guard branch, fires only if the anchor sentence is gone |
| `claims16eb.py:94` | `False` | yes |
| `claims16eb.py:142` | `False` | yes |
| `claims16eb.py:156` | **`True`** | yes |
| `claims16eb.py:178` | **`True`** | yes |
| `claims16eb.py:194` | `False` | yes |
| `claims16eb.py:217` | `False` | yes |

So: **over the population of 17 printed rows, 6 are constants** — the 4 literal `False` the
ticket names, **and two literal `True`s the ticket does not**. The ticket's "4 of 17" is
exact for the grain *literal `False`* and short by two for the grain *verdict that cannot
change*. A literal `True` is the worse of the two shapes: a row pinned `False` at least
reports a problem, and a row pinned `True` is a control that has **never been capable of
failing**, sitting inside the numerator of the file's own headline count.

The guard at line 72 is **not** counted as a defect. It is a deliberate alarm — it runs only
when the sentence it is about has been deleted — and mg-65eb marked it as such. This repair
keeps it and says so.

**D-2 — "nothing runs it" is true of one population and false of another.** No file in
`code/state_delegation_repair_a74f/` names `claims16eb.py` (that is the ticket's population,
and it is correct). But `code/state_delegation_audit_16eb/run_all.sh:82` — the file's own
suite — runs it as section 4, and `code/state_visibility_audit_65eb/run_all.sh:106` runs it
as section 11. **Over the population "every file in the repository", 2 files run it.** The
ticket's sentence is scoped in its body and unscoped in its title; this is recorded because
naming the population is the discipline this whole arc exists to enforce.

**D-3 — `739f7bd` is SHA-DISPLACED BY A REBASE, not lost.** Measured before this file was
written:

```
git patch-id --stable  of 739f7bd  ->  17a7bca3c7be2fc4f9ab736294b06230a11c5cc0
git patch-id --stable  of cfd2af5  ->  17a7bca3c7be2fc4f9ab736294b06230a11c5cc0   IDENTICAL
git merge-base --is-ancestor cfd2af5 main  ->  exit 0
```

Their **trees differ** (`1dbf047` vs `fd6b2f4`) and their **parents differ** (`bd24efc` vs
`b469d67`), which is exactly what a rebase produces and exactly why ancestry fails while the
content is intact. The two fixes the ticket says "look identical" are therefore
distinguished, and the one that applies is *re-point the anchor at the merged twin*, not
*the commit is gone, re-derive the property*.

**D-4 — `anchor65eb.py`'s twin search matches on the commit SUBJECT** (`six65eb`-adjacent
code, `anchor65eb.py:twin_of`). A subject is a label. Two commits can carry one subject and
different content, so a twin identified by subject is an assertion about naming, not about
bytes. This repair identifies the twin by `patch-id` and **constructs the case that breaks
the subject rule** rather than arguing that it could break.

---

## P-1 — the 6 constants, made real

**P-1a.** All 6 printed constant rows can be computed from the tree. **Predicted: 6 of 6.**
I am not predicting that all 6 are computable *without a markdown renderer* — see P-3.

**P-1b — where they land at `HEAD` once computed.** mg-a74f repaired the four `False` rows,
so a *computed* verdict should move. Predicted, row by row, over the population of 6:

| row | predicted verdict at `HEAD` |
|---|---|
| `:94` two tables cannot drift apart in EITHER direction | **holds** — mg-a74f implemented the missing direction |
| `:142` exit 1 means "no longer presented to a reader" | **NOT `holds` and NOT `BROKEN`** — I predict the sentence mg-16eb quoted is **not in the file at `HEAD`** because mg-a74f narrowed it, and the honest computed state is a third one |
| `:156` "NOTHING IN THIS FILE CHANGED EXCEPT ONE MESSAGE AND FOUR SELF-TEST CASES" | **holds** |
| `:178` the R1/R2 table: exit 0 against mg-bee1, exit 1 against mg-0049 | **holds** |
| `:194` both batteries "re-run in section 7 of run_all.sh" | **BROKEN** — I predict mg-a74f did **not** touch mg-0049's README pointer, so this row was pinned to the right answer and stays `BROKEN` when computed |
| `:217` R5 "`<details>` at the top SUPPRESSES NOTHING" | **BROKEN** — the sentence is mg-0049's and I predict it is still in `render0049.py` verbatim |

**If `:194` and `:217` come out `BROKEN` when computed, that is the most useful outcome in
this file**, because it is the case where a constant and a measurement agree — and the whole
point of the ticket is that agreeing today is not the same as being able to disagree.

**P-1c.** The printed headline will change from `13 of 17 ... 4 do not` to a line that names
**three** states, not two, because a row whose sentence has been deleted is neither. I
predict the new headline reports **at least one row in the third state**.

---

## P-2 — THE FLIP CONTROL. This is the part that can fail.

For each of the 6 rows made real, `flip_0120.py` constructs an input on which the verdict
takes the **opposite** value, in a throwaway git worktree, and prints both. A row that
cannot be flipped is reported **NOT PROVEN CAPABLE OF BOTH ANSWERS** and is not counted as
repaired.

**P-2a. Predicted: 6 of 6 flip.**

**P-2b. Predicted: at least one of the 6 does NOT flip on my first construction** and needs
a second one, and I will keep the first failing construction in the transcript rather than
delete it. I name the row I expect to be hardest in advance: **`:156`**, because
"NOTHING IN THIS FILE CHANGED EXCEPT ONE MESSAGE AND FOUR SELF-TEST CASES" is a claim about
a diff against `db2b77d`, and a mutation that flips it must change `presentation.py` in a way
the certified digests still tolerate.

**P-2c.** The flip harness itself will be run against a **deliberately re-pinned copy** of
`claims16eb.py` — a copy where one verdict has been put back to a literal — and it must
report that row as NOT capable of both answers. Predicted: it does, on 1 of 1. Without this,
the flip harness is itself a control nobody has seen fail.

---

## P-3 — the dependency, declared before it bites

Rows `:142` and `:217` are about what a reader is shown, and mg-16eb, mg-0049, mg-5644 and
mg-a74f all measure that with two real GFM renderers installed outside the repo. **Predicted:
2 of the 6 rows require `marked` and `markdown-it`, and without them those two rows are
reported UNPROBED rather than guessed** — never silently as `holds`. `claims16eb.py`'s
current header says *"Nothing here mutates anything"*; this repair keeps the **working tree**
inviolate and does its constructions in throwaway worktrees, and it will say so in the header
rather than leaving the old sentence to go quietly false.

---

## P-4 — THE QUESTION THE TICKET EXISTS FOR: what rests on the four rows?

> *"Then find out whether any conclusion in the arc rests on those four rows — that is the
> question this ticket exists for, and it is not answered by fixing the file."*

**P-4a. Predicted: YES, and the load-bearing thing is the number SIX.** `claims16eb.py`'s
output is where "mg-16eb's six broken claims" comes from. Four of those six are constants, so
the cardinality **6** is itself partly a constant. Every downstream sentence that says *six*
— mg-a74f's commit subject `mg-16eb's SIX BROKEN CLAIMS REPAIRED BY CLASS`, its README, its
`claims_a74f.py` docstring, mg-65eb's `six65eb.py` (which is *named* after the number) —
inherits that.

**P-4b. Predicted: ≥ 3 distinct files assert the figure six** (population: every tracked
`.py`/`.md`/`.sh`; grain: a file, counted once however many times it says it).

**P-4c. Predicted: the number six SURVIVES.** That is, when the six rows are recomputed at
`bd24efc` — the revision where mg-16eb ran — I predict the count of BROKEN rows is still 6,
so the conclusion built on it is **true but was unevidenced for 4 of its 6 rows**. This is a
prediction I could easily lose: if the computed count at `bd24efc` is not 6, then a published
cardinality in three or more documents is wrong and that is a much larger finding.

---

## P-5 — the anchors, re-measured over a population that is not mg-65eb's

**P-5a.** Re-running `anchor65eb.py`'s rule at today's `main` over its own 4-directory
population reproduces **23 LIVE / 1 STALE**. Predicted: it does, because none of those four
directories has changed since.

**P-5b — the population is too small, and that is the finding.** Predicted: extending the
same rule to **every tracked `.py`/`.md`/`.sh` in the repository** finds **more than one**
stale anchor — I predict **≥ 5 distinct stale sha tokens**, because every arc in this repo
pre-registers predictions on a polecat branch, names that branch's sha in its own prose, and
is then **rebased** by the refinery. `739f7bd` is not a mistake somebody made; it is what the
merge process does to every anchor written before the merge.

**P-5c.** Predicted: **0** of the stale ones are `ANCHOR-DEAD` (no ref reaches them), because
the polecat branches are still on `origin`. This matters: it means the repo-wide finding is
"pointers rotted", not "evidence lost", and those need different alarm levels.

**P-5d.** Predicted: for **≥ 4 of the stale tokens**, a patch-id twin exists on `main`, i.e.
the fix is mechanical.

---

## P-6 — what I predict about my own instruments

**P-6a.** I predict `flip_0120.py` will find **at least one defect in my own repaired
`claims16eb.py`** — a row I believed computed that turns out to be insensitive to the input I
constructed for it. Predicted count: **≥ 1**.

**P-6b.** mg-16eb's committed `out_claims.txt` will **stop reproducing** from the repaired
program. That is not a regression, it is the repair. Predicted disposition: the pre-repair
transcript is kept under an explicit name rather than deleted, and the README says so.

**P-6c.** I predict I will **not** wire `claims16eb.py` into
`code/state_delegation_repair_a74f/run_all.sh`. Its own suite already runs it (D-2) and
adding a third caller would make the "nothing runs it" sentence *look* answered without
changing whether anyone reads the answer.

---

## SCORING

Every P above is scored in `README.md` with the measurement beside it, including the ones I
lose. A prediction is not revised after the fact; a refuted prediction is a result.
