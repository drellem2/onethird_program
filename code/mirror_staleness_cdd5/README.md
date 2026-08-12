# mg-cdd5 — THE MIRROR WAS 76 COMMITS BEHIND, THE SWEEP IS NOT A ZERO, AND THE REPAIR HAD A COST

`pm-onethird` filed this off `p05ec`'s disclosure in `mg-05ec`: `mg-d1be`'s strike
of `λ_std ≤ λ₂^{BK}` is on `one_third_width_three` `origin/main` at `bde9610`, the
checked-out `main-mirror` is at `912f1b1` which predates it, and `STATE.md:78`
cites the section. Everything in that sentence is **CONFIRMED**. The ticket's real
deliverable was the *sweep* — whether any **other** citation lands on superseded
text — and it comes back **NOT ZERO**.

    sh run_all.sh          # ~9.7 s MEASURED; pure Python 3 + git, no third-party packages

Suite exit **0**. Selftest **50 checks, 0 FAIL**. Controls **12 arms, 12
satisfactory**.

---

## 1. The commit state, established from the remote (ticket step 1)

Every command and its answer is in `out_s0_state.txt`. The tracking ref is checked
against `git ls-remote` — asking the remote itself — because confirming a stale
checkout with a *cached copy of the remote* is the ticket's own defect one level up.

| | |
|---|---|
| `git ls-remote origin refs/heads/main` | `949c43926b6e` — **the remote's own answer** |
| `git rev-parse origin/main` | `949c43926b6e` — agrees |
| `git rev-parse --abbrev-ref HEAD` | `main-mirror` |
| `git rev-parse HEAD` (before repair) | `912f1b1498f2`, dated **2026-07-19** |
| `git rev-list --left-right --count HEAD...origin/main` | **0 ahead, 76 behind** |
| `git status --porcelain` | clean |
| `git merge-base --is-ancestor bde9610 origin/main` | **YES** — the strike is on `origin/main` |
| `git merge-base --is-ancestor 912f1b1 origin/main` | **YES** — the mirror is a strict ancestor |

**And the consequence, read at both revisions by `git show` and never off disk.**
At `912f1b1`, line 286 reads

> `- **But \`λ_std ≤ λ₂^{BK}\`** (the standard sector is a subspace): …`

**unstruck.** At `origin/main` the same line is `~~`-struck and blockquoted, and
**`§5.0′` — the section `STATE.md:78` cites by name — does not occur in the
mirror's copy at all.** So the citation does not merely land on stale text: **half
of it does not resolve.** That is sharper than the ticket stated it.

**Why the mirror was stale, and it is structural.** `git reflog show main-mirror`
carries exactly one entry — `branch: Created from origin/main` — and nothing has
ever advanced it. It exists at all because `main` in that repository **is checked
out in another worktree** (`/Users/daniel/.pogo/agents/pm-onethird/repo`), so
`git checkout main` in the top-level directory refuses. *"Just use `main`"* is
therefore **not** an available remedy.

## 2. What bringing the mirror current actually brings in (ticket step 2)

The ticket says do not assume a fetch is safe or sufficient without looking. So
`s1_delta.py` enumerates rather than argues; the whole list is in
`out_s1_delta.txt`.

**Mechanically safe — three facts, not the word "safe":** 0 commits ahead, clean
working tree, `HEAD` an ancestor of `origin/main`. A `--ff-only` merge can lose
nothing. *That is all it says.* It does not say the 133 files it rewrites are ones
a reader wanted rewritten.

**76 commits**, 2026-07-21 → 2026-08-09. **133 files: 123 added, 10 modified, 0
deleted, 0 renamed** — `docs` 53, `scripts` 49, `data` 26, `.github` 2, plus
`README.md`, `.gitignore`, `.pogo`.

The 10 **modified** files are the ones that can withdraw something a reader is
currently reading as live; an *added* file cannot retract a claim nobody has been
sent to. **Five of them gain strike markup:**

| modified file | strike markup gained |
|---|---|
| `docs/OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md` | `STRUCK` ×1, `~~` ×2 |
| `docs/OneThird-L1b-Spread-Locality.md` | `STRUCK` ×3, `~~` ×6 |
| `docs/OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md` | `REFUTED` ×2, `WITHDRAWN` ×1, `~~` ×6 |
| `docs/OneThird-StandardDominance-ComparisonRoute.md` | `REFUTED` ×2, `WITHDRAWN` ×1, `~~` ×8 |
| `docs/OneThird-L1b-BK-Transport-Transfer-Probe.md` | (rewritten, no new markers) |

**So the headline file is not special.** Four other documents withdrew claims in
this window, and the sweep asks which of them anyone is being pointed at.

## 3. THE SWEEP — and it is not a zero (ticket step 3)

`out_s2_sweep.txt`. Two tiers, reported separately and **never merged**.

### Tier 1 — `STATE.md` and its rendered twin `docs/state-of-the-wall.html`

**Population: 6 citations, 5 distinct cited paths, 2 source documents.**

| verdict | count |
|---|---|
| `UNCHANGED` | 2 |
| `CHANGED` | 1 |
| `CHANGED-WITH-STRIKE` | **3** |
| **not clean** | **4 of 6** |

The rows:

| citing | cited | verdict |
|---|---|---|
| `STATE.md:78` | `docs/probe-lambda-constant-bound.md` | UNCHANGED |
| `STATE.md:78` | `docs/OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md` | **STRUCK** — and `§5.0′` absent from the mirror |
| `STATE.md:112` | `docs/OneThird-L1b-BK-Transport-Transfer-Probe.md` | CHANGED |
| `STATE.md:112` | `docs/OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md` | **STRUCK** |
| `STATE.md:112` | `docs/OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md` | **STRUCK** — `REFUTED` ×2, `WITHDRAWN` ×1, `~~` ×6 |
| `STATE.md:115` | `step8.tex` | UNCHANGED |

**`STATE.md:78` was the ticket's example. `STATE.md:112` is a second site the
ticket did not name, and it is worse: it points at TWO withdrawn documents, and
one of them is not the Reverse-Cheeger file at all.** That is `row 3b` — the
standard-dominance row — whose supporting probe was `REFUTED`/`WITHDRAWN` on
2026-08-07 by `a8688f2` (`mg-e2a0`), a commit whose own subject says it landed the
ruling *"AT ITS DESTINATION — the one document `STATE.md` row 3b points at."* **The
ruling landed in the mirror repo and the mirror checkout never received it.**

**The twin's zero is attributable, not merely reported.** `docs/state-of-the-wall.html`
returns 0 cross-repo citations — and it contains **0 `href=` and 0 markdown links
in total**. So the zero is a property of the document, not of the extractor. That
distinction is checked, not asserted: arm E6 plants an `<a href=…>` and shows the
extractor sees it.

### Tier 2 — widened: every `.md/.html/.txt/.py/.sh/.json/.tex/.yml` under `docs/` and `code/`

**Population: 2699 files scanned** (this instrument's own directory excluded,
with the excluded count printed by the run — see D1), **18 citations, 7 distinct cited paths, 12 citing files.**

| verdict | count |
|---|---|
| `UNCHANGED` | 13 |
| `CHANGED-WITH-STRIKE` | **3** |
| `DIRECTORY-REF` | 2 (counted, kept out of the hazard tally) |

**3 more citations in 3 more files**, all pointing at documents that gained
withdrawal markup:

* `code/row3b_audit_eba7/OUTCOMES.md:72` → `OneThird-StandardDominance-ComparisonRoute.md`
* `docs/state-history/audit-mg-eba7-of-mg-55f2.md:112` → the same
* `docs/OneThird-Compression-W1-LinearEigenfunction-Provenance-mg-bb60.md:126` → `OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md`

**`ABSENT-AT-BOTH` is 0 in both tiers: every citation resolves.** That is a
measured zero and it took a parser fix to earn (D2).

### The answer to "a count of any other citations that resolve to superseded text"

**Tier 1: 4 of 6 not clean, 3 of them struck, over 3 distinct mirror documents.
Tier 2: 3 more, in 3 more citing files. The count is NOT zero.**

## 4. The remedy — done, and it is a one-shot

**`git -C /Users/daniel/research/one_third_width_three merge --ff-only origin/main`.**
`main-mirror` `912f1b1` → `949c439`. It moved a branch pointer: no commit created,
no history rewritten, no other branch touched (a pre-existing stash on
`mayor-a5-g2-status` is intact), working tree clean before and after.

**Undo, exactly:** `git -C /Users/daniel/research/one_third_width_three reset --hard 912f1b1`.

`x1_after_repair.py` reads the result back **off disk** — the one place in this
instrument where opening the working copy is the measurement and not the defect —
and confirms line 286 is now struck, `§5.0′` resolves, and the other two swept
documents carry their withdrawal markup too. `out_x1_after_repair.txt`.

**AND IT WILL GO STALE AGAIN.** Nothing advances `main-mirror`. This deliverable
does **not** ship a structural fix, and the reason is stated rather than skipped:
the fix belongs in `one_third_width_three` (a hook, a scheduled fast-forward, or
retiring `main-mirror` in favour of a detached checkout that is obviously not a
branch), and this branch targets `onethird_program`. **What is shipped here is the
detector**, which is the half that belongs in the citing repository: `s2_sweep.py`
answers *"is anything we point readers at superseded"* from any checkout, at any
staleness, because it never reads the checkout.

**Also not done, and named:** no `git fetch` is run by anything here.
`ls-remote` established that the tracking ref already agreed with the remote, which
is a stronger statement than *"I refreshed it and then trusted it."*

## 5. Section numbering, and what was edited in `STATE.md` (ticket step 4)

**No cited section was renumbered.** `§5` is `§5` at both revisions; `§5.0′` is an
**insertion**. Heading sets compared per document, every anchored row in
`out_s2_sweep.txt`. **So no section citation is edited, exactly as the ticket
directed** — the citations are right and the tree they landed in was stale.

**Two LINE anchors were edited, and this is a consequence of the repair, not of the
ticket.** `STATE.md:112` carries `…Proof-Attempt.md:310` and
`…KillShot-Probe.md:286`. Both **quote** the line they point at; both quotes match
**exactly at `912f1b1`** and nothing at `origin/main`, because `bde9610` inserted
`§5.0′` above them. Two consequences:

1. **The anchors were authored against the stale tree.** That is direct evidence,
   caught in the act, that this programme's authors have been reading the mirror
   checkout rather than `origin/main` — which is the ticket's hazard rendered as a
   measurement instead of a worry.
2. **The fast-forward breaks them.** The repair is right for the prose and wrong
   for these anchors, and this deliverable does not pretend it was free.

They are repaired — **`:310 → :449`** (exact text match) and **`:286 → :350`**
(unique 74-character prefix match; the line itself gained the sampling-artifact
warning). Both numbers were **derived by `s4_anchors.py` and never typed**.

**A third integer, and the extractor could not see it.** The same sentence at
`STATE.md:112` also says *"L1b's own document says so in as many words at
`:310–313`"* — a **bare backticked range with no path attached**, invisible to an
extractor that keys on `one_third_width_three/`. Repairing only the linked anchor
would have left `:449` and `:310–313` pointing at the same paragraph from one
sentence. Found by hand, verified by exact text (`449–452` at `origin/main` is the
same four lines), repaired.

**So the bare-reference surface was swept by hand, and the result is stated with
its population.** Every `STATE.md` line that mentions `one_third_width_three` — **3
lines: 78, 112, 115** — was checked for bare backticked line references. `:78`
carries `:81` and `:112` carries `:76`, both references to `STATE.md`'s **own**
lines. `:115` carries **12** bare references and every one is into `step8.tex`,
which the sweep classes **UNCHANGED** between the two revisions, so none of them
moved. **One bare reference into the mirror needed repair and it is the one
above.**

`wc -w STATE.md` is **19750 before and 19750 after**: three integers changed, zero
words.

**Anchors in frozen audit records are LEFT.** `code/row3b_audit_eba7/OUTCOMES.md`
and `docs/state-history/audit-mg-eba7-of-mg-55f2.md` both anchor into
`ComparisonRoute.md:104`; that line was **edited in place**, so those anchors still
stand — but the standing rule here is that a record of what was read at the time is
not improved by being re-pointed at what is true now.

**Authorship is decided only by a quoted span**, ≥ 25 characters, compared modulo
whitespace and inline markup. **Shifting decides nothing** and is not used as
evidence — in a file whose content moved, both directions relocate. Rows with no
usable quote say `UNDECIDED` (1 of 8) rather than guessing.

**The repair erased its own evidence, so the evidence is replayed.** `s4` now reports
those two rows as `TIP-AUTHORED`, because they were fixed. Arm
`PRE-REPAIR-ANCHORS` reads `STATE.md` out of git at `0a8415b` and re-runs the same
decision on it: **both come back `PIN-AUTHORED`.** Without that arm, the finding
would be invisible to the next reader and the repair would look like a retraction.

## 6. FIVE DEFECTS OF MY OWN, ALL KEPT

**D1 — the sweep swept itself.** The first run of `s2` included this instrument's
own directory, and the synthetic citations in the selftest and controls
(`docs/a.md`, a planted `href`, a `%s` inside a format string) produced **10 rows**
— so a sweep whose entire subject is *"does this repository point readers at
withdrawn text"* reported ten broken cross-repo references **that it had written
itself**. Excluded, with the excluded count printed, and arm **D1** fails if that
exclusion ever stops mattering.

**D2 — a parser defect wearing the clothes of a corpus defect.** The corpus writes
line ranges with an **en dash** (`step8.tex:389–394`). A `:(\d+)$` reader leaves the
whole `tex:389–394` in the path, where it resolves at neither revision — reported
as **3 false `ABSENT-AT-BOTH` rows**, i.e. *broken citations*, which is a
worse-sounding finding than the true one. Arm **D2** runs the naive reader beside
the fixed one and shows both answers.

**D3 — the number and the list it labelled came from different sources.** `s1`'s
header printed `st.behind` above a list computed from the pinned range. Identical
until the repair lands, then it read **"0 of them"** above 76 printed rows. The
count now comes from the list.

**D4 — I missed my own sharpest finding, twice over.** The extractor read link
*targets* only. This corpus writes the line anchor in the **display text**
(``[`…Proof-Attempt.md:310`](../one_third_width_three/docs/….md)``), so the first
`s4` reported **`tier-1 anchored: 0`** — a confident zero over the exact rows that
carried the finding. Fixed, and the label channel is in the selftest.

**D5 — and the wrong answer flattered me.** The first authorship rule inferred
`PIN-AUTHORED` from *shifting*. In a file whose content moved, **both** directions
relocate, so that rule is not evidence at all; it got **3 of 5 rows wrong, in the
direction that made the repair look more necessary than measured.** Replaced with
the quote test, which refuses where it cannot decide.

**A sixth, caught before it shipped rather than after:** arm E1 was first written
as `disk == blob@912f1b1`, which goes **RED the day the mirror is brought current**
— red because its own finding was acted on. That is `mg-d0e2`'s shape and is not a
control. It is now scored on two direction-stable facts (disk tracks `HEAD`; the two
pinned revisions differ) with the checkout's staleness **reported, not scored**.

## 7. What this cannot see

* **B1** A citing document outside `docs/` and `code/` in this repository, or one
  whose reference is prose without a path (*"the Reverse-Cheeger document"*). The
  extractor needs `one_third_width_three/` in the text.
* **B2** Whether a `CHANGED` file's change touches the part actually being relied
  on. File-level and section-level are reported separately for exactly this reason,
  but only where the citation names a section.
* **B3** Staleness in the **other** direction: a citing document here that is
  itself out of date about the mirror's content in ways no diff shows.
* **B4** Any repository other than `one_third_width_three`. The mirror name is
  supplied, not discovered.
* **B4b** **A bare line reference with no path attached** (`` `:310–313` ``). The
  extractor keys on the string `one_third_width_three/`, so a prose reference that
  relies on the surrounding sentence for its target is invisible to it. One such
  reference existed in `STATE.md` and is repaired (§5); the by-hand sweep that
  found it covered 3 lines and is not a standing check.
* **B5** Whether a strike marker means the *cited* passage was withdrawn or merely
  some other passage in the same file. `CHANGED-WITH-STRIKE` is a file-level
  statement and the row prints the marker counts so a reader can go look.
* **B6** Anything after `949c439`. **Every figure here is measured against
  `one_third_width_three origin/main = 949c43926b6e`, and that pin is printed in the
  transcript.** If the ref moves, this document is stale — which is the defect it is
  about. Re-run rather than quote (E2).

## 8. Predictions, scored

`PREDICTIONS.md`, committed at `cac9de0` before one line of the sweep existed, with
the exposure disclosed: H1 (the commit state was already measured), H2 (I had read
the 76 subject lines), H3 (I had counted `STATE.md`'s links).

| # | p | outcome |
|---|---|---|
| P1 | 0.85 | **HIT** — 4 further cited paths differ; 2 in tier 1 besides the Reverse-Cheeger file |
| P2 | 0.45 | **HIT** — both `OneThird-L1b-BK-Transport-Transfer-Probe.md` and `OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md` changed |
| P3 | 0.55 | **MISS** — the twin cites nothing; it contains **no links at all** |
| P4 | 0.70 | **HIT** — 3 tier-1 and 3 tier-2 citations land on files that gained `~~`/`REFUTED`/`WITHDRAWN` |
| P5 | 0.50 | **HIT** — no cited section renumbered; `§5.0′` is an insertion; no section citation edited |
| P6 | 0.95 | **HIT** — `--ff-only` clean, 76 commits, no conflict, nothing lost |
| P7 | 0.40 | **MISS** — the widened sweep found **3** further citing files, not ≥ 5 |
| P8 | 0.35 | **HIT** — one reflog entry, `branch: Created from origin/main`, and nothing has moved it |
| P9 | 0.60 | **HIT** — `main` is checked out at `/Users/daniel/.pogo/agents/pm-onethird/repo`, so `git checkout main` in the top-level directory refuses |

**7 of 9.** Both misses are informative. **P3** is the better one: I priced the
twin at 0.55 to cite *something* cross-repo, and it turns out to carry **zero links
of any kind** — so `twin_pin.py`'s per-row reconciliation is the *only* thing
connecting it to anything, and this whole class of hazard cannot reach it. **P7**
overestimated the blast radius by more than half: the cross-repo citation surface of
this repository is **24 citations over 9 distinct cited paths in 13 citing
files**, which is small, and that is a fact
worth having on its own.

## 9. What is NOT done

* **No structural fix to `main-mirror`.** §4 says why and names the options.
* **No `STATE.md` prose edited**, no ledger row touched, no claim landed or
  withdrawn. Two integers, zero words (§5).
* **No frozen audit record edited** (§5).
* **`docs/state-of-the-wall.html` untouched** — it carries no cross-repo links.
* **Nothing scheduled.** `run_all.sh` is run by a person or a gate; this
  deliverable wires it into neither.
* **No claim about whether `λ_std ≤ λ₂^{BK}` is true.** `mg-d1be` settled that; this
  ticket is about who can see the settlement.
