# mg-64cb — PREDICTIONS for THE LANDING/AUDIT CONCURRENCY SWEEP

Committed **before one line of the instrument exists**. Scored in `REPORT.md` after.

The ticket asks a population question nobody has asked: how many landings in this arc
carried figures from a parent document that was under audit? My job is to answer it
*before* choosing a remedy, because the ticket forbids serialising every landing behind
every audit if this has happened once.

---

## H — EXPOSURE, DISCLOSED RATHER THAN LAUNDERED

A prediction about something I have already measured is not a prediction. These are
measurements, and nothing below is scored on them.

- **H1. My ticket body prints the mg-8d63 / mg-5cba case in full** — both ids, the five
  repairs, their before and after values, and the fact that a rebase conflict is what
  caught it. Every reproduction of that one case in this tree is a **FORMALITY**. It is
  the *seed*, not a finding.
- **H2. I RAN THE POPULATION SWEEP BY HAND BEFORE WRITING THIS FILE, and I know the
  counts.** Over 624 `onethird` work items (137 strict audits, 240 items whose merge
  commit touches a canonical document), a first-cut join produced **47
  landing/parent/audit triples**, bucketed by the two intervals `[claim, done]`:

  | bucket | STATE.md | docs-only | total |
  |---|---|---|---|
  | **CONCURRENT** (intervals overlap) | 3 | 10 | **13** |
  | audit-after-landing | 5 | 4 | 9 |
  | audit-before-landing | 5 | 12 | 17 |
  | unmeasurable (missing timestamps) | 3 | 5 | 8 |

  So **P1 IS NOT A BET ABOUT WHETHER THE NEAR-MISS IS UNIQUE. I ALREADY KNOW IT IS NOT.**
  The ticket's own instruction — *do not serialise without measuring (1) first, because if
  this has happened once the cure is worse than the disease* — is **already discharged on
  the raw count**, and discharged against the ticket's expectation. What remains live is
  whether that 13 survives hand adjudication, which is the whole of P1.
- **H3. I know the timestamp coverage**: 565 of 624 items carry a `work.claim` event and
  562 carry `work.done`. The 8 unmeasurable triples are unmeasurable for that reason and
  for no other.
- **H4. I read `mg schedule --help` before predicting** and know that the **dependency gate
  already exists and is enforced** — a `pending` item with `depends:` is not promoted to
  `available` until its parent is `done`. So P6 is a bet about a **count and a cost**, not
  about whether a mechanism would have to be built.
- **H5. I have read `mg-8d63.result.json` and `mg-5cba.result.json` in full.** I have read
  **none** of the other 12 concurrent cases' tickets, verdicts, documents or diffs.
  Everything in P1–P5 and P7–P8 about those is a live bet.

---

## P — THE BETS

### P1 (0.80) — MY OWN HEADLINE 13 IS AN OVER-COUNT

At least **4 of the 13** CONCURRENT triples are not the shape the ticket describes, on
hand adjudication, for one of two reasons: **(a)** the "landing" AUTHORED the document it
edited rather than carrying a parent's figures outward, so there was no parent figure to
carry; or **(b)** the "audit" audits a **sibling or a different document** from the one
the landing read, so the two never touched the same number.

This is the over-report this ticket is most exposed to, and it is exposed to it in the
direction that makes the ticket look most important. I would rather score my own headline
down than publish a population count that is really a count of my join being loose.

### P2 (0.70) — AT LEAST ONE OTHER REAL CASE EXISTS

Setting mg-8d63 aside, **at least one** of the remaining 12 CONCURRENT triples is a
genuine instance: a landing that carried a figure outward while a concurrent audit was
repairing that same figure. If this is FALSE — if mg-8d63 is the only real one in 47
triples — then the ticket's premise survives as stated and remedy (a) really would be a
cure worse than the disease.

### P3 (0.50) — AND ONE OF THEM STILL CARRIES THE WRONG FIGURE TODAY

For at least one collision other than mg-8d63, a figure the audit repaired is **still
wrong in a canonical document at HEAD**. This is the ticket's question 2 and the one that
separates *a near-miss caught by rebase* from *one that landed and stayed*. A coin-flip is
an honest number here: I have not looked, and the arc is disciplined enough that a later
audit may have swept each one up.

### P4 (0.75) — THE REBASE IS THE ONLY REBASE

mg-8d63 is the **only** case in the population where a **rebase conflict** is what
surfaced the collision. Every other real case, if any, was caught by a later audit, by a
reader, or not at all. The ticket calls the rebase "luck with good hygiene attached"; the
bet is that the luck did not recur.

### P5 (0.60) — THE `audit-after-landing` COLUMN IS A FAN-OUT, NOT A RACE

4 of the 5 STATE.md rows in the `audit-after-landing` bucket share **one** parent
(mg-6bc2) and **one** audit (mg-41b7). The bet is that hand-reading confirms this is a
*different defect* from the ticket's: not two concurrent tickets colliding, but **many
landings built on one document whose audit had not been dispatched yet**. If so it needs
naming separately, because remedy (b) — re-read from the audit's verdict — has nothing to
re-read from at the moment those landings ran.

### P6 (0.85) — REMEDY (a) COSTS ONE FIELD, NOT NEW MACHINERY

`depends:` already gates promotion, and the evidence is in the pair this ticket is about:
**mg-5cba carried `depends: [mg-789d]` and waited; mg-8d63 carried `depends: []` and did
not.** The audit was sequenced behind the parent by an existing mechanism, in the same
dispatch, and the landing was not. So remedy (a) is `depends: [<the audit>]` on the
landing, and the honest cost question is not *can we* but *how long would it have held*.

### P7 (0.55) — AND THE COST IS SMALL FOR MOST AND LARGE FOR ONE

Under remedy (a), a landing waits until its parent's audit is `done`. Measured as
`audit_done − landing_claim` over the CONCURRENT set: **the median delay is under one
hour, and at least one case exceeds four hours.** The interesting number is the tail, not
the median — a rule whose median cost is nothing and whose worst case blocks a headline
for half a day will be judged on the worst case.

### P8 (0.65) — THE RULE CAN BE CHECKED, NOT MERELY DECLARED

A machine check can answer, at landing time and from data that already exists, the
question *"does an unfinished audit of my parent exist?"* — and it can answer **both
ways**, i.e. it can be shown refusing a landing that should be refused and passing one
that should pass. If this fails, remedy (c) (a figure-provenance line per number) is the
only one left that does not depend on who noticed a conflict.

---

## E — MY OWN ERRORS, FILED IN ADVANCE

- **E1. My `landing` is git-measured and therefore too wide.** "Its merge commit touched
  `STATE.md`, `docs/` or `README.md`" counts every document-*authoring* ticket as a
  landing. This inflates the denominator and can inflate the numerator. It is the direct
  cause of P1 and I chose it anyway, because the title-based reading ("LAND" in the title)
  finds 45 items and misses every landing that did not say so.
- **E2. My parent extraction reads `depends:`, the `mg-XXXX-followup` tag, and the first
  1500 characters of the body.** A landing that names its parent only in prose further
  down is INVISIBLE to me, so the population is a LOWER BOUND and I must not report it as
  a census.
- **E3. `[claim, done]` is not the reading window.** `work.claim` is stamped by pogod at
  spawn and `work.done` at merge, so my interval includes merge-queue time. An overlap I
  report may be a *queue* overlap rather than a *reading* overlap — the landing may have
  finished reading before the audit's repairs existed, and still show as CONCURRENT.
- **E4. I AM A LANDING CARRYING mg-5cba's AND mg-8d63's FIGURES.** Every number in my
  report about the five repairs is read from their records. If I quote one that has since
  moved, I commit the exact defect I was sent to report, inside the report.
- **E5. I bet my own headline down and then adjudicate it myself.** An author who
  pre-registers "my number is too big" and then finds it too big has arranged to be right
  either way. The adjudication must therefore be per-case and printed, so the reader can
  disagree with each one.
- **E6. Commits that do not name their work item are invisible** to the git-measured
  reading, so a landing whose commit subject omits `(mg-XXXX)` cannot be in my population
  at all.
- **E7. `depends:` may be advisory in practice even though it gates in principle.** If
  items are created directly in `available/` rather than `pending/`, the gate never fires
  and P6's mechanism is a mechanism nobody uses. I must check that a real onethird item
  was actually HELD by it, not merely that the help text says it would be.
- **E8. I will be tempted to report "13" as though the denominator were 47.** It is not:
  8 triples are unmeasurable, so the measured denominator is 39, and the population of
  landings the join could even see is 240 of 624.
- **E9. Do NOT re-open the five figures.** The ticket forbids it and they are settled on
  mg-5cba's audited values. If any probe here recomputes one of them and disagrees, that
  is a defect in my probe and it goes in the defect list — it does not move a figure.
