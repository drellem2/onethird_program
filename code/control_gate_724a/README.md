# mg-724a — the thing that ASKS the control suites

`mg-9876` made 50 arms falsifiable across 59 sites and demonstrated all 50 RED against a
known-bad input. Nothing ran any of them. Its own author named the gap before its ticket and
again after it, in these words:

> I made the instruments falsifiable. I did not make them fire.

This directory is what fires them.

---

## 0. What was actually true before this landed — measured, not asserted

| measurement | value | how |
|---|---|---|
| merge requests this repository has put through the refinery | 48 | `pogo refinery history --json` |
| …that merged carrying the refinery's own words `(no quality gates configured)` | **46** | same |
| …that failed before reaching the gate step | 2 | same |
| …that ran **any** gate | **0** | same |
| git hooks installed in this repository | 0 (14 `.sample` files, which git never runs) | `ls .git/hooks` |
| CI configuration files in the tree | 0 | `find . -name '*.yml' -o -name '*.yaml'` |

So the arc's position was: controls that CAN fail, which nothing ASKS.

## 1. Runtime, before choosing anything

The ticket is right that a gate whose cost nobody measured is how gates get removed six weeks
later, so the cost is the first thing here rather than a footnote.

| suite | wall clock |
|---|---|
| `code/rendered_twin_pin_9bc2/run_all.sh` | **1.0–1.9 s** |
| `code/control_audit_9876/run_all.sh` | **12.7–13.6 s** |
| this gate as a whole, including its own §4/§5 falsification | **~15 s** |

§4 and §5 together cost under a tenth of a second, because none of their probes re-runs a
suite: they mutate the bytes the run already captured.

The ticket's stated worry — *this arc's suites are not all fast* — is **false for these two,
by measurement**. Against this fleet's observed gate wall-clock (a duplicated suite costing a
median of 2m30s per merge was worth a ticket of its own, mg-da30), 15 s is small.

## 2. The trigger: the refinery merge gate. Why, and why not the others

**(a) The merge gate — CHOSEN.** It is the only candidate that fires *before* the landing it
should block, and a landing is where wrong figures propagate. It costs ~15 s on the critical
path of each merge, which is measured above rather than hoped for. Wired in
`.pogo/refinery.toml` and, independently, by the root `build.sh` (§5 below).

**(b) A schedule — rejected as the primary.** It reports after the landing it should have
blocked. For a corpus whose characteristic defect is *a published figure moved*, that means
the wrong number is already on `main` and already being cited by the time anyone hears. It
stays the right answer for anything too slow to gate, which is where the next widening will
need it.

**(c) A hook on the covered files — rejected, and refuted rather than merely disliked.** Git
hooks live in `.git/hooks`, which is not tracked and not transferred by clone. A hook
committed to this repository is not installed by checking it out; the refinery merges in its
own private clone which would never have it; and this repository's `.git/hooks` today
contains nothing but the 14 samples git ships. A trigger every participant must remember to
install is this ticket's own defect, one layer down.

**(d) A combination — not needed at 15 s.** It becomes correct the moment the scope widens
past these two directories, and that is where the successor ticket starts.

## 3. What it does on RED, and who hears

**It blocks.** The gate exits non-zero, the refinery fails the merge request, and the branch
does not land. `pogo refinery show <id>` carries the gate's whole transcript, including the
`GATE VERDICT:` line and the field that diverged.

The addressee is named, because mg-be37's finding was that a detector firing into
`events.log` with no mail path is indistinguishable from one that never fired:

- **The submitting agent** sees `status: failed` on its own poll loop — this is step 6 of
  every polecat's protocol — and its step 7 is *mail the mayor with failure details*. That
  is a mail path with a person at the end of it, not a log line.
- **A blocked merge cannot be silent anyway.** The branch does not land. Whatever else fails
  to be read, the change does not reach `main`, which is the property being bought.

## 4. Why the gate is a comparison and not `sh run_all.sh`

Wiring the suites directly is the obvious answer and it is wrong twice.

**It is red on arrival.** `code/control_audit_9876/run_all.sh` exits **1** today — a2 scores
arm C3 `UNFALSIFIABLE`, a standing recorded finding of mg-9876, not a new defect. A gate that
blocks every merge from the day it lands is a gate that gets deleted, and deleting it would
take the working half with it.

**And it is blind to the thing this arc is about.**
`code/rendered_twin_pin_9bc2/run_all.sh` exits **0** on DRIFT — deliberately; its header says
drift is the normal condition of a hand-maintained rendering between reconciliations. It
exits 0 whether the drift worklist is `8`, `7 8`, or `1 2 7 8`. `x1_exhibit.py` plants that
world and measures it (`out_x1_exhibit.txt`):

```
ledger row 7's applicability narrowed from `any` to `n ≤ 6` in STATE.md

  the suite's RUNNER EXIT CODE : 0 -> 0        UNCHANGED — blind
  the suite's DRIFT WORKLIST   : ['8'] -> ['7', '8']   grew — the suite DID see it
```

A published applicability claim narrowed, the twin control saw it, and a gate reading the
suite's exit code lands it.

**So the gate compares against a declared baseline.** `BASELINE.json` names 25 fields, each
with the value this repository stands at and a `why`. RED is: *a GATED field's observed value
differs from its declared value, in either direction.*

The green direction matters as much as the red one. `audit.arms_not_shown` going `1 -> 0`
means either arm C3 was repaired or a2 stopped asking, and those are opposite events. The
remedy is identical and is one line: **move the value in `BASELINE.json` in the same commit
and write the reason into its `why`.** That is the gate's entire cost to an author who
legitimately changes the estate. What is not available is landing the change and leaving the
declared state behind it.

There is deliberately **no `--refresh` mode**. A gate that can rewrite its own expectations
on demand turns every red into a keystroke, which is laundering with extra steps.

### The 3 fields that are RECORDED and not gated, named rather than omitted

`audit.sweep_membership_candidates`, `audit.sweep_tee_sites`,
`audit.sweep_dirs_without_evidence` are `a4_sweep.py`'s population counts over **every**
directory under `code/`. They move whenever any ticket adds code, so gating them would turn
unrelated branches red. They are printed with both values on every run, and probe **T10**
demonstrates on every run that they really are silent — the blind spot is exhibited, not
promised. `audit.sweep_grade` **is** gated: if the sweep's own two-sided control stops
answering both ways, its counts are not citable at all.

## 5. How it is wired, and the trap found while wiring it

```toml
# .pogo/refinery.toml
[gates]
commands = ["./build.sh"]
timeout = "20m"
```

`./build.sh` execs `code/control_gate_724a/run_all.sh`. There is exactly **one** definition of
what the gate is — that one line — reached by two independent routes: the config above, and
the refinery's *default* discovery, which looks for `./build.sh` at the root when a repository
declares no gates. If `.pogo/refinery.toml` is ever deleted, the gate still runs. Two routes,
one definition, so they cannot drift into two gate lists that disagree.

**The trap.** `.pogo/` is excluded by this repository's `.git/info/exclude`, so
`git add .pogo/refinery.toml` **silently does nothing** — the file that turns the gate on is
in a directory git is configured to ignore, and the failure is a no-op with no message. It is
committed here with `git add -f`. `.git/info/exclude` is machine-local and never cloned, so
the tracked file behaves normally everywhere else; the hazard is only for the next person who
edits it. That hazard is this ticket's own defect class — *the control that nothing runs* —
wearing a config file, and the root `build.sh` is the second route precisely because of it.

## 6. Scope, and what is deliberately NOT wired

Two directories: `code/rendered_twin_pin_9bc2` and `code/control_audit_9876`. Nothing else.

c9876's population index says the estate is far wider — 202 whole-output membership tests in
66 of 178 directories, 18 live `| tee` sites in 4, and 24 directories shipping code with no
evidence of any falsification attempt. Wiring 178 directories in one step is how a gate
acquires a failure nobody can attribute. This proves the mechanism on the two that were
audited; widening is the successor ticket's, and `audit.sweep_dirs_without_evidence` is
recorded here so that the widening has a number to move.

## 7. This gate is itself a control, and is shown able to fail on every run

Every gated merge runs, against its own captured bytes and at a cost under 0.1 s:

- **§4, 14 probes** (`negative_control.py`) — the worklist gaining a row; each runner's exit
  status moving; the VERDICT grade flipping; the twin's negative control catching one fewer
  mutation; a row becoming UNFALSIFIABLE; **the audit's one non-discriminating arm silently
  becoming green**; the census gaining an arm; the selftest losing a planted world; the audit
  reporting no findings; the RECORDED counts moving *without* going red; a decision line
  vanishing; a decision line appearing twice.
- **§5, 8 worlds** — baseline missing, unreadable schema, a field with no `why`, a field that
  is neither gated nor recorded, no `fields` object, the extractor producing a field the
  baseline never declared, the baseline declaring one the extractor cannot produce, and a
  wired suite that has been deleted. Each must **REFUSE**, and the refusal must name the
  thing.

Two rules are adopted from mg-9876 rather than paraphrased:

1. **The unmutated report is scored first.** A probe whose expectation is already satisfied by
   the good input cannot fail and is reported `UNFALSIFIABLE`, never `CAUGHT`. That is the
   generalisation of `"8 9" in out`, which satisfied a positive control about a drift worklist
   for its whole life.
2. **Every mutation is derived from the captured bytes, never typed.** `worklist + " 99"`, not
   `"8" -> "7 8"`. A transform that changes nothing is `SETUP FAILED` and is red, because a
   mutation that stopped mutating reads exactly like one that was caught.

And one rule of its own: **no field is read by a membership test.** Each is matched by an
anchored pattern that must hit **exactly once**; zero matches and two matches are both
refusals. Zero means the suite never reached that decision — a traceback and a finding leave
the same exit code — and two means the pattern no longer names a single fact. `a4_sweep.py`
counts 0 whole-output membership tests in this directory.

## 8. Defects of my own, kept

**D1 — my own directory was scored by mg-9876's sweep as shipping code with NO evidence of a
falsification attempt, and it was right.** `a4_sweep.py` §3 asks two questions: is there a
*source file named* for a negative/self/positive control, and does a *committed transcript*
carry red tokens. The first was no, because the probes lived inside `gate.py`. The second was
also no — and the reason is worse: the only transcript carrying those tokens is `out_gate.txt`,
which **the run is still writing when a4 reads it**. That is mg-f8e5's d5 (reading a file the
current run has not finished producing) committed inside the instrument built to report that
class of thing. `audit.sweep_dirs_without_evidence` went 25 → 26 and the 26th was me. Repaired
by moving the probes into `negative_control.py`, i.e. by following the estate's convention
rather than arguing with the detector.

**D2 — the exhibit's first planted world was bad for the wrong reason.** Ledger row 1 is the
obvious cell to mutate, and mutating it made the suite exit **2** with `negative exit : 1` —
because `rendered_twin_pin_9bc2/negative_control.py` already plants a mutation on row 1, so my
world made *its* fixture unfalsifiable. That is a true red that would have flattered this
exhibit, since it proves nothing about exit-code blindness. Row 7 is used instead, and the
measurement is recorded here rather than quietly dropped.

**D3 — `x1_exhibit.py` exited 1 with a traceback and no decision line, on its first run.**
`extract()` demanded both suites and the exhibit runs one. The runner's decision-line
discipline is the only reason that was a visible failure rather than a silent one — which is
the discipline's entire argument, paid for by the instrument that adopts it.

**D4 — the `only=` parameter that fixed D3 is a way to gate less.** It restricts the read to
one suite, and a narrowing option is exactly how coverage goes quietly missing. It is safe
here for a structural reason and not a promise: `gate.py` never passes it, and `compare()`
refuses outright when the observed field set and the baseline's disagree in either direction,
so a partial extraction can only reach a refusal, never a verdict. Worlds S6 and S7 are that
refusal, in both directions.

**D5 — the gate leaves four tracked files modified in two directories that are not mine.**
Both subject suites redirect into their own directories, by design, and this ticket does not
edit another ticket's directory to change that. In the refinery it is harmless: the merge
pipeline resets tracked modifications after gates and before the target checkout. Locally,
run `git checkout -- code/` afterwards. Naming it because a gate with an undocumented
side-effect on the tree is how someone later stashes the wrong thing.

## 9. Files

| file | what |
|---|---|
| `../../build.sh` | the refinery's entry point; one line, two discovery routes |
| `../../.pogo/refinery.toml` | the gate declaration and the argument for it |
| `run_all.sh` | the runner: no pipe, and the `GATE VERDICT:` line must exist before the exit code is read |
| `gate.py` | runs both suites, compares to the baseline, reports; `GATE VERDICT: GREEN / RED / BROKEN / REFUSED` |
| `lib724a.py` | exactly-once extraction, baseline validation, comparison |
| `negative_control.py` | §4's 14 probes and §5's 8 worlds — how this gate can fail and refuse |
| `BASELINE.json` | 25 declared fields, each `gated` or `recorded`, each with a `why` |
| `x1_exhibit.py` | the measured argument for the design; writes and restores `STATE.md`, checked by digest |
| `out_gate.txt`, `out_x1_exhibit.txt` | committed transcripts |
| `out_exhibit_refinery.txt` | the end-to-end demonstration: a real merge request, blocked by this gate |
