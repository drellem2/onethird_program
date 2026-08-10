# mg-fd9c — predictions for THE HEAD CORPUS IS NOT A FIXED POINT

**Committed before one line of `libfd9c.py` exists.** Everything below is written
against a directory that holds this file and nothing else.

---

## 0. THE EXPOSURE, DISCLOSED RATHER THAN LAUNDERED

This ticket is unusual in this arc: **it names its own answer in its title, and it
hands me the two numbers the answer is about.** So the disclosure below is longer
than the predictions, and it has to be, because a prediction made after the
measurement is a transcription.

**H1 — MY TICKET BODY PRINTS THE PHENOMENON.** `818/589`, `1984/1966`, `seven runs`,
and the causal story (`the corpus includes its own auditors, so each run changes what
the next run measures`) are all in the dispatch. Nothing I say about *what was
observed* is a prediction.

**H2 — I READ THESE IN FULL BEFORE WRITING THIS FILE.**
`code/grain_arity_9160/README.md`, `code/grain_arity_9160/lib9160.py` (corpus
section), `code/grain_arity_9160/s1_reproduce.py`, `code/grain_arity_9160/run_all.sh`,
`code/grain_axis_audit_03d1/lib03d1.py`, `code/grain_axis_audit_03d1/a1_axes.py`
(A1d), `code/grain_axis_audit_03d1/a6_self.py` (AF1),
`code/grain_axis_audit_03d1/README.md`, `code/runner_exit_audit_56dc/lib56dc.py`
(`outs`, `count_rows`, `_classify`, `grain_of`), `code/runner_exit_repair_70c7/lib70c7.py`
(`outs`), `code/truncate_sweep_ec63/README.md` and `lib_ec63.trees()`,
`code/corpus_universe_1d6c/README.md`.

**H3 — NINE MEASUREMENTS ARE ALREADY IN HAND.** I ran these *before* writing this
file, in throwaway clones of this repository under `/tmp`, with **nothing in this
worktree written or regenerated**. They are MEASUREMENTS, not predictions, and no
prediction below is allowed to be a restatement of one:

| | measured, before this file existed |
|---|---|
| **M1** | at `c689ad0` on a clean tree the arc-wide census is **825 files / 2015 rows / 592 words / 485 e-rows / 1262 e-ints** |
| **M2** | `mg-9160`'s committed `out_s1_reproduce.txt` prints the HEAD row **818 / 1984 / 458 / 1198 / 589** — c9160's figure, and it does **not** hold at `c689ad0` |
| **M3** | `c689ad0` alone added **7** transcripts (`code/lstar_789d/`), moving the census by **+7 files / +31 rows / +3 words** |
| **M4** | re-running `mg-9160`'s suite in a clone at `c689ad0`: the six transcripts are **byte-identical from run 2 through run 10**, and the printed HEAD row is **825/2015/485/1262/592** at every run |
| **M5** | re-running `mg-9160`'s suite in a clone at `757f999` with the tree's transcripts **absent** — c9160's own condition — reproduces **818 / 1984 / 458 / 1198 / 589** exactly, at run 1 on disk and printed from run 2 on; runs 2–5 are byte-identical |
| **M6** | `count_rows(out_s1_reproduce.txt)` = **18**, and `1984 − 1966 = 18` |
| **M7** | running `s1_reproduce.py` with a plain `>` in the clone at `c689ad0` prints **1997**, against **2015** in the `.new`+`mv` regime: a drop of **exactly 18**, `files` unchanged at 825 |
| **M8** | `mg-03d1`'s A1d publishes 15 corpus-dependent figures; at `c689ad0` they read **825 / 2015 / 592 / 32 / 5 / 0 / 555 / 174936 / 20695 / 154241 / 88.2 % / 37 / 666 / 160 / 76.0 %** against the published **517 / 1191 / 400 / 26 / 4 / 0 / 370 / 79800 / 11204 / 68596 / 86.0 % / 30 / 435 / 104 / 76.1 %** |
| **M9** | the arc records the self-inclusion at **four** sites I found by reading: `grain_axis_audit_03d1/README.md:122`, `runner_exit_repair_70c7/lib70c7.py` (ORDERING NOTE in `outs`), `truncate_sweep_ec63/README.md` (109 vs 110), `corpus_universe_1d6c/README.md` (STATE C is not stable) |

**What that leaves.** M1–M9 settle *what happened*. They do not settle **why the
arc believed it was a non-convergence**, whether **any** tree in the arc genuinely
fails to converge, how **large** the affected population is, or what the **published
form** of such a figure should be. Those are what the predictions are about, and I
have deliberately not measured them yet.

---

## 1. THE PRINCIPAL BET

**P1 — THE OSCILLATION IS NOT AN OSCILLATION, AND `1966` IS THE OBSERVER'S OWN
WEIGHT. — prior 0.90**

D7 says the row count *oscillates between 1984 and 1966 without converging*. I bet
it does not oscillate at all: **the census map reaches a byte-stable fixed point at
run 2 and holds it**, and the two values are the **same corpus read under two write
regimes** —

```
1984  =  the corpus with the observer's own transcript on disk   (.new + mv)
1966  =  the same corpus with the observer's own transcript empty  (plain >)
1984 - 1966 = 18 = count_rows(out_s1_reproduce.txt), exactly
```

M6 and M7 establish the arithmetic and the mechanism at `c689ad0`. **What is
predicted is the transfer:** that running `s1_reproduce.py` under a plain `>` at
`757f999`, in c9160's own corpus state, prints **exactly 1966** — not 1965, not
1967. If it prints anything else, P1 is LOST and I will say so in the same table
that scores it.

**Why this is not free.** A drop of 18 at `c689ad0` fixes the *rule*; it does not
fix the *value* at another ref, because `out_s1_reproduce.txt` is regenerated at
each ref and its own row count is a measurement, not a constant. P1 is a bet that
that particular number did not move between `757f999` and `c689ad0`.

---

## 2. THE REST

| | bet | prior |
|---|---|---:|
| **P2** | **self-inclusion alone CONVERGES.** For a tree whose probes print a number of count rows that does not depend on the values they print, the census map is idempotent after one application. I bet `mg-03d1`'s suite — the other arc-wide corpus consumer, five minutes a run, never iterated by anyone — also reaches a byte-stable fixed point, and does it by run 3. | 0.72 |
| **P3** | **the arc's real instability is GROWTH, not oscillation.** Over the arc's own commit sequence the arc-wide census is **monotone non-decreasing** in `files` at every commit that touches `code/*/out_*.txt`, with **0** decreases. | 0.60 |
| **P4** | **the affected population is bigger than mg-03d1.** ≥ **25** distinct published figures, in ≥ **3** trees, are computed against a disk glob of the whole-repo transcript corpus, counting one figure per printed row and per prose number. | 0.75 |
| **P5** | **at least 3 of them reached PROSE** — a README, `STATE.md`, or `docs/` — carrying no ref and no date, so that a reader cannot tell which corpus they are figures about. | 0.80 |
| **P6** | **the reconstructed row is byte-stable and I will confirm it**, and it is byte-stable for a reason that is not a virtue of reconstruction: it reads through `git ls-tree`, so it cannot see an untracked file, which is the same blindness `lib56dc.outs()` documents as the reason the arc globs the disk in the first place. So reconstruction **fixes the stability and loses the run**, and I bet the cost is nameable in one sentence and is: *a reconstruction cannot measure the corpus a tree's own run ranged over*. | 0.85 |
| **P7** | **my own instrument commits the defect it measures.** This tree writes `out_*.txt` into `code/`, so its own transcripts join the corpus every census here ranges over, and **my own published figures will be stale the moment this branch merges**. I bet the size of my contamination is ≥ 40 count rows, i.e. ≥ 2 % of the corpus row count, and I bet I can only report it as a *range* and not as a number. | 0.70 |
| **P8** | **the arc already half-recorded this and nobody joined it up.** The ticket says *nothing in the arc records it*. I bet that is FALSE at ≥ 3 sites (M9 says 4 — so this is scored on whether those sites **record the phenomenon** or merely **record a symptom**), and that what is genuinely absent is not the observation but the **convention**: no site in the arc states an error bar, a ref, or a stability class for a corpus figure. | 0.65 |
| **P9** | **the convention already exists in miniature and was never generalised** — `corpus_universe_1d6c`'s STATE A / STATE B / STATE C (two frozen refs and one drifting worktree, with STATE C declared unstable in advance). I bet my convention is that one, generalised, and that I add exactly one thing to it: a **stability class printed beside the figure** rather than in prose a reader has to find. | 0.55 |

---

## 3. ERRORS OF MY OWN, FILED IN ADVANCE

**E1 — P1's arithmetic is a coincidence until the mechanism is exhibited.** `18` is
a small number and the corpus has 2015 rows; some other 18-row difference could
produce the same gap. The only thing that makes P1 more than numerology is running
the probe under both regimes at the same ref and getting the two values out, which
is what M7 does at `c689ad0` and what P1 bets at `757f999`. **If I report P1 HIT on
the arithmetic alone, that is the defect.**

**E2 — I did not see c9160 run.** Every statement here about *what c9160 did* is an
inference from what reproduces. c9160 may have edited `s1_reproduce.py` between its
seven runs, in which case both values are real and neither is a regime. I cannot
distinguish those two stories from inside this worktree, and P1 being right about
the arithmetic does not make it right about c9160.

**E3 — my clones are not c9160's worktree.** `757f999` + the tree's sources from
`65e350e` is my reconstruction of c9160's disk. If c9160 had any other untracked
file matching `code/*/out_*.txt`, my baseline is wrong and so is every number that
rests on it.

**E4 — a census that converges is not a census that is right.** P2 is about a fixed
point, not about a correct value. A tree whose probes all print the same wrong
number every run converges beautifully.

**E5 — the survey's population is a glob of my own choosing.** P4 counts figures
computed against `code/*/out_*.txt`. A figure computed against a *different* corpus
with the same disease is invisible to it. `corpus_universe_1d6c` is the tree that
already proved this class of blindness costs sites, and I will inherit it.

**E6 — "monotone" in P3 is a property of a commit ORDER.** The arc's history is not
linear in the sense the word implies; I will state which walk I took and P3 is only
about that walk.

**E7 — I am about to move published numbers.** The ticket forbids moving a
published number without saying which figure moved and by how much, in the same
commit. Every figure this tree recomputes at HEAD is a candidate. **My rule: this
tree writes no number into any other tree's file, and every drift I report is
printed as `published → HEAD now`, both values, never one.**

**E8 — the error bar could be theatre.** A convention that decorates a figure with
a range nobody can check is worse than a bare number, because it looks like rigour.
If the convention I land cannot be mechanically checked, it is a style guide, and I
will label it one.

**E9 — P7 predicts my own contamination and then I get to measure it.** That is a
bet whose subject I control. It is worth something only because the number is fixed
by how much this tree prints, which is decided before I can see the total — and I am
writing this before `libfd9c.py` exists, which is the only reason it is a bet at all.
