# `mg-e720` is pinned to an as-of commit (`mg-20ee`)

Both scripts in this directory printed **addresses into things they do not own**, computed from
live state. Under `mg-20ee` they read that state **at a declared commit** instead — the method
`mg-c824` proved on `code/c3_audit_a94c3/a4_census.py`.

## `verify_landing_claims.py` — the evidence is `git log` walks, and they were unbounded

Every `-S` / `-G` / `-60` walk started at `HEAD`, so each answered *"whatever the history looks
like when you happen to run me"*. That is worse than a moved address here, because **the walks
are scored as verdicts**.

`AS_OF` is now `8fab006`, and **it is the parent of the commit carrying the transcript, not that
commit.** Pinning at the carrying commit `7f04902` leaves exactly one line wrong: the `-60` walk
then reaches `7f04902` itself and reports it among the commits saying *"changes behaviour"*. An
instrument is **run before it is committed**, so the history it measured is the history *without*
its own commit. At `8fab006` the committed transcript reproduces **byte-identically** — checked
before a line of it was edited. It is an ancestor of `main`.

### Two verdicts move against today's history, and they are REPORTED, not pinned away

The ticket's rule is that anything moving a verdict is a **finding**, not a pinning. `E720_AT=HEAD`
moves two:

| verdict | pinned | at `HEAD` |
|---|---|---|
| *no commit ever added the row to `STATE.md`* | `REPRODUCED` | **`REFUTED`** |
| *the A6 narrowing attributes its quotation to the right commit* | `REFUTED` | **`REPRODUCED`** |

The first flips because the `-S`/`-G` walks now reach `cc4c663`, `bdcb006`, `57f962f`, `b80dea0`,
`e16e41c` and `bbe83b5` — commits that were **not in this audit's history when it ran**. Some are
genuinely later work (`cc4c663`, 2026-08-06, rewrote `STATE.md` into an executive summary); others
carry 2026-07-30 dates and are reachable today only because the branch was rebased. **Which of
those two causes dominates is not adjudicated here** — it is named so that whoever owns the claim
can decide. This audit's own verdict, over its own history, is unchanged and reproduces exactly.

## `attack_artifact_check.py` — it copied the attacked battery from the working tree

The script copies `code/face_geometry/`, mutates the copy, and reports **which line** of the
produced artifact carries the banner. Copying from the working tree made those line numbers move
whenever anyone amended `controls.py`, and they already had: a re-run on 2026-08-13 reports the
injected banner at **line 67** where the transcript says **60**.

The battery is now materialised with `git archive` at `AS_OF`. *"The committed tree is never
modified"* still holds and is now stronger — the tree is not even read.

## Both directions measured

- **Unchanged corpus**: both transcripts regenerate `+18 / -0` and `+25 / -0` — the stamps are
  added and **not one existing line moves** — and two consecutive `run_all.sh` runs are
  byte-identical.
- **Changed corpus**: `E720_ATTACK_AT=HEAD` moves 12 lines in `out_attack.txt` and **every route's
  outcome is identical** — no attack that was repelled now succeeds, and none that succeeded is
  now repelled. `E720_AT=HEAD` moves 18 lines in `out_verify.txt`, of which the two verdicts above
  are the findings recorded here.

Escape hatches: `E720_AT=<commit>` and `E720_ATTACK_AT=<commit>|WORKTREE`.
