# mg-4adb — PREDICTIONS

**Written and committed BEFORE any probe in this directory was run**, and not edited afterwards.
`OUTCOMES.md` scores it. A prediction that missed is kept as written; the miss is the useful part.

The repair is written first and the predictions are about **the repaired tree** — this is a repair
ticket, not an audit, so the interesting question is not "what does the defect do" (mg-6ef4 measured
that) but "does the repair do what it claims, and does its own deletion population contain every
line its gate depends on".

---

## What is being predicted about

Two repairs.

**R1 — the fifth rung.** mg-6ef4's F3: `set -e` sits 53, 60 and 43 lines above the cross-section
call in the three species runners, it is the statement that turns e2's exit code into the runner's,
and it is in **no** deletion population this arc has used. Deleted alone, 3 of 3 runners exit 0 while
printing e2's finding in full.

The repair does **not** add a guard beside `set -e`. mg-4700's F2 already measured what that
produces: a `|| { …; exit 1; }` next to a `set -e` is a line whose deletion changes no verdict,
because the other one catches it — five lines that moved the MESSAGE and not the VERDICT. Adding one
back would be that finding, re-committed. Instead **the gate is moved to the end of the runner**, so
the statement that carries e2's status into the runner's status is the call itself: the exit status
of a POSIX shell script is that of its last command. `set -e` stays, but nothing about the gate rests
on it, and the population that certifies the gate is **every line of the runner file, with no
exclusions at all** — so there is no exclusion to justify.

**R2 — the second layer.** mg-6ef4's F1: an unreadable regular file passes `walk_residue`, fails
`open()`, and is caught by `except (UnicodeDecodeError, OSError)` under a printed sentence saying the
reason was the file's ENCODING — printed, not counted, contents never scanned, `w3_scope.py` exit 0
over a live X4 statement. The repair splits the two exceptions into two named buckets and counts
only the one no sentence covers.

---

## R1 — the deletion population is the whole file

`v1_population.py`. Every line of each of the three runners is deleted alone and the runner is
executed with e2 forced red. 196-odd runs; nothing is sampled and nothing is excluded.

| id | question | prediction | reasoning |
|----|----------|-----------|-----------|
| P1a | with e2 red, how many lines per runner turn it GREEN when deleted alone? | **1, 1, 1** — and in each case the line is the call `python3 ../species_extent_d633/e2_crosssection.py` | after the move the call is the last command, so deleting it is the only way to lose the status |
| P1b | `set -e` deleted alone, e2 red | **1, 1, 1** — still red, and 3 of 3 still print `STANDING UN-STRUCK` | this is the repair; mg-6ef4 measured `0, 0, 0` here |
| P1c | the heading `echo "cross-section check…"` deleted alone | **1, 1, 1** — still red. The heading is INERT and stays inert | mg-6ef4's T2c measured the same; the repair does not claim to change it |
| P1d | do the MEASURED load-bearing lines equal the DECLARED ones? | **yes**, and the declared set is `{the call}` in all three | if it does not, the population is wrong again and the direction of the error is the finding |
| P1e | comment and blank lines, deleted alone | **0 findings** — every one of them leaves the verdict unchanged | they are not statements; but they are deleted anyway, because "obviously inert" is a prediction and this arc has watched one be wrong |
| P1f | lines whose deletion makes the runner red for a reason that is NOT e2 (a broken `\|\|` guard, a lost `cd`) | **> 0 in all three**, and each is reported separately from the gate rows | half of a two-line `\|\| { … }` guard is a syntax error |

## R1b — where `set -e` still carries something, said out loud

`v1_population.py`, second half. `set -e` deleted, and then **each step of each runner forced red one
at a time** — the question mg-6ef4's F3 raises about every OTHER line of these files.

| id | question | prediction | reasoning |
|----|----------|-----------|-----------|
| P2a | `species_repair_a4ef`: steps that exit 0 with `set -e` gone | **0** | every step there already reads its own status with an explicit `\|\|` guard |
| P2b | `species_remainder_f8fa`: same | **0** | same |
| P2c | `species_repair_6f61`: same | **3** — `r1_smallest.py`, `r2_columns.py`, `r3_quotes.py` | those three steps have no guard, and `set -e` is the only thing that reads them |
| P2d | is P2c a defect of this repair? | **no** — it is the disclosure. `set -e` is the single rung for those three steps, it is IN the population, and deleting it is measured to flip their verdict. mg-6ef4's finding was a load-bearing line **outside** the population, not a load-bearing line | adding a second guard beside it would make BOTH look removable, which is mg-4700 F2 |

## R2 — the second layer

`v2_layer2.py`. Planted in `code/species_7d75`, against a no-plant baseline, worktree restored and
proved restored.

| id | plant | prediction | reasoning |
|----|-------|-----------|-----------|
| P3a | a regular file at mode `000` carrying a live X4 statement | `w3_scope.py` **exit 1**, and the file named under a bucket that says UNREADABLE and names `PermissionError` | the repair splits the except |
| P3b | the word ENCODING does not appear on P3a's line | **holds** | a wrong bucket sends the next reader to the wrong hypothesis, which is the half of F1 that matters |
| P3c | `code/species_remainder_f8fa/run_all.sh` with P3a's plant on disk | **exit 1** | w3 is guarded in that runner |
| P3d | a readable file whose bytes are not valid UTF-8, same tree | `w3_scope.py` **exit 0**, file named under a bucket that says ENCODING | a sentence carries that exclusion — the printed extent has said "less the N named as undecodable" since mg-d633 — so it is a STATED decline, like `__pycache__/`, and stated declines are not counted |
| P3e | are P3a's and P3d's printed lines distinguishable to a reader? | **yes**, different bucket word and different reason text | this is mg-6ef4's P1d, inverted |
| P3f | `s1_extent.py` with P3a's plant | **exit 1** | same split, same tree in its four |
| P3g | `e1_extents.py` with P3a's plant | **exit 1**, and it must name the file as NOT read | `trace_open.py` recorded the path before calling the real `open`, so a failed attempt counted as a read; that is reversed |
| P3h | the four species runners and `code/species_extent_d633/run_all.sh` with NO plant | **all exit 0** | the repair must not redden a clean tree |
| P3i | `code/species_extent_audit_6cb9/a1_bothways.py` Q18 — "a non-UTF-8 file added to `species_7d75`, expect exit 0" | **still passes** | this is why P3d is not counted; a landed audit asserts it and the assertion is right |

## R3 — this instrument, held to its own rule

`v3_self.py`.

| id | question | prediction |
|----|----------|-----------|
| P4a | every line of **this** instrument's `run_all.sh`, deleted alone, with one step forced red | the measured load-bearing set equals the declared one |
| P4b | each of this instrument's own steps forced red one at a time | **every one** reddens the runner |
| P4c | does this runner's exit status depend on `set -e`? | **no** — every step reads its own status, and the last statement is an explicit `exit` |

---

## What would falsify the repair

- Any line outside the declared set whose deletion turns a red runner green (P1d).
- `w3_scope.py` exit 0 with an unreadable file carrying a live statement (P3a).
- A clean tree turning red (P3h) — a repair that reddens what was correct has moved the problem, not
  removed it.
