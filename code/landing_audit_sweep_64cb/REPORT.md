# mg-64cb — THE LANDING/AUDIT CONCURRENCY SWEEP

**The near-miss was not a near-miss population of one. It is one of thirteen, and one of
the thirteen is not a near-miss at all — it landed, it stayed, and it is still wrong at
`HEAD` today.**

Filed against mg-8d63's rebase collision. The ticket's instruction was: measure the
population *before* choosing a remedy, because if this has happened once the cure is worse
than the disease. The population is measured. **It has happened thirteen times**, and the
cure costs **15.3 hours of wall-clock across the arc's entire recorded history**.

Every number below is produced by `run_all.sh` (exit 0, seven arms) and is readable in the
committed `out_s*.txt` beside this file.

---

## 0. THE THREE ANSWERS, UP FRONT

| the ticket asked | the answer |
|---|---|
| **(1)** How many landings carried figures from a parent under audit? | **13**, after machine adjudication knocked 8 out of 21 candidates. 3 of the 13 touch `STATE.md`. |
| **(2)** For any found, is the wrong figure still in the canonical documents today? | **YES, in one case — `mg-51f4`.** The seed case `mg-8d63` is a confirmed **near-miss**: 0 of 4 superseded figures stand at `HEAD`. |
| **(3)** Which sequencing rule, and what does it cost? | **(a) as the default, (b) as the named escape.** (a) costs one `depends:` field and 15.3 hours arc-wide, total. (c) is refused: 1739 provenance lines for the residue alone. |

---

## 1. THE POPULATION (`s1`, `s2`)

```
count  onethird work items                     624
count  of them, STRICT audits                  137
count  of them, landing by TITLE                45
count  of them, landing by GIT (canonical doc) 240
count  of them, touching STATE.md               87
count  landing/parent/audit triples             48
```

**WHAT I SEARCHED, since the ticket asks.** The `~/.macguffin` item store (2544 items, 624
carrying the `onethird` tag or repo), the `work.claim` / `work.done` event log (36771
events), and all 524 commits on `main` with their touched files. A *landing* is measured
from git — its merge commit modifies `STATE.md`, `docs/**` or `README.md` — **not** from
its title. That choice is load-bearing and it is the reason this sweep found anything:

```
count  title-only (git never saw a canonical-doc commit)  12
count  git-only   (never said LAND in its title)         207
count  both                                               33
```

**The title reading misses 207 of 240 landings.** A sweep run on "does the title say LAND"
would have reported this arc as roughly five times safer than it is, and would have found
the ticket's own seed case and almost nothing else.

### The buckets, under two readings that disagree

`wall` = `[work.claim, work.done]`, spawn to merge. `write` = first to last commit **author**
date, which survives the refinery's rebase. They answer different questions and I report
both rather than picking the one that flatters the finding.

| verdict | wall STATE.md | wall docs | **wall total** | write STATE.md | write docs | **write total** |
|---|---|---|---|---|---|---|
| **CONCURRENT** | 3 | 10 | **13** | 4 | 9 | **13** |
| AUDIT-AFTER | 5 | 4 | 9 | 3 | 1 | 4 |
| AUDIT-BEFORE | 5 | 10 | 15 | 2 | 8 | 10 |
| REFUSED | 4 | 7 | 11 | 8 | 13 | 21 |

Both readings return **13** and they are **not the same 13**. Five triples are CONCURRENT
under both — those are the rows no reading can explain away. 21 are CONCURRENT under one
or the other, and that 21 is the candidate set the adjudication in §2 works on.

### ⚠️ THE STRICTER READING REFUSES THE ONE CASE WHERE THE TRUTH IS KNOWN

`mg-8d63` — the ticket's own seed, the case we know collided because a **rebase conflict
happened** — is **`REFUSED` under the write reading**, because it has a single canonical
commit and a single commit gives an instant, not an interval.

That is the whole argument for the wall reading, and it is an argument from ground truth
rather than from preference. It is also why `wall_interval` and `write_interval` return an
explicit `REFUSED` sentinel instead of a degenerate `[t, t]`: **a zero-length interval
overlaps nothing under any half-open rule, so a default would have scored the seed case as
`AUDIT-BEFORE` — my own instrument reporting "no collision" about the collision it was
built to study.** `mg-845e` is the same shape on the wall side (claim and done in the same
second). Both are forced arms in `s0`.

---

## 2. ADJUDICATION — MY OWN HEADLINE, SCORED DOWN BY RULES THAT RUN (`s3`)

P1 bet the headline was an over-count. Betting that and then hand-waving cases away is the
cheapest possible way to be right, so every disqualification is made by a stated rule:

| rule | what it disqualifies | fired |
|---|---|---|
| **D1** LANDING-OF-THE-AUDIT | the landing NAMES the audit in its own title or body head — it is *carrying* the audit, which is remedy (b) already working | **6** |
| **D2** AUDIT-OF-THE-LANDING | the audit's declared subject IS the landing; the triple is backwards | **1** |
| **D3** SUBJECT MISMATCH | the audit's title says *"INDEPENDENT AUDIT of mg-XXXX"* and that subject is not the parent | **2** |
| **D4** SELF-AUTHORED | every canonical file the landing touched is a document named after the landing itself | 0 |

```
count DISQUALIFIED  8
count RESIDUE      13   (3 of them touching STATE.md)
```

**P1's CLAIM SURVIVES AND P1'S REASONS DID NOT.** I named two categories, (a) self-authored
and (b) subject mismatch. **D4 — the category I led with — fired zero times.** The largest
killer is **D1, a category I did not name at all**: six of the eight are landings whose job
was to carry an audit's own findings outward. Those are not the defect; they are the
remedy, working, before anyone wrote it down.

**AND P1 LOSES ON THE NUMBER.** It bet *at least 4 of the 13* wall-CONCURRENT triples would
fall. **Three did** (`mg-200d`/D3, `mg-4417`/D1, `mg-e10a`/D1). My own scepticism was
calibrated too generously toward myself: the population is **bigger** than I bet it was.

### The residue

| landing | parent | audit | tier | wall | write |
|---|---|---|---|---|---|
| mg-00a1 | mg-131e | mg-eaa1 | **STATE.md** | CONCURRENT | AUDIT-BEFORE |
| mg-131e | mg-200d | mg-41b7 | docs | AUDIT-AFTER | CONCURRENT |
| mg-24fb | mg-5ce3 | mg-3e06 | docs | CONCURRENT | CONCURRENT |
| mg-372e | mg-131e | mg-eaa1 | docs | CONCURRENT | AUDIT-BEFORE |
| **mg-51f4** | **mg-28ff** | **mg-29fe** | docs | **CONCURRENT** | **CONCURRENT** |
| mg-81ff | mg-9461 | mg-39bf | docs | CONCURRENT | AUDIT-BEFORE |
| mg-8311 | mg-76b2 | mg-94c3 | docs | CONCURRENT | CONCURRENT |
| mg-845e | mg-3969 | mg-d3c7 | docs | REFUSED | CONCURRENT |
| **mg-8d63** | mg-789d | mg-5cba | **STATE.md** | CONCURRENT | REFUSED |
| mg-af28 | mg-1953 | mg-3b51 | docs | CONCURRENT | CONCURRENT |
| mg-b488 | mg-200d | mg-41b7 | **STATE.md** | AUDIT-AFTER | CONCURRENT |
| mg-be0b | mg-3329 | mg-07fd | docs | CONCURRENT | REFUSED |
| mg-c2b3 | mg-821e | mg-4700 | docs | CONCURRENT | REFUSED |

---

## 3. QUESTION 2 — WHAT IS STILL WRONG TODAY (`s4`)

### 3.1 THE SEED IS A CONFIRMED NEAR-MISS — 0 of 4 (`s4` arm A)

Each of mg-5cba's repairs names its **superseded** value, so this is a search and not a
screen. Every superseded figure was searched across all 163 canonical documents at `HEAD`
and classified `LIVE` (running prose, uncorrected — the defect) / `STRUCK` (inside `~~…~~`
or with the repair named within ±3 lines) / `IN-REPAIR` (inside the document publishing the
repair — quoting a wrong value in order to correct it *is* the correction).

```
R2  LSTAR(6) `0.794253`                  LIVE=0  STRUCK=5  IN-REPAIR=5   -> STRUCK
R3  Theorem A (SO) at n<=7 `338`         LIVE=0  STRUCK=5  IN-REPAIR=6   -> STRUCK
R4  (M#) triple `0.943 / 0.982 / 0.958`  LIVE=0  STRUCK=2  IN-REPAIR=2   -> STRUCK
R5  counterexample count "all three"     LIVE=0  STRUCK=2  IN-REPAIR=4   -> STRUCK

count seed probes reading LIVE at HEAD 0 of 4
```

**c8d63's hand rebuild held.** `STATE.md:170` carries every one of the five inside `~~…~~`
with the audited value beside it, and `docs/OneThird-LStar-mg-789d.md:48–58` carries the
superseded survival triple in prose *followed immediately by the blockquoted mg-5cba R4
correction*. Hand-read, not taken from the classifier.

**This is a statement about a rebase conflict and one polecat's care. It is not evidence
that any control caught anything, and it must not be read as one.**

### 3.2 ⚠️ AND ONE DID NOT — `mg-51f4` LANDED IT AND IT IS STILL THERE

`docs/OneThird-SweepLoss-mg-51f4.md:147–148`, at `HEAD`, unamended since its only commit
`2f76a01`:

> **`n = 7` IS ENUMERATED HERE, NOT SAMPLED.** `mg-28ff`'s `n = 7` figures are deterministic
> samples of 40–200 posets, **correctly labelled as such at every appearance in its
> document**, and I do not quote any of them.

`mg-29fe` — the **independent audit of `mg-28ff`**, running concurrently under **both**
readings (`mg-51f4` 20:14:37–22:37:59Z, `mg-29fe` 20:27:57–21:41:55Z) — found the opposite,
at three joints:

1. *"§4.3's summary sentence promotes a sample to an enumeration"* — directly under the
   sampled `n = 7` row it reads **"100 % at every enumerated `n`"**. That is an appearance
   **not** correctly labelled.
2. *"§8.1's own scope self-audit is false as written"* — it claims every `n = 7` row is
   labelled *sample, not a maximum*; only §4.1's is.
3. §4.2's `n = 7` population is a **different sample** from §4.1's and §4.3's (40 primitive
   vs 106), both labelled `(sample)`, and the document does not say so.

**The repair landed in the PARENT and never reached the LANDING.** `mg-28ff` now carries
mg-29fe's repair at its own `:21` — *"§4.3 summary … read a **sample** as an enumeration,
and is **false of the truth**"* — while `mg-51f4:148` still tells the reader that document
was correctly labelled at every appearance. **Two landed canonical documents contradict
each other at `HEAD`, and the contradiction is exactly the concurrency this ticket is
about.**

**THE HONEST QUALIFICATION.** This is a landed **characterisation of an unaudited parent**,
not a landed **numeric figure**. It is the ticket's *shape* — carrying outward from a
document whose audit was in flight, and the carried claim being the thing the audit
repaired — in a different currency. I am not going to inflate it into "a wrong number
reached STATE.md", because it did not: `mg-51f4`'s doc is `docs-only`, and mg-29fe measured
propagation into `STATE.md` / `roadmap.md` / the rendered twin and found **none**.

**WHY MG-29FE COULD NOT HAVE CAUGHT IT.** Its propagation sweep ran against the canonical
documents *that existed*. `docs/OneThird-SweepLoss-mg-51f4.md` was being written in the same
window and was not on `main` yet. **An audit's "nothing has propagated" is a measurement
over the corpus at the moment it runs, and a concurrent landing is invisible to it by
construction.** That is a second, independent reason the sequencing matters: the audit
cannot see the landing either.

**NOT REPAIRED HERE.** `docs/OneThird-SweepLoss-mg-51f4.md` is another ticket's landed
document. This ticket reports; it does not edit. Successor filed.

### 3.3 The screen over the other eleven, and why it is only a screen

My first draft intersected **all** numeric literals between the landing's added canonical
lines and the audit's correction lines. It flagged **13 of 13** — on section numbers
(`4.2`, `5.1`), years (`2026`) and ticket digits (`9461`). Restricted to **measured
quantities** (decimals with ≥3 fraction digits) it flags **4**:

```
count flagged on ALL literals (the bad screen)  13
count flagged on MEASURED quantities             4
```

The drop from 13 to 4 is the measurement. Of the four, `mg-51f4` is §3.2 above; the other
three (`mg-845e`, `mg-8d63`, `mg-be0b`) were hand-read and none carries a superseded value
in running prose. **A shared literal is a necessary condition, not a finding, and `s4`
refuses to call any of them one.**

---

## 4. THE STRUCTURAL DEFECT IS ONE FIELD WIDE (`s1`)

The ticket calls the defect its own and says the standing practice — pre-file the audit in
the same action — is right and is not changing. **It is right, and the missing half is
already implemented.** `mg schedule`'s dependency gate holds a `pending` item until its
`depends:` parents are `done`, and it is enforced. In the arc:

```
count  onethird items with a non-empty depends: field  154
count  of those that are AUDITS                         84
count  of those that are GIT-LANDINGS                   13
```

**The arc gates audits on their parents and does not gate landings on the audits.** The
seed pair is that asymmetry in two lines of frontmatter, dispatched in the same action:

```
mg-5cba (the AUDIT)    depends: [mg-789d]     -> HELD. Claimed 04:05, after mg-789d done 03:25.
mg-8d63 (the LANDING)  depends: []            -> NOT HELD. Claimed 05:27, while mg-5cba ran until 05:58.
```

**P6 HITS.** Remedy (a) is not new machinery. It is `depends: [<the audit>]` on the landing.

---

## 5. WHAT EACH REMEDY COSTS (`s5`)

### (a) SERIALISE — the landing waits for its parent's audit

| | |
|---|---|
| residue triples priced | 13 |
| would have waited at all | **12** |
| median wait among those | **65.7 min** |
| worst wait | **241.4 min** (`mg-131e`, waiting on `mg-41b7`) |
| **total delay, arc-wide, whole history** | **918.1 min = 15.3 hours** |

**THE TICKET'S FEAR IS REFUTED BY MEASUREMENT.** 15.3 hours is not the daily cost or the
weekly cost — it is every minute remedy (a) would have cost across **every collision the
sweep can see in the arc's entire recorded history**. Against that, one repaired-figure
contradiction standing in a canonical document since 2026-08-09, and four superseded
figures that reached a `STATE.md` row and were withdrawn only because a rebase conflict
made someone look.

### (b) RE-READ — no wall-clock, a per-landing obligation

```
count landings in the population              240
count that would have run the check            44
count where the check would have FIRED         30
fire rate among those CHECKED               68.2%
fire rate across ALL landings               12.5%
```

Both rates are the honest pair. Once a landing *has* an audited parent, a collision is the
**common case (68%), not the exception** — which is the strongest single number in this
report. Across all landings the rule is silent 87.5% of the time, so it is cheap to carry.

### (c) PROVENANCE PER FIGURE — refused on cost

```
count distinct numeric literals the residue landings added to canonical docs  1739
mean per landing                                                               134
```

134 provenance lines per landing, for the residue alone. Applied arc-wide it is the most
expensive of the three by a wide margin. **It is also the only one that would catch a figure
copied from a parent that was never audited at all** — so it is not refuted, it is
**deferred**, and §6 says where it should go instead.

---

## 6. THE DECISION

> **A LANDING MUST DECLARE `depends:` ON EVERY AUDIT OF EVERY PARENT IT CARRIES.**
> If it may not wait, it MUST re-read its figures from the audit's verdict and **say in its
> commit which values it took and from where**.

**(a) is the default and (b) is the named escape, in that order**, and the ordering is the
decision. c8d63 performed (b) by hand and it worked — but it worked *because a rebase
conflict forced the question*. The thirteen cases in §2 are the ones where nothing forced
it, and in one of them nothing caught it either.

**Why not (b) alone**, which is what the ticket leans toward: (b) is a rule about what a
polecat must *remember* while reading a document that looks finished. (a) is a rule the
scheduler enforces without anyone remembering anything, and it costs 15.3 hours across the
arc. When a mechanism already exists and the price of using it is that small, choosing the
one that depends on vigilance is choosing the failure mode.

**Why not (c)**: priced above. **Where it should go instead**: not on every figure, but on
figures a landing takes from a document it did not author *and* whose audit it did not
wait for — i.e. exactly the residue of the (a)/(b) rule. That is a much smaller set and it
is a follow-up, not this ticket.

### The rule runs, and it refuses and passes (`s6`)

`unaudited_parent(landing, at)` needs nothing new: parents from the ticket's own
`depends:`/tags/body, audits from the item store, states from the `work.claim` /
`work.done` events pogod already writes.

```
count PASS (no audited parent)           193
count PASS (every audit already DONE)     14
count REFUSE                              30
count UNTIMEABLE                           3
count TOTAL                              240
```

Non-vacuous in both directions. Forced arms: it **refuses** `mg-8d63` at its own claim
instant (`mg-5cba` RUNNING) and **passes** `mg-5cba` at its own claim instant. Two controls:
a parentless item is never refused; and asking at `t = 2099` still refuses 9 landings, each
one traced by machine to an audit that has **no `work.done` event at all** — the rule
saying an incomplete audit is incomplete, which is the rule working.

---

## 7. PREDICTIONS, SCORED

| | bet | outcome |
|---|---|---|
| **P1** (0.80) | ≥4 of the wall-13 are over-count | **LOST.** 3 fell, not 4. And **D4, the category I led with, fired zero times** while **D1, which I never named, killed six.** The claim's direction was right; its number and both its reasons were wrong. |
| **P2** (0.70) | ≥1 real case besides mg-8d63 | **WON.** `mg-51f4`, and 12 others survive adjudication. |
| **P3** (0.50) | ≥1 still wrong at `HEAD` today | **WON.** `mg-51f4:148` vs `mg-28ff:21`, contradicting each other at `HEAD`. |
| **P4** (0.75) | the rebase is the only rebase | **WON.** 0 of the other 12 residue verdicts mention a rebase catch (grep over the result sidecars). |
| **P5** (0.60) | the AUDIT-AFTER column is a fan-out, not a race | **WON.** `mg-41b7` alone accounts for 4 of the 5 STATE.md rows, across two parents (`mg-6bc2`, `mg-200d`). |
| **P6** (0.85) | (a) costs one field, not machinery | **WON.** §4. |
| **P7** (0.55) | median <1h **and** worst >4h | **LOST, on the conjunction, by 6 minutes and by 1 minute.** Median **65.7 min** (not under an hour); worst **241.4 min** (just over four hours). Both halves land within minutes of the line and the bet is scored as written. |
| **P8** (0.65) | the rule can be checked both ways | **WON.** §6. |

**6 of 8 hit. Both misses are on numbers I chose, and P1's miss is the informative one:**
I pre-registered that my own headline was inflated, and it was inflated **less** than I
allowed for, by reasons I had not thought of.

---

## 8. MY OWN DEFECTS — ALL KEPT

- **D1. MY FIRST SURVIVAL CLASSIFIER SCORED 6 OF 6 SUPERSEDED FIGURES `LIVE`, AND EVERY ONE
  WAS A QUOTATION INSIDE THE DOCUMENT THAT REPAIRS IT.** It had two classes where the
  question needs three. An instrument built to ask *"is this wrong figure still standing?"*
  answered **yes** about mg-5cba's audit document quoting the value it was correcting.
  Repaired by the `IN-REPAIR` class; the two-class version would have published four false
  "landed and stayed" findings against a ticket that is about false figures propagating.
- **D2. MY `four` PROBE MATCHED 944 LINES.** The first draft of the R5 arm searched for the
  word *four*. A probe with 944 hits across 163 documents measures the English language.
  Replaced with the specific claim (`"four counterexamples"` / `"all three"` near
  *counterexample*).
- **D3. MY BARE-NUMBER PROBE MATCHED INSIDE A 13-DIGIT INTEGER AND INSIDE A LINE REFERENCE.**
  `(?<![\d.])338(?![\d])` fires inside `1,338,193,159,771` — the comma is neither a digit
  nor a dot — and inside `:338`. Three false `LIVE`s on the arm whose entire job is deciding
  whether a superseded figure still stands. Now `(?<![\d.,:])338(?![\d,])`; it took two
  tries and the first one looked right.
- **D4. MY FIRST SCREEN FLAGGED 13 OF 13 AND I NEARLY REPORTED IT.** Intersecting *all*
  numeric literals fires on section numbers, years and ticket ids. A screen that flags
  everything is not a screen; both counts are printed in `s4` so the reader can see the
  drop rather than take the restricted one on trust.
- **D5. `[claim, done]` IS NOT THE READING WINDOW** (filed as E3). It includes merge-queue
  time. Mitigated by computing the `write` reading too and printing both on every row —
  **not eliminated**, and 8 of the 21 candidates are CONCURRENT on `wall` only.
- **D6. MY PARENT EXTRACTION IS A LOWER BOUND** (E2). `depends:` + `-followup` tag + a
  1500-character prose window. A landing naming its parent further down is invisible, so
  **13 is a floor, not a census**, and §1 must not be read as one.
- **D7. THE `audit` TAG WOULD HAVE SCORED TWO LANDINGS AS THEIR OWN AUDITORS.** `mg-1319`
  and `mg-a806` are tagged `audit` and are landings *of* an audit's consequences. Caught
  before it mattered only because `s0` has rejection arms; forced there permanently.
- **D8. I AM A LANDING CARRYING mg-5cba's AND mg-8d63's FIGURES** (E4). The five superseded
  values in `s4` are **read** from their records and not recomputed — the ticket forbids
  re-opening them. This report can say where a value sits; it cannot say mg-5cba was right
  about it, and nothing here should be quoted as if it could.
- **D9. E7 WAS CHECKED AND HELD, WHICH IS LUCK.** I filed the risk that `depends:` might be
  advisory in practice. It is not — `mg schedule --help` documents the gate and `mg-5cba`
  is an instance of it holding. Had it been advisory, §4 and the whole of §6 would have
  been an argument for machinery that does not exist, and I filed the check late.
- **D10. `mg-c2b3` SURVIVED ADJUDICATION AND I DOUBT IT.** It is an arc-wide `run_all.sh`
  tooling sweep; whether it "carries figures from mg-821e" is a stretch. **It is left in
  the residue** because no stated rule disqualifies it, and removing it by hand after the
  rules ran is exactly the manoeuvre E5 forbids. The reader who disagrees should read 12,
  not 13 — and P1 would still have lost.

---

## 9. WHAT THIS TICKET DID NOT DO

- **The five figures are NOT re-opened.** Settled on mg-5cba's audited values, credited at
  every site by c8d63. `s4` reads them; nothing recomputes them.
- **`docs/OneThird-SweepLoss-mg-51f4.md:148` is NOT repaired.** It is another ticket's
  landed document. Reported in §3.2 and filed as successor **`mg-d19f`**.
- **Nothing outside `code/landing_audit_sweep_64cb/` is edited.** Checked by
  `git status --porcelain` in `run_all.sh`, printed empty.
- **The rule is NOT enforced anywhere.** §6 shows the predicate runs and answers both ways.
  Wiring it into dispatch is pm-onethird's call and is a separate item — this ticket was
  sent to decide the rule and price it, and it has.
- **`AUDIT-BEFORE` triples were not read.** 15 on wall, 10 on write. If the audit finished
  before the landing started, the landing *could* have read the repaired figures; whether it
  *did* is a different sweep, and a bigger one.
