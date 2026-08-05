# mg-d53d — INDEPENDENT AUDIT of the mg-4adb deletion-population repair

An audit of `4bb4384` (mg-4adb), which landed mg-6ef4's two OPEN items: the
deletion population that could not see `set -e`, and the `except` that filed an
unreadable regular file under a bucket naming its *encoding*.

Pre-filed in the same action as its parent. `PREDICTIONS.md` was written and
committed **before any script in this directory existed** — commit `79e23c8`,
whose tree contains that file and nothing else of this instrument. Everything
below is a commit on top of it. `OUTCOMES.md` scores all 25 predictions; the
five that missed are kept as written, and two of them are the headline.

    sh code/species_gate_audit_d53d/run_all.sh        # about 40 minutes

## What this asks that mg-4adb did not

mg-6ef4's finding was never "`set -e` was load-bearing". It was:

> the line whose removal breaks the gate was **outside the population that
> certifies the gate** — and the exclusion looks like nothing, because the
> certificate still reads 100%.

mg-4adb answered by making the population **every line of the runner file**,
with no exclusion list. This audit does not read that definition and check it
looks complete. It takes the source, deletes each line itself, and asks the
same question **of the thing that actually carries the verdict**:

    e2_crosssection.py  ->  its exit code  ->  the runner's exit code  ->  reader

The three runners are 255 lines. `e2_crosssection.py` is 299 and `kernd633.py`,
which computes the finding, is 252. **The verdict path is 806 lines and
mg-4adb's certificate covers the first 255 of them.** All 806 are deleted here,
one at a time, with a live finding planted and the runner or the checker
executed for every one.

## What it found

**mg-4adb's own headline reproduces exactly.** Under an instrument that shares
no code with it, the only runner line whose deletion turns a red runner green
is the cross-section call itself — 1, 1, 1 — and this audit's 255 dispositions
agree with mg-4adb's 255 rows **row for row, on exit code, disposition and
finding-printed alike**. The repair does what its ticket claims and its
certificate is honest.

**And the class it repaired is still open one level down.** Six deletions
outside the certified population turn a red gate green:

| file | line | what it is | finding still printed? |
|------|------|-----------|------------------------|
| `e2_crosssection.py` | 52 | `FILES += _f` | **no — silent** |
| `e2_crosssection.py` | 144 | `bad += len(fires)` | yes |
| `e2_crosssection.py` | 299 | `sys.exit(1 if bad else 0)` | yes |
| `kernd633.py` | 127 | `spans.append((prev, len(text)))` | **no — silent** |
| `kernd633.py` | 196 | `for dp, dns, fns in os.walk(...)` | **no — silent** |
| `kernd633.py` | 205 | `else:` | **no — silent** |

Every one of the nine runner executions over the first three exits **0**, and
six of the nine print `*** STANDING UN-STRUCK ***` while doing it. That is
mg-6ef4's F3 word for word — a green runner printing the finding in full — on
the same verdict path, after the repair that closed it. The other three are
worse: the checker reads nothing, says nothing and returns 0.

This is **not** a defect of mg-4adb's implementation. It is the *scope* of the
population, which is the same shape of error the repair was written to answer:
a boundary drawn where the file ends rather than where the verdict path does.

**The fourth species runner cannot go red over a finding.** Nothing in either
ticket names `code/species_7d75/run_all.sh`; mg-4adb's P3h used its exit 0 as
evidence of a clean tree. Six of the seven scripts it calls end in an
*unconditional* `sys.exit(0)` — read out of the parsed source, not sampled —
and its last command is `grep -h "TOTAL BAD" out_t*.txt`, which exits 0 when it
matches. A step printing `T1 TOTAL BAD: 7` leaves the runner exiting 0 with
that line in its own output. It goes red for a **crash** (G5e: exit 1) and for
nothing else. This arc has found and repaired exactly this defect once before —
`w3_scope.py`'s own comment records it: *"mg-a4ef: this was `sys.exit(0)`
unconditionally"*.

**The misclassification is repaired, in all three of its parts.** Asked
separately, as the ticket demands: the bucket says `REACHED AND NOT READ` and
names `PermissionError`; `w3_scope.py` exits 1; the runner exits 1. The STATED
decline survives — an undecodable file is still printed and still not counted.
And the counterfactual is measured: the same file readable **is** a live X4
finding, so the plant was a real hazard and not a bucket around nothing.

**The self-reference is intact, and that is the correct state.** The diff over
mg-6ef4's own tree is empty and no predicate anywhere in `77306a7..HEAD`
excludes an instrument's own files or commits from a population it counts.
mg-4adb's three `*.md` files are in the census that counts them, 3 of 3.

## Sections

| | |
|---|---|
| `selftest_d53d.py` | the sandbox, the deletion, the plant and the disposition, each given an input whose right answer is known — **including the ones that must say no** |
| `g1_population.py` | the 806-line deletion sweep; G1d compares its 255 overlapping rows against mg-4adb's own transcript |
| `g2_red.py` | 15 step substitutions, 3 natural inputs, and `set -e` deleted alone **at HEAD and at the pin** |
| `g3_layer2.py` | the misclassification in three separate rows, plus the counterfactual, e2's own unreadable-file behaviour, and an unreadable **directory** |
| `g4_self.py` | the self-reference, with an inverted finding condition |
| `g5_fourth.py` | the fourth species runner |

## The sandbox is a git clone, and that is load-bearing

Every probe runs in `git clone --shared` of this worktree, never in the
worktree. A plain file copy would have been cheaper and wrong: `s1_extent.py`
replays its detector at `ebecd89` and `83ac472` through `git archive`, and in a
sandbox without `.git` those two controls print `git unavailable -- SKIPPED`.
The deletion sweep would then have been certifying a runner with two of its own
controls silently switched off — this arc's own defect, committed by its
auditor. `selftest_d53d.py` S1 does not assert the clone is git-backed; it runs
`s1_extent.py` in it and reads whether the controls printed a measurement.

A clone carries only tracked files, so it has no `__pycache__`. Two committed
transcripts move on such a tree — `out_s1_extent.txt`'s `DECLINED, STATED`
count and `out_w3_scope.txt`'s `stated` count. **That was observed before
`PREDICTIONS.md` was written and is disclosed there as G5a, scored as an
observation and not as a hit.** No verdict moves with it.

## Four defects of this instrument, kept

1. **G4's rule read its own definition as an instance of what it detects.**
   The first version flagged, as self-exclusions, a docstring sentence in
   `code/runner_exit_audit_56dc/t2_strictest.py`, a bare `continue` whose
   self-naming words were in the comment beside it, and **two lines of
   `g4_self.py` itself — one of them the line defining the rule**. Q18 and Q20
   scored MISSED on that run. The repair is *not* to exclude this file from the
   scan, which is the regression G4 exists to report: it is to stop treating
   prose as a predicate. Every file is tokenized, comments and string contents
   are blanked, and the disposition is read off what is left. Both the raw line
   and the code-only rendering are printed for all six candidates.
2. **G2's third natural input was caught by the wrong checker, and the prose
   said otherwise.** The probe used a paraphrase of a `STRICKEN` entry;
   `check_doc.py` did not fire on it and `e2` did, further down the same
   runner. Q9 still held — the runner went red — but the sentence naming which
   checker caught it was written rather than measured. The input is now the
   verbatim table entry and the `caught by` column is **derived from the run**.
3. **The repair for defect 2 was itself too narrow, in the same direction.**
   `caught_by` matched `^<name>.py FAILED`; 6f61's guard prints `CHECK_DOC
   FAILED`, so the column read `(cannot be told from the output)` for a run
   whose very next line said which checker it was — and the row asserting the
   three inputs reach three different checkers passed *because that string is
   distinct from the other two*. A row that goes green on its own ignorance is
   this audit's subject, committed by its author. The pattern is now
   `^<anything> FAILED` and the row requires all three to be named as well as
   distinct.
4. **The selftest's git-availability check fired on the right output.** It
   looked for `SKIPPED`, which `s1_extent.py` prints for an unrelated and
   correct exclusion (`SKIPPED, NAMED, so the exclusion cannot grow unseen`).
   Narrowed to `git unavailable -- SKIPPED`, and the bare-word count is printed
   beside it so the narrowing is visible rather than silent.

## What is still open

1. **The verdict path's other 551 lines have no certificate.** This audit
   deleted them and reports six. It did not install a control that keeps them
   covered. Naming the hole is not closing it.
2. **`code/species_7d75/run_all.sh` is unrepaired.** Six unconditional
   `sys.exit(0)`s and a `grep` for a gate. The fix is the one `w3_scope.py`
   already received.
3. **e2 has no bucket for an unreadable `*.md`** (G3f): it exits 1 by uncaught
   traceback. The reader is not told the wrong thing, only nothing — which is
   why it is reported rather than filed as a second F1.
4. **Deletions are one line at a time.** Two lines deleted together, and a line
   *edited* rather than removed, are outside every number here.
5. **G4's candidate rule is a regex over diff text.** It reports six candidates
   over 29 119 added `*.py`/`*.sh` lines and prints all six. A self-exclusion
   written as a data table rather than as a predicate is invisible to it.

## Why there is no `out_g1_population.txt`

There are five per-section transcripts and one whole-suite transcript,
`out_run_all_d53d.txt`. **G1's own output is only in the second**, and that is
a consequence of obeying the rung rather than an omission.

G1 carries this audit's primary claim, so it is `run_all.sh`'s last command and
its exit status is the file's. Redirecting it to a transcript and `cat`ing the
transcript afterwards would put a `cat` after the gate — a command whose status
is 0 whatever G1 returned. That is precisely the defect mg-c2b3 found in these
runners (`tee`), mg-6ef4 found again in `set -e`, and mg-4adb repaired by
making the call the last command. An auditor who broke it to obtain a tidier
artifact would have written the finding into its own instrument.

So the whole-suite transcript is the committed evidence for G1, and every row
of all 806 deletions is in it.

It was captured with `2>&1`, so it also carries the sweep's own progress
counters (`... 250/299`), which G1 writes to stderr. They appear grouped ahead
of the section they belong to rather than interleaved with it: Python buffers
stdout when it is a file and does not buffer stderr. The five per-section
transcripts are stdout only and carry none of it.

## Reading the exit codes

`run_all.sh` **exits 1**, and that is the correct verdict: G1 reports four
findings and G5 one. A non-zero `TOTAL BAD` in this suite is a finding
*reported*, not a broken instrument — and `PREDICTIONS MISSED` is neither. A
prediction that missed is a result. Five of twenty-five missed, four of them in
the direction of *more*, and `OUTCOMES.md` scores every one against what
`PREDICTIONS.md` says, unedited.
