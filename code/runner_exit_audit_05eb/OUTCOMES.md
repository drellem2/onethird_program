# mg-05eb — outcomes: predictions scored, and this instrument's own defects

## Predictions, scored against `PREDICTIONS.md`

Written before the instrument existed. Misses are kept as written; none was
re-tuned to pass.

| id | predicted | measured | |
|---|---|---|---|
| Q1 | `*.sh` at `bee07a1` = 72 | 72 | ok |
| Q2 | named `run_all.sh` = 64 | 64 | ok |
| Q3 | bare grep over `run_all.sh` = 23 | 23 | ok |
| Q4 | real pipelines in `run_all.sh` = 17 | 17 | ok |
| Q5 | pipelined `*.sh` outside `run_all.sh` = 2 | 2 | ok |
| Q6 | pipelines in those = 8 | 8 | ok |
| Q7 | still pipelined at HEAD = 2 files / 8 pipelines | 2 / 8 | ok |
| **Q8** | **pipefail in any `*.sh` = 0** | **1** | **MISS** |
| **Q9** | **the ticket's `1` is not in a `*.sh`** | **it is** | **MISS** |
| Q10 | `species_depth_audit_4700` absent at the pin | absent | ok |
| Q11 | R3 consumer files at HEAD ≥ 4 | 13 | ok |
| Q12 | ≥ 2 exit-status scorers outside the nine | 2 | ok |
| Q13 | the two `SWALLOWED` rows no longer hold | 2 of 2 flipped | ok |
| Q14 | the nine sites still carry their quoted text = 9 of 9 | 9 of 9 | ok |
| Q15 | RED: 17 of 17 exit non-zero | 17 of 17 | ok |
| Q16 | RED: 17 of 17 stop at the forced step | 17 of 17 | ok |
| Q17 | GREEN: 17 of 17 exit 0 | 17 of 17 | ok |
| Q18 | NEGATIVE: 2 of 2 exit 0 | 2 of 2 SWALLOWED | ok |
| Q19 | 34 of 34 pipeline sites repaired | 34 of 34 | ok |
| Q20 | the uniform repair IS stated | 5 of 5 sentences present | ok |
| Q21 | 34 of 34 guards `cat` on failure | 34 of 34 | ok |
| Q22 | ≥ 1 of the 64 runners is not `#!/bin/sh` | 5 of 64 | ok |
| Q23 | 4 artifacts assert `pipefail 1 / confirmed` | 4 | ok |

**Q8 and Q9 are the interesting misses**, and they missed for one reason:
they are the two predictions where I took the parent's published answer instead
of measuring. The parent said `re-derived 0`, so I predicted 0. The ticket's `1`
was right all along, and the whole of finding **F2** is downstream of that miss.
Q22 and Q23 were written after the miss and before `J1e` existed; the timing is
stated in `PREDICTIONS.md` rather than smoothed over.

## Four defects in THIS instrument, caught and recorded

Recorded here rather than quietly fixed, because an audit that reports only the
faults it found in someone else's work is reporting half a measurement.

### D1 — the forced failure was a no-op on two of the seventeen targets

`j3_control.py`'s first draft forced a step to fail by **appending**
`raise SystemExit(1)` to the target script. That fires only if the script falls
off its own end. `code/face_geometry_audit_6653/verify_claims.py` and
`code/face_geometry_audit_e720/verify_landing_claims.py` end in
`sys.exit(main())`, so the forcer never ran, the runners legitimately came back
`0`, and my table printed **`*** NOT CAUGHT ***` against two sound runners**.

That is this audit's own defect wearing the finding's clothes: an instrument
reporting a failure that is its own. It was caught by the conjunction — the
`reached` column said the forced marker never appeared, which is inconsistent
with "the runner swallowed a failure" and consistent with "there was no failure".

**The replacement is strictly harder than what it replaces.** A `sitecustomize.py`
injected through `PYTHONPATH` registers an `atexit` hook in the process whose
`sys.argv[0]` is the named target. `atexit` fires on every exit path — falling off
the end, `sys.exit`, an uncaught exception — and the target's bytes and line
numbers are never touched, which matters because several instruments in this arc
read their own and each other's source by line.

### D2 — `later ran` was measured after the restore, and was 8 of 17 false

`j3_control.py` stamps every later transcript to epoch 0 and reads its mtime back
to decide whether a later step ran. The first draft read the mtime **after**
`L.Sandbox.__exit__` had called `git checkout -- .`, which rewrites tracked files
unconditionally and gives every one of them a fresh mtime. Every runner therefore
looked as though its later steps had all run. The measurement now happens inside
the sandbox, before any restore.

### D3 — a probe that looked for a form of words instead of for the claim

`j4_scope.py` §J4b asks whether the sweep *said* it repaired the sites it had just shown were
unaffected. Its first version searched `docs/OneThird-RunnerExit-ArcWideSweep.md` for the
literal string `"34 of 34"`, did not find it, and scored the sweep **4 of 5 — not stated**.

The document does state it, in different words: *"Repaired anyway, and listed so that `all 34
carried a verdict` is not asserted when it is false."* Searching for a **form of words** rather
than for the **claim** is the same error as counting a header comment as a pipeline — which is
the error this entire arc is about, committed by the instrument auditing it. Prediction **Q20
was right and my instrument was wrong**; the probe now looks for `"Repaired anyway"` in the
document and the section reports 5 of 5.

### D4 — the self-test grepped for `shell=True` and scored its own docstrings BAD

§S7 checks that no instrument here reintroduces a shell. Its first version tested
`"shell=True" in src`, which matches the sentence *"we never pass `shell=True`"* — so four of
my own files, including `lib05eb.py` whose docstring makes exactly that promise, came back BAD.
It now **parses** each file and looks for a `shell=` keyword on a real `Call` node and a real
`os.system` call, and is driven in both senses: it must see a real `subprocess.run(…,
shell=True)`, and it must NOT see a docstring naming both constructs.

The same class caught §S6 one more time: the check *"this runner contains no pipeline of any
kind"* flagged this tree's own headline `grep -h 'A\|B' out_*.txt`, where the `\|` is a regex
alternation inside single quotes. `lib05eb.unquoted()` now blanks quoted spans before looking
for a pipe, and both `tee_pipelines` and `any_pipelines` use it. **Three separate times, in one
instrument, the rule counted a mention as an occurrence.** That is the defect this arc keeps
finding, and it is worth saying plainly that this audit produced three instances of it.

### And one process-level error, which is not an instrument defect but is a result

The first `j3` run was terminated with a `pkill -f` pattern anchored to the full
path; the process's actual command line is `python3 -u j3_control.py`, so the
pattern matched nothing and **two `j3` processes ran concurrently into one output
file**, interleaving rows and mutating the same worktree. The rows from that
window were discarded and the section re-run from a clean tree. It is recorded
because those interleaved rows looked exactly like findings.

## The instrument's own headline numbers

| section | TOTAL BAD | extent of that number |
|---|---|---|
| `S` self-test | **0** (44 checks) | seven rules, both senses each; this tree's own runner bytes; every `.py` here parsed for a shell |
| `J1` census | **2** | F2's two: prose contradicting its own transcript, and the false `measured` shebang claim |
| `J2` retroactive | **1** | F3: one past-claim R3 consumer of an affected runner outside the nine |
| `J3` control | **0** | 17 of 17 both directions, worktree clean; J3c's 2 SWALLOWED are the finding, not a fault |
| `J4` scope | **0** | 34 of 34 repaired, 5 of 5 sentences, 34 of 34 guards cat |

**Predictions across all sections: 21 of 23 as predicted, 2 MISSED (Q8, Q9).**

## Findings, and what each is worth

| | finding | kind |
|---|---|---|
| **F1** | 2 runners with 8 real `\| tee` pipelines are outside the sweep's population and unrepaired at HEAD; `J3c` reproduces the defect on them | scope — MAJOR |
| **F2** | the one census number said to be "confirmed exactly" is the one the instrument got wrong, and 4 artifacts assert a measurement the transcript contradicts | summary-vs-rows — MAJOR |
| **F3** | a past R3 claim reading two affected runners' exit codes, outside the enumeration, hidden by the caller scan's pin | retroactive — MAJOR |
| **F4** | on "did it fix what did not need fixing, and did it say so" the sweep is CLEAN, measured at 5 of 5 sentences | no finding |
| **F5** | `K2a` also excludes every `run_all.sh` from being a caller; 3 executions are invisible to it, and none targets an affected runner | hole, checked, empty |
| **F6** | the failing step's diagnosis reaches the runner's stdout only where the guard `cat`s — measured at **34 of 34** in `J4c` and **17 of 17** live in `J3a` | the floor item, and it comes back CLEAN |

**What is NOT a finding, said explicitly.** The forward repair is sound: 17 of 17
repaired runners exit non-zero when their first scored step fails, stop at that
step, and exit 0 unmodified. The mechanism argument against `set -o pipefail` is
correct. The retroactive METHOD — routing every claim R1/R2/R3 and settling only
R3 — is right, and the per-claim dispositions in `K3a` are done per claim with a
reason, which is what item 1 of the assignment asked to check. `F3` is a gap in
the population that method was applied to, not a fault in the method.
