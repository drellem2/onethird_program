# mg-56dc — predictions, written BEFORE any probe in this directory was run

The independent audit of `d456f58` / `973ca61` (mg-70c7), which landed the six
findings of `mg-dee4` against `1ee1f1b` (mg-7522).

**Provenance, stated rather than implied.** Every number below was written from
reading the sources and the committed transcripts of `code/runner_exit_repair_70c7/`,
`code/runner_exit_repair_7522/`, `code/runner_exit_c2b3/` and
`code/runner_exit_audit_dee4/`, and from two throwaway `python3 -c` reads of
`lib7522.MARK` / `MARK_OLD` at the terminal. **No probe in this directory
existed when this file was written**, and the commit that carries it carries no
probe and no transcript, so the order is checkable from `git log` rather than
asserted here. Misses are kept, not corrected into hits.

---

## The grain question, which is the primary target

| id | prediction |
|---|---|
| **T1a** | Every count `mg-70c7` prints can be classified SITES / EXECUTIONS / FILES / OTHER by reading the label it is printed with. I predict **between 60 and 130** printed count lines across its 7 transcripts, and that **at least 2** carry a label whose grain disagrees with the artifact prose that quotes the same quantity. |
| **T1b** | The `for pair in …` loop of `state_delegation_audit_16eb/run_all.sh` at `1ee1f1b^` holds **2** pipeline SITES and runs **6** discarded `git diff` EXECUTIONS; `state_delegation_repair_0049/run_all.sh` holds **1** site and runs **2**. Total **3 sites / 8 executions**. The 8 `\| tee` lines of the two `run_audit.sh` are in **no** loop, so there **8 sites = 8 executions**, and the published `16 of 16` is therefore sound at the execution grain. |
| **T1c** | `out_r4_property.txt` labels **43** and **10** as *"executing sites"*. I predict these count **(site, target) MATCH ROWS**, not sites: `selftestc2b3.py:155` names two different `*.sh` on one line and is counted twice. Distinct sites: **42** and **9**. |
| **T1d** | The README, the published document, `r4_property.py`'s own docstring and `OUTCOMES.md`'s **R5a HIT** row all state **9** for the quantity its own transcript prints as **10**. So a figure the repair calls a measurement is stated at a grain its own instrument does not print. |
| **T1e** | `out_r5_population.txt` prints *"external sites naming `c0_repro.sh` … **10** in **5** file(s)"*; the published document says *"**nine** sites in **four** files"*; `lib7522.consumed`'s docstring says *"**nine** sites in **three** files"*. **Three numbers for one quantity**, and the difference is whether the instrument counts its own line. I predict all three readings reproduce. |

**T1 findings predicted: 3. Predicted exit code 3.**

## The strictest rule, run against the prose

| id | prediction |
|---|---|
| **T2a** | `r6_self.py`'s **E1** is the strictest rule this repair applies to anything — *every count over source must carry a grain word*. Its population is `M.outs(M.TREE)`, i.e. the `out_*.txt` **of one directory**. The README, `OUTCOMES.md`, `PREDICTIONS.md` and the published document — the four artifacts `R2c` itself names as *"my reader-facing artifacts"* — are **outside it**. I predict **at least 3** count lines in those four artifacts that the E1 rule, run unchanged, reports as having no grain word in their window. |
| **T2b** | `lib7522.MARK_OLD` (the old self-facing rule) has 3 alternatives, one of which — **`proven`** — is **not in the merged `MARK`**. `mg-dee4`'s own transcript names it: *"in SELF and not in SUBJECT 1 proven"*, and `mg-dee4`'s own D4 used a **10**-alternative union. So *"one rule object"* is the SUBJECT's nine **verbatim**, not the union, and `R3a` cannot see this because it only puts the **three markers the D4 docstring names** to the rule. |
| **T2c** | `r6_self.py`'s R6c applies the marker rule to `MINE_PY + MINE_SH` — **this tree's own `*.md` and the published document are outside it**, which is the population half of F3 reproduced inside the repair of F3. I predict **at least 1** marker USE in those four artifacts that the R6c population cannot reach. |
| **T2d** | **THE FLOOR ITEM — nothing in the brief names this.** `lib70c7.figures()` drops a number when `v <= _SMALL` with `_SMALL = 3`; `lib7522.figures()` keeps it when `v > 2`. **Two copies of the same figure rule that disagree on exactly one value: `3`.** `R3c` compares its own UNBACKED count against `out_s5_self.txt`'s, which was computed under the other copy. I predict the two functions differ on `3` and agree on every other integer in `0..500`. |

**T2 findings predicted: 4. Predicted exit code 4.**

## The population, not the instance

| id | prediction |
|---|---|
| **T3a** | **F5, a case outside the OLD definition.** A fixture line executing `zz_probe_56dc.sh` — a basename that is neither `run_all.sh` nor `run_audit.sh` and did not exist when either rule was written — is **caught** by `libc2b3.targets` at HEAD and **missed** by the two-name rule as it stands at `1ee1f1b`. Predicted: caught at HEAD, missed pre-repair. |
| **T3b** | **F6, a case outside the OLD definition.** A fixture with **no `set -e`**, a real pipeline whose output is captured and read, is `consumed` **True / arm VALUE** under the repaired clause and **False** under the errexit-only clause of `bee07a1`. Predicted: caught at HEAD, missed pre-repair. |
| **T3c** | **F6's failure direction.** The repaired clause never reads the direction, so a **QUIET** member of the same shape — a script whose discarded stage failing changes the answer and still exits **0**, printing nothing — is in the population on the same terms as the loud one. I predict `consumed` returns True/VALUE for the quiet fixture, and that the forced-failure arm of it exits **0** where `c0_repro.sh`'s exits **1**. If the rule turned out to catch only the loud one it would be a different rule, and that is the thing being checked. |
| **T3d** | Neither `lib7522.consumed` nor `libc2b3.targets` mentions a failure direction in the code that decides membership. Predicted: **0** direction tests in either predicate. |

**T3 findings predicted: 0. Predicted exit code 0.**

## Do not disturb, and preserve the disclosures

| id | prediction |
|---|---|
| **T4a** | `code/runner_exit_audit_dee4/` is **byte-unchanged** since `ba85387`. Its two disclosures — the A5 reach-from-stdout defect that *"scored 0 of 5 and 0 of 3 steps reached on two runners that had completed perfectly"* and *"would have read A5d's forced-failure check as a PASS for the same wrong reason"*, and the kept **P4** prediction miss — are present verbatim. Predicted: **0 files changed, 2 of 2 disclosures present**. |
| **T4b** | `mg-70c7`'s own kept misses are still written as misses: **R4b, R6c, R6d, R6e** — **4** MISS rows in `OUTCOMES.md` — and the five recorded instrument defects are still five. Predicted: 4 and 5. |
| **T4c** | The population table at `bee07a1` re-derives as **P0 72**, **P1 23 / 53**, **P2 (errexit) 19 / 26**, **P2 (either) 20 / 27**, **shape 19 / 42**, **name 17 / 34**. Predicted: all six reproduce. |
| **T4d** | The property population is **exactly the four repaired files** at `1ee1f1b^` and **0** at HEAD, and the comparison anchor is a **fixed pre-repair ref** (`1ee1f1b^` / `bee07a1`), not a moving one. Predicted: 4 and 0, anchor fixed. |
| **T4e** | The **8** discarded `git diff` executions all exit **0**, re-derived here under my own parser. Predicted: 8 of 8. |

**T4 findings predicted: 0. Predicted exit code 0.**

## The fixture, and the population of fixtures

| id | prediction |
|---|---|
| **T5a** | `code/runner_exit_c2b3/out_k1_census.txt` was **NOT** regenerated: its blob at HEAD is **identical** to its blob at `52aeaf4`, and it still reads `setting pipefail  ticket 1  re-derived 0  DIFFERS`. Predicted: identical, DIFFERS present. |
| **T5b** | Re-derived live at HEAD, the same census row reads **ticket 1 / re-derived 1 / AGREES**. That is the hazard: the transcript **will not reproduce**, and a reader who re-runs it concludes the record was wrong. Predicted: AGREES at HEAD. |
| **T5c** | Before this ticket, **1 of 3** places carries the staleness note: `k1_census.py`'s docstring does (*"it predates the mg-7522 repair"*, with a pointer to the corrected reading); **`out_k1_census.txt` itself does not**, and **`mg-05eb`'s citation at `code/runner_exit_audit_05eb/README.md:40` does not**. I predict 1 of 3 at `main` and 3 of 3 at HEAD after this ticket. |
| **T5d** | **The class has not been counted.** I predict **between 2 and 8** committed transcripts in this repository that are cited by prose as evidence of a defect **and** do not reproduce at HEAD because the defect was repaired, and that **at most 3** of them carry an explicit note saying so. |

**T5 findings predicted: 0 after the notes are added. Predicted exit code 0.**

## Exit codes, every one, predicted before the run

| step | predicted exit |
|---|---|
| `selftest56dc.py` | **0** |
| `t1_grain.py` | **3** |
| `t2_strictest.py` | **4** |
| `t3_population.py` | **0** |
| `t4_standing.py` | **0** |
| `t5_fixture.py` | **0** |
| `run_all.sh` | **0** — the runner reports each probe's code and does not adopt it |

**7 of 7 predicted.** A non-zero probe exit is how a probe here reports findings,
which is `mg-dee4`'s convention and is stated in `run_all.sh`.

## What I am NOT predicting, named rather than folded into a total

* **That any of the six findings is wrongly repaired.** T3 checks the two
  population repairs against cases outside the old definitions; it does not
  argue that the definitions are the right ones.
* **`mg-c2b3`'s own 34.** Cited, not re-measured, for the fourth ticket running.
* **Every intermediate commit.** Read at `HEAD` and at named refs, on one
  machine — inherited from the same limit stated by every tree in this arc.
