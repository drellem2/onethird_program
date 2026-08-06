# mg-1d26 — the verdict path's other 551 lines, certified

Repairs the hole mg-d53d found in the mg-4adb deletion-population repair: **six
deletions outside the certified population turn a red gate green, four of them
silently**, and one of them makes the checker **read no document, say nothing
and return 0.**

```
MG1D26_WORKERS=6 sh code/verdict_path_repair_1d26/run_all.sh    # about 25 minutes
```

Pure Python 3, no dependencies, no network. `git` is used against this
repository, which is local. `PREDICTIONS.md` was committed in `28c8029` **before
any script in this directory existed** — the tree of that commit contains that
file and nothing else of this instrument — and has not been edited.
`OUTCOMES.md` scores every line of it, and the misses are kept as written.

---

## Correcting the framing the ticket asked me to correct

The ticket says every figure in it is mg-d53d's, recovered from commit messages,
and asks to be corrected. Four corrections, each of them a measurement in
`out_run_all_1d26.txt`:

**1. mg-d53d's six reproduce exactly — but only on a tree with one finding in
it.** The six are the six, 4 silent and 2 loud, re-derived by an instrument that
shares no code with mg-d53d and does not read its transcripts. But **this tree is
already red**, and a second live finding *masks* one of them: with nothing
neutralised, deleting `kernd633.py:127` leaves the checker exiting 1, because an
unrelated occurrence is still firing. Five of the six, not six. mg-d53d's
measurement was conditional on a tree whose only finding was its own plant, and
nothing in its report says so. `P2a` neutralises exactly one named document in
the sandbox and proves the sandbox green before any deletion is made.

**2. The vacuous-pass line is not one line. It is two, and a third comes within
one directory of it.** The ticket names `e2_crosssection.py:52` (`FILES += _f`).
`kernd633.py:196` — the `os.walk` header — **also leaves the population
completely empty**: measured, not argued, by the repaired checker exiting `2`
(`FOUND NOTHING TO CHECK`) on both. `kernd633.py:205` (`else:`) shrinks the
population to the top level of `docs/` instead of emptying it. Three of the six
are population defects and two of them are the *same* vacuous pass.

**3. Both parent instruments' clean-tree controls are false of this tree.**
mg-4adb's V1b (`3 of 3 runners are GREEN on a clean tree`) and mg-d53d's G1b
(`3 of 3 runners GREEN on a clean tree and e2 silent`) were true when they ran.
At the commit this ticket was written against, `e2_crosssection.py` exits **1**
over a live standing occurrence in `code/face_geometry_repair_e35b/README.md` —
struck at line 39, asserted live at line 36, planted by nobody. That is a real
cross-section finding doing what e2 exists to do. **It is not repaired here** and
it is not a defect of anything this ticket touches; it is disclosed in
`PREDICTIONS.md` as D2, measured in `P2a`, and named so that the next reader of
either parent's transcript is not misled by a row that has since gone false.

**4. Python's indentation is not the safety net mg-d53d's Q6 hoped for; it is
the mechanism of the silence.** `PREDICTIONS.md` P4b predicted `kernd633:196`
and `:205` would raise `IndentationError` and therefore be *held* gates rather
than lost ones. **Refuted, both.** Deleting the `os.walk` header does not
un-indent anything — it re-parents the loop body into the `onerror` function
defined immediately above it, so the walk function returns three empty lists and
says nothing. Deleting the `else:` re-parents `keep.append(d)` into the
`elif os.path.islink(p)` branch above it, so only symlinked directories are
descended into. Neither raises. Both are silent. **A deleted line that changes
which block the next line belongs to is the most dangerous member of this
population and nothing in this arc had named it.**

---

## The population, derived rather than inherited

The whole defect is that a certified population was narrower than believed, so
re-using the certification's own boundary reproduces the error. `p1_population.py`
does not read mg-d53d's five-file list. It applies a rule, outward from the
runner:

> the verdict path is the runner file, plus the script its **last command**
> invokes, plus the transitive closure of that script's repository-local imports.

Applied to all three runners it returns **five files**, and the same five — a
reproduction, with the closure printed file by file and every unresolved import
returned rather than dropped. mg-4adb's certificate, parsed out of its own
transcript, is **255 rows over 3 files**. The other two files carry the verdict
and have no certificate. `selftest1d26.py` S8 gives the rule a toy tree whose
answer is known, including a runner whose last command is not a `python3` call —
the row that must say no.

Every count in this instrument is printed with **the population it is over and
the grain of the value**. `806` is the line grain over five files *at mg-d53d's
tree*; this repair adds lines to two of them, so the same population is `1042`
lines here. Those are not the same number and they are not a disagreement.

## What the repair is

Four mechanisms, in `kernd633.py` and `e2_crosssection.py`. None of them is a
list of lines, and none of them is an exclusion.

**1. The dead man's switch — `arm_verdict()` / `deliver()`.**
`sys.exit(1 if bad else 0)` as the last line of a checker is a line whose
*deletion exits 0*: CPython gives status 0 to a process that runs off the end of
its own module, so losing the verdict **was** a pass. `arm_verdict()` registers
a shutdown handler; a process that never reached `deliver` exits **9** and says
`NO VERDICT WAS DELIVERED`. It is a call and not an import side effect because
`e1_extents.py`, `e3_bothways.py` and `selftestd633.py` import the same kernel
and do not deliver through it — arming them would redden three runs that are not
lying about anything, and `P3c` has that as a row that must say no.

**2. `returned 0` and `examined nothing` are now different states, in the exit
code and in the output.** `deliver` prints the population size on **every** run,
passes included, and an empty population gets its own exit code (**2**) and its
own sentence (`FOUND NOTHING TO CHECK — THIS IS NOT A PASS`). `P3b` calls the
floor directly with five inputs, two of which must still be green: a floor that
reddened a real clean run would be the same defect with the sign flipped.

**3. The population is counted twice, by enumerations sharing no line.**
`os.walk` with a stated residue (mg-5040's), and `glob` with `**`. A single
deleted line can break either; it cannot make the two **agree** on a population
that is wrong. Disagreement is a finding with both deltas **named**, never
summarised as a count. This is what catches `kernd633:205`.

**4. The verdict is computed twice and the two must agree.** The running counter
`bad`, and a recount off the rows that were actually printed. `bad += len(fires)`
deleted, the rows still say `STANDING UN-STRUCK` and the counter says 0 — and a
verdict a reader can see contradicted by the rows above it is not a verdict. This
is what catches `e2_crosssection.py:144`.

**And one control battery had a direction, which is itself a population.**
`kernd633:127` is `spans.append((prev, len(text)))` — the token span *after the
last strike*. Deleted, every restatement that **follows** its own strike becomes
invisible, and all five of E2b's controls stay green, because every one of them
restates the claim **before** the strike. Controls `(f)` and `(g)` are the two
directions, as two rows: a single row over "either direction" would pass on the
strength of the one that still works.

## The demonstration, which is the point

`P2b` sweeps **every line** of both files at their pre-repair content — carried
in this directory as `pre1d26_e2_crosssection.py` and `pre1d26_kernd633.py`,
byte-identical copies and **not a SHA**, because the refinery rebases and a
recorded revision is displaced on `main` (mg-c067, mg-a74f). `P2c` sweeps every
line of both files as repaired, **including every line the repair itself adds**.
`P2d` then deletes each of mg-d53d's six again and runs **all three species
runners** over it — eighteen rows, printed one per line, because e2's own exit
code is not what a reader sees. `P2e` records what each of the six now *prints*
while going red: mg-1d26's third instruction is *loud before impossible*.

The six are addressed **by content**, never by line number — this repair edits
both files, so all six of mg-d53d's line numbers are already wrong (mg-7522's
S3). `locate()` refuses an entry that does not match exactly once, and
`selftest1d26.py` S1 gives it three inputs on which refusing is the right answer.
The one line whose *text* changed carries its correspondence in writing:
`sys.exit(1 if bad else 0)` **was** the only line in e2 that could deliver a
verdict and `deliver("E2", …)` **is**.

## Defects of this instrument, kept

**1. The repair's own first run was defeatable, and the sweep is what found it.**
`P2c`'s first run reported **one** `GATE LOST`: `kernd633.py:172`, the
`sys.exit(1 if bad else 0)` **inside `deliver` itself**. The switch recorded the
*fact* of a verdict, so deleting the exit recorded it, returned normally and
exited 0 — this ticket's own defect, one function inside its own repair.
`PREDICTIONS.md` P4c said the first run would go red for exactly that kind of
reason; the transcript of that run is committed as
**`out_p2_FIRSTRUN_one_lost.txt`** and is not tidied away. The switch now records
the **exit code** and returns it, so the verdict is carried by two lines and
either alone delivers it. `P3c` has both halves as rows.

**2. The sweep needs a tree with one finding in it, and it makes one.**
`neutralise()` strips the strike markers from one named document in the sandbox.
Without it, four of the six measure `GATE HELD` for a reason that has nothing to
do with the gate. It is stated, the file is named, the count of markers removed
is printed, `P2a` proves the sandbox is green afterwards, and it is never done to
the worktree. It is still an instrument that edits the tree it measures, and no
row here is a fact about the unedited tree.

**3. `attribution()` reports the first sentence it recognises, not the one that
caused the red.** In `P2e`, two of the six are attributed to *the cross-section
finding itself* because `STANDING UN-STRUCK` is printed in those runs and comes
first in the list, although what produced the red was the two-witness
disagreement in one case and the dead man's switch in the other. **The exit code
is the reliable column** — `2` is the empty-population floor and `9` is the
switch — and the attribution column should be read as *this sentence was
present*, not *this control fired*.

**4. `GATE HELD, UNATTRIBUTED` is 189 of 803 rows and this repair does not
reduce it.** Those are deletions that leave a traceback: red, and nothing in the
output names which control fired. mg-1d26's instruction is that a deletion must
not change the **verdict** silently, and a traceback changes nothing silently —
so these are counted and printed rather than filed as findings. They are also
the reason the disposition vocabulary here has four states and mg-d53d's had
three: `died before the gate` collapses *crashed* with *a different control
fired and said so*, and this repair adds five controls whose whole purpose is to
fire instead of the finding.

**5. `attribution()` is a fixed list of strings this repository prints.** A
control that fires with a sentence nobody added to `ATTRIBUTIONS` is scored
`UNATTRIBUTED`, which is wrong in the direction of noise rather than silence.
`selftest1d26.py` S4 checks each string and checks that a traceback matches
none — but a *new* control's sentence is invisible to it until somebody adds it.

## The result, in one table

| | before this repair | after |
|---|---|---|
| deletions outside mg-4adb's certificate that leave the gate green | **6** | **0** |
| of those, silent | **4** | **0** |
| lines swept, outside that certificate | 551 | **803**, every line of both repaired files |
| runner executions over the six at the repaired tree | — | **18 of 18 red** |
| the six, each naming a control in its own output | 2 of 6 | **6 of 6** |
| distinct kinds of red the six now produce | 1 | **3** — a finding (1), an empty population (2), no verdict at all (9) |
| the verdict path, derived | 806 lines at mg-d53d's tree | **1058** at this one |

## What is still open

1. **Deletions are one line at a time.** Two lines deleted together, and a line
   *edited* rather than removed, are outside every number here. The dead man's
   switch is explicitly a two-line redundancy, so a two-line deletion defeats it
   and that is stated rather than discovered.
2. **The 255 runner lines are not re-swept here.** mg-4adb's certificate covers
   them and mg-d53d reproduced it row for row; this instrument reads that
   certificate's *extent* and takes its *contents* on the strength of two
   independent measurements rather than a third.
3. **`code/species_7d75/run_all.sh` is unrepaired** — mg-d53d's G5: six
   unconditional `sys.exit(0)`s and a `grep` for a gate. This ticket does not
   name it and has not touched it.
4. **mg-d53d's G2 sentinel** — `(cannot be told from the output)` counted as a
   member of the set of catcher names — is a defect of mg-d53d's own instrument
   and is not touched here.
5. **The live occurrence in `code/face_geometry_repair_e35b/README.md` is not
   repaired.** It is reported, and the two parent rows it falsifies are reported
   with it.
6. **`e2` still has no bucket for an unreadable `*.md`** (mg-d53d's G3f). The
   population is now counted twice, and both enumerations would fail the same
   way on a file they can see and cannot read.

## What I did not do

I did not run mg-d53d's suite, mg-4adb's suite, or any of the four species
runners' own checkers other than by executing the three runners whole. I did not
re-derive mg-d53d's 806 by deleting 806 lines — I swept the 551 that had no
certificate, twice, and read mg-4adb's 255 out of its transcript as an extent.
I did not measure any failure mode of the checker other than the planted
occurrence. I did not repair, and did not attempt to repair, any of the six
items above.

## Why there is no `out_p2_widened.txt`

`p2_widened.py` carries this repair's primary claim, so it is `run_all.sh`'s last
command and its exit status is the file's. Redirecting it to a transcript and
`cat`ing the transcript afterwards would put a `cat` after the gate — a command
whose status is 0 whatever P2 returned. That is the defect mg-c2b3 found in these
runners as a `tee`, mg-6ef4 found again as `set -e`, and mg-4adb repaired by
making the gate the last command. **`out_run_all_1d26.txt` is the committed
evidence for P2, and every row of both sweeps is in it.**

That transcript was captured with `2>&1`, so it also carries the sweeps' progress
counters, which P2 writes to stderr. They appear grouped ahead of the section
they belong to rather than interleaved with it: Python buffers stdout when it is
a file and does not buffer stderr (mg-d53d recorded the same artefact).

## The two files this ticket edits, and what else moves with them

`code/species_extent_d633/e2_crosssection.py` and
`code/species_extent_d633/kernd633.py`. `out_e2_crosssection.txt` beside them is
regenerated, because a committed transcript showing an output shape the code can
no longer produce is a stale figure of exactly the kind this arc keeps chasing —
and the `E2 TOTAL BAD: 1` in it is the live `e35b` occurrence, not a regression.
Every other instrument's committed transcript is a dated record of **its own**
run, anchored to the revision it names, and is left alone.

**The revision a transcript is a fact about is not the commit that publishes
it** (mg-bf79's P1a). `out_e2_crosssection.txt` names the revision its census was
taken at; the commit that ships it is necessarily one later, and the next commit
that adds a `*.md` anywhere under `docs/` or `code/` makes its file count stale
again. That is the mechanism working, not a defect: the sentence stays true of
the tree it names, which is what lets a reader tell STALE from WRONG without
re-deriving anything.
