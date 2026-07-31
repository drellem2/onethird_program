# The rung repair — mg-4adb

Repairs mg-6ef4's two OPEN items. mg-6ef4 audited mg-5040 / `3c8f535`, which repaired mg-4700's three
OPEN items; mg-4700 audited mg-821e, which repaired mg-6cb9, which audited mg-d633.

Instrument: `code/species_rung_repair_4adb`, `sh run_all.sh`. Pure Python 3, no network; `git` is
used against this repository, which is local. `PREDICTIONS.md` was committed **before any probe ran**
and is scored in `OUTCOMES.md`.

---

## 1. THE ONE SENTENCE

The gate reported success while its own output stated the failure — and the line that made it do so
was one line, at the top of the file, **outside every deletion population this arc had used**.

> A mutation population that excludes a line makes that line invisible to the control that the
> population certifies — and the exclusion looks like nothing, because the certificate still reads
> 100%.

So two things are repaired, and the second matters more than the first. **The gate stops depending on
action at a distance**, and **the population becomes the whole file**.

---

## 2. OPEN 1 — THE FIFTH RUNG

mg-6ef4's F3, measured: with e2 forced red by one planted markdown file, `set -e` deleted alone left
**3 of 3 runners at exit 0 with e2's finding printed in full.** The check ran. Its output was printed.
The runner was green. That is mg-6cb9's F2 exactly, arriving through the shell instead of through a
pipeline.

And the four levels this arc had climbed — gate (mg-9220), clause (mg-64b6), twenty-line block
(mg-4700), line (mg-5040) — each made the **tested unit smaller** while the population stayed "the
wiring". The statement carrying the return was outside all four, so no refinement of the grain
reached it.

### The fix is a MOVE, not an addition

**The gate is now the last command of the runner.** A POSIX shell script's exit status is its last
command's, so the statement that turns e2's exit code into the runner's exit code is the call itself
— inside the block, inside every population that has ever enumerated the block, and the only line
whose deletion can lose the verdict.

**Why not a guard beside `set -e`.** Because that is a measurement this arc already has. mg-4700's F2
deleted the old `|| { …; exit 1; }` alone and found the verdict unchanged in 3 of 3 runners, because
`set -e` already aborted — five lines that moved the MESSAGE and not the VERDICT. mg-5040 removed
them. Adding one back would put two rungs where each masks the other's deletion, and a deletion test
over a masked pair reports **both as removable** while removing both is fatal. One rung, measured,
beats two that hide each other.

`set -e` stays: two guards are better than one, and in `species_repair_6f61` it is also the only rung
three unguarded steps have. What changed is that nothing about the *gate* rests on it, and what it
does still carry is now named in a transcript.

### The population is the whole file

`v1_population.py`, section V1a states it and it fits in two lines:

```
IN:   every line of the file, 1..N, deleted one at a time.
OUT:  nothing.
```

The ticket asks that each exclusion be justified individually. The honest way to meet that is to have
none. Comments are in. Blank lines are in. The shebang is in. `set -e` is in — the line mg-6ef4 found
outside all three previous populations. Every mutant is **executed**, because a call present in a
script is not evidence of execution (mg-6cb9 F2), and each result is one of three things:

| disposition | meaning |
|---|---|
| `gate fired` | red, and e2's own sentence in the output — the deletion cost nothing |
| `GATE LOST` | **exit 0**; a second column records whether the finding was printed anyway |
| `BROKE EARLY` | red, and e2 never spoke — the deletion broke the runner before the gate |

Those three are separated because collapsing them is how a green run gets read as a working gate.
`BROKE EARLY` is not a working gate and `GATE LOST` is not a broken runner.

V1d then compares the **measured** load-bearing set against the **declared** one — declared by line
CONTENT and never by line number (mg-7522's S3) — and asserts against the source that the call is
still the last command. "Nothing may be appended below it" is not a convention; it is the rung, and a
checker holds it rather than a comment asking a reader to.

The per-line census, the declared-against-measured rows, and the pinned before/after are in
`code/species_rung_repair_4adb/out_v1_population.txt`. The figures are not restated here: a figure in
prose is a copy, and this arc has watched copies rot for five tickets.

### What `set -e` still carries, said out loud

V1e forces each step red one at a time, with `set -e` present and with it deleted. In
`species_repair_a4ef` and `species_remainder_f8fa` every step already reads its own status, so the
answer is *nothing*. In `species_repair_6f61` three steps have no guard and the answer is those three
lines, printed by name.

**That is not a defect of this repair.** mg-6ef4's finding was a load-bearing line **outside the
population**, not a load-bearing line. A rung that is single, measured and named is the thing a
deletion test is for. A rung that is masked by a second rung is what makes a deletion test print
`removable` about a line whose removal is fatal.

---

## 3. OPEN 2 — THE SECOND LAYER

mg-6ef4's F1. The set these checkers quantify over is built twice:

```
layer 1   os.walk           -- which entries are REACHED     <- residue installed by mg-5040
layer 2   open(...).read()  -- which reached entries are READ <- except (UnicodeDecodeError, OSError)
```

A **regular file this process cannot open** passes layer 1 — `os.path.isfile` is true and the walk's
residue is empty — fails layer 2 with `PermissionError`, and was filed under a printed sentence
saying the reason was the file's **encoding**. Printed, not counted, contents never scanned,
`w3_scope.py` exit 0 and its runner GREEN over a live X4 statement.

**Three defects in one path, and the ticket orders them.** The classification is repaired first,
because a wrong bucket sends every later reader to the wrong hypothesis — worse than no bucket, and
the half that outlives the exit code.

### Two declines, two names, and only one of them counts

Layer 2 now uses layer 1's own vocabulary, so a reader who has read the walk's residue already knows
what the second list means:

| exception | bucket | counted | why |
|---|---|---|---|
| `UnicodeDecodeError` | ENCODING, **STATED** | no | a sentence has carried it since mg-d633: the printed extent says the run covers every regular file *less the ones named as undecodable*. mg-6cb9's `a1_bothways.py` Q18 asserts exit 0 for exactly this plant, and that assertion is right |
| `OSError` | UNREADABLE, **NOT STATED** | **yes** | no extent line in this repository has ever put a regular file this process cannot open outside the claim |

The distinction is not a preference about severity. It is the same test the walk already applies: a
decline a sentence carries is a rule a reader meets before the surprise; a decline no sentence
carries is a hole, and a hole arrives as RED.

### Three files carried it, and the third is the interesting one

`w3_scope.py` and `s1_extent.py` split the `except`. `trace_open.py` did something else and worse: it
recorded the path **before** calling the real `open`, so an attempt that raised counted as a read —
and `e1_extents.py`, the instrument whose whole job is deciding whether a printed extent is true,
compared its own walk against that record and **certified the extent as true** over a file nobody had
read a byte of.

An instrument that records intent and reports it as outcome cannot fail in the one direction it
exists to detect. The record is now taken after the real `open` returns, and the attempts that raised
are kept in a third list — subtracting them silently would be the same defect with the sign reversed
— and reported by `e1_extents.py` in a column called `ATTEMPTED AND FAILED`.

### The fourth checker, measured and NOT repaired

`e2_crosssection.py` reads every `*.md` under `code/` and `docs/` with an unguarded `open`. On an
unreadable `*.md` it raises. **This ticket does not change that**, and the reason is a distinction the
ticket itself draws: OPEN 2 is about a failure filed under the *wrong name* and a checker going
*silent*. e2 does neither — it raises, and a traceback is loud. V2g measures it so the choice is a
row in a transcript rather than an omission, and leaves it for whoever takes the next verdict.

---

## 4. THIS INSTRUMENT, HELD TO THE RULE IT SHIPS

> Check that your own deletion population contains every line your gate depends on, and that every
> runner you touch can go red.

`v3_self.py` asks V1's two questions of `code/species_rung_repair_4adb/run_all.sh`: every line deleted
alone, every step forced red one at a time, and `set -e` deleted to show that no verdict moves.

**And it states what it cannot do.** This runner calls V3, so executing it verbatim inside itself does
not terminate. What is executed is a **stand-in**: the runner's own bytes with each `python3 …`
*command* replaced by one whose exit code the probe chooses. The redirects, the `||` guards, the `RC`
assignments, the `exit`, the comments and the blank lines are the file's own. So V3 measures the
**wiring** of this runner and not its checkers — and the checkers are measured by being run, which is
what V1 and V2 are.

---

## 5. NOT DISTURBED

**mg-5040's subtraction is preserved.** No `followlinks=True` was added anywhere, the walk's residue
is unchanged, and layer 2 was given the residue layer 1 already had rather than a new mechanism. The
twenty-line wiring block is still two lines with one return; the repair moved it, it did not grow it.

**mg-6ef4's own instrument still runs.** `set -e` was not deleted from the three runners, so
`selftest6ef4.py`'s premise — `set -e` appears exactly once in each — still holds and `t2_wiring.py`'s
deletion probe still has a line to delete. Its T2e row is written so that it goes from FINDING to `ok`
when the repair lands, which is what the measurement in V1f shows independently.

**mg-6ef4's T2f row is not closed by editing mg-6ef4.** That row says `set -e` is in the deletion
population of none of `p3_wiring.py`, `q2_wiring.py`, `r2_wiring.py`. That is a true statement about
those three instruments and about the moment it was made. It is closed by this ticket's population
containing every line that exists, not by adding a fourth name to an audit's table after the fact.

**mg-6ef4's F5 is kept, not fixed.** The restore proof cannot see a permission mode; it is stated in
`kern4adb.Probe`'s docstring, and V2 — which plants a file at mode 000 — restores the mode explicitly
and re-reads it rather than trusting the class for the one thing it is known not to cover.

**No mathematics was touched.**
