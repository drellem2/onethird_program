# mg-56dc — the independent audit of mg-70c7

`mg-70c7` (`d456f58`, `973ca61`) landed the six findings of `mg-dee4` against
`1ee1f1b` (`mg-7522`), which repaired the three open sites of `682db2c`
(`mg-05eb`), which audited the arc-wide `| tee` sweep `52aeaf4` (`mg-c2b3`).
This tree audits that repair.

Instrument: `sh run_all.sh`, about four minutes, pure Python 3, no dependencies,
no network. Every figure below is printed by a probe here next to the predicate
that produced it, and the transcripts are committed.

**`PREDICTIONS.md` was committed before any probe in this directory existed**
(`6aa043a`), so the order is checkable from `git log` rather than asserted in
the file. **Five predictions missed and are kept as written.**

---

## The one-line verdict

*The six repairs hold where they were pointed and the two population repairs
hold against cases built outside their old definitions — but the repair's own
self-check has the shape of the finding it repairs: **the strictest rule it
applies to anything ranges over the `out_*.txt` of one directory**, its
self-facing marker population is the `*.py` + `*.sh` it faults `mg-7522` for,
its merged "one rule object" is the subject's nine alternatives verbatim and
**drops the one alternative `mg-dee4` named as being in the self rule and not in
the subject's**, and **four artifacts publish `9` for a quantity their own
instrument prints as `10`** — the site count and the row count, exactly the
distinction the repair exists to make.*

---

## The findings

| | finding | where |
|---|---|---|
| **T1c** | `out_r4_property.txt` labels **10** *"executing sites"*; it is a count of **(site, target) match rows**. The distinct-**SITE** count is **9**. `selftestc2b3.py:155` names two `*.sh` on one line and is counted twice under a label that says `sites` | `t1_grain.py` |
| **T1d** | **4** artifacts — the README, the published document, `r4_property.py`'s own docstring (*"a measurement and not a citation of mg-dee4"*) and the **R5a row `OUTCOMES.md` scores HIT** — state **9** where the transcript they point at prints **10** | `t1_grain.py` |
| **T1e** | one quantity, the sites reading `c0_repro.sh`'s status, is published as **10 in 5 files**, **nine in four files**, **nine in three files** and **9**. The differences are whether the instrument counts its own line, and sites against files. No artifact says which | `t1_grain.py` |
| **T2a** | the strictest rule the repair applies to anything — E1, *every count over source carries a grain word* — has the population `M.outs(M.TREE)`: **the `out_*.txt` of one directory**. The four artifacts `R2c` itself calls *"my reader-facing artifacts"* are outside it | `t2_strictest.py` |
| **T2b** | the merged `MARK` is the **subject's nine verbatim, not the union**: `proven` was in the old self-facing rule and in `mg-dee4`'s own D4 union and is **not** in it. `R3a` cannot see this — it puts only the **three** markers the docstring names to the rule | `t2_strictest.py` |
| **T2c** | the self-facing **marker** check runs over `MINE_PY + MINE_SH`; its own `*.md` and the published document are outside it. That is the population half of F3, in the section that repairs F3 | `t2_strictest.py` |
| **T2d** | **the floor item, named in no list:** `lib70c7.figures()` and `lib7522.figures()` are two copies of one rule that **disagree on exactly the value `3`**, while both docstrings say they exclude *0, 1 and 2* | `t2_strictest.py` |
| **T5d** | **the class the PM asked to have counted has 38 members; 1 carried a note at `main` and 2 do after this ticket.** One instance was found by a worker's conscience; the population had not been counted | `t5_fixture.py` |

## What HOLDS, measured rather than assumed

* **The `16 of 16` is at the execution grain and is sound.** Counted both ways
  here under a parser written from scratch: the `git diff` lines are **3 sites
  / 8 executions**, the `| tee` lines are **8 sites / 8 executions** *because no
  loop encloses one*, and that reason is printed rather than assumed.
* **Both population repairs hold against cases outside the old definitions.**
  A target basename invented for this probe is caught by `libc2b3.targets` and
  missed by the two-name rule **read out of `1ee1f1b`, where it still runs**. A
  fixture with no `set -e` is in the widened P2 and outside the errexit-only
  clause of `bee07a1`.
* **F6's clause is direction-blind, and that is the right answer.** A **QUIET**
  fixture of the same shape — the discarded stage fails, the printed answer
  changes, the script still exits **0** — is in the population on the same terms
  as the loud one. Both were run; the loud arm exits **1**, the quiet arm
  exits **0**. **0** direction tests appear in either membership predicate.
* **Nothing was disturbed.** `mg-dee4`'s tree is **byte-unchanged** since
  `ba85387`; both of its disclosures are present verbatim, including the one
  that matters most — that A5's first draft measured reach from **stdout**,
  scored **0 of 5** on a perfect run, and *"would have read A5d's forced-failure
  check as a PASS for the same wrong reason"*. All **4** of `mg-70c7`'s kept
  misses are still scored MISS and all **5** of its recorded instrument defects
  are still recorded.
* **The do-not-disturb figures re-derive.** **7 of 7** rows of the published
  population table at `bee07a1`; the property population at `1ee1f1b^` is
  **exactly the four repaired files** under the errexit clause and **five** under
  the widened one, the fifth being the member the VALUE arm adds; the errexit arm
  at HEAD is **0**; the comparison is still against a fixed pre-repair ref; and
  **8 of 8** executions exit **0**.

## The fixture, and what this ticket added

`code/runner_exit_c2b3/out_k1_census.txt` was **not** regenerated — its body is
byte-identical to the blob at `52aeaf4` and still reads *ticket 1 / re-derived 0
/ DIFFERS*. **The hazard is measured rather than described:** the same census
row re-derived at the ticket's own revision under the repaired regex reads
**1**, so the transcript **will not reproduce** and a reader who re-runs it
concludes the record was wrong.

At `main` the staleness note was at **1 of 3** sites — `k1_census.py`'s
docstring. **This ticket adds it to the other two**: a header on the transcript
itself, above a marker line, with the record below it unaltered; and a note at
`mg-05eb`'s citation. `t5_fixture.py` reads both revisions, so the control is a
commit where the defect is still present.

**The regeneration decision is not revisited.** It was right, it is ratified,
and the file's bytes below the marker are unchanged.

## What this audit does NOT establish, named rather than folded into a total

* **That the value arm is the right widening.** Inherited from `mg-70c7`'s own
  statement of the same limit: it is a disagreement with a definition.
* **`mg-c2b3`'s own 34.** Cited, not re-measured, for the fourth ticket running.
* **That a stale-looking transcript really fails to reproduce.** T5d's criterion
  is *the producing code changed*, which is **necessary and not sufficient**, so
  **38** is an **upper bound** and the direction is stated. The one member known
  to actually not reproduce is measured in T5b.
* **Whether a grain WORD is the right one.** T1a reads the word; T1c is what
  catches a wrong one, and it does it by re-deriving a count at both grains
  rather than by reading its label harder.
* **Every intermediate commit.** Read at `HEAD` and at named refs, on one
  machine.
