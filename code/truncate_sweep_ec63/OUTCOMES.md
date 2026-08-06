# mg-ec63 — OUTCOMES: every row of PREDICTIONS.md scored

PREDICTIONS.md was committed at `454f565`, **before any script of this
instrument existed**. Nothing in it has been revised. Where a prediction is
wrong it is scored MISS and left as written, including the two that are wrong in
the way this arc keeps being wrong.

Scored against the transcripts in this directory, which are from the run that
ships them.

| row | prediction | verdict | what actually happened |
|---|---|---|---|
| **P1a** | truncating runners ≠ 86, lands in [80, 100] | **HIT** | **95**, over a population of 110 (109 without this suite). The gap is the rule: a text regex mis-parses two of the six runner idioms and cannot see two more. |
| **P1b** | ≥10 runners write no transcript at all; `state_claims_repair_0120` is one | **HIT** | **13**, and `state_claims_repair_0120` is one of them — it streams every section to stdout. |
| **P1c** | ≥1 runner comes back UNRESOLVED rather than guessed at | **HIT** | **3**, all printed with the line that defeated the resolver: two `cd`-into-another-tree, one `python3 -c`. |
| **P2a** | the tightened rule gives ≤40 biting | **HIT** | **37 steps in 21 trees.** |
| **P2b** | ≥8 of mg-03d1's 43 fall out under the tightened rule | **PART** | The STALE class is **13 steps in 11 further trees** — so 11 trees do fall out at the tree grain, which is ≥8. But I cannot map my 32 onto *its* 43 tree-for-tree, because its 43 was measured over a population that includes a tree I do not have. The direction is confirmed; the arithmetic against its list is not, and pretending otherwise would be the orphaned-number error again. |
| **P2c** | the text rule differs from observed opens **in both directions**, ≥1 each way | **HIT** | **56 false positives** and **32 false negatives** over 422 steps; 334 agree. Both directions, by more than an order of magnitude over the predicted floor. |
| **P3a** | SAME ≥60% of confirmed bites | **MISS** | **12 of 37 = 32%.** The prediction assumed the residue would be small; it is not. 14 are NONDETERMINISTIC and 5 hit the timeout on both runs — categories P3a's arithmetic simply did not allow for, which is the flaw in the prediction rather than in the result. Of the 18 steps that produced a clean comparison, 12 are SAME (67%) — but that is a population I chose *after* seeing the answer, and it is recorded here as such rather than promoted to the headline. |
| **P3b** | ≥1 DIFFERENT beyond mg-bf79's own | **HIT** | **6**, in six different trees, all with the same mechanism: a census over the tree's own artifacts that cannot see its own transcript, so numerator *and* denominator are understated. |
| **P3c** | ≥1 NEVER EXERCISED, and say so plainly if 0 | **MISS**, and the escape clause is honoured | **0.** No probe in the emptied population fails against a populated transcript. Said plainly: the class the ticket calls the worst and easiest to miss is empty in this sweep. |
| **P3d** | ≥1 confirmed bite where A does not reproduce the committed transcript | **HIT** | **25 of 37** have drifted; only **12** reproduce. Among the 6 DIFFERENT rows, only **1** reproduces — which is why S4a2 exists and why five rows are `suspect` rather than `wrong`. |
| **P4a** | name the published claim per DIFFERENT tree, or state none does | **HIT** | Done, and split: **1 proven** (A byte-identical to the committed transcript), **5 drifted**, **3 with an integer of the delta also appearing in prose** — labelled a candidate, not a proof. |
| **P4b** | ≥1 DIFFERENT tree where no prose claim rests on it | **HIT** | **3**, including the one *proven* row (`runner_exit_repair_70c7 :: r6_self.py`): its committed transcript provably is a defect run, and nothing published rests on it. |
| **P5a** | the bf79 control recovers **exactly 9**, and any other number means the instrument is wrong | **MISS** | Two things went wrong, and the second is the interesting one. At HEAD the control **cannot fire**: `p5_self.py` detects its own emptied transcript and falls back to HEAD — mg-bf79 closed the hole *twice* and recorded once. Re-run at `675c2ba`, the last revision without that fallback, the control **fires** at **+27 rows**, but not at 9. P5a's error was assuming a figure measured against the 2026-08-05 tree is reproducible against the 2026-08-06 one; that tree has been republished twice since. **That is this arc's own recurring error, made inside the prediction written to guard against it.** P5a is kept exactly as written. |
| **P6a** | I will not reach step 2 (fixing the other 84) and will say so | **HIT** | The fix was applied to **no other tree**. Named under WHAT I DID NOT DO in README.md rather than left to silence. |
| **P6b** | `git status` byte-identical across `code/` before and after | **PART** | It is now, and it was **not** on the first two passes. Killed probes left an unreadable file, an injected directory, two strike files, an armed shell script, and **two appended sections in `docs/`** — a measurement that edited the arc's prose. The prediction's population was also too narrow: it said `code/`, and `docs/` is where the worst of it landed. Fixed by `restore_arc()`; recorded as SD6c. |
| **P7a** | ≥1 published `N of M` where **M counts an empty file** | **HIT** | Every one of the six DIFFERENT rows is this. `audit_2c77`: `84 site(s) in all; 20 …` → `87; 21`. `audit_330a`: `ALL 86 / 21 / 36` → `87 / 21 / 37`. `branching_audit_d330`: `72 occurrences` → `73`. The empty file sits in the denominator as a member contributing nothing, exactly as P7a described it. |

**14 rows scored: 9 HIT, 2 PART, 3 MISS. No row revised.**

---

## The disclosures, checked

D-1 through D-6 were measurements already taken when PREDICTIONS.md was written
and were labelled as such rather than laundered into predictions. All six hold,
with one correction that belongs here rather than in the prediction table:

- **D-1** said 109 runners at `fe6a495`. Correct then. It is **110** now, because
  this suite acquired a runner. D-1 was a measurement of a tree that no longer
  exists in that state, and S1a prints both numbers.
- **D-3** said **1** runner carries the structural fix. It is **2** now, for the
  same reason. mg-03d1 reported 2 and I reported 1, and neither was wrong: they
  were counts over the two different populations D-2 describes, and now mine has
  become 2 by the same mechanism that made theirs 2.

---

## Defects of this instrument, and where each was caught

Seven, measured in S6. Three were caught by something other than reading the
output, which is the only reason they were caught at all:

| | caught by | |
|---|---|---|
| **SD3** — invented probes called `can`, `the`, `ridge` | validating each parsed path against the disk | a quoted `step "F2: can the V6 row go red?"` split on whitespace |
| **SD3a** — a **write** counted as a **read**, then the evidence **misattributed** | `git status` after the pass | the mode fix is right; its measured effect is **0**; the two modified transcripts were written by probes of *other* trees, killed before cleanup |
| **SD3b** — the restore rested on files happening to be **tracked** | the selftest assertion that checks the restore | git cannot restore what it does not track; every swept tree is tracked, so no number was affected — the guarantee was resting on a coincidence |
| **SD4** — a `shift` sharing a line with an assignment was invisible | the `expect` trees resolving to a probe named `0` | every positional parameter after it off by one |
| **SD1** — this tree is a member of the population it counts | S1a, by construction | both numbers printed |
| **SD2** — the audit hook sees only the probe's own process | reading the probes for `subprocess` | reported as a **bound**, not a measurement |
| **SD6b** — timed-out steps recorded as not-reading when the truth is not-known | S2a | **every count in S2b is a lower bound**, said where the number is printed |
| **SD6c** — a killed probe leaves **another ticket's fixture** on disk | `git status -- code docs` | `docs/` was edited by a measurement |

---

## One thing this suite did that the ticket did not ask for, and one it did not do

**Did:** it ran mg-bf79's probe at a revision other than HEAD, and that is what
turned "the control does not fire, so the instrument is suspect" into "the
control cannot fire, because the subject has a second defence nobody recorded."
The first sentence would have been a false confession.

**Did not:** it never ran any of the 37 swept probes at *their* publishing
revisions. That is the work that converts the five *suspect* rows into *wrong* or
*fine*, and it is the largest thing this ticket leaves open.
