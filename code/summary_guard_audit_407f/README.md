# mg-407f — INDEPENDENT AUDIT of mg-cf83, by running it

**VERDICT: mg-cf83's repair of `s1_rows.py` is CONFIRMED SOUND, in all three
arms, by a harness that shares no code with it. Its claim is true and proved.
The claim it does not make is the problem: THE SAME DEFECT IS ALIVE IN TWO
SIBLING SCRIPTS OF THE SAME DELIVERABLE, and I found it by running them, not by
reading them.**

```
sh run_all.sh      # ~6 min; clones 4 real repos, breaks 2 real remotes
```

`a1_arms.py` shares **no code** with the subject. It does not import
`lib_f3ff`. It makes real clones, breaks a real remote **after** cloning so
`origin/main` still resolves, runs the subject's scripts as **subprocesses**,
and greps their **real stdout**. mg-4d3b's entire F-series began with a
`force_fail=True` that returned before `git fetch` was ever spawned; a fix
verified by a stub reproduces that mistake, and so does an audit.

---

## 1. CHECK 1 — RUN AGAINST A REAL BROKEN CLONE. **PASSES.**

Not `force_fail`. A PATH shim recorded every `git` invocation: `git fetch
origin` was **spawned twice and exited 128 both times**, and `origin/main`
still resolved to `b7b6941b4bb3` / `42499a568f97` in the broken clones, so an
UNKNOWN is a *failed fetch*, not an absent ref.

mg-4d3b's F1–F5, hunted by literal string in real stdout, are all **ABSENT**:

| | pre-repair (mg-4d3b) | ARM B now |
|---|---|---|
| F1 | `all 4 are now checked against the tree` | `0 of 4 are checked` + rows named |
| F2 | `WRONG on 0 of its 4 rows and RIGHT on 0` | `WRONG on UNKNOWN … RIGHT on UNKNOWN` |
| F3 | `4 of 4 checked, 0 refuted` | `THIS RUN DOES NOT SUPERSEDE IT` |
| F4 | four rows of `0 / 0` | four rows of `? / ?` |
| F5 | `TypeError: len(None)` | no traceback; script completes |

**The P15 guard — a crash is not a clean UNKNOWN.** I filed in advance that my
most likely error was mistaking a death for a guard. So the pass required all
four: exit status **1**, the summary header **present**, **≥20 lines** of
stdout after it, and **no traceback**. All four hold.

## 2. CHECK 2 — PROVE THE CHECK CAN FAIL. **PASSES.**

ARM H, both clones healthy: exit 0, `REFUTED 2 of 4. UPHELD 2 of 4. UNKNOWN 0
of 4.`, `The census was WRONG on 2 of its 4 rows and RIGHT on 2.` Real
integers. Not hard-wired.

**The sharpest single piece of evidence in this audit:** rows 3 and 4 have
genuinely zero successors. On ARM H they print `0 / 0`. On ARM B *the same two
rows* print `? / ?`. **None and empty are rendered differently by the same code
on the same rows** — which is precisely what a summary hard-wired to UNKNOWN
could not do. Both directions, as the ticket demanded.

## 3. CHECK 4 — ONE PATH OR TWO? **ONE. DERIVED, NOT GUARDED.**

This is the question the ticket said would decide whether the defect survives
in a narrower form. It does not.

Every summary figure in `s1_rows.py` is a **fold over `lines`** — the tuples
the row sections themselves printed (`s1_rows.py:154-160`). `ref`, `up`, `unk`,
`n_rows`, `measured`, `unk_rows` and every depth cell come from there. **No
repo is re-read after the row loop.** mg-cf83 did what it was told: it derived
the summary from the values that already printed correctly, rather than bolting
guards onto a second computation path.

The one residual re-read — the P2 sub-clause at `:218` — is gated on the row's
own verdict (`verdicts.get(2) != "UNKNOWN"`) *and* independently None-checked,
so it cannot print a count when the row says UNKNOWN. That is the site where
F5 killed the script; the gate makes the crash unreachable rather than caught.

## 4. CHECK 5 — TRY TO MAKE THEM DISAGREE. **I COULD NOT. Here is what I tried.**

- **All-repo failure (ARM B).** Rows UNKNOWN, summary UNKNOWN. No disagreement.
- **Partial failure (ARM M).** Repo 1 healthy, repo 2 broken. The row prints
  `[onethird_program=7  one_third_width_three=UNKNOWN]` — *partial information
  is preserved and shown, not discarded* — the verdict goes UNKNOWN because
  UNKNOWN is sticky, and the summary agrees. No disagreement, and no
  over-broad blanking either, which is the failure mode I had predicted (P12).
- **A fourth verdict value.** `lib_f3ff.census_row` returns exactly one of
  `{UNKNOWN, REFUTED, UPHELD}`, so `ref + up + unk == n_rows` always and the
  `if unk:` gate is exhaustive. There is no verdict that escapes both branches.
- **Empty population.** `n_rows = 0` yields a vacuous "all 0 are checked" —
  odd, but not a disagreement, and unreachable while `ROWS` is a constant.

I could not construct an input where `s1_rows.py`'s rows say UNKNOWN and its
summary says anything else.

---

## 5. CHECK 3 — THE SWEEP. **THIS IS WHERE THE AUDIT FINDS SOMETHING.**

The ticket said: sweep for the idiom rather than trusting the three line
numbers in the parent. Doing so found that **the ticket's own spelling is too
narrow.**

A grep for `0 if not gens` finds the site mg-cf83 already fixed **and nothing
else**. `a2_idiom.py` sweeps a *family* — 14 sites across 7 scripts — and the
live one is spelled:

```python
g1 = p8_gain.get(1, 0)          # s3_graph.py:170 — the default IS the merger
```

A dict `.get` whose default is the literal zero, for a row that was never
measured. Same merger — *"I could not look"* printed as *"I looked and found
none"* — wearing syntax no sweep for the parent's string would ever match.

### FINDING 1 — `s3_graph.py`: the rows say UNKNOWN and the summary says 0. **LIVE.**

In one transcript, from a real fetch failure (`out_a1_arms.txt`):

```
  (a) tickets whose body names mg-fcf1: 5
      UNKNOWN -- a repo could not be read.        <-- the rows are RIGHT
...
  P8  ... OBSERVED: 0                             <-- the summary is WRONG
      P8: *** MISS ***
      OBSERVED: row 3 no, row 4 no                    P9: *** MISS or PARTIAL ***
      ... rows none                                   P10: *** MISS ***
== s3 exit: 0 (findings do not set this instrument's exit) ==
```

This is mg-4d3b's F-class defect, alive, in the same deliverable — rows correct,
summary block confidently zero.

### FINDING 2 — and the false zero **flips published verdicts**.

Worse than printing a wrong number. Between ARM H and ARM B, with *nothing*
changed but whether a repo could be read:

| | ARM H (healthy) | ARM B (fetch fails) |
|---|---|---|
| P9 | `P9: HIT` | `P9: *** MISS or PARTIAL ***` |
| P10 | `P10: HIT — 2 row(s)` | `P10: *** MISS *** — 0 row(s)` |

An unreadable repo does not merely print `0` — it **propagates into the
deliverable's own published scoreboard and refutes two predictions that hold.**
`UNMEASURED`, the third scoring state mg-cf83 added to `s1_rows.py` for exactly
this reason, does not exist in `s3_graph.py`.

### FINDING 3 — `s3_graph.py` **exits 0** under a total fetch failure.

`s1_rows.py` now exits 1 for *this run did not happen*. Its sibling reports
success.

### FINDING 4 — `s2_controls.py` **dies with F5, verbatim**.

```
  File ".../s2_controls.py", line 80, in main
    nfull = sum(len(x) for x in _p.values())
TypeError: object of type 'NoneType' has no len()
```

The identical `len(None)` death mg-cf83 removed from `s1_rows.py`, on the same
library call, still live one file away.

### The mechanism, stated precisely — and NOT misattributed

The four `or []` sites at `s2_controls.py:130-131` and `s3_graph.py:85-86` are
**LATENT, not live**: `s3`'s pair sits after `if before is None: continue`, and
`s2`'s sits after the crash at `:80`. Neither is reached under a fetch failure.
I checked this by **printed evidence** — the output those sites produce is
absent from the ARM B transcript — rather than by asserting it. Billing them as
the live defect would have been the easy, wrong answer.

**The shape mg-cf83 got right and its neighbours did not:** `s1_rows.py` folds
the summary out of `lines`, the rows' own output, so an UNKNOWN row cannot
become a zero downstream. `s3_graph.py` accumulates into *separate* dicts during
the row loop and folds *those* — and the loop `continue`s past them on UNKNOWN,
leaving them empty. Same author, same deliverable, same failure: one path
repaired, its neighbour not.

---

## 6. WAS THIS OVERCLAIMED? **NO — and that matters.**

mg-cf83's README says "**`s1_rows.py`** now holds three rules" and its docstring
says "three rules now hold **in this file**". Both are scoped, and both are
true. mg-cf83 **under-swept; it did not overclaim.** The residual risk is one of
*placement*: section 10 sits in `census_repair_f3ff/README.md`, the README of
the whole six-script deliverable, under the heading "the summary block,
repaired" — and a reader there may reasonably conclude the deliverable's
summary blocks are repaired, when `s3_graph.py`'s is not.

**And its detector is honest.** I predicted (P13, 55%) that `c1_summary_guard.py`
would share code with what it validates, and (P14, 50%) that one of its arms
would be simulated. **Both wrong.** It makes real clones, breaks real remotes,
runs `s1_rows.py` as a subprocess, greps real stdout, carries a mutation control
(ARM H) and an anti-vacuity check that `origin/main` resolves. It is the right
shape, and my check 1 is therefore a **reproduction of a claimed result by a
disjoint harness** — disclosed as H2 in `PREDICTIONS.md` before I ran anything —
not a discovery.

---

## 7. PREDICTIONS, SCORED AS WRITTEN — 8 HIT, 6 MISSED

Committed at `8cc1f3e` before any script of this audit existed and before one
line of the diff was read.

| | claim | conf | result |
|---|---|---|---|
| P1 | broken arm summary says UNKNOWN, not 0 | 80% | **HIT** |
| P2 | broken arm does not crash; summary completes | 65% | **HIT** |
| P3 | healthy arm reports real numbers | 85% | **HIT** |
| P4 | healthy arm reproduces `2 of 4` | 55% | **HIT** |
| P5 | an idiom site survives outside `s1_rows.py` | 72% | **HIT** (4 sites) |
| P6 | at least one surviving **`or []`** site is LIVE | 40% | **MISS** |
| P7 | distinction carried by `is None` branches, not a type | 60% | **HIT** |
| P8 | hybrid: ≥1 summary figure still independently computed | 45% | **MISS** |
| P9 | a shared record both rows and summary read | 50% | **HIT** (`lines`) |
| P10 | I fail to break it on homogeneous input | 65% | **HIT** |
| P11 | mixed input is where it breaks | 45% | **MISS** |
| P12 | over-broad UNKNOWN discards real information | 30% | **MISS** |
| P13 | `c1` shares code with its subject | 55% | **MISS** |
| P14 | ≥1 of `c1`'s arms is simulated | 50% | **MISS** |

**P6 IS A MISS AND IS KEPT AS A MISS.** I found a live defect of the same
*class* by a different *spelling*; that does not retro-fit the prediction I
actually wrote, which named `or []`. All four `or []` sites are latent.

**All six misses run in the same direction: mg-cf83 is better than I predicted.**
I forecast a hybrid repair (P8) validated by a self-referential detector (P13,
P14) breakable on partial input (P11, P12). It is a fully-derived repair with an
honest subprocess detector that already ran the mixed arm. That is a result
about my priors — a repair ticket in this arc was more likely to be sound than I
gave it credit for — and I am recording it rather than burying it.

**P15 and P16 were guards, not forecasts, and neither error was committed.**
P15's four-part assertion and P16's PATH shim are both enforced in `a1_arms.py`
and both passed. Had the shim shown 0 spawns, check 1 would have been reported
UNMEASURED, not passed.

## 8. DEFECTS OF THIS INSTRUMENT, KEPT AND NAMED

1. **My a1 docstring asserted a falsehood about mg-cf83 and I caught it by
   reading their transcript.** It first read *"ARM M — the arm mg-cf83's own
   control does NOT run."* mg-cf83 **does** run it: `out_c1_summary_guard.txt:104`
   is ARM P, *"ONE remote broken — half the population is perfectly readable."*
   My ARM M is a reproduction at the **opposite orientation** (they break repo 1,
   I break repo 2). Corrected in the source with the correction stated, not
   silently. **This is the exact error my own ticket warns about — concluding
   from what a repair "would have" skipped instead of looking.**
2. **`a2_idiom.py` first printed an explanation naming the wrong object.** It
   gave the `cell()`/`gens` reason for `c.owner or '(none)'` sites, which are
   optional metadata with no third state to lose — the same *named-the-wrong-object*
   error mg-4d3b committed and kept. Fixed, disclosed, and the family's
   false-positive rate (8 of 14 hits) is now printed rather than hidden.
3. **`a2`'s LIVE/LATENT classification is by printed fingerprint, not by
   coverage instrumentation.** It is an observation a reader can check against
   the transcript, but it is weaker than a traced execution: a site could in
   principle run and print nothing. 4 sites are left UNCLASSIFIED and are **not
   billed** rather than assumed dead.
4. **`stage()` edits the subject's `REPOS` constant.** `lib_f3ff.REPOS` is a
   hard-coded absolute path with no CLI or env override, so there is no other
   way to aim the subject at a clone. Repointing a path is not stubbing a
   failure — every fetch is real and really fails, proved by the shim — but it
   is an edit to the subject and it is named here rather than left implicit.

## 9. WHAT I DID NOT DO

- **I did not repair anything.** Findings 1–4 are reported, not fixed. No
  source file of `census_repair_f3ff/` was modified on this branch, and no
  ticket body was corrected.
- **I did not run `s0_freshness.py`, `s4_crosscheck.py`, or
  `selftest_f3ff.py`** in any arm. Three of the deliverable's seven scripts are
  therefore **unmeasured under failure**, and `s4_crosscheck.py` carries two
  UNCLASSIFIED census hits I did not chase. The sweep is a sweep of what I ran.
- **I did not re-derive the census.** `2 of 4` is inherited from mg-f3ff via
  mg-4d3b, which confirmed it from a disjoint reader; I checked only that the
  healthy arm still *reports* it.
- **I did not audit `c1_summary_guard.py`'s own checks for correctness.** I
  established its *shape* is honest (real clones, subprocess, real stdout) and
  that its ARM P exists. I did not verify that each of its 176 committed lines
  asserts what it claims to.
- **I did not open `code/idiom_sweep_audit_18dc/`.** I confirmed by grep that it
  never names `s2_controls` or `s3_graph`, so findings 1–4 are not duplicates of
  it — but I did not read it, and its relationship to this idiom is unexamined.
- **I did not test the network-failure shape**, only a broken-URL shape. Both
  produce a non-zero `git fetch`, but a hung or partially-succeeding fetch is a
  third case nobody in this lineage has exercised.
- **I did not run `run_all.sh` of the subject** in any arm, so the aggregate
  exit status under failure is unmeasured. (`s1`=1, `s2`=1, `s3`=0 individually.)
