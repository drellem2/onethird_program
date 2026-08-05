# mg-1abe — PREDICTIONS, committed BEFORE any script of this census exists

This file is written and committed before `lib_1abe.py` or any `t*.py` of this
census exists in any tree.  Nothing below is revised after the fact.  Where a
prediction misses, the miss is kept in the README with the number that refuted
it.

The ticket's headline is `MEASURE THE BLAST RADIUS`, and it says plainly that
the number is the deliverable and everything else is consequence.  So the
predictions below are predictions about **counts over named populations**, not
about whether a repair works.

---

## 0. DISCLOSURES — measurements already taken, NOT predictions

The arc's rule is that a measurement already in hand is disclosed as a
measurement rather than laundered into a prediction.  Four are in hand before
this file is committed.

**D1 — the population, measured.**  `git ls-files 'code/*/out_*.txt'` on `main`
at `6fb424f` returns **504** transcripts, spread over **133 distinct carrying
commits** and **152 distinct (directory, carrying commit) groups**, where a
transcript's CARRYING COMMIT is `git log -1 --format=%H main -- <path>`.  That
504 is the denominator of every CLASS 2 count in this census.  It is not
predicted; it is counted.

**D2 — one transcript already re-run, and it DOES NOT REPRODUCE.**
`code/anchor_population_audit_0ba7/out_a2_oldest.txt`, carried by `8490669`,
re-run from a detached worktree at `8490669`, differs from the committed bytes
in two places.  Both differences are counts of things OUTSIDE the tree being
measured — `worktree / this worktree` goes `26 28` -> `27 29` and
`history-derived sites` goes `28 29` -> `30 31`.  Nothing in the tree at
`8490669` changed; `main` grew past it.  This is a THIRD cause, and it is
neither of the ticket's two: not a rebase, not a regeneration.

**D3 — the ticket's second finding is already repaired on `main`.**  The
`unreachable[:3]` silent cap in `code/audit_c067/c2_anchors.py` does not exist
on `main`.  It was removed by mg-c3a2 in `5bd0d71`, whose replacement prints
every distinct commit and is documented in a comment at `c2_anchors.py:209`.
The only surviving occurrence of the string `unreachable[:3]` in that file is
inside that comment.  So there is nothing to fix in passing, and this census
will not pretend to have fixed it.

**D4 — the instrument runs, and the cost is real.**  One producer re-run
(`a2_oldest.py` at `8490669`) took **52 seconds** wall clock.  504 producers at
that rate is roughly seven hours on one core.  This machine has 10.  The census
therefore runs in parallel worktrees with a per-producer timeout, and any
producer that exceeds it is reported in its OWN bucket and never folded into
`DOES NOT REPRODUCE`.

---

## 1. Predictions about the CLASS 2 census (the deliverable)

Population: the 504 committed transcripts of D1.  Grain: one verdict per
transcript file.  Method: check out the transcript's carrying commit in a
detached worktree, run the producing command as `run_all.sh` **at that same
commit** spells it, compare bytes.

- **P1.1** — `REPRODUCES` (byte-identical) will be **at least 250 of 504**.
  Point estimate 300.  Most of this arc is deterministic combinatorics that
  never opens `.git`.
- **P1.2** — `DOES NOT REPRODUCE` will be **at least 100 of 504**.  Point
  estimate 150.
- **P1.3** — `CANNOT BE RUN` (producer not derivable from `run_all.sh` at the
  carrying commit, or the script is absent from that tree) will be **between 40
  and 90**.  Point estimate 60.  This bucket exists because 62 of the 504
  transcript names do not match `out_<stem>.txt` -> `<stem>.py` in their own
  directory, which is already measured; how many of those `run_all.sh` rescues
  is not.
- **P1.4** — the three buckets plus the timeout bucket will sum to exactly 504.
  A census whose buckets do not sum to its denominator is not a census.

## 2. Predictions about CAUSE — where I expect to correct the ticket's framing

The ticket asserts one mechanism (refinery rebase) behind three sightings and
adds a fourth (regeneration) in an addendum.  D2 is already a third cause.

- **P2.1** — the LARGEST cause of `DOES NOT REPRODUCE` will be **neither rebase
  nor regeneration**.  It will be producers that measure REPOSITORY-GLOBAL
  state — refs, `git log`, `rev-list`, the set of files on `main` — rather than
  the tree they are checked out at.  Such a transcript is stale the moment the
  NEXT commit lands, on any branch, by anyone.  Predicted: more than half of
  all non-reproducers.
- **P2.2** — there will be at least one non-reproducer whose recorded
  CONCLUSION (its verdict rows / exit code) still holds when re-run, and at
  least one whose conclusion FLIPS.  The ticket is right that displaced is not
  the same as wrong, and this census will show both in the same population.
- **P2.3** — at least one further cause will be found that is in neither the
  ticket nor D2.  Named in advance so it cannot be claimed retroactively: I
  expect **nondeterminism inside the producer itself** (dict/set ordering,
  wall-clock, unseeded sampling, absolute paths) to account for at least one
  non-reproducer.  If I find none, P2.3 MISSED.

## 3. Predictions about CLASS 1 (recorded SHAs — bookkeeping, context)

Population: every SHA-shaped token (7–40 hex chars) appearing in a tracked
`.md`, `.py`, `.sh` or `out_*.txt` file on `main` that resolves to nothing, or
resolves but is not an ancestor of `main`.  Grain: one verdict per (file,
token) site.

- **P3.1** — of the recorded SHAs that are NOT ancestors of `main`, **at least
  90%** will have a patch-id-identical twin that IS on `main`.  STALE, not
  LOST.  This is the mayor's three samples generalised, and P3.1 is the claim
  that they generalise.
- **P3.2** — CLASS 1 will be at least five times larger than CLASS 2 by raw
  count, and will matter less.  Reporting them as one number would overstate
  the damage, which is exactly what the addendum warns against.

## 4. Prediction about the third bucket nobody has counted

- **P4.1** — **ZERO** conflict-resolving rebases in this arc.  Every
  displaced-by-rebase commit I can pair with its pre-rebase twin will be
  patch-id-IDENTICAL.  If any pair differs, that is a genuine content
  discrepancy and it goes in the README in its own section, in bold, because it
  would mean a rebase silently altered committed evidence.

## 5. Predictions about this census's own instrument (self-application)

- **P5.1** — this census's OWN committed transcripts will not all reproduce at
  the commit that carries them.  At least one of mine will be a
  `DOES NOT REPRODUCE`, for exactly the D2 reason: my census reads `main`.  I
  am predicting my own instrument into the defect it is measuring, before
  writing it, because the alternative is to discover it afterwards and call it
  a caveat.
- **P5.2** — the control I ship will go RED on `main` as it stands.  A control
  that is green on first run has not been shown able to fire.

## 6. Prediction about the shape, not the instance

- **P6.1** — the `[:N]`-cap-under-an-`each`-sentence shape that the ticket asks
  me to fix in one file (and which D3 shows is already fixed there) survives
  ELSEWHERE.  There are 1450 `[:N]` slices in `.py` files under `code/`;
  I predict **at least 5** live sites where a truncated list is printed under a
  sentence whose own words claim completeness.  If I find fewer than 5, P6.1
  MISSED and the ticket's generalisation was wrong.

## 7. What I am pre-committing NOT to do

- Not to use `git merge-base --is-ancestor` as the instrument for whether
  content survived.  It answers a different question and gives a confident
  false negative on every rebased commit.
- Not to touch the refinery.
- Not to edit, reword or re-run any other ticket's committed transcript in
  order to make it reproduce.  A transcript that does not reproduce is a
  measurement, and overwriting it destroys the measurement.
- Not to report a producer that exceeded its timeout as `DOES NOT REPRODUCE`.
