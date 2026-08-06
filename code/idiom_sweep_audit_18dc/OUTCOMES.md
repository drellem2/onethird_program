# mg-18dc — PREDICTIONS, SCORED

Scored against `PREDICTIONS.md`, committed at `b8f92cd` before any script of
this audit existed. **Nine hit, three missed, one unscored. Misses are kept as
written.** Two are misses because of a defect in my own instrument, and that is
said where it happened rather than repaired backwards into a hit.

| | prediction | verdict |
|---|---|---|
| **P1** | zero pre-existing arc runners modified between `eacc5e1` and `7fccb4e` | **HIT** |
| **P2a** | the tree missing from `9f1ecaa` is `grain_axis_audit_03d1`, mg-03d1's own | **HIT** — exactly 1 tree, and it is that one |
| **P2b** | the 109 at `d33970b` partitions 86 + 2 + 21 as mg-03d1 printed | **HIT** |
| **P3a** | execution-derived truncation count > 86 | **HIT** — 88 |
| **P3b** | ≥ 1 false positive of the regex | **HIT** — exactly 1 |
| **P3c** | ≥ 3 false negatives of the regex | **HIT** — exactly 3 |
| **P4** | the bite count is not 43 | **HIT** — 11 trees / 16 transcripts |
| **P5a** | ≥ 1 of the 11 `SAME` steps breaks in **both** arms | **MISS** — 0 of 11 |
| **P5b** | ≥ 1 of the 11 completes cleanly over an **empty population** | **UNSCORED** — see below |
| **P5c** | mg-ec63's `classify()` returns `SAME` on a step that cannot run at all | **HIT** |
| **P6** | `tee`-without-`pipefail` and the truncating set overlap in ≥ 10 runners | **MISS** — 0 |
| **P7** | ≥ 1 file outside the subject directory dirtied by the run A4d restores from | **MISS** — 0 |
| **P8** | ≥ 1 transcript does not converge on a `.new`+`mv` tree mg-03d1 did not use | **HIT** — 1 of 7 |
| **P9** | ≥ 3 defects of this instrument, ≥ 1 an instance of the audited class | **HIT** — 13, at least four self-instances |

---

## P5a is the one that mattered, and it is a miss

The pre-registered hypothesis was that mg-ec63's `NEVER EXERCISED = 0` would
turn out non-empty once the class was measured properly — that its `SAME` bucket
was absorbing probes which cannot run at all. Re-running its own 11 `SAME` steps
at its own tree state: **10 INERT READ and 1 SAME. Zero break in either arm.**
mg-ec63 was right about all eleven.

**The structural half of the criticism survives and the empirical half does
not.** P5c holds: `classify()` reaches `NEVER EXERCISED` only when the *healthy*
arm breaks while the *defect* arm works, so a probe failing against real input
lands in `SAME`, and the reported 0 is a property of the rule. But the class is
also empty in fact. *"Unsupported"* and *"wrong"* are different words and only
the first applies.

**This is also where my instrument nearly wrote the finding for me.** The first
V4 pass reported **6 steps CANNOT RUN AT ALL** — exactly the pre-registered
result — and all six were an artifact: my disposable clone had no local `main`
(SD14) and five of the six were timeouts folded into a verdict they had no
business being in. The count was stable, reproducible, and about my own harness.
It was caught by reading a traceback rather than counting it.

## P5b is unscored, and that is a defect of the prediction

P5b said *"completes cleanly in both arms over an empty population — a vacuous
pass"*. "Empty population" is not a property I can read off a probe's stdout
without a rule for what its population is, and I never wrote one. The nearest
thing I did measure is **INERT READ — the probe opens the emptied transcript and
produces byte-identical output either way: 13 of 25, and 10 of the 11 `SAME`
rows.** That is a real and interesting class — the read is decorative, the answer
does not depend on the artifact — but it is not what P5b said. Scoring it as a
hit would be moving the target.

## P6 is a miss because my own rule read a comment as code

The first pass found 23 runners using `| tee`, 31 setting `pipefail`, and an
overlap of 20 with the truncating set — a comfortable hit. 29 of those 31 are
the comment *"`set -o pipefail` is not used: /bin/sh is dash on Linux, which
rejects the option"*, the most repeated line in this arc's runners; 22 of the 23
`tee` matches are the same kind. Corrected: **1** runner uses `tee`, and it
**does** set `pipefail`, so the population is empty and the overlap is 0. The
prediction is wrong and the number that made it look right was mine.

## P7 is a plain miss

I predicted a run of `runner_exit_repair_bf79` would dirty at least one path
outside its own directory, making mg-03d1's one-directory `git status` assertion
narrower than the run. Measured over the whole clone: **6 inside, 0 outside.**
The scope is narrower in principle and adequate in fact for the tree it guards.
mg-ec63 found the general version from the other end (`b9fc6a9`); on this
subject it does not bite.

---

## The predictions I declined to file

`PREDICTIONS.md` declined the timed-out steps, the three *suspect* trees, and
the `>`/`tee` causal question. Two were right and one was a hedge:

- **the timeouts** — right, and the reason got worse: 22 killed at a 240 s
  timeout, 27 at 420 s, because the machine was busier. The unmeasured set is
  not a fixed list of trees.
- **the suspect trees** — right. Nothing here could have settled them.
- **the `>`/`tee` relation** — a hedge. Having measured both populations the
  honest statement was available: they do not overlap because one is empty, and
  that is a fact about repair history rather than about the shapes.

---

## Disclosures, re-checked

All eight disclosures in `PREDICTIONS.md` were measurements taken before the
predictions were written, and all eight survive re-derivation by the shipped
probes. D1's revision table is `out_v1_population.txt`/V1a. D4 and D5 — the
commit whose subject announces a repair its diff does not contain — are the only
findings in this audit resting on `git log` rather than on execution, and they
are checkable in three commands.
