# mg-d53d — PREDICTIONS

**INDEPENDENT AUDIT of the mg-4adb repair** (`4bb4384`, which landed mg-6ef4's two OPEN items).
Written and committed **before any probe in this directory exists**, and not edited afterwards.
`OUTCOMES.md` scores it. A prediction that missed is kept as written; the miss is the useful part.

---

## What was already done before this file was written, and it is disclosed

mg-330a's practice: anything already observed is named here rather than presented later as a
prediction that happened to hold.

1. Read, at HEAD: the three species runners, `v1_population.py`, `kern4adb.py`,
   `e2_crosssection.py`, `kernd633.py`, `w3_scope.py`'s repaired `except` split, mg-4adb's own
   `README.md` and `PREDICTIONS.md`, mg-6ef4's `t3_census.py`, and `code/species_7d75/run_all.sh`.
   **No transcript of mg-4adb's was read as evidence for any number below** — `out_v1_population.txt`
   is parsed by this instrument in section G1f, which is a measurement of *that file*, not a source
   for a prediction.
2. Executed clean, with no mutation and nothing planted: the three runners (exit 0, 0, 0; 6.6 s,
   4.2 s, 27.8 s) and `e2_crosssection.py` (exit 0, 0.55 s). These are timings and a baseline.
3. **Observed, not predicted (G5a).** Running `code/species_repair_a4ef/run_all.sh` and
   `code/species_remainder_f8fa/run_all.sh` on a worktree with no `__pycache__` directories rewrites
   their committed transcripts: `out_s1_extent.txt` moves `DECLINED, STATED -- 9 entr(ies)` to `6`
   and `out_w3_scope.txt` moves `1 stated` to `0 stated`. The committed transcripts are only
   reproducible on a tree where the sibling trees already carry a `__pycache__`, which is untracked.
   No verdict moves. Because this was seen before this file existed it is scored as an observation
   and not as a hit.
4. Counted from the source, before any probe: the three runners are 83, 85 and 87 lines (255);
   `e2_crosssection.py` is 299 lines; `kernd633.py` is 252.
5. `git diff 77306a7..HEAD -- code/species_bound_audit_6ef4/` was run and is empty. Q18 below still
   states it as a prediction because the *second half* of Q18 — that the repair added no
   self-excluding predicate anywhere — has not been measured.

---

## The frame: what population certifies the gate

mg-6ef4's finding was **not** "`set -e` was load-bearing". It was: *the line whose removal breaks the
gate was outside the population that certifies the gate.* mg-4adb answered by making the population
**every line of the runner file, with no exclusion list**.

This audit asks that question of the thing that actually carries the verdict. The runner's exit
status is now its last command's, and that last command is `python3
../species_extent_d633/e2_crosssection.py`. So a red verdict travels:

    e2_crosssection.py  ->  its process exit code  ->  the runner's exit code  ->  the reader

`kernd633.py` is imported by `e2_crosssection.py` and computes the finding itself. The **verdict
path** is therefore 255 + 299 + 252 = **806 lines**, and mg-4adb's certified population is the first
255 of them. This audit deletes each line of all three files itself.

---

## G1 — the deletion population, checked from outside its own definition

`g1_population.py`. Every deletion is made by this instrument's own operator and every runner
execution is this instrument's own, from the repository root.

| id | question | prediction |
|----|----------|-----------|
| Q1 | my own sweep of the 255 runner lines, e2 forced red: lines per runner whose deletion turns a red runner GREEN | **1, 1, 1**, and in each case the line is `python3 ../species_extent_d633/e2_crosssection.py` |
| Q2 | my 255 dispositions against the 255 rows of mg-4adb's committed `out_v1_population.txt`, row for row | **255 of 255 agree** |
| Q3 | the certified population's size, read out of that transcript, and how many of its rows are lines of a file other than the three runners | **255 rows, 0 of them** |
| Q4 | `e2_crosssection.py`, 299 deletions, strike live: how many leave e2 **exit 0** | **2** — `bad += len(fires)` and `sys.exit(1 if bad else 0)` — and **both print the finding** |
| Q5 | each Q4 line, with the three runners executed | **6 of 6 exit 0**, and 6 of 6 print `STANDING UN-STRUCK` while doing it |
| Q6 | `kernd633.py`, 252 deletions: how many leave e2 exit 0 | **0** — Python's indentation turns most of them into a raise, and `E2b`'s controls catch the ones that quietly disable the detector |
| Q7 | deletions that lose the gate and lie **outside** mg-4adb's certified population | **2**, against a verdict path of **806** lines of which the certificate covers **255** |

**Q4 and Q7 are the primary claim of this audit.** If they hold, mg-6ef4's finding is still live one
level down: the two lines whose deletion turns a red gate green are in no deletion population this
arc has ever used, and the certificate reads 100% anyway.

## G2 — can each runner go RED?

`g2_red.py`.

| id | question | prediction |
|----|----------|-----------|
| Q8 | every step of the three runners forced red one at a time (15 steps: 4 + 5 + 6) | **15 of 15** leave the runner non-zero |
| Q9 | a natural input per runner — a4ef a planted strike, f8fa an unreadable regular file, 6f61 a document violation `check_doc.py` catches | **exit 1, 1, 1** |
| Q10 | `set -e` deleted alone with the strike live, at HEAD, and at the pin `77306a7` | HEAD **1, 1, 1** with the finding printed 3 of 3 — status and printed content **agree**; pin **0, 0, 0** with the finding printed 3 of 3 — they **disagree** |

## G3 — the misclassification, and its three parts checked separately

`g3_layer2.py`. The ticket's warning is that the parent may fix the bucket and leave the silence, so
the bucket, the exit code and the runner are three rows and not one.

| id | question | prediction |
|----|----------|-----------|
| Q12 | a regular file at mode `000` carrying a live X4 statement: the line `w3_scope.py` prints for it | says **UNREADABLE / REACHED AND NOT READ** and names `PermissionError`; the word `ENCODING` is **not** on it |
| Q13 | `w3_scope.py`'s exit code with that plant, asked separately from Q12 | **1** |
| Q14 | `sh code/species_remainder_f8fa/run_all.sh` with that plant, asked separately from Q13 | **exit 1** |
| Q15 | a **readable** file whose bytes are not valid UTF-8, same tree | `w3_scope.py` **exit 0**, bucket says ENCODING — the STATED decline is intact |
| Q16 | an unreadable `*.md` under `code/`, against `e2_crosssection.py` — the fourth checker mg-4adb measured and did not repair | **exit 1 by uncaught traceback**, and `STANDING UN-STRUCK` **not** printed |
| Q17 | an unreadable **directory** (mode 000) under `code/` holding a `*.md` — a case no list in either ticket names | `os.walk`'s `onerror` fires, the entry lands in **NOT STATED**, and e2 exits **1** |

## G4 — the self-reference, which must be left alone

`g4_self.py`.

| id | question | prediction |
|----|----------|-----------|
| Q18 | `git diff 77306a7..HEAD -- code/species_bound_audit_6ef4/`, and any predicate added anywhere by the repair that excludes an instrument's own files or commits from a population it counts | **empty**, and **0** such predicates — no regression |
| Q19 | mg-4adb's own three `.md` files in `census(HEAD)`, and any self-exclusion in `t3_census.py`'s `git log --all` population | **3 of 3 present**, **none** — the self-reference is intact |
| Q20 | this instrument's own `.md` files, once committed | **join the census too, and are not excluded** — the same disclosure, made by the audit rather than repaired |

## G5 — floor, not scope: the FOURTH species runner

Nothing in either ticket names `code/species_7d75/run_all.sh`. It is the fourth species runner,
mg-4adb's `P3h` used its exit 0 as evidence that the repair does not redden a clean tree, and it is
in **no** deletion population in this arc, including mg-4adb's.

| id | question | prediction |
|----|----------|-----------|
| Q21 | of the 7 scripts that runner calls, how many end in an **unconditional** `sys.exit(0)` and contain no other exit — asked of the parsed source, not of a sample | **6** (`t1`..`t6`); `selftest.py` is the one that does not |
| Q22 | those six executed standalone | **exit 0**, 6 of 6, whatever `TOTAL BAD` they print |
| Q23 | the runner's last command | **`grep -h "TOTAL BAD" out_t*.txt`** — not a checker call, so the rung mg-4adb installed in three runners is **absent from the fourth** |
| Q24 | a step replaced by a stand-in that prints `T1 TOTAL BAD: 7` and exits 0, which is what the real script does for any value of `bad` | the runner exits **0** while its own output prints `TOTAL BAD: 7` |
| Q25 | a step forced to exit 1 | the runner exits **1** — it can go red for a **crash**, and that is the distinction |

**If Q21–Q25 hold, `code/species_7d75/run_all.sh` cannot be made to go red over any finding its own
battery makes** — and this arc has already found and repaired exactly this defect once, in
`w3_scope.py`, whose own comment records it: *"mg-a4ef: this was `sys.exit(0)` unconditionally"*.

---

## What would falsify this audit

- Q1 measuring anything other than 1, 1, 1 — then mg-4adb's own headline figure does not reproduce
  under a different instrument, which is a larger finding than anything below it.
- Q4 measuring 0 — then the second layer is closed and the primary claim of this audit is wrong.
- Q10's pin column not reproducing 0, 0, 0 — then the before-state was not what mg-6ef4 and mg-4adb
  both describe, and every after-figure proves less than it appears to.
- Q21 measuring 0 — then the fourth runner reports its own findings and G5 is noise.
