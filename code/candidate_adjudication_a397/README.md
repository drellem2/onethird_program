# mg-a397 — ADJUDICATING mg-9876's INDEX

mg-9876 produced an **index of candidates** and stopped, deliberately, saying so in its own
module docstring: *"establishing that a particular one DOES [match something printed
unconditionally] requires running it two ways, which is `a2_discriminate.py`'s method and was
applied to exactly one directory."* This directory does the running.

The three figures the ticket was filed on, and what they turned into:

| index (2026-08-10, c9876) | today | adjudicated to |
|---|---|---|
| 202 whole-output membership tests in 66 directories | see `out_a1_index.txt` | `out_a4_membership.txt` §3 |
| 18 live `\| tee` sites in 4 directories | see `out_a1_index.txt` | `out_a2_tee.txt` §5 |
| 24 directories shipping code with no evidence of a falsification attempt | see `out_a1_index.txt` | `out_a3_bare.txt` §6 |

**The counts moved, and that is not a finding against c9876.** The population is *every
directory under `code/`* and this repository gains directories daily; mg-724a's gate observed
207 membership candidates on the rebased tree where its author's worktree observed 206, on the
same afternoon. `a1` re-measures with **c9876's own detector, loaded as a module and hashed**,
and prints the drift as arithmetic. What would be a finding is the *detector* changing, and
`a1 §1` is where that would show.

## The rule this directory is run under

> **THESE ARE CANDIDATES.** A membership test is not a defect; it is a construction that CAN be
> one. Reporting the 202 as defects would be the same error the whole mg-9876 line has been
> correcting: a count taken off a pattern sieve rather than a measurement.

So every cell below is one of

- **LAUNDERED** — measured. The check is satisfied by the GOOD world, or reports success over a
  failing arm.
- **DISCRIMINATES** — measured. The check answers differently on a known-good and a known-bad
  input (a2), or is not already satisfied by the good world (a4, and a4's is the weaker claim
  of the two — it is stated as such in the transcript).
- **CANNOT-TELL-WITHOUT-RUNNING** — not measured. A **first-class outcome**, never rounded to
  clean, and counted beside the other two.
- **CANNOT-LAUNDER-A-GREEN** — structural, needs no run: the site's answer never reaches a
  verdict, or is not a membership test at all.

## The arms

| arm | subject | how it can fail |
|---|---|---|
| `a1_index.py` | the index, re-measured with c9876's detector | §1 exercises the loaded patterns on the two constructions c9876's own repair distinguishes (`X in out` vs `for line in out.splitlines()`), and hashes the detector file |
| `a2_tee.py` | the `\| tee` sites | §3 requires a synthetic `> file` runner and a synthetic `PIPESTATUS` runner to come back DISCRIMINATES while a synthetic `\| tee` runner comes back LAUNDERED, in the same run |
| `a3_bare.py` | the directories with no falsification evidence | §5 plants five directories, one per answer, including one whose entire apparatus is an EMPTY FILE NAMED `selftest.py` |
| `a4_membership.py` | the membership candidates | §4 replays the known instance out of git **by blob**, three-sided: TRUE-ON-GOOD on the real report, FALSE-ON-GOOD on the same report with the unconditional line removed, and NOT-A-MEMBERSHIP-TEST on the quotation of the defect in the repaired file at HEAD |
| `a5_selftest.py` | this instrument | five planted files for the anatomy classifier, one planted directory for the recorder, and one planted directory whose file digests itself — which a4 must refuse rather than measure |

`run_all.sh` contains **no `\| tee` and no `\|\| true`**, and says why in its own header: a
runner that laundered its arms' exit codes inside the suite measuring laundered exit codes
would be the next instance rather than a report of one.

## Why this is NOT wired into `build.sh`

mg-724a, mg-e331 and mg-06d1 all wired their suites into the merge gate, and this one is not,
for **mg-724a's own stated reason**: its `a4` counts were left `recorded` rather than `gated`
because *"a4's counts sweep every directory under `code/` and would turn unrelated branches
red"*. Every figure in this directory has that shape — it is a **dated reading over the whole
corpus**, and a merge gate comparing it against a baseline would block the next author's
unrelated branch the moment somebody adds a directory. That is not hypothetical here: it
happened to mg-724a on a live merge request, in 40 minutes.

The cost is the second reason and it is measured rather than asserted: `a2` alone runs four
real suites under a 300 s budget and `a4` sweeps up to 1500 s. See `out_a2_tee.txt` and
`out_a4_membership.txt` for the per-directory timings.

## What this directory does NOT establish

1. **a4 ran the healthy world only.** `FALSE-ON-GOOD` says a check is *not already satisfied*;
   it does **not** say the check would fire. Only `a2` runs its subject both ways, and only
   over the tee sites.
2. **Polarity is a reading.** a4 decides whether a needle names a bad-world marker by looking
   for words like `FAIL` and `Traceback` in it. A negative-control expectation phrased in
   ordinary English is read as POSITIVE and lands in CANNOT-TELL. The error is conservative
   and it is why CANNOT-TELL is large.
3. **The registry's SUBJECT sentences are untouched**, for c9876's reason: a probe is written
   FROM the subject, so a subject that misdescribes its arm yields a probe that agrees with it.
   Nothing here claims to settle that, and nothing here should be read as having tried.
4. **a3's scope is inside the directory.** "No record of a falsification attempt" means no
   record *in that directory*. Another directory may have falsified it from outside; a3 does
   not look, and says so.

## Defects of my own, all kept

- **D1 — a kill that did not land, inside the arm about runners.** `a2`'s first `run()` was
  `subprocess.run(..., timeout=...)`, which kills `sh run_all.sh` and nothing else. The
  producer it had launched survived the budget and went on writing tracked transcripts while
  the arm measured the *next* directory. I watched `out_b2_census.txt` change after a2 had
  moved on. That is mg-a71f's finding — a killed run is not a verdict — committed inside the
  arm whose whole subject is what a runner does with a status it cannot see. Repaired with
  that ticket's own mechanism (`start_new_session` + `killpg`, `t2_census.py:128`).
- **D2 — a consumer detector that answered `everyone who types the words`.** `a2.consumers()`
  first grepped for the string `run_all.sh`, and reported three README.md files and a
  committed transcript as consumers of an exit code. Tightened to require a status read, it
  still reported `census_remainder_f8e5/d5_timeout.py:87` — which is the string
  `'subprocess.Popen(["sh", "run_all.sh"]'` **inside a membership test**, i.e. one of the very
  candidates this directory adjudicates, counted as a consumer by the arm doing the
  adjudicating. That is mg-9876's own 597 one layer up. Only a parsed `Call` counts now.
- **D3 — I uppercased my evidence.** `a3`'s outcome matches were `.upper()`ed before printing,
  which made §2 read as though c9876's case-**sensitive** token test had missed the literal
  string `CAUGHT`. It had not: the tree had written `caught`. Destroying the evidence while
  reporting on evidence is this ticket's subject. The case is kept now.
- **D4 — my own directory is in the population it measures.** `a1` counts it, `a3` scored it a
  HOLE before `a5` existed, and `a4` skips it because running a4 from inside a4 is not a
  measurement. This is mg-724a's D1 arriving again and it is left visible in the tables rather
  than filtered out.
- **D5 — the anatomy classifier's `assigned-used` reaching test is deliberately loose.** Any
  later `Load` of the assigned name counts, including a print. It errs toward calling a site
  verdict-bearing, because the cheap error is to excuse a check somebody does read.
