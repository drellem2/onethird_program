# `landing_audit_sweep_64cb` — did a landing ever carry a figure its parent's audit was repairing?

**Read [`REPORT.md`](REPORT.md).** This file says only what is here and how to re-run it.

Filed against mg-8d63's rebase collision (mg-64cb). The ticket asked a population question
and forbade choosing a remedy before answering it. Answer: **13 collisions, not one; one of
them landed and is still wrong at `HEAD`; and remedy (a) costs 15.3 hours across the arc's
entire history.**

## Run it

```
./run_all.sh          # seven arms, exit 0 iff all hold; writes out_s*.txt beside them
```

No `| tee` anywhere — mg-c2b3 found 23 of 63 `run_all.sh` in this arc piping into `tee` with
one setting `pipefail`, so any of them can print FAILED and exit 0. Exit codes are read
directly.

## The arms

| file | what it does |
|---|---|
| `lib64cb.py` | the readers and the three definitions (LANDING from git, AUDIT strict, INTERVAL twice). Returns an explicit `REFUSED` rather than a default when it cannot time something. |
| `s0_selftest.py` | forced arms, including **three the classifiers must REJECT** and the `REFUSED`-propagation arms. A classifier that said yes to everything would be caught here. |
| `s1_population.py` | the census, under both interval readings, with the timeable denominator stated. |
| `s2_collisions.py` | every collision, one row, both readings side by side. |
| `s3_adjudicate.py` | four stated rules that disqualify candidates, applied before any verdict. |
| `s4_survival.py` | is a superseded figure still standing at `HEAD`? Three classes, not two. |
| `s5_cost.py` | what each of the ticket's three remedies costs, measured. |
| `s6_rule.py` | the rule as a predicate that runs, shown refusing and passing, with controls. |

## Two things worth knowing before you re-run

**The `write` reading refuses the seed case.** `mg-8d63` has one canonical commit, and one
commit is an instant, not an interval. That is why the intervals return `REFUSED` instead of
a degenerate `[t, t]`: a zero-length interval overlaps nothing, so a default would have made
this instrument report "no collision" about the collision it exists to study. `s0` forces
that arm on a live instance (`mg-845e`, whose claim and done land in the same second).

**The reader is meant to be able to disagree per case.** `s3` prints all four rule outcomes
for every candidate, and `s4` prints both the bad screen's count and the restricted one, so
the residue can be re-derived rather than taken on trust. `REPORT.md` §8 D10 names one
residue row its own author doubts and leaves it in, because removing it by hand after the
rules ran is the manoeuvre the predictions file forbade.

## Provenance

`PREDICTIONS.md` was committed before any code here existed (`db1d1cc`), with the population
count disclosed as **H2 — a measurement I had already taken** rather than laundered into a
bet. 6 of 8 predictions hit; the two misses are scored in `REPORT.md` §7, and the
informative one is P1, where my own headline turned out **less** inflated than I bet and for
reasons I had not named.

Population read at `main` as of 2026-08-10: 624 `onethird` items, 137 strict audits, 240
git-measured landings, 524 commits, 36771 store events.
