# mg-6ef4 — OUTCOMES

Scores `PREDICTIONS.md`, which was committed in `b2a849b` **before any probe ran** and has not been
edited. Three predictions missed. All three are kept as written and developed below, and two of them
are the most useful thing this instrument produced.

---

## The bottom line

```
selftest6ef4: 30 assertions, 0 failed
T1 TOTAL BAD: 9      T1 PREDICTIONS MISSED: 0
T2 TOTAL BAD: 4      T2 PREDICTIONS MISSED: 0
T3 TOTAL BAD: 5      T3 PREDICTIONS MISSED: 1
T4 TOTAL BAD: 4      T4 PREDICTIONS MISSED: 1
```

**mg-5040 SUBTRACTED. It did not widen a third time.** `followlinks=True` was not added, the word
"total" was not used, and the walk returns its own residue with an unstated entry counted into the
checker's own `TOTAL BAD`. `t1_bound.py` T1a shows the residue mechanism working on the shipped
functions, and `t2_wiring.py` T2a shows the twenty-line block reduced to two lines with one return.
Every one of the three OPEN items moved in the right direction.

The findings are about **where the subtraction stops**.

---

## The predictions that missed

### P1f — I predicted `s1_extent.py` would exit 1 without naming the planted file. It names it, and my own predicate was wrong about what naming means

**Predicted:** `(1, NAMES IT: no)`. **Got, on the first instrument:** `(1, NAMES IT: yes)` — and the
`yes` was **my instrument's defect, not a fact about the checker**. `s1_extent.py` prints a legend
line reading `!! = STILL ASSERTED` in every run it ever makes, and the predicate asked whether that
string and the planted filename both appeared **anywhere** in the run. It reported a catch from a
checker that had died before reaching its own verdict.

Fixed to require both on **one line**, and a `verdict` column added asking whether the checker
printed its own `TOTAL BAD` line at all. Measured again: exit 1, `CAUGHT` **no**, verdict **NO** —
`shutil.copytree` raises `Permission denied` on the planted file and the run never reaches
`S1 TOTAL BAD`. The prediction is scored as a hit against the corrected predicate and this paragraph
is why a reader should discount that. `selftest6ef4.py` now asserts the predicate is silent on a
legend line, on a real hit line, and on a filename that sits on a different line from the marker.

### P3f — I predicted 3 distinct message texts; there are 5

**Predicted:** 3. **Got:** 5, across **10 commit objects** — every one of the five has a rebase twin.
The direction was right (P3e, "more than mg-5040's two", is a hit) and the size was not. I reasoned
from the commits visible on the branch and did not count the ones a merge queue had already
duplicated.

### P4a — I predicted `kern5040.Probe` would not notice a tracked file left at mode `000`. It notices, and the reason it notices is the finding

**Predicted:** `restored=True`. **Got:** `restored=False`.

And the miss is worth more than the prediction was. It notices because **git cannot read a `000`
file**, so `git status --porcelain` reports it as **modified** — although not one byte of it changed.
Right verdict, wrong reason: a reader is told the content moved and it did not. That is mg-4700's D2b
in the harness instead of in a subject.

So a second mode was probed, chosen precisely because it is the case the proof is actually about:
**`400`** — readable by git, executable bit unchanged. `kern5040.Probe` reports **RESTORED** and the
file is not restored. Both rows are in `out_t4_restore.txt`, and the mode-aware control in T4b names
both.

---

## Findings

### F1 — MAJOR. The residue was installed at the WALK. The file set has two layers, and layer 2 still declines in silence

`t1_bound.py` T1b/T1bb/T1d. The set these four checkers quantify over is built twice:

```
layer 1   os.walk           -- which entries are REACHED     <- walk_residue names everything
layer 2   open(...).read()  -- which reached entries are READ <- except (UnicodeDecodeError, OSError)
```

A **regular file this process cannot open** passes layer 1 (`os.path.isfile` is true), so the residue
is empty; fails layer 2 with `PermissionError`, which is an `OSError`; and is filed under a printed
sentence that says the reason was the file's **encoding**. That bucket is printed and is **not**
counted into `bad`.

Measured, with a live X4 statement planted in `code/species_7d75` at mode `000`, against a no-plant
baseline and two controls:

| checker | exit | names file | CAUGHT | verdict printed | residue |
|---|---|---|---|---|---|
| `w3_scope.py` | **0** | yes | **no** | — | **0** |
| `s1_extent.py` | 1 | yes | no | **NO** | 0 |
| `e1_extents.py` | 1 | no | no | yes | 0 |
| `e2_crosssection.py` | 0 | no | no | yes | 0 |

* **`w3_scope.py` is silent.** `code/species_7d75` is that checker's entire extent and it now holds a
  live X4 statement. Exit 0, same as baseline. The **attribution control** — the identical statement
  in a *readable* file — is exit 1 and names it, so the silence is the mode and not the statement.
* **`s1_extent.py` is loud for the wrong reason.** It never prints `S1 TOTAL BAD`: `shutil.copytree`
  in its own injection control raises `Permission denied`. The diagnosis a reader is handed is that
  the **control** broke. mg-4700 found this shape once (D2b) and mg-5040 found it three times out of
  four (P1e); this is a fourth structure, and neither of them planted it.
* **`e1_extents.py` certifies the extent as TRUE.** Its row *reads every non-excluded regular file of
  all four trees (53)* reads `ok`. `trace_open.py` records the path **before** calling the real
  `open`, so an attempt that raises is recorded as a read and `want <= got` holds. mg-5040's answer to
  "an instrument that computes its expectation the subject's way cannot disagree with the subject" was
  to make E1 walk independently — and here the two agree anyway, through the **tracer** instead of
  through the walk. E1 does go red, on two **count** rows, which say the printed number disagrees and
  say nothing about a file that was not read.
* **The two layer-2 worlds are byte-identical on stdout.** An unreadable-but-valid file and a
  genuinely undecodable one produce the same sentence:
  `(skipped as not UTF-8 text: leak6ef4.py; skipped as __pycache__: the whole directory rule)`.

**At the runner level, which is what a reader meets:** with the plant on disk,
`code/species_remainder_f8fa/run_all.sh` — the runner that executes `w3_scope.py` — **exits 0**, and
so does `species_repair_6f61`. One of three goes red, through the `copytree` crash, and **0 of 1** red
runners print `STILL ASSERTED` against the planted file.

**This is not a regression.** T1c runs the same plant against `4372fae` and the pre-repair tree is
silent in exactly the same way. It is a **generation the subtraction did not reach**, and T1c is
printed and deliberately not scored for that reason.

### F2 — MAJOR. Two mismatches between the printed bound and the code, both in the enumerator

`t1_bound.py` T1a, measured on the functions lifted out of the shipped files by parsing them.

1. **`walk_residue`'s first statement is `if not os.path.isdir(root): return files, stated, unstated`
   — an entire root declined with EMPTY residue**, in 3 of 3 copies, in the function whose stated
   contract is that nothing is dropped without landing in one of the last two lists.
2. **The printed bound says the walk "reads no entry that is not a regular file".** `os.path.isfile`
   follows symlinks, so a symlink to a regular file is returned in `files` and is not in the residue.
   The sentence is false in the direction nobody checks.

Neither is reachable by planting anything in a tree. They are properties of the enumerator, and they
are the two places it stops being a measurement and goes back to being a rule somebody wrote down.

### F3 — MAJOR. The fifth rung is not a finer grain. It is `set -e`, one line, outside every deletion population this arc has used

`t2_wiring.py` T2e/T2f. mg-5040 did **not** add a fourth level of granularity in the sense the ticket
feared — it removed structure until the by-line test fits. The block is 2 non-comment lines with
exactly one return, and mg-5040 measured that honestly. But the runners' own comment says it plainly:

> `set -e` carries the verdict, which is what it was already doing.

`set -e` sits 53, 60 and 43 lines above the call, and it is in **no** deletion population: mg-821e's
`p3_wiring.py`, mg-4700's `q2_wiring.py` and mg-5040's `r2_wiring.py` each enumerate **the block**.

Measured, with e2 forced red by one planted markdown file and the three runners executed:

| state | a4ef | f8fa | 6f61 |
|---|---|---|---|
| unmodified (attribution control) | 1 | 1 | 1 — all three print `STANDING UN-STRUCK` |
| `echo` heading deleted alone | 1 | 1 | 1 — e2's full output present. **Inert.** |
| `python3` call deleted alone | 0 | 0 | 0 — no trace the check ran |
| **`set -e` deleted alone** | **0** | **0** | **0** — and 3 of 3 print e2's finding IN FULL |

The check runs. Its output is printed. The runner is green. That is mg-6cb9's F2 exactly, reached by
deleting one line no deletion test in this arc has ever had in its population — and no refinement of
the **grain** reaches it, because the problem is the **scope**. The levels went gate (mg-9220) →
clause (mg-64b6) → twenty-line block (mg-4700) → line (mg-5040), each smaller than the last, and the
statement carrying the return was outside all four.

**Also:** the by-line test still has an inert part, 1 of 2 where mg-4700 found 2 of 3, and **0 of 4**
`.py` files that mention the heading string require it — every one of them is a deletion-test
instrument that names the line in order to remove it, this one included.

### F4 — MAJOR. The figure rests on two derivations that disagree, and the copies were never evidence

`t3_census.py` T3d/T3e/T3f.

* **The census is re-derived and mg-4700's numbers hold exactly.** From tree objects alone:
  `e8fbd4f` claims 100, holds 105 (short 5); `af432ee` claims 123, holds 131 (**short 8**).
* **`A2 TOTAL BAD` exists as 10 commit objects and 5 distinct texts** — every one of the five has a
  rebase twin. mg-5040 reported "two commit messages". Neither an object count nor a text count is
  wrong; the sentence does not say which it is, and in a rebased history they are not the same
  number. **44 file occurrences** exist besides.
* **THE SOURCE.** Exactly **two** artifacts in this repository are transcripts of a run of
  `a2_crosssection.py` — identified by markers lifted from that script's own source, at 67 and 59
  markers against 5, 4, 3, 3, 3 for everything that merely quotes it. They say **2** and **1**.
  `code/species_extent_audit_6cb9/out_a2_crosssection.txt` says **2** and was committed **first**;
  `code/species_sites_821e/out_a2_6cb9_after.txt` says **1** and is the one every commit message
  copied. **53 copies rest on 2 derivations, and the derivations disagree.** A contradicting
  measurement was in the tree the whole time and nothing in the arc compared them.
* **3 committed files at HEAD still state the old figure bare**, including
  `code/species_sites_821e/out_a2_6cb9_after.txt:119` — the source itself.
* **3 committed census figures at HEAD name no revision at all.** mg-5040's `MEASURED AT <rev>`
  makes a committed copy STALE rather than WRONG, and it is forward-only: the population it does not
  cover is named nowhere in mg-5040.

### F5 — MINOR, and the floor item. `kern5040.Probe`'s restore proof is blind to a permission mode

`t4_restore.py`. **Chosen because nothing in the ticket names it**, and because T1 has to `chmod` a
tracked file to ask its question at all — so the first thing to ask of a borrowed harness was whether
it would have noticed.

* `chmod 400` on a tracked file, left unrestored: **`restored=True`**. `git status --porcelain` and
  the full `git diff` carry one bit of a file's mode, and `Probe` snapshots bytes and never stats.
* `chmod 000`: `restored=False` — for the wrong reason, above.
* A tracked file **unreadable at entry** is **absent from `Probe.snapshot`** (`except OSError: pass`),
  therefore un-restorable, and there is no field that says so. Same `except OSError` as the checkers'
  layer 2 in F1, in the harness that measured them.
* `selftest5040.py` has **14** assertions mentioning `restored` and **0** mentioning a mode. It tests
  the contract in the direction that must fail — for the one class it had already thought of.
* `__enter__` is byte-identical at `cada54f`, the commit that published the harness, so this is not
  something the audit introduced by running it in a worktree it was not written for.

**No probe in mg-5040 is shown to have left the tree broken, and this section does not claim one
did.** What is measured is that if one had, in this class, the proof would have said RESTORED.

---

## What is confirmed, and was not disturbed

* **It subtracted.** No `followlinks=True` anywhere; the word "total" is not used; the residue is
  computed, printed, and counted into `bad`. T1a shows it working, and the two mismatches are at the
  edges of the enumerator rather than in its idea.
* **OPEN 2's structure really was reduced.** 2 non-comment lines, 1 with a return, in 3 of 3 runners,
  and mg-5040's count of the pin's block at 6 parts against mg-4700's hand-split 3 is reproduced by
  the same by-line rule here.
* **mg-4700's F5 is closed.** The `||` guard that reported any crash as `a struck claim stands
  un-struck elsewhere` is gone; with the call deleted, no runner claims a finding e2 never made.
* **The census numbers mg-4700 raised are right**, re-derived from tree objects by a different
  instrument: 5 short at `e8fbd4f`, 8 short at `af432ee`.
* **mg-5040 was right about the ticket's own figure.** The ticket said three commit messages; the
  message-side population is larger and differently shaped than either number, and mg-5040's
  refusal to take the ticket's figure was the correct move.
* **T3dd fired at nothing, and it is kept.** It was built to catch mg-5040's own evidence commit
  stating the figure bare — a copy its pinned enumeration could not have contained. Measured: the
  paragraph carrying that figure names `cada54f` twice, and `cada54f` is the tree the figure is
  about. The bound on a pinned enumeration is real; the copy it could not see was anchored anyway.

Nothing above was weakened. No mathematics was touched.

---

## Defects in this instrument, kept

1. **The catch predicate matched a legend line.** Developed under P1f above. It reported three
   catches that had not happened, including one from a checker that crashed before its own verdict.
   The self-test now asserts it in the direction that must fail.
2. **The first restore put every file back at `0o644`** and silently un-executabled three
   `run_all.sh`. It was caught by this class's own **mode** proof — the one direction a restore
   checker is worth anything in — and `write()` now remembers the previous mode beside the previous
   bytes.
3. **`git log --all --no-walk` lists REF TIPS, not history.** T3d called that "every commit reachable
   from every ref" and examined 123 objects instead of 292. The population sentence would have been
   false about the population the instrument actually took, in the section about populations.
4. **A bare `(\d+) markdown file\(s\)` is not a census.** That string occurs in three unrelated senses
   here, and the first version of T3b pulled an instrument's declaration of its own markdown count
   into a column of census claims. The two spellings that state a census are matched and nothing else.
5. **The marker rule for "derivation" was a magic number.** At 2 markers it classified nothing; at 3
   it classified five quoting documents as derivations. It is now a quarter of the producer's own
   printable literals, the count is printed for every candidate, and the two populations are 67/59
   against 5/4/3/3/3 — visibly not close.
6. **A run was killed mid-probe, twice, and each time left three `run_all.sh` with `set -e`
   deleted.** The restore is inside the process. `README.md` now says so and says the one command
   that puts it back.
7. **Two probe processes ran against the same worktree at once.** A backgrounded run that looked dead
   was alive; the two trampled each other's plants and one reported a restore failure the other had
   caused. Every measurement in this file comes from a single run of `run_all.sh` afterwards.
8. **Editing a tracked file while a probe is running gets the edit reverted.** `Probe6ef4` snapshots
   every tracked file's bytes at entry and writes them back at exit, so a section added to
   `t3_census.py` mid-run vanished without a word. It is the hazard mg-5040 recorded of mg-4700's
   restore contract, in the instrument written after reading that sentence.
9. **This instrument perturbs the census it audits.** Its markdown sits under `code/`. `t3_census.py`
   counts from tree objects at named revisions and is immune; the perturbation is declared in
   `README.md` and this ticket's own figure occurrences are listed separately in T3e with the reason.

---

## Extent of this audit

Four sections over one repair. It covers mg-5040's three OPEN items by planting structures in the
real worktree, executing runners, lifting the shipped enumerators, and counting from `git` tree and
commit objects.

It says **nothing** about the mathematics of the species tree; nothing about any walk outside the
four checkers in `kern6ef4.CHECKERS`; nothing about whether `e2_crosssection.py` is the right check;
nothing about the other 14 `run_all.sh` mg-c2b3 swept; nothing about any step in the three runners
other than the cross-section block; nothing about untracked files or deleted branches in the figure
census; and nothing about whether `A2 TOTAL BAD` is 1 or 2 — only about how many times it was copied
and how many times it was derived.

`Tn TOTAL BAD` counts outcomes that contradict **mg-5040's own claims**. `Tn PREDICTIONS MISSED`
counts predictions in `PREDICTIONS.md` that were wrong. **The two are separate on purpose.**
