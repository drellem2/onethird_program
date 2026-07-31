# mg-4700 — PREDICTIONS, written before a single probe ran

Independent audit of mg-821e (`af432ee` + `b534db7` + `41ac5d4`), which repaired
mg-6cb9 / `26c8d5c`, which audited mg-d633 / `e8fbd4f`.

The rule for this file: it is written and committed **before** the instrument is
run, and it is **not edited afterwards**.  Misses stay as written and are named
in `OUTCOMES.md`.  A battery whose expectations are written after the run cannot
be wrong, and a wrong prediction is the only evidence that the run told me
something I did not already believe.

Exit-code convention throughout this arc: a checker exits **1** when it has a
finding, **0** when it does not.  So "fires" = exit 1.

---

## D1 — DEPTH.  The extent said "every regular file"; add a subdirectory and see.

mg-6cb9's F1 was that `EVERY REGULAR FILE` was true **only because no tree under
`code/species_*` had a subdirectory**.  mg-821e says it removed the condition:
all three walks are `os.walk` now.  I do not read the code and conclude that.  I
plant directories and watch.

| id | probe | prediction |
|----|-------|-----------|
| D1a | plant `code/species_7d75/sub/leak.md` carrying X4, run `w3_scope.py` | exit **1**, X4 named at `sub/leak.md` |
| D1b | same tree state, run `s1_extent.py` | exit **1**, `STILL ASSERTED` at `sub/leak.md` |
| D1c | plant at depth **3**, `code/species_7d75/a/b/c/leak.md` | exit **1** from both — `os.walk` has no depth limit |
| D1d | plant `code/species_repair_a4ef/sub/leak.md` (a tree mg-6cb9 never planted in) | `s1_extent.py` exit **1**; `w3_scope.py` exit **0**, because its extent is one tree and says so |
| D1e | plant `code/species_7d75/__pycache__/leak.md` | both exit **0** — and this is CORRECT, because that rule is stated and printed |
| D1f | plant an innocent `code/species_7d75/sub/note.md`, run `e1_extents.py` | exit **0**, and the nested path is PRINTED in the extent line |
| D1g | revert `w3_scope.py`'s walk to `os.listdir`, subdirectory planted, run `e1_extents.py` | exit **1** |
| D1h | same for `s1_extent.py`'s walk | exit **1** |
| D1i | same for `e1_extents.py`'s OWN walk (`regular()`) — the expectation side | exit **1**.  *Low confidence.* If E1's expectation shrinks to match a subject that also shrank, it cannot disagree — but here only E1 is reverted while the two subjects still recurse, so `want <= got` should hold and E1 might instead go **0**.  I predict 1 and expect to be wrong. |

## D2 — HUNTING A SECOND ONE.  What state of the world does the repaired extent still silently assume?

The brief: *a claim true by accident of the current tree is invisible by
inspection; ask of every extent what state of the world it silently assumes.*
`os.walk` does not descend into a **symlinked directory** unless
`followlinks=True`, and none of the three walks passes it.  The symlink is
classified into `dirnames`, so it is never a candidate file either.  That is a
**second directory rule carried by no sentence** — the extent lines name exactly
one, `__pycache__`.  It is invisible today for exactly the reason F1 was
invisible: no tree contains a symlink.

| id | probe | prediction |
|----|-------|-----------|
| D2a | `code/species_7d75/slink -> <outside dir>/` holding `leak.md` with X4; run `w3_scope.py` | exit **0** — SILENT.  The F1 shape, reproduced after the repair. |
| D2b | same, run `s1_extent.py` | exit **0** — silent |
| D2c | same, run `e1_extents.py` | exit **0** — it certifies the extent as TRUE, because `regular()` walks the same way and cannot disagree |
| D2d | symlink to a **file** rather than a directory: `code/species_7d75/slink.md -> <outside>/leak.md` | exit **1** from `w3_scope.py` — `os.path.isfile` follows the link, so symlinked *files* are read.  Only symlinked *directories* are dropped. |
| D2e | does the extent line mention symlinks at all? | **no** — grep of all three printed extents finds no occurrence |

If D2a/D2b/D2c come out as predicted, the repair closed the instance and left the
class open one rule to the side.

## D3 — WIRING.  Verified by RUNNING all three, not by grepping the call.

| id | probe | prediction |
|----|-------|-----------|
| D3a | run `code/species_repair_a4ef/run_all.sh` | exit **0**, and its stdout carries `cross-section check (mg-821e), its own output:` followed by `E2 TOTAL BAD: 0` |
| D3b | run `code/species_remainder_f8fa/run_all.sh` | same, exit **0** |
| D3c | run `code/species_repair_6f61/run_all.sh` | same, exit **0** |
| D3d | restore B1 on disk (a struck claim standing un-struck in another section) and run all three | exit **1** in **3 of 3**, each naming `STANDING UN-STRUCK` |
| D3e | DELETION AT THE FINEST UNIT — remove only the `\|\| { … exit 1; }` guard, leave the `E2OUT=$(…)` assignment, with B1 restored | exit **1** in 3 of 3 **anyway**: under `set -e` a failed command substitution in an assignment already aborts the script.  If so the guard block moves the *message* and not the *verdict*, and the 20-line unit mg-821e deletion-tested is coarser than the unit that has a return. |
| D3f | remove only the two `echo` lines that PRINT the check's output, leave call and guard | exit **0** in 3 of 3 and the output vanishes — the claim "the OUTPUT is printed, not just the call made" has **no guard of its own** |
| D3g | make `e2_crosssection.py` crash (syntax error) and run the three | exit **1** in 3 of 3, but each prints `a struck claim stands un-struck elsewhere` with **no** `STANDING UN-STRUCK` line — a crash reported as a finding it did not make |

## D4 — C4'S ANCHORS, deleted at the reader-facing site only.

| id | probe | prediction |
|----|-------|-----------|
| D4a | for each of the 7 `(site, anchor)` pairs, delete that occurrence **at that site only** and run `check_doc.py` | fires **7 of 7** |
| D4b | delete one copy of `mg-a61f` at a NON-site heading region | exit **0** — silent, correctly: multiplicity elsewhere has no vote |
| D4c | the same 7 one-site deletions against `check_doc.py` **as it stood before the repair** (`af432ee~1`) | fires **2 of 7** — the figure mg-821e claims |
| D4d | delete the body of section 10 leaving its heading | exit **1** |

## D5 — DO NOT DISTURB WHAT IS CONFIRMED.

| id | probe | prediction |
|----|-------|-----------|
| D5a | mg-6cb9's `a1_bothways.py`, unmodified, against the tree as committed | `A1 TOTAL BAD: 0`, exit **0** |
| D5b | mg-6cb9's `a2_crosssection.py`, unmodified | `A2 TOTAL BAD: 1` (R29, that audit's own kept prediction miss), exit **1**, and both F4 rows read `ok` |
| D5c | all four extents measured in BOTH directions at mg-6cb9's own sites | 4 of 4 still measured both ways |
| D5d | the cross-section check demonstrably fires, three ways in two documents | still 3 of 3 |

## D6 — ONE THING NO LIST HERE NAMES.

`41ac5d4` fixed `| tee` swallowing a red self-test **in mg-821e's own runner**,
and its message says: *"Every other run_all.sh in this arc still uses `| tee`;
noted, not touched."*  Two of the three runners this repair edited are in that
set.  The repair had those files open — it added twenty lines to each — and left
the swallow in place.

| id | probe | prediction |
|----|-------|-----------|
| D6a | force `selftesta4ef.py` red, run `code/species_repair_a4ef/run_all.sh` | exit **0** with `*** FAILED ***` on its own stdout — the swallow, live |
| D6b | force `selftestf8fa.py` red, run `code/species_remainder_f8fa/run_all.sh` | exit **0**, same |
| D6c | force `selftest6f61.py` red, run `code/species_repair_6f61/run_all.sh` | exit **1** — 6f61 uses `>` and a guard, so it is already correct |
| D6d | count `\| tee` self-test invocations across every `run_all.sh` in the repo | more than 2; the class is repo-wide and the two here are the ones this repair touched |

## Addendum — written after Q1 and Q2 had run, before Q3 and Q4

Two probes that the sections above do not name.  They are in a separate block
with this heading rather than folded into D4 above, because a prediction written
later is worth less than one written first and the transcript should say which
is which.  Nothing above was edited.

| id | probe | prediction |
|----|-------|-----------|
| D4e | rename the heading a C4 site regex targets, leaving every anchor in place | exit **1**, `NO SUCH SECTION` — otherwise a site whose heading is renamed becomes an unchecked one, silently |
| D4f | sweep: for each of the 5 anchors, every heading region of the repair document that contains it, against the 7 covered `(site, anchor)` pairs | **more regions than pairs** — C4 covers the sites mg-821e chose, and a reader-facing site it did not choose is the same defect one site over |

## Restore contract

Every probe mutates the real worktree and restores it.  `git status --porcelain`
**and** the full `git diff` are captured before each probe and compared after;
any difference stops the run.  Symlinks and planted directories are removed by
path, and `__pycache__` is emptied under every mutated file's directory —
mg-821e's OUTCOMES.md records that stale `.pyc` inverted one of mg-6cb9's
results, and `PYTHONDONTWRITEBYTECODE` is set for every child here.
