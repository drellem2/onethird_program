# `superseded_figures_5827` — a repeatable way to find every site quoting a superseded input

**Work item.** `mg-5827`.
**Run it.** `bash code/superseded_figures_5827/run_all.sh` (from anywhere; it cds to the repo root).
**Gate only.** `python3 code/superseded_figures_5827/s3_gate.py` — exit 1 on any flat-text site.

---

## Why this exists

`mg-2860` swept **four sites** for the superseded-`ε_spec` class on 2026-08-06 and missed a fifth,
which was then found by a reader who happened to open the right document. Two edits repaired it
(`c413c9e`, `7645941`). Those edits are not the interesting part. The interesting part is that the
*next* stale figure will be found the same way unless something changes.

## The answer to "why did mg-2860 miss it" — measured, not inferred

Run `s2_retrospective.py`. It reports:

| measurement | value |
|---|---|
| files `mg-2860` touched | **1** (`STATE.md`) |
| its own commit message | *"FOUR SITES, FIVE LINES, NOTHING ELSE"*, and *"outside what this ticket lists"* |
| flat-text sites at its base commit `f758468`, **inside** `STATE.md` | **0** |
| flat-text sites at its base commit, **outside** `STATE.md` | **23** |
| change in the flat-text count across the sweep | **+0** |

**The list is the defect.** `mg-2860` executed a fixed list of five line numbers supplied by its
ticket, in one file, and it executed it correctly — there were **zero** flat-text sites left inside
`STATE.md`. The whole of the miss is the **file boundary**. It also swept a *different class*: its
subject was which *form* leads (limit vs constant); the numeric budget was a rider its ticket added
(*"WHILE YOU ARE THERE"*), which it landed correctly **into** `STATE.md` while never looking **out**
of it.

This is not a criticism of `mg-2860`. It was obedient, it said so in terms, and it explicitly
declared a site it was declining to touch. **The defect is in the mechanism, and a ticket-supplied
list of line numbers has no way to grow.**

## How it works

1. **The registry** (`registry.json`) holds one entry per superseded input: the stale value, the
   repaired value, the provenance of the correction, and — as a first-class field — **the direction
   of the error**, because a stale figure that flatters and one that alarms fail differently.
2. **The file list comes from `git ls-files`**, not from a glob. `docs/*.md` is `os.listdir`-shaped:
   non-recursive, and it reads the working tree rather than the index (`mg-1d6c`). A sweep that
   cannot recurse into `docs/state-history/` cannot see where the correction was recorded.
3. **Every occurrence is classified into exactly one of four buckets**, all four printed with counts:
   * `DEFECT` — flat text. The site asserts the stale value with nothing to say otherwise.
   * `REPAIRED` — the site says so: the value is struck out (`~~…~~`) on its own line, or the
     repaired value stands beside it, or a shouted repair marker sits in the same blockquote or
     within ±6 lines.
   * `AUTHORITY` — a declared file where the correction *lives*. Flagging these would be flagging
     the fix.
   * `FROZEN` — a committed transcript under `code/`: evidence at a commit, not a live claim.
4. **Exit 1 on any `DEFECT`.**

## The positive control — because a sweep that has never fired is indistinguishable from a broken one

`s1_control.py`, **27 constructions in throwaway git repositories outside this tree**:

* **C1** plants the exact sentence that was live in the primary document tonight and watches the
  detector report it — **2 defects, exit 1**.
* **C2** repairs that same sentence and watches it go quiet — **0 defects, exit 0**, while still
  *counting* both occurrences as `REPAIRED`. Silence and blindness must not look the same.
* **C3 is the mutation test**, because C1/C2 is only evidence if a detector that ignores its input
  fails it. An **always-DEFECT** detector and an **always-CLEAN** detector are each run against the
  pair and each fails.
* **C4–C11** cover the blind spots the arc has been bitten by: an unmatched `~~`, a nested directory
  a glob could not reach, an untracked file, a revision scan, a declared authority, path-prefix
  matching (`code/` must not swallow `codex/`), and the bound on the blockquote exemption.
* **C12** is the fixed-point control: writing the census down must not change the census.

## Defects of this instrument, found by its own controls and left recorded

1. **`C4` failed on the first form, and the failure was a FALSE NEGATIVE** — the direction that
   costs something. `repair_markers` contained the token `STRUCK`, matched case-insensitively, so
   the ordinary English word *"struck"* in a neighbouring sentence laundered a live stale figure
   into `REPAIRED`. A clean report and a corpus that is clean are then indistinguishable — the exact
   failure this instrument exists to prevent, inside the instrument. Repaired by matching shouted
   markers **case-sensitively**.
2. **The proximity window cut a supersession box in half** and reported its own tail as a live
   claim. Repaired *structurally* — a markdown blockquote is one annotation unit — rather than by
   widening the window, because widening buys the same coverage in exchange for false negatives.
   `C10`/`C11` bound the new exemption so one blockquote cannot silence another.
3. **THE CENSUS WAS NOT A FIXED POINT, AND THE NUMBER IT PRINTED GREW EVERY TIME ANYONE RAN IT.**
   `out_gate.txt` records every occurrence the gate finds, and the transcript is a tracked file, so
   the next run found all of them again *inside the transcript*: **691 self-occurrences against 46
   real ones**. Bucketing them as `AUTHORITY` was not enough — an exempt occurrence is still
   *counted*, so the printed totals were a fiction. The transcripts are now **out of the
   population**, not merely exempt (`registry.json` and the scripts stay in, so the instrument
   remains visible to itself), and `s3_gate.py` prints what it dropped by name. Control `C12` holds
   the property. Found only because `main` moved under this branch mid-ticket and the total jumped
   from 60 to 331 — which is the population-moves-under-my-own-hand trap, and it fired.
4. **The hand sweep of `c413c9e` missed a site and this instrument found it**:
   `docs/OneThird-lambda-std-Operative-Form.md` §7.1 told the reader the empirical probe ran *"an
   order of magnitude above the `ε_leak ≈ 0.02` the constant budget needs"*. At the repaired
   calibration `ε_leak ≈ 0.20`, so the probe ran at **exactly** the budget, not above it — and that
   very measurement is what `mg-e35c` uses to calibrate the repaired value in the first place. This
   site fails in the **opposite direction** from the headline: it made the empirical position look
   *safer* than it is, while the same superseded input at §6.3 made the *mathematical* position look
   *worse* than it is. **One superseded input, two opposite-signed errors.** Direction has to be read
   per site; it cannot be inferred from the input.

## DECLARED LIMITS — what this instrument cannot do

* **It reports only what the registry knows about.** A superseded input nobody has filed is
  invisible. The single point of failure has moved from *"whoever happens to read the right
  document"* to *"whoever lands a correction remembering to file a registry row"*. That is strictly
  better. It is not nothing.
* **It cannot express a superseded CLAIM, only a superseded VALUE.** This was filed as prediction
  P10 before the code existed and it held. The second defect this same ticket repaired —
  `STATE.md:72` listing **(A) SPREAD** among machinery that a later audited row says is off the
  critical path — is **invisible to this instrument**, because there is no stale *number* anywhere in
  it. A sentence that asserts something a later audited row denies is a different detector, and this
  is not it.
* **Its own directory is exempt** (`registry.json` must name the stale value in order to search for
  it). So a live stale figure in *this* README would not be flagged. Declared, not hidden.
* **`FROZEN` is a real weakening.** Committed transcripts under `code/` are exempted wholesale.
  `README.md` / `OUTCOMES.md` / `PREDICTIONS.md` directly inside a code directory are deliberately
  *not* frozen, because those are prose in the present tense. Any other live claim that happens to
  live under `code/` is under-reported.
* **The retrospective is not a blind re-run.** The registry was written after the fact, by someone
  who already knew where the sites were. The 23 is what a search *would* have found had the registry
  existed — not what `mg-2860` could have found with what it had.
* **No mathematics is re-derived here.** Every repaired value is `mg-e35c`'s, checked arithmetically
  against its stated inputs and no further. `mg-3ce3`'s `0 RED / 6681` was not re-run.

## Files

| file | what it is | declared exit |
|---|---|---|
| `registry.json` | the registry of superseded inputs — **the file you edit** | — |
| `lib5827.py` | the detector: file list, patterns, four-bucket classifier | — |
| `s1_control.py` | positive control + mutation test, 23 constructions | 0 |
| `s2_retrospective.py` | why `mg-2860` missed the fifth site, by measurement | 0 |
| `s3_gate.py` | the gate over the tracked corpus | 0 |
| `run_all.sh` | all three, transcripts via `.new` + `mv`, re-entrancy guard | 0 |
| `out_*.txt` | committed transcripts |  |
