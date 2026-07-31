# mg-4adb — OUTCOMES

Scores `PREDICTIONS.md`, which was committed in `2e48b67` **before any probe in this directory ran**
and has not been edited since.

---

## The bottom line

```
selftest4adb: 41 assertions, 0 failed
V1 TOTAL BAD: 0      V1 PREDICTIONS MISSED: 0
V2 TOTAL BAD: 0      V2 PREDICTIONS MISSED: 0
V3 TOTAL BAD: 0      V3 PREDICTIONS MISSED: 0
V4 TOTAL BAD: 0
```

Both OPEN items moved, and each was **re-derived against the pin** rather than quoted from the audit:

- **OPEN 1.** `set -e` deleted alone turns 3 of 3 runners **green at the pin, printing e2's finding in
  full** (V1f) — mg-6ef4's F3, reproduced by a different instrument — and leaves 3 of 3 **red at
  HEAD**, still printing it. The deletion population is now every line of every runner with **no
  exclusion list**, and the measured load-bearing set equals the declared one in 3 of 3 (V1d).
- **OPEN 2.** An unreadable regular file carrying a live X4 statement leaves `w3_scope.py` **exit 0
  and its runner green at the pin** (V2f) and, at HEAD, **exit 1 with the file named on a line that
  says `REACHED AND NOT READ … PermissionError`** and its runner red (V2b).

`V1 TOTAL BAD` and the rest count outcomes that contradict **this repair's own claims**, so four
zeroes is what a repair that landed clean looks like. `PREDICTIONS MISSED` is separate and is not
expected to be zero — it happens to be.

---

## The predictions

Every prediction in `PREDICTIONS.md` is scored in the transcript that measures it, next to the
measurement. None missed.

| id | predicted | got | where |
|----|-----------|-----|-------|
| P1a | 1, 1, 1 lines lose the gate | 1, 1, 1 — the call, in all three | `out_v1_population.txt` V1c |
| P1b | 1, 1, 1 red without `set -e` | 1, 1, 1, still printing the finding | V1f |
| P1c | heading deleted alone: still red | 1, 1, 1 | V1c |
| P1d | measured == declared | yes, 3 of 3 | V1d |
| P1e | 0 comment/blank lines lose the gate | 0 | V1c |
| P1f | some lines break the runner before the gate | yes, in all three | V1c |
| P2a | a4ef: 0 steps `set -e` alone reports | 0 | V1e |
| P2b | f8fa: 0 | 0 | V1e |
| P2c | 6f61: 3 | 3 — `r1_smallest`, `r2_columns`, `r3_quotes`, named | V1e |
| P3a | unreadable plant → `w3_scope` exit 1 | 1 | `out_v2_layer2.txt` V2b |
| P3b | its line does not blame the encoding | holds | V2b |
| P3c | f8fa runner red | 1 | V2b |
| P3d | non-UTF-8 plant → exit 0 | 0 | V2d |
| P3e | the two lines are distinguishable | yes | V2e |
| P3f | `s1_extent` exit 1 | 1 | V2b |
| P3g | `e1_extents` exit 1, names it as not read | 1, named | V2b |
| P3h | clean tree stays green | 4 checkers, 3 runners, all 0 | V2a |
| P3i | mg-6cb9's Q18 still passes | passes | V2d, and run in `out_v4_neighbours.txt` |
| P4a | this runner's measured set == declared | yes | `out_v3_self.txt` V3a |
| P4b | every step of this runner reddens it | yes | V3b |
| P4c | this runner does not depend on `set -e` | yes | V3c |

**P2d is a judgement and not a measurement**, and it is written here rather than scored: `set -e`
being the only rung for three steps of `species_repair_6f61` is a disclosure, not a defect. The
reasoning is in the next section and the measurement that supports it is V1e.

---

## The three things worth reading even if every row is `ok`

### 1. The population has no exclusion list, and that is the whole answer to F3

The ticket asks for the deletion set to be stated and **each exclusion justified individually**. Every
way of meeting that except one leaves somebody deciding which lines cannot matter — and F3 is what
one of those decisions cost. So the set is every line of the file and the exclusion list is empty.

It costs about two hours of runner executions, and **the cost is the point**: a cheaper population is
a smaller one, and a smaller one is what F3 was. The transcripts are committed so that reading the
result does not cost what producing it did.

### 2. `set -e` is still load-bearing in one runner, and that is not the defect

V1e names three lines in `species_repair_6f61` whose failure only `set -e` reports. **No second guard
was added beside it**, and the reason is a measurement this arc already owns: mg-4700's F2 found that
a `|| { …; exit 1; }` next to a `set -e` is a line whose deletion changes no verdict, because the
other one catches it — five lines that moved the MESSAGE and not the VERDICT, which mg-5040 then
removed. Two rungs that mask each other make a deletion test report **both as removable** while
removing both is fatal.

mg-6ef4's finding was a load-bearing line **outside the population**, not a load-bearing line. One
rung, inside the population, measured to flip the verdict, and named in a transcript is the state a
deletion test exists to produce.

### 3. The ENCODING bucket is still not counted, and a landed audit is the reason

Splitting the `except` could have counted both halves. It does not: `UnicodeDecodeError` stays a
**stated** decline. A sentence has carried that exclusion since mg-d633 — the printed extent says the
run covers every regular file *less the ones named as undecodable* — and mg-6cb9's `a1_bothways.py`
**Q18 asserts exit 0 for exactly this plant**. Counting it would have reddened a landed audit's
control, and the control is right.

What was wrong was never that a mis-encoded file is excluded. It was that **a file nobody could open
was filed under the same word**, and no sentence anywhere put it outside the claim.

---

## One regression this repair caused, found by the enumeration and repaired

`code/species_extent_d633/e3_bothways.py`, **P11b**. That probe measures the *exoneration rule*: it
needs its plant to land within six lines of a ticket id `kerna4ef.NAMES_A_REPAIR` matches, and its
own label says so — *"six lines from an unrelated `mg-73df`"*. It got there by **appending to the end
of `code/species_repair_a4ef/run_all.sh`**, which happened to end with a sentence naming `mg-73df`.

Moving the gate to the end of that file moved the sentence up, the plant stopped landing near the
marker, and the probe reported a MISS — while its label still said it was measuring the rule.

Repaired by keying the site on the **marker** instead of on the end of the file (`plant_near`), which
is mg-7522's S3 correction applied to a position rather than a line number: *a probe that names a
property should locate itself by that property.* It raises if the marker is absent, because a plant
that lands somewhere unintended is worse than a probe that stops. `E3 TOTAL BAD` is back to 0 and
`code/species_extent_d633/run_all.sh` is green — V4a row 2.

**This is the finding of the night in this instrument**, and it was found by V4 and not by V1 or V2:
the two probes aimed at the repair both said `ok` while a neighbour two directories away was red.

---

## What was checked

Every one of these was **executed**, with the assertion that belongs to it, in `out_v4_neighbours.txt`:

| what | result | why it could have broken |
|---|---|---|
| `code/species_7d75/run_all.sh` | exit 0 | the tree the checkers quantify over and V2 plants in |
| `code/species_extent_d633/run_all.sh` | exit 0 | ships `trace_open.py` and `e1_extents.py` |
| mg-6cb9 `a1_bothways.py` | exit 0, Q18 holds | Q18 is why ENCODING is not counted |
| mg-5040 `r2_wiring.py` | exit 0 | deletes lines from the block this repair moved |
| mg-6ef4 `selftest6ef4.py` | exit 0 | asserts `set -e` appears once — the line kept on purpose |
| mg-6ef4 `t2_wiring.py` | exit 1, **T2e now `ok`** | the probe that raised OPEN 1 |
| `code/runner_exit_c2b3/k3_retro.py` | pre-existing, from git | its `E2OUT=$(` is 0 at the pin and 0 now |

Plus, inside V1 and V2: the three species runners on a clean tree and with e2 red, the four checkers
on a clean tree, and every one of them again with each plant.

**V4b forces one of them red on purpose** — `set -e` deleted from `species_repair_a4ef`, and
`selftest6ef4.py` goes to exit 1 on the assertion that names the deleted line. A table of green rows
with nothing that could have been red is not evidence.

**mg-6ef4's T2f row is deliberately left as a finding.** It says `set -e` is in the deletion
population of none of `p3_wiring.py`, `q2_wiring.py`, `r2_wiring.py`. That is a true statement about
those three instruments, and it is closed by *this* ticket's population containing every line that
exists — not by adding a fourth name to an audit's table after the fact. An audit is a record of what
was true when it ran.

## What was not checked

- deletions of **more than one line at a time** — every mutant here is one line short of the original;
- any failure mode of `e2_crosssection.py` other than the planted B1;
- a file that becomes unreadable **between** layer 1 and layer 2;
- any tree outside the four these checkers name;
- `code/species_bound_repair_5040/run_all.sh`, `code/species_bound_audit_6ef4/run_all.sh` and
  `code/species_extent_audit_6cb9/run_all.sh` as whole runners — the files inside them that carry the
  dependency are run, and V4a says which and why;
- mg-4700's `q2_wiring.py` and mg-821e's `p3_wiring.py` — audits of states this repair is two and
  three tickets downstream of. Re-running an audit against a tree it did not audit does not test this
  repair; it replaces a record with a measurement of something else.

---

## Defects in this instrument, kept

1. **The first `v1_population.py` run reported `restored: False` for its own sweep, and was right
   to.** Running the runners from the repository root is what makes `cd "$(dirname "$0")"` testable —
   and a mutant with that line deleted writes its `out_*.txt` **at the root**. The probe put back
   every tracked file and left three untracked ones it had no record of. `run_runner` now removes
   them, and the restore proof was the thing that noticed: a probe that dirties the worktree while
   reporting `restored: True` is the shape of everything this arc has been about.

2. **`v3_self.py`'s stand-in truncated the transcript it was being written into.** The first version
   rebound only the redirect TARGETS to a scratch directory, so every `cat out_X.txt` read a file its
   own step no longer wrote, and every mutant was red for that reason instead of the one being asked.
   Worse, `out_v3_self.txt` is one of those paths and is the file V3's own stdout goes to. Every
   transcript path in an executable line is now rebound together, and the deviation is stated in the
   file rather than discovered in a transcript full of `V3 STAND-IN STEP`.

3. **`v3_self.py` computed a step's index against one version of a file and used it against another.**
   Two of its three sections mutate the runner before choosing which step to force red, and after
   `set -e` is removed every index below it is off by one. Keyed on line CONTENT now — mg-7522's S3,
   met a second time in the same instrument that quotes it.

4. **Two predictions had no `score()` row.** P1c and P3b were measured by rows that printed `ok` and
   scored by nothing, so `PREDICTIONS MISSED` could not have counted them. Both now score against the
   measurement already taken rather than against a second one: a prediction scored against its own
   re-measurement is two chances to be right.

5. **`s1_extent.py` goes red at the pin for the wrong reason, and this instrument does not fix it.**
   V2f shows `s1_extent` exit 1 with the unreadable file planted **at the pin**, where the
   classification defect is still live: it is red because `shutil.copytree` in its own injection
   control raises `Permission denied`, so the reader is told the CONTROL broke. That is mg-6ef4's
   D2b, and it is still true at HEAD — `s1_extent`'s output names the file twice, once from the
   residue and once from a `shutil.Error`. The residue row is the one this ticket repaired; the
   control's fragility is not, and is left named here.
