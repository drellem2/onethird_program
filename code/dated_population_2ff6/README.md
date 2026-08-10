# mg-2ff6 — ADOPTING THE DATED-POPULATION CONVENTION

**This is the ticket where the published numbers move.**

mg-fd9c decided the convention — FROZEN / GROWING / OBSERVED, a value with a
date — and wrote the checker that enforces it, and moved **no** published
number anywhere: its `run_all.sh` proves that with `git status` rather than an
assertion. This ticket adopts the convention in the two trees the checker was
pointed at, and in the ten prose sites cfd9c deliberately did not touch. That
means moving published output, and the whole of the accounting is
`out_d1_moved.txt`.

## THE HEADLINE

**Of the 22 arc-wide corpus figures in the two trees, 13 moved and 9 did
not — and the 9 were never stale.** Their population is a **ref**, so they are
constants; they were only ever *undated*. A ticket that had "refreshed the
stale figures" would have rewritten nine numbers that cannot go stale and
called it a repair. Telling those two apart, without re-running anything, is
the entire thing the convention buys.

| figure | published | now | |
|---|---|---|---|
| `ARTIFACTS in that corpus` | 517 | **854** | OBSERVED |
| `count ROWS in them` | 1191 | **2233** | OBSERVED |
| `distinct grain WORDS` | 400 | **638** | OBSERVED |
| `grain WORDS classifying NONE` | 370 | **598** | OBSERVED |
| `unordered PAIRS of grain words` | 79 800 | **203 203** | OBSERVED |
| `PAIRS it collapses` | 68 596 | **179 108** | OBSERVED |
| `the disk at HEAD now` (5 fields) | 818/1984/458/1198/589 | **854/2233/576/1441/638** | OBSERVED |
| `grain WORDS classifying BOTH` | 0 | 0 | OBSERVED — and still 0 |
| mg-9160's `400`, `79 800`, `11` | — | unchanged | **FROZEN @9f1ecaa+eacc5e1** |
| A1e's three `AXES` rows | — | unchanged | **FROZEN**, a hand list |

The pair counts more than doubled because they go as the square of the word
count. That is why "is the figure stale" was never the right question.

## THE SCORE, BY cfd9c's OWN CHECKER, RUN AND NOT COPIED

`d2_convention.py` contains **no checker**. It runs
`corpus_fixedpoint_fd9c/s4_convention.py` as a subprocess and reads the answer
off its output. There is no code here that *could* respecify it — which is the
ticket's trap, since cfd9c already respecified this checker once after it
failed on cfd9c's own tree.

| | at `5c0849a` | now |
|---|---|---|
| arc-wide figures S4c finds | 27 | **27** (excluding this tree) |
| …carrying a dated population line | **0** | **22** |
| `grain_axis_audit_03d1` | 0 / 18 | **18 / 18** |
| `grain_arity_9160` | 0 / 4 | **4 / 4** |
| the four trees this ticket is not scoped to | 0 / 5 | 0 / 5 |

**It did fail on me first, and the checker was not touched.** Two of my own
population lines wrapped, so `population:` was on one line and the `@ref` on
the next — and S4c reads the ref off the line carrying the word. It scored
`grain_axis_audit_03d1` at **15 of 18**. The probes were shortened, and
`lib2ff6.pop` now **refuses** a multi-line population text, because *remember
not to wrap* is not a fix.

**And `27` was never the right target.** S4c says in its own text that it
over-collects on the LABEL; the five rows outside the two trees in scope are a
13-file per-tree census, a control that is meant to read `0`, and a tree
counting its own rows. Finishing at 27 of 27 would have meant editing four more
trees to make a checker print a rounder number. `d2d` prints all five with
their values.

Including this tree's own transcripts the live reading is **35 of 40** — my own
E3 arriving in my own number, since `code/dated_population_2ff6/out_*.txt` is
in the glob S4c censuses. Both readings are printed.

## THE 10 PROSE SITES — DATED, NOT RECOMPUTED

**0 of 10 figures changed. 10 of 10 now carry a ref.** The check points the
unusual way round: a prose site *fails* if its figure moved. `517` still says
517; what it now also says is `[pop @9f1ecaa+eacc5e1, OBSERVED]`, so a reader
who re-runs the probe and gets 854 has measured the arc's growth rather than
found a refutation. Each of the four `.md` files carries the same closing note
explaining the three classes and why `@9f1ecaa+eacc5e1` is a **union of two
refs** — and that note names **no HEAD value**, because a ticket about dating
figures that put a fresh undated one into prose would be its own
counterexample.

**And the arc's own prose check cannot see any of it.** Named in advance as P9:
cfd9c's S2c prints its ref count as a **printed literal `0`**, beside a `noref`
it computes over the *path* rather than the line and then never uses. Both
halves fail in the same direction. It is not repaired here — repairing it means
re-running cfd9c's suite, which would overwrite `out_s4_convention.txt`, the
BEFORE reading this ticket's whole D2 rests on.

## A FINDING NOBODY ASKED FOR: DATING A VALUE DOES NOT DATE A MEMBERSHIP

`out_a6_self.txt` carries a table with **one row per tree** that has an
uncounted count inside a label. **Five rows left that table and five joined
it** between `5c0849a` and this run. The convention dates *values*. Nothing in
it reaches a published table whose **row set** is a function of the corpus, and
a reader diffing the two transcripts by value finds rows with no counterpart on
the other side.

## MY OWN BETS: 8 HIT, 1 MISS

The miss is **P2**, and it is instructive: I bet S4c would score `22 of 27`.
It scores `35 of 40`, because **this tree's own transcripts joined the corpus
it censuses** — filed in advance as E3 and it still caught me in a number. The
restricted reading *is* 22 of 27 and it is printed; the bet is **not** scored
on it.

P7 (rounds 2 and 3 byte-identical) hits at **12 of 12 transcripts**, and the
arm earned its keep: it caught `d1_moved`'s row order being non-deterministic —
two DROPPED rows transposing whenever the current text shifted by a line —
which nothing else here would have noticed.

## TEN DEFECTS, ALL KEPT

D1 my population lines wrapped and S4c was right to fail them; D2 my prose
follower reported two *dated* sites as **deleted** because it matched a fixed
48-character stem and my own marker lands at character 35; D3 I made two old
trees import a new one; D4 the ref is a commit and my three rounds read three
different disks; D5 the ref is one commit early in every transcript here;
D6 my accounting cannot see a moved **percentage**, because `86.0% → 88.6%` is
not a count row and two of them moved in `a1_axes` unnamed; D7 two of my nine
bets are scored by reading; D8 I republished a claim cfd9c refuted
(`s1_reproduce.py` still says the row count *oscillates without converging*)
because repairing it is a different ticket's edit; D9 my roll was not
deterministic; **D10 my scorer read the first count row with a given label, my
own `d2` prints one of them four times, and it scored P3 a MISS that is a HIT
and printed P2's evidence off the BEFORE block** — the labels are unique now
and `figure()` raises on a duplicate.

## WHAT THIS TICKET DID NOT DO

1. It did not touch the four other trees S4c flags — all five rows are
   per-tree censuses or controls, and `d2d` prints them.
2. It did not repair cfd9c's S2c.
3. It did not re-run `a2`–`a5` of mg-03d1 — `d1d` names all five transcripts
   left at their published bytes, and `a4` runs another tree's whole suite
   twice.
4. It did not make a growing figure comparable to itself. Two dated readings of
   `count ROWS in them` are two facts about two corpora.
5. It did not date a membership.

## FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed before `lib2ff6.py` existed and before any probe was edited, with H1–H5 disclosed as measurements |
| `lib2ff6.py` | the instrument: cfd9c's convention re-exported, the selector **extracted** from cfd9c's source rather than re-typed, the section-and-ordinal row key, the accounting, the prose-site follower |
| `d0_selftest.py` | 7 arms including three the selector must **reject**, a fixture built to break a label-only key, and the check that nothing this ticket prints into another tree is a count row |
| `d1_moved.py` | **the accounting** — every count row of every re-run transcript, published → now, with its delta |
| `d2_convention.py` | the score, by running cfd9c's checker as a subprocess |
| `d3_prose.py` | the 10 sites: dated, and **not** recomputed |
| `d4_self.py` | the convergence arm, the bets, ten defects, what was not done |
| `run_all.sh` | three rounds; the only runner in this arc that accounts for what it wrote outside its own directory instead of proving it wrote nothing |
