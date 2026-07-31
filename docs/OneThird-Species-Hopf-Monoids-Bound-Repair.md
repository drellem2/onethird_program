# The bound repair — mg-5040

Repairs mg-4700's three OPEN items. mg-4700 audited mg-821e (`af432ee` + `b534db7` + `41ac5d4`),
which repaired mg-6cb9 / `26c8d5c`, which audited mg-d633 / `e8fbd4f`.

Instrument: `code/species_bound_repair_5040`, `sh run_all.sh`. Pure Python 3, no network except
`git archive` and `git log` against this repository, which are local.

---

## 1. THE ONE SENTENCE

Three tickets in a row widened a walk so that a sentence about "every regular file" would be true,
and each widening bought exactly one generation. **What generated the generations was not the depth
rule and not the symlink rule. It was the silence** — `os.walk` declines things without saying so,
and a sentence quantified over what came back. So nothing is widened here. **Each walk returns what
it declined, with the reason, and a declined entry that is not the one stated rule is a finding.**

---

## 2. OPEN 1 — WHICH OF THE TWO OPTIONS WAS TAKEN

mg-5040 named two honest options and asked which. **This took option 1: state the walk's actual
bound, so that the claim and the code describe the same set.**

**Not option 2.** Making a filesystem walk *total* means `followlinks=True` plus cycle detection —
and a walk that follows links still stops at a mount boundary, still declines a device node, and
still cannot enter a directory the process has no permission for. "Total" would have been the third
widening wearing a stronger word, and it would have bought one generation like the two before it.

But a bound written in prose is a copy of the code, and this arc has watched copies rot for four
tickets. So **the bound is not written in prose. It is stated in the enumeration:**

```python
def walk_residue(root, stated_dirs=(PYCACHE,)):
    """(files, stated, unstated) -- nothing is dropped without landing in
    one of the last two."""
```

`os.walk` silently declines four kinds of thing: a directory the caller pruned, a **symlinked**
directory (no `followlinks`), an entry that is not a regular file, and any directory it raised an
error on — which it swallows entirely unless `onerror` is given. All four now come back. The residue
is printed beside the count, and **anything in it that is not the stated `__pycache__` rule is
counted into that checker's `TOTAL BAD`.**

That is a subtraction, not a widening. The residue is **a measurement of what happened**, not a list
of the rules somebody remembered — so it covers the rule nobody has thought of yet.

### The evidence that it is the floor and not another rung

`r1_bound.py` plants four structures in `code/species_7d75` and runs all four checkers against each.
**Two of the four were chosen precisely because no extent line in this repository has ever mentioned
them**, and no line of the repair knows they exist:

| planted | `w3_scope` | `s1_extent` | `e1_extents` | `e2_crosssection` |
|---|---|---|---|---|
| a symlinked directory | 1 | 1 | 1 | 1 |
| a fifo | 1 | 1 | 1 | 0 — and correctly: it is not `*.md`, so it is not in e2's extent |
| a broken symlink named `leak.md` | 1 | 1 | 1 | 1 |
| a directory with mode `000` | 1 | 1 | 1 | 1 |

Against the pinned pre-repair tree `4372fae`, the same four structures leave the same checkers
silent — with one instructive exception developed in `OUTCOMES.md`: `s1_extent.py` there exits 1 on
three of the four, every time through its `shutil.copytree` control and never through its extent,
telling a reader the injection control broke while a forbidden statement sits live.

**And `e1_extents.py` can now disagree with its subjects without out-walking them.** mg-4700's F1 was
that E1 walks the way its subjects walk, so when both decline the same thing `want <= got` holds and
E1 certifies a false extent. Widening E1's walk would have fixed the instance. Instead E1 checks the
walk **against itself**: `r1_bound.py` R1d shows E1 exiting 1 with every `reads every …` inclusion row
still `ok`, and the row that fails being the residue row.

### What is still true and is not claimed to be more

The sentence still says `EVERY REGULAR FILE … AT ANY DEPTH`, verbatim, because three committed
instruments assert those exact phrases and this ticket does not weaken what is confirmed. What is
new is that the sentence now **continues**: *every regular file the walk reached — and here is
everything it declined.* The claim and the code describe the same set because the run goes red
whenever they would differ.

---

## 3. OPEN 2 — RUNG OR FLOOR

The deletion test has now missed at the **gate** (mg-9220), at the **return**, at the **clause**
(mg-64b6), and at a **multi-statement shell block** (mg-4700 F2). Four levels, each found by the
level below it failing.

**That is not four bugs. It is a test whose grain is chasing the code's structure**, and a grain that
chases structure never catches up: the next level exists as soon as somebody writes a compound
statement the current grain does not split. `r2_wiring.py` measures exactly this — mg-4700 split the
old block into **3** parts by hand; splitting it by line gives **6**. *That the two counts disagree
is the finding.* The number of parts a block has depends on how finely you choose to cut it.

**So this is the floor, and it is reached by removing the structure.** The twenty lines became two:

```sh
echo "cross-section check (mg-821e), its own output, unfiltered:"
python3 ../species_extent_d633/e2_crosssection.py
```

Running the check and printing its output are now **the same statement**. Neither can be deleted
without the other; `set -e` carries the verdict, which is what it was already doing. Nothing is
piped, because a pipeline's status in POSIX `sh` is its last command's and `set -o pipefail` is not
available in dash (mg-c2b3).

Three things fall out of the deletion rather than being fixed:

* the `|| { … exit 1; }` guard that moved the message and not the verdict — **gone**;
* the two `echo`s that printed the check's output and were guarded by nothing — **gone**, because
  the printing is no longer separable from the call;
* mg-4700's **F5**, the guard announcing any non-zero exit as *"a struck claim stands un-struck
  elsewhere"* even when `e2` had crashed — **gone with the guard that made the claim.**

The remaining `echo` is a heading. Deleting it changes a heading and nothing else, and that is the
honest state for a line that makes no claim.

---

## 4. OPEN 3 — THE CENSUS, AND WHY REGENERATING IT IS NOT THE REPAIR

The committed `code/species_extent_d633/out_e2_crosssection.txt` claimed 123 markdown files where the
tree held 131 — and by the time mg-5040 ran, 146. mg-d633's was short by 5; mg-821e regenerated it
and the gap widened.

**The count is a property of a tree, not of the checker**, so it goes false the moment any commit
adds a markdown file — and re-running at commit time does not repair that, because a merge queue
moves the tree afterwards. **Post-commit is not post-merge.** mg-821e obeyed Appendix A exactly and
was still wrong, because the rule names a condition (*the commit*) that something else is free to
change underneath it.

So the figure is **anchored**. `e2_crosssection.py` now prints the revision it measured:

```
MEASURED AT <rev> (mg-5040, on mg-4700's F3).
```

A claim about "now" that nothing can keep true becomes a claim about a commit git cannot move. **The
mechanism is not removed and this document does not claim it is:** the next commit that adds a
markdown file makes the count stale again. What changes is that a stale copy now reads as *stale*
rather than as *wrong*, without a reader re-deriving anything — the same move as OPEN 1, one level
out, and mg-6cb9's `a2_crosssection.py` row `the COMMITTED run's extent line is true at HEAD` will go
red again on the next such commit. That row is a **staleness** check and it is correct to keep it.

---

## 5. THE CORRECTION RECORD — every copy of `A2 TOTAL BAD`, and which ones share a source

**The rows win.** mg-6cb9's `a2_crosssection.py`, run unmodified **against the tree those summaries
shipped in — `4372fae`, which git cannot move** — reports **`A2 TOTAL BAD: 2`**. Every summary that
says otherwise is corrected here or in place.

**And the anchor is not decoration.** The first version of `r3_summaries.py` graded the summaries
against a *live* run in this worktree — and this ticket regenerates the census, which turns one of
the two rows green, so the live figure is **1** again for a reason the correction itself caused.
**That is F3 one level out, inside the file repairing F3.** `r3` now runs the artifact twice: at the
pin, in a git repository initialised from a `git archive` extraction so `a2`'s own `git ls-tree HEAD`
answers for the pinned tree, and in this worktree — and only the first grades anything. A bare figure
names no tree, and a figure that names no tree cannot be corrected, only replaced.

| where | says | can it be edited | disposition |
|---|---|---|---|
| `docs/OneThird-Species-Hopf-Monoids-Repair-Sites.md` §6.1 | 1 | **yes** | **edited in place**, with the reason |
| commit `41ac5d4` | 1 | no — merged history | corrected here |
| commit `b534db7` | 1 | no — merged history | corrected here |
| `code/species_sites_821e/out_a2_6cb9_after.txt` | 1 | **must not be** | it is the record of a run that really happened; editing it to carry a number that run did not produce would be a forgery. Corrected here. **This is the source the two commit messages were copied from.** |
| commit `5c16f5c` (mg-4700's audit) | 2 and 1 | — | already carries the correction beside the old figure |
| `code/species_depth_audit_4700/PREDICTIONS.md` | 1 | — | a **prediction**, already scored `*** MISSED ***` in its own tree's `out_q4_standing.txt`. Reported rather than filtered |
| `code/species_audit_a61f/out_a2_bidigare.txt` | 0 | — | **not this artifact.** A different checker prints the same tag. Named rather than filtered, because an exclusion nobody can see is how a census goes 8 short |

### The sharpening, which is worth more than the number

**Three agreeing statements were not three confirmations.** They were three copies of one run —
`out_a2_6cb9_after.txt` — taken in a worktree whose tree is not the tree the work shipped in.
**Replication is not corroboration when the copies share a source.** Nothing compared the copy to
the artifact for a whole ticket.

### And the ticket's own count, checked against the rows

mg-5040 says *three commit messages say 1*. Measured by `r3_summaries.py`: **two** commit messages
state the old figure with no correction beside it; the third statement of `1` is in a **document**,
and a fourth is the **published transcript** both messages copied. The ticket's "three" is itself a
figure that arrived in a summary, and it is reported against the rows rather than repeated — which is
the same discipline the item asks for, applied to the item.

---

## 6. THIS DELIVERABLE, CHECKED FOR THE DEFECT IT REMEDIES

This is a claim about coverage, repairing claims about coverage. Four kinds of artifact are produced
and each is checked against the OPEN item that could spoil it (`r4_self.py`):

1. **Code that enumerates by walking.** This instrument reads its own files; that walk states its
   bound and names its residue, and R4a fails if the residue carries anything unstated. `r3`'s census
   enumerates with `git ls-files`, which is not a filesystem traversal and so has no depth, symlink
   or extension rule to be silent about — it has **one** bound, *a file that is not tracked is not in
   the census*, and R4a prints every untracked file so that bound is visible.
2. **A shell runner.** R4b **splits this instrument's own `run_all.sh`** and fails if it finds a
   multi-part block of the kind mg-4700 F2 found inert, or a `| tee`.
3. **Figures in prose.** R4c reads every `Rn TOTAL BAD: k` stated in this tree's `README.md`,
   `OUTCOMES.md` and `PREDICTIONS.md` and compares each with the transcript of that run. **It cannot
   check the commit message, which does not exist when it runs** — that hole is named in the run
   rather than left to be noticed, and what closes it is that every figure in the commit message must
   appear in one of those files first.
4. **A pinned comparison.** R4d greps this instrument's own sources for a comparison anchored on
   `HEAD` — mg-821e's defect — and fails if it finds one. The pin is `4372fae`.

### Two branches that cannot exhibit the defect, with the reason stated

* **The mathematics.** Nothing here reads, evaluates or restates a mathematical claim; the checkers
  match sentences and this repair changes which files they read. R4f **measures** rather than asserts
  it: no file under `code/species_7d75` changed, and every added line mentioning theorem/lemma/proof
  is printed for a reader to judge.
* **The auditors' instruments.** mg-6cb9's and mg-4700's batteries make coverage claims of their own
  and are **not** checked here — deliberately, and not because they are safe. An instrument graded by
  the thing it audits has stopped being evidence. They are run unmodified and whatever they say is
  reported. This is not a hole because their claims are *about* this repair, so an error in them
  shows up as a disagreement with these rows rather than as silence.

---

## 7. WHAT THIS DID NOT DO

1. **It did not make any walk total.** Option 2 was available and was not taken; the reason is in the
   code at each of the four sites.
2. **It did not repair the stale-census mechanism.** §4 says what it did instead and what remains.
3. **It did not touch mg-6cb9's or mg-4700's instruments,** or the mathematics.
4. **It did not sweep the class beyond these four checkers.** Every other walk in this repository
   that quantifies over what it enumerated is untouched, and named here rather than closed.

---

## 8. REPRODUCE

```
cd code/species_bound_repair_5040 && sh run_all.sh     # ~25 min, NO NETWORK
cd code/species_extent_d633       && sh run_all.sh
cd code/species_repair_a4ef       && sh run_all.sh     # now prints e2's full output
cd code/species_remainder_f8fa    && sh run_all.sh
cd code/species_repair_6f61       && sh run_all.sh
```
