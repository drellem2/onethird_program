# mg-ec63 — OUTCOMES: every row of PREDICTIONS.md scored

PREDICTIONS.md was committed at `454f565`, **before any script of this instrument
existed**. Nothing in it has been revised. Where a prediction is wrong it is
scored MISS and left as written, including the two that are wrong in the way this
arc keeps being wrong.

Scored against the transcripts in this directory, which are from the run that
ships them.

| row | prediction | verdict | what actually happened |
|---|---|---|---|
| **P1a** | truncating runners ≠ 86, lands in [80, 100] | **HIT** | **96** over a population of 110 — **95** over the 109 this sweep is about, once this suite's own runner is set aside (README, "S6a/SD1b IS A FALSE POSITIVE"). The gap is the rule: a text regex mis-parses two of the six runner idioms and cannot see two more. |
| **P1b** | ≥10 runners write no transcript at all; `state_claims_repair_0120` is one | **HIT** | **13**, and `state_claims_repair_0120` is one of them — it streams every section to stdout. |
| **P1c** | ≥1 runner comes back UNRESOLVED rather than guessed at | **HIT** | **3**, each printed with the line that defeated the resolver: two `cd`-into-another-tree, one `python3 -c`. |
| **P2a** | the tightened rule gives ≤40 biting | **HIT** | **32 steps in 19 trees.** |
| **P2b** | ≥8 of mg-03d1's 43 fall out under the tightened rule | **PART** | The STALE class is **12 steps in 11 further trees** — 11 trees do fall out at the tree grain, which is ≥8. But I cannot map my 30 onto *its* 43 tree-for-tree, because its 43 was measured over a population containing a tree I do not have. The direction is confirmed; the arithmetic against its list is not, and pretending otherwise would be the orphaned-number error again. |
| **P2c** | the text rule differs from observed opens **in both directions**, ≥1 each way | **HIT** | **58 false positives** and **28 false negatives** over 422 steps; 336 agree. Both directions, by more than an order of magnitude over the predicted floor. |
| **P3a** | SAME ≥60% of confirmed bites | **MISS** | **11 of 32 = 34%.** The prediction assumed the residue would be small; it is not. 14 are NONDETERMINISTIC and 3 hit the timeout on both runs — categories P3a's arithmetic did not allow for, which is the flaw in the prediction rather than in the result. Of the 15 steps that produced a clean comparison, 11 are SAME (73%) — but that is a population chosen *after* seeing the answer, and it is recorded here as such rather than promoted to the headline. |
| **P3b** | ≥1 DIFFERENT beyond mg-bf79's own | **HIT** | **4**, in four different trees, all with the same mechanism: a census over the tree's own artifacts that cannot see its own transcript, so numerator *and* denominator are understated. `branching_audit_d330` goes `72 occurrences` → `73`; `face_geometry_audit_6653` goes `7 in this audit's own scanner` → `9`. |
| **P3c** | ≥1 NEVER EXERCISED, and say so plainly if 0 | **MISS**, escape clause honoured | **0.** No probe in the emptied population fails against a populated transcript. Said plainly: the class the ticket calls the worst and easiest to miss is empty in this sweep. |
| **P3d** | ≥1 confirmed bite where A does not reproduce the committed transcript | **HIT** | **21 of 32** have drifted; only **11** reproduce. Among the 4 DIFFERENT rows, only **1** reproduces — which is why S4a2 exists and why three rows are `suspect` rather than `wrong`. |
| **P4a** | name the published claim per DIFFERENT tree, or state none does | **HIT** | Done, and split: **1 proven** (A byte-identical to the committed transcript), **3 drifted**, **0** with any changed integer appearing in prose. |
| **P4b** | ≥1 DIFFERENT tree where no prose claim rests on it | **HIT**, and larger than predicted | **All 4.** No integer that moves between A and B appears in any of those trees' `.md` files or commit subjects. Recorded as a result: on this branch the idiom cost the published record nothing this instrument can find. |
| **P5a** | the bf79 control recovers **exactly 9**, and any other number means the instrument is wrong | **MISS** | Two things went wrong, and the second is the interesting one. At HEAD the control **cannot fire**: `p5_self.py` detects its own emptied transcript and falls back to HEAD — mg-bf79 closed the hole *twice* and recorded once. Re-run at `675c2ba`, the last revision without that fallback, the control **fires** at **+27 rows**, but not at 9. P5a's error was assuming a figure measured against the 2026-08-05 tree is reproducible against the 2026-08-06 one; that tree has been republished twice since. **This arc's own recurring error, made inside the prediction written to guard against it.** Kept exactly as written. |
| **P6a** | I will not reach step 2 (fixing the other 84) and will say so | **HIT** | The fix was applied to **no other tree**. Named under WHAT I DID NOT DO rather than left to silence. |
| **P6b** | `git status` byte-identical across `code/` before and after | **PART** | On the shipping run: **0 lines of change outside this tree**, across `code/` *and* `docs/`. It was **not** clean on the first three passes — killed probes left an unreadable file, an injected directory, two strike files, an armed shell script, and two appended sections in `docs/`. The prediction's population was also too narrow: it said `code/`, and `docs/` is where the worst of it landed. |
| **P7a** | ≥1 published `N of M` where **M counts an empty file** | **HIT** | All four DIFFERENT rows are this. The empty file sits in the denominator as a member contributing nothing, exactly as P7a described it — and in `face_geometry_audit_6653` it sits in the *exclusion* count, which is worse: an artifact excluded from a census on the grounds of being the auditor's own, undercounted because it could not be read. |

**16 rows scored: 12 HIT, 2 PART, 2 MISS. No row revised.**

---

## The disclosures, checked

D-1 through D-6 were measurements already taken when PREDICTIONS.md was written,
labelled as such rather than laundered into predictions. All six hold, with two
corrections that belong here rather than in the prediction table:

- **D-1** said 109 runners at `fe6a495`. Correct then. It is **110** now, because
  this suite acquired a runner. D-1 was a measurement of a tree that no longer
  exists in that state, and S1a prints both numbers.
- **D-3** said **1** runner carries the structural fix. Still **1** — and for a
  reason D-3 could not have anticipated: this suite ended up *not* using
  `.new`+`mv` but something stronger (a work directory outside the repository),
  which the resolver classifies as `TRUNC`. See the README's correction section.

---

## The four defects this suite found in itself the hard way

Twelve are measured in S6; a thirteenth (SD5b) is corrected in prose in the
README. Four were caught by something other than reading the output, and those
are the ones worth naming here:

| | the tell |
|---|---|
| **SD3** — invented probes called `can`, `the`, `ridge` | every parsed path validated against the disk |
| **SD3a** — a **write** counted as a **read**, then the evidence **misattributed** | `git status` after the pass. The mode fix is right and its measured effect is **0**; the two modified transcripts were written by probes of *other* trees. A rigorous fix with a confidently wrong mechanism |
| **SD6d** — a **child's** read attributed to its **parent**, and not stable | arithmetic: S2 printed 37 EMPTIED steps and S3, reading the same ledger, swept 36 |
| **SD6f** — **the sweep's own transcript destroyed by the arc it was sweeping** | a zero-byte `out_s2_bite.txt` beside `exit 32`, and a SUMMARY with the S2 row missing — a vacuous pass of exactly this ticket's shape, produced by the sweep for it |

SD6f is the one to carry forward. It is not a bug in this code: a 40-step subset
of the same probe writes its transcript perfectly. It is that **a suite which
executes 422 of the arc's own probes cannot keep its in-flight output inside the
arc.** The repair is structural — transcripts, ledger, shim and traces live under
`$EC63_WORK` outside the repository and land in the tree only after the last
probe has exited.

---

## One thing this suite did that the ticket did not ask for, and one it did not do

**Did:** it ran mg-bf79's probe at a revision other than HEAD, and that is what
turned "the control does not fire, so the instrument is suspect" into "the
control cannot fire, because the subject has a second defence nobody recorded."
The first sentence would have been a false confession.

**Did not:** it never ran any of the 32 swept probes at *their* publishing
revisions. That is the work that converts the three *suspect* rows into *wrong*
or *fine*, and it is the largest thing this ticket leaves open.
