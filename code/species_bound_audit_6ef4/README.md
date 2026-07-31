# mg-6ef4 — independent audit of the mg-5040 repair

Audits `3c8f535` + `f93e41f` + `3bc2cf7` (mg-5040), which repaired the three OPEN items
mg-4700 left against mg-821e. Pre-filed in the same action as its parent.

```
sh code/species_bound_audit_6ef4/run_all.sh      # ~12 min, pure Python 3, NO NETWORK
```

`git` is used against this repository, which is local.

## What is in here

| file | what it measures |
|---|---|
| `PREDICTIONS.md` | written and **committed before any probe ran**; never edited |
| `OUTCOMES.md` | the findings, the predictions that missed, and this instrument's own defects |
| `kern6ef4.py` | the header, the checker runner, the pin, and a **mode-aware** probe |
| `selftest6ef4.py` | this instrument's contracts, including the restore proof **in the two directions that must fail** |
| `t1_bound.py` | OPEN 1 — the stated bound against the code, and the **next world-change** |
| `t2_wiring.py` | OPEN 2 — the block by line, and **the fifth rung** |
| `t3_census.py` | the census re-derived, every copy of the figure, and how many times it was **derived** |
| `t4_restore.py` | the floor — `kern5040.Probe`'s restore proof, which no list in the ticket names |

## The three things this instrument does differently, and why

**Its probe is MODE-AWARE.** `kern5040.Probe` snapshots bytes and proves the restore with `git
status --porcelain --untracked-files=all` plus the full `git diff`. Neither of those carries a
file's permission mode beyond the executable bit. T1 has to `chmod 000` a tracked file to ask its
question at all, so the borrowed harness could not have proved its own restore of this audit's
perturbation — which is `t4_restore.py`, measured rather than asserted. `Probe6ef4` snapshots
`st_mode` beside the bytes, records the files it could **not** read by name instead of `except
OSError: pass`, and prints the porcelain delta when the proof fails.

**Every "before" figure is anchored on `4372fae`.** That is mg-5040's own pin, reused deliberately
so "before" means the same thing in both instruments. `selftest6ef4.py` fails if any comparison here
is anchored on `HEAD`, and asserts that the pin does **not** already carry the repair under audit —
including that `set -e` was already at the top of those runners before mg-5040, so the fifth rung is
not something the repair introduced.

**Two columns where the arc has been using one.** A checker that prints a planted filename and a
checker that reports the planted statement are not the same event, and neither is a checker that
exits 1 after printing its verdict and one that exits 1 because it died before reaching it.
`t1_bound.py` prints `names`, `CAUGHT`, `verdict` and `residue` separately. The first version of the
`CAUGHT` predicate matched `s1_extent.py`'s **legend line** and recorded three catches that had not
happened; it is kept in `OUTCOMES.md` and the self-test now asserts the predicate is silent on a
legend.

## What it perturbs, declared

This directory's markdown sits under `code/`, and `e2_crosssection.py` counts every `*.md` under
`docs/` and `code/`. So a live census run is higher than the shipped tree's by the number of markdown
files here. `t3_census.py` counts from **tree objects** at four named revisions and is immune;
nothing here reads the worktree for a census figure. None of these files carries a `~~strike~~`, so
the cross-section check is not perturbed — except inside `t2_wiring.py`'s probe, which plants one
markdown file for exactly as long as the probe runs and removes it.

`t2_wiring.py` executes three `run_all.sh` twelve times. Those runners regenerate the committed
`out_*.txt` beside them and write `__pycache__` directories; both are restored, and the
`__pycache__` removal is limited to directories that were **absent at entry**.

## Exit-code convention

A probe exits **1** when it has a finding and **0** when it does not. `Tn TOTAL BAD` counts outcomes
that contradict **mg-5040's own claims**; `Tn PREDICTIONS MISSED` counts predictions in
`PREDICTIONS.md` that were wrong. **The two are separate on purpose** — a wrong prediction about code
this ticket did not write is information, not a defect.

## Do not kill this run mid-probe

`t1` and `t2` mutate the real worktree and the restore is inside the process. A killed run leaves
three `run_all.sh` with `set -e` deleted. `git checkout -- code/species_*/run_all.sh` puts them back.
This happened twice while the instrument was being written and both times are in `OUTCOMES.md`.
