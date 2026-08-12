# mg-eba7 — INDEPENDENT AUDIT of mg-55f2 (row 3b restated conditionally)

**Verdict: CONFIRMED on all five in-scope checks — and the one escaped copy in this
programme is NOT in this repo. It is in `one_third_width_three`, at
`docs/OneThird-StandardDominance-ComparisonRoute.md:104`, where `0/132` is quoted
bare as "Empirically supported" in a live status table. mg-55f2 could not have
struck it — that repo is not this ticket's — so this is not a failure of mg-55f2.
It is the remaining reach of the finding, and nobody owns it.**

Scope: pm-onethird's re-scope of 2026-08-07 14:16 leaves **checks 1–5 only**.
Deliverable 2 (the width ≥ 3 row, checks 6–9) is withdrawn to mg-5998 and is not
audited here. Predictions were committed at `e5b89c2` before `git show 276aead` was
run and before `STATE.md` was opened.

---

## 0. WHICH VERSION I READ — named, per the dispatch

| | |
|---|---|
| dispatch named STATE.md at | `491d42c79f7628c18cb7a5d197faa9f4600cd6c1` |
| `main` HEAD when I audited | `dafe75910f731927affdf366457d681e262acf62` |
| `STATE.md` **blob** at BOTH | `7f73bfc87b4bc4caab6c836f8c3922a2416863cf` |

**STATE.md has not moved since the dispatch SHA.** I audited blob `7f73bfc`, which
is reachable at `491d42c` and at `dafe759` alike, so the two readings cannot
diverge. mg-55f2 landed at **`276aead`**; `21ee93f` (mg-9adf) and `491d42c`
(mg-b488) touched STATE.md after it. Every finding below is stated at both
`276aead` (did the parent do it?) and `dafe759` (does today's reader meet it?).

**Row 3b survived the two later landings byte-for-byte.** Lines `5`, `13`, `76`,
`95`, `110`, `117` are md5-identical between `276aead` and `dafe759`. **P12
refuted** — I bet at 35% that a hot file edited twice more would disturb the
correction, and it did not.

---

## 1. CHECK 1 — THE ESCAPED FIGURE. I swept for it myself.

I did **not** accept mg-55f2's site list. I derived the ground truth from the
**pre-state** `276aead^` — the parent's input, not its output — and then asked what
the parent had done to each site.

### 1.1 My declared frame (bound at `e5b89c2`, before the grep ran)

Every tracked file at `276aead^` and at `dafe759`, no extension filter. Needles:
`0/132`, `0 / 132` (the source's own spacing), `0 of 132`, bare `\b132\b`, `clean
sweep`, `\b166\b`, `row 3b`, `standard dominance`, `all-pairs-frozen`, `top-λ`.
Also swept: all git commit messages on all refs. **Defect criterion, bound in
advance:** a surviving `0/132` is a defect only if (i) it is *used as evidence* —
as opposed to a probe reporting its own measurement, or a later document quoting
the figure in order to strike it — **and** (ii) the frame is absent from the same
sentence, the same table cell, or the immediately adjacent sentence.

### 1.2 The pre-state site list I derived independently

`0/132` at `276aead^`: **14 occurrences across 6 files.**

| file | pre `276aead^` | parent output `276aead` | today `dafe759` | touched by mg-55f2 |
|---|---|---|---|---|
| `STATE.md` | 5 | 6 | 6 | **yes** |
| `docs/state-of-the-wall.html` | 3 | 4 | 4 | **yes** |
| `docs/OneThird-TheoremE-…-mg-957a.md` | 2 | 4 | 4 | **yes** |
| `docs/OneThird-LIBweak-mg-c3ca.md` | 1 | 4 | 4 | **yes** |
| `docs/state-history/threads-chronology.md` | 1 | 1 | 1 | **yes** |
| `docs/roadmap.md` | 2 | 2 | 2 | **no** |
| `docs/state-history/audit-mg-2eed-of-mg-b488.md` | — | — | 1 | n/a (created after) |

**The sixth file is not a miss.** `docs/roadmap.md` is pm-onethird's own evening
sweep `f8bd3ae`, landed in the commit immediately *before* `276aead`, and both its
occurrences already carry the correction: `:662` states the frame and mg-b0a6's
declaration in full, and `:669` quotes *"a clean sweep like row 3b's `0/132`"* in
order to record that the phrase had escaped. Quotation-as-struck fails my criterion
(i) and I do not score it.

**The seventh file is the correction propagating.** `audit-mg-2eed-of-mg-b488.md`
was written *after* mg-55f2 by a different ticket, and its single occurrence reads
*"the same evidence bound row `:110` keeps for `166`/`0/132`, and I keep it here."*
A later document inheriting the bound unprompted is the strongest evidence I have
that the repair took.

**Result for this repo: 0 escaped sites. `0/132` cannot be quoted bare anywhere in
`onethird_program`.** Every one of the 20 surviving occurrences either carries the
frame, or is a strike-through, or is a quotation of the struck phrase.

### 1.3 The corners a `0/132` grep would miss — swept, all null

- **Spaced variant `0 / 132`** (how the source actually renders it): 1 hit, inside
  row 3b's own verbatim quotation of the source. Clean.
- **Bare `132`** in prose: 60+ hits, **every one unrelated** — the Bratteli
  path-pair count `132/132/99/42`, and `STATE.md:132` line-number self-references.
  No stripped-slash escape.
- **`code/`**: 0 occurrences of `0/132` in any script or output file.
- **`.tex`**: 0.
- **Root `README.md`**: 0 for all needles.
- **Other `.html`**: `docs/state-of-the-wall.html` is the *only* tracked HTML file.
  **P13 refuted** — I bet 30% on a third ledger carrier and there is none.
- **Concept-level escape** (dominance asserted as holding, without the number):
  `standard dominance` occurs in 7 files; the only one mg-55f2 did not annotate is
  `docs/state-history/attempt-mg-a58f.md:70`, and there it is a *route name*
  ("mg-4a86's standard-dominance/Wilson comparison route"), not a claim. Clean.
- **Commit messages** (out of reach of any patch): the phrase survives only in
  mg-55f2's own subject describing the strike and in pm-onethird's roadmap subject.
  **No commit message uses it as evidence. P11 refuted.**

### 1.4 THE ONE ESCAPED COPY — and it is in the other repo

I extended the sweep past my declared frame to `one_third_width_three`, because row
3b's own links point into it and "the escaped copy is the one a future reader
meets" does not stop at a repo boundary. Read-only; no state touched.

**`one_third_width_three/docs/OneThird-StandardDominance-ComparisonRoute.md:104`:**

> `| **SD-Cayley** | λ₂(Cayley walk) = λ_std | Empirically supported, **0/132** (mgb0a6). Coherent and nontrivial. |`

This is a **live status table**, the figure is quoted **bare**, and the status cell
reads **"Empirically supported"**. It fails both halves of my criterion: used as
evidence, no frame. It is the exact pattern the ruling forbids.

Three things must be said precisely, because it is easy to overstate this:

1. **It is a different statement.** SD-Cayley is `λ₂(Cayley walk) = λ_std`, not the
   BK-chain dominance of row 3b. mg-8b64's 166 refuters are BK-chain, and this
   document's own §1.1 is the finding that the `0/132` **does not transfer** to the
   BK reading. **I do not claim SD-Cayley is refuted.** I have not established that
   and neither has anyone else.
2. **The sampling defect transfers even though the statement does not.** The frame
   — `n ≤ 6` exhaustive + `n = 7` top-λ spot only — is a property of the
   *population*, not of which conjecture you read it against. "Empirically
   supported, 0/132" is a frame-limited count presented as support, whichever
   statement it supports.
3. **This is not a failure by mg-55f2.** Its ticket names
   `/Users/daniel/research/onethird_program` as its repo. It could not have struck
   this and was not asked to. **The finding's reach exceeds the ticket's, and the
   remainder has no carrier.**

The sharp edge: **row 3b cites this very document as corroborating** — *"mg-4a86's
audit found the `0/132` is Cayley-walk evidence, not BK-chain evidence, and was
mis-attributed"* — so STATE.md sends the reader to the one place the figure is
still quotable bare.

Adjacent, reported as an observation and **not** scored as the escaped figure per
my E1 guard: the source probe
`OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md` carries `standard dominance |
**holds**` at `:198` and **GREEN** at `:20`/`:103` with no scope qualifier, while
its frame is declared 88 lines later at `:286`. That is a source document's verdict
on its own probe, which my pre-bound criterion exempts — but a reader who stops at
`:198` gets an unqualified "holds".

---

## 2. CHECK 2 — DID THE FRAME TRAVEL WITH THE NUMBER? **YES, at 20 of 20.**

Every surviving occurrence of `0/132` in this repo carries `n ≤ 6 exhaustive + n = 7
top-λ spot` (or a faithful paraphrase) within the same cell or the adjacent
sentence. Verified individually, not by keyword count.

**And the quotation is faithful to the source, which I checked at the source rather
than against the parent's report.** Row 3b quotes the frame as *"standard-dominance
failures (`n≤6` exhaustive + `n=7` top-λ spot) — 0 / 132"* and attributes it to
`KillShot-Probe.md:286`. The source line reads:

> `| standard-dominance failures (n≤6 exhaustive + n=7 top-λ spot) | 0 / 132 |`

**Exact.** The frame is genuinely the source's own wording, not a gloss mg-55f2
constructed — which is the whole load-bearing claim of the finding, and it holds.

Two more source checks, both exact:

- `OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md:310` states `L1b ⟺ "all-pairs-frozen
  ⇒ standard dominance"` **verbatim**, as row 3b (b) asserts.
- The `:310–313` quotation in row 3b — *"reported standard dominance 'universal,'
  but only checked `n≤6` exhaustively and `n=7` at the highest-λ posets; the
  moderate-λ `n=7` refuters, outside that spot-check, violate it"* — reproduces the
  source **word for word** (only the italic markers on *highest* are dropped).

---

## 3. CHECK 3 — WAS THE KIND LAUNDERED BY RELOCATION? **The relocation happened. The provenance followed it — at 4 of 5 sites.**

**The relocation is real and I measured it: `166` occurs 0 times in `STATE.md` at
`276aead^` and 5 times at `dafe759`. Same in the HTML twin: 0 → 3.** mg-55f2
imported mg-8b64's figure into the ledger from another repo's probe document. That
is precisely the move check 3 was written to catch. **P5 held.**

So the only question is whether the provenance travelled. Site by site:

| site | quotes `166`? | carries "read, not re-measured"? |
|---|---|---|
| `STATE.md:110` (**the row**) | yes | **yes**, twice — in the claim cell (*"EVIDENCE BOUND, kept rather than laundered … READ FROM THE TWO PROBE DOCUMENTS AND NOT RE-MEASURED — not by mg-65f5, not here"*) and again in the Evidence cell (*"read, not re-measured"*) |
| `STATE.md:13` | yes | **yes** — *"(166 refuters, mg-8b64, read-not-measured)"* |
| `STATE.md:76` | yes | **yes** — *"mg-8b64 — read, not re-measured"* |
| `STATE.md:95` (Kinds legend) | no | n/a — quotes no figure, and says *"See the row."* |
| **`STATE.md:5`** (top banner) | **yes** | **NO** — *"its **unconditional** form is **REFUTED** (`FP✗`, 166 refuters at moderate-λ `n = 7`)"*. No citation, no bound. |

**FINDING (minor, real, and asymmetric): `STATE.md:5` is the one site where a
measurement-kind mark (`FP✗`) sits beside the figure `166` with no provenance and
no source.** It is the topmost warning block in the file — the first thing a reader
meets, and the very block whose own instruction is *"READ THE `Kind` COLUMN BEFORE
QUOTING ANY ROW"*.

Two things sharpen it rather than soften it:

- **The HTML twin is stricter than the `.md` here.** Its counterpart banner
  (`state-of-the-wall.html:229`) *does* say *"166 refuters, mg-8b64,
  read-not-measured"*, as do `:364` and `:374`. All three HTML sites that quote
  `166` carry the bound; three of the four `.md` sites do. This corpus's recorded
  failure mode is fixing the `.md` and forgetting the twin; here it is **inverted**,
  which is why a twin-diff would not have caught it.
- **The `Kind` vocabulary itself cannot carry the distinction.** The legend defines
  `FP✗` as *"a finite population exhibiting a counterexample"* — silent on whether
  the population is held or read. So `FP✗` alone never encodes U-by-citation, and
  the bound has to be written out at each site. It is, at every site but one.

**Ruling: NOT laundered.** Per the E2 guard I bound in advance, laundering requires
that the file's own vocabulary fail to carry the read-not-measured distinction
*where the reader of row 3b meets it*. It carries it in the row, in both cells, and
at two of the three aggregating sites. **P6 — my single most likely predicted
finding, at 40% — is REFUTED.** I expected the words "read"/"not re-measured" to be
the thing that was missing, and mg-55f2 wrote them out four times.

**Third figure, unbudgeted and therefore checked at source.** Row 3b also states
*"every one of the 166 has `δ(P) ∈ {0.473, 0.474, 0.500}`"*. The evidence bound
sentence names only `166` and `0/132`, so this figure is carried without an explicit
mark. I verified it rather than scoring it: `OneThird-L1b-BK-Transport-Transfer-Probe.md:112`
reads *"**Every one of the 166 refuters has δ(P) ∈ {0.473, 0.474, 0.500}** — i.e. it
possesses a near-balanced or balanced pair"* — **verbatim, gloss included**. It is a
source read like the others and it is accurate. Worth a clause; not a defect.

---

## 4. CHECK 4 — IS THE REFUTATION OVERSTATED? **No. It is bounded, and the bound is argued rather than asserted.**

Every site says the unconditional form is refuted **and** that the all-pairs-frozen
conditional is **OPEN**. Nothing reads as refuting the conditional. **P9 refuted.**

More than that, row 3b **actively defends L1b** in a sentence it did not have to
write: *"Why the conditional survives the refuters, stated because it is a real
limit on them and not a rescue: every one of the 166 has `δ(P) ∈ {0.473, 0.474,
0.500}`, i.e. possesses a near-balanced or balanced pair, so none of them is a
counterexample and none is in the all-pairs-frozen regime; they kill the
unconditional form and leave the conditional untouched."*

**I re-derived that argument rather than accepting it.** δ(P) ≥ 0.473 means the
poset has a pair with balance within 0.027 of even. All-pairs-frozen requires every
pair to be *un*balanced. So none of the 166 is in the regime, and none has δ < 1/3,
so none is a counterexample to the conjecture either. The refuters therefore cannot
touch the conditional. **The reasoning is sound and the figures are at source.** The
expensive direction — killing L1b by accident — did not happen.

---

## 5. CHECK 5 — DID IT UNDERSTATE? **No.**

Row 3b opens with *"This row is NOT independent empirical support for L1b; the half
of it that is open IS L1b"* and repeats it in (b): *"not a second witness for it …
Reading this row as support for L1b records the open problem as its own evidence."*
The same statement is at `:5`, `:13`, `:76`, `:95` and at all four HTML sites. The
defect mg-55f2 existed to fix is gone from every site that carried it. **P7, P8
held.** The ticket closed correctly.

**The parent's restraint is also correct and disclosed.** `STATE.md:81` still
carries a stale `FP` for row 3b in its body — and mg-55f2 appended a note *at that
paragraph* saying so (*"Row 3b's mark in it is stale … so 'the reduction rests on an
`n ≤ 7` check' understates it"*) rather than rewriting a paragraph that belongs to
`mg-a1db`'s patch. Annotating in place beats silently editing another ticket's
target, and beats leaving it unmarked.

---

## 6. TWO THINGS WRONG WITH THE PARENT'S COMMIT SUBJECT — which is what the next agent greps

Neither changes the verdict; both are the kind of claim that rots into a false
belief, and this ticket exists because of one of those.

1. **"in BOTH files" undercounts the diff to 2 of 5.** mg-55f2 edited `STATE.md`,
   `docs/state-of-the-wall.html`, `docs/OneThird-LIBweak-mg-c3ca.md`,
   `docs/OneThird-TheoremE-…-mg-957a.md` and
   `docs/state-history/threads-chronology.md`. The roadmap entry gets it right ("2
   files and 3 further documents"); the commit subject does not, and the subject is
   the artifact that survives in `git log`. The error runs in the safe direction —
   it did *more* than it claims.
2. **"the ESCAPED 'clean sweep' phrase … struck at every site it reached, in BOTH
   files" conflates the phrase with the figure. The phrase never reached both
   files.** At `276aead^`, `clean sweep` applied to row 3b occurs in exactly **one**
   file — `STATE.md:117` — plus pm-onethird's own roadmap quotation of it. It is
   **0** in `docs/state-of-the-wall.html`. What reached both files was the *figure*
   `0/132` and the `FP` *mark*, and mg-55f2 correctly fixed all of those. **P2
   refuted**: I bet 70% the phrase was in both files and it was in one.

---

## 7. THE WITHDRAWN CHECKS 6–9 DID NOT EVAPORATE — I checked, because my brief told me to

The width ≥ 3 row is **absent** from `STATE.md` at `dafe759` (rows present: 1, 2,
3a, 3b, 4, 5, 6, 7, 8, 9, 10, 11; no `Linial` anywhere; `Sah` only in the
pre-existing literature paragraph at `:207`, untouched). **Its absence is the
re-scope working and I do not score it. P10 held.**

**And the handover held.** `mg-5998` is still `available` (not yet landed), and
`mg-8d4b` is pre-filed against it with the check in its own title, verbatim: *"…and
check the width>=3 row did not re-inherit Sah's exception class."* **The check my
dispatch was worried about losing is carried.** Nothing to report as lost.

---

## 8. PREDICTION SCORING — 8 held, 6 refuted, all as written at `e5b89c2`

| | bet | outcome |
|---|---|---|
| P1 | ≥3 pre-state sites, ≥2 outside row 3b [80%] | **HELD** — 14 occurrences, 6 files |
| P2 | phrase in both `.md` and `.html` pre-state [70%] | **REFUTED** — one file only (§6.2) |
| P3 | 0 live "clean sweep" in either file today [75%] | **HELD** — only strike-throughs and prohibitions |
| P4 | ≥1 surviving `0/132` outside the two files [45%] | **HELD** — 5 files |
| P4b | ≥1 of those is a defect [30%] | **REFUTED in this repo** (0). Held only outside my declared frame, in `one_third_width_three` (§1.4) — scored refuted, because the frame was declared first |
| P5 | `166` absent from STATE.md pre-state [55%] | **HELD** — 0 → 5. The relocation is real |
| P6 | `FP✗` marked without read-not-measured **[40%, my most likely finding]** | **REFUTED** — written out four times |
| P7 | row states (a) REFUTED with 166 / mg-8b64 [85%] | **HELD** |
| P8 | row states (b) conditional OPEN and IS L1b [80%] | **HELD** |
| P9 | refutation overstated, kills L1b [20%] | **REFUTED** — it defends L1b explicitly |
| P10 | no width ≥ 3 row [88%] | **HELD** |
| P11 | phrase survives as a *use* in a commit message [50%] | **REFUTED** — only as self-description |
| P12 | row 3b disturbed by the two later landings [35%] | **REFUTED** — 6/6 lines md5-identical |
| P13 | a third ledger-carrying file [30%] | **REFUTED** — one `.html` in the tree |
| P14 | mg-5998 unlanded **and** the Sah check lost [60%] | **SPLIT** — unlanded yes; check **not** lost (mg-8d4b) |

**E1 fired and I obeyed it.** Four sites tripped my grep that a looser criterion
would have scored: `roadmap.md:669`, `KillShot-Probe.md:286`,
`ComparisonRoute.md:110–111` and `audit-mg-2eed:…`. All four are quotation, source
measurement, or the strike itself. The criterion was written before the grep ran
and it is the reason the only defect I report is a status cell in another repo,
rather than a pile of false positives.

---

## 9. WHAT I DID NOT DO

- **I did not re-measure `166`, `0/132`, or `δ(P) ∈ {0.473, 0.474, 0.500}`.** They
  stay U-by-citation on my side too. What I did was stronger than accepting them and
  weaker than measuring them: I opened the two probe documents and **checked the
  quotations are faithful to their sources**, character by character. That verifies
  transcription, not the underlying computation. If mg-b0a6's probe miscounted, this
  audit does not catch it and neither did mg-65f5 or mg-55f2.
- **I did not run any instrument.** No script, no enumeration, no poset was built.
  This audit is documentary throughout and every claim in it is a `git grep`, a
  `sed`, an `md5`, or a hand reading. There is no code in this branch.
- **I did not audit deliverable 2.** Withdrawn by pm-onethird's 14:16 re-scope;
  checks 6–9 belong to whatever audits mg-5998, and mg-8d4b carries them.
- **I did not verify Linial 1984, read Sah beyond what STATE.md:207 already prints,
  or re-derive δ(E) = 1/3.** All of that is mg-5998's.
- **I did not settle whether SD-Cayley survives the sampling frame.** §1.4 reports
  that the figure is quoted bare there; it does **not** claim the statement is
  false, and I have no evidence either way.
- **I did not patch `one_third_width_three`.** It is not this ticket's repo and not
  this branch's target. §1.4 is a finding to be carried, not a fix.
- **I did not fix `STATE.md:5`.** §3's finding is minor, it is in a hot file with
  `mg-a83c` and `mg-bb87` still pending on it, and an auditor editing its parent's
  landing mid-flight is how two tickets acquire one conflict. It is reported, with
  the exact missing clause named and the HTML twin's correct wording available to
  copy.
- **I did not read mg-55f2's verdict mail or its predictions**, by design, so §1's
  site list is derived from `276aead^` and not from anything the parent said about
  itself.

---

## DRIFT NOTE — this document's cross-repo line anchors, and why none of them is edited (mg-96df, 2026-08-12)

**Appended, never inserted.** Every line number above is exactly where it was;
`code/anchor_drift_96df/a2_controls.py` fails if that stops being true. This
document is itself cited by line — `docs/OneThird-SupersededDescent-mg-688c.md`
and `code/mirror_staleness_cdd5/README.md` both anchor at `:112` — so a banner
at the top of this file would have broken two live anchors while repairing a
report about broken anchors. That is why this is at the bottom.

**WHAT MOVED.** §1.4, §2 and §3 anchor into `one_third_width_three` by line
number. Those numbers resolve against **`912f1b1`** (2026-07-19) — the revision
this repository's *mirror checkout* stood at, and had stood at for nineteen days,
when this audit was written. That branch was never advanced until mg-cdd5
fast-forwarded it to **`949c439`** on 2026-08-12 (`4ce7da3`). So the anchors were
correct against the bytes on disk and were **never** checked against the cited
repo's `origin/main`; `af7fc2d` had already moved one of them nine days earlier.
*"Nobody made a mistake, the target moved"* is the right conclusion for the wrong
reason: what these authors read was a stale checkout, not a moving target.

**THE NUMBERS ARE NOT CHANGED, AND THAT IS THE RULING, NOT AN OMISSION.**
mg-cdd5 settled this class in writing, naming this file, when it repaired
`STATE.md` and stopped: *"Anchors in frozen audit records are LEFT … the standing
rule here is that a record of what was read at the time is not improved by being
re-pointed at what is true now"* (`code/mirror_staleness_cdd5/README.md`, §5).
Renumbering would make this document assert a reading that did not happen, and
would erase the evidence that the drift occurred at all. What is owed is this
note, at the site.

**WHERE THE CITED TEXT IS AT `949c439`.** Machine-derived by content match, never
typed and never by offset arithmetic; re-derive with
`code/anchor_drift_96df/run_all.sh`. **The `at 949c439` in this heading is
load-bearing** — these numbers are true at that revision and nowhere else, which
is the whole defect this note is about, so the section names in the last column
are the half that keeps working.

| cited above as | at `949c439` | how it was matched | durable form — the section it is in |
|---|---|---|---|
| `ComparisonRoute.md:104` (top verdict block, and §1.4) | **`:104` — it did not move** | same number, 78 identical leading characters, then rewritten | `## §1 Three inequivalent statements called "standard dominance"` |
| `:20` (§1.4) | `:68` | 125-char prefix; 360 chars appended, strike added | `## Executive verdict` |
| `:103` (§1.4) | `:151` | 43-char prefix; 20 chars appended, strike added | `## Kill-shot 2 — Standard dominance` |
| `:198` (§1.4) | `:251` | **exact** | `### The N-poset: the skeptical-bar centrepiece` |
| `KillShot-Probe.md:286` (§1.4, §2, §8) | `:350` | 73-char prefix; 487 chars appended | `## Data appendix` |
| `Reverse-Cheeger-Proof-Attempt.md:310` (§2) | `:449` | **exact** | `### 5.0′ Correction to the bullet above (mg-d1be)` |
| `:310–313` (§2) | `:449–452` | **exact**, all four lines, one offset | same section |
| `BK-Transport-Transfer-Probe.md:112` (§3) | `:121` | **exact** | `### 2.1 The naive single-cut reading is FALSE (the 166 refuters)` |

**NONE OF THE EIGHT LACKS A TARGET.** mg-96df's originating ticket reports four
of nine as *"text rewritten, no verbatim target … they need a human to decide"*.
That is an artefact of exact matching meeting this corpus's repair idiom, which
is to **append** a strike and a warning to a line rather than replace it: a row
that gained `~~…~~ ⚠️ **WITHDRAWN**` is byte-different and is the same row. Every
one of them relocates on a prefix of 43 characters or more. `:286 → :350` is not
even a new derivation — mg-cdd5 derived it from a *"unique 74-character prefix"*
and applied it to `STATE.md` at `4ce7da3`, so the *unrepairable* row and its
completed repair have been sitting in this repository together.

### The two things renumbering would not have fixed, which are the reason this note is prose

**1. §1.4's finding HAS BEEN ACTED ON, and §1.4 does not know it.** The escaped
bare `0/132` was struck at its destination by **`a8688f2`** (mg-e2a0,
2026-08-07T22:20:29Z), in a commit whose subject is *"land mg-55f2's 0/132 ruling AT ITS
DESTINATION — the figure was still quotable bare in the one document `STATE.md`
row 3b points at."* At `949c439` that cell reads
*"~~Empirically supported, 0/132~~ ⚠️ **THE BARE FIGURE IS WITHDRAWN**"*.

*The timing is given both ways because the two clocks disagree in direction and
one of them would flatter this note.* `e9ae5e0`, which committed this document,
carries **author** date `21:33:04Z` and **commit** date `22:36:18Z`: the strike
landed **47 minutes after this audit was written and 16 minutes before it was
committed**. Neither figure decides anything, and that is the point — the author
could not have seen the strike on either reading, because the checkout they were
reading stood at `912f1b1`, nineteen days behind. (The originating ticket gives
`23:16:33Z` for this commit, a *push* time; it is not the author or commit date
in either repository, and on push time the strike lands 40 minutes after the
audit's commit rather than 16 before it.)

So the present tense of §1.4 — *"This **is** a live status table, the figure
**is** quoted bare"*, *"nobody owns it"*, *"the part of the finding that still
has no carrier"* — was true for about three quarters of an hour and is false now.
**The finding was correct and it was picked up.** Nothing about the audit's
verdict changes; what changes is that its open item is closed, and the anchor
that would have shown you so still resolves perfectly. **This is a staleness no
renumbering could have reached**, because the line never moved.

**2. The `:20`/`:103`/`:198` observation is now HALF true, and the surviving half
is the sharp one.** §1.4 closes by observing that the probe carries `standard
dominance | **holds**` at `:198` and **GREEN** at `:20`/`:103` *"with no scope
qualifier"*. At `949c439`: `:20` (now `:68`) and `:103` (now `:151`) **both
gained the qualifier** — `~~**GREEN**~~ ⚠️ **GREEN ONLY INSIDE THIS PROBE'S
FRAME**` and `~~**GREEN**~~ **GREEN-IN-FRAME ONLY**`. `:198` (now `:251`) is
**byte-identical and still unqualified**; what it gained is a parenthesis five
lines below it explaining that the row is a per-poset readout on the N-poset and
is *"flagged and deliberately left, mg-e2a0."* So the sentence *"a reader who
stops at `:198` gets an unqualified 'holds'"* **still stands**, and it is now the
only part of that observation that does — deliberately, and on the record.

### And the argument against renumbering is measured, not preferred

The cited document's own banner tries the renumbering, by hand, at `949c439`
lines 22–24: *"`STATE.md` row 3b cites this document at `:286`, which … is
`:345` after it. Line refs into this file made before 2026-08-07 are off by +59
from here down."* **Both figures are wrong by five.** The row is at `:350`, not
`:345`; the offset for it is `+64`, not `+59`; and there is no single offset to
quote — the five anchors above move by `+48`, `+48`, `+53`, `+53` and `+64`. The
file has been byte-identical since `a8688f2`, the one commit that moved anything
in it, so this is not drift: **the hand-written renumbering was wrong the day it
was written and has been wrong ever since.** The same banner's first instinct is
the right one and it is two lines earlier — *"Sites are named by section, not by
line."* That is a defect in `one_third_width_three` and is reported, not fixed
here; this repository does not own that file.

