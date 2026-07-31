# mg-4700 — independent audit of the mg-821e repair

Audits `af432ee` + `b534db7` + `41ac5d4` (mg-821e), which repaired mg-6cb9 /
`26c8d5c`, which audited mg-d633 / `e8fbd4f`.

    sh code/species_depth_audit_4700/run_all.sh      # ~6 min, no network

## What this instrument is for

mg-6cb9 left three OPEN items and mg-821e closed all three. Two of the three are
about a distinction that **cannot be seen by reading the code**:

* a **contingent** extent and a **sound** one print the same sentence and exit
  the same way. The only thing that separates them is a subdirectory.
* a call **present** in a script and a call the script **executes** are the same
  bytes. The only thing that separates them is the runner's own stdout.

So nothing here is inferred from source. Every depth claim is measured by
planting a real directory in the real worktree and running the checker; every
wiring claim is measured by executing `run_all.sh` and reading what it printed.

## Files

| file | what it does |
|------|--------------|
| `PREDICTIONS.md` | written and committed **before** any probe ran; never edited |
| `OUTCOMES.md` | the findings, and the predictions that missed |
| `kern4700.py` | mutate-and-prove-the-restore harness, and the copied helpers |
| `selftest4700.py` | 82 assertions, including the restore contract **in both directions** |
| `q1_depth.py` | OPEN 1 — plant subdirectories; and hunt a second unstated condition |
| `q2_wiring.py` | OPEN 2 — 21 `run_all.sh` executions; deletion at the finest unit |
| `q3_sites.py` | OPEN 3 — each anchor deleted at its own site, others left standing |
| `q4_standing.py` | do not disturb what is confirmed — mg-6cb9's battery, unmodified |

## Results

| section | total bad | predictions missed |
|---------|-----------|--------------------|
| Q1 depth | 1 | 1 |
| Q2 wiring | 4 | 0 |
| Q3 sites | 0 | 0 |
| Q4 standing | 2 | 1 |

`Q1..Q4` exit 1 when they have a finding, so a non-zero exit is the instrument
working. `PREDICTIONS MISSED` is not expected to be zero and the misses are kept
as written — see `OUTCOMES.md`.

**All three OPEN items are genuinely closed at their own grain.** OPEN 3 is
closed cleanly: 7 of 7 one-site deletions fire, against 2 of 7 for the checker
it replaced, with the other direction silent 1 of 1 and a renamed heading loud.
OPEN 1's walks really do recurse — a statement planted at depth 3, and in a tree
mg-6cb9 never planted in, is caught. OPEN 2's check really does execute in 3 of
3 runners, with the un-wired control green 3 of 3 so the red is attributable.

What the findings are about is the **edge** of each of those, and one of them is
the same shape one rule over. See `OUTCOMES.md` and
`docs/OneThird-Species-Hopf-Monoids-Sites-IndependentAudit.md`.

## This instrument mutates the worktree

Every probe edits the tree it runs in and restores it. `git status --porcelain`
**and** the full `git diff` are captured before each probe and compared after;
a difference stops the run. `selftest4700.py` tests that contract in the
direction that must fail as well as the one that must pass — a restore checker
only ever seen to pass is worth nothing. Do not kill the run mid-probe: the
restore is in the process.
