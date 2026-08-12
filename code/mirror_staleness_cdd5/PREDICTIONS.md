# mg-cdd5 — predictions for THE STALE MAIN-MIRROR SWEEP

Committed **before one line of the sweep instrument exists**. The exposure is
**disclosed rather than laundered**: I established the commit state of both repos
before writing this file, because the ticket's step 1 *is* that establishment and
it is the input to everything else. So the step-1 and step-2 figures below are
**REPORTS at zero credit**, marked `[REPORT]`, and only the sweep predictions
(step 3) are live bets.

---

## Exposure, stated first

**H1 — I have already measured the commit state.** Before writing this file I ran
`git ls-remote`, `merge-base --is-ancestor`, `rev-list --count`, and read the
cited section at both revisions. I know: `origin/main = 949c439` (confirmed
against the true remote, not the tracking ref alone); the checked-out branch is
`main-mirror` at `912f1b1`, **0 ahead / 76 behind**; `bde9610` is an ancestor of
`origin/main`; the struck bullet stands unstruck at line 286 of the mirror's copy;
and `§5.0′` does not occur in the mirror's copy at all. Every one of those is a
`[REPORT]`.

**H2 — I have read the 76 subject lines.** One of them, `a8688f2` (mg-e2a0), says
in its own subject that it landed a repair *"AT ITS DESTINATION — the figure was
still quotable bare in the one document `STATE.md` row 3b points at"*. That is a
commit announcing that it repaired a document `STATE.md` cites, dated after
`912f1b1`. **P1 below is therefore a heavily informed bet and not a blind one**,
and it is priced high for that reason and not because the reasoning is strong.

**H3 — I have counted STATE.md's cross-repo links.** `grep -oE
'\(\.\./one_third_width_three/[^)]*\)' STATE.md` returns **6 occurrences over 5
distinct paths**. `[REPORT]`. I have **not** looked at the twin
(`docs/state-of-the-wall.html`), and I have not diffed any cited file other than
the Reverse-Cheeger document.

---

## Live predictions

| # | p | prediction |
|---|---|---|
| **P1** | 0.85 | At least one cited path **other than** `OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md` has a different blob at `912f1b1` than at `origin/main`. (Informed by H2.) |
| **P2** | 0.45 | At least one of the four *non*-Reverse-Cheeger paths currently linked from `STATE.md` (`step8.tex`, `probe-lambda-constant-bound.md`, `OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md`, `OneThird-L1b-BK-Transport-Transfer-Probe.md`) has changed. |
| **P3** | 0.55 | The twin (`docs/state-of-the-wall.html`) cites **at least one** path inside the mirror repo. |
| **P4** | 0.70 | At least one changed cited file gains an **explicit withdrawal marker** (`~~`, `STRUCK`, `REFUTED`, `WITHDRAWN`) between `912f1b1` and `origin/main` — i.e. the Reverse-Cheeger case is not unique in kind. |
| **P5** | 0.50 | **No cited section NUMBER changes.** `§5` is still `§5` at `origin/main`; `§5.0′` is an insertion, not a renumbering. If this holds, `STATE.md:78`'s citation is **not** edited (ticket step 4). |
| **P6** | 0.95 | `git merge --ff-only origin/main` on `main-mirror` succeeds with no conflict and no working-tree loss: the tree is clean and the branch is 0 ahead. |
| **P7** | 0.40 | A **widened** sweep — every file under `docs/` and `code/` in this repo, not just `STATE.md` and the twin — finds **≥ 5** further citing files whose cited mirror text changed after `912f1b1`. |
| **P8** | 0.35 | The mirror's staleness has **no** deliberate cause: the reflog for `main-mirror` carries exactly one entry (`branch: Created from origin/main`) and nothing has ever advanced it. Scored on the reflog, not on intent. `[near-REPORT — I have seen the reflog; priced as a bet only on whether a second cause turns up elsewhere.]` |
| **P9** | 0.60 | The *reason* the top-level checkout is not simply on `main` is that `main` is **already checked out in another worktree** (`git worktree list` shows one), so `git checkout main` there would refuse. If true, "just check out main" is **not** an available remedy and the mirror branch is structural. |

---

## Ways THIS instrument could exhibit the defect it is about

A remedy is an artifact of the same kind as the defect. Enumerated before it is
built, each one checked in `s3_controls.py`:

- **E1 — resolving against the working copy.** A sweep that reads the cited file
  off disk reads it **at `912f1b1`** and reports "unchanged" for everything,
  because it never sees the other revision. This is the ticket's own defect
  committed by the instrument sent to find it. *Every* read here must be
  `git show <rev>:<path>`; the working copy is never opened.
- **E2 — my own report going stale.** Every figure here is measured at a
  revision. If `origin/main` moves, this document becomes exactly the thing it
  documents. Remedy: the pin is **printed in the transcript** and named in the
  README, and the sweep **re-derives** rather than quoting.
- **E3 — absent ≡ absent scored as unchanged.** A path that exists at neither
  revision compares equal (`None == None`) and a naive differ calls it clean. A
  citation to a file that has never existed is a *worse* finding than a stale
  one, and it must not be reported as green.
- **E4 — the relative link does not resolve from here.** `../one_third_width_three/…`
  is relative to *this repo's parent*, and this instrument runs inside a polecat
  worktree whose parent is `/Users/daniel/.pogo/polecats/`. Naive `os.path.join`
  resolution silently finds nothing. The mirror repo must be located explicitly.
- **E5 — file-level diff over-reports.** `STATE.md:78` cites `§5` and `§5.0′`, not
  the whole file. A file that changed elsewhere is not a stale citation. Where a
  citation names a section, the section is checked, and the file-level and
  section-level answers are reported **separately** rather than merged.
- **E6 — the twin is HTML.** A markdown-link extractor run over
  `state-of-the-wall.html` returns 0 and that 0 reads as *"the twin cites
  nothing"* rather than *"the parser is wrong"*. The extractor must be shown able
  to see an HTML `href` before its zero is quotable.
- **E7 — a measured zero with no population.** The ticket demands the population
  be named. A count of stale citations is meaningless without the count of
  citations swept and the count that could not be resolved.

---

## What is deliberately NOT predicted

Whether the fast-forward is the **right** remedy. That is a judgement, it is
argued in the README on what the update actually contains, and pre-registering a
number for it would be theatre.
