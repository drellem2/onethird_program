# mg-5040 — OUTCOMES

Scores `PREDICTIONS.md`, which was written before `r1`–`r4` were run and has not been edited. Three
predictions missed, all three in the same section, and all three are kept as written and developed
below — they are the most useful thing this instrument produced.

Figures here are compared against this tree's own transcripts by `r4_self.py` R4c, in the run, so
that a number in this file cannot drift from the run it describes. That check exists because of the
defect OPEN 3 is about.

---

## The bottom line

```
R1 TOTAL BAD: 0      R1 PREDICTIONS MISSED: 3
R2 TOTAL BAD: 0
R3 TOTAL BAD: 0
R4 TOTAL BAD: 0
selftest5040: 26 assertions, 0 failed
```

---

## The three predictions that missed, all at the pin

### P1e — I predicted the pre-repair tree would be SILENT on all four structures. `s1_extent.py` is LOUD on three of them, and never through its extent.

**Predicted:** exit 0 from `s1_extent.py` at `4372fae` for the fifo, the broken symlink and the
unreadable directory. **Got:** exit 1 for the fifo and the unreadable directory, and exit 1 from
`e1_extents.py` for the broken symlink.

And the misses are worth more than the hits. `s1_extent.py`'s control copies the tree with
`shutil.copytree`, which **follows** a symlinked directory and **raises** on a fifo and on a
directory it cannot read. So at the pin the run goes red — and **the diagnosis a reader is handed is
that the injection control broke.** Nothing in it says a forbidden statement is live. mg-4700 found
this shape once, at D2b, and predicted silence everywhere else; it is three of four.

This is why every row in `r1_bound.py` carries a `NAMES IT` column beside the exit code. A probe that
scored the exit code alone would have recorded the pre-repair tree as **catching** three of these
four structures, which it does not.

`e1_extents.py` on a broken symlink named `leak.md` is the fourth, and it is a different mechanism
again: E1's expectation set for `e2_crosssection.py` collects every `*.md` **without** an `isfile`
test, so `want <= got` fails and E1 fires — a real disagreement, reached without any residue and for
a reason unrelated to the extent.

---

## What is closed, and how it was measured

### OPEN 1 — option 1, stated in code

Four structures, four checkers, planted in the real worktree and restored with the proof shown:

* a **symlinked directory**: 4 of 4 fire, 4 of 4 name it. At the pin: `w3_scope` silent,
  `e1_extents` **certifies the extent as true**, `e2_crosssection` silent.
* a **fifo**: 3 of 3 in-extent checkers fire. `e2_crosssection` is silent **and that is correct** —
  a fifo not named `*.md` is not in its extent, and scoring it would be asking a checker to widen a
  claim to cover a probe. Not scored, with the reason printed.
* a **broken symlink named `leak.md`**: 4 of 4 fire. It is named `leak.md` precisely so that it *is*
  inside `e2`'s stated extent and `e2` can be scored on it.
* a **directory with mode `000`**: the three tree-walking checkers fire naming `PermissionError` —
  a case `os.walk` swallows entirely unless `onerror` is passed.

**Two of those four are structures no extent line in this repository has ever mentioned, and no line
of the repair knows they exist.** That is the evidence that the residue is a measurement rather than
a list of remembered rules.

`e1_extents.py` fires **on a row `want <= got` cannot reach**: R1d shows it exiting 1 with every
`reads every …` inclusion row still `ok` and the residue row the one that fails.

### OPEN 2 — the structure removed, not a fourth level added

* the rewired block has **2** non-comment lines; deleting the `python3` line makes 3 of 3 runners
  exit 0 **with no trace the check ran**, and deleting the `echo` heading leaves 3 of 3 red with the
  full output present. One unit, one return.
* at the pin the same split by line gives **6** parts, of which **4 are inert** (the runner still
  exits 1 without them), **1 is load-bearing**, and **1 leaves a script that does not parse** — which
  is reported separately, because "inert" and "no longer valid shell" are not the same thing and a
  two-way split would hide one inside the other.
* mg-4700 split the old block into **3** parts by hand; by line it is **6**. **That the two counts
  disagree is the finding.**
* mg-4700's **F5** is closed as a side effect: with `e2` made to raise, 3 of 3 runners exit 1 and
  **0 of 3** claim `a struck claim stands un-struck elsewhere`. The guard that made the claim is gone.

### OPEN 3 — the rows win, and the copies are counted

`a2_crosssection.py` run unmodified **at `4372fae`, the tree those summaries shipped in**, reports
**`A2 TOTAL BAD: 2`**; run in this worktree it reports **1**, because this ticket regenerates the
census and turns one of the two rows green. **Only the first grades anything**, and the second is
printed beside it. Every copy of the figure was
enumerated from git — commit messages reachable from the pin, and every tracked file at the pin and
in this worktree — and every copy has a printed disposition. The one editable copy, in
`docs/OneThird-Species-Hopf-Monoids-Repair-Sites.md`, is corrected in place with the reason. Two
commit messages and one published transcript cannot be edited and are corrected in §5 of
`docs/OneThird-Species-Hopf-Monoids-Bound-Repair.md`.

**The ticket's own count is checked against the rows and does not match it.** mg-5040 says three
commit messages say `1`. Measured: **two** commit messages state the old figure with nothing beside
it; the third statement is in a **document**; and the **fourth** is the published transcript both
messages were copied from. The instrument reports its measurement rather than the ticket's figure,
which is the discipline OPEN 3 asks for applied to OPEN 3.

**The sharpening.** The agreeing summaries were not independent. They were copies of one run, taken
in a worktree whose tree is not the tree the work shipped in. Replication is not corroboration when
the copies share a source.

---

## Defects in this instrument, kept

1. **The restore proof passed while the tree was dirty.** `git status --porcelain` **collapses an
   untracked directory to a single line**, and this instrument's own directory is untracked until it
   is committed — so a probe that deliberately left a file inside it was reported as *restored*. The
   self-test caught it only because it asserts the restore contract **in the direction that must
   fail**. Fixed with `--untracked-files=all`; the assertion that found it is still there.
2. **The first restore contract did not cover files the probe never wrote.** `r2` executes
   `run_all.sh`, and a runner **regenerates the committed `out_*.txt` beside it**. The first version
   of `Probe` restored only what it had written and then reported, correctly, that the tree was not
   restored — with the reason nowhere in sight. It now snapshots every tracked file at entry.
3. **The first B1 probe produced a red that proved nothing.** It appended the restated claim to a
   document those runners' own checkers also read, and 2 of 3 went red **without** printing
   `STANDING UN-STRUCK`. The document was changed to one carrying a strike that only `e2` reads.
4. **The first "different checker" rule excluded the wrong artifact.** A transcript need not name its
   own producer, and `out_a2_6cb9_after.txt` — the single artifact §5 is about — was filtered out for
   not containing the string `a2_crosssection`. The rule now takes its markers from the artifact's
   own live output.
5. **The self-test imported a script and ran a whole checker.** `from s1_extent import walk_residue`
   executes `s1_extent.py`. The function is now lifted out of the file by parsing it, which has the
   side benefit that the test reads the code that ships rather than a copy of it.
6. **A `cd` in an early shell command persisted**, exactly as mg-4700 recorded of its own instrument.
   Every path here is absolute or `REPO`-relative.
7. **`r3` graded the summaries against a figure this ticket had moved.** `A2 TOTAL BAD` is a property
   of a tree; regenerating the census turns one of its two rows green, so a live run in this
   worktree reports `1` — and the correction would have been marked wrong by a number the correction
   caused. **F3, one level out, inside the file repairing F3.** The artifact is now run at the pinned
   revision in a git repository initialised from the extraction, and only that run grades anything.

---

## Extent of this deliverable

Four sections over one repair. It covers mg-4700's three OPEN items by planting structures,
executing runners, and enumerating figures from `git`. It says **nothing** about the mathematics of
the species tree; nothing about any walk in this repository outside the four checkers named in
`kern5040.CHECKERS`; nothing about whether `e2_crosssection.py` is the right check; nothing about
mg-6cb9's or mg-4700's instruments, which are run unmodified and never graded; and nothing about the
17 runners mg-c2b3 swept beyond the three rewired here.

`Rn TOTAL BAD` counts outcomes that contradict **this repair's own claims**. `R1 PREDICTIONS MISSED`
counts predictions that were wrong. **The two are separate on purpose.**
