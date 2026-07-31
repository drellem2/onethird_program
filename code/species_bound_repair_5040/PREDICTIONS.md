# mg-5040 — PREDICTIONS, written before the instrument was run

Repair of mg-4700's three OPEN items. mg-4700 audited mg-821e (`af432ee` +
`b534db7` + `41ac5d4`), which repaired mg-6cb9 / `26c8d5c`, which audited
mg-d633 / `e8fbd4f`.

The rule for this file: written **before** the probes in `r1`–`r4` were run and
**not edited afterwards**. Misses stay as written and are named in
`OUTCOMES.md`.

Exit-code convention: a checker exits **1** when it has a finding, **0** when it
does not. "Fires" = exit 1.

---

## HONESTY ABOUT WHICH OF THESE ARE BLIND

A repair is written by changing code until it does the thing, so some of what is
predicted here **was already observed at a shell prompt while the change was
being written**. Calling those predictions would inflate the tally, and a tally
that counts confirmations of things already seen is exactly the defect OPEN 3 is
about. So every row below is marked:

* **BLIND** — not observed before this file was committed. A miss here is real
  information.
* **SEEN** — observed once, ad hoc, during development, and re-measured here
  inside the instrument. Recorded for the reader, **scored separately**, and
  never counted as evidence that the prediction was risky.

`P1a`, `P1b`, `P1d` are SEEN: a symlinked directory, a fifo and an unreadable
directory were each planted once by hand against `s1_extent.py` before this file
existed. Everything else is BLIND.

---

## P1 — OPEN 1. The bound is stated, and stating it is what fires.

The repair takes **option 1 of the two mg-5040 names — state the walk's actual
bound** — and states it in code rather than prose: the walk returns every entry
it declined, with the reason, and a declined entry that is not the one stated
`__pycache__` rule is counted into that checker's `TOTAL BAD`.

| id | probe | prediction | |
|----|-------|-----------|-|
| P1a | plant a symlinked directory in `code/species_7d75`, run all four checkers | **4 of 4 exit 1**, each naming the link | SEEN |
| P1b | plant a fifo in `code/species_7d75`, run all four | `w3_scope.py`, `s1_extent.py`, `e1_extents.py` exit **1**; `e2_crosssection.py` exit **0**, because a fifo not named `*.md` is not in its extent at all and saying otherwise would be a wider claim than it makes | SEEN |
| P1c | plant a **broken symlink** named `leak.md` | all four exit **1** — three because it is not a regular file, e2 because it is named `*.md` and is not a regular file | BLIND |
| P1d | plant a directory with mode `000` | `w3_scope.py`, `s1_extent.py`, `e1_extents.py` exit **1** naming `PermissionError`; `e2_crosssection.py` exit **1** for the same reason | SEEN for the first three, BLIND for e2 |
| P1e | the same four probes against the **pinned pre-repair tree** `4372fae` | symlinked directory: `w3_scope.py` **0**, `e1_extents.py` **0**, `e2_crosssection.py` **0**; `s1_extent.py` **1** but for the wrong reason (its `copytree` control follows the link — mg-4700 D2b). fifo, broken symlink, unreadable directory: **0 from all four**, all four silent | BLIND |
| P1f | clean tree, all four checkers | **0 from 4 of 4** — a repair that fires on everything is not a repair | BLIND |
| P1g | does any of the four printed extents now carry its own residue list? | **4 of 4 yes**; and at the pin, **0 of 4** | BLIND |
| P1h | with a symlinked directory planted, does `e1_extents.py` fire on a row that `want <= got` cannot see? | **yes** — `want` and `got` still agree, because E1's walk declines the link too. The row that fails is the residue row | BLIND |

**P1e is the load-bearing one.** If the pre-repair tree also fires, this repair
bought nothing and the difference is somewhere else.

## P2 — OPEN 2. The wiring is one statement, and it is the one with a return.

mg-4700's F2: the 20-line wiring block had three separable parts, two of them
inert under the deletion test that was applied to the block as a whole.

| id | probe | prediction | |
|----|-------|-----------|-|
| P2a | run all three rewired `run_all.sh` on a clean tree | **0 from 3 of 3**, each printing `E2 TOTAL BAD: 0` from the check's own stdout | BLIND |
| P2b | restore B1 (a struck claim standing un-struck) and run all three | **1 from 3 of 3** | BLIND |
| P2c | delete the single `python3 …e2_crosssection.py` line, B1 restored, run all three | **0 from 3 of 3**, and `E2 TOTAL BAD` appears nowhere in the output — one unit, one return, and it carries both the verdict and the printing | BLIND |
| P2d | delete only the `echo` label line above it, B1 restored | **1 from 3 of 3** and the check's full output still present — the label has no return and makes no claim, which is the honest state for a heading | BLIND |
| P2e | count the separable parts of the new block that have a return | **1 of 1**. At the pin: **1 of 3** | BLIND |
| P2f | make `e2_crosssection.py` raise, run the three | **1 from 3 of 3**, and **0 of 3** print `a struck claim stands un-struck elsewhere` — mg-4700's F5, closed as a side effect of deleting the guard that made the claim | BLIND |

## P3 — OPEN 3. The summaries, and how many there really are.

| id | probe | prediction | |
|----|-------|-----------|-|
| P3a | live `A2 TOTAL BAD` at this worktree | **2** | BLIND |
| P3b | how many **commit messages** reachable from the pin state a figure for `A2 TOTAL BAD`? | **3** — `41ac5d4`, `b534db7` and `5c16f5c`. Of those, **2** say `1` and one (the audit that found it) says `2` | BLIND |
| P3c | how many **committed files** state it? | **4**: `code/species_sites_821e/out_a2_6cb9_after.txt` (`1`, and it is the SOURCE both messages copied), `code/species_extent_audit_6cb9/out_a2_crosssection.txt` (`2`), `code/species_depth_audit_4700/out_q4_standing.txt` (`2`), and `docs/OneThird-Species-Hopf-Monoids-Repair-Sites.md` (`1`, in prose) | BLIND |
| P3d | so is the ticket's "three commit messages say 1" right? | **No.** Two commit messages say `1`; the third statement of `1` is in a **document**, and a fourth is the transcript both messages were copied from. I predict the instrument finds **two** commit messages and **two** other uncorrected copies | BLIND |
| P3e | after the repair, how many uncorrected copies of `1` remain **that this ticket can edit**? | **0** — the document is edited, and neither a commit message nor a published transcript may be edited, so both get a correction record instead | BLIND |
| P3f | does `code/species_depth_audit_4700/PREDICTIONS.md`'s `A2 TOTAL BAD: 1` count as an uncorrected copy? | **No**, and the instrument must say why rather than filter it silently: it is a **prediction**, scored `*** MISSED ***` in the same tree's `out_q4_standing.txt`. A figure that has already been marked wrong beside itself is corrected | BLIND |
| P3g | the `out_e2_crosssection.txt` census, regenerated for this commit and then anchored | the count is **right for the revision it names** and the mechanism is **not** repaired; I predict mg-6cb9's `a2_crosssection.py` row `the COMMITTED run's extent line is true at HEAD` still reads red after any subsequent commit that adds a markdown file, and say so rather than claim the row | BLIND |

## P4 — this deliverable, checked for the defect it repairs.

| id | probe | prediction | |
|----|-------|-----------|-|
| P4a | does this instrument's own file walk state its bound and name its residue? | **yes** | BLIND |
| P4b | does this instrument's `run_all.sh` contain a multi-part block whose parts have differing returns? | **no** — every step is one statement with one return | BLIND |
| P4c | is every figure in this instrument's own README/OUTCOMES derived from a run rather than typed? | the instrument checks its own documents' figures against its own transcripts and I predict **0 mismatches** | BLIND |
| P4d | which branches of "check it for the defect it remedies" **cannot** exhibit the defect, and is a reason stated for each? | I predict **2** such branches, each with a stated reason | BLIND |

---

## What this repair does NOT claim

* It does not make any walk **total**. Option 2 was available and was not taken;
  the reason is in the code at each site.
* It does not repair the mechanism behind the stale census. It **anchors** the
  figure so that a stale copy is readable as stale.
* It does not touch mg-6cb9's or mg-4700's instruments. An auditor's battery
  that is edited by the thing it audits has stopped being evidence.
