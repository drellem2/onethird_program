# The kernel half really is back, and five really is five — but the reason given for the row that was added says the opposite of what the row does — `mg-e34a`

**Independent audit of `mg-76cc` (`4755d02`), which closed the two sites
`mg-957f` left open on `mg-7e58`.** Pre-filed in the same action as its parent.
Audited at `4755d029`.

`mg-957f`'s `F-1` was the first site in this arc where a repair *removed*
detection rather than relocating a defect, and it was visible only by running
the predicate the repair had replaced. So the instruction that found it is the
first thing applied here — to `mg-76cc`'s own patch, and not only to the patch
`mg-76cc` was fixing.

The instrument is `code/branching_audit_e34a/`. Nothing in it imports
`lib58da`, `lib957f` or `lib76cc` for its own reading; `k4 (v)` loads
`lib76cc` deliberately, unmodified, in order to run *their* reader against a
committed file.

---

## 0. The bottom line

**Both open sites are closed, and the primary check comes back clean.**

* **The pre-repair predicate was run against the same inputs, and coverage did
  not go backwards.** **7 inputs × 3 revisions of `g1` = 21 runs.** Inputs
  where the pre-repair predicate fires and this one is silent: **0 at the exit
  grain, 0 at the finding grain**, and **0** files named by a pre-repair
  finding that no repaired finding names. Two of the seven inputs are not on
  `mg-76cc`'s list.
* **`OPEN 1` is closed and the closing is confirmed by the means it was found
  by.** Bend `kern_a218.py` as a commit in a clone and the repaired `g1` exits
  `1` with `1/3` **naming `kern_a218.py`**, where the predicate it replaced
  exits `0` with `0/0` and names it nowhere. That row is reproduced here
  independently, in `k1 (iii)`.
* **`OPEN 2` is closed on five, counted here.** `1 of 5` byte for byte,
  `5 of 5` under a one-revision normalisation with **0 lines unexplained**, and
  the population is the five outputs `run_all.sh`'s **own redirections** name,
  not a written list. The normalisation is shown to act at the **same line
  positions on both sides**, which a count of surviving lines cannot see.
* **Nothing `mg-957f` confirmed is weaker.** **18 of 18** attributions agree
  against a ground truth derived twice over `286d5030..HEAD` — *not* over
  `mg-957f`'s own pinned HEAD. `g1`'s three pre-`mg-76cc` direction probes are
  present **by name** and HIT, `5 of 5` at HEAD. `g4` reads exit `1`, `0/2` and
  `g1` reads exit `0`, `0/0`, exactly as `mg-957f` read them.

**Three findings. None of them reopens either site.**

* **`E-1` — the reason given for the row `mg-76cc` added is inverted**, in
  five places including `g1`'s docstring, `g1`'s own printed output and the
  commit message of `4755d02`. Built and measured, a cancelling pair does the
  opposite of what the sentence says.
* **`E-2` — on that input the repaired predicate books two findings asserting
  that the 198 cells "have to be re-taken"**, while its own `both together`
  row — the only one of the three that asks what the tree as it stands
  measures — prints `IDENTICAL` on the same run.
* **`E-3` — `lib76cc.findings_of()` over-counts**, demonstrated at HEAD on
  `out_g4_fleet.txt`: `3` where the file's own trailer says `2`.

---

## 1. The primary target — the pre-repair predicate, run

### 1.1 The pre-repair revision is derived, not taken on trust

`lib76cc.py` carries

```python
REV_957F = "e006581c2e1185cba3fa58c91a9fd4954bd63eae"   # g1 BEFORE mg-76cc
```

A pinned literal beside a comment is a claim that stops being checked the
moment the file moves again. `k1` computes the revision instead — the last
commit that touched `g1_provenance.py` (`4755d029`) and then its first parent
(`3bc2cf76`) — and then **checks the two against each other**, because if they
named different files, `mg-76cc` ran something other than the predicate its own
patch replaced:

```
   g1_provenance.py         at e006581c vs at 3bc2cf76 : IDENTICAL
   lib58da.py               at e006581c vs at 3bc2cf76 : IDENTICAL
```

They agree. `mg-76cc` ran the right predicate. That row is not decoration: it
is the only thing standing between "the pre-repair predicate" and "a revision
somebody typed".

The pinned predicate travels with **its own `lib58da`**, under a module name of
its own, with exactly one substitution — its import line — asserted to have
happened once. `mg-76cc` changed `run_c1`'s signature in the same commit as
`g1`; a pre-repair predicate run against the repaired library is a third thing
that never existed.

### 1.2 Seven inputs, and the buckets are not filtered by a declaration

`mg-76cc`'s own `r3` computes its backwards set like this:

```python
for label, rel, mut, real, why in INPUTS:
    if not real:
        continue                      # <- the answer depends on the declaration
```

so an input the repair itself has declared "not a defect" cannot enter the set
however the two predicates behave on it. Here **every** input is bucketed and
the declaration is printed *beside* the bucket rather than in front of it.

Two inputs are added that `mg-76cc` does not have:

* **a comment appended to `kern_a218.py`.** `mg-76cc`'s list has a byte-only
  control for `c1_branching.py` and **none for the kernel** — the file the
  whole repair is about. A restored half that fires on a comment is not
  restored. It does not fire: both silent.
* **the cancelling pair** — `§2`.

Asked at two grains, because they are not the same question. `r3` compares
**exit codes**; a script can exit `1` on a SELF-ERROR alone — it could not
build a probe out of an already-bent file — and at the exit grain that is
indistinguishable from a catch. Every bent input here raises a self-error
alongside its findings, so `exit 1` on those rows is partly a fact about the
script. **No row in this table exits `1` on a self-error alone**, which is why
the two grains agreed; that is luck, not design, and it is why both are
printed.

```
   input                                      moves  before mg-7e58   BEFORE REPAIR    this repair
                                              meas?  exit self find  exit self find  exit self find
     unmodified -- NULL                         no     1    0    1     0    0    0     0    0    0
     kern_a218.py: dim L(n,p) one too big       YES    1    0    2     0    0    0     1    1    3
     c1_branching.py: vertex dims one too big   YES    1    0    1     1    1    3     1    1    4
     c1_branching.py: a comment appended        no     1    0    1     0    0    0     0    0    0
     c1_branching.py: a line past section (iii) no     1    0    1     0    0    0     0    0    0
     kern_a218.py: a comment appended           no     1    0    2     0    0    0     0    0    0
     THE CANCELLING PAIR: kern +1 and c1 -1     no     1    0    2     1    1    3     1    2    5
```

**The row `OPEN 1` turns on is the second one**, and it is reproduced
independently: the predicate before this repair is `0/0` on a bent kernel; the
repaired one is `1/3` and names the file.

Buckets, unfiltered:

| input | exit grain | finding grain |
|---|---|---|
| NULL | both silent | both silent |
| `kern` dim +1 | *new fires, old silent* | *new fires, old silent* |
| `c1` dims +1 | both fire | both fire |
| `c1` comment | both silent | both silent |
| `c1` line past (iii) | both silent | both silent |
| `kern` comment | both silent | both silent |
| the cancelling pair | both fire | both fire |

**`OLD FIRES, NEW SILENT`: 0 at both grains.**

### 1.3 And "both fire" is not "the same thing was caught"

Two predicates can exit `1` on the same input and disagree about what moved. So
every file each finding **names** is compared:

```
     input                                      named by OLD             named by NEW
     kern_a218.py: dim L(n,p) one too big       -                        kern_a218.py
     c1_branching.py: vertex dims one too big   -                        c1_branching.py
     THE CANCELLING PAIR: kern +1 and c1 -1     -                        c1_branching.py, kern_a218.py
```

**Files a pre-repair finding names and no repaired finding does: 0.** The
traffic is all the other way — the repair names files the predicate before it
named nowhere, which is `mg-76cc`'s "so a finding says WHICH file moved the
measurement", measured rather than asserted.

---

## 2. `E-1` — the reason given for the `both together` row is backwards

`mg-76cc` added a third row to section `(v)` and gave it a reason. The reason is
written in five places — `g1`'s docstring (`g1_provenance.py:42`), `g1`'s
printed text (`:257`), the committed transcript (`out_g1_provenance.txt:94`),
the repair's document (`repair-mg-76cc-…md:109`) and the commit message of
`4755d02`:

> "then both are moved together, because **two changes that cancel would pass
> each half on its own**."

A rationale is a claim, and this one **names an input**. Nothing in `mg-76cc`
ever built one. `k4` builds it:

* `kern_a218.py`'s `dim_L(n,p)` one too **big**,
* `c1_branching.py`'s vertex dims one too **small**,

so each file's own measurement moves and the two together restore the printed
measurement exactly. The pair is asserted to really cancel in the selftest,
before any row rests on it.

```
     half moved to HEAD              baseline         moved            verdict
     c1_branching.py (the script)   a8db5dbd4c758765 0c91a182221d5880 MOVED
     kern_a218.py (its kernel)      a8db5dbd4c758765 cb329be9d6265c27 MOVED
     both together (cancellation)   a8db5dbd4c758765 a8db5dbd4c758765 IDENTICAL
```

**The row named `cancellation` is the only one of the three that a cancelling
pair passes.** The two halves it was added to backstop are the two that catch
it. The sentence is exactly inverted.

**The finding is against the sentence, not against the row.** The row is
load-bearing, for the *other* pair: a **conspiring** pair — each file's change
harmless on its own, the two together moving the measurement — is caught by
`both together` and by neither half. What is wrong is the reason, and a reason
that survives into four files and a commit message is how the next reader
learns the wrong thing about what the row does.

A different sentence in the same repair — `r1_kernel.py:376`, *"a cancelling
pair cannot pass"* — is **true**, and is named in `k4 (i)` as excluded from the
population so that the line can be seen to have been drawn on purpose.

---

## 3. `E-2` — what the halves cost on that input

`§2`'s pair is not a defect of the measurement: the tree's own measurement, both
files as they stand, is byte-identical to the measurement at `286d5030`. The
198 cells do **not** need re-taking.

The repaired `g1` books **five findings** on it, two of which say they do:

```
   NEW FINDING: c1's own measurement is not the same at 286d5030 and at HEAD when c1_branching.py is moved …
   NEW FINDING: c1's own measurement is not the same at 286d5030 and at HEAD when kern_a218.py is moved …
```

each ending *"… and the 198 cells have to be re-taken"* — while the run's own
`both together` row prints `IDENTICAL`.

This is the grain error `mg-7e58` was repairing, relocated: `mg-321d`'s `G-1`
was `g1` concluding from a **file** what is true of a **measurement**;
`mg-76cc`'s halves conclude from the measurement of a **half-moved tree that
exists nowhere**. The two half rows are a *decomposition*, useful for saying
which file moved something — and they have been promoted to findings without
the row that answers the tree's actual question gating them.

**The class is not new and is not booked as if it were.** The predicate before
this repair fires on the same input, through its `c1` comparison; `k1 (v)`
prints both columns for exactly that reason. What is new is that the repair's
own rationale names this input and states the opposite outcome, so the one
place a reader would look to find out how the rows behave on it is the place
that is wrong.

The remaining three findings on that input are direction probes: the two rows
labelled `NULL PROBE` fire, having been predicted silent. A "null probe" that
compares `(old_c1, head_kern)` against `(old_c1, old_kern)` is not null — it is
the same comparison as the `kern_a218.py` half row, and it goes red under
exactly the condition that makes that row go red. It is reported here rather
than booked: on the tree as it stands `kern_a218.py` is `SAME` across the range
and the probe is genuinely null, and the pre-`mg-76cc` `c1` null probe has the
same shape.

---

## 4. `E-3` — the repair's own finding reader over-counts

Found while cross-checking a trailer against the lines under it, and kept.

`lib76cc.findings_of()` is:

```python
def findings_of(out):
    return [line.split("FINDING: ", 1)[1].strip()
            for line in out.splitlines() if "   FINDING: " in line]
```

A transcript that **quotes** another script's finding at a deeper indentation
contains that substring too. Run unmodified — theirs, loaded by path, not
re-implemented — against files committed at HEAD:

```
     file                        trailer says  their reader  mine
     out_g4_fleet.txt            2             3             2
     out_g1_provenance.txt       0             0             0
     out_g3_findings.txt         0             0             0
     out_r1_kernel.txt           0             0             0
     out_r3_prerepair.txt        0             0             0
```

`out_g4_fleet.txt:89` is `g4` reporting what another member's run said, at six
spaces. `g4`'s own trailer says `2`; the reader says `3`.

**Where it could bite.** `r3` uses that reader for its `names kern_a218.py`
column:

```python
kern = bool([x for x in L.findings_of(o) if "kern_a218.py" in x])
```

and that column is what the whole `OPEN 1` verdict turns on. It does not bite:
`g1` quotes no nested transcript, so every line the reader picks up there is
`g1`'s own. **A live defect with no live consequence** — which is worth saying
plainly rather than either inflating or omitting.

`k1` and `k3` book this discrimination as their own reader's rule: a line is
this script's finding only if it comes **after** the trailer that counts them
**and** is indented by exactly three spaces. `k3` raised a SELF-ERROR on
`g4_fleet.txt` before that rule was in, which is how it was found.

---

## 5. `OPEN 2` — counted on five

`k2` re-runs `mg-58da`'s `run_all.sh` in a clone whose HEAD **is** this
branch's HEAD — nothing is committed in it, so the fresh transcripts name a
revision anybody can `git show`, where `mg-76cc`'s clone adds a scratch commit
and names one that exists only inside a temp directory.

The population is enumerated from the runner's own `run <script>` lines and its
own redirection, and then compared against `mg-76cc`'s written `FIVE_OUTPUTS`
list: **0 written and not listed, 0 listed and not written.**

```
     file                        committed  re-run  differing  byte for byte
     out_selftest_58da.txt      7          7       0          YES
     out_g1_provenance.txt      166        166     5          no
     out_g2_redo.txt            116        116     1          no
     out_g3_findings.txt        147        147     1          no
     out_g4_fleet.txt           226        226     2          no

   1 of 5 reproduce byte for byte, over 9 differing lines in all.
   …
   REPRODUCE UNDER THE NAMED NORMALISATION : 5 of 5, 0 lines unexplained.
```

**Five is five.** Counted here, on the tree as committed on this branch, and
the figures match `mg-76cc`'s.

Two things are added to the check rather than taken from it:

* **The substitution must act at the same line positions on both sides.** A
  substitution that fires on the record and not on the re-run absorbs a
  difference instead of explaining one, and a count of surviving lines cannot
  tell those apart. **Files where the positions differ: 0.**
* **A third control**, alongside the two `mg-76cc` has. Both of theirs perturb
  the committed side and must survive normalisation; this one makes the record
  name **another real revision, subject and all**, re-derived from the mutated
  transcript exactly as the normalisation derives it from the real one, and
  must be **absorbed**. It is. That is not a defect being certified — it is the
  residual weakness `r2` names in its own verdict (*"a transcript naming some
  other real revision would normalise clean"*), shown rather than restated.

**And the staleness row has moved.** `r2 (iv)` prints

> `commits from it to this HEAD : 0` — *"0 means the record was taken at the
> tree's current HEAD and has NOT yet been committed; it becomes 1 the moment
> it is, and 1 is the freshest a committed record can ever be."*

That was true of the worktree `r2` ran in. On the branch the record landed on
it is **6**: six commits from other tickets landed between the run and the
commit. The row is not gated by `mg-76cc` and is not gated here — what it
bounds is how far the tree may have moved under a transcript that still
normalises clean, and a figure of `0` that is really `6` is the difference
between "written just now" and "written and then overtaken". It is printed.

---

## 6. What `mg-957f` confirmed, re-derived at HEAD

`mg-957f` scored the attribution over `286d5030..2d23d880` — **its own HEAD,
pinned**. `mg-05eb` has already booked a finding in this arc whose whole
content was that a scan had been pinned, so `k3` ends the range at `HEAD`.

* **The two derivation routes agree at `5 of 5` members** before either is used
  — `git log <range> -- <path>` against `git show --name-only` per commit.
* **`18 of 18` attributions agree.** `mg-957f` scored `17`; the difference is
  named rather than reconciled — `g4`'s `(none) uncommitted` entry is scored
  here twice, once as an ATTRIBUTION-block row and once as a summary line,
  where `mg-957f` scored it once. Both readings are of the same two printed
  lines.
* **`g4` exit `1`, `0/2`; `g1` exit `0`, `0/0`** — as `mg-957f` read them, and
  both gated.
* **`g1`'s three pre-`mg-76cc` direction probes are looked for by name**, not
  inferred from the population having grown: `3 of 3` present and HIT, and the
  whole population at HEAD is `5 of 5` HIT.

Nothing here is weaker than `mg-957f` left it.

---

## 7. The floor, and what was chosen

The ticket asks for at least one thing no list in it names, and for the choice
to be said. **Chosen: the sentence `mg-76cc` uses to justify the row it
added** — because a rationale is a claim, this one names a specific input, and
the input can be built. That is `§2` (`E-1`), and `§3` (`E-2`) follows from
running it. `§4` (`E-3`) was found on the way and kept.

`k4 (iv)` also scores `mg-76cc`'s own `PREDICTIONS.md` — prose that nothing
executes — reading its exit-code table's **rows** and checking both its
`predicted` and its `actual` column against the committed `TOTAL BAD` of the
transcript each row names. `5 of 5` agree; the `run_all.sh (worst)` row is
excluded **by name**, because it has no transcript of its own.

## 8. What is open after this audit

* **`E-1`** — the inverted rationale, in five places. Not repaired here:
  editing `g1_provenance.py` would move `out_g1_provenance.txt`, which is one
  of the five outputs `§5` counts, and this is an audit.
* **`E-2`** — the half rows book findings on a tree whose measurement did not
  move, with the row that measures it printing `IDENTICAL` beside them.
* **`E-3`** — `lib76cc.findings_of()` counts a quoted finding as its own.
* **Unchanged from `mg-76cc`, and correctly stated there**: the revision token
  itself is not reproduced by the `G-3` normalisation, and `g4`'s second
  finding (`mg-d330`'s, on `c3_withdrawal.py`) remains OPEN.
