# mg-fd9c — the HEAD corpus **is** a fixed point; the arc is not

**From c9160's defect D7, via pm-onethird's ticket, whose central claim this
tree refutes and whose central worry it confirms.**

Run: `sh run_all.sh` (about a minute, pure Python 3, no network). Six probes,
all six expected to exit 0. Nothing outside this directory is written and
`run_all.sh` **checks that** rather than asserting it.

One probe is **not** in `run_all.sh` because it clones the repository and runs
two other trees' suites nine times:

```
python3 x1_orbit.py --sandbox /tmp/fd9c-orbit      # ~20 min, refuses to run inside the repo
```

---

## THE HEADLINE, IN ONE PARAGRAPH

D7 says the arc-wide row count **oscillates between 1984 and 1966 and does not
converge**, and names the cause: *the tree writes into the population it counts*.
The observation is real; the mechanism is not. **The census map reaches a
byte-stable fixed point at run 2 and holds it** — six consecutive runs of
mg-9160's suite from c9160's own corpus state in the committed `out_x1_orbit.txt`
(and **twelve** in the same experiment run by hand before this tree existed,
`PREDICTIONS.md`/M5, which is five more than c9160's seven), plus three of
mg-03d1's, all period 1. **1984 and 1966 are not two states of one system. They are two
readings of one state**, taken under the two transcript-write disciplines that
are both live in this arc today:

```
818  1984  458  1198  589      `.new` + `mv`   -- what run_all.sh does
818  1966  457  1197  589      a plain `>`     -- what a hand-run does
  0    18    1     1    0      the difference = count_rows(out_s1_reproduce.txt)
```

Both rows are measured, at `757f999`, off one corpus, in `X1b`. The `files`
column does not move because `>` truncates and does not unlink, and that is the
fingerprint that tells the two regimes apart.

**Self-inclusion alone converges.** The sufficient condition is one sentence: if
a probe prints a number of count rows that does not depend on the *values* it
prints, one application of the map fixes the corpus row count and every later
one is the identity. Every probe in mg-9160, in mg-03d1 and here has that shape.
S1c iterates the map in memory with three renderers built to cycle at periods
2, 3 and 5 and the detector returns those periods — so `period 1` is a
measurement and not a thing this instrument always says.

**And this suite is a fixed point of itself.** Its transcripts are
byte-identical across two consecutive runs — the same property it measures in
mg-9160 and mg-03d1, on the one tree it is allowed to change.

## AND THE TICKET'S REAL WORRY IS WORSE THAN IT SAYS

The corpus does not oscillate. **It grows, and every arc-wide figure this arc
has published is stale.** Recomputed at HEAD by the parents' own rules:

| | mg-03d1 published | `@5c8f879` | moved |
|---|---:|---:|---:|
| ARTIFACTS in the corpus | 517 | 832 | +315 |
| count ROWS | 1191 | 2093 | +902 |
| distinct grain WORDS | 400 | 614 | +214 |
| grain words classifying `NONE` | 370 | 577 | +207 |
| unordered PAIRS of grain words | 79 800 | 188 191 | **+108 391** |
| PAIRS it collapses | 68 596 | 166 682 | +98 086 |
| collapse rate over the corpus | 86.0 % | 88.6 % | +2.6 pp |
| ROWS with a count inside the label | 246 | 504 | +258 |
| integer ITEMS inside labels | 626 | 1283 | +657 |

**Read the right-hand column with its `@` on.** It is the corpus at `5c8f879`
**including this tree's own seven transcripts** — 78 rows, 3.7 % of it — because
the run that produced these figures had already written them. On a clean tree
before this suite runs, the same column reads 825 / 2015 / 592. Both are true;
they are readings of two different populations, and the whole of §"the
convention" below is about saying which one you mean.

**21 of 22** published arc-wide figures have moved; the exception is
`classifying BOTH`, published 0 and still 0. The pair counts have **more than
doubled**, because they go as the square of a word count that grew — so the
drift is not even linear in the corpus.

**And the shelf life is the number that should end the argument.** Walking all
**245** first-parent commits of this branch that touch a transcript:

| | |
|---|---:|
| commits in the walk | **245** |
| commits at which mg-03d1's `517 / 1191` was the right answer | **0** |
| commits at which mg-9160's `818 / 1984` was the right answer | **1** |
| steps where `files` decreased | 1 |
| steps where `rows` decreased | 2 |

mg-03d1's pair is the answer at **no commit that has ever existed** — its
population is the union of two refs, which is a state this repository was never
in. That is c9160's P7 miss, mechanically confirmed and given a size.

## THE TICKET SAYS NOTHING IN THE ARC RECORDS IT. THAT IS FALSE AT FOUR SITES

- `grain_axis_audit_03d1/README.md:122` — *"517, 1191 and 400 are larger than
  the 510, 1068 and 363 the same probes printed before this tree was written,
  because **this audit's seven transcripts joined the corpus it measures**."*
- `runner_exit_repair_70c7/lib70c7.py`, the ORDERING NOTE inside `outs()` — the
  truncate-before-probe mechanism, stated exactly, for one tree's file list.
- `truncate_sweep_ec63/README.md` — *"the population acquired a member that is
  the counter the moment this directory had a runner"*, and mg-03d1's A4b
  prediction going from right to wrong when it did.
- `corpus_universe_1d6c/README.md` — **STATE C is not stable**, declared in
  advance, with the reader told what to expect on a re-run.

**What is missing is not the observation. It is the convention**, and S4c
measures its absence mechanically: of **27** arc-wide corpus figures in the
arc's transcripts, **0** carry a dated population line.

## THE CONVENTION, DECIDED (item 4)

`corpus_universe_1d6c`'s STATE A/B/C, generalised into a class any figure can be
assigned by two booleans, plus a rendering rule and a checker:

| class | when | published form |
|---|---|---|
| **FROZEN** | population is a ref | `1191 @9f1ecaa+eacc5e1` |
| **GROWING** | population is a disk glob, censor outside | `832 @5c8f879 (GROWING)` |
| **OBSERVED** | population is a disk glob, censor inside | `2019-2093 @5c8f879 (OBSERVED)` |

The interval on an OBSERVED figure is **not** a statistical error bar and
calling it one would be theatre. It is the two readings the apparatus actually
admits, and its width is the censor's own weight — one call to `own_weight`.
Note that `files` gets an *empty* interval (`832-832`) because a file count
cannot tell the regimes apart: a convention that decorated every figure equally
would be decorating the one figure that is not at risk.

**It is a check, not a style note.** S4c runs it over the arc (0 of 27) and over
this tree (5 of 5), and this tree's `pop()` has no form that omits the ref.

## IS RECONSTRUCTION THE ANSWER? (item 3) — YES FOR THE RECORD, NO FOR THE RUN

It reproduces `517 / 1191 / 246 / 626 / 400` on a disk that has grown by 315
files since, and it is stable **for a checkable reason**: its input is two tree
hashes, not a directory. What it costs and cannot do, each with a size:

- **it cannot see an untracked file** — and a tree's transcripts are untracked
  on the run that writes them, which is the documented reason this arc globs the
  disk at all. mg-03d1's own 7, mg-9160's 6, this tree's 7.
- **it cannot be computed from any single commit** — shelf life 0, above.
- **it cannot say which write regime produced a figure** — 1984 and 1966
  reconstruct equally well.
- **it needs two refs worked out by hand, once per figure** — `PARENT_REV` and
  `PARENT_PUB` are constants a human typed into `lib9160.py`. Reconstruction is
  an archival act, not an instrument you can point at the arc.
- **and it needs those refs to stay reachable.** Checked, not assumed:
  **`9f1ecaa` is not an ancestor of HEAD.** The arc's one stable instrument
  rests on a commit that is not on this branch's history. Filed as D10, **not
  repaired** — it is mg-9160's ticket.

## PREDICTIONS, SCORED

`PREDICTIONS.md` was committed at `5c8f879`, before `libfd9c.py` existed, with
**nine hand measurements disclosed in it as measurements** rather than laundered
into predictions. **Two bets lose and neither is rescued.**

| bet | prior | outcome |
|---|---:|---|
| P1 the oscillation is not one; `1966 = 1984 − 18` | 0.90 | **HIT** — both values out of one corpus |
| P2 mg-03d1's suite converges too | 0.72 | HIT — by run 2, one earlier than the bet |
| P3 monotone growth, 0 decreases in `files` | 0.60 | **LOST** — 1 decrease, named |
| P4 ≥ 25 figures in ≥ 3 trees | 0.75 | **LOST** — 22 in 2; not rescued by S4c's 27 |
| P5 ≥ 3 undated prose sites | 0.80 | HIT — 10, none dated |
| P6 reconstruction stable, cost in one sentence | 0.85 | HIT |
| P7 my own contamination ≥ 40 rows and ≥ 2 % | 0.70 | HIT — 78 rows, 3.7 % |
| P8 `nothing records it` is FALSE | 0.65 | HIT — four sites |
| P9 the convention is mg-1d6c's plus one thing | 0.55 | SPLIT — plus **two** |

## ELEVEN DEFECTS OF THIS INSTRUMENT, KEPT

Full text in `out_s5_self.txt`/S5c. The two that matter:

**D1 — my first renderers emitted zero count rows and the headline would have
been vacuous.** `_row_line` used a single space where `lib56dc._COUNT_ROW` wants
two, so the virtual transcript never entered the census, the map was constant,
and *every* renderer "converged" — including the two built to cycle. `S0/C6` is
the anti-vacuity arm and it exists because I nearly shipped that.

**D11 — I respecified S4c's checker after seeing it fail on me, and it moved my
own score from 1 of 2 to 5 of 5.** The first form wanted a dated population line
within 12 lines and my own table is 22 rows deep. The reason for the change is
structural — a checker that fails on long tables pushes authors towards short
ones — and it moved a number **towards** me, which is the only fact that makes
the 5 of 5 worth arguing with.

Also kept: D2 (X1's first form printed `CENSUS FAILED` in every row while both
fixed-point arms went green), D3 (a character class inside a character class,
12 prose sites → 10), D4 (my `census()` is a re-typing, held by two forced arms),
D5 (I write into the population I count — sized in S5b), D6 (S4c over-collects,
by design, and I refuse to rescue P4 with it), D7 (I never saw c9160 run),
D8 (the walk is first-parent), D9 (X1's sandbox is my reconstruction of c9160's
disk), D10 (`9f1ecaa` is not an ancestor).

## WHAT I DID NOT DO

**No published number was moved. Not one byte outside this directory changed.**
Every drift is printed as `published → HEAD now`, both values, on one line. I
did not freeze the corpus; I did not regenerate any other tree's transcripts in
this worktree; I did not repair mg-03d1's or mg-9160's probes to emit dated
population lines; I did not touch the 10 prose sites in 4 tracked `.md` files; I did not determine *why*
c9160 saw its two values, only that one corpus produces both; I did not measure
what the 21 per-tree disk-glob figures would have been under the other regime;
and I did not repair D10 or sweep for other unreachable reconstruction refs.
Full list in `out_s5_self.txt`/S5d.

## FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed before `libfd9c.py` existed, with M1–M9 disclosed |
| `libfd9c.py` | the instrument: census, observer's weight, the in-memory orbit, designed-period controls, the history reader, the convention |
| `s0_selftest.py` | 16 arms, including the anti-vacuity arm and three designed-period negative controls |
| `s1_orbit.py` | **the correction** — two regimes, every tree's own weight, the orbit |
| `s2_drift.py` | the affected figures, the prose sites, and the shelf life |
| `s3_reconstruction.py` | is the reconstructed row the answer, and what it costs |
| `s4_convention.py` | the classes, the form, and a checker that runs on the arc and on me |
| `s5_self.py` | bets scored, eleven defects, what I did not do |
| `x1_orbit.py` | the runs — **not** in `run_all.sh`; clones the repo, refuses to run inside it |
| `out_x1_orbit.txt` | a **dated** measurement, not a regenerated one. It goes stale exactly the way every other figure in this arc does, and S4 gives that its class. |
