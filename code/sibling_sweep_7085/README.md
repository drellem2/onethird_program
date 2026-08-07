# mg-7085 — the rest of mg-cf83's sweep, run rather than read

    python3 r1_sweep.py          # ~10 min, pure Python 3 + git, no third-party packages

**Subject:** `code/census_repair_f3ff/` — `s2_controls.py`, `s3_graph.py`,
`s4_crosscheck.py` repaired; `s0_freshness.py` and `selftest_f3ff.py` measured
and left alone. The repair itself lives in that directory and is written up in
its **§11**. This directory is the instrument that found it and the evidence
that it holds.

---

## What this is the rest of

mg-cf83 repaired `s1_rows.py`'s summary block and **did not overclaim** — its
README and its docstring both scope the three rules to that one file. mg-407f
confirmed the repair sound in all three arms with a harness sharing no code with
it, and found the same defect **alive in two siblings**. This is the rest of the
sweep, plus the coverage gap mg-407f recorded so it would not be rediscovered.

## The one reusable lesson: don't sweep by grepping an idiom

mg-cf83's ticket told it to grep `0 if not gens`. **That spelling finds the site
already repaired and nothing else.** The live defect was spelled

```python
g1 = p8_gain.get(1, 0)
```

— a **dict default on an accumulator the row loop's `continue` never wrote**.
Same None-becomes-zero merger, different syntax. `p9_rows.get(3)` returning
`None` and rendering as `no` is the same one again in boolean clothing, and
`for gen in gens` over a `None` is the third costume.

So the sweep **enumerates the ways a `None` becomes a `0`** — `or []`,
`.get(k, 0)`, `if not x`, `len(x or [])`, truthiness on a possibly-`None`, a
bare `for` over one — and then **checks each site by running the failing arm**.
Reading a guard is exactly what makes an insufficient one look sufficient:
`s4_crosscheck.py`'s guard *reads* as complete and is one repo too narrow.

## How the arms are built, and why that matters

The remote is broken **after cloning**, so `origin/main` still resolves from the
refs the clone already fetched. Breaking it before would leave no ref at all,
and every UNKNOWN would be an artefact of an absent ref rather than of a failed
fetch. This is mg-4d3b's shape, and it is the incident's own shape: no network
at boot, every checkout holding yesterday's refs.

A `git` shim on `PATH` logs every argv and every exit status, so each failing arm
**proves `git fetch origin` was actually spawned and actually exited 128** — and
the healthy arm proves its own fetch was spawned and exited **0**, because a
healthy arm whose fetch silently failed is just a second broken arm. Without the
shim, a run that never fetched is indistinguishable from one whose fetch failed,
and both arms are the same run reported twice. The original defect shipped
because its control returned *before* `git fetch` was ever spawned.

**Every arm fetches from a frozen bare mirror taken once at startup.** This is
methodology, not plumbing. The healthy arm's fetch really runs and really
succeeds — that is what makes it the mutation control — so if it fetched from
the *live* repos, a commit landing on `main` between the BEFORE run and the
AFTER run would change the subject's output and be scored as an effect of the
repair. `main` moved twice during this ticket's own session. With mirrors, both
versions see byte-identical history and **the only variable is the code**, which
is what lets the healthy-arm outputs be compared byte-for-byte at all.

| arm | repo 1 | repo 2 | what it is for |
|---|---|---|---|
| **H** | healthy | healthy | **the mutation control.** A script hard-wired to print UNMEASURED passes every failing arm and is worthless. H proves the repaired scripts still report real numbers — that they *can* fail. |
| **B** | broken | broken | total fetch failure — the arm mg-cf83 and mg-407f ran |
| **M** | healthy | broken | **partial** failure. The arm that found `s4_crosscheck.py`, which is clean under B. |

Each arm runs **all six scripts and `run_all.sh`**, in **both** the before state
(`ba67d39`, materialised with `git archive` rather than copied into the tree) and
the worktree state. Every "repaired" claim is therefore a **difference between
two runs of the same harness**, not an absence observed once — an absence
observed once is also what a script that never ran looks like.

## A defect of this instrument, kept — and it is the audited class, committed by the auditor

CHECK 7's first form grepped the bare phrase `row verdicts flipped` out of s2's
stdout. **It fired twice against correct code** — on `s2_controls.py`'s own
UNMEASURED branch, whose prose *quotes* the sentence it is refusing to print.

A detector that reads the subject's **prose** as the subject's **output** is
mg-4d3b's own §6 defect (*"a source census that READ MY OWN PROSE AS CODE,
inside the section about rules that read one thing as another"*), and I
committed it about two hours after quoting that section. The failing run is
committed at `57fd381` rather than only described here, because a defect
described after it was fixed is a claim and a defect in the history is a record.

The patterns now match the **assertion** — a figure in its sentence,
`\d+ of \d+ row verdicts flipped at depth` — and not the vocabulary. The same
correction found a second instance in my own repair: `s4_crosscheck.py`'s
UNMEASURED branch had a hard-coded `misses 13` in its explanation, which is rule
2 broken by the sentence explaining rule 2.

## Two ways this harness could have lied, and the guards against them

- **A crash is not a clean UNMEASURED.** mg-407f filed this against itself as
  P15 and it is enforced here too: the repaired arms assert the scoring-block
  header is *present*, that stdout *continues past it*, and that there is no
  traceback — not merely that a false zero is absent. A dead script prints no
  false zero either.
- **The staging directory must be inside a git checkout.** `selftest_f3ff.py`
  resolves `git rev-parse --show-toplevel` from its own CWD. Staged in a bare
  tmp dir it dies on `not a git repository` — **and this harness did exactly
  that on its first run**, producing something that looks identical to a finding
  about the subject. Staging now happens inside the arm's own clone. The
  underlying CWD-sensitivity is a real fragility of the selftest's fixtures; it
  is **recorded and not repaired**, because it is not the defect this ticket
  sweeps for and quietly fixing it would hide that it was ever there.

## Findings

See `code/census_repair_f3ff/README.md` §11 for the full table of what was LIVE,
what was LATENT, and the printed evidence each classification rests on — and for
the one detail worth carrying forward: **`s2_controls.py:130`'s `or []` was
latent only because the crash above it returned first.** Repairing the crash
alone would have made it live and turned "the tree could not be read" into "the
tree found no successor", scored as *agreement* with the mail reader. A latent
site downstream of a live one is not a separate ticket.

## Exit

**0 if this instrument ran.** Findings about the subject do **not** set it —
the same rule `run_all.sh` states for mg-f3ff, for the same reason: an
instrument that exited 1 for successfully finding what it was sent to find could
not distinguish *the subject has a defect* from *the auditor is broken*, and
those need different responses. A failed check **of this harness** does set it.

## Files

| file | what |
|---|---|
| `r1_sweep.py` | the sweep: three arms × two versions × seven runs, all as subprocesses |
| `run_all.sh` | the runner; reports the instrument's status, not `tee`'s |
| `out_r1_sweep.txt` | the committed transcript |
| `out_r1_sweep_FIRSTRUN_2FAIL.txt` | the **first** run, kept: two checks of this harness failing against correct code. See the defect section above. A discarded detector that was wrong is evidence too. |
