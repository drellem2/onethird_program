# mg-4adb — the fifth rung, and the second layer

Repairs the two OPEN items mg-6ef4 left against the mg-5040 repair (`3c8f535`), audited in
`4ede6ef` with its instrument in `code/species_bound_audit_6ef4/`.

```
sh code/species_rung_repair_4adb/run_all.sh          # about an hour
```

Pure Python 3, no dependencies, no network. `git` is used against this repository, which is local.
`PREDICTIONS.md` was committed in `2e48b67` **before any probe in this directory ran** and has not
been edited; `OUTCOMES.md` scores it.

---

## OPEN 1 — `set -e` was the fifth rung, and it was outside every deletion population

mg-6ef4's F3. `set -e` sits at the top of each of the three species runners, dozens of lines above
the cross-section call, and it is the statement that turns e2's exit code into the runner's. Deleted
alone: **3 of 3 runners exit 0 while printing e2's finding in full.** And it is in **no** deletion
population this arc has used — mg-821e's `p3_wiring.py`, mg-4700's `q2_wiring.py` and mg-5040's
`r2_wiring.py` each enumerate *the block*.

> A mutation population that excludes a line makes that line invisible to the control that the
> population certifies — and the exclusion looks like nothing, because the certificate still reads
> 100%.

**The rung.** The gate is **moved to the end** of each runner. A POSIX shell script's exit status is
its last command's, so what carries e2's status out of the file is now the call itself — inside the
block, inside every population that has ever enumerated the block, and the only line whose deletion
can lose the verdict.

No guard was added beside `set -e`, and that is a decision with a measurement behind it: mg-4700's F2
found that a `|| { …; exit 1; }` next to a `set -e` is a line whose deletion changes no verdict
because the other one catches it — five lines that moved the MESSAGE and not the VERDICT — and
mg-5040 removed it. Re-adding one would be that finding, re-committed. `set -e` stays; nothing about
the gate rests on it.

**The population.** It is **every line of the runner file. There is no exclusion list**, so there is
no exclusion to justify. Comments are in, blank lines are in, the shebang is in, `set -e` is in.
`v1_population.py` deletes each one alone and executes the runner with e2 forced red — the count is
printed by V1a as `TOTAL RUNNER EXECUTIONS IN V1c` rather than written here as a figure that would
rot. Each result is one of three things, and they are not the same:

| disposition | meaning |
|---|---|
| `gate fired` | red, and e2's own sentence is in the output — the deletion cost nothing |
| `GATE LOST` | **exit 0** — the class this ticket is about; a second column says whether the finding was printed anyway |
| `BROKE EARLY` | red, and e2 never spoke — the deletion broke the runner before the gate |

V1d then compares the **measured** load-bearing set against the **declared** one, and asserts against
the file's source that the call is still the last command — because "nothing may be appended below
it" is not a convention, it is the rung.

V1e asks what `set -e` still carries, by forcing each step red with `set -e` deleted. In
`species_repair_6f61` three steps have no `||` guard, and the answer is *those three lines* — named
in a transcript rather than left to be inferred. That is not a defect of this repair: mg-6ef4's
finding was a load-bearing line **outside the population**, not a load-bearing line.

V1f re-derives the before-figure rather than quoting it: the runners as they were at the pin are
written into the worktree and the same deletion is made.

## OPEN 2 — an unreadable regular file is not a mis-encoded one

mg-6ef4's F1. The file set is built in two layers — `os.walk` decides what is REACHED, `open().read()`
decides what is READ — and mg-5040 installed a residue at layer 1 only. A regular file this process
cannot open passed layer 1, failed layer 2 with `PermissionError`, and was caught by one
`except (UnicodeDecodeError, OSError)` under a printed sentence saying the reason was the file's
**ENCODING**: printed, not counted, contents never scanned, `w3_scope.py` exit 0 and its runner GREEN
over a live X4 statement.

**The classification is repaired first**, because a wrong bucket sends every later reader to the wrong
hypothesis. Layer 2 now declines by the same vocabulary layer 1 already uses:

| exception | bucket | counted? | why |
|---|---|---|---|
| `UnicodeDecodeError` | **ENCODING**, STATED | no | a sentence has carried it since mg-d633 — the printed extent says the run covers every regular file *less the ones named as undecodable* — and mg-6cb9's `a1_bothways.py` Q18 asserts exit 0 for exactly this plant |
| `OSError` | **UNREADABLE**, NOT STATED | **yes** | no extent line in this repository has ever put a regular file this process cannot open outside the claim |

Three files carried the defect and all three are repaired: `w3_scope.py`, `s1_extent.py`, and
`trace_open.py` — the last because it recorded the path **before** calling the real `open`, so an
attempt that raised counted as a read and `e1_extents.py` certified an extent over files whose bytes
nobody had seen. It now records after the call returns, and the attempts that raised are kept in a
third list and reported by `e1_extents.py` as `ATTEMPTED AND FAILED`.

`e2_crosssection.py` is the fourth checker and is **measured but not repaired** — V2g. On an
unreadable `*.md` it raises, and a traceback is loud. OPEN 2 is about a failure filed under the wrong
name and a checker going silent; e2 does neither. The choice is a row in a transcript rather than an
omission.

## This instrument, held to its own rule

`v3_self.py`. Every line of **this** runner is deleted alone, every step is forced red one at a time,
and `set -e` is deleted to show no verdict moves. What is executed is a **stand-in**: this runner's
own bytes with each `python3 …` *command* replaced by one whose exit code the probe chooses — the
redirects, guards, `RC` assignments, `exit`, comments and blanks are the file's own. Executing this
runner verbatim inside itself does not terminate. That limitation is stated in the file and in V3's
extent line: V3 measures the WIRING, and the checkers are measured by being run.

## What was checked, and what was not

Run and green with these files present: the four species runners (`species_7d75`,
`species_repair_a4ef`, `species_remainder_f8fa`, `species_repair_6f61`),
`code/species_extent_d633/run_all.sh`, and mg-6cb9's `a1_bothways.py` Q18 control. The exact list and
the exit codes are in `OUTCOMES.md`.

Not covered, and stated because a population is a claim about what was tried: deletions of **more
than one line at a time**; any failure mode of e2 other than the planted B1; a file that becomes
unreadable *between* the two layers; and any tree outside the four these checkers name.

## Kept, not fixed

mg-6ef4's F5 — the restore proof cannot see a permission mode — is kept as a limitation and stated in
`kern4adb.Probe`'s docstring. V2 plants a file at mode 000, so it restores the mode explicitly and
re-reads it rather than trusting the class for the one thing it is known not to cover.
