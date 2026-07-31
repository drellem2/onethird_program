# Independent audit of the mg-821e repair — the walks, the wiring, and the sites

**Target:** mg-821e / `af432ee` + `b534db7` + `41ac5d4`, which repaired mg-6cb9 /
`26c8d5c`, which audited mg-d633 / `e8fbd4f`.
**Audit landed:** mg-4700.
**Instrument:** `code/species_depth_audit_4700`, `sh run_all.sh`, about 6
minutes, no network, 82-assertion self-test.
**Predictions:** `code/species_depth_audit_4700/PREDICTIONS.md`, written and
committed before a single probe ran and not edited since. Two missed; both are
in `code/species_depth_audit_4700/OUTCOMES.md`.

---

## 0. VERDICT

**All three OPEN items are closed, and each at its own grain.** OPEN 3 is closed
cleanly and completely. OPEN 1's walks genuinely recurse. OPEN 2's check
genuinely executes in three of three runners. None of it was taken from the
source or from a commit message: directories were planted, runners were
executed, and mg-6cb9's own battery was re-run unmodified.

Three MAJOR findings, none of which reopens an OPEN item:

1. **The class OPEN 1 was about survives, one directory rule to the side.**
   `os.walk` does not descend into a **symlinked directory**, none of the three
   walks passes `followlinks=True`, and no printed extent contains the word
   `symlink`. A statement planted behind a link leaves `w3_scope.py` silent and
   `e1_extents.py` certifying the extent as TRUE.
2. **The deletion test for OPEN 2 was run at a 20-line unit, two of whose parts
   have no return.** Removing the `||` guard alone changes the message and not
   the verdict; removing the two `echo`s alone leaves all three runners green
   with no trace the check ran — and that printing is the whole of what
   distinguishes this repair from the state mg-6cb9 found.
3. **The committed census is eight files short and `A2 TOTAL BAD` is 2, not the
   1 the repair's own commits report.** Not drift: `af432ee` regenerated the
   artifact and the gap widened. The measurement was true at the commit and false
   at the merge.

Two MINOR: `| tee` still swallows a red self-test in two of the three runners
this repair edited, and the wiring's failure message reports any crash as a
specific finding it did not make.

**Nothing confirmed was weakened.** All four extents are still measured both
ways, `A1 TOTAL BAD` is 0, mg-821e's published transcript of that run is
byte-identical to the live one at 178 of 178 lines, and the cross-section check
still fires three ways in two documents. No mathematics was touched.

---

## 1. OPEN 1 — a contingent extent looks identical to a sound one

mg-6cb9's F1: *EVERY REGULAR FILE in each tree is read* was true, and true for
exactly one reason — no tree under `code/species_*` had a subdirectory. A
contingent extent and a sound one print the same sentence and exit the same way.
The only instrument that separates them is a subdirectory, so this audit read no
walk and planted directories instead.

### 1.1 The condition really was removed, not stated

| probe | planted | `w3_scope.py` | `s1_extent.py` |
|-------|---------|---------------|----------------|
| D1a/b | `species_7d75/sub/leak.md` | exit **1**, path named | exit **1**, `STILL ASSERTED` at `sub/leak.md` |
| D1c | `species_7d75/a/b/c/leak.md` (depth 3) | exit **1** | exit **1** |
| D1d | `species_repair_a4ef/sub/leak.md` | exit 0 — correct, its extent is one tree | exit **1** |
| D1e | `species_7d75/__pycache__/leak.md` | exit 0 | exit 0 |

D1d matters on its own: mg-6cb9 planted only in `code/species_7d75`, and a repair
that fixes the walk it was shown is a different repair from one that fixes the
walk. This one fixes the walk. D1e is the rule measured in the direction that
can only fail — a repair that widened until nothing was excluded would have
passed every row above while quietly dropping the one rule its extent promises.
`__pycache__` is still skipped and still named, in both printed extents.

### 1.2 The guard that did not exist

mg-6cb9's F1 was invisible because `e1_extents.py` — whose job is deciding
whether a printed extent is true — listed the tree the same way its subjects
did. Each walk was reverted to `os.listdir`, one line at a time, with a
subdirectory planted:

| reverted | E1 |
|----------|-----|
| `w3_scope.py` | exit **1** — `reads every regular file of code/species_7d75 (19)  *** FALSE ***` |
| `s1_extent.py` | exit **1** — `reads every non-excluded regular file of all four trees (53)  *** FALSE ***` |
| `e1_extents.py`'s own `regular()` | exit **1** — `the printed file count agrees with what was read  *** FALSE ***` |

The third row is the one this audit predicted would go quiet, on the reasoning
that an expectation shrinking to match a still-recursing subject cannot disagree
with it. It fires, through a different row than the one that reasoning was
about. The prediction is scored a hit and the reasoning is recorded as wrong.

### 1.3 FINDING (MAJOR) — the second condition, still unstated

`os.walk` does not descend into a symlinked directory unless `followlinks=True`.
None of the three walks passes it, and the link is classified into `dirnames`,
so it is never a candidate file either. That is a **second directory rule
carried by no sentence**, and it is invisible today for precisely the reason F1
was invisible: no tree has one.

With the same statement planted behind a link into a directory outside the
repository:

| checker | exit | |
|---------|------|-|
| `w3_scope.py` | 0 | silent |
| `s1_extent.py` | 1 | but its scan read 18 files, **0 below the root**, and reported **0 asserted** |
| `e1_extents.py` | 0 | **certifies the extent as TRUE** |

`s1_extent.py`'s non-zero exit is not the extent working. Its scan is as blind as
the other two; what breaks is control (c), which `shutil.copytree`s the tree into
a scratch copy — with `symlinks=False`, so it **follows** the link and
materialises the planted file as a real one, where the same scan now finds it and
the injection count comes out one high. The reader of that run is told the
injection control is broken. Nothing tells them a forbidden statement is live in
`code/species_7d75`.

The rule is exactly *symlinked **directory***: a symlink to a **file** is read,
because `os.path.isfile` follows it. That is what makes it a directory rule, and
puts it beside `__pycache__` in a sentence that names only `__pycache__`. None of
the three printed extents contains the word `symlink`.

This is the sentence mg-821e itself wrote about `os.listdir`, with `followlinks`
in place of recursion, and it is the reason the finding is MAJOR rather than a
curiosity: the repair removed the instance it was shown and the **class** — an
extent sentence complete about the rule somebody thought of — is intact.

---

## 2. OPEN 2 — verified by running, not by grepping

Presence of a call in a script is not evidence it executes. Every row here is
`sh run_all.sh` from inside its own tree and the runner's own stdout. Twenty-one
executions in all.

### 2.1 The observed output, per script, all three

```
code/species_repair_a4ef      exit 0
      | cross-section check (mg-821e), its own output:
      |   15 file(s) carry a strike, 34 strike(s) measured, 0 standing.
      | E2 TOTAL BAD: 0
code/species_remainder_f8fa   exit 0
      | cross-section check (mg-821e), its own output:
      |   15 file(s) carry a strike, 34 strike(s) measured, 0 standing.
      | E2 TOTAL BAD: 0
code/species_repair_6f61      exit 0
      | cross-section check (mg-821e), its own output:
      |   15 file(s) carry a strike, 34 strike(s) measured, 0 standing.
      | E2 TOTAL BAD: 0
```

3 of 3, where mg-6cb9 measured 0 of 3.

### 2.2 B1 restored on disk — with the control that makes it mean something

A red runner proves the wiring works only if the same document state with the
wiring **removed** is green; otherwise `exit 1` could be `check_doc.py` failing
forty lines earlier and the check never being reached.

| tree | wired, B1 restored | unwired, B1 restored |
|------|--------------------|----------------------|
| `species_repair_a4ef` | exit 1, names `STANDING UN-STRUCK` | exit **0** |
| `species_remainder_f8fa` | exit 1, names `STANDING UN-STRUCK` | exit **0** |
| `species_repair_6f61` | exit 1, names `STANDING UN-STRUCK` | exit **0** |

Caught 3 of 3, green unwired 3 of 3 — the second number is what makes the first
mean anything. And `unwire()` of each runner is **byte-identical** to the file at
the pinned pre-repair ref `af432ee~1`, so "a pure addition" is measured rather
than asserted. The ref is pinned and not `HEAD`: anchored on `HEAD` this row
would have stopped comparing on the day the repair landed, which is the error
`41ac5d4` had to come back and fix.

### 2.3 FINDING (MAJOR) — the block is not one unit

mg-821e deletion-tests the wiring as one 20-line unit. It has three separable
parts, and each was deleted alone:

* **the `|| { … exit 1; }` guard alone**, B1 restored: 3 of 3 still exit 1.
  Under `set -e` a failed command substitution in an assignment already aborts
  the script. Five of twenty lines move the **message**, not the **verdict**.
* **the two `echo`s that print the check's output alone**, clean tree: 3 of 3
  exit 0 with **no sign the check ran at all**. The sentence that distinguishes
  this repair from the state mg-6cb9 found — *the OUTPUT is printed, not just the
  call made* — is guarded by nothing. No self-test and no checker asserts those
  two lines exist.

The call itself is load-bearing and was correctly identified. What is not
supported is that the unit deletion-tested is the unit that has a return.

### 2.4 FINDING (MINOR) — a crash reported as a finding

With `e2_crosssection.py` made to raise, all three runners exit 1 and all three
print `E2 CROSS-SECTION FAILED -- a struck claim stands un-struck elsewhere`,
and none prints a `STANDING UN-STRUCK` line. `stderr` is not captured into
`$E2OUT`, so the traceback goes to the terminal while the one summary line a
transcript reader gets asserts a finding that was never made. Minor: the run does
go red. Reported and not scored.

### 2.5 FINDING (MINOR) — the swallow, in two of the three runners repaired

`41ac5d4` fixed `| tee` in front of `set -e` in mg-821e's own runner and recorded
that every other runner in the arc still has it. Two of those are runners this
repair edited — it added twenty lines to each. With each self-test forced red:

| runner | exit | printed `*** FAILED ***` | |
|--------|------|--------------------------|-|
| `species_repair_a4ef` | **0** | yes | swallowed |
| `species_remainder_f8fa` | **0** | yes | swallowed |
| `species_repair_6f61` | 1 | no | stopped the run |

Ten `run_all.sh` in the repository pipe a self-test through `tee`, so the class
is repo-wide and was disclosed. It is a finding because disclosure in a commit
message is not a guard.

---

## 3. OPEN 3 — the anchors, deleted at the site a reader meets them

**Closed, cleanly, and this is the part of the repair with nothing wrong with
it.** Each of the seven `(site, anchor)` pairs had its anchor deleted from **one
heading region only**, every other copy in the file left standing:

| site | anchor | copies left elsewhere | |
|------|--------|----------------------|-|
| `# Repair of mg-7d75` | the target document | 0 | fires |
| `# Repair of mg-7d75` | `mg-a61f` | **17** | fires |
| `# Repair of mg-7d75` | `code/species_repair_6f61` | 1 | fires |
| `## 11. REPRODUCE` | `code/species_repair_6f61` | 1 | fires |
| `### 2.1` | `2 of 45` | 2 | fires |
| `## 11. REPRODUCE` | `2 of 45` | 2 | fires |
| `## 10.` | `WHAT THIS REPAIR DID NOT DO` | 0 | fires |

**7 of 7.** The same seven mutations against `check_doc.py` at the pinned
pre-repair ref fire **2 of 7** — the five silent rows are exactly mg-6cb9's F3:
the copy a reader meets is gone and the run is green. The figure mg-821e reports
is re-measured here, not quoted.

And it is right in the other direction: a copy of `mg-a61f` deleted at a
**non-site** heading region is silent (multiplicity elsewhere has no vote),
section 10 emptied under its own heading fires, and a **renamed** site heading
fires loudly with `NO SUCH SECTION` rather than going quiet.

**Observed, not scored:** seventeen heading regions of the repair document carry
one of the five anchors and seven are checked. That is not a defect — C4's extent
line says explicitly that a copy elsewhere neither helps nor is required, which
is true and deliberate. What the sweep shows is where the third remedy's cost
sits: the set of reader-facing sites is a judgement written into a table by hand,
and nothing checks the table against the document. A new section that a reader
would meet the instrument's name in joins the unchecked column silently.

---

## 4. WHAT WAS CONFIRMED, AND WAS NOT DISTURBED

mg-6cb9's battery was run **unmodified** rather than re-implemented — a
re-implementation can agree with a weakened subject by being weakened in the same
place.

* `a1_bothways.py`: `A1 TOTAL BAD: 0`. The four extents are still measured in
  both directions at that audit's own sites. `Q17e` still prints red **by
  design** — it runs `e1_extents.py`, whose exit 1 means an extent line is false,
  and mg-6cb9 scores a WIDE row good only at exit 1.
* mg-821e's published transcript of that run, `out_a1_6cb9_after.txt`, is
  **byte-identical** to the live run: 178 of 178 lines.
* `a2_crosssection.py`: `the species trees' run_all.sh reach it  3 of 3  ok`.
  The cross-section check still fires three ways in two documents.

Nothing was weakened.

---

## 5. FINDING (MAJOR) — post-commit is not post-merge

`A2 TOTAL BAD` is **2**. `41ac5d4` says *"Its a2_crosssection.py: A2 TOTAL BAD 1,
the one row being R29 … both F4 rows still read ok against HEAD"*, and `b534db7`
— whose entire subject is publishing the post-commit measurement — says *"A2
TOTAL BAD stays 1."* Live at HEAD, both F4 rows read red:

```
the COMMITTED run's extent line is true at HEAD                *** FALSE, off by 8 ***
the committed CENSUS is right for the shipped tree             *** WRONG ***
```

Counting `*.md` under `docs/` and `code/` from `git` alone, at four named
commits:

| commit | what it is | transcript claims | tree holds | short |
|--------|-----------|-------------------|-----------|-------|
| `e8fbd4f` | mg-d633 wrote the transcript | 100 | 105 | 5 |
| `af432ee` | **mg-821e regenerated it** | 123 | 131 | **8** |
| `HEAD` | the tree it ships in | 123 | 131 | **8** |

**The load-bearing row is `af432ee`, not `HEAD`.** That row is a statement about
a commit fixed in git — the transcript it contains claims 123, the tree it
contains holds 131 — and no later commit can move either number. The `HEAD` row
will move: this audit's own commit adds markdown files under `docs/` and `code/`
and makes the same extent line staler still. That is the mechanism, not a fix,
and it is why the finding is anchored on a pinned commit rather than on `HEAD` —
which is the error `41ac5d4` came back to correct.

This is not a re-run that drifted: `out_e2_crosssection.txt` is a committed
artifact, `af432ee` regenerated it, and mg-6cb9's F4 exists to measure exactly
that line. The gap did not close, it **widened**. mg-821e's own published
transcript records the run that produced 123 as having seen `git ls-tree HEAD --
123`, which is a tree no commit in this history has, and 34 of its 129 lines no
longer reproduce.

**What happened, and the repair did the right thing by the rule it was given.**
This arc's Appendix A says:

> A COMMIT THAT MEASURES SOMETHING IT ALSO MODIFIES MUST PUBLISH THE POST-COMMIT
> MEASUREMENT

`b534db7` obeyed it: it re-ran a2 with the repair landed and both F4 rows turned
`ok`. Then the work was **rebased** onto a main that had grown by eight markdown
files while the ticket was open, and an artifact regenerated against the
pre-rebase HEAD shipped inside a different tree. The rule names a condition —
*the commit* — that a merge queue is free to change underneath it, and nothing
re-checks it afterwards.

That is this repair's own OPEN 1, one level out and in its evidence rather than
its code: a measurement true because of a state of the world nobody had stated.
There it was *no tree has a subdirectory*. Here it is *main has not moved since I
ran this*. The first was removed by construction. The second is stated nowhere,
and it has now gone false twice in the same file.

**What is not affected, stated so the finding is not read as wider than it is:**
e2's verdict. A live run at HEAD reports 0 standing, and section 2.1 above prints
exactly that from inside all three runners. None of the eight unread files
carries a strike that could have changed it. What is false is an extent line on a
committed transcript — which is the kind of claim this arc exists to take
seriously, and the reason the finding is here rather than in a footnote.

---

## 6. THE SHAPE THAT OUTLIVES THE TICKET

Three of the five findings above are one shape, and mg-821e named it in its own
commit message before any of them existed:

> a claim contingent on a condition nobody had stated, which would have gone
> false silently on the day somebody added one

* `no tree has a subdirectory` — removed by construction, correctly (section 1.1).
* `no tree has a symlinked directory` — still standing, still unstated,
  measurably invisible to all three walks and to the instrument that judges them
  (section 1.3).
* `main has not moved since I ran this` — unstated, and false twice in one file
  (section 5).

A repair can remove an instance without touching the class, and the way to tell
which happened is not to read the fix. It is to ask what state of the world the
repaired sentence still assumes, and then to arrange for that state to be
different.

---

## 7. WHAT THIS AUDIT DID NOT DO

It did not touch the mathematics, and did not check any. It did not run
mg-6cb9's `a3_differ_and_placement.py`. It did not audit `e2_crosssection.py`'s
own correctness — mg-d633 and mg-6cb9 measured that and it was re-run here only
as a subject. It did not repair anything: the five findings are reported and
none is fixed, because an auditor that repairs its subject has removed the
evidence for its own report. It says nothing about any tree outside
`code/species_7d75`, `code/species_repair_a4ef`, `code/species_remainder_f8fa`,
`code/species_repair_6f61` and `code/species_extent_d633`.

**One thing this instrument does to its own subject, declared:** its markdown
files live under `code/`, and `e2_crosssection.py` reads every `*.md` under
`code/`, so it raises that checker's file count by its own number of markdown
files. Section 5's numbers are counted from `git` at named commits and are immune
to it. The rest is declared in the run.

## 8. REPRODUCE

    sh code/species_depth_audit_4700/run_all.sh

About 6 minutes, no network, 82-assertion self-test, and it **mutates the
worktree it runs in**, one edit at a time, restoring and proving the restore
after each. `git status --porcelain` and the full `git diff` are compared before
and after every probe; a difference stops the run. Predictions are in
`code/species_depth_audit_4700/PREDICTIONS.md`, written first; the two that
missed, and five defects in this instrument, are in
`code/species_depth_audit_4700/OUTCOMES.md`.
