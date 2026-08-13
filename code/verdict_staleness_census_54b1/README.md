# `code/verdict_staleness_census_54b1` — stale in the STRONG sense, and who is not asking

**Work item:** `mg-54b1`, whose instance was `code/species_extent_audit_6cb9` and whose question
was the one after it: *how many instruments outside `mg-20ee`'s 44 are stale in this strong
sense?*

```
sh code/verdict_staleness_census_54b1/run_all.sh     # under 2 s, safe in your worktree
```

The runner runs the two **cheap** arms. The expensive one is `sweep_54b1.sh`, which re-runs
instruments and therefore must be pointed at a clone — see §4.

| file | what it is |
|---|---|
| `lib54b1.py` | the classifier: two rules, `VERDICT MOVED` vs `ADDRESSES ONLY` |
| `c0_controls.py` / `out_c0_controls.txt` | 17 planted worlds in both directions, 3 real diffs, and one published over-count |
| `c1_population.py` / `out_c1_population.txt` | the three populations and the size of the blind spot. Exact, no runs |
| `sweep_54b1.sh` | the expensive arm. Re-runs a sample **in a clone** and keeps every diff |
| `classify.py` / `out_sweep_54b1.txt` | reads a sweep and reports the split. **One dated run** |

## 1 — The two senses, and why they are different populations

`mg-20ee`'s `ground_truth.sh` answers **`DIFFERS` or `REPRODUCES`** — any byte. That is the
**weak** sense, and its whole pinning tranche exists because most of those bytes are **addresses**:
a sha, a line number, a corpus size, a timing. An `AS_OF` pin removes them and **no verdict has
moved**.

The **strong** sense is that the transcript's *adjudication* changed: a reader of the committed
copy is told one thing and a reader who re-runs it is told another.

`code/species_extent_audit_6cb9` is the proof that these are different populations, and every
clause of the following is measured:

* Three of its verdicts moved — `*** MISSED ***` → `as predicted`, `*** EXTENT WIDER ***` →
  `extent TRUE here` (twice), and `A1 TOTAL BAD: 1` → `0`.
* It carries **no foreign address**, so `census.py` — a classifier *for foreign addresses* — was
  never going to nominate it, and `out_ground_truth.txt` never asked it the question.
* It is not in `./build.sh`'s loop, so `mg-f771`'s fixed-point gate cannot see it either, by that
  gate's own construction: *"a transcript no suite rewrites is never modified and therefore never
  appears"*.

**A verdict can go stale with no address having moved at all.** That is the argument for this
directory existing rather than for widening `census.py`.

## 2 — The blind spot, measured exactly

`c1_population.py` recomputes all of this from `git ls-files`, from `build.sh` itself and from
`mg-20ee`'s own transcript on every run. **Nothing below is a written-in number**, which is why
this arm is a fixed point and the sweep is not.

    tracked transcripts under code/ (out_*.txt)      1052
    directories carrying at least one                 217
        with a run_all.sh to re-take them             187
        with NO runner at all                          30

    watched by ./build.sh's loop                        9
    re-run by mg-20ee's ground_truth.sh                44

    THE BLIND SPOT -- in NEITHER                      164
        of those, runnable                            137
        of those, with no runner                       27

**76 % of every transcript-carrying directory in this repository is re-taken by nothing on any
schedule.** `6cb9` was one of the 164, and it was found only because a polecat ran it for an
unrelated reason.

## 3 — The classifier, and both directions of its error

Two rules decide `VERDICT MOVED`, and **only the second uses a vocabulary**.

**RULE A — a word changed.** Erase from both sides of a changed line every token this corpus
treats as an address or a magnitude — worktree roots, repo-relative paths, filenames, bare
instrument names (`<topic>_<4 hex>`), sha-like hex, dates, clock times, durations, and then every
remaining digit run — and *delete* the placeholders rather than leaving them in place. If the line
still differs, something that is not an address changed. **This rule names no verdict words**, so
it catches vocabularies nobody enumerated: `[HOLDS]` → `[BROKEN]`, `ok` → `*** FAILED ***`,
`SILENT` → `fired`.

**RULE B — a scored counter changed.** Rule A erases digits, so a verdict whose digit *is* the
verdict survives it. `SCORED_COUNTERS` is a **declared, short list** of those shapes. It is a
vocabulary and is therefore the half that can be blind; `c0` prints it with its length, so growing
it is visible in a diff.

**Both directions are planted, and the negative half is the load-bearing one** — a classifier that
says `VERDICT MOVED` to everything measures nothing. `c0` runs 7 worlds that must fire, 8 that
must not, 2 for the other classes, and 3 real diffs from this repository's history labelled **by
their own commit messages** rather than by me.

### What it got wrong before it got it right

Three defects were found by enumerating this classifier against the defect it exists to detect,
and all three are kept as controls rather than quietly fixed:

* **`VERDICT count` read a duration as a scored counter.** Written `VERDICT:[^0-9]*(\d+)`, it
  matched the `0` of `VERDICT: CLEAN  0.11s`, so a run that got 0.03 s slower reported a moved
  verdict — **a magnitude counted as a finding, on the exact line shape `mg-f771`'s W3 declares
  NOISE, inside the rule written to keep magnitudes out.** World `N8`.
* **A census listing that gained an entry read as a word change.** Placeholders keep an address's
  *position*, so every later column shifted. Measured on the real diff of `417a789`. Fixed by
  deleting address placeholders instead of marking them — and it is **still** an over-count when
  the listing's own length changes, which is `R3` and is **published rather than tuned away**: a
  rule that could tell a census listing from a findings listing would be a rule about one file.
* **`§4`'s coverage list was hand-written and under-reported itself.** `failure tally` also matches
  the `0 failed` of `W7`'s line. It is now computed by running every world's lines back through the
  list.

**One miss is named and measured rather than reasoned about.** `3 WIDE site(s) are silent` → `1`
is one of the three verdicts this ticket itself quotes, and no `SCORED_COUNTERS` entry matches it,
so Rule A erases the digit and the line reads as an address. `6cb9` is still reported
`VERDICT MOVED` because other lines in the same run moved; an instrument whose **only** movement is
an unlisted counter would be missed outright.

## 4 — The sweep, and why it is not in the runner

`sweep_54b1.sh` re-runs each instrument in a declared sample and keeps the diff. It is not in
`run_all.sh` and not in `./build.sh`, for two reasons and not one:

* **It costs about 40 minutes** against an 88-second gate.
* **It executes every instrument in the sample**, and those instruments mutate the tree they run
  in. Several mutate directories *other* than their own and restore them; one killed by the
  timeout is killed **mid-probe**, with somebody else's file half-written. `git checkout -- .` in
  the tree you are working in is not a restore, it is a loss. **So it takes a clone as an
  argument** — the one way it differs from `ground_truth.sh`, which restores in place.

```
git clone --no-hardlinks . /tmp/sweep54b1
sh code/verdict_staleness_census_54b1/sweep_54b1.sh /tmp/sweep54b1 /tmp/sweepout 40 120
python3 code/verdict_staleness_census_54b1/classify.py /tmp/sweepout
```

**The sample is a function of the path and of nothing else** — the 137 runnable blind-spot
directories ordered by the md5 of their path, first N. There is no seed to lose, it is the same
sample in every clone and on every host, and it cannot have been chosen after the answers were
known. The **size** was chosen for a ~40-minute budget before any result was in; the **order** is
not choosable. `sweep_54b1.sh` takes its work list from `c1_population.py --sample N`, so the
population and the sweep cannot drift apart.

**The committed `sweep_54b1.sh` is not byte-for-byte the script that produced `out_sweep_54b1.txt`,
and the two differences are listed rather than left to be discovered.** The run was driven by a
scratch copy, and against it the committed file differs in exactly two places:

* **Where the work list comes from.** The run read a precomputed file; the committed script calls
  `c1_population.py --sample N`. The two lists were compared element-for-element and are
  **identical**, which is checkable — the sample is a function of the path.
* **The `load` column**, added *after* that run, which is why every row in the committed
  transcript reads `not recorded` in it. `classify.py` says so where it prints them.

Nothing about what is executed, timed or measured differs. Saying this is cheaper than a reader
finding it.

**A `TIMEOUT` is a reported class and not a drop.** An instrument the sweep could not finish
inside its budget is *unmeasured*, and `classify.py` counts it as unmeasured rather than as
reproducing. Silently skipping it would read as coverage.

## 4b — What the sweep found

One run, 2026-08-13, 40 of the 137 in md5 order, 120 s per instrument, 61 minutes wall.

    VERDICT MOVED     9        DEAD              2
    ADDRESSES ONLY    1        REPRODUCES        8
    NOT RUN           1        TIMEOUT          19
                                                ---
                                                 40

**Of the 20 it could measure, 11 are stale in the strong sense — 55 %.** Nineteen more were killed
at the budget on a host whose load average was 16 when the sweep started and 60 an hour later;
they are **unmeasured**, not healthy, and half the sample being unmeasured is this run's largest
weakness.

**Of the 12 transcripts that differ at all, exactly 1 differs only in its addresses.** That is the
number that decides whether `mg-20ee`'s remedy reaches this population, and it says it does not:
an `AS_OF` pin removes an address difference and does nothing whatever for a moved verdict. Its 44
were nominated *by a classifier for foreign addresses*, so an address-only difference is precisely
what it went looking for and precisely what pinning fixed. **These instruments do not need a
declared commit. They need anything at all that re-runs them.**

The evidence is quoted in `out_sweep_54b1.txt` §3, one `-`/`+` pair per finding, because `c0`
measures a real over-count on a real diff and a number without its evidence is a net.

## 4c — Three defects in this instrument, each found by measurement

None of these came from reading the code; each came from running it against real data, and all
three are kept as controls:

* **A magnitude counted as a finding.** `VERDICT:[^0-9]*(\d+)` matched the `0` of
  `VERDICT: CLEAN  0.11s`, so a run 0.03 s slower reported a moved verdict — on the exact line
  shape `mg-f771`'s W3 declares NOISE, inside the rule written to keep magnitudes out. `N8`.
* **A repair reported as a death.** `TRACEBACK in diff_text` was a membership test against a whole
  captured diff — `mg-9876`'s own smell — and a unified diff carries context and *removed* lines.
  Six transcripts here carry a traceback on purpose, and **this branch created the third case
  itself** by committing one into `6cb9`'s `out_a3_differ.txt`: the day `a3` is re-aimed, the diff
  reads `-Traceback` and nothing would have stopped this classifier calling that repair a death.
  `D3`, `D4`.
* **Silence read as success.** `code/anticorrelation_c50b`'s runner has no `cd` and names
  `s0_selftest.py` bare, so from the repository root it exits instantly having written nothing —
  which leaves the tree exactly as clean as a perfect reproduction. The sweep scored it
  `REPRODUCES`. **`mg-20ee`'s `ground_truth.sh` decides the same way**, so its nine `REPRODUCES`
  rows carry the same question; 13 of the 193 tracked runners have no `cd`, most of them meant to
  be run from the root. Separating those needs a per-instrument look and is **named, not done**.

## 5 — What this does not do

* **The sweep is a sample of the blind spot, not a count of it.** `c1` prints the population's
  size; `classify.py` prints the sample's.
* **It says nothing about `./build.sh`'s 9**, which `mg-f771` regrades on every merge, **nor about
  `mg-20ee`'s 44**, whose own ground truth already re-ran them.
* **It does not repair anything.** Every instrument it names is a finding for its owner.
* **It cannot see a precondition failure.** An instrument whose baseline control has gone red has
  every remaining row unscorable *without any of them changing*. `6cb9`'s `a2` arm is exactly that
  — its `R0` unmutated baseline now exits 1 — and this classifier reports the four rows that moved,
  which is true but is not the finding.

## 6 — This instrument is in its own blind spot, and does not exempt itself

`c1_population.py` §3 **counts this directory into the 164 and scores that it did**, because the
expensive arm's `out_sweep_54b1.txt` is exactly what this ticket is about: a transcript that
records one dated run and that no runner re-takes. `mg-20ee`'s `out_ground_truth.txt` has the same
property and says so in its own header — *"It is NOT a fixed point and does not claim to be"*.

The two cheap arms **are** re-taken by `run_all.sh` and are fixed points — byte-identical across
two consecutive runs, measured.

**They are still not added to `./build.sh`, and the reason is not cost.** Under 2 seconds against
an 88-second gate would be affordable. But `c1`'s numbers move the moment **any** branch adds a
directory under `code/`, so putting it in the loop would create a **third** generated census that
every such branch must refresh — and `417a789`'s own commit message is the record of what that
costs: *"every branch that adds a directory under `code/` must refresh this same generated census,
and two such branches conflict on content neither wrote by hand"*, a conflict it hit **twice**.
Manufacturing a third of those to watch a population nothing was watching would be paying for the
measurement in merge conflicts on generated files. `mg-d72e`'s warning — that adding a suite to the
loop is exactly the operation that created that bug — applies to the cheap arms too.

**And this instrument was red until its own transcripts were committed**, which is worth writing
down because it is the third time this arc has met it: `git ls-files` does not show an instrument
its own untracked files, so §3's self-inclusion row failed on the first run and passed on the
second. `mg-502f` hit the same shape (*"an instrument that reads `git ls-files` is BLIND TO ITSELF
FOR EXACTLY AS LONG AS IT IS NEW"*) and `mg-3902`'s pin hit its chicken-and-egg cousin. It is not
worked around here: the row is left able to fail, and committing the transcripts is what makes it
pass.
