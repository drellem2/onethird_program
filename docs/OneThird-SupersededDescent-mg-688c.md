# DID ANYTHING DESCEND FROM THE SUPERSEDED READINGS? — mg-688c

**Instrument:** `code/superseded_descent_688c/` (`run_all.sh`, ~4 min).
**Measured against** `one_third_width_three` `origin/main` = `949c439`, mirror revision
`912f1b1`. Every line number into that repository in this document is stated at `949c439`
unless it is explicitly a mirror-era anchor. **If that ref moves, re-run rather than quote.**

---

## VERDICT

**NOTHING DESCENDED.** No live claim in this programme rests on text that was withdrawn
while the `main-mirror` checkout was showing it as live.

That is a zero, so here is what produced it, and here is the part of it that is not a zero:

- **The window is bounded exactly, on both ends**, and it is *not* unbounded:
  **2026-07-21T00:05:09Z → 2026-08-12T21:07:16Z, 22d 21h 02m 07s.** The mirror was **born
  current** and fell behind 28 minutes and 34 seconds later.
- **Four populations swept** — 573 commits, 5,100 work items, 30,364 mail messages, and
  every line anchor in 2,756 tracked files. 124 fingerprint occurrences, 109 carrying the
  withdrawal, 15 bare, **0 descendants** after hand adjudication.
- **TWO STALE READS ARE MECHANICALLY PROVED** — two documents quote line numbers that resolve
  at `912f1b1` and not at `origin/main`, so their authors demonstrably had the stale copy
  open. **Neither of them read withdrawn text.** In both cases what they took out of the
  stale tree is text the withdrawal explicitly leaves standing. That is the substantive
  finding: the hazard was real, it was walked into twice, and it did not bite either time.
- **One agent hit the drift, named it, and routed around it** (`mg-a1db`, inside the hazard
  window). That is on the record below because it is the behaviour that made the zero.
- **One inference in mg-cdd5's commit message does not survive dating** and is corrected
  here. Its measurements are all confirmed.

---

## 1. THE WINDOW, BOUNDED

The `main-mirror` branch carries its entire life in **two** reflog entries — creation and
mg-cdd5's fast-forward, nothing between. That is what "76 behind" means and it is also what
makes the interval exact.

| instant | when (UTC) | what |
|---|---|---|
| `912f1b1` pushed | `2026-07-19T22:08:44Z` | it becomes `origin/main` |
| branch created | `2026-07-20T23:36:35Z` | `main-mirror` from `origin/main` |
| next push (`a90f0f7`, 3 commits) | `2026-07-21T00:05:09Z` | **the mirror falls behind** |
| `merge --ff-only` | `2026-08-12T21:07:16Z` | **the mirror is current again** |

**The mirror was born current, not born stale, and the commit dates say the opposite.** The
first commit past `912f1b1` (`3b1f63b`) has committer date `2026-07-20T23:18:01Z` — eighteen
minutes *before* the branch existed. Read from commit dates alone the branch looks born
already-behind. It was not: those three commits were **pushed together** at
`2026-07-21T00:05:09Z`. Commit date is when a commit was written; only the push is when it
became fetchable, and only the push can open a hazard window. This distinction is used
throughout and it changes several answers.

### The hazard windows are per-claim, and all of them are shorter than 22 days

A citation only resolves into *withdrawn* text from the moment the withdrawal is on the
remote. Before that the stale text and the live text **are the same text**.

| claim | withdrawal pushed | hazard window |
|---|---|---|
| BK1 — the `946` count | `2026-07-29T18:02:52Z` | 14d 03h |
| KS1 / KS2 / KS3 / CR2 — the Kill-Shot and SD-Cayley withdrawals | `2026-08-07T23:16:33Z` | 4d 21h |
| RC1 / RC2 — the `λ_std ≤ λ₂^BK` strike and §5.0′ | `2026-08-07T23:27:31Z` | 4d 21h |
| CR1 — row C3's "exactly the ordinal sums" | `2026-08-09T18:06:45Z` | 3d 03h |

**The three STRUCK-class hazards opened on 2026-08-07 and 2026-08-09**, not on 2026-07-21.
Anything written before those instants was correct when written, whichever tree its author
had open. This is the single biggest reduction in the search space and it is measured, not
assumed: applying it removes **177 of 242** fingerprint occurrences in the commit population
(`s3` X5).

---

## 2. STALE TEXT vs CURRENT TEXT, PER AFFECTED CITATION

Seven citing sites, four cited documents, eight withdrawn claims. Both sides read with
`git show <rev>:<path>` — full transcript in `out_s1_delta.txt`.

### The citing sites (mg-cdd5's not-clean rows)

| tier | citing site | cited document | mg-cdd5's class |
|---|---|---|---|
| 1 | `STATE.md:78` | Reverse-Cheeger-Proof-Attempt | CHANGED-WITH-STRIKE |
| 1 | `STATE.md:112` | Reverse-Cheeger-Proof-Attempt | CHANGED-WITH-STRIKE |
| 1 | `STATE.md:112` | Spectral-NearOrdinalSum-KillShot-Probe | CHANGED-WITH-STRIKE |
| 1 | `STATE.md:112` | L1b-BK-Transport-Transfer-Probe | CHANGED |
| 2 | `code/row3b_audit_eba7/OUTCOMES.md:72` | StandardDominance-ComparisonRoute | CHANGED-WITH-STRIKE |
| 2 | `docs/OneThird-Compression-W1-…-mg-bb60.md:126` | Spectral-NearOrdinalSum-KillShot-Probe | CHANGED-WITH-STRIKE |
| 2 | `docs/state-history/audit-mg-eba7-of-mg-55f2.md:112` | StandardDominance-ComparisonRoute | CHANGED-WITH-STRIKE |

### The claims that were struck

**RC1 — `λ_std ≤ λ₂^{BK}`.** *Struck by `bde9610` (mg-d1be).*
Stale (`912f1b1:286`, unstruck): *"**But `λ_std ≤ λ₂^{BK}`** (the standard sector is a
subspace): Theorem E bounds the gap in the *wrong direction* for the transport quotient."*
Current: the same bullet **struck**, with exact counterexamples — `A₂⊕A₂`: `1 > 2/3`;
`A₃⊕A₃`: `1 > 9/10` — and the note that the parenthetical is a valid schema with a false
hypothesis. The bullet's *conclusion* survives on stronger ground: the two spectra are
**incomparable**, so a bound on `λ₂^{BK}` carries no information about `λ_std` in either
direction.

**RC2 — §5.0′ itself.** *Absent in the mirror.*
`"5.0′"` occurs **0 times** at `912f1b1` and 3 times at `949c439`. This is the sharpest of
the eight and it is not a changed sentence: **the section `STATE.md:78` cites by name does
not exist in the stale copy at all.** A reader following that citation lands on nothing, in
a file that otherwise reads normally, with the refuted bullet standing where the correction
should have been.

**KS1 — Kill-shot 2's verdict word.** *Withdrawn by `a8688f2` (mg-e2a0).*
Stale (`:103`): `## Kill-shot 2 — Standard dominance — **GREEN**`.
Current (`:151`): `~~**GREEN**~~ **GREEN-IN-FRAME ONLY**`, under a scope-correction banner.
The measurements stand; the verdict word does not.

**KS2 — the word "universal".** *Withdrawn by `a8688f2`.*
Stale (`:250`): *"…standard dominance is **universal**, the eigenvector order tracks expected
rank…"* — asserted as a property of posets.
Current (`:308`): *"**'UNIVERSAL' IS WITHDRAWN AND WAS THE WORST SENTENCE IN THIS
DOCUMENT**"* — the unconditional form is REFUTED by 166 moderate-λ `n = 7` refuters outside
the frame; what stays open is the all-pairs-frozen conditional, **which is L1b**.

**KS3 — `0 / 132` quoted bare.** *Withdrawn by `a8688f2`.*
Stale (`:286`): `| standard-dominance failures (n≤6 exhaustive + n=7 top-λ spot) | 0 / 132 |`
— and no consequence of that frame recorded anywhere in the document.
Current (`:350`): **SAMPLING ARTIFACT, NEVER QUOTABLE BARE** — the frame excludes the known
refuters, and `132 = 126 + 6` with only the 126 in the published JSON, so a third-party
check bottoms out at `0/126`.

**CR1 — row C3.** *Struck by `949c439` (mg-24eb), recording mg-d1be.*
Stale (`:75`): *"`λ_std ≤ λ₂^BK` fails **exactly on the ordinal sums**, holds elsewhere —
**[proven]** at `n=4,5`"*, and §2.4's prose *"true generically and fails on a thin,
exactly-identified set"*.
Current: the **"exactly" is FALSE for `n ≥ 7`** and breaks wholesale at `n = 8` (19
indecomposable violators, 16 of width exactly 3). A small-`n` coincidence, not a theorem
with exceptions.

**CR2 — SD-Cayley's `0/132`.** *Withdrawn by `a8688f2`.*
Stale (`:104`): *"Empirically supported, **0/132** (`mgb0a6`). Coherent and nontrivial."*
Current: struck, with **THE BARE FIGURE IS WITHDRAWN**.

**BK1 — the `946` count.** *Corrected by `af7fc2d` (mg-60d3), no strike.*
Stale: *"Exhaustive both-connected posets **n = 3..7** (3, 9, 12, 104, **946** posets)"*,
with no correction present.
Current: a CORRECTED banner — there are **956**, not 946; `iso_signature` is not a perfect
canonical form and collapses 10 classes at `n = 7`; `n = 3..6` unaffected; **no conclusion in
the document turns on the 10.**

⚠️ **BK1's fingerprint is blind and this is stated before any count that uses it.** The
correction was landed as a banner **above** the sentence, so the sentence still reads "946"
at `origin/main`. A bare `946` anywhere is therefore not evidence of a stale read
(`s3` X4).

---

## 3. THE SWEEP

| | population | in a hazard window | occurrences | carries withdrawal | bare |
|---|---|---|---|---|---|
| POP-A | `onethird_program` commits, added lines | 544 / 573 | 65 | 57 | 8 |
| POP-B | macguffin work items | 1,469 / 5,100 | 33 | 28 | 5 |
| POP-C | macguffin mail | 11,573 / 30,364 | 26 | 24 | 2 |
| POP-D | line anchors at HEAD | 2,756 files | 13 unique anchors | — | 9 broken |
| | **total** | | **124** | **109** | **15** |

### The 15 bare hits, adjudicated

Each is printed in full in `out_s2_descent.txt`. None is a descendant:

| # | where | why not a descendant |
|---|---|---|
| 1–4 | `d19d127` — `build.sh` and `code/facts_registry_03cf/f1_adjacency_corollary.py` | uses `0/132` as the **cautionary example** the registry gate exists to prevent — *"a figure quoted away from the population that makes it true"* |
| 5 | `0a8415b` — mg-05ec's stock-take | quotes *"the standard sector is a subspace"* as **the justification that was struck**, alongside §5.0′'s exact witnesses — content that exists only at the tip |
| 6–7 | `7058fbd` — mg-bb60's provenance doc | an **evidence-bound** sentence: the figures *"are read from the documents that publish them and are not re-measured here"* |
| 8 | `c8c60a8` 2026-07-30 | `"CYCLE FOUND after 946 tries"` — a retry counter. Numeric collision, not the poset count |
| 9–10 | `mg-bb60.result.json` | the same evidence bound, in the verdict sidecar |
| 11 | `mg-cdd5.md` | mg-cdd5's own ticket text |
| 12–13 | `mg-a1db.result.json` | **the opposite of a descendant** — see §5 |
| 14–15 | two mails, 2026-07-30 | `"the gate plus the probe both enumerate the 946 posets"` — a CI timeout estimate, and `946` is still the current text's own wording (`s3` X4) |

---

## 4. POP-D — TWO STALE READS, CAUGHT

POP-A/B/C detect a claim being **repeated**. POP-D detects **the act of reading**: a line
number that resolves at `912f1b1` and not at `origin/main` can only have been copied out of
the stale copy. It does not depend on an author reusing anyone's wording, and it is the test
that found something.

Nine anchors at HEAD resolve to different text at the two revisions. **Seven were authored
BEFORE the push that shifted those line numbers** — correct against the live remote at the
moment they were typed, and evidence of nothing. Two were not:

**① `docs/state-history/audit-mg-eba7-of-mg-55f2.md` → `BK-Transport-Transfer-Probe.md:112`**
Written `2026-08-07T22:36:18Z` (`e9ae5e0`, mg-eba7's independent audit of mg-55f2's row 3b).
Line numbers there shifted `2026-07-29T18:02:52Z` — **nine days earlier**. The document
quotes the line verbatim: *"**Every one of the 166 refuters has `δ(P) ∈ {0.473, 0.474,
0.500}`** — i.e. it possesses a near-balanced or balanced pair"*, and says so in as many
words: *"I verified it rather than scoring it."* It verified against the stale copy.
**What it read is not withdrawn.** `af7fc2d` corrected the `n = 7` *count* and nothing else;
the 166-refuters line is untouched and now sits at `:121`.

**② `docs/OneThird-Compression-W1-LinearEigenfunction-Provenance-mg-bb60.md` →
`KillShot-Probe.md:127–142`**
Written `2026-08-12T12:44:57Z` (`7058fbd`) — **inside the Kill-Shot hazard window**, eight
and a half hours before the repair. It quotes Kill-shot 3's sub-claims (a) and (b) —
Kendall-τ 0.857, `85/126` order-identification failures — at mirror-era line numbers.
**What it read is not withdrawn either**, and the withdrawal says so itself: *"Nothing else
in this document is withdrawn. Kill-shots 1, 3 and 4, the N-poset section, and the risk
localization stand as written."* The content now sits at `:180`.

**So the hazard was walked into twice and did not bite either time** — not because anyone
checked, but because both readers happened to be reading the parts of those documents that
the withdrawals left alone.

### Nine broken anchors are now standing, and this ticket does not repair them

The anchors are broken at HEAD whether or not they were correct when written. mg-cdd5 scoped
its anchor repair to `STATE.md`, and editing three further documents is a different job from
answering what descended, so this ticket **reports and does not edit**. `out_s2_descent.txt`
carries the repair table, computed by content match rather than by offset arithmetic:

| citing file | anchor | text now at |
|---|---|---|
| `docs/state-history/audit-mg-eba7-of-mg-55f2.md` | Reverse-Cheeger `:310` | `:449` |
| `docs/state-history/audit-mg-eba7-of-mg-55f2.md` | BK-Transport `:112` | `:121` |
| `docs/state-history/audit-mg-eba7-of-mg-55f2.md` | KillShot `:198` | `:251` |
| `docs/state-history/audit-mg-eba7-of-mg-55f2.md` | KillShot `:20`, `:103`, `:286`; ComparisonRoute `:104` | text rewritten — no verbatim target |
| `code/row3b_audit_eba7/OUTCOMES.md` | ComparisonRoute `:104` | text rewritten — no verbatim target |
| `docs/OneThird-Compression-W1-…-mg-bb60.md` | KillShot `:127` | `:180` |

---

## 5. THE AGENT THAT HIT THE DRIFT AND ROUTED AROUND IT

`mg-a1db`'s result sidecar, written `2026-08-09T23:30:15Z` — **inside the RC hazard window**
— records:

> `git show main:docs/probe-lambda-constant-bound.md | sed -n 60,70p` puts the
> `T`/`S`/`lambda_std` display block exactly at `:65`; §5 and §5.0′ both exist in
> `OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md` (`:277`, `:300`) … **Drifted hard refs
> `:288`/`:310` deliberately not reused — section anchors used instead.**

Three things follow, and all three matter:

1. It read via **`git show main:`**, not off the `main-mirror` checkout, and got `:449` for
   the `L1b ⟺ all-pairs-frozen ⇒ standard dominance` line — the **tip** number. So the
   staleness was confined to the `main-mirror` branch; `main` in the sibling worktree was
   current, and an agent reading through it saw current text.
2. It **noticed the drift** and named it.
3. It **switched to section anchors**, which is the durable form. That choice is a large part
   of why this sweep's answer is a zero.

---

## 6. A CORRECTION TO ONE INFERENCE IN mg-cdd5

mg-cdd5's commit message reports `STATE.md:112`'s two line anchors as *"direct evidence —
caught in the act — that authors here read the mirror checkout"*, on the grounds that both
quotes match exactly at `912f1b1` and nothing at `origin/main`.

**The measurement is correct. The inference does not survive dating.** Those anchors were
authored at `2026-08-07T17:09:24Z` (`276aead`), and the two pushes that shifted those line
numbers landed at `23:16:33Z` and `23:27:31Z` **the same evening**. At the moment they were
typed, the live `origin/main` carried the same text at the same lines — the three affected
documents are **byte-identical** between `912f1b1` and `42499a5`, which was `origin/main`
then. The anchors are consistent with reading *any* tree that afternoon and prove nothing
about which one.

The same test, applied to every anchor rather than to those two, is what turned up the two
reads in §4 that **do** survive dating. This is a correction to one sentence of a commit
message, not to mg-cdd5's work, which found and reported the widened tier itself.

---

## 7. WHAT THIS DOES NOT ESTABLISH

- The sweep is **fingerprint-based**. It finds a descendant that reuses a claim's wording or
  a line number. A descendant that consumed a withdrawn reading and wrote it in words sharing
  nothing with the original is **outside what four regexes over four populations can see**.
  POP-D narrows the gap — a line anchor is wording-independent — and does not close it.
- A reading that left **no artifact on this machine** cannot be swept at all.
- `BK1`'s fingerprint cannot discriminate, for the reason given above. If anything descended
  from the `946` count specifically, this instrument would not distinguish it from the
  current text's own wording.
- Nothing here re-audits the mathematics. Every claim above is of the form *file `F`, at
  revision `R`, line `L`, says `S`*.

**The zero is a measured zero over four named populations inside eight dated windows. It is
not a proof that no reader was ever misled.**
